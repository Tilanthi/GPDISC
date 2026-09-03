"""
Palliative Care Domain for GPDISC

Comprehensive palliative care consultation covering:
- Pain management (cancer and non-cancer pain)
- Symptom control (nausea, vomiting, constipation, dyspnoea)
- End-of-life care
- Psychosocial support
- Advance care planning
- Spiritual and existential distress
- Communication skills (breaking bad news, goals of care discussions)
- Bereavement support

Evidence-based guidelines:
- NICE NGxx guidelines
- EAPC (European Association for Palliative Care)
- Association for Palliative Medicine of Great Britain & Ireland
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class PalliativeCareDomain(BaseDomainModule):
    """
    Palliative Care domain for comprehensive palliative and end-of-life
    care consultation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="palliative_care",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive palliative care: pain management, symptom control, end-of-life care, psychosocial support, advance care planning",
            keywords=[
                "palliative care", "palliative", "end of life", "terminal", "hospice",
                "pain management", "cancer pain", "morphine", "opioid", "analgesia",
                "symptom control", "nausea", "vomiting", "constipation", "dyspnoea", "breathlessness",
                "advance care planning", "living will", "dnar", "resuscitation", "dnacpr",
                "breaking bad news", "prognosis", "life expectancy", "prognostication",
                "bereavement", "grief", "loss", "spiritual", "existential",
                "secretions", "death rattle", "syringe driver", "pump", "anticipatory",
                "agitation", "terminal restlessness", "delirium", "confusion",
                " malignant spinal cord compression", "hypercalcaemia", "svc obstruction"
            ],
            capabilities=[
                "pain_management",
                "symptom_control",
                "end_of_life_care",
                "anticipatory_prescribing",
                "advance_care_planning",
                "psychosocial_support",
                "communication_difficult_conversations",
                "bereavement_support",
                "palliative_emergencies"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process palliative care query with emergency detection
        """
        query_lower = query.lower()

        # PALLIATIVE EMERGENCIES - HIGHEST PRIORITY

        # Malignant spinal cord compression
        if any(term in query_lower for term in ["spinal cord compression", "mscc", "malignant spinal",
                                                   "spinal compression", "cord compression"]):
            return self._handle_spinal_cord_compression(query, context)

        # Hypercalcaemia
        if any(term in query_lower for term in ["hypercalcaemia", "high calcium", "elevated calcium",
                                                   "calcium high"]):
            return self._handle_hypercalcaemia(query, context)

        # SVC obstruction
        if any(term in query_lower for term in ["svc", "superior vena cava", "svc obstruction",
                                                   "facial swelling", "swollen face"]):
            return self._handle_svc_obstruction(query, context)

        # PAIN MANAGEMENT
        if any(term in query_lower for term in ["pain", "pain management", "morphine", "opioid",
                                                   "analgesia", "analgesic", "severe pain",
                                                   "cancer pain", "breakthrough pain"]):
            return self._handle_pain_management(query, context)

        # NAUSEA AND VOMITING
        if any(term in query_lower for term in ["nausea", "vomiting", "emesis", "antiemetic",
                                                   "feeling sick", "being sick"]):
            return self._handle_nausea_vomiting(query, context)

        # CONSTIPATION
        if any(term in query_lower for term in ["constipation", "bowel obstruction", "no bowel movement",
                                                   "opened bowels", "not opened bowels"]):
            return self._handle_constipation(query, context)

        # DYSPNOEA (BREATHLESSNESS)
        if any(term in query_lower for term in ["dyspnoea", "breathlessness", "shortness of breath",
                                                   "breathing difficulty", "difficulty breathing"]):
            return self._handle_dyspnoea(query, context)

        # AGITATION / DELIRIUM
        if any(term in query_lower for term in ["agitation", "restlessness", "confusion", "delirium",
                                                   "terminal restlessness", "hallucination"]):
            return self._handle_agitation_delirium(query, context)

        # SECRETIONS / DEATH RATTLE
        if any(term in query_lower for term in ["secretions", "death rattle", "noisy breathing",
                                                   "respiratory secretions"]):
            return self._handle_secretions(query, context)

        # SYRINGE DRIVER / PUMP
        if any(term in query_lower for term in ["syringe driver", "pump", "csci",
                                                   "subcutaneous infusion"]):
            return self._handle_syringe_driver(query, context)

        # ANTICIPATORY PRESCRIBING
        if any(term in query_lower for term in ["anticipatory", "anticipatory prescribing",
                                                   "just in case", "end of life drugs"]):
            return self._handle_anticipatory_prescribing(query, context)

        # ADVANCE CARE PLANNING
        if any(term in query_lower for term in ["advance care planning", "living will", "advance directive",
                                                   "dnacpr", "dnar", "resuscitation", "resus"]):
            return self._handle_advance_care_planning(query, context)

        # BREAKING BAD NEWS
        if any(term in query_lower for term in ["breaking bad news", "prognosis", "life expectancy",
                                                   "prognostication", "prognostic indicator"]):
            return self._handle_breaking_bad_news(query, context)

        # GENERAL PALLIATIVE CARE
        return self._handle_general_palliative_care(query, context)

    def _handle_spinal_cord_compression(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle malignant spinal cord compression - palliative emergency"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**MALIGNANT SPINAL CORD COMPRESSION (MSCC) - PALLIATIVE EMERGENCY**

**IMMEDIATE ACTION:**
- **URGENT oncology referral** (same day)
- **Start Dexamethasone IMMEDIATELY** (do not delay for imaging if high clinical suspicion)
- **Arrange MRI whole spine** (within 24 hours)

**RISK STRATIFICATION:**

**HIGH RISK (≥50% probability) - START DEXAMETHASONE IMMEDIATELY:**
- Known cancer + back pain + **ANY** of following:
  - Weakness (difficulty standing/walking)
  - Sensory changes (numbness, tingling)
  - Bladder dysfunction (hesitancy, retention, incontinence)
  - Bowel dysfunction (constipation, incontinence)
  - Thoracic level pain (radiating around chest/abdomen)

**MODERATE RISK (5-50%):**
- Known cancer + back pain + **NO** neurological symptoms
- **Urgent MRI** (within 24-48 hours)

**LOW RISK (<5%):**
- No cancer diagnosis (investigate alternative causes)
- No neurological symptoms
- **Routine referral**

**IMMEDIATE MANAGEMENT:**

**1. Dexamethasone (HIGH RISK):**
- **Loading dose:** Dexamethasone 16 mg PO/IV
- **Maintenance:** Dexamethasone 16 mg daily** (divided BD or single dose)
- **Rapid improvement** in pain and neurological function expected (within 24-72 hours)
- **Gastric protection:** PPI (Omeprazole 20 mg daily) if on dexamethasone >2 weeks
- **Taper** after definitive treatment (radiotherapy/surgery) as per oncology

**2. Pain control:**
- ** escalate analgesia** (severe pain common)
- **Paracetamol** 1 g QDS
- **Opioid:** Morphine (or appropriate strong opioid)
- **adjuvant:** consider neuropathic pain agents (Amitriptyline, Gabapentin, Pregabalin)

**3. Spinal precautions:**
- **Log roll** for transfers (prevent further damage)
- **Avoid spinal manipulation** (physiotherapy, chiropractic)
- **Encourage mobilisation** if no neurological deficit (bed rest NOT recommended)

**INVESTIGATIONS:**

**MRI whole spine (gold standard):**
- **T1-weighted + T2-weighted + STIR sequences**
- Identifies level(s) of compression
- Identifies skip lesions

**CT myelogram** (if MRI contraindicated - pacemaker, severe claustrophobia)
- Equivalent diagnostic accuracy to MRI

**DEFINITIVE TREATMENT:**

**Decision-making (multidisciplinary):**

**Factors considered:**
- **Tumour type:** radio-sensitive vs. radio-resistant
- **Level of compression:** cervical, thoracic, lumbar
- **Neurological status:** ambulant vs. non-ambulant
- **Previous radiotherapy** (re-irradiation risk)
- **Life expectancy**
- **Patient preference**

**Radiotherapy (most common):**
- **External beam radiotherapy (EBRT)**
- **Fractionation:**
  - **Single fraction (8 Gy):** poor prognosis, short life expectancy
  - **Multiple fractions (20 Gy in 5 fractions, 30 Gy in 10 fractions):** better local control, longer life expectancy
- **Outpatient treatment** (usually)
- **Pain relief:** 70-80%
- **Ambulant patients:** 80-90% remain ambulant
- **Non-ambulant patients:** 30-50% regain ability to walk

**Surgery:**
- **Indications:**
  - Spinal instability
  - Radio-resistant tumour (renal cell carcinoma, melanoma, sarcoma)
  - Previous radiotherapy to same site
  - Progressive neurological deficit despite radiotherapy
  - Tissue diagnosis required (unknown primary)
- **Procedure:** surgical decompression ± spinal fixation (instrumentation)
- **Followed by:** post-operative radiotherapy
- **Outcomes:** better pain relief and ambulation than radiotherapy alone in selected patients

**PROGNOSIS:**
- **Ambulant at diagnosis:** median survival 6-12 months
- **Non-ambulant at diagnosis:** median survival 1-3 months
- **Poor prognostic factors:** high tumour burden, visceral metastases, poor performance status

**COMPLICATIONS:**
- **Paraplegia** (if not treated promptly)
- **Incontinence** (urinary and/or faecal)
- **Pressure ulcers** (if immobile)
- **Deep vein thrombosis** (DVT)
- **Depression** (adjustment to loss of function)

**FOLLOW-UP:**
- **Regular neurological assessment** (motor strength, sensation, sphincter function)
- **Monitor for:** late effects of radiotherapy (myelopathy)
- **Rehabilitation:** physiotherapy, occupational therapy

**Sources:** NICE CG175, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_hypercalcaemia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle hypercalcaemia - palliative emergency"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**HYPERCALCAEMIA OF MALIGNANCY - PALLIATIVE EMERGENCY**

**DEFINITION:**
- **Corrected serum calcium >2.6 mmol/L** (or >2.75 mmol/L depending on lab)
- **Common in cancer:** affects 20-30% of patients at some point
- **Most common causes:** squamous cell carcinoma (lung, head & neck), breast cancer, multiple myeloma, renal cell carcinoma

**PATHOPHYSIOLOGY:**
- **PTHrP (Parathyroid Hormone-Related Protein)** secretion by tumour (most common)
- **Local osteolysis:** bone metastases (breast, myeloma)
- **1,25-dihydroxyvitamin D** production (lymphoma)

**SYMPTOMS (remember "stones, bones, groans, thrones, psychic overtones"):**

**Mild (2.6-3.0 mmol/L):**
- Often asymptomatic
- Non-specific symptoms: fatigue, anorexia, nausea

**Moderate (3.0-3.5 mmol/L):**
- **GI:** nausea, vomiting, constipation, abdominal pain, anorexia
- **Renal:** polyuria, polydipsia, dehydration
- **Neurological:** confusion, lethargy, depression, cognitive impairment
- **Cardiac:** shortened QT interval, arrhythmias

**Severe (>3.5 mmol/L) - MEDICAL EMERGENCY:**
- **Severe confusion, drowsiness, coma**
- **Severe dehydration, pre-renal failure**
- **Pancreatitis**
- **Cardiac arrest**

**IMMEDIATE MANAGEMENT:**

**1. Aggressive Rehydration (CORNERSTONE):**
- **0.9% NaCl (Normal Saline) IV**
- **Rate:** 3-4 L/day (or 200-300 mL/hour)
- **Duration:** 24-48 hours
- **Monitoring:** fluid balance, daily U&E (watch for fluid overload)
- **Caution:** in heart failure or renal failure

**2. Loop Diuretic (if fluid overloaded):**
- **Furosemide 20-40 mg IV** (after adequate rehydration)
- **Increases calcium excretion**
- **Monitor:** U&E, fluid balance

**3. Bisphosphonate (DEFINITIVE TREATMENT):**

**IV Bisphosphonates (most effective):**
- **Zoledronic acid 4 mg IV over 15 min** (preferred - single dose, potent)
- **Or:** Pamidronate 60-90 mg IV over 2-4 hours
- **Onset:** 2-4 days
- **Peak effect:** 4-7 days
- **Duration:** 2-4 weeks
- **Repeat:** every 3-4 weeks (for recurrent hypercalcaemia)

**Contraindications / precautions:**
- **Renal impairment:** dose adjust or avoid
- **Pregnancy:** contraindicated
- **Dental:** risk of osteonecrosis of jaw (avoid invasive dental work)

**Oral bisphosphonates (less commonly used):**
- **Clodronate 1600-3200 mg daily** (divided doses)
- **Onset:** slower, less potent than IV

**4. Denosumab (if bisphosphonate resistant or contraindicated):**
- **RANK ligand inhibitor**
- **120 mg SC weekly** (for hypercalcaemia)
- **Indications:** bisphosphonate-resistant hypercalcaemia, severe renal impairment
- **Onset:** rapid (1-3 days)
- **Calcium monitoring** (risk of hypocalcaemia)

**5. Calcitonin (rarely used):**
- **Calcitonin 100-200 IU SC/IM 6-12 hourly**
- **Rapid onset** (within hours)
- **Short duration** (tachyphylaxis develops)
- **Bridging therapy** while waiting for bisphosphonate effect

**6. Glucocorticoids (specific tumour types):**
- **Prednisolone 40-60 mg daily**
- **Indications:** lymphoma, myeloma (vitamin D-mediated hypercalcaemia)
- **Onset:** days
- **Mechanism:** inhibits 1α-hydroxylase (↓ 1,25-dihydroxyvitamin D)

**7. Treat underlying cause:**
- **Chemotherapy** (for tumour control)
- **Radiotherapy** (for local bone pain)
- **Surgery** (for solitary lesion)

**MONITORING:**
- **Daily calcium** (corrected)
- **Daily U&E** (renal function)
- **Fluid balance** (input/output)
- **Observations** (BP, HR, RR)

**RESPONSE TO TREATMENT:**
- **Good response:** calcium falls to <2.6 mmol/L within 5-7 days
- **Recurrent hypercalcaemia:** common (requires repeat bisphosphonate every 3-4 weeks)

**PROGNOSIS:**
- **Median survival:** 1-3 months (hypercalcaemia reflects advanced disease)
- **Poor prognostic factor:** hypercalcaemia

**SUPPORTIVE CARE:**
- **Advance care planning** (discuss goals of care)
- **Symptom control:** nausea, confusion, pain
- **Psychosocial support** (for patient and family)

**Sources:** NICE NG145, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_svc_obstruction(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle SVC obstruction - palliative emergency"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**SUPERIOR VENA CAVA (SVC) OBSTRUCTION - PALLIATIVE EMERGENCY**

**DEFINITION:**
- **Obstruction of superior vena cava** (SVC) by tumour compression or thrombosis
- **Medical emergency** (although not immediately life-threatening)

**AETIOLOGY:**
- **Lung cancer (small cell, non-small cell):** 75-80% of cases (right upper lobe tumour most common)
- **Lymphoma:** 10-15%
- **Metastatic disease:** breast, germ cell tumours
- **Thrombosis:** SVC thrombosis (indwelling catheters, pacemaker leads)

**PATHOPHYSIOLOGY:**
- **Obstruction** → impaired venous return from head, neck, upper extremities
- **Collateral circulation** develops (azygos, internal mammary veins)

**CLINICAL FEATURES:**

**Typical triad (not all present):**
1. **Facial swelling** (oedema) - puffiness, redness
2. **Arm swelling** (bilateral) - "brawny oedema"
3. **Distended neck veins** and veins on chest wall

**Other symptoms:**
- **Headache** (worse on lying flat, bending forward)
- **Facial plethora** (redness)
- **Dysphnoea** (breathlessness)
- **Cough**, **wheeze**
- **Dysphagia** (difficulty swallowing)
- **Hoarseness** (laryngeal oedema)
- **Confusion**, **drowsiness** (cerebral oedema - rare)

**SIGNS:**
- **Facial/neck/arm oedema** (pitting, non-tender)
- **Distended veins** (neck, chest wall - "caput medusae")
- **Plethora** (redness)
- **Cyanosis** (severe cases)
- **Horner's syndrome** (Pancoast tumour)

**IMMEDIATE MANAGEMENT:**

**1. Elevate head of bed:**
- **30-45° elevation** (reduces venous pressure, swelling)
- **Avoid lying flat**

**2. Oxygen:**
- **If hypoxic** (SpO2 <94%)
- **High-flow** (if respiratory distress)

**3. Dexamethasone:**
- **Dexamethasone 8-16 mg daily** (divided BD or single dose)
- **Reduces tumour oedema** → rapid symptom relief
- **Onset:** hours to days
- **Gastric protection:** PPI if on dexamethasone >2 weeks

**4. Urgent oncology referral:**
- **Same-day referral**
- **Definitive treatment:** chemotherapy, radiotherapy, stent insertion

**DEFINITIVE TREATMENT:**

**Decision-making (multidisciplinary):**

**Factors considered:**
- **Tumour type:** chemo-sensitive vs. chemo-resistant
- **Previous treatment:** radiotherapy field, chemotherapy response
- **Symptom severity:** laryngeal oedema, cerebral oedema (urgency)
- **Life expectancy**
- **Patient preference**

**Chemotherapy:**
- **First-line for chemosensitive tumours:**
  - Small cell lung cancer (rapid response)
  - Lymphoma (rapid response)
  - Germ cell tumours
- **Onset:** days to weeks
- **Response rate:** 70-90% (for chemosensitive tumours)

**Radiotherapy:**
- **Indications:** chemoresistant tumours, previous chemotherapy (poor response)
- **Fractionation:**
  - **Single fraction (8 Gy):** poor prognosis, urgent symptom relief
  - **Multiple fractions (20 Gy in 5 fractions, 30 Gy in 10 fractions):** better local control, longer life expectancy
- **Onset:** days to weeks
- **Response rate:** 60-80%

**Endovascular Stent Insertion:**
- **Indications:**
  - Rapid symptom relief required (laryngeal oedema, cerebral oedema)
  - Chemo-/radio-resistant tumour
  - Recurrent SVC obstruction after previous radiotherapy
- **Procedure:** percutaneous insertion of expandable metal stent into SVC
- **Onset:** immediate to days
- **Response rate:** 90%+ rapid symptom relief
- **Complications:** stent migration, thrombosis, infection

**Anticoagulation:**
- **Indicated:** if SVC thrombosis (not tumour compression)
- **Low molecular weight heparin** (Dalteparin, Tinzaparin)
- **Duration:** 3-6 months (or lifelong if malignancy persistent)

**SYMPTOMATIC MANAGEMENT:**

**Oedema:**
- **Elevation** of head and arms
- **Compression stockings** (caution - may worsen arm swelling)

**Headache:**
- **Dexamethasone** (reduces cerebral oedema)
- **Simple analgesia** (paracetamol, codeine)

**Anxiety:**
- **Reassurance** (SVC obstruction rarely immediately fatal)
- **Explanation:** collateral circulation develops
- **Anxiolytics** (Lorazepam 0.5-1 mg SL/PO PRN)

**PROGNOSIS:**
- **Without treatment:** median survival 4-8 weeks
- **With treatment:** median survival 4-12 months (depends on tumour type, stage)
- **Poor prognostic factor:** SVC obstruction (reflects advanced disease)

**COMPLICATIONS:**
- **Laryngeal oedema** (stridor, airway compromise) - **EMERGENCY**
- **Cerebral oedema** (confusion, drowsiness, seizures) - **EMERGENCY**
- **SVCO thrombosis** extension (DVT, PE)

**RED FLAGS (urgent intervention):**
- **Stridor** (laryngeal oedema)
- **Confusion, drowsiness** (cerebral oedema)
- **Facial cyanosis** (severe obstruction)

**Sources:** NICE NG145, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_pain_management(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle pain management"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**PAIN MANAGEMENT IN PALLIATIVE CARE**

**PRINCIPLES:**
- **Pain is whatever the patient says it is**
- **"By mouth, by the clock, by the ladder"** (WHO analgesic ladder)
- **Individualise treatment** (no "one size fits all")
- **Assess regularly** (pain score, effect of treatment, side effects)

**PAIN ASSESSMENT:**

**History:**
- **Site, radiation, character, severity, aggravating/relieving factors**
- **Temporal pattern:** continuous, episodic (breakthrough), incident pain
- **Impact on:** sleep, activity, mood, relationships
- **Current analgesia:** dose, frequency, effectiveness, side effects
- **Comorbidities:** renal impairment, hepatic impairment, respiratory disease

**Examination:**
- **Identify cause** of pain (if possible)
- **Neurological examination** (if neuropathic pain suspected)

**Pain assessment tools:**
- **Numerical rating scale (0-10):** 0 = no pain, 10 = worst pain imaginable
- **Visual analogue scale (VAS):** 100 mm line
- **Pain diary:** record pain scores, analgesia use, functional impact

**WHO ANALGESIC LADDER:**

**Step 1: Non-Opioid ± Adjuvant:**
- **Paracetamol 1 g QDS** (max 4 g/day)
- **NSAID** (if appropriate):
  - Naproxen 250-500 mg BD/TDS
  - Ibuprofen 400-600 mg TDS
  - Celecoxib 100-200 mg BD (if GI risk)
- **Adjuvants:** neuropathic agents, muscle relaxants, bisphosphonates

**Step 2: Weak Opioid + Non-Opioid ± Adjuvant:**
- **Codeine 30-60 mg QDS** (max 240 mg/day)
- **Tramadol 50-100 mg QDS** (max 400 mg/day)
- **Combination products:** Co-codamol, Co-dydramol (avoid long-term)

**Step 3: Strong Opioid + Non-Opioid ± Adjuvant:**
- **Morphine:** first-line strong opioid
- **Oxycodone:** alternative (renal impairment)
- **Fentanyl:** transdermal (stable opioid requirements)
- **Methadone:** specialist use only
- **Buprenorphine:** transdermal (renal impairment)

**STRONG OPIOIDS:**

**Morphine (first-line):**

**Starting doses (opioid-naïve):**
- **Immediate release (IR):** 2.5-5 mg 4-hourly PRN
- **Once controlled:** convert to **modified release (MR)** 12-hourly
- **Total daily dose (TDD) = IR dose × 6** (for 4-hourly dosing)
- **MR dose:** TDD/2 (12-hourly)

**Dose titration:**
- **Increase by 30-50%** every 2-3 days (if inadequate analgesia)
- **Review daily** (inpatient) or every 2-3 days (community)

**Breakthrough pain (episodic pain):**
- **Prescribe:** PRN immediate release morphine
- **Dose:** **1/6th of total daily dose** (round to nearest available strength)
- **Frequency:** 2-4 hourly PRN

**Switching opioids (opioid rotation):**
- **Indications:** inadequate analgesia, intolerable side effects
- **Calculate:** total daily dose of current opioid
- **Convert:** to equivalent dose of new opioid (use conversion chart)
- **Reduce:** by 25-50% (cross-tolerance incomplete)
- **Titrate:** to effect

**COMMON OPIOID SIDE EFFECTS:**

**Constipation (universal):**
- **PREVENT:** prescribe laxative from start
- **Stimulant laxative:** Senna 2-4 tablets at night (± softener: Lactulose 10-20 mL BD)
- **Osmotic laxative:** Macrogol (Movicol) 1-2 sachets daily

**Nausea and vomiting:**
- **Anti-emetic:** Metoclopramide 10 mg TDS or Haloperidol 1.5-3 mg BD
- **Usually resolves** within 1 week of starting opioid (continue anti-emetic if needed)

**Drowsiness/sedation:**
- **Common** at initiation or dose increase
- **Usually resolves** within 3-5 days
- **Reduce dose** if persistent (especially if affecting function)

**Confusion/hallucinations:**
- **Opioid toxicity** (especially renal impairment)
- **Reduce dose** or switch opioid

**Respiratory depression:**
- **Rare** with careful titration
- **Signs:** RR <10, cyanosis, drowsiness
- **Treatment:** naloxone 100-200 mcg IV/IM/SC (repeat PRN)

**Myoclonus (jerking):**
- **Opioid toxicity** (especially morphine, renal impairment)
- **Switch opioid** (e.g., to Oxycodone or Fentanyl)

**NEUROPATHIC PAIN:**

**Adjuvant analgesics:**
- **Amitriptyline:** start 10 mg at night, titrate to 50-100 mg
- **Gabapentin:** start 100 mg TDS, titrate to 300 mg TDS (max 1800 mg/day)
- **Pregabalin:** start 75 mg BD, titrate to 150 mg BD (max 600 mg/day)
- **Duloxetine:** 30-60 mg daily (especially for diabetic neuropathy, chemotherapy-induced neuropathy)

**BONE PAIN:**
- **NSAID:** (Naproxen 250-500 mg BD/TDS)
- **Bisphosphonate:** (Zoledronic acid 4 mg IV every 3-4 weeks)
- **Radiotherapy:** (localised bone pain, especially if pathological fracture risk)
- **Radionuclides:** (Strontium-89, Samarium-153 - for widespread bone pain)

**NON-PHARMACOLOGICAL:**
- **Radiotherapy** (bone pain, soft tissue infiltration)
- **Physiotherapy** (mobilisation, exercises)
- **Occupational therapy** (positioning, equipment)
- **Psychological support** (CBT, relaxation techniques)
- **TENS** (transcutaneous electrical nerve stimulation)
- **Heat/cold** (localised pain)

**EMERGENCIES:**
- **Spinal cord compression** (back pain + neurological symptoms)
- **Pathological fracture** (bone pain + deformity, loss of function)
- **Malignant wound ulceration** (foul-smelling, bleeding, painful)

**Sources:** NICE NG140, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_nausea_vomiting(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle nausea and vomiting"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**NAUSEA AND VOMITING IN PALLIATIVE CARE**

**DEFINITION:**
- **Nausea:** unpleasant sensation of needing to vomit
- **Vomiting:** forceful expulsion of gastric contents
- **Retching:** vomiting without expulsion of gastric contents
- **Very common** in palliative care (up to 70% of patients)

**ASSESSMENT:**

**History:**
- **Timing:** constant vs. episodic, relationship to meals/medications
- **Frequency:** number of episodes per day
- **Content:** food, blood, coffee-ground material, faeculent material
- **Associated symptoms:** abdominal pain, distension, constipation, headache
- **Medications:** recent changes, opioids, chemotherapy
- **Investigations:** calcium (hypercalcaemia), renal function (uraemia)

**CAUSES:**

**1. Gastrointestinal (most common):**
- **Gastric stasis:** opioids, diabetes, autonomic neuropathy
- **Bowel obstruction:** tumour, constipation
- **Gastric outlet obstruction:** tumour, peptic ulcer
- **Gastro-oesophageal reflux:** acid reflux
- **Hepatomegaly:** liver capsule stretch
- **Ascites:** abdominal distension

**2. Biochemical:**
- **Hypercalcaemia:** (nausea, constipation, confusion)
- **Uraemia:** (nausea, vomiting, drowsiness)
- **Hyponatraemia:** (nausea, headache, confusion)

**3. Drugs (very common):**
- **Opioids:** (gastric stasis, constipation)
- **Chemotherapy:** (direct stimulation of CTZ)
- **Antibiotics:** (direct mucosal irritation)
- **Iron supplements:** (gastric irritation)
- **Digoxin, theophylline:** (toxicity)

**4. Vestibular:**
- **Motion sickness**
- **Labyrinthitis, Meniere's disease**

**5. Central:**
- **Raised intracranial pressure:** (headache, vomiting, papilloedema)
- **Meningeal irritation:** (meningitis, subarachnoid haemorrhage)
- **Psychological:** (anxiety, anticipation)

**PRINCIPLES OF MANAGEMENT:**

1. **Identify and treat cause** (if possible)
2. **Prescribe regular anti-emetic** (not PRN)
3. **Choose anti-emetic based on presumed mechanism** (emetic pathway)
4. **Review regularly** (effectiveness, side effects)
5. **Use second anti-emetic** (if inadequate response) - **different mechanism**

**ANTI-EMETIC PATHWAYS:**

**1. Chemoreceptor Trigger Zone (CTZ):**
- **Dopamine antagonists:**
  - **Haloperidol** 1.5-3 mg BD (or 1.5-5 mg SC/IV)
  - **Levomepromazine** 6.25-25 mg BD/OD (or 6.25-25 mg SC)
  - **Metoclopramide** 10 mg TDS (or 10-20 mg SC/IV) - **also increases GI motility**
  - **Prochlorperazine** 5 mg TDS (or 12.5 mg PR/IM)

**2. Vagus nerve / Gastrointestinal tract:**
- **Motility stimulants:**
  - **Metoclopramide** 10 mg TDS
  - **Domperidone** 10-20 mg TDS
- **Muscarinic antagonists:**
  - **Hyoscine butylbromide (Buscopan)** 20 mg QDS PRN (or 20-60 mg SC/24h)
  - **Hyoscine hydrobromide (Scopolamine)** 0.3-0.6 mg SC/IV

**3. Vestibular apparatus:**
- **Antihistamines:**
  - **Cyclizine** 50 mg TDS (or 50 mg SC/IV)
  - **Promethazine** 25 mg BD/TDS
  - **Cinnarizine** 15 mg TDS

**4. Cortex (higher centres):**
- **Benzodiazepines:**
  - **Lorazepam** 0.5-1 mg SL/OD/BD
  - **Diazepam** 5-10 mg OD/BD
- **Corticosteroids:**
  - **Dexamethasone** 4-8 mg BD/OD (anti-emetic, reduces tumour oedema)

**ANTI-EMETIC SELECTION (BY CAUSE):**

**Gastric stasis (opioids, diabetes):**
- **Metoclopramide** 10 mg TDS SC/PO
- **Domperidone** 10-20 mg TDS PO

**Bowel obstruction:**
- **Hyoscine butylbromide (Buscopan)** 20-60 mg SC/24h
- **Levomepromazine** 6.25-25 mg SC/24h
- **Octreotide** 50-100 mcg SC TDS (reduces secretions)

**Chemotherapy-induced:**
- **5-HT3 antagonist:** Ondansetron 8 mg BD
- **Dexamethasone** 8 mg BD (additive effect)
- **Aprepitant** (NK1 antagonist) - for high-risk chemotherapy

**Raised intracranial pressure:**
- **Dexamethasone** 8-16 mg daily
- **Consider:** Cyclizine 50 mg TDS

**Vestibular:**
- **Cyclizine** 50 mg TDS
- **Promethazine** 25 mg BD/TDS

**Anxiety/anticipation:**
- **Lorazepam** 0.5-1 mg SL 1 hour before trigger (e.g., chemotherapy)

**Hypercalcaemia:**
- **Treat hypercalcaemia** (rehydration, bisphosphonate)
- **Anti-emetic:** Metoclopramide or Haloperidol

**Uraemia:**
- **Treat underlying cause**
- **Anti-emetic:** Cyclizine (vestibular component)

**SPECIFIC SCENARIOS:**

**Inoperable malignant bowel obstruction:**
- **Hyoscine butylbromide** 20-60 mg SC/24h (reduce colic)
- **Octreotide** 50-100 mcg SC TDS (reduce secretions, vomiting)
- **Levomepromazine** 6.25-25 mg SC/24h (anti-emetic, sedative)
- **Dexamethasone** 8-16 mg daily (reduce tumour oedema)
- **Consider:** venting percutaneous gastrostomy if isolated gastric obstruction

**Nausea and vomiting at the end of life:**
- **Levomepromazine** 6.25-25 mg SC/24h (anti-emetic, sedative)
- **Hyoscine butylbromide** 20-60 mg SC/24h (reduce secretions)
- **Midazolam** 10-20 mg SC/24h (reduce distress, agitation)
- **Consider:** syringe driver (CSCI - continuous subcutaneous infusion)

**NON-PHARMACOLOGICAL:**
- **Small, frequent meals**
- **Avoid strong smells** (cooking, perfumes)
- **Cold or room temperature food** (less odour)
- **Sit upright** after meals (prevent reflux)
- **Oral hygiene** (reduce bad taste)
- **Acupressure (P6)** - limited evidence

**Sources:** Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_constipation(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle constipation"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**CONSTIPATION IN PALLIATIVE CARE**

**DEFINITION:**
- **Infrequent passage of hard stools**
- **Straining**, **incomplete evacuation**, **sense of rectal fullness**
- **Very common** in palliative care (up to 50% of patients)

**CAUSES:**

**1. Drugs (very common):**
- **Opioids** (universal side effect - gi opioid receptor stimulation)
- **Vinca alkaloids** (vincristine, vinblastine)
- **Calcium channel blockers**
- **Iron supplements**
- **Anticholinergics**

**2. Reduced mobility:**
- **Bedbound**, **limited activity**

**3. Decreased oral intake:**
- **Anorexia**, **nausea**, **dysphagia**

**4. Metabolic:**
- **Hypercalcaemia**, **dehydration**, **hypokalaemia**

**5. Structural:**
- **Bowel obstruction** (tumour, adhesions)
- **Colonic stricture** (tumour, radiotherapy)

**ASSESSMENT:**

**History:**
- **Frequency:** when last bowel opened (LBO), usual pattern
- **Consistency:** Bristol Stool Chart (type 1-2 = constipation)
- **Associated symptoms:** abdominal pain, distension, nausea, vomiting
- **Red flags:** complete obstruction, perforation, ischaemia

**Examination:**
- **Abdomen:** distension, masses, tenderness, bowel sounds
- **Rectal examination:** impaction, masses, sphincter tone

**INVESTIGATIONS:**
- **Abdominal X-ray** (if obstruction suspected)
- **CT abdomen** (if obstruction uncertain, or surgical intervention considered)

**MANAGEMENT:**

**1. PREVENTION (cornerstone):**
- **Prescribe laxative** from start of opioids (prophylactic)
- **Encourage fluids** (2-3 L/day if possible)
- **Encourage mobility** (within limits)
- **Review medications** ( minimise constipating drugs)

**2. LAXATIVES:**

**Stimulant laxatives (increase peristalsis):**
- **Senna** 2-4 tablets at night (or 15-30 mL syrup)
- **Bisacodyl** 5-10 mg at night (or 10 mg PR)
- **Sodium picosulfate** 5-10 mg at night
- **Onset:** 6-12 hours
- **Side effects:** abdominal cramping

**Osmotic laxatives (retain water in stool):**
- **Lactulose** 10-20 mL BD (softener + stimulant)
- **Macrogol (Movicol, Laxido)** 1-2 sachets daily (dose can be titrated up to 8 sachets/day)
- **Onset:** 24-48 hours
- **Side effects:** bloating, flatulence

**Softener/lubricant:**
- **Docusate** 100-200 mg BD
- **Liquid paraffin** (rarely used - lipoid pneumonia risk)

**Combination products:**
- **Co-danthramer** (stimulant + softener)
- **Co-danthrusate** (stimulant + softener)

**Rectal measures (if oral ineffective, or acute impaction):**
- **Phosphate enema** (rectum only)
- **Arachis oil enema** (softener - left overnight)
- **Manual evacuation** (if faecal impaction)

**3. SPECIFIC SCENARIOS:**

**Opioid-induced constipation:**
- **Prophylaxis:** prescribe laxative from start
- **First line:** Senna 2 tablets at night ± Lactulose 10-15 mL BD
- **Alternative:** Macrogol 1-2 sachets daily (titrate)
- **Refractory:** consider **Methylnaltrexone** or **Naloxegol** (peripherally acting mu-opioid receptor antagonists) - specialist only

**Spinal cord compression (cauda equina syndrome):**
- **Bowel management programme:** digital stimulation, suppositories, manual evacuation
- **Laxatives:** Macrogol (adjust dose to achieve daily bowel movement)
- **Enemas/suppositories:** not if rectal sensation absent (risk of autonomic dysreflexia)

**Bowel obstruction (inoperable):**
- **Treat cause** if possible (surgery, stent)
- **Reduce secretions:** Octreotide 50-100 mcg SC TDS
- **Reduce colic:** Hyoscine butylbromide 20-60 mg SC/24h
- **Anti-emetic:** Levomepromazine 6.25-25 mg SC/24h
- **Consider:** venting percutaneous gastrostomy if isolated gastric obstruction

**Constipation at the end of life:**
- **Reduce oral intake** (less stool)
- **Continue laxative** (if needed)
- **Focus on comfort** (rectal measures may not be appropriate)

**4. MONITORING:**
- **Bowel chart** (frequency, consistency, laxative use)
- **Abdominal examination** (distension, tenderness)
- **Review regularly** (laxative dose, effectiveness, side effects)

**5. REFERRAL:**
- **Surgical review** (if bowel obstruction suspected, not previously investigated)
- **Specialist palliative care** (if refractory symptoms)

**COMPLICATIONS:**
- **Faecal impaction** (overflow diarrhoea, urinary retention)
- **Bowel obstruction** (complete vs. partial)
- **Bowel perforation** (rare, life-threatening)

**PREVENTION (cornerstone):**
- **Prescribe laxative prophylactically** with opioids
- **Regular review** of bowel function
- **Early intervention** (don't wait for complete obstruction)

**Sources:** NICE CG31, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_dyspnoea(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle dyspnoea/breathlessness"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**DYSPNOEA (BREATHLESSNESS) IN PALLIATIVE CARE**

**DEFINITION:**
- **Subjective sensation** of difficult, uncomfortable breathing
- **"Breathlessness"**, **"shortness of breath"**, **"air hunger"**
- **Very common** in palliative care (up to 70% of patients)

**CAUSES:**

**1. Respiratory (most common):**
- **Pleural effusion:** (malignant most common)
- **Lung tumour:** (primary, metastasis)
- **Lymphangitis carcinomatosa:** (diffuse lung infiltration)
- **Pneumonia:** (infective)
- **Pulmonary embolus:** (DVT)
- **COPD:** (underlying lung disease)

**2. Cardiac:**
- **Heart failure:** (LVF, RVF)
- **Pericardial effusion:** (malignant)
- **Arrhythmia:** (AF)

**3. General:**
- **Anaemia:** (Hb <100 g/L)
- **Deconditioning:** (muscle wasting, reduced mobility)
- **Anxiety:** (panic, fear)
- **Pain:** (reduced chest wall movement)

**ASSESSMENT:**

**History:**
- **Onset:** gradual vs. sudden (acute vs. chronic)
- **Pattern:** continuous vs. episodic, exertional vs. rest
- **Severity:** effect on function, distress
- **Associated symptoms:** chest pain, cough, haemoptysis, fever, ankle swelling
- **Relieving factors:** position (orthopnoea), medications

**Examination:**
- **Observations:** SpO2, respiratory rate, heart rate, BP, temperature
- **Respiratory examination:** chest expansion, percussion, auscultation (breath sounds, added sounds)
- **Cardiovascular examination:** heart sounds, murmurs, ankle oedema
- **General:** pallor (anaemia), cachexia (cancer)

**INVESTIGATIONS:**
- **CXR** (pleural effusion, tumour, consolidation)
- **CT chest** (if CXR diagnostic uncertainty, or surgical intervention considered)
- **ABG** (if hypoxic, or uncertain diagnosis)
- **ECG** (if cardiac cause suspected)
- **FBC** (anaemia)
- **D-dimer** (if PE suspected)
- **CXR** comparison (if previous available)

**MANAGEMENT:**

**1. Treat underlying cause** (if possible and consistent with goals of care)

**2. Non-pharmacological (first line):**

**Positioning:**
- **Sit upright**, **lean forward** (tripod position)
- **High back chair**, **bed with pillows**

**Cool air:**
- **Open window**, **fan** (airflow on face reduces sensation of breathlessness)

**Relaxation techniques:**
- **Pursed lip breathing** (slow expiration)
- **Diaphragmatic breathing** (reduce accessory muscle use)
- **Distraction** (music, reading)

**Mobility aids:**
- **Walking aids** (reduce energy expenditure)
- **Wheelchair** (for longer distances)

**3. Pharmacological:**

**Oxygen (if hypoxic):**
- **SpO2 <94%** → oxygen 2-4 L/min via nasal cannulae
- **SpO2 94-98%** → no oxygen needed (unless patient finds helpful)
- **SpO2 >98%** → no oxygen (no benefit)

**Opioids (for refractory dyspnoea):**

**Morphine:**
- **Starting dose:** 2.5-5 mg PO/SC every 4 hours PRN (opioid-naïve)
- **Or:** regular low-dose morphine 2.5-5 mg PO/SC 4-hourly
- **Titrate:** to effect (reduce respiratory rate, relieve dyspnoea)
- **Monitoring:** sedation, respiratory rate (watch for respiratory depression - rare at low doses)
- **Mechanism:** reduces respiratory drive, reduces anxiety, reduces preload/afterload

**Fentanyl:**
- **Fentanyl 12-25 mcg SL (buccal)** PRN
- **Rapid onset** (5-10 minutes)
- **Useful:** episodic dyspnoea, breakthrough dyspnoea

**Anxiolytics:**

**Benzodiazepines:**
- **Lorazepam 0.5-1 mg SL/PO** PRN (episodic dyspnoea)
- **Midazolam 2.5-5 mg SC/IV** (severe, persistent dyspnoea)
- **Diazepam 5-10 mg PO** (regular, if frequent anxiety)
- **Mechanism:** reduce anxiety, muscle relaxation
- **Caution:** sedation, respiratory depression (especially with opioids)

**Other:**

**Bronchodilators** (if COPD/asthma):
- **Salbutamol 2.5-5 mg** nebulised (or 100-200 mcg inhaler)
- **Ipratropium 0.5 mg** nebulised (or 20-40 mcg inhaler)
- **Combination:** Salbutamol + Ipratropium nebulised

**Corticosteroids** (if tumour oedema, COPD exacerbation):
- **Dexamethasone 8-16 mg daily**
- **Prednisolone 30-40 mg daily**
- **Onset:** hours to days
- **Mechanism:** reduce tumour oedema, reduce inflammation

**4. SPECIFIC INTERVENTIONS:**

**Pleural effusion:**
- **Thoracentesis:** therapeutic aspiration (relief temporary - days to weeks)
- **Indwelling pleural catheter** (IPC): for recurrent effusions (patient-controlled drainage)
- **Pleurodesis:** talc slurry (via IPC) or talc poudrage (VATS)

**Malignant airway obstruction:**
- **Stent insertion** (bronchoscopic)
- **Brachytherapy** (endobronchial radiotherapy)
- **Laser therapy** (bronchoscopic)
- **Cryotherapy** (bronchoscopic)

**Lymphangitis carcinomatosa:**
- **Dexamethasone** 8-16 mg daily (reduce tumour oedema)
- **Chemotherapy** (if chemosensitive tumour)

**Anaemia:**
- **Blood transfusion** (2-4 units)
- **Erythropoietin** (if chronic, chemotherapy-related)

**5. NON-INVASIVE VENTILATION (NIV):**
- **Consider:** COPD exacerbation (with respiratory acidosis)
- **Palliative:** may be inappropriate (discuss goals of care)

**6. END-STAGE DYSPNOEA:**
- **Opioid:** morphine 5-10 mg SC every 4 hours PRN (or regular)
- **Anxiolytic:** midazolam 2.5-5 mg SC PRN (or regular)
- **Anticholinergic:** hyoscine hydrobromide 0.3-0.6 mg SC (to reduce secretions if "death rattle")
- **Consider:** syringe driver (CSCI) for continuous medication

**NON-PHARMACOLOGICAL (REITERATE):**
- **Positioning** (upright)
- **Cool air** (fan)
- **Relaxation** (breathing exercises)
- **Distraction** (music, reading)

**SUPPORTIVE CARE:**
- **Explanation** (reassurance - not "suffocating")
- **Anxiety management** (relaxation, anxiolytics)
- **Family support** (witnessing breathlessness is distressing)

**COMPLICATIONS:**
- **Hypoxia** (organ dysfunction)
- **Hypercapnia** (respiratory acidosis)
- **Respiratory depression** (opioid toxicity - rare at low doses)

**Sources:** NICE NG145, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_agitation_delirium(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle agitation/delirium"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**AGITATION / DELIRIUM IN PALLIATIVE CARE**

**DEFINITION:**
- **Delirium:** acute fluctuating disturbance in attention, awareness, cognition
- **Agitation:** motor restlessness, verbal or physical aggression
- **Very common** in palliative care (up to 80% of patients in last days of life)

**TERMINAL RESTLESSNESS:**
- Agitated delirium in last days/hours of life
- Distressing for patient and family
- Multiple causes (often multifactorial)

**CAUSES:**

**1. Drugs (very common):**
- **Opioids** (toxicity, especially renal impairment)
- **Anticholinergics** (hyoscine, amitriptyline, haloperidol)
- **Benzodiazepines** (paradoxical agitation, especially if liver impairment)
- **Corticosteroids** (psychosis, agitation)
- **Chemotherapy** (if hepatic/renal impairment)

**2. Metabolic:**
- **Renal failure** (uraemia)
- **Hepatic failure** (hyperammonaemia)
- **Hypercalcaemia**
- **Hyponatraemia**, **hypernatraemia**
- **Hypoglycaemia**, **hyperglycaemia**

**3. Infection:**
- **Urinary tract infection** (UTI)
- **Pneumonia**
- **Sepsis**

**4. Organ failure:**
- **Liver failure** (hepatic encephalopathy)
- **Renal failure** (uraemia)

**5. Hypoxia:**
- **Pleural effusion**
- **Pneumonia**
- **Pulmonary embolus**

**6. Uncontrolled pain:**
- **Severe pain** (especially if unable to communicate)
- **Urinary retention** (bladder distension)
- **Constipation** (faecal impaction)

**7. Psychological/existential:**
- **Anxiety**, **fear**
- **Unresolved issues** (family conflict, spiritual distress)

**ASSESSMENT:**

**History (from family, carers):**
- **Onset:** acute (delirium) vs. chronic (dementia)
- **Fluctuation:** worse at night (sundowning)
- **Symptoms:** confusion, hallucinations, agitation, aggression
- **Recent changes:** medications, dehydration, infection
- **Predisposing factors:** dementia, older age, sensory impairment

**Examination:**
- **Observations:** temperature, RR, HR, BP, SpO2 (infection, hypoxia)
- **Abdomen:** bladder distension (urinary retention), constipation
- **Neurological:** focal signs (stroke, metastasis)
- **Skin:** pressure ulcers, infection

**INVESTIGATIONS:**
- **FBC, U&E** (infection, renal failure, electrolytes)
- **Calcium** (hypercalcaemia)
- **Glucose** (hypoglycaemia, hyperglycaemia)
- **CRP** (infection)
- **Urinalysis** (UTI)
- **CXR** (infection, effusion)
- **ABG** (hypoxia, respiratory failure)

**MANAGEMENT:**

**1. Treat underlying cause** (if possible and consistent with goals of care)
- **Infection:** antibiotics
- **Hypercalcaemia:** rehydration, bisphosphonate
- **Urinary retention:** catheter
- **Constipation:** laxative, enema
- **Pain:** analgesia
- **Hypoxia:** oxygen

**2. Non-pharmacological:**
- **Reorientation** (frequently, calmly)
- **Calm environment** (reduce stimulation)
- **Familiar objects** (photos, music)
- **Presence of family** (reassurance)
- **Adequate lighting** (reduce confusion at night)

**3. Pharmacological (if agitation causing distress, risk of harm):**

**Antipsychotics (first line for delirium):**

**Haloperidol:**
- **Dose:** 0.5-1.5 mg PO/SC/IV BD/TDS (titrate to max 10-20 mg/day)
- **Onset:** 30-60 minutes (PO), 15-30 minutes (SC/IV)
- **Side effects:** extrapyramidal symptoms (EPS), QT prolongation
- **Cautions:** dementia (increased mortality), Parkinson's disease, Lewy body dementia
- **Alternatives:**
  - **Levomepromazine** 6.25-25 mg SC/PO nocte (or BD) - less EPS, more sedating
  - **Olanzapine** 2.5-5 mg PO nocte (or BD) - atypical antipsychotic
  - **Quetiapine** 12.5-25 mg PO nocte (or BD) - atypical antipsychotic

**Benzodiazepines (if alcohol withdrawal, or terminal restlessness):**

**Midazolam:**
- **Dose:** 2.5-5 mg SC/IV PRN (or 5-20 mg SC/24h via CSCI)
- **Indications:** terminal restlessness, severe agitation, myoclonus
- **Onset:** 5-10 minutes (SC/IV)
- **Side effects:** respiratory depression (especially with opioids), sedation
- **Caution:** paradoxical agitation (if liver impairment)

**Lorazepam:**
- **Dose:** 0.5-1 mg SL/PO PRN
- **Indications:** episodic agitation, anxiety
- **Onset:** 15-30 minutes (SL), 30-60 minutes (PO)

**4. SPECIFIC SCENARIOS:**

**Opioid toxicity:**
- **Symptoms:** drowsiness, myoclonus, agitation, hallucinations, respiratory depression
- **Management:**
  - **Reduce opioid dose** by 25-50%
  - **Switch opioid** (especially if renal impairment - morphine to oxycodone or fentanyl)
  - **Consider:** naloxone infusion (specialist only)

**Anticholinergic toxicity:**
- **Symptoms:** agitation, confusion, dry mouth, urinary retention, constipation, mydriasis
- **Management:**
  - **Stop anticholinergic** (hyoscine, amitriptyline, haloperidol, cyclizine)
  - **Use alternative** (e.g., glycopyrronium instead of hyoscine)

**Terminal restlessness (last days/hours of life):**
- **Midazolam** 5-20 mg SC/24h via CSCI (continuous)
- **Levomepromazine** 6.25-25 mg SC/24h via CSCI (add or alternative)
- **Haloperidol** 1.5-3 mg SC/24h via CSCI (if delirium predominant)
- **Anticholinergic:** glycopyrronium 0.2-0.4 mg SC/4-6h (if secretions)

**5. MONITORING:**
- **Sedation score** (level of consciousness)
- **Agitation scale** (distress, risk of harm)
- **Observations** (respiratory rate, oxygen saturation - especially if opioids + benzodiazepines)
- **Side effects** (EPS, sedation, respiratory depression)

**6. FAMILY SUPPORT:**
- **Explanation** (delirium, not dementia)
- **Reassurance** (not "suffering", unaware of surroundings)
- **Presence** (sitting with patient)
- **Involvement** (help with reorientation, familiar objects)

**PROGNOSIS:**
- **Delirium:** usually reversible if cause identified and treated
- **Terminal restlessness:** usually irreversible (last hours/days of life)
- **Persistent delirium:** consider goals of care (artificial nutrition/hydration?)

**ETHICAL CONSIDERATIONS:**
- **Capacity** (fluctuating, decision-specific)
- **Best interests** (treatment decisions)
- **Restraint** (least restrictive, proportionate, necessary)
- **Sedation** (palliative sedation for refractory symptoms - specialist only)

**Sources:** Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_secretions(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle respiratory secretions / death rattle"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**RESPIRATORY SECRETIONS ("DEATH RATTLE")**

**DEFINITION:**
- **Noisy breathing** due to secretions in upper airway (pharynx, trachea)
- **"Death rattle"** - common in last days/hours of life
- **Distressing to family**, usually **NOT distressing to patient** (unconscious)

**CAUSES:**
- **Inability to cough** (weakness, reduced consciousness)
- **Increased secretions** (respiratory infection, pulmonary oedema, aspiration)
- **Impaired swallowing** (reduced consciousness, dysphagia)
- **Positioning** (supine, unable to mobilise secretions)

**ASSESSMENT:**
- **Listen:** noisy breathing (inspiratory, expiratory, both)
- **Observe:** depth and rate of respiration, work of breathing, distress
- **Position:** supine (worsens), upright (improves)
- **Family distress:** very common (family often more distressed than patient)

**MANAGEMENT:**

**1. Positioning (first line):**
- **Sit upright** (30-45 degrees)
- **Lateral position** (side-lying, secretions drain by gravity)
- **Turn regularly** (every 2-4 hours)

**2. Reassurance (family):**
- **Explain:** patient not distressed, unconscious, unaware of secretions
- **Noise:** caused by air moving through secretions, not "suffocating" or "drowning"
- **Normal:** common in last days/hours of life
- **Reassure:** patient comfortable (if pain and agitation controlled)

**3. Anticholinergic (antimuscarinic) medications:**

**Indications:**
- Noisy secretions causing **family distress**
- Noisy secretions with **patient distress** (rare - usually unconscious)
- Anticipatory (if high risk - unconscious, retained secretions)

**Contraindications / cautions:**
- **Delirium** (anticholinergics worsen confusion)
- **Urinary retention** (anticholinergics worsen retention)
- **Glaucoma** (anticholinergics increase intraocular pressure)
- **Tachyarrhythmias** (anticholinergics increase heart rate)

**Anticholinergic options:**

**Hyoscine Hydrobromide (Scopolamine):**
- **Dose:** 0.3-0.6 mg SC/IV every 4-6 hours PRN
- **Or:** 0.6-2.4 mg SC/24h via CSCI (continuous subcutaneous infusion)
- **Onset:** 10-20 minutes (SC/IV)
- **Side effects:** sedation, delirium, tachycardia, urinary retention, mydriasis (worsens glaucoma)
- **Caution:** delirium (may worsen), glaucoma (contraindicated), urinary retention (may worsen)

**Glycopyrronium:**
- **Dose:** 0.2-0.4 mg SC every 4-6 hours PRN
- **Or:** 0.4-1.2 mg SC/24h via CSCI
- **Onset:** 10-20 minutes (SC)
- **Side effects:** fewer CNS side effects than hyoscine (less sedation, less delirium)
- **Advantages:** does NOT cross blood-brain barrier (less delirium)
- **Preferred** if delirium, confusion, or high risk of delirium

**Hyoscine Butylbromide (Buscopan):**
- **Dose:** 20 mg SC every 4-8 hours PRN
- **Or:** 60-120 mg SC/24h via CSCI
- **Onset:** 10-20 minutes (SC)
- **Side effects:** tachycardia, urinary retention, dry mouth
- **Does NOT cross blood-brain barrier** (less CNS side effects)

**4. Suctioning (rarely indicated):**
- **Indications:** if secretions causing respiratory distress, patient conscious
- **Procedure:** oropharyngeal suction (soft catheter, gentle)
- **Caution:** very distressing for patient and family, often ineffective (secretions reform quickly)
- **Avoid** routine suctioning in last hours of life (not beneficial)

**5. Physiotherapy:**
- **Indications:** if secretions causing respiratory distress, patient able to cooperate
- **Techniques:** positioning, percussion, vibration, assisted cough
- **Caution:** distressing for terminally ill patient, often not appropriate in last hours of life

**6. Artificial hydration (controversial):**
- **Dehydration** reduces secretions
- **Hydration** increases secretions (may worsen death rattle)
- **Individualise:** consider patient comfort, family wishes, goals of care
- **Reduce/stop** artificial hydration if secretions causing distress

**ANTICIPATORY PRESCRIBING (for patients at risk):**

**Common in syringe driver (CSCI) in last days of life:**
- **Midazolam** 10-20 mg SC/24h (agitation, anxiety, distress)
- **Antipsychotic** (Haloperidol 1.5-3 mg SC/24h OR Levomepromazine 6.25-25 mg SC/24h) (delirium, nausea, vomiting)
- **Anticholinergic** (Glycopyrronium 0.4-0.8 mg SC/24h OR Hyoscine Hydrobromide 0.6-1.2 mg SC/24h) (secretions)
- **Opioid** (Morphine 10-30 mg SC/24h) (pain, dyspnoea)

**FAMILY SUPPORT (REITERATE):**
- **Explanation:** patient not in distress, unconscious, unaware
- **Noise:** air moving through secretions, not "suffocating" or "drowning"
- **Reassurance:** patient comfortable (if pain and agitation controlled)
- **Presence:** sit with patient, talk to them (hearing last to go)
- **Involvement:** help with positioning, moisten mouth, gentle touch

**COMPLICATIONS:**
- **Family distress** (very common - explanation, reassurance crucial)
- **Delirium** (if anticholinergic used)
- **Urinary retention** (if anticholinergic used)
- **Tachycardia** (if anticholinergic used)

**Sources:** Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_syringe_driver(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle syringe driver / CSCI"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**SYRINGE DRIVER (CSCI - CONTINUOUS SUBCUTANEOUS INFUSION)**

**DEFINITION:**
- **Continuous subcutaneous infusion (CSCI)** of medications
- **Syringe driver** (battery-operated pump) delivers medications at constant rate
- **Used when:** patient unable to take oral medications (vomiting, dysphagia, unconsciousness, severe weakness)

**INDICATIONS:**

**1. Nausea and vomiting:**
- **Intractable nausea/vomiting** (oral medications not tolerated)
- **Bowel obstruction** (oral medications not absorbed)

**2. Severe weakness:**
- **Unable to swallow** safely (dysphagia, reduced consciousness)

**3. Poor control of symptoms with oral medications:**
- **Frequent breakthrough symptoms** (requires PRN medications)
- **Rapid symptom control** needed (continuous infusion provides steady state)

**4. End-of-life care:**
- **Last days of life** (anticipatory prescribing, symptom control)

**COMMON MEDICATIONS (in syringe driver):**

**1. Anti-emetics:**
- **Haloperidol** 1.5-3 mg SC/24h (nausea, vomiting, delirium)
- **Levomepromazine** 6.25-25 mg SC/24h (nausea, vomiting, agitation, sedation)
- **Metoclopramide** 30-60 mg SC/24h (gastric stasis, nausea)
- **Cyclizine** 150 mg SC/24h (vestibular causes of nausea)

**2. Opioids:**
- **Morphine** 10-30 mg SC/24h (pain, dyspnoea) - most common
- **Oxycodone** 10-30 mg SC/24h (renal impairment)
- **Fentanyl** (not commonly used in CSCI - too potent)

**3. Anxiolytics / sedatives:**
- **Midazolam** 5-20 mg SC/24h (agitation, anxiety, dyspnoea, myoclonus)
- **Levomepromazine** (anxiolytic, sedative)

**4. Anticholinergics:**
- **Hyoscine Hydrobromide** 0.6-2.4 mg SC/24h (secretions)
- **Glycopyrronium** 0.4-1.2 mg SC/24h (secretions - less delirium)
- **Hyoscine Butylbromide** 60-120 mg SC/24h (secretions, colic)

**5. Corticosteroids:**
- **Dexamethasone** 4-8 mg SC/24h (nausea, appetite, pain, tumour oedema)

**COMPATIBILITY:**

**CRITICAL:** **Not all medications compatible** in same syringe
- **Check compatibility chart** before mixing
- **Incompatible medications** precipitate (crystals) → block syringe → loss of symptom control

**Common compatible combinations:**
- **Morphine + Midazolam + Haloperidol + Hyoscine Hydrobromide** (compatible)
- **Morphine + Midazolam + Levomepromazine + Glycopyrronium** (compatible)
- **Oxycodone + Midazolam + Haloperidol + Hyoscine Butylbromide** (compatible)

**Common INCOMPATIBLE combinations:**
- **Metoclopramide + Haloperidol** (INCOMPATIBLE)
- **Dexamethasone + many medications** (check compatibility)
- **Cyclizine + many medications** (check compatibility)

**PREPARATION:**

**1. Choose driver:**
- **Graseby MS16A** (older, 1 mm/day = 1 mL/24h)
- **Graseby MS26** (newer, 0.5 mm/h = 0.5 mL/h = 12 mL/24h)
- **CME** (various models)
- **Ambulatory** (portable, battery-operated)

**2. Calculate total dose:**
- **Regular dose × 24 hours** (e.g., Morphine 5 mg SC QDS → 20 mg/24h)
- **Add PRN doses** (if frequent: e.g., 4 PRN doses per day × 5 mg = 20 mg → total 40 mg/24h)
- **Round** to nearest practical dose

**3. Choose syringe size:**
- **10 mL syringe** (small volumes, 24-hour duration)
- **20 mL syringe** (larger volumes, 24-48 hour duration)
- **30 mL syringe** (large volumes, 48-72 hour duration)
- **Volume:** typically 10-20 mL (avoid >20 mL if possible - tissue irritation)

**4. Choose diluent:**
- **Water for injection (WFI)** (most medications)
- **Sodium chloride 0.9%** (some medications)
- **Check compatibility** (some medications require specific diluent)

**5. Prepare syringe:**
- **Draw up medications** in correct order (some medications absorb into plastic)
- **Dilute to appropriate volume** (10-20 mL typically)
- **Label clearly:** patient name, medications, doses, date, time, rate, signature

**6. Set rate:**
- **Calculate:** volume / duration (mL/24h)
- **Set driver:** to correct rate (mm/day or mm/h depending on driver)

**ADMINISTRATION:**

**1. Choose site:**
- **Subcutaneous** (not intramuscular, not intravenous)
- **Abdomen** (away from waistline, scars, irradiated areas)
- **Thigh** (anterior or lateral)
- **Upper arm** (deltoid region)
- **Buttock** (upper outer quadrant)

**2. Insert needle:**
- **Butterfly needle** (21G or 23G) or **gripper needle**
- **Site preparation** (alcohol swab)
- **Insert** at 45-degree angle
- **Secure** (transparent dressing)

**3. Connect driver:**
- **Prime** tubing (remove air)
- **Connect** to needle
- **Start** driver
- **Check:** infusion running, site not swollen, no leakage

**4. Documentation:**
- **Medication chart:** record medications, doses, rate, site
- **Flow sheet:** record site checked, observations, PRN medications

**MONITORING:**

**Site checks (every 4-6 hours):**
- **Inspect:** erythema, swelling, induration, leakage
- **Palpate:** tenderness, hardness
- **Action:** rotate site if problems (every 24-48 hours routinely)

**Observations:**
- **Sedation score** (level of consciousness)
- **Pain score** (effectiveness)
- **Respiratory rate** (opioid toxicity)
- **Symptom control** (breakthrough PRN required?)

**Troubleshooting:**
- **Noisy breathing:** anticholinergic (hyoscine, glycopyrronium)
- **Agitation:** increase midazolam, consider antipsychotic
- **Pain:** increase opioid
- **Nausea:** add/increase anti-emetic
- **Dyspnoea:** increase opioid, add midazolam

**DISCONTINUING:**
- **Oral intake resumes:** stop CSCI, convert to oral medications
- **Death:** stop CSCI (no longer needed)
- **Change of route:** convert to oral, PRN SC

**Sources:** Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_anticipatory_prescribing(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle anticipatory prescribing"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**ANTICIPATORY PRESCRIBING IN PALLIATIVE CARE**

**DEFINITION:**
- **Pre-prescribing medications** for anticipated symptoms at end of life
- **"Just in case" medications** (JIC) or **"anticipatory" medications**
- **Ensures rapid symptom control** when needed (no delays obtaining medications)

**INDICATIONS:**

**1. Patients in last days/weeks of life:**
- **Advanced life-limiting illness**
- **Deteriorating** (clinically assessed to be in last weeks of life)
- **Risk of:** pain, nausea/vomiting, agitation, dyspnoea, secretions

**2. Patients at risk of specific symptoms:**
- **Severe pain:** strong opioid prescribed
- **Nausea/vomiting:** anti-emetic prescribed
- **Agitation/delirium:** antipsychotic prescribed
- **Respiratory secretions:** anticholinergic prescribed

**3. Patients unable to take oral medications:**
- **Dysphagia**, **severe nausea**, **unconsciousness**, **severe weakness**
- **Syringe driver set up** (or PRN SC medications prescribed)

**COMMONLY PRESCRIBED MEDICATIONS:**

**1. Opioid (for pain, dyspnoea):**
- **Morphine:** 10-20 mg SC every 4 hours PRN (or 10-30 mg SC/24h via CSCI)
- **Or:** Oxycodone (if renal impairment) 5-10 mg SC every 4 hours PRN
- **Indications:** pain, dyspnoea, cough

**2. Anti-emetic (for nausea, vomiting):**
- **Haloperidol:** 1.5-3 mg SC every 4 hours PRN (or 1.5-3 mg SC/24h via CSCI)
- **Or:** Levomepromazine (if sedation desired) 6.25-25 mg SC every 4-8 hours PRN
- **Indications:** nausea, vomiting (especially opioid-induced, gastric stasis)

**3. Antipsychotic (for agitation, delirium):**
- **Haloperidol:** (as above)
- **Or:** Levomepromazine 6.25-25 mg SC every 4-8 hours PRN
- **Indications:** agitation, confusion, hallucinations, delirium

**4. Anxiolytic/sedative (for anxiety, agitation, dyspnoea):**
- **Midazolam:** 2.5-5 mg SC every 4 hours PRN (or 5-20 mg SC/24h via CSCI)
- **Indications:** anxiety, agitation, dyspnoea, myoclonus

**5. Anticholinergic (for respiratory secretions):**
- **Hyoscine Hydrobromide:** 0.3-0.6 mg SC every 4 hours PRN (or 0.6-2.4 mg SC/24h via CSCI)
- **Or:** Glycopyrronium 0.2 mg SC every 4-6 hours PRN (preferred if delirium risk)
- **Indications:** noisy breathing, respiratory secretions ("death rattle")

**6. Other (specific indications):**
- **Cyclizine:** 50 mg SC TDS (vestibular nausea, motion sickness)
- **Metoclopramide:** 10 mg SC TDS (gastric stasis)
- **Dexamethasone:** 4-8 mg SC/PO BD (nausea, appetite, pain, tumour oedema)

**PRESCRIBING CONSIDERATIONS:**

**1. Choose appropriate medications:**
- **Based on:** individual patient needs (not all patients need all medications)
- **Avoid:** unnecessary medications (polypharmacy)

**2. Choose appropriate doses:**
- **Start low:** titrate to effect
- **PRN doses:** typically 1/6th of total daily dose (for opioids)
- **Maximum doses:** specify if needed (prevent overdose)

**3. Choose appropriate route:**
- **SC (subcutaneous):** most common (patient unable to take oral)
- **PO (oral):** if patient can swallow safely
- **PR (rectal):** rarely used (diazepam, diclofenac)
- **CSCI (continuous subcutaneous infusion):** if frequent PRN doses required

**4. Specify duration:**
- **End of life:** "until death" or "until further review"
- **Reversible cause:** "until review" (e.g., 3-7 days)

**5. Specify maximum:**
- **PRN doses:** specify frequency (e.g., "every 4 hours PRN")
- **Maximum dose:** if appropriate (e.g., "maximum 60 mg/24h")

**6. Provide clear instructions:**
- **Administration:** SC (not IM, not IV)
- **Site:** abdomen, thigh, upper arm
- **Technique:** rotate sites
- **Documentation:** record PRN doses given

**COMMUNICATION:**

**1. Explain to patient (if appropriate):**
- **Why prescribed:** anticipate symptoms, rapid control
- **What to expect:** medications given if symptoms occur
- **Goals:** comfort, dignity, symptom control

**2. Explain to family/carers:**
- **What prescribed:** anticipatory medications ("just in case")
- **Why:** ensure rapid symptom control, no delays
- **How given:** SC injection (not oral)
- **What to expect:** nurse will administer if needed
- **Reassurance:** medications for comfort, not to hasten death

**3. Ensure availability:**
- **Medications available:** in home, care home, hospice
- **Nurses aware:** how to administer, when to administer
- **Documentation clear:** medication chart, care plan

**MONITORING AND REVIEW:**

**1. Regular review:**
- **Daily review** (inpatient)
- **Weekly review** (community)
- **Assess:** need for anticipatory medications, doses, routes

**2. Adjust as needed:**
- **Increase dose** if symptoms poorly controlled
- **Add medications** if new symptoms emerge
- **Stop medications** if no longer needed (e.g., recovery)

**3. Re-prescribe:**
- **Expiry:** typically 6 months (check local policy)
- **Supply:** ensure medications not expired

**ETHICAL CONSIDERATIONS:**

**1. Goals of care:**
- **Symptom control:** primary goal (comfort, dignity)
- **NOT to hasten death:** medications for symptom control, not euthanasia
- **NOT to prolong dying:** medications for comfort, not prolonging dying process

**2. Communication:**
- **Transparent:** explain purpose, expected effect
- **Reassurance:** not "overdosing", appropriate symptom control
- **Address concerns:** family concerns about hastening death

**3. Documentation:**
- **Clear:** goals of care, indications, doses, routes
- **Shared:** with patient (if appropriate), family, healthcare team

**Sources:** NICE NG31, Association for Palliative Medicine, EAPC Guidelines"""
        )

    def _handle_advance_care_planning(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle advance care planning"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**ADVANCE CARE PLANNING (ACP) IN PALLIATIVE CARE**

**DEFINITION:**
- **Voluntary process** of discussion between patient, family, healthcare professionals
- **Documents:** patient's preferences, wishes, priorities for future care
- **Goal:** ensure care aligns with patient's values and preferences

**COMPONENTS:**

**1. Advance Decision to Refuse Treatment (ADRT):**
- **Legally binding** (in England and Wales) if strict criteria met
- **Specific refusal** of specific treatment (not "refusal of all treatment")
- **Can refuse:** life-sustaining treatment (e.g., ventilation, dialysis, CPR)
- **Cannot refuse:** basic care (food, water, pain relief, warmth)
- **Can withdraw:** at any time (while has capacity)

**2. Advance Statement (preferences):**
- **Not legally binding** but must be considered
- **Documents:** preferences, wishes, values
- **Examples:** wish to die at home, wish to avoid hospital admission, wish to be visited by chaplain

**3. DNACPR (Do Not Attempt Cardiopulmonary Resuscitation):**
- **Specific decision** about CPR in event of cardiac arrest
- **NOT** "do not treat" or "withdraw treatment"
- **Separate** from other treatment decisions
- **Legally binding** (if completed correctly)

**4. Lasting Power of Attorney (LPA):**
- **Property and affairs LPA:** appoints attorney to make financial decisions
- **Health and welfare LPA:** appoints attorney to make health and welfare decisions
- **Attorney** can make decisions when patient loses capacity

**5. Preferred Priorities for Care (PPC):**
- **Document** summarising patient's preferences, priorities for care
- **Focus:** what matters to patient (e.g., wish to die at home)
- **Portable:** travels with patient (home, hospital, care home)

**ADVANCE DECISION TO REFUSE TREATMENT (ADRT):**

**Criteria for legally binding:**
1. **Patient ≥18 years old** and has capacity
2. **Clearly specifies** treatment being refused
3. **Clearly specifies** circumstances in which refusal applies
4. **In writing** (signed, witnessed)
5. **Made voluntarily** (not under duress)
6. **Informed** (patient understands consequences)

**What CAN be refused:**
- **CPR** (cardiopulmonary resuscitation)
- **Ventilation** (invasive or non-invasive)
- **Dialysis** (renal replacement therapy)
- **Artificial nutrition and hydration** (if specific circumstances)
- **Antibiotics** (if specific circumstances)
- **Hospital admission** (if specific circumstances)

**What CANNOT be refused:**
- **Basic care** (food, water by mouth, pain relief, warmth)
- **Action** to keep patient comfortable (palliative care)

**Withdrawing ADRT:**
- **Can withdraw** at any time (while has capacity)
- **Can destroy** ADRT
- **Inform healthcare professionals** (GP, hospital)

**DNACPR (Do Not Attempt Cardiopulmonary Resuscitation):**

**Indications:**
- **CPR would not restart heart and breathing** (futile)
- **CPR would not provide overall benefit** (burdens outweigh benefits)
- **Patient does not want CPR** (for any reason)

**Decision-making:**
- **Clinician-led** decision (not patient alone, not family alone)
- **Based on:** clinical judgement, patient's wishes, best interests
- **Discussion:** with patient (if possible), with family (if appropriate)

**Documentation:**
- **DNACPR form** (specific form for locality)
- **Record:** decision, reasons, discussion with patient/family, date, signature
- **Review:** no set time (review if clinical situation changes)

**Scope:**
- **Specific to CPR** (only)
- **NOT** "do not treat" or "withdraw treatment"
- **All other treatment decisions** based on clinical judgement, patient's wishes

**DISCUSSING ACP:**

**Timing:**
- **Early** (before loss of capacity)
- **When patient is stable** (not during emergency, not acutely unwell)
- **Gradual** (multiple discussions over time)

**Setting:**
- **Quiet, private** environment
- **Adequate time** (not rushed)
- **Support person present** (family member, friend) if patient wishes

**Approach:**
- **Ask open questions:** "What matters most to you?", "What are your hopes and fears?"
- **Explore values:** "What makes life worth living for you?", "What would make life not worth living?"
- **Discuss scenarios:** "If you became very unwell and couldn't communicate, what would you want?"
- **Listen actively:** allow silence, acknowledge emotions

**Topics to discuss:**
- **Priorities:** what matters most (e.g., being at home, being comfortable, seeing family)
- **Fears:** what are you most afraid of (e.g., pain, being alone, being a burden)
- **Preferences:** where would you want to be cared for (home, hospital, hospice)
- **Treatment goals:** prolong life at all costs vs. comfort-focused
- **Specific treatments:** CPR, ventilation, hospital admission

**COMMUNICATION WITH FAMILY:**

**Important:** (with patient's permission)
- **Family involved** (if patient wishes)
- **Family understands** patient's wishes
- **Family prepared** for patient's death

**Without patient permission:**
- **Discuss generally** (not specifics)
- **Explain principles** (best interests, comfort)
- **Listen to concerns** (family often anxious, protective)

**DOCUMENTATION:**

**Record clearly:**
- **Patient's preferences, wishes, priorities**
- **Specific decisions** (ADRT, DNACPR)
- **Discussion** (who involved, what discussed)
- **Date, signature** (patient, healthcare professional)

**Share:**
- **With patient** (provide copy)
- **With GP** (primary care record)
- **With family** (if patient wishes)
- **With hospital** (if admitted)
- **With care home** (if resident)

**REVIEW:**

**Regular review:**
- **Review** if clinical situation changes
- **Review** if patient changes mind
- **Review** if new treatment options emerge

**Initiating ACP:**
- **Any healthcare professional** can initiate ACP discussion
- **Refer to specialist palliative care** if complex decisions, uncertainty

**ETHICAL CONSIDERATIONS:**

**Respect for autonomy:**
- **Patient's right** to make decisions about their care
- **Respect patient's wishes** (even if healthcare professionals disagree)

**Best interests:**
- **If patient lacks capacity** and no ADRT: decisions made in best interests
- **Consider:** patient's previously expressed wishes, values, preferences

**Beneficence vs. non-maleficence:**
- **Beneficence:** act in patient's best interests
- **Non-maleficence:** do no harm (avoid futile, burdensome treatment)

**Sources:** NICE NG142, GMC Guidelines, BMA Guidance"""
        )

    def _handle_breaking_bad_news(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle breaking bad news / prognosis"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**BREAKING BAD NEWS & PROGNOSTICATION**

**BREAKING BAD NEWS (SPIKES PROTOCOL):**

**S - Setting:**
- **Private, quiet** environment (not corridor, not over telephone if possible)
- **Sit down** (at same level as patient)
- **Adequate time** (allow for questions, emotions)
- **Support person** present (family member, friend) if patient wishes
- **Tissues** available
- **Turn off pager/mobile** (avoid interruptions)

**P - Perception:**
- **Assess patient's understanding:** "What have you been told about your condition?"
- **Assess expectations:** "What were you expecting from today's appointment?"
- **Identify misconceptions:** correct gently later

**I - Invitation:**
- **Ask permission:** "How would you like to receive information? In detail or summary?"
- **Ask:** "How much information would you like?"
- **Respect wishes:** some patients want all details, some want minimal information

**K - Knowledge:**
- **Give warning:** "I'm afraid the news is not good."
- **Give information** in small chunks
- **Avoid jargon:** use plain language
- **Check understanding:** "Does that make sense?"
- **Allow silence:** give patient time to process information

**E - Emotions:**
- **Acknowledge emotions:** "I can see this is difficult news."
- **Validate emotions:** normal to be sad, angry, shocked
- **Allow tears:** don't rush to stop patient crying
- **Respond to emotions:** "I can see how upsetting this is for you."
- **Use NURS:**
  - **N**aming: "I can see you're angry."
  - **U**nderstanding: "It's understandable to feel angry."
  - **R**especting: "Your feelings are important."
  - **S**upporting: "I'm here to support you."

**S - Strategy/Summary:**
- **Summarise:** "So we've discussed..."
- **Make a plan:** "The next step is..."
- **Arrange follow-up:** "I'll see you again in..."
- **Written information:** provide leaflets, website
- **Involve family:** if patient wishes

**PROGNOSTICATION:**

**Discussing prognosis:**
- **Honest but hopeful:** balance realism with hope
- **Range not exact:** "weeks to months" not "6 weeks"
- **Uncertainty acknowledged:** "Everyone is different," "hard to predict exactly"
- **Focus on quality of life:** not just length of life

**Answering questions:**
- **"How long have I got?"**
  - **General answer:** "weeks to months" or "months to years"
  - **Explain:** uncertainty, individual variation
  - **Focus:** "What would you like to achieve in this time?"

**Prognostic indicators:**
- **Performance status:** (WHO/ECOG score)
- **Weight loss:** (cachexia)
- **Symptom burden:** (pain, dyspnoea, fatigue)
- **Biochemical markers:** (CRP, albumin, LDH)
- **Disease burden:** (metastasis, tumour burden)
- **Rate of progression:** (deterioration over recent weeks)

**Surprise question:**
- **"Would I be surprised if this patient died within the next 6-12 months?"**
- **Useful trigger** to identify patients for palliative care referral
- **Helps identify** patients who may benefit from ACP discussions

**GOALS OF CARE DISCUSSIONS:**

**Timing:**
- **Early** (before crisis)
- **When patient stable** (not during emergency, not acutely unwell)
- **Gradual** (multiple discussions over time)

**Topics to discuss:**
- **Understanding of illness:** "What is your understanding of your condition?"
- **Priorities:** "What matters most to you?"
- **Fears:** "What are you most afraid of?"
- **Expectations:** "What are you hoping for?"
- **Trade-offs:** "What would you be willing to go through for the possibility of more time?"

**Goals of care:**
- **Life-prolonging:** (e.g., ICU admission, ventilation, dialysis)
- **Life-sustaining:** (e.g., hospital admission, antibiotics)
- **Comfort-focused:** (e.g., symptom control, avoid hospital)

**DOCUMENTATION:**
- **Record:** discussions, decisions, patient's wishes
- **Share:** with healthcare team (GP, hospital, community nurses)
- **Review:** if clinical situation changes, if patient changes mind

**COMMUNICATION CHALLENGES:**

**Denial:**
- **Acknowledge:** "I know this is difficult to take in."
- **Gentle persistence:** repeat information over multiple consultations
- **Involve family:** (if patient wishes)

**Anger:**
- **Acknowledge:** "I can see you're angry."
- **Validate:** "It's understandable to feel angry."
- **Don't take personally:** anger at situation, not you

**Collusion:**
- **Family ask to withhold information:** "Don't tell him he has cancer."
- **Explore:** "Why do you feel this way?"
- **Explain:** "Most patients prefer to know." "Secrets are difficult to maintain."
- **Negotiate:** "How much information do you think he would want?"
- **Respect patient autonomy:** ultimately, patient has right to know

**Silence:**
- **Allow silence:** give patient time to process
- **Don't fill silence:** wait for patient to speak
- **Observe:** patient's body language, emotions

**Crying:**
- **Allow tears:** don't rush to stop patient crying
- **Offer tissues:** practical support
- **Acknowledge:** "I can see how upsetting this is."
- **Don't say:** "Don't cry," "It'll be okay." (dismissive)

**HOPE:**

**Balance honesty with hope:**
- **Realistic hope:** "Hope for the best, prepare for the worst."
- **Reframe hope:** hope for quality of life, hope for peaceful death
- **Avoid false hope:** "You'll be fine," "There's a good chance of cure" (if not true)

**Maintain hope:**
- **Focus on:** what can be done (symptom control, quality of life)
- **Avoid:** "There's nothing more we can do." (instead: "There's no more curative treatment, but there's a lot we can do to keep you comfortable")

**Sources:** SPIKES Protocol, NICE NG161, GMC Guidelines"""
        )

    def _handle_general_palliative_care(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general palliative care query"""
        return DomainQueryResult(
            domain_name="palliative_care",
            answer="""**PALLIATIVE CARE - General Consultation**

Palliative care is an approach that improves the quality of life of patients and their families facing the problems associated with life-threatening illness.

**PRINCIPLES:**
- **Affirms life** and regards dying as a normal process
- **Neither hastens nor postpones death**
- **Provides relief** from pain and other distressing symptoms
- **Integrates psychological and spiritual aspects of care
- **Offers support** to help patients live as actively as possible until death
- **Offers support** to help the family cope during the patient's illness and bereavement

**WHEN TO REFER TO PALLIATIVE CARE:**

**Triggers for referral:**
- **Advanced cancer:** (metastatic, progressive)
- **End-stage organ failure:** (heart failure, COPD, renal failure)
- **Progressive neurological disease:** (MND, Parkinson's, MS)
- **Uncontrolled symptoms:** (pain, nausea, dyspnoea, agitation)
- **Complex needs:** (psychosocial, spiritual, ethical)
- **End of life:** (last days/weeks of life)

**EARLY referral** (months before death) is better than late referral:
- Allows relationship building
- Allows symptom optimisation
- Allows advance care planning
- Improves quality of life
- May improve survival (some evidence)

**PALLIATIVE CARE EMERGENCIES:**

**Medical emergencies (treat if consistent with goals of care):**
- **Spinal cord compression** (back pain + neurological symptoms)
- **Hypercalcaemia** (confusion, drowsiness, dehydration)
- **SVC obstruction** (facial swelling, dyspnoea)
- **Airway obstruction** (stridor, respiratory distress)
- **Massive haemorrhage** (coughing up blood, bleeding)
- **Status epilepticus** (seizures)

**SYMPTOM MANAGEMENT:**

**Common symptoms:**
- **Pain** (70-90%)
- **Nausea/vomiting** (40-70%)
- **Constipation** (30-50%)
- **Dyspnoea** (50-70%)
- **Fatigue** (80-90%)
- **Anxiety/depression** (20-50%)
- **Delirium/confusion** (up to 80% in last days)

**END OF LIFE CARE:**

**Last days of life:**
- **Recognise dying:** (deteriorating day by day, reduced oral intake, reduced consciousness)
- **Communicate:** with patient (if possible), family, healthcare team
- **Prescribe anticipatory medications:** (opioid, anti-emetic, anxiolytic, anticholinergic)
- **Assess and manage symptoms:** (pain, agitation, dyspnoea, secretions)
- **Support family:** (reassurance, explanation, presence)

**Recognition of dying:**
- **Deteriorating day by day**
- **Reduced oral intake** (little or no food/fluid)
- **Reduced consciousness** (drowsy, unconscious)
- **Cheyne-Stokes breathing** (irregular breathing pattern)
- **Peripheral cyanosis** (mottled extremities)
- **Unable to swallow** medications

**MANAGEMENT IN LAST DAYS OF LIFE:**

**Medications (CSCI or PRN SC):**
- **Opioid:** morphine 10-30 mg SC/24h (pain, dyspnoea)
- **Anti-emetic:** haloperidol 1.5-3 mg SC/24h OR levomepromazine 6.25-25 mg SC/24h
- **Anxiolytic:** midazolam 5-20 mg SC/24h (agitation, anxiety, dyspnoea)
- **Anticholinergic:** hyoscine hydrobromide 0.6-2.4 mg SC/24h OR glycopyrronium 0.4-1.2 mg SC/24h

**Hydration:**
- **Assess individually:** (no "one size fits all")
- **Consider:** benefits vs. burdens
- **Discuss:** with patient (if possible), family
- **Review regularly:** (if continuing)

**Family support:**
- **Explain:** what is happening, what to expect
- **Reassure:** patient comfortable (not in pain, not suffering)
- **Encourage:** presence, talking to patient (hearing last to go)
- **Support:** practical, emotional, spiritual

**BEREAVEMENT:**

**Immediate:**
- **Attend to deceased:** (last offices)
- **Support family:** (listen, acknowledge emotions)
- **Provide information:** (what happens next, registration of death, funeral)

**Follow-up:**
- **Contact family** (within 1-2 weeks)
- **Offer bereavement support** (counselling, support groups)
- **Recognise complicated grief** (persistent, disabling grief)

**ETHICAL ISSUES:**

**Capacity:**
- **Assess capacity** (specific decision, specific time)
- **Act in best interests** (if lacks capacity)
- **Respect autonomy** (if has capacity)

**Artificial nutrition/hydration:**
- **Consider:** benefits vs. burdens
- **Discuss:** with patient, family
- **Individualise:** (no blanket policy)

**Sedation:**
- **Palliative sedation** (refractory symptoms)
- **Goal:** symptom relief (not euthanasia)
- **Specialist only** (complex decision-making)

**Sources:** NICE NG31, WHO Definition of Palliative Care, Association for Palliative Medicine"""
        )


def create_palliative_care_domain():
    """Factory function to create palliative care domain"""
    return PalliativeCareDomain()
