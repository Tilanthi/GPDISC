"""
Nephrology Domain for GPDISC
Comprehensive renal medicine consultation covering acute kidney injury,
chronic kidney disease, electrolyte disorders, and dialysis.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class NephrologyDomain(BaseDomainModule):
    """
    Nephrology (Renal Medicine) Specialist Domain

    Covers:
    - Acute kidney injury staging and management
    - Chronic kidney disease staging and management
    - Electrolyte disorders (Na+, K+, Ca2+, PO4)
    - Acid-base disorders
    - Proteinuria/hematuria evaluation
    - Hypertension with renal cause
    - Dialysis indications and modalities
    - Transplant considerations
    - Drug dosing in renal impairment
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="nephrology",
            version="1.0.0",
            dependencies=[],
            description="Nephrology: AKI, CKD, electrolyte disorders, acid-base, hypertension, dialysis, transplantation",
            keywords=[
                # Renal conditions
                "kidney", "renal", "nephrology", "nephrologist",
                "acute kidney injury", "aki", "acute renal failure",
                "chronic kidney disease", "ckd", "chronic renal failure",
                "end-stage renal disease", "esrd", "end-stage renal failure",
                "glomerulonephritis", "nephrotic", "nephritic",
                "proteinuria", "albuminuria", "hematuria",

                # Electrolytes
                "sodium", "hyponatremia", "hypernatremia", "na+",
                "potassium", "hypokalemia", "hyperkalemia", "k+",
                "calcium", "hypocalcemia", "hypercalcemia", "ca2+",
                "phosphate", "hypophosphatemia", "hyperphosphatemia", "po4",
                "electrolyte", "electrolytes",

                # Acid-base
                "acidosis", "alkalosis", "metabolic acidosis", "metabolic alkalosis",
                "respiratory acidosis", "respiratory alkalosis",
                "ph", "bicarbonate", "hco3",

                # Renal function
                "creatinine", "egfr", "gfr", "glomerular filtration rate",
                "urea", "bun", "blood urea nitrogen",
                "renal function", "kidney function",

                # Dialysis/transplant
                "dialysis", "hemodialysis", "peritoneal dialysis",
                "transplant", "kidney transplant", "renal transplant",

                # Hypertension
                "renal hypertension", "renovascular", "renal artery stenosis"
            ],
            capabilities=[
                "aki_staging_management",
                "ckd_staging_management",
                "electrolyte_disorder_management",
                "acid_base_interpretation",
                "proteinuria_hematuria_evaluation",
                "renal_hypertension_management",
                "dialysis_assessment",
                "transplant_evaluation",
                "renal_dosing_guidance"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Route nephrology query to appropriate handler"""
        query_lower = query.lower()

        # AKI
        if any(term in query_lower for term in ["aki", "acute kidney injury", "acute renal failure", "arf"]):
            return self._handle_aki(query, context)

        # CKD
        elif any(term in query_lower for term in ["ckd", "chronic kidney disease", "chronic renal failure"]):
            return self._handle_ckd(query, context)

        # Electrolytes
        elif any(term in query_lower for term in ["sodium", "hyponatremia", "hypernatremia", "na+"]):
            return self._handle_sodium(query, context)
        elif any(term in query_lower for term in ["potassium", "hypokalemia", "hyperkalemia", "k+"]):
            return self._handle_potassium(query, context)
        elif any(term in query_lower for term in ["calcium", "hypocalcemia", "hypercalcemia", "ca2+"]):
            return self._handle_calcium(query, context)

        # Acid-base
        elif any(term in query_lower for term in ["acidosis", "alkalosis", "acid-base", "ph", "hco3"]):
            return self._handle_acid_base(query, context)

        # Proteinuria/hematuria
        elif any(term in query_lower for term in ["proteinuria", "albuminuria", "hematuria", "protein in urine", "blood in urine"]):
            return self._handle_proteinuria_hematuria(query, context)

        # Dialysis
        elif "dialysis" in query_lower:
            return self._handle_dialysis(query, context)

        # Transplant
        elif any(term in query_lower for term in ["transplant", "kidney transplant", "renal transplant"]):
            return self._handle_transplant(query, context)

        # Renal function interpretation
        elif any(term in query_lower for term in ["creatinine", "egfr", "gfr", "renal function", "kidney function"]):
            return self._interpret_renal_function(query, context)

        # General nephrology
        else:
            return self._handle_general_nephrology(query, context)

    def _handle_aki(self, query: str, context: dict) -> DomainQueryResult:
        """Handle acute kidney injury queries"""
        answer = """**Acute Kidney Injury (AKI) Assessment**

**Definition:**
- **Acute decline** in renal function (hours to days)
- **Creatinine rise** ≥ 26 µmol/L (0.3 mg/dL) within 48 hours
- **OR** creatinine rise ≥ 1.5x baseline within 7 days
- **OR** urine output < 0.5 mL/kg/hour for 6 hours

**KDIGO Staging:**

| Stage | Creatinine Criteria | Urine Output Criteria |
|-------|-------------------|----------------------|
| **Stage 1** | Creatinine ↑ 1.5-1.9x baseline OR ↑ 26-52 µmol/L (0.3-0.5 mg/dL) | < 0.5 mL/kg/hour for 6-12 hours |
| **Stage 2** | Creatinine ↑ 2.0-2.9x baseline | < 0.5 mL/kg/hour for ≥ 12 hours |
| **Stage 3** | Creatinine ↑ 3.0x baseline OR ↑ ≥ 354 µmol/L (4.0 mg/dL) OR initiation of RRT | < 0.3 mL/kg/hour for ≥ 24 hours OR anuria for 12 hours |

**Etiology (Prerenal, Intrinsic, Postrenal):**

**Prerenal (40-50%):**
- **Decreased renal perfusion** (most common, reversible)
- **Causes:**
  - **Hypovolemia:** Dehydration, hemorrhage, diarrhea, vomiting
  - **Decreased cardiac output:** Heart failure, arrhythmias
  - **Sepsis** (vasodilation, hypotension)
  - **Medications:** ACE inhibitors, ARBs, NSAIDs, diuretics
- **Findings:**
  - **High urine osmolality** (> 500 mOsm/kg)
  - **High urine sodium** (< 20 mmol/L - kidney reabsorbing sodium)
  - **High BUN:Creatinine ratio** (> 20:1)
  - **Muddy brown casts** (if ATN)

**Intrinsic (30-40%):**
- **Structural damage** to kidney parenchyma
- **Causes:**
  - **Acute tubular necrosis (ATN):** Ischemia, nephrotoxins (contrast, aminoglycosides, cisplatin, myoglobin)
  - **Glomerulonephritis:** Nephritic syndrome (hematuria, proteinuria, RBC casts)
  - **Interstitial nephritis:** Allergic (antibiotics, PPIs, NSAIDs)
  - **Vasculitis:** GPA, MPA, TTP, HUS
  - **Multiple myeloma** (light chains)
- **Findings:**
  - **Muddy brown casts** (ATN)
  - **RBC casts** (glomerulonephritis)
  - **WBC casts, eosinophils** (interstitial nephritis)

**Postrenal (5-10%):**
- **Urinary tract obstruction**
- **Causes:**
  - **BPH**, prostate cancer (most common in men)
  - **Nephrolithiasis** (bilateral or solitary kidney)
  - **Tumors**, **strictures**, **blood clots**
  - **Neurogenic bladder**
- **Findings:**
  - **Anuria** (no urine output)
  - **Hydronephrosis** on ultrasound
  - **Post-void residual** > 100 mL (bladder scan)

**Evaluation:**

**History:**
- **Medications:** NSAIDs, ACE inhibitors, ARBs, diuretics, antibiotics, contrast
- **Comorbidities:** CKD, diabetes, hypertension, heart failure, liver disease
- **Symptoms:** Volume status (dehydrated vs. fluid overloaded), dysuria, flank pain

**Physical Examination:**
- **Volume assessment:** JVP, edema, lung crackles, orthostatic vitals
- **Bladder:** Suprapubic fullness (palpable bladder)
- **Skin:** Rash (vasculitis), petechiae (TTP)

**Laboratory:**
- **Creatinine**, **BUN**, **electrolytes**, **bicarbonate**, **phosphate**, **calcium**
- **CBC** (anemia, thrombocytopenia)
- **Urinalysis** (casts, protein, RBC, WBC)
- **Urine electrolytes:** Na+, creatinine, osmolality (distinguish prerenal vs. ATN)

**Imaging:**
- **Renal ultrasound** (rule out obstruction, assess kidney size)
- **CT abdomen** (if obstruction suspected, ultrasound equivocal)

**Management:**

**Prerenal AKI:**
- **Volume repletion** (IV crystalloids: LR or NS)
- **Discontinue/adjust:** ACE inhibitors, ARBs, NSAIDs, diuretics
- **Treat underlying cause:** Sepsis (antibiotics), heart failure (diuretics, inotropes)

**Intrinsic AKI:**
- **ATN:** Supportive care, avoid nephrotoxins, consider RRT if severe
- **Glomerulonephritis:** Urgent renal biopsy, steroids ± cyclophosphamide
- **Interstitial nephritis:** Discontinue offending drug, consider steroids
- **Myeloma kidney:** Hydration, chemotherapy, consider plasmapheresis

**Postrenal AKI:**
- **Relieve obstruction:**
  - **Foley catheter** (bladder outlet obstruction)
  - **Nephrostomy tube** (ureteral obstruction)
  - **Urology consult** (definitive management)

**General Measures:**
- **Avoid nephrotoxins:** NSAIDs, iodinated contrast, aminoglycosides
- **Medication adjustment:** Reduce dose/interval for renal impairment
- **Nutrition:** Adequate calories (20-30 kcal/kg/day), restrict protein if not on dialysis (0.8 g/kg/day)
- **Electrolyte management:**
  - **Hyperkalemia:** Calcium gluconate, insulin/dextrose, salbutamol, dialysis if severe
  - **Metabolic acidosis:** Sodium bicarbonate if severe (< 7.1 or bicarbonate < 12)
  - **Hyperphosphatemia:** Phosphate binders (sevelamer, calcium acetate)
  - **Hypocalcemia:** Calcium gluconate (if symptomatic)

**Dialysis Indications:**
- **Refractory hyperkalemia** (> 6.5 mmol/L despite medical management)
- **Refractory metabolic acidosis** (pH < 7.1)
- **Volume overload** (pulmonary edema not responding to diuretics)
- **Uremic symptoms** (pericarditis, encephalopathy, bleeding)
- **Severe AKI** (Stage 3, anuria, creatinine > 350 µmol/L)

**Prognosis:**
- **Mortality:** 20-50% (hospitalized patients, higher in ICU)
- **Recovery:** Most recover renal function (except if irreversible damage)
- **Risk of progression to CKD:** 10-20%

**Sources:** KDIGO 2024, NICE NG203, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "nephrology",
                "focus": "aki_management",
                "sources": ["KDIGO 2024", "NICE NG203", "RCP 2024"]
            }
        )

    def _handle_ckd(self, query: str, context: dict) -> DomainQueryResult:
        """Handle chronic kidney disease queries"""
        answer = """**Chronic Kidney Disease (CKD) Management**

**Definition:**
- **Abnormal renal function** (eGFR < 60 mL/min/1.73m²) OR **structural damage** (proteinuria, hematuria)
- **Duration > 3 months** (distinguish from AKI)

**KDIGO Staging:**

| Stage | eGFR (mL/min/1.73m²) | Description | Action |
|-------|----------------------|-------------|---------|
| **G1** | ≥ 90 | Normal/high | Monitor if proteinuria present |
| **G2** | 60-89 | Mildly decreased | Monitor if proteinuria present |
| **G3a** | 45-59 | Mild-moderate decreased | Monitor, CV risk reduction |
| **G3b** | 30-44 | Moderate-severe decreased | Monitor, consider referral |
| **G4** | 15-29 | Severely decreased | Refer to nephrology |
| **G5** | < 15 | Kidney failure | Prepare for RRT |

**Proteinuria Albuminuria Staging:**

| Category | ACR (mg/g) | ACR (mg/mmol) |
|----------|------------|---------------|
| **A1** | < 30 | < 3 | Normal/mildly increased |
| **A2** | 30-300 | 3-30 | Moderately increased |
| **A3** | > 300 | > 30 | Severely increased |

**Risk Stratification (Combine G + A categories):**
- **Low risk:** G1-2 + A1-2
- **Moderately increased risk:** G1-2 + A3, G3a + A1-2
- **High risk:** G3a + A3, G3b + A1-3
- **Very high risk:** G4 + A1-3, G5 + A1-3

**Etiology:**

**Common Causes (90%):**
- **Diabetes** (40-50%) - diabetic nephropathy
- **Hypertension** (25-30%) - hypertensive nephrosclerosis
- **Glomerulonephritis** (10-15%)
- **Polycystic kidney disease** (5-10%)
- **Other:** Obstructive uropathy, reflux nephropathy, analgesic nephropathy

**Evaluation:**

**History:**
- **CKD risk factors:** Diabetes, hypertension, cardiovascular disease, family history
- **Medications:** NSAIDs, aminoglycosides, contrast, ACE inhibitors, ARBs
- **Symptoms:** Fatigue, nausea, pruritus, edema, nocturia

**Physical Examination:**
- **Blood pressure** (hypertension common)
- **Edema** (periorbital, peripheral)
- **Fundoscopy** (hypertensive retinopathy, diabetic retinopathy)
- **Abdominal** (polycystic kidneys - enlarged, irregular)

**Laboratory:**
- **Creatinine**, **eGFR**, **BUN**, **electrolytes**
- **Urinalysis** (protein, RBC, WBC, casts)
- **Urine ACR** (albumin-to-creatinine ratio - quantifies proteinuria)
- **CBC** (anemia, thrombocytopenia)
- **Calcium**, **phosphate**, **PTH**, **alkaline phosphatase** (bone mineral disease)
- **HbA1c** (if diabetes)

**Imaging:**
- **Renal ultrasound** (kidney size, cysts, obstruction)
- **Kidney size:**
  - **Normal:** 10-12 cm
  - **< 9 cm:** Suggests chronic disease (small kidneys)
  - **Asymmetry:** Suggests renovascular disease, reflux

**Management:**

**Blood Pressure Control:**
- **Target:** < 140/90 mmHg (most patients)
- **Target:** < 130/80 mmHg (if proteinuria A2-3)
- **First-line:**
  - **ACE inhibitors** (ramipril, perindopril) OR **ARBs** (losartan, candesartan)
  - **Mechanism:** Reduce intraglomerular pressure, reduce proteinuria
- **Add if needed:** Calcium channel blockers, diuretics, beta-blockers
- **Avoid:** ACE inhibitors + ARBs together (increased AKI risk)

**Proteinuria Reduction:**
- **ACE inhibitors/ARBs** (reduce proteinuria by 30-50%)
- **SGLT2 inhibitors** (dapagliflozin, empagliflozin) - slow CKD progression
- **Target ACR:** < 30 mg/g (or reduce by > 50% if cannot achieve < 30)

**Diabetes Management:**
- **Target HbA1c:** 48-53 mmol/mol (6.5-7.0%)
- **SGLT2 inhibitors:** (dapagliflozin, empagliflozin) - renal and cardiovascular benefits
- **GLP-1 agonists:** (semaglutide, liraglutide) - cardiovascular benefits

**Cardiovascular Risk Reduction:**
- **Statin:** Atorvastatin 20 mg (if eGFR > 30) or 40-80 mg (if eGFR 30-60)
- **Antiplatelet:** Aspirin 75 mg (if high CV risk, low bleeding risk)
- **Smoking cessation**

**Complications Management:**

**Anemia:**
- **Mechanism:** Decreased erythropoietin production (kidney)
- **Target Hb:** 100-120 g/L (avoid > 130 g/L - increased thrombosis risk)
- **Treatment:**
  - **Iron supplementation** (IV iron if ferritin < 100 µg/L or TSAT < 20%)
  - **ESA** (erythropoiesis-stimulating agent: epoetin, darbepoetin) if Hb < 100 g/L despite iron repletion

**CKD-MBD (Chronic Kidney Disease-Mineral and Bone Disorder):**
- **Biochemical targets:**
  - **Calcium:** 2.1-2.5 mmol/L (corrected)
  - **Phosphate:** 0.9-1.5 mmol/L
  - **PTH:** 2-9x upper limit of normal
  - **Alkaline phosphatase:** Normal range
- **Treatment:**
  - **Phosphate binders** (sevelamer, calcium acetate, lanthanum)
  - **Vitamin D analogs** (calcitriol, alfacalcidol) if PTH elevated
  - **Cinacalcet** (calcimimetic) if PTH refractory to vitamin D

**Metabolic Acidosis:**
- **Target:** Bicarbonate ≥ 22 mmol/L
- **Treatment:** Sodium bicarbonate 600 mg TID-QDS (titrate)

**Hyperkalemia:**
- **Avoid:** ACE inhibitors, ARBs (if severe)
- **Dietary:** Low-potassium diet
- **Binders:** Sodium zirconium cyclosilicate, patiromer

**Referral Criteria:**
- **eGFR < 30** (Stage G4)
- **Proteinuria ACR > 300** (A3)
- **Rapid decline** in eGFR (> 5 mL/min/1.73m²/year)
- **Uncontrolled hypertension** despite 3+ antihypertensives
- **Uncertain diagnosis** (needs renal biopsy)

**Dialysis Preparation (eGFR < 15-20):**
- **Education:** RRT options (hemodialysis, peritoneal dialysis, transplant)
- **Access creation:** AV fistula (hemodialysis) 6-12 months before needed
- **Transplant evaluation:** Refer early (ideal: eGFR 20-25)

**Prognosis:**
- **Progression to ESRD:** Variable (depends on etiology, proteinuria, BP control)
- **Cardiovascular disease:** Leading cause of death (10-20x increased risk)
- **Mortality:** Higher with lower eGFR, higher proteinuria

**Sources:** KDIGO 2024, NICE NG203, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "nephrology",
                "focus": "ckd_management",
                "sources": ["KDIGO 2024", "NICE NG203", "RCP 2024"]
            }
        )

    def _handle_sodium(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sodium disorders"""
        answer = """**Sodium Disorders Management**

**Normal Sodium:** 135-145 mmol/L

**Hyponatremia (Na+ < 135 mmol/L):**

**Severity:**
- **Mild:** 130-135 mmol/L
- **Moderate:** 125-129 mmol/L
- **Severe:** < 125 mmol/L

**Classification by Volume Status:**

**1. Hypovolemic Hyponatremia (Decreased total body sodium):**
- **Causes:**
  - **GI losses:** Vomiting, diarrhea, nasogastric suction
  - **Renal losses:** Diuretics (thiazides), salt-wasting nephropathy, adrenal insufficiency
  - **Third spacing:** Burns, pancreatitis, intestinal obstruction
- **Findings:** Dry mucous membranes, decreased skin turgor, orthostatic hypotension, low JVP
- **Urine Na+:** > 20 mmol/L (renal loss), < 20 mmol/L (extrarenal loss)

**2. Euvolemic Hyponatremia (Normal total body sodium):**
- **Causes:**
  - **SIADH** (syndrome of inappropriate ADH): Malignancy, CNS disorders, pneumonia, medications (SSRIs, carbamazepine)
  - **Hypothyroidism**
  - **Primary polydipsia** (psychogenic water drinking)
- **Findings:** No signs of hypervolemia or hypovolemia
- **Urine Na+:** > 20 mmol/L (SIADH), < 20 mmol/L (primary polydipsia)

**3. Hypervolemic Hyponatremia (Increased total body sodium):**
- **Causes:**
  - **Heart failure** (most common)
  - **Cirrhosis**
  - **Nephrotic syndrome**
- **Findings:** Edema, ascites, elevated JVP
- **Urine Na+:** < 20 mmol/L (kidney reabsorbing sodium)

**Acute vs Chronic:**
- **Acute:** < 48 hours (high risk of cerebral edema)
- **Chronic:** > 48 hours (brain adapts, lower risk)

**Treatment:**

**Symptomatic Hyponatremia (Seizures, coma):**
- **3% hypertonic saline:** 150 mL IV over 20 minutes (repeat if needed)
- **Target:** Increase Na+ by 5 mmol/L rapidly (symptom relief)
- **Furosemide** 20-40 mg IV (if hypervolemic)

**Asymptomatic Hyponatremia:**

**Hypovolemic:**
- **Isotonic saline (0.9% NaCl):** Correct volume depletion, sodium will correct

**Euvolemic:**
- **Fluid restriction:** < 1 L/day (SIADH)
- **Demeclocycline:** 300-600 mg daily (if fluid restriction ineffective)
- **Tolvaptan** (V2 receptor antagonist): Consider if refractory

**Hypervolemic:**
- **Fluid restriction** (< 1 L/day)
- **Loop diuretic** (furosemide) to remove excess fluid
- **Salt restriction** (< 2 g/day)

**Rate of Correction:**
- **Acute:** Can correct rapidly (< 1-2 mmol/L/hour)
- **Chronic:** **SLOW correction** (< 8-10 mmol/L in 24 hours)
- **Risks of rapid correction:** **Osmotic demyelination syndrome** (central pontine myelinolysis) - irreversible neurological injury

**Hypernatremia (Na+ > 145 mmol/L):**

**Etiology:**
- **Net water loss:** Inadequate intake, diarrhea, osmotic diuresis (hyperglycemia, mannitol)
- **Sodium gain:** Salt tablets, hypertonic saline, hyperaldosteronism
- **Diabetes insipidus** (central or nephrogenic)

**Clinical Features:**
- **Symptoms:** Lethargy, seizures, coma (severe: > 160 mmol/L)
- **Signs:** Dry mucous membranes, decreased skin turgor, hypotension

**Treatment:**

**Calculate water deficit:**
- **Water deficit (L)** = 0.6 × weight (kg) × [(Na+/140) - 1]

**Management:**
- **Hypovolemic:** Isotonic saline (0.9% NaCl) first, then hypotonic fluids (0.45% NaCl or D5W)
- **Euvolemic:** Hypotonic fluids (0.45% NaCl or D5W)
- **Diabetes insipidus:** Desmopressin (DDAVP) if central

**Rate of Correction:**
- **Chronic hypernatremia:** **SLOW** (< 0.5 mmol/L/hour, < 10 mmol/L/day)
- **Acute hypernatremia:** Can correct faster

**Sources:** NICE NG182, European Clinical Practice Guidelines 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "nephrology_electrolytes",
                "focus": "sodium_disorders",
                "sources": ["NICE NG182", "ECPG 2024"]
            }
        )

    def _handle_potassium(self, query: str, context: dict) -> DomainQueryResult:
        """Handle potassium disorders"""
        answer = """**Potassium Disorders Management**

