"""Stage 6 (Tier 1): the emergencies corpus — nobody dies of nothing.

The 2026-09-03 global audit fired 55 probes across trauma, obstetrics,
toxicology, oncology-supportive, derm emergencies, paediatric protection
and post-exposure prophylaxis: 19 returned an empty differential. This
corpus part closes those gaps. Every condition carries the full profile
standard; symptom tokens must appear in SYMPTOM_SYNONYMS_PART4 (the
corpus integrity test enforces it).

Sections (Tasks 6.3-6.7):
  6.3 trauma & burns      6.4 toxicology & withdrawal
  6.5 obstetric emergencies  6.6 oncology-supportive + derm emergencies
  6.7 paediatric protection & syndromes
"""
from typing import Dict, List

from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
)

CONDITIONS_PART4: List[ConditionProfile] = [
    # ================= 6.3 TRAUMA & BURNS =================
    ConditionProfile(
        condition_id="head_injury_moderate_severe",
        name="Moderate/severe traumatic brain injury",
        category="trauma",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("head_hit_event", 0.95, 0.55),
            # NB specificity 0.40 (was 0.80): 'blacked out when I stood
            # up' is syncope language — an emergency-tier TBI leading on
            # that single generic token floored the escalation to
            # emergency (Stage 7 contender-gate lesson). The strike story
            # (head_hit_event + vomiting/confusion tokens) carries a real
            # TBI, and the head_injury_red_flags safety rule carries the
            # 999 for actual head trauma regardless.
            SymptomFrequency("loss_of_consciousness", 0.80, 0.40),
            SymptomFrequency("vomiting_after_injury", 0.60, 0.85),
            SymptomFrequency("confusion_after_injury", 0.65, 0.85),
            SymptomFrequency("drowsiness", 0.60, 0.50),
            SymptomFrequency("clear_fluid_from_ear_nose", 0.10, 0.95),
            SymptomFrequency("focal_weakness_one_side", 0.30, 0.90),
        ],
        discriminators=["any loss of consciousness, amnesia or repeated "
                        "vomiting after head impact",
                        "warfarin/DOAC or bleeding disorder lowers every "
                        "threshold",
                        "deteriorating conscious level = extradural until "
                        "proven otherwise"],
        red_flags=["reduced GCS, unequal pupils, seizures, focal neurology",
                   "clear fluid from ear/nose (CSF leak) or bruising behind "
                   "both ears (Battle's sign)"],
        investigations=[
            InvestigationProfile("CT head (Canadian CT head rule / NICE CG176)",
                                 "indicated if LOC, amnesia, vomiting, GCS<15, "
                                 "focal deficit, anticoagulated, >65 with "
                                 "dangerous mechanism", 0.95, 0.70,
                                 "NICE CG176 head injury"),
        ],
        management_first_line="Do not allow to sleep unobserved; urgent CT "
                              "per rule; neurosurgical referral for any "
                              "intracranial injury.",
        referral_tier="emergency",
        safety_net="Anyone knocked out, vomiting, confused or drowsy after a "
                   "head injury needs emergency assessment now — lucid "
                   "intervals lie.",
        dangerous_mimic_of=["tension_headache", "migraine"],
        source="NICE CG176 head injury; Canadian CT head rule",
    ),
    ConditionProfile(
        condition_id="head_injury_mild",
        name="Mild head injury (no red flags)",
        category="trauma",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("head_hit_event", 0.95, 0.55),
            SymptomFrequency("headache_after_injury", 0.70, 0.45),
            SymptomFrequency("nausea_mild", 0.40, 0.10),
        ],
        discriminators=["fully conscious throughout, no vomiting, no "
                        "amnesia, not anticoagulated",
                        "headache settles over hours-days"],
        red_flags=["repeated vomiting, drowsiness, confusion, weakness, "
                   "seizure or clear fluid from ear/nose -> emergency now"],
        investigations=[],
        management_first_line="Rest, analgesia, adult observation for the "
                              "first 24h with written red-flag advice.",
        referral_tier="self_care",
        safety_net="Return immediately if vomiting repeatedly, becoming "
                   "drowsy or confused, weakness, seizure, or clear fluid "
                   "from ear or nose.",
        source="NICE CG176 head injury",
    ),
    ConditionProfile(
        condition_id="penetrating_torso_trauma",
        name="Penetrating chest/abdominal trauma",
        category="trauma",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("stab_or_gunshot", 0.95, 0.98),
            SymptomFrequency("breathless_acute", 0.60, 0.30),
            SymptomFrequency("wound_bleeding", 0.70, 0.40),
            SymptomFrequency("pale_cold_skin", 0.40, 0.60),
        ],
        discriminators=["any penetrating wound between neck and groin — "
                        "platen signs develop late",
                        "impaled objects are stabilised in place, never "
                        "removed"],
        red_flags=["expanding neck veins + silent chest = tension "
                   "pneumothorax; evisceration; absent pulses"],
        investigations=[
            InvestigationProfile("eFAST scan + trauma series", "at trauma "
                                 "centre before X-rays if unstable", 0.85,
                                 0.90, "ATLS 10th ed"),
        ],
        management_first_line="Call emergency services; control external "
                              "bleeding with direct pressure; do NOT remove "
                              "impaled objects; sit leaning injured-side "
                              "down if penetrating eye injury; nothing by "
                              "mouth.",
        referral_tier="emergency",
        safety_net="This is a surgical emergency — 999/ambulance now.",
        source="ATLS; trauma network practice",
    ),
    ConditionProfile(
        condition_id="blunt_chest_trauma",
        name="Blunt chest trauma (rib fracture / haemothorax)",
        category="trauma",
        prevalence_per_consult=0.0015,
        symptoms=[
            SymptomFrequency("chest_impact_event", 0.90, 0.85),
            SymptomFrequency("rib_pain_tender", 0.85, 0.70),
            SymptomFrequency("breathless_acute", 0.45, 0.30),
            SymptomFrequency("cough_after_injury", 0.30, 0.25),
            SymptomFrequency("pale_cold_skin", 0.20, 0.60),
        ],
        discriminators=["pain on breathing/pressing the ribs after impact",
                        "older or osteoporotic patients fracture with "
                        "minimal force"],
        red_flags=["breathlessness, coughing blood, or reduced breath "
                   "sounds -> pneumothorax/haemothorax",
                   "bruise pattern across the chest (seat-belt sign) marks "
                   "a high-energy transfer"],
        investigations=[
            InvestigationProfile("chest X-ray", "pneumothorax, haemothorax, "
                                 "fractures", 0.75, 0.85, "ATLS"),
        ],
        management_first_line="Analgesia good enough to breathe deeply "
                              "(rib fractures kill by splinting and "
                              "atelectasis); emergency assessment for any "
                              "breathlessness or high-energy mechanism.",
        referral_tier="emergency",
        safety_net="Return immediately for breathlessness, coughing blood, "
                   "or fever within days (pneumonia complicates rib "
                   "fractures).",
        source="ATLS; NICE NG39 major trauma",
    ),
    ConditionProfile(
        condition_id="haemorrhagic_shock",
        name="Haemorrhagic shock",
        category="trauma",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("pale_cold_skin", 0.90, 0.60),
            SymptomFrequency("rapid_weak_pulse", 0.70, 0.55),
            SymptomFrequency("visible_bleeding_severe", 0.60, 0.85),
            SymptomFrequency("dizzy_on_standing", 0.55, 0.25),
            SymptomFrequency("confusion_after_injury", 0.35, 0.30),
        ],
        discriminators=["pale, cold, clammy with fast weak pulse after "
                        "injury or bleeding — blood pressure is normal "
                        "until >30% lost (a late sign)",
                        "young patients compensate then collapse"],
        red_flags=["mottled skin, absent radial pulse, agitated confusion "
                   "= decompensated shock"],
        investigations=[
            InvestigationProfile("no investigation before control",
                                 "pressure -> emergency transfer; bloods "
                                 "en route, never a barrier to transfer",
                                 None, None, "ATLS"),
        ],
        management_first_line="Direct pressure on the bleeding point; lay "
                              "flat, keep warm; tourniquet above spurting "
                              "limb bleeding; emergency services now.",
        referral_tier="emergency",
        safety_net="Shock can develop over an hour after apparently minor "
                   "injury — any pallor, cold sweat or faintness after "
                   "injury means emergency review.",
        dangerous_mimic_of=["vasovagal_syncope"],
        source="ATLS 10th ed",
    ),
    ConditionProfile(
        condition_id="limb_fracture_closed",
        name="Closed limb fracture",
        category="trauma",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("limb_injury_event", 0.90, 0.60),
            SymptomFrequency("deformity_limb", 0.60, 0.90),
            SymptomFrequency("cannot_weight_bear", 0.70, 0.50),
            SymptomFrequency("swelling_after_injury", 0.70, 0.30),
        ],
        discriminators=["pain + swelling + bony tenderness + inability to "
                        "weight-bear (Ottawa ankle/knee rules)",
                        "deformity or crepitus is fracture until X-rayed"],
        red_flags=["numbness, pins-and-needles or white cold fingers/toes "
                   "beyond the injury = neurovascular compromise, emergency",
                   "tense compartment + pain on passive stretch = "
                   "compartment syndrome"],
        investigations=[
            InvestigationProfile("X-ray", "Ottawa rules gate the need",
                                 0.90, 0.90, "Ottawa ankle rules"),
        ],
        management_first_line="Immobilise, elevate, analgesia, same-day "
                              "fracture clinic / A&E; open wounds or "
                              "neurovascular change are emergencies.",
        referral_tier="urgent",
        safety_net="Numbness, pins-and-needles, or cold pale digits beyond "
                   "the injury — emergency now, not tomorrow.",
        source="Ottawa rules; NICE NG38 fractures",
    ),
    ConditionProfile(
        condition_id="limb_fracture_open",
        name="Open (compound) fracture",
        category="trauma",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("limb_injury_event", 0.95, 0.60),
            SymptomFrequency("bone_visible_wound", 0.80, 0.97),
            SymptomFrequency("wound_bleeding", 0.60, 0.40),
            SymptomFrequency("deformity_limb", 0.70, 0.90),
        ],
        discriminators=["any wound communicating with the fracture site — "
                        "even a tiny puncture over a deformity",
                        "farm/soil contamination = highest infection risk"],
        red_flags=["bone through skin, or a wound over the fracture point"],
        investigations=[
            InvestigationProfile("X-ray + surgical exploration",
                                 "in theatre; IV antibiotics and tetanus "
                                 "cover first", 0.95, 0.95,
                                 "NICE NG37 complex fractures"),
        ],
        management_first_line="Cover with sterile saline-soaked dressing, "
                              "no wound exploration; IV antibiotics + "
                              "tetanus; nil by mouth; emergency transfer.",
        referral_tier="emergency",
        safety_net="Emergency — risk of osteomyelitis and gas gangrene "
                   "without operative washout.",
        source="NICE NG37 complex fractures",
    ),
    ConditionProfile(
        condition_id="crush_injury",
        name="Crush injury / crush syndrome",
        category="trauma",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("trapped_crushed_duration", 0.90, 0.95),
            SymptomFrequency("limb_pain_swelling", 0.80, 0.40),
            SymptomFrequency("dark_urine", 0.40, 0.90),
            SymptomFrequency("pale_cold_skin", 0.35, 0.60),
            SymptomFrequency("confusion_after_injury", 0.25, 0.30),
        ],
        discriminators=["limb trapped under weight for >15 min — release "
                        "triggers reperfusion",
                        "dark urine = myoglobinuria: kidneys fail hours "
                        "later; also hyperkalaemia stops hearts"],
        red_flags=["trapped >4h, absent pulse, rigid swollen compartment"],
        investigations=[
            InvestigationProfile("potassium + CK + ECG", "before and "
                                 "immediately after release; continuous "
                                 "cardiac monitoring", 0.90, 0.80,
                                 "ATLS; earthquake-medicine literature"),
        ],
        management_first_line="Do not delay release but monitor for "
                              "reperfusion: IV fluids BEFORE release where "
                              "possible, cardiac monitor, emergency "
                              "transfer; tourniquet considered if trapped "
                              ">4h with no care available.",
        referral_tier="emergency",
        safety_net="Crush syndrome kills after rescue — fluids, potassium "
                   "check and monitoring are not optional.",
        source="ATLS; crush syndrome guidance",
    ),
    ConditionProfile(
        condition_id="major_burn",
        name="Major burn",
        category="trauma",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("burn_scald_large", 0.90, 0.90),
            SymptomFrequency("burn_face_airway", 0.25, 0.95),
            SymptomFrequency("blistered_skin", 0.70, 0.50),
            SymptomFrequency("breathless_acute", 0.25, 0.30),
            SymptomFrequency("singed_nasal_hairs", 0.15, 0.97),
        ],
        discriminators=[">10% total body surface area adult (>5% child), "
                        "or any burn to face/hands/feet/genitals/airway, or "
                        "circumferential, or full-thickness >5%",
                        "enclosed-space fire or singed nasal hairs = airway "
                        "burn: stridor can develop over hours"],
        red_flags=["hoarseness, stridor, singed nasal hairs, carbon in "
                   "sputum = airway burn — intubate early",
                   "circumferential limb/chest burn = escharotomy risk"],
        investigations=[
            InvestigationProfile("none before transfer", "Parkland fluid "
                                 "formula from the clock of the burn: "
                                 "3 mL x kg x %TBSA over 24h", None, None,
                                 "ATLS burn chapter"),
        ],
        management_first_line="Cool running water 20 min (within 3h of "
                              "burn), then clean cling-film covering, keep "
                              "warm, nothing by mouth, emergency transfer "
                              "to burn centre per referral criteria.",
        referral_tier="emergency",
        safety_net="Airway burns swell with no warning — any hoarse voice "
                   "or stridor after fire/smoke is an immediate 999.",
        source="ATLS; national burn network referral criteria",
    ),
    ConditionProfile(
        condition_id="minor_burn",
        name="Minor burn / scald",
        category="trauma",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("burn_scald_small", 0.90, 0.80),
            SymptomFrequency("blistered_skin", 0.60, 0.50),
            SymptomFrequency("painful_red_skin", 0.85, 0.40),
        ],
        discriminators=["<10% adult / <5% child, superficial or "
                        "partial-thickness, not face/hands/airway/genitals",
                        "blanching red = superficial; white/leathery = "
                        "full thickness, needs review"],
        red_flags=["any full-thickness area, >1cm blister clusters on "
                   "hands/face, or chemical/electrical burn -> urgent+ "
                   "assessment"],
        investigations=[],
        management_first_line="Cool running water 20 min; leave blisters "
                              "intact; non-adherent dressing; analgesia; "
                              "tetanus check.",
        referral_tier="self_care",
        safety_net="Spreading redness around the burn, fever, or increasing "
                   "pain after 2 days = infection — urgent review.",
        source="national burn first-aid guidance",
    ),
    ConditionProfile(
        condition_id="tetanus_prone_wound",
        name="Tetanus-prone wound",
        category="trauma",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("dirty_or_deep_wound", 0.85, 0.85),
            SymptomFrequency("tetanus_status_unknown", 0.60, 0.90),
            SymptomFrequency("soil_or_faecal_contamination", 0.40, 0.95),
            SymptomFrequency("wound_bleeding", 0.40, 0.40),
        ],
        discriminators=["deep puncture, soil/faecal/spit contamination, "
                        "devitalised tissue, or any wound with unknown "
                        "immunisation status",
                        "tetanus spores survive everywhere — rust is not "
                        "the marker, dirt is"],
        red_flags=["trismus (jaw spasm), back stiffness, facial spasm — "
                   "incubation 3-21 days; once spasms start, mortality "
                   "10-50%"],
        investigations=[
            InvestigationProfile("none — immune status history is the test",
                                 "decide vaccine vs immunoglobulin by wound "
                                 "class + vaccine history", None, None,
                                 "UK Green Book ch.30"),
        ],
        management_first_line="Clean and debride; complete primary course "
                              "or booster per schedule; tetanus "
                              "immunoglobulin for dirty wounds with "
                              "incomplete/unknown immunity — same day.",
        referral_tier="urgent",
        safety_net="Jaw stiffness, difficulty opening the mouth, or muscle "
                   "spasms days-weeks after any wound = emergency now.",
        dangerous_mimic_of=["wound_infection"],
        source="UK Green Book tetanus ch.30; WHO tetanus position",
    ),
    ConditionProfile(
        condition_id="wound_infection",
        name="Infected wound",
        category="trauma",
        prevalence_per_consult=0.006,
        symptoms=[
            SymptomFrequency("spreading_redness_wound", 0.80, 0.85),
            SymptomFrequency("pus_wound", 0.70, 0.85),
            SymptomFrequency("wound_pain_increasing", 0.75, 0.40),
            SymptomFrequency("fever", 0.40, 0.20),
        ],
        discriminators=["spreading redness, increasing pain after 2-3 days, "
                        "pus — infection declares itself by day 3",
                        "look for a retained foreign body in any infected "
                        "wound"],
        red_flags=["pain out of proportion + rapid spread + crepitus or "
                   "skin sloughing = necrotising infection, emergency",
                   "red streaking toward the axilla/groin = lymphangitis"],
        investigations=[],
        management_first_line="Swab; antibiotics per local guideline; open "
                              "and explore if abscess; remove sutures/foreign "
                              "body; mark the red margin and review 24-48h.",
        referral_tier="urgent",
        safety_net="If redness crosses the marked line, pain escalates "
                   "disproportionately, or the skin turns purple/black — "
                   "emergency now (necrotising fasciitis).",
        dangerous_mimic_of=["cellulitis"],
        source="NICE CG191; antimicrobial stewardship",
    ),
    ConditionProfile(
        condition_id="spinal_injury_suspect",
        name="Suspected spinal injury",
        category="trauma",
        prevalence_per_consult=0.0006,
        symptoms=[
            SymptomFrequency("spinal_pain_after_trauma", 0.85, 0.85),
            SymptomFrequency("limb_numbness_after_trauma", 0.50, 0.90),
            SymptomFrequency("high_energy_event", 0.70, 0.60),
            SymptomFrequency("focal_weakness_one_side", 0.30, 0.90),
        ],
        discriminators=["neck/mid-back pain after high-energy impact with "
                        "any limb numbness, tingling or weakness",
                        "diving into shallow water, ejection, fall >2m "
                        "= assume unstable spine"],
        red_flags=["any limb neurology after trauma; priapism; loss of "
                   "anal tone — immobilise and transfer"],
        investigations=[
            InvestigationProfile("whole-spine CT (or MRI if neurology)",
                                 "before any movement is permitted", 0.95,
                                 0.90, "NICE NG41 spinal injury"),
        ],
        management_first_line="Manual in-line stabilisation, log-roll, "
                              "immobilise; emergency transfer; pressure-"
                              "area care from minute one.",
        referral_tier="emergency",
        safety_net="New numbness or weakness after any fall or crash — "
                   "emergency now, keep still until assessed.",
        source="NICE NG41 spinal injury; ATLS",
    ),
    ConditionProfile(
        condition_id="intra_abdominal_injury",
        name="Blunt abdominal trauma (solid organ / bowel injury)",
        category="trauma",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("abdominal_impact_event", 0.90, 0.85),
            SymptomFrequency("abdominal_pain_after_impact", 0.85, 0.75),
            SymptomFrequency("guarding_rigidity", 0.50, 0.85),
            SymptomFrequency("pale_cold_skin", 0.35, 0.60),
            SymptomFrequency("shoulder_tip_pain", 0.25, 0.60),
        ],
        discriminators=["abdominal pain after impact — seat-belt bruise "
                        "marks small-bowel and mesenteric injury",
                        "left rib pain + shock = splenic rupture; shoulder-"
                        "tip pain signals diaphragmatic irritation"],
        red_flags=["rigid abdomen, shock, increasing distension"],
        investigations=[
            InvestigationProfile("eFAST at bedside; CT abdomen if stable",
                                 "bloods + crossmatch in parallel", 0.90,
                                 0.90, "ATLS"),
        ],
        management_first_line="Nil by mouth, IV access, emergency "
                              "transfer; do not palpate repeatedly — "
                              "examine once, gently.",
        referral_tier="emergency",
        safety_net="Abdominal pain worsening over hours after any impact, "
                   "with faintness or pallor — emergency now (delayed "
                   "splenic rupture is real).",
        source="ATLS 10th ed",
    ),
    # ================= 6.4 TOXICOLOGY & WITHDRAWAL =================
    ConditionProfile(
        condition_id="paracetamol_overdose",
        name="Paracetamol (acetaminophen) overdose",
        category="toxicology",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("overdose_event", 0.95, 0.75),
            SymptomFrequency("paracetamol_ingested", 0.90, 0.95),
            SymptomFrequency("staggered_over_hours", 0.25, 0.85),
            SymptomFrequency("nausea", 0.40, 0.10),
            SymptomFrequency("abdominal_pain", 0.25, 0.20),
        ],
        discriminators=["dose per kg and time since ingestion drive "
                        "everything: >150 mg/kg or staggered = treat",
                        "patients look well for 24-72h while the liver "
                        "dies — wellbeing predicts nothing"],
        red_flags=["staggered overdose over hours-days, unknown quantity, "
                   "or presentation >8h after ingestion",
                   "jaundice, drowsiness or bleeding = established liver "
                   "failure"],
        investigations=[
            InvestigationProfile("paracetamol level (4h post-ingestion) "
                                 "+ LFT/INR/creatinine",
                                 "plot on the treatment nomogram; INR is "
                                 "the liver-failure tracker", 0.95, 0.95,
                                 "TOXBASE; NICE NG16 self-harm"),
        ],
        management_first_line="TOXBASE/poison centre advice; N-acetyl-"
                              "cysteine per nomogram (start before levels "
                              "return if >8h or staggered); never discharge "
                              "without mental-health assessment if "
                              "deliberate.",
        referral_tier="emergency",
        safety_net="Any paracetamol overdose — however well the person "
                   "looks — needs same-day hospital assessment.",
        source="TOXBASE; UK paracetamol overdose guidelines",
    ),
    ConditionProfile(
        condition_id="opioid_overdose",
        name="Opioid overdose",
        category="toxicology",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("opioid_drug_context", 0.85, 0.90),
            SymptomFrequency("wont_wake", 0.75, 0.80),
            SymptomFrequency("pinpoint_pupils", 0.60, 0.90),
            SymptomFrequency("slow_breathing", 0.70, 0.75),
            SymptomFrequency("blue_lips", 0.35, 0.85),
        ],
        discriminators=["unresponsive with pinpoint pupils and slow "
                        "breathing after heroin/opioids",
                        "snoring/gurgling airway = dying sound"],
        red_flags=["respiratory rate <10, cyanosis, unrousable"],
        investigations=[],
        management_first_line="Call 999; rescue breathing/ventilation "
                              "FIRST (hypoxia kills before naloxone "
                              "arrives); naloxone if available; recovery "
                              "position; stay — naloxone wears off before "
                              "the opioid.",
        referral_tier="emergency",
        safety_net="Never leave an opioid-overdosed person alone once "
                   "roused — re-sedation after 30-90 minutes is expected.",
        source="WHO community management of opioid overdose",
    ),
    ConditionProfile(
        condition_id="tricyclic_overdose",
        name="Tricyclic antidepressant overdose",
        category="toxicology",
        prevalence_per_consult=0.0006,
        symptoms=[
            SymptomFrequency("overdose_event", 0.95, 0.75),
            SymptomFrequency("tca_drug_context", 0.90, 0.95),
            SymptomFrequency("drowsiness", 0.70, 0.50),
            SymptomFrequency("seizure", 0.25, 0.60),
            SymptomFrequency("blurred_vision", 0.40, 0.40),
            SymptomFrequency("palpitations", 0.40, 0.30),
        ],
        discriminators=["any amitriptyline-class overdose: the ECG QRS "
                        "width predicts seizures and arrhythmia",
                        "deterioration in the first 6h; sodium "
                        "bicarbonate is the antidote"],
        red_flags=["widened QRS >100ms, seizure, coma, temperature spike"],
        investigations=[
            InvestigationProfile("ECG (serial)", "QRS duration drives "
                                 "bicarbonate therapy", 0.85, 0.85,
                                 "TOXBASE"),
        ],
        management_first_line="Emergency transfer, IV access, serial ECG; "
                              "sodium bicarbonate for QRS >100ms or "
                              "seizures; never give anti-arrhythmics "
                              "class 1a.",
        referral_tier="emergency",
        safety_net="Tricyclic overdose kills by arrhythmia in the first "
                   "hours — emergency now, however well the person looks.",
        source="TOXBASE",
    ),
    ConditionProfile(
        condition_id="salicylate_overdose",
        name="Salicylate (aspirin) overdose",
        category="toxicology",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("overdose_event", 0.95, 0.75),
            SymptomFrequency("aspirin_ingested", 0.85, 0.95),
            SymptomFrequency("tinnitus", 0.45, 0.80),
            SymptomFrequency("hyperventilation", 0.40, 0.80),
            SymptomFrequency("nausea", 0.50, 0.10),
            SymptomFrequency("confusion", 0.30, 0.30),
        ],
        discriminators=["tinnitus + deep rapid breathing + vomiting after "
                        "aspirin (or salicylate-rich oil of wintergreen)",
                        "chronic therapeutic intoxication in the elderly "
                        "mimics delirium"],
        red_flags=["fever, confusion, seizures, non-cardiogenic pulmonary "
                   "oedema"],
        investigations=[
            InvestigationProfile("salicylate level + ABG + glucose + "
                                 "electrolytes", "levels guide "
                                 "haemodialysis; recheck 2h after "
                                 "ingestion", 0.90, 0.90, "TOXBASE"),
        ],
        management_first_line="Emergency transfer; activated charcoal if "
                              "<1h; urine alkalinisation; haemodialysis "
                              "for severe toxicity.",
        referral_tier="emergency",
        safety_net="Aspirin overdose worsens for hours — any tinnitus, "
                   "fast deep breathing or confusion after ingestion "
                   "means emergency assessment.",
        source="TOXBASE",
    ),
    ConditionProfile(
        condition_id="benzodiazepine_overdose",
        name="Benzodiazepine overdose",
        category="toxicology",
        prevalence_per_consult=0.0007,
        symptoms=[
            SymptomFrequency("overdose_event", 0.95, 0.75),
            SymptomFrequency("benzo_drug_context", 0.85, 0.95),
            SymptomFrequency("drowsiness", 0.80, 0.50),
            SymptomFrequency("slurred_speech", 0.60, 0.60),
        ],
        discriminators=["isolated benzo overdose is rarely fatal — "
                        "co-ingestion (opioids, alcohol) is what kills",
                        "flumazenil is dangerous in dependent users "
                        "(precipitates seizures)"],
        red_flags=["respiratory depression, co-ingestions, unknown "
                   "substances"],
        investigations=[],
        management_first_line="Emergency assessment and observation; "
                              "airway support; flumazenil only in "
                              "selected ventilated non-tolerant cases.",
        referral_tier="emergency",
        safety_net="Drowsiness deepening over hours, or any breathing "
                   "difficulty — emergency now.",
        source="TOXBASE",
    ),
    ConditionProfile(
        condition_id="carbon_monoxide_poisoning",
        name="Carbon monoxide poisoning",
        category="toxicology",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("fume_source_exposure", 0.75, 0.90),
            SymptomFrequency("multiple_household_affected", 0.50, 0.95),
            SymptomFrequency("headache", 0.85, 0.20),
            SymptomFrequency("nausea", 0.55, 0.10),
            SymptomFrequency("dizziness", 0.60, 0.20),
            SymptomFrequency("confusion", 0.35, 0.30),
        ],
        discriminators=["flu-like illness in several household members at "
                        "once, better outside the building, worse at "
                        "home — CO has no smell",
                        "winter + gas boiler/fire + headaches that ease "
                        "at work or school"],
        red_flags=["any loss of consciousness, chest pain, seizures, "
                   "pregnancy (fetal haemoglobin binds CO harder)"],
        investigations=[
            InvestigationProfile("carboxyhaemoglobin (blood gas, "
                                 "pre-oxygenation)",
                                 "CO-oximetry; pulse oximetry LIES "
                                 "(reads normal)", 0.90, 0.95,
                                 "NICE NG139 carbon monoxide"),
        ],
        management_first_line="Leave the source, fresh air, 999; high-flow "
                              "oxygen 15 L/non-rebreather; check everyone "
                              "else in the building; pregnancy = "
                              "hyperbaric discussion regardless of level.",
        referral_tier="emergency",
        safety_net="Symptoms that return on re-entering the building mean "
                   "the source is still active — stay out until the "
                   "boiler/appliance is checked.",
        source="NICE NG139 carbon monoxide",
    ),
    ConditionProfile(
        condition_id="alcohol_withdrawal_delirium",
        name="Alcohol withdrawal delirium (delirium tremens)",
        category="toxicology",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("alcohol_heavy_use", 0.85, 0.80),
            SymptomFrequency("stopped_drinking_recently", 0.75, 0.85),
            SymptomFrequency("tremor", 0.80, 0.40),
            SymptomFrequency("hallucinations", 0.50, 0.85),
            SymptomFrequency("confusion", 0.70, 0.30),
            SymptomFrequency("withdrawal_sweats", 0.65, 0.50),
            SymptomFrequency("seizure", 0.15, 0.60),
        ],
        discriminators=["6-72h after the last drink: coarse tremor, "
                        "sweats, confusion, visual hallucinations "
                       "(insects, rats), paranoia",
                        "DTs kill ~5% untreated — this is not 'shakes'"],
        red_flags=["hallucinations, disorientation, fever, seizure, "
                   "hypertension with tachycardia"],
        investigations=[
            InvestigationProfile("glucose, electrolytes (incl. magnesium), "
                                 "temperature, BP",
                                 "rule out hypoglycaemia and sepsis which "
                                 "co-present and kill faster", 0.60, 0.60,
                                 "NICE CG100/CG115 alcohol-use disorders"),
        ],
        management_first_line="Emergency/acute assessment; parenteral "
                              "benzodiazepines (chlordiazepoxide IV/IM or "
                              "lorazepam); thiamine BEFORE any glucose; "
                              "treat in a lit, familiar environment.",
        referral_tier="emergency",
        safety_net="Confusion, seeing things or a seizure in a heavy "
                   "drinker who has stopped = medical emergency, not "
                   "'drunk'.",
        source="NICE CG115; RCP alcohol withdrawal guidelines",
    ),
    ConditionProfile(
        condition_id="opiate_withdrawal",
        name="Opiate withdrawal",
        category="toxicology",
        prevalence_per_consult=0.0015,
        symptoms=[
            SymptomFrequency("opioid_dependent_context", 0.80, 0.90),
            SymptomFrequency("supply_interrupted", 0.75, 0.85),
            SymptomFrequency("yawning_runny_nose", 0.55, 0.80),
            SymptomFrequency("muscle_aches", 0.65, 0.40),
            SymptomFrequency("diarrhoea", 0.50, 0.20),
            SymptomFrequency("goosebumps_cold_flushes", 0.45, 0.85),
            SymptomFrequency("withdrawal_sweats", 0.60, 0.50),
        ],
        discriminators=["flu-like misery without fever: yawning, streaming "
                        "eyes/nose, gooseflesh, cramps, diarrhoea 6-24h "
                        "after last opiate",
                        "miserable, not dangerous — except in pregnancy "
                        "and in infants"],
        red_flags=["pregnancy (miscarriage risk), injected infection "
                   "signs, chest pain"],
        investigations=[],
        management_first_line="Supportive fluids, anti-emetics, "
                              "loperamide; assess for opioid substitution "
                              "therapy; never prescribe opioids to "
                              "relieve withdrawal on demand alone.",
        referral_tier="urgent",
        safety_net="Withdrawal itself is not life-threatening in adults — "
                   "but fever, chest pain or a red painful injection site "
                   "means something else is happening.",
        source="WHO/clinical guidelines opiate withdrawal",
    ),
    ConditionProfile(
        condition_id="serotonin_syndrome",
        name="Serotonin syndrome",
        category="toxicology",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("serotonergic_drug_context", 0.85, 0.90),
            SymptomFrequency("muscle_clonus_twitching", 0.70, 0.90),
            SymptomFrequency("withdrawal_sweats", 0.60, 0.50),
            SymptomFrequency("confusion", 0.55, 0.30),
            SymptomFrequency("tremor", 0.60, 0.40),
            SymptomFrequency("fever", 0.45, 0.20),
        ],
        discriminators=["the triad: clonus (ankle/inducible), autonomic "
                        "instability, agitation — after adding/raising an "
                        "SSRI, tramadol, linezolid or triptan",
                        "clonus distinguishes it from NMS (lead-pipe "
                        "rigidity, slower onset over days)"],
        red_flags=["temperature >38.5, hypertonicity, rigidity"],
        investigations=[],
        management_first_line="Stop the serotonergic drug; emergency "
                              "assessment; benzodiazepines for agitation; "
                              "cyproheptadine in severe cases; active "
                              "cooling.",
        referral_tier="emergency",
        safety_net="Twitching or shivering with confusion after a new "
                   "antidepressant or tramadol — emergency now.",
        source="Hunter serotonin toxicity criteria",
    ),
    ConditionProfile(
        condition_id="stimulant_toxicity",
        name="Stimulant toxicity (cocaine / MDMA / amphetamine)",
        category="toxicology",
        prevalence_per_consult=0.0006,
        symptoms=[
            SymptomFrequency("stimulant_drug_context", 0.85, 0.95),
            SymptomFrequency("agitation", 0.70, 0.50),
            SymptomFrequency("fever", 0.40, 0.20),
            SymptomFrequency("palpitations", 0.60, 0.30),
            SymptomFrequency("chest_pain", 0.35, 0.30),
            SymptomFrequency("muscle_clonus_twitching", 0.30, 0.90),
        ],
        discriminators=["agitated, hot, sweating, jaw clenching (MDMA), "
                        "chest pain after cocaine",
                        "hyperthermia + muscle rigidity = impending "
                        "rhabdomyolysis and death"],
        red_flags=["core temperature >39.5, seizures, chest pain, "
                   "agitation needing restraint"],
        investigations=[],
        management_first_line="Emergency: active cooling, benzodiazepines "
                              "in generous doses, fluids; treat cocaine "
                              "chest pain as ACS (avoid beta-blockers).",
        referral_tier="emergency",
        safety_net="Anyone hot, agitated and twitching after stimulants "
                   "needs emergency care now — cooled, not calmed down at "
                   "home.",
        source="TOXBASE; recreational-drug toxicity guidance",
    ),
    ConditionProfile(
        condition_id="methanol_glycol_poisoning",
        name="Methanol / ethylene glycol poisoning",
        category="toxicology",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("methanol_source_context", 0.70, 0.95),
            SymptomFrequency("drunk_then_deteriorating", 0.70, 0.90),
            SymptomFrequency("visual_disturbance", 0.40, 0.40),
            SymptomFrequency("abdominal_pain", 0.50, 0.20),
            SymptomFrequency("confusion", 0.50, 0.30),
        ],
        discriminators=["drunk-like intoxication from spirits/antifreeze/"
                        "windscreen wash that then deteriorates over "
                        "6-30h with deep breathing",
                        "methanol blinds (permanent), glycol destroys "
                        "kidneys — both fatal without antidote"],
        red_flags=["any visual change after bootleg spirit ingestion; "
                   "no urine output"],
        investigations=[
            InvestigationProfile("blood gas (anion-gap acidosis) + osmolar "
                                 "gap + calcium",
                                 "the acidosis severity drives dialysis",
                                 0.80, 0.85, "TOXBASE"),
        ],
        management_first_line="Emergency transfer; fomepizole or ethanol "
                              "antidote; haemodialysis for acidosis/renal "
                              "failure; thiamine+pyridoxine adjuncts.",
        referral_tier="emergency",
        safety_net="Drunkenness that keeps deepening hours later, or any "
                   "blurred vision after drinking unfamiliar spirits — "
                   "emergency now.",
        source="TOXBASE",
    ),
    ConditionProfile(
        condition_id="organophosphate_poisoning",
        name="Organophosphate / pesticide poisoning",
        category="toxicology",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("pesticide_exposure", 0.85, 0.95),
            SymptomFrequency("drooling_salivation", 0.60, 0.85),
            SymptomFrequency("pinpoint_pupils", 0.60, 0.90),
            SymptomFrequency("generalised_weakness", 0.55, 0.50),
            SymptomFrequency("withdrawal_sweats", 0.55, 0.50),
            SymptomFrequency("vomiting", 0.60, 0.15),
            SymptomFrequency("slow_pulse", 0.35, 0.80),
        ],
        discriminators=["the SLUDGE picture after pesticide/spray "
                        "exposure: salivation, lacrimation, urination, "
                        "diarrhoea, GI cramps, emesis + pinpoint pupils",
                        "a major killer of farm workers worldwide; skin "
                        "and clothes carry the poison"],
        red_flags=["weakness of neck/breathing muscles, bradycardia, "
                   "seizures, coma"],
        investigations=[
            InvestigationProfile("RBC cholinesterase activity",
                                 "confirms exposure (often unavailable — "
                                 "treat on toxidrome)", 0.80, 0.85,
                                 "WHO pesticide poisoning guidance"),
        ],
        management_first_line="Decontaminate (gloves, remove clothes, "
                              "wash skin), 999/emergency; atropine in "
                              "repeating doses until chest clear; "
                              "pralidoxime early; protect yourself from "
                              "contamination.",
        referral_tier="emergency",
        safety_net="Anyone exposed to pesticide spray who is sweating, "
                   "drooling or weak needs emergency care now — handle "
                   "their clothes with gloves.",
        source="WHO clinical management of pesticide poisoning",
    ),
    ConditionProfile(
        condition_id="snake_envenomation",
        name="Snake envenomation",
        category="toxicology",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("snake_bite", 0.95, 0.98),
            SymptomFrequency("bite_site_swelling", 0.70, 0.70),
            SymptomFrequency("bleeding_gums_unexplained", 0.30, 0.85),
            SymptomFrequency("nausea", 0.40, 0.10),
            SymptomFrequency("regional_lymph_pain", 0.30, 0.70),
            SymptomFrequency("drooling_salivation", 0.15, 0.85),
        ],
        discriminators=["any snake bite: 20-40% are dry bites, but "
                        "envenoming declares within hours — spreading "
                        "swelling, tender nodes, bleeding gums, drooping "
                        "eyelids (elapids)",
                        "viper pain/swelling at the site vs elapid "
                        "neurotoxicity with minimal local change"],
        red_flags=["any systemic sign: bleeding, ptosis, swallowing "
                   "difficulty, dark urine, rapid spreading pain"],
        investigations=[
            InvestigationProfile("20-minute whole-blood clotting test "
                                 "(bedside)",
                                 "blood that fails to clot in a clean "
                                 "glass = haemotoxic envenoming", 0.85,
                                 0.85, "WHO snakebite guidelines"),
        ],
        management_first_line="Keep the limb STILL and level, remove "
                              "rings; splint; no tourniquet, no cutting, "
                              "no sucking; emergency transfer to a "
                              "hospital with antivenom; mark and time the "
                              "swelling margin.",
        referral_tier="emergency",
        safety_net="A snake bite with no symptoms yet still needs "
                   "hospital observation for at least 24h — envenoming "
                   "can begin hours later.",
        source="WHO guidelines for the management of snakebites",
    ),
    # ================= 6.5 OBSTETRIC EMERGENCIES =================
    ConditionProfile(
        condition_id="eclampsia",
        name="Eclampsia",
        category="obstetrics",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("pregnancy_context", 0.90, 0.60),
            SymptomFrequency("seizure", 0.90, 0.60),
            SymptomFrequency("headache", 0.50, 0.05),
            SymptomFrequency("visual_disturbance", 0.35, 0.35),
            SymptomFrequency("swelling_hands_face", 0.35, 0.55),
        ],
        discriminators=["any seizure or unresponsive collapse after 20 "
                        "weeks of pregnancy, in labour, or within 6 weeks "
                        "of birth — eclampsia until proven otherwise",
                        "can occur without prior headache, swelling or "
                        "recorded hypertension"],
        red_flags=["seizure, coma, breathing difficulty after a fit, "
                   "fewer than 4 reflexes/eyelid flicker after seizure"],
        investigations=[
            InvestigationProfile("BP + proteinuria + bloods (FBC, renal, "
                                 "liver, platelets, coagulation)",
                                 "severity and HELLP screen; do not delay "
                                 "treatment for results", 0.80, 0.80,
                                 "NICE NG133 hypertension in pregnancy"),
        ],
        management_first_line="999; left-lateral recovery position during "
                              "fits; magnesium sulfate IV (loading then "
                              "infusion); senior obstetric + anaesthetic "
                              "call; the only cure is delivery.",
        referral_tier="emergency",
        safety_net="Any fit, severe headache, visual change or pain under "
                   "the ribs in pregnancy — emergency now, not tomorrow.",
        source="NICE NG133; WHO maternal health",
    ),
    ConditionProfile(
        condition_id="postpartum_haemorrhage",
        name="Postpartum haemorrhage (PPH)",
        category="obstetrics",
        prevalence_per_consult=0.0006,
        symptoms=[
            SymptomFrequency("birth_recently", 0.95, 0.90),
            SymptomFrequency("bleeding_heavy", 0.95, 0.75),
            SymptomFrequency("pale_cold_skin", 0.45, 0.60),
            SymptomFrequency("dizzy_on_standing", 0.40, 0.25),
            SymptomFrequency("rapid_weak_pulse", 0.35, 0.55),
        ],
        discriminators=["bleeding >500 mL after birth, or any bleeding "
                        "that soaks a pad an hour — the 4 Ts: Tone "
                        "(atony, commonest), Tissue (retained), Trauma, "
                        "Thrombin",
                        "delayed PPH after going home: retained products "
                        "or infection until proven otherwise"],
        red_flags=["soaking pads hourly, passing clots the size of an "
                   "egg or larger, faintness, pale clammy — shock can "
                   "develop in minutes"],
        investigations=[],
        management_first_line="999; lie flat, elevate legs; uterine "
                              "massage (rub up the fundus) if trained; "
                              "empty bladder; keep baby to breast "
                              "(oxytocin); save any passed tissue/clots "
                              "for examination.",
        referral_tier="emergency",
        safety_net="After any birth: a pad an hour soaked, clots bigger "
                   "than an egg, faintness or feeling cold and clammy — "
                   "emergency now.",
        source="WHO PPH recommendations; RCOG green-top 52",
    ),
    ConditionProfile(
        condition_id="imminent_birth",
        name="Imminent birth / active labour",
        category="obstetrics",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("contractions_frequent", 0.85, 0.80),
            SymptomFrequency("pushing_sensation", 0.60, 0.85),
            SymptomFrequency("crowning_head_visible", 0.35, 0.97),
            SymptomFrequency("waters_broke_gush", 0.50, 0.55),
            SymptomFrequency("pregnancy_context", 0.85, 0.60),
        ],
        discriminators=["contractions <3 min apart lasting >45s, or any "
                        "urge to push, or the baby's head visible — birth "
                        "is minutes away",
                        "call an ambulance if birth is imminent and no "
                        "midwife present; do NOT travel in a private car "
                        "at this stage"],
        red_flags=["cord prolapse (cord at the vagina), bleeding at the "
                   "height of a contraction, head delivered >60s without "
                   "the body following"],
        investigations=[],
        management_first_line="Call 999 / midwife NOW; keep mum calm and "
                              "warm; clean towels; if the head is visible "
                              "do NOT push her legs together — support "
                              "the perineum, deliver onto her abdomen, "
                              "dry and warm the baby skin-to-skin.",
        referral_tier="emergency",
        safety_net="Cord felt at the vagina: kneel on all fours with "
                   "bottom raised and call 999 immediately.",
        source="emergency birth guidance; RCOG",
    ),
    ConditionProfile(
        condition_id="obstructed_labour",
        name="Obstructed / prolonged labour",
        category="obstetrics",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("labour_prolonged", 0.90, 0.90),
            SymptomFrequency("contractions_frequent", 0.60, 0.80),
            SymptomFrequency("abdominal_pain", 0.80, 0.20),
            SymptomFrequency("exhaustion", 0.60, 0.30),
        ],
        discriminators=["labour >12h (multip) / >6h active (primip) with "
                        "no descent — obstruction until assessed; in "
                        "low-resource settings this is the fistula and "
                        "death pathway",
                        "bladder distension, bandl's ring (uterine "
                        "rupture precursor), fetal head high"],
        red_flags=["contractions stopping with continuous pain (rupture), "
                   "fever, foul discharge, maternal exhaustion"],
        investigations=[],
        management_first_line="Emergency obstetric transfer; nil by "
                              "mouth; IV fluids; bladder catheter; do not "
                              "push oxytocin in obstruction.",
        referral_tier="emergency",
        safety_net="Labour lasting many hours with no progress, or "
                   "contractions that fade into constant pain — emergency "
                   "transfer now.",
        source="WHO obstructed labour guidance",
    ),
    ConditionProfile(
        condition_id="shoulder_dystocia",
        name="Shoulder dystocia",
        category="obstetrics",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("head_delivered_body_stuck", 0.95, 0.97),
            SymptomFrequency("birth_recently", 0.60, 0.90),
            SymptomFrequency("exhaustion", 0.30, 0.30),
        ],
        discriminators=["head born, rest not following with routine "
                        "traction — the clock starts: 5-minute window to "
                        "the baby's brain"],
        red_flags=["head delivered >60s without the body"],
        investigations=[],
        management_first_line="Call for emergency help; HELPERR: call "
                              "help, episiotomy evaluation, legs "
                              "McRoberts (knees to chest), suprapubic "
                              "pressure; do NOT pull the head/neck.",
        referral_tier="emergency",
        safety_net="This is an every-second emergency during birth — it "
                   "happens where the birth happens and needs the "
                   "emergency services on the line.",
        source="RCOG green-top 42 shoulder dystocia",
    ),
    ConditionProfile(
        condition_id="cord_prolapse",
        name="Cord prolapse",
        category="obstetrics",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("cord_felt_visible", 0.85, 0.97),
            SymptomFrequency("waters_broke_gush", 0.60, 0.55),
            SymptomFrequency("pregnancy_context", 0.60, 0.60),
        ],
        discriminators=["cord at or below the vagina after the waters "
                        "break, often with the baby's heart-rate "
                        "dropping — pressure on the cord strangles the "
                        "baby"],
        red_flags=["anything prolapsing from the vagina after membrane "
                   "rupture in labour"],
        investigations=[],
        management_first_line="999; knee-to-chest or all-fours position "
                              "with hips high; if present, gently lift "
                              "the presenting part off the cord (fingers "
                              "in vagina, lifting the head) and hold "
                              "until caesarean.",
        referral_tier="emergency",
        safety_net="Cord felt — position hips high and call 999; do not "
                   "wait to see if it settles.",
        source="RCOG green-top 50 cord prolapse",
    ),
    ConditionProfile(
        condition_id="miscarriage_threatened",
        name="Threatened miscarriage",
        category="obstetrics",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("pregnancy_context", 0.90, 0.60),
            SymptomFrequency("vaginal_bleeding", 0.95, 0.60),
            SymptomFrequency("lower_abdominal_pain", 0.40, 0.15),
        ],
        discriminators=["bleeding <24 weeks with a closed cervix; many "
                        "settle — but an ectopic can present identically",
                        "the EPU scan is what separates threatened "
                        "miscarriage from missed/ectopic — clinical "
                        "gestation alone cannot"],
        red_flags=["heavy bleeding with clots/dizziness, one-sided pain, "
                   "shoulder-tip pain (ectopic)"],
        investigations=[
            InvestigationProfile("early pregnancy unit scan + hCG "
                                 "trajectory",
                                 "location and viability", 0.95, 0.90,
                                 "NICE NG126 ectopic and miscarriage"),
        ],
        management_first_line="Same-day EPU assessment (under 18 weeks); "
                              "rest does not prevent miscarriage; "
                              "anti-D if rhesus negative; return "
                              "immediately for heavy bleeding, pain or "
                              "dizziness.",
        referral_tier="urgent",
        safety_net="Bleeding that soaks a pad an hour, faintness, or "
                   "one-sided/shoulder-tip pain — emergency now.",
        dangerous_mimic_of=["ectopic_pregnancy"],
        source="NICE NG126",
    ),
    ConditionProfile(
        condition_id="miscarriage_incomplete",
        name="Incomplete / ongoing miscarriage",
        category="obstetrics",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("pregnancy_context", 0.85, 0.60),
            SymptomFrequency("vaginal_bleeding", 0.95, 0.60),
            SymptomFrequency("tissue_passed", 0.60, 0.85),
            SymptomFrequency("lower_abdominal_pain", 0.70, 0.15),
        ],
        discriminators=["heavy bleeding with clots and/or passed tissue, "
                        "ongoing pain — retained products keep the "
                        "bleeding going and invite infection"],
        red_flags=["bleeding soaking >1 pad/hour, faintness, fever"],
        investigations=[],
        management_first_line="Urgent same-day EPU: expectant, medical "
                              "(misoprostol) or surgical (ERPC) options; "
                              "anti-D if rhesus negative; save passed "
                              "tissue for examination.",
        referral_tier="urgent",
        safety_net="Fever or smelly discharge after miscarriage — "
                   "sepsis risk, urgent assessment.",
        source="NICE NG126",
    ),
    ConditionProfile(
        condition_id="puerperal_sepsis",
        name="Puerperal sepsis (post-birth infection)",
        category="obstetrics",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("birth_recently", 0.95, 0.90),
            SymptomFrequency("fever", 0.85, 0.20),
            SymptomFrequency("lochia_offensive", 0.55, 0.85),
            SymptomFrequency("fundal_tenderness", 0.50, 0.85),
            SymptomFrequency("confusion", 0.25, 0.30),
            SymptomFrequency("breast_redness_painful", 0.30, 0.60),
        ],
        discriminators=["fever, tachycardia or offensive lochia any time "
                        "after birth — the historic killer of mothers; "
                        "also check breast (mastitis) and caesarean "
                        "wound",
                        "the smiling mother who collapses: puerperal "
                        "sepsis moves fast"],
        red_flags=["confusion, not passing urine, fast breathing, "
                   "mottled skin — sepsis pathway now"],
        investigations=[
            InvestigationProfile("bloods + cultures + swabs",
                                 "sepsis source hunt before antibiotics",
                                 0.70, 0.70, "WHO maternal sepsis"),
        ],
        management_first_line="Sepsis Six within an hour (oxygen, IV "
                              "fluids, cultures, IV antibiotics, "
                              "lactate, urine output); emergency "
                              "admission; retained products need "
                              "evacuation.",
        referral_tier="emergency",
        safety_net="Any fever, tummy pain or smelly bleeding after birth "
                   "— same-day assessment minimum; confusion or "
                   "breathlessness = 999.",
        source="WHO statements on maternal sepsis; RCOG",
    ),
    # ====== 6.6 ONCOLOGY-SUPPORTIVE + DERMATOLOGICAL EMERGENCIES ======
    ConditionProfile(
        condition_id="neutropenic_sepsis",
        name="Neutropenic sepsis",
        category="oncology_supportive",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("chemo_cancer_treatment", 0.90, 0.95),
            SymptomFrequency("fever", 0.85, 0.20),
            SymptomFrequency("confusion", 0.30, 0.30),
            SymptomFrequency("breathless_acute", 0.30, 0.30),
        ],
        discriminators=["ANY fever or feeling-unwell in a patient on "
                        "chemotherapy (or within 6 weeks) — neutropenic "
                        "sepsis until proven otherwise",
                        "no fever does not exclude it on steroids; a "
                        "sore mouth or shaking chill alone counts"],
        red_flags=["temperature >38 once, or >37.5 twice; confusion, "
                   "hypotension, reduced urine"],
        investigations=[
            InvestigationProfile("FBC (neutrophils) + cultures + lactate",
                                 "neutrophils <0.5 confirms; do not wait "
                                 "for results before antibiotics", 0.90,
                                 0.85, "NICE CG151 neutropenic sepsis"),
        ],
        management_first_line="Emergency admission; empiric IV "
                              "antibiotics within ONE hour of "
                              "presentation (the febrile neutropenia "
                              "clock starts at home, not at the hospital "
                              "door); oncology team call.",
        referral_tier="emergency",
        safety_net="On chemotherapy: any fever, chills or feeling "
                   "suddenly unwell = emergency now, day or night.",
        source="NICE CG151 neutropenic sepsis",
    ),
    ConditionProfile(
        condition_id="malignant_cord_compression",
        name="Malignant spinal cord compression",
        category="oncology_supportive",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("cancer_known_history", 0.90, 0.95),
            SymptomFrequency("new_or_worsening_back_pain", 0.90, 0.70),
            SymptomFrequency("leg_weakness_bilateral", 0.55, 0.85),
            SymptomFrequency("limb_numbness_after_trauma", 0.35, 0.90),
            SymptomFrequency("bladder_bowel_change", 0.40, 0.80),
        ],
        discriminators=["known cancer + new/worsening back pain — cord "
                        "compression until imaged; pain precedes weakness "
                        "by days to weeks, and the window to preserve "
                        "walking is short",
                        "weakness, saddle numbness or bladder change = "
                        "hours matter"],
        red_flags=["any leg weakness, difficulty walking, numbness "
                   "between the legs, new incontinence"],
        investigations=[
            InvestigationProfile("whole-spine MRI (urgent, same day)",
                                 "whole spine — skip films; if MRI "
                                 "unavailable discuss dexamethasone "
                                 "start with oncology", 0.95, 0.95,
                                 "NICE CG75 metastatic cord compression"),
        ],
        management_first_line="Dexamethasone 16 mg (oncology advice) + "
                              "same-day whole-spine MRI + emergency "
                              "oncology referral; keep mobile if "
                              "possible — walking at diagnosis is the "
                              "strongest predictor of walking after.",
        referral_tier="emergency",
        safety_net="With any cancer history: new back pain that is worse "
                   "at night, or any new leg weakness/numbness — "
                   "emergency same-day assessment.",
        source="NICE CG75",
    ),
    ConditionProfile(
        condition_id="svco_superior_vena_cava_obstruction",
        name="Superior vena cava obstruction (SVCO)",
        category="oncology_supportive",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("facial_neck_arm_swelling", 0.80, 0.90),
            SymptomFrequency("neck_veins_distended", 0.55, 0.90),
            SymptomFrequency("worse_lying_flat", 0.45, 0.70),
            SymptomFrequency("breathless_acute", 0.50, 0.30),
            SymptomFrequency("headache_worse_morning", 0.35, 0.60),
            SymptomFrequency("cough", 0.45, 0.20),
        ],
        discriminators=["swollen face/neck/arms with distended neck "
                        "veins, worse lying or bending — usually lung "
                        "cancer or lymphoma until imaged",
                        "the puffiness is vascular: collar tight, "
                        "eyes puffy on waking"],
        red_flags=["stridor, severe breathlessness, fainting on sitting "
                   "up, confusion"],
        investigations=[
            InvestigationProfile("CT chest with contrast",
                                 "diagnosis and histology planning; "
                                 "stent before tissue if severe", 0.95,
                                 0.95, "NICE NG12 / SVCO guidance"),
        ],
        management_first_line="Urgent/emergency assessment; sit upright; "
                              "oxygen if breathless; CT chest; steroids "
                              "only after oncology advice (can blur "
                              "lymphoma histology).",
        referral_tier="emergency",
        safety_net="A face and neck that swell, especially worse lying "
                   "down with breathlessness — emergency assessment.",
        source="NICE lung-cancer SVCO pathway",
    ),
    ConditionProfile(
        condition_id="stevens_johnson_ten",
        name="Stevens–Johnson syndrome / toxic epidermal necrolysis",
        category="dermatology",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("new_drug_started", 0.85, 0.60),
            SymptomFrequency("rash_mucosal_involvement", 0.90, 0.90),
            SymptomFrequency("skin_pain_out_of_proportion", 0.70, 0.85),
            SymptomFrequency("blistering_skin_detaching", 0.65, 0.90),
            SymptomFrequency("fever", 0.55, 0.20),
        ],
        discriminators=["a rash that HURTS (not itches), with lips/"
                        "eyes/genitals involved, 1-3 weeks after a new "
                        "drug (antiepileptics, allopurinol, "
                        "sulfonamides, NSAIDs)",
                        "positive Nikolsky sign: skin peels when "
                        "gently rubbed — skin failure like a burn"],
        red_flags=["mucosal involvement at two+ sites, skin peeling, "
                   "unable to eat/drink, temperature"],
        investigations=[],
        management_first_line="Stop the suspected drug NOW; emergency "
                              "transfer (burns/ITU care for >30% "
                              "detachment); fluids, warmth, analgesia; "
                              "do not debride adherent skin.",
        referral_tier="emergency",
        safety_net="A painful spreading rash with sore lips, eyes or "
                   "genitals after any new medicine — emergency now.",
        source="SJS/TEN consensus guidance",
    ),
    ConditionProfile(
        condition_id="eczema_herpeticum",
        name="Eczema herpeticum",
        category="dermatology",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("eczema_known_context", 0.85, 0.85),
            SymptomFrequency("punched_out_erosions_clustered", 0.85, 0.90),
            SymptomFrequency("fever", 0.55, 0.20),
            SymptomFrequency("skin_pain_out_of_proportion", 0.45, 0.85),
        ],
        discriminators=["eczema that suddenly worsens with clusters of "
                        "punched-out little erosions, monomorphic, "
                        "painful, with fever — herpes simplex in broken "
                        "skin",
                        "affects the face and neck first; can seed the "
                        "eye (urgent ophthalmology)"],
        red_flags=["fever, unwell child, refusal to drink, eye "
                   "involvement, rapidly spreading"],
        investigations=[],
        management_first_line="Emergency same-day assessment; oral "
                              "acyclovir started empirically; swab for "
                              "PCR; ophthalmology if periocular.",
        referral_tier="emergency",
        safety_net="Eczema that turns painful and weepy with little "
                   "holes and fever — same-day emergency review.",
        source="BAD eczema herpeticum guidance",
    ),
    ConditionProfile(
        condition_id="necrotising_fasciitis",
        name="Necrotising fasciitis",
        category="dermatology",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("pain_out_of_proportion_skin", 0.85, 0.90),
            SymptomFrequency("rapid_spreading_swelling_skin", 0.75, 0.85),
            SymptomFrequency("skin_discolouration_dark", 0.40, 0.90),
            SymptomFrequency("fever", 0.55, 0.20),
            SymptomFrequency("confusion", 0.35, 0.30),
            SymptomFrequency("crepitus_skin", 0.15, 0.95),
        ],
        discriminators=["pain VASTLY out of proportion to any visible "
                        "skin change, worsening over hours, with "
                        "systemic toxicity — the skin lags the death "
                        "beneath",
                        "the pain-beats-the-look rule at any wound, "
                        "bruise, insect bite or muscle strain"],
        red_flags=["pain > findings, tachycardia out of proportion, "
                   "purple/black patches, crepitus, collapse"],
        investigations=[
            InvestigationProfile("surgical exploration (not imaging)",
                                 "the diagnosis is made in theatre; LRINEC "
                                 "score only assists", 0.90, 0.90,
                                 "surgical necrotising-infection guidance"),
        ],
        management_first_line="Surgical emergency: theatre for "
                              "debridement NOW + IV antibiotics "
                              "(gram-positive, gram-negative, anaerobic "
                              "cover); do not wait for imaging or "
                              "dermatology review.",
        referral_tier="emergency",
        safety_net="Any skin pain far worse than the skin looks, "
                   "spreading fast with fever — emergency now. Hours "
                   "cost limbs and lives.",
        dangerous_mimic_of=["cellulitis", "wound_infection"],
        source="NICE; surgical literature on necrotising infections",
    ),
    ConditionProfile(
        condition_id="erythroderma_skin_failure",
        name="Erythroderma (skin failure)",
        category="dermatology",
        prevalence_per_consult=0.00005,
        symptoms=[
            SymptomFrequency("generalised_red_skin", 0.90, 0.95),
            SymptomFrequency("skin_shedding_scaling", 0.70, 0.80),
            SymptomFrequency("shivering_temperature_instability", 0.50, 0.80),
            SymptomFrequency("breathless_acute", 0.25, 0.30),
        ],
        discriminators=[">90% of the skin red and shedding: fluid, "
                        "protein and heat loss make this a burns-"
                        "equivalent emergency whatever the cause",
                        "look for the trigger: eczema, psoriasis, drugs, "
                        "lymphoma (Sézary)"],
        red_flags=["shivering/hypothermia, high-output cardiac failure, "
                   "can't maintain temperature"],
        investigations=[],
        management_first_line="Admission (warm room, ~30°C); fluids and "
                              "electrolytes; emollients; barrier nursing; "
                              "stop non-essential drugs; dermatology "
                              "same day.",
        referral_tier="emergency",
        safety_net="Skin red all over with shivering or breathlessness — "
                   "emergency admission; this is skin failure.",
        source="BAD erythroderma guidance",
    ),
    # ================= 6.7 PAEDIATRIC PROTECTION & SYNDROMES ==========
    ConditionProfile(
        condition_id="non_accidental_injury",
        name="Non-accidental injury in a child (safeguarding)",
        category="safeguarding",
        prevalence_per_consult=0.001,
        symptoms=[
            # NB no bare 'bruise' token: a bruise alone is not NAI. The
            # concerning sites (torso/ears/neck), patterned marks, the
            # non-mobile context (urgent safety rule) and the history
            # that doesn't add up are what score here.
            SymptomFrequency("bruise_torso_site", 0.40, 0.80),
            SymptomFrequency("patterned_bruise_marks", 0.25, 0.95),
            SymptomFrequency("inconsistent_history", 0.50, 0.90),
            SymptomFrequency("frozen_watchfulness", 0.20, 0.80),
            SymptomFrequency("delayed_presentation_injury", 0.30, 0.60),
        ],
        discriminators=["a bruise on a child who is not yet crawling or "
                        "walking is never 'just a bruise' — those who "
                        "don't cruise rarely bruise",
                        "bruises of different ages, patterned marks (bite, "
                        "belt, hand), or sites torso/ears/neck",
                        "history that doesn't fit the injury, changes "
                        "between tellers, or presentation days later"],
        red_flags=["infant <4 months with ANY bruise",
                   "patterned injuries, fractures under 1 year, "
                   "immersion-pattern burns (glove/stocking, sparing "
                   "flexures)",
                   "drowsiness or vomiting after a 'minor' injury (shaken "
                   "baby until proven otherwise)"],
        investigations=[
            InvestigationProfile("Same-day paediatric + safeguarding "
                                 "assessment (full examination, "
                                 "ophthalmology, skeletal survey <2y)",
                                 "identifies occult fractures, retinal "
                                 "haemorrhages and other injuries; social "
                                 "care referral must not be delayed", 0.85,
                                 0.90,
                                 "NICE CG89 child maltreatment; RCPCH"),
        ],
        management_first_line="Do not send home pending 'explanation'; "
                              "same-day referral to paediatrics with "
                              "safeguarding lead informed; document "
                              "verbatim; do not interrogate the family; "
                              "consider immediate separation if the child "
                              "is drowsy or has patterned injuries.",
        referral_tier="urgent",
        safety_net="Any bruise in a non-mobile child, or a patterned or "
                   "unexplained injury, needs same-day safeguarding "
                   "assessment — this is about protecting the child, not "
                   "accusing the parent.",
        dangerous_mimic_of=["accidental_bruising"],
        source="NICE CG89; RCPCH child protection companion",
    ),
    ConditionProfile(
        condition_id="kawasaki_disease",
        name="Kawasaki disease",
        category="paediatric",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("fever_five_days_plus", 0.95, 0.95),
            SymptomFrequency("red_eyes_injection", 0.90, 0.70),
            SymptomFrequency("cracked_red_lips", 0.85, 0.70),
            SymptomFrequency("inconsolable_irritability", 0.70, 0.40),
            SymptomFrequency("red_palms_soles", 0.50, 0.70),
            SymptomFrequency("strawberry_tongue", 0.40, 0.85),
            SymptomFrequency("peeling_fingers", 0.30, 0.85),
            SymptomFrequency("neck_gland_swollen_one_side", 0.35, 0.60),
        ],
        discriminators=["fever >=5 days plus at least 2 mucocutaneous "
                        "features (red eyes without discharge, cracked "
                        "lips, strawberry tongue, red palms/soles, "
                        "peeling, unilateral neck gland)",
                        "irritability out of proportion (meningeal "
                        "irritation without meningitis)",
                        "not soothed by paracetamol the way simple "
                        "viruses are"],
        red_flags=["coronary artery aneurysms form in the second week — "
                   "IVIG works best given within 10 days of fever onset",
                   "any fever >=5 days without a source is 'incomplete "
                   "Kawasaki' until proven otherwise"],
        investigations=[
            InvestigationProfile("FBC/CRP/ESR, LFT (low albumin), "
                                 "echocardiography",
                                 "supporting labs raise or lower the "
                                 "diagnosis score; echo dates and sizes "
                                 "any coronary aneurysm", 0.80, 0.75,
                                 "AHA/BCSH Kawasaki guidance"),
        ],
        management_first_line="Same-day paediatric admission: IVIG 2 g/kg "
                              "plus aspirin; cardiology follow-up with "
                              "echo. Do not wait for the full textbook "
                              "picture.",
        referral_tier="emergency",
        safety_net="Fever five days or more with red eyes, cracked lips "
                   "or red palms needs same-day assessment — the heart "
                   "coronaries are what we are protecting.",
        dangerous_mimic_of=["measles", "scarlet_fever", "viral_urti"],
        source="AHA Kawasaki statement; RCPCH",
    ),
    ConditionProfile(
        condition_id="iga_vasculitis_hsp",
        name="IgA vasculitis (Henoch-Schönlein purpura)",
        category="paediatric",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("palpable_purpura", 0.90, 0.95),
            SymptomFrequency("purpura_buttocks_legs", 0.80, 0.85),
            SymptomFrequency("joint_pain_ankles_hsp", 0.60, 0.60),
            SymptomFrequency("abdominal_pain", 0.55, 0.20),
            SymptomFrequency("blood_in_urine_child", 0.25, 0.75),
            SymptomFrequency("sore_throat_last_week", 0.30, 0.30),
            SymptomFrequency("scrotal_swelling_pain", 0.10, 0.75),
        ],
        discriminators=["purpura you can FEEL (raised), concentrated on "
                        "buttocks and legs, platelets normal",
                        "migrating joint pain (ankles/knees) and colicky "
                        "tummy pain clinch it",
                        "test BP and dip the urine at every review — "
                        "renal disease declares in the first month"],
        red_flags=["severe abdominal pain (intussusception complication), "
                   "testicular pain, or purpura spreading to trunk",
                   "hypertension or haematuria/proteinuria — nephritis "
                   "needs paediatric nephrology"],
        investigations=[
            InvestigationProfile("BP measurement + urinalysis at "
                                 "diagnosis and weekly x4-6, FBC "
                                 "(platelets normal), U&E, albumin",
                                 "the kidneys are the organ at risk; "
                                 "platelet count separates from ITP", 0.70,
                                 0.85,
                                 "RCPCH/CKS Henoch-Schönlein guidance"),
        ],
        management_first_line="Most children need rest, simple analgesia "
                              "and BP+urine monitoring; admit for abdominal "
                              "or testicular pain, renal involvement or "
                              "being unable to walk comfortably.",
        referral_tier="urgent",
        safety_net="Return immediately with severe tummy pain, swollen or "
                   "painful testicles, headache or visual change, or if "
                   "the rash spreads to the trunk; BP and urine checks "
                   "weekly for a month whatever the child's outlook today.",
        dangerous_mimic_of=["meningococcal_child", "idiopathic_thrombocytopenia"],
        source="CKS Henoch-Schönlein purpura; RCPCH",
    ),
    ConditionProfile(
        condition_id="febrile_convulsion",
        name="Febrile convulsion (simple)",
        category="paediatric",
        prevalence_per_consult=0.006,
        symptoms=[
            SymptomFrequency("seizure_with_fever_child", 0.95, 0.90),
            SymptomFrequency("seizure_recovered_quickly", 0.70, 0.70),
            SymptomFrequency("fever", 0.90, 0.10),
        ],
        discriminators=["generalised, <5 minutes, once per illness, fully "
                        "recovered within an hour, age 6 months-5 years",
                        "not afebrile seizure, not focal, not prolonged — "
                        "those are not 'simple' and need more",
                        "the fit frightens everyone; the fever source "
                        "(usually viral) is what needs finding"],
        red_flags=[">5 minutes, repeated in the day, focal, or <6 months "
                   "old — treat as something worse",
                   "not fully back to normal within an hour, or a stiff "
                   "neck / non-fading rash — reassess now",
                   "first fit needs same-day medical review even when "
                   "the child looks perfect afterwards"],
        investigations=[
            InvestigationProfile("Same-day clinical review; urine "
                                 "testing; no routine bloods/imaging for "
                                 "a simple febrile convulsion",
                                 "confirms recovery and hunts the fever "
                                 "source; over-investigation is the "
                                 "usual error, not under-", 0.60, 0.90,
                                 "NICE CG160 feverish illness in children"),
        ],
        management_first_line="Nothing in the mouth; recovery position "
                              "during the fit; after it, paracetamol for "
                              "comfort (not to prevent fits), same-day "
                              "review, parental explanation — a third of "
                              "children have another with a future fever.",
        referral_tier="urgent",
        safety_net="Call 999 if a fit lasts 5 minutes or more, repeats, "
                   "the child is not themselves within the hour, or a "
                   "rash that doesn't fade appears.",
        source="NICE CG160; AAP febrile seizures guideline",
    ),
    ConditionProfile(
        condition_id="neonatal_jaundice",
        name="Neonatal jaundice requiring assessment",
        category="paediatric",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("young_baby_age_marker", 0.95, 0.90),
            SymptomFrequency("jaundice", 0.95, 0.20),
            SymptomFrequency("jaundice_first_48_hours", 0.20, 0.90),
            SymptomFrequency("pale_stool_dark_urine", 0.15, 0.95),
            SymptomFrequency("prolonged_jaundice", 0.35, 0.80),
            SymptomFrequency("poor_feeding", 0.40, 0.20),
            SymptomFrequency("sleepy_newborn", 0.35, 0.30),
        ],
        discriminators=["jaundice in the first 24-48 hours is ALWAYS "
                        "pathological (haemolysis until proven otherwise)",
                        "pale stools + dark urine = biliary atresia; the "
                        "Kasai operation works best before ~60 days",
                        "jaundice persisting beyond 2 weeks (term) needs "
                        "a conjugated fraction measured, not watchful "
                        "waiting"],
        red_flags=["yellow in day 1-2, pale stool or dark urine, sleepy "
                   "and not feeding, or still yellow after 2 weeks",
                   "rising jaundice with arching/opisthotonus = "
                   "kernicterus risk — that injury is permanent"],
        investigations=[
            InvestigationProfile("Serum bilirubin (fractionated if "
                                 "prolonged/early), FBC + blood group + "
                                 "DAT (Coomb's), urine culture",
                                 "separates the dangerous causes "
                                 "(haemolysis, biliary atresia, sepsis) "
                                 "from physiological jaundice", 0.85,
                                 0.85,
                                 "NICE CG98 neonatal jaundice"),
        ],
        management_first_line="Same-day paediatric assessment for any "
                              "day-1/2 jaundice, pale stools, dark urine "
                              "or a sleepy feeding-rejecting baby; "
                              "phototherapy or exchange transfusion "
                              "thresholds per NICE threshold charts.",
        referral_tier="urgent",
        safety_net="A yellow baby with pale stools or dark wee, a yellow "
                   "baby in the first two days, or one too sleepy to "
                   "feed needs same-day assessment — pale poo means the "
                   "bile ducts may be blocked and that window closes by "
                   "two months.",
        source="NICE CG98 jaundice in newborn babies",
    ),
    ConditionProfile(
        condition_id="neonatal_sepsis",
        name="Neonatal sepsis / serious bacterial infection",
        category="paediatric",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("young_baby_age_marker", 0.95, 0.90),
            SymptomFrequency("fever_newborn", 0.35, 0.95),
            SymptomFrequency("poor_feeding", 0.75, 0.30),
            SymptomFrequency("grunting_breathing", 0.35, 0.90),
            SymptomFrequency("sleepy_newborn", 0.55, 0.40),
            SymptomFrequency("temperature_unstable_newborn", 0.35, 0.80),
            SymptomFrequency("umbilical_discharge", 0.15, 0.85),
        ],
        discriminators=["any fever >=38 in a baby under 3 months is a "
                        "full septic workup — no exceptions, however "
                        "well the baby looks",
                        "the newborn sepsis signs are subtle: grunting, "
                        "not feeding, temperature LOW as often as high",
                        "'the baby just isn't right' from a parent who "
                        "knows their baby outranks any normal obs"],
        red_flags=["grunting, floppy, cold peripheries, capillary refill "
                   ">3s, or a temperature <36 — emergency now",
                   "umbilical or skin infection in the first week "
                   "(omphalitis) is sepsis until proven otherwise"],
        investigations=[
            InvestigationProfile("Full septic screen: FBC, CRP, blood "
                                 "culture, urine (catheter/supra-pubic), "
                                 "LP if clinically safe, CXR if "
                                 "respiratory signs",
                                 "a fever <3 months old gets all of it — "
                                 "the cost of a missed neonatal sepsis is "
                                 "death or disability", 0.90, 0.95,
                                 "NICE CG149 neonatal infection"),
        ],
        management_first_line="Emergency transfer; IV antibiotics within "
                              "the hour (ampicillin+gentamicin per local "
                              "policy); do not delay for feeding attempts "
                              "or obs re-checks.",
        referral_tier="emergency",
        safety_net="A baby under three months with any fever, grunting, "
                   "not feeding, or abnormally low temperature goes to "
                   "hospital now — newborns hide sepsis until they "
                   "collapse.",
        dangerous_mimic_of=["bronchiolitis", "feeding_problem_benign"],
        source="NICE CG149 neonatal infection; NICE CG160",
    ),
    ConditionProfile(
        condition_id="slapped_cheek_parvovirus",
        name="Slapped cheek (parvovirus B19, fifth disease)",
        category="paediatric",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("slapped_cheek_rash", 0.85, 0.95),
            SymptomFrequency("lacy_rash_arms", 0.55, 0.80),
            SymptomFrequency("fever", 0.40, 0.10),
            SymptomFrequency("mild_unwell", 0.50, 0.05),
            SymptomFrequency("joint_pain_adults", 0.30, 0.40),
        ],
        discriminators=["bright red cheeks with circumoral sparing, then "
                        "a lacy reticular rash on arms/trunk that fades "
                        "and reappears with heat",
                        "the child is usually well — the rash often "
                        "arrives after the infectious period",
                        "adult contacts get symmetric polyarthritis "
                        "instead of the rash"],
        red_flags=["exposure of a pregnant contact (esp <20 weeks): "
                   "hydrops fetalis risk — the pregnant woman needs to "
                   "tell her midwife/GP and have parvovirus IgM/IgG",
                   "a child with sickle cell or hereditary spherocytosis: "
                   "aplastic crisis — urgent FBC if pale or lethargic",
                   "immunocompromised contact: chronic anaemia risk"],
        investigations=[
            InvestigationProfile("None for the child (clinical "
                                 "diagnosis); parvovirus serology for "
                                 "pregnant or anaemia-prone contacts",
                                 "protects the people around the child — "
                                 "the child themselves needs no tests",
                                 0.90, 0.95,
                                 "UKHSA parvovirus guidance; CKS"),
        ],
        management_first_line="Symptom-free children need no exclusion "
                              "from school (infectious before the rash); "
                              "emollients/fluids; inform pregnant and "
                              "sickle-cell contacts to seek advice.",
        referral_tier="self_care",
        safety_net="Tell any pregnant contact to speak to their midwife "
                   "or GP today (small risk to the baby, easily checked "
                   "with a blood test), and if the child has sickle "
                   "cell disease and becomes pale or lethargic, seek "
                   "urgent review.",
        source="UKHSA guidance on parvovirus B19; CKS slapped cheek",
    ),
    # ================= 6.8 POST-EXPOSURE PROPHYLAXIS ===================
    # decision support lives in gpdisc_core/post_exposure/; these two
    # entries are what the consultation pipeline ranks and names.
    ConditionProfile(
        condition_id="rabies_exposure_risk",
        name="Rabies exposure risk (mammalian bite/scratch)",
        category="infection",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("bite_wound_exposure", 0.85, 0.60),
            SymptomFrequency("rabies_region_exposure", 0.60, 0.70),
            SymptomFrequency("saliva_broken_skin", 0.15, 0.80),
            SymptomFrequency("bat_contact", 0.05, 0.95),
            SymptomFrequency("wound_not_treated", 0.40, 0.40),
        ],
        discriminators=["transdermal bite in an endemic area = category "
                        "III: vaccine PLUS immunoglobulin, same day",
                        "any bat contact anywhere (including the UK) is "
                        "category III — lyssaviruses cross borders",
                        "a healthy observable pet in a rabies-free "
                        "country may defer to 10-day observation; a "
                        "stray abroad never does"],
        red_flags=["tingling, numbness or pain at the wound site — "
                   "prodrome, the window has closed (~100% fatal)",
                   "delayed presentation weeks later with no PEP: "
                   "start now — there is no 'too late' until symptoms"],
        investigations=[
            InvestigationProfile("None that wait: same-day PEP decision "
                                 "(vaccine ± RIG per WHO category)",
                                 "the decision is clinical and "
                                 "geographical, made from the exposure "
                                 "story, not from tests", 0.95, 0.95,
                                 "WHO rabies position paper; UKHSA "
                                 "rabies PEP guidelines"),
        ],
        management_first_line="Wash 15 minutes soap + water, "
                              "povidone-iodine; avoid primary suturing; "
                              "same-day vaccine course (d0,3,7,14) and "
                              "RIG into the wound for category III; "
                              "co-amoxiclav + tetanus check.",
        referral_tier="urgent",
        safety_net="Any bite or scratch from a mammal abroad, or any bat "
                   "contact anywhere: same-day PEP advice — however long "
                   "ago it happened, until symptoms begin it is not too "
                   "late. Wound tingling or difficulty swallowing after "
                   "a bite is an emergency.",
        dangerous_mimic_of=["animal_bite_infection"],
        source="WHO rabies; UKHSA PEP guidelines",
    ),
    ConditionProfile(
        condition_id="occupational_bbv_exposure",
        name="Bloodborne-virus exposure (needlestick/splash/sexual)",
        category="infection",
        prevalence_per_consult=0.0015,
        symptoms=[
            SymptomFrequency("needlestick_event", 0.70, 0.90),
            SymptomFrequency("source_hepatitis_b", 0.20, 0.90),
            SymptomFrequency("source_hiv_positive", 0.15, 0.90),
            SymptomFrequency("source_hepatitis_c", 0.10, 0.90),
            SymptomFrequency("mucosal_blood_splash", 0.15, 0.85),
            SymptomFrequency("unprotected_exposure_event", 0.25, 0.70),
        ],
        discriminators=["the HIV PEP window is 72 hours; HBIG works best "
                        "inside 48 — the clock starts at the exposure, "
                        "not at the appointment",
                        "source known and treated (HIV undetectable) = "
                        "effectively no risk: say so, test baseline "
                        "anyway",
                        "hepatitis C has no PEP: RNA at 6 weeks, and "
                        "treatment cures >95%"],
        red_flags=["exposure inside the window with an HIV-positive "
                   "source — first PEP dose NOW, questions afterwards",
                   "HBsAg-positive source with an unprotected recipient — "
                   "HBIG + vaccine ideally <48h"],
        investigations=[
            InvestigationProfile("Baseline recipient labs: HIV 4th-gen, "
                                 "HBsAg + anti-HBs, HCV Ab, LFTs; source "
                                 "testing where consented",
                                 "anchors the decision and the follow-up "
                                 "schedule; anti-HBs ≥10 = already "
                                 "protected against HBV", 0.90, 0.85,
                                 "UKHSA HIV PEP guidance; DOH BBV "
                                 "occupational guidance"),
        ],
        management_first_line="First dose before the full story: HIV PEP "
                              "(28-day starter) if <72h and source "
                              "positive/unknown-risk; HBIG + accelerated "
                              "HBV vaccine if source HBsAg+ and recipient "
                              "unprotected; wash/irrigate the site; "
                              "report per occupational-health protocol.",
        referral_tier="urgent",
        safety_net="Needlestick, splash or unprotected exposure with a "
                   "known-positive source: same-day assessment — HIV PEP "
                   "works inside 72 hours and HBIG inside ~48. Never "
                   "'wait and see' inside those windows.",
        source="UKHSA HIV PEP; UK DOH bloodborne-occupational-exposure",
    ),
]

