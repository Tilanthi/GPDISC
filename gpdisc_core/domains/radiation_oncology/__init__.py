"""
Radiation Oncology Domain for GPDISC

Comprehensive radiation oncology domain covering radiotherapy treatment
planning, delivery, side effect management, and cancer care.

Evidence-based: ASTRO (American Society for Radiation Oncology), ESTRO,
NICE Guidelines, NHS England Cancer Guidelines
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class RadiationOncologyDomain(BaseDomainModule):
    """
    Radiation Oncology Domain

    Covers all aspects of radiation oncology including:
    - Radiotherapy treatment planning
    - External beam radiotherapy (EBRT)
    - Brachytherapy
    - Stereotactic radiosurgery (SRS)
    - Stereotactic body radiotherapy (SBRT)
    - Side effect management
    - Palliative radiotherapy
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="radiation_oncology",
            version="1.0.0",
            dependencies=[],
            description="Radiation oncology - Radiotherapy treatment planning, delivery, side effect management",
            keywords=[
                # Radiotherapy
                "radiotherapy", "radiation therapy", "radiation", "rt", "ebrt",
                "external beam radiotherapy", "brachytherapy", "internal radiotherapy",
                "stereotactic radiosurgery", "srs", "gamma knife", "cyberknife",
                "stereotactic body radiotherapy", "sbrt", "sabr",
                "palliative radiotherapy", "curative radiotherapy",
                # Side effects
                "radiation side effects", "radiation toxicity", "radiation burn",
                "mucositis", "xerostomia", "dry mouth", "dysphagia", "oesophagitis",
                "radiation pneumonitis", "radiation enteritis", "proctitis",
                "radiation cystitis", "skin reaction", "desquamation",
                # Cancer types
                "breast cancer radiotherapy", "prostate cancer radiotherapy",
                "lung cancer radiotherapy", "brain tumour radiotherapy",
                "head and neck cancer radiotherapy", "rectal cancer radiotherapy",
                "cervical cancer radiotherapy",
                # Treatment planning
                "radiotherapy planning", "simulation", "ct simulation",
                "radiotherapy dose", "radiotherapy fractions",
                "imrt", "vmat", "igrt", "3dcrt",
                "radiotherapy mask", "immobilisation"
            ],
            capabilities=[
                "radiotherapy_consultation", "side_effect_management",
                "palliative_radiotherapy_guidance", "treatment_planning_guidance",
                "radiotherapy_consent", "radiotherapy_techniques"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        query_lower = query.lower()

        # EMERGENCY: Radiation oncology emergencies
        if any(term in query_lower for term in ["spinal cord compression", "cord compression",
                                                   "cauda equina syndrome", "malignant spinal cord compression"]):
            return self._handle_spinal_cord_compression(query, context)

        # EMERGENCY: Superior vena cava obstruction
        if any(term in query_lower for term in ["svco", "superior vena cava obstruction",
                                                   "superior vena cava syndrome", "svco obstruction"]):
            return self._handle_svco(query, context)

        # EMERGENCY: Acute radiation toxicity
        if any(term in query_lower for term in ["acute radiation toxicity", "radiation emergency",
                                                   "severe radiation reaction", "radiation pneumonitis emergency"]):
            return self._handle_acute_radiation_toxicity(query, context)

        # PALLIATIVE RADIOTHERAPY (bone metastases, brain metastases)
        if any(term in query_lower for term in ["bone metastases radiotherapy", "bone mets",
                                                   "palliative radiotherapy", "brain metastases radiotherapy",
                                                   "brain mets radiotherapy"]):
            return self._handle_palliative_radiotherapy(query, context)

        # BREAST CANCER RADIOTHERAPY
        if any(term in query_lower for term in ["breast cancer radiotherapy", "breast radiotherapy",
                                                   "post-mastectomy radiotherapy", "breast conservation"]):
            return self._handle_breast_radiotherapy(query, context)

        # PROSTATE CANCER RADIOTHERAPY
        if any(term in query_lower for term in ["prostate cancer radiotherapy", "prostate radiotherapy",
                                                   "prostate brachytherapy", "seed implantation"]):
            return self._handle_prostate_radiotherapy(query, context)

        # LUNG CANCER RADIOTHERAPY
        if any(term in query_lower for term in ["lung cancer radiotherapy", "nsclc radiotherapy",
                                                   "sbrt lung", "sabrt lung", "radical radiotherapy lung"]):
            return self._handle_lung_radiotherapy(query, context)

        # HEAD AND NECK CANCER RADIOTHERAPY
        if any(term in query_lower for term in ["head and neck cancer radiotherapy", "oropharyngeal radiotherapy",
                                                   "laryngeal radiotherapy", "nasopharyngeal radiotherapy"]):
            return self._handle_head_neck_radiotherapy(query, context)

        # RADIATION SIDE EFFECTS
        if any(term in query_lower for term in ["radiation side effects", "radiation toxicity",
                                                   "radiation skin reaction", "xerostomia", "mucositis",
                                                   "radiation pneumonitis", "radiation cystitis"]):
            return self._handle_radiation_side_effects(query, context)

        # BRACHYTHERAPY
        if any(term in query_lower for term in ["brachytherapy", "internal radiotherapy",
                                                   "seed implantation", "high dose rate", "hdr"]):
            return self._handle_brachytherapy(query, context)

        # STEREOTACTIC RADIOSURGERY (SRS)
        if any(term in query_lower for term in ["stereotactic radiosurgery", "srs", "gamma knife",
                                                   "cyberknife", "brain radiosurgery"]):
            return self._handle_srs(query, context)

        # GENERAL RADIOTHERAPY
        else:
            return self._handle_general_radiation_oncology(query, context)

    def _handle_spinal_cord_compression(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Malignant spinal cord compression management"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**MALIGNANT SPINAL CORD COMPRESSION (MSCC) - EMERGENCY MANAGEMENT**

**DEFINITION:**
Compression of the spinal cord or cauda equina by metastatic tumour, causing neurological deficit.

**RED FLAGS (HIGH RISK OF MSCC):**
- **Back pain:** Progressive, thoracic region, worsens with lying flat, Valsalva manoeuvre
- **Neurological deficit:** Motor weakness (difficulty walking, ascending weakness), sensory changes (sensory level), sphincter disturbance (urinary retention, constipation), saddle anaesthesia (S2-S5 dermatomes)
- **Previous cancer:** Breast, prostate, lung, renal, myeloma, melanoma
- **Known spinal metastases:** High risk of progression to MSCC

**IMMEDIATE ACTION:**

1. **URGENT MRI WHOLE SPINE** (within 24 hours of presentation)
   - **T1-weighted:** Assess tumour extent, cord compression
   - **T2-weighted:** Assess cord oedema, signal change
   - **STIR:** Assess bone metastases, marrow infiltration

2. **DEXAMETHASONE** (if cord compression confirmed or high suspicion)
   - **High-dose dexamethasone:** 16 mg PO/IV loading dose, then 16 mg PO/IV OD (reduce oedema, improve symptoms)
   - **Rapid taper:** After radiotherapy/surgery completion (taper over 2-3 weeks)
   - **PPI prophylaxis:** Omeprazole 20 mg OD (stress ulcer prophylaxis)

3. **NEUROSURGICAL/ORTHOPAEDIC REFERRAL**
   - **Indications for surgery:** Spinal instability, rapid neurological deterioration, unknown primary, radioresistant tumour
   - **Decision:** Multidisciplinary discussion (oncology, neurosurgery, orthopaedics, radiology)

**TREATMENT:**

**EMERGENCY RADIOTHERAPY:**
- **Indication:** Non-surgical candidates, radiosensitive tumours, multilevel disease
- **Dose:** 20 Gy in 5 fractions (1 week) OR 8 Gy single fraction (palliative)
- **Technique:** EBRT (external beam radiotherapy) with IMRT/VMAT
- **Simulation:** CT simulation with immobilisation (thermoplastic mask for cervical spine, vac-lok for thoracolumbar spine)
- **Target volume:** Gross tumour volume (GTV) + clinical target volume (CTV) margin (usually 1 cm)
- **Organs at risk:** Spinal cord (max dose <45 Gy)

**SURGERY:**
- **Indication:** Spinal instability, rapid neurological deterioration, unknown primary (biopsy), radioresistant tumour (renal cell carcinoma, melanoma, sarcoma)
- **Procedure:** Decompressive surgery (laminectomy, corpectomy) ± spinal stabilisation (instrumentation, cement augmentation)

**MULTIDISCIPLINARY CARE:**
- **Physiotherapy:** Mobilisation, gait assessment, rehabilitation
- **Occupational therapy:** Mobility aids, home assessment, social care
- **Palliative care:** Symptom management, psychosocial support, advance care planning

**PROGNOSIS:**
- **Ambulant pre-treatment:** 80-90% remain ambulant
- **Non-ambulant pre-treatment:** 30-50% regain ambulation
- **Survival:** Median 3-6 months (dependent on primary tumour, performance status)

**Sources:** NICE Guidelines (NG75), BOA Guidelines, SCOPIC Guidelines""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG75)", "BOA Guidelines", "SCOPIC Guidelines"],
                "emergency_protocol": "spinal_cord_compression"
            }
        )

    def _handle_svco(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Superior vena cava obstruction management"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**SUPERIOR VENA CAVA OBSTRUCTION (SVCO) - EMERGENCY MANAGEMENT**

**DEFINITION:**
Obstruction of the superior vena cava (SVC) by tumour (usually lung cancer), causing impaired venous drainage from head, neck, and upper extremities.

**RED FLAGS (SVCO):**
- **Facial oedema:** Facial swelling, plethora (redness)
- **Neck swelling:** Distended neck veins, jugular venous distension
- **Arm oedema:** Bilateral arm swelling (more marked than unilateral)
- **Dyspnoea:** Shortness of breath, orthopnoea
- **Cough:** Persistent cough, haemoptysis
- **Headache:** Worse when lying flat, morning headache
- **Visual disturbance:** Periorbital oedema, facial plethora

**IMMEDIATE ACTION:**

1. **URGENT CT CHEST WITH CONTRAST**
   - **Diagnosis:** Identify SVC obstruction, tumour extent, thrombosis
   - **Alternative:** MRI chest (if contrast contraindicated)
   - **Avoid:** SVC central line insertion (risk of exacerbating obstruction)

2. **EMERGENCY RADIOTHERAPY** (if SVCO due to tumour)
   - **Indication:** SVCO secondary to lung cancer (SCLC, NSCLC), lymphoma
   - **Dose:** 20 Gy in 5 fractions (1 week) OR 8 Gy single fraction (palliative)
   - **Onset of action:** 7-10 days (symptom improvement)
   - **Technique:** EBRT with AP/PA fields or IMRT/VMAT
   - **Target volume:** Mediastinal mass + margin (usually 2 cm)

3. **CHEMOTHERAPY** (if SVCO due to chemo-sensitive tumour)
   - **Indication:** Small cell lung cancer (SCLC), lymphoma, germ cell tumour
   - **Onset of action:** 3-7 days (faster than radiotherapy)
   - **Decision:** Multidisciplinary discussion (oncology, respiratory medicine)

4. **STENT INSERTION** (if rapid relief required)
   - **Indication:** Life-threatening SVCO, chemo-resistant tumour, recurrent SVCO
   - **Procedure:** Endovascular SVC stent insertion (interventional radiology)
   - **Onset of action:** Immediate (symptom relief within 24-48 hours)
   - **Complications:** Stent migration, thrombosis, infection

5. **SYMPTOMATIC MANAGEMENT:**
   - **Elevate head of bed:** 30-45 degrees (reduce facial oedema)
   - **Oxygen:** 15 L/min if hypoxic (SpO2 <94% on room air)
   - **Dexamethasone:** 8 mg PO/IV BD (reduce tumour oedema, improve symptoms)
   - **Diuretics:** Furosemide 40 mg PO/IV OD (reduce fluid overload, symptomatic relief)

6. **THROMBOSIS MANAGEMENT** (if SVCO due to thrombosis)
   - **Anticoagulation:** Low molecular weight heparin (LMWH) (e.g., enoxaparin 1 mg/kg SC BD)
   - **Thrombolysis:** Consider if severe SVCO, recent thrombosis (<14 days)
   - **Thrombectomy:** Surgical or endovascular (rare)

**PROGNOSIS:**
- **Symptom improvement:** 70-80% (radiotherapy, chemotherapy, stenting)
- **Duration of response:** 3-6 months (dependent on tumour type)
- **Survival:** Median 6-12 months (dependent on primary tumour, performance status)

**Sources:** NICE Guidelines, BTS Guidelines, British Society of Interventional Radiology Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "emergency",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines", "BTS Guidelines", "British Society of Interventional Radiology Guidelines"],
                "emergency_protocol": "svco"
            }
        )

    def _handle_acute_radiation_toxicity(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Acute radiation toxicity management"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**ACUTE RADIATION TOXICITY - EMERGENCY MANAGEMENT**

**ACUTE RADIATION SYNDROME (ARS):**
Rare complication of accidental radiation exposure (not radiotherapy). Requires immediate specialist referral.

**RADIOTHERAPY-RELATED EMERGENCIES:**

**1. ACUTE RADIATION PNEUMONITIS:**

**Clinical features (occurs 1-6 months post-radiotherapy):**
- **Dyspnoea:** Progressive shortness of breath
- **Cough:** Dry cough, productive cough (if infection)
- **Fever:** Low-grade fever (infection superimposed)
- **Chest pain:** Pleuritic chest pain
- **Hypoxia:** Desaturation on exertion

**Risk factors:**
- **Total dose:** >30 Gy (higher dose = higher risk)
- **Fraction size:** >2 Gy per fraction (higher fraction size = higher risk)
- **Concurrent chemotherapy:** Taxanes, gemcitabine (increases risk)
- **Pre-existing lung disease:** COPD, pulmonary fibrosis
- **Large treatment volume:** Whole lung irradiation, large PTV

**Investigation:**
- **CXR:** New pulmonary infiltrates within radiation field
- **CT chest:** Ground-glass opacities, consolidation within radiation field
- **Infection exclusion:** Blood cultures, sputum culture, consider bronchoscopy with BAL
- **Pulmonary function tests:** Reduced DLCO, restrictive pattern

**Management:**
- **High-dose corticosteroids:** Prednisolone 1 mg/kg/day (max 60 mg OD) for 4-6 weeks, then slow taper over 6-12 weeks
- **Oxygen:** 15 L/min if hypoxic (SpO2 <94% on room air)
- **Antibiotics:** If superimposed infection (e.g., amoxicillin 500 mg TDS + clarithromycin 500 mg BD)
- **Supportive care:** Pulmonary rehabilitation, physiotherapy
- **Avoid further radiotherapy:** To irradiated lung (risk of permanent fibrosis)

**2. SEVERE MUCOSITIS:**

**Clinical features (occurs 2-3 weeks post-radiotherapy):**
- **Painful oral mucosa:** Ulceration, erythema, pseudomembrane formation
- **Dysphagia:** Severe odynophagia, unable to swallow
- **Dehydration:** Reduced oral intake
- **Weight loss:** Malnutrition

**Management:**
- **Pain control:** Opioid analgesia (e.g., oromorph 10 mg PRN, morphine sulphate solution 10 mg/5 mL)
- **Topical analgesia:** Lidocaine 5% viscous solution 5 mL SWISH & SPIT PRN
- **Mouth care:** Saline mouthwash (0.9% NaCl) QDS, soft toothbrush, avoid alcohol-based mouthwashes
- **Antifungal prophylaxis:** Fluconazole 50 mg OD (or nystatin 100,000 units QDS)
- **Nutritional support:** Dietician referral, consider nasogastric tube or PEG tube if unable to swallow for >1 week
- **IV fluids:** 0.9% NaCl 1-2 L/day if dehydrated

**3. SEVERE ESOPHAGITIS:**

**Clinical features (occurs 2-4 weeks post-radiotherapy):**
- **Odynophagia:** Painful swallowing
- **Dysphagia:** Difficulty swallowing solids, then liquids
- **Chest pain:** Retrosternal chest pain
- **Weight loss:** Reduced oral intake

**Management:**
- **Pain control:** Opioid analgesia (e.g., morphine sulphate solution 10 mg/5 mL 5-10 mL QDS PRN)
- **PPI:** Omeprazole 20 mg OD (acid suppression)
- **Diet modification:** Soft diet, liquid diet if severe
- **Nutritional support:** Dietician referral, consider nasogastric tube if unable to swallow for >1 week
- **Dilate esophageal stricture:** If chronic stricture develops (post-radiotherapy)

**4. SEVERE SKIN REACTION:**

**Clinical features (occurs 2-4 weeks post-radiotherapy):**
- **Erythema:** Redness within radiation field
- **Desquamation:** Dry desquamation (scaling) or moist desquamation (blistering, ulceration)
- **Pain:** Burning sensation, tenderness

**Management:**
- **Dry desquamation:** Moisturiser (e.g., aqueous cream BID), avoid irritants (soap, perfumes)
- **Moist desquamation:** Non-adherent dressing (e.g., Mepitel), topical steroid (e.g., 1% hydrocortisone cream BID)
- **Infection:** If suspected (increasing pain, purulent exudate), oral antibiotics (e.g., flucloxacillin 500 mg QDS)
- **Avoid:** Sun exposure, tight clothing, friction, heat (hot showers)
- **Healing:** Usually 2-4 weeks after radiotherapy completion

**5. ACUTE RADIATION CYSTITIS:**

**Clinical features (occurs 3-6 months post-radiotherapy):**
- **Dysuria:** Painful urination
- **Frequency:** Frequent urination
- **Urgency:** Urgent need to urinate
- **Haematuria:** Blood in urine (microscopic or macroscopic)

**Management:**
- **Hydration:** 2-3 L/day (dilute urine, reduce irritation)
- **Analgesia:** Paracetamol 1 g QDS PRN, NSAID (if renal function adequate)
- **Antispasmodics:** Oxybutynin 5 mg TDS (reduce frequency/urgency)
- **Antibiotics:** If UTI suspected (e.g., trimethoprim 200 mg BD)
- **Bladder irrigation:** For severe haematuria (clot retention)
- **Fulgentration:** For chronic haematuria unresponsive to conservative management

**Sources:** NICE Guidelines, RCR Guidelines, ASTRO Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines", "RCR Guidelines", "ASTRO Guidelines"],
                "emergency_protocol": "acute_radiation_toxicity"
            }
        )

    def _handle_palliative_radiotherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Palliative radiotherapy for bone metastases and brain metastases"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**PALLIATIVE RADIOTHERAPY - BONE METASTASES AND BRAIN METASTASES**

