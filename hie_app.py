import streamlit as st
import sqlite3
import threading
import pandas as pd
import json
import os
import io
import re

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "hie_shared.db")

GROUPS = [
    "Group 1 - Midwife Practice",
    "Group 2 - Laboratory",
    "Group 3 - Imaging Center",
    "Group 4 - Obstetric Clinic",
    "Group 5 - EMS Ambulance",
    "Group 6 - Hospital Maternity",
    "Group 7 - PMI Postnatal",
    "Group 8 - Insurance Payer",
]

GROUP_TABLES = {
    "Group 1 - Midwife Practice": ["patients", "encounters", "vitals"],
    "Group 2 - Laboratory": ["patients", "lab_results"],
    "Group 3 - Imaging Center": ["patients", "encounters", "imaging"],
    "Group 4 - Obstetric Clinic": ["patients", "encounters", "vitals", "medications"],
    "Group 5 - EMS Ambulance": ["patients", "encounters", "vitals", "medications"],
    "Group 6 - Hospital Maternity": ["patients", "encounters", "vitals", "lab_results", "medications"],
    "Group 7 - PMI Postnatal": ["patients", "encounters", "vitals"],
    "Group 8 - Insurance Payer": ["patients", "claims"],
}

HIE_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    national_health_id  TEXT,
    last_name           TEXT NOT NULL,
    first_name          TEXT NOT NULL,
    date_of_birth       TEXT NOT NULL,
    sex                 TEXT,
    address             TEXT,
    phone               TEXT,
    insurance_number    TEXT,
    related_patient_id  INTEGER,
    relationship_type   TEXT,
    source_system       TEXT NOT NULL,
    source_patient_id   TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS encounters (
    encounter_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_type      TEXT NOT NULL,
    facility_name       TEXT,
    provider_name       TEXT,
    encounter_date      TEXT NOT NULL,
    encounter_time      TEXT,
    admission_date      TEXT,
    discharge_date      TEXT,
    chief_complaint     TEXT,
    diagnosis_code      TEXT,
    diagnosis_text      TEXT,
    procedure_code      TEXT,
    procedure_text      TEXT,
    notes               TEXT,
    source_system       TEXT NOT NULL,
    source_encounter_id TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
CREATE TABLE IF NOT EXISTS vitals (
    vital_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_id        INTEGER,
    measurement_date    TEXT NOT NULL,
    measurement_time    TEXT,
    systolic_bp         INTEGER,
    diastolic_bp        INTEGER,
    heart_rate          INTEGER,
    spo2                INTEGER,
    temperature         REAL,
    respiratory_rate    INTEGER,
    weight_kg           REAL,
    notes               TEXT,
    source_system       TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);
CREATE TABLE IF NOT EXISTS lab_results (
    lab_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_id        INTEGER,
    test_date           TEXT NOT NULL,
    test_time           TEXT,
    test_code           TEXT,
    test_name           TEXT NOT NULL,
    result_value        REAL,
    result_text         TEXT,
    unit                TEXT,
    reference_low       REAL,
    reference_high      REAL,
    flag                TEXT,
    is_corrected        INTEGER DEFAULT 0,
    notes               TEXT,
    source_system       TEXT NOT NULL,
    source_test_id      TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);
CREATE TABLE IF NOT EXISTS medications (
    medication_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_id        INTEGER,
    medication_name     TEXT NOT NULL,
    dose                TEXT,
    route               TEXT,
    frequency           TEXT,
    start_date          TEXT,
    end_date            TEXT,
    prescriber          TEXT,
    notes               TEXT,
    source_system       TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);
CREATE TABLE IF NOT EXISTS imaging (
    imaging_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_id        INTEGER,
    exam_date           TEXT NOT NULL,
    exam_type           TEXT NOT NULL,
    findings_structured TEXT,
    report_text         TEXT,
    measurements        TEXT,
    radiologist         TEXT,
    source_system       TEXT NOT NULL,
    source_exam_id      TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);
CREATE TABLE IF NOT EXISTS claims (
    claim_id_hie        INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id          INTEGER NOT NULL,
    encounter_id        INTEGER,
    service_date        TEXT NOT NULL,
    processing_date     TEXT,
    beneficiary_number  TEXT,
    service_code        TEXT,
    service_description TEXT,
    diagnosis_code      TEXT,
    total_amount        REAL,
    reimbursement_rate  REAL,
    amount_reimbursed   REAL,
    patient_copay       REAL,
    claim_status        TEXT,
    notes               TEXT,
    source_system       TEXT NOT NULL,
    source_claim_id     TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);
"""

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
_db_lock = threading.Lock()


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db():
    """Create tables if they don't exist."""
    with _db_lock:
        conn = get_connection()
        conn.executescript(HIE_SCHEMA_SQL)
        conn.commit()
        conn.close()


def execute_write(sql: str):
    """Execute an INSERT statement. Returns (success, message, dataframe_or_none)."""
    sql_stripped = sql.strip().rstrip(";").strip()
    sql_upper = sql_stripped.upper()

    # Safety: only allow INSERT
    if not sql_upper.startswith("INSERT"):
        return False, "Only INSERT statements are allowed in this tab. Use the **Query** tab for SELECT.", None

    # Block dangerous statements
    for keyword in ["DROP", "DELETE", "UPDATE", "ALTER", "CREATE", "ATTACH"]:
        if keyword in sql_upper:
            return False, f"The keyword `{keyword}` is not allowed.", None

    with _db_lock:
        conn = get_connection()
        try:
            cursor = conn.execute(sql_stripped)
            last_id = cursor.lastrowid
            conn.commit()

            # Determine which table was inserted into
            # Parse table name from INSERT INTO <table>
            table_name = sql_stripped.split("(")[0].split()[-1].strip()

            # Fetch the row that was just inserted
            try:
                df = pd.read_sql_query(
                    f"SELECT * FROM {table_name} WHERE rowid = ?",
                    conn,
                    params=(last_id,),
                )
            except Exception:
                df = None

            return True, f"Success! Row inserted into `{table_name}` with ID **{last_id}**.", df
        except Exception as e:
            conn.rollback()
            return False, f"**SQL Error:** {e}", None
        finally:
            conn.close()


def execute_read(sql: str):
    """Execute a SELECT statement. Returns (success, message, dataframe_or_none)."""
    sql_stripped = sql.strip().rstrip(";").strip()
    sql_upper = sql_stripped.upper()

    if not sql_upper.startswith("SELECT") and not sql_upper.startswith("PRAGMA"):
        return False, "Only SELECT and PRAGMA statements are allowed in this tab. Use the **Insert Data** tab for INSERT.", None

    for keyword in ["DROP", "DELETE", "UPDATE", "ALTER", "CREATE", "INSERT", "ATTACH"]:
        if keyword in sql_upper:
            return False, f"The keyword `{keyword}` is not allowed in queries.", None

    conn = get_connection()
    try:
        df = pd.read_sql_query(sql_stripped, conn)
        return True, f"Query returned **{len(df)}** row(s).", df
    except Exception as e:
        return False, f"**SQL Error:** {e}", None
    finally:
        conn.close()


def get_table_counts():
    """Return a dict of table_name -> row count."""
    conn = get_connection()
    tables = ["patients", "encounters", "vitals", "lab_results", "medications", "imaging", "claims"]
    counts = {}
    for t in tables:
        try:
            result = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()
            counts[t] = result[0]
        except Exception:
            counts[t] = 0
    conn.close()
    return counts


def get_group_submissions():
    """Return a dataframe of submissions per group per table."""
    conn = get_connection()
    tables = ["patients", "encounters", "vitals", "lab_results", "medications", "imaging", "claims"]
    rows = []
    for t in tables:
        try:
            result = conn.execute(
                f"SELECT source_system, COUNT(*) as records FROM {t} GROUP BY source_system"
            ).fetchall()
            for source, count in result:
                rows.append({"Table": t, "Group": source, "Records": count})
        except Exception:
            pass
    conn.close()
    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(columns=["Table", "Group", "Records"])


# ---------------------------------------------------------------------------
# FHIR Resource Builders
# ---------------------------------------------------------------------------

ENCOUNTER_TYPE_MAP = {
    "outpatient": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB", "display": "ambulatory"},
    "inpatient": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
    "emergency": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "EMER", "display": "emergency"},
    "home_visit": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "HH", "display": "home health"},
}


