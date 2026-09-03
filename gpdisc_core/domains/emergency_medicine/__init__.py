"""
Emergency Medicine Domain for GPDISC

Comprehensive emergency medicine consultation covering:
- Emergency triage and resuscitation
- Cardiac emergencies (ACS, arrhythmias, cardiac arrest)
- Respiratory emergencies (asthma, PE, pneumonia, pneumothorax)
- Neurological emergencies (stroke, seizure, meningitis)
- Trauma (head injury, fractures, burns, wounds)
- Surgical emergencies (appendicitis, cholecystitis, bowel obstruction)
- Toxicology (overdose, poisoning)
- Pediatric emergencies

Evidence-based guidelines:
- Resuscitation Council (UK)
- NICE NGxx guidelines
- ACEP (American College of Emergency Physicians)
- Royal College of Emergency Medicine
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class EmergencyMedicineDomain(BaseDomainModule):
    """
    Emergency Medicine domain for comprehensive emergency consultation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="emergency_medicine",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive emergency medicine: cardiac emergencies, respiratory emergencies, neurological emergencies, trauma, toxicology, pediatric emergencies",
            keywords=[
                "emergency", "emergency department", "ed", "a&e", "er", "accident and emergency",
                "cardiac arrest", "cpr", "defibrillation", "als", "bls",
                "heart attack", "myocardial infarction", "chest pain", "acs",
                "arrhythmia", "af", "atrial fibrillation", "svt", "vt", "vf",
                "stroke", "tia", "transient ischaemic attack", "fast",
                "seizure", "epilepsy", "convulsion", "status epilepticus",
                "asthma attack", "acute asthma", "pe", "pulmonary embolism",
                "pneumothorax", "tension pneumothorax", "chest trauma",
                "meningitis", "sepsis", "septic shock", "anaphylaxis",
                "trauma", "head injury", "concussion", "fracture", "burns",
                "appendicitis", "cholecystitis", "bowel obstruction",
                "overdose", "poisoning", "toxicology", "paracetamol", "opioid",
                "triage", "resuscitation", "emergency medicine"
            ],
            capabilities=[
                "emergency_triage",
                "cardiac_emergency_management",
                "respiratory_emergency_management",
                "neurological_emergency_management",
                "trauma_assessment",
                "toxicology_management",
                "pediatric_emergency",
                "resuscitation"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process emergency medicine query with immediate triage
        """
        query_lower = query.lower()

        # LIFE-THREATENING EMERGENCIES - HIGHEST PRIORITY

        # Cardiac arrest
        if any(term in query_lower for term in ["cardiac arrest", "cpr", "no pulse", "unconscious not breathing",
                                                   "vf", "ventricular fibrillation", "pulseless vt"]):
            return self._handle_cardiac_arrest(query, context)

        # Anaphylaxis
        if any(term in query_lower for term in ["anaphylaxis", "anaphylactic shock", "severe allergic reaction",
                                                   "airway swelling", "throat closing"]):
            return self._handle_anaphylaxis(query, context)

        # Septic shock
        if any(term in query_lower for term in ["septic shock", "severe sepsis", "sepsis"]):
            return self._handle_septic_shock(query, context)

        # CARDIAC EMERGENCIES

        # ACS / Heart attack
        if any(term in query_lower for term in ["heart attack", "myocardial infarction", "mi", "chest pain",
                                                   "acute coronary syndrome", "acs", "stemi", "nstemi"]):
            return self._handle_acs(query, context)

        # Arrhythmias
        if any(term in query_lower for term in ["arrhythmia", "atrial fibrillation", "af", "svt",
                                                   "supraventricular tachycardia", "ventricular tachycardia", "vt"]):
            return self._handle_arrhythmia(query, context)

        # RESPIRATORY EMERGENCIES

        # Acute severe asthma
        if any(term in query_lower for term in ["acute asthma", "asthma attack", "severe asthma", "status asthmaticus"]):
            return self._handle_acute_asthma(query, context)

        # Pulmonary embolism
        if any(term in query_lower for term in ["pulmonary embolism", "pe", "blood clot in lung"]):
            return self._handle_pulmonary_embolism(query, context)

        # Pneumothorax
        if any(term in query_lower for term in ["pneumothorax", "tension pneumothorax", "collapsed lung",
                                                   "chest trauma"]):
            return self._handle_pneumothorax(query, context)

        # NEUROLOGICAL EMERGENCIES

        # Stroke
        if any(term in query_lower for term in ["stroke", "cva", "cerebrovascular accident", "brain attack",
                                                   "fast", "facial droop", "arm weakness", "speech difficulty"]):
            return self._handle_stroke(query, context)

        # Seizure / Status epilepticus
        if any(term in query_lower for term in ["seizure", "epilepsy", "convulsion", "fit",
                                                   "status epilepticus", "prolonged seizure"]):
            return self._handle_seizure(query, context)

        # Meningitis
        if any(term in query_lower for term in ["meningitis", "meningeal signs", "neck stiffness",
                                                   "photophobia", "headache fever"]):
            return self._handle_meningitis(query, context)

        # TRAUMA

        # Head injury
        if any(term in query_lower for term in ["head injury", "concussion", "head trauma", "traumatic brain injury"]):
            return self._handle_head_injury(query, context)

        # Burns
        if any(term in query_lower for term in ["burn", "burns", "scald", "thermal injury"]):
            return self._handle_burns(query, context)

        # TOXICOLOGY

        # Overdose / Poisoning
        if any(term in query_lower for term in ["overdose", "poisoning", "toxicology", "paracetamol overdose",
                                                   "opioid overdose", "ingestion"]):
            return self._handle_overdose(query, context)

        # GENERAL EMERGENCY
        return self._handle_general_emergency(query, context)

    def _handle_cardiac_arrest(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle cardiac arrest"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**CARDIAC ARREST - LIFE-THREATENING EMERGENCY**

**IMMEDIATE ACTION:**
- **CALL FOR HELP** / Call emergency services (999/911)
- **START CPR IMMEDIATELY** if unconscious, not breathing normally
- **DEFIBRILLATE ASAP** if VF/VT (shockable rhythm)

**ALS (ADVANCED LIFE SUPPORT) - UNIVERSAL ALGORITHM:**

**1. Shockable Rhythms (VF/pVT):**
   - **1st shock:** Immediate defibrillation (150-200 J biphasic)
   - **CPR:** 2 minutes (resume immediately after shock)
   - **Adrenaline:** 1 mg IV after 2nd shock (then every 3-5 minutes)
   - **Amiodarone:** 300 mg IV after 3rd shock
   - **2nd shock:** After 2 min CPR (150-200 J)
   - **3rd shock:** After 2 min CPR (150-200 J)
   - **Repeat:** CPR 2 min → shock 150-200 J (continue)

**2. Non-shockable Rhythms (PEA/Asystole):**
   - **CPR:** 2 minutes (continuous, minimal interruptions)
   - **Adrenaline:** 1 mg IV ASAP (then every 3-5 minutes)
   - **Reversible causes:** identify and treat
   - **Repeat:** CPR 2 min → adrenaline 1 mg (continue)

**QUALITY CPR:**
- **Rate:** 100-120 compressions/minute
- **Depth:** 5-6 cm (adults)
- **Recoil:** allow full chest recoil
- **Ratio:** 30:2 (compression:ventilation) if single rescuer
- **Minimise interruptions:** chest compression fraction >60%
- **Switch rescuers:** every 2 minutes (to prevent fatigue)

**AIRWAY & BREATHING:**
- **Head tilt-chin lift** (unless trauma → jaw thrust)
- **Oropharyngeal airway** (Guedel) or **Nasopharyngeal airway**
- **Bag-mask ventilation:** 15 L/min O2, 1:2 compression:ventilation ratio (30:2)
- **Advanced airway:** (supraglottic or endotracheal) when available
   - Once advanced airway placed: continuous compressions, 10 breaths/min

**DEFIBRILLATION:**
- **Pads placement:**
   - **Anterolateral:** right upper chest, left lateral chest (standard)
   - **Anteroposterior:** right upper chest, left back (if anterolateral not possible)
- **Energy:**
   - **Biphasic:** 150-200 J (manufacturer recommendation)
   - **Monophasic:** 360 J
- **Safety:** ensure rescuer clear before shocking

**REVERSIBLE CAUSES (4H4T):**
- **Hypoxia:** (hypoxaemia, airway obstruction)
- **Hypovolaemia:** (haemorrhage, dehydration)
- **Hypo/hyperkalaemia:** (electrolyte abnormalities)
- **Hypothermia:** (accidental hypothermia)
- **Tension pneumothorax:** (decompression needed)
- **Tamponade (cardiac):** (pericardiocentesis needed)
- **Thrombosis (coronary):** (consider PCI, thrombolysis)
- **Thrombosis (pulmonary):** (consider thrombolysis)

**POST-RESUSCITATION CARE:**

**Optimisation:**
- **Airway:** advanced airway, capnography (EtCO2 35-40 mmHg)
- **Breathing:** SpO2 94-98%, ventilation 6-8 breaths/min
- **Circulation:** MAP >65 mmHg, central venous access, cardiac monitoring
- **Disability:** GCS, pupils, glucose (normoglycaemia)

**Targeted temperature management:**
- **Comatose survivors** of VF/VT cardiac arrest
- **Cool to 32-36°C** for at least 24 hours
- **Prevent fever:** <37.5°C

**Identify cause:**
- **12-lead ECG** (ACS, STEMI)
- **Chest X-ray** (pneumothorax, pulmonary oedema)
- **ABG** (hypoxia, acidosis, hypercapnia)
- **Blood tests:** (FBC, U&E, glucose, troponin, lactate)
- **CT brain** (if ROSC but GCS not improving)

**WITHHOLDING CPR:**
- **If obviously dead** (rigor mortis, dependent lividity, decapitation, decomposition)
- **If no benefit:** (terminal illness, death inevitable)
- **Advance decision:** (DNACPR - valid, applicable to current situation)

**Sources:** Resuscitation Council (UK), ERC Guidelines 2021"""
        )

    def _handle_anaphylaxis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle anaphylaxis"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**ANAPHYLAXIS - LIFE-THREATENING EMERGENCY**

