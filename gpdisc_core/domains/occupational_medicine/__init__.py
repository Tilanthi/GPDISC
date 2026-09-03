"""
Occupational Medicine Domain for GPDISC

Comprehensive occupational medicine domain covering work-related health,
occupational diseases, workplace hazards, and fitness for work.

Evidence-based: Faculty of Occupational Medicine (FOM), HSE, NICE Guidelines,
SOM (Society of Occupational Medicine)
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class OccupationalMedicineDomain(BaseDomainModule):
    """
    Occupational Medicine Domain

    Covers all aspects of occupational medicine including:
    - Work-related health assessments
    - Occupational diseases (asbestosis, silicosis, occupational asthma, etc.)
    - Workplace hazards (chemical, physical, biological, ergonomic, psychosocial)
    - Fitness for work assessments
    - Sickness absence management
    - Workplace health surveillance
    - Health and safety regulations
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="occupational_medicine",
            version="1.0.0",
            dependencies=[],
            description="Occupational medicine - Work-related health, occupational diseases, workplace hazards, fitness for work, sickness absence",
            keywords=[
                # Work-related health
                "work-related health", "occupational health", "occupational medicine",
                "workplace health", "employee health", "fitness for work", "fit note",
                "sickness absence", "sick note", "return to work",
                # Occupational diseases
                "occupational asthma", "occupational dermatitis", "hand eczema",
                "asbestosis", "mesothelioma", "silicosis", "occupational lung disease",
                "noise-induced hearing loss", "vibration white finger", "hand-arm vibration syndrome",
                "repetitive strain injury", "rsi", "work-related upper limb disorder", "wruld",
                "stress", "work-related stress", "burnout", "mental health at work",
                # Workplace hazards
                "workplace hazard", "chemical hazard", "physical hazard", "biological hazard",
                "ergonomic hazard", "psychosocial hazard", "coshh", "risk assessment",
                "coshh", "health surveillance", "display screen equipment", "dse",
                # Work injuries
                "work injury", "accident at work", "riddor", "workplace accident",
                "industrial injury", "work-related injury"
            ],
            capabilities=[
                "occupational_health_assessment", "fitness_for_work_assessment",
                "occupational_disease_diagnosis", "workplace_hazard_assessment",
                "sickness_absence_management", "health_surveillance", "rehabilitation_guidance"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        query_lower = query.lower()

        # WORKPLACE EMERGENCIES
        if any(term in query_lower for term in ["workplace emergency", "chemical exposure",
                                                   "accident at work", "work injury emergency"]):
            return self._handle_workplace_emergency(query, context)

        # OCCUPATIONAL ASTHMA
        if any(term in query_lower for term in ["occupational asthma", "work-related asthma",
                                                   "baker's asthma", "isocyanate asthma"]):
            return self._handle_occupational_asthma(query, context)

        # OCCUPATIONAL DERMATITIS
        if any(term in query_lower for term in ["occupational dermatitis", "hand eczema",
                                                   "work-related dermatitis", "contact dermatitis"]):
            return self._handle_occupational_dermatitis(query, context)

        # NOISE-INDUCED HEARING LOSS
        if any(term in query_lower for term in ["noise-induced hearing loss", "nihl",
                                                   "industrial deafness", "work-related hearing loss"]):
            return self._handle_noise_induced_hearing_loss(query, context)

        # HAND-ARM VIBRATION SYNDROME
        if any(term in query_lower for term in ["hand-arm vibration syndrome", "havs",
                                                   "vibration white finger", "vwf", "vibration injury"]):
            return self._handle_havs(query, context)

        # ASBESTOS-RELATED DISEASES
        if any(term in query_lower for term in ["asbestosis", "mesothelioma", "asbestos exposure",
                                                   "pleural plaque", "asbestosis diagnosis"]):
            return self._handle_asbestos_diseases(query, context)

        # WORK-RELATED STRESS
        if any(term in query_lower for term in ["work-related stress", "occupational stress",
                                                   "workplace stress", "burnout", "mental health at work"]):
            return self._handle_work_related_stress(query, context)

        # REPETITIVE STRAIN INJURY (RSI)
        if any(term in query_lower for term in ["repetitive strain injury", "rsi",
                                                   "work-related upper limb disorder", "wruld",
                                                   "carpal tunnel syndrome work"]):
            return self._handle_rsi(query, context)

        # FITNESS FOR WORK
        if any(term in query_lower for term in ["fitness for work", "fit note", "fit for work assessment",
                                                   "return to work", "sick note", "sickness absence"]):
            return self._handle_fitness_for_work(query, context)

        # DISPLAY SCREEN EQUIPMENT (DSE)
        if any(term in query_lower for term in ["display screen equipment", "dse", "computer workstation",
                                                   "vdu", "visual display unit", "eye strain work"]):
            return self._handle_dse(query, context)

        # GENERAL OCCUPATIONAL MEDICINE
        else:
            return self._handle_general_occupational_medicine(query, context)

    def _handle_workplace_emergency(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Workplace emergency management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**WORKPLACE EMERGENCY MANAGEMENT**

**CHEMICAL EXPOSURE:**

**IMMEDIATE ACTION:**

1. **REMOVE from exposure:**
   - **Inhalation:** Move to fresh air immediately
   - **Skin contact:** Remove contaminated clothing, wash skin with copious water (15-20 minutes)
   - **Eye contact:** Irrigate eyes with water/normal saline (15-20 minutes)
   - **Ingestion:** Do NOT induce vomiting, rinse mouth, give water to drink (if conscious)

2. **ASSESS ABCDE:**
   - **Airway:** Assess patency, prepare for intubation
   - **Breathing:** Oxygen 15 L/min, check respiratory effort, auscultation
   - **Circulation:** BP, heart rate, ECG, IV access
   - **Disability:** GCS, pupil response
   - **Exposure:** Full examination, skin inspection

3. **SPECIFIC TREATMENTS:**
   - **Inhaled irritants:** Oxygen, nebulised bronchodilator (salbutamol 2.5-5 mg), consider corticosteroids (if severe airway oedema)
   - **Skin burns:** Cool running water (20 minutes), cover with non-adherent dressing, refer to burns unit
   - **Eye exposure:** Irrigate with water/normal saline (15-20 minutes), fluorescein staining, refer to ophthalmology

4. **DECONTAMINATION:**
   - **Remove clothing:** Place in plastic bag (avoid contamination)
   - **Wash skin:** Soap and water, copious water
   - **Shower:** Full body shower (if contaminated)

5. **OBSERVATION:**
   - **Observation period:** 4-6 hours (delayed pulmonary oedema possible)
   - **Monitoring:** Pulse oximetry, respiratory rate, chest X-ray (if symptomatic)
   - **Admission:** If symptomatic (cough, dyspnoea, hypoxia) or significant exposure

**ACCIDENT AT WORK:**

**IMMEDIATE ACTION:**

1. **ASSESS INJURY:**
   - **Primary survey:** ABCDE (life-threatening injuries first)
   - **Secondary survey:** Full examination, identify all injuries
   - **Imaging:** X-ray, CT as indicated

2. **TREATMENT:**
   - **Fractures:** Immobilise, analgesia, refer to orthopaedics
   - **Wounds:** Clean, dress, tetanus prophylaxis (if indicated)
   - **Head injury:** CT head if indications (GCS <15, focal neurology, amnesia >30 minutes, loss of consciousness)
   - **Spinal injury:** Spinal precautions (log-roll, cervical collar), CT whole spine

3. **DOCUMENTATION:**
   - **Accident report:** Complete accident report form (RIDDOR report if required)
   - **First aid record:** Document first aid provided
   - **Incident investigation:** Identify root cause, prevent recurrence

**RIDDOR REPORTING:**

**RIDDOR (Reporting of Injuries, Diseases and Dangerous Occurrences Regulations):**

**Reportable accidents:**
- **Death:** Any work-related death
- **Major injury:** Fracture (other than fingers/toes), amputation, dislocation, loss of sight, chemical/ hot metal burn to eye/face, injury leading to resuscitation/loss of consciousness >24 hours, admission to hospital >24 hours
- **Over-7-day injury:** Injury leading to absence >7 days (must report within 15 days)
- **Over-3-day injury:** Injury leading to absence >3 days (must record in accident book)

**Reportable diseases:**
- **Carpal tunnel syndrome:** Work-related
- **Cramp of the hand:** Work-related
- **Occupational dermatitis:** Work-related
- **Hand-arm vibration syndrome:** Work-related
- **Occupational asthma:** Work-related
- **Tendonitis/tenosynovitis:** Work-related
- **Asbestosis, mesothelioma:** asbestos-related

**Reportable dangerous occurrences:**
- **Collapse, overturning, failure:** Of lift, scaffolding, crane, etc.
- **Explosion:** Collapse of building, structure
- **Accidental release:** Of biological agent, hazardous substance
- **Electrical short circuit:** Causing fire or explosion

**Reporting:**
- **Online:** HSE website (https://www.hse.gov.uk/riddor)
- **Telephone:** HSE Infoline (for fatal/major incidents only)
- **Timeframe:** Immediately for fatalities/major injuries, within 10 days for other incidents

**Sources:** HSE Guidelines, FOM Guidelines, Resuscitation Council (UK) Guidelines""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "Resuscitation Council (UK) Guidelines"],
                "emergency_protocol": "workplace_emergency"
            }
        )

    def _handle_occupational_asthma(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Occupational asthma diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**OCCUPATIONAL ASTHMA**

**DEFINITION:**
Asthma caused by workplace exposure to sensitising agents (asthmagens) or irritants.

**WORKPLACE SENSITISERS (ASTHMAGENS):**

**High-molecular-weight agents (protein sensitizers):**
- **Flour/grain:** Baker's asthma (flour dust, grain dust)
- **Animals:** Laboratory animal allergy (urine protein, dander)
- **Latex:** Natural rubber latex (healthcare workers)
- **Enzymes:** Detergent enzymes (proteases)
- **Wood dust:** Western red cedar, oak, mahogany
- **Food:** Seafood, spices, food processing

**Low-molecular-weight agents (chemical sensitizers):**
- **Isocyanates:** Spray painting, foam manufacturing (MDI, TDI, HDI)
- **Resins:** Epoxy resins, acrylic resins
- **Metal salts:** Platinum salts, nickel, chromium, cobalt
- **Persulphates:** Hairdressers (hair bleach)
- **Antibiotics:** Pharmaceutical manufacturing

**DIAGNOSIS:**

**Clinical features:**
- **Symptoms:** Wheeze, cough, chest tightness, dyspnoea (work-related)
- **Timing:** Symptoms improve on weekends/holidays, worsen on workdays
- **Latency period:** Months to years of exposure before symptoms develop (sensitisation period)

**Objective tests:**
- **Serial peak flow monitoring:** Measure peak flow 4 times daily (work days vs. rest days)
  - **Occupational pattern:** 20% diurnal variation + work-related variation (better on rest days)
- **Spirometry:** Reversible airflow obstruction (FEV1/FVC <0.7, >12% and >200 mL improvement post-bronchodilator)
- **Bronchial hyperresponsiveness:** Methacholine challenge test (if baseline spirometry normal)
- **Immunology:** Specific IgE (RAST) to workplace sensitizer (if available)

**MANAGEMENT:**

**1. REMOVE FROM EXPOSURE:**
- **Complete removal:** Permanent removal from exposure (essential for sensitizers)
- **Reduce exposure:** If removal not possible (use respiratory protection, improve ventilation)

**2. ASTHMA TREATMENT:**
- **Short-acting bronchodilator:** Salbutamol 100-200 mcg prn (reliever)
- **Inhaled corticosteroid:** Beclometasone 200 mcg BD or budesonide 200 mcg BD (preventer)
- **Long-acting bronchodilator:** Salmeterol 50 mcg BD or formoterol 12 mcg BD (if persistent symptoms)
- **Combination inhaler:** Salmeterol/fluticasone 50/250 mcg BD (if moderate-severe asthma)

**3. REHABILITATION:**
- **Return to work:** If exposure eliminated (different job, different department)
- **Retraining:** New skills for different job (if unable to return to previous job)
- **Benefits:** Statutory sick pay, Employment and Support Allowance (ESA) if unable to work

**PROGNOSIS:**
- **Early removal:** Better prognosis (symptoms may improve or resolve)
- **Continued exposure:** Worse prognosis (asthma persists even after removal, airway remodelling)

**PREVENTION:**
- **Substitution:** Replace sensitizers with less hazardous alternatives
- **Engineering controls:** Enclose processes, local exhaust ventilation (LEV)
- **Respiratory protection:** Face mask (FFP3 mask for sensitizer exposure)
- **Health surveillance:** Annual respiratory questionnaire and spirometry for at-risk workers

**Sources:** HSE Guidelines, BOHRF Guidelines, SIGN Guidelines (British Occupational Health Research Foundation)""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "BOHRF Guidelines", "SIGN Guidelines"]
            }
        )

    def _handle_occupational_dermatitis(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Occupational dermatitis (hand eczema) diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**OCCUPATIONAL DERMATITIS (HAND ECZEMA)**

**DEFINITION:**
Work-related skin inflammation, most commonly affecting hands (contact dermatitis).

**CAUSES:**

**Irritant contact dermatitis (80% of cases):**
- **Wet work:** Frequent hand washing, glove use (healthcare workers, hairdressers, cleaners)
- **Detergents:** Cleaning products, shampoos, dishwashing liquids
- **Solvents:** Oils, degreasers (mechanics, engineers)
- **Foods:** Juices, spices (chefs, food processing)

**Allergic contact dermatitis (20% of cases):**
- **Nickel:** Tools, keys, coins (hairdressers, mechanics, cashiers)
- **Chromate:** Cement, leather (construction workers, shoemakers)
- **Rubber chemicals:** Latex, accelerators (gloves, PPE)
- **Plants:** Tulip bulbs, primrose (gardeners, florists)
- **Resins:** Epoxy resins (glues, adhesives)

**CLINICAL FEATURES:**
- **Erythema:** Redness (backs of hands, fingers, finger webs)
- **Vesiculation:** Blisters (acute phase)
- **Scaling:** Dry, scaly skin (chronic phase)
- **Fissuring:** Cracks (painful, risk of infection)
- **Itch:** Pruritus (often severe)

**DIAGNOSIS:**

**Clinical diagnosis:** Based on history and examination

**History:**
- **Work exposure:** Wet work, chemical exposure, glove use
- **Timing:** Worse at work, better on weekends/holidays
- **Duration:** Acute (recent onset) or chronic (longstanding)

**Examination:**
- **Distribution:** Hands (palms, backs of hands, fingers, finger webs), wrists, forearms
- **Appearance:** Acute (vesicles, erythema, oedema) or chronic (lichenification, hyperkeratosis, fissuring)

**Patch testing:**
- **Indication:** If allergic contact dermatitis suspected (chronic, not improving despite avoidance)
- **Procedure:** Apply allergens to back under occlusion, remove at 48 hours, read at 48 and 96 hours
- **Common allergens:** Nickel, chromate, rubber chemicals, fragrance, preservatives

**MANAGEMENT:**

**1. AVOIDANCE:**
- **Identify allergen/irritant:** Patch testing, work exposure assessment
- **Substitution:** Replace irritants/allergens with less hazardous alternatives
- **Protection:** Gloves (nitrile gloves, not latex if latex allergy), barrier creams

**2. SKIN CARE:**
- **Emollients:** Regular use (2-3 times daily), especially after hand washing
  - **Ointments:** Most effective (greasier, more moisturising) - e.g., white soft paraffin, 50% white soft paraffin/50% liquid paraffin
  - **Creams:** Less greasy - e.g., aqueous cream, moisturising cream
  - **Lotions:** Least moisturising (good for hairy areas)
- **Soap substitutes:** Use emollient as soap substitute (e.g., aqueous cream, emulsifying ointment)
- **Hand washing:** Use lukewarm water, pat dry (don't rub), apply emollient immediately after washing

**3. TOPICAL CORTICOSTEROIDS:**
- **Mild:** Hydrocortisone 1% cream BD (face, neck)
- **Moderate:** Clobetasone butyrate 0.05% cream BD (body, hands)
- **Potent:** Betamethasone valerate 0.1% cream OD (severe, thickened skin)
- **Very potent:** Clobetasol propionate 0.05% ointment OD (severe, lichenified skin)

**4. ORAL AGENTS:**
- **Antihistamine:** Cetirizine 10 mg nocte (if allergic contact dermatitis)
- **Antibiotics:** Flucloxacillin 500 mg QDS (if secondary infection)
- **Alitretinoin:** For severe chronic hand eczema (specialist initiation)

**5. WORK MODIFICATION:**
- **Reduce exposure:** Less frequent hand washing, use gloves, avoid irritants
- **Job modification:** Different duties (if exposure unavoidable)
- **Retraining:** New skills for different job (if unable to continue in current job)

**PROGNOSIS:**
- **Early intervention:** Better prognosis (may resolve with avoidance)
- **Chronic disease:** Worse prognosis (may persist despite avoidance, especially if allergic contact dermatitis)

**PREVENTION:**
- **Health surveillance:** Regular skin checks for at-risk workers (wet work, chemical exposure)
- **Education:** Skin care training, proper use of PPE, early reporting of skin problems
- **Workplace assessment:** Identify and control hazards (substitution, engineering controls)

**Sources:** HSE Guidelines, BAD Guidelines, BOHRF Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "BAD Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_noise_induced_hearing_loss(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Noise-induced hearing loss diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**NOISE-INDUCED HEARING LOSS (NIHL)**

**DEFINITION:**
Permanent hearing loss due to prolonged exposure to loud noise in the workplace.

**RISK FACTORS:**

**Noise intensity:**
- **<80 dB(A):** Low risk
- **80-85 dB(A):** Action level (lower exposure action value)
- **85 dB(A):** Action level (upper exposure action value)
- **>85 dB(A):** High risk (mandatory hearing protection)

**Noise duration:**
- **8 hours at 85 dB(A):** First action level (mandatory hearing protection)
- **<8 hours:** Higher exposure levels permitted for shorter durations (e.g., 88 dB(A) for 4 hours)

**High-risk industries:**
- **Construction:** Use of power tools, heavy machinery
- **Manufacturing:** Textile mills, metalworking, bottling lines
- **Transportation:** Rail, aviation, military
- **Entertainment:** Music industry, nightclubs, bars

**CLINICAL FEATURES:**

**Symptoms:**
- **Hearing loss:** Bilateral, symmetrical, sensorineural (high-frequency hearing loss first)
- **Tinnitus:** Ringing in ears (persistent or intermittent)
- **Difficulty:** Speech discrimination in noisy environments (cocktail party effect)

**Audiometry findings:**
- **High-frequency hearing loss:** 4 kHz dip (early), 6 kHz dip (later)
- **Sensorineural loss:** Bone conduction = air conduction (both reduced)
- **Bilateral:** Both ears affected (similar degree)

**DIAGNOSIS:**

**Audiometry:** Pure tone audiogram (0.5, 1, 2, 3, 4, 6, 8 kHz)
- **Normal:** ≤20 dB HL at all frequencies
- **Mild hearing loss:** 21-40 dB HL
- **Moderate hearing loss:** 41-70 dB HL
- **Severe hearing loss:** 71-90 dB HL
- **Profound hearing loss:** >90 dB HL

**Tympanometry:** Normal tympanogram (Type A) (rules out middle ear pathology)

**Speech audiometry:** Speech discrimination score (reduced speech discrimination in noise)

**MANAGEMENT:**

**1. PREVENTION (FURTHER HEARING LOSS):**
- **Remove from noise:** Permanent removal from hazardous noise exposure
- **Hearing protection:** Earmuffs or earplugs (use correctly, proper fit)
- **Engineering controls:** Reduce noise at source (enclosure, maintenance, quieter machinery)
- **Administrative controls:** Limit exposure time, job rotation

**2. HEARING AIDS:**
- **Indication:** Hearing loss affecting communication, work, social activities
- **Types:** Behind-the-ear (BTE), in-the-ear (ITE), receiver-in-the-canal (RIC)
- **Fitting:** Audiologist assessment, hearing aid mould (ear impression), hearing aid programming
- **Trial:** 4-6 week trial (to assess benefit)

**3. ASSISTIVE DEVICES:**
- ** amplified telephones:** Volume control, tone control
- **Loop systems:** Induction loop (hearing aid compatible)
- **Alerting devices:** Visual alarms (smoke detector, doorbell, alarm clock)
- **Communication strategies:** Lip-reading, sign language (if severe hearing loss)

**4. TINNITUS MANAGEMENT:**
- **Sound enrichment:** White noise, environmental sounds (reduce tinnitus perception)
- **Relaxation techniques:** Stress management (stress exacerbates tinnitus)
- **Hearing aids:** If hearing loss present (amplification reduces tinnitus)
- **Tinnitus retraining therapy (TRT):** Cognitive behavioural therapy (CBT) + sound enrichment

**5. COMMUNICATION STRATEGIES:**
- **Face speaker:** Lip-reading, visual cues
- **Reduce background noise:** Quiet environment for conversation
- **Ask for repetition:** If didn't hear or understand
- **Confirm understanding:** Repeat back important information

**PROGNOSIS:**
- **Permanent:** Noise-induced hearing loss is permanent (no recovery)
- **Progression:** Continues to progress if noise exposure continues (stabilises if removed from noise)
- **Prevention:** Early intervention (hearing protection) prevents progression

**COMPENSATION:**

**Industrial Injuries Disablement Benefit (IIDB):**
- **Prescribed disease:** Occupational deafness (Disease PD D1)
- **Eligibility:** Work in specified occupation (e.g., boilermaker, cauler, forgeman), ≥10 years exposure, significant hearing loss
- **Assessment:** Disablement assessment (percentage disability)

**Civil claim:**
- **Negligence:** Employer failed to provide safe workplace (hearing protection, noise control)
- **Limitation:** 3 years from date of knowledge of hearing loss and attribution to work

**PREVENTION:**

**Health surveillance:**
- **Audiometry:** Annual hearing test for workers exposed to ≥85 dB(A)
- **Fitness for work:** If hearing loss detected, refer to occupational health
- **Record-keeping:** Keep health records for 40 years after last exposure

**Noise control:**
- **Elimination:** Eliminate noise source (e.g., replace noisy machinery)
- **Substitution:** Replace with quieter machinery
- **Engineering controls:** Enclosure, maintenance, vibration damping
- **Administrative controls:** Limit exposure time, job rotation
- **Hearing protection:** Last resort (earmuffs or earplugs)

**Sources:** HSE Guidelines, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_havs(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Hand-arm vibration syndrome (HAVS) diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**HAND-ARM VIBRATION SYNDROME (HAVS)**

**DEFINITION:**
Group of conditions caused by prolonged use of vibrating tools or machinery.

**COMPONENTS:**

**1. VASCULAR (Vibration White Finger - VWF):**
- **Symptoms:** Fingers turn white (blanching) triggered by cold or damp
- **Progression:** White → Blue (cyanosis) → Red (recovery) (Raynaud's phenomenon)
- **Severity:** Mild (occasional blanching) to severe (frequent blanching, finger numbness)

**2. NEUROLOGICAL:**
- **Symptoms:** Numbness, tingling, reduced sensation (fine touch, proprioception, temperature)
- **Distribution:** Tips of fingers (usually thumb, index, middle fingers first)
- **Progression:** Worse with continued vibration exposure

**3. MUSCULOSKELETAL:**
- **Symptoms:** Grip weakness, reduced dexterity, pain
- **Causes:** Muscle weakness, tendonitis, tenosynovitis, carpal tunnel syndrome

**VIBRATING TOOLS:**

**High-risk tools:**
- **Chainsaws, brush cutters:** Forestry, landscaping
- **Breakers, pneumatic drills:** Construction, demolition
- **Grinders, Sanders:** Metalworking, woodworking
- **Riveters, impact wrenches:** Automotive, manufacturing

**Risk factors:**
- **Vibration magnitude:** Higher acceleration (m/s²) = higher risk
- **Duration of use:** Hours per day, years of exposure
- **Temperature:** Cold/damp environment (exacerbates vascular symptoms)

**DIAGNOSIS:**

**Clinical features:**
- **History:** Prolonged use of vibrating tools (usually months to years)
- **Symptoms:** White finger (VWF), numbness, tingling, grip weakness
- **Timing:** Worse at work, improves on weekends/holidays (early stages)

**Examination:**
- **Vascular:** Blanching test (triggered by cold water immersion or cold air), capillary refill time
- **Neurological:** Semmes-Weinstein monofilament testing (sensory testing), two-point discrimination, grip strength (dynamometer), dexterity (Purdue pegboard test)
- **Musculoskeletal:** Grip strength, range of movements, carpal tunnel provocation tests (Tinel's sign, Phalen's test)

**Investigations:**
- **Cold provocation test:** Finger blanching triggered by cold water (5°C) or cold air (10°C)
- **Thermography:** Assess temperature recovery after cold challenge
- **Nerve conduction studies:** If carpal tunnel syndrome suspected

**HAVS STAGING (Stockholm Workshop Scale):**

**Vascular staging:**
- **Stage 0:** No symptoms
- **Stage 1:** Occasional attacks affecting only tips of fingers
- **Stage 2:** Occasional attacks affecting distal and middle phalanges
- **Stage 3:** Frequent attacks affecting all phalanges
- **Stage 4:** Severe attacks, skin changes (trophic changes, ulcers)

**Neurological staging:**
- **Stage 0SN:** No symptoms
- **Stage 1SN:** Intermittent numbness, tingling
- **Stage 2SN:** Reduced sensation, fine touch affected
- **Stage 3SN:** Reduced sensation, proprioception affected, grip weakness

**MANAGEMENT:**

**1. REMOVE FROM EXPOSURE:**
- **Cease vibration exposure:** Essential to prevent progression
- **Job modification:** Different duties (if possible)
- **Retraining:** New skills for different job (if unable to continue in current job)

**2. VASCULAR SYMPTOMS (VWF) MANAGEMENT:**
- **Keep hands warm:** Gloves (thermal, insulated), hand warmers, avoid cold/damp environments
- **Smoking cessation:** Smoking exacerbates vasoconstriction (cessation improves symptoms)
- **Medications:** Calcium channel blocker (nifedipine 10 mg TDS) if severe (vasodilator)
- **Avoid vasoconstrictors:** Caffeine, beta-blockers, decongestants

**3. NEUROLOGICAL SYMPTOMS MANAGEMENT:**
- **Sensory re-education:** Desensitisation (rubbing, tapping, texture exercises)
- **Grip exercises:** Strengthening exercises (theraputty, hand grippers)
- **Dexterity exercises:** Fine motor skills training (Purdue pegboard, puzzles, craft activities)
- **Protection:** Avoid trauma, cuts, burns (reduced sensation → injury risk)

**4. MUSCULOSKELETAL SYMPTOMS MANAGEMENT:**
- **Strengthening exercises:** Grip strengthening, forearm strengthening
- **Stretching exercises:** Wrist flexor/extensor stretches
- **Ergonomic assessment:** Workstation assessment, tool modification
- **Pain management:** Analgesia (paracetamol, NSAID), physiotherapy

**PROGNOSIS:**
- **Early stage:** May improve if removed from exposure (especially neurological symptoms)
- **Late stage:** Permanent (vascular symptoms especially persist, may progress despite removal)

**PREVENTION:**

**Health surveillance:**
- **Annual assessment:** HAVS questionnaire, vascular and neurological examination
- **Fitness for work:** If HAVS detected, refer to occupational health
- **Record-keeping:** Keep health records for 40 years after last exposure

**Vibration control:**
- **Elimination:** Replace vibrating tools with non-vibrating alternatives
- **Substitution:** Use low-vibration tools (lower acceleration)
- **Engineering controls:** Tool maintenance (reduces vibration), anti-vibration handles, tool balancer
- **Administrative controls:** Limit exposure time (breaks, job rotation)
- **Personal protective equipment:** Anti-vibration gloves (limited protection, last resort)

**COMPENSATION:**

**Industrial Injuries Disablement Benefit (IIDB):**
- **Prescribed disease:** Vibration white finger (Disease PD D2)
- **Eligibility:** Work in specified occupation (e.g., caulker, boiler scaler, metal grinder), ≥10 years exposure
- **Assessment:** Disablement assessment (percentage disability)

**Civil claim:**
- **Negligence:** Employer failed to provide safe workplace (vibration control, health surveillance)
- **Limitation:** 3 years from date of knowledge of HAVS and attribution to work

**Sources:** HSE Guidelines, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_asbestos_diseases(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Asbestos-related diseases diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**ASBESTOS-RELATED DISEASES**

**ASBESTOS EXPOSURE:**

**High-risk industries:**
- **Construction:** Demolition, renovation, insulation work
- **Shipbuilding:** Shipbuilding, ship repair, dockyards
- **Manufacturing:** Asbestos cement, asbestos textiles, asbestos insulation
- **Engineering:** Pipe fitters, laggers, boiler makers
- **Firefighting:** Asbestos-containing materials (ACMs) in buildings

**Asbestos types:**
- **Chrysotile (white asbestos):** Most common (curly fibres, less pathogenic)
- **Amosite (brown asbestos):** Straight fibres, more pathogenic
- **Crocidolite (blue asbestos):** Straight fibres, most pathogenic

**ASBESTOS-RELATED DISEASES:**

**1. PLEURAL PLAQUES:**
- **Pathology:** Localised areas of fibrosis in parietal pleura
- **Symptoms:** Asymptomatic (incidental finding on CXR)
- **CXR:** Well-defined areas of pleural thickening (calcified or non-calcified)
- **Significance:** Marker of asbestos exposure (not benign - increased risk of lung cancer)

**2. PLEURAL EFFUSION:**
- **Pathology:** Benign asbestos-related pleural effusion
- **Symptoms:** Dyspnoea, chest pain (may be asymptomatic)
- **CXR:** Unilateral or bilateral pleural effusion
- **Management:** Aspirate (diagnostic), exclude malignancy (cytology, pleural biopsy), resolves spontaneously over months

**3. DIFFUSE PLEURAL THICKENING:**
- **Pathology:** Extensive pleural fibrosis (visceral pleura)
- **Symptoms:** Dyspnoea, reduced exercise tolerance
- **CXR:** Diffuse pleural thickening (>50% chest wall), costophrenic angle blunting
- **Prognosis:** Progressive (no specific treatment), respiratory impairment

**4. ROUNDED ATELECTASIS:**
- **Pathology:** Folded lung with pleural fibrosis
- **Symptoms:** Asymptomatic (incidental finding on CXR)
- **CXR:** Rounded mass-like opacity (mimics lung cancer)
- **CT diagnosis:** Comet tail sign (curved bronchovascular bundles entering lesion)
- **Management:** Excludes malignancy (no treatment required)

**5. ASBESTOSIS:**
- **Pathology:** Pulmonary fibrosis (lower zones, basal predominance)
- **Symptoms:** Progressive dyspnoea, dry cough, reduced exercise tolerance
- **CXR:** Irregular reticulonodular opacities (lower zones), pleural plaques
- **CT:** Interlobular septal thickening, parenchymal bands, honeycombing (late)
- **Pulmonary function tests:** Restrictive pattern (reduced TLC, reduced DLCO)
- **Prognosis:** Progressive (median survival 10-20 years from diagnosis)

**6. MESOTHELIOMA:**
- **Pathology:** Malignant tumour of pleura (or peritoneum, pericardium, tunica vaginalis)
- **Risk:** 20-40 years latency (from asbestos exposure)
- **Symptoms:** Chest pain, dyspnoea, weight loss, night sweats
- **CXR:** Pleural mass, pleural effusion, pleural thickening (encases lung)
- **CT:** Pleural thickening/nodularity, pleural effusion, chest wall invasion
- **Diagnosis:** Image-guided biopsy (CT-guided or thoracoscopic), immunohistochemistry (calretinin, WT-1 positive)
- **Prognosis:** Poor (median survival 12 months from diagnosis)

**7. LUNG CANCER:**
- **Risk:** Asbestos exposure increases risk (bronchogenic carcinoma, adenocarcinoma)
- **Synergism:** Smoking + asbestos exposure = 50-90 times increased risk
- **Symptoms:** Cough, haemoptysis, weight loss, dyspnoea
- **CXR/CT:** Lung mass, mediastinal lymphadenopathy
- **Diagnosis:** Biopsy (bronchoscopy, CT-guided), staging (CT, PET-CT, brain MRI)
- **Prognosis:** Dependent on stage (surgery if early stage, palliative if late stage)

**DIAGNOSIS:**

**History:**
- **Asbestos exposure:** Occupation, duration of exposure, years since first exposure
- **Smoking history:** Pack-years, current smoker/ex-smoker/never-smoker

**Imaging:**
- **CXR:** Initial investigation (pleural plaques, pleural effusion, pleural thickening, lung mass)
- **CT:** High-resolution CT (HRCT) for asbestos-related lung disease, CT with contrast for suspected lung cancer or mesothelioma

**Pulmonary function tests:**
- **Spirometry:** FEV1, FVC, FEV1/FVC ratio
- **Lung volumes:** TLC, RV, FRC (restrictive pattern in asbestosis, diffuse pleural thickening)
- **TLCO/DCO:** Carbon monoxide transfer factor (reduced in asbestosis, mesothelioma, lung cancer)

**Biopsy:**
- **Indication:** Suspected mesothelioma (pleural biopsy), suspected lung cancer (bronchoscopic or CT-guided biopsy)
- **Immunohistochemistry:** Mesothelioma (calretinin, WT-1, D2-40 positive; CEA, TTF-1 negative)

**MANAGEMENT:**

**Asbestosis:**
- **Remove from asbestos exposure:** Essential (prevent further disease progression)
- **Smoking cessation:** Reduces risk of lung cancer (critical intervention)
- **Vaccination:** Annual influenza vaccination, one-off pneumococcal vaccination (PPV23)
- **Oxygen:** If hypoxic (SpO₂ <92% on room air)
- **Pulmonary rehabilitation:** Exercise training, education, self-management

**Mesothelioma:**
- **Multidisciplinary team (MDT):** Oncologist, respiratory physician, thoracic surgeon, palliative care
- **Chemotherapy:** Pemetrexed + cisplatin (first-line), immunotherapy (nivolumab + ipilimumab) (second-line)
- **Radiotherapy:** Palliative radiotherapy (pain control)
- **Surgery:** Radical surgery (extrapleural pneumonectomy) - highly selected patients only
- **Palliative care:** Symptom control (pain, dyspnoea), psychosocial support, end-of-life care

**Lung cancer:**
- **Multidisciplinary team (MDT):** Oncologist, respiratory physician, thoracic surgeon, radiologist, pathologist
- **Surgery:** Lobectomy (if early stage, fit for surgery)
- **Radiotherapy:** Radical radiotherapy (if unfit for surgery), stereotactic ablative body radiotherapy (SABR) for peripheral tumours
- **Chemotherapy:** Platinum-based chemotherapy (cisplatin + pemetrexed, carboplatin + paclitaxel)
- **Immunotherapy:** Checkpoint inhibitors (nivolumab, pembrolizumab) (if high PD-L1 expression)
- **Palliative care:** Symptom control, psychosocial support, end-of-life care

**COMPENSATION:**

**Industrial Injuries Disablement Benefit (IIDB):**
- **Prescribed diseases:**
  - **PD D1:** Asbestosis
  - **PD D3:** Mesothelioma
  - **PD D8:** Lung cancer (if asbestosis also present, or asbestos exposure equivalent to 20 years at occupational level)
- **Eligibility:** Evidence of asbestos exposure (occupational history), diagnosis of prescribed disease
- **Assessment:** Disablement assessment (percentage disability)

**Civil claim:**
- **Negligence:** Employer failed to provide safe workplace (asbestos exposure, lack of protective equipment)
- **Limitation:** 3 years from date of knowledge of diagnosis and attribution to asbestos exposure (or 20 years from date of knowledge of asbestos exposure, whichever is later)

**PREVENTION:**

**Asbestos survey:**
- ** asbestos survey:** Identify asbestos-containing materials (ACMs) in workplace
- **Asbestos register:** Record location, type, condition of ACMs

**Asbestos management:**
- **Encapsulation:** Seal asbestos (paint over, enclose)
- **Enclosure:** Enclose asbestos (boxed-in, sealed)
- **Removal:** Licensed asbestos removal contractor (last resort)

**Personal protective equipment (PPE):**
- **Respiratory protection:** FFP3 mask (if asbestos exposure unavoidable)
- **Disposable coveralls:** Prevent contamination of personal clothing
- **Training:** Asbestos awareness training (identify asbestos, avoid exposure)

**Health surveillance:**
- **Medical surveillance:** Annual respiratory questionnaire and lung function testing for at-risk workers
- **Record-keeping:** Keep health records for 40 years after last exposure

**Sources:** HSE Guidelines, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_work_related_stress(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Work-related stress diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**WORK-RELATED STRESS**

**DEFINITION:**
Harmful reaction people have to undue pressures and demands placed on them at work.

**RISK FACTORS:**

**Workplace hazards:**
- **Excessive workload:** Unrealistic deadlines, too much work, lack of resources
- **Lack of control:** Lack of autonomy in how work is done
- **Poor support:** Lack of managerial support, lack of peer support
- **Poor relationships:** Bullying, harassment, conflict at work
- **Unclear role:** Unclear job description, conflicting roles
- **Organisational change:** Restructuring, redundancy, job insecurity

**Individual factors:**
- **Personality:** Perfectionism, Type A personality, high achievers
- **Coping skills:** Poor coping strategies, lack of resilience
- **Work-life balance:** Long working hours, lack of time off

**SYMPTOMS:**

**Physical:**
- **Fatigue:** Exhaustion, lethargy, poor sleep
- **Gastrointestinal:** Abdominal pain, diarrhoea, constipation, nausea
- **Cardiovascular:** Palpitations, chest pain, hypertension
- **Musculoskeletal:** Headache, back pain, muscle tension
- **Immune system:** Frequent infections (due to stress-induced immunosuppression)

**Psychological:**
- **Emotional:** Irritability, anxiety, depression, mood swings, tearfulness
- **Cognitive:** Poor concentration, memory problems, indecisiveness, reduced productivity
- **Behavioural:** Withdrawal, absenteeism, presenteeism (at work but not productive)

**DIAGNOSIS:**

**Clinical interview:**
- **Work stressors:** Identify workplace hazards causing stress
- **Symptoms:** Physical, psychological, behavioural symptoms
- **Timing:** Worse at work, improves on weekends/holidays
- **Impact:** Work performance, relationships, health

**Screening tools:**
- **HSE Management Standards Indicator:** Assess workplace stressors
- **Work-related stress questionnaire:** Identify specific stressors

**MANAGEMENT:**

**1. WORKPLACE INTERVENTIONS:**
- **Address work stressors:** Reduce workload, improve support, clarify role, improve relationships
- **Workplace adjustments:** Flexible working hours, job modification, redeployment
- **Management training:** Stress management, mental health awareness training
- **Organisational change:** Improve workplace culture, address bullying/harassment

**2. INDIVIDUAL INTERVENTIONS:**
- **Stress management:** Relaxation techniques (deep breathing, progressive muscle relaxation), mindfulness-based stress reduction (MBSR), cognitive behavioural therapy (CBT)
- **Lifestyle modifications:** Regular exercise, balanced diet, adequate sleep, reduce caffeine/alcohol
- **Social support:** Talk to family, friends, colleagues, trade union representative
- **Professional help:** Counselling, psychotherapy, psychiatric referral (if severe)

**3. SICKNESS CERTIFICATION:**
- **Statutory sick pay (SSP):** Up to 28 weeks (if eligible)
- **Fit note:** Statement of fitness for work (may recommend reduced hours, modified duties, phased return)
- **Occupational health referral:** Work-related stress assessment, workplace adjustments

**4. MEDICATION (if anxiety/depression):**
- **Mild anxiety:** Self-help, stress management, CBT
- **Moderate-severe anxiety:** SSRI (e.g., sertraline 50 mg OD) + CBT
- **Mild depression:** Self-help, exercise, CBT
- **Moderate-severe depression:** SSRI (e.g., sertraline 50 mg OD) + CBT

**PROGNOSIS:**
- **Early intervention:** Good prognosis (if workplace stressors addressed)
- **Chronic stress:** Poorer prognosis (burnout, depression, anxiety disorders)

**PREVENTION:**

**Workplace risk assessment:**
- **HSE Management Standards:** Six key areas of work design (demands, control, support, relationships, role, change)
- **Stress risk assessment:** Identify stressors, assess risk, implement control measures
- **Regular review:** Monitor stress levels, review control measures

**Employee support:**
- **EAP (Employee Assistance Programme):** Confidential counselling service
- **Mental health training:** Mental health awareness, stress management training
- **Health promotion:** Stress management workshops, resilience training

**LEGAL DUTIES:**

**Employer duties:**
- **Health and Safety at Work etc. Act 1974:** Duty of care to protect employees from work-related stress
- **Management of Health and Safety at Work Regulations 1999:** Risk assessment for stress (HSE Management Standards)
- **Equality Act 2010:** Duty to make reasonable adjustments for disability (depression, anxiety may be disability)

**Employee rights:**
- **Report concerns:** Raise concerns with manager, HR, trade union representative
- **Fit note:** Obtain fit note from GP (may recommend reduced hours, modified duties)
- **Legal action:** Constructive dismissal, unfair dismissal, discrimination (if employer fails to address stress)

**Sources:** HSE Guidelines, FOM Guidelines, NICE Guidelines (NG205)""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "NICE Guidelines (NG205)"]
            }
        )

    def _handle_rsi(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Repetitive strain injury (RSI) diagnosis and management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**REPETITIVE STRAIN INJURY (RSI) / WORK-RELATED UPPER LIMB DISORDER (WRULD)**

**DEFINITION:**
Work-related musculoskeletal disorder affecting upper limbs (neck, shoulder, arm, elbow, forearm, wrist, hand) due to repetitive movements, forceful exertions, awkward postures.

**RISK FACTORS:**

**Workplace hazards:**
- **Repetitive movements:** Typing, assembly line work, cashier work, food processing
- **Forceful exertions:** Heavy lifting, forceful gripping, using vibrating tools
- **Awkward postures:** Neck flexion, wrist deviation, shoulder abduction, arm elevation
- **Static loading:** Prolonged sitting/standing, holding same posture for long periods
- **Inadequate rest breaks:** No breaks, insufficient recovery time

**High-risk occupations:**
- **Office workers:** Typing, computer use (mouse, keyboard)
- **Assembly line workers:** Repetitive tasks, fast-paced work
- **Cashiers:** Scanning, lifting, bagging groceries
- **Musicians:** Playing instruments (piano, guitar, violin)
- **Sportspeople:** Racket sports (tennis, badminton), golf

**CLINICAL FEATURES:**

**Symptoms:**
- **Pain:** Localised pain (neck, shoulder, arm, elbow, forearm, wrist, hand)
- **Stiffness:** Joint stiffness, reduced range of movement
- **Weakness:** Reduced grip strength, weakness, fatigue
- **Paraesthesia:** Numbness, tingling (nerve compression - carpal tunnel syndrome)
- **Worse at work:** Symptoms worse at work, improve on weekends/holidays

**COMMON CONDITIONS:**

**1. CARPAL TUNNEL SYNDROME:**
- **Anatomy:** Median nerve compression at wrist (carpal tunnel)
- **Symptoms:** Numbness, tingling, pain in thumb, index, middle fingers (worse at night)
- **Signs:** Thenar eminence weakness, Tinel's sign (tapping wrist elicits symptoms), Phalen's test (wrist flexion elicits symptoms)
- **Work-related:** Repetitive wrist movements, typing, assembly work

**2. TENNIS ELBOW (LATERAL EPICONDYLITIS):**
- **Anatomy:** Common extensor origin inflammation (lateral elbow)
- **Symptoms:** Lateral elbow pain, gripping weakness, point tenderness (lateral epicondyle)
- **Signs:** Pain on resisted wrist extension, Cozen's test (pain on resisted wrist extension)
- **Work-related:** Repetitive wrist extension, gripping, screwdriver use

**3. GOLFER'S ELBOW (MEDIAL EPICONDYLITIS):**
- **Anatomy:** Common flexor origin inflammation (medial elbow)
- **Symptoms:** Medial elbow pain, gripping weakness, point tenderness (medial epicondyle)
- **Signs:** Pain on resisted wrist flexion
- **Work-related:** Repetitive wrist flexion, gripping, throwing sports

**4. ROTATOR CUFF TENDINOPATHY:**
- **Anatomy:** Supraspinatus, infraspinatus, teres minor, subscapularis tendons (shoulder)
- **Symptoms:** Shoulder pain, weakness (especially overhead activities), night pain
- **Signs:** Painful arc (60-120° abduction), drop arm test, external rotation weakness
- **Work-related:** Repetitive overhead activities (painting, assembly work)

**5. DE QUERVAIN'S TENOSYNOVITIS:**
- **Anatomy:** Abductor pollicis longus and extensor pollicis brevis tendons (first dorsal compartment)
- **Symptoms:** Radial wrist pain, thumb pain, swelling, crepitus
- **Signs:** Finkelstein's test (pain on ulnar deviation of wrist with thumb flexed)
- **Work-related:** Repetitive thumb movements, pinching, grasping

**DIAGNOSIS:**

**Clinical diagnosis:** Based on history and examination

**History:**
- **Work exposure:** Repetitive movements, forceful exertions, awkward postures
- **Symptoms:** Pain, stiffness, weakness, paraesthesia
- **Timing:** Worse at work, improves on weekends/holidays (early stages)

**Examination:**
- **Inspection:** Swelling, redness, deformity
- **Palpation:** Point tenderness
- **Range of movement:** Active and passive ROM (reduce if painful)
- **Strength:** Grip strength (dynamometer), resisted movements (identify tendinopathy)
- **Neurological:** Sensory testing (light touch, pinprick), reflexes
- **Special tests:** Condition-specific tests (e.g., Tinel's sign, Phalen's test, Finkelstein's test)

**Investigations:**
- **X-ray:** Exclude fracture, arthritis, calcific tendinopathy
- **Ultrasound:** Tendon pathology, inflammation, tears
- **Nerve conduction studies:** If nerve compression suspected (carpal tunnel syndrome)

**MANAGEMENT:**

**1. WORKPLACE MODIFICATIONS:**
- **Ergonomic assessment:** Workstation assessment (desk, chair, monitor, keyboard, mouse)
- **Reduce repetition:** Job rotation, task variation
- **Reduce force:** Mechanical aids, powered tools
- **Improve posture:** Adjustable chair, monitor at eye level, neutral wrist position (typing)
- **Rest breaks:** Regular breaks (e.g., 5 minutes every hour), microbreaks (30 seconds every 10 minutes)

**2. EXERCISE THERAPY:**
- **Stretching exercises:** Stretch affected muscles (3-5 times daily)
- **Strengthening exercises:** Eccentric exercises (e.g., Alfredson protocol for Achilles tendinopathy, Tyler twist for tennis elbow)
- **Neural mobilisation:** Nerve gliding exercises (if nerve compression)
- **Posture exercises:** Scapular stabilisation exercises, postural taping

**3. MANUAL THERAPY:**
- **Soft tissue massage:** Myofascial release, trigger point release
- **Joint mobilisations:** Maitland, Mulligan techniques
- **Acupuncture:** May provide pain relief (controversial evidence)

**4. ELECTROTHERAPY:**
- **TENS:** Transcutaneous electrical nerve stimulation (pain relief)
- **Ultrasound therapy:** Tissue healing (controversial evidence)
- **Low-level laser therapy (LLLT):** Tissue healing (controversial evidence)

**5. MEDICATION:**
- **Analgesia:** Paracetamol 1 g QDS PRN, NSAID (ibuprofen 400 mg TDS PRN) if appropriate
- **Neuropathic pain agents:** Gabapentin 300 mg TDS, pregabalin 75 mg BD (if nerve compression)

**6. INJECTIONS:**
- **Corticosteroid injection:** Local injection around affected tendon (short-term pain relief, guide physiotherapy)
- **Platelet-rich plasma (PRP):** Autologous blood product (inconclusive evidence)

**7. SURGERY:**
- **Carpal tunnel release:** Indicated if severe symptoms, failing conservative treatment (EMG confirmed)
- **Rotator cuff repair:** Indicated if complete tear, young patient, functional deficit
- **Tennis elbow release:** Indicated if severe symptoms, failing conservative treatment (rare)

**PROGNOSIS:**
- **Early intervention:** Good prognosis (if workplace modifications implemented)
- **Chronic disease:** Poorer prognosis (may persist despite treatment)

**PREVENTION:**

**Workplace risk assessment:**
- **Display screen equipment (DSE) assessment:** Ergonomic workstation (monitor at eye level, neutral wrist position, adjustable chair)
- **Manual handling risk assessment:** Assess lifting, carrying, pushing, pulling tasks
- **Job rotation:** Rotate tasks to reduce repetitive strain
- **Training:** Manual handling training, DSE assessor training

**Employee training:**
- **Ergonomic training:** Proper posture, neutral position, workstation setup
- **Breaks:** Regular rest breaks, microbreaks
- **Stretching:** Regular stretching exercises (desk stretches)
- **Report early:** Report symptoms early (prevents progression)

**Sources:** HSE Guidelines, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_fitness_for_work(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Fitness for work and sickness absence management"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**FITNESS FOR WORK AND SICKNESS ABSENCE MANAGEMENT**

**FITNESS FOR WORK ASSESSMENT:**

**Definition:**
Assessment of whether employee is fit to return to work (current role or modified duties) following sickness absence.

**Principles:**
- **Work is good for health:** Promotes recovery, prevents deconditioning, maintains social contact
- **Fit note:** Statement of fitness for work (formerly sick note) - GP or specialist
- **Employer duties:** Make reasonable adjustments for disability, support return to work

**FIT NOTE (Statement of Fitness for Work):**

**Options:**
- **Fit for work:** No restrictions, can return to normal duties
- **Fit for work with restrictions:** Can return to work with adjustments (reduced hours, modified duties)
- **Not fit for work:** Not fit for any work (continue sickness absence)

**Common adjustments:**
- **Reduced hours:** Part-time hours, gradual increase (phased return)
- **Modified duties:** Lighter duties, different tasks, temporary alternative work
- **Workplace modifications:** Ergonomic assessment, equipment modifications
- **Flexible working:** Flexible start/finish times, home working
- **Support:** Additional support, training, supervision

**SICKNESS ABSENCE MANAGEMENT:**

**Short-term sickness absence (<4 weeks):**
- **Common causes:** Minor illness (cough, cold, flu), minor injury, short-term stress
- **Management:** Self-certification (first 7 days), fit note (from day 8)
- **Return to work:** Full duties expected (unless specified otherwise on fit note)

**Long-term sickness absence (>4 weeks):**
- **Common causes:** Musculoskeletal conditions (back pain, RSI), stress, anxiety, depression, chronic illness
- **Management:** Occupational health referral, fit note with adjustments, return to work plan
- **Return to work:** Phased return, graded exposure, workplace adjustments

**OCCUPATIONAL HEALTH ASSESSMENT:**

**Referral reasons:**
- **Long-term sickness absence:** >4 weeks absence (or frequent short-term absences)
- **Work-related illness:** Suspected occupational disease (occupational asthma, dermatitis, NIHL, HAVS, asbestosis)
- **Fitness for work:** Complex medical condition, require specialist assessment
- **Workplace adjustments:** Need for workplace modifications, reasonable adjustments
- **Rehabilitation:** Return to work plan, work rehabilitation

**Occupational health assessment:**
- **Medical assessment:** Diagnosis, treatment, prognosis, functional impairment
- **Workplace assessment:** Job demands, hazards, adjustments, accommodations
- **Fitness for work advice:** Fit for work (with or without restrictions), not fit for work
- **Return to work plan:** Phased return, graded exposure, workplace adjustments, review date

**RETURN TO WORK PLAN:**

**Phased return:**
- **Week 1-2:** Reduced hours (e.g., 2 hours/day, gradually increase)
- **Week 3-4:** Gradual increase in hours (e.g., 4 hours/day, then 6 hours/day)
- **Week 5+:** Full hours (return to normal duties)

**Graduated exposure:**
- **Week 1-2:** Light duties (restricted tasks)
- **Week 3-4:** Gradual reintroduction of normal duties
- **Week 5+:** Normal duties (full role)

**Workplace adjustments:**
- **Ergonomic assessment:** Workstation modifications, equipment adaptations
- **Job modification:** Temporary or permanent changes to job role
- **Support:** Additional training, supervision, mentoring

**RED FLAGS (POTENTIALLY SERIOUS CONDITIONS):**

**Imminent danger to self or others:**
- **Uncontrolled epilepsy:** Safety-critical work (driving, machinery, working at heights)
- **Uncontrolled psychiatric illness:** Suicidal ideation, psychosis, mania
- **Uncontrolled cardiovascular disease:** Recent MI, unstable angina, severe heart failure
- **Severe visual impairment:** Safety-critical work (driving, machinery)
- **Severe hearing loss:** Safety-critical work (driving, machinery, telephonist)

**SICKNESS CERTIFICATION:**

**SSP (Statutory Sick Pay):**
- **Eligibility:** Employed, earning ≥£120/week, off work for ≥4 days in a row
- **Duration:** Up to 28 weeks (if eligible)
- **Rate:** £99.35/week (2024/25 rate)

**FIT NOTE:**
- **Issued by:** GP or specialist
- **Duration:** Up to 3 months initially, can be extended
- **Options:** Fit for work (with or without restrictions), not fit for work

**Occupational health fit note:**
- **Issued by:** Occupational health physician
- **Duration:** Can be longer than GP fit note
- **Advice:** Detailed advice on fitness for work, workplace adjustments, return to work plan

**Sources:** DWP Guidelines, HSE Guidelines, FOM Guidelines, NICE Guidelines (NG223)""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["DWP Guidelines", "HSE Guidelines", "FOM Guidelines", "NICE Guidelines (NG223)"]
            }
        )

    def _handle_dse(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Display screen equipment (DSE) guidance"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**DISPLAY SCREEN EQUIPMENT (DSE) GUIDANCE**

**DEFINITION:**
Equipment with an alphanumeric or graphic display screen (including laptops, tablets, smartphones).

**DSE REGULATIONS (1992, amended 2002):**

**Employer duties:**
- **Risk assessment:** Assess DSE workstation (identify hazards, assess risks, implement control measures)
- **DSE assessment:** If employee uses DSE for >1 hour continuously or >2 hours intermittently per day
- **Provide training:** Information and training on DSE use
- **Provide eye tests:** Eye and eyesight tests on request (if DSE user)
- **Provide breaks:** Rest breaks or changes of activity

**WORKSTATION ASSESSMENT:**

**Chair:**
- **Adjustable height:** Seat height adjustable (thighs horizontal, feet flat on floor or footrest)
- **Backrest:** Adjustable backrest (lumbar support, reclined 100-110° from vertical)
- **Seat depth:** Adjustable (2-3 fingers width between front edge of seat and back of knee)
- **Armrests:** Adjustable height, width (optional, if not interfering with desk)
- **Base:** 5-point base (stability), castors (if desk is height-adjustable)

**Desk:**
- **Height:** Adjustable desk (or platform for monitor/keyboard) - elbow height when sitting
- **Depth:** Sufficient depth for monitor (arm's length away from user)
- **Width:** Sufficient width for monitor, keyboard, mouse, documents, equipment
- **Leg room:** Clear leg room under desk (no obstructions)

**Monitor:**
- **Position:** Arm's length away from user (approximately 50-70 cm), directly in front
- **Height:** Top of monitor at or slightly below eye level (neutral neck position)
- **Tilt:** Adjustable tilt (reduce glare, reflection)
- **Brightness/contrast:** Adjustable for comfort (reduce eye strain)

**Keyboard:**
- **Position:** Directly in front of user (shoulders relaxed, elbows at 90°)
- **Height:** Sloping keyboard or wrist rest (neutral wrist position)
- **Mouse:** Positioned next to keyboard (minimal reaching)

**DOCUMENT HOLDER:**
- **Position:** Between monitor and keyboard (or adjacent to monitor)
- **Type:** Adjustable angle, height (reduce neck twisting, eye strain)

**FOOTREST:**
- **Indication:** If feet not flat on floor (chair height not adjustable, or desk height not adjustable)
- **Type:** Adjustable height, angle (support feet, reduce pressure on backs of thighs)

**DSE HAZARDS:**

**Upper limb disorders:**
- **Neck pain:** Neck flexion, prolonged static posture
- **Shoulder pain:** Shoulder abduction, arm elevation (mouse use, typing)
- **Arm/elbow pain:** Repetitive movements, awkward postures
- **Wrist/hand pain:** Wrist deviation, repetitive movements (typing, mouse use)

**Eye strain:**
- **Visual fatigue:** Prolonged screen use, poor lighting, glare, reflection
- **Dry eyes:** Reduced blink rate (when looking at screen), low humidity
- **Headache:** Eye strain, neck pain, tension headache

**Fatigue:**
- **Physical fatigue:** Static posture, lack of movement
- **Mental fatigue:** Concentration, attention, decision-making

**PREVENTION:**

**Ergonomic workstation:**
- **Neutral posture:** Head balanced over neck (not flexed/extended), shoulders relaxed (not elevated), elbows at 90° (not abducted/adducted), wrists neutral (not deviated), hips slightly higher than knees (90-100°), feet flat on floor or footrest
- **Adjustable equipment:** Chair, desk, monitor, keyboard, mouse (adjust to fit user)

**Work habits:**
- **Breaks:** 5-10 minute break every hour (or microbreaks - 30 seconds every 10 minutes)
- **Task variety:** Mix DSE work with other tasks (phone calls, filing, walking)
- **Stretching exercises:** Neck stretches, shoulder shrugs, back stretches (every hour)

**Eye care:**
- **Blink regularly:** Remember to blink (reduces dry eyes)
- **20-20-20 rule:** Every 20 minutes, look at something 20 feet away for 20 seconds (reduces eye strain)
- **Eye tests:** Regular eye tests (every 2 years, or more frequently if recommended by optometrist)

**Lighting:**
- **Ambient lighting:** Sufficient ambient lighting (avoid too bright or too dark)
- **Task lighting:** Task light (for documents) if ambient lighting insufficient
- **Glare/reflection:** Reduce glare (close blinds, reposition monitor), avoid reflection (use matte screen)

**TRAINING:**
- **DSE awareness:** Training on DSE hazards, ergonomic principles, work habits
- **Workstation setup:** Practical training on setting up workstation
- **Breaks and exercises:** Importance of breaks, stretching exercises

**EMPLOYEE RESPONSIBILITIES:**
- **Cooperate:** Follow employer's DSE procedures
- **Report problems:** Report symptoms early (neck pain, arm pain, eye strain)
- **Take breaks:** Take regular breaks (as recommended)
- **Adjust workstation:** Adjust chair, desk, monitor to fit body (ergonomic setup)

**Sources:** HSE DSE Regulations, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE DSE Regulations", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )

    def _handle_general_occupational_medicine(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """General occupational medicine consultation"""

        return DomainQueryResult(
            domain_name="occupational_medicine",
            answer="""**OCCUPATIONAL MEDICINE**

Occupational medicine is a medical specialty focused on the relationship between work and health.

**CORE FUNCTIONS:**

**1. Fitness for Work:**
- **Assessment:** Determine if employee medically fit for work (current role or modified duties)
- **Fit note:** Statement of fitness for work (fit for work, fit for work with restrictions, not fit for work)
- **Return to work:** Phased return, graduated exposure, workplace adjustments

**2. Occupational Diseases:**
- **Diagnosis:** Work-related diseases (occupational asthma, dermatitis, NIHL, HAVS, asbestosis, mesothelioma, lung cancer)
- **Management:** Treatment, workplace modifications, sickness absence, benefits
- **Prevention:** Health surveillance, risk assessment, control measures

**3. Workplace Hazards:**
- **Chemical hazards:** Solvents, dusts, fumes, gases (COSHH regulations)
- **Physical hazards:** Noise, vibration, temperature, radiation, electricity
- **Biological hazards:** Infections (bacteria, viruses, fungi, parasites)
- **Ergonomic hazards:** Manual handling, repetitive movements, awkward postures, static loading
- **Psychosocial hazards:** Work-related stress, bullying, harassment, violence

**4. Health Surveillance:**
- **Purpose:** Early detection of work-related disease, monitor effectiveness of control measures
- **Required for:** Noise (≥85 dB(A)), vibration (HAVS), asbestos, respiratory sensitisers, skin sensitisers, compressed air work
- **Tests:** Respiratory questionnaire and spirometry (respiratory sensitisers), audiometry (noise), HAVS assessment (vibration), skin surveillance (dermatitis)

**5. Sickness Absence Management:**
- **Short-term:** <4 weeks (usually self-limiting, return to full duties)
- **Long-term:** >4 weeks (occupational health referral, workplace adjustments, phased return)
- **Frequent absences:** Bradford score (pattern of absences), underlying cause, management

**6. Disability and Equality:**
- **Equality Act 2010:** Duty to make reasonable adjustments for disability
- **Reasonable adjustments:** Workplace modifications, flexible working, support, equipment
- **Disability:** Physical or mental impairment with substantial and long-term adverse effect on ability to carry out normal day-to-day activities

**COMMON OCCUPATIONAL DISEASES:**

**Respiratory:**
- **Occupational asthma:** Baker's asthma, isocyanate asthma
- **Chronic obstructive pulmonary disease (COPD):** Coal workers' pneumoconiosis, silicosis
- **Asbestos-related diseases:** Asbestosis, mesothelioma, lung cancer

**Skin:**
- **Occupational dermatitis:** Hand eczema (wet work, chemical exposure)
- **Contact urticaria:** Latex allergy, food allergy

**Hearing:**
- **Noise-induced hearing loss (NIHL):** Industrial deafness
- **Tinnitus:** Ringing in ears (associated with NIHL)

**Musculoskeletal:**
- **Hand-arm vibration syndrome (HAVS):** Vibration white finger, numbness, grip weakness
- **Repetitive strain injury (RSI):** Carpal tunnel syndrome, tennis elbow, rotator cuff tendinopathy

**Cancer:**
- **Mesothelioma:** Asbestos exposure
- **Lung cancer:** Asbestos exposure, silica exposure, radon exposure
- **Skin cancer:** Sun exposure (outdoor workers)

**WORKPLACE REGULATIONS:**

**COSHH (Control of Substances Hazardous to Health):**
- **Risk assessment:** Assess hazardous substances, implement control measures
- **Heirarchy of controls:** Elimination → Substitution → Engineering controls → Administrative controls → PPE
- **Health surveillance:** For hazardous substances (respiratory sensitisers, skin sensitisers)

**RIDDOR (Reporting of Injuries, Diseases and Dangerous Occurrences):**
- **Reportable accidents:** Death, major injury, over-7-day injury
- **Reportable diseases:** Occupational diseases (Carpel tunnel syndrome, occupational dermatitis, etc.)
- **Reportable dangerous occurrences:** Collapse, overturning, explosion, accidental release

**Display Screen Equipment (DSE) Regulations:**
- **Workstation assessment:** Ergonomic assessment of chair, desk, monitor, keyboard, mouse
- **Eye tests:** Eye and eyesight tests on request
- **Breaks:** Rest breaks or changes of activity

**Manual Handling Operations Regulations:**
- **Risk assessment:** Assess manual handling tasks (lifting, carrying, pushing, pulling)
- **Hierarchy of controls:** Avoid manual handling → Assess and reduce risk → Provide training

**Sources:** HSE Guidelines, FOM Guidelines, BOHRF Guidelines""",
            confidence=0.85,
            metadata={
                "urgency": "non-urgent",
                "specialty": "occupational_medicine",
                "sources": ["HSE Guidelines", "FOM Guidelines", "BOHRF Guidelines"]
            }
        )


def create_occupational_medicine_domain():
    """Factory function for Occupational Medicine Domain"""
    return OccupationalMedicineDomain()
