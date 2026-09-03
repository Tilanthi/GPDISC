"""
Neurology Domain for GPDISC
Comprehensive neurology consultation covering stroke, headaches, movement disorders,
neuromuscular conditions, and other neurological disorders.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class NeurologyDomain(BaseDomainModule):
    """
    Neurology Specialist Domain

    Covers:
    - Stroke management and prevention
    - Headache and migraine management
    - Movement disorders (Parkinson's, tremor, dystonia)
    - Neuromuscular conditions
    - Epilepsy (basic)
    - Multiple sclerosis
    - Peripheral neuropathy
    - Dementia and cognitive impairment
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="neurology",
            version="1.0.0",
            dependencies=[],
            description="Neurology: stroke, headaches, movement disorders, neuromuscular conditions, MS, neuropathy, dementia",
            keywords=[
                # Stroke
                "stroke", "tia", "transient ischaemic attack", "mini stroke",
                "cerebrovascular", "brain attack", "ischaemic stroke",
                "haemorrhagic stroke", "intracerebral bleed", "subarachnoid",

                # Headaches
                "headache", "migraine", "tension headache", "cluster headache",
                "cephalgia", "head pain", "facial pain", "trigeminal neuralgia",

                # Movement disorders
                "parkinson", "parkinsonism", "tremor", "shaking",
                "dystonia", "chorea", "huntington", "dyskinesia",
                "restless leg", "rls", "akathisia",

                # Neuromuscular
                "neuromuscular", "myasthenia", "gravis", "muscle weakness",
                "muscle atrophy", "motor neuron", "als", "lou gehrig",
                "peripheral neuropathy", "neuropathy", "nerve pain",

                # Demyelinating
                "multiple sclerosis", "ms", "demyelinating", "relapse",
                "optic neuritis", "transverse myelitis",

                # Cognitive
                "dementia", "alzheimer", "cognitive impairment", "memory loss",
                "confusion", "delirium",

                # Other neurological
                "neurology", "neurological", "brain", "spinal cord", "nerve",
                "seizure", "fit", "convulsion", "epilepsy",
                "faint", "syncope", "collapse", "blackout",
                "vertigo", "dizziness", "balance", "ataxia", "gait"
            ],
            capabilities=[
                "stroke_assessment",
                "headache_management",
                "movement_disorder_evaluation",
                "neuromuscular_assessment",
                "dementia_screening",
                "neurological_investigation_interpretation"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """Process neurology query"""

        query_lower = query.lower()

        # Stroke assessment
        if any(term in query_lower for term in ["stroke", "tia", "transient ischaemic", "cerebrovascular"]):
            return self._handle_stroke_query(query, context)

        # Headache evaluation
        elif any(term in query_lower for term in ["headache", "migraine", "cluster headache", "tension headache"]):
            return self._handle_headache_query(query, context)

        # Movement disorders
        elif any(term in query_lower for term in ["parkinson", "tremor", "dystonia", "chorea", "movement disorder"]):
            return self._handle_movement_disorder_query(query, context)

        # Neuromuscular
        elif any(term in query_lower for term in ["neuromuscular", "myasthenia", "muscle weakness", "neuropathy"]):
            return self._handle_neuromuscular_query(query, context)

        # Dementia
        elif any(term in query_lower for term in ["dementia", "alzheimer", "cognitive impairment", "memory loss"]):
            return self._handle_dementia_query(query, context)

        # Syncope
        elif any(term in query_lower for term in ["syncope", "faint", "collapse", "blackout"]):
            return self._handle_syncope_query(query, context)

        # General neurology
        else:
            return self._handle_general_neurology_query(query, context)

    def _handle_stroke_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle stroke-related queries"""

        answer = """**NEUROLOGY: STROKE ASSESSMENT**

**Immediate Action Required:**
If this is an acute stroke (symptoms < 4.5 hours), call emergency services (999/911) immediately.

**FAST Assessment:**
• **F**ace - Facial drooping?
• **A**rms - Arm weakness?
• **S**peech - Speech difficulty?
• **T**ime - Time to call emergency services

**Stroke Classification:**
• Ischaemic stroke (85%) - thrombotic or embolic
• Haemorrhagic stroke (15%) - intracerebral or subarachnoid
• TIA (Transient Ischaemic Attack) - resolves within 24 hours

**Investigation:**
• Non-contrast CT head (immediate) - exclude haemorrhage
• CT angiography - identify vessel occlusion
• MRI brain (if available) - DWI for acute infarction
• Carotid Doppler - if anterior circulation stroke
• Echocardiogram - if cardioembolic suspected
• ECG + telemetry - detect atrial fibrillation
• Bloods: FBC, U&E, CRP, coagulation profile, HbA1c, lipids

**Management (Ischaemic Stroke):**
• Thrombolysis (alteplase) if < 4.5 hours and no contraindications
• Thrombectomy (mechanical clot retrieval) if large artery occlusion < 6 hours
• Antiplatelet therapy (aspirin 300mg loading, then 75mg daily)
• High-intensity statin (atorvastatin 80mg)
• Blood pressure management (target < 140/90 after 24 hours)
• Dysphagia screening before oral intake
• Early mobilization and stroke rehabilitation

**Secondary Prevention:**
• Antiplatelet: aspirin + clopidogrel (for 90 days) then aspirin alone OR long-term clopidogrel
• Statin: atorvastatin 80mg daily
• Blood pressure: target < 130/80
• Anticoagulation if atrial fibrillation detected (DOAC preferred)
• Lifestyle: smoking cessation, diet, exercise, alcohol moderation

**Red Flags:**
• Sudden severe headache ("thunderclap") - suspect subarachnoid haemorrhage
• Decreasing consciousness - suspect raised ICP
• Progressive symptoms - consider stroke mimic

**Evidence:** NICE NG128, RCP Stroke Guidelines, AHA/ASA Guidelines

**Urgency:** URGENT - Emergency admission required for acute stroke"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "neurology",
                "subspecialty": "stroke",
                "urgency": "urgent",
                "sources": ["NICE NG128", "RCP Stroke Guidelines", "AHA/ASA Guidelines"]
            }
        )

    def _handle_headache_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle headache-related queries"""

        answer = """**NEUROLOGY: HEADACHE ASSESSMENT**

