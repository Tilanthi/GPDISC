"""
Respiratory Medicine Domain for GPDISC
Comprehensive respiratory system consultation covering asthma, COPD, pneumonia,
and other respiratory conditions.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class RespiratoryDomain(BaseDomainModule):
    """
    Respiratory Medicine Specialist Domain

    Covers:
    - Asthma diagnosis and management
    - COPD diagnosis and management
    - Respiratory infections (pneumonia, bronchitis, TB)
    - Spirometry interpretation
    - Chest X-ray interpretation
    - Arterial blood gas analysis
    - Oxygen therapy guidance
    - Pleural disease
    - Pneumothorax
    - Pulmonary embolism
    - Lung cancer screening
    - Interstitial lung disease
    - Sleep-disordered breathing
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="respiratory",
            version="1.0.0",
            dependencies=[],
            description="Respiratory Medicine: asthma, COPD, pneumonia, TB, pleural disease, pulmonary embolism, lung cancer",
            keywords=[
                # Breathing symptoms
                "breath", "breathless", "breathlessness", "dyspnoea", "dyspnea",
                "short of breath", "shortness of breath", "wheeze", "wheezing",
                "cough", "sputum", "phlegm", "chest tightness", "chest infection",

                # Respiratory conditions
                "asthma", "copd", "chronic obstructive pulmonary disease",
                "pneumonia", "bronchitis", "chest infection", "respiratory infection",
                "tb", "tuberculosis", "pleurisy", "pleural effusion",
                "pneumothorax", "collapsed lung", "pulmonary embolism", "pe",
                "lung cancer", "mesothelioma", "fibrosis", "ild", "interstitial lung",

                # Investigations
                "spirometry", "fev1", "fvc", "peak flow", "chest x-ray", "cxr",
                "abg", "arterial blood gas", "sats", "saturation", "oxygen",
                "ctpa", "v/q scan", "bronchoscopy",

                # Respiratory anatomy
                "lung", "pulmonary", "respiratory", "airway", "bronchi", "alveoli",
                "pleura", "diaphragm", "thoracic", "ventilation", "respiration"
            ],
            capabilities=[
                "respiratory_diagnosis",
                "asthma_management",
                "copd_management",
                "respiratory_infection_treatment",
                "spirometry_interpretation",
                "chest_xray_interpretation",
                "abg_interpretation",
                "oxygen_therapy_guidance",
                "pleural_disease_management",
                "pulmonary_embolism_assessment"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Process respiratory consultation query"""
        query_lower = query.lower()

        # Spirometry interpretation
        if any(term in query_lower for term in ["spirometry", "fev1", "fvc", "peak flow"]):
            return self._handle_spirometry(query, context)

        # Asthma
        elif "asthma" in query_lower:
            return self._handle_asthma(query, context)

        # COPD
        elif any(term in query_lower for term in ["copd", "chronic obstructive"]):
            return self._handle_copd(query, context)

        # Pneumonia/chest infection
        elif any(term in query_lower for term in ["pneumonia", "chest infection", "chest infection"]):
            return self._handle_pneumonia(query, context)

        # Breathlessness/dyspnoea
        elif any(term in query_lower for term in ["breathless", "short of breath", "dyspnoea", "dyspnea"]):
            return self._handle_breathlessness(query, context)

        # Cough
        elif "cough" in query_lower and len(query_lower) < 200:  # Avoid catching everything
            return self._handle_cough(query, context)

        # Chest X-ray
        elif any(term in query_lower for term in ["chest x-ray", "cxr", "chest xray"]):
            return self._handle_chest_xray(query, context)

        # ABG
        elif any(term in query_lower for term in ["abg", "arterial blood gas", "blood gas"]):
            return self._handle_abg(query, context)

        # Oxygen/sats
        elif any(term in query_lower for term in ["oxygen", "sats", "saturation", "hypoxic"]):
            return self._handle_oxygen(query, context)

        # Pulmonary embolism
        elif any(term in query_lower for term in ["pulmonary embolism", "pe", "embolism"]):
            return self._handle_pe(query, context)

        # Pleural effusion
        elif any(term in query_lower for term in ["pleural effusion", "fluid on lung"]):
            return self._handle_pleural_effusion(query, context)

        # Pneumothorax
        elif any(term in query_lower for term in ["pneumothorax", "collapsed lung", "deflated lung"]):
            return self._handle_pneumothorax(query, context)

        # TB
        elif any(term in query_lower for term in ["tb", "tuberculosis"]):
            return self._handle_tb(query, context)

        # Lung cancer
        elif any(term in query_lower for term in ["lung cancer", "mesothelioma"]):
            return self._handle_lung_cancer(query, context)

        # General respiratory
        else:
            return self._handle_general_respiratory(query, context)

    def _handle_spirometry(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret spirometry results"""

        answer = """**Spirometry Interpretation - Respiratory Consultation**

**Understanding Spirometry Results:**

Spirometry measures:
- **FEV1** (Forced Expiratory Volume in 1 second): How much air you can forcefully exhale in 1 second
- **FVC** (Forced Vital Capacity): Total amount of air you can forcefully exhale
- **FEV1/FVC Ratio**: The proportion of FVC exhaled in the first second

**Normal Values (approximate):**
- FEV1: >80% predicted
- FVC: >80% predicted
- FEV1/FVC ratio: >0.70 (70%)

---

**Interpreting Your Results:**

**OBSTRUCTIVE Pattern (FEV1/FVC < 0.70):**
- Suggests airway obstruction (asthma, COPD)
- FEV1 severity determines obstruction grade:
  - Mild: FEV1 ≥70% predicted
  - Moderate: FEV1 60-69% predicted
  - Severe: FEV1 50-59% predicted
  - Very severe: FEV1 <50% predicted

**RESTRICTIVE Pattern (FEV1/FVC ≥ 0.70, but both FEV1 and FVC reduced):**
- Suggests lung restriction (pulmonary fibrosis, chest wall disease)
- Both FEV1 and FVC <80% predicted

**MIXED Pattern:** Features of both obstruction and restriction

---

**Reversibility Testing:**
- **Bronchodilator reversibility**: Improvement in FEV1 >12% and >200mL after bronchodilator suggests asthma
- **Poor reversibility**: Suggests COPD (smoking-related lung damage)

---

**For accurate interpretation, I need:**
1. Your actual FEV1, FVC, and FEV1/FVC values
2. Predicted values (based on age, height, sex, ethnicity)
3. Bronchodilator response (if tested)

**⚠️ RED FLAGS requiring urgent referral:**
- FEV1 <30% predicted (severe obstruction)
- Rapid decline in FEV1 over time
- Normal spirometry but significant symptoms

---

**Confidence:** Provide actual spirometry values for personalized interpretation
**Sources:** BTS/ERS Spirometry Guidelines 2021, NICE NG161
**Next:** If you share actual results, I can provide detailed interpretation"""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.88,
            metadata={
                "topic": "spirometry_interpretation",
                "requires_actual_results": True,
                "red_flags": ["FEV1 <30% predicted", "rapid FEV1 decline"]
            }
        )

    def _handle_asthma(self, query: str, context: dict) -> DomainQueryResult:
        """Asthma diagnosis and management"""

        answer = """**Asthma Consultation - Respiratory Medicine**

**What is Asthma?**

Asthma is a chronic inflammatory condition of the airways causing:
- Reversible airway obstruction
- Airway hyperresponsiveness
- Underlying inflammation

**Common Symptoms:**
- Wheeze (whistling chest sound)
- Cough (often worse at night or with exercise)
- Chest tightness
- Shortness of breath (often episodic)
- Variable symptoms from day-to-day

---

**Diagnosis of Asthma:**

**Clinical Diagnosis (based on symptom patterns):**
- Episodic wheeze, cough, breathlessness, chest tightness
- Symptoms worse at night/early morning
- Triggered by exercise, allergens, cold air, irritants
- Family history of asthma/atopy
- Improvement with bronchodilator (reliever inhaler)

**Investigations:**
- **Spirometry** (age 5+): Obstructive pattern with reversibility
- **FeNO** (Fractional exhaled NO): >35ppb suggests eosinophilic inflammation
- **Peak flow diary**: Variability >20% supports diagnosis
- **Skin prick tests**: For allergic sensitization

---

**Asthma Severity Classification:**

**Symptom Control (over last 4 weeks):**
- **Well controlled**: None of these twice/week or less
- **Partly controlled**: Any of these more than twice/week
- **Uncontrolled**: Any of these + night waking + rescue needed daily

**Exacerbations:**
- **Mild**: Short-acting bronchodilator only needed
- **Moderate**: Requires systemic steroids
- **Severe:** Emergency admission/PCP attendance

---

**Asthma Treatment:**

**1. Reliever Inhaler (SABA - Short-acting beta-agonist)**
- Salbutamol/Albuterol 100-200mc per puff
- Use as needed for symptom relief
- No more than 4-6 puffs per day indicates good control

**2. Preventer Inhaler (ICS - Inhaled corticosteroid)**
- Beclometasone, Budesonide, Fluticasone, Mometasone
- Used regularly (usually twice daily)
- Reduces inflammation and prevents symptoms
- Dose depends on severity

**3. Combination Inhaler (LABA + ICS)**
- Salmeterol/Fluticasone (Seretide)
- Formoterol/Budesonide (Symbicort)
- For moderate-severe asthma or poor control

**4. Additional Agents:**
- **LTRA** (Leukotriene receptor antagonist): Montelukast
- **LAMA** (Long-acting muscarinic antagonist): Tiotropium
- **Biologics**: Omalizumab, Mepolizumab (for severe refractory)

---

**Asthma Action Plan Essentials:**

**GREEN (Good Control):**
- Continue preventer
- Use reliever <4 times/week
- No night symptoms
- Normal activities

**YELLOW (Warning Signs):**
- Daytime symptoms increasing
- Reliever use increasing
- Night cough/wheeze
- Reduce triggers, double preventer for 7-14 days

**RED (Severe Attack):**
- Too breathless to speak in sentences
- Reliever not helping or lasting <4 hours
- **SEEK URGENT MEDICAL CARE**

---

**Triggers to Avoid/Minimize:**
- Tobacco smoke (absolutely contraindicated)
- Allergens (house dust mite, pets, pollen)
- Cold air
- Exercise-induced (use pre-exercise SABA 15min before)
- Irritants (perfumes, cleaning products)
- Certain medications (NSAIDs, beta-blockers) - **CHECK FIRST**

---

**Monitoring:**
- Regular reviews (at least annually)
- Peak flow monitoring during exacerbations
- Inhaler technique check
- Review of control level

---

**⚠️ EMERGENCY SIGNS - Seek immediate care:**
- Inability to complete sentences
- Blue lips or confusion
- Exhaustion from respiratory effort
- No improvement from reliever after 10-15 minutes
- Peak flow <50% personal best

---

**Confidence:** 0.92
**Sources:** BTS/SIGN British Guideline on Asthma 2024, GINA 2025
**Note:** This is general information. Personalized treatment requires proper diagnosis and monitoring by healthcare provider."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.92,
            metadata={
                "topic": "asthma",
                "condition": "asthma",
                "emergency_signs": ["Inability to speak", "Cyanosis", "Exhaustion", "No reliever response"],
                "red_flags": ["Frequent reliever use", "Night symptoms"]
            }
        )

    def _handle_copd(self, query: str, context: dict) -> DomainQueryResult:
        """COPD diagnosis and management"""

        answer = """**COPD Consultation - Respiratory Medicine**

