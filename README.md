# Scriptedness Research: Why Your Best Reps Don't Sound Like They're Reading

## The Problem

Sales reps using dynamic script generation engines (like Nerdy AI) face a fundamental delivery choice: **read the content verbatim** or **internalize it and deliver it naturally**. This research measures that difference — which we call **scriptedness** — from call transcripts alone, and tests whether it correlates with conversion.

All three hypotheses are confirmed: scriptedness is measurable, it varies meaningfully across reps, and natural delivery correlates with higher conversion.

## Key Findings (100-call experiment)

| Group | N | Composite Mean (0-10) | Median |
|---|---|---|---|
| **Booked** | 50 | **7.01** | 7.0 |
| **Not Booked** | 50 | **5.79** | 5.2 |
| **Delta** | — | **+1.22** | +1.8 |

### Strongest differentiators by dimension

| Dimension | Booked Mean | Not Booked Mean | Delta |
|---|---|---|---|
| **Conversational Ownership** | 3.54 | 2.74 | **+0.80** |
| Contextual Anchoring | 4.40 | 3.74 | +0.66 |
| Responsive Flow | 3.96 | 3.32 | +0.64 |
| Language Register | 3.14 | 2.64 | +0.50 |
| Information Pacing | 2.48 | 2.04 | +0.44 |

### The extremes tell the story

**Most Scripted (3.2/10)** — Expert Eugene: *"We've helped thousands of high school students strengthen their AP and advanced math skills"* — corporate monologue, no customer participation.

**Most Natural (9.6/10)** — Expert Lamar: *"The sun is shining and my dogs are acting like knuckleheads in the backyard"* — genuine rapport, consultative dialogue, knowledge delivered as his own.

## The Rubric: 5 Dimensions

Each dimension scored 0 (fully scripted) to 5 (fully natural). Composite averages all 5, mapped to 0-10.

| # | Dimension | What It Measures | Research Basis |
|---|---|---|---|
| 1 | **Language Register** | Marketing copy vs. conversational language | Linguistics: read speech has higher syntactic complexity |
| 2 | **Responsive Flow** | Two-way dialogue vs. predetermined sequence | Balto: intent-based adherence; Gong: 43:57 ratio |
| 3 | **Information Pacing** | Monologue dumps vs. digestible chunks | Gong: pitches >2 min decrease win rates sharply |
| 4 | **Contextual Anchoring** | Generic pitch vs. personalized consultation | Industry: Natural Script Compliance framework |
| 5 | **Conversational Ownership** | Reading from screen vs. internalized delivery | Balto: improvisation/internalization distinction |

## Research Foundation

This is not a heuristic — the rubric is grounded in published research:

- **Balto Research** (567 agents, 2022): #1 reason agents go off-script is desire to improvise. 64% want to change their scripts. Intent-based adherence outperforms verbatim compliance.
- **Gong Labs** (hundreds of thousands of calls): Optimal talk-to-listen is 43:57. Company pitches >2 min sharply reduce win rates. Top performers maintain consistent ratios.
- **Penn Linguistics / Language Log** (2023): Spontaneous speech has 77% more phrase segments, ~8% filled pauses, self-corrections — all absent in read speech. Detectable from transcripts alone.

Full research details in [`scriptedness_research_report.md`](scriptedness_research_report.md).

## Business Opportunities

1. **Coachable behavior**: Information Pacing is the biggest weakness (64% score 1-2/5). Simple fix: "pause and check in after every 2-3 sentences."
2. **New scoring dimension**: Integrate alongside existing quality/derailer prompts in the call scoring pipeline.
3. **Script engine feedback**: Feed pacing data back to Nerdy AI — shorter content, conversational register, bullet points over paragraphs.
4. **Hiring signal**: Track scriptedness trajectory in onboarding to identify reps who internalize vs. plateau.

## Repo Structure

```
scriptedness-research/
├── README.md                              # This file
├── scriptedness_research_report.md        # Full narrative report (CEO-review style)
├── prompts/
│   └── scriptedness.md                    # The evaluation prompt (5-dim rubric, JSON output)
├── scripts/
│   └── scriptedness_eval.py              # Fetch + score + analyze pipeline
├── data/
│   └── results/
│       └── scriptedness_analysis.md       # Statistical analysis from 100-call run
└── requirements.txt
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (or create .env)
export SUPABASE_URL="..."
export SUPABASE_SERVICE_KEY="..."
export ANTHROPIC_API_KEY="..."

# Run the full experiment (fetch 100 calls, score, analyze)
python scripts/scriptedness_eval.py --limit 100

# Re-score cached calls (skip fetch)
python scripts/scriptedness_eval.py --skip-fetch

# Re-analyze cached scores (skip fetch + score)
python scripts/scriptedness_eval.py --skip-score
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | VT Sales Intelligence Supabase instance URL |
| `SUPABASE_SERVICE_KEY` | Yes | Supabase service role key |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude |
| `ANTHROPIC_MODEL` | No | Model override (default: `claude-sonnet-4-5-20250929`) |

## Limitations

- **Correlation, not causation.** A coaching intervention study would establish causation.
- **Single time window.** Sample is from mid-February 2026. Patterns may vary seasonally.
- **Call-level, not rep-level.** Aggregating to per-rep scores over 20+ calls would be more stable.
- **Transcripts only.** No audio features (tone, pace, intonation). Text-detectable signals only.
