"""
Allergy and Immunology Domain for GPDISC

Comprehensive allergy and immunology consultation covering:
- Allergic rhinitis and conjunctivitis
- Asthma (allergic and non-allergic)
- Atopic dermatitis (eczema)
- Urticaria (hives) and angioedema
- Anaphylaxis (life-threatening emergency)
- Food allergy
- Drug allergy
- Immunodeficiency disorders
- Autoimmune diseases

Evidence-based guidelines:
- BSACI (British Society for Allergy and Clinical Immunology)
- NICE NGxx guidelines
- AAAAI (American Academy of Allergy, Asthma & Immunology)
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class AllergyImmunologyDomain(BaseDomainModule):
    """
    Allergy and Immunology domain for comprehensive allergy and
    immunology consultation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="allergy_immunology",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive allergy and immunology: rhinitis, asthma, eczema, urticaria, anaphylaxis, food/drug allergies, immunodeficiency",
            keywords=[
                "allergy", "allergic", "rhinitis", "hay fever", "sneezing", "runny nose",
                "asthma", "wheeze", "inhaler", "ventolin", "steroid",
                "eczema", "atopic dermatitis", "itchy skin", "atopy",
                "urticaria", "hives", "angioedema", "swelling",
                "anaphylaxis", "anaphylactic", "allergic shock", "epipen",
                "food allergy", "peanut", "nut", "shellfish", "milk", "egg",
                "drug allergy", "penicillin", "antibiotic allergy", "drug reaction",
                "immunodeficiency", "primary immunodeficiency", "recurrent infection",
                "autoimmune", "immunology", "allergen", "desensitisation",
                "antihistamine", "cetirizine", "loratadine", "prednisolone"
            ],
            capabilities=[
                "allergy_diagnosis",
                "anaphylaxis_management",
                "asthma_allergy_management",
                "eczema_atopic_dermatitis_treatment",
                "urticaria_angioedema_management",
                "food_allergy_evaluation",
                "drug_allergy_assessment",
                "immunodeficiency_screening",
                "allergen_immunotherapy"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process allergy/immunology query with emergency detection
        """
        query_lower = query.lower()

        # ANAPHYLAXIS - HIGHEST PRIORITY EMERGENCY
        if any(term in query_lower for term in ["anaphylaxis", "anaphylactic shock", "severe allergic reaction",
                                                   "airway swelling", "throat closing", "difficulty breathing",
                                                   "wheezing allergy", "collapse allergy", "epipen", "adrenaline"]):
            return self._handle_anaphylaxis(query, context)

        # ANGIOEDEMA - URGENT (airway compromise risk)
        if any(term in query_lower for term in ["angioedema", "facial swelling", "lip swelling",
                                                   "tongue swelling", "eye swelling"]):
            return self._handle_angioedema(query, context)

        # ACUTE SEVERE ASTHMA
        if any(term in query_lower for term in ["severe asthma", "asthma attack", "acute asthma",
                                                   "status asthmaticus", "life-threatening asthma"]):
            return self._handle_severe_asthma(query, context)

        # ALLERGIC RHINITIS
        if any(term in query_lower for term in ["hay fever", "allergic rhinitis", "sneezing", "runny nose",
                                                   "itchy nose", "nasal allergy", "pollen"]):
            return self._handle_allergic_rhinitis(query, context)

        # ASTHMA
        if any(term in query_lower for term in ["asthma", "wheeze", "wheezing", "inhaler",
                                                   "ventolin", "salbutamol", "preventer", "brown inhaler"]):
            return self._handle_asthma(query, context)

        # ATOPIC DERMATITIS / ECZEMA
        if any(term in query_lower for term in ["eczema", "atopic dermatitis", "atopic eczema",
                                                   "itchy skin", "atopic skin", "childhood eczema"]):
            return self._handle_eczema(query, context)

        # URTICARIA / HIVES
        if any(term in query_lower for term in ["urticaria", "hives", "welts", "itchy welts",
                                                   "raised rash", "wheals"]):
            return self._handle_urticaria(query, context)

        # FOOD ALLERGY
        if any(term in query_lower for term in ["food allergy", "peanut allergy", "nut allergy",
                                                   "shellfish allergy", "milk allergy", "egg allergy",
                                                   "allergic to food", "food reaction"]):
            return self._handle_food_allergy(query, context)

        # DRUG ALLERGY
        if any(term in query_lower for term in ["drug allergy", "penicillin allergy", "antibiotic allergy",
                                                   "allergic to penicillin", "drug reaction", "medication allergy"]):
            return self._handle_drug_allergy(query, context)

        # IMMUNODEFICIENCY
        if any(term in query_lower for term in ["immunodeficiency", "primary immunodeficiency",
                                                   "recurrent infection", "frequent infection",
                                                   "immune deficiency"]):
            return self._handle_immunodeficiency(query, context)

        # GENERAL ALLERGY
        return self._handle_general_allergy(query, context)

    def _handle_anaphylaxis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle anaphylaxis - life-threatening emergency"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ANAPHYLAXIS - LIFE-THREATENING EMERGENCY**

**IMMEDIATE ACTION:**
- **Call for help / Call emergency services (999/911)**
- **Administer IM adrenaline (epinephrine) IMMEDIATELY**
- **Do NOT delay treatment for investigation**

**DIAGNOSIS (clinical):**
Anaphylaxis is **HIGHLY LIKELY** if ANY of the following 3 criteria are met:

1. **Acute onset** (minutes to hours) with involvement of:
   - Skin/mucosa (urticaria, itch, flush, swelling) AND
   - Respiratory compromise (wheeze, stridor, dyspnoea) OR
   - Reduced BP or associated symptoms (collapse, syncope, incontinence)

2. **Two or more** of the following occurring rapidly after exposure to allergen:
   - Skin/mucosal involvement
   - Respiratory compromise
   - Reduced BP or associated symptoms
   - Persistent gastrointestinal symptoms (crampy pain, vomiting)

3. **Reduced BP** after exposure to known allergen:
   - Infants/children: low systolic BP (age-specific) or >30% drop
   - Adults: systolic BP <90 mmHg or >30% drop from baseline

**COMMON TRIGGERS:**
- **Food:** peanuts, tree nuts, shellfish, milk, egg
- **Drugs:** antibiotics (penicillin), NSAIDs, anaesthetic agents
- **Stings:** bees, wasps
- **Latex**
- **Exercise** (food-dependent exercise-induced anaphylaxis)
- **Idiopathic** (unknown cause)

**IMMEDIATE MANAGEMENT (ABC):**

**1. Adrenaline (Epinephrine) - FIRST LINE, DO NOT DELAY:**
- **IM injection** into anterolateral thigh (vastus lateralis)
- **Adults:** 0.5 mg IM (0.5 mL of 1:1000 solution)
- **Children >6 years:** 0.3 mg IM (0.3 mL of 1:1000)
- **Children 6 months-6 years:** 0.15 mg IM (0.15 mL of 1:1000)
- **Repeat every 5 minutes** if no improvement

**2. Call for help:**
- Emergency team, crash cart
- Consider airway protection (early intubation if respiratory distress)

**3. Positioning:**
- **Lie flat with legs elevated** (unless breathing difficult → sit up)
- **DO NOT stand or walk** (increases risk of cardiac arrest)
- Pregnant women: left lateral position

**4. Remove trigger (if possible):**
- Stop IV infusion (drug reaction)
- Remove stinger (if visible)

**5. Oxygen:**
- High-flow (15 L/min) via non-rebreathe mask
- Maintain SpO2 >94%

**6. IV fluids:**
- **Crystalloid bolus** (500-1000 mL rapid infusion)
- Repeat as needed (shock may require large volumes)

**7. Adjunctive therapies:**

**Antihistamines (H1 blocker):**
- Diphenhydramine 25-50 mg IV/IM OR Cetirizine 10 mg IV/PO
- **Do NOT use as first-line or sole treatment**
- Does NOT treat airway obstruction or shock

**Corticosteroids:**
- Methylprednisolone 100 mg IV or Hydrocortisone 200 mg IV
- Takes 4-6 hours to work
- May prevent biphasic reaction (prolonged symptoms)

**Bronchodilators:**
- Salbutamol 5 mg nebulised (if wheezing)
- Ipratropium 0.5 mg nebulised (if bronchospasm)

**8. Refractory anaphylaxis:**
- **Adrenaline infusion:** start 0.05-0.1 mcg/kg/min, titrate
- Consider glucagon (if on beta-blockers)

**BIPHASIC REACTION:**
- Occurs in up to 20% of cases
- Symptoms recur 1-72 hours (usually 8-12 hours) without re-exposure
- **Observe for 6-12 hours** (longer if severe or refractory)
- **Prescribe adrenaline autoinjector** (EpiPen, Jext) on discharge

**DISCHARGE PLANNING:**
- Adrenaline autoinjector (2 devices)
- Antihistamine (cetirizine 10 mg daily)
- Oral steroids (prednisolone 40-50 mg for 3-5 days)
- **Education:** how to use autoinjector
- **Action plan:** written instructions
- **Referral:** allergy clinic for investigation

**INVESTIGATIONS (post-stabilisation):**
- Mast cell tryptase:
  - Sample 1: as soon as possible after reaction (within 1-2 hours)
  - Sample 2: 24-48 hours later (baseline)
  - Elevated (>1.2 × baseline + 2 ng/mL) confirms mast cell activation
- Specific IgE (RAST) testing
- Skin prick testing

**Sources:** Resuscitation Council (UK), BSACI Guidelines, NICE CG134""",
            metadata={
                "urgency": "emergency",
                "condition": "anaphylaxis",
                "time_to_adrenaline": "immediate"
            }
        )

    def _handle_angioedema(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle angioedema"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ANGIOEDEMA - URGENT (Airway Risk)**

**DEFINITION:**
- Localised swelling of dermis, subcutaneous, or submucosal tissues
- Often involves face, lips, tongue, soft palate
- **Can progress to life-threatening airway obstruction**

**TYPES:**

**1. Histaminergic Angioedema (Allergic):**
- **Mechanism:** IgE-mediated mast cell degranulation
- **Triggers:** food, drugs, latex, insect stings
- **Onset:** minutes to hours
- **Associated:** urticaria (hives), itching, flushing
- **Responsive to:** antihistamines, corticosteroids

**2. Bradykinin-Mediated Angioedema:**
- **Mechanism:** Bradykinin accumulation (not IgE-mediated)
- **Types:**
  - **Hereditary Angioedema (HAE):** C1 esterase inhibitor deficiency
  - **Acquired Angioedema:** C1 esterase inhibitor deficiency (acquired)
  - **ACE inhibitor-induced angioedema:** 0.1-0.7% patients on ACEi

**ACE INHIBITOR-INDUCED ANGIOEDEMA:**
- **Can occur at any time** (days to years after starting)
- **Higher risk:** African descent, smoking, history of drug rash
- **Management:**
  - **Stop ACE inhibitor permanently**
  - **Avoid ALL ACE inhibitors** and **ARBs** (cross-reaction possible)
  - Supportive care (airway protection if needed)
  - **NOT responsive** to antihistamines, corticosteroids, adrenaline
  - **Specific therapies:** icatibant (bradykinin B2 receptor antagonist), C1 esterase inhibitor

**IMMEDIATE MANAGEMENT:**

**Assess airway:**
- **Stridor, hoarseness, dyspnoea** → **potential airway obstruction**
- **Early involvement of anaesthetics/ENT**
- **Prepare for difficult airway**

**Airway protection:**
- **Early intubation** (before complete obstruction)
- **Fibreoptic intubation** (may be needed due to swelling)
- **Cricothyrotomy** (if cannot intubate, cannot ventilate)

**Medical management:**

**Histaminergic angioedema:**
1. **Adrenaline (IM)** if airway involvement or anaphylaxis
2. **Antihistamine:**
   - Cetirizine 10 mg IV/PO or Loratadine 10 mg PO
   - Add H2 blocker (Ranitidine 50 mg IV or Famotidine 20 mg IV)
3. **Corticosteroids:**
   - Methylprednisolone 40-125 mg IV or Prednisolone 40-50 mg PO
4. **Observation:** 4-6 hours (discharge if improving, airway safe)

**Bradykinin-mediated angioedema:**
1. **Stop ACE inhibitor** (if applicable)
2. **Specific therapy (if available):**
   - **Icatibant** 30 mg SC (max 3 doses in 24 hours)
   - **C1 esterase inhibitor** (for HAE)
   - **Ecallantide** (kallikrein inhibitor)
3. **Fresh frozen plasma** (if specific therapy unavailable)
4. **NOT responsive** to antihistamines or steroids

**HEREDITARY ANGIOEDEMA (HAE):**
- **Autosomal dominant**
- **C1 esterase inhibitor deficiency** (Type I or II)
- **Triggers:** stress, trauma, menstruation, pregnancy, ACE inhibitors
- **Symptoms:** recurrent angioedema (face, extremities, abdomen, airway)
- **Abdominal attacks:** severe pain, vomiting, diarrhoea (mimics surgical abdomen)
- **Prophylaxis:**
  - **Attenuated androgens:** Danazol 200-400 mg daily
  - **C1 esterase inhibitor** (regular infusions)
  - **Tranexamic acid** (weaker, less used)
- **Acute treatment:** C1 esterase inhibitor concentrate, Icatibant

**INVESTIGATIONS:**
- **C4 complement** (low in HAE, normal in histaminergic)
- **C1 esterase inhibitor** level and function
- **C1q** (low in acquired, normal in hereditary)

**REFERRAL:**
- **Urgent allergy/immunology referral** if recurrent angioedema
- **Urgent ENT/anaesthetics** if airway involvement

**Sources:** BSACI Guidelines, AAAAI Guidelines, NICE CG134"""
        )

    def _handle_severe_asthma(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle acute severe asthma"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ACUTE SEVERE ASTHMA - MEDICAL EMERGENCY**

**IMMEDIATE ACTION:**
- **Assess severity** (near-fatal, life-threatening, severe)
- **Administer oxygen, bronchodilators, steroids IMMEDIATELY**
- **Consider early admission** (life-threatening features)

**SEVERITY ASSESSMENT:**

**Near-Fatal Asthma:**
- Raised PaCO2
- Need for mechanical ventilation

**Life-Threatening Asthma (any of following):**
- Peak flow <33% best or predicted
- SpO2 <92%
- PaO2 <8 kPa
- Normal PaCO2 (4.6-6.0 kPa) - indicates fatigue
- Silent chest
- Poor respiratory effort
- Cyanosis
- Exhaustion
- Confusion, drowsiness
- Arrhythmia

**Severe Asthma (any of following):**
- Peak flow 33-50% best or predicted
- Respiratory rate ≥25/min
- Heart rate ≥110/min
- Unable to complete sentences in one breath

**IMMEDIATE MANAGEMENT:**

**1. Oxygen:**
- High-flow (15 L/min) via non-rebreathe mask
- Target SpO2 94-98%

**2. Bronchodilators:**

**Short-acting beta-agonist (SABA):**
- **Salbutamol 5 mg** nebulised (driven by oxygen)
- Repeat every 15-20 minutes (or continuous nebulisation)
- **If no nebuliser:** 4-10 puffs via spacer (every 10 minutes)

**Ipratropium bromide:**
- **0.5 mg** nebulised (added to salbutamol)
- Particularly in life-threatening asthma
- Repeat every 4-6 hours

**3. Systemic Corticosteroids:**
- **Prednisolone 40-50 mg PO** (or Methylprednisolone 40-125 mg IV)
- Continue for 5 days
- **DO NOT delay** for nebulised bronchodilators

**4. IV Magnesium Sulphate:**
- **2 g IV over 20 minutes** (for severe or life-threatening asthma)
- Safe, may reduce admission

**5. IV Salbutamol (if refractory):**
- Consider if poor response to nebulised therapy
- 5 mcg/min (titrate)
- Monitor: tachycardia, hypokalaemia, tremor

**6. Aminophylline (if refractory):**
- Consider if no response to maximal bronchodilators + steroids + Mg
- Loading dose 5 mg/kg over 20 minutes (if not on theophylline)
- Maintenance 0.5-0.7 mg/kg/hr
- **Monitor levels:** 10-20 mg/L
- **Contraindicated:** on oral theophylline

**MONITORING:**
- **Peak flow** (or FEV1) every 15-30 minutes
- **Observations:** RR, HR, BP, SpO2, temperature
- **ABG** if life-threatening (hypoxia, hypercapnia)
- **CXR** (if pneumothorax suspected, or not improving)

**RESPONSE TO TREATMENT:**

**Good response:**
- PEF >50% predicted/best
- No features of life-threatening asthma
- Discharge after 4-6 hours observation

**Poor response / life-threatening features:**
- Admit to hospital
- **Consider HDU/ITU** if:
  - PEF <33%
  - Persistent hypoxia
  - Hypercapnia (PaCO2 >6 kPa)
  - Need for frequent bronchodilators
  - Drowsiness, exhaustion

**INTUBATION AND VENTILATION:**
- **Early discussion with anaesthetics/ITU**
- **Indications:**
  - Respiratory arrest
  - Severe hypoxia refractory to treatment
  - Hypercapnia with respiratory fatigue
  - Decreasing level of consciousness
- **Strategy:**
  - Rapid sequence induction
  - Low tidal volume (6-8 mL/kg)
  - Low respiratory rate (10-12/min)
  - Long expiratory time (I:E 1:4 or 1:5)
  - Permissive hypercapnia
- **Avoid:**
  - PEEP (can cause dynamic hyperinflation, pneumothorax)
  - Excessive sedation

**DISCHARGE PLANNING:**
- **Review inhaler technique**
- **Personalised asthma action plan**
- **Optimise maintenance therapy:**
  - **ICS + LABA** (if on SABA alone)
  - Consider leukotriene receptor antagonist (Montelukast)
  - Ensure adherence
- **Follow-up:** review in 2-7 days (GP or asthma clinic)
- **Consider referral:** difficult asthma clinic if recurrent admissions

**Sources:** BTS/SIGN British Guideline on Asthma, NICE NG80"""
        )

    def _handle_allergic_rhinitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle allergic rhinitis"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ALLERGIC RHINITIS (Hay Fever)**