**What is COPD?**

**C**hronic **O**bstructive **P**ulmonary **D**isease - progressive, poorly reversible airway limitation usually caused by smoking.

**Key Features:**
- Chronic progressive breathlessness
- Chronic cough (often "smoker's cough")
- Sputum production (especially mornings)
- History of smoking (typically >10 pack-years)
- Age >35 years usually
- Chronic exposure to other irritants (biomass, occupational)

**NOT asthma:** Limited/no reversibility with bronchodilators

---

**COPD Diagnosis:**

**Spirometry (Post-bronchodilator):**
- FEV1/FVC ratio <0.70 (confirmed after bronchodilator)
- FEV1 <80% predicted
- Poor reversibility (<12% improvement after bronchodilator)

**GOLD Grading (FEV1 % predicted):**
- **GOLD 1 (Mild):** FEV1 ≥80%
- **GOLD 2 (Moderate):** FEV1 50-79%
- **GOLD 3 (Severe):** FEV1 30-49%
- **GOLD 4 (Very Severe):** FEV1 <30%

**Symptom Assessment (CAT score):**
- Cough, phlegm, chest tightness, breathlessness
- Activity limitation, confidence
- Outdoor restriction, sleep disturbance
- Score 0-40: Higher = worse symptoms

---

**COPD Treatment - Stepwise Approach:**

**ALL PATIENTS:**
1. **Smoking cessation** - SINGLE MOST IMPORTANT intervention
   - Varenicline, Bupropion, NRT available
   - Counselling and support crucial

2. **Vaccinations:**
   - **Influenza:** Annually
   - **Pneumococcal:** PCV13 then PPSV23
   - **COVID-19:** As per guidelines
   - **RSV/Shingles:** Age-appropriate

3. **Short-acting bronchodilator (SABA or SAMA):**
   - Salbutamol or Ipratropium as needed
   - For symptom relief, NOT prevention

---

**MODERATE-TO-SEVERE COPD (Regular symptoms):**

**LAMA (Long-acting muscarinic antagonist):**
- Tiotropium (HandiHaler) once daily
- Glycopyrronium (Breo) once daily
- Umeclidinium (Incruse) once daily
- Improves symptoms and reduces exacerbations

**OR LABA (Long-acting beta-agonist):**
- Salmeterol, Formoterol, Indacaterol, Olodaterol

**Preferred: LABA + LAMA combination:**
- Symbicort (Formoterol + Tiotropium)
- Anoro (Umeclidinium + Vilanterol)
- Dual bronchodilation is superior to single agents

---

**SEVERE COPD or Frequent Exacerbations:**

**Add ICS (Inhaled corticosteroid):**
- Triple therapy: LABA + LAMA + ICS
- Reduces exacerbations by ~20%
- **Risk:** Pneumonia (caution in eosinophils)

---

**EXACERBATION MANAGEMENT:**

**Home Management Plan:**
1. **Increase reliever** (4-6 puffs as needed)
2. **Increase preventer** (double for 7-14 days)
3. **Start antibiotics + steroids** if:
   - Increased sputum purulence
   - Increased sputum volume
   - Increased breathlessness

**Common Regimen:**
- **Prednisolone:** 30-40mg daily for 5 days
- **Doxycycline:** 100mg BD for 5-7 days OR
- **Amoxicillin:** 500mg TDS for 5-7 days
- **Azithromycin:** 500mg daily for 3 days (if penicillin allergy)

**⚠️ Seek urgent care if:**
- Too breathless to leave house
- Confusion or drowsiness
- Cyanosis (blue lips/face)
- No improvement with home management
- sats <92% (if oximeter available)

---

**Oxygen Therapy:**
- Indicated if sats <92% on room air
- Target: 88-92% (NOT 100% in COPD)
- Assessment for long-term oxygen if sats persistently low
- 18+ hours/day improves survival in hypoxemic COPD

---

**Non-Drug Management:**

**Pulmonary Rehabilitation:**
- Exercise training
- Education
- Nutrition advice
- Breathing techniques
- Proven to improve symptoms and quality of life

**Breathing Techniques:**
- Pursed-lip breathing (reduces air trapping)
- Recovery position (forward lean, elbows on knees)
- Active cycle of breathing technique

**Nutrition:**
- BMI <20: Underweight, increased mortality
- BMI >30: Increased dyspnoea
- Balance diet with adequate protein

---

**PROGNOSIS:**

**Life Expectancy:**
- Mild COPD: Near-normal
- Moderate: Reduced by ~3-5 years
- Severe: Reduced by ~8-10 years
- Very severe: Median survival 3-4 years

**Disease Progression:**
- Smoking cessation slows but doesn't stop progression
- Rate of decline: 30-50ml FEV1/year (variable)
- Exacerbations accelerate decline

---

**⚠️ RED FLAGS requiring urgent review:**
- Rapidly increasing breathlessness
- New chest pain
- Hemoptysis (coughing blood)
- Confusion or behavioral changes
- Cor pulmonale signs (swollen ankles, right heart failure)

---

