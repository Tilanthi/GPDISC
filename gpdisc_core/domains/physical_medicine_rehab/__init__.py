"""
Physical Medicine & Rehabilitation Domain for GPDISC

Comprehensive physical medicine and rehabilitation domain covering all aspects of
functional recovery, disability management, and rehabilitation medicine.

Evidence-based: BSRM (British Society of Rehabilitation Medicine), ACRM,
NICE Guidelines, NHS England Rehabilitation Guidelines
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class PhysicalMedicineRehabDomain(BaseDomainModule):
    """
    Physical Medicine and Rehabilitation Domain

    Covers all aspects of rehabilitation medicine including:
    - Stroke rehabilitation
    - Musculoskeletal rehabilitation
    - Neurological rehabilitation
    - Cardiac rehabilitation
    - Pulmonary rehabilitation
    - Amputee rehabilitation
    - Spinal cord injury rehabilitation
    - Paediatric rehabilitation
    - Disability assessment and management
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="physical_medicine_rehab",
            version="1.0.0",
            dependencies=[],
            description="Physical medicine and rehabilitation - Stroke, musculoskeletal, neurological, cardiac, pulmonary, amputee, spinal cord injury rehabilitation",
            keywords=[
                # Rehabilitation
                "rehabilitation", "rehab", "physical therapy", "physiotherapy", "occupational therapy",
                "speech and language therapy", "salt", "therapy", "functional recovery",
                # Stroke rehabilitation
                "stroke rehabilitation", "hemiplegia", "hemiparesis", "aphasia",
                "dysphagia", "mobility after stroke", "arm weakness", "leg weakness",
                # Musculoskeletal
                "musculoskeletal rehabilitation", "orthopaedic rehabilitation", "fracture rehabilitation",
                "joint replacement rehab", "knee replacement rehab", "hip replacement rehab",
                "back pain rehab", "chronic pain", "whiplash", "soft tissue injury",
                # Neurological
                "neurological rehabilitation", "parkinson's rehab", "multiple sclerosis rehab",
                "guillain-barre", "gbs", "motor neuron disease", "muscular dystrophy",
                # Cardiac
                "cardiac rehabilitation", "heart attack rehab", "cardiac rehab",
                "post-mi rehab", "heart failure rehab", "cardiac surgery rehab",
                # Pulmonary
                "pulmonary rehabilitation", "copd rehab", "respiratory rehab",
                "lung rehab", "breathlessness rehab", "chronic lung disease rehab",
                # Amputee
                "amputee rehabilitation", "amputation rehab", "prosthetic training",
                "phantom limb pain", "stump pain", "below knee amputation", "above knee amputation",
                # Spinal cord injury
                "spinal cord injury rehab", "paraplegia", "tetraplegia", "quadriplegia",
                "spinal injury", "complete injury", "incomplete injury",
                # Paediatric
                "paediatric rehabilitation", "developmental delay", "cerebral palsy",
                " paediatric physiotherapy", "children's rehab",
                # Disability
                "disability assessment", "functional assessment", "mobility assessment",
                "activities of daily living", "adl", "independent living", "care needs"
            ],
            capabilities=[
                "rehabilitation_assessment", "stroke_rehabilitation", "musculoskeletal_rehab",
                "neurological_rehab", "cardiac_rehab", "pulmonary_rehab",
                "amputee_rehab", "spinal_cord_injury_rehab", "disability_assessment"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        query_lower = query.lower()

        # EMERGENCY: Spinal cord compression
        if any(term in query_lower for term in ["spinal cord compression", "cord compression",
                                                   "cauda equina syndrome", "traumatic spinal injury"]):
            return self._handle_spinal_cord_compression(query, context)

        # STROKE REHABILITATION
        if any(term in query_lower for term in ["stroke rehab", "stroke rehabilitation", "hemiplegia",
                                                   "hemiparesis", "aphasia", "dysphagia"]):
            return self._handle_stroke_rehabilitation(query, context)

        # MUSCULOSKELETAL REHABILITATION
        if any(term in query_lower for term in ["orthopaedic rehab", "joint replacement rehab",
                                                   "knee replacement", "hip replacement", "fracture rehab",
                                                   "back pain rehab", "whiplash rehab"]):
            return self._handle_musculoskeletal_rehabilitation(query, context)

        # CARDIAC REHABILITATION
        if any(term in query_lower for term in ["cardiac rehabilitation", "cardiac rehab",
                                                   "heart attack rehab", "post-mi rehab", "heart failure rehab"]):
            return self._handle_cardiac_rehabilitation(query, context)

        # PULMONARY REHABILITATION
        if any(term in query_lower for term in ["pulmonary rehabilitation", "pulmonary rehab",
                                                   "copd rehab", "respiratory rehab", "breathlessness rehab"]):
            return self._handle_pulmonary_rehabilitation(query, context)

        # NEUROLOGICAL REHABILITATION
        if any(term in query_lower for term in ["parkinson's rehab", "multiple sclerosis rehab",
                                                   "guillain-barre", "motor neuron disease",
                                                   "neurological rehab"]):
            return self._handle_neurological_rehabilitation(query, context)

        # AMPUTEE REHABILITATION
        if any(term in query_lower for term in ["amputee rehabilitation", "amputation rehab",
                                                   "prosthetic", "phantom limb", "stump pain"]):
            return self._handle_amputee_rehabilitation(query, context)

        # SPINAL CORD INJURY REHABILITATION
        if any(term in query_lower for term in ["spinal cord injury rehab", "paraplegia",
                                                   "tetraplegia", "quadriplegia", "spinal injury rehab"]):
            return self._handle_spinal_cord_injury_rehabilitation(query, context)

        # DISABILITY ASSESSMENT
        if any(term in query_lower for term in ["disability assessment", "functional assessment",
                                                   "activities of daily living", "adl", "mobility assessment",
                                                   "care needs assessment"]):
            return self._handle_disability_assessment(query, context)

        # GENERAL REHABILITATION
        else:
            return self._handle_general_rehabilitation(query, context)

    def _handle_spinal_cord_compression(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Spinal cord compression assessment"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**SPINAL CORD COMPRESSION - EMERGENCY ASSESSMENT**

**RED FLAGS (HIGH RISK OF SPINAL CORD COMPRESSION):**

**Clinical features:**
- **Progressive weakness:** Ascending weakness, difficulty walking, reduced mobility
- **Sensory changes:** Sensory level, numbness, paraesthesia, loss of sensation
- **Sphincter disturbance:** Urinary retention, constipation, faecal incontinence, loss of anal tone
- **Saddle anaesthesia:** S2-S5 dermatomes (perineum, perianal region, inner thighs)
- **Back pain:** Progressive, thoracic region, worsens with lying flat, Valsalva manoeuvre
- **Upper motor neurone signs:** Hyperreflexia, spasticity, Babinski sign, clonus

**IMMEDIATE ACTION:**

1. **URGENT MRI WHOLE SPINE** (within 24 hours of presentation)
   - **T1-weighted:** Assess tumour extent, cord compression, vertebral collapse
   - **T2-weighted:** Assess cord oedema, signal change, compression severity
   - **STIR:** Assess bone metastases, marrow infiltration, vertebral fracture

2. **NEUROSURGICAL/ORTHOPAEDIC REFERRAL** (emergency)
   - **Indications for emergency surgery:** Spinal instability, rapid neurological deterioration, unknown primary (biopsy)
   - **Indications for emergency radiotherapy:** Non-surgical candidates, radiosensitive tumour, multilevel disease

3. **DEXAMETHASONE** (if cord compression confirmed or high suspicion)
   - **High-dose dexamethasone:** 16 mg PO/IV loading dose, then 16 mg PO/IV OD
   - **Rapid taper:** After radiotherapy/surgery completion (taper over 2-3 weeks)
   - **PPI prophylaxis:** Omeprazole 20 mg OD (stress ulcer prophylaxis)

4. **BLADDER CATHETERISATION** (if urinary retention)
   - **Indwelling urinary catheter:** 12-16 Fr Foley catheter
   - **Intermittent self-catheterisation:** If appropriate (patient able, reversible cord compression)

5. **SKIN PROTECTION** (prevent pressure ulcers)
   - **Pressure-relieving mattress:** Alternating pressure mattress
   - **Regular turning:** Every 2-4 hours
   - **Skin inspection:** Daily (sacrum, heels, ischial tuberosities)

**REHABILITATION ASSESSMENT:**

**Baseline assessment:**
- **Motor function:** Muscle strength (MRC grading), functional ability (mobility, transfers)
- **Sensory function:** Light touch, pinprick, proprioception (sensory level)
- **Sphincter function:** Bladder (catheter vs. continent), bowel (constipation, incontinence)
- **Functional independence:** Barthel Index, Functional Independence Measure (FIM)

**Rehabilitation goals:**
- **Maximise independence:** Mobility, transfers, activities of daily living (ADL)
- **Prevent complications:** Pressure ulcers, DVT, UTI, constipation, contractures
- **Psychological support:** Adjustment to disability, depression, anxiety

**PROGNOSIS:**
- **Ambulant pre-treatment:** 80-90% remain ambulant
- **Non-ambulant pre-treatment:** 30-50% regain ambulation
- **Complete vs. incomplete injury:** Incomplete injury (some preserved function below level) has better prognosis

**Sources:** NICE Guidelines (NG75), BOA Guidelines, BSRM Guidelines""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG75)", "BOA Guidelines", "BSRM Guidelines"],
                "emergency_protocol": "spinal_cord_compression"
            }
        )

    def _handle_stroke_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Stroke rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**STROKE REHABILITATION**

**PRINCIPLES OF STROKE REHABILITATION:**

- **Early mobilisation:** Within 24 hours of stroke (if medically stable)
- **Intensive, repetitive, task-specific training:** Promotes neuroplasticity
- **Multidisciplinary team (MDT):** Physiotherapy, occupational therapy, speech and language therapy, psychology, nursing, medical staff
- **Goal-oriented:** Patient-centred, functional goals (SMART: Specific, Measurable, Achievable, Relevant, Time-bound)
- **Family involvement:** Education, training, support

