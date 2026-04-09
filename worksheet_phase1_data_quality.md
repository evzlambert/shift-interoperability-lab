# Data Quality Assessment Worksheet

## Phase 1 — Data Discovery (45 minutes)

**Group:** _______________________________________________

**Group Members:** _______________________________________________

**Date:** _______________________________________________

---

## Your Task

You have received a CSV file containing your group's healthcare dataset. Your job is to examine it carefully and document every data quality problem you find. You will use this worksheet during Phase 1 and refer back to it during Phase 2 when you try to load the data into the shared HIE database.

**Open your CSV file in Excel or Google Sheets.** Read every column and every row. Look for anything that seems wrong, inconsistent, missing, or hard to interpret.

---

## Reference: Issue Types

Use these abbreviations in the Issue Type column:

| Code | Type | What it means |
|------|------|---------------|
| **FI** | Format Inconsistency | Same field recorded in different formats (e.g., dates as DD/MM/YYYY in some rows and YYYY-MM-DD in others) |
| **MD** | Missing Data | A field that should have a value is blank or null |
| **TR** | Truncation | A value has been cut off and is incomplete (e.g., a test name that ends mid-word) |
| **EE** | Encoding Error | A character appears garbled or wrong (e.g., accented letters like é showing as strange symbols) |
| **TM** | Type Mismatch | A field contains the wrong kind of data (e.g., a number field contains text like "N/A") |
| **DU** | Duplicate | The same record or patient appears more than once |
| **AC** | Ambiguous Coding | A code or value that could mean more than one thing, or uses a non-standard system |
| **OT** | Other | Any issue that does not fit the above categories |

---

## Reference: Severity Scale

| Level | Label | What it means |
|-------|-------|---------------|
| **1** | Minor | Cosmetic issue — does not affect meaning or care decisions |
| **2** | Moderate | Requires a manual fix before the data can safely be shared |
| **3** | Critical | Could cause a clinical error if shared without correction |

---

## Completed Example

*This row shows what a well-completed entry looks like.*

| # | Field Name | Issue Description | Issue Type | Severity (1–3) | Patient Safety Impact? | Proposed Fix |
|---|------------|-------------------|------------|----------------|----------------------|-------------|
| *ex* | *blood_pressure* | *Recorded as "11/7" (French shorthand) instead of separate systolic and diastolic values. The HIE requires two numeric fields: systolic_bp and diastolic_bp.* | *FI* | *2* | *Yes — "11/7" could be misread as 11 mmHg systolic, which is incompatible with life. The correct value is 110/70 mmHg.* | *Split into two fields: systolic_bp = 110, diastolic_bp = 70. Multiply French shorthand by 10.* |

---

## Your Worksheet

| # | Field Name | Issue Description | Issue Type | Severity (1–3) | Patient Safety Impact? | Proposed Fix |
|---|------------|-------------------|------------|----------------|----------------------|-------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |
| 8 | | | | | | |
| 9 | | | | | | |
| 10 | | | | | | |

*Add rows as needed.*

---

## Summary Questions

Answer these before moving to Phase 2.

**1. How many issues did you find in total?**

&nbsp;

**2. How many were Severity 3 (Critical)?**

&nbsp;

**3. Which single issue worries you most about sharing this data with other groups? Why?**

&nbsp;

&nbsp;

&nbsp;

**4. Before you can submit this data to the HIE, which fields will definitely require transformation (not just cleaning, but actually restructuring or reformatting)?**

&nbsp;

&nbsp;

&nbsp;

---

*Deliverable: Hand in this completed worksheet at the end of Phase 1, or bring it with you to Phase 2.*
