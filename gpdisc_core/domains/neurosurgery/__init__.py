"""
Neurosurgery Domain Module for GPDISC

Comprehensive neurosurgery consultation covering brain, spine, and peripheral nerve surgery.

Evidence-based guidelines from:
- Society of British Neurological Surgeons (SBNS)
- National Institute for Health and Care Excellence (NICE)
- Congress of Neurological Surgeons (CNS)
- European Association of Neurosurgical Societies (EANS)

Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class NeurosurgeryDomain(BaseDomainModule):
    """
    Neurosurgery specialty domain for GPDISC

    Covers brain surgery, spine surgery, and peripheral nerve surgery.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="neurosurgery",
            version="1.0.0",
            dependencies=[],
            description="Neurosurgery: brain, spine, and peripheral nerve surgery",
            keywords=[
                # Brain surgery
                "brain tumour", "brain tumor", "glioma", "meningioma", "pituitary adenoma",
                "acoustic neuroma", "vestibular schwannoma", "metastasis", "brain metastasis",
                "craniotomy", "neurosurgery", "brain surgery", "neurosurgeon",
                "subdural haematoma", "subdural hematoma", "sdh", "chronic subdural",
                "extradural haematoma", "epidural hematoma", "edh", " extradural",
                "subarachnoid haemorrhage", "subarachnoid hemorrhage", "sah", "aneurysm",
                "intracerebral haemorrhage", "intracerebral hemorrhage", "ich", "brain bleed",
                "hydrocephalus", "vp shunt", "ventriculoperitoneal shunt", "shunt",
                "normal pressure hydrocephalus", "nph",
                "head injury", "traumatic brain injury", "tbi", "concussion", "brain injury",
                "skull fracture", "depressed skull fracture", "compound skull fracture",

                # Spine surgery
                "spine surgery", "spinal surgery", "back surgery", "neck surgery",
                "discectomy", "microdiscectomy", "herniated disc", "slipped disc",
                "laminectomy", "decompression", "spinal stenosis", "lumbar stenosis",
                "spinal fusion", "scoliosis surgery", "spinal deformity",
                "vertebroplasty", "kyphoplasty", "spinal fracture", "compression fracture",
                "spinal tumour", "spinal tumor", "spinal metastasis", "spinal cord tumour",
                "cervical myelopathy", "cervical spondylotic myelopathy", "csm",
                "cauda equina", "cauda equina syndrome", "ces", "spinal cord compression",
                "disc prolapse", "disc herniation", "sciatica", "radiculopathy",

                # Peripheral nerve
                "carpal tunnel", "carpal tunnel syndrome", "cts", "carpal tunnel release",
                "ulnar nerve", "cubital tunnel", "ulnar nerve entrapment",
                "peripheral nerve", "nerve injury", "nerve compression", "nerve entrapment",
                "tarsal tunnel", "morton's neuroma", "ganglion cyst",

                # General neurosurgery
                "neuro", "neurosurgical", "neurosurgeon", "brain", "spinal cord",
                "neuro-oncology", "neurovascular", "spine", "vertebrae", "disc", "nerve"
            ],
            capabilities=[
                "brain_tumour_surgery",
                "traumatic_brain_injury_management",
                "neurovascular_emergency_management",
                "hydrocephalus_management",
                "spine_surgery_consultation",
                "spinal_cord_compression_management",
                "peripheral_nerve_surgery",
                "preoperative_assessment"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process neurosurgery query

        Routes to appropriate handler based on query content.
        """
        query_lower = query.lower()

        # NEUROSURGICAL EMERGENCIES - Highest priority
        if any(term in query_lower for term in [
            "subarachnoid haemorrhage", "subarachnoid hemorrhage", "sah", "aneurysm rupture",
            " extradural haematoma", "epidural hematoma", "edh", "acute subdural",
            "cauda equina syndrome", "cauda equina", "ces", "spinal cord compression",
            "traumatic brain injury", "tbi", "severe head injury"
        ]):
            return self._handle_neurosurgical_emergency(query, context)

        # Brain tumour
        elif any(term in query_lower for term in [
            "brain tumour", "brain tumor", "glioma", "meningioma", "pituitary adenoma",
            "acoustic neuroma", "vestibular schwannoma", "brain metastasis", "brain cancer"
        ]):
            return self._handle_brain_tumour_query(query, context)

        # Subdural haematoma
        elif any(term in query_lower for term in [
            "subdural haematoma", "subdural hematoma", "sdh", "chronic subdural"
        ]):
            return self._handle_subdural_query(query, context)

        # Hydrocephalus
        elif any(term in query_lower for term in [
            "hydrocephalus", "vp shunt", "ventriculoperitoneal shunt", "normal pressure hydrocephalus"
        ]):
            return self._handle_hydrocephalus_query(query, context)

        # Spine surgery
        elif any(term in query_lower for term in [
            "spine surgery", "spinal surgery", "back surgery", "discectomy",
            "laminectomy", "spinal fusion", "spinal stenosis", "sciatica",
            "disc prolapse", "disc herniation", "radiculopathy", "slipped disc"
        ]):
            return self._handle_spine_surgery_query(query, context)

        # Cauda equina
        elif any(term in query_lower for term in [
            "cauda equina", "cauda equina syndrome", "ces", "saddle anaesthesia"
        ]):
            return self._handle_cauda_equina_query(query, context)

        # Cervical myelopathy
        elif any(term in query_lower for term in [
            "cervical myelopathy", "csm", "cervical myelopathy", "spinal cord compression"
        ]):
            return self._handle_cervical_myelopathy_query(query, context)

        # Peripheral nerve
        elif any(term in query_lower for term in [
            "carpal tunnel", "cts", "carpal tunnel syndrome", "ulnar nerve", "cubital tunnel",
            "peripheral nerve", "nerve compression", "nerve entrapment"
        ]):
            return self._handle_peripheral_nerve_query(query, context)

        # General neurosurgery
        else:
            return self._handle_general_neurosurgery_query(query, context)

    def _handle_neurosurgical_emergency(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle neurosurgical emergencies requiring urgent intervention"""
        query_lower = query.lower()

        # Subarachnoid haemorrhage
        if any(term in query_lower for term in [
            "subarachnoid haemorrhage", "subarachnoid hemorrhage", "sah", "aneurysm rupture"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**SUBARACHNOID HAEMORRHAGE (SAH) - NEUROSURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent CT head** (non-contrast)
- **Urgent neurosurgical involvement**
- **Transfer to neurosurgical centre**

**CLINICAL PRESENTATION:**
- **Sudden severe headache** ("worst headache of my life")
- **Thunderclap onset** (seconds to peak)
- **Neck stiffness** (meningeal irritation)
- **Photophobia** (light sensitivity)
- **Nausea, vomiting**
- **Decreased conscious level**
- **Focal neurological deficit** (depending on site)
- **Seizures**

**DIAGNOSIS:**

**1. Non-contrast CT Head**
- Sensitivity ~95% within 24 hours
- Sensitivity ~50% after 5-7 days
- Shows blood in subarachnoid space

**2. Lumbar Puncture (if CT negative)**
- Perform >12 hours after symptom onset
- Look for:
  - **Xanthochromia** (yellow tint - bilirubin)
  - **Red blood cells** (do not clear)
- Spectrophotometry most sensitive

**3. CT Angiography**
- Identify aneurysm
- Size, location, morphology
- Guide treatment planning

**IMMEDIATE MANAGEMENT:**

**1. Resuscitation**
- **ABC approach**
- Secure airway if GCS <8
- IV access, bloods
- Monitor neurological status

**2. Blood Pressure Control**
- Target SBP <140 mmHg until aneurysm secured
- IV labetalol or nicardipine
- Avoid hypotension (maintain cerebral perfusion)

**3. Analgesia**
- IV opioids (morphine/fentanyl)
- Avoid sedation that obscures neurological assessment

**4. Prevention of Rebleeding**
- Bed rest
- Stool softeners (avoid straining)
- Antifibrinolytics (tranexamic acid) - controversial
- Secure aneurysm as soon as possible

**ANEURYSM TREATMENT:**

**1. Endovascular Coiling**
- **First-line** for most aneurysms
- Advantages:
  - Less invasive
  - Lower morbidity/mortality
  - Shorter hospital stay
- Disadvantages:
  - Higher recurrence rate
  - May require retreatment

**2. Surgical Clipping**
- Indicated if:
  - Coiling not anatomically suitable
  - Large/giant aneurysms
  - Middle cerebral artery aneurysms (better outcomes)
  - Young patients (durability)
  - Haematomas requiring evacuation

**COMPLICATIONS:**
- **Rebleeding:** 20% within 14 days (highest risk)
- **Vasospasm:** Days 4-14, may cause delayed ischaemia
- **Hydrocephalus:** 20% (may require shunt)
- **Seizures:** 5-10%
- **Neurological deficit:** Stroke, cognitive impairment

**PROGNOSIS:**
- Mortality: 30-40% overall
- Good outcome: 50-60%
- Worse with:
  - Poor WFNS grade on admission
  - Rebleeding
  - Vasospasm
  - Delayed treatment

**WFNS GRADING (World Federation of Neurological Surgeons):**
- **Grade I:** GCS 15, no motor deficit
- **Grade II:** GCS 13-14, no motor deficit
- **Grade III:** GCS 13-14, motor deficit
- **Grade IV:** GCS 7-12
- **Grade V:** GCS 3-6

**EVIDENCE:** NICE NG228, EANN Guidelines""",
                confidence=0.97,
                reasoning_trace=[
                    "Identified subarachnoid haemorrhage - neurosurgical emergency",
                    "Applied WFNS grading",
                    "Prioritized aneurysm securing (coiling or clipping)"
                ],
                capabilities_used=["neurovascular_emergency_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "subarachnoid_haemorrhage",
                    "intervention": "coiling_or_clipping"
                }
            )

        # Extradural haematoma
        elif any(term in query_lower for term in [
            "extradural haematoma", "epidural hematoma", "edh", "epidural"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**EXTRADURAL HAEMATOMA (EDH) - NEUROSURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent CT head**
- **Urgent neurosurgical involvement**
- **TIME IS BRAIN** - surgical evacuation if symptomatic

**CLINICAL PRESENTATION:**
- **Head injury** (usually temporal bone fracture)
- **Lucid interval** (brief period of consciousness between injury and deterioration)
- **Headache**
- **Vomiting**
- **Decreasing conscious level**
- **Uncal herniation** (ipilateral dilated pupil, contralateral hemiparesis)
- **Coma** if untreated

**CAUSES:**
- **Trauma** (95%)
- Middle meningeal artery rupture (temporal bone fracture)
- Venous (less common, slower progression)

**DIAGNOSIS:**
- **CT head** - lens-shaped (biconvex) hyperdensity
- Typically temporal or temporoparietal
- May cross suture lines but NOT dural reflections
- Midline shift if large

**IMMEDIATE MANAGEMENT:**

**1. Resuscitation**
- **ABC approach**
- Secure airway if GCS <8
- IV access
- Monitor GCS, pupils, vital signs

**2. Reduce ICP**
- Head of bed 30°
- Mannitol 0.5-1 g/kg IV
- Hyperventilation (target PaCO2 4.0-4.5 kPa)
- Sedation if intubated

**3. Urgent Neurosurgical Referral**
- Transfer to neurosurgical centre
- Immediate surgical evacuation

**SURGICAL TREATMENT:**

**Craniotomy and Evacuation**
- **Indicated for:**
  - Symptomatic EDH (any size)
  - Asymptomatic EDH >1 cm thickness or midline shift >5 mm
  - Rapidly expanding EDH
- **Procedure:**
  - Burr hole or craniotomy
  - Evacuate clot
  - Control bleeding (diathermy, bone wax)
  - Drain insertion
- **Outcomes:** Excellent if treated early (<2 hours from deterioration)

**CONSERVATIVE MANAGEMENT:**
- **Indicated for:**
  - Asymptomatic EDH
  - Small EDH (<1 cm)
  - No midline shift
  - Comorbidities prohibit surgery
- **Serial CT scans** (q6-12 hours initially)

**PROGNOSIS:**
- **Mortality:** 5-30% (lower if treated early)
- **Good outcome:** 80-90% if rapidly evacuated
- **Poor prognostic factors:**
  - Delayed presentation (>2 hours from symptom onset)
  - GCS <8 on admission
  - Fixed dilated pupil
  - Associated intracranial injuries

**COMPLICATIONS:**
- **Uncal herniation** - if untreated
- **Residual haematoma**
- **Seizures** (5-10%)
- **Infection** (rare)

**EVIDENCE:** NICE NG232, SBNS Guidelines""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified extradural haematoma - neurosurgical emergency",
                    "Applied classic lucid interval presentation",
                    "Surgical evacuation if symptomatic"
                ],
                capabilities_used=["traumatic_brain_injury_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "extradural_haematoma",
                    "intervention": "surgical_evacuation"
                }
            )

        # Acute subdural haematoma
        elif any(term in query_lower for term in [
            "acute subdural", "acute sdh", "severe head injury", "traumatic brain injury"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**ACUTE SUBDURAL HAEMATOMA (SDH) - NEUROSURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent CT head**
- **Urgent neurosurgical involvement**
- **High mortality** - aggressive management indicated

**CLINICAL PRESENTATION:**
- **Head injury** (often severe)
- **Decreasing conscious level**
- **Headache, vomiting**
- **Focal neurological deficit** (hemiparesis, aphasia)
- **Dilated pupil** (ipsilateral to lesion if uncal herniation)
- **Coma** (if severe or rapid deterioration)

**CAUSES:**
- **Trauma** (most common)
- Bridging vein rupture
- Often associated with:
  - Cerebral contusion
  - Diffuse axonal injury
  - Intracerebral haematoma

**DIAGNOSIS:**
- **CT head** - crescentic (concave) hyperdensity over convexity
- May cross suture lines but NOT dural reflections
- Midline shift common
- Underlying brain injury often present

**IMMEDIATE MANAGEMENT:**

**1. Resuscitation**
- **ABC approach**
- Secure airway if GCS <8
- IV access, bloods
- Monitor GCS, pupils, vital signs

**2. Reduce ICP**
- Head of bed 30°
- Mannitol 0.5-1 g/kg IV
- Hyperventilation (target PaCO2 4.0-4.5 kPa)
- Sedation if intubated

**3. Urgent Neurosurgical Referral**
- Transfer to neurosurgical centre
- Consider surgical evacuation

**SURGICAL TREATMENT:**

**Craniotomy and Evacuation**
- **Indicated for:**
  - Symptomatic acute SDH (any size)
  - Thickness >10 mm or midline shift >5 mm (even if asymptomatic)
  - Rapid neurological deterioration
- **Procedure:**
  - Large craniotomy flap
  - Evacuate clot
  - Control bleeding
  - Decompressive craniectomy if brain swollen
  - Drain insertion
- **Outcomes:** Variable, depends on underlying brain injury

**CONSERVATIVE MANAGEMENT:**
- **Indicated for:**
  - Small SDH (<10 mm)
  - Minimal midline shift (<5 mm)
  - No neurological deterioration
  - Severe underlying brain injury (poor prognosis)
- **Serial CT scans**
- ICP monitoring if indicated

**PROGNOSIS:**
- **Mortality:** 40-60% (higher than EDH)
- **Good outcome:** 30-50% (depends on associated injuries)
- **Poor prognostic factors:**
  - GCS <8 on admission
  - Fixed dilated pupil
  - Rapid progression
  - Severe associated brain injury
  - Age >65 years

**COMPLICATIONS:**
- **Rebleeding**
- **Cerebral oedema**
- **Infection**
- **Seizures**
- **Hydrocephalus**

**EVIDENCE:** NICE NG232, SBNS Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified acute subdural haematoma - neurosurgical emergency",
                    "Higher mortality than EDH due to associated brain injury",
                    "Surgical evacuation if symptomatic or large"
                ],
                capabilities_used=["traumatic_brain_injury_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "acute_subdural_haematoma",
                    "intervention": "surgical_evacuation"
                }
            )

        # General neurosurgical emergency
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**NEUROSURGICAL EMERGENCIES**

**COMMON NEUROSURGICAL EMERGENCIES:**

**Subarachnoid Haemorrhage (SAH)**
- Thunderclap headache
- Neck stiffness, photophobia
- Urgent CT head + CTA
- Aneurysm securing (coiling or clipping)

**Extradural Haematoma (EDH)**
- Head injury, lucid interval
- Rapid deterioration
- Lens-shaped CT hyperdensity
- Urgent craniotomy and evacuation

**Acute Subdural Haematoma (SDH)**
- Head injury, decreasing conscious level
- Crescentic CT hyperdensity
- Surgical evacuation if symptomatic or large

**Traumatic Brain Injury (TBI)**
- Severe head injury (GCS <8)
- Intracranial haemorrhage
- Cerebral oedema
- ICP monitoring, surgical decompression if indicated

**Cauda Equina Syndrome**
- Low back pain, bilateral leg weakness
- Saddle anaesthesia, urinary retention
- MRI spine, urgent neurosurgical referral
- Surgical decompression if <48 hours

**Spinal Cord Compression**
- Back pain, progressive weakness
- Sensory level, bladder/bowel dysfunction
- MRI spine, urgent neurosurgical referral
- Surgical decompression ± radiotherapy

**PRINCIPLES OF MANAGEMENT:**

**1. Resuscitation**
- ABC approach
- Secure airway if GCS <8
- IV access, monitor GCS

**2. Reduce ICP**
- Head of bed 30°
- Mannitol, hypertonic saline
- Hyperventilation (temporary)
- Sedation, paralysis

**3. Urgent Imaging**
- CT head (emergencies)
- MRI spine (spinal cord compression)

**4. Urgent Neurosurgical Referral**
- Transfer to neurosurgical centre
- Early intervention improves outcomes

**Evidence:** NICE Guidelines, SBNS Guidelines""",
                confidence=0.90,
                reasoning_trace=[
                    "Provided overview of neurosurgical emergencies",
                    "Listed common emergencies and principles",
                    "Emphasized early intervention"
                ],
                capabilities_used=["neurovascular_emergency_management", "traumatic_brain_injury_management"],
                metadata={
                    "urgency": "emergency",
                    "topic": "neurosurgical_emergencies"
                }
            )

    def _handle_brain_tumour_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle brain tumour queries"""
        query_lower = query.lower()

        # Glioma/high-grade glioma
        if any(term in query_lower for term in [
            "glioma", "glioblastoma", "gbm", "high grade glioma", "brain tumour"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**GLIOMA (INCLUDING GLIOBLASTOMA)**

**CLASSIFICATION (WHO GRADE):**

**Grade I (Benign):**
- Pilocytic astrocytoma
- Curative with surgery alone
- Common in children

**Grade II (Low-Grade):**
- Diffuse astrocytoma, oligodendroglioma
- Slow-growing but infiltrative
- Progress to high grade over time

**Grade III (Anaplastic):**
- Anaplastic astrocytoma, oligodendroglioma
- Malignant, faster-growing
- Require surgery + chemoradiotherapy

**Grade IV (Glioblastoma - GBM):**
- Most malignant primary brain tumour
- Rapid progression
- Poor prognosis

**SYMPTOMS:**
- **Headache** (worse in morning, worse with Valsalva)
- **Focal neurological deficit** (weakness, sensory change, speech)
- **Seizures** (30-50%)
- **Cognitive change** (confusion, memory)
- **Raised ICP signs** (nausea, vomiting, papilloedema)

**DIAGNOSIS:**

**1. MRI Brain with Contrast**
- **T1 with contrast** - enhancement pattern
- **T2/FLAIR** - oedema, infiltration
- **Spectroscopy** - metabolite profile (helps grade)
- **Perfusion** - blood flow (high in high grade)

**2. Biopsy/Surgical Resection**
- Histological diagnosis definitive
- Molecular markers (IDH, 1p/19q, MGMT)
- Guide prognosis and treatment

**MANAGEMENT:**

**Surgery:**
- **Goal:** Maximal safe resection
- **Awake craniotomy** if tumour near eloquent areas (speech, motor)
- **Neuronavigation** - GPS for brain surgery
- **5-ALA fluorescence** - tumour glows under blue light (high-grade gliomas)
- **Extent of resection** correlates with survival

**Radiotherapy:**
- **Grade II:** Consider if progression or incomplete resection
- **Grade III/IV:** Standard of care
- 60 Gy in 30 fractions (6 weeks)
- Concurrent with temozolomide (GBM)

**Chemotherapy:**
- **Temozolomide** (concurrent and adjuvant) for GBM
- **PCV** (procarbazine, lomustine, vincristine) for anaplastic oligodendroglioma (if 1p/19q co-deleted)

**PROGNOSIS:**
- **Grade II:** Median survival 5-10 years
- **Grade III:** Median survival 3-5 years
- **Grade IV (GBM):** Median survival 12-18 months
- **Better prognosis with:**
  - Younger age
  - Good performance status
  - Extensive resection
  - MGMT promoter methylation (GBM)
  - IDH mutation (grades II-III)

**COMPLICATIONS:**
- **Neurological deficit** (motor, speech, vision)
- **Seizures**
- **Infection** (wound, meningitis)
- **DVT/PE** (high risk)
- **Cognitive decline**

**EVIDENCE:** NICE NG99, EANO Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified glioma query",
                    "Applied WHO grading (I-IV)",
                    "Maximal safe resection + chemoradiotherapy for high-grade"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "glioma",
                    "guideline": "nice_ng99"
                }
            )

        # Meningioma
        elif any(term in query_lower for term in [
            "meningioma", "meningioma surgery", "benign brain tumour"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**MENINGIOMA**

**WHAT IS IT?**
- Usually benign tumour arising from meninges
- **WHO Grade I** (most common) - benign
- **WHO Grade II** - atypical
- **WHO Grade III** - anaplastic (malignant)
- 20% of all primary brain tumours
- More common in women, age 40-60 years

**COMMON LOCATIONS:**
- **Convexity** (over brain surface)
- **Parasagittal** (near superior sagittal sinus)
- **Sphenoid wing** (skull base)
- **Olfactory groove** (frontal base)
- **Posterior fossa** (cerebellopontine angle)

**SYMPTOMS:**
- **Headache**
- **Focal neurological deficit** (location-dependent)
  - Frontal: Personality change, weakness
  - Parietal: Sensory change, seizures
  - Temporal: Visual field defect, speech
  - Posterior fossa: Ataxia, cranial nerve palsies
- **Seizures** (30-50%)
- **Raised ICP** (if large)

**DIAGNOSIS:**

**1. MRI Brain with Contrast**
- **T1 with contrast:** Intense homogeneous enhancement
- **Dural tail** (characteristic)
- **Extra-axial** (outside brain)
- **T2:** Variable signal
- **Perfusion:** High blood flow

**2. CT Head**
- May show hyperostosis (thickened bone)
- Calcification common
- Helpful for surgical planning

**MANAGEMENT:**

**Observation:**
- **Indicated for:**
  - Asymptomatic or minimally symptomatic
  - Small tumours (<2-3 cm)
  - Older patients
  - Significant comorbidities
- **Serial MRI** (6-12 months, then yearly if stable)

**Surgery:**
- **Indicated for:**
  - Symptomatic tumours
  - enlarging tumours
  - Younger patients
- **Goals:**
  - **Simpson Grade I** (complete removal with dural excision)
  - **Simpson Grade II** (complete removal, coagulate dural attachment)
  - **Simpson Grade III-IV** (subtotal resection)
- **Approach:**
  - Craniotomy (most)
  - Skull base approach (if anterior/middle cranial fossa)
- **Outcomes:**
  - Gross total resection: 10-year recurrence 10-20%
  - Subtotal resection: 10-year recurrence 50-70%

**Radiotherapy:**
- **Indicated for:**
  - Atypical (Grade II) or anaplastic (Grade III)
  - Recurrent or residual after surgery
  - Patients not surgical candidates
- **Stereotactic radiosurgery** (Gamma Knife, CyberKnife) for small residual/recurrent
- **Fractionated radiotherapy** for larger or higher-grade tumours

**PROGNOSIS:**
- **Grade I:** 10-year survival 80-90%
- **Grade II:** 10-year survival 60-70%
- **Grade III:** 10-year survival 30-40%
- **Recurrence:** 10-20% (Grade I), higher for Grade II-III

**COMPLICATIONS:**
- **Neurological deficit** (seizures, weakness, vision)
- **Infection** (wound, meningitis)
- **Venous infarction** (if sagittal sinus involved)
- **New neurological deficit** after surgery (5-10%)

**EVIDENCE:** NICE NG99, EANO Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified meningioma query",
                    "Usually benign (WHO Grade I)"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "meningioma",
                    "guideline": "nice_ng99"
                }
            )

        # Pituitary adenoma
        elif any(term in query_lower for term in [
            "pituitary adenoma", "pituitary tumour", "pituitary tumour", "prolactinoma"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**PITUITARY ADENOMA**

**WHAT IS IT?**
- Tumour of pituitary gland
- Usually benign (10% malignant)
- **Functioning** (secrete hormones)
- **Non-functioning** (no hormone secretion)
- 10-15% of all intracranial tumours

**CLASSIFICATION:**

**Functioning Adenomas:**
- **Prolactinoma** (most common) - prolactin
- **Somatotroph adenoma** - growth hormone (acromegaly)
- **Corticotroph adenoma** - ACTH (Cushing's disease)
- **Thyrotroph adenoma** - TSH (rare)
- **Gonadotroph adenoma** - FSH/LH (rare)

**Non-Functioning Adenomas:**
- No hormone secretion
- Present with mass effect (vision, headache)

**SYMPTOMS:**

**Mass Effect (Non-Functioning and Large Functioning):**
- **Headache**
- **Visual field defect** - bitemporal hemianopia (classical)
- **Hypopituitarism** - loss of normal pituitary function
- **Cranial nerve palsies** (if large - rare)

**Hormonal Effects (Functioning):**
- **Prolactinoma:** Galactorrhoea, amenorrhoea, infertility, decreased libido
- **Acromegaly:** Coarse features, enlargement of hands/feet, hypertension, diabetes
- **Cushing's:** Weight gain, moon face, buffalo hump, hypertension, diabetes

**DIAGNOSIS:**

**1. MRI Pituitary with Contrast**
- Microadenoma (<10 mm)
- Macroadenoma (>10 mm)
- Assess chiasm compression, cavernous sinus invasion

**2. Visual Field Testing**
- Bitemporal hemianopia
- If optic chiasm compressed

**3. Hormonal Assessment**
- **Prolactin** (prolactinoma)
- **IGF-1** (acromegaly)
- **24-hour urinary cortisol, dexamethasone suppression** (Cushing's)
- **TSH, T4, cortisol, LH/FSH, testosterone/oestrogen** (hypopituitarism)

**MANAGEMENT:**

**Prolactinoma:**
- **Medical therapy first-line**
  - **Cabergoline** (dopamine agonist) - first-line
  - **Bromocriptine** - alternative
- **Surgery** if:
  - Intolerant/resistant to medical therapy
  - Visual compromise not improving with medical therapy
  - Apoplexy (haemorrhage into tumour)

**Acromegaly:**
- **Surgery first-line** (transsphenoidal resection)
- **Medical therapy** if surgery contraindicated or failed:
  - **Somatostatin analogues** (octreotide, lanreotide)
  - **Growth hormone receptor antagonists** (pegvisomant)
- **Radiotherapy** if residual/recurrent

**Cushing's Disease:**
- **Surgery first-line** (transsphenoidal resection)
- **Radiotherapy** if failed
- **Bilateral adrenalectomy** (last resort)

**Non-Functioning Adenoma:**
- **Surgery** if:
  - Visual field defect
  - Hypopituitarism
  - Appropriate growth on serial MRI
- **Observation** if small, asymptomatic
- **Radiotherapy** if residual/recurrent

**SURGICAL APPROACH:**

**Transsphenoidal Surgery (Most Common)**
- Endoscopic or microscopic
- Through nose or upper lip
- Minimally invasive
- Faster recovery
- **Complications:** CSF leak (5-10%), diabetes insipidus (10-20%), hypopituitarism (5-10%)

**Craniotomy (Rare)**
- Large tumours with significant suprasellar extension
- Complex anatomy

**PROGNOSIS:**
- **Surgical cure:** 70-90% (microadenoma), 50-70% (macroadenoma)
- **Recurrence:** 10-20% at 10 years
- **Hormonal normalization:** Depends on tumour type

**COMPLICATIONS:**
- **Hypopituitarism** - requires lifelong hormone replacement
- **Diabetes insipidus** - often transient, may be permanent
- **CSF leak** - may require lumbar drain or reoperation
- **Visual deterioration** (rare)
- **Cavernous sinus injury** (rare - cranial nerve palsies)

**EVIDENCE:** NICE NG145, Endocrine Society Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified pituitary adenoma query",
                    "Distinguished functioning vs non-functioning",
                    "Medical therapy for prolactinoma, surgery for others"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "pituitary_adenoma",
                    "guideline": "nice_ng145"
                }
            )

        # Acoustic neuroma
        elif any(term in query_lower for term in [
            "acoustic neuroma", "vestibular schwannoma", "acoustic tumour"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**ACOUSTIC NEUROMA (VESTIBULAR SCHWANNOMA)**

**WHAT IS IT?**
- Benign tumour of vestibular nerve (8th cranial nerve)
- Arises from Schwann cells
- **NOT a neuroma** (actually schwannoma)
- 8% of intracranial tumours
- Usually unilateral (bilateral if neurofibromatosis type 2)

**SYMPTOMS:**
- **Sensorineural hearing loss** (progressive, unilateral)
- **Tinnitus** (ringing in ear)
- **Imbalance** (vestibular dysfunction)
- **Facial numbness** (trigeminal nerve involvement - rare)
- **Facial weakness** (facial nerve involvement - rare)
- **Raised ICP** (if very large - rare)

**DIAGNOSIS:**

**1. MRI Brain with Contrast**
- **T1 with contrast:** Intense enhancement
- **T2:** Hyperintense
- Located in **cerebellopontine angle**
- **Ice cream cone** appearance (extending into internal auditory meatus)

**2. Audiogram**
- Sensorineural hearing loss
- Asymmetrical

**3. Brainstem Auditory Evoked Potentials**
- Delayed wave V (if small tumour)

**TUMOUR SIZE:**
- **Intracanalicular** (<1 cm) - confined to internal auditory meatus
- **Small** (1-1.5 cm)
- **Medium** (1.5-2.5 cm)
- **Large** (2.5-4 cm)
- **Giant** (>4 cm)

**MANAGEMENT:**

**Observation (Watch and Wait):**
- **Indicated for:**
  - Small tumours (<1.5 cm)
  - Asymptomatic or minimal symptoms
  - Older patients
  - Significant comorbidities
- **Serial MRI** (6-12 months, then yearly if stable)
- **Growth rate:** ~1-2 mm/year (some faster, some stable)
- **50% grow over 5 years**

**Surgery:**
- **Indicated for:**
  - Growing tumours
  - Significant symptoms (hearing loss, tinnitus, imbalance)
  - Larger tumours (>2.5 cm)
  - Younger patients
  - Patient preference
- **Approaches:**
  - **Retrosigmoid** - most common, good facial nerve exposure
  - **Translabyrinthine** - sacrifice hearing, good tumour exposure
  - **Middle fossa** - attempt to preserve hearing (small tumours)
- **Outcomes:**
  - **Facial nerve preservation:** 90-95% (small tumours), 70-80% (large)
  - **Hearing preservation:** 30-50% (small tumours selected for hearing preservation)
  - **Complete resection:** 90-95%
  - **Recurrence:** <5% at 10 years

**Stereotactic Radiosurgery (Gamma Knife, CyberKnife):**
- **Indicated for:**
  - Small to medium tumours (<3 cm)
  - Patients not surgical candidates
  - Recurrent/residual tumours
  - Patient preference
- **Mechanism:** Single high-dose radiation
- **Outcomes:**
  - **Tumour control:** 90-95% at 10 years
  - **Hearing preservation:** 50-70%
  - **Facial nerve preservation:** >95%
  - **Complications:** Trigeminal neuropathy (5-10%), hydrocephalus (5%)

**CHOOSING BETWEEN OBSERVATION, SURGERY, AND RADIOSURGERY:**

**Factors Favoring Observation:**
- Small tumour (<1.5 cm)
- Minimal symptoms
- Older patient
- Significant comorbidities

**Factors Favoring Surgery:**
- Large tumour (>2.5 cm)
- Significant symptoms
- Younger patient
- Patient preference (wants tumour gone)
- Need for histological diagnosis

**Factors Favoring Radiosurgery:**
- Small to medium tumour (<3 cm)
- Growing tumour
- Patient not surgical candidate
- Patient preference (avoid surgery)

**COMPLICATIONS:**
- **Hearing loss** (inevitable with surgery, possible with radiosurgery)
- **Facial weakness** (transient 20-30%, permanent 5-10%)
- **Tinnitus** (may persist or worsen)
- **Imbalance** (vestibular dysfunction)
- **CSF leak** (5-10% after surgery)
- **Meningitis** (1-5% after surgery)
- **Hydrocephalus** (5% - may require shunt)

**PROGNOSIS:**
- **Excellent** for tumour control
- **Good functional outcome** in most
- **Quality of life** depends on hearing and facial function

**EVIDENCE:** NICE NGNG, BKINI Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified acoustic neuroma query",
                    "Explained management options: observation, surgery, radiosurgery"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "acoustic_neuroma",
                    "guideline": "nice_ng"
                }
            )

        # Brain metastasis
        elif any(term in query_lower for term in [
            "brain metastasis", "brain mets", "secondary brain tumour", "brain spread"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**BRAIN METASTASES**

**WHAT ARE THEY?**
- Secondary brain tumours from systemic cancer
- **Most common** intracranial tumours (more common than primary brain tumours)
- **20-40%** of cancer patients develop brain metastases
- Most common primary sites:
  - **Lung** (40-50%)
  - **Breast** (15-20%)
  - **Melanoma** (10-15%)
  - **Renal** (5-10%)
  - **Colorectal** (5%)

**SYMPTOMS:**
- **Headache** (60-70%)
- **Focal neurological deficit** (40-50%)
- **Seizures** (20-30%)
- **Cognitive change** (20-30%)
- **Raised ICP** (nausea, vomiting, papilloedema)
- **Asymptomatic** (10-20% - found on staging)

**DIAGNOSIS:**

**1. MRI Brain with Contrast**
- Multiple lesions in 70-80%
- **T1 with contrast:** Ring-enhancing (often)
- **T2/FLAIR:** Oedema (often significant)
- **Diffusion:** May help distinguish abscess

**2. CT Head**
- If MRI not available
- Multiple hyperdense lesions with oedema

**3. Staging**
- **CT chest/abdomen/pelvis** - identify primary
- **PET-CT** - if primary unknown

**GRADING PROGNOSIS:**

**Recursive Partitioning Analysis (RPA) Classes:**
- **Class I:** KPS ≥70, age <65, controlled primary, no extracranial metastases
- **Class II:** KPS ≥70, age ≥65 OR uncontrolled primary OR extracranial metastases
- **Class III:** KPS <70

**RPA Class I** - median survival ~12 months
**RPA Class II** - median survival ~4-6 months
**RPA Class III** - median survival ~2 months

**MANAGEMENT:**

**1. Corticosteroids**
- **Dexamethasone** 4-16 mg/day
- Reduce oedema, improve symptoms
- Taper once definitive treatment initiated

**2. Antiepileptics**
- **Levetiracetam** first-line (if seizures)
- Prophylactic antiepileptics NOT recommended routinely

**3. Surgery**
- **Indicated for:**
  - **Single accessible metastasis** with good prognosis
  - Symptomatic mass effect
  - Diagnosis uncertain (need biopsy)
  - Large tumour (>3 cm)
- **Not indicated if:**
  - Multiple metastases (usually)
  - Poor prognosis (RPA Class III)
  - Inaccessible location (brainstem, deep)

**4. Whole Brain Radiotherapy (WBRT)**
- **Indicated for:**
  - Multiple metastases
  - Surgery not possible
  - Leptomeningeal disease
- **20 Gy in 5 fractions** (most common)
- **30 Gy in 10 fractions** (better control, more side effects)
- **Side effects:** Fatigue, alopecia, neurocognitive decline

**5. Stereotactic Radiosurgery (SRS)**
- **Gamma Knife or CyberKnife**
- **Indicated for:**
  - **1-4 metastases** (each <3-4 cm)
  - Surgery not possible or refused
  - Recurrent metastases after WBRT
- **High local control** (80-90%)
- **Preserves neurocognitive function** (vs WBRT)

**6. Combined Modality**
- **Surgery + WBRT** - for single metastasis
- **Surgery + SRS** - for resection cavity
- **WBRT + SRS** - for multiple metastases

**CHOOSING TREATMENT:**

**Single Metastasis:**
- **Surgery** if accessible and patient good candidate
- **SRS** if not surgical candidate
- **WBRT** if >3 metastases or poor prognosis

**2-4 Metastases:**
- **SRS** (if each <3-4 cm)
- **WBRT** (if SRS not available)

**>4 Metastases:**
- **WBRT**
- Consider best supportive care if poor prognosis

**PROGNOSIS:**
- **Median survival:** 3-12 months (depends on RPA class)
- **Better prognosis with:**
  - Good performance status (KPS ≥70)
  - Controlled primary tumour
  - No extracranial metastases
  - Age <65 years
  - Limited number of metastases

**COMPLICATIONS:**
- **Neurological death** (50% die from brain metastases)
- **Neurocognitive decline** (WBRT)
- **Radionecrosis** (SRS)
- **Leptomeningeal spread** (5-10%)

**EVIDENCE:** NICE NG99, ASTRO Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified brain metastasis query",
                    "Applied RPA classification for prognosis",
                    "Treatment based on number of metastases and prognosis"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "brain_metastases",
                    "guideline": "nice_ng99"
                }
            )

        # General brain tumour
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**BRAIN TUMOURS**

**COMMON BRAIN TUMOURS:**

**Primary Brain Tumours:**
- **Glioma** - glial cells (astrocytoma, oligodendroglioma, ependymoma)
  - **Glioblastoma (GBM)** - most malignant, poor prognosis
  - **Low-grade glioma** - slow-growing, may progress
- **Meningioma** - meninges, usually benign
- **Pituitary adenoma** - pituitary gland
- **Acoustic neuroma** - vestibular nerve (schwannoma)
- **Medulloblastoma** - cerebellum, children

**Secondary Brain Tumours (Metastases):**
- Most common intracranial tumours
- From lung, breast, melanoma, renal, colorectal
- Often multiple

**SYMPTOMS:**
- **Headache** (worse in morning, with Valsalva)
- **Focal neurological deficit** (weakness, sensory, speech)
- **Seizures**
- **Cognitive change** (confusion, memory)
- **Raised ICP** (nausea, vomiting, papilloedema)

**DIAGNOSIS:**
- **MRI brain with contrast** (investigation of choice)
- **CT head** (if MRI not available or emergency)
- **Biopsy** (histological diagnosis)

**TREATMENT:**
- **Surgery** (maximal safe resection)
- **Radiotherapy** (adjuvant or definitive)
- **Chemotherapy** (temozolomide for glioblastoma)
- **Symptomatic** (steroids, antiepileptics)

**PROGNOSIS:**
- Variable by tumour type and grade
- **GBM:** 12-18 months
- **Meningioma (Grade I):** 10-year survival 80-90%
- **Metastases:** 3-12 months (depends on RPA class)

**EVIDENCE:** NICE NG99""",
                confidence=0.84,
                reasoning_trace=[
                    "Provided general brain tumour overview",
                    "Listed common primary and secondary tumours",
                    "Outlined general approach to diagnosis and treatment"
                ],
                capabilities_used=["brain_tumour_surgery"],
                metadata={
                    "topic": "brain_tumour_general",
                    "guideline": "nice_ng99"
                }
            )

    def _handle_subdural_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle subdural haematoma queries"""
        query_lower = query.lower()

        # Chronic subdural haematoma
        if any(term in query_lower for term in [
            "chronic subdural", "csdh", "chronic sdh", "elderly", "alcohol", "anticoagulated"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**CHRONIC SUBDURAL HAEMATOMA (CSDH)**

**WHAT IS IT?**
- Collection of blood in subdural space >3 weeks old
- **Low-pressure venous bleed** (bridging veins)
- Common in **elderly**, **alcoholics**, **anticoagulated** patients
- Often minor trauma (or no trauma remembered)
- **Slow progression** over weeks

**RISK FACTORS:**
- **Age >65 years** (brain atrophy, bridging veins stretched)
- **Alcohol abuse**
- **Anticoagulation** (warfarin, DOACs)
- **Antiplatelets** (aspirin, clopidogrel)
- **Falls** (even minor)
- **Epilepsy** (trauma from seizures)

**SYMPTOMS:**
- **Headache** (most common)
- **Cognitive decline** (confusion, memory)
- **Gait disturbance** (difficulty walking, falls)
- **Hemiparesis** (often mild)
- **Speech disturbance**
- **Decreased conscious level** (if large)
- **Seizures** (rare)

**DIAGNOSIS:**

**CT Head:**
- **Isodense or hypodense** (same density as brain)
- **Crescentic shape** (concave toward brain)
- **Midline shift** (if large)
- May be **bilateral** (20-30%)

**MRI Brain:**
- **T1:** Variable signal (depends on age of blood)
- **T2:** Hyperintense
- More sensitive than CT for small CSDH

**MANAGEMENT:**

**1. Reversal of Anticoagulation**
- **Warfarin:**
  - **Prothrombin complex concentrate (PCC)** - rapid reversal
  - **Vitamin K** 5-10 mg IV (slower, but sustained)
  - Target INR <1.5 before surgery
- **DOACs:**
  - **Idarucizumab** for dabigatran
  - **Andexanet alfa** for apixaban/rivaroxaban (if available)
  - **PCC** (if specific reversal agents not available)

**2. Surgical Evacuation**
- **Indicated for:**
  - Symptomatic CSDH (any size)
  - GCS <15
  - Focal neurological deficit
  - Significant midline shift (>5 mm)
  - Radiological progression
- **NOT indicated for:**
  - Asymptomatic, small CSDH with no midline shift
- **Procedures:**
  - **Burr hole evacuation** (most common)
    - 1-2 burr holes
    - Irrigate subdural space
    - Drain insertion (closed for 24-48 hours)
    - Recurrence rate: 10-20%
  - **Twist drill craniostomy** (smaller, bedside)
    - For very frail patients
    - Higher recurrence
  - **Craniotomy** (rare)
    - For recurrent or organized CSDH
    - Membranes excised

**3. Conservative Management**
- **Indicated for:**
  - Asymptomatic CSDH
  - Small CSDH (<1 cm thickness, <5 mm midline shift)
  - Poor surgical candidate (frailty, comorbidities)
  - Patient refusal
- **Management:**
  - Serial CT scans (q1-2 weeks initially)
  - Reverse anticoagulation (if possible)
  - Close neurological monitoring
- **Resolution:** Spontaneous in 30-50% (small CSDH)

**POSTOPERATIVE CARE:**
- **Drain:** Left in situ for 24-48 hours
- **Bed rest** (head of bed flat)
- **Adequate hydration** (promotes brain expansion)
- **Avoid Valsalva** (constipation - stool softeners)
- **Restart anticoagulation** (if indicated) after 2-3 days

**COMPLICATIONS:**
- **Recurrence:** 10-20% (higher if anticoagulated)
- **Infection:** 1-5% (meningitis, wound infection)
- **Seizures:** 5% (prophylactic antiepileptics NOT recommended routinely)
- **Intracerebral haematoma** (brain injury during evacuation)
- **Chronic subdural hygroma** (CSF collection)

**PROGNOSIS:**
- **Mortality:** 5-15% (higher in elderly, comorbidities)
- **Good outcome:** 70-80%
- **Poor prognostic factors:**
  - Age >80 years
  - GCS <13 on admission
  - Significant comorbidities
  - Recurrent CSDH

**PREVENTION:**
- **Fall prevention** in elderly
- **Caution with anticoagulation** (risk-benefit assessment)
- **Avoid alcohol** excess
- **Prompt medical attention** after head injury (especially if on anticoagulation)

**EVIDENCE:** NICE NG232, SBNS Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified chronic subdural haematoma query",
                    "Burr hole evacuation is standard treatment",
                    "High recurrence rate (10-20%)"
                ],
                capabilities_used=["traumatic_brain_injury_management"],
                metadata={
                    "topic": "chronic_subdural_haematoma",
                    "guideline": "nice_ng232"
                }
            )

        # General subdural
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**SUBDURAL HAEMATOMA (SDH)**

**WHAT IS IT?**
- Blood collection in subdural space
- Between dura and arachnoid mater
- **Bridging veins** rupture

**CLASSIFICATION:**

**Acute SDH (<3 days):**
- High-pressure arterial bleed (rare)
- Or severe trauma (venous)
- **Hyperdense** on CT
- **High mortality** (40-60%)

**Subacute SDH (3-21 days):**
- **Isodense** on CT (same density as brain - hard to see)
- May be missed on CT

**Chronic SDH (>21 days):**
- **Hypodense** on CT
- Low-pressure venous bleed
- Common in elderly, alcoholics, anticoagulated

**SYMPTOMS:**
- **Headache**
- **Confusion**, cognitive decline
- **Focal deficit** (hemiparesis)
- **Decreased conscious level**
- **Seizures** (rare)

**DIAGNOSIS:**
- **CT head** (first-line)
- **MRI brain** (if CT equivocal)

**MANAGEMENT:**
- **Acute symptomatic:** Surgical evacuation (craniotomy)
- **Chronic symptomatic:** Burr hole evacuation
- **Asymptomatic small:** Observation or serial imaging

**PROGNOSIS:**
- **Acute:** High mortality (40-60%)
- **Chronic:** Good outcome in 70-80%

**EVIDENCE:** NICE NG232""",
                confidence=0.87,
                reasoning_trace=[
                    "Provided subdural haematoma overview",
                    "Classified by time (acute, subacute, chronic)"
                ],
                capabilities_used=["traumatic_brain_injury_management"],
                metadata={
                    "topic": "subdural_haematoma",
                    "guideline": "nice_ng232"
                }
            )

    def _handle_hydrocephalus_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle hydrocephalus queries"""
        query_lower = query.lower()

        # Normal pressure hydrocephalus
        if any(term in query_lower for term in [
            "normal pressure hydrocephalus", "nph", "elderly hydrocephalus",
            "wet wacky wobbly"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**NORMAL PRESSURE HYDROCEPHALUS (NPH)**

**WHAT IS IT?**
- Form of communicating hydrocephalus
- **Classic triad:** Wet, Wacky, Wobbly
- **Normal opening pressure** on lumbar puncture (but dynamic impairment)
- Reversible cause of dementia (if treated early)
- Usually **idiopathic** (or secondary to SAH, meningitis, head injury)

**CLASSIC TRIAD (ADAM TRIAD):**

**Wet (Urinary Incontinence):**
- Urgency, frequency
- Incontinence
- Due to disruption of frontal bladder pathways

**Wacky (Dementia):**
- Memory impairment
- Apathy, reduced motivation
- Slowed thinking (bradyphrenia)
- **"Frontal" dementia** (unlike Alzheimer's - early memory loss)

**Wobbly (Gait Disturbance):**
- **First and most prominent symptom** in most
- **Magnetic gait** - feet seem stuck to floor
- Shuffling, broad-based
- Difficulty with turns
- Falls

**DIAGNOSIS:**

**1. MRI Brain**
- **Ventriculomegaly** (enlarged ventricles)
- **Periventricular hyperintensities** (transependymal CSF flow)
- **Disproportionately enlarged subarachnoid space hydrocephalus (DESH)**
- Aqueductal flow void (on gradient echo sequences)

**2. Lumbar Puncture (Diagnostic Trial)**
- **Opening pressure** usually normal (10-20 cmH2O)
- **Tap test** - remove 30-50 mL CSF
- **Assess gait before and after** (timed walk test)
- Improvement supports diagnosis (but not diagnostic)

**3. Gait Analysis**
- Quantitative gait assessment
- Stride length, speed, cadence
- Improvement after tap test supports diagnosis

**4. Intracranial Pressure Monitoring**
- Overnight ICP monitoring
- **B-waves** (plateau waves) support diagnosis
- Used if diagnosis uncertain

**5. Isotope Cisternography**
- Radionuclide injected into lumbar CSF
- **Delayed clearance** over convexities (reflux into ventricles)
- Rarely used now

**MANAGEMENT:**

**Ventriculoperitoneal (VP) Shunt:**
- **Definitive treatment**
- **Procedure:**
  - Catheter into lateral ventricle (frontal or parietal)
  - Valve (programmable or fixed-pressure)
  - Distal catheter into peritoneal cavity
- **Outcomes:**
  - 60-80% improve with shunt
  - Gait: Best response (80%)
  - Incontinence: Moderate response (60-70%)
  - Dementia: Variable response (40-60%)
  - Earlier treatment = better outcome
- **Complications:**
  - **Shunt obstruction** (10-20%)
  - **Shunt infection** (5-10%)
  - **Subdural haematoma** (5-10%) - due to overdrainage
  - **Shunt malfunction** (10%)
  - **Seizures** (rare)

**Patient Selection for Shunting:**
- **Classic triad present** (gait, cognitive, urinary)
- **MRI supportive** (ventriculomegaly, DESH)
- **Positive tap test** (gait improvement)
- **No significant comorbidities** limiting benefit
- **Not too advanced** dementia (may still benefit if gait predominant)

**Prognostic Factors (Good Outcome):**
- Short duration of symptoms (<2 years)
- Gait predominant (not dementia predominant)
- Minimal white matter disease on MRI
- No significant comorbidities
- Younger age (<75 years)

**PROGNOSIS:**
- **Untreated:** Progressive dementia, gait disturbance, incontinence
- **Treated:** 60-80% improve, some stabilize
- **Earlier treatment = better outcome**
- **Delayed treatment = less benefit** (irreversible brain changes)

**COMPLICATIONS:**
- **Shunt obstruction:** Requires shunt revision
- **Shunt infection:** Requires shunt removal, antibiotics, reinsertion
- **Subdural haematoma:** Due to overdrainage, may require shunt revision
- **Overdrainage:** Low pressure headaches (may need valve adjustment)
- **Underdrainage:** No improvement (may need valve adjustment)

**FOLLOW-UP:**
- **Clinical assessment** at 6 weeks, 6 months, then yearly
- **Programmable valve adjustments** as needed
- **Shunt series X-rays** if malfunction suspected

**EVIDENCE:** NICE NG306, AAN Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified normal pressure hydrocephalus query",
                    "Applied classic triad (wet, wacky, wobbly)"
                ],
                capabilities_used=["hydrocephalus_management"],
                metadata={
                    "topic": "normal_pressure_hydrocephalus",
                    "guideline": "nice_ng306"
                }
            )

        # General hydrocephalus
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**HYDROCEPHALUS**

**WHAT IS IT?**
- Abnormal accumulation of CSF in ventricles
- **Increased intracranial pressure** (except NPH)
- **Obstructive** (non-communicating) vs **communicating**

**TYPES:**

**Congenital Hydrocephalus:**
- Present at birth
- Due to neural tube defects, aqueduct stenosis, infection

**Acquired Hydrocephalus:**
- **Tumour** (obstructive)
- **Subarachnoid haemorrhage** (communicating)
- **Meningitis** (communicating)
- **Head injury** (communicating)

**Normal Pressure Hydrocephalus (NPH):**
- Elderly
- Classic triad: Wet, wacky, wobbly
- Normal opening pressure

**SYMPTOMS:**
- **Headache** (raised ICP)
- **Nausea, vomiting** (raised ICP)
- **Decreased conscious level** (raised ICP)
- **Gait disturbance** (especially NPH)
- **Cognitive decline** (especially NPH)
- **Urinary incontinence** (especially NPH)

**SIGNS:**
- **Papilloedema** (raised ICP)
- **Sunsetting eyes** (infants)
- **Enlarging head** (infants - rapid head growth)
- **Frontal bossing** (infants)

**DIAGNOSIS:**
- **MRI brain** (ventriculomegaly)
- **CT head** (if MRI unavailable)
- **Lumbar puncture** (NPH - tap test)

**MANAGEMENT:**

**VP Shunt (Most Common):**
- Ventricular catheter → valve → peritoneal catheter
- **Complications:** Obstruction (10-20%), infection (5-10%), subdural haematoma

**Endoscopic Third Ventriculostomy (ETV):**
- For obstructive hydrocephalus
- Create hole in floor of third ventricle
- Avoids shunt (no foreign body)
- Success: 70-80%

**Temporary Measures (While Awaiting Definitive):**
- **Lumbar puncture** (communicating hydrocephalus)
- **External ventricular drain (EVD)** (obstructive hydrocephalus)
- **Acetazolamide** (reduce CSF production - limited efficacy)

**PROGNOSIS:**
- **Good if treated early**
- **Developmental delay** if untreated in children
- **Reversible** if NPH treated early

**EVIDENCE:** NICE Guidelines""",
                confidence=0.86,
                reasoning_trace=[
                    "Provided hydrocephalus overview",
                    "Classified as obstructive vs communicating",
                    "VP shunt is standard treatment"
                ],
                capabilities_used=["hydrocephalus_management"],
                metadata={
                    "topic": "hydrocephalus_general"
                }
            )

    def _handle_spine_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle spine surgery queries"""
        query_lower = query.lower()

        # Discectomy/herniated disc
        if any(term in query_lower for term in [
            "discectomy", "microdiscectomy", "herniated disc", "slipped disc", "disc prolapse",
            "disc herniation", "sciatica", "radiculopathy"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**HERNIATED LUMBAR DISC / SCIATICA**

**WHAT IS IT?**
- Prolapse of intervertebral disc nucleus pulposus
- Compresses nerve root → **radiculopathy** (sciatica)
- Most common at **L4/5** and **L5/S1**

**SYMPTOMS:**
- **Low back pain** (may be minor)
- **Radiculopathy** (sciatica)
  - Pain shooting down leg (dermatomal distribution)
  - **L4:** Anterior thigh, knee
  - **L5:** Lateral thigh, anterior/lateral leg, dorsum of foot
  - **S1:** Posterior thigh, calf, sole of foot
- **Sensory loss** (numbness, tingling)
- **Motor weakness** (foot drop, inability to heel walk - L5; inability to toe walk - S1)
- **Absent ankle jerk** (S1), **reduced knee jerk** (L3/4)

**DIAGNOSIS:**

**1. MRI Lumbar Spine (Investigation of Choice)**
- Shows disc prolapse
- Assess size, location (central vs paracentral vs foraminal)
- Identify nerve root compression

**2. CT Lumbar Spine**
- Alternative if MRI contraindicated
- Shows bony anatomy better than disc

**MANAGEMENT:**

**Conservative (First-Line for Most):**
- **Analgesia** (paracetamol, NSAIDs, opioids if severe)
- **Physiotherapy**
  - McKenzie exercises
  - Core strengthening
  - Gradual return to activity
- **Epidural steroid injection** (consider if severe pain, not responding to conservative)
- **Time:** 6-12 weeks for most to improve

**Surgery (Discectomy):**
- **Indicated for:**
  - **Cauda equina syndrome** (emergency)
  - **Severe motor weakness** (foot drop, weakness scoring ≤3/5)
  - **Intractable pain** (>6-12 weeks, not responding to conservative)
  - **Recurrent episodes** affecting quality of life
  - **Patient preference** (after failed conservative)

**Microdiscectomy (Standard Procedure):**
- **Minimally invasive**
- **Small incision** (2-3 cm)
- **Microscope** for visualization
- **Remove disc fragment** compressing nerve
- **NOT complete discectomy** (leave remaining disc)
- **Outcomes:**
  - 80-90% good/excellent
  - Rapid pain relief
  - Faster return to work vs conservative
- **Complications:**
  - **Dural tear** (2-5%) - may require repair
  - **Infection** (1-2%)
  - **Recurrent disc herniation** (5-10%)
  - **Nerve root injury** (1%)
  - **Discitis** (rare, serious)

**POSTOPERATIVE CARE:**
- **Day case** or overnight stay
- **Mobilize day of surgery** or next day
- **Avoid heavy lifting** for 4-6 weeks
- **Physiotherapy** (core strengthening, gradual return to activity)
- **Return to work:** 2-4 weeks (sedentary), 6-12 weeks (manual labour)

**PROGNOSIS:**
- **Conservative:** 70-80% improve over 6-12 weeks
- **Surgical:** 80-90% good/excellent outcome
- **Recurrence:** 5-10% (same level or different level)
- **Chronic low back pain:** 20-30% (regardless of treatment)

**EVIDENCE:** NICE NG59, NASS Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified herniated disc/sciatica query",
                    "Conservative management first-line (6-12 weeks)",
                    "Surgery for cauda equina, severe weakness, or intractable pain"
                ],
                capabilities_used=["spine_surgery_consultation"],
                metadata={
                    "topic": "herniated_disc",
                    "guideline": "nice_ng59"
                }
            )

        # Spinal stenosis
        elif any(term in query_lower for term in [
            "spinal stenosis", "lumbar stenosis", "neurogenic claudication"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**LUMBAR SPINAL STENOSIS**

**WHAT IS IT?**
- Narrowing of spinal canal
- Compression of cauda equina nerve roots
- **Neurogenic claudication** (classic symptom)
- Degenerative (age-related) - most common
- Can be congenital (achondroplasia)

**SYMPTOMS:**

**Neurogenic Claudication (Classic):**
- **Pain, numbness, weakness** in legs with walking
- **Relieved by bending forward** (shopping cart sign)
- **Relieved by sitting**
- **Distance-limited** (can only walk 50-200 meters before symptoms)
- **Bilateral** (usually, but may be asymmetric)
- **May be asymmetric or unilateral** (if lateral recess stenosis)

**Other Symptoms:**
- **Low back pain** (may be present)
- **Radiating pain** (but not classic radiculopathy)
- **Numbness** in legs
- **Weakness** (less common)
- **Normal foot pulses** (distinguish from vascular claudication)

**DIFFERENTIAL DIAGNOSIS:**

**Neurogenic vs Vascular Claudication:**

| Feature | Neurogenic | Vascular |
|---------|-----------|----------|
| Relief with sitting | Yes | No (need rest) |
| Relief with standing | No | Yes (venous pooling) |
| Bending forward helps | Yes | No |
| Bicycle | Yes (leaning forward) | No (effort-limiting) |
| Pedal pulses | Normal | Diminished/absent |
| Skin changes | No | May have ulcers, hair loss |

**DIAGNOSIS:**

**1. MRI Lumbar Spine (Investigation of Choice)**
- **Central canal stenosis** (measured at L3/4, L4/5)
  - Mild: 10-12 mm
  - Moderate: 8-10 mm
  - Severe: <8 mm
- **Lateral recess stenosis**
- **Foraminal stenosis**
- **Facet joint hypertrophy**, **ligamentum flavum hypertrophy**, **disc bulge**

**2. CT Lumbar Spine**
- Alternative if MRI contraindicated
- Shows bony anatomy well

**MANAGEMENT:**

**Conservative (First-Line):**
- **Analgesia** (paracetamol, NSAIDs, neuropathic agents - gabapentin/pregabalin)
- **Physiotherapy**
  - Flexion-based exercises
  - Walking program (tolerance-based)
  - Core strengthening
- **Epidural steroid injection** (consider if severe symptoms)
- **Time:** 3-6 months trial

**Surgery (Decompression):**
- **Indicated for:**
  - **Severe symptoms** affecting quality of life
  - **Walking distance <100 meters** (despite conservative)
  - **Progressive neurological deficit** (rare)
  - **Cauda equina syndrome** (emergency)
  - **Patient preference** (after failed conservative)

**Laminectomy (Standard Procedure):**
- **Remove lamina** (roof of spinal canal)
- **Remove ligamentum flavum**
- **Facetectomy** (partial removal of facet joints if needed)
- **Foraminotomy** (if foraminal stenosis)
- **Midline incision**
- **Hospital:** 2-5 days
- **Outcomes:**
  - 70-80% good/excellent
  - Improved walking distance
  - Reduced pain
- **Complications:**
  - **Dural tear** (5-10%)
  - **Infection** (2-5%)
  - **Instability** (5-10%) - may require fusion
  - **Epidural hematoma** (rare, emergency)
  - **Nerve root injury** (1%)

**Minimally Invasive Decompression:**
- **Smaller incisions**
- **Less muscle disruption**
- **Faster recovery**
- Similar outcomes to open surgery

**Decompression + Fusion:**
- **Indicated if:**
  - **Instability** preoperative (spondylolisthesis)
  - **Extensive facetectomy** (risk of postoperative instability)
  - **Degenerative scoliosis**
- **Instrumented fusion** (pedicle screws + rods)
- **Higher morbidity**, longer recovery

**POSTOPERATIVE CARE:**
- **Mobilize day 1 or 2**
- **Physiotherapy** (core strengthening, walking program)
- **Avoid heavy lifting** for 6-12 weeks
- **Return to work:** 4-8 weeks (sedentary), 12+ weeks (manual labour)

**PROGNOSIS:**
- **Conservative:** 30-50% improve over 3-6 months
- **Surgical:** 70-80% good/excellent outcome
- **Recurrence:** 10-20% (restenosis)
- **Progression:** Common if untreated

**EVIDENCE:** NICE NG59, NASS Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified spinal stenosis query",
                    "Neurogenic claudication is classic symptom",
                    "Laminectomy is standard surgical treatment"
                ],
                capabilities_used=["spine_surgery_consultation"],
                metadata={
                    "topic": "spinal_stenosis",
                    "guideline": "nice_ng59"
                }
            )

        # Spondylolisthesis
        elif any(term in query_lower for term in [
            "spondylolisthesis", "spondylo", "slipped vertebra", "spondylolysis"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**SPONDYLOLISTHESIS**

**WHAT IS IT?**
- Slippage of one vertebra on another
- Most common at **L5 on S1** or **L4 on L5**
- **Spondylolysis** (pars defect) is common cause

**CLASSIFICATION:**

**1. By Cause (Wiltse Classification):**
- **Type I (Dysplastic):** Congenital abnormality of pars interarticularis
- **Type II (Isthmic):** Spondylolysis (pars defect) - most common
- **Type III (Degenerative):** Facet joint arthritis, disc degeneration - common in elderly
- **Type IV (Traumatic):** Acute fracture of pars
- **Type V (Pathological):** Bone disease (Paget's, metastasis)

**2. By Grade (Meyerding Classification):**
- **Grade I:** 0-25% slippage
- **Grade II:** 25-50% slippage
- **Grade III:** 50-75% slippage
- **Grade IV:** 75-100% slippage
- **Grade V:** Spondyloptosis (100% slippage - vertebra completely displaced)

**SYMPTOMS:**
- **Low back pain** (most common)
- **Radiculopathy** (nerve root compression)
  - **L5:** Pain, numbness lateral leg, foot drop
  - **S1:** Pain posterior leg, weakness calf, absent ankle jerk
- **Neurogenic claudication** (if spinal stenosis)
- **Hamstring tightness** (common in adolescents)
- **May be asymptomatic** (incidental finding)

**DIAGNOSIS:**

**1. X-ray Lumbar Spine**
- **Lateral view** - best for assessing slippage grade
- **Oblique views** - pars defect (Scotty dog "collar" broken)
- **Flexion/extension views** - assess instability

**2. MRI Lumbar Spine**
- **Nerve root compression**
- **Spinal stenosis**
- **Disc degeneration**
- **Pars oedema** (stress reaction)

**3. CT Lumbar Spine**
- **Pars defect** (better than MRI)
- **Bony anatomy**

**MANAGEMENT:**

**Conservative (First-Line for Grade I-II):**
- **Analgesia** (paracetamol, NSAIDs)
- **Physiotherapy**
  - Core strengthening
  - Hamstring stretching
  - Flexion-based exercises
  - Avoid hyperextension
- **Activity modification** (avoid hyperextension sports)
- **Time:** 3-6 months

**Surgery:**
- **Indicated for:**
  - **Persistent symptoms** (>6 months) despite conservative
  - **Progressive slippage** (on serial X-rays)
  - **Neurological deficit** (weakness, cauda equina syndrome)
  - **Severe slippage** (Grade III-IV)
  - **Instability** (on flexion/extension X-rays)

**Decompression + Fusion (Standard Procedure):**
- **Decompression:** Laminectomy, foraminotomy (relieve nerve compression)
- **Fusion:** Instrumented posterolateral fusion (pedicle screws + rods)
  - Reduces motion, stabilizes spine
  - Promotes bony fusion
- **Interbody cage** (TLIF, PLIF, ALIF) - optional
  - Restore disc height
  - Increase fusion surface area
  - Improve lordosis
- **Hospital:** 3-5 days
- **Outcomes:**
  - 80-90% good/excellent
  - Fusion rate: 80-95%
  - Reduced pain, improved function
- **Complications:**
  - **Nonunion** (5-10%) - may require revision
  - **Hardware failure** (5-10%)
  - **Infection** (2-5%)
  - **Dural tear** (5-10%)
  - **Nerve root injury** (1%)
  - **Adjacent segment disease** (10-20% at 10 years)

**POSTOPERATIVE CARE:**
- **Mobilize day 1 or 2** (with brace if prescribed)
- **Physiotherapy** (core strengthening once fusion solid)
- **No heavy lifting** for 3-6 months
- **Brace** (optional, for 6-12 weeks)
- **Serial X-rays** (assess fusion)
- **Return to work:** 6-12 weeks (sedentary), 6+ months (manual labour)

**PROGNOSIS:**
- **Conservative:** 50-70% improve (Grade I-II)
- **Surgical:** 80-90% good/excellent outcome
- **Fusion:** 80-95% solid fusion
- **Recurrence:** Rare if fused
- **Adjacent segment disease:** Common (10-20% at 10 years)

**EVIDENCE:** NICE NG59, NASS Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified spondylolisthesis query",
                    "Applied Meyerding grading (I-V)",
                    "Decompression + fusion is standard surgical treatment"
                ],
                capabilities_used=["spine_surgery_consultation"],
                metadata={
                    "topic": "spondylolisthesis",
                    "guideline": "nice_ng59"
                }
            )

        # General spine surgery
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**SPINE SURGERY**

**COMMON SPINE CONDITIONS:**

**Herniated Disc (Sciatica)**
- Disc prolapse compressing nerve root
- Pain, numbness, weakness in leg
- Conservative first (6-12 weeks)
- Microdiscectomy if severe weakness or intractable pain

**Spinal Stenosis**
- Narrowing of spinal canal
- Neurogenic claudication (pain walking)
- Conservative first (3-6 months)
- Laminectomy if severe

**Spondylolisthesis**
- Slippage of vertebra
- Low back pain, radiculopathy
- Conservative for Grade I-II
- Fusion for higher grades or instability

**Cervical Myelopathy**
- Spinal cord compression in neck
- Hand clumsiness, gait disturbance
- Surgical decompression ± fusion

**Cauda Equina Syndrome**
- Emergency surgical decompression
- Saddle anaesthesia, urinary retention

**COMMON PROCEDURES:**

**Discectomy**
- Remove herniated disc fragment
- Microdiscectomy (minimally invasive)
- 80-90% good outcome

**Laminectomy**
- Remove lamina (roof of spinal canal)
- Decompress nerves
- For spinal stenosis

**Spinal Fusion**
- Permanently join vertebrae
- Instrumented (pedicle screws + rods)
- For instability, spondylolisthesis

**Discectomy + Fusion**
- Remove disc, fuse vertebrae
- For recurrent disc, instability

**PREOPERATIVE ASSESSMENT:**
- MRI spine (investigation of choice)
- CT spine (if MRI contraindicated)
- X-rays (flexion/extension if instability suspected)
- Assessment of comorbidities (especially for fusion)

**RISKS:**
- Infection (1-5%)
- Dural tear (2-10%)
- Nerve root injury (1%)
- Nonunion (fusion)
- Adjacent segment disease (fusion)
- Recurrence (discectomy)

**RECOVERY:**
- Discectomy: 2-4 weeks
- Laminectomy: 4-8 weeks
- Fusion: 3-6 months

**EVIDENCE:** NICE NG59""",
                confidence=0.84,
                reasoning_trace=[
                    "Provided spine surgery overview",
                    "Listed common conditions and procedures",
                    "Outlines risks and recovery"
                ],
                capabilities_used=["spine_surgery_consultation"],
                metadata={
                    "topic": "spine_surgery_general"
                }
            )

    def _handle_cauda_equina_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle cauda equina syndrome queries"""
        return DomainQueryResult(
            domain_name="neurosurgery",
            answer="""**CAUDA EQUINA SYNDROME (CES) - NEUROSURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **URGENT MRI WHOLE SPINE**
