"""
Vascular Surgery Domain Module for GPDISC

Comprehensive vascular surgery consultation covering arterial and venous disease,
vascular trauma, and vascular emergencies.

Evidence-based guidelines from:
- European Society for Vascular Surgery (ESVS)
- National Institute for Health and Care Excellence (NICE)
- Society for Vascular Surgery (SVS)
- British Society for Interventional Radiology (BSIR)

Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class VascularSurgeryDomain(BaseDomainModule):
    """
    Vascular Surgery specialty domain for GPDISC

    Covers arterial and venous disease, vascular trauma, and vascular emergencies.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="vascular_surgery",
            version="1.0.0",
            dependencies=[],
            description="Vascular surgery: arterial and venous disease, aneurysms, vascular trauma",
            keywords=[
                # Arterial disease
                "peripheral arterial disease", "pad", "arterial", "artery", "aorta", "aortic",
                "aneurysm", "aaa", "abdominal aortic aneurysm", "thoracic aneurysm",
                "carotid", "carotid artery", "carotid stenosis", "tia", "transient ischemic attack",
                "limb ischaemia", "acute limb ischaemia", "chronic limb ischaemia", "critical limb ischaemia",
                "claudication", "rest pain", "gangrene", "ulcer", "foot ulcer",
                "bypass", "angioplasty", "stent", "endarterectomy",

                # Venous disease
                "venous", "vein", "dvt", "deep vein thrombosis", "venous thrombosis",
                "pulmonary embolism", "pe", "venous thromboembolism", "vte",
                "varicose vein", "varicose veins", "venous ulcer", "leg ulcer",
                "venous insufficiency", "chronic venous insufficiency", "cvi",
                "thrombophlebitis", "superficial thrombophlebitis",
                "compression", "compression stocking", "compression therapy",

                # Vascular emergencies
                "ruptured aneurysm", "aortic rupture", "dissection", "aortic dissection",
                "acute limb ischaemia", "arterial embolus", "arterial thrombosis",
                "mesenteric ischaemia", "acute mesenteric ischaemia", "chronic mesenteric ischaemia",
                "vascular trauma", "arterial injury", "venous injury",

                # Other vascular conditions
                "vascular", "blood vessel", "circulation", "poor circulation",
                "raynaud", "raynaud's", "raynaud's phenomenon", "acrocyanosis",
                "thromboangiitis obliterans", "burger's disease",
                "fibromuscular dysplasia", "fmd",
                "vascular access", "fistula", "graft", "avf", "avg",
                "dialysis access", "haemodialysis access",

                # Vascular imaging and procedures
                "duplex", "doppler", "ultrasound", "ct angiogram", "mra", "angiography",
                "vascular surgery", "vascular surgeon", "vascular procedure",
                "stent graft", "evare", "evar", "tevar", "fenestrated"
            ],
            capabilities=[
                "arterial_disease_assessment",
                "aneurysm_evaluation_and_management",
                "carotid_disease_management",
                "peripheral_arterial_disease_treatment",
                "venous_disease_assessment",
                "dvt_diagnosis_and_management",
                "venous_ulcer_management",
                "vascular_emergency_management",
                "vascular_trauma_assessment",
                "vascular_imaging_interpretation",
                "preoperative_assessment"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process vascular surgery query

        Routes to appropriate handler based on query content.
        """
        query_lower = query.lower()

        # VASCULAR EMERGENCIES - Highest priority
        if any(term in query_lower for term in [
            "ruptured aneurysm", "aortic rupture", "rupture", "ruptured aaa",
            "aortic dissection", "dissection", "type a dissection",
            "acute limb ischaemia", "limb ischaemia", "acute arterial",
            "mesenteric ischaemia", "acute mesenteric", "bowel ischaemia",
            "vascular trauma", "arterial injury", "vascular injury"
        ]):
            return self._handle_vascular_emergency(query, context)

        # Aortic aneurysm
        elif any(term in query_lower for term in [
            "aneurysm", "aaa", "abdominal aortic aneurysm", "thoracic aneurysm",
            "aortic dilation", "aortic widening"
        ]):
            return self._handle_aneurysm_query(query, context)

        # Carotid disease
        elif any(term in query_lower for term in [
            "carotid", "carotid artery", "carotid stenosis", "carotid endarterectomy"
        ]):
            return self._handle_carotid_query(query, context)

        # Peripheral arterial disease / claudication
        elif any(term in query_lower for term in [
            "pad", "peripheral arterial", "peripheral artery", "claudication",
            "rest pain", "critical limb ischaemia", "gangrene", "foot ulcer"
        ]):
            return self._handle_pad_query(query, context)

        # Deep vein thrombosis / VTE
        elif any(term in query_lower for term in [
            "dvt", "deep vein thrombosis", "venous thrombosis", "blood clot in leg",
            "pulmonary embolism", "pe", "venous thromboembolism", "vte"
        ]):
            return self._handle_dvt_query(query, context)

        # Varicose veins / venous disease
        elif any(term in query_lower for term in [
            "varicose", "varicose vein", "venous ulcer", "leg ulcer",
            "venous insufficiency", "chronic venous", "spider vein"
        ]):
            return self._handle_venous_disease_query(query, context)

        # Vascular access
        elif any(term in query_lower for term in [
            "vascular access", "fistula", "avf", "avg", "dialysis access",
            "haemodialysis access", "hemodialysis access"
        ]):
            return self._handle_vascular_access_query(query, context)

        # Raynaud's / vasospastic disease
        elif any(term in query_lower for term in [
            "raynaud", "raynaud's", "raynauds", "acrocyanosis", "chilblain"
        ]):
            return self._handle_raynaud_query(query, context)

        # General vascular surgery query
        else:
            return self._handle_general_vascular_query(query, context)

    def _handle_vascular_emergency(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle vascular emergencies requiring urgent intervention"""
        query_lower = query.lower()

        # Ruptured aneurysm
        if any(term in query_lower for term in [
            "ruptured aneurysm", "rupture", "ruptured aaa", "aortic rupture"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**RUPTURED AORTIC ANEURYSM - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Activate MAJOR TRAUMA protocol**
- **Urgent vascular surgery involvement**
- **Immediate transfer to vascular centre with EVAR capability**

**CLINICAL PRESENTATION:**
- Classic triad: sudden severe pain, hypotension, pulsatile abdominal mass
- Back pain (abdominal) or chest pain (thoracic)
- Syncope or collapse
- Signs of shock: tachycardia, hypotension, cool peripheries

**IMMEDIATE MANAGEMENT:**
1. **ABC approach**
   - Secure airway if decreased conscious level
   - Large bore cannulas (14G/16G) x2
   - Cross-match 4-6 units blood

2. **Fluid resuscitation**
   - Balanced blood products if available (1:1:1 ratio)
   - O-negative blood if protocol not available
   - Target MAP 60-70 mmHg (permissive hypotension)
   - Avoid excessive fluids before control

3. **Imaging**
   - **CT angiogram** if patient stable enough
   - Transfer to theatre if unstable
   - Informed consent may not be possible

4. **Definitive treatment**
   - **EVAR** (Endovascular aneurysm repair) if anatomically suitable
   - **Open repair** if EVAR not suitable
   - Theatre should be prepared for both

**PROGNOSIS:**
- Mortality: 50-80% overall
- Better outcomes with EVAR if suitable
- Time to repair is critical

**Evidence:** ESVS 2019 Guidelines, NICE NG156""",
                confidence=0.97,
                reasoning_trace=[
                    "Identified ruptured aneurysm - life-threatening vascular emergency",
                    "Applied ESVS rupture management protocol",
                    "Prioritized rapid transfer to vascular centre",
                    "Considered EVAR vs open repair options"
                ],
                capabilities_used=["vascular_emergency_management", "aneurysm_evaluation_and_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "ruptured_aortic_aneurysm",
                    "intervention": "urgent_surgical_repair",
                    "mortality_risk": "high"
                }
            )

        # Aortic dissection
        elif any(term in query_lower for term in [
            "aortic dissection", "dissection", "type a", "type b"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**AORTIC DISSECTION - CARDIOVASCULAR EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent CT angiogram** (whole aorta)
- **Type A dissection: immediate surgical intervention**
- **Type B dissection: consider TEVAR**

**CLINICAL PRESENTATION:**
- **Tearing chest pain** radiating to back (Type A)
- **Tearing back/abdominal pain** (Type B)
- Pulse deficits or blood pressure discrepancies
- Neurological deficits if carotid involved
- Syncope, cardiac tamponade signs (Type A)

**CLASSIFICATION:**
- **Type A (Stanford):** Ascending aorta involved → Surgical emergency
- **Type B (Stanford):** Descending aorta only → Medical management initially

**IMMEDIATE MANAGEMENT:**
1. **Analgesia** - IV opioids
2. **BP control**
   - Target SBP 100-120 mmHg
   - IV labetalol or esmolol
   - Add nicardipine if needed
3. **Heart rate control**
   - Target HR 60-80 bpm
   - Beta-blocker first-line
4. **CT angiogram** for definitive diagnosis
5. **Urgent cardiac surgery referral** for Type A

**TREATMENT:**
- **Type A:** Emergency surgical repair (ascending aorta replacement)
- **Type B with complications:** TEVAR (thoracic EVAR)
- **Type B uncomplicated:** Medical management (antihypertensives)

**Evidence:** ESVS 2023 Guidelines, ESC 2023 Guidelines""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified aortic dissection - cardiovascular emergency",
                    "Applied Stanford classification (Type A vs Type B)",
                    "Type A requires immediate surgical intervention",
                    "Type B may be managed medically or with TEVAR"
                ],
                capabilities_used=["vascular_emergency_management", "aneurysm_evaluation_and_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "aortic_dissection",
                    "classification": "stanford",
                    "intervention": "surgical_or_tevar"
                }
            )

        # Acute limb ischaemia
        elif any(term in query_lower for term in [
            "acute limb ischaemia", "limb ischaemia", "acute arterial", "cold limb",
            "pulseless limb", "white leg"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**ACUTE LIMB ISCHAEMIA - LIMB-THREATENING EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent vascular surgery assessment**
- **Time to reperfusion critical** - salvage decreases after 6 hours
- **Admit for urgent intervention**

**CLINICAL PRESENTATION:**
- **Pain** - Severe, sudden onset
- **Pallor** - Pale, white limb
- **Pulseless** - Absent pulses distal to occlusion
- **Paraesthesia** - Numbness, tingling
- **Paralysis** - Motor weakness (late sign - poor prognosis)
- **Poikilothermia** - Cold limb

**ASSESSMENT:**
1. **Check pulses** - Compare with contralateral limb
2. **Capillary refill** - Prolonged >3 seconds
3. **Sensory examination** - Light touch, proprioception
4. **Motor function** - Ankle/toe movements
5. **Doppler ultrasound** - If available

**IMMEDIATE MANAGEMENT:**
1. **Anticoagulation**
   - Heparin bolus: 5000 units IV (or 80 units/kg)
   - Followed by infusion (18 units/kg/h)
   - Target APTT 1.5-2.5 x control

2. **Analgesia** - IV opioids
3. **Protect limb** - Keep at heart level, avoid pressure
4. **Urgent imaging**
   - CT angiography or duplex ultrasound
   - Identify level and extent of occlusion

**TREATMENT:**
- **Embolectomy** - Fogarty catheter for embolic occlusion
- **Thrombectomy** - Surgical or catheter-based
- **Thrombolysis** - Catheter-directed for thrombotic occlusion
- **Bypass** - If unsuitable for thrombectomy/thrombolysis
- **Amputation** - If irreversible ischaemia

**PROGNOSIS:**
- Limb salvage: 80-90% if treated within 6 hours
- Decreases to <50% after 12 hours
- Mortality: 15-30% (often comorbid patients)

**Evidence:** ESVS 2022 Guidelines, Rutherford classification""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified acute limb ischaemia - limb-threatening emergency",
                    "Applied 6P clinical assessment framework",
                    "Prioritized immediate anticoagulation",
                    "Time-critical intervention required"
                ],
                capabilities_used=["vascular_emergency_management", "arterial_disease_assessment"],
                metadata={
                    "urgency": "emergency",
                    "condition": "acute_limb_ischaemia",
                    "time_critical": "6_hours",
                    "intervention": "embolectomy_or_revascularization"
                }
            )

        # Acute mesenteric ischaemia
        elif any(term in query_lower for term in [
            "mesenteric ischaemia", "acute mesenteric", "bowel ischaemia", "mesenteric artery"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**ACUTE MESENTERIC ISCHAEMIA - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Urgent surgical assessment**
- **High mortality (50-80%)** - early intervention critical
- **Requires CT angiography for diagnosis**

**CLINICAL PRESENTATION:**
- **Severe abdominal pain out of proportion to examination**
- Nausea, vomiting
- History of atrial fibrillation (arterial embolus)
- Blood in stool (late sign - bowel infarction)
- Metabolic acidosis (elevated lactate)

**CAUSES:**
- **Arterial embolus** (50%) - usually from atrial fibrillation
- **Arterial thrombosis** (25%) - on background of atherosclerosis
- **Mesenteric venous thrombosis** (15%)
- **Non-occlusive** (10%) - low flow state (shock, vasopressors)

**IMMEDIATE MANAGEMENT:**
1. **Resuscitation**
   - IV fluids (crystalloid/colloid)
   - Correct electrolyte abnormalities
   - Broad-spectrum antibiotics

2. **Urgent imaging**
   - **CT angiography** (investigation of choice)
   - May show: mesenteric occlusion, bowel dilation, pneumatosis

3. **Anticoagulation**
   - Heparin infusion if not actively bleeding
   - Continue if arterial embolus/thrombosis

**TREATMENT:**
- **Arterial embolus:** Embolectomy + bowel resection if infarcted
- **Arterial thrombosis:** Bypass + bowel resection if infarcted
- **Venous thrombosis:** Anticoagulation ± bowel resection
- **Second-look laparotomy** at 24-48 hours if viability uncertain

**PROGNOSIS:**
- Mortality: 50-80% overall
- Better outcomes with early diagnosis and intervention
- Delay >24 hours associated with poor prognosis

**Evidence:** ESVS 2022 Guidelines, BJS Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified acute mesenteric ischaemia - surgical emergency",
                    "Applied clinical assessment (pain out of proportion)",
                    "High mortality condition requiring urgent intervention",
                    "CT angiography required for diagnosis"
                ],
                capabilities_used=["vascular_emergency_management", "arterial_disease_assessment"],
                metadata={
                    "urgency": "emergency",
                    "condition": "acute_mesenteric_ischaemia",
                    "mortality_risk": "very_high",
                    "intervention": "surgical_exploration"
                }
            )

        # Vascular trauma
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**VASCULAR TRAUMA - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Control of haemorrhage is priority**
- **Urgent vascular surgery involvement**
- **Consider major trauma protocol**

**CLINICAL PRESENTATION:**
- **Hard signs of vascular injury:**
  - Active haemorrhage
  - Expanding haematoma
  - Pulse deficit
  - Bruit/thrill
  - Distal ischaemia (pain, pallor, paralysis)
- **Soft signs:**
  - History of significant bleeding
  - Proximity to major vessel
  - Neurological deficit

**IMMEDIATE MANAGEMENT:**
1. **ABC approach**
   - Control major haemorrhage (direct pressure, tourniquet)
   - Secure airway and breathing
   - Large bore cannulas x2

2. **Resuscitation**
   - IV fluids/blood products
   - Cross-match 4 units
   - Consider massive transfusion protocol

3. **Imaging**
   - **CT angiography** if patient stable
   - Intra-op angiography if unstable
   - Consider duplex for penetrating limb trauma

4. **Definitive management**
   - **Repair** (primary repair, patch angioplasty)
   - **Bypass** (interposition graft)
   - **Ligation** (last resort, usually non-critical vessels)
   - **Endovascular** (stent graft, coil embolization)

**SPECIFIC INJURIES:**
- **Carotid:** Repair if possible, consider shunting
- **Subclavian/axillary:** Repair or bypass
- **Brachial/femoral:** Repair preferred
- **Popliteal:** Repair, vein graft preferred
- **Tibial:** Consider ligation if single-vessel injury

**Evidence:** SVS 2022 Guidelines, EAST Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified vascular trauma - surgical emergency",
                    "Applied hard vs soft signs classification",
                    "Prioritized haemorrhage control",
                    "Multiple repair options available"
                ],
                capabilities_used=["vascular_emergency_management", "vascular_trauma_assessment"],
                metadata={
                    "urgency": "emergency",
                    "condition": "vascular_trauma",
                    "priority": "haemorrhage_control",
                    "intervention": "surgical_repair"
                }
            )

    def _handle_aneurysm_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle aortic aneurysm queries"""
        query_lower = query.lower()

        # Screening queries
        if any(term in query_lower for term in [
            "screen", "screening", "should i be screened", "who needs screening"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**ABDOMINAL AORTIC ANEURYSM (AAA) SCREENING**

**WHO SHOULD BE SCREENED?**

**NICE NG156 (2020) Recommendations:**
- **Men aged 65-75** - One-time ultrasound screening
- **Men >75** - Consider screening if not previously done
- **Women** - Routine screening NOT recommended
  - Consider if family history of AAA
  - Consider if risk factors present

**HIGH-RISK GROUPS (Consider Earlier Screening):**
- Family history of AAA (1st degree relative)
- Smoking history
- Hypertension
- Other arterial disease (PAD, carotid stenosis)
- Connective tissue disorders (Marfan, Ehlers-Danlos)

**SCREENING METHOD:**
- **Ultrasound** abdomen - non-invasive, accurate
- Measures aortic diameter

**THRESHOLDS:**
- **<3.0 cm:** Normal - no follow-up needed
- **3.0-4.4 cm:** Repeat ultrasound in 12 months
- **4.5-5.4 cm:** Repeat ultrasound in 3-6 months
- **≥5.5 cm (or ≥5.0 cm in women):** Refer to vascular surgery

**EVIDENCE:** UK National AAA Screening Programme, NICE NG156""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified AAA screening query",
                    "Applied NICE NG156 screening recommendations",
                    "Risk-stratified follow-up based on aneurysm size"
                ],
                capabilities_used=["aneurysm_evaluation_and_management"],
                metadata={
                    "topic": "aaa_screening",
                    "guideline": "nice_ng156"
                }
            )

        # Surveillance intervals
        elif any(term in query_lower for term in [
            "surveillance", "follow up", "monitoring", "how often", "interval"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**AAA SURVEILLANCE INTERVALS**

**NICE NG156 RECOMMENDATIONS:**

| Aortic Diameter | Surveillance Interval | Action |
|----------------|----------------------|--------|
| <3.0 cm | No follow-up | Normal |
| 3.0-3.9 cm | 12 months | Routine surveillance |
| 4.0-4.4 cm | 12 months | Consider vascular referral |
| 4.5-4.9 cm | 6 months | Vascular referral recommended |
| 5.0-5.4 cm | 3 months | Refer to vascular surgery |
| ≥5.5 cm (men) | Immediate | Refer for repair consideration |
| ≥5.0 cm (women) | Immediate | Refer for repair consideration |

**ADDITIONAL FACTORS:**
- **Rapid growth** (>1 cm/year) - Refer urgently
- **Symptomatic aneurysm** - Refer immediately (emergency)
- **Family history** - Consider lower threshold for referral
- **Women** - Repair at smaller sizes (higher rupture risk)

**REPAIR THRESHOLDS:**
- **Men:** ≥5.5 cm
- **Women:** ≥5.0 cm (higher rupture risk at smaller sizes)
- **Rapid growth** (>1 cm/year) at any size

**EVIDENCE:** NICE NG156 (2020), ESVS 2019 Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified AAA surveillance query",
                    "Applied size-based surveillance intervals",
                    "Considered sex-specific differences"
                ],
                capabilities_used=["aneurysm_evaluation_and_management"],
                metadata={
                    "topic": "aaa_surveillance",
                    "guideline": "nice_ng156"
                }
            )

        # Treatment options
        elif any(term in query_lower for term in [
            "treatment", "repair", "surgery", "evar", "stent graft", "open repair"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**AAA TREATMENT OPTIONS**

**REPAIR INDICATIONS:**
- **Diameter ≥5.5 cm** (men) or ≥5.0 cm (women)
- **Rapid growth** (>1 cm/year)
- **Symptomatic** (pain, rupture - emergency)
- **Rupture** - surgical emergency

**TREATMENT OPTIONS:**

**1. EVAR (Endovascular Aneurysm Repair)**
- **Procedure:** Stent graft inserted via femoral arteries
- **Advantages:**
  - Lower perioperative mortality (1-2% vs 4-5%)
  - Shorter hospital stay (2-5 days vs 7-14 days)
  - Faster recovery
- **Disadvantages:**
  - Requires suitable anatomy (neck length, angulation)
  - Requires lifelong surveillance (risk of endoleak)
  - May require reintervention (10-15%)
  - Not suitable for all anatomies

**2. Open Surgical Repair**
- **Procedure:** Laparotomy, graft replacement of aneurysmal segment
- **Advantages:**
  - Durable repair (low reintervention rate)
  - No ongoing imaging required
  - Suitable for all anatomies
- **Disadvantages:**
  - Higher perioperative mortality (4-5%)
  - Longer hospital stay (7-14 days)
  - Longer recovery (6-12 weeks)
  - Higher morbidity (cardiac, respiratory, renal)

**CHOOSING BETWEEN EVAR AND OPEN:**

**Factors favoring EVAR:**
- Age >70 years
- Significant comorbidities (cardiac, respiratory, renal)
- Suitable anatomy (adequate neck, no severe tortuosity)
- Life expectancy <10 years

**Factors favoring Open:**
- Younger patient (<65 years)
- Good surgical risk
- Unsuitable anatomy for EVAR
- Connective tissue disorder (Marfan, Ehlers-Danlos)
- Long life expectancy

**EVIDENCE:** ESVS 2019 Guidelines, NICE NG156, EVAR-1 Trial""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified AAA treatment query",
                    "Compared EVAR vs open repair options",
                    "Considered patient factors for treatment selection"
                ],
                capabilities_used=["aneurysm_evaluation_and_management"],
                metadata={
                    "topic": "aaa_treatment",
                    "guideline": "esvs_2019"
                }
            )

        # General aneurysm information
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**ABDOMINAL AORTIC ANEURYSM (AAA)**

**WHAT IS IT?**
- Abnormal dilation of the abdominal aorta
- Defined as diameter ≥3.0 cm (or >50% normal)
- Most occur infrarenal (below renal arteries)

**RISK FACTORS:**
- **Age** - Risk increases with age
- **Sex** - Men:Women 4:1 to 6:1
- **Smoking** - Strong modifiable risk factor
- **Hypertension**
- **Family history** - 15-25% have affected 1st degree relative
- **Other arterial disease** - PAD, carotid stenosis
- **Hyperlipidaemia**

**NATURAL HISTORY:**
- **Small aneurysms (3.0-4.4 cm):** Rupture risk <1%/year
- **Medium (4.5-5.4 cm):** Rupture risk 1-5%/year
- **Large (≥5.5 cm):** Rupture risk 10-20%/year
- **Growth rate:** Average 2-3 mm/year

**SYMPTOMS:**
- Usually **asymptomatic** until large or ruptured
- May have abdominal or back pain if expanding
- Rupture: severe pain, collapse, hypotension

**DIAGNOSIS:**
- **Ultrasound** - screening and surveillance
- **CT angiography** - preoperative planning
- **MRI** - alternative if CT contraindicated

**MANAGEMENT:**
- **Small (<5.5 cm):** Surveillance ultrasound
- **Large (≥5.5 cm):** Repair (EVAR or open)
- **Rupture:** Emergency surgery

**PREVENTION:**
- Stop smoking
- Blood pressure control
- Statin therapy
- Antiplatelet (aspirin)

**EVIDENCE:** ESVS 2019 Guidelines, NICE NG156""",
                confidence=0.90,
                reasoning_trace=[
                    "Provided general AAA information",
                    "Explained natural history and risk factors",
                    "Outlined management approach"
                ],
                capabilities_used=["aneurysm_evaluation_and_management"],
                metadata={
                    "topic": "aaa_general",
                    "guideline": "esvs_2019"
                }
            )

    def _handle_carotid_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle carotid artery disease queries"""
        query_lower = query.lower()

        # Symptomatic carotid stenosis
        if any(term in query_lower for term in [
            "symptomatic", "tia", "transient ischemic", "stroke", "amaurosis fugax",
            "retinal embolus", "central retinal artery"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**SYMPTOMATIC CAROTID STENOSIS**

**DEFINITION:**
- Carotid stenosis in territory of recent (<6 months) cerebral ischaemic event
- Events: TIA, stroke, amaurosis fugax, retinal embolus

**IMMEDIATE MANAGEMENT:**
1. **Urgent imaging** - CT/MRI brain to exclude haemorrhage
2. **Carotid imaging** - Duplex ultrasound ± CT angiography
3. **Risk factor modification**
   - Start antiplatelet (aspirin, clopidogrel, or dual for TIA)
   - Statin (high-intensity: atorvastatin 80mg)
   - BP control (target <130/80 mmHg)
   - Smoking cessation
4. **Urgent vascular referral** - within 7 days of event

**INDICATIONS FOR CAROTID ENDARTERECTOMY (CEA):**

**NICE NG128 RECOMMENDATIONS:**
- **50-69% stenosis:** Consider CEA if event within last 7 days
- **70-99% stenosis:** CEA recommended if event within last 7 days

**TIMING:**
- **Within 7 days** of index event (optimal)
- **Within 2 weeks** (acceptable)
- **>6 months:** Not recommended (benefit unclear)

**CAROTID ARTERY STENTING (CAS):**
- Consider if:
  - CEA not suitable (e.g., previous neck surgery/radiation)
  - High surgical risk
  - Lesion not accessible surgically
- **Not recommended** if symptomatic and >70 years

**BENEFITS OF CEA:**
- Reduces stroke risk from ~20% to ~5% over 5 years
- Number needed to treat: ~10 to prevent one stroke

**EVIDENCE:** NICE NG128 (2023), ESVS 2023 Guidelines, NASCET Trial""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified symptomatic carotid stenosis query",
                    "Applied NICE NG128 recommendations",
                    "Prioritized urgent intervention within 7 days"
                ],
                capabilities_used=["carotid_disease_management"],
                metadata={
                    "topic": "symptomatic_carotid_stenosis",
                    "guideline": "nice_ng128",
                    "time_sensitive": "7_days"
                }
            )

        # Asymptomatic carotid stenosis
        elif any(term in query_lower for term in [
            "asymptomatic", "incidental", "found on scan", "routine", "no symptoms"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**ASYMPTOMATIC CAROTID STENOSIS**

**DEFINITION:**
- Carotid stenosis detected incidentally
- No history of TIA, stroke, or retinal ischaemia in ipsilateral territory

**MANAGEMENT:**

**1. OPTIMAL MEDICAL THERAPY (FIRST-LINE):**
- **Antiplatelet:** Aspirin 75mg daily OR clopidogrel 75mg daily
- **Statin:** High-intensity (atorvastatin 80mg or rosuvastatin 40mg)
- **BP control:** Target <130/80 mmHg
- **Lifestyle:**
  - Smoking cessation
  - Weight loss if overweight
  - Regular exercise
  - Healthy diet (Mediterranean)

**2. CAROTID ENDARTERECTOMY (CEA):**
- **Consider for:**
  - Men aged 65-75 years
  - Stenosis 70-99% on duplex
  - Low surgical risk
  - Life expectancy >5 years
  - Surgical risk <3%

- **NOT recommended for:**
  - Stenosis <50%
  - Women (benefit less clear)
  - Age >75 years (higher surgical risk)
  - Significant comorbidities

**3. SURVEILLANCE:**
- Duplex ultrasound at 6-12 months
- If stable: annual duplex
- If progressing: Consider intervention

**RISK OF STROKE:**
- With optimal medical therapy: ~1-2%/year
- With CEA: Reduces to ~0.5%/year in selected patients
- Number needed to treat: ~30 to prevent one stroke (vs ~10 for symptomatic)

**EVIDENCE:** NICE NG128 (2023), ESVS 2023 Guidelines, ACST-2 Trial""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified asymptomatic carotid stenosis query",
                    "Prioritized optimal medical therapy",
                    "CEA only beneficial in highly selected patients"
                ],
                capabilities_used=["carotid_disease_management"],
                metadata={
                    "topic": "asymptomatic_carotid_stenosis",
                    "guideline": "nice_ng128"
                }
            )

        # General carotid information
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**CAROTID ARTERY DISEASE**

**WHAT IS IT?**
- Atherosclerotic plaque in carotid arteries
- Can cause TIA or stroke if emboli to brain
- Most common at carotid bifurcation

**SYMPTOMS:**
- **Asymptomatic** (most common)
- **TIA:** Transient focal neurological deficit
  - Amaurosis fugax (transient vision loss)
  - Aphasia
  - Hemiparesis
  - Hemisensory loss
- **Stroke:** Persistent neurological deficit

**DIAGNOSIS:**
- **Duplex ultrasound** - first-line imaging
- **CT angiography** - preoperative planning
- **MR angiography** - alternative to CT

**STENOSIS GRADING:**
- **Normal:** <50%
- **Moderate:** 50-69%
- **Severe:** 70-99%
- **Occlusion:** 100%

**MANAGEMENT:**
- **All patients:**
  - Optimal medical therapy (antiplatelet, statin, BP control)
  - Lifestyle modification (smoking, diet, exercise)

- **Symptomatic 50-99%:**
  - CEA recommended if within 7 days of event
  - CAS considered if CEA not suitable

- **Asymptomatic 70-99%:**
  - Consider CEA in highly selected patients
  - Optimal medical therapy for most

**CAROTID ENDARTERECTOMY (CEA):**
- Surgical removal of plaque
- Reduces stroke risk in symptomatic patients
- Perioperative stroke risk: 2-3%
- Perioperative death risk: 1-2%

**EVIDENCE:** NICE NG128 (2023), ESVS 2023 Guidelines""",
                confidence=0.88,
                reasoning_trace=[
                    "Provided general carotid disease information",
                    "Explained diagnosis and grading",
                    "Outlined management approach"
                ],
                capabilities_used=["carotid_disease_management"],
                metadata={
                    "topic": "carotid_general",
                    "guideline": "nice_ng128"
                }
            )

    def _handle_pad_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle peripheral arterial disease queries"""
        query_lower = query.lower()

        # Critical limb ischaemia
        if any(term in query_lower for term in [
            "critical limb ischaemia", "cli", "rest pain", "gangrene", "tissue loss"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**CRITICAL LIMB ISCHAEMIA (CLI)**

**DEFINITION:**
- Rest pain >2 weeks OR tissue loss (ulcer/gangrene)
- Plus objective evidence of arterial disease (ABPI <0.4 or pressure <50 mmHg)

**IMMEDIATE MANAGEMENT:**
1. **Pain control**
   - Severe rest pain requires strong opioids
   - Consider nerve block if pain intractable

2. **Urgent vascular referral**
   - Vascular imaging within 1-2 weeks
   - Consider revascularization

3. **Wound care**
   - Protect tissue loss from infection
   - Debridement if necrotic tissue
   - Antibiotics if infection present

4. **Risk factor modification**
   - Smoking cessation (critical)
   - Statin (high-intensity)
   - Antiplatelet therapy
   - BP control
   - Diabetes control

**REVASULARIZATION OPTIONS:**

**1. Angioplasty (PTA)**
- First-line for TASC II A, B, C lesions
- Minimal access, local anaesthetic
- Lower initial morbidity/mortality
- May require repeat procedures

**2. Bypass surgery**
- TASC II D lesions (extensive disease)
- Long occlusions not suitable for angioplasty
- More durable for long-segment disease
- Higher perioperative risk

**3. Hybrid procedures**
- Combine angioplasty and surgical bypass
- Used in complex multilevel disease

**MAJOR AMPUTATION:**
- Considered if:
  - Unrevascularizable disease
  - Extensive tissue loss/gangrene
  - Uncontrollable infection
  - Intractable rest pain
- Below-knee amputation (BKA) preferred if possible
- Above-knee amputation (AKA) if more extensive disease

**PROGNOSIS:**
- Without revascularization: 25% amputation, 25% death at 1 year
- With successful revascularization: Limb salvage 70-80% at 1 year

**EVIDENCE:** ESVS 2023 Guidelines, NICE NG145""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified critical limb ischaemia",
                    "Applied revascularization pathway",
                    "Considered angioplasty vs bypass options"
                ],
                capabilities_used=["peripheral_arterial_disease_treatment"],
                metadata={
                    "urgency": "urgent",
                    "condition": "critical_limb_ischaemia",
                    "intervention": "revascularization"
                }
            )

        # Intermittent claudication
        elif any(term in query_lower for term in [
            "claudication", "pain walking", "calf pain", "leg pain walking",
            "intermittent"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**INTERMITTENT CLAUDICATION**

**WHAT IS IT?**
- Reproducible muscle pain on exercise
- Relieved by rest (usually within 10 minutes)
- Caused by arterial insufficiency
- Most commonly calf pain (popliteal disease)

**DIAGNOSIS:**
- **Clinical history** - typical claudication distance
- **ABPI** (Ankle Brachial Pressure Index)
  - 0.9-1.3: Normal
  - 0.7-0.9: Borderline/mild disease
  - 0.5-0.7: Moderate disease
  - <0.5: Severe disease
- **Duplex ultrasound** - localize disease

**INITIAL MANAGEMENT (CONSERVATIVE):**

**1. Supervised Exercise Programme**
- **FIRST-LINE treatment** for all patients
- 30 minutes, 3x/week for 12 weeks
- Walk to pain, rest, walk again
- Improves walking distance by 150-200%

**2. Risk Factor Modification**
- **Smoking cessation** - single most important intervention
- **Statin** - Atorvastatin 80mg or rosuvastatin 40mg
- **Antiplatelet** - Aspirin 75mg or clopidogrel 75mg
- **BP control** - Target <130/80 mmHg
- **Diabetes control** - HbA1c <48 mmol/mol

**3. Medications**
- **Cilostazol 100mg BD** - Consider if clopidogrel contraindicated
  - Improves walking distance by 50-100%
  - Contraindicated in heart failure
- **Naftidrofuryl** - Alternative if cilostazol not tolerated
- **Avoid beta-blockers** (worsen symptoms - theoretical)

**REVASULARIZATION (IF CONSERVATIVE FAILS):**
- Indicated if:
  - Inadequate response to conservative therapy (3-6 months)
  - Severe limitation of lifestyle/occupation
  - Critical limb ischaemia develops

**Options:**
- Angioplasty (most common)
- Bypass surgery (for extensive disease)

**PROGNOSIS:**
- Benign natural history
- Only 10-20% progress to CLI over 5 years
- 5-10% require major amputation over 5 years
- Cardiovascular events (MI, stroke) are main risk

**EVIDENCE:** NICE NG145 (2019), ESVS 2023 Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified intermittent claudication query",
                    "Prioritized conservative management first",
                    "Revascularization only if conservative fails"
                ],
                capabilities_used=["peripheral_arterial_disease_treatment"],
                metadata={
                    "topic": "intermittent_claudication",
                    "guideline": "nice_ng145"
                }
            )

        # General PAD information
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**PERIPHERAL ARTERIAL DISEASE (PAD)**

**WHAT IS IT?**
- Atherosclerotic narrowing of peripheral arteries
- Most commonly affects lower limbs
- Affects 15-20% of >70 year olds

**RISK FACTORS:**
- **Smoking** - strongest modifiable risk factor
- **Diabetes** - 2-4x increased risk
- **Hypertension**
- **Hyperlipidaemia**
- **Age** - risk increases with age
- **Family history**

**CLASSIFICATION:**

**1. Asymptomatic**
- No symptoms
- May have abnormal ABPI

**2. Intermittent Claudication**
- Muscle pain on exercise
- Relieved by rest
- Most common presentation

**3. Critical Limb Ischaemia**
- Rest pain OR tissue loss
- Evidence of arterial disease
- Limb-threatening

**DIAGNOSIS:**
- **ABPI** - initial assessment
- **Duplex ultrasound** - localize disease
- **CT angiography** - preoperative planning
- **MR angiography** - alternative

**MANAGEMENT:**
- **All patients:**
  - Smoking cessation
  - Statin therapy
  - Antiplatelet
  - BP control
  - Supervised exercise

- **Claudication:**
  - Conservative management first
  - Revascularization if lifestyle limiting

- **Critical ischaemia:**
  - Urgent vascular referral
  - Revascularization (angioplasty or bypass)
  - Amputation if unrevascularizable

**PROGNOSIS:**
- Claudication: benign course, 10-20% develop CLI
- CLI: 25% mortality, 25% amputation at 1 year without revascularization

**EVIDENCE:** NICE NG145, ESVS 2023 Guidelines""",
                confidence=0.88,
                reasoning_trace=[
                    "Provided general PAD information",
                    "Explained classification and severity",
                    "Outlined management approach"
                ],
                capabilities_used=["peripheral_arterial_disease_treatment"],
                metadata={
                    "topic": "pad_general",
                    "guideline": "nice_ng145"
                }
            )

    def _handle_dvt_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle DVT/venous thromboembolism queries"""
        query_lower = query.lower()

        # Acute DVT diagnosis
        if any(term in query_lower for term in [
            "diagnose", "diagnosis", "do i have", "suspected", "possible",
            "wells score", "d-dimer", "compression ultrasound"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**DEEP VEIN THROMBOSIS (DVT) - DIAGNOSIS**

**CLINICAL ASSESSMENT:**

**WELLS SCORE FOR DVT:**

| Feature | Points |
|---------|--------|
| Active cancer | 1 |
| Paralysis/paresis/immobilization | 1 |
| Bedridden >3 days or major surgery <12 weeks | 1 |
| Localized tenderness along deep venous system | 1 |
| Entire leg swollen | 1 |
| Calf swelling >3cm than asymptomatic side | 1 |
| Pitting oedema | 1 |
| Collateral superficial veins | 1 |
| Previous DVT | 1 |
| Alternative diagnosis as likely as DVT | -2 |

**INTERPRETATION:**
- **Score ≤0:** Low probability (DVT likely in <5%)
- **Score 1-2:** Moderate probability (DVT likely in ~17%)
- **Score ≥3:** High probability (DVT likely in ~75%)

**INVESTIGATIONS:**

**1. D-Dimer**
- **Negative:** DVT excluded (if low/moderate Wells)
- **Positive:** Requires imaging (ultrasound)

**2. Compression Ultrasound**
- Gold standard for diagnosis
- Compressibility of vein assessed
- Proximal veins (femoral, popliteal) - most important
- Distal veins (calf) - less clinically significant

**3. CT Venography**
- If ultrasound inconclusive
- Suspected iliac/IVC thrombosis

**IMMEDIATE MANAGEMENT (WHILE AWAITING CONFIRMATION):**
- **DO NOT START anticoagulation** until diagnosis confirmed
- **Compression stockings** if DVT suspected
- **Analgesia** for pain

**EVIDENCE:** NICE NG158 (2023), RCP Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified DVT diagnosis query",
                    "Applied Wells score assessment",
                    "Outlined diagnostic pathway"
                ],
                capabilities_used=["dvt_diagnosis_and_management"],
                metadata={
                    "topic": "dvt_diagnosis",
                    "guideline": "nice_ng158"
                }
            )

        # DVT treatment
        elif any(term in query_lower for term in [
            "treatment", "treat", "anticoagulation", "blood thinner", "warfarin",
            "apixaban", "rivaroxaban", "dabigatran", "edoxaban", "dvt treatment"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**DVT TREATMENT**

**IMMEDIATE MANAGEMENT:**

**1. Anticoagulation (START IMMEDIATELY)**

**DIRECT ORAL ANTICOAGULANTS (DOACs) - FIRST-LINE:**

| DOAC | Dose for DVT | Duration |
|------|--------------|----------|
| **Apixaban** | 10mg BD x7 days, then 5mg BD | ≥3 months |
| **Rivaroxaban** | 15mg BD x21 days, then 20mg OD | ≥3 months |
| **Dabigatran** | 150mg BD (after 5-10 days parenteral) | ≥3 months |
| **Edoxaban** | 60mg OD (after 5 days parenteral) | ≥3 months |

**Contraindications to DOACs:**
- Severe renal impairment (CrCl <15-30 mL/min depending on DOAC)
- Antiphospholipid syndrome (warfarin preferred)
- Pregnancy (warfarin/LMWH preferred)

**WARFARIN (ALTERNATIVE):**
- Target INR 2.0-3.0
- Requires bridging with LMWH until INR therapeutic for 24 hours
- Requires regular INR monitoring

**2. Compression Stockings**
- **Class 2 (18-24 mmHg)**
- Wear on affected leg
- Put on in morning, remove at night
- Continue for ≥2 years if post-thrombotic syndrome develops

**3. Analgesia**
- Paracetamol ± codeine for pain
- Avoid NSAIDs (increase bleeding risk)

**4. Elevate Leg**
- When sitting/lying
- Avoid prolonged standing

**DURATION OF ANTICOAGULATION:**

**Provoked DVT (clear trigger):**
- **3 months** standard duration
- No extended anticoagulation needed

**Unprovoked DVT (no clear trigger):**
- **≥3 months** minimum
- Consider extending if:
  - High risk of recurrence (male, residual thrombosis)
  - Low bleeding risk
  - Patient preference

**Recurrent Unprovoked DVT:**
- Consider **indefinite** anticoagulation if low bleeding risk

**EVIDENCE:** NICE NG158 (2023), CHEST Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified DVT treatment query",
                    "Prioritized DOACs as first-line",
                    "Risk-stratified duration based on provoked vs unprovoked"
                ],
                capabilities_used=["dvt_diagnosis_and_management"],
                metadata={
                    "topic": "dvt_treatment",
                    "guideline": "nice_ng158"
                }
            )

        # Pulmonary embolism
        elif any(term in query_lower for term in [
            "pe", "pulmonary embolism", "lung clot", "breath clot", "embolism"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**PULMONARY EMBOLISM (PE)**

**DEFINITION:**
- Venous thrombus embolizes to pulmonary arterial system
- Spectrum from asymptomatic to cardiovascular collapse

**CLINICAL PRESENTATION:**
- **Dyspnoea** (most common)
- **Pleuritic chest pain**
- **Haemoptysis** (less common)
- **Tachycardia**, tachypnoea
- **Hypoxia**
- **Hypotension, shock** (massive PE)

**RISK STRATIFICATION:**

**1. Low Risk (PESI Class I-II):**
- Haemodynamically stable
- No right ventricular strain on echo/CT
- Troponin normal

**2. Intermediate Risk (PESI Class III-IV):**
- Haemodynamically stable
- Right ventricular strain on echo/CT
- Troponin elevated ±

**3. High Risk (Massive PE):**
- Haemodynamically unstable
- SBP <90 mmHg or drop >40 mmHg
- Signs of shock

**DIAGNOSIS:**
- **CT Pulmonary Angiography (CTPA)** - gold standard
- **V/Q scan** - if CT contraindicated (renal impairment, contrast allergy)
- **D-dimer** - if low clinical probability

**TREATMENT:**

**Low/Intermediate Risk:**
- **Anticoagulation** (same as DVT)
- **DOACs first-line** (apixaban, rivaroxaban)
- Admit to hospital for intermediate risk
- Consider home treatment for low risk

**High Risk (Massive PE):**
- **Thrombolysis** (alteplase 10mg IV bolus, then 90mg over 2 hours)
  - Contraindicated if high bleeding risk
- Consider **surgical embolectomy** if thrombolysis contraindicated
- Consider **percutaneous mechanical thrombectomy**
- Admit to ICU/HDU

**DURATION:**
- **Provoked PE:** 3 months
- **Unprovoked PE:** ≥3 months, consider extended if recurrent/unprovoked

**PROGNOSIS:**
- Mortality: 10-15% overall (higher if massive)
- Recurrence: 5-10% after stopping anticoagulation
- Chronic thromboembolic pulmonary hypertension (CTEPH) - 4% long-term

**EVIDENCE:** NICE NG158 (2023), ESC 2023 Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified pulmonary embolism query",
                    "Risk-stratified into low/intermediate/high",
                    "Tailored treatment based on risk category"
                ],
                capabilities_used=["dvt_diagnosis_and_management"],
                metadata={
                    "topic": "pulmonary_embolism",
                    "guideline": "nice_ng158"
                }
            )

        # VTE prevention
        elif any(term in query_lower for term in [
            "prevent", "prevention", "prophylaxis", "avoid", "risk"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**VENOUS THROMBOEMBOLISM (VTE) PROPHYLAXIS**

**HOSPITALIZED PATIENTS:**

**Medical Patients:**
- **LMWH** (tinzaparin 4500 units OD or enoxaparin 40mg OD)
- Consider **fondaparinux** 2.5mg SC OD if renal impairment/heparin-induced thrombocytopenia
- Continue until mobile or discharge

**Surgical Patients:**

**Low Risk:**
- Early mobilization
- Mechanical prophylaxis (compression stockings, intermittent pneumatic compression)

**Moderate-High Risk:**
- **LMWH** (dose adjusted for renal function)
- Start 12 hours pre-op or 12-24 hours post-op
- Continue for 28-35 days for major cancer surgery
- Continue for shorter duration (5-7 days) for other major surgery

**HIGH BLEEDING RISK:**
- Mechanical prophylaxis initially
- Pharmacological prophylaxis when bleeding risk acceptable

**CONTRAINDICATIONS TO PHARMACOLOGICAL PROPHYLAXIS:**
- Active bleeding
- Severe thrombocytopenia (platelets <50 x 10^9/L)
- Severe renal impairment (LMWH)
- Heparin-induced thrombocytopenia (HIT)

**GENERAL MEASURES:**
- Adequate hydration
- Early mobilization
- Avoid dehydration
- Leg exercises when immobile
- Compression stockings for at-risk patients

**OUTPATIENT PROPHYLAXIS:**
- Consider for high-risk outpatients (cancer chemotherapy)
- LMWH or DOAC (rivaroxaban 10mg OD for 6 months)
- Individualized decision based on risk-benefit

**EVIDENCE:** NICE NG89 (2018), ACCP Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified VTE prevention query",
                    "Stratified by medical vs surgical patients",
                    "Considered bleeding risk"
                ],
                capabilities_used=["dvt_diagnosis_and_management"],
                metadata={
                    "topic": "vte_prophylaxis",
                    "guideline": "nice_ng89"
                }
            )

        # General DVT information
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**DEEP VEIN THROMBOSIS (DVT)**

**WHAT IS IT?**
- Blood clot in deep veins (usually leg)
- Can embolize to lungs → Pulmonary Embolism (PE)
- DVT + PE = VTE (Venous Thromboembolism)

**RISK FACTORS:**
- **Immobilization** - surgery, trauma, travel
- **Cancer** - active malignancy
- **Pregnancy** and postpartum
- **Oestrogen** - COCP, HRT
- **Previous VTE** - recurrence risk
- **Thrombophilia** - inherited (Factor V Leiden) or acquired (APLS)
- **Obesity** (BMI >30)
- **Age** >60 years
- **Varicose veins** (minor risk)

**SYMPTOMS:**
- **Unilateral leg swelling**
- **Pain** - calf or thigh
- **Redness, warmth**
- **Distended veins**
- May be asymptomatic

**COMPLICATIONS:**
- **Pulmonary Embolism** - most serious
- **Post-thrombotic syndrome** - chronic leg swelling, ulceration
- **Recurrence** - 5-10% after stopping anticoagulation

**DIAGNOSIS:**
- **Wells score** - risk stratification
- **D-dimer** - if low/moderate probability
- **Compression ultrasound** - confirm diagnosis

**TREATMENT:**
- **Anticoagulation** - DOACs first-line
- **Compression stockings** - prevent post-thrombotic syndrome
- **Elevate leg**
- **Analgesia**

**DURATION:**
- **Provoked:** 3 months
- **Unprovoked:** ≥3 months, consider extended

**PREVENTION:**
- Early mobilization after surgery
- Compression stockings for high risk
- Pharmacological prophylaxis for hospital patients

**EVIDENCE:** NICE NG158 (2023)""",
                confidence=0.88,
                reasoning_trace=[
                    "Provided general DVT information",
                    "Explained risk factors and complications",
                    "Outlined management approach"
                ],
                capabilities_used=["dvt_diagnosis_and_management"],
                metadata={
                    "topic": "dvt_general",
                    "guideline": "nice_ng158"
                }
            )

    def _handle_venous_disease_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle varicose veins and venous ulcer queries"""
        query_lower = query.lower()

        # Venous leg ulcer
        if any(term in query_lower for term in [
            "venous ulcer", "leg ulcer", "stasis ulcer", "varicose ulcer"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**VENOUS LEG ULCER**

**DEFINITION:**
- Chronic ulceration of lower leg due to venous insufficiency
- Most common cause of leg ulcers (70-80%)
- Associated with varicose veins, DVT, superficial venous reflux

**DIAGNOSIS:**
- **Clinical:** Typically medial gaiter area, shallow, with varicose veins
- **ABPI:** Exclude arterial disease (must be >0.8 to apply compression)
- **Duplex ultrasound:** Identify reflux, obstruction

**MANAGEMENT:**

**1. COMPRESSION THERAPY (CORNERSTONE)**

**4-Layer Bandaging:**
- Wool orthopaedic wadding
- Light compression crepe
- Light compression bandage
- Cohesive compression bandage
- Apply from toe to knee
- Change weekly

**2-Layer System:**
- Padding layer
- Coban or similar cohesive bandage
- Easier to apply than 4-layer

**Compression Hosiery:**
- Class 2 (18-24 mmHg) or Class 3 (25-35 mmHg)
- Once ulcer healed
- Prevents recurrence

**2. WOUND CARE**
- Cleanse with warm tap water or saline
- Debride slough if present
- Appropriate dressing (hydrocolloid, foam, alginate)
- No one dressing proven superior

**3. TREAT UNDERLYING VENOUS DISEASE**
- **Endovenous ablation** (laser or radiofrequency)
- **Sclerotherapy** (foam sclerotherapy)
- **Surgery** (ligation and stripping)
- Reduces recurrence rate

**4. ADJUNCTIVE MEASURES**
- **Elevate legs** when resting
- **Exercise** - calf muscle pump activation
- **Weight loss** if overweight
- **Skin care** - emollients for surrounding skin

**HEALING RATES:**
- With compression: 50-70% heal within 12 weeks
- Without compression: <20% heal
- Recurrence without treatment of underlying veins: ~50%

**COMPLICATIONS:**
- Infection (cellulitis)
- Contact dermatitis from dressings
- Malignant transformation (Marjolin's ulcer - rare)

**EVIDENCE:** NICE NG168 (2023), EWMA Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified venous leg ulcer query",
                    "Prioritized compression therapy",
                    "Considered treatment of underlying venous disease"
                ],
                capabilities_used=["venous_disease_assessment", "venous_ulcer_management"],
                metadata={
                    "topic": "venous_leg_ulcer",
                    "guideline": "nice_ng168"
                }
            )

        # Varicose veins treatment
        elif any(term in query_lower for term in [
            "varicose vein treatment", "treat varicose", "remove varicose",
            "surgery for varicose", "laser", "radiofrequency", "sclerotherapy",
            "stripping", "ablation"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**VARICOSE VEINS TREATMENT**

**INDICATIONS FOR TREATMENT:**

**NICE NG168 RECOMMENDATIONS:**
- **Symptoms:** Aching, heaviness, swelling, cramps
- **Complications:** Superficial thrombophlebitis, bleeding, ulceration
- **Cosmetic concerns** (self-funded treatment)

**CONSERVATIVE MANAGEMENT (FIRST-LINE):**
- **Compression stockings** (Class 2, 18-24 mmHg)
- **Leg elevation**
- **Regular exercise**
- **Weight loss** if overweight

**INTERVENTION OPTIONS:**

**1. ENDOVENOUS THERMAL ABLATION (FIRST-LINE)**

**Endovenous Laser Ablation (EVLA):**
- Laser fibre inserted into vein
- Thermal ablation of vein
- Local anaesthetic, day case
- Success: 90-95% at 5 years

**Radiofrequency Ablation (RFA):**
- Radiofrequency catheter
- Thermal ablation
- Local anaesthetic, day case
- Success: 85-90% at 5 years

**2. FOAM SCLEROTHERAPY**
- Chemical ablation using foam sclerosant
- Multiple injections needed
- Less invasive than thermal ablation
- Lower success rate: 70-80% at 5 years
- Useful for:
  - Recurrent varicose veins after previous surgery
  - Tortuous veins not suitable for thermal ablation

**3. SURGERY (LIGATION AND STRIPPING)**
- Traditional open surgery
- General or regional anaesthetic
- Higher morbidity than endovenous techniques
- Longer recovery
- Now reserved for:
  - Veins not suitable for endovenous treatment
  - Patient preference

**4. PHLEBECTOMY**
- Removal of superficial varicose veins
- Through small incisions
- Often combined with endovenous ablation

**PREOPERATIVE ASSESSMENT:**
- **Duplex ultrasound** - map reflux
- **Clinical assessment** - CEAP classification
- **ABPI** - exclude significant arterial disease

**POSTOPERATIVE CARE:**
- **Compression stockings** for 1-2 weeks
- **Return to normal activities** within 1-2 weeks
- **Avoid heavy lifting** for 2-4 weeks

**EVIDENCE:** NICE NG168 (2023), ESVS 2022 Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified varicose vein treatment query",
                    "Prioritized endovenous thermal ablation as first-line",
                    "Offered alternative options based on suitability"
                ],
                capabilities_used=["venous_disease_assessment"],
                metadata={
                    "topic": "varicose_vein_treatment",
                    "guideline": "nice_ng168"
                }
            )

        # General varicose veins
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**VARICOSE VEINS**

**WHAT ARE THEY?**
- Dilated, tortuous superficial veins of the leg
- Caused by venous valve incompetence
- Affects 20-30% of population

**RISK FACTORS:**
- **Family history** - strongest risk factor
- **Age** - increases with age
- **Female sex** - pregnancy increases risk
- **Obesity**
- **Prolonged standing**
- **Previous DVT**

**SYMPTOMS:**
- **Visible dilated veins** - blue/purple, bulging
- **Aching, heaviness** - worse at end of day
- **Swelling** - ankles and feet
- **Cramps, itching**
- **Restless legs**

**COMPLICATIONS:**
- **Superficial thrombophlebitis** - painful, inflamed vein
- **Bleeding** - can be significant if vein traumatized
- **Venous eczema** - red, scaly skin around ankle
- **Lipodermatosclerosis** - hardened, discoloured skin
- **Venous ulceration** - difficult to heal

**DIAGNOSIS:**
- **Clinical examination** - typically standing
- **Duplex ultrasound** - confirm reflux, map anatomy
- **Trendelenburg test** - historical (rarely used now)

**MANAGEMENT:**

**Conservative (First-Line):**
- Compression stockings (Class 2)
- Leg elevation
- Regular exercise
- Weight loss

**Interventional (If Conservative Fails):**
- Endovenous thermal ablation (laser/radiofrequency)
- Foam sclerotherapy
- Surgery (ligation and stripping)
- Phlebectomy (for superficial veins)

**WHEN TO REFER:**
- Symptomatic varicose veins affecting quality of life
- Complications (thrombophlebitis, ulceration, bleeding)
- Recurrent varicose veins after previous treatment

**EVIDENCE:** NICE NG168 (2023)""",
                confidence=0.88,
                reasoning_trace=[
                    "Provided general varicose vein information",
                    "Explained symptoms and complications",
                    "Outlined management approach"
                ],
                capabilities_used=["venous_disease_assessment"],
                metadata={
                    "topic": "varicose_veins_general",
                    "guideline": "nice_ng168"
                }
            )

    def _handle_vascular_access_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle vascular access (dialysis access) queries"""
        return DomainQueryResult(
            domain_name="vascular_surgery",
            answer="""**VASCULAR ACCESS FOR HAEMODIALYSIS**

**TYPES OF VASCULAR ACCESS:**

**1. ARTERIOVENOUS FISTULA (AVF) - FIRST-LINE**
- Surgical connection of artery to vein
- Usually radial-cephalic or brachiocephalic
- **Maturation time:** 4-6 weeks
- **Advantages:**
  - Most durable option
  - Lowest infection rate
  - Lowest thrombosis rate
  - No foreign material
- **Disadvantages:**
  - Requires surgical creation
  - Time to maturation
  - May fail to mature

**2. ARTERIOVENOUS GRAFT (AVG)**
- PTFE graft connecting artery to vein
- **Maturation time:** 2-3 weeks
- **Advantages:**
  - Faster maturation than AVF
  - Can be placed in patients with poor veins
  - Easier to cannulate
- **Disadvantages:**
  - Higher infection rate
  - Higher thrombosis rate
  - Shorter lifespan than AVF

**3. TUNNELED CATHETER**
- Silicone catheter inserted into central vein
- **Immediate use**
- **Advantages:**
  - Immediate use
  - No surgery required (just insertion)
- **Disadvantages:**
  - High infection rate
  - High thrombosis rate
  - Central stenosis risk
  - Should be temporary bridge

**PREOPERATIVE ASSESSMENT:**
- **Duplex ultrasound** - vein mapping
- **ABPI** - exclude arterial disease
- **Central vein imaging** if previous access

**CARE OF VASCULAR Access:**

**AVF/AVG:**
- **Avoid compression** - no blood pressure, IV lines, needles on access arm
- **Check thrill** daily (buzzing sensation)
- **Report concerns** - loss of thrill, pain, redness, swelling
- **Keep clean** - wash with soap and water

**Catheter:**
- **Keep dry** - no swimming
- **Dressings changed** by dialysis staff
- **Report fever** - possible line infection

**COMPLICATIONS:**

**Thrombosis:**
- Loss of thrill/pulse
- Urgent vascular review
- May require thrombectomy or thrombolysis

**Infection:**
- AVF/AVG: Rare, requires antibiotics ± surgery
- Catheter: Common, requires removal + antibiotics

**Steal Syndrome:**
- Hand ischaemia due to diversion of flow
- May require revision or ligation

**High Output Heart Failure:**
- Rare complication of large AVF
- May require banding or ligation

**EVIDANCE:** KDOQI Guidelines, VAS Guidelines""",
            confidence=0.90,
            reasoning_trace=[
                "Provided vascular access information",
                "Compared AVF vs AVG vs catheter options",
                "Outlined care and complications"
            ],
            capabilities_used=["arterial_disease_assessment"],
            metadata={
                "topic": "vascular_access",
                "guideline": "kdoqi"
            }
        )

    def _handle_raynaud_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle Raynaud's phenomenon queries"""
        query_lower = query.lower()

        # Primary vs secondary
        if any(term in query_lower for term in [
            "primary", "secondary", "raynaud's phenomenon", "raynaud's disease",
            "difference", "cause"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**RAYNAUD'S PHENOMENON: PRIMARY VS SECONDARY**

**PRIMARY RAYNAUD'S (Raynaud's Disease):**
- **No underlying cause** identified
- **More common** (80-90% of cases)
- Typically younger age of onset (<30 years)
- Female predominance (F:M 9:1)
- Benign course
- No tissue damage

**SECONDARY RAYNAUD'S:**
- **Associated with** underlying condition
- **Less common** (10-20% of cases)
- Older age of onset (>30 years)
- May cause tissue damage (ulcers, gangrene)

**CAUSES OF SECONDARY RAYNAUD'S:**

**Connective Tissue Disease (90%):**
- **Systemic sclerosis** (most common)
- **SLE** (lupus)
- **Rheumatoid arthritis**
- **Sjögren's syndrome**
- **Dermatomyositis/polymyositis**

**Other Causes:**
- **Vibration white finger** (occupational)
- **Atherosclerosis** (proximal arterial disease)
- **Thoracic outlet syndrome**
- **Drugs** (beta-blockers, ergotamines)
- **Hyperviscosity** (cryoglobulins)

**DIFFERENTIATING FEATURES:**

| Feature | Primary | Secondary |
|---------|---------|-----------|
| Age of onset | <30 years | >30 years |
| Symmetry | Bilateral | May be unilateral |
| Tissue damage | Rare | Common |
| Nailfold capillaries | Normal | Abnormal |
| Autoantibodies | Negative | Positive (ANA, etc.) |

**INVESTIGATIONS FOR SUSPECTED SECONDARY:**
- **FBC, ESR** - inflammatory markers
- **Autoantibodies** - ANA, ENA, rheumatoid factor
- **Nailfold capillaroscopy** - assess capillary loops
- **Thermography** - assess temperature recovery
- **Doppler/angiography** - exclude proximal arterial disease

**EVIDENCE:** VAS Guidelines, EULAR Recommendations""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified Raynaud's primary vs secondary query",
                    "Compared features of both types",
                    "Outlined causes of secondary Raynaud's"
                ],
                capabilities_used=["arterial_disease_assessment"],
                metadata={
                    "topic": "raynauds_phenomenon",
                    "guideline": "eular"
                }
            )

        # Raynaud's treatment
        elif any(term in query_lower for term in [
            "treatment", "manage", "help", "medication", "calcium channel"
        ]):
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**RAYNAUD'S PHENOMENON TREATMENT**

**GENERAL MEASURES (FIRST-LINE):**

**1. Keep Warm**
- **Gloves** - warm when outside
- **Socks** - keep feet warm
- **Layers** - wear multiple layers
- **Keep whole body warm** - not just hands

**2. Avoid Triggers**
- Cold exposure
- Emotional stress
- Smoking (cessation critical)
- Caffeine
- Vibration (power tools, etc.)
- Beta-blockers (may exacerbate)

**3. Lifestyle**
- Regular exercise
- Stress management
- Avoid nicotine

**PHARMACOLOGICAL TREATMENT:**

**CALCIUM CHANNEL BLOCKERS (FIRST-LINE):**
- **Nifedipine:** 30-60mg OD or 10-20mg TDS
- **Amlodipine:** 5-10mg OD
- **Diltiazem:** 60-120mg TDS
- Reduces frequency/severity by 50-70%
- Side effects: Headache, flushing, ankle swelling

**OTHER OPTIONS (IF CCB INEFFECTIVE):**

**Topical Nitrates:**
- Glyceryl trinitrate 1% cream
- Apply to affected area before cold exposure
- Side effects: Headache, hypotension

**Phosphodiesterase-5 Inhibitors:**
- Sildenafil 20mg TDS
- For severe secondary Raynaud's
- Improves digital ulcer healing

**Iloprost (Prostacyclin):**
- IV infusion for severe secondary Raynaud's
- Hospital admission required
- Reduces frequency/severity of attacks

**Botulinum Toxin:**
- Injections into digital arteries
- For severe refractory cases
- Evidence limited but promising

**SURGICAL OPTIONS (LAST RESORT):**

**Digital Sympathectomy:**
- Surgical division of sympathetic nerves
- For severe refractory cases
- Risk of recurrence

**Amputation:**
- For digital gangrene
- Only if irreversible tissue damage

**MONITORING:**
- Monitor for digital ulcers
- Assess for progression of underlying disease (if secondary)
- Regular review for treatment effectiveness

**EVIDENCE:** VAS Guidelines, EULAR Recommendations""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified Raynaud's treatment query",
                    "Prioritized general measures and CCBs",
                    "Escalated treatment options"
                ],
                capabilities_used=["arterial_disease_assessment"],
                metadata={
                    "topic": "raynauds_treatment",
                    "guideline": "eular"
                }
            )

        # General Raynaud's
        else:
            return DomainQueryResult(
                domain_name="vascular_surgery",
                answer="""**RAYNAUD'S PHENOMENON**

**WHAT IS IT?**
- Episodic vasospasm of digital arteries
- Triggered by cold or emotional stress
- Colour changes: White (ischaemia) → Blue (deoxygenation) → Red (reperfusion)

**PREVALENCE:**
- Primary: 5-10% of population
- Female predominance (F:M 9:1)
- Peak onset: 15-30 years

**SYMPTOMS:**
- **Colour changes** - white, blue, red
- **Cold sensation** - affected digits
- **Numbness/tingling** - during attack
- **Pain** - throbbing on reperfusion (red phase)
- Typically affects fingers, may involve toes, nose, ears

**TRIGGERS:**
- **Cold exposure** - most common trigger
- **Emotional stress**
- **Smoking**
- **Caffeine**
- **Vibration**
- **Certain medications** - beta-blockers, ergotamines

**TYPES:**

**Primary Raynaud's:**
- No underlying cause
- Benign condition
- No tissue damage
- More common

**Secondary Raynaud's:**
- Associated with underlying condition
- Most commonly systemic sclerosis
- May cause tissue damage (ulcers, gangrene)
- More severe

**COMPLICATIONS:**
- **Digital ulcers** - painful, slow to heal
- **Gangrene** - tissue loss, may require amputation
- **Nailfold capillary changes** - in secondary

**DIAGNOSIS:**
- **Clinical** - typical history
- **Nailfold capillaroscopy** - differentiate primary vs secondary
- **Autoantibodies** - if secondary suspected
- **Thermography** - assess recovery

**MANAGEMENT:**
- **Keep warm** - gloves, socks, layers
- **Avoid triggers** - cold, stress, smoking
- **Calcium channel blockers** - first-line pharmacological
- **Treat underlying cause** - if secondary

**EVIDENCE:** VAS Guidelines, EULAR Recommendations""",
                confidence=0.87,
                reasoning_trace=[
                    "Provided general Raynaud's information",
                    "Explained primary vs secondary",
                    "Outlined management approach"
                ],
                capabilities_used=["arterial_disease_assessment"],
                metadata={
                    "topic": "raynauds_general",
                    "guideline": "eular"
                }
            )

    def _handle_general_vascular_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general vascular surgery queries"""
        return DomainQueryResult(
            domain_name="vascular_surgery",
            answer="""**VASCULAR SURGERY**

Vascular surgery is a specialty dealing with arterial and venous diseases.

**KEY CONDITIONS:**

**Arterial Disease:**
- **Peripheral arterial disease (PAD)** - leg pain on walking (claudication)
- **Aortic aneurysm** - dilation of aorta, risk of rupture
- **Carotid disease** - narrowing of carotid arteries, stroke risk
- **Acute limb ischaemia** - sudden loss of blood supply (emergency)
- **Mesenteric ischaemia** - bowel blood supply compromised

**Venous Disease:**
- **Deep vein thrombosis (DVT)** - blood clot in deep veins
- **Pulmonary embolism (PE)** - clot travels to lungs
- **Varicose veins** - dilated superficial veins
- **Venous leg ulcers** - difficult to heal ulcers
- **Chronic venous insufficiency** - leg swelling, skin changes

**Vascular Emergencies:**
- Ruptured aortic aneurysm
- Aortic dissection
- Acute limb ischaemia
- Acute mesenteric ischaemia
- Vascular trauma

**COMMON INVESTIGATIONS:**
- **Duplex ultrasound** - first-line for most vascular disease
- **CT angiography** - detailed arterial mapping
- **MR angiography** - alternative to CT
- **ABPI** - assess peripheral arterial disease

**COMMON OPERATIONS:**
- **EVAR** - endovascular aneurysm repair
- **Carotid endarterectomy** - remove plaque from carotid
- **Angioplasty/stenting** - open narrowed arteries
- **Bypass surgery** - reroute blood around blockage
- **Sclerotherapy** - treat varicose veins

**PREVENTION:**
- **Stop smoking** - single most important intervention
- **Exercise regularly** - 30 minutes, 5x/week
- **Healthy diet** - Mediterranean, low saturated fat
- **Weight control** - BMI 18.5-25
- **Blood pressure control** - <130/80 mmHg
- **Cholesterol control** - statin if indicated
- **Diabetes control** - HbA1c <48 mmol/mol

**Evidence:** ESVS Guidelines, NICE Guidelines""",
            confidence=0.82,
            reasoning_trace=[
                "Provided general vascular surgery overview",
                "Listed key conditions and emergencies",
                "Outlined prevention strategies"
            ],
            capabilities_used=[
                "arterial_disease_assessment",
                "venous_disease_assessment",
                "vascular_emergency_management"
            ],
            metadata={
                "topic": "vascular_surgery_general"
            }
        )


def create_vascular_surgery_domain():
    """Factory function for vascular surgery domain"""
    return VascularSurgeryDomain()
