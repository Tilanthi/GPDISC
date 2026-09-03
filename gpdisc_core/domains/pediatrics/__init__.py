"""
Pediatrics Domain for GPDISC

Comprehensive pediatrics covering:
- Pediatric red flags and emergencies
- Fever in children
- Respiratory presentations (wheeze, stridor, cough)
- Gastrointestinal presentations (vomiting, diarrhea, abdominal pain)
- Neurological presentations (seizures, headache)
- Infectious diseases (rash, meningitis, sepsis)
- Neonatal concerns (jaundice, feeding)
- Developmental surveillance
- Growth and nutrition
- Common pediatric conditions
- Injury prevention
- Behavioral concerns

Evidence-based guidelines: NICE, RCPCH, AAP, BTS
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Optional, Dict, List, Any
import re


class PediatricsDomain(BaseDomainModule):
    """
    Pediatrics specialty domain focusing on pediatric red flags,
    acute presentations, and common pediatric conditions.

    Emphasizes recognition of serious illness in children and
    appropriate urgency triage.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="pediatrics",
            version="1.0.0",
            dependencies=[],
            description="Pediatric assessment and management focusing on red flags, acute presentations, infectious diseases, developmental surveillance, and common pediatric conditions with emphasis on urgent recognition",
            keywords=[
                # Core pediatrics
                "child", "children", "pediatric", "paediatric", "baby", "infant", "toddler",
                "neonate", "newborn", "adolescent", "teenager", "baby", "kid",

                # Red flags / emergencies
                "fever", "high temperature", "seizure", "convulsion", "fit", "meningitis",
                "sepsis", "septic", "dehydration", "difficulty breathing", "wheeze",
                "stridor", "croup", "bronchiolitis", "choking",

                # Common symptoms
                "rash", "vomiting", "diarrhea", "constipation", "abdominal pain", "tummy pain",
                "cough", "cold", "earache", "sore throat", "headache",

                # Neonatal
                "jaundice", "newborn", "feeding", "weight", "umbilical",

                # Development
                "development", "milestone", "walking", "talking", "growth", "height", "weight",

                # Infectious
                "chickenpox", "measles", "mumps", "rubella", "whooping cough", "scarlet fever",
                "slapped cheek", "hand foot mouth", "impetigo", "thrush",

                # Common conditions
                "asthma", "eczema", "allergy", "food allergy", "urticaria", "constipation",
                "bedwetting", "sleep", "behavior"
            ],
            capabilities=[
                "pediatric_red_flag_recognition", "fever_management", "respiratory_assessment",
                "gastrointestinal_evaluation", "infectious_disease_management",
                "developmental_surveillance", "growth_monitoring", "neonatal_assessment",
                "seizure_evaluation", "rash_assessment", "dehydration_assessment",
                "injury_prevention_counseling", "behavioral_concerns_evaluation",
                "asthma_management", "allergy_assessment", "acute_illness_triage"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """
        Process pediatric queries with emphasis on red flag recognition.
        """
        query_lower = query.lower()

        # EMERGENCY: Sepsis, meningitis, anaphylaxis
        if any(term in query_lower for term in ["sepsis", "septic", "meningitis", "anaphylaxis", "allergic reaction"]) and \
           any(term in query_lower for term in ["urgent", "emergency", "collapse", "unresponsive"]):
            return self._handle_pediatric_emergency(query, context)

        # EMERGENCY: Choking, severe respiratory distress
        if any(term in query_lower for term in ["choking", "can't breathe", "struggling to breathe", "apnea", "not breathing"]):
            return self._handle_choking_emergency(query, context)

        # Fever (very common pediatric concern)
        if any(term in query_lower for term in ["fever", "high temperature", "pyrexia", "hot"]):
            return self._handle_fever_query(query, context)

        # Seizure/convulsion
        if any(term in query_lower for term in ["seizure", "convulsion", "fit", "twitching", "unresponsive"]):
            return self._handle_seizure_query(query, context)

        # Respiratory distress
        if any(term in query_lower for term in ["breathing", "wheeze", "stridor", "croup", "bronchiolitis", "cough"]):
            return self._handle_respiratory_query(query, context)

        # Gastrointestinal
        if any(term in query_lower for term in ["vomiting", "diarrhea", "constipation", "abdominal pain", "tummy pain", "stomach pain"]):
            return self._handle_gi_query(query, context)

        # Rash
        if any(term in query_lower for term in ["rash", "spots", "hives", "urticaria", "bruising"]):
            return self._handle_rash_query(query, context)

        # Neonatal concerns
        if any(term in query_lower for term in ["newborn", "neonate", "jaundice", "umbilical", "cord"]):
            return self._handle_neonatal_query(query, context)

        # Head injury
        if any(term in query_lower for term in ["head injury", "fell", "hit head", "concussion"]):
            return self._handle_head_injury_query(query, context)

        # Developmental concerns
        if any(term in query_lower for term in ["development", "milestone", "walking", "talking", "delay"]):
            return self._handle_developmental_query(query, context)

        # Growth/nutrition
        if any(term in query_lower for term in ["growth", "height", "weight", "failure to thrive", "obesity", "eating"]):
            return self._handle_growth_query(query, context)

        # Common infectious diseases
        if any(term in query_lower for term in ["chickenpox", "measles", "mumps", "rubella", "whooping cough", "impetigo"]):
            return self._handle_infectious_query(query, context)

        # Earache/sore throat
        if any(term in query_lower for term in ["earache", "ear pain", "sore throat", "throat pain"]):
            return self._handle_ent_query(query, context)

        # Behavioral concerns
        if any(term in query_lower for term in ["behavior", "naughty", "aggressive", "adhd", "autism", "sleep"]):
            return self._handle_behavioral_query(query, context)

        # General pediatrics
        return self._handle_general_pediatric_query(query, context)

    def _handle_pediatric_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pediatric emergencies - sepsis, meningitis, anaphylaxis."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**PEDIATRIC EMERGENCY - IMMEDIATE ACTION REQUIRED**

**CALL 999/911/112 IMMEDIATELY IF:**
- Child is unresponsive
- Not breathing or breathing is abnormal
- Severe difficulty breathing
- Pale/mottled/blue (cyanosis)
- Fits/seizure lasting >5 minutes
- Severe abdominal pain with collapse
- Non-blanching rash (meningococcal sepsis)

**SEPSIS - LIFE-THREATENING**

**Red flags (any = urgent hospital assessment)**:
- Temperature >38°C or <36°C
- Heart rate outside normal range for age
- Respiratory rate outside normal range for age
- Oxygen saturation <92%
- Capillary refill time >2 seconds
- Reduced urine output (dry nappies >12 hours)
- Altered behavior (irritable, lethargic, not responding normally)
- Non-blanching rash (meningococcal disease)
- History of immune compromise

**Immediate action**:
- **Urgent hospital assessment** - do NOT delay
- **Antibiotics within 1 hour** if sepsis suspected (IV ceftriaxone, add vancomycin/aciclovir as indicated)
- **Fluid resuscitation** if shock
- **Oxygen** if hypoxic

**MENINGITIS - MEDICAL EMERGENCY**

**Red flags (suspect meningitis/meningococcal sepsis)**:
- Fever + headache + photophobia + neck stiffness
- Altered mental status (confusion, irritability, lethargy)
- Non-blanching rash (petechiae/purpura) - MANDATORY URGENT REFERRAL
- Seizure
- Bulging fontanelle (infants)
- Shock (pale, mottled, tachycardic, poor capillary refill)

**Non-blanching rash test**:
- Press glass against rash
- If rash does NOT fade (blanch) - URGENT MEDICAL ATTENTION (meningococcal sepsis until proven otherwise)
- Do NOT wait for other symptoms

**Immediate action**:
- **Urgent hospital admission** (do NOT give oral antibiotics, delay hospital transfer)
- **IV antibiotics** (ceftriaxone ± vancomycin)
- **Steroids** (dexamethasone for suspected bacterial meningitis >3 months)
- **ICU** if shock, raised ICP

**ANAPHYLAXIS - LIFE-THREATENING ALLERGIC REACTION**

**Diagnosis** (sudden onset, rapidly progressive, severe):
- **Airway**: Stridor, swelling (tongue, throat), hoarseness
- **Breathing**: Wheeze, respiratory distress, tachypnea, hypoxia
- **Circulation**: Hypotension, shock, tachycardia/bradycardia, collapse
- **Skin**: Urticaria (hives), angioedema, flushing, pruritus (ABSENT in 20%)
- **Gastrointestinal**: Vomiting, abdominal pain, diarrhea

**Immediate management**:
1. **Call for help** (999/911/112)
2. **IM adrenaline** (epinephrine) - outer mid-thigh:
   - **<6 years**: 150 mcg (0.15 mL of 1:1000)
   - **6-12 years**: 300 mcg (0.3 mL of 1:1000)
   - **>12 years**: 500 mcg (0.5 mL of 1:1000)
   - Repeat every 5 minutes if no improvement
3. **Remove trigger** if possible (stop IV drug, stinger)
4. **Call 999/911/112** for ambulance
5. **Position**: Lie flat with legs raised (unless breathing difficult - sit up)
6. **Oxygen**: 15 L/min if hypoxic
7. **Fluid bolus**: Crystalloid 20 mL/kg if shock
8. **Antihistamines**: Diphenhydramine 1 mg/kg IV/IM (adjunct, NOT替代 adrenaline)
9. **Steroids**: Hydrocortisone 4 mg/kg IV (adjunct, takes hours to work)

**Observation**: Minimum 4-6 hours after resolution (may be biphasic)

**SOURCES:** NICE NG51, RCPCH, Resuscitation Council
""",
            confidence=0.99,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Pediatric Emergency - Sepsis/Meningitis/Anaphylaxis",
                "urgency": "emergency",
                "sources": ["NICE NG51", "RCPCH", "Resuscitation Council"]
            }
        )

    def _handle_choking_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle choking emergency."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**CHOKING EMERGENCY - ACT IMMEDIATELY**

**IF CHILD IS CHOKING (CONSCIOUS)**:

**SIGNS OF CHOKING**:
- Unable to breathe/cry/speak
- Hands at throat (universal choking sign)
- Silent cough
- Cyanosis (blue lips/face)
- Loss of consciousness if not relieved

**IMMEDIATE ACTION**:

**INFANT (<1 YEAR)**:
1. **Sit down**, place infant face down along your forearm (support head/jaw), head lower than chest
2. **Give up to 5 back blows**: Between shoulder blades with heel of hand (check if object expelled after each blow)
3. **If unsuccessful**, turn infant face up along forearm (head lower than body), give up to 5 chest thrusts (2 fingers on lower half of sternum, push downward 1.5 inches, check if object expelled after each thrust)
4. **Alternate**: 5 back blows → 5 chest thrusts until object expelled OR infant becomes unconscious

**CHILD (>1 YEAR)**:
1. **Stand behind child**, wrap arms around waist (make fist, place between navel and rib cage)
2. **Give up to 5 abdominal thrusts** (Heimlich maneuver): Pull inward and upward (check if object expelled after each thrust)
3. **Repeat** until object expelled OR child becomes unconscious

**IF CHILD BECOMES UNCONSCIOUS**:
1. **Call for help** (999/911/112) if not already called
2. **Place on firm, flat surface** (back)
3. **Start CPR**: 30 chest compressions (lower half of sternum, at least 1/3 depth, 100-120/min) → 2 rescue breaths
4. **Look for object** before breaths: If visible, attempt to remove with finger sweep (ONLY if object can be seen and grasped)
5. **Continue CPR** until object expelled, child starts breathing, or help arrives

**AFTER CARE**:
- **All children who choked** need medical assessment (even if object expelled) - possible aspiration, airway injury, recurrence

**PREVENTION**:
- **Avoid high-risk foods** for <3 years: Whole grapes/tomatoes (cut in half), nuts, popcorn, hard candy, raw carrot/apple, marshmallows
- **Sit while eating**: No running/playing with food
- **Supervise meals**: Especially young children
- **Keep small objects out of reach**: Coins, buttons, batteries (especially button batteries - URGENT if ingested), balloons, small toys

**BUTTON BATTERY INGESTION - URGENT**:
- **Damage within hours**: Burns through esophagus, fistula, death
- **Urgent X-ray**: If battery in esophagus - urgent endoscopic removal
- **Do NOT induce vomiting**

**SOURCES:** Resuscitation Council, St John Ambulance
""",
            confidence=0.99,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Choking Emergency",
                "urgency": "emergency",
                "sources": ["Resuscitation Council", "St John Ambulance"]
            }
        )

    def _handle_fever_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle fever queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**FEVER IN CHILDREN**