**Normal Potassium:** 3.5-5.0 mmol/L

**Hyperkalemia (K+ > 5.0 mmol/L):**

**Severity:**
- **Mild:** 5.0-5.9 mmol/L
- **Moderate:** 6.0-6.4 mmol/L
- **Severe:** ≥ 6.5 mmol/L

**Etiology:**
- **Decreased excretion (most common):**
  - **CKD** (decreased GFR)
  - **Medications:** ACE inhibitors, ARBs, spironolactone, NSAIDs, trimethoprim
  - **Hyporeninemic hypoaldosteronism** (diabetes)
- **Shift out of cells:**
  - **Acidosis** (H+ moves into cells, K+ moves out)
  - **Insulin deficiency** (DKA)
  - **Beta-blockers**, **digoxin toxicity**
  - **Cell lysis:** Rhabdomyolysis, tumor lysis syndrome, massive transfusion
- **Increased intake:**
  - **IV potassium** (iatrogenic)
  - **Salt substitutes** (KCl)
  - **Fruits** (bananas, avocados, dried fruits) - rarely sole cause

**Clinical Features:**
- **Muscle weakness**, flaccid paralysis
- **Palpitations**, **cardiac arrhythmias**
- **ECG changes:** (progressive with increasing K+)
  - **5.5-6.5:** Peaked T waves
  - **6.5-7.5:** Prolonged PR interval, flattened P waves, QRS widening
  - **> 7.5:** Sine wave pattern, asystole, ventricular fibrillation

