"""
Infectious Diseases Domain for GPDISC
Comprehensive infectious disease consultation covering sepsis, antibiotic stewardship,
tropical diseases, vaccination, and infection control.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class InfectiousDiseasesDomain(BaseDomainModule):
    """
    Infectious Diseases Specialist Domain

    Covers:
    - Sepsis recognition and management
    - Antibiotic selection and stewardship
    - Culture interpretation
    - Fever of unknown origin investigation
    - Tropical diseases recognition
    - Vaccination schedules
    - Infection control principles
    - Post-operative infections
    - UTI, pneumonia, skin infections
    - Meningitis/encephalitis
    - HIV and AIDS
    - Viral hepatitis (B, C)
    - COVID-19, influenza, RSV
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="infectious_diseases",
            version="1.0.0",
            dependencies=[],
            description="Infectious Diseases: sepsis, antibiotics, tropical diseases, vaccination, HIV, hepatitis, COVID-19",
            keywords=[
                # Infection types
                "infection", "infectious", "bacteria", "virus", "viral", "fungal", "parasite",
                "sepsis", "septic", "bacteremia", "fungemia", "viremia",
                "fever", "pyrexia", "temperature", "febrile",

                # Specific infections
                "uti", "urinary tract infection", "cystitis", "pyelonephritis",
                "pneumonia", "chest infection", "respiratory infection",
                "meningitis", "encephalitis", "brain infection",
                "cellulitis", "abscess", "skin infection", "wound infection",
                "endocarditis", "heart valve infection",
                "diverticulitis", "appendicitis", "peritonitis", "abdominal infection",

                # Tropical/travel
                "malaria", "dengue", "chikungunya", "zika", "yellow fever",
                "typhoid", "paratyphoid", "cholera",
                "ebola", "marburg", "lassa fever",
                "schistosomiasis", "leishmaniasis", "trypanosomiasis",
                "tuberculosis", "tb", "leprosy",

                # HIV/hepatitis
                "hiv", "aids", "antiretroviral", "art",
                "hepatitis b", "hepatitis c", "hbv", "hcv",

                # COVID-19/influenza
                "covid", "covid-19", "coronavirus", "sars-cov-2",
                "influenza", "flu", "h1n1", "rsv", "respiratory syncytial virus",

                # Antibiotics
                "antibiotic", "antimicrobial", "antibacterial",
                "penicillin", "amoxicillin", "cephalosporin", "ciprofloxacin",
                "vancomycin", "mrsa", "mrsa", "c. diff", "clostridium difficile",

                # Lab tests
                "culture", "blood culture", "urine culture", "sputum culture",
                "sensitivity", "resistance", "susceptibility", "mc&s",
                "crp", "esr", "procalcitonin", "wbc", "white cell count",

                # Prevention
                "vaccine", "vaccination", "immunization", "booster",
                "infection control", "isolation", "quarantine", "ppe",
                "travel medicine", "travel health", "malaria prophylaxis"
            ],
            capabilities=[
                "sepsis_recognition_management",
                "antibiotic_stewardship",
                "culture_interpretation",
                "fever_investigation",
                "tropical_diseases_recognition",
                "vaccination_guidance",
                "infection_control",
                "uti_management",
                "pneumonia_management",
                "meningitis_management",
                "hiv_management",
                "hepatitis_management",
                "covid19_management",
                "influenza_management"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Route infectious disease query to appropriate handler"""
        query_lower = query.lower()

        # Sepsis
        if any(term in query_lower for term in ["sepsis", "septic shock", "bacteremia"]):
            return self._handle_sepsis(query, context)

        # Antibiotics
        elif any(term in query_lower for term in ["antibiotic", "antimicrobial", "antibacterial", "mrsa", "c. diff", "clostridium"]):
            return self._handle_antibiotics(query, context)

        # Culture interpretation
        elif any(term in query_lower for term in ["culture", "sensitivity", "resistance", "mc&s", "susceptibility"]):
            return self._interpret_culture(query, context)

        # Fever
        elif any(term in query_lower for term in ["fever", "pyrexia", "febrile", "temperature", "fever of unknown origin", "fuo"]):
            return self._handle_fever(query, context)

        # Tropical diseases
        elif any(term in query_lower for term in ["malaria", "dengue", "chikungunya", "zika", "typhoid", "yellow fever", "ebola", "tuberculosis", "tb"]):
            return self._handle_tropical(query, context)

        # HIV
        elif any(term in query_lower for term in ["hiv", "aids", "antiretroviral", "art"]):
            return self._handle_hiv(query, context)

        # Hepatitis
        elif any(term in query_lower for term in ["hepatitis", "hbv", "hcv"]):
            return self._handle_hepatitis(query, context)

        # COVID-19
        elif any(term in query_lower for term in ["covid", "coronavirus", "sars-cov-2"]):
            return self._handle_covid(query, context)

        # Influenza
        elif any(term in query_lower for term in ["influenza", "flu", "h1n1"]):
            return self._handle_influenza(query, context)

        # Meningitis
        elif "meningit" in query_lower or "encephalit" in query_lower:
            return self._handle_meningitis(query, context)

        # UTI
        elif any(term in query_lower for term in ["uti", "urinary tract infection", "cystitis", "pyelonephritis"]):
            return self._handle_uti(query, context)

        # Pneumonia
        elif any(term in query_lower for term in ["pneumonia", "chest infection", "respiratory infection"]):
            return self._handle_pneumonia(query, context)

        # Skin/soft tissue
        elif any(term in query_lower for term in ["cellulitis", "abscess", "skin infection", "wound infection"]):
            return self._handle_skin_infection(query, context)

        # Vaccination
        elif any(term in query_lower for term in ["vaccine", "vaccination", "immunization", "booster"]):
            return self._handle_vaccination(query, context)

        # Travel medicine
        elif any(term in query_lower for term in ["travel", "malaria prophylaxis", "travel medicine", "travel health"]):
            return self._handle_travel_medicine(query, context)

        # General infectious diseases
        else:
            return self._handle_general_infectious(query, context)

    def _handle_sepsis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sepsis queries"""
        answer = """**Sepsis and Septic Shock Management**

**Definitions (Sepsis-3):**

**Sepsis:**
- **Life-threatening organ dysfunction** caused by dysregulated host response to infection
- **Organ dysfunction:** Increase in SOFA score ≥ 2 ( Sequential Organ Failure Assessment)
- **Clinical criteria:** qSOFA (2 or more = high risk of sepsis):
  - **Respiratory rate ≥ 22**
  - **Altered mentation** (GCS < 15)
  - **Systolic BP ≤ 100 mmHg**

**Septic Shock:**
- **Sepsis +** persistent hypotension requiring vasopressors
- **Lactate ≥ 2 mmol/L** despite adequate volume resuscitation

**Recognition (Red Flags):**

**Systemic Inflammatory Response Syndrome (SIRS):**
- **2 or more of:**
  - **Temperature > 38°C** or < 36°C
  - **Heart rate > 90 bpm**
  - **Respiratory rate > 20** or PaCO2 < 32 mmHg
  - **WBC > 12,000** or < 4,000 or > 10% bands

**Quick SOFA (qSOFA):**
- **Respiratory rate ≥ 22**
- **Altered mentation**
- **Systolic BP ≤ 100 mmHg**

**Management (Hour-1 Bundle):**

**1. Measure Lactate:**
- **Lactate ≥ 4 mmol/L:** High mortality risk (> 40%)
- **Repeat lactate** if initial lactate elevated (goal: decrease by ≥ 10% over 2 hours)

**2. Obtain Blood Cultures:**
- **BEFORE antibiotics** (if possible)
- **2 sets** (aerobic + anaerobic)
- **Volume:** 20-30 mL per set (higher yield)
- **Timing:** Within 1 hour of recognition

**3. Administer Broad-Spectrum Antibiotics:**
- **WITHIN 1 HOUR** of sepsis recognition
- **Empiric coverage** based on suspected source:
  - **Community-acquired pneumonia:** Ceftriaxone 2g IV + azithromycin 500 mg IV/PO
  - **Hospital-acquired pneumonia:** Vancomycin 15 mg/kg IV + cefepime 2g IV q8h
  - **Intra-abdominal:** Ceftriaxone 2g IV + metronidazole 500 mg IV q8h
  - **Urinary:** Ceftriaxone 2g IV (or levofloxacin 500 mg IV)
  - **Unknown source:** Vancomycin + piperacillin-tazobactam 3.375g IV q6h

**4. Begin Fluid Resuscitation:**
- **30 mL/kg** crystalloid bolus (LR or NS)
- **Reassess** after bolus (hemodynamics, lactate, urine output)
- **Repeat** if hypotension persists

**5. Apply Vasopressors (if hypotensive after fluids):**
- **Norepinephrine** (first-line): Start 5-10 mcg/min, titrate to MAP ≥ 65 mmHg
- **Add vasopressin** 0.03 U/min (if norepinephrine dose > 0.25 mcg/kg/min)
- **Consider epinephrine** (if refractory shock)
- **Target MAP:** 65 mmHg (higher if previous hypertension)

**6. Reassess Volume Status:**
- **Repeat bolus** if signs of hypovolemia
- **Avoid fluid overload** (pulmonary edema, tissue edema)
- **Consider:** Dynamic measures (stroke volume variation, passive leg raise)

**Additional Measures:**

**Source Control:**
- **Identify and eliminate** source of infection
- **Intervention:** Drain abscess, remove infected line, surgery (necrotizing fasciitis, perforated viscus)
- **Timing:** Within 6-12 hours of recognition (earlier if possible)

**Corticosteroids:**
- **Consider IV hydrocortisone 200 mg daily** if refractory shock (requiring high-dose norepinephrine)

**Blood Products:**
- **Target Hb:** 7-9 g/dL (transfuse if < 7 g/dL, or < 9 g/dL if myocardial ischemia)
- **Platelets:** < 10,000 (or < 20,000 if bleeding)
- **FFP/Cryoprecipitate:** If coagulopathy + bleeding or planned procedure

**Ventilation:**
- **Low tidal volume** (6 mL/kg predicted body weight) if ARDS
- **Target plateau pressure:** < 30 cm H2O
- **Consider:** Early intubation (if respiratory failure)

**Renal Replacement Therapy:**
- **Indications:** Severe AKI (Stage 3), refractory hyperkalemia, metabolic acidosis, fluid overload

**Antibiotic Stewardship:**
- **De-escalate** once culture results available (48-72 hours)
- **Duration:** 7-10 days for most infections (shorter if rapid response)
- **Discharge:** Consider oral step-down therapy if hemodynamically stable, GI absorption intact

**Sources:** Surviving Sepsis Campaign 2021, NICE NG51, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "infectious_diseases_sepsis",
                "focus": "sepsis_management",
                "sources": ["Surviving Sepsis 2021", "NICE NG51", "BMJ 2024"]
            }
        )

    def _handle_antibiotics(self, query: str, context: dict) -> DomainQueryResult:
        """Handle antibiotic queries"""
        answer = """**Antibiotic Selection and Stewardship**

**Principles of Antibiotic Use:**

**1. Identify the Likely Pathogen:**
- **Anatomic site:** Urine (E. coli), respiratory (S. pneumoniae), skin (S. aureus)
- **Community vs hospital:** Hospital-acquired = resistant organisms (MRSA, Pseudomonas)
- **Host factors:** Immunocompromised, recent antibiotics, recent hospitalization, colonization

**2. Assess Severity:**
- **Mild:** Oral antibiotics, outpatient
- **Moderate:** Oral or IV, consider hospitalization
- **Severe:** IV antibiotics, hospitalization, ICU if unstable

**3. Choose Appropriate Agent:**

**Common Infections - First-line Agents:**

**Community-Acquired Pneumonia (Mild-Moderate):**
- **Amoxicillin** 500 mg TDS (or 1 g TDS if severe) + **macrolide** (azithromycin 500 mg daily, then 250 mg daily)
- **Doxycycline** 100 mg BD (alternative to macrolide)
- **Duration:** 5 days (if improving)

**Complicated UTI (Pyelonephritis):**
- **Ciprofloxacin** 500 mg BD (or 400 mg IV BD) for 7 days
- **Ceftriaxone** 2 g IV daily (if quinolone resistance, severe)
- **Add gentamicin** if severe (IV, dose by renal function)

**Cellulitis:**
- **Flucloxacillin** 500 mg QDS (or 1-2 g IV q6h if severe)
- **Alternative:** Clarithromycin 500 mg BD (if penicillin allergy)
- **Duration:** 5-7 days (extend if not improving)

**Intra-Abdominal Infection:**
- **Ceftriaxone** 2 g IV daily + **metronidazole** 500 mg IV TDS
- **Alternative:** Piperacillin-tazobactam 3.375 g IV q6h
- **Duration:** 4-7 days (source control essential)

**Meningitis (Empiric):**
- **Ceftriaxone** 2 g IV q12h + **vancomycin** 15 mg/kg IV q12h + **dexamethasone** 10 mg IV q6h (before/with antibiotics)
- **Add acyclovir** if HSV suspected (immunocompromised)

**4. Assess for Resistant Organisms:**

**MRSA (Methicillin-Resistant S. aureus):**
- **Risk factors:** Recent hospitalization, recent antibiotics, MRSA colonization, nursing home resident
- **Treatment:** Vancomycin 15 mg/kg IV q12h (trough 15-20 mg/L)
- **Severe skin infection:** Add vancomycin if cellulitis not responding to flucloxacillin

**Pseudomonas:**
- **Risk factors:** Hospitalization > 7 days, prior antibiotics, structural lung disease (bronchiectasis)
- **Treatment:** Piperacillin-tazobactam 3.375 g IV q6h, cefepime 2 g IV q8h, or meropenem 1 g IV q8h

**ESBL (Extended-Spectrum Beta-Lactamase):**
- **Risk factors:** Recent travel, prior ESBL colonization, recent cephalosporin use
- **Treatment:** Avoid cephalosporins, use carbapenem (meropenem) or nitrofurantoin (lower UTI)

**5. Antibiotic Stewardship:**

**De-escalation:**
- **Narrow spectrum** once culture results available
- **Stop** if no evidence of infection (negative cultures, no clinical improvement)
- **Convert IV to PO** (if hemodynamically stable, GI absorption intact)

**Duration:**
- **Uncomplicated infections:** 5-7 days
- **Complicated infections:** 7-14 days
- **Longer if:** Incomplete source control, immunocompromised, slow response

**Avoid:**
- **Treating colonization:** Asymptomatic bacteriuria (unless pregnant, urologic procedure), catheter tip colonization
- **Broad-spectrum** when narrow-spectrum effective
- **Duplicate coverage** (e.g., ceftriaxone + ciprofloxacin)

**6. Dosing in Renal Impairment:**

**Adjust Dose/Interval:**
- **eGFR 30-50:** Reduce dose or extend interval (drug-specific)
- **eGFR 10-30:** Significantly reduce dose or extend interval
- **eGFR < 10:** Avoid nephrotoxic drugs (gentamicin, vancomycin) or use with extreme caution

**Safe in Renal Failure:**
- **Ceftriaxone** (no adjustment needed)
- **Azithromycin**, **doxycycline**
- **Nitrofurantoin** (avoid if eGFR < 30-45)

**Avoid in Renal Failure:**
- **Aminoglycosides** (gentamicin, tobramycin)
- **Vancomycin** (monitor levels, adjust dose)

**7. Common Antibiotic Side Effects:**

**Penicillins:**
- **Rash** (5-10%, can be anaphylaxis if type I hypersensitivity)
- **Diarrhea** (ampicillin > amoxicillin)
- **Interactions:** Oral contraceptives (reduced efficacy)

**Cephalosporins:**
- **Cross-reactivity:** 1-5% with penicillins (higher with 1st generation)
- **Diarrhea** (especially ceftriaxone, cefotaxime - biliary excretion)

**Fluoroquinolones:**
- **Tendon rupture** (elderly, corticosteroids)
- **QT prolongation** (avoid if prolonged QT, electrolyte abnormalities)
- **CNS effects:** Insomnia, seizures (rare)
- **Aortic dissection** (controversial, avoid if high risk)

**Macrolides:**
- **QT prolongation** (avoid if prolonged QT)
- **CYP3A4 inhibition:** Drug interactions (statins, warfarin)

**Aminoglycosides:**
- **Nephrotoxicity** (dose- and duration-dependent)
- **Ototoxicity** (irreversible hearing loss, vertigo)
- **Monitor:** Peak and trough levels, renal function

**Vancomycin:**
- **Nephrotoxicity** (higher risk with concomitant aminoglycosides)
- **Red man syndrome** (histamine-related, infusion-related - slow infusion, premedicate)

**Sources:** NICE NG190, BMJ Best Practice 2024, Sanford Guide 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "infectious_diseases_antibiotics",
                "focus": "antibiotic_stewardship",
                "sources": ["NICE NG190", "BMJ 2024", "Sanford Guide 2024"]
            }
        )

    def _interpret_culture(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret culture results"""
        answer = """**Culture and Sensitivity Interpretation**

**Blood Cultures:**

**Collection:**
- **Volume:** 20-30 mL per set (2 bottles: aerobic + anaerobic)
- **Sets:** 2 sets from 2 different sites (increase yield)
- **Timing:** BEFORE antibiotics (if possible)

**Common Pathogens:**

**Gram-Positive:**
- **Staphylococcus aureus:**
  - **MSSA:** Flucloxacillin, cefazolin
  - **MRSA:** Vancomycin
- **Coagulase-negative staphylococci (CoNS):**
  - **S. epidermidis** (common contaminant, consider if multiple sets positive)
- **Enterococcus:**
  - **E. faecalis:** Amoxicillin ± gentamicin
  - **E. faecium:** Vancomycin (VRE resistance emerging)

**Gram-Negative:**
- **Escherichia coli:**
  - **Community:** Ceftriaxone, ciprofloxacin
  - **Hospital-acquired, ESBL:** Meropenem
- **Klebsiella pneumoniae:**
  - **Community:** Ceftriaxone
  - **Hospital-acquired, ESBL:** Meropenem
- **Pseudomonas aeruginosa:**
  - **Piperacillin-tazobactam**, cefepime, meropenem
- **Proteus mirabilis:**
  - **Ceftriaxone**, ciprofloxacin

**Contaminants vs True Pathogens:**

**Common Contaminants:**
- **CoNS** (Coagulase-negative staphylococci)
- **Corynebacterium**, **Propionibacterium**
- **Viridans streptococci** (unless endocarditis)

**True Pathogens:**
- **S. aureus**, **E. coli**, **Klebsiella**, **Pseudomonas**
- **Multiple sets positive** (same organism)
- **Time to positivity:** < 24 hours (suggests high bacterial load)

**Urine Cultures:**

**Collection:**
- **Midstream clean-catch** (or catheter specimen)
- **Refrigerate** if transport delayed > 2 hours

**Significant Bacteriuria:**
- **≥ 10^5 CFU/mL** (single organism)
- **≥ 10^3 CFU/mL** (if symptomatic + catheter specimen)
- **≥ 10^4 CFU/mL** (if symptomatic + clean-catch)

**Common Pathogens:**
- **E. coli** (80-90%)
- **Klebsiella**, **Proteus**
- **Enterococcus**
- **Pseudomonas** (catheter-associated, recurrent UTI)

**Contaminants:**
- **Lactobacillus**, **Corynebacterium**, **CoNS**
- **Multiple organisms** (unless catheter specimen)

**Sputum Cultures:**

**Collection:**
- **Deep cough** specimen (first morning specimen best)
- **Quality:** < 10 squamous epithelial cells/LPF (good specimen)

**Common Pathogens:**
- **Streptococcus pneumoniae** (community-acquired pneumonia)
- **Haemophilus influenzae**
- **Staphylococcus aureus**
- **Pseudomonas aeruginosa** (hospital-acquired, bronchiectasis)
- **Klebsiella pneumoniae** (aspiration, alcoholism)

**Interpretation:**
- **Quantitative:** ≥ 10^6 CFU/mL (significant)
- **Qualitative:** Presence of pathogen + compatible clinical syndrome

**Wound Cultures:**

**Collection:**
- **Clean wound** (remove surface debris)
- **Swab** or **tissue biopsy** (tissue more accurate)

**Common Pathogens:**
- **S. aureus** (most common)
- **Streptococcus pyogenes** (group A strep)
- **Pseudomonas**, **Enterococcus** (chronic wounds, diabetic foot)

**Interpretation:**
- **Polymicrobial** (mixed flora) common in chronic wounds
- **Clinical correlation** essential (colonization vs infection)

**Antibiotic Sensitivity (AST):**

**Report Format:**
- **S (Sensitive):** Antibiotic achieves reliable concentrations at site of infection
- **I (Intermediate):** Antibiotic may be effective if high dose used (or alternative route)
- **R (Resistant):** Antibiotic unlikely to be effective

**Common Resistance Mechanisms:**

**Beta-Lactamase Production:**
- **Enzyme** that breaks down penicillins
- **Treat:** Beta-lactamase resistant penicillins (flucloxacillin), cephalosporins

**ESBL (Extended-Spectrum Beta-Lactamase):**
- **Enzyme** that breaks down cephalosporins
- **Treatment:** Carbapenems (meropenem), avoid cephalosporins

**MRSA (Methicillin-Resistant S. aureus):**
- **Altered PBPs** (penicillin-binding proteins)
- **Treatment:** Vancomycin, linezolid, clindamycin

**Pseudomonas Resistance:**
- **Efflux pumps**, **porin mutations**
- **Treatment:** Piperacillin-tazobactam, cefepime, meropenem (check sensitivities)

**Culture-Negative Infections:**

**Causes:**
- **Prior antibiotics** (most common)
- **Fastidious organisms** (requiring special culture media)
- **Intracellular pathogens** (Legionella, Mycoplasma)
- **Non-bacterial pathogens** (viruses, fungi)

**Approach:**
- **Repeat cultures** (if possible)
- **Serology** (Legionella, Mycoplasma)
- **PCR** (viral pathogens, atypical bacteria)
- **Empiric treatment** based on clinical presentation

**Sources:** BMJ Best Practice 2024, Sanford Guide 2024, NICE 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "infectious_diseases_laboratory",
                "focus": "culture_interpretation",
                "sources": ["BMJ 2024", "Sanford Guide 2024", "NICE 2024"]
            }
        )

    def _handle_fever(self, query: str, context: dict) -> DomainQueryResult:
        """Handle fever queries"""
        answer = """**Fever of Unknown Origin (FUO) Investigation**

**Definitions:**

**Classic FUO (Petersdorf & Beeson):**
- **Fever ≥ 38.3°C (101°F)** on several occasions
- **Duration ≥ 3 weeks**
- **Uncertain diagnosis** after 3 outpatient visits or 3 days in hospital (or 1 week of intelligent investigation)

**Categories:**
- **Classic FUO** (outpatients)
- **Nosocomial FUO** (hospital-acquired, fever ≥ 38.3°C after 3 days of admission, not present on admission)
- **Neutropenic FUO** (fever ≥ 38.3°C, neutrophils < 500/mm³)
- **HIV-associated FUO** (fever ≥ 38.3°C for > 4 weeks in outpatient or > 3 days in hospital)

**Etiology:**

**Infections (30-40%):**
- **Tuberculosis** (extrapulmonary: miliary, meningeal, renal, bone)
- **Endocarditis** (subacute, culture-negative)
- **Intra-abdominal abscess** (diverticular abscess, subphrenic abscess)
- **Empyema**, **liver abscess**
- **Osteomyelitis** (chronic, low-grade)
- **Cat-scratch disease**, **toxoplasmosis**
- **Epstein-Barr virus**, **CMV** (prolonged fever)

**Malignancies (20-30%):**
- **Lymphoma** (Hodgkin, non-Hodgkin - B symptoms)
- **Leukemia** (acute, chronic)
- **Renal cell carcinoma** (paraneoplastic fever)
- **Hepatocellular carcinoma**
- **Solid tumors** (with metastasis - necrosis, fever)

**Autoimmune/Rheumatologic (10-20%):**
- **Still's disease** (adult-onset)
- **Systemic lupus erythematosus**
- **Rheumatoid arthritis**
- **Polyarteritis nodosa**, **Takayasu arteritis**
- **Giant cell arteritis** (elderly)
- **Inflammatory bowel disease**

**Other (10-20%):**
- **Drug fever** (antibiotics, antiepileptics, allopurinol)
- **Factitious fever** (self-induced, Munchausen's)
- **Hyperthyroidism** (thyrotoxicosis)
- **Dysautonomia** (familial Mediterranean fever)

**Undiagnosed (10-20%):**
- **Self-limited** (resolve without diagnosis)
- **Many resolve spontaneously**

**Evaluation:**

**History:**
- **Travel:** Malaria, dengue, typhoid, tuberculosis
- **Animal exposures:** Pets, occupational (farmers, veterinarians)
- **Medications:** Recent antibiotics, new drugs
- **Comorbidities:** HIV, immunosuppression, prosthetic devices
- **Family history:** Inherited fever syndromes (FMF)

**Physical Examination:**
- **Repeat examinations** (daily if hospitalized)
- **Look for:**
  - **Heart murmur** (endocarditis)
  - **Lymphadenopathy** (lymphoma, TB)
  - **Hepatosplenomegaly** (lymphoma, leukemia, TB)
  - **Skin lesions** (rash, petechiae, Osler nodes, Janeway lesions)
  - **Prosthetic devices** (infected shunts, joints)

**Laboratory:**

**First-line:**
- **CBC with differential** (eosinophilia - drug fever, parasitic)
- **ESR/CRP** (elevated in inflammation, infection, malignancy)
- **Blood cultures** (3 sets, 24 hours apart)
- **Urinalysis + culture**
- **Liver function tests** (elevated in liver involvement, lymphoma)
- **Chest X-ray** (TB, lymphoma, pneumonia)

**Second-line (if first-line negative):**
- **Serology:**
  - **HIV**, **hepatitis B/C**
  - **EBV**, **CMV**
  - **Histoplasma**, **Coccidioides** (if travel/residence endemic)
  - **Brucella**, **leptospira**
- **Tuberculin skin test** or **IGRA** (Quantiferon-TB Gold)
- **Autoimmune markers:** ANA, RF, anti-CCP, ANCA
- **Tumor markers:** LDH (elevated in lymphoma)

**Imaging:**
- **CT chest/abdomen/pelvis** with contrast (lymphadenopathy, abscess, malignancy)
- **Echocardiogram** (TTE ± TEE if endocarditis suspected)
- **PET scan** (if CT negative, fever persists - localizes inflammation/infection)

**Procedures:**
- **Bone marrow biopsy** (if cytopenias, suspected hematologic malignancy)
- **Liver biopsy** (if elevated LFTs, suspected granulomatous disease)
- **Lymph node biopsy** (excisional - if lymphadenopathy)

**Empiric Treatment:**
- **Avoid empiric antibiotics** (unless sepsis or neutropenia)
- **If deteriorating:**
  - **Neutropenic:** Meropenem + vancomycin
  - **Endocarditis suspected:** Vancomycin + gentamicin
  - **TB suspected:** Trial of anti-tuberculous therapy (if high suspicion)

**Prognosis:**
- **Infections:** Good if identified and treated
- **Malignancies:** Variable (depends on type, stage)
- **Autoimmune:** Good with immunosuppression
- **Undiagnosed:** Many resolve spontaneously

**Sources:** NICE DG260, UpToDate 2024, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "infectious_diseases_fever",
                "focus": "fuo_investigation",
                "sources": ["NICE DG260", "UpToDate 2024", "BMJ 2024"]
            }
        )

    def _handle_tropical(self, query: str, context: dict) -> DomainQueryResult:
        """Handle tropical disease queries"""
        answer = """**Tropical Diseases Recognition**

