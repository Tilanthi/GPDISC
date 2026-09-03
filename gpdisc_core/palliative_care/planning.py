"""Planning care for the last days of life.

The anticipatory ('just in case') medications, the decisions to make
while the person still has capacity, and the conversation frameworks —
cross-referenced, not duplicated, from the packages that own them:
SPIKES lives in consultation_skills, the two-stage capacity test and
DNACPR rules in uk_practice.
"""
from typing import Dict, List


def end_of_life_plan() -> Dict[str, List[str]]:
    """The structured plan for the last days of life."""
    return {
        "title": "Planning care for the last days of life",
        "priorities": [
            "Comfort becomes the explicit goal: anticipate symptoms "
            "rather than react to them.",
            "Stop what no longer serves comfort — daily bloods, "
            "monitoring, non-essential drugs, uncomfortable "
            "investigations. De-prescribing is active care.",
            "One written individual plan that everyone — family, "
            "district nursing, out-of-hours — can follow.",
        ],
        "anticipatory": [
            "Prescribe the 'just in case' / anticipatory medications "
            "BEFORE they are needed, so nothing waits on a visit: "
            "pain (morphine or suitable opioid, subcutaneous), nausea "
            "and vomiting (haloperidol or cyclizine, subcutaneous), "
            "agitation (midazolam, subcutaneous), respiratory "
            "secretions (hyoscine butylbromide or glycopyrronium, "
            "subcutaneous).",
            "They live in the fridge at home; the family and district "
            "nurses know where, and what each is for.",
            "Confirm the exact drugs, doses and indications with the "
            "local palliative formulary when prescribing.",
        ],
        "decisions": [
            "Capacity: make the big decisions WITH the person while "
            "they still have capacity — the two-stage test and "
            "best-interests framework live in uk_practice.",
            "DNACPR: decide and document in advance, with reasons, "
            "and discuss it honestly with patient and family — an "
            "undiscussed decision becomes a crisis at the worst "
            "moment.",
            "Preferred place of death (home, hospice, hospital), "
            "recorded with what has been put in place to make it "
            "possible.",
            "Documented treatment escalation plan (ReSPECT or local "
            "equivalent) so out-of-hours teams know what to do — "
            "and what not to do.",
        ],
        "communication": [
            "The conversation that dying is approaching: use SPIKES "
            "(setting, perception, invitation, knowledge, empathy, "
            "strategy) from consultation_skills — and ask first what "
            "the patient and family already understand.",
            "Do not collude with silence: gently check how much the "
            "person wants to know, but never deceive.",
            "Warn the family what the last days look like (withdrawing, "
            "sleeping more, stopping eating and drinking) — the "
            "expected surprises nobody warned them about.",
        ],
        "support": [
            "District nursing / hospice-at-home team on board early; "
            "know the local out-of-hours palliative advice line and "
            "put the number where the family can find it.",
            "Carer support: who is doing the caring, what respite "
            "exists, who they call at 3 a.m.",
            "Verification of death at home is GP / district-nurse "
            "territory — the family should know they do NOT call 999 "
            "when the death was expected and has happened.",
            "Bereavement support offered afterwards, by name and "
            "number, not as a leaflet.",
        ],
    }
