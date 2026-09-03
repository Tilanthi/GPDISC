"""Rabies post-exposure decisions — a vaccine that works until the
day symptoms begin, and a disease that is ~100% fatal after that.

Categories follow WHO/UKHSA:
  I   touching/feeding, licks on intact skin          -> no PEP
  II  nibbling, minor scratches without bleeding      -> vaccine
  III transdermal bite/scratch, saliva on broken skin,
      mucosal contact, ANY bat contact                -> vaccine + RIG

Rabies-free domestic-animal exposures (UK pet) may defer to 10-day
observation of the animal; anything abroad, stray, wild, or a bat
anywhere does not get that luxury. Local data only.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# words that make the exposure transdermal (III) vs superficial (II)
_BREAK_SKIN = re.compile(
    r"broke the skin|drew blood|bleeding|bled|deep|puncture|through "
    r"the skin|broke skin|transdermal", re.I)
_SCRATCH_ONLY = re.compile(
    r"scratch\w*|nibbl\w*|red mark|surface abrasion|graze|bite mark|"
    r"\bbite\b|\bbitten\b", re.I)
_INTACT_SKIN = re.compile(
    r"licked? (?:my |the )?(?:hand|skin|leg|arm)|lick on intact skin|"
    r"skin not broken|no break in the skin|didn'?t break "
    r"the skin", re.I)
_BAT = re.compile(r"\bbats?\b", re.I)
_ANIMAL = re.compile(
    r"\b(?:dog|puppy|cat|kitten|monkey|macaque|mongoose|fox|bat|bats|"
    r"jackal|racoon|raccoon|coyote|wolf|farm animal|horse|cow|goat|"
    r"camel)\b", re.I)
_BITE = re.compile(
    r"\bbitten\b|\bbite\b|bite wound|bite marks|teeth broke|"
    r"scratched by|scratched my|clawed|nip\w* my", re.I)

# high-risk geography: anything mentioning these is endemic-path
_ENDEMIC = re.compile(
    r"\bbali\b|indonesia|india|thailand|vietnam|philippines|myanmar|"
    r"burma|cambodia|laos|sri lanka|nepal|bangladesh|china|pakistan|"
    r"africa|kenya|tanzania|ghana|nigeria|uganda|gambia|ethiopia|sudan|"
    r"morocco|tunisia|egypt|peru|bolivia|brazil|colombia|venezuela|"
    r"mexico|guatemala|honduras|nicaragua|ecuador|madagascar|vietnam|"
    r"malaysia|bali|lombok|sumatra|java|gili|komodo|ubud|seminyak|"
    r"kuta|canggu", re.I)
_RABIES_FREE = re.compile(
    r"\buk\b|united kingdom|britain|scotland|england|wales|northern "
    r"ireland|ireland|japan|new zealand|australia|hawaii|malta|"
    r"barbados|fiji|maldives|iceland|portugal|spain (?:mainland)?|"
    r"leeds|london|manchester|birmingham|glasgow|edinburgh|at home", re.I)
_OBSERVABLE = re.compile(
    r"\bmy own (?:dog|cat|pet)|own (?:dog|cat|pet)|pet is|dog is "
    r"(?:well|vaccinated|healthy)|cat is (?:well|healthy)|observable|"
    r"we have the (?:dog|cat|animal)|the (?:dog|cat) is home|"
    r"vaccinated and well", re.I)
_SYMPTOMS = re.compile(
    r"tingling|numb\w* at the (?:bite|wound|site)|fever|hydrophobia|"
    r"difficulty swallow\w*|agitated|paralysis|aerophobia", re.I)


@dataclass
class RabiesAssessment:
    exposure_category: str = "unknown"    # I | II | III | unknown
    animal: str = "unspecified mammal"
    region_risk: str = "unknown"          # endemic | rabies_free_observable | ...
    needs_pep: bool = False
    rig_needed: bool = False
    urgency: str = ""
    wound_care: List[str] = field(default_factory=list)
    schedule: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    observation_note: str = ""


# negated injury mentions ("no scratch", "not broken") must not count
# as injuries — scrub them before the positive patterns run
_NEGATED_INJURY = re.compile(
    r"\b(?:no|not|never|without|didn'?t|doesn'?t|wasn'?t)\s+"
    r"(?:scratch\w*|bite|bites|bitten|blood|bleeding|bleed|broken|"
    r"break\w*|puncture|cut|cuts|deep|wound|wounds)\b", re.I)


def _category(text: str, bat: bool) -> str:
    if bat:
        return "III"          # bat contact is III by definition
    scrubbed = _NEGATED_INJURY.sub(" ", text)
    # precedence: broken skin beats scratch beats intact skin. "No
    # blood" after a scratch still means the skin was scratched (II).
    if _BREAK_SKIN.search(scrubbed):
        return "III"
    if _SCRATCH_ONLY.search(scrubbed) or _BITE.search(scrubbed):
        return "II"
    if _INTACT_SKIN.search(text):
        return "I"
    return "unknown"


def rabies_pep(presentation: str, context: Optional[Dict] = None) -> RabiesAssessment:
    t = (presentation or "") + " " + " ".join(
        str(v) for v in (context or {}).values())
    a = RabiesAssessment()

    m = _ANIMAL.search(t)
    a.animal = m.group(0).lower() if m else "unspecified mammal"
    bat = bool(_BAT.search(t))
    a.exposure_category = _category(t, bat)

    if _ENDEMIC.search(t):
        a.region_risk = "endemic"
    elif bat:
        a.region_risk = "lyssavirus_risk_bat"     # bats: anywhere, incl UK
    elif _RABIES_FREE.search(t) and _OBSERVABLE.search(t):
        a.region_risk = "rabies_free_observable"
    elif _RABIES_FREE.search(t):
        a.region_risk = "rabies_free_stray_or_unknown"
    else:
        a.region_risk = "unknown_treat_as_endemic"

    symptomatic = bool(_SYMPTOMS.search(t))

    # ---- the decision ----
    if symptomatic and a.exposure_category in ("II", "III"):
        a.needs_pep = True
        a.urgency = ("EMERGENCY now — symptoms after a possible rabies "
                     "exposure mean the window has closed: critical care "
                     "and public-health involvement today.")
        a.rig_needed = False   # RIG is for before symptoms
    elif a.region_risk == "rabies_free_observable" and \
            a.exposure_category in ("II", "III") and not bat:
        a.needs_pep = False    # deferred, not dismissed
        a.observation_note = (
            "Healthy, observable pet in a rabies-free country: hold the "
            "animal under 10-day observation; start PEP only if it "
            "develops signs or dies. Wound care, antibiotics and tetanus "
            "do NOT wait.")
    elif a.exposure_category in ("II", "III", "unknown"):
        a.needs_pep = True
        a.rig_needed = a.exposure_category == "III"
        a.urgency = ("Same-day PEP — vaccine today" +
                     (" plus rabies immunoglobulin into the wound"
                      if a.rig_needed else "") +
                     ". There is no 'too late' until symptoms: start "
                     "however many days or weeks have passed.")
    else:   # category I
        a.needs_pep = False
        a.urgency = ("Intact-skin exposure (WHO category I): no PEP "
                     "needed; wash the area and watch it.")

    # ---- wound care (every category) ----
    a.wound_care = [
        "Wash all wounds and scratches for 15 minutes with soap and "
        "running water, then povidone-iodine or alcohol",
        "Do not suture unless unavoidable; if it must be closed, "
        "delayed closure is preferred",
        "Antibiotic cover for mammal bites (co-amoxiclav) — infection "
        "risk is independent of rabies risk",
        "Check tetanus status",
    ]

    # ---- schedule ----
    a.schedule = [
        "Previously unvaccinated: vaccine days 0, 3, 7 and 14 "
        "(plus day 28 if immunocompromised)",
        "RIG (immunoglobulin) infiltrated into and around the wound on "
        "day 0, category III only, never after day 7",
        "Previously vaccinated: days 0 and 3 only, no RIG",
    ]
    if symptomatic:
        a.schedule = ["PEP schedule no longer applies — this is "
                      "symptomatic disease; urgent hospital care."]

    a.questions = [
        "Has the person ever been vaccinated against rabies (any prior "
        "course)?",
        "Where exactly did it happen, and was the animal stray, wild, "
        "or an owned pet?",
        "Is the animal available for observation, and is it still well?",
    ]
    return a
