"""
Regression tests for gpdisc_core.memory.patient_records.PatientRecordStore.

Local-only patient record storage. No external transmission.
Run from repo root:  python3 -m pytest gpdisc_core/tests/test_patient_records.py -v
"""

from datetime import date

import pytest

from gpdisc_core.memory.patient_records import (
    create_patient_record_store,
    ClinicalNote,
    ECGRecord,
)


def _cold_reload(storage_dir, patient_id):
    """Load with a brand-new store instance so the in-memory cache cannot
    mask a deserialization bug (PatientRecordStore caches loaded records)."""
    fresh = create_patient_record_store(storage_dir=storage_dir)
    return fresh.load_patient(patient_id)


def test_clinical_note_survives_save_and_cold_reload(tmp_path):
    """A stored ClinicalNote must round-trip through disk.

    Regression for the bug where _deserialize_record passed an unexpected
    `test_date` kwarg into ClinicalNote (which has no such field), crashing
    load_patient and silently returning None.
    """
    pid = "TEST_ROUNDTRIP_NOTE"
    store = create_patient_record_store(storage_dir=str(tmp_path))
    store.create_patient(pid)

    note = ClinicalNote(
        consultation_date=date(2026, 8, 13),
        consultation_type="GPDISC second-opinion consult",
        presenting_complaint="test complaint",
        diagnosis="test diagnosis",
        management_plan="test plan",
    )
    assert store.add_clinical_note(pid, note) is True

    reloaded = _cold_reload(str(tmp_path), pid)

    assert reloaded is not None, "cold reload returned None — deserializer crashed"
    assert len(reloaded.clinical_notes) == 1
    assert reloaded.clinical_notes[0].presenting_complaint == "test complaint"
    assert reloaded.clinical_notes[0].consultation_date == date(2026, 8, 13)


def test_ecg_survives_save_and_cold_reload(tmp_path):
    """ECG records must continue to round-trip (guardrail: the fix must not
    regress the record types that already worked)."""
    pid = "TEST_ROUNDTRIP_ECG"
    store = create_patient_record_store(storage_dir=str(tmp_path))
    store.create_patient(pid)

    ecg = ECGRecord(
        test_date=date(2026, 8, 12),
        indication="test indication",
        rhythm="sinus",
        rate=88,
        impression="test impression",
    )
    assert store.add_ecg(pid, ecg) is True

    reloaded = _cold_reload(str(tmp_path), pid)

    assert reloaded is not None
    assert len(reloaded.ecgs) == 1
    assert reloaded.ecgs[0].rate == 88
    assert reloaded.ecgs[0].test_date == date(2026, 8, 12)
