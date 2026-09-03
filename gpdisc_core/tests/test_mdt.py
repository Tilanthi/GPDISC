"""Tests for the MDT layer (expertise program Stage 4)."""
import pytest
from gpdisc_core.clinical_reasoning.diagnostic_engine import DifferentialEngine
from gpdisc_core.mdt.challenger import (
    challenge_differential, Challenge, ATTACK_TYPES,
)


class TestChallenger:
    eng = DifferentialEngine()

    def test_challenges_are_structured(self):
        result = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, "
            "pain radiating to left arm, smoker")
        challenges = challenge_differential(result)
        for c in challenges:
            assert isinstance(c, Challenge)
            assert c.attack_type in ATTACK_TYPES
            assert c.argument and c.action

    def test_never_silent_on_a_leader(self):
        # every differential produces at least one challenge
        result = self.eng.build_differential("tired all the time")
        assert challenge_differential(result)

    def test_dangerous_mimic_attack_fires_on_benign_headache(self):
        result = self.eng.build_differential(
            "mild bilateral headache after stress for a week")
        challenges = challenge_differential(result)
        mimic_attacks = [c for c in challenges if c.attack_type == "dangerous_mimic"]
        assert any("SAH" in c.argument or "subarachnoid" in c.argument.lower()
                   or "GCA" in c.argument or "arteritis" in c.argument.lower()
                   or "meningitis" in c.argument.lower()
                   for c in mimic_attacks)

    def test_empty_differential_no_crash(self):
        class _Empty:
            ranked = []
            retained_dangerous = []
        assert challenge_differential(_Empty()) == []

    def test_missing_discriminator_cites_features(self):
        result = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, "
            "pain radiating to left arm, smoker")
        challenges = challenge_differential(result)
        md = [c for c in challenges if c.attack_type == "missing_discriminator"]
        assert md and md[0].action


from gpdisc_core.mdt.roles import MDT_ROLES, MDTRole, contribute


class TestMDTRoles:
    def test_core_team_six_roles(self):
        # Stage 9 Task 9.1: six core roles + six consultant opinions
        assert {r.key for r in MDT_ROLES} == {
            "gp_chair", "geriatrician", "clinical_pharmacologist",
            "safeguarding_practitioner", "mental_health", "patient_advocate",
            "cardiologist", "neurologist", "oncologist", "paediatrician",
            "psychiatrist", "palliative_physician"}

    def test_every_core_role_contributes_something(self):
        core = ("gp_chair", "geriatrician", "clinical_pharmacologist",
                "safeguarding_practitioner", "mental_health",
                "patient_advocate")
        for key in core:
            assert contribute(key, "tired all the time", {})

    def test_consultants_silent_on_generic_presentation(self):
        # A specialist who comments on everything is noise: on a
        # non-specific presentation no consultant speaks.
        consultants = ("cardiologist", "neurologist", "oncologist",
                       "paediatrician", "psychiatrist",
                       "palliative_physician")
        for key in consultants:
            assert contribute(key, "tired all the time", {}) == []

    def test_pharmacologist_uses_renal_flags(self):
        notes = contribute("clinical_pharmacologist",
                           "dizzy and confused",
                           {"medications": ["metformin"], "egfr": 25})
        assert any("STOP" in n or "metformin" in n.lower() for n in notes)

    def test_geriatrician_fires_on_age(self):
        notes = contribute("geriatrician", "confusion", {"age_years": 82})
        assert any("atypical" in n.lower() for n in notes)

    def test_safeguarding_detects_concerns(self):
        notes = contribute("safeguarding_practitioner",
                           "son always answers for her, money missing", {})
        assert any("privately" in n.lower() or "alone" in n.lower()
                   for n in notes)

    def test_unknown_role_empty(self):
        assert contribute("astronaut", "anything") == []


from gpdisc_core.mdt.debate import run_mdt, MDTResult


