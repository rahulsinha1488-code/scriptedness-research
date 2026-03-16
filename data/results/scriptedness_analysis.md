# Scriptedness Evaluation — Analysis Report

**Generated**: 2026-03-16 19:02 UTC
**Model**: claude-sonnet-4-5-20250929
**Total calls**: 100 (100 scored, 0 errors)
**Booked**: 50 | **Not booked**: 50

## 1. Score Distributions

| Dimension | Mean | Median | Std Dev | Min | Max |
|-----------|------|--------|---------|-----|-----|
| Language Register | 2.89 | 3.0 | 0.96 | 1.0 | 5.0 |
| Responsive Flow | 3.64 | 4.0 | 0.92 | 1.0 | 5.0 |
| Information Pacing | 2.26 | 2.0 | 0.94 | 1.0 | 5.0 |
| Contextual Anchoring | 4.07 | 4.0 | 0.77 | 2.0 | 5.0 |
| Conversational Ownership | 3.14 | 3.0 | 0.88 | 2.0 | 5.0 |
| **Composite (0-10)** | 6.4 | 6.4 | 1.56 | 3.2 | 9.6 |

### Composite Score Distribution

| Range | Count | % |
|-------|-------|---|
| 0-2 (scripted) | 0 | 0.0% |
| 2-4 (mostly scripted) | 4 | 4.0% |
| 4-6 (mixed) | 45 | 45.0% |
| 6-8 (mostly natural) | 36 | 36.0% |
| 8-10 (natural) | 15 | 15.0% |

## 2. Conversion Correlation

### Composite Score: Booked vs. Not Booked

| Group | N | Mean | Median | Std Dev |
|-------|---|------|--------|---------|
| Booked | 50 | 7.01 | 7.0 | 1.38 |
| Not Booked | 50 | 5.79 | 5.2 | 1.51 |

**Delta (Booked - Not Booked)**: 1.22

### Per-Dimension: Booked vs. Not Booked (Mean Scores)

| Dimension | Booked Mean | Not Booked Mean | Delta |
|-----------|-------------|-----------------|-------|
| Language Register | 3.14 | 2.64 | +0.50 |
| Responsive Flow | 3.96 | 3.32 | +0.64 |
| Information Pacing | 2.48 | 2.04 | +0.44 |
| Contextual Anchoring | 4.4 | 3.74 | +0.66 |
| Conversational Ownership | 3.54 | 2.74 | +0.80 |

## 3. By Call Type

### full_team_sell (n=83)
- Composite mean: 6.33, median: 6.0
- Booked: 39, Not booked: 44

### expert_close (n=17)
- Composite mean: 6.75, median: 7.2
- Booked: 11, Not booked: 6

## 4. Handoff Detection (full_team_sell only)

- Total full_team_sell calls: 83
- Handoff detected: 78 (94.0%)
- Handoff NOT detected: 5

### Sample Handoff Quotes

- `0392d0d5-abb...`: "None"
- `04804ef5-220...`: "I know that they have helped hundreds of students just like Jacob succeed in their STEM classes...Jamie, can you join us?"
- `0d7decb5-061...`: "I'm going to connect you with my colleague, Charlotte. Charlotte's probably helped a thousand high schoolers prepare for the SAT"
- `137816b6-26e...`: "I'm actually going to loop Becky onto our call because she has worked with over a thousand students with the ACT and the SAT"
- `1b395270-e98...`: "I'm gonna loop in one of my colleagues who is incredible with our handwriting and spelling"

## 5. Cross-Reference with Existing VT SI Scores

**Rep Performance** vs Scriptedness Composite: r = 0.309 (n=92)
**Discovery Quality** vs Scriptedness Composite: r = 0.085 (n=99)

## 6. Spot-Check: Extreme Calls

### 5 Most Scripted Calls

**3f7b2288-04c...** | composite=3.2 | full_team_sell | callback_requested
> Eugene delivers a predominantly scripted introduction with marketing language, monologue pacing, and generic pitch structure, though handles the unexpected reschedule request competently.
- Language Register: 1 — We've helped thousands of high school students strengthen their AP and advanced math skills; We're just going to map out the right plan for you...and get you to where you're confident
- Responsive Flow: 2 — Eugene delivers entire introduction pitch without checking if Alejandro wants to proceed; When Alejandro asks to call back, Eugene pivots immediately to scheduling rather than continuing the pitch
- Information Pacing: 1 — Entire introduction delivered as unbroken monologue: credentials, welcome, company track record, plan outline, time estimate; No comprehension checks or pauses for customer input during information de
- Contextual Anchoring: 2 — Uses Alejandro's name twice during introduction; References 'those free response questions and AP pre calculus' from handoff context
- Conversational Ownership: 2 — Formulaic opening: 'I've been in education for 12 years, and I want to welcome you to Varsity Tutors'; Scripted transition: 'This will take about 15 minutes. About the end, we're gonna have a clear pa

