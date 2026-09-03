"""MDT roles — six computed perspectives on the consultation, plus the
six consultant opinions of Stage 9 Task 9.1.

Stage 4, Task 2: each core role's contribution is computed from the
packages already installed (clinical reasoning, uk practice) —
deterministic rules, no LLM. Roles contribute questions and
observations, never conclusions: the chair synthesises.

Stage 9, Task 9.1: six consultant roles (cardiologist, neurologist,
oncologist, paediatrician, psychiatrist, palliative physician) — the
specialist a GP would ring. A consultant speaks ONLY when their domain
is implicated (a domain condition in the differential, or
domain-specific presentation features); a specialist who comments on
everything is noise, not expertise. Consultant notes are corpus-driven:
discriminators and investigations come from the ConditionProfile of
whatever domain condition is actually in play, plus the package
cross-references (2ww criteria, palliative frames) the specialty owns.
"""
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from gpdisc_core.uk_practice.capacity_and_safeguarding import (
    capacity_concern_keywords,
)
from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements,
    renal_flags,
)


@dataclass(frozen=True)
class MDTRole:
    key: str
    title: str
    remit: str


MDT_ROLES: List[MDTRole] = [
    MDTRole("gp_chair", "GP (chair)",
            "Holds the whole picture; keeps the patient's agenda central"),
    MDTRole("geriatrician", "Geriatrician",
            "Frailty, falls, polypharmacy, atypical presentations"),
    MDTRole("clinical_pharmacologist", "Clinical pharmacologist",
            "Every symptom is a drug side effect until proven otherwise"),
    MDTRole("safeguarding_practitioner", "Safeguarding practitioner",
            "Capacity, coercion, neglect — the questions nobody else asks"),
    MDTRole("mental_health", "Mental health clinician",
            "Depression/anxiety as cause and consequence of physical illness"),
    MDTRole("patient_advocate", "Patient advocate",
            "What matters to THIS patient; plain language; no decision about "
            "them without them"),
]

# --- Consultant opinions (Stage 9, Task 9.1) ---
# The specialist on the telephone. Silent unless their domain is implicated.

CONSULTANT_ROLES: List[MDTRole] = [
    MDTRole("cardiologist", "Consultant cardiologist",
            "The trace before the troponin; rate, rhythm and territory"),
    MDTRole("neurologist", "Consultant neurologist",
            "Onset speed and anatomy decide the neuro differential"),
    MDTRole("oncologist", "Consultant oncologist",
            "Threshold to refer, staging fitness, and time-critical complications"),
    MDTRole("paediatrician", "Consultant paediatrician",
            "Weight-based everything; children compensate then crash"),
    MDTRole("psychiatrist", "Consultant psychiatrist",
            "Risk structure and delirium-before-label"),
    MDTRole("palliative_physician", "Palliative medicine consultant",
            "Reversibility, anticipatory prescribing, what the days are for"),
]

MDT_ROLES = MDT_ROLES + CONSULTANT_ROLES

_MEDICATION_HINTS = ("medication", "tablets", "pills", "on ", "prescribed",
                     "drug", "eight medications", "medicines")
_ELDER_HINTS = ("79", "80", "85", "elderly", "old ", "frail", "falls",
                "confusion", "memory")
_MOOD_HINTS = ("low mood", "depressed", "anxious", "can't sleep",
               "no interest", "worry", "panic")

# Consultant trigger hints — deliberately NARROW (substring lessons of
# stages 6-8 apply to role notes too: over-triggered advice is noise).
_CARDIAC_HINTS = ("chest pain", "chest tightness", "chest pressure",
                  "palpitations", "syncope", "fainted", "orthopnoea",
                  "swollen ankles", "breathless lying")
_NEURO_HINTS = ("seizure", "convuls", "headache", "migraine", "facial droop",
                "slurred speech", "double vision", "pins and needles",
                "numbness", "weakness down one")