**Confidence:** 0.90
**Sources:** GOLD COPD Guidelines 2024, NICE NG115
**Note:** COPD management requires regular review and adjustment. Smoking cessation is the single most important intervention."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.90,
            metadata={
                "topic": "copd",
                "condition": "chronic_obstructive_pulmonary_disease",
                "emergency_signs": ["Too breathless to leave house", "Confusion", "Cyanosis", "No improvement"],
                "smoking_cessation_critical": True
            }
        )

    def _handle_pneumonia(self, query: str, context: dict) -> DomainQueryResult:
        """Pneumonia assessment and management"""

        answer = """**Pneumonia Assessment - Respiratory Consultation**

**⚠️ MEDICAL ATTENTION MAY BE REQUIRED - This is general information only**

---

**What is Pneumonia?**

Infection of the lung parenchyma (alveoli) causing:
- Consolidation (fluid/pus in air sacs)
- Impaired gas exchange
- Systemic inflammatory response

**Types:**
- **Community-acquired (CAP):** Acquired outside hospital
- **Hospital-acquired (HAP):** Developed after 48h admission
- **Aspiration:** Related to inhaling gastric contents
- **Atypical:** Different pathogens (Mycoplasma, Legionella)

---

**Typical Symptoms:**

**Respiratory:**
- Cough (productive with purulent sputum)
- Shortness of breath (dyspnoea)
- Pleuritic chest pain (sharp, worse on inspiration)
- Hemoptysis (rusty or blood-streaked sputum)

**Systemic:**
- Fever (usually >38°C)
- Rigors (shaking chills)
- Malaise, fatigue
- Myalgia (muscle aches)
- Anorexia, nausea

---

**CRB-65 Severity Score (for CAP):**

Each factor = 1 point:

| Factor | Points |
|--------|--------|
| **C**onfusion: New confusion | 1 |
| **R**espiratory rate: ≥30/min | 1 |
| **B**lood pressure: <90 systolic OR ≤60 diastolic | 1 |
| **6**5 years: Age ≥65 | 1 |

**Score Interpretation:**
- **0-1:** Low risk - Manage at home
- **2:** Moderate - Hospital admission considered
- **3-4:** High - Hospital admission required
- **5:** Very high - Consider critical care

---

**Diagnosis:**

**Chest X-ray:** consolidation (white opacity) - **Required for diagnosis**

**Blood Tests:**
- **FBC:** Leukocytosis (elevated WBC)
- **CRP:** Elevated inflammatory marker
- **U&Es:** Hydration, kidney function
- **LFTs:** Baseline, may show hepatic involvement

**Microbiology:**
- **Sputum culture** (if productive cough)
- **Blood cultures** (if severe)
- **Urinary antigens** (Legionella, Pneumococcal)

---

**Treatment of Community-Acquired Pneumonia:**

**LOW SEVERITY (CRB-65 0-1, home treatment):**

**Antibiotics (choose one):**

**Option 1 (5-day course):**
- **Amoxicillin:** 500mg TDS for 5 days

**Option 2 (if penicillin allergy):**
- **Doxycycline:** 100mg BD for 5 days

**Option 3 (if atypical suspected):**
- **Amoxicillin + Macrolide:**
  - Amoxicillin 500mg TDS
  - Doxycycline 100mg BD OR Clarithromycin 500mg BD

---

**MODERATE-TO-HIGH SEVERITY (hospital admission):**

**Severe CAP (CURB-65 2-5):**

**Co-amoxiclav:** 1.2g TDS + **Macrolide:** Clarithromycin 500mg BD

OR

**Ceftriaxone:** 2g IV/IM OD + **Macrolide**

---

**Severe CAP (ITU level):**

**Ceftriaxone 2g IV** + **Clarithromycin 500mg IV** ± **Vancomycin** (if MRSA risk)

---

**Supportive Treatment:**

**Hydration:** 2-3L/day (if no contraindication)

**Analgesia:** Paracetamol for fever/pain
- **AVOID NSAIDs** (can worsen infection)

**Cough suppressant:** Not recommended (impairs sputum clearance)

**Bronchodilators:** If underlying COPD/asthma

**Physiotherapy:** Chest percussion, postural drainage

---

**When to Admit:**

**Mandatory admission:**
- CRB-65 score ≥3
- sats <92% on room air
- Systolic BP <90 or diastolic <60
- Confusion
- Inability to tolerate oral intake
- Severe social circumstances

**Consider admission:**
- CRB-65 score 2
- Significant comorbidities
- Pregnancy
- Age >75 with significant symptoms
- Failure of home treatment

---

**Complications:**

**Empyema:** Infected pleural fluid (requires drainage)
**Lung abscess:** Cavitation, usually alcoholics/aspiration
**Sepsis:** Life-threatening organ dysfunction
**Respiratory failure:** Requires ventilatory support

---

**Prevention:**

**Vaccination:**
- **Pneumococcal:** PCV13 → PPSV23 (8 weeks later)
- **Influenza:** Annually
- **COVID-19:** As per guidelines
- **Hib/Whooping cough:** As appropriate

---

**⚠️ EMERGENCY - Call 999/911 if:**
- Severe breathlessness at rest
- Unable to speak in full sentences
- Confusion or drowsiness
- Cyanosis (blue lips/face)
- Chest pain
- sats <92%
- Hemoptysis (coughing significant blood)

---

**Follow-up:**

**Repeat CXR:** 6 weeks post-diagnosis (especially if aged 50+, smoker)
**Clinical review:** Ensure resolution
**Investigate underlying cause:** Consider bronchoscopy if recurrent

---

**Confidence:** 0.91
**Sources:** BTS Pneumonia Guidelines 2024, NICE NG191
**Important:** This is general information. Pneumonia requires proper clinical assessment and may need hospital treatment. severity assessment (CRB-65) should be performed by healthcare professional."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.91,
            metadata={
                "topic": "pneumonia",
                "condition": "community_acquired_pneumonia",
                "severity_assessment": "CRB-65",
                "emergency_signs": ["sats <92%", "confusion", "severe breathlessness"]
            }
        )

    def _handle_breathlessness(self, query: str, context: dict) -> DomainQueryResult:
        """Breathlessness/dyspnoea assessment"""

        answer = """**Breathlessness Assessment - Respiratory Consultation**

**⚠️ If this is acute or severe, seek urgent medical care**

---

**Understanding Breathlessness (Dyspnoea)**

Breathlessness is a subjective sensation of difficult, uncomfortable breathing. It can range from mild exertional dyspnoea to life-threatening respiratory distress.

---

**Key Questions for Assessment:**

**1. Onset:**
- **Acute (minutes-hours):** Pulmonary embolism, pneumothorax, acute asthma, pulmonary edema, pneumonia, foreign body
- **Subacute (days-weeks):** Pneumonia, pleural effusion, worsening heart failure, COPD exacerbation
- **Chronic (months-years):** COPD, pulmonary fibrosis, chronic heart failure, deconditioning

**2. Triggers:**
- Exertional: Cardiac, respiratory deconditioning
- Positional: Orthopnea (heart failure), trepopnea (pleural effusion)
- Resting: Usually significant disease

**3. Associated Symptoms:**
- Chest pain → Cardiac, PE, pneumothorax
- Cough → Respiratory infection, COPD
- Wheeze → Asthma, COPD, heart failure
- Fever → Infection
- Swollen ankles → Heart failure

**4. Risk Factors:**
- Smoking → COPD, lung cancer, cardiovascular disease
- Heart disease → Heart failure, arrhythmia
- Recent travel → PE (DVT risk)
- Recent surgery → PE risk

---

**Common Causes of Breathlessness:**

**RESPIRATORY:**
- **Asthma:** Episodic, wheeze, trigger-related
- **COPD:** Progressive, smokers, chronic
- **Pneumonia:** Acute, fever, cough
- **Pulmonary embolism:** Acute, pleuritic pain, DVT risk
- **Pneumothorax:** Acute, sharp pain, tall thin young men
- **Pleural effusion:** Progressive, underlying malignancy/infection
- **Interstitial lung disease:** Progressive, dry cough, clubbing
- **Lung cancer:** Progressive, weight loss, smokers

**CARDIAC:**
- **Heart failure:** Exertional, orthopnea, PND, ankle swelling
- **Arrhythmia:** Palpitations, intermittent
- **Ischemic heart disease:** Exertional, chest pain, risk factors
- **Valve disease:** Gradual onset, murmur

**OTHER:**
- **Anemia:** Progressive fatigue, pallor
- **Anxiety:** Hyperventilation, tingling, panic
- **Deconditioning:** Chronic lack of fitness
- **Obesity:** Exertional, weight-related
- **Thyrotoxicosis:** Anxiety, heat intolerance, tremor

---

**Urgency Assessment:**

**⚠️ IMMEDIATE (999/911) for:**
- sats <92% (if oximeter available)
- Unable to speak in full sentences
- Chest pain
- Acute confusion
- Rapid onset (minutes-hours) with high risk
- Known significant cardiac/respiratory disease

**⚠️ URGENT (same day) for:**
- sats 92-94%
- Recent onset (days)
- Known heart/lung disease with worsening
- Fever with breathlessness
- Recent DVT risk factor (surgery, travel, immobilization)

---

**Investigation Approach:**

**1. Assessment:**
- Observations: sats, respiratory rate, heart rate, BP, temperature
- Examination: chest expansion, breath sounds, heart sounds, ankles
- Risk stratification: comorbidities, medications

**2. Investigations (often needed):**
- **Chest X-ray:** First-line for most causes
- **ECG:** Cardiac causes
- **Blood tests:** FBC, U&Es, CRP, D-dimer (if PE suspected), BNP
- **Spirometry:** If obstructive airway disease suspected
- **CTPA:** If PE suspected (D-dimer positive)
- **Echocardiogram:** If heart failure suspected

---

**Self-Care While Awaiting Review:**

**Positioning:**
- Sit upright (reduces breathlessness)
- Lean forward (helps with pleural effusion)
- Fresh air if possible

**Breathing Techniques:**
- Pursed-lip breathing (breathe out through pursed lips)
- Recovery position (sit, lean forward with elbows on knees)
- Relax shoulders, don't hunch

**Avoid:**
- Exertion
- Smoking (absolutely)
- Triggers identified (dust, fumes, allergens)
- NSAIDs (can worsen some conditions)

---

**Red Flag Signs:**

- sats <92% on room air
- Respiratory rate >25/min
- Heart rate >120/min
- Systolic BP <90 mmHg
- New confusion
- Inability to speak in sentences
- Chest pain
- Hemoptysis

If any present → **SEEK URGENT MEDICAL CARE**

---

