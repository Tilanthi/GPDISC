"""Tests for the GPDISC clinical reasoning core (expertise program Stage 1)."""
import pytest

from gpdisc_core.clinical_reasoning.knowledge import (
    CONDITIONS, SYMPTOM_SYNONYMS, ConditionProfile,
    find_condition, conditions_for_symptom,
)
from gpdisc_core.clinical_reasoning.test_interpretation import (
    TestInterpreter, REFERENCE_RANGES,
)
from gpdisc_core.clinical_reasoning.safety import SafetyLayer, EscalationLevel
from gpdisc_core.clinical_reasoning.diagnostic_engine import DifferentialEngine
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline

VALID_TIERS = {"self_care", "routine", "urgent", "two_week_wait", "emergency"}


class TestCorpusIntegrity:
    def test_all_entries_are_profiles(self):
        assert all(isinstance(c, ConditionProfile) for c in CONDITIONS)

    def test_ids_unique(self):
        ids = [c.condition_id for c in CONDITIONS]
        assert len(ids) == len(set(ids))

    def test_every_field_populated(self):
        for c in CONDITIONS:
            assert c.name and c.category
            assert c.symptoms, c.condition_id
            assert 0.0 < c.prevalence_per_consult <= 0.5, c.condition_id
            for s in c.symptoms:
                assert 0.0 < s.frequency <= 1.0
                assert 0.0 <= s.specificity <= 1.0
            assert c.referral_tier in VALID_TIERS, c.condition_id
            assert c.safety_net and c.management_first_line

    def test_every_symptom_token_has_synonyms(self):
        tokens = {s.symptom for c in CONDITIONS for s in c.symptoms}
        for tok in tokens:
            assert tok in SYMPTOM_SYNONYMS, f"missing synonym entry: {tok}"

    def test_find_condition(self):
        assert find_condition("acs_stemi").name
        assert find_condition("nope") is None

    def test_conditions_for_symptom(self):
        hits = conditions_for_symptom("chest_pain")
        assert any(c.condition_id == "acs_stemi" for c in hits)

    def test_corpus_breadth(self):
        assert len(CONDITIONS) >= 75
        cats = {c.category for c in CONDITIONS}
        for needed in ("endocrine", "infection", "paediatric", "geriatric_frailty",
                       "mental_health", "musculoskeletal", "dermatology",
                       "ent_eye", "womens_health", "urology_kidney", "haematology"):
            assert needed in cats, f"missing category {needed}"


from gpdisc_core.clinical_reasoning.knowledge_tropical import (
    CONDITIONS_PART3, SYMPTOM_SYNONYMS_PART3,
)


