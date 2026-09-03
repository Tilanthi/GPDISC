"""
Radiology/Medical Imaging Domain for GPDISC

Comprehensive radiology and medical imaging domain covering all imaging modalities
and their diagnostic applications across medical specialties.

Evidence-based: RCR (Royal College of Radiologists), ACR (American College of Radiology),
ESR (European Society of Radiology), NICE Guidelines
"""

from typing import Dict, Any, List, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import os

# Import DICOM processor
try:
    from .dicom_processor import (
        create_dicom_processor,
        DICOMProcessor,
        DICOMAnalysisResult,
        generate_dicom_report
    )
    DICOM_AVAILABLE = True
except ImportError:
    DICOM_AVAILABLE = False
    DICOMProcessor = None


class RadiologyDomain(BaseDomainModule):
    """
    Radiology and Medical Imaging Domain

    Covers all imaging modalities including:
    - Plain radiography (X-ray)
    - Computed tomography (CT)
    - Magnetic resonance imaging (MRI)
    - Ultrasound (US)
    - Nuclear medicine (PET, SPECT)
    - Interventional radiology
    - Contrast media and safety
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="radiology",
            version="1.0.0",
            dependencies=[],
            description="Radiology and medical imaging - X-ray, CT, MRI, ultrasound, nuclear medicine, interventional radiology",
            keywords=[
                # Imaging modalities
                "x-ray", "xray", "radiograph", "plain film", "chest x-ray", "cxr",
                "ct", "cat scan", "computed tomography", "ct scan",
                "mri", "magnetic resonance", "magnetic resonance imaging",
                "ultrasound", "us", "sonogram", "doppler", "echocardiogram",
                "pet", "spect", "nuclear medicine", "isotope scan", "bone scan",
                "interventional radiology", "angiogram", "angiography",
                "mammogram", "mammography", "breast imaging",
                "fluoroscopy", "barium", "contrast", "contrast media",
                # Image interpretation requests
                "interpret", "review", "report", "imaging findings", "radiological",
                "scan", "image", "film", "study", "examination",
                # Clinical scenarios
                "pulmonary embolism", "pe", "ctpa", "v/q scan",
                "appendicitis", "abdominal pain", "ct abdomen",
                "head injury", "intracranial bleed", "ct head",
                "stroke", "mri brain", "ct brain",
                "fracture", "bone x-ray", "skeletal survey",
                "contrast allergy", "contrast reaction", "contrast induced nephropathy",
                "radiation dose", "radiation risk", "pregnancy", "contrast safety",
                # DICOM and image file analysis
                "dicom", ".dcm", "dicom file", "dicom image", "analyze dicom",
                "dicom analysis", "dicom metadata", "dicom processing",
                "medical image file", "scan file", "image file analysis",
                "load dicom", "read dicom", "dicom viewer", "dicom report"
            ],
            capabilities=[
                "imaging_modality_selection", "image_interpretation_guidance",
                "contrast_safety_assessment", "radiation_safety_counselling",
                "interventional_radiology_guidance", "emergency_imaging_protocols",
                "dicom_file_analysis", "dicom_metadata_extraction",
                "medical_image_processing", "dicom_report_generation"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        query_lower = query.lower()

        # DICOM FILE ANALYSIS (NEW)
        if any(term in query_lower for term in ["dicom", ".dcm", "dicom file", "analyze dicom",
                                                   "dicom analysis", "dicom metadata",
                                                   "load dicom", "read dicom", "dicom report"]):
            return self._handle_dicom_analysis(query, context)

        # EMERGENCY: Contrast anaphylaxis
        if any(term in query_lower for term in ["contrast anaphylaxis", "anaphylactic reaction", "severe contrast reaction",
                                                   "contrast shock", "life-threatening contrast"]):
            return self._handle_contrast_anaphylaxis(query, context)

        # EMERGENCY: Contrast extravasation
        if any(term in query_lower for term in ["contrast extravasation", "contrast leak", "tissue injury"]):
            return self._handle_contrast_extravasation(query, context)

        # EMERGENCY: Pregnancy radiation exposure
        if any(term in query_lower for term in ["pregnant", "pregnancy", "radiation exposure in pregnancy",
                                                   " fetal radiation", "radiation dose pregnancy"]):
            return self._handle_pregnancy_radiation(query, context)

        # CT ANGIGRAPHY (CTPA, AORTIC DISSECTION)
        if any(term in query_lower for term in ["ctpa", "ct pulmonary angiogram", "pe protocol",
                                                   "pulmonary embolism ct", "aortic dissection ct"]):
            return self._handle_ct_angiography(query, context)

        # HEAD CT (trauma, stroke, bleed)
        if any(term in query_lower for term in ["ct head", "head ct", "brain ct", "intracranial",
                                                   "subarachnoid", "subdural", "extradural", "intracerebral"]):
            return self._handle_head_ct(query, context)

        # CHEST X-RAY
        if any(term in query_lower for term in ["chest x-ray", "cxr", "chest radiograph", "chest film"]):
            return self._handle_chest_xray(query, context)

        # IMAGING FOR APPENDICITIS/ABDOMINAL PAIN
        if any(term in query_lower for term in ["appendicitis", "ct abdomen", "ct appendicitis",
                                                   "right iliac fossa pain", "rlq pain"]):
            return self._handle_appendicitis_imaging(query, context)

        # MRI CONTRAST (gadolinium safety)
        if any(term in query_lower for term in ["gadolinium", "mri contrast", "gadolinium safety",
                                                   "nsf", "nephrogenic systemic fibrosis"]):
            return self._handle_mri_contrast(query, context)

        # CONTRAST MEDIA SAFETY
        if any(term in query_lower for term in ["contrast", "contrast media", "iodinated contrast",
                                                   "contrast allergy", "contrast safety", "contrast reaction"]):
            return self._handle_contrast_safety(query, context)

        # RADIATION SAFETY
        if any(term in query_lower for term in ["radiation dose", "radiation risk", "radiation safety",
                                                   "radiation exposure", "radiation protection"]):
            return self._handle_radiation_safety(query, context)

        # IMAGING MODALITY SELECTION
        if any(term in query_lower for term in ["which imaging", "what scan", "best imaging", "imaging choice",
                                                   "modality selection", "scan choice"]):
            return self._handle_modality_selection(query, context)

        # GENERAL RADIOLOGY
        else:
            return self._handle_general_radiology(query, context)

    def _handle_contrast_anaphylaxis(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Contrast anaphylaxis management"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**CONTRAST ANAPHYLAXIS - EMERGENCY MANAGEMENT**

**IMMEDIATE ACTION (Call for help, activate emergency team):**

1. **STOP contrast injection immediately**

2. **ABCDE assessment:**
   - **Airway:** Assess patency, prepare for intubation
   - **Breathing:** Oxygen 15 L/min, check respiratory effort, auscultate
   - **Circulation:** IV access, BP monitoring, ECG
   - **Disability:** GCS, pupil response, conscious level
   - **Exposure:** Full examination, skin inspection (urticaria, angioedema)

3. **IMMEDIATE ADRENALINE (EPINEPHRINE):**
   - **IM adrenaline 1:1000 (500 mcg)**: 0.5 mL IM into anterolateral thigh
   - Repeat every 5 minutes if no improvement
   - **IV adrenaline (if cardiac arrest/imminent):** 50 mcg bolus, titrate

4. **ADJUNCTIVE TREATMENTS:**
   - **Oxygen:** High-flow (15 L/min) via non-rebreather mask
   - **Fluids:** IV crystalloid bolus (500-1000 mL) for hypotension
   - **Antihistamine:** IV chlorphenamine 10 mg (non-urgent)
   - **Steroids:** IV hydrocortisone 200 mg (non-urgent, prevent biphasic reaction)

5. **MONITORING:**
   - Continuous ECG, SpO2, BP monitoring
   - Observe for minimum 6-12 hours (severe reactions)
   - Watch for biphasic reaction (recurrence within 8-12 hours)

**POST-REACTION MANAGEMENT:**
- Document reaction grade (Radiological Society grade 1-5)
- Refer to allergy clinic for skin testing
- Issue MedicAlert identifying contrast allergy
- Future scans: Use alternative contrast or premedication (if essential)

**SOURCES:** RCR Guidelines, Resuscitation Council (UK), ACR Manual on Contrast Media""",
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "Resuscitation Council (UK)", "ACR Manual on Contrast Media"],
                "emergency_protocol": "contrast_anaphylaxis"
            }
        )

    def _handle_contrast_extravasation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Contrast extravasation management"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**CONTRAST EXTRAVASATION - IMMEDIATE MANAGEMENT**