- **URGENT NEUROSURGICAL REFERRAL**
- **TIMELY SURGICAL DECOMPRESSION** (ideally <24-48 hours)

**WHAT IS IT?**
- Compression of cauda equina nerve roots (below conus medullaris)
- **Surgical emergency** - permanent damage if untreated
- Usually at **L4/5** or **L5/S1** level

**CAUSES:**
- **Large central disc prolapse** (most common)
- **Spinal stenosis**
- **Trauma** (vertebral fracture, haematoma)
- **Tumour** (metastasis, ependymoma)
- **Infection** (epidural abscess)
- **Iatrogenic** (post-spinal surgery)

**CLASSIC SYMPTOMS:**

**1. Saddle Anaesthesia**
- Numbness in saddle area (perineum, buttocks, genitals, anus)
- **Key feature** - highly suggestive

**2. Urinary Retention**
- Inability to pass urine
- **Overflow incontinence**
- **Loss of sensation of full bladder**
- **Painless retention**

**3. Bowel Dysfunction**
- Constipation
- **Faecal incontinence**
- **Loss of anal sphincter tone**

**4. Sexual Dysfunction**
- Erectile dysfunction
- Loss of sensation in genitals

**5. Bilateral Radiculopathy**
- Pain, numbness, weakness in **both legs**
- May be asymmetric