**BONE METASTASES RADIOTHERAPY:**

**Indications:**
- **Painful bone metastases:** Localised bone pain (analgesic requirement)
- **Impending fracture:** Weight-bearing bone with >50% cortical destruction or >2.5 cm lesion
- **Spinal cord compression:** (Emergency - see separate protocol)
- **Prevention:** Prophylactic radiotherapy to high-risk lesions (e.g., femoral metastasis)

**Radiotherapy regimens:**

**Single fraction (preferred):**
- **8 Gy single fraction:** Effective pain relief, convenient for patient
- **Onset of action:** 7-14 days (peak effect at 4-6 weeks)
- **Duration of response:** 50-70% have pain relief at 1 month
- **Re-treatment:** Consider if pain recurs after initial response

**Multi-fraction:**
- **20 Gy in 5 fractions:** For patients with better prognosis (longer survival)
- **30 Gy in 10 fractions:** For complex bone metastases (e.g., weight-bearing bone, multifocal disease)
- **Onset of action:** Similar to single fraction (7-14 days)
- **Duration of response:** Similar to single fraction (50-70% have pain relief at 1 month)

**Side effects:**
- **Acute:** Fatigue, skin erythema (mild), local pain flare (10-20%, transient, responds to analgesia)
- **Late:** Osteonecrosis (rare, <5%), pathological fracture (if bone weakened)

