# HIE Streamlit App — Complete Guide for Instructors and Students

## SHIFT Program - France | Interoperability Lab

---

## What Is the HIE App?

The **HIE (Health Information Exchange) Streamlit App** is a web-based tool built specifically for this lab. It replaces any need to download or install DB Browser for SQLite. Students and instructors access it directly in a web browser.

The app simulates a **shared regional health information exchange platform** — the integration target where all 8 groups must submit their patient data. It runs locally on the instructor's laptop and students access it over the classroom WiFi network.

**The app has four tabs:**

| Tab | Purpose |
|-----|---------|
| **Insert Data** | Write SQL INSERT statements to load your data into the HIE |
| **Query Data** | Run SELECT queries to explore the shared HIE database |
| **Dashboard** | Real-time view of how many records each group has submitted |
| **FHIR Explorer** | See the submitted data transformed into HL7 FHIR R4 resources |

---

---

# PART 1: INSTRUCTOR GUIDE

---

## Before Class: One-Time Setup

### Step 1: Verify Python Is Installed

Open a terminal and check:

```bash
python3 --version
```

You need Python 3.8 or higher. If not installed, download from https://www.python.org/downloads/

### Step 2: Install Required Packages

From the `SHIFT-Interoperability-Lab` folder, run:

```bash
pip install streamlit pandas
```

Or if pip3 is your default:

```bash
pip3 install streamlit pandas
```

You only need to do this once.

### Step 3: Test the App Before Class

From the `SHIFT-Interoperability-Lab` folder, run:

```bash
streamlit run hie_app.py
```

The app should open automatically in your browser at **http://localhost:8501**

You will see:
- The title "Regional Health Information Exchange (HIE)"
- Four tabs: Insert Data, Query Data, Dashboard, FHIR Explorer
- A sidebar with "Your Group" selector and schema reference

The first time it runs, the app automatically creates the `hie_shared.db` database file in the same folder. You do **not** need to create this file manually.

### Step 4: Prepare Student Access

Students access the app over the classroom WiFi. To get the shareable URL:

1. Start the app with:
   ```bash
   streamlit run hie_app.py --server.address 0.0.0.0
   ```

2. Find your laptop's local IP address:
   - **macOS:** `System Preferences → Network` or run `ipconfig getifaddr en0` in terminal
   - **Windows:** Run `ipconfig` in command prompt, look for "IPv4 Address"
   - Example: `192.168.1.45`

3. Give students the URL: **`http://192.168.1.45:8501`**

> **Important:** Your laptop and all student devices must be on the **same WiFi network**. If the classroom has a guest/restricted network, check that device-to-device connections are allowed. If not, use your laptop as a hotspot.

### Step 5: Distribute Student Materials

Before class, make sure each group has:
- [ ] Their group's CSV file (from the `datasets/` folder)
- [ ] A printed or digital copy of the Clinical Reference Sheet
- [ ] A printed Data Quality Assessment Worksheet
- [ ] A printed Interoperability Challenge Log
- [ ] The URL of the Streamlit app

---

## Resetting the Database

### Between runs of the same class session:
The `hie_shared.db` file stores all inserted data. To wipe it and start fresh:

1. Stop the app (Ctrl+C in terminal)
2. Delete the `hie_shared.db` file (and `hie_shared.db-shm` and `hie_shared.db-wal` if present)
3. Restart: `streamlit run hie_app.py`

The app recreates the database automatically on startup.

### Between different class sections:
Delete `hie_shared.db` as above before each new class session so groups start with a clean slate.

---

## Monitoring During the Exercise

### Dashboard Tab
The **Dashboard** tab gives you a live view of the exercise:
- **Total records in HIE** — overall progress counter
- **Records per table** — shows which tables have data
- **Submissions by group** — pivot table showing exactly which groups have submitted what
- **Marie Dupont's Care Timeline** — auto-generated timeline of submitted encounters

Click **Refresh Dashboard** to update the view. This is useful to project on the classroom screen so students can see the whole class's progress in real time.

### Instructor Tips by Phase

**Phase 1 (Data Discovery, 45 min):**
- Students are only working with their own CSV files at this point — the app is not yet in use
- Walk around and confirm each group can open their CSV and read their column headers
- Remind them to use the Clinical Reference Sheet for medical terminology

**Phase 2 (Data Exchange, 45 min):**
- This is when groups start using the app
- Direct students to the app URL
- Watch the Dashboard tab and project it on screen — the real-time counter creates energy
- Expect errors! SQL errors are pedagogically intentional — they surface the ETL challenges
- Group 6 (Hospital) and Group 8 (Insurance) should be submitting data from multiple sources, so watch for foreign key and patient matching issues

**Phase 3 (Standards Workshop, 45 min):**
- After the standards committee discussion, invite students to use the **FHIR Explorer** tab
- Walk through one FHIR Patient resource live on the projector — map it to Marie Dupont's submitted data
- Point out the LOINC codes on observations, the INS system OID, the RelatedPerson linkage