**6. Perineal Analgesia**
- Loss of pain sensation in perineum

**RED FLAGS (SUSPECT CES):**
- **Saddle anaesthesia**
- **Urinary retention** or **incontinence**
- **Faecal incontinence**
- **Bilateral leg symptoms**
- **Severe low back pain** with neurological symptoms

**DIAGNOSIS:**

**1. MRI Whole Spine (Urgent)**
- **Investigation of choice**
- Identify level and cause of compression
- May need gadolinium if infection/tumour suspected

**2. CT Spine**
- Alternative if MRI contraindicated
- Less sensitive than MRI

**MANAGEMENT:**

**1. Urgent Surgical Decompression**
- **Indicated for ALL patients with CES**
- **Procedure:**
  - Emergency laminectomy
  - Microdiscectomy (if disc prolapse)
  - Decompression of cauda equina
- **Timing:** Ideally within **24-48 hours** of symptom onset
  - Earlier intervention = better outcome
  - Even after 48 hours, surgery may still improve outcome

**2. Preoperative Preparation**
- **Catheterize** if urinary retention
- **Admit** to hospital
- **Nil by mouth** (prepare for surgery)
- **VTE prophylaxis** (compression stockings, LMWH post-op)

**3. Postoperative Care**
- **Catheter** remains in situ (may take weeks-months to recover)
- **Physiotherapy** (mobility, strengthening)
- **Bowel management** (laxatives, suppositories)
- **Bladder training** (if recovery)