**Malaria:**

**Etiology:**
- **Plasmodium falciparum** (most severe, Africa)
- **P. vivax**, **P. ovale**, **P. malariae**, **P. knowlesi** (less severe)

**Transmission:**
- **Anopheles mosquito** bite (evening to dawn)
- **Endemic:** Sub-Saharan Africa, Southeast Asia, South America

**Clinical Features:**
- **Incubation:** 7-30 days (can be longer with P. vivax, P. ovale - liver hypnozoites)
- **Symptoms:**
  - **Paroxysms:** Fever, chills, rigors (every 48-72 hours depending on species)
  - **Headache**, **myalgia**, **arthralgia**
  - **Anemia**, **jaundice** (hemolysis)
  - **Splenomegaly**
- **Severe malaria (P. falciparum):**
  - **Cerebral malaria** (coma, seizures)
  - **Severe anemia** (Hb < 5 g/dL)
  - **Renal failure**, **ARDS**, **DIC**
  - **Hypoglycemia**

**Diagnosis:**
- **Blood smear:** Gold standard (thick and thin smear)
  - **Thick smear:** Detects parasites (sensitive)
  - **Thin smear:** Identifies species (specific)
- **Rapid diagnostic test (RDT):** Antigen detection (HRP2, aldolase)
- **PCR:** If smear negative but high suspicion

