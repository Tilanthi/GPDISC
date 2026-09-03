"""Resource settings — the same escalation means different actions in
different worlds (Stage 8 Task 8.2, Tier 3).

A '999 now' disposition assumes an ambulance system. A remote clinic
hours from the nearest hospital, a humanitarian field post serving a
displaced population, and an offshore vessel with a medic and a
satellite phone each translate the same level of concern into a
different FIRST ACTION. This module never changes the level of concern
— the clinical reasoning is resource-independent — it adapts only the
disposition: how to get the patient to the care the level demands.

Philosophy: in low-resource settings the first hour of stabilisation
IS the treatment, because the referral chain may take days.
"""
from typing import Dict, List, Optional

# setting profiles: what exists, what does not, what to do about it
SETTINGS: Dict[str, Dict] = {
    "uk_general_practice": {
        "label": "UK general practice (default ruleset)",
        "has_ambulance": True,
        "transfer": "999 ambulance, pre-alerted ED, minutes to hours",
        "investigations": "same-day bloods, ECG, imaging on site or nearby",
        "assumptions": [
            "Emergency = 999. Urgent = same-day primary care or ED.",
            "Pharmacy, district nursing and out-of-hours services exist.",
        ],
    },
    "remote_rural_clinic": {
        "label": "Remote rural clinic (hours from hospital)",
        "has_ambulance": False,
        "transfer": "whatever moves: ambulance service if reachable, "
                    "private vehicle, boat, or waiting for the road",
        "investigations": "basic point-of-care tests at best "
                          "(malaria RDT, HIV test, urine dip, glucose)",
        "assumptions": [
            "No 999 system: stabilise first, then arrange transport.",
            "The nearest hospital may be 3-8 hours away — what you do "
            "before transfer is the treatment.",
        ],
    },
    "humanitarian_field": {
        "label": "Humanitarian field setting (displaced population)",
        "has_ambulance": False,
        "transfer": "coordinated referral: medical coordinator arranges "
                    "transport, security escort where needed",
        "investigations": "field lab: malaria RDT, HIV, TB smear where "
                          "programme exists; X-ray at base if at all",
        "assumptions": [
            "Referral is a negotiated decision, not an ambulance call.",
            "Protocols (MSF/ICRC/WHO) and the essential medicines list "
            "govern what can be given.",
            "Community health workers extend the clinic's reach; "
            "security constraints may override clinical urgency.",
        ],
    },
    "offshore_vessel": {
        "label": "Offshore vessel / remote site with medic",
        "has_ambulance": False,
        "transfer": "telemedicine decision: helicopter medevac is "
                    "weather- and distance-dependent",
        "investigations": "on-board kit: vitals, glucose, urinalysis; "
                          "no imaging, no bloods",
        "assumptions": [
            "Call the telemedical support service FIRST — it owns the "
            "evacuation decision.",
            "Hours of handover: treat with what is aboard while the "
            "evacuation window is decided.",
        ],
    },
}

DEFAULT_SETTING = "uk_general_practice"


def describe_setting(setting: str) -> str:
    """One-line description of the active ruleset, for the record."""
    s = SETTINGS.get(setting)
    if not s:
        return (f"Unknown setting '{setting}' — UK general practice "
                "assumptions used by default")
    return s["label"]