**PROGNOSIS:**
- **Complete recovery:** 40-50% (if treated <24 hours)
- **Partial recovery:** 30-40%
- **Poor recovery:** 10-20% (persistent symptoms)
- **Better prognostic factors:**
  - Early decompression (<24 hours)
  - Incomplete CES (some sensation/motor preserved)
  - Younger age
  - Disc prolapse (vs other causes)
- **Worse prognostic factors:**
  - Delayed decompression (>48 hours)
  - Complete CES (total anaesthesia, total urinary retention)
  - Late presentation (>1 week)
  - Significant comorbidities

**RESIDUAL SYMPTOMS:**
- **Urinary dysfunction** (most common residual)
  - Incontinence, retention, frequency
  - May require intermittent self-catheterization
- **Bowel dysfunction**
  - Incontinence, constipation
- **Sexual dysfunction**
  - Erectile dysfunction, loss of sensation
- **Saddle anaesthesia**
- **Leg weakness, pain**

**COMPLICATIONS:**
- **Permanent neurological deficit** (if untreated or delayed)
- **Urinary tract infection** (from catheter)
- **DVT/PE** (from immobility)
- **Pressure sores** (if immobile)
- **Depression** (from chronic symptoms)

**MEDICO-LEGAL:**
- **Common cause of litigation**
- **Red flags must be recognized** by all healthcare professionals
- **Urgent referral** to neurosurgery is mandatory
- **Document symptoms, timing, referral clearly**

