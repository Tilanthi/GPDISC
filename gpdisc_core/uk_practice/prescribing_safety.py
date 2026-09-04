"""High-risk prescribing — monitoring schedules + renal dose flags.

Expertise program Stage 3, Task 7. The BNF-level safety knowledge for the
drugs that most often harm in UK primary care: what to monitor and when,
plus eGFR thresholds at which prescribing must change.
"""
from typing import Dict, List, Tuple

MONITORING: Dict[str, List[str]] = {
    "lithium": [
        "Level 12h post-dose: target 0.4-0.8mmol/L (up to 1.0 in mania)",
        "U&E + TFT + calcium every 6 months; weight and BP",
        "Acute illness / dehydration / ACEi / NSAID → toxicity risk: hold and "
        "check the level",
        "Interactions to recite: NSAIDs, ACEi/ARB, thiazides, D&V — the "
        "classic exam stem",
    ],
    "methotrexate": [
        "FBC + LFT at baseline, weekly until dose stable (4-6 weeks), then "
        "every 2-4 weeks for 3 months, then 3-monthly",
        "Folic acid 5mg once WEEKLY (not on methotrexate day); NEVER daily "
        "dosing of methotrexate",
        "New cough/dyspnoea → stop and image (pneumonitis)",
        "Sore throat, mouth ulcers or fever → urgent FBC (marrow suppression)",
        "Alcohol within unit guidance; contraception for both sexes",
    ],
    "warfarin": [
        "INR to target range; more frequently after dose or interaction changes",
        "INR 4-5 no bleeding: reduce/omit a dose; >8 no bleeding: hold and "
        "give vitamin K per protocol",
        "Interactions: antibiotics (macrolides, metronidazole, "
        "co-trimoxazole), amiodarone, NSAIDs, alcohol binge",
    ],
    "doac": [
        "Annual: FBC, U&E, LFT and weight",
        "Renal function drives dosing — recheck annually (6-monthly if CKD3+)",
        "No routine coagulation monitoring — but never assume 'no monitoring'",
    ],
    "digoxin": [
        "U&E; level if toxicity suspected (nausea, visual disturbance, "
        "new arrhythmia)",
        "Toxicity amplified by hypokalaemia/hypomagnesaemia — check before "
        "increasing",
    ],
    "amiodarone": [
        "TFT + LFT every 6 months",
        "Annual chest X-ray (pneumonitis); counsel on corneal deposits and "
        "photosensitivity",
    ],
    "ace_or_arki": [
        "U&E before starting, and 1-2 weeks after starting or each dose increase",
        "Acceptable creatinine rise: <30% — beyond that, stop and reconsider",
    ],
    "spironolactone": [
        "U&E at 1 week, 1 month, then 6-monthly",
        "Hyperkalaemia risk with ACEi/ARB — the trilogy of death: ACEi + "
        "spironolactone + NSAID",
    ],
    "sodium_valproate": [
        "LFT + FBC at baseline and if clinically indicated",
        "Never in women of childbearing potential without a pregnancy "
        "prevention programme (neural tube + neurodevelopmental harm)",
    ],
    "clozapine": [
        "Weekly FBC for 18 weeks, then 2-weekly to a year, then monthly for life",
        "Any fever or sore throat → urgent FBC (agranulocytosis) and stop "
        "until the result",
        "Shared care with mental health; monitoring-service registration is "
        "mandatory",
    ],
}

# Aliases: common drug names → monitoring keys
_DRUG_ALIASES = {
    "ramipril": "ace_or_arki", "enalapril": "ace_or_arki", "lisinopril": "ace_or_arki",
    "perindopril": "ace_or_arki", "captopril": "ace_or_arki",
    "losartan": "ace_or_arki", "candesartan": "ace_or_arki", "valsartan": "ace_or_arki",
    "apixaban": "doac", "rivaroxaban": "doac", "edoxaban": "doac",
    "dabigatran": "doac",
    "valproate": "sodium_valproate", "depakote": "sodium_valproate",
    "ibuprofen": "nsaid", "naproxen": "nsaid", "diclofenac": "nsaid",
    "celecoxib": "nsaid",
}

