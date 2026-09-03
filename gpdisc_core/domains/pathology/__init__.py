"""
Pathology/Lab Medicine Domain for GPDISC

Comprehensive pathology and laboratory medicine domain covering all aspects of
diagnostic pathology, clinical biochemistry, haematology, microbiology, and
blood transfusion science.

Evidence-based: RCPath (Royal College of Pathologists), AABB, BCSH, UK NEQAS,
ASCP, CAP, NICE Guidelines
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class PathologyDomain(BaseDomainModule):
    """
    Pathology and Laboratory Medicine Domain

    Covers all aspects of pathology and laboratory medicine including:
    - Clinical biochemistry (blood tests, electrolytes, liver function, etc.)
    - Haematology (blood disorders, anaemia, coagulation)
    - Microbiology (infection diagnosis, antimicrobial susceptibility)
    - Histopathology (tissue diagnosis, cancer pathology)
    - Blood transfusion (blood grouping, crossmatching, transfusion reactions)
    - Immunology (autoimmune disease, allergy testing)
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="pathology",
            version="1.0.0",
            dependencies=[],
            description="Pathology and laboratory medicine - Clinical biochemistry, haematology, microbiology, histopathology, transfusion science",
            keywords=[
                # Laboratory tests
                "blood test", "bloods", "lab test", "laboratory", "pathology",
                "biochemistry", "blood count", "fbc", "cbc", "u&e", "electrolytes",
                "lft", "liver function", "bone profile", "hba1c", "glucose",
                "cholesterol", "lipid profile", "thyroid", "tsh", "t4", "t3",
                "crp", "esr", "inflammatory markers",
                # Haematology
                "haematology", "blood count", "haemoglobin", "haematocrit",
                "anaemia", "iron", "b12", "folate", "ferritin",
                "coagulation", "inr", "aptt", "pt", "d-dimer",
                "platelet", "thrombocytopenia", "thrombocythaemia",
                "white cell", "leucocytosis", "leucopenia", "neutrophil", "lymphocyte",
                # Microbiology
                "microbiology", "culture", "sensitivity", "antibiotic",
                "infection", "sepsis", "blood culture", "urine culture", "msu",
                "wound swab", "throat swab", "sputum culture",
                "covid test", "covid pcr", "influenza",
                # Histopathology
                "histopathology", "biopsy", "histology", "cytology",
                "cancer diagnosis", "tumour", "malignancy", "histology report",
                "polyp", "lesion", "skin biopsy", "colonic biopsy",
                # Transfusion
                "blood transfusion", "blood group", "crossmatch", "compatibility",
                "transfusion reaction", "blood products", "packed cells", "ffp",
                "platelet transfusion", "transfusion consent",
                # Specific tests
                "troponin", "d-dimer", "psa", "afp", "cea", "ca125",
                "tumour marker", "cancer marker", "calcium",
                "drug level", "therapeutic drug monitoring", "digoxin", "gentamicin",
                "arterial blood gas", "abg", "venous blood gas", "vbg",
                # Interpretation
                "abnormal", "elevated", "low", "high", "result", "reference range",
                "interpret", "explain", "mean", "diagnosis"
            ],
            capabilities=[
                "test_interpretation", "biochemistry_review", "haematology_review",
                "microbiology_guidance", "transfusion_science", "histopathology_guidance",
                "reference_ranges", "clinical_correlation"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        query_lower = query.lower()

        # EMERGENCY: Transfusion reaction
        if any(term in query_lower for term in ["transfusion reaction", "blood transfusion reaction",
                                                   "acute haemolytic transfusion reaction", "anaphylaxis"]):
            return self._handle_transfusion_reaction(query, context)

        # EMERGENCY: Hyperkalaemia
        if any(term in query_lower for term in ["hyperkalaemia", "hyperkalemia", "high potassium",
                                                   "elevated potassium", "k+", "raised potassium"]):
            return self._handle_hyperkalaemia(query, context)

        # EMERGENCY: Severe anaemia
        if any(term in query_lower for term in ["severe anaemia", "hb 4", "hb 5", "haemoglobin 4",
                                                   "haemoglobin 5", "very low hb"]):
            return self._handle_severe_anaemia(query, context)

        # EMERGENCY: Thrombocytopenia with bleeding
        if any(term in query_lower for term in ["thrombocytopenia bleeding", "low platelets bleeding",
                                                   "platelet 10", "platelet 5", "very low platelets"]):
            return self._handle_thrombocytopenia_bleeding(query, context)

        # TROPONIN (acute coronary syndrome)
        if any(term in query_lower for term in ["troponin", "hs troponin", "cardiac enzymes",
                                                   "raised troponin", "elevated troponin"]):
            return self._handle_troponin(query, context)

        # D-DIMER (pulmonary embolism, DVT)
        if any(term in query_lower for term in ["d-dimer", "d dimmer", "ddimer", "raised d-dimer",
                                                   "d-dimer result", "pe rule out"]):
            return self._handle_d_dimer(query, context)

        # ARTERIAL BLOOD GAS (ABG)
        if any(term in query_lower for term in ["abg", "arterial blood gas", "acidosis", "alkalosis",
                                                   "respiratory acidosis", "metabolic acidosis"]):
            return self._handle_abg(query, context)

        # LIVER FUNCTION TESTS (LFT)
        if any(term in query_lower for term in ["lft", "liver function", "elevated liver enzymes",
                                                   "raised alt", "raised ast", "high bilirubin"]):
            return self._handle_lft(query, context)

        # THYROID FUNCTION TESTS (TFT)
        if any(term in query_lower for term in ["tsh", "thyroid", "hypothyroid", "hyperthyroid",
                                                   "thyroxine", "t4", "t3", "raised tsh"]):
            return self._handle_tft(query, context)

        # HAEMOGLOBIN A1c (diabetes)
        if any(term in query_lower for term in ["hba1c", "a1c", "glycated haemoglobin",
                                                   "diabetes", "raised a1c"]):
            return self._handle_hba1c(query, context)

        # FULL BLOOD COUNT (FBC)
        if any(term in query_lower for term in ["fbc", "blood count", "full blood count", "cbc",
                                                   "haemoglobin", "white cell", "platelet"]):
            return self._handle_fbc(query, context)

        # INR/COAGULATION
        if any(term in query_lower for term in ["inr", "international normalised ratio", "coagulation",
                                                   "warfarin", "bleeding time", "aptt"]):
            return self._handle_inr(query, context)

        # C-REACTIVE PROTEIN (CRP)
        if any(term in query_lower for term in ["crp", "c-reactive protein", "inflammatory marker",
                                                   "raised crp", "elevated crp"]):
            return self._handle_crp(query, context)

        # URINE MICROSCOPY, CULTURE AND SENSITIVITY (MC&S)
        if any(term in query_lower for term in ["msu", "urine culture", "uti", "urinary tract infection",
                                                   "dipstick", "nitrites", "leucocytes"]):
            return self._handle_urine_culture(query, context)

        # BLOOD CULTURE
        if any(term in query_lower for term in ["blood culture", "sepsis screen", "bacteraemia",
                                                   "positive blood culture"]):
            return self._handle_blood_culture(query, context)

        # TUMOUR MARKERS
        if any(term in query_lower for term in ["tumour marker", "psa", "afp", "cea", "ca125",
                                                   "cancer marker", "raised psa"]):
            return self._handle_tumour_markers(query, context)

        # GENERAL TEST INTERPRETATION
        else:
            return self._handle_general_pathology(query, context)

    def _handle_transfusion_reaction(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Blood transfusion reaction management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**TRANSFUSION REACTION - EMERGENCY MANAGEMENT**

**IMMEDIATE ACTION (STOP TRANSFUSION):**

1. **STOP the transfusion immediately**

2. **ASSESS ABCDE:**
   - **Airway:** Assess patency, prepare for intubation
   - **Breathing:** Oxygen 15 L/min, respiratory rate, auscultation
   - **Circulation:** BP, heart rate, ECG, IV access
   - **Disability:** Conscious level, GCS, pupil response
   - **Exposure:** Full examination, skin inspection (urticaria, flushing, rash)

3. **CALL FOR HELP:**
   - Alert senior doctor/consultant
   - Contact transfusion laboratory immediately
   - Activate emergency team if patient deteriorating

4. **INITIAL MANAGEMENT:**
   - **Maintain IV access:** Keep IV line open with normal saline (0.9% NaCl)
   - **DO NOT** flush the transfusion line (may exacerbate reaction)
   - **Send blood samples:** Pre-transfusion sample (clotted and EDTA), post-transfusion sample (clotted and EDTA), urine for haemoglobinuria
   - **Return blood unit:** Send the transfused unit and giving set to transfusion laboratory for investigation

**DIFFERENT TYPES OF TRANSFUSION REACTIONS:**

**1. ACUTE HAEMOLYTIC TRANSFUSION REACTION (AHTR):**

**Causes:** ABO incompatibility (most commonly), Rh incompatibility

**Clinical features (onset within minutes to hours):**
- **Fever, chills, rigors**
- **Pain:** IV site, back, flank, chest
- **Haemoglobinuria:** Red/brown urine (free haemoglobin)
- **Hypotension, tachycardia**
- **Disseminated intravascular coagulation (DIC):** Bleeding, petechiae
- **Shock, renal failure, cardiac arrest**

**Management:**
- **STOP transfusion immediately**
- **Aggressive IV fluid resuscitation:** Normal saline 1-2 L bolus
- **Maintain urine output:** >100 mL/hour (may require diuretics)
- **Treat hypotension:** Vasopressors if fluid-refractory (noradrenaline)
- **Treat DIC:** Replace clotting factors (FFP, platelets, cryoprecipitate)
- **Consider dialysis:** If acute kidney injury (hyperkalaemia, fluid overload)
- **Inform senior clinician and transfusion laboratory immediately**

**Investigation:**
- **Direct antiglobulin test (DAT/Coombs test):** Positive
- **Elution:** Identify offending antibody
- **Repeat blood grouping:** Confirm ABO compatibility

**2. ANAPHYLACTIC REACTION:**

**Causes:** IgA deficiency (anti-IgA antibodies), allergic reaction to plasma proteins

**Clinical features (onset within seconds to minutes):**
- **Respiratory distress:** Stridor, wheeze, dyspnoea
- **Cardiovascular collapse:** Hypotension, tachycardia, shock
- **Cutaneous:** Urticaria, flushing, angioedema
- **Gastrointestinal:** Abdominal pain, vomiting, diarrhoea

**Management:**
- **STOP transfusion immediately**
- **IM adrenaline (epinephrine):** 0.5 mg (0.5 mL of 1:1000) IM into anterolateral thigh
- **Repeat adrenaline every 5 minutes if no improvement**
- **Oxygen:** 15 L/min via non-rebreather mask
- **IV fluids:** Crystalloid bolus (500-1000 mL)
- **Antihistamine:** IV chlorphenamine 10 mg (non-urgent)
- **Steroid:** IV hydrocortisone 200 mg (non-urgent)

**3. FEBRILE NON-HAEMOLYTIC TRANSFUSION REACTION (FNHTR):**

**Causes:** Cytokine accumulation in stored blood, anti-HLA or anti-HNA antibodies

**Clinical features (onset during or within 4 hours of transfusion):**
- **Fever:** Temperature rise >1°C above baseline
- **Chills, rigors**
- **No haemolysis, no hypotension**

**Management:**
- **STOP or slow transfusion**
- **Paracetamol:** 1 g PO/IV
- **Consider stopping transfusion:** If symptoms severe or persistent
- **Investigation:** Exclude haemolytic reaction, sepsis

**4. ALLERGIC REACTION (MILD):**

**Causes:** Plasma proteins in transfused blood

**Clinical features:**
- **Urticaria, pruritus**
- **No respiratory distress, no hypotension**

**Management:**
- **Slow or pause transfusion**
- **Antihistamine:** PO cetirizine 10 mg or chlorphenamine 4 mg
- **Consider paracetamol:** For fever
- **Restart transfusion:** If symptoms resolve

**5. TRANSFUSION-ASSOCIATED CIRCULATORY OVERLOAD (TACO):**

**Causes:** Rapid transfusion, volume overload (especially elderly, cardiac/renal impairment)

**Clinical features:**
- **Dyspnoea, orthopnoea**
- **Hypertension, tachycardia**
- **Pulmonary oedema:** Crackles on auscultation, CXR findings
- **Peripheral oedema**

**Management:**
- **STOP transfusion immediately**
- **Sit patient upright**
- **Diuretic:** IV furosemide 40 mg
- **Oxygen:** If hypoxic
- **Consider non-invasive ventilation:** If severe respiratory distress
- **Monitor:** Fluid balance, daily weights

**6. TRANSFUSION-RELATED ACUTE LUNG INJURY (TRALI):**

**Causes:** Anti-HLA or anti-HNA antibodies in donor plasma, neutrophil priming

**Clinical features (onset within 6 hours of transfusion):**
- **Acute hypoxia:** SpO2 <90% on room air
- **Bilateral pulmonary infiltrates:** CXR (pulmonary oedema)
- **No evidence of left atrial hypertension** (differentiate from TACO)
- **Fever, hypotension**

**Management:**
- **STOP transfusion immediately**
- **Supportive care:** Oxygen, respiratory support (may require mechanical ventilation)
- **No diuretics:** Not effective (cardiac function normal)
- **Report to transfusion laboratory:** Donor investigation

**7. SEPTIC REACTION:**

**Causes:** Bacterial contamination of blood unit (especially platelets)

**Clinical features (onset during or within hours of transfusion):**
- **Fever, rigors, hypotension**
- **Shock, DIC**
- **High mortality if untreated**

**Management:**
- **STOP transfusion immediately**
- **Broad-spectrum IV antibiotics:** e.g., meropenem 1 g IV + vancomycin 1 g IV
- **Aggressive supportive care:** IV fluids, vasopressors
- **Blood cultures:** Pre- and post-transfusion, blood unit culture
- **Report to transfusion laboratory:** Immediate notification

**POST-REACTION INVESTIGATION:**

All transfusion reactions require investigation:

1. **Pre-transfusion sample:** Clotted and EDTA (from transfusion laboratory)
2. **Post-transfusion sample:** Clotted and EDTA (repeat group and screen, DAT)
3. **Urine:** For haemoglobinuria
4. **Blood unit:** Return to transfusion laboratory for culture and testing
5. **Fluid:** Remainder of IV fluids/administered medications
6. **Completing transfusion reaction form:** Document details

**PREVENTION:**

- **Correct patient identification:** Wristband, patient confirmation, blood unit check
- **Blood grouping and screening:** Pre-transfusion testing
- **Compatibility testing:** Crossmatch (electronic or serological)
- **Patient education:** Inform healthcare team of previous reactions
- **MedicAlert:** If previous severe reaction (consider alternative products)

**Sources:** BCSH Guidelines, AABB Standards, RCPath Guidelines, SHOT (Serious Hazards of Transfusion) Reports""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "AABB Standards", "RCPath Guidelines", "SHOT Reports"],
                "emergency_protocol": "transfusion_reaction"
            }
        )

    def _handle_hyperkalaemia(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Hyperkalaemia management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**HYPERKALAEMIA - EMERGENCY MANAGEMENT**

**SEVERITY GRADING:**

| Potassium (mmol/L) | Severity | Action |
|--------------------|----------|--------|
| 5.5-5.9 | Mild | Monitor, consider dietary review, medication review |
| 6.0-6.4 | Moderate | Urgent treatment, cardiac monitoring |
| ≥6.5 | Severe | EMERGENCY treatment, continuous cardiac monitoring |

**ECG CHANGES (progressive with increasing severity):**
1. **Peaked T waves** (earliest sign)
2. **Prolonged PR interval**
3. **Loss of P waves**
4. **Widening QRS complex**
5. **Sine wave pattern** (pre-terminal)
6. **Ventricular fibrillation/asystole** (cardiac arrest)

**EMERGENCY MANAGEMENT (K+ ≥6.5 mmol/L OR ECG changes):**

**IMMEDIATE ACTION:**

1. **CARDIAC PROTECTION (within minutes):**
   - **Calcium gluconate 10%:** 10 mL IV over 10 minutes
   - **OR Calcium chloride 10%:** 10 mL IV over 5-10 minutes
   - **Repeat after 5 minutes:** If no improvement or ECG changes worsen
   - **Mechanism:** Stabilises cardiac membrane (does NOT lower potassium)
   - **CAUTION:** Avoid if on digoxin (risk of arrhythmias)

2. **SHIFT POTASSIUM INTO CELLS (within 15-30 minutes):**
   - **Insulin:** Actrapid 10 units IV
   - **Glucose:** 50 mL of 50% dextrose IV (25 g)
   - **Monitor blood glucose:** Hypoglycaemia common, check at 1 hour and repeat dextrose if needed
   - **Alternatives if dextrose not needed:** Salbutamol 5 mg nebulised (shifts K+ into cells)

3. **ELIMINATE POTASSIUM (within 30-60 minutes):**
   - **Calcium resonium:** 15 g PO (4 hourly) PR
   - **OR Calcium polystyrene sulfonate:** 30 g PR (retention enema)
   - **OR Sodium zirconium cyclosilicate:** 10 g PO (three times daily)
   - **OR Patiromer:** 8.4 g PO (once daily)
   - **Note:** Onset of action 2-6 hours, not for emergency use alone

4. **ENHANCE ELIMINATION:**
   - **IV fluids:** 0.9% NaCl 1 L (if volume depleted)
   - **Furosemide:** 40-80 mg IV (if eGFR >30 mL/min/1.73 m², fluid status allows)
   - **Dialysis:** Indicated for severe renal impairment, refractory hyperkalaemia

5. **IDENTIFY AND TREAT UNDERLYING CAUSE:**
   - **Medications:** Stop/reduce ACE inhibitors, ARBs, spironolactone, NSAIDs, potassium supplements
   - **Renal impairment:** AKI, CKD
   - **Tissue necrosis:** Rhabdomyolysis, tumour lysis syndrome, haemolysis
   - **Metabolic acidosis:** Correct with sodium bicarbonate if severe (pH <7.1)
   - **Adrenal insufficiency:** Consider hydrocortisone if Addison's suspected

**MONITORING:**
- **ECG:** Continuous cardiac monitoring
- **Potassium:** Repeat in 1 hour, then 2-4 hours until stable
- **Urea and electrolytes:** Monitor for response and recurrence
- **Fluid balance:** Strict input/output monitoring

**NON-EMERGENCY MANAGEMENT (MILD-MODERATE HYPERKALAEMIA):**

**1. Review medications:**
   - **Stop:** Potassium supplements, potassium-containing salt substitutes
   - **Reduce/stop:** ACE inhibitors, ARBs, spironolactone (if appropriate)
   - **Review:** NSAIDs, trimethoprim, pentamidine

**2. Dietary modifications:**
   - **Low potassium diet:** Avoid bananas, oranges, potatoes, tomatoes, chocolate, nuts, salt substitutes
   - **Dietician referral:** For detailed dietary advice

**3. Optimise renal function:**
   - **Volume repletion:** IV fluids if dehydrated
   - **Avoid nephrotoxins:** NSAIDs, ACE inhibitors if AKI
   - **Treat underlying CKD:** Renal clinic referral

**4. Potassium binders (if persistent):**
   - **Calcium resonium:** 15 g PO/PR daily
   - **Sodium zirconium cyclosilicate:** 10 g PO once daily (titrate)
   - **Patiromer:** 8.4 g PO once daily (titrate)

**PSEUDOHYPERKALAEMIA (ARTIFACTUAL):**

**Causes:** Haemolysis (traumatic venepuncture, delayed processing), leukocytosis, thrombocytosis

**Clinical features:** Asymptomatic, no ECG changes, normal repeat sample

**Management:** Repeat blood sample (careful venepuncture technique, prompt processing)

**Sources:** BCSH Guidelines, NICE Guidelines, UK Renal Association Guidelines""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "NICE Guidelines", "UK Renal Association Guidelines"],
                "emergency_protocol": "hyperkalaemia"
            }
        )

    def _handle_severe_anaemia(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Severe anaemia management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**SEVERE ANAEMIA - EMERGENCY MANAGEMENT**

**SEVERITY GRADING (ADULTS):**

| Haemoglobin (g/L) | Severity | Clinical Features | Action |
|-------------------|----------|-------------------|--------|
| 100-119 (female), 120-139 (male) | Mild | Often asymptomatic | Investigate cause |
| 70-99 | Moderate | Fatigue, pallor, dyspnoea on exertion | Investigate + treat |
| 50-69 | Severe | Marked fatigue, dyspnoea at rest, tachycardia | Urgent treatment |
| <50 | Life-threatening | Heart failure, angina, confusion | EMERGENCY transfusion |

**EMERGENCY MANAGEMENT (Hb <70 g/L OR SYMPTOMATIC):**

**IMMEDIATE ACTION:**

1. **ASSESS CLINICAL STATUS:**
   - **Observations:** BP, HR, RR, SpO2, temperature
   - **Cardiovascular:** Chest pain, palpitations, heart failure signs (oedema, crackles)
   - **Respiratory:** Dyspnoea at rest, respiratory rate
   - **Neurological:** Confusion, syncope, dizziness

2. **INVESTIGATIONS (URGENT):**
   - **Full blood count (FBC):** Hb, MCV, MCHC, white cell count, platelet count
   - **Blood film:** Red cell morphology (normocytic, microcytic, macrocytic)
   - **Ret iculocyte count:** Assess bone marrow response
   - **Haematinics:** Ferritin, iron, total iron-binding capacity (TIBC), B12, folate
   - **Renal function:** Urea, creatinine, eGFR
   - **Thyroid function:** TSH, T4 (if macrocytic)
   - **Liver function:** LFT (associated with chronic disease, alcohol)
   - **Haptoglobin, LDH:** If haemolysis suspected
   - **Direct antiglobulin test (Coombs test):** If haemolysis suspected
   - **Blood group and screen:** If transfusion likely

3. **OXYGEN:**
   - **High-flow oxygen:** 15 L/min via non-rebreather mask if hypoxic (SpO2 <94% on room air)
   - **Maintain SpO2:** 94-98% (or 88-92% if at risk of CO2 retention)

4. **INTRAVENOUS FLUIDS:**
   - **Crystalloid challenge:** 500 mL 0.9% NaCl or Hartmann's solution IV if hypovolaemic
   - **CAUTION:** Avoid fluid overload in patients with cardiac/renal impairment

5. **BLOOD TRANSFUSION:**

**Indications for EMERGENCY transfusion:**
- **Hb <50 g/L** (regardless of symptoms)
- **Hb <70 g/L** WITH cardiovascular compromise (chest pain, heart failure, syncope)
- **Hb <80 g/L** WITH ongoing acute bleeding

**Transfusion protocol:**
- **Blood group and screen:** Mandatory before transfusion
- **Compatibility:** Crossmatched blood (if time permits) or O negative (emergency release)
- **Dose:** 1 unit (approximately 300 mL) of packed red cells
- **Expected rise:** Hb increases by approximately 10 g/L per unit
- **Duration:** Infuse over 1-2 hours (slower if cardiac failure risk)
- **Monitoring:** Observations pre-, during, and post-transfusion (15 minutes post-transfusion minimum)

**6. IDENTIFY AND TREAT UNDERLYING CAUSE:**

**ACUTE BLOOD LOSS:**
- **Active bleeding:** Control source (endoscopy, surgery, interventional radiology)
- **Trauma:** Emergency surgery, massive transfusion protocol
- **GI bleed:** Urgent gastroenterology review, consider O negative if massive bleed
- **Obstetric bleed:** Emergency obstetric management

**IRON DEFICIENCY ANAEMIA (MICROCYTIC, LOW FERRITIN):**
- **Oral iron:** Ferrous sulfate 200 mg TDS (take with vitamin C for absorption)
- **IV iron:** If oral intolerance, malabsorption, inflammatory bowel disease, pregnancy (2nd/3rd trimester)
- **Investigate cause:** Menstrual blood loss, GI malignancy (endoscopy/colonoscopy if indicated)

**B12/FOLATE DEFICIENCY (MACROCYTIC):**
- **B12 deficiency:** Hydroxocobalamin 1000 μg IM every 3 months (after loading dose)
- **Folate deficiency:** Folic acid 5 mg OD for 4 months
- **Investigate cause:** Pernicious anaemia (anti-intrinsic factor antibodies), malabsorption, dietary deficiency

**HAEMOLYTIC ANAEMIA:**
- **Autoimmune:** Prednisolone 1 mg/kg, immunosuppression, consider rituximab
- **Hereditary (sickle cell, thalassaemia):** Haematology referral, hydroxycarbamide, transfusion programme

**ANAEMIA OF CHRONIC DISEASE (NORMOCYTIC):**
- **Treat underlying condition:** Inflammation, infection, malignancy
- **Consider transfusion:** If symptomatic and severe

**RENAL FAILURE (NORMOCYTIC):**
- **Erythropoiesis-stimulating agents:** Epoetin or darbepoetin (haematology/renal clinic)
- **Iron supplementation:** Often required concomitantly (IV iron)

**7. ADJUNCTIVE MEASURES:**
- **Bed rest:** If symptomatic, reduce oxygen demand
- **Avoid exertion:** Minimise cardiac workload
- **Treat tachycardia:** Beta-blocker if appropriate (e.g., bisoprolol)
- **Treat heart failure:** Diuretics if fluid overloaded (furosemide 40 mg IV)

**FOLLOW-UP:**
- **Repeat FBC:** 24 hours post-transfusion (check response)
- **Investigate underlying cause:** Haematinics, blood film, haemolysis screen
- **Referral:** Haematology (if unexplained, complex, or requiring ongoing management)
- **Gastroenterology:** If iron deficiency without obvious cause (exclude GI malignancy)
- **Gynaecology:** If heavy menstrual bleeding

**Sources:** BCSH Guidelines, NICE Guidelines, British Society of Gastroenterology Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "emergency",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "NICE Guidelines", "British Society of Gastroenterology Guidelines"],
                "emergency_protocol": "severe_anaemia"
            }
        )

    def _handle_thrombocytopenia_bleeding(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Thrombocytopenia with bleeding management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**THROMBOCYTOPENIA WITH BLEEDING - EMERGENCY MANAGEMENT**

**SEVERITY GRADING:**

| Platelet Count (×10⁹/L) | Bleeding Risk | Action |
|--------------------------|---------------|--------|
| >150 | Normal | No action |
| 100-150 | Mild | Monitor, investigate cause |
| 50-99 | Moderate | Monitor, avoid trauma, consider prophylactic platelet transfusion for invasive procedures |
| 20-49 | Severe | Prophylactic platelet transfusion for procedures, consider for spontaneous bleeding |
| <20 | Very severe | Prophylactic platelet transfusion (spontaneous bleeding risk high) |

**EMERGENCY MANAGEMENT (ACTIVE BLEEDING + PLATELETS <50 ×10⁹/L):**

**IMMEDIATE ACTION:**

1. **ASSESS BLEEDING SEVERITY:**
   - **Mucocutaneous bleeding:** Petechiae, purpura, gum bleeding, epistaxis
   - **Gastrointestinal bleeding:** Melaena, haematemesis
   - **Genitourinary bleeding:** Haematuria, menorrhagia
   - **Intracranial bleeding:** Headache, neurological deficit (LIFE-THREATENING)
   - **Obstetric bleeding:** Postpartum haemorrhage

2. **AIRWAY, BREATHING, CIRCULATION:**
   - **Secure airway:** If epistaxis severe or haematemesis (aspiration risk)
   - **Oxygen:** 15 L/min if hypoxic
   - **IV access:** Two large-bore cannulae
   - **Fluid resuscitation:** Crystalloid or blood products if shocked

3. **PLATELET TRANSFUSION (EMERGENCY):**

**Indications:**
- **Active bleeding** AND platelets <50 ×10⁹/L
- **Intracranial bleeding** (regardless of platelet count, aim >100 ×10⁹/L)
- **Platelets <10 ×10⁹/L** (prophylactic, even without bleeding)
- **Platelets <20 ×10⁹/L** with fever/infection

**Transfusion protocol:**
- **Dose:** 1 adult therapeutic dose (approximately 300 ×10⁹ platelets)
- **Expected rise:** Increase platelet count by 30-50 ×10⁹/L
- **Duration:** Infuse over 15-30 minutes (rapid infusion for active bleeding)
- **Repeat:** Check platelet count 1 hour post-transfusion, repeat if inadequate response

**Special considerations:**
- **HLA-matched platelets:** If refractory to random donor platelets (anti-HLA antibodies)
- **CMV-negative platelets:** For immunocompromised patients (e.g., chemotherapy, transplant)
- **Irradiated platelets:** For patients at risk of transfusion-associated graft-versus-host disease (e.g., Hodgkin lymphoma, immunocompromised)

4. **ANTIFIBRINOLYTIC THERAPY:**
   - **Tranexamic acid:** 1 g IV loading dose, then 1 g IV every 8 hours (or 1-1.5 g PO TDS)
   - **Contraindications:** Active thromboembolism, DIC, renal failure (dose reduction)
   - **Useful for:** Mucocutaneous bleeding, menorrhagia, gastrointestinal bleeding

5. **OTHER BLOOD PRODUCTS:**
   - **Cryoprecipitate:** If fibrinogen low (<1.5 g/L) in DIC or massive transfusion
   - **Fresh frozen plasma (FFP):** If coagulopathy (elevated INR/APTT)
   - **Packed red cells:** If anaemia from blood loss

6. **SPECIFIC BLEEDING MANAGEMENT:**

**Epistaxis (nosebleed):**
- **Sit forward,** pinch soft part of nose for 10-15 minutes
- **Ice packs** to bridge of nose
- **Topical adrenaline/cocaine** (if available)
- **Nasal packing** (if bleeding persists)
- **Urgent ENT referral:** If uncontrolled

**Oral bleeding:**
- **Tranexamic acid mouthwash:** 10 mL swish and swallow (500 mg in 10 mL water)
- **Topical pressure:** Gauze swab
- **Urgent dental/maxillofacial review:** If severe

**Gastrointestinal bleeding:**
- **Proton pump inhibitor:** Omeprazole 40 mg IV OD
- **Urgent gastroenterology review:** For endoscopy
- **Octreotide:** If variceal bleeding suspected

**Menorrhagia:**
- **Tranexamic acid:** 1-1.5 g PO TDS during menstruation
- **Combined oral contraceptive pill:** To reduce menstrual blood loss
- **Levonorgestrel intrauterine system (Mirena):** For long-term management

**Genitourinary bleeding:**
- **Hydration:** Maintain high urine output (>100 mL/hour)
- **Bladder irrigation:** If haematuria with clots
- **Urology review:** If severe or persistent

7. **IDENTIFY AND TREAT UNDERLYING CAUSE:**

**DECREASED PRODUCTION:**
- **Bone marrow failure:** Aplastic anaemia, leukaemia, myelodysplasia
- **Chemotherapy/radiotherapy:** Transient bone marrow suppression
- **Viral infection:** HIV, hepatitis C, EBV, parvovirus B19
- **Megaloblastic anaemia:** B12/folate deficiency
- **Medications:** Chemotherapy, valproate, thiazides, ethanol
- **Management:** Treat underlying cause, consider platelet transfusion

**INCREASED DESTRUCTION:**
- **Immune thrombocytopenic purpura (ITP):** Autoantibodies against platelets
- **Heparin-induced thrombocytopenia (HIT):** Platelet activation by heparin
- **Thrombotic thrombocytopenic purpura (TTP):** ADAMTS13 deficiency
- **Disseminated intravascular coagulation (DIC):** Consumptive coagulopathy
- **Sepsis:** Platelet activation and consumption

**ITP MANAGEMENT:**
- **First-line:** Prednisolone 1 mg/kg/day (max 60-80 mg)
- **Second-line:** Rituximab, thrombopoietin receptor agonists (eltrombopag, romiplostim)
- **Splenectomy:** For refractory ITP (consider vaccination)

**SEQUESTRATION:**
- **Splenomegaly:** Portal hypertension, myelofibrosis, lymphoma
- **Management:** Treat underlying cause, platelet transfusion if bleeding

8. **ADJUNCTIVE MEASURES:**
- **Avoid antiplatelet drugs:** Stop aspirin, NSAIDs, clopidogrel
- **Avoid anticoagulants:** Stop warfarin, DOACs, heparin
- **Avoid IM injections:** Use oral or IV route
- **Avoid invasive procedures:** Unless platelet transfusion given
- **Platelet function preservation:** Avoid NSAIDs

**FOLLOW-UP:**
- **Repeat platelet count:** 1 hour post-transfusion, then daily
- **Bone marrow aspirate/trephine:** If unexplained thrombocytopenia
- **Haematology referral:** For complex cases, ITP, bone marrow disorders
- **Monitor for complications:** Bleeding, thrombosis (especially in HIT)

**Sources:** BCSH Guidelines, NICE Guidelines, British Society for Haematology Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "emergency",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "NICE Guidelines", "British Society for Haematology Guidelines"],
                "emergency_protocol": "thrombocytopenia_bleeding"
            }
        )

    def _handle_troponin(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Troponin interpretation and acute coronary syndrome"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**TROPONIN - ACUTE CORONARY SYNDROME (ACS) INTERPRETATION**

**HIGH-SENSITIVITY TROPONIN (HS-TROPONIN):**

**Reference ranges (varies by assay):**
- **99th percentile upper reference limit (URL):** Typically 14-50 ng/L
- **Significant rise:** ≥50% change above baseline (on serial testing)

**ACUTE CORONARY SYNDROME (ACS) CLASSIFICATION:**

**1. ST-ELEVATION MYOCARDIAL INFARCTION (STEMI):**
- **ECG:** ST elevation ≥1 mm in two contiguous leads
- **Troponin:** Elevated (but may be normal early)
- **Management:** Emergency reperfusion (primary PCI or thrombolysis)
- **Time to treatment:** Door-to-balloon ≤90 minutes, door-to-needle ≤30 minutes

**2. NON-ST-ELEVATION MYOCARDIAL INFARCTION (NSTEMI):**
- **ECG:** ST depression, T-wave inversion, or normal ECG
- **Troponin:** Elevated (significant rise on serial testing)
- **Management:** Risk stratification, early invasive strategy (coronary angiography)

**3. UNSTABLE ANGINA:**
- **ECG:** ST depression, T-wave inversion, or normal ECG
- **Troponin:** Normal
- **Management:** Risk stratification, medical management, consider angiography

**SERIAL TROPONIN TESTING:**

**HS-Troponin 0/1-hour algorithm:**
- **0 hours:** Initial troponin
- **1 hour:** Repeat troponin
- **Interpretation:**

| 0-hour troponin | 1-hour troponin | Interpretation | Action |
|-----------------|-----------------|----------------|--------|
| <URL AND Δ <50% | <URL AND Δ <50% | Rule-out | Discharge (if low risk) |
| ≥URL OR Δ ≥50% | ≥URL OR Δ ≥50% | Rule-in | Admit, manage as ACS |
| <URL AND Δ <50% | ≥URL OR Δ ≥50% | Indeterminate | Observe, repeat at 3 hours |

**Alternative (0/3-hour algorithm):**
- **0 hours:** Initial troponin
- **3 hours:** Repeat troponin
- **Interpretation:** Rule-out if both <URL and Δ <50%

**CAUSES OF ELEVATED TROPONIN (NON-ACS):**

**1. MYOCARDIAL STRAIN/INJURY:**
- **Heart failure:** Acute decompensated heart failure
- **Arrhythmias:** Atrial fibrillation with rapid ventricular response, SVT
- **Cardiomyopathy:** Myocarditis, stress cardiomyopathy (Takotsubo)
- **Cardiac contusion:** Trauma

**2. PULMONARY EMBOLISM:**
- **Right heart strain:** Elevated troponin in massive/submassive PE
- **Clinical significance:** Prognostic marker (higher mortality)

**3. SEPSIS/CRITICAL ILLNESS:**
- **Type 2 myocardial infarction:** Supply-demand mismatch (critical illness)
- **Myocardial depression:** Sepsis-associated cardiac dysfunction

**4. CHRONIC KIDNEY DISEASE (CKD):**
- **Reduced clearance:** Troponin may be chronically elevated
- **Interpretation:** Look for significant rise (Δ ≥50%) on serial testing

**5. MYOCARDITIS:**
- **Viral myocarditis:** Coxsackievirus, influenza, COVID-19
- **Autoimmune myocarditis:** Lupus, rheumatoid arthritis

**6. CARDIAC PROCEDURES:**
- **Post-PCI:** Troponin elevation expected (procedure-related myocardial injury)
- **Post-cardiac surgery:** Troponin elevation expected (surgical myocardial injury)

**CLINICAL INTERPRETATION:**

**Pre-test probability (clinical assessment):**
- **High pre-test probability:** Typical chest pain, risk factors (age, hypertension, diabetes, smoking, family history)
- **Low pre-test probability:** Atypical chest pain, young patient, no risk factors

**Interpretation framework:**
- **Troponin elevated + high pre-test probability:** Likely ACS
- **Troponin elevated + low pre-test probability:** Consider alternative causes
- **Troponin normal + chest pain:** Unlikely ACS (if >6 hours from symptom onset), consider alternative diagnoses (e.g., musculoskeletal, gastrointestinal, pulmonary)

**CLINICAL SCENARIOS:**

**1. TYPICAL CHEST PAIN + NORMAL INITIAL TROPONIN:**
- **Action:** Admit, observe, repeat troponin at 3-6 hours
- **If troponin rises:** Manage as ACS
- **If troponin remains normal:** Consider alternative diagnoses, stress testing, CTCA (if stable)

**2. ATYPICAL CHEST PAIN + ELEVATED TROPONIN:**
- **Action:** Admit, investigate for alternative causes (PE, heart failure, myocarditis)
- **Consider:** Echocardiography, CT pulmonary angiogram, cardiac MRI

**3. CHEST PAIN + ELEVATED TROPONIN + NORMAL ECG:**
- **Action:** Admit, observe, repeat troponin
- **Diagnosis:** Likely NSTEMI (if serial rise) or alternative cause

**4. ASYMPTOMATIC ELEVATED TROPONIN:**
- **Action:** Investigate for chronic elevation (CKD, heart failure)
- **Clinical correlation:** Assess for symptoms of heart failure, ischaemia

**SOURCES:** NICE Guidelines (NG95), ESC Guidelines, ACC/AHA Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "urgent",
                "specialty": "pathology",
                "sources": ["NICE Guidelines (NG95)", "ESC Guidelines", "ACC/AHA Guidelines"]
            }
        )

    def _handle_d_dimer(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """D-dimer interpretation for pulmonary embolism and DVT"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**D-DIMER - VENOUS THROMBOEMBOLISM (VTE) RULE-OUT**

**D-DIMER PHYSIOLOGY:**

- **D-dimer:** Fibrin degradation product (cross-linked D-dimer fragment)
- **Formation:** Cross-linked fibrin degraded by plasmin
- **Elevated in:** Thrombosis, DIC, surgery, trauma, infection, malignancy, pregnancy, advancing age

**REFERENCE RANGE:**
- **Age-adjusted D-dimer:** Age × 10 μg/L (for patients >50 years)
  - Example: 75-year-old → 75 × 10 = 750 μg/L (D-dimer <750 μg/L is normal)
- **Standard cut-off:** <500 μg/L (for patients ≤50 years)

**CLINICAL UTILITY:**

**HIGH NEGATIVE PREDICTIVE VALUE (NPV):**
- **Normal D-dimer:** Effectively rules out VTE (if low/moderate pre-test probability)
- **Sensitivity:** 95-99% (rarely false-negative)
- **Specificity:** 40-60% (often false-positive)

**DIAGNOSTIC ALGORITHM:**

**PULMONARY EMBOLISM (PE):**

1. **ASSESS CLINICAL PROBABILITY:**
   - **Wells score:** Calculate 2-level PE score (likely vs. unlikely)
   - **PERC rule:** If negative, no further testing required (low risk patients)

2. **D-DIMER TESTING:**
   - **PE unlikely (Wells ≤4):** Perform D-dimer
     - Normal D-dimer: PE ruled out (no imaging required)
     - Elevated D-dimer: CTPA required
   - **PE likely (Wells >4):** Proceed directly to CTPA (D-dimer not helpful)

**DEEP VEIN THROMBOSIS (DVT):**

1. **ASSESS CLINICAL PROBABILITY:**
   - **Wells score:** Calculate 2-level DVT score (likely vs. unlikely)

2. **D-DIMER TESTING:**
   - **DVT unlikely (Wells ≤1):** Perform D-dimer
     - Normal D-dimer: DVT ruled out (no imaging required)
     - Elevated D-dimer: Compression Doppler ultrasound required
   - **DVT likely (Wells >1):** Proceed directly to compression Doppler ultrasound (D-dimer not helpful)

**CAUSES OF ELEVATED D-DIMER (NON-VTE):**

**1. PHYSIOLOGICAL:**
- **Age:** D-dimer increases with age (hence age-adjusted cut-off)
- **Pregnancy:** D-dimer elevated throughout pregnancy
- **Post-partum:** Elevated for up to 6 weeks post-delivery

**2. MEDICAL CONDITIONS:**
- **Infection:** Pneumonia, UTI, sepsis
- **Malignancy:** Active cancer, chemotherapy
- **Inflammation:** Rheumatoid arthritis, IBD
- **Trauma:** Fractures, soft tissue injury
- **Surgery:** Postoperative state (elevated for weeks)
- **Heart failure:** Acute decompensated heart failure
- **Liver disease:** Reduced clearance of D-dimer
- **Renal impairment:** Reduced clearance of D-dimer

**3. HAEMATOLOGICAL:**
- **Disseminated intravascular coagulation (DIC):** Markedly elevated
- **Stroke:** Ischaemic stroke

**CLINICAL INTERPRETATION:**

**1. YOUNG PATIENT (<50 YEARS) WITH ELEVATED D-DIMER:**
- **Significant elevation:** More specific for VTE
- **Mild elevation:** Consider alternative causes
- **Action:** Imaging if high clinical suspicion

**2. ELDERLY PATIENT (>50 YEARS) WITH MILDLY ELEVATED D-DIMER:**
- **Use age-adjusted cut-off:** Age × 10 μg/L
- **If D-dimer < age-adjusted cut-off:** VTE ruled out
- **If D-dimer > age-adjusted cut-off:** Imaging required (D-dimer less specific in elderly)

**3. POST-SURGICAL PATIENT WITH ELEVATED D-DIMER:**
- **Expected elevation:** D-dimer elevated for weeks post-surgery
- **Clinical correlation essential:** Assess for VTE symptoms (leg swelling, chest pain)
- **Imaging required:** If clinical suspicion of VTE (D-dimer not helpful)

**4. PREGNANT PATIENT WITH ELEVATED D-DIMER:**
- **Expected elevation:** D-dimer increases throughout pregnancy
- **Clinical correlation essential:** Assess for VTE symptoms
- **Imaging required:** If clinical suspicion of VTE (D-dimer not helpful)
- **Safe imaging:** CTPA (low fetal dose), V/Q scan, compression Doppler ultrasound

**LIMITATIONS:**

- **Not diagnostic:** D-dimer cannot confirm VTE diagnosis (only rules out)
- **Poor specificity:** Elevated in many conditions (high false-positive rate)
- **Not useful in high clinical probability:** Proceed directly to imaging
- **Not useful in post-surgical patients:** Elevated for weeks post-surgery
- **Not useful in pregnancy:** Elevated throughout pregnancy
- **Not useful in malignancy:** Chronic elevation

**CLINICAL SCENARIOS:**

**1. LOW RISK PATIENT WITH NORMAL D-DIMER:**
- **Action:** VTE ruled out, no imaging required
- **Safety:** NPV >99%

**2. MODERATE RISK PATIENT WITH ELEVATED D-DIMER:**
- **Action:** Imaging required (CTPA or compression Doppler ultrasound)
- **Outcome:** Most will have negative imaging (D-dimer false-positive)

**3. HIGH RISK PATIENT WITH NORMAL D-DIMER (RARE):**
- **Action:** Consider imaging anyway (clinical suspicion outweighs D-dimer)
- **Caution:** False-negative D-dimer rare but possible

**SOURCES:** NICE Guidelines, British Thoracic Society Guidelines, ACCP Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["NICE Guidelines", "British Thoracic Society Guidelines", "ACCP Guidelines"]
            }
        )

    def _handle_abg(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Arterial blood gas interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**ARTERIAL BLOOD GAS (ABG) INTERPRETATION**

**SYSTEMATIC APPROACH:**

**1. ASSESS pH (ACID-BASE STATUS):**
- **Normal range:** 7.35-7.45
- **Acidosis:** pH <7.35
- **Alkalosis:** pH >7.45

**2. ASSESS PaCO₂ (RESPIRATORY COMPONENT):**
- **Normal range:** 4.5-6.0 kPa (35-45 mmHg)
- **Respiratory acidosis:** PaCO₂ >6.0 kPa
- **Respiratory alkalosis:** PaCO₂ <4.5 kPa

**3. ASSESS HCO₃⁻ (METABOLIC COMPONENT):**
- **Normal range:** 22-26 mmol/L
- **Metabolic acidosis:** HCO₃⁻ <22 mmol/L
- **Metabolic alkalosis:** HCO₃⁻ >26 mmol/L

**4. ASSESS BASE EXCESS (BUFFER):**
- **Normal range:** -2 to +2 mmol/L
- **Metabolic acidosis:** Base excess <-2 mmol/L
- **Metabolic alkalosis:** Base excess >+2 mmol/L

**5. ASSESS PaO₂ (OXYGENATION):**
- **Normal range:** 10-13 kPa (80-100 mmHg) on room air
- **Mild hypoxaemia:** 8-10 kPa (60-80 mmHg)
- **Moderate hypoxaemia:** 6-8 kPa (45-60 mmHg)
- **Severe hypoxaemia:** <6 kPa (<45 mmHg)

**6. ASSESS SaO₂ (OXYGEN SATURATION):**
- **Normal range:** 94-98% on room air
- **Mild desaturation:** 90-94%
- **Moderate desaturation:** 85-90%
- **Severe desaturation:** <85%

**7. ASSESS LACTATE (TISSUE PERFUSION):**
- **Normal range:** <2.0 mmol/L
- **Hyperlactataemia:** 2.0-4.0 mmol/L
- **Severe hyperlactataemia:** >4.0 mmol/L (suggests tissue hypoperfusion/shock)

**ACID-BASE DISORDERS:**

**RESPIRATORY ACIDOSIS:**
- **pH:** ↓ (<7.35)
- **PaCO₂:** ↑ (>6.0 kPa)
- **HCO₃⁻:** Normal or ↑ (if chronic)
- **Causes:** COPD, respiratory depression (opiates), neuromuscular disease, chest wall deformity, obesity hypoventilation
- **Compensation:** Renal retention of HCO₃⁻ (takes 3-5 days)

**RESPIRATORY ALKALOSIS:**
- **pH:** ↑ (>7.45)
- **PaCO₂:** ↓ (<4.5 kPa)
- **HCO₃⁻:** Normal or ↓ (if chronic)
- **Causes:** Anxiety, hyperventilation, pulmonary embolism, early asthma, pneumonia, pneumothorax, high altitude
- **Compensation:** Renal excretion of HCO₃⁻ (takes 2-3 days)

**METABOLIC ACIDOSIS:**
- **pH:** ↓ (<7.35)
- **PaCO₂:** Normal or ↓ (hyperventilation compensation)
- **HCO₃⁻:** ↓ (<22 mmol/L)
- **Base excess:** ↓ (<-2 mmol/L)

**Anion gap:** Na⁺ - (Cl⁻ + HCO₃⁻) (normal: 8-16 mmol/L)

**High anion gap metabolic acidosis:**
- **Causes:** Lactic acidosis (tissue hypoperfusion, sepsis), ketoacidosis (DKA, alcohol starvation), renal failure, toxic ingestion (salicylates, methanol, ethylene glycol)

**Normal anion gap metabolic acidosis:**
- **Causes:** Diarrhoea (bicarbonate loss), renal tubular acidosis, carbonic anhydrase inhibitors, ureterosigmoidostomy

**METABOLIC ALKALOSIS:**
- **pH:** ↑ (>7.45)
- **PaCO₂:** Normal or ↑ (hypoventilation compensation)
- **HCO₃⁻:** ↑ (>26 mmol/L)
- **Base excess:** ↑ (>+2 mmol/L)
- **Causes:** Vomiting (gastric acid loss), diuretics (thiazides, loop), hypokalaemia, hyperaldosteronism (Cushing's, Conn's), massive blood transfusion
- **Compensation:** Respiratory depression (PaCO₂ rises by 0.7 kPa per 10 mmol/L rise in HCO₃⁻)

**MIXED DISORDERS:**

**Respiratory acidosis + Metabolic acidosis:**
- **pH:** Markedly ↓ (often <7.20)
- **PaCO₂:** ↑ (>6.0 kPa)
- **HCO₃⁻:** ↓ (<22 mmol/L)
- **Causes:** Cardiorespiratory arrest, severe COPD with lactic acidosis

**Respiratory alkalosis + Metabolic acidosis:**
- **pH:** Variable (often near normal)
- **PaCO₂:** ↓ (<4.5 kPa)
- **HCO₃⁻:** ↓ (<22 mmol/L)
- **Causes:** Sepsis, salicylate poisoning, pulmonary embolism with lactic acidosis

**Respiratory acidosis + Metabolic alkalosis:**
- **pH:** Variable (often near normal)
- **PaCO₂:** ↑ (>6.0 kPa)
- **HCO₃⁻:** ↑ (>26 mmol/L)
- **Causes:** COPD on diuretics, ventilator-dependent patient with vomiting

**TYPES OF HYPOXIA:**

**1. Hypoxaemic hypoxia (Type 1 respiratory failure):**
- **PaO₂:** Low (<8 kPa)
- **PaCO₂:** Normal or low
- **Causes:** Pneumonia, pulmonary oedema, pulmonary embolism, ARDS

**2. Hypercapnic respiratory failure (Type 2 respiratory failure):**
- **PaO₂:** Low (<8 kPa)
- **PaCO₂:** High (>6.0 kPa)
- **Causes:** COPD, respiratory depression, neuromuscular disease

**3. Anaemic hypoxia:**
- **PaO₂:** Normal
- **Oxygen-carrying capacity:** Reduced (anaemia, carbon monoxide poisoning)

**4. Circulatory hypoxia:**
- **PaO₂:** Normal
- **Tissue perfusion:** Reduced (shock, heart failure)

**5. Histotoxic hypoxia:**
- **PaO₂:** Normal
- **Cellular utilisation:** Impaired (cyanide poisoning)

**CLINICAL SCENARIOS:**

**1. ACIDOSIS + HYPERCAPNIA + NORMAL HCO₃⁻:**
- **Diagnosis:** Acute respiratory acidosis
- **Causes:** Respiratory depression (opiates), acute exacerbation of COPD

**2. ACIDOSIS + HYPERCAPNIA + ELEVATED HCO₃⁻:**
- **Diagnosis:** Chronic respiratory acidosis (compensated)
- **Causes:** COPD, obesity hypoventilation

**3. ALKALOSIS + HYPOCAPNIA + NORMAL HCO₃⁻:**
- **Diagnosis:** Acute respiratory alkalosis
- **Causes:** Anxiety, hyperventilation, pulmonary embolism

**4. ACIDOSIS + LOW HCO₃⁻ + HIGH ANION GAP:**
- **Diagnosis:** High anion gap metabolic acidosis
- **Causes:** Lactic acidosis, DKA, renal failure

**5. ACIDOSIS + LOW HCO₃⁻ + NORMAL ANION GAP:**
- **Diagnosis:** Normal anion gap metabolic acidosis
- **Causes:** Diarrhoea, renal tubular acidosis

**SOURCES:** ARCI Guidelines (BBC), NICE Guidelines, British Thoracic Society Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["ARCI Guidelines (BBC)", "NICE Guidelines", "British Thoracic Society Guidelines"]
            }
        )

    def _handle_lft(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Liver function tests interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**LIVER FUNCTION TESTS (LFT) INTERPRETATION**

**LIVER FUNCTION TESTS PROFILE:**

**1. BILIRUBIN:**
- **Normal range:** <21 μmol/L
- **Elevated:** Jaundice, haemolysis, Gilbert's syndrome, biliary obstruction, liver disease

**2. ALANINE AMINOTRANSFERASE (ALT):**
- **Normal range:** 10-40 U/L (female), 10-60 U/L (male)
- **Elevated:** Hepatocellular injury (hepatitis, ischaemic hepatitis, drug-induced liver injury)

**3. ASPARTATE AMINOTRANSFERASE (AST):**
- **Normal range:** 10-40 U/L
- **Elevated:** Hepatocellular injury, muscle injury (AST also found in skeletal muscle)

**4. ALKALINE PHOSPHATASE (ALP):**
- **Normal range:** 30-130 U/L
- **Elevated:** Cholestatic disease (biliary obstruction, primary biliary cholangitis), bone disease (Paget's, metastases), pregnancy

**5. GAMMA-GLUTAMYL TRANSFERASE (GGT):**
- **Normal range:** <60 U/L (male), <40 U/L (female)
- **Elevated:** Cholestatic disease, alcohol use, enzyme-inducing drugs (carbamazepine, phenytoin)

**6. ALBUMIN:**
- **Normal range:** 35-50 g/L
- **Low:** Chronic liver disease (synthetic dysfunction), malnutrition, protein-losing enteropathy, nephrotic syndrome

**7. PROTHROMBIN TIME (PT) / INTERNATIONAL NORMALISED RATIO (INR):**
- **Normal range:** PT 9-13 seconds, INR 0.9-1.2
- **Elevated:** Chronic liver disease (synthetic dysfunction), vitamin K deficiency, warfarin therapy

**LIVER ENZYME PATTERNS:**

**HEPATOCELLULAR INJURY (ALT/AST predominant):**
- **ALT:** Markedly elevated (often >1000 U/L in acute hepatitis)
- **AST:** Elevated (may be >ALT in alcoholic liver disease)
- **ALP:** Normal or mildly elevated
- **GGT:** Normal or mildly elevated
- **Bilirubin:** Variable

**Causes:**
- **Viral hepatitis:** Hepatitis A, B, C, E
- **Alcoholic liver disease:** AST:ALT ratio >2:1
- **Non-alcoholic fatty liver disease (NAFLD):** ALT >AST
- **Drug-induced liver injury (DILI):** Paracetamol, antibiotics, statins
- **Ischaemic hepatitis (shock liver):** Markedly elevated ALT/AST (often >5000 U/L)
- **Autoimmune hepatitis:** Elevated ALT/AST, elevated IgG

**CHOLESTATIC DISEASE (ALP/GGT predominant):**
- **ALP:** Markedly elevated (often >2-3× upper limit of normal)
- **GGT:** Elevated (confirms hepatic origin of ALP)
- **ALT/AST:** Normal or mildly elevated
- **Bilirubin:** Elevated (if biliary obstruction)

**Causes:**
- **Biliary obstruction:** Gallstones, pancreatic cancer, cholangiocarcinoma
- **Primary biliary cholangitis (PBC):** Middle-aged females, positive AMA
- **Primary sclerosing cholangitis (PSC):** Associated with ulcerative colitis
- **Drug-induced cholestasis:** Oestrogens, anabolic steroids, antibiotics

**MIXED PATTERN (BOTH HEPATOCELLULAR AND CHOLESTATIC):**
- **ALT/AST:** Elevated
- **ALP/GGT:** Elevated
- **Causes:** Alcoholic liver disease, drug-induced liver injury, viral hepatitis with cholestasis

**LIVER SYNTHETIC FUNCTION:**

**NORMAL SYNTHETIC FUNCTION:**
- **Albumin:** Normal
- **INR:** Normal
- **Platelets:** Normal

**ABNORMAL SYNTHETIC FUNCTION (CHRONIC LIVER DISEASE):**
- **Albumin:** Low (<35 g/L)
- **INR:** Elevated (>1.2)
- **Platelets:** Low (<150 ×10⁹/L) (portal hypertension, splenic sequestration)

**SPECIFIC CLINICAL SCENARIOS:**

**1. ISOLATED ELEVATED BILIRUBIN (Gilbert's Syndrome):**
- **Bilirubin:** Mildly elevated (<100 μmol/L), predominantly unconjugated
- **ALT/AST/ALP:** Normal
- **Haemoglobin:** Normal (no haemolysis)
- **Clinical:** Asymptomatic, jaundice precipitated by fasting, illness, alcohol
- **Management:** Reassurance, no treatment required

**2. ISOLATED ELEVATED GGT (ALCOHOL USE):**
- **GGT:** Elevated
- **ALT/AST/ALP/Bilirubin:** Normal
- **Clinical:** Heavy alcohol use
- **Management:** Reduce alcohol intake, repeat LFT in 3 months

**3. MARKEDLY ELEVATED ALT/AST (>1000 U/L):**
- **Causes:** Acute viral hepatitis, ischaemic hepatitis (shock liver), drug-induced liver injury (paracetamol)
- **Investigation:** Viral hepatitis serology, paracetamol level, ultrasound liver
- **Management:** Admit, supportive care, refer to hepatology

**4. MILDLY ELEVATED ALT/AST (<2× ULN):**
- **Causes:** NAFLD, alcoholic liver disease, medication side effects
- **Investigation:** Ultrasound liver, FibroScan (liver elastography), viral hepatitis serology
- **Management:** Lifestyle modification (weight loss, reduce alcohol), review medications

**5. ELEVATED ALP WITH NORMAL GGT (BONE DISEASE):**
- **Causes:** Paget's disease, bone metastases, healing fractures, pregnancy
- **Investigation:** Serum calcium, phosphate, ALP isoenzymes, bone scan
- **Management:** Referral to endocrinology/rheumatology/oncology as appropriate

**6. ELEVATED ALP WITH ELEVATED GGT (BILE DUCT OBSTRUCTION):**
- **Causes:** Gallstones, pancreatic cancer, cholangiocarcinoma
- **Investigation:** Ultrasound liver/biliary tree (look for dilated bile ducts), MRCP, ERCP
- **Management:** Refer to gastroenterology/hepatology, consider ERCP for stone extraction/stent insertion

**7. LOW ALBUMIN WITH NORMAL INR (MALNUTRITION):**
- **Causes:** Malnutrition, protein-losing enteropathy, nephrotic syndrome
- **Investigation:** Nutritional assessment, urine protein (for nephrotic syndrome), faecal elastase (for pancreatic insufficiency)
- **Management:** Nutritional support, treat underlying condition

**8. LOW ALBUMIN WITH ELEVATED INR (CHRONIC LIVER DISEASE):**
- **Causes:** Cirrhosis (alcoholic, viral, NAFLD, autoimmune)
- **Investigation:** Ultrasound liver (look for nodularity, ascites), FibroScan, viral hepatitis serology, endoscopy (variceal screening)
- **Management:** Refer to hepatology, treat complications of cirrhosis (ascites, varices, encephalopathy), consider liver transplantation

**LIVER FIBROSIS ASSESSMENT:**

**Non-invasive markers:**
- **FIB-4 score:** (Age × AST) / (Platelets × √ALT)
- **NAFLD fibrosis score:** Multivariate score for NAFLD patients
- **FibroScan (liver elastography):** Transient elastography (liver stiffness measurement)

**SOURCES:** BSG Guidelines, NICE Guidelines, EASL Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["BSG Guidelines", "NICE Guidelines", "EASL Guidelines"]
            }
        )

    def _handle_tft(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Thyroid function tests interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**THYROID FUNCTION TESTS (TFT) INTERPRETATION**

**THYROID FUNCTION TESTS PROFILE:**

**1. THYROID-STIMULATING HORMONE (TSH):**
- **Normal range:** 0.4-4.0 mU/L (varies by assay)
- **Low:** Hyperthyroidism, secondary hypothyroidism (pituitary disease)
- **High:** Hypothyroidism, subclinical hypothyroidism

**2. FREE THYROXINE (FT4 / T4):**
- **Normal range:** 10-20 pmol/L
- **Low:** Hypothyroidism, secondary hypothyroidism (pituitary disease)
- **High:** Hyperthyroidism

**3. FREE TRIIODOTHYRONINE (FT3 / T3):**
- **Normal range:** 3.5-6.5 pmol/L
- **Low:** Hypothyroidism, non-thyroidal illness (sick euthyroid syndrome)
- **High:** Hyperthyroidism

**THYROID DYSFUNCTION PATTERNS:**

**PRIMARY HYPOTHYROIDISM:**
- **TSH:** High (>4.0 mU/L)
- **FT4:** Low (<10 pmol/L)
- **FT3:** Low (<3.5 pmol/L)
- **Causes:** Hashimoto's thyroiditis, radioactive iodine ablation, thyroidectomy, drug-induced (amiodarone, lithium)

**SUBCLINICAL HYPOTHYROIDISM:**
- **TSH:** High (5-10 mU/L)
- **FT4:** Normal
- **FT3:** Normal
- **Causes:** Early Hashimoto's thyroiditis, post-radioactive iodine, thyroidectomy
- **Management:**
  - **TSH 5-10 mU/L:** Repeat TFT in 3-6 months, consider levothyroxine if symptomatic or TSH >10 mU/L
  - **TSH >10 mU/L:** Treat with levothyroxine (target TSH 0.4-4.0 mU/L)

**PRIMARY HYPERTHYROIDISM:**
- **TSH:** Low (<0.4 mU/L)
- **FT4:** High (>20 pmol/L)
- **FT3:** High (>6.5 pmol/L)
- **Causes:** Graves' disease, toxic multinodular goitre, toxic adenoma, thyroiditis

**SUBCLINICAL HYPERTHYROIDISM:**
- **TSH:** Low (<0.4 mU/L)
- **FT4:** Normal
- **FT3:** Normal
- **Causes:** Early Graves' disease, toxic multinodular goitre, excessive levothyroxine replacement
- **Management:**
  - **TSH <0.1 mU/L:** Consider treatment if persistent, symptomatic, or risk factors (age >65, AF, osteoporosis)
  - **TSH 0.1-0.4 mU/L:** Repeat TFT in 3-6 months, monitor

**SECONDARY HYPOTHYROIDISM (PITUITARY DISEASE):**
- **TSH:** Low or normal
- **FT4:** Low
- **FT3:** Low or normal
- **Causes:** Pituitary adenoma, pituitary surgery, pituitary radiotherapy, Sheehan's syndrome
- **Management:** Refer to endocrinology, consider other pituitary hormone deficiencies (ACTH, LH/FSH, GH)

**NON-THYROIDAL ILLNESS (SICK EUTHYROID SYNDROME):**
- **Acute illness:** Low T3 (low T4 in severe illness), normal/low TSH
- **Recovery phase:** High T4 with high TSH (transient)
- **Management:** Treat underlying illness, avoid treating thyroid function abnormalities (usually resolve with recovery)

**SPECIFIC CLINICAL SCENARIOS:**

**1. ELEVATED TSH WITH NORMAL FT4 (SUBCLINICAL HYPOTHYROIDISM):**
- **Check:** Repeat TFT in 3-6 months (to confirm persistent elevation)
- **Check:** Thyroid peroxidase antibodies (TPO antibodies) (if positive, higher risk of progression to overt hypothyroidism)
- **Management:**
  - **TSH 5-10 mU/L:** Repeat TFT in 3-6 months, consider levothyroxine if symptomatic or TPO positive
  - **TSH >10 mU/L:** Treat with levothyroxine (starting dose 25-50 mcg daily, adjust by 25 mcg every 6-8 weeks, target TSH 0.4-4.0 mU/L)

**2. LOW TSH WITH NORMAL FT4 (SUBCLINICAL HYPERTHYROIDISM):**
- **Check:** Repeat TFT in 3-6 months (to confirm persistent suppression)
- **Check:** TSH receptor antibodies (TRAb) if Graves' disease suspected
- **Management:**
  - **TSH <0.1 mU/L:** Consider treatment if persistent, symptomatic, or risk factors (age >65, AF, osteoporosis)
  - **TSH 0.1-0.4 mU/L:** Repeat TFT in 3-6 months, monitor

**3. LOW TSH WITH HIGH FT4 (OVERT HYPERTHYROIDISM):**
- **Check:** TRAb (Graves' disease), thyroid ultrasound (toxic multinodular goitre, toxic adenoma)
- **Management:**
  - **Graves' disease:** Carbimazole 20-40 mg daily (reduce to maintenance dose 5-15 mg daily once euthyroid), consider definitive treatment (radioactive iodine or thyroidectomy)
  - **Toxic multinodular goitre/toxic adenoma:** Radioactive iodine or thyroidectomy (definitive treatment preferred)
  - **Thyroiditis:** Propranolol for symptomatic control (beta-blocker), NSAIDs for pain (subacute thyroiditis), prednisolone for severe cases

**4. HIGH TSH WITH LOW FT4 (OVERT HYPOTHYROIDISM):**
- **Check:** TPO antibodies (Hashimoto's thyroiditis)
- **Management:** Levothyroxine replacement (starting dose 25-50 mcg daily, titrate by 25 mcg every 6-8 weeks, target TSH 0.4-4.0 mU/L)
  - **Young patients (<65 years):** Full replacement dose (1.6 mcg/kg/day)
  - **Elderly patients (>65 years):** Lower starting dose (25 mcg daily, titrate slowly)
  - **Ischaemic heart disease:** Lower starting dose (25 mcg daily, titrate slowly to avoid angina)

**5. LOW/NORMAL TSH WITH LOW FT4 (SECONDARY HYPOTHYROIDISM):**
- **Check:** 9 am cortisol (ACTH deficiency), prolactin (prolactinoma), LH/FSH (gonadotropin deficiency), IGF-1 (GH deficiency)
- **Management:** Refer to endocrinology, consider levothyroxine replacement (dose titrated to FT4 in upper half of reference range)

**THYROID FUNCTION IN PREGNANCY:**

**Trimester-specific reference ranges:**
- **First trimester:** TSH 0.1-2.5 mU/L (hCG stimulates thyroid, lowering TSH)
- **Second trimester:** TSH 0.2-3.0 mU/L
- **Third trimester:** TSH 0.3-3.0 mU/L

**Management:**
- **Pre-existing hypothyroidism:** Increase levothyroxine dose by 30-50% as soon as pregnancy confirmed, target TSH <2.5 mU/L
- **New-onset hypothyroidism in pregnancy:** Treat with levothyroxine (target TSH <2.5 mU/L)
- **Hyperthyroidism in pregnancy:** Propylthiouracil (PTU) in first trimester (carbimazole teratogenic), switch to carbimazole after first trimester

**DRUGS AFFECTING THYROID FUNCTION:**

**Hypothyroidism:**
- **Amiodarone:** Inhibits conversion of T4 to T3, causes hypothyroidism in 15-20%
- **Lithium:** Inhibits thyroid hormone synthesis
- **Phenytoin, carbamazepine:** Increases metabolism of thyroid hormones

**Hyperthyroidism:**
- **Amiodarone:** Iodine-rich, causes hyperthyroidism in 2-3% (type 1: iodine excess, type 2: thyroiditis)

**SOURCES:** BTA Guidelines, NICE Guidelines (NG145), ATA Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["BTA Guidelines", "NICE Guidelines (NG145)", "ATA Guidelines"]
            }
        )

    def _handle_hba1c(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """HbA1c interpretation and diabetes management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**HAEMOGLOBIN A1c (HbA1c) - DIABETES DIAGNOSIS AND MONITORING**

**HbA1c PHYSIOLOGY:**

- **HbA1c:** Glycated haemoglobin (glucose bound to haemoglobin)
- **Reflects:** Average blood glucose over previous 2-3 months
- **Formation:** Irreversible, proportional to blood glucose concentration
- **Normal range:** 20-42 mmol/mol (4.0-6.0%)

**DIAGNOSTIC CRITERIA (DIABETES):**

| HbA1c (mmol/mol) | HbA1c (%) | Interpretation | Action |
|-------------------|-----------|----------------|--------|
| <20 | <4.0 | Abnormally low | Investigate (anaemia, haemoglobinopathy) |
| 20-41 | 4.0-6.0 | Normal | No action |
| 42-47 | 6.0-6.4 | Pre-diabetes (high risk) | Lifestyle intervention, annual HbA1c |
| ≥48 | ≥6.5 | Diabetes | Confirm with second test (unless symptomatic) |

**CONFIRMATION OF DIAGNOSIS:**

- **Asymptomatic patient:** Confirm with repeat HbA1c (unless HbA1c ≥48 mmol/mol on two separate occasions)
- **Symptomatic patient:** Classic hyperglycaemic symptoms (polyuria, polydipsia, weight loss) + random glucose ≥11.1 mmol/L OR HbA1c ≥48 mmol/L

**FACTORS AFFECTING HbA1c:**

**FALSELY ELEVATED HbA1c:**
- **Iron deficiency anaemia:** Reduced red cell turnover
- **Vitamin B12/folate deficiency:** Reduced red cell turnover
- **Alcoholism:** Reduced red cell turnover
- **Chronic kidney disease (CKD stages 3-5):** Reduced red cell turnover, uraemia
- **Splenectomy:** Increased red cell lifespan

**FALSELY LOW HbA1c:**
- **Anaemia (haemolytic, blood loss):** Increased red cell turnover
- **Haemoglobinopathies:** Sickle cell disease, thalassaemia
- **Pregnancy:** Increased red cell turnover (physiological anaemia)
- **Recent blood transfusion:** Donor red cells not glycated
- **Liver disease:** Reduced red cell survival
- **Antiretroviral therapy:** Increased red cell turnover

**If HbA1c unreliable:** Use fasting glucose, random glucose, or oral glucose tolerance test (OGTT) for diagnosis

**HbA1c AND GLUCOSE CORRELATION:**

| HbA1c (mmol/mol) | HbA1c (%) | Estimated Average Glucose (mmol/L) | Estimated Average Glucose (mg/dL) |
|-------------------|-----------|------------------------------------|------------------------------------|
| 31 | 5.0 | 5.4 | 97 |
| 42 | 6.0 | 7.0 | 126 |
| 53 | 7.0 | 8.6 | 154 |
| 64 | 8.0 | 10.2 | 183 |
| 75 | 9.0 | 11.8 | 212 |
| 86 | 10.0 | 13.4 | 241 |

**DIABETES MANAGEMENT TARGETS:**

**ADULTS WITH TYPE 2 DIABETES:**
- **General population:** HbA1c ≤48 mmol/mol (≤6.5%)
- **Individualised target:** HbA1c 48-53 mmol/mol (6.5-7.0%) (consider patient factors)
- **Relaxed target:** HbA1c 53-64 mmol/mol (7.0-8.0%) (frail elderly, limited life expectancy, recurrent hypoglycaemia)

**ADULTS WITH TYPE 1 DIABETES:**
- **General target:** HbA1c ≤48 mmol/mol (≤6.5%)
- **Individualised target:** Balance optimal glycaemic control with risk of hypoglycaemia

**PREGNANCY (PRE-GESTATIONAL DIABETES):**
- **Target:** HbA1c <43 mmol/mol (<6.1%) pre-conception (reduce risk of congenital malformations)
- **Target:** HbA1c <42 mmol/mol (<6.0%) during pregnancy (reduce risk of macrosomia, stillbirth)

**PREGNANCY (GESTATIONAL DIABETES):**
- **Diagnosis:** OGTT 75 g (fasting glucose ≥5.6 mmol/L OR 2-hour glucose ≥7.8 mmol/L)
- **HbA1c NOT recommended** for diagnosis of gestational diabetes

**HYPOGLYCAEMIA AWARENESS:**

- **Level 1 (mild):** Blood glucose 3.0-3.9 mmol/L, asymptomatic or mild symptoms
- **Level 2 (moderate):** Blood glucose <3.0 mmol/L, requires self-treatment
- **Level 3 (severe):** Blood glucose <3.0 mmol/L, requires assistance (cognitive impairment, unable to self-treat)

**PRE-DIABETES (HbA1c 42-47 mmol/mol):**

**Management:**
- **Lifestyle intervention:** Weight loss (5-10% of body weight), healthy diet (Mediterranean diet), regular exercise (150 minutes/week moderate intensity)
- **Annual HbA1c:** Monitor for progression to diabetes
- **Cardiovascular risk assessment:** Blood pressure, lipid profile, smoking cessation

**Progression to diabetes:**
- **Risk:** 5-10% per year (without intervention)
- **Risk reduction:** 40-60% with lifestyle intervention (Diabetes Prevention Program)

**DIABETES COMPLICATIONS SCREENING:**

**Microvascular complications:**
- **Retinopathy:** Annual digital retinal screening
- **Nephropathy:** Annual urine albumin:creatinine ratio (ACR), serum creatinine/eGFR
- **Neuropathy:** Annual foot examination (monofilament testing, sensation)

**Macrovascular complications:**
- **Cardiovascular disease:** Blood pressure control (target <140/80 mmHg), lipid control (statin therapy), antiplatelet therapy (aspirin 75 mg OD if high cardiovascular risk)

**SOURCES:** NICE Guidelines (NG28), ADA Standards of Care, SIGN Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["NICE Guidelines (NG28)", "ADA Standards of Care", "SIGN Guidelines"]
            }
        )

    def _handle_fbc(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Full blood count interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**FULL BLOOD COUNT (FBC) INTERPRETATION**

**FULL BLOOD COUNT PROFILE:**

**RED CELL INDICES:**
- **Haemoglobin (Hb):** Oxygen-carrying capacity (normal: male 130-170 g/L, female 120-150 g/L)
- **Haematocrit (Hct):** Proportion of blood volume occupied by red cells (normal: male 0.40-0.52 L/L, female 0.36-0.46 L/L)
- **Mean cell volume (MCV):** Average red cell volume (normal: 80-100 fL)
- **Mean cell haemoglobin (MCH):** Average haemoglobin per red cell (normal: 27-32 pg)
- **Mean cell haemoglobin concentration (MCHC):** Average haemoglobin concentration (normal: 320-360 g/L)
- **Red cell distribution width (RDW):** Variation in red cell size (normal: 11-15%)

**WHITE CELL COUNT:**
- **Total white cell count (WCC):** Normal 4.0-11.0 ×10⁹/L
- **Neutrophils:** Normal 2.0-7.5 ×10⁹/L (bacterial infection, inflammation, stress)
- **Lymphocytes:** Normal 1.0-4.0 ×10⁹/L (viral infection, chronic lymphocytic leukaemia)
- **Monocytes:** Normal 0.2-0.8 ×10⁹/L (chronic infection, autoimmune disease)
- **Eosinophils:** Normal 0.04-0.4 ×10⁹/L (allergy, parasitic infection, asthma)
- **Basophils:** Normal <0.1 ×10⁹/L (myeloproliferative disorders)

**PLATELETS:**
- **Platelet count:** Normal 150-400 ×10⁹/L
- **Mean platelet volume (MPV):** Normal 8-12 fL (increased in platelet destruction)

**ANAEMIA CLASSIFICATION (BY MCV):**

**MICROCYTIC ANAEMIA (MCV <80 fL):**

**Iron deficiency anaemia:**
- **Hb:** Low
- **MCV:** Low (<80 fL)
- **MCH:** Low (<27 pg)
- **MCHC:** Low (<320 g/L)
- **RDW:** High (>15%)
- **Ferritin:** Low (<15 μg/L) (diagnostic)
- **Iron:** Low
- **TIBC:** High
- **Blood film:** Hypochromic microcytic red cells, pencil cells, target cells
- **Causes:** Menstrual blood loss, gastrointestinal blood loss, pregnancy, malabsorption (coeliac disease)
- **Management:** Oral iron (ferrous sulfate 200 mg TDS), investigate underlying cause

**Thalassaemia:**
- **Hb:** Low or normal
- **MCV:** Low (<80 fL)
- **MCH:** Low (<27 pg)
- **MCHC:** Normal (320-360 g/L)
- **RDW:** Normal (11-15%)
- **Ferritin:** Normal or high
- **Iron:** Normal or high
- **Blood film:** Microcytic hypochromic red cells, target cells, basophilic stippling
- **Causes:** Alpha thalassaemia, beta thalassaemia (hereditary)
- **Management:** Genetic counselling, haematology referral

**Sideroblastic anaemia:**
- **Hb:** Low
- **MCV:** Low
- **Ferritin:** High (iron-loaded mitochondria in red cell precursors)
- **Blood film:** Dimorphic red cell population, Pappenheimer bodies (iron granules)
- **Causes:** Hereditary (ALAS2 mutation), acquired (lead poisoning, alcohol, isoniazid)
- **Management:** Haematology referral, pyridoxine (hereditary form), treat underlying cause (acquired form)

**NORMOCYTIC ANAEMIA (MCV 80-100 fL):**

**Acute blood loss:**
- **Hb:** Low (may be normal immediately after acute bleed, drops over 24-48 hours)
- **MCV:** Normal (initially), may become microcytic if iron deficiency develops
- **Platelets:** High (reactive thrombocytosis)
- **Clinical:** Signs of hypovolaemia, bleeding source identified
- **Management:** Stop bleeding, fluid resuscitation, blood transfusion if Hb <70 g/L or symptomatic

**Anaemia of chronic disease:**
- **Hb:** Low (usually mild-moderate)
- **MCV:** Normal or low (late stages)
- **Ferritin:** Normal or high (acute phase reactant)
- **Iron:** Low
- **TIBC:** Low
- **CRP/ESR:** High (inflammatory markers)
- **Causes:** Chronic infection, autoimmune disease, malignancy, chronic kidney disease
- **Management:** Treat underlying condition, consider IV iron if functional iron deficiency

**Haemolytic anaemia:**
- **Hb:** Low
- **MCV:** Normal or high
- **Reticulocyte count:** High (>2%) (bone marrow response)
- **LDH:** High (>250 U/L)
- **Haptoglobin:** Low (<0.3 g/L) (consumed in haemolysis)
- **Bilirubin:** High (>21 μmol/L) (unconjugated)
- **Blood film:** Polychromasia (reticulocytes), spherocytes (autoimmune haemolysis), schistocytes (microangiopathic haemolysis)
- **Causes:** Autoimmune, hereditary spherocytosis, G6PD deficiency, thrombotic thrombocytopenic purpura (TTP), disseminated intravascular coagulation (DIC)
- **Management:** Treat underlying cause, corticosteroids (autoimmune haemolysis), folic acid supplementation

**Renal failure:**
- **Hb:** Low
- **MCV:** Normal
- **Ferritin:** Normal or high (functional iron deficiency)
- **Clinical:** Elevated urea and creatinine (reduced eGFR)
- **Causes:** Reduced erythropoietin production (chronic kidney disease)
- **Management:** Erythropoiesis-stimulating agents (epoetin, darbepoetin), IV iron, folic acid

**MACROCYTIC ANAEMIA (MCV >100 fL):**

**Megaloblastic anaemia (B12/folate deficiency):**
- **Hb:** Low
- **MCV:** High (>100 fL)
- **White cells:** Low (leucopenia), hypersegmented neutrophils (≥5 lobes)
- **Platelets:** Low (thrombocytopenia)
- **B12:** Low (<150 ng/L)
- **Folate:** Low (<3 μg/L)
- **Blood film:** Macrocytosis, hypersegmented neutrophils
- **Causes:** Pernicious anaemia (autoimmune), dietary deficiency (vegan, alcoholism), malabsorption (coeliac disease, Crohn's disease), medications (methotrexate, phenytoin)
- **Management:** B12 replacement (hydroxocobalamin 1000 μg IM every 3 months), folic acid replacement (5 mg OD for 4 months)

**Non-megaloblastic macrocytosis:**
- **MCV:** High (>100 fL)
- **Hb:** Normal or low
- **White cells/platelets:** Normal
- **Causes:** Alcohol, liver disease, hypothyroidism, reticulocytosis, medications (azathioprine, hydroxycarbamide)
- **Management:** Treat underlying condition

**WHITE CELL ABNORMALITIES:**

**Neutrophilia (neutrophils >7.5 ×10⁹/L):**
- **Causes:** Bacterial infection, inflammation, stress (cortisol), steroids, pregnancy, smoking, leukaemia
- **Left shift:** Immature neutrophils (bands, metamyelocytes) on blood film (severe bacterial infection)

**Neutropenia (neutrophils <1.5 ×10⁹/L):**
- **Mild:** 1.0-1.5 ×10⁹/L (moderate risk of infection)
- **Moderate:** 0.5-1.0 ×10⁹/L (high risk of infection)
- **Severe:** <0.5 ×10⁹/L (very high risk of infection)
- **Causes:** Viral infection (influenza, hepatitis, HIV), chemotherapy/radiotherapy, autoimmune disease (SLE, rheumatoid arthritis), medications (carbimazole, co-trimoxazole, clozapine), vitamin B12/folate deficiency, leukaemia
- **Management:** Treat underlying cause, prophylactic antibiotics if severe neutropenia, G-CSF (filgrastim) for chemotherapy-induced neutropenia

**Lymphocytosis (lymphocytes >4.0 ×10⁹/L):**
- **Causes:** Viral infection (infectious mononucleosis, cytomegalovirus, hepatitis), chronic lymphocytic leukaemia, whooping cough
- **Atypical lymphocytes:** Reactive lymphocytes (infectious mononucleosis)

**Lymphopenia (lymphocytes <1.0 ×10⁹/L):**
- **Causes:** HIV infection, corticosteroids, chemotherapy/radiotherapy, autoimmune disease, severe stress

**Eosinophilia (eosinophils >0.4 ×10⁹/L):**
- **Mild:** 0.4-1.0 ×10⁹/L (allergy, asthma)
- **Moderate:** 1.0-1.5 ×10⁹/L (parasitic infection, drug reaction)
- **Severe:** >1.5 ×10⁹/L (hypereosinophilic syndrome, leukaemia)
- **Causes:** Allergy (asthma, eczema, hay fever), parasitic infection (worms), drug reaction (antibiotics, NSAIDs), autoimmune disease (Churg-Strauss syndrome), Hodgkin lymphoma, Cushing's syndrome
- **Management:** Treat underlying cause, stool ova/cysts/parasites if parasitic infection suspected

**Monocytosis (monocytes >0.8 ×10⁹/L):**
- **Causes:** Chronic bacterial infection (tuberculosis, endocarditis), protozoal infection, autoimmune disease (SLE, rheumatoid arthritis), acute myelomonocytic leukaemia

**PLATELET ABNORMALITIES:**

**Thrombocytosis (platelets >400 ×10⁹/L):**
- **Mild:** 400-600 ×10⁹/L (reactive)
- **Moderate:** 600-1000 ×10⁹/L (reactive or essential)
- **Severe:** >1000 ×10⁹/L (essential thrombocythaemia)
- **Reactive causes:** Infection, inflammation, iron deficiency, blood loss, surgery, trauma
- **Essential causes:** Essential thrombocythaemia (myeloproliferative disorder)
- **Management:** Treat underlying cause (reactive), aspirin (essential thrombocythaemia), cytoreduction (hydroxycarbamide, anagrelide) if high risk

**Thrombocytopenia (platelets <150 ×10⁹/L):**
- **Mild:** 100-150 ×10⁹/L (minimal bleeding risk)
- **Moderate:** 50-99 ×10⁹/L (increased bleeding risk)
- **Severe:** <50 ×10⁹/L (high bleeding risk)
- **Causes:** Decreased production (bone marrow failure, leukaemia, chemotherapy), increased destruction (ITP, TTP, DIC, sepsis), sequestration (splenomegaly), dilution (massive transfusion)
- **Management:** Treat underlying cause, platelet transfusion if <10 ×10⁹/L (or <20 ×10⁹/L with bleeding), corticosteroids (ITP)

**SOURCES:** BCSH Guidelines, NICE Guidelines, British Society of Haematology Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "NICE Guidelines", "British Society of Haematology Guidelines"]
            }
        )

    def _handle_inr(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """INR and coagulation interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**INR (INTERNATIONAL NORMALISED RATIO) - COAGULATION INTERPRETATION**

**INR PHYSIOLOGY:**

- **Prothrombin time (PT):** Time for plasma to clot after addition of thromboplastin (tissue factor)
- **INR (International Normalised Ratio):** Standardised PT to account for differences in thromboplastin reagents between laboratories
- **Normal range:** 0.9-1.2 (varies slightly by laboratory)
- **Elevated INR:** Prolonged coagulation time (bleeding risk)

**COAGULATION CASCADE:**

**Extrinsic pathway:** Tissue factor → Factor VII → Factor X → Thrombin → Fibrin clot
**PT/INR assesses:** Extrinsic pathway (Factors VII, X, V, II, fibrinogen)

**CAUSES OF ELEVATED INR:**

**1. WARFARIN THERAPY:**
- **Mechanism:** Inhibits vitamin K epoxide reductase (reduces Factors II, VII, IX, X, protein C, protein S)
- **Indications:** Atrial fibrillation (stroke prevention), venous thromboembolism (DVT/PE), mechanical heart valves
- **Target INR:** Condition-dependent (see below)
- **Onset of action:** 2-3 days (due to half-life of clotting factors)
- **Duration of action:** 5-7 days after discontinuation

**Target INR ranges:**
- **Atrial fibrillation:** 2.0-3.0
- **DVT/PE (venous thromboembolism):** 2.0-3.0
- **Mechanical mitral valve:** 2.5-3.5
- **Mechanical aortic valve:** 2.0-3.0
- **Recurrent VTE despite anticoagulation:** 2.5-3.5
- **Antiphospholipid syndrome:** 2.5-3.5

**2. VITAMIN K DEFICIENCY:**
- **Causes:** Malnutrition, malabsorption (coeliac disease, Crohn's disease, cholestasis), broad-spectrum antibiotics (vitamin K-producing gut flora eradication), warfarin poisoning
- **INR:** Mildly elevated (1.5-2.5)
- **Management:** Vitamin K 10 mg IV/PO/IM (slowly corrects INR over 6-24 hours)

**3. LIVER DISEASE:**
- **Mechanism:** Reduced synthesis of clotting factors (produced in liver)
- **INR:** Mildly elevated (1.3-2.0 in chronic liver disease)
- **Associated with:** Elevated bilirubin, low albumin, low platelets (synthetic dysfunction)
- **Management:** Treat underlying liver disease, vitamin K (if deficient), fresh frozen plasma (FFP) if bleeding or invasive procedure

**4. DISSEMINATED INTRAVASCULAR COAGULATION (DIC):**
- **Mechanism:** Consumption of clotting factors and platelets (microvascular thrombosis)
- **INR:** Elevated (1.5-3.0)
- **Associated with:** Low platelets, low fibrinogen, elevated D-dimer
- **Clinical:** Bleeding (ecchymosis, petechiae, mucosal bleeding), thrombosis (organ dysfunction)
- **Management:** Treat underlying cause (sepsis, malignancy, obstetric complication), FFP, platelet transfusion, cryoprecipitate

**5. DIRECT ORAL ANTICOAGULANTS (DOACs):**
- **DOACs:** Dabigatran, rivaroxaban, apixaban, edoxaban
- **Effect on INR:** May mildly elevate INR (but INR NOT reliable for monitoring DOACs)
- **Management:** DOAC-level anti-Xa assay (for rivaroxaban, apixaban, edoxaban) or dilute thrombin time (for dabigatran)

**6. CONGENITAL FACTOR DEFICIENCIES:**
- **Factor VII deficiency:** Isolated prolonged PT/INR with normal APTT
- **Factor X deficiency:** Prolonged PT/INR and APTT
- **Factor V deficiency:** Prolonged PT/INR and APTT
- **Management:** Factor replacement, FFP, vitamin K (if Factor VII deficiency due to vitamin K deficiency)

**WARFARIN MANAGEMENT:**

**INITIATION:**
- **Starting dose:** 5 mg OD (elderly: 3 mg OD)
- **INR monitoring:** Daily until INR in therapeutic range for 2 consecutive days
- **Duration of loading:** Usually 4-5 days

**MAINTENANCE:**
- **INR monitoring:** Every 12 weeks once stable (more frequent if dose adjusted, interacting medications started, illness)
- **Dose adjustment:** Increase or decrease by 5-10% weekly dose (INR outside target range)
- **Target INR:** Individualised based on indication (see above)

**INTERACTING MEDICATIONS/FOODS:**

**Potentiates warfarin (increases INR):**
- **Amiodarone:** Reduce warfarin dose by 30-50%
- **Antibiotics:** Broad-spectrum (erythromycin, clarithromycin, metronidazole, co-trimoxazole)
- **Antifungals:** Fluconazole, itraconazole
- **NSAIDs:** Aspirin, ibuprofen (also increase bleeding risk)
- **Statins:** Simvastatin, rosuvastatin
- **SSRIs:** Citalopram, fluoxetine, sertraline (also impair platelet function)
- **Alcohol:** Binge drinking (chronic alcohol consumption induces liver enzymes, reduces INR)

**Antagonises warfarin (decreases INR):**
- **Enzyme inducers:** Carbamazepine, phenytoin, rifampicin, St John's wort
- **Vitamin K-rich foods:** Green leafy vegetables (spinach, broccoli, kale, Brussels sprouts)

**WARFARIN REVERSAL:**

**Indications:**
- **INR >8.0** (no bleeding)
- **INR >5.0** (high bleeding risk)
- **Life-threatening bleeding** (regardless of INR)

**Management:**
1. **STOP warfarin**
2. **Vitamin K:**
   - **INR 5.0-8.0 (no bleeding):** Vitamin K 1-2.5 mg PO
   - **INR >8.0 (no bleeding):** Vitamin K 2.5-5 mg PO
   - **Life-threatening bleeding:** Vitamin K 10 mg IV (slow IV injection over 10 minutes)
3. **Prothrombin complex concentrate (PCC):**
   - **Indication:** Life-threatening bleeding
   - **Dose:** 25-50 IU/kg Factor IX (individualised)
   - **Effect:** Immediate INR correction (within minutes)
4. **Fresh frozen plasma (FFP):**
   - **Indication:** Life-threatening bleeding (if PCC unavailable)
   - **Dose:** 15-20 mL/kg (approximately 4 units)
   - **Effect:** INR correction within 6-24 hours
5. **Re-check INR:** After 6 hours (to assess response to vitamin K)

**INR AND BLEEDING RISK:**

**INR <3.0:** Minimal bleeding risk (if no other risk factors)
**INR 3.0-4.5:** Increased bleeding risk (consider dose reduction)
**INR 4.5-10.0:** High bleeding risk (hold warfarin, give vitamin K)
**INR >10.0:** Very high bleeding risk (hold warfarin, give vitamin K, consider PCC/FFP if bleeding)

**SOURCES:** BCSH Guidelines, NICE Guidelines, American College of Chest Physicians Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["BCSH Guidelines", "NICE Guidelines", "American College of Chest Physicians Guidelines"]
            }
        )

    def _handle_crp(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """C-reactive protein interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**C-REACTIVE PROTEIN (CRP) - INFLAMMATORY MARKER INTERPRETATION**

**CRP PHYSIOLOGY:**

- **CRP:** Acute phase protein produced by liver in response to IL-6
- **Function:** Opsonin (binds to pathogens, activates complement system)
- **Normal range:** <5 mg/L (varies by laboratory)
- **Elevated CRP:** Inflammation, infection, tissue injury, malignancy

**CRP LEVELS AND INTERPRETATION:**

| CRP (mg/L) | Interpretation | Clinical Significance |
|------------|----------------|----------------------|
| <5 | Normal | No significant inflammation |
| 5-10 | Mild elevation | Mild inflammation (early infection, minor tissue injury) |
| 10-40 | Moderate elevation | Moderate inflammation (viral infection, localised bacterial infection) |
| 40-100 | Marked elevation | Significant inflammation (bacterial infection, tissue necrosis) |
| >100 | Very high elevation | Severe inflammation (sepsis, severe bacterial infection, major tissue injury) |

**SPECIFIC CLINICAL SCENARIOS:**

**1. INFECTION:**

**Viral infection:**
- **CRP:** Mild-moderate elevation (10-40 mg/L)
- **Clinical:** URTI symptoms, influenza, glandular fever
- **Management:** Symptomatic treatment, antivirals (influenza), antibiotics NOT indicated

**Bacterial infection:**
- **CRP:** Marked elevation (40-100 mg/L)
- **Clinical:** Fever, focal signs of infection (pneumonia, cellulitis, urinary tract infection)
- **Management:** Antibiotics (culture-directed if possible)

**Sepsis:**
- **CRP:** Very high elevation (>100 mg/L)
- **Clinical:** Systemic inflammatory response syndrome (SIRS), organ dysfunction
- **Management:** Sepsis six (IV antibiotics, fluid resuscitation, oxygen, lactate measurement, blood cultures, urinary catheter), intensive care admission

**2. INFLAMMATORY DISEASE:**

**Rheumatoid arthritis:**
- **CRP:** Moderate elevation (10-40 mg/L)
- **Clinical:** Joint pain, swelling, morning stiffness, symmetrical small joint involvement
- **Management:** NSAIDs, corticosteroids, DMARDs (methotrexate), biologics

**Giant cell arteritis (temporal arteritis):**
- **CRP:** Marked elevation (40-100 mg/L, often >100 mg/L)
- **ESR:** Markedly elevated (>50 mm/hr)
- **Clinical:** Headache, scalp tenderness, jaw claudication, visual disturbance, polymyalgia rheumatica
- **Management:** **URGENT:** High-dose corticosteroids (prednisolone 40-60 mg OD), urgent temporal artery biopsy (within 2 weeks of starting steroids), ophthalmology review (visual disturbance)

**Polymyalgia rheumatica:**
- **CRP:** Marked elevation (40-100 mg/L)
- **ESR:** Markedly elevated (>50 mm/hr)
- **Clinical:** Bilateral shoulder and hip girdle pain, stiffness, morning stiffness >45 minutes, age >65 years
- **Management:** Low-dose corticosteroids (prednisolone 15 mg OD), taper over 12-18 months

**Inflammatory bowel disease (Crohn's disease, ulcerative colitis):**
- **CRP:** Mild-moderate elevation (10-40 mg/L)
- **Clinical:** Diarrhoea, abdominal pain, weight loss, blood in stool
- **Management:** Gastroenterology referral, colonoscopy, treatment with 5-ASAs, corticosteroids, immunomodulators, biologics

**3. TISSUE INJURY:**

**Myocardial infarction:**
- **CRP:** Marked elevation (peaks at 48-72 hours, 20-100 mg/L)
- **Troponin:** Elevated (diagnostic of myocardial infarction)
- **Clinical:** Chest pain, ECG changes
- **Management:** Antiplatelet therapy, anticoagulation, reperfusion (primary PCI or thrombolysis)

**Surgery:**
- **CRP:** Marked elevation (peaks at 48-72 hours, 50-150 mg/L)
- **Expected rise:** Post-operative inflammatory response
- **Persistent elevation:** Consider post-operative complications (infection, anastomotic leak)

**Trauma:**
- **CRP:** Marked elevation (peaks at 48-72 hours)
- **Clinical:** Fractures, soft tissue injury, burns
- **Management:** Treat injuries, monitor CRP trend (should decline after 72 hours)

**4. MALIGNANCY:**

**Solid tumours:**
- **CRP:** Mild-moderate elevation (10-40 mg/L)
- **Clinical:** Weight loss, fatigue, localised symptoms
- **Management:** Investigations to identify primary tumour (CT imaging, tumour markers, biopsy)

**Haematological malignancies (lymphoma, leukaemia):**
- **CRP:** Marked elevation (40-100 mg/L)
- **Clinical:** B symptoms (fever, night sweats, weight loss), lymphadenopathy
- **Management:** Haematology referral, biopsy, staging investigations

**CRP TRENDS:**

**Rising CRP:**
- **Worsening inflammation:** Progressive infection, inadequate treatment, complications

**Falling CRP:**
- **Improving inflammation:** Resolving infection, response to treatment

**Persistently elevated CRP:**
- **Chronic inflammation:** Autoimmune disease, untreated infection, malignancy
- **Further investigations:** Imaging, biopsy, specialist referral

**CRP VS ESR (ERYTHROCYTE SEDIMENTATION RATE):**

**CRP:**
- **Advantages:** Rapid result (minutes), not affected by anaemia, pregnancy, age
- **Disadvantages:** Non-specific (elevated in any inflammation)

**ESR:**
- **Advantages:** Sensitive to chronic inflammation
- **Disadvantages:** Slow result (hours), affected by anaemia (falsely elevated), pregnancy (falsely elevated), age (increases with age)

**CLINICAL UTILITY:**

**CRP useful for:**
- **Diagnosis:** Infection vs. non-infectious inflammation
- **Monitoring:** Response to treatment (falling CRP indicates response)
- **Prognosis:** Higher CRP associated with worse outcomes (infection, cardiovascular disease, malignancy)
- **Screening:** Not recommended (too non-specific)

**SOURCES:** BSR Guidelines, NICE Guidelines, British Association of Dermatologists Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["BSR Guidelines", "NICE Guidelines", "British Association of Dermatologists Guidelines"]
            }
        )

    def _handle_urine_culture(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Urine microscopy, culture and sensitivity (MC&S) interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**URINE MICROSCOPY, CULTURE AND SENSITIVITY (MC&S) INTERPRETATION**

**URINE SAMPLE COLLECTION:**

**Midstream urine (MSU):**
- **Method:** Collect midstream sample after cleansing genital area (reduce contamination)
- **Transport:** To laboratory within 2 hours (or refrigerated at 4°C for up to 24 hours)
- **Container:** Sterile universal container

**Catheter specimen:**
- **Indication:** If patient catheterised, or unable to provide MSU
- **Method:** Clamp catheter distal to port, clean port with alcohol swab, aspirate urine with needle and syringe

**Suprapubic aspiration:**
- **Indication:** If diagnosis uncertain (e.g., children, pregnancy)
- **Method:** Ultrasound-guided needle aspiration of bladder (sterile sample)

**URINE DIPSTICK:**

**Nitrites:**
- **Produced by:** Gram-negative bacteria (E. coli, Klebsiella, Proteus, Pseudomonas) converting nitrate to nitrite
- **Sensitivity:** Poor (only detects Gram-negative bacteria)
- **Specificity:** Good (rare false positives)
- **Time:** Requires 4 hours in bladder (negative if recent voiding)

**Leucocyte esterase:**
- **Produced by:** White blood cells (pyuria)
- **Sensitivity:** Good (detects pyuria)
- **Specificity:** Poor (pyuria can occur in non-UTI inflammation, e.g., interstitial cystitis, vaginitis)

**Blood:**
- **Causes:** UTI, menstruation, trauma, renal stones, glomerular disease
- **Differentiation:** Red cell morphology on urine microscopy (dysmorphic red cells = glomerular disease)

**URINE MICROSCOPY:**

**White blood cells (WBCs):**
- **Normal:** <10 WBCs/μL (or <10 WBCs per high-power field)
- **Pyuria:** ≥10 WBCs/μL (suggests inflammation, UTI)

**Red blood cells (RBCs):**
- **Normal:** <3 RBCs/μL (or <3 RBCs per high-power field)
- **Haematuria:** ≥3 RBCs/μL (requires investigation if asymptomatic and persistent)

**Bacteria:**
- **Normal:** None (or occasional contaminants)
- **Bacteriuria:** Presence of bacteria on microscopy

**URINE CULTURE:**

**Significant bacteriuria:**
- **≥10⁵ colony-forming units (CFU)/mL** (single organism) in asymptomatic patients
- **≥10³ CFU/mL** in symptomatic women (catheter specimen or suprapubic aspiration)
- **≥10⁴ CFU/mL** in symptomatic men

**Contaminants:**
- **Mixed growth:** Multiple organisms (≥2 organisms, each <10⁵ CFU/mL) (suggests contamination)
- **Low count:** <10⁴ CFU/mL (in asymptomatic patients)

**COMMON UTI PATHOGENS:**

**1. Escherichia coli (E. coli):**
- **Frequency:** 70-80% of community-acquired UTIs
- **Antibiotic resistance:** Increasing resistance to trimethoprim, quinolones

**2. Klebsiella pneumoniae:**
- **Frequency:** 5-10% of community-acquired UTIs
- **Antibiotic resistance:** ESBL-producing strains (resistant to cephalosporins)

**3. Proteus mirabilis:**
- **Frequency:** 2-5% of community-acquired UTIs
- **Clinical:** Associated with struvite stones (urea-producing, alkalinises urine)

**4. Enterococcus faecalis:**
- **Frequency:** 2-5% of community-acquired UTIs
- **Antibiotic resistance:** Intrinsic resistance to cephalosporins

**5. Pseudomonas aeruginosa:**
- **Frequency:** 5-10% of hospital-acquired UTIs
- **Antibiotic resistance:** Resistant to many oral antibiotics (requires IV treatment)

**6. Staphylococcus saprophyticus:**
- **Frequency:** 5-10% of community-acquired UTIs in young women
- **Antibiotic sensitivity:** Usually sensitive to most oral antibiotics

**ANTIBIOTIC SENSITIVITY TESTING:**

**Sensitive (S):** Antibiotic inhibits bacterial growth at clinically achievable concentrations
**Intermediate (I):** Antibiotic inhibits bacterial growth at high concentrations (may not be achievable with standard dosing)
**Resistant (R):** Antibiotic does not inhibit bacterial growth at clinically achievable concentrations

**COMMON FIRST-LINE ANTIBIOTICS FOR UNCOMPLICATED UTI:**

**1. Nitrofurantoin:**
- **Dose:** 100 mg MR BD for 3 days (women), 7 days (men)
- **Mechanism:** Bactericidal (inhibits bacterial enzymes)
- **Spectrum:** E. coli, Staph. saprophyticus, Enterococcus
- **Contraindications:** eGFR <45 mL/min/1.73 m²

**2. Trimethoprim:**
- **Dose:** 200 mg BD for 3 days (women), 7 days (men)
- **Mechanism:** Bacteriostatic (inhibits bacterial DNA synthesis)
- **Spectrum:** E. coli (if sensitive)
- **Check local resistance rates:** If >20% resistance, avoid as first-line

**3. Fosfomycin:**
- **Dose:** 3 g single dose (women)
- **Mechanism:** Bactericidal (inhibits bacterial cell wall synthesis)
- **Spectrum:** E. coli, Enterococcus
- **Alternative:** For resistant UTIs

**SECOND-LINE ANTIBIOTICS FOR COMPLICATED UTI:**

**1. Ciprofloxacin:**
- **Dose:** 500 mg BD for 7 days
- **Mechanism:** Bactericidal (inhibits bacterial DNA gyrase)
- **Spectrum:** Gram-negative bacteria (E. coli, Klebsiella, Proteus, Pseudomonas)
- **Reserve for:** Resistant UTIs, complicated UTIs

**2. Co-amoxiclav:**
- **Dose:** 500/125 mg TDS for 7 days
- **Mechanism:** Bactericidal (inhibits bacterial cell wall synthesis)
- **Spectrum:** Gram-positive and Gram-negative bacteria (including Enterococcus)

**3. Cefalexin:**
- **Dose:** 500 mg TDS for 7 days
- **Mechanism:** Bactericidal (inhibits bacterial cell wall synthesis)
- **Spectrum:** Gram-positive and Gram-negative bacteria (excluding Pseudomonas)

**ASYMPTOMATIC BACTERIURIA:**

**Definition:** Significant bacteriuria (≥10⁵ CFU/mL) without UTI symptoms

**Management:** **DO NOT TREAT** (antibiotics do not reduce risk of symptomatic UTI, increase antibiotic resistance)

**Exceptions:**
- **Pregnancy:** Treat (screening at 12-16 weeks, treat if positive)
- **Urological procedures:** Treat (prostate biopsy, ureteroscopy)
- **Neutropenic patients:** Treat (immunocompromised)

**RECURRENT UTI:**

**Definition:** ≥2 UTIs in 6 months, or ≥3 UTIs in 12 months

**Management:**
- **Trigger avoidance:** Hydration, void after intercourse, avoid spermicides
- **Antibiotic prophylaxis:** Post-coital (single dose after intercourse) or continuous (low-dose nightly for 6 months)
- **Vaginal oestrogen:** Post-menopausal women (reduce risk of recurrent UTI)
- **Investigations:** Ultrasound urinary tract, cystoscopy (if risk factors for structural abnormality)

**SOURCES:** PHE Guidelines, NICE Guidelines (NG110), EAU Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["PHE Guidelines", "NICE Guidelines (NG110)", "EAU Guidelines"]
            }
        )

    def _handle_blood_culture(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Blood culture interpretation and sepsis management"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**BLOOD CULTURE - INTERPRETATION AND SEPSIS MANAGEMENT**

**BLOOD CULTURE COLLECTION:**

**Indications:**
- **Sepsis:** Systemic inflammatory response syndrome (SIRS) with suspected infection
- **Fever:** Pyrexia of unknown origin (PUO)
- **Endocarditis:** Suspected infective endocarditis
- **Meningitis:** Suspected bacterial meningitis
- **Immunocompromised:** Chemotherapy, transplantation, HIV (high risk of bacteraemia)

**Collection technique:**
- **Skin preparation:** Chlorhexidine or povidone-iodine (allow to dry)
- **Volume:** 20-30 mL per blood culture set (2 sets = 4 bottles)
- **Sites:** Two separate venepuncture sites (reduce contamination)
- **Timing:** Before antibiotics (ideally)

**Blood culture bottles:**
- **Aerobic bottle:** Grows aerobic bacteria (most common pathogens)
- **Anaerobic bottle:** Grows anaerobic bacteria (e.g., Bacteroides, Clostridium)

**Blood culture sets:**
- **1 set:** 2 bottles (1 aerobic, 1 anaerobic)
- **2 sets:** 4 bottles (recommended for sepsis)

**BLOOD CULTURE INTERPRETATION:**

**POSITIVE BLOOD CULTURE:**
- **Significant bacteraemia:** Same organism grown from ≥2 sets (pathogenic)
- **Contaminant:** Organism grown from 1 set only (likely skin contaminant)
- **Polymicrobial:** Multiple organisms (contamination or intra-abdominal sepsis)

**Time to positivity:**
- **Most bacteria:** 12-48 hours
- **Fast-growing (Strep. pneumoniae, Staph. aureus):** 8-12 hours
- **Slow-growing (HACEK organisms):** 5-7 days
- **Fungi (Candida):** 24-72 hours

**COMMON BLOOD CULTURE PATHOGENS:**

**Gram-positive bacteria:**
- **Staphylococcus aureus:** Skin and soft tissue infection, endocarditis, line infection
- **Coagulase-negative staphylococci (CoNS):** Contaminant (unless ≥2 sets positive, immunocompromised, or prosthetic device)
- **Streptococcus pneumoniae:** Pneumonia, meningitis
- **Enterococcus faecalis/faecium:** Intra-abdominal sepsis, urinary tract infection, endocarditis
- **Viridans streptococci:** Endocarditis

**Gram-negative bacteria:**
- **Escherichia coli:** Urinary tract infection, intra-abdominal sepsis
- **Klebsiella pneumoniae:** Pneumonia, urinary tract infection, intra-abdominal sepsis
- **Pseudomonas aeruginosa:** Hospital-acquired infection, immunocompromised
- **Haemophilus influenzae:** Pneumonia, meningitis
- **Neisseria meningitidis:** Meningitis, meningococcaemia

**Fungi:**
- **Candida albicans:** Fungal sepsis (immunocompromised, central venous catheters)
- **Candida glabrata:** Fungal sepsis (resistant to fluconazole)

**Anaerobes:**
- **Bacteroides fragilis:** Intra-abdominal sepsis
- **Clostridium perfringens:** Gas gangrene, septic abortion

**BLOOD CULTURE CONTAMINANTS:**

**Common contaminants:**
- **Coagulase-negative staphylococci (CoNS):** Staphylococcus epidermidis (skin commensal)
- **Corynebacterium species:** Diphtheroids (skin commensal)
- **Propionibacterium acnes:** Skin commensal
- **Viridans streptococci:** Oral commensal (unless endocarditis suspected)

**Distinguishing contaminant vs. pathogen:**
- **≥2 sets positive:** Pathogenic
- **1 set positive:** Contaminant (unless high-risk patient or clinical suspicion of infection)

**ANTIBIOTIC SENSITIVITY TESTING:**

**Sensitive (S):** Antibiotic inhibits bacterial growth at clinically achievable concentrations
**Intermediate (I):** Antibiotic inhibits bacterial growth at high concentrations
**Resistant (R):** Antibiotic does not inhibit bacterial growth

**COMMON ANTIBIOTIC RESISTANCE MECHANISMS:**

**Methicillin-resistant Staphylococcus aureus (MRSA):**
- **Mechanism:** Altered penicillin-binding protein (PBP2a)
- **Treatment:** Vancomycin, teicoplanin, linezolid

**Extended-spectrum beta-lactamase (ESBL)-producing Enterobacteriaceae:**
- **Mechanism:** Enzyme that hydrolyses penicillins, cephalosporins, aztreonam
- **Treatment:** Carbapenems (meropenem, ertapenem)

**Carbapenem-resistant Enterobacteriaceae (CRE):**
- **Mechanism:** Carbapenemase production (KPC, NDM)
- **Treatment:** Polymyxin B, colistin, tigecycline

**SEPSIS MANAGEMENT:**

**Sepsis six (within 1 hour):**
1. **Oxygen:** 15 L/min if hypoxic (SpO2 <94% on room air)
2. **Intravenous access:** Two large-bore cannulae
3. **Blood cultures:** Before antibiotics (2 sets, 4 bottles)
4. **Intravenous antibiotics:** Broad-spectrum (e.g., meropenem 1 g IV TDS + vancomycin 1 g IV BD)
5. **Fluid resuscitation:** Crystalloid bolus (500-1000 mL 0.9% NaCl or Hartmann's solution)
6. **Lactate measurement:** Serum lactate (prognostic marker, guides resuscitation)

**Antibiotic selection (empirical):**
- **Community-acquired sepsis:** Co-amoxiclav 1.2 g IV TDS + gentamicin 5-7 mg/kg OD
- **Hospital-acquired sepsis:** Meropenem 1 g IV TDS + vancomycin 1 g IV BD
- **Neutropenic sepsis:** Meropenem 1 g IV TDS + vancomycin 1 g IV BD
- **Meningitis:** Ceftriaxone 2 g IV BD + vancomycin 1 g IV BD

**Antibiotic de-escalation:**
- **Review at 48-72 hours:** Review blood culture results, clinical response
- **Narrow spectrum:** Switch to narrow-spectrum antibiotic (targeted therapy)
- **Duration:** 5-7 days (uncomplicated sepsis), 7-14 days (complicated sepsis, endocarditis)

**SOURCES:** BSAC Guidelines, NICE Guidelines (NG51), Surviving Sepsis Campaign Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "urgent",
                "specialty": "pathology",
                "sources": ["BSAC Guidelines", "NICE Guidelines (NG51)", "Surviving Sepsis Campaign Guidelines"]
            }
        )

    def _handle_tumour_markers(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Tumour markers interpretation and clinical utility"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**TUMOUR MARKERS - INTERPRETATION AND CLINICAL UTILITY**

**GENERAL PRINCIPLES:**

- **Tumour markers:** Substances produced by cancer cells or by the body in response to cancer
- **Utility:** Screening, diagnosis, monitoring response to treatment, detecting recurrence
- **Limitations:** Poor specificity (elevated in benign conditions), poor sensitivity (not all cancers produce markers)

**COMMON TUMOUR MARKERS:**

**1. PROSTATE-SPECIFIC ANTIGEN (PSA):**

**Physiology:**
- **Source:** Prostate epithelial cells
- **Function:** Liquify semen (prevents coagulation)
- **Normal range:** <4.0 μg/L (age-adjusted: age <50: <2.5 μg/L, age 50-59: <3.5 μg/L, age 60-69: <4.5 μg/L, age >70: <6.5 μg/L)

**Clinical utility:**
- **Prostate cancer screening:** Controversial (USPSTF recommends against routine screening, PSA testing available in UK for informed men aged ≥50)
- **Prostate cancer monitoring:** Rising PSA after treatment indicates recurrence
- **Prostate cancer prognosis:** Higher PSA associated with higher stage/grade

**Elevated PSA causes (non-cancerous):**
- **Benign prostatic hyperplasia (BPH):** Enlarged prostate (very common in elderly men)
- **Prostatitis:** Prostate inflammation/infection
- **Prostate manipulation:** Recent prostate biopsy, DRE, ejaculation (wait 48 hours before PSA)
- **Urinary retention:** Acute or chronic
- **Prostate infarction:** Rare (after prostate artery embolisation)

**Prostate cancer risk assessment:**
- **PSA <4 μg/L:** Low risk (but not zero risk)
- **PSA 4-10 μg/L:** Intermediate risk (prostate biopsy may be indicated)
- **PSA >10 μg/L:** High risk (prostate biopsy indicated)

**PSA velocity:** Rate of PSA rise (>0.75 μg/L/year associated with prostate cancer)

**Free/total PSA ratio:** Lower free:total ratio associated with prostate cancer (<10% free PSA associated with higher risk)

**2. ALPHA-FETOPROTEIN (AFP):**

**Physiology:**
- **Source:** Fetal liver, yolk sac
- **Normal adult range:** <10 μg/L

**Clinical utility:**
- **Hepatocellular carcinoma (HCC):** Elevated in 70-90% of HCC
- **Non-seminomatous germ cell tumours:** Yolk sac tumour (endodermal sinus tumour)
- **Monitoring:** AFP level correlates with tumour burden (rising AFP indicates recurrence)

**Elevated AFP causes (non-cancerous):**
- **Pregnancy:** Fetal source (normal in pregnancy)
- **Hepatitis:** Acute or chronic hepatitis (elevated transaminases)
- **Cirrhosis:** Regenerative nodules (benign liver disease)

**3. CARCINOEMBRYONIC ANTIGEN (CEA):**

**Physiology:**
- **Source:** Fetal gastrointestinal tract
- **Normal range:** <3 μg/L (non-smokers), <5 μg/L (smokers)

**Clinical utility:**
- **Colorectal cancer:** Pre-operative staging (elevated CEA associated with metastatic disease)
- **Monitoring:** Rising CEA after surgery indicates recurrence (lead time of 3-6 months before clinical/radiological recurrence)
- **Prognosis:** Higher CEA associated with worse prognosis

**Elevated CEA causes (non-cancerous):**
- **Smoking:** Mild elevation (<5 μg/L)
- **Inflammation:** Inflammatory bowel disease (Crohn's disease, ulcerative colitis)
- **Infection:** Pneumonia, bronchitis
- **Benign conditions:** Pancreatitis, liver cirrhosis

**4. CANCER ANTIGEN 125 (CA125):**

**Physiology:**
- **Source:** Mesothelial cells (pleura, peritoneum, pericardium)
- **Normal range:** <35 U/mL

**Clinical utility:**
- **Ovarian cancer:** Elevated in 80-90% of epithelial ovarian cancer
- **Monitoring:** Rising CA125 indicates recurrence, falling CA125 indicates response to treatment
- **Prognosis:** Higher CA125 associated with advanced stage

**Elevated CA125 causes (non-cancerous):**
- **Menstruation:** Mild elevation (physiological)
- **Pregnancy:** Mild elevation (physiological)
- **Endometriosis:** Mild-moderate elevation
- **Fibroids:** Mild elevation
- **Pelvic inflammatory disease:** Moderate elevation
- **Peritoneal inflammation:** Peritonitis, pancreatitis, liver cirrhosis

**5. HUMAN CHORIONIC GONADOTROPIN (HCG):**

**Physiology:**
- **Source:** Syncytiotrophoblast cells (placenta)
- **Normal range:** <5 IU/L (non-pregnant)

**Clinical utility:**
- **Gestational trophoblastic neoplasia (GTN):** Molar pregnancy, choriocarcinoma
- **Germ cell tumours:** Seminoma, non-seminomatous germ cell tumour
- **Monitoring:** Rising HCG indicates recurrence

**Elevated HCG causes (non-cancerous):**
- **Pregnancy:** Most common cause (physiological)
- **Menopause:** Mild elevation (due to pituitary HCG)
- **Marijuana use:** Mild elevation

**6. CANCER ANTIGEN 19-9 (CA19-9):**

**Physiology:**
- **Source:** Pancreatic ductal cells, biliary epithelial cells
- **Normal range:** <37 U/mL

**Clinical utility:**
- **Pancreatic cancer:** Elevated in 70-90% of pancreatic cancer
- **Biliary cancer:** Cholangiocarcinoma, gallbladder cancer
- **Monitoring:** Rising CA19-9 indicates recurrence

**Elevated CA19-9 causes (non-cancerous):**
- **Pancreatitis:** Acute or chronic pancreatitis
- **Biliary obstruction:** Choledocholithiasis, biliary stricture
- **Liver disease:** Cirrhosis, hepatitis
- **Lewis-negative individuals:** 5-10% of population lack Lewis antigens (cannot produce CA19-9, CA19-9 unreliable)

**TUMOUR MARKER LIMITATIONS:**

**Poor specificity:**
- **Elevated in benign conditions:** Inflammation, infection, physiological states (pregnancy, menstruation)
- **Elevated in non-target cancers:** Many tumour markers produced by multiple cancer types

**Poor sensitivity:**
- **Not all cancers produce markers:** Early-stage cancers may not produce detectable levels
- **False-negative results:** Normal tumour marker does not exclude cancer

**CLINICAL SCENARIOS:**

**1. SCREENING:**
- **Prostate cancer:** PSA (controversial, not recommended for population screening)
- **Ovarian cancer:** CA125 + transvaginal ultrasound (limited sensitivity/specificity)
- **Hepatocellular carcinoma:** AFP + liver ultrasound (high-risk patients: cirrhosis, hepatitis B/C)

**2. DIAGNOSIS:**
- **Tumour markers alone are NOT diagnostic:** Tissue diagnosis (biopsy) required
- **Tumour markers support diagnosis:** Elevated PSA + abnormal DRE/trus biopsy → prostate cancer

**3. MONITORING:**
- **Response to treatment:** Falling tumour marker indicates response (e.g., falling AFP in HCC after chemotherapy)
- **Recurrence:** Rising tumour marker indicates recurrence (e.g., rising CEA after colorectal cancer surgery)
- **Lead time:** Tumour markers may detect recurrence months before clinical/radiological recurrence

**4. PROGNOSIS:**
- **Higher tumour marker levels:** Associated with advanced stage, worse prognosis
- **Tumour marker kinetics:** Rapid rise (short doubling time) associated with aggressive disease

**SOURCES:** NICE Guidelines, ESMO Guidelines, ASCO Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["NICE Guidelines", "ESMO Guidelines", "ASCO Guidelines"]
            }
        )

    def _handle_general_pathology(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """General pathology consultation and laboratory test interpretation"""

        return DomainQueryResult(
            domain_name="pathology",
            answer="""**PATHOLOGY AND LABORATORY MEDICINE**

Pathology is the study of disease, involving the analysis of blood, tissue, and other samples to diagnose and monitor disease.

**PATHOLOGY SPECIALTIES:**

**1. CLINICAL BIOCHEMISTRY:**
- **Tests:** Blood tests (urea and electrolytes, liver function tests, thyroid function tests, lipid profile, HbA1c)
- **Common investigations:**
  - **U&E (Urea and Electrolytes):** Kidney function, electrolyte imbalance (sodium, potassium, urea, creatinine)
  - **LFT (Liver Function Tests):** Liver function, liver disease (bilirubin, ALT, AST, ALP, GGT, albumin, INR)
  - **TFT (Thyroid Function Tests):** Thyroid function, thyroid disease (TSH, FT4, FT3)
  - **Lipid profile:** Cardiovascular risk assessment (total cholesterol, HDL, LDL, triglycerides)
  - **HbA1c:** Diabetes diagnosis and monitoring
  - **Troponin:** Acute coronary syndrome
  - **D-dimer:** Venous thromboembolism rule-out
  - **CRP/ESR:** Inflammatory markers

**2. HAEMATOLOGY:**
- **Tests:** Blood tests (full blood count, coagulation studies)
- **Common investigations:**
  - **FBC (Full Blood Count):** Anaemia, infection, leukaemia (haemoglobin, MCV, MCHC, white cell count, platelet count)
  - **Blood film:** Red cell morphology, white cell morphology (anaemia classification, leukaemia diagnosis)
  - **INR/PT/APTT:** Coagulation, warfarin monitoring, bleeding disorders
  - **Reticulocyte count:** Bone marrow response (anaemia assessment)
  - **Haematinics:** Anaemia assessment (ferritin, iron, TIBC, B12, folate)

**3. MICROBIOLOGY:**
- **Tests:** Infection diagnosis (culture, sensitivity testing, PCR)
- **Common investigations:**
  - **Blood cultures:** Sepsis, bacteraemia
  - **Urine MC&S:** Urinary tract infection
  - **Sputum culture:** Pneumonia, tuberculosis
  - **Wound swab:** Skin and soft tissue infection
  - **Throat swab:** Streptococcal pharyngitis
  - **CSF analysis:** Meningitis, encephalitis
  - **Stool culture:** Gastroenteritis
  - **PCR tests:** COVID-19, influenza, sexually transmitted infections (Chlamydia, gonorrhoea)

**4. HISTOPATHOLOGY:**
- **Tests:** Tissue diagnosis (biopsy, surgical specimen)
- **Common investigations:**
  - **Biopsy:** Cancer diagnosis, inflammation, infection
  - **Surgical specimen:** Cancer staging, margin assessment
  - **Cervical smear:** Cervical cancer screening
  - **Skin biopsy:** Skin cancer diagnosis (melanoma, BCC, SCC)

**5. BLOOD TRANSFUSION:**
- **Tests:** Blood grouping, crossmatching, transfusion science
- **Common investigations:**
  - **Blood group and screen:** ABO grouping, RhD typing, antibody screen
  - **Crossmatch:** Compatibility testing before transfusion
  - **Direct antiglobulin test (Coombs test):** Haemolytic anaemia, haemolytic disease of the newborn

**6. IMMUNOLOGY:**
- **Tests:** Autoimmune disease, allergy, immunodeficiency
- **Common investigations:**
  - **Autoantibodies:** Rheumatoid factor, anti-CCP (rheumatoid arthritis), ANA (SLE), anti-dsDNA (SLE), ANCA (vasculitis)
  - **Allergy testing:** Skin prick testing, specific IgE (RAST)
  - **Immunodeficiency:** Immunoglobulin levels (IgG, IgA, IgM), HIV testing, complement levels

**CLINICAL QUESTIONS:**

- "What blood tests should I order for [condition]?" → Consider clinical context, pre-test probability, test performance
- "What does this abnormal result mean?" → Consider reference ranges, clinical context, confirmatory testing
- "Is this result significant?" → Consider magnitude of abnormality, trend over time, clinical context
- "What are the reference ranges?" → Laboratory-specific reference ranges (age- and sex-dependent)
- "How do I interpret this test?" → Consider sensitivity, specificity, positive predictive value, negative predictive value

**TEST INTERPRETATION PRINCIPLES:**

- **Treat the patient, not the numbers:** Clinical context is essential
- **Trends are important:** Changes over time more informative than single values
- **Pre-test probability matters:** Low pre-test probability reduces positive predictive value (more false positives)
- **Confirmatory testing:** Abnormal screening test requires confirmatory test (e.g., abnormal PSA → prostate biopsy)
- **Incidental findings:** Abnormal results may be unrelated to presenting complaint (e.g., incidental hyponatraemia)

**SOURCES:** RCPath Guidelines, NICE Guidelines, BCSH Guidelines""",
            confidence=0.85,
            metadata={
                "urgency": "non-urgent",
                "specialty": "pathology",
                "sources": ["RCPath Guidelines", "NICE Guidelines", "BCSH Guidelines"]
            }
        )


def create_pathology_domain():
    """Factory function for Pathology Domain"""
    return PathologyDomain()
