"""Stage 9 Task 9.2: interpretation breadth.

The pattern-readers: ECG (rhythm, territory, the treat-first patterns),
ABG (disorder → cause → compensation → severity), CSF (cells → glucose
→ protein), urine dip, spirometry, joint aspirate, culture logic.
Every reader states urgency, actions, and what it does NOT settle.
"""
import pytest

from gpdisc_core.interpretation import (
    interpret_abg, interpret_csf, interpret_culture, interpret_ecg,
    interpret_pft, interpret_synovial_fluid, interpret_urine_dip,
)


class TestECGRhythms:
    def test_af_fast_is_urgent(self):
        r = interpret_ecg("irregularly irregular, no P waves, rate 130", {})
        assert r.rhythm == "Atrial fibrillation"
        assert r.urgency == "urgent"
        assert any("CHA2DS2-VASc" in a for a in r.actions)

    def test_af_with_chest_pain_is_emergency(self):
        r = interpret_ecg("irregularly irregular with chest pain", {})
        assert r.urgency == "emergency"

    def test_vt_treated_as_vt_even_when_stable(self):
        r = interpret_ecg("regular broad complex tachycardia at 180, "
                          "patient alert", {})
        assert "VT until proven otherwise" in r.rhythm
        assert r.urgency == "emergency"
        assert any("verapamil" in a or "calcium-channel" in a
                   for a in r.actions)

    def test_torsades_gets_magnesium(self):
        r = interpret_ecg("polymorphic twisting tachycardia", {})
        assert r.urgency == "emergency"
        assert any("Magnesium" in a for a in r.actions)

    def test_complete_heart_block_paced(self):
        r = interpret_ecg("complete heart block, P waves dissociated "
                          "from QRS", {})
        assert r.urgency == "emergency"
        assert any("acing" in a for a in r.actions)

    def test_mobitz_ii_vs_wenckebach(self):
        assert interpret_ecg("Mobitz II 2:1 block", {}).urgency == "urgent"
        assert interpret_ecg("Wenckebach periodicity", {}).urgency == \
            "routine"

    def test_hyperkalaemia_treated_on_the_ecg(self):
        r = interpret_ecg("peaked T waves, wide QRS, no P waves",
                          {"potassium": 7.1})
        assert "Hyperkalaemia" in r.rhythm
        assert r.urgency == "emergency"
        assert any("Calcium gluconate" in a for a in r.actions)
        assert any("7.1" in f for f in r.findings)

    def test_digoxin_toxicity_before_benign_rhythm(self):
        r = interpret_ecg("on digoxin, bradycardia with ectopics", {})
        assert "toxicity" in r.rhythm
        assert any("level" in a.lower() or "antibody" in a.lower()
                   for a in r.actions)

    def test_unknown_pattern_is_said(self):
        r = interpret_ecg("some squiggles i don't understand", {})
        assert "not recognised" in r.rhythm

    def test_normal_ecg_does_not_exclude_acs(self):
        r = interpret_ecg("ECG normal", {"chest_pain": True})
        assert r.urgency == "urgent"
        assert any("serial" in a.lower() for a in r.actions)


class TestECGTerritories:
    def test_anterior_v2_v4(self):
        r = interpret_ecg("ST elevation V2-V4 with chest pain", {})
        assert r.urgency == "emergency"
        assert "Anteroseptal" in r.rhythm and "Anterior" in r.rhythm
        assert any("LAD" in f for f in r.findings)

    def test_inferior_gets_right_sided_leads(self):
        r = interpret_ecg("ST elevation in II, III and aVF", {})
        assert "Inferior" in r.rhythm
        assert any("RIGHT-SIDED" in a or "V4R" in a for a in r.actions)

    def test_lateral(self):
        r = interpret_ecg("ST elevation I, aVL and V5-V6", {})
        assert "Lateral" in r.rhythm

    def test_posterior_mirror_image(self):
        r = interpret_ecg("ST depression V1-V3 with tall R waves", {})
        assert "Posterior" in r.rhythm
        assert r.urgency == "emergency"

    def test_unmapped_st_elevation_still_emergency(self):
        r = interpret_ecg("there is ST elevation", {})
        assert r.urgency == "emergency"
        assert "unmapped" in r.rhythm.lower()