**DEFINITION:**
- Inflammation of nasal mucosa due to IgE-mediated reaction to allergens
- **Seasonal (intermittent):** pollen (tree, grass, weed)
- **Perennial (persistent):** dust mites, pets, mold

**SYMPTOMS:**
- **Nasal:** sneezing, itching, rhinorrhoea (runny nose), congestion
- **Ocular:** itching, watering, redness (allergic conjunctivitis)
- **Other:** post-nasal drip, cough, fatigue, impaired sleep

**IMPACT:**
- Quality of life (sleep, work, school)
- Exacerbates asthma
- Increases risk of sinusitis

**DIAGNOSIS:**
- **Clinical diagnosis** (typical history)
- **Skin prick testing** (if specific allergen identification needed)
- **Specific IgE (RAST)** (if skin testing unavailable)
- **Nasal endoscopy** (if structural abnormality suspected)

**MANAGEMENT:**

**1. Allergen Avoidance:**
- **Pollen:**
  - Keep windows closed (high pollen season)
  - Avoid outdoor activities when pollen count high
  - Apply barrier balm around nostrils
  - Wash face/hair after outdoor exposure
  - Wear sunglasses
- **Dust mites:**
  - Encase mattress/pillows in allergen-proof covers
  - Wash bedding weekly at >60°C
  - Remove carpets (if possible)
  - Reduce humidity (<50%)
  - Regular vacuuming with HEPA filter