**Phase 4 (Debrief, 45 min):**
- Leave the Dashboard projected — the incomplete pivot (some groups submitted, some didn't, some had errors) is itself a teaching moment about interoperability failure

---

## Instructor Preparation Checklist

- [ ] Python 3.8+ installed on teaching laptop
- [ ] `streamlit` and `pandas` installed (`pip install streamlit pandas`)
- [ ] App tested — `streamlit run hie_app.py` opens without errors
- [ ] Local IP address noted for sharing URL with students
- [ ] `hie_shared.db` deleted/reset from any previous test runs
- [ ] App restarted clean so database is empty on class day
- [ ] Student devices can reach `http://[your-ip]:8501` on classroom WiFi (test this!)
- [ ] CSV datasets in `datasets/` folder confirmed present (8 files)
- [ ] Clinical Reference Sheets distributed or printed
- [ ] Data Quality Assessment Worksheets printed (1 per student or per group)
- [ ] Interoperability Challenge Logs printed (1 per group)
- [ ] Instructor Answer Key reviewed (do NOT distribute to students)
- [ ] Phase 3B slides prepared (real-world standards mapping)
- [ ] Optional: prepared FHIR demonstration on HAPI test server

---

---

# PART 2: STUDENT GUIDE

---

## Background: What You Need to Know Before You Start

This section explains a few technical concepts in plain language. If you already know what a CSV file and SQL are, skip ahead to Getting Started.

---

### What is a CSV file?

A **CSV (Comma-Separated Values)** file is a plain-text spreadsheet. Each row is one record. Each column is separated by a delimiter character — usually a comma (`,`) but sometimes a semicolon (`;`).

You can open a CSV file in Excel or Google Sheets. If the columns look scrambled when you open it, it usually means you need to tell the program which delimiter the file uses.

**How to open a CSV correctly in Excel:**
1. Do not double-click the file — instead open Excel first, then go to **Data → From Text/CSV**
2. Select your file
3. Excel will show a preview. Look for a "Delimiter" dropdown — change it to **Semicolon** if your columns are scrambled (Groups 1, 2, and 4 use semicolons; all others use commas)
4. Click **Load**

**How to open a CSV correctly in Google Sheets:**
1. Go to File → Import → Upload your CSV file
2. Under "Separator type" choose **Custom** and type `;` if needed
3. Click **Import data**

---

### What is a database?

A **database** stores information in organized tables — like a very structured spreadsheet. Each table has named columns, and each row is one record.

The HIE app uses a database called **SQLite**, which runs entirely on your laptop — there is nothing to install or log into. When you open the app, the database is already running in the background.

The HIE database has 7 tables: `patients`, `encounters`, `vitals`, `lab_results`, `medications`, `imaging`, and `claims`. Each table stores a different type of healthcare data. Your job is to move data from your group's CSV file into the appropriate tables.

---

### What is SQL?

**SQL (Structured Query Language)** is the language used to talk to a database. You only need to know two types of SQL statements for this exercise:

**INSERT** — adds a new row to a table:
```sql
INSERT INTO patients (last_name, first_name, date_of_birth, source_system)
VALUES ('DUPONT', 'Marie', '1993-03-15', 'Group 1 - Midwife Practice');
```
Read this as: *"Put a new row into the patients table. The last_name is DUPONT, the first_name is Marie, the date_of_birth is 1993-03-15, and the source_system is Group 1 - Midwife Practice."*

**SELECT** — retrieves rows from a table:
```sql
SELECT * FROM patients;
```
Read this as: *"Show me everything in the patients table."*

**You do not need programming experience to write these.** The app gives you a template to start from, and the group-specific examples in this guide show you exactly what to write for your data. Your main job is to look at your CSV, compare it to the HIE schema, and figure out how to translate each value.

**Important rules for SQL text:**
- Text values must be wrapped in single quotes: `'DUPONT'` ✓
- Numbers must NOT have quotes: `68.5` ✓ not `'68.5'` ✗
- Dates must be in YYYY-MM-DD format: `'1993-03-15'` ✓ not `'15/03/1993'` ✗
- If a field is blank or unknown, use: `NULL` (no quotes)

---

### What is the HIE?

**HIE stands for Health Information Exchange** — a shared platform where multiple healthcare organizations submit patient data so that providers across the system can see a complete picture of a patient's care.

In this exercise, the Streamlit app simulates an HIE. Each of your 8 groups represents a different healthcare organization. The HIE is the place where all your data is supposed to come together. The challenge — which you will experience directly — is that each organization stores data differently, and getting it all into a shared format is harder than it sounds.

---

## Getting Started

### Step 1: Open the App

Open a web browser and go to the URL your instructor gives you. It will look like:

```
http://192.168.1.XX:8501
```

You should see the **Regional Health Information Exchange (HIE)** app.

### Step 2: Select Your Group

In the **left sidebar**, click the dropdown under "Your Group" and select your group. For example:
- Group 1 - Midwife Practice
- Group 2 - Laboratory
- etc.

This tells the app who you are. Your group name will be automatically inserted into INSERT templates as the `source_system` value — this is how the HIE tracks which records came from which system.

The sidebar also shows:
- **Your Target Tables** — the specific HIE tables you need to populate
- **Quick Schema Reference** — the exact column names and data types for any table

---

## What You Are Doing

You are acting as the **data integration team** for your healthcare setting. Your job is to take the messy, imperfect data from your group's CSV file and insert it into the **shared HIE database** using SQL INSERT statements.

The HIE database has a standardized schema — clean field names, consistent date formats, numeric-only fields for numbers. Your source data does NOT match this schema directly. That's the point: you will encounter real ETL (Extract, Transform, Load) challenges as you reconcile your data to the HIE format.

---

## The Four App Tabs

### Tab 1: Insert Data

This is where you write SQL INSERT statements to load your data into the HIE.

**How to use it:**
1. Look at your CSV dataset and identify the patient, encounter, and clinical data
2. Look at the HIE schema in the sidebar for the table you want to populate
3. Write an INSERT statement (see examples below for your group)
4. Click **Execute**
5. If successful: a green banner shows the new row ID — **write this ID down!** You'll need it for subsequent inserts (e.g., the `patient_id` when inserting an encounter)
6. If there's an error: a red banner shows the SQL error message, plus a helpful hint about the likely cause

**Critical rule — insert in order:**
Always insert the **patient first**, then encounters, then clinical data. This is because encounters reference a `patient_id`, and labs/vitals/medications reference both a `patient_id` and an `encounter_id`. If you try to insert an encounter before the patient exists, you'll get a foreign key error.

**Order of inserts:**
```
1. patients       ← always first
2. encounters     ← references patient_id
3. vitals         ← references patient_id + encounter_id
4. lab_results    ← references patient_id + encounter_id
5. medications    ← references patient_id + encounter_id
6. imaging        ← references patient_id + encounter_id
7. claims         ← references patient_id + encounter_id
```

---

### Tab 2: Query Data

Run SELECT statements to explore the shared HIE database.

**Quick query buttons** at the top give you instant results:
- **All patients** — see every patient record submitted so far
- **All encounters** — timeline of all encounters by date
- **My group's data** — count of records your group has submitted per table
- **Duplicate patients** — find cases where the same patient appears to have been registered multiple times

You can also write your own queries in the text box. Examples:

```sql
-- Find all of Marie Dupont's data
SELECT * FROM patients WHERE UPPER(last_name) = 'DUPONT';

-- See all lab results submitted
SELECT patient_id, test_name, result_value, unit, source_system FROM lab_results;

-- Compare medication data from different systems
SELECT m.medication_name, m.dose, m.source_system
FROM medications m
JOIN patients p ON m.patient_id = p.patient_id
WHERE UPPER(p.last_name) = 'DUPONT';
```

---

### Tab 3: Dashboard

Shows a live summary of all submitted data:
- Total records in the HIE
- Records per table
- A group-by-table pivot showing which groups have submitted
- Marie Dupont's care timeline (auto-built from submitted encounters)

Click **Refresh Dashboard** to update.

---

### Tab 4: FHIR Explorer

After data is submitted, this tab shows what the same data looks like as **HL7 FHIR R4** resources — the modern international standard for exchanging health data.

Select a resource type (Patient, Encounter, Observation, MedicationRequest, Claim) and then select a specific record. The app shows:
- The FHIR JSON resource (with standardized coding systems like LOINC and SNOMED CT)
- A side-by-side comparison: HIE relational table row vs FHIR resource

Use this tab during Phase 3 of the exercise to connect your SQL experience to real-world standards.

---

## HIE Schema: What Fields Are Required

When writing INSERT statements, required fields (marked `NOT NULL`) must always be included. Optional fields can be omitted or set to `NULL`.

### patients table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| national_health_id | TEXT | Optional | INS number if known |
| last_name | TEXT | **Required** | |
| first_name | TEXT | **Required** | |
| date_of_birth | TEXT | **Required** | Format: YYYY-MM-DD |
| sex | TEXT | Optional | 'M' or 'F' |
| address | TEXT | Optional | |
| phone | TEXT | Optional | |
| insurance_number | TEXT | Optional | Carte Vitale / Sécurité Sociale number |
| related_patient_id | INTEGER | Optional | Used for mother-baby linkage (patient_id of the related person) |
| relationship_type | TEXT | Optional | 'mother' or 'child' |
| source_system | TEXT | **Required** | Your group name (auto-filled in template) |
| source_patient_id | TEXT | Optional | The ID used in your source system |

### encounters table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | Must match an existing patient_id |
| encounter_type | TEXT | **Required** | 'outpatient', 'inpatient', 'emergency', or 'home_visit' |
| facility_name | TEXT | Optional | |
| provider_name | TEXT | Optional | |
| encounter_date | TEXT | **Required** | Format: YYYY-MM-DD |
| encounter_time | TEXT | Optional | Format: HH:MM |
| chief_complaint | TEXT | Optional | |
| diagnosis_code | TEXT | Optional | ICD-10/CIM-10 code |
| diagnosis_text | TEXT | Optional | Human-readable diagnosis |
| procedure_code | TEXT | Optional | CCAM code |
| procedure_text | TEXT | Optional | |
| notes | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |
| source_encounter_id | TEXT | Optional | Original ID from your system |

### vitals table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | |
| encounter_id | INTEGER | Optional | Link to the encounter |
| measurement_date | TEXT | **Required** | YYYY-MM-DD |
| measurement_time | TEXT | Optional | HH:MM |
| systolic_bp | INTEGER | Optional | Must be a whole number in mmHg |
| diastolic_bp | INTEGER | Optional | Must be a whole number in mmHg |
| heart_rate | INTEGER | Optional | Beats per minute |
| spo2 | INTEGER | Optional | Percentage |
| temperature | REAL | Optional | Celsius |
| weight_kg | REAL | Optional | Must use dot decimal (e.g., 68.5 not 68,5) |
| notes | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |

### lab_results table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | |
| encounter_id | INTEGER | Optional | |
| test_date | TEXT | **Required** | YYYY-MM-DD |
| test_time | TEXT | Optional | HH:MM |
| test_code | TEXT | Optional | LOINC code if known |
| test_name | TEXT | **Required** | Full name — no truncation |
| result_value | REAL | Optional | Numeric result (use dot decimal) |
| result_text | TEXT | Optional | For non-numeric results (e.g., 'Positive') |
| unit | TEXT | Optional | |
| reference_low | REAL | Optional | |
| reference_high | REAL | Optional | |
| flag | TEXT | Optional | 'H', 'L', or 'N' |
| is_corrected | INTEGER | Optional | 1 if this corrects a previous result, 0 otherwise |
| notes | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |
| source_test_id | TEXT | Optional | Original test ID from your system |

### medications table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | |
| encounter_id | INTEGER | Optional | |
| medication_name | TEXT | **Required** | |
| dose | TEXT | Optional | e.g., '250mg' |
| route | TEXT | Optional | 'oral', 'IV', 'IM' |
| frequency | TEXT | Optional | e.g., 'twice daily' |
| start_date | TEXT | Optional | YYYY-MM-DD |
| end_date | TEXT | Optional | YYYY-MM-DD |
| prescriber | TEXT | Optional | |
| notes | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |

### imaging table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | |
| encounter_id | INTEGER | Optional | |
| exam_date | TEXT | **Required** | YYYY-MM-DD |
| exam_type | TEXT | **Required** | e.g., 'Obstetric Ultrasound' |
| findings_structured | TEXT | Optional | Key structured findings |
| report_text | TEXT | Optional | Narrative report |
| measurements | TEXT | Optional | |
| radiologist | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |
| source_exam_id | TEXT | Optional | Original exam ID |

### claims table

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| patient_id | INTEGER | **Required** | |
| encounter_id | INTEGER | Optional | |
| service_date | TEXT | **Required** | YYYY-MM-DD (use service date, not processing date) |
| processing_date | TEXT | Optional | YYYY-MM-DD |
| beneficiary_number | TEXT | Optional | |
| service_code | TEXT | Optional | Procedure/CCAM code |
| service_description | TEXT | Optional | |
| diagnosis_code | TEXT | Optional | |
| total_amount | REAL | Optional | Numeric, in EUR — use dot decimal (e.g., 124.50 not 124,50) |
| reimbursement_rate | REAL | Optional | As a decimal: 1.0 = 100%, 0.7 = 70% |
| amount_reimbursed | REAL | Optional | |
| patient_copay | REAL | Optional | |
| claim_status | TEXT | Optional | 'Paid', 'Pending', 'Rejected', or 'Duplicate' |
| notes | TEXT | Optional | |
| source_system | TEXT | **Required** | Your group name |
| source_claim_id | TEXT | Optional | Original claim ID from your system |

---

## Group-Specific Instructions

### GROUP 1 — Cabinet de Sage-Femme (Midwife Practice)

**Your target tables:** `patients`, `encounters`, `vitals`

**Your data challenges to solve before inserting:**
- Dates in your CSV are in DD/MM/YYYY or DD-MMM-YY format → convert to YYYY-MM-DD
- Blood pressure is recorded as French shorthand (e.g., "11/7") → convert to separate fields: systolic = 110, diastolic = 70
- Weight uses comma decimals ("68,5") → change to dot decimal: 68.5
- Some encoding errors in text fields (e.g., "decreas??d") → write correct text
- No patient national health ID → omit that field

**Example INSERT — patient:**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Marie', '1993-03-15', 'F',
    'Group 1 - Midwife Practice', 'DUPONT-Marie-1993'
);
```
*Write down the patient_id returned — you'll use it in every subsequent INSERT.*

**Example INSERT — encounter (prenatal visit):**
```sql
INSERT INTO encounters (
    patient_id, encounter_type, facility_name, provider_name,
    encounter_date, chief_complaint,
    source_system, source_encounter_id
) VALUES (
    1,                           -- replace with your actual patient_id
    'outpatient',
    'Cabinet Sage-Femme Leclerc',
    'Mme LECLERC',
    '2025-08-12',               -- converted from 12/08/2025
    'Prenatal visit week 12',
    'Group 1 - Midwife Practice', 'V001'
);
```

**Example INSERT — vitals (blood pressure + weight):**
```sql
INSERT INTO vitals (
    patient_id, encounter_id,
    measurement_date,
    systolic_bp, diastolic_bp,
    weight_kg,
    source_system
) VALUES (
    1,    -- your patient_id
    1,    -- your encounter_id
    '2025-08-12',
    110,  -- converted from "11/7" French shorthand
    70,
    68.5, -- converted from "68,5"
    'Group 1 - Midwife Practice'
);
```

**What to watch for:** Each row in your CSV is a separate visit. You will create one encounter and one vitals record per row. You only insert the patient ONCE.

---

### GROUP 2 — Laboratoire d'Analyses Médicales (Clinical Laboratory)

**Your target tables:** `patients`, `lab_results`

**Your data challenges to solve before inserting:**
- Some test names are truncated (e.g., "Antibody Screen (Ir" → should be "Antibody Screen (Irregular Antibody) - Anti-Kell")
- Glucose values mix units: some in g/L, some in mmol/L → convert all to mmol/L (multiply g/L × 5.55)
- Results stored as text strings ("5.2") → use the numeric `result_value` field (no quotes)
- One corrected result exists → set `is_corrected = 1` for the correction row
- Reference ranges formatted inconsistently → separate into `reference_low` and `reference_high`
- Flag field mixes French and English ("H", "L", "N", "Haut") → standardize to H/L/N

**Example INSERT — patient:**
```sql
INSERT INTO patients (
    national_health_id, last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    '293031593',
    'DUPONT', 'MARIE', '1993-03-15', 'F',
    'Group 2 - Laboratory', 'LAB-293031593'
);
```

**Example INSERT — lab result (glucose, converted to mmol/L):**
```sql
INSERT INTO lab_results (
    patient_id, test_date, test_time,
    test_name, result_value, unit,
    reference_low, reference_high, flag,
    source_system, source_test_id
) VALUES (
    2,           -- your patient_id
    '2025-10-15',
    '08:30',
    'Fasting Plasma Glucose',
    6.3,         -- converted: 1.14 g/L × 5.55 = 6.33 mmol/L
    'mmol/L',
    3.9, 5.5, 'H',
    'Group 2 - Laboratory', 'LAB-2025-44823'
);
```

**Example INSERT — corrected lab result:**
```sql
INSERT INTO lab_results (
    patient_id, test_date, test_name,
    result_value, unit, flag,
    is_corrected,
    notes,
    source_system, source_test_id
) VALUES (
    2,
    '2025-10-15',
    'Fasting Plasma Glucose (CORRECTED)',
    5.8, 'mmol/L', 'H',
    1,
    'Correction: pre-analytical error on original sample. This value supersedes previous result.',
    'Group 2 - Laboratory', 'LAB-2025-44823-CORR'
);
```

**Critical patient safety issue to discuss:** Your CSV has a truncated test name: `"Antibody Screen (Ir"`. The full name is `"Antibody Screen (Irregular Antibody) - Anti-Kell Positive"`. When you insert this into the HIE, use the **full name**. The truncation exists in your source system — but if the hospital group queries the HIE and only sees the truncated name, they cannot identify the anti-Kell antibody. This is a real patient safety risk.

---

### GROUP 3 — Centre d'Imagerie Médicale (Imaging Center)

**Your target tables:** `patients`, `encounters`, `imaging`

**Your data challenges to solve before inserting:**
- Exam dates in DICOM format (YYYYMMDD, e.g., "20250816") → convert to YYYY-MM-DD: "2025-08-16"
- Some reports are PDFs ("Report: [PDF - not machine readable]") → enter a note in `report_text` indicating the report is only available as a scanned document
- Patient name may be truncated in your system → use the full name from the patient story
- Measurements recorded with/without unit → standardize in the notes or `measurements` field
- Internal exam codes do not map to CCAM → leave `procedure_code` empty and explain in `notes`

**Example INSERT — patient:**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Marie', '1993-03-15', 'F',
    'Group 3 - Imaging Center', 'IMG-2025-DUPONT'
);
```