class TestABG:
    def test_dka_winters_appropriate(self):
        r = interpret_abg(7.28, 3.4, 12, lactate=2.0)
        assert r.disorder == "acidosis" and r.cause == "metabolic"
        assert "appropriately compensated" in r.compensation

    def test_fatiguing_dka_undercompensated(self):
        r = interpret_abg(7.20, 6.0, 12)
        assert "Under-compensated" in r.compensation

    def test_respiratory_acidosis(self):
        r = interpret_abg(7.25, 8.5, 28)
        assert r.cause == "respiratory"

    def test_mixed_acidosis(self):
        r = interpret_abg(7.10, 7.5, 10)
        assert "mixed" in r.cause

    def test_metabolic_alkalosis(self):
        r = interpret_abg(7.50, 5.0, 32)
        assert r.disorder == "alkalosis" and r.cause == "metabolic"

    def test_lactate_4_is_emergency_with_sepsis_six(self):
        r = interpret_abg(7.30, 4.0, 14, lactate=5.5)
        assert r.severity == "emergency"
        assert any("Sepsis Six" in a for a in r.actions)

    def test_hypoxia_is_the_emergency(self):
        r = interpret_abg(7.40, 4.5, 24, pao2=6.8)
        assert r.severity == "emergency"

    def test_mmhg_auto_converted(self):
        r = interpret_abg(7.20, 50, 10)      # 50 mmHg ≈ 6.7 kPa
        assert "respiratory" in r.cause

    def test_compensated_disorder_named(self):
        r = interpret_abg(7.40, 8.0, 32)
        assert r.disorder == "compensated disorder"

    def test_normal_gas_with_raised_lactate(self):
        r = interpret_abg(7.40, 5.0, 24, lactate=3.0)
        assert r.severity == "concern"
        assert any("Lactate" in f for f in r.findings)


class TestCSF:
    def test_bacterial_pattern_treats_within_the_hour(self):
        r = interpret_csf(wbc=1200, neutrophils_pct=88, protein=2.2,
                          csf_glucose=1.2, serum_glucose=6.0)
        assert r.urgency == "emergency"
        assert any("within the hour" in a for a in r.actions)
        assert any("public health" in a.lower() for a in r.actions)

    def test_partially_treated_still_treats(self):
        r = interpret_csf(wbc=400, neutrophils_pct=80, protein=1.5)
        assert r.urgency == "emergency"

    def test_viral_pattern_with_encephalitis_action(self):
        r = interpret_csf(wbc=150, neutrophils_pct=20, protein=0.6,
                          csf_glucose=3.6, serum_glucose=6.0)
        assert r.urgency == "urgent"
        assert any("HSV PCR" in a for a in r.actions)

    def test_lymphocytic_low_glucose_tb_frame(self):
        r = interpret_csf(wbc=200, neutrophils_pct=10, protein=1.8,
                          csf_glucose=1.5, serum_glucose=6.0)
        assert "TB" in r.pattern or "TB" in " ".join(r.findings)

    def test_xanthochromia_is_sah(self):
        r = interpret_csf(xanthochromia=True)
        assert r.urgency == "emergency"
        assert any("SAH" in a or "neurosurg" in a.lower()
                   for a in r.actions)

    def test_gram_stain_overrides(self):
        r = interpret_csf(wbc=5, gram_stain="gram-positive diplococci")
        assert r.urgency == "emergency"
        assert "meningitis" in " ".join(r.findings).lower()

    def test_bloody_tap_correction_note(self):
        r = interpret_csf(appearance="blood-stained", wbc=10)
        assert any("traumatic" in f.lower() or "correction" in f.lower()
                   for f in r.findings)


class TestUrineDip:
    def test_uti_both_markers(self):
        r = interpret_urine_dip({"nitrites": True, "leukocytes": True})
        assert "UTI" in r.pattern
        assert any("Nitrofurantoin" in a for a in r.actions)

    def test_fever_makes_it_pyelonephritis(self):
        r = interpret_urine_dip({"nitrites": True, "leukocytes": True},
                                {"fever": True, "loin_pain": True})
        assert "pyelonephritis" in " ".join(r.findings).lower()

    def test_sterile_pyuria_chlamydia_tb(self):
        r = interpret_urine_dip({"leukocytes": True})
        joined = " ".join(r.findings).lower()
        assert "chlamydia" in joined or "tb" in joined

    def test_glomerular_pattern_urgent(self):
        r = interpret_urine_dip({"blood": True, "protein": True})
        assert r.urgency == "urgent"
        assert any("nephrolog" in a.lower() for a in r.actions)

    def test_glucose_ketones_dka_pathway(self):
        r = interpret_urine_dip({"glucose": True, "ketones": True})
        assert r.urgency == "emergency"
        assert any("DKA" in a for a in r.actions)


