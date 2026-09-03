"""Mental Capacity Act, DNACPR, safeguarding, Gillick — UK legal frameworks.

Expertise program Stage 3, Task 4. Knowledge is encoded as structured
checklists (the actual frameworks a GP applies in consultation), plus a
concern-keyword detector that flags presentations suggesting capacity
fluctuation, undue influence, or neglect.
"""
from typing import Dict, List


def capacity_two_stage_test() -> List[str]:
    """The MCA 2005 two-stage capacity test, as applied at the bedside."""
    return [
        "Stage 1 (diagnostic): Is there an impairment of, or disturbance in, "
        "the functioning of the mind or brain? If no → MCA does not apply.",
        "Stage 2 (functional): Can the person (a) understand the information "
        "relevant to the decision, (b) retain it long enough to decide, "
        "(c) use or weigh it, (d) communicate the decision by any means?",
        "All four abilities must be present for capacity; failing any one → "
        "lacks capacity FOR THIS DECISION (capacity is decision-specific and "
        "time-specific).",
        "Capacity is presumed — assess, do not assume; unwise decisions ≠ "
        "incapacity.",
        "Maximise capacity first: best time of day, hearing aids, glasses, "
        "simple language, involving a trusted person.",
    ]


def best_interests_checklist() -> List[str]:
    """Best-interests decision-making checklist (MCA s4)."""
    return [
        "The person's past and present wishes, feelings, beliefs and values",
        "Written statements made while they had capacity (advance decisions, LPA)",
        "Views of family, carers, attorney or deputy — weigh them, don't obey them",
        "Whether capacity might return (reassess later / defer non-urgent decisions)",
        "Least restrictive option that achieves the purpose",
        "Involve the person in the decision as far as possible",
        "For serious medical treatment: consider an IMCA if there is no "
        "family or friend to consult",
    ]


def dnacpr_principles() -> List[str]:
    """DNACPR / emergency-care-planning principles (post-Tracey, ReSPECT era)."""
    return [
        "A DNACPR decision is about CPR ONLY — it does not stop any other "
        "treatment.",
        "Should be made in advance as part of emergency care planning "
        "(ReSPECT), not left to the moment of arrest.",
        "Where capacity exists: the patient's informed decision governs; "
        "discuss in plain language what CPR can and cannot achieve for them.",
        "Where capacity is lacking: best-interests decision (futility, "
        "burden, outcome), documented with reasons.",
        "Aim to involve family/representatives; unresolved disagreement → "
        "second opinion, ethics support, or court.",
        "Review the decision when circumstances change; communicate it "
        "across care settings (ambulance, out-of-hours, care home).",
    ]


SAFEGUARDING_ADULT_TYPES: List[str] = [
    "Physical abuse",
    "Sexual abuse",
    "Psychological/emotional abuse",
    "Financial/material abuse",
    "Neglect and acts of omission",
    "Self-neglect",
    "Discriminatory abuse",
    "Organisational abuse",
    "Domestic abuse (including coercive control)",
    "Modern slavery",
]


def safeguarding_adult_types() -> List[str]:
    """The ten recognised categories of adult abuse/neglect (Care Act 2014)."""
    return list(SAFEGUARDING_ADULT_TYPES)


SAFEGUARDING_CHILDREN_LEVELS: List[Dict] = [
    {"level": 1, "name": "Universal",
     "detail": "All children — universal services, GP registration"},
    {"level": 2, "name": "Additional need",
     "detail": "Early help (Team Around the Family); no statutory threshold"},
    {"level": 3, "name": "Complex need / child in need (s17)",
     "detail": "Statutory social care assessment required"},
    {"level": 4, "name": "Child protection / s47",
     "detail": "Significant harm suspected → referral the same day + "
               "strategy discussion"},
]


def safeguarding_children_levels() -> List[Dict]:
    """The four threshold levels of the children's safeguarding continuum."""
    return [dict(x) for x in SAFEGUARDING_CHILDREN_LEVELS]


def gillick_checklist() -> List[str]:
    """Fraser/Gillick criteria for a under-16's consent without parental knowledge."""
    return [
        "Understands the advice and its implications (including risks)",
        "Cannot be persuaded to inform parents / to allow the clinician to do so",
        "Is likely to begin or continue sexual activity without contraception",
        "Physical or mental health is likely to suffer without treatment",
        "Best interests require treatment WITHOUT parental consent",
    ]


_CONCERN_KEYWORDS: Dict[str, List[str]] = {
    "capacity_fluctuating": ["fluctuating capacity", "confusion comes and goes",
                             "lucid intervals"],
    "undue_influence": ["undue influence", "controlling", "won't let them speak",
                        "always answers for"],
    "coercive_control": ["coercive control", "checks her phone", "not allowed out",
                         "controls all my", "controls my medicines",
                         "won't let me", "not allowed to see"],
    "financial_abuse": ["money missing", "pressure to change the will",
                        "new best friend managing finances"],
    "self_neglect": ["not eating", "hoarding", "squalor", "refusing care"],
    "pressure_ulcer_neglect": ["pressure ulcer", "pressure sore at home"],
}


def capacity_concern_keywords(text: str) -> List[str]:
    """Flag concern categories whose indicator phrases appear in the text.

    A screening aid for the consultation, not a diagnosis: a hit means
    'explore this', never 'this is abuse'.
    """
    t = text.lower()
    return [key for key, phrases in _CONCERN_KEYWORDS.items()
            if any(p in t for p in phrases)]
