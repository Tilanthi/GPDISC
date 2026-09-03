"""Bayesian test interpretation: reference ranges, predictive values,
likelihood-ratio arithmetic, and treat/test threshold logic.

Threshold framework follows the classic treat-test/threshold-only-test
model (Djulbegovic & Heng 2007, 'Modern research methodologies').
"""
from typing import Dict, Optional, Tuple

# (low, high, critical_low, critical_high, unit) — adult ambulatory values;
# paediatric ranges differ and are deliberately NOT guessed here.
REFERENCE_RANGES: Dict[str, Tuple[float, float, Optional[float], Optional[float], str]] = {
    "potassium":      (3.5, 5.1, 2.8, 6.0, "mmol/L"),
    "sodium":         (133, 146, 120, 155, "mmol/L"),
    "creatinine":     (60, 110, None, 350, "umol/L"),
    "haemoglobin":    (115, 165, 70, None, "g/L"),
    "crp":            (0.0, 5.0, None, 350, "mg/L"),
    "white_cell":     (4.0, 11.0, 1.5, 25.0, "x10^9/L"),
    "platelets":      (150, 400, 50, 800, "x10^9/L"),
    "glucose_random": (4.0, 7.8, 2.5, 20.0, "mmol/L"),
    "hba1c":          (0.0, 41.0, None, 75.0, "mmol/mol"),
    "tsh":            (0.4, 4.0, 0.01, 20.0, "mU/L"),
    "calcium":        (2.20, 2.60, 1.90, 3.00, "mmol/L"),
    "troponin_hs":    (0.0, 14.0, None, 50.0, "ng/L"),
}


class TestInterpreter:
    def interpret_value(self, analyte: str, value: float) -> str:
        r = REFERENCE_RANGES.get(analyte)
        if r is None:
            return "unknown_analyte"
        low, high, crit_low, crit_high, _unit = r
        # Critical bounds are strict: the boundary value itself is flagged
        # low/high (abnormal) rather than critical.
        if crit_low is not None and value < crit_low:
            return "critical_low"
        if crit_high is not None and value > crit_high:
            return "critical_high"
        if value < low:
            return "low"
        if value > high:
            return "high"
        return "normal"

    def predictive_values(self, sens: float, spec: float,
                          prevalence: float) -> Tuple[float, float]:
        tp = sens * prevalence
        fp = (1 - spec) * (1 - prevalence)
        ppv = tp / (tp + fp) if (tp + fp) else 0.0
        fn = (1 - sens) * prevalence
        tn = spec * (1 - prevalence)
        npv = tn / (tn + fn) if (tn + fn) else 0.0
        return ppv, npv

    def likelihood_ratio_positive(self, sens: float, spec: float) -> float:
        return sens / (1 - spec)

    def post_test_probability(self, pre_test: float, lr: float) -> float:
        pre_odds = pre_test / (1 - pre_test) if 0 < pre_test < 1 else pre_test
        post_odds = pre_odds * lr
        return post_odds / (1 + post_odds)

    def should_investigate(self, pre_test: float, sensitivity: float,
                           specificity: float, test_threshold: float,
                           treatment_threshold: float) -> str:
        post_pos = self.post_test_probability(
            pre_test, self.likelihood_ratio_positive(sensitivity, specificity))
        post_neg = self.post_test_probability(pre_test, 1.0 / max(
            self.likelihood_ratio_positive(sensitivity, specificity), 1e-9))
        if post_pos >= treatment_threshold:
            return "test"
        if post_neg > test_threshold:
            return "test"          # negative result still matters
        if post_pos <= test_threshold and post_neg <= test_threshold:
            return "no_value"
        return "test"