_ONCOLOGY_HINTS = ("weight loss", "unexplained lump", "night sweats and weight")
_PSYCHIATRY_HINTS = ("suicidal", "self-harm", "self harm", "hearing voices",
                     "voices telling", "psychosis", "delusion", "paranoid",
                     "mania", "wants to die", "kill myself")
_PALLIATIVE_HINTS = ("dying", "end of life", "end-of-life", "palliative",
                     "hospice", "terminal", "last days", "weeks to live")
_CHILD_WORDS = ("child", "baby", "infant", "toddler", "my son", "my daughter")
_CHILD_AGE = re.compile(r"\b(\d{1,2})[- ](?:year|month|week)[- ]olds?\b",
                        re.I)

# corpus categories driving the four category-lookup consultants; the
# oncologist and palliative physician have dedicated handlers below
_DOMAINS: dict = {
    "cardiologist": ("cardiovascular",),
    "neurologist": ("neurological",),
    "paediatrician": ("paediatric",),
    "psychiatrist": ("mental_health",),
}

_ONCOLOGY_CATEGORIES = ("oncology_supportive", "haematology")


def _domain_conditions(differential, categories: Tuple[str, ...]):
    """The corpus profiles of differential conditions in these categories
    (ranked and must-not-miss both — a retained danger is exactly when a
    consultant's discriminators matter). A ranked entry counts only as a
    GENUINE contender (score >= 0.5x the leader's — the validator's
    contender gate): without this the noise tail of a 20-entry
    differential contains every category, and every consultant speaks on
    every case."""
    if differential is None:
        return []
    from gpdisc_core.clinical_reasoning.knowledge import find_condition
    ranked = list(getattr(differential, "ranked", []) or [])
    retained = list(getattr(differential, "retained_dangerous", []) or [])
    leader = max((getattr(d, "score", 0.0) for d in ranked), default=0.0)
    ids = [d.condition_id for d in ranked
           if getattr(d, "score", 0.0) >= 0.5 * leader]
    # retained counts ONLY on the emergency short-circuit (ranked empty),
    # where the single retained rule IS the working diagnosis. With a
    # ranked differential present, the retained list is the dangerous-
    # mimic tail the challenger already attacks — spanning every category,
    # it would make every consultant speak on every case.
    if not ranked and retained:
        ids += [d.condition_id for d in retained]
    out = []
    for cid in ids:
        c = find_condition(cid)
        if c is not None and c.category in categories and c not in out:
            out.append(c)
    return out


def _child_in_case(text: str, ctx: dict) -> bool:
    age = ctx.get("age_years")
    if isinstance(age, (int, float)) and age < 18:
        return True
    if any(w in text for w in _CHILD_WORDS):
        return True
    m = _CHILD_AGE.search(text)
    return bool(m and int(m.group(1)) < 18)


