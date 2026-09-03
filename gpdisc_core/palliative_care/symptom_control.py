"""Terminal symptom control and the can't-swallow route advice.

Stage 7 Task 7.4. The front door used to route every end-of-life
presentation to 'outside what I know' — honest, but useless to the
family asking how to keep a dying person comfortable. This module is
the replacement: the five terminal symptom frames (pain, agitation,
respiratory secretions, nausea, breathlessness), the drug-route table
for the moment tablets can no longer be swallowed, and the free-text
router that picks between them.

Doses are the standard UK palliative formulary (PCF-style) values as
decision support. Every drug section carries the instruction to
confirm against the LOCAL palliative formulary before prescribing —
this module scaffolds the thinking, it does not replace the
prescriber's judgement.
"""
import re
from typing import Dict, List

# ---------------------------------------------------------------------------
# The five terminal symptom frames
# ---------------------------------------------------------------------------

TERMINAL_SYMPTOMS: Dict[str, Dict] = {
    "pain": {
        "title": "terminal pain",
        "primary_sc_drug": "morphine",
        "assess": [
            "Total pain — physical, emotional, social and spiritual "
            "components all contribute; treat more than the body.",
            "Separate continuous background pain (needs regular "
            "analgesia) from breakthrough pain (needs a rescue dose).",
            "Severe renal impairment changes the opioid: morphine "
            "accumulates — alfentanil or fentanyl are the safer "
            "subcutaneous choices; involve specialist palliative care.",
        ],
        "non_drug": [
            "Positioning, warmth, presence of family, calm environment.",
            "Review whether the existing oral analgesia still works "
            "before adding anything.",
        ],
        "drugs": [
            "Morphine oral solution while the patient can still "
            "swallow — regular dose every 4 hours plus a matching "
            "breakthrough dose.",
            "When tablets cannot be swallowed: morphine subcutaneously "
            "by syringe driver over 24 hours — convert the total ORAL "
            "24-hour dose and HALVE it for the subcutaneous route.",
            "Breakthrough dose = one sixth (divide by 6) of the total "
            "24-hour subcutaneous dose, given PRN subcutaneously.",
            "Confirm every conversion and dose with the local "
            "palliative care team / formulary before prescribing.",
        ],
    },
    "agitation": {
        "title": "terminal agitation and restlessness",
        "primary_sc_drug": "midazolam",
        "assess": [
            "Look for reversible causes BEFORE sedating: untreated "
            "pain, urinary retention, constipation, medication "
            "side-effects, hypoxia, infection.",
            "Distinguish fear from delirium — fear responds to "
            "presence, reassurance and familiar voices; delirium "
            "(hallucinations, paranoia, flipping day/night) may need "
            "medication.",
        ],
        "non_drug": [
            "Quiet room, familiar voices, gentle touch, one-to-one "
            "presence — often the most effective measure.",
            "Explain to the family: agitation in the last days is "
            "common and does not mean the person is suffering; their "
            "calm presence helps more than they think.",
        ],
        "drugs": [
            "Midazolam subcutaneous 2.5-5 mg PRN; if repeated doses "
            "are needed, 10-30 mg over 24 hours by syringe driver "
            "(higher with specialist advice).",
            "Haloperidol subcutaneous 1.5-3 mg over 24 hours when "
            "delirium rather than plain restlessness dominates.",
            "Confirm doses with the local palliative care team / "
            "formulary before prescribing.",
        ],
    },
    "secretions": {
        "title": "respiratory secretions at the end of life",
        "primary_sc_drug": "hyoscine butylbromide",
        "assess": [
            "Explain to the family first: the rattling noise "
            "distresses the watchers far more than the patient, who "
            "by this stage is usually unconscious and NOT choking.",
            "Decide WITH the family whether to medicate at all — "
            "repositioning plus explanation is a legitimate, kind "
            "choice.",
        ],
        "non_drug": [
            "Reposition onto the side (recovery position) so "
            "secretions can drain from the mouth.",
            "Reduce or stop subcutaneous fluids, if the family "
            "understands and agrees.",
            "Simple, regular mouth care.",
        ],
        "drugs": [
            "Hyoscine butylbromide subcutaneous 20 mg PRN, or "
            "60-120 mg over 24 hours by syringe driver.",
            "Glycopyrronium subcutaneous 200 micrograms PRN, or "
            "600-1200 micrograms over 24 hours — less sedating than "
            "hyoscine.",
            "Antimuscarinics work best given EARLY: they prevent new "
            "secretions rather than drying what is already there. "
            "Confirm doses with the local palliative formulary.",
        ],
    },
    "nausea": {
        "title": "terminal nausea and vomiting",
        "primary_sc_drug": "haloperidol",
        "assess": [
            "Identify the cause where possible — the antiemetic "
            "follows the cause: chemical (opioids, uraemia, "
            "hypercalcaemia), gastric stasis (full, undigested-food "
            "vomits), bowel obstruction (colic + vomiting), raised "
            "intracranial pressure.",
            "Review the medication list: opioids and antibiotics are "
            "frequent culprits that can be adjusted, not just "
            "covered.",
        ],
        "non_drug": [
            "Small cold foods, avoid cooking smells, sit upright for "
            "and after meals.",
            "Regular mouth care; stop culprit drugs where possible.",
        ],
        "drugs": [
            "Haloperidol subcutaneous 1.5-3 mg over 24 hours — first "
            "line for chemical causes.",
            "Metoclopramide subcutaneous 10 mg three times daily, or "
            "30-60 mg over 24 hours — for gastric stasis.",
            "Cyclizine subcutaneous 50 mg three times daily — for "
            "raised intracranial pressure or bowel obstruction.",
            "Levomepromazine subcutaneous 6.25 mg PRN, or 6.25-25 mg "
            "over 24 hours — broad-spectrum second line.",
            "Confirm doses with the local palliative care team / "
            "formulary before prescribing.",
        ],
    },
    "breathlessness": {
        "title": "terminal breathlessness",
        "primary_sc_drug": "morphine",
        "assess": [
            "Treat reversible causes if that serves the agreed plan "
            "of care — pleural effusion, pulmonary oedema, anaemia, "
            "anxiety component.",
            "Ask patient and family whether further investigation "
            "still serves comfort; 'no more tests' is a valid "
            "decision.",
        ],
        "non_drug": [
            "Fan to the face, upright or forward-lean positioning, "
            "calm presence — the fan is unfashionably effective.",
            "Oxygen only if hypoxic AND subjectively helpful — not "
            "as routine.",
        ],
        "drugs": [
            "Low-dose morphine 2.5-5 mg orally (or the subcutaneous "
            "equivalent) relieves the SENSATION of breathlessness in "
            "advanced disease without harmful respiratory depression.",
            "Midazolam 2.5-5 mg subcutaneous PRN when anxiety "
            "dominates the picture.",
            "Confirm doses with the local palliative care team / "
            "formulary before prescribing.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Route advice for the moment tablets can no longer be swallowed
# ---------------------------------------------------------------------------

DRUG_ROUTE_TABLE: Dict[str, Dict[str, str]] = {
    "morphine": {
        "route": "Subcutaneous — syringe driver over 24 h, or PRN "
                 "subcutaneous injections",
        "conversion": "Divide the total 24-hour ORAL morphine dose by "
                      "2 for the subcutaneous route (oral : SC = 2 : 1). "
                      "Breakthrough = one sixth of the 24-h SC dose.",
    },
    "oxycodone": {
        "route": "Subcutaneous — syringe driver or PRN",
        "conversion": "Divide the total 24-hour oral oxycodone dose by "
                      "2 for subcutaneous use (oral : SC = 2 : 1).",
    },
    "diamorphine": {
        "route": "Subcutaneous — preferred by some UK services (very "
                 "soluble, small volumes)",
        "conversion": "Oral morphine : subcutaneous diamorphine is "
                      "approximately 3 : 1 — confirm locally before "
                      "converting.",
    },
    "fentanyl": {
        "route": "Transdermal patch if already established; patches "
                 "should not be STARTED for the first time in an "
                 "unstable, opioid-naive situation",
        "conversion": "Patch-to-injection conversions are "
                      "specialist territory — confirm ratios with the "
                      "local palliative team before switching.",
    },
    "midazolam": {
        "route": "Subcutaneous — PRN or syringe driver (no useful "
                 "oral form at the end of life; tablets are not the "
                 "issue, the route is)",
        "conversion": "2.5-5 mg PRN; 10-30 mg over 24 h by driver for "
                      "continuous agitation.",
    },
    "hyoscine butylbromide": {
        "route": "Subcutaneous — PRN or syringe driver",
        "conversion": "20 mg PRN; 60-120 mg over 24 h for secretions.",
    },
    "glycopyrronium": {
        "route": "Subcutaneous — PRN or syringe driver",
        "conversion": "200 micrograms PRN; 600-1200 micrograms over "
                      "24 h for secretions.",
    },
    "haloperidol": {
        "route": "Subcutaneous — syringe driver or PRN",
        "conversion": "1.5-3 mg over 24 h for terminal nausea or "
                      "delirium.",
    },
    "levomepromazine": {
        "route": "Subcutaneous — PRN or syringe driver",
        "conversion": "6.25 mg PRN; 6.25-25 mg over 24 h for nausea.",
    },
    "metoclopramide": {
        "route": "Subcutaneous — PRN or syringe driver",
        "conversion": "10 mg three times daily; 30-60 mg over 24 h for "
                      "gastric stasis.",
    },
    "cyclizine": {
        "route": "Subcutaneous — syringe driver preferred (it can "
                 "irritate as repeated PRN injections)",
        "conversion": "50 mg three times daily; 150 mg over 24 h.",
    },
    "paracetamol": {
        "route": "Intravenous or per-rectal formulations exist, but at "
                 "the end of life paracetamol is usually stopped "
                 "rather than converted — it is not a syringe-driver "
                 "drug",
        "conversion": "No subcutaneous conversion; de-prescribe if "
                      "swallowing is lost unless a specific purpose "
                      "remains.",
    },
}


def cant_swallow_route_advice(drug_or_class: str) -> Dict:
    """Route advice for one drug when the oral route is lost.

    Returns the route, the conversion arithmetic where it exists, and
    the standing caution to confirm locally. Unknown drugs get an
    honest 'ask the specialist' answer rather than a guessed ratio.
    """
    text = (drug_or_class or "").lower()
    for key, entry in DRUG_ROUTE_TABLE.items():
        if key in text:
            return {
                "drug": key,
                "route": entry["route"],
                "conversion": entry["conversion"],
                "caution": "Confirm with the local palliative care team "
                           "and formulary before prescribing.",
            }
    return {
        "drug": drug_or_class,
        "unknown": True,
        "route": "No route entry for this drug",
        "conversion": "Ask the specialist palliative care team — confirm "
                      "any conversion in the local formulary before "
                      "prescribing.",
        "caution": "Guessed equivalence ratios are how dosing errors "
                   "happen at the end of life.",
    }


# ---------------------------------------------------------------------------
# Free-text router: which frame does this presentation need?
# ---------------------------------------------------------------------------

_PLANNING_WORDS = re.compile(
    r"\b(plan|planning|prepare|preparation|organis|organiz|arrange|"
    r"what to expect|last days|final days|before (?:he|she|they|my))\b",
    re.I)

_CANT_SWALLOW = re.compile(
    r"\b(?:can'?t|cannot|unable to|no longer able to|difficulty)\s+"
    r"swallow|swallowing\s+(?:tablets?|pills?|medicine)",
    re.I)

_SYMPTOM_KEYWORDS: List = [
    ("secretions", re.compile(
        r"\b(rattl\w*|gurgl\w*|noisy (?:chest|breathing|breath)|"
        r"secretions?|fluid on the chest|death rattle)\b", re.I)),
    ("agitation", re.compile(
        r"\b(agitat\w*|restless\w*|fidget\w*|trying to climb out of bed|"
        r"picking at)\b", re.I)),
    ("nausea", re.compile(
        r"\b(nausea|nauseous|vomit\w*|being sick|throwing up|"
        r"queasy|feel sick)\b", re.I)),
    ("breathlessness", re.compile(
        r"\b(breathless\w*|short of breath|struggling to breathe|"
        r"can'?t breathe|difficulty breathing)\b", re.I)),
    ("pain", re.compile(r"\b(pain\w*|ache|aching|hurts?|sore|"
                        r"uncomfortable|distress\w*)\b", re.I)),
]


def eol_guidance_for(text: str) -> Dict:
    """Route an end-of-life presentation to its guidance frame.

    Symptom keywords win first (the family asking about a symptom need
    that symptom's protocol); anything else — including a bare 'how do
    we keep him comfortable' — routes to planning, which is the right
    default answer to the general question.
    """
    for key, pattern in _SYMPTOM_KEYWORDS:
        if pattern.search(text):
            return _frame_with_route(key, text)
    return _planning_frame()


def _frame_with_route(key: str, text: str) -> Dict:
    frame = {k: (list(v) if isinstance(v, list) else v)
             for k, v in TERMINAL_SYMPTOMS[key].items()}
    frame["key"] = key
    frame["cant_swallow"] = bool(_CANT_SWALLOW.search(text))
    if frame["cant_swallow"]:
        advice = cant_swallow_route_advice(frame["primary_sc_drug"])
        frame["route_advice"] = [
            f"{advice['drug']}: {advice['route']}. {advice['conversion']}"
        ]
    else:
        frame["route_advice"] = []
    return frame


def _planning_frame() -> Dict:
    from .planning import end_of_life_plan
    plan = end_of_life_plan()
    return {"key": "planning", "cant_swallow": False,
            "route_advice": [], **plan}


def terminal_symptom_control(symptom: str) -> Dict:
    """Guidance frame for one terminal symptom, unknowns honestly."""
    key = (symptom or "").lower().strip()
    if key in TERMINAL_SYMPTOMS:
        return {**{k: (list(v) if isinstance(v, list) else v)
                   for k, v in TERMINAL_SYMPTOMS[key].items()},
                "key": key, "cant_swallow": False, "route_advice": []}
    return {
        "key": key,
        "unknown": True,
        "title": f"{key} at the end of life",
        "assess": ["No protocol loaded for this symptom — take a full "
                   "history of what is happening and when."],
        "non_drug": ["Comfort measures and presence while advice is "
                     "sought."],
        "drugs": ["Discuss with the local palliative care team and "
                  "confirm any dose in the local formulary — no "
                  "protocol is loaded for this symptom."],
        "cant_swallow": False,
        "route_advice": [],
    }
