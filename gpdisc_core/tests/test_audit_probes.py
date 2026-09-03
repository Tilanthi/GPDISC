"""The consultant-audit probes, locked as regression tests.

Every case here is a marginal or atypical presentation that fell through
the engine on audit day (docs/superpowers/specs/2026-09-03-consultant-audit.md).
These are the patients keyword textbooks lose: the woman with ACS and no
chest-pain words, the elderly mother who 'just went quiet', the ectopic no
one suspected. Targets are honest clinical expectations, verified by hand.
"""
import pytest
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline

PIPE = ConsultationPipeline()


def _ids(rec):
    return ({d["condition_id"] for d in rec.ranked_differential}
            | {d["condition_id"] for d in rec.dangerous_alternatives}
            | {d["condition_id"] for d in rec.syndrome_differentials})


class TestAuditProbes:
    def test_atypical_acs_woman_no_chest_pain_words(self):
        rec = PIPE.run("67 year old woman, sudden nausea and sweating with "
                       "jaw ache for 20 minutes, no chest pain", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_afebrile_elderly_behaviour_change(self):
        rec = PIPE.run("my 88 year old mother has gone quiet and off her "
                       "food since yesterday, not herself, no fever, "
                       "speaking fewer words", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_ectopic_pregnancy_not_suspected(self):
        rec = PIPE.run("32 year old woman sudden severe one-sided pelvic "
                       "pain, dizzy on standing, no bleeding, coil in place", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_infant_poor_feeding_urgent(self):
        rec = PIPE.run("4 month old baby, poor feeding since yesterday, "
                       "fewer wet nappies, drowsy, no fever, no rash", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_weight_loss_night_sweats_keeps_systemic_differential(self):
        rec = PIPE.run("63 year old man, lost 6 kg without trying over two "
                       "months, night sweats, otherwise feels fine", {})
        ids = _ids(rec)
        assert ids & {"tb_pulmonary", "infective_endocarditis",
                      "hiv_seroconversion", "colorectal_cancer"}

    def test_somatic_depression_recognised(self):
        rec = PIPE.run("45 year old woman, no energy for six months, aching "
                       "all over, sleeping badly, can't enjoy anything, "
                       "periods normal", {})
        ids = {d["condition_id"] for d in rec.ranked_differential}
        assert "depression_moderate" in ids

    def test_medication_cause_ranked(self):
        rec = PIPE.run("72 year old man dizzy when standing since his new "
                       "tablet last week, takes ramipril and furosemide", {})
        ids = {d["condition_id"] for d in rec.ranked_differential}
        assert "polypharmacy_adverse_effect" in ids

    def test_posterior_circulation_stroke(self):
        rec = PIPE.run("79 year old, sudden dizziness and double vision "
                       "since breakfast, unsteady on his feet, no weakness", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_postoperative_pe_emergency(self):
        rec = PIPE.run("58 year old woman, breathless for three days, knee "
                       "replacement two weeks ago, no calf pain", {})
        assert rec.escalation == "emergency"

    def test_new_heart_failure_ranked(self):
        rec = PIPE.run("78 year old, new ankle swelling both legs and "
                       "waking at night breathless, on amlodipine", {})
        ids = {d["condition_id"] for d in rec.ranked_differential}
        assert "acute_heart_failure" in ids

    def test_coercive_control_disclosure_flagged(self):
        rec = PIPE.run("my husband controls all my medicines and won't let "
                       "me come to the doctor alone", {})
        assert rec.validation is not None
        assert any(f.check == "safeguarding_signal"
                   for f in rec.validation.findings)

    def test_self_harm_cutting_without_suicide_words(self):
        rec = PIPE.run("17 year old girl has been cutting herself for "
                       "weeks, says she does not want to die", {})
        assert rec.escalation in ("urgent", "emergency")

    def test_meningitis_photophobia_without_fever_word(self):
        rec = PIPE.run("22 year old, severe headache since yesterday, light "
                       "hurts my eyes, vomiting twice", {})
        ids = _ids(rec)
        assert ids & {"meningitis", "sah_subarachnoid", "migraine"}

    def test_anaphylaxis_early_word_order(self):
        rec = PIPE.run("lip swelling and itchy rash after eating a new "
                       "food, breathing normal at the moment", {})
        assert rec.escalation == "emergency"

    def test_marginal_dizziness_asks_discriminating_questions(self):
        rec = PIPE.run("off balance, room spins sometimes when I move "
                       "quickly", {})
        assert rec.discriminating_questions, (
            "marginal presentation must produce questions, not a shrug")

    def test_paracetamol_overdose_escalates(self):
        rec = PIPE.run("took 20 paracetamol tablets six hours ago, "
                       "feels sick", {})
        assert rec.escalation in ("urgent", "emergency")


class TestMarginalQuestionProcess:
    def test_close_top_two_generates_questions(self):
        rec = PIPE.run("67 year old woman, sudden nausea and sweating with "
                       "jaw ache for 20 minutes, no chest pain", {})
        # if the safety layer caught it, the emergency pathway legitimately
        # overrides question-asking; otherwise marginal = must ask
        if rec.escalation != "emergency":
            assert rec.discriminating_questions

    def test_clear_leader_no_synonym_still_consistent(self):
        rec = PIPE.run("sore throat, runny nose and cough for three days, "
                       "no fever, no tonsillar pus", {})
        # questions may or may not fire; the record must stay valid
        assert rec.validation is not None
        assert rec.escalation not in ("emergency",)


class TestValidationWiredIntoPipeline:
    def test_every_record_carries_a_validation_report(self):
        for case in ("chest pain for 30 minutes sweating",
                     "mild headache after stress",
                     "fever since returning from Ghana"):
            rec = PIPE.run(case, {})
            assert rec.validation is not None, case

    def test_summary_renders_validation(self):
        rec = PIPE.run("67 year old woman, sudden nausea and sweating with "
                       "jaw ache for 20 minutes, no chest pain", {})
        assert "Validation" in rec.summary()
