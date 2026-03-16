"""
Scriptedness Evaluation Experiment.

Pulls ~100 calls from vt-sales-intelligence Supabase (full_team_sell + expert_close),
runs the scriptedness prompt via Claude, and saves per-call scores plus an analysis report.

Usage:
    python scripts/scriptedness_eval.py
    python scripts/scriptedness_eval.py --limit 100
    python scripts/scriptedness_eval.py --skip-fetch   # re-run scoring on cached calls
    python scripts/scriptedness_eval.py --skip-score   # re-run analysis on cached scores
"""

import argparse
import json
import math
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from statistics import mean, median, stdev
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

_env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                k, v = _line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import requests

try:
    import anthropic
except ImportError:
    sys.exit("ERROR: anthropic package not installed. Run: pip install anthropic")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
PROMPT_PATH = os.path.join(PROJECT_ROOT, "prompts", "scriptedness.md")

OUT_DIR = os.path.join(PROJECT_ROOT, "data", "results")
CALLS_CACHE = os.path.join(OUT_DIR, "calls_sample.json")
SCORES_PATH = os.path.join(OUT_DIR, "raw_scores.json")
REPORT_PATH = os.path.join(OUT_DIR, "scriptedness_analysis.md")

SALES_TYPES = ["full_team_sell", "expert_close"]
MIN_DURATION = 240
DEFAULT_LIMIT = 100
MAX_WORKERS = 5

DIMENSIONS = [
    "language_register",
    "responsive_flow",
    "information_pacing",
    "contextual_anchoring",
    "conversational_ownership",
]


def ensure_env():
    missing = []
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_SERVICE_KEY:
        missing.append("SUPABASE_SERVICE_KEY")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if missing:
        sys.exit(f"ERROR: Missing environment variables: {', '.join(missing)}")


def supabase_get(table: str, params: dict[str, str]) -> list[dict[str, Any]]:
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=180)
    resp.raise_for_status()
    return resp.json()


def fetch_calls(limit: int) -> list[dict[str, Any]]:
    """Fetch calls from Supabase, stratified by outcome."""
    fields = ",".join([
        "id", "interaction_id", "started_at", "transcript_type",
        "audience_segment", "call_outcome", "contact_duration_seconds",
        "rep_performance_score", "discovery_quality", "objection_handling_score",
        "rapport_building_score", "active_listening_score", "close_confidence",
        "transcription_text",
    ])

    half = limit // 2

    booked_params = {
        "select": fields,
        "transcript_type": f"in.({','.join(SALES_TYPES)})",
        "contact_duration_seconds": f"gt.{MIN_DURATION}",
        "call_outcome": "eq.booked",
        "order": "started_at.desc.nullslast",
        "limit": str(half),
    }
    booked = supabase_get("calls", booked_params)

    non_booked_params = {
        "select": fields,
        "transcript_type": f"in.({','.join(SALES_TYPES)})",
        "contact_duration_seconds": f"gt.{MIN_DURATION}",
        "call_outcome": "neq.booked",
        "order": "started_at.desc.nullslast",
        "limit": str(limit - half),
    }
    non_booked = supabase_get("calls", non_booked_params)

    combined = booked + non_booked
    valid = [c for c in combined if c.get("transcription_text")]
    print(f"Fetched {len(booked)} booked + {len(non_booked)} non-booked = {len(combined)} total ({len(valid)} with transcripts)")
    return valid


def load_prompt() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def render_prompt(template: str, transcript: str) -> str:
    rendered = template.replace("{transcript}", transcript)
    rendered = rendered.replace("{{", "{").replace("}}", "}")
    return rendered


