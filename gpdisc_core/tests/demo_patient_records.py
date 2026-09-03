#!/usr/bin/env python3
"""
GPDISC Patient Record System Demonstration

Demonstrates the patient record memory system with cross-session persistence.

All data is stored locally - no external transmission.
"""

from datetime import date, datetime
from gpdisc_core.memory.patient_records import (
    create_patient_record_store,
    PatientDemographics,
    BloodTestResult,
    ECGRecord,
    ImagingReport,
    MedicationRecord,
    ClinicalNote,
    AllergyRecord,
    DiagnosisRecord
)


def demo_create_patient():
    """Demonstrate creating a new patient record"""
    print("=" * 70)
    print("Creating New Patient Record")
    print("=" * 70)

    store = create_patient_record_store()

    # Create a new patient
    patient_id = "PATIENT001"
    record = store.create_patient(patient_id)

    # Add demographics
    demographics = PatientDemographics(
        patient_id=patient_id,
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1980, 5, 15),
        sex="M",
        blood_group="O+",
        nhs_number="1234567890"
    )
    store.add_demographics(patient_id, demographics)

    print(f"✓ Created patient: {patient_id}")
    print(f"  Name: {demographics.first_name} {demographics.last_name}")
    print(f"  DOB: {demographics.date_of_birth}")
    print(f"  Blood Group: {demographics.blood_group}")

    return patient_id, store


def demo_add_blood_tests(patient_id: str, store):
    """Demonstrate adding blood test results"""
    print("\n" + "=" * 70)
    print("Adding Blood Test Results")
    print("=" * 70)

    # Recent blood test
    blood_test = BloodTestResult(
        test_date=date.today(),
        test_name="Full Blood Count & U&Es",
        results={
            "Haemoglobin": "145 g/L",
            "WBC": "7.5 x10^9/L",
            "Platelets": "250 x10^9/L",
            "Sodium": "140 mmol/L",
            "Potassium": "4.2 mmol/L",
            "Creatinine": "85 μmol/L",
            "eGFR": ">90 mL/min"
        },
        reference_ranges={
            "Haemoglobin": "130-180 g/L",
            "WBC": "4.0-11.0 x10^9/L",
            "Platelets": "150-400 x10^9/L"
        },
        abnormal_flags=[],
        notes="All results within normal range",
        requesting_clinician="Dr Smith",
        laboratory="City Hospital Laboratory"
    )

    store.add_blood_test(patient_id, blood_test)
    print(f"✓ Added blood test: {blood_test.test_name}")
    print(f"  Date: {blood_test.test_date}")
    print(f"  Key results: Hb {blood_test.results['Haemoglobin']}, "
          f"K {blood_test.results['Potassium']}")


def demo_add_ecg(patient_id: str, store):
    """Demonstrate adding ECG records"""
    print("\n" + "=" * 70)
    print("Adding ECG Record")
    print("=" * 70)

    ecg = ECGRecord(
        test_date=date.today(),
        indication="Routine cardiac assessment",
        rhythm="Sinus rhythm",
        rate=72,
        axis="Normal",
        pr_interval="160ms",
        qrs_duration="90ms",
        qt_interval="400ms",
        qt_corrected="420ms",
        findings=[
            "Sinus rhythm",
            "Normal axis",
            "No significant conduction abnormality",
            "Normal QTc"
        ],
        impression="Normal ECG",
        interpretation="Normal sinus rhythm. No acute ischemic changes.",
        reporting_clinician="Dr Jones (Cardiologist)"
    )

    store.add_ecg(patient_id, ecg)
    print(f"✓ Added ECG: {ecg.rhythm}, HR {ecg.rate} bpm")
    print(f"  Impression: {ecg.impression}")


def demo_add_imaging(patient_id: str, store):
    """Demonstrate adding imaging reports"""
    print("\n" + "=" * 70)
    print("Adding Imaging Report")
    print("=" * 70)

    ct_chest = ImagingReport(
        test_date=date(2024, 5, 1),
        modality="CT",
        body_part="Chest",
        indication="Chronic cough",
        findings="""
        CT Chest:
        - No focal lung lesion
        - No mediastinal mass
        - No significant lymphadenopathy
        - Heart size normal
        - No pleural or pericardial effusion
        """,
        impression="No acute abnormality detected",
        radiologist="Dr Williams",
        hospital="City Hospital Radiology"
    )

    store.add_imaging_report(patient_id, ct_chest)
    print(f"✓ Added imaging: {ct_chest.modality} {ct_chest.body_part}")
    print(f"  Impression: {ct_chest.impression}")


