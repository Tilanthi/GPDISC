"""Refugee / asylum-seeker arrival health screening (Stage 8 Task 8.4).

The evidence-based minimal new-arrival bundle, sequenced trauma-
informed: the highest-yield infectious screen first (TB above all),
immunisation catch-up on the no-records-restart principle, maternal
and child health, a gentle mental-health first pass, and the medico-
legal needs the patient themselves will ask about. What NOT to do
matters as much: no repeat invasive examinations, no interrogation
about the journey before trust, interpreter never a family member.
"""
from typing import Dict, List, Optional

# presentations that signal a new-arrival screening consultation
_ARRIVAL_PATTERNS = [
    "asylum seeker", "refugee", "just arrived as a refugee",
    "arrived as an asylum", "newly arrived", "displaced",
    "resettled", "just got refugee status", "claiming asylum",
    "moved here from a refugee camp", "transit camp", "detention centre",
    "immigration removal", "hotel placement", "initial accommodation",
]


def is_arrival_consultation(text: str) -> bool:
    """Does this presentation signal a new-arrival screening consult?"""
    t = (text or "").lower()
    return any(p in t for p in _ARRIVAL_PATTERNS)


def arrival_health_screen(context: Optional[Dict] = None) -> Dict[str, List[str]]:
    """The structured new-arrival screen. One visit cannot do it all —
    the bundle is ordered by yield and by what can harm fastest."""
    return {
        "title": "New-arrival health screen (refugee / asylum seeker)",
        "first_visit": [
            "Establish language + dialect; book a professional "
            "interpreter for everything that follows — never a family "
            "member, never a child",
            "Ask what THEY want addressed first — trust predicts every "
            "later disclosure, including torture and trafficking",
            "Acute problems today before screening: pain, pregnancy, "
            "infection, mental-health crisis",
            "TB screen (the highest-yield single item): cough >2 weeks, "
            "night sweats, weight loss, haemoptysis — and an interferon-"
            "gamma release test / chest X-ray per local programme; "
            "active TB is a public-health duty, not a choice",
            "Baseline bloods: HIV, hepatitis B AND C, syphilis; "
            "eosinophil count (intestinal parasites if raised); "
            "haemoglobin (anaemia), varicella and rubella immunity "
            "where relevant",
            "Malaria test TODAY if febrile and transited or originated "
            "in an endemic area — fever after transit is malaria until "
            "proven otherwise",
        ],
        "next_visits": [
            "Immunisation catch-up: no written records means RESTART "
            "the schedule — an extra safe vaccine beats a missed one "
            "(WHO principle); document what is given for the future",
            "Maternal and child health: pregnancy status, antenatal "
            "booking, child growth + development checks, dental",
            "Mental-health first pass — depression, PTSD, the "
            "torture-survivor care pathway where disclosed "
            "(gpdisc_core torture_survivor_care: consent and pacing "
            "are the treatment)",
            "Chronic disease re-establishment: diabetes, hypertension, "
            "epilepsy, mental-health medicines interrupted by the "
            "journey — restart before complications, not after",
            "Medico-legal: asylum report requests documented verbatim "
            "from day one (Istanbul Protocol where applicable)",
            "Nutrition, vitamin D, dental pain — the everyday things "
            "that decide whether the family engages with the system",
        ],
        "do_not": [
            "NO repeat invasive examinations already done elsewhere — "
            "each one re-traumatises; ask what has been done",
            "Do not interrogate about the journey's details before "
            "trust exists — disclosure comes on its own timeline",
            "Do not let an immigration-status question delay clinical "
            "care: everyone is entitled to urgent and necessary "
            "treatment",
            "Do not use children as interpreters — ever, for anything",
        ],
        "red_flags": [
            "Cough >2 weeks + weight loss: active TB pathway now",
            "Fever after endemic transit: malaria test now",
            "Pregnant with no antenatal care: booking this week",
            "Suicidal ideation, or disclosure of torture/trafficking: "
            "same-day senior review + safeguarding",
            "Unaccompanied child: separate pathway (see "
            "unaccompanied_minor_review)",
        ],
    }


def screening_summary(context: Optional[Dict] = None) -> str:
    """The consultation-facing rendering of the screen."""
    s = arrival_health_screen(context)
    parts = [s["title"]]
    for section in ("first_visit", "next_visits", "do_not", "red_flags"):
        parts.append(section.replace("_", " ").capitalize() + ":")
        parts.extend("  - " + item for item in s[section])
    return "\n".join(parts)
