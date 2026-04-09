# HIE Interoperability Lab — Instructor Guide

## SHIFT Program - France

---

## The HIE App

The **HIE (Health Information Exchange) Streamlit App** is a cloud-hosted web tool that simulates a shared regional health information exchange platform. All 8 student groups connect to the same shared database automatically — no installation required for anyone.

**App URL:** **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**

**GitHub repo:** https://github.com/evzlambert/shift-interoperability-lab

### App Tabs Overview

| Tab | Used By | Purpose |
|-----|---------|---------|
| **Insert Data** | Students | Write SQL INSERT statements to submit data to the HIE |
| **Query Data** | Students | Run SELECT queries to explore all groups' data |
| **Dashboard** | Instructor + Students | Real-time submission progress across all 8 groups |
| **FHIR Explorer** | Phase 3 | Shows submitted data as HL7 FHIR R4 resources |
| **Export (Assessment)** | Instructor | Per-group scorecard, automated feedback, Excel download |

---

## Before Class: Setup

The app is already deployed. There is nothing to install.

### Day Before Class

1. Open **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/** and confirm it loads
2. Sign in to **https://share.streamlit.io** with GitHub account (evzlambert) and locate the app — find the ⋮ menu and confirm you can see the **Reboot app** option

### Day of Class — Before Students Arrive

1. **Reboot the app** to reset the database to empty:
   - Go to https://share.streamlit.io
   - Find `shift-interoperability-lab`
   - Click the **⋮ (three dots)** menu
   - Click **"Reboot app"**
   - Wait about 30 seconds, then refresh the app URL — the Dashboard should show 0 records

2. **Confirm the app is clean** — open the Dashboard tab and verify all record counts are 0

3. **Write the URL on the board or first slide:**
   > **https://shift-interoperability-lab-eksxqkfwaeq2pvmxwjay5h.streamlit.app/**

4. **Project the Dashboard tab** on the classroom screen — leave it visible throughout Phase 2

> **Why reboot?** The database persists between sessions on the same container. Rebooting resets the filesystem so each class starts fresh. Do this immediately before class, not hours before, as the app may hibernate and auto-reset anyway.

---

## Preparation Checklist

### App
- [ ] Confirm app loads at the URL above (day before)
- [ ] Sign in to share.streamlit.io and locate the Reboot option (day before)
- [ ] Reboot app just before class — confirm Dashboard shows 0 records
- [ ] URL written on board or slide

### Materials
- [ ] 8 CSV dataset files distributed to each group (from `datasets/` folder) — email or shared drive
- [ ] `Clinical_Reference_Sheet.docx` printed or sent digitally to all students
- [ ] `Assignment-Instructions.docx` distributed to all students
- [ ] `Student_Guide.docx` distributed to all students
- [ ] Data Quality Assessment Worksheets printed (1 per student or per group)
- [ ] Interoperability Challenge Logs printed (1 per group)
- [ ] Instructor Answer Key reviewed — **do NOT distribute to students**
- [ ] Phase 3B slides prepared (real-world standards mapping)
- [ ] Optional: FHIR demonstration prepared using HAPI test server (http://hapi.fhir.org/)

---

## Facilitation by Phase

### Phase 1 — Data Discovery (45 min)
- Students work only with their CSV files — the app is not yet in use
- Walk around and confirm each group can open their CSV correctly (delimiter issues are common)
- Remind students the Clinical Reference Sheet explains medical terms
- In the last 5 minutes, ask students to open the app and browse the schema in the sidebar — this helps them anticipate what transformations they'll need before Phase 2

### Phase 2 — Data Exchange (45 min)
The app is central to this phase. Students spend ~30 min submitting data, then ~15 min querying.

**During submission (30 min):**
- Remind students of the URL if needed
- Watch the **Dashboard** tab (projected) — the real-time counter builds energy and shows which groups are behind
- Expect SQL errors — these are pedagogically intentional. They surface ETL challenges. Encourage groups to document every error in their Interoperability Challenge Log rather than just fixing and moving on
- Common instructor interventions:
  - "What does that error message tell you about the incompatibility?"
  - "How would a real HIE need to handle this automatically?"

**During shared queries (15 min):**
- Lead the class through the 6 discovery queries in the Assignment Instructions (run them on the projected screen)
- Prompt discussion at each result — especially the duplicate patient query and the baby linkage query
- The incomplete Dashboard pivot (some groups submitted more than others) is itself a discussion point about uneven adoption of interoperability standards

### Phase 3 — Standards Workshop (45 min)
- After the standards committee discussion (Part A), direct students to the **FHIR Explorer** tab
- Walk through one Patient resource on the projector: show the `identifier` array, the `link` field on the baby record, and the side-by-side HIE vs FHIR view
- Switch to an Observation and point out the LOINC code — contrast with how test names were handled in students' raw CSVs

### Phase 4 — Debrief (45 min)
- Leave the Dashboard projected — the incomplete submission picture is a concrete artifact of interoperability failure
- Use the three reflection lenses from the Assignment Instructions: technical/organizational challenges → executive impact → patient safety and cost

---

## Assessment: Exporting Student Work

### During Class
The **Export (Assessment)** tab provides:
- **Class Scorecard** — record counts per group per table, with flags for missing required submissions
- **Per-Group Detailed Review** — expandable view of each group's submitted data with automated feedback on common errors (date formats, unit conversions, mother-baby linkage, truncated test names, duplicate claims, etc.)

### End of Class — Download Before Students Leave
The database resets when the app restarts. Download the data before class ends.

1. Go to the **Export (Assessment)** tab
2. Click **"Generate Excel Workbook"**
3. Click **"⬇ Download All Data (Excel)"**
4. Save the file — it contains a Summary sheet plus one sheet per table with all groups' data

You can also download a per-group CSV by selecting a group in the detailed review section.

---

## Automated Assessment Feedback Reference

The Export tab checks the following automatically:

| Check | Group(s) | What to Look For |
|-------|---------|-----------------|
| Date format (YYYY-MM-DD) | All | Any dates not matching the required format |
| Baby submitted as separate patient | 6, 7 | Baby Louise (DOB 2026-01-28) should appear as own row |
| Mother-baby linkage | 6, 7 | `related_patient_id` should be populated on baby's record |
| Confusable patient DUPOND excluded | 4 | DUPOND (born 16/03/1993) should NOT be in the database |
| Blood pressure converted | 1 | `systolic_bp` should be non-null |
| Baby weight in kg (not grams) | 7 | Values > 100 flagged as likely still in grams |
| Anti-Kell test name not truncated | 2 | Test names ending in "(Ir" flagged |
| Glucose units consistent (mmol/L) | 2 | Mixed g/L and mmol/L flagged |
| Corrected result flagged | 2 | `is_corrected = 1` expected on at least one lab result |
| Methyldopa discrepancy documented | 4, 6 | `notes` field on Methyldopa record should be non-empty |
| Duplicate claim flagged | 8 | At least one claim with `claim_status = 'Duplicate'` expected |
| Reimbursement rate as decimal | 8 | Values > 1.0 flagged as likely still in percentage format |

---

## Grading Notes

The Export tab captures **what** students submitted, but grading depth comes from reading:
- The `notes` fields in submitted records — did students document discrepancies, transformations, and data quality issues they found?
- The Interoperability Challenge Logs (paper) — did students correctly identify the challenges and articulate what would fix them?
- The Phase 4 reflection paper — can students connect the data problems to real-world consequences?

---

*Do not distribute this document to students.*
*Instructor Answer Key is in `INSTRUCTOR_ANSWER_KEY.docx`.*