**BRAIN METASTASES RADIOTHERAPY:**

**Indications:**
- **Multiple brain metastases:** ≥3 brain metastases
- **Single brain metastasis:** (Surgery ± radiotherapy, or SRS if ≤3 cm)
- **Progressive disease:** After previous treatment

**Radiotherapy regimens:**

**Whole brain radiotherapy (WBRT):**
- **20 Gy in 5 fractions:** Standard palliative regimen (1 week treatment)
- **12 Gy in 2 fractions:** For frail patients or poor performance status
- **30 Gy in 10 fractions:** For patients with better prognosis (longer survival)
- **Onset of action:** 1-4 weeks (symptom improvement)
- **Survival:** Median 3-6 months (dependent on primary tumour, performance status, extracranial disease control)

**Side effects:**
- **Acute:** Fatigue, alopecia (hair loss), scalp erythema, headache, nausea
- **Subacute:** Somnolence syndrome (drowsiness, worsening neurological symptoms) 4-8 weeks post-treatment (corticosteroids)
- **Late:** Cognitive decline (memory impairment, executive dysfunction), radiation necrosis (rare)

**Stereotactic radiosurgery (SRS):**
- **Indication:** 1-4 brain metastases, each ≤3-4 cm
- **Dose:** 18-24 Gy single fraction (lesion size-dependent)
- **Onset of action:** 4-8 weeks (tumour shrinkage)
- **Advantages:** Focal treatment, spares normal brain, preserves cognitive function
- **Disadvantages:** Requires specialised equipment, not suitable for large or numerous metastases

**DECISION-MAKING:**

**Prognostic factors (better prognosis):**
- **Age:** <65 years
- **Performance status:** ECOG 0-2 (good functional status)
- **Primary tumour:** Breast cancer, renal cell carcinoma (better prognosis)
- **Extracranial disease:** Controlled (no metastases outside brain)
- **Number of brain metastases:** ≤3 metastases

**Recursive partitioning analysis (RPA) classes:**
- **Class I (best prognosis):** Age <65, KPS ≥70, controlled primary, no extracranial metastases → Median survival 7 months
- **Class II (intermediate prognosis):** Age ≥65 OR KPS <70, controlled primary, no extracranial metastases → Median survival 4 months
- **Class III (worst prognosis):** KPS <70, uncontrolled primary, extracranial metastases → Median survival 2 months

**Treatment selection:**
- **Class I:** SRS (if ≤4 metastases, each ≤3-4 cm) OR WBRT (if numerous metastases)
- **Class II:** WBRT (20 Gy in 5 fractions)
- **Class III:** WBRT (12 Gy in 2 fractions) OR best supportive care (if very poor prognosis)

**Sources:** NICE Guidelines (NG76), ASTRO Guidelines, EANO Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG76)", "ASTRO Guidelines", "EANO Guidelines"]
            }
        )

    def _handle_breast_radiotherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Breast cancer radiotherapy guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**BREAST CANCER RADIOTHERAPY**

**INDICATIONS:**

**Breast-conserving surgery (lumpectomy):**
- **Standard:** Whole breast radiotherapy (WBRT) after breast-conserving surgery (reduces risk of ipsilateral breast recurrence by 50%)
- **Age:** All ages (no upper age limit for radiotherapy after breast-conserving surgery)

**Mastectomy:**
- **High-risk features:** Tumour >5 cm, ≥4 positive axillary lymph nodes, positive margins
- **Chest wall radiotherapy:** Reduces risk of locoregional recurrence and improves survival

**LYMPH NODE IRRADIATION:**

**Regional nodal irradiation (RNI):**
- **Indication:** ≥4 positive axillary lymph nodes (or 1-3 positive nodes with other high-risk features)
- **Target volumes:** Supraclavicular fossa (SCF), axilla (levels I-III), internal mammary chain (IMC)

**RADIOTHERAPY TECHNIQUES:**

**Whole breast radiotherapy (WBRT):**
- **Standard dose:** 40 Gy in 15 fractions (3 weeks, 2.67 Gy per fraction)
- **Alternative:** 50 Gy in 25 fractions (5 weeks, 2 Gy per fraction)
- **Boost:** Additional 10-16 Gy to tumour bed (if age <50, high-grade tumour, close/positive margins)

**Partial breast irradiation (PBI):**
- **Indication:** Low-risk early breast cancer (age >50, tumour <3 cm, node-negative, clear margins)
- **Techniques:** External beam radiotherapy (EBRT), brachytherapy (interstitial, intracavitary), intraoperative radiotherapy (IORT)
- **Dose:** 38.5 Gy in 10 fractions BID (external beam) OR 20 Gy single fraction (IORT)

**SIMULATION:**

**CT simulation:**
- **Position:** Supine, breast board (inclination to separate breast from chest wall)
- **Immobilisation:** Arm abduction (affected side), thermoplastic mask (if nodal irradiation)
- **Tattoos:** Small permanent skin marks (3-5) for setup verification
- **Contrast:** Oral contrast (to delineate small bowel if IMC irradiated)

**TARGET VOLUMES:**
- **GTV (Gross Tumour Volume):** Tumour bed (if visible on CT planning scan)
- **CTV (Clinical Target Volume):** Whole breast (or chest wall) ± regional nodes (SCF, axilla, IMC)
- **PTV (Planning Target Volume):** CTV + setup margin (usually 0.5-1 cm)

**ORGANS AT RISK (OAR):**
- **Heart:** Mean dose <4 Gy (left breast) OR <2 Gy (right breast) (reduce risk of cardiac morbidity)
- **Left anterior descending (LAD) artery:** Max dose <20 Gy
- **Lungs:** V20 <30% (volume of lung receiving ≥20 Gy) (reduce risk of radiation pneumonitis)
- **Contralateral breast:** Max dose <5 Gy (reduce risk of secondary malignancy)
- **Thyroid:** Mean dose <30 Gy (reduce risk of hypothyroidism)
- **Spinal cord:** Max dose <45 Gy (reduce risk of myelopathy)

**SIDE EFFECTS:**

**Acute (during radiotherapy):**
- **Skin reaction:** Erythema, dry desquamation, moist desquamation (inframammary fold, axilla)
- **Fatigue:** Mild-moderate fatigue (improves after radiotherapy completion)
- **Breast pain:** Mild discomfort, tenderness
- **Lymphoedema:** Arm swelling (if axillary irradiation)

**Late (months to years after radiotherapy):**
- **Breast fibrosis:** Firmness, shrinkage, cosmetic changes
- **Telangiectasia:** Dilated blood vessels (cosmetic)
- **Cardiac toxicity:** Ischaemic heart disease, pericarditis (left breast radiotherapy)
- **Radiation pneumonitis:** Cough, dyspnoea, fever (rare, <5%)
- **Rib fracture:** Rare (<1%)
- **Secondary malignancy:** Rare (<1% at 10 years)

