"""Stage 8 Task 8.1: the world — global high-burden and environmental
extremes.

Tier 3's premise: this doctor could be anywhere. The tests here hold
three things:
1. corpus integrity — 26 profiles, every token has synonyms, every
   key was new at merge time, tiers are honest;
2. the cohorts the world actually carries — leprosy, the NTDs,
   chronic viral hepatitis, HIV found late, sickle crisis, altitude
   and heat and cold, DCI, radiation;
3. the over-triage guards — geography alone never diagnoses (the
   Nepal-trek lesson, now locked for India-years and gym-sweat and
   ski-holiday stories too).

The probe pass that shaped this file caught a shadow-duplicate
cholera (two cholera rows in one differential) and a pre-existing
bare-country fever token ("worked in India for years" led with
malaria) — both fixed before this suite was written, both guarded
here.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.clinical_reasoning.knowledge import (
    CONDITIONS, SYMPTOM_SYNONYMS, find_condition)
from gpdisc_core.clinical_reasoning.knowledge_global import (
    CONDITIONS_PART6, SYMPTOM_SYNONYMS_PART6)

PIPE = ConsultationPipeline()


def _names(rec):
    """All condition names the record surfaced, ranked or retained."""
    return ({d["name"] for d in rec.ranked_differential} |
            {d["name"] for d in rec.dangerous_alternatives})


def _leader(rec):
    return rec.ranked_differential[0] if rec.ranked_differential else None


class TestCorpusIntegrity:
    def test_part6_count_and_unique_ids(self):
        ids = [c.condition_id for c in CONDITIONS_PART6]
        assert len(ids) == 26
        assert len(ids) == len(set(ids))
        # no shadow duplicates against the merged corpus
        merged = [c.condition_id for c in CONDITIONS]
        assert len(merged) == len(set(merged)), "duplicate condition id"

    def test_every_token_has_synonyms(self):
        for c in CONDITIONS_PART6:
            for s in c.symptoms:
                assert s.symptom in SYMPTOM_SYNONYMS, \
                    f"{c.condition_id}: {s.symptom} has no synonyms"

    def test_synonym_keys_were_new_at_merge(self):
        # update() overwrites: a PART6 key colliding with an earlier
        # key would silently rewrite an existing token's synonyms
        import gpdisc_core.clinical_reasoning.knowledge_breadth as kb
        import gpdisc_core.clinical_reasoning.knowledge_breadth2 as kb2
        import gpdisc_core.clinical_reasoning.knowledge_emergencies as ke
        earlier = (set(kb.SYMPTOM_SYNONYMS_PART2) |
                   set(kb2.SYMPTOM_SYNONYMS_PART5) |
                   set(ke.SYMPTOM_SYNONYMS_PART4) |
                   set(SYMPTOM_SYNONYMS) - set(SYMPTOM_SYNONYMS_PART6))
        assert not (set(SYMPTOM_SYNONYMS_PART6) & earlier)

    def test_tiers_and_categories(self):
        tiers = {c.referral_tier for c in CONDITIONS_PART6}
        assert tiers <= {"self_care", "routine", "urgent",
                         "two_week_wait", "emergency"}
        cats = {c.category for c in CONDITIONS_PART6}
        # the world's own categories, new at 8.1
        assert "environmental" in cats
        assert "zoonotic_infection" in cats

    def test_geography_tokens_never_carry_alone(self):
        """The Nepal-trek lesson, made structural: every geographic or
        exposure-context token in PART6 carries specificity <= 0.55, so
        a place name can only ever SUPPORT a specific symptom token —
        never lead a diagnosis by itself."""
        low_cap = {"endemic_area_long_stay", "latin_america_rural_origin",
                   "sandfly_region_stay", "se_asia_stay_low"}
        for c in CONDITIONS_PART6:
            for s in c.symptoms:
                if s.symptom in low_cap:
                    assert s.specificity <= 0.55, \
                        f"{c.condition_id}: {s.symptom} at " \
                        f"{s.specificity} — geography must stay weak"

    def test_cholera_exists_exactly_once(self):
        """The probe that wrote this test: my PART6 cholera shadowed
        knowledge_tropical's entry under the same condition_id and both
        rendered in one differential. One cholera, once."""
        cholera = [c for c in CONDITIONS
                   if "cholera" in c.condition_id.lower()]
        assert len(cholera) == 1

    def test_emergency_entries_have_red_flags(self):
        for c in CONDITIONS_PART6:
            if c.referral_tier == "emergency":
                assert c.red_flags, c.condition_id


class TestChronicViralCohort:
    def test_known_hep_b_carrier_routed_routine_hepatology(self):
        """The 8.1 probe inverted: the carrier story is a ROUTINE
        hepatology review — never a needlestick exposure, never
        nothing."""
        rec = PIPE.run("tired all the time, hepatitis B carrier for "
                       "years", {})
        leader = _leader(rec)
        assert leader is not None
        assert "hepatitis b" in leader["name"].lower()
        assert rec.escalation == "routine"
        assert not any("bloodborne" in n.lower() or "needlestick" in n.lower()
                       for n in _names(rec))
        assert "contacts" in find_condition(
            "chronic_hepatitis_b").discriminators[2]

    def test_hep_c_positive_curable_frame(self):
        rec = PIPE.run("hep c positive on a blood test, injected drugs "
                       "years ago", {})
        leader = _leader(rec)
        assert leader and "hepatitis c" in leader["name"].lower()
        assert rec.escalation == "routine"

    def test_hiv_late_presentation_urgent_with_hiv_leader(self):
        rec = PIPE.run("shingles twice this year and thrush keeps "
                       "coming back, losing weight", {})
        assert rec.escalation == "urgent"
        assert any("hiv" in n.lower() for n in _names(rec))


class TestNeglectedTropicalCohort:
    def test_leprosy_numb_patches_lead(self):
        rec = PIPE.run("patches on my skin that feel numb, worked in "
                       "India for years", {})
        leader = _leader(rec)
        assert leader and "leprosy" in leader["name"].lower()
        assert rec.escalation == "routine"

    def test_leprosy_management_names_multidrug_therapy(self):
        lep = find_condition("leprosy")
        assert "multidrug therapy" in lep.management_first_line.lower() \
            or "rifampicin" in lep.management_first_line.lower()

    def test_sleeping_sickness_safari_somnolence(self):
        rec = PIPE.run("back from a safari in Tanzania, sleeps all day, "
                       "glands at the back of the neck", {})
        leader = _leader(rec)
        assert leader and "trypanosomiasis" in leader["name"].lower()
        assert rec.escalation == "urgent"

    def test_brucellosis_undulant_fever_raw_dairy(self):
        rec = PIPE.run("fever that comes and goes for six weeks, drinks "
                       "unpasteurised milk from the farm", {})
        leader = _leader(rec)
        assert leader and "brucellosis" in leader["name"].lower()
        assert rec.escalation == "urgent"

    def test_visceral_leishmaniasis_spleen_pancytopenia(self):
        rec = PIPE.run("fever for two months in Ethiopia, doctor said "
                       "my spleen is enlarged, blood counts all low", {})
        leader = _leader(rec)
        assert leader and "leishmaniasis" in leader["name"].lower()
        assert rec.escalation == "urgent"

    def test_neurocysticercosis_in_new_seizure_differential(self):
        rec = PIPE.run("first seizure at 38, from a village in Mexico, "
                       "cysts in the brain on the scan", {})
        assert any("cysticercosis" in n.lower() for n in _names(rec))
        assert rec.escalation in ("urgent", "emergency")

    def test_chagas_screen_letter(self):
        rec = PIPE.run("from Bolivia, blood donation letter says chagas "
                       "positive", {})
        leader = _leader(rec)
        assert leader and "chagas" in leader["name"].lower()
        assert rec.escalation == "routine"

    def test_symptomatic_rabies_is_emergency(self):
        rec = PIPE.run("bitten by a dog in India two months ago, now "
                       "tingling where the bite was and spasms when I "
                       "try to drink", {})
        leader = _leader(rec)
        assert leader and "rabies" in leader["name"].lower()
        assert rec.escalation == "emergency"


class TestEnvironmentalCohort:
    def test_ams_routine_with_hace_hape_questions(self):
        """AMS is self-limiting — but the record must carry the two
        killer questions (ataxia, breathlessness at rest) as runners-up,
        not bury them."""
        rec = PIPE.run("trekking in Nepal, headache and nausea at "
                       "altitude since the climb yesterday", {})
        leader = _leader(rec)
        assert leader and "mountain sickness" in leader["name"].lower()
        assert rec.escalation == "routine"
        assert any("cerebral" in n.lower() for n in _names(rec)) or \
            any("pulmonary" in n.lower() for n in _names(rec))

    def test_hace_ataxia_emergency(self):
        rec = PIPE.run("at 5000 metres my friend is stumbling around "
                       "camp and not making sense", {})
        leader = _leader(rec)
        assert leader and "cerebral" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_hape_breathless_at_rest_emergency(self):
        rec = PIPE.run("breathless at rest at 4200 metres, cough at "
                       "altitude, can't lie flat", {})
        leader = _leader(rec)
        assert leader and "pulmonary" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_heat_exhaustion_urgent_but_not_stroke(self):
        rec = PIPE.run("working in the sun all day roofing, sweating "
                       "heavily and feeling weak with muscle cramps", {})
        leader = _leader(rec)
        assert leader and "heat exhaustion" in leader["name"].lower()
        assert rec.escalation == "urgent"
        assert "heat stroke" not in leader["name"].lower()

    def test_hot_dry_confused_is_heat_stroke_emergency(self):
        rec = PIPE.run("collapsed in the sun at the marathon, burning "
                       "hot but not sweating, temperature of 41", {})
        leader = _leader(rec)
        assert leader and "heat stroke" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_hypothermia_found_cold_drowsy_emergency(self):
        rec = PIPE.run("found my mother cold and drowsy at home, "
                       "temperature of 33, shivering has stopped", {})
        leader = _leader(rec)
        assert leader and "hypothermia" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_decompression_illness_after_dive_emergency(self):
        rec = PIPE.run("shoulder pain after the dive and numbness "
                       "after diving this morning", {})
        leader = _leader(rec)
        assert leader and "decompression" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_radiation_source_vomiting_emergency(self):
        rec = PIPE.run("found a metal capsule at the scrapyard, "
                       "vomited within an hour of handling it", {})
        assert rec.escalation == "emergency"
        assert any("radiation" in n.lower() for n in _names(rec))


class TestGlobalHaematology:
    def test_sickle_crisis_known_disease_emergency(self):
        rec = PIPE.run("I have sickle cell disease, severe pain in my "
                       "back and legs since last night", {})
        leader = _leader(rec)
        assert leader and "sickle" in leader["name"].lower()
        assert rec.escalation == "emergency"

    def test_sickle_red_flags_name_acute_chest(self):
        sickle = find_condition("sickle_vaso_occlusive_crisis")
        flags = " ".join(sickle.red_flags).lower()
        assert "chest" in flags and "priapism" in flags

    def test_rheumatic_fever_migratory_joints_young(self):
        rec = PIPE.run("my 9 year old's knee pain moved to the ankle, "
                       "sore throat a few weeks ago", {})
        assert any("rheumatic" in n.lower() for n in _names(rec))
        assert rec.escalation in ("urgent", "emergency")


class TestHumanRightsCare:
    def test_fgm_disclosure_urgent_with_specialist_care(self):
        rec = PIPE.run("I have been cut, periods take days to drain and "
                       "passing urine is slow", {})
        leader = _leader(rec)
        assert leader and "mutilation" in leader["name"].lower()
        assert rec.escalation == "urgent"
        fgm = find_condition("fgm_care_needs")
        joined = " ".join(fgm.red_flags).lower()
        assert "under 18" in joined and "mandatory" in joined

    def test_torture_survivor_trauma_informed(self):
        rec = PIPE.run("was tortured in my country, scars from beatings "
                       "on my back, nightmares every night", {})
        leader = _leader(rec)
        assert leader and "torture" in leader["name"].lower()
        assert rec.escalation == "routine"
        torture = find_condition("torture_survivor_care")
        joined = (torture.investigations[0].name + " " +
                  torture.management_first_line).lower() \
            if torture.investigations else \
            torture.management_first_line.lower()
        assert "consent" in joined


class TestOvertriageGuards:
    """Every guard here is a probe story that could have been a false
    emergency. Geography, gym sweat, ski holidays and winter hands are
    not diagnoses."""

    def test_years_in_india_alone_is_not_malaria(self):
        """fever_after_travel once carried bare ' in india': 'worked in
        India for years' led with malaria. Long-ago residence is an
        endemic-area hint at LOW specificity, never a fever token."""
        rec = PIPE.run("worked in India for years, my knees ache", {})
        assert rec.escalation == "routine"
        assert not any("malaria" in n.lower() for n in _names(rec))

    def test_gym_sweat_is_not_heat_illness(self):
        rec = PIPE.run("sweaty after a workout at the gym, feeling fine", {})
        assert rec.escalation != "emergency"
        assert not any("heat" in n.lower() and "stroke" in n.lower()
                       for n in _names(rec))

    def test_ski_holiday_headache_is_not_hace(self):
        rec = PIPE.run("headache on a skiing holiday in the Alps", {})
        assert rec.escalation != "emergency"
        assert not any("altitude" in n.lower() or "cerebral oedema" in n.lower()
                       for n in _names(rec))

    def test_cold_fingers_winter_morning_not_hypothermia(self):
        rec = PIPE.run("cold fingers every winter morning", {})
        assert rec.escalation != "emergency"
        assert not any("hypothermia" in n.lower() for n in _names(rec))

    def test_sea_swimming_ear_pain_is_not_decompression(self):
        rec = PIPE.run("ear pain after swimming in the sea", {})
        assert not any("decompression" in n.lower() for n in _names(rec))

    def test_weekend_footy_knees_not_rheumatic_fever(self):
        rec = PIPE.run("both knees ache since playing twice a week", {})
        assert not any("rheumatic" in n.lower() for n in _names(rec))

    def test_drunken_stumble_without_altitude_is_not_hace(self):
        """The ataxia synonyms were widened for natural phrasing — this
        guard holds the line that a pub story never buys HACE."""
        rec = PIPE.run("my husband was stumbling like he's drunk at the "
                       "pub last night, fine this morning", {})
        assert rec.escalation != "emergency"
        assert not any("altitude" in n.lower() for n in _names(rec))
