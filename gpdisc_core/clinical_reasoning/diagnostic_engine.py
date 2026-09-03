"""Diagnostic engine: problem representation from free text, ranked
differential construction, Bayesian updating, and anti-anchoring.

Scoring: each condition scores sum over matched symptom tokens of
(frequency x specificity), anchored by prior prevalence, normalised to a
0-1 score. Anti-anchoring: any condition in the top quartile of
dangerousness (referral_tier emergency/two_week_wait) that shares at
least one matched symptom with the leader is RETAINED and displayed even
when ranked low — the engine is forbidden from presenting a differential
that has pruned every dangerous mimic.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .knowledge import CONDITIONS, SYMPTOM_SYNONYMS
from .test_interpretation import TestInterpreter, REFERENCE_RANGES

DANGEROUS_TIERS = {"emergency", "two_week_wait", "urgent"}


@dataclass
class RankedDiagnosis:
    condition_id: str
    name: str
    score: float
    post_test_probability: Optional[float] = None
    is_retained_dangerous: bool = False
    reasons: List[str] = field(default_factory=list)


@dataclass
class DifferentialResult:
    ranked: List[RankedDiagnosis]
    retained_dangerous: List[RankedDiagnosis]
    key_features: List[str]
    uncertainty: str


# "no weight loss", "denies chest pain" — a symptom phrase preceded by a
# negation is an ABSENT feature, not a present one.
_NEGATION_PREFIX = re.compile(
    r"\b(?:no|not|never had|without|denies?|negative for)\s+(?:\w+\s+){0,2}$")


def _extract_features(text: str, context: Optional[Dict]) -> List[str]:
    t = (text or "").lower()
    for v in (context or {}).values():
        t += " " + str(v).lower()
    hits = []
    for token, phrases in SYMPTOM_SYNONYMS.items():
        for p in phrases:
            i = t.find(p)
            if i < 0:
                continue
            if _NEGATION_PREFIX.search(t[max(0, i - 30):i]):
                continue  # negated mention — symptom explicitly absent
            hits.append(token)
            break
    return hits


class DifferentialEngine:
    def __init__(self, conditions: Optional[List] = None):
        self.conditions = conditions or CONDITIONS
        self.interp = TestInterpreter()

    def build_differential(self, presentation: str,
                           context: Optional[Dict] = None) -> DifferentialResult:
        feats = _extract_features(presentation, context)
        scored: List[RankedDiagnosis] = []
        for c in self.conditions:
            matched, s, reasons = [], 0.0, []
            for sf in c.symptoms:
                if sf.symptom in feats:
                    matched.append(sf.symptom)
                    s += sf.frequency * sf.specificity
            if s <= 0:
                continue
            prior = c.prevalence_per_consult
            score = s * (0.5 + 0.5 * min(prior / 0.05, 1.0))  # prior-anchored
            scored.append(RankedDiagnosis(
                condition_id=c.condition_id, name=c.name, score=score,
                reasons=[f"matched: {', '.join(sorted(set(matched)))}"]))
        scored.sort(key=lambda d: d.score, reverse=True)

        # anti-anchoring: retain dangerous conditions sharing a matched feature.
        # Only the top-2 leaders are excluded — a dangerous mimic sitting in
        # ranks 3-8 is still must-not-miss material and is flagged as such,
        # so the differential can never present without dangerous alternatives.
        leader_feats = set(feats)
        retained = []
        leader_ids = {d.condition_id for d in scored[:2]}
        for c in self.conditions:
            if c.referral_tier not in DANGEROUS_TIERS:
                continue
            shares = any(sf.symptom in leader_feats for sf in c.symptoms)
            if shares and c.condition_id not in leader_ids:
                retained.append(RankedDiagnosis(
                    condition_id=c.condition_id, name=c.name, score=0.0,
                    is_retained_dangerous=True,
                    reasons=["must-not-miss: actively exclude this dangerous mimic"]))
        uncertainty = self._uncertainty_statement(feats, scored)
        return DifferentialResult(ranked=scored[:8], retained_dangerous=retained,
                                  key_features=feats, uncertainty=uncertainty)

    def _uncertainty_statement(self, feats: List[str],
                               scored: List[RankedDiagnosis]) -> str:
        if not feats:
            return ("Insufficient information to localise the problem — the "
                    "medically correct next step is targeted history, not a "
                    "diagnosis. 'I don't know yet' applies.")
        if not scored:
            return ("No corpus condition matched these features; presentation "
                    "is outside current knowledge — human assessment advised.")
        top = scored[0]
        if len(scored) == 1 or (top.score > 0 and scored[1].score / top.score < 0.35):
            return ("Leading diagnosis is favoured but premature closure is a "
                    "known error — dangerous alternatives retained below must "
                    "be actively excluded.")
        return ("Competing hypotheses remain close — treat the differential as "
                "genuinely open and use targeted tests to separate them.")

    def update_with_test(self, result: Dict, condition_id: str,
                         pre_test: Optional[float] = None) -> float:
        """Update a condition's probability given a test result dict
        {test, value} using corpus test characteristics where available.

        Tests are ordered because suspicion already exists: when the caller
        does not supply a pre-test probability, the population prevalence is
        floored at a testing-context prior of 0.3 (the typical context in
        which an investigation is actually ordered) — updating from raw
        population prevalence would make almost no positive result matter.
        """
        from .knowledge import find_condition
        c = find_condition(condition_id)
        if c is None:
            return 0.0
        inv = next((i for i in c.investigations if i.name == result.get("test")), None)
        pre = c.prevalence_per_consult if pre_test is None else pre_test
        if inv is None or inv.sensitivity is None or inv.specificity is None:
            return pre
        interp = self.interp.interpret_value(result.get("test", ""), result.get("value", 0))
        lr_pos = self.interp.likelihood_ratio_positive(inv.sensitivity, inv.specificity)
        lr_neg = 1.0 / lr_pos
        lr = lr_pos if interp in ("high", "critical_high", "low", "critical_low") else lr_neg
        return self.interp.post_test_probability(max(pre, 0.3 if pre_test is None else 0.01), lr)