**SIDE EFFECT MANAGEMENT:**

**Skin reaction:**
- **Dry desquamation:** Moisturiser (e.g., aqueous cream BID)
- **Moist desquamation:** Non-adherent dressing (e.g., Mepitel), topical steroid (e.g., 1% hydrocortisone cream BID)
- **Avoid:** Sun exposure, tight clothing, deodorant (if skin reaction severe)

**Fatigue:**
- **Exercise:** Light exercise (walking, yoga)
- **Sleep hygiene:** Regular sleep pattern, avoid caffeine
- **Energy conservation:** Prioritise activities, rest breaks

**Lymphoedema:**
- **Prevention:** Avoid blood pressure measurement, venepuncture, IV cannulation on affected arm
- **Early treatment:** Compression garment, manual lymphatic drainage massage, physiotherapy

**Sources:** NICE Guidelines (NG101), ABS Consensus Guidelines, ESTRO Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG101)", "ABS Consensus Guidelines", "ESTRO Guidelines"]
            }
        )

    def _handle_prostate_radiotherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Prostate cancer radiotherapy guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**PROSTATE CANCER RADIOTHERAPY**

**INDICATIONS:**

**Localised prostate cancer:**
- **Low-risk:** Radiotherapy OR active surveillance OR radical prostatectomy
- **Intermediate-risk:** Radiotherapy + androgen deprivation therapy (ADT) OR radical prostatectomy
- **High-risk:** Radiotherapy + long-term ADT OR radical prostatectomy

**Locally advanced prostate cancer:**
- **Radiotherapy + long-term ADT** (standard treatment)

**RADIOTHERAPY TECHNIQUES:**

**External beam radiotherapy (EBRT):**
- **Standard dose:** 60 Gy in 20 fractions (4 weeks, 3 Gy per fraction) OR 74 Gy in 37 fractions (7.5 weeks, 2 Gy per fraction)
- **Technique:** IMRT (intensity-modulated radiotherapy) OR VMAT (volumetric modulated arc therapy) (image-guided radiotherapy with fiducial markers or cone-beam CT)
- **Advantages:** Precise dose delivery, reduced toxicity, dose escalation possible

**Brachytherapy (LDR - low dose rate):**
- **Indication:** Low-risk localised prostate cancer (Gleason ≤6, PSA <10 ng/mL, T1-T2a)
- **Technique:** Permanent implantation of radioactive iodine-125 (I-125) seeds into prostate
- **Dose:** 145 Gy (prescribed dose)
- **Advantages:** Single procedure, outpatient, rapid return to normal activities
- **Disadvantages:** Requires general anaesthesia, urinary retention risk, erectile dysfunction risk

**Brachytherapy (HDR - high dose rate):**
- **Indication:** Intermediate- to high-risk localised prostate cancer (boost after EBRT)
- **Technique:** Temporary insertion of radioactive iridium-192 (Ir-192) sources into prostate
- **Dose:** 15 Gy in 3 fractions (boost after EBRT)
- **Advantages:** Precise dose delivery, outpatient (day case)
- **Disadvantages:** Requires general anaesthesia, urinary retention risk, erectile dysfunction risk

**SIMULATION:**

**CT simulation:**
- **Preparation:** Full bladder (push small bowel out of pelvis), empty rectum (enema if required)
- **Position:** Supine, immobilisation device (vac-lok, foot stocks)
- **Fiducial markers:** Gold seeds inserted into prostate (under ultrasound guidance) for image guidance
- **Tattoos:** Small permanent skin marks (3-5) for setup verification

**TARGET VOLUMES:**
- **GTV (Gross Tumour Volume):** Prostate (visible on CT planning scan or MRI fusion)
- **CTV (Clinical Target Volume):** Prostate ± proximal seminal vesicles (if high-risk)
- **PTV (Planning Target Volume):** CTV + setup margin (usually 0.5-1 cm)

**ORGANS AT RISK (OAR):**
- **Rectum:** V70 <20% (volume of rectum receiving ≥70 Gy) (reduce risk of proctitis)
- **Bladder:** V65 <50% (volume of bladder receiving ≥65 Gy) (reduce risk of cystitis)
- **Femoral heads:** V50 <5% (volume of femoral heads receiving ≥50 Gy) (reduce risk of femoral head necrosis)
- **Urethra:** Max dose <75 Gy (reduce risk of urethral stricture)
- **Penile bulb:** Mean dose <50 Gy (reduce risk of erectile dysfunction)

**SIDE EFFECTS:**

**Acute (during radiotherapy):**
- **Urinary:** Frequency, urgency, dysuria, nocturia, haematuria
- **Gastrointestinal:** Diarrhoea, proctitis, tenesmus, rectal bleeding
- **Sexual:** Erectile dysfunction (temporary during radiotherapy)
- **Fatigue:** Mild-moderate fatigue (improves after radiotherapy completion)

**Late (months to years after radiotherapy):**
- **Urinary:** Urethral stricture, urinary incontinence (rare, <5%)
- **Gastrointestinal:** Chronic proctitis, rectal bleeding, fistula (rare, <1%)
- **Sexual:** Erectile dysfunction (30-50% at 5 years)
- **Secondary malignancy:** Rectal cancer, bladder cancer (rare, <1% at 10 years)

**SIDE EFFECT MANAGEMENT:**

**Urinary symptoms:**
- **Alpha-blocker:** Tamsulosin 400 mcg OD (reduce frequency/urgency)
- **Analgesia:** Paracetamol 1 g QDS PRN
- **Hydration:** 2-3 L/day (dilute urine, reduce irritation)
- **Avoid:** Caffeine, alcohol (bladder irritants)

**Gastrointestinal symptoms:**
- **Loperamide:** 2 mg PRN (diarrhoea)
- **Rectal steroids:** Predfoam enema BD (proctitis)
- **Diet modification:** Low-residue diet (reduce bowel frequency)
- **Hydration:** 2-3 L/day (prevent dehydration)

**Erectile dysfunction:**
- **Phosphodiesterase-5 inhibitors:** Sildenafil 50 mg PRN (30-60 minutes before sexual activity)
- **Referral:** Erectile dysfunction clinic (if PDE5 inhibitors ineffective)

**Sources:** NICE Guidelines (NG131), EAU Guidelines, ASTRO Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG131)", "EAU Guidelines", "ASTRO Guidelines"]
            }
        )

    def _handle_lung_radiotherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Lung cancer radiotherapy guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**LUNG CANCER RADIOTHERAPY**

**INDICATIONS:**

**Non-small cell lung cancer (NSCLC):**

**Early-stage (stage I):**
- **SABR (stereotactic ablative radiotherapy):** Alternative to surgery for medically inoperable patients
- **Dose:** 54 Gy in 3 fractions OR 50 Gy in 5 fractions (peripheral tumour)
- **Central tumours:** 60 Gy in 8 fractions (reduced dose due to higher toxicity risk)
- **Outcomes:** 3-year local control 80-90% (comparable to surgery)

**Locally advanced (stage III):**
- **Concurrent chemoradiotherapy (cCRT):** Cisplatin-based chemotherapy + radiotherapy (standard treatment)
- **Sequential chemoradiotherapy (sCRT):** Chemotherapy followed by radiotherapy (if unfit for concurrent)
- **Radiotherapy dose:** 60 Gy in 30 fractions (6 weeks, 2 Gy per fraction)
- **Target volume:** Primary tumour + involved lymph nodes (CT/PET-based)

**Metastatic (stage IV):**
- **Palliative radiotherapy:** Symptomatic thoracic disease (cough, dyspnoea, haemoptysis, chest pain)
- **Dose:** 20 Gy in 5 fractions OR 8 Gy single fraction (palliative)

**Small cell lung cancer (SCLC):**

**Limited-stage (LS-SCLC):**
- **Concurrent chemoradiotherapy (cCRT):** Cisplatin + etoposide + radiotherapy (starting cycle 2 or 3)
- **Radiotherapy dose:** 45 Gy in 30 fractions BID (3 weeks, 1.5 Gy per fraction BID) OR 66 Gy in 33 fractions (6.5 weeks, 2 Gy per fraction)
- **Prophylactic cranial irradiation (PCI):** 25 Gy in 10 fractions (reduces risk of brain metastases)

**Extensive-stage (ES-SCLC):**
- **Chemotherapy:** Cisplatin + etoposide (first-line)
- **Prophylactic cranial irradiation (PCI):** If response to chemotherapy (reduces risk of brain metastases)
- **Palliative radiotherapy:** Symptomatic thoracic disease, brain metastases, bone metastases

**RADIOTHERAPY TECHNIQUES:**

**3D-CRT (3-dimensional conformal radiotherapy):**
- **Technique:** Multiple beams shaped to tumour (using multileaf collimator)
- **Advantages:** Conformal dose distribution, reduces normal tissue toxicity
- **Disadvantages:** Less conformal than IMRT/VMAT