**ASSESSMENT:**

1. **STOP injection immediately**

2. **Assess severity:**
   - **Mild:** <50 mL, minimal swelling, no pain
   - **Moderate:** 50-100 mL, swelling, mild pain
   - **Severe:** >100 mL, tense swelling, severe pain, blistering, compartment syndrome signs

3. **Document:**
   - Volume and type of contrast extravasated
   - Site of extravasation
   - Patient symptoms (pain, numbness, pallor)

**MANAGEMENT:**

**MILD CASES (<50 mL):**
- Elevate limb above heart level
- Observe for 2-4 hours
- Review patient before discharge
- Advise to return if worsening pain/swelling

**MODERATE CASES (50-100 mL):**
- Elevate limb
- Apply warm compresses (vasodilatation, improve absorption)
- Observe for 4-6 hours
- Consider surgical review if worsening

**SEVERE CASES (>100 mL or signs of compartment syndrome):**
- **Urgent plastics/surgical review**
- ELEVATE limb
- DO NOT apply heat or massage (may increase tissue damage)
- Consider fasciotomy if compartment syndrome suspected
- Monitor for nerve injury, skin necrosis, tissue loss

**FOLLOW-UP:**
- Review at 24-48 hours
- Monitor for late sequelae (necrosis, ulceration, compartment syndrome)
- Document in radiology report and patient notes

**CONTRAST TYPES AND TISSUE TOXICITY:**
- **Ionic contrast:** Higher tissue toxicity
- **Non-ionic contrast:** Lower tissue toxicity (most commonly used)
- **Gadolinium:** Generally well-tolerated in tissues

**SOURCES:** RCR Guidelines, ACR Manual on Contrast Media""",
            confidence=0.90,
            metadata={
                "urgency": "urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Manual on Contrast Media"],
                "emergency_protocol": "contrast_extravasation"
            }
        )

    def _handle_pregnancy_radiation(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """EMERGENCY: Radiation exposure in pregnancy assessment and counselling"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**RADIATION IN PREGNANCY - ASSESSMENT AND COUNSELLING**

**KEY PRINCIPLE:** No diagnostic X-ray is绝对 contraindicated in pregnancy - benefit vs. risk assessment required.

**RADIATION DOSES:**

| Examination | Fetal Dose (mGy) |
|-------------|------------------|
| Chest X-ray | 0.0001-0.01 |
| Abdominal X-ray | 0.1-3 |
| CT Head | <0.01 |
| CT Chest | 0.01-0.1 |
| CT Abdomen/Pelvis | 8-50 |
| CT Pulmonary Angiogram (CTPA) | 0.01-0.1 |
| V/Q Scan | 0.1-0.5 |
| Nuclear medicine | Variable |

**RISK THRESHOLDS:**

- **<50 mGy:** No increased risk (no indication for termination)
- **50-100 mGy:** Possible risk, discuss with patient
- **>100 mGy:** Increased risk of fetal damage, consider termination discussion

**Deterministic effects (threshold doses):**
- **>100 mGy:** Potential for fetal growth restriction
- **>500 mGy:** Potential for intellectual disability, microcephaly
- **>1 Gy:** High risk of severe neurological damage, fetal death

**Stochastic effects (no safe threshold):**
- **Childhood cancer:** 1 in 2000 background risk → 1 in 1000 at 10 mGy
- Absolute risk remains LOW even at high doses

**CLINICAL SCENARIOS:**

**1. PULMONARY EMBOLISM (PE) IN PREGNANCY:**
- **First-line:** CTPA (lower fetal dose, better maternal risk profile)
- **Alternative:** V/Q scan (especially if known PE, chest X-ray abnormal)
- **Chest X-ray:** Safe (dose negligible)

**2. APPENDICITIS IN PREGNANCY:**
- **First-line:** MRI (no ionising radiation)
- **Alternative:** USS (limited in later pregnancy)
- **CT:** Consider if MRI unavailable, benefit outweighs risk

**3. TRAUMA IN PREGNANCY:**
- **Life-threatening maternal injury:** Proceed with CT without delay
- **Minor trauma:** Consider modalities with lower dose (USS, MRI)

**COUNSELLING PATIENTS:**

- Explain the actual radiation dose in context
- Discuss the clinical indication (why the scan is needed)
- Discuss the risks of NOT imaging (missed diagnosis)
- Document the discussion in medical records

**PROTECTION MEASURES:**

- Use lead shielding where appropriate (abdominal shielding for non-pelvic imaging)
- Limit scan range to area of interest
- Use low-dose protocols where possible
- Consider alternative modalities (USS, MRI)

**DOCUMENTATION:**

- Record gestational age at time of exposure
- Record estimated fetal dose
- Record counselling discussion
- Document decision to proceed/defer