def build_fhir_patient(row):
    """Build a FHIR R4 Patient resource from a patients table row."""
    resource = {
        "resourceType": "Patient",
        "id": str(row["patient_id"]),
        "meta": {"source": row["source_system"]},
        "name": [
            {
                "use": "official",
                "family": row["last_name"],
                "given": [row["first_name"]],
            }
        ],
        "birthDate": row["date_of_birth"],
    }
    if row.get("sex"):
        resource["gender"] = "female" if row["sex"] == "F" else "male"
    if row.get("phone"):
        resource["telecom"] = [{"system": "phone", "value": row["phone"]}]
    if row.get("address"):
        resource["address"] = [{"text": row["address"]}]
    identifiers = []
    if row.get("national_health_id"):
        identifiers.append({
            "system": "urn:oid:1.2.250.1.213.1.4.8",
            "value": row["national_health_id"],
            "type": {"text": "INS (Identifiant National de Sante)"},
        })
    if row.get("insurance_number"):
        identifiers.append({
            "system": "urn:oid:1.2.250.1.213.1.4.2",
            "value": row["insurance_number"],
            "type": {"text": "Numero de Securite Sociale"},
        })
    if row.get("source_patient_id"):
        identifiers.append({
            "system": f"urn:source:{row['source_system']}",
            "value": row["source_patient_id"],
            "type": {"text": "Source System ID"},
        })
    if identifiers:
        resource["identifier"] = identifiers
    if row.get("related_patient_id"):
        resource["link"] = [
            {
                "other": {"reference": f"Patient/{row['related_patient_id']}"},
                "type": "seealso",
            }
        ]
    return resource


def build_fhir_encounter(row):
    """Build a FHIR R4 Encounter resource from an encounters table row."""
    enc_type = row.get("encounter_type", "").lower()
    class_coding = ENCOUNTER_TYPE_MAP.get(enc_type, {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
        "display": enc_type,
    })

    resource = {
        "resourceType": "Encounter",
        "id": str(row["encounter_id"]),
        "meta": {"source": row["source_system"]},
        "status": "finished",
        "class": class_coding,
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "period": {"start": row["encounter_date"]},
    }
    if row.get("encounter_time"):
        resource["period"]["start"] = f"{row['encounter_date']}T{row['encounter_time']}:00"
    if row.get("discharge_date"):
        resource["period"]["end"] = row["discharge_date"]
    if row.get("facility_name"):
        resource["serviceProvider"] = {"display": row["facility_name"]}
    if row.get("chief_complaint"):
        resource["reasonCode"] = [{"text": row["chief_complaint"]}]
    if row.get("diagnosis_code"):
        resource["diagnosis"] = [{
            "condition": {"display": row.get("diagnosis_text", "")},
            "use": {"text": "billing"},
        }]
    return resource


