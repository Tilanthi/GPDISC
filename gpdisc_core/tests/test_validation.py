"""Tests for the clinical validator — GPDISC's anti-hallucination layer.

Two kinds of verification:
1. consult-level: the diagnostic record must be internally consistent
   (escalation agrees with the differential it came from, retained
   killers are not silently dropped, safety-net present, safeguarding
   signals surfaced).
2. claim-level: free-text clinical claims must be grounded in the
   knowledge base (drug/renal, monitoring, guideline citations) or
   corrected from the persistent hallucination register.
"""
import pytest
from gpdisc_core.clinical_reasoning.consultation import ConsultationRecord
from gpdisc_core.clinical_reasoning.validation import (
    ClinicalValidator, ValidationReport, ValidationFinding,
)


@pytest.fixture()
def validator(tmp_path):
    return ClinicalValidator(register_path=tmp_path / "register.json")


def _record(**kw) -> ConsultationRecord:
    base = dict(presenting_complaint="test presentation",
                safety_net="Return if worse.",
                escalation="routine")
    base.update(kw)
    return ConsultationRecord(**base)


class TestEscalationConsistency:
    def test_emergency_leader_blocks_routine_label(self, validator):
        rec = _record(
            ranked_differential=[
                {"condition_id": "acs_stemi", "name": "STEMI", "score": 2.0,
                 "reasons": []}],
            safety_net="", escalation="routine")
        report = validator.validate_consultation(rec)
        # block-level: corrected in place, never left routine
        assert rec.escalation == "emergency"
        assert any(f.check == "escalation_consistency" and f.severity == "block"
                   for f in report.findings)
        assert report.corrections

    def test_urgent_leader_raises_routine(self, validator):
        rec = _record(ranked_differential=[
            {"condition_id": "tb_pulmonary", "name": "TB", "score": 1.5,
             "reasons": []}], escalation="routine")
        validator.validate_consultation(rec)
        assert rec.escalation in ("urgent", "emergency")

    def test_two_week_wait_leader_names_the_pathway(self, validator):
        rec = _record(ranked_differential=[
            {"condition_id": "colorectal_cancer", "name": "Colorectal ca", "score": 1.2,
             "reasons": []}], escalation="routine")
        report = validator.validate_consultation(rec)
        assert rec.escalation == "urgent"
        assert any("2ww" in c or "two-week" in c for c in report.corrections)

    def test_consistent_routine_record_passes_clean(self, validator):
        rec = _record(ranked_differential=[
            {"condition_id": "viral_urti", "name": "Viral URTI", "score": 1.0,
             "reasons": []}], escalation="routine")
        report = validator.validate_consultation(rec)
        assert not any(f.severity == "block" for f in report.findings)

    def test_correction_only_ever_raises(self, validator):
        # a record already at emergency must never be demoted
        rec = _record(escalation="emergency",
                      ranked_differential=[
                          {"condition_id": "viral_urti", "name": "Viral URTI",
                           "score": 1.0, "reasons": []}])
        validator.validate_consultation(rec)
        assert rec.escalation == "emergency"

    def test_noise_scored_killer_does_not_floor_escalation(self, validator):
        # GCA matching only the generic word 'headache' (score 0.1 beside a
        # 0.4 tension-headache leader) is not a contender — a noise-scored
        # emergency-tier entry must not floor a routine record
        rec = _record(ranked_differential=[
            {"condition_id": "tension_headache", "name": "Tension headache",
             "score": 0.4, "reasons": []},
            {"condition_id": "giant_cell_arteritis", "name": "GCA",
             "score": 0.1, "reasons": []}],
            escalation="routine", safety_net="Return if worse.")
        report = validator.validate_consultation(rec)
        assert rec.escalation == "routine"
        assert not any(f.check == "escalation_consistency"
                       for f in report.findings)

    def test_close_scored_killer_does_floor_escalation(self, validator):
        # the same killer within reach of the leader IS a contender
        rec = _record(ranked_differential=[
            {"condition_id": "chikungunya", "name": "Chikungunya",
             "score": 0.46, "reasons": []},
            {"condition_id": "malaria_falciparum", "name": "Malaria",
             "score": 0.45, "reasons": []}],
            escalation="urgent", safety_net="Return if worse.")
        validator.validate_consultation(rec)
        assert rec.escalation == "emergency"

    def test_generic_only_emergency_match_does_not_floor(self, validator):
        """Criterion 3 (8.1): CO matched purely on 'headache, nausea'
        (specificity 0.20/0.10) 999'd every hangover and altitude
        headache in the system. Two generic words are the same noise
        one generic word already was."""
        rec = _record(ranked_differential=[
            {"condition_id": "migraine", "name": "Migraine",
             "score": 0.13, "reasons": []},
            {"condition_id": "carbon_monoxide_poisoning", "name": "CO",
             "score": 0.11,
             "reasons": ["matched: headache, nausea"]}],
            escalation="routine", safety_net="Return if worse.")
        report = validator.validate_consultation(rec)
        assert rec.escalation == "routine"
        assert not any(f.check == "escalation_consistency"
                       for f in report.findings)

    def test_specific_token_emergency_match_still_floors(self, validator):
        """fever_after_travel (specificity 0.85) is a real
        discriminator: the malaria raise must survive criterion 3."""
        rec = _record(ranked_differential=[
            {"condition_id": "chikungunya", "name": "Chikungunya",
             "score": 0.46, "reasons": []},
            {"condition_id": "malaria_falciparum", "name": "Malaria",
             "score": 0.45,
             "reasons": ["matched: fever, fever_after_travel"]}],
            escalation="urgent", safety_net="Return if worse.")
        validator.validate_consultation(rec)
        assert rec.escalation == "emergency"

    def test_single_token_match_is_not_a_contender(self, validator):
        """The eclampsia lesson (Stage 6.5): when EVERY entry scores low,
        ratios are meaningless — eclampsia sat at 0.93x the leader of an
        8-week-miscarriage record by matching the single generic word
        'pregnant'. A one-token match is noise regardless of ratio."""
        rec = _record(ranked_differential=[
            {"condition_id": "miscarriage_threatened",
             "name": "Threatened miscarriage", "score": 0.29,
             "reasons": ["matched: pregnancy_context, vaginal_bleeding"]},
            {"condition_id": "eclampsia", "name": "Eclampsia",
             "score": 0.27, "reasons": ["matched: pregnancy_context"]}],
            escalation="urgent", safety_net="Return if worse.")
        report = validator.validate_consultation(rec)
        assert rec.escalation == "urgent"

    def test_two_token_close_match_is_a_contender(self, validator):
        """Same presentation, but eclampsia matched two distinct features
        (seizure + pregnancy) — that is evidence, and it floors."""
        rec = _record(ranked_differential=[
            {"condition_id": "miscarriage_threatened",
             "name": "Threatened miscarriage", "score": 0.29,
             "reasons": ["matched: pregnancy_context, vaginal_bleeding"]},
            {"condition_id": "eclampsia", "name": "Eclampsia",
             "score": 0.27, "reasons": ["matched: seizure, pregnancy_context"]}],
            escalation="urgent", safety_net="Return if worse.")
        validator.validate_consultation(rec)
        assert rec.escalation == "emergency"


