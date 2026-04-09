# Interoperability Lab: The Journey of a Maternity Patient Across the French Healthcare System

## SHIFT Program - France

**Duration:** 3 hours
**Format:** Group-based simulation exercise
**Topic:** Health Data Interoperability - Challenges, Standards, and Solutions

---

## Overview

In this exercise, students simulate a real-world healthcare interoperability scenario. Each group represents a different healthcare setting involved in the care of **Marie Dupont**, a 32-year-old pregnant woman with gestational diabetes and developing preeclampsia, through to the birth of her baby. Each group receives a synthetic dataset from their setting's perspective, works through data quality issues, then must share and integrate data with other groups - experiencing firsthand the challenges of health information exchange.

**Important Note for Students:** You do not need clinical or medical knowledge to complete this exercise. Your role is that of a health information management professional, healthcare administrator, data analyst, or IT system administrator - the people who build, maintain, and manage the systems that store and exchange health data. A **Clinical Reference Sheet** is provided to help you understand the medical terms in the datasets. Your focus is on the **data** - its structure, quality, format, and how it moves (or fails to move) between systems.

## Learning Objectives

By the end of this exercise, students will be able to:

1. Identify common data quality issues (type mismatches, truncation, missing values, encoding errors, inconsistent formats)
2. Recognize how different healthcare settings collect and structure the same patient's data differently
3. Experience the practical barriers to health data exchange across organizations
4. Understand why interoperability standards (HL7 FHIR, IHE profiles, CI-SIS in France) exist
5. Articulate the relationship between data governance, patient safety, and interoperability
6. Discuss GDPR considerations in cross-organizational data sharing
7. Analyze mother-baby record linkage as a unique interoperability challenge
8. Understand how payer/insurance data creates additional data exchange requirements and complexities

---

## The Patient Story: Marie Dupont

Marie Dupont is a 32-year-old woman, pregnant with her second child. She lives in a mid-sized French city. Her care journey spans multiple settings over several months:

1. **Prenatal care** with her sage-femme (midwife) at a community practice (Months 4-8)
2. **Laboratory testing** at an independent lab for routine bloodwork and glucose tolerance testing
3. **Imaging** at a radiology center for ultrasounds and Doppler studies
4. **Specialist consultations** at an obstetric clinic when gestational diabetes is identified
5. **Emergency transfer** via SAMU/ambulance at 38 weeks when she develops severe preeclampsia symptoms
6. **Hospital admission** at the maternity ward for emergency delivery (cesarean section)
7. **Postnatal follow-up** through PMI (Protection Maternelle et Infantile) for mother and newborn
8. **Insurance/payer processing** by the national health insurance fund for claims and reimbursement

**Clinical Timeline:**
- Week 12: First prenatal visit with sage-femme; referred for dating ultrasound
- Week 14: First trimester labs (blood type, serology, blood count)
- Week 16: Imaging center - dating/morphology ultrasound
- Week 24: Glucose tolerance test (HGPO 75g) at laboratory - gestational diabetes diagnosed
- Week 26: Referred to obstetric clinic for specialist management
- Week 28: Follow-up labs, growth ultrasound
- Week 32: Specialist visit - blood pressure elevated, proteinuria noted
- Week 36: Growth ultrasound showing reduced amniotic fluid
- Week 38: At home, develops severe headache and visual disturbances. Partner calls 15 (SAMU). Emergency transfer to hospital.
- Week 38: Emergency cesarean delivery. Baby girl born, 2.9 kg, Apgar 8/9.
- Week 38+3 days: Discharge from hospital
- Week 40: PMI postnatal home visit for mother and newborn
- Ongoing: Insurance claims processed for each encounter across all settings

---

## Key Concept: Mother-Baby Record Linkage

One of the most challenging interoperability problems in maternity care is the relationship between the mother's record and the baby's record. This exercise highlights these issues across multiple groups.

### Why Mother-Baby Linkage Is Uniquely Difficult