class TestDebate:
    def test_result_shape(self):
        r = run_mdt("66 year old man, chest pain for 40 minutes, "
                    "sweating, pain radiating to left arm")
        assert isinstance(r, MDTResult)
        assert r.escalation == "emergency"
        assert r.differential_ids
        assert r.synthesis and r.actions

    def test_emergency_first_action_is_escalation(self):
        r = run_mdt("crushing chest pain 30 minutes, sweating")
        assert r.actions[0].startswith("Escalate")

    def test_uncertainty_is_stated(self):
        r = run_mdt("tired all the time")
        assert "I don't know yet" in r.synthesis or "Not settled" in r.synthesis

    def test_challenges_flow_into_actions(self):
        r = run_mdt("mild bilateral headache after stress for a week")
        assert len(r.actions) >= 2  # safety net + at least one challenge action

    def test_roles_recorded(self):
        r = run_mdt("79 year old woman, dizzy and confused, eight medications",
                    {"medications": ["metformin", "ramipril"], "egfr": 28})
        assert "clinical_pharmacologist" in r.role_notes
        assert "geriatrician" in r.role_notes

    def test_actions_deduplicated(self):
        r = run_mdt("fever for two days since returning from Ghana")
        assert len(r.actions) == len(set(r.actions))

    def test_syndrome_survives_the_debate(self):
        r = run_mdt("fever for two days since returning from Ghana")
        assert r.syndrome == "fever_after_travel"


from gpdisc_core.mdt.multimorbidity import (
    TREATMENT_TENSIONS, ACB_SCORES, whole_patient_review,
)


GLENN_CASE = {
    "age_years": 79,
    "conditions": ["chronic_kidney_disease", "type_2_diabetes",
                   "heart_failure", "osteoarthritis", "cognitive_impairment",
                   "hypertension"],
    "medications": ["metformin", "ramipril", "furosemide", "bisoprolol",
                    "amitriptyline", "gliclazide", "paracetamol", "omeprazole"],
    "egfr": 28,
    "symptoms": ["dizziness", "confusion"],
}


class TestMultimorbidity:
    def test_ten_tensions_defined(self):
        assert len(TREATMENT_TENSIONS) == 10

    def test_glenn_case_renal_flags_fire(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("metformin" in f and "STOP" in f
                   for f in review["medication_flags"])

    def test_glenn_case_acb_scores(self):
        review = whole_patient_review(GLENN_CASE)
        assert review["anticholinergic_burden"] >= 4  # amitriptyline 3 + furosemide 1
        assert "amitriptyline" in review["anticholinergic_drugs"]

    def test_glenn_case_tensions_matched(self):
        review = whole_patient_review(GLENN_CASE)
        pairs = [tuple(t["conditions"]) for t in review["tensions"]]
        assert ("chronic_kidney_disease", "osteoarthritis") in pairs
        assert ("type_2_diabetes", "cognitive_impairment") in pairs

    def test_dizziness_causes_include_postural_bp(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("standing" in c.lower()
                   for c in review["symptom_causes"]["dizziness"])

    def test_confusion_rules_out_sepsis_first(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("sepsis" in c.lower()
                   for c in review["symptom_causes"]["confusion"])

    def test_priorities_ordered_and_nonempty(self):
        review = whole_patient_review(GLENN_CASE)
        assert review["priorities"]
        standing = [p for p in review["priorities"] if "standing" in p.lower()]
        assert standing  # postural BP is in the priority list for dizziness

    def test_appointment_design_present(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("Stop before you start" in a for a in review["appointment_design"])

    def test_minimal_patient_defaults_sensibly(self):
        review = whole_patient_review({})
        assert review["medication_flags"] == []
        assert review["priorities"]  # patient's own priority is still first


from gpdisc_core.mdt import (
    run_mdt, challenge_differential, MDT_ROLES, contribute,
    whole_patient_review, TREATMENT_TENSIONS,
)


class TestMDTExports:
    def test_package_root_exports(self):
        assert callable(run_mdt)
        assert len(MDT_ROLES) == 12  # 6 core + 6 consultants (Stage 9)
        assert len(TREATMENT_TENSIONS) == 10
        assert whole_patient_review({"medications": ["metformin"], "egfr": 25})