class TestRetainedAndCompleteness:
    def test_retained_killer_without_exclusion_flagged(self, validator):
        rec = _record(ranked_differential=[
            {"condition_id": "tension_headache", "name": "Tension", "score": 1.0,
             "reasons": []}],
            dangerous_alternatives=[
                {"condition_id": "sah_subarachnoid", "name": "SAH"}],
            treatment="reassurance and simple analgesia")
        report = validator.validate_consultation(rec)
        assert any(f.check == "retained_without_exclusion"
                   for f in report.findings)

    def test_retained_killer_with_documented_exclusion_not_flagged(self, validator):
        rec = _record(ranked_differential=[
            {"condition_id": "tension_headache", "name": "Tension", "score": 1.0,
             "reasons": []}],
            dangerous_alternatives=[
                {"condition_id": "sah_subarachnoid", "name": "SAH"}],
            safety_net="Thunderclap onset or neck stiffness — exclude SAH same day.")
        report = validator.validate_consultation(rec)
        assert not any(f.check == "retained_without_exclusion"
                       for f in report.findings)

    def test_missing_safety_net_flagged(self, validator):
        rec = _record(safety_net="")
        report = validator.validate_consultation(rec)
        assert any(f.check == "safety_net_presence" for f in report.findings)


class TestSafeguardingSignal:
    def test_coercive_control_disclosure_surfaced(self, validator):
        rec = _record(presenting_complaint=(
            "my husband controls all my medicines and won't let me come "
            "to the doctor alone"))
        report = validator.validate_consultation(rec)
        assert any(f.check == "safeguarding_signal" and "coercive" in f.evidence
                   for f in report.findings)

    def test_neutral_complaint_no_safeguarding_flag(self, validator):
        rec = _record(presenting_complaint="sore throat for two days")
        report = validator.validate_consultation(rec)
        assert not any(f.check == "safeguarding_signal" for f in report.findings)


