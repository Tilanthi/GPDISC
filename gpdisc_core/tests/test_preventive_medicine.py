"""Tests for preventive_medicine (expertise program Stage 2)."""
import pytest
from gpdisc_core.preventive_medicine import (
    VACCINES_UK, SCREENING_UK, prevention_check, cvd_prevention_advice,
)


class TestTables:
    def test_table_sizes(self):
        assert len(VACCINES_UK) >= 12
        assert len(SCREENING_UK) == 8
        for s in SCREENING_UK:
            assert s.programme and s.cohort and s.test


class TestPreventionCheck:
    def test_68yo_man(self):
        due = [x["name"] for x in prevention_check({"age_years": 68, "sex": "m"})]
        assert "Bowel cancer screening (FIT)" in due
        assert "Abdominal aortic aneurysm" in due
        assert "Shingles (Shingrix)" in due
        assert "Influenza (annual)" in due

    def test_52yo_woman(self):
        due = [x["name"] for x in prevention_check({"age_years": 52, "sex": "f"})]
        assert "Breast cancer screening" in due
        assert "Cervical screening (HPV)" in due
        assert "Abdominal aortic aneurysm" not in due

    def test_pregnant_20w(self):
        due = [x["name"] for x in prevention_check(
            {"age_years": 30, "sex": "f", "pregnant": True})]
        assert "Pertussis (whooping cough)" in due
        assert "Antenatal screening" in due

    def test_aaa_done_not_due_again(self):
        due = [x["name"] for x in prevention_check(
            {"age_years": 68, "sex": "m", "aaa_done": True})]
        assert "Abdominal aortic aneurysm" not in due


class TestCVDPrevention:
    def test_qrisk_over_threshold_gets_statin_discussion(self):
        r = cvd_prevention_advice({"qrisk10": 14, "age_years": 62})
        assert any("statin" in x["name"].lower() for x in r)

    def test_on_statin_not_flagged(self):
        r = cvd_prevention_advice({"qrisk10": 14, "on_statin": True})
        assert not any("statin" in x["name"].lower() for x in r)

    def test_high_bp_needs_confirmation(self):
        r = cvd_prevention_advice({"systolic": 152})
        assert any("hypertension" in x["name"].lower() for x in r)

    def test_smoker_gets_cessation(self):
        r = cvd_prevention_advice({"smoker": True, "systolic": 120})
        assert any("smoking" in x["name"].lower() for x in r)

    def test_clean_patient_no_flags(self):
        assert cvd_prevention_advice({"qrisk10": 4, "systolic": 118}) == []