**Confidence:** 0.87
**Sources:** NICE NG121 Breathlessness, BTS Dyspnoea Guidelines
**Note:** Breathlessness requires proper clinical assessment. This is general guidance - actual diagnosis requires examination and investigations."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.87,
            metadata={
                "topic": "breathlessness",
                "red_flags": ["sats <92%", "unable to speak", "chest pain", "confusion"],
                "emergency_signs": ["sats <92%", "respiratory rate >25/min", "new confusion"]
            }
        )

    def _handle_chest_xray(self, query: str, context: dict) -> DomainQueryResult:
        """Chest X-ray interpretation basics"""

        answer = """**Chest X-ray Interpretation - Respiratory Consultation**

**⚠️ Disclaimer:** CXR interpretation requires expertise. This is general guidance only.

---

**Understanding Chest X-ray Views:**

**PA (Posteroanterior):**
- Standard view, taken from front to back
- Heart appears normal size
- Best for most pathology

**Lateral:**
- Taken from side
- Shows areas hidden on PA (behind heart, diaphragm)
- Used for confirmation and localization

---

**Normal CXR Features:**

**Lungs:**
- Black (air-filled), transparent
- Vascular markings visible but fade out
- No opacities or consolidations

**Heart:**
- Width <50% thoracic width
- Left border formed by aortic arch, pulmonary artery, left ventricle
- Right border formed by right atrium

**Mediastinum:**
- Central, midline
- Width <8cm at widest
- Trachea central

**Diaphragm:**
- Right higher than left by ~1-2cm
- Sharp, well-defined
- Costophrenic angles sharp

**Bones:**
- No fractures or lytic lesions
- No bony destruction

---

**Common Abnormal Patterns:**

**CONSOLIDATION (white opacity, air bronchograms):**
- Pneumonia (lobar, bronchopneumonia)
- Pulmonary infarction (PE)
- Atelectasis (collapse)

**INTERSTITIAL (hazy, reticular, nodular):**
- Pulmonary edema (heart failure)
- Pulmonary fibrosis
- Interstitial lung disease
- Sarcoidosis

**NODULES (round opacities):**
- Solitary nodule: Cancer vs benign granuloma vs infection
- Multiple: Metastases, infection, granulomatous disease

**PLEURAL:**
- Effusion: Blunted costophrenic angle, meniscus sign
- Pneumothorax: Air in pleural space, absent lung markings

**CARDIOMEGALY:**
- Heart width >50% thoracic width
- Heart failure, hypertension, valve disease

---

**Specific Examples:**

**1. Lower Zone Consolidation + Air Bronchograms:**
- **Most likely:** Pneumonia
- **Differential:** Pulmonary infarction (PE)

**2. Bilateral Bat Wings (perihilar haziness):**
- **Most likely:** Pulmonary edema (heart failure)
- **Differential:** Pneumonia, hemorrhage

**3. Upper lobe cavitation:**
- **Most likely:** TB (if apical)
- **Differential:** Cancer, fungal infection

**4. Solitary peripheral nodule <3cm:**
- **Need:** CT follow-up or investigation
- **Risk:** Higher if smoker, older, larger

**5. Complete white-out of hemithorax:**
- **Causes:** Massive effusion, complete collapse (obstruction), pneumonectomy

---

**Importance of Old CXRs:**
- Comparison is crucial
- New vs. old changes
- Rate of change

---

**⚠️ RED FLAGS on CXR:**

- Large mass (>3cm) or significant enlargement
- Effusion (pleural fluid)
- Pneumothorax (collapsed lung)
- Cardiac enlargement (new)
- Widened mediastinum
- Bone destruction or fractures
- Foreign body

---

**Limitations of CXR:**

- Normal doesn't exclude pathology (e.g., early PE, small cancers)
- Poor sensitivity for interstitial disease
- Superimposition can hide lesions
- CT required for clarification

---

**Confidence:** 0.75 (requires radiologist for definitive interpretation)
**Sources:** Radiopaedia.org, BTS Chest Imaging Guidelines
**Important:** All CXRs should be reviewed by radiologist. This is general guidance for educational purposes only."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.75,
            metadata={
                "topic": "chest_xray_interpretation",
                "requires_specialist_review": True,
                "red_flags": ["mass >3cm", "effusion", "pneumothorax", "cardiomegaly"]
            }
        )

    def _handle_abg(self, query: str, context: dict) -> DomainQueryResult:
        """Arterial blood gas interpretation"""

        answer = """**Arterial Blood Gas (ABG) Interpretation - Respiratory Consultation**

**⚠️ Clinical correlation required - Values change rapidly**

---

**Normal ABG Ranges (on room air):**

| Parameter | Normal Range |
|-----------|--------------|
| **pH** | 7.35 - 7.45 |
| **PaO2** | 10.6 - 13.3 kPa (80-100 mmHg) |
| **PaCO2** | 4.7 - 6.0 kPa (35-45 mmHg) |
| **HCO3-** | 22 - 26 mmol/L |
| **Base Excess** | -2 to +2 |
| **SaO2** | >94% |
| **Lactate** | <2.0 mmol/L |

---

**Step-by-Step Interpretation:**

**STEP 1: pH (Acid-Base Status)**
- **<7.35:** Acidemia
- **7.35-7.45:** Normal
- **>7.45:** Alkalemia

**STEP 2: PaCO2 (Respiratory Component)**
- **<4.7 kPa:** Hyperventilation (respiratory alkalosis)
- **4.7-6.0 kPa:** Normal
- **>6.0 kPa:** Hypoventilation (respiratory acidosis)

**STEP 3: HCO3- (Metabolic Component)**
- **<22:** Metabolic acidosis
- **22-26:** Normal
- **>26:** Metabolic alkalosis

**STEP 4: PaO2 (Oxygenation)**
- **<8.0 kPa:** Hypoxemia (requires oxygen)
- **8.0-10.6 kPa:** Mild hypoxemia
- **>10.6 kPa:** Normal

---

**Common Patterns:**

**1. Respiratory Acidosis (Acute):**
- pH ↓, PaCO2 ↑, HCO3- normal (initially)
- **Causes:** COPD exacerbation, respiratory failure, drug overdose
- **Compensation:** Kidneys retain HCO3- (takes 3-5 days)

**2. Respiratory Alkalosis (Acute):**
- pH ↑, PaCO2 ↓, HCO3- normal
- **Causes:** Anxiety, pain, hypoxia (driving hyperventilation), PE
- **Compensation:** Kidneys excrete HCO3-

**3. Metabolic Acidosis:**
- pH ↓, PaCO2 ↓ or normal, HCO3- ↓
- **Causes:** Sepsis, DKA, renal failure, lactic acidosis, diarrhea
- **Compensation:** Hyperventilation (blows off CO2)

**4. Metabolic Alkalosis:**
- pH ↑, PaCO2 ↑ or normal, HCO3- ↑
- **Causes:** Vomiting, diuretics, hypokalemia
- **Compensation:** Hypoventilation (retains CO2)

**5. Mixed Disorders:**
- pH may be normal but PaCO2 and HCO3- abnormal
- Example: COPD (chronic respiratory acidosis) + DKA (metabolic acidosis)

---

**Clinical Scenarios:**

**COPD Exacerbation (Acute-on-Chronic):**
- pH may be normal (compensated)
- PaCO2 elevated (maybe 6-8 kPa or higher)
- HCO3- elevated (renal compensation)
- **Target sats:** 88-92% (NOT normal!)
- **NIV (Non-invasive ventilation):** May be indicated

**Type 2 Respiratory Failure (COPD):**
- PaO2 <8.0 kPa + PaCO2 >6.0 kPa
- **Caution:** Controlled hypoxemia (target sats 88-92%)
- **Oxygen caution:** Too much O2 can worsen hypercapnia

**ARDS (Acute Respiratory Distress Syndrome):**
- Severe hypoxemia refractory to oxygen
- PaO2/FiO2 ratio <200
- Bilateral infiltrates on CXR
- No cardiac cause

---

**Oxygenation Indices:**

**PaO2/FiO2 Ratio:**
- **Mild:** 200-300
- **Moderate:** 150-200
- **Severe:** <150 (ARDS if <200 with bilateral infiltrates)

**A-a Gradient (Alveolar-arterial):**
- Increased in VQ mismatch, shunt
- Normally <15 mmHg (increases with age)

---

**When to Act on ABG:**

⚠️ **Immediate intervention required:**
- pH <7.2 or >7.6
- PaO2 <6.7 kPa despite oxygen
- PaCO2 >8.0 kPa with respiratory acidosis
- Lactate >4.0 mmol/L

---

**Limitations:**
- Snapshot in time - values change rapidly
- Arterial (not venous) required
- Temperature correction may be needed
- Clinical correlation essential

---