class TestClaimGrounding:
    def test_false_renal_claim_blocked_with_truth(self, validator):
        report = validator.verify_claim("metformin is safe to continue at egfr 20")
        assert not report.passed
        assert any(f.severity == "block" and "metformin" in f.evidence.lower()
                   for f in report.findings)

    def test_truthful_renal_claim_passes(self, validator):
        report = validator.verify_claim("metformin should be stopped at egfr 20")
        assert report.passed

    def test_false_monitoring_claim_flagged(self, validator):
        report = validator.verify_claim("lithium needs no monitoring")
        assert not report.passed

    def test_ungrounded_guideline_citation_flagged(self, validator):
        report = validator.verify_claim(
            "NICE NG99 says prescribe antibiotics for all sore throats")
        assert not report.passed

    def test_grounded_guideline_citation_passes(self, validator):
        report = validator.verify_claim("per CKS sore throat guidance, "
                                        "most are viral and self-limiting")
        assert report.passed

    def test_neutral_claim_passes(self, validator):
        report = validator.verify_claim("encourage fluids and rest")
        assert report.passed


class TestHallucinationRegister:
    def test_recorded_hallucination_blocks_and_corrects(self, tmp_path):
        v = ClinicalValidator(register_path=tmp_path / "reg.json")
        v.record_hallucination("azithromycin cures all pneumonias in one dose",
                               "no single-dose rule exists in the knowledge base",
                               "antimicrobial_stewardship")
        v2 = ClinicalValidator(register_path=tmp_path / "reg.json")
        report = v2.verify_claim("azithromycin cures all pneumonias in one dose")
        assert not report.passed
        assert any("no single-dose rule" in f.evidence for f in report.findings)

    def test_register_loads_from_default_path_when_file_missing(self, tmp_path):
        v = ClinicalValidator(register_path=tmp_path / "never_written.json")
        assert v.verify_claim("paracetamol for pain").passed

    def test_claims_round_trip_through_disk(self, tmp_path):
        p = tmp_path / "reg2.json"
        ClinicalValidator(register_path=p).record_hallucination(
            "claim a", "truth a", "test")
        data = ClinicalValidator(register_path=p)._load_register()
        assert any(e.claim == "claim a" for e in data.values())


class TestReportShape:
    def test_summary_renders(self, validator):
        rec = _record(safety_net="", ranked_differential=[
            {"condition_id": "acs_stemi", "name": "STEMI", "score": 2.0,
             "reasons": []}], escalation="routine")
        report = validator.validate_consultation(rec)
        assert "escalation_consistency" in report.summary()