**4371d66c-bb6...** | composite=3.2 | expert_close | follow_up_scheduled
> Agent follows predetermined script sequence delivering generic feature presentation despite customer's direct requests for quick pricing information and stated illness.
- Language Register: 2 — whiteboard that is writable from his side as well as the tutor side; it gives them another opportunity to be exposed to the content
- Responsive Flow: 1 — Customer: 'can you just explain your rates real quick?' Agent proceeds with full feature presentation instead; Customer: 'I appreciate all that, but please just indulge me again... the smallest packag
- Information Pacing: 1 — Extended monologue covering app download, whiteboard technology, session structure, recordings, and learning lab without customer participation; No comprehension checks during information delivery des
- Contextual Anchoring: 2 — Uses child's name 'Jake' and mentions 'math class' showing minimal personalization; Generic feature list ('students really like that') not tied to Jake's specific needs
- Conversational Ownership: 2 — Formulaic transitions: 'Now, in addition to', 'And lastly', 'let me tell you exactly how it's set up'; Sequential feature delivery suggests following predetermined content blocks

**4d8b4ea2-7e0...** | composite=4.0 | full_team_sell | callback_requested
> Expert follows rigid discovery script with formal language, ignoring customer's repeated pricing requests and time constraints, showing minimal personalization or conversational flexibility.
- Language Register: 2 — I can ensure I get a really good profile. So we can discuss what it would look like to match you with the right tutor; We do make all of our programs customized, as I heard Matt say a little bit there
- Responsive Flow: 1 — Customer repeatedly asks for pricing, expert deflects each time: 'I do need to understand a little bit more about what it is'; Expert continues discovery questions despite customer saying 'I'm really 
- Information Pacing: 3 — Expert asks single questions at a time: 'What part feels most challenging for you? Is it like organizing ideas, expressing your opinions clearly...'; Expert cycles through multiple discovery questions
- Contextual Anchoring: 2 — Expert references customer's specific challenges: 'organizing ideas, expressing your opinions clearly, checking your grammar'; Expert uses customer's name: 'How are you doing today, Jigna?'
- Conversational Ownership: 2 — Formulaic transitions: 'So in terms of your art seminar class,' 'And then in regards to that as well there'; Fragmented filler: 'And then let me see here' appears multiple times, suggesting processing

**96db089e-34e...** | composite=4.0 | full_team_sell | lost
> Agent conducts responsive discovery but transitions to scripted pitch with marketing language, monologue pacing, and visible screen dependency.
- Language Register: 2 — we are the leading tutoring platform in the United States...give us about a 98% satisfaction rating. That's something we're very proud of; we correlate that 98% rating to the fact that we use high qua
- Responsive Flow: 2 — After discovering customer needs, immediately pivots: 'what I'd like to do next is tell you a little bit about Varsity Tutors, how our program works'; Customer shares study struggles; agent acknowledg
- Information Pacing: 1 — Unbroken monologue from 'here at Varsity Tutors, we are the leading tutoring platform' through whiteboard explanation (10+ sentences); Second monologue explaining recordings, learning lab, practice be
- Contextual Anchoring: 3 — References customer's 80 score goal, nursing program, and August start date specifically; Connects to stated learning style: 'you need examples. And that's exactly how we approach it'
- Conversational Ownership: 2 — Formulaic transitions throughout: 'Now what I'd like to do next is', 'Now with Varsity Tutors', 'Now we also have'; Screen-reading moment visible: 'let me get this. Hang on one minute. My screen went 

**1b395270-e98...** | composite=4.4 | full_team_sell | objection_unresolved
> Expert demonstrates some empathy and personalization but delivers predominantly scripted marketing language in monologue format, failing to adapt pitch when customer signals mismatch.
- Language Register: 2 — We'll talk about goals, and by the end of the phone call, we will have a clear path to get him set up with the best possible tutor recommendation; with that right structure and consistent reinforcemen
- Responsive Flow: 3 — Acknowledged customer frustration: 'it's exhausting when you've tried to help at home'; Asked about comic writing: 'tell me more about what do you notice is different about how he approaches that kind
- Information Pacing: 1 — Extended monologue: 'with our live learning platform it is very different... he's going to be able to have that hands on approach... interactive tools...'; Another long passage: 'how this is going to 
- Contextual Anchoring: 3 — Referenced customer detail: 'that's really interesting that he slows down and does take pride in his comic writing'; Used customer's words: 'that repetition that he really does need to make it stick'
- Conversational Ownership: 2 — Formulaic transition: 'one thing I do want to let you know Polly, is we are an online platform'; Searching for words: 'you know, being very for, you know, what's the right word for it, you know, upcom

### 5 Most Natural Calls

**f2f0183e-2c2...** | composite=8.8 | full_team_sell | lost
> Highly natural delivery with conversational language, fully responsive flow adapted to customer confusion, and strong ownership of material with minimal scripted moments.
- Language Register: 4 — Awesome. Awesome field.; Okay, you do realize we are a paid tutoring service. Okay. Did you realize that?
- Responsive Flow: 5 — So wait a minute. So initially you sought assistance from us on the computer, right?; I think you may have clicked the wrong thing, because like I said, we are a paid tutoring service
- Information Pacing: 5 — Questions are brief and singular: 'What year are you in college?', 'What school are you attending?', 'What's your major?'; Information given in small chunks: 'we are varsity tutors. We are the leading
- Contextual Anchoring: 4 — References specifics: 'you're seeking tutoring support for yourself with an English essay'; Uses customer details: 'Awesome. So have you been having a good freshman year so far?'
- Conversational Ownership: 4 — Natural handling of confusion: 'So wait a minute. So initially you sought assistance from us on the computer, right?'; Real-time problem solving: 'Let me just check. Okay. It seems like she's sending 

