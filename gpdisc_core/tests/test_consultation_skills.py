"""Tests for consultation skills (expertise program Stage 5)."""
import pytest
from gpdisc_core.consultation_skills import (
    ice_questions, chunking_rules, spikes_steps, safety_net_formula,
    difficult_consultation_guidance, uncertainty_scripts, CONSULTATION_MODELS,
)


class TestConsultationSkills:
    def test_ice_three_core_questions(self):
        q = ice_questions()
        assert len(q) == 3
        assert any("think" in x for x in q)
        assert any("worried" in x for x in q)
        assert any("hoping" in x for x in q)

    def test_ice_tailors_to_cancer_fear(self):
        q = ice_questions("I'm worried this is cancer")
        assert len(q) == 4 and any("Name the fear" in x for x in q)

    def test_chunking_five_rules(self):
        assert len(chunking_rules()) == 5

    def test_spikes_six_steps_in_order(self):
        s = spikes_steps()
        assert len(s) == 6
        assert s[0].startswith("Setting") and s[5].startswith("Strategy")

    def test_safety_net_formula(self):
        s = safety_net_formula("viral illness settles in a week",
                               "rash that doesn't fade, drowsiness",
                               "48 hours")
        assert "viral illness" in s and "48 hours" in s

    def test_six_difficult_consultations(self):
        assert len(difficult_consultation_guidance("the_angry_patient")) >= 3
        assert difficult_consultation_guidance("the_dragon") == []

    def test_uncertainty_scripts_honest(self):
        s = uncertainty_scripts()
        assert any("I don't know" in x for x in s)

    def test_four_models(self):
        assert len(CONSULTATION_MODELS) == 4
