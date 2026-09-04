"""Tests for sexual_health (expertise program Stage 2)."""
import pytest
from gpdisc_core.sexual_health import (
    UKMEC, ukmec_category, safe_methods, panel_for, emergency_contraception,
)


class TestUKMEC:
    def test_migraine_aura_cocp_is_4(self):
        cat, why = ukmec_category("cocp", "migraine_with_aura")
        assert cat == 4 and "stroke" in why.lower()

    def test_pop_safe_with_aura(self):
        cat, _ = ukmec_category("pop", "migraine_with_aura")
        assert cat == 1

    def test_iud_pregnancy_is_4(self):
        assert ukmec_category("ius_iud", "pregnancy")[0] == 4

    def test_unknown_pair_returns_zero(self):
        assert ukmec_category("implant", "migraine_with_aura")[0] == 0

    def test_safe_methods_for_vte_history(self):
        methods = safe_methods("vte_history")
        assert "implant" in methods and "pop" in methods
        assert "cocp" not in methods

    def test_table_size(self):
        # 21 since the audit fix: smoker_35_plus split into <15/day (3)
        # and >=15/day (4) per FSRH UKMEC.
        assert len(UKMEC) == 21


class TestSTIPanels:
    def test_ulcer_panel(self):
        name, panel = panel_for("painful ulcer on my penis")
        assert name == "genital_ulcer"
        assert any("syphilis" in t.lower() for t in panel)

    def test_male_discharge_panel(self):
        name, panel = panel_for("discharge from my penis")
        assert name == "symptomatic_male_discharge"

    def test_pelvic_pain_panel_includes_pregnancy_test(self):
        name, panel = panel_for("lower abdominal pain for three days")
        assert name == "symptomatic_female_pelvic_pain"
        assert any("pregnancy" in t.lower() for t in panel)

    def test_default_asymptomatic(self):
        name, _ = panel_for("just want a routine check")
        assert name == "asymptomatic_screen"


class TestEmergencyContraception:
    def test_within_120h_copper_first_line(self):
        r = emergency_contraception(80)
        assert r["recommendation"] == "Copper IUD"
        first = [o["method"] for o in r["options"] if o["first_line"]]
        assert first == ["Copper IUD"]

    def test_beyond_120h_no_hormonal(self):
        r = emergency_contraception(130)
        assert r["recommendation"] == "None in-window — discuss referral"

    def test_bmi_over_26_flags_reduced_efficacy(self):
        r = emergency_contraception(24, bmi=30)
        assert any("reduced" in o["effectiveness"].lower() for o in r["options"])

    def test_levonorgestrel_only_within_72h(self):
        r = emergency_contraception(70)
        methods = [o["method"] for o in r["options"]]
        assert "Levonorgestrel 1.5mg" in methods