**IMRT (intensity-modulated radiotherapy):**
- **Technique:** Modulated beam intensity (optimises dose distribution)
- **Advantages:** More conformal dose distribution, reduces normal tissue toxicity
- **Disadvantages:** Longer treatment time, higher integral dose (low-dose bath)

**VMAT (volumetric modulated arc therapy):**
- **Technique:** Rotational delivery with modulated beam intensity
- **Advantages:** Faster treatment time (2-3 minutes vs. 10-15 minutes), more conformal dose distribution
- **Disadvantages:** Higher integral dose (low-dose bath)

**IGRT (image-guided radiotherapy):**
- **Technique:** Daily imaging (cone-beam CT) to verify target position before treatment
- **Advantages:** Reduces setup error, enables margin reduction, improves accuracy

**SIMULATION:**

**CT simulation:**
- **Position:** Supine, immobilisation (vac-lok, arm rest above head)
- **Breathing technique:** Deep inspiration breath-hold (DIBH) (reduces heart dose, especially left-sided tumours) OR 4D-CT (assess tumour motion with breathing)
- **Contrast:** IV contrast (to delineate tumour, mediastinal lymph nodes)
- **PET-CT fusion:** For staging and target volume delineation (especially for lymph nodes)

**TARGET VOLUMES:**
- **GTV (Gross Tumour Volume):** Primary tumour + involved lymph nodes (CT/PET-based)
- **CTV (Clinical Target Volume):** GTV + margin for microscopic disease (usually 0.5-1 cm)
- **ITV (Internal Target Volume):** CTV + margin for tumour motion (using 4D-CT or DIBH)
- **PTV (Planning Target Volume):** ITV + setup margin (usually 0.5-1 cm)

**ORGANS AT RISK (OAR):**
- **Spinal cord:** Max dose <45 Gy (reduce risk of myelopathy)
- **Lungs:** V20 <35% (volume of lungs receiving ≥20 Gy) (reduce risk of radiation pneumonitis)
- **Heart:** Mean dose <20 Gy (left-sided tumours) OR <10 Gy (right-sided tumours) (reduce risk of cardiac toxicity)
- **Oesophagus:** Mean dose <34 Gy (reduce risk of oesophagitis)
- **Thyroid:** Mean dose <30 Gy (reduce risk of hypothyroidism)

**SIDE EFFECTS:**

**Acute (during radiotherapy):**
- **Oesophagitis:** Dysphagia, odynophagia, chest pain (grade 2-3)
- **Pneumonitis:** Cough, dyspnoea, fever, hypoxia (rare, <10%)
- **Fatigue:** Mild-moderate fatigue (improves after radiotherapy completion)
- **Skin reaction:** Erythema, dry desquamation (mild, unless high-dose)

**Late (months to years after radiotherapy):**
- **Pulmonary fibrosis:** Reduced lung function, dyspnoea on exertion (V20 predicts risk)
- **Cardiac toxicity:** Ischaemic heart disease, pericarditis (left-sided tumours)
- **Oesophageal stricture:** Dysphagia (late oesophagitis complication)
- **Spinal cord myelopathy:** Rare (<1%, max dose <45 Gy)
- **Secondary malignancy:** Rare (<1% at 10 years)

**SIDE EFFECT MANAGEMENT:**

**Oesophagitis:**
- **Pain control:** Opioid analgesia (e.g., morphine sulphate solution 10 mg/5 mL 5-10 mL QDS PRN)
- **PPI:** Omeprazole 20 mg OD (acid suppression)
- **Diet modification:** Soft diet, liquid diet if severe
- **Nutritional support:** Dietician referral, consider nasogastric tube if unable to swallow for >1 week

**Radiation pneumonitis:**
- **High-dose corticosteroids:** Prednisolone 1 mg/kg/day (max 60 mg OD) for 4-6 weeks, then slow taper over 6-12 weeks
- **Oxygen:** 15 L/min if hypoxic (SpO2 <94% on room air)
- **Antibiotics:** If superimposed infection (e.g., amoxicillin 500 mg TDS + clarithromycin 500 mg BD)

**Sources:** NICE Guidelines (NG122), ASTRO Guidelines, ESTRO Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG122)", "ASTRO Guidelines", "ESTRO Guidelines"]
            }
        )

    def _handle_head_neck_radiotherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Head and neck cancer radiotherapy guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**HEAD AND NECK CANCER RADIOTHERAPY**

**INDICATIONS:**

**Early-stage (stage I-II):**
- **Radiotherapy alone:** Alternative to surgery (organ preservation, especially larynx)
- **Dose:** 66 Gy in 33 fractions (6.5 weeks, 2 Gy per fraction)
- **Brachytherapy:** Selected early-stage oral cavity, oropharyngeal cancers

**Locally advanced (stage III-IV):**
- **Concurrent chemoradiotherapy (cCRT):** Cisplatin 100 mg/m² IV day 1, 22, 43 (standard treatment)
- **Radiotherapy dose:** 70 Gy in 35 fractions (7 weeks, 2 Gy per fraction)
- **Target volume:** Primary tumour + involved lymph nodes (CT/PET-based)

**Post-operative radiotherapy:**
- **Indication:** Positive margins, extracapsular extension (ECE), perineural invasion, lymphovascular invasion, multiple positive lymph nodes
- **Radiotherapy dose:** 60-66 Gy in 30-33 fractions (6-6.5 weeks, 2 Gy per fraction)
- **Concurrent chemotherapy:** If high-risk features (positive margins, ECE)

**RADIOTHERAPY TECHNIQUES:**

**IMRT (intensity-modulated radiotherapy):**
- **Technique:** Modulated beam intensity (optimises dose distribution)
- **Advantages:** Parotid sparing (reduces xerostomia), conformal dose distribution
- **Standard of care** for most head and neck cancers

**VMAT (volumetric modulated arc therapy):**
- **Technique:** Rotational delivery with modulated beam intensity
- **Advantages:** Faster treatment time (2-3 minutes vs. 10-15 minutes)

**IGRT (image-guided radiotherapy):**
- **Technique:** Daily imaging (cone-beam CT) to verify target position before treatment
- **Advantages:** Reduces setup error, enables margin reduction, improves accuracy

**SIMULATION:**

**CT simulation:**
- **Position:** Supine, immobilisation (head shell, shoulder depression)
- **Dental assessment:** Extract decayed teeth (reduce risk of osteoradionecrosis)
- **Dental mould:** Fluoride mouthguard (to protect teeth during radiotherapy)
- **Contrast:** IV contrast (to delineate tumour, lymph nodes)
- **PET-CT fusion:** For staging and target volume delineation

**TARGET VOLUMES:**
- **GTV (Gross Tumour Volume):** Primary tumour + involved lymph nodes (clinical/examination + imaging)
- **CTV (Clinical Target Volume):** GTV + margin for microscopic disease (usually 1 cm)
- **PTV (Planning Target Volume):** CTV + setup margin (usually 0.3-0.5 cm)

**Prophylactic nodal irradiation:**
- **N0 neck (clinically negative):** Elective irradiation of levels at risk (based on primary tumour site)
- **N1-N3 neck (clinically positive):** Therapeutic irradiation of involved nodal levels ± prophylactic irradiation of additional levels

**ORGANS AT RISK (OAR):**
- **Spinal cord:** Max dose <45 Gy (reduce risk of myelopathy)
- **Brainstem:** Max dose <54 Gy (reduce risk of brainstem injury)
- **Optic chiasm:** Max dose <50 Gy (reduce risk of visual loss)
- **Optic nerves:** Max dose <50 Gy (reduce risk of visual loss)
- **Parotid glands:** Mean dose <26 Gy (reduce risk of xerostomia)
- **Oral cavity:** Mean dose <30 Gy (reduce risk of mucositis)
- **Larynx:** Mean dose <44 Gy (reduce risk of laryngeal dysfunction)
- **Mandible:** Max dose <70 Gy (reduce risk of osteoradionecrosis)
- **Temporomandibular joint (TMJ):** Max dose <65 Gy (reduce risk of trismus)
- **Middle ear:** Mean dose <45 Gy (reduce risk of otitis media)

**SIDE EFFECTS:**

**Acute (during radiotherapy):**
- **Mucositis:** Painful oral mucosa, ulceration, pseudomembrane formation (grade 2-3)
- **Dysphagia:** Odynophagia, inability to swallow solids, then liquids
- **Xerostomia:** Dry mouth (due to salivary gland dysfunction)
- **Dysgeusia:** Altered taste sensation (temporary during radiotherapy)
- **Skin reaction:** Erythema, dry desquamation, moist desquamation (neck, face)
- **Fatigue:** Moderate fatigue (improves after radiotherapy completion)