**STROKE REHABILITATION PHASES:**

**1. ACUTE PHASE (FIRST 1-2 WEEKS):**

**Goals:**
- **Medical stabilisation:** Blood pressure control, temperature regulation, blood glucose control
- **Prevention of complications:** Aspiration pneumonia, DVT, pressure ulcers, shoulder pain, contractures
- **Early mobilisation:** Bed mobility, sitting balance, standing (if able)
- **Swallowing assessment:** Bedside swallow assessment (water test), if abnormal → videofluoroscopic swallow study (VFSS) or fibreoptic endoscopic evaluation of swallowing (FEES)

**Interventions:**
- **Positioning:** Proper positioning to prevent shoulder subluxation, contractures, pressure ulcers
- **Passive range of movement exercises:** Prevent contractures (especially affected upper limb)
- **Active-assisted exercises:** Encourage use of affected limb
- **Sensory stimulation:** Tactile, proprioceptive, visual stimulation of affected limb
- **Cognitive stimulation:** Orientation, attention, memory exercises

**2. SUBACUTE PHASE (2-12 WEEKS):**

**Goals:**
- **Maximise functional recovery:** Mobility, ADL, communication, cognition
- **Promote neuroplasticity:** Intensive, repetitive, task-specific training
- **Prevent secondary complications:** Shoulder subluxation, contractures, learned non-use

**Interventions:**
- **Mobility training:** Sit-to-stand, standing balance, walking (gait re-education)
- **Upper limb rehabilitation:** Constraint-induced movement therapy (CIMT), task-specific training, mirror therapy
- **Lower limb rehabilitation:** Treadmill training, body-weight-supported treadmill training, cycling, electrical stimulation (functional electrical stimulation - FES)
- **Communication rehabilitation:** Speech and language therapy (SALT) for aphasia, dysarthria, apraxia of speech
- **Swallowing rehabilitation:** SALT for dysphagia (dietary modification, swallowing exercises)
- **Cognitive rehabilitation:** Orientation, attention, memory, executive function exercises
- **Visual rehabilitation:** Visual field defects (hemianopia), visual neglect, visuospatial neglect

**3. CHRONIC PHASE (>12 WEEKS):**

**Goals:**
- **Maintain functional gains:** Continue exercises, prevent learned non-use
- **Promote community reintegration:** Return to work, leisure activities, driving
- **Psychological support:** Depression, anxiety, adjustment to disability

**Interventions:**
- **Continued physiotherapy:** Maintenance exercises, walking aids, orthoses (ankle-foot orthosis - AFO)
- **Occupational therapy:** ADL training, home modifications, return to work/school
- **Speech and language therapy:** Communication strategies, aphasia groups
- **Psychological support:** Counselling, cognitive behavioural therapy (CBT), support groups

**STROKE REHABILITATION INTERVENTIONS:**

**MOBILITY REHABILITATION:**
- **Early mobilisation:** Within 24 hours of stroke (if medically stable)
- **Gait re-education:** Walking practice, treadmill training (with or without body-weight support)
- **Walking aids:** Tripod stick, frame, rollator (as appropriate)
- **Orthoses:** Ankle-foot orthosis (AFO) for foot drop (if appropriate)

**UPPER LIMB REHABILITATION:**
- **Constraint-induced movement therapy (CIMT):** Restrict unaffected upper limb, intensive training of affected upper limb (2-6 hours/day for 2 weeks)
- **Task-specific training:** Repetitive practice of functional tasks (reaching, grasping, manipulation)
- **Mirror therapy:** Mirror box to create visual illusion of moving affected limb
- **Electrical stimulation:** Functional electrical stimulation (FES) to improve motor function
- **Robotic-assisted therapy:** Exoskeleton or end-effector devices for upper limb rehabilitation
- **Botulinum toxin:** For spasticity (reduce tone, improve function, prevent contractures)

**LOWER LIMB REHABILITATION:**
- **Strengthening exercises:** Hip, knee, ankle strengthening (especially affected lower limb)
- **Stretching exercises:** Prevent contractures (especially plantar flexors, hip flexors)
- **Balance training:** Standing balance, weight-shifting, perturbation training
- **Functional electrical stimulation (FES):** Foot drop stimulation (improve gait, reduce tripping)
- **Cycling:** Stationary cycling (recumbent or upright) for lower limb strengthening and cardiovascular fitness

**COMMUNICATION REHABILITATION:**
- **Aphasia rehabilitation:** Speech and language therapy (SALT) for expressive/receptive aphasia (anomia, sentence construction, comprehension)
- **Dysarthria rehabilitation:** SALT for articulation, prosody, respiration (speech exercises, rate control, augmentative and alternative communication - AAC)
- **Apraxia of speech rehabilitation:** SALT for motor planning deficits (articulatory rate control, prosodic control)

**SWALLOWING REHABILITATION:**
- **Dietary modification:** Texture-modified foods and thickened fluids (as recommended by SALT)
- **Swallowing exercises:** Tongue strengthening, exercises to improve airway protection
- **Compensatory strategies:** Chin tuck, head rotation, effortful swallow, multiple swallows, supraglottic swallow
- **Tube feeding:** Nasogastric tube (NGT) or percutaneous endoscopic gastrostomy (PEG) if severe dysphagia (inadequate oral intake)

**COGNITIVE REHABILITATION:**
- **Orientation:** Regular reorientation (time, place, person), orientation board in room
- **Attention rehabilitation:** Focused attention, sustained attention, divided attention exercises
- **Memory rehabilitation:** Memory aids (notebook, smartphone, alarms), external memory strategies
- **Executive function rehabilitation:** Problem-solving, planning, organisation exercises

**SPASTICITY MANAGEMENT:**
- **Physiotherapy:** Stretching exercises, positioning, casting/splinting
- **Oral medications:** Baclofen (10 mg TDS, titrate to effect), tizanidine (2 mg TDS, titrate to effect), dantrolene (25 mg OD, titrate to effect)
- **Botulinum toxin:** Local injection into spastic muscles (reduce tone, improve function, prevent contractures)
- **Intrathecal baclofen pump:** For severe generalised spasticity (refractory to oral medications)

**SHOULDER PAIN MANAGEMENT:**
- **Proper positioning:** Prevent shoulder subluxation (arm support in wheelchair, proper positioning in bed)
- **Passive range of movement exercises:** Prevent contractures, maintain shoulder ROM
- **Strapping/sling:** Support shoulder (if subluxation)
- **Analgesia:** Paracetamol, NSAID (if appropriate), consider corticosteroid injection (if severe)

**DEPRESSION AND ANXIETY MANAGEMENT:**
- **Screening:** Regular screening for depression (PHQ-9), anxiety (GAD-7)
- **Counselling:** Psychological support, adjustment to disability
- **Cognitive behavioural therapy (CBT):** For depression, anxiety
- **Antidepressants:** SSRI (e.g., sertraline 50 mg OD) if moderate-severe depression

**Sources:** NICE Guidelines (NG232), RCP Guidelines, BSRM Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG232)", "RCP Guidelines", "BSRM Guidelines"]
            }
        )

    def _handle_musculoskeletal_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Musculoskeletal rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**MUSCULOSKELETAL REHABILITATION**

**PRINCIPLES OF MUSCULOSKELETAL REHABILITATION:**

- **Early mobilisation:** Prevent stiffness, muscle wasting, joint contractures
- **Progressive loading:** Gradual increase in load/activity (protect healing tissue, promote remodelling)
- **Pain management:** Multimodal analgesia, exercise therapy, manual therapy
- **Restoration of function:** ROM, strength, proprioception, functional activities
- **Return to activity/sport:** Gradual return, guided by symptoms, functional assessment

**COMMON MUSCULOSKELETAL CONDITIONS REQUIRING REHABILITATION:**

**1. JOINT REPLACEMENT REHABILITATION (TOTAL KNEE ARTHROPLASTY - TKA, TOTAL HIP ARTHROPLASTY - THA):**

**Pre-operative (prehabilitation):**
- **Education:** Explain procedure, expected recovery, rehabilitation goals
- **Exercise therapy:** Pre-operative strengthening (quadriceps, hip abductors), gait training (walking aid familiarisation)
- **Home assessment:** Assess for modifications (ramps, handrails, toilet seat raiser)

**Post-operative:**
- **Day 0-2:** Mobilisation (sit-to-stand, walking with frame), circulation exercises (ankle pumps), deep breathing exercises
- **Day 3-7:** Progress mobilisation (frame → stick → walking aid), ROM exercises (flexion/extension), strengthening exercises (quadriceps, gluteals), stair assessment
- **Week 2-6:** Progress walking (outdoor walking, increase distance), continue ROM exercises, progress strengthening (resistance bands, weights), return to ADL (independent with walking aid)
- **Week 6-12:** Discontinue walking aid (if appropriate), progress strengthening (gym-based exercises), return to leisure activities (swimming, cycling)
- **3-6 months:** Return to sport (low impact: swimming, cycling, golf; high impact: running, tennis - if appropriate)

**2. FRACTURE REHABILITATION:**

**Principles:**
- **Immobilisation:** Protect fracture (cast, splint, internal fixation)
- **Early mobilisation:** Joints above and below fracture (if allowed by orthopaedic surgeon)
- **Weight-bearing status:** Non-weight-bearing (NWB), partial weight-bearing (PWB), weight-bearing as tolerated (WBAT) (guided by orthopaedic surgeon)
- **ROM exercises:** Prevent joint stiffness, muscle contractures
- **Strengthening exercises:** Once fracture united (confirmed by X-ray)

**Common fractures:**
- **Upper limb fractures:** Clavicle, humerus, radius/ulna, wrist, hand (finger, metacarpal, phalangeal)
- **Lower limb fractures:** Hip, femur, tibia/fibula, ankle, foot (calcaneum, metatarsal, phalangeal)

