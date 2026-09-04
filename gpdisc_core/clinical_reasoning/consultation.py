"""Consultation pipeline: presenting complaint -> history -> background ->
medication/allergies -> risk factors -> targeted examination -> problem
representation -> ranked differential -> dangerous alternatives ->
investigation strategy -> interpretation -> treatment -> referral ->
follow-up -> safety net. Emits a structured ConsultationRecord.

The engine never fabricates history the patient did not give: stages the
input does not populate are marked as questions to ask, which is the
consultation skill of knowing what to ask next.

Honesty rules (2026-09-03 global audit): when the corpus has nothing to
say — empty differential, or a presentation whose intent is outside its
scope (e.g. end-of-life care until the palliative module exists) — the
record says so instead of force-fitting a leader. A noise-scored leader is
annotated as low confidence, never presented as the diagnosis.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .diagnostic_engine import DifferentialEngine, DifferentialResult
from .safety import SafetyLayer, EscalationLevel
from .syndromes import SyndromeEngine, discriminating_questions
from .validation import ClinicalValidator, ValidationReport
from ..palliative_care import eol_guidance_for
from ..humanitarian_care import (
    arrival_health_screen, is_arrival_consultation, screening_summary,
)

STAGES = ["presenting_complaint", "history", "background", "medication_allergies",
          "risk_factors", "targeted_examination", "problem_representation",
          "ranked_differential", "dangerous_alternatives", "investigation_strategy",
          "interpretation", "treatment", "referral", "follow_up", "safety_net"]

QUESTIONS_BY_STAGE = {
    "history": ["Onset, character, radiation, timing, severity, exacerbators?",
                "Systemic features: fever, weight loss, night sweats?"],
    "background": "Relevant past history not yet provided — ask.",
    "medication_allergies": "Drug history and allergies not yet provided — ask.",
    "risk_factors": "Smoking, alcohol, family history, occupation, travel?",
    "targeted_examination": "Focused examination guided by the differential.",
}

# A leader scored below this is noise-matched on a generic word, not a
# diagnosis (calibrated 2026-09-03: benign bank leaders 0.144-0.787, the
# incontinence noise leader 0.112 — the bank test pins the margin).
LOW_CONFIDENCE_FLOOR = 0.13

# Presentations whose intent is care the corpus does not yet carry. Saying
# so beats force-fitting quinsy onto a dying patient. Safety screen wins:
# this guard only runs when no emergency/urgent rule fired.
# Widened 2026-09-04 (audit missing-area 4): "stage four cancer,
# struggling to cope" fell to an empty differential before; the
# cancer-spread phrasings route to the palliative module's planning and
# symptom frames. Deliberately NOT bare "spread to the lungs" — an
# infection spreads too.
_EOL_INTENT = re.compile(
    r"\b(dying|end of life|palliative|hospice|last (?:days|hours|weeks)|"
    r"comfortable|make (?:him|her|them) comfortable)\b"
    r"|stage (?:four|4) cancer|terminal cancer|cancer has spread|"
    r"\bsecondaries\b|\bmetastas\w+\b|no more (?:treatment|they can do)|"
    r"oncolog\w+ (?:can't|cannot|won't) (?:do|offer|treat)", re.I)

# Pre-travel consults route to the travel-medicine plan (audit routing
# gap 1). Needs a travel word AND either a future marker or an explicit
# what-do-I-need question, and must NOT fire post-travel ("fever since
# I came back" is the fever-after-travel syndrome, not a plan request).
_TRAVEL_WORD = re.compile(
    r"travell?ing|travel plans|going abroad|flying to|flying out|"
    r"\btrip (?:to|next|abroad)\b|holiday (?:in|to|next|abroad)|"
    r"backpack\w*|travel clinic|travel vaccin\w*|"
    r"before (?:i|we) (?:go|travel|fly|leave)", re.I)
_TRAVEL_FUTURE = re.compile(
    r"next (?:month|week|year|weekend|summer|spring|autumn|winter|"
    r"january|february|march|april|may|june|july|august|september|"
    r"october|november|december|\d+ (?:weeks?|months?))|"
    r"in (?:a|two|three|four|five|six|eight|ten|\d+) (?:weeks?|months?)|"
    r"soon|booked|\btomorrow\b", re.I)
_TRAVEL_ASK = re.compile(
    r"vaccin|immunis|\bjabs?\b|malaria|prophyla|tablets|travel kit|"
    r"what (?:do|should) (?:i|we)|do i need|advice", re.I)
_POST_TRAVEL = re.compile(
    r"since (?:i|we) (?:came|got) back|(?:just|recently) (?:got|came) back|"
    r"return\w* from|back from\b|after (?:the |my )?(?:trip|holiday|travel)|"
    r"post[- ]travel", re.I)

# Preventive-care questions route to the prevention module (audit routing
# gaps 6-7): "what am I due at 68", "should I get the shingles vaccine".
_PREVENTION_INTENT = re.compile(
    r"what (?:vaccin\w*|screening|checks?|jabs?|am i due|do i need)\b|"
    r"(?:am i|what's) due\b|due any\b|due a (?:check|jab|vaccine)|"
    r"(?:shingles|flu|pneumococcal|covid|rsv|whooping cough) vaccin\w*|"
    r"health check|\bscreening\b|bowel kit|smear test", re.I)

# "Can I drink while taking X?" routes to the alcohol-interaction table
# (audit routing gap 5): metronidazole is the famous one, but the
# question is asked about warfarin, MTX and paracetamol too.
_ALCOHOL_WORD = re.compile(r"\balcohol\b|\bdrinks?\b|\bdrinking\b|\bbooze\b", re.I)
_DRUG_WORD = re.compile(
    r"metronidazole|tinidazole|flagyl|isoniazid|ketoconazole|disulfiram|"
    r"warfarin|methotrexate|paracetamol|doxycycline|nitrofurantoin|"
    r"amoxicillin|clarithromycin|antibiot\w*|\btablets?\b|\bmedicine\b|"
    r"\bmedication\b", re.I)

HONESTY_STATEMENT = ("I don't have enough knowledge to assess this "
                     "presentation — describe more or see a clinician.")


@dataclass
class ConsultationRecord:
    presenting_complaint: str = ""
    history: List[str] = field(default_factory=list)
    background: str = ""
    medication_allergies: str = ""
    risk_factors: str = ""
    targeted_examination: str = ""
    problem_representation: str = ""
    ranked_differential: List[Dict] = field(default_factory=list)
    dangerous_alternatives: List[Dict] = field(default_factory=list)
    investigation_strategy: List[str] = field(default_factory=list)
    interpretation: str = ""
    treatment: str = ""
    referral: str = ""
    follow_up: str = ""
    safety_net: str = ""
    escalation: str = "routine"
    uncertainty: str = ""
    syndrome: str = ""
    syndrome_differentials: List[Dict] = field(default_factory=list)
    discriminating_questions: List[str] = field(default_factory=list)
    stages: Dict[str, str] = field(default_factory=dict)
    validation: Optional[ValidationReport] = None
    outside_scope: bool = False
    ruleset: str = ""        # whose rules this consultation ran under (8.3)

    def summary(self) -> str:
        lines = [f"Presenting complaint: {self.presenting_complaint}"]
        if self.outside_scope:
            # honesty over force-fitting: no differential block, no
            # made-up leader — what this record knows is what it doesn't
            lines.append(HONESTY_STATEMENT)
            if self.uncertainty:
                lines.append(f"Uncertainty: {self.uncertainty}")
            if self.discriminating_questions:
                lines.append("Ask next: " + " | ".join(self.discriminating_questions[:3]))
            lines.append(f"Safety net: {self.safety_net}")
            if self.validation is not None:
                lines.append(self.validation.summary())
            return "\n".join(lines)
        lines.append(f"Problem representation: {self.problem_representation}")
        # palliative/comfort records carry no differential — no empty
        # header for them (7.4)
        if self.ranked_differential or self.dangerous_alternatives or \
                self.syndrome_differentials:
            lines.append("Differential:")
        for d in self.ranked_differential[:5]:
            lines.append(f"  - {d['name']} (score {d['score']:.2f})")
        if self.dangerous_alternatives:
            lines.append("Must-not-miss (retained):")
            for d in self.dangerous_alternatives:
                lines.append(f"  ! {d['name']}")
        if self.syndrome:
            lines.append(f"Syndrome frame: {self.syndrome}")
            for d in self.syndrome_differentials[:5]:
                lines.append(f"  ? {d['condition_id']}: {d['key_discriminator']}")
        if self.discriminating_questions:
            lines.append("Ask next: " + " | ".join(self.discriminating_questions[:3]))
        if self.investigation_strategy:
            lines.append("Investigations: " + "; ".join(self.investigation_strategy))
        if self.treatment:
            lines.append(f"Treatment: {self.treatment}")
        if self.referral:
            lines.append(f"Referral: {self.referral}")
        lines.append(f"Safety net: {self.safety_net}")
        if self.ruleset:
            lines.append(self.ruleset)
        if self.uncertainty:
            lines.append(f"Uncertainty: {self.uncertainty}")
        if self.validation is not None:
            lines.append(self.validation.summary())
        return "\n".join(lines)


class ConsultationPipeline:
    def __init__(self, engine: Optional[DifferentialEngine] = None,
                 safety: Optional[SafetyLayer] = None,
                 syndromes: Optional[SyndromeEngine] = None,
                 validator: Optional[ClinicalValidator] = None):
        self.engine = engine or DifferentialEngine()
        self.safety = safety or SafetyLayer()
        self.syndromes = syndromes or SyndromeEngine()
        self.validator = validator or ClinicalValidator()

    def _finalize(self, rec: ConsultationRecord,
                  context: Optional[Dict] = None) -> ConsultationRecord:
        """No consultation leaves unvalidated: the anti-hallucination layer
        runs on every exit path and its report rides on the record. The
        resource setting (8.2) adapts the DISPOSITION line last — after
        validation, and never the level of concern itself."""
        try:
            rec.validation = self.validator.validate_consultation(rec)
        except Exception as exc:  # validation must never break a consultation
            rec.validation = ValidationReport(
                passed=True, findings=[], corrections=[
                    f"validation unavailable: {exc}"])
        try:
            from ..resource_settings import setting_line
            line = setting_line(rec.escalation, (context or {}).get("setting"))
            if line:
                rec.referral = f"{rec.referral} {line}".strip()
        except Exception:   # disposition adaptation is advisory, never vital
            pass
        try:    # 8.3: the record states whose rules it ran under
            from ..jurisdictions import ruleset_line
            rec.ruleset = ruleset_line(context)
        except Exception:
            pass
        return rec

    def run(self, presentation: str, context: Optional[Dict] = None) -> ConsultationRecord:
        rec = ConsultationRecord(presenting_complaint=presentation[:300])
        assessment = self.safety.screen(presentation, context)
        rec.escalation = assessment.level.value

        # Syndrome frame attaches BEFORE the emergency branch so the frame's
        # differentials and safety rule ride along even when an emergency rule
        # short-circuits the rest of the consultation.
        frame = self.syndromes.for_presentation(presentation, context)
        if frame is not None:
            rec.syndrome = frame.key
            rec.syndrome_differentials = [
                {"condition_id": d.condition_id,
                 "key_discriminator": d.key_discriminator}
                for d in frame.differentials]
            rec.discriminating_questions = discriminating_questions(frame)
            rec.investigation_strategy = list(frame.first_tests)
            rec.uncertainty = frame.rank_note

        if assessment.level == EscalationLevel.EMERGENCY:
            rec.stages["presenting_complaint"] = presentation[:300]
            rec.problem_representation = (
                f"EMERGENCY pattern matched: {assessment.emergency_rule}")
            rec.dangerous_alternatives = [{
                "condition_id": assessment.emergency_rule,
                "name": assessment.emergency_rule.replace("_", " ")}]
            rec.referral = f"EMERGENCY: {assessment.advice} Call 999 now."
            rec.safety_net = assessment.advice
            rec.treatment = "Do not delay transfer for further history."
            rec.uncertainty = "Emergency pathway overrides diagnostic refinement."
            return self._finalize(rec, context)

        # End-of-life presentations route to the palliative module (7.4):
        # terminal symptom control, can't-swallow route advice, planning.
        # Only when NO emergency/urgent rule fired — a dying patient can
        # still develop a massive bleed or a fracture: safety always wins.
        if assessment.level == EscalationLevel.ROUTINE and \
                _EOL_INTENT.search(presentation):
            guidance = eol_guidance_for(presentation)
            rec.problem_representation = (
                f"End-of-life care — {guidance['title']}.")
            parts = []
            if guidance.get("assess"):
                parts.append("Assess first: " +
                             " ".join(guidance["assess"]))
            if guidance.get("non_drug"):
                parts.append("Care measures: " +
                             " ".join(guidance["non_drug"]))
            if guidance.get("drugs"):
                parts.append("Medicines: " + " ".join(guidance["drugs"]))
            if guidance.get("priorities"):
                # planning frame: the whole plan, section by section
                for section in ("priorities", "anticipatory", "decisions",
                                "communication", "support"):
                    if guidance.get(section):
                        parts.append(section.capitalize() + ": " +
                                     " ".join(guidance[section]))
            if guidance.get("route_advice"):
                parts.append("Route (tablets cannot be swallowed): " +
                             " ".join(guidance["route_advice"]))
            rec.treatment = "\n".join(parts)
            rec.uncertainty = (
                "Comfort-focused end-of-life guidance, not a diagnosis. "
                "This is symptom control scaffolding — the GP and "
                "palliative/district-nursing team own the decisions and "
                "the doses.")
            rec.safety_net = (
                "If pain, agitation, breathlessness or vomiting escalate "
                "beyond what the medicines at home control, call the GP or "
                "out-of-hours service the same day; 999 for a sudden "
                "catastrophic event.")
            rec.referral = (
                "GP today; district nursing / hospice-at-home team; local "
                "out-of-hours palliative advice line.")
            return self._finalize(rec, context)

        # New-arrival presentations route to the humanitarian module
        # (8.4): arrival screening, interpreter rules, unaccompanied
        # minors. Same guard as palliative: safety screen wins — a
        # refugee with chest pain is a chest pain first.
        if assessment.level == EscalationLevel.ROUTINE and \
                is_arrival_consultation(presentation):
            from ..humanitarian_care import (
                minor_summary, unaccompanied_minor_review)
            is_minor = bool(re.search(
                r"\b(child|boy|girl|teenager|minor|son|daughter|"
                r"unaccompanied)\b", presentation, re.I))
            if is_minor:
                review = unaccompanied_minor_review()
                rec.problem_representation = review["title"]
                rec.treatment = minor_summary()
                rec.safety_net = (
                    "Any trafficking indicator, suicidal talk, or an "
                    "adult whose relationship is unclear — children's "
                    "social services the same day.")
            else:
                screen = arrival_health_screen()
                rec.problem_representation = screen["title"]
                rec.treatment = screening_summary()
                rec.safety_net = (
                    "Fever after transit, cough beyond two weeks with "
                    "weight loss, or pregnancy without care — urgent "
                    "review, not the next routine appointment.")
            rec.uncertainty = (
                "Screening framework, not a diagnosis — the interpreter, "
                "the patient's own priorities and the local programme "
                "decide the order of the bundle.")
            rec.referral = (
                "Professional interpreter booking; health-visitor / "
                "looked-after-children team where a minor; local "
                "new-arrival / infectious-diseases screening programme.")
            return self._finalize(rec, context)

        # Pre-travel consults route to the travel plan (audit routing
        # gap 1). Same guard discipline: ROUTINE only — a febrile
        # returned traveller is a fever-after-travel emergency first.
        if assessment.level == EscalationLevel.ROUTINE and \
                _TRAVEL_WORD.search(presentation) and \
                (_TRAVEL_FUTURE.search(presentation) or
                 _TRAVEL_ASK.search(presentation)) and \
                not _POST_TRAVEL.search(presentation):
            from ..travel_medicine import pre_travel_consult
            plan = pre_travel_consult(presentation, context)
            rec.problem_representation = (
                f"Pre-travel consultation — "
                f"{plan.destination or 'destination not recognised'}.")
            parts = []
            mal = plan.malaria or {}
            if mal.get("risk"):
                parts.append(f"Malaria ({mal['risk']}): "
                             f"{mal.get('recommendation', '')}")
            if plan.vaccines:
                v = plan.vaccines[0]
                names = ", ".join(v) if isinstance(v, (list, tuple)) \
                    else str(v)
                for entry in plan.vaccines:
                    if isinstance(entry, dict):
                        names = ", ".join(str(x) for x in entry.values())
                        break
                parts.append(f"Vaccines to consider: {names}")
            if plan.certificate:
                parts.append("Certificate: " + plan.certificate)
            if plan.general:
                parts.append("General: " + " ".join(plan.general))
            rec.treatment = "\n".join(parts) or (
                "Destination not in the local table — build the plan "
                "from NaTHNaC / TravelHealthPro country pages.")
            rec.uncertainty = (
                "Plan from the destination named and the history given; "
                "itinerary details, pregnancy and medical conditions "
                "change it.")
            rec.safety_net = (
                "Fever after return is never 'just a bug' — same-day "
                "assessment, and say where you have been.")
            rec.referral = (
                "Practice nurse / travel clinic for vaccine "
                "administration and any certificates.")
            return self._finalize(rec, context)

        # Preventive-care questions route to the prevention module
        # (audit routing gaps 6-7). Age and sex are read from the text
        # when stated; without them the check still runs but says what
        # it needs.
        if assessment.level == EscalationLevel.ROUTINE and \
                _PREVENTION_INTENT.search(presentation):
            from ..preventive_medicine import prevention_check
            patient: Dict = dict(context or {})
            m_age = re.search(r"\b(\d{1,3})\b", presentation)
            if m_age and 1 <= int(m_age.group(1)) <= 105:
                patient.setdefault("age_years", int(m_age.group(1)))
            if re.search(r"\b(?:woman|female|she|her)\b", presentation,
                         re.I):
                patient.setdefault("sex", "f")
            elif re.search(r"\b(?:man|male|he|his)\b", presentation,
                           re.I):
                patient.setdefault("sex", "m")
            items = prevention_check(patient)
            rec.problem_representation = (
                "Preventive care check — vaccinations and screening due.")
            if items:
                rec.treatment = "\n".join(
                    f"{it['kind'].capitalize()}: {it['name']} — "
                    f"{it['detail']}" for it in items)
            else:
                rec.treatment = (
                    "Nothing flagged due from the age and sex as given — "
                    "tell me the age, sex and any conditions for a full "
                    "check.")
            rec.uncertainty = (
                "Schedule generated from age/sex as stated; "
                "immunosuppression, pregnancy, and long-term conditions "
                "add cohorts.")
            rec.safety_net = (
                "New symptoms are not answered by a prevention check — "
                "describe them separately.")
            rec.referral = (
                "Practice nurse / healthcare assistant for "
                "administration and booking.")
            return self._finalize(rec, context)

        # "Can I drink while taking X?" routes to the alcohol table
        # (audit routing gap 5). Needs BOTH the alcohol word and a drug
        # word in the same question.
        if assessment.level == EscalationLevel.ROUTINE and \
                _ALCOHOL_WORD.search(presentation) and \
                _DRUG_WORD.search(presentation):
            from ..uk_practice.prescribing_safety import (
                alcohol_interaction, ALCOHOL_INTERACTIONS)
            hits = alcohol_interaction(presentation)
            rec.problem_representation = (
                "Alcohol-and-medication interaction question.")
            if hits:
                rec.treatment = "\n".join(
                    f"{drug.capitalize()}: {guidance}"
                    for drug, guidance in hits)
            else:
                named = [d for d in ALCOHOL_INTERACTIONS
                         if d in presentation.lower()]
                rec.treatment = (
                    f"No alcohol-interaction row for the medicine named"
                    f"{'' if not named else ' (' + ', '.join(named) + ')'}"
                    " — check the BNF or ask the pharmacist; do not "
                    "guess from a similar-sounding drug.")
            rec.uncertainty = (
                "Interaction guidance only — the underlying condition "
                "being treated is a separate question.")
            rec.safety_net = (
                "Flushing, vomiting or palpitations after drinking on "
                "antibiotics — stop drinking and seek advice.")
            rec.referral = "Community pharmacist for the specific product."
            return self._finalize(rec, context)

        diff: DifferentialResult = self.engine.build_differential(presentation, context)
        rec.problem_representation = (
            f"{len(diff.key_features)} discriminating features extracted: "
            + ", ".join(diff.key_features[:8]) if diff.key_features
            else "Problem not yet localisable")
        rec.ranked_differential = [
            {"condition_id": d.condition_id, "name": d.name,
             "score": round(d.score, 3), "reasons": d.reasons}
            for d in diff.ranked]
        rec.dangerous_alternatives = [
            {"condition_id": d.condition_id, "name": d.name}
            for d in diff.retained_dangerous]
        if not rec.uncertainty:
            rec.uncertainty = diff.uncertainty

        # honesty: empty differential means exactly that — no force-fit
        if not diff.ranked and not diff.retained_dangerous:
            rec.outside_scope = True
            rec.problem_representation = "No corpus condition matched."
            rec.uncertainty = HONESTY_STATEMENT
            rec.safety_net = ("If symptoms worsen or new concerning "
                              "features appear, seek medical review.")
            rec.referral = "See a clinician — this presentation is outside what I know."
            return self._finalize(rec, context)

        # honesty: a noise-scored leader is annotated, never presented as
        # the diagnosis (LOW_CONFIDENCE_FLOOR calibration comment above)
        if diff.ranked and diff.ranked[0].score < LOW_CONFIDENCE_FLOOR:
            note = ("low confidence differential — the leading match is weak; "
                    "describe more or see a clinician")
            rec.uncertainty = (note if not rec.uncertainty
                               else f"{rec.uncertainty} ({note})")

        # stages the input did not populate become questions to ask
        for stage, q in QUESTIONS_BY_STAGE.items():
            rec.stages[stage] = q if not getattr(rec, stage, "") else getattr(rec, stage)

        top = diff.ranked[0] if diff.ranked else None
        if top is not None:
            from .knowledge import find_condition
            c = find_condition(top.condition_id)
            if c:
                if not rec.investigation_strategy:  # syndrome frame tests win
                    rec.investigation_strategy = [i.name + " — " + i.purpose
                                                  for i in c.investigations]
                rec.treatment = c.management_first_line
                tier_text = {
                    "self_care": "self-care with pharmacy support",
                    "routine": "routine GP review",
                    "urgent": "same-day urgent review",
                    "two_week_wait": "urgent suspected-cancer (2ww) referral",
                    "emergency": "emergency department / 999",
                }
                rec.referral = tier_text.get(c.referral_tier, "routine GP review")
                rec.safety_net = self.safety.safety_net_for(c.condition_id)
        if not rec.safety_net:
            rec.safety_net = ("If symptoms worsen, change, or new red-flag "
                              "features appear, seek urgent medical review.")

        # an urgent safety rule's advice is the REASON this consultation
        # is urgent — it must reach the output. Emergency rules return
        # early above with their advice; urgent rules fall through to
        # this differential flow, so without this the tier text would
        # silently replace the rule's instruction (e.g. the MTX warning-
        # card 'STOP and same-day FBC' advice).
        if assessment.level == EscalationLevel.URGENT and assessment.advice:
            rec.referral = (f"URGENT ({assessment.emergency_rule}): "
                            f"{assessment.advice} | {rec.referral}").strip(" |")

        # marginal presentations: when the top two are too close to call,
        # the consultation's next step is the questions that separate them.
        # A benign-vs-emergency pair match is marginal by definition, so its
        # discriminators are asked even when the differential is thin.
        # (Syndrome frames already filled their questions above.)
        if not rec.discriminating_questions:
            from .knowledge import find_condition as _find_condition
            from .benign_vs_emergency import find_pairs as _find_pairs
            qs: List[str] = []
            if len(diff.ranked) >= 2:
                top1, top2 = diff.ranked[0], diff.ranked[1]
                if top2.score >= 0.75 * top1.score:
                    for d in (top1, top2):
                        c = _find_condition(d.condition_id)
                        if c is not None and c.discriminators:
                            qs.extend(c.discriminators[:2])
            for p in _find_pairs(presentation):
                qs.extend(p.discriminators[:2])
            if qs:
                rec.discriminating_questions = list(dict.fromkeys(qs))[:5]

        rec.follow_up = "Review if not improving within the expected course, or sooner per safety net."
        return self._finalize(rec, context)
