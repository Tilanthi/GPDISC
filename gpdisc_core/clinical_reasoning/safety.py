"""Level 6 safety and metacognition: emergency overlays that run BEFORE
benign reasoning, escalation classification, and safety-netting.

Design rule: a dangerous cluster detected in free text can never be
downgraded by later benign reasoning. Emergency detection is deliberately
over-inclusive — the cost of a false emergency escalation is a wasted
call; the cost of a missed emergency is a death.
"""
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .knowledge import find_condition


class EscalationLevel(Enum):
    EMERGENCY = "emergency"
    URGENT = "urgent"
    ROUTINE = "routine"
    SELF_CARE = "self_care"


@dataclass
class SafetyAssessment:
    level: EscalationLevel
    triggers: List[str] = field(default_factory=list)
    emergency_rule: str = ""
    advice: str = ""


@dataclass
class EmergencyPattern:
    rule_id: str
    patterns: List[str]          # regex, case-insensitive, all matched on same text
    min_matches: int             # how many patterns must hit
    advice: str


# Emergency rules ordered by clinical priority
EMERGENCY_RULES: List[EmergencyPattern] = [
    EmergencyPattern("sepsis", [
        r"confus", r"breath\w* fast|rapid breath|tachypno",
        r"fever|temperature|rigor",
        r"not (?:passed|passed any) urine|oliguria|mottl",
        r"fast heart|palpitation|tachycard",
    ], 2, "Possible sepsis — this is a medical emergency (999)."),
    EmergencyPattern("stroke_fast", [
        r"face (?:droop|drooping|drooped)|facial droop",
        r"slurr|arm weakness|arm drift|sudden weakness on one side",
        r"speech (?:difficulty|slurred|lost)|can'?t speak|words jumbled",
    ], 1, "Possible stroke — call 999 immediately (FAST). Time = brain."),
    EmergencyPattern("thunderclap_headache", [
        r"worst headache|thunderclap|like a (?:blow|thunder)|hit by",
        r"sudden(?:ly)? (?:severe|worst) headache",
    ], 1, "Possible subarachnoid haemorrhage — emergency assessment now."),
    EmergencyPattern("anaphylaxis", [
        r"swelling of (?:tongue|lips|throat)|throat closing",
        r"(?:lip|lips|tongue|throat|face|eyelids?) swelling"
        r"|swollen (?:lips?|tongue|throat|face|eyelids?)|angioedema",
        r"difficulty breath\w* (?:after|following) (?:bee|wasp|nut|peanut|sting|food|medicin)",
        r"widespread (?:rash|hives|urticaria).*(breath|swell|faint)",
    ], 1, "Possible anaphylaxis — adrenaline auto-injector and 999."),
    EmergencyPattern("cauda_equina", [
        r"(?:can'?t|cannot|loss of) control (?:of )?(?:my )?bladder|incontinen",
        r"saddle (?:area|numbness|anaesthesia)|numb\w* (?:between|around) (?:the )?legs",
        r"retention",
    ], 1, "Possible cauda equina syndrome — emergency MRI/same-day assessment."),
    EmergencyPattern("meningitis", [
        r"neck stiff|photophobia|light hurts",
        r"non-?blanch\w*|doesn'?t fade when press|doesn'?t disappear when pressed",
        r"fever.*headache|headache.*fever",
        r"bulging fontanelle",
    ], 2, "Possible meningitis — emergency assessment."),
    EmergencyPattern("gi_bleed", [
        r"vomit\w* blood|haematemesis|coffee-?ground",
        r"black tarry|melaena|black stool",
    ], 1, "GI bleeding — same-day emergency assessment."),
    EmergencyPattern("dka", [
        r"thirsty.*passing lots of urine|polyuria",
        r"vomit\w*.*(?:diabet|breath smell|fruity)",
        r"deep\w* (?:and )?(?:fast|rapid)? ?breath\w*|breath\w* deep\w*|kussmaul",
        r"diabet\w*.*(?:vomit|drowsy|breathless)",
    ], 2, "Possible DKA — emergency; diabetic decompensation."),
    EmergencyPattern("testicular_torsion", [
        r"(?:testicle|testicular|scrotal?).*(?:sudden|swollen|pain)",
    ], 1, "Possible testicular torsion — surgical emergency, time-critical."),
    EmergencyPattern("ectopic_pregnancy", [
        r"pregnan\w*|\bcoil\b|\biud\b|intrauterine|period(?:'s| is| was)? "
        r"(?:late|missed|irregular)",
        r"(?:one-?sided|lower) (?:abdominal|pelvic|tummy) pain",
        r"bleed\w* (?:heavily|with pain)|shoulder tip pain",
    ], 2, "Possible ectopic pregnancy — emergency. Pregnancy is never "
          "excluded by contraception: a coil or late period with one-sided "
          "pain is ectopic until proven otherwise."),
    EmergencyPattern("paediatric_rash_fever", [
        r"\b(?:child|toddler|baby|year old|infant)\b",
        r"rash",
        r"(?:doesn'?t|does not) (?:fade|disappear)|non-?blanch",
        r"fever|temperature",
    ], 4, "Non-blanching rash with fever in a child — emergency (999)."),
    EmergencyPattern("airway_obstruction", [
        r"(?<!no )(?<!not )drool\w*|hot potato|muffle\w* voice|stridor"
        r"|can'?t swallow (?:own )?saliva",
    ], 1, "Possible airway obstruction (epiglottitis/quinsy) — emergency. "
          "Keep the patient sitting up; do NOT examine the throat or lie them down."),
    EmergencyPattern("pe", [
        r"(?:swollen|painful|red|tender)[a-z ]{0,14}calf|calf (?:swelling|pain)"
        r"|recent (?:flight|surgery|immobilis\w*)|(?:after|following) (?:a )?"
        r"(?:long )?(?:flight|coach|car|train) (?:journey|trip)|long[- ]haul",
        r"breathless|pleuritic|worse on (?:breathing in|deep breath\w*)",
    ], 2, "Possible pulmonary embolism — emergency assessment now."),
    EmergencyPattern("acs", [
        r"crush\w* chest pain|chest pain.*(sweat|cold clammy|radiat\w* to (?:arm|jaw))",
        r"chest (?:pain|pressure|tightness).*\b(?:20|30|60|hour|night)s?\b",
    ], 1, "Possible acute coronary syndrome — call 999."),
    EmergencyPattern("visual_curtain", [
        r"\bcurtain\b|flashes? and floaters|(?:loss|lost) of (?:vision|sight)"
        r"|sudden (?:vision|sight) loss",
    ], 1, "Possible retinal detachment/glaucoma — same-day emergency eye assessment."),
    EmergencyPattern("status_epilepticus", [
        r"seizure.*(more than|over) (?:five|5) minutes|seizure.*not (?:stopped|waking)",
        r"convulsion.*(continuous|repeated)",
    ], 1, "Status epilepticus — 999."),
    EmergencyPattern("acs_atypical", [
        # NB 'sweating' deliberately excluded: night sweats over weeks is a
        # constitutional symptom, not an autonomic episode — including it
        # made every weight-loss-plus-night-sweats presentation an 'ACS'.
        r"\b(?:nausea|nauseous|vomit\w*|clammy|pale|grey)\b",
        r"(?:jaw|both arms|left arm|arm|neck|throat|back|shoulder) "
        r"(?:ache|aching|pain|discomfort|heaviness)",
        r"\b[4-9]\d\b (?:year|man|woman|old)",
    ], 2, "Atypical ACS — women and older patients often have no chest "
          "pain. Emergency assessment now."),
    EmergencyPattern("posterior_stroke", [
        r"dizz\w*|vertigo|room spin\w*",
        r"double vision|diplopia",
        r"unsteady|ataxi\w*|off balance|wobbly|falling to one side",
        r"sudden|since (?:breakfast|this morning|waking|lunch)",
    ], 3, "Sudden dizziness with diplopia or ataxia — posterior circulation "
          "stroke until excluded. Emergency."),
    # ---- Stage 6 Task 6.3: trauma & burns ----
    # NB: LOC and mechanism are separate patterns on purpose — LOC alone
    # without a head-injury mechanism is not scored; mechanism + any
    # deterioration (vomit/confusion/drowsiness) is NICE CG176 emergency.
    EmergencyPattern("head_injury_red_flags", [
        r"hit (?:my|his|her|their) head|banged (?:my|his|her|their) head|"
        r"struck (?:my|his|her|their) head|head (?:injury|wound)|"
        r"fell (?:off|from|onto|on) .{0,25}head|fell (?:off|from) (?:a |the )?"
        r"(?:ladder|bike|horse|roof|stairs|window|scaffold)|fell down the stairs",
        r"knocked out|knocked unconscious|lost consciousness|unconscious|"
        r"blacked out|out cold",
        r"vomit\w*|drows\w*|confus\w*|seizure|"
        r"clear fluid from (?:the |his |her |their )?(?:ear|nose)|"
        r"unequal pupils|weak\w* (?:arm|leg|one side)|"
        r"not (?:himself|herself) since",
        r"warfarin|anticoagulat\w*|blood thinner|apixaban|rivaroxaban|"
        r"dabigatran|edoxaban|clopidogrel",
    ], 2, "Head injury with loss of consciousness, deterioration or "
          "anticoagulation — emergency CT and neuro review now."),
    EmergencyPattern("penetrating_trauma", [
        # 'stabbed'/'stab wound' = injury; bare 'stab\w*' also matched
        # 'stabbing pain', the commonest benign pain descriptor there is
        # (7.3: a neuropathic-pain probe once escalated to 999 on this).
        r"stabbed|stab wounds?|gunshot|shot (?:in|wound|through)|"
        r"knife wound|impal\w*|"
        r"penetrat\w+ (?:wound|injur\w*|chest|abdomen|neck)",
    ], 1, "Penetrating injury — surgical emergency. Call 999 now; do not "
          "remove any impaled object."),
    EmergencyPattern("haemorrhagic_shock", [
        r"pale and (?:cold|clammy|grey|sweaty)|cold and clammy|"
        r"grey and (?:cold|clammy)|white as a sheet|pale, (?:cold|clammy)",
        r"fast (?:pulse|heart)|rapid pulse|racing (?:heart|pulse)|"
        r"weak pulse|thready",
        r"bleeding (?:heavily|badly|won'?t stop|through)|won'?t stop bleeding|"
        r"blood (?:pouring|gushing|pooling)|lost a lot of blood|haemorrhag\w*",
        r"trapped (?:under|beneath)|pinned under|"
        r"crushed (?:legs?|arms?|chest|pelvis|in)|road accident|car crash|"
        r"hit by a (?:car|lorry|van|train|bus)",
    ], 2, "Signs of shock after injury or bleeding — keep flat, press on the "
          "bleeding point, call 999 now."),
    EmergencyPattern("major_burn", [
        r"scald\w*|singed|smoke inhalation|breathed in smoke|house fire|"
        r"circumferential",
        r"burns? to (?:the |his |her |my |their )?(?:face|hands?|arms?|legs?|"
        r"chest|back|airway|genitals|feet)|burnt? (?:his |her |my |their )?"
        r"(?:face|both|chest|airway)|burned (?:his |her |my |their )?"
        r"(?:face|both|chest|airway)",
        r"boiling water|kettle|hot oil|chip pan",
        r"\d{1,2}\s?% (?:of )?(?:my|his|her|their|the) (?:body|skin|arm|leg|"
        r"chest|back|face|hand)",
    ], 1, "Major burn/scald — cool with running water 20 minutes, cling-film, "
          "keep warm, emergency transfer. Airway burns (hoarseness, singed "
          "hairs) need 999 immediately."),
    # NB: neurology pattern requires BILATERAL ('both' / plural limbs) —
    # unilateral 'numbness down my leg' is sciatica, not cord compression.
    EmergencyPattern("spinal_injury", [
        r"fell (?:from|off)|car crash|road accident|motorbike|hit by a|"
        r"high[- ]speed|collision|thrown from|ejected|"
        r"div\w+ into (?:shallow|a pool)|fall from a horse|horse fall",
        r"(?:neck|back|spine) (?:pain|hurts|tender\w*|injur)",
        r"can'?t (?:feel|move) (?:my|his|her|their) (?:legs|arms)|"
        r"numb\w* (?:in|down) both (?:legs|arms)|"
        r"pins and needles (?:in|down) both|weak\w* both|paralys\w*",
    ], 2, "Possible spinal injury — keep still, do not move the person, "
          "call 999. New bilateral limb numbness or weakness after trauma "
          "is never routine."),
    # ---- Stage 6 Task 6.4: toxicology & withdrawal ----
    # Any stated overdose is an emergency regardless of stated intent or
    # current wellness — paracetamol looks benign for 48h while the liver
    # fails. The urgent self_harm rule stays for cutting-only presentations.
    EmergencyPattern("st_elevation_ecg", [
        r"(?<!no )(?<!without )(?<!negative for )st[- ]elevat\w+|"
        r"\bstemi\b|st elevation in (?:ii|iii|avf|the inferior)",
    ], 1, "ST elevation on an ECG is an acute myocardial infarction until proven otherwise — emergency assessment NOW."),
    EmergencyPattern("any_overdose", [
        r"overdose|took (?:\d+|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred) (?:\w+ )?(?:tablets|pills|capsules)|"
        r"swallowed (?:\d+|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred) (?:\w+ )?(?:tablets|pills)|took too many|"
        r"whole packet|a handful of (?:tablets|pills|capsules)|"
        r"took a handful|more than the packet|"
        r"more than it says on the (?:box|packet)|over the (?:packet|box) "
        r"limit",
    ], 1, "Overdose — emergency assessment now, however well the person "
          "feels. Bring the packets. Do not make them vomit."),
    EmergencyPattern("opioid_toxidrome", [
        r"heroin|morphine|oxycodone|fentanyl|methadone|tramadol|codeine|"
        r"dihydrocodeine|opiate|opioid|strong painkillers| smack",
        r"won'?t wake|cannot wake|can'?t wake|unresponsive|pin[- ]?point|"
        r"tiny pupils|constricted pupils|slow(?:ing)? breathing|"
        r"breathing (?:slowly|is slow|stopped|hardly)|blue lips|"
        r"turned blue|snoring breathing|gurgling",
    ], 2, "Opioid overdose — 999. Rescue breathing first (hypoxia kills "
          "before anything else); naloxone if available; stay with them."),
    EmergencyPattern("carbon_monoxide", [
        r"carbon monoxide|\bCO\b|gas boiler|gas fire|gas heater|gas stove|"
        r"faulty boiler|charcoal|generator (?:indoors|in)|car exhaust|"
        r"exhaust fumes|engine running|blocked flue|chimney|"
        r"paraffin heater|kerosene heater|wood[- ]burning",
        r"headache|nausea|nauseous|dizz\w*|confus\w*|drows\w*|vomit\w*|"
        r"collapse|unconscious",
        r"everyone (?:in the|at home|in the flat)|whole family|"
        r"all of us|the whole household|several of us|"
        r"my partner and i both|both children and i",
    ], 2, "Possible carbon monoxide poisoning — leave the building, fresh "
          "air, 999. Pulse oximeters read falsely normal; symptoms in "
          "more than one person in the same building clinch it."),
    # NB min 3: alcohol + interruption + severe sign. Shakes/sweats alone
    # after stopping drinking is urgent (corpus), not this emergency rule.
    EmergencyPattern("delirium_tremens", [
        r"alcohol|drinker|drinking|vodka|cider|spirits|wine",
        r"stopped drinking|hasn'?t had a drink|haven'?t had a drink|"
        r"ran out|cold turkey|withdrawal|detox|custody|arrested|"
        r"admitted|in hospital|cut down",
        r"hallucinat\w*|seeing things|sees things|hearing voices|"
        r"confus\w*|seizure|delirium tremens|\bDTs\b|dels? tremens",
    ], 3, "Alcohol withdrawal delirium — emergency now. This kills ~5% "
          "untreated; it is not 'just the shakes'. Thiamine before any "
          "glucose."),
    # ---- Stage 6 Task 6.5: obstetric emergencies ----
    EmergencyPattern("eclampsia_seizure", [
        r"pregnan\w*|trimester|gestation|in labour|in labor|"
        r"(?:just )?given birth|after the birth|postpartum|had a baby",
        r"seizure|\bfit\b|fits\b|convuls\w*|collapsed|unconscious",
    ], 2, "Seizure or collapse in pregnancy, labour or after birth — "
          "eclampsia until proven otherwise. 999, recovery position, "
          "magnesium sulfate."),
    # A venomous bite is an emergency until proven dry: envenoming
    # declares within hours, so absence of swelling now means nothing.
    EmergencyPattern("venomous_bite", [
        r"snake ?bite|bitten by (?:a|an) (?:snake|adder|viper|cobra|mamba|"
        r"serpent|krait)|adder bite|scorpion sting|stung by a scorpion",
    ], 1, "Possible envenomation — keep the limb still and level, no "
          "tourniquet, no cutting, mark the swelling margin, emergency "
          "transfer. Observe at least 24h even if well."),
    EmergencyPattern("postpartum_haemorrhage", [
        r"(?:just )?given birth|since the birth|after the birth|"
        r"delivered|postpartum|had a baby|after delivery",
        r"bleeding heav\w*|soak\w*|won'?t stop bleeding|flooding|"
        r"clots? (?:the size of|bigger than|large|huge)|"
        r"a pad an hour|bleeding through",
        r"pale|clammy|dizz\w*|faint\w*|fast (?:pulse|heart)|racing|"
        r"sweat\w*|confus\w*",
    ], 2, "Bleeding after birth — 999 now. Lie flat, rub the fundus if "
          "trained, baby to breast, keep warm."),
    EmergencyPattern("imminent_birth", [
        r"crown\w*|head (?:is )?(?:visible|out|coming|born)|"
        r"can see (?:the|her|his) head|shoulders? stuck|body won'?t come|"
        r"cord (?:is |has )?(?:coming out|out|hanging|prolaps\w+)|"
        r"felt the cord|baby is coming|about to give birth",
        r"contractions? (?:every|less than) (?:one|two|three|four|five|1|2|"
        r"3|4|5) minutes?|urge to push|(?:need|want|need) to push|"
        r"feels? like pushing|pushing now|waters (?:broke|have broken|went)",
        r"head (?:delivered|is out) but|head born but",
    ], 1, "Birth is imminent or obstructed — 999 / midwife NOW; clean "
          "towels, keep mum and baby warm. Cord at the vagina: hips "
          "high, all-fours. Head out, body stuck: McRoberts, knees to "
          "chest, help now."),
    # ---- Stage 6 Task 6.6: oncology-supportive + derm emergencies ----
    EmergencyPattern("neutropenic_sepsis", [
        r"chemotherapy|chemo|on chemo|cancer treatment|immunotherapy|"
        r"radiotherapy|cycle of chemo|carboplatin|cisplatin|"
        r"white cell injection",
        r"fever|feverish|temperature|unwell|chill\w*|rigor\w*|shiver\w*|"
        r"sore mouth|confus\w*|not passing urine",
    ], 2, "Fever or sudden illness on chemotherapy — neutropenic sepsis "
          "until proven otherwise: emergency now, antibiotics within the "
          "hour."),
    EmergencyPattern("cord_compression_cancer", [
        r"(?:has|with|history of) cancer|breast cancer|lung cancer|"
        r"prostate cancer|myeloma|lymphoma|metastas\w*|under oncology|"
        r"cancer spread",
        r"back pain|spine pain|weak (?:legs|leg)|legs? (?:feel )?weak|"
        r"can'?t walk|difficulty walking|numb\w* (?:legs|saddle|between)|"
        r"incontinen\w*|bladder|can'?t control",
        r"worse at night|band[- ]like|progress\w*|getting worse|new pain",
    ], 2, "Known cancer with new back pain or any leg weakness/numbness — "
          "malignant cord compression: same-day MRI, dexamethasone, "
          "oncology. Walking is what we are protecting."),
    EmergencyPattern("necrotising_infection", [
        r"pain (?:way )?out of proportion|far more painful than|"
        r"excruciating pain|screaming in pain|unbearable pain",
        r"spreading fast|spreading rapid\w*|doubl\w+ in size|"
        r"getting bigger by the hour|crossing the marked line|"
        r"turning purple|going black|dusky|crepitus|crackling|"
        r"bubbles under the skin",
        r"fever|confus\w*|heart racing|fast pulse|collapse|not passing "
        r"urine",
    ], 2, "Pain far beyond what the skin looks like, spreading fast — "
          "necrotising infection: theatre now, not another day of "
          "antibiotics."),
    # ---- Stage 6 Task 6.7: paediatric protection & syndromes ----
    EmergencyPattern("inflicted_injury", [
        r"shak\w* (?:the |my |his |her |their |a )?"
        r"(?:baby|infant|child|son|daughter|twin)",
        r"shaken baby",
        r"\bbite marks?\b",
        r"\bbelt\b.{0,30}(?:mark|bruise|welt|hit)|\bwelts\b",
        r"slapped (?:the |my |his |her |a |their )?"
        r"(?:baby|child|son|daughter|face|him|her)",
        r"cigarette (?:burn|mark)s?",
        r"(?:burn|scald)\w*\s+(?:in|on|to)\s+(?:both )?"
        r"(?:hands?(?: and feet)?|feet|bottom|genitals?|perineum)"
        r"|glove[d]? (?:burn|pattern)|stocking (?:burn|distribution)",
        r"linear (?:burns?|bruises?|marks?)|loop\w* (?:bruise|mark|welts?)",
        r"\bfinger\w* (?:marks?|bruises?)\b|grab marks?|defensive bruise",
    ], 1, "Patterned or inflicted injury in a child — emergency now: "
          "the child is not safe to go home without assessment, and may "
          "have injuries you cannot see (shaken baby presents as "
          "sleepiness). Do not interrogate; document verbatim; involve "
          "the safeguarding lead."),
    EmergencyPattern("kawasaki_fever_days", [
        r"fever\D{0,30}(?:five|5|six|6|seven|7|eight|8|nine|9|ten|10)"
        r"\s*days?|fever for a week|fever for over a week|feverish for "
        r"(?:five|5|six|6|seven|7) days|fever now day (?:five|5|six|6|"
        r"seven|7)|temperature for (?:five|5|six|6) days|"
        r"temperature for a week",
        r"red eyes?|bloodshot|conjunctiv\w*|strawberry tongue|"
        r"cracked lips?|peeling (?:fingers|toes|palms|skin|hands)|"
        r"red (?:palms|soles|tongue|lips)|bright red tongue|"
        r"swollen neck gland|gland in the neck|inconsolable",
    ], 2, "Fever five days or more with mucocutaneous signs — Kawasaki "
          "until proven otherwise: same-day paediatrics. The coronary "
          "aneurysms this causes are prevented by IVIG inside ten days, "
          "not after."),
    EmergencyPattern("neonatal_illness", [
        r"\bnewborn\b|\bneonate\b|\b\d+ (?:day|week)s? old\b|"
        r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
        r"twelve) (?:day|week)s? old\b|"
        r"under (?:one|two|three|1|2|3) months? old|first month",
        r"fever|temperature|grunting|not feeding|won'?t feed|"
        r"poor feeding|lethargic|very sleepy|hard to wake|flopp\w*|"
        r"cold baby|low temperature|umbilical|blue lips|not waking",
    ], 2, "A baby under three months who is unwell in ANY way — fever, "
          "grunting, not feeding, floppy, cold, or 'just not right' — "
          "is a full septic workup now. Newborns hide sepsis until "
          "they collapse."),
]