**The baby has no identity at birth.** When a baby is born, they do not yet have:
- A name (the parents may not have decided yet, or civil registration may take days)
- A national health ID number (not assigned until after birth registration)
- An insurance number (initially covered under the mother's policy, then must be registered separately)

**Temporary naming conventions vary by system.** Until the baby is officially named, different systems record the newborn differently:
- Hospital system: "Baby Girl DUPONT" or "BG DUPONT" or "NEWBORN DUPONT"
- Birth register: "DUPONT, unnamed female"
- Insurance: inherits mother's policy number with a dependent suffix
- Public health: records baby under "Mother: DUPONT Marie - Baby: F, DOB 28/01/2026"

**Once the baby is named, records must be updated** - but not all systems update at the same time. The hospital may still show "Baby Girl DUPONT" while the civil register already shows "Louise DUPONT" and the insurance system shows "DUPONT Louise" with a new beneficiary number.

**In France specifically:**
- Parents can choose the mother's last name, father's last name, or a hyphenated combination (since 2005 law). If Marie Dupont and Thomas Dupont are the parents, the baby could be: DUPONT, DUPONT-DUPONT, or if the father had a different surname, any combination.
- Civil registration (declaration de naissance) must happen within 5 days of birth
- The baby's INS (national health ID) is generated only after civil registration

**What links mother and baby?**
Each system uses a different linkage method:
- Hospital: mother's local ID (IPP) + newborn suffix (e.g., NNE-2026-88431-01)
- Lab: baby may get own lab orders under mother's name with note "newborn of..."
- Insurance: mother's beneficiary number + dependent code
- Public health: mother's name + baby's DOB (no formal ID linkage)

### What Students Should Look For
In the datasets, watch for:
- How is the baby identified in each system? Is there a consistent baby ID?
- How is the baby linked to the mother? What happens if the mother's name is wrong?
- What happens when the baby is named "Louise" but some systems still say "Baby Girl"?
- If the mother's record has errors (misspelled name, wrong DOB), do those errors propagate to the baby's record?
- How would you merge baby data from the hospital with baby data from the PMI visit if the identifiers don't match?

---

## Group Assignments

### Group 1: Cabinet de Sage-femme (Midwife Practice)

**Setting:** Independent community midwife practice providing prenatal care
**System:** Small practice management software with basic EHR
**Dataset characteristics:**
- Handwritten notes partially digitized
- Mix of structured and free-text data
- Inconsistent date formats (DD/MM/YYYY in some records, DD-MMM-YY in others)
- Patient identified by name + date of birth (no national health ID recorded consistently)
- Blood pressure recorded inconsistently (e.g., "12/8" French style vs "120/80 mmHg")
- Weight in kg but sometimes with commas as decimal separators (French convention: 72,5 vs 72.5)
- Some accent characters corrupted (e.g., "premi\u00e8re" appearing as "premi??re" or "premiÃ¨re")

### Group 2: Laboratoire d'Analyses Medicales (Clinical Laboratory)

**Setting:** Independent laboratory performing blood tests and urinalysis
**System:** Laboratory Information System (LIS)
**Dataset characteristics:**
- Highly structured numerical data
- Uses NABM codes (Nomenclature des Actes de Biologie Medicale) - not universally known outside French labs
- Some test names truncated to 20 characters due to legacy system field limits
- Glucose values in mmol/L (some historical values in g/L from a system migration)
- Results stored as text strings even when numeric (e.g., "5.2" as text, not number)
- Reference ranges included but formatted inconsistently
- Patient identified by INS (Identifiant National de Sante) + name
- Some flag fields use "H"/"L"/"N" (Haut/Low/Normal - mixing French and English)

### Group 3: Centre d'Imagerie Medicale (Imaging Center)

**Setting:** Radiology and imaging center performing obstetric ultrasounds
**System:** RIS/PACS (Radiology Information System)
**Dataset characteristics:**
- Structured metadata (dates, patient ID, exam type) + unstructured narrative reports
- Reports written in free-text French (medical abbreviations, no standard coding)
- DICOM metadata fields present but some populated inconsistently
- Patient name field limited to 30 characters (truncation of hyphenated names)
- Exam dates in YYYYMMDD format (DICOM standard) vs DD/MM/YYYY in the report text
- Measurements in mm but sometimes recorded with unit, sometimes without
- Some reports are scanned PDFs (represented as "Report: [PDF - not machine readable]")
- Uses internal exam codes that don't map to CCAM codes

### Group 4: Clinique Obstetrique (Obstetric Clinic)

**Setting:** Specialist obstetric clinic managing high-risk pregnancies
**System:** Specialized obstetric EHR
**Dataset characteristics:**
- Well-structured clinical data with CIM-10 (French ICD-10) diagnosis codes
- CCAM procedure codes for consultations
- Medication data with CIS codes (French drug database)
- Patient identified by Carte Vitale number (different from INS)
- Some duplicate entries from system migration (same visit recorded twice with slight variations)
- Allergy field uses free text in one record, coded values in another
- Referral letters stored as free text blobs
- Some fields use clinical abbreviations without expansion (SA = semaines d'amenorrhee, HTA = hypertension arterielle)

### Group 5: SAMU / Ambulance (Emergency Medical Services)

**Setting:** SAMU dispatch and ambulance transport
**System:** Emergency dispatch system + handwritten transport records
**Dataset characteristics:**
- Minimal dataset - collected under time pressure
- Timestamps in HH:MM 24-hour format but date sometimes missing (assumed "today")
- Vital signs recorded at intervals but with inconsistent field names (TA vs BP vs "tension")
- Patient name recorded phonetically by dispatcher (may contain errors: "Du Pont" vs "Dupont")
- Address field has abbreviations (Bd = Boulevard, R = Rue)
- Glasgow Coma Scale recorded but field expects text, contains number
- Triage category uses local color coding (not standardized)
- Sparse clinical history - "G2P1 38 SA diabete gesta" (heavily abbreviated)
- Handoff notes field limited to 200 characters - truncated mid-sentence

### Group 6: Hopital - Service Maternite (Hospital L&D Ward)

**Setting:** Public hospital maternity unit
**System:** Hospital Information System (SIH/DPI)
**Dataset characteristics:**
- Most comprehensive and structured dataset
- Uses multiple coding systems simultaneously (CIM-10, CCAM, UCD for drugs)
- HL7v2 message fragments included (ADT admission message)
- Patient matched via INS but also has local hospital ID (IPP - Identifiant Permanent du Patient)
- Timestamps in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Includes both mother and newborn records (linked by different ID schemes)
- Some lab results imported from external lab but with mapping issues (different test names)
- Discharge summary in semi-structured format with coded + narrative sections
- Medication reconciliation shows discrepancies with clinic prescriptions

**Mother-Baby linkage issues (key focus for this group):**
- Newborn initially registered as "BG DUPONT" (Baby Girl DUPONT) with hospital-generated ID NNE-2026-88431-01
- Baby's name later updated to "Louise DUPONT" after civil registration but some records still show "BG DUPONT"
- Newborn linked to mother via hospital ID suffix convention (mother: IPP-2026-88431, baby: NNE-2026-88431-01) - but this convention is hospital-specific and won't be understood by other systems
- Newborn has no national health ID yet
- Baby's blood type needs separate testing (especially critical given mother's anti-Kell antibody) but lab order is placed under mother's name with note "for newborn"
- Discharge produces TWO separate summaries (mother + baby) but they reference each other with different ID formats

### Group 7: PMI - Protection Maternelle et Infantile (Public Health / Postnatal)

**Setting:** Government public health service for maternal and child health
**System:** Legacy departmental database (Conseil Departemental)
**Dataset characteristics:**
- Focus on social determinants and public health surveillance
- Uses INSEE codes for geographic data
- Collects data from multiple sources - some fields are second-hand (transcribed from health booklet)
- Date format inconsistent (some DD/MM/YYYY, some YYYY-MM-DD from newer module)
- Newborn identified by mother's name + DOB (no INS assigned yet at time of visit)
- Vaccination data uses ATC codes (different from CIS codes used by clinic)
- Weight recorded in grams for newborn, kg for mother (but field label just says "weight")
- Some legacy fields still use ISO-8859-1 encoding while system now expects UTF-8
- Includes socioeconomic data fields not present in any other dataset

**Mother-Baby linkage issues:**
- Baby recorded as "Louise DUPONT" (the official name) - but hospital records may still show "BG DUPONT"
- No baby national health ID - PMI identifies baby by "mother name + baby DOB + baby sex"
- Mother and baby data are in the SAME record rows (not separate), making it ambiguous which weight/measurement belongs to whom
- No formal link to hospital records - PMI nurse transcribed data from the paper health booklet brought by the mother

### Group 8: Assurance Maladie / CPAM (Health Insurance / Payer)

**Setting:** National health insurance fund (Caisse Primaire d'Assurance Maladie) processing claims
**System:** Claims processing and reimbursement system
**Dataset characteristics:**
- Purely administrative and financial - no clinical details
- Uses beneficiary number (different from INS and insurance card number)
- Claims coded with procedure/service codes mapped to fee schedules
- Diagnosis codes required for certain claims but often less specific than clinical records
- Baby initially covered as a dependent (beneficiary = mother, with "ayant droit" dependent link)
- After birth registration, baby gets own beneficiary number - but claims before that date are under mother's number
- Dates are processing dates (when claim was received) not service dates - these may differ by days or weeks
- Provider identified by FINESS number (facility code) and RPPS number (individual practitioner code)
- Some claims rejected/pending with error codes that are system-specific
- Amount fields in euros with centimes (decimal formatting issues)
- Multiple claims for same encounter (professional fee + facility fee + lab fee = separate line items)
- Maternity pathway ("parcours maternite") has special reimbursement rules - 100% coverage from month 6

**Mother-Baby linkage issues:**
- All prenatal claims are under mother's beneficiary number
- Delivery claims include both mother and baby but coded as mother's encounter
- Baby's first claims (newborn exam, hearing screen, vaccines) may be filed under EITHER the mother's number with a dependent code OR a new beneficiary number - depending on whether civil registration has been processed
- If baby is filed under wrong beneficiary, claims are rejected - creating a gap in the baby's health record from the payer perspective

---

## Exercise Structure (3 Hours)

### Phase 1: Data Discovery and Quality Assessment (45 minutes)

**Objective:** Each group examines their dataset, identifies data quality issues, and documents them.

**Instructions:**
1. Open your group's CSV file (provided by the instructor)
   - Open it in Excel, Google Sheets, or LibreOffice Calc
   - **Important:** If columns appear scrambled, check the delimiter: Groups 1, 2, and 4 use **semicolons** (`;`); Groups 3, 5, 6, 7, and 8 use **commas** (`,`)
   - In Excel: use Data → From Text/CSV and specify the correct delimiter
2. Review every column: understand what it represents, check the data type, look for anomalies
3. Complete the **Data Quality Assessment Worksheet** (provided below):
   - List every data quality issue found
   - Classify each issue: format inconsistency, missing data, truncation, encoding error, type mismatch, duplicate, ambiguous coding
   - Assess severity: would this issue affect patient care if data were shared?
   - Propose a fix for each issue within your dataset
   - Think ahead: will this issue cause a problem when you try to insert this data into the HIE database?
4. Clean your dataset as best you can — document what you changed and why
5. Prepare a 2-minute summary of your setting's key data challenges
6. **Preview the HIE schema** before Phase 2 starts: open **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**, select your group in the sidebar, and browse the schema reference — this will help you anticipate what transformations you'll need

**Deliverable:** Completed Data Quality Assessment Worksheet + cleaned dataset

### Phase 2: Data Exchange Simulation (45 minutes)

**Objective:** Each group submits their data to the shared HIE. The class then queries the combined result — discovering firsthand what happens when 8 different systems try to represent the same patient.

**Instructions:**

**Part A — Submit your data (30 minutes):**
1. Open the **HIE Streamlit App** in your browser: **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**
2. Select your group in the left sidebar
3. Review the schema for your target tables (sidebar → Quick Schema Reference)
4. Write SQL INSERT statements in the **Insert Data** tab to load your cleaned data into the HIE
   - Insert your patient first, then encounters, then clinical data (vitals, labs, medications, etc.)
   - Write down each row ID returned — you will need them for subsequent inserts
   - See `streamlit_app_guide.md` for INSERT examples specific to your group
5. Document every obstacle in your **Interoperability Challenge Log** as you go:
   - What data transformations did you have to make to fit the HIE schema? (date formats, units, number formats, splitting fields)
   - What errors did your INSERT statements produce — and what does each error tell you about the incompatibility?
   - What data from your source could not be mapped to any HIE field? What did you lose?
6. Check the **Dashboard** tab to see class-wide progress

**Part B — Query the shared database together (15 minutes):**

Once most groups have submitted, run these queries in the **Query Data** tab — either follow along on screen or type them yourself. For each one, look at the results carefully and record what you find in your Interoperability Challenge Log.

**Query 1 — How many times was Marie Dupont registered?**
```sql
SELECT patient_id, last_name, first_name, date_of_birth, national_health_id, source_system
FROM patients
WHERE UPPER(last_name) LIKE '%DUPONT%' OR UPPER(last_name) LIKE '%DU PONT%';
```
*What to look for: Are there multiple rows? Do the names match exactly? Does every group have a national_health_id, or is it blank for some? Without a shared unique ID, how would you know these are all the same person?*

**Query 2 — Did any group accidentally register the wrong patient?**
```sql
SELECT patient_id, last_name, first_name, date_of_birth, source_system
FROM patients
WHERE UPPER(last_name) = 'DUPOND';
```
*What to look for: "DUPOND" is a different patient in Group 4's dataset — born one day apart from Marie Dupont. If any group inserted this record, it would pollute the HIE with a false patient.*

**Query 3 — What does Marie Dupont's care timeline look like?**
```sql
SELECT e.encounter_date, e.encounter_time, e.encounter_type,
       e.facility_name, e.chief_complaint, e.diagnosis_text, e.source_system
FROM encounters e
JOIN patients p ON e.patient_id = p.patient_id
WHERE UPPER(p.last_name) = 'DUPONT'
ORDER BY e.encounter_date, e.encounter_time;
```
*What to look for: Is the timeline complete — does it go from the first prenatal visit to the postnatal visit? Are there gaps? Are dates in a consistent format, or did some groups not convert correctly?*

**Query 4 — Can you find baby Louise, and is she linked to her mother?**
```sql
SELECT patient_id, last_name, first_name, date_of_birth,
       related_patient_id, relationship_type, source_system
FROM patients
WHERE date_of_birth = '2026-01-28';
```
*What to look for: Did all groups that have baby data submit her as a separate patient? Is her name consistent across groups (Louise DUPONT vs BG DUPONT)? Is the `related_patient_id` filled in, linking her to her mother?*

**Query 5 — Are medication doses consistent across systems?**
```sql
SELECT m.medication_name, m.dose, m.frequency, m.notes, m.source_system
FROM medications m
JOIN patients p ON m.patient_id = p.patient_id
WHERE UPPER(m.medication_name) LIKE '%METHYLDOPA%';
```
*What to look for: Does every group that recorded this medication agree on the dose? If Group 4 says 500mg/day and another source suggests 750mg/day, which is correct? What would a clinician have to do to resolve this?*

**Query 6 — Do duplicate patients exist across groups?**
```sql
SELECT last_name, first_name, date_of_birth, COUNT(*) AS registrations
FROM patients
GROUP BY UPPER(last_name), UPPER(first_name), date_of_birth
HAVING COUNT(*) > 1;
```
*What to look for: Any row here means the same person was registered more than once. Does the HIE have any way to automatically detect this? What would need to be true for this query to return zero rows?*

**Rules:**
- SQL errors are not failures — they are data points. Every error reveals a real interoperability barrier. Document them.
- If a field from your source data cannot be mapped to any HIE column, set it to NULL and record the gap in your Challenge Log — do not invent a mapping.

**Deliverable:** Interoperability Challenge Log documenting your submission obstacles + the class's shared query results

### Phase 3: Standards and Solutions Workshop (45 minutes)

**Objective:** Groups collaborate to design an interoperability solution, then learn about real standards.

**Part A - Design Your Own Standard (20 minutes):**

1. Form a "standards committee" with one representative from each group. The remaining group members stay at their seats and will be asked to apply whatever the committee decides.

2. The committee works through these five questions — use the query results from Phase 2 as your evidence:

   **Question 1 — Patient identity**
   Look at Query 1 results: Marie Dupont appeared multiple times with slight variations. What single piece of information, if every system were required to record it, would guarantee you could match the same patient across all 8 systems? What would you call this field? What format would it use (numbers only? letters and numbers? how many characters)? What happens to patients who don't have this identifier yet — like a newborn?

   **Question 2 — Dates and times**
   Your data had at least four different date formats (DD/MM/YYYY, DD-MMM-YY, YYYYMMDD, YYYY-MM-DD). Pick one. Write it down exactly. Now — does your chosen format include time? What timezone? What happens to records that were created before your standard existed?

   **Question 3 — Minimum required fields**
   If every healthcare setting had to submit exactly the same fields to the HIE — no more, no less — what would those fields be? Think about the smallest set of information that would allow you to: identify the patient, understand what happened, know when and where it happened, and link a mother's record to her baby's record.

   **Question 4 — Codes for diagnoses and medications**
   Group 4 used CIM-10 codes. Group 7 used ATC codes. Group 2 used NABM codes. Group 5 used free text. Could you pick one coding system for all settings? What would you force a midwife practice — which currently uses no codes — to do? Who pays for that?

   **Question 5 — File format for exchange**
   When your system needs to send data to another system, what format should the file be in? CSV? Something else? What are the rules about column names, delimiter characters, and encoding (especially for accented French characters)?

3. Once the committee has agreed on answers, remaining group members spend 5 minutes trying to apply the committee's rules to their own dataset. Can they actually do it?

4. Full class discussion: What was hardest to agree on? What did a group member discover when they tried to apply the committee's decision that the committee hadn't anticipated?

**Part B - Real-World Standards Introduction (25 minutes):**
Instructor-led discussion mapping the students' experience to real interoperability frameworks:

| Student Experience | Real-World Standard/Solution |
|---|---|
| Common patient ID | INS (Identifiant National de Sante), MPI (Master Patient Index) |
| Common date format | ISO 8601 (required by HL7 FHIR) |
| Minimum dataset | Volet de Synthese Medicale (VSM), IPS (International Patient Summary) |
| Common coding | CIM-10, LOINC, SNOMED CT, CCAM, ATC |
| Exchange format | HL7 FHIR (resources: Patient, Observation, Encounter, etc.) |
| Exchange architecture | DMP, MSSante (secure health messaging), IHE profiles (XDS, PDQ, PIX) |
| Consent and security | GDPR, cadre d'interoperabilite des SI de sante (CI-SIS) |
| Mother-baby linkage | RelatedPerson resource (FHIR), MPI with family linking |
| Payer data exchange | FHIR ExplanationOfBenefit, Claims resources, NOEMIE protocol (France) |

**In-app FHIR demonstration (5 minutes):**
Navigate to the **FHIR Explorer** tab in the HIE app (the same browser window students have been using). Select "Patient" as the resource type, then select Marie Dupont's record. Show students:
- How the same data they inserted as SQL rows is now represented as a structured JSON resource
- The `identifier` array — where the INS, Carte Vitale, and source IDs appear as separate coded identifiers
- The `link` field on the baby's record that references the mother (this is the FHIR equivalent of the `related_patient_id` they set in SQL)
- Switch to "Observation" and show a lab result — point out the LOINC code and the structured `valueQuantity`
- Show the side-by-side view: HIE database row (left) vs FHIR resource (right)

**Optional additional demonstration:** POST a FHIR Patient resource to the HAPI FHIR public test server at http://hapi.fhir.org/ to show students a live, real-world FHIR exchange.

### Phase 4: Debrief and Reflection (45 minutes)

**Part A - Group Presentations (25 minutes):**
Each group presents (2-3 minutes each):
1. The top 3 data quality issues in their dataset
2. The biggest barrier they faced when sharing/receiving data
3. One insight about why interoperability is difficult

**Part B - Structured Reflection: From Data Problems to Real-World Impact (20 minutes)**

This reflection bridges the technical exercise to organizational strategy. The goal is for students to connect the data issues they just experienced to three real-world consequences: executive decision-making, patient quality and safety, and cost.

**Format:** Instructor-facilitated discussion. Students remain in their groups but respond to the room. The instructor guides through three lenses in sequence, spending roughly 6-7 minutes on each. Students may reference their worksheets and challenge logs.

---

#### Lens 1: What Were Your Challenges? (6 minutes)

Start with a quick round-robin: each group states in one sentence their single biggest frustration during the exercise. Then discuss:

- At what point did you realize that cleaning your own data was not enough - that the real problem was what happened when your data met someone else's data?
- Which challenges were **technical** (format, encoding, data types) and which were **organizational** (no shared ID scheme, no agreement on what data to collect, no governance)?
- Did any group make assumptions about how the HIE schema worked that turned out to be wrong? What did that assumption cost you?
- When you queried the shared database and saw all groups' data together — what was the first thing that surprised you? What did you expect to find that wasn't there?
- Group 8 (Insurance): what surprised you about trying to map financial claims onto a schema that was built around clinical events?

---

#### Lens 2: How Does This Impact Executive Decision-Making? (7 minutes)

Prompt: *"You are no longer a student. You are now the Chief Information Officer, Chief Financial Officer, or Chief Quality Officer of a hospital system or regional health authority. The data problems you just experienced are happening every day across your organization. How does this affect your ability to lead?"*

Discussion questions:

- **Strategic planning:** If your organization cannot reliably link a mother's records to her baby's records across departments, how can you accurately report on maternity outcomes? How does a hospital board make investment decisions about a maternity ward if the outcome data is incomplete or unreliable?
- **Population health management:** A regional health authority wants to know: "How many women in our region developed preeclampsia last year, and what were their outcomes?" Based on what you experienced today, could you answer that question with confidence using data from multiple providers? What would be missing?
- **Vendor and system decisions:** If you are a CIO choosing between two EHR systems, and one uses proprietary coding while the other supports open standards, what did today's exercise teach you about the long-term cost of that choice?
- **Performance measurement:** Executives rely on dashboards and KPIs. If the underlying data has the quality issues you discovered today - truncated test names, mismatched identifiers, inconsistent units - what does that mean for any metric built on top of that data? Can you trust your own reports?
- **Regulatory compliance:** GDPR requires that you can produce a complete record of a patient's data on request. Based on today's exercise, could you locate and compile all of Marie Dupont's data across 8 systems? How long would it take? What would you miss?

---

#### Lens 3: How Does This Impact Patient Quality of Care and Cost? (7 minutes)

Prompt: *"Every data problem you encountered today has a patient on the other side of it. And every workaround has a cost."*

**Patient quality and safety:**

- The anti-Kell antibody was identified by the lab but the test name was truncated. In a real scenario, if the hospital cannot confirm the specific antibody before an emergency cesarean requiring blood transfusion, what happens to the patient? (Answer: transfusion reaction risk, delay while lab is re-contacted, or use of universal donor blood which may be in limited supply.)
- The hospital couldn't confirm whether Marie's methyldopa dose was 500mg/day or 750mg/day. What is the clinical consequence of guessing wrong? What do real clinicians do when they encounter this? (Answer: they call the clinic, the patient, or the pharmacy - adding time, phone calls, and delay in a situation where minutes matter.)
- Baby Louise's lab results were ordered under her mother's name. In a busy neonatal unit, what is the risk of those results being filed in the wrong chart? What downstream decisions depend on the baby's blood type being correctly attributed?
- If the PMI nurse cannot match Baby Louise's records to her hospital stay (because the hospital says "BG DUPONT" and the PMI says "Louise DUPONT"), what follow-up care might fall through the cracks? (Answer: metabolic screening results pending, vaccination tracking, identification of complications.)

**Cost:**

- Every time a clinician, administrator, or billing specialist has to manually reconcile data between systems - making phone calls, looking up records, correcting entries - that is labor cost. In your exercise, how many of these manual workarounds did you identify? Now multiply that by every patient, every day, across an entire health system.
- The insurance group discovered a duplicate claim for the PMI visit. In real healthcare, duplicate claims cost payers billions annually. What system design would have prevented that specific duplicate?
- The hospital's DRG-based claim bundled all inpatient services into one payment. But the external lab, the ambulance, and the clinic each submitted separate claims. If the payer cannot easily reconcile these as related to the same patient episode, what happens? (Answer: audits, payment delays, appeals - all administrative cost.)
- When a corrected lab result exists (the glucose value that was wrong then corrected), and a system uses the wrong one, what is the cost? It could be an unnecessary medication, an unnecessary consultation, or a missed diagnosis. Each has both a patient safety and a financial dimension.

**Closing question for all students:**
> If you could change ONE thing about how these 8 systems work together - not the clinical care, but the data infrastructure - what would it be, and who in the organization has the authority to make that change happen?

---

## Worksheets

### Data Quality Assessment Worksheet

Use this worksheet during **Phase 1** to document every problem you find in your group's CSV file.

**Issue Types:** Format Inconsistency (FI), Missing Data (MD), Truncation (TR), Encoding Error (EE), Type Mismatch (TM), Duplicate (DU), Ambiguous Coding (AC), Other (OT)

**Severity:** 1 = Minor (cosmetic, no impact on care), 2 = Moderate (requires manual fix before sharing), 3 = Critical (could cause a clinical error if shared as-is)

**Completed example — so you know what a filled row looks like:**

| # | Field Name | Issue Description | Issue Type | Severity (1-3) | Patient Safety Impact? | Proposed Fix |
|---|-----------|-------------------|------------|----------------|----------------------|-------------|
| *ex* | *blood_pressure* | *Recorded as "11/7" (French shorthand) instead of separate systolic/diastolic values. The HIE requires two numeric fields: systolic_bp and diastolic_bp.* | *FI* | *2* | *Yes — "11/7" could be misread as 11 mmHg systolic, which is incompatible with life. The correct reading is 110/70 mmHg.* | *Split into two fields: systolic = 110, diastolic = 70. Multiply French shorthand by 10.* |

**Your worksheet:**

| # | Field Name | Issue Description | Issue Type | Severity (1-3) | Patient Safety Impact? | Proposed Fix |
|---|-----------|-------------------|------------|----------------|----------------------|-------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |
| 8 | | | | | | |

---

### Interoperability Challenge Log

Use this log during **Phase 2** to document every obstacle you hit while submitting your data to the HIE and while exploring the shared database.

There are two types of entries:
- **Submission obstacle** — something that prevented or complicated your INSERT (e.g., a SQL error, a field that didn't exist in the schema, a value you had to convert)
- **Query discovery** — something surprising or broken you found when querying all groups' data together (e.g., the same patient registered three different ways, missing records, conflicting values)

**Completed example — so you know what a filled row looks like:**

| # | Type | Your Group | Data Element | What Happened | Was it resolved? | How / What would fix it? |
|---|------|-----------|-------------|---------------|-----------------|--------------------------|
| *ex* | *Submission obstacle* | *Group 1 - Midwife Practice* | *weight_kg* | *Source data had "68,5" (French comma decimal). INSERT failed with datatype mismatch because the HIE field expects a number, not text. Had to change to "68.5" before the INSERT would succeed.* | *Yes* | *Manually replaced comma with dot. A real system fix: configure the source EHR to export decimals in ISO format, or add a transformation rule at the HIE ingestion layer.* |
| *ex* | *Query discovery* | *All groups* | *patients.last_name* | *Running "SELECT * FROM patients" showed Marie Dupont registered 6 times with slight variations: DUPONT, Dupont, DU PONT, DUPOND. None of the records had a shared unique identifier to confirm they are the same person.* | *No* | *Requires a Master Patient Index (MPI) with a probabilistic matching algorithm, or a national unique health ID (INS) that all systems are required to record.* |

**Your log:**

| # | Type | Your Group | Data Element | What Happened | Was it resolved? | How / What would fix it? |
|---|------|-----------|-------------|---------------|-----------------|--------------------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |
| 8 | | | | | | |

---

## Platform and Tools Recommendations

### For the Exercise (Free Options)

**Option A: Google Sheets (Simplest - Recommended for first run)**
- Each group gets a Google Sheet with their dataset pre-loaded
- A shared "Exchange" Google Sheet serves as the integration platform
- Groups export their cleaned data to their tab in the Exchange sheet
- Hospital group and PMI group attempt to build an integrated view
- Advantages: No setup, everyone knows it, real-time collaboration visible
- Limitation: Doesn't simulate real system-to-system exchange

**Option B: CSV Files + Shared Google Drive Folder**
- Each group receives their dataset as a CSV file
- Groups clean data using any tool (Excel, Google Sheets, LibreOffice, Python)
- Groups upload cleaned CSV files to a shared folder
- Receiving groups must import and integrate using only the files (no verbal help)
- Advantages: More realistic - forces groups to deal with encoding, delimiters, format issues
- The CSV approach also naturally surfaces issues like delimiter conflicts (semicolons in French CSVs vs commas)

**Option C: HAPI FHIR Test Server (Most Sophisticated)**
- Public free FHIR server: http://hapi.fhir.org/
- In Phase 3, groups attempt to transform their data into FHIR resources and POST them
- Other groups query the server to retrieve data
- Advantages: Introduces FHIR hands-on, very realistic
- Limitation: Requires some technical comfort with JSON and REST APIs; better suited if students have some informatics background
- Alternative: Use the FHIR server for instructor demonstration only

**Option D: HIE Streamlit App — Cloud-Hosted Shared Database (Recommended for Informatics Learners)**

> **This is the primary option for this lab.** The app is hosted in the cloud — no installation, no local setup, no WiFi restrictions. Students open a URL in any browser and they are connected.

**App URL: https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**

- Nothing to install — students open the URL on any device (laptop, tablet, phone)
- A shared HIE SQLite database is hosted in the cloud; all students connect to the same database automatically
- Each group selects their group name in the sidebar; the app tracks submissions by group
- Groups write SQL INSERT statements to load their cleaned data into the shared HIE schema
- The **Dashboard** tab shows real-time submission progress across all 8 groups
- The **FHIR Explorer** tab automatically transforms submitted data into HL7 FHIR R4 resources — directly connecting the SQL exercise to real-world standards
- Surfaces schema mismatch, data type conversion, and ETL issues in a clear, guided interface

**The app has four tabs students will use:**

| Tab | Used In | Purpose |
|-----|---------|---------|
| Insert Data | Phase 2 | Write SQL INSERT statements to submit data to the HIE |
| Query Data | Phase 2 | Run SELECT queries to find other groups' data |
| Dashboard | Phase 2 & 4 | Track all groups' submission progress in real time |
| FHIR Explorer | Phase 3 | See the data as FHIR resources and compare to relational schema |

**See `streamlit_app_guide.md` for complete setup and student instructions**, including:
- Instructor setup (Python requirements, how to run the app, sharing URL with students)
- Resetting the database between sessions
- Student step-by-step guide with INSERT examples for every group
- Group-specific challenges and tips
- Verification queries for the debrief

### For Generating/Modifying Synthetic Datasets

- **Synthea** (https://synthetichealth.github.io/synthea/): Open-source synthetic patient generator. Can generate FHIR, CSV, HL7v2 formats. The pregnancy module can generate maternity care data. However, it generates US-style data - you would need to adapt identifiers, coding systems, and formats to French context.
- **Manual creation** (recommended for this exercise): Create the datasets by hand to precisely control which data quality issues appear in each one. The datasets below are designed for this purpose.

---

## Synthetic Datasets

The datasets are provided as separate CSV files (one per group). Each dataset tells part of Marie Dupont's story from that setting's perspective, with intentional data quality issues embedded throughout.

See the `/datasets/` folder for the CSV files:
- `group1_midwife_practice.csv`
- `group2_laboratory.csv`
- `group3_imaging_center.csv`
- `group4_obstetric_clinic.csv`
- `group5_ems_ambulance.csv`
- `group6_hospital_maternity.csv`
- `group7_public_health_postnatal.csv`
- `group8_insurance_payer.csv`

A **Clinical Reference Sheet** (`clinical_reference_sheet.md`) is provided for students who are not clinical professionals. Distribute to all groups.

The instructor answer key (`INSTRUCTOR_ANSWER_KEY.md`) documents all intentional data issues embedded in each dataset. **Do not distribute to students.**

---

## Ideas for Enhanced Sophistication

### 1. Add a Patient Safety Trigger
Embed a critical clinical finding in one group's dataset that, if not successfully communicated, leads to a patient safety risk. For example:
- The laboratory dataset shows Marie has a rare blood antibody (anti-Kell)
- This information is truncated in the lab's export: "Anticorps irr: POSIT" with no detail
- If the hospital doesn't get the full result, they might give incompatible blood during the cesarean
- This creates urgency and demonstrates real stakes of interoperability failures

### 2. RGPD/Consent Complications
Give one group (e.g., PMI) a consent restriction: Marie has refused to share her social situation data. The PMI dataset has fields that should be redacted before sharing. Groups must identify which fields contain sensitive social data and handle the consent restriction - introducing the concept of granular consent and data segmentation.

### 3. Add a Second Patient (Confusion Scenario)
Include in 2-3 datasets a second patient with a similar name: "Marie Dupond" (note: slightly different spelling), born one day apart. This forces groups to confront patient matching challenges and understand why unique identifiers matter.

### 4. Versioning / Corrections
In the laboratory dataset, include a corrected result that supersedes an earlier one (e.g., an initial glucose value that was wrong due to a pre-analytical error, with a corrected value issued later). Groups must figure out which value is current. This teaches about data versioning and amendment tracking.

### 5. Multilingual Element
Include one dataset (e.g., imaging) where a report was generated by a visiting radiologist and is partially in English. Groups must deal with language barriers in clinical documentation - relevant in cross-border European healthcare.

### 6. Timed Clinical Decision
At the start of Phase 2, give the Hospital group a clinical scenario requiring a decision within 20 minutes: "Marie's blood pressure is 180/110. You need her medication history, latest labs, and allergy information to manage her safely. Go." This adds time pressure and prioritization - they must decide what data they need most urgently from which groups.

### 7. Digital Health Wallet / Patient-Mediated Exchange
Designate one student as "Marie" who carries a paper folder with some (but not all) of her records - simulating a patient-held health record (carnet de sante / Mon Espace Sante). The hospital can ask "Marie" for information, but what she carries may be incomplete, outdated, or in yet another format.

### 8. Observer/Regulator Role
Assign 1-2 students as ARS (Agence Regionale de Sante) observers who monitor the data exchange process, flag RGPD violations, and report on system-level failures. They present their findings during the debrief.

---

## Instructor Preparation Checklist

### Technology Setup (Day Before)
- [ ] Open **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/** and confirm the app loads
- [ ] Sign in to **https://share.streamlit.io** — locate the app and confirm you can see the ⋮ menu and Reboot option
- [ ] Test the app on a second device (phone or tablet) to confirm it works on any browser

### Materials Preparation (Day Before)
- [ ] 8 CSV dataset files distributed to each group — email or shared drive (in `datasets/` folder)
- [ ] Clinical Reference Sheet printed or sent digitally to all students
- [ ] Data Quality Assessment Worksheets printed (1 per student or per group)
- [ ] Interoperability Challenge Logs printed (1 per group)
- [ ] Instructor Answer Key reviewed (do NOT distribute to students)
- [ ] Phase 3B slides prepared mapping student experience to real standards
- [ ] Groups assigned in advance or randomization method prepared

### Day of Class — Before Students Arrive
- [ ] **Reboot the app** to reset the database: share.streamlit.io → find app → ⋮ → Reboot app
- [ ] Confirm the app loads and the Dashboard shows 0 records
- [ ] Write the URL on the board: **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**
- [ ] Open the Dashboard tab on your projected screen — leave it visible throughout Phase 2
- [ ] Brief students: clinical knowledge is NOT required — they are acting as data/IT professionals

### Optional Enhancements
- [ ] Prepare FHIR demonstration: Patient + Observation resources on HAPI test server
- [ ] Prepare patient safety trigger briefing for Phase 2 (anti-Kell scenario)
- [ ] Assign observer/regulator roles (ARS observers)
- [ ] Designate one student as "Marie" with a paper health folder (patient-mediated exchange scenario)

---

## Assessment Options

**Formative (during exercise):**
- Observation of group collaboration and problem-solving approaches
- Quality of completed worksheets and logs
- Participation in debrief discussion

**Summative (post-exercise):**
- Individual reflection paper (1-2 pages): "Based on this exercise, what are the three most important requirements for a national health information exchange system?"
- Group report: Propose an interoperability architecture for the maternity care pathway, identifying standards, governance, and technical requirements
- Quiz on interoperability concepts, standards, and French digital health infrastructure (Segur du Numerique, CI-SIS, DMP, MSSante, INS)
