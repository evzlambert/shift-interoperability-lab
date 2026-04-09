# Clinical Reference Sheet for Non-Clinical Students

**This sheet explains the medical terminology and clinical context in your datasets. You do NOT need to be a healthcare provider to complete this exercise. Your job is to focus on the DATA - its structure, quality, and how it moves between systems.**

---

## The Patient's Condition - Plain Language Summary

Marie Dupont is pregnant with her second child. During pregnancy, she develops two complications:

1. **Gestational Diabetes (GDM):** A type of diabetes (high blood sugar) that develops during pregnancy. It is diagnosed through a blood test called an OGTT (Oral Glucose Tolerance Test), where the patient drinks a sugary drink and blood sugar is measured over time. It is managed with diet and blood sugar monitoring.

2. **Preeclampsia:** A dangerous condition in pregnancy involving high blood pressure and protein in the urine. It can progress to be life-threatening for both mother and baby. Severe preeclampsia requires emergency treatment and often emergency delivery.

She is ultimately delivered by **emergency cesarean section** (surgical delivery) because the preeclampsia becomes too severe to wait for natural labor.

---

## Common Medical Terms in the Datasets

### Patient Demographics and History

| Term | Meaning |
|------|---------|
| G2P1 | Gravida 2, Para 1 - this is her 2nd pregnancy (G2), she has delivered 1 baby before (P1) |
| Gestational age (weeks) | How far along the pregnancy is, measured in weeks from last menstrual period |
| 38 weeks / 38 wk | The pregnancy is at 38 weeks (full term is typically 37-42 weeks) |
| SA (semaines d'amenorrhee) | French term for gestational weeks - same concept as gestational age |
| DDG / EDD | Estimated due date (Date de Debut de Grossesse / Estimated Date of Delivery) |

### Vital Signs and Measurements

| Term | Meaning | Normal Range (Pregnancy) |
|------|---------|------------------------|
| Blood pressure (BP) | Pressure of blood in arteries. Written as systolic/diastolic (e.g., 120/80 mmHg). In French shorthand, "12/8" means 120/80 | Below 140/90 in pregnancy |
| TA (Tension Arterielle) | French term for blood pressure - same as BP |
| Heart rate (HR/FC) | Heartbeats per minute | 60-100 bpm |
| SpO2 | Blood oxygen saturation level | 95-100% |
| Temperature | Body temperature in Celsius | 36.5-37.5 C |
| Respiratory rate (RR/FR) | Breaths per minute | 12-20 |
| Fetal heart rate (FHR/FCF) | Baby's heartbeat, measured in beats per minute | 110-160 bpm |
| Fundal height | Distance from pubic bone to top of uterus (in cm) - approximates gestational age | Roughly equal to weeks of gestation |
| Glasgow Coma Scale (GCS) | Consciousness assessment scored 3-15. 15 = fully alert and oriented | 15 |

### Laboratory Tests

| Test | What It Measures | Why It Matters |
|------|-----------------|----------------|
| CBC / NFS (Complete Blood Count) | Red blood cells, white blood cells, platelets, hemoglobin | Low platelets can indicate a dangerous complication called HELLP syndrome |
| Hemoglobin (Hb) | Oxygen-carrying protein in red blood cells | Low = anemia, common in pregnancy |
| Platelets | Blood clotting cells | Low count in preeclampsia = danger sign |
| Blood type (ABO + Rh) | Blood group classification (A, B, AB, O) and Rh factor (+/-) | Critical for safe blood transfusion |
| Antibody screen / RAI | Checks for irregular antibodies in blood | Positive = patient has antibodies that could react with transfused blood |
| Anti-Kell | A specific irregular antibody | Makes blood transfusion matching more complex - must use Kell-negative blood |
| Glucose (fasting) | Blood sugar level when patient hasn't eaten | High = possible diabetes |
| OGTT / HGPO | Oral glucose tolerance test - blood sugar measured after drinking glucose | Diagnoses gestational diabetes |
| HbA1c | Average blood sugar over past 2-3 months | Measures long-term glucose control |
| AST / ASAT, ALT / ALAT | Liver enzymes | Elevated in preeclampsia = liver damage |
| Creatinine | Kidney function marker | Elevated = kidneys not filtering well |
| Uric acid | Waste product in blood | Elevated in preeclampsia |
| Proteinuria | Protein in urine | Key sign of preeclampsia |
| Protein/Creatinine ratio | More precise measure of protein in urine | Above 30 mg/mmol = significant |

### Units of Measurement

| Unit | What It Measures | Notes |
|------|-----------------|-------|
| g/L (grams per liter) | Concentration | French standard for glucose |
| mmol/L (millimoles per liter) | Concentration | International standard for glucose |
| g/dL (grams per deciliter) | Concentration | Used for hemoglobin |
| G/L (Giga per liter) | Count (billions per liter) | Used for platelets |
| IU/L or UI/L | International Units per liter | Used for liver enzymes |
| umol/L (micromoles per liter) | Concentration | Used for creatinine, uric acid |
| mg/mmol | Ratio | Used for protein/creatinine ratio |
| mmHg | Millimeters of mercury | Blood pressure unit |
| mm | Millimeters | Fetal measurements on ultrasound |

**Key conversion to watch for:** Glucose can be reported in g/L (French) or mmol/L (international). 1 g/L = 5.55 mmol/L. If your dataset switches between these units, values will look very different for the same test.

### Imaging / Ultrasound Terms

| Term | Meaning |
|------|---------|
| CRL (LCC) | Crown-Rump Length - measures baby size in early pregnancy |
| BPD (BIP) | Biparietal Diameter - measures baby's head width |
| HC (PC) | Head Circumference |
| AC (PA) | Abdominal Circumference |
| FL (LF) | Femur Length - measures baby's thigh bone |
| NT (CN) | Nuchal Translucency - fluid at back of baby's neck (screening test) |
| EFW (PFE) | Estimated Fetal Weight |
| AFI (ILA) | Amniotic Fluid Index - measures fluid around baby |
| Oligohydramnios | Too little amniotic fluid (AFI < 8cm) - concerning |
| Doppler (umbilical/cerebral) | Measures blood flow in baby's blood vessels. PI = Pulsatility Index | Abnormal flow = baby may not be getting enough oxygen |
| PACS | Picture Archiving and Communication System - where images are stored |
| DICOM | Digital Imaging standard - the format medical images use |
| RIS | Radiology Information System |

### Medications in the Datasets

| Medication | What It Does |
|-----------|-------------|
| Methyldopa (Aldomet) | Lowers blood pressure - commonly used in pregnancy |
| Nicardipine | IV blood pressure medication for emergencies |
| Magnesium Sulfate (MgSO4) | Prevents seizures in severe preeclampsia |
| Nifedipine | Oral blood pressure medication (used after delivery) |
| Betamethasone | Steroid injection to mature baby's lungs before early delivery |
| Folic acid | Vitamin supplement for pregnancy |

### Procedures and Events

| Term | Meaning |
|------|---------|
| Cesarean section (C-section) | Surgical delivery through an incision in the abdomen |
| Apgar score | Quick assessment of newborn's condition at 1 and 5 minutes after birth (scored 0-10). 8/9 = healthy baby |
| HELLP syndrome | Serious complication: Hemolysis, Elevated Liver enzymes, Low Platelets |
| Late decelerations | Drops in fetal heart rate after contractions - sign baby is in distress |
| Medication reconciliation | Process of comparing medication lists from different sources to find discrepancies |

### Abbreviations You May Encounter

| Abbreviation | Full Term |
|-------------|-----------|
| NKA / NKDA | No Known Allergies / No Known Drug Allergies |
| RAS | Rien A Signaler (French: nothing to report) |
| HTA | Hypertension (French abbreviation) |
| DG / GDM | Gestational Diabetes |
| HTN | Hypertension |
| IV / IVSE | Intravenous / IV with syringe pump |
| IM | Intramuscular (injection into muscle) |
| SAMU | French emergency medical services (Service d'Aide Medicale Urgente) |
| PMI | Protection Maternelle et Infantile (French maternal and child health service) |
| INS | French national health identifier |
| IPP | Hospital-specific patient identifier |
| EPDS | Edinburgh Postnatal Depression Scale (screening questionnaire) |
| DMP | Dossier Medical Partage (French shared medical record system) |

---

## Coding Systems You Will See

As a data/IT professional, you need to recognize that different systems use different coding systems to represent the same concepts:

| Coding System | Used By | What It Codes |
|--------------|---------|---------------|
| ICD-10 / CIM-10 | Clinics, Hospitals | Diagnoses (e.g., O14.1 = Severe preeclampsia) |
| CCAM | Clinics, Hospitals | Medical procedures (e.g., JQGA002 = cesarean delivery) |
| NABM | Laboratories | Lab tests (French-specific lab test codes) |
| LOINC | International standard | Lab tests (universal codes) |
| ATC | Pharmacies, Public Health | Medications (e.g., J07AP = Hepatitis B vaccine) |
| FINESS | Insurance/Admin | Healthcare facility identification numbers |
| RPPS | Insurance/Admin | Individual healthcare provider identification numbers |
| GHM / DRG | Hospitals, Insurance | Diagnosis-Related Groups for billing (groups similar cases for payment) |
| INSEE | Government/Admin | Geographic area codes |

**The interoperability problem:** When a lab uses NABM code "5005" for a glucose test and a hospital uses LOINC code "1558-6" for the same test, a computer cannot automatically know these refer to the same thing unless there is a mapping between the two systems.

---

## Your Role in This Exercise

You are NOT expected to:
- Make clinical decisions
- Interpret whether lab results are medically concerning
- Know treatment protocols

You ARE expected to:
- Identify when data is missing, inconsistent, truncated, or incorrectly formatted
- Recognize when two datasets are referring to the same patient, test, or event but using different formats
- Understand the impact of data quality on downstream use (whether clinical, administrative, or financial)
- Propose solutions from a data management, IT systems, or governance perspective
- Think about how standards, policies, and system design could prevent the issues you find