**Example INSERT — encounter + imaging study:**
```sql
-- Insert the encounter first
INSERT INTO encounters (
    patient_id, encounter_type, facility_name,
    encounter_date, procedure_text,
    source_system
) VALUES (
    3,  -- your patient_id
    'outpatient',
    'Centre Imagerie Beaumont',
    '2025-08-16',  -- converted from DICOM date 20250816
    'Obstetric Ultrasound - Dating/Morphology',
    'Group 3 - Imaging Center'
);

-- Then insert the imaging record
INSERT INTO imaging (
    patient_id, encounter_id,
    exam_date, exam_type,
    findings_structured,
    report_text,
    measurements,
    radiologist,
    source_system, source_exam_id
) VALUES (
    3,   -- your patient_id
    3,   -- your encounter_id (returned from previous INSERT)
    '2025-08-16',
    'Obstetric Ultrasound - 2nd Trimester',
    'Single fetus, cephalic presentation, normal morphology',
    'Ultrasound performed at 16 weeks gestation. Normal fetal anatomy. BPD 34mm, FL 22mm, AC 107mm. Placenta posterior, grade 0. AFI normal.',
    'BPD: 34mm, FL: 22mm, AC: 107mm',
    'Dr MARTIN',
    'Group 3 - Imaging Center', 'ECHO-2025-001'
);
```