# Every token used by CONDITIONS_PART4 must appear here (corpus integrity
# test enforces it). Phrases are lowercase substrings matched against the
# presentation; a negation prefix ("no", "not", "denies"...) within 30
# characters before the phrase marks the feature ABSENT. Phrases that could
# collide with chronic/benign presentations (e.g. bare "bleeding", bare
# "widespread") are deliberately anchored to their trauma context.
SYMPTOM_SYNONYMS_PART4: Dict[str, List[str]] = {
    # --- head injury ---
    "head_hit_event": [
        "hit my head", "hit his head", "hit her head", "hit their head",
        "banged my head", "banged his head", "banged her head",
        "knocked my head", "struck my head", "struck his head",
        "fell on my head", "fell on his head", "fell on her head",
        "head hit the", "head injury", "head wound",
        "fell off a ladder", "fell from a ladder", "fell down the stairs",
        "fell down stairs", "fell off his bike", "fell off her bike",
        "fell off my bike", "fell off a horse", "fell off the roof",
    ],
    "vomiting_after_injury": [
        "vomited since", "vomiting since", "been sick since",
        "threw up since", "throwing up since", "vomited after the fall",
        "vomited after the accident", "vomiting after the",
        "vomited twice", "vomited three times", "vomited several",
        "repeated vomiting", "repeatedly vomited", "keeps vomiting",
        "vomiting repeatedly", "been sick twice",
    ],
    "confusion_after_injury": [
        "confused since", "confusion since", "muddled since",
        "not himself since", "not herself since", "not with it since",
        "agitated since the fall", "agitated since the accident",
    ],
    "clear_fluid_from_ear_nose": [
        "clear fluid from the ear", "clear fluid from his ear",
        "clear fluid from her ear", "clear fluid from the nose",
        "fluid leaking from the ear", "fluid from the ear",
        "fluid leaking from the nose", "liquid from the ear",
    ],
    "focal_weakness_one_side": [
        "weakness on one side", "weak down one side",
        "weakness down one side", "one side is weak",
        "weakness in one arm", "weakness in one leg",
        "arm went weak", "leg went weak",
    ],
    "headache_after_injury": [
        "headache since the fall", "headache since he fell",
        "headache since she fell", "headache since the accident",
        "headache after the fall", "headache since the bang",
        "headache since being hit", "head pain since the fall",
    ],
    "nausea_mild": [
        "mildly nauseous", "a bit nauseous", "slight nausea",
        "a little nauseous", "mild nausea", "feels a bit sick",
    ],
    # --- penetrating / blunt trauma ---
    "stab_or_gunshot": [
        "stab", "knife wound", "gunshot", "been shot",
        "shot in the chest", "shot in the stomach", "impaled",
        "penetrating wound",
    ],
    "breathless_acute": [
        "breathless", "short of breath", "can't breathe",
        "cannot breathe", "struggling to breathe", "gasping",
        "winded",
    ],
    "wound_bleeding": [
        "bleeding", "blood pouring", "blood gushing",
    ],
    "pale_cold_skin": [
        "pale and cold", "pale, cold", "cold and clammy",
        "pale and clammy", "grey and clammy", "white as a sheet",
        "pale and sweaty", "grey and cold", "pale, clammy",
    ],
    "chest_impact_event": [
        "road accident", "road traffic accident", "car crash",
        "car accident", "motorbike crash", "motorbike accident",
        "hit by a car", "hit by a van", "hit by a lorry",
        "fell from a height", "fall from height", "steering wheel",
        "horse-riding accident", "riding accident", "kicked by a horse",
        "chest hit the", "hit his chest on", "hit her chest on",
    ],
    "rib_pain_tender": [
        "rib pain", "ribs hurt", "ribs are tender", "broken rib",
        "cracked rib", "pain in my ribs", "pain in the ribs",
        "pain when i breathe", "pain when breathing", "pain on breathing",
        "hurts to breathe", "hurts to take a deep breath",
    ],
    "cough_after_injury": [
        "coughing since the accident", "coughing since the fall",
        "coughing since the crash", "coughing up blood since",
    ],
    "rapid_weak_pulse": [
        "fast pulse", "rapid pulse", "racing heart",
        "heart is racing", "heart racing", "pulse is racing",
        "weak pulse", "thready pulse", "heart pounding",
    ],
    "visible_bleeding_severe": [
        "bleeding heavily", "won't stop bleeding", "bleeding won't stop",
        "blood pouring", "blood gushing", "lost a lot of blood",
        "bleeding through the dressing", "pooling blood",
    ],
    "dizzy_on_standing": [
        "dizzy when i stand", "dizzy on standing",
        "dizzy when standing", "dizzy when i get up",
        "faint on standing", "light-headed on standing",
        "lightheaded on standing", "feels faint when standing",
    ],
    # --- limbs / fractures ---
    "limb_injury_event": [
        "fell on my arm", "fell on his arm", "fell on her arm",
        "fell on my wrist", "fell on his wrist", "fell on her wrist",
        "landed on my arm", "landed on his arm", "landed on her arm",
        "twisted my ankle", "twisted his ankle", "twisted her ankle",
        "rolled my ankle", "rolled his ankle", "rolled her ankle",
        "injured the arm", "injured the leg", "injured the ankle",
        "injured the wrist", "injured his ankle", "injured her ankle",
        "arm injury", "leg injury", "ankle injury", "wrist injury",
        "hurt his arm", "hurt her arm", "hurt my arm",
        "hurt his leg", "hurt her leg", "hurt my leg",
    ],
    "deformity_limb": [
        "deformed", "bent the wrong way", "sticking out at an angle",
        "at an odd angle", "at a funny angle",
        "bent where it shouldn't", "looks the wrong shape",
    ],
    "cannot_weight_bear": [
        "can't put weight on it", "cannot put weight on it",
        "can't walk on it", "cannot walk on it",
        "can't stand on it", "cannot stand on it",
        "can't weight bear", "unable to put weight",
        "can't put any weight", "not putting weight",
    ],
    "swelling_after_injury": [
        "swollen since the fall", "swollen since the accident",
        "swelling since", "swollen since he fell",
        "swollen since she fell", "came up like a balloon",
        "swelled up since",
    ],
    "bone_visible_wound": [
        "bone sticking out", "bone poking through",
        "bone through the skin", "can see the bone", "can see bone",
        "bone visible", "compound fracture", "the bone is showing",
    ],
    "trapped_crushed_duration": [
        "trapped under", "crushed under", "pinned under",
        "trapped beneath", "crushed legs", "crushed arm",
        "legs crushed", "arm crushed", "was crushed",
        "trapped for", "pinned for", "crushed in a road accident",
        "crushed in a crash",
    ],
    "limb_pain_swelling": [
        "leg is swollen and painful", "arm is swollen and painful",
        "painful swollen leg", "painful swollen arm",
        "leg pain and swelling", "arm pain and swelling",
        "swollen and painful",
    ],
    # --- burns ---
    "burn_scald_large": [
        "scalded his arm", "scalded her arm", "scalded my arm",
        "scalded the arm", "scalded his leg", "scalded her leg",
        "scalded my leg", "scalded the leg", "scalded my baby",
        "scalded the baby", "scalded his chest", "scalded her chest",
        "scalded my chest", "large burn", "large scald",
        "widespread burn", "burns all over", "severe burn",
        "severe scald", "burns to both", "burnt both", "burned both",
        "boiling water spilt", "boiling water spilled",
        "hot water scald", "pulled a kettle", "pulled the kettle",
        "hot water over", "kettle fell",
    ],
    "burn_face_airway": [
        "burnt his face", "burnt her face", "burnt my face",
        "burn to the face", "burns to the face", "burned his face",
        "burned her face", "burned my face", "singed his eyebrows",
        "singed her eyebrows", "smoke inhalation", "breathed in smoke",
        "was in a house fire", "in a house fire",
    ],
    "blistered_skin": [
        "blisters", "blistered", "covered in blisters",
    ],
    "singed_nasal_hairs": [
        "singed nose", "singed nostril", "singed nasal",
        "singed hairs", "soot in the nose", "soot in his nose",
        "soot in her nose", "black specks in the nose",
    ],
    "burn_scald_small": [
        "small burn", "small scald", "minor burn", "minor scald",
        "burnt my finger", "burned my finger", "burnt his finger",
        "burned her finger", "tiny burn", "superficial burn",
        "mild burn", "little burn",
    ],
    "painful_red_skin": [
        "red and painful skin", "skin is red and painful",
        "painful red patch", "red painful skin",
    ],
    # --- wounds ---
    "dirty_or_deep_wound": [
        "dirty wound", "deep wound", "deep cut", "gash",
        "puncture wound", "deep puncture", "wound is dirty",
        "gravel in the wound", "glass in the wound",
        "animal bite", "bitten by a dog", "dog bite", "cat bite",
    ],
    "tetanus_status_unknown": [
        "tetanus injection status unknown", "tetanus status unknown",
        "not sure about tetanus", "can't remember tetanus",
        "don't know about tetanus", "unsure about tetanus",
        "never had a tetanus", "not had a tetanus",
        "no idea when my last tetanus", "no tetanus injection",
        "can't remember the last tetanus", "tetanus jab status unknown",
        "not sure when the last tetanus",
    ],
    "soil_or_faecal_contamination": [
        "soil in the wound", "dirt in the wound", "mud in the wound",
        "soil contamination", "farm injury", "stood on a nail",
        "stood on a rusty nail", "rusty nail", "manure",
        "faeces in the wound", "rose thorn", "gardening wound",
    ],
    "spreading_redness_wound": [
        "spreading redness", "redness spreading",
        "redness around the wound", "red streaks", "red streaking",
        "redness getting bigger", "getting redder around",
        "spreading up the arm from the wound",
    ],
    "pus_wound": [
        "pus", "yellow discharge from the wound", "weeping pus",
        "full of pus", "pus coming from",
    ],
    "wound_pain_increasing": [
        "more painful each day", "pain getting worse each day",
        "wound getting more painful", "hurts more every day",
        "increasing pain", "pain worsening",
    ],
    # --- spinal / abdominal ---
    "spinal_pain_after_trauma": [
        "neck pain since the accident", "back pain since the accident",
        "neck pain since the fall", "back pain since the fall",
        "neck pain after the fall", "back pain after the fall",
        "neck pain since the crash", "back pain since the crash",
        "spine pain since", "injured his neck", "injured her neck",
        "hurt his neck in", "hurt her neck in", "neck pain after a fall",
    ],
    "limb_numbness_after_trauma": [
        "can't feel his legs", "can't feel her legs", "can't feel my legs",
        "can't feel his arms", "can't feel her arms", "can't feel my arms",
        "numbness in the legs since", "numbness in the arms since",
        "pins and needles in the legs since", "tingling down the arms since",
        "numb since the accident", "legs feel numb since",
        "arms feel numb since", "numbness since the fall",
        "pins and needles since the accident",
    ],
    "high_energy_event": [
        "fell from a height", "fell from height", "fell off a roof",
        "fell off a ladder", "fell from a ladder", "down the stairs",
        "car crash", "road accident", "motorbike accident",
        "thrown from", "ejected", "dived into shallow water",
        "dove into shallow", "hit by a car", "high speed collision",
        "fall from a horse", "horse fall",
    ],
    "abdominal_impact_event": [
        "hit his stomach", "hit her stomach", "hit my stomach",
        "blow to the abdomen", "blow to the stomach",
        "kicked in the stomach", "punched in the stomach",
        "punched in the abdomen", "seat belt", "seatbelt",
        "handlebars", "fell onto the handlebars",
        "crushed in a crash",
    ],
    "abdominal_pain_after_impact": [
        "stomach pain since the accident", "tummy pain since the accident",
        "abdominal pain since the accident", "stomach pain since the crash",
        "tummy pain since the crash", "stomach pain since the fall",
        "abdominal pain after the accident", "stomach hurts since",
        "belly pain since the crash", "stomach pain since being hit",
    ],
    "guarding_rigidity": [
        "guarding", "rigid abdomen", "rigid stomach",
        "stomach is rigid", "abdomen is rigid",
        "won't let anyone touch his stomach",
        "too painful to touch the stomach", "peritonism",
    ],
    # --- 6.4 toxicology & withdrawal ---
    "overdose_event": [
        "overdose", "took too many", "swallowed some tablets",
        "took the whole packet", "took a handful",
        "taken too much", "suicidal ingestion",
    ],
    "paracetamol_ingested": [
        "paracetamol", "acetaminophen", "tylenol",
        "calpol", "co-codamol", "solpadeine", "panadol",
    ],
    "staggered_over_hours": [
        "staggered", "over the last few days", "several times over",
        "a few now and then all day", "topped up through the day",
    ],
    "opioid_drug_context": [
        "heroin", "morphine", "oxycodone", "fentanyl", "methadone",
        "tramadol", "codeine", "dihydrocodeine", "opiate", "opioid",
        "strong painkillers", "poppers of", " smack",
    ],
    "wont_wake": [
        "won't wake", "won't wake up", "cannot wake", "can't wake",
        "unresponsive", "unconscious", "not waking", "won't rouse",
    ],
    "pinpoint_pupils": [
        "pinpoint pupils", "pin-point pupils", "tiny pupils",
        "constricted pupils", "pupils are tiny", "pupils like pinpricks",
        "pinned pupils",
    ],
    "slow_breathing": [
        "slow breathing", "breathing slowly", "breathing is slow",
        "hardly breathing", "barely breathing", "stopped breathing",
        "breaths are shallow", "gasping breaths",
    ],
    "blue_lips": [
        "blue lips", "lips are blue", "blue face", "turned blue",
        "cyanosed", "bluish lips",
    ],
    "tca_drug_context": [
        "amitriptyline", "nortriptyline", "imipramine", "clomipramine",
        "dosulepin", "dothiepin", "tricyclic", "lofepramine",
    ],
    "aspirin_ingested": [
        "aspirin", "salicylate", "disprin", "alka-seltzer",
        "oil of wintergreen", "ben-gay", "methyl salicylate",
    ],
    "tinnitus": [
        "tinnitus", "ringing in my ears", "ringing in the ears",
        "ears are ringing", "ringing ears", "buzzing in the ears",
    ],
    "hyperventilation": [
        "breathing fast and deep", "deep rapid breathing",
        "breathing very fast", "hyperventilat", "panting",
        "breaths are deep", "sighing breathing",
    ],
    "benzo_drug_context": [
        "diazepam", "temazepam", "zopiclone", "zolpidem", "alprazolam",
        "lorazepam", "benzodiazepine", "sleeping tablets", "sleeping pills",
        "valium", "ativan",
    ],
    "slurred_speech": [
        "slurred speech", "words are slurred", "slurring",
        "speech is slurred", "tongue-tied speech",
    ],
    "fume_source_exposure": [
        "carbon monoxide", "gas boiler", "gas fire", "gas heater",
        "gas stove", "faulty boiler", "charcoal", "coal fire",
        "generator indoors", "generator in", "car exhaust", "exhaust fumes",
        "engine running in", "blocked flue", "chimney blocked",
        "paraffin heater", "kerosene heater", "wood-burning stove",
    ],
    "multiple_household_affected": [
        "everyone in the house", "all of us at home", "the whole family",
        "both children and i", "everyone at home", "my partner and i both",
        "the whole household", "several of us in the flat",
        "everyone in the flat",
    ],
    "alcohol_heavy_use": [
        "heavy drinker", "drinks heavily", "bottle of vodka",
        "a bottle of wine a day", "drinks a lot", "alcohol dependent",
        "alcoholic", "drinks every day", "drinks daily",
        "been drinking for years", "drink problem", "litres of cider",
    ],
    "stopped_drinking_recently": [
        "stopped drinking", "hasn't had a drink", "haven't had a drink",
        "no alcohol for", "ran out of alcohol", "gave up drinking",
        "stopped three days ago", "cold turkey", "admitted yesterday",
        "in hospital since", "was admitted", "in police custody",
    ],
    "hallucinations": [
        "hallucinat", "seeing things", "sees things", "seeing insects",
        "hearing voices", "thinks there are rats", "seeing rats",
        "shadows moving", "people in the room that aren't",
    ],
    "withdrawal_sweats": [
        "drenched in sweat", "soaking sweats", "sweating profusely",
        "sweating and shaking", "cold sweats", "pouring with sweat",
        "night sweats and shaking",
    ],
    "opioid_dependent_context": [
        "on methadone", "heroin user", "uses heroin", "on subutex",
        "buprenorphine", "on a script", "pharmacy closed",
        "missed my methadone", "haven't used since",
        "drug user", "injecting user", "on oramorph long-term",
    ],
    "supply_interrupted": [
        "ran out of", "couldn't get my", "pharmacy closed",
        "missed my", "no supply", "script ran out", "prescription didn't",
        "haven't taken any for", "without it for",
    ],
    "yawning_runny_nose": [
        "can't stop yawning", "yawning constantly", "runny nose and eyes",
        "streaming eyes", "nose running constantly", "tears streaming",
        "sneezing and yawning",
    ],
    "muscle_aches": [
        "muscle aches", "aching all over", "bones ache", "muscles hurt",
        "body aches", "aches and pains everywhere", "cramps in the legs",
    ],
    "goosebumps_cold_flushes": [
        "goosebumps", "goose flesh", "goose pimples", "cold flushes",
        "skin crawling", "hot and cold flushes",
    ],
    "serotonergic_drug_context": [
        "sertraline", "citalopram", "fluoxetine", "escitalopram",
        "paroxetine", "venlafaxine", "duloxetine", "trazodone",
        "ssri", "snri", "just started an antidepressant",
        "upped the dose", "linezolid", "tramadol and", "triptyline",
        "st john's wort",
    ],
    "muscle_clonus_twitching": [
        "clonus", "twitching", "can't stop my legs jerking",
        "legs are jerking", "shivering though i'm not cold",
        "tremors and twitching", "muscle twitching", "jerking legs",
        "hyperreflexia",
    ],
    "stimulant_drug_context": [
        "cocaine", "crack", "mdma", "ecstasy", "amphetamine",
        "speed", "meth", "crystal meth", "mephedrone", "mkat",
        "adderall overdose", "took a lot of coke",
    ],
    "agitation": [
        "agitated", "agitation", "restless and pacing",
        "can't sit still", "very worked up", "hyped up",
        "pacing and sweating", "extremely restless",
    ],
    "methanol_source_context": [
        "moonshine", "bootleg spirit", "home-brewed spirit",
        "antifreeze", "windscreen wash", "screenwash", "brake fluid",
        "industrial alcohol", "methanol", "ethylene glycol",
        "antifreeze drunk", "spirit from the market",
    ],
    "drunk_then_deteriorating": [
        "seemed drunk but", "drunk but getting worse",
        "still drunk hours later", "drunkenness that won't wear off",
        "drunk yesterday and now", "getting worse since drinking",
    ],
    "pesticide_exposure": [
        "pesticide", "organophosphate", "insecticide", "sprayed crops",
        "crop spraying", "sheep dip", "parquet", "malathion",
        "diazinon", "chlorpyrifos", "spraying the field",
        "pesticide on the crops", "spray tank", "roundup",
    ],
    "drooling_salivation": [
        "drooling", "salivating", "can't swallow the spit",
        "frothing at the mouth", "spit pooling", "excess saliva",
    ],
    "generalised_weakness": [
        "weak all over", "whole body is weak", "can't hold his head up",
        "floppy", "too weak to stand", "limp", "muscles won't work",
        "weakness everywhere",
    ],
    "slow_pulse": [
        "slow pulse", "pulse is slow", "heart rate is slow",
        "bradycardia", "slow heartbeat", "heart beating slowly",
    ],
    "snake_bite": [
        "snake bite", "snakebite", "bitten by a snake", "snake bit",
        "viper bit", "cobra bit", "adder bite", "bitten by an adder",
    ],
    "bite_site_swelling": [
        "bite is swelling", "swelling from the bite", "swollen around the bite",
        "arm swelling after the bite", "leg swelling after the bite",
        "spreading swelling from", "swelling spreading up",
    ],
    "bleeding_gums_unexplained": [
        "bleeding gums", "gums bleeding", "nosebleeds that won't stop",
        "bleeding from the gums", "blood blister", "oozing from puncture",
        "unexplained bruising after the bite",
    ],
    "regional_lymph_pain": [
        "tender glands in the groin", "tender glands in the armpit",
        "painful nodes draining", "armpit nodes hurting",
        "groin nodes tender", "lymph nodes tender near",
    ],
    # --- 6.5 obstetric emergencies ---
    "pregnancy_context": [
        "pregnant", "pregnancy", "weeks gestation", "weeks' gestation",
        "trimester", "due date", "gravid", "expecting",
        "the baby is moving less", "my bump",
    ],
    "birth_recently": [
        "just given birth", "gave birth", "since the birth",
        "after the birth", "yesterday i had the baby", "had a baby",
        "delivered", "postpartum", "day 3 after delivery",
        "six days after giving birth", "newborn at home",
    ],
    "bleeding_heavy": [
        "bleeding heavily", "bleeding very heavily", "soaking",
        "soaked through", "won't stop bleeding", "flooding",
        "clots the size of", "huge clots", "passing big clots",
        "bleeding through the pads", "a pad an hour",
    ],
    "contractions_frequent": [
        "contractions every", "contractions three minutes",
        "contractions two minutes", "contractions 3 minutes",
        "contractions 2 minutes", "contractions are coming fast",
        "tightenings every", "pains every three minutes",
        "pains every two minutes", "pains every few minutes",
    ],
    "pushing_sensation": [
        "need to push", "needs to push", "feels like pushing",
        "want to push", "urge to push", "body is pushing",
        "pushing now",
    ],
    "crowning_head_visible": [
        "crowning", "head is visible", "can see the head",
        "can see her head", "baby's head is there", "head is coming",
        "the head is out",
    ],
    "waters_broke_gush": [
        "waters broke", "waters have broken", "water broke",
        "gush of water", "waters went", "membranes ruptured",
        "fluid gushed", "my waters",
    ],
    "labour_prolonged": [
        "in labour for", "in labor for", "labouring for hours",
        "contracting all day", "in labour since last night",
        "labour for 12 hours", "labour for hours", "no progress",
        "been in labour all day",
    ],
    "exhaustion": [
        "exhausted", "completely worn out", "can't keep going",
        "no energy left", "collapse with tiredness", "past exhaustion",
    ],
    "head_delivered_body_stuck": [
        "head is out but", "head delivered but", "baby's head is born but",
        "head born but the shoulders", "head is out and the body",
        "shoulders stuck", "body won't come", "shoulders are stuck",
    ],
    "cord_felt_visible": [
        "cord is coming out", "cord has come out", "felt the cord",
        "cord hanging", "cord presenting", "the cord is out",
        "cord prolapse", "something hanging after my waters",
    ],
    "tissue_passed": [
        "passed tissue", "passed something solid", "passed clots and tissue",
        "something came away", "passed the sac", "tissue in the toilet",
        "grey material passed",
    ],
    "lochia_offensive": [
        "smelly bleeding", "offensive discharge", "bleeding smells",
        "discharge smells bad", "smells foul", "bad-smelling lochia",
        "lochia smells",
    ],
    "fundal_tenderness": [
        "womb is tender", "fundus tender", "tummy is tender below the bump",
        "pain when i press my tummy after the birth", "uterine tenderness",
        "sore womb",
    ],
    "breast_redness_painful": [
        "red painful breast", "breast is red and painful",
        "painful red area on the breast", "mastitis", "breast engorged and red",
        "flu-like with a red breast",
    ],
    # --- 6.6 oncology-supportive + dermatological emergencies ---
    "chemo_cancer_treatment": [
        "chemotherapy", "chemo", "on chemo", "having chemo",
        "cancer treatment", "immune suppression from treatment",
        "radiotherapy last month", "infusion two weeks ago",
        "on immunotherapy", "on carboplatin", "on cisplatin",
        "cycle of chemo", "white cell injection",
    ],
    "cancer_known_history": [
        "has cancer", "cancer history", "with cancer", "known cancer",
        "breast cancer", "lung cancer", "prostate cancer", "myeloma",
        "lymphoma", "secondary cancer", "metastases", "metastatic",
        "cancer spread to", "under oncology", "palliative cancer",
    ],
    "new_or_worsening_back_pain": [
        "new back pain", "back pain getting worse over weeks",
        "back pain worse at night", "worse at night in bed",
        "back pain for weeks getting worse", "band-like tightness around the trunk",
        "tightness around the chest and tummy", "back pain no injury",
    ],
    "leg_weakness_bilateral": [
        "legs feel weak", "both legs weak", "legs giving way",
        "difficulty walking", "trouble walking", "legs won't hold",
        "unsteady on the feet", "getting weaker in the legs",
        "legs feel heavy and weak",
    ],
    "bladder_bowel_change": [
        "can't control my bladder", "incontinent of urine", "wetting herself",
        "loss of bladder control", "constipated then loose", "losing control of the bowels",
        "bladder not working", "new incontinence",
    ],
    "facial_neck_arm_swelling": [
        "face is swollen", "swollen face", "puffy face", "face and neck swollen",
        "eyes are puffy", "swelling of the neck", "arm is swollen and blue",
        "both arms swollen", "collars feel tight", "collar is tight",
        "neck is swollen", "wakes with a puffy face",
    ],
    "neck_veins_distended": [
        "neck veins", "veins sticking out on the neck",
        "veins in the neck bulging", "distended neck",
    ],
    "worse_lying_flat": [
        "worse lying down", "worse when i lie", "worse lying flat",
        "can't lie flat", "worse bending forward", "worse when bending",
    ],
    "headache_worse_morning": [
        "headache worse in the morning", "worse on waking",
        "wakes me in the night", "headache on waking",
    ],
    "new_drug_started": [
        "new tablet", "started a new", "new antibiotic", "new medicine",
        "started lamotrigine", "started carbamazepine", "new anticonvulsant",
        "started allopurinol", "new painkiller", "changed medication last week",
        "on sulfasalazine", "started trimethoprim", "new drug",
    ],
    "rash_mucosal_involvement": [
        "lips are sore and blistered", "mouth ulcers and rash",
        "eyes red and sore with a rash", "rash in the mouth",
        "sore lips and rash", "genital ulcers with rash",
        "rash with mouth involvement", "can't eat because of sore lips",
        "eyes stuck together with a rash",
        # 7.2: the patient-order phrasings the audit probe used
        "sore blistered lips", "blistered lips and eyes",
        "lips and eyes are sore", "rash with sore lips",
        "blisters on the lips", "sore mouth with the rash",
    ],
    "skin_pain_out_of_proportion": [
        "skin hurts to touch", "skin is exquisitely tender",
        "burning pain in the skin", "rash hurts more than it looks",
        "pain out of proportion", "far more painful than it looks",
        "unbearable skin pain",
        # 7.2: bare 'skin hurts' is safe here — it is the phrase patients
        # actually use, and no benign corpus entry credits it
        "skin hurts", "skin stings all over",
    ],
    "blistering_skin_detaching": [
        "skin peeling off", "skin coming away", "blisters breaking leaving raw skin",
        "skin sloughing", "peels when rubbed", "nikolsky",
    ],
    "eczema_known_context": [
        "eczema", "atopic dermatitis", "his eczema", "her eczema",
        "eczema flare",
    ],
    "punched_out_erosions_clustered": [
        "little holes in the skin", "punched out", "clusters of small ulcers",
        "little craters", "monomorphic spots", "weeping pinpoint erosions",
    ],
    "pain_out_of_proportion_skin": [
        "pain out of proportion", "far more painful than it looks",
        "excruciating pain at the site", "screaming in pain at the site",
        "pain much worse than the wound looks",
    ],
    "rapid_spreading_swelling_skin": [
        "spreading fast", "spreading by the hour", "getting bigger before our eyes",
        "redness crossing the line within hours", "doubled in size since this morning",
        "spreading rapidly",
    ],
    "skin_discolouration_dark": [
        "turning purple", "going black", "black patch", "purple discolouration",
        "skin going dusky", "grey-black areas",
    ],
    "crepitus_skin": [
        "crackling under the skin", "crunchy to touch", "crepitus",
        "air under the skin", "bubbles under the skin",
    ],
    "generalised_red_skin": [
        "red all over", "whole body is red", "red from head to toe",
        "generalised red rash everywhere", "all his skin is red",
    ],
    "skin_shedding_scaling": [
        "skin peeling in sheets", "scaling off", "skin flaking off in flakes",
        "sheds like dandruff everywhere", "peeling all over",
    ],
    "shivering_temperature_instability": [
        "shivering", "rigors and can't get warm", "can't keep warm",
        "feels cold all the time", "temperature keeps swinging",
    ],
    # --- 6.7 paediatric protection & syndromes ---
    "bruise_torso_site": [
        "bruises on his back", "bruises on her back", "bruise on his tummy",
        "bruise on her tummy", "bruises on the belly", "bruises on his chest",
        "bruise behind the ear", "bruises on the ears", "bruises on the neck",
        "bruised trunk", "bruises on his bottom", "bruises on her bottom",
    ],
    "patterned_bruise_marks": [
        "bite mark", "bite marks", "hand print", "handprint", "slap mark",
        "finger marks", "finger bruises", "grab marks", "belt mark",
        "belt welt", "loop bruise", "linear bruise", "linear burn mark",
        "bruise like a hand", "imprint of",
    ],
    "inconsistent_history": [
        "don't know how he got", "don't know how she got",
        "no idea how he got", "no idea how she got", "can't explain the bruise",
        "can't explain the injury", "explanation doesn't fit",
        "story keeps changing", "stories don't match", "no explanation for",
        "didn't seek help for days", "waited three days before",
    ],
    "frozen_watchfulness": [
        "frozen watchfulness", "flinches when i move", "cowers",
        "won't make eye contact", "startles at every noise",
        "goes stiff when picked up",
    ],
    "delayed_presentation_injury": [
        "happened days ago but", "injury was last week and only now",
        "noticed the bruise days ago", "injury days before bringing",
    ],
    "fever_five_days_plus": [
        "fever for five days", "fever for 5 days", "fever for six days",
        "fever for 6 days", "fever for seven days", "fever for a week",
        "fever for over a week", "fever lasting five days",
        "fever for more than four days", "temperature for five days",
        "temperature for a week", "feverish for five days",
        "fever now day five", "fever now day six",
    ],
    "red_eyes_injection": [
        "red eyes", "both eyes red", "eyes are red", "bloodshot eyes",
        "redness in both eyes", "eyes look red and angry", "red eyes without discharge",
    ],
    "cracked_red_lips": [
        "cracked lips", "dry cracked lips", "red cracked lips",
        "lips are cracked", "lips cracked and bleeding", "sore cracked lips",
    ],
    "inconsolable_irritability": [
        "inconsolable", "so irritable", "very irritable", "extremely irritable",
        "can't be comforted", "screaming and nothing helps",
    ],
    "red_palms_soles": [
        "red palms", "red soles", "hands and feet are red and swollen",
        "red swollen hands", "red swollen feet", "palms are bright red",
    ],
    "strawberry_tongue": [
        "strawberry tongue", "tongue like a strawberry", "red bumpy tongue",
        "tongue is bright red with bumps",
    ],
    "peeling_fingers": [
        "peeling fingers", "skin peeling off his fingers",
        "peeling toes", "fingers peeling", "peeling palms",
        "skin coming off the fingers and toes",
    ],
    "neck_gland_swollen_one_side": [
        "swollen gland on one side of the neck", "one gland in the neck",
        "lump on one side of his neck", "single swollen neck gland",
    ],
    "palpable_purpura": [
        "purpura", "purpuric", "purple spots you can feel",
        "raised purple rash", "purple bumps you can feel",
        "bumpy purple rash", "can feel the spots",
    ],
    "purpura_buttocks_legs": [
        "on his legs and bottom", "on her legs and bottom",
        "legs and bottom", "rash on the buttocks", "purpura on the legs",
        "purple rash on the bottom", "spots on his bottom",
        "spots on her bottom", "backside and legs",
    ],
    "joint_pain_ankles_hsp": [
        "ankles are swollen", "swollen ankles", "ankles swollen and sore",
        "swollen knee", "knees are swollen", "sore swollen ankles",
        "can't walk on his ankles", "can't walk on her ankles",
    ],
    "blood_in_urine_child": [
        "blood in his urine", "blood in her urine", "wee is red",
        "urine looks red", "pink urine", "blood in the wee", "red urine",
    ],
    "sore_throat_last_week": [
        "sore throat last week", "had a sore throat a week ago",
        "recent sore throat", "cold two weeks ago", "tonsillitis last week",
        "sore throat a fortnight ago",
    ],
    "scrotal_swelling_pain": [
        "swollen testicle", "testicles are swollen", "scrotal swelling",
        "painful swollen scrotum", "swollen painful testicle",
    ],
    "seizure_with_fever_child": [
        "fit with a fever", "fit with the fever", "convulsion with fever",
        "seizure with a temperature", "febrile convulsion", "fit while feverish",
        "convulsed with the fever", "seizure when feverish", "fits with fever",
        "a fit when she was hot",
    ],
    "seizure_recovered_quickly": [
        "back to himself now", "back to herself now", "back to normal within an hour",
        "fine after an hour", "settled quickly after the fit",
        "completely back to normal afterwards", "back to his usual self",
    ],
    "young_baby_age_marker": [
        # anchored to baby contexts: bare "week old" would match
        # "a week old rash"
        "week old baby", "week-old baby", "weeks old baby", "week old boy",
        "week old girl", "weeks old boy", "weeks old girl", "newborn",
        "neonate", "one month old baby", "six week old", "6 week old",
        "8 week check", "eight week check", "under three months",
        "little baby", "tiny baby", "months old baby",
    ],
    "fever_newborn": [
        "fever in a newborn", "newborn has a temperature",
        "baby under three months with a fever", "fever at three weeks old",
        "temperature in a newborn",
    ],
    "grunting_breathing": [
        "grunting", "grunting with each breath", "grunty breathing",
        "making grunting noises",
    ],
    "sleepy_newborn": [
        "very sleepy", "sleepy baby", "hard to wake", "difficult to wake",
        "won't wake for feeds", "lethargic baby", "sleepy and won't feed",
    ],
    "temperature_unstable_newborn": [
        "temperature is low", "low temperature", "cold baby",
        "temperature below normal", "not keeping warm", "baby feels cold",
    ],
    "umbilical_discharge": [
        "umbilical discharge", "cord stump is smelly", "pus from the belly button",
        "weeping cord", "smelly umbilicus", "belly button is red and weeping",
    ],
    "jaundice_first_48_hours": [
        "jaundice in the first day", "yellow on day one", "jaundiced at 24 hours",
        "jaundice within 48 hours", "yellow in the first two days",
        "jaundice on day 2",
    ],
    "pale_stool_dark_urine": [
        "pale stools", "pale poo", "poo is pale", "white stools", "white poo",
        "grey stool", "chalky stool", "wee like tea", "urine like tea",
        "dark wee", "brown urine",
    ],
    "prolonged_jaundice": [
        "still yellow", "still jaundiced", "jaundice for three weeks",
        "jaundice for a fortnight", "still yellow at a month",
        "yellow for two weeks now",
    ],
    "slapped_cheek_rash": [
        "slapped cheek", "slapped-cheek", "bright red cheeks",
        "cheeks like she's been slapped", "slapped face appearance",
        "cheeks look like they've been slapped",
    ],
    "lacy_rash_arms": [
        "lacy rash", "lacy pattern", "lace-like rash", "net-like rash",
        "lacy rash on her arms", "lacy rash on his arms",
    ],
    "mild_unwell": [
        "mildly unwell", "a bit off", "not himself but drinking",
        "slightly under the weather", "well in himself apart from",
    ],
    "joint_pain_adults": [
        "aching joints", "joint pains", "sore joints", "wrists are sore",
        "arthralgia", "fingers are achy",
    ],
    # --- 6.8 post-exposure prophylaxis ---
    "bite_wound_exposure": [
        "bitten", "bite wound", "bite marks", "bitten by a dog",
        "bitten by a cat", "bitten by a monkey", "dog bite", "cat bite",
        "monkey bite", "scratched by a dog", "scratched by a cat",
        "scratched by a monkey", "animal bite",
    ],
    "saliva_broken_skin": [
        "licked a fresh cut", "lick on broken skin",
        "saliva on an open wound", "licked the wound",
        "licked the scratch",
    ],
    "bat_contact": [
        # anchored: bare "bat" sits inside "combat"/"debate"
        "a bat", "the bat", "bat flew", "bat bite", "bat scratched",
        "found a bat", "bats in", "bat on",
    ],
    "rabies_region_exposure": [
        # 8.1: this list once carried bare country names ("nepal",
        # "india"...) — substring matching meant a Nepal TREK with an
        # altitude headache scored as an emergency-tier rabies
        # contender and got 999'd by the validator. Geography alone
        # never implies a bite: only bite-context phrasings here.
        "street dog", "stray dog", "stray cat", "wild monkey",
        "monkey around", "stray abroad", "dog abroad", "bitten abroad",
        "scratched abroad", "bitten overseas", "animal abroad",
    ],
    "wound_not_treated": [
        "never had any injections", "no injections", "haven't seen a doctor",
        "not had treatment", "wound not cleaned", "no vaccination",
        "never got it seen",
    ],
    "needlestick_event": [
        "needlestick", "needle stick", "sharps injury",
        "stuck by a needle", "jabbed with a needle", "stood on a needle",
        "stepped on a needle", "used needle", "needle went through",
        "needlestick injury",
    ],
    "source_hepatitis_b": [
        # 8.1: patient-describing phrases ("hepatitis b carrier",
        # "known hepatitis b") once lived here — they claimed the
        # PATIENT'S own chronic hepatitis B as a needlestick exposure
        # story. Only SOURCE-phrasings belong in a bloodborne-exposure
        # feature.
        "source patient known hepatitis b",
        "source is hepatitis b positive", "source was hepatitis b",
        "source hepatitis b positive", "source patient hepatitis b",
        "source is hbsag positive",
    ],
    "source_hepatitis_c": [
        "hepatitis c positive", "known hepatitis c",
        "hepatitis c carrier",
    ],
    "source_hiv_positive": [
        "hiv positive", "has hiv", "known hiv", "with hiv",
        "hiv positive source",
    ],
    "mucosal_blood_splash": [
        "blood splash in my eye", "blood in my eye", "splash of blood",
        "blood splashed", "blood in the eye", "blood in my mouth",
    ],
    "unprotected_exposure_event": [
        "condom broke", "condom split", "condom came off",
        "sexually assaulted", "unprotected sex with", "rape",
    ],
}