**DEFINITION**: Temperature ≥38.0°C (100.4°F)

**MEASUREMENT**:
- **<6 months**: Rectal or axillary (rectal most accurate)
- **>6 months**: Axillary, tympanic (ear), oral, rectal
- **Forehead strips**: Less accurate, but reasonable for screening

**CAUSES**:
- **Viral** (70%): URTI, cold, flu, roseola, chickenpox, etc.
- **Bacterial** (30%): UTI, pneumonia, meningitis, sepsis, otitis media, cellulitis
- **Other**: Post-immunization (24-48 hours), overheating (over-wrapping), teething (mild, <38°C)

**FEVER RED FLAGS (URGENT HOSPITAL ASSESSMENT)**:

**Any of the following**:
- Age <3 months with fever ≥38°C
- Age 3-6 months with temperature ≥39°C
- Fever ≥5 days
- Petechial/non-blanching rash
- Seizure
- Stiff neck, photophobia
- Altered mental status (confusion, lethargy, irritability)
- Difficult breathing / rapid breathing
- Poor capillary refill (>2 seconds) / pale/mottled/blue
- Dehydration (dry nappies >12 hours, sunken fontanelle, dry mouth)
- Severe abdominal pain
- Reduced urine output
- Known immunocompromise
- Recent antibiotics (possible resistant infection)

**ASSESSMENT**:
- **Temperature**: How high? Duration? Response to antipyretics?
- **Associated symptoms**: Cough, vomiting, diarrhea, rash, ear pain, urinary symptoms, sore throat, irritability, lethargy
- **Hydration status**: Urine output, tears, moist mouth, fontanelle
- **Behavior**: Alert, playful, lethargic, irritable, difficult to console
- **Medical history**: Prematurity, chronic conditions, immunizations

**MANAGEMENT**:

**Treat the child, NOT the number**:
- **Well child** with fever but playing, alert, good hydration → observation at home
- **Unwell child** (lethargic, irritable, poor feeding, signs of dehydration) → urgent assessment

**Antipyretics** (for discomfort, NOT mandatory):
- **Paracetamol/Acetaminophen**: 15 mg/kg every 4-6 hours (max 4 doses/24h)
- **Ibuprofen**: 5-10 mg/kg every 6-8 hours (max 3 doses/24h) (>3 months only, >5 kg)
- **Alternating agents**: NOT routinely recommended (risk of dosing errors, no additional benefit)
- **Do NOT use** in <3 months (urgent assessment needed instead)

**Home care**:
- **Fluids**: Encourage fluids (breast milk, formula, water, diluted juice)
- **Clothing**: Light clothing, avoid over-wrapping (fever worsens with overheating)
- **Environment**: Comfortable room temperature (18-21°C), not too hot
- **Rest**: Allow child to rest as needed
- **Monitoring**: Check child regularly (especially at night), seek help if worsening

**FEVER SEIZURES** (Febrile seizures):
- **Age**: 6 months to 6 years (peak 12-18 months)
- **Trigger**: Rapid rise in temperature (not height of fever)
- **Simple febrile seizure**: Generalized, <15 minutes, once in 24 hours, no focal features
- **Management**:
  - **Protect child** from injury, place on side
  - **Do NOT** restrain, put anything in mouth
  - **Time seizure**: If >5 minutes → call ambulance
  - **After**: Seek medical assessment (first seizure = always assess, recurrent seizures = if unusual features)
- **Risk**: 2-5% of children, 30% recurrence, 1% later develop epilepsy (slightly higher than general population)
- **Prognosis**: Generally benign, no long-term effects, no treatment needed (prophylactic medications not recommended)

**POST-VACCINATION FEVER**:
- **Common**: 24-48 hours after vaccination
- **Management**: Antipyretics if uncomfortable, fluids, light clothing
- **Seek help** if fever >72 hours post-vaccination, or child unwell

**MENINGITIS RED FLAGS**:
- Non-blanching rash (petechiae/purpura) - PRESS GLASS TEST (if doesn't fade, URGENT)
- Fever + headache + photophobia + neck stiffness
- Altered mental status (confusion, lethargy, irritability)
- Bulging fontanelle (infants)
- Seizure

**WHEN TO SEEK URGENT MEDICAL HELP**:
- Any red flag (see above)
- You are worried about your child (parental concern is a red flag itself)
- No improvement or worsening after 48 hours
- Persistent fever >5 days
- You feel unsure or something is not right

**SOURCES:** NICE NG143, RCPCH
""",
            confidence=0.96,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Fever in Children",
                "sources": ["NICE NG143", "RCPCH"]
            }
        )

    def _handle_seizure_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle seizure queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**SEIZURES IN CHILDREN**

**IMMEDIATE ACTION DURING SEIZURE**:
1. **Protect from injury**: Remove harmful objects, place on soft surface, protect head
2. **DO NOT** restrain, put anything in mouth (risk of injury, obstruction, teeth damage)
3. **Position**: Recovery position (side) if possible to prevent aspiration
4. **Time**: How long does it last?
5. **Call ambulance if**: First seizure, >5 minutes, injury occurred, breathing difficulties, another seizure immediately after, child unwell afterwards, you are unsure/worried

**FEBRILE SEIZURES** (Most common childhood seizure):
- **Age**: 6 months to 6 years (peak 12-18 months)
- **Trigger**: Rapid rise in temperature (not height of fever)
- **Simple febrile seizure** (75%): Generalized tonic-clonic, <15 minutes, once in 24 hours, no focal features, returns to baseline within 1 hour
- **Complex febrile seizure** (25%): Focal, >15 minutes, multiple in 24 hours, or post-ictal deficit
- **Prognosis**: Generally benign, 2-5% of children, 30% recurrence risk, 1% later develop epilepsy (slightly higher than general population)
- **Management**: Treat underlying fever, antipyretics (do NOT prevent recurrence), reassurance, no prophylactic medications needed

**EPILEPSY**:
- **Definition**: ≥2 unprovoked seizures >24 hours apart
- **Incidence**: 0.5-1% of children
- **Types**: Generalized (absence, tonic-clonic, myoclonic, atonic), Focal (with/without impaired awareness), Unknown
- **Diagnosis**: Detailed history, witness account, EEG (may be normal between seizures), MRI (if focal or refractory)
- **Management**: Antiepileptic drugs (AEDs) if recurrent seizures or specific syndrome, first-line AEDs vary by seizure type (carbamazepine for focal, sodium valproate for generalized), ketogenic diet (refractory), surgery (select cases)

**ABSENCE SEIZURES** (Petit mal):
- **Age**: 4-12 years
- **Appearance**: Brief (5-10 seconds) staring spells, unresponsive, may flutter eyelids, no post-ictal confusion, returns immediately to baseline
- **Frequency**: Dozens to hundreds per day (may be mistaken for daydreaming, ADHD)
- **Triggers**: Hyperventilation (provocative test), sleep deprivation
- **Diagnosis**: EEG (typical 3 Hz spike-and-wave)
- **Prognosis**: 60-80% outgrow by adolescence, some develop generalized tonic-clonic seizures
- **Management**: Ethosuximide (first-line), sodium valproate, lamotrigine

**INFANTILE SPASMS** (West syndrome):
- **Age**: 4-8 months (rarely >2 years)
- **Appearance**: Sudden jerks (salaam seizures), head flexion, arm abduction, clusters (especially on waking), developmental regression
- **Causes**: Structural (tuberous sclerosis, stroke, malformation), metabolic, genetic, idiopathic
- **Diagnosis**: EEG (hypsarrhythmia - chaotic high-voltage slow waves), MRI (identify underlying cause)
- **EMERGENCY**: Early treatment critical for developmental outcome (every day delay worsens prognosis)
- **Management**: Adrenocorticotropic hormone (ACTH) or vigabatrin (especially if tuberous sclerosis), corticosteroids, ketogenic diet, treat underlying cause

**OTHER SEIZURE TYPES**:
- **Focal seizures**: May have aura (warning), motor signs (jerking, stiffening), sensory symptoms, autonomic symptoms, impaired awareness, automatisms (lip smacking, fidgeting)
- **Generalized tonic-clonic**: Tonic (stiffening), clonic (jerking), post-ictal (confusion, sleepiness)
- **Myoclonic**: Brief shock-like jerks, may be single or clusters
- **Atonic**: Sudden loss of tone (drop attacks), falls
- **Tonic**: Sudden stiffness, may fall

**CAUSES OF SEIZURES** (Acute/provoked vs. unprovoked/epilepsy):
- **Acute/provoked**: Fever (febrile seizures), hypoglycemia, hyponatremia, hypocalcemia, meningitis, encephalitis, head injury, stroke, drug withdrawal, toxins
- **Unprovoked/epilepsy**: Genetic, structural (malformations, stroke, tumor), metabolic, unknown

**ASSESSMENT**:
- **History**: Detailed description of seizure (onset, progression, duration, recovery), triggers, prodrome, aura, post-ictal state, developmental history, family history
- **Examination**: Neurological exam, dysmorphic features (if genetic syndrome), skin examination (sturge-weber, tuberous sclerosis)
- **Investigations** (if first unprovoked seizure):
  - **Blood glucose** (bedside) - if available, check immediately
  - **Electrolytes**: Sodium, calcium, magnesium, glucose
  - **Infection screen**: If fever or signs of infection
  - **EEG**: Interictal (between seizures), may be normal, helps classify seizure type
  - **MRI**: If focal seizure, abnormal neurological exam, refractory seizures, age <1 year

**RED FLAGS (URGENT)**:
- **First seizure**: Always seek medical assessment (determine cause, exclude meningitis)
- **Status epilepticus**: Seizure >5 minutes OR recurrent seizures without recovery → URGENT
- **Fever + seizure**: Exclude meningitis (especially if <18 months, unwell after, or complex febrile seizure)
- **Head injury**: Seizure after head injury → urgent CT, observe
- **Focal features**: May indicate structural lesion → MRI
- **Regressing development**: May indicate neurodegenerative disorder → urgent assessment

**LONG-TERM MANAGEMENT**:
- **Diagnosis**: Confirm epilepsy (recurrent unprovoked seizures), classify seizure type
- **Treatment**: AEDs if recurrent seizures or high risk of recurrence, choose based on seizure type, side effect profile
- **Safety**: Supervision during bathing, swimming, avoid heights, notify school (seizure action plan), avoid unsecured climbing
- **Driving**: Restrictions apply depending on seizure control (varies by country)
- **Prognosis**: Variable, depends on cause (idiopathic generalized often remits, symptomatic often persistent)

**SOURCES:** NICE CG137, RCPCH, ILAE
""",
            confidence=0.95,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Seizures in Children",
                "sources": ["NICE CG137", "RCPCH", "ILAE"]
            }
        )

    def _handle_respiratory_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle respiratory queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**RESPIRATORY PRESENTATIONS IN CHILDREN**