**Rehabilitation timeline:**
- **0-6 weeks:** Immobilisation (cast, splint), ROM exercises (joints above/below fracture), non-weight-bearing or partial weight-bearing (lower limb fractures)
- **6-12 weeks:** Fracture union (confirmed by X-ray), progress ROM, progress weight-bearing (lower limb fractures), begin strengthening exercises
- **12+ weeks:** Full weight-bearing, progress strengthening, return to ADL/sport

**3. BACK PAIN REHABILITATION:**

**Acute low back pain (<6 weeks):**
- **Education:** Reassurance (benign, self-limiting), avoid bed rest (stay active)
- **Exercise therapy:** Gentle exercises (walking, stretching, core stabilisation)
- **Manual therapy:** Spinal mobilisation/manipulation (physiotherapist, osteopath, chiropractor)
- **Analgesia:** Paracetamol, NSAID (if appropriate), consider neuropathic pain agents (if radiculopathy)

**Chronic low back pain (>12 weeks):**
- **Exercise therapy:** Core stabilisation (Pilates, McKenzie method), general exercise (walking, swimming, cycling)
- **Cognitive behavioural therapy (CBT):** Address fear-avoidance beliefs, promote self-management
- **Manual therapy:** Spinal mobilisation/manipulation (short-term benefit)
- **Multidisciplinary pain management:** Pain clinic referral (if not improved)
- **Consider referral:** For spinal injections (nerve root block, facet joint injection), spinal surgery (if structural abnormality, e.g., spinal stenosis, spondylolisthesis)

**4. WHIPLASH-ASSOCIATED DISORDERS (WAD):**

**Grading:**
- **Grade 0:** No neck symptoms, no physical signs
- **Grade 1:** Neck pain, stiffness, tenderness only (no physical signs)
- **Grade 2:** Neck complaints + musculoskeletal signs (decreased ROM, tender points)
- **Grade 3:** Neck complaints + neurological signs (weakness, sensory changes, reflex changes)
- **Grade 4:** Neck complaints + fracture/dislocation

**Rehabilitation:**
- **Grade 0-1:** Reassurance, early mobilisation, gentle ROM exercises, return to normal activities
- **Grade 2:** Early mobilisation, ROM exercises, strengthening exercises (deep neck flexors, scapular stabilisers), manual therapy
- **Grade 3:** As for grade 2, consider neurological assessment, specialist referral
- **Grade 4:** Orthopaedic management (fracture/dislocation), refer to orthopaedics

**5. TENDINOPATHY REHABILITATION:**

**Common tendinopathies:**
- **Rotator cuff tendinopathy:** Shoulder pain, weakness, night pain
- **Tennis elbow (lateral epicondylitis):** Lateral elbow pain, gripping weakness
- **Golfer's elbow (medial epicondylitis):** Medial elbow pain, gripping weakness
- **Achilles tendinopathy:** Ankle pain, stiffness (morning), pain with activity
- **Patellar tendinopathy:** Anterior knee pain, jumping activities

**Rehabilitation principles:**
- **Load management:** Reduce aggravating activities, relative rest (avoid complete rest)
- **Exercise therapy:** Eccentric loading exercises (Alfredson protocol for Achilles tendinopathy), isometric exercises (for pain relief), isotonic exercises (strengthening), plyometric exercises (return to sport)
- **Manual therapy:** Soft tissue massage, frictions, mobilisations
- **Adjuncts:** Low-level laser therapy, extracorporeal shockwave therapy (ESWT), platelet-rich plasma (PRP) (evidence limited)

**6. OSTEOARTHRITIS REHABILITATION:**

**Principles:**
- **Exercise therapy:** Strengthening (quadriceps for knee OA, hip abductors for hip OA), ROM exercises, low-impact aerobic exercise (walking, cycling, swimming)
- **Weight loss:** If overweight or obese (reduce joint load, improve symptoms)
- **Pain management:** Paracetamol, topical NSAID, oral NSAID, consider intra-articular corticosteroid injection
- **Assistive devices:** Walking stick (reduce joint load), braces (offload affected compartment), shoe modifications (lateral wedge for medial knee OA)
- **Joint protection:** Avoid high-impact activities (running, jumping), modify activities (swimming, cycling instead)

**MUSCULOSKELETAL REHABILITATION INTERVENTIONS:**

**EXERCISE THERAPY:**
- **Range of movement (ROM) exercises:** Active, active-assisted, passive exercises
- **Strengthening exercises:** Isometric, isotonic, isokinetic, eccentric exercises
- **Proprioceptive exercises:** Balance training, neuromuscular training
- **Functional exercises:** Task-specific training (sit-to-stand, stair climbing, gait training)
- **Cardiovascular exercise:** Walking, cycling, swimming (low-impact)

**MANUAL THERAPY:**
- **Soft tissue massage:** Myofascial release, trigger point release
- **Joint mobilisations:** Maitland, Kaltenborn, Mulligan techniques
- **Joint manipulation:** High-velocity, low-amplitude thrust (HVLAT) (spinal, peripheral joints)
- **Stretching:** Static stretching, PNF (proprioceptive neuromuscular facilitation) stretching

**ELECTROTHERAPY:**
- **Transcutaneous electrical nerve stimulation (TENS):** Pain relief (gate control theory)
- **Interferential therapy (IFT):** Pain relief, muscle stimulation
- **Ultrasound therapy:** Tissue healing, pain relief (evidence limited)
- **Low-level laser therapy (LLLT):** Tissue healing, pain relief (evidence limited)

**Sources:** NICE Guidelines (NG59, NG226), BSRM Guidelines, CSP Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG59, NG226)", "BSRM Guidelines", "CSP Guidelines"]
            }
        )

    def _handle_cardiac_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Cardiac rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**CARDIAC REHABILITATION**

**DEFINITION:**
Cardiac rehabilitation (CR) is a comprehensive intervention designed to optimise cardiovascular health following cardiac events (myocardial infarction, cardiac surgery, heart failure).

**CORE COMPONENTS OF CARDIAC REHABILITATION:**

1. **Exercise training:** Aerobic exercise, resistance training, flexibility exercises
2. **Education:** Heart disease, risk factor modification, medication adherence
3. **Risk factor modification:** Smoking cessation, dietary modification, weight management, blood pressure control, lipid management, diabetes management
4. **Psychological support:** Stress management, anxiety, depression, social support

**INDICATIONS FOR CARDIAC REHABILITATION:**

- **Myocardial infarction (MI):** STEMI, NSTEMI (post-acute phase)
- **Coronary revascularisation:** PCI (percutaneous coronary intervention), CABG (coronary artery bypass grafting)
- **Heart failure:** Left ventricular systolic dysfunction (LVSD), NYHA class II-III
- **Cardiac surgery:** Valve replacement/repair, cardiac transplantation
- **Stable angina:** Chronic stable angina (optimise medical management)

**CARDIAC REHABILITATION PHASES:**

**PHASE 1 (INPATIENT):**

**Goals:**
- **Early mobilisation:** Prevent deconditioning, deep vein thrombosis (DVT), pneumonia
- **Education:** Diagnosis, treatment, risk factor modification, discharge planning
- **Psychological support:** Anxiety, depression, adjustment to diagnosis

**Interventions:**
- **Mobilisation:** Bed rest for first 12-24 hours (STEMI), then progressive mobilisation (sit out of bed, walking, stairs)
- **Exercise testing:** Submaximal exercise test (e.g., 6-minute walk test) prior to discharge
- **Education:** Heart-healthy diet (Mediterranean diet), smoking cessation, medication adherence, warning signs (red flags)
- **Discharge planning:** Referral to Phase 2 cardiac rehabilitation

**PHASE 2 (OUTPATIENT - FIRST 6-12 WEEKS):**

**Goals:**
- **Exercise training:** Improve cardiovascular fitness, functional capacity
- **Risk factor modification:** Smoking cessation, dietary modification, weight management, blood pressure control, lipid management, diabetes management
- **Psychological support:** Stress management, anxiety, depression

**Exercise training:**
- **Aerobic exercise:** 3-5 sessions/week, 20-60 minutes/session (moderate intensity: 40-70% heart rate reserve or 11-14 on Borg RPE scale)
- **Resistance training:** 2-3 sessions/week, 8-10 exercises, 1-3 sets, 10-15 repetitions (moderate intensity: 40-60% 1-RM)
- **Flexibility exercises:** 2-3 sessions/week, major muscle groups (static stretching, hold 15-30 seconds)

**Risk factor modification:**
- **Smoking cessation:** Counselling, nicotine replacement therapy (NRT), varenicline, bupropion
- **Dietary modification:** Mediterranean diet (high in fruits, vegetables, whole grains, fish, olive oil; low in red meat, saturated fats, processed foods)
- **Weight management:** Aim for BMI 18.5-24.9 kg/m², waist circumference <94 cm (men), <80 cm (women)
- **Blood pressure control:** <140/90 mmHg (<130/80 mmHg if diabetes, CKD)
- **Lipid management:** Total cholesterol <4 mmol/L, LDL <2 mmol/L (or <1.4 mmol/L if very high risk)
- **Diabetes management:** HbA1c <48 mmol/mol (<6.5%)

**Psychological support:**
- **Stress management:** Relaxation techniques (deep breathing, progressive muscle relaxation), mindfulness-based stress reduction (MBSR)
- **Anxiety/depression:** Screening (HADS - Hospital Anxiety and Depression Scale), counselling, cognitive behavioural therapy (CBT), antidepressants if moderate-severe depression

**PHASE 3 (MAINTENANCE - LONG-TERM):**

**Goals:**
- **Maintain exercise habits:** Long-term adherence to exercise programme
- **Maintain risk factor modification:** Smoking cessation, dietary modification, weight management
- **Prevent recurrence:** Secondary prevention of cardiovascular disease

**Interventions:**
- **Exercise:** Continue aerobic exercise 3-5 sessions/week, resistance training 2-3 sessions/week
- **Risk factor modification:** Continue smoking cessation, dietary modification, weight management
- **Regular follow-up:** Annual review with GP or cardiologist

