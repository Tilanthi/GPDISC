"""Tests for uk_practice (expertise program Stage 3)."""
import pytest
from gpdisc_core.uk_practice.guidelines_index import (
    GUIDELINES, GuidelineRef, lookup_guideline,
)


class TestGuidelinesIndex:
    def test_24_entries(self):
        # 26 since the audit fix: NG198 acne and CG97 LUTS-in-men rows
        # added so the validator can ground the corpus's own (corrected)
        # citations instead of flagging them as unknown numbers.
        assert len(GUIDELINES) == 26

    def test_every_entry_populated(self):
        for g in GUIDELINES:
            assert g.topic and g.nice_ref and g.cks_topic

    def test_lookup_chest_pain(self):
        hits = lookup_guideline("patient with chest pain")
        assert any(g.nice_ref == "NICE CG95" for g in hits)

    def test_lookup_diabetes_matches_both(self):
        hits = lookup_guideline("newly diagnosed type 2 diabetes")
        assert any(g.topic == "type 2 diabetes" for g in hits)

    def test_no_hit_empty(self):
        assert lookup_guideline("moon rocks") == []


from gpdisc_core.uk_practice.two_week_wait import (
    TWO_WEEK_WAIT_RULES, two_week_wait_check,
)


class TestTwoWeekWait:
    def test_16_rules(self):
        assert len(TWO_WEEK_WAIT_RULES) == 16
        for r in TWO_WEEK_WAIT_RULES:
            assert r.cancer_site and r.trigger and r.action

    def test_haemoptysis_age_46_lung(self):
        hits = two_week_wait_check("coughing up blood for a week", age=46)
        assert any(r.cancer_site == "lung" for r in hits)

    def test_haemoptysis_age_30_no_lung_rule(self):
        hits = two_week_wait_check("coughing up blood", age=30)
        assert not any(r.cancer_site == "lung" for r in hits)

    def test_dysphagia_any_age(self):
        hits = two_week_wait_check("food sticking when I swallow", age=28)
        assert any(r.cancer_site == "oesophago_gastric" for r in hits)

    def test_ovarian_sex_filtered(self):
        hits = two_week_wait_check("persistent bloating and early satiety",
                                   age=62, sex="f")
        assert any(r.cancer_site == "ovarian" for r in hits)
        hits_m = two_week_wait_check("persistent bloating and early satiety",
                                     age=62, sex="m")
        assert not any(r.cancer_site == "ovarian" for r in hits_m)

    def test_breast_lump_over_30(self):
        hits = two_week_wait_check("found a breast lump", age=41, sex="f")
        assert any(r.cancer_site == "breast" for r in hits)


from gpdisc_core.uk_practice.dvla_rules import DRIVING_RULES, driving_rules


class TestDVLARules:
    def test_14_rules(self):
        assert len(DRIVING_RULES) == 14

    def test_seizure_rule_found(self):
        hits = driving_rules("patient had a first seizure last week")
        assert hits and "seizure" in hits[0].condition.lower()

    def test_insulin_group2_stricter(self):
        g1 = driving_rules("diabetes on insulin", group=1)
        g2 = driving_rules("diabetes on insulin", group=2)
        assert "3-year" in g1[0].group1_rule or "3 year" in g1[0].group1_rule
        assert "Annual" in g2[0].group2_rule

    def test_unknown_empty(self):
        assert driving_rules("sprained ankle") == []


from gpdisc_core.uk_practice.capacity_and_safeguarding import (
    capacity_two_stage_test, best_interests_checklist, dnacpr_principles,
    safeguarding_adult_types, safeguarding_children_levels, gillick_checklist,
    capacity_concern_keywords,
)


class TestCapacitySafeguarding:
    def test_capacity_two_stage(self):
        stages = capacity_two_stage_test()
        assert any("Stage 1" in s for s in stages)
        assert any("Stage 2" in s for s in stages)
        assert any("decision-specific" in s for s in stages)

    def test_best_interests_items(self):
        ci = best_interests_checklist()
        assert any("least restrictive" in s.lower() for s in ci)
        assert any("IMCA" in s for s in ci)

    def test_dnacpr_scope_limited_to_cpr(self):
        assert any("CPR only" in p or "CPR ONLY" in p for p in dnacpr_principles())

    def test_ten_adult_abuse_types(self):
        assert len(safeguarding_adult_types()) == 10

    def test_children_levels(self):
        lv = safeguarding_children_levels()
        assert [x["level"] for x in lv] == [1, 2, 3, 4]
        assert "significant harm" in lv[3]["detail"].lower()

    def test_gillick_five(self):
        assert len(gillick_checklist()) == 5

    def test_concern_keywords(self):
        hits = capacity_concern_keywords("daughter always answers for him "
                                         "and checks her phone")
        assert "undue_influence" in hits and "coercive_control" in hits


from gpdisc_core.uk_practice.controlled_drugs import (
    controlled_drug_class, prescribing_guardrails, CD_SCHEDULES, CD_SAFE_PRACTICE,
)