def demo_add_medications(patient_id: str, store):
    """Demonstrate adding medications"""
    print("\n" + "=" * 70)
    print("Adding Medications")
    print("=" * 70)

    medications = [
        MedicationRecord(
            medication_name="Atorvastatin",
            dose="20mg",
            frequency="Nocte",
            route="PO",
            start_date=date(2023, 1, 15),
            indication="Hypercholesterolaemia",
            prescriber="Dr Smith",
            active=True
        ),
        MedicationRecord(
            medication_name="Ramipril",
            dose="2.5mg",
            frequency="OD",
            route="PO",
            start_date=date(2023, 1, 15),
            indication="Hypertension",
            prescriber="Dr Smith",
            active=True
        )
    ]

    for med in medications:
        store.add_medication(patient_id, med)
        print(f"✓ Added medication: {med.medication_name} {med.dose} {med.frequency}")


def demo_add_allergies(patient_id: str, store):
    """Demonstrate adding allergies"""
    print("\n" + "=" * 70)
    print("Adding Allergies")
    print("=" * 70)

    allergy = AllergyRecord(
        allergen="Penicillin",
        allergy_type="drug",
        reaction="Rash",
        severity="mild",
        date_noted=date(2020, 3, 10),
        source="patient_reported",
        active=True
    )

    store.add_allergy(patient_id, allergy)
    print(f"✓ Added allergy: {allergy.allergen}")
    print(f"  Reaction: {allergy.reaction} ({allergy.severity})")


def demo_add_diagnosis(patient_id: str, store):
    """Demonstrate adding diagnoses"""
    print("\n" + "=" * 70)
    print("Adding Diagnoses")
    print("=" * 70)

    diagnoses = [
        DiagnosisRecord(
            diagnosis_date=date(2023, 1, 10),
            diagnosis="Essential hypertension",
            icd10_code="I10",
            status="chronic",
            certainty="confirmed",
            clinician="Dr Smith",
            notes="Well controlled on Ramipril"
        ),
        DiagnosisRecord(
            diagnosis_date=date(2023, 1, 10),
            diagnosis="Hypercholesterolaemia",
            icd10_code="E78.0",
            status="chronic",
            certainty="confirmed",
            clinician="Dr Smith",
            notes="Statin therapy initiated"
        )
    ]

    for diagnosis in diagnoses:
        store.add_diagnosis(patient_id, diagnosis)
        print(f"✓ Added diagnosis: {diagnosis.diagnosis} ({diagnosis.status})")


def demo_add_clinical_note(patient_id: str, store):
    """Demonstrate adding clinical notes"""
    print("\n" + "=" * 70)
    print("Adding Clinical Note")
    print("=" * 70)

    note = ClinicalNote(
        consultation_date=date.today(),
        consultation_type="GP Review",
        presenting_complaint="Routine review of chronic conditions",
        history_of_presenting_complaint="""
        Patient attending for 3-monthly review of hypertension and
        hypercholesterolaemia. Reports good adherence to medications.
        No side effects reported.
        """,
        examination_findings="""
        BP: 128/78 mmHg (well controlled)
        HR: 72 bpm regular
        Cardiovascular: Normal heart sounds, no peripheral oedema
        """,
        diagnosis="Hypertension and hypercholesterolaemia well controlled",
        management_plan="""
        - Continue current medications
        - Repeat bloods in 3 months
        - Review in clinic in 3 months
        """,
        investigations_ordered=["FBC & U&Es", "Lipid profile"],
        medications_prescribed=["Atorvastatin 20mg", "Ramipril 2.5mg"],
        follow_up="3 months",
        clinician="Dr Smith"
    )

    store.add_clinical_note(patient_id, note)
    print(f"✓ Added clinical note: {note.consultation_type}")
    print(f"  Diagnosis: {note.diagnosis}")