**Treatment (Based on Severity):**

**Mild Hyperkalemia (5.0-5.9 mmol/L):**
- **Review medications:** Stop/reduce ACE inhibitors, ARBs, spironolactone
- **Dietary:** Low-potassium diet
- **Loop diuretic:** Furosemide 20-40 mg IV/PO (if volume overloaded)

**Moderate Hyperkalemia (6.0-6.4 mmol/L):**
- **All of above PLUS:**
- **Calcium gluconate 10%** 10 mL IV over 10 minutes (stabilizes cardiac membrane, does NOT lower potassium)
- **Insulin/dextrose:** 10 units regular insulin + 25 g dextrose (50 mL D50W) IV (shifts K+ into cells, onset 15-30 min, duration 4-6 hours)
- **Salbutamol:** 10-20 mg nebulized (shifts K+ into cells, additive to insulin)

**Severe Hyperkalemia (≥ 6.5 mmol/L) OR ECG Changes:**
- **ALL of above PLUS:**
- **Emergency dialysis** (if refractory to medical management)
- **Sodium zirconium cyclosilicate** or **patiromer** (potassium binders)

**Hypokalemia (K+ < 3.5 mmol/L):**

**Severity:**
- **Mild:** 3.0-3.4 mmol/L
- **Moderate:** 2.5-2.9 mmol/L
- **Severe:** < 2.5 mmol/L