**Headache Red Flags (SNOOP4):**
• **S**ystemic symptoms - fever, weight loss
• **N**eurologic symptoms - confusion, weakness, papilledema
• **O**nset sudden, abrupt ("thunderclap")
• **O**lder - new onset > 50 years old
• **P**ositional - worsened by lying flat
• **P**recipitated by Valsalva
• **P**regnancy or postpartum
• **P**apilledema

**Common Headache Types:**

**1. Tension-Type Headache:**
• Bilateral, band-like pressure
• Mild to moderate intensity
• No nausea/vomiting, no photophobia
• Stress-related
• Treatment: simple analgesics, stress management

**2. Migraine:**
• Unilateral (often), throbbing
• Moderate to severe intensity
• Nausea/vomiting, photophobia, phonophobia
• Aura in 25% (visual, sensory, speech)
• Triggers: stress, food, hormones, sleep
• Treatment: triptans (sumatriptan), NSAIDs, antiemetics
• Prevention: propranolol, topiramate, amitriptyline

**3. Cluster Headache:**
• Severe unilateral orbital/temporal pain
• 15-180 minutes, 1-8 times/day
• Associated with lacrimation, rhinorrhea, ptosis
• More common in males, smokers
• Treatment: oxygen 100%, sumatriptan SC/IN, verapamil prevention

**Investigation:**
• Most headaches: clinical diagnosis, no imaging needed
• Red flags present: CT/MRI brain
• Chronic daily headache: MRI to exclude secondary cause
• Sudden onset severe headache: CT to exclude SAH

**Management:**
• Identify and avoid triggers
• Acute treatment: simple analgesics, triptans
• Preventive treatment if frequent (>4 days/month)
• Lifestyle: regular sleep, hydration, stress management

**Evidence:** NICE CG150, BASH Guidelines, ICHD-3 Classification

**Urgency:** URGENT if red flags present"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "neurology",
                "subspecialty": "headache",
                "sources": ["NICE CG150", "BASH Guidelines", "ICHD-3"]
            }
        )

    def _handle_movement_disorder_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle movement disorder queries"""

        answer = """**NEUROLOGY: MOVEMENT DISORDERS**

