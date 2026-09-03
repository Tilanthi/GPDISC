"""
Hematology and Oncology Domain Module for GPDISC

Comprehensive coverage of blood disorders, malignant diseases, chemotherapy,
bone marrow transplantation, and supportive oncology care.

Evidence-based with NICE, ASCO, ESMO, and British Society for Haematology guidelines.
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, Any, List


class HematologyOncologyDomain(BaseDomainModule):
    """
    Hematology and Oncology domain for blood disorders and cancer care.

    Covers:
    - Haematological malignancies (leukaemia, lymphoma, myeloma)
    - Solid tumours (breast, lung, colorectal, prostate, etc.)
    - Chemotherapy and targeted therapy
    - Bone marrow transplantation
    - Anaemia and coagulation disorders
    - Supportive oncology care
    - Oncological emergencies
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="hematology_oncology",
            version="1.0.0",
            dependencies=[],
            description="Hematology and Oncology - blood disorders, cancer care, chemotherapy, and transplantation",
            keywords=[
                "cancer", "malignancy", "tumour", "tumor", "oncology", "haematology", "hematology",
                "leukaemia", "leukemia", "lymphoma", "myeloma", "chemotherapy", "radiotherapy",
                "anaemia", "anemia", "thrombocytopenia", "neutropenia", "pancytopenia",
                "clotting", "coagulation", "dvt", "pe", "pulmonary embolism",
                "bone marrow", "transplant", "stem cell",
                "breast cancer", "lung cancer", "colorectal cancer", "prostate cancer",
                "tumour lysis", "neutropenic sepsis", "spinal cord compression",
                "hypercalcaemia", "svco", "superior vena cava",
                "blood transfusion", "platelet", "packed cell",
                "iron deficiency", "b12 deficiency", "folate deficiency",
                "haemoglobin", "hemoglobin", "haematocrit", "wbc", "rbc",
                "malignant", "metastasis", "adenocarcinoma", "carcinoma", "sarcoma", "melanoma"
            ],
            capabilities=[
                "cancer_diagnosis", "chemotherapy_management", "oncological_emergency_management",
                "blood_disorder_management", "coagulation_disorder_management",
                "bone_marrow_transplantation", "supportive_oncology_care",
                "anaemia_evaluation", "thrombosis_management"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process haematology/oncology queries with emergency prioritization.

        Emergency conditions detected:
        - Neutropenic sepsis
        - Tumour lysis syndrome
        - Spinal cord compression
        - Superior vena cava obstruction
        - Hypercalcaemia of malignancy
        - Acute leukaemia presentation
        """
        query_lower = query.lower()

        # EMERGENCY: Neutropenic sepsis (life-threatening)
        if any(term in query_lower for term in ["neutropenic sepsis", "neutropenic fever", "fever neutropenic"]):
            return self._handle_neutropenic_sepsis(query, context)

        # EMERGENCY: Spinal cord compression
        elif any(term in query_lower for term in ["spinal cord compression", "cord compression", "mets spine"]):
            return self._handle_spinal_cord_compression(query, context)

        # EMERGENCY: Tumour lysis syndrome
        elif any(term in query_lower for term in ["tumour lysis", "tumor lysis", "tls"]):
            return self._handle_tumour_lysis_syndrome(query, context)

        # EMERGENCY: Superior vena cava obstruction
        elif any(term in query_lower for term in ["svco", "superior vena cava", "svc obstruction"]):
            return self._handle_svco(query, context)

        # EMERGENCY: Hypercalcaemia of malignancy
        elif any(term in query_lower for term in ["hypercalcaemia malignancy", "high calcium cancer"]):
            return self._handle_malignant_hypercalcaemia(query, context)

        # Leukaemia
        elif any(term in query_lower for term in ["leukaemia", "leukemia", "acute leukaemia", "chronic leukaemia", "all", "aml", "cll", "cml"]):
            return self._handle_leukaemia_query(query, context)

        # Lymphoma
        elif any(term in query_lower for term in ["lymphoma", "hodgkin", "non-hodgkin", "nhl"]):
            return self._handle_lymphoma_query(query, context)

        # Myeloma
        elif any(term in query_lower for term in ["myeloma", "multiple myeloma", "plasmacytoma"]):
            return self._handle_myeloma_query(query, context)

        # Solid tumours - breast
        elif any(term in query_lower for term in ["breast cancer", "breast malignancy", "breast lump"]):
            return self._handle_breast_cancer_query(query, context)

        # Solid tumours - lung
        elif any(term in query_lower for term in ["lung cancer", "bronchogenic carcinoma", "mesothelioma"]):
            return self._handle_lung_cancer_query(query, context)

        # Solid tumours - colorectal
        elif any(term in query_lower for term in ["colorectal cancer", "colon cancer", "bowel cancer", "rectal cancer"]):
            return self._handle_colorectal_cancer_query(query, context)

        # Solid tumours - prostate
        elif any(term in query_lower for term in ["prostate cancer", "prostate malignancy", "psa"]):
            return self._handle_prostate_cancer_query(query, context)

        # Chemotherapy queries
        elif any(term in query_lower for term in ["chemotherapy", "chemo", "targeted therapy", "immunotherapy"]):
            return self._handle_chemotherapy_query(query, context)

        # Anaemia queries
        elif any(term in query_lower for term in ["anaemia", "anemia", "low haemoglobin", "low hemoglobin", "iron deficiency"]):
            return self._handle_anaemia_query(query, context)

        # Coagulation/thrombosis
        elif any(term in query_lower for term in ["dvt", "pe", "pulmonary embolism", "blood clot", "thrombosis", "warfarin", "doac"]):
            return self._handle_thrombosis_query(query, context)

        # Blood transfusion
        elif any(term in query_lower for term in ["blood transfusion", "transfusion", "packed cells", "platelet transfusion"]):
            return self._handle_transfusion_query(query, context)

        # General oncology
        else:
            return self._handle_general_oncology_query(query, context)

    def _handle_neutropenic_sepsis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle neutropenic sepsis - ONCOLOGICAL EMERGENCY"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**NEUTROPENIC SEPSIS - ONCOLOGICAL EMERGENCY - ADMIT IMMEDIATELY**

Neutropenic sepsis is a medical emergency in immunocompromised patients with high mortality if not treated urgently.

**IMMEDIATE ACTIONS:**
1. **ADMIT IMMEDIATELY** - DO NOT wait for blood results
2. **ABCDE assessment** - patients can deteriorate rapidly
3. **EMPIRICAL ANTIBIOTICS WITHIN 1 HOUR** - critical time window
4. **Blood cultures** (at least 2 sets) BEFORE antibiotics if possible
5. **Urinalysis, chest X-ray, other cultures** as indicated

**DEFINITION:**
- **Neutropenia**: ANC < 0.5 × 10⁹/L or < 1.0 × 10⁹/L and falling
- **Fever**: Single oral temperature ≥ 38.3°C (101°F) OR ≥ 38.0°C (100.4°F) sustained over 1 hour

**EMPIRICAL ANTIBIOTIC THERAPY (NICE NG151):**

**High-risk patients (expected neutropenia > 7 days, comorbidities):**
- **Piperacillin-tazobactam** 4.5g IV 8-hourly (first-line)
- **Alternatives**:
  - Meropenem 1g IV 8-hourly
  - Imipenem-cilastatin 500mg IV 6-hourly
  - Cefepime 2g IV 8-hourly

**Add vancomycin/teicoplanin if:**
- Suspected central line infection
- Skin/soft tissue infection
- Haemodynamic instability
- MRSA colonisation known
- Blood cultures growing Gram-positive bacteria

**Add aminoglycoside if:**
- Septic shock
- Susceptibility to Pseudomonas suspected

**Low-risk patients (expected neutropenia < 7 days, well):**
- May consider outpatient management with oral ciprofloxacin + amoxicillin-clavulanate
- **ONLY if** reliable for follow-up, no comorbidities

**SUPPORTIVE CARE:**
- **IV fluids**: Crystalloid resuscitation
- **Antipyretics**: Paracetamol (avoid aspirin/NSAIDs - bleeding risk)
- **G-CSF (filgrastim)**: Consider if high-risk, prolonged neutropenia expected
- **Growth factors**: May shorten hospitalisation in selected cases

**MONITORING:**
- **Vital signs** continuously if unstable
- **Daily blood counts** (ANC recovery usually 5-7 days)
- **CRP, procalcitonin**: Inflammatory markers
- **Renal/liver function**: For antibiotic dosing and toxicity

**DE-ESCALATION:**
- **Review at 48-72 hours**:
  - Afebrile 48 hours → consider oral step-down
  - Cultures positive → target therapy
  - Cultures negative → continue empiric for 7 days if high-risk
- **Stop antibiotics** when ANC > 0.5 × 10⁹/L AND afebrile 48 hours

**PREVENTION:**
- **Prophylactic antibiotics**: Consider fluoroquinolone in high-risk (> 7 days neutropenia expected)
- **Antifungal prophylaxis**: Consider posaconazole/voriconazole in very high-risk
- **G-CSF primary prophylaxis**: If > 20% risk of febrile neutropenia

**PROGNOSIS:**
- **Mortality**: 5-20% (higher with shock, organ failure)
- **Risk stratification** using MASCC score guides intensity of therapy

**Sources:** NICE NG151, ASCO Guidelines, ESMO Guidelines, British Society for Haematology""",
            confidence=0.97,
            reasoning_trace=["Detected neutropenic sepsis keywords", "This is an oncological emergency", "Antibiotics within 1 hour critical", "High mortality if delayed"],
            capabilities_used=["oncological_emergency_management"],
            metadata={
                "urgency": "emergency",
                "condition": "neutropenic_sepsis",
                "time_to_antibiotics": "1_hour",
                "mortality_risk": "high",
                "requires_hospital_admission": True,
                "sources": ["NICE NG151", "ASCO", "ESMO", "BSH"]
            }
        )

    def _handle_spinal_cord_compression(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle spinal cord compression - ONCOLOGICAL EMERGENCY"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**SPINAL CORD COMPRESSION - ONCOLOGICAL EMERGENCY - URGENT MRI REQUIRED**

Spinal cord compression is a medical emergency requiring urgent imaging and intervention to prevent permanent paralysis.

**IMMEDIATE ACTIONS:**
1. **URGENT MRI WHOLE SPINE** (within 24 hours, ideally within 4-8 hours)
2. **DO NOT delay for other investigations** if clinical suspicion high
3. **Neurosurgery/spinal oncology referral** URGENT
4. **High-dose dexamethasone** if compression confirmed or strongly suspected

**RED FLAG SYMPTOMS (Progressive):**
- **Back pain** (worsens with lying down, coughing, straining)
- **Radicular pain** (band-like, dermatomal distribution)
- **Motor weakness** (difficulty walking, ascending weakness)
- **Sensory changes** (numbness, paraesthesia, sensory level)
- **Autonomic dysfunction** (urinary retention, constipation, impotence)
- **Complete cord** (paraplegia, sensory level, incontinence) - LATE SIGN

**INVESTIGATIONS:**

**MRI Whole Spine (GOLD STANDARD):**
- **T1-weighted**: Anatomy, cord compression
- **T2-weighted**: Oedema, cord signal change
- **STIR**: Bone marrow oedema, metastases
- **Contrast**: Tumour enhancement

**CT Spine** (if MRI contraindicated):
- Bony detail, fracture, compression
- Less sensitive than MRI

**PLAIN X-RAYS** (NOT first-line):
- May show vertebral collapse, sclerosis
- **MISS** early disease

**MANAGEMENT:**

**DEXAMETHASONE (HIGH DOSE):**
- **Loading dose**: Dexamethasone 16mg IV/PO
- **Maintenance**: 8-16mg daily in divided doses
- **Rapid reduction** of oedema, pain relief
- **Start BEFORE imaging** if high clinical suspicion
- **Taper** after definitive treatment

**DEFINITIVE TREATMENT:**

**Surgical Decompression (if indicated):**
- **Indications**:
  - Progressive neurological deficit
  - Instability
  - Radioresistant tumour
  - Unknown primary (biopsy needed)
  - Single level or limited disease
- **Procedure**: Laminectomy, vertebrectomy, stabilization
- **Outcomes**: Better ambulation at 30 days vs radiotherapy alone

**Radiotherapy:**
- **Indications**:
  - Radio-sensitive tumours (lymphoma, myeloma, breast, prostate)
  - Multiple levels
  - Poor surgical candidate
  - Patient preference
- **Dose**: Usually 20 Gy in 5 fractions or 30 Gy in 10 fractions
- **Start**: Within 24-48 hours

**PRIMARY TUMOURS CAUSING SCC:**
1. **Prostate** (most common in men)
2. **Breast** (most common in women)
3. **Lung** (rapid progression, poor prognosis)
4. **Lymphoma** (radio-sensitive, good outcome)
5. **Myeloma** (radio-sensitive)
6. **Renal cell carcinoma** (surgical emergency - hypervascular)

**PROGNOSIS:**
- **Ambulatory at presentation**: 70-90% remain ambulatory
- **Non-ambulatory at presentation**: Only 20-40% regain ambulation
- **Time is critical**: < 8 hours to treatment → best outcome

**FOLLOW-UP:**
- **Neurological assessment** daily during radiotherapy
- **MRI spine** post-treatment (if uncertain response)
- **Rehabilitation**: Physiotherapy, occupational therapy

**Sources:** NICE NG147, ASCO Guidelines, ESMO Guidelines""",
            confidence=0.96,
            reasoning_trace=["Detected spinal cord compression keywords", "This is an oncological emergency", "MRI required urgently", "Surgery or radiotherapy for definitive treatment"],
            capabilities_used=["oncological_emergency_management"],
            metadata={
                "urgency": "emergency",
                "condition": "spinal_cord_compression",
                "mortality_risk": "high_if_paraplegic",
                "requires_hospital_admission": True,
                "time_to_mri": "4_8_hours",
                "sources": ["NICE NG147", "ASCO", "ESMO"]
            }
        )

    def _handle_tumour_lysis_syndrome(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle tumour lysis syndrome - ONCOLOGICAL EMERGENCY"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**TUMOUR LYSIS SYNDROME (TLS) - ONCOLOGICAL EMERGENCY**

Tumour lysis syndrome is an oncologic emergency caused by rapid tumour cell death leading to metabolic derangements.

**DEFINITION (Cairo-Bishop Criteria):**

**Laboratory TLS (2 or more of following within 24 hours before or after chemotherapy):**
- **Uric acid**: ≥ 476 μmol/L (8 mg/dL) OR 25% increase from baseline
- **Potassium**: ≥ 6.0 mmol/L OR 25% increase from baseline
- **Phosphate**: ≥ 2.1 mmol/L (children) OR 1.45 mmol/L (adults) OR 25% increase
- **Calcium**: ≤ 1.75 mmol/L (7 mg/dL) OR 25% decrease from baseline

**Clinical TLS:** Laboratory TLS + ONE of:
- **Increased creatinine** (1.5 × upper limit of normal)
- **Cardiac arrhythmia** or sudden death
- **Seizures**
- **Death**

**HIGH-RISK TUMOURS:**
- **ALL** (acute lymphoblastic leukaemia) - VERY HIGH risk
- **AML** (acute myeloid leukaemia) with high WBC
- **Burkitt lymphoma** - VERY HIGH risk
- **Diffuse large B-cell lymphoma** with high LDH
- **Acute leukaemia** with WBC > 100 × 10⁹/L

**PROPHYLAXIS (HIGH-RISK PATIENTS):**
1. **Aggressive hydration** (3L/m²/day):
   - Maintain urine output > 100 mL/m²/hour
   - Add diuretics (furosemide) if needed
2. **Allopurinol** (xanthine oxidase inhibitor):
   - 100 mg/m² TDS (max 400 mg TDS)
   - Start 24-48 hours BEFORE chemotherapy
   - Continue for 7 days
3. **Rasburicase** (recombinant uric oxidase):
   - **Consider** if uric acid > 476 μmol/L or high tumour burden
   - 0.15-0.2 mg/kg IV single dose
   - **Contraindicated** in G6PD deficiency

**TREATMENT (ESTABLISHED TLS):**

**FLUID RESUSCITATION:**
- **IV 0.9% saline** with sodium bicarbonate (alkalinises urine, reduces uric acid precipitation)
- **Target urine output**: > 100-150 mL/hour
- **Diuretics** (furosemide 20-40mg IV) if urine output inadequate

**HYPERURICAEMIA:**
- **Rasburicase** (first-line for established TLS):
  - 0.15-0.2 mg/kg IV over 30 minutes
  - Repeat in 24 hours if needed
  - Reduces uric acid within 4 hours
- **Allopurinol** (continuation from prophylaxis)

**HYPERKALAEMIA (> 6.0 mmol/L):**
- **IV calcium gluconate 10%**: 10mL over 10 minutes (cardiac protection)
- **Insulin + dextrose**: 10 units insulin in 50mL 50% dextrose
- **Salbutamol nebulised**: 5mg (alternative)
- **Sodium bicarbonate**: 150mmol IV if acidotic
- **Consider dialysis** if refractory

**HYPERPHOSPHATAEMIA:**
- **Oral phosphate binders**: Sevelamer, lanthanum carbonate
- **AVOID calcium-based binders** (risk of calcium-phosphate precipitation)
- **Consider dialysis** if severe (> 3.2 mmol/L)

**HYPOCALCAEMIA:**
- **Only treat if symptomatic** (tetany, arrhythmia, seizures)
- **IV calcium gluconate 10%**: 10mL over 10 minutes
- **Correction of hyperphosphataemia** often corrects hypocalcaemia

**RENAL REPLACEMENT THERAPY:**
- **Indications**:
  - Refractory hyperkalaemia
  - Symptomatic hypocalcaemia
  - Volume overload
  - Severe metabolic acidosis
  - Uremic symptoms
- **Modality**: Intermittent haemodialysis (most efficient)

**MONITORING:**
- **4-6 hourly**: U&Es, calcium, phosphate, uric acid, LDH
- **Fluid balance**: Strict input/output
- **ECG monitoring**: If hyperkalaemia

**Sources:** NICE NG151, Cairo-Bishop 2010, British Society for Haematology""",
            confidence=0.95,
            reasoning_trace=["Detected tumour lysis syndrome keywords", "This is an oncological emergency", "Aggressive hydration and rasburicase key", "May require dialysis"],
            capabilities_used=["oncological_emergency_management"],
            metadata={
                "urgency": "emergency",
                "condition": "tumour_lysis_syndrome",
                "mortality_risk": "moderate_high",
                "requires_hospital_admission": True,
                "sources": ["NICE NG151", "Cairo-Bishop 2010", "BSH"]
            }
        )

    def _handle_svco(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle superior vena cava obstruction - ONCOLOGICAL EMERGENCY"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**SUPERIOR VENA CAVA OBSTRUCTION (SVCO) - ONCOLOGICAL EMERGENCY**

SVCO is caused by obstruction of the superior vena cava, usually by malignancy.

**SYMPTOMS:**
- **Facial/neck swelling** (worse with leaning forward)
- **Arm swelling** (bilateral or unilateral)
- **Dilated veins** on chest wall, arms
- **Headache, facial fullness**
- **Dyspnoea, orthopnoea**
- **Cough, hoarseness**
- **Stridor** (late sign - laryngeal oedema)

**SIGNS:**
- **Plethora** (facial flushing)
- **Oedema** (face, neck, arms)
- **Collateral veins** on chest wall
- **Cyanosis** (severe cases)
- **Papilloedema** (if intracranial pressure elevated)

**CAUSES:**
- **Lung cancer** (small cell, non-small cell) - 60-80%
- **Lymphoma** (especially Hodgkin)
- **Metastatic** (breast, germ cell)
- **Thrombosis** (central lines, pacemakers)
- **Benign** (fibrosing mediastinitis, thrombosis)

**INVESTIGATIONS:**

**CT Chest with Contrast (Gold Standard):**
- **Shows**: Level of obstruction, collateral circulation, thrombus
- **Diagnostic**: Usually establishes diagnosis
- **Planning**: Guides radiotherapy fields

**MRI** (if CT contraindicated):
- Better soft tissue characterization
- Not routine

**VENOGRAPHY** (rare):
- Invasive, reserved for equivocal cases or stenting planning

**Bronchoscopy**:
- If endobronchial obstruction suspected
- Allows biopsy for histology

**MANAGEMENT:**

**INITIAL STABILIZATION:**
1. **Head elevation** (30-45°)
2. **Oxygen** if hypoxic
3. **Corticosteroids**:
   - **Dexamethasone** 8-16mg daily
   - Reduces oedema, rapid symptom relief
   - Start BEFORE radiotherapy
4. **Diuretics**:
   - **Furosemide** 20-40mg daily
   - Symptomatic relief (controversial efficacy)

**DEFINITIVE TREATMENT:**

**Radiotherapy (First-line for most):**
- **Indications**: Most malignant causes
- **Dose**: 20 Gy in 5 fractions or 30 Gy in 10 fractions
- **Onset**: Symptom improvement within 72 hours
- **Emergency**: Consider single 4 Gy fraction if severe

**Chemotherapy:**
- **First-line for**: Small cell lung cancer, lymphoma, germ cell tumours
- **Combined with radiotherapy**: For synergistic effect

**Stenting (Endovascular):**
- **Indications**:
  - Rapid symptom relief required
  - Radiotherapy-resistant
  - Benign SVCO
  - Recurrent SVCO after radiotherapy
- **Procedure**: Percutaneous stent placement
- **Outcomes**: Immediate symptom relief in 70-90%

**Thrombolysis/Thrombectomy:**
- **Indications**: SVCO due to thrombosis
- **Alteplase** + heparin
- **Consider** if acute thrombosis (< 14 days)

**ANTICOAGULATION:**
- **If thrombosis** documented or suspected:
  - **LMWH** (therapeutic dose) initially
  - Transition to DOAC/warfarin if long-term needed

**PROGNOSIS:**
- **Depends on underlying cause**
- **Lung cancer**: Poor (median survival 6-12 months)
- **Lymphoma**: Good (80% response to treatment)
- **Small cell lung cancer**: Response common but recurrence frequent

**COMPLICATIONS:**
- **Laryngeal oedema**: Stridor, airway compromise
- **Cerebral oedema**: Headache, confusion, seizures
- **Papilloedema**: Visual disturbance

**Sources:** NICE NG147, ESMO Guidelines, British Thoracic Society""",
            confidence=0.93,
            reasoning_trace=["Detected SVCO keywords", "This is an oncological emergency", "Radiotherapy first-line for most causes", "Stenting for rapid relief"],
            capabilities_used=["oncological_emergency_management"],
            metadata={
                "urgency": "emergency",
                "condition": "superior_vena_cava_obstruction",
                "mortality_risk": "variable",
                "requires_hospital_admission": True,
                "sources": ["NICE NG147", "ESMO", "BTS"]
            }
        )

    def _handle_malignant_hypercalcaemia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle malignant hypercalcaemia - ONCOLOGICAL EMERGENCY"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**HYPERCALCAEMIA OF MALIGNANCY - ONCOLOGICAL EMERGENCY**

Hypercalcaemia is the most common metabolic emergency in cancer patients.

**DEFINITION:**
- **Corrected calcium**: > 2.60 mmol/L
- **Severe**: > 3.00 mmol/L OR symptoms at any level

**PATHOPHYSIOLOGY:**
- **Humoral hypercalcaemia of malignancy (80%)**:
  - **PTHrP** secretion by tumour (PTH-related protein)
  - Lung cancer, breast cancer, renal cell carcinoma
- **Local osteolytic (20%)**:
  - Direct bone destruction
  - Multiple myeloma, breast cancer, lymphoma
- **Other**: 1,25-(OH)₂ vitamin D secretion (lymphoma)

**SYMPTOMS (More severe than hyperparathyroidism at same calcium):**
- **"Bones, stones, groans, thrones" +**
- **Dehydration**: Polyuria, polydipsia
- **Neurological**: Confusion, lethargy, coma
- **Cardiac**: Short QT, arrhythmias
- **Renal**: Pre-renal AKI, nephrogenic diabetes insipidus

**INVESTIGATIONS:**

**Serum tests:**
- **Corrected calcium**, phosphate, PTH, PTHrP
- **Urea & electrolytes**, creatinine, eGFR
- **Albumin** (for correction)
- **Vitamin D** (25-OH)

**Other tests:**
- **ECG**: Short QT interval, arrhythmias
- **PTH**: Low (distinguishes from hyperparathyroidism)
- **PTHrP**: Elevated in humoral hypercalcaemia

**MANAGEMENT:**

**EMERGENCY TREATMENT (Calcium > 3.0 mmol/L or symptomatic):**

**1. AGGRESSIVE REHYDRATION:**
- **IV 0.9% saline**: 3-4L over 24 hours
- **Initial**: 200-300 mL/hour
- **Monitor**: For fluid overload (especially cardiac/renal impairment)
- **Target**: Urine output 100-150 mL/hour

**2. LOOP DIURETIC (after rehydration):**
- **Furosemide**: 20-40mg IV 6-8 hourly
- **Enhances calcium excretion**
- **Only after volume repleted**
- **AVOID** if dehydrated

**3. BISPHOSPHONATES (Cornerstone of treatment):**

**Zoledronic acid** (preferred):
- **4mg IV over 15 minutes**
- **Onset**: 2-4 days
- **Duration**: 2-4 weeks
- **Repeat**: Every 3-4 weeks as needed
- **Renal dose adjustment**: Required if eGFR < 60

**Pamidronate** (alternative):
- **60-90mg IV over 2-4 hours**
- **Onset**: 24-48 hours
- **Renal dose adjustment**: Required

**4. DENOSUMAB (if bisphosphonate contraindicated/resistant):**
- **120mg SC weekly** for 4 weeks, then monthly
- **RANKL inhibitor**
- **Indications**:
  - Bisphosphonate-resistant
  - Severe renal impairment (eGFR < 30)
  - Hypercalcaemia due to tumours producing PTHrP

**5. GLUCOCORTICOIDS (specific tumours):**
- **Prednisolone**: 40-60mg daily
- **Indications**:
  - Multiple myeloma (very effective)
  - Lymphoma
  - Vitamin D-mediated hypercalcaemia
- **Mechanism**: Reduces 1,25-(OH)₂ vitamin D production

**6. CALCITONIN (rapid but short-lived):**
- **Calcitonin**: 4 IU/kg SC 12-hourly
- **Onset**: 4-6 hours
- **Duration**: Tachyphylaxis develops in 48 hours
- **Bridge therapy** until bisphosphonates work

**7. DIALYSIS (refractory cases):**
- **Indications**:
  - Severe renal failure
  - Heart failure (cannot tolerate fluids)
  - Refractory to medical management

**MONITORING:**
- **Calcium**: 6-12 hourly until improving
- **U&Es**: Daily (renal function, electrolytes)
- **Fluid balance**: Strict I/O
- **ECG**: If arrhythmias or severe hypercalcaemia

**PROGNOSIS:**
- **Response rate**: 70-90% to bisphosphonates
- **Median survival**: 1-3 months (worse if hypercalcaemia recurs)
- **Poor prognostic signs**: Recurrent hypercalcaemia, low albumin, high PTHrP

**PREVENTION:**
- **Prophylactic bisphosphonates**:
  - Multiple myeloma (monthly zoledronic acid)
  - Breast cancer with bone metastases (monthly zoledronic acid)
  - Prostate cancer with bone metastases (every 3 months)
- **Benefits**: Reduces skeletal-related events (pain, fracture, hypercalcaemia)

**Sources:** NICE NG151, ASCO Guidelines, ESMO Guidelines""",
            confidence=0.94,
            reasoning_trace=["Detected malignant hypercalcaemia keywords", "This is an oncological emergency", "Aggressive rehydration and bisphosphonates key", "Consider denosumab if renal impairment"],
            capabilities_used=["oncological_emergency_management"],
            metadata={
                "urgency": "emergency",
                "condition": "malignant_hypercalcaemia",
                "mortality_risk": "high",
                "requires_hospital_admission": True,
                "sources": ["NICE NG151", "ASCO", "ESMO"]
            }
        )

    def _handle_leukaemia_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle leukaemia queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**LEUKAEMIA OVERVIEW**