**RESPIRATORY DISTRESS - RED FLAGS**:
- **Stridor** (high-pitched sound on inspiration) - upper airway obstruction
- **Wheeze** (high-pitched expiratory sound) - lower airway obstruction
- **Grunting** (expiratory sound) - serious respiratory distress, attempt to increase PEEP
- **Recession** (chest indrawing): Subcostal, intercostal, sternal
- **Tachypnea** (fast breathing): See age-specific rates below
- **Oxygen saturation** <92%
- **Altered mental status**: Lethargy, irritability, confusion
- **Cyanosis** (blue lips/face) - LATE SIGN, URGENT
- **Apnea** (cessation of breathing) - URGENT

**NORMAL RESPIRATORY RATES (breaths/minute)**:
- **Newborn**: 40-60
- **Infant (1-12 months)**: 30-40
- **Toddler (1-2 years)**: 25-35
- **Preschool (3-5 years)**: 20-30
- **School age (6-12 years)**: 18-25
- **Adolescent (13-18 years)**: 12-20

**CROUP (Laryngotracheobronchitis)**:
- **Cause**: Viral (parainfluenza), age 6 months to 3 years (peak 2 years)
- **Symptoms**: Barking cough, stridor (worse at night/when upset), hoarse voice, low-grade fever
- **Severity** (Westley croup score):
  - **Mild**: Occasional stridor when agitated, no recession at rest
  - **Moderate**: Stridor at rest, recession, but alert
  - **Severe**: Stridor at rest + marked recession + lethargy/anxiety
  - **Impending respiratory failure**: Decreased stridor + decreased air entry + lethargy/obtunded
- **Management**:
  - **Mild**: Comfort, calm child, hydration
  - **Moderate**: Single dose of oral dexamethasone 0.15 mg/kg (reduces admission, shortens illness), consider nebulized epinephrine (adrenaline) if significant stridor
  - **Severe**: Urgent hospital admission, nebulized epinephrine 0.5 mL/kg of 1:1000 (max 5 mL), repeat every 20-30 min as needed, dexamethasone 0.6 mg/kg, consider ICU
  - **DO NOT**: Routine antibiotics (viral), physiotherapy (not helpful), laryngoscopy (unless alternative diagnosis suspected)

**BRONCHIOLITIS**:
- **Cause**: RSV (respiratory syncytial virus), age <2 years (peak 3-6 months)
- **Symptoms**: Coryza (runny nose), cough, fever, wheeze, feeding difficulty, respiratory distress
- **Management**: Supportive (oxygen if hypoxic, fluids if dehydrated, nasal suction), hospital if high risk (prematurity <32 weeks, <3 months, congenital heart disease, chronic lung disease, immunocompromise), **DO NOT** give routine antibiotics, salbutamol (ineffective in most), steroids (ineffective), chest physiotherapy
- **Admission criteria**: Oxygen saturation <92%, apnea, poor feeding (<50% normal), dehydration, social concerns

**WHEEZE** (Lower airway obstruction):
- **Asthma** (most common cause of recurrent wheeze): Recurrent wheeze + cough + shortness of breath ± chest tightness, often triggered by exercise, cold, allergens, infections, family history of atopy/asthma, age >1 year (usually), responds to bronchodilator (salbutamol/albuterol)
- **Viral-induced wheeze** (especially <3 years): Wheeze associated with colds, often does NOT respond to bronchodilator, many outgrow by school age
- **Management**:
  - **Salbutamol/albuterol**: 4-6 puffs via spacer (or 0.15 mg/kg nebulized if severe), repeat every 20 min for 3 doses, then hourly if needed, consider systemic steroids (prednisolone 1-2 mg/kg, max 40 mg) if moderate-severe
  - **Oxygen**: If hypoxic
  - **Ipratropium**: If severe (salbutamol + ipratropium combined)
  - **Magnesium sulfate**: IV (if life-threatening asthma not responding to initial treatment)
  - **Admission**: If poor response to bronchodilators, oxygen requirement, social concerns

**PNEUMONIA**:
- **Symptoms**: Fever, cough, tachypnea, difficulty breathing, chest pain, vomiting (especially in infants)
- **Causes**: Viral (RSV, influenza, adenovirus) - more common in <2 years; Bacterial (Streptococcus pneumoniae, Staphylococcus aureus, Haemophilus influenzae) - more common >2 years
- **Management**: Hospital if <2 years, oxygen requirement, dehydration, difficulty breathing, sepsis; antibiotics (high-dose amoxicillin 40-90 mg/kg/day in 2 divided doses) if bacterial suspected; supportive care (oxygen, fluids)

**FOREIGN BODY ASPIRATION**:
- **Suspect**: Sudden onset choking/cough/wheeze in previously well child, unilateral wheeze, decreased breath sounds, recurrent pneumonia
- **Management**: Urgent bronchoscopy for removal, DO NOT attempt blind finger sweep (may push object further), Heimlich if complete airway obstruction (choking)

**PERTUSSIS** (Whooping cough):
- **Symptoms**: Coryza, mild cough → paroxysmal cough (fits) → whoop (inspiratory gasp), vomiting after coughing, apnea (infants), cyanosis, duration >2 weeks ("100-day cough")
- **Management**: Supportive care, macrolide antibiotics (azithromycin, clarithromycin, erythromycin) if <3 weeks from cough onset (reduces transmission, may not alter symptoms), isolation (5 days of antibiotics or 3 weeks if untreated), admission if <6 months, complications (apnea, pneumonia, seizures, encephalopathy)

**INHALED FOREIGN BODY**:
- **Suspect**: Sudden onset of choking/cough/wheeze in a previously well child
- **Management**: Urgent referral for bronchoscopy, DO NOT use Heimlich maneuver if breathing (only if complete airway obstruction), consider CXR (may be normal, may show unilateral hyperinflation/atelectasis)