**Etiology:**
- **Increased losses:**
  - **GI losses:** Vomiting, diarrhea (most common)
  - **Renal losses:** Diuretics (loop, thiazides), hyperaldosteronism, renal tubular acidosis, magnesium depletion
- **Shift into cells:**
  - **Alkalosis**
  - **Insulin therapy** (DKA treatment)
  - **Beta-agonists** (salbutamol, albuterol)
- **Decreased intake:** Malnutrition, alcoholism

**Clinical Features:**
- **Muscle weakness**, cramps, paralysis
- **Ileus**, constipation
- **Cardiac arrhythmias**
- **ECG changes:** Flattened T waves, U waves, ST depression, prolonged QT

**Treatment:**

**Mild Hypokalemia (3.0-3.4 mmol/L):**
- **Oral potassium:** KCl 20-40 mmol daily (divided doses)
- **Correct magnesium** (if low)

**Moderate-Severe Hypokalemia (< 3.0 mmol/L):**
- **IV potassium:** KCl in saline (NOT dextrose - dextrose stimulates insulin, shifts K+ into cells)
- **Maximum rate:** 10 mmol/hour (unless cardiac monitoring)
- **Maximum concentration:** 40 mmol/L (via peripheral line)
- **Goal:** K+ > 4.0 mmol/L (especially if on digoxin)

**Correct Underlying Cause:**
- **Stop/reduce diuretics** (if possible)
- **Treat vomiting/diarrhea**
- **Correct magnesium** (hypomagnesemia causes refractory hypokalemia)

**Monitoring:**
- **ECG** (if severe hyperkalemia or hypokalemia)
- **Repeat potassium** (1-2 hours after IV, 4-6 hours after oral)
- **Renal function** (eGFR affects potassium excretion)

