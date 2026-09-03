"""
Cardiothoracic Surgery Domain Module for GPDISC

Comprehensive cardiothoracic surgery consultation covering cardiac surgery,
thoracic surgery, and cardiothoracic emergencies.

Evidence-based guidelines from:
- Society for Cardiothoracic Surgery (SCTS)
- European Association for Cardio-Thoracic Surgery (EACTS)
- National Institute for Health and Care Excellence (NICE)
- British Thoracic Society (BTS)

Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class CardiothoracicSurgeryDomain(BaseDomainModule):
    """
    Cardiothoracic Surgery specialty domain for GPDISC

    Covers cardiac surgery, thoracic surgery, and cardiothoracic emergencies.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="cardiothoracic_surgery",
            version="1.0.0",
            dependencies=[],
            description="Cardiothoracic surgery: cardiac, thoracic, and oesophageal surgery",
            keywords=[
                # Cardiac surgery
                "cardiac surgery", "heart surgery", "heart surgeon", "cardiac surgeon",
                "coronary artery bypass", "cabg", "bypass surgery", "heart bypass",
                "valve surgery", "valve replacement", "valve repair", "aortic valve", "mitral valve",
                "aortic valve replacement", "avr", "mitral valve repair", "mitral valve replacement",
                "heart valve", "valve disease", "aortic stenosis", "mitral regurgitation",
                "aortic surgery", "aortic root", "aortic dissection", "aortic aneurysm",
                "arrhythmia surgery", "af ablation", "atrial fibrillation surgery", "maze procedure",
                "cardiac tumour", "atrial myxoma", "heart tumour",
                "pericardial surgery", "pericardial effusion", "pericardiectomy",
                "transplant", "heart transplant", "lung transplant", "heart-lung transplant",
                "lvad", "left ventricular assist device", "ventricular assist device", "vad",
                "ecmo", "extracorporeal membrane oxygenation",

                # Thoracic surgery
                "thoracic surgery", "chest surgery", "lung surgery", "lung surgeon",
                "lung cancer", "lung tumour", "lung nodule", "pulmonary nodule",
                "lobectomy", "wedge resection", "pneumonectomy", "segmentectomy",
                "lung resection", "lung volume reduction", "lvrs",
                "pleural effusion", "pleural tap", "chest drain", "thoracocentesis",
                "pleurodesis", "pleural biopsy", "pleural disease",
                "pneumothorax", "collapsed lung", "chest tube", "tension pneumothorax",
                "empyema", "infected pleural fluid", "rib resection", "decortication",
                "chest wall", "rib tumour", "chest wall deformity", "pectus", "pectus excavatum",
                "mediastinum", "mediastinal mass", "mediastinal tumour", "thymoma", "thymus",
                "oesophageal surgery", "esophageal surgery", "oesophagectomy", "esophagectomy",
                "oesophageal cancer", "esophageal cancer", "achalasia", "oesophageal diverticulum",
                "diaphragmatic", "diaphragm", "hiatus hernia", "para-oesophageal hernia",

                # Cardiothoracic emergencies
                "cardiac trauma", "penetrating cardiac injury", "stab wound heart", "gunshot heart",
                "aortic dissection", "type a dissection", "type b dissection",
                "cardiac tamponade", "pericardial tamponade", "tamponade",
                "traumatic pneumothorax", "tension pneumothorax", "haemothorax", "chest trauma",
                "flail chest", "rib fracture", "sternal fracture",

                # Preoperative/postoperative
                "sternotomy", "thoracotomy", "video assisted thoracoscopic", "vats",
                "robotic surgery", "da vinci", "minimally invasive cardiac",
                "sternotomy infection", "sternal wound", "sternal dehiscence",
                "post cardiac surgery", "after heart surgery", "cabg recovery",
                "sternal precautions", "sternal care", "breastbone precautions",

                # General cardiothoracic
                "cardiothoracic", "cardiothoracic surgeon", "cts", "heart and lung"
            ],
            capabilities=[
                "cardiac_surgery_consultation",
                "coronary_revascularization",
                "valve_surgery_assessment",
                "aortic_surgery_management",
                "thoracic_surgery_consultation",
                "lung_cancer_surgery",
                "pleural_disease_management",
                "oesophageal_surgery_consultation",
                "cardiothoracic_emergency_management",
                "preoperative_assessment"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process cardiothoracic surgery query

        Routes to appropriate handler based on query content.
        """
        query_lower = query.lower()

        # CARDIOTHORACIC EMERGENCIES - Highest priority
        if any(term in query_lower for term in [
            "cardiac tamponade", "pericardial tamponade", "tamponade",
            "penetrating cardiac injury", "cardiac trauma", "stab wound chest", "gunshot chest",
            "aortic dissection", "type a dissection", "acute dissection",
            "tension pneumothorax", "traumatic pneumothorax"
        ]):
            return self._handle_cardiothoracic_emergency(query, context)

        # Cardiac surgery - CABG
        elif any(term in query_lower for term in [
            "cabg", "coronary artery bypass", "bypass surgery", "heart bypass",
            "coronary graft", "coronary surgery"
        ]):
            return self._handle_cabg_query(query, context)

        # Valve surgery
        elif any(term in query_lower for term in [
            "valve surgery", "valve replacement", "valve repair", "aortic valve",
            "mitral valve", "aortic stenosis", "mitral regurgitation", "heart valve"
        ]):
            return self._handle_valve_surgery_query(query, context)

        # Aortic surgery
        elif any(term in query_lower for term in [
            "aortic surgery", "aortic root", "ascending aorta", "aortic arch",
            "bentall", "david", "aortic valve sparing"
        ]):
            return self._handle_aortic_surgery_query(query, context)

        # Lung cancer/thoracic surgery
        elif any(term in query_lower for term in [
            "lung cancer", "lung tumour", "lung nodule", "pulmonary nodule",
            "lobectomy", "lung resection", "wedge resection", "pneumonectomy",
            "lung surgery", "thoracic surgery"
        ]):
            return self._handle_thoracic_surgery_query(query, context)

        # Pleural disease
        elif any(term in query_lower for term in [
            "pleural effusion", "pleural tap", "chest drain", "thoracocentesis",
            "pneumothorax", "collapsed lung", "empyema", "pleurodesis"
        ]):
            return self._handle_pleural_disease_query(query, context)

        # Oesophageal surgery
        elif any(term in query_lower for term in [
            "oesophageal surgery", "esophageal surgery", "oesophagectomy",
            "oesophageal cancer", "achalasia", "hiatus hernia"
        ]):
            return self._handle_oesophageal_surgery_query(query, context)

        # Post cardiac surgery
        elif any(term in query_lower for term in [
            "after heart surgery", "post cabg", "postoperative cardiac",
            "sternotomy recovery", "sternal care", "sternal precautions"
        ]):
            return self._handle_post_cardiac_surgery_query(query, context)

        # LVAD/VAD/ECMO
        elif any(term in query_lower for term in [
            "lvad", "ventricular assist", "vad", "ecmo", "heart pump",
            "artificial heart", "mechanical support"
        ]):
            return self._handle_mechanical_support_query(query, context)

        # General cardiothoracic query
        else:
            return self._handle_general_cardiothoracic_query(query, context)

    def _handle_cardiothoracic_emergency(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle cardiothoracic emergencies requiring urgent intervention"""
        query_lower = query.lower()

        # Cardiac tamponade
        if any(term in query_lower for term in [
            "cardiac tamponade", "pericardial tamponade", "tamponade"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**CARDIAC TAMPONADE - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent echocardiography** to confirm
- **Pericardiocentesis** if haemodynamically unstable
- **Cardiothoracic surgical involvement**

**CLINICAL PRESENTATION (BECK'S TRIAD):**
- **Hypotension**
- **Jugular venous distension (JVD)**
- **Muffled heart sounds**

**ADDITIONAL SIGNS:**
- Tachycardia
- Pulsus paradoxus (>10 mmHg drop in SBP on inspiration)
- Equalized central venous pressure
- Distant heart sounds
- Kussmaul's sign (rise in JVP on inspiration)
- Electrical alternans (on ECG)

**CAUSES:**
- **Trauma** (penetrating - stab/gunshot)
- **Post-cardiac surgery** (early tamponade)
- **Aortic dissection**
- **Pericarditis** (viral, bacterial, TB)
- **Malignancy** (lung cancer, mesothelioma, metastatic)
- **Renal failure** (uraemic pericarditis)
- **Post-MI** (Dressler's syndrome, free wall rupture)

**IMMEDIATE MANAGEMENT:**

**1. Resuscitation**
- IV fluids (crystalloid/colloid bolus)
- Avoid excessive fluids (can worsen tamponade)
- Inotropes if needed (noradrenaline)
- Oxygen if hypoxic

**2. Pericardiocentesis**
- **Subxiphoid approach** under ECG/echo guidance
- Aspirate as much fluid as possible
- Send fluid for analysis (cell count, culture, cytology)
- Leave drain in place

**3. Surgical Drainage**
- **Subxiphoid pericardial window**
- **Thoracotomy/pericardiotomy** if penetrating trauma
- Indicated if:
  - Pericardiocentesis unsuccessful
  - Reaccumulation after aspiration
  - Trauma (blood in pericardium)
  - Need for biopsy (malignancy)

**DEFINITIVE MANAGEMENT:**
- Treat underlying cause
- Surgical window if recurrent
- Pericardiectomy for constrictive pericarditis

**PROGNOSIS:**
- Mortality high if untreated
- Better outcomes with prompt intervention
- Recurrence common if underlying cause not treated

**Evidence:** BTS Guidelines, ESC Guidelines""",
                confidence=0.97,
                reasoning_trace=[
                    "Identified cardiac tamponade - surgical emergency",
                    "Applied Beck's triad clinical assessment",
                    "Prioritized pericardiocentesis and surgical drainage"
                ],
                capabilities_used=["cardiothoracic_emergency_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "cardiac_tamponade",
                    "intervention": "pericardiocentesis_or_surgery"
                }
            )

        # Penetrating cardiac injury
        elif any(term in query_lower for term in [
            "penetrating cardiac injury", "cardiac trauma", "stab wound chest", "gunshot chest"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**PENETRATING CARDIAC INJURY - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Activate major trauma protocol**
- **Immediate transfer to operating theatre**
- **Left anterolateral thoracotomy** if arrested

**CLINICAL PRESENTATION:**
- **Precordial wound** (stab/gunshot)
- **Cardiac tamponade** (muffled heart sounds, JVD, hypotension)
- **Haemorrhagic shock**
- **Cardiac arrest** (may be PEA or asystole)

**IMMEDIATE MANAGEMENT:**

**1. Emergency Department Thoracotomy (EDT)**
- **Indicated if:**
  - Cardiac arrest with precordial wound
  - Vital signs lost in ED
  - Penetrating chest trauma
- **NOT indicated if:**
  - Blunt trauma with no signs of life >10 minutes
  - Asystole without tamponade

**2. Resuscitative Thoracotomy (LEFT ANTEROLATERAL)**
- Incision 4th/5th intercostal space
- Open pericardium vertically (avoid phrenic nerve)
- Evacuate clot/blood
- **Control cardiac wound**
  - Finger occlusion
  - Skin stapler or Foley catheter (temporary)
  - Prolene 3/0 or 4/0 suture (definitive)
- **Internal cardiac massage** (if arrested)
- **Cross-clamp aorta** (if no BP with massage)

**3. Definitive Management in OT**
- Median sternotomy or thoracotomy
- Repair cardiac injury
- Prosthetic patch if large defect
- Coronary artery bypass if injured

**SPECIFIC INJURIES:**
- **Right ventricle** (40% - most common)
- **Left ventricle** (40%)
- **Right atrium** (15%)
- **Left atrium** (5%)
- **Coronary arteries** (rare but serious)

**SURVIVAL:**
- Overall: 10-30%
- With vital signs on arrival: 50-70%
- With cardiac arrest: <10%

**EVIDENCE:** EAST Guidelines, RCS Guidelines""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified penetrating cardiac injury - surgical emergency",
                    "Applied emergency thoracotomy protocol",
                    "Prioritized immediate surgical intervention"
                ],
                capabilities_used=["cardiothoracic_emergency_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "penetrating_cardiac_injury",
                    "intervention": "emergency_thoracotomy"
                }
            )

        # Aortic dissection
        elif any(term in query_lower for term in [
            "aortic dissection", "type a dissection", "acute dissection"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**ACUTE AORTIC DISSECTION - CARDIOTHORACIC EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent CT angiogram** (whole aorta)
- **Type A dissection: EMERGENCY SURGERY**
- **Type B dissection: medical management or TEVAR**

**CLASSIFICATION:**

**Stanford Classification:**
- **Type A:** Ascending aorta involved → Surgical emergency
- **Type B:** Descending aorta only → Medical/TEVAR

**DeBakey Classification:**
- **Type I:** Ascending + descending aorta
- **Type II:** Ascending aorta only
- **Type III:** Descending aorta only

**CLINICAL PRESENTATION:**
- **Tearing chest pain** radiating to back (Type A)
- **Tearing back/abdominal pain** (Type B)
- Pulse deficits or blood pressure discrepancies
- Syncope, cardiac tamponade (Type A)
- Stroke symptoms if carotid involved
- Paraplegia if spinal cord involved (Type B)

**IMMEDIATE MANAGEMENT:**

**1. Analgesia**
- IV opioids (morphine/fentanyl)
- Reduce sympathetic drive

**2. Blood Pressure Control**
- Target SBP 100-120 mmHg
- IV labetalol (first-line):
  - 20mg IV over 2 minutes
  - Repeat 20-80mg q10min to max 300mg
  - Then infusion 1-2 mg/min
- Alternative: Esmolol infusion
- Add nicardipine or nitroprusside if needed

**3. Heart Rate Control**
- Target HR 60-80 bpm
- Beta-blocker first-line (labetalol/esmolol)
- **AVOID beta-blocker** if aortic regurgitation with acute heart failure

**4. CT Angiography**
- Gold standard for diagnosis
- Shows true and false lumen, intimal flap
- Identifies entry tear, branch vessel involvement

**TREATMENT:**

**Type A Dissection (Ascending Aorta):**
- **EMERGENCY SURGERY**
- **Bentall procedure** (if aortic root dilated)
  - Replace aortic root + valve
  - Re-attach coronary arteries
- **David procedure** (valve-sparing)
  - Replace aortic root, spare native valve
  - For patients with normal valve
- **Supracommissural graft** (if root normal)
  - Replace ascending aorta only
- **Mortality:** 15-30% despite surgery

**Type B Dissection (Descending Aorta):**
- **Medical management first-line**
  - Antihypertensives, beta-blockers
  - Analgesia
- **TEVAR** (thoracic EVAR) if:
  - Malperfusion (renal, mesenteric, limb)
  - Rupture or impending rupture
  - Persistent pain despite medical management
  - Refractory hypertension

**PROGNOSIS:**
- **Type A:** 50% mortality without surgery, 15-30% with surgery
- **Type B:** 10-20% mortality with medical management
- Long-term: surveillance CT required (3, 6, 12 months, then annually)

**EVIDENCE:** ESC 2023 Guidelines, EACTS Guidelines""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified aortic dissection - cardiothoracic emergency",
                    "Applied Stanford classification",
                    "Type A requires emergency surgery, Type B medical/TEVAR"
                ],
                capabilities_used=["cardiothoracic_emergency_management", "aortic_surgery_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "aortic_dissection",
                    "classification": "stanford",
                    "intervention": "emergency_surgery_type_a"
                }
            )

        # Tension pneumothorax
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**TENSION PNEUMOTHORAX - RESUSCITATION EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **DO NOT WAIT FOR CXR**
- **IMMEDIATE NEEDLE DECOMPRESSION**
- **Followed by chest drain**

**CLINICAL PRESENTATION:**
- **Severe respiratory distress**
- **Tachypnoea, tachycardia**
- **Hypotension** (cardiac compromise)
- **Tracheal deviation** AWAY from affected side (late sign)
- **Decreased breath sounds** on affected side
- **Hyperresonant** percussion on affected side
- **Distended neck veins** (JVD)

**IMMEDIATE MANAGEMENT:**

**1. Needle Decompression**
- **Second intercostal space, midclavicular line** (affected side)
- **14G or 16G cannula**
- Insert perpendicular to chest wall, over top of rib
- Listen for rush of air (hissing)
- If no rush, consider malposition or diagnosis incorrect

**2. Chest Drain**
- **Insert after needle decompression**
- **5th intercostal space, anterior axillary line**
- **Size 12-16Fr** (smaller for trauma, larger for spontaneous pneumothorax)
- Connect to underwater seal drainage
- Aim for suction -20 cmH2O

**3. Supportive Care**
- High-flow oxygen
- IV fluids if hypotensive
- Analgesia
- Monitor for re-expansion pulmonary oedema

**CAUSES:**
- **Trauma** (blunt or penetrating)
- **Iatrogenic** (central line, pleural tap, mechanical ventilation)
- **Spontaneous** (underlying lung disease)
- **Barotrauma** (mechanical ventilation)

**COMPLICATIONS:**
- Re-expansion pulmonary oedema
- Bleeding (chest wall vessel injury)
- Infection
- Recurrence

**DEFINITIVE MANAGEMENT:**
- Treat underlying cause
- VATS pleurodesis for recurrent spontaneous pneumothorax
- Thoracotomy for trauma with ongoing bleeding/air leak

**Evidence:** BTS Pleural Disease Guidelines, ATLS Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified tension pneumothorax - resuscitation emergency",
                    "Prioritized immediate needle decompression",
                    "Followed by chest drain insertion"
                ],
                capabilities_used=["cardiothoracic_emergency_management", "pleural_disease_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "tension_pneumothorax",
                    "intervention": "needle_decompression_chest_drain"
                }
            )

    def _handle_cabg_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle CABG queries"""
        query_lower = query.lower()

        # CABG indications
        if any(term in query_lower for term in [
            "indication", "when", "candidate", "need", "qualify",
            "guidelines", "recommend"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**CORONARY ARTERY BYPASS GRAFTING (CABG) - INDICATIONS**

**NICE GUIDELINES (NG185) RECOMMENDATIONS:**

**CABG is FIRST-LINE for:**

**1. Left Main Stem Disease**
- Stenosis >50%
- Reduces mortality compared to medical therapy

**2. Triple Vessel Disease**
- Especially with diabetes
- CABG superior to PCI in long-term survival

**3. Double Vessel Disease**
- With proximal LAD stenosis
- With diabetes or reduced LV function

**4. Reduced Left Ventricular Function**
- LV ejection fraction <35%
- Viability demonstrated (stress echo, MRI, PET)
- CABG improves survival if viable myocardium

**5. Failed PCI**
- Stent thrombosis, restenosis
- Complex anatomy not suitable for PCI

**PCI PREFERRED over CABG for:**
- Single vessel disease (except proximal LAD)
- Low SYNTAX score (<22)
- High surgical risk (frailty, comorbidities)
- Patient preference for less invasive option

**SHARED DECISION MAKING:**
- Discuss benefits/risks of CABG vs PCI
- Heart team approach (cardiologist + cardiac surgeon)
- Consider patient values, preferences
- Consider life expectancy, comorbidities

**BENEFITS OF CABG:**
- Better long-term survival (especially in diabetes, multivessel disease)
- Lower repeat revascularization rate
- More complete revascularization
- No antiplatelet beyond aspirin (vs 12 months DAPT for PCI)

**RISKS OF CABG:**
- Perioperative mortality: 1-2% (overall)
- Stroke: 1-2%
- Wound infection: 1-3% (higher in diabetes, obesity)
- Atrial fibrillation: 30%
- Renal dysfunction: 5-10%
- Blood transfusion: 30-50%

**EVIDENCE:** NICE NG185 (2023), ESC Guidelines, SYNTAX Trial""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified CABG indications query",
                    "Applied NICE NG185 recommendations",
                    "Considered Heart Team approach"
                ],
                capabilities_used=["cardiac_surgery_consultation", "coronary_revascularization"],
                metadata={
                    "topic": "cabg_indications",
                    "guideline": "nice_ng185"
                }
            )

        # CABG procedure details
        elif any(term in query_lower for term in [
            "procedure", "how is", "surgery", "graft", "conduit",
            "mammary artery", "saphenous vein"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**CABG PROCEDURE DETAILS**

**CONDUITS (GRAFTS):**

**1. Internal Mammary Arteries (IMA) - BEST CONDUIT**
- **Left IMA (LIMA) to LAD** - gold standard
- 10-year patency: >90%
- **Right IMA (RIMA)** - use for second target
- Arterial conduit, resistant to atherosclerosis

**2. Radial Artery**
- Good second or third arterial conduit
- 10-year patency: 80-90%
- Must harvest carefully to prevent hand ischaemia
- Preop Allen's test mandatory

**3. Saphenous Vein Grafts (SVG)**
- Most commonly used (after IMA)
- 10-year patency: 50-60%
- Harvest from leg (open or endoscopic)
- Reserve for less critical targets

**PROCEDURE:**

**1. Anaesthesia**
- General anaesthetic
- Arterial line (invasive BP monitoring)
- Central venous line
- Transoesophageal echo (TOE)

**2. Cardiopulmonary Bypass (CPB)**
- Most CABGs done "on-pump"
- Heart stopped with cardioplegia
- Machine oxygenates and circulates blood
- Allows precise anastomosis

**3. Off-Pump CABG (OPCAB)**
- Surgery on beating heart
- Stabilization device used
- No CPB required
- Selected cases (high risk for CPB)
- Similar outcomes to on-pump in selected patients

**4. Anastomosis**
- Proximal anastomosis (graft to aorta)
- Distal anastomosis (graft to coronary artery)
- 7/0 or 8/0 prolene suture

**5. Sternotomy Closure**
- Steel wires to approximate sternum
- Dissolvable sutures for skin

**POSTOPERATIVE CARE:**
- ICU/HDU for 24-48 hours
- Chest drains removed day 1-2
- Epidural or PCA for pain
- Early mobilization (day 2-3)
- Discharge day 5-7 (if uncomplicated)

**EVIDENCE:** EACTS Guidelines, STS Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified CABG procedure query",
                    "Explained conduit options (IMA > radial > vein)",
                    "Outlined on-pump vs off-pump techniques"
                ],
                capabilities_used=["cardiac_surgery_consultation", "coronary_revascularization"],
                metadata={
                    "topic": "cabg_procedure",
                    "guideline": "eacts"
                }
            )

        # CABG recovery
        elif any(term in query_lower for term in [
            "recovery", "postoperative", "after surgery", "post cabg",
            "how long", "back to normal"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**CABG RECOVERY**

**HOSPITAL STAY:**
- **ICU/HDU:** 1-2 nights
- **Ward:** 3-5 nights
- **Total:** 5-7 days (uncomplicated)

**IMMEDIATE POSTOPERATIVE (FIRST 24-48 HOURS):**

**1. Wound Care**
- **Sternal precautions** (see below)
- Leg wounds (if vein harvest)
- Keep wounds clean and dry
- Dressings removed day 5-7

**2. Pain Management**
- PCA or epidural initially
- Oral analgesia (paracetamol, opioids)
- NSAIDs generally avoided (bleeding risk, renal)

**3. Breathing Exercises**
- Incentive spirometry
- Deep breathing and coughing
- Pillow to support sternum

**4. Mobilization**
- Sit out of bed day 1
- Walk with assistance day 2-3
- Progressive independence

**STERNAL PRECAUTIONS (FOR 6-8 WEEKS):**
- **NO pushing, pulling, lifting >5 lbs (2 kg)**
- **NO reaching above shoulders**
- **NO driving** for 4-6 weeks (check insurance)
- Sleep on back, supported by pillows
- Hug a pillow when coughing/sneezing
- Avoid tight clothing

**RETURN TO ACTIVITIES:**
- **Light activity:** 2-3 weeks
- **Driving:** 4-6 weeks
- **Work:**
  - Sedentary: 4-6 weeks
  - Manual labour: 12+ weeks
- **Exercise:** Gradual increase, cardiac rehab recommended
- **Sexual activity:** 4-6 weeks when comfortable

**MEDICATIONS:**
- **Aspirin 75mg** indefinitely
- **Statin** indefinitely
- **Beta-blocker** if indicated
- **ACE inhibitor** if LV dysfunction
- Duration of DAPT depends on conduits used

**RED FLAGS (SEEK MEDICAL ATTENTION):**
- Fever >38°C
- Wound redness, discharge, or increasing pain
- Shortness of breath
- Chest pain
- Palpitations
- Leg swelling (DVT/PE)

**LONG-TERM OUTCOME:**
- 10-year survival: 70-80%
- Graft patency:
  - IMA: >90% at 10 years
  - SVG: 50-60% at 10 years
- Symptom relief in 90%+
- Repeat revascularization rate: 10% at 10 years

**EVIDENCE:** STS Guidelines, BACPA Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified CABG recovery query",
                    "Provided timeline for recovery",
                    "Emphasized sternal precautions"
                ],
                capabilities_used=["cardiac_surgery_consultation"],
                metadata={
                    "topic": "cabg_recovery",
                    "guideline": "sts"
                }
            )

        # General CABG information
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**CORONARY ARTERY BYPASS GRAFTING (CABG)**

**WHAT IS IT?**
- Surgery to bypass blocked coronary arteries
- New route for blood to reach heart muscle
- Reduces angina, improves survival in selected patients

**WHO NEEDS CABG?**
- Left main stem disease
- Triple vessel disease (especially with diabetes)
- Double vessel with proximal LAD disease
- Failed PCI
- Reduced LV function with viable myocardium

**PROCEDURE:**
- Median sternotomy (breastbone split)
- Cardiopulmonary bypass (heart-lung machine)
- Stop heart with cardioplegia
- Grafts attached:
  - **LIMA to LAD** (best, most important)
  - Additional grafts to other arteries
- Restart heart, wean off bypass
- Close sternum with wires

**CONDUITS (GRAFTS):**
- **Internal mammary artery** (best, 10yr patency >90%)
- **Radial artery** (good, 10yr patency 80-90%)
- **Saphenous vein** (common, 10yr patency 50-60%)

**RISKS:**
- Mortality: 1-2% (overall)
- Stroke: 1-2%
- Wound infection: 1-3%
- Atrial fibrillation: 30%
- Renal dysfunction: 5-10%

**RECOVERY:**
- Hospital: 5-7 days
- Return to normal: 6-12 weeks
- Full recovery: 3-6 months

**ALTERNATIVES:**
- **PCI** (stenting) - less invasive, higher recurrence
- **Medical therapy** - for some patients

**LONG-TERM:**
- Aspirin indefinitely
- Statin indefinitely
- Risk factor modification critical
- Regular follow-up

**EVIDENCE:** NICE NG185, ESC Guidelines""",
                confidence=0.87,
                reasoning_trace=[
                    "Provided general CABG information",
                    "Explained indications and procedure",
                    "Outlined recovery and alternatives"
                ],
                capabilities_used=["cardiac_surgery_consultation", "coronary_revascularization"],
                metadata={
                    "topic": "cabg_general",
                    "guideline": "nice_ng185"
                }
            )

    def _handle_valve_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle valve surgery queries"""
        query_lower = query.lower()

        # Aortic stenosis
        if any(term in query_lower for term in [
            "aortic stenosis", "as", "aortic valve replacement", "aortic valve narrowing"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**AORTIC STENOSIS**

**DEFINITION:**
- Narrowing of aortic valve orifice
- Progressive obstruction to left ventricular outflow

**SEVERITY ASSESSMENT:**

| Parameter | Mild | Moderate | Severe |
|-----------|------|----------|--------|
| Aortic valve area | >1.5 cm² | 1.0-1.5 cm² | <1.0 cm² |
| Mean gradient | <25 mmHg | 25-40 mmHg | >40 mmHg |
| Peak velocity | <3.0 m/s | 3.0-4.0 m/s | >4.0 m/s |

**SYMPTOMS (Critical Red Flags):**
- **Angina**
- **Syncope** (fainting)
- **Heart failure** (dyspnoea)
- **Sudden cardiac death** (if symptomatic, untreated)

**INDICATIONS FOR AORTIC VALVE REPLACEMENT (AVR):**

**NICE GUIDELINES (NG208) RECOMMENDATIONS:**

**1. Symptomatic Severe AS**
- AVR indicated for ALL symptomatic patients
- Urgent referral (within 2 weeks)
- Symptoms carry poor prognosis without surgery

**2. Asymptomatic Severe AS**
- Consider AVR if:
  - LV ejection fraction <50%
  - Abnormal exercise test
  - Very severe AS (gradient >60 mmHg, area <0.6 cm²)
  - Rapidly progressive (increase in velocity >0.3 m/s/year)
  - Undergoing other cardiac surgery

**AVR OPTIONS:**

**1. Surgical Aortic Valve Replacement (SAVR)**
- Open heart surgery (sternotomy)
- Cardiopulmonary bypass
- Mechanical or tissue valve
- **Preferred for:**
  - Age <65 years (mechanical valve)
  - Need for concomitant cardiac surgery (CABG, etc.)
  - Unsuitable anatomy for TAVI

**2. Transcatheter Aortic Valve Implantation (TAVI)**
- Minimally invasive (femoral artery access)
- No sternotomy, no bypass
- Tissue valve only
- **Preferred for:**
  - Age ≥75 years
  - High surgical risk (STS score >8%)
  - Frailty, comorbidities
  - Patient preference for less invasive

**VALVE CHOICE:**

**Mechanical Valve:**
- **Advantages:** Durable (lifelong)
- **Disadvantages:** Lifelong warfarin (INR 2.5-3.5), bleeding risk
- **Best for:** Age <65, long life expectancy, already on warfarin

**Tissue (Bioprosthetic) Valve:**
- **Advantages:** No long-term anticoagulation
- **Disadvantages:** Limited durability (10-15 years), may need redo
- **Best for:** Age ≥65, contraindication to warfarin, patient preference

**PROGNOSIS:**
- **Without surgery** (symptomatic severe AS):
  - 50% mortality at 2 years
- **With surgery**:
  - Operative mortality: 1-3% (SAVR), <1% (TAVI)
  - Symptom relief: excellent
  - Normal life expectancy after successful surgery

**EVIDENCE:** NICE NG208 (2021), ESC/ EACTS Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified aortic stenosis query",
                    "Applied severity criteria (gradient, area, velocity)",
                    "Symptomatic severe AS requires urgent AVR"
                ],
                capabilities_used=["valve_surgery_assessment"],
                metadata={
                    "topic": "aortic_stenosis",
                    "guideline": "nice_ng208"
                }
            )

        # Mitral regurgitation
        elif any(term in query_lower for term in [
            "mitral regurgitation", "mr", "mitral valve leak", "mitral incompetence"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**MITRAL REGURGITATION**

**DEFINITION:**
- Incompetence of mitral valve
- Backflow of blood from left ventricle to left atrium

**TYPES:**

**1. Primary (Degenerative) MR**
- **Prolapse** - valve leaflet prolapses into atrium
- **Flail** - leaflet tip everts (usually chordal rupture)
- **Carcinoid**, **rheumatic**, **endocarditis**

**2. Secondary (Functional) MR**
- Normal valve, abnormal ventricle
- Ischaemic cardiomyopathy
- Dilated cardiomyopathy
- Left ventricular dilation

**SEVERITY ASSESSMENT:**

| Parameter | Mild | Moderate | Severe |
|-----------|------|----------|--------|
| Regurgitant volume | <30 mL | 30-59 mL | ≥60 mL |
| Regurgitant fraction | <30% | 30-49% | ≥50% |
| Effective orifice area | - | - | ≥40 mm² |
| Vena contracta width | <0.3 cm | 0.3-0.69 cm | ≥0.7 cm |

**INDICATIONS FOR SURGERY:**

**Primary MR (NICE GUIDELINES):**

**1. Symptomatic Severe MR**
- Mitral valve surgery (repair preferred)
- LV ejection fraction >30% (avoid irreversible dysfunction)

**2. Asymptomatic Severe MR**
- Consider surgery if:
  - LV ejection fraction 30-60%
  - LV end-systolic dimension >40 mm
  - Pulmonary hypertension (PASP >50 mmHg)
  - New-onset atrial fibrillation

**Secondary MR:**
- **Medical therapy first-line**
  - ACE inhibitors/ARBs
  - Beta-blockers
  - Diuretics for congestion
- **Surgery** if:
  - Symptoms despite optimal medical therapy
  - Undergoing CABG (add mitral valve repair)
  - Severe MR with LVEF >30%

**SURGICAL OPTIONS:**

**1. Mitral Valve Repair (PREFERRED)**
- **Annuloplasty** - ring to reduce annular size
- **Chordal repair** - replace or shorten chords
- **Leaflet resection** - remove prolapsing segment
- **Advantages:**
  - Preserves native valve
  - Better LV function preservation
  - No anticoagulation needed
  - Lower risk of endocarditis
- **Success:** 90-95% for degenerative MR

**2. Mitral Valve Replacement**
- Mechanical or tissue valve
- **Indicated if:**
  - Valve not repairable
  - Calcified or rheumatic valve
  - Failed previous repair
- **Disadvantages:** Loss of chordal support, worse LV function

**TRANSCATHETER OPTIONS (for high surgical risk):**
- **MitraClip** - edge-to-edge repair
- **Transcatheter mitral valve replacement** (emerging)

**PROGNOSIS:**
- Operative mortality: 1-2% (repair), 3-5% (replacement)
- 10-year survival after repair: 60-70%
- Recurrence: 10% at 10 years (repair), higher with replacement

**EVIDENCE:** NICE NG208, ESC/ EACTS Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified mitral regurgitation query",
                    "Distinguished primary vs secondary MR",
                    "Mitral valve repair preferred over replacement"
                ],
                capabilities_used=["valve_surgery_assessment"],
                metadata={
                    "topic": "mitral_regurgitation",
                    "guideline": "nice_ng208"
                }
            )

        # General valve surgery
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**HEART VALVE SURGERY**

**COMMON VALVE PROBLEMS:**

**Aortic Stenosis**
- Narrowing of aortic valve
- Progressive obstruction
- Symptoms: angina, syncope, heart failure
- Treatment: aortic valve replacement (SAVR or TAVI)

**Mitral Regurgitation**
- Leaking mitral valve
- Backflow to left atrium
- Symptoms: breathlessness, fatigue, atrial fibrillation
- Treatment: mitral valve repair (preferred) or replacement

**Aortic Regurgitation**
- Leaking aortic valve
- Volume overload of left ventricle
- Symptoms: breathlessness, fatigue, angina
- Treatment: aortic valve replacement or root preservation

**Mitral Stenosis**
- Narrowing of mitral valve
- Usually rheumatic heart disease
- Symptoms: breathlessness, atrial fibrillation, haemoptysis
- Treatment: balloon valvuloplasty or valve replacement

**SURGICAL APPROACH:**
- Median sternotomy (most common)
- Cardiopulmonary bypass
- Cardioplegia to stop heart
- Valve repair or replacement
- Restart heart, wean off bypass

**VALVE TYPES:**

**Mechanical Valve:**
- Lifelong durability
- Requires lifelong warfarin
- Clicking sound
- Best for young patients

**Tissue (Bioprosthetic) Valve:**
- Limited durability (10-15 years)
- No long-term anticoagulation
- Silent
- Best for older patients

**RISKS:**
- Operative mortality: 1-3% (varies by valve, procedure)
- Stroke: 1-2%
- Bleeding: 2-5%
- Infection: 1-2%
- Pacemaker requirement (especially after AVR)

**RECOVERY:**
- Hospital: 5-7 days
- Return to normal: 6-12 weeks
- Lifelong follow-up required

**EVIDENCE:** NICE NG208, ESC Guidelines""",
                confidence=0.86,
                reasoning_trace=[
                    "Provided general valve surgery overview",
                    "Listed common valve problems",
                    "Explained valve types (mechanical vs tissue)"
                ],
                capabilities_used=["valve_surgery_assessment"],
                metadata={
                    "topic": "valve_surgery_general",
                    "guideline": "nice_ng208"
                }
            )

    def _handle_aortic_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle aortic surgery queries"""
        return DomainQueryResult(
            domain_name="cardiothoracic_surgery",
            answer="""**AORTIC SURGERY**

**ASCENDING AORTA AND AORTIC ROOT:**

**Indications for Surgery:**

**1. Aortic Aneurysm**
- **Diameter ≥5.5 cm** (or ≥5.0 cm if connective tissue disorder)
- **Growth rate ≥0.5 cm/year**
- **Family history of dissection/rupture** (lower threshold)
- **Bicuspid aortic valve** (lower threshold: ≥5.0 cm)

**2. Aortic Dissection (Type A)**
- Surgical emergency
- Replace ascending aorta ± root

**PROCEDURES:**

**Bentall Procedure:**
- Replace aortic root + aortic valve
- Re-implant coronary arteries
- Composite graft (mechanical or tissue valve)
- Indicated for:
  - Aortic root aneurysm with aortic valve disease
  - Type A dissection with root involvement
  - Connective tissue disorders (Marfan, Loeys-Dietz)

**David Procedure (Valve-Sparing):**
- Replace aortic root, spare native valve
- Re-implantation technique
- Indicated for:
  - Normal aortic valve
  - Aortic root aneurysm
  - Young patients (avoid prosthetic valve)
- Better than Bentall for:
  - Avoids anticoagulation (if native valve preserved)
  - Lower risk of endocarditis
  - Better haemodynamics

**Supracommissural Graft:**
- Replace ascending aorta only
- Preserve aortic root and valve
- Indicated for:
  - Ascending aortic aneurysm with normal root
  - Type A dissection with normal root

**AORTIC ARCH SURGERY:**
- More complex than ascending aorta
- Requires circulatory arrest, hypothermia
- Indicated for:
  - Arch aneurysm
  - Type A dissection extending into arch
  - Penetrating ulcer of arch

**THORACOABDOMINAL AORTA:**
- Open surgery (high risk)
- Or endovascular (frozen elephant trunk, branched EVAR)
- Indicated for:
  - Thoracoabdominal aneurysm
  - Crawford extent I-IV

**RISKS:**
- Operative mortality: 5-10% (varies by extent)
- Stroke: 2-5%
- Paraplegia (thoracoabdominal): 5-10%
- Renal failure: 5-10%
- Reoperation for bleeding: 5-10%

**RECOVERY:**
- ICU: 2-5 days (varies by complexity)
- Hospital: 7-14 days
- Full recovery: 3-6 months

**LIFELONG SURVEILLANCE:**
- CT or MRI surveillance of remaining aorta
- Lifelong blood pressure control
- Beta-blocker therapy
- Lifestyle modifications

**EVIDENCE:** EACTS Guidelines, ESVS Guidelines""",
            confidence=0.89,
            reasoning_trace=[
                "Provided aortic surgery overview",
                "Explained Bentall vs David procedures",
                "Outlined indications and risks"
            ],
            capabilities_used=["aortic_surgery_management"],
            metadata={
                "topic": "aortic_surgery",
                "guideline": "eacts"
            }
        )

    def _handle_thoracic_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle thoracic surgery queries"""
        query_lower = query.lower()

        # Lung cancer surgery
        if any(term in query_lower for term in [
            "lung cancer", "lung tumour", "lung nodule", "pulmonary nodule",
            "nsclc", "non small cell"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**LUNG CANCER SURGERY**

**PREOPERATIVE ASSESSMENT:**

**1. Indications for Surgery**
- **NSCLC** (non-small cell lung cancer) Stage I-II
- Selected Stage IIIA (after neoadjuvant therapy)
- **Not suitable** for small cell (SCLC) - usually chemo/RT
- Patient fitness (adequate lung function, performance status)

**2. Staging Investigations**
- **CT chest/abdomen/pelvis**
- **PET-CT** for metastases
- **EBUS** (endobronchial ultrasound) for mediastinal nodes
- **Brain MRI** if symptoms or large tumour
- **Invasive staging** (mediastinoscopy) if PET/EBUS equivocal

**3. Fitness Assessment**
- **Spirometry** (FEV1)
- **DLCO** (diffusing capacity)
- **Cardiopulmonary exercise testing** if FEV1/DLCO borderline
- **Predicted postoperative FEV1** must be >0.8 L or >40% predicted

**SURGICAL PROCEDURES:**

**1. Lobectomy (STANDARD)**
- Removal of entire lung lobe
- Standard of care for most lung cancers
- **Risks:** Air leak, bleeding, infection, atrial fibrillation

**2. Segmentectomy**
- Removal of one or more lung segments
- **Indicated for:**
  - Tumours ≤2 cm (peripheral)
  - Poor lung function
  - Patient preference
- **Higher local recurrence** than lobectomy

**3. Wedge Resection**
- Removal of wedge of lung containing tumour
- **Indicated for:**
  - Very small tumours (<1 cm)
  - Poor lung function
  - Diagnostic wedge (if frozen section confirms cancer)
- **Highest recurrence rate**

**4. Pneumonectomy**
- Removal of entire lung
- **Indicated for:**
  - Central tumours involving main bronchus/vessels
  - Tumours crossing fissure
- **High morbidity and mortality**
- **Last resort**

**SURGICAL APPROACH:**

**VATS (Video-Assisted Thoracoscopic Surgery)**
- Minimally invasive
- 3-4 small incisions
- Camera and instruments through ports
- **Advantages:** Less pain, faster recovery
- **Disadvantages:** Technical challenge, longer operative time

**Thoracotomy (Open)**
- Large incision between ribs (posterolateral)
- Rib spreader
- **Advantages:** Better exposure, tactile feedback
- **Disadvantages:** More pain, slower recovery

**Robotic**
- Similar to VATS but with robotic arms
- 3D vision, wristed instruments
- Emerging technology

**COMPLICATIONS:**
- **Air leak** (>5 days): 10-20%
- **Atrial fibrillation:** 20-30%
- **Pneumonia:** 5-10%
- **Respiratory failure:** 5%
- **Bleeding requiring reoperation:** 2-5%
- **Mortality:** 1-3% (lobectomy), 5-10% (pneumonectomy)

**POSTOPERATIVE CARE:**
- ICU/HDU for 24-48 hours
- Chest drain (until air leak stops, lung expanded)
- Analgesia (epidural or paravertebral catheter)
- Incentive spirometry, early mobilization
- Oxygen if needed
- Discharge 5-7 days (uncomplicated)

**ADJUVANT THERAPY:**
- **Chemotherapy** for Stage II-IIIA
- **Radiotherapy** for positive margins or N2 disease
- **Immunotherapy** (emerging)

**PROGNOSIS:**
- **Stage I:** 5-year survival 60-80%
- **Stage II:** 5-year survival 40-60%
- **Stage III:** 5-year survival 20-40%

**EVIDENCE:** NICE NG122, BTS Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified lung cancer surgery query",
                    "Applied staging and fitness assessment",
                    "Lobectomy is standard of care for most patients"
                ],
                capabilities_used=["thoracic_surgery_consultation", "lung_cancer_surgery"],
                metadata={
                    "topic": "lung_cancer_surgery",
                    "guideline": "nice_ng122"
                }
            )

        # General thoracic surgery
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**THORACIC SURGERY**

**COMMON THORACIC PROCEDURES:**

**Lung Resection:**
- **Lobectomy** - removal of lung lobe (most common for cancer)
- **Segmentectomy** - removal of lung segment (for small tumours or poor function)
- **Wedge reection** - removal of wedge of lung
- **Pneumonectomy** - removal of entire lung (high risk)

**Approaches:**
- **VATS** - minimally invasive, 3-4 small incisions
- **Thoracotomy** - open, large incision between ribs
- **Robotic** - similar to VATS but with robotic assistance

**Pleural Procedures:**
- **Pleural biopsy** - diagnosis of pleural disease
- **Decortication** - remove fibrinous peel (empyema)
- **Pleurodesis** - fuse pleural layers (prevent recurrent effusion/pneumothorax)
- **Wedge resection** - for pneumothorax (bleb/bulla)

**Mediastinal Procedures:**
- **Thymectomy** - remove thymus (myasthenia gravis, thymoma)
- **Mediastinal mass biopsy** - diagnosis
- **Mediastinal lymphadenectomy** - staging

**Chest Wall:**
- **Rib resection** - for tumour, infection
- **Chest wall resection** - for tumour
- **Pectus repair** - Nuss or Ravitch procedure

**DIAPHRAGM:**
- **Diaphragmatic plication** - for eventration/phrenic nerve injury
- **Repair of hiatus hernia** - para-oesophageal or sliding

**INDICATIONS FOR REFERRAL:**
- Lung cancer (early stage)
- Mediastinal mass
- Pleural effusion (undiagnosed after 2 taps)
- Empyema not resolving with chest drain
- Recurrent pneumothorax
- Chest wall tumour
- Diaphragmatic hernia

**PREOPERATIVE ASSESSMENT:**
- Spirometry (FEV1, FVC)
- DLCO (diffusing capacity)
- CPET if borderline
- Cardiac assessment if indicated

**RISKS:**
- Mortality: 1-3% (varies by procedure)
- Morbidity: 20-30%
- Air leak, atrial fibrillation, pneumonia, respiratory failure

**EVIDENCE:** BTS Guidelines, NICE Guidelines""",
                confidence=0.85,
                reasoning_trace=[
                    "Provided general thoracic surgery overview",
                    "Listed common procedures and approaches",
                    "Outlined indications and risks"
                ],
                capabilities_used=["thoracic_surgery_consultation"],
                metadata={
                    "topic": "thoracic_surgery_general"
                }
            )

    def _handle_pleural_disease_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle pleural disease queries"""
        query_lower = query.lower()

        # Pneumothorax
        if any(term in query_lower for term in [
            "pneumothorax", "collapsed lung", "lung collapse"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**PNEUMOTHORAX**

**CLASSIFICATION:**

**1. Spontaneous Pneumothorax**
- **Primary:** No underlying lung disease (usually young, tall, thin males)
- **Secondary:** Underlying lung disease (COPD, fibrosis, etc.)

**2. Traumatic Pneumothorax**
- **Penetrating trauma** (stab, gunshot)
- **Blunt trauma** (rib fracture)

**3. Iatrogenic Pneumothorax**
- **Following procedure** (central line, pleural tap, lung biopsy)

**4. Tension Pneumothorax**
- **Medical emergency**
- One-way valve effect
- Cardiovascular compromise
- Requires immediate decompression

**MANAGEMENT:**

**Primary Spontaneous Pneumothorax:**
- **Small (<2 cm, <15%):**
  - Observation
  - Discharge with safety netting
  - Repeat CXR in 2 weeks

- **Large (≥2 cm, ≥15%) or Symptomatic:**
  - **Aspiration** (first-line)
  - If successful: discharge
  - If unsuccessful: chest drain (12-16 Fr)

**Secondary Spontaneous Pneumothorax:**
- **ALL require admission**
- **High risk** due to underlying lung disease
- **Chest drain** (most cases)
- Consider aspiration if small and minimally symptomatic

**Traumatic Pneumothorax:**
- **Chest drain** (28 Fr if trauma)
- Admit to hospital
- Monitor for bleeding

**Tension Pneumothorax:**
- **IMMEDIATE needle decompression** (14G/16G, 2nd IC space MCL)
- Followed by chest drain
- DO NOT wait for CXR

**CHEST DRAIN MANAGEMENT:**
- **Size:**
  - Primary spontaneous: 12-16 Fr (small)
  - Trauma: 28-32 Fr (large)
- **Position:**
  - Pneumothorax: 2nd intercostal space, midclavicular line
  - Effusion: 5th intercostal space, posterior axillary line
- **Connect to underwater seal**
- **Suction** (-20 cmH2O) if lung not expanding
- **Remove when:**
  - Lung fully expanded
  - No air leak for 24-48 hours
  - Patient recovered

**INDICATIONS FOR SURGERY:**
- Persistent air leak (>7 days)
- Recurrent pneumothorax (ipsilateral)
- Bilateral pneumothorax
- Occupational risk (pilot, diver)
- Failure of chest drain
- VATS bullectomy + pleurodesis

**PREVENTION OF RECURRENCE:**
- **Pleurodesis** (talc poudrage) during VATS
- Recurrence rate: ~5% after surgery
- Recurrence rate: ~30% without surgery

**EVIDENCE:** BTS Pleural Disease Guidelines (2010)""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified pneumothorax query",
                    "Classified by type (spontaneous, traumatic, tension)",
                    "Management based on size and symptoms"
                ],
                capabilities_used=["pleural_disease_management"],
                metadata={
                    "topic": "pneumothorax",
                    "guideline": "bts_pleural"
                }
            )

        # Pleural effusion
        elif any(term in query_lower for term in [
            "pleural effusion", "fluid on lung", "pleural fluid", "pleural tap"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**PLEURAL EFFUSION**

**CLASSIFICATION:**

**Transudative (Low Protein):**
- **Heart failure** (most common)
- **Hypoalbuminaemia** (nephrotic syndrome, liver disease)
- **Cirrhosis** (hepatic hydrothorax)
- **Nephrotic syndrome**
- **Peritoneal dialysis**

**Exudative (High Protein):**
- **Infection** (pneumonia, empyema, TB)
- **Malignancy** (lung cancer, mesothelioma, metastasis)
- **Pulmonary embolism**
- **Rheumatoid arthritis**, **SLE**
- **Pancreatitis**, **oesophageal rupture**

**INVESTIGATIONS:**

**1. CXR**
- Blunted costophrenic angle
- May show meniscus sign
- Large effusions cause mediastinal shift AWAY from effusion

**2. Pleural Aspiration (Diagnostic Tap)**
- **Indicated for:**
  - All symptomatic effusions
  - Unexplained effusion
- **Send fluid for:**
  - Biochemistry (protein, LDH, pH, glucose)
  - Microscopy (cell count, differential)
  - Microbiology (culture, sensitivity)
  - Cytology (malignant cells)

**3. Light's Criteria (Exudate vs Transudate)**
- Exudate if:
  - Pleural fluid protein/serum protein >0.5
  - Pleural fluid LDH/serum LDH >0.6
  - Pleural fluid LDH >2/3 upper limit of normal serum LDH

**4. CT Chest**
- Underlying lung disease
- Pleural thickening/nodules
- Guide pleural biopsy

**5. Pleural Biopsy**
- **Indicated if:**
  - Suspicious pleural thickening/nodules
  - Undiagnosed exudative effusion after 2 taps
- **Image-guided** (CT or ultrasound)
- **Thoracoscopic** (medical or surgical) for higher yield

**MANAGEMENT:**

**Therapeutic Aspiration:**
- **Indicated if:**
  - Significant dyspnoea
  - Mediastinal shift
- **Drain <1.5 L** at a time (avoid re-expansion pulmonary oedema)
- **Consider chest drain** if fluid reaccumulates rapidly

**Chest Drain:**
- **Indicated for:**
  - Large effusion requiring repeated drainage
  - Empyema
  - Haemothorax
  - Chylothorax
- **Size:** 12-16 Fr (standard)
- **Connect to underwater seal**
- **Consider suction** if lung not expanding

**Pleurodesis:**
- **Indicated for:**
  - Recurrent symptomatic malignant effusion
  - Failed spontaneous pleurodesis
- **Method:**
  - Talc slurry (through chest drain)
  - Talc poudrage (VATS or thoracotomy)
- **Success:** 70-90% (malignant effusion)

**EMERGENCY DRAINAGE:**
- **Tension effusion** (rare but life-threatening)
- Urgent therapeutic aspiration or chest drain

**EVIDENCE:** BTS Pleural Disease Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified pleural effusion query",
                    "Applied Light's criteria for classification",
                    "Management based on aetiology and symptoms"
                ],
                capabilities_used=["pleural_disease_management"],
                metadata={
                    "topic": "pleural_effusion",
                    "guideline": "bts_pleural"
                }
            )

        # Empyema
        elif any(term in query_lower for term in [
            "empyema", "infected pleural fluid", "infected effusion"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**EMPYEMA (Infected Pleural Fluid)**

**DEFINITION:**
- Infection in pleural space
- Purulent fluid or organism on culture
- Stages: simple, complicated, organized

**STAGES (PLEURAL INFECTION):**

**Stage 1: Uncomplicated Parapneumonic Effusion**
- Free-flowing fluid
- pH >7.2
- No organisms on Gram stain
- **Management:** Antibiotics ± drainage

**Stage 2: Complicated Parapneumonic Effusion**
- Loculated fluid
- pH <7.2
- Glucose <2.2 mmol/L
- LDH >1000 IU/L
- **Management:** Chest drain + fibrinolytics OR surgery

**Stage 3: Empyema**
- Thick pleural peel
- Organized, loculated
- Trapped lung
- **Management:** Surgical decortication

**INVESTIGATIONS:**

**1. CXR** - blunted CP angle, may show loculation

**2. CT Chest**
- Confirm diagnosis
- Assess extent
- Identify underlying pneumonia/abscess

**3. Pleural Aspiration**
- **Send for:**
  - pH (critical)
  - Glucose
  - LDH
  - Microscopy, culture, sensitivity
  - Cell count (neutrophilia)

**4. Ultrasound**
- Identify loculations
- Guide chest drain insertion

**MANAGEMENT:**

**1. Antibiotics**
- **Broad-spectrum** initially (ceftriaxone + metronidazole)
- Tailor to culture results
- Duration: 2-4 weeks (IV then oral)

**2. Chest Drain**
- **Indicated for:**
  - pH <7.2
  - Glucose <2.2 mmol/L
  - Loculated fluid
  - Septic patient
- **Size:** 12-16 Fr (small) or 20-24 Fr (large/loculated)
- **Image-guided insertion** (ultrasound or CT)
- **Suction** may help lung expansion

**3. Intrapleural Fibrinolytics**
- **Tissue plasminogen activator (tPA)** + DNase
- **Indicated for:**
  - Multiloculated effusion
  - Poor drainage despite chest drain
- **Improves drainage**, may avoid surgery

**4. Surgical Decortication**
- **Indicated for:**
  - Failed chest drain + fibrinolytics
  - Organized empyema (thick peel, trapped lung)
  - Septic patient despite medical management
- **Procedure:**
  - VATS (if early) - debride, break loculations
  - Thoracotomy (if organized) - decortication, remove peel
- **Success:** >90% if done early
- **Mortality:** 5-10% (higher if delayed, frail patients)

**COMPLICATIONS:**
- **Sepsis**
- **Respiratory failure**
- **Trapped lung** (persistent air space)
- **Bronchopleural fistula** (rare)
- **Empyema necessitatis** (extends through chest wall - rare)

**PROGNOSIS:**
- Good if treated early (Stage 1-2)
- Worse if delayed (Stage 3, organized)
- Mortality: 10-20% (higher with comorbidities)

**EVIDENCE:** BTS Pleural Infection Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified empyema query",
                    "Staged infection (uncomplicated, complicated, organized)",
                    "Escalating management: antibiotics → drain → fibrinolytics → surgery"
                ],
                capabilities_used=["pleural_disease_management"],
                metadata={
                    "topic": "empyema",
                    "guideline": "bts_pleural_infection"
                }
            )

        # General pleural disease
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**PLEURAL DISEASE**

**COMMON CONDITIONS:**

**Pleural Effusion (Fluid in Pleural Space)**
- **Transudative:** Heart failure, cirrhosis, nephrotic syndrome
- **Exudative:** Infection, malignancy, pulmonary embolism
- Investigation: CXR, pleural aspiration, Light's criteria
- Management: Treat cause, therapeutic drainage if symptomatic

**Pneumothorax (Air in Pleural Space)**
- **Primary spontaneous:** Young, tall, thin males (no lung disease)
- **Secondary spontaneous:** Underlying lung disease (COPD, fibrosis)
- **Traumatic:** Chest trauma, iatrogenic (procedures)
- Management: Aspiration, chest drain, surgery (if recurrent)

**Empyema (Infected Pleural Fluid)**
- Complication of pneumonia
- Stages: uncomplicated → complicated → organized
- Management: Antibiotics, chest drain, fibrinolytics, surgical decortication

**Mesothelioma**
- Malignancy of pleura
- asbestos exposure (20-40 years latency)
- Diagnosis: CT, thoracoscopy, biopsy
- Prognosis: Poor (median 12 months)

**INVESTIGATIONS:**

**CXR** - Initial investigation
**CT Chest** - Detailed anatomy, guide interventions
**Ultrasound** - Guide procedures, identify loculations
**Pleural Aspiration** - Diagnostic/therapeutic
**Thoracoscopy** - Direct visualization, biopsy, pleurodesis

**PROCEDURES:**

**Pleural Aspiration (Tap)**
- Diagnostic (send fluid for analysis)
- Therapeutic (drain symptomatic effusion)

**Chest Drain (Intercostal Catheter)**
- Pneumothorax, effusion, empyema, haemothorax
- Connect to underwater seal drain
- Suction if lung not expanding
- Remove when lung expanded, no air leak

**Pleurodesis**
- Fuse pleural layers to prevent fluid/air recurrence
- Talc (most effective)
- Indicated for recurrent pneumothorax or malignant effusion

**DECORTICATION**
- Surgical removal of thickened pleural peel
- Indicated for organized empyema (trapped lung)

**EVIDENCE:** BTS Pleural Disease Guidelines""",
                confidence=0.84,
                reasoning_trace=[
                    "Provided general pleural disease overview",
                    "Listed common pleural conditions",
                    "Outlined investigations and procedures"
                ],
                capabilities_used=["pleural_disease_management"],
                metadata={
                    "topic": "pleural_disease_general"
                }
            )

    def _handle_oesophageal_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle oesophageal surgery queries"""
        return DomainQueryResult(
            domain_name="cardiothoracic_surgery",
            answer="""**OESOPHAGEAL SURGERY**

**COMMON OESOPHAGEAL PROCEDURES:**

**Oesophagectomy (Oesophageal Cancer):**
- **Indicated for:** Oesophageal cancer (early stage)
- **Approaches:**
  - **Transhiatal** - no thoracotomy (for lower third tumours)
  - **Ivor Lewis** - right thoracotomy + laparotomy (most common)
  - **McKeown** - left thoracotomy + laparotomy + neck anastomosis
- **Reconstruction:** Gastric pull-up (most common), colonic interposition
- **Morbidity:** 40-50% (anastomotic leak, recurrent laryngeal nerve palsy)
- **Mortality:** 2-5% (high-volume centres)

**Achalasia Cardia:**
- **Heller's cardiomyotomy** - surgical division of lower oesophageal sphincter
- **Laparoscopic** (minimally invasive)
- **Add partial fundoplication** (Dor or Toupet) to prevent reflux
- **Success:** 80-90%

**Hiatus Hernia:**
- **Type I (Sliding):** 95% of cases
  - **Fundoplication** (Nissen or Toupet) - anti-reflux surgery
- **Type II (Para-oesophageal):**
  - **Emergency repair** if incarcerated/strangulated
  - **Elective repair** once diagnosed
  - Reduce hernia, close crura, fundoplication

**Oesophageal Perforation:**
- **Medical emergency**
- **Iatrogenic** (endoscopy) most common
- **Management:**
  - **Early (<24 hours):** Surgical repair ± primary repair, ± reinforcement
  - **Late (>24 hours):** Drainage, diversion (cervical spit fistula), exclusion
  - **Endoscopic stenting** (selected cases)
- **Mortality:** 10-30% (higher if delayed)

**Oesophageal Diverticulum:**
- **Zenker's** (pharyngeal) - cricopharyngeal myotomy ± diverticulectomy
- **Epiphrenic** - above diaphragm, myotomy ± diverticulectomy
- **Traction** - often treated for underlying cause

**PREOPERATIVE ASSESSMENT:**
- **Endoscopy** - visualize tumour, take biopsies
- **CT chest/abdomen/pelvis** - staging
- **PET-CT** - metastases
- **Endoscopic ultrasound (EUS)** - T and N stage
- **Nutritional assessment** - malnutrition common
- **Cardiopulmonary exercise testing** - fitness for major surgery

**POSTOPERATIVE CARE:**
- ICU/HDU for 48-72 hours
- **Nasogastric tube** - decompress stomach
- **Chest drains** - if thoracotomy
- **Anastomotic leak** (most serious complication) - fever, sepsis, neck swelling
- **Contrast swallow** (day 5-7) - check anastomosis before oral intake
- Gradual diet (water → liquid → soft → solid)

**COMPLICATIONS:**
- **Anastomotic leak:** 10-20% (life-threatening)
- **Recurrent laryngeal nerve palsy:** 5-10%
- **Chyle leak:** 5% (thoracic duct injury)
- **Pulmonary:** 20-30% (pneumonia, respiratory failure)
- **Mortality:** 2-5% (high-volume centres)

**EVIDENCE:** NICE NG182, OESO Guidelines""",
            confidence=0.88,
            reasoning_trace=[
                "Provided oesophageal surgery overview",
                "Covered cancer, achalasia, hernia, perforation",
                "Outlined assessment and complications"
            ],
            capabilities_used=["oesophageal_surgery_consultation"],
            metadata={
                "topic": "oesophageal_surgery",
                "guideline": "nice_ng182"
            }
        )

    def _handle_post_cardiac_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle post cardiac surgery queries"""
        return DomainQueryResult(
            domain_name="cardiothoracic_surgery",
            answer="""**POST CARDIAC SURGERY RECOVERY**

**IMMEDIATE POSTOPERATIVE (ICU/HDU - 24-48 HOURS):**

**1. Monitoring**
- Invasive arterial line (blood pressure)
- Central venous line
- Urinary catheter (output)
- Chest drains (monitor bleeding)
- Pacemaker wires (if placed)

**2. Pain Control**
- Epidural or paravertebral catheter (if thoracotomy)
- PCA (patient-controlled analgesia)
- Oral analgesia when eating/drinking

**3. Breathing Exercises**
- Incentive spirometry (10 breaths hourly)
- Deep breathing and coughing
- Pillow to support sternum

**4. Mobilization**
- Sit out of bed day 1
- Walk with assistance day 2-3
- Progressive independence

**STERNAL PRECAUTIONS (FOR 6-8 WEEKS):**

**DO NOT:**
- Push, pull, lift >5 lbs (2 kg)
- Reach above shoulders
- Drive (4-6 weeks - check insurance)
- Sleep on side (sleep on back, supported)

**DO:**
- Hug a pillow when coughing/sneezing
- Keep wounds clean and dry
- Wear loose clothing
- Gentle arm exercises (below shoulder level)

**WOUND CARE:**
- **Sternal wound:**
  - Keep dry
  - Dressings removed day 5-7
  - Sterile strips (Steri-Strips) fall off naturally (7-10 days)
  - May see wires (normal)
- **Leg wounds** (if vein harvest):
  - Keep elevated when sitting
  - Dressings removed day 5-7
  - May have sutures or clips (removed day 7-10)

**MEDICATIONS:**
- **Aspirin 75mg** - indefinitely (most cardiac surgery)
- **Statin** - indefinitely
- **Beta-blocker** - if indicated
- **ACE inhibitor** - if LV dysfunction
- **Warfarin** - if mechanical valve (INR 2.5-3.5 for aortic, 3.0-4.0 for mitral)
- **Duration of DAPT** - depends on conduits used (if CABG)

**RED FLAGS (SEEK MEDICAL ATTENTION):**
- Fever >38°C
- Wound redness, discharge, or increasing pain
- Shortness of breath
- Chest pain
- Palpitations
- Leg swelling (DVT/PE)
- Fainting

**RETURN TO ACTIVITIES:**
- **Light activity:** 2-3 weeks
- **Driving:** 4-6 weeks
- **Work:**
  - Sedentary: 4-6 weeks
  - Manual labour: 12+ weeks
- **Exercise:** Gradual increase, cardiac rehab recommended
- **Sexual activity:** 4-6 weeks when comfortable

**LONG-TERM:**
- Lifelong follow-up
- Repeat imaging if symptoms recur
- Cardiac rehabilitation programme
- Risk factor modification (smoking, BP, cholesterol, diabetes, weight)

**EVIDENCE:** STS Guidelines, BACPA Guidelines""",
            confidence=0.89,
            reasoning_trace=[
                "Provided post cardiac surgery recovery information",
                "Emphasized sternal precautions",
                "Red flags for complications"
            ],
            capabilities_used=["cardiac_surgery_consultation"],
            metadata={
                "topic": "post_cardiac_surgery",
                "guideline": "sts"
            }
        )

    def _handle_mechanical_support_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle LVAD/VAD/ECMO queries"""
        query_lower = query.lower()

        # LVAD
        if any(term in query_lower for term in [
            "lvad", "left ventricular assist", "ventricular assist", "vad", "heart pump"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**LEFT VENTRICULAR ASSIST DEVICE (LVAD)**

**WHAT IS IT?**
- Mechanical pump that assists failing left ventricle
- Implanted in left ventricular apex
- Outflow graft to ascending aorta
- External battery/controller

**INDICATIONS:**

**1. Bridge to Transplant (BTT)**
- Patient awaiting heart transplant
- LVAD supports until donor organ available

**2. Destination Therapy (DT)**
- Patient not candidate for transplant
- LVAD as permanent therapy
- Usually older patients with comorbidities

**3. Bridge to Recovery**
- Temporary support for potentially reversible heart failure
- Myocarditis, post-cardiotomy shock
- Some recover, others progress to transplant or DT

**PATIENT SELECTION:**
- **Advanced heart failure** (NYHA III-IV)
- **LVEF ≤25%**
- **Maximal medical therapy** (ACE-I, beta-blocker, aldosterone antagonist)
- **Failed or ineligible for cardiac resynchronization therapy (CRT)**
- **Suitable for surgery** (frailty assessment)
- **Social support** (critical for device management)

**COMMON DEVICES:**

**HeartMate 3:**
- Fully magnetically levitated (no bearings)
- Lower stroke risk than previous generations
- Whisper quiet (unlike HeartMate II)
- Most commonly used currently

**HeartWare HVAD:**
- Smaller, centrifugal flow
- Implanted in pericardial space
- Higher thrombosis risk than HeartMate 3
- No longer available (withdrawn from market)

**SURGERY:**
- Median sternotomy
- CPB (cardiopulmonary bypass)
- Inflow cannula in LV apex
- Outflow graft to ascending aorta
- Driveline exits abdomen (periumbilical)
- Controller and batteries external

**COMPLICATIONS:**

**Bleeding:**
- Gastrointestinal bleeding most common
- Acquired von Willebrand disease (shear stress)
- Anticoagulation adds to risk

**Thrombosis:**
- Pump thrombosis
- Requires thrombolysis or pump exchange
- Less common with HeartMate 3

**Stroke:**
- Ischaemic (pump thrombosis)
- Haemorrhagic (anticoagulation)
- ~5-10% overall

**Infection:**
- Driveline infection (most common)
- Pump infection (serious)
- Requires long-term antibiotics ± device exchange

**Right Ventricular Failure:**
- 20-30% require temporary RVAD support
- May need permanent RVAD (BiVAD)

**Anticoagulation:**
- **Warfarin** (INR 2.0-3.0)
- **Aspirin 75-100 mg** daily
- **NOACs not used** (lack evidence)

**QUALITY OF LIFE:**
- Significant improvement in NYHA class
- Improved exercise capacity
- Return to normal activities possible
- Continuous power supply (batteries 6-12 hours)
- No swimming or bathing (device external)

**PROGNOSIS:**
- 1-year survival: 80-90%
- 2-year survival: 70-80%
- 5-year survival: 50-60%
- Better than medical therapy alone

**EVIDENCE:** NICE TA563, ISHLT Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified LVAD query",
                    "Explained indications (BTT, DT, bridge to recovery)",
                    "Outlined complications and anticoagulation"
                ],
                capabilities_used=["cardiac_surgery_consultation"],
                metadata={
                    "topic": "lvad",
                    "guideline": "nice_ta563"
                }
            )

        # ECMO
        elif any(term in query_lower for term in [
            "ecmo", "extracorporeal membrane oxygenation", "ecmo support"
        ]):
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**EXTRACORPOREAL MEMBRANE OXYGENATION (ECMO)**

**WHAT IS IT?**
- External circuit for oxygenation and circulation
- Bypass heart and lungs temporarily
- Used for severe respiratory or cardiac failure

**TYPES:**

**1. Veno-Venous (VV) ECMO**
- **Respiratory support only**
- **Cannulation:**
  - Drainage: Femoral vein (or internal jugular)
  - Return: Femoral vein or internal jugular
- **Indicated for:**
  - Severe ARDS (acute respiratory distress syndrome)
  - Refractory hypoxaemia despite optimal ventilation
  - Waiting for lung transplant
  - Bridge to recovery
- **Flow:** 3-5 L/min

**2. Veno-Arterial (VA) ECMO)**
- **Cardiac and respiratory support**
- **Cannulation:**
  - Drainage: Femoral vein
  - Return: Femoral artery (or central)
- **Indicated for:**
  - Cardiogenic shock
  - Post-cardiotomy shock
  - Refractory cardiac arrest (E-CPR)
  - Waiting for heart transplant
  - Bridge to decision (recovery, VAD, transplant)
- **Flow:** 4-6 L/min

**INDICATIONS:**

**Respiratory (VV ECMO):**
- **Severe ARDS** (P/F ratio <80 despite optimal ventilation)
- **Murray score >3** (or >2 with refractory hypercapnia)
- **Reversible cause** (pneumonia, ARDS, trauma)
- **No contraindications** (futility, comorbidities)

**Cardiac (VA ECMO):**
- **Cardiogenic shock** refractory to medical therapy
- **Post-cardiotomy shock** (unable to wean from CPB)
- **E-CPR** (extracorporeal CPR) for refractory cardiac arrest
- **Bridge to decision** (recovery, VAD, transplant)

**CONTRAINDICATIONS:**
- **Futility** (no chance of meaningful recovery)
- **Severe comorbidities** (advanced malignancy, severe neurological injury)
- **Uncontrolled bleeding**
- **Severe peripheral vascular disease** (for femoral cannulation)

**COMPLICATIONS:**

**Bleeding:**
- Anticoagulation required (heparin infusion)
- Gastrointestinal, surgical site, intracranial
- Thrombocytopenia

**Thrombosis:**
- Circuit thrombosis
- Oxygenator failure
- Requires circuit change

**Infection:**
- Cannula site infection
- Sepsis

**Neurological:**
- Ischaemic stroke (thromboembolism)
- Intracranial haemorrhage
- Hypoxic brain injury

**Limb Ischaemia:**
- Femoral artery cannulation (VA ECMO)
- May require distal perfusion cannula

**Anticoagulation:**
- **Heparin infusion**
- **Target APTT:** 60-80 seconds (or anti-Xa 0.3-0.7)
- **Monitor:** APTT q6h, anti-Xa daily

**OUTCOMES:**
- High mortality (50-70% overall)
- Better in selected patients
- Survival to discharge:
  - ARDS on VV ECMO: 60-70%
  - Cardiogenic shock on VA ECMO: 40-50%
  - E-CPR: 20-30%

**EVIDENCE:** ELSO Guidelines, NICE NG397""",
                confidence=0.90,
                reasoning_trace=[
                    "Identified ECMO query",
                    "Distinguished VV (respiratory) vs VA (cardiac)",
                    "Outlined indications and complications"
                ],
                capabilities_used=["cardiac_surgery_consultation"],
                metadata={
                    "topic": "ecmo",
                    "guideline": "elso"
                }
            )

        # General mechanical support
        else:
            return DomainQueryResult(
                domain_name="cardiothoracic_surgery",
                answer="""**MECHANICAL CIRCULATORY SUPPORT**

**LVAD (Left Ventricular Assist Device):**
- Implanted pump to assist failing left ventricle
- Indications: Bridge to transplant, destination therapy
- Continuous flow, external power source
- Requires anticoagulation (warfarin)
- Complications: bleeding, thrombosis, stroke, infection

**RVAD (Right Ventricular Assist Device):**
- Supports failing right ventricle
- Often used temporarily
- May be needed if RV fails after LVAD implantation
- BiVAD if both ventricles fail

**ECMO (Extracorporeal Membrane Oxygenation):**
- Temporary support
- **VV ECMO:** Respiratory support only
- **VA ECMO:** Cardiac and respiratory support
- Indicated for severe ARDS, cardiogenic shock, refractory cardiac arrest
- Short-term use (days to weeks)
- High mortality, high complication rate

**TOTAL ARTIFICIAL HEART:**
- Replaces entire native heart
- Bridge to transplant
- Rare, high-risk procedure

**INDICATIONS FOR MECHANICAL SUPPORT:**
- Advanced heart failure (NYHA III-IV)
- Refractory to maximal medical therapy
- Eligible for transplant (BTT) or not eligible (DT)
- Reversible cardiac failure (bridge to recovery)

**SELECTION:**
- Assessment by heart failure multidisciplinary team
- Cardiologist, cardiac surgeon, transplant coordinator
- Social support critical (especially for LVAD)
- Frailty assessment
- Nutritional assessment

**EVIDENCE:** NICE Guidelines, ISHLT Guidelines""",
                confidence=0.85,
                reasoning_trace=[
                    "Provided general mechanical support overview",
                    "Compared LVAD vs RVAD vs ECMO",
                    "Outlined indications and selection"
                ],
                capabilities_used=["cardiac_surgery_consultation"],
                metadata={
                    "topic": "mechanical_support"
                }
            )

    def _handle_general_cardiothoracic_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general cardiothoracic surgery queries"""
        return DomainQueryResult(
            domain_name="cardiothoracic_surgery",
            answer="""**CARDIOTHORACIC SURGERY**

Cardiothoracic surgery is a specialty dealing with heart and lung surgery.

**CARDIAC SURGERY:**

**Coronary Artery Bypass Grafting (CABG)**
- Bypass blocked coronary arteries
- Indications: Left main disease, triple vessel disease, failed PCI
- LIMA to LAD (gold standard)
- Hospital: 5-7 days

**Valve Surgery**
- Aortic valve replacement (for stenosis/regurgitation)
- Mitral valve repair (preferred) or replacement (for regurgitation)
- Surgical (SAVR) or transcatheter (TAVI)
- Choice: Mechanical (lifelong, warfarin) vs tissue (limited, no warfarin)

**Aortic Surgery**
- Ascending aorta aneurysm repair
- Bentall procedure (root + valve)
- David procedure (valve-sparing root)
- Emergency: Type A aortic dissection

**Arrhythmia Surgery**
- Surgical ablation for atrial fibrillation (maze procedure)
- Often combined with other cardiac surgery

**THORACIC SURGERY:**

**Lung Resection**
- Lobectomy (standard for cancer)
- Segmentectomy, wedge resection (small tumours/poor function)
- Pneumonectomy (entire lung - high risk)
- VATS (minimally invasive) or thoracotomy (open)

**Pleural Procedures**
- Chest drain for pneumothorax, effusion, empyema
- Decortication (empyema)
- Pleurodesis (prevent recurrence)

**Oesophageal Surgery**
- Oesophagectomy (cancer)
- Heller myotomy (achalasia)
- Hiatus hernia repair

**CARDIOTHORACIC EMERGENCIES:**
- Cardiac tamponade (pericardiocentesis, surgery)
- Penetrating cardiac injury (emergency thoracotomy)
- Aortic dissection Type A (emergency surgery)
- Tension pneumothorax (needle decompression, chest drain)

**PREOPERATIVE ASSESSMENT:**
- CXR, ECG, echocardiogram
- Coronary angiography (if cardiac surgery)
- CT chest (if thoracic surgery)
- Spirometry (if lung resection)
- CPET if borderline fitness

**RISKS:**
- Mortality: 1-3% (varies by procedure)
- Stroke: 1-2% (cardiac surgery)
- Bleeding: 2-5%
- Infection: 1-3%
- Arrhythmias: 20-30% (AF post-cardiac surgery)

**RECOVERY:**
- ICU/HDU: 1-2 days
- Hospital: 5-7 days (uncomplicated)
- Return to normal: 6-12 weeks

**EVIDENCE:** NICE Guidelines, EACTS/ ESC Guidelines""",
            confidence=0.82,
            reasoning_trace=[
                "Provided general cardiothoracic surgery overview",
                "Listed main cardiac and thoracic procedures",
                "Outlined assessment and risks"
            ],
            capabilities_used=[
                "cardiac_surgery_consultation",
                "thoracic_surgery_consultation"
            ],
            metadata={
                "topic": "cardiothoracic_surgery_general"
            }
        )


def create_cardiothoracic_surgery_domain():
    """Factory function for cardiothoracic surgery domain"""
    return CardiothoracicSurgeryDomain()