def parse_json_output(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        end_idx = len(lines) - 1
        if lines[end_idx].strip() == "```":
            text = "\n".join(lines[1:end_idx])
        else:
            text = "\n".join(lines[1:])

    end = text.rfind("}")
    if end < 0:
        raise ValueError("No closing brace found")
    depth = 0
    start = -1
    for i in range(end, -1, -1):
        if text[i] == "}":
            depth += 1
        elif text[i] == "{":
            depth -= 1
            if depth == 0:
                start = i
                break
    if start < 0:
        raise ValueError("Could not find matching opening brace")
    return json.loads(text[start : end + 1])


def score_call(
    client: anthropic.Anthropic,
    call: dict[str, Any],
    prompt_template: str,
    call_index: int,
    total: int,
) -> dict[str, Any]:
    call_id = call["id"]
    transcript = call.get("transcription_text", "")

    result = {
        "call_id": call_id,
        "transcript_type": call.get("transcript_type"),
        "call_outcome": call.get("call_outcome"),
        "audience_segment": call.get("audience_segment"),
        "contact_duration_seconds": call.get("contact_duration_seconds"),
        "rep_performance_score": call.get("rep_performance_score"),
        "discovery_quality": call.get("discovery_quality"),
        "transcript_length": len(transcript),
        "scores": None,
        "error": None,
    }

    rendered = render_prompt(prompt_template, transcript)

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": rendered}],
        )
        raw = message.content[0].text
        parsed = parse_json_output(raw)
        result["scores"] = parsed
        composite = parsed.get("composite", {}).get("composite_score", None)
        print(f"  [{call_index+1}/{total}] {call_id[:12]}... type={call.get('transcript_type')} outcome={call.get('call_outcome')} composite={composite}")
    except anthropic.BadRequestError as e:
        err_msg = str(e)
        if "prompt is too long" in err_msg.lower():
            result["error"] = "prompt_too_long"
            print(f"  [{call_index+1}/{total}] {call_id[:12]}... SKIPPED (prompt too long)")
        else:
            result["error"] = err_msg
            print(f"  [{call_index+1}/{total}] {call_id[:12]}... ERROR: {err_msg[:80]}")
    except Exception as e:
        result["error"] = str(e)
        print(f"  [{call_index+1}/{total}] {call_id[:12]}... ERROR: {str(e)[:80]}")

    return result


def run_scoring(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt_template = load_prompt()
    total = len(calls)
    results = []

    print(f"\nScoring {total} calls with model={MODEL}, workers={MAX_WORKERS}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(score_call, client, call, prompt_template, i, total): i
            for i, call in enumerate(calls)
        }
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda r: r["call_id"])
    return results


def safe_stat(values: list[float], func, default=0.0):
    if not values:
        return default
    try:
        return round(func(values), 2)
    except Exception:
        return default