**CARDIAC REHABILITATION EXERCISE PRESCRIPTION:**

**Aerobic exercise:**
- **Mode:** Walking, cycling, swimming, treadmill, rowing machine, elliptical trainer
- **Intensity:** Moderate intensity (40-70% heart rate reserve or 11-14 on Borg RPE scale)
- **Duration:** 20-60 minutes/session (start with 10-20 minutes, progress gradually)
- **Frequency:** 3-5 sessions/week
- **Progression:** Gradual increase in duration, then intensity (over 6-12 weeks)

**Resistance training:**
- **Mode:** Resistance machines, free weights, resistance bands, bodyweight exercises
- **Intensity:** Moderate intensity (40-60% 1-RM, 10-15 repetitions)
- **Volume:** 8-10 exercises, 1-3 sets
- **Frequency:** 2-3 sessions/week
- **Exercises:** Major muscle groups (chest, back, shoulders, arms, legs, core)

**Flexibility exercises:**
- **Mode:** Static stretching, PNF stretching
- **Intensity:** Stretch to point of mild discomfort (not pain)
- **Duration:** Hold 15-30 seconds, repeat 2-4 times
- **Frequency:** 2-3 sessions/week
- **Exercises:** Major muscle groups (quadriceps, hamstrings, calves, chest, back, shoulders)

**CONTRAINDICATIONS AND PRECAUTIONS:**

**Absolute contraindications:**
- **Acute coronary syndrome:** Unstable angina, acute MI (within first 48 hours)
- **Uncontrolled heart failure:** NYHA class IV (decompensated)
- **Severe aortic stenosis:** Valve area <1.0 cm²
- **Hypertrophic obstructive cardiomyopathy:** With significant outflow obstruction
- **Uncontrolled arrhythmias:** Atrial fibrillation with rapid ventricular response, ventricular tachycardia

**Relative contraindications:**
- **Severe left ventricular systolic dysfunction:** LVEF <30%
- **Significant pulmonary hypertension:** Pulmonary artery systolic pressure >50 mmHg
- **Severe symptomatic anaemia:** Hb <80 g/L
- **Uncontrolled hypertension:** BP >180/100 mmHg
- **Orthopaedic limitations:** Severe arthritis, recent fracture, joint replacement

**EXERCISE TRAINING SAFETY:**

**Monitoring:**
- **Pre-exercise:** Blood pressure, heart rate, symptoms (chest pain, dyspnoea, dizziness)
- **During exercise:** Borg RPE scale, symptoms (chest pain, dyspnoea, dizziness)
- **Post-exercise:** Cool-down, monitor for delayed symptoms

**Warning signs (STOP exercise):**
- **Chest pain/angina:** Tightness, heaviness, squeezing in chest
- **Excessive dyspnoea:** Unable to talk in full sentences
- **Dizziness/lightheadedness:** Presyncope, syncope
- **Palpitations:** Irregular heartbeat, tachycardia, bradycardia
- **Excessive fatigue:** Unusual tiredness, weakness

**BENEFITS OF CARDIAC REHABILITATION:**

- **Reduced mortality:** 20-30% reduction in cardiovascular mortality
- **Reduced morbidity:** Reduced hospital admissions, improved quality of life
- **Improved functional capacity:** Improved exercise tolerance, activities of daily living
- **Improved risk factor profile:** Blood pressure, lipid profile, glycaemic control
- **Psychological benefits:** Reduced anxiety, depression, improved mood

**Sources:** NICE Guidelines (NG172), BACPR Guidelines, ESC Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG172)", "BACPR Guidelines", "ESC Guidelines"]
            }
        )

    def _handle_pulmonary_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Pulmonary rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**PULMONARY REHABILITATION**

**DEFINITION:**
Pulmonary rehabilitation (PR) is a comprehensive intervention designed to reduce symptoms, improve functional capacity, and enhance quality of life in patients with chronic respiratory disease.

**CORE COMPONENTS OF PULMONARY REHABILITATION:**

1. **Exercise training:** Aerobic exercise, resistance training, upper limb exercises
2. **Education:** Respiratory disease, medication, inhaler technique, self-management
3. **Behavioural change:** Smoking cessation, physical activity promotion
4. **Psychological support:** Anxiety, depression, panic management

**INDICATIONS FOR PULMONARY REHABILITATION:**

- **Chronic obstructive pulmonary disease (COPD):** GOLD stage II-IV (mild-severe airflow limitation)
- **Bronchiectasis:** Chronic productive cough, recurrent infections
- **Interstitial lung disease (ILD):** Pulmonary fibrosis, sarcoidosis
- **Pulmonary hypertension:** WHO functional class II-III
- **Pre- and post-lung transplantation:** Optimise functional capacity pre-transplant, rehabilitation post-transplant
- **COVID-19:** Post-COVID syndrome (persistent symptoms >12 weeks)

**PULMONARY REHABILITATION PROGRAMME:**

**Structure:**
- **Duration:** 6-8 weeks
- **Frequency:** 2-3 sessions/week
- **Duration per session:** 2 hours (exercise training + education)
- **Location:** Hospital-based, community-based, or home-based (supervised or unsupervised)
- **Multidisciplinary team:** Physiotherapist, occupational therapist, respiratory nurse, dietician, psychologist

**EXERCISE TRAINING:**

**Aerobic exercise:**
- **Mode:** Walking (treadmill or overground), cycling (stationary bike), stepping
- **Intensity:** Moderate intensity (symptom-limited, Borg RPE 12-14, dyspnoea <5 on Borg CRQ scale)
- **Duration:** 20-30 minutes/session (start with 5-10 minutes, progress gradually)
- **Frequency:** 2-3 sessions/week
- **Progression:** Gradual increase in duration (aim for 30 minutes continuous exercise), then intensity

**Resistance training:**
- **Mode:** Resistance machines, free weights, resistance bands, bodyweight exercises
- **Intensity:** Moderate intensity (10-15 repetitions, 2-3 sets)
- **Frequency:** 2-3 sessions/week
- **Exercises:** Major muscle groups (quadriceps, hamstrings, calves, chest, back, shoulders, arms)

**Upper limb exercises:**
- **Importance:** Upper limb activities exacerbate dyspnoea in COPD (due to accessory muscle use)
- **Exercises:** Arm raises, shoulder exercises, arm ergometer (arm cycling)
- **Intensity:** Symptom-limited, start with 5 minutes, progress gradually

**Inspiratory muscle training:**
- **Indication:** Inspiratory muscle weakness (maximal inspiratory pressure [PImax] <60 cmH₂O)
- **Device:** Threshold loading device (e.g., PowerBreathe)
- **Protocol:** 30 breaths twice daily at 30-50% maximal inspiratory pressure (6-12 weeks)
- **Benefits:** Improved inspiratory muscle strength, reduced dyspnoea

**EXERCISE TRAINING MODIFICATIONS:**

**Oxygen supplementation:**
- **Indication:** SpO₂ <88% during exercise (or SpO₂ <90% in interstitial lung disease)
- **Prescription:** Titrate oxygen to maintain SpO₂ ≥88-90% during exercise
- **Delivery:** Nasal cannulae (2-6 L/min), Venturi mask (24-28%)

**Bronchodilator pre-treatment:**
- **Indication:** COPD, bronchiectasis (reversible airflow obstruction)
- **Protocol:** Short-acting bronchodilator (salbutamol 200-400 mcg via spacer) 30 minutes before exercise
- **Benefits:** Reduced dyspnoea, improved exercise tolerance

**Non-invasive ventilation (NIV):**
- **Indication:** Severe COPD with hypercapnic respiratory failure (CO₂ retention)
- **Protocol:** NIV during exercise (if available, limited evidence)
- **Benefits:** Reduced dyspnoea, improved exercise tolerance (select patients)

**EDUCATION COMPONENT:**

**Respiratory disease:**
- **Pathophysiology:** COPD, bronchiectasis, interstitial lung disease, pulmonary hypertension
- **Prognosis:** Disease progression, exacerbations, end-of-life care
- **Treatment:** Medications, inhalers, oxygen therapy, non-invasive ventilation

**Medication and inhaler technique:**
- **Bronchodilators:** Short-acting (salbutamol, ipratropium) vs. long-acting (salmeterol, tiotropium)
- **Inhaled corticosteroids:** Fluticasone, budesonide (add-on for frequent exacerbators)
- **Inhaler technique:** Check and optimise inhaler technique (MDI + spacer, DPI, soft mist inhaler)
- **Adherence:** Importance of regular medication use, proper inhaler technique

**Self-management:**
- **Action plan:** Recognise exacerbation symptoms (increased dyspnoea, sputum volume/purulence, fever), early intervention (antibiotics, oral corticosteroids)
- **Energy conservation:** Pacing, prioritising activities, planning ahead
- **Airway clearance techniques:** Active cycle of breathing technique (ACBT), autogenic drainage, positive expiratory pressure (PEP) devices

**Smoking cessation:**
- **Counselling:** Motivational interviewing, brief intervention
- **Pharmacotherapy:** Nicotine replacement therapy (NRT), varenicline, bupropion
- **Support:** Smoking cessation clinic, quitline, support groups

**BEHAVIOURAL CHANGE:**

**Physical activity promotion:**
- **Goal:** 150 minutes/week moderate-intensity physical activity (in bouts of ≥10 minutes)
- **Strategies:** Pedometer/accelerometer, walking groups, activity diary
- **Benefits:** Improved functional capacity, reduced exacerbations, improved quality of life

**Energy conservation:**
- **Pacing:** Break tasks into smaller chunks, rest breaks, prioritise activities
- **Planning:** Plan ahead (prepare meals in advance, batch cooking, online shopping)
- **Assistive devices:** Walking aids, perching stool, grab rails, shower chair

**PSYCHOLOGICAL SUPPORT:**