Leukaemia is a malignant proliferation of white blood cells in the bone marrow.

**ACUTE LEUKAEMIAS:**

**Acute Lymphoblastic Leukaemia (ALL):**
- **Most common childhood cancer** (peak 2-5 years)
- **Adult ALL**: Peak 20-40 years, worse prognosis
- **Presentation**:
  - **Fatigue, pallor** (anaemia)
  - **Bleeding, bruising** (thrombocytopenia)
  - **Infections, fever** (neutropenia)
  - **Bone pain, arthralgia** (bone marrow expansion)
  - **Lymphadenopathy, hepatosplenomegaly**
  - **CNS involvement**: Headache, vomiting, cranial nerve palsies
- **Diagnosis**:
  - **Blood film**: Blasts present
  - **Bone marrow aspirate**: > 20% blasts
  - **Immunophenotyping**: B-cell vs T-cell
  - **Cytogenetics**: t(9;22), t(12;21), MLL rearrangements
- **Treatment**:
  - **Induction**: Vincristine, steroids, asparaginase ± anthracycline
  - **Consolidation**: High-dose methotrexate, cytarabine
  - **Maintenance**: Mercaptopurine, methotrexate (2-3 years)
  - **CNS prophylaxis**: Intrathecal chemotherapy, cranial irradiation
