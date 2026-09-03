"""Stage 6 Task 6.8: post-exposure prophylaxis — decisions in hours.

Rabies, hepatitis B and HIV each have a window after exposure during
which prophylaxis changes the outcome, and each is useless after it:
rabies vaccine works until symptoms begin (then it is 100% fatal),
HBIG works best inside 48 hours, HIV PEP inside 72. The audit's Bali
dog-bite probe returned an empty differential; a decision this
time-boxed must never return nothing.
"""
from gpdisc_core.post_exposure import (
    rabies_pep, bloodborne_exposure, pep_screen,
)
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline

PIPE = ConsultationPipeline()


class TestRabiesPEP:
    def test_bali_dog_bite_category_three(self):
        a = rabies_pep("bitten by a dog in Bali two days ago, broke the "
                       "skin and bled", {})
        assert a.exposure_category == "III"
        assert a.needs_pep is True
        assert a.rig_needed is True          # category III = immunoglobulin
        assert any("0" in s or "day" in s.lower() for s in a.schedule)
        assert any("15" in w for w in a.wound_care)  # wash 15 minutes

    def test_bat_contact_is_pep_even_in_uk(self):
        """Bats carry lyssaviruses even in rabies-free countries — a
        bat anywhere is category III until proven otherwise."""
        a = rabies_pep("found a bat on my pillow, it scratched my hand "
                       "this morning, we live in Scotland", {})
        assert a.needs_pep is True
        assert a.rig_needed is True

    def test_lick_intact_skin_category_one_no_pep(self):
        a = rabies_pep("stray dog licked my hand in India, skin not "
                       "broken, no scratch", {})
        assert a.exposure_category == "I"
        assert a.needs_pep is False

    def test_scratch_without_bleeding_category_two(self):
        a = rabies_pep("monkey scratched my ankle in Thailand, red mark "
                       "but no blood", {})
        assert a.exposure_category == "II"
        assert a.needs_pep is True
        assert a.rig_needed is False         # II = vaccine only, no RIG

    def test_uk_domestic_observable_dog_defers(self):
        """A healthy, observable UK pet dog: 10-day observation may
        spare vaccination — the decision is documented, not skipped."""
        a = rabies_pep("my own dog bit my hand at home in Leeds, drew "
                       "blood, dog is vaccinated and well", {})
        assert a.region_risk in ("rabies_free_observable",)
        assert a.observation_note            # 10-day observation path
        assert a.wound_care                  # but wound care + tetanus still

    def test_never_too_late_until_symptoms(self):
        a = rabies_pep("bitten by a street dog in India six weeks ago, "
                       "never had any injections, feel fine", {})
        assert a.needs_pep is True
        assert any("symptom" in s.lower()
                   for s in a.schedule + [a.urgency])

    def test_questions_include_vaccination_status(self):
        a = rabies_pep("bitten by a cat in Vietnam yesterday", {})
        assert any("vaccinat" in q.lower() or "immune" in q.lower()
                   for q in a.questions)