**EVIDENCE:** NICE NG232, SBNS Guidelines""",
            confidence=0.97,
            reasoning_trace=[
                "Identified cauda equina syndrome - neurosurgical emergency",
                "Applied classic red flags (saddle anaesthesia, urinary retention)",
                "Surgical decompression within 24-48 hours"
            ],
            capabilities_used=["spinal_cord_compression_management"],
            metadata={
                "urgency": "emergency",
                "condition": "cauda_equina_syndrome",
                "intervention": "surgical_decompression",
                "time_sensitive": "24_48_hours"
            }
        )

    def _handle_cervical_myelopathy_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle cervical myelopathy queries"""
        return DomainQueryResult(
            domain_name="neurosurgery",
            answer="""**CERVICAL SPONDYLOTIC MYELOPATHY (CSM)**

**WHAT IS IT?**
- Spinal cord compression in cervical spine
- Degenerative changes (disc osteophyte complex, ligamentum flavum hypertrophy, facet hypertrophy)
- Progressive, can cause permanent disability if untreated
- Most common cause of **spinal cord dysfunction** in adults >55 years

**SYMPTOMS:**

**Myelopathy (Spinal Cord Dysfunction):**
- **Gait disturbance** (most common early symptom)
  - Broad-based, shuffling gait
  - Difficulty with turns
  - Frequent falls
- **Hand clumsiness**
  - Difficulty with buttons, zippers, fine motor tasks
  - Dropping objects
- **Weakness** (upper and lower extremities)
- **Sensory changes** (numbness, tingling in hands)
- **Hyperreflexia** (brisk reflexes, Hoffman's sign, Babinski)
- **Spasticity** (stiffness, clonus)

**Radiculopathy (Nerve Root Compression) - May Coexist:**
- **Neck pain**
- **Radicular arm pain** (dermatomal)
- **Numbness, tingling** in arm/hand
- **Weakness** in specific myotome

**DIAGNOSIS:**

**1. MRI Cervical Spine (Investigation of Choice)**
- **Spinal cord compression** (level, extent)
- **T2 hyperintensity** in cord (myelomalacia - worse prognosis)
- **Disc osteophyte complex**
- **Ligamentum flavum hypertrophy**
- **Canal stenosis**

**2. CT Cervical Spine**
- Alternative if MRI contraindicated
- Shows bony anatomy well

**3. X-ray Cervical Spine**
- Dynamic flexion/extension (assess instability)
- Disc height loss, osteophytes

**MANAGEMENT:**

**Surgical Decompression (Generally Recommended):**
- **Indicated for:**
  - **Progressive myelopathy** (most)
  - **Moderate to severe myelopathy** (Nurick Grade 3-5)
  - **Significant cord compression** on MRI
- **Observation** NOT recommended (cord damage may be permanent)
- **No proven role for conservative management** (collar, physiotherapy)

**Surgical Procedures:**

**Anterior Cervical Discectomy and Fusion (ACDF):**
- **Most common** for 1-2 level disease
- **Approach:** Anterior (front of neck)
- **Procedure:**
  - Remove disc, osteophytes
  - Decompress spinal cord
  - Place interbody cage or bone graft
  - Plate anteriorly (instrumentation)
- **Outcomes:**
  - 70-90% improve or stabilize
  - Good fusion rate (>90%)
- **Complications:**
  - **Dysphagia** (transient 20-30%, permanent 2-5%)
  - **Hoarseness** (recurrent laryngeal nerve palsy - 2-5%)
  - **Dural tear** (2-5%)
  - **C5 palsy** (5-10%)
  - **Nonunion** (5%)
  - **Adjacent segment disease** (2-3% per year)

**Cervical Laminoplasty:**
- **Posterior approach**
- **Indicated for:**
  - 3+ level disease
  - Ossification of posterior longitudinal ligament (OPLL)
  - Lordotic spine
- **Procedure:** Expand spinal canal (hinge laminae open)
- **Outcomes:** Similar to ACDF for multilevel disease
- **Complications:** Axial neck pain, C5 palsy, kyphosis

**Cervical Laminectomy + Fusion:**
- **Posterior approach**
- **Indicated for:**
  - 3+ level disease
  - OPLL
  - Kyphotic spine
- **Procedure:** Remove laminae, instrumented fusion (lateral mass screws)
- **Outcomes:** Good decompression, but lose neck motion

**POSTOPERATIVE CARE:**
- **Mobilize day 1** (with collar if prescribed)
- **Collar** (soft or rigid) for 4-6 weeks (depending on procedure)
- **Physiotherapy** (neck range of motion once fused)
- **Serial X-rays** (assess fusion)

**PROGNOSIS:**
- **Improvement:** 70-80% stabilize or improve
- **Complete recovery:** Rare (cord damage may be permanent)
- **Stabilization:** 10-20% (no improvement, no progression)
- **Worsening:** <5% (despite surgery)
- **Better prognostic factors:**
  - Younger age
  - Shorter duration of symptoms (<12 months)
  - Less severe myelopathy (Nurick Grade 1-2)
  - No T2 hyperintensity in cord on MRI
- **Worse prognostic factors:**
  - Older age (>70 years)
  - Long duration of symptoms (>2 years)
  - Severe myelopathy (Nurick Grade 4-5)
  - T2 hyperintensity in cord (myelomalacia)

**NURICK GRADING (Cervical Myelopathy):**
- **Grade 0:** Signs of root involvement without myelopathy
- **Grade 1:** Signs of cord involvement but no difficulty walking
- **Grade 2:** Slight difficulty walking, does not prevent employment
- **Grade 3:** Difficulty walking preventing employment
- **Grade 4:** Able to walk only with assistance
- **Grade 5:** Chairbound or bedridden

**COMPLICATIONS:**
- **Permanent neurological deficit** (if untreated)
- **C5 palsy** (5-10%)
- **Dysphagia** (2-5% permanent)
- **Hoarseness** (2-5%)
- **Nonunion** (5%)
- **Adjacent segment disease** (common long-term)
- **Postoperative C5 palsy** (may recover)

**EVIDENCE:** NICE NG232, AANS/CNS Guidelines""",
            confidence=0.93,
            reasoning_trace=[
                "Identified cervical myelopathy query",
                "Surgical decompression generally recommended (observation not recommended)",
                "ACDF for 1-2 levels, laminoplasty/laminectomy for 3+ levels"
            ],
            capabilities_used=["spinal_cord_compression_management"],
            metadata={
                "topic": "cervical_myelopathy",
                "guideline": "nice_ng232"
            }
        )

    def _handle_peripheral_nerve_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle peripheral nerve queries"""
        query_lower = query.lower()

        # Carpal tunnel syndrome
        if any(term in query_lower for term in [
            "carpal tunnel", "cts", "carpal tunnel syndrome", "wrist numbness"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**CARPAL TUNNEL SYNDROME (CTS)**

**WHAT IS IT?**
- Compression of median nerve at wrist
- Most common **compressive neuropathy**
- **Female predominance** (F:M 3:1)
- Peak incidence: 40-60 years
- May be **bilateral** (50-60%)

**SYMPTOMS:**

**Classic Symptoms:**
- **Numbness, tingling** in thumb, index, middle, radial half of ring finger
- **Nocturnal symptoms** (wakes patient from sleep)
- **Activity-related** (driving, holding phone, reading)
- **Shaking hands** relieves symptoms
- **Hand weakness** (dropping objects)
- **Thenar atrophy** (advanced cases)

**PHYSICAL EXAMINATION:**
- **Tinel's sign** - tap over carpal tunnel → tingling in median distribution
- **Phalen's manoeuvre** - hold wrists flexed 60 seconds → symptoms reproduced
- **Carpal compression test** - direct pressure over tunnel → symptoms
- **Thenar atrophy** (advanced)
- **Abductor pollicis brevis weakness**

**DIAGNOSIS:**

**1. Clinical Diagnosis** (usually sufficient)
- Classic symptoms + positive physical examination
- No imaging needed for diagnosis

**2. Nerve Conduction Studies (NCS)**
- **Indicated if:**
  - Atypical symptoms
  - Prior to surgery (baseline)
  - Worker's compensation
  - Surgical failure (consider alternative diagnosis)
- **Shows:** Prolonged median nerve distal latency

**3. Ultrasound**
- May show median nerve enlargement
- Not routinely needed

**4. MRI**
- Not routinely indicated
- May consider if space-occupying lesion suspected

**CAUSES/RISK FACTORS:**
- **Idiopathic** (most common)
- **Repetitive hand use** (typing, assembly line)
- **Pregnancy** (fluid retention - usually resolves postpartum)
- **Rheumatoid arthritis**
- **Diabetes mellitus**
- **Hypothyroidism**
- **Obesity** (BMI >30)
- **Renal failure**
- **Family history**

**MANAGEMENT:**

**Conservative (First-Line for Mild-Moderate):**
- **Activity modification**
  - Avoid repetitive hand/wrist activities
  - Ergonomic assessment (workstation)
- **Wrist splint** (neutral position)
  - **Wear at night** (most effective)
  - May wear during day if symptoms provoked
  - Trial for 6-12 weeks
- **Corticosteroid injection**
  - Into carpal tunnel
  - 60-80% temporary relief
  - May last 3-12 months
  - May be repeated (max 2-3 injections)
- **Physiotherapy**
  - Nerve gliding exercises
  - Grasping exercises

**Surgery (Carpal Tunnel Release):**
- **Indicated for:**
  - **Severe symptoms** (thenar atrophy, weakness)
  - **Failed conservative management** (>3-6 months)
  - **Constant numbness**
  - **Patient preference**
- **Procedure:**
  - **Open release** (standard)
    - 2-3 cm incision at wrist
    - Divide transverse carpal ligament
    - Quick recovery
  - **Endoscopic release** (minimally invasive)
    - Smaller incision
    - Faster recovery, less scar pain
    - Higher cost, risk of nerve injury
- **Outcomes:**
  - 90-95% good/excellent
  - Rapid symptom relief
  - Return to light activities in 1-2 weeks
  - Return to heavy activities in 4-6 weeks
- **Complications:**
  - **Pillar pain** (10-20%) - scar tenderness, may last months
  - **Incomplete release** (<5%) - persistent symptoms, may need revision
  - **Nerve injury** (1-2%) - median nerve or palmar cutaneous branch
  - **Infection** (1%)
  - **Reflex sympathetic dystrophy** (<1%)

**POSTOPERATIVE CARE:**
- **Light dressings** for 10-14 days
- **Wound care** (keep dry)
- **Mobilize fingers** immediately
- **Gradual return to activities**
  - Light activities: 1-2 weeks
  - Driving: 2-4 weeks
  - Heavy activities: 4-6 weeks
- **Physiotherapy** (scar massage, desensitization)
- **Night splint** (if symptoms persist)

**PROGNOSIS:**
- **Conservative:** 30-50% improve (especially mild cases, pregnancy)
- **Surgical:** 90-95% good/excellent outcome
- **Recurrence:** <5% (after surgery)
- **Complete recovery:** Common if treated before thenar atrophy
- **Residual symptoms:** May persist if treatment delayed (>12 months)

**PREVENTION:**
- **Ergonomic workstation**
- **Frequent breaks** from repetitive activities
- **Wrist splints** (if symptoms provoked by activities)
- **Treat underlying conditions** (diabetes, hypothyroidism, RA)

**EVIDENCE:** NICE NG297, AAOS Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified carpal tunnel syndrome query",
                    "Conservative management first-line (splint, injection)",
                    "Surgery for severe symptoms or failed conservative"
                ],
                capabilities_used=["peripheral_nerve_surgery"],
                metadata={
                    "topic": "carpal_tunnel_syndrome",
                    "guideline": "nice_ng297"
                }
            )

        # Ulnar nerve entrapment
        elif any(term in query_lower for term in [
            "ulnar nerve", "cubital tunnel", "ulnar neuropathy", "ring little finger numbness"
        ]):
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**ULNAR NEUROPATHY (CUBITAL TUNNEL SYNDROME)**

**WHAT IS IT?**
- Compression of ulnar nerve at elbow (cubital tunnel)
- Second most common **compressive neuropathy** after CTS
- May occur at **wrist** (Guyon's canal) - less common

**SYMPTOMS:**

**Sensory:**
- **Numbness, tingling** in ring and little finger
- **Elbow pain** (aching)
- **Forearm pain** (may radiate to hand)
- **Symptoms worse with elbow flexion** (driving, talking on phone)

**Motor:**
- **Weakness** of grip (due to intrinsic muscle weakness)
- **Clumsiness** (dropping objects)
- **Difficulty with fine motor tasks** (buttoning, playing instruments)
- **Froment's sign** (use of abductor pollicis brevis to compensate for adductor pollicis)

**PHYSICAL EXAMINATION:**
- **Tinel's sign** at elbow - tap over cubital tunnel
- **Elbow flexion test** - hold elbow flexed 60 seconds → symptoms
- **Weakness** of intrinsic hand muscles (interossei, hypothenar)
- **Atrophy** of intrinsic muscles (advanced cases)
- **Positive Froment's sign** (thumb IP joint flexes when pinching paper)

**DIAGNOSIS:**

**1. Clinical Diagnosis** (usually sufficient)
- Classic symptoms + positive physical examination

**2. Nerve Conduction Studies (NCS)**
- **Indicated if:**
  - Atypical symptoms
  - Prior to surgery (baseline)
  - Surgical failure (consider alternative diagnosis)
- **Shows:** Prolonged ulnar nerve distal latency, slowing across elbow

**3. Ultrasound**
- May show ulnar nerve enlargement or subluxation
- Not routinely needed

**4. X-ray Elbow**
- Indicated if bony abnormality suspected (osteophyte, fracture)

**CAUSES/RISK FACTORS:**
- **Idiopathic** (most common)
- **Anatomical** (cubital tunnel retinaculum, Osborne's band)
- **Repetitive elbow flexion** (throwing, weightlifting)
- **Elbow trauma** (fracture, dislocation)
- **Osteoarthritis** (osteophytes)
- **Occupational** ( prolonged leaning on elbows)
- **Diabetes mellitus**

**CLASSIFICATION:**

**Mild:**
- Sensory symptoms only
- No weakness, no atrophy

**Moderate:**
- Sensory symptoms
- Mild weakness
- No atrophy

**Severe:**
- Sensory symptoms
- Weakness, atrophy
- Froment's sign positive

**MANAGEMENT:**

**Conservative (First-Line for Mild-Moderate):**
- **Activity modification**
  - Avoid prolonged elbow flexion
  - Avoid leaning on elbows
  - Ergonomic assessment
- **Elbow padding** (avoid direct pressure)
- **Night splinting**
  - Elbow splint in extension (30-45°)
  - Trial for 6-12 weeks
- **Physiotherapy**
  - Nerve gliding exercises
  - Stretching
- **Corticosteroid injection**
  - Around ulnar nerve (at cubital tunnel)
  - 40-60% temporary relief
  - May be repeated (max 2-3 injections)

**Surgery (Ulnar Nerve Decompression/Transposition):**
- **Indicated for:**
  - **Severe symptoms** (weakness, atrophy)
  - **Failed conservative management** (>3-6 months)
  - **Constant numbness**
  - **Subluxing nerve** (nerve dislocates over medial epicondyle)
  - **Patient preference**
- **Procedures:**
  - **Simple decompression**
    - Release cubital tunnel retinaculum
    - Leave nerve in situ
    - Quicker recovery, less morbidity
    - **Preferred for most** (better outcomes than transposition for most)
  - **Anterior transposition**
    - Move nerve anterior to medial epicondyle
    - **Subcutaneous** (most common)
    - **Submuscular** (if severe, revision surgery)
    - Indicated for:
      - Subluxing nerve
      - Revision surgery
      - Severe deformity/valgus elbow
- **Outcomes:**
  - 80-90% good/excellent
  - Symptom relief (especially sensory)
  - Motor recovery slower (may take 12-18 months)
  - Recovery may be incomplete if long-standing (>12 months)
- **Complications:**
  - **Incomplete release** (<5%)
  - **Nerve injury** (2-5%)
  - **Painful scar** (10-20%)
  - **Infection** (1%)
  - **Refractory symptoms** (10-20%)

**POSTOPERATIVE CARE:**
- **Light bandage** for 10-14 days
- **Mobilize fingers** immediately
- **Elbow range of motion** (as tolerated)
- **Gradual return to activities**
  - Light activities: 2-4 weeks
  - Heavy activities: 6-12 weeks
- **Physiotherapy** (scar massage, desensitization, strengthening)

**PROGNOSIS:**
- **Conservative:** 30-50% improve (especially mild cases)
- **Surgical:** 80-90% good/excellent outcome
- **Sensory recovery:** Common (weeks-months)
- **Motor recovery:** Slower (months-years), may be incomplete
- **Recurrence:** <5% (after surgery)
- **Worse prognostic factors:**
  - Long-standing symptoms (>12 months)
  - Severe atrophy
  - Age >60 years
  - Revision surgery

**EVIDENCE:** AAOS Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified ulnar nerve entrapment query",
                    "Conservative management first-line",
                    "Simple decompression preferred (better outcomes than transposition)"
                ],
                capabilities_used=["peripheral_nerve_surgery"],
                metadata={
                    "topic": "ulnar_neuropathy",
                    "guideline": "aaos"
                }
            )

        # General peripheral nerve
        else:
            return DomainQueryResult(
                domain_name="neurosurgery",
                answer="""**PERIPHERAL NERVE SURGERY**