**SOURCES:** NICE, BTS, RCPCH
""",
            confidence=0.94,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Respiratory Presentations",
                "sources": ["NICE", "BTS", "RCPCH"]
            }
        )

    def _handle_gi_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle gastrointestinal queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**GASTROINTESTINAL PRESENTATIONS IN CHILDREN**

**GASTROENTERITIS** (Vomiting and Diarrhea):
- **Definition**: Increase in stool looseness and frequency (>3 stools/24 hours, looser than normal) ± vomiting
- **Causes**: Viral (rotavirus, norovirus, adenovirus), bacterial (salmonella, campylobacter, shigella, E. coli), parasitic (giardia, cryptosporidium)
- **Risk**: Dehydration (most common complication), especially <6 months, low birth weight, >6 stools/24 hours, >3 vomits/24 hours

**DEHYDRATION ASSESSMENT**:
- **Mild (1-3%)**: Normal, thirsty, moist mouth
- **Moderate (3-6%)**: Thirsty, dry mouth, sunken eyes, decreased urine output (dry nappies >6 hours), lethargic, irritable
- **Severe (>6%):** Drowsy, unresponsive, sunken fontanelle (infants), pale/mottled/cold extremities, poor capillary refill, deep breathing, tachycardia, oliguria/anuria

**MANAGEMENT**:
- **Rehydration**: ORS (oral rehydration solution) - small amounts frequently (5 mL every 2-5 minutes, gradually increase), breastfed babies should continue breastfeeding
- **Fluids**: Avoid sugary drinks (coke, juice) - worsen diarrhea, ORS is ideal, dilute apple juice can be used if ORS refused (mild diarrhea)
- **Diet**: Normal diet when rehydrated (complex carbohydrates, lean protein, fruits/vegetables), avoid fatty foods, high-sugar foods, initially avoid lactose if severe (transient lactose intolerance)
- **Medications**: DO NOT give routine antibiotics (only if dysentery - blood in stool + fever - suspect bacterial), loperamide NOT in children <12 (risk of ileus, CNS depression), antiemetics rarely used (consider if persistent vomiting preventing oral rehydration)

**ADMISSION CRITERIA**:
- Shock (pale/mottled, tachycardic, poor capillary refill)
- Altered mental status (lethargy, irritable, seizures)
- Severe dehydration (>6%)
- Inability to tolerate oral fluids (persistent vomiting)
- High-risk child (young infant, chronic illness, immunocompromise)
- Social concerns (unable to monitor at home)
- Abdominal signs (surgical abdomen suspected)

**RED FLAGS (URGENT)**:
- Blood in stool (dysentery) - bacterial cause, antibiotics indicated
- Bile-stained vomiting (green) - surgical emergency (intestinal obstruction, malrotation/volvulus)
- Abdominal distention, pain, tenderness (peritonitis) - surgical abdomen
- Severe abdominal pain with collapse - appendicitis, intussusception
- High fever + abdominal pain + vomiting - appendicitis

**APPENDICITIS**:
- **Symptoms**: Abdominal pain (periumbilical → right lower quadrant), vomiting, anorexia (pain precedes vomiting), fever (low-grade), pain on movement (coughing, jumping), migration of pain (classic)
- **Signs**: Tenderness at McBurney's point (RLQ), rebound tenderness, guarding, Rovsing's (LLQ pain causes RLQ pain), psoas sign (pain on extension of right hip), obturator sign (pain on internal rotation of right hip)
- **Investigation**: Ultrasound (first-line in children), CT (if ultrasound equivocal), CBC (elevated WBC), CRP
- **Management**: Urgent surgical consultation, IV fluids, antibiotics (preoperative), appendectomy (open or laparoscopic)

**INTUSSUSCEPTION**:
- **Age**: 3 months to 3 years (peak 6-12 months)
- **Symptoms**: Intermittent, colicky abdominal pain (child draws up legs), vomiting (becomes bilious), lethargy between episodes, "red currant jelly" stool (late sign - 50%), pallor, shock
- **Signs**: Sausage-shaped mass in abdomen (RLQ), RUQ emptiness (Dance sign)
- **Investigation**: Ultrasound (target sign/pseudo-kidney sign), abdominal X-ray (if perforation suspected)
- **Management**: Urgent pediatric surgical consultation, air or barium enema (diagnostic and therapeutic - 80% success), surgery if enema fails or perforated

**CONSTIPATION**:
- **Definition**: Infrequent passage of hard, painful stools
- **Causes**: Functional (95% - low fiber, poor fluid intake, withholding behavior, painful defecation → withholding cycle), organic (Hirschsprung's disease, hypothyroidism, cerebral palsy, medications)
- **Management**: Macrogol (PEG) laxatives (first-line) - start 0.5-1 g/kg/day, adjust to effect, may need long-term, stool softeners (lactulose), lubricants (paraffin), rectal medications (glycerin suppositories, enemas) for fecal impaction, disimpaction if needed (macrogol high dose or enemas), then maintenance with macrogol
- **Red flags**: Delayed passage of meconium (>48 hours), ribbon stools, abdominal distention, failure to thrive, severe abdominal pain - exclude Hirschsprung's disease

**GASTROESOPHAGEAL REFLUX (GERD)**:
- **Infants**: Physiological reflux common (posseting), resolves by 12-18 months, GERD if complications (poor weight gain, irritability, feeding refusal, respiratory symptoms, esophagitis)
- **Older children**: Heartburn, retrosternal pain, dysphagia, regurgitation, abdominal pain, cough, wheeze (especially at night)
- **Management**: Positioning (upright after feeds, thickened feeds, smaller frequent feeds), alginates (infants), PPIs (omeprazole, lanzoprazole) if confirmed GERD, surgery (fundoplication) if refractory

**ABDOMINAL PAIN**:
- **Functional abdominal pain** (most common): Recurrent abdominal pain without organic pathology, periumbilical, associated with stress/anxiety, normal growth, normal examination, management includes reassurance, dietary changes, psychological approaches
- **Surgical abdomen** (red flags): Pain with fever, vomiting, localized tenderness, guarding/rebound, distention, blood in stool/vomit - urgent referral

**SOURCES:** NICE, ESPGHAN, RCPCH
""",
            confidence=0.93,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Gastrointestinal Presentations",
                "sources": ["NICE", "ESPGHAN", "RCPCH"]
            }
        )

    def _handle_rash_query(self, str: str, context: dict) -> DomainQueryResult:
        """Handle rash queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**RASH IN CHILDREN**

**MENINGOCOCCAL RASH - MEDICAL EMERGENCY**:
- **Non-blanching petechiae/purpura**: Press glass against rash - if it does NOT fade (blanch), call 999/911/112 IMMEDIATELY
- **Distribution**: Anywhere, often starts on trunk/skin folds
- **Progression**: Petechiae (pinpoint) → purpura (larger) → ecchymoses (bruises) → necrosis
- **Associated**: Fever, irritability, lethargy, sepsis, meningitis
- **Action**: Give IM benzylpenicillin if available (delay transfer), urgent hospital transfer

**NON-BLANCHING RASH DIFFERENTIAL**:
- **Meningococcal sepsis** (most urgent): Fever, unwell, non-blanching rash - URGENT
- **Idiopathic thrombocytopenic purpura (ITP)**: Well child, petechiae/purpura, bruising, NOT otherwise unwell, platelets low (but child well)
- **Henoch-Schönlein purpura (HSP)**: Palpable purpura on buttocks/lower extremities, abdominal pain, arthritis, renal involvement (hematuria)
- **Mechanical/trauma**: Bruising from falls, accidents - consider NAI if inconsistent history

**COMMON VIRAL EXANTHEMS**:

**CHICKENPOX (Varicella)**:
- **Incubation**: 10-21 days (infectious 48 hours before rash until all lesions crusted)
- **Rash**: Crops of macules → papules → vesicles (teardrop) → pustules → crusts, all stages present simultaneously, starts on trunk/face → spreads, itchy
- **Symptoms**: Fever, malaise, headache, sore throat
- **Management**: Supportive (calamine lotion, antihistamines for itch, paracetamol for fever, trim fingernails, isolate until non-infectious), AVOID ibuprofen (increased risk of necrotizing soft tissue infections), AVOID aspirin (Reye's syndrome), consider acyclovir if immunocompromised or severe disease
- **Complications**: Secondary bacterial skin infection (cellulitis, impetigo), pneumonia, encephalitis, rarely death

**MEASLES**:
- **Incubation**: 10-12 days
- **Prodrome**: Fever, cough, coryza, conjunctivitis (3 C's), Koplik spots (white lesions on buccal mucosa - pathognomonic but transient)
- **Rash**: Maculopapular, starts on head/neck → spreads downward, becomes confluent, fades after 3-4 days (leaves desquamation)
- **Complications**: Pneumonia (most common cause of death), otitis media, diarrhea, encephalitis (1:1000), subacute sclerosing panencephalitis (SSPE - rare, years later), death (1:1000 in developed, 1:10 in malnourished)
- **Prevention**: MMR vaccine (first dose 12-13 months, second dose 3 years 4 months), highly effective

**RUBELLA** (German measles):
- **Incubation**: 14-21 days
- **Rash**: Pink maculopapular, starts on face → spreads, fades after 2-3 days
- **Symptoms**: Mild fever, sore throat, lymphadenopathy (especially posterior auricular, suboccipital)
- **Complications**: Arthralgia (common in adult women), encephalitis (rare), congenital rubella syndrome if pregnant (cataracts, deafness, cardiac defects, IUGR, miscarriage)
- **Prevention**: MMR vaccine

**ROSEOLA INFANTUM** (Exanthem subitum, Sixth disease):
- **Age**: 6 months to 3 years (peak 6-15 months)
- **Cause**: HHV-6 (human herpesvirus 6)
- **Course**: High fever (3-5 days) → fever resolves → rash appears (rose-pink macules/papules on trunk) → fades after 1-2 days
- **Complications**: Febrile seizures (due to high fever), otherwise benign

**FIFTH DISEASE** (Erythema infectiosum, slapped cheek):
- **Cause**: Parvovirus B19
- **Rash**: "Slapped cheek" appearance (bright red cheeks), then lacy reticulated rash on body (especially arms), may worsen with heat/exercise
- **Symptoms**: Mild fever, malaise, joint pain (especially in adult women)
- **Complications**: Aplastic crisis in sickle cell/other hemolytic anemias, hydrops fetalis if pregnant (risk of fetal loss)

**HAND, FOOT, AND MOUTH DISEASE**:
- **Cause**: Coxsackie virus A16, enterovirus 71
- **Rash**: Vesicular lesions on hands, feet, buttocks, mouth (painful ulcers), may be on trunk
- **Symptoms**: Fever, malaise, sore mouth, decreased oral intake
- **Management**: Supportive (oral analgesia, fluids), isolation (very contagious), avoid salty/spicy/acidic foods
- **Complications**: Dehydration (if painful mouth ulcers), nail shedding (weeks later), rare neurological complications (enterovirus 71)

**IMPETIGO** (School sores):
- **Cause**: Staphylococcus aureus, Streptococcus pyogenes
- **Rash**: Honey-colored crusted plaques, around nose/mouth, on extremities, itchy
- **Management**: Topical antibiotics (mupirocin, fusidic acid) if localized, oral antibiotics (flucloxacillin) if extensive, hygiene measures, exclude from school until treated (48 hours)

**SCARLET FEVER**:
- **Cause**: Group A streptococcus (pharyngitis + erythrogenic toxin)
- **Rash**: Sandpaper-like micropapular rash, circumoral pallor, Pastia's lines (petechiae in skin folds), strawberry tongue (white coating → red strawberry)
- **Symptoms**: Fever, sore throat, tender anterior cervical lymphadenopathy
- **Management**: Oral penicillin V (or amoxicillin) for 10 days, exclude from school for 24 hours after starting antibiotics

**KAWASAKI DISEASE**:
- **Age**: <5 years (peak 18-24 months), can occur older
- **Diagnostic criteria (Fever ≥5 days + ≥4 of 5)**:
  1. Bilateral non-purulent conjunctivitis
  2. Rash (polymorphous - maculopapular, urticarial, etc.)
  3. Cervical lymphadenopathy (usually unilateral, >1.5 cm)
  4. Strawberry tongue, cracked lips
  5. Erythema/edema of hands/feet (later desquamation)
- **Complications**: Coronary artery aneurysms (15-25% untreated, 5% with treatment), myocardial infarction, death
- **Management**: IV immunoglobulin (2 g/kg single dose) + high-dose aspirin, then low-dose aspirin for 6-8 weeks, echocardiogram (baseline, 2-6 weeks, 6-12 months)

**HENÖCH-SCHÖNLEIN PURPURA (HSP)**:
- **Vasculitis**: IgA-mediated, most common childhood vasculitis
- **Presentation**: Palpable purpura on buttocks/lower extremities (mandatory), abdominal pain, arthritis/arthralgia, renal involvement (hematuria, proteinuria)
- **Management**: Supportive (pain control), monitor renal function (BP, urine dipstick regularly), may need steroids for severe abdominal pain/renal disease
- **Prognosis**: Usually self-limiting (4-6 weeks), renal disease may progress to chronic kidney disease (rare)

**URTICARIA** (Hives, wheals):
- **Appearance**: Transient, pruritic, erythematous, raised plaques/welts, blanch with pressure, can be any size/shape, migratory
- **Causes**: Allergic (foods, medications, insect stings), physical (cold, heat, pressure, sunlight, exercise), idiopathic (most), viral (upper respiratory infection)
- **Management**: Avoid triggers (if identified), antihistamines (cetirizine, loratadine), short course (3-5 days) usually sufficient, consider longer if chronic (>6 weeks)
- **Red flags**: Angioedema (swelling of lips/tongue/airway) - risk of airway obstruction, anaphylaxis (urticaria + respiratory/cardiovascular symptoms) - urgent

**ALLERGIC RASH**:
- **Maculopapular**: Most common drug eruption, appears 1-2 weeks after starting medication, starts on trunk → spreads
- **Management**: Stop offending drug (if suspected), antihistamines if pruritic, topical steroids, avoid re-exposure
- **Severe**: Stevens-Johnson syndrome/toxic epidermal necrolysis (SJS/TEN) - widespread blistering, mucosal involvement, hospital admission

**SOURCES:** NICE, RCPCH, BMJ Best Practice
""",
            confidence=0.94,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Rash in Children",
                "sources": ["NICE", "RCPCH", "BMJ Best Practice"]
            }
        )

    def _handle_neonatal_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle neonatal queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**NEONATAL CONCERNS (First 28 days)**

**JAUNDICE**:
- **Physiological jaundice** (60% term, 80% preterm): Appears day 2-3, peaks day 3-5, resolves by 2 weeks, unconjugated (indirect) hyperbilirubinemia
- **Breast milk jaundice**: Prolonged (beyond 2 weeks), unconjugated, benign
- **Pathological jaundice**: Appears <24 hours or >2 weeks, rises rapidly (>8.5 μmol/L/hour), requires phototherapy/exchange transfusion, conjugated (direct) hyperbilirubinemia (pale stool, dark urine)
- **Investigation**: Serum bilirubin (total & direct), blood group (mother & baby), Coombs test (if ABO/Rh incompatibility), infection screen (CRP, blood culture), thyroid function (if prolonged)
- **Management**:
  - **Phototherapy**: If bilirubin exceeds treatment thresholds (based on hours of life, gestational age, risk factors), converts bilirubin to excretable form
  - **Exchange transfusion**: If bilirubin very high or not responding to phototherapy (rare)
  - **Treat underlying cause**: Infection, hypothyroidism, biliary atresia (urgent referral for Kasai procedure)
  - **Breastfeeding**: Continue (do NOT stop breastfeeding), feed frequently (8-12 times/24 hours)
- **Red flags**: Jaundice <24 hours, pale stool, dark urine (conjugated bilirubin), lethargy, poor feeding, fever, bilirubin >340 μmol/L (term) or >250 μmol/L (preterm)