**Parkinson's Disease:**

**Diagnostic Features (UK Brain Bank Criteria):**
• Bradykinesia (slowness of movement) - ESSENTIAL
• PLUS at least one of:
  - Resting tremor (4-6 Hz "pill-rolling")
  - Rigidity (lead-pipe or cogwheel)
  - Postural instability

**Other Features:**
• Hypomimia (reduced facial expression)
• Micrographia (small handwriting)
• Shuffling gait, reduced arm swing
• Freezing of gait
• Speech: hypophonia, monotone
• Autonomic: constipation, urinary urgency

**Investigation:**
• Clinical diagnosis (no definitive test)
• Consider DaTSCAN if diagnosis uncertain
• Exclude other causes (medications, vascular, normal pressure hydrocephalus)

**Management:**
• Levodopa + dopamine decarboxylase inhibitor (co-beneldopa, co-careldopa)
• Dopamine agonists (ropinirole, pramipexole) - younger patients
• MAO-B inhibitors (selegiline, rasagiline)
• COMT inhibitors (entacapone) - for wearing-off
• Anticholinergics - for tremor only
• Physiotherapy, occupational therapy, speech therapy
• Deep brain stimulation (STN or GPi) for advanced disease

**Essential Tremor:**
• Action tremor (not resting)
• Bilateral, often hereditary
• Worsened by stress, caffeine
• Treatment: propranolol, primidone

**Dystonia:**
• Sustained muscle contractions, abnormal postures
• Focal (cervical, writer's cramp), segmental, generalized
• Treatment: botulinum toxin injections, anticholinergics

**Evidence:** NICE NG71, Parkinson's UK Guidelines, MDS Criteria

**Urgency:** ROUTINE (unless rapid progression or red flags present)"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "neurology",
                "subspecialty": "movement_disorders",
                "sources": ["NICE NG71", "Parkinson's UK"]
            }
        )

    def _handle_neuromuscular_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle neuromuscular queries"""

        answer = """**NEUROLOGY: NEUROMUSCULAR DISORDERS**

**Myasthenia Gravis:**

**Key Features:**
• Fatigable muscle weakness
• Ocular: ptosis, diplopia (most common presentation)
• Bulbar: dysphagia, dysarthria, fatigable jaw
• Limb: proximal > distal
• Respiratory: crisis (life-threatening)

**Diagnosis:**
• Anti-AChR antibodies (80-85% positive)
• Anti-MuSK antibodies (5-10% of AChR-negative)
• Edrophonium (Tensilon) test - rarely used now
• EMG: decremental response on repetitive stimulation
• Single-fiber EMG (most sensitive)
• CT chest for thymoma/thymic hyperplasia

**Management:**
• Acetylcholinesterase inhibitors: pyridostigmine
• Immunosuppression: prednisolone, azathioprine, mycophenolate
• Thymectomy (if thymoma or generalized MG)
• Plasma exchange or IVIG for crisis
• Mycophenolate mofetil for refractory cases
• Avoid: aminoglycosides, fluoroquinolones, beta-blockers, magnesium

**Peripheral Neuropathy:**

**Classification:**
• Demyelinating vs axonal
• Sensory vs motor vs autonomic
• Acute vs chronic
• Hereditary vs acquired

**Common Causes:**
• Diabetes mellitus (most common)
• B12 deficiency
• Alcohol
• Medications (chemotherapy, isoniazid, metronidazole)
• Paraproteinaemia
• Vasculitis
• CIDP (chronic inflammatory demyelinating polyneuropathy)
• GBS (Guillain-Barré syndrome)

**Investigation:**
• Nerve conduction studies/EMG
• Bloods: B12, folate, glucose, HbA1c, LFT, protein electrophoresis
• Autoimmune screen: ANA, ENA, ANCA
• Infection screen: HIV, hepatitis, Lyme, syphilis
• Nerve biopsy if vasculitis suspected
• Genetic testing if hereditary suspected

**Management:**
• Treat underlying cause
• Symptomatic: analgesia, amitriptyline, gabapentin, pregabalin
• Physiotherapy and occupational therapy
• Immunotherapy for inflammatory neuropathies