**COMMON PERIPHERAL NERVE CONDITIONS:**

**Carpal Tunnel Syndrome**
- Median nerve compression at wrist
- Numbness, tingling in thumb, index, middle
- Nocturnal symptoms
- Splinting, injection first-line
- Surgery if severe or failed conservative

**Ulnar Neuropathy (Cubital Tunnel)**
- Ulnar nerve compression at elbow
- Numbness, tingling in ring, little finger
- Weakness of grip
- Splinting, physiotherapy first-line
- Simple decompression surgery (most)

**Other Entrapment Neuropathies:**
- **Tarsal tunnel** (tibial nerve at ankle)
- **Meralgia paraesthetica** (lateral femoral cutaneous nerve)
- **Suprascapular nerve** (shoulder)
- **Radial tunnel** (radial nerve at elbow)

**Nerve Injury:**
- **Trauma** (laceration, stretch, compression)
- **Iatrogenic** (surgery, injections)
- **Classification:**
  - **Neuropraxia** (conduction block, no axonal loss - recovers in weeks-months)
  - **Axonotmesis** (axon loss, endoneurium intact - recovers in months)
  - **Neurotmesis** (complete transection - surgery required)

**Surgery:**
- **Nerve repair** (primary if possible, delayed if contaminated)
- **Nerve graft** (if gap between nerve ends)
- **Nerve transfer** (for proximal injuries)
- **Decompression** (for entrapment neuropathies)

