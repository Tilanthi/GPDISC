"""Controlled drugs — Misuse of Drugs Regulations schedules + guardrails.

Expertise program Stage 3, Task 5. Schedule lookup (1-5) for the drugs a
GP prescribes or meets in practice, plus per-drug prescribing guardrails
(the rules that prevent the classic CD errors) and safe-practice
requirements for CD prescriptions and registers.
"""
from typing import Dict, List

CD_SCHEDULES: Dict[str, List[str]] = {
    "1": ["lysergide", "mdma", "psilocin", "cannabinol derivatives"],
    "2": ["morphine", "diamorphine", "fentanyl", "oxycodone", "pethidine",
          "methadone", "amphetamine", "methylphenidate"],
    "3": ["buprenorphine", "ketamine", "flunitrazepam", "midazolam",
          "tramadol", "phenobarbital"],
    "4": ["diazepam", "lorazepam", "zopiclone", "zolpidem", "temazepam",
          "clonazepam", "nitrazepam", "anabolic steroids (part 2)"],
    "5": ["co-codamol and other codeine compound preparations",
          "morphine low-concentration oral solutions", "kaolin & morphine"],
}


def controlled_drug_class(drug: str) -> str:
    """Return the CD schedule ("1".."5") for a drug name, "" if not a CD.

    Substring match on the schedule's example lists; the lists carry the
    common GP-relevant entries, not the full regulations.
    """
    d = drug.lower()
    for schedule, drugs in CD_SCHEDULES.items():
        for entry in drugs:
            # Match on the leading drug token ("fentanyl patch" → "fentanyl")
            head = entry.split()[0].rstrip(",")
            if head in d:
                return schedule
    return ""


_GUARDRAILS: Dict[str, List[str]] = {
    "fentanyl_patch": [
        "NEVER initiate patches in opioid-naïve patients — only after "
        "≥60mg oral morphine-equivalent daily",
        "Patch change every 72h (some brands 96h); document site rotation",
        "After stopping: analgesia persists 12-24h — cover breakthrough pain",
    ],
    "morphine": [
        "Start modified-release only when pain is controlled on "
        "immediate-release",
        "Prescribe immediate-release for breakthrough at 1/6 of total daily dose",
        "ALWAYS co-prescribe a laxative + antiemetic for the first week; offer "
        "naloxone if overdose risk",
    ],
    "oxycodone": [
        "Second-line opioid after morphine intolerance or renal issues",
        "Oral oxycodone is roughly TWICE as potent as oral morphine: halve "
        "the total daily morphine dose when converting, then titrate",
    ],
    "methadone": [
        "Specialist initiation only — long and variable half-life",
        "QT monitoring at high dose or with other QT-prolonging drugs",
    ],
    "diazepam": [
        "Max 2-4 weeks for anxiety/insomnia — dependence develops within weeks",
        "Withdraw slowly after long use (months) to avoid seizures",
        "No repeat prescribing of hospital-initiated benzodiazepines without review",
    ],
    "zopiclone": [
        "Same 2-4 week ceiling as benzodiazepines",
        "Warn about next-morning driving if residual sedation",
    ],
    "methylphenidate": [
        "Shared care with the specialist after titration and stabilisation",
        "Monitor BP, HR, height and weight 6-monthly",
    ],
    "buprenorphine": [
        "For opioid dependence: supervised consumption initially; "
        "co-prescribe take-home naloxone and train family",
    ],
}


def prescribing_guardrails(drug: str) -> List[str]:
    """Return the prescribing guardrails for a CD, [] if none recorded.

    Accepts both bare drug names and the guarded keys (e.g. "fentanyl"
    and "fentanyl_patch" both hit the patch rules).
    """
    d = drug.lower()
    if d in _GUARDRAILS:
        return list(_GUARDRAILS[d])
    # Alias bare names to their guarded key where the meaning is unambiguous
    alias = {"fentanyl": "fentanyl_patch", "zopiclone": "zopiclone"}
    key = alias.get(d, d)
    return list(_GUARDRAILS.get(key, []))


CD_SAFE_PRACTICE: List[str] = [
    "Controlled drug register: entries within 24h, kept for 2 years after "
    "the last entry",
    "Instalment prescriptions (FP10MDA) for opioid substitution; total "
    "quantity in words AND figures for schedule 2 and 3",
    "A valid CD prescription states: precise dose, total quantity in words "
    "and figures, and the prescriber's address",
    "Prescribe naloxone to patients at risk of opioid overdose, with family "
    "training",
    "Check the patient's full opioid picture across prescribers before "
    "issuing (prescription-monitoring system where available)",
]