**Anxiety management:**
- **Prevalence:** Anxiety common in COPD (20-40%), due to dyspnoea, fear of breathlessness
- **Screening:** HADS (Hospital Anxiety and Depression Scale), GAD-7 (Generalised Anxiety Disorder 7-item)
- **Interventions:** Relaxation techniques (deep breathing, progressive muscle relaxation), cognitive behavioural therapy (CBT), mindfulness-based stress reduction (MBSR)

**Depression management:**
- **Prevalence:** Depression common in COPD (20-40%), due to chronic illness, functional limitation
- **Screening:** PHQ-9 (Patient Health Questionnaire 9-item)
- **Interventions:** Counselling, cognitive behavioural therapy (CBT), antidepressants (SSRI, e.g., sertraline 50 mg OD)

**Panic management:**
- **Prevalence:** Panic attacks common in COPD (10-20%), due to dyspnoea, fear of breathlessness
- **Interventions:** Breathing control (pursed-lip breathing, breathing exercises), cognitive restructuring, exposure therapy

**PULMONARY REHABILITATION OUTCOMES:**

**Functional outcomes:**
- **Improved exercise capacity:** 6-minute walk distance (6MWD) increase by 50-80 meters (clinically significant)
- **Improved dyspnoea:** Reduced dyspnoea (Borg CRQ scale, mMRC dyspnoea scale)
- **Improved quality of life:** St George's Respiratory Questionnaire (SGRQ) score decrease by 8-10 points (clinically significant)

**Healthcare utilisation:**
- **Reduced hospital admissions:** 30-50% reduction in COPD admissions
- **Reduced length of stay:** Shorter hospital stay if admitted for exacerbation
- **Reduced exacerbations:** Fewer exacerbations (if smoking cessation, medication optimisation)

**Mortality:**
- **No mortality benefit:** Pulmonary rehabilitation improves symptoms and quality of life, but does not reduce mortality

**Sources:** NICE Guidelines (NG115), BTS Guidelines, ATS/ERS Statement""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG115)", "BTS Guidelines", "ATS/ERS Statement"]
            }
        )

    def _handle_neurological_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Neurological rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**NEUROLOGICAL REHABILITATION**

**PRINCIPLES OF NEUROLOGICAL REHABILITATION:**

- **Neuroplasticity:** Brain's ability to reorganise and form new connections (promoted by repetitive, task-specific training)
- **Compensatory strategies:** Use of intact functions to compensate for impaired functions
- **Adaptive equipment:** Assistive devices to promote independence
- **Multidisciplinary team (MDT):** Neurologist, physiotherapist, occupational therapist, speech and language therapist, psychologist, nursing staff
- **Patient-centred goals:** SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals

**COMMON NEUROLOGICAL CONDITIONS REQUIRING REHABILITATION:**

**1. PARKINSON'S DISEASE (PD):**

**Motor symptoms:**
- **Resting tremor:** 4-6 Hz pill-rolling tremor (worse at rest, improves with activity)
- **Bradykinesia:** Slowness of movement, difficulty initiating movement
- **Rigidity:** Lead-pipe rigidity (increased tone throughout ROM), cogwheel rigidity (superimposed tremor)
- **Postural instability:** Impaired balance, falls risk

**Non-motor symptoms:**
- **Neuropsychiatric:** Depression, anxiety, apathy, hallucinations, dementia
- **Autonomic:** Constipation, urinary frequency/urgency, orthostatic hypotension, erectile dysfunction
- **Sleep:** Insomnia, REM sleep behaviour disorder (RBD), excessive daytime sleepiness
- **Sensory:** Hyposmia (loss of smell), pain, paraesthesia

**Rehabilitation:**
- **Exercise therapy:** Aerobic exercise (walking, cycling), resistance training, balance training, Tai Chi, dance (e.g., ballet, tango)
- **Physiotherapy:** Gait training (cueing strategies - visual cues, auditory cues), fall prevention, transfers
- **Occupational therapy:** ADL training (fine motor skills, dressing, feeding), home modifications, assistive devices
- **Speech and language therapy:** Speech (hypophonia - soft speech, monotone speech), swallowing (dysphagia)
- **Cognitive rehabilitation:** Cognitive exercises, compensatory strategies (memory aids, notebooks)

**2. MULTIPLE SCLEROSIS (MS):**

**Types:**
- **Relapsing-remitting MS (RRMS):** Relapses followed by remission (80-85% at onset)
- **Secondary progressive MS (SPMS):** Progressive disability after relapsing-remitting phase
- **Primary progressive MS (PPMS):** Progressive disability from onset (10-15%)
- **Progressive-relapsing MS (PRMS):** Progressive disease with superimposed relapses (rare)

**Rehabilitation:**
- **Exercise therapy:** Aerobic exercise (walking, cycling, swimming), resistance training, balance training, core stabilisation, Pilates, yoga
- **Fatigue management:** Energy conservation, pacing, cooling strategies (heat sensitivity), aerobic exercise (reduces fatigue), medication (amantadine 100 mg BD)
- **Spasticity management:** Stretching exercises, positioning, oral medications (baclofen 10 mg TDS, tizanidine 2 mg TDS), botulinum toxin injections, intrathecal baclofen pump
- **Bladder dysfunction:** Anticholinergics (oxybutynin 5 mg TDS), intermittent self-catheterisation (if urinary retention)
- **Bowel dysfunction:** Constipation (fibre, fluid, laxatives), faecal incontinence (antidiarrhoeals, bowel programme)
- **Cognitive rehabilitation:** Cognitive exercises, compensatory strategies (memory aids, notebooks, smartphone apps)
- **Psychological support:** Counselling, cognitive behavioural therapy (CBT), support groups

**3. GUILLAIN-BARRÉ SYNDROME (GBS):**

**Clinical features:**
- **Ascending weakness:** Starts in legs, ascends to arms, trunk, facial muscles (may progress to respiratory failure)
- **Areflexia:** Loss of deep tendon reflexes
- **Sensory changes:** Paraesthesia, numbness, pain (common in back, limbs)
- **Autonomic dysfunction:** Fluctuating blood pressure, tachycardia, arrhythmias

**Rehabilitation:**
- **Acute phase:** Immobilisation (prevent contractures, pressure ulcers), respiratory monitoring (ventilatory support if required), autonomic instability monitoring (fluctuating BP, HR)
- **Subacute phase:** Progressive mobilisation (bed → sitting → standing → walking), ROM exercises (prevent contractures), strengthening exercises, balance training, gait re-education
- **Chronic phase:** Continue exercises, orthoses (ankle-foot orthosis - AFO for foot drop), assistive devices (walking aids), pain management (neuropathic pain agents - gabapentin, pregabalin), psychological support (adjustment to disability)
- **Prognosis:** 70-80% make good recovery, 10-15% permanent disability, 5-10% mortality

**4. MOTOR NEURONE DISEASE (MND) / AMYOTROPHIC LATERAL SCLEROSIS (ALS):**

**Clinical features:**
- **Muscle weakness:** Progressive weakness, wasting (limb-onset, bulbar-onset)
- **UMN signs:** Spasticity, hyperreflexia, Babinski sign
- **LMN signs:** Fasciculations, weakness, wasting, areflexia
- **Bulbar involvement:** Dysarthria, dysphagia, emotional lability

**Rehabilitation:**
- **Mobility:** Walking aids (walking stick, frame), wheelchair assessment (as disease progresses)
- **Upper limb:** Assistive devices (feeding aids, dressing aids, writing aids), orthoses (wrist splint)
- **Speech and language therapy:** Communication aids (alphabet board, communication device, eye-tracking technology), swallowing assessment (dietary modification, PEG tube if indicated)
- **Respiratory:** Non-invasive ventilation (NIV) for respiratory failure (hypercapnia), cough assist device (mechanical insufflator-exsufflator), airway clearance techniques
- **Palliative care:** Early referral for symptom management, psychosocial support, end-of-life care

**NEUROLOGICAL REHABILITATION INTERVENTIONS:**

**EXERCISE THERAPY:**
- **Aerobic exercise:** Walking, cycling, swimming (low-impact, improves cardiovascular fitness)
- **Resistance training:** Strengthening exercises (prevent muscle atrophy, improve function)
- **Balance training:** Standing balance, weight-shifting, perturbation training, Tai Chi
- **Stretching exercises:** Prevent contractures (especially if spasticity)
- **Gait training:** Cueing strategies (visual cues, auditory cues), gait aids (walking stick, frame), orthoses (AFO for foot drop)

**ASSISTIVE DEVICES:**
- **Mobility aids:** Walking stick, tripod, frame, rollator, wheelchair (manual or powered)
- **Orthoses:** Ankle-foot orthosis (AFO) for foot drop, hand splint (for spasticity, contracture)
- **ADL aids:** Feeding aids, dressing aids, bathing aids, writing aids, communication aids
- **Home modifications:** Ramps, handrails, stairlift, bathroom modifications (grab rails, shower chair)

**SPASTICITY MANAGEMENT:**
- **Physiotherapy:** Stretching exercises, positioning, casting/splinting
- **Oral medications:** Baclofen (10 mg TDS, titrate to effect), tizanidine (2 mg TDS, titrate to effect), dantrolene (25 mg OD, titrate to effect)
- **Botulinum toxin:** Local injection into spastic muscles (reduce tone, improve function, prevent contractures)
- **Intrathecal baclofen pump:** For severe generalised spasticity (refractory to oral medications)

**FATIGUE MANAGEMENT:**
- **Energy conservation:** Pacing, prioritising activities, rest breaks, planning ahead
- **Exercise therapy:** Graded exercise programme (avoid overexertion, prevent post-exertional fatigue)
- **Cooling strategies:** For heat sensitivity (MS) - cold packs, cooling vests, avoid hot environments
- **Medication:** Amantadine 100 mg BD (MS fatigue), modafinil 200 mg OD (off-label)

**Sources:** NICE Guidelines (NG71, NG258), BSRM Guidelines, ABN Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG71, NG258)", "BSRM Guidelines", "ABN Guidelines"]
            }
        )

    def _handle_amputee_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Amputee rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**AMPUTEE REHABILITATION**