**FEEDING DIFFICULTIES**:
- **Breastfeeding**:
  - **Positioning**: Baby facing mother, nose to nipple, wait for wide mouth, aim nipple to roof of mouth, chin touches breast first
  - **Latch assessment**: Clicking sounds, pain during feed, visible areola (should see some areola above lip, more below), audible swallowing
  - **Frequency**: 8-12 times/24 hours (on demand), baby should have ≥6 wet nappies/24 hours after day 5, ≥3 yellow stools/24 hours after day 5
  - **Weight loss**: Up to 10% acceptable, >10% requires assessment
  - **Support**: Lactation consultant, peer support, breast feeding nurse
- **Formula feeding**:
  - **Preparation**: Sterilize bottles, correct powder-to-water ratio (1 scoop to 30 mL water), feed temperature (body temperature)
  - **Frequency**: Baby-led, typically 6-8 feeds/24 hours, 60-120 mL/feed (varies)
  - **Types**: First infant formula (whey-based, suitable 0-12 months), hungry baby formula (casein-based, slower digestion), comfort formula (partially hydrolyzed protein, for colic/constipation), specialized formulas (extensively hydrolyzed, amino acid - for cow's milk protein allergy, soy - rarely indicated)
- **Red flags**: Poor weight gain or weight loss, dehydration (<6 wet nappies/24 hours), lethargy, weak suck, feeding aversion

**UMBILICAL CORD CARE**:
- **Separation**: 5-15 days (average 7-10 days)
- **Care**: Keep clean and dry, fold nappy below cord to allow air exposure, clean with plain water if soiled, avoid antiseptics (alcohol, chlorhexidine) routinely
- **Abnormal**: Delayed separation (>3 weeks) → investigate (immune deficiency, leukocyte adhesion defect), persistent discharge → exclude umbilical granuloma, patent urachus, omphalitis
- **Omphalitis**: Infection of umbilical stump, redness, swelling, pus, fever → URGENT antibiotics (sepsis risk)

**NEWBORN SCREENING**:
- **Blood spot** (Guthrie test, heel prick, day 5-8): Hypothyroidism, cystic fibrosis, sickle cell disease, MCADD, PKU, others (varies by country)
- **Physical examination**: Congenital heart defects (pulse oximetry), developmental dysplasia of the hip (barlow/ortolani), undescended testes, cataract, congenital cataract
- **Hearing test**: Automated otoacoustic emissions (AOAE) or automated auditory brainstem response (AABR)

**CONGENITAL ABNORMALITIES**:
- **Developmental dysplasia of the hip (DDH)**: Risk factors (breech, family history), screening (clinical examination, ultrasound if high risk or abnormal examination), treatment (Pavlik harness, surgery if late diagnosis)
- **Undescended testes (cryptorchidism)**: Examination at birth and 6-8 weeks, treatment (orchidopexy 6-12 months - reduces infertility, cancer risk)
- **Congenital heart disease**: Cyanotic (tetralogy of Fallot, transposition), acyanotic (VSD, ASD, PDA), screening (pulse oximetry >24 hours, antenatal ultrasound), management (prostaglandin, surgery)
- **Cleft lip/palate: Feeding difficulties (special teats, tubes), surgical repair (lip 3 months, palate 12 months), multidisciplinary team

**NEONATAL SEPSIS**:
- **Risk factors**: Prolonged rupture of membranes (>18 hours), maternal fever, chorioamnionitis, prematurity, low birth weight, invasive procedures (ventilation, central lines)
- **Symptoms**: Poor feeding, lethargy, temperature instability (hypothermia more common), apnea, bradycardia, respiratory distress, poor perfusion, hypotension, hypoglycemia, seizures, jaundice
- **Investigation**: Blood culture, CRP, full blood count, lumbar puncture (if indicated), urine culture (if >72 hours), consider chest X-ray (respiratory symptoms)
- **Management**: Urgent antibiotics (IV ampicillin + gentamicin ± cefotaxime), supportive care (IV fluids, respiratory support), treat for 36-48 hours if cultures negative (or 7-10 days if meningitis confirmed)

**SOURCES:** NICE, RCPCH, AAP
""",
            confidence=0.93,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Neonatal Concerns",
                "sources": ["NICE", "RCPCH", "AAP"]
            }
        )

    def _handle_head_injury_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle head injury queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**PEDIATRIC HEAD INJURY**

**IMMEDIATE ACTION**:
- If unconscious, not breathing normally → Start CPR, call 999/911/112
- If neck injury suspected (fall from height, diving accident) → Do NOT move neck (stabilize head-neck position)

**RED FLAGS (URGENT HOSPITAL ASSESSMENT)**:
- **Loss of consciousness** (>30 seconds, or any if <1 year)
- **Vomiting** (≥2 episodes, especially if delayed)
- **Amnesia** (>5 minutes for events before/after injury)
- **Confusion**, disorientation, abnormal behavior
- **Seizure** during or after injury
- **Headache** progressively worsening
- **Drowsiness**, difficulty waking
- **Visual disturbances**, double vision, unequal pupils
- **Weakness**, numbness, coordination problems
- **Suspicious mechanism** (fall >1 meter, high-speed injury, assault)
- **Bleeding from ear**, CSF leak (clear fluid from nose/ear)
- **Scalp hematoma** (especially large, boggy in <2 years - possible skull fracture)
- **Age**: <1 year (especially <6 months) - higher risk of intracranial injury, non-accidental injury (NAI) consideration

**MINOR HEAD INJURY** (Low risk):
- Brief loss of consciousness (<30 seconds) in child >1 year
- No red flags
- Normal behavior after brief period of irritability
- Acting normally, playing, alert

**OBSERVATION AT HOME** (if advised by healthcare professional):
- **Monitor** for red flags (see above)
- **Wake child** every 2-4 hours for first 24 hours (or as advised)
- **Paracetamol/acetaminophen** for headache (avoid ibuprofen - increases bleeding risk)
- **Rest** from vigorous activity/sports for 24-48 hours
- **No return to school** until fully recovered
- **Gradual return** to normal activities as symptoms improve

**SKULL FRACTURE**:
- **Linear fracture**: Most common, usually managed conservatively (unless depressed or associated with intracranial injury)
- **Depressed fracture**: Indented skull bone ("ping-pong fracture"), may need surgical elevation if depressed > skull thickness
- **Basilar fracture**: Signs (bleeding from ear, CSF leak, raccoon eyes, Battle's sign - bruising over mastoid), hospital admission

**INTRACRANIAL INJURY**:
- **Epidural hematoma**: Arterial bleed (usually middle meningeal artery), lucid interval → rapid deterioration, surgical emergency
- **Subdural hematoma**: Venous bleed (bridging veins), more common in <2 years (especially shaken baby), may have delay in symptoms
- **Cerebral contusion**: Bruising of brain tissue, may cause seizures, focal deficits
- **Diffuse axonal injury**: Shearing of axons (severe acceleration-deceleration injuries), coma common

**CONCUSSION** (Mild traumatic brain injury):
- **Definition**: Trauma-induced alteration in mental function, with or without loss of consciousness
- **Symptoms**: Headache, dizziness, nausea/vomiting, confusion, memory problems, balance problems, sensitivity to light/noise, fatigue, mood changes, sleep disturbance
- **Management**: Physical rest (24-48 hours), cognitive rest (limit schoolwork, screens, reading), gradual return to activities (stepwise: light activity → school → sports), monitor for worsening symptoms (rare but serious - second impact syndrome)
- **Return to play**: Gradual, symptom-limited, minimum 6 days (for most), medical clearance before full contact sports

**NON-ACCIDENTAL INJURY (NAI)**:
- **Consider especially in**:
  - Inconsistent mechanism (injury doesn't match history)
  - Delayed presentation
  - Recurrent injuries
  - Injuries inconsistent with developmental stage
  - Associated with other injuries (bruising, fractures, retinal hemorrhages)
  - Story changes
  - No witnessed explanation
- **Action**: Safeguarding referral, coagulation screen (if bleeding disorder suspected), skeletal survey (if <2 years), ophthalmology review (retinal hemorrhages), CT head (if indicated), social work involvement

**WHEN TO SEEK URGENT MEDICAL HELP**:
- Any red flag (see above)
- Worsening symptoms despite rest
- No improvement after 24-48 hours
- You are worried about your child

**PREVENTION**:
- Car seats/booster seats (age/size-appropriate, rear-facing as long as possible - minimum 15 months, preferably 2-4 years)
- Helmets (cycling, skiing, skateboarding, horse riding)
- Supervision (especially near heights, water, roads)
- Childproofing (gates, window guards, corner protectors)
- Sports safety (rules, equipment, supervision)

**SOURCES:** NICE CG176, RCPCH, CHALICE
""",
            confidence=0.95,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Head Injury",
                "sources": ["NICE CG176", "RCPCH", "CHALICE"]
            }
        )

    def _handle_developmental_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle developmental queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**DEVELOPMENTAL SURVEILLANCE**

**DEVELOPMENTAL MILESTONES** (Approximate, range is normal):

**GROSS MOTOR**:
- **6 weeks**: Lifts head when prone
- **3 months**: Holds head steady, bears weight on legs when supported
- **6 months**: Sits without support, rolls front to back
- **9 months**: Crawls, pulls to stand
- **12 months**: Walks holding hands, may stand alone
- **18 months**: Walks independently, runs stiffly, kicks ball
- **2 years**: Walks up/down stairs holding rail, runs, jumps with both feet
- **3 years**: Walks up/down stairs alternating feet, rides tricycle, catches ball

**FINE MOTOR**:
- **3 months**: Hands open, grasps objects placed in hand
- **6 months**: Transfers objects between hands, reaches for objects, bangs objects
- **9 months**: Pincer grasp (thumb and finger), bangs two objects together
- **12 months**: Pincer grasp mature, puts objects in container, points with index finger
- **18 months**: Builds tower of 2-3 blocks, scribbles, turns pages of book
- **2 years**: Builds tower of 6 blocks, draws circles, uses spoon well
- **3 years**: Copies circle, builds tower of 9 blocks, draws person with head, trunk, limbs

**SOCIAL/COMMUNICATION**:
- **6 weeks**: Social smile
- **3 months**: Vocalizes (coos, gurgles), laughs
- **6 months**: Responds to name, babbling (ba-ba, ma-ma)
- **9 months**: Understands "no", uses gestures (waves bye-bye), says "mama" or "dada" non-specifically
- **12 months**: Says 1-2 words with meaning, follows simple commands ("give me"), mimics actions
- **18 months**: Says 10-20 words, 2-word phrases ("more juice"), points to wants
- **2 years**: Says 50+ words, 2-3 word sentences ("want juice"), names familiar objects
- **3 years**: 3-4 word sentences, uses "I", "me", "you", asks "what", "where" questions, sings songs

**RED FLAGS (Refer for Developmental Assessment)**:
- **No social smile** by 6 weeks
- **Not sitting** by 9 months
- **Not walking** by 18 months
- **No babbling** by 12 months
- **No single words** by 18 months
- **No two-word phrases** by 24 months
- **Loss of skills** (regression) - URGENT
- **Absence of joint attention** (pointing, showing, following gaze)
- **Repetitive behaviors**, hand flapping, toe walking
- **Lack of eye contact**, poor social engagement

