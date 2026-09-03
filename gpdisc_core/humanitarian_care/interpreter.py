"""Working through interpreters — the consultation infrastructure of
cross-language care (Stage 8 Task 8.4).

Getting this wrong is not an inconvenience: family interpreters filter
disclosures (domestic abuse, sexual health, torture), children are
silenced by what they are asked to translate, and dialect mismatches
make professional interpreters useless. The rules below are short
because they are absolute.
"""
from typing import Dict, List

_INTERPRETER_NEVER = [
    "family members — they filter what is said: abuse, sexual health "
    "and torture disclosures die in the retelling",
    "children — never, for anything, in any direction",
    "the companion who 'happens to speak the language' — relationship "
    "to the patient is a conflict of interest",
    "staff who 'know a bit of the language'",
]

_PRINCIPLES = [
    "Book a PROFESSIONAL interpreter, and check the DIALECT as well as "
    "the language — a Syrian Arabic interpreter may not serve a "
    "Kurdish patient; ask the patient which language they dream in",
    "Telephone interpreting is acceptable for routine care and "
    "emergencies; in-person for breaking bad news, safeguarding, "
    "mental-health and medico-legal conversations",
    "Brief the interpreter before the consultation: what it is about, "
    "that they must translate everything including hesitation and "
    "distress, first person only, and stop if the patient switches "
    "language",
    "Speak to the PATIENT, not the interpreter — eye contact, first "
    "person, short segments; your notes record 'via interpreter: "
    "<language, dialect>'",
    "Confidentiality works through the interpreter too: say so out "
    "loud to the patient, both ways",
    "Check understanding by teach-back, never 'do you understand?'",
    "Offer a same-gender interpreter or chaperone where culture or "
    "trauma makes it matter — and accept a refused interpreter "
    "gracefully; a patient may need a different one to disclose",
    "Write in the record that an interpreter was offered, used, or "
    "REFUSED — refusal is clinically significant and medico-legally "
    "protective",
]


def interpreter_principles(situation: str = "") -> Dict[str, List[str]]:
    """The rules, optionally emphasised for a situation ('breaking bad
    news', 'safeguarding', 'emergency', 'routine')."""
    emphasise = []
    s = (situation or "").lower()
    if "bad news" in s or "spikes" in s:
        emphasise.append("in-person interpreter for breaking bad news — "
                         "telephone strips the register this moment needs")
    if "safeguard" in s or "abuse" in s or "torture" in s:
        emphasise.append("safeguarding and torture conversations: "
                         "professional interpreter IN PERSON, never "
                         "anyone connected to the patient or the "
                         "household")
    if "emergency" in s or "999" in s:
        emphasise.append("emergencies: telephone interpreting line "
                         "immediately — do not wait for an in-person "
                         "booking, and do not let the family fill the "
                         "gap")
    if "child" in s or "minor" in s:
        emphasise.append("a child must never interpret for a parent — "
                         "role reversal harms both and hides abuse")
    return {
        "never": list(_INTERPRETER_NEVER),
        "principles": _PRINCIPLES,
        "for_this_situation": emphasise,
    }


def same_language_check(desired: str, available: str) -> str:
    """Language match honest check: returns an advice line for the
    record. A near-miss language pairing is a consultation without
    communication."""
    d, a = (desired or "").strip().lower(), (available or "").strip().lower()
    if not d or not a:
        return "Record the patient's language AND dialect before booking."
    if d == a:
        return "Language match confirmed."
    return (f"Language mismatch: patient needs '{desired}', "
            f"interpreter offers '{available}' — do not proceed on a "
            "near-miss; dialect errors are invisible until the "
            "disclosure never happens.")