---

### GROUP 4 — Clinique Obstétrique (Obstetric Clinic)

**Your target tables:** `patients`, `encounters`, `vitals`, `medications`

**Your data challenges to solve before inserting:**
- Patient identified by Carte Vitale number (different from INS) → use `insurance_number` field, not `national_health_id`
- Watch for the second patient: "DUPOND, Marie" (born 16/03/1993) — this is NOT Marie Dupont (born 15/03/1993). Do NOT insert this record.
- Duplicate visit entries from system migration → insert only once, note the duplicate in your Challenge Log
- Allergy field is inconsistent (free text vs coded) → standardize to free text in `notes`
- Medication dose discrepancy: some records say 250mg×2/day, others 250mg×3/day → document this discrepancy in `notes` on both records

**Example INSERT — patient:**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    insurance_number,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Marie', '1993-03-15', 'F',
    '2930315982057',   -- Carte Vitale number
    'Group 4 - Obstetric Clinic', 'CLIN-DUPONT-2025'
);
```

**Example INSERT — medication with dose discrepancy documented:**
```sql
INSERT INTO medications (
    patient_id, encounter_id,
    medication_name, dose, route, frequency,
    start_date,
    notes,
    source_system
) VALUES (
    4,   -- your patient_id
    4,   -- your encounter_id
    'Methyldopa',
    '250mg',
    'oral',
    'twice daily',
    '2025-11-15',
    'DISCREPANCY: Clinic record shows 250mg x2/day (500mg/day total). Patient self-reported 250mg x3/day (750mg/day). Discrepancy not resolved in source system.',
    'Group 4 - Obstetric Clinic'
);
```

---

### GROUP 5 — SAMU / Ambulance (Emergency Medical Services)

**Your target tables:** `patients`, `encounters`, `vitals`, `medications`

**Your data challenges to solve before inserting:**
- Patient name recorded phonetically as "Du Pont" → standardize to "DUPONT"
- Date missing on some timestamps (assumed current date at time of call) → use the correct encounter date from the clinical timeline (2026-01-28)
- Vital signs have inconsistent field names (TA, BP, tension) → all go to `systolic_bp`/`diastolic_bp`
- Glasgow Coma Scale in the wrong field type → put numeric value in `notes`
- Triage color code (local) → translate to encounter type: Red = emergency
- Handoff notes truncated mid-sentence → record what is available, note truncation

**Example INSERT — patient:**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    'DUPONT',    -- corrected from "Du Pont" phonetic error
    'Marie', '1993-03-15', 'F',
    'Group 5 - EMS Ambulance', 'SAMU-2026-0128-001'
);
```

