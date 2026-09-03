"""The consultation craft — the "doctor" skills.

Stage 5, Task 1. The skills Glenn weighted most heavily: eliciting the
patient's agenda, structuring information, safety-netting as a formula
rather than a mumble, handling difficult consultations, and saying "I
don't know yet" in language that maintains trust.
"""
from typing import Dict, List


def ice_questions(concern: str = "") -> List[str]:
    """Ideas, Concerns, Expectations — the patient's agenda, by name."""
    base = [
        "Ideas: 'What do you think might be going on?'",
        "Concerns: 'Is there anything you're worried this might be?'",
        "Expectations: 'What were you hoping we could do about it today?'",
    ]
    c = concern.lower()
    if "cancer" in c:
        base.append("Name the fear: 'You mentioned cancer — can I ask what "
                    "made that come to mind?'")
    if "tired" in c or "fatigue" in c:
        base.append("Fatigue expectations: 'What would good energy look like "
                    "for you — what are you aiming to get back to?'")
    if "pain" in c:
        base.append("Pain goal: 'What could you do again that the pain stops "
                    "you doing now?'")
    return base


CHUNKING_RULES: List[str] = [
    "Ask one question at a time; park the rest visibly ('I'll come back to "
    "the sleep problem — first the chest pain')",
    "Chunk and check: after 2-3 exchanges, summarise what you heard and ask "
    "what you missed",
    "Screen: 'Is there anything else you were hoping to cover?' — ask it "
    "TWICE; the second ask surfaces the real agenda",
    "The golden minute: let the patient speak uninterrupted for the first "
    "60 seconds — it shortens the consultation",
    "Sit down, look up from the screen, match pace — the consultation is "
    "the treatment as much as anything prescribed",
]


def chunking_rules() -> List[str]:
    """Five structural rules that keep a consultation on track."""
    return list(CHUNKING_RULES)


SPIKES_STEPS: List[str] = [
    "Setting: privacy, sitting down, no interruptions, warning shot "
    "('I'm afraid I have some difficult news')",
    "Perception: 'What do you understand about your illness so far?' — "
    "anchor to what they already know",
    "Invitation: 'How much detail would you like?'",
    "Knowledge: warn, pause, then deliver the information in plain language "
    "in small chunks — no jargon",
    "Emotions: respond to the reaction BEFORE more information — name the "
    "silence, allow it",
    "Strategy and summary: agree concrete next steps; write them down; "
    "book the follow-up before they leave",
]


def spikes_steps() -> List[str]:
    """SPIKES — breaking difficult news, step by step."""
    return list(SPIKES_STEPS)


def safety_net_formula(what_to_expect: str, what_changes_mind: str,
                       timescale: str) -> str:
    """Safety-netting as a complete sentence, not a mumbled 'come back if
    worse': expected course, the specific changes that matter, and a
    timeframe — said aloud and written down."""
    return (f"Expected course: {what_to_expect}. Come back or seek urgent "
            f"care if: {what_changes_mind}. Timeframe: {timescale}. "
            "Say it, then write it down.")


DIFFICULT_CONSULTATIONS: Dict[str, List[str]] = {
    "the_angry_patient": [
        "Anger is usually fear wearing armour — ask about the fear under it",
        "Do not match tone; slow down, lower the volume",
        "Acknowledge explicitly: 'I can see this has been frustrating' — "
        "before any explanation",
        "Separate the system's failure from your own: apologise for what "
        "you own, explain what you will do next",
        "Never block the exit; stay seated; if threatened, end the "
        "consultation and follow the practice protocol",
    ],
    "the_reassurance_seeker": [
        "Repeated reassurance without exploration feeds the loop",
        "Ask what the worry would mean if true (catastrophic meaning drives "
        "the return)",
        "Reassure against the SPECIFIC fear, with the evidence: 'the ECG "
        "shows X, which is why this isn't Y'",
        "Agree a plan for if symptoms change — structure replaces infinite "
        "reassurance",
    ],
    "the_bringer_of_lists": [
        "Negotiate the agenda in the first minute; the list is anxiety "
        "management, not rudeness",
        "Pick one or two items together; book the rest — do not attempt all "
        "in ten minutes",
    ],
    "the_silent_patient": [
        "Silence is data: allow it, count five seconds before filling it",
        "Try the indirect route: 'Some people with this find it hard to "
        "talk about — is that how it is for you?'",
        "Consider depression, shame, coercion, or a hidden agenda — the "
        "presenting complaint is not always the complaint",
    ],
    "the_internet_researcher": [
        "Ask what they found and what worried them — engage, never mock",
        "Use their research as a shared document to correct: 'this part "
        "doesn't apply to you because...'",
    ],
    "the_denier": [
        "Check understanding of what has been said — denial is often "
        "unprocessed shock",
        "Do not argue; leave the door marked: 'this stays on the table "
        "whenever you want to return to it'",
        "Enlist a trusted person (with consent); document the refusal "
        "conversation and the capacity assessment",
    ],
}


def difficult_consultation_guidance(kind: str) -> List[str]:
    """Guidance for a difficult-consultation pattern, [] if unknown."""
    return list(DIFFICULT_CONSULTATIONS.get(kind, []))


def uncertainty_scripts() -> List[str]:
    """Honest uncertainty that maintains trust rather than eroding it."""
    return [
        "I don't know yet — and here is how we'll find out: [tests]. "
        "Here is what would change my mind: [signs].",
        "There are three possibilities at this point; today's job is to "
        "narrow them, not to guess.",
        "I can tell you what this isn't, which matters as much as what "
        "it is.",
        "If you're worse in [timescale], that isn't the plan failing — "
        "it's information, and I want to see it.",
    ]


CONSULTATION_MODELS: Dict[str, str] = {
    "calgary_cambridge": "Structural: initiating the session, gathering "
                         "information, explanation & planning, closing — "
                         "with the relationship continuous throughout",
    "balint": "The doctor as drug: the consultation's therapeutic effect "
              "and the patient's 'offer'",
    "neighbour": "Five checkpoints: connecting, summarising, handing over, "
                 "safety-netting, housekeeping",
    "pendleton_functional": "Consultation tasks: reason for attendance, "
                            "considered actions, doctor's management, "
                            "achieving shared understanding and shared plans",
}
