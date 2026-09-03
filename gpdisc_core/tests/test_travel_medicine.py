"""Tests for travel_medicine (expertise program Stage 2)."""
import pytest
from gpdisc_core.travel_medicine import (
    find_destination, recommend_prophylaxis, pre_travel_consult,
)


class TestDestinations:
    def test_ghana_found_by_name(self):
        d = find_destination("holiday in Ghana for two weeks")
        assert d is not None and d.region == "West Africa"

    def test_unknown_destination_none(self):
        assert find_destination("trip to the moon") is None

    def test_hajj_requires_acwy_certificate(self):
        d = find_destination("going on Hajj")
        assert d.certificate == "meningococcal_acwy_hajj"
        assert "meningococcal_acwy" in d.vaccines_recommended

    def test_rows_complete(self):
        from gpdisc_core.travel_medicine.destinations import DESTINATIONS
        assert len(DESTINATIONS) == 24
        for d in DESTINATIONS:
            assert d.malaria_risk in ("none", "low", "high"), d.destination_id
            assert d.aliases and d.region


class TestProphylaxis:
    def test_ghana_gets_three_modern_options(self):
        d = find_destination("ghana")
        drugs = [o.drug for o in recommend_prophylaxis(d)]
        assert "Atovaquone/proguanil" in drugs and "Doxycycline" in drugs
        assert "Chloroquine" not in drugs  # resistance

    def test_mefloquine_excluded_with_psych_history(self):
        d = find_destination("ghana")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"psychiatric_history": True})]
        assert "Mefloquine" not in drugs

    def test_doxycycline_excluded_in_child(self):
        d = find_destination("thailand")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"age_years": 8})]
        assert "Doxycycline" not in drugs

    def test_pregnant_traveller_gets_mefloquine_only(self):
        d = find_destination("kenya")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"pregnant": True})]
        assert drugs == ["Mefloquine"]

    def test_no_malaria_no_options(self):
        d = find_destination("hajj")
        assert recommend_prophylaxis(d) == []


class TestPreTravelConsult:
    def test_plan_structure(self):
        plan = pre_travel_consult("two weeks in Ghana", {"age_years": 40})
        assert plan.destination == "ghana"
        assert plan.malaria["risk"] == "high"
        assert plan.certificate == "yellow_fever"
        assert any(v["vaccine"].startswith("yellow_fever") for v in plan.vaccines)
        assert plan.general  # bite avoidance etc.

    def test_ideal_timing_present(self):
        plan = pre_travel_consult("india")
        assert all("when" in v for v in plan.vaccines)


from gpdisc_core.travel_medicine import post_travel_screening


class TestPostTravel:
    def test_fbc_always(self):
        r = post_travel_screening("back from a week in Paris")
        assert r[0]["test"].startswith("FBC")

    def test_freshwater_adds_schistosomiasis(self):
        r = post_travel_screening("three weeks in Malawi, swam in Lake Malawi every day")
        tests = [x["test"] for x in r]
        assert any("Schistosoma" in x for x in tests)
        assert any("Strongyloides" in x for x in tests)

    def test_malarious_region_mentions_fever_rule(self):
        r = post_travel_screening("back from Ghana business trip")
        assert any("6 months" in x["when"] for x in r)

    def test_long_stay_adds_tb(self):
        r = post_travel_screening("volunteered in Kenya for six months")
        assert any("IGRA" in x["test"] for x in r)