def contribute(role_key: str, presentation: str, context: Optional[dict] = None,
               differential=None) -> List[str]:
    """One role's computed observations on this consultation."""
    ctx = context or {}
    text = presentation.lower()
    meds = ctx.get("medications") or []
    notes: List[str] = []

    if role_key == "gp_chair":
        notes.append("Agree the agenda first: what does the patient think "
                     "is going on, and what are they most worried about?")
        if len(text.split()) > 30:
            notes.append("Long presentation — ask the patient to pick the "
                         "one problem they most want sorted today.")
        notes.append("Close the loop: summarise back, check understanding, "
                     "agree the next step out loud.")

    elif role_key == "geriatrician":
        if any(h in text for h in _ELDER_HINTS) or ctx.get("age_years", 0) >= 75:
            notes.append("Atypical presentation is the norm at this age: "
                         "infection presents as confusion, MI as breathlessness.")
            notes.append("Screen the geriatric giants: falls, continence, "
                         "cognition, nutrition, and who is at home.")
        if ctx.get("falls") or "fall" in text:
            notes.append("Falls: review the medication list first — "
                         "antihypertensives, sedatives, anticholinergics.")
        if not notes:
            notes.append("Ask about function: what can the patient no longer "
                         "do that they could last month? Function anchors "
                         "every geriatric decision.")

    elif role_key == "clinical_pharmacologist":
        if meds or any(h in text for h in _MEDICATION_HINTS):
            notes.append("Reconcile the full list including over-the-counter "
                         "and hospital leftovers before attributing symptoms.")
            egfr = ctx.get("egfr")
            for drug in meds:
                flags = renal_flags(drug, egfr) if egfr else []
                mon = monitoring_requirements(drug)
                if flags:
                    notes.append(f"{drug}: {'; '.join(flags)}")
                if mon:
                    notes.append(f"{drug}: {mon[0]}")
        notes.append("Before adding any drug, ask which existing one could "
                     "be STOPPED — the indication may have expired.")

    elif role_key == "safeguarding_practitioner":
        hits = capacity_concern_keywords(presentation)
        if hits:
            notes.append("Concern indicators present (" + ", ".join(hits) +
                         ") — explore privately, without the accompanying person.")
        if ctx.get("accompanied") and hits:
            notes.append("Interview alone for part of the consultation; "
                         "document that the opportunity was offered.")
        notes.append("Consider capacity for the decisions actually being "
                     "made today — decision-specific, presumed until assessed.")

    elif role_key == "mental_health":
        if any(h in text for h in _MOOD_HINTS):
            notes.append("Screen openly: two questions beat ten — low mood "
                         "and anhedonia — then explore risk.")
        notes.append("Physical and mental causes are not mutually exclusive; "
                     "treat both streams, do not rank them.")

    elif role_key == "patient_advocate":
        notes.append("Ask what the patient has already tried and what they "
                     "were hoping for from this consultation.")
        if ctx.get("interpreter_needed"):
            notes.append("Book an interpreter — family translation changes "
                         "the clinical story.")

    # --- Consultant opinions (Stage 9, Task 9.1) ---
    elif role_key in _DOMAINS:
        notes.extend(_consultant_notes(role_key, presentation, ctx,
                                       differential))

    elif role_key == "oncologist":
        notes.extend(_oncologist_notes(presentation, ctx, differential))

    elif role_key == "palliative_physician":
        notes.extend(_palliative_notes(presentation, ctx))

    return notes


def _corpus_notes(conditions) -> List[str]:
    """Discriminators + investigations straight from the corpus profiles."""
    notes: List[str] = []
    for c in conditions[:2]:
        if c.discriminators:
            notes.append(f"{c.name}: what separates it — "
                         + "; ".join(c.discriminators[:2]) + ".")
        if c.investigations:
            notes.append(f"{c.name} work-up: "
                         + ", ".join(i.name for i in c.investigations[:3])
                         + ".")
    return notes