class TestCorpusPart3:
    def test_part3_integrity(self):
        for c in CONDITIONS_PART3:
            assert c.referral_tier in VALID_TIERS, c.condition_id
            assert 0.0 < c.prevalence_per_consult <= 0.5, c.condition_id
            assert c.safety_net and c.management_first_line, c.condition_id
            for s in c.symptoms:
                assert 0.0 < s.frequency <= 1.0 and 0.0 <= s.specificity <= 1.0

    def test_part3_ids_unique_and_new(self):
        from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS
        ids = [c.condition_id for c in CONDITIONS]
        assert len(ids) == len(set(ids)), "duplicate condition id after merge"
        # 121 (Stage 1) + 15 (tropical, Stage 2) + 14 (breadth, Stage 5)
        # + 14 trauma/burns (6.3) + 13 toxicology (6.4)
        # + 9 obstetric (6.5) + 7 onc-supportive/derm (6.6)
        # + 7 paediatric protection (6.7) + 2 PEP exposure (6.8)
        # + 13 chronic neurology + mental health (7.1)
        # + 16 derm + women's + men's health (7.2)
        # + 15 chronic GI/hepato-renal + eyes/ENT + sleep/pain (7.3)
        # + 26 global burden + environmental extremes (8.1; cholera
        # dropped as a shadow duplicate of knowledge_tropical's entry)
        # + 1 advanced-cancer supportive care (audit missing-area, 2026-09-04)
        assert len(CONDITIONS) == 273
        part3_ids = {c.condition_id for c in CONDITIONS_PART3}
        old_ids = set(ids) - part3_ids
        assert not (part3_ids & old_ids)

    def test_part4_trauma_corpus_integrity(self):
        """Stage 6 Tasks 6.3+6.4: trauma/burns + toxicology — the
        categories the corpus did not have. Every profile carries the
        full standard and its symptom tokens all have synonyms."""
        from gpdisc_core.clinical_reasoning.knowledge import (
            CONDITIONS, SYMPTOM_SYNONYMS)
        from gpdisc_core.clinical_reasoning.knowledge_emergencies import (
            CONDITIONS_PART4)
        assert len(CONDITIONS_PART4) == 52
        trauma = [c for c in CONDITIONS if c.category == "trauma"]
        tox = [c for c in CONDITIONS if c.category == "toxicology"]
        obst = [c for c in CONDITIONS if c.category == "obstetrics"]
        assert len(trauma) == 14
        assert len(tox) == 13
        assert len(obst) == 9
        onc = [c for c in CONDITIONS if c.category == "oncology_supportive"]
        assert len(onc) == 3
        # 6.7: six paediatric entries plus the safeguarding category
        # (8.1: +1 — FGM care/safeguarding)
        safeguard = [c for c in CONDITIONS if c.category == "safeguarding"]
        assert len(safeguard) == 2
        assert {c.condition_id for c in safeguard} == {
            "non_accidental_injury", "fgm_care_needs"}
        peds = [c for c in CONDITIONS if c.category == "paediatric"]
        assert len(peds) == 12
        for c in CONDITIONS_PART4:
            assert c.referral_tier in ("emergency", "urgent", "self_care"), \
                c.condition_id
            assert c.red_flags, c.condition_id
            for s in c.symptoms:
                assert s.symptom in SYMPTOM_SYNONYMS, \
                    f"{c.condition_id}: {s.symptom} has no synonyms"

    def test_part5_chronic_neuro_and_mh_corpus(self):
        """Stage 7 Tasks 7.1-7.3: chronic neurology + mental health
        (13) + derm/women's/men's health (16) + chronic GI/hepato-
        renal + eyes/ENT + sleep/pain/continence (15) — 44 entries,
        full standard, every token has synonyms."""
        from gpdisc_core.clinical_reasoning.knowledge import (
            CONDITIONS, SYMPTOM_SYNONYMS)
        from gpdisc_core.clinical_reasoning.knowledge_breadth2 import (
            CONDITIONS_PART5)
        # 44 (Stage 7) + advanced_cancer_supportive (audit missing-area
        # 3, 2026-09-04) = 45
        assert len(CONDITIONS_PART5) == 45
        # the 7.1 over-triage fix must hold: status_epilepticus scores
        # only on not-stopping wording, never the bare word 'seizure'
        status = find_condition("status_epilepticus")
        assert all(s.symptom != "seizure" for s in status.symptoms)
        for c in CONDITIONS_PART5:
            for s in c.symptoms:
                assert s.symptom in SYMPTOM_SYNONYMS, \
                    f"{c.condition_id}: {s.symptom} has no synonyms"

    def test_part3_synonym_keys_were_new(self):
        # update() overwrites existing keys — every part-3 key must have been
        # new at merge time. Part2 keys are the previously-added set.
        from gpdisc_core.clinical_reasoning import knowledge_breadth
        assert not (set(SYMPTOM_SYNONYMS_PART3) & set(knowledge_breadth.SYMPTOM_SYNONYMS_PART2))

    def test_new_categories_present(self):
        from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS
        cats = {c.category for c in CONDITIONS}
        for needed in ("tropical", "ent_oral", "sexual_health"):
            assert needed in cats, needed
        tropical = [c for c in CONDITIONS if c.category == "tropical"]
        assert len(tropical) == 20   # 14 + 8.1 NTDs (cholera stayed tropical)
        assert any(c.referral_tier == "emergency" for c in tropical)  # vhf_suspect

    def test_malaria_vivax_findable(self):
        from gpdisc_core.clinical_reasoning.knowledge import find_condition
        assert find_condition("malaria_vivax").referral_tier == "urgent"
        assert find_condition("vhf_suspect").referral_tier == "emergency"

    def test_strongyloides_hyperinfection_red_flag(self):
        from gpdisc_core.clinical_reasoning.knowledge import find_condition
        c = find_condition("strongyloidiasis")
        assert any("immunosuppression" in f or "steroid" in f
                   for f in c.red_flags + [c.safety_net])


