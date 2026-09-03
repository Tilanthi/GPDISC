"""Stage 9 Task 9.1: consultant opinions in the MDT.

Six specialists — cardiologist, neurologist, oncologist, paediatrician,
psychiatrist, palliative physician — join the debate. A consultant
speaks ONLY when their domain is implicated, and their notes are
corpus-driven: discriminators and investigations come from the
ConditionProfile of a GENUINE contender (>= 0.5x the leader's score —
the validator's contender gate), never from the noise tail.

The suite also locks the corpus gap the 9.1 probes found: "on exertion
/ relieved by rest" — the textbook stable-angina discriminators — used
to extract as nothing, so a months-long exertional story led with
STEMI. Fixed in knowledge.py; locked here so it can never regress.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.mdt import CONSULTANT_ROLES, MDT_ROLES, run_mdt
from gpdisc_core.mdt.roles import contribute

CONSULTANT_KEYS = ("cardiologist", "neurologist", "oncologist",
                   "paediatrician", "psychiatrist", "palliative_physician")


def _speaking(result) -> list:
    return [k for k in CONSULTANT_KEYS if k in result.role_notes]


class TestRegistry:
    def test_six_consultants_registered(self):
        assert [r.key for r in CONSULTANT_ROLES] == list(CONSULTANT_KEYS)
        assert MDT_ROLES[-6:] == CONSULTANT_ROLES

    def test_every_consultant_key_routable(self):
        for key in CONSULTANT_KEYS:
            assert any(r.key == key for r in MDT_ROLES)


class TestCardiologist:
    def test_speaks_on_heart_failure_with_corpus_content(self):
        r = run_mdt("palpitations, irregular heartbeat, breathless "
                    "lying flat at night, swollen ankles",
                    {"age_years": 72})
        notes = r.role_notes.get("cardiologist", [])
        assert notes
        # corpus-driven: the profile's discriminator or work-up appears
        assert any("heart failure" in n.lower() for n in notes)
        assert any("ECG" in n or "echo" in n.lower() for n in notes)
        # craft: the trace before the troponin
        assert any("12-lead ECG" in n for n in notes)

    def test_speaks_on_emergency_acs_path(self):
        """Emergency short-circuit: ranked is empty, the retained rule is
        the working diagnosis — the cardiologist still speaks."""
        r = run_mdt("66 year old man, chest pain 40 minutes, sweating", {})
        assert r.escalation == "emergency"
        assert "cardiologist" in r.role_notes


class TestNeurologist:
    def test_first_seizure_gets_corpus_and_driving_craft(self):
        r = run_mdt("first fit in a 30 year old, fully recovered, "
                    "witnessed", {})
        notes = r.role_notes.get("neurologist", [])
        assert notes
        assert any("witness" in n.lower() or "separates" in n.lower()
                   for n in notes)
        assert any("driving" in n.lower() for n in notes)

    def test_onset_speed_craft(self):
        notes = contribute("neurologist",
                           "worst headache of my life", {})
        assert any("onset" in n.lower() for n in notes)


class TestOncologist:
    def test_two_week_wait_criteria_surface(self):
        r = run_mdt("58 year old man, difficulty swallowing, losing "
                    "weight over two months", {})
        notes = r.role_notes.get("oncologist", [])
        assert any("2ww" in n for n in notes)
        assert any("swallow" in n.lower() or "endoscop" in n.lower()
                   for n in notes)

    def test_oncological_emergency_on_chemo_fever(self):
        r = run_mdt("fever on chemotherapy for lymphoma", {})
        assert r.escalation == "emergency"
        notes = r.role_notes.get("oncologist", [])
        assert any("neutropenic" in n.lower() for n in notes)

    def test_refer_at_threshold_craft(self):
        notes = contribute("oncologist", "unexplained lump in the neck", {})
        assert any("threshold" in n.lower() for n in notes)


class TestPaediatrician:
    def test_weight_based_dosing_craft(self):
        r = run_mdt("3 year old with fever and a barky cough, drooling",
                    {})
        notes = r.role_notes.get("paediatrician", [])
        assert any("weight" in n.lower() for n in notes)
        assert any("quiet child" in n.lower() or "crash" in n.lower()
                   for n in notes)

    def test_child_age_context_triggers(self):
        notes = contribute("paediatrician", "fever and rash",
                           {"age_years": 6})
        assert notes

    def test_adult_age_does_not_trigger(self):
        assert contribute("paediatrician", "fever and rash",
                          {"age_years": 45}) == []


class TestPsychiatrist:
    def test_risk_structure_on_self_harm(self):
        r = run_mdt("hearing voices telling him to hurt himself, not "
                    "sleeping for days", {"age_years": 24})
        notes = r.role_notes.get("psychiatrist", [])
        assert any("means" in n.lower() and "plan" in n.lower()
                   for n in notes)
        assert any("delirium" in n.lower() for n in notes)

    def test_no_risk_craft_when_no_risk_implicated(self):
        # a psychiatric presentation without suicidality: the delirium
        # craft fires, the suicide-risk craft line stays out of it
        notes = contribute("psychiatrist",
                           "he's paranoid and not sleeping", {})
        assert notes
        assert not any("means, plan" in n for n in notes)


class TestPalliativePhysician:
    def test_dying_presentation_gets_palliative_opinion(self):
        r = run_mdt("my father is dying at home, agitated and "
                    "distressed, can't swallow tablets", {})
        notes = r.role_notes.get("palliative_physician", [])
        assert any("assess" in n.lower() for n in notes)
        assert any("anticipatory" in n.lower() for n in notes)
        assert any("999" in n for n in notes)  # expected death ≠ 999

    def test_context_flag_triggers(self):
        notes = contribute("palliative_physician", "nausea and vomiting",
                           {"palliative": True})
        assert any("anticipatory" in n.lower() for n in notes)


class TestSilenceGuards:
    """A specialist who comments on everything is noise. These must
    keep NO consultant in the room."""

    @pytest.mark.parametrize("presentation,context", [
        ("sore throat for two days, no fever, mild", {}),
        ("knee pain after football, 30 year old, no other symptoms", {}),
        ("tired all the time", {}),
    ])
    def test_no_consultant_on_benign_presentations(self, presentation,
                                                   context):
        r = run_mdt(presentation, context)
        assert _speaking(r) == []

    def test_contender_gate_blocks_noise_tail(self):
        """The heart-failure differential's noise tail contains HSP
        (paediatric), GBS (neuro), neutropenic sepsis (oncology) — none
        of them genuine contenders. Only the cardiologist speaks."""
        r = run_mdt("palpitations, irregular heartbeat, breathless "
                    "lying flat at night, swollen ankles",
                    {"age_years": 72})
        assert _speaking(r) == ["cardiologist"]


class TestStableAnginaCorpusFix:
    """Locked 2026-09-03 (Stage 9 probe): the exertional pattern now
    leads with stable angina, not STEMI. Discovered while testing the
    cardiologist role — 'chest pain on exertion for months, relieved by
    rest' extracted only the generic chest_pain token, and STEMI's
    higher specificity won. The discriminators now carry."""

    def test_exertional_months_leads_stable_angina(self):
        rec = ConsultationPipeline().run(
            "central chest pain on exertion for months, relieved by "
            "rest, 55 year old smoker", {})
        assert rec.escalation == "routine"
        assert rec.ranked_differential[0]["condition_id"] == "stable_angina"

    def test_acs_still_wins_acute(self):
        rec = ConsultationPipeline().run(
            "66 year old man, chest pain 40 minutes, sweating", {})
        assert rec.escalation == "emergency"

    def test_msk_chest_pain_unaffected(self):
        rec = ConsultationPipeline().run(
            "sharp chest pain when i breathe in, after a fall, tender "
            "ribs", {})
        assert rec.ranked_differential[0]["condition_id"] == \
            "musculoskeletal_chest_pain"