- **Pets:**
  - Keep pets out of bedroom
  - HEPA filter air purifier
  - Wash pets regularly

**2. Intranasal Corticosteroids (first line for moderate-severe):**
- **Mometasone 200 mcg** (2 sprays) daily
- **Fluticasone 200 mcg** (2 sprays) daily
- **Triamcinolone 220 mcg** (2 sprays) daily
- **Onset:** 12 hours, max effect 3-7 days
- **Technique important:** tilt head forward, point away from septum
- **Safe:** minimal systemic absorption

**3. Oral Antihistamines (first line for mild):**
- **Second-generation** (non-sedating preferred):
  - Cetirizine 10 mg daily
  - Loratadine 10 mg daily
  - Fexofenadine 120 mg daily
  - **Azelastine** (intranasal antihistamine spray)
- **Onset:** 1-2 hours
- **Safe:** can take daily during season

**4. Intranasal Antihistamines:**
- **Azelastine 0.1% spray** (1-2 sprays per nostril BD)
- Rapid onset (15-30 minutes)
- Can use with intranasal steroid

**5. Decongestants (short-term only):**
- **Oral:** Pseudoephedrine 60 mg TDS (max 7 days)
- **Intranasal:** Xylometazoline (Otrivine) 1-2 sprays TDS (max 7 days)
- **Rebound congestion** with prolonged use

**6. Leukotriene Receptor Antagonists:**
- **Montelukast 10 mg daily**
- If nasal symptoms + asthma
- If inadequate response to intranasal steroid

**7. Cromones (mast cell stabilisers):**
- **Sodium cromoglicate** nasal spray
- Safe but less effective, requires frequent dosing (4-6x daily)

**8. Allergen Immunotherapy (Desensitisation):**
- **Subcutaneous (SCIT)** or **Sublingual (SLIT)**
- Consider if:
  - Severe symptoms despite optimal medical therapy
  - Single allergen sensitivity
  - Duration ≥3 years
- **Contraindications:** uncontrolled asthma, beta-blocker use
- **Duration:** 3-5 years
- **Effect:** disease modification (long-term benefit after stopping)

**STEPWISE APPROACH:**

**Mild intermittent:**
- Oral antihistamine PRN
- Intranasal antihistamine PRN

**Mild persistent / Moderate-severe:**
- **Intranasal steroid** (regular use)
- Add oral antihistamine
- Add intranasal antihistamine if needed

**Severe / Refractory:**
- **Intranasal steroid + oral antihistamine + intranasal antihistamine**
- Add Montelukast (if asthma component)
- Consider **allergen immunotherapy**
- Referral to allergy clinic

**NON-RESPONSIVE?**
- Review adherence and technique
- Review diagnosis (is it really allergic?)
- Consider structural problems (deviated septum, polyps)
- Consider chronic rhinosinusitis

