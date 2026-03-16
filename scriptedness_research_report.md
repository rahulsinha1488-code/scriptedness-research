# Scriptedness Research: Why Your Best Reps Don't Sound Like They're Reading

## The Problem

Varsity Tutors reps use **Nerdy AI**, a dynamic script generation engine that feeds them content about the lead, program details, and recommended talking points in real time. The question is not whether reps should use this tool — they should. The question is **how they use it**.

When a rep reads Nerdy AI output verbatim, the customer hears corporate language that sounds pre-written, long monologues of product information, and a pitch that feels generic regardless of what they just said. When a rep **internalizes** the content and delivers it in their own voice, the customer hears a knowledgeable consultant having a genuine conversation about their child's education.

We hypothesized that this difference — which we call **scriptedness** — is measurable from transcripts alone, that it varies meaningfully across reps, and that it correlates with conversion.

All three hypotheses are confirmed.

## The Research Foundation

Before writing a single line of scoring logic, we surveyed the call center industry's best available evidence on scripted vs. natural delivery.

### What the industry says

**Balto Research** (567 contact center agents, 2022): The #1 reason agents go off-script is the desire to improvise — not forgetfulness, not boredom. 64% of agents want to change their scripts. Script adherence negatively correlates with job satisfaction. The researchers concluded that "intent-based adherence" — did the rep convey the right ideas? — matters more than verbatim adherence.

**Gong Labs** (hundreds of thousands of sales calls): The optimal talk-to-listen ratio is 43:57. Company pitches exceeding 2 minutes have a "sharp negative correlation" with win rates — spending 10% of call time on company overview reduces win rates to 25% of top-performer levels. Top performers maintain consistent ratios regardless of outcome; lower performers swing 10% between won and lost deals.

### What the linguistics says

**Mark Liberman, Penn Linguistics** (Language Log, 2023): Comparing the same speaker reading prepared text vs. answering questions spontaneously, even simple acoustic analysis reveals dramatic differences. Spontaneous speech has 77% more speech segments per minute (shorter phrases with more pauses). Filled pauses ("uh," "um") comprise ~8% of tokens in spontaneous speech but are nearly absent in read speech. Self-corrections and false starts are common in natural speech, absent in reading.

**Key implication for transcript analysis**: These differences are detectable from text alone. Natural speech produces shorter, simpler sentences with self-corrections and conversational fragments. Read speech produces longer, grammatically complete, marketing-grade sentences with no disfluencies.

### What existing scoring already captures (and doesn't)

Our current scoring pipeline partially measures scriptedness through two existing dimensions:

- **Discovery Responsiveness** (quality.md): Scores 0 = "Completely script-bound" to 5 = "Highly adaptive" — but only within the discovery phase, not the full call
- **Feature Dumping** (derailer.md): Explicitly references "scripted pitch" — but frames it as a derailer behavior, not a standalone delivery measure

Neither captures **language register**, **transition authenticity**, or **conversational ownership** as standalone signals. A dedicated scriptedness score gives coaches a single, actionable number to discuss with reps.

## How We Measured It

### The Rubric: 5 Dimensions, Single Spectrum

Each dimension is scored 0-5, where 0 = fully scripted/robotic and 5 = fully natural/consultative. The composite score averages all 5 and maps to 0-10.

| Dimension | What It Measures | Research Basis |
|---|---|---|
| **Language Register** | Marketing copy vs. conversational language | Linguistics: read speech has higher syntactic complexity and formal register |
| **Responsive Flow** | Two-way dialogue vs. predetermined content sequence | Balto: intent-based adherence; Gong: 43:57 talk-to-listen ratio |
| **Information Pacing** | Monologue dumps vs. digestible dialogue chunks | Gong: company pitches >2 min sharply decrease win rates |
| **Contextual Anchoring** | Generic pitch vs. personalized consultation | Industry: "Natural Script Compliance" framework |
| **Conversational Ownership** | Reading unfamiliar content vs. delivering internalized knowledge | Balto: improvisation/internalization distinction; Linguistics: spontaneous speech markers |

### Expert Portion Only

In `full_team_sell` calls (where a dialer warms the lead, then hands off to an expert), we score **only the expert's portion** after the handoff. The dialer's job is inherently more scripted — that's a role design choice, not a delivery quality problem. Measuring the dialer's scriptedness conflates the two.

For `expert_close` calls (single expert, no dialer), we score the entire call.

### The Experiment

- **100 calls** from the VT Sales Intelligence Supabase database
- **Stratified sample**: 50 booked (converted) + 50 not booked
- **Call types**: 83 `full_team_sell` + 17 `expert_close`
- **Duration filter**: >240 seconds (substantive calls only)
- **Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- **Success rate**: 100/100 scored, 0 errors

## Findings

### Finding 1: The conversion signal is real

| Group | N | Composite Mean (0-10) | Composite Median |
|---|---|---|---|
| **Booked** | 50 | **7.01** | 7.0 |
| **Not Booked** | 50 | **5.79** | 5.2 |
| **Delta** | — | **+1.22** | +1.8 |

Reps who convert score 1.22 points higher on the scriptedness composite than reps who don't. On a 10-point scale, that's a meaningful, coachable gap.

The median gap is even larger (+1.8), suggesting the difference is driven by the not-booked group having a long tail of highly scripted calls.

### Finding 2: Conversational Ownership is the strongest conversion predictor

| Dimension | Booked Mean | Not Booked Mean | Delta |
|---|---|---|---|
| **Conversational Ownership** | 3.54 | 2.74 | **+0.80** |
| Contextual Anchoring | 4.40 | 3.74 | +0.66 |
| Responsive Flow | 3.96 | 3.32 | +0.64 |
| Language Register | 3.14 | 2.64 | +0.50 |
| Information Pacing | 2.48 | 2.04 | +0.44 |

**Conversational Ownership** — whether the rep sounds like they own the knowledge or are reading unfamiliar content from a screen — has the largest delta between booked and not-booked calls.

This maps directly to the Balto research distinction between "internalization" and "reading." A rep who has internalized the Nerdy AI content can paraphrase, handle interruptions, explain the same concept from different angles. A rep who is reading it delivers in fragments, uses formulaic transitions, and loses their place when the customer interrupts.

### Finding 3: Information Pacing is the biggest universal weakness

| Dimension | Mean | Median | % Scoring 1-2 |
|---|---|---|---|
| **Information Pacing** | **2.26** | 2.0 | **64%** |
| Language Register | 2.89 | 3.0 | 48% |
| Conversational Ownership | 3.14 | 3.0 | 28% |
| Responsive Flow | 3.64 | 4.0 | 6% |
| Contextual Anchoring | 4.07 | 4.0 | 4% |

Nearly two-thirds of all calls score 1 or 2 on Information Pacing. Reps are routinely delivering long, unbroken monologues of product and program information without checking in, without pausing for customer questions, and without tying information to customer concerns.

This is the most universally coachable finding from the experiment. Every rep can improve here with a simple behavioral change: after every 2-3 sentences of information, pause and ask a check-in question.

### Finding 4: Contextual Anchoring is the strongest skill

Contextual Anchoring (how personalized the delivery is) has the highest mean score (4.07/5) and 82% of calls score 4-5. Reps are generally good at using the customer's name, referencing their child's subject and grade, and connecting recommendations to expressed needs.

This is likely a downstream effect of good discovery — if discovery captures details, reps naturally use them. It also means **scriptedness is NOT about personalization** in this population. The reps who sound scripted are still personalizing; they're just delivering the personalized content in a scripted manner.

### Finding 5: This measures something genuinely new

| Existing Score | Correlation with Scriptedness Composite | Interpretation |
|---|---|---|
| Rep Performance Score | r = 0.309 | Weak — scriptedness captures something beyond overall rep quality |
| Discovery Quality | r = 0.085 | Near zero — scriptedness is almost completely independent of discovery |

The scriptedness composite has very low correlation with existing VT SI scores. It is not a repackaging of quality or discovery metrics — it's measuring a distinct behavioral signal that the current scoring pipeline does not capture.

### Finding 6: Handoff detection works

94% accuracy (78/83) on `full_team_sell` calls. The prompt correctly identifies the dialer-to-expert handoff and scopes evaluation to the expert portion only.

### Finding 7: The extremes tell the story

**Most Scripted Call (Composite: 3.2)** — An expert named Eugene in a `full_team_sell` callback:

> Eugene delivers a predominantly scripted introduction with marketing language, monologue pacing, and generic pitch structure.

Evidence: *"We've helped thousands of high school students strengthen their AP and advanced math skills"* — delivered as an unbroken monologue with no customer participation. Customer asks to call back; Eugene immediately pivots to scheduling rather than engaging.

**Most Natural Call (Composite: 9.6)** — An expert named Lamar in a `full_team_sell` that booked:

> Lamar delivers a highly natural, conversational consultation built entirely on responsive dialogue, personal anchoring, and complete ownership of the material.

Evidence: *"The sun is shining and my dogs are acting like knuckleheads in the backyard. So all is right with the world."* Later: *"I was a history teacher. It would have taken me an hour to come up with that"* — referring to a customer's math answer, demonstrating genuine rapport and subject matter comfort.

The gap between these two calls is not about what they say — both cover the same program information. It's entirely about **how they say it.**

## The Distribution

```
Composite Score    Count    Label
─────────────────  ─────    ──────────────
0.0 - 2.0           0      Scripted
2.1 - 4.0           4      Mostly Scripted (4%)
4.1 - 6.0          45      Mixed (45%)
6.1 - 8.0          36      Mostly Natural (36%)
8.1 - 10.0         15      Natural (15%)
```

The bulk of calls land in the "mixed" and "mostly natural" range. Only 4% are deeply scripted. But the 45% in the "mixed" zone represent the largest coaching opportunity — these are reps who show natural delivery in some dimensions but fall back to scripted patterns in others.

## What This Means for the Business

### Opportunity 1: Coachable Behavior with Measurable Impact

Scriptedness is not a personality trait — it's a set of behaviors that can be coached. The five dimensions map to specific, actionable changes:

| Dimension | Coaching Action | Who Benefits |
|---|---|---|
| Information Pacing | "After every 2-3 sentences of program info, stop and check in" | 64% of reps (scoring 1-2) |
| Conversational Ownership | "Read the Nerdy AI content before the call, not during it" | 28% of reps (scoring 2) |
| Language Register | "Say it like you'd explain it to a friend, not like you're reading a brochure" | 48% of reps (scoring 1-2) |
| Responsive Flow | "Start your next sentence with something the customer just said" | 6% of reps (scoring 1-2) |
| Contextual Anchoring | Already strong — reinforce, don't over-coach | Only 4% need help |

### Opportunity 2: Integrate into the Scoring Pipeline

Scriptedness can be added to the existing call scoring pipeline as a new prompt alongside quality, derailer, connectivity, and summary. This would:

- Produce per-call scriptedness scores in the existing dashboard
- Enable trending: is scriptedness improving week-over-week?
- Enable per-rep coaching: "Lamar, your scriptedness score is 9.6 — you're the model. Eugene, your score is 3.2 — here's why and what to change."
- Enable correlation analysis in BigQuery against pGC, CC90, and other conversion metrics at scale

### Opportunity 3: Nerdy AI Product Feedback Loop

If scriptedness correlates with conversion, and reps who internalize Nerdy AI content outperform reps who read it, then Nerdy AI itself could be improved:

- **Shorter, punchier content**: If reps are reading long passages, the passages may be too long. Feed the pacing data back to the script engine.
- **Conversational language**: If marketing-grade language gets read verbatim and reduces conversion, rewrite the scripts in conversational register.
- **Bullet points over paragraphs**: Format the script as talking points, not prose. Reps who see prose read prose; reps who see bullets paraphrase.

### Opportunity 4: Hiring and Onboarding Signal

Over time, scriptedness scores could inform:

- **Hiring**: Reps who naturally score high on conversational ownership and responsive flow may be better suited for expert roles. Reps who score high on information pacing but low on ownership might be better suited for dialer roles.
- **Onboarding**: Track new hires' scriptedness trajectory. If a rep starts at 3.0 and reaches 6.0 in 30 days, they're internalizing. If they plateau at 3.0, they need different coaching.
- **Performance management**: A rep who scores 9.0 on scriptedness but has low pGC has a different problem than a rep who scores 3.0 on scriptedness and has low pGC. The first needs help with close technique; the second needs help with delivery.

## Limitations and Next Steps

### What this experiment does NOT prove

1. **Causation.** We show correlation between scriptedness and conversion, not causation. It's possible that better reps are both more natural AND better at closing for unrelated reasons. A controlled experiment (coaching intervention on scriptedness → measure conversion change) would establish causation.

2. **Generalizability across time.** The sample is from a single ~2-day window in mid-February 2026. Patterns may differ by season, campaign, or traffic mix.

3. **Per-rep stability.** We scored calls, not reps. A rep's scriptedness may vary call-to-call depending on fatigue, familiarity with the subject, or customer difficulty. Aggregating to per-rep scores over 20+ calls would be more stable.

### Recommended next steps

```
STEP                                           EFFORT    IMPACT    TIMELINE
─────────────────────────────────────────────  ────────  ────────  ─────────
1. Run on 500+ calls for statistical power     Low       High      1 week
2. Aggregate to per-rep scores and correlate   Low       High      1 week
   with per-rep pGC
3. Integrate into scoring pipeline as new      Medium    High      2-3 weeks
   prompt (alongside quality, derailer, etc.)
4. Run coaching pilot: train 10 reps on        Medium    Very High 4-6 weeks
   information pacing + ownership → measure
   pGC change
5. Feed pacing data back to Nerdy AI content   High      High      8-12 weeks
   formatting
```

## Technical Reference

### Files

| File | Purpose |
|---|---|
| `prompts/scriptedness.md` | The evaluation prompt (5-dimension rubric, JSON output, expert-only scoping) |
| `scripts/analysis/scriptedness_eval.py` | Fetch calls from Supabase, run prompt via Claude, generate analysis report |
| `data/results/scriptedness_eval/calls_sample.json` | 100 cached calls (for re-running without re-fetching) |
| `data/results/scriptedness_eval/raw_scores.json` | Per-call scores with evidence and reasoning |
| `data/results/scriptedness_eval/scriptedness_analysis.md` | Statistical analysis report |

### Reproducing the experiment

```bash
# Full run (fetch + score + analyze)
python scripts/analysis/scriptedness_eval.py --limit 100

# Re-score cached calls (skip fetch)
python scripts/analysis/scriptedness_eval.py --skip-fetch

# Re-analyze cached scores (skip fetch + score)
python scripts/analysis/scriptedness_eval.py --skip-score
```

### Environment requirements

- `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in `.env` (VT Sales Intelligence access)
- `ANTHROPIC_API_KEY` in `.env` (Claude API access)
- Python packages: `requests`, `anthropic`