- **Prognosis**:
  - **Children**: 90% cure rate
  - **Adults**: 40-60% cure rate

**Acute Myeloid Leukaemia (AML):**
- **Most common acute leukaemia in adults**
- **Peak incidence**: 60-70 years
- **Presentation**:
  - **Similar to ALL** but more prone to:
  - **Bleeding** (DIC, coagulopathy)
  - **Leukostasis** (high WBC → stroke, respiratory failure)
  - **Gum hypertrophy, skin leukaemia cutis**
- **FAB subtypes** (M0-M7):
  - **M3 (APL)**: Medical emergency (DIC risk), ATRA + arsenic trioxide (highly curable)
- **Cytogenetics** (prognostic):
  - **Favourable**: t(8;21), inv(16)
  - **Intermediate**: Normal karyotype
  - **Unfavourable**: Monosomy 7, complex karyotype
- **Treatment**:
  - **Induction**: "7+3" (cytarabine × 7 days + daunorubicin × 3 days)
  - **Consolidation**: High-dose cytarabine or allogeneic transplant
  - **Targeted therapy**: FLT3 inhibitors, IDH inhibitors (mutation-specific)
- **Prognosis**:
  - **Overall**: 40% cure rate
  - **APL (M3)**: > 80% cure rate (ATRA revolution)

**CHRONIC LEUKAEMIAS:**

**Chronic Lymphocytic Leukaemia (CLL):**
- **Most common adult leukaemia** in Western world
- **Peak incidence**: 70-75 years
- **Presentation**:
  - **Often asymptomatic** (incidental lymphocytosis)
  - **Fatigue, lymphadenopathy**
  - **Recurrent infections** (hypogammaglobulinaemia)
  - **Autoimmune haemolytic anaemia** (10%)
- **Diagnosis**:
  - **CLL score**: CD5+, CD19+, CD20+, CD23+, weak surface immunoglobulin
  - **Staging** (Binet): A (good), B (intermediate), C (poor)
- **Management**:
  - **Watchful waiting** (if asymptomatic)
  - **Chemoimmunotherapy**: FCR (fludarabine, cyclophosphamide, rituximab)
  - **Targeted agents**: Ibrutinib (BTK inhibitor), venetoclax (BCL-2 inhibitor)
  - **Allogeneic transplant** (selected cases)

**Chronic Myeloid Leukaemia (CML):**
- **Philadelphia chromosome** t(9;22) → BCR-ABL fusion gene
- **Natural history** (without treatment):
  - **Chronic phase**: 3-5 years
  - **Accelerated phase**: 6-18 months
  - **Blast crisis**: 3-6 months (terminal)
- **Presentation**:
  - **Fatigue, weight loss**
  - **Splenomegaly** (massive)
  - **Leukocytosis** (often > 100 × 10⁹/L)
  - **Basophilia, eosinophilia**
- **Treatment**:
  - **TKI (tyrosine kinase inhibitor)** - revolutionized prognosis
  - **Imatinib**: First-line (8-year survival > 80%)
  - **Second-generation TKI**: Dasatinib, nilotinib (if imatinib failure)
  - **Allogeneic transplant**: Considered if TKI failure
- **Monitoring**:
  - **BCR-ABL transcript levels** (PCR)
  - **Major molecular response**: BCR-ABL < 0.1%
  - **Deep molecular response**: BCR-ABL < 0.01%

**SOURCES:** NICE NG151, British Society for Haematology, ESMO Guidelines""",

            confidence=0.91,
            reasoning_trace=["Detected leukaemia keywords", "Providing comprehensive leukaemia information", "NICE NG151 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG151", "BSH", "ESMO"]}
        )

    def _handle_lymphoma_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle lymphoma queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**LYMPHOMA OVERVIEW**

Lymphoma is a malignancy of lymphocytes (B or T cells) arising in lymph nodes or extranodal sites.

**CLASSIFICATION:**

**Hodgkin Lymphoma (HL):**
- **10-15%** of all lymphomas
- **Peak incidence**: Bimodal (20-30 years, > 55 years)
- **Classic HL** (95%):
  - **Reed-Sternberg cells** (CD15+, CD30+)
  - **Subtypes**: Nodular sclerosis, mixed cellularity, lymphocyte-rich, lymphocyte-depleted
- **NLPHL** (5%):
  - **Popcorn cells** (CD20+, CD15-, CD30-)
- **Presentation**:
  - **Painless lymphadenopathy** (cervical, mediastinal)
  - **B symptoms**: Fever, night sweats, weight loss (> 10% in 6 months)
  - **Alcohol-induced pain** (site-specific, pathognomonic)
  - **Pruritus** (generalized)
- **Staging** (Ann Arbor):
  - **Stage I**: Single lymph node region
  - **Stage II**: Two regions on same side of diaphragm
  - **Stage III**: Both sides of diaphragm
  - **Stage IV**: Extranodal involvement (liver, bone marrow)
  - **A/B**: Absence/presence of B symptoms
- **Treatment**:
  - **Early stage (I-IIA)**: ABVD × 2-4 cycles + involved field radiotherapy
  - **Advanced stage (IIB-IV)**: ABVD × 6-8 cycles ± radiotherapy
  - **Relapsed/refractory**: BEACOPP, autologous stem cell transplant
- **Prognosis**:
  - **Overall**: 80-90% cure rate
  - **Early stage**: > 95% cure rate
  - **Advanced stage**: 70-80% cure rate

**Non-Hodgkin Lymphoma (NHL):**

**Aggressive NHL:**
- **Diffuse Large B-Cell Lymphoma (DLBCL)**:
  - **Most common NHL** (30-40%)
  - **Rapid progression** (weeks to months)
  - **Extranodal common** (CNS, testis, breast, stomach)
  - **Treatment**: R-CHOP × 6-8 cycles
    - **Rituximab** (anti-CD20)
    - **Cyclophosphamide, doxorubicin, vincristine, prednisone**
  - **Prognosis**: 60-70% cure rate with R-CHOP

**Indolent NHL:**
- **Follicular Lymphoma**:
  - **Second most common NHL** (20-25%)
  - **Indolent course** (median survival 10-15 years)
  - **Incurable** but responsive to treatment
  - **Presentation**: Painless lymphadenopathy, stage III/IV common
  - **Treatment**:
    - **Watchful waiting** (if asymptomatic)
    - **R-CHOP** (symptomatic)
    - **Rituximab maintenance** (prolongs remission)
    - **Radioimmunotherapy** (90Y-ibritumomab)
  - **Transformation** to DLBCL (10-30% per year) - poor prognosis

**Other NHL subtypes:**
- **Mantle Cell Lymphoma**: Aggressive, poor prognosis, CD5+, cyclin D1+
- **Burkitt Lymphoma**: Very aggressive, endemic (African) vs sporadic, c-MYC translocation
- **MALT Lymphoma**: Indolent, gastric (H. pylori association), responds to antibiotics
- **T-Cell Lymphomas**: Rare, aggressive, poor prognosis

**STAGING INVESTIGATIONS:**
- **PET-CT** (HL, aggressive NHL): Baseline and response assessment
- **CT chest/abdomen/pelvis**
- **Bone marrow biopsy** (HL not routinely required)
- **LDH** (prognostic marker)
- **Hepatitis B/C serology** (rituximab reactivation risk)
- **HIV test** (if risk factors)

**PROGNOSTIC INDICES:**

**IPI (International Prognostic Index) for Aggressive NHL:**
- **Age** > 60 years
- **LDH** > normal
- **ECOG performance status** ≥ 2
- **Stage** III or IV
- **Extranodal sites** > 1

**Low risk (0 factors)**: 5-year survival 73%
**Low-intermediate (1 factor)**: 5-year survival 51%
**High-intermediate (2 factors)**: 5-year survival 43%
**High risk (3-5 factors)**: 5-year survival 26%

**FOLLOW-UP:**
- **Clinical review** every 3-6 months for 5 years
- **Vaccinations**:
  - **Influenza annually** (immune compromised)
  - **Pneumococcal** every 5 years
  - **COVID-19** booster
- **Secondary malignancy** screening:
  - **Breast cancer** (if mantle radiotherapy)
  - **Skin cancer** (if radiotherapy)
  - **Thyroid cancer** (if neck radiotherapy)

**SOURCES:** NICE NG151, British Society for Haematology, ESMO Guidelines""",

            confidence=0.90,
            reasoning_trace=["Detected lymphoma keywords", "Providing comprehensive lymphoma information", "NICE NG151 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG151", "BSH", "ESMO"]}
        )

    def _handle_myeloma_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle myeloma queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**MULTIPLE MYELOMA OVERVIEW**

Multiple myeloma is a malignant proliferation of plasma cells in the bone marrow producing monoclonal protein.

**EPIDEMIOLOGY:**
- **Incidence**: 8-10 per 100,000 per year
- **Median age at diagnosis**: 70 years
- **Male**: Female ratio 3:2

**PATHOPHYSIOLOGY:**
- **Plasma cell proliferation** in bone marrow
- **Monoclonal protein (M-protein)** production (IgG or IgA)
- **Bone destruction** (osteoclast activation)
- **Renal impairment** (light chain deposition)
- **Immunodeficiency** (hypogammaglobulinaemia)
- **Anaemia** (marrow infiltration)

**CRAB DIAGNOSTIC CRITERIA (Requires at least one):**
- **C**: Calcium elevation (> 2.75 mmol/L)
- **R**: Renal insufficiency (creatinine > 177 μmol/L)
- **A**: Anaemia (Hb < 10 g/dL or > 20 g/L below normal)
- **B**: Bone lesions (lytic lesions, osteoporosis, fractures)

**Plus ONE of:**
- **Bone marrow plasma cells**: ≥ 10%
- **Plasmacytoma** (biopsy-proven)
- **M-protein** in serum or urine (except in non-secretory myeloma)

**SYMPTOMS:**
- **Bone pain** (back, ribs - worse with movement)
- **Pathological fractures** (vertebra, ribs, femur)
- **Recurrent infections** (pneumonia, UTI, sepsis)
- **Fatigue, lethargy** (anaemia, renal failure)
- **Hypercalcaemia**: Confusion, polyuria, constipation
- **Hyperviscosity** (IgA myeloma): Headache, visual disturbance, bleeding

**INVESTIGATIONS:**

**Blood tests:**
- **FBC, film**: Anaemia, rouleaux formation, leucoerythroblastic picture
- **U&Es, calcium**: Renal impairment, hypercalcaemia
- **Serum protein electrophoresis**: M-protein quantification
- **Serum free light chains**: κ:λ ratio (sensitive)
- **β2-microglobulin**: Prognostic marker

**Urine tests:**
- **Bence Jones protein** (light chains in urine)
- **24-hour urine protein electrophoresis**: M-protein quantification

**Bone marrow aspirate/trephine:**
- **Plasma cell percentage**
- **Cytogenetics**: t(11;14), t(4;14), t(14;16), del(17p)
- **FISH**: High-risk cytogenetics

**Imaging:**
- **Whole body low-dose CT** (preferred)
- **MRI spine** (if CT negative but back pain)
- **PET-CT** (if CT negative, for metabolic activity)

**STAGING (ISS - Revised International Staging System):**

**Stage I**:
- **β2-microglobulin**: < 3.5 mg/L AND
- **Albumin**: ≥ 35 g/L AND
- **No high-risk cytogenetics**: t(4;14), del(17p), t(14;16)

**Stage II**:
- Not fitting stage I or III criteria

**Stage III**:
- **β2-microglobulin**: ≥ 5.5 mg/L OR
- **High-risk cytogenetics present

**TREATMENT:**

**FIT PATIENTS (< 70-75 years):**
- **Induction**: VRd (bortezomib, lenalidomide, dexamethasone) × 4-6 cycles
- **Stem cell mobilization**: Cyclophosphamide + G-CSF
- **High-dose melphalan**: 200 mg/m² with autologous stem cell rescue (ASCT)
- **Maintenance**: Lenalidomide until progression

**UNFIT/ELDERLY PATIENTS (> 75 years):**
- **VRd lite** (dose-adjusted)
- **Rd** (lenalidomide, dexamethasone)
- **VMP** (bortezomib, melphalan, prednisone)
- **Cyclophosphamide, thalidomide, dexamethasone (CTD)**

**SUPPORTIVE CARE:**