**Sources:** NICE NG182, UpToDate 2024, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "nephrology_electrolytes",
                "focus": "potassium_disorders",
                "sources": ["NICE NG182", "UpToDate 2024", "RCP 2024"]
            }
        )

    def _handle_calcium(self, query: str, context: dict) -> DomainQueryResult:
        """Handle calcium disorders"""
        answer = """**Calcium Disorders Management**

**Corrected Calcium:** 2.1-2.5 mmol/L (8.4-10.2 mg/dL)

**Correction Formula (for low albumin):**
- **Corrected Ca** = Measured Ca + 0.02 × (40 - albumin [g/L])

**Hypercalcemia (Corrected Ca > 2.5 mmol/L):**

**Etiology:**
- **Primary hyperparathyroidism** (most common outpatient)
- **Malignancy** (most common inpatient - PTHrP, bone metastases)
- **Medications:** Thiazides, lithium, vitamin D intoxication
- **Granulomatous disease:** Sarcoidosis, TB (increased 1,25-OH vitamin D)
- **Immobilization**

**Clinical Features:**
- **"Stones, bones, groans, thrones":**
  - **Stones:** Nephrolithiasis (kidney stones)
  - **Bones:** Bone pain, osteopenia, osteoporosis
  - **Groans:** Abdominal pain, constipation, nausea, vomiting
  - **Thrones:** Depression, fatigue, cognitive impairment
- **Severe:** Coma, cardiac arrest

**Treatment (Based on Severity):**

**Asymptomatic, Mild (Ca 2.5-3.0 mmol/L):**
- **Hydration:** 2-3 L/day
- **Avoid:** Thiazides, lithium
- **Treat underlying cause**

**Symptomatic or Moderate-Severe (Ca > 3.0 mmol/L):**

**Immediate Measures:**
- **IV hydration:** 2-4 L/day NS or LR (reverses volume depletion, increases calcium excretion)
- **Loop diuretic:** Furosemide 20-40 mg IV q6-8h (after volume replete - increases calcium excretion)
- **Avoid:** Thiazide diureptics (increase calcium)

**Specific Therapy (if persistent, symptomatic):**

**Primary Hyperparathyroidism:**
- **Parathyroidectomy** (definitive, curative)
- **Cinacalcet** (calcimimetic, lowers calcium, PTH) - if not surgical candidate

**Malignancy-Associated:**
- **Bisphosphonates:** Zoledronic acid 4 mg IV (single dose, onset 1-2 days, duration 2-4 weeks)
- **Denosumab:** 120 mg SC weekly (if bisphosphonate contraindicated)
- **Glucocorticoids:** Prednisone 20-40 mg daily (if granulomatous disease, lymphoma)
- **Treat underlying malignancy**

**Hypocalcemia (Corrected Ca < 2.1 mmol/L):**

**Etiology:**
- **Hypoparathyroidism** (post-thyroidectomy, autoimmune)
- **Vitamin D deficiency**
- **CKD** (decreased 1-alpha-hydroxylation of vitamin D)
- **Medications:** Cinacalcet, bisphosphonates, citrate (blood products)
- **Pancreatitis**, **rhabdomyolysis** (saponification of calcium)

**Clinical Features:**
- **Neuromuscular irritability:** Tetany, perioral numbness, carpopedal spasm
- **Trousseau's sign** (carpal spasm after BP cuff inflation)
- **Chvostek's sign** (facial muscle spasm after tapping facial nerve)
- **Seizures**, laryngospasm, bronchospasm

**Treatment:**

**Acute, Symptomatic Hypocalcemia:**
- **IV calcium gluconate 10%:** 10-20 mL over 10 minutes (followed by continuous infusion)
- **IV calcium chloride 10%:** More irritating, use if central line
- **Oral calcium + vitamin D** (once stable)

**Chronic Hypocalcemia:**

**Calcium Supplements:**
- **Calcium carbonate:** 500-1000 mg TID-QDS (take with food)
- **Calcium citrate:** If on PPIs (better absorption without acid)

**Active Vitamin D (Calcitriol):**
- **Calcitriol** (1,25-dihydroxyvitamin D): 0.25-0.5 mcg BID
- **Alfacalcidol:** 0.5-1.0 mcg daily
- **NOT regular vitamin D** (ineffective in hypoparathyroidism)

**Hypoparathyroidism:**
- **Add thiazide diuretic** (decreases urinary calcium loss)
- **Low-salt diet** (reduces calcium excretion)
- **Monitor:** Urinary calcium (watch for hypercalciuria → nephrolithiasis)

**Sources:** NICE NG132, UpToDate 2024, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "nephrology_electrolytes",
                "focus": "calcium_disorders",
                "sources": ["NICE NG132", "UpToDate 2024", "RCP 2024"]
            }
        )

    def _handle_acid_base(self, query: str, context: dict) -> DomainQueryResult:
        """Handle acid-base disorders"""
        answer = """**Acid-Base Disorders Interpretation**

**Normal Values:**
- **pH:** 7.35-7.45
- **PaCO2:** 35-45 mmHg (4.6-6.0 kPa)
- **HCO3-:** 22-26 mmol/L
- **Base Excess (BE):** -2 to +2

**Stepwise Approach:**

**Step 1: Assess pH**
- **pH < 7.35:** Acidosis
- **pH > 7.45:** Alkalosis
- **pH 7.35-7.45:** Normal (or fully compensated)

**Step 2: Assess Primary Process (PaCO2 or HCO3-)**

**Respiratory Acidosis (High PaCO2):**
- **Primary:** ↑ PaCO2 (alveolar hypoventilation)
- **Compensation:** ↑ HCO3- (renal)

**Respiratory Alkalosis (Low PaCO2):**
- **Primary:** ↓ PaCO2 (alveolar hyperventilation)
- **Compensation:** ↓ HCO3- (renal)

**Metabolic Acidosis (Low HCO3-):**
- **Primary:** ↓ HCO3-
- **Compensation:** ↓ PaCO2 (respiratory)

**Metabolic Alkalosis (High HCO3-):**
- **Primary:** ↑ HCO3-
- **Compensation:** ↑ PaCO2 (respiratory)