class TestPFT:
    def test_obstruction_with_severity(self):
        r = interpret_pft(45, 80, reversibility_pct=5)
        assert "Obstructive" in r.pattern
        assert "severe" in " ".join(r.findings).lower()
        assert any("COPD" in a for a in r.actions)

    def test_significant_reversibility_asthma(self):
        r = interpret_pft(60, 80, reversibility_pct=18)
        assert any("asthma" in f.lower() for f in r.findings)

    def test_restriction_needs_volumes(self):
        r = interpret_pft(65, 68)
        assert "Restrictive" in r.pattern
        assert any("TLCO" in a or "volumes" in a.lower()
                   for a in r.actions)

    def test_normal_spirometry_symptoms_elsewhere(self):
        r = interpret_pft(95, 95)
        assert "Normal" in r.pattern

    def test_normal_but_reversible_chases_asthma(self):
        r = interpret_pft(92, 95, reversibility_pct=14)
        assert any("asthma" in f.lower() for f in r.findings)


class TestSynovialFluid:
    def test_septic_range_emergency(self):
        r = interpret_synovial_fluid(appearance="turbid", wbc=90000)
        assert r.urgency == "emergency"
        assert any("washout" in a.lower() for a in r.actions)

    def test_crystal_does_not_exclude_infection(self):
        r = interpret_synovial_fluid(wbc=100000, crystals="needles")
        assert any("DOES NOT EXCLUDE" in f for f in r.findings)

    def test_needle_crystals_gout(self):
        r = interpret_synovial_fluid(wbc=20000,
                                     crystals="negatively birefringent "
                                              "needles")
        assert "gout" in " ".join(r.findings).lower()
        assert any("allopurinol" in a.lower() for a in r.actions)

    def test_rhomboid_cppd_with_screen(self):
        r = interpret_synovial_fluid(wbc=30000,
                                     crystals="positively birefringent "
                                              "rhomboids")
        joined = " ".join(r.findings + r.actions).lower()
        assert "cppd" in joined and "haemochromatosis" in joined

    def test_non_inflammatory_oa(self):
        r = interpret_synovial_fluid(appearance="clear viscous", wbc=500)
        assert "Non-inflammatory" in r.pattern

    def test_bloody_aspirate_clotting_question(self):
        r = interpret_synovial_fluid(appearance="bloody", wbc=800)
        assert any("clotting" in a.lower() or "haemarthrosis" in f.lower()
                   for f, a in zip(r.findings, r.actions)) or \
            any("haemarthrosis" in f.lower() for f in r.findings)


class TestCultures:
    def test_double_skin_flora_contaminant(self):
        r = interpret_culture("blood", ["Coagulase negative "
                                        "staphylococcus",
                                        "Corynebacterium"])
        assert "contaminant" in r.pattern
        assert any("NOT treat" in a or "do not treat" in a.lower()
                   for a in r.actions)

    def test_skin_flora_with_line_is_significant(self):
        r = interpret_culture("blood", ["Coagulase negative "
                                        "staphylococcus"],
                              {"line_in_situ": True, "septic": True})
        assert r.urgency != "routine"

    def test_aureus_never_contaminant(self):
        r = interpret_culture("blood", ["Staphylococcus aureus"])
        assert r.urgency == "emergency"
        assert any("endocarditis" in " ".join(r.findings + r.actions)
                   .lower() for _ in [0])

    def test_no_growth_after_antibiotics(self):
        r = interpret_culture("blood", [], {"antibiotics_first": True})
        assert any("culture-negative" in f.lower()
                   for f in r.findings)

    def test_asymptomatic_bacteriuria_not_treated(self):
        r = interpret_culture("urine", ["E. coli"],
                              {"catheter": True, "asymptomatic": True})
        assert any("NOT an infection" in f or "No antibiotics" in a
                   for f, a in zip(r.findings, r.actions)) or \
            any("No antibiotics" in a for a in r.actions)