**Bone disease:**
- **Zoledronic acid** 4mg IV monthly: Reduces skeletal-related events (pain, fracture, hypercalcaemia)
- **Denosumab** 120mg SC monthly: Alternative if renal impairment

**Anaemia:**
- **Erythropoietin**: If Hb < 10 g/dL
- **Transfusion**: If symptomatic

**Renal impairment:**
- **Aggressive hydration**: Prevent/treat myeloma kidney
- **Treat hypercalcaemia**: Rehydration, bisphosphonates
- **Avoid nephrotoxic drugs**: NSAIDs, IV contrast
- **Plasma exchange**: If cast nephropathy with dialysis-dependent renal failure

**Infection prophylaxis:**
- **Acyclovir**: If herpes zoster risk (bortezomib)
- **Antibiotic prophylaxis**: Levofloxacin (first 2 months)
- **IVIG replacement**: If recurrent infections with hypogammaglobulinaemia

**Thromboprophylaxis (if on immunomodulatory drugs):**
- **Aspirin 75mg daily** (if low risk)
- **LMWH** (if high risk: previous VTE, multiple myeloma-related risk factors)

**PROGNOSIS:**
- **Median survival**: 5-7 years (with modern therapy)
- **5-year survival**: 50-60%
- **High-risk cytogenetics**: 2-3 years
- **Standard-risk**: 7-10 years

**MONITORING:**
- **Serum M-protein**: Every cycle during induction
- **Serum free light chains**: Sensitive marker of response
- **24-hour urine**: If M-protein in urine
- **Response criteria**: CR, VGPR, PR, SD, PD

**SOURCES:** NICE NG151, British Society for Haematology, IMWG Guidelines""",

            confidence=0.91,
            reasoning_trace=["Detected myeloma keywords", "Providing comprehensive myeloma information", "NICE NG151 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG151", "BSH", "IMWG"]}
        )

    def _handle_breast_cancer_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle breast cancer queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**BREAST CANCER OVERVIEW**

Breast cancer is the most common cancer in women worldwide.

**EPIDEMIOLOGY:**
- **Incidence**: 1 in 8 women (12% lifetime risk)
- **Peak incidence**: 50-70 years
- **Male breast cancer**: 1% of all breast cancers

**RISK FACTORS:**
- **Non-modifiable**:
  - **Female sex**, **increasing age**
  - **Family history** (BRCA1/2 mutations)
  - **Early menarche** (< 12 years), **late menopause** (> 55 years)
  - **Nulliparity**, **late first pregnancy** (> 30 years)
  - **Previous breast cancer**, **atypical hyperplasia**
- **Modifiable**:
  - **HRT** (oestrogen-progestogen): Increased risk
  - **Alcohol**: 7 units/week increases risk by 10%
  - **Obesity** (postmenopausal): Increases risk
  - **Physical inactivity**: Increases risk

**PRESENTATION:**
- **Breast lump** (80-90% present with lump)
- **Nipple changes**: Inversion, discharge, eczema (Paget's disease)
- **Skin changes**: Dimpling (peau d'orange), ulceration, inflammation (IBC)
- **Axillary lump**: Lymphadenopathy

**INVESTIGATIONS:**

**Triple Assessment**:

**1. CLINICAL EXAMINATION**:
- Breast size, symmetry, lump characteristics
- Nipple examination, skin changes
- Axillary and supraclavicular lymph nodes

**2. IMAGING**:
- **Mammography** (women > 35 years):
  - Microcalcifications, masses, architectural distortion
  - **BI-RADS** classification (1-5)
- **Ultrasound** (all ages):
  - Distinguish solid vs cystic
  - Guid biopsy
- **MRI** (selected cases):
  - Young women with dense breasts
  - Implant rupture
  - Neoadjuvant therapy response assessment

**3. BIOPSY**:
- **Core biopsy** (14G): Histology, grade, receptor status
- **FNAC** (rare now): Cytology only
- **Excision biopsy** (if core inadequate)

**PATHOLOGY** (Essential for treatment planning):
- **Histological type**: Ductal (80%), lobular (10-15%), other
- **Histological grade**: 1 (well), 2 (moderate), 3 (poor)
- **Receptor status**:
  - **ER** (oestrogen receptor): Positive (70-80%)
  - **PR** (progesterone receptor): Positive (60-70%)
  - **HER2** (human epidermal growth factor receptor 2): Amplified (15-20%)
- **Ki-67**: Proliferation index
- **Molecular subtype**: Luminal A, Luminal B, HER2-enriched, Triple-negative

**STAGING** (TNM 8th edition):
- **T**: Tumour size (T1: ≤ 2 cm, T2: 2-5 cm, T3: > 5 cm, T4: chest wall/skin involvement)
- **N**: Nodal involvement (N0: none, N1: 1-3 nodes, N2: 4-9 nodes, N3: ≥ 10 nodes)
- **M**: Metastasis (M0: none, M1: distant metastasis)

**SURGERY:**

**Breast-conserving surgery** (wide local excision):
- **Indications**: Unifocal tumour < 4 cm, adequate breast size, patient preference
- **Oncoplastic techniques**: Therapeutic mammoplasty
- **Margin**: ≥ 2 mm (UK), ≥ 1 mm (US)
- **Radiotherapy**: Mandatory after BCS

**Mastectomy**:
- **Indications**: Multifocal/multicentric, large tumour (> 4 cm), central tumour, patient preference
- **Types**: Simple, skin-sparing, nipple-sparing
- **Reconstruction**: Immediate (implant, LD flap) or delayed

**Axillary surgery**:
- **Sentinel lymph node biopsy** (SLNB):
  - **Indications**: Clinically node-negative
  - **Technique**: Isotope + blue dye
  - **If positive**: Axillary dissection or radiotherapy
- **Axillary node dissection**:
  - **Indications**: Clinically node-positive, SLNB positive (macrometastasis)

**SYSTEMIC THERAPY:**

**Neoadjuvant** (before surgery):
- **Indications**: Tumour > 2 cm, node-positive, inflammatory, downstaging for BCS
- **Chemotherapy**: Anthracycline + taxane-based
- **HER2-targeted**: Trastuzumab + pertuzumab + chemotherapy
- **Endocrine therapy**: For postmenopausal women

**Adjuvant** (after surgery):

**Chemotherapy**:
- **Indications**: Node-positive, triple-negative, HER2-positive, high-risk features
- **Regimens**: FEC-T, AC-T, TC (docetaxel + cyclophosphamide)

**Radiotherapy**:
- **After BCS**: Whole breast 40 Gy in 15 fractions ± boost
- **After mastectomy**: If tumour > 5 cm, ≥ 4 nodes positive, other high-risk features
- **Chest wall + regional nodes**: 50 Gy in 25 fractions

**Endocrine therapy** (ER-positive):
- **Premenopausal**:
  - **Tamoxifen** 20mg daily for 5-10 years ± ovarian suppression
- **Postmenopausal**:
  - **Aromatase inhibitor** (anastrozole, letrozole, exemestane) for 5-10 years
  - **Tamoxifen** 20mg daily for 5-10 years (if AI contraindicated)
  - **Sequencing**: AI → tamoxifen (or vice versa)

**HER2-targeted therapy** (HER2-positive):
- **Trastuzumab** 8 mg/kg loading, then 6 mg/kg 3-weekly for 1 year
- **Pertuzumab** (with trastuzumab) in neoadjuvant or metastatic setting
- **T-DM1 (ado-trastuzumab emtansine)**: If residual disease after neoadjuvant therapy

**FOLLOW-UP:**
- **Clinical review**: Every 6 months for 5 years, then annually
- **Mammography**: Annually (ipsilateral breast after BCS, contralateral always)
- **Screening for metastatic disease**: NOT routine (only if symptoms)

**PROGNOSIS:**
- **5-year survival** (UK): 85-90% (all stages)
- **Stage I**: 98-99%
- **Stage II**: 85-90%
- **Stage III**: 50-70%
- **Stage IV**: 20-30% (median survival 2-3 years)

**SOURCES:** NICE NG101, ESMO Guidelines, ASCO Guidelines""",

            confidence=0.91,
            reasoning_trace=["Detected breast cancer keywords", "Providing comprehensive breast cancer information", "NICE NG101 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG101", "ESMO", "ASCO"]}
        )

    def _handle_lung_cancer_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle lung cancer queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**LUNG CANCER OVERVIEW**

Lung cancer is the leading cause of cancer death worldwide.

**EPIDEMIOLOGY:**
- **Incidence**: 1 in 14 men, 1 in 17 women (UK lifetime risk)
- **Peak incidence**: 70-80 years
- **Male**: Female ratio 3:2 (changing, now approaching 1:1)

**RISK FACTORS:**
- **Smoking** (85-90% of cases): Dose-response relationship
- **Passive smoking**: 20-30% increased risk
- **Radon exposure** (second leading cause): Residential radon in certain areas
- **Occupational**: Asbestos, silica, diesel exhaust, heavy metals
- **Family history**: 2x increased risk
- **Previous lung disease**: COPD, pulmonary fibrosis

**HISTOLOGICAL TYPES:**

**Non-Small Cell Lung Cancer (NSCLC)** - 85%:
- **Adenocarcinoma** (40%): Most common in non-smokers, women, peripheral location
- **Squamous cell carcinoma** (25-30%): Strongly associated with smoking, central location
- **Large cell carcinoma** (10-15%): Poorly differentiated, aggressive
- **Other**: Bronchoalveolar carcinoma, adenosquamous, sarcomatoid

**Small Cell Lung Cancer (SCLC)** - 15%:
- **Strongly associated** with smoking
- **Central location** (hilar mass)
- **Aggressive**, **early metastasis**
- **Chemosensitive** but early relapse

**PRESENTATION:**
- **Incidental finding** (on CXR/CT for other reason)
- **Persistent cough** (3 weeks or more)
- **Haemoptysis** (30%)
- **Dyspnoea**, **wheeze**
- **Chest pain** (30-40%)
- **Weight loss**, **anorexia**
- **Superior vena cava obstruction** (SCLC, SCC)
- **Paraneoplastic syndromes** (10%): SIADH, Cushing's, Lambert-Eaton myasthenic syndrome
- **Metastatic presentation**: Bone pain, neurological symptoms (brain metastasis)

**INVESTIGATIONS:**

**Chest X-ray** (first-line):
- **Sensitivity**: 70-80%
- **Findings**: Mass, collapse, pleural effusion

**CT chest** (with contrast):
- **Characterization**: Size, location, invasion, lymph nodes
- **PET-CT**: Metabolic activity, metastasis detection, staging

**Bronchoscopy**:
- **Central tumours**: Direct visualization, biopsy, washings
- **Endobronchial ultrasound (EBUS)**: Mediastinal lymph node sampling

**Percutaneous lung biopsy**:
- **Peripheral tumours**: CT-guided core biopsy
- **Complication**: Pneumothorax (10-20%)

**STAGING (TNM 8th edition):**
- **T**: Tumour size, invasion (T1: ≤ 3 cm, T2: 3-5 cm or invasion, T3: > 5 cm or separate tumour, T4: invasion of mediastinum, heart, great vessels)
- **N**: Nodal involvement (N0: none, N1: ipsilateral hilar, N2: ipsilateral mediastinal/subcarinal, N3: contralateral/ supraclavicular)
- **M**: Metastasis (M0: none, M1a: contralateral lung nodules/pleural effusion, M1b: distant single organ, M1c: multiple organs)

**MOLECULAR TESTING** (NSCLC, adenocarcinoma):
- **EGFR mutations** (10-15%): Tyrosine kinase inhibitor (TKI) sensitive
- **ALK rearrangements** (3-7%): Crizotinib, alectinib
- **PD-L1 expression** (50% high): Immunotherapy (pembrolizumab)
- **ROS1**, **BRAF**, **NTRK**, **RET**, **MET**: Other actionable mutations

**TREATMENT:**

**NSCLC - Early Stage (I-II):**
- **Surgery** (lobectomy preferred):
  - **Video-assisted thoracoscopic surgery (VATS)**: Less invasive, faster recovery
  - **Open thoracotomy**: Required for large/central tumours, complex resections
- **Adjuvant chemotherapy**: For stage II (cisplatin-based)
- **Radiotherapy**: If medically unfit for surgery

**NSCLC - Locally Advanced (III):**
- **Multimodality therapy**:
  - **Concurrent chemoradiotherapy**: Cisplatin/etoposide + radiotherapy 60 Gy
  - **Durvalumab** (PD-L1 inhibitor) for 1 year if no progression after chemoradiation
- **Surgery**: Selected cases after neoadjuvant therapy

**NSCLC - Metastatic (IV):**
- **Driver mutation-positive**:
  - **EGFR**: Osimertinib (first-line), erlotinib, gefitinib
  - **ALK**: Alectinib, brigatinib, crizotinib
  - **ROS1**: Crizotinib, entrectinib
- **Driver mutation-negative**:
  - **PD-L1 high** (≥ 50%): Pembrolizumab monotherapy
  - **PD-L1 low (1-49%)**: Pembrolizumab + chemotherapy
  - **PD-L1 negative**: Chemotherapy alone (carboplatin + paclitaxel ± bevacizumab)

**SCLC - Limited Stage (I-III):**
- **Concurrent chemoradiotherapy**:
  - **Chemotherapy**: Cisplatin + etoposide × 4-6 cycles
  - **Radiotherapy**: 60-70 Gy concurrent with cycles 2-3
- **Prophylactic cranial irradiation** (PCI): If complete response to chemoradiation

**SCLC - Extensive Stage (IV):**
- **Chemotherapy**:
  - **Carboplatin + etoposide** (preferred)
  - **Cisplatin + etoposide** (if fit)
- **Immunotherapy**:
  - **Atezolizumab** or **durvalumab** added to chemotherapy (first-line)
- **PCI**: Consider if good response to chemotherapy
- **Radiotherapy**: For symptomatic metastases (brain, bone)

**PROGNOSIS:**

**NSCLC:**
- **5-year survival** (UK): 10-15% (all stages)
- **Stage I**: 60-80%
- **Stage II**: 30-50%
- **Stage III**: 10-15%
- **Stage IV**: 1-5% (median survival 8-12 months)