**Step 3: Assess Compensation (Winter's Formula)**

**Expected PaCO2 for Metabolic Acidosis:**
- **Winter's Formula:** Expected PaCO2 = (1.5 × HCO3-) + 8 ± 2
- **If PaCO2 > expected:** Additional respiratory acidosis
- **If PaCO2 < expected:** Additional respiratory alkalosis

**Expected PaCO2 for Metabolic Alkalosis:**
- **Expected PaCO2 = 40 + (0.7 × HCO3- increase) ± 2**
- **If PaCO2 > expected:** Additional respiratory acidosis
- **If PaCO2 < expected:** Additional respiratory alkalosis

**Step 4: Calculate Anion Gap (if metabolic acidosis)**

**Anion Gap = Na+ - (Cl- + HCO3-)**

**Normal Anion Gap:** 8-12 mmol/L (adjusted for albumin)
- **Albumin correction:** Add 2.5 to gap for every 1 g/dL albumin < 4.0

**High Anion Gap Metabolic Acidosis (HAGMA) (> 12):**
- **Causes:** MUDPILES
  - **M:** Methanol, Metformin
  - **U:** Uremia (CKD)
  - **D:** DKA, alcoholic ketoacidosis
  - **P:** Paraldehyde, Phenformin (rare)
  - **I:** INH, Iron, Isoniazid
  - **L:** Lactic acidosis
  - **E:** Ethanol, Ethylene glycol
  - **S:** Salicylates, Starvation

**Normal Anion Gap Metabolic Acidosis (NAGMA):**
- **Causes:** GI loss (diarrhea), Renal loss (RTA type 1, 2, 4), Carbonic anhydrase inhibitors

**Delta-Delta (if HAGMA):**
- **Δ Anion Gap = Anion Gap - 12**
- **Δ Bicarbonate = 24 - HCO3-**
- **If Δ Gap = Δ Bicarbonate:** Pure HAGMA
- **If Δ Gap > Δ Bicarbonate:** HAGMA + metabolic alkalosis (or respiratory acidosis)
- **If Δ Gap < Δ Bicarbonate:** HAGMA + NAGMA (or respiratory alkalosis)

**Mixed Disorders:**

**Respiratory Acidosis + Metabolic Alkalosis:**
- **Causes:** COPD + diuretic use, mechanical ventilation with NG suction

**Respiratory Alkalosis + Metabolic Acidosis:**
- **Causes:** Sepsis (lactic acidosis + hyperventilation), salicylate poisoning

**Triple Acid-Base Disorder:**
- **Respiratory acidosis + HAGMA + metabolic alkalosis**
- **Example:** COPD (respiratory acidosis) + DKA (HAGMA) + diuretic use (metabolic alkalosis)

**Common Clinical Scenarios:**

**Diabetic Ketoacidosis (DKA):**
- **HAGMA** (ketones) + **respiratory alkalosis** (Kussmaul respirations)

**Sepsis:**
- **Lactic acidosis** (HAGMA) + **respiratory alkalosis** (hyperventilation)

**COPD Exacerbation:**
- **Respiratory acidosis** (CO2 retention) + **compensated metabolic alkalosis** (elevated HCO3-)

**Diarrhea:**
- **NAGMA** (bicarbonate loss in stool) + **respiratory alkalosis** (hyperventilation due to volume depletion)

**Vomiting:**
- **Metabolic alkalosis** (acid loss) + **respiratory acidosis** (hypoventilation due to hypokalemia)

**Sources:** NICE NG204, UpToDate 2024, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "nephrology_acidbase",
                "focus": "acid_base_interpretation",
                "sources": ["NICE NG204", "UpToDate 2024", "RCP 2024"]
            }
        )

    def _handle_proteinuria_hematuria(self, query: str, context: dict) -> DomainQueryResult:
        """Handle proteinuria and hematuria"""
        answer = """**Proteinuria and Hematuria Evaluation**

**Proteinuria:**

**Definition:**
- **Normal:** < 150 mg/day (or ACR < 3 mg/mmol, < 30 mg/g)
- **Microalbuminuria:** ACR 3-30 mg/mmol (30-300 mg/g)
- **Macroproteinuria:** ACR > 30 mg/mmol (> 300 mg/g)

**Etiology:**

**Transient (Benign):**
- **Fever**, **exercise**, **heat exposure**, **emotional stress**
- **Orthostatic:** Proteinuria only when upright (common in young adults)

**Persistent (Pathological):**

**Glomerular (Nephrotic-range proteinuria > 3 g/day):**
- **Nephrotic syndrome:** Heavy proteinuria (> 3.5 g/day), hypoalbuminemia, edema, hyperlipidemia
- **Causes:** Minimal change disease, FSGS, membranous nephropathy, diabetic nephropathy

**Tubulointerstitial:**
- **Causes:** Pyelonephritis, interstitial nephritis, heavy metals (lead, cadmium)

**Overflow:**
- **Causes:** Multiple myeloma (Bence Jones proteinuria), rhabdomyolysis (myoglobin)

**Evaluation:**

**Urinalysis:**
- **Dipstick:** Detects albumin (semi-quantitative: trace, 1+, 2+, 3+)
- **Microscopy:** Casts (white cell casts, granular casts), RBCs

**Urine ACR (Albumin-to-Creatinine Ratio):**
- **First-morning urine** preferred
- **Quantifies proteinuria** (more accurate than dipstick)
- **Staging CKD:** A1 (< 3), A2 (3-30), A3 (> 30)

**24-Hour Urine Collection:**
- **Total protein** (if non-albumin proteinuria suspected)
- **Creatinine clearance** (if eGFR unreliable)

**Serum Studies:**
- **Creatinine**, **eGFR** (renal function)
- **Albumin** (nephrotic syndrome if < 30 g/L)
- **Lipids** (elevated in nephrotic syndrome)
- **Serum protein electrophoresis** (if multiple myeloma suspected)
- **ANCA**, **anti-GBM**, **ANA**, **complement C3/C4** (if glomerulonephritis suspected)

**Renal Biopsy:**
- **Indications:**
  - Nephrotic syndrome (adults - determine specific glomerular disease)
  - Unexplained CKD with active urine sediment
  - Rapidly progressive GN (crescentic GN)
  - Systemic disease with renal involvement (SLE, vasculitis)

**Treatment:**
- **ACE inhibitors/ARBs** (reduce proteinuria, slow progression)
- **SGLT2 inhibitors** (reduce proteinuria, slow CKD progression)
- **Disease-specific:** Steroids ± cyclophosphamide (GN), immunosuppression (SLE), chemotherapy (myeloma)

---

**Hematuria:**

**Definition:**
- **Microscopic:** > 3 RBC/hpf (urine microscopy)
- **Macroscopic (Gross):** Visible blood in urine
- **Dipstick:** Detects hemoglobin (positive in hematuria, myoglobinuria, hemoglobinuria)

**Etiology:**

**Glomerular (Dysmorphic RBCs, RBC casts):**
- **IgA nephropathy** (most common)
- **Alport syndrome** (hereditary nephritis)
- **Post-infectious GN**

**Non-Glomerular (Isomorphic RBCs, no casts):**

**Medical:**
- **UTI**, **pyelonephritis**
- **Kidney stones**
- **BPH** (prostatic enlargement)
- **Trauma**
- **Exercise-induced hematuria**

**Malignancy:**
- **Renal cell carcinoma**
- **Transitional cell carcinoma** (bladder, ureter, renal pelvis)
- **Prostate cancer**

**Evaluation:**

**History:**
- **Associated symptoms:** Dysuria, frequency, flank pain (UTI, stones)
- **Macroscopic vs microscopic:** Macroscopic higher risk of malignancy
- **Age:** > 50 (higher risk of malignancy)
- **Smoking** (bladder cancer risk)
- **Family history** of renal disease
- **Medications:** Anticoagulants (may unmask but not cause hematuria)

**Physical Examination:**
- **Abdominal** (mass, tenderness)
- **Genitourinary** (prostate exam)

**Laboratory:**
- **Urinalysis** (RBCs, WBCs, nitrites, leukocyte esterase, casts)
- **Urine cytology** (if high risk for bladder cancer)
- **PSA** (if > 50, prostate evaluation)

**Imaging:**
- **CT urogram** (gold standard - detects stones, tumors)
- **Renal ultrasound** (if CT contraindicated)
- **Cystoscopy** (if high risk for bladder cancer: age > 50, smoking, macroscopic hematuria)

**Red Flags (Urgent Referral):**
- **Macroscopic hematuria** (especially if persistent, > 50 years old, smoker)
- **Clots** in urine
- **Abdominal mass**, flank pain
- **Unexplained weight loss**

**Sources:** NICE NG203, UpToDate 2024, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "nephrology",
                "focus": "proteinuria_hematuria",
                "sources": ["NICE NG203", "UpToDate 2024", "RCP 2024"]
            }
        )

    def _handle_dialysis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle dialysis queries"""
        answer = """**Dialysis Assessment and Modality Selection**

**Indications for Dialysis:**

**Absolute Indications (Emergent):**
- **Refractory hyperkalemia** (> 6.5 mmol/L despite medical management)
- **Refractory metabolic acidosis** (pH < 7.1 despite bicarbonate)
- **Volume overload** with pulmonary edema not responding to diuretics
- **Uremic complications:**
  - **Pericarditis** (rub, effusion)
  - **Encephalopathy** (confusion, seizures, coma)
  - **Bleeding diathesis** (platelet dysfunction)
  - **Uremic frost** (rare)

**Relative Indications (Elective):**
- **Symptomatic uremia:** Nausea, vomiting, pruritus, fatigue, anorexia, weight loss
- **Malnutrition** (unintentional weight loss, albumin < 30 g/L)
- **eGFR < 5-10 mL/min/1.73m²** (if no symptoms)
- **Preparing for transplant** (living donor identified)

**Dialysis Modalities:**

**1. Hemodialysis (HD):**

**Description:**
- **Extracorporeal** blood filtration (outside body)
- **Vascular access:** AV fistula (surgically created), AV graft, central venous catheter
- **Schedule:** 3 times/week (4 hours/session) - in-center

**Advantages:**
- **Rapid correction** of electrolytes, volume, toxins
- **Staff-monitored** (trained nurses/technicians)
- **No home equipment** needed

**Disadvantages:**
- **Vascular access** complications (infection, stenosis, thrombosis)
- **Hemodynamic instability** (hypotension during dialysis)
- **Schedule-dependent** (3x/week, no flexibility)
- **Travel to center** required

**Candidates:**
- **Unstable** patients (arrhythmias, electrolyte disturbances)
- **Limited home support** or unable to perform self-care
- **Need for rapid correction** (hyperkalemia, volume overload)

**2. Peritoneal Dialysis (PD):**

**Description:**
- **Intracorporeal** dialysis (uses peritoneum as membrane)
- **Catheter:** Peritoneal catheter surgically placed
- **Modalities:**
  - **CAPD** (Continuous Ambulatory PD): Manual exchanges, 3-4 times/day
  - **APD** (Automated PD): Machine-assisted overnight exchanges

**Advantages:**
- **Home-based** (no travel to center)
- **Gentle** (no hemodynamic instability)
- **Flexible** (can adjust schedule)
- **Preserves residual renal function** better than HD
- **No needles**

**Disadvantages:**
- **Self-care required** (patient or caregiver)
- **Peritonitis risk** (infection of peritoneal cavity)
- **Weight gain** (glucose in dialysate)
- **Catheter complications** (infection, malfunction)
- **Less efficient** (may need transplant earlier)

**Candidates:**
- **Motivated, able** to perform self-care or have caregiver
- **Home environment** suitable for storage/supplies
- **Preserve residual renal function**
- **Avoid hemodynamic instability**

**Dialysis Modality Selection:**

**Factors to Consider:**

**Patient Factors:**
- **Age** (younger patients may prefer home therapies)
- **Comorbidities** (heart failure, diabetes, vascular disease)
- **Functional status** (ability to perform self-care)
- **Home support** (caregiver availability)
- **Living situation** (space for supplies, distance to center)
- **Personal preference** (lifestyle, independence)

**Medical Factors:**
- **Vascular access** (suitable veins for fistula)
- **Peritoneal membrane** characteristics (high vs low transporter)
- **Residual renal function** (better preserved with PD)
- **Previous abdominal surgery** (may contraindicate PD)

**Shared Decision-Making:**
- **Education** on both modalities (modality education session)
- **Trial** of modality (can switch)
- **Goal:** Patient-centered decision

**Vascular Access for Hemodialysis:**

**AV Fistula (Preferred):**
- **Surgical creation** (artery + vein anastomosis)
- **Maturation:** 6-12 weeks before use
- **Location:** Radiocephalic (wrist), brachiocephalic (elbow)
- **Advantages:** Lower infection, thrombosis, longer patency
- **Disadvantages:** Time to mature, not suitable for everyone

**AV Graft:**
- **Synthetic tube** connecting artery + vein
- **Maturation:** 2-3 weeks (quicker than fistula)
- **Location:** Forearm, upper arm
- **Advantages:** Quicker to use, suitable for poor veins
- **Disadvantages:** Higher infection, thrombosis, shorter patency

**Central Venous Catheter (CVC):**
- **Temporary access** (tunneled or non-tunneled)
- **Placement:** Internal jugular, subclavian, femoral
- **Advantages:** Immediate use, no surgery needed
- **Disadvantages:** High infection, thrombosis, central stenosis, NOT long-term

**Complications of Dialysis:**

**Hemodialysis:**
- **Hypotension** (most common)
- **Muscle cramps**, **headache**, **nausea**
- **Access complications** (infection, stenosis, thrombosis)
- **Anemia**, **bone disease**, **cardiovascular disease**

**Peritoneal Dialysis:**
- **Peritonitis** (infection of peritoneal fluid)
- **Exit site infection**, **catheter malfunction**
- **Weight gain**, **hyperglycemia**
- **Hernia**, **back pain**

**Sources:** NICE NG107, KDIGO 2024, RCP 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "nephrology_dialysis",
                "focus": "dialysis_assessment",
                "sources": ["NICE NG107", "KDIGO 2024", "RCP 2024"]
            }
        )

    def _handle_transplant(self, query: str, context: dict) -> DomainQueryResult:
        """Handle transplant queries"""
        answer = """**Kidney Transplant Evaluation and Management**