def generate_report(scores: list[dict[str, Any]]) -> str:
    scored = [s for s in scores if s.get("scores") and not s.get("error")]
    errored = [s for s in scores if s.get("error")]
    total = len(scores)

    booked = [s for s in scored if s.get("call_outcome") == "booked"]
    not_booked = [s for s in scored if s.get("call_outcome") != "booked"]

    lines = []
    lines.append("# Scriptedness Evaluation — Analysis Report")
    lines.append("")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"**Generated**: {ts}")
    lines.append(f"**Model**: {MODEL}")
    lines.append(f"**Total calls**: {total} ({len(scored)} scored, {len(errored)} errors)")
    lines.append(f"**Booked**: {len(booked)} | **Not booked**: {len(not_booked)}")
    lines.append("")

    lines.append("## 1. Score Distributions")
    lines.append("")
    lines.append("| Dimension | Mean | Median | Std Dev | Min | Max |")
    lines.append("|-----------|------|--------|---------|-----|-----|")

    for dim in DIMENSIONS:
        vals = []
        for s in scored:
            sc = s["scores"].get(dim, {}).get("score")
            if sc is not None:
                vals.append(float(sc))
        display = dim.replace("_", " ").title()
        lines.append(
            f"| {display} | {safe_stat(vals, mean)} | {safe_stat(vals, median)} | "
            f"{safe_stat(vals, stdev) if len(vals) > 1 else 'N/A'} | "
            f"{min(vals) if vals else 'N/A'} | {max(vals) if vals else 'N/A'} |"
        )

    composites = []
    for s in scored:
        c = s["scores"].get("composite", {}).get("composite_score")
        if c is not None:
            composites.append(float(c))
    lines.append(
        f"| **Composite (0-10)** | {safe_stat(composites, mean)} | {safe_stat(composites, median)} | "
        f"{safe_stat(composites, stdev) if len(composites) > 1 else 'N/A'} | "
        f"{min(composites) if composites else 'N/A'} | {max(composites) if composites else 'N/A'} |"
    )
    lines.append("")

    lines.append("### Composite Score Distribution")
    lines.append("")
    buckets = {"0-2 (scripted)": 0, "2-4 (mostly scripted)": 0, "4-6 (mixed)": 0, "6-8 (mostly natural)": 0, "8-10 (natural)": 0}
    for c in composites:
        if c <= 2:
            buckets["0-2 (scripted)"] += 1
        elif c <= 4:
            buckets["2-4 (mostly scripted)"] += 1
        elif c <= 6:
            buckets["4-6 (mixed)"] += 1
        elif c <= 8:
            buckets["6-8 (mostly natural)"] += 1
        else:
            buckets["8-10 (natural)"] += 1
    lines.append("| Range | Count | % |")
    lines.append("|-------|-------|---|")
    for label, count in buckets.items():
        pct = round(count / len(composites) * 100, 1) if composites else 0
        lines.append(f"| {label} | {count} | {pct}% |")
    lines.append("")

    lines.append("## 2. Conversion Correlation")
    lines.append("")
    lines.append("### Composite Score: Booked vs. Not Booked")
    lines.append("")

    booked_composites = [
        float(s["scores"]["composite"]["composite_score"])
        for s in booked
        if s["scores"].get("composite", {}).get("composite_score") is not None
    ]
    not_booked_composites = [
        float(s["scores"]["composite"]["composite_score"])
        for s in not_booked
        if s["scores"].get("composite", {}).get("composite_score") is not None
    ]

    lines.append("| Group | N | Mean | Median | Std Dev |")
    lines.append("|-------|---|------|--------|---------|")
    lines.append(
        f"| Booked | {len(booked_composites)} | {safe_stat(booked_composites, mean)} | "
        f"{safe_stat(booked_composites, median)} | {safe_stat(booked_composites, stdev) if len(booked_composites) > 1 else 'N/A'} |"
    )
    lines.append(
        f"| Not Booked | {len(not_booked_composites)} | {safe_stat(not_booked_composites, mean)} | "
        f"{safe_stat(not_booked_composites, median)} | {safe_stat(not_booked_composites, stdev) if len(not_booked_composites) > 1 else 'N/A'} |"
    )

    if booked_composites and not_booked_composites:
        diff = safe_stat(booked_composites, mean) - safe_stat(not_booked_composites, mean)
        lines.append(f"\n**Delta (Booked - Not Booked)**: {round(diff, 2)}")
    lines.append("")

    lines.append("### Per-Dimension: Booked vs. Not Booked (Mean Scores)")
    lines.append("")
    lines.append("| Dimension | Booked Mean | Not Booked Mean | Delta |")
    lines.append("|-----------|-------------|-----------------|-------|")
    for dim in DIMENSIONS:
        b_vals = [float(s["scores"][dim]["score"]) for s in booked if s["scores"].get(dim, {}).get("score") is not None]
        nb_vals = [float(s["scores"][dim]["score"]) for s in not_booked if s["scores"].get(dim, {}).get("score") is not None]
        b_mean = safe_stat(b_vals, mean)
        nb_mean = safe_stat(nb_vals, mean)
        delta = round(b_mean - nb_mean, 2)
        display = dim.replace("_", " ").title()
        lines.append(f"| {display} | {b_mean} | {nb_mean} | {delta:+.2f} |")
    lines.append("")

    lines.append("## 3. By Call Type")
    lines.append("")
    for ctype in SALES_TYPES:
        subset = [s for s in scored if s.get("transcript_type") == ctype]
        if not subset:
            continue
        c_vals = [float(s["scores"]["composite"]["composite_score"]) for s in subset if s["scores"].get("composite", {}).get("composite_score") is not None]
        lines.append(f"### {ctype} (n={len(subset)})")
        lines.append(f"- Composite mean: {safe_stat(c_vals, mean)}, median: {safe_stat(c_vals, median)}")
        b_sub = [s for s in subset if s.get("call_outcome") == "booked"]
        nb_sub = [s for s in subset if s.get("call_outcome") != "booked"]
        lines.append(f"- Booked: {len(b_sub)}, Not booked: {len(nb_sub)}")
        lines.append("")

    lines.append("## 4. Handoff Detection (full_team_sell only)")
    lines.append("")
    fts = [s for s in scored if s.get("transcript_type") == "full_team_sell"]
    if fts:
        detected = sum(1 for s in fts if s["scores"].get("call_structure", {}).get("handoff_detected") is True)
        not_detected = len(fts) - detected
        lines.append(f"- Total full_team_sell calls: {len(fts)}")
        lines.append(f"- Handoff detected: {detected} ({round(detected/len(fts)*100, 1)}%)")
        lines.append(f"- Handoff NOT detected: {not_detected}")
        lines.append("")
        if detected > 0:
            lines.append("### Sample Handoff Quotes")
            lines.append("")
            for s in fts[:5]:
                hq = s["scores"].get("call_structure", {}).get("handoff_quote", "N/A")
                lines.append(f"- `{s['call_id'][:12]}...`: \"{hq}\"")
            lines.append("")
    else:
        lines.append("No full_team_sell calls in sample.")
        lines.append("")

    lines.append("## 5. Cross-Reference with Existing VT SI Scores")
    lines.append("")
    existing_fields = [
        ("rep_performance_score", "Rep Performance"),
        ("discovery_quality", "Discovery Quality"),
    ]
    for field, label in existing_fields:
        pairs = []
        for s in scored:
            existing_val = s.get(field)
            comp = s["scores"].get("composite", {}).get("composite_score")
            if existing_val is not None and comp is not None:
                try:
                    pairs.append((float(existing_val), float(comp)))
                except (ValueError, TypeError):
                    pass
        if len(pairs) >= 5:
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            x_mean = mean(xs)
            y_mean = mean(ys)
            num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
            den_x = math.sqrt(sum((x - x_mean) ** 2 for x in xs))
            den_y = math.sqrt(sum((y - y_mean) ** 2 for y in ys))
            corr = round(num / (den_x * den_y), 3) if den_x > 0 and den_y > 0 else 0
            lines.append(f"**{label}** vs Scriptedness Composite: r = {corr} (n={len(pairs)})")
        else:
            lines.append(f"**{label}**: Insufficient data for correlation (n={len(pairs)})")
    lines.append("")

    lines.append("## 6. Spot-Check: Extreme Calls")
    lines.append("")

    sorted_by_composite = sorted(scored, key=lambda s: s["scores"].get("composite", {}).get("composite_score", 5))

    lines.append("### 5 Most Scripted Calls")
    lines.append("")
    for s in sorted_by_composite[:5]:
        comp = s["scores"].get("composite", {}).get("composite_score", "?")
        summary = s["scores"].get("composite", {}).get("summary", "")
        lines.append(f"**{s['call_id'][:12]}...** | composite={comp} | {s.get('transcript_type')} | {s.get('call_outcome')}")
        lines.append(f"> {summary}")
        for dim in DIMENSIONS:
            dim_data = s["scores"].get(dim, {})
            ev = dim_data.get("evidence", [])
            evidence_str = "; ".join(ev[:2]) if ev else "no evidence"
            lines.append(f"- {dim.replace('_', ' ').title()}: {dim_data.get('score', '?')} — {evidence_str[:200]}")
        lines.append("")

    lines.append("### 5 Most Natural Calls")
    lines.append("")
    for s in sorted_by_composite[-5:]:
        comp = s["scores"].get("composite", {}).get("composite_score", "?")
        summary = s["scores"].get("composite", {}).get("summary", "")
        lines.append(f"**{s['call_id'][:12]}...** | composite={comp} | {s.get('transcript_type')} | {s.get('call_outcome')}")
        lines.append(f"> {summary}")
        for dim in DIMENSIONS:
            dim_data = s["scores"].get(dim, {})
            ev = dim_data.get("evidence", [])
            evidence_str = "; ".join(ev[:2]) if ev else "no evidence"
            lines.append(f"- {dim.replace('_', ' ').title()}: {dim_data.get('score', '?')} — {evidence_str[:200]}")
        lines.append("")

    if errored:
        lines.append("## 7. Errors")
        lines.append("")
        lines.append(f"Total errors: {len(errored)}")
        lines.append("")
        for s in errored:
            lines.append(f"- `{s['call_id'][:12]}...`: {s['error']}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Scriptedness evaluation experiment")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Total calls to fetch (split ~50/50 booked/not)")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching, use cached calls_sample.json")
    parser.add_argument("--skip-score", action="store_true", help="Skip scoring, use cached raw_scores.json")
    args = parser.parse_args()

    ensure_env()
    os.makedirs(OUT_DIR, exist_ok=True)

    if args.skip_fetch and os.path.exists(CALLS_CACHE):
        print(f"Loading cached calls from {CALLS_CACHE}")
        with open(CALLS_CACHE) as f:
            calls = json.load(f)
        print(f"Loaded {len(calls)} calls from cache")
    else:
        print(f"Fetching {args.limit} calls from Supabase (stratified by outcome)...")
        calls = fetch_calls(args.limit)
        with open(CALLS_CACHE, "w") as f:
            json.dump(calls, f, indent=2)
        print(f"Saved {len(calls)} calls to {CALLS_CACHE}")

    if not calls:
        sys.exit("ERROR: No calls to process")

    if args.skip_score and os.path.exists(SCORES_PATH):
        print(f"Loading cached scores from {SCORES_PATH}")
        with open(SCORES_PATH) as f:
            scores = json.load(f)
        print(f"Loaded {len(scores)} scores from cache")
    else:
        scores = run_scoring(calls)
        with open(SCORES_PATH, "w") as f:
            json.dump(scores, f, indent=2)
        print(f"\nSaved {len(scores)} scores to {SCORES_PATH}")

    print("Generating analysis report...")
    report = generate_report(scores)
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    print(f"Report saved to {REPORT_PATH}")

    scored = [s for s in scores if s.get("scores") and not s.get("error")]
    composites = [s["scores"]["composite"]["composite_score"] for s in scored if s["scores"].get("composite", {}).get("composite_score") is not None]
    if composites:
        print(f"\n=== SUMMARY ===")
        print(f"Scored: {len(scored)}/{len(scores)}")
        print(f"Composite mean: {round(mean(composites), 2)}, median: {round(median(composites), 2)}")


if __name__ == "__main__":
    main()
