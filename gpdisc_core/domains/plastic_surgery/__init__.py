"""
Plastic Surgery Domain Module for GPDISC

Comprehensive plastic surgery consultation covering reconstructive surgery,
hand surgery, burns management, and aesthetic surgery.

Evidence-based guidelines from:
- British Association of Plastic, Reconstructive and Aesthetic Surgeons (BAPRAS)
- Royal College of Surgeons (RCS) England
- American Society of Plastic Surgeons (ASPS)
- National Institute for Health and Care Excellence (NICE)

Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class PlasticSurgeryDomain(BaseDomainModule):
    """
    Plastic Surgery specialty domain for GPDISC

    Covers reconstructive surgery, hand surgery, burns, and aesthetic surgery.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="plastic_surgery",
            version="1.0.0",
            dependencies=[],
            description="Plastic surgery: reconstructive, hand, burns, and aesthetic surgery",
            keywords=[
                # Reconstructive surgery
                "reconstructive surgery", "reconstruction", "skin graft", "skin flap",
                "free flap", "local flap", "regional flap", "tissue expansion",
                "wound reconstruction", "scar revision", "scar", "keloid", "hypertrophic scar",
                "breast reconstruction", "breast implant", "breast augmentation",
                "mastectomy reconstruction", "diep flap", "tram flap", "latissimus dorsi flap",
                "head and neck reconstruction", "mandible reconstruction", "jaw reconstruction",
                "pressure sore", "pressure ulcer", "decubitus ulcer",

                # Hand surgery
                "hand surgery", "carpal tunnel", "trigger finger", "dupuytren's",
                "dupuytren contracture", "ganglion cyst", "hand fracture", "finger fracture",
                "tendon repair", "flexor tendon", "extensor tendon", "nerve repair",
                "hand trauma", "hand injury", "finger amputation", "finger replantation",
                "hand infection", "felon", "paronychia", "tenosynovitis",

                # Burns
                "burn", "burns", "thermal burn", "scald", "electrical burn", "chemical burn",
                "burn care", "burn wound", "escharotomy", "fasciotomy", "skin graft burn",
                "burn reconstruction", "burn scar", "contracture", "post-burn contracture",

                # Skin cancer
                "skin cancer", "basal cell carcinoma", "bcc", "squamous cell carcinoma", "scc",
                "melanoma", "malignant melanoma", "skin lesion", "skin tumour",
                "mohs surgery", "excision biopsy", "wide local excision",

                # Aesthetic surgery (cosmetic)
                "cosmetic surgery", "aesthetic surgery", "plastic surgery",
                "rhinoplasty", "nose job", "nose surgery", "septoplasty",
                "blepharoplasty", "eyelid surgery", "eye bag removal",
                "facelift", "rhytidectomy", "face lift",
                "breast augmentation", "breast enlargement", "breast implant",
                "breast reduction", "breast lift", "mastopexy", "gynaecomastia",
                "abdominoplasty", "tummy tuck", "liposuction", "liposculpture",
                "otoplasty", "ear pinning", "ear surgery",
                "brow lift", "forehead lift",

                # General plastic surgery
                "plastic surgeon", "plastic surgery consultation", "reconstruct"
            ],
            capabilities=[
                "reconstructive_surgery_consultation",
                "hand_surgery_consultation",
                "burns_management",
                "skin_cancer_excision",
                "wound_management",
                "scar_management",
                "preoperative_assessment"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process plastic surgery query

        Routes to appropriate handler based on query content.
        """
        query_lower = query.lower()

        # BURNS - Highest priority (time-critical)
        if any(term in query_lower for term in [
            "burn", "burns", "scald", "thermal burn", "electrical burn", "chemical burn"
        ]):
            return self._handle_burns_query(query, context)

        # Hand surgery
        elif any(term in query_lower for term in [
            "hand surgery", "hand trauma", "hand injury", "hand fracture", "finger fracture",
            "tendon repair", "nerve repair", "finger amputation", "replantation",
            "trigger finger", "dupuytren", "ganglion"
        ]):
            return self._handle_hand_surgery_query(query, context)

        # Skin cancer
        elif any(term in query_lower for term in [
            "skin cancer", "basal cell carcinoma", "bcc", "squamous cell carcinoma", "scc",
            "melanoma", "malignant melanoma", "skin lesion"
        ]):
            return self._handle_skin_cancer_query(query, context)

        # Breast reconstruction
        elif any(term in query_lower for term in [
            "breast reconstruction", "mastectomy reconstruction", "diep flap", "tram flap"
        ]):
            return self._handle_breast_reconstruction_query(query, context)

        # Wound management
        elif any(term in query_lower for term in [
            "wound", "ulcer", "pressure sore", "pressure ulcer", "diabetic ulcer",
            "venous ulcer", "arterial ulcer", "skin graft", "flap"
        ]):
            return self._handle_wound_management_query(query, context)

        # Scar management
        elif any(term in query_lower for term in [
            "scar", "keloid", "hypertrophic scar", "scar revision"
        ]):
            return self._handle_scar_management_query(query, context)

        # Aesthetic surgery
        elif any(term in query_lower for term in [
            "cosmetic surgery", "aesthetic surgery", "rhinoplasty", "nose job",
            "blepharoplasty", "eyelid surgery", "facelift", "face lift",
            "breast augmentation", "breast reduction", "tummy tuck", "abdominoplasty"
        ]):
            return self._handle_aesthetic_surgery_query(query, context)

        # General plastic surgery
        else:
            return self._handle_general_plastic_surgery_query(query, context)

    def _handle_burns_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle burns queries"""
        query_lower = query.lower()

        # Major burns/emergency burns
        if any(term in query_lower for term in [
            "major burn", "severe burn", "burn emergency", "inhalation injury",
            "circumferential burn", "electrical burn", "chemical burn"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**MAJOR BURNS - EMERGENCY MANAGEMENT**

**IMMEDIATE ACTION REQUIRED:**
- **Stop the burning process**
- **ABC assessment** (airway, breathing, circulation)
- **Urgent transfer to burns centre** for major burns

**DEFINITION OF MAJOR BURN:**
- **>5% TBSA** in children or >10% TBSA in adults
- **Any full-thickness burn**
- **Burns involving:** Face, hands, feet, genitalia, perineum, major joints
- **Electrical burns** (including lightning)
- **Chemical burns**
- **Inhalation injury**
- **Burns with associated trauma**
- **Burns in patients with comorbidities** (extremes of age, pregnancy)

**IMMEDIATE MANAGEMENT:**

**1. Stop the Burning Process:**
- **Thermal:** Remove from heat source, remove hot clothing, jewellery
- **Chemical:** Remove contaminated clothing, brush off dry chemicals, irrigate with water (20+ minutes)
- **Electrical:** Disconnect power source before touching patient
- **Tar:** Cool with water, do not remove (trauma)

**2. ABC Assessment:**

**Airway:**
- **Inhalation injury** suspected if:
  - Burn in enclosed space
  - Stridor, hoarseness, cough
  - Soot around mouth/nose
  - Facial burns, singed nasal hairs
- **Early intubation** if airway compromised

**Breathing:**
- **100% oxygen** (if inhalation injury or CO poisoning)
- **Chest escharotomy** if circumferential chest burn restricting ventilation

**Circulation:**
- **IV access** through unburned skin if possible
- **IV fluids** (Parkland formula for resuscitation)
- **Escharotomy** if circumferential limb burn (compartment syndrome)

**Disability:**
- **Level of consciousness** (CO poisoning, head injury)
- **Pain control** (IV opioids)

**Exposure:**
- **Assess TBSA** (Total Body Surface Area) burned
- **Rule of Nines** (adults) or Lund-Browder (children)
- **Assess depth** (superficial, partial-thickness, full-thickness)

**Fluid Resuscitation (Parkland Formula):**
- **3-4 mL x kg x %TBSA** (first 24 hours)
- **Half** in first 8 hours (from time of burn)
- **Half** in next 16 hours
- **Crystalloid** (Hartmann's or Ringer's lactate)
- **Urine output:** 0.5 mL/kg/hour (adults), 1 mL/kg/hour (children)

**BURN DEPTH:**

**Superficial (Epidermal):**
- Erythema, pain, no blisters
- Heal in 7-10 days, no scarring

**Superficial Partial-Thickness (Dermal):**
- Blisters, moist, painful, blanch with pressure
- Heal in 10-14 days, minimal scarring

**Deep Partial-Thickness:**
- White/ blotchy, dry, less painful, may not blanch
- Heal in 3-4 weeks, significant scarring

**Full-Thickness:**
- White/charred, leathery, insensate, no blisters
- **Will not heal** without surgery
- **Skin graft required**

**ESCHAROTOMY:**
- **Indicated for:**
  - **Circumferential burns** of chest/limb
  - **Compartment syndrome** (pain, pallor, pulselessness, paralysis, paraesthesia)
- **Procedure:**
  - Incise through eschar (burned skin) down to fascia
  - Chest: Two longitudinal incisions (lateral)
  - Limb: Medial or lateral incision (or both if severe)
  - **Do NOT** cut through unburned skin

**TRANSFER TO BURNS CENTRE:**
- **Indicated for:**
  - All major burns (see definition above)
  - Burns requiring specialized care (hands, face, genitalia)
  - Children with significant burns
  - Electrical/chemical burns
- **Stabilize** before transfer (ABC, fluids, analgesia)

**CHEMICAL BURNS:**
- **Remove contaminated clothing**
- **Brush off dry chemicals** before irrigation
- **Irrigate copiously** with water (20+ minutes)
- **DO NOT** use neutralizing agents (may cause heat from exothermic reaction)
- **Consider specific antidotes** (e.g., calcium gluconate for hydrofluoric acid)

**ELECTRICAL BURNS:**
- **Disconnect power** before touching patient
- **Cardiac monitoring** (arrhythmias common)
- **Myoglobinuria** (rhabdomyolysis) - maintain high urine output (1-2 mL/kg/hour)
- **Compartment syndrome** common (even without visible burns)
- **Deep tissue damage** (much worse than skin appearance)

**PROGNOSIS:**
- **Mortality:** Depends on age, TBSA, inhalation injury
- **Rule of 100s:** Age + TBSA = mortality (rough estimate)
- **Morbidity:** Scarring, contractures, infection

**COMPLICATIONS:**
- **Hypovolaemic shock** (fluid loss)
- **Infection** (most common cause of death)
- **Sepsis** (Pseudomonas, Staphylococcus)
- **Contractures** (post-burn)
- **Hypertrophic scars, keloids**
- **Psychological trauma**

**Evidence:** NICE NG204, BAPRAS Guidelines""",
                confidence=0.96,
                reasoning_trace=[
                    "Identified major burn - emergency",
                    "Applied ABC approach, Parkland formula",
                    "Escharotomy for circumferential burns"
                ],
                capabilities_used=["burns_management"],
                metadata={
                    "urgency": "emergency",
                    "condition": "major_burn",
                    "intervention": "resuscitation_escharotomy"
                }
            )

        # Minor burns
        elif any(term in query_lower for term in [
            "minor burn", "small burn", "first aid burn", "home burn treatment"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**MINOR BURNS - FIRST AID AND MANAGEMENT**

**DEFINITION OF MINOR BURN:**
- **<5% TBSA** in adults, <2% TBSA in children
- **Superficial or superficial partial-thickness**
- **Not involving:** Face, hands, feet, genitalia, major joints
- **No inhalation injury**
- **No associated trauma**

**IMMEDIATE FIRST AID:**

**1. Stop the Burning Process:**
- Remove from heat source
- Remove hot clothing, jewellery (before swelling)
- **DO NOT** remove if stuck to burn

**2. Cool the Burn:**
- **Cool running water** (15-20°C) for **20 minutes**
- **Within 3 hours** of injury (most effective)
- **DO NOT use:** Ice, iced water, butter, creams, ointments (first aid)
- **Stop cooling** if patient becomes cold (hypothermia risk, especially children/elderly)

**3. Cover the Burn:**
- **Cling film** (plastic wrap) is ideal
  - Non-adherent
  - Allows assessment through film
  - Do not wrap tightly
- **Sterile non-adherent dressing** if cling film not available
- **DO NOT** use cotton wool, fluffy dressings (fibres stick to burn)

**4. Analgesia:**
- **Paracetamol** (first-line)
- **Ibuprofen** (if not contraindicated)
- **Opioids** (severe pain)

**ASSESSMENT:**

**Estimate TBSA (Total Body Surface Area):**
- **Rule of Nines:** (Adults)
  - Head/neck: 9%
  - Each arm: 9%
  - Anterior trunk: 18%
  - Posterior trunk: 18%
  - Each leg: 18%
  - Genitalia: 1%
- **Palm method:** Patient's palm (including fingers) = ~1% TBSA

**Assess Depth:**
- **Superficial:** Erythema, pain, no blisters
- **Superficial partial-thickness:** Blisters, moist, painful
- **Deep partial-thickness:** White/ blotchy, dry, less painful
- **Full-thickness:** White/charred, leathery, insensate

**MANAGEMENT:**

**Superficial Burns (Sunburn):**
- **Cooling** (as above)
- **Moisturizer** (aloe vera, aqueous cream)
- **Analgesia** (paracetamol, ibuprofen)
- **Do NOT** pop blisters (if present)
- **Heal in 7-10 days**

**Superficial Partial-Thickness Blisters:**
- **Intact blisters:** Leave intact (protect wound)
  - May aspirate large/tense blisters (sterile needle)
  - De-roof if ruptured (clean with saline)
- **De-roofed blisters:**
  - Clean with saline or water
  - Apply **non-adherent dressing** (e.g., Jelonet, Melolin, Inadine)
  - Cover with gauze, bandage
  - Change **daily** (or if dressing soiled/leaking)
- **Topical antibiotics** NOT routinely indicated
- **Heal in 10-14 days**

**Deep Partial-Thickness:**
- **Refer to plastic surgery** (may need skin graft)
- **Clean** with saline or water
- **Non-adherent dressing**
- **Consider** topical silver (e.g., Acticoat, Aquacel Ag) if high infection risk
- **Heal in 3-4 weeks** (may scar)

**Full-Thickness:**
- **Refer to plastic surgery** (skin graft required)
- **Will not heal** without surgery
- **Temporary cover** while awaiting graft (non-adherent dressing)

**INFECTION PREVENTION:**
- **Clean hands** before dressing changes
- **Sterile technique** (or clean technique for minor burns)
- **Do NOT** use topical antibiotics routinely (resistance risk)
- **Consider** topical silver if high infection risk

**SIGNS OF INFECTION:**
- Increasing pain, redness
- Purulent discharge
- Foul odour
- Fever
- **Seek medical attention** if infection suspected

**TETANUS PROPHYLAXIS:**
- **Tetanus-prone wounds:**
  - Full-thickness burns
  - Contaminated burns (soil, feces)
- **Vaccination:**
  - **Fully vaccinated** (5 doses): No booster needed
  - **Incomplete vaccination:** Booster + tetanus immunoglobulin if high risk

**WHEN TO SEEK MEDICAL ATTENTION:**
- **Full-thickness burn** (white/charred, painless)
- **Deep partial-thickness** (white/ blotchy, dry)
- **Burns >5% TBSA** (adults), >2% TBSA (children)
- **Burns involving:** Face, hands, feet, genitalia, joints
- **Electrical/chemical burns**
- **Signs of infection**
- **No improvement after 2 weeks**

**PROGNOSIS:**
- **Superficial:** Heal without scarring (7-10 days)
- **Superficial partial-thickness:** Minimal scarring (10-14 days)
- **Deep partial-thickness:** Significant scarring (3-4 weeks)
- **Full-thickness:** Will scar, requires graft (will not heal)

**SCAR MANAGEMENT:**
- **Massage** (once healed) with moisturizer
- **Sun protection** (UV exposure darkens scars for 6-12 months)
- **Silicone gel/sheets** (for hypertrophic scars)
- **Consider** steroid injection (for hypertrophic/keloid)

**EVIDENCE:** NICE NG204, BAPRAS Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified minor burn query",
                    "Cool running water for 20 minutes (first aid)",
                    "Dressing management by depth"
                ],
                capabilities_used=["burns_management"],
                metadata={
                    "topic": "minor_burns",
                    "guideline": "nice_ng204"
                }
            )

        # General burns information
        else:
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**BURNS**

**CLASSIFICATION:**

**By Depth:**
- **Superficial:** Erythema, pain (sunburn)
- **Superficial partial-thickness:** Blisters, moist, painful
- **Deep partial-thickness:** White/ blotchy, dry, less painful
- **Full-thickness:** White/charred, insensate (requires graft)

**By TBSA (Total Body Surface Area):**
- **Minor:** <5% TBSA (adults), <2% TBSA (children)
- **Moderate:** 5-15% TBSA (adults), 2-10% TBSA (children)
- **Major:** >15% TBSA (adults), >10% TBSA (children)

**By Cause:**
- **Thermal:** Fire, scald, hot objects
- **Chemical:** Acids, alkalis
- **Electrical:** Low voltage, high voltage, lightning
- **Radiation:** Sunburn, radiation therapy

**IMMEDIATE MANAGEMENT:**

**All Burns:**
- **Stop burning process**
- **Cool burn** (cool running water, 20 minutes)
- **Remove jewellery, hot clothing**
- **Cover** (cling film, sterile dressing)
- **Analgesia**

**Major Burns:**
- **ABC assessment**
- **Fluid resuscitation** (Parkland formula)
- **Escharotomy** (if circumferential)
- **Transfer to burns centre**

**COMPLICATIONS:**
- **Hypovolaemic shock** (fluid loss)
- **Infection** (most common cause of death)
- **Contractures** (post-burn scarring)
- **Hypertrophic scars, keloids**

**PROGNOSIS:**
- **Mortality:** Depends on age, TBSA, inhalation injury
- **Scarring:** Worse with deep partial-thickness, full-thickness
- **Functional impairment:** Depends on location (joints, hands)

**EVIDENCE:** NICE NG204""",
                confidence=0.86,
                reasoning_trace=[
                    "Provided general burns overview",
                    "Classified by depth and TBSA",
                    "Outlined immediate management"
                ],
                capabilities_used=["burns_management"],
                metadata={
                    "topic": "burns_general"
                }
            )

    def _handle_hand_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle hand surgery queries"""
        query_lower = query.lower()

        # Hand trauma
        if any(term in query_lower for term in [
            "hand trauma", "hand injury", "finger injury", "finger amputation", "replantation",
            "tendon injury", "tendon laceration", "nerve injury", "fracture"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**HAND TRAUMA**

**IMMEDIATE MANAGEMENT:**

**1. Assess and Control Bleeding:**
- **Direct pressure** to wound
- **Elevate hand** (above heart)
- **DO NOT** use tourniquet (risk of digital ischaemia)

**2. Assess Injury:**
- **Tendons:** Test flexor/ extensor function
- **Nerves:** Test sensation (digital nerves)
- **Bones:** Assess for fracture (tenderness, deformity, crepitus)
- **Vascular:** Assess capillary refill, digital colour, temperature

**3. Imaging:**
- **X-ray** (if fracture, foreign body suspected)
- **Tendon/nerve** assessed clinically (imaging not usually needed)

**4. Tetanus Prophylaxis:**
- **Tetanus-prone wounds** (contaminated, devitalized tissue)
- **Vaccinate** if not fully vaccinated

**SPECIFIC INJURIES:**

**Flexor Tendon Laceration:**
- **Inability to flex** finger (distal interphalangeal joint)
- **No active motion** beyond level of injury
- **Surgical repair** within 7-10 days (earlier better)
- **Zone I-V classification** (guides prognosis)

**Extensor Tendon Laceration:**
- **Inability to extend** finger
- **Surgical repair** (more forgiving than flexor)
- **Splinting** important postoperatively

**Digital Nerve Laceration:**
- **Numbness** in digital distribution
- **Surgical repair** (primary repair best)
- **Sensation may not fully recover**

**Finger Amputation:**
- **Wrap amputated part** in saline-moistened gauze
- **Place in plastic bag**, then on ice
- **DO NOT** put amputated part directly on ice
- **Replantation** if:
  - Sharp injury (better outcome)
  - Multiple digits amputated
  - Thumb amputation (high priority)
  - Distal amputation (better outcome)
  - Young patient (better motivation, recovery)
- **Revision amputation** if:
  - Crush injury (poor outcome)
  - Severely contaminated
  - Multiple levels of injury
  - Patient not fit for long surgery

**Fractures:**
- **Phalanx fractures** (most common)
- **Metacarpal fractures** (boxer's fracture - 5th metacarpal neck)
- **Management:**
  - **Reduction** if displaced
  - **Splinting** (buddy taping, gutter splint)
  - **K-wiring** (if unstable)
  - **Open reduction internal fixation** (if severely displaced)

**PRINCIPLES OF HAND SURGERY:**

**Early Intervention:**
- **Tendon/nerve repair** within 7-10 days (earlier better)
- **Fracture fixation** within 1-2 weeks
- **Debridement** of contaminated wounds (urgent)

**Minimize Trauma:**
- **Gentle tissue handling**
- **Avoid unnecessary dissection**
- **Preserve vascularity**

**Repair Structures:**
- **Tendons** (primary repair with 4/0 or 5/0 prolene)
- **Nerves** (primary repair with 8/0 or 9/0 nylon)
- **Bones** (K-wires, plates, screws)

**POSTOPERATIVE CARE:**
- **Splinting** (protect repair)
- **Elevation** (reduce swelling)
- **Hand therapy** (critical for good outcome)
- **Early protected mobilization** (after tendon repair)

**HAND THERAPY:**
- **Essential** for good functional outcome
- **Splinting** (protect repair, prevent contractures)
- **Exercises** (regain range of motion, strength)
- **Scar massage** (prevent adhesions)
- **Desensitization** (for nerve injuries)

**PROGNOSIS:**
- **Tendon repairs:** 70-90% good/excellent (if repaired early)
- **Nerve repairs:** 50-70% good sensory recovery
- **Replantation:** 70-90% survival (but function variable)
- **Fractures:** Most heal with good function if properly aligned

**COMPLICATIONS:**
- **Stiffness** (most common)
- **Tendon adhesion** (limiting motion)
- **Infection**
- **Nonunion** (fractures)
- **Complex regional pain syndrome** (CRPS)

**EVIDENCE:** BSSH Guidelines, BAPRAS Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified hand trauma query",
                    "ABC approach: control bleeding, assess injury",
                    "Early intervention critical for good outcome"
                ],
                capabilities_used=["hand_surgery_consultation"],
                metadata={
                    "topic": "hand_trauma",
                    "guideline": "bssh"
                }
            )

        # Trigger finger
        elif any(term in query_lower for term in [
            "trigger finger", "trigger thumb", "stenosing tenosynovitis"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**TRIGGER FINGER (STENOSING TENOSYNOVITIS)**

**WHAT IS IT?**
- **Tendon entrapment** at A1 pulley
- Flexor tendon catches (clicks) when flexing/ extending finger
- Most common in **thumb, ring, middle** fingers
- **Female predominance** (F:M 6:1)
- Peak incidence: 40-60 years

**SYMPTOMS:**
- **Catching, clicking, popping** when flexing/ extending finger
- **Finger locks** in flexed position (may need to straighten with other hand)
- **Pain** at base of finger (palm side)
- **Stiffness** (worse in morning)
- **Nodule** may be palpable at base of finger

**CAUSES/RISK FACTORS:**
- **Idiopathic** (most common)
- **Repetitive gripping** (occupational)
- **Diabetes mellitus** (10-20%)
- **Rheumatoid arthritis**
- **Gout**
- **Pregnancy** (usually resolves postpartum)
- **Hypothyroidism**

**PHYSICAL EXAMINATION:**
- **Tenderness** at A1 pulley (base of finger, palm side)
- **Catching** on flexion/ extension
- **Nodule** palpable in tendon
- ** triggering** may be demonstrable
- **Assess for** associated conditions (RA, diabetes)

**GRADING:**
- **Grade I:** Pre-triggering (pain, no catching)
- **Grade II:** Triggering (actively correctable)
- **Grade III:** Locking (passively correctable)
- **Grade IV:** Contracture (not correctable)

**MANAGEMENT:**

**Conservative (First-Line for Grade I-II):**
- **Activity modification**
  - Avoid repetitive gripping
  - Ergonomic assessment
- **Splinting**
  - **Metacarpophalangeal (MCP) joint splint**
  - Wear at night (and during day if possible)
  - Trial for 6-12 weeks
  - **Not recommended** for Grade III-IV
- **Corticosteroid injection**
  - **Into tendon sheath** (A1 pulley)
  - 60-80% success rate
  - May be repeated (max 2-3 injections)
  - **Avoid** if diabetes (higher failure rate, infection risk)
  - **Complications:** Pain, bruising, skin depigmentation, tendon rupture (rare)

**Surgery (Trigger Finger Release):**
- **Indicated for:**
  - **Grade III-IV** (locking, contracture)
  - **Failed conservative management** (>3 months)
  - **Recurrent** after injection
  - **Associated conditions** (RA, gout - may need synovectomy)
- **Procedure:**
  - **Open release** (standard)
    - 1-2 cm incision at base of finger
    - Release A1 pulley
    - Protect neurovascular bundles
    - Quick recovery, high success rate
  - **Percutaneous release** (blind or ultrasound-guided)
    - Needle through skin to release pulley
    - No incision, faster recovery
    - Risk of incomplete release, nerve injury
- **Outcomes:**
  - 90-95% good/excellent
  - Immediate relief of triggering
  - Return to activities in 1-2 weeks
- **Complications:**
  - **Incomplete release** (<5%) - persistent triggering
  - **Nerve injury** (1-2%) - digital nerve
  - **Infection** (1%)
  - **Bowstringing** (rare - if A2 pulley inadvertently released)
  - **Scar tenderness** (10-20%)

**POSTOPERATIVE CARE:**
- **Light bandage** for 5-7 days
- **Mobilize finger** immediately (prevent stiffness)
- **Wound care** (keep dry)
- **Hand therapy** (if stiff)
- **Return to activities:** 1-2 weeks

**PROGNOSIS:**
- **Conservative:** 50-70% improve (especially Grade I-II)
- **Injection:** 60-80% success (may last months-years)
- **Surgical:** 90-95% good/excellent outcome
- **Recurrence:** <5% (after surgery)
- **Multiple digits:** 20% (bilateral in 20%)

**PATIENT INFORMATION:**
- **Benign condition** (not dangerous)
- **Activity modification** may prevent recurrence
- **Diabetes:** Higher recurrence rate, lower success rate with injection
- **Return to normal activities** expected after treatment

**EVIDENCE:** BSSH Guidelines, AAOS Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified trigger finger query",
                    "Grading (I-IV) guides treatment",
                    "Corticosteroid injection first-line (Grade I-II), surgery for Grade III-IV"
                ],
                capabilities_used=["hand_surgery_consultation"],
                metadata={
                    "topic": "trigger_finger",
                    "guideline": "bssh"
                }
            )

        # Dupuytren's contracture
        elif any(term in query_lower for term in [
            "dupuytren", "dupuytren's contracture", "viking disease", "lump in palm"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**DUPUTREN'S CONTRACTURE**

**WHAT IS IT?**
- **Fibromatosis** of palmar fascia
- **Nodules, cords** develop in palm/fingers
- Progressive **flexion contracture** of fingers
- **"Viking disease"** (common in Northern European descent)
- **Male predominance** (M:F 7:1)
- Peak incidence: 50-60 years

**AETIOLOGY:**
- **Genetic predisposition** (autosomal dominant with incomplete penetrance)
- **Risk factors:**
  - **Northern European ancestry** (Vikings)
  - **Male sex**
  - **Age** (>50 years)
  - **Diabetes mellitus** (3x increased risk)
  - **Smoking**
  - **Alcohol** (heavy use)
  - **Manual labour** (controversial)
  - **Epilepsy**, **HIV** (increased risk)

**NATURAL HISTORY:**
- **Progressive** (worsens over time)
- **Rate of progression variable** (some slow, some rapid)
- **Spontaneous regression** does NOT occur (once contracture develops)
- **Unpredictable** which patients/digits will progress

**CLINICAL FEATURES:**
- **Palmar nodule** (firm, fixed to skin, not to deeper structures)
- **Palmar cord** (band-like thickening)
- **Digital cord** (extends into finger)
- **Flexion contracture** (MCP, PIP joints most affected)
- **Pitting** of skin (over cords)
- **Knuckle pads** (Garrod's pads) over dorsal PIP joints

**MOST COMMONLY AFFECTED DIGITS:**
- **Ring finger** (most common)
- **Little finger**
- **Middle finger**
- **Thumb** (less common)

**SEVERITY ASSESSMENT:**

**Tubiana Staging:**
- **Stage 0:** No contracture (palmar nodule only)
- **Stage N (N1, N2, N3):** Contracture 0-45°, 45-90°, 90-135°
- **Stage IV (IIIA, IIIB):** Contracture 135-180° (IIIA: distal to MCP, IIIB: includes MCP)

**Assessment Tables:**
- **MCP contracture:** Measure angle of finger extension (palmar surface to finger)
- **PIP contracture:** Measure angle of finger extension
- **Functional impact:** Difficulty with activities (handwashing, putting hand in pocket, shaking hands)

**INDICATIONS FOR TREATMENT:**
- **Contracture** causing functional limitation
- **MCP contracture** >30°
- **PIP contracture** >15-20° (even small PIP contractures cause significant functional limitation)
- **Patient preference**

**MANAGEMENT:**

**Observation:**
- **Indicated for:**
  - No contracture (palmar nodule only)
  - Minimal contracture (<30° at MCP, <15° at PIP)
  - Patient not bothered
- **Monitor** for progression (review 6-12 monthly)

**Needle Aponeurotomy (NA):**
- **Minimally invasive**
- **Procedure:**
  - Needle inserted through skin
  - Divide cord (multiple passes)
  - No incision
- **Advantages:**
  - Quick procedure (office-based)
  - Immediate improvement
  - Faster recovery
  - Lower morbidity
- **Disadvantages:**
  - Higher recurrence rate (30-50% at 3 years)
  - Higher risk of nerve injury (blind procedure)
  - Skin tears (10-20%)
  - Not suitable for severe contractures or recurrent disease
- **Outcomes:**
  - Immediate correction
  - Good for early disease, MCP contractures
  - Higher recurrence than open surgery

**Collagenase Clostridium Histolyticum (CCH) Injection:**
- **Enzymatic dissolution** of cord
- **Procedure:**
  - Inject CCH into cord
  - Next day: manipulate finger to rupture cord
- **Advantages:**
  - Minimally invasive
  - No incision
  - Good for MCP contractures
- **Disadvantages:**
  - High cost
  - Multiple injections often needed (different cords)
  - Skin tears, swelling, bruising common
  - Higher recurrence (40-50% at 5 years)
- **Not suitable for:** PIP contractures, recurrent disease

**Open Fasciectomy (Standard Surgical Treatment):**
- **Indicated for:**
  - Significant contracture (>30° MCP, >15° PIP)
  - Recurrent disease
  - PIP contractures (better outcome)
  - Patient preference
- **Procedure:**
  - **Local/general anaesthetic**
  - **Zigzag incision** (or Bruner incision for digits)
  - **Excise diseased fascia** (cord)
  - **Release contracture**
  - **Skin closure** (may need **Z-plasty** or **skin graft** if skin deficiency)
- **Advantages:**
  - Most complete correction
  - Lower recurrence (20-30% at 5 years)
  - Can address PIP contractures
  - Can treat recurrent disease
- **Disadvantages:**
  - Longer recovery
  - Higher morbidity (infection, wound healing problems)
  - Scar (long incisions)
- **Outcomes:**
  - 80-90% good/excellent correction
  - Recurrence: 20-30% at 5 years
  - **DUPUYTREN'S DISEASE RECURS** (may progress in other digits)
- **Complications:**
  - **Nerve injury** (digital nerve) - 2-5%
  - **Infection** - 2-5%
  - **Wound healing problems** - 5-10%
  - **Complex regional pain syndrome** (CRPS) - 1-2%
  - **Skin necrosis** (if Z-plasty or skin graft needed)
  - **Recurrence/progression** (20-30% at 5 years)

**Dermofasciectomy:**
- **Excise diseased fascia** AND overlying skin
- **Skin graft** to close defect
- **Indicated for:**
  - **Recurrent disease** (previous surgery)
  - **Severe skin involvement**
  - **Younger patients** (lower recurrence)
- **Lower recurrence** (10-20% at 5 years)
- **Higher morbidity** (skin graft, donor site)

**POSTOPERATIVE CARE:**
- **Splinting** (extension splint at night for 3-6 months)
- **Hand therapy** (critical for good outcome)
  - **Elevation** (reduce swelling)
  - **Exercises** (regain range of motion, strength)
  - **Scar massage** (prevent adhesions)
- **Mobilize early** (day 1-2 postoperative)
- **Return to activities:** 2-6 weeks (depends on procedure, job)

**PROGNOSIS:**
- **High recurrence rate** (30-50% lifetime)
- **Progression** to other digits common (30-50%)
- **Better outcome** with:
  - Early intervention (before severe contracture)
  - Complete correction
  - Hand therapy
- **Worse outcome** with:
  - PIP contractures (harder to fully correct)
  - Recurrent disease
  - Younger age (more aggressive disease)
  **Family history** (more aggressive disease)

**PATIENT INFORMATION:**
- **Chronic condition** (requires long-term follow-up)
- **Progressive** (worsens over time)
- **Recurrence common** (may need further surgery in future)
- **Early treatment** = better outcome
- **Family screening** (first-degree relatives at risk)

**EVIDENCE:** BSSH Guidelines, BAPRAS Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified Dupuytren's contracture query",
                    "Progressive condition, high recurrence",
                    "Surgical fasciectomy is standard treatment"
                ],
                capabilities_used=["hand_surgery_consultation"],
                metadata={
                    "topic": "dupuytren_contracture",
                    "guideline": "bssh"
                }
            )

        # Ganglion cyst
        elif any(term in query_lower for term in [
            "ganglion", "ganglion cyst", "wrist lump", "cyst on wrist"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**GANGLION CYST**

**WHAT IS IT?**
- **Benign cyst** arising from joint or tendon sheath
- **Most common hand/wrist lump**
- **Mucin-filled** (gelatinous fluid)
- **NOT a true cyst** (no epithelial lining)
- **Female predominance** (F:M 3:1)
- Peak incidence: 20-40 years

**CAUSES:**
- **Idiopathic** (most common)
- **Joint or tendon irritation** (trauma, overuse)
- **Degenerative joint disease** (arthritis)
- **Connection** to joint or tendon sheath (one-way valve)

**CLINICAL FEATURES:**
- **Smooth, round, mobile lump**
- **Most common locations:**
  - **Dorsal wrist** (70-80%) - over scapholunate ligament
  - **Volar wrist** (15-20%) - over radial artery
  - **Flexor tendon sheath** (trigger finger)
  - **Dorsal finger** (mucous cyst - associated with osteoarthritis)
- **Fluctuant** (may feel tense)
- **Transillumination** (light passes through cyst)
- **May be painful** (if compressing nerve)
- **May limit range of motion** (if large)

**DIAGNOSIS:**
- **Clinical** (usually straightforward)
- **Transillumination** (confirms cystic nature)
- **Aspiration** (diagnostic and therapeutic - but high recurrence)
- **Ultrasound** (if diagnosis uncertain)
- **MRI** (rarely needed)

**MANAGEMENT:**

**Observation (First-Line):**
- **Many resolve spontaneously** (30-50%)
- **Indicated for:**
  - Asymptomatic ganglion
  - Small ganglion
  - Patient not bothered
- **Reassure** that it's benign
- **Monitor** for change

**Aspiration:**
- **Indicated for:**
  - Symptomatic ganglion
  - Diagnostic (if uncertain)
  - Patient preference (avoid surgery)
- **Procedure:**
  - Sterile needle aspiration
  - Remove viscous gelatinous fluid
  - **DO NOT inject steroid** (no benefit, may cause complications)
- **Outcomes:**
  - Immediate relief of symptoms
  - High recurrence (50-70%)
  - May be repeated
- **Complications:**
  - **Recurrence** (most common)
  - **Infection** (rare)
  - **Bleeding** (rare)
  - **Nerve injury** (rare - if dorsal wrist ganglion near radial sensory nerve)

**Surgical Excision:**
- **Indicated for:**
  - **Persistent symptoms** after failed aspiration
  - **Recurrent ganglion**
  - **Large ganglion** causing functional limitation
  - **Volar wrist ganglion** (near radial artery - higher risk of aspiration)
  - **Patient preference**
- **Procedure:**
  - **Excise ganglion** along with stalk to joint/tendon sheath
  - **Identify and protect** nerves, arteries (especially radial artery for volar wrist ganglion)
  - **Remove a portion of joint capsule** (to reduce recurrence)
- **Outcomes:**
  - 90-95% successful
  - Recurrence: 5-10% (lower than aspiration)
  - Symptom relief
- **Complications:**
  - **Recurrence** (5-10%)
  - **Stiffness** (5-10%)
  - **Scar tenderness** (10-20%)
  - **Nerve injury** (1-2% - radial sensory nerve for dorsal ganglion)
  - **Arterial injury** (rare - radial artery for volar ganglion)
  - **Infection** (1%)
  - **Complex regional pain syndrome** (CRPS) (1%)

**POSTOPERATIVE CARE:**
- **Light bandage** for 5-7 days
- **Mobilize wrist** once wound healed (7-10 days)
- **Hand therapy** (if stiff)
- **Scar massage** (once healed)
- **Return to activities:** 1-2 weeks

**PROGNOSIS:**
- **Benign** (not cancerous)
- **Spontaneous resolution:** 30-50%
- **Aspiration:** 50-70% recurrence
- **Surgery:** 90-95% success, 5-10% recurrence
- **May recur** in same location or different location

**PATIENT INFORMATION:**
- **Benign condition** (not dangerous)
- **Many resolve spontaneously**
- **Do NOT smash** with book (traditional treatment - causes injury, may damage underlying structures)
- **Higher recurrence** with aspiration
- **Surgery has lower recurrence** but higher morbidity

**EVIDENCE:** BSSH Guidelines""",
                confidence=0.90,
                reasoning_trace=[
                    "Identified ganglion cyst query",
                    "Most common hand/wrist lump, benign",
                    "Observation first-line (many resolve spontaneously)"
                ],
                capabilities_used=["hand_surgery_consultation"],
                metadata={
                    "topic": "ganglion_cyst",
                    "guideline": "bssh"
                }
            )

        # General hand surgery
        else:
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**HAND SURGERY**

**COMMON HAND CONDITIONS:**

**Trigger Finger (Stenosing Tenosynovitis)**
- Catching/locking of finger
- Nodule at base of finger
- Steroid injection first-line
- Surgery if Grade III-IV

**Dupuytren's Contracture**
- Progressive flexion contracture
- Palmar nodules, cords
- Surgery (fasciectomy) if contracture >30° MCP, >15° PIP

**Ganglion Cyst**
- Most common hand/wrist lump
- Benign, may resolve spontaneously
- Aspiration (high recurrence) or surgery (lower recurrence)

**Carpal Tunnel Syndrome**
- Median nerve compression at wrist
- Numbness, tingling in thumb, index, middle
- Splinting, injection first-line
- Surgery if severe or failed conservative

**Ulnar Neuropathy**
- Ulnar nerve compression at elbow
- Numbness, tingling in ring, little finger
- Splinting first-line
- Simple decompression surgery (most)

**HAND TRAUMA:**

**Tendon Injuries:**
- Flexor tendon laceration (cannot flex finger)
- Extensor tendon laceration (cannot extend finger)
- Surgical repair (early = better outcome)

**Nerve Injuries:**
- Digital nerve laceration (numbness in finger)
- Surgical repair (primary repair best)
- Sensation may not fully recover

**Fractures:**
- Phalanx fractures (most common)
- Metacarpal fractures (boxer's fracture)
- Reduction, splinting, K-wiring if unstable

**Finger Amputation:**
- Replantation (if sharp injury, thumb, multiple digits)
- Revision amputation (if crush injury, poor prognosis)

**POSTOPERATIVE CARE:**
- **Splinting** (protect repair)
- **Elevation** (reduce swelling)
- **Hand therapy** (critical for good outcome)
- **Early protected mobilization**

**PROGNOSIS:**
- **Good functional recovery** if early intervention, appropriate rehabilitation
- **Stiffness** most common complication
- **Hand therapy** essential

**EVIDENCE:** BSSH Guidelines""",
                confidence=0.85,
                reasoning_trace=[
                    "Provided hand surgery overview",
                    "Listed common conditions and trauma",
                    "Emphasized hand therapy critical for good outcome"
                ],
                capabilities_used=["hand_surgery_consultation"],
                metadata={
                    "topic": "hand_surgery_general"
                }
            )

    def _handle_skin_cancer_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle skin cancer queries"""
        query_lower = query.lower()

        # Basal cell carcinoma
        if any(term in query_lower for term in [
            "basal cell carcinoma", "bcc", "rodent ulcer", "basal cell"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**BASAL CELL CARCINOMA (BCC)**

**WHAT IS IT?**
- **Most common type of skin cancer**
- **Arises from basal cells** of epidermis
- **Locally invasive** (rarely metastasizes)
- **Sun-exposed areas** (face, neck, scalp)
- **Low malignant potential** but can cause significant local destruction

**RISK FACTORS:**
- **UV exposure** (sun, tanning beds)
- **Fair skin** (Fitzpatrick I-II)
- **Age** >50 years (peak 60-80 years)
- **Male sex** (slightly higher)
- **Previous BCC** (30% develop second BCC)
- **Immunosuppression** (transplant, HIV)
- **Arsenic exposure** (rare)
- **Gorlin syndrome** (nevoid basal cell carcinoma syndrome - rare genetic)

**TYPES:**

**Nodular BCC (Most Common - 60%):**
- **Pearly nodule** with telangiectasia
- **Central ulceration** ("rodent ulcer")
- **Well-defined** edges

**Superficial BCC (10-15%):**
- **Scaly plaque**
- **Raised, red patch**
- **Common on trunk**
- **May be confused** with eczema or psoriasis

**Morphoeic BCC (5-10%):**
- **Scar-like** plaque
- **Ill-defined** edges
- **More aggressive** (higher recurrence after surgery)
- **Common on face**

**Pigmented BCC:**
- **Pigmented** (brown, black, blue)
- **May be confused** with melanoma

**DIAGNOSIS:**

**Clinical Diagnosis:**
- **Typical appearance**
- **Slowly growing** (months-years)
- **May bleed**, crust over

**Biopsy:**
- **Punch biopsy** (most common)
- **Incisional biopsy** (if large)
- **Excisional biopsy** (if small)

**Histology (Definitive Diagnosis):**
- **Basaloid cells** at periphery of tumour nests
- **Palisading** nuclei
- **Retraction artefact** (tumour nests separate from stroma)

**MANAGEMENT:**

**Surgical Excision (Gold Standard):**
- **Wide local excision**
  - **Margins:** 4-5 mm for low-risk, 10-15 mm for high-risk BCC
  - **Primary closure** (if small)
  - **Skin graft or local flap** (if large)
- **Outcomes:**
  - 5-year cure: 95-99%
  - Recurrence: 1-5% (depends on margins, histology)
- **Complications:**
  - **Scarring** (cosmetic)
  - **Wound infection** (1-2%)
  - **Bleeding** (1%)
  - **Nerve injury** (rare - facial nerve for facial BCC)

**Mohs Micrographic Surgery (MMS):**
- **Indicated for:**
  - **High-risk BCC** (morphoeic, recurrent, large, ill-defined)
  - **Facial BCC** (cosmetically sensitive area)
  - **Where tissue conservation** critical
- **Procedure:**
  - Excision with narrow margin
  - **Frozen section** assessment of margins
  - **Serial excision** until clear margins
  - **Immediate reconstruction** once clear
- **Advantages:**
  - **Highest cure rate** (99% at 5 years)
  - **Tissue conservation** (smallest defect)
  - **Margin assessment** (complete circumferential margin assessment)
- **Disadvantages:**
  - **Time-consuming** (several hours)
  - **Higher cost**
  - **Requires specialized training**
  - **Not available everywhere**
- **Outcomes:**
  - 5-year cure: 99%
  - Recurrence: <1%

**Radiotherapy (Definitive):**
- **Indicated for:**
  - **Patients not surgical candidates** (comorbidities, age)
  - **Large BCC** where surgery would be morbid
  - **Patient preference** (avoid surgery)
- **NOT indicated for:**
  - **Morphoeic BCC** (higher recurrence)
  - **Recurrent BCC** (higher recurrence)
- **Outcomes:**
  - 5-year cure: 85-90%
  - Recurrence: 10-15% (higher than surgery)
- **Complications:**
  - **Radiation dermatitis**
  - **Cosmetic** (worse than surgery)
  - **Long-term risk** of radiodermatitis, secondary malignancy (rare)

**Topical Therapies (for Superficial BCC):**
- **Imiquimod 5% cream** (immune modulator)
  - Applied 5x/week for 6-12 weeks
  - 5-year cure: 80-85%
  - Recurrence: 15-20%
  - **Indicated for:** Low-risk superficial BCC on trunk
- **5-Fluorouracil (5-FU) cream** (chemotherapy)
  - Applied 1-2x/day for 6-12 weeks
  - Similar efficacy to imiquimod
  - **Not NICE-approved** for BCC (but used off-label)

**Cryotherapy (for Small, Low-Risk BCC):**
- **Liquid nitrogen**
- **2 freeze-thaw cycles**
- 5-year cure: 85-90%
- Recurrence: 10-15%
- **Not recommended for** facial BCC or high-risk BCC

**Photodynamic Therapy (PDT):**
- **Photosensitizer** (methyl aminolevulinate) + light
- **Indicated for:** Low-risk superficial BCC
- 5-year cure: 75-80%
- Recurrence: 20-25%
- **Not NICE-approved** for BCC (but used off-label)

**PROGNOSIS:**
- **Excellent** (rarely metastasizes)
- **Local invasion** may cause significant tissue destruction (esp. morpheaform, neglect)
- **Recurrence risk** depends on:
  - **Margins** (wider margins = lower recurrence)
  - **Histology** (morphoeic higher recurrence)
  - **Site** (facial higher recurrence)
  - **Previous treatment** (recurrent BCC higher recurrence)

**FOLLOW-UP:**
- **Annual skin check** (30% develop second BCC)
- **Self-examination** (monthly)
- **Sun protection** (critical for prevention)

**PREVENTION:**
- **Sun protection:**
  - **Sunscreen** SPF 30+ (reapply every 2 hours)
  - **Protective clothing** (hat, long sleeves)
  - **Avoid midday sun** (10 am - 4 pm)
  - **No tanning beds**
- **Vitamin D supplementation** (if sun-avoiding)

**EVIDENCE:** NICE NG14, BAD Guidelines""",
                confidence=0.94,
                reasoning_trace=[
                    "Identified basal cell carcinoma query",
                    "Most common skin cancer, rarely metastasizes",
                    "Surgical excision (gold standard) or Mohs (high-risk/facial)"
                ],
                capabilities_used=["skin_cancer_excision"],
                metadata={
                    "topic": "basal_cell_carcinoma",
                    "guideline": "nice_ng14"
                }
            )

        # Squamous cell carcinoma
        elif any(term in query_lower for term in [
            "squamous cell carcinoma", "scc", "squamous cell", "skin scc"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**SQUAMOUS CELL CARCINOMA (SCC)**

**WHAT IS IT?**
- **Second most common type of skin cancer**
- **Arises from keratinocytes** of epidermis
- **Can metastasize** (unlike BCC)
- **Sun-exposed areas** (face, ears, neck, dorsal hands)
- **More aggressive** than BCC

**RISK FACTORS:**
- **UV exposure** (sun, tanning beds)
- **Fair skin** (Fitzpatrick I-II)
- **Age** >60 years (peak 70-80 years)
- **Male sex** (higher than BCC)
- **Immunosuppression** (transplant, HIV - much higher risk)
- **Chronic wounds/scars** (Marjolin's ulcer)
- **Human papillomavirus** (HPV - especially genital SCC)
- **Arsenic exposure** (rare)

**PRECARIOUS LESIONS:**
- **Actinic keratosis** (rough, scaly patch)
- **Bowen's disease** (SCC in situ)
- **Erythroplasia of Queyrat** (SCC in situ of glans penis)
- **Leukoplakia** (oral SCC in situ)

**CLINICAL FEATURES:**
- **Hyperkeratotic plaque** or nodule
- **Ulceration** common
- **Elevated, indurated** edges
- **Rapid growth** (weeks-months)
- **May bleed**, crust over
- **Common sites:** Face (ears, lips, nose), dorsal hands, forearms

**DIAGNOSIS:**

**Clinical Diagnosis:**
- **Typical appearance**
- **Rapidly growing** (faster than BCC)

**Biopsy:**
- **Punch biopsy** (most common)
- **Incisional biopsy** (if large)
- **Excisional biopsy** (if small)

**Histology (Definitive Diagnosis):**
- **Keratin pearls** (round collections of keratin)
- **Intercellular bridges**
- **Dyskeratosis** (abnormal keratinization)
- **Invasion** of dermis

**STAGING (AJCC 8th Edition):**

**T Stage (Primary Tumour):**
- **Tis:** SCC in situ (Bowen's disease)
- **T1:** <2 cm, <2 mm depth, no high-risk features
- **T2:** 2-4 cm OR 2-4 mm depth OR one high-risk feature
- **T3:** >4 cm OR >4 mm depth OR two high-risk features OR bone invasion
- **T4:** Major invasion (skull, axial skeleton, brain)

**High-Risk Features:**
- **Depth** >2 mm
- **Perineural invasion**
- **Poor differentiation**
- **Site** (ear, lip, eyelid)
- **Immunosuppression**

**MANAGEMENT:**

**Surgical Excision (Gold Standard):**
- **Wide local excision**
  - **Margins:** 4-6 mm for low-risk, 10-20 mm for high-risk SCC
  - **Primary closure** (if small)
  - **Skin graft or local flap** (if large)
- **Sentinel lymph node biopsy** (if high-risk, >2 cm, >2 mm depth)
- **Outcomes:**
  - 5-year cure: 90-95% (low-risk), 70-80% (high-risk)
  - Recurrence: 5-10% (low-risk), 20-30% (high-risk)
- **Complications:**
  - **Scarring** (cosmetic)
  - **Wound infection** (2-5%)
  - **Bleeding** (1-2%)
  - **Nerve injury** (rare - facial nerve for facial SCC)

**Mohs Micrographic Surgery (MMS):**
- **Indicated for:**
  - **High-risk SCC** (large, deep, poorly differentiated, perineural invasion)
  - **Facial SCC** (cosmetically sensitive area)
  - **Where tissue conservation** critical
- **Advantages:**
  - **Highest cure rate** (95-97% at 5 years)
  - **Complete margin assessment**
  - **Tissue conservation**
- **Disadvantages:**
  - **Time-consuming**
  - **Higher cost**
  - **Not available everywhere**
- **Outcomes:**
  - 5-year cure: 95-97%

**Radiotherapy (Definitive):**
- **Indicated for:**
  - **Patients not surgical candidates** (comorbidities, age)
  - **Large SCC** where surgery would be morbid
  - **Adjuvant** (positive margins, lymph node metastasis)
  - **Palliative** (metastatic SCC)
- **NOT indicated for:**
  - **Young patients** (long-term radiation risk)
  - **Cartilage involvement** (radiation necrosis)
- **Outcomes:**
  - 5-year cure: 80-90% (definitive)
  - Recurrence: 10-20% (higher than surgery)
- **Complications:**
  - **Radiation dermatitis**
  - **Cosmetic** (worse than surgery)
  - **Long-term risk** of radiodermatitis, secondary malignancy

**Lymph Node Management:**
- **Elective lymph node dissection** (if high-risk, no clinically involved nodes)
- **Therapeutic lymph node dissection** (if clinically involved nodes)
- **Sentinel lymph node biopsy** (increasingly used for high-risk SCC)
- **Adjuvant radiotherapy** (if multiple positive nodes, extracapsular extension)

**Systemic Therapy (for Metastatic SCC):**
- **Cemiplimab** (PD-1 inhibitor) - approved for advanced cutaneous SCC
- **Chemotherapy** (platinum-based) - palliative
- **Clinical trials**

**PROGNOSIS:**
- **Risk of metastasis:** 2-5% overall (higher for high-risk SCC)
- **Risk factors for metastasis:**
  - **Depth** >2 mm (most important)
  - **Poor differentiation**
  - **Perineural invasion**
  - **Site** (ear, lip)
  - **Immunosuppression** (especially transplant)
  - **Large size** (>2 cm)
  - **Recurrence**
- **5-year survival:**
  - **Localized SCC:** 90-95%
  - **Regional lymph node metastasis:** 50-60%
  - **Distant metastasis:** 10-20%

**FOLLOW-UP:**
- **Skin check** every 3-6 months for 2 years, then annually
- **Lymph node examination** (at each visit)
- **Self-examination** (monthly)
- **Sun protection**

**PREVENTION:**
- **Sun protection** (critical):
  - **Sunscreen** SPF 30+
  - **Protective clothing**
  - **Avoid midday sun**
  - **No tanning beds**
- **Treat actinic keratoses** (cryotherapy, fluorouracil, photodynamic therapy)
- **Vitamin D supplementation** (if sun-avoiding)

**EVIDENCE:** NICE NG14, BAD Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified squamous cell carcinoma query",
                    "More aggressive than BCC (can metastasize)",
                    "Surgical excision (gold standard), consider sentinel lymph node biopsy for high-risk"
                ],
                capabilities_used=["skin_cancer_excision"],
                metadata={
                    "topic": "squamous_cell_carcinoma",
                    "guideline": "nice_ng14"
                }
            )

        # Melanoma
        elif any(term in query_lower for term in [
            "melanoma", "malignant melanoma", "changing mole", "suspicious mole"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**MALIGNANT MELANOMA**

**WHAT IS IT?**
- **Most serious type of skin cancer**
- **Arises from melanocytes**
- **Can metastasize early** (high mortality if late diagnosis)
- **Increasing incidence** (fastest increasing cancer in fair-skinned populations)
- **Sun exposure** (especially intermittent, intense sun exposure)

**RISK FACTORS:**
- **UV exposure** (sun, tanning beds - strong association)
- **Fair skin** (Fitzpatrick I-II) - higher risk
- **Sunburns** (especially in childhood/adolescence)
- **Numerous naevi** (>100 common naevi)
- **Atypical naevi** (dysplastic naevi)
- **Family history** of melanoma (2x increased risk)
- **Previous melanoma** (5x increased risk)
- **Genetic predisposition** (CDKN2A mutation - rare)
- **Immunosuppression**

**CLINICAL FEATURES:**

**ABCDE Criteria (For Suspicious Pigmented Lesion):**
- **A:** Asymmetry (one half unlike the other)
- **B:** Border (irregular, scalloped, poorly defined)
- **C:** Colour (variegated - shades of brown, black, red, white, blue)
- **D:** Diameter (>6 mm, although small melanomas occur)
- **E:** Evolving (changing in size, shape, colour)
- **Elevation** is NOT a criterion (nodular melanoma may be elevated)

**Red Flags (Urgent Referral):**
- **New nodule** arising in existing naevus
- **Change in size, shape, colour** (especially rapid)
- **Bleeding, ulceration, crusting**
- **Itching, pain** (late signs)

**TYPES:**

**Superficial Spreading Melanoma (Most Common - 70%):**
- **Radial growth phase** (horizontal spread)
- **Common on trunk** (men), legs (women)
- **Better prognosis** (diagnosed earlier)

**Nodular Melanoma (Most Aggressive - 15-20%):**
- **Vertical growth phase** (rapid deep invasion)
- **Nodular** (may be amelanotic - pink/red)
- **Worse prognosis** (often diagnosed late)

**Lentigo Maligna Melanoma (5-10%):**
- **Arises in lentigo maligna** (Hutchinson's freckle)
- **Chronic sun-damaged skin** (face, neck)
- **Large, flat, tan/brown patch** with variable colour
- **Better prognosis** (radial growth phase for months-years)

**Acral Lentiginous Melanoma (5-10%):**
- **Palms, soles, nailbeds**
- **Most common** in dark-skinned individuals
- **Often diagnosed late** (poor prognosis)

**Amelanotic Melanoma (Rare):**
- **No pigment** (pink/red nodule)
- **Often diagnosed late** (mimics pyogenic granuloma, BCC, SCC)

**DIAGNOSIS:**

**Biopsy:**
- **Excisional biopsy** with 1-3 mm margin (gold standard)
- **Incisional biopsy** if large lesion (avoid complete excision without margins)
- **DO NOT** shave biopsy (inadequate depth assessment)
- **DO NOT** diathermy/destroy lesion (histological assessment needed)

**Histology (Definitive Diagnosis):**
- **Breslow thickness** (most important prognostic factor)
- **Clark level** (anatomical level of invasion - less important since Breslow)
- **Ulceration** (adverse prognostic factor)
- **Mitotic rate** (number of mitoses/mm²)
- **Margin status** (positive vs negative)
- **Satellite metastases** (microscopic satellites around primary)

**BRESLOW THICKNESS (PROGNOSIS):**
- **<0.8 mm:** Excellent prognosis (10-year survival 95%)
- **0.8-1.0 mm:** Good prognosis (10-year survival 90%)
- **1.0-2.0 mm:** Intermediate prognosis (10-year survival 80%)
- **2.0-4.0 mm:** Poor prognosis (10-year survival 65%)
- **>4.0 mm:** Very poor prognosis (10-year survival 50%)

**MANAGEMENT:**

**Surgical Excision (Primary Treatment):**
- **Wide local excision**
  - **Margins:** (depends on Breslow thickness)
    - **In situ melanoma:** 5-10 mm
    - **<1 mm:** 1 cm
    - **1-2 mm:** 1-2 cm
    - **>2 mm:** 2 cm
  - **Primary closure** (if possible)
  - **Skin graft or local flap** (if large defect)
- **Sentinel lymph node biopsy** (if Breslow >0.8 mm or ulcerated)
- **Outcomes:**
  - Local recurrence: 3-5%
  - 10-year survival: Depends on stage (see staging)

**Sentinel Lymph Node Biopsy (SLNB):**
- **Indicated for:**
  - **Melanoma >0.8 mm Breslow** (or ulcerated)
  - **Clinically negative nodes**
- **Procedure:**
  - **Preoperative lymphoscintigraphy** (identify sentinel node)
  - **Intraoperative gamma probe** (localize sentinel node)
  - **Excise sentinel node** (1-3 nodes)
  - **Histological examination** (H&E, immunohistochemistry)
- **Outcomes:**
  - If SLNB negative: No further lymph node surgery needed
  - If SLNB positive: Consider completion lymph node dissection (CLND) or clinical trial

**Completion Lymph Node Dissection (CLND):**
- **Indicated if:**
  - **Positive sentinel lymph node** (some patients)
  - **Clinically positive lymph nodes**
- **Procedure:**
  - Remove all lymph nodes in draining nodal basin
- **Outcomes:**
  - **Regional control** (reduces regional recurrence)
  - **NO survival benefit** (MSLT-II trial)
  - **Significant morbidity** (lymphoedema 20-30%)
- **Alternative:** Observation with ultrasound (for patients with low tumour burden in sentinel node)

**Adjuvant Therapy:**
- **Immunotherapy** (nivolumab, pembrolizumab) for Stage III melanoma
- **Targeted therapy** (vemurafenib, cobimetinib) for BRAF-mutant melanoma
- **Clinical trials** (ongoing)

**Metastatic Melanoma (Stage IV):**
- **Immunotherapy** (nivolumab, pembrolizumab, ipilimumab) - first-line
- **Targeted therapy** (BRAF inhibitors + MEK inhibitors) if BRAF-mutant
- **Chemotherapy** (dacarbazine) - palliative, limited efficacy
- **Clinical trials** (ongoing)

**STAGING (AJCC 8th Edition):**

**Stage 0:** In situ melanoma (Tis N0 M0)
**Stage IA:** <0.8 mm without ulceration (T1a N0 M0)
**Stage IB:** <0.8 mm with ulceration OR 0.8-1.0 mm (T1b N0 M0)
**Stage IIA:** 1.0-2.0 mm without ulceration OR 2.0-4.0 mm without ulceration (T2b-T3a N0 M0)
**Stage IIB:** 1.0-2.0 mm with ulceration OR 2.0-4.0 mm with ulceration OR >4.0 mm without ulceration (T2b-T3b N0 M0)
**Stage IIC:** >4.0 mm with ulceration (T3b N0 M0)
**Stage III:** Regional lymph node metastasis (any T N1-3 M0)
**Stage IV:** Distant metastasis (any T any N M1)

**PROGNOSIS:**
- **10-year survival:**
  - **Stage I:** 95-98%
  - **Stage II:** 80-90%
  - **Stage III:** 40-70%
  - **Stage IV:** 10-20%
- **Most important prognostic factor:** Breslow thickness

**FOLLOW-UP:**
- **Regular skin checks** (every 3-12 months depending on stage)
- **Lymph node examination** (at each visit)
- **Imaging** (CT, PET) for Stage III/IV (every 3-12 months)
- **Self-examination** (monthly - patient and partner)
- **Sun protection** (critical for prevention of second melanoma)

**PREVENTION:**
- **Sun protection** (critical):
  - **Sunscreen** SPF 30+ (reapply every 2 hours)
  - **Protective clothing** (hat, long sleeves)
  - **Avoid midday sun** (10 am - 4 pm)
  - **No tanning beds** (major risk factor)
- **Early detection** (ABCDE criteria, regular skin checks)
- **Excision of atypical naevi** (controversial - not routinely recommended)

**EVIDENCE:** NICE NG14, BAD Guidelines""",
                confidence=0.95,
                reasoning_trace=[
                    "Identified malignant melanoma query",
                    "Most serious skin cancer, can metastasize early",
                    "Excisional biopsy, wide local excision, sentinel lymph node biopsy if >0.8 mm"
                ],
                capabilities_used=["skin_cancer_excision"],
                metadata={
                    "topic": "malignant_melanoma",
                    "guideline": "nice_ng14"
                }
            )

        # General skin cancer
        else:
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**SKIN CANCER**

**COMMON TYPES:**

**Basal Cell Carcinoma (BCC)**
- Most common skin cancer
- Locally invasive, rarely metastasizes
- Sun-exposed areas (face, neck, scalp)
- Pearly nodule, ulceration
- Surgical excision (gold standard) or Mohs

**Squamous Cell Carcinoma (SCC)**
- Second most common
- Can metastasize (unlike BCC)
- Sun-exposed areas
- Hyperkeratotic plaque, ulceration
- Surgical excision, consider sentinel lymph node biopsy

**Malignant Melanoma**
- Most serious skin cancer
- Can metastasize early
- ABCDE criteria (Asymmetry, Border, Colour, Diameter, Evolving)
- Excisional biopsy (1-3 mm margin)
- Wide local excision (margins depend on Breslow thickness)

**DIAGNOSIS:**
- **Clinical examination** (ABCDE criteria, features of BCC/SCC)
- **Dermoscopy** (improves diagnostic accuracy)
- **Biopsy** (excisional, incisional, punch)
- **Histology** (definitive diagnosis)

**TREATMENT:**
- **Surgical excision** (most common, gold standard for BCC/SCC/melanoma)
- **Mohs surgery** (high-risk BCC/SCC, facial lesions)
- **Radiotherapy** (patients not surgical candidates, adjuvant)
- **Topical therapies** (imiquimod, 5-FU for superficial BCC)
- **Cryotherapy** (small, low-risk BCC)

**PREVENTION:**
- **Sun protection** (critical):
  - Sunscreen SPF 30+ (reapply every 2 hours)
  - Protective clothing (hat, long sleeves)
  - Avoid midday sun (10 am - 4 pm)
  - No tanning beds
- **Early detection** (regular skin checks, self-examination)
- **Treat actinic keratoses** (precursors to SCC)

**PROGNOSIS:**
- **BCC:** Excellent (rarely metastasizes)
- **SCC:** Good (5-10% metastasize, higher if high-risk)
- **Melanoma:** Depends on stage (95% 10-year survival Stage I, 10-20% Stage IV)

**EVIDENCE:** NICE NG14""",
                confidence=0.87,
                reasoning_trace=[
                    "Provided skin cancer overview",
                    "BCC most common, SCC second, melanoma most serious",
                    "Sun protection critical for prevention"
                ],
                capabilities_used=["skin_cancer_excision"],
                metadata={
                    "topic": "skin_cancer_general",
                    "guideline": "nice_ng14"
                }
            )

    def _handle_breast_reconstruction_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle breast reconstruction queries"""
        return DomainQueryResult(
            domain_name="plastic_surgery",
            answer="""**BREAST RECONSTRUCTION**

**TIMING:**
- **Immediate:** At time of mastectomy (most common)
- **Delayed:** Months/years after mastectomy (if adjuvant radiotherapy, patient preference)
- **Delayed-immediate:** Tissue expander placed at mastectomy, reconstructed later

**TYPES:**

**Implant-Based Reconstruction:**
- **Expander/Implant** (most common)
  - **Tissue expander** placed at mastectomy
  - **Expanded** over weeks-months (serial saline injections)
  - **Replaced** with permanent implant
  - OR **Direct-to-implant** (if adequate skin)
- **Advantages:**
  - Simpler surgery
  - Shorter recovery
  - No donor site morbidity
- **Disadvantages:**
  - Multiple procedures (expander changes, implant exchange)
  - Capsular contracture (10-20%)
  - Implant rupture/leak
  - May need revision over time
  - Less natural feel/ appearance than autologous
  - Not suitable if radiotherapy planned (higher complication rate)

**Autologous (Flap) Reconstruction:**
- **DIEP flap** (Deep Inferior Epigastric Perforator) - gold standard
  - **Abdominal tissue** (skin, fat, blood vessels)
  - **Preserves rectus muscle** (muscle-sparing)
  - **Natural feel/ appearance**
  - **Abdominoplasty effect** (bonus)
  - **Longer surgery** (6-8 hours)
  - **Donor site morbidity** (abdominal scar, weakness, hernia risk)
- **TRAM flap** (Transverse Rectus Abdominis Myocutaneous)
  - **Abdominal tissue** with rectus muscle
  - **Pedicle or free**
  - **Higher morbidity** than DIEP (muscle sacrifice)
- **Latissimus dorsi flap**
  - **Back tissue** (muscle, skin, fat)
  - **Often combined with implant** (for volume)
  - **Reliable flap**
  - **Donor site morbidity** (back scar, weakness)
  - May cause **back pain**, **shoulder dysfunction**
- **SGAP flap** (Superior Gluteal Artery Perforator) - buttock tissue
- **IGAP flap** (Inferior Gluteal Artery Perforator) - buttock tissue
- **TUG flap** (Transverse Upper Gracilis) - inner thigh tissue
- **Free flaps** (microsurgery - higher risk, longer surgery)

**COMBINATION (Hybrid):**
- **Latissimus dorsi + implant**
- **DIEP + fat grafting**
- **Other flap + implant**

**CHOOSING RECONSTRUCTION:**

**Factors Favoring Implant:**
- **Bilateral reconstruction** (symmetry easier to achieve)
- **Slim patient** (insufficient donor tissue)
- **No radiotherapy** planned
- **Patient preference** (avoid donor site morbidity)
- **Comorbidities** (may preclude long flap surgery)

**Factors Favoring Autologous:**
- **Radiotherapy planned** or received (flap tolerates radiotherapy better)
- **Abdominal tissue available** (tummy tuck effect)
- **Natural feel/ appearance** important
- **Long-term durability** (flaps last, implants may not)
- **Previous implant failure**
- **Patient preference** (own tissue)

**COMPLICATIONS:**

**Implant-Based:**
- **Capsular contracture** (10-20%)
- **Infection** (2-5%)
- **Implant rupture/leak** (1-2% per year)
- **Implant malposition**
- **Revision surgery** (20-30% at 10 years)

**Autologous:**
- **Flap loss** (1-2% for free flaps)
- **Fat necrosis** (10-20%)
- **Donor site morbidity** (abdominal weakness, hernia, back pain)
- **Infection** (2-5%)
- **Revision surgery** (20-30% at 10 years)

**PROSTHESIS-NIPPLE RECONSTRUCTION:**
- **Nipple reconstruction** (3-6 months after breast reconstruction)
- **Tattooing** (for areola - 2-3 months after nipple reconstruction)
- **3D tattooing** (nipple-areolar complex simulated with tattoo only)
- **Nipple sharing** (from contralateral nipple)

**CONTRAINDDICATIONS:**
- **Active smoking** (delayed wound healing, flap loss)
- **Uncontrolled diabetes** (delayed wound healing, infection)
- **Obesity** (higher complication rate)
- **Previous abdominal surgery** (may preclude DIEP/TRAM)

**RECOVERY:**
- **Implant-based:** 2-4 weeks
- **Autologous:** 6-8 weeks (off work 4-8 weeks)
- **No heavy lifting** for 6-12 weeks (autologous)

**PATIENT SATISFACTION:**
- **High** (80-90% satisfied with reconstruction)
- **Better quality of life** vs no reconstruction
- **Psychological benefit** (body image, self-esteem)

**EVIDENCE:** NICE NG101, BAPRAS Guidelines""",
            confidence=0.91,
            reasoning_trace=[
                "Provided breast reconstruction overview",
                "Implant-based vs autologous (DIEP gold standard for autologous)",
                "Choice depends on radiotherapy, body habitus, patient preference"
            ],
            capabilities_used=["reconstructive_surgery_consultation"],
            metadata={
                "topic": "breast_reconstruction",
                "guideline": "nice_ng101"
            }
        )

    def _handle_wound_management_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle wound management queries"""
        query_lower = query.lower()

        # Diabetic foot ulcer
        if any(term in query_lower for term in [
            "diabetic ulcer", "diabetic foot ulcer", "diabetic foot", "diabetic wound"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**DIABETIC FOOT ULCER**

**DEFINITION:**
- **Full-thickness wound** below ankle in diabetic patient
- **Most common cause** of foot ulceration in diabetes
- **Major cause** of amputation (85% of amputations preceded by ulcer)

**AETIOLOGY:**
- **Neuropathy** (peripheral neuropathy - loss of protective sensation)
- **Ischaemia** (peripheral arterial disease)
- **Trauma** (minor injury goes unnoticed due to neuropathy)
- **Infection** (complicates ulcers, may lead to sepsis)
- **High plantar pressure** (deformity, callus)

**ASSESSMENT:**

**1. Vascular Assessment**
- **ABPI** (Ankle Brachial Pressure Index)
  - 0.9-1.3: Normal
  - 0.7-0.9: Borderline
  - <0.7: Significant arterial disease
  - >1.3: Calcified vessels (unreliable)
- **Doppler waveform** (triphasic, biphasic, monophasic)
- **TcPO2** (transcutaneous oxygen pressure) if ABPI unreliable
- **Consider angiography** if ischaemia suspected

**2. Neurological Assessment**
- **10 g monofilament** (test protective sensation)
- **Vibration perception** (128 Hz tuning fork)
- **Pinprick sensation**
- **Ankle reflexes**

**3. Wound Assessment**
- **Size, depth** (probe to bone)
- **Infection** signs (erythema, discharge, odour)
- **Callus** (debride to assess underlying ulcer)
- **Sinus tract** (may probe to bone)

**4. Infection Assessment**
- **Mild:** Superficial, <2 cm cellulitis
- **Moderate:** >2 cm cellulitis, spread to fascia
- **Severe:** Systemic signs (fever, leukocytosis, metabolic instability)

**CLASSIFICATION:**

**Wagner Classification:**
- **Grade 0:** No ulcer, high-risk foot
- **Grade 1:** Superficial ulcer
- **Grade 2:** Deep ulcer to tendon, bone, joint
- **Grade 3:** Deep ulcer with abscess, osteomyelitis
- **Grade 4:** Gangrene of toes/forefoot
- **Grade 5:** Extensive gangrene of foot

**MANAGEMENT:**

**1. Debridement:**
- **Remove necrotic tissue** (sharp debridement - scalpel, scissors)
- **Remove callus** (relieve pressure, assess underlying ulcer)
- **Infection control** (debridement reduces bacterial load)
- **Promote healing** (convert chronic to acute wound)
- **Avoid debridement** if severe ischaemia (revascularize first)

**2. Infection Control:**
- **Mild:** Oral antibiotics (co-amoxiclav, clindamycin, ciprofloxacin)
- **Moderate:** IV antibiotics (same as mild, but IV)
- **Severe:** IV broad-spectrum (piperacillin-tazobactam, vancomycin, clindamycin)
- **Duration:** 1-2 weeks (soft tissue infection), 4-6 weeks (osteomyelitis)
- **Osteomyelitis** (probe to bone + X-ray/MRI): 4-6 weeks IV antibiotics ± surgery

**3. Offloading (Critical):**
- **Total contact cast (TCC)** (gold standard)
  - Irremovable cast
  - Reduces plantar pressure by 80-90%
  - Changed weekly (or weekly, cast changed to debride, reassess)
  - Contraindicated if severe ischaemia or infection
- **Removable cast walker** (if TCC not possible)
  - Less effective (patient may not wear 24/7)
  - Consider "instant TCC" (cast walker wrapped with plaster/fibreglass)
- **Therapeutic footwear** (for healed ulcer - prevention)

**4. Wound Dressings:**
- **Maintain moist wound healing**
- **Absorb exudate**
- **Deslough** (cadexomer iodine, hydrogels)
- **Antimicrobial** (silver, iodine, honey - if infection)
- **No single dressing proven superior**

**5. Glycaemic Control:**
- **Target HbA1c** <48 mmol/mol (<6.5%)
- **Insulin** (often required during active ulceration)
- **Close monitoring** (hypo/hyperglycaemia)

**6. Vascular Assessment:**
- **Revascularization** if significant ischaemia
  - **Angioplasty** (first-line)
  - **Bypass surgery** (if angioplasty not possible)
  - **Major amputation** if unreconstructable

**7. Advanced Therapies:**
- **Negative pressure wound therapy (NPWT)**
  - **Indicated for:** Deep ulcers, post-debridement, surgical wounds
  - **Vacuum-assisted closure** (VAC)
  - **Contraindicated** if: Untreated infection, osteomyelitis, ischaemia
- **Hyperbaric oxygen** (controversial)
  - **May be considered for:** Non-healing ulcers despite optimal care
  - **Limited availability**
  - **Costly**
- **Growth factors, bioengineered skin substitutes** (expensive, limited availability)

**8. Surgery:**
- **Debridement** (sharp, in theatre if extensive)
- **Amputation** (if extensive gangrene, sepsis)
  - **Minor amputation** (toe, transmetatarsal) - preserves limb function
  - **Major amputation** (below-knee, above-knee) - if extensive tissue loss, unreconstructable ischaemia

**PROGNOSIS:**
- **Healing rate:** 50-70% with optimal care (over 12-20 weeks)
- **Recurrence rate:** 30-50% at 3 years
- **Amputation rate:** 15-20% (minor + major)
- **Mortality:** 5-10% per year (higher after amputation)
- **Better outcomes with:**
  - Multidisciplinary team (diabetologist, podiatry, plastic surgery, vascular surgery)
  - Early intervention
  - Optimal glycaemic control
  - Revascularization (if ischaemia)
  - Offloading (critical)

**PREVENTION:**
- **Foot care education** (daily inspection, proper footwear)
- **Regular podiatry** (callus debridement, nail care)
- **Optimal glycaemic control**
- **Stop smoking**
- **Regular foot screening** (annual for all diabetics)

**EVIDENCE:** NICE NG19, IWGDF Guidelines""",
                confidence=0.93,
                reasoning_trace=[
                    "Identified diabetic foot ulcer query",
                    "Multidisciplinary approach critical",
                    "Debridement, offloading, infection control, revascularization"
                ],
                capabilities_used=["wound_management"],
                metadata={
                    "topic": "diabetic_foot_ulcer",
                    "guideline": "nice_ng19"
                }
            )

        # Pressure ulcer
        elif any(term in query_lower for term in [
            "pressure sore", "pressure ulcer", "decubitus ulcer", "bedsore"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**PRESSURE ULCER (PRESSURE INJURY)**

**DEFINITION:**
- **Localized damage** to skin and underlying tissue
- **Caused by pressure** (often with shear, friction)
- **Over bony prominence**
- **Most common** in immobile patients

**RISK FACTORS:**
- **Immobility** (spinal cord injury, stroke, critical illness)
- **Poor nutrition** (malnutrition, low albumin)
- **Incontinence** (moisture causes maceration)
- **Age** >65 years (thinner skin, less subcutaneous tissue)
- **Reduced sensation** (spinal cord injury, neuropathy)
- **Comorbidities** (diabetes, vascular disease, COPD)

**COMMON SITES:**
- **Sacrum** (most common)
- **Heels** (second most common)
- **Trochanters** (hips)
- **Ischium** (buttocks)
- **Occiput** (back of head - in bedbound patients)
- **Spine**, **elbows**, **ankles**

**CLASSIFICATION (NPIAP 2019):**

**Stage 1:**
- Non-blanchable erythema of intact skin
- Persistent redness (does not turn white when pressed)
- May be painful, itchy, or asymptomatic

**Stage 2:**
- Partial-thickness skin loss with exposed dermis
- Red-pink wound bed
- May be intact blister or open ulcer

**Stage 3:**
- Full-thickness skin loss
- Fat visible
- May include undermining/tunneling

**Stage 4:**
- Full-thickness skin and tissue loss
- Muscle, bone, tendon exposed
- Undermining/tunneling common

**Unstageable:**
- Full-thickness skin and tissue loss
- Covered by slough/eschar (obscures depth)
- Once debrided, staged (usually Stage 3 or 4)

**Deep Tissue Pressure Injury (DTPI):**
- Persistent non-blanchable deep red, maroon, purple discoloration
- May look like bruise
- May evolve rapidly to Stage 3/4 or resolve with treatment

**PREVENTION:**
- **Regular repositioning** (every 2-4 hours)
- **Pressure-relieving surfaces** (mattress, cushion)
- **Skin care** (keep clean, dry, moisturized)
- **Nutrition** (adequate protein, calories)
- **Incontinence management** (prompt pad changes, barrier creams)
- **Education** (patient, family, caregivers)

**MANAGEMENT:**

**1. Relieve Pressure:**
- **Repositioning** (every 2-4 hours)
- **Pressure-relieving mattress** (dynamic air mattress for Stage 3/4)
- **Offloading** (pressure redistribution - pillows, foam wedges)

**2. Debridement:**
- **Remove necrotic tissue** (slough, eschar)
- **Sharp debridement** (scalpel, scissors - in theatre if extensive)
- **Autolytic debridement** (hydrogels, dressings)
- **Enzymatic debridement** (collagenase - rarely used)
- **Larval therapy** (maggots - for sloughy wounds)
- **Avoid debridement** if eschar on heels (may be body's natural protection)

**3. Infection Control:**
- **Swab for culture** (if signs of infection)
- **Oral antibiotics** (if cellulitis: co-amoxiclav, clindamycin, ciprofloxacin)
- **IV antibiotics** (if systemic signs, osteomyelitis suspected)
- **Osteomyelitis** (probe to bone, X-ray, MRI, bone scan): IV antibiotics 4-6 weeks

**4. Wound Dressings:**
- **Maintain moist wound healing**
- **Absorb exudate**
- **Antimicrobial** (silver, iodine, honey - if infected)
- **No single dressing proven superior**
- **Dressings:**
  - **Hydrogels** (dry sloughy wounds)
  - **Foams** (moderate to high exudate)
  - **Alginates** (high exudate)
  - **Antimicrobial** (silver, iodine - if infected)
  - **Negative pressure** (large Stage 3/4, surgical wounds)

**5. Nutrition:**
- **Adequate calories** (30-35 kcal/kg/day)
- **Adequate protein** (1.2-1.5 g/kg/day)
- **Vitamin C** (500 mg BD)
- **Zinc** (40 mg OD) if deficient
- **Consider supplements** if malnourished
- **Dietician referral** (if malnourished)

**6. Surgery:**
- **Debridement** (sharp, in theatre)
- **Direct closure** (rare - high tension, high recurrence)
- **Skin graft** (split-thickness skin graft) - Stage 3/4
- **Flap reconstruction** (Stage 4, recurrent, large defects)
  - **Muscle flap** (gluteus maximus, tensor fasciae latae)
  - **Perforator flap** (gluteal artery perforator)
  - **Free flap** (rare - if local options exhausted)
- **Amputation** (rare - if extensive gangrene, sepsis)

**7. Adjunctive Therapies:**
- **Negative pressure wound therapy (NPWT/VAC)**
  - **Indicated for:** Stage 3/4, post-debridement wounds
  - **Promotes granulation**
  - **Reduces edema**
  - **Contraindicated** if: Untreated infection, osteomyelitis, malignancy
- **Electrical stimulation** (may improve healing)
- **Hyperbaric oxygen** (controversial, limited evidence)
- **Therapeutic ultrasound** (limited evidence)

**PROGNOSIS:**
- **Healing rate:**
  - Stage 1-2: 70-90% (with optimal care)
  - Stage 3-4: 50-70% (may require surgery)
- **Recurrence rate:** 30-50% (if pressure relief not maintained)
- **Mortality:** 5-10% per year (higher with Stage 3/4, comorbidities)
- **Better outcomes with:**
  - Multidisciplinary team (nursing, medicine, surgery, dietetics, physiotherapy)
  - Early intervention
  - Optimal nutrition
  - Pressure relief
  - Surgery (for Stage 3/4)

**COMPLICATIONS:**
- **Infection** (most common complication)
- **Osteomyelitis** (bone infection - requires IV antibiotics)
- **Sepsis** (may lead to death)
- **Pain**
- **Malodor** (management with charcoal dressings, metronidazole gel)
- **Exudate** (heavy exudate may require frequent dressing changes, NPWT)

**PREVENTION (Critical):**
- **Risk assessment** (Braden, Norton, Waterlow scales)
- **Regular repositioning** (every 2-4 hours)
- **Pressure-relieving surfaces** (mattress, cushion)
- **Skin inspection** (daily - identify early Stage 1)
- **Skin care** (keep clean, dry, moisturized)
- **Nutrition** (adequate protein, calories, fluids)
- **Incontinence management** (prompt pad changes, barrier creams)
- **Education** (patient, family, staff)

**EVIDENCE:** NICE NG179, NPIAP Guidelines""",
                confidence=0.92,
                reasoning_trace=[
                    "Identified pressure ulcer query",
                    "Prevention critical (repositioning, pressure relief)",
                    "Staging (Stage 1-4, unstageable, DTPI)"
                ],
                capabilities_used=["wound_management"],
                metadata={
                    "topic": "pressure_ulcer",
                    "guideline": "nice_ng179"
                }
            )

        # General wound management
        else:
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**WOUND MANAGEMENT**

**TYPES OF WOUNDS:**

**Acute Wounds:**
- Surgical wounds
- Traumatic wounds
- Burns
- Healing by primary intention (sutures) or secondary intention (granulation)

**Chronic Wounds:**
- Diabetic foot ulcers
- Venous leg ulcers
- Arterial ulcers
- Pressure ulcers
- Non-healing >6 weeks

**WOUND HEALING PHASES:**

**1. Haemostasis (Immediate)**
- Vasoconstriction, platelet aggregation, clot formation

**2. Inflammation (Days 1-6)**
- Vasodilation, neutrophil infiltration, debridement

**3. Proliferation (Days 4-14)**
- Granulation tissue, angiogenesis, collagen deposition, epithelialization

**4. Maturation (Day 14 onwards)**
- Collagen remodeling, scar formation

**PRINCIPLES OF WOUND MANAGEMENT:**

**1. Assess Wound:**
- Size, depth, edges
- Exudate (amount, type)
- Tissue type (granulation, slough, necrotic)
- Infection signs
- Surrounding skin

**2. Optimize Healing Environment:**
- **Moist wound healing** (not wet, not dry)
- **Debridement** (remove necrotic tissue)
- **Infection control** (antimicrobials if infected)
- **Exudate management** (absorbent dressings)

**3. Dressing Selection:**
- **Hydrogels** (dry, sloughy wounds)
- **Foams** (moderate exudate)
- **Alginates** (high exudate, haemostatic)
- **Antimicrobials** (silver, iodine - if infected)
- **Negative pressure** (large, deep wounds)

**4. Address Underlying Causes:**
- **Ischaemia** (revascularization)
- **Venous hypertension** (compression)
- **Diabetes** (glycaemic control, offloading)
- **Pressure** (relief, redistribution)
- **Nutrition** (protein, calories, micronutrients)

**5. Adjunctive Therapies:**
- **Negative pressure** (VAC)
- **Hyperbaric oxygen** (selected wounds)
- **Growth factors**
- **Skin grafts, flaps**

**COMPLICATIONS:**
- Infection (most common)
- Delayed healing
- Hypertrophic scars, keloids
- Marjolin's ulcer (malignant change in chronic wound - rare)

**EVIDENCE:** NICE Guidelines""",
                confidence=0.85,
                reasoning_trace=[
                    "Provided wound management overview",
                    "Wound healing phases (haemostasis, inflammation, proliferation, maturation)"
                ],
                capabilities_used=["wound_management"],
                metadata={
                    "topic": "wound_management_general"
                }
            )

    def _handle_scar_management_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle scar management queries"""
        query_lower = query.lower()

        # Keloid scar
        if any(term in query_lower for term in [
            "keloid", "keloid scar", "raised scar", "hypertrophic keloid"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**KELOID SCAR**

**WHAT IS IT?**
- **Excessive scar tissue** extending beyond original wound
- **Benign** but can cause significant cosmetic/functional problems
- **More common** in darker skin (Fitzpatrick IV-VI)
- **Younger age** (10-30 years)
- **Certain sites** (earlobe, sternum, deltoid, upper back)

**RISK FACTORS:**
- **Genetic predisposition** (family history)
- **Skin type** (darker skin - African, Asian, Hispanic)
- **Age** (10-30 years)
- **Site** (earlobe, sternum, deltoid, upper back)
- **Tension** (wound under tension)
- **Infection** (postoperative wound infection)
- **Delayed healing**

**DIFFERENTIAL DIAGNOSIS:**

**Keloid vs Hypertrophic Scar:**

| Feature | Keloid | Hypertrophic Scar |
|---------|--------|-------------------|
| Extends beyond wound | Yes | No |
| Regression | Rare | Common (over months-years) |
| Recurrence after excision | High (50-100%) | Low |
| Site predilection | Earlobe, sternum, deltoid | Anywhere |
| Histology | Thick hyalinized collagen | Type III collagen |

**MANAGEMENT:**

**Prevention:**
- **Meticulous surgical technique** (minimal tension, gentle tissue handling)
- **Closed incision** (avoid sutures under tension)
- **Sterile technique** (avoid infection)
- **Postoperative silicone** (gel/sheets) for 3-6 months
- **Pressure therapy** (earlobes - pressure earrings)
- **Avoid elective surgery** in high-risk patients (if possible)

**Non-Surgical Treatments:**

**Silicone Gel/Sheets (First-Line):**
- **Mechanism:** Unknown (may hydrate stratum corneum, regulate fibroblast activity)
- **Apply** for 12-23 hours/day (sheets), twice daily (gel)
- **Duration:** 3-6 months
- **Efficacy:** 60-70% improvement (flattening, softening, reduced erythema)
- **Safe,** minimal side effects

**Corticosteroid Injections (Second-Line):**
- **Triamcinolone** (10-40 mg/mL)
- **Inject** into keloid (every 4-6 weeks)
- **3-5 sessions** typically needed
- **Efficacy:** 50-80% improvement (flattening, softening)
- **Side effects:**
  - Pain, bruising at injection site
  - Skin atrophy, hypopigmentation, telangiectasia
  - Systemic absorption (rare - if high dose)

**Pressure Therapy:**
- **Custom-made pressure garments**
- **Wear 23 hours/day** (for 6-12 months)
- **Efficacy:** 50-70% improvement
- **Particularly effective** for earlobe keloids (pressure earrings)

**Cryotherapy:**
- **Liquid nitrogen** (freeze keloid)
- **2-3 freeze-thaw cycles** per session
- **1-3 sessions** (4-6 weeks apart)
- **Efficacy:** 50-70% improvement
- **Side effects:** Pain, blistering, hypopigmentation

**Radiotherapy:**
- **Superficial X-rays** (adjunct to surgical excision)
- **Given postoperatively** (within 24-48 hours)
- **3-5 fractions** (total 10-15 Gy)
- **Efficacy:** 80-90% reduction in recurrence (when combined with surgery)
- **Contraindicated** in pregnancy, children, certain sites (breast, thyroid)

**Laser Therapy:**
- **Pulsed-dye laser** (PDL) - erythema, vascularity
- **CO2 laser** (ablation)
- **Efficacy:** Limited evidence
- **Often used** as adjunct to other treatments

**5-Fluorouracil (5-FU) Injections:**
- **Chemotherapy** (inhibits fibroblast proliferation)
- **Inject** intralesionally
- **Often combined** with steroid injections
- **Efficacy:** Similar to steroids
- **Side effects:** Pain, ulceration (if too much)

**Surgical Excision:**
- **Indicated for:**
  - Symptomatic keloids (pain, itch, contracture)
  - Failed non-surgical treatment
  - Patient preference
- **Recurrence rate:** 50-100% (if excision alone)
- **Combination therapy** (to reduce recurrence):
  - **Excision + steroid injections** (intraoperative, postoperative)
  - **Excision + radiotherapy** (postoperative)
  - **Excision + silicone/pressure** (postoperative)
- **Techniques:**
  - **Intralesional excision** (remove keloid from inside, leave wound edges)
  - **Z-plasty, W-plasty** (reduce tension)
  - **Skin graft** (if wound too large for primary closure)

**PROGNOSIS:**
- **High recurrence** after excision alone (50-100%)
- **Recurrence reduced** with combination therapy (10-30%)
- **Better outcomes** with early intervention
- **Worse outcomes** with:
  - Previous keloid excision
  - Large keloids
  - High-risk sites (sternum, earlobe)
  - Darker skin type

**PATIENT INFORMATION:**
- **Benign** (not cancerous)
- **Chronic condition** (may recur after treatment)
- **Prevention** critical (avoid elective surgery in high-risk patients)
- **Early treatment** (smaller keloids respond better)
- **Combination therapy** better than single modality

**EVIDENCE:** BAPRAS Guidelines, IACS Guidelines""",
                confidence=0.91,
                reasoning_trace=[
                    "Identified keloid scar query",
                    "Distinguished from hypertrophic scar",
                    "Silicone first-line, steroid injections second-line, surgery with adjuncts (recurrence high)"
                ],
                capabilities_used=["scar_management"],
                metadata={
                    "topic": "keloid_scar",
                    "guideline": "bapras"
                }
            )

        # Hypertrophic scar
        elif any(term in query_lower for term in [
            "hypertrophic scar", "raised scar", "thick scar"
        ]):
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**HYPERTROPHIC SCAR**

**WHAT IS IT?**
- **Raised, thickened scar** within boundaries of original wound
- **Benign** (not cancerous)
- **Common** after surgery, trauma, burns
- **May regress** over time (unlike keloids)

**RISK FACTORS:**
- **Tension** (wound under tension)
- **Infection** (postoperative wound infection)
- **Delayed healing**
- **Burn scars** (especially deep partial-thickness, full-thickness)
- **Younger age** (more active fibroblasts)
- **Genetic predisposition** (family history)

**DIFFERENTIAL DIAGNOSIS:**

**Hypertrophic vs Keloid:**

| Feature | Hypertrophic Scar | Keloid |
|---------|------------------|--------|
| Extends beyond wound | No | Yes |
| Regression | Common (over months-years) | Rare |
| Recurrence after excision | Low | High (50-100%) |
| Site predilection | Anywhere (over joints, under tension) | Earlobe, sternum, deltoid |
| Histology | Type III collagen | Thick hyalinized collagen |

**MANAGEMENT:**

**Prevention:**
- **Meticulous surgical technique** (minimal tension, gentle tissue handling)
- **Closed incision** (avoid sutures under tension)
- **Sterile technique** (avoid infection)
- **Silicone gel/sheets** postoperatively (for 3-6 months)
- **Pressure therapy** (for burns, grafts)

**Non-Surgical Treatments:**

**Silicone Gel/Sheets (First-Line):**
- **Apply** for 12-23 hours/day (sheets), twice daily (gel)
- **Duration:** 3-6 months
- **Efficacy:** 70-80% improvement (flattening, softening, reduced erythema)
- **Safe,** minimal side effects

**Corticosteroid Injections (Second-Line):**
- **Triamcinolone** (10-40 mg/mL)
- **Inject** into scar (every 4-6 weeks)
- **3-5 sessions** typically needed
- **Efficacy:** 70-90% improvement
- **Side effects:** Pain, bruising, skin atrophy, hypopigmentation

**Pressure Therapy:**
- **Custom-made pressure garments**
- **Wear 23 hours/day** (for 6-12 months)
- **Efficacy:** 70-80% improvement
- **Particularly effective** for burn scars

**Laser Therapy:**
- **Pulsed-dye laser** (PDL) - erythema, vascularity
- **CO2 laser** (ablative - vaporizes scar tissue)
- **Fractionated laser** (microscopic columns of ablation)
- **Efficacy:** Variable, limited high-quality evidence
- **Often used** as adjunct to other treatments

**Surgical Excision:**
- **Indicated for:**
  - Symptomatic scars (pain, itch, contracture)
  - Cosmetic concerns
  - Failed non-surgical treatment
  - Functional limitation (e.g., over joint, limiting range of motion)
- **Recurrence rate:** 30-50% (lower than keloid)
- **Combination therapy** (to reduce recurrence):
  - **Excision + steroid injections** (intraoperative, postoperative)
  - **Excision + silicone/pressure** (postoperative)
  - **Z-plasty, W-plasty** (reduce tension, change direction)
  - **Skin graft** (if wound too large for primary closure)
- **Outcomes:**
  - 70-80% good/excellent
  - Recurrence: 30-50% (lower with adjuncts)

**PROGNOSIS:**
- **Good** (most improve with non-surgical treatment)
- **Regression** common over 1-2 years (unlike keloids)
- **Better outcomes** with early intervention
- **Recurrence** after excision: 30-50% (lower than keloid)

**PATIENT INFORMATION:**
- **Benign** (not cancerous)
- **Common** after surgery, trauma, burns
- **May regress** over time
- **Treatment effective** (silicone, steroids, surgery)
- **Prevention** critical (silicone postoperatively)

**EVIDENCE:** BAPRAS Guidelines, IACS Guidelines""",
                confidence=0.90,
                reasoning_trace=[
                    "Identified hypertrophic scar query",
                    "Distinguished from keloid (does not extend beyond wound, may regress)",
                    "Silicone first-line, steroid injections second-line"
                ],
                capabilities_used=["scar_management"],
                metadata={
                    "topic": "hypertrophic_scar",
                    "guideline": "bapras"
                }
            )

        # General scar management
        else:
            return DomainQueryResult(
                domain_name="plastic_surgery",
                answer="""**SCAR MANAGEMENT**

**TYPES OF SCARS:**

**Normal (Mature) Scar:**
- Flat, pale, soft
- Final result of wound healing (12-18 months)

**Hypertrophic Scar:**
- Raised, thickened
- Within boundaries of original wound
- May regress over time

**Keloid Scar:**
- Extends beyond original wound
- Does not regress
- High recurrence after excision

**Atrophic Scar:**
- Depressed, pitted (e.g., acne scars)
- Loss of collagen

**Contracture:**
- Scar tightening across joint
- Limits range of motion

**SCAR MATURATION:**
- **Immature scar** (red, raised, stiff, sensitive) - first 3 months
- **Maturing scar** (pink, softening) - 3-12 months
- **Mature scar** (pale, flat, soft) - 12-18 months

**MANAGEMENT:**

**Prevention:**
- **Meticulous surgical technique**
- **Minimal tension**
- **Sterile technique**
- **Silicone** postoperatively

**Non-Surgical:**
- **Silicone gel/sheets** (first-line)
- **Corticosteroid injections** (raised scars)
- **Pressure therapy** (burns, hypertrophic scars)
- **Laser therapy** (erythema, texture)
- **Make-up** (camouflage)

**Surgical:**
- **Scar revision** (excision, resuture)
- **Z-plasty, W-plasty** (change direction, reduce tension)
- **Skin graft** (if large defect)
- **Flap** (if deep defect, need bulk)

**TIMING:**
- **Wait 12 months** before intervention (allows scar maturation)
- **Earlier intervention** if complications (infection, dehiscence)

**EVIDENCE:** BAPRAS Guidelines""",
                confidence=0.84,
                reasoning_trace=[
                    "Provided scar management overview",
                    "Scar types (normal, hypertrophic, keloid, atrophic, contracture)"
                ],
                capabilities_used=["scar_management"],
                metadata={
                    "topic": "scar_management_general"
                }
            )

    def _handle_aesthetic_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle aesthetic (cosmetic) surgery queries"""
        return DomainQueryResult(
            domain_name="plastic_surgery",
            answer="""**AESTHETIC (COSMETIC) SURGERY**

**IMPORTANT NOTE:**
- Cosmetic surgery is **elective** (patient-driven)
- **NOT covered by NHS** (except in exceptional circumstances)
- **Realistic expectations** critical for patient satisfaction
- **Psychological assessment** important (body dysmorphic disorder)

**COMMON PROCEDURES:**

**Breast Augmentation:**
- **Implants** (silicone or saline)
- **Incisions:** Inframammary (crease under breast), periareolar (around nipple), axillary, transumbilical
- **Pocket:** Subglandular (over muscle) or submuscular (under muscle)
- **Risks:** Capsular contracture, implant rupture, infection, malposition, reoperation (20-30% at 10 years)
- **Recovery:** 2-4 weeks

**Breast Reduction (Reduction Mammaplasty):**
- **Indications:** Macromastia (large breasts causing back/neck/shoulder pain, shoulder groove, intertrigo)
- **Incisions:** Inferior pedicle, medial pedicle, vertical scar, periareolar
- **Recovery:** 4-6 weeks
- **Risks:** Scarring, infection, nipple loss, reduced/lost sensation, difficulty breastfeeding

**Abdominoplasty (Tummy Tuck):**
- **Indications:** Excess abdominal skin/fat (post-pregnancy, weight loss)
- **Plication** of rectus muscles (if diastasis recti)
- **Umbilicus** transposed (new umbilicus created)
- **Recovery:** 4-6 weeks (no heavy lifting for 6-8 weeks)
- **Risks:** Scarring, infection, seroma, hematoma, wound dehiscence, umbilical necrosis, DVT/PE

**Rhinoplasty (Nose Job):**
- **Indications:** Cosmetic hump, bulbous tip, deviated septum
- **Approaches:** Open (columellar incision) vs closed (all incisions inside nose)
- **Osteotomies** (break nasal bones to reshape)
- **Septoplasty** (straighten septum if deviated)
- **Recovery:** 2-4 weeks (swelling may persist for 6-12 months)
- **Risks:** Bleeding, infection, nasal obstruction, unsatisfactory appearance (5-10% revision rate)

**Blepharoplasty (Eyelid Surgery):**
- **Upper blepharoplasty:** Remove excess skin, fat from upper eyelids
- **Lower blepharoplasty:** Remove excess skin, fat from lower eyelids (canthopexy to support lower eyelid)
- **Recovery:** 1-2 weeks
- **Risks:** Bleeding, infection, ectropion (eyelid pulls down), lagophthalmos (unable to close eye), unsatisfactory appearance (5% revision rate)

**Facelift (Rhytidectomy):**
- **Indications:** Aging face (jowls, neck laxity)
- **SMAS plication** (superficial musculoaponeurotic system - deeper layer)
- **Incisions:** Temporal, preauricular, postauricular, occipital
- **Recovery:** 2-4 weeks (bruising, swelling may persist for weeks)
- **Risks:** Bleeding, infection, nerve injury (facial nerve branches), hair loss, scarring, unsatisfactory appearance (10-15% revision rate)

**Liposuction:**
- **Indications:** Localized fat deposits resistant to diet/exercise
- **Common sites:** Abdomen, flanks, thighs, arms, neck
- **Technique:** Tumescent (inject fluid), suction cannula
- **Recovery:** 1-2 weeks
- **Risks:** Contour irregularities, seroma, infection, skin necrosis, DVT/PE

**Otoplasty (Ear Pinning):**
- **Indications:** Prominent ears (bat ears)
- **Technique:** Create antihelical fold, conchal setback (set back ear)
- **Recovery:** 1-2 weeks (headband for 4-6 weeks)
- **Risks:** Overcorrection, undercorrection, asymmetry, recurrence

**GENERAL PRINCIPLES:**

**Patient Selection:**
- **Realistic expectations** (critical)
- **Psychologically stable** (screen for body dysmorphic disorder)
- **Good medical health** (optimize comorbidities)
- **Non-smoker** (smoking increases complications)
- **Stable weight** (avoid significant weight fluctuations)

**Preoperative Assessment:**
- **Medical history** (comorbidities, medications, allergies)
- **Physical examination** (anatomy, skin quality)
- **Psychological assessment** (expectations, body dysmorphic disorder)
- **Photographs** (preoperative documentation)
- **Informed consent** (risks, benefits, alternatives)

**Risks of Cosmetic Surgery:**
- **Unsatisfactory result** (5-15% revision rate depending on procedure)
- **Scarring** (all procedures)
- **Infection** (1-5%)
- **Bleeding/hematoma** (1-5%)
- **Wound dehiscence** (1-5%)
- **Nerve injury** (variable depending on procedure)
- **DVT/PE** (0.5-2%)
- **Anesthesia risks**
- **Psychological impact** (depression, regret)

**PATIENT INFORMATION:**
- **Elective procedure** (patient choice, not medically necessary)
- **Realistic expectations** critical (photos of typical results)
- **Recovery varies** (weeks to months depending on procedure)
- **Scars** (all surgery leaves scars, plastic surgery attempts to hide/minimize)
- **Risk of revision** (5-15% depending on procedure)
- **Psychological impact** (dysphoria, depression common in early postoperative period)

**EVIDENCE:** BAPRAS Guidelines, ASAPS Guidelines""",
            confidence=0.86,
            reasoning_trace=[
                "Provided aesthetic surgery overview",
                "Patient selection critical (realistic expectations, stable psychology)",
                "Listed common procedures, risks, recovery"
            ],
            capabilities_used=["reconstructive_surgery_consultation"],
            metadata={
                "topic": "aesthetic_surgery"
            }
        )

    def _handle_general_plastic_surgery_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general plastic surgery queries"""
        return DomainQueryResult(
            domain_name="plastic_surgery",
            answer="""**PLASTIC SURGERY**

Plastic surgery is a specialty dealing with reconstructive and aesthetic surgery.

**RECONSTRUCTIVE SURGERY:**

**Skin Cancer**
- Basal cell carcinoma (most common)
- Squamous cell carcinoma
- Malignant melanoma (most serious)
- Excision with appropriate margins
- Mohs surgery (high-risk, facial lesions)
- Reconstruction (primary closure, skin graft, local flap)

**Breast Reconstruction**
- Implant-based (expander/implant)
- Autologous (DIEP flap, TRAM flap, latissimus dorsi flap)
- Immediate or delayed
- Nipple reconstruction, tattooing

**Head and Neck Reconstruction**
- After skin cancer excision, trauma
- Local flaps, free flaps
- Functional and aesthetic restoration

**HAND SURGERY:**

**Common Conditions:**
- Trigger finger (stenosing tenosynovitis)
- Dupuytren's contracture
- Ganglion cyst
- Carpal tunnel syndrome

**Trauma:**
- Tendon injuries (flexor, extensor)
- Nerve injuries (digital, median, ulnar)
- Fractures (phalanx, metacarpal)
- Finger amputation (replantation, revision)

**BURNS MANAGEMENT:**

**Classification:**
- By depth (superficial, partial-thickness, full-thickness)
- By TBSA (Total Body Surface Area)

**Management:**
- **Minor burns:** Cool running water, first aid dressings
- **Major burns:** Resuscitation (Parkland formula), escharotomy, transfer to burns centre
- **Skin grafting** (full-thickness burns, deep partial-thickness)
- **Scar management** (pressure garments, laser, surgery)

**WOUND MANAGEMENT:**

**Acute Wounds:**
- Surgical wounds, traumatic wounds
- Primary closure (sutures), secondary intention (granulation)

**Chronic Wounds:**
- Diabetic foot ulcers
- Venous leg ulcers
- Pressure ulcers
- Non-healing >6 weeks

**SCAR MANAGEMENT:**

**Types:**
- Normal (mature), hypertrophic, keloid, atrophic, contracture

**Treatment:**
- Silicone gel/sheets (first-line)
- Corticosteroid injections (raised scars)
- Pressure therapy (burns)
- Laser therapy (erythema, texture)
- Surgical revision (if symptomatic)

**AESTHETIC (COSMETIC) SURGERY:**

**Common Procedures:**
- Breast augmentation, reduction, lift
- Abdominoplasty (tummy tuck)
- Rhinoplasty (nose job)
- Blepharoplasty (eyelid surgery)
- Facelift
- Liposuction
- Otoplasty (ear pinning)

**GENERAL PRINCIPLES:**
- **Patient selection critical** (realistic expectations, stable psychology)
- **Informed consent** (risks, benefits, alternatives)
- **Surgical planning** (incision placement, tension-free closure)
- **Meticulous technique** (gentle tissue handling, hemostasis)
- **Postoperative care** (dressings, scar management, physiotherapy)

**EVIDENCE:** BAPRAS Guidelines, NICE Guidelines""",
            confidence=0.83,
            reasoning_trace=[
                "Provided plastic surgery overview",
                "Covered reconstructive, hand, burns, wound, scar, aesthetic surgery",
                "Emphasized patient selection and realistic expectations"
            ],
            capabilities_used=[
                "reconstructive_surgery_consultation",
                "hand_surgery_consultation"
            ],
            metadata={
                "topic": "plastic_surgery_general"
            }
        )


def create_plastic_surgery_domain():
    """Factory function for plastic surgery domain"""
    return PlasticSurgeryDomain()