**SOURCES:** RCR Guidelines, ACR Guidance, RANZCR Guidelines, NICE Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Guidance", "RANZCR Guidelines", "NICE Guidelines"],
                "emergency_protocol": "pregnancy_radiation"
            }
        )

    def _handle_ct_angiography(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """CT angiography protocols and interpretation (CTPA, aortic dissection)"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**CT ANGIOGRAPHY - CTPA AND AORTIC DISSECTION**

**CT PULMONARY ANGIOGRAM (CTPA) FOR PULMONARY EMBOLISM:**

**Indications:**
- High clinical suspicion of PE ( Wells/PERC score)
- Abnormal V/Q scan or non-diagnostic V/Q
- Need alternative diagnosis (e.g., aortic dissection)

**Protocol:**
- **Contrast:** 50-100 mL iodinated contrast (350-370 mgI/mL)
- **Injection rate:** 4-5 mL/s
- **Timing:** Bolus tracking (main pulmonary artery)
- **Slice thickness:** 1-1.25 mm reconstructions
- **Gantry:** 0.5-0.625 mm detector width

**Interpretation:**

1. **Positive PE findings:**
   - Filling defect in pulmonary artery (partial or complete)
   - "Railroad track" sign (partial filling defect with contrast around)
   - "Polo mint" sign (complete filling defect seen en face)
   - Distal vessels may be occluded (oligaemia)

2. **Right heart strain signs:**
   - Right ventricular dilatation (RV:LV ratio >1.0)
   - Bowing of interventricular septum
   - Reflux of contrast into IVC/hepatic veins
   - SVC/right atrium distension

3. **Alternative diagnoses:**
   - Aortic dissection (fluoroscopy look at aorta)
   - Pneumonia/consolidation
   - Pleural effusion
   - Lung mass
   - Rib fracture (trauma)

**AORTIC DISSECTION CT:**

**Protocol (CT Aortogram):**
- **Contrast:** 80-120 mL iodinated contrast
- **Injection rate:** 4-5 mL/s
- **Timing:** Bolus tracking (ascending aorta at level of pulmonary artery)
- **Coverage:** Entire aorta (arch to iliac bifurcation)
- **ECG-gating:** Consider for ascending aorta assessment (reduce motion artefact)

**Interpretation (Stanford Classification):**

**Type A (Surgical emergency):**
- Ascending aorta involvement
- May extend into arch, descending aorta
- **Complications:** Cardiac tamponade, aortic regurgitation, myocardial infarction, stroke

**Type B (Medical management initially):**
- Descending aorta only (distal to left subclavian)
- Medical management unless complications

**Key Signs:**
- **Intimal flap:** Double lumen aorta
- **True vs. false lumen:** False lumen usually larger, slower flow
- **Entry tear:** Site of communication between true and false lumen
- **Branch vessel involvement:** Coronary, carotid, subclavian, renal, mesenteric, iliac arteries

**Contrast Considerations:**
- **eGFR >45:** No pre-hydration required
- **eGFR 30-45:** Consider pre-hydration (1 mL/kg 1 hour before, 4-6 hours after)
- **eGFR <30:** Discuss with referrer, consider alternative imaging
- **Contrast allergy:** Premedication (prednisolone 50 mg 13h, 7h, 1h before + cetirizine 10 mg 1h before) or use alternative modality

**Sources:** RCR Guidelines, NICE Guidelines, British Thoracic Society Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "NICE Guidelines", "British Thoracic Society Guidelines"]
            }
        )

    def _handle_head_ct(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Head CT interpretation and indications"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**HEAD CT - TRAUMA AND STROKE**

**INDICATIONS:**

**Trauma:**
- Head injury with GCS <15 at 2 hours post-injury
- Suspected intracranial bleed (any GCS)
- Penetrating head injury
- Focal neurological deficit
- Seizure post-head injury
- Coagulopathy + head injury
- Warfarin + head injury
- Loss of consciousness >5 minutes
- Amnesia >30 minutes post-injury

**Stroke (Hyperacute):**
- FAST positive (Face, Arm, Speech, Time)
- Onset <4.5 hours (thrombolysis window)
- Onset <6 hours (thrombectomy window - extended criteria)

**Protocol:**

**Non-contrast CT (NCCT) - first-line for trauma/stroke:**
- 5 mm axial slices (brain window)
- 1-1.25 mm coronal/sagittal reconstructions (bone window)
- Assess:
  - Brain parenchyma (bleed, infarct, mass, oedema)
  - Skull (fracture, lucencies, air)
  - Ventricles (size, asymmetry, shift)
  - Extra-axial spaces (blood, collections)

**CT Angiogram (CTA) - for stroke:**
- CTA Circle of Willis (vessel occlusion, aneurysm, AVM)
- CTA Carotids (carotid stenosis, dissection)
- CT Perfusion (penumbra vs. infarct core)

**INTERPRETATION - TRAUMA:**

**Extra-axial blood:**

1. **Extradural (epidural) haematoma:**
   - **Location:** Between skull and dura (lentiform/biconvex)
   - **Crosses sutures:** YES (does not cross suture lines)
   - **Crosses falx:** NO (stops at falx/tentorium)
   - **Arterial source:** Middle meningeal artery (temporal bone fracture)
   - **Lucid interval:** May have initial consciousness then rapid deterioration
   - **Urgency:** Surgical emergency

2. **Acute subdural haematoma:**
   - **Location:** Between dura and arachnoid (crescent-shaped)
   - **Crosses sutures:** YES
   - **Crosses falx:** YES
   - **Venous source:** Bridging veins (brain atrophy, shearing forces)
   - **Associated:** Underlying brain injury
   - **Urgency:** Surgical if significant mass effect (>5 mm midline shift)

3. **Chronic subdural haematoma:**
   - **Appearance:** Hypodense (same density as CSF)
   - **Location:** Crescentic collection
   - **Clinical:** Insidious onset, confusion, falls in elderly
   - **Urgency:** Surgical if symptomatic

4. **Subarachnoid haemorrhage (SAH):**
   - **Location:** Subarachnoid space (sulci, basal cisterns)
   - **Appearance:** Hyperdense blood in CSF spaces
   - **Common:** Circle of Willis (ruptured aneurysm)
   - **Urgency:** CTA for aneurysm, neurosurgical referral

**Intra-axial injuries:**
- **Contusion:** Focal brain injury (frontal/temporal poles common)
- **Intracerebral haematoma:** Parenchymal bleed with mass effect
- **Diffuse axonal injury:** Multiple small petechial haemorrhages, shearing injury
- **Oedema:** Hypodense areas, mass effect

**INTERPRETATION - STROKE:**

**Early ischaemic signs (within 6 hours):**
- **Loss of grey-white matter differentiation** (insular ribbon, lentiform nucleus)
- **Sulcal effacement** (brain swelling)
- **Hyperdense artery sign** (middle cerebral artery thrombus)
- **Hypoattenuation** (infarct core)

**CT Perfusion (CTP):**
- **Infarct core:** Cerebral blood volume (CBV) reduced (<30% of normal)
- **Penumbra:** Mean transit time (MTT) prolonged, CBV preserved (salvageable brain)
- **Mismatch:** Penumbra > Core (candidate for thrombectomy)

**Early CT signs of middle cerebral artery (MCA) infarct:**
- Hyperdense MCA sign (thrombus)
- Loss of insular ribbon (insular cortex)
- Loss of lentiform nucleus differentiation (basal ganglia)
- Sulcal effacement (brain swelling)

**Sources:** RCR Guidelines, NICE Guidelines, SIGN Guidelines, RCS (Edinburgh) Head Injury Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "NICE Guidelines", "SIGN Guidelines", "RCS (Edinburgh) Head Injury Guidelines"]
            }
        )

    def _handle_chest_xray(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Chest X-ray interpretation and systematic approach"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**CHEST X-RAY - SYSTEMATIC APPROACH AND INTERPRETATION**

**SYSTEMATIC APPROACH:**

Use **ABCDE** or **PIRPLE** mnemonic:

**PIRPLE:**
- **P:** Patient details (name, DOB, date, time, side markers)
- **I:** Inspiration (count anterior ribs - should see 6-7 anterior ribs, 10-11 posterior ribs)
- **R:** Rotation (spinous process alignment, clavicular asymmetry)
- **P:** Projection (PA vs. AP - heart appears larger on AP)
- **L:** Lung fields (compare left vs. right)
- **E:** Everything else (bones, soft tissues, tubes, lines, devices)

**DETAILED ASSESSMENT:**

**1. AIRWAY:**
- Trachea central? (deviation suggests tension pneumothorax, mediastinal shift)
- Carina angle (bifurcation of trachea) - normal <60 degrees, widened suggests left atrial enlargement

**2. BREATHING (LUNGS):**
- **Compare left vs. right:** Symmetry, density, transparency
- **Normal:** Lungs are black (air-filled)
- **White (opacity):** Fluid, consolidation, collapse, mass, fibrosis

**Common pathologies:**
- **Pneumonia:** Consolidation (air bronchograms, lobar distribution)
- **Pulmonary oedema:** Bat wing distribution, interstitial oedema (Kerley B lines), cardiomegaly
- **Pleural effusion:** Blunted costophrenic angle, meniscus sign, mediastinal shift if large
- **Pneumothorax:** Absent lung markings, visceral pleural line visible
- **Collapse (atelectasis):** Volume loss, mediastinal shift toward affected side
- **Mass:** Round opacity, spiculation (suggests malignancy), cavitation
- **Fibrosis:** Reticular opacities, reduced lung volumes

**3. CIRCULATION (CARDIOVASCULAR):**
- **Heart size:** Cardiothoracic ratio (CTR) <50% on PA film
  - CTR >50% = Cardiomegaly
  - CTR unreliable on AP film (magnification)
- **Heart borders:**
  - **Right heart border:** Right atrium
  - **Left heart border:** Left atrial appendage (superior), Left ventricle (inferior)
  - **Loss of heart border:** Silhouette sign (adjacent consolidation)
- **Aorta:** Knuckle of ascending aorta, descending aorta (aortic knob)
- **Pulmonary vasculature:**
  - **Upper lobe diversion:** Pulmonary oedema (redistribution to upper lobes)
  - **Pulmonary hypertension:** Enlarged pulmonary arteries

**4. DISABILITY (BONES AND SOFT TISSUES):**
- **Bones:** Ribs, clavicles, scapulae, spine (fractures, lytic lesions, sclerosis)
- **Soft tissues:** Breast shadows, chest wall masses
- **Pleura:** Thickening, pleural plaques (asbestos), effusions
- **Diaphragm:** Hemidiaphragm position (elevated in phrenic nerve palsy, eventration)
- **Gastric bubble:** Assess below left hemidiaphragm

**5. EVERYTHING ELSE (TUBES, LINES, DEVICES):**
- **Endotracheal tube:** Tip 5 cm above carina (T4 level), in trachea (not right main bronchus)
- **Central venous line:** Tip in SVC (T5-7), not in right atrium
- **Nasogastric tube:** Tip in stomach (below diaphragm)
- **Chest drain:** Positioned in pleural space (apical for pneumothorax, basal for effusion)
- **Pacemaker/ICD:** Leads in right atrium/right ventricle
- **Cardiac surgery:** Sternal wires, prosthetic valves

**COMMON ABNORMALITIES:**

**PNEUMONIA:**
- **Lobar pneumonia:** Airspace consolidation, lobar distribution, air bronchograms
- **Bronchopneumonia:** Patchy consolidation, bilateral, peribronchial
- **Typical organisms:** Strep. pneumoniae, H. influenzae, Staph. aureus
- **Atypical organisms:** Mycoplasma, Legionella (less consolidation)

**PULMONARY OEDEMA:**
- **Cardiogenic:** Cardiomegaly, upper lobe diversion, interstitial oedema (Kerley B lines), alveolar oedema (bat wing), pleural effusions
- **Non-cardiogenic:** Normal heart size, widespread alveolar oedema (ARDS)

**PNEUMOTHORAX:**
- **Visible visceral pleural line:** Thin white line (lung edge)
- **Absent lung markings:** Beyond visceral pleural line
- **Tension pneumothorax:** Mediastinal shift away from affected side, flattened hemidiaphragm, contralateral compression

**PLEURAL EFFUSION:**
- **Small:** Blunted costophrenic angle
- **Moderate:** Meniscus sign, homogeneous opacity
- **Large:** Mediastinal shift away from effusion
- **Loculated:** Does not shift with decubitus films

**Sources:** RCR Guidelines, NICE Guidelines, BTS Guidelines""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "NICE Guidelines", "BTS Guidelines"]
            }
        )

    def _handle_appendicitis_imaging(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Imaging for appendicitis and right iliac fossa pain"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**IMAGING FOR APPENDICITIS AND RIGHT ILIAC FOSSA PAIN**

**IMAGING MODALITY SELECTION:**

**PREGNANT PATIENTS:**
1. **First-line:** MRI (no ionising radiation, excellent for appendix)
2. **Second-line:** Ultrasound (limited in later pregnancy)
3. **CT:** Consider if MRI unavailable, benefit outweighs risk

**PAEDIATRIC PATIENTS:**
1. **First-line:** Ultrasound (no ionising radiation)
2. **Second-line:** CT if USS non-diagnostic (radiation concerns)

**ADULTS:**
1. **First-line:** CT abdomen/pelvis (high sensitivity and specificity)
2. **Alternative:** MRI (if available, avoids radiation)
3. **Limited role for USS:** Operator-dependent, less sensitive

**ULTRASOUND FINDINGS (APPENDICITIS):**

**Normal appendix:**
- Diameter <6 mm
- Compressible
- No peri-appendiceal fat stranding
- Visible blind-ended tubular structure

**Positive findings:**
- **Diameter >6 mm** (non-compressible)
- **Appendicolith** (echogenic focus with shadowing)
- **Peri-appendiceal fat stranding** (increased echogenicity)
- **Appendiceal wall hyperaemia** (on Doppler)
- **Fluid collection** (abscess formation)
- **Enlarged mesenteric lymph nodes**

**LIMITATIONS OF USS:**
- Operator-dependent
- Limited by bowel gas, body habitus
- Appendix not visualised in up to 50% of cases
- Non-diagnostic USS requires CT

**CT FINDINGS (APPENDICITIS):**

**Positive findings:**
- **Dilated appendix:** >6 mm diameter
- **Appendiceal wall thickening:** >3 mm
- **Peri-appendiceal fat stranding:** Inflammatory fat stranding
- **Appendicolith:** Calcified faecolith (present in 25%)
- **Abscess:** Fluid collection, phlegmon, enhancing wall
- **Enhancement:** Mural enhancement (contrast administration)

**Alternative diagnoses on CT:**
- **Crohn's disease:** Terminal ileum thickening, skip lesions
- **Ovarian pathology:** Cyst, torsion, mass (CT limited, consider USS)
- **Diverticulitis:** Right-sided (caecal diverticulitis) mimics appendicitis
- **Mesenteric adenitis:** Enlarged lymph nodes, normal appendix
- **Gynaecological:** Ovarian cyst, torsion, ectopic pregnancy (beta-hCG correlation)
- **Urological:** Renal colic (CT KUB for stones)

**CT PROTOCOL (APPENDICITIS):**

**Standard CT Abdomen/Pelvis:**
- **Contrast:** IV contrast (portal venous phase, 70 seconds)
- **Oral contrast:** Optional (some centres omit)
- **Rectal contrast:** Optional (helps with rectal and sigmoid pathology)
- **Slice thickness:** 1-2 mm reconstructions (multiplanar reformats)
- **Coverage:** From diaphragm to symphysis pubis

**Radiation dose:**
- Typical effective dose: 5-10 mSv
- Pregnancy: Consider MRI or low-dose CT protocol
- Paediatrics: Use low-dose protocol (ALARA principle)

**ALTERNATIVE DIAGNOSES (RIGHT ILIAC FOSSA PAIN):**

**Gynaecological (females):**
- **Ovarian cyst:** Rupture, torsion, haemorrhage
- **Ectopic pregnancy:** Positive beta-hCG
- **Pelvic inflammatory disease:** Cervical discharge, adnexal tenderness
- **Mittelschmerz:** Mid-cycle ovulation pain

**Urological:**
- **Renal colic:** Ureteric calculus, hydronephrosis
- **Urinary tract infection:** Dysuria, frequency, fever
- **Epididymo-orchitis:** Testicular pain, swelling

**Gastrointestinal:**
- **Crohn's disease:** Terminal ileitis, diarrhoea, weight loss
- **Caecal cancer:** Mass, weight loss, anaemia
- **Gastroenteritis:** Diarrhoea, vomiting, fever

**Sources:** RCR Guidelines, NICE Guidelines, ACR Appropriateness Criteria""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "NICE Guidelines", "ACR Appropriateness Criteria"]
            }
        )

    def _handle_mri_contrast(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """MRI contrast (gadolinium) safety and considerations"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**MRI CONTRAST (GADOLINIUM) SAFETY**

**GADOLINIUM-BASED CONTRAST AGENTS (GBCAs):**

**Classification (by risk of NSF):**

**GROUP 1 (Highest risk - CONTRAINDICATED in renal failure):**
- **Gadodiamide (Omniscan)** - Linear, non-ionic
- **Gadoversetamide (OptiMARK)** - Linear, non-ionic
- **Gadopentetate dimeglumine (Magnevist)** - Linear, ionic

**GROUP 2 (Intermediate risk - AVOID in severe renal impairment):**
- **Gadobenate dimeglumine (MultiHance)** - Linear, ionic
- **Gadoxetate disodium (Primovist)** - Linear, ionic
- **Gadofosveset (Vasovist)** - Linear, ionic

**GROUP 3 (Lowest risk - safe in renal impairment):**
- **Gadoteridol (ProHance)** - Macrocyclic
- **Gadobutrol (Gadovist)** - Macrocyclic
- **Gadoteric acid (Dotarem)** - Macrocyclic
- **Gadoterate meglumine (Dotarem)** - Macrocyclic

**NEPHROGENIC SYSTEMIC FIBROSIS (NSF):**

**Risk factors:**
- Severe renal impairment (eGFR <30 mL/min/1.73 m²)
- Acute kidney injury (AKI)
- Hepatorenal syndrome
- Peri-operative liver transplantation
- High-dose or repeat gadolinium exposure

**Clinical features:**
- Skin thickening and fibrosis (peau d'orange)
- Joint contractures
- Systemic fibrosis (lungs, heart, diaphragm)
- Onset: days to months post-exposure
- **Potentially fatal**

**Prevention:**
- Use GROUP 3 (macrocyclic) agents in patients with eGFR 30-60 mL/min/1.73 m²
- AVOID gadolinium in severe renal impairment (eGFR <30 mL/min/1.73 m²)
- If essential: Use GROUP 3 agent, lowest effective dose, discuss risks
- Dialysis: Consider dialysis post-exposure (controversial, may help eliminate)

**GADOLINIUM DEPOSITION:**

**Brain deposition:**
- Dentate nucleus and globus pallidus hyperintensity on unenhanced T1-weighted MRI
- Seen with repeated gadolinium exposure (especially linear agents)
- Clinical significance: Unclear, no clear neurological symptoms reported
- Prefer macrocyclic agents to minimise deposition

**PREGNANCY AND BREASTFEEDING:**

**Pregnancy:**
- **Avoid gadolinium in pregnancy** unless essential
- Gadolinium crosses placenta, fetal exposure unknown
- Consider alternative imaging (non-contrast MRI, USS)
- **First trimester:** Avoid unless critical (organogenesis period)

**Breastfeeding:**
- **Safe to continue breastfeeding** after gadolinium
- <0.04% of maternal dose excreted in breast milk
- <0.0004% of infant dose absorbed from gut
- **Option:** Patient may choose to express and discard breast milk for 24 hours (reassurance)

**CONTRAST REACTIONS:**

**Acute adverse reactions (<1 hour):**
- **Mild:** Nausea, headache, flushing (self-limiting)
- **Moderate:** Urticaria, dyspnoea, mild hypotension
- **Severe:** Anaphylaxis (rare, <0.01%)

**Management:**
- **Stop injection immediately**
- **Supportive care:** Airway, breathing, circulation
- **Adrenaline:** If anaphylaxis (same protocol as iodinated contrast)
- **Antihistamine:** Chlorphenamine for urticaria
- **Steroids:** Hydrocortisone (non-urgent)

**LATE ADVERSE REACTIONS (1 hour to 7 days):**
- **Nephrogenic systemic fibrosis (NSF):** Discussed above
- **Gadolinium-associated plaques:** Rare skin reactions
- **Arthralgia:** Joint pain

**CONTRAINDICATIONS:**

**Absolute:**
- Previous severe anaphylaxis to gadolinium
- Severe renal impairment (eGFR <30 mL/min/1.73 m²) for Group 1 agents

**Relative:**
- Pregnancy (benefit vs. risk discussion required)
- Severe renal impairment (eGFR <30 mL/min/1.73 m²) for Group 2/3 agents
- Previous mild/moderate reaction (premedication may be considered)

**Sources:** RCR Guidelines, ACR Manual on Contrast Media, ESUR Guidelines""",
            confidence=0.92,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Manual on Contrast Media", "ESUR Guidelines"]
            }
        )

    def _handle_contrast_safety(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Contrast media safety assessment and pre-medication"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**CONTRAST MEDIA SAFETY - IODINATED CONTRAST**

**IODINATED CONTRAST AGENTS:**

**Classification:**

**Osmolality:**
- **High-osmolar:** Ionic monomers (e.g., sodium diatrizoate) - RARELY used
- **Low-osmolar:** Non-ionic monomers (e.g., iohexol, iopamidol, iomeprol) - STANDARD
- **Iso-osmolar:** Non-ionic dimers (e.g., iodixanol) - For high-risk patients

**CONTRAINDICATIONS:**

**Absolute:**
- Previous anaphylaxis to iodinated contrast
- Untreated thyrotoxicosis (risk of thyroid storm)
- Pregnancy (CT with contrast - avoid unless essential)

**Relative:**
- Renal impairment (eGFR <30 mL/min/1.73 m²)
- Diabetes on metformin (metformin-associated lactic acidosis)
- Contrast allergy (mild/moderate reactions)
- Multiple myeloma (dehydration risk)

**CONTRAST-INDUCED NEPHROPATHY (CIN):**

**Risk factors:**
- Pre-existing renal impairment (eGFR <60 mL/min/1.73 m²)
- Diabetes mellitus
- Dehydration
- Advanced age (>75 years)
- High contrast volume (>100 mL)
- Repeat contrast exposure within 72 hours

**Definition:**
- Rise in serum creatinine >25% or >44 μmol/L within 48-72 hours
- Usually self-limiting (peaks at 3-5 days, resolves by 7-10 days)
- **Permanent dialysis:** RARE (<1%)

**Prevention:**
- **Hydration:** 1 mL/kg/hr IV normal saline for 6-12 hours pre- and post-contrast
- **eGFR >45:** No pre-hydration required
- **eGFR 30-45:** Consider pre-hydration (1 mL/kg 1 hour before, 4-6 hours after)
- **eGFR <30:** Discuss with referrer, consider alternative imaging
- **Minimise contrast volume:** Use lowest effective dose
- **Consider iso-osmolar contrast:** For high-risk patients
- **Avoid repeat contrast:** Wait at least 72 hours if possible

**METFORMIN PRECAUTIONS:**

**Risk:**
- Metformin-associated lactic acidosis (MALA)
- Risk increased if acute kidney injury from contrast

**Guidance:**
- **eGFR >60:** Continue metformin (no change)
- **eGFR 45-60:** Continue metformin (no change)
- **eGFR 30-45:** Continue metformin, monitor renal function
- **eGFR <30:** STOP metformin 48 hours before contrast
- **Re-start metformin:** 48 hours post-contrast if renal function stable

**CONTRAST ALLERGY:**

**Previous reaction grading:**

**Mild reactions:**
- Limited cutaneous urticaria
- Pruritus
- Flushing
- Nausea/vomiting (limited)

**Moderate reactions:**
- Diffuse urticaria
- Facial oedema
- Dyspnoea without stridor
- Mild hypotension (responds to fluids)

**Severe reactions:**
- Anaphylaxis (life-threatening)
- Laryngeal oedema (stridor, respiratory distress)
- Bronchospasm (wheeze, respiratory distress)
- Severe hypotension/shock
- Cardiac arrest

**PRE-MEDICATION PROTOCOL:**

**For patients with previous mild/moderate reaction:**
- **Prednisolone:** 50 mg orally at 13 hours, 7 hours, and 1 hour before contrast
- **Cetirizine (or alternative antihistamine):** 10 mg orally 1 hour before contrast
- **Consider:** Use low-osmolar non-ionic contrast (standard)
- **NOT indicated:** For patients with no previous reaction (prophylactic premedication)

**For patients with previous severe reaction (anaphylaxis):**
- **AVOID iodinated contrast** if possible
- Consider alternative imaging (USS, MRI)
- If contrast essential: Discuss with senior radiologist, consider premedication, use iso-osmolar contrast, have resuscitation equipment prepared

**Sources:** RCR Guidelines, ACR Manual on Contrast Media, ESUR Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Manual on Contrast Media", "ESUR Guidelines"]
            }
        )

    def _handle_radiation_safety(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Radiation safety and dose counselling"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**RADIATION SAFETY - DOSE COUNSELLING AND RISK ASSESSMENT**

**RADIATION DOSE COMPARISON:**

| Examination | Typical Effective Dose (mSv) | Equivalent Period of Natural Background Radiation |
|-------------|------------------------------|---------------------------------------------------|
| Chest X-ray (PA) | 0.02 | 3 days |
| Chest X-ray (PA + lateral) | 0.04 | 6 days |
| Abdominal X-ray | 0.7 | 4 months |
| CT Head | 2 | 1 year |
| CT Chest | 7 | 3 years |
| CT Abdomen/Pelvis | 10 | 4 years |
| CT Pulmonary Angiogram (CTPA) | 6 | 3 years |
| CT Coronary Angiogram | 6 | 3 years |
| PET-CT | 14 | 6 years |
| Barium Enema | 7 | 3 years |
| Mammogram (single view) | 0.4 | 2 months |
| Nuclear medicine (bone scan) | 6 | 3 years |
| Natural background radiation (annual) | 2.7 | 1 year |

**RISK ASSESSMENT:**

**Deterministic effects (threshold effects):**
- **Threshold:** Typically >100 mSv
- **Severity:** Increases with dose
- **Examples:** Skin erythema, cataract formation, fetal abnormalities

**Stochastic effects (random effects):**
- **No safe threshold:** Theoretical risk at any dose
- **Probability:** Increases with dose
- **Severity:** Not related to dose
- **Examples:** Cancer induction, genetic effects

**LIFETIME CANCER RISK:**

- **Background risk:** 1 in 3 people will develop cancer in their lifetime
- **Additional risk from 10 mSv:** Approximately 1 in 2000
- **For comparison:** Smoking 20 cigarettes/day increases risk by ~1 in 8

**RISK IN PREGNANCY:**

**Counselling points:**
- No diagnostic X-ray is absolutely contraindicated in pregnancy
- Benefit vs. risk assessment required
- Most diagnostic X-rays (especially outside abdomen/pelvis) have negligible fetal dose
- CT abdomen/pelvis has highest fetal dose (8-50 mGy)
- **Threshold for concern:** >100 mGy (no increased risk below this dose)

**PROTECTION MEASURES:**

**ALARA Principle (As Low As Reasonably Achievable):**
- Justification: Is the examination indicated?
- Optimisation: Use lowest dose that answers the clinical question
- Limitation: Limit scan range to area of interest

**Specific measures:**
- **Shielding:** Lead shielding for radiosensitive organs (e.g., gonads, breasts) where appropriate
- **Collimation:** Limit X-ray beam to area of interest
- **Low-dose protocols:** Use modality-specific low-dose protocols (e.g., CT pulmonary embolism protocol, low-dose CT for renal colic)
- **Alternative modalities:** Consider USS or MRI where appropriate (no ionising radiation)
- **Avoid repeat examinations:** Review previous imaging before requesting new studies

**PATIENT COUNSELLING:**

**Key points:**
- Explain the radiation dose in context (e.g., equivalent to X years of background radiation)
- Discuss the clinical indication (why the examination is needed)
- Discuss the risks of NOT imaging (missed diagnosis, delayed treatment)
- Reassure that the risk is low compared to the background risk
- Document the discussion in medical records

**Example script:**
"The CT scan of your abdomen involves a radiation dose equivalent to approximately 4 years of natural background radiation. The small additional risk from this radiation is approximately 1 in 2000, which is very low compared to your baseline lifetime cancer risk of 1 in 3. The scan is needed to [explain clinical indication], and the benefit of diagnosing [condition] outweighs this small risk."

**Sources:** RCR Guidelines, ICRP Recommendations, PHE/Public Health England""",
            confidence=0.88,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ICRP Recommendations", "PHE/Public Health England"]
            }
        )

    def _handle_modality_selection(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """Imaging modality selection for clinical scenarios"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**IMAGING MODALITY SELECTION**

**COMMON CLINICAL SCENARIOS:**

**1. PULMONARY EMBOLISM (PE):**
- **First-line:** CTPA (CT pulmonary angiogram)
  - High sensitivity and specificity
  - Low fetal dose in pregnancy
  - Alternative diagnoses visible (e.g., aortic dissection, pneumonia)
- **Alternative:** V/Q scan (especially if known PE, chest X-ray abnormal)
- **Chest X-ray:** Always perform first (to exclude alternative diagnoses)

**2. HEAD INJURY:**
- **First-line:** CT head (non-contrast)
  - Rapid assessment for intracranial bleed
  - Indications: GCS <15 at 2 hours, coagulopathy, focal neurology, penetrating injury
- **Indication for MRI:** Suspected diffuse axonal injury, posterior fossa lesion (CT limited by bone artefact)

**3. STROKE (HYPERACUTE):**
- **First-line:** Non-contrast CT head (exclude haemorrhage)
- **CTA:** If candidate for thrombolysis/thrombectomy
- **CT Perfusion:** If thrombectomy candidate >6 hours (penumbra assessment)
- **MRI:** Not first-line in hyperacute period (too slow)

**4. ACUTE APPENDICITIS:**
- **Pregnant:** MRI (no ionising radiation)
- **Paediatric:** Ultrasound (no ionising radiation)
- **Adult:** CT abdomen/pelvis (high sensitivity and specificity)
- **Alternative:** MRI (if available, avoids radiation)

**5. RENAL COLIC:**
- **First-line:** CT KUB (CT kidneys, ureters, bladder)
  - Low-dose protocol (radiation dose minimised)
  - High sensitivity for stones
- **Alternative:** Ultrasound (pregnancy, recurrent stones, radiation concern)

**6. CHEST PAIN (CARDIAC):**
- **First-line:** Chest X-ray (exclude pneumothorax, pneumonia, widened mediastinum)
- **Coronary artery assessment:** CT coronary angiogram (if stable, intermediate risk)
- **Aortic dissection:** CT aortogram (CT angiography of entire aorta)

**7. ABDOMINAL PAIN:**
- **General:** CT abdomen/pelvis with IV contrast
- **Pancreatitis:** CT abdomen with IV contrast (72 hours after onset for necrosis assessment)
- **Diverticulitis:** CT abdomen/pelvis with IV contrast (oral and rectal contrast optional)
- **Biliary:** Ultrasound (gallstones, biliary dilation)

**8. BONE FRACTURE:**
- **First-line:** Plain X-ray (2 views)
- **Indication for CT:** Complex fracture, surgical planning, spinal fracture
- **Indication for MRI:** Occult fracture (e.g., scaphoid), stress fracture, soft tissue injury

**9. JOINT PAIN:**
- **First-line:** Plain X-ray
- **Soft tissue/ligament:** MRI (e.g., meniscal tear, ACL rupture, rotator cuff tear)
- **Loose body:** CT (better than MRI for intra-articular loose bodies)

**10. LIVER LESION:**
- **Characterisation:** MRI liver (specific sequences for liver lesions)
- **Alternative:** CT triphasic liver (arterial, portal venous, delayed phases)
- **Surveillance:** Ultrasound (e.g., cirrhosis surveillance for HCC)

**PREGNANCY-SPECIFIC CONSIDERATIONS:**

- **Avoid ionising radiation** where possible
- **First-line:** Ultrasound or MRI
- **If CT required:** Use lowest dose protocol, limit scan range, document counselling discussion

**PAEDIATRIC-SPECIFIC CONSIDERATIONS:**

- **Radiation sensitivity:** Children are more radiosensitive than adults
- **Longer life expectancy:** More time for radiation-induced cancer to develop
- **ALARA principle:** Use lowest dose possible, consider alternative modalities (USS, MRI)

**Sources:** RCR Guidelines, ACR Appropriateness Criteria, NICE Guidelines""",
            confidence=0.90,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Appropriateness Criteria", "NICE Guidelines"]
            }
        )

    def _handle_general_radiology(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """General radiology consultation and imaging guidance"""

        return DomainQueryResult(
            domain_name="radiology",
            answer="""**RADIOLOGY AND MEDICAL IMAGING**

Radiology is a medical specialty that uses medical imaging (X-ray, CT, MRI, ultrasound, nuclear medicine) to diagnose and treat disease.

**IMAGING MODALITIES:**

**Plain Radiography (X-ray):**
- **Uses:** Ionising radiation to create 2D images
- **Common examinations:** Chest X-ray, skeletal X-ray, abdominal X-ray
- **Advantages:** Widely available, quick, inexpensive
- **Disadvantages:** Limited soft tissue contrast, 2D projection (overlapping structures)
- **Radiation dose:** Low (e.g., chest X-ray: 0.02 mSv)

**Computed Tomography (CT):**
- **Uses:** X-rays from multiple angles to create 3D cross-sectional images
- **Common examinations:** CT head, CT chest, CT abdomen/pelvis, CT angiography
- **Advantages:** Rapid, excellent spatial resolution, widely available
- **Disadvantages:** Higher radiation dose, limited soft tissue contrast compared to MRI
- **Radiation dose:** Moderate to high (e.g., CT abdomen/pelvis: 10 mSv)

**Magnetic Resonance Imaging (MRI):**
- **Uses:** Magnetic fields and radio waves (no ionising radiation)
- **Common examinations:** MRI brain, MRI spine, MRI joints, MRI liver
- **Advantages:** Excellent soft tissue contrast, no ionising radiation
- **Disadvantages:** Expensive, slower, not universally available, contraindicated in some implants (e.g., pacemakers)
- **Contrast:** Gadolinium-based (different safety profile from iodinated contrast)

**Ultrasound (US):**
- **Uses:** High-frequency sound waves (no ionising radiation)
- **Common examinations:** Abdominal ultrasound, obstetric ultrasound, musculoskeletal ultrasound
- **Advantages:** No ionising radiation, real-time imaging, bedside availability
- **Disadvantages:** Operator-dependent, limited by bone/air, lower resolution than CT/MRI
- **Doppler:** Assesses blood flow (e.g., deep vein thrombosis, arterial stenosis)

**Nuclear Medicine:**
- **Uses:** Radioactive isotopes (gamma camera) to assess physiological function
- **Common examinations:** Bone scan, V/Q scan, PET-CT
- **Advantages:** Functional imaging, detects disease before structural changes
- **Disadvantages:** Radiation dose, limited spatial resolution, longer scanning time
- **PET-CT:** Combines metabolic (FDG-PET) and anatomical (CT) imaging

**INTERVENTIONAL RADIOLOGY:**
- **Uses:** Imaging guidance (fluoroscopy, CT, ultrasound) for minimally invasive procedures
- **Common procedures:** Biopsy, drainage, angioplasty, embolisation, stent insertion
- **Advantages:** Minimally invasive, reduced recovery time compared to surgery
- **Disadvantages:** Radiation exposure (fluoroscopy), contrast use, risk of bleeding/infection

**COMMON CLINICAL QUESTIONS:**

- "What's the best imaging for [condition]?" → Consider indication, patient factors (age, pregnancy, renal function), modality availability
- "What's the radiation dose?" → Provide context (equivalent to X years of background radiation)
- "Is contrast safe?" → Assess renal function, contrast allergy, pregnancy status
- "Is it safe in pregnancy?" → Consider benefit vs. risk, use alternative modalities (USS, MRI) where possible
- "How do I interpret this image?" → Provide systematic approach and key findings

**Sources:** RCR Guidelines, ACR Manual on Contrast Media, ESR Guidelines""",
            confidence=0.85,
            metadata={
                "urgency": "non-urgent",
                "specialty": "radiology",
                "sources": ["RCR Guidelines", "ACR Manual on Contrast Media", "ESR Guidelines"]
            }
        )

    def _handle_dicom_analysis(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Handle DICOM file analysis requests

        Supports:
        - DICOM file loading and metadata extraction
        - Pixel data analysis
        - Modality-specific findings
        - Privacy-preserving local processing
        """
        if not DICOM_AVAILABLE:
            return DomainQueryResult(
                domain_name="radiology",
                answer="""**DICOM Analysis - Dependencies Not Available**

To enable DICOM file analysis, the following dependencies are required:

```
pip install pydicom numpy
```

After installing dependencies, restart the system to enable DICOM processing.

**DICOM Capabilities** (when dependencies installed):
- DICOM file loading (.dcm files)
- Metadata extraction (patient info, study info, image characteristics)
- Pixel data analysis (statistics, window/level)
- Modality-specific findings (CT, X-ray, MRI, Ultrasound)
- Privacy-preserving local processing (no external data transmission)

**Privacy Commitment:**
- All DICOM files processed locally
- No medical images transmitted externally
- Patient data remains on local system
- PHI (Protected Health Information) never leaves the local environment

**Sources:** RCR, ACR, ESR Guidelines""",
                confidence=0.95,
                metadata={
                    "category": "dicom_analysis",
                    "dependencies_required": ["pydicom", "numpy"],
                    "sources": ["RCR", "ACR", "ESR"]
                }
            )

        # Extract file path from query or context
        filepath = None
        query_lower = query.lower()

        # Try to get filepath from query
        if ".dcm" in query_lower:
            # Extract file path from query
            words = query.split()
            for i, word in enumerate(words):
                if ".dcm" in word.lower():
                    filepath = word.strip('"\'')
                    break
                elif i > 0 and words[i-1].lower() in ["file", "analyze", "load", "read"]:
                    filepath = word.strip('"\'')
                    break

        # Try to get filepath from context
        if not filepath and context:
            filepath = context.get("dicom_file", context.get("filepath", context.get("file")))

        if not filepath:
            return DomainQueryResult(
                domain_name="radiology",
                answer="""**DICOM Analysis - File Path Required**

Please provide the path to the DICOM file you wish to analyze.

**Usage:**
- "Analyze DICOM file /path/to/file.dcm"
- "Load DICOM /path/to/file.dcm"
- Provide file path in context: `{"dicom_file": "/path/to/file.dcm"}`

**Supported File Types:**
- DICOM files (.dcm)
- DICOM series (directories containing multiple .dcm files)

**DICOM Analysis Features:**
- ✓ Metadata extraction (patient info, study details, image characteristics)
- ✓ Pixel data analysis (statistics, window/level adjustments)
- ✓ Modality-specific findings (CT, X-ray, MRI, Ultrasound)
- ✓ Privacy-preserving local processing
- ✓ Anonymized output (default)

**Privacy Notice:**
All DICOM processing occurs locally on your system. No medical images or patient data are transmitted to external services.

**Sources:** RCR, ACR, ESR Guidelines""",
                confidence=0.90,
                metadata={
                    "category": "dicom_analysis",
                    "requires_filepath": True,
                    "sources": ["RCR", "ACR", "ESR"]
                }
            )

        # Process the DICOM file
        try:
            processor = create_dicom_processor(anonymize=True)
            result = processor.process_dicom_file(filepath, extract_pixels=True)

            if result.success:
                # Generate comprehensive report
                report_lines = []
                report_lines.append("**DICOM File Analysis Report**\n")
                report_lines.append("=" * 70)
                report_lines.append("")

                # Metadata section
                if result.metadata:
                    report_lines.append("**METADATA:**")
                    metadata = result.metadata
                    if metadata.modality:
                        report_lines.append(f"Modality: {metadata.modality}")
                    if metadata.body_part:
                        report_lines.append(f"Body Part: {metadata.body_part}")
                    if metadata.study_date:
                        report_lines.append(f"Study Date: {metadata.study_date}")
                    if metadata.view_position:
                        report_lines.append(f"View Position: {metadata.view_position}")
                    if metadata.series_description:
                        report_lines.append(f"Series Description: {metadata.series_description}")
                    report_lines.append("")

                # Image characteristics
                if result.image_shape:
                    report_lines.append("**IMAGE CHARACTERISTICS:**")
                    report_lines.append(f"Image Shape: {result.image_shape}")
                    if result.pixel_array_stats:
                        stats = result.pixel_array_stats
                        report_lines.append(f"Pixel Value Range: {stats['min']:.2f} to {stats['max']:.2f}")
                        report_lines.append(f"Mean: {stats['mean']:.2f}")
                        report_lines.append(f"Std Deviation: {stats['std']:.2f}")
                    report_lines.append("")

                # Findings
                if result.findings:
                    report_lines.append("**FINDINGS:**")
                    for finding in result.findings:
                        report_lines.append(f"• {finding}")
                    report_lines.append("")

                # Warnings
                if result.warnings:
                    report_lines.append("**WARNINGS:**")
                    for warning in result.warnings:
                        report_lines.append(f"⚠ {warning}")
                    report_lines.append("")

                # Privacy notice
                report_lines.append("**PRIVACY NOTICE:**")
                report_lines.append("All processing performed locally. No medical images or")
                report_lines.append("patient data transmitted externally.")
                report_lines.append("")
                report_lines.append("**Sources:** RCR, ACR, ESR Guidelines")

                answer = "\n".join(report_lines)

                return DomainQueryResult(
                    domain_name="radiology",
                    answer=answer,
                    confidence=0.95,
                    metadata={
                        "category": "dicom_analysis",
                        "file_processed": filepath,
                        "modality": result.metadata.modality if result.metadata else None,
                        "body_part": result.metadata.body_part if result.metadata else None,
                        "image_shape": result.image_shape,
                        "findings_count": len(result.findings),
                        "warnings_count": len(result.warnings),
                        "sources": ["RCR", "ACR", "ESR Guidelines"],
                        "local_processing": True,
                        "anonymized": True
                    }
                )
            else:
                return DomainQueryResult(
                    domain_name="radiology",
                    answer=f"""**DICOM Analysis - Processing Failed**

Error: {result.error_message}

**Possible Issues:**
- File not found: Check the file path is correct
- Invalid DICOM file: File may be corrupted or not a valid DICOM format
- Unsupported format: Some DICOM variants may not be supported

**Troubleshooting:**
1. Verify file path: `{filepath}`
2. Check file is a valid DICOM file (.dcm extension)
3. Ensure file is not corrupted
4. Try opening with a standard DICOM viewer to verify file integrity

**Sources:** RCR, ACR, ESR Guidelines""",
                    confidence=0.85,
                    metadata={
                        "category": "dicom_analysis",
                        "error": result.error_message,
                        "filepath": filepath,
                        "sources": ["RCR", "ACR", "ESR"]
                    }
                )

        except Exception as e:
            return DomainQueryResult(
                domain_name="radiology",
                answer=f"""**DICOM Analysis - System Error**

An error occurred while processing the DICOM file:

Error: {str(e)}

**This may indicate:**
- Missing dependencies (pydicom, numpy)
- Insufficient memory for large DICOM files
- File access permissions

**To install dependencies:**
```
pip install pydicom numpy
```

**Sources:** RCR, ACR, ESR Guidelines""",
                confidence=0.75,
                metadata={
                    "category": "dicom_analysis",
                    "error": str(e),
                    "sources": ["RCR", "ACR", "ESR"]
                }
            )


def create_radiology_domain():
    """Factory function for Radiology Domain"""
    return RadiologyDomain()