**AUTISM SPECTRUM DISORDER (ASD)**:
- **Prevalence**: 1-2% (increasing)
- **Male:Female**: 4:1
- **Core features**: Social communication deficits, restricted/repetitive behaviors, sensory differences
- **Red flags**: No joint attention, poor eye contact, delayed/regressed language, repetitive play, lining up toys, hand flapping, toe walking, sensory sensitivities (noise, texture)
- **Screening**: M-CHAT (Modified Checklist for Autism in Toddlers) at 18-24 months
- **Diagnosis**: Multidisciplinary assessment (pediatrician, speech therapist, psychologist), observational tools (ADOS), developmental history
- **Management**: Early intervention (behavioral, speech, occupational therapy), parent training, educational support

**DEVELOPMENTAL DELAY**:
- **Global delay**: Delay in ≥2 domains (motor, speech, cognitive)
- **Specific delay**: Single domain affected (e.g., speech delay)
- **Causes**: Genetic (Down syndrome, Fragile X), cerebral palsy, autism, hearing loss, vision problems, psychosocial deprivation, hypothyroidism (congenital), metabolic disorders
- **Investigation**: Hearing test, vision assessment, genetic testing (karyotype, microarray), thyroid function, brain imaging (if abnormal neurology or regression)

**CEREBRAL PALSY**:
- **Definition**: Permanent disorder of movement/posture due to non-progressive disturbance of developing brain
- **Types**: Spastic (70% - hemiplegia, diplegia, quadriplegia), Dyskinetic (dystonia, athetosis), Ataxic
- **Risk factors**: Prematurity, periventricular leukomalacia, stroke, infection, birth asphyxia
- **Early signs**: Abnormal tone (hypotonia early → hypertonia later), asymmetrical movement, persistent primitive reflexes, delayed motor milestones
- **Management**: Multidisciplinary (physiotherapy, occupational therapy, orthopedics, neurology), orthoses, botox, orthopedic surgery

**SPEECH DELAY**:
- **Normal variation**: Late bloomer (especially boys), usually catches up by 3 years
- **Causes**: Hearing loss (glue ear most common), autism, developmental language disorder, cerebral palsy, psychosocial deprivation, intellectual disability
- **Red flags**: No babbling by 12 months, no single words by 18 months, no two-word phrases by 24 months, loss of language skills
- **Management**: Hearing assessment, speech therapy referral, developmental surveillance, autism screen if social communication concerns

**DEVELOPMENTAL SURVEILLANCE**:
- **At every well-child visit**: Ask about development, observe child, elicit parental concerns
- **Parental concern**: Highly predictive of actual developmental problems - always take seriously
- **Screening tools**: Ages and Stages Questionnaire (ASQ), Parents' Evaluation of Developmental Status (PEDS)
- **Early identification**: Improves outcomes, allows early intervention

**SOURCES:** NICE, RCPCH, CDC
""",
            confidence=0.92,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Developmental Surveillance",
                "sources": ["NICE", "RCPCH", "CDC"]
            }
        )

    def _handle_growth_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle growth and nutrition queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**GROWTH AND NUTRITION**

**GROWTH MONITORING**:
- **Height/Length**: Measure recumbent until 2 years, then standing
- **Weight**: Naked/minimal clothing, same scale each time
- **Head circumference**: Until 2 years (brain growth indicator)
- **Growth charts**: WHO growth standards (0-4 years), UK-WHO (0-4 years), then UK growth reference (4-18 years)
- **Plot**: At birth, 6-8 weeks, 3-4 months, then regularly (every few months in infancy, less frequently as child grows)
- **Red flags**: Crossing centiles upward (especially weight) or downward, height <0.4th centile, weight <0.4th centile, head circumference crossing centiles, height <3rd centile with reduced growth velocity

**FAILURE TO THRIVE** (FTT):
- **Definition**: Weight falling through ≥2 centiles or weight <0.4th centile, weight-for-height <2nd centile, weight-for-age <2nd centile
- **Causes**: Inadequate intake (80%): breastfeeding difficulties, inadequate formula, poverty, neglect, feeding problems; Increased requirements: congenital heart disease, chronic lung disease, infections; Malabsorption: celiac disease, cystic fibrosis, cow's milk protein allergy; Chronic illness: renal, liver, cardiac; Endocrine: hypothyroidism, growth hormone deficiency
- **Management**: Detailed feeding history, growth chart review, physical examination, investigations (if indicated: CBC, ESR/CRP, coeliac screen, thyroid, urine, sweat test, etc.), dietetic referral, increase caloric intake (fortify feeds, more frequent feeds), address psychosocial issues

**OBESITY**:
- **Definition**: BMI ≥95th centile (obesity), BMI 85th-95th centile (overweight)
- **BMI calculation**: Weight (kg) / Height (m)², plot on BMI centile chart
- **Complications**: Type 2 diabetes, hypertension, dyslipidemia, fatty liver, obstructive sleep apnea, orthopedic problems (Blount's disease, SCFE), psychological (depression, low self-esteem, bullying), social exclusion
- **Red flags**: BMI ≥99.6th centile, associated comorbidities (diabetes, hypertension, OSA), rapid weight gain, family history of early cardiovascular disease
- **Management**: Multidisciplinary approach (dietitian, psychologist, exercise specialist), family-based lifestyle changes (NOT just child), dietary modifications (reduce sugary drinks, fast food, portion sizes), increase physical activity (60 minutes daily), reduce screen time, behavioral strategies (self-monitoring, goal setting), very low-calorie diets (only in specialist care, severe obesity), bariatric surgery (rare, only in specialist centers with strict criteria)

**SHORT STATURE**:
- **Definition**: Height <0.4th centile
- **Causes**: Familial (both parents short), constitutional delay (late bloomer, normal growth velocity, delayed bone age), chronic illness (celiac, IBD, renal, cardiac, cardiac), endocrine (growth hormone deficiency, hypothyroidism, Cushing's), genetic (Turner syndrome, Noonan syndrome), skeletal dysplasia (achondroplasia), psychosocial deprivation
- **Red flags**: Height <0.4th centile, height falling through centiles, disproportion (short limbs vs trunk), dysmorphic features, associated symptoms (polyuria/polydipsia - diabetes, headaches/vision - pituitary, gastrointestinal - celiac), family history of consanguinity, early deaths
- **Investigations**: Bone age (X-ray left hand/wrist), growth hormone, IGF-1, thyroid function, coeliac screen, karyotype (girls), referral to pediatric endocrinologist

**TALL STATURE**:
- **Definition**: Height >99.6th centile
- **Causes**: Familial (tall parents), constitutional (early growth spurt), obesity, Klinefelter syndrome (XXY), Marfan syndrome, growth hormone excess (gigantism, pituitary adenoma), androgen insensitivity
- **Red flags**: Height >> mid-parental height, disproportion (arm span > height), dysmorphic features (Marfan - tall, slender, hypermobile, lens dislocation, aortic root dilation), associated symptoms (headache, vision - pituitary), rapid growth velocity
- **Management**: Exclude pathology (especially Marfan - cardiac monitoring), reassurance if familial

**MICRONUTRIENT DEFICIENCIES**:
- **Iron deficiency anemia**: Common (especially 6 months to 3 years), picky eaters, low iron intake (cow's milk before 12 months, >500 mL/day cow's milk), symptoms: pallor, fatigue, poor feeding, pica (eating non-foods), management: iron supplements, dietary changes (red meat, fortified cereals, green leafy vegetables), limit cow's milk to 300 mL/day
- **Vitamin D deficiency**: Risk factors (darker skin, exclusive breastfeeding without supplements, winter, indoor lifestyle), symptoms: rickets (bowed legs, swelling of wrists, poor growth, seizures), management: vitamin D supplements (400 IU daily for all <4 years, higher if deficient), calcium
- **Vitamin A deficiency**: Rare in developed countries, risk (malabsorption, restrictive diet), symptoms: night blindness, xerophthalmia, immune deficiency, management: vitamin A supplements

**FEEDING DIFFICULTIES**:
- **Breastfeeding**: See neonatal section
- **Bottle feeding**: See neonatal section
- **Weaning (introducing solids)**: Start around 6 months (not before 4 months), single-ingredient vegetables/fruits first, introduce new foods every 3 days (identify allergies), progress textures (puree → mashed → finger foods → family foods), avoid choking hazards (whole grapes, nuts, popcorn, hot dogs), introduce allergenic foods early (peanut, egg - 6-12 months, high risk infants - early introduction after allergy assessment)
- **Picky eating**: Common in toddlers (neophobia), usually resolves with repeated exposure (8-15 exposures), avoid pressure, serve family foods, role modeling, limit grazing/snacking, consider multivitamin if very restrictive diet
- **Food refusal**: Manage by structured meals (3 meals, 2-3 snacks), child decides how much to eat (not parents), no pressure/coercion, pleasant mealtime environment, limit distractions (TV, screens), consistent routine

**SOURCES:** NICE, RCPCH, WHO Growth Standards
""",
            confidence=0.91,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Growth and Nutrition",
                "sources": ["NICE", "RCPCH", "WHO Growth Standards"]
            }
        )

    def _handle_infectious_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle common infectious disease queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**COMMON PEDIATRIC INFECTIOUS DISEASES**

**CHICKENPOX (Varicella)** - see Rash section

**MEASLES** - see Rash section

**MUMPS**:
- **Incubation**: 14-25 days (average 17 days)
- **Symptoms**: Low-grade fever, headache, malaise, anorexia, then parotitis (swollen parotid glands - one or both), pain with chewing/sour foods
- **Complications**: Orchitis (testicular inflammation - especially postpubertal), oophoritis, pancreatitis, meningitis, encephalitis, deafness, infertility (rare)
- **Management**: Supportive (cold compresses, soft diet, analgesia), isolation (5 days from parotitis onset), exclude from school for 5 days
- **Prevention**: MMR vaccine (first dose 12-13 months, second dose 3 years 4 months), very effective

**RUBELLA** (German measles) - see Rash section

**WHOOPING COUGH** (Pertussis) - see Respiratory section

**SCARLET FEVER** - see Rash section

**HAND, FOOT, AND MOUTH DISEASE** - see Rash section

**FIFTH DISEASE** (Slapped cheek) - see Rash section

**ROSEOLA** - see Rash section

**IMPETIGO** (School sores) - see Rash section

**KAWASAKI DISEASE** - see Rash section

**HERPANGINA**:
- **Cause**: Coxsackie A virus
- **Symptoms**: Fever, sore throat, painful vesicles/ulcers on posterior pharynx, tonsils, soft palate, may have lesions on hands/feet (but not mouth - unlike HFMD)
- **Management**: Supportive (oral analgesia, fluids, avoid acidic/spicy foods), self-limiting (7-10 days)

**GASTROENTERITIS** - see Gastrointestinal section

**UPPER RESPIRATORY TRACT INFECTIONS (URTI)**:
- **Common cold**: Nasal congestion, rhinorrhea, sore throat, cough, low-grade fever, self-limiting (7-10 days), supportive (nasal saline, analgesia, fluids), avoid antibiotics (viral), decongestants not recommended <6 years, cough suppressants not recommended <6 years
- **Pharyngitis/tonsillitis**: Sore throat, difficulty swallowing, fever, tender cervical lymphadenopathy, exudate on tonsils, viral (70%) vs bacterial (30% - group A strep), rapid strep test/throat culture if bacterial suspected, antibiotics (penicillin V, amoxicillin) if confirmed bacterial, consider infectious mononucleosis (EBV) if adolescent with fatigue, splenomegaly, atypical lymphocytes, avoid amoxicillin/ampicillin (causes rash if EBV)
- **Otitis media**: Ear pain, fever, irritability, tugging/rubbing ear, poor feeding/sleep, vomiting (younger children), tympanic membrane erythema, bulging, loss of landmarks, viral (most common) vs bacterial, antibiotics (amoxicillin, especially if <2 years, bilateral, systemic symptoms, discharge >48 hours, symptoms >3 days), analgesia (paracetamol/acetaminophen), avoid decongestants/antihistamines (not effective)