**Example INSERT — emergency transport encounter:**
```sql
INSERT INTO encounters (
    patient_id, encounter_type,
    facility_name, provider_name,
    encounter_date, encounter_time,
    chief_complaint,
    diagnosis_code, diagnosis_text,
    notes,
    source_system, source_encounter_id
) VALUES (
    5,   -- your patient_id
    'emergency',
    'SAMU Mobile Unit → Hôpital Beaumont',
    'Dr ROSSETTI',
    '2026-01-28',
    '15:10',
    'Severe headache, visual disturbances, 38 weeks pregnant',
    'O14.1', 'Severe preeclampsia',
    'Patient transported from home. Handoff notes truncated: "Patiente G2P1 38 SA, TA 185/115, céphalées intenses, phosphènes depuis 2h. Glycémie non..." [truncated at 200 char limit]. GCS: 15.',
    'Group 5 - EMS Ambulance', 'SAMU-INT-2026-0128'
);
```

---

### GROUP 6 — Hôpital - Service Maternité (Hospital Maternity Ward)

**Your target tables:** `patients`, `encounters`, `vitals`, `lab_results`, `medications`

**Your dataset is the most complex.** It contains:
- Mother's records AND baby's records (two separate patients in the HIE)
- Mixed record types (ADT, LAB, MED, PROC, BIRTH, VITALS)
- Baby's name changes from "BG DUPONT" to "Louise DUPONT"
- HL7v2 message fragments (these are metadata — you do not insert them as-is)

