"""Stage 7 Task 7.4: the palliative_care module.

The consultation front door used to answer every end-of-life
presentation with 'outside what I know' — honest, but useless to the
family asking how to keep a dying person comfortable. This module
gives the front door real content: terminal symptom control, the
can't-swallow-tablets route advice, and end-of-life planning.

Doses are the standard UK palliative formulary values as
decision-support scaffolding — every output carries the instruction
to confirm against the local palliative formulary before prescribing.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.palliative_care import (
    TERMINAL_SYMPTOMS,
    cant_swallow_route_advice,
    end_of_life_plan,
    eol_guidance_for,
    terminal_symptom_control,
)

PIPE = ConsultationPipeline()


class TestSymptomControlFrames:
    def test_four_core_symptoms_present(self):
        for key in ("pain", "agitation", "secretions", "nausea",
                    "breathlessness"):
            assert key in TERMINAL_SYMPTOMS, key
            frame = TERMINAL_SYMPTOMS[key]
            assert frame.get("title")
            assert frame.get("assess")          # look-before-treating
            assert frame.get("non_drug")        # care measures first
            assert frame.get("drugs")           # dose scaffolding

    def test_pain_carries_breakthrough_rule(self):
        g = terminal_symptom_control("pain")
        blob = " ".join(g["drugs"] + g["assess"]).lower()
        assert "breakthrough" in blob
        assert "divide" in blob or "sixth" in blob or "/ 6" in blob \
            or "by 6" in blob

    def test_agitation_looks_for_causes_before_sedating(self):
        g = terminal_symptom_control("agitation")
        blob = " ".join(g["assess"]).lower()
        assert "pain" in blob or "retention" in blob or \
            "constipation" in blob

    def test_secretions_explain_family_distress(self):
        g = terminal_symptom_control("secretions")
        blob = " ".join(g["non_drug"] + g["assess"]).lower()
        assert "family" in blob or "distress" in blob

    def test_every_drug_line_carry_formulary_caution(self):
        for key, frame in TERMINAL_SYMPTOMS.items():
            joined = " ".join(frame["drugs"]).lower()
            assert "confirm" in joined or "formulary" in joined or \
                "local" in joined, key

    def test_unknown_symptom_is_honest(self):
        g = terminal_symptom_control("hiccups")
        assert g.get("unknown") or "confirm" in " ".join(
            g.get("drugs", [])).lower()


class TestRouteAdvice:
    def test_morphine_oral_to_subcut(self):
        advice = cant_swallow_route_advice("morphine")
        assert advice["route"]
        assert advice["conversion"]
        assert "2" in advice["conversion"]   # oral->SC halved

    def test_midazolam_route(self):
        advice = cant_swallow_route_advice("midazolam")
        assert "subcutaneous" in advice["route"].lower() or \
            "sc" in advice["route"].lower()

    def test_unknown_drug_gets_honest_answer(self):
        advice = cant_swallow_route_advice("some-new-drug")
        assert advice.get("unknown") or \
            "specialist" in str(advice).lower() or \
            "formulary" in str(advice).lower()


class TestGuidanceRouter:
    def test_pain_text_routes_to_pain(self):
        g = eol_guidance_for("dying at home in pain, can't swallow")
        assert g["key"] == "pain"

    def test_rattling_routes_to_secretions(self):
        g = eol_guidance_for("noisy rattling chest at the end")
        assert g["key"] == "secretions"

    def test_agitated_routes_to_agitation(self):
        g = eol_guidance_for("she is dying and very agitated and restless")
        assert g["key"] == "agitation"

    def test_planning_text_routes_to_plan(self):
        g = eol_guidance_for("how do we plan for his last days at home")
        assert g["key"] == "planning"


class TestEndOfLifePlanning:
    def test_plan_has_anticipatory_box(self):
        plan = end_of_life_plan()
        blob = str(plan).lower()
        assert "anticipatory" in blob or "just in case" in blob
        # the four classic indications for the box
        for word in ("pain", "nausea", "agitation", "secretions"):
            assert word in blob, word

    def test_plan_cross_references_spikes_and_capacity(self):
        blob = str(end_of_life_plan()).lower()
        assert "spikes" in blob
        assert "capacity" in blob or "dnacpr" in blob


class TestFrontDoorIntegration:
    def test_dying_probe_gets_useful_guidance(self):
        rec = PIPE.run("my father is dying at home, how do we keep him "
                       "comfortable", {})
        summary = rec.summary().lower()
        # useful content, not the old 'outside what I know'
        assert "outside what i know" not in summary
        assert "don't have enough" not in summary
        # and it must still not force-fit an airway leader
        assert "quinsy" not in summary
        assert "epiglottitis" not in summary

    def test_cant_swallow_probe_gets_route_advice(self):
        rec = PIPE.run("my mother is dying, in pain, she can't swallow "
                       "tablets any more", {})
        summary = rec.summary().lower()
        assert "subcutaneous" in summary or " sc " in summary or \
            "route" in summary
        assert rec.escalation != "emergency"

    def test_emergency_still_wins_over_palliative_frame(self):
        """Comfort care never masks an emergency complication."""
        rec = PIPE.run("my father is dying at home and has started "
                       "vomiting blood", {})
        assert rec.escalation == "emergency"
