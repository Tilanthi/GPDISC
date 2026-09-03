"""Stage 8 Task 8.4: humanitarian care — the refugee/asylum
consultation layer.

Three modules: arrival screening (the highest-yield bundle, sequenced
trauma-informed), interpreter principles (the never-family rule),
unaccompanied minors (age-assessment caution + trafficking duties).
Front-door routing follows the 7.4 palliative pattern: the module is
REACHABLE, and safety always wins over screening.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.humanitarian_care import (
    arrival_health_screen, is_arrival_consultation, screening_summary,
    interpreter_principles, same_language_check,
    trafficking_indicators, unaccompanied_minor_review, minor_summary,
)

PIPE = ConsultationPipeline()


class TestArrivalScreen:
    def test_screen_covers_the_high_yield_bundle(self):
        s = arrival_health_screen()
        joined = " ".join(v if isinstance(v, str) else " ".join(v)
                          for v in s.values()).lower()
        for item in ("tb", "hiv", "hepatitis b", "syphilis",
                     "immunisation", "interpreter", "mental-health",
                     "malaria", "asylum report"):
            assert item in joined, item

    def test_screen_names_what_not_to_do(self):
        s = arrival_health_screen()
        assert len(s["do_not"]) >= 4
        assert "repeat invasive" in " ".join(s["do_not"]).lower()

    def test_arrival_detection(self):
        assert is_arrival_consultation(
            "asylum seeker needing first health check")
        assert is_arrival_consultation("just arrived as a refugee family")
        assert not is_arrival_consultation("sore throat for two days")

    def test_red_flags_include_tb_and_malaria_urgency(self):
        flags = " ".join(arrival_health_screen()["red_flags"]).lower()
        assert "tb" in flags and "malaria" in flags


class TestInterpreterPrinciples:
    def test_never_list_bans_family_and_children(self):
        never = " ".join(interpreter_principles()["never"]).lower()
        assert "family" in never and "children" in never

    def test_dialect_checked_not_just_language(self):
        principles = " ".join(interpreter_principles()["principles"]).lower()
        assert "dialect" in principles

    def test_situation_emphasis_safeguarding(self):
        g = interpreter_principles("safeguarding disclosure")
        assert any("safeguarding" in p.lower() for p in g["for_this_situation"])

    def test_language_mismatch_is_named_as_failure(self):
        line = same_language_check("Kurdish (Sorani)", "Syrian Arabic")
        assert "mismatch" in line.lower()

    def test_language_match_confirmed(self):
        assert "confirmed" in same_language_check("Tigrinya", "Tigrinya")


class TestUnaccompaniedMinors:
    def test_age_assessment_is_not_treated_as_medical(self):
        duties = " ".join(unaccompanied_minor_review()
                          ["immediate_duties"]).lower()
        assert "not a medical act" in duties or \
            "benefit of the doubt" in duties

    def test_trafficking_indicators_actionable(self):
        assert len(trafficking_indicators()) >= 6
        joined = " ".join(trafficking_indicators()).lower()
        assert "debt" in joined or "bondage" in joined
        assert "speak for the child" in joined

    def test_consent_own_understanding_not_the_adult(self):
        consent = " ".join(unaccompanied_minor_review()
                           ["consent_and_capacity"]).lower()
        assert "accompanying adult's agreement" in consent


class TestFrontDoorRouting:
    def test_adult_arrival_gets_screen_not_empty_differential(self):
        rec = PIPE.run("I am an asylum seeker, just arrived, what "
                       "health checks do I need?", {})
        assert rec.escalation == "routine"
        assert "New-arrival" in rec.problem_representation
        assert "TB screen" in rec.treatment
        assert "interpreter" in rec.treatment.lower()

    def test_unaccompanied_minor_gets_minor_pathway(self):
        rec = PIPE.run("unaccompanied child asylum seeker arrived "
                       "last week, 15 years old, needs checks", {})
        assert rec.escalation == "routine"
        assert "child" in rec.problem_representation
        assert "age assessment" in rec.treatment.lower()
        assert "trafficking" in rec.treatment.lower()

    def test_chest_pain_beats_screening(self):
        """Safety always wins: a refugee with ACS is ACS, not a
        screening consultation."""
        rec = PIPE.run("asylum seeker with crushing chest pain for 30 "
                       "minutes, sweating", {})
        assert rec.escalation == "emergency"
        assert "EMERGENCY" in rec.problem_representation

    def test_torture_disclosure_not_hijacked_by_arrival_screen(self):
        """The torture corpus entry owns torture disclosures; the
        arrival screen is for arrivals, not every migrant story."""
        rec = PIPE.run("was tortured in my country, nightmares, scars "
                       "from beatings", {})
        assert not rec.outside_scope
        assert rec.ranked_differential
        assert "torture" in rec.ranked_differential[0]["name"].lower()

    def test_summary_renders_screen(self):
        rec = PIPE.run("refugee, newly arrived, health check please", {})
        text = rec.summary()
        assert "Treatment:" in text
        assert "interpreter" in text.lower()