# Renal flags: drug key → [(eGFR threshold below which the message fires, message)]
_RENAL_FLAGS: Dict[str, List] = {
    "metformin": [
        (45.0, "Review dose; eGFR 30-45: reduce to max 1g/day and avoid "
               "starting new"),
        (30.0, "STOP metformin — eGFR <30 is contraindicated"),
    ],
    "nitrofurantoin": [
        (45.0, "Avoid if eGFR <45 (insufficient urinary concentration; "
               "neuropathy risk with prolonged use)"),
        (30.0, "Contraindicated at eGFR <30"),
    ],
    "doac": [
        (30.0, "Apixaban can continue with caution ≥15; dabigatran avoid "
               "<30 — check the drug-specific threshold"),
    ],
    "nsaid": [
        (60.0, "Avoid in CKD; if unavoidable use the lowest dose, shortest "
               "course, with a PPI, and recheck renal function at 1-2 weeks"),
    ],
    "ace_or_arki": [
        (30.0, "Specialist advice before continuing or starting an ACEi at "
               "eGFR <30"),
    ],
}


def _canonical(drug: str) -> str:
    d = drug.lower().strip()
    if d in MONITORING or d in _RENAL_FLAGS:
        return d
    return _DRUG_ALIASES.get(d, d)


def monitoring_requirements(drug: str) -> List[str]:
    """Return the monitoring requirements for a high-risk drug, [] if none."""
    return list(MONITORING.get(_canonical(drug), []))


def renal_flags(drug: str, egfr: float) -> List[str]:
    """Return renal cautions for a drug at a given eGFR.

    Every threshold whose eGFR is below the given value fires, so a very
    low eGFR surfaces the full escalation ladder.
    """
    key = _canonical(drug)
    return [msg for (threshold, msg) in _RENAL_FLAGS.get(key, [])
            if egfr < threshold]


# ---- audit routing-gap fix (2026-09-04): "can I drink while taking X?" ----
# The famous one is metronidazole; the honest table covers the drugs the
# question is actually asked about. Verdicts are conservative UK practice
# (BNF / NICE CKS framing): "avoid" = do not drink; "caution" = limits and
# monitoring; "moderate ok" = no interaction at normal intake.

ALCOHOL_INTERACTIONS: Dict[str, str] = {
    "metronidazole": (
        "AVOID alcohol during treatment and for 48 HOURS after the last "
        "dose — disulfiram-like reaction (flushing, vomiting, "
        "palpitations, headache). This is the classic exam question and "
        "a real one: mouthwash and other alcohol-containing medicines "
        "count too."),
    "tinidazole": (
        "AVOID alcohol during treatment and for 48 hours after the last "
        "dose — same disulfiram-like reaction as metronidazole."),
    "flagyl": None,          # alias for metronidazole, resolved below
    "isoniazid": (
        "AVOID — alcohol adds to the hepatotoxicity risk; if drinking "
        "is ongoing, LFTs need watching."),
    "ketoconazole": (
        "AVOID — disulfiram-like reaction reported."),
    "disulfiram": (
        "NEVER — the entire point of the drug; severe reaction."),
    "warfarin": (
        "CAUTION — binge drinking swings the INR (acutely up, "
        "chronically down via the liver); a steady small intake is "
        "safer than variable drinking, and the INR check tells the "
        "truth either way."),
    "methotrexate": (
        "CAUTION — both are hepatotoxic; keep well inside UK unit "
        "limits, and the routine LFT monitoring already booked is the "
        "safety net."),
    "paracetamol": (
        "CAUTION at chronic heavy intake — the hepatotoxic threshold "
        "falls; standard doses remain safe for an occasional drinker, "
        "never exceed 4 g/day."),
    "doxycycline": (
        "Moderate intake is fine — no disulfiram reaction; chronic "
        "heavy drinking reduces blood levels, so separate doses from "
        "drinking sessions."),
    "nitrofurantoin": (
        "Moderate intake is fine — no interaction of note."),
    "amoxicillin": (
        "Moderate intake is fine — the metronidazole warning is the "
        "famous one, not this."),
    "clarithromycin": (
        "Moderate intake is fine; the interactions that matter here "
        "are with other DRUGS (statins, warfarin), not alcohol."),
}
ALCOHOL_INTERACTIONS["flagyl"] = ALCOHOL_INTERACTIONS["metronidazole"]


def alcohol_interaction(text: str) -> List[Tuple[str, str]]:
    """Drugs mentioned in the text that carry an alcohol-interaction
    row. Returns (canonical drug, guidance) pairs; empty list means no
    row matched — say so honestly rather than guessing."""
    hits = []
    for drug, guidance in ALCOHOL_INTERACTIONS.items():
        if drug in text.lower():
            hits.append((drug, guidance))
    # 'flagyl' text hits the alias row; report it under metronidazole
    return [(d, g) for d, g in hits]
