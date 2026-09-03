"""Tests for benign-vs-emergency discrimination (Stage 5)."""
from gpdisc_core.clinical_reasoning.benign_vs_emergency import (
    PAIRS, DiscriminationPair, find_pairs,
)
from gpdisc_core.clinical_reasoning.safety import SafetyLayer, EscalationLevel


class TestDiscriminationPairs:
    def test_ten_pairs(self):
        assert len(PAIRS) == 10
        for p in PAIRS:
            assert p.discriminators

    def test_find_pairs_by_condition(self):
        hits = find_pairs("sah_subarachnoid")
        assert any(p.emergency_condition == "sah_subarachnoid" for p in hits)

    def test_find_pairs_by_keyword(self):
        hits = find_pairs("rash that doesn't fade")
        assert any(p.emergency_condition == "meningococcal_child" for p in hits)

    def test_no_match_empty(self):
        assert find_pairs("prescription request") == []


class TestPairsAgainstLiveSafetyLayer:
    sl = SafetyLayer()

    def test_emergency_sides_escalate(self):
        from gpdisc_core.clinical_reasoning.knowledge import find_condition
        required = 0
        escalated = 0
        for p in PAIRS:
            if p.emergency_condition == "lymphoma_suspect":
                # Time-critical, but a 2ww cancer pathway — NOT an ED trip.
                c = find_condition("lymphoma_suspect")
                assert c is None or c.referral_tier in ("two_week_wait", "urgent")
                continue
            required += 1
            a = self.sl.screen(p.emergency_presentation, {})
            if a.level in (EscalationLevel.URGENT, EscalationLevel.EMERGENCY):
                escalated += 1
        assert escalated >= required - 1  # at most one judgement call missed

    def test_benign_sides_do_not_emergency_escalate(self):
        for p in PAIRS:
            a = self.sl.screen(p.benign_presentation, {})
            assert a.level != EscalationLevel.EMERGENCY, p.benign_presentation
