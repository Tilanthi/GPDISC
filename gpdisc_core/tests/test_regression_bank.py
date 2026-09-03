"""The dangerous-mimic regression bank — diagnostic reasoning as curriculum.

Stage 5, Task 3. Every case runs through the live ConsultationPipeline;
expectations are clinical ground truth. Where an expectation and the
engine disagree, the disagreement is resolved by clinical judgement —
never by silently weakening the expectation.
"""
import pytest
from gpdisc_core.tests.regression_bank import BANK
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline


class TestRegressionBank:
    pipe = ConsultationPipeline()

    def test_bank_has_40_cases(self):
        # 40 locked (Stage 5) + 5 trauma/burns (6.3) + 4 tox (6.4)
        # + 4 obstetric (6.5) + 4 onc/derm (6.6) + 3 paediatric (6.7)
        # + 2 PEP (6.8) + 3 chronic neuro/MH (7.1)
        # + 3 women's/men's health (7.2)
        # + 3 chronic GI/eyes/sleep (7.3)
        # + 4 the world (8.1: heat stroke, HACE, sickle, leprosy)
        assert len(BANK) == 75
        for entry in BANK:
            assert entry["case"] and entry["leader_or_retained"]

    def test_every_case_produces_a_record(self):
        for entry in BANK:
            rec = self.pipe.run(entry["case"], {})
            assert rec.presenting_complaint or rec.problem_representation

    def test_escalations_hold(self):
        checked = 0
        for entry in BANK:
            if entry.get("escalation") is None:
                continue
            rec = self.pipe.run(entry["case"], {})
            assert rec.escalation == entry["escalation"], (
                entry["case"], rec.escalation)
            checked += 1
        assert checked >= 24  # most of the bank pins escalation

    def test_leaders_or_retained_present(self):
        for entry in BANK:
            rec = self.pipe.run(entry["case"], {})
            ids = ({d["condition_id"] for d in rec.ranked_differential}
                   | {d["condition_id"] for d in rec.dangerous_alternatives}
                   | {d["condition_id"] for d in rec.syndrome_differentials})
            assert ids & set(entry["leader_or_retained"]), (
                entry["case"], sorted(ids))

    def test_syndromes_hold(self):
        checked = 0
        for entry in BANK:
            if not entry.get("syndrome"):
                continue
            rec = self.pipe.run(entry["case"], {})
            assert rec.syndrome == entry["syndrome"], entry["case"]
            checked += 1
        assert checked >= 3