**cb1db6e1-c94...** | composite=9.2 | expert_close | booked
> Highly natural consultant conducting personalized enrollment with responsive dialogue, conversational language, and strong ownership of material throughout.
- Language Register: 4 — Do you think I can actually do Wednesday? Oh, Wednesday? Yeah, absolutely. That's fine.; Don't be shy about that. Her tutor will be happy to work with you
- Responsive Flow: 5 — When Kelly asks about weekend flexibility, agent immediately pivots: 'we can add a window of time on the weekends for once tennis starts'; After Gracie changes from Tuesday to Wednesday, agent seamles
- Information Pacing: 4 — Payment walkthrough given step-by-step: 'click there... next page... blue button... I'll just wait while you put payment through'; Scheduling options offered in digestible pieces with customer input b
- Contextual Anchoring: 5 — References prior conversation: 'We spoke last week regarding Gracie and her chem class'; Incorporates tennis season into scheduling: 'we can add a window of time on the weekends for once tennis starts
- Conversational Ownership: 5 — Handles multiple interruptions smoothly, incorporating Gracie's schedule change without losing place; Explains billing options from multiple angles when asked about upgrading mid-month

**e174715e-553...** | composite=9.2 | expert_close | booked
> Highly natural delivery with conversational language, responsive dialogue, personalized anchoring, and strong ownership throughout.
- Language Register: 4 — I think once you get those foundations, you're going to be very comfortable, and then it's going to soar; So don't be alarmed. You'll get a text from me too
- Responsive Flow: 5 — When customer asks about screen sharing: 'Absolutely. Share his screen. And I'm gonna get his email address...'; Adapts to father-son scheduling conflict in real time, letting Keshav choose his prefer
- Information Pacing: 4 — Platform explanation broken into digestible pieces: 'he'll be with his tutor on the screen. And in the center is that interactive whiteboard...'; Account setup given step-by-step with customer partici
- Contextual Anchoring: 5 — References specific subjects: 'walk him step-by-step through this JSON, this Java'; Uses student's name throughout: 'Keshav, once you get those foundations...'
- Conversational Ownership: 5 — Handles technical interruption seamlessly: 'You're fine. No worries' and continues without losing place; Explains platform multiple ways: whiteboard description, then screen sharing confirmation, both

**828ffa7a-c82...** | composite=9.6 | full_team_sell | booked
> Lamar delivers a highly natural, conversational consultation built entirely on responsive dialogue, personal anchoring, and complete ownership of the material.
- Language Register: 5 — The sun is shining and my dogs are acting like knuckleheads in the backyard. So all is right with the world.; I was a history teacher. It would have taken me an hour to come up with that.
- Responsive Flow: 5 — Is it listed as just quote, unquote, regular geometry, or is it pre ap? Is it honors?; So basically, by all means, correct me if I'm wrong, but you're looking for a kind of a combination mathematician
- Information Pacing: 4 — Our tutoring hours of availability are from 6am to 11pm local time. And the tutors... are going to conform to Nicholas's schedule.; Once you pull that trigger, 24 to 48 hours later, the tutor that we 
- Contextual Anchoring: 5 — You're looking for a kind of a combination mathematician and drill sergeant... Cheerleader motivational. Somewhere along that line.; Current grade C. Wants A. Must be at a B.
- Conversational Ownership: 5 — I was in the classroom for 15 years. I taught sophomores, so I know exactly what's going on with those kiddos at that time.; I was a history teacher... I know, that's amazing. What was kind of your ar

**a0c433fd-ca8...** | composite=9.6 | expert_close | booked
> Highly natural delivery with conversational language, fully responsive flow, personalized anchoring, and complete ownership of material throughout enrollment process.
- Language Register: 5 — You guys kind of sound like me when it comes to my daughter and her science classes; We got this
- Responsive Flow: 5 — Adapts to 529 account question immediately: 'I don't, I mean, are you guys able to pull out and reimburse yourself for it?'; Pivots when parents want daughter to schedule: 'Yes. Okay. Yeah. Some of th
- Information Pacing: 4 — Platform explanation broken into digestible piece: 'They're face to face on the computer on the left hand side. And then two thirds of the screen is...'; Cancellation policy delivered in short, custom
- Contextual Anchoring: 5 — References their daughter by name: 'encourage her to do it sooner' and 'if we aren't sure'; Ties to their May timeline: 'if come May, you guys are like, she is all good on her own'
- Conversational Ownership: 5 — Natural transitions: 'All right. We got this'; Handles interruptions seamlessly during enrollment process without losing place