**Confidence:** 0.85
**Sources:** BTS ABG Interpretation Guidelines, Critical Care Tutorials
**Important:** ABG interpretation must be combined with clinical assessment. This is general guidance for educational purposes."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.85,
            metadata={
                "topic": "abg_interpretation",
                "laboratory_test": "arterial_blood_gas",
                "red_flags": ["pH <7.2 or >7.6", "PaO2 <6.7", "PaCO2 >8.0 with acidosis", "lactate >4"]
            }
        )

    def _handle_oxygen(self, query: str, context: dict) -> DomainQueryResult:
        """Oxygen therapy guidance"""

        answer = """**Oxygen Therapy Guidance - Respiratory Consultation**

---

**Oxygen Saturation Targets:**

**General Population:**
- Normal sats: 96-98% on room air
- Hypoxemia: sats <94%
- **Target:** 94-98% (NOT 100%)

**COPD (Type 2 Respiratory Failure):**
- **Target:** 88-92% (controlled hypoxemia)
- **Caution:** High-flow O2 can cause CO2 retention (hypercapnia)
- **Monitor:** Blood gases if concerned

**Acute Illness (pneumonia, PE, etc.):**
- **Target:** 94-98% initially
- May need higher targets if very ill

**End-of-Life / Palliative:**
- Comfort rather than normal sats
- Target patient comfort rather than numbers

---

**Oxygen Delivery Devices:**

**Low Flow (24-40% O2):**
- **Nasal cannula (1-2 L/min):** ~24-28% O2
  - Comfortable, eating/talking possible
  - FiO2 increases ~4% per L
- **Simple face mask (5-10 L/min):** ~35-50% O2
  - Higher FiO2 but less comfortable
  - Cannot eat/talk

**High Flow (>40% O2):**
- **Venturi mask (blue 24%, pink 28%, yellow 35%, white 50%):**
  - Fixed FiO2 regardless of flow rate (up to 15 L/min)
  - Precise oxygen delivery
  - Good for COPD (controlled oxygen)

**Reservoir mask:**
- **Non-rebreather (15 L/min):** ~80-90% O2
  - Highest FiO2 without mechanical ventilation
  - Tight seal required
  - Used in severe hypoxemia

**High Flow Nasal Cannula:**
- Heated, humidified
- Up to 60 L/min, FiO2 21-100%
- For respiratory failure (sometimes ICU-level care)

---

**When to Start Oxygen:**

**General guidance:**
- sats <94% on room air
- Acute illness with sats <92%
- Known chronic hypoxemia

**Cautious approach:**
- Start at 24-28% (1-2 L/min nasal cannula)
- Target sats 94-98% (88-92% in COPD)
- Titrate based on response and ABG

---

**Monitoring on Oxygen:**

**Check:**
- sats (continuous or regular spot checks)
- Breathing pattern
- Mental status (confusion = CO2 retention?)
- Work of breathing

**If concerned about COPD:**
- **ABG after 30-60 minutes** on oxygen
- Check PaCO2 (if >8-10 kPa, reduce oxygen)
- May need NIV (non-invasive ventilation)

---

**Dangers of Oxygen:**

**In COPD (Type 2 Respiratory Failure):**
- Oxygen can suppress respiratory drive
- CO2 retention → hypercapnia → respiratory acidosis
- Can cause CO2 narcosis (drowsiness → coma)
- **WHY target sats are lower (88-92%) in COPD**

**Fire Risk:**
- **NO SMOKING** near oxygen!
- Oxygen supports combustion
- Keep away from flames, sparks

---

**Oxygen at Home:**

**Indications for home oxygen:**
- sats <92% on room air at rest (stable)
- Exercise desaturation (<90% on ambulation)
- Pulmonary hypertension
- End-stage lung disease
- Heart failure with hypoxemia

**Equipment:**
- Oxygen concentrator (electric)
- Portable cylinders (for外出)
- Nasal cannula (usually)

**Duration:** Usually 16-24h/day for benefit

---

**Travel with Oxygen:**

**Planning needed:**
- Airlines require notification
- Extra oxygen cylinders for travel
- Insurance considerations
- Portable concentrator options

---

**⚠️ EMERGENCY signs:**
- Increasing breathlessness despite oxygen
- Confusion or drowsiness (CO2 retention?)
- sats dropping despite oxygen
- Chest pain
- Unable to tolerate oxygen

**SEEK URGENT MEDICAL CARE**

---

**Confidence:** 0.89
**Sources:** BTS Oxygen Guidelines, NICE CG134
**Important:** Oxygen prescription requires proper assessment. COPD patients need specific guidance to avoid CO2 retention."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.89,
            metadata={
                "topic": "oxygen_therapy",
                "target_sats": {
                    "general": "94-98%",
                    "copd": "88-92%"
                },
                "emergency_signs": ["increasing breathlessness", "confusion", "drowsiness"]
            }
        )

    def _handle_pe(self, query: str, context: dict) -> DomainQueryResult:
        """Pulmonary embolism assessment"""

        answer = """**Pulmonary Embolism (PE) Assessment - Respiratory Consultation**

**⚠️ PE is a medical emergency - can be life-threatening**

---

**What is Pulmonary Embolism?**

Blood clot (usually from deep vein thrombosis in leg) that travels to lungs and blocks pulmonary arteries.

**Risk Factors:**
- Recent surgery (especially orthopedic)
- Immobility (long flights, bed rest)
- Cancer (active or previous)
- Pregnancy/postpartum
- Estrogen-containing contraception
- Previous DVT/PE
- Thrombophilia (clotting disorder)
- Obesity
- Smoking

---

**Typical Symptoms:**

**Respiratory:**
- Sudden-onset shortness of breath
- Pleuritic chest pain (sharp, worse on inspiration)
- Cough (sometimes with blood-streaked sputum)
- Hemoptysis

**Systemic:**
- Tachycardia (fast heart rate >100)
- Syncope (fainting) in massive PE
- Anxiety, sense of doom
- Sweating

**Signs:**
- Tachycardia (>100/min)
- Tachypnea (>20/min)
- Low-grade fever
- Loud P2 (heart sound) if large PE

---

**Well's Criteria for PE Prediction:**

**Score 1 point each:**

| Sign | Points |
|------|--------|
| DVT symptoms | 3 |
| PE #1 likely than other diagnoses | 3 |
| Heart rate >100 | 1.5 |
| Immobilization/surgery | 1.5 |
| Previous DVT/PE | 1.5 |
| Hemoptysis | 1 |
| Cancer | 1 |

**Interpretation:**
- **Score 0-4:** PE unlikely
- **Score >4:** PE likely (requires investigation)

**Note:** Clinical gestalt can override - if high suspicion, investigate regardless of score.

---

**Investigation:**

**1. D-dimer (if PE unlikely - score ≤4):**
- Negative: PE effectively ruled out
- Positive: Requires imaging

**2. CTPA (CT Pulmonary Angiogram):**
- Gold standard investigation
- Positive if filling defect seen
- Also shows other lung pathology

**3. V/Q Scan (if CTPA contraindicated):**
- Renal impairment, contrast allergy, pregnancy
- Ventilation/perfusion mismatch

**4. CTPA:**
- Lower extremity Doppler ultrasound (if DVT suspected)

---

**PE Severity (PESI Score):**

**Age >80:** +1 point each decade (simplified)
Male: +10
Cancer: +30
Heart failure: +10
Chronic lung disease: +10
HR >110: +20
SBP <100: +30
Respiratory rate >30: +20
Temp <36°C: +20
Altered mental status: +60
O2 sat <90%: +20

**Interpretation:**
- **Low risk (0):** Outpatient management
- **High risk (>0):** Inpatient treatment

---

**Treatment of PE:**

**Low-moderate severity (hemodynamically stable):**

**Anticoagulation (start immediately if high suspicion):**

**Apixaban:** 10mg BD for 7 days, then 5mg BD
- **Preferred:** NO monitoring, safe, effective

OR

**Rivaroxaban:** 15mg BD for 21 days, then 20mg OD
- Also NO monitoring

OR

**LMWH (Low Molecular Weight Heparin):**
- Enoxaparin, Dalteparin, Tinzaparin
- Requires weight-based dosing
- Continue if warfarin chosen

**Duration of treatment:**
- **Provoked (surgery, trauma):** 3 months
- **Unprovoked:** 3-6 months (extend if risk factors persist)
- **Recurrent PE:** Indefinite anticoagulation

---

**Massive PE (hemodynamically unstable):**

**Thrombolysis:** Alteplase
- **Contraindications:** Active bleeding, recent surgery, stroke
- **Alternative:** Surgical embolectomy (rare)

---

**DVT Treatment:**

**Same anticoagulation as PE**
- LMWH or DOAC (apixaban, rivaroxaban)
- Duration: 3 months minimum

**Compression stockings:**
- Below-knee, 30-40 mmHg
- Reduce post-thrombotic syndrome

---

**Prevention:**

**Mechanical:**
- Compression stockings (if immobilized)
- Intermittent pneumatic compression (IPC)

**Chemoprophylaxis:**
- LMWH (e.g., enoxaparin 40mg daily)
- DOAC (apixaban 2.5mg BD)
- For high-risk surgical/medical patients

---

**⚠️ EMERGENCY signs:**
- Severe breathlessness
- Hemodynamic instability (low BP, shock)
- Cardiac arrest
- Massive PE (right heart strain on ECG/echo)

**SEEK IMMEDIATE MEDICAL CARE (call 999/911)**

---

**Confidence:** 0.90
**Sources:** NICE NG158 PE Guidelines, ESC PE Guidelines 2024
**Important:** PE is life-threatening and requires urgent medical assessment. Suspected PE needs immediate investigation (CTPA/VQ scan). This is general information for educational purposes."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.90,
            metadata={
                "topic": "pulmonary_embolism",
                "condition": "pe",
                "urgency": "emergency",
                "diagnostic_test": "d-dimer_wells_score_ctpa",
                "treatment": "anticoagulation"
            }
        )

    def _handle_pleural_effusion(self, query: str, context: dict) -> DomainQueryResult:
        """Pleural effusion assessment"""

        answer = """**Pleural Effusion Assessment - Respiratory Consultation**

---

**What is Pleural Effusion?**

Fluid accumulation in the pleural space (between lung and chest wall).

**Causes:**

**Transudative (clear fluid, low protein):**
- Heart failure (most common)
- Liver disease (cirrhosis)
- Nephrotic syndrome
- Hypoalbuminemia

**Exudative (cloudy, high protein):**
- Infection (pneumonia, empyema)
- Malignancy (lung cancer, mesothelioma, metastases)
- Pulmonary embolism
- TB
- Autoimmune (rheumatoid arthritis, SLE)
- Pancreatitis

---

**Symptoms:**

**Breathlessness:**
- Proportional to size of effusion
- May be asymptomatic if small/gradual

**Chest pain:**
- Pleuritic (sharp, worse on inspiration)
- Dull ache (if large)

**Other:**
- Dry cough
- Fever (if infected/empyema)
- Weight loss (if malignancy)

---

**Investigation:**

**1. Chest X-ray:**
- Blunted costophrenic angle (meniscus sign)
- Large effusion: White-out of hemithorax, mediastinal shift

**2. Ultrasound (Best first test):**
- Detects fluid, guides aspiration
- Distinguishes fluid vs. solid

**3. Pleural aspiration:**
- diagnostic tap (send samples):
  - Microscopy (cells)
  - Culture (infection)
  - Biochemistry (protein, LDH, glucose, pH)
- Therapeutic drain if large

---

**Fluid Analysis:**

**Transudate vs. Exudate (Light's Criteria):**

| Test | Transudate | Exudate |
|------|-----------|----------|
| Protein | <30g/L | >30g/L |
| LDH | <2/3 serum | >2/3 serum |
| pH | Similar to blood | Often <7.3 (infection) |

**If all 3 favor exudate → Exudate**
**If all 3 favor transudate → Transudate**

---

**Management:**

**Small effusion (<1cm depth):**
- Treat underlying cause
- Monitor clinically

**Moderate effusion (1-3cm):**
- Aspirate if diagnosis uncertain
- Treat underlying cause

**Large effusion (>3cm):**
- Therapeutic tap (drain 1-1.5L)
- Improve breathlessness
- Send fluid for analysis

**Infected/empyema:**
- **Urgent chest drain**
- IV antibiotics
- Consider surgical drainage if organized

---

**Underlying Causes:**

**Heart failure:**
- Diuretics
- Treat heart failure
- Reaccumulation common

**Malignancy:**
- CT chest (if not already done)
- Bronchoscopy if cytology negative
- Thoracoscopy if diagnosis uncertain

**Infection:**
- Antibiotics
- Drainage

**Autoimmune:**
- Treat underlying disease
- Consider steroids

---

**⚠️ EMERGENCY:**
- **Empyema:** Infected pleural fluid
- **Tension hydrothorax:** Fluid under pressure, compresses heart/lungs
- **Massive effusion:** Severe breathlessness, mediastinal shift

**SEEK URGENT CARE**

---

**Confidence:** 0.86
**Sources:** BTS Pleural Disease Guidelines 2010, NICE NG139
**Important:** All pleural effusions require investigation for underlying cause. Aspiration only after ultrasound guidance."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.86,
            metadata={
                "topic": "pleural_effusion",
                "investigation": "ultrasound_aspiration",
                "emergency": ["empyema", "tension_hydrothorax"]
            }
        )

    def _handle_pneumothorax(self, query: str, context: dict) -> DomainQueryResult:
        """Pneumothorax assessment"""

        answer = """**Pneumothorax Assessment - Respiratory Consultation**