def build_fhir_observation_vitals(row):
    """Build FHIR Observation resources from a vitals table row. Returns a list."""
    observations = []
    base = {
        "meta": {"source": row["source_system"]},
        "status": "final",
        "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs", "display": "Vital Signs"}]}],
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "effectiveDateTime": row["measurement_date"],
    }
    if row.get("encounter_id"):
        base["encounter"] = {"reference": f"Encounter/{row['encounter_id']}"}

    if row.get("systolic_bp") and row.get("diastolic_bp"):
        bp = {**base, "resourceType": "Observation", "id": f"vitals-bp-{row['vital_id']}"}
        bp["code"] = {"coding": [{"system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel"}]}
        bp["component"] = [
            {
                "code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]},
                "valueQuantity": {"value": row["systolic_bp"], "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"},
            },
            {
                "code": {"coding": [{"system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure"}]},
                "valueQuantity": {"value": row["diastolic_bp"], "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"},
            },
        ]
        observations.append(bp)

    if row.get("heart_rate"):
        hr = {**base, "resourceType": "Observation", "id": f"vitals-hr-{row['vital_id']}"}
        hr["code"] = {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]}
        hr["valueQuantity"] = {"value": row["heart_rate"], "unit": "/min", "system": "http://unitsofmeasure.org", "code": "/min"}
        observations.append(hr)

    if row.get("weight_kg"):
        wt = {**base, "resourceType": "Observation", "id": f"vitals-wt-{row['vital_id']}"}
        wt["code"] = {"coding": [{"system": "http://loinc.org", "code": "29463-7", "display": "Body weight"}]}
        wt["valueQuantity"] = {"value": row["weight_kg"], "unit": "kg", "system": "http://unitsofmeasure.org", "code": "kg"}
        observations.append(wt)

    if row.get("temperature"):
        temp = {**base, "resourceType": "Observation", "id": f"vitals-temp-{row['vital_id']}"}
        temp["code"] = {"coding": [{"system": "http://loinc.org", "code": "8310-5", "display": "Body temperature"}]}
        temp["valueQuantity"] = {"value": row["temperature"], "unit": "Cel", "system": "http://unitsofmeasure.org", "code": "Cel"}
        observations.append(temp)

    if row.get("spo2"):
        sp = {**base, "resourceType": "Observation", "id": f"vitals-spo2-{row['vital_id']}"}
        sp["code"] = {"coding": [{"system": "http://loinc.org", "code": "2708-6", "display": "Oxygen saturation"}]}
        sp["valueQuantity"] = {"value": row["spo2"], "unit": "%", "system": "http://unitsofmeasure.org", "code": "%"}
        observations.append(sp)

    return observations


def build_fhir_observation_lab(row):
    """Build a FHIR Observation resource from a lab_results table row."""
    resource = {
        "resourceType": "Observation",
        "id": f"lab-{row['lab_id']}",
        "meta": {"source": row["source_system"]},
        "status": "corrected" if row.get("is_corrected") else "final",
        "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory", "display": "Laboratory"}]}],
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "effectiveDateTime": row["test_date"],
    }
    code_entry = {"text": row["test_name"]}
    if row.get("test_code"):
        code_entry["coding"] = [{"system": "http://loinc.org", "code": row["test_code"], "display": row["test_name"]}]
    resource["code"] = code_entry

    if row.get("encounter_id"):
        resource["encounter"] = {"reference": f"Encounter/{row['encounter_id']}"}
    if row.get("result_value") is not None:
        resource["valueQuantity"] = {"value": row["result_value"]}
        if row.get("unit"):
            resource["valueQuantity"]["unit"] = row["unit"]
    elif row.get("result_text"):
        resource["valueString"] = row["result_text"]
    if row.get("reference_low") is not None or row.get("reference_high") is not None:
        ref_range = {}
        if row.get("reference_low") is not None:
            ref_range["low"] = {"value": row["reference_low"]}
        if row.get("reference_high") is not None:
            ref_range["high"] = {"value": row["reference_high"]}
        resource["referenceRange"] = [ref_range]
    if row.get("flag"):
        flag_map = {"H": "high", "L": "low", "N": "normal"}
        interp = flag_map.get(row["flag"].upper(), row["flag"])
        resource["interpretation"] = [{"text": interp}]
    return resource


def build_fhir_medication_request(row):
    """Build a FHIR MedicationRequest resource from a medications table row."""
    resource = {
        "resourceType": "MedicationRequest",
        "id": f"med-{row['medication_id']}",
        "meta": {"source": row["source_system"]},
        "status": "completed" if row.get("end_date") else "active",
        "intent": "order",
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "medicationCodeableConcept": {"text": row["medication_name"]},
    }
    if row.get("encounter_id"):
        resource["encounter"] = {"reference": f"Encounter/{row['encounter_id']}"}
    if row.get("prescriber"):
        resource["requester"] = {"display": row["prescriber"]}
    dosage = {}
    if row.get("dose"):
        dosage["text"] = row["dose"]
    if row.get("route"):
        dosage["route"] = {"text": row["route"]}
    if row.get("frequency"):
        dosage["timing"] = {"code": {"text": row["frequency"]}}
    if dosage:
        resource["dosageInstruction"] = [dosage]
    return resource


def build_fhir_claim(row):
    """Build a FHIR Claim resource from a claims table row."""
    resource = {
        "resourceType": "Claim",
        "id": f"claim-{row['claim_id_hie']}",
        "meta": {"source": row["source_system"]},
        "status": "active",
        "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional"}]},
        "use": "claim",
        "patient": {"reference": f"Patient/{row['patient_id']}"},
        "created": row.get("processing_date") or row["service_date"],
        "total": {"value": row.get("total_amount", 0), "currency": "EUR"},
    }
    if row.get("beneficiary_number"):
        resource["insurance"] = [{"sequence": 1, "focal": True, "coverage": {"display": f"Beneficiary: {row['beneficiary_number']}"}}]
    item = {"sequence": 1, "servicedDate": row["service_date"]}
    if row.get("service_code"):
        item["productOrService"] = {"coding": [{"code": row["service_code"]}], "text": row.get("service_description", "")}
    elif row.get("service_description"):
        item["productOrService"] = {"text": row["service_description"]}
    if row.get("diagnosis_code"):
        resource["diagnosis"] = [{"sequence": 1, "diagnosisCodeableConcept": {"coding": [{"code": row["diagnosis_code"]}]}}]
    resource["item"] = [item]
    return resource


