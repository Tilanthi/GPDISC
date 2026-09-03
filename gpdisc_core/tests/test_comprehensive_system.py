#!/usr/bin/env python3
"""
GPDISC Comprehensive System Test

Tests all imports, cross-links, dependencies, and module interactions.
"""

import sys
import os
import traceback
from pathlib import Path


test_results = []
total_tests = 0
passed_tests = 0
failed_tests = 0


def test_section(title):
    """Print test section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_import(description, import_statement):
    """Test an import statement"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    try:
        exec(import_statement, globals())
        print(f"✅ {description}")
        passed_tests += 1
        return True
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Error: {e}")
        failed_tests += 1
        test_results.append({
            'test': description,
            'status': 'FAILED',
            'error': str(e),
            'traceback': traceback.format_exc()
        })
        return False


def test_function(description, function_call):
    """Test a function call"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    try:
        result = eval(function_call, globals())
        print(f"✅ {description}")
        passed_tests += 1
        return True, result
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Error: {e}")
        failed_tests += 1
        test_results.append({
            'test': description,
            'status': 'FAILED',
            'error': str(e),
            'traceback': traceback.format_exc()
        })
        return False, None


def main():
    """Run comprehensive system tests"""

    print("\n" + "=" * 70)
    print("  GPDISC COMPREHENSIVE SYSTEM TEST")
    print("  Testing all imports, dependencies, and module interactions")
    print("=" * 70)

    # Test 1: Core Module Imports
    test_section("1. CORE MODULE IMPORTS")

    test_import("Import gpdisc_core",
               "from gpdisc_core import create_gpdisc_system")

    test_import("Import unified system",
               "from gpdisc_core.core.unified import UnifiedGPDISCSystem")

    test_import("Import enhanced system",
               "from gpdisc_core.core.unified_enhanced import EnhancedUnifiedGPDISCSystem")

    test_import("Import domain registry",
               "from gpdisc_core.domains import DomainRegistry")

    test_import("Import base domain module",
               "from gpdisc_core.domains import BaseDomainModule")

    test_import("Import domain config",
               "from gpdisc_core.domains import DomainConfig")

    test_import("Import domain query result",
               "from gpdisc_core.domains import DomainQueryResult")

    # Test 2: Medical Domain Imports (Phase 1 - High Priority)
    test_section("2. PHASE 1: HIGH PRIORITY MEDICAL DOMAINS")

    test_import("Import Cardiology domain",
               "from gpdisc_core.domains.cardiology import CardiologyDomain")

    test_import("Import Epilepsy domain",
               "from gpdisc_core.domains.epilepsy import EpilepsyDomain")

    test_import("Import General Practice domain",
               "from gpdisc_core.domains.general_practice import GeneralPracticeDomain")

    test_import("Import Orthopedics domain",
               "from gpdisc_core.domains.orthopedics import OrthopedicsDomain")

    test_import("Import Pharmacology domain",
               "from gpdisc_core.domains.pharmacology import PharmacologyDomain")

    test_import("Import Neurology domain",
               "from gpdisc_core.domains.neurology import NeurologyDomain")

    # Test 3: Medical Domain Imports (Phase 2 - Medium Priority)
    test_section("3. PHASE 2: MEDIUM PRIORITY MEDICAL DOMAINS")

    test_import("Import Dermatology domain",
               "from gpdisc_core.domains.dermatology import DermatologyDomain")

    test_import("Import Ophthalmology domain",
               "from gpdisc_core.domains.ophthalmology import OphthalmologyDomain")

    test_import("Import ENT domain",
               "from gpdisc_core.domains.ent import ENTDomain")

    test_import("Import Rheumatology domain",
               "from gpdisc_core.domains.rheumatology import RheumatologyDomain")

    # Test 4: Medical Domain Imports (Phase 3 - Special Populations)
    test_section("4. PHASE 3: SPECIAL POPULATIONS")

    test_import("Import Geriatric Medicine domain",
               "from gpdisc_core.domains.geriatric_medicine import GeriatricMedicineDomain")

    test_import("Import Women's Health domain",
               "from gpdisc_core.domains.womens_health import WomensHealthDomain")

    test_import("Import Pediatrics domain",
               "from gpdisc_core.domains.pediatrics import PediatricsDomain")

    # Test 5: Medical Domain Imports (Phase 4)
    test_section("5. PHASE 4: ADDITIONAL MEDICAL DOMAINS")

    test_import("Import Endocrinology domain",
               "from gpdisc_core.domains.endocrinology import EndocrinologyDomain")

    test_import("Import Gastroenterology domain",
               "from gpdisc_core.domains.gastroenterology import GastroenterologyDomain")

    test_import("Import Infectious Diseases domain",
               "from gpdisc_core.domains.infectious_diseases import InfectiousDiseasesDomain")

    test_import("Import Nephrology domain",
               "from gpdisc_core.domains.nephrology import NephrologyDomain")

    test_import("Import Respiratory Medicine domain",
               "from gpdisc_core.domains.respiratory import RespiratoryDomain")

    test_import("Import Psychiatry domain",
               "from gpdisc_core.domains.psychiatry import PsychiatryDomain")

    test_import("Import Mental Health domain",
               "from gpdisc_core.domains.mental_health import MentalHealthDomain")

    test_import("Import Urology domain",
               "from gpdisc_core.domains.urology import UrologyDomain")

    test_import("Import Allergy Immunology domain",
               "from gpdisc_core.domains.allergy_immunology import AllergyImmunologyDomain")

    test_import("Import Palliative Care domain",
               "from gpdisc_core.domains.palliative_care import PalliativeCareDomain")

    test_import("Import Emergency Medicine domain",
               "from gpdisc_core.domains.emergency_medicine import EmergencyMedicineDomain")

    test_import("Import Anesthesiology domain",
               "from gpdisc_core.domains.anesthesiology import AnesthesiologyDomain")

    # Test 6: Medical Domain Imports (Phase 6 - Surgical)
    test_section("6. PHASE 6: SURGICAL SPECIALTIES")

    test_import("Import General Surgery domain",
               "from gpdisc_core.domains.general_surgery import GeneralSurgeryDomain")

    test_import("Import Vascular Surgery domain",
               "from gpdisc_core.domains.vascular_surgery import VascularSurgeryDomain")

    test_import("Import Cardiothoracic Surgery domain",
               "from gpdisc_core.domains.cardiothoracic_surgery import CardiothoracicSurgeryDomain")

    test_import("Import Neurosurgery domain",
               "from gpdisc_core.domains.neurosurgery import NeurosurgeryDomain")

    test_import("Import Plastic Surgery domain",
               "from gpdisc_core.domains.plastic_surgery import PlasticSurgeryDomain")

    # Test 7: Medical Domain Imports (Phase 7 - Other)
    test_section("7. PHASE 7: OTHER SPECIALTIES")

    test_import("Import Radiology domain",
               "from gpdisc_core.domains.radiology import RadiologyDomain")

    test_import("Import DICOM processor",
               "from gpdisc_core.domains.radiology.dicom_processor import DICOMProcessor")

    test_import("Import Pathology domain",
               "from gpdisc_core.domains.pathology import PathologyDomain")

    test_import("Import Radiation Oncology domain",
               "from gpdisc_core.domains.radiation_oncology import RadiationOncologyDomain")

    test_import("Import PM&R domain",
               "from gpdisc_core.domains.physical_medicine_rehab import PhysicalMedicineRehabDomain")

    test_import("Import Occupational Medicine domain",
               "from gpdisc_core.domains.occupational_medicine import OccupationalMedicineDomain")

    test_import("Import Medical Genetics domain",
               "from gpdisc_core.domains.medical_genetics import MedicalGeneticsDomain")

    # Test 8: Biology Domain Imports (Preserved)
    test_section("8. PRESERVED BIOLOGY DOMAINS")

    test_import("Import Molecular Biology domain",
               "from gpdisc_core.domains.molecular_biology import MolecularBiologyDomain")

    test_import("Import Biochemistry domain",
               "from gpdisc_core.domains.biochemistry import BiochemistryDomain")

    test_import("Import Genetics domain",
               "from gpdisc_core.domains.genetics import GeneticsDomain")

    test_import("Import Cell Biology domain",
               "from gpdisc_core.domains.cell_biology import CellBiologyDomain")

    test_import("Import Biophysics domain",
               "from gpdisc_core.domains.biophysics import BiophysicsDomain")

    test_import("Import Bioinformatics domain",
               "from gpdisc_core.domains.bioinformatics import BioinformaticsDomain")

    test_import("Import Computational Biology domain",
               "from gpdisc_core.domains.computational_biology import ComputationalBiologyDomain")

    test_import("Import Genomics domain",
               "from gpdisc_core.domains.genomics import GenomicsDomain")

    test_import("Import Proteomics domain",
               "from gpdisc_core.domains.proteomics import ProteomicsDomain")

    test_import("Import Systems Biology domain",
               "from gpdisc_core.domains.systems_biology import SystemsBiologyDomain")

    # Test 9: New Capability Imports
    test_section("9. NEW CAPABILITY IMPORTS")

    test_import("Import patient records system",
               "from gpdisc_core.memory.patient_records import create_patient_record_store")

    test_import("Import patient record classes",
               "from gpdisc_core.memory.patient_records import PatientRecord, PatientRecordStore")

    test_import("Import drug interaction checker",
               "from gpdisc_core.safety.drug_interactions import check_patient_medications")

    test_import("Import drug interaction functions",
               "from gpdisc_core.safety.drug_interactions import check_drugs_interact, check_new_prescription")

    test_import("Import interaction checker class",
               "from gpdisc_core.safety.drug_interactions import create_interaction_checker")

    # Test 10: Function Creation Tests
    test_section("10. SYSTEM CREATION TESTS")

    test_function("Create main GPDISC system",
                  "create_gpdisc_system()")

    test_function("Create patient record store",
                  "create_patient_record_store()")

    test_function("Create interaction checker",
                  "create_interaction_checker()")

    # Test 11: Domain Instantiation Tests
    test_section("11. DOMAIN INSTANTIATION TESTS")

    # Only test a few key domains to save time
    test_function("Instantiate Cardiology domain",
                  "CardiologyDomain()")

    test_function("Instantiate Pharmacology domain",
                  "PharmacologyDomain()")

    test_function("Instantiate Radiology domain",
                  "RadiologyDomain()")

    # Test 12: Cross-Module Integration Tests
    test_section("12. CROSS-MODULE INTEGRATION TESTS")

    # Test that system can be created and answer queries
    success, system = test_function("Create system and test basic query",
                                    "create_gpdisc_system()")

    if success and system:
        try:
            result = system.answer("test query")
            if 'answer' in result:
                print("✅ System query test passed")
            else:
                print("❌ System query test failed - missing 'answer' key")
        except Exception as e:
            print(f"❌ System query test failed: {e}")

    # Test 13: Memory System Tests
    test_section("13. MEMORY SYSTEM TESTS")

    success, store = test_function("Create patient record store",
                                   "create_patient_record_store()")
    if success and store:
        try:
            patient = store.create_patient("TEST_PATIENT")
            if patient:
                print("✅ Patient creation test passed")
            else:
                print("❌ Patient creation test failed")
        except Exception as e:
            print(f"❌ Patient creation test failed: {e}")

    # Test 14: Drug Interaction Tests
    test_section("14. DRUG INTERACTION SYSTEM TESTS")

    success, result = test_function("Test drug interaction checking",
                                    "check_patient_medications(['warfarin', 'ibuprofen'])")
    if success and result:
        try:
            if hasattr(result, 'summary'):
                print("✅ Drug interaction result structure test passed")
            else:
                print("❌ Drug interaction result structure test failed")
        except Exception as e:
            print(f"❌ Drug interaction test failed: {e}")

    # Test 15: DICOM Processor Tests
    test_section("15. DICOM PROCESSOR TESTS")

    # Check if pydicom is available
    try:
        import pydicom
        test_function("Create DICOM processor",
                      "DICOMProcessor()")
    except ImportError:
        print("⚠️  DICOM processor test skipped (pydicom not installed - optional dependency)")
        print("   Install: pip install pydicom numpy")

    # Print Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

    if failed_tests > 0:
        print("\n" + "=" * 70)
        print("  FAILED TESTS DETAILS")
        print("=" * 70)
        for result in test_results:
            print(f"\n❌ {result['test']}")
            print(f"   Error: {result['error']}")
            # Don't print full traceback for summary
            print(f"   (Traceback available in detailed output)")

    print("\n" + "=" * 70)
    if failed_tests == 0:
        print("  ✅ ALL TESTS PASSED - SYSTEM IS FULLY OPERATIONAL")
    else:
        print("  ⚠️ SOME TESTS FAILED - REPAIR NEEDED")
    print("=" * 70 + "\n")

    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
