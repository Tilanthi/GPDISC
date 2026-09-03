"""Stage 7 (Tier 2 daily breadth) Task 7.1: chronic neurology + mental
health. The probes that exposed these gaps were run against the live
pipeline before a line of PART5 was written:

  - "my husband is 74 and getting forgetful, left the cooker on twice
    this month"      -> routine, EMPTY differential (no dementia entry)
  - first-ever seizure, fully recovered -> EMERGENCY led by
    status_epilepticus scoring on the bare word "seizure" (over-triage;
    a recovered first seizure is same-day-urgent, not 999)
  - mania probe      -> EMPTY differential
  - Parkinson's probe-> led by alcohol withdrawal delirium (absurd)
  - cluster headache -> migraine-led

Each condition added carries the full profile standard; symptom tokens
must exist in SYMPTOM_SYNONYMS_PART5 (corpus integrity test enforces).
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.clinical_reasoning.knowledge import (
    CONDITIONS, SYMPTOM_SYNONYMS, find_condition,
)
from gpdisc_core.clinical_reasoning.knowledge_breadth2 import (
    CONDITIONS_PART5, SYMPTOM_SYNONYMS_PART5,
)

VALID_TIERS = {"self_care", "routine", "urgent", "two_week_wait", "emergency"}


def _ids(rec):
    return ({d["condition_id"] for d in rec.ranked_differential}
            | {d["condition_id"] for d in rec.dangerous_alternatives})


class TestCorpusPart5Integrity:
    """Every PART5 entry meets the full standard and every token has
    synonyms in the merged map."""

    def test_part5_count(self):
        # 7.1: 7 chronic neurology + 6 mental health
        # 7.2: 7 dermatology + 5 women's health + 4 men's health
        # 7.3: 7 chronic GI/hepatology/renal + 3 eyes/ENT
        #      + 5 sleep/pain/continence
        assert len(CONDITIONS_PART5) == 44

    def test_part5_ids_unique_and_new(self):
        ids = [c.condition_id for c in CONDITIONS]
        assert len(ids) == len(set(ids)), "duplicate id after merge"
        part5_ids = {c.condition_id for c in CONDITIONS_PART5}
        assert part5_ids <= set(ids)
        old_ids = set(ids) - part5_ids
        assert not (part5_ids & old_ids)

    def test_part5_profile_standard(self):
        for c in CONDITIONS_PART5:
            assert c.referral_tier in VALID_TIERS, c.condition_id
            assert 0.0 < c.prevalence_per_consult <= 0.5, c.condition_id
            assert c.safety_net and c.management_first_line, c.condition_id
            assert c.red_flags, c.condition_id
            for s in c.symptoms:
                assert 0.0 < s.frequency <= 1.0
                assert 0.0 <= s.specificity <= 1.0
                assert s.symptom in SYMPTOM_SYNONYMS, \
                    f"{c.condition_id}: {s.symptom} has no synonyms"

    def test_part5_synonym_keys_were_new(self):
        # update() overwrites existing keys silently — every part-5 key
        # must have been new at merge time.
        from gpdisc_core.clinical_reasoning import (
            knowledge_breadth, knowledge_tropical, knowledge_emergencies)
        earlier = (set(knowledge_breadth.SYMPTOM_SYNONYMS_PART2)
                   | set(knowledge_tropical.SYMPTOM_SYNONYMS_PART3)
                   | set(knowledge_emergencies.SYMPTOM_SYNONYMS_PART4))
        from gpdisc_core.clinical_reasoning.knowledge import (
            SYMPTOM_SYNONYMS as CORE)
        core_keys = {k for k in CORE}
        assert not (set(SYMPTOM_SYNONYMS_PART5) & earlier)
        assert not (set(SYMPTOM_SYNONYMS_PART5) & core_keys - set(
            SYMPTOM_SYNONYMS_PART5)), "part-5 key collides with a core key"

    def test_categories(self):
        neuro = [c for c in CONDITIONS if c.category == "neurological"]
        mh = [c for c in CONDITIONS if c.category == "mental_health"]
        assert any(c.condition_id == "dementia_suspected" for c in neuro)
        assert {"bipolar_mania", "ocd", "ptsd", "eupd",
                "bulimia_nervosa", "perinatal_mental_health"} <= {
            c.condition_id for c in mh}
        derm = [c for c in CONDITIONS if c.category == "dermatology"]
        assert {"acne_vulgaris", "urticaria_chronic", "scabies",
                "tinea_corporis", "drug_eruption", "venous_leg_ulcer",
                "seborrhoeic_dermatitis"} <= {c.condition_id for c in derm}
        womens = [c for c in CONDITIONS if c.category == "womens_health"]
        assert {"menopause", "perimenopause", "subfertility", "pcos",
                "dysmenorrhoea"} <= {c.condition_id for c in womens}
        mens = [c for c in CONDITIONS if c.category == "urology_kidney"]
        assert {"erectile_dysfunction", "benign_prostatic_hyperplasia",
                "testicular_cancer_suspect", "prostatitis"} <= {
            c.condition_id for c in mens}
        gi = [c for c in CONDITIONS if c.category == "gastrointestinal"]
        assert {"constipation_simple", "crohns_disease_suspect",
                "ulcerative_colitis_suspect", "coeliac_disease",
                "cirrhosis_decompensated", "inguinal_hernia"} <= {
            c.condition_id for c in gi}
        uro = [c for c in CONDITIONS if c.category == "urology_kidney"]
        assert {"ckd_advanced", "stress_incontinence"} <= {
            c.condition_id for c in uro}
        eye = [c for c in CONDITIONS if c.category == "ent_eye"]
        assert {"wet_amd", "sudden_sensorineural_hearing_loss",
                "orbital_cellulitis"} <= {c.condition_id for c in eye}
        resp = [c for c in CONDITIONS if c.category == "respiratory"]
        assert any(c.condition_id == "obstructive_sleep_apnoea"
                   for c in resp)
        mh = [c for c in CONDITIONS if c.category == "mental_health"]
        assert any(c.condition_id == "insomnia_disorder" for c in mh)
        neuro = [c for c in CONDITIONS if c.category == "neurological"]
        assert any(c.condition_id == "neuropathic_pain" for c in neuro)
        msk = [c for c in CONDITIONS if c.category == "musculoskeletal"]
        assert any(c.condition_id == "chronic_primary_pain" for c in msk)


class TestChronicNeurology:
    pipe = ConsultationPipeline()

    def test_dementia_probe_answered(self):
        rec = self.pipe.run(
            "my husband is 74 and getting forgetful, left the cooker on "
            "twice this month", {})
        assert rec.escalation in ("routine", "urgent")
        assert _ids(rec) & {"dementia_suspected"}, rec.problem_representation

    def test_dementia_mentions_reversible_screen(self):
        c = find_condition("dementia_suspected")
        blob = " ".join(c.discriminators + c.red_flags).lower()
        assert "depression" in blob and "thyroid" in blob and "b12" in blob

    def test_first_seizure_recovered_is_urgent_not_emergency(self):
        rec = self.pipe.run(
            "had my first ever seizure this morning, fully recovered now, "
            "never had a seizure before", {})
        assert rec.escalation == "urgent", rec.problem_representation
        assert _ids(rec) & {"first_seizure_adult"}

    def test_status_epilepticus_still_emergency(self):
        rec = self.pipe.run(
            "my son has been having seizures for the last ten minutes and "
            "is not waking up between them", {})
        assert rec.escalation == "emergency"
        # on the emergency short-circuit the matched SAFETY-RULE id rides
        # in dangerous_alternatives
        assert "status_epilepticus" in _ids(rec)

    def test_status_corpus_no_longer_scores_on_bare_seizure(self):
        c = find_condition("status_epilepticus")
        bare = [s for s in c.symptoms if s.symptom == "seizure"]
        assert not bare, "bare 'seizure' token restored — over-triage risk"
        assert any(s.specificity >= 0.9 for s in c.symptoms)

    def test_parkinsons_leads_over_withdrawal(self):
        rec = self.pipe.run(
            "tremor in my right hand for a year, walking has slowed, "
            "smaller handwriting", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked and ranked[0] == "parkinsons_disease", ranked[:3]
        assert rec.escalation in ("routine", "urgent")

    def test_cluster_headache_leads(self):
        rec = self.pipe.run(
            "severe one-sided headache every night at the same time for a "
            "week, eye watering", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "cluster_headache" in ranked[:2], ranked[:3]
        assert rec.escalation in ("routine", "urgent")

    def test_multiple_sclerosis_in_differential(self):
        rec = self.pipe.run(
            "over the last two years two separate episodes of numbness in "
            "my feet lasting weeks, and blurred vision in one eye last "
            "spring", {})
        assert _ids(rec) & {"multiple_sclerosis_suspect"}

    def test_peripheral_neuropathy_leads_in_diabetic(self):
        rec = self.pipe.run(
            "burning and pins and needles in both feet every night, "
            "diabetic for twenty years", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked and ranked[0] == "peripheral_neuropathy", ranked[:3]

    def test_established_epilepsy_breakthrough(self):
        rec = self.pipe.run(
            "I have epilepsy and take carbamazepine, had a seizure "
            "yesterday morning, first one in two years", {})
        assert _ids(rec) & {"epilepsy_established"}
        assert rec.escalation in ("urgent", "routine")


class TestMentalHealthBreadth:
    pipe = ConsultationPipeline()

    def test_mania_probe_answered(self):
        rec = self.pipe.run(
            "haven't slept for three nights, talking fast, spending money "
            "wildly, feeling invincible", {})
        assert rec.escalation == "urgent", rec.problem_representation
        assert _ids(rec) & {"bipolar_mania"}

    def test_mania_lists_psychosis_red_flag(self):
        c = find_condition("bipolar_mania")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "psychos" in blob or "delusion" in blob

    def test_ocd_leads(self):
        rec = self.pipe.run(
            "washing my hands fifty times a day and checking the locks for "
            "an hour before I can leave, I know it's silly but I can't stop",
            {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "ocd" in ranked[:2], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_ptsd_leads(self):
        rec = self.pipe.run(
            "nightmares and flashbacks since the car crash three months "
            "ago, jumping at loud noises, avoiding the motorway", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "ptsd" in ranked[:2], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_eupd_present_with_self_harm_red_flag(self):
        c = find_condition("eupd")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "self-harm" in blob or "self harm" in blob or "suicid" in blob

    def test_bulimia_present(self):
        rec = self.pipe.run(
            "making myself sick after meals for a year, worried about my "
            "weight, eat huge amounts then panic", {})
        assert _ids(rec) & {"bulimia_nervosa"}

    def test_perinatal_mh_flagged(self):
        rec = self.pipe.run(
            "four weeks since the baby was born, can't sleep even when she "
            "sleeps, tearful all the time, frightening thoughts about "
            "harming the baby", {})
        assert _ids(rec) & {"perinatal_mental_health"}
        assert rec.escalation in ("urgent", "emergency")


class TestOverTriageGuards7_1:
    """Breadth must not turn ordinary life into referrals."""

    pipe = ConsultationPipeline()

    def test_occasional_forgetfulness_is_not_dementia(self):
        rec = self.pipe.run(
            "I forgot where I put my keys this morning, otherwise fine, "
            "I'm 70", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["dementia_suspected"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_simple_faint_is_not_first_seizure(self):
        rec = self.pipe.run(
            "felt faint and blacked out briefly when I stood up too fast, "
            "back to normal within seconds", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "first_seizure_adult" not in ranked[:2], ranked[:3]
        assert rec.escalation != "emergency"

    def test_normal_sleepless_new_parent_not_urgent_mania(self):
        # sleep deprivation alone must not trip the mania entry
        rec = self.pipe.run(
            "exhausted, up every two hours with the baby, sleeping badly "
            "for a month", {})
        assert "bipolar_mania" not in _ids(rec) or \
            [d["condition_id"] for d in rec.ranked_differential][0] != \
            "bipolar_mania"

    def test_single_headache_at_night_is_not_cluster_led(self):
        rec = self.pipe.run(
            "mild headache last night, fine today, no other symptoms", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["cluster_headache"], ranked[:3]


class TestDermatologyBreadth:
    """Task 7.2: the derm gap the audit called out — acne, urticaria,
    scabies and tinea once returned chickenpox/eczema/strongyloides
    leaders; a leg ulcer probe once led with dementia."""

    pipe = ConsultationPipeline()

    def test_acne_leads_and_does_not_escalate(self):
        rec = self.pipe.run(
            "spotty rash on my face and back since I was a teenager, "
            "greasy skin", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["acne_vulgaris"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_acne_mentions_pcos_link_for_women(self):
        c = find_condition("acne_vulgaris")
        blob = " ".join(c.discriminators + c.red_flags).lower()
        assert "pcos" in blob or "polycystic" in blob

    def test_chronic_urticaria_leads(self):
        rec = self.pipe.run(
            "itchy weals coming up all over for six weeks, coming and "
            "going", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["urticaria_chronic"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_urticaria_carries_airway_red_flag(self):
        c = find_condition("urticaria_chronic")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "breath" in blob or "airway" in blob or "999" in blob

    def test_scabies_leads_on_family_itch(self):
        rec = self.pipe.run(
            "itchy at night, whole family scratching, little burrow "
            "tracks between the fingers", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["scabies"], ranked[:3]

    def test_tinea_leads_on_ring_shape(self):
        rec = self.pipe.run(
            "ring-shaped itchy patch in the groin and between the toes",
            {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["tinea_corporis"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_drug_eruption_leads_when_otherwise_well(self):
        rec = self.pipe.run(
            "blistered rash on my arms a week after starting "
            "antibiotics, otherwise well", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["drug_eruption"], ranked[:3]
        assert rec.escalation in ("routine", "urgent")

    def test_sjs_still_wins_over_drug_eruption_on_mucosal_signs(self):
        """The drug_eruption entry must never displace SJS/TEN on the
        mucosal presentation — regression guard for this task."""
        rec = self.pipe.run(
            "started lamotrigine two weeks ago, now a rash with sore "
            "blistered lips and eyes, skin hurts", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[0] == "stevens_johnson_ten", ranked[:3]
        assert rec.escalation == "emergency"

    def test_venous_leg_ulcer_leads(self):
        rec = self.pipe.run(
            "grazing sore above the ankle that never heals, swollen "
            "varicose legs for months", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["venous_leg_ulcer"], ranked[:3]

    def test_leg_ulcer_carries_cancer_edge_red_flag(self):
        c = find_condition("venous_leg_ulcer")
        blob = " ".join(c.red_flags).lower()
        assert "edge" in blob or "cancer" in blob or "2ww" in blob

    def test_seborrhoeic_dermatitis_leads(self):
        rec = self.pipe.run(
            "flaky red rash in my eyebrows and around my nose, mild "
            "itch", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["seborrhoeic_dermatitis"], ranked[:3]


class TestWomensHealthBreadth:
    pipe = ConsultationPipeline()

    def test_menopause_leads_not_anxiety(self):
        rec = self.pipe.run(
            "I'm 52, periods stopped a year ago, hot flushes and night "
            "sweats, finding it hard to concentrate", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["menopause"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_menopause_carries_pmb_red_flag(self):
        c = find_condition("menopause")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "postmenopausal" in blob or "after the periods stopped" \
            in blob or "any bleeding" in blob

    def test_pcos_leads_on_the_classic_triad(self):
        rec = self.pipe.run(
            "trying for a baby for two years, periods come every three "
            "months, put on weight, hairs on my chin", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "pcos" in ranked[:2], ranked[:3]
        assert _ids(rec) & {"subfertility"}
        assert rec.escalation in ("routine", "urgent")

    def test_dysmenorrhoea_leads(self):
        rec = self.pipe.run(
            "my periods are agony every month, first day especially, "
            "no other problems", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["dysmenorrhoea"], ranked[:3]

    def test_dysmenorrhoea_names_endometriosis(self):
        c = find_condition("dysmenorrhoea")
        blob = " ".join(c.discriminators + c.red_flags).lower()
        assert "endometriosis" in blob


class TestMensHealthBreadth:
    pipe = ConsultationPipeline()

    def test_ed_leads(self):
        rec = self.pipe.run(
            "difficulty getting erections for six months, still get "
            "early morning erections", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["erectile_dysfunction"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_ed_carries_cardiovascular_red_flag(self):
        c = find_condition("erectile_dysfunction")
        blob = " ".join(c.red_flags + c.discriminators).lower()
        assert "cardiovascular" in blob or "heart" in blob or \
            "vascular" in blob

    def test_bph_leads(self):
        rec = self.pipe.run(
            "up three times a night to pass urine, weak stream, 68 "
            "year old man", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["benign_prostatic_hyperplasia"], ranked[:3]
        assert rec.escalation in ("routine", "urgent")

    def test_testicular_cancer_is_2ww(self):
        rec = self.pipe.run(
            "dull ache in one testicle for two months, felt a hard "
            "lump, 34 year old smoker", {})
        assert _ids(rec) & {"testicular_cancer_suspect"}
        assert find_condition("testicular_cancer_suspect").referral_tier \
            == "two_week_wait"
        assert rec.escalation != "emergency"

    def test_prostatitis_is_urgent(self):
        rec = self.pipe.run(
            "burning when I pass water and deep pelvic ache for a "
            "week, 45 year old man, mild fever", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["prostatitis"], ranked[:3]
        assert rec.escalation == "urgent"


class TestOverTriageGuards7_2:
    pipe = ConsultationPipeline()

    def test_young_woman_headaches_not_menopause(self):
        rec = self.pipe.run(
            "I'm 30 with headaches, on the pill, periods normal", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["menopause"], ranked[:3]

    def test_simple_insect_bites_not_scabies(self):
        rec = self.pipe.run(
            "a few itchy bumps on my arm after gardening, fine "
            "otherwise", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["scabies"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_acute_testicular_pain_stays_torsion_territory(self):
        """The chronic-cancer entry must not soften the acute story."""
        rec = self.pipe.run(
            "sudden severe pain in one testicle three hours ago, "
            "swollen and tender, vomiting", {})
        assert rec.escalation == "emergency"
        assert "testicular_torsion" in _ids(rec)


class TestChronicGIRenal:
    """Task 7.3: chronic GI, hepatology and renal — the probes that
    exposed the gaps returned EMPTY (constipation, hernia) or absurd
    leaders (CKD-4 story -> eczema/chickenpox; coeliac ->
    gastroenteritis; Crohn's -> gastroenteritis)."""

    pipe = ConsultationPipeline()

    def test_constipation_leads(self):
        rec = self.pipe.run(
            "haven't opened my bowels for nine days, tummy is "
            "uncomfortable, hard stools", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["constipation_simple"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_constipation_names_obstruction_red_flag(self):
        c = find_condition("constipation_simple")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "vomit" in blob or "obstruction" in blob

    def test_uc_leads_on_chronic_bloody_diarrhoea(self):
        rec = self.pipe.run(
            "diarrhoea with blood and mucous for six weeks, waking me "
            "at night, rushing to the toilet", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "ulcerative_colitis_suspect" in ranked[:2], ranked[:3]
        assert rec.escalation == "urgent"

    def test_uc_names_toxic_megacolon_risk(self):
        c = find_condition("ulcerative_colitis_suspect")
        blob = " ".join(c.red_flags).lower()
        assert "toxic" in blob or "six stools" in blob or \
            "admission" in blob

    def test_crohns_leads_on_the_gnawing_picture(self):
        rec = self.pipe.run(
            "mouth ulcers, crampy tummy pain, diarrhoea for months, "
            "losing weight", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "crohns_disease_suspect" in ranked[:2], ranked[:3]
        assert rec.escalation in ("urgent", "routine")

    def test_coeliac_leads_on_wheat_trigger(self):
        rec = self.pipe.run(
            "bloated and diarrhoea every time I eat bread or pasta, "
            "tired all the time", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "coeliac_disease" in ranked[:2], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_coeliac_mentions_serology_on_gluten(self):
        c = find_condition("coeliac_disease")
        blob = " ".join(i.name for i in c.investigations).lower()
        assert "serology" in blob or "gluten" in blob

    def test_decompensated_cirrhosis_is_urgent(self):
        rec = self.pipe.run(
            "my husband has cirrhosis, now confused, turned yellow "
            "and his tummy is swelling", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "cirrhosis_decompensated" in ranked[:2], ranked[:3]
        assert rec.escalation == "urgent"

    def test_advanced_ckd_leads_when_known(self):
        rec = self.pipe.run(
            "known kidney disease, stage four, tired, itchy skin, "
            "nauseated, ankles swollen", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["ckd_advanced"], ranked[:3]

    def test_inguinal_hernia_leads(self):
        rec = self.pipe.run(
            "bulge in my groin that comes and goes, aches after "
            "lifting", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["inguinal_hernia"], ranked[:3]

    def test_hernia_names_strangulation_red_flag(self):
        c = find_condition("inguinal_hernia")
        blob = " ".join(c.red_flags + [c.safety_net]).lower()
        assert "strangulat" in blob or "tender" in blob or \
            "vomit" in blob


class TestEyesENTBreadth:
    """Task 7.3: wet AMD and sudden sensorineural hearing loss both
    returned EMPTY; the SNHL story once led with addisonian crisis."""

    pipe = ConsultationPipeline()

    def test_wet_amd_leads_on_distortion(self):
        rec = self.pipe.run(
            "straight lines look wobbly in one eye, been a month, "
            "reading is hard", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["wet_amd"], ranked[:3]
        assert rec.escalation == "urgent"

    def test_amd_names_rapid_referral_need(self):
        c = find_condition("wet_amd")
        blob = " ".join(c.management_first_line.split()).lower()
        assert "week" in blob or "urgent" in blob or "clinic" in blob

    def test_sudden_hearing_loss_is_urgent(self):
        rec = self.pipe.run(
            "lost the hearing in my right ear overnight three days "
            "ago, some dizziness", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "sudden_sensorineural_hearing_loss" in ranked[:2], \
            ranked[:3]
        assert rec.escalation == "urgent"

    def test_wax_deafness_does_not_fire_sudden_loss(self):
        rec = self.pipe.run(
            "my ear feels blocked, deafness for weeks after a cold, "
            "no pain", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["sudden_sensorineural_hearing_loss"], \
            ranked[:3]

    def test_orbital_cellulitis_is_emergency(self):
        c = find_condition("orbital_cellulitis")
        assert c.referral_tier == "emergency"
        rec = self.pipe.run(
            "swollen red painful eye around the eyelid, double "
            "vision, fever", {})
        assert rec.escalation == "emergency"
        assert "orbital_cellulitis" in _ids(rec)

    def test_stye_does_not_become_orbital_cellulitis(self):
        rec = self.pipe.run(
            "a stye on my eyelid, little lump along the lashes, "
            "slightly red, otherwise fine", {})
        assert rec.escalation in ("routine", "self_care")
        assert "orbital_cellulitis" not in {
            d["condition_id"] for d in rec.ranked_differential}


class TestSleepPainContinence:
    """Task 7.3: OSA once led with OBSTRUCTED LABOUR; stress
    incontinence with covid/TB; insomnia with dementia."""

    pipe = ConsultationPipeline()

    def test_osa_leads(self):
        rec = self.pipe.run(
            "snoring terribly, exhausted in the day, falling asleep "
            "at the wheel", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["obstructive_sleep_apnoea"], ranked[:3]
        assert rec.escalation in ("routine", "urgent")

    def test_osa_names_driving_stop(self):
        c = find_condition("obstructive_sleep_apnoea")
        blob = " ".join(c.red_flags + [c.management_first_line,
                                       c.safety_net]).lower()
        assert "driving" in blob or "dvla" in blob

    def test_insomnia_leads_not_dementia(self):
        rec = self.pipe.run(
            "can't sleep at all for months, worrying about work, "
            "lying awake", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["insomnia_disorder"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")

    def test_chronic_pain_frame_present(self):
        rec = self.pipe.run(
            "constant back pain for years, nothing helps any more, "
            "can't work", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert "chronic_primary_pain" in ranked[:2], ranked[:3]

    def test_chronic_pain_carries_red_flag_screen(self):
        c = find_condition("chronic_primary_pain")
        blob = " ".join(c.red_flags).lower()
        assert "weight loss" in blob or "night pain" in blob or \
            "cancer" in blob

    def test_neuropathic_pain_leads(self):
        rec = self.pipe.run(
            "burning stabbing pain in my shoulder like electric "
            "shocks, even clothes hurt against it", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["neuropathic_pain"], ranked[:3]

    def test_stress_incontinence_leads(self):
        rec = self.pipe.run(
            "leaking urine when I cough, sneeze or exercise, had "
            "three children", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] == ["stress_incontinence"], ranked[:3]
        assert rec.escalation in ("routine", "self_care")


class TestOverTriageGuards7_3:
    pipe = ConsultationPipeline()

    def test_tiredness_not_ckd_led_without_kidney_context(self):
        rec = self.pipe.run(
            "tired all the time for six months, bloods normal last "
            "year", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["ckd_advanced"], ranked[:3]

    def test_viral_diarrhoea_not_uc_led(self):
        rec = self.pipe.run(
            "loose stools and vomiting since last night after a "
            "takeaway", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["ulcerative_colitis_suspect"], ranked[:3]
        assert rec.escalation in ("routine", "self_care", "urgent")

    def test_snoring_without_sleepiness_not_osa_led(self):
        rec = self.pipe.run(
            "my wife says I snore, sleeping fine, full of energy", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["obstructive_sleep_apnoea"], ranked[:3]

    def test_acute_back_pain_not_chronic_pain_led(self):
        rec = self.pipe.run(
            "lifted a box badly yesterday, back pain since, worst "
            "today", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["chronic_primary_pain"], ranked[:3]

    def test_migraine_aura_not_amd_led(self):
        rec = self.pipe.run(
            "my migraines start with zigzag lines in both eyes for "
            "twenty minutes then the headache", {})
        ranked = [d["condition_id"] for d in rec.ranked_differential]
        assert ranked[:1] != ["wet_amd"], ranked[:3]