**URINARY TRACT INFECTION (UTI)**:
- **Prevalence**: 5-7% of febrile illnesses in <2 years, more common in girls
- **Symptoms**: Fever (often only sign in infants), irritability, vomiting, poor feeding, failure to thrive, older children: dysuria, frequency, urgency, abdominal pain, flank pain
- **Red flags**: Any fever >38°C in <3 months, fever >39°C in 3-6 months, fever without focus, fever >48 hours, UTI in past, atypical UTI (non-E. coli, systemic symptoms)
- **Investigation**: Urine dipstick (leukocytes, nitrites), urine culture (MSU, catheter, suprapubic aspirate in infants), consider ultrasound if atypical UTI or recurrent UTIs
- **Management**: Antibiotics (nitrofurantoin, trimethoprim, cefalexin, depending on local resistance patterns) for 3 days (older children) or 7-10 days (infants, atypical UTIs), investigate renal tract if recurrent or atypical (ultrasound, MCUG, DMSA)

**GLANDULAR FEVER** (Infectious mononucleosis):
- **Cause**: Epstein-Barr virus (EBV), adolescents/young adults
- **Symptoms**: Fever, severe sore throat, tonsillar exudate, cervical lymphadenopathy (often posterior), fatigue, malaise, splenomegaly (50%), hepatomegaly (20%), rash (especially if given amoxicillin - "amoxicillin rash")
- **Diagnosis**: MonoSpot (heterophile antibody), EBV serology, atypical lymphocytes on blood film
- **Management**: Supportive (rest, fluids, analgesia, avoid contact sports if splenomegaly - rupture risk), avoid amoxicillin/ampicillin, corticosteroids if airway compromise (severe tonsillar hypertrophy)
- **Complications**: Splenic rupture, airway obstruction, hepatitis, hemolytic anemia, thrombocytopenia, neurological (Guillain-Barré, Bell's palsy)

**DENGUE FEVER**:
- **Cause**: Mosquito-borne flavivirus (Aedes mosquito)
- **Symptoms**: Sudden high fever, severe headache, retro-orbital pain, myalgia/arthralgia ("breakbone fever"), maculopapular rash, petechiae, tourniquet test positive, recovery in 7-10 days
- **Severe dengue** (Dengue hemorrhagic fever/shock): Plasma leakage (pleural effusion, ascites), bleeding (petechiae, ecchymoses, GI bleeding), shock, organ impairment
- **Management**: Supportive (IV fluids, close monitoring, avoid NSAIDs - increases bleeding risk), admit if warning signs (abdominal pain, persistent vomiting, clinical fluid accumulation, mucosal bleeding, lethargy, liver enlargement >2 cm, increasing hematocrit with decreasing platelets)
- **Prevention**: Mosquito avoidance (repellent, clothing, screens)

**Sources:** NICE, RCPCH, Health Protection Agency
""",
            confidence=0.90,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Common Pediatric Infectious Diseases",
                "sources": ["NICE", "RCPCH", "HPA"]
            }
        )

    def _handle_ent_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle earache/sore throat queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**EARACHE (OTALGIA)**:

**ACUTE OTITIS MEDIA (AOM)**:
- **Prevalence**: Most common cause of earache in children, 80% have at least one episode by age 3
- **Symptoms**: Ear pain, fever, irritability, tugging/rubbing ear, poor feeding/sleep, vomiting (younger children), hearing loss (older children)
- **Signs**: Tympanic membrane erythema, bulging, loss of landmarks, decreased mobility, perforation with discharge
- **Causes**: Viral (most common), bacterial (Streptococcus pneumoniae, Haemophilus influenzae, Moraxella catarrhalis)
- **Management**:
  - **Analgesia**: Paracetamol/acetaminophen 15 mg/kg q4-6h OR ibuprofen 5-10 mg/kg q6-8h (>3 months, >5 kg)
  - **Antibiotics**: NOT routine for uncomplicated AOM (most resolve spontaneously), consider if <2 years, bilateral AOM, systemic symptoms, discharge >48 hours, symptoms >3 days, high risk (immune compromise, cochlear implant, Down syndrome)
  - **Antibiotic choice**: Amoxicillin 40-90 mg/kg/day in 2 divided doses for 5 days (or 10 days if <2 years or severe), if penicillin allergy - erythromycin, clarithromycin, or azithromycin
  - **Follow-up**: Reassess if not improving after 48-72 hours, consider alternative diagnosis (mastoiditis)
- **Prevention**: Avoid tobacco smoke, reduce pacifier use after 6 months, breastfeeding, pneumococcal vaccine, influenza vaccine

**OTITIS MEDIA WITH EFFUSION (OME)** ("Glue ear"):
- **Definition**: Fluid in middle ear without infection/inflammation, conductive hearing loss
- **Risk factors**: Recent URTI, passive smoking, adenoidal hypertrophy, cleft palate, Down syndrome
- **Symptoms**: Hearing loss (child asks to repeat, turns TV up loud), delayed speech/language, behavioral problems, inattention, poor school performance
- **Management**: Watchful waiting for 3 months (most resolve), consider hearing assessment if persistent >3 months, consider grommets (tympanostomy tubes) if hearing loss >25-30 dB in both ears for >3 months and speech/language delay or educational/behavioral problems, adenoidectomy (if nasal symptoms)
- **NOT indicated**: Antibiotics (not infection), antihistamines/decongestants (ineffective)

**OTITIS EXTERNA** (Swimmer's ear):
- **Definition**: Infection of ear canal skin, often after swimming
- **Symptoms**: Ear pain (worse with tragal pressure, jaw movement), ear discharge, itching, decreased hearing, canal edema, erythema
- **Management**: Aural toilet (clean debris), topical antibiotic/steroid drops (ciprofloxacin/dexamethasone), avoid water entry (keep dry, ear plugs when swimming), analgesia, oral antibiotics if spreading (cellulitis)

**SORE THROAT**:

**VIRAL PHARYNGITIS** (70%):
- **Symptoms**: Sore throat, nasal congestion, rhinorrhea, cough, hoarseness, conjunctivitis, viral exanthem, low-grade fever
- **Signs**: Mild erythema of pharynx/tonsils, tonsils may be enlarged but without exudate, cervical lymphadenopathy (usually mild, not tender)
- **Management**: Supportive (fluids, soft diet, analgesia - paracetamol/acetaminophen, ibuprofen), saltwater gargles (older children), avoid antibiotics

**BACTERIAL PHARYNGITIS/TONSILLITIS** (Group A Streptococcus - GAS) (30%):
- **Symptoms**: Sudden onset sore throat, painful swallowing, fever, headache, nausea/vomiting, abdominal pain (especially in children)
- **Signs**: Tonsillar exudate, tender anterior cervical lymphadenopathy, palatal petechiae, scarlatiniform rash (scarlet fever), absence of cough/coryza (Centor criteria)
- **Diagnosis**: Rapid strep test (rapid antigen detection test - RADT) OR throat culture (gold standard), treat if positive
- **Management**: Antibiotics (penicillin V 250 mg QDS or amoxicillin 50 mg/kg/day in 2 divided doses for 10 days, erythromycin if penicillin allergy), analgesia (paracetamol/acetaminophen, ibuprofen), exclude from school for 24 hours after starting antibiotics
- **Complications**: Peritonsillar abscess (quinsy), post-streptococcal glomerulonephritis, rheumatic fever (rare in developed countries with appropriate treatment)

**PERITONSILLAR ABSCESS (QUINSY)**:
- **Symptoms**: Severe sore throat, unilateral throat pain, difficulty swallowing (drooling), muffled voice ("hot potato voice"), trismus (difficulty opening mouth), fever
- **Signs**: Unilateral tonsillar swelling, deviation of uvula to opposite side, trismus, tender cervical lymphadenopathy
- **Management**: Urgent ENT referral, needle aspiration or incision and drainage, antibiotics (penicillin + metronidazole or co-amoxiclav), analgesia, IV fluids if dehydrated

**INFECTIOUS MONONUCLEOSIS** (Glandular fever):
- **Cause**: Epstein-Barr virus (EBV), adolescents/young adults
- **Symptoms**: Severe sore throat, fever, fatigue, malaise, cervical lymphadenopathy (especially posterior), splenomegaly, hepatomegaly
- **Signs**: Tonsillar exudate, palatal petechiae, periorbital edema, maculopapular rash (especially if given amoxicillin), splenomegaly
- **Management**: Supportive (rest, fluids, analgesia), avoid amoxicillin/ampicillin (causes rash), avoid contact sports if splenomegaly (rupture risk), corticosteroids if airway compromise (severe tonsillar hypertrophy)

**FOREIGN BODY**:
- **Ear**: Beads, toys, food, insects - symptoms (pain, discharge, decreased hearing), management (remove with suction/microscopy if accessible, referral if not, do NOT attempt if difficult or risk of injury)
- **Nose**: Beads, toys, food, paper - symptoms (unilateral nasal discharge, foul odor, bleeding), management (remove if easily accessible, referral if not, do NOT push further back)
- **Throat**: Food, coins, toys - urgent if airway compromise (choking), non-choking foreign bodies may require removal under general anesthesia

**SOURCES:** NICE, RCPCH, ENT UK
""",
            confidence=0.92,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Earache and Sore Throat",
                "sources": ["NICE", "RCPCH", "ENT UK"]
            }
        )

    def _handle_behavioral_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle behavioral concern queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**BEHAVIORAL CONCERNS IN CHILDREN**

**TEMPER TANTRUMS**:
- **Normal behavior**: Common in toddlers (1-3 years), especially 18-36 months, developmental stage (independence, limited language, frustration), outgrow by 4-5 years
- **Triggers**: Hunger, fatigue, frustration, transition, overstimulation, illness, wanting independence, limited communication
- **Management**:
  - **Prevention**: Regular routine, adequate sleep/snacks, warning before transitions, offer limited choices ("red or blue cup?"), positive reinforcement (praise good behavior)
  - **During**: Stay calm (do not get angry), ensure safety (do not let child hurt self/others), ignore minor tantrums (do not reinforce with attention), do NOT give in (teaches tantrums work)
  - **After**: Reconnect, praise calming, discuss (if older child), move on
- **Red flags**: Daily tantrums >15 minutes, self-harm or aggression, tantrums after 4-5 years, tantrums in multiple settings (home, school, childcare)

**SLEEP PROBLEMS**:
- **Infants (0-12 months)**:
  - **Night wakings**: Normal (all wake, some can self-settle, some need help), gradual retreat (teach self-settling), responsive feeding (night feeds normal first months)
  - **Settling difficulties**: Association with parent (rocking, feeding to sleep), teach independent settling (gradual retreat, camping out, controlled comforting)