def _consultant_notes(role_key: str, presentation: str, ctx: dict,
                      differential) -> List[str]:
    """The shared shape of a consultant opinion: domain conditions in the
    differential drive the corpus part; the trigger hints decide whether
    the specialty speaks at all; each adds its own craft lines."""
    text = presentation.lower()
    conditions = _domain_conditions(differential, _DOMAINS[role_key])
    craft: List[str] = []

    if role_key == "cardiologist":
        if not (conditions or any(h in text for h in _CARDIAC_HINTS)):
            return []
        craft.append("Every cardiac presentation gets a 12-lead ECG in the "
                     "first ten minutes — the trace before the troponin; "
                     "troponin answers the ACS question, not the "
                     "breathless one.")
        craft.append("Before echocardiography: rate, rhythm, and a blood "
                     "pressure you would be happy to defend — the three "
                     "numbers that change tonight's plan.")

    elif role_key == "neurologist":
        if not (conditions or any(h in text for h in _NEURO_HINTS)):
            return []
        craft.append("Onset speed is half the neuro differential: "
                     "seconds-to-maximum points vascular or seizure, "
                     "progressive-over-hours points toxic/infective, "
                     "days-to-weeks points mass or inflammatory.")
        if "seizure" in text or "convuls" in text or \
                any(c.condition_id == "first_seizure_adult"
                    for c in conditions):
            craft.append("First fit: driving law, ECG (QT and morphology), "
                         "glucose, and a witnessed account before any "
                         "label — the syndrome, not the seizure, is the "
                         "diagnosis.")

    elif role_key == "paediatrician":
        if not (_child_in_case(text, ctx)
                or conditions):
            return []
        craft.append("Weight in kilograms today: paediatric dosing is "
                     "weight-based, never a fraction of an adult dose — "
                     "and defibrillation/drug doses come off the tape, "
                     "not memory.")
        craft.append("Children compensate then crash: a quiet child is a "
                     "worrying child — reassess, and never discharge on "
                     "the observation you made an hour ago.")

    elif role_key == "psychiatrist":
        if not (conditions or any(h in text for h in _PSYCHIATRY_HINTS)):
            return []
        cond_ids = {c.condition_id for c in conditions}
        # command hallucinations ("voices telling him to hurt himself")
        # are a risk context even without the word suicidal
        if "suicide_risk" in cond_ids or any(
                h in text for h in ("suicidal", "self-harm", "self harm",
                                    "wants to die", "kill myself",
                                    "voices telling", "hurt himself",
                                    "hurt herself", "harm himself",
                                    "harm herself")):
            craft.append("Risk in structure, not adjectives: means, plan, "
                         "intent, timeframe — each asked directly and each "
                         "written down.")
        if "psychosis_first_episode" in cond_ids or any(
                h in text for h in ("voices", "psychosis", "delusion",
                                    "paranoid", "mania")):
            craft.append("Exclude delirium before any new psychiatric "
                         "label: acute onset, fluctuating course, visual "
                         "hallucinations, inattention — a first psychosis "
                         "at 70 with fever is a medical admission.")

    return _corpus_notes(conditions) + craft


def _oncologist_notes(presentation: str, ctx: dict,
                      differential) -> List[str]:
    """The oncologist: referral thresholds from the 2ww rules, plus the
    time-critical complications carried in the corpus."""
    from gpdisc_core.uk_practice import two_week_wait_check
    conditions = _domain_conditions(differential, _ONCOLOGY_CATEGORIES)
    hits = two_week_wait_check(presentation,
                               age=ctx.get("age_years"),
                               sex=ctx.get("sex"))
    if not (conditions or hits or any(
            h in presentation.lower() for h in _ONCOLOGY_HINTS)):
        return []
    notes: List[str] = []
    for r in hits[:2]:
        notes.append(f"2ww ({r.cancer_site}): {r.action}.")
    if conditions:
        for c in conditions[:2]:
            red = "; ".join(c.red_flags[:2]) if c.red_flags else ""
            line = f"{c.name} is the oncological emergency to hold in mind"
            line += f" — {red}." if red else "."
            notes.append(line)
    notes.append("Refer at the threshold, not beyond it: a 2ww referral "
                 "needs the discriminating features, baseline bloods and "
                 "fitness stated up front — a referral made late is the "
                 "only unrecoverable oncology error.")
    return notes


def _palliative_notes(presentation: str, ctx: dict) -> List[str]:
    """The palliative physician: reversibility, the frames from the
    palliative module, anticipatory prescribing."""
    text = presentation.lower()
    if not (any(h in text for h in _PALLIATIVE_HINTS)
            or ctx.get("palliative")):
        return []
    notes: List[str] = []
    try:
        from gpdisc_core.palliative_care import eol_guidance_for
        g = eol_guidance_for(presentation)
        if g and g.get("assess"):
            notes.append(f"{g['title']}: assess first — "
                         + " ".join(g["assess"][:2]))
    except Exception:
        pass
    notes.append("Run the reversibility check once: which of today's "
                 "problems would we still treat if this were the last "
                 "week — and write the answer down.")
    notes.append("Anticipatory medications prescribed BEFORE they are "
                 "needed (confirm doses against the local formulary); "
                 "an expected death at home is not a 999 call.")
    return notes