**Indications for Transplant:**
- **ESRD** (eGFR < 15) requiring or approaching dialysis
- **ESRD** on dialysis (optimal timing: before dialysis initiation)
- **Certain systemic diseases** with renal involvement (e.g., SLE, MPGN)

**Contraindications:**

**Absolute:**
- **Active malignancy** (except non-melanoma skin cancer)
- **Active infection** (including HIV, hepatitis B/C - if uncontrolled)
- **Severe, irreversible cardiopulmonary disease**
- **Life expectancy < 1-2 years** (due to non-renal disease)
- **Active substance abuse**, **non-adherence**

**Relative:**
- **Obesity** (BMI > 35-40)
- **Severe peripheral vascular disease**
- **Previous malignancy** (cancer-free period depends on type)
- **Advanced age** (physiologic, not chronologic)
- **Psychiatric illness**, **cognitive impairment**

**Living Donor Evaluation:**

**Donor Selection:**
- **Age:** 18-70 years (some centers up to 75)
- **ABO compatibility** (blood group matching)
- **Crossmatch:** Negative (no donor-specific antibodies)
- **Medical fitness:** No significant comorbidities
- **Psychological:** Voluntary, informed consent, no coercion

**Donor Risks:**
- **Surgical:** Bleeding, infection, blood clots (1-3%)
- **Long-term:** Slight increase in BP, proteinuria, CKD (but NOT ESRD)
- **Mortality:** 0.03% (3 in 10,000)
- **Living donor** has excellent long-term outcomes (similar to general population)

**Deceased Donor:**

**Types:**
- **Standard criteria donor (SCD):** Age < 50, no comorbidities
- **Expanded criteria donor (ECD):** Age ≥ 60, or age 50-59 with comorbidities
- **Donation after cardiac death (DCD):** Cardiac death before organ retrieval

**Allocation (UK - NHS Blood and Transplant):**
- **Waiting list:** Prioritized by:
  - **HLA matching** (better match = better outcomes)
  - **Time on waiting list**
  - **Sensitization** (high PRA = harder to match)
  - **Geography** (cold ischemia time)
  - **Pediatric priority** (children < 18)
  - **Highly sensitized patients**

**Pre-Transplant Evaluation:**

**Recipient Assessment:**
- **Cardiovascular:** Stress test, echo (age > 50, diabetes, CVD risk)
- **Infectious:** HIV, hepatitis B/C, TB, CMV, EBV
- **Malignancy:** Age-appropriate screening
- **Urologic:** Bladder function, lower urinary tract anatomy
- **Immunologic:** HLA typing, PRA (panel reactive antibodies), crossmatch
- **Psychosocial:** Support system, adherence, financial

**Transplant Surgery:**

**Procedure:**
- **Donor kidney:** Placed in iliac fossa (usually right, retroperitoneal)
- **Artery anastomosis:** Renal artery to internal iliac artery
- **Vein anastomosis:** Renal vein to external iliac vein
- **Ureter implantation:** Into bladder (ureteroneocystostomy)
- **Native kidneys:** Usually left in place (removed if infected, large polycystic kidneys)

**Post-Transplant Management:**

**Immediate Post-op (0-30 days):**
- **Immunosuppression:**
  - **Induction:** Basiliximab or antithymocyte globulin (ATG)
  - **Maintenance:** Tacrolimus + mycophenolate mofetil (MMF) + prednisone