class TestTestInterpreter:
    ti = TestInterpreter()

    def test_ppv_npv_classic_example(self):
        # sens .99, spec .95, prevalence 1% -> PPV ~16.6%, NPV ~99.99%
        ppv, npv = self.ti.predictive_values(0.99, 0.95, 0.01)
        assert ppv == pytest.approx(0.166, abs=0.01)
        assert npv > 0.9998

    def test_post_test_probability_with_lr(self):
        # pre-test 10% odds, LR+ 10 -> post ~52.6%
        assert self.ti.post_test_probability(0.10, 10.0) == pytest.approx(0.526, abs=0.005)

    def test_lr_positive_from_sens_spec(self):
        assert self.ti.likelihood_ratio_positive(0.99, 0.95) == pytest.approx(19.8, abs=0.1)

    def test_lr_below_one_lowers(self):
        assert self.ti.post_test_probability(0.5, 0.1) < 0.15

    def test_reference_range_classification(self):
        assert self.ti.interpret_value("potassium", 3.0) == "low"
        assert self.ti.interpret_value("potassium", 4.2) == "normal"
        assert self.ti.interpret_value("potassium", 6.7) == "critical_high"
        assert self.ti.interpret_value("haemoglobin", 70.0) == "low"

    def test_unknown_analyte(self):
        assert self.ti.interpret_value("not_a_test", 1.0) == "unknown_analyte"

    def test_should_investigate_test_only_if_it_changes_management(self):
        # very low pre-test, weak test, treatment threshold high -> do not test
        decision = self.ti.should_investigate(
            pre_test=0.01,
            sensitivity=0.5, specificity=0.5,
            test_threshold=0.05, treatment_threshold=0.9)
        assert decision == "no_value"
        # positive result would cross treatment threshold -> test
        decision = self.ti.should_investigate(
            pre_test=0.3,
            sensitivity=0.95, specificity=0.9,
            test_threshold=0.05, treatment_threshold=0.6)
        assert decision == "test"


from gpdisc_core.clinical_reasoning.syndromes import (
    SyndromeEngine, SYNDROME_FRAMES, discriminating_questions,
)


class TestSyndromeEngine:
    eng = SyndromeEngine()

    def test_five_frames_defined(self):
        assert [f.key for f in SYNDROME_FRAMES] == [
            "fever_after_travel", "eosinophilia_returning_traveller",
            "fever_thrombocytopenia", "fever_jaundice", "fever_rash"]

    def test_fever_after_travel_detected_from_text(self):
        f = self.eng.for_presentation("high fever for three days since returning from Ghana")
        assert f is not None and f.key == "fever_after_travel"
        assert f.differentials[0].condition_id == "malaria_falciparum"

    def test_fever_plus_rash_frame(self):
        f = self.eng.for_presentation("fever and a widespread rash that started yesterday")
        assert f.key == "fever_rash"
        assert any(d.condition_id == "meningococcal_child" for d in f.differentials)

    def test_thrombocytopenia_frame_from_context(self):
        f = self.eng.for_presentation("fever after returning from Vietnam",
                                      {"bloods": "platelets are low"})
        assert f.key in ("fever_after_travel", "fever_thrombocytopenia")

    def test_eosinophilia_frame(self):
        f = self.eng.for_presentation("routine bloods show raised eosinophils, "
                                      "back from Kenya three months ago")
        assert f.key == "eosinophilia_returning_traveller"
        assert any(d.condition_id == "strongyloidiasis" for d in f.differentials)

    def test_no_frame_for_unrelated(self):
        assert self.eng.for_presentation("knee pain for six weeks") is None

    def test_discriminating_questions_nonempty(self):
        f = self.eng.for_presentation("fever and rash since returning from Nigeria")
        qs = discriminating_questions(f)
        assert qs and any("blanch" in q.lower() or "glass" in q.lower() for q in qs)

    def test_frame_differentials_carry_ids(self):
        for f in SYNDROME_FRAMES:
            for d in f.differentials:
                assert d.condition_id