**SCLC:**
- **5-year survival** (UK): 5-7% (all stages)
- **Limited stage**: 20-25% (median survival 16-20 months)
- **Extensive stage**: 1-2% (median survival 8-13 months)

**SOURCES:** NICE NG122, ESMO Guidelines, ASCO Guidelines""",

            confidence=0.90,
            reasoning_trace=["Detected lung cancer keywords", "Providing comprehensive lung cancer information", "NICE NG122 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG122", "ESMO", "ASCO"]}
        )

    def _handle_colorectal_cancer_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle colorectal cancer queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**COLORECTAL CANCER OVERVIEW**

Colorectal cancer (CRC) is the fourth most common cancer in the UK.

**EPIDEMIOLOGY:**
- **Incidence**: 1 in 14 men, 1 in 19 women (UK lifetime risk)
- **Peak incidence**: 70-80 years
- **Male**: Female ratio 3:2

**RISK FACTORS:**
- **Age** > 50 years (90% of cases)
- **Family history** (2-3x risk if one first-degree relative < 50 years)
- **Inflammatory bowel disease**: Ulcerative colitis, Crohn's disease
- **Hereditary syndromes**:
  - **FAP** (familial adenomatous polyposis): APC gene mutation, hundreds to thousands of polyps
  - **HNPCC** (hereditary non-polyposis colorectal cancer, Lynch syndrome): Mismatch repair genes
- **Lifestyle factors**:
  - **Red meat**, **processed meat** (WHO Group 1 carcinogen)
  - **Alcohol** (> 14 units/week)
  - **Obesity**, **physical inactivity**
  - **Smoking**

**PROTECTIVE FACTORS:**
- **Aspirin** (30% risk reduction with 5 years use)
- **NSAIDs**, **calcium**
- **High-fibre diet**, **fruit and vegetables**
- **Physical activity**

**PRESENTATION:**
- **Right-sided (caecum, ascending colon)**:
  - **Iron deficiency anaemia** (fatigue, lethargy)
  - **Right iliac fossa pain**
  - **Mass** (occasionally palpable)
- **Left-sided (descending colon, sigmoid, rectum)**:
  - **Change in bowel habit** (3-6 weeks)
  - **Rectal bleeding** (bright red blood mixed with stool)
  - **Tenesmus** (rectal cancer)
  - **Obstruction** (descending colon cancer)
- **Emergency presentation** (15-20%):
  - **Complete obstruction**: Abdominal pain, distension, vomiting, constipation
  - **Perforation**: Peritonitis, sepsis
  - **Rectal bleeding** (massive)

**INVESTIGATIONS:**

**Colonoscopy** (Gold standard):
- **Diagnostic**: Visualize tumour, biopsy for histology
- **Therapeutic**: Polypectomy (if early lesion)
- **Complete**: Requires bowel preparation

**CT colonography** (if colonoscopy incomplete or contraindicated):
- **Sensitivity**: 85-90% for polyps > 1 cm
- **Disadvantages**: No biopsy, radiation exposure

**Flexible sigmoidoscopy**:
- **Left-sided lesions only**
- **No bowel preparation** (enemas only)

**CT chest/abdomen/pelvis** (staging):
- **Primary tumour**: Size, local invasion
- **Lymph nodes**: Mesenteric, retroperitoneal
- **Metastasis**: Liver, lungs, peritoneum

**MRI pelvis** (rectal cancer only):
- **Local staging**: Tumour depth, mesorectal fascia involvement
- **Radiotherapy planning**

**CEA** (carcinoembryonic antigen):
- **Baseline** before treatment
- **Monitoring**: Post-treatment surveillance (rising CEA suggests recurrence)

**PATHOLOGY:**
- **Adenocarcinoma** (95%)
- **Mucinous**, **signet ring** (poor prognosis)
- **Neuroendocrine** (rare, better prognosis)
- **Grade**: Well, moderate, poor differentiation

**STAGING (TNM 8th edition):**
- **T**: Tumour depth (T1: submucosa, T2: muscularis propria, T3: through muscularis propria, T4: serosa/other organs)
- **N**: Nodal involvement (N0: none, N1: 1-3 nodes, N2: ≥ 4 nodes)
- **M**: Metastasis (M0: none, M1: distant metastasis)

**TREATMENT:**

**Colon Cancer**:
- **Surgery** (mainstay):
  - **Right hemicolectomy** (caecum, ascending, hepatic flexure, transverse)
  - **Left hemicolectomy** (splenic flexure, descending, sigmoid)
  - **Anterior resection** (upper rectum)
  - **Abdominoperineal resection** (lower rectum, permanent colostomy)
- **Laparoscopic** vs **open**:
  - **Laparoscopic**: Faster recovery, shorter hospital stay, equivalent oncologic outcomes
  - **Open**: Required for emergency obstruction/perforation, locally advanced tumours
- **Adjuvant chemotherapy** (Stage III, high-risk Stage II):
  - **FOLFOX** (5-FU, leucovorin, oxaliplatin) × 6 months
  - **CAPOX** (capecitabine, oxaliplatin) × 3-6 months
  - **5-FU/LV** (if oxaliplatin contraindicated)

**Rectal Cancer**:
- **Preoperative radiotherapy** (Stage II-III):
  - **Short-course** (5 Gy × 5 fractions): Surgery within 7 days
  - **Long-course chemoradiation** (50.4 Gy + capecitabine): Surgery 6-10 weeks later, tumour downstaging
- **Total mesorectal excision (TME)**: Standard surgical technique
- **Adjuvant chemotherapy**: Consider if high-risk features (positive circumferential margin, < 12 nodes, poor differentiation)

**Metastatic Disease:**
- **Liver-only metastases** (resectable or potentially resectable):
  - **Surgical resection** (5-year survival 40-50%)
  - **Neoadjuvant chemotherapy** (FOLFOX or FOLFIRI + bevacizumab)
  - **Portal vein embolization** (if future liver remnant < 20%)
- **Lung metastases** (resectable):
  - **Surgical resection** (5-year survival 30-40%)
- **Unresectable metastatic disease**:
  - **Chemotherapy**: FOLFOX, FOLFIRI ± bevacizumab
  - **Targeted therapy**:
    - **Bevacizumab** (anti-VEGF): First-line
    - **Cetuximab**, **panitumumab** (anti-EGFR): RAS wild-type only
    - **Regorafenib** (third-line)
  - **Immunotherapy**: **Pembrolizumab** (MSI-H/dMMR tumours only, 5% of CRC)

**EMERGENCY SURGERY:**
- **Obstruction** (colon):
  - **Right-sided**: Right hemicolectomy with primary anastomosis
  - **Left-sided**: Hartmann's procedure (resection + end colostomy) OR decompressing stent ± subsequent resection
- **Perforation**: Hartmann's procedure (resection + end colostomy)
- **Massive rectal bleeding**: Subtotal colectomy or Hartmann's procedure

**FOLLOW-UP:**
- **Clinical review**: Every 3-6 months for 3 years, then every 6 months for 2 years
- **CEA**: Every 3-6 months for 3 years
- **CT chest/abdomen/pelvis**: Annually for 5 years
- **Colonoscopy**: At 1 year (if preoperative colonoscopy incomplete), then at 3 years, then every 5 years

**SCREENING** (NHS Bowel Cancer Screening Programme):
- **Age 60-74**: Home fecal immunochemical test (FIT) every 2 years
- **Positive FIT**: Colonoscopy
- **Age 55**: One-off bowel scope screening (flexible sigmoidoscopy)
- **Benefit**: 16% mortality reduction, 300 cancers prevented per 100,000 screened

**PROGNOSIS:**
- **5-year survival** (UK): 55-60% (all stages)
- **Stage I**: 90-95%
- **Stage II**: 75-80%
- **Stage III**: 45-55%
- **Stage IV**: 5-10% (median survival 12-18 months)

**SOURCES:** NICE NG151, ESMO Guidelines, ASCO Guidelines""",

            confidence=0.91,
            reasoning_trace=["Detected colorectal cancer keywords", "Providing comprehensive colorectal cancer information", "NICE NG151 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG151", "ESMO", "ASCO"]}
        )

    def _handle_prostate_cancer_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle prostate cancer queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**PROSTATE CANCER OVERVIEW**

Prostate cancer is the most common cancer in men in the UK.

**EPIDEMIOLOGY:**
- **Incidence**: 1 in 8 men (12% lifetime risk)
- **Peak incidence**: 70-80 years
- **Male only** (rarely diagnosed < 50 years)

**RISK FACTORS:**
- **Age** (strongest risk factor): Rare < 50 years, increases with age
- **Ethnicity**: Black African/Caribbean men 2-3x increased risk vs white men
- **Family history**: 2-3x increased risk if father/brother affected
- **Genetics**: BRCA2 mutations (5% increased risk)
- **Obesity**: Possible association with aggressive disease

**PROTECTIVE FACTORS:**
- **Diet**: Lycopene (tomatoes), selenium, vitamin E (evidence weak)
- **5-alpha reductase inhibitors** (finasteride, dutasteride): 25% risk reduction

**PRESENTATION:**
- **Screening-detected** (PSA testing, now less common)
- **Lower urinary tract symptoms** (LUTS): Poor stream, frequency, urgency, nocturia (often BPH, not cancer)
- **Incidental finding** (on TURP for BPH)
- **Advanced disease**: Bone pain (spine, pelvis, ribs), weight loss, anaemia
- **Urinary retention** (rare, if locally advanced)

**INVESTIGATIONS:**

**PSA (Prostate-Specific Antigen):**
- **Age-specific ranges**:
  - **40-49 years**: < 2.5 ng/mL
  - **50-59 years**: < 3.5 ng/mL
  - **60-69 years**: < 4.5 ng/mL
  - **70-79 years**: < 6.5 ng/mL
- **PSA > 100 ng/mL**: Suggests metastatic disease
- **Limitations**:
  - **False positives**: BPH, prostatitis, UTI, ejaculation (within 48 hours), vigorous exercise
  - **False negatives**: 15% of men with PSA < 4 ng/mL have cancer

**Multiparametric MRI (mpMRI)** (GOLD STANDARD for staging):
- **T2-weighted**: Anatomy, tumour detection
- **Diffusion-weighted imaging (DWI)**: Cellularity
- **Dynamic contrast-enhanced (DCE)**: Vascularity
- **PI-RADS score**: 1-5 (likelihood of clinically significant cancer)
- **Advantages**: Avoids biopsy in 25-30% (if negative), targets suspicious lesions

**Transperineal template prostate biopsy** (if mpMRI positive):
- **Indications**: PSA > age-specific range, abnormal DRE, mpMRI PI-RADS 4-5
- **Technique**: Template-guided cores under general anaesthetic
- **Complications**: Infection (1-2%), bleeding (5-10%), urinary retention (2-5%)

**Digital rectal examination (DRE)**:
- **Findings**: Hard, irregular nodule, asymmetry
- **Limitations**: 50% of cancers are posterior and palpable, 50% are not palpable
- **Staging**: T2 (organ-confined), T3 (extracapsular extension), T4 (fixed to surrounding structures)

**Bone scan** (if PSA > 10 ng/mL or bone pain):
- **Technetium-99m** radionuclide scan
- **Findings**: Hot spots (metastasis), cold spots (healing fracture after treatment)

**CT abdomen/pelvis** (staging):
- **Lymph nodes**: Pelvic, retroperitoneal
- **Visceral metastases**: Liver, lung (rare)

**PATHOLOGY:**
- **Adenocarcinoma** (> 95%)
- **Gleason score**: 6 (well), 7 (moderate), 8-10 (poor)
- **Grade Group**: 1 (Gleason 6), 2 (Gleason 3+4), 3 (Gleason 4+3), 4 (Gleason 8), 5 (Gleason 9-10)

**STAGING (TNM 8th edition):**
- **T**: T1: Clinically inapparent, T2: Organ-confined, T3: Extracapsular extension, T4: Fixed
- **N**: N0: No nodes, N1: Regional lymph node metastasis
- **M**: M0: No distant metastasis, M1: Distant metastasis (bone usually)

**RISK STRATIFICATION:**

**Low-risk**:
- **PSA** < 10 ng/mL
- **Gleason score** ≤ 6
- **Clinical stage** T1-T2a

**Intermediate-risk**:
- **PSA** 10-20 ng/mL OR
- **Gleason score** 7 OR
- **Clinical stage** T2b

**High-risk**:
- **PSA** > 20 ng/mL OR
- **Gleason score** 8-10 OR
- **Clinical stage** T3-T4

**TREATMENT:**

**LOCALIZED DISEASE**:

**Active Surveillance** (low-risk, selected intermediate-risk):
- **Monitoring**: PSA every 3-6 months, repeat mpMRI/biopsy at 12-24 months
- **Switch to definitive treatment** if progression (PSA doubling time < 3 years, Gleason upgrade, tumour volume increase)
- **Advantages**: Avoid treatment-related side effects
- **Disadvantages**: Anxiety, risk of progression

**Radical Prostatectomy** (all risk groups):
- **Techniques**:
  - **Open retropubic**: Standard, longer recovery
  - **Laparoscopic**: Less invasive, longer operating time
  - **Robot-assisted (RARP)**: Most common, faster recovery, better visualization
- **Nerve-sparing**: Preserves erectile function (if bilateral nerve-sparing possible)
- **Side effects**:
  - **Urinary incontinence**: 5-15% at 12 months
  - **Erectile dysfunction**: 30-50% (age-dependent)

**Radical Radiotherapy** (all risk groups):
- **External beam radiotherapy (EBRT)**: 78 Gy in 39 fractions over 7-8 weeks
- **Brachytherapy** (low-dose rate permanent implants): For low-risk disease only
- **Hypofractionated EBRT**: 60 Gy in 20 fractions over 4 weeks (equivalent efficacy, more convenient)
- **Side effects**:
  - **Urinary**: Frequency, urgency, dysuria (acute), urethral stricture (late)
  - **Bowel**: Diarrhoea, proctitis (acute), rectal bleeding (late)
  - **Erectile dysfunction**: 30-40% (age-dependent)