**Treatment:**

**Uncomplicated Malaria:**
- **P. falciparum (uncomplicated):**
  - **Artemisinin-based combination therapy (ACT):**
    - **Artemether-lumefantrine** (Coartem) 6-dose regimen
    - **Atovaquone-proguanil** (Malarone) 4 tablets daily × 3 days
- **P. vivax, P. ovale:**
  - **Chloroquine** (if chloroquine-sensitive) + **primaquine** (radical cure of liver hypnozoites)

**Severe Malaria:**
- **IV artesunate** (2.4 mg/kg at 0, 12, 24 hours, then daily)
- **Switch to oral ACT** once able to tolerate oral medications

**Prophylaxis:**
- **Atovaquone-proguanil** (Malarone) - 1 tablet daily (start before travel, continue 1 week after)
- **Doxycycline** - 100 mg daily (start before travel, continue 4 weeks after)
- **Mefloquine** - 250 mg weekly (start before travel, continue 4 weeks after)

---

**Dengue Fever:**

**Etiology:**
- **Flavivirus** (4 serotypes: DENV-1, -2, -3, -4)
- **Transmission:** Aedes mosquito (day-biting)

**Clinical Features:**
- **Incubation:** 3-14 days
- **Phases:**
  - **Febrile phase:** High fever, headache, myalgia ("breakbone fever"), retro-orbital pain, rash
  - **Critical phase (days 3-7):** Plasma leakage, shock, organ dysfunction
  - **Recovery phase:** Reabsorption of fluid, resolution of symptoms

**Warning Signs (Severe Dengue):**
- **Abdominal pain**, **persistent vomiting**
- **Clinical fluid accumulation** (ascites, pleural effusion)
- **Mucosal bleed**, **lethargy**, **restlessness**
- **Liver enlargement** (> 2 cm)
- **Rising hematocrit** with falling platelet count

**Diagnosis:**
- **NS1 antigen** (days 1-5)
- **IgM/IgG serology** (after day 5)
- **PCR** (early infection, serotype identification)

**Treatment:**
- **Supportive care** (no specific antiviral)
- **Fluid management:** Crystalloids (LR or NS), avoid over-resuscitation (critical phase)
- **Avoid:** Aspirin, NSAIDs (bleeding risk) - use acetaminophen
- **Monitor:** Hematocrit, platelet count (daily in critical phase)

---

**Zika Virus:**

**Etiology:**
- **Flavivirus** (similar to dengue)
- **Transmission:** Aedes mosquito, sexual transmission, congenital

**Clinical Features:**
- **Mild:** Fever, rash, arthralgia, conjunctivitis
- **Severe:** **Guillain-Barré syndrome**, **Congenital Zika syndrome** (microcephaly)

**Diagnosis:**
- **RT-PCR** (urine, serum - days 0-14)
- **Serology:** IgM (after day 4)

**Treatment:**
- **Supportive care**
- **Avoid:** Pregnancy (if infected or traveled to endemic area)
- **Prevention:** Mosquito avoidance, condom use (if pregnant or planning pregnancy)

---

**Chikungunya:**

**Etiology:**
- **Alphavirus** (Togaviridae family)
- **Transmission:** Aedes mosquito

**Clinical Features:**
- **Acute:** Fever, severe arthralgia (joint pain), myalgia, headache, rash
- **Chronic:** Persistent arthralgia (months to years)

**Diagnosis:**
- **RT-PCR** (days 0-7)
- **Serology:** IgM (after day 5)

**Treatment:**
- **Supportive care**
- **NSAIDs** (for joint pain - after acute phase)
- **Chronic:** Physical therapy, NSAIDs, DMARDs (refractory cases)

---

**Yellow Fever:**

**Etiology:**
- **Flavivirus**
- **Transmission:** Aedes, Haemagogus mosquitoes (jungle cycle)

**Clinical Features:**
- **Mild:** Fever, chills, myalgia, headache, nausea
- **Severe:** Hepatitis, jaundice, hemorrhage, shock, multiorgan failure
- **Case fatality:** 20-50% (severe disease)

**Diagnosis:**
- **RT-PCR** (days 0-10)
- **Serology:** IgM (after day 4)
- **Liver biopsy:** Post-mortem (yellow fever necrosis)

**Treatment:**
- **Supportive care** (no specific antiviral)
- **Prevention:** **Yellow fever vaccine** (live attenuated, single dose, lifelong immunity)

---

**Ebola Virus Disease:**

**Etiology:**
- **Filovirus**
- **Transmission:** Direct contact with bodily fluids (blood, vomit, feces), fomites

**Clinical Features:**
- **Incubation:** 2-21 days (average 8-10 days)
- **Symptoms:** Fever, headache, myalgia, vomiting, diarrhea
- **Severe:** Hemorrhage (bleeding from gums, nose, eyes), shock, multiorgan failure
- **Case fatality:** 25-90% (average 50%)

**Diagnosis:**
- **RT-PCR** (blood, bodily fluids)
- **Antigen detection** (ELISA)
- **Serology:** IgM/IgG (after day 6-10)

**Treatment:**
- **Supportive care** (aggressive fluid resuscitation, electrolyte replacement)
- **Specific:** **Inmazeb** (atoltivimab, maftivimab, odesivimab), **Ebanga** (ansuvimab) - monoclonal antibodies

---

**Tuberculosis (TB):**

**Etiology:**
- **Mycobacterium tuberculosis**
- **Transmission:** Airborne (droplet nuclei)

**Clinical Features:**
- **Pulmonary TB (most common):**
  - **Chronic cough** (> 2-3 weeks)
  - **Hemoptysis**, **weight loss**, **night sweats**
  - **Fever**, **fatigue**
- **Extrapulmonary TB:**
  - **Lymphadenitis** (scrofula)
  - **Pleural effusion**, **pericarditis**
  - **Meningitis**, **Pott's disease** (spine)

**Diagnosis:**
- **Sputum:** AFB stain (Ziehl-Neelsen), culture (gold standard, 4-8 weeks)
- **Chest X-ray:** Apical cavitation, infiltrates, pleural effusion
- **Tuberculin skin test (TST)** or **IGRA** (Quantiferon-TB Gold)
- **NAAT** (GeneXpert) - rapid diagnosis, rifampin resistance

**Treatment:**

**Drug-Sensitive TB:**
- **2HRZE/4HR regimen:**
  - **Intensive phase (2 months):** Isoniazid + Rifampin + Pyrazinamide + Ethambutol
  - **Continuation phase (4 months):** Isoniazid + Rifampin
- **DOTS** (directly observed therapy, short-course)

**MDR-TB (Multidrug-Resistant TB):**
- **Resistant to:** Isoniazid + Rifampin
- **Treatment:** 5-7 drugs for 9-20 months (fluoroquinolone, injectable agent, etc.)

**Latent TB Infection (LTBI):**
- **Isoniazid** 300 mg daily for 6-9 months
- **Rifampin** 600 mg daily for 4 months
- **Isoniazid + Rifapentine** weekly for 3 months

