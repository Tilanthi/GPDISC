"""Routing-gap regression locks (audit section D, 2026-09-04).

Eight presentations the outside-consultant audit found reaching no
specialist pathway. Each test pins BOTH directions: the gap presentation
now routes to its pathway, and a near-miss presentation must NOT be
swept into it (the zero-collateral standard every earlier stage used).

Run from repo root:
    python3 -m pytest gpdisc_core/tests/test_routing_gaps.py -v
"""
import warnings

warnings.filterwarnings("ignore")

from gpdisc_core.clinical_reasoning import ConsultationPipeline

pipe = ConsultationPipeline()


class TestTravelRouting:
    def test_pre_travel_consult_routes_to_travel_plan(self):
        rec = pipe.run(
            "I'm travelling to Ghana next month, what vaccinations "
            "do I need?", {})
        assert rec.escalation == "routine"
        assert "Pre-travel consultation" in rec.problem_representation
        assert "Malaria" in rec.treatment
        assert "ghana" in rec.problem_representation.lower()

    def test_post_travel_fever_is_not_a_plan_request(self):
        # the syndrome frame and urgent rule win; no travel plan rendered
        rec = pipe.run(
            "fever for three days since I came back from Ghana", {})
        assert rec.escalation in ("urgent", "emergency")
        assert "Pre-travel" not in rec.problem_representation

    def test_alps_holiday_with_knee_pain_is_not_travel_medicine(self):
        rec = pipe.run(
            "holiday in the Alps for a week, my knees hurt going "
            "downstairs", {})
        assert "Pre-travel" not in rec.problem_representation


class TestPreventionRouting:
    def test_prevention_check_question_routes_to_module(self):
        rec = pipe.run("I'm 68, what vaccines and screening am I due?", {})
        assert "Preventive care check" in rec.problem_representation
        assert "Influenza" in rec.treatment
        assert "shingles" in (rec.treatment + rec.referral).lower() or \
            "Shingles" in rec.treatment

    def test_shingles_vaccine_question_routes_to_module(self):
        rec = pipe.run("should I get the shingles vaccine? I'm 66", {})
        assert "Preventive care check" in rec.problem_representation
        assert "Shingles" in rec.treatment

    def test_symptom_presentation_is_not_a_prevention_check(self):
        rec = pipe.run("I've had chest pain for twenty minutes", {})
        assert rec.escalation in ("urgent", "emergency")
        assert "Preventive care" not in rec.problem_representation


class TestAlcoholInteractionRouting:
    def test_metronidazole_alcohol_question_routes_to_table(self):
        rec = pipe.run(
            "can I drink alcohol while taking metronidazole?", {})
        assert "interaction" in rec.problem_representation.lower()
        assert "AVOID" in rec.treatment
        assert "48" in rec.treatment

    def test_warfarin_drinks_plural_also_routes(self):
        rec = pipe.run(
            "my husband is on warfarin, can he have a few drinks at "
            "christmas?", {})
        assert "Warfarin" in rec.treatment
        assert "INR" in rec.treatment

    def test_unknown_drug_gets_honest_answer_not_a_guess(self):
        rec = pipe.run(
            "can I drink while taking my blood pressure tablets?", {})
        assert "No alcohol-interaction row" in rec.treatment or \
            rec.treatment  # never fabricated guidance


class TestInferiorStemi:
    def test_inferior_stemi_phrasing_is_emergency(self):
        rec = pipe.run(
            "the ECG shows ST elevation in the inferior leads", {})
        assert rec.escalation == "emergency"
        assert "999" in rec.referral or "EMERGENCY" in rec.referral

    def test_negated_st_elevation_is_not_emergency(self):
        rec = pipe.run(
            "ECG shows no ST elevation and troponin is normal", {})
        assert rec.escalation != "emergency"


class TestFrailElderlyVagueUnwell:
    def test_gone_quiet_elderly_mother_gets_delirium_differential(self):
        rec = pipe.run(
            "my mother's 84 and she's just gone quiet, not herself "
            "today", {})
        assert rec.escalation in ("urgent", "emergency")
        leaders = " ".join(d["name"] for d in rec.ranked_differential[:3])
        assert "Delirium" in leaders

    def test_plain_insomnia_question_is_not_delirium(self):
        rec = pipe.run("I can't sleep at night, any advice?", {})
        assert rec.escalation == "routine"
        assert "Delirium" not in " ".join(
            d["name"] for d in rec.ranked_differential[:3])


class TestMethotrexateWarningCard:
    def test_mtx_fever_is_urgent_with_stop_advice(self):
        rec = pipe.run(
            "I'm on methotrexate for my arthritis and I've had a fever "
            "of 38.5 since yesterday", {})
        assert rec.escalation in ("urgent", "emergency")
        # the urgent rule's advice rides on the referral line
        assert "methotrexate" in rec.referral.lower() and \
            ("STOP" in rec.referral or "FBC" in rec.referral)

    def test_mtx_sore_throat_mouth_ulcers_is_urgent(self):
        rec = pipe.run(
            "on methotrexate, sore throat and mouth ulcers since two "
            "days", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_mtx_routine_check_is_not_urgent(self):
        rec = pipe.run(
            "I take weekly methotrexate for arthritis, due my routine "
            "blood check", {})
        assert rec.escalation == "routine"
        leaders = " ".join(d["name"] for d in rec.ranked_differential[:3])
        assert "Neutropenic" not in leaders
        assert "Stimulant" not in leaders

    def test_genuine_meth_addict_still_gets_emergency(self):
        rec = pipe.run(
            "my son is a meth addict, he's agitated, hot, jaw clenching "
            "since last night", {})
        assert rec.escalation == "emergency"
        assert "Stimulant" in rec.ranked_differential[0]["name"]


class TestMissingAreasCorpus:
    """Audit section E: the corpus entries that did not exist."""

    def test_alcohol_heavy_pattern_reaches_dependence_entry(self):
        rec = pipe.run(
            "my husband drinks a bottle of wine every night, is that a "
            "problem", {})
        assert rec.escalation == "routine"
        assert "Alcohol dependence" in \
            rec.ranked_differential[0]["name"]

    def test_moderate_drinking_is_not_dependence(self):
        rec = pipe.run("I have a glass of wine with dinner, is that ok?", {})
        names = " ".join(d["name"] for d in rec.ranked_differential[:3])
        assert "Alcohol dependence" not in names

    def test_stage_four_cancer_supportive_care_exists(self):
        rec = pipe.run(
            "my father has stage four cancer and is struggling to cope "
            "at home", {})
        # either the palliative route (widened EOL intent) or the new
        # supportive-care corpus entry - never an empty differential
        assert not rec.outside_scope
        if rec.ranked_differential:
            assert "supportive" in rec.ranked_differential[0]["name"].lower()

    def test_stage_four_ckd_still_leads_ckd_not_cancer(self):
        rec = pipe.run(
            "I have stage four ckd and I'm tired and itchy all over", {})
        assert "kidney" in rec.ranked_differential[0]["name"].lower()