def disposition_guidance(level: str, setting: str) -> Dict[str, str]:
    """The disposition translation table. Returns action / transport /
    alongside / note for an escalation level under a setting. The level
    itself is never negotiated here — only how to act on it."""
    level = (level or "routine").lower()
    if setting not in SETTINGS:
        base = disposition_guidance(level, DEFAULT_SETTING)
        base["setting"] = setting or "(unspecified)"
        base["note"] = (f"Unknown setting '{setting}' — UK general "
                        "practice disposition assumed; adapt locally.")
        return base

    table: Dict[str, Dict[str, str]] = {
        "uk_general_practice": {
            "emergency": {
                "action": "Call 999 now — ambulance with pre-alert.",
                "transport": "999 ambulance",
                "alongside": "Do not delay transfer for history.",
            },
            "urgent": {
                "action": "Same-day urgent review (primary care or ED).",
                "transport": "own transport unless acutely unwell",
                "alongside": "Safety-net explicitly; specify what "
                             "changes the plan.",
            },
            "routine": {
                "action": "Routine booked review.",
                "transport": "—",
                "alongside": "Safety-net for new red flags.",
            },
            "self_care": {
                "action": "Self-care with pharmacy support.",
                "transport": "—",
                "alongside": "Safety-net for deterioration.",
            },
        },
        "remote_rural_clinic": {
            "emergency": {
                "action": "No 999 here: stabilise NOW (airway, "
                          "breathing, circulation, positioning, "
                          "whatever this presentation's first line "
                          "demands), then arrange the fastest "
                          "available transfer.",
                "transport": "ambulance service if reachable; private "
                             "vehicle or boat otherwise — never alone",
                "alongside": "Send written note + vitals + treatments "
                             "given with the patient; phone the "
                             "receiving hospital ahead.",
            },
            "urgent": {
                "action": "Clinician review today if one is on site; "
                          "otherwise arrange transfer or telephone "
                          "advice today — do not let it wait for "
                          "next week's clinic.",
                "transport": "same-day arranged transport",
                "alongside": "Start what can be started here "
                             "(point-of-care tests, first-line "
                             "treatment) before transfer.",
            },
            "routine": {
                "action": "Next clinic day or the visiting team's "
                          "next visit; write the expectation down.",
                "transport": "—",
                "alongside": "Name the red flags that must trigger "
                             "an earlier, urgent contact.",
            },
            "self_care": {
                "action": "Self-care with community health worker "
                          "follow-up where available.",
                "transport": "—",
                "alongside": "Say exactly when to come back to the "
                             "clinic.",
            },
        },
        "humanitarian_field": {
            "emergency": {
                "action": "Stabilise per field protocol now; referral "
                          "is a coordinated decision — alert the "
                          "medical coordinator immediately.",
                "transport": "programme vehicle with escort where "
                             "security requires",
                "alongside": "The referral chain may take days: what "
                             "you do in the first hour is the "
                             "treatment. Document for handover; "
                             "consent in the patient's language.",
            },
            "urgent": {
                "action": "Add to today's triage list; same-day "
                          "clinician review within the programme.",
                "transport": "programme transport if referral needed",
                "alongside": "Use the essential-medicines protocol; "
                             "community health worker follow-up "
                             "tomorrow.",
            },
            "routine": {
                "action": "Next OPD session or mobile-clinic visit.",
                "transport": "—",
                "alongside": "Categorise per programme triage; "
                             "safety-net for deterioration.",
            },
            "self_care": {
                "action": "Self-care with health-education support "
                          "in the patient's language.",
                "transport": "—",
                "alongside": "CHW checks back; return criteria "
                             "stated explicitly.",
            },
        },
        "offshore_vessel": {
            "emergency": {
                "action": "Call the telemedical support service NOW — "
                          "it owns the medevac decision.",
                "transport": "helicopter medevac, weather- and "
                             "distance-dependent",
                "alongside": "Treat with the on-board kit while the "
                             "evacuation window is decided; keep "
                             "timed notes for handover.",
            },
            "urgent": {
                "action": "Telemedicine consultation today; medic "
                          "review with remote support.",
                "transport": "evacuation or next-port decision",
                "alongside": "Monitor vitals on a written schedule; "
                             "escalate per protocol.",
            },
            "routine": {
                "action": "Next port with medical facilities, or "
                          "review at crew change.",
                "transport": "—",
                "alongside": "Written plan for the medic; red flags "
                             "that trigger a telemedicine call.",
            },
            "self_care": {
                "action": "Self-care from the on-board formulary.",
                "transport": "—",
                "alongside": "Report to the medic if not improving "
                             "within the expected course.",
            },
        },
    }

    entry = table[setting].get(level) or table[setting]["routine"]
    return {
        "setting": setting,
        "level": level,
        "action": entry["action"],
        "transport": entry["transport"],
        "alongside": entry["alongside"],
        "note": "",
    }


def setting_line(level: str, setting: Optional[str]) -> Optional[str]:
    """The one-line disposition adaptation for a consultation record.
    None when the setting is the default (UK general practice) — the
    existing referral text already says what to do there. Never lowers
    the level; only translates the action. In settings without an
    ambulance system the line says explicitly that it OVERRIDES the
    default 'call 999' text, so the two never read as contradictory."""
    if not setting or setting == DEFAULT_SETTING \
            or setting not in SETTINGS:
        return None
    g = disposition_guidance(level, setting)
    no_ambulance = (not SETTINGS[setting]["has_ambulance"]
                    and g["level"] == "emergency")
    lead = ("NO AMBULANCE SYSTEM HERE — this overrides the default "
            "'call 999' above:"
            if no_ambulance else
            f"[{SETTINGS[setting]['label']}]")
    line = (f"{lead} {g['action']} Transport: {g['transport']}. "
            f"{g['alongside']}")
    return line


def available_settings() -> List[str]:
    return list(SETTINGS)