**Sources:** CDC Yellow Book 2024, WHO Guidelines 2024, NICE NG33"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "infectious_diseases_tropical",
                "focus": "tropical_diseases",
                "sources": ["CDC 2024", "WHO 2024", "NICE NG33"]
            }
        )

    def _handle_hiv(self, query: str, context: dict) -> DomainQueryResult:
        """Handle HIV queries"""
        answer = """**HIV and AIDS Management**

**Definitions:**

**HIV Infection:**
- **Acute HIV:** 2-4 weeks after infection (fever, rash, pharyngitis, lymphadenopathy)
- **Chronic HIV:** Asymptomatic for years (CD4 gradually declines)
- **AIDS (Acquired Immunodeficiency Syndrome):** CD4 < 200 cells/mm³ or AIDS-defining illness

**Diagnosis:**

**Testing:**
- **HIV-1/2 antigen/antibody combination immunoassay (4th generation):**
  - **Detects:** HIV-1/2 antibodies + p24 antigen (early infection)
  - **Window period:** 18-45 days (p24 antigen detectable earlier)
- **Confirmatory:** HIV-1/HIV-2 differentiation immunoassay
- **NAT (RNA PCR):** If acute HIV suspected (negative serology, high risk)

**CD4 Count:**
- **Normal:** 500-1500 cells/mm³
- **Mild immunosuppression:** 350-499 cells/mm³
- **Advanced immunosuppression:** 200-349 cells/mm³
- **Severe immunosuppression:** < 200 cells/mm³ (AIDS-defining)

**Viral Load (HIV RNA):**
- **Goal:** < 50 copies/mL (undetectable)
- **Monitoring:** Every 3-6 months (once on ART)
- **Failure:** > 200 copies/mL on 2 consecutive tests

**Antiretroviral Therapy (ART):**

**Indications:**
- **ALL HIV-infected individuals** (regardless of CD4 count)
- **Pregnant women** (prevent mother-to-child transmission)
- **HIV-2 infection** (different regimen)

**First-line Regimens:**

**Integrase Strand Transfer Inhibitor (INSTI) + 2 NRTIs:**
- **Bictegravir/Tenofovir alafenamide/Emtricitabine (BIC/TAF/FTC):**
  - **Biktarvy:** 1 tablet daily
  - **Advantages:** High barrier to resistance, well tolerated
- **Dolutegravir + Tenofovir/Emtricitabine (DTG + TDF/FTC):**
  - **Triumeq:** 1 tablet daily
  - **Advantages:** High potency, well tolerated, minimal drug interactions

**Alternative Regimens:**
- **Protease inhibitor + 2 NRTIs:** Darunavir/ritonavir + TDF/FTC
- **NNRTI + 2 NRTIs:** Efavirenz/TDF/FTC (Atripla) - less preferred due to CNS side effects

**Monitoring:**
- **Baseline:** CD4, viral load, resistance testing (if ART-experienced), HLA-B*5701 (if abacavir considered)
- **Follow-up:** Viral load at 4-8 weeks, then every 3-6 months
- **CD4:** Every 3-6 months (until > 350 cells/mm³, then every 6-12 months)
- **Toxicity monitoring:** Renal function (TDF), bone density (TDF), lipids (PIs)

**AIDS-Defining Illnesses:**

**Opportunistic Infections:**

**Pneumocystis jirovecii Pneumonia (PJP):**
- **CD4 < 200 cells/mm³**
- **Symptoms:** Fever, dry cough, dyspnea, hypoxia
- **Diagnosis:** Sputum stain (PJP), beta-D-glucan
- **Treatment:** Trimethoprim-sulfamethoxazole (TMP-SMX) IV/PO
- **Prophylaxis:** TMP-SMX 1 DS tablet daily (if CD4 < 200)

**Toxoplasma gondii Encephalitis:**
- **CD4 < 100 cells/mm³**, Toxoplasma IgG positive
- **Symptoms:** Headache, focal neurologic deficits, seizures
- **Diagnosis:** MRI brain (ring-enhancing lesions), Toxoplasma serology
- **Treatment:** Pyrimethamine + sulfadiazine + folinic acid
- **Prophylaxis:** TMP-SMX (if CD4 < 100, Toxoplasma IgG positive)

**Mycobacterium avium Complex (MAC):**
- **CD4 < 50 cells/mm³**
- **Symptoms:** Fever, weight loss, night sweats, diarrhea
- **Diagnosis:** Blood culture, bone marrow culture
- **Treatment:** Azithromycin + ethambutol ± rifabutin
- **Prophylaxis:** Azithromycin 1,200 mg weekly (if CD4 < 50)

**CMV (Cytomegalovirus):**
- **CD4 < 50 cells/mm³**
- **Retinitis:** Blurred vision, floaters, vision loss (fundoscopy: retinal hemorrhages, exudates)
- **Colitis:** Diarrhea, abdominal pain, weight loss
- **Treatment:** Ganciclovir or valganciclovir (IV then PO)
- **Prophylaxis:** Not routinely recommended ( preemptive therapy with CMV PCR monitoring)

**Cryptococcal Meningitis:**
- **CD4 < 100 cells/mm³**
- **Symptoms:** Headache, fever, neck stiffness, altered mental status
- **Diagnosis:** CSF cryptococcal antigen, India ink stain, culture
- **Treatment:** Amphotericin B + flucytosine (2 weeks), then fluconazole (8 weeks), then fluconazole maintenance
- **Screening:** Cryptococcal antigen (if CD4 < 100)

**Tuberculosis:**
- **Increased risk** if CD4 < 350 cells/mm³
- **Disseminated TB** (extrapulmonary) more common
- **Treatment:** Standard RIPE therapy (avoid rifampin in severe immunosuppression - use rifabutin)
- **IRIS (Immune Reconstitution Inflammatory Syndrome):** Worsening symptoms after ART initiation (due to immune recovery)

**Prevention:**

**Pre-Exposure Prophylaxis (PrEP):**
- **Tenofovir disoproxil fumarate/emtricitabine (TDF/FTC):** 1 tablet daily
- **Indications:** Men who have sex with men (MSM), heterosexuals with high-risk partners, people who inject drugs (PWID)
- **Efficacy:** 90-99% reduction in HIV acquisition (if adherent)

**Post-Exposure Prophylaxis (PEP):**
- **Indication:** Within 72 hours of high-risk exposure (unprotected sex, needle stick injury)
- **Regimen:** TDF/FTC + dolutegravir (or raltegravir) for 28 days
- **Testing:** HIV baseline, 4-6 weeks, 3 months, 6 months

**Prevention of Mother-to-Child Transmission:**
- **ART for ALL pregnant women** (regardless of CD4/viral load)
- **Deliver by C-section** if viral load > 1,000 copies/mL near delivery
- **Avoid breastfeeding** (if safe alternative feeding available)
- **Infant prophylaxis:** Zidovudine (AZT) for 6 weeks (if maternal viral load suppressed)

**Sources:** BHIVA Guidelines 2024, WHO 2023, NICE NG150"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "infectious_diseases_hiv",
                "focus": "hiv_management",
                "sources": ["BHIVA 2024", "WHO 2023", "NICE NG150"]
            }
        )

    def _handle_hepatitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle hepatitis queries"""
        answer = """**Viral Hepatitis Management**

**Hepatitis B (HBV):**

**Etiology:**
- **DNA virus** (Hepadnaviridae family)
- **Transmission:** Blood, sexual, perinatal

**Natural History:**
- **Acute infection:** 70% asymptomatic, 30% symptomatic (jaundice, fatigue)
- **Chronic infection:** 90% if neonatal, 5-10% if adult
- **Complications:** Cirrhosis, hepatocellular carcinoma (HCC)

**Serology:**

| Marker | Interpretation |
|--------|---------------|
| **HBsAg** | Current infection (acute or chronic) |
| **Anti-HBc** | Past or current infection |
| **Anti-HBs** | Immunity (vaccination or past infection) |
| **HBeAg** | High infectivity, active replication |
| **HBV DNA** | Viral load (treatment monitoring) |

**Diagnosis:**
- **Chronic infection:** HBsAg positive for > 6 months
- **Active replication:** HBeAg positive, HBV DNA > 2,000 IU/mL (HBeAg-negative) or > 20,000 IU/mL (HBeAg-positive)

**Treatment Indications (Chronic HBV):**
- **HBV DNA > 2,000 IU/mL** (HBeAg-negative) or > 20,000 IU/mL (HBeAg-positive)
- **ALT elevated**, significant fibrosis (F3/F4)
- **Decompensated cirrhosis** (treat regardless of viral load)

**Treatment:**
- **First-line:**
  - **Entecavir** 0.5 mg daily (or 1 mg if lamivudine-experienced)
  - **Tenofovir TAF** 25 mg daily (or TDF 300 mg daily)
- **Duration:** Long-term (usually lifelong)
- **Monitoring:** ALT, HBV DNA every 3-6 months

**Prevention:**
- **HBV vaccine** (universal vaccination, 3 doses)
- **Post-exposure prophylaxis:** HBV vaccine + HBIG (if not vaccinated)

---

**Hepatitis C (HCV):**

**Etiology:**
- **RNA virus** (Flaviviridae family)
- **Transmission:** Blood (IVDU, blood transfusion before 1992, tattoos)

**Genotypes:**
- **1-6** (genotype 1 most common in UK/US)
- **Important for treatment selection**

**Chronic Infection:**
- **80%** (acute rarely symptomatic)
- **Complications:** Cirrhosis, HCC (20-30% develop cirrhosis over 20-30 years)

**Diagnosis:**
- **HCV antibody** (screening test)
- **HCV RNA** (confirmatory, if antibody positive)
- **Genotyping** (if treatment planned)
- **Fibrosis staging:** Transient elastography (FibroScan), liver biopsy

**Treatment:**
- **All chronic HCV** (treat all, regardless of fibrosis)
- **Direct-acting antivirals (DAAs):**
  - **Sofosbuvir/velpatasvir (Epclusa):** 400/100 mg daily for 12 weeks (pan-genotypic)
  - **Glecaprevir/pibrentasvir (Mavyret):** 3 tablets daily for 8-12 weeks (pan-genotypic)
- **Cure rate (SVR12):** > 95%
- **Monitoring:** HCV RNA at 12 weeks post-treatment (SVR12 = cure)

**Prevention:**
- **No vaccine** (unlike HBV)
- **Harm reduction:** Clean needles, safe sex, safe tattoo practices

---

**Hepatitis A (HAV):**

**Etiology:**
- **RNA virus** (Picornaviridae family)
- **Transmission:** Fecal-oral (contaminated food/water)

**Clinical Features:**
- **Acute hepatitis:** Fever, jaundice, fatigue, nausea
- **Never chronic**, fulminant hepatitis rare

**Diagnosis:**
- **IgM anti-HAV** (acute infection)
- **IgG anti-HAV** (past infection, immunity)

**Treatment:**
- **Supportive care** (no specific therapy)
- **Prevention:** HAV vaccine (high-risk groups), hand hygiene

---

**Hepatitis D (HDV):**

**Etiology:**
- **Defective virus** (requires HBV coinfection)
- **Transmission:** Blood, sexual

**Clinical Features:**
- **Co-infection:** HBV + HDV (acute)
- **Superinfection:** Chronic HBV + HDV (more severe)

**Diagnosis:**
- **Anti-HDV** (screening)
- **HDV RNA** (confirmatory)

**Treatment:**
- **Pegylated interferon** (cure rate ~ 30%)
- **Bulevirtide** (new, not widely available)

---

**Hepatitis E (HEV):**

**Etiology:**
- **RNA virus** (Hepeviridae family)
- **Transmission:** Fecal-oral (undercooked pork, deer meat)

**Clinical Features:**
- **Acute, self-limited** (except in pregnancy, immunocompromised)
- **Fulminant hepatitis** in pregnancy (20% mortality)

**Diagnosis:**
- **IgM anti-HEV** (acute)
- **HEV RNA** (confirmatory)

**Treatment:**
- **Supportive care**
- **Ribavirin** (if chronic infection in immunocompromised)

**Sources:** NICE CG165, AASLD 2023, EASL 2023"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "infectious_diseases_hepatitis",
                "focus": "viral_hepatitis",
                "sources": ["NICE CG165", "AASLD 2023", "EASL 2023"]
            }
        )

    def _handle_covid(self, query: str, context: dict) -> DomainQueryResult:
        """Handle COVID-19 queries"""
        answer = """**COVID-19 Management**

**Etiology:**
- **SARS-CoV-2** (coronavirus)
- **Transmission:** Respiratory droplets, aerosols, fomites

**Clinical Features:**

**Asymptomatic:**
- **No symptoms** (but can transmit)

**Mild Disease (80%):**
- **Fever**, **cough**, **fatigue**
- **Anosmia** (loss of smell), **ageusia** (loss of taste)
- **Sore throat**, **headache**, **myalgia**

**Severe Disease (15-20%):**
- **Dyspnea**, **hypoxia** (SpO2 < 94%)
- **Pneumonia** (bilateral infiltrates on CXR)
- **Hospitalization** required

**Critical Disease (5%):**
- **Respiratory failure** (requiring mechanical ventilation)
- **Shock**, **multiorgan failure**
- **ICU admission**

**Diagnosis:**

**Testing:**
- **RT-PCR** (nasopharyngeal swab) - gold standard
- **Rapid antigen test** (less sensitive, rapid)
- **Serology:** Antibody testing (past infection, not for acute diagnosis)

**Imaging:**
- **Chest X-ray:** Bilateral peripheral infiltrates ("ground glass opacities")
- **CT chest:** More sensitive, ground glass opacities (not routinely needed)

**Laboratory:**
- **Lymphopenia** (low lymphocyte count)
- **Elevated CRP**, **ferritin**, **LDH** (inflammatory markers)
- **Elevated D-dimer** (coagulopathy)