- **Toddlers/preschoolers**:
  - **Resistance at bedtime**: Stall tactics, fear of missing out, separation anxiety, consistent bedtime routine, clear boundaries, quiet time before bed
  - **Night wakings**: Check briefly, boring, minimal interaction, return to bed (super nanny method), sleep clock (can get up when clock shows sun)
- **School-age**:
  - **Difficulty falling asleep**: Screen time (avoid screens 1 hour before bed), caffeine, anxiety, routine, dark room, relaxation techniques
  - **Nightmares**: Common 3-6 years, comfort, reassure, discuss (if old enough), limit scary media
  - **Sleep terrors**: Different from nightmares (occur first third of night, child does NOT remember, do NOT wake, keep safe, wait out)

**OPPOSITIONAL DEFIANT DISORDER (ODD)**:
- **Definition**: Pattern of angry/irritable mood, argumentative/defiant behavior, vindictiveness lasting ≥6 months
- **Symptoms**: Loses temper, argues with adults, defies/refuses to comply with rules, deliberately annoys others, blames others, angry/resentful, spiteful/vindictive
- **Prevalence**: 3-5%
- **Risk factors**: Temperamental (difficulty regulating emotions), harsh/inconsistent discipline, parental mental health, family conflict, socioeconomic disadvantage
- **Management**: Parenting programs (Incredible Years, Triple P), positive parenting (clear expectations, consistent consequences, praise good behavior, time-out for misbehavior), family therapy, child CBT, address comorbidities (ADHD, anxiety, learning difficulties)

**ATTENTION DEFICIT HYPERACTIVITY DISORDER (ADHD)**:
- **Definition**: Pattern of inattention and/or hyperactivity-impulsivity interfering with functioning or development, present before age 12, present in ≥2 settings (home, school)
- **Prevalence**: 5% (male:female 3:1)
- **Types**: Predominantly inattentive (ADD), predominantly hyperactive-impulsive, combined
- **Symptoms** (must have ≥6 for <17 years, ≥5 for ≥17 years):
  - **Inattention**: Difficulty sustaining attention, doesn't listen, fails to finish tasks, difficulty organizing, avoids tasks requiring sustained effort, loses things, easily distracted, forgetful
  - **Hyperactivity**: Fidgets, leaves seat, runs/climbs excessively (in adolescents, feeling restless), difficulty playing quietly, "on the go", excessive talking
  - **Impulsivity**: Blurts out answers, difficulty waiting turn, interrupts/intrudes
- **Diagnosis**: Comprehensive assessment (parent/teacher questionnaires - Conners, SNAP, clinical interview, observation, medical exclusion), school involvement, specialist referral (pediatrician, child psychiatrist)
- **Management**:
  - **First-line**: Parent training/education programs, behavioral therapy (especially <6 years), school support (IEP, 504 plan, classroom accommodations)
  - **Medication** (if ≥6 years and moderate-severe or non-responsive to behavioral interventions):
    - **Stimulants** (methylphenidate, amphetamines): Most effective, first-line, monitor height/weight/BP/sleep/appetite, consider "drug holidays" ( weekends, holidays)
    - **Non-stimulants** (atomoxetine, guanfacine, clonidine): Alternative if stimulants ineffective or not tolerated, especially if comorbid anxiety/tics
- **Prognosis**: 50% persist into adulthood, impairments (academic, occupational, social, relationships), increased risk of comorbidities (oppositional defiant disorder, conduct disorder, anxiety, depression, substance use)

**AUTISM SPECTRUM DISORDER (ASD)** - see Developmental section

**ANXIETY**:
- **Types**: Separation anxiety (common 6 months to 3 years, persistent if interferes with functioning), specific phobias, social anxiety, generalized anxiety disorder
- **Symptoms**: Physical (headaches, stomachaches, nausea), behavioral (avoidance, clinginess, meltdowns), cognitive (worries, negative thoughts)
- **Management**: CBT, gradual exposure (facing fears gradually), relaxation techniques (deep breathing, progressive muscle relaxation), parent support, school involvement, medications (SSRIs - specialist initiation)

**DEPRESSION**:
- **Prevalence**: 2-3% (adolescents)
- **Symptoms**: Low mood, anhedonia (loss of interest), irritability (especially in children), sleep/appetite changes, fatigue, worthlessness/guilt, concentration difficulties, thoughts of death/suicide
- **Risk factors**: Family history, adverse childhood experiences, chronic illness, bullying, LGBTQ+, social isolation
- **Management**: CBT (first-line mild-moderate), SSRI (fluoxetine first-line if moderate-severe or not responding to CBT), urgent referral if suicidal ideation, hospitalization if high risk

**ENURESIS** (Bedwetting):
- **Definition**: Involuntary urination in children ≥5 years (daytime, nighttime, or both)
- **Nocturnal enuresis** (more common): Primary (never dry), secondary (relapse after ≥6 months dry)
- **Causes**: Genetic (76% if both parents, 44% if one parent), nocturnal polyuria, reduced bladder capacity, deep sleep, constipation, UTI
- **Management**: Reassurance (not child's fault, NOT deliberate), bladder training (regular toileting, fluid intake), enuresis alarm (first-line, most effective long-term), desmopressin (second-line, for short-term or if alarm fails/not tolerated), address constipation

**ENCOPRESIS** (Soiling):
- **Definition**: Involuntary passage of feces in inappropriate places in children ≥4 years (or developmental equivalent)
- **Causes**: Constipation with overflow incontinence (most common), withholding behavior, painful defecation, Hirschsprung's disease (rare)
- **Management**: Disimpaction (macrogol high dose or enemas), maintenance macrogol, toilet training (regular toileting after meals), reward system, behavioral interventions, exclude organic causes if red flags (delayed meconium, ribbon stools, failure to thrive)

**SOURCES:** NICE, RCPCH, AACAP
""",
            confidence=0.90,
            metadata={
                "specialty": "Pediatrics",
                "focus": "Behavioral Concerns",
                "sources": ["NICE", "RCPCH", "AACAP"]
            }
        )

    def _handle_general_pediatric_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general pediatric queries."""

        return DomainQueryResult(
            domain_name="pediatrics",
            answer="""
**PEDIATRICS - GENERAL APPROACH TO THE UNWELL CHILD**

**PEDIATRIC ASSESSMENT**:

**Appearance** (most important indicator):
- **Well**: Alert, playful, interactive, smiling, normal color, good eye contact
- **Unwell**: Lethargic, irritable, poor interaction, difficult to console, pale/mottled, poor eye contact, reduced activity

**ABCDE approach** (for acute illness):
- **A**irway: Obstruction, stridor, hoarseness
- **B**reathing: Rate, effort (recession, grunting, nasal flaring), oxygen saturation, breath sounds
- **C**irculation: Heart rate, capillary refill, pulses, blood pressure, skin color/temperature
- **D**isability: Consciousness (AVPU), response to pain, posture, seizures
- **E**xposure: Temperature, rash, signs of trauma, injuries

**PEDIATRIC VITAL SIGNS** (age-dependent):
- **Heart rate**: Newborn 100-160, Infant 100-160, Toddler 90-150, Preschool 80-140, School-age 70-120, Adolescent 60-100
- **Respiratory rate**: Newborn 40-60, Infant 30-40, Toddler 25-35, Preschool 20-30, School-age 18-25, Adolescent 12-20
- **Systolic BP**: Newborn 60-90, Infant 70-100, Toddler 90-105, Preschool 95-110, School-age 100-120, Adolescent 110-135

**RED FLAGS** (any = urgent medical assessment):
- Temperature <36°C or >38°C (<3 months) or >39°C (3-6 months)
- Heart rate or respiratory rate outside normal range
- Oxygen saturation <92%
- Capillary refill >2 seconds
- Non-blanching rash
- Seizure
- Altered mental status (confusion, lethargy, irritability)
- Poor feeding/inability to tolerate fluids
- Reduced urine output (dry nappies >12 hours)
- Severe respiratory distress (stridor, wheeze, grunting, recession)
- Severe abdominal pain with collapse
- Dehydration
- Recent antibiotics
- Immunocompromise
- Parental concern ("you know your child best")

**ACUTE FEVER** - see Fever section

**COMMON PEDIATRIC CONDITIONS**:
- Respiratory: Croup, bronchiolitis, wheeze, pneumonia - see Respiratory section
- Gastrointestinal: Gastroenteritis, appendicitis, constipation - see GI section
- Infectious diseases: Chickenpox, measles, etc. - see Rash section, Infectious section
- Neonatal: Jaundice, feeding difficulties - see Neonatal section
- Developmental: Milestones, autism, speech delay - see Developmental section
- Growth: Failure to thrive, obesity - see Growth section
- Behavioral: Tantrums, sleep, ADHD, autism - see Behavioral section

**INJURY PREVENTION**:
- **Car safety**: Age/size-appropriate restraints, rear-facing as long as possible
- **Home safety**: Gates, window guards, cupboard locks, smoke detectors, hot water temperature (<49°C)
- **Water safety**: Supervision around water, pool fences, swimming lessons
- **Burn prevention**: Sunscreen, sun protection, keep hot drinks out of reach
- **Fall prevention**: Window guards, stair gates, safe sleep surfaces
- **Choking prevention**: Avoid high-risk foods, supervise meals, keep small objects out of reach
- **Poisoning prevention**: Lock cabinets, keep medicines/cleaning products out of reach
- **Sun safety**: Sunscreen (SPF 30+), hats, shade, avoid midday sun

**IMMUNIZATIONS** (UK schedule, may vary by country):
- **8 weeks**: 6-in-1 (diphtheria, tetanus, whooping cough, polio, Hib, hepatitis B), Rotavirus, PCV (pneumococcal), MenB
- **12 weeks**: 6-in-1 (2nd dose), Rotavirus (2nd dose)
- **16 weeks**: 6-in-1 (3rd dose), PCV (2nd dose)
- **1 year**: Hib/MenC, PCV (3rd dose), MenB (2nd dose), MMR (1st dose)
- **2-3 years**: Flu vaccine (annual)
- **3 years 4 months**: MMR (2nd dose), 4-in-1 pre-school booster
- **12-13 years**: HPV vaccine (2 doses)
- **14 years**: 3-in-1 teenage booster (tetanus, diphtheria, polio), MenACWY

**SAFEGUARDING**:
- **Signs of abuse**: Unexplained injuries, injuries inconsistent with development/history, delay in seeking care, repeated presentations, parental concern about different injuries, neglect (poor hygiene, inadequate clothing, food, medical care)
- **Action**: Safeguarding referral, coagulation screen if bleeding disorder suspected, skeletal survey if <2 years, ophthalmology review (retinal hemorrhages), CT head (if indicated), social work involvement

**WHEN TO SEEK URGENT MEDICAL HELP**:
- Any red flag (see above)
- You are worried about your child (parental concern is a red flag)
- No improvement or worsening after 48 hours
- Persistent fever >5 days
- You feel unsure or something is not right
- Trust your instincts

**SOURCES:** NICE, RCPCH, Resuscitation Council
""",
            confidence=0.90,
            metadata={
                "specialty": "Pediatrics",
                "focus": "General Pediatrics",
                "sources": ["NICE", "RCPCH", "Resuscitation Council"]
            }
        )


def create_pediatrics_domain():
    """
    Factory function to create pediatrics domain instance.

    Returns:
        PediatricsDomain: Configured pediatrics specialty domain
    """
    return PediatricsDomain()