**IMMEDIATE ACTION:**
- **CALL FOR HELP** / Call emergency services (999/911)
- **ADMINISTER IM ADRENALINE (EPINEPHRINE) IMMEDIATELY**
- **Do NOT delay for investigation**

**DIAGNOSIS (clinical):**
Anaphylaxis is **HIGHLY LIKELY** if ANY of following:

1. **Acute onset** (minutes to hours) with:
   - Skin/mucosal involvement (urticaria, itch, flush, swelling) AND
   - Respiratory compromise (wheeze, stridor, dyspnoea) OR
   - Reduced BP or associated symptoms (collapse, syncope)

2. **Two or more** of following after allergen exposure:
   - Skin/mucosal involvement
   - Respiratory compromise
   - Reduced BP or associated symptoms
   - Persistent GI symptoms (crampy pain, vomiting)

3. **Reduced BP** after known allergen:
   - Adults: systolic BP <90 mmHg or >30% drop
   - Children: low systolic BP (age-specific) or >30% drop

**IMMEDIATE MANAGEMENT:**

**1. Adrenaline (EPINEPHRINE) - FIRST LINE, DO NOT DELAY:**
- **IM injection** into anterolateral thigh (vastus lateralis)
- **Adults:** 0.5 mg IM (0.5 mL of 1:1000)
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
- **Crystalloid bolus** (500-1000 mL rapid)
- Repeat as needed (shock may require large volumes)

**7. Adjunctive therapies:**

**Antihistamines (H1 blocker):**
- Diphenhydramine 25-50 mg IV/IM OR Cetirizine 10 mg IV/PO
- **Do NOT use** as first-line or sole treatment

**Corticosteroids:**
- Methylprednisolone 100 mg IV or Hydrocortisone 200 mg IV
- Takes 4-6 hours to work
- May prevent biphasic reaction

**Bronchodilators:**
- Salbutamol 5 mg nebulised (if wheezing)

**8. Refractory anaphylaxis:**
- **Adrenaline infusion:** start 0.05-0.1 mcg/kg/min, titrate

**BIPHASIC REACTION:**
- Occurs in up to 20%
- Symptoms recur 1-72 hours (usually 8-12 hours)
- **Observe for 6-12 hours**