def get_all_fhir_resources():
    """Build all FHIR resources from current HIE data. Returns a dict of resource_type -> list."""
    conn = get_connection()
    resources = {
        "Patient": [],
        "Encounter": [],
        "Observation": [],
        "MedicationRequest": [],
        "Claim": [],
    }

    # Patients
    rows = conn.execute("SELECT * FROM patients").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM patients LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["Patient"].append(build_fhir_patient(r))

    # Encounters
    rows = conn.execute("SELECT * FROM encounters").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM encounters LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["Encounter"].append(build_fhir_encounter(r))

    # Vitals -> Observations
    rows = conn.execute("SELECT * FROM vitals").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM vitals LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["Observation"].extend(build_fhir_observation_vitals(r))

    # Lab results -> Observations
    rows = conn.execute("SELECT * FROM lab_results").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM lab_results LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["Observation"].append(build_fhir_observation_lab(r))

    # Medications
    rows = conn.execute("SELECT * FROM medications").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM medications LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["MedicationRequest"].append(build_fhir_medication_request(r))

    # Claims
    rows = conn.execute("SELECT * FROM claims").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM claims LIMIT 0").description]
    for row in rows:
        r = dict(zip(cols, row))
        resources["Claim"].append(build_fhir_claim(r))

    conn.close()
    return resources


# ---------------------------------------------------------------------------
# Initialize database
# ---------------------------------------------------------------------------
init_db()

# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HIE Shared Database",
    page_icon="🏥",
    layout="wide",
)

st.title("Regional Health Information Exchange (HIE)")
st.caption("Interoperability Lab - Shared Database")

# Sidebar - Group selection and schema reference
with st.sidebar:
    st.header("Your Group")
    group = st.selectbox("Select your group:", GROUPS)

    st.divider()
    st.header("Your Target Tables")
    for table in GROUP_TABLES.get(group, []):
        st.markdown(f"- `{table}`")

    st.divider()
    st.header("Quick Schema Reference")
    schema_table = st.selectbox("View table schema:", [
        "patients", "encounters", "vitals", "lab_results",
        "medications", "imaging", "claims",
    ])
    conn = get_connection()
    schema_df = pd.read_sql_query(f"PRAGMA table_info({schema_table})", conn)
    conn.close()
    st.dataframe(
        schema_df[["name", "type", "notnull"]].rename(
            columns={"name": "Column", "type": "Type", "notnull": "Required"}
        ),
        hide_index=True,
        use_container_width=True,
    )

# Main content - tabs
tab_insert, tab_query, tab_dashboard, tab_fhir, tab_export = st.tabs(["Insert Data", "Query Data", "Dashboard", "FHIR Explorer", "Export (Assessment)"])