class TestControlledDrugs:
    def test_schedule_lookup(self):
        assert controlled_drug_class("morphine") == "2"
        assert controlled_drug_class("diazepam") == "4"
        assert controlled_drug_class("codeine 30mg") == ""  # plain tablets are not CDs

    def test_fentanyl_patch_guardrail(self):
        g = prescribing_guardrails("fentanyl_patch")
        assert any("opioid-naïve" in x or "opioid-naive" in x for x in g)

    def test_benzo_ceiling(self):
        g = prescribing_guardrails("diazepam")
        assert any("2-4 weeks" in x for x in g)

    def test_unknown_drug_empty(self):
        assert prescribing_guardrails("paracetamol") == []

    def test_safe_practice_nonempty(self):
        assert len(CD_SAFE_PRACTICE) >= 5

    def test_audit_corrected_schedules(self):
        # Locked 2026-09-04 hallucination-audit corrections:
        # midazolam/tramadol are Schedule 3; medicinal diamorphine is
        # Schedule 2 (never 1); temazepam Schedule 4 (the old Schedule 3
        # note string used to hijack this substring lookup).
        assert controlled_drug_class("midazolam") == "3"
        assert controlled_drug_class("tramadol") == "3"
        assert controlled_drug_class("diamorphine") == "2"
        assert controlled_drug_class("temazepam") == "4"

    def test_audit_corrected_dvla(self):
        # DVLA guide (Nov 2025): group 2 after stroke/TIA = 1-year
        # revocation; elective PCI group 1 = 1 week; unexplained syncope
        # group 1 = 6 months.
        g2 = driving_rules("tia", group=2)[0].group2_rule
        assert "1 year" in g2
        pci = driving_rules("angioplasty", group=1)[0].group1_rule
        assert "1 week" in pci
        syn = driving_rules("syncope", group=1)[0].group1_rule
        assert "6 months" in syn


from gpdisc_core.uk_practice.antimicrobial_stewardship import (
    ANTIBIOTIC_GUIDANCE, AntibioticGuidance, antibiotic_for, stewardship_principles,
)


class TestStewardship:
    def test_12_infections(self):
        assert len(ANTIBIOTIC_GUIDANCE) == 12

    def test_sore_throat_feverpain(self):
        hits = antibiotic_for("sore throat score 4")
        assert hits and "FeverPAIN" in (hits[0].first_line + hits[0].delayed_note)

    def test_penicillin_allergy_changes_answer(self):
        plain = antibiotic_for("cellulitis of the leg")
        allergic = antibiotic_for("cellulitis of the leg", penicillin_allergy=True)
        assert plain[0].first_line == "Flucloxacillin"
        assert "Clarithromycin" in allergic[0].penicillin_allergic

    def test_womens_uti_3_days(self):
        hits = antibiotic_for("cystitis symptoms for two days, woman")
        assert any("3 days" in h.duration for h in hits)

    def test_principles_include_review(self):
        assert any("48" in p for p in stewardship_principles())


from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements, renal_flags, MONITORING,
)


class TestPrescribingSafety:
    def test_methotrexate_never_daily(self):
        m = monitoring_requirements("methotrexate")
        assert any("NEVER daily" in x or "weekly" in x.lower() for x in m)

    def test_lithium_interactions(self):
        m = monitoring_requirements("lithium")
        assert any("NSAID" in x for x in m)

    def test_unknown_drug_empty(self):
        assert monitoring_requirements("paracetamol") == []

    def test_metformin_egfr_25_stops(self):
        flags = renal_flags("metformin", egfr=25)
        assert any("STOP" in f for f in flags)

    def test_metformin_egfr_50_clean(self):
        assert renal_flags("metformin", egfr=50) == []

    def test_nitrofurantoin_egfr_40_avoid(self):
        flags = renal_flags("nitrofurantoin", egfr=40)
        assert any("45" in f for f in flags)

    def test_ten_drugs_monitored(self):
        assert len(MONITORING) == 10

    def test_drug_name_aliasing(self):
        assert monitoring_requirements("ramipril") == \
            monitoring_requirements("ace_or_arki")
        assert renal_flags("ibuprofen", egfr=50) != []


from gpdisc_core.uk_practice.fit_notes import fit_note_guidance, ADJUSTMENT_OPTIONS


class TestFitNotes:
    def test_day_3_self_cert(self):
        g = fit_note_guidance(3)
        assert "Self-certification" in g["route"]

    def test_day_10_needs_med3(self):
        g = fit_note_guidance(10)
        assert "fit note" in g["route"].lower()

    def test_long_term_signposts_oh(self):
        g = fit_note_guidance(120)
        assert "occupational health" in g["employer_guidance"].lower()

    def test_adjustments_listed(self):
        assert "Phased return" in " ".join(ADJUSTMENT_OPTIONS)


from gpdisc_core.uk_practice import (
    lookup_guideline, two_week_wait_check, driving_rules,
    capacity_two_stage_test, controlled_drug_class, antibiotic_for,
    monitoring_requirements, fit_note_guidance,
)


class TestPackageExports:
    def test_all_modules_reachable_from_package_root(self):
        assert lookup_guideline("asthma")
        assert two_week_wait_check("haemoptysis", age=46)
        assert driving_rules("epilepsy")
        assert capacity_two_stage_test()
        assert controlled_drug_class("morphine") == "2"
        assert antibiotic_for("cellulitis")
        assert monitoring_requirements("lithium")
        assert fit_note_guidance(3)["route"]
