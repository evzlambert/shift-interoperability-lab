# Interoperability Challenge Log

## Phase 2 — Data Exchange (45 minutes)

**Group:** _______________________________________________

**Group Members:** _______________________________________________

**Date:** _______________________________________________

---

## Your Task

This log has two purposes:

**Part A — Submission obstacles (during the first ~30 minutes)**
Every time something goes wrong when you try to INSERT data into the HIE, stop and log it here before you fix it. The errors are the lesson — do not skip past them.

**Part B — Query discoveries (during the last ~15 minutes)**
When the class runs the shared queries together, record anything surprising or broken that you see in the results. These are interoperability failures visible only because everyone's data is now in the same database.

---

## Entry Types

| Type | When to use it |
|------|---------------|
| **Submission obstacle** | Something prevented or complicated your INSERT statement — a SQL error, a value you had to convert, a field that didn't exist in the schema, data you had to leave as NULL |
| **Query discovery** | Something surprising or broken found when querying all groups' data together — the same patient registered multiple ways, missing records, conflicting values, fields that can't be compared across groups |

---

## Completed Examples

*These rows show what well-completed entries look like.*

| # | Type | Your Group | Data Element | What Happened | Was It Resolved? | How / What Would Fix It? |
|---|------|-----------|-------------|---------------|-----------------|--------------------------|
| *ex* | *Submission obstacle* | *Group 1 — Midwife Practice* | *weight_kg* | *Source data had "68,5" (French comma decimal). INSERT failed with a datatype mismatch because the HIE field expects a number, not text. Had to change to "68.5" before INSERT would succeed.* | *Yes* | *Manually replaced comma with period. Real system fix: configure source EHR to export decimals in ISO format, or add a transformation rule at the HIE ingestion layer.* |
| *ex* | *Query discovery* | *All groups* | *patients.last_name* | *Running SELECT \* FROM patients showed Marie Dupont registered 6 times with slight variations: DUPONT, Dupont, DU PONT, DUPOND. None of the records had a shared unique identifier to confirm they are the same person.* | *No* | *Requires a Master Patient Index (MPI) with probabilistic matching, or a national unique health ID (INS) that all systems are required to record.* |

---

## Your Log

| # | Type | Your Group | Data Element | What Happened | Was It Resolved? | How / What Would Fix It? |
|---|------|-----------|-------------|---------------|-----------------|--------------------------|
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

## Part B — Shared Query Results

Record what you observe when the class runs the 6 shared queries together. You do not need to write out the full results — just note what surprised you or what seems like a problem.

**Query 1 — How many times does Marie Dupont appear?**

Result / Observation: _______________________________________________

_______________________________________________

**Query 2 — Which groups submitted data for each table?**

Result / Observation: _______________________________________________

_______________________________________________

**Query 3 — What date formats are present in the database?**

Result / Observation: _______________________________________________

_______________________________________________

**Query 4 — Are there any patients linked to another patient (mother-baby)?**

Result / Observation: _______________________________________________

_______________________________________________

**Query 5 — What lab test names were submitted, and are they consistent across groups?**

Result / Observation: _______________________________________________

_______________________________________________

**Query 6 — Are there any duplicate or suspicious insurance claims?**

Result / Observation: _______________________________________________

_______________________________________________

---

## Summary

**How many total obstacles did your group hit during submission?** _______________

**How many were resolved during the session?** _______________

**In one sentence: what was the single biggest interoperability barrier your group encountered?**

&nbsp;

&nbsp;

&nbsp;

---

*Deliverable: Bring this completed log to Phase 3. You will use it as evidence during the Standards Working Group discussion.*