**⚠️ Can be life-threatening - urgent assessment needed**

---

**What is Pneumothorax?**

Air in the pleural space (between lung and chest wall), causing lung collapse.

**Types:**

**Primary Spontaneous Pneumothorax:**
- No obvious cause
- Tall, thin, young males (classic presentation)
- Smoking (strong risk factor)
- Can occur at rest or during exertion

**Secondary Spontaneous Pneumothorax:**
- Underlying lung disease
- COPD (most common cause)
- Asthma, CF, pulmonary fibrosis
- Lung cancer
- TB, pneumonia

**Traumatic Pneumothorax:**
- Rib fracture
- Penetrating injury
- Iatrogenic (central line, lung biopsy, mechanical ventilation)

---

**Symptoms:**

**Sudden onset:**
- Sharp chest pain (pleuritic)
- Shortness of breath
- Unilateral symptoms

**Severity depends on:**
- Size of pneumothorax
- Underlying lung function
- Presence of tension (life-threatening)

---

**Examination Findings:**

**Mild/Moderate:**
- Reduced breath sounds on affected side
- Reduced chest expansion
- Hyper-resonant to percussion (tapping)

**Severe/Tension:**
- Tachycardia (>120/min)
- Hypotension (low blood pressure)
- Deviated trachea (away from affected side)
- Distended neck veins
- Cyanosis
- Cardiac arrest (if untreated)

---

**Investigation:**

**Chest X-ray (upright expiratory film):**
- **Small:** Visible at apex only
- **Moderate:** Visible at apex + visible lung edge
- **Large:** Complete collapse with mediastinal shift

**CT Chest:**
- More sensitive than CXR
- Shows small pneumothorax
- Identifies underlying lung disease

---

**Pneumothorax Size Grading:**

**Small:** <2cm from apex to cupola
**Moderate:** 2-4cm from apex to cupola
**Large:** >4cm from apex to cupola

---

**Management:**

**Small Pneumothorax (<2cm, minimal symptoms):**
- Observation
- Oxygen if needed (sats <94%)
- Analgesia (NSAIDs OK unless contraindicated)
- Serial CXRs (monitor for expansion)

**Large Pneumothorax (>2cm or symptomatic):**
- **Aspiration** (cannula or Seldinger technique)
- Connect to underwater seal drain
- Check for resolution
- Admit to hospital

**Tension Pneumothorax (LIFE-THREATENING):**
- **Immediate decompression**
- Insert large-bore cannula (14-16G) into 2nd intercostal space, mid-clavicular line
- Listen for rush of air
- Then insert formal chest drain
- **DO NOT WAIT FOR CXR**

---

**Aspiration Indications:**
- Large pneumothorax (>2cm)
- Symptomatic (breathless, pain)
- Secondary pneumothorax (underlying lung disease)
- Tension pneumothorax

**Contraindications to aspiration:**
- Bleeding diathesis
- Anticoagulation (NOT absolute contraindication)
- No safe pleural space

---

**Chest Drain Management:**

**Underwater seal drain:**
- Allows air to escape but not re-enter
- Swing (water level moves when patient breathes) confirms patent drain
- Secure drain, sutured to skin

**Monitoring:**
- Check drain is swinging
- Check for air leaks
- Monitor bubbling
- Patient comfort

---

**Resolution:**

**CXR checked:**
- After 24 hours
- Before clamping
- After clamping (if considering removal)

**Removal criteria:**
- Lung fully expanded
- No air leak for 24 hours
- Patient improving

---

**Prevention of Recurrence:**

**Primary spontaneous:**
- Smoking cessation (critical)
- Avoid smoking for 4 weeks after resolution
- High recurrence if continues smoking

**Secondary spontaneous:**
- Optimize treatment of underlying lung disease
- Consider pleurodesis if recurrent

---

**Surgery (if recurrent):**

**Pleurodesis:**
- Irritant (talc, doxycycline) causes pleural surfaces to adhere
- Prevents recurrence
- Performed via VATS (keyhole surgery)

**Bleb resection:**
- Remove blebs (air blisters) from lung surface
- Usually via VATS

---

**⚠️ EMERGENCY SIGNS:**

- Tension pneumothorax (deviated trachea, hypotension, tachycardia)
- Severe breathlessness at rest
- Cyanosis
- Altered mental status

**IMMEDIATE MEDICAL CARE REQUIRED**

---