def demo_get_summary(patient_id: str, store):
    """Demonstrate getting patient summary"""
    print("\n" + "=" * 70)
    print("Patient Summary")
    print("=" * 70)

    summary = store.get_patient_summary(patient_id)

    if summary:
        print(f"\nPatient: {summary['demographics']['name']}")
        print(f"DOB: {summary['demographics']['date_of_birth']}")
        print(f"Sex: {summary['demographics']['sex']}")
        print(f"Blood Group: {summary['demographics']['blood_group']}")

        print(f"\nActive Medications ({len(summary['active_medications'])}):")
        for med in summary['active_medications']:
            print(f"  - {med['name']} {med['dose']} {med['frequency']}")

        print(f"\nAllergies ({len(summary['allergies'])}):")
        for allergy in summary['allergies']:
            print(f"  - {allergy['allergen']}: {allergy['reaction']} ({allergy['severity']})")

        print(f"\nActive Diagnoses:")
        for dx in summary['recent_diagnoses']:
            print(f"  - {dx['diagnosis']}")

        print(f"\nRecord Counts:")
        for record_type, count in summary['record_counts'].items():
            print(f"  - {record_type}: {count}")


def demo_cross_session_persistence(patient_id: str):
    """Demonstrate that records persist across sessions"""
    print("\n" + "=" * 70)
    print("Cross-Session Persistence Test")
    print("=" * 70)

    # Simulate new session by creating a new store instance
    new_store = create_patient_record_store()

    # Load patient from "new session"
    record = new_store.load_patient(patient_id)

    if record:
        print(f"✓ Successfully loaded patient from 'new session'")
        print(f"  Patient: {record.demographics.first_name} {record.demographics.last_name}")
        print(f"  Records: {len(record.clinical_notes)} notes, "
              f"{len(record.blood_tests)} blood tests, "
              f"{len(record.medications)} medications")
        print(f"\n  ✓ Data persisted across sessions!")
    else:
        print("✗ Failed to load patient from new session")


def demo_consultation_integration():
    """Demonstrate integration with medical consultation"""
    print("\n" + "=" * 70)
    print("Integration with Medical Consultation")
    print("=" * 70)

    from gpdisc_core import create_gpdisc_system

    system = create_gpdisc_system()
    store = create_patient_record_store()

    # Get patient summary
    patient_id = "PATIENT001"
    summary = store.get_patient_summary(patient_id)

    if summary:
        # Construct consultation query with patient context
        context = f"""
Patient Context:
- Name: {summary['demographics']['name']}
- Age: 44 years (born {summary['demographics']['date_of_birth']})
- Active Medications: {', '.join([m['name'] for m in summary['active_medications']])}
- Allergies: {', '.join([a['allergen'] for a in summary['allergies']])}
- Diagnoses: {', '.join([d['diagnosis'] for d in summary['recent_diagnoses']])}
- Latest bloods: {summary['latest_blood_tests'][-1]['test_name'] if summary['latest_blood_tests'] else 'None'}
        """

        query = f"Patient on Atorvastatin and Ramipril. Reviewing blood test results. Any concerns?"

        print(f"\nConsultation Query: {query}")
        print(f"\nPatient Context Provided:")
        print(context)

        # Get consultation
        result = system.answer(query)
        print(f"\nConsultation Response:")
        print(result['answer'][:300] + "...")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("GPDISC Patient Record System Demonstration")
    print("=" * 70)
    print("\nPrivacy Notice:")
    print("- All patient data stored locally")
    print("- No external API calls or data transmission")
    print("- Records persist across sessions")
    print("=" * 70)

    # Create patient and add records
    patient_id, store = demo_create_patient()
    demo_add_blood_tests(patient_id, store)
    demo_add_ecg(patient_id, store)
    demo_add_imaging(patient_id, store)
    demo_add_medications(patient_id, store)
    demo_add_allergies(patient_id, store)
    demo_add_diagnosis(patient_id, store)
    demo_add_clinical_note(patient_id, store)

    # Get summary
    demo_get_summary(patient_id, store)

    # Test cross-session persistence
    demo_cross_session_persistence(patient_id)

    # Integration with consultation
    demo_consultation_integration()

    print("\n" + "=" * 70)
    print("Demonstration Complete")
    print("=" * 70)
    print("\nPatient records stored locally at:")
    print(f"  {store.storage_dir}")
    print("\nRecords will persist across sessions.")
    print("All data is private and local-only.")
    print("=" * 70)


if __name__ == "__main__":
    main()