**Strategy:**
1. First insert the **mother** as a patient
2. Then insert the **baby** as a separate patient
3. Link baby to mother using `related_patient_id` (the mother's patient_id) and `relationship_type = 'child'`
4. Insert encounters and clinical records for each patient separately

**Example INSERT — mother patient:**
```sql
INSERT INTO patients (
    national_health_id, last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    '293031593',
    'DUPONT', 'Marie', '1993-03-15', 'F',
    'Group 6 - Hospital Maternity', 'IPP-2026-88431'
);
```
*Note the returned patient_id — assume it's 6 in this example.*

**Example INSERT — baby patient (linked to mother):**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    related_patient_id, relationship_type,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Louise',
    '2026-01-28',   -- birth date
    'F',
    6,              -- mother's patient_id
    'child',
    'Group 6 - Hospital Maternity', 'NNE-2026-88431-01'
);
```

**Example INSERT — hospital admission encounter (mother):**
```sql
INSERT INTO encounters (
    patient_id, encounter_type,
    facility_name, provider_name,
    encounter_date, encounter_time,
    admission_date, discharge_date,
    chief_complaint,
    diagnosis_code, diagnosis_text,
    source_system, source_encounter_id
) VALUES (
    6,   -- mother's patient_id
    'inpatient',
    'Hôpital Beaumont - Maternité L3',
    'Dr LAURENT',
    '2026-01-28',
    '15:25',
    '2026-01-28', '2026-01-31',
    'Emergency admission: severe preeclampsia at 38 weeks',
    'O14.1', 'Severe preeclampsia',
    'Group 6 - Hospital Maternity', 'ADT-2026-88431'
);
```

**Example INSERT — lab result filed under mother's name but for the baby:**
```sql
INSERT INTO lab_results (
    patient_id,      -- use BABY's patient_id, even though the order was placed under mother's name
    test_date, test_name,
    result_text,
    notes,
    source_system, source_test_id
) VALUES (
    7,   -- baby's patient_id
    '2026-01-29',
    'Newborn Blood Group and Rhesus',
    'A Positive',
    'WARNING: Lab order was placed under mother IPP-2026-88431 with note "for newborn". Result manually re-attributed to newborn NNE-2026-88431-01 (Louise DUPONT). Verify attribution before clinical use.',
    'Group 6 - Hospital Maternity', 'LAB-NB-001'
);
```

---

### GROUP 7 — PMI - Protection Maternelle et Infantile (Public Health/Postnatal)

**Your target tables:** `patients`, `encounters`, `vitals`

**Your data challenges to solve before inserting:**
- Baby identified as "Louise DUPONT" (the official name now) — but hospital may still show "BG DUPONT"
- No national health IDs for mother or baby → omit those fields
- Mother and baby measurements appear in the same rows → carefully separate which measurement belongs to whom
- Baby weight recorded in grams → convert to kg (divide by 1000: 3100g = 3.1 kg)
- Socioeconomic data fields present → these are GDPR-sensitive; do NOT insert them into the HIE; document the omission in your Challenge Log
- Vaccination codes use ATC format → record in `notes`, not as structured procedure codes

**Example INSERT — mother patient (checking for duplicate from other groups):**
```sql
-- Note: First run this query to check if Marie Dupont already exists:
-- SELECT * FROM patients WHERE last_name = 'DUPONT' AND date_of_birth = '1993-03-15';
-- If she exists, note her patient_id and use it; do not insert a duplicate.

INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Marie', '1993-03-15', 'F',
    'Group 7 - PMI Postnatal', 'PMI-DUPONT-MARIE-1993'
);
```

**Example INSERT — baby patient:**
```sql
INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Louise', '2026-01-28', 'F',
    'Group 7 - PMI Postnatal', 'PMI-DUPONT-MARIE-1993-BABY-F'  -- PMI uses mother name + baby DOB + sex
);
```

**Example INSERT — postnatal home visit encounter:**
```sql
INSERT INTO encounters (
    patient_id, encounter_type,
    facility_name, provider_name,
    encounter_date,
    chief_complaint,
    source_system
) VALUES (
    8,    -- mother's patient_id
    'home_visit',
    'PMI - Conseil Départemental',
    'Infirmière BEAUMONT',
    '2026-02-11',
    'Postnatal follow-up visit, week 40',
    'Group 7 - PMI Postnatal'
);
```

**Example INSERT — baby weight at postnatal visit (with unit conversion):**
```sql
INSERT INTO vitals (
    patient_id, encounter_id,
    measurement_date,
    weight_kg,
    notes,
    source_system
) VALUES (
    9,      -- baby Louise's patient_id
    10,     -- encounter_id for the postnatal visit
    '2026-02-11',
    3.1,    -- converted from 3100 grams ÷ 1000
    'Weight at PMI postnatal visit. Original value in source system: 3100g. Converted to kg for HIE compatibility.',
    'Group 7 - PMI Postnatal'
);
```

**GDPR note to document in your Challenge Log:**
> "The PMI dataset contains socioeconomic fields (housing situation, employment status, family support score). These fields are restricted under GDPR Article 9 (special category data). We have omitted these fields from the HIE submission. They remain in the PMI system under restricted access. The HIE does not have a consent mechanism to handle granular field-level consent for these data elements."

---

### GROUP 8 — Assurance Maladie / CPAM (Health Insurance / Payer)

**Your target tables:** `patients`, `claims`

**Your data challenges to solve before inserting:**
- Amount fields use comma decimals ("124,50 EUR") → convert to dot decimal numeric: 124.50
- Reimbursement rate stored as text "100%" → convert to decimal: 1.0 (100% = 1.0, 70% = 0.7)
- Baby initially filed under mother's beneficiary number → insert baby as separate patient using the mother's patient_id as `related_patient_id`
- Duplicate claims exist → identify them and set `claim_status = 'Duplicate'` for the duplicate
- Processing dates (when claim was received) ≠ service dates (when care was given) → use service dates for `service_date`, processing dates for `processing_date`
- Some claims rejected with system-specific error codes → record error code in `notes`

**Example INSERT — patient (checking for existing record first):**
```sql
-- Check if Marie Dupont exists from another group:
-- SELECT patient_id, last_name, first_name, source_system FROM patients WHERE last_name = 'DUPONT';
-- Use her patient_id if found. If not found, insert:

