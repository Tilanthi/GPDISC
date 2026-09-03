"""Stage 8 Task 8.2: resource settings — the same level of concern,
different first action.

The clinical reasoning is resource-independent; the disposition is
not. A '999 now' assumes an ambulance system that a remote clinic, a
humanitarian field post and an offshore vessel do not have. The
invariant under test: the setting ADAPTS the action and NEVER lowers
the concern.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.resource_settings import (
    SETTINGS, DEFAULT_SETTING, available_settings, describe_setting,
    disposition_guidance, setting_line,
)

PIPE = ConsultationPipeline()

LEVELS = ["emergency", "urgent", "routine", "self_care"]
NON_DEFAULT = [s for s in SETTINGS if s != DEFAULT_SETTING]


class TestGuidanceTable:
    def test_every_level_has_guidance_in_every_setting(self):
        for setting in SETTINGS:
            for level in LEVELS:
                g = disposition_guidance(level, setting)
                assert g["action"], (setting, level)
                assert g["transport"], (setting, level)
                assert g["alongside"], (setting, level)
                assert g["setting"] == setting
                assert g["level"] == level

    def test_same_emergency_different_worlds_different_actions(self):
        uk = disposition_guidance("emergency", "uk_general_practice")
        remote = disposition_guidance("emergency", "remote_rural_clinic")
        field = disposition_guidance("emergency", "humanitarian_field")
        assert "999" in uk["action"]
        # the non-UK worlds may mention 999 only to DISAVOW it
        assert "call 999" not in remote["action"].lower()
        assert "stabilise" in remote["action"].lower()
        assert "call 999" not in field["action"].lower()
        assert "coordinator" in field["action"].lower()
        # and no two worlds say the same thing
        assert len({uk["action"], remote["action"], field["action"]}) == 3

    def test_unknown_setting_falls_back_with_honest_note(self):
        g = disposition_guidance("emergency", "mars_colony")
        assert "999" in g["action"]           # UK default used
        assert "unknown setting" in g["note"].lower()

    def test_setting_profiles_declare_their_constraints(self):
        for name, s in SETTINGS.items():
            assert "has_ambulance" in s
            assert "transfer" in s and "investigations" in s
            assert s["assumptions"], name

    def test_describe_setting_names_the_ruleset(self):
        assert "UK general practice" in describe_setting(DEFAULT_SETTING)
        assert "Remote" in describe_setting("remote_rural_clinic")
        assert "Unknown" in describe_setting("wakanda")

    def test_setting_line_none_for_default(self):
        assert setting_line("emergency", None) is None
        assert setting_line("emergency", DEFAULT_SETTING) is None
        assert setting_line("emergency", "made_up_place") is None


class TestPipelineWiring:
    """The consultation record carries the adapted disposition line,
    and the adaptation changes NOTHING clinical."""

    def test_emergency_uk_says_999(self):
        rec = PIPE.run("crushing central chest pain for 30 minutes, "
                       "sweating, 66 year old smoker", {})
        assert rec.escalation == "emergency"
        assert "999" in rec.referral
        assert "Remote" not in rec.referral

    def test_emergency_remote_overrides_999_explicitly(self):
        rec = PIPE.run("crushing central chest pain for 30 minutes, "
                       "sweating, 66 year old smoker",
                       {"setting": "remote_rural_clinic"})
        assert rec.escalation == "emergency"   # concern never lowered
        assert "NO AMBULANCE SYSTEM HERE" in rec.referral
        assert "stabilise" in rec.referral.lower()
        # the override says so out loud, not as a quiet contradiction
        assert "overrides" in rec.referral

    def test_emergency_field_names_coordinator(self):
        rec = PIPE.run("crushing central chest pain for 30 minutes, "
                       "sweating, 66 year old smoker",
                       {"setting": "humanitarian_field"})
        assert rec.escalation == "emergency"
        assert "coordinator" in rec.referral.lower()

    def test_emergency_offshore_names_telemedicine(self):
        rec = PIPE.run("crushing central chest pain for 30 minutes, "
                       "sweating, 66 year old smoker",
                       {"setting": "offshore_vessel"})
        assert rec.escalation == "emergency"
        assert "telemedic" in rec.referral.lower()

    def test_routine_remote_gets_clinic_day_not_999(self):
        rec = PIPE.run("sore throat for two days, no fever, eating "
                       "normally", {"setting": "remote_rural_clinic"})
        assert rec.escalation == "routine"
        assert "999" not in rec.referral
        assert "clinic" in rec.referral.lower()

    def test_differential_identical_across_settings(self):
        """The setting adapts disposition ONLY — same presentation,
        same ranked differential, same safety net, same escalation."""
        text = "sore throat for three days, painful to swallow, fever"
        base = PIPE.run(text, {})
        remote = PIPE.run(text, {"setting": "remote_rural_clinic"})
        field = PIPE.run(text, {"setting": "humanitarian_field"})
        assert base.ranked_differential == remote.ranked_differential
        assert base.ranked_differential == field.ranked_differential
        assert base.escalation == remote.escalation == field.escalation
        assert base.safety_net == remote.safety_net

    def test_unknown_setting_in_context_changes_nothing(self):
        text = "crushing central chest pain for 30 minutes, sweating"
        a = PIPE.run(text, {})
        b = PIPE.run(text, {"setting": "not_a_real_place"})
        assert b.referral == a.referral     # no bogus line appended
        assert b.escalation == a.escalation


class TestSafetyInvariant:
    @pytest.mark.parametrize("setting", NON_DEFAULT)
    def test_emergency_never_lowered_by_setting(self, setting):
        rec = PIPE.run("sudden drooping face and slurred speech this "
                       "morning", {"setting": setting})
        assert rec.escalation == "emergency"

    @pytest.mark.parametrize("setting", NON_DEFAULT)
    def test_urgent_stays_urgent_or_higher(self, setting):
        rec = PIPE.run("finding it hard to breathe, wheezy, inhalers "
                       "not helping", {"setting": setting})
        assert rec.escalation in ("urgent", "emergency")