**DIAGNOSIS:**
- Clinical examination
- Nerve conduction studies
- EMG
- Ultrasound, MRI (selected cases)

**PROGNOSIS:**
- Variable (depends on injury, timing)
- Better with early intervention
- Recovery may be incomplete

**EVIDENCE:** AAOS Guidelines""",
                confidence=0.84,
                reasoning_trace=[
                    "Provided peripheral nerve overview",
                    "Carpal tunnel and ulnar neuropathy most common"
                ],
                capabilities_used=["peripheral_nerve_surgery"],
                metadata={
                    "topic": "peripheral_nerve_general"
                }
            )

    def _handle_general_neurosurgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general neurosurgery queries"""
        return DomainQueryResult(
            domain_name="neurosurgery",
            answer="""**NEUROSURGERY**

Neurosurgery is a specialty dealing with surgical disorders of the brain and spine.

**BRAIN SURGERY:**

**Tumours**
- **Glioma** (glioblastoma, low-grade glioma)
- **Meningioma** (usually benign)
- **Pituitary adenoma**
- **Acoustic neuroma**
- **Metastases**

**Vascular**
- **Subarachnoid haemorrhage** (aneurysm)
- **Intracerebral haemorrhage**
- **AVM** (arteriovenous malformation)
- **Cavernoma**

**Trauma**
- **Extradural haematoma** (surgical emergency)
- **Acute subdural haematoma** (surgical emergency)
- **Chronic subdural haematoma** (burr hole evacuation)
- **Depressed skull fracture**

**Hydrocephalus**
- **VP shunt** (ventriculoperitoneal shunt)
- **ETV** (endoscopic third ventriculostomy)
- **NPH** (normal pressure hydrocephalus)

**SPINE SURGERY:**

**Degenerative**
- **Herniated disc** (microdiscectomy)
- **Spinal stenosis** (laminectomy)
- **Spondylolisthesis** (decompression + fusion)
- **Cervical myelopathy** (decompression ± fusion)

**Emergency**
- **Cauda equina syndrome** (surgical decompression)
- **Spinal cord compression** (surgical decompression ± radiotherapy)

**Tumour**
- **Metastasis** (decompression ± fusion, radiotherapy)
- **Primary tumour** (resection)

**PERIPHERAL NERVE SURGERY:**

**Carpal Tunnel Syndrome**
- Most common compressive neuropathy
- Wrist splint, injection first-line
- Surgery if severe or failed conservative

**Ulnar Neuropathy**
- Second most common
- Simple decompression surgery (most)

**COMMON PROCEDURES:**

**Craniotomy**
- Open brain surgery
- For tumours, haematomas, AVMs

**Microdiscectomy**
- Minimally invasive disc surgery
- 80-90% good outcome

**Laminectomy**
- Remove lamina (decompression)
- For spinal stenosis

**Spinal Fusion**
- Permanently join vertebrae
- For instability, spondylolisthesis

**VP Shunt**
- Treat hydrocephalus
- Ventricular catheter → valve → peritoneal catheter

**NEUROSURGICAL EMERGENCIES:**
- Extradural haematoma (craniotomy)
- Acute subdural haematoma (craniotomy)
- Subarachnoid haemorrhage (coiling/clipping)
- Cauda equina syndrome (decompression)
- Spinal cord compression (decompression)

**Evidence:** NICE Guidelines, SBNS Guidelines""",
            confidence=0.82,
            reasoning_trace=[
                "Provided general neurosurgery overview",
                "Covered brain, spine, and peripheral nerve surgery",
                "Listed common procedures and emergencies"
            ],
            capabilities_used=[
                "brain_tumour_surgery",
                "traumatic_brain_injury_management",
                "spine_surgery_consultation"
            ],
            metadata={
                "topic": "neurosurgery_general"
            }
        )


def create_neurosurgery_domain():
    """Factory function for neurosurgery domain"""
    return NeurosurgeryDomain()