- **Monitoring:** Creatinine, eGFR, tacrolimus levels (12-hour trough)
- **Complications:**
  - **Delayed graft function (DGF):** Kidney not working immediately (more common with ECD, DCD)
  - **Acute rejection:** Biopsy-proven (treated with high-dose steroids)
  - **Infection:** CMV, BK virus (polyomavirus), UTI, pneumonia
  - **Surgical:** Urine leak, lymphocele, vascular thrombosis

**Long-Term Management (> 30 days):**

**Immunosuppression:**
- **Tacrolimus:** Target trough 5-15 ng/mL (center-specific)
- **Mycophenolate mofetil (MMF):** 500-1000 mg BD
- **Prednisone:** 5-10 mg daily (may be discontinued in some protocols)

**Monitoring:**
- **Creatinine**, **eGFR** (renal function)
- **Tacrolimus levels** (if on tacrolimus)
- **Urine protein** (proteinuria = rejection or recurrence)
- **Infection surveillance:** CMV PCR, BK PCR (if indicated)
- **Malignancy screening:** Skin, lip, cervical, breast, colon, prostate

**Complications:**

**Acute Rejection:**
- **Incidence:** 10-20% in first year
- **Symptoms:** Decreased urine output, rising creatinine, fever, graft tenderness
- **Diagnosis:** Renal biopsy (gold standard)
- **Treatment:** High-dose IV methylprednisolone (500 mg-1 g daily × 3 days)

**Chronic Allograft Dysfunction:**
- **Gradual decline** in renal function over years
- **Causes:** Chronic rejection, CNI toxicity, recurrent disease, BK nephropathy
- **Treatment:** Optimize immunosuppression, treat underlying cause

**Infections:**
- **CMV:** most common viral infection (fever, leukopenia, elevated LFTs)
- **BK virus:** Polyomavirus (nephropathy → graft loss)
- **UTI:** Most common bacterial infection
- **PJP:** Prophylaxis with TMP-SMX for 6-12 months

**Malignancy:**
- **Skin cancer** (SCC, BCC) - most common
- **PTLD** (post-transplant lymphoproliferative disorder) - EBV-related
- **Solid tumors:** Colorectal, lung, breast (increased risk due to immunosuppression)

**Cardiovascular Disease:**
- **Leading cause of death** in transplant recipients
- **Risk factors:** Hypertension, diabetes, dyslipidemia, immunosuppression
- **Aggressive CV risk reduction** (statins, BP control, smoking cessation)

**Outcomes:**
- **1-year graft survival:** 95-98% (living donor), 90-95% (deceased donor)
- **5-year graft survival:** 80-90% (living donor), 70-80% (deceased donor)
- **Patient survival:** Superior to dialysis (10-15 years longer life expectancy)

**Sources:** NICE NG159, KDIGO 2024, British Transplantation Society 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "nephrology_transplant",
                "focus": "kidney_transplant",
                "sources": ["NICE NG159", "KDIGO 2024", "BTS 2024"]
            }
        )

    def _interpret_renal_function(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret renal function tests"""
        answer = """**Renal Function Test Interpretation**

**Creatinine:**
- **Normal:** 60-120 µmol/L (0.7-1.3 mg/dL) - varies by age, gender, muscle mass
- **Limitations:** Affected by muscle mass, diet (meat), medications
- **NOT** sensitive to early renal disease (50% function lost before creatinine rises)

**eGFR (Estimated Glomerular Filtration Rate):**
- **Normal:** > 90 mL/min/1.73m² (may be > 120 in young, healthy)
- **CKD Stage 3:** 30-59 mL/min/1.73m²
- **CKD Stage 4:** 15-29 mL/min/1.73m²
- **CKD Stage 5:** < 15 mL/min/1.73m² (kidney failure)
- **Formulas:**
  - **CKD-EPI** (preferred): More accurate than MDRD, especially at higher GFR
  - **MDRD** (Modification of Diet in Renal Disease): Valid for GFR < 60
  - **Cockcroft-Gault** (older, used for drug dosing)

**BUN (Blood Urea Nitrogen) / Urea:**
- **Normal:** 2.5-7.1 mmol/L (urea), 7-20 mg/dL (BUN)
- **BUN:Creatinine Ratio:**
  - **Normal:** 10-20:1
  - **> 20:1:** Prerenal azotemia (decreased renal perfusion)
  - **< 10:1:** ATN, liver disease, low protein intake

**Urinalysis Findings:**

**Protein:**
- **Dipstick:** Detects albumin (semi-quantitative)
- **ACR:** Quantifies albuminuria (preferred)
- **Normal:** ACR < 3 mg/mmol (< 30 mg/g)

**Blood:**
- **Dipstick:** Positive in hematuria, hemoglobinuria, myoglobinuria
- **Microscopy:** Distinguishes RBCs (hematuria) from other causes

**Casts:**
- **RBC casts:** Glomerulonephritis
- **WBC casts:** Interstitial nephritis, pyelonephritis
- **Granular casts:** ATN
- **Waxy casts:** Chronic kidney disease

**Crystals:**
- **Calcium oxalate:** Kidney stones
- **Uric acid:** Gout, kidney stones
- **Struvite:** Infection stones (Proteus)

**Sources:** NICE NG203, KDIGO 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "nephrology",
                "focus": "renal_function_interpretation",
                "sources": ["NICE NG203", "KDIGO 2024"]
            }
        )

    def _handle_general_nephrology(self, query: str, context: dict) -> DomainQueryResult:
        """General nephrology information"""
        answer = """**Nephrology Overview**

**Kidney Function:**
- **Filtration:** Remove waste products (creatinine, urea)
- **Regulation:** Fluid balance, electrolytes, acid-base
- **Endocrine:** Erythropoietin (RBC production), renin (BP regulation), activate vitamin D

**Common Kidney Conditions:**

**Acute Kidney Injury (AKI):**
- Sudden decline in renal function (hours to days)
- Causes: Prerenal (decreased perfusion), intrinsic (ATN, GN), postrenal (obstruction)

**Chronic Kidney Disease (CKD):**
- Progressive decline in renal function (months to years)
- Stages 1-5 (based on eGFR)
- Complications: Anemia, bone disease, cardiovascular disease

**Electrolyte Disorders:**
- **Hyperkalemia:** Medications (ACE inhibitors, ARBs), renal failure
- **Hyponatremia:** SIADH, heart failure, cirrhosis
- **Hypercalcemia:** Hyperparathyroidism, malignancy

**Kidney Stones:**
- **Calcium oxalate** (most common)
- **Uric acid**, **struvite** (infection), **cystine** (genetic)

**Glomerular Disease:**
- **Nephrotic syndrome:** Heavy proteinuria, hypoalbuminemia, edema
- **Nephritic syndrome:** Hematuria, RBC casts, oliguria, hypertension

**Renal Replacement Therapy (RRT):**
- **Hemodialysis:** In-center, 3x/week
- **Peritoneal dialysis:** Home-based, daily
- **Transplant:** Best outcomes (living donor > deceased donor)

**Sources:** NICE NG203, KDIGO 2024"""

        return DomainQueryResult(
            domain_name="nephrology",
            answer=answer,
            confidence=0.84,
            metadata={
                "specialty": "nephrology",
                "focus": "general_information",
                "sources": ["NICE NG203", "KDIGO 2024"]
            }
        )

def create_nephrology_domain():
    """Factory function to create nephrology domain instance"""
    return NephrologyDomain()