**Motor Neuron Disease (MND/ALS):**

**Key Features:**
• Progressive weakness
• UMN signs: spasticity, hyperreflexia, Babinski
• LMN signs: wasting, fasciculations, weakness
• No sensory involvement
• No sphincter involvement (early)
• Bulbar: dysarthria, dysphagia

**Evidence:** NICE NG138, MDA Guidelines, AANEM Guidelines

**Urgency:** URGENT for GBS or myasthenic crisis"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "neurology",
                "subspecialty": "neuromuscular",
                "sources": ["NICE NG138", "MDA Guidelines", "AANEM"]
            }
        )

    def _handle_dementia_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle dementia queries"""

        answer = """**NEUROLOGY: DEMENTIA AND COGNITIVE IMPAIRMENT**

**Dementia Subtypes:**

**1. Alzheimer's Disease (60-80%):**
• Progressive memory impairment (episodic memory first)
• Aphasia, apraxia, agnosia, executive dysfunction
• Insidious onset, gradual progression
• Risk factors: age, APOE ε4, vascular risk factors

**2. Vascular Dementia:**
• Stepwise decline or acute onset
• Focal neurological signs
• Imaging evidence of cerebrovascular disease
• History of stroke/TIA

**3. Dementia with Lewy Bodies:**
• Fluctuating cognition
• Visual hallucinations
• Parkinsonism
• Neuroleptic sensitivity (severe reaction)
• REM sleep behaviour disorder

**4. Frontotemporal Dementia:**
• Early behavioural change or language problems
• Disinhibition, apathy, loss of empathy
• Relatively preserved memory early on
• Younger onset (often 45-65 years)

**Investigation:**
• Blood tests: FBC, U&E, LFT, TFT, B12, folate, calcium, glucose, HbA1c, syphilis serology
• CT brain: exclude other pathologies
• MRI brain: if atypical features or young onset
• SPECT/PET: if diagnostic uncertainty
• Cognitive assessment: MMSE, MoCA, Addenbrooke's
• Depression screen: GDS-15
• Neuropsychology testing: if early onset or atypical

**Management:**
• Cholinesterase inhibitors (donepezil, rivastigmine, galantamine) for Alzheimer's, DLB, PDD
• Memantine for moderate-severe Alzheimer's or if cholinesterase inhibitors not tolerated
• Treat depression if present
• Manage BPSD (behavioural and psychological symptoms)
• Avoid antipsychotics if possible (increased mortality in dementia)
• Cognitive stimulation therapy
• Exercise, social engagement, music therapy
• Advance care planning, Lasting Power of Attorney

**Driving:**
• Must inform DVLA if diagnosed with dementia
• Driving assessment may be required

**Evidence:** NICE NG97, SCAN Guidelines, DSM-5 Criteria

**Urgency:** ROUTINE (unless delirium or rapid progression present)"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "neurology",
                "subspecialty": "dementia",
                "sources": ["NICE NG97", "SCAN Guidelines", "DSM-5"]
            }
        )

    def _handle_syncope_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle syncope queries"""

        answer = """**NEUROLOGY: SYNCOPE (FAINTING)**

**Definition:**
Transient loss of consciousness (T-LOC) due to cerebral hypoperfusion, characterized by rapid onset, short duration, and spontaneous complete recovery.

**Common Causes:**

**1. Vasovagal Syncope (Simple Faint) - 60%:**
• Triggered by emotion, pain, standing
• Prodrome: nausea, sweating, warmth, visual changes
• Rapid recovery
• Diagnosis: clinical (no investigation needed if typical)

**2. Cardiac Syncope - 15%:**
• Arrhythmia: SVT, VT, complete heart block, long QT
• Structural: HOCM, aortic stenosis, pulmonary embolism
• No warning, sudden loss of consciousness
• May occur during exercise
• HIGH MORTALITY RISK

**3. Orthostatic Hypotension - 10%:**
• Drop in BP on standing (>20/10 mmHg)
• Causes: dehydration, medications (diuretics, alpha-blockers, antihypertensives), autonomic failure
• Occurs within 3 minutes of standing