**Treatment:**

**Mild Disease (Outpatient):**
- **Supportive care:** Rest, hydration, antipyretics
- **Monitor for worsening:** Shortness of breath, persistent fever > 1 week
- **Isolation:** 10 days from symptom onset (or 10 days from positive test if asymptomatic)

**Severe Disease (Hospitalized):**

**Antiviral Therapy (within 5-7 days of symptom onset):**
- **Remdesivir:** 200 mg IV day 1, then 100 mg IV daily for 4 days (total 5 days)
- **Nirmatrelvir/ritonavir (Paxlovid):** 300/100 mg PO BID for 5 days (mild-moderate disease, high-risk outpatient)

**Immunomodulators (for severe disease requiring oxygen):**
- **Dexamethasone:** 6 mg daily IV/PO for 10 days (or until discharge)
- **Tocilizumab:** 8 mg/kg IV (max 800 mg) × 1-2 doses (if rapidly worsening, requiring high-flow oxygen or mechanical ventilation)

**Anticoagulation:**
- **Prophylactic:** Enoxaparin 40 mg SC daily (or therapeutic dose if D-dimer significantly elevated)

**Supportive Care:**
- **Oxygen:** Target SpO2 92-96% (88-92% if at risk of hypercapnia)
- **Fluid:** Conservative (avoid fluid overload)
- **High-flow nasal cannula** (if hypoxemic respiratory failure)
- **Mechanical ventilation:** Low tidal volume (6 mL/kg), plateau pressure < 30 cm H2O (if ARDS)

**Post-COVID Syndrome (Long COVID):**

**Symptoms:**
- **Fatigue**, **brain fog**, **shortness of breath**
- **Chest pain**, **palpitations**, **joint pain**
- **Depression**, **anxiety**, **sleep disturbance**

**Management:**
- **Multidisciplinary rehabilitation**
- **Gradual return to activity**
- **Treat specific symptoms** (e.g., inhalers for breathlessness, CBT for anxiety)

**Prevention:**

**Vaccination:**
- **mRNA vaccines:** Pfizer-BioNTech (BNT162b2), Moderna (mRNA-1273)
- **Viral vector vaccine:** Oxford-AstraZeneca (ChAdOx1)
- **Booster doses:** Every 6-12 months (variants, waning immunity)

**Non-Pharmaceutical Interventions:**
- **Face masks** (surgical, N95/FFP2)
- **Social distancing** (2 meters/6 feet)
- **Hand hygiene** (wash hands, sanitizer)
- **Ventilation** (open windows, air filtration)

**Sources:** NICE NG188, NIH Guidelines 2024, WHO 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "infectious_diseases_covid",
                "focus": "covid19_management",
                "sources": ["NICE NG188", "NIH 2024", "WHO 2024"]
            }
        )

    def _handle_influenza(self, query: str, context: dict) -> DomainQueryResult:
        """Handle influenza queries"""
        answer = """**Influenza Management**

**Etiology:**
- **Orthomyxovirus** (Influenza A, B, C, D)
- **Types:** Influenza A (more severe, pandemics), Influenza B (seasonal)
- **Transmission:** Respiratory droplets, aerosols, fomites

**Clinical Features:**

**Typical Influenza:**
- **Sudden onset** (unlike common cold)
- **Fever** (> 38°C), **chills**, **rigors**
- **Myalgia**, **arthralgia**, **headache**
- **Dry cough**, **sore throat**, **fatigue**
- **Duration:** 5-7 days (fatigue may persist for weeks)

**Complications:**
- **Pneumonia** (primary viral, secondary bacterial)
- **Exacerbation of underlying disease** (COPD, heart failure)
- **Myositis**, **rhabdomyolysis** (children)
- **Encephalitis**, **seizures** (children)
- **Death** (elderly, comorbidities, pregnancy)

**Diagnosis:**

**Testing:**
- **Rapid influenza diagnostic test (RIDT):** Antigen detection (bedside, result in 15 minutes, sensitivity 50-70%)
- **RT-PCR:** Gold standard (sent to lab, result in hours-days, sensitivity > 95%)
- **Viral culture** (not routine, surveillance)

**Indications for Testing:**
- **Hospitalized** with respiratory illness
- **High-risk** patients (elderly, comorbidities, pregnancy)
- **Outbreak** investigation (nursing homes, schools)

**Treatment:**

**Antiviral Therapy (within 48 hours of symptom onset):**

**Oseltamivir (Tamiflu):**
- **75 mg PO BID** for 5 days
- **Indications:**
  - **Severe influenza** (hospitalized)
  - **High-risk patients:** Age > 65, comorbidities, pregnancy, immunocompromised
  - **Early treatment** (< 48 hours) shortens duration by 1-2 days, reduces complications
- **Side effects:** Nausea, vomiting (take with food)

**Baloxavir marboxil (Xofluza):**
- **Single dose:** 40 mg PO (< 80 kg), 80 mg PO (≥ 80 kg)
- **Mechanism:** Inhibits endonuclease (cap-dependent endonuclease inhibitor)
- **Indications:** Mild illness in low-risk patients (not approved for high-risk or hospitalized)

**Supportive Care:**
- **Antipyretics:** Acetaminophen, NSAIDs (fever, myalgia)
- **Hydration:** Adequate fluids
- **Rest:** Avoid strenuous activity

**Treatment of Complications:**

**Secondary Bacterial Pneumonia:**
- **S. pneumoniae**, **S. aureus** (most common)
- **Antibiotics:** Amoxicillin-clavulanate, or ceftriaxone + azithromycin (if hospitalized)

**Exacerbation of Underlying Disease:**
- **COPD:** Oral steroids, antibiotics, bronchodilators
- **Heart failure:** Diuretics, oxygen

**Prevention:**

**Vaccination:**

**Inactivated Influenza Vaccine (IIV):**
- **Quadrivalent:** 2 influenza A strains (H1N1, H3N2) + 2 influenza B strains
- **Dose:** 0.5 mL IM (single dose)
- **Timing:** Annually (before flu season - September/October)
- **Indications:** **ALL** ≥ 6 months (universal recommendation)

**Live Attenuated Influenza Vaccine (LAIV):**
- **Nasal spray** (intranasal)
- **Indications:** Healthy children 2-17 years (some countries)

**Contraindications:**
- **Severe egg allergy** (anaphylaxis) - consider egg-free vaccine or supervised administration
- **Guillain-Barré syndrome** within 6 weeks of previous influenza vaccine
- **Age < 6 months**

**High-Risk Groups (Prioritize Vaccination):**
- **Age ≥ 65** (high mortality)
- **Comorbidities:** COPD, heart disease, diabetes, immunocompromised
- **Pregnancy** (all trimesters)
- **Healthcare workers** (protect patients)
- **Residents** of nursing homes

**Antiviral Prophylaxis:**
- **Oseltamivir 75 mg PO daily** for 10 days (or until 7 days after last case in outbreak)
- **Indications:**
  - **Outbreaks** (nursing homes, hospitals)
  - **High-risk** unvaccinated individuals after exposure
  - **Immunocompromised** post-exposure

**Non-Pharmaceutical Interventions:**
- **Face masks**, **hand hygiene**, **social distancing**
- **Isolation:** Stay home until fever-free for 24 hours (without antipyretics)

**Sources:** NICE NG158, CDC 2024, WHO 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "infectious_diseases_influenza",
                "focus": "influenza_management",
                "sources": ["NICE NG158", "CDC 2024", "WHO 2024"]
            }
        )

    def _handle_meningitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle meningitis queries"""
        answer = """**Meningitis Management**

**Etiology:**

**Bacterial Meningitis:**
- **Streptococcus pneumoniae** (most common, all ages)
- **Neisseria meningitidis** (adolescents, young adults, epidemics)
- **Listeria monocytogenes** (elderly, immunocompromised, neonates)
- **Haemophilus influenzae type b** (children - now rare due to vaccination)

**Viral Meningitis:**
- **Enteroviruses** (most common, summer/fall)
- **Herpes simplex virus (HSV)** (HSV-2 meningitis, Mollaret's meningitis)
- **West Nile virus**, **Zika virus**, **CMV**, **EBV**

**Fungal Meningitis:**
- **Cryptococcus neoformans** (HIV/AIDS, immunocompromised)
- **Coccidioides**, **Histoplasma** (endemic areas)

**Clinical Features:**

**Classic Triad (not always present):**
1. **Fever**
2. **Headache**
3. **Nuchal rigidity** (neck stiffness)

**Other Symptoms:**
- **Photophobia** (light sensitivity)
- **Altered mental status** (confusion, lethargy, coma)
- **Seizures**, **focal neurologic deficits**
- **Petechial rash** (meningococcemia - medical emergency)

**Diagnostic Evaluation:**

**Blood Tests:**
- **CBC with differential** (elevated WBC, left shift)
- **CRP/ESR** (elevated)
- **Blood cultures** (2 sets, BEFORE antibiotics)
- **Serum glucose** (compare to CSF glucose)

**Lumbar Puncture (LP):**

**Opening Pressure:**
- **Normal:** 6-25 cm H2O
- **Elevated:** > 25 cm H2O (bacterial, fungal)

**CSF Analysis:**

| Parameter | Normal | Bacterial | Viral | Fungal | TB |
|-----------|--------|----------|-------|--------|-----|
| **Appearance** | Clear | Turbid | Clear | Clear | Clear |
| **WBC** | 0-5 | ↑↑ (1,000-10,000) | ↑ (10-300) | ↑ (10-500) | ↑ (50-500) |
| **Predominant** | Mononuclear | Neutrophils | Lymphocytes | Lymphocytes | Lymphocytes |
| **Glucose** | 2/3 serum | ↓↓ (< 40% serum) | Normal | ↓↓ | ↓ |
| **Protein** | 0.15-0.45 g/L | ↑↑ (> 1 g/L) | ↑ (0.5-1 g/L) | ↑↑ | ↑↑ |
| **Gram stain** | Negative | Positive (50%) | Negative | Negative | Negative |
| **Culture** | Negative | Positive | Negative | Positive (slow) | Positive (slow) |

**Specific CSF Tests:**
- **Cryptococcal antigen** (cryptococcal meningitis)
- **VDRL** (syphilitic meningitis)
- **PCR** (HSV, VZV, enterovirus, West Nile virus)
- **AFB stain/culture** (TB meningitis)

**Imaging:**
- **CT head** BEFORE LP if:
  - **Focal neurologic deficits**
  - **Papilledema** (increased ICP)
  - **Altered mental status** (GCS < 12)
  - **Immunocompromised**

**Treatment:**

**Empiric Therapy (START IMMEDIATELY - DO NOT DELAY FOR LP IF CT NEEDED):**

**Age < 50, Immunocompetent:**
- **Ceftriaxone** 2 g IV q12h (covers S. pneumoniae, N. meningitidis)
- **Vancomycin** 15 mg/kg IV q12h (if penicillin-resistant S. pneumoniae suspected)
- **Dexamethasone** 10 mg IV q6h (BEFORE or WITH first dose of antibiotics - reduces hearing loss, mortality)

**Age > 50 or Immunocompromised:**
- **Ceftriaxone** 2 g IV q12h
- **Vancomycin** 15 mg/kg IV q12h
- **Ampicillin** 2 g IV q4h (covers Listeria)
- **Dexamethasone** 10 mg IV q6h

**Pathogen-Directed Therapy:**

**S. pneumoniae:**
- **Penicillin-susceptible:** Penicillin G 4 million units IV q4h
- **Penicillin-resistant:** Ceftriaxone or vancomycin

**N. meningitidis:**
- **Ceftriaxone** 2 g IV q12h (or penicillin G if susceptible)
- **Prophylaxis:** Rifampin 600 mg BID × 2 days (or ciprofloxacin 500 mg single dose) for close contacts

**L. monocytogenes:**
- **Ampicillin** 2 g IV q4h ± **gentamicin** 1 mg/kg IV q8h

**HSV Meningitis/Encephalitis:**
- **Acyclovir** 10 mg/kg IV q8h (for 14-21 days)

**Cryptococcal Meningitis:**
- **Amphotericin B** 0.7 mg/kg IV daily + **flucytosine** 100 mg/kg/day PO divided q6h (2 weeks)
- **Then:** Fluconazole 400 mg daily (8 weeks), then 200 mg daily (maintenance)

**TB Meningitis:**
- **RIPE therapy:** Rifampin, Isoniazid, Pyrazinamide, Ethambutol (2 months)
- **Then:** Rifampin + Isoniazid (7-10 months)

**Dexamethasone:**
- **Indications:** Suspected or proven pneumococcal meningitis
- **Dose:** 10 mg IV q6h for 4 days (or before/with antibiotics)
- **Mechanism:** Reduces hearing loss, neurological sequelae, mortality

**Supportive Care:**
- **ICU admission** (if altered mental status, seizures)
- **Seizure prophylaxis:** Levetiracetam (if structural brain injury on imaging)
- **ICP monitoring** (if cerebral edema)
- **Fluid management:** Isotonic fluids (avoid hypotonic fluids - worsen cerebral edema)

**Prevention:**

**Vaccination:**
- **Hib vaccine:** Part of routine childhood vaccination (H. influenzae type b)
- **Pneumococcal vaccine:** PCV13 (children), PPSV23 (adults > 65, high-risk)
- **Meningococcal vaccine:** MCV4 (adolescents, high-risk), MPSV4 (outbreaks)
- **Travel vaccine:** Meningococcal (if traveling to meningitis belt - sub-Saharan Africa)

**Prophylaxis:**
- **Close contacts** of meningococcal meningitis: Rifampin, ciprofloxacin, or ceftriaxone
- **Household contacts** of Hib meningitis: Rifampin (if unvaccinated < 4 years old)

**Sources:** NICE CG102, BMJ Best Practice 2024, IDSA 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "infectious_diseases_cns",
                "focus": "meningitis_management",
                "sources": ["NICE CG102", "BMJ 2024", "IDSA 2024"]
            }
        )

    def _handle_uti(self, query: str, context: dict) -> DomainQueryResult:
        """Handle UTI queries"""
        answer = """**Urinary Tract Infection (UTI) Management**