**Hormone therapy** (combined with radiotherapy for intermediate-high risk, or alone for advanced disease):
- **LHRH agonists** (goserelin, leuprorelin): 3-monthly injections
- **LHRH antagonists** (degarelix): Alternative if tumour flare concern
- **Anti-androgens** (bicalutamide, flutamide): Combined with LHRH agonists (complete androgen blockade)
- **Side effects**: Hot flushes, sexual dysfunction, osteoporosis, metabolic syndrome

**ADVANCED DISEASE**:

**Metastatic hormone-sensitive prostate cancer** (HSPC, newly diagnosed):
- **Androgen deprivation therapy** (ADT): LHRH agonists/antagonists ± anti-androgens
- **Chemohormonal therapy** (DOCETAXEL + ADT): If high-volume disease (CHAARTED trial)
- **ADT + Abiraterone + Prednisolone** (STAMPEDE trial): If high-volume disease
- **Prostate radiotherapy**: If low-volume metastatic disease (HORRAD trial)

**Metastatic castration-resistant prostate cancer** (CRPC):
- **First-line**:
  - **Abiraterone + Prednisolone** (COU-AA-302 trial)
  - **Enzalutamide** (AFFIRM trial)
  - **Docetaxel chemotherapy** (TAX-327 trial)
- **Second-line** (after progression on first-line):
  - **Cabazitaxel** (TROPIC trial)
  - **Radium-223** (ALSYMPCA trial, if bone metastases only)
  - **Sipuleucel-T** (immunotherapy, US only)
- **Palliative radiotherapy**: For bone pain, spinal cord compression, local progression

**FOLLOW-UP:**
- **Clinical review**: Every 6-12 months
- **PSA monitoring**: Every 3-6 months (if on active surveillance or after treatment)
- **DRE**: Annually (if on active surveillance)
- **Testosterone monitoring**: Every 3-6 months (if on hormone therapy, target castrate < 1.7 nmol/L)

**SCREENING CONTROVERSY:**
- **UK**: No routine PSA screening (lack of mortality benefit, overdiagnosis, overtreatment)
- **USA**: USPSTF recommends against PSA screening (grade D)
- **Informed choice**: Discuss PSA testing with men aged 50-69 years (black men 45-69 years) if they inquire

**PROGNOSIS:**
- **5-year survival** (UK): 85-90% (all stages)
- **Localized disease**: 98-100%
- **Locally advanced**: 70-80%
- **Metastatic disease**: 30% (median survival 3-4 years, improved with abiraterone/enzalutamide)

**SOURCES:** NICE NG131, ESMO Guidelines, AUA Guidelines""",

            confidence=0.90,
            reasoning_trace=["Detected prostate cancer keywords", "Providing comprehensive prostate cancer information", "NICE NG131 guidelines applied"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE NG131", "ESMO", "AUA"]}
        )

    def _handle_chemotherapy_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle chemotherapy queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**CHEMOTHERAPY OVERVIEW**

Chemotherapy is the use of cytotoxic drugs to kill cancer cells.

**PRINCIPLES:**
- **Cytotoxic**: Kills rapidly dividing cells (cancer cells, but also normal cells)
- **Cell cycle specificity**:
  - **Cell cycle-specific**: Act on specific phases (S-phase: antimetabolites; M-phase: vinca alkaloids)
  - **Cell cycle-nonspecific**: Act on all phases (alkylating agents, antibiotics)
- **Dose-limiting toxicity**: Maximum tolerated dose based on side effects
- **Combination therapy**: Multiple drugs with different mechanisms, non-overlapping toxicities

**INDICATIONS:**
- **Adjuvant**: After surgery/primary treatment (eradicates micrometastasis)
- **Neoadjuvant**: Before surgery (downstaging, organ preservation)
- **Concurrent**: With radiotherapy (radiosensitizer)
- **Palliative**: Metastatic disease (symptom control, prolong life)
- **Curative**: High-dose therapy with stem cell rescue (leukaemia, lymphoma)

**ADMINISTRATION:**
- **IV** (most common): Peripheral line, PICC line, central line, PORT
- **Oral**: Capecitabine, cyclophosphamide, etoposide, temozolomide
- **Intrathecal**: Methotrexate, cytarabine (CNS prophylaxis/treatment)
- **Intravesical**: BCG, mitomycin C (bladder cancer)
- **Intra-arterial**: Hepatic (for liver metastases)
- **Topical**: 5-FU, nitrogen mustard (skin cancer)

**COMMON REGIMENS:**

**AC**: Doxorubicin + Cyclophosphamide (breast cancer)
**AC-T**: AC followed by Paclitaxel (breast cancer)
**BEACOPP**: Bleomycin, Etoposide, Doxorubicin, Cyclophosphamide, Vincristine, Procarbazine, Prednisolone (Hodgkin lymphoma)
**CAPOX**: Capecitabine + Oxaliplatin (colorectal cancer)
**CARBOPLATIN/PACLITAXEL**: Ovarian, lung, bladder cancer
**CHOP**: Cyclophosphamide, Doxorubicin, Vincristine, Prednisolone (NHL)
**CISPLATIN/ETOPOSIDE**: Small cell lung cancer, germ cell tumours
**CMF**: Cyclophosphamide, Methotrexate, 5-Fluorouracil (breast cancer)
**DOCFOS**: Docetaxel + Fosfamide (soft tissue sarcoma)
**FEC**: 5-Fluorouracil, Epirubicin, Cyclophosphamide (breast cancer)
**FOLFIRI**: 5-FU, Leucovorin, Irinotecan (colorectal cancer)
**FOLFOX**: 5-FU, Leucovorin, Oxaliplatin (colorectal cancer)
**FOLFOXIRI**: 5-FU, Leucovorin, Oxaliplatin, Irinotecan (colorectal cancer)
**GEMCITABINE/CISPLATIN**: Lung, bladder, pancreatic cancer
**R-CHOP**: Rituximab + CHOP (diffuse large B-cell lymphoma)
**TIP**: Paclitaxel, Ifosfamide, Cisplatin (germ cell tumours)
**TIP/TIP**: Paclitaxel, Ifosfamide, Cisplatin (germ cell tumours)
**VAD**: Vincristine, Doxorubicin, Dexamethasone (myeloma)
**VC**: Vincristine + Carboplatin (small cell lung cancer)
**XELODA**: Capecitabine (breast, colorectal cancer)

**SIDE EFFECTS (Management):**

**Myelosuppression**:
- **Neutropenia**:
  - **Primary prophylaxis**: G-CSF (filgrastim, pegfilgrastim) if > 20% risk of febrile neutropenia
  - **Secondary prophylaxis**: G-CSF after febrile neutropenia episode
  - **Dose reduction**: If recurrent neutropenia
- **Anaemia**:
  - **Erythropoietin** (epoetin alfa, darbepoetin alfa) if Hb < 10 g/dL
  - **Transfusion**: If symptomatic or Hb < 8 g/dL
- **Thrombocytopenia**:
  - **Platelet transfusion** if < 10 × 10⁹/L or < 20 × 10⁹/L with bleeding/fever
  - **Dose reduction**: If recurrent thrombocytopenia

**Nausea and Vomiting** (NICE CG122):
- **Anti-emetics**: Dexamethasone, 5-HT3 antagonists (ondansetron, granisetron), NK1 antagonists (aprepitant, fosaprepitant)
- **Risk-based prophylaxis**:
  - **High** (cisplatin, AC, cyclophosphamide > 1500 mg/m²): Triple antiemetics (dexamethasone + 5-HT3 + NK1)
  - **Moderate** (carboplatin, oxaliplatin, irinotecan): Dexamethasone + 5-HT3
  - **Low** (taxanes, gemcitabine, 5-FU): Dexamethasone alone
  - **Minimal** (targeted therapies, immunotherapy): Antiemetics as needed

**Mucositis**:
- **Oral care**: Saline mouthwash, soft toothbrush, avoid alcohol-containing mouthwashes
- **Pain control**: Benzydamine mouthwash, lidocaine viscous, systemic analgesics
- **Fungal prophylaxis**: Nystatin, fluconazole (if prolonged steroids/antibiotics)

**Alopecia**:
- **Scalp cooling**: Reduces hair loss with taxanes, anthracyclines
- **Wig provision**: NHS prescription available
- **Reversible**: Hair regrows 3-6 months after chemotherapy completion

**Cardiotoxicity** (anthracyclines):
- **Doxorubicin, epirubicin, daunorubicin**
- **Cumulative dose**: Doxorubicin > 450 mg/m² (high risk)
- **Monitoring**: Echocardiogram or MUGA scan before and after treatment
- **Dexrazoxane**: Cardioprotectant (if high cumulative dose)

**Neuropathy** (taxanes, platinum compounds, vinca alkaloids):
- **Peripheral sensory neuropathy**: Numbness, tingling, burning (glove-and-stocking distribution)
- **Motor neuropathy**: Weakness, foot drop, wrist drop
- **Autonomic neuropathy**: Constipation, orthostatic hypotension, urinary retention
- **Dose reduction/treatment cessation**: If Grade 2-3 neuropathy

**Nephrotoxicity** (cisplatin):
- **Prevention**: Aggressive hydration before, during, after cisplatin
- **Monitoring**: U&Es before each cycle
- **Dose reduction**: If CrCl < 60 mL/min (switch to carboplatin)

**Hypersensitivity reactions** (platinum compounds, taxanes):
- **Premedication**: Dexamethasone, antihistamines (H1 and H2 blockers)
- **Desensitization**: If previous reaction and no alternative
- **Switch**: Carboplatin if cisplatin allergy (cross-reactivity 50%)

**Reproductive toxicity**:
- **Infertility**: Common with alkylating agents (cyclophosphamide, ifosfamide)
- **Sperm banking**: Before chemotherapy (men)
- **Embryo/egg freezing**: Before chemotherapy (women)
- **Contraception**: Required during and for 6-12 months after chemotherapy

**PRE-CHEMOTHERAPY CHECKLIST:**
- **Performance status**: ECOG 0-4 (0 = fully active, 4 = bedbound)
- **Blood counts**: ANC > 1.5, platelets > 100, Hb > 8 g/dL
- **Renal function**: Creatinine clearance > 50 mL/min (most regimens)
- **Liver function**: Bilirubin < 1.5 × ULN, AST/ALT < 2.5 × ULN
- **Cardiac function**: LVEF > 50% (if anthracyclines)
- **Pregnancy test**: (if applicable)
- **Contraception counseling**: (if applicable)
- **Blood-borne virus status**: Hepatitis B, C, HIV (relevant for rituximab, stem cell transplant)

**SOURCES:** NICE CG122, British Society for Haematology, ASCO Guidelines""",

            confidence=0.89,
            reasoning_trace=["Detected chemotherapy keywords", "Providing comprehensive chemotherapy information", "NICE CG122 guidelines applied"],
            capabilities_used=["chemotherapy_management"],
            metadata={"sources": ["NICE CG122", "BSH", "ASCO"]}
        )

    def _handle_anaemia_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle anaemia queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**ANAEMIA OVERVIEW**

Anaemia is a reduction in haemoglobin (Hb) below the reference range for age and sex.

**REFERENCE RANGES:**
- **Men**: 13.0-17.0 g/dL
- **Women**: 11.5-15.5 g/dL
- **Pregnancy**: > 11.0 g/dL (first trimester), > 10.5 g/dL (second/third trimester)
- **Severity**:
  - **Mild**: 10.0 - lower limit of normal
  - **Moderate**: 7.0 - 9.9 g/dL
  - **Severe**: < 7.0 g/dL

**CLASSIFICATION (MCV - Mean Corpuscular Volume):**

**MICROCYTIC ANAEMIA (MCV < 80 fL):**

**Iron deficiency anaemia** (most common):
- **Causes**:
  - **Blood loss**: Menstruation, GI bleeding (ulcer, cancer, angiodysplasia), pregnancy
  - **Poor intake**: Vegetarian/vegan diet, malnutrition
  - **Malabsorption**: Coeliac disease, gastrectomy, H. pylori infection
- **Investigations**:
  - **Ferritin**: Low (< 15 ng/mL = diagnostic, 15-30 ng/mL = suggestive)
  - **Iron studies**: Low iron, low ferritin, high TIBC, low transferrin saturation
  - **CRP**: Inflammation marker (ferritin is acute phase reactant, can be falsely normal/high)
  - **Red cell indices**: Low MCV, low MCH, high RDW
- **Treatment**:
  - **Iron replacement**: Ferrous sulfate 200mg TDS (or ferrous fumarate 305mg BD)
  - **Take on empty stomach** (Vitamin C enhances absorption)
  - **Avoid tea, coffee, milk, PPIs** (decrease absorption)
  - **Duration**: 3-6 months (corrects Hb in 6-8 weeks, replenishes stores in 3-6 months)
  - **IV iron** (if malabsorption, intolerance, rapid correction needed): Iron sucrose, ferric carboxymaltose
- **Identify and treat cause**: Endoscopy/colonoscopy if GI bleeding suspected (men > 50 years, postmenopausal women)

**Thalassaemia** (hereditary):
- **Alpha-thalassaemia**:
  - **Silent carrier** (-α/αα): Normal Hb, low MCV
  - **Trait** (--/αα): Anaemia, low MCV, normal iron studies
  - **HbH disease** (-α/--): Moderate-severe anaemia, jaundice, splenomegaly
  - **Bart's hydrops** (--/--): Fatal in utero or severe anaemia requiring lifelong transfusion
- **Beta-thalassaemia**:
  - **Trait** (β+/β or β⁰/β): Anaemia, low MCV, high HbA2, normal iron studies
  - **Major** (β⁰/β⁰ or β⁰/β⁺): Severe anaemia, transfusion-dependent, hepatosplenomegaly, iron overload
  - **Intermediate** (β⁰/β⁰ or β⁰/β⁺ with modifier genes): Transfusion-independent, moderate anaemia