**Sources:** Resuscitation Council (UK), BSACI Guidelines"""
        )

    def _handle_septic_shock(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle septic shock"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**SEPTIC SHOCK - MEDICAL EMERGENCY**

**DEFINITION:**
- **Sepsis:** life-threatening organ dysfunction caused by dysregulated host response to infection
   - **Organ dysfunction:** SOFA score ≥2 (or ≥2 point increase)
   - **Clinical criteria:** qSOFA ≥2 (RR ≥22, altered mentation, SBP ≤100)
- **Septic shock:** sepsis with persistent hypotension requiring vasopressors to maintain MAP ≥65 mmHg and lactate >2 mmol/L despite adequate fluid resuscitation

**IMMEDIATE MANAGEMENT (within 1 hour - "SEPSIS SIX"):**

**1. Oxygen:**
- Target SpO2 94-98% (88-92% if at risk of hypercapnic respiratory failure)

**2. Blood Cultures:**
- **Take BEFORE antibiotics** (2 sets, 2 bottles per set: aerobic + anaerobic)
- **Other sites:** urine, sputum, wound swab, CSF if meningitis suspected

**3. Broad-spectrum Antibiotics:**
- **Within 1 hour** of recognition (do NOT delay for investigations)
- **Empiric choice:** (based on likely source, local resistance patterns)
   - **Ceftriaxone 2 g IV** (or Meropenem 1 g IV if high risk of resistant organisms)
   - **Add:** Vancomycin 15-20 mg/kg IV (if MRSA risk)
   - **Add:** Clindamycin 600 mg IV (if necrotising infection)

**4. IV Fluids:**
- **Crystalloid bolus:** 500 mL over <15 minutes (Hartmann's or 0.9% NaCl)
- **Repeat:** 500 mL boluses (up to 30 mL/kg in first 6 hours)
- **Monitor:** for signs of fluid overload (crackles, rising JVP, pulmonary oedema)
- **Target:** MAP ≥65 mmHg, urine output ≥0.5 mL/kg/hr, ScvO2 ≥70%

**5. Lactate:**
- **Serum lactate** (measure on presentation, repeat after 3-6 hours)
- **Lactate clearance:** (lactate0 - lactate6)/lactate0 × 100%
   - **Target:** >10% clearance at 6 hours (associated with improved mortality)

**6. Urine Output:**
- **Catheterise** (if shock, or to monitor fluid balance)
- **Target:** ≥0.5 mL/kg/hr

**SOURCE CONTROL:**
- **Identify source** of infection (chest, urine, abdomen, skin, lines, CNS)
- **Source control:** drain abscess, remove infected line, debride necrotic tissue
- **Imaging:** CXR, urine dipstick, CT abdomen/pelvis (if intra-abdominal source suspected)

**VASOPRESSORS (if fluid-resistant hypotension):**

**Noradrenaline (Norepinephrine):**
- **First-line vasopressor**
- **Start:** 0.05-0.1 mcg/kg/min
- **Titrate:** to MAP ≥65 mmHg
- **Mechanism:** predominantly α1 effect (vasoconstriction)

**Vasopressin:**
- **Second-line** (if noradrenaline >0.3-0.5 mcg/kg/min)
- **Dose:** 0.03 units/min (fixed dose, not titrated)
- **Mechanism:** V1 receptor stimulation (vasoconstriction)

**Adrenaline (Epinephrine):**
- **Third-line** (if noradrenaline + vasopressin inadequate)
- **Dose:** 0.05-0.5 mcg/kg/min
- **Mechanism:** α1 + β1 + β2 effects (vasoconstriction, inotropy, bronchodilation)

**Dopamine:**
- **Alternative** in selected patients (e.g., bradycardia, low risk of tachyarrhythmias)
- **Dose:** 2-20 mcg/kg/min

**INOTROPES:**

**Dobutamine:**
- **Indicated:** if myocardial dysfunction (low cardiac output, ScvO2 <70% despite adequate MAP)
- **Dose:** 2.5-20 mcg/kg/min
- **Mechanism:** β1 + β2 effects (inotropy, vasodilatation)

**CORTICOSTEROIDS:**
- **Indicated:** if refractory shock (requiring vasopressors >0.25 mcg/kg/min noradrenaline)
- **Hydrocortisone:** 50 mg IV QDS (200 mg daily)
- **Fludrocortisone:** 50 mcg NG/PO daily (if hydrocortisone used)
- **Duration:** 7 days or until ICU discharge (whichever sooner)

**BLOOD PRODUCTS:**
- **Red cell transfusion:** if Hb <70 g/L (or <80 g/L if myocardial ischaemia)
- **Platelet transfusion:** if platelets <10×10⁹/L (or <20×10⁹/L if bleeding)
- **FFP:** if INR >1.5 and bleeding/invasive procedure planned

**GLUCOSE CONTROL:**
- **Target:** 6-10 mmol/L (108-180 mg/dL)
- **Avoid hypoglycaemia** (<4 mmol/L)

**PROPHYLAXIS:**
- **Stress ulcer prophylaxis:** PPI (Omeprazole 40 mg NG/OD) if GI bleed risk
- **VTE prophylaxis:** LMWH (Dalteparin 5000 units SC daily) unless contraindicated

**Sources:** NICE NG51, Surviving Sepsis Campaign 2021"""
        )

    def _handle_acs(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle acute coronary syndrome"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**ACUTE CORONARY SYNDROME (ACS) - MEDICAL EMERGENCY**

**CLASSIFICATION:**
- **STEMI:** ST-elevation MI (≥1 mm in ≥2 contiguous leads) or new LBBB
- **NSTEMI:** Elevated cardiac biomarkers WITHOUT ST elevation
- **Unstable angina:** Symptoms without biomarker elevation

**IMMEDIATE MANAGEMENT (ALL ACS):**

**1. Aspirin:**
- **300 mg chewed** (not swallowed) immediately
- **Loading dose** (antiplatelet effect)

**2. Oxygen:**
- **If SpO2 <94%:** 4-8 L/min via face mask
- **If SpO2 ≥94%:** no oxygen (may worsen infarct size)

**3. Nitroglycerin (Glyceryl Trinitrate - GTN):**
- **500 mcg SL** (spray or tablet)
- **Repeat every 5 minutes** (max 3 doses) if pain persists
- **Contraindications:**
   - RV infarction (can cause severe hypotension)
   - SBP <90 mmHg
   - Phosphodiesterase inhibitor use within 24-48h (sildenafil, tadalafil)
   - Severe aortic stenosis
   - Hypertrophic obstructive cardiomyopathy

**4. Analgesia:**
- **Morphine 2.5-5 mg IV** (slow titration, repeat q5-10min PRN)
- **Anti-emetic:** Metoclopramide 10 mg IV or Ondansetron 4 mg IV
- **Caution:** morphine may delay P2Y12 inhibitor absorption

**5. Dual Antiplatelet Therapy (DAPT):**

**P2Y12 inhibitor (clopidogrel, ticagrelor, prasugrel):**
- **Clopidogrel 300-600 mg loading dose** (all ACS)
- **Ticagrelor 180 mg loading dose** (moderate-high risk NSTEMI, STEMI)
- **Prasugrel 60 mg loading dose** (PCI planned, no prior stroke/TIA)

**STEMI MANAGEMENT:**

**Primary PCI (PPCI) - GOLD STANDARD:**
- **Goal:** door-to-balloon time <90 minutes
- **Indications:** all STEMI (if PPCI available within 120 minutes of first medical contact)

**Fibrinolysis (if PPCI not available within 120 min):**
- **Indication:** STEMI presenting <12 hours
- **Contraindications:** active bleeding, previous haemorrhagic stroke, intracranial neoplasm, ischemic stroke within 3 months, severe uncontrolled HTN
- **Agent:** Tenecteplase (weight-adjusted) or Alteplase

**Anticoagulation (during PPCI/fibrinolysis):**
- **Unfractionated heparin** (UFH): 70 U/kg bolus (max 5000 U)
- **Enoxaparin:** 0.5 mg/kg IV (if fondaparinux not available)

**NSTEMI/Unstable Angina Management:**

**Risk Stratification (GRACE score):**
- **High risk (GRACE >140):** early invasive strategy (coronary angiography within 24 hours)
- **Intermediate risk (GRACE 109-140):** early invasive strategy (within 72 hours)
- **Low risk (GRACE <109):** conservative strategy (ischemia-guided management)

**Anticoagulation:**
- **Enoxaparin 1 mg/kg SC BD** (or 0.75 mg/kg SC BD if CrCl 30-60 mL/min)
- **Or:** Fondaparinux 2.5 mg SC daily (avoid if PCI planned - use UFH instead)

**SECONDARY PREVENTION (DISCHARGE MEDICATIONS):**

**1. Antiplatelets (DAPT):**
- **Aspirin 75 mg daily** indefinitely
- **P2Y12 inhibitor:**
   - **Clopidogrel 75 mg daily** (12 months)
   - **Ticagrelor 90 mg BD** (12 months)
   - **Prasugrel 10 mg daily** (12 months)

**2. Statin:**
- **High-intensity statin:** Atorvastatin 80 mg daily (or Rosuvastatin 40 mg daily)

**3. Beta-blocker:**
- **Start within first few days** (if no contraindications)
- **Bisoprolol 2.5-5 mg daily** or Metoprolol 25-50 mg BD

**4. ACE inhibitor/ARB:**
- **Start if:** LV dysfunction (LVEF <40%), heart failure, diabetes, hypertension
- **Ramipril 2.5-5 mg daily** (or Losartan 50 mg daily)

**5. Aldosterone antagonist:**
- **Eplerenone 25-50 mg daily** (if LVEF <35% + diabetes/heart failure)

**COMPLICATIONS:**

**Ventricular arrhythmias:**
- **VF/VT:** immediate defibrillation, amiodarone 300 mg IV
- **Frequent PVCs:** observe (treatment if symptomatic)

**Bradycardia:**
- **Atropine 500 mcg IV** (repeat up to 3 mg)
- **Transcutaneous pacing** if atropine ineffective

**Cardiogenic shock:**
- **IV fluids** (if no pulmonary oedema)
- **Inotropes:** Dobutamine, Noradrenaline
- **Early revascularisation** (PCI or CABG)

**Sources:** NICE NG95, ESC Guidelines 2020"""
        )

    def _handle_arrhythmia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle arrhythmias"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**ARRHYTHMIAS - CARDIAC EMERGENCIES**

**IMMEDIATE ASSESSMENT:**
- **ABC:** airway, breathing, circulation
- **Observations:** BP, HR, RR, SpO2, temperature
- **12-lead ECG:** confirm rhythm
- **Blood tests:** FBC, U&E, Mg²⁺, troponin
- **Chest X-ray:** (if cardiac failure, chest pain)

**UNSTABLE TACHYARRHYTHMIA:**

**Signs of instability:**
- Shock (SBP <90 mmHg, hypoperfusion)
- Altered mental status (confusion, drowsiness)
- Ischaemic chest pain
- Acute heart failure

**Management (if unstable):**
- **Immediate Synchronised Cardioversion**
   - **AF/Atrial flutter with RVR:** 120-200 J biphasic
   - **Regular narrow-complex tachycardia (SVT):** 100 J initially
   - **Wide-complex tachycardia (VT):** 150-200 J biphasic
   - **Polymorphic VT (including Torsades):** unsynchronised defibrillation (200 J)

**STABLE TACHYARRHYTHMIA:**

**Narrow-complex SVT:**

**1. Vagal manoeuvres:**
- **Valsalva** (most effective): forced expiration against closed glottis (blowing into 10 mL syringe)
- **Carotid sinus massage** (one side at a time, avoid if carotid bruit, TIA, stroke history)

**2. Adenosine (if vagal manoeuvres fail):**
- **6 mg IV rapid bolus** (followed by 20 mL saline flush)
- **If no response:** 12 mg IV (repeat once if needed)
- **Contraindications:** asthma, severe COPD, 2nd/3rd degree heart block, sick sinus syndrome, BP <90 mmHg, severe hypotension
- **Side effects:** transient flushing, dyspnoea, chest discomfort, bradycardia

**3. Verapamil (if adenosine contraindicated/ineffective):**
- **2.5-5 mg IV over 2 minutes**
- **Alternative:** Diltiazem 250 mcg/kg IV

**Atrial Fibrillation with Rapid Ventricular Response (AF RVR):**

**Rate control:**
- **Diltiazem 250 mcg/kg IV** (or 0.25 mg/kg) over 2 minutes
- **Or:** Verapamil 2.5-5 mg IV over 2 minutes
- **Or:** Metoprolol 2.5-5 mg IV over 2 minutes

**Rhythm control:**
- **Amiodarone 150 mg IV over 10 minutes** (if AF <48 hours, or haemodynamically unstable)
- **Elective cardioversion** (if AF >48 hours, anticoagulate for 3 weeks first, or TOE to exclude LA thrombus)

**Atrial Flutter:**
- **Similar management** to AF
- **More responsive** to cardioversion (lower energy)

**Wide-Complex Tachycardia:**

**VT (most common):**
- **If stable:** Amiodarone 150 mg IV over 10 minutes (repeat 300 mg if needed)
- **Alternatively:** Procainamide 10-15 mg/kg IV
- **Cardioversion** (if medical therapy fails)

**SVT with aberrancy:**
- **Treat as SVT** (adenosine)

**BRADYARRHYTHMIAS:**

**Sinus Bradycardia:**
- **Asymptomatic:** observe
- **Symptomatic (dizziness, syncope, hypotension):**
   - **Atropine 500 mcg IV** (repeat up to 3 mg)
   - **Pacing** (transcutaneous or transvenous) if atropine ineffective

**AV Block:**
- **1st degree:** observe
- **2nd degree (Mobitz I - Wenckebach):** observe (often benign)
- **2nd degree (Mobitz II):** pacing indicated
- **3rd degree (complete):** pacing indicated

**Sick Sinus Syndrome:**
- **Pacing indicated** (if symptomatic)

**SPECIFIC ARRHYTHMIAS:**

**Atrial Flutter:**
- **Typical flutter:** sawtooth flutter waves in II, III, aVF
- **Carotid sinus massage** may terminate
- **Radiofrequency ablation** (high success rate)

**AV Nodal Re-entrant Tachycardia (AVNRT):**
- **Common SVT** in young adults with structurally normal heart
- **Adenosine** usually terminates
- **Radiofrequency ablation** (curative)

**WPW (Wolff-Parkinson-White) Syndrome:**
- **Pre-excited AF** (irregular, wide-complex, very fast)
- **AVOID:** AV node blocking agents (adenosine, verapamil, diltiazem, digoxin) - may precipitate VF
- **Treatment:** Procainamide 10-15 mg/kg IV

**Torsades de Pointes:**
- **Polymorphic VT** with prolonged QT interval
- **MgSO4 2 g IV** over 10-15 minutes
- **Correct K+, Mg2+**
- **Temporary pacing** (overdrive pacing)
- **Avoid:** QT-prolonging drugs

**LONG-TERM MANAGEMENT:**

**Anticoagulation (AF):**
- **CHA₂DS₂-VASc score:** (stroke risk)
- **HAS-BLED score:** (bleeding risk)
- **DOACs** (Apixaban, Rivaroxaban, Dabigatran, Edoxaban) preferred over warfarin
- **Indicated:** if CHA₂DS₂-VASc ≥2 (men) or ≥3 (women)

**Rate control (AF):**
- **Beta-blocker** (Bisoprolol, Metoprolol)
- **Diltiazem** (if beta-blocker contraindicated)
- **Digoxin** (sedentary patients, or if beta-blocker/diltiazem insufficient)

**Rhythm control (AF):**
- **Electrical cardioversion** (AF <48 hours, or anticoagulated)
- **Pharmacological cardioversion:** Flecainide, Propafenone (if structurally normal heart), Amiodarone
- **Catheter ablation** (paroxysmal AF)

**Sources:** Resuscitation Council (UK), ESC Guidelines 2020"""
        )

    def _handle_acute_asthma(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle acute severe asthma"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**ACUTE SEVERE ASTHMA - MEDICAL EMERGENCY**

**ASSESSMENT OF SEVERITY:**

**Life-Threatening Asthma (any of following):**
- Peak flow <33% best or predicted
- SpO2 <92%
- PaO2 <8 kPa
- Normal or raised PaCO2 (4.6-6.0 kPa) - indicates fatigue
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
- **If no nebuliser:** 4-10 puffs via spacer (repeat every 10 minutes)

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

    def _handle_pulmonary_embolism(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle pulmonary embolism"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**PULMONARY EMBOLISM (PE) - MEDICAL EMERGENCY**

**ASSESSMENT:**

**Clinical Features:**
- **Dyspnoea** (sudden onset)
- **Pleural chest pain**
- **Haemoptysis**
- **Syncope** (massive PE)
- **Tachycardia** (>100/min)
- **Tachypnoea** (>20/min)
- **Signs of DVT** (leg swelling, tenderness)

**Risk Stratification (Wells Score):**
- **DVT symptoms:** 3 points
- **PE as likely or more likely than Dx:** 3 points
- **Heart rate >100/min:** 1.5 points
- **Immobilisation/surgery in previous 4 weeks:** 1.5 points
- **Previous DVT/PE:** 1.5 points
- **Haemoptysis:** 1 point
- **Malignancy:** 1 point

**Interpretation:**
- **Score >4:** PE likely
- **Score ≤4:** PE unlikely

**INVESTIGATIONS:**

**1. Chest X-ray:**
- **Often normal** (or shows: atelectasis, pleural effusion, elevated hemidiaphragm)
- **Exclude:** other causes (pneumonia, pneumothorax)

**2. ECG:**
- **Often normal** or sinus tachycardia
- **Classic signs (rare):** S1Q3T3 (S wave in lead I, Q wave in lead III, inverted T in lead III), right heart strain (T wave inversion V1-V4)

**3. ABG:**
- **Hypoxia** (PaO2 <10 kPa on room air)
- **Hypocapnia** (PaCO2 <4.6 kPa) due to hyperventilation
- **Normal ABG does NOT exclude PE**

**4. D-dimer:**
- **Sensitive but NOT specific** (elevated in infection, malignancy, pregnancy, post-op, age >50)
- **If D-dimer negative:** PE effectively excluded (if Wells score ≤4)

**5. CTPA (CT Pulmonary Angiography):**
- **Gold standard** for diagnosis
- **Indicated:** if Wells score >4, or positive D-dimer + Wells score ≤4

**6. V/Q Scan:**
- **Alternative** if CTPA contraindicated (renal impairment, contrast allergy, pregnancy)

**7. Echocardiogram:**
- **Right ventricular strain** (in massive PE)
- **Indicated:** if haemodynamically unstable

**RISK STRATIFICATION:**

**High risk (Massive PE):**
- **Shock or hypotension** (SBP <90 mmHg or drop ≥40 mmHg)
- **Requires:** thrombolysis or embolectomy

**Intermediate risk (Sub-massive PE):**
- **Normotensive** with RV dysfunction (echo, CT) or elevated cardiac biomarkers (troponin, BNP)
- **Monitor** for clinical deterioration

**Low risk:**
- **Normotensive**, no RV dysfunction, normal biomarkers
- **Consider outpatient** management (Hestia criteria)

**MANAGEMENT:**

**1. Anticoagulation (IMMEDIATE):**

**Initial:**
- **Low molecular weight heparin (LMWH):**
   - Enoxaparin 1 mg/kg SC BD (or 1.5 mg/kg SC daily)
   - Dalteparin 200 IU/kg SC daily (or 100 IU/kg SC BD)
   - Tinzaparin 175 IU/kg SC daily
- **Or:** Fondaparinux 5-7.5 mg SC daily (if HIT)

**Oral anticoagulation (after 5 days LMWH):**
- **DOACs** (Apixaban, Rivaroxaban, Dabigatran, Edoxaban) - preferred
- **Or:** Vitamin K antagonist (Warfarin, target INR 2-3) - if DOAC contraindicated

**Duration:**
- **Provoked PE:** 3 months
- **Unprovoked PE:** ≥3 months (consider indefinite if high risk of recurrence)

**2. Thrombolysis (Massive PE):**

**Indications:**
- **Massive PE with shock** (SBP <90 mmHg)
- **Cardiac arrest**

**Agents:**
- **Alteplase (tPA):** 10 mg IV bolus → 90 mg IV over 2 hours
- **Tenecteplase:** weight-adjusted IV bolus (30-50 mg depending on weight)

**Contraindications:**
- Active bleeding
- Recent surgery/trauma (<10 days)
- Previous haemorrhagic stroke
- Ischemic stroke within 3 months
- Intracranial neoplasm
- Severe uncontrolled HTN

**3. Surgical Embolectomy:**
- **Indicated:** if thrombolysis contraindicated or failed (massive PE)
- **Surgical:** pulmonary embolectomy (cardiopulmonary bypass)
- **Percutaneous:** catheter-directed thrombectomy

**4. IVC Filter:**
- **Indicated:** if PE recurrence despite adequate anticoagulation
- **Or:** contraindication to anticoagulation (high bleeding risk)
- **Removable filters** preferred

**Sources:** NICE NG144, ESC Guidelines 2019"""
        )

    def _handle_pneumothorax(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle pneumothorax"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**PNEUMOTHORAX - MEDICAL EMERGENCY**

**CLASSIFICATION:**

**Primary spontaneous pneumothorax (PSP):**
- **No underlying lung disease**
- **Typically:** young, tall, thin males (smokers)
- **Recurrence rate:** 30% (ipsilateral), 10% (contralateral)

**Secondary spontaneous pneumothorax (SSP):**
- **Underlying lung disease** (COPD, fibrosis, pneumonia, cancer)
- **Higher mortality** (due to limited respiratory reserve)

**Traumatic pneumothorax:**
- **Blunt or penetrating trauma**
- **Iatrogenic** (central line, lung biopsy, mechanical ventilation)

**Tension pneumothorax:**
- **Life-threatening emergency**
- **One-way valve** → air enters pleural space on inspiration, cannot exit on expiration
- **Progressive** accumulation → mediastinal shift, cardiovascular collapse

**ASSESSMENT:**

**Symptoms:**
- **Sudden onset** pleuritic chest pain
- **Dyspnoea** (severity depends on size, underlying lung disease)

**Signs:**
- **Reduced chest expansion** on affected side
- **Reduced breath sounds** on affected side
- **Hyper-resonant** percussion on affected side
- **Tension pneumothorax:**
   - Tracheal deviation (away from affected side)
   - Distended neck veins
   - Hypotension
   - Tachycardia
   - Cyanosis

**INVESTIGATIONS:**

**Chest X-ray (erect, inspiratory):**
- **Visceral pleural line** (sharp, white line parallel to chest wall)
- **Absence of lung markings** peripheral to visceral pleural line
- **Size estimation:** distance from visceral pleural line to chest wall at hilum
   - **<2 cm:** small
   - **≥2 cm:** large

**CT Chest:**
- **More sensitive** (detects small pneumothoraces)
- **Indicated:** if CXR equivocal, or to assess underlying lung disease

**MANAGEMENT:**

**TENSION PNEUMOTHORAX - IMMEDIATE DECOMPRESSION:**
- **DO NOT wait for CXR**
- **Needle decompression:** 14-16G cannula inserted 2nd intercostal space, midclavicular line
- **Followed by:** chest drain insertion

**PRIMARY SPONTANEOUS PNEUMOTHORAX:**

**Small (<2 cm, minimal symptoms):**
- **Observation** (admit to hospital, monitor)
- **High-flow oxygen** (10-15 L/min) - accelerates resolution (nitrogen washout)
- **Repeat CXR** (after 4-6 hours, then 24 hours)
- **Consider discharge** if resolved, asymptomatic, reliable patient

**Large (≥2 cm, symptomatic):**
- **Aspiration** (first line): 16G cannula inserted 2nd intercostal space, midclavicular line; aspirate until resistance felt or >2.5 L aspirated
- **If aspiration fails:** chest drain insertion

SECONDARY SPONTANEOUS PNEUMOTHORAX:

**ALL cases:**
- **Admit to hospital** (higher mortality due to limited respiratory reserve)
- **Chest drain** (unless very small and minimal symptoms)
- **High-flow oxygen** (if no COPD with CO2 retention)

**CHEST DRAIN INSERTION:**

**Site:** 4th or 5th intercostal space, anterior axillary line (safe triangle)

**Size:**
- **Small (12-16 Fr):** pneumothorax (less painful)
- **Large (20-24 Fr):** haemothorax, trauma, mechanical ventilation

**Technique:**
- **Seldinger technique** (smaller drains)
- **Surgical technique** (larger drains, trauma)

**Connection:**
- **Underwater seal** (or Heimlich valve for ambulatory management)

**Monitoring:**
- **CXR** after insertion (confirm position, re-expansion)
- **Swing** visible in drain
- **Air leak** (bubbling)

**REMOVAL:**
- **Indications:** lung fully expanded, no air leak for 24-48 hours
- **Clamp** (trial of clamping for 24 hours, CXR to confirm no recurrence)
- **Remove** (if lung remains expanded after clamping)

**DEFINITIVE MANAGEMENT (to prevent recurrence):**

**Indications:**
- **Recurrent ipsilateral pneumothorax** (after 2 episodes)
- **First contralateral pneumothorax**
- **Bilateral pneumothoraces**
- **Persistent air leak** (>7 days)
- **High-risk professions** (pilots, divers)

**Options:**
- **Video-assisted thoracoscopic surgery (VATS):**
   - **Bullectomy** (resect apical blebs)
   - **Pleurodesis** (mechanical abrasion or chemical talc pleurodesis)
- **Open thoracotomy** (if VATS not available)
- **Pleural talc slurry** (if not surgical candidate)

**SOURCES OF OXYGEN:**
- **High-flow oxygen:** 10-15 L/min via non-rebreathe mask
- **Mechanism:** nitrogen washout (reduces nitrogen in pleural space, increases reabsorption gradient)
- **Caution:** in COPD with CO2 retention (target SpO2 88-92%)

**Sources:** BTS Pleural Disease Guidelines 2010, NICE NG138"""
        )

    def _handle_stroke(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle stroke"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**STROKE - MEDICAL EMERGENCY (TIME IS BRAIN)**

**RECOGNITION (FAST):**
- **F - Face:** facial droop (ask patient to smile)
- **A - Arms:** arm weakness (ask patient to raise both arms)
- **S - Speech:** speech disturbance (ask patient to speak a sentence)
- **T - Time:** time to call emergency services (999/911)

**IMMEDIATE ACTION:**
- **Urgent admission** to Hyperacute Stroke Unit (HASU)
- **CT brain** within 1 hour of arrival (door-to-scan time)
- **Thrombolysis** if ischaemic stroke and within time window (4.5 hours from symptom onset)
- **Thrombectomy** if large vessel occlusion and within time window (6 hours, up to 24 hours in selected cases)

**INITIAL ASSESSMENT:**

**1. ABC:**
- **Airway:** protect if decreased GCS
- **Breathing:** SpO2 94-98% (94-98% in stroke, 88-92% if COPD)
- **Circulation:** BP (DO NOT lower unless >220/120 mmHg for thrombolysis, or >185/110 mmHg for thrombectomy)

**2. Observations:**
- BP, HR, RR, SpO2, temperature, GCS, BM (glucose)

**3. Blood tests:**
- **FBC, U&E, CRP**
- **Glucose** (exclude hypoglycaemia/hyperglycaemia mimicking stroke)
- **Troponin** (if ACS suspected)
- **Coagulation** (if anticoagulated, or considering thrombolysis)

**4. CT Brain (NON-CONTRAST):**
- **Indicated:** for ALL suspected stroke (exclude haemorrhage)
- **Door-to-scan time:** <25 minutes (ideal)
- **Within 1 hour** of arrival (target)

**5. ECG:**
- **Atrial fibrillation** (if present, may be cardioembolic stroke)

**DIAGNOSIS:**

**Ischaemic Stroke (85%):**
- **CT:** normal initially (or shows early signs: loss of grey-white differentiation, sulcal effacement, hyperdense artery sign)
- **Management:** thrombolysis (if eligible), thrombectomy (if eligible), antiplatelet, statin, anticoagulation (if AF)

**Haemorrhagic Stroke (15%):**
- **CT:** hyperdense intracerebral haemorrhage
- **Management:** reverse anticoagulation, BP control, neurosurgical referral (if deteriorating)

**Stroke Mimics (up to 25%):**
- **Hypoglycaemia** (treat with 50 mL 10% dextrose IV)
- **Migraine** (usually headache, visual aura, gradual onset)
- **Seizure** (Todd's paresis)
- **Bell's palsy** (isolated facial weakness, no other symptoms)
- **Functional neurological disorder** (inconsistent findings)

**ISCHEMIC STROKE MANAGEMENT:**

**Thrombolysis (Alteplase):**
- **Indications:** ischaemic stroke, within 4.5 hours of symptom onset, definite diagnosis
- **Contraindications:** intracranial haemorrhage, recent head trauma/surgery (<3 months), previous intracranial haemorrhage, GI/GU bleed within 21 days, coagulopathy (INR >1.7, platelets <100×10⁹/L), uncontrolled HTN (>185/110 mmHg), blood glucose <2.7 or >22 mmol/L
- **Dose:** 0.9 mg/kg (10% bolus, 90% infusion over 1 hour)
- **Max dose:** 90 mg
- **Post-thrombolysis:** admit to Stroke Unit, repeat CT at 24 hours (or if neurological deterioration)

**Mechanical Thrombectomy:**
- **Indications:** large vessel occlusion (MCA, ICA, basilar artery), within 6 hours of symptom onset (up to 24 hours in selected cases based on perfusion imaging)
- **Contraindications:** large established infarct core (ASPECTS <6), poor functional status (mRS >2)
- **Outcome:** significantly better functional outcome compared to thrombolysis alone

**Antiplatelet:**
- **Aspirin 300 mg** immediately (if not thrombolysed)
- **After thrombolysis:** wait 24 hours (CT confirmed no haemorrhage) → start Aspirin 300 mg
- **Maintenance:** Aspirin 75 mg daily (or Clopidogrel 75 mg daily if aspirin intolerant)
- **DAPT:** Aspirin + Clopidogrel for 90 days (if minor stroke or TIA) - CHANCE trial

**Statin:**
- **High-intensity statin:** Atorvall 80 mg daily (or Rosuvastatin 40 mg daily)
- **Indicated:** all ischaemic strokes (unless contraindicated)

**Anticoagulation:**
- **Indicated:** if atrial fibrillation (after 24 hours, CT confirmed no haemorrhage)
- **DOACs** (Apixaban, Rivaroxaban, Dabigatran, Edoxaban) preferred over warfarin
- **Start:** after 24 hours (if small infarct, no haemorrhagic transformation)
- **Delay:** 7-14 days (if large infarct, high risk of haemorrhagic transformation)

**BP Management:**
- **Permissive hypertension:** (allow BP up to 220/120 mmHg for first 7 days)
- **Rationale:** maintains cerebral perfusion to penumbra (area at risk)
- **Treat:** if BP >220/120 mmHg (for thrombolysis), >185/110 mmHg (for thrombectomy), >185/105 mmHg (if receiving thrombolysis and BP remains high for >24 hours)

**BLOOD GLUCOSE:**
- **Target:** 6-10 mmol/L (108-180 mg/dL)
- **Avoid hypoglycaemia** (<4 mmol/L)

**HAEMORRHAGIC STROKE MANAGEMENT:**

**Reverse Anticoagulation:**
- **Warfarin:** Prothrombin complex concentrate (PCC) 50 IU/kg IV + 5 mg Vitamin K IV (slow)
- **DOACs:**
   - **Dabigatran:** Idarucizumab 5 g IV (2.5 g bolus ×2) or Andexanet alfa
   - **Apixaban/Rivaroxaban/Edoxaban:** Andexanet alfa (if available) or PCC 50 IU/kg IV (off-label)

**BP Control:**
- **Target:** SBP <140 mmHg (to prevent haematoma expansion)
- **Agent:** Labetalol IV (or Nicardipine IV)

**Neurosurgery:**
- **Indications:** deteriorating GCS, hydrocephalus, cerebellar haemorrhage (>3 cm, brainstem compression)
- **Procedure:** evacuation of haematoma, EVD (external ventricular drain) for hydrocephalus

**Sources:** NICE NG128, Royal College of Physicians Stroke Guidelines"""
        )

    def _handle_seizure(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle seizure / status epilepticus"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**SEIZURE / STATUS EPILEPTICUS - MEDICAL EMERGENCY**

**DEFINITIONS:**

**Seizure:**
- **Generalised tonic-clonic:** loss of consciousness, tonic stiffening, clonic jerking
- **Focal:** focal onset (may remain focal or secondarily generalise)

**Status Epilepticus:**
- **Convulsive:** tonic-clonic seizure lasting >30 minutes, or recurrent seizures without recovery in between
- **Time to treatment:** >5 minutes (start treatment)

**IMMEDIATE MANAGEMENT:**

**ABC:**
- **Airway:** recovery position, suction secretions, **DO NOT** insert bite block/force airway
- **Breathing:** SpO2 94-98%, **administer oxygen** if hypoxic
- **Circulation:** BP, HR, monitor cardiac rhythm

**Initial Benzodiazepine:**

**Lorazepam (FIRST LINE):**
- **0.1 mg/kg IV** (max 4 mg)
- **Onset:** 1-2 minutes
- **Duration:** 6-12 hours (longer than diazepam)
- **Repeat once** after 10 minutes if seizure continues

**Or Diazepam (if IV access unavailable):**
- **0.2-0.3 mg/kg PR** (rectal diazepam) - max 10 mg
- **Or:** 10-20 mg PR
- **Onset:** 2-5 minutes (PR)
- **Duration:** 2-4 hours

**Or Buccal Midazolam (if IV/PR unavailable):**
- **0.2-0.3 mg/kg buccal** (max 10 mg)
- **Onset:** 5-10 minutes

**Second-line (if seizure continues after 2 doses benzodiazepine):**

**Levetiracetam:**
- **20-60 mg/kg IV** (max 3000 mg) over 5 minutes
- **Or:** 1000-1500 mg IV over 5 minutes
- **Adverse:** drowsiness, behavioural changes

**Or Phenytoin:**
- **15-20 mg/kg IV** (max 1 g) at 50 mg/min
- **Adverse:** hypotension, arrhythmias, purple glove syndrome (extravasation)
- **Contraindications:** heart block, severe bradycardia

**Or Fosphenytoin:**
- **15-20 mg/kg IV** (phenytoin equivalents) at 150 mg/min
- **Adverse:** fewer than phenytoin (safer)

**Or Valproate:**
- **20-40 mg/kg IV** (max 3000 mg) over 5 minutes
- **Contraindications:** pregnancy (teratogenic), liver disease, pancreatitis

**Third-line (if seizure continues):**

**Propofol infusion:**
- **2-4 mg/kg/hr** (titrate to EEG burst suppression)
- **Requires ITU admission**, mechanical ventilation, invasive monitoring

**Or Midazolam infusion:**
- **0.05-0.2 mg/kg/hr** (titrate to EEG burst suppression)
- **Requires ITU admission**, mechanical ventilation

**Or Thiopental infusion:**
- **2-4 mg/kg bolus** → 2-5 mg/kg/hr (titrate to EEG burst suppression)
- **Requires ITU admission**, mechanical ventilation

**INVESTIGATIONS:**

**Bedside:**
- **BM (glucose)** - exclude hypoglycaemia (treat with 50 mL 10% dextrose IV)
- **Observations** (BP, HR, RR, SpO2, temperature)

**Blood tests:**
- **FBC, U&E** (renal failure, hyponatraemia)
- **Ca²⁺, Mg²⁺** (hypocalcaemia, hypomagnesaemia)
- **Toxicology screen** (drug overdose, alcohol withdrawal)
- **Anti-epileptic drug levels** (if known epilepsy)

**Imaging:**
- **CT brain** (if first seizure, focal seizure, post-ictal paralysis, head injury, anticoagulation, malignancy, immunosuppression, fever, persistent headache)
- **MRI brain** (if CT normal and first seizure, or for epilepsy surgery planning)

**EEG:**
- **Indicated:** if status epilepticus, or diagnostic uncertainty (seizure vs. pseudoseizure)

**POST-ICTAL MANAGEMENT:**

**Recovery Position:**
- **Place** in recovery position (until fully recovered)
- **Monitor** airway, breathing, circulation

**Observation:**
- **Close monitoring** until fully recovered (GCS returns to baseline)
- **Check:** BM, observations, neurological examination

**Discharge Considerations:**
- **First unprovoked seizure:** do NOT start anti-epileptic drug
- **Provoked seizure:** treat underlying cause (e.g., stop alcohol, correct electrolyte abnormality)
- **Recurrent seizures:** start anti-epileptic drug (if second unprovoked seizure)

**REFERRAL:**
- **Epilepsy specialist** (if first seizure, or recurrent seizures)
- **Neurosurgery** (if structural lesion on imaging)

**DRIVING:**
- **Group 1 entitlement (cars/motorcycles):** 6 months off driving
- **Group 2 entitlement (lorries/buses):** 5 years off driving

**Sources:** NICE NG217, ILAE Status Epilepticus Guidelines"""
        )

    def _handle_meningitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle meningitis"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**MENINGITIS - MEDICAL EMERGENCY**

**DEFINITION:**
- **Inflammation** of leptomeninges (arachnoid and pia mater)
- **Causes:** bacterial, viral, fungal, TB, chemical

**BACTERIAL MENINGITIS - EMERGENCY:**

**Typical Organisms (by age):**
- **<3 months:** Group B Strep, E. coli, Listeria
- **3 months - 5 years:** Neisseria meningitidis, Streptococcus pneumoniae, Haemophilus influenzae type b
- **5-50 years:** N. meningitidis, S. pneumoniae
- **>50 years:** S. pneumoniae, Listeria, Gram-negative bacilli

**CLASSIC SYMPTOMS:**
- **Headache** (severe)
- **Fever** (high)
- **Neck stiffness** (nuchal rigidity)
- **Photophobia** (light sensitivity)
- **Altered mental status** (confusion, drowsiness)

**SIGNS:**
- **Kernig's sign:** resistance to extension of knee when hip flexed (supine)
- **Brudzinski's sign:** passive neck flexion → involuntary hip and knee flexion
- **Petechial rash** (meningococcal septicaemia)

**IMMEDIATE MANAGEMENT:**

**1. ABC:**
- **Airway:** protect airway if decreased GCS (<8)
- **Breathing:** SpO2 94-98%, oxygen if hypoxic
- **Circulation:** IV access, fluid resuscitation if shock

**2. EMPIRICAL ANTIBIOTICS (DO NOT DELAY FOR LUMBAR PUNCTURE):**

**Adults (<50 years, no immunocompromise):**
- **Ceftriaxone 2 g IV** every 12 hours
- **Add:** Vancomycin 15-20 mg/kg IV every 12 hours (if penicillin-resistant pneumococcus suspected)

**Adults (>50 years, or immunocompromised):**
- **Ceftriaxone 2 g IV** every 12 hours
- **Add:** Vancomycin 15-20 mg/kg IV every 12 hours
- **Add:** Ampicillin 2 g IV every 4 hours (Listeria coverage)

**Children:**
- **Ceftriaxone 80 mg/kg/day IV** (in 2 divided doses)
- **Add:** Vancomycin 15 mg/kg IV every 6 hours (if penicillin-resistant pneumococcus suspected)

**3. Dexamethasone:**
- **Indicated:** if pneumococcal meningitis suspected (adults, children)
- **Dose:** 0.15 mg/kg IV every 6 hours (or 10 mg IV every 6 hours adults)
- **Timing:** BEFORE or WITH first dose of antibiotics (reduces mortality, hearing loss)
- **Duration:** 2-4 days (stop if meningococcal meningitis confirmed)

**4. Fluid Resuscitation (if shock):**
- **Crystalloid bolus** (Hartmann's or 0.9% NaCl) 500 mL over <15 minutes
- **Repeat** if shock persists
- **Consider:** inotropes (noradrenaline) if fluid-resistant shock

**5. Isolation:**
- **Isolate patient** (until 24 hours of antibiotics completed)
- **Inform infection control**

**INVESTIGATIONS:**

**Blood Tests:**
- **FBC, U&E, CRP**
- **Blood cultures** (×2 sets) - BEFORE antibiotics
- **Coagulation** (if petechial rash, DIC suspected)
- **Serum glucose** (for CSF glucose comparison)

**Lumbar Puncture:**

**Indications:**
- **Suspected meningitis** (if no contraindications)
- **Timing:** after CT brain (if contraindications), or immediately (if no contraindications)

**Contraindications (perform CT first):**
- **Reduced GCS** (<13)
- **Focal neurological deficit**
- **Papilloedema**
- **Immunocompromise**
- **Seizures**

**CSF Analysis:**
- **Appearance:** clear (viral/TB), cloudy (bacterial), xanthochromic (SAH)
- **White cells:** normal (<5), viral (lymphocytes), bacterial (neutrophils)
- **Protein:** elevated (bacterial > viral > normal)
- **Glucose:** normal (50-70% blood glucose), low (bacterial <40% blood glucose)
- **Gram stain:** may reveal organisms (bacterial)
- **Culture:** definitive diagnosis

**CT Brain:**
- **Indicated:** before lumbar puncture if contraindications (see above)
- **Findings:** may be normal (early), cerebral oedema, hydrocephalus

**MENINGOCOCCAL SEPTICAEMIA:**

**Petechial/Purpuric Rash:**
- **Non-blanching** rash (glass test fails)
- **Progresses** rapidly to purpura, ecchymoses
- **Signs of shock:** tachycardia, hypotension, poor perfusion

**Management:**
- **Urgent antibiotics** (Ceftriaxone 2 g IV)
- **Fluid resuscitation** (aggressive)
- **Inotropes** (noradrenaline) if fluid-resistant shock
- **Intensive care** (ITU admission)

**PUBLIC HEALTH:**
- **Notify:** public health authorities (meningococcal meningitis is notifiable)
- **Prophylaxis:** Rifampicin 600 mg BD for 2 days (for close contacts)
- **Vaccination:** meningococcal ACWY vaccine (for close contacts)

**VIRAL MENINGITIS:**

**Typical Viruses:**
- **Enteroviruses** (Coxsackie, Echovirus) - most common
- **Herpes Simplex Virus (HSV)**
- **Varicella Zoster Virus (VZV)**
- **Mumps, HIV, EBV, CMV**

**Management:**
- **Supportive care** (analgesia, hydration)
- **Acyclovir 10 mg/kg IV every 8 hours** (if HSV suspected)
- **DO NOT give antibiotics** (if confident viral aetiology)

**PROGNOSIS:**
- **Bacterial meningitis:** mortality 10-20% (higher in elderly, pneumococcal)
- **Meningococcal septicaemia:** mortality up to 50% (with shock)
- **Viral meningitis:** full recovery (usually)

**Sources:** NICE NG102, Meningitis Research Foundation"""
        )

    def _handle_head_injury(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle head injury"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**HEAD INJURY - MEDICAL EMERGENCY**

**ASSESSMENT:**

**Mechanism:**
- **High-risk mechanisms:** fall from >1 metre, assault, road traffic accident, pedestrian struck by vehicle
- **Low-risk mechanisms:** ground-level fall, walking into object

**Symptoms:**
- **Headache**
- **Vomiting** (>1 episode)
- **Altered mental status** (confusion, drowsiness)
- **Seizure**
- **Amnesia** (retrograde, anterograde)
- **Focal neurological deficit**

**Signs:**
- **GCS** (Glasgow Coma Scale) - eye opening, verbal response, motor response
- **Pupils** (size, equality, reactivity)
- **Focal deficit** (limb weakness, visual field defect)
- **Battle's sign** (bruising over mastoid - basal skull fracture)
- **Raccoon eyes** (periorbital bruising - basal skull fracture)
- **CSF otorrhoea/rhinorrhoea** (basal skull fracture)
- **Haemotympanum** (blood behind tympanic membrane - basal skull fracture)

**RISK STRATIFICATION (NICE CG176):**

**RED FLAGS (requires immediate CT brain):**
- **GCS <13** at any time
- **GCS <15** at 2 hours post-injury
- **Suspected open/depressed skull fracture**
- **Basal skull fracture** signs
- **Focal neurological deficit**
- **Seizure** (post-traumatic)
- **>1 episode vomiting** (adults) or >2 episodes (children)
- **Amnesia >30 minutes** of events before injury
- **Coagulopathy** (warfarin, bleeding disorder)
- **High-risk mechanism** (pedestrian vs. vehicle, fall from >3 metres, ejection from vehicle)

**ORANGE FLAGS (requires CT brain within 8 hours):**
- **Amnesia 30 minutes - 24 hours** of events before injury
- **Dangerous mechanism** (fall from 1-3 metres, assault with weapon, ejection from vehicle)

**IMMEDIATE MANAGEMENT:**

**ABC:**
- **Airway:** cervical spine immobilisation (if trauma, or GCS <8)
- **Breathing:** SpO2 94-98%
- **Circulation:** BP, HR, establish IV access

**Cervical Spine:**
- **Immobilise** (hard collar, sandbags, tape) until cervical spine cleared
- **Indicated:** if trauma, or GCS <15 (unable to assess neck pain/tenderness)

**CT Brain:**
- **Indicated:** if red flags or orange flags (see above)
- **Timing:** immediately (red flags) or within 8 hours (orange flags)

**Head Injury Instructions:**
- **Discharge with head injury instructions** if CT normal, no red flags, and accompanied by responsible adult

**MANAGEMENT OF SPECIFIC INJURIES:**

**Concussion (Mild Head Injury):**
- **Definition:** GCS 14-15 at 2 hours, no red flags, normal CT
- **Management:** discharge with head injury instructions
- **Advice:** avoid strenuous activity, sports, alcohol for 2 weeks, return driving when symptom-free

**Intracranial Haemorrhage:**
- **Extradural haematoma:** lens-shaped haemorrhage, arterial (middle meningeal artery), lucid interval then rapid deterioration → **NEUROSURGICAL EMERGENCY**
- **Subdural haematoma:** crescent-shaped haemorrhage, venous (bridging veins), may be acute, subacute, chronic → **NEUROSURGICAL EMERGENCY** (if mass effect)
- **Intracerebral haemorrhage:** parenchymal bleed (hypertension, trauma)
- **Subarachnoid haemorrhage:** blood in subarachnoid space (aneurysm, trauma)

**Skull Fracture:**
- **Linear:** managed conservatively (observe)
- **Depressed:** require neurosurgical elevation (if depressed > skull thickness)
- **Basal:** (see above) - admit for observation

**DIFFUSE AXONAL INJURY:**
- **Severe traumatic brain injury** (shearing injury)
- **CT:** may be normal initially
- **MRI:** more sensitive (shows petechial haemorrhages)
- **Management:** neurocritical care, ICP monitoring

**NEUROSURGICAL REFERRAL:**

**Indications:**
- **Extradural/subdural haematoma** with mass effect
- **Depressed skull fracture** (depressed > skull thickness)
- **Intracranial haemorrhage** with deterioration
- **Raised ICP** refractory to medical management
- **Penetrating head injury**

**RAISED INTRACRANIAL PRESSURE (ICP):**

**Signs:**
- **Cushing's triad:** hypertension, bradycardia, irregular respirations
- **Pupillary dilatation** (unilateral or bilateral)
- **Decreasing GCS**

**Management:**
- **20% Mannitol 1 g/kg IV** over 20 minutes (or 0.25-1 g/kg)
- **Elevate head of bed** 30°
- **Hyperventilation** (target PaCO2 4.5-5 kPa) - temporary
- **Sedation** (propofol, midazolam)
- **Paralysis** (neuromuscular blockade)
- **Decompressive craniectomy** (if refractory)

**DISCHARGE CRITERIA:**

**All of following:**
- **GCS 15** (back to baseline)
- **Normal CT brain** (or CT normal for age)
- **No red flags** (see above)
- **Responsible adult** to accompany for 24 hours
- **Head injury instructions** provided

**Head Injury Instructions:**
- **NO alcohol** for 24 hours
- **NO driving** until medically cleared
- **Responsible adult** to stay with patient for 24 hours
- **Return to ED** if: vomiting, drowsiness, confusion, headache worsens, seizure, focal neurological deficit

**Sources:** NICE CG176, SIGN 110"""
        )

    def _handle_burns(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle burns"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**BURNS - MEDICAL EMERGENCY**

**ASSESSMENT:**

**Mechanism:**
- **Thermal:** flame, scald, contact, tar
- **Electrical:** high-voltage (>1000 V), low-voltage (<1000 V), lightning
- **Chemical:** acid, alkali, organic compounds
- **Radiation:** sunburn, ionising radiation

**Depth:**
- **Superficial (epidermal):** erythema, pain, no blisters (sunburn)
- **Superficial partial-thickness (superficial dermal):** erythema, blisters, painful, blanches with pressure
- **Deep partial-thickness (deep dermal):** white/red, mottled, less painful, does not blanch
- **Full-thickness (third-degree):** white/brown/charred, painless (nerve endings destroyed), leathery, waxy

**Extent (TBSA - Total Body Surface Area):**

**Rule of Nines (adults):**
- **Head/neck:** 9%
- **Each upper limb:** 9%
- **Anterior trunk:** 18%
- **Posterior trunk:** 18%
- **Each lower limb:** 18%
- **Perineum:** 1%

**Rule of Palm:**
- **Patient's palm (including fingers):** 1% TBSA

**Lund-Browder Chart (children):**
- **Head/neck:** 18% (infant), 13% (child), 9% (adult)
- **Each lower limb:** 14% (infant), 16% (child), 18% (adult)

**IMMEDIATE MANAGEMENT:**

**ABC:**
- **Airway:** **secure early** (if facial/oropharyngeal burns, soot in sputum, stridor, hoarseness, respiratory distress)
- **Breathing:** SpO2 94-98%, 100% oxygen if carbon monoxide poisoning suspected
- **Circulation:** IV access (through unburnt skin if possible), fluid resuscitation

**STOP BURNING PROCESS:**
- **Thermal:** remove from heat source, cool with running water (20°C) for 20 minutes
- **Electrical:** disconnect power source (DO NOT touch patient until disconnected)
- **Chemical:** brush off dry powder, irrigate with copious water (≥30 minutes)

**REMOVE:** jewellery, clothing, constricting items (from injured area)

**COOLING:**
- **Running water (20°C)** for 20 minutes (if thermal burn)
- **Avoid:** ice, ice water (causes vasoconstriction, further injury)
- **After cooling:** cover with cling film, clean sheet, or non-adherent dressing

**FLUID RESCITATION:**

**Parkland Formula (for burns >15% TBSA in adults, >10% TBSA in children):**
- **Crystalloid (Hartmann's or 0.9% NaCl):** 4 mL × weight (kg) × %TBSA
- **Half:** given in first 8 hours
- **Half:** given in next 16 hours
- **Start:** from time of burn (not time of arrival)

**Children:**
- **Maintenance fluid:** (100 mL/kg for 1st 10 kg, 50 mL/kg for 2nd 10 kg, 20 mL/kg for remaining kg) per 24 hours
- **Add:** Parkland resuscitation fluid

**ENDPOINTS:**
- **Urine output:** 0.5-1 mL/kg/hr (adults), 1-1.5 mL/kg/hr (children)
- **MAP:** >65 mmHg
- **Capillary refill:** <2 seconds

**ESCHAROTOMY:**
- **Indications:** full-thickness circumferential burns (limbs, trunk), respiratory distress (chest burns)
- **Procedure:** incise eschar (through full-thickness burn) along medial/lateral aspects of limb, or lateral chest wall
- **Goal:** relieve pressure, allow expansion, restore perfusion/ventilation

**PAIN MANAGEMENT:**
- **IV opioids:** Morphine 0.1 mg/kg (or 5-10 mg) IV/SC titrated
- **Anti-anxiety:** consider benzodiazepine (Lorazepam 1-2 mg PO/SL) if anxious

**TETANUS PROPHYLAXIS:**
- **Tetanus toxoid:** if not fully vaccinated (3 doses) or last dose >10 years ago
- **Tetanus immunoglobulin:** if tetanus-prone wound (contaminated, devitalised tissue) and not fully vaccinated

**ANTIBIOTICS:**
- **NOT indicated** routinely (prophylactic antibiotics increase resistance, do not prevent infection)
- **Indicated:** if clinical infection (cellulitis, sepsis)

**REFERRAL CRITERIA (to Burns Centre):**

**Specialised burns centre required for:**
- **All burns >5% TBSA** in adults, >2% TBSA in children
- **Full-thickness burns >5% TBSA** (any age)
- **Burns involving:** face, hands, feet, genitalia, perineum, major joints
- **Electrical burns** (including lightning)
- **Chemical burns** (if deep, >5% TBSA)
- **Inhalation injury** (suspected)
- **Significant co-morbidities** (diabetes, immunosuppression)
- **Pregnancy**
- **Children** (all significant burns)

**INHALATION INJURY:**

**Suspect if:**
- **Closed space fire**
- **Soot in sputum**, burnt nasal hairs
- **Stridor, hoarseness**, respiratory distress
- **Facial burns**
- **Altered mental status** (CO poisoning)

**Management:**
- **100% oxygen** (if CO poisoning)
- **Intubation** (early, before airway oedema progresses)
- **Bronchoscopy** (diagnostic, therapeutic)

**ELECTRICAL BURNS:**

**Special considerations:**
- **High-voltage (>1000 V):** deep tissue injury, myoglobinuria, arrhythmias, fractures (from tetany)
- **Low-voltage (<1000 V):** usually oral burns (in children - chewing extension cord)
- **Lightning:** cardiorespiratory arrest, neurologic injury, tympanic membrane rupture

**Management:**
- **Cardiac monitoring** (if high-voltage or loss of consciousness)
- **ECG** (look for arrhythmias)
- **CK, urine myoglobin** (rhabdomyolysis)
- **Fluid resuscitation** (Aggressive - to prevent myoglobin-induced renal failure)
- **Fasciotomy** (if compartment syndrome)

**CHEMICAL BURNS:**

**Management:**
- **Remove chemical** (brush off dry powder, cut off contaminated clothing)
- **Irrigate** with copious water (≥30 minutes, ≥2 litres) - do not neutralise acid with alkali (generates heat)
- **Specific antidotes:**
   - **Hydrofluoric acid:** Calcium gluconate gel (topical) or injection (local, intra-arterial)
   - **Cement (alkali burns):** Irrigate, then apply acetic acid (vinegar) to neutralise
   - **Phenol:** Irrigate with water (NOT effective - use polyethylene glycol)
   - **White phosphorus:** Irrigate, then cover with saline-soaked gauze (prevents contact with air, ignition)

**Sources:** NICE CG174, British Burns Association"""
        )

    def _handle_overdose(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle overdose / poisoning"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**OVERDOSE / POISONING - MEDICAL EMERGENCY**

**IMMEDIATE MANAGEMENT:**

**ABC:**
- **Airway:** protect airway (decreased GCS), consider intubation (GCS <8)
- **Breathing:** SpO2 94-98%, respiratory support
- **Circulation:** IV access, BP, ECG, observe arrhythmias

**DECONTAMINATION:**

**1. Activated Charcoal:**
- **Dose:** 1 g/kg (max 50 g) PO/NG
- **Timing:** within 1 hour of ingestion (most effective)
- **Indications:**
   - **Life-threatening overdose** (within 1 hour)
   - **Drugs:** aspirin, tricyclic antidepressants, theophylline, phenobarbital, quinine
- **Contraindications:**
   - **Decreased GCS** (aspiration risk)
   - **Corrosives** (acid, alkali)
   - **Hydrocarbons** (aspiration pneumonitis)
   - **Irritants** (heavy metals)

**2. Gastric Lavage:**
- **Rarely indicated**
- **Consider:** if life-threatening overdose, within 1 hour of ingestion, charcoal contraindicated or ineffective
- **Contraindications:** corrosives, hydrocarbons, decreased GCS (intubate first)

**3. Whole Bowel Irrigation:**
- **Indicated:** ingestion of:
   - **Sustained-release/enteric-coated preparations** (iron, lithium, sustained-release theophylline)
   - **Packets** of drugs (body packers, stuffers)
- **Contraindicated:** bowel obstruction, ileus, perforation, haemodynamic instability

**SPECIFIC POISONS:**

**PARACETAMOL (ACETAMINOPHEN):**

**Toxicity:**
- **Single acute ingestion:** >150 mg/kg (or >12 g in adults)
- **Chronic ingestion:** >6 g/day for >2 days

**Management:**
- **N-acetylcysteine (NAC) IV** (if level above treatment line)
- **Treatment line:** (based on serum paracetamol level, time since ingestion)
   - **Low risk:** 150 mg/L at 4 hours, 50 mg/L at 12 hours, 20 mg/L at 24 hours
   - **High risk** (alcoholics, enzyme-inducing drugs, malnourished): 75 mg/L at 4 hours, 30 mg/L at 12 hours, 10 mg/L at 24 hours
- **NAC regimen:**
   - **150 mg/kg in 200 mL over 1 hour**
   - **50 mg/kg in 500 mL over 4 hours**
   - **100 mg/kg in 1 L over 16 hours**
- **Monitor:** INR, LFTs, renal function, ABG (metabolic acidosis), glucose

**OPIOIDS:**

**Toxicity:**
- **Triad:** coma, respiratory depression, miosis
- **Other:** hypotension, bradycardia, hypothermia, rhabdomyolysis (prolonged coma)

**Management:**
- **Naloxone 0.04-0.4 mg IV/IM/SC** (titrate to respiratory rate >10/min)
- **Repeat PRN** (duration 30-90 minutes - naloxone shorter than most opioids)
- **Consider naloxone infusion** (if recurrent respiratory depression)
- **Supportive care:** airway, breathing, circulation

**TRICYCLIC ANTIDEPRESSANTS (TCA):**

**Toxicity:**
- **"3 Cs":** Coma, Convulsions, Cardiotoxicity
- **Cardiac:** QRS prolongation (>100 ms), VT/VF, hypotension (Na+ channel blockade)

**Management:**
- **Activated charcoal** (1 g/kg within 1 hour)
- **Sodium bicarbonate 1-2 mEq/kg IV** (if QRS >100 ms, or arrhythmias)
- **Repeat** sodium bicarbonate (target pH 7.50-7.55)
- **Avoid:** Class Ia antiarrhythmics (quinidine, procainamide, disopyramide) - worsen Na+ channel blockade

**SALICYLATE (ASPIRIN):**

**Toxicity:**
- **Early:** nausea, vomiting, tinnitus, hyperventilation (respiratory alkalosis)
- **Late:** metabolic acidosis, cerebral oedema, pulmonary oedema, coagulopathy

**Management:**
- **Activated charcoal** (1 g/kg within 1 hour)
- **Serial salicylate levels** (q2-4h until decreasing)
- **Urinary alkalinisation:** (NaHCO₃ infusion) - promotes salicylate excretion
   - **Dextrose 5% + NaHCO₃ 150 mmol/L** at 1-2 mL/kg/hr
   - **Target:** urine pH 7.5-8.0, serum pH 7.45-7.55
- **Haemodialysis:** (if level >700 mg/L, or refractory acidosis, pulmonary oedema, cerebral oedema, renal failure)

**BENZODIAZEPINES:**

**Toxicity:**
- **CNS depression** (drowsiness, coma, respiratory depression)
- **Hypotension** (rare)

**Management:**
- **Supportive care** (airway, breathing, circulation)
- **Flumazenil 0.2 mg IV** (titrate to awakening, max 3 mg)
- **Contraindications:** co-ingestion of pro-convulsant (TCA, bupropion) - precipitates seizures
- **Caution:** benzodiazepine-dependent (precipitates withdrawal)

**INSULIN:**

**Toxicity:**
- **Hypoglycaemia** (confusion, sweating, tachycardia, seizures, coma)

**Management:**
- **BM** (capillary blood glucose)
- **If hypoglycaemic (<4 mmol/L):** 50 mL 10% dextrose IV (adults) or 2 mL/kg 10% dextrose IV (children)
- **If persistent hypoglycaemia:** octreotide 50 mcg SC (inhibits insulin secretion)
- **Monitor:** BM every 1 hour until stable

**SULPHONYLUREAS:**

**Toxicity:**
- **Hypoglycaemia** (can be profound, prolonged)

**Management:**
- **50 mL 10% dextrose IV** (if hypoglycaemic)
- **Octreotide 50 mcg SC** TDS (prevents recurrent hypoglycaemia)
- **Monitor:** BM for 24 hours (hypoglycaemia can recur)

**IRON:**

**Toxicity:**
- **5 stages:**
   1. **Gastrointestinal:** nausea, vomiting, diarrhoea, haematemesis (0-6 hours)
   2. **Quiescent:** apparent recovery (6-24 hours)
   3. **Shock/metabolic acidosis:** (12-24 hours)
   4. **Hepatotoxicity:** (2-4 days)
   5. **Gastric scarring/stricture:** (weeks-months)

**Management:**
- **Activated charcoal** (ineffective - iron does not bind charcoal)
- **Whole bowel irrigation** (if significant ingestion)
- **Deferoxamine IV** (if symptomatic, or level >500 mcg/L)
   - **15 mg/kg/hr** (continuous infusion)
   - **Maximum:** 6 g/day
- **Monitor:** iron levels, LFTs, renal function, ABG (metabolic acidosis), CXR (radiopaque tablets)

**ETHANOL/ALCOHOL:**

**Toxicity:**
- **CNS depression**, respiratory depression, hypoglycaemia (especially children)

**Management:**
- **Supportive care** (airway, breathing, circulation)
- **Thiamine 100 mg IV** (prevent Wernicke's encephalopathy)
- **10% dextrose IV** (if hypoglycaemic)
- **Monitor:** BM, blood ethanol level

**GLYPHOSATE (ROUNDUP):**

**Toxicity:**
- **Gastrointestinal:** nausea, vomiting, diarrhoea, abdominal pain
- **Cardiovascular:** hypotension, arrhythmias, pulmonary oedema (surfactant in formulation)

**Management:**
- **Supportive care** (airway, breathing, circulation)
- **IV fluids** (aggressive resuscitation if hypotension)
- **Monitor:** CXR (pulmonary oedema), ABG, ECG

**GENERAL MEASURES:**

**History:**
- **What?** (drug, dose, formulation)
- **When?** (time of ingestion)
- **How much?** (amount, number of tablets)
- **Why?** (accidental, intentional, suicidal)
- **Other?** (co-ingestants, alcohol)

**Examination:**
- **Observations** (BP, HR, RR, SpO2, temperature)
- **GCS** (level of consciousness)
- **Pupils** (size, reactivity - miosis/opioids, mydriasis/amphetamines)
- **Skin** (dry/atropine, sweating/organophosphates, needle marks)
- **Abdomen** (bowel sounds, tenderness)

**Investigations:**
- **Paracetamol level** (4 hours post-ingestion)
- **Salicylate level** (4 hours post-ingestion)
- **ECG** (arrhythmias, QRS prolongation/TCA, QT prolongation)
- **ABG** (respiratory acidosis/opioids, metabolic acidosis/salicylate, metformin)
- **FBC, U&E, LFTs, INR** (baseline)
- **Blood glucose** (exclude hypoglycaemia)
- **Serum toxicology screen** (if unknown ingestion)

**DISPOSITION:**
- **Admit** (if intentional overdose, significant ingestion, abnormal investigations, abnormal observations)
- **Discharge** (if minor accidental ingestion, asymptomatic, normal investigations, reliable supervision)

**PSYCHIATRIC REVIEW:**
- **All intentional overdoses** (suicide risk assessment)

**POISONS INFORMATION SERVICE:**
- **UK:** 0344 892 0111 (NPIS - National Poisons Information Service)

**Sources:** TOXBASE, NICE NG205"""
        )

    def _handle_general_emergency(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general emergency medicine query"""
        return DomainQueryResult(
            domain_name="emergency_medicine",
            answer="""**EMERGENCY MEDICINE - General Consultation**

Emergency medicine covers immediate diagnosis and treatment of acute illness and injury.

**TRIAGE CATEGORIES:**

**Immediate (Red):**
- Life-threatening conditions requiring immediate intervention
- Examples: cardiac arrest, anaphylaxis, shock, severe respiratory distress

**Very Urgent (Orange):**
- Serious conditions requiring urgent assessment and intervention
- Examples: chest pain, stroke, severe trauma, severe asthma

**Urgent (Yellow):**
- Serious conditions requiring timely assessment
- Examples: moderate pain, dehydration, moderate trauma

**Standard (Green):**
- Minor conditions requiring routine assessment
- Examples: minor injuries, minor illness

**Non-urgent (Blue):**
- Minor conditions suitable for primary care
- Examples: sore throat, minor rash

**COMMON EMERGENCIES:**

**Cardiac:**
- Cardiac arrest, acute coronary syndrome, arrhythmias, heart failure

**Respiratory:**
- Acute asthma, COPD exacerbation, pulmonary embolism, pneumonia, pneumothorax, respiratory arrest

**Neurological:**
- Stroke, TIA, seizure, meningitis, encephalitis, head injury

**Trauma:**
- Head injury, fractures, dislocations, burns, wounds, soft tissue injury

**Surgical:**
- Appendicitis, cholecystitis, bowel obstruction, perforated viscus

**Toxicological:**
- Overdose, poisoning, drug withdrawal

**Paediatric:**
- Febrile convulsion, bronchiolitis, croup, dehydration, sepsis

**CRITICAL CARE:**
- **Airway management:** intubation, cricothyroidotomy
- **Breathing support:** mechanical ventilation, NIV
- **Circulatory support:** inotropes, vasopressors
- **Neurological support:** ICP monitoring, seizure control

**REFERRAL CRITERIA:**

**Admission:**
- **Unstable** (requiring monitoring, intervention)
- **Social reasons** (unable to cope at home)
- **Investigations** (requiring hospital facilities)
- **Treatment** (requiring IV therapy, oxygen, observation)

**Discharge:**
- **Stable** (normal observations, improving)
- **Reliable carer** (if needed)
- **Able to self-care** (or carer available)
- **Follow-up arranged** (GP, clinic)

**Sources:** Royal College of Emergency Medicine, NICE Guidelines"""
        )


def create_emergency_medicine_domain():
    """Factory function to create emergency medicine domain"""
    return EmergencyMedicineDomain()