# ---- Tab 1: Insert Data ----
with tab_insert:
    st.subheader("Write your INSERT statement")
    st.markdown(
        "Write a SQL `INSERT INTO` statement to load your data into the HIE database. "
        "You do **not** need to prefix table names — just use `patients`, `encounters`, etc."
    )

    # Provide a starter template
    starter = f"""INSERT INTO patients (
    last_name,
    first_name,
    date_of_birth,
    source_system
) VALUES (
    'DUPONT',
    'Marie',
    '1993-03-15',
    '{group}'
);"""

    sql_insert = st.text_area(
        "SQL INSERT statement:",
        value="" if st.session_state.get("sql_cleared") else "",
        height=250,
        placeholder=starter,
        key="insert_sql",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_insert = st.button("Execute", type="primary", key="run_insert")
    with col2:
        if st.button("Show example", key="show_example"):
            st.code(starter, language="sql")

    if run_insert and sql_insert.strip():
        success, message, df = execute_write(sql_insert)
        if success:
            st.success(message)
            if df is not None and not df.empty:
                st.markdown("**Inserted row:**")
                st.dataframe(df, hide_index=True, use_container_width=True)

            st.info(
                "**Remember this ID!** Use it as `patient_id` or `encounter_id` in your next INSERT statements."
            )
        else:
            st.error(message)

            # Provide helpful hints for common errors
            msg_lower = message.lower()
            if "not null" in msg_lower:
                st.warning(
                    "A required field is missing. Check the schema in the sidebar to see which columns are required (Required = 1)."
                )
            elif "foreign key" in msg_lower:
                st.warning(
                    "The `patient_id` or `encounter_id` you used does not exist. "
                    "Did you insert the patient first? Check the Query tab to find your patient's ID."
                )
            elif "syntax error" in msg_lower:
                st.warning(
                    "Check for: trailing commas before `)`, mismatched parentheses, or missing quotes around text values."
                )
    elif run_insert:
        st.warning("Paste or type your SQL statement above before clicking Execute.")

# ---- Tab 2: Query Data ----
with tab_query:
    st.subheader("Query the HIE database")
    st.markdown("Run `SELECT` statements to explore the shared HIE data from all groups.")

    # Quick query buttons
    st.markdown("**Quick queries:**")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    quick_query = None
    with qcol1:
        if st.button("All patients"):
            quick_query = "SELECT patient_id, last_name, first_name, date_of_birth, source_system FROM patients;"
    with qcol2:
        if st.button("All encounters"):
            quick_query = "SELECT encounter_id, patient_id, encounter_type, encounter_date, facility_name, source_system FROM encounters ORDER BY encounter_date;"
    with qcol3:
        if st.button("My group's data"):
            quick_query = f"SELECT 'patients' as tbl, COUNT(*) as n FROM patients WHERE source_system = '{group}' UNION ALL SELECT 'encounters', COUNT(*) FROM encounters WHERE source_system = '{group}' UNION ALL SELECT 'vitals', COUNT(*) FROM vitals WHERE source_system = '{group}' UNION ALL SELECT 'lab_results', COUNT(*) FROM lab_results WHERE source_system = '{group}' UNION ALL SELECT 'medications', COUNT(*) FROM medications WHERE source_system = '{group}' UNION ALL SELECT 'imaging', COUNT(*) FROM imaging WHERE source_system = '{group}' UNION ALL SELECT 'claims', COUNT(*) FROM claims WHERE source_system = '{group}';"
    with qcol4:
        if st.button("Duplicate patients"):
            quick_query = "SELECT last_name, first_name, date_of_birth, COUNT(*) as registrations FROM patients GROUP BY UPPER(last_name), UPPER(first_name), date_of_birth HAVING COUNT(*) > 1;"

    sql_query = st.text_area(
        "SQL SELECT statement:",
        value=quick_query if quick_query else "",
        height=150,
        placeholder="SELECT * FROM patients;",
        key="query_sql",
    )

    if st.button("Run Query", type="primary", key="run_query") or quick_query:
        query_to_run = sql_query.strip() if sql_query.strip() else (quick_query or "")
        if query_to_run:
            success, message, df = execute_read(query_to_run)
            if success:
                st.success(message)
                if df is not None and not df.empty:
                    st.dataframe(df, hide_index=True, use_container_width=True)
                elif df is not None:
                    st.info("Query returned no results.")
            else:
                st.error(message)

# ---- Tab 3: Dashboard ----
with tab_dashboard:
    st.subheader("HIE Database Status")

    # Record counts per table
    counts = get_table_counts()
    total = sum(counts.values())

    st.metric("Total records in HIE", total)

    st.markdown("**Records per table:**")
    count_df = pd.DataFrame(
        [{"Table": t, "Records": c} for t, c in counts.items()]
    )
    st.dataframe(count_df, hide_index=True, use_container_width=True)

    st.divider()

    # Submissions by group
    st.markdown("**Submissions by group:**")
    sub_df = get_group_submissions()
    if not sub_df.empty:
        # Pivot for a nice grid view
        pivot = sub_df.pivot_table(
            index="Group", columns="Table", values="Records", fill_value=0, aggfunc="sum"
        ).reset_index()
        st.dataframe(pivot, hide_index=True, use_container_width=True)
    else:
        st.info("No data has been submitted yet. Groups should start inserting their data!")

    st.divider()

    # Timeline check
    st.markdown("**Marie Dupont's Care Timeline** (auto-generated from submitted data):")
    conn = get_connection()
    try:
        timeline_df = pd.read_sql_query(
            """
            SELECT
                e.encounter_date,
                e.encounter_time,
                e.encounter_type,
                e.facility_name,
                e.chief_complaint,
                e.source_system
            FROM encounters e
            JOIN patients p ON e.patient_id = p.patient_id
            WHERE UPPER(p.last_name) = 'DUPONT'
              AND p.date_of_birth = '1993-03-15'
            ORDER BY e.encounter_date, e.encounter_time
            """,
            conn,
        )
        if not timeline_df.empty:
            st.dataframe(timeline_df, hide_index=True, use_container_width=True)
        else:
            st.info("No encounters for Marie Dupont yet. The timeline will appear as groups submit data.")
    except Exception:
        st.info("No encounters submitted yet.")
    finally:
        conn.close()

    if st.button("Refresh Dashboard"):
        st.rerun()

# ---- Tab 4: FHIR Explorer ----
with tab_fhir:
    st.subheader("FHIR Resource Explorer")
    st.markdown(
        "This tab shows what the HIE data would look like as **HL7 FHIR R4** resources. "
        "FHIR (Fast Healthcare Interoperability Resources) is the modern standard for "
        "exchanging healthcare data between systems. Instead of flat database tables, "
        "FHIR uses structured JSON resources with standardized coding systems."
    )

    fhir_resources = get_all_fhir_resources()
    total_fhir = sum(len(v) for v in fhir_resources.values())

    if total_fhir == 0:
        st.info("No data in the HIE yet. Insert some data first, then come back to see it as FHIR resources.")
    else:
        st.markdown(f"**{total_fhir} FHIR resources** generated from the HIE data:")

        # Summary counts
        fcols = st.columns(5)
        for i, (rtype, rlist) in enumerate(fhir_resources.items()):
            with fcols[i]:
                st.metric(rtype, len(rlist))

        st.divider()

        # Let user pick which resource type to explore
        resource_type = st.selectbox(
            "Select a FHIR resource type to view:",
            [rt for rt, rl in fhir_resources.items() if rl],
        )

        if resource_type:
            resource_list = fhir_resources[resource_type]

            # Build labels for each resource
            labels = []
            for r in resource_list:
                if resource_type == "Patient":
                    name = r.get("name", [{}])[0]
                    labels.append(f"Patient/{r['id']} - {name.get('family', '?')}, {name.get('given', ['?'])[0]}")
                elif resource_type == "Encounter":
                    labels.append(f"Encounter/{r['id']} - {r.get('class', {}).get('display', '?')} ({r.get('period', {}).get('start', '?')})")
                elif resource_type == "Observation":
                    labels.append(f"Observation/{r['id']} - {r.get('code', {}).get('coding', [{}])[0].get('display', r.get('code', {}).get('text', '?'))}")
                elif resource_type == "MedicationRequest":
                    labels.append(f"MedicationRequest/{r['id']} - {r.get('medicationCodeableConcept', {}).get('text', '?')}")
                elif resource_type == "Claim":
                    labels.append(f"Claim/{r['id']} - {r.get('total', {}).get('value', '?')} EUR")
                else:
                    labels.append(f"{resource_type}/{r.get('id', '?')}")

            selected_label = st.selectbox("Select a resource:", labels)
            selected_idx = labels.index(selected_label)
            selected_resource = resource_list[selected_idx]

            # Show the resource as formatted JSON
            st.json(selected_resource)

            # Side-by-side comparison: HIE row vs FHIR
            st.divider()
            st.markdown("**HIE Database Row vs FHIR Resource**")
            st.markdown(
                "The left side shows how this data is stored in the HIE relational database. "
                "The right side shows the same data as a FHIR resource — notice the standardized "
                "coding systems (LOINC, SNOMED), structured references between resources, "
                "and self-describing format."
            )

            col_db, col_fhir = st.columns(2)
            with col_db:
                st.markdown("**HIE Database (relational table)**")
                # Fetch the original row
                conn = get_connection()
                try:
                    rid = selected_resource["id"]
                    if resource_type == "Patient":
                        orig_df = pd.read_sql_query("SELECT * FROM patients WHERE patient_id = ?", conn, params=(rid,))
                    elif resource_type == "Encounter":
                        orig_df = pd.read_sql_query("SELECT * FROM encounters WHERE encounter_id = ?", conn, params=(rid,))
                    elif resource_type == "Observation":
                        # Could be vitals or lab
                        if rid.startswith("lab-"):
                            lab_id = rid.replace("lab-", "")
                            orig_df = pd.read_sql_query("SELECT * FROM lab_results WHERE lab_id = ?", conn, params=(lab_id,))
                        else:
                            # vitals - extract vital_id from id like "vitals-bp-3"
                            vital_id = rid.split("-")[-1]
                            orig_df = pd.read_sql_query("SELECT * FROM vitals WHERE vital_id = ?", conn, params=(vital_id,))
                    elif resource_type == "MedicationRequest":
                        med_id = rid.replace("med-", "")
                        orig_df = pd.read_sql_query("SELECT * FROM medications WHERE medication_id = ?", conn, params=(med_id,))
                    elif resource_type == "Claim":
                        claim_id = rid.replace("claim-", "")
                        orig_df = pd.read_sql_query("SELECT * FROM claims WHERE claim_id_hie = ?", conn, params=(claim_id,))
                    else:
                        orig_df = pd.DataFrame()

                    if not orig_df.empty:
                        # Display as vertical key-value pairs
                        for col_name in orig_df.columns:
                            val = orig_df[col_name].iloc[0]
                            if val is not None and str(val).strip():
                                st.markdown(f"`{col_name}`: {val}")
                    else:
                        st.info("Could not find the original row.")
                except Exception as e:
                    st.error(f"Error fetching original row: {e}")
                finally:
                    conn.close()

            with col_fhir:
                st.markdown("**FHIR R4 Resource (JSON)**")
                st.code(json.dumps(selected_resource, indent=2), language="json")

        st.divider()
        st.markdown("### What makes FHIR different from our HIE database?")
        st.markdown(
            """
| HIE Database (what you built) | FHIR (the standard) |
|------|------|
| Flat tables with columns | Nested JSON resources with references |
| Custom column names (`systolic_bp`) | Standardized codes (LOINC `8480-6`) |
| Foreign keys link tables (`patient_id = 1`) | Resource references (`Patient/1`) |
| Schema is local to this database | Schema is a global standard — any FHIR server understands it |
| You had to agree on one schema for 8 groups | FHIR provides the agreed schema for everyone |
| Data types vary (text dates, mixed formats) | Strict data types with required formats |

**Key insight:** The work you did today — mapping your data to a shared schema, converting date formats,
splitting blood pressure values, choosing the right codes — is exactly the work that FHIR aims to
standardize so that every system does it the same way, once, rather than every exchange partner
negotiating their own mappings.
"""
        )

# ---- Tab 5: Export (Assessment) ----
with tab_export:
    st.subheader("Export & Assessment")
    st.markdown(
        "Use this tab to review each group's submissions and download data for grading. "
        "The scorecard flags common errors automatically. Download the full Excel workbook "
        "at the end of class before students leave — data does not persist after the app restarts."
    )
    st.info("**Instructor reminder:** Download the Excel file before ending class. The database resets when the app restarts.")

    ALL_TABLES = ["patients", "encounters", "vitals", "lab_results", "medications", "imaging", "claims"]

    # ------------------------------------------------------------------
    # Section 1: Class-wide scorecard
    # ------------------------------------------------------------------
    st.divider()
    st.markdown("### Class Scorecard — Submissions by Group")

    def build_scorecard():
        conn = get_connection()
        rows = []
        for grp in GROUPS:
            required = GROUP_TABLES.get(grp, [])
            row = {"Group": grp}
            missing = []
            for table in ALL_TABLES:
                try:
                    count = conn.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE source_system = ?", (grp,)
                    ).fetchone()[0]
                except Exception:
                    count = 0
                row[table] = count
                if table in required and count == 0:
                    missing.append(table)
            row["Status"] = "✓ Complete" if not missing else f"✗ Missing: {', '.join(missing)}"
            rows.append(row)
        conn.close()
        return pd.DataFrame(rows)

    scorecard_df = build_scorecard()
    st.dataframe(scorecard_df, hide_index=True, use_container_width=True)

    if st.button("Refresh Scorecard"):
        st.rerun()

    # ------------------------------------------------------------------
    # Section 2: Per-group detailed review with automated feedback
    # ------------------------------------------------------------------
    st.divider()
    st.markdown("### Per-Group Detailed Review")
    st.markdown("Select a group to see their submitted data and automated assessment feedback.")

    selected_group_export = st.selectbox(
        "Select group to review:",
        ["-- Select a group --"] + GROUPS,
        key="export_group_select"
    )

    if selected_group_export and selected_group_export != "-- Select a group --":
        conn = get_connection()
        required_tables = GROUP_TABLES.get(selected_group_export, [])
        st.markdown(f"**Required tables for this group:** {', '.join(f'`{t}`' for t in required_tables)}")
        st.markdown("---")

        for table in required_tables:
            try:
                df = pd.read_sql_query(
                    f"SELECT * FROM {table} WHERE source_system = ?",
                    conn, params=(selected_group_export,)
                )
            except Exception:
                df = pd.DataFrame()

            count = len(df)
            status_icon = "✓" if count > 0 else "✗"
            with st.expander(f"{status_icon} `{table}` — {count} record(s) submitted", expanded=(count == 0)):
                if df.empty:
                    st.error("No records submitted for this table.")
                else:
                    st.dataframe(df, hide_index=True, use_container_width=True)

                    # --- Automated assessment checks ---
                    feedback = []

                    if table == "patients":
                        # Date format check
                        if "date_of_birth" in df.columns:
                            bad = df[~df["date_of_birth"].fillna("").str.match(r"^\d{4}-\d{2}-\d{2}$")]
                            if not bad.empty:
                                feedback.append(("warning", f"{len(bad)} patient(s) have `date_of_birth` not in YYYY-MM-DD format. Dates must be converted from DD/MM/YYYY."))
                        # source_patient_id documented?
                        if "source_patient_id" in df.columns:
                            missing_src = df["source_patient_id"].isna().sum()
                            if missing_src == count:
                                feedback.append(("info", "No `source_patient_id` values recorded. Students are encouraged to document the original system ID for traceability."))
                        # Mother-baby linkage for Groups 6 & 7
                        if selected_group_export in ["Group 6 - Hospital Maternity", "Group 7 - PMI Postnatal"]:
                            if "related_patient_id" in df.columns:
                                linked = df["related_patient_id"].notna().sum()
                                if linked == 0:
                                    feedback.append(("warning", "No mother-baby linkage found (`related_patient_id` is empty). The baby patient should be linked to the mother using this field."))
                                else:
                                    feedback.append(("success", f"{linked} patient record(s) have mother-baby linkage (`related_patient_id` populated). ✓"))
                            babies = df[df["date_of_birth"].fillna("") == "2026-01-28"] if "date_of_birth" in df.columns else pd.DataFrame()
                            if babies.empty:
                                feedback.append(("warning", "Baby Louise (DOB 2026-01-28) does not appear as a separate patient record. Groups 6 and 7 should submit both mother and baby as separate patients."))
                            else:
                                feedback.append(("success", "Baby Louise submitted as a separate patient record. ✓"))
                        # Check for confusable patient DUPOND (Group 4)
                        if selected_group_export == "Group 4 - Obstetric Clinic":
                            if "last_name" in df.columns:
                                dupond = df[df["last_name"].str.upper() == "DUPOND"]
                                if not dupond.empty:
                                    feedback.append(("error", "Patient 'DUPOND' was submitted — this is the confusable second patient, NOT Marie Dupont. This record should have been excluded."))
                                else:
                                    feedback.append(("success", "Confusable patient DUPOND was correctly excluded. ✓"))

                    if table == "encounters":
                        if "encounter_date" in df.columns:
                            bad = df[~df["encounter_date"].fillna("").str.match(r"^\d{4}-\d{2}-\d{2}$")]
                            if not bad.empty:
                                feedback.append(("warning", f"{len(bad)} encounter(s) have `encounter_date` not in YYYY-MM-DD format. DICOM dates (YYYYMMDD) and French dates (DD/MM/YYYY) must be converted."))
                        if "encounter_type" in df.columns:
                            valid_types = {"outpatient", "inpatient", "emergency", "home_visit"}
                            invalid = df[~df["encounter_type"].str.lower().isin(valid_types)]
                            if not invalid.empty:
                                feedback.append(("warning", f"{len(invalid)} encounter(s) use an unrecognised `encounter_type`. Valid values: outpatient, inpatient, emergency, home_visit."))

                    if table == "vitals":
                        if "systolic_bp" in df.columns:
                            no_bp = df["systolic_bp"].isna().sum()
                            if no_bp == count:
                                feedback.append(("warning", "No `systolic_bp` values submitted. Blood pressure data should be converted from French shorthand (e.g., '11/7' → systolic=110, diastolic=70)."))
                        if "weight_kg" in df.columns and selected_group_export == "Group 7 - PMI Postnatal":
                            high_weight = df[df["weight_kg"].fillna(0) > 100]
                            if not high_weight.empty:
                                feedback.append(("error", f"{len(high_weight)} weight value(s) appear to be in grams, not kg (value > 100). Baby weight must be converted: divide grams by 1000 (e.g., 3100g → 3.1 kg)."))
                            else:
                                feedback.append(("success", "Weight values appear to be in kg (all ≤ 100). Unit conversion from grams looks correct. ✓"))

                    if table == "lab_results":
                        if selected_group_export == "Group 2 - Laboratory":
                            # Check for corrected result flag
                            if "is_corrected" in df.columns:
                                corrected = (df["is_corrected"] == 1).sum()
                                if corrected == 0:
                                    feedback.append(("warning", "No corrected lab results (`is_corrected = 1`). Group 2 should have flagged the corrected glucose value."))
                                else:
                                    feedback.append(("success", f"{corrected} corrected result(s) properly flagged with `is_corrected = 1`. ✓"))
                            # Check for truncated test names
                            if "test_name" in df.columns:
                                truncated = df[df["test_name"].fillna("").str.endswith(("(Ir", "(I", "Scre", "Anti"))]
                                if not truncated.empty:
                                    feedback.append(("error", f"{len(truncated)} test name(s) appear truncated. The anti-Kell antibody test name must be written in full — truncation is a patient safety issue."))
                                # Check units consistency
                                if "unit" in df.columns:
                                    units = df["unit"].dropna().unique()
                                    if "g/L" in units and "mmol/L" in units:
                                        feedback.append(("warning", "Both g/L and mmol/L units found in lab results. All glucose values should be converted to a single unit (mmol/L preferred)."))
                                    elif "mmol/L" in units:
                                        feedback.append(("success", "Units appear consistent (mmol/L). ✓"))

                    if table == "medications":
                        if selected_group_export in ["Group 4 - Obstetric Clinic", "Group 6 - Hospital Maternity"]:
                            if "notes" in df.columns:
                                methyldopa = df[df["medication_name"].str.upper().str.contains("METHYLDOPA", na=False)]
                                if not methyldopa.empty:
                                    noted = methyldopa["notes"].notna().sum()
                                    if noted == 0:
                                        feedback.append(("warning", "Methyldopa submitted but `notes` field is empty. The dose discrepancy (500mg/day vs 750mg/day) should be documented in notes."))
                                    else:
                                        feedback.append(("success", "Methyldopa notes field populated — dose discrepancy documented. ✓"))

                    if table == "claims":
                        if selected_group_export == "Group 8 - Insurance Payer":
                            # Check for duplicate flagging
                            if "claim_status" in df.columns:
                                dupes = df[df["claim_status"].fillna("").str.lower() == "duplicate"]
                                if dupes.empty:
                                    feedback.append(("warning", "No claims flagged as 'Duplicate'. Group 8 should have identified and flagged the duplicate claim."))
                                else:
                                    feedback.append(("success", f"{len(dupes)} claim(s) correctly flagged as Duplicate. ✓"))
                            # Check amount formatting
                            if "total_amount" in df.columns:
                                non_numeric = df[df["total_amount"].isna() & df["service_description"].notna()]
                                if not non_numeric.empty:
                                    feedback.append(("info", "Some claims have no `total_amount`. Verify that euro amounts were converted from comma decimal format (e.g., '124,50' → 124.50)."))
                            if "reimbursement_rate" in df.columns:
                                text_rates = df[df["reimbursement_rate"] > 1.0]
                                if not text_rates.empty:
                                    feedback.append(("error", f"{len(text_rates)} claim(s) have `reimbursement_rate` > 1.0. Rates must be decimal fractions (100% → 1.0, 70% → 0.7), not percentages."))

                    # Render feedback
                    if feedback:
                        st.markdown("**Automated Feedback:**")
                        for level, msg in feedback:
                            if level == "success":
                                st.success(msg)
                            elif level == "warning":
                                st.warning(msg)
                            elif level == "error":
                                st.error(msg)
                            else:
                                st.info(msg)

        conn.close()

    # ------------------------------------------------------------------
    # Section 3: Download
    # ------------------------------------------------------------------
    st.divider()
    st.markdown("### Download for Grading")
    st.markdown("Download all submitted data as an Excel workbook. Each table is a separate sheet. A Summary sheet shows record counts by group.")

    def build_excel_workbook():
        output = io.BytesIO()
        conn = get_connection()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Summary sheet
            summary_rows = []
            for grp in GROUPS:
                required = GROUP_TABLES.get(grp, [])
                for table in ALL_TABLES:
                    try:
                        count = conn.execute(
                            f"SELECT COUNT(*) FROM {table} WHERE source_system = ?", (grp,)
                        ).fetchone()[0]
                    except Exception:
                        count = 0
                    required_flag = "Yes" if table in required else "No"
                    submitted_flag = "✓" if count > 0 else ("✗ Missing" if table in required else "—")
                    summary_rows.append({
                        "Group": grp,
                        "Table": table,
                        "Required": required_flag,
                        "Records Submitted": count,
                        "Status": submitted_flag,
                    })
            pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)

            # One sheet per table with all groups
            for table in ALL_TABLES:
                try:
                    df = pd.read_sql_query(
                        f"SELECT * FROM {table} ORDER BY source_system", conn
                    )
                    if not df.empty:
                        df.to_excel(writer, sheet_name=table[:31], index=False)
                except Exception:
                    pass

        conn.close()
        output.seek(0)
        return output.read()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Generate Excel Workbook", type="primary", key="gen_excel_btn"):
            with st.spinner("Building workbook — this may take a few seconds..."):
                try:
                    excel_bytes = build_excel_workbook()
                    st.session_state["excel_ready"] = excel_bytes
                except Exception as e:
                    st.error(f"Error building workbook: {e}")

        if st.session_state.get("excel_ready"):
            st.download_button(
                label="⬇ Download All Data (Excel)",
                data=st.session_state["excel_ready"],
                file_name="hie_interoperability_lab_submissions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_excel_btn",
            )

    with col_b:
        if selected_group_export and selected_group_export != "-- Select a group --":
            def build_group_csv(grp):
                conn = get_connection()
                frames = []
                for table in ALL_TABLES:
                    try:
                        df = pd.read_sql_query(
                            f"SELECT ? as _table, * FROM {table} WHERE source_system = ?",
                            conn, params=(table, grp)
                        )
                        frames.append(df)
                    except Exception:
                        pass
                conn.close()
                if frames:
                    return pd.concat(frames, ignore_index=True).to_csv(index=False).encode("utf-8")
                return b""

            csv_bytes = build_group_csv(selected_group_export)
            if csv_bytes:
                safe_name = re.sub(r"[^a-zA-Z0-9]", "_", selected_group_export)
                st.download_button(
                    label=f"⬇ Download {selected_group_export} Only (CSV)",
                    data=csv_bytes,
                    file_name=f"hie_submission_{safe_name}.csv",
                    mime="text/csv",
                    key="dl_csv_btn",
                )
