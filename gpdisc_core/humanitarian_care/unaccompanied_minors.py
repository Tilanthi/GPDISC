"""Unaccompanied asylum-seeking children — a child alone, with a
trauma history and a legal process, in one consultation (Stage 8
Task 8.4).

The duties stack: safeguarding first (age assessment, trafficking
indicators), then health (the arrival screen adapted to a child),
then consent (Gillick-style capacity is harder, not easier, through
an interpreter), then the ordinary developmental needs of any child.
"""
from typing import Dict, List

_TRAFFICKING_INDICATORS = [
    "adults who speak FOR the child and answer questions directed at them",
    "inconsistent or scripted account of the journey",
    "no knowledge of who arranged the journey or who paid",
    "signs of physical control: branding, tattoos, unusual scarring "
    "in patterns",
    "working excessive hours or no school attendance",
    "money owed for the journey (debt bondage)",
    "unexplained phone contact controlling the child's movements",
    "sexual exploitation indicators: gifts/money from unknown adults, "
    "STIs, pregnancy",
    "drug carrying or 'finding' the child in possession of drugs "
    "(county lines pattern)",
]


def unaccompanied_minor_review(context=None) -> Dict[str, List[str]]:
    """The structured review of a child arriving alone."""
    return {
        "title": "Unaccompanied asylum-seeking child — review",
        "immediate_duties": [
            "Age assessment is NOT a medical act: paediatric age "
            "estimates carry wide error ranges — the benefit of the "
            "doubt goes to the child; record the claimed age and the "
            "uncertainty, and never let a borderline age change the "
            "safeguarding response",
            "Trafficking screen — the indicators below; any single "
            "credible indicator = children's social services the SAME "
            "DAY (modern slavery / NRM duty where it applies)",
            "Confirm the legal status of the accompanying adult, if "
            "any: who are they, what is the relationship, who has "
            "parental responsibility — an unrelated 'uncle' is a "
            "safeguarding question, not a convenience",
            "Interpreters: professional, in-person where possible, "
            "age-appropriate, and NEVER the accompanying adult",
        ],
        "health_screen": [
            "The full arrival screen (see arrival_health_screen), "
            "age-weighted: growth, development, dental, vision, "
            "hearing",
            "TB + latent TB per programme; immunisation restart with "
            "written documentation — school entry will need it",
            "Mental-health first pass with an age-appropriate tool; "
            "sleep, nightmares, bedwetting, dissociation — trauma in "
            "children speaks behaviour, not words",
            "Pregnancy/sexual-health where age-appropriate, offered "
            "with the interpreter and without the accompanying adult "
            "present",
            "Chronic conditions and interrupted treatment restarted",
        ],
        "consent_and_capacity": [
            "Consent through the child's OWN demonstrated "
            "understanding (Gillick-style), assessed with an "
            "interpreter — not the accompanying adult's agreement",
            "A child refusing an interpreter offered is itself a "
            "signal worth exploring",
            "Looked-after status changes who consents: social services "
            "hold some decisions, the child holds others — document "
            "who consented to WHAT",
        ],
        "red_flags": _TRAFFICKING_INDICATORS,
    }


def trafficking_indicators() -> List[str]:
    return list(_TRAFFICKING_INDICATORS)


def minor_summary(context=None) -> str:
    s = unaccompanied_minor_review(context)
    parts = [s["title"]]
    for section in ("immediate_duties", "health_screen",
                    "consent_and_capacity", "red_flags"):
        parts.append(section.replace("_", " ").capitalize() + ":")
        parts.extend("  - " + item for item in s[section])
    return "\n".join(parts)