**PRINCIPLES OF AMPUTEE REHABILITATION:**

- **Early involvement:** Pre-operative counselling, post-operative rehabilitation, prosthetic training
- **Multidisciplinary team (MDT):** Vascular surgeon, orthopaedic surgeon, physiotherapist, occupational therapist, prosthetist, psychologist
- **Patient-centred goals:** Functional independence, mobility, return to activities/work/sport
- **Psychological support:** Adjustment to limb loss, body image, depression, anxiety

**LEVELS OF AMPUTATION:**

**LOWER LIMB AMPUTATION:**

**Transtibial (below-knee) amputation (BKA):**
- **Level:** Through tibia
- **Functional outcome:** Good functional outcome, energy-efficient walking with prosthesis
- **Prosthesis:** Patellar tendon-bearing socket, prosthetic foot (SACH, single-axis, multiaxis, energy-storing and return - ESAR)

**Knee disarticulation:**
- **Level:** Through knee joint
- **Functional outcome:** Good lever arm for prosthesis, preserves femur length
- **Prosthesis:** Suction socket, prosthetic knee (single-axis, polycentric, microprocessor knee)

**Transfemoral (above-knee) amputation (AKA):**
- **Level:** Through femur
- **Functional outcome:** Higher energy cost of walking, more challenging prosthetic training
- **Prosthesis:** Ischial containment socket, prosthetic knee (single-axis, polycentric, microprocessor knee), prosthetic foot

**Hip disarticulation:**
- **Level:** Through hip joint
- **Functional outcome:** Poor functional outcome, high energy cost, wheel chair mobility preferred
- **Prosthesis:** Canadian-type hip disarticulation prosthesis (if ambulatory)

**UPPER LIMB AMPUTATION:**

**Transradial (below-elbow) amputation (BEA):**
- **Level:** Through radius and ulna
- **Functional outcome:** Good functional outcome, cosmetic prosthesis or body-powered prosthesis or myoelectric prosthesis

**Transhumeral (above-elbow) amputation (AEA):**
- **Level:** Through humerus
- **Functional outcome:** Poorer functional outcome than BEA, body-powered prosthesis or myoelectric prosthesis

**Shoulder disarticulation:**
- **Level:** Through shoulder joint
- **Functional outcome:** Poor functional outcome, cosmetic prosthesis or body-powered prosthesis

**PRE-OPERATIVE PHASE:**

**Counselling:**
- **Explanation of procedure:** Level of amputation, expected functional outcome, rehabilitation timeline
- **Prosthetic assessment:** Pre-prosthetic assessment (mobility, comorbidities, goals)
- **Psychological support:** Adjustment to limb loss, body image, depression, anxiety

**Mobility assessment:**
- **Current mobility:** Walking aid requirement, functional independence
- **Comorbidities:** Ischaemic heart disease, COPD, diabetes, visual impairment (affect prosthetic potential)

**POST-OPERATIVE PHASE (FIRST 2-4 WEEKS):**

**Goals:**
- **Wound healing:** Prevent infection, promote wound healing
- **Pain management:** Multimodal analgesia, stump pain management, phantom limb pain management
- **Prevent complications:** DVT prophylaxis, pressure ulcers, contractures, oedema

**Interventions:**
- **Stump bandaging:** Elastic bandaging (reduce oedema, shape stump for prosthetic)
- **Stump exercises:** ROM exercises (hip/knee exercises for lower limb amputation, shoulder/elbow exercises for upper limb amputation), strengthening exercises (residual limb and whole body)
- **Desensitisation:** Rubbing, tapping, massage (reduce hypersensitivity)
- **Mobilisation:** Bed mobility, transfers, mobilisation ( wheelchair if lower limb amputation)
- **Psychological support:** Adjustment to limb loss, body image, depression, anxiety

**PHANTOM LIMB PAIN:**

**Definition:** Pain in the absent limb (felt as if limb still present)

**Prevalence:** 50-80% of amputees

**Management:**
- **Analgesia:** Gabapentin 300 mg TDS (titrate to 1800 mg/day), pregabalin 75 mg BD (titrate to 300 mg BD), amitriptyline 25 mg nocte (titrate to 75-150 mg nocte)
- **Mirror therapy:** Mirror box (visual feedback of intact limb moving, reduces phantom limb pain)
- **Graded motor imagery:** Laterality training, imagined movements, mirror therapy
- **Desensitisation:** Rubbing, tapping, massage (reduce hypersensitivity)

**STUMP PAIN:**

**Definition:** Pain in the residual limb (stump)

**Causes:** Neuroma (painful nerve ending), infection, wound breakdown, pressure ulcer, ill-fitting prosthetic socket

**Management:**
- **Analgesia:** Paracetamol, NSAID, neuropathic pain agents (gabapentin, pregabalin)
- **Stump care:** Wound care, desensitisation, stump bandaging, correct prosthetic socket fit
- **Revision surgery:** If neuroma (excision of neuroma, nerve burying in muscle/bone)

**PROSTHETIC TRAINING (2-12 WEEKS POST-AMPUTATION):**

**Goals:**
- **Prosthetic fitting:** Temporary prosthesis (preparatory prosthesis) at 2-4 weeks, permanent prosthesis at 3-6 months
- **Prosthetic training:** Donning and doffing, standing balance, walking training
- **Functional independence:** ADL with prosthesis, return to activities/work/sport

**Interventions:**
- **Donning and doffing:** Put on and take off prosthesis (sock, liner, socket)
- **Standing balance:** Weight-bearing on prosthesis, static standing, dynamic standing (perturbations)
- **Gait training:** Walking training (parallel bars → walking aid → independent walking)
- **Stair training:** Stair ascent and descent (different technique for BKA vs. AKA)
- **Functional training:** Walking on uneven ground, slopes, steps, ramps
- **Fall prevention:** Balance training, gait aid (walking stick, frame), education (fall prevention strategies)

**PROSTHETIC POTENTIAL ASSESSMENT:**

**Good prognostic factors:**
- **Younger age:** <65 years
- **Good mobility pre-amputation:** Independent ambulator
- **Motivation:** High motivation, realistic goals
- **Comorbidities:** Minimal comorbidities (no ischaemic heart disease, COPD, diabetes complications)
- **Level of amputation:** Lower level (transtibial vs. transfemoral)
- **Cognition:** Intact cognition (able to follow instructions, learn prosthetic use)

**Poor prognostic factors:**
- **Older age:** >75 years
- **Poor mobility pre-amputation:** Wheelchair user pre-amputation
- **Comorbidities:** Significant comorbidities (ischaemic heart disease, COPD, diabetes complications, visual impairment)
- **Level of amputation:** Higher level (transfemoral vs. transtibial)
- **Cognition:** Cognitive impairment (dementia, confusion)

**LOWER LIMB PROSTHETIC OPTIONS:**

**Prosthetic feet:**
- **SACH (Solid Ankle Cushion Heel):** Basic foot, non-articulated, low cost
- **Single-axis foot:** Hinge at ankle, allows some dorsiflexion/plantarflexion
- **Multiaxis foot:** Multi-axial ankle, accommodates uneven terrain
- **Energy-storing and return (ESAR) foot:** Stores energy during stance phase, returns energy during push-off (for active amputees)
- **Microprocessor foot:** Microprocessor-controlled ankle (adapts to terrain, improves gait efficiency)

**Prosthetic knees (transfemoral amputation):**
- **Single-axis knee:** Hinge knee, stable, low cost
- **Polycentric knee:** Multi-axis knee, more natural gait, variable stability
- **Stance control knee:** Weight-activated locking, stable during stance phase
- **Microprocessor knee:** Microprocessor-controlled knee (adapts to gait speed, improves stability, reduces falls)

**UPPER LIMB PROSTHETIC OPTIONS:**

**Cosmetic prosthesis:**
- **Appearance:** Cosmetic restoration of limb appearance
- **Function:** No active function, passive positioning only
- **Indication:** Patients with low functional requirements, cosmetic appearance important

**Body-powered prosthesis:**
- **Mechanism:** Harness and cable system (movement of shoulder protracts and retracts hook)
- **Function:** Hook or hand for grasping, releasing
- **Indication:** Patients with good trunk and shoulder control, functional requirements

**Myoelectric prosthesis:**
- **Mechanism:** Electrodes detect muscle activity (EMG) in residual limb, control prosthetic hand
- **Function:** Electrically powered hand or hook (battery-powered)
- **Indication:** Patients with good EMG signals in residual limb, high functional requirements, cosmetic appearance important

**Sources:** NICE Guidelines (NG179), BSRM Guidelines, ISPO Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG179)", "BSRM Guidelines", "ISPO Guidelines"]
            }
        )

    def _handle_spinal_cord_injury_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Spinal cord injury rehabilitation guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**SPINAL CORD INJURY REHABILITATION**

**SPINAL CORD INJURY (SCI) CLASSIFICATION:**

**Complete injury:**
- **ASIA Impairment Scale (AIS) grade A:** No motor or sensory function preserved at S4-S5 segment
- **Prognosis:** Poor prognosis for functional recovery below level of injury

**Incomplete injury:**
- **ASIA Impairment Scale (AIS) grade B:** Sensory but not motor function preserved below level of injury
- **ASIA Impairment Scale (AIS) grade C:** Motor function preserved below level of injury, majority of key muscles <3/5
- **ASIA Impairment Scale (AIS) grade D:** Motor function preserved below level of injury, majority of key muscles ≥3/5
- **Prognosis:** Better prognosis for functional recovery (especially AIS grade D)

**LEVELS OF SPINAL CORD INJURY:**

**TETRAPLEGIA (QUADRIPLEGIA) - CERVICAL INJURY (C1-C8):**
- **Functional impairment:** Weakness/paralysis of all four limbs, trunk, pelvic organs
- **Respiratory impairment:** Diaphragmatic breathing (C3-5), ventilator dependency if high cervical injury (C1-C4)
- **Functional outcome:** Dependent level of injury (higher injury = greater functional impairment)