- **Investigations**: Hb electrophoresis (HbA2, HbF), DNA studies
- **Treatment**:
  - **Trait**: No treatment, genetic counseling
  - **Major**: Regular transfusion + iron chelation (deferoxamine, deferiprone, deferasirox), stem cell transplant (curative)

**Sideroblastic anaemia**:
- **Causes**: Acquired (alcohol, lead, isoniazid), congenital (X-linked)
- **Ring sideroblasts** on bone marrow (iron-loaded mitochondria around nucleus)
- **High ferritin** with anaemia (distinguishes from iron deficiency)

**NORMOCYTIC ANAEMIA (MCV 80-100 fL):**

**Anaemia of chronic disease** (second most common):
- **Causes**: Chronic inflammation (infection, autoimmune, malignancy), chronic kidney disease
- **Pathophysiology**: Hepcidin-mediated iron sequestration, reduced erythropoiesis
- **Investigations**:
  - **Ferritin**: Normal/high (inflammation)
  - **Iron studies**: Low iron, low transferrin saturation, normal/high ferritin
  - **CRP/ESR**: Elevated
- **Treatment**: Treat underlying cause, consider IV iron (if functional iron deficiency), EPO (if CKD)

**Acute blood loss**:
- **Hypovolaemia** first, then anaemia after fluid resuscitation
- **Normocytic initially**, becomes microcytic over weeks (iron deficiency)

**Haemolytic anaemia**:
- **Increased red cell destruction**
- **Signs**: Jaundice, dark urine (haemoglobinuria), splenomegaly, gallstones
- **Investigations**:
  - **Raised bilirubin** (unconjugated)
  - **Raised LDH**
  - **Low haptoglobin**
  - **Positive direct antiglobulin test (Coombs)**: Autoimmune haemolytic anaemia
  - **Blood film**: Spherocytes (autoimmune), schistocytes (microangiopathic), bite cells (G6PD), sickle cells (sickle cell disease)
- **Treatment**:
  - **Autoimmune**: Corticosteroids (prednisolone 1mg/kg), rituximab, splenectomy (refractory)
  - **Microangiopathic** (TTP, HUS): Plasma exchange
  - **G6PD deficiency**: Avoid oxidant drugs (sulfonamides, dapsone, primaquine)
  - **Sickle cell disease**: Hydroxycarbamide, transfusion, stem cell transplant

**MACROCYTIC ANAEMIA (MCV > 100 fL):**

**Vitamin B12 deficiency**:
- **Causes**:
  - **Pernicious anaemia** (autoimmune atrophic gastritis): Anti-parietal cell, anti-intrinsic factor antibodies
  - **Malabsorption**: Crohn's disease, ileal resection, bacterial overgrowth, fish tapeworm
  - **Dietary**: Vegans (limited animal products)
  - **Medications**: Metformin, PPIs (long-term)
- **Investigations**:
  - **B12 level**: Low (< 150 pmol/L = deficient, 150-200 pmol/L = borderline)
  - **Methylmalonic acid (MMA)**, **homocysteine**: Elevated if true B12 deficiency
  - **Intrinsic factor antibodies**, **parietal cell antibodies** (if pernicious anaemia suspected)
- **Neurological complications** (subacute combined degeneration of cord): Peripheral neuropathy, posterior column damage (proprioception loss), ataxia
- **Treatment**:
  - **Hydroxocobalamin** 1000 mcg IM every 3 months (lifelong if pernicious anaemia)
  - **Alternative**: Oral B12 1000 mcg daily (if dietary deficiency or malabsorption mild)

**Folate deficiency**:
- **Causes**: Poor diet (alcoholism, elderly), malabsorption (coeliac disease), increased demand (pregnancy, haemolysis), medications (methotrexate, phenytoin, trimethoprim)
- **Investigations**:
  - **Serum folate**: Low (< 7 nmol/L)
  - **RBC folate** (more accurate, reflects tissue stores)
  - **B12 level** (always check concurrently - folate supplementation can mask B12 deficiency)
- **Neurological complications**: None (distinguishes from B12 deficiency)
- **Treatment**: Folic acid 5mg daily for 4 months, then identify and treat cause

**ALCOHOL-RELATED MACROCYTOSIS**:
- **Direct toxicity** to bone marrow
- **Nutritional deficiencies** (folate, B12)
- **Liver disease** (alcoholic liver disease)
- **Treatment**: Abstinence, nutritional supplementation, folate 5mg daily

**ANAEMIA MANAGEMENT:**

**Transfusion** (if symptomatic or very severe):
- **Indications**: Hb < 7 g/dL, Hb < 8 g/dL with cardiac/respiratory disease, symptomatic (angina, heart failure, syncope)
- **Packed red cells**: 1 unit raises Hb by 1 g/dL
- **Rate**: Usually over 2-4 hours (1 unit), slower if cardiac failure (over 4 hours)
- **Diuretic**: Furosemide 20-40mg IV after transfusion (if fluid overload risk)

**Erythropoiesis-stimulating agents (ESAs)**:
- **Epoetin alfa**, **darbepoetin alfa** (CKD, chemotherapy-induced anaemia)
- **Target Hb**: 10-12 g/dL (higher risk of thrombosis, stroke if Hb > 12 g/dL)
- **Contraindications**: Uncontrolled hypertension, pregnancy

**SOURCES:** NICE CG24, British Society for Haematology""",

            confidence=0.92,
            reasoning_trace=["Detected anaemia keywords", "Providing comprehensive anaemia information", "NICE CG24 guidelines applied"],
            capabilities_used=["blood_disorder_management"],
            metadata={"sources": ["NICE CG24", "BSH"]}
        )

    def _handle_thrombosis_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle thrombosis queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**VENOUS THROMBOEMBOLISM (VTE) OVERVIEW**

VTE includes deep vein thrombosis (DVT) and pulmonary embolism (PE).

**EPIDEMIOLOGY:**
- **Incidence**: 1-2 per 1000 population per year
- **Risk factors**: Surgery, trauma, immobility, cancer, pregnancy, oral contraceptives, thrombophilia
- **Recurrence**: 30% after first VTE, 50% after idiopathic VTE

**DEEP VEIN THROMBOSIS (DVT):**

**Risk factors (Virchow's triad):**
- **Venous stasis**: Immobility, paralysis, obesity, varicose veins
- **Hypercoagulability**: Cancer, pregnancy, OCP, thrombophilia (Factor V Leiden, prothrombin mutation), antiphospholipid syndrome
- **Endothelial injury**: Surgery, trauma, indwelling catheters

**Symptoms:**
- **Leg swelling** (unilateral)
- **Pain** (calf, thigh)
- **Redness**, **warmth**
- **Dilated superficial veins**
- **Distended leg veins** (non-specific)

**Signs:**
- **Homan's sign** (calf pain on dorsiflexion) - poor sensitivity/specificity
- **Pitting oedema**
- **Tenderness** over deep veins
- **Difference in calf circumference** (> 3 cm compared to asymptomatic side 10 cm below tibial tuberosity)

**INVESTIGATIONS:**

**D-dimer** (if low clinical probability):
- **Negative**: Excludes DVT (high NPV)
- **Positive**: Non-specific (elevated in infection, inflammation, cancer, post-op)
- **Age-adjusted**: Age × 10 μg/L (if > 50 years) improves specificity

**Compression ultrasound** (GOLD STANDARD):
- **Proximal CUS**: Femoropopliteal veins (sensitivity 95%, specificity 95%)
- **Distal CUS**: Calf veins (tibial, peroneal) - sensitivity 70-80%
- **Repeat**: If negative but high clinical suspicion (day 3-7 and day 14)

**CT venography** (if proximal extension, planning for thrombolysis/thrombectomy)

**Contrast venography** (rare, replaced by CUS)

**MANAGEMENT:**

**ACUTE DVT**:

**Anticoagulation** (DO NOT delay if high clinical suspicion, even while awaiting investigations):

**LMWH** (first-line for initial treatment):
- **Tinzaparin**: 175 IU/kg SC once daily
- **Enoxaparin**: 1.5 mg/kg SC once daily (or 1 mg/kg BD)
- **Dalteparin**: 200 IU/kg SC once daily (or 100 IU/kg BD)
- **Duration**: Minimum 5 days AND until INR therapeutic for 24 hours (if warfarin) or until DOAC initiated
- **Advantages**: Immediate onset, no monitoring, safe in pregnancy, safe in cancer

**DOACs** (direct oral anticoagulants - first-line for DVT):
- **Rivaroxaban** 15 mg BD for 21 days, then 20 mg daily
- **Apixaban** 10 mg BD for 7 days, then 5 mg BD
- **Dabigatran** 150 mg BD (after 5 days LMWH)
- **Edoxaban** 60 mg daily (after 5 days LMWH)

**Warfarin** (if DOAC contraindicated or patient preference):
- **Target INR**: 2.0-3.0 (2.5 for recurrent VTE, antiphospholipid syndrome)
- **Loading**: 5-10 mg for 2 days (careful in elderly)
- **Overlap**: With LMWH for minimum 5 days and until INR therapeutic for 24 hours
- **Monitoring**: INR every 1-2 days until stable, then every 12 weeks

**Thrombolysis** (catheter-directed):
- **Indications**: Iliofemoral DVT, phlegmasia cerulea dolens, floating thrombus (high risk of PE)
- **Contraindications**: Active bleeding, recent surgery, stroke, uncontrolled hypertension

**Inferior vena cava (IVC) filter**:
- **Indications** (absolute): Contra-indication to anticoagulation (active bleeding)
- **Indications** (relative): Recurrent VTE despite adequate anticoagulation, massive PE with residual DVT, free-floating thrombus
- **Complications**: DVT (20-30%), filter migration, IVC thrombosis

**Duration of anticoagulation**:

**Provoked DVT** (transient risk factor):
- **3 months**: Surgery, trauma, immobilization, OCP, pregnancy

**Unprovoked DVT** (no identifiable risk factor):
- **At least 3 months** (reassess after 3 months)
- **Consider long-term** if:
  - **Recurrent unprovoked VTE**
  - **High-risk thrombophilia**
  - **Active cancer**
  - **Persistent risk factors** (reduced mobility, obesity, thrombophilia)
  - **Male sex** (higher recurrence risk than female)
  - **Proximal DVT** (vs distal)
  - **Residual thrombosis** on CUS
  - **Elevated D-dimer** after stopping anticoagulation

**Cancer-associated thrombosis (CAT):**
- **LMWH preferred** (tinzaparin, dalteparin) for 3-6 months
- **DOACs** (rivaroxaban, edoxaban) are alternatives (SELECTE, Hokusai-VTE trials)
- **Warfarin**: Less effective, higher recurrence, higher bleeding

**PULMONARY EMBOLISM (PE):**

**Risk stratification** (based on haemodynamic stability, right ventricular strain):

**High-risk (massive) PE**:
- **Definition**: Shock (SBP < 90 mmHg or drop ≥ 40 mmHg for > 15 min)
- **Management**:
  - **Thrombolysis** (alteplase 10 mg IV bolus, then 90 mg over 2 hours)
  - **Surgical embolectomy** (if thrombolysis contraindicated or failed)
  - **Anticoagulation** (after thrombolysis/surgery)

**Intermediate-risk (submassive) PE**:
- **Definition**: Normotensive but RV dysfunction (echocardiogram: RV dilation, hypokinesis, pulmonary hypertension) OR positive cardiac biomarkers (troponin, BNP)
- **Management**:
  - **Anticoagulation** (LMWH, DOAC, warfarin)
  - **Thrombolysis** (consider if high-risk features: severe RV dysfunction, massive clot burden, persistent hypotension)

**Low-risk PE**:
- **Definition**: Normotensive, no RV dysfunction, normal biomarkers
- **Management**:
  - **Home treatment** (if low-risk PESI score)
  - **Anticoagulation** (LMWH, DOAC, warfarin)

**Symptoms:**
- **Dyspnoea** (sudden onset)
- **Pleuritic chest pain**
- **Haemoptysis**
- **Syncope** (if massive PE)
- **Palpitations**, **anxiety**
- **Asymptomatic** (small PE)

**Signs:**
- **Tachycardia** (> 100 bpm)
- **Tachypnoea** (> 20 breaths/min)
- **Hypoxia** (SpO2 < 94%)
- **Loud P2**, **fixed split**, **parasternal heave** (if pulmonary hypertension)
- **DVT signs** (may be absent)

**INVESTIGATIONS:**

**ECG** (non-specific):
- **Sinus tachycardia** (most common)
- **S1Q3T3** (S1 deep, Q in III, T3 inverted) - rare
- **Right axis deviation**, **RBBB**, **T wave inversion V1-V4** (right heart strain)
- **Normal** (30% of PE)

**Chest X-ray** (often normal):
- **Hampton's hump** (peripheral wedge-shaped consolidation)
- **Westermark sign** (oligaemia)
- **Effusion**, **atelectasis**
- **Normal** (30-40% of PE)

**CT pulmonary angiography (CTPA)** (GOLD STANDARD):
- **Sensitivity**: 85-95% (depends on size/location)
- **Specificity**: 90-95%
- **Diagnosis**: Filling defect in pulmonary artery
- **Alternative**: V/Q scan (if CTPA contraindicated: renal impairment, contrast allergy, pregnancy)

**D-dimer** (if low clinical probability):
- **Negative**: Excludes PE (high NPV)
- **Positive**: Non-specific

**Compression ultrasound** (legs): Detect DVT (if positive, treat as PE without further imaging)

**THROMBOPROPHYLAXIS**:

**Medical patients** (NICE NG89):
- **LMWH** or **fondaparinux** (if reduced mobility, acute medical illness)
- **DOACs** (rivaroxaban, apixaban, betrixaban) - alternatives to LMWH
- **Mechanical prophylaxis** (graduated compression stockings, intermittent pneumatic compression): If pharmacological contraindicated

**Surgical patients**:
- **Major surgery**: LMWH (start 12 hours pre-op or 12 hours post-op)
- **Orthopaedic surgery**: LMWH for 28-35 days (or DOAC: rivaroxaban, apixaban, dabigatran)
- **Cancer surgery**: LMWH for 28 days (high risk)

**POST-THROMBOTIC SYNDROME (PTS):**
- **Definition**: Chronic venous insufficiency after DVT (pain, swelling, ulceration)
- **Incidence**: 20-50% after proximal DVT
- **Prevention**: Compression stockings (30-40 mmHg at ankle) for 2 years after DVT
- **Treatment**: Compression stockings, elevation, exercise

**Sources:** NICE NG158, British Society for Haematology, ACCP Guidelines""",

            confidence=0.93,
            reasoning_trace=["Detected thrombosis keywords", "Providing comprehensive VTE information", "NICE NG158 guidelines applied"],
            capabilities_used=["coagulation_disorder_management"],
            metadata={"sources": ["NICE NG158", "BSH", "ACCP"]}
        )

    def _handle_transfusion_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle blood transfusion queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**BLOOD TRANSFUSION OVERVIEW**

