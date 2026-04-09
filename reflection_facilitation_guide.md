# Reflection Facilitation Guide

## From Data Problems to Real-World Impact
**Duration:** 20 minutes
**Position:** Final activity of the Interoperability Lab exercise
**Audience:** Non-clinical students (HIM, healthcare admin, CS)

---

## Purpose

This reflection moves students from "we found data problems" to understanding why those problems matter to three audiences who make decisions based on health data: **executives**, **clinicians and patients**, and **the financial system**. The goal is for students to see themselves as the professionals who sit at the intersection of these audiences - the people who build, govern, and manage the data infrastructure that everyone else depends on.

## Setup

- Students remain in their groups with their completed worksheets and challenge logs
- Instructor stands at front and facilitates; this is a guided conversation, not a lecture
- Use a whiteboard or shared screen to capture key points as they emerge
- Aim for student voices making up ~70% of the talking time

## Facilitation Tips

- Start each lens with the framing prompt (read it aloud or display it)
- Let 2-3 groups respond before moving to the next question
- If a group gives a vague answer ("it's bad for patients"), push them to be specific: "Which data issue? What specific harm? To whom?"
- Reference specific issues from their datasets by name - this validates their work and makes the discussion concrete
- Watch the clock: 6-7 minutes per lens is tight. It's better to go deep on 2 questions than shallow on all of them.

---

## Lens 1: What Were Your Challenges? (6 minutes)

**Opening:** Quick round-robin. Each group states their single biggest frustration in one sentence. No discussion yet - just collect them. Write them on the board.

Then ask:

1. "Look at this list. How many of these are purely technical problems, and how many are organizational or governance problems?"
   - *Guide students to see that most technical problems (no shared ID, no agreed format) are actually governance failures - someone needed to set a rule and no one did.*

2. "Hospital group - when you received data from 7 systems simultaneously, what happened? Could you actually use it?"
   - *Expected: overwhelm, couldn't match patients, couldn't interpret fields, gave up on some data*

3. "Insurance group - what surprised you about trying to build a financial picture from everyone else's data?"
   - *Expected: clinical systems weren't built with billing in mind, baby had no identity, timestamps didn't align*

4. "Did anyone accidentally use the wrong data or misinterpret a field? What happened?"
   - *This surfaces the human cost of bad data quality - real people make real mistakes*

---

## Lens 2: Executive Decision-Making Impact (7 minutes)

**Read aloud:** *"You are no longer a student. You are now the CIO, CFO, or Chief Quality Officer of a hospital system or a regional health authority. The data problems you just experienced are happening every day across your organization."*

Ask these in order, spending ~2 minutes each:

1. **"Can you measure what you can't see?"**
   A regional health authority asks: "How many preeclampsia cases did we have last year, and what were maternal and neonatal outcomes across all facilities?" Based on what you experienced today, could you answer that?
   - *Key insight: if you can't link records across settings, you can't do population health analytics. Executives are making strategic decisions on incomplete data.*

2. **"What is the cost of a bad system choice?"**
   You're a CIO choosing between two systems: one uses proprietary coding, the other supports open standards. What did today teach you about the 10-year cost of that decision?
   - *Key insight: the purchase price of a system is a fraction of the total cost. Integration, data migration, and interoperability are where the real money goes.*

3. **"Can you trust your own dashboard?"**
   If the data underneath has truncated test names, mismatched identifiers, and inconsistent units, what does that mean for any KPI or performance metric built on top of it?
   - *Key insight: every executive dashboard is only as good as its data pipeline. "Garbage in, garbage out" is not a cliche when it drives budget allocation.*

---

## Lens 3: Patient Quality of Care and Cost (7 minutes)

**Read aloud:** *"Every data problem you encountered today has a patient on the other side of it. And every workaround has a price tag."*

### Patient Safety (3-4 minutes)

Pick 2-3 of these based on what resonated most during the exercise:

- **The anti-Kell antibody:** "The lab found it. The test name was truncated. The hospital isn't sure. Marie needs an emergency cesarean and might need a blood transfusion. What happens next?"
  - *Expected: delay to re-contact lab, risk of transfusion reaction, use of universal donor blood (limited supply)*

- **The medication discrepancy:** "Is Marie on 500mg or 750mg of methyldopa per day? The clinic says one thing, the patient says another. Her blood pressure is 180/110 right now."
  - *Expected: clinician has to stop and make phone calls during an emergency, or make a guess*

- **Baby Louise's identity:** "The hospital chart says 'BG DUPONT.' The PMI says 'Louise DUPONT.' The insurance says 'dependent 01.' The metabolic screening results come back in 2 weeks addressed to 'Baby Girl DUPONT.' Who receives them? What if they get lost?"
  - *Expected: follow-up falls through cracks, screening results not acted on*

### Cost (3-4 minutes)

- **"Count the workarounds."** "During Phase 2, how many times did you wish you could just call the other group and ask what their data meant? In real life, that call happens - and it's a nurse, a billing specialist, or an IT analyst spending 15 minutes on the phone. Multiply that by every patient encounter, every day."
  - *Ask: "If it takes 15 minutes of staff time to reconcile one patient's records across 3 systems, and your hospital sees 200 patients per day, what is the annual labor cost of poor interoperability?"*
  - *(Back-of-napkin: 200 patients x 15 min x 365 days = 18,250 hours/year = ~9 FTEs doing nothing but data reconciliation)*

- **"The duplicate claim."** The PMI visit was billed twice - once under the baby and once under the mother. In real healthcare, duplicate claims generate audits, denials, appeals, and administrative overhead. What system design would have prevented it?

- **"The hidden cost of missing data."** If Marie's gestational diabetes history doesn't reach the hospital, she might receive treatment that conflicts with her condition, or miss monitoring that prevents a complication. A preventable complication can cost tens of thousands in additional care. The interoperability failure upstream cost nothing to fix but everything to recover from downstream.

---

## Closing (1-2 minutes)

End with this single question. Let 2-3 students answer. Do not try to reach consensus - the point is to hear different perspectives.

> "If you could change ONE thing about how these 8 systems work together - not the clinical care, but the data infrastructure underneath it - what would it be? And who in the organization has the authority to make that change happen?"

*Key insight to draw out: the answer is almost never "buy better software." It's usually governance - someone with authority needs to mandate a shared identifier, a common format, a data-sharing agreement. Technology enables interoperability, but leadership and policy make it happen.*

---

## After the Reflection

Optionally ask students to write a 1-paragraph individual response to the closing question and submit it. This serves as both a formative assessment and a record of their thinking that can be revisited later in the curriculum.