**Confidence:** 0.88
**Sources:** BTS Pneumothorax Guidelines 2023, NICE CG202
**Important:** Pneumothorax requires medical assessment. Tension pneumothorax is life-threatening and requires immediate intervention."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.88,
            metadata={
                "topic": "pneumothorax",
                "urgency": "emergency_if_tension",
                "treatment": "observation_aspiration_drain"
            }
        )

    def _handle_tb(self, query: str, context: dict) -> DomainQueryResult:
        """Tuberculosis assessment"""

        answer = """**Tuberculosis (TB) Consultation - Respiratory Medicine**

---

**⚠️ TB is a notifiable disease - requires public health involvement**

---

**What is Tuberculosis?**

Bacterial infection caused by *Mycobacterium tuberculosis*.

**Types:**

**Pulmonary TB (most common):**
- Infection of lungs
- Person-to-person transmission
- Cough, fever, weight loss, night sweats

**Extrapulmonary TB:**
- Lymph nodes, pleura, bones/joints, genitourinary, meningeal
- Less contagious, still requires treatment

**Latent TB:**
- Asymptomatic
- Person infected but not infectious
- Can reactivate later (10% lifetime risk)

---

**Risk Factors:**

**Close contact with infectious TB**
- Household member, coworker, close friend
- TB more common in certain countries

**Compromised immunity:**
- HIV/AIDS (10-15x risk)
- Diabetes (3x risk)
- Immunosuppressive medications (steroids, biologics)
- Chemotherapy
- Organ transplant

**Other risk factors:**
- Homelessness, incarceration
- Substance misuse
- Malnutrition
- Silicosis, COPD
- Renal failure

---

**Symptoms of Pulmonary TB:**

**Constitutional (often prominent):**
- Fever (low-grade, evening spikes)
- Night sweats (drenching)
- Weight loss (significant)
- Anorexia, fatigue
- Malaise

**Respiratory:**
- Cough (>2-3 weeks)
- Sputum production (may be blood-streaked)
- Hemoptysis (coughing blood)
- Chest pain
- Breathlessness (if advanced)

**Other:**
- Pleuritic chest pain (if pleurisy)
- Hoarseness (if mediastinal nodes)

---

**Investigation:**

**1. Sputum samples (3 morning samples):**
- **Microscopy:** Look for AFB (acid-fast bacilli)
- **Culture:** Takes 6-8 weeks
- **NAAT/PCR:** Rapid molecular diagnosis (1-2 days)

**2. Chest X-ray:**
- **Typical apical (upper lobe) cavitation**
- Also: Infiltrates, consolidation, effusion
- Can be normal in smear-negative or HIV

**3. Interferon-Gamma Release Assay (IGRA):**
- Blood test
- Distinguishes TB infection vs. BCG vaccination
- Positive in latent and active TB

**4. CT Chest:**
- More detailed than CXR
- Shows cavitation, nodes, infiltrates
- Identifies complications

---

**Diagnosis:**

**Definite TB:** Positive culture or NAAT from respiratory sample

**Probable TB:** Clinical features + CXR/CT findings + decision to treat

---

**Treatment:**

**Standard 4-drug regimen (2 months intensive, 4 months continuation):**

**Intensive Phase (2 months):**
- **Rifampic:** 10mg/kg daily
- **Isoniazid:** 5mg/kg daily
- **Pyrazinamide:** 25mg/kg daily
- **Ethambutol:** 15mg/kg daily

**Continuation Phase (4 months):**
- **Rifampic:** 10mg/kg daily
- **Isoniazid:** 5mg/kg daily
- **Ethambutol:** 15mg/kg daily (if resistant)

**Directly Observed Therapy (DOT):**
- Healthcare worker watches daily/3x weekly
- Ensures adherence
- Prevents resistance

---

**Side Effects of TB Medications:**

**Rifampic:**
- Orange urine, tears (harmless)
- Liver toxicity
- Drug interactions (contraindicated with some HIV meds)

**Isoniazid:**
- Peripheral neuropathy (take pyridoxine/vitamin B6)
- Liver toxicity

**Pyrazinamide:**
- Hyperuricemia (gout)
- Liver toxicity

**Ethambutol:**
- Optic neuritis (color vision changes)
- Visual disturbances

---

**Monitoring During Treatment:**

**Baseline:**
- LFTs, renal function, FBC
- HIV test (if not known)
- Visual acuity (Ethambutol)
- Uric acid (Pyrazinamide)

**Regular monitoring:**
- LFTs (monthly initially)
- Symptom review
- Weight monitoring
- Sputum for culture conversion (should become negative after 2 months)

---

**Infection Control:**

**Before treatment:**
- Patient potentially infectious
- Mask (surgical mask)
- Isolate if smear-positive
- Ventilation, avoid crowded spaces

**After treatment:**
- **NON-INFECTIOUS after 2 weeks of appropriate treatment**
- 3 negative sputum samples confirm
- Can return to normal activities

---

**Public Health Involvement:**

TB is **notifiable disease**
- Public Health England (PHE) notified
- Contact tracing of close contacts
- Offer screening to contacts (IGRA, CXR)
- Ensure treatment completion

---

**Latent TB:**

**Who needs treatment:**
- Children <5 years (exposed to infectious TB)
- HIV-positive (with positive IGRA, no active disease)
- Immunosuppressed (biologics, steroids, transplant)
- <35 years with recent conversion (IGRA +, CXR -)
- Fibrotic changes on CXR

**Treatment:**
- Isoniazid + Rifampic for 3 months OR
- Isoniazid + Rifapentine weekly for 3 months

---

**Complications of TB:**

**Pleural effusion:** Empyema requires drainage
**Pneumothorax:** Air in pleural space
**Bronchiectasis:** Permanent airway dilation
**Hemoptysis:** Coughing blood
**Miliary TB:** Disseminated TB (life-threatening)
**TB meningitis:** Life-threatening emergency

---

**⚠️ EMERGENCY signs:**
- Massive hemoptysis (coughing >200mL blood)
- Respiratory distress
- Miliary/meningeal TB symptoms
- Spinal cord compression (Pott's disease)

**SEEK URGENT CARE**

---

**Confidence:** 0.88
**Sources:** NICE NG33 TB, NICE NG124 Latent TB, BTS TB Guidelines
**Important:** TB requires specialist management. Public health involvement mandatory. Treatment is long (6+ months) and requires monitoring for side effects and adherence."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.88,
            metadata={
                "topic": "tuberculosis",
                "condition": "tb",
                "notifiable": True,
                "treatment_duration": "6_months_minimum",
                "public_health": True
            }
        )

    def _handle_lung_cancer(self, query: str, context: dict) -> DomainQueryResult:
        """Lung cancer assessment"""

        answer = """**Lung Cancer Consultation - Respiratory Medicine**

---

**⚠️ Cancer diagnosis and management requires specialist care**

---

**Lung Cancer Overview:**

**Main Types:**

**Non-Small Cell Lung Cancer (NSCLC) - 85% of cases:**
- **Adenocarcinoma** (most common, increasing)
- **Squamous cell carcinoma**
- **Large cell carcinoma**

**Small Cell Lung Cancer (SCLC) - 15% of cases:**
- Aggressive, early metastasis
- Chemotherapy-sensitive but often relapses
- Strong association with smoking

---

**Risk Factors:**

**Smoking:**
- Causes 85-90% of lung cancers
- Risk increases with pack-years
- Risk decreases after quitting but never reaches zero

**Other risk factors:**
- Radon exposure (2nd leading cause)
- Asbestos (mesothelioma)
- Air pollution
- Occupational exposures (silica, metals)
- Family history (genetics)
- Age (most cases >65)

---

**Symptoms of Lung Cancer:**

**Local (airway invasion):**
- Cough (>3 weeks, changing pattern)
- Hemoptysis (coughing blood)
- Dyspnoea (breathlessness)
- Wheeze (unilateral, new)
- Hoarseness (recurrent nerve palsy)

**Local (chest wall invasion):**
- Chest pain
- Shoulder tip pain (Pancoast tumor)
- Superior vena cava obstruction

**Metastatic (spread):**
- Bone pain (fracture without trauma)
- Headache, neurological symptoms (brain mets)
- Weight loss, anorexia

**Paraneoplastic:**
- Hypercalcemia (SCLC)
- SIADH (inappropriate ADH)
- Cushing syndrome (ACTH production)
- Lambert-Eaton myasthenic syndrome

---

**Red Flag Symptoms (Urgent Referral):**

**For suspected cancer:**
- **Persistent cough (>3 weeks)** or changing pattern
- **Hemoptysis** (coughing blood)
- **Dysphonia** (hoarseness >3 weeks)
- **Chest wall pain** (persistent)
- **Weight loss** (unintentional, significant)
- **Appetite loss**
- **Fatigue**

**For suspected Pancoast tumor:**
- Shoulder tip pain
- Horner's syndrome (ptosis, miosis, anhidrosis)
- Rib erosion

---

**Investigation:**

**1. Chest X-ray (first-line):**
- May show mass, consolidation, effusion
- **Normal CXR DOES NOT exclude cancer** (CT needed)

**2. CT Chest (with contrast):**
- Size, location, character of lesion
- Lymph node enlargement
- Metastases
- Biopsy guidance

**3. PET-CT:**
- Staging (metastases?)
- Distinguish benign vs malignant
- Biopsy targeting

**4. Tissue Diagnosis (biopsy):**
- Bronchoscopy (central tumors)
- CT-guided biopsy (peripheral lesions)
- Surgical biopsy (if other methods fail)

**5. Staging Investigations:**
- **Brain MRI** (if SCLC or symptoms)
- **CT abdomen/pelvis** (liver/adrenal mets)
- **Bone scan** (if bone pain)
- **Mediastinoscopy** (node sampling)

---

**Staging (NSCLC):**

**Stage I:** Tumor <3-5cm, no nodes, no mets
**Stage II:** Tumor + ipsilateral nodes
**Stage III:** Tumor + contralateral nodes or locally advanced
**Stage IV:** Distant metastases

**Small Cell Staging:**
**Limited stage:** Confined to one hemithorax
**Extensive stage:** Distant metastases

---

**Treatment:**

**NSCLC - Early Stage (I-II):**
- **Surgery** (lobectomy, pneumonectomy)
- **Adjuvant chemotherapy** (considered for stage II)
- **Radiotherapy** (if surgery contraindicated)

**NSCLC - Locally Advanced (III):**
- **Chemoradiation** (chemo + radiation together)
- Immunotherapy (PD-1/PD-L1 inhibitors)

**NSCLC - Metastatic (IV):**
- **Immunotherapy** (first-line for most)
- **Targeted therapy** (if mutation found):
  - EGFR inhibitors
  - ALK inhibitors
  - ROS1 inhibitors
  - BRAF/MEK inhibitors
- **Chemotherapy** (if no driver mutation or immunotherapy contraindicated)

**SCLC - Limited Stage:**
- **Chemoradiation** (chemo + chest radiation)
- **Prophylactic cranial irradiation** (PCI)

**SCLC - Extensive Stage:**
- **Chemotherapy** (platinum + etoposide)
- **Immunotherapy** (recent advances)
- **PCI** if responds to chemo

---

**Molecular Testing:**

**All NSCLC adenocarcinomas and any NSCLC in non-smokers should be tested for:**

**EGFR mutations** (tyrosine kinase inhibitors)
- Exon 19 deletion (most common)
- L858R point mutation
- Other rarer mutations

**ALK rearrangements**
**ROS1 rearrangements**
**BRAF mutations**
**NTRK fusions**
**PD-L1 expression** (for immunotherapy)

---

**Prognosis:**

**5-Year Survival (by stage):**
- **Stage I:** 60-80%
- **Stage II:** 40-50%
- **Stage III:** 15-30%
- **Stage IV:** 5-10%

**Prognostic factors:**
- Performance status (functional status)
- Weight loss
- Tumor markers (certain mutations)
- Response to treatment

---

**Palliative Care:**

**Radiotherapy:**
- Painful bone mets (very effective)
- Brain mets (symptom control)
- Superior vena cava obstruction
- Hemoptysis

**Other:**
- Pain management
- Dyspnoea relief (oxygen, opioids)
- Psychological support

---

**Follow-up:**

**After treatment:**
- CT chest every 3-6 months (initially)
- Then annually up to 5 years
- Surveillance for second primary cancers (risk elevated)

**Smoking cessation:**
- Critical after diagnosis
- Reduces risk of second primary
- Improves treatment efficacy
- Increases survival

---

**Prevention:**

**Avoid smoking** (single most important)
- Avoid secondhand smoke
- Avoid radon (test home, mitigate if elevated)
- Occupational protection (asbestos, silica)