class TestBloodbornePEP:
    def test_needlestick_hbv_positive_source(self):
        a = bloodborne_exposure(
            "needlestick injury, source patient known hepatitis B "
            "positive, 2 hours ago", {})
        assert a.hbv_pep is True
        assert "48" in a.hbv_note or "HBIG" in a.hbv_note
        assert any("anti-HBs" in t or "antibod" in t.lower()
                   for t in a.tests)

    def test_needlestick_hiv_positive_source_within_window(self):
        a = bloodborne_exposure(
            "needlestick from a patient with HIV, happened this morning, "
            "about 4 hours ago", {})
        assert a.hiv_pep is True
        assert "72" in a.hiv_note

    def test_hiv_undetectable_source_frames_risk_honestly(self):
        a = bloodborne_exposure(
            "needlestick, source has HIV but is on treatment with an "
            "undetectable viral load", {})
        # risk is effectively zero — say so rather than reflexive PEP,
        # but baseline testing still happens
        assert "undetectable" in a.hiv_note.lower() or \
            "effectively" in a.hiv_note.lower()
        assert a.tests

    def test_unknown_source_community_needle(self):
        """A community-found needle: HIV PEP usually not indicated,
        HBV status and tetanus matter more — the assessment says which."""
        a = bloodborne_exposure(
            "stood on a used needle in the park this morning, source "
            "unknown", {})
        assert a.hiv_note                    # explicit decision either way
        assert any("tetanus" in q.lower() for q in a.questions)

    def test_condom_broke_with_hiv_partner_30_hours(self):
        a = bloodborne_exposure(
            "condom broke last night with a partner who is HIV positive, "
            "about 30 hours ago", {})
        assert a.hiv_pep is True

    def test_hcv_has_no_pep_but_has_a_test_plan(self):
        a = bloodborne_exposure(
            "needlestick, source known hepatitis C positive", {})
        assert a.hcv_note
        assert any("6" in t or "RNA" in t for t in a.tests)

    def test_sexual_assault_gets_full_pathway(self):
        a = bloodborne_exposure("sexually assaulted last night", {})
        assert a.hiv_pep is True             # PEP offered within 72h
        assert any("contracep" in q.lower() or "emergency contraception"
                   in " ".join(a.questions).lower() for q in a.questions)


class TestPEPScreenDispatcher:
    def test_bite_routes_to_rabies(self):
        r = pep_screen("bitten by a dog in Bali", {})
        assert r["pathway"] == "rabies"

    def test_needlestick_routes_to_bloodborne(self):
        r = pep_screen("needlestick injury at work", {})
        assert r["pathway"] == "bloodborne"

    def test_irrelevant_returns_none_pathway(self):
        r = pep_screen("sore throat for two days", {})
        assert r["pathway"] == "none"


class TestPEPPipelineWiring:
    def test_bali_dog_bite_escalates_and_names_rabies(self):
        rec = PIPE.run("bitten by a dog in Bali two days ago, broke the "
                       "skin and bled", {})
        assert rec.escalation in ("urgent", "emergency")
        names = {d["name"] for d in rec.ranked_differential} | \
                {d["name"] for d in rec.dangerous_alternatives}
        assert any("rabies" in n.lower() or "bite" in n.lower()
                   for n in names)

    def test_needlestick_hbv_source_urgent_with_bloodborne_named(self):
        rec = PIPE.run("needlestick injury, source patient known "
                       "hepatitis B positive, 2 hours ago", {})
        assert rec.escalation in ("urgent", "emergency")
        names = {d["name"] for d in rec.ranked_differential} | \
                {d["name"] for d in rec.dangerous_alternatives}
        assert any("bloodborne" in n.lower() or "needlestick" in n.lower()
                   or "exposure" in n.lower() for n in names)

    # ---- 8.1 substring-discipline guards (probes that exposed the
    # geographic and patient-describing bare substrings) ----
    def test_country_mention_alone_is_not_rabies(self):
        """'rabies_region_exposure' once carried bare country names:
        'nepal' made an altitude trek a 999 rabies contender."""
        rec = PIPE.run("trekking in Nepal, headache and nausea at "
                       "4000 metres", {})
        names = {d["name"] for d in rec.ranked_differential} | \
                {d["name"] for d in rec.dangerous_alternatives}
        assert not any("rabies" in n.lower() for n in names), names
        assert rec.escalation != "emergency"

    def test_own_carrier_status_is_not_an_exposure_story(self):
        """'source_hepatitis_b' once carried patient-describing
        phrases: the patient's own chronic hepatitis B was claimed as
        a needlestick exposure."""
        rec = PIPE.run("tired all the time, hepatitis B carrier for "
                       "years", {})
        names = {d["name"] for d in rec.ranked_differential} | \
                {d["name"] for d in rec.dangerous_alternatives}
        assert not any("bloodborne" in n.lower() for n in names), names