**Late (months to years after radiotherapy):**
- **Xerostomia:** Permanent dry mouth (if parotid glands irradiated to high dose)
- **Dental caries:** Increased risk (due to xerostomia)
- **Osteoradionecrosis:** Bone necrosis (mandible, maxilla) (rare, <5%)
- **Dysphagia:** Chronic oesophageal stricture (late oesophagitis complication)
- **Hypothyroidism:** If thyroid gland in treatment field (30-50% at 5 years)
- **Trismus:** Temporomandibular joint (TMJ) fibrosis (reduced mouth opening)
- **Second primary malignancy:** Rare (<1% at 10 years)

**SIDE EFFECT MANAGEMENT:**

**Mucositis:**
- **Pain control:** Opioid analgesia (e.g., oromorph 10 mg PRN, morphine sulphate solution 10 mg/5 mL)
- **Topical analgesia:** Lidocaine 5% viscous solution 5 mL SWISH & SPIT PRN
- **Mouth care:** Saline mouthwash (0.9% NaCl) QDS, soft toothbrush, avoid alcohol-based mouthwashes
- **Antifungal prophylaxis:** Fluconazole 50 mg OD (or nystatin 100,000 units QDS)
- **Nutritional support:** Dietician referral, consider nasogastric tube or PEG tube if unable to swallow for >1 week

**Xerostomia:**
- **Saliva substitutes:** Artificial saliva (e.g., Biotene mouthwash)
- **Saliva stimulants:** Pilocarpine 5 mg TDS (if residual salivary function)
- **Dental care:** Fluoride mouthguard, regular dental review (prevent dental caries)
- **Hydration:** Sip water regularly

**Dysphagia:**
- **Pain control:** Opioid analgesia (e.g., morphine sulphate solution 10 mg/5 mL 5-10 mL QDS PRN)
- **Diet modification:** Soft diet, liquid diet if severe
- **Nutritional support:** Dietician referral, consider nasogastric tube or PEG tube if unable to swallow for >1 week

**Skin reaction:**
- **Dry desquamation:** Moisturiser (e.g., aqueous cream BID)
- **Moist desquamation:** Non-adherent dressing (e.g., Mepitel), topical steroid (e.g., 1% hydrocortisone cream BID)
- **Avoid:** Sun exposure, tight clothing, friction, heat (hot showers)