**Screening:**
- Available for high-risk patients
- Low-dose CT (LDCT)
- Reduces lung cancer mortality by 20%
- Considered in heavy smokers aged 50-80

---

**⚠️ URGENT REFERRAL NEEDED:**

- Any of the red flag symptoms above
- Suspected superior vena cava obstruction
- Massive hemoptysis
- Spinal cord compression

---

**Confidence:** 0.89
**Sources:** NICE NG151 Lung Cancer, NICE NG131 Lung Cancer Screening
**Important:** Lung cancer requires urgent specialist referral. Rapid diagnostic pathways available. Smoking cessation remains critical even after diagnosis."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.89,
            metadata={
                "topic": "lung_cancer",
                "condition": "lung_cancer",
                "urgency": "urgent_referral_required",
                "red_flags": ["cough >3 weeks", "hemoptysis", "hoarseness", "weight loss"],
                "screening": "low_dose_ct"
            }
        )

    def _handle_cough(self, query: str, context: dict) -> DomainQueryResult:
        """Cough assessment"""

        answer = """**Cough Assessment - Respiratory Consultation**

---

**Cough is one of the most common reasons for medical consultation**

---

**Key Questions for Assessment:**

**1. Duration:**
- **Acute (<3 weeks):** Usually infection (URTI, pneumonia, bronchitis)
- **Subacute (3-8 weeks):** Post-infective, asthma, reflux, early chronic disease
- **Chronic (>8 weeks):** Chronic cough (asthma, COPD, UGORD, post-nasal drip)

**2. Character:**
- **Dry:** Viral, asthma, reflux, post-nasal drip, interstitial lung disease, meds (ACEi)
- **Productive:** Bacterial infection, COPD, bronchiectasis, TB, cancer

**3. Timing:**
- **Morning:** Smoker's cough (bronchitis), post-nasal drip
- **Throughout day:** Asthma, UGORD, interstitial lung disease
- **Night:** Heart failure, post-nasal drip
- **With eating:** Dysphagia, aspiration risk

**4. Triggers:**
- **Exercise:** Asthma, deconditioning
- **Cold air:** Asthma
- **Lying down:** Heart failure, post-nasal drip
- **Talking:** Laryngeal irritation, reflux

**5. Associated Symptoms:**
- **Fever:** Infection
- **Weight loss:** Cancer, TB, hyperthyroidism, IBD
- **Night sweats:** TB, lymphoma, menopause
- **Chest pain:** Pneumonia, PE, pneumothorax, pericarditis
- **Dysphagia:** Stroke, neuromuscular disease, esophageal cancer
- **Hoarseness:** Lung cancer (recurrent nerve), reflux, laryngitis
- **Wheeze:** Asthma, COPD, heart failure

---

**Common Causes of Chronic Cough (>8 weeks):**

**1. Upper Airway Cough Syndrome (40%):**
- **Post-nasal drip** (rhinitis, sinusitis)
- **Asthma** (cough-variant asthma may not wheeze)
- **Laryngeal irritation** (reflux, post-nasal drip)

**2. GORD (Gastroesophageal Reflux):**
- Acid reflux causes airway irritation
- Cough often after meals, lying down
- May have classic reflux symptoms too

**3. Asthma:**
- **Cough-variant asthma** (cough may be only symptom)
- Exercise-induced, allergen-triggered
- Nighttime cough common

**4. COPD:**
- Smoker's cough (morning productive cough)
- Progressive exertional dyspnoea
- Usually significant smoking history

**5. Medications:**
- **ACE inhibitors:** Dry cough in 20% (starts days-weeks after starting)
- **Beta-blockers:** Can trigger bronchospasm in asthmatics
- **Others:** Amiodarone, NSAIDs

---

**Other Important Causes:**

**Infections:**
- **Acute bronchitis:** URTI complication
- **Pneumonia:** Systemic symptoms, fever
- **Whooping cough:** Paroxysmal cough, whoop, post-tussive vomiting
- **TB:** Chronic, weight loss, night sweats

**Cardiovascular:**
- **Heart failure:** Orthopnea, PND, ankle swelling
- **Pulmonary embolism:** Acute, pleuritic pain, DVT risk
- **Pericarditis:** Sharp positional pain, friction rub

**Malignancy:**
- **Lung cancer:** Changing cough, hemoptysis, weight loss
- **Lymphoma:** Night sweats, weight loss, nodes
- **Mesothelioma:** Asbestos exposure, chest pain

**Other:**
- **Interstitial lung disease:** Progressive dry cough, clubbing
- **Bronchiectasis:** Large volumes of sputum, chronic infections
- **Psychogenic:** Habit cough, tic

---

**Investigation Approach:**

**1. Chest X-ray:**
- First-line for most chronic cough
- May show masses, effusions, cardiac enlargement, interstitial changes
- **Normal CXR does NOT exclude cancer** (early disease may be invisible)

**2. Spirometry:**
- Obstruction (asthma, COPD)
- Restriction (fibrosis, neuromuscular)
- Reversibility (asthma vs COPD)

**3. Blood tests:**
- **FBC:** Infection (leukocytosis), anemia
- **CRP:** Inflammation
- **U&Es:** Renal function
- **LFTs:** Liver metastases
- **ESR/CRP:** Inflammatory markers

**4. Sputum culture:**
- If productive cough
- Bacteria, TB

**5. CT Chest (if CXR abnormal or high suspicion):**
- Better than CXR for small cancers, early disease
- Lymph node assessment

**6. ENT review:**
- Post-nasal drip assessment
- Laryngoscopy if hoarseness

**7. GORD assessment:**
- Trial of PPI (Proton Pump Inhibitor)
- pH monitoring if uncertain

---

**Management Principles:**

**Specific treatment of underlying cause**

**Symptomatic relief:**
- Simple linctus (demulcents)
- Honey (evidence-based for cough)
- Avoid over-suppression (protects cough reflex)

---

**⚠️ RED FLAGS requiring urgent investigation:**

- Hemoptysis (coughing blood)
- Weight loss with no obvious cause
- Night sweats
- Smoker >40 with new cough
- Hoarseness >3 weeks
- Chest pain
- Dysphagia
- Exposure to TB

---

**Confidence:** 0.86
**Sources:** NICE NG121 Chronic Cough, BTS Cough Guidelines
**Important:** Persistent cough (>8 weeks) or cough with red flag symptoms requires proper investigation. This is general guidance - diagnosis requires examination and investigations."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.0,
            metadata={
                "topic": "cough",
                "duration_based_assessment": True,
                "red_flags": ["hemoptysis", "weight loss", "night sweats", "hoarseness >3 weeks"]
            }
        )

    def _handle_general_respiratory(self, query: str, context: dict) -> DomainQueryResult:
        """General respiratory consultation"""

        answer = """**Respiratory Medicine Consultation - Second Opinion**

I can provide consultation on:

**Common Respiratory Conditions:**
- Asthma (diagnosis, management, action plans)
- COPD (staging, exacerbations, oxygen)
- Pneumonia (assessment, treatment, severity)
- Respiratory infections (bronchitis, bronchiectasis)
- Pleural effusion (investigation, drainage)
- Pneumothorax (management, drainage)
- Pulmonary embolism (risk, investigation, treatment)
- Tuberculosis (diagnosis, treatment, infection control)
- Interstitial lung disease
- Lung cancer (symptoms, screening, referral)

**Diagnostic Tests I Can Help Interpret:**
- Spirometry (FEV1, FVC, FEV1/FVC, reversibility)
- Chest X-rays (basic interpretation)
- Arterial blood gases (pH, PaO2, PaCO2, HCO3-)
- Sputum culture results
- Pulmonary function tests
- CT chest reports

**Symptom-Based Consultation:**
- Breathlessness/dyspnoea (assessment approach)
- Cough (differential diagnosis)
- Wheeze (causes, management)
- Chest pain (respiratory causes)
- Sputum production (color, volume, character)
- Hemoptysis (causes, urgency)
- Fever with respiratory symptoms

**Treatment Guidance:**
- Inhaler techniques
- Smoking cessation strategies
- Vaccination (influenza, pneumococcal, COVID-19, RSV, shingles)
- Pulmonary rehabilitation
- Oxygen therapy
- Nebulizer use
- Breathing techniques

**Chronic Disease Management:**
- Asthma control assessment
- COPD GOLD staging and treatment
- Long-term oxygen therapy
- Palliative care in advanced disease

---

**For the most accurate consultation, please provide:**
1. Your specific respiratory concern
2. Duration and progression of symptoms
3. Associated symptoms
4. Risk factors (smoking, occupational, travel)
5. Previous respiratory history
6. Any test results you have (spirometry, CXR, bloods)
7. Current medications

---

**⚠️ EMERGENCY - Seek immediate care for:**
- Severe breathlessness at rest
- Inability to speak in full sentences
- Chest pain
- Coughing significant blood
- Confusion or drowsiness
- sats <92% (if oximeter available)

---

**Confidence:** 0.85
**Sources:** BTS Guidelines, NICE Respiratory Guidelines
**I can provide evidence-based second opinions and help you understand your respiratory condition, test results, and treatment options.**

**Remember:** This is general medical information for educational purposes. For diagnosis and treatment, you must see a qualified healthcare professional."""

        return DomainQueryResult(
            domain_name="respiratory",
            answer=answer,
            confidence=0.85,
            metadata={
                "topic": "general_respiratory",
                "scope": "comprehensive_respiratory_consultation"
            }
        )