INSERT INTO patients (
    last_name, first_name, date_of_birth, sex,
    insurance_number,
    source_system, source_patient_id
) VALUES (
    'DUPONT', 'Marie', '1993-03-15', 'F',
    '293031593282',  -- beneficiary number from CPAM
    'Group 8 - Insurance Payer', 'CPAM-293031593282'
);
```

**Example INSERT — claim with corrected formatting:**
```sql
INSERT INTO claims (
    patient_id,
    service_date, processing_date,
    beneficiary_number,
    service_code, service_description,
    diagnosis_code,
    total_amount, reimbursement_rate,
    amount_reimbursed, patient_copay,
    claim_status,
    source_system, source_claim_id
) VALUES (
    8,   -- your patient_id
    '2025-10-20',   -- service date (when care was given)
    '2025-10-28',   -- processing date (when claim was received - 8 days later)
    '293031593282',
    'CCAM-JNQP002', 'Obstetric consultation - high risk pregnancy',
    'O24.4',
    45.00,   -- converted from "45,00 EUR"
    1.0,     -- converted from "100%" (maternity pathway: 100% reimbursed from month 6)
    45.00,
    0.00,
    'Paid',
    'Group 8 - Insurance Payer', 'CLM-2025-48827'
);
```

**Example INSERT — duplicate claim (marked as such):**
```sql
INSERT INTO claims (
    patient_id,
    service_date,
    service_description,
    total_amount,
    claim_status,
    notes,
    source_system, source_claim_id
) VALUES (
    8,
    '2026-02-11',
    'PMI postnatal home visit',
    0.00,
    'Duplicate',
    'Duplicate claim detected: same service date and provider as CLM-2026-50043. Original claim paid. This duplicate was rejected by CPAM with error code DUP-44.',
    'Group 8 - Insurance Payer', 'CLM-2026-50043-DUP'
);
```

---

## Common SQL Errors and How to Fix Them

| Error Message | What It Means | How to Fix |
|---------------|--------------|------------|
| `NOT NULL constraint failed: patients.last_name` | You omitted a required field | Check the schema — add the missing required column and value |
| `FOREIGN KEY constraint failed` | The `patient_id` or `encounter_id` you used does not exist | Use the Query tab to find your patient's actual `patient_id` first |
| `syntax error near ")"` | Trailing comma before the closing parenthesis | Remove the comma after the last value in your VALUES list |
| `no such column: [name]` | You used a column name that doesn't exist in the HIE schema | Check the schema in the sidebar — copy the exact column name |
| `datatype mismatch` | You're inserting text into a numeric field | Remove quotes from numeric values: use `68.5` not `'68.5'` |
| `Only INSERT statements are allowed` | You tried to run a SELECT in the Insert tab | Switch to the **Query Data** tab for SELECT statements |

---

## Tips for Writing INSERT Statements

1. **Copy the column list from the sidebar schema** — never guess column names
2. **TEXT values need single quotes:** `'DUPONT'` ✓ vs `DUPONT` ✗
3. **Numbers do NOT use quotes:** `68.5` ✓ vs `'68.5'` ✗
4. **Dates must be YYYY-MM-DD:** `'2026-01-28'` ✓ vs `'28/01/2026'` ✗
5. **NULL for optional empty fields:** `NULL` (no quotes)
6. **Semicolons at the end are optional** — the app handles both
7. **If a required field doesn't exist in your source data**, explain the absence in a `notes` field

---

## Phase 2 Activity: What Each Group Should Submit

All groups follow the same workflow: submit your own data to the HIE, document the obstacles you encounter, then the whole class queries the combined result together.

**Each group's minimum target and the key challenge they will hit:**

| Group | Minimum to Submit | Key Challenge to Discover |
|-------|-----------------|--------------------------|
| Group 1 | Patient + 3-4 prenatal encounters + vitals | Date format conversion, BP conversion from French shorthand (11/7 → 110/70) |
| Group 2 | Patient + 5-6 lab results | Truncated test names must be expanded; unit conversion (g/L → mmol/L); text-stored numbers must be unquoted |
| Group 3 | Patient + 2-3 imaging encounters + imaging records | DICOM date format (YYYYMMDD → YYYY-MM-DD); scanned PDFs cannot be stored as structured data |
| Group 4 | Patient + 2-3 clinic encounters + medications | Confusable second patient (DUPOND vs DUPONT) must be excluded; medication dose discrepancy must be documented |
| Group 5 | Patient + emergency transport encounter + vitals | Patient name phonetic error must be corrected; truncated handoff notes must be flagged as incomplete |
| Group 6 | Mother + baby as 2 separate linked patients + hospital encounters + lab results | Mother-baby linkage via `related_patient_id`; baby name change mid-dataset; lab result attributed to wrong patient |
| Group 7 | Mother + baby as 2 separate patients + postnatal encounter + vitals | Grams → kg conversion; GDPR-sensitive fields omitted and documented; baby name may conflict with Group 6's "BG DUPONT" |
| Group 8 | Patient + 4-6 claims | Comma decimals → dot decimals; "100%" text → 1.0 decimal; duplicate claim identified and flagged |

**After all groups have submitted**, run the shared queries below as a class to see what the combined data reveals.

---

## After All Groups Have Submitted: Verification Queries

Run these queries in the **Query Data** tab to verify the class exercise and facilitate debrief:

```sql
-- How many records did each group submit?
SELECT source_system, COUNT(*) as records
FROM patients GROUP BY source_system
UNION ALL
SELECT source_system, COUNT(*) FROM encounters GROUP BY source_system;
```

```sql
-- How many different versions of "Marie Dupont" were registered?
SELECT patient_id, last_name, first_name, date_of_birth, national_health_id, source_system
FROM patients
WHERE UPPER(last_name) LIKE '%DUPONT%' OR UPPER(last_name) LIKE '%DU PONT%';
```

```sql
-- Did any group submit the confusable patient DUPOND instead of DUPONT?
SELECT * FROM patients WHERE UPPER(last_name) = 'DUPOND';
```

```sql
-- Show the full care timeline for Marie Dupont
SELECT e.encounter_date, e.encounter_time, e.encounter_type,
       e.facility_name, e.chief_complaint, e.diagnosis_text, e.source_system
FROM encounters e
JOIN patients p ON e.patient_id = p.patient_id
WHERE UPPER(p.last_name) = 'DUPONT' AND p.date_of_birth = '1993-03-15'
ORDER BY e.encounter_date, e.encounter_time;
```

```sql
-- Are baby Louise's records linked to her mother?
SELECT p.patient_id, p.last_name, p.first_name, p.date_of_birth,
       p.related_patient_id, p.relationship_type, p.source_system
FROM patients p
WHERE p.date_of_birth = '2026-01-28';
```

```sql
-- Find duplicate patient registrations (same name + DOB submitted by multiple groups)
SELECT last_name, first_name, date_of_birth, COUNT(*) as registrations
FROM patients
GROUP BY UPPER(last_name), UPPER(first_name), date_of_birth
HAVING COUNT(*) > 1;
```

```sql
-- Compare medication doses for Methyldopa across systems
SELECT m.medication_name, m.dose, m.frequency, m.notes, m.source_system
FROM medications m
JOIN patients p ON m.patient_id = p.patient_id
WHERE UPPER(m.medication_name) LIKE '%METHYLDOPA%';
```

```sql
-- Were lab results for the baby filed under the mother's patient ID?
SELECT lr.lab_id, lr.test_name, lr.result_text, lr.notes,
       p.last_name, p.first_name, p.date_of_birth
FROM lab_results lr
JOIN patients p ON lr.patient_id = p.patient_id
WHERE lr.source_system = 'Group 6 - Hospital Maternity';
```

```sql
-- Show all claims and check for duplicates
SELECT claim_id_hie, service_date, service_description,
       total_amount, claim_status, source_system
FROM claims ORDER BY service_date;
```

---

*This guide is part of the SHIFT Program - France Interoperability Lab materials.*
*Instructor Answer Key is in a separate document — do not distribute to students.*