**Sources:** BSACI Guidelines for Allergic Rhinitis, NICE NG134"""
        )

    def _handle_asthma(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle asthma"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ASTHMA**

**DEFINITION:**
- Chronic inflammatory airway disease
- **Variable airflow obstruction** (reversible spontaneously or with treatment)
- **Hyperresponsiveness** to various stimuli
- **Underlying inflammation** (eosinophilic usually)

**DIAGNOSIS (clinical + physiological):**

**Symptoms:**
- Wheeze
- Breathlessness
- Chest tightness
- Cough (often worse at night/early morning)
- **Variable** (day-to-day, seasonally)

**Objective evidence:**
- **Spirometry** (≥12 years):
  - **FEV1/FVC <0.7** (obstructive pattern)
  - **Reversibility:** ↑FEV1 ≥12% AND ≥200 mL after bronchodilator
- **Peak flow variability** (if spirometry unavailable)
  - >20% diurnal variability over 3 days
- **FeNO** (fractional exhaled nitric oxide) - eosinophilic inflammation

**PHENOTYPES:**

**Allergic asthma (most common):**
- Childhood onset
- Atopic history (eczema, allergic rhinitis)
- Seasonal variation
- Elevated IgE, FeNO

**Non-allergic asthma:**
- Adult onset
- No atopic history
- Often more severe

**Occupational asthma:**
- Work-related exposure
- Improves away from work
- Specific agents (isocyanates, flour, wood dust, animals)

**SEVERITY ASSESSMENT:**

**Mild:**
- Symptoms ≤2x/week
- Night waking ≤2x/month
- Normal lung function

**Moderate:**
- Daily symptoms
- Night waking >1x/week
- FEV1 60-80% predicted

**Severe:**
- Continuous symptoms
- Frequent night waking
- FEV1 <60% predicted
- Exacerbations requiring oral steroids

**MANAGEMENT (STEPWISE APPROACH):**

**Step 1: SABA PRN (Mild intermittent):**
- Salbutamol 100-200 mcg PRN
- **No regular controller** needed

**Step 2: Regular ICS (Low dose):**
- Beclometasone 200 mcg BD (or equivalent)
- **For ALL patients:** regular controller better than SABA alone
- SABA PRN

**Step 3: ICS + LABA (Medium dose ICS):**
- **Preferred:** **Combination inhaler** (SMART/MART regimen)
  - **Formoterol/Budesonide** (1-2 puffs PRN for symptoms, regular maintenance)
  - Or **Fluticasone/Vilanterol** (1 puff daily)
- **Alternative:** Separate ICS + LABA + SABA PRN
- **Medium dose ICS:** Beclometasone 400-500 mcg BD

**Step 4: Medium dose ICS + LABA:**
- Increase ICS dose to medium (if not already)
- Consider adding LTRA (Montelukast) or Theophylline

**Step 5: Referral + Additional therapies:**
- **Refer to respiratory specialist**
- Consider:
  - High dose ICS (max dose)
  - Long-acting muscarinic antagonist (LAMA) - Tiotropium
  - Anti-IL5 (Mepolizumab) - eosinophilic severe asthma
  - Anti-IgE (Omalizumab) - allergic severe asthma
  - Anti-IL4/13 (Dupilumab) - type 2 inflammation

**NON-PHARMACOLOGICAL:**
- **Smoking cessation** (critical)
- **Asthma education**
- **Written asthma action plan**
- **Inhaler technique check** (critical!)
- **Trigger avoidance**
- **Annual influenza vaccination**
- **Pneumococcal vaccination** (once)
- **Regular review** (at least annually)

**EXACERBATIONS:**

**Home management:**
- **SABA:** 4-10 puffs via spacer (repeat every 20 minutes)
- **Oxygen** if available (SpO2 target 94-98%)
- **Prednisolone 40-50 mg** daily for 5 days
- **DO NOT delay** starting oral steroids

**RED FLAGS (admit):**
- Peak flow <33% best/predicted
- SpO2 <92%
- Exhaustion, confusion
- Poor response to initial bronchodilators
- Pregnancy
- Previous near-fatal asthma

**MONITORING:**
- **Asthma Control Test (ACT)** or **Asthma Control Questionnaire (ACQ)**
- **Peak flow diary** (if poor control)
- **FeNO** (if diagnostic uncertainty or treatment monitoring)
- **Spirometry** (annually or after change in therapy)

**Sources:** BTS/SIGN British Guideline on Asthma, NICE NG80"""
        )

    def _handle_eczema(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle atopic dermatitis/eczema"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ATOPIC DERMATITIS (ECZEMA)**

**DEFINITION:**
- Chronic, relapsing inflammatory skin disease
- Pruritus (itch) is hallmark
- Typical distribution and morphology
- Often associated with atopy (asthma, allergic rhinitis)

**EPIDEMIOLOGY:**
- 15-20% children, 2-10% adults
- 60% develop in first year of life
- 85% by age 5
- Often improves with age (many "outgrow" it)

**DIAGNOSIS (clinical):**
- **Itchy skin** (must have!) + 3+ of following:
  - History of flexural involvement (elbows, knees, neck)
  - History of asthma/hay fever (or first-degree relative)
  - History of general dry skin in last year
  - Onset <2 years (not applicable if child <4 years)
  - Visible flexural dermatitis (if child >4 years)

**DISTRIBUTION:**

**Infants:**
- Face, scalp, extensor surfaces
- Nappy area usually spared

**Children:**
- Flexures (antecubital, popliteal fossae)
- Neck, wrists, ankles

**Adults:**
- Flexures, face, neck, hands
- Lichenified (thickened) skin

**TRIGGERS:**
- **Irritants:** soaps, detergents, wool, synthetic fabrics
- **Allergens:** dust mites, pets, pollen, foods (in infants)
- **Climate:** heat, sweating, low humidity
- **Stress:** exacerbations
- **Infection:** Staph aureus colonisation (common)

**MANAGEMENT:**

**1. Emollients (moisturisers) - CORNERSTONE OF THERAPY:**

**Use FREQUENTLY:**
- **Liberal application** (at least 2-3 times daily)
- **In abundance** (250-500 g per week for infants, 500 g for adults)
- **Even when skin clear** (prevention)

**Types:**
- **Lotions:** light, good for hairy areas, but need frequent application
- **Creams:** moisturising, cosmetically acceptable
- **Ointments:** most moisturising, greasy, best for dry skin

**Technique:**
- **Smooth in direction of hair growth**
- **Apply after bathing** (within 3 minutes)
- **Use medicated bath emollient** (instead of soap)
- **Use emollient soap substitute** (instead of soap)

**2. Anti-inflammatory therapy:**

**Topical Corticosteroids (TCS):**

**Potency ladder:**
- **Mild:** Hydrocortisone 0.5-1% (face, flexures, infants)
- **Moderate:** Clobetasone butyrate 0.05%, Eumovate
- **Potent:** Betamethasone valerate 0.1%, Mometasone 0.1%
- **Very potent:** Clobetasol propionate 0.05% (specialist use only)

**Fingertip units (FTU):**
- **1 FTU** = 0.5 g (from distal crease to fingertip)
- **Face + neck:** 2.5 FTU
- **One hand:** 1 FTU (both hands = 2 FTU)
- **One foot:** 2 FTU
- **One arm:** 3 FTU
- **One leg:** 6 FTU
- **Trunk (front + back):** 7 FTU each

**Application:**
- **Apply once daily** (BD for flares)
- **For 3-7 days** (then stop if improved, continue if needed)
- **Use sufficient quantity**
- **Step down potency** as improves
- **DO NOT fear steroids** (undertreatment worse than overtreatment)

**Calcineurin Inhibitors (TCI):**
- **Tacrolimus 0.03%/0.1%** ointment
- **Pimecrolimus 1%** cream
- **Indications:**
  - Sensitive areas (face, neck, genitalia) where TCS risk
  - Maintenance (twice weekly)
  - Steroid-sparing
- **Side effect:** burning/stinging (first few days)

**3. Pruritus (Itch) Control:**
- **Keep cool** (avoid overheating)
- **Keep fingernails short** (minimise damage from scratching)
- **Antihistamines** (sedating) at night:
  - **Chlorphenamine 4 mg** at night (child >1 year)
  - **Hydroxyzine** (child >6 months)
  - Does NOT reduce itch directly, but promotes sleep
  - **Non-sedating antihistamines** NOT effective for eczema itch

**4. Infection Control:**
- **Staph aureus** colonisation common
- **Infected eczema:** crusting, weeping, rapid worsening, fever
- **Treatment:**
  - **Flucloxacillin 500 mg QDS** (or 500 mg TDS for 5 days) OR
  - **Erythromycin 500 mg QDS** (if penicillin allergy)
  - **Topical antibiotics:** NOT recommended (resistance risk)
  - **Bleach baths** (for recurrent infection): 0.005% sodium hypochlorite

**5. Wet Wraps (for severe flares):**
- Apply emollient + topical steroid
- Cover with damp tubular bandage
- Leave for 12-24 hours
- **Hospital-only** or under dermatology supervision

**6. Systemic Therapy (specialist-initiated):**

**Phototherapy:**
- Narrowband UVB
- Twice weekly for 10-12 weeks
- Effective for moderate-severe eczema

**Immunosuppressants:**
- **Ciclosporin** (most commonly used)
- **Azathioprine**
- **Methotrexate**
- **Mycophenolate mofetil**

**Biologics:**
- **Dupilumab** (anti-IL4/13) - for moderate-severe eczema
- **Other biologics** (emerging)

**7. ALTERNATIVE THERAPIES:**

**Bleach Baths (dilute sodium hypochlorite):**
- **Indication:** recurrent Staph aureus infection
- **Recipe:** 1/2 cup household bleach in full bathtub (150 L)
- **Concentration:** 0.005%
- **Soak:** 5-10 minutes, twice weekly
- **Rinse** after bath
- **Apply emollient** immediately after

**PREVENTION:**
- **Avoid triggers** (identify and minimise)
- **Avoid irritants** (soaps, detergents, fragrances)
- **Wear cotton** (avoid wool, synthetic fabrics)
- **Keep cool** (overheating exacerbates)
- **Maintain skincare routine** (even when clear)
- **Recognise early signs of flare** (treat early)

**COMPLICATIONS:**
- **Infection** (bacterial, viral, fungal)
- **Eczema herpeticum** (widespread HSV - emergency!)
- **Psychological** (sleep disturbance, low self-esteem)
- **Growth failure** (severe, poorly controlled eczema)

**RED FLAGS (refer urgently):**
- **Eczema herpeticum:** fever, widespread painful erosions, punched-out lesions
- **Severe infection:** fever, cellulitis, systemic illness
- **Failure to thrive** (infants/children)
- **Psychological distress** (severe)

**Sources:** NICE NG57, BAD Guidelines, BSACI"""
        )

    def _handle_urticaria(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle urticaria/hives"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**URTICARIA (Hives)**

**DEFINITION:**
- Transient, pruritic, raised wheals (hives)
- Central swelling, often with erythematous flare
- Usually resolves within 24 hours (individual lesion)
- Can be acute (<6 weeks) or chronic (>6 weeks)

**TYPES:**

**1. Spontaneous Urticaria:**
- **Acute:** infection, food allergy, drug allergy
- **Chronic:** idiopathic (50%), autoimmune (30%), physical (20%)

**2. Inducible Urticaria (Physical):**
- **Dermatographic urticaria:** stroking skin
- **Cold urticaria:** cold exposure
- **Solar urticaria:** sunlight
- **Heat urticaria:** heat exposure
- **Cholinergic urticaria:** heat, emotion, exercise
- **Pressure urticaria:** sustained pressure
- **Vibratory angioedema:** vibration
- **Aquagenic urticaria:** water contact

**3. Other types:**
- **Contact urticaria:** direct skin contact (latex, foods)
- **Urticarial vasculitis:** painful, lasts >24 hours, purpuric

**PATHOPHYSIOLOGY:**
- **Mast cell degranulation** → histamine release
- IgE-mediated (allergic) OR non-IgE mediated
- Cutaneous inflammation and vasodilation

**DIAGNOSIS:**
- **Clinical diagnosis** (typical appearance)
- **History:** triggers, duration, associated symptoms (angioedema?)
- **Examination:** wheals (confirm urticaria), look for angioedema

**INVESTIGATIONS (if chronic or atypical):**
- **FBC, ESR/CRP** (infection, inflammation)
- **Autoantibodies:** thyroid (TPO antibodies), ANA
- **Specific IgE (RAST)** if allergic trigger suspected
- **Serum tryptase** (if systemic symptoms or anaphylaxis suspected)
- **Skin biopsy** (if urticarial vasculitis suspected)

**MANAGEMENT:**

**ACUTE URTICARIA (<6 weeks):**

**Identify and remove trigger (if possible):**
- **Food allergy:** recent food ingestion, onset <2 hours
- **Drug reaction:** recent medication (antibiotics, NSAIDs, ACE inhibitors)
- **Infection:** viral URTI, URI, bacterial infection
- **Physical stimuli:** cold, heat, pressure, sunlight

**Symptomatic treatment:**
1. **Non-sedating antihistamine** (first line):
   - **Cetirizine 10 mg** daily
   - **Loratadine 10 mg** daily
   - **Fexofenadine 120-180 mg** daily
   - Take regularly (not PRN) for better control

2. **Sedating antihistamine at night** (if severe itch affecting sleep):
   - **Chlorphenamine 4 mg** at night
   - **Hydroxyzine 25 mg** at night

3. **Corticosteroids (short course only):**
   - **Prednisolone 40 mg** daily for 3-5 days
   - For severe acute urticaria
   - **NOT for long-term** (side effects)

**CHRONIC URTICARIA (>6 weeks):**

**Stepwise approach:**

**Step 1: Standard dose non-sedating antihistamine**
- Cetirizine 10 mg daily OR Loratadine 10 mg daily
- Take **regularly** (not PRN)
- Continue for 4-6 weeks
- Reassess response

**Step 2: Increase to 4x standard dose (if inadequate response)**
- **Cetirizine 10 mg** → 10 mg TDS or 20 mg BD (up to 40 mg daily)
- **Loratadine 10 mg** → 10 mg QDS (up to 40 mg daily)
- **Off-label** but widely used, safe
- Monitor for sedation, anticholinergic side effects

**Step 3: Add second-line agent (if still inadequate):**
- **Montelukast 10 mg** daily (leukotriene receptor antagonist)
- Particularly for **autologous serum skin test (ASST) positive** or **aspirin-exacerbated**
- Add to high-dose antihistamine

**Step 4: Refer to specialist (dermatology/allergy) for:**
- **Omalizumab** (anti-IgE): highly effective, very expensive
- **Ciclosporin** (immunosuppressant): effective but significant side effects
- **Other immunosuppressants:** methotrexate, mycophenolate

**PHYSICAL URTICARIAS:**
- **Identify trigger** and avoid if possible
- **Standard dose antihistamine** (regular use)
- **Step up to high-dose** if inadequate
- **Montelukast** may help (especially cold urticaria)
- **Desensitisation** (for cold urticaria) - specialist only

**ANGIOEDEMA WITH URTICARIA:**
- **Same management** (antihistamines, steroids)
- **Monitor airway** (facial swelling → airway risk)
- **Emergency treatment** if airway involvement

**PROGNOSIS:**
- **Acute:** self-limiting (days to weeks)
- **Chronic:** average duration 2-5 years, but can be longer
- **Spontaneous remission** in 50% within 1 year, 80% within 5 years

**TRIGGERS TO AVOID (if identified):**
- **Aspirin and NSAIDs** (worsen 20-30% of chronic urticaria)
- **Alcohol** (vasodilation)
- **Heat, stress** (cholinergic urticaria)
- **Pressure** (tight clothing, straps)

**Sources:** BSACI Guidelines for Urticaria, NICE NG134"""
        )

    def _handle_food_allergy(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle food allergy"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**FOOD ALLERGY**

**DEFINITION:**
- Adverse immune response to food protein
- **IgE-mediated** (immediate) or **non-IgE mediated** (delayed)
- **Distinct from food intolerance** (non-immune)

**PREVALENCE:**
- 6-8% children, 2-4% adults
- Increasing over time

**COMMON ALLERGENS (The "Big 8"):**
1. **Peanuts** (legume)
2. **Tree nuts** (almond, cashew, walnut, pistachio, brazil, hazelnut, pecan)
3. **Shellfish** (shrimp, crab, lobster, crayfish)
4. **Fish** (cod, salmon, tuna)
5. **Milk** (cow's milk)
6. **Egg** (chicken egg)
7. **Soy**
8. **Wheat**

**Others:** sesame, mustard, lupin, molluscs

**IgE-MEDIATED FOOD ALLERGY (Immediate):**

**Onset:** minutes to 2 hours after ingestion

**Symptoms:**
- **Cutaneous:** urticaria (hives), angioedema, flushing, pruritus
- **Respiratory:** wheeze, cough, stridor, dyspnoea
- **Gastrointestinal:** nausea, vomiting, abdominal pain, diarrhoea
- **Cardiovascular:** hypotension, tachycardia, collapse
- **Anaphylaxis:** multi-system involvement, life-threatening

**Risk factors for severe reaction:**
- Asthma (especially poorly controlled)
- Previous severe reaction
- Peanut/tree nut allergy
- Teenagers/young adults
- Delayed epinephrine administration

**NON-IGE-MEDIATED FOOD ALLERGY (Delayed):**

**Onset:** hours to days after ingestion

**Types:**
- **Food protein-induced enterocolitis syndrome (FPIES):**
  - Vomiting, diarrhoea, dehydration (1-4 hours after ingestion)
  - Milk, soy, rice, oat (common triggers)
  - Infants/young children
  - **NOT IgE-mediated** (skin prick/RAST negative)
- **Food protein-induced allergic proctocolitis:**
  - Blood-streaked stools in infants
  - Milk/soy protein (via breast milk or formula)
  - Resolves by age 1-2 years
- **Celiac disease** (gluten)
- **Eosinophilic esophagitis/gastroenteritis**

**DIAGNOSIS:**

**History:**
- **Timing:** immediate vs. delayed
- **Specific food:** amount, preparation (raw vs. cooked)
- **Symptoms:** detailed description
- **Previous reactions:** pattern, severity
- **Atopic history:** asthma, eczema, allergic rhinitis

**Skin Prick Testing (SPT):**
- **Positive:** wheal ≥3 mm than negative control
- **False positives** common (sensitisation ≠ clinical allergy)
- **Negative:** high negative predictive value (rules out allergy)
- **Do NOT test:** if history of anaphylaxis to specific food

**Specific IgE (RAST):**
- **Positive:** ≥0.35 kU/L
- **Correlates with severity** (peanuts, tree nuts, milk, egg)
- **Not diagnostic alone** (must correlate with history)

**Oral Food Challenge (OFC):**
- **Gold standard** for diagnosis
- **Supervised medical setting** (resuscitation equipment available)
- **Gradual incremental dosing**
- **Positive:** objective allergic reaction
- **Negative:** can introduce food into diet

**Component-Resolved Diagnostics:**
- **Specific protein components** (e.g., Ara h 2 for peanut)
- **Differentiates sensitisation from true allergy**
- **Predicts severity**

**MANAGEMENT:**

**1. Strict Avoidance:**
- **Read food labels** meticulously
- **Hidden allergens** (e.g., peanut in sauces, milk in baked goods)
- **Cross-contamination** (shared utensils, fryers)
- **Restaurant meals:** inform staff of allergy, ask about ingredients

**2. Emergency Treatment:**

**Adrenaline autoinjector:**
- **Prescribe for:** all patients with previous anaphylaxis, or high-risk foods (peanuts, tree nuts)
- **Two devices** prescribed (always carry spare)
- **Training:** proper technique (video + in-person)
- **Review:** every 1-2 years

**Antihistamine:**
- Cetirizine or Loratadine for mild reactions only
- **NOT for anaphylaxis** (adrenaline first)

**3. Allergy Action Plan:**
- **Written instructions** for managing reactions
- **When to use adrenaline**
- **When to call emergency services**
- **Distribute** to family, school, workplace

**4. Identification:**
- **Medical alert bracelet/necklace**
- **Carry emergency card** (allergy details)

**5. Education:**
- **Avoidance strategies**
- **Recognition of allergic reactions**
- **Use of adrenaline autoinjector**
- **Label reading**

**PROGNOSIS:**

**Resolution rates:**
- **Milk:** 80% by age 16
- **Egg:** 70% by age 16
- **Soy/Wheat:** 70% by age 10
- **Peanut:** 20% by age 16 (most persistent)
- **Tree nuts:** 10% by age 20 (most persistent)
- **Shellfish/fish:** usually lifelong

**Predictors of persistence:**
- High specific IgE levels
- Severe initial reaction
- Peanut/tree nut allergy
- Older age of onset

**PREVENTION:**

**For infants at high risk (allergic disease in first-degree relative):**
- **Exclusive breastfeeding** for 4-6 months
- **Introduce allergenic foods** (peanut, egg) at 6-12 months (after weaning started)
- **DO NOT delay** introduction of allergenic foods
- **Consider early introduction** (4-6 months) after specialist assessment

**Oral immunotherapy (OIT):**
- **Specialist-only** (clinical trial setting)
- **Gradual desensitisation** to allergenic food (peanut, milk, egg)
- **Aim:** increase threshold for reaction, reduce anaphylaxis risk
- **NOT cure** (must continue regular exposure)

**Sources:** BSACI Guidelines for Food Allergy, NICE NG134"""
        )

    def _handle_drug_allergy(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle drug allergy"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**DRUG ALLERGY**

**DEFINITION:**
- Adverse drug reaction with immunological mechanism
- **IgE-mediated** (immediate) or **non-IgE mediated** (delayed)
- **Distinct from adverse drug reaction** (non-immune)

**PREVALENCE:**
- Affects 10-20% of hospitalized patients
- Up to 30% of patients report "penicillin allergy" (but <10% truly allergic)

**COMMON DRUG ALLERGENS:**

**Antibiotics (most common):**
- **Beta-lactams:** Penicillins, Cephalosporins, Carbapenems
- **Sulfonamides:** Co-trimoxazole (Septrin)
- **Macrolides:** Erythromycin, Clarithromycin (rare)
- **Fluoroquinolones:** Ciprofloxacin, Moxifloxacin (rare)

**Other:**
- **NSAIDs:** Aspirin, Ibuprofen, Diclofenac (cross-reactivity common)
- **Opioids:** Morphine, Codeine
- **Anaesthetic agents:** Neuromuscular blocking agents, Latex
- **Radiocontrast media**
- **Vaccines** (egg-containing, gelatin)

**CLASSIFICATION:**

**1. Immediate (IgE-mediated):**
- **Onset:** minutes to 1-2 hours after drug administration
- **Mechanism:** IgE antibodies to drug (or metabolite)
- **Reactions:** Urticaria, angioedema, bronchospasm, anaphylaxis
- **Examples:** Penicillin anaphylaxis, NSAID-induced urticaria

**2. Delayed (non-IgE mediated or T-cell mediated):**
- **Onset:** hours to days (or weeks) after drug exposure
- **Mechanism:** T-cell mediated, immune complex, or direct mast cell activation
- **Reactions:**
  - **Maculopapular rash** (most common)
  - **SJS/TEN** (severe blistering)
  - **DRESS** (Drug Reaction with Eosinophilia and Systemic Symptoms)
  - **Serum sickness-like reaction**
  - **Drug-induced hepatitis, nephritis**

**PENICILLIN ALLERGY:**

**Prevalence:**
- **10%** of patients report penicillin allergy
- **<10%** of these are truly allergic (penicillin skin test positive)
- **90%** can tolerate penicillins (tolerance preserved)

**Cross-reactivity:**
- **Penicillins → Cephalosporins:** 1-2% cross-reactivity (much lower than historically thought)
- **Penicillins → Carbapenems:** <1% cross-reactivity
- **Penicillins → Monobactams (Aztreonam):** negligible cross-reactivity

**Evaluation:**

**History:**
- **Reaction:** timing, symptoms, treatment received
- **Immediate:** urticaria, angioedema, wheeze, anaphylaxis (within 1-2 hours)
- **Delayed:** rash >72 hours, SJS/TEN, DRESS
- **Timing:** how long ago?
- **Subsequent:** penicillin received since? (tolerated?)

**Skin testing:**
- **Indicated:** if history of immediate reaction, or unclear history
- **Penicillin skin test:** Pre-pen + Penicillin G (major and minor determinants)
- **Negative:** 97-99% can tolerate penicillin
- **Positive:** avoid penicillins (and consider cephalosporins with caution)

**Graded challenge (test dose):**
- **Indicated:** if history is vague, or skin test negative
- **Supervised medical setting**
- **Gradual incremental dosing** (10%, 25%, 50%, 100% of full dose)
- **Observation:** 30-60 minutes after each dose

**Management:**

**If TRUE penicillin allergy:**
- **Avoid:** all penicillins (Penicillin V, Amoxicillin, Augmentin, Flucloxacillin)
- **Avoid:** cephalosporins (especially 1st generation) - cross-reactivity risk
- **Use:** macrolides (Erythromycin, Clarithromycin), clindamycin, doxycycline
- **Warn:** inform all healthcare providers of allergy
- **Wear:** medical alert bracelet (if severe reaction)

**If NOT true penicillin allergy:**
- **De-label** "penicillin allergy"
- **Document:** tolerance confirmed
- **Use penicillins** (first-line for many infections)

**NSAID ALLERGY:**

**Mechanism:**
- **COX-1 inhibition** → increased leukotriene production
- **NOT IgE-mediated**
- **Cross-reactivity:** common among traditional NSAIDs

**Types:**

**1. NSAID-exacerbated respiratory disease (NERD):**
- **Patients:** asthma, chronic urticaria, nasal polyps
- **Reaction:** bronchospasm, urticaria, angioedema
- **Trigger:** aspirin, ibuprofen, naproxen, diclofenac (most traditional NSAIDs)
- **Safe:** COX-2 inhibitors (Celecoxib, Etoricoxib)

**2. NSAID-exacerbated cutaneous disease (NECD):**
- **Patients:** chronic urticaria
- **Reaction:** urticaria, angioedema
- **Trigger:** aspirin, most NSAIDs
- **Safe:** paracetamol, COX-2 inhibitors (usually)

**3. Single NSAID-induced reaction:**
- **IgE-mediated** to specific NSAID
- **Reaction:** urticaria, anaphylaxis
- **Safe:** other NSAIDs (no cross-reactivity)

**Management:**
- **Avoid:** all NSAIDs that trigger reactions
- **Use:** paracetamol, COX-2 inhibitors (if respiratory exacerbation)
- **Desensitisation:** aspirin desensitisation (if required for cardiovascular disease)

**ANTIBIOTIC-INDUCED SEVERE CUTANEOUS ADVERSE REACTIONS (SCARs):**

**Stevens-Johnson Syndrome (SJS) / Toxic Epidermal Necrolysis (TEN):**
- **Incidence:** 1-2 per million per year
- **Drugs:** Allopurinol, Carbamazepine, Lamotrigine, Sulfonamides, NSAIDs, Penicillins
- **Onset:** 1-4 weeks after drug initiation
- **Symptoms:** fever, mucosal involvement, widespread bullae, epidermal detachment
- **Severity:** SJS (<10% BSA), SJS/TEN overlap (10-30%), TEN (>30%)
- **Mortality:** 10-30% (higher in TEN)
- **Management:** **STOP DRUG**, **ADMIT** to burns unit/ITU, supportive care, **NO rechallenge**

**DRESS (Drug Reaction with Eosinophilia and Systemic Symptoms):**
- **Incidence:** 1 in 1000-10,000
- **Drugs:** Carbamazepine, Lamotrigine, Phenytoin, Allopurinol, Sulfonamides
- **Onset:** 2-8 weeks after drug initiation
- **Symptoms:** fever, rash, facial edema, eosinophilia, abnormal LFTs, renal impairment
- **Mortality:** 10-20%
- **Management:** **STOP DRUG**, systemic steroids, **NO rechallenge**

**EVALUATION OF DRUG ALLERGY:**

**History:**
- **Drug:** name, dose, route, formulation
- **Timing:** onset, duration
- **Symptoms:** detailed description
- **Treatment:** required? (hospitalisation, adrenaline)
- **Rechallenge:** drug taken since? (tolerated?)

**Investigations:**

**Skin testing:**
- **Indicated:** IgE-mediated reactions (penicillin, neuromuscular blocking agents)
- **Prick testing** (immediate hypersensitivity)
- **Intradermal testing** (if prick test negative)
- **Patch testing** (delayed hypersensitivity)

**Specific IgE (RAST):**
- **Available:** penicillin (minor determinant not available), neuromuscular blocking agents, latex
- **Not available:** most other drugs

**Drug provocation test (graded challenge):**
- **Gold standard** for diagnosis
- **Indicated:** non-severe reactions, low-risk patients, skin test negative
- **Supervised medical setting** (resuscitation equipment available)

**MANAGEMENT:**

**1. Discontinue offending drug**

**2. Symptomatic treatment:**
- **Mild (urticaria only):** antihistamine (cetirizine 10 mg)
- **Moderate (angioedema, bronchospasm):** adrenaline IM + antihistamine + steroids
- **Severe (anaphylaxis):** adrenaline IM + antihistamine + steroids + fluids

**3. Education:**
- **Avoidance:** drug and cross-reactive drugs
- **Medical alert bracelet** (if severe reaction)
- **Inform all healthcare providers**
- **Documentation:** clearly document allergy in medical records

**4. Alternatives:**
- **Choose:** different drug class
- **Desensitisation:** if no alternative (e.g., penicillin for syphilis, chemotherapy)

**Sources:** BSACI Guidelines for Drug Allergy, NICE NG134"""
        )

    def _handle_immunodeficiency(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle immunodeficiency"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**PRIMARY IMMUNODEFICIENCY (PID)**

**DEFINITION:**
- Inherited defects in immune system
- **Broad spectrum:** from mild to life-threatening
- **Often underdiagnosed** (median diagnostic delay: 4-9 years)

**WARNING SIGNS (10 warning signs - Jeffrey Modell Foundation):**

1. **≥8 ear infections** within 1 year
2. **≥2 serious sinus infections** within 1 year
3. **≥2 months on antibiotics** with little effect
4. **≥2 episodes of pneumonia** within 1 year
5. **Failure of an infant** to gain weight or grow normally
6. **Deep-seated infections** (abscesses, organ infections)
7. **Persistent thrush** in mouth or fungal infection on skin
8. **Need for IV antibiotics** to clear infections
9. **≥2 deep-seated infections** (septicaemia, meningitis, osteomyelitis)
10. **Family history** of primary immunodeficiency

**CLASSIFICATION:**

**1. Antibody Deficiencies (B-cell defects):**

**Common Variable Immunodeficiency (CVID):**
- **Epidemiology:** 1:25,000
- **Onset:** adolescence/adulthood (can be earlier)
- **Pathophysiology:** failure of B-cell differentiation to plasma cells
- **Presentation:** recurrent sinopulmonary infections (pneumonia, sinusitis, otitis media)
- **Complications:** bronchiectasis, autoimmune disease, lymphoma
- **Diagnosis:** low IgG, IgA, and/or IgM; poor vaccine response
- **Treatment:** immunoglobulin replacement (IVIG or SCIG) + antibiotics

**X-linked Agammaglobulinaemia (Bruton's):**
- **Epidemiology:** 1:200,000 (male only)
- **Genetics:** mutation in BTK gene (X-linked)
- **Onset:** 6-12 months (after maternal antibodies wane)
- **Pathophysiology:** block in B-cell maturation → no B cells, low all immunoglobulins
- **Presentation:** recurrent bacterial infections (pneumonia, otitis media, sinusitis, sepsis)
- **Pathogens:** encapsulated bacteria (Strep pneumo, H. flu, Staph aureus)
- **Diagnosis:** very low B cells (<1%), low all immunoglobulins
- **Treatment:** immunoglobulin replacement + antibiotics

**Selective IgA Deficiency:**
- **Epidemiology:** 1:400 (most common PID)
- **Pathophysiology:** isolated IgA deficiency
- **Presentation:** often asymptomatic; recurrent sinopulmonary, GI infections
- **Associations:** autoimmune disease, allergy
- **Diagnosis:** low IgA (<7 mg/dL), normal IgG, IgM
- **Treatment:** usually none; antibiotics for infections; **NO IVIG** (anti-IgA antibodies → anaphylaxis)

**Specific Antibody Deficiency:**
- **Normal immunoglobulin levels**
- **Poor vaccine response** (fail to mount protective antibody titres)
- **Presentation:** recurrent infections with encapsulated bacteria
- **Treatment:** immunoglobulin replacement (if severe) or antibiotic prophylaxis

**2. Combined Immunodeficiencies (T-cell + B-cell defects):**

**Severe Combined Immunodeficiency (SCID):**
- **Epidemiology:** 1:50,000-100,000
- **Genetics:** multiple genetic defects (X-linked, ADA deficiency, etc.)
- **Onset:** first months of life
- **Presentation:** failure to thrive, severe, persistent infections (bacterial, viral, fungal, opportunistic), chronic diarrhoea
- **Pathogens:** all types (PCP, CMV, Candida, bacteria, viruses)
- **Diagnosis:** very low T cells, low B cells, low NK cells; low lymphocytes
- **Treatment:** **haematopoietic stem cell transplantation (HSCT)** (curative); immunoglobulin replacement; antibiotic/antifungal prophylaxis

**3. Phagocytic Defects:**

**Chronic Granulomatous Disease (CGD):**
- **Epidemiology:** 1:200,000
- **Genetics:** X-linked (70%) or autosomal recessive (30%)
- **Pathophysiology:** defect in NADPH oxidase → impaired killing of catalase-positive organisms
- **Presentation:** recurrent infections with catalase-positive organisms (Staph aureus, Serratia, Burkholderia, Aspergillus); granuloma formation
- **Infections:** abscesses (skin, liver, lymph nodes), pneumonia, osteomyelitis
- **Diagnosis:** nitroblue tetrazolium (NBT) test or dihydrorhodamine (DHR) flow cytometry
- **Treatment:** antibiotic and antifungal prophylaxis; interferon-gamma; HSCT (severe)

**4. Complement Deficiencies:**
- **Early complement components (C1, C2, C4):** autoimmune disease (SLE-like)
- **C3 deficiency:** recurrent sinopulmonary infections (similar to antibody deficiency)
- **C5-C9 deficiency (terminal complement):** recurrent Neisseria infections (meningococcus, gonococcus)
- **Diagnosis:** complement assays (CH50, AH50)
- **Treatment:** meningococcal vaccination; antibiotic prophylaxis (for C5-C9)

**DIAGNOSTIC APPROACH:**

**1. Screening tests:**
- **FBC with differential** (lymphocyte subsets)
- **Immunoglobulin levels** (IgG, IgA, IgM)
- **Vaccine response** (tetanus, pneumococcal titres)
- **Complement levels** (C3, C4, CH50)
- **HIV test** (rule out secondary immunodeficiency)

**2. Specialised tests (if screening abnormal or clinical suspicion high):**
- **Lymphocyte subsets** (T cells, B cells, NK cells)
- **Functional assays:** nitroblue tetrazolium test (CGD), flow cytometry (DHR)
- **Genetic testing:** next-generation sequencing panels
- **Specialist referral:** immunology

**MANAGEMENT:**

**1. Immunoglobulin Replacement:**
- **Indications:** antibody deficiency (CVID, XLA, SCID)
- **Preparations:**
  - **IVIG:** intravenous (every 3-4 weeks)
  - **SCIG:** subcutaneous (weekly or more frequent)
- **Dose:** 400-600 mg/kg/month
- **Target:** trough IgG level >7 g/L (or higher if infections persist)

**2. Antibiotic Prophylaxis:**
- **Antibody deficiency:** sometimes indicated (if recurrent infections despite IVIG)
- **Phagocytic defect:** always indicated
  - **CGD:** Trimethoprim-sulfamethoxazole (PCP prophylaxis)
  - **Antifungal:** Itraconazole (Aspergillus prophylaxis)

**3. Live Vaccines:**
- **CONTRAINDICATED** in severe T-cell deficiencies (SCID)
- **Safe:** in antibody deficiencies (CVID, XLA)

**4. Monitoring:**
- **Clinical:** infection frequency, severity
- **Laboratory:** immunoglobulin levels (trough levels), lung function (if bronchiectasis)
- **Complications:** bronchiectasis, autoimmune disease, lymphoma

**PROGNOSIS:**
- **Mild:** normal lifespan with appropriate treatment
- **Severe (SCID):** fatal within first 2 years without HSCT
- **CVID:** good with immunoglobulin replacement, but increased risk of complications

**Sources:** UK Primary Immunodeficiency Network, Jeffrey Modell Foundation, NICE NG134"""
        )

    def _handle_general_allergy(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general allergy query"""
        return DomainQueryResult(
            domain_name="allergy_immunology",
            answer="""**ALLERGY & IMMUNOLOGY - General Consultation**

Allergy and Immunology covers diagnosis and management of allergic diseases and immunodeficiency disorders.

**COMMON ALLERGIC CONDITIONS:**

**Respiratory:**
- Allergic rhinitis (hay fever)
- Asthma (allergic)
- Allergic bronchopulmonary aspergillosis (ABPA)

**Skin:**
- Atopic dermatitis (eczema)
- Urticaria (hives)
- Angioedema
- Allergic contact dermatitis

**Drug:**
- Penicillin allergy
- NSAID allergy
- Anaphylaxis

**Food:**
- Peanut allergy
- Tree nut allergy
- Shellfish allergy
- Milk/egg allergy
- Food protein-induced enterocolitis syndrome (FPIES)

**Insect venom:**
- Bee sting allergy
- Wasp sting allergy

**IMMUNODEFICIENCY DISORDERS:**

**Antibody deficiency:**
- Common Variable Immunodeficiency (CVID)
- X-linked Agammaglobulinaemia
- Selective IgA deficiency
- Specific antibody deficiency

**Combined immunodeficiency:**
- Severe Combined Immunodeficiency (SCID)

**Phagocytic defect:**
- Chronic Granulomatous Disease (CGD)

**Complement deficiency:**
- Early complement deficiency (autoimmunity)
- Terminal complement deficiency (meningococcal infections)

**ALLERGY INVESTIGATIONS:**

**Skin testing:**
- Skin prick testing (SPT)
- Intradermal testing
- Patch testing (delayed hypersensitivity)

**Blood tests:**
- Specific IgE (RAST)
- Serum tryptase (anaphylaxis)
- Immunoglobulin levels (IgG, IgA, IgM)
- Lymphocyte subsets
- Complement levels (C3, C4)

**Challenge testing:**
- Oral food challenge (OFC)
- Drug provocation test (DPT)
- Bronchial challenge

**IMMUNOTHERAPY:**

**Allergen immunotherapy (desensitisation):**
- **Subcutaneous (SCIT):** injections
- **Sublingual (SLIT):** drops/tablets
- **Indications:** allergic rhinitis, venom allergy
- **Duration:** 3-5 years
- **Effect:** disease modification (long-term benefit)

**Drug desensitisation:**
- **Indication:** no alternative drug available
- **Examples:** penicillin, aspirin, chemotherapy
- **Specialist-only** (supervised medical setting)

**When to refer URGENTLY:**
- Anaphylaxis (refer to allergy clinic for investigation)
- Angioedema (if airway involvement)
- Severe asthma attack
- Suspected immunodeficiency (recurrent, severe infections)

**When to refer ROUTINELY:**
- Allergic rhinitis (if moderate-severe, or not responding to treatment)
- Asthma (if poor control)
- Eczema (if moderate-severe, or not responding to optimised therapy)
- Chronic urticaria (>6 weeks)
- Possible food allergy (for investigation)
- Possible drug allergy (for evaluation, testing, de-labelling)
- Recurrent infections (possible immunodeficiency)

**Sources:** BSACI Guidelines, NICE Guidelines, AAAAI Guidelines"""
        )


def create_allergy_immunology_domain():
    """Factory function to create allergy/immunology domain"""
    return AllergyImmunologyDomain()
