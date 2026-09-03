"""Fit notes (Med3) and work advice — UK sick-certification rules.

Expertise program Stage 3, Task 8. The 'doctor as occupational physician'
knowledge: when self-certification suffices, when a Med3 is required, and
the adjustments that keep people in work rather than out of it.
"""
from typing import Dict, List

ADJUSTMENT_OPTIONS: List[str] = [
    "Phased return — building up hours over 1-2 weeks",
    "Altered hours",
    "Amended duties",
    "Workplace adaptations (equipment, seating, breaks)",
]


def fit_note_guidance(days_off: int) -> Dict:
    """Route a sickness absence to the right certification pathway.

    ``days_off`` is calendar days of absence (or the expected total).
    """
    if days_off <= 7:
        route = ("Self-certification (Statutory Sick Pay covers the first "
                 "7 days) — no fit note needed")
        employer = ("The employee self-certifies; an employer cannot require "
                    "a GP certificate for absence of 7 days or fewer")
    elif days_off <= 92:
        route = "GP fit note (Med3) required from day 8"
        employer = ("A fit note may advise 'may be fit for work' with "
                    "adjustments — employer and employee discuss feasibility")
    else:
        route = ("GP fit note; have the 'fit for work' conversation and "
                 "consider an occupational health referral if off >4 weeks")
        employer = ("Long-term sickness: occupational health involvement + "
                    "phased-return planning; DWP may assess ESA after 28 weeks")
    return {"days_off": days_off, "route": route,
            "employer_guidance": employer, "adjustments": ADJUSTMENT_OPTIONS}