URGENT_RULES: List[EmergencyPattern] = [
    EmergencyPattern("fever_after_travel", [r"fever|temperature"], 1,
                     "Fever after travel — needs same-day assessment with travel history; malaria until proven otherwise."),
    EmergencyPattern("pregnancy_bleeding_pain", [r"pregnan\w*", r"bleed|pain"], 2,
                     "Bleeding/pain in pregnancy — same-day assessment (EPU)."),
    EmergencyPattern("new_confusion_elderly", [r"confus", r"\b(?:elderly|old|78|80|85|90)\b|\byears?\b"], 2,
                     "New confusion in an older person — same-day assessment; delirium until proven otherwise."),
    EmergencyPattern("self_harm", [
        r"kill myself|suicide|end it all|self[- ]harm|hurt myself",
        r"cut\w* (?:her|him|them|my)self|cutting (?:her|him|them)",
        r"overdose|took \d+ (?:\w+ )?(?:tablets|pills)|burn\w* (?:her|him|them)self",
    ], 1, "Risk of self-harm — same-day mental-health crisis pathway."),
    EmergencyPattern("paediatric_rash_verify", [
        r"\b(?:child|toddler|baby|year old|infant)\b", r"rash",
        r"fever|temperature",
    ], 3, "Fever and rash in a child — verify the glass test in person "
         "today; any non-blanching element is an emergency."),
    EmergencyPattern("red_flag_syncope", [
        r"blackout|faint\w*|syncope|collaps\w*",
        r"no warning|without warning|palpitation\w*|while sitting|at rest|during exercis\w*",
    ], 2, "Red-flag syncope (no prodrome, palpitations, or supine/exertional) "
          "— same-day ECG and assessment."),
    EmergencyPattern("acute_abdomen_ischaemia", [
        r"out of proportion",
        r"severe (?:constant|abdominal)|distend\w*|very tender",
    ], 2, "Severe abdominal pain out of proportion to findings — same-day "
          "surgical review; mesenteric ischaemia and obstruction must not be missed."),
    EmergencyPattern("elderly_behaviour_change", [
        r"\b(?:7\d|8\d|9\d)\b|\belderly\b|\b(?:mother|father|grandma|"
        r"grandpa|nan|grandad|auntie|uncle)\b",
        r"gone quiet|not (?:her|him|them)self|off (?:her|him|his|their) "
        r"(?:food|drink)|drows\w*|new confusion|fewer words|not drinking|"
        r"less responsive|not (?:eating|drinking) much",
    ], 2, "Behaviour change in an older person — same-day assessment; "
          "delirium until proven otherwise (sepsis, hypoxia, retention, "
          "drugs all present this way)."),
    # ---- Stage 6 Task 6.7: paediatric protection ----
    # 'Those who don't cruise rarely bruise' (TEN4): a bruise on a child
    # who is not independently mobile is safeguarding-until-proven-
    # otherwise — same-day assessment even with a plausible explanation,
    # because the explanation may be the cover story.
    EmergencyPattern("non_mobile_bruise", [
        r"\bbruis\w*\b",
        r"\b(?:baby|infant|newborn|neonate)\b|"
        r"\b(?:two|three|four|five|six|seven|eight|nine|[2-9])\s?"
        r"(?:week|month)s? old\b|"
        r"\bnot (?:yet )?(?:walking|crawling|cruising|mobile)\b|"
        r"can'?t (?:walk|crawl|crawl) (?:yet|at all)",
    ], 2, "A bruise in a child who is not yet walking or cruising — "
          "same-day paediatric/safeguarding assessment. This is not an "
          "accusation; it is how injured babies are found. Do not "
          "accept 'she rolls into things' as closure on the day."),
    # ---- Stage 6 Task 6.8: post-exposure prophylaxis windows ----
    EmergencyPattern("animal_bite_exposure", [
        r"\bbitten\b|bite wound|bite marks|\bbite\b|"
        r"scratched (?:by|my)",
        r"\b(?:dog|cat|monkey|macaque|bat|bats|mongoose|fox|horse|"
        r"cow|camel|racoon|raccoon)\b",
    ], 2, "Mammalian bite or scratch — same-day assessment: wound "
          "care, antibiotics, tetanus, and the rabies PEP decision. "
          "Abroad or any bat anywhere: vaccine ± immunoglobulin today; "
          "there is no 'too late' until symptoms."),
    EmergencyPattern("methotrexate_warning_signs", [
        r"on methotrexate|taking methotrexate|methotrexate injection|"
        r"weekly methotrexate|methotrexate weekly|\bon mtx\b",
        r"\bfever\b|feverish|high temperature|temperature of 3[89]|"
        r"38\.\d|39\.\d|\brigors?\b|\bchills\b|hot and cold|"
        r"sore throat|mouth ulcers?",
    ], 2, "Fever, sore throat or mouth ulcers on methotrexate (the "
          "warning-card signs): STOP the methotrexate and same-day FBC "
          "- the UK's commonest cytotoxic disaster pattern, not "
          "wait-and-see."),
    EmergencyPattern("bloodborne_exposure_rule", [
        r"needlestick|needle stick|sharps injury|stood on a needle|"
        r"stepped on a needle|stuck by a (?:used )?needle|"
        r"jabbed with a needle|"
        r"blood splash\w* (?:in|into|to) (?:my |the )?(?:eye|face|"
        r"mouth)|blood in (?:my|the) (?:eye|mouth)|"
        r"condom (?:broke|split|came off) with|"
        r"source (?:is |was )?hiv|hepatitis [bc] positive",
    ], 1, "Bloodborne exposure — same-day assessment with the clock "
          "in mind: HIV PEP inside 72 hours (first dose before the "
          "story is complete), HBIG inside ~48 for an HBsAg-positive "
          "source, hepatitis C has no PEP but a test plan."),
]