**Classification:**

**Anatomic:**
- **Lower UTI:** Cystitis (bladder infection)
- **Upper UTI:** Pyelonephritis (kidney infection)

**Complicated vs Uncomplicated:**
- **Uncomplicated:** Normal urinary tract, no comorbidities, not pregnant
- **Complicated:** Pregnancy, male, catheter, obstruction, stones, diabetes, immunocompromised, recent antibiotics, hospital-acquired

**Etiology:**

**Common Pathogens:**
- **E. coli** (80-90%)
- **Klebsiella pneumoniae**
- **Proteus mirabilis**
- **Enterococcus faecalis**
- **Staphylococcus saprophyticus** (young women)
- **Pseudomonas aeruginosa** (catheter-associated, recurrent UTI)

**Clinical Features:**

**Cystitis (Lower UTI):**
- **Dysuria** (painful urination)
- **Urinary frequency**, **urgency**
- **Suprapubic pain**, **hematuria**
- **NO fever**, **NO systemic symptoms**

**Pyelonephritis (Upper UTI):**
- **Fever**, **chills**, **rigors**
- **Flank pain**, **costovertebral angle tenderness**
- **Systemic symptoms:** Nausea, vomiting, malaise
- **May have dysuria** (concomitant cystitis)

**Diagnosis:**

**Dipstick Urinalysis:**
- **Leukocyte esterase:** Positive (WBCs)
- **Nitrite:** Positive (Gram-negative bacteria: E. coli, Klebsiella, Proteus)
- **Blood:** May be positive (hematuria)
- **Protein:** May be +1 (infection)

**Microscopy:**
- **WBCs:** > 10 WBC/hpf (pyuria)
- **RBCs:** May be present (hematuria)
- **Bacteria:** May be present

**Urine Culture:**
- **Indications:**
  - **Complicated UTI**
  - **Pyelonephritis**
  - **Recurrent UTI**
  - **Pregnant women**
  - **Failure to respond** to initial therapy
- **Significant bacteriuria:** ≥ 10^5 CFU/mL (single organism)

**Treatment:**

**Uncomplicated Cystitis (Women):**

**First-line:**
- **Nitrofurantoin** 100 mg MR BD (or 50 mg QDS) for 5 days
- **Trimethoprim** 200 mg BD for 3 days (if local resistance < 20%)
- **Alternative:** Fosfomycin 3 g single dose

**Second-line (if first-line contraindicated or resistant):**
- **Ciprofloxacin** 250 mg BD for 3 days (reserve for resistant organisms)
- **Amoxicillin-clavulanate** 500/125 mg TDS for 5 days

**Complicated Cystitis:**

**Pregnant Women:**
- **Nitrofurantoin** 100 mg MR BD for 7 days (avoid at term - hemolytic anemia in baby)
- **Cefalexin** 500 mg TDS for 7 days
- **Avoid:** Fluoroquinolones (Cartilage damage in fetus), Trimethoprim (Folic acid antagonist - teratogenic)

**Men:**
- **Ciprofloxacin** 500 mg BD for 7 days (or 500 mg BD for 14 days if recurrent)
- **Cefalexin** 500 mg TDS for 7 days
- **Consider:** Urology referral (rule out prostate enlargement, stones)

**Catheter-Associated:**
- **Remove catheter** if possible
- **Ciprofloxacin** 500 mg BD for 7 days
- **Avoid:** Nitrofurantoin (poor tissue penetration)

**Pyelonephritis (Upper UTI):**

**Mild (Outpatient):**
- **Ciprofloxacin** 500 mg BD for 7-14 days
- **Cefalexin** 500 mg TDS for 10-14 days
- **Add:** Gentamicin 5-7 mg/kg IV/IM single dose (if severe)

**Moderate-Severe (Hospitalized):**
- **Ceftriaxone** 2 g IV daily (or cefotaxime 2 g IV q8h)
- **Gentamicin** 5-7 mg/kg IV daily (add if severe)
- **Switch to oral** once afebrile for 48 hours (complete 10-14 day course)

**Pregnant Women (Pyelonephritis):**
- **Ceftriaxone** 2 g IV daily (hospitalization required)
- **Duration:** 10-14 days

**Recurrent UTI:**

**Prevention:**
- **Hydration:** 2-3 L/day
- **Voiding:** After intercourse
- **Cranberry products:** 500 mg daily (may prevent E. coli adhesion)
- **Low-dose antibiotic prophylaxis:**
  - **Nitrofurantoin** 50-100 mg at night
  - **Trimethoprim** 100 mg at night
  - **Cephalexin** 250-500 mg at night
  - **Duration:** 6-12 months (if recurrent)

**Post-Coital Prophylaxis:**
- **Nitrofurantoin** 50-100 mg single dose post-coital
- **Trimethoprim** 100 mg single dose post-coital

**Self-Start Therapy:**
- **Patient-initiated** at first symptoms (if recognized pattern)
- **Nitrofurantoin** 100 mg MR BD for 3-5 days

**Follow-up:**

**Test of Cure:**
- **NOT routinely indicated** (unless persistent symptoms, pregnancy)
- **Pregnant women:** Repeat urine culture 1-2 weeks after treatment

**Imaging:**
- **Indicated if:**
  - **Recurrent UTI** (> 2 infections in 6 months, > 3 infections in 1 year)
  - **Persistent hematuria**
  - **Suspected obstruction**
  - **No response** to appropriate antibiotics
- **Modalities:** Renal ultrasound, CT abdomen

**Urology Referral:**
- **Recurrent UTI** (especially men)
- **Suspected obstruction** (stones, stricture, prostate enlargement)
- **Persistent hematuria** (rule out bladder cancer)
- **Anatomic abnormality** (vesicoureteral reflux, diverticulum)