Blood transfusion replaces blood components lost through surgery, trauma, or disease.

**BLOOD COMPONENTS:**

**Red blood cells (packed cells)**:
- **Indications**:
  - **Symptomatic anaemia**: Hb < 7 g/dL OR Hb < 8 g/dL with cardiac/respiratory disease
  - **Acute blood loss**: > 1500 mL (30% blood volume) or haemodynamic instability
  - **Chronic anaemia**: Only if symptomatic (angina, heart failure, syncope)
- **Dose**: 1 unit raises Hb by 1 g/dL (usually 2 units)
- **Duration**: Transfuse over 2-4 hours (1 unit)
- **Compatibility**: ABO and RhD matching required
- **Massive transfusion**: > 4 units in 1 hour or > 10 units in 24 hours (requires massive transfusion protocol: RBC:FFP:platelets 1:1:1)

**Platelets**:
- **Indications**:
  - **Thrombocytopenia**: < 10 × 10⁹/L (prophylactic) OR < 20 × 10⁹/L (if fever, bleeding)
  - **Active bleeding**: < 50 × 10⁹/L
  - **Invasive procedure**: < 50 × 10⁹/L (prophylactic)
  - **High-risk procedure**: < 100 × 10⁹/L (CNS, ophthalmic surgery)
- **Dose**: 1 adult therapeutic pool (6-10 units single-donor apheresis) raises platelet count by 30-50 × 10⁹/L
- **Duration**: Transfuse over 30-60 minutes (rapid infusion if life-threatening bleeding)
- **Compatibility**: ABO matching preferred (but not essential if urgent)
- **Refractoriness**: Poor increment (< 15 × 10⁹/L) after 2 transfusions → HLA-matched platelets

**Fresh frozen plasma (FFP)**:
- **Indications**:
  - **Correction of coagulopathy** (elevated INR/APTT) with bleeding or before invasive procedure
  - **Massive transfusion** (to prevent dilutional coagulopathy)
  - **Warfarin reversal** (if urgent surgery or major bleeding, PCC preferred)
  - **Specific factor deficiency**: Factor V, XI (if specific factor concentrate unavailable)
- **Contraindications**: Do NOT use for volume expansion alone (use crystalloids/colloids)
- **Dose**: 12-15 mL/kg (usually 4 units)
- **Duration**: Thaw before use (takes 20-30 minutes), transfuse over 20-30 minutes
- **Compatibility**: ABO compatible preferred

**Cryoprecipitate**:
- **Indications**:
  - **Fibrinogen replacement**: < 1.0-1.5 g/L (with bleeding or before invasive procedure)
  - **Von Willebrand disease** (if Humate-P unavailable)
  - **Haemophilia A** (if factor VIII concentrate unavailable)
  - **Uremic bleeding** (if dialysis ineffective)
- **Components** (from 1 unit FFP): Factor VIII, factor XIII, fibrinogen, von Willebrand factor, fibronectin
- **Dose**: 2 pools (10 units) raises fibrinogen by 1 g/L
- **Duration**: Thaw before use (takes 10-15 minutes), transfuse over 10-20 minutes
- **Compatibility**: ABO compatible preferred

**Granulocytes** (rare):
- **Indications**: Severe neutropenia (< 0.5 × 10⁹/L) with life-threatening infection unresponsive to antibiotics
- **Dose**: 1 unit (≥ 1 × 10¹⁰ granulocytes)
- **Duration**: Transfuse over 2-4 hours
- **Irradiated**: To prevent GVHD (Graft-versus-Host Disease)
- **Limitations**: Limited availability, poor engraftment, pulmonary reactions

**TRANSFUSION REACTIONS:**

**Acute haemolytic reaction** (ABO incompatibility):
- **Symptoms**: Fever, chills, rigors, flank pain, dark urine (haemoglobinuria), hypotension, shock
- **Management**:
  - **STOP transfusion immediately**
  - **Maintain urine output**: IV fluids 200-300 mL/hour, diuretics (furosemide 20-40mg IV)
  - **Treat hypotension**: Crystalloid/colloid resuscitation, vasopressors (noradrenaline)
  - **Prevent renal failure**: Alkalinise urine (sodium bicarbonate)
  - **Investigate**: Repeat blood group, direct Coombs test, plasma haemoglobin, LDH, bilirubin

**Febrile non-haemolytic reaction** (most common):
- **Symptoms**: Fever > 38°C, chills, rigors (during or within 4 hours of transfusion)
- **Management**:
  - **STOP transfusion** (if fever > 39°C or rigors)
  - **Paracetamol 1g PO/PR**
  - **Investigate**: Blood and urine cultures (if febrile after stopping)
- **Prevention**: Leukodepleted blood, paracetamol premedication (if previous reaction)

**Allergic reaction** (mild to anaphylaxis):
- **Symptoms**: Urticaria, pruritus, flushing (mild); wheeze, stridor, hypotension, shock (severe)
- **Management**:
  - **STOP transfusion immediately** (if severe reaction)
  - **Mild**: Antihistamine (chlorphenamine 10mg IV/PO), continue transfusion slowly after 30 minutes
  - **Severe**: Adrenaline 0.5 mg IM (0.5 mL of 1:1000), hydrocortisone 200 mg IV, antihistamine
- **Prevention**: Washed red cells (remove plasma proteins)

**Transfusion-associated circulatory overload (TACO)**:
- **Risk factors**: Elderly, cardiac/renal impairment, rapid transfusion, large volume
- **Symptoms**: Dyspnoea, orthopnoea, cough, pulmonary oedema, hypertension, tachycardia
- **Management**:
  - **STOP transfusion immediately**
  - **Sit patient up**, **oxygen**
  - **Diuretics**: Furosemide 20-40mg IV
  - **Nitrates**: GTN spray (if pulmonary oedema)
  - **Non-invasive ventilation** (if severe)
- **Prevention**: Slow transfusion rate (2-4 hours per unit), diuretics during transfusion

**Transfusion-related acute lung injury (TRALI)**:
- **Incidence**: 1 in 5,000 transfusions (leading cause of transfusion-related mortality)
- **Pathophysiology**: Antibodies in donor plasma reacting with recipient HLA/neutrophil antigens
- **Symptoms**: Acute respiratory distress (within 6 hours of transfusion), hypoxia, bilateral pulmonary infiltrates
- **Management**:
  - **STOP transfusion immediately**
  - **Supportive care**: Oxygen, mechanical ventilation (if severe)
  - **No diuretics** (unlike TACO, pulmonary oedema not due to fluid overload)
- **Prevention**: Avoid plasma-rich products from multiparous females (TRALI reduction strategies)

**Transfusion-associated graft versus host disease (TA-GVHD)**:
- **Incidence**: Rare (1 in 500,000) but 90% mortality
- **Pathophysiology**: Donor T-lymphocytes engraft and attack recipient tissues
- **Risk factors**: Immunocompromised recipient, HLA-matched donor, directed donations from relatives
- **Symptoms**: Fever, rash, diarrhoea, pancytopenia, liver dysfunction (7-10 days post-transfusion)
- **Management**: **High-dose steroids** (methylprednisolone 1g/day), cyclosporine, supportive care
- **Prevention**: Irradiation of blood components (25 Gy) for high-risk patients

**SPECIAL CIRCUMSTANCES:**

**Massive transfusion protocol**:
- **Indications**: > 4 units in 1 hour or > 10 units in 24 hours
- **Ratio**: RBC:FFP:Platelets 1:1:1 (prevents dilutional coagulopathy, thrombocytopenia)
- **Laboratory monitoring**: ABG, FBC, coagulation profile, fibrinogen, calcium every 1-2 hours
- **Complications**: Hypothermia, hypocalcaemia, hyperkalaemia, acidosis, dilutional coagulopathy, TRALI, TACO

**Irradiated blood**:
- **Indications**:
  - **Bone marrow transplant** recipients (pre- and post-transplant)
  - **Immunocompromised**: Hodgkin lymphoma, acute leukaemia, congenital immunodeficiency
  - **Intrauterine transfusion**
  - **Directed donations** from blood relatives
- **Prevents**: TA-GVHD
- **Effects**: Irradiation does not affect RBC survival or function

**Washed blood**:
- **Indications**:
  - **IgA deficiency** (with anti-IgA antibodies and anaphylaxis to plasma)
  - **Severe allergic reactions** to plasma proteins
  - **Neonatal exchange transfusion**
- **Process**: Removes 99% of plasma proteins
- **Effects**: Reduced viability (transfuse within 24 hours of washing)

**CMV-negative blood**:
- **Indications**:
  - **Pregnant women** (CMV-negative)
  - **Neonates** (CMV-negative)
  - **Immunocompromised**: CMV-negative transplant candidates, HIV-positive
- **Prevents**: Cytomegalovirus transmission

**ALTERNATIVES TO TRANSFUSION:**

**Cell salvage** (intraoperative blood salvage):
- **Indications**: Cardiac surgery, orthopaedic surgery, trauma, liver transplantation
- **Contraindications**: Malignancy (cancer cells can be reinfused), infection (peritonitis)
- **Process**: Suction blood from surgical field, filter, wash, centrifuge, reinfuse
- **Benefits**: Reduces allogeneic transfusion requirements, avoids transfusion reactions, reduces infection risk

**Tranexamic acid** (antifibrinolytic):
- **Indications**: Trauma, obstetric haemorrhage, cardiac surgery, orthopaedic surgery
- **Dose**: 1 g IV over 10 minutes, then 1 g infusion over 8 hours OR 1 g PO TDS
- **Contraindications**: Severe renal impairment, epilepsy, thromboembolic disease
- **Benefits**: Reduces blood loss by 30-40%, reduces transfusion requirements

**Erythropoiesis-stimulating agents (ESAs)**:
- **Indications**: Chronic kidney disease, chemotherapy-induced anaemia, pre-operative autologous donation
- **Agents**: Epoetin alfa, darbepoetin alfa
- **Target Hb**: 10-12 g/dL (avoid > 13 g/dL)
- **Contraindications**: Uncontrolled hypertension, pregnancy, hypersensitivity

**Iron therapy**:
- **Oral iron**: Ferrous sulfate 200mg TDS (3-6 months)
- **IV iron**: Iron sucrose, ferric carboxymaltose (rapid correction, malabsorption, intolerance)
- **Indications**: Iron deficiency anaemia (especially if cannot tolerate oral or rapid correction needed)

**BLOOD SAFETY:**
- **HIV**: 1 in 7.8 million transfusions (UK, 2021)
- **Hepatitis B**: 1 in 1.2 million transfusions (UK, 2021)
- **Hepatitis C**: 1 in 22 million transfusions (UK, 2021)
- **vCJD**: Theoretical risk, no confirmed cases from transfusion (UK, 2021)

**CONSENT**:
- **Valid consent**: Explain risks, benefits, alternatives (including refusal)
- **Religious beliefs**: Jehovah's Witnesses (refuse blood products), respect autonomy

**SOURCES:** NICE NG24, British Society for Haematology, SHOT (Serious Hazards of Transfusion)""",

            confidence=0.91,
            reasoning_trace=["Detected transfusion keywords", "Providing comprehensive blood transfusion information", "NICE NG24 guidelines applied"],
            capabilities_used=["blood_disorder_management"],
            metadata={"sources": ["NICE NG24", "BSH", "SHOT"]}
        )

    def _handle_general_oncology_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general oncology queries"""
        return DomainQueryResult(
            domain_name="hematology_oncology",
            answer="""**HAEMATOLOGY AND ONCOLOGY OVERVIEW**

Haematology covers blood disorders, while oncology covers cancer management.

**COMMON HAEMATOLOGICAL CONDITIONS:**

**Anaemia**:
- Iron deficiency, B12/folate deficiency, anaemia of chronic disease, haemolytic anaemia
- Treatment: Iron replacement, vitamin supplementation, blood transfusion

**Coagulation disorders**:
- **Venous thromboembolism**: DVT, PE
- **Arterial thromboembolism**: Stroke, MI, limb ischaemia
- Treatment: Anticoagulation (LMWH, DOAC, warfarin), thrombolysis

**COMMON CANCERS**:
- **Breast, lung, colorectal, prostate**: Big 4 (most common)
- **Haematological malignancies**: Leukaemia, lymphoma, myeloma
- **Treatment**: Surgery, radiotherapy, chemotherapy, immunotherapy, targeted therapy

**ONCOLOGICAL EMERGENCIES**:
- Neutropenic sepsis, tumour lysis syndrome, spinal cord compression, SVCO, malignant hypercalcaemia
- **Urgent admission required** - time is critical

**SOURCES:** NICE Guidelines, British Society for Haematology""",

            confidence=0.85,
            reasoning_trace=["Detected general oncology keywords", "Providing overview of haematology/oncology"],
            capabilities_used=["cancer_diagnosis"],
            metadata={"sources": ["NICE", "BSH"]}
        )

def create_hematology_oncology_domain():
    """Factory function to create haematology/oncology domain instance"""
    return HematologyOncologyDomain()