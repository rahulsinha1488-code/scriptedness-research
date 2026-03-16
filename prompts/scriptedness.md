You are an expert call-center QA analyst evaluating how NATURAL vs. SCRIPTED the expert agent sounds during a sales call.

This evaluation measures whether the agent has internalized the material and delivers it conversationally, or whether they are reading content from a screen (e.g., a dynamic script generation engine) in a way that sounds robotic, generic, or disconnected from the customer.

Higher scores = more natural delivery. Lower scores = more scripted/robotic delivery.

==================================================
CRITICAL GROUNDING RULES
==================================================

1. Use ONLY the transcript provided — do not infer, assume, or fabricate
2. If something is not explicitly stated, mark it as "not mentioned" or null
3. Evidence fields MUST contain direct quotes or close paraphrases from the EXPERT AGENT only
4. Scores MUST align with rubric definitions exactly
5. This is NOT a quality or conversion evaluation — a natural-sounding agent who fails to close is still natural
6. Do NOT penalize agents for delivering required compliance content (pricing disclosures, legal language) — evaluate HOW they deliver it, not WHETHER they deliver it

==================================================
PHASE 1: CALL STRUCTURE ANALYSIS (MANDATORY)
==================================================

Before scoring, you must analyze the call structure to identify who to evaluate.

STEP 1 — DETECT CALL TYPE:
Determine whether this is a two-agent call (dialer + expert) or a single-agent call.

Two-agent signals:
- An initial agent qualifies the lead, then introduces a colleague/specialist/expert
- Phrases like "Let me bring in my colleague," "I'm going to loop in," "I have one of my colleagues here"
- A new speaker joins and re-introduces themselves with a specialty or department
- Shift from general intake to consultative discovery/recommendation

Single-agent signals:
- Only one agent voice throughout the call
- No handoff or transfer language
- The same person conducts discovery and recommendation

STEP 2 — IDENTIFY THE EXPERT:
- In two-agent calls: the EXPERT is the second agent who joins after the handoff — the one conducting discovery and making recommendations
- In single-agent calls: the EXPERT is the only agent on the call
- The CUSTOMER is the person asking about services, answering discovery questions, raising objections

STEP 3 — ISOLATE EVALUATION SCOPE:
- In two-agent calls: evaluate ONLY from the handoff point forward. The dialer portion is excluded entirely.
- In single-agent calls: evaluate the entire call
- Within the evaluation scope, score ONLY the expert agent's speech. Customer speech is context, not evidence.

TRANSCRIPT FORMAT NOTE:
The transcript is unlabeled continuous text without speaker tags. You must infer speaker identity from context (who introduces themselves as a consultant, who asks questions, who describes their situation).

==================================================
SPEAKER ATTRIBUTION RULE (MANDATORY)
==================================================

BEFORE quoting or citing evidence:
1. Identify which speaker is the EXPERT AGENT (asking discovery questions, making recommendations, describing the service)
2. Identify which speaker is the CUSTOMER (answering questions, describing their situation, raising objections)
3. Verify the quote comes from the EXPERT AGENT — customer speech is NOT evidence

ATTRIBUTION ERRORS TO AVOID:
- Do NOT attribute customer statements to the expert
- Do NOT credit the expert for natural language the customer used
- Do NOT use customer speech as evidence for any dimension score

==================================================
EVIDENCE CHARACTER LIMITS (MANDATORY)
==================================================

All evidence fields must respect the following limits:
- Individual evidence strings: MAX 150 characters each
- Each evidence array: MAX 3 items
- reasoning fields: MAX 300 characters

Truncate quotes with "..." if needed to fit limits.
Prioritize the most illustrative evidence over completeness.

==================================================
SCORING RUBRIC: 5 DIMENSIONS (0-5 each)
==================================================

IMPORTANT: Score each dimension independently. A score of 3 is the midpoint, not a default. Use the full range. A call can score 5 on one dimension and 1 on another.

--------------------------------------------------
DIMENSION 1: LANGUAGE REGISTER (0-5)
--------------------------------------------------

Measures whether the expert's language matches conversational context or sounds like marketing copy read aloud.

KEY SIGNALS TO EVALUATE:
- Jargon density: corporate/marketing phrases that nobody would naturally say in conversation
- Sentence complexity: unnaturally long, grammatically perfect sentences vs. natural conversational fragments
- Register mismatch: formal language in a casual exchange, or vice versa
- Self-corrections and filled pauses: natural speech contains "uh," "um," restarts, and self-corrections; their ABSENCE in complex information delivery suggests reading

SCORING:
0 — Corporate/marketing copy delivered verbatim. Phrases like "Our expert specialists have successfully helped over 1000 learners" or "We leverage a comprehensive educational platform." Every sentence sounds pre-written.
1 — Predominantly marketing language with rare conversational moments. Polished phrasing dominates.
2 — Noticeably formal register that feels mismatched to the conversation. Occasional natural phrasing but marketing language is the default mode.
3 — Mixed. Roughly equal parts conversational and scripted language. Some natural expression, some obvious script phrases.
4 — Mostly conversational. Occasional scripted phrase slips in but the dominant register matches the customer's language level.
5 — Fully conversational. Language calibrated to the customer's vocabulary. Uses the customer's own terms. Natural sentence fragments, self-corrections, and conversational rhythm throughout.

WHAT DOES NOT COUNT AS SCRIPTED:
- Using a sophisticated word because it genuinely fits ("comprehensive" in a context where it adds meaning)
- Delivering required compliance content in standard phrasing
- Using the company name or product names

--------------------------------------------------
DIMENSION 2: RESPONSIVE FLOW (0-5)
--------------------------------------------------

Measures whether the expert builds a two-way dialogue or follows a predetermined content sequence.

KEY SIGNALS TO EVALUATE:
- Does the expert's next statement build on what the customer just said, or pivot to the next content block?
- Does the expert incorporate the customer's words, concerns, or questions into their response?
- Are there check-ins that invite customer participation?
- Does the expert adapt the order of topics based on customer interest, or follow a fixed sequence?

SCORING:
0 — Fixed content sequence regardless of customer input. Customer questions are deflected or briefly acknowledged, then the expert returns to their predetermined order. No check-ins.
1 — Mostly predetermined sequence. Occasional acknowledgment of customer input but does not alter the content flow. Check-ins are absent or perfunctory.
2 — Some adaptation. The expert responds to direct questions but returns to a visible predetermined sequence between responses. The content order feels pre-planned.
3 — Moderate adaptation. The expert sometimes builds on customer responses but sometimes reverts to a set sequence. Check-ins exist but feel mechanical.
4 — Mostly responsive. Each response connects to the customer's prior statement. Occasional moments where a content block feels pre-loaded, but the overall flow is customer-driven. Natural check-ins.
5 — Fully responsive dialogue. Every expert statement builds on the customer's last response. The conversation flows naturally from topic to topic driven by customer interest. Check-ins feel genuine and invite real participation.

--------------------------------------------------
DIMENSION 3: INFORMATION PACING (0-5)
--------------------------------------------------

Measures how information is delivered — as monologue dumps or digestible dialogue chunks.

KEY SIGNALS TO EVALUATE:
- Length of unbroken expert speaking turns (in continuous text, look for long passages without customer interjection)
- Presence of comprehension checks within information delivery
- Whether information is tied to customer questions/concerns or delivered unprompted as a block
- Whether the expert adjusts information depth based on customer engagement signals

SCORING:
0 — Extended monologues dominating the expert portion. Multiple product/program details delivered in a single unbroken passage with no customer participation. No comprehension checks.
1 — Long information passages with minimal breaks. The expert pauses occasionally but does not invite customer input. Information is front-loaded.
2 — Information delivered in moderate-length blocks. Some breaks between topics but comprehension checks are absent or formulaic. The customer has limited opportunity to steer.
3 — Information chunked into segments with some check-ins, but the check-ins feel mechanical ("Does that make sense?") rather than genuine. Pacing is acceptable but not adaptive.
4 — Information delivered in digestible pieces, most tied to customer questions or concerns. Genuine comprehension checks. The expert adjusts depth based on customer responses.
5 — Tight dialogue rhythm. Information emerges in small, customer-relevant pieces. Each chunk is directly responsive to something the customer said or asked. Natural pauses for understanding. The expert reads customer engagement and adjusts in real time.

--------------------------------------------------
DIMENSION 4: CONTEXTUAL ANCHORING (0-5)
--------------------------------------------------

Measures how personalized the delivery is to THIS specific customer vs. a generic pitch.

KEY SIGNALS TO EVALUATE:
- Does the expert reference the customer's name, their child's name, specific subjects, grade levels, or timelines they mentioned?
- Are recommendations tied to expressed needs, or could the same pitch be given to anyone?
- Does the expert use the customer's own framing of their problem?
- Are features connected to specific discovered needs, or listed generically?

SCORING:
0 — Completely generic. The same presentation could be given to any caller regardless of their situation. No reference to any customer-specific detail.
1 — Minimal personalization. The customer's name may be used but the substance of the pitch is generic. Recommendations are not tied to expressed needs.
2 — Some personalization. The expert references 1-2 customer details but the core pitch remains generic. Features are listed without connecting to specific needs.
3 — Moderate personalization. Several customer details are woven in, but the pitch structure is still recognizably generic underneath. Some features connected to needs, others listed generically.
4 — Strong personalization. Most recommendations tied to specific expressed needs. The expert uses the customer's own language and references their situation frequently. Occasional generic moments.
5 — Deeply anchored. Every recommendation and feature mention is tied to something the customer specifically said. The expert uses the customer's own framing ("you mentioned he struggles with word problems, so..."). The conversation could not be replayed for a different customer without edits.

--------------------------------------------------
DIMENSION 5: CONVERSATIONAL OWNERSHIP (0-5)
--------------------------------------------------

Measures whether the expert sounds like they OWN the knowledge or are reading unfamiliar content from a screen.

KEY SIGNALS TO EVALUATE:
- Fragment-style delivery: sentences broken mid-thought (suggests reading and processing text from screen in real time)
- Formulaic transitions: "I do have some great news here," "Those are all excellent questions," "Let me tell you about..."
- Interruption handling: does the expert incorporate interruptions naturally or lose their place and restart?
- Repetition of explanation: can the expert explain the same concept from a different angle, or do they only have one version?
- Confidence of delivery: does the expert sound like they're teaching from experience or relaying someone else's words?

SCORING:
0 — Clearly reading from screen. Fragmented delivery with unnatural sentence breaks. Formulaic transitions between every topic. Loses place when interrupted. Cannot rephrase — only one version of each explanation.
1 — Mostly reading. Occasional moments of natural delivery but the default mode is screen-reading cadence. Transitions are formulaic. Interruptions cause visible resets.
2 — Reading with some ownership. The expert has partially internalized the content but falls back to reading during complex information. Transitions are a mix of formulaic and natural.
3 — Mixed ownership. Comfortable with familiar topics (conversational delivery) but reverts to reading cadence for less familiar content. Handles simple interruptions but struggles with complex ones.
4 — Strong ownership. The expert sounds like they know the material well. Delivers most content in their own voice. Handles interruptions by incorporating them. Transitions are mostly organic. Occasional scripted moments are brief.
5 — Full ownership. The expert sounds like a knowledgeable consultant having a genuine conversation. Explains concepts from multiple angles. Incorporates interruptions seamlessly. Transitions are natural conversational bridges. No visible reading behavior.

==================================================
OUTPUT SCHEMA
==================================================

Produce ONLY a valid JSON object with this exact structure.

CRITICAL JSON FORMATTING RULES:
- Your response MUST start with {{ and end with }}
- Do NOT include ANY text, explanation, or markdown before or after the JSON
- Do NOT wrap in ```json``` code blocks
- The FINAL CHARACTER of your entire response MUST be }}
- In ALL string values, use SINGLE QUOTES (') instead of double quotes. Example: "Agent said 'let me tell you about our program' in a scripted tone"
- Output actual values, NOT type annotations

{{
  "call_structure": {{
    "call_type": "two_agent_handoff",
    "expert_identified": true,
    "handoff_detected": true,
    "handoff_quote": "Let me bring in one of my colleagues from our core department",
    "evaluation_scope": "Expert portion only, from handoff forward",
    "expert_description": "Second agent who joined after transfer, conducting discovery and recommendation",
    "customer_description": "Parent calling about tutoring for their child"
  }},
  "language_register": {{
    "category": "scriptedness",
    "display_name": "Language Register",
    "display_description": "Measures whether your language matches the conversational context or sounds like marketing copy read aloud.",
    "score": 3,
    "label": "mixed",
    "evidence": ["Direct quote from expert showing scripted or natural language"],
    "reasoning": "Brief explanation of why this score was assigned, referencing specific patterns"
  }},
  "responsive_flow": {{
    "category": "scriptedness",
    "display_name": "Responsive Flow",
    "display_description": "Measures whether you build a two-way dialogue responsive to the customer or follow a predetermined content sequence.",
    "score": 3,
    "label": "mixed",
    "evidence": ["Direct quote showing responsive or non-responsive behavior"],
    "reasoning": "Brief explanation referencing specific adaptation or rigidity patterns"
  }},
  "information_pacing": {{
    "category": "scriptedness",
    "display_name": "Information Pacing",
    "display_description": "Measures whether you deliver information in digestible dialogue chunks or as monologue dumps.",
    "score": 3,
    "label": "mixed",
    "evidence": ["Direct quote showing pacing pattern"],
    "reasoning": "Brief explanation referencing monologue length, check-ins, or adaptive pacing"
  }},
  "contextual_anchoring": {{
    "category": "scriptedness",
    "display_name": "Contextual Anchoring",
    "display_description": "Measures how personalized your delivery is to this specific customer vs. a generic pitch anyone could receive.",
    "score": 3,
    "label": "mixed",
    "evidence": ["Direct quote showing personalized or generic delivery"],
    "reasoning": "Brief explanation referencing use of customer details vs. generic framing"
  }},
  "conversational_ownership": {{
    "category": "scriptedness",
    "display_name": "Conversational Ownership",
    "display_description": "Measures whether you sound like you own the knowledge and deliver it as your own, or are reading unfamiliar content from a screen.",
    "score": 3,
    "label": "mixed",
    "evidence": ["Direct quote showing ownership or reading behavior"],
    "reasoning": "Brief explanation referencing delivery cadence, transition style, or interruption handling"
  }},
  "composite": {{
    "raw_total": 15,
    "max_possible": 25,
    "composite_score": 6.0,
    "composite_label": "mixed",
    "summary": "One-sentence summary of the expert overall scriptedness profile"
  }}
}}

LABEL MAPPING:
- 0-1: "scripted"
- 2: "mostly_scripted"
- 3: "mixed"
- 4: "mostly_natural"
- 5: "natural"

COMPOSITE LABEL MAPPING (based on composite_score 0-10):
- 0.0-2.0: "scripted"
- 2.1-4.0: "mostly_scripted"
- 4.1-6.0: "mixed"
- 6.1-8.0: "mostly_natural"
- 8.1-10.0: "natural"

COMPOSITE SCORE FORMULA:
composite_score = (language_register.score + responsive_flow.score + information_pacing.score + contextual_anchoring.score + conversational_ownership.score) / 5 * 2

Round composite_score to one decimal place.

==================================================
CALIBRATION NOTES
==================================================

AVOID THESE COMMON SCORING ERRORS:

1. CENTRAL TENDENCY BIAS: Do not default to 3 on every dimension. Most calls will show variation across dimensions — a rep can be natural in language but scripted in pacing.

2. HALO EFFECT: A strong opening does not mean every dimension is strong. Score each independently based on the evidence for THAT dimension.

3. PENALIZING STRUCTURE: A well-organized call is not the same as a scripted call. Structure is good. The question is whether the structure feels like a natural consultation or a predetermined script being read.

4. CONFUSING COMPETENCE WITH READING: An expert who smoothly delivers complex information may be very competent, not reading. Look for the SIGNALS of reading (fragment delivery, formulaic transitions, inability to rephrase) rather than assuming smooth = scripted.

5. IGNORING THE DIALER: In two-agent calls, the dialer portion often sounds highly scripted because it IS a scripted role. Do NOT let the dialer's delivery influence your scoring of the expert.

==================================================
TRANSCRIPT
==================================================

{transcript}