**Sources:** NICE NG109, EAU Guidelines 2024, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "infectious_diseases_uti",
                "focus": "uti_management",
                "sources": ["NICE NG109", "EAU 2024", "BMJ 2024"]
            }
        )

    def _handle_pneumonia(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pneumonia queries"""
        answer = """**Pneumonia Management**

**Classification:**

**Anatomic:**
- **Community-acquired pneumonia (CAP):** Acquired outside hospital
- **Hospital-acquired pneumonia (HAP):** Acquired > 48 hours after admission
- **Ventilator-associated pneumonia (VAP):** Acquired > 48 hours after intubation

**Severity Assessment:**

**CURB-65 Score (Calculate for each patient):**

| Parameter | Points |
|-----------|---------|
| **C**onfusion | 1 |
| **U**rea > 7 mmol/L (19 mg/dL) | 1 |
| **R**espiratory rate ≥ 30/min | 1 |
| **B**lood pressure: Systolic < 90 or Diastolic ≤ 60 | 1 |
| **65:** Age ≥ 65 | 1 |

**CURB-65 Interpretation:**
- **0-1:** Low risk (home treatment)
- **2:** Moderate risk (consider hospitalization)
- **3-5:** High risk (hospitalization, consider ICU)

**CRB-65 (if urea unavailable):**
- **0-1:** Low risk (home)
- **2:** Moderate (consider hospital)
- **3-4:** High (hospitalize)

**Etiology:**

**Community-Acquired Pneumonia (CAP):**
- **Streptococcus pneumoniae** (most common)
- **Haemophilus influenzae**
- **Atypical pathogens:** Mycoplasma pneumoniae, Chlamydia pneumoniae, Legionella pneumophila
- **Viruses:** Influenza, RSV, COVID-19, adenovirus

**Hospital-Acquired Pneumonia (HAP):**
- **Staphylococcus aureus** (MRSA)
- **Pseudomonas aeruginosa**
- **Klebsiella pneumoniae** (ESBL)
- **Enterobacter species**

**Diagnosis:**

**Symptoms:**
- **Cough**, **sputum** (purulent, rust-colored if pneumococcal)
- **Fever**, **chills**, **rigors**
- **Dyspnea**, **pleuritic chest pain**
- **Systemic:** Fatigue, myalgia, headache

**Physical Examination:**
- **Tachypnea** (> 20/min), **tachycardia**
- **Hypoxia** (SpO2 < 94%)
- **Crackles**, **bronchial breath sounds**, **egophony** (consolidation)
- **Pleural rub** (if pleurisy)

**Laboratory:**
- **CBC:** Leukocytosis (WBC > 11,000) or leukopenia (WBC < 4,000)
- **CRP** (elevated)
- **Procalcitonin** (if bacterial vs viral - elevated in bacterial)
- **Blood cultures** (2 sets, severe CAP or hospitalized)
- **Sputum culture** (if hospitalized, severe CAP)
- **Urinary antigens:** S. pneumoniae, Legionella (if severe CAP)

**Imaging:**
- **Chest X-ray:** New infiltrate/consolidation (gold standard for diagnosis)
- **CT chest:** If CXR negative but high clinical suspicion, or complications suspected

**Treatment:**

**Community-Acquired Pneumonia (CAP):**

**Mild (CURB-65 0-1, Home Treatment):**
- **Amoxicillin** 500 mg TDS (or 1 g TDS if severe comorbidities)
- **Add:** Macrolide (azithromycin 500 mg day 1, then 250 mg daily for 4 days) if atypical pathogens suspected
- **Duration:** 5 days (if improving)

**Moderate-Severe (CURB-65 ≥ 2, Hospitalized):**

**Non-Severe (Ward):**
- **Ceftriaxone** 2 g IV daily + **azithromycin** 500 mg daily
- **Alternative:** Amoxicillin-clavulanate 1.2 g IV TDS + macrolide

**Severe (ICU):**
- **Ceftriaxone** 2 g IV q12h + **azithromycin** 500 mg daily
- **Add:** **Vancomycin** 15 mg/kg IV q12h (if MRSA risk)
- **Add:** **Meropenem** 1 g IV q8h (if Pseudomonas risk)

**Duration:**
- **Uncomplicated:** 5-7 days
- **Complicated:** 7-10 days
- **Severe:** 10-14 days

**Hospital-Acquired Pneumonia (HAP):**

**Early-onset (≤ 5 days):**
- **Ceftriaxone** 2 g IV daily + **azithromycin** 500 mg daily
- **Alternative:** Piperacillin-tazobactam 3.375 g IV q6h

**Late-onset (> 5 days) or Risk Factors for MDR:**
- **Piperacillin-tazobactam** 3.375 g IV q6h (or cefepime 2 g IV q8h, or meropenem 1 g IV q8h)
- **Add:** **Vancomycin** 15 mg/kg IV q12h (if MRSA risk)
- **Duration:** 7-14 days (based on pathogen, response)

**Atypical Pneumonia:**

**Mycoplasma, Chlamydia, Legionella:**
- **Doxycycline** 100 mg BD (7-14 days)
- **Alternative:** Azithromycin 500 mg day 1, then 250 mg daily (5 days)
- **Severe Legionella:** Add **rifampin** 600 mg daily

**Viral Pneumonia:**

**Influenza:**
- **Oseltamivir** 75 mg BD for 5 days (within 48 hours of symptom onset)

**COVID-19:**
- **Remdesivir** (if hospitalized, requiring oxygen)
- **Dexamethasone** 6 mg daily (if requiring oxygen)

**RSV:**
- **Supportive care** (no specific antiviral)

**Supportive Care:**

**Oxygen:**
- **Target SpO2:** 92-96% (88-92% if at risk of hypercapnia - COPD)

**Fluids:**
- **Conservative** (avoid fluid overload - worsens oxygenation)

**Antipyretics:**
- **Acetaminophen**, NSAIDs (fever, myalgia)

**Bronchodilators:**
- **Salbutamol** (if wheezing, underlying COPD/asthma)

**Complications:**

**Parapneumonic Effusion / Empyema:**
- **Chest tube** drainage if purulent or loculated effusion
- **Intrapleural fibrinolytics** (tPA/DNase) if loculated

**Respiratory Failure:**
- **High-flow nasal cannula** (if hypoxemic respiratory failure)
- **Mechanical ventilation** (if worsening)
- **ECMO** (refractory hypoxemia)

**Sepsis:**
- **IV fluids**, **vasopressors** (septic shock)
- **See:** Sepsis section

**Prevention:**

**Vaccination:**
- **Pneumococcal vaccine:** PCV13 (children), PPSV23 (adults > 65, high-risk)
- **Influenza vaccine:** Annually (all > 6 months)
- **COVID-19 vaccine:** As per guidelines

**Smoking Cessation:**
- **Increased risk** of pneumococcal pneumonia, Legionella
- **Counseling**, **pharmacotherapy** (NRT, varenicline)

**Sources:** NICE NG191, BTS 2024, IDSA 2019"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "infectious_diseases_respiratory",
                "focus": "pneumonia_management",
                "sources": ["NICE NG191", "BTS 2024", "IDSA 2019"]
            }
        )

    def _handle_skin_infection(self, query: str, context: dict) -> DomainQueryResult:
        """Handle skin/soft tissue infection queries"""
        answer = """**Skin and Soft Tissue Infection (SSTI) Management**

**Classification:**

**Uncomplicated SSTI:**
- **Superficial:** Cellulitis, erysipelas, impetigo, folliculitis
- **No purulent drainage**, **no abscess**
- **Minimal systemic symptoms**

**Complicated SSTI:**
- **Deep:** Abscess, fasciitis, myositis
- **Purulent drainage**, **necrosis**
- **Systemic symptoms:** Fever, tachycardia, hypotension
- **Comorbidities:** Diabetes, immunocompromised, peripheral vascular disease

**Common Infections:**

**Cellulitis:**
- **Etiology:** Staphylococcus aureus, Streptococcus pyogenes (group A strep)
- **Clinical:** Erythema, warmth, edema, tenderness
- **Distribution:** Unilateral, lower extremity most common
- **Distinguishing from DVT:** Cellulitis has well-demarcated erythema, DVT has swelling but no erythema

**Erysipelas:**
- **Etiology:** Streptococcus pyogenes (group A strep)
- **Clinical:** Bright red, well-demarcated, raised plaque
- **Location:** Face, lower extremities
- **Systemic:** Fever, chills common

**Impetigo:**
- **Etiology:** S. aureus, S. pyogenes
- **Clinical:** Honey-colored crusts, erosions
- **Population:** Children (2-5 years)
- **Contagious:** Highly contagious (skin-to-skin contact)

**Abscess:**
- **Etiology:** S. aureus (MRSA increasingly common)
- **Clinical:** Fluctuant, tender, erythematous nodule
- **Treatment:** Incision and drainage (I&D)

**Necrotizing Fasciitis:**
- **Etiology:** Polymicrobial (S. pyogenes + anaerobes) OR monomicrobial (S. aureus, Vibrio, Aeromonas)
- **Clinical:** Severe pain, swelling, crepitus, bullae, necrosis, systemic toxicity
- **Emergency:** Surgical debridement, IV antibiotics

**Diagnosis:**

**Clinical Diagnosis:**
- **Most SSTIs** diagnosed clinically (appearance, symptoms)
- **Culture** indicated if:
  - **Severe infection** (ICU admission)
  - **Purulent drainage** (abscess, exudate)
  - **Systemic symptoms** (fever, hypotension)
  - **Recurrent infection**
  - **MRSA risk** (recent hospitalization, antibiotics, known colonization)

**Laboratory:**
- **CBC with differential** (WBC, bands)
- **CRP/ESR** (inflammatory markers)
- **Blood cultures** (if severe, systemic symptoms)
- **Wound culture** (if purulent, abscess)
- **Swab** (if possible)

**Imaging:**
- **Ultrasound** (distinguish abscess from cellulitis)
- **CT/MRI** (if deep infection, necrotizing fasciitis suspected)

**Treatment:**

**Cellulitis/Erysipelas:**

**Mild (Outpatient):**
- **Flucloxacillin** 500 mg PO QDS (or 500-1000 mg IV q6h if severe)
- **Duration:** 5-7 days (extend to 10-14 days if slow response)
- **Penicillin allergy:**
  - **Mild:** Clarithromycin 500 mg PO BD
  - **Severe:** Clindamycin 300-450 mg PO QID

**Moderate-Severe (Hospitalized):**
- **Cefazolin** 2 g IV q8h (or ceftriaxone 2 g IV daily)
- **Add:** **Vancomycin** 15 mg/kg IV q12h (if MRSA risk: severe infection, recent hospitalization, known colonization)
- **Duration:** 7-14 days

**Purulent Infection (Abscess, Furuncle):**

**Incision and Drainage (I&D):**
- **Primary treatment** for abscess
- **Antibiotics NOT routinely required** if I&D performed and mild infection
- **Antibiotics indicated if:**
  - **Severe infection** (extensive cellulitis, systemic symptoms)
  - **Rapid progression** despite I&D
  - **Comorbidities:** Diabetes, immunocompromised, severe edema
  - **Location:** Face, hand, genitalia (high-risk areas)

**Antibiotics for Purulent Infection:**
- **If MRSA suspected:**
  - **Clindamycin** 300-450 mg PO QID
  - **Trimethoprim-sulfamethoxazole (TMP-SMX):** 2 DS PO BD
  - **Doxycycline** 100 mg PO BD
- **Duration:** 5-10 days

**Necrotizing Fasciitis:**

**EMERGENCY:**
- **SURGICAL DEBRIDEMENT** (immediate, extensive)
- **IV Antibiotics:**
  - **Penicillin G** 2-4 million units IV q4h (covers S. pyogenes)
  - **Clindamycin** 900 mg IV q8h (toxin suppression)
  - **Add:** **Gentamicin** 5-7 mg/kg IV daily (if Gram-negative risk)
  - **Add:** **Vancomycin** 15 mg/kg IV q12h (if MRSA risk)

**Supportive Care:**
- **IV fluids**, **vasopressors** (septic shock)
- **ICU admission**
- **Hyperbaric oxygen** (controversial, may consider)

**Duration:** 2-6 weeks (based on surgical findings, response)

**Impetigo:**

**Topical:**
- **Mupirocin** 2% ointment TID (localised infection)
- **Retapamulin** 1% ointment BID (alternative)

**Oral (if extensive):**
- **Flucloxacillin** 500 mg PO QDS (5 days)
- **Alternative:** Erythromycin 250-500 mg QID (if penicillin allergy)

**Folliculitis:**

**Mild:**
- **Topical antibiotic:** Mupirocin 2% ointment BID
- **Antiseptic wash:** Chlorhexidine gluconate 4% cleanser daily

**Moderate-Severe:**
- **Oral antibiotic:** Cephalexin 500 mg PO QID (7-10 days)
- **Penicillin allergy:** Clindamycin 300-450 mg PO QID

**Specific Considerations:**

**Diabetic Foot Infection:**
- **Polymicrobial:** S. aureus, Streptococci, anaerobes, Gram-negative rods
- **Treatment:**
  - **Mild:** Cephalexin 500 mg PO QID + **metronidazole** 500 mg PO TID (10-14 days)
  - **Severe:** Piperacillin-tazobactam 3.375 g IV q6h ± **vancomycin** (10-14 days)
- **Debridement** (essential)
- **Vascular surgery** (if ischemia)

**Periorbital/Orbital Cellulitis:**
- **Periorbital:** Cefalexin 500 mg PO QID (or flucloxacillin 500 mg PO QDS) for 5-7 days
- **Orbital:** **EMERGENCY** (vision loss, CNS spread)
  - **Ceftriaxone** 2 g IV q12h + **metronidazole** 500 mg IV TID
  - **Add:** **Vancomycin** 15 mg/kg IV q12h (if MRSA risk)
  - **CT orbit** (if orbital involvement suspected)
  - **Surgical drainage** (if abscess)
  - **Ophthalmology** consultation

**Recurrent Cellulitis:**
- **Identify/modify risk factors:** Tinea pedis, edema, venous insufficiency, obesity
- **Prophylaxis:**
  - **Penicillin V** 500 mg PO daily (or BD)
  - **Erythromycin** 250 mg PO daily (if penicillin allergy)
  - **Duration:** 4-52 weeks (based on frequency of recurrence)

**Sources:** NICE NG110, IDSA 2014, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "infectious_diseases_skin",
                "focus": "ssti_management",
                "sources": ["NICE NG110", "IDSA 2014", "BMJ 2024"]
            }
        )

    def _handle_vaccination(self, query: str, context: dict) -> DomainQueryResult:
        """Handle vaccination queries"""
        answer = """**Vaccination Schedules (UK - NHS Schedule)**

**Childhood Immunizations (0-18 years):**

**8 Weeks:**
- **6-in-1 vaccine** (1st dose): Diphtheria, Hepatitis B, Hib (Haemophilus influenzae type b), Polio, Tetanus, Pertussis (whooping cough)
- **Rotavirus vaccine** (1st dose): Oral
- **MenB vaccine** (1st dose): Meningococcal group B

**12 Weeks:**
- **6-in-1 vaccine** (2nd dose)
- **Pneumococcal (PCV)** vaccine (1st dose)
- **Rotavirus vaccine** (2nd dose)

**16 Weeks:**
- **6-in-1 vaccine** (3rd dose)
- **MenB vaccine** (2nd dose)

**1 Year (12-13 months):**
- **Hib/MenC booster** (1st dose)
- **MMR** (1st dose): Measles, Mumps, Rubella
- **Pneumococcal (PCV)** booster (2nd dose)
- **MenB booster** (3rd dose)

**2-3 Years:**
- **Influenza vaccine:** Nasal spray (annual)

**3 Years 4 Months (Pre-school):**
- **MMR** (2nd dose)
- **4-in-1 pre-school booster:** Diphtheria, Tetanus, Pertussis, Polio

**12-13 Years (Girls):**
- **HPV vaccine:** Human Papillomavirus (2 doses, 6-24 months apart)

**14 Years:**
- **3-in-1 teenage booster:** Tetanus, Diphtheria, Polio
- **MenACWY:** Meningococcal groups A, C, W, Y
- **MMR** (if missed earlier)

**Adult Immunizations:**

**Influenza (Annual):**
- **Indications:** ALL adults ≥ 65 years, high-risk groups (chronic disease, immunocompromised, pregnancy, healthcare workers, carers)
- **Timing:** September-November (before flu season)
- **Types:**
  - **Egg-based:** Quadrivalent (4 strains)
  - **Cell-based:** (egg allergy)
  - **Adjuvanted:** (> 65 years - stronger immune response)

**Pneumococcal:**

**PPSV23 (Pneumococcal polysaccharide vaccine):**
- **Indications:** ALL adults ≥ 65 years (single dose)
- **High-risk:** < 65 years with chronic disease (asplenia, immunocompromised, cochlear implant, CSF leak)
- **Repeat:** Once after 5 years (if asplenia, immunocompromised)

**PCV13 (Pneumococcal conjugate vaccine):**
- **Indications:** Adults ≥ 65 years (single dose, 1 year before PPSV23 if both needed)
- **High-risk:** < 65 years with immunocompromising conditions, asplenia, CSF leak, cochlear implant

**Shingles (Herpes Zoster):**

**Shingles vaccine (Shingrix - recombinant subunit):**
- **Indications:** Adults ≥ 70 years (up to 79 years)
- **Dose:** 2 doses, 2 months apart
- **Efficacy:** > 90% (prevents shingles, post-herpetic neuralgia)

**COVID-19:**
- **Booster doses:** Every 6-12 months (variants, waning immunity)

**Travel Vaccinations:**