**Sources:** NICE Guidelines (NG36), ASTRO Guidelines, DAHANCA Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG36)", "ASTRO Guidelines", "DAHANCA Guidelines"]
            }
        )

    def _handle_radiation_side_effects(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Radiation side effects management"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**RADIATION SIDE EFFECTS MANAGEMENT**

**ACUTE SIDE EFFECTS (DURING RADIOTHERAPY):**

**SKIN REACTIONS:**

**Grade 1 (mild erythema):**
- **Appearance:** Redness, dry skin, mild itching
- **Management:** Moisturiser (e.g., aqueous cream BID), avoid irritants (soap, perfumes)

**Grade 2 (dry desquamation):**
- **Appearance:** Peeling skin, dry scaling, moderate itching
- **Management:** Moisturiser (e.g., aqueous cream BID), topical steroid (e.g., 1% hydrocortisone cream BID)

**Grade 3 (moist desquamation):**
- **Appearance:** Blistering, ulceration, weeping skin
- **Management:** Non-adherent dressing (e.g., Mepitel), topical steroid (e.g., 1% hydrocortisone cream BID), oral antibiotics if infection (e.g., flucloxacillin 500 mg QDS)

**Prevention:**
- **Wash gently:** Lukewarm water, pat dry (don't rub)
- **Wear loose clothing:** Cotton clothing, avoid friction
- **Avoid sun:** No sun exposure to treated area
- **Avoid heat:** Hot showers, saunas, heat packs

**MUCOSITIS:**

**Grade 1 (mild):**
- **Appearance:** Erythema, mild discomfort
- **Management:** Saline mouthwash (0.9% NaCl) QDS, maintain oral hygiene

**Grade 2 (moderate):**
- **Appearance:** Patchy ulceration, moderate pain, able to eat soft diet
- **Management:** Topical analgesia (lidocaine 5% viscous solution 5 mL SWISH & SPIT PRN), oral analgesia (paracetamol 1 g QDS PRN), maintain oral hygiene

**Grade 3 (severe):**
- **Appearance:** Confluent ulceration, severe pain, unable to swallow
- **Management:** Opioid analgesia (e.g., oromorph 10 mg PRN, morphine sulphate solution 10 mg/5 mL 5-10 mL QDS PRN), topical analgesia (lidocaine 5% viscous solution 5 mL SWISH & SPIT PRN), antifungal prophylaxis (fluconazole 50 mg OD or nystatin 100,000 units QDS), nutritional support (dietician referral, consider nasogastric tube or PEG tube if unable to swallow for >1 week)

**Prevention:**
- **Oral hygiene:** Soft toothbrush, saline mouthwash (0.9% NaCl) QDS
- **Avoid:** Alcohol, tobacco, spicy foods, acidic foods
- **Saliva substitutes:** Artificial saliva (e.g., Biotene mouthwash)

**DYSPHAGIA:**

**Grade 1 (mild):**
- **Symptoms:** Able to eat soft diet
- **Management:** Diet modification (soft diet), maintain nutrition

**Grade 2 (moderate):**
- **Symptoms:** Unable to eat solid food, able to swallow liquids
- **Management:** Diet modification (liquid diet), nutritional support (dietician referral), pain control (paracetamol 1 g QDS PRN)

**Grade 3 (severe):**
- **Symptoms:** Unable to swallow liquids, dehydration
- **Management:** Pain control (opioid analgesia, e.g., morphine sulphate solution 10 mg/5 mL 5-10 mL QDS PRN), nutritional support (nasogastric tube or PEG tube if unable to swallow for >1 week), IV fluids if dehydrated

**NAUSEA AND VOMITING:**

**Grade 1 (mild):**
- **Symptoms:** Able to eat adequate diet
- **Management:** Dietary advice (small, frequent meals, avoid fatty/spicy foods)

**Grade 2 (moderate):**
- **Symptoms:** Reduced oral intake, IV fluids indicated <24 hours
- **Management:** Antiemetic (e.g., ondansetron 8 mg BD), dietary advice

**Grade 3 (severe):**
- **Symptoms:** Inadequate oral intake, IV fluids indicated ≥24 hours
- **Management:** Antiemetic (e.g., ondansetron 8 mg TDS, dexamethasone 8 mg OD), IV fluids, nutritional support

**FATIGUE:**

**Grade 1 (mild):**
- **Symptoms:** Overexertion affects normal activities
- **Management:** Energy conservation, light exercise (walking, yoga)

**Grade 2 (moderate):**
- **Symptoms:** Unable to work, able to perform activities of daily living
- **Management:** Energy conservation, light exercise, sleep hygiene

**Grade 3 (severe):**
- **Symptoms:** Unable to perform activities of daily living, bedbound
- **Management:** Supportive care, referral to palliative care if appropriate

**LATE SIDE EFFECTS (MONTHS TO YEARS AFTER RADIOTHERAPY):**

**XEROSTOMIA (DRY MOUTH):**
- **Symptoms:** Dry mouth, difficulty swallowing, speaking, dental caries
- **Management:** Saliva substitutes (artificial saliva, e.g., Biotene mouthwash), saliva stimulants (pilocarpine 5 mg TDS if residual salivary function), dental care (fluoride mouthguard, regular dental review)

**FIBROSIS:**
- **Symptoms:** Tissue hardening, reduced mobility, contractures
- **Management:** Physiotherapy, massage, scar management

**TELANGIECTASIA:**
- **Symptoms:** Dilated blood vessels, cosmetic concern
- **Management:** Laser therapy, cosmetic camouflage

**LYMPHOEDEMA:**
- **Symptoms:** Limb swelling, heaviness, discomfort
- **Management:** Compression garment, manual lymphatic drainage massage, physiotherapy

**OSTEORADIONECROSIS:**
- **Symptoms:** Bone necrosis, pain, fracture (mandible, ribs)
- **Management:** Surgical debridement, hyperbaric oxygen therapy, antibiotics if infection

**SECONDARY MALIGNANCY:**
- **Symptoms:** New cancer within radiation field (usually years after radiotherapy)
- **Management:** Oncology referral, staging, treatment (surgery, radiotherapy, chemotherapy)

**Sources:** NICE Guidelines, RCR Guidelines, CTCAE (Common Terminology Criteria for Adverse Events)""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines", "RCR Guidelines", "CTCAE"]
            }
        )

    def _handle_brachytherapy(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Brachytherapy guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**BRACHYTHERAPY (INTERNAL RADIOTHERAPY)**

**DEFINITION:**
Brachytherapy involves placing radioactive sources inside or adjacent to tumour, delivering high dose of radiation to tumour while sparing surrounding normal tissues.

**BRACHYTHERAPY TECHNIQUES:**

**1. LOW-DOSE RATE (LDR) BRACHYTHERAPY:**

**Prostate cancer (LDR):**
- **Indication:** Low-risk localised prostate cancer (Gleason ≤6, PSA <10 ng/mL, T1-T2a)
- **Technique:** Permanent implantation of radioactive iodine-125 (I-125) seeds into prostate
- **Dose:** 145 Gy (prescribed dose)
- **Procedure:** General anaesthesia or spinal anaesthesia, transrectal ultrasound-guided seed implantation (outpatient procedure, 1-2 hours)
- **Advantages:** Single procedure, outpatient, rapid return to normal activities, precise dose delivery
- **Disadvantages:** Requires general anaesthesia, urinary retention risk (10-20%), erectile dysfunction risk (30-50% at 5 years), rectal toxicity (diarrhoea, bleeding, rare)

**Gynaecological brachytherapy (LDR):**
- **Indication:** Cervical cancer, endometrial cancer (boost after EBRT)
- **Technique:** Afterloading applicators (Fletcher-Suit applicator) placed in cervix/uterus under anaesthesia
- **Dose:** 20-30 Gy (prescribed dose)
- **Procedure:** General anaesthesia, applicator insertion, imaging verification (CT/MRI), treatment planning, radioactive source insertion (outpatient procedure, 1-2 days)

**2. HIGH-DOSE RATE (HDR) BRACHYTHERAPY:**

**Prostate cancer (HDR):**
- **Indication:** Intermediate- to high-risk localised prostate cancer (boost after EBRT)
- **Technique:** Temporary insertion of radioactive iridium-192 (Ir-192) sources into prostate
- **Dose:** 15 Gy in 3 fractions (boost after EBRT)
- **Procedure:** General anaesthesia or spinal anaesthesia, transperineal catheter insertion (day case)
- **Advantages:** Precise dose delivery, outpatient (day case), no permanent radioactive sources
- **Disadvantages:** Requires general anaesthesia, urinary retention risk (10-20%), erectile dysfunction risk (30-50% at 5 years)

**Gynaecological brachytherapy (HDR):**
- **Indication:** Cervical cancer (standard treatment), endometrial cancer (boost after EBRT)
- **Technique:** Afterloading applicators (Fletcher-Suit applicator, ring and tandem) placed in cervix/uterus under anaesthesia
- **Dose:** 21 Gy in 3 fractions (cervical cancer)
- **Procedure:** General anaesthesia, applicator insertion, imaging verification (CT/MRI), treatment planning, radioactive source insertion (outpatient procedure, 3 fractions over 3-5 days)

**Lung cancer (HDR):**
- **Indication:** Endobronchial lung cancer (palliative)
- **Technique:** Endobronchial catheter insertion via bronchoscopy
- **Dose:** 15 Gy single fraction (palliative)
- **Procedure:** Local anaesthesia, bronchoscopy, catheter insertion, treatment planning, radioactive source insertion (outpatient procedure)

**Oesophageal cancer (HDR):**
- **Indication:** Oesophageal cancer (palliative)
- **Technique:** Endoluminal catheter insertion via endoscopy
- **Dose:** 10-12 Gy single fraction (palliative)
- **Procedure:** Sedation, endoscopy, catheter insertion, treatment planning, radioactive source insertion (outpatient procedure)

**3. PULSEDOSE RATE (PDR) BRACHYTHERAPY:**

**Technique:** Delivers radiation in pulses (hourly) over several days (combines advantages of LDR and HDR)

**Advantages:** Outpatient treatment (after initial implantation), flexible dose distribution
**Disadvantages:** Requires prolonged immobilisation, limited availability

**BRACHYTHERAPY VS. EXTERNAL BEAM RADIOTHERAPY (EBRT):**

**Brachytherapy advantages:**
- **Higher dose:** Delivers higher dose to tumour (more effective tumour kill)
- **Sparing of normal tissues:** Rapid dose fall-off (reduces toxicity)
- **Shorter treatment time:** Single procedure (LDR) or few fractions (HDR)
- **Convenience:** Outpatient procedure (no daily treatment for 6-7 weeks)

**EBRT advantages:**
- **Non-invasive:** No anaesthesia, no procedure
- **Treats larger volumes:** Treats primary tumour + lymph nodes
- **Flexible:** Can treat any tumour site (not limited by accessibility)
- **Widely available:** More accessible than brachytherapy

**BRACHYTHERAPY SIDE EFFECTS:**

**Prostate brachytherapy:**
- **Acute:** Urinary frequency, urgency, dysuria, nocturia, haematuria, rectal irritation, fatigue
- **Late:** Urinary incontinence (rare, <5%), urethral stricture (rare, <5%), erectile dysfunction (30-50% at 5 years), rectal bleeding (rare, <5%)

**Gynaecological brachytherapy:**
- **Acute:** Vaginal discharge, bleeding, pain, urinary frequency, dysuria, diarrhoea
- **Late:** Vaginal stenosis (reduced vaginal length, dyspareunia), vaginal dryness, cystitis, proctitis, fistula (rare, <1%)

**BRACHYTHERAPY PRECAUTIONS:**

**LDR prostate brachytherapy:**
- **Radiation safety:** Temporary precautions for 2-3 months after implantation (radiation exposure to others is minimal, but avoid prolonged close contact with pregnant women and young children)
- **Seed migration:** Rare (<5%), seeds may migrate to lungs (usually asymptomatic, require chest X-ray if respiratory symptoms)

**HDR brachytherapy:**
- **No radiation precautions:** Radioactive sources removed after treatment (no radiation exposure to others)

**Sources:** NICE Guidelines, ABS (American Brachytherapy Society) Guidelines, ESTRO Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines", "ABS Guidelines", "ESTRO Guidelines"]
            }
        )

    def _handle_srs(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Stereotactic radiosurgery (SRS) guidance"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**STEREOTACTIC RADIOSURGERY (SRS)**

**DEFINITION:**
Stereotactic radiosurgery (SRS) is a highly precise form of radiation therapy that delivers a high dose of radiation to a small, well-defined target in a single or few fractions, while sparing surrounding normal tissues.

**SRS TECHNIQUES:**

**1. GAMMA KNIFE:**
- **Technique:** 201 cobalt-60 sources, focused on target (stereotactic frame immobilisation)
- **Indication:** Brain metastases (1-4 lesions, each ≤3-4 cm), vestibular schwannoma, meningioma, arteriovenous malformation (AVM), trigeminal neuralgia
- **Procedure:** Local anaesthesia + sedation, stereotactic frame fixation, MRI planning, treatment (4-6 hours)
- **Dose:** 18-24 Gy single fraction (lesion size-dependent)
- **Advantages:** High precision, rapid dose fall-off, single treatment
- **Disadvantages:** Invasive (frame fixation), limited to intracranial lesions

**2. CYBERKNIFE:**
- **Technique:** Linear accelerator mounted on robotic arm, real-time image guidance (no frame required)
- **Indication:** Brain metastases (1-5 lesions, each ≤5 cm), vestibular schwannoma, meningioma, spinal tumours, prostate cancer (extracranial SRS/SBRT)
- **Procedure:** Customised immobilisation mask (for brain) or vac-lok (for spine), CT planning, treatment (1-2 hours)
- **Dose:** 18-24 Gy single fraction (lesion size-dependent) OR 27-35 Gy in 3-5 fractions (larger lesions or lesions near critical structures)
- **Advantages:** Non-invasive (no frame required), extracranial applications (spine, prostate, lung, liver)
- **Disadvantages:** Longer treatment time, higher integral dose (low-dose bath)

**3. LINAC-BASED SRS:**
- **Technique:** Modified linear accelerator with micromultileaf collimator or cone-based collimation (frameless, image-guided)
- **Indication:** Brain metastases (1-5 lesions, each ≤5 cm), vestibular schwannoma, meningioma, AVM
- **Procedure:** Customised immobilisation mask, CT planning, treatment (30-60 minutes)
- **Dose:** 18-24 Gy single fraction (lesion size-dependent) OR 27-35 Gy in 3-5 fractions (larger lesions or lesions near critical structures)
- **Advantages:** Non-invasive (no frame required), widely available
- **Disadvantages:** Less precise than Gamma Knife (for single fraction), higher integral dose (low-dose bath)

**SRS INDICATIONS:**

**Brain metastases:**
- **Indication:** 1-4 brain metastases, each ≤3-4 cm (Gamma Knife) OR 1-5 brain metastases, each ≤5 cm (CyberKnife/LINAC)
- **Advantages:** Focal treatment, spares normal brain, preserves cognitive function, single treatment (or few fractions)
- **Outcomes:** Local control 80-90% at 1 year (dependent on tumour type, size)
- **WBRT alternative:** SRS alone (no WBRT) preserves cognitive function, but higher risk of new brain metastases (salvage SRS or WBRT at progression)

**Vestibular schwannoma (acoustic neuroma):**
- **Indication:** Growing vestibular schwannoma, symptomatic (hearing loss, tinnitus, imbalance)
- **Dose:** 12-13 Gy single fraction (margin dose)
- **Outcomes:** Tumour control 90-95% at 5 years, hearing preservation 50-70% (dependent on pre-treatment hearing)

**Meningioma:**
- **Indication:** Growing meningioma, symptomatic (headache, seizure, neurological deficit), or postoperative residual/recurrent tumour
- **Dose:** 14-16 Gy single fraction (margin dose)
- **Outcomes:** Tumour control 90-95% at 5 years

**Arteriovenous malformation (AVM):**
- **Indication:** Unruptured AVM (high risk of surgery/embolisation) OR partially treated AVM (post-embolisation)
- **Dose:** 18-25 Gy single fraction (margin dose)
- **Outcomes:** Obliteration 60-80% at 3 years (dependent on AVM volume, dose)

**Trigeminal neuralgia:**
- **Indication:** Medically refractory trigeminal neuralgia
- **Dose:** 80-90 Gy single fraction (target: trigeminal nerve root entry zone)
- **Outcomes:** Pain relief 70-80% at 1 year (initial), 50% at 5 years (sustained)

**SRS SIDE EFFECTS:**

**Acute (within days to weeks):**
- **Headache:** Mild headache (managed with simple analgesia)
- **Nausea/vomiting:** Rare (<10%, managed with antiemetics)
- **Fatigue:** Mild fatigue (improves after treatment)
- **Seizure:** Rare (<5%, prophylactic antiepileptic if high risk)

**Subacute (weeks to months):**
- **Radiation necrosis:** Focal necrosis within high-dose region (rare, 5-10%, asymptomatic or symptomatic (headache, neurological deficit))
- **Peritumoural oedema:** Focal oedema around treated lesion (10-20%, asymptomatic or symptomatic (headache, neurological deficit))
- **Management:** Corticosteroids (dexamethasone 4-8 mg/day) if symptomatic, consider surgical resection or laser interstitial thermal therapy (LITT) if refractory

**Late (months to years):**
- **Cranial nerve palsy:** Rare (<5%, dependent on dose, nerve proximity)
- **Cognitive dysfunction:** Rare (<5%, reduced compared to WBRT)
- **Second malignancy:** Rare (<1% at 10 years)

**SRS VS. SURGERY:**

**Brain metastases:**
- **SRS:** Non-invasive, treats multiple lesions, outpatient (day case), shorter recovery
- **Surgery:** Invasive, treats single lesion (or few large lesions), inpatient (hospital stay 3-7 days), immediate symptom relief (mass effect), tissue diagnosis

**Decision-making:**
- **SRS preferred:** Multiple lesions, deep-seated lesions, poor surgical candidate, patient preference
- **Surgery preferred:** Large lesion (>3-4 cm), symptomatic mass effect (raised intracranial pressure), diagnostic uncertainty (biopsy required)

**SRS + WBRT VS. SRS ALONE:**

**SRS alone:**
- **Advantages:** Preserves cognitive function, fewer side effects
- **Disadvantages:** Higher risk of new brain metastases (salvage SRS or WBRT at progression)

**SRS + WBRT:**
- **Advantages:** Reduces risk of new brain metastases, improves intracranial control
- **Disadvantages:** Cognitive decline (memory impairment, executive dysfunction), leukoencephalopathy

**Decision-making:**
- **SRS alone preferred:** 1-4 brain metastases, good performance status, limited extracranial disease
- **SRS + WBRT considered:** Numerous brain metastases (>4), poor prognostic factors (short survival)

**Sources:** NICE Guidelines (NG76), ASTRO Guidelines, EANO Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines (NG76)", "ASTRO Guidelines", "EANO Guidelines"]
            }
        )

    def _handle_general_radiation_oncology(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """General radiation oncology consultation"""

        return DomainQueryResult(
            domain_name="radiation_oncology",
            answer="""**RADIATION ONCOLOGY**

Radiation oncology is a medical specialty that uses ionizing radiation to treat cancer (curative or palliative).

**RADIOTHERAPY MODALITIES:**

**EXTERNAL BEAM RADIOTHERAPY (EBRT):**
- **3D-CRT:** 3-dimensional conformal radiotherapy (multiple beams shaped to tumour)
- **IMRT:** Intensity-modulated radiotherapy (modulated beam intensity)
- **VMAT:** Volumetric modulated arc therapy (rotational delivery with modulated beam intensity)
- **IGRT:** Image-guided radiotherapy (daily imaging for target verification)
- **SABR/SBRT:** Stereotactic ablative body radiotherapy (high dose, few fractions)
- **SRS:** Stereotactic radiosurgery (high dose, single or few fractions, brain)

**BRACHYTHERAPY:**
- **LDR:** Low-dose rate brachytherapy (permanent implantation, e.g., prostate seeds)
- **HDR:** High-dose rate brachytherapy (temporary afterloading, e.g., gynaecological cancer)
- **PDR:** Pulsed dose rate brachytherapy (hourly pulses over several days)

**SYSTEMIC RADIOTHERAPY:**
- **Radionuclide therapy:** Radioactive isotopes administered systemically (e.g., iodine-131 for thyroid cancer, radium-223 for prostate cancer bone metastases)

**RADIOTHERAPY TECHNIQUES:**

**SIMULATION:**
- **CT simulation:** Planning CT scan for target volume delineation and dose calculation
- **Immobilisation:** Customised devices (thermoplastic mask, vac-lok) to ensure reproducibility
- **Image fusion:** PET-CT or MRI fusion for accurate target delineation

**TREATMENT PLANNING:**
- **GTV (Gross Tumour Volume):** Visible tumour (clinical examination + imaging)
- **CTV (Clinical Target Volume):** GTV + margin for microscopic disease
- **PTV (Planning Target Volume):** CTV + margin for setup error and organ motion
- **OAR (Organs at Risk):** Normal tissues with dose constraints (e.g., spinal cord, lungs, heart, parotid glands)

**DOSE PRESCRIPTION:**
- **Curative:** 60-80 Gy (2 Gy per fraction, 5 fractions per week for 6-8 weeks)
- **Palliative:** 8-20 Gy (single fraction or few fractions)
- **SABR/SBRT:** High dose (30-60 Gy) in few fractions (1-5 fractions)

**SIDE EFFECTS:**

**Acute (during radiotherapy):**
- **Skin:** Erythema, dry/moist desquamation
- **Mucosa:** Mucositis (painful oral mucosa, ulceration)
- **Gastrointestinal:** Diarrhoea, proctitis
- **Genitourinary:** Cystitis, dysuria
- **Haematological:** Leucopenia, thrombocytopenia, anaemia
- **General:** Fatigue

**Late (months to years after radiotherapy):**
- **Fibrosis:** Tissue hardening, reduced mobility
- **Xerostomia:** Dry mouth (salivary gland dysfunction)
- **Telangiectasia:** Dilated blood vessels
- **Organ dysfunction:** Heart, lungs, liver, kidneys (dose-dependent)
- **Second malignancy:** Rare (<1% at 10 years)

**COMMON CANCERS TREATED WITH RADIOTHERAPY:**

**Curative:**
- **Breast cancer:** Whole breast radiotherapy after breast-conserving surgery
- **Prostate cancer:** EBRT ± brachytherapy
- **Lung cancer:** SBRT for early-stage, chemoradiotherapy for locally advanced
- **Head and neck cancer:** IMRT (parotid sparing) ± concurrent chemotherapy
- **Cervical cancer:** EBRT + brachytherapy ± concurrent chemotherapy
- **Rectal cancer:** Pre-operative chemoradiotherapy
- **Brain tumours:** SRS (brain metastases, vestibular schwannoma, meningioma)

**Palliative:**
- **Bone metastases:** Pain relief (8 Gy single fraction or 20 Gy in 5 fractions)
- **Brain metastases:** WBRT (20 Gy in 5 fractions) OR SRS (for limited disease)
- **Spinal cord compression:** Emergency radiotherapy (8 Gy single fraction or 20 Gy in 5 fractions)
- **SVCO:** Emergency radiotherapy (20 Gy in 5 fractions)
- **Haemoptysis:** Palliative radiotherapy (10-20 Gy)
- **Bronchial obstruction:** Palliative radiotherapy (20 Gy in 5 fractions)

**CLINICAL DECISION-MAKING:**

**Curative vs. Palliative:**
- **Curative:** Aimed at cure or long-term disease control (higher dose, longer treatment)
- **Palliative:** Aimed at symptom relief (lower dose, shorter treatment)

**Radiotherapy alone vs. Chemoradiotherapy:**
- **Radiotherapy alone:** Early-stage disease, radiosensitive tumours
- **Chemoradiotherapy:** Locally advanced disease (concurrent or sequential)

**Radiotherapy vs. Surgery:**
- **Radiotherapy:** Organ preservation (e.g., larynx, breast, prostate), non-invasive
- **Surgery:** Tumour removal, immediate symptom relief, tissue diagnosis

**Sources:** NICE Guidelines, RCR Guidelines, ASTRO Guidelines""",
            confidence=0.85,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiation_oncology",
                "sources": ["NICE Guidelines", "RCR Guidelines", "ASTRO Guidelines"]
            }
        )


def create_radiation_oncology_domain():
    """Factory function for Radiation Oncology Domain"""
    return RadiationOncologyDomain()