**Investigation:**
• ECG (all patients) - look for arrhythmia, conduction disease, prolonged QT
• Echocardiogram - if cardiac murmur or suspected structural disease
• 24-hour Holter (or event recorder) - if recurrent syncope
• Head-up tilt test - if vasovagal suspected and atypical
• Carotid sinus massage - if > 40 years old and syncope triggered by head turning
• Bloods: FBC, U&E, glucose
• CT/MRI brain - only if focal neurological signs or head trauma

**Red Flags (Cardiac Syncope):**
• Exertional syncope
• Family history of sudden cardiac death (< 40 years)
• Abnormal ECG
• Heart failure or structural heart disease
• No prodrome (no warning)

**Management:**
• Treat underlying cause
• Avoid triggers
• Stop or reduce offending medications
• Increase fluid and salt intake (for vasovagal/orthostatic)
• Compression stockings (for orthostatic)
• Pacemaker for bradyarrhythmias
• ICD for ventricular arrhythmias
• Educate on recognizing prodrome and采取 maneuvers

**Driving:**
• Must inform DVLA if syncope has occurred while driving
• Group 1 entitlement: cease driving until 4 weeks symptom-free and cause identified/treated

**Evidence:** NICE CG109, ESC Guidelines on Syncope

**Urgency:** URGENT if cardiac syncope suspected"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "neurology",
                "subspecialty": "syncope",
                "sources": ["NICE CG109", "ESC Guidelines"]
            }
        )

    def _handle_general_neurology_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general neurology queries"""

        answer = """**NEUROLOGY: GENERAL NEUROLOGICAL CONSULTATION**

**Common Neurological Conditions:**

**Central Nervous System:**
• Stroke and cerebrovascular disease
• Headache disorders (migraine, tension, cluster)
• Movement disorders (Parkinson's, essential tremor, dystonia)
• Dementia and cognitive impairment
• Multiple sclerosis and demyelinating disorders
• Epilepsy and seizure disorders
• Brain tumours
• CNS infections (meningitis, encephalitis, abscess)

**Peripheral Nervous System:**
• Peripheral neuropathy
• Myasthenia gravis
• Motor neuron disease
• Guillain-Barré syndrome
• CIDP
• Muscular dystrophies

**Autonomic Nervous System:**
• Syncope and orthostatic hypotension
• Autonomic neuropathy

**Common Neurological Investigations:**

**Imaging:**
• CT head (acute: haemorrhage, trauma, stroke)
• MRI brain (structural detail, tumours, demyelination)
• CT/MRI angiography (vascular imaging)
• DaTSCAN (parkinsonian syndromes)

**Neurophysiology:**
• EEG (epilepsy, encephalopathy)
• Nerve conduction studies (neuropathy, entrapment)
• EMG (myopathy, MND, radiculopathy)
• Evoked potentials (demyelination)

**Laboratory:**
• Lumbar puncture (infection, inflammation, malignancy)
• Blood tests (autoimmune, infection, metabolic)
• Genetic testing (hereditary disorders)

**Neurology Emergency Signs:**
• Sudden onset focal neurological deficit - **STROKE**
• Thunderclap headache - **SUBARACHNOID HAEMORRHAGE**
• Fever + headache + neck stiffness - **MENINGITIS**
• Rapidly progressive weakness - **GBS**
• Seizure > 5 minutes or recurrent without recovery - **STATUS EPILEPTICUS**
• Decreasing consciousness + focal signs - **RAISED ICP**

**Referral Criteria:**
• Any red flag signs
• Progressive neurological deficit
• Diagnostic uncertainty
• Require specialist investigation
• Require specialist treatment (e.g., disease-modifying therapy for MS)

**Evidence:** NICE Guidelines, RCP Guidelines, AAN Guidelines

**Urgency:** ASSESSED BASED ON CONDITION"""

        return DomainQueryResult(
            domain_name="neurology",
            answer=answer,
            confidence=0.82,
            metadata={
                "specialty": "neurology",
                "sources": ["NICE Guidelines", "RCP Guidelines", "AAN"]
            }
        )


def create_neurology_domain():
    """Factory function for Neurology domain"""
    return NeurologyDomain()