class TestSafetyLayer:
    sl = SafetyLayer()

    def test_sepsis_cluster_is_emergency(self):
        a = self.sl.screen("My father is confused, breathing fast, feverish and hasn't passed urine since morning", {})
        assert a.level == EscalationLevel.EMERGENCY
        assert any("sepsis" in t for t in a.triggers)

    def test_stroke_fast_is_emergency(self):
        a = self.sl.screen("sudden drooping face and slurred speech this morning", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_thunderclap_headache_is_emergency(self):
        a = self.sl.screen("worst headache of my life came on like a blow an hour ago", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_benign_tension_headache_not_escalated(self):
        a = self.sl.screen("mild bilateral headache after stress for a week, no other symptoms", {})
        assert a.level in (EscalationLevel.ROUTINE, EscalationLevel.SELF_CARE)

    def test_cauda_equina_red_flag(self):
        a = self.sl.screen("back pain and now can't control my bladder, numbness in the saddle area", {})
        assert a.level == EscalationLevel.EMERGENCY
        assert any("cauda" in t for t in a.triggers)

    def test_fever_after_travel_flagged(self):
        a = self.sl.screen("fever for two days since returning from Ghana", {})
        assert a.level == EscalationLevel.URGENT
        assert any("travel" in t for t in a.triggers)

    def test_child_rash_non_blanching(self):
        a = self.sl.screen("my 3 year old has fever and a rash that doesn't fade when pressed", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_pregnancy_bleeding_urgent_plus(self):
        a = self.sl.screen("6 weeks pregnant and bleeding heavily with one-sided pain", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_safety_net_for_condition(self):
        assert "999" in self.sl.safety_net_for("acs_stemi")

    def test_requires_human(self):
        a = self.sl.screen("crushing chest pain sweating", {})
        assert self.sl.requires_human(a) is True


class TestDifferentialEngine:
    eng = DifferentialEngine()

    def test_typical_chest_pain_ranks_acs_in_top3(self):
        r = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, pain radiating to left arm, smoker")
        top3 = [d.condition_id for d in r.ranked[:3]]
        assert "acs_stemi" in top3 or "acs_nstemi" in top3

    def test_common_things_common(self):
        r = self.eng.build_differential(
            "mild bilateral headache coming on over days after stress, no other symptoms")
        top2 = [d.condition_id for d in r.ranked[:2]]
        assert "tension_headache" in top2
        assert "sah_subarachnoid" not in top2

    def test_anti_anchoring_retains_dangerous_alternative(self):
        r = self.eng.build_differential(
            "mild bilateral headache coming on over days after stress, no other symptoms")
        retained_ids = {d.condition_id for d in r.retained_dangerous}
        assert "sah_subarachnoid" in retained_ids or "giant_cell_arteritis" in retained_ids \
            or "meningitis" in retained_ids

    def test_thunderclap_puts_sah_top(self):
        r = self.eng.build_differential(
            "sudden worst headache of my life one hour ago, vomiting")
        assert r.ranked[0].condition_id == "sah_subarachnoid"

    def test_every_result_has_uncertainty_statement(self):
        r = self.eng.build_differential("tired all the time")
        assert r.uncertainty  # non-empty — uncertainty is first-class

    def test_test_update_uses_likelihood_ratios(self):
        p = self.eng.update_with_test({"test": "troponin_hs", "value": 45}, "acs_nstemi")
        assert p > 0.5
        p_neg = self.eng.update_with_test({"test": "troponin_hs", "value": 3}, "acs_nstemi")
        assert p_neg < p


class TestConsultationPipeline:
    pipe = ConsultationPipeline()

    def test_record_has_all_stages(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        for stage in ("presenting_complaint", "history", "problem_representation",
                      "ranked_differential", "dangerous_alternatives",
                      "investigation_strategy", "treatment", "referral",
                      "follow_up", "safety_net"):
            assert hasattr(rec, stage) or stage in rec.stages

    def test_emergency_short_circuits_to_referral(self):
        rec = self.pipe.run("crushing chest pain for 30 minutes, sweating, "
                            "pain radiating to left arm", {})
        assert rec.escalation == "emergency"
        assert "999" in rec.referral or "999" in rec.safety_net

    def test_summary_is_human_readable(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        s = rec.summary()
        assert "Differential" in s and "Safety net" in s

    def test_benign_gets_safety_net_anyway(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        assert rec.safety_net  # never empty

    def test_uncertainty_is_carried(self):
        rec = self.pipe.run("tired all the time", {})
        assert rec.uncertainty

    def test_fever_after_travel_gets_syndrome_frame(self):
        rec = self.pipe.run("fever for two days since returning from Ghana", {})
        assert rec.syndrome == "fever_after_travel"
        assert any(d["condition_id"] == "malaria_falciparum"
                   for d in rec.syndrome_differentials)
        assert any("malaria" in q.lower() or "itinerary" in q.lower()
                   for q in rec.discriminating_questions)

    def test_no_syndrome_for_plain_headache(self):
        rec = self.pipe.run("mild bilateral headache after stress for a week", {})
        assert rec.syndrome == ""
        assert rec.syndrome_differentials == []

    def test_summary_renders_syndrome(self):
        rec = self.pipe.run("fever and a widespread rash for two days", {})
        s = rec.summary()
        assert "Syndrome frame" in s


from gpdisc_core.core.unified_enhanced import EnhancedUnifiedGPDISCSystem


class TestFrontDoorWiring:
    def test_emergency_query_carries_escalation(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("crushing chest pain 30 minutes, sweating, radiating to left arm")
        assert r.get("escalation") == "emergency"
        assert "consultation" in r

    def test_benign_query_gets_consultation_record(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("mild headache for a week after stress")
        assert "consultation" in r
        assert r["consultation"]["safety_net"]

    def test_existing_answer_key_preserved(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("What does this ECG show: ST elevation in V1-V4")
        assert "answer" in r

    def test_front_door_carries_syndrome(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("fever for two days since returning from Ghana")
        assert r["consultation"]["syndrome"] == "fever_after_travel"
        assert r["consultation"]["discriminating_questions"]

    def test_syndrome_engine_exported(self):
        from gpdisc_core.clinical_reasoning import SyndromeEngine, SYNDROME_FRAMES
        assert len(SYNDROME_FRAMES) == 5

    def test_end_to_end_fever_after_travel_full_stack(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("fever for two days since returning from Ghana, "
                        "swimming in Lake Volta last month")
        assert r["escalation"] in ("emergency", "urgent")
        c = r["consultation"]
        assert c["syndrome"] == "fever_after_travel"
        ids = [d["condition_id"] for d in c["ranked_differential"]]
        assert "malaria_falciparum" in ids
        assert any("malaria" in t.lower() for t in c["investigation_strategy"])

    def test_non_blanching_rash_stays_emergency_with_syndrome(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("my 3 year old has fever and a rash that doesn't fade when pressed")
        assert r["escalation"] == "emergency"
        assert r["consultation"]["syndrome"] == "fever_rash"