def _match_count(pattern: EmergencyPattern, text: str) -> int:
    n = 0
    for p in pattern.patterns:
        if re.search(p, text, re.IGNORECASE):
            n += 1
    return n


class SafetyLayer:
    def screen(self, text: str, context: Optional[Dict] = None) -> SafetyAssessment:
        t = (text or "")
        ctx_text = t + " " + " ".join(str(v) for v in (context or {}).values())
        for rule in EMERGENCY_RULES:
            if _match_count(rule, ctx_text) >= rule.min_matches:
                return SafetyAssessment(
                    level=EscalationLevel.EMERGENCY,
                    triggers=[rule.rule_id],
                    emergency_rule=rule.rule_id,
                    advice=rule.advice)
        for rule in URGENT_RULES:
            # travel rule only fires if travel actually mentioned
            if rule.rule_id == "fever_after_travel" and not re.search(
                    r"travel|return\w*|holiday (?:abroad|in (?:thailand|ghana"
                    r"|nigeria|kenya|tanzania|vietnam|india|indonesia|cambodia"
                    r"|laos|myanmar|sri lanka|bangladesh|peru|bolivia|brazil"
                    r"|uganda|gambia))|malaria (?:area|zone)|abroad"
                    r"|in (?:thailand|ghana|nigeria|kenya|tanzania|vietnam|india"
                    r"|indonesia|cambodia|laos|myanmar|sri lanka|bangladesh|peru"
                    r"|bolivia|brazil|uganda|gambia|sub-?saharan)"
                    r"|(?:back from|visited|trip to) (?:thailand|ghana|nigeria"
                    r"|kenya|tanzania|vietnam|india|africa|asia)",
                    ctx_text, re.I):
                continue
            if _match_count(rule, ctx_text) >= rule.min_matches:
                return SafetyAssessment(
                    level=EscalationLevel.URGENT,
                    triggers=[rule.rule_id],
                    emergency_rule=rule.rule_id,
                    advice=rule.advice)
        return SafetyAssessment(level=EscalationLevel.ROUTINE,
                                 triggers=[], advice="")

    def safety_net_for(self, condition_id: str) -> str:
        c = find_condition(condition_id)
        return c.safety_net if c else (
            "If symptoms worsen, change, or you feel much unwell, seek urgent medical review.")

    def requires_human(self, assessment: SafetyAssessment) -> bool:
        return assessment.level in (EscalationLevel.EMERGENCY, EscalationLevel.URGENT)