**PARAPLEGIA - THORACIC (T1-T12) OR LUMBAR (L1-L5) INJURY:**
- **Functional impairment:** Weakness/paralysis of lower limbs, trunk, pelvic organs
- **Arm function:** Normal (normal upper limb strength)
- **Functional outcome:** Independent wheelchair mobility, some household/community ambulation possible with orthoses (crutches, reciprocating gait orthosis - RGO) in low thoracic/lumbar injuries

**SPINAL CORD INJURY REHABILITATION PHASES:**

**1. ACUTE PHASE (FIRST 1-2 WEEKS):**

**Goals:**
- **Medical stabilisation:** Spinal stabilisation (surgery, traction, halo fixation), prevent secondary injury
- **Respiratory management:** Ventilator weaning (if ventilator-dependent), respiratory physiotherapy (chest physiotherapy, assisted coughing)
- **Prevent complications:** DVT prophylaxis (compression stockings, LMWH), pressure ulcers (pressure-relieving mattress, turning 2-4 hourly), UTI (indwelling urinary catheter, strict aseptic technique), constipation (bowel programme)

**Interventions:**
- **Immobilisation:** Spinal precautions (log-roll, thoracolumbar orthosis - TLSO, cervical collar)
- **Respiratory physiotherapy:** Breathing exercises, assisted coughing, mechanical insufflator-exsufflator (MI-E)
- **Passive range of movement exercises:** Prevent contractures (especially lower limbs)
- **Psychological support:** Adjustment to disability, depression, anxiety

**2. SUBACUTE PHASE (2-12 WEEKS):**

**Goals:**
- **Maximise functional recovery:** Intensive rehabilitation (physiotherapy, occupational therapy)
- **Promote neuroplasticity:** Repetitive, task-specific training
- **Prevent secondary complications:** Contractures, pressure ulcers, UTI, osteoporosis

**Interventions:**
- **Mobility training:** Bed mobility, sitting balance, standing balance (tilt table, standing frame), wheelchair mobility, gait training (if incomplete injury)
- **Upper limb strengthening:** Strengthening exercises (especially if tetraplegia - dependent on level of injury)
- **Lower limb exercises:** Active-assisted exercises (if incomplete injury), passive range of movement exercises (if complete injury)
- **Activities of daily living (ADL):** Feeding, dressing, grooming, bathing, toileting (adaptive equipment, techniques)
- **Bladder management:** Intermittent self-catheterisation (ISC) if appropriate, indwelling catheter if unable to perform ISC
- **Bowel management:** Bowel programme (diet, fluid, medications, suppositories, digital stimulation)
- **Skin care:** Pressure ulcer prevention (pressure-relieving mattress, regular turning, skin inspection)

**3. CHRONIC PHASE (>12 WEEKS):**

**Goals:**
- **Maintain functional gains:** Continue exercises, prevent deconditioning
- **Promote community reintegration:** Return to work/school, driving, leisure activities
- **Prevent secondary complications:** Osteoporosis, heterotopic ossification, syringomyelia, post-traumatic cyst

**Interventions:**
- **Continued physiotherapy:** Maintenance exercises, wheelchair skills, gait training (if appropriate)
- **Occupational therapy:** Home modifications, workplace modifications, assistive devices, driving assessment
- **Psychological support:** Depression, anxiety, adjustment to disability, peer support groups

**SPINAL CORD INJURY COMPLICATIONS:**

**AUTONOMIC DYSREFLEXIA (AD):**
- **Definition:** Life-threatening condition (injury at T6 or above), characterised by sudden onset of excessively high blood pressure due to spinal cord injury
- **Triggers:** Pain, pressure ulcer, bladder distension, bowel distension, ingrown toenail, tight clothing
- **Symptoms:** Severe headache, blurred vision, profuse sweating, flushing (above level of injury), nasal congestion, Bradycardia
- **Management:** Sit patient upright, loosen tight clothing, identify and remove trigger, pharmacological management (nifedipine 10 mg SL, nitroglycerin 0.4 mg SL) if severe

**PRESSURE ULCERS:**
- **Risk factors:** Impaired sensation, immobility, moisture, poor nutrition
- **Prevention:** Pressure-relieving mattress, regular turning (2-4 hourly), skin inspection, pressure relief (lifting, shifting weight)
- **Management:** Debride necrotic tissue, dressings (hydrocolloid, foam, alginate), antibiotics if infection, surgical debridement if deep ulcer

**DEEP VEIN THROMBOSIS (DVT):**
- **Risk factors:** Immobility, hypercoagulable state (spinal shock)
- **Prevention:** Compression stockings, LMWH (enoxaparin 40 mg SC OD), intermittent pneumatic compression (IPC)
- **Management:** Anticoagulation (therapeutic LMWH, warfarin target INR 2-3), IVC filter (if anticoagulation contraindicated)

**URINARY TRACT INFECTION (UTI):**
- **Risk factors:** Indwelling urinary catheter, incomplete bladder emptying, high bladder pressures
- **Prevention:** Aseptic technique, adequate fluid intake, regular catheter changes, intermittent self-catheterisation (ISC)
- **Management:** Antibiotics (based on culture and sensitivity), bladder monitoring (renal ultrasound, urodynamics)

**BOWEL DYSFUNCTION:**
- **Neurogenic bowel:** Constipation, faecal incontinence, autonomous dysreflexia (during bowel programme)
- **Management:** Bowel programme (diet, fluid, medications - stool softeners, laxatives, suppositories, digital stimulation), regular timing (every 1-2 days)

**HETEROTOPIC OSSIFICATION (HO):**
- **Definition:** Ectopic bone formation in soft tissues (around joints, especially hips, knees)
- **Clinical features:** Swelling, warmth, reduced ROM around joint (usually occurs 1-3 months post-injury)
- **Management:** NSAID (indomethacin 50 mg TDS) for prevention, bisphosphonates (etidronate) for treatment, surgical excision if severe (restricted ROM)

**OSTEOPOROSIS:**
- **Risk factors:** Immobilisation, reduced weight-bearing
- **Prevention:** Weight-bearing activities (if possible), calcium (1000 mg/day), vitamin D (800 IU/day), bisphosphonates (alendronate 70 mg weekly)
- **Management:** As above, treat fragility fractures (orthopaedic management)

**SPINAL CORD INJURY FUNCTIONAL OUTCOMES:**

**Tetraplegia (C1-C8):**
- **C1-C4:** Dependent for all care (ventilator-dependent if C1-C4)
- **C5:** Independent feeding with adaptive equipment, dependent for dressing, bathing, toileting
- **C6:** Independent feeding, some dressing (lower body), independent wheelchair (electric wheelchair)
- **C7-C8:** Independent ADL, independent wheelchair (manual wheelchair), some household ambulation possible with orthoses (if incomplete injury)

**Paraplegia (T1-T12, L1-L5):**
- **T1-T9:** Independent wheelchair (manual wheelchair), household ambulation possible with orthoses (reciprocating gait orthosis - RGO)
- **T10-L2:** Independent wheelchair (manual wheelchair), household/community ambulation possible with orthoses (crutches, ankle-foot orthosis - AFO)
- **L3-S5:** Independent wheelchair (manual wheelchair), community ambulation possible with orthoses (crutches, AFO), may walk independently without aids (if incomplete injury)