**Hepatitis A:**
- **Indications:** Travel to endemic areas (South Asia, Africa, Central/South America), MSM, chronic liver disease
- **Dose:** 2 doses, 6-12 months apart

**Typhoid:**
- **Indications:** Travel to endemic areas (South Asia, parts of Africa, Latin America)
- **Types:**
  - **Oral live attenuated:** 3 doses, every other day (booster every 5 years)
  - **Vi capsular polysaccharide:** Single dose (booster every 2-3 years)

**Yellow Fever:**
- **Indications:** Travel to endemic areas (sub-Saharan Africa, South America)
- **Single dose:** Lifelong immunity (most countries)
- **Certificate:** Required for entry to some countries (valid 10 days after vaccination, lifetime)

**Japanese Encephalitis:**
- **Indications:** Travel to endemic areas (rural Asia, Pacific)
- **Dose:** 2 doses, 28 days apart

**Rabies:**
- **Pre-exposure prophylaxis:** 3 doses, days 0, 7, 21-28
- **Indications:** Travel to high-risk areas, handling animals, prolonged stay

**Meningococcal:**
- **MenACWY:** Travel to meningitis belt (sub-Saharan Africa), Hajj pilgrimage
- **MenB:** Not routinely recommended for travel

**Tetanus:**
- **Booster:** Every 10 years (if injury > 5 years since last dose, give booster)
- **Post-exposure:** Tetanus vaccine ± tetanus immunoglobulin (if high-risk wound, < 3 doses, > 10 years since last dose)

**Contraindications:**

**Absolute:**
- **Anaphylaxis** to previous dose or vaccine component
- **Encephalitis** within 7 days of previous pertussis-containing vaccine

**Precautions:**
- **Acute moderate-severe illness:** Defer vaccination until recovered
- **Pregnancy:** Live vaccines contraindicated (MMR, varicella, yellow fever), inactivated vaccines safe (influenza, Tdap)
- **Immunocompromised:** Avoid live vaccines (except MMR, varicella if HIV with CD4 > 15%)

**Special Populations:**

**Pregnancy:**
- **Safe:** Influenza (any trimester), Tdap (27-36 weeks), COVID-19
- **Avoid:** Live vaccines (MMR, varicella, yellow fever)
- **Postpartum:** MMR, varicella (if not immune)

**Immunocompromised:**
- **Inactivated vaccines:** Safe (may have reduced response)
- **Live vaccines:** Generally contraindicated (MMR, varicella, yellow fever, LAIV influenza) EXCEPT:
  - **MMR, varicoline:** If HIV with CD4 ≥ 15% (children), ≥ 200 cells/mm³ (adults)

**HIV-Infected:**
- **Follow routine schedule** (except live vaccines if severely immunocompromised)
- **Additional vaccines:** Pneumococcal (PCV13 + PPSV23), Hepatitis A, Hepatitis B, Meningococcal (MenACWY, MenB), HPV

**Asplenia (Functional or Anatomic):**
- **Additional vaccines:**
  - **Pneumococcal:** PCV13 + PPSV23 (booster every 5 years)
  - **Meningococcal:** MenACWY (booster every 5 years), MenB
  - **Hib:** Single dose
  - **Influenza:** Annual

**Sources:** NHS UK Schedule 2024, PHE Green Book 2024, WHO 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "infectious_diseases_prevention",
                "focus": "vaccination_schedules",
                "sources": ["NHS 2024", "PHE 2024", "WHO 2024"]
            }
        )

    def _handle_travel_medicine(self, query: str, context: dict) -> DomainQueryResult:
        """Handle travel medicine queries"""
        answer = """**Travel Medicine Consultation**

**Pre-Travel Assessment (6-8 weeks before departure):**

**1. Destination-Specific Risks:**
- **Endemic diseases:** Malaria, yellow fever, typhoid, Japanese encephalitis
- **Vaccine requirements:** Yellow fever (certificate required), meningococcal (Hajj, meningitis belt)
- **Food/water safety:** Traveler's diarrhea, cholera, typhoid, hepatitis A
- **Insect-borne diseases:** Malaria, dengue, chikungunya, Zika, yellow fever, Japanese encephalitis

**2. Individual Risk Assessment:**
- **Age:** Pediatric, elderly (special considerations)
- **Pregnancy:** Avoid live vaccines, certain antimalarials
- **Comorbidities:** Immunocompromised, chronic diseases
- **Medications:** Drug interactions, contraindications
- **Allergies:** Vaccine components (eggs, gelatin, neomycin)

**3. Travel Itinerary:**
- **Duration:** Extended travel (> 6 months) may require additional vaccinations
- **Season:** Rainy season (malaria transmission higher)
- **Activities:** Rural travel (malaria, yellow fever risk), animal contact (rabies), freshwater exposure (schistosomiasis, leptospirosis)
- **Accommodation:** Budget backpacking (higher risk) vs luxury resort (lower risk)
- **Access to medical care:** Remote (pack medical kit)

**Vaccination:**

**Routine Vaccinations (Update if needed):**
- **MMR:** Measles, mumps, rubella (outbreaks in travel destinations)
- **Tdap:** Tetanus, diphtheria, pertussis (booster every 10 years)
- **Polio:** Booster if traveling to endemic areas (Afghanistan, Pakistan)
- **Influenza:** Annual (if traveling during flu season)
- **COVID-19:** As per destination requirements

**Travel-Specific Vaccinations:**

**Hepatitis A:**
- **Indications:** Travel to developing countries (endemic areas)
- **Dose:** 2 doses, 6-12 months apart
- **Efficacy:** 95-100%

**Typhoid:**
- **Indications:** Travel to endemic areas (South Asia, parts of Africa, Latin America)
- **Types:**
  - **Oral live attenuated:** 3 doses, every other day (booster every 5 years)
  - **Vi capsular polysaccharide:** Single dose (booster every 2-3 years)
- **Efficacy:** 50-80% (oral), 50-70% (Vi)

**Yellow Fever:**
- **Indications:** Travel to endemic areas (sub-Saharan Africa, South America)
- **Certificate:** Required for entry to some countries (valid 10 days after vaccination, lifetime)
- **Contraindicated:** Pregnancy, immunocompromised, infants < 6 months
- **Exemption:** Medical waiver if contraindicated

**Japanese Encephalitis:**
- **Indications:** Travel to rural Asia for > 1 month (transmission season)
- **Dose:** 2 doses, 28 days apart
- **Efficacy:** > 90%

**Meningococcal (MenACWY):**
- **Indications:** Travel to meningitis belt (sub-Saharan Africa), Hajj pilgrimage
- **Certificate:** Required for Hajj (valid 5 years)
- **Dose:** Single dose (booster every 5 years)

**Rabies (Pre-Exposure Prophylaxis):**
- **Indications:** Travel to high-risk areas, handling animals, prolonged stay, remote areas (no access to rabies immunoglobulin)
- **Dose:** 3 doses, days 0, 7, 21-28
- **NOT** for post-exposure (still requires 2 doses post-exposure, no rabies immunoglobulin needed)

**Malaria Prophylaxis:**

**Risk Assessment:**
- **Destination:** Endemic areas (sub-Saharan Africa, South Asia, parts of South America, Asia)
- **Season:** Transmission season (often rainy season)
- **Duration:** Short trip (< 1 week) vs long-term (> 1 month)
- **Activities:** Rural travel (higher risk) vs urban business travel (lower risk)

**Antimalarial Options:**

**Atovaquone-Proguanil (Malarone):**
- **Dose:** 1 tablet daily (start 1-2 days before, continue 1 week after)
- **Advantages:** Well tolerated, few side effects, short duration
- **Disadvantages:** Expensive, daily dosing

**Doxycycline:**
- **Dose:** 100 mg daily (start 1-2 days before, continue 4 weeks after)
- **Advantages:** Inexpensive, also prevents rickettsial diseases, no drug interactions
- **Disadvantages:** Photosensitivity, vaginal candidiasis, esophagitis (take with plenty of water)

**Mefloquine:**
- **Dose:** 250 mg weekly (start 2-3 weeks before, continue 4 weeks after)
- **Advantages:** Weekly dosing, inexpensive
- **Disadvantages:** Contraindicated in epilepsy, psychiatric disorders, severe neuropsychiatric side effects (rare but potentially irreversible)

**Malaria Prevention (Non-Pharmacologic):**
- **Mosquito avoidance:** DEET or picaridin repellents, permethrin-treated clothing, bed nets (if sleeping in unscreened areas)
- **Peak biting times:** Dawn to dusk (Anopheles mosquitoes)
- **Clothing:** Long sleeves, long pants, light-colored clothing

**Traveler's Diarrhea Prevention:**
- **Food/water safety:** Boil it, cook it, peel it, or forget it
- **Avoid:** Tap water, ice, raw fruits/vegetables (unless washed with safe water), street food
- **Safe:** Bottled water (sealed), hot cooked food, fruits you peel yourself
- **Prophylaxis:** Rifaximin 200 mg TID (short-term travelers, consider if high-risk)
- **Treatment:** Loperamide + azithromycin 500 mg daily (if moderate diarrhea, no fever)

**Medical Kit:**
- **First aid:** Bandages, antiseptic, pain relievers
- **Medications:**
  - **Antibiotics:** Azithromycin (traveler's diarrhea, respiratory infections)
  - **Antidiarrheal:** Loperamide
  - **Antiemetic:** Ondansetron
  - **Rehydration salts:** ORS packets
  - **Antihistamine:** Cetirizine (allergic reactions)
  - **Topical:** Antibiotic ointment (mupirocin), hydrocortisone cream, antifungal (clotrimazole)
  - **Altitude sickness:** Acetazolamide (if traveling to high altitude)
  - **Motion sickness:** Meclizine, transdermal scopolamine

**Post-Travel Assessment:**

**Fever:**
- **Urgent medical evaluation** if fever within 6 months of travel (especially malaria, dengue, typhoid)
- **Malaria:** Most important to rule out (can be rapidly fatal)
- **Dengue:** Supportive care, avoid NSAIDs (bleeding risk)
- **Typhoid:** Blood cultures, fluoroquinolones

**Diarrhea:**
- **Persistent** (> 14 days): Stool for ova & parasites (Giardia, Cryptosporidium), consider post-infectious IBS, lactose intolerance

**Skin Lesions:**
- **Cutaneous larva migrans** (hookworm)
- **Myiasis** (botfly)
- **Tungiasis** (chigoe flea)
- **Leishmaniasis** (sandfly bite)

**Sources:** CDC Yellow Book 2024, WHO 2024, NaTHNaC 2024"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "infectious_diseases_travel",
                "focus": "travel_medicine",
                "sources": ["CDC 2024", "WHO 2024", "NaTHNaC 2024"]
            }
        )

    def _handle_general_infectious(self, query: str, context: dict) -> DomainQueryResult:
        """General infectious diseases information"""
        answer = """**Infectious Diseases Overview**

**Infection Types:**
- **Bacterial:** Staphylococcus, Streptococcus, E. coli, Pseudomonas
- **Viral:** Influenza, COVID-19, HIV, hepatitis, herpes viruses
- **Fungal:** Candida, Aspergillus, Cryptococcus
- **Parasitic:** Malaria, Giardia, Toxoplasma

**Common Presentations:**
- **Fever** (elevated temperature)
- **Sepsis** (life-threatening organ dysfunction)
- **Respiratory** (pneumonia, bronchitis)
- **Urinary** (UTI, pyelonephritis)
- **Skin/soft tissue** (cellulitis, abscess)
- **CNS** (meningitis, encephalitis)

**Treatment Principles:**
- **Antibiotics:** Bacterial infections (choice based on likely pathogen, severity, resistance patterns)
- **Antivirals:** Viral infections (influenza, herpes, HIV)
- **Antifungals:** Fungal infections (candidiasis, aspergillosis)
- **Supportive care:** Hydration, antipyretics, oxygen

**Prevention:**
- **Vaccination** (most effective public health intervention)
- **Hand hygiene** (alcohol hand rub, soap and water)
- **Safe food/water** (traveler's diarrhea prevention)
- **Infection control** (isolation, PPE)

**Sources:** NICE guidelines, WHO, CDC"""

        return DomainQueryResult(
            domain_name="infectious_diseases",
            answer=answer,
            confidence=0.84,
            metadata={
                "specialty": "infectious_diseases",
                "focus": "general_information",
                "sources": ["NICE", "WHO", "CDC"]
            }
        )

def create_infectious_diseases_domain():
    """Factory function to create infectious diseases domain instance"""
    return InfectiousDiseasesDomain()