**Sources:** NICE Guidelines (NG250), BSRM Guidelines, ISCoS Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["NICE Guidelines (NG250)", "BSRM Guidelines", "ISCoS Guidelines"]
            }
        )

    def _handle_disability_assessment(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Disability and functional assessment guidance"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**DISABILITY AND FUNCTIONAL ASSESSMENT**

**FUNCTIONAL ASSESSMENT TOOLS:**

**1. BARTHEL INDEX (BI):**

**Purpose:** Assess functional independence in activities of daily living (ADL)

**Domains (10 items, scored 0-15, maximum 20):**
1. **Feeding:** 0-10 (0 = unable, 5 = needs help cutting/spreading, 10 = independent)
2. **Transfer:** 0-15 (0 = unable, 5 = major help, 10 = minor help, 15 = independent)
3. **Grooming:** 0-5 (0 = dependent, 5 = independent)
4. **Toilet use:** 0-10 (0 = dependent, 5 = needs help, 10 = independent)
5. **Bathing:** 0-5 (0 = dependent, 5 = independent)
6. **Mobility (level surface):** 0-15 (0 = immobile, 5 = wheelchair independent, 10 = walks with help, 15 = independent)
7. **Stairs:** 0-10 (0 = unable, 5 = needs help, 10 = independent)
8. **Dressing:** 0-10 (0 = dependent, 5 = needs help, 10 = independent)
9. **Bowel control:** 0-10 (0 = incontinent, 5 = occasional accident, 10 = continent)
10. **Bladder control:** 0-10 (0 = incontinent, 5 = occasional accident, 10 = continent)

**Interpretation:**
- **20:** Independent
- **15-19:** Slight dependence
- **10-14:** Moderate dependence
- **5-9:** Severe dependence
- **0-4:** Total dependence

**2. FUNCTIONAL INDEPENDENCE MEASURE (FIM):**

**Purpose:** Assess severity of disability and burden of care

**Domains (18 items, scored 1-7, maximum 126):**
- **Self-care (6 items):** Eating, grooming, bathing, dressing - upper, dressing - lower, toileting
- **Sphincter control (2 items):** Bladder management, bowel management
- **Transfers (3 items):** Bed, chair, wheelchair; Toilet; Tub, shower
- **Locomotion (2 items):** Walk/wheelchair; Stairs
- **Communication (2 items):** Comprehension; Expression
- **Social cognition (3 items):** Social interaction; Problem-solving; Memory

**Scoring:**
- **1:** Total assistance (performs <25% of task)
- **2:** Maximal assistance (performs 25-49% of task)
- **3:** Moderate assistance (performs 50-74% of task)
- **4:** Minimal contact assistance (performs 75%+ of task)
- **5:** Supervision or setup (independent with supervision or setup)
- **6:** Modified independence (independent with device or takes >2x normal time)
- **7:** Complete independence (no assistance, no device, normal time)

**Interpretation:**
- **126:** Independent
- **108-125:** Modified independence
- **90-107:** Minimal assistance
- **72-89:** Moderate assistance
- **54-71:** Maximal assistance
- **18-53:** Total assistance

**3. FUNCTIONAL ASSESSMENT MEASURE (FAM):**

**Purpose:** Assess functional outcome after brain injury (stroke, traumatic brain injury)

**Domains (30 items, scored 1-7, maximum 210):**
- **FIM domains** (18 items)
- **Plus 12 additional items:** Cognitive, behavioural, communication items (attention, memory, organisation, safety)

**Scoring:** Same as FIM (1-7 scale)

**4. MOBILITY ASSESSMENT:**

**Timed Up and Go (TUG) test:**
- **Procedure:** Patient rises from armchair, walks 3 meters, turns, walks back, sits down
- **Timing:** Normal <10 seconds, frail >20 seconds, falls risk >30 seconds

**10-Metre Walk Test (10MWT):**
- **Procedure:** Patient walks 10 meters at comfortable speed
- **Interpretation:** Normal walking speed 1.2-1.4 m/s, slow walking speed <0.8 m/s (frailty, falls risk)

**6-Minute Walk Test (6MWT):**
- **Procedure:** Patient walks as far as possible in 6 minutes
- **Interpretation:** Normal distance 400-700 meters (age-, sex-, height-adjusted)

**5. COGNITIVE ASSESSMENT:**

**Mini-Mental State Examination (MMSE):**
- **Domains:** Orientation, registration, attention, recall, language, praxis
- **Scoring:** 0-30 (normal ≥27, mild impairment 21-26, moderate impairment 11-20, severe impairment ≤10)

**Montreal Cognitive Assessment (MoCA):**
- **Domains:** Visuospatial, naming, memory, attention, language, abstraction, delayed recall, orientation
- **Scoring:** 0-30 (normal ≥26, mild impairment 18-25, moderate impairment 10-17, severe impairment ≤9)

**6. DEPRESSION AND ANXIETY SCREENING:**

**Hospital Anxiety and Depression Scale (HADS):**
- **Domains:** Anxiety (7 items), depression (7 items)
- **Scoring:** 0-21 (normal 0-7, mild 8-10, moderate 11-14, severe 15-21)

**Patient Health Questionnaire 9-item (PHQ-9):**
- **Scoring:** 0-27 (minimal 0-4, mild 5-9, moderate 10-14, moderately severe 15-19, severe 20-27)

**Generalised Anxiety Disorder 7-item (GAD-7):**
- **Scoring:** 0-21 (minimal 0-4, mild 5-9, moderate 10-14, severe 15-21)

**CARE NEEDS ASSESSMENT:**

**Social care needs:**
- **Activities of daily living (ADL):** Feeding, dressing, bathing, toileting, mobility, transfers
- **Instrumental activities of daily living (IADL):** Shopping, cooking, cleaning, laundry, managing medications, managing finances, using telephone, transportation
- **Continence:** Bladder and bowel control
- **Cognition:** Memory, attention, executive function, safety awareness
- **Behaviour:** Aggression, wandering, night-time disturbance, social inappropriateness
- **Carer support:** Respite, day care, home care, residential care, nursing care

**DISABILITY BENEFITS (UK):**

**Personal Independence Payment (PIP):**
- **Daily living component:** 10 activities (preparing food, taking nutrition, managing therapy, washing and bathing, managing toilet needs, dressing and undressing, communicating verbally, reading and understanding signs, engaging with others face-to-face, making budgeting decisions)
- **Mobility component:** 2 activities (planning and following journeys, moving around)
- **Scoring:** 0, 2, 4, 6, 8, 10, 12 points per activity (standard rate 8 points, enhanced rate 12 points)

**Attendance Allowance (AA):**
- **Eligibility:** State pension age or above, needs supervision or assistance throughout the day or night (or both)
- **Scoring:** Lower rate (day supervision OR night supervision), higher rate (day supervision AND night supervision)

**Employment and Support Allowance (ESA):**
- **Eligibility:** State pension age below, limited capability for work-related activity
- **Support group:** Limited capability for work-related activity (severe illness/disability)
- **Work-related activity group:** Limited capability for work (some work-related activity possible)

**Sources:** BSRM Guidelines, RCP Guidelines, NICE Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["BSRM Guidelines", "RCP Guidelines", "NICE Guidelines"]
            }
        )

    def _handle_general_rehabilitation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """General rehabilitation consultation"""

        return DomainQueryResult(
            domain_name="physical_medicine_rehab",
            answer="""**PHYSICAL MEDICINE AND REHABILITATION**

Physical medicine and rehabilitation (PM&R), also known as rehabilitation medicine or physiatry, is a medical specialty focused on restoring function and improving quality of life for people with physical impairments or disabilities.

**REHABILITATION SPECIALTIES:**

**NEUROLOGICAL REHABILITATION:**
- **Stroke:** Hemiplegia, aphasia, dysphagia, mobility, ADL
- **Traumatic brain injury (TBI):** Cognitive rehabilitation, behavioural management, community reintegration
- **Spinal cord injury:** Tetraplegia, paraplegia, autonomic dysreflexia, bowel/bladder dysfunction
- **Neurodegenerative diseases:** Parkinson's disease, multiple sclerosis, motor neuron disease, Guillain-Barré syndrome

**MUSCULOSKELETAL REHABILITATION:**
- **Orthopaedic rehabilitation:** Joint replacement, fracture rehabilitation, soft tissue injury, tendinopathy
- **Back pain rehabilitation:** Acute low back pain, chronic low back pain, whiplash-associated disorders
- **Sports injury rehabilitation:** Acute sports injuries, chronic tendinopathy, return to sport

**CARDIOPULMONARY REHABILITATION:**
- **Cardiac rehabilitation:** Myocardial infarction, cardiac surgery (CABG, valve surgery), heart failure
- **Pulmonary rehabilitation:** COPD, bronchiectasis, interstitial lung disease, pulmonary hypertension, post-COVID syndrome

**AMPUTEE REHABILITATION:**
- **Lower limb amputation:** Transtibial (BKA), transfemoral (AKA), knee disarticulation, hip disarticulation
- **Upper limb amputation:** Transradial (BEA), transhumeral (AEA), shoulder disarticulation
- **Prosthetic training:** Donning/doffing, standing balance, gait training, functional training

**PAEDIATRIC REHABILITATION:**
- **Developmental delay:** Delayed motor milestones, cerebral palsy
- **Neuromuscular disorders:** Muscular dystrophy, spinal muscular atrophy
- **Acquired brain injury:** Traumatic brain injury, stroke (cerebral sinovenous thrombosis), brain tumour

**REHABILITATION TEAM:**

**Multidisciplinary team (MDT):**
- **Rehabilitation physician:** Medical assessment, diagnosis, treatment coordination
- **Physiotherapist:** Mobility, gait, balance, exercises, manual therapy
- **Occupational therapist:** ADL, home modifications, workplace modifications, assistive devices
- **Speech and language therapist (SALT):** Communication, swallowing, cognition
- **Psychologist:** Adjustment to disability, depression, anxiety, cognitive behavioural therapy (CBT)
- **Nurse:** Wound care, continence, medication, patient education
- **Social worker:** Benefits, housing, care needs assessment, safeguarding

**REHABILITATION INTERVENTIONS:**

**Exercise therapy:**
- **Aerobic exercise:** Walking, cycling, swimming (improves cardiovascular fitness)
- **Resistance training:** Strengthening exercises (improves strength, prevents muscle atrophy)
- **Flexibility exercises:** Stretching exercises (prevents contractures, improves ROM)
- **Balance training:** Standing balance, weight-shifting, Tai Chi (prevents falls)

**Manual therapy:**
- **Soft tissue massage:** Myofascial release, trigger point release
- **Joint mobilisations:** Maitland, Kaltenborn, Mulligan techniques
- **Joint manipulation:** High-velocity, low-amplitude thrust (HVLAT)

**Electrotherapy:**
- **Transcutaneous electrical nerve stimulation (TENS):** Pain relief
- **Interferential therapy (IFT):** Pain relief, muscle stimulation
- **Ultrasound therapy:** Tissue healing, pain relief
- **Low-level laser therapy (LLLT):** Tissue healing, pain relief

**Assistive devices:**
- **Mobility aids:** Walking stick, tripod, frame, rollator, wheelchair (manual or powered)
- **Orthoses:** Ankle-foot orthosis (AFO) for foot drop, wrist splint
- **ADL aids:** Feeding aids, dressing aids, bathing aids, writing aids
- **Communication aids:** Alphabet board, communication device, eye-tracking technology

**REHABILITATION GOALS:**

**SMART goals:**
- **Specific:** Clearly defined goal (e.g., "I want to walk 50 meters independently")
- **Measurable:** Quantifiable outcome (e.g., "50 meters in <2 minutes")
- **Achievable:** Realistic given impairment and prognosis
- **Relevant:** Meaningful to patient (e.g., return to work, play with grandchildren)
- **Time-bound:** Set timeframe for achieving goal (e.g., "within 6 weeks")

**Examples:**
- **Mobility:** Walk 10 meters independently with walking stick within 2 weeks
- **ADL:** Independent dressing (upper and lower body) within 4 weeks
- **Community:** Independent community ambulation (walk to local shops) within 3 months
- **Work:** Return to work (modified duties) within 6 months

**Sources:** BSRM Guidelines, NICE Guidelines, RCP Guidelines""",
            confidence=0.85,
            metadata={
                "urgency": "non-urgent",
                "specialty": "physical_medicine_rehab",
                "sources": ["BSRM Guidelines", "NICE Guidelines", "RCP Guidelines"]
            }
        )


def create_physical_medicine_rehab_domain():
    """Factory function for Physical Medicine and Rehabilitation Domain"""
    return PhysicalMedicineRehabDomain()
