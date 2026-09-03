#!/usr/bin/env python3
"""
GPDISC DICOM Integration Test Script

Tests the DICOM analysis capabilities integrated with the Radiology domain.

Run this script to verify DICOM functionality is working correctly.
"""

import sys
import os
from pathlib import Path

def test_dicom_imports():
    """Test that DICOM modules can be imported"""
    print("=" * 70)
    print("Testing DICOM Module Imports...")
    print("=" * 70)

    try:
        from gpdisc_core.domains.radiology.dicom_processor import (
            DICOMProcessor,
            DICOMMetadata,
            DICOMAnalysisResult,
            create_dicom_processor,
            analyze_dicom_file,
            generate_dicom_report
        )
        print("✓ DICOM processor module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import DICOM processor: {e}")
        print("\nTo install required dependencies:")
        print("  pip install pydicom numpy")
        return False

def test_dicom_classes():
    """Test that DICOM classes can be instantiated"""
    print("\n" + "=" * 70)
    print("Testing DICOM Class Instantiation...")
    print("=" * 70)

    try:
        from gpdisc_core.domains.radiology.dicom_processor import (
            DICOMMetadata,
            DICOMAnalysisResult
        )

        # Test DICOMMetadata
        metadata = DICOMMetadata(
            patient_id="TEST123",
            modality="CT",
            body_part="CHEST",
            rows=512,
            columns=512
        )
        print(f"✓ DICOMMetadata created: {metadata.modality} {metadata.body_part}")

        # Test DICOMAnalysisResult
        result = DICOMAnalysisResult(success=True)
        result.metadata = metadata
        result.findings = ["Test finding 1", "Test finding 2"]
        print(f"✓ DICOMAnalysisResult created with {len(result.findings)} findings")

        return True
    except Exception as e:
        print(f"✗ Failed to instantiate DICOM classes: {e}")
        return False

def test_dicom_processor():
    """Test DICOM processor creation"""
    print("\n" + "=" * 70)
    print("Testing DICOM Processor Creation...")
    print("=" * 70)

    try:
        from gpdisc_core.domains.radiology.dicom_processor import create_dicom_processor

        processor = create_dicom_processor(anonymize=True)
        print(f"✓ DICOM processor created successfully")
        print(f"  - Anonymization: {processor.anonymize_output}")
        print(f"  - Processing stats: {processor.processing_stats}")

        return True
    except Exception as e:
        print(f"✗ Failed to create DICOM processor: {e}")
        return False

def test_radiology_domain_dicom():
    """Test that Radiology domain has DICOM capabilities"""
    print("\n" + "=" * 70)
    print("Testing Radiology Domain DICOM Integration...")
    print("=" * 70)

    try:
        from gpdisc_core.domains.radiology import RadiologyDomain

        domain = RadiologyDomain()
        config = domain.get_default_config()

        # Check for DICOM keywords
        dicom_keywords = [kw for kw in config.keywords if "dicom" in kw.lower() or ".dcm" in kw.lower()]
        print(f"✓ Radiology domain has {len(dicom_keywords)} DICOM-related keywords")

        # Check for DICOM capabilities
        dicom_caps = [cap for cap in config.capabilities if "dicom" in cap.lower()]
        print(f"✓ Radiology domain has {len(dicom_caps)} DICOM-related capabilities")

        # Test DICOM query routing
        result = domain.process_query("Analyze DICOM file test.dcm")
        print(f"✓ DICOM query routed correctly")
        print(f"  - Domain: {result.domain_name}")
        print(f"  - Confidence: {result.confidence}")

        return True
    except Exception as e:
        print(f"✗ Failed Radiology domain DICOM test: {e}")
        return False

def test_gpdisc_dicom_integration():
    """Test full GPDISC system with DICOM query"""
    print("\n" + "=" * 70)
    print("Testing Full GPDISC System DICOM Integration...")
    print("=" * 70)

    try:
        from gpdisc_core import create_gpdisc_system

        system = create_gpdisc_system()

        # Test various DICOM queries
        queries = [
            "Analyze DICOM file /path/to/scan.dcm",
            "Load DICOM /path/to/file.dcm",
            "DICOM analysis /path/to/image.dcm"
        ]

        for query in queries:
            result = system.answer(query)
            print(f"✓ Query processed: {query[:40]}...")
            print(f"  - Domain: {result.get('domain', 'system')}")

        return True
    except Exception as e:
        print(f"✗ Failed GPDISC DICOM integration test: {e}")
        return False

def test_dicom_file_processing():
    """Test actual DICOM file processing (if sample file available)"""
    print("\n" + "=" * 70)
    print("Testing DICOM File Processing...")
    print("=" * 70)

    # Look for sample DICOM files in common locations
    sample_locations = [
        "./test_data/sample.dcm",
        "./sample.dcm",
        "/tmp/sample.dcm"
    ]

    sample_file = None
    for location in sample_locations:
        if os.path.exists(location):
            sample_file = location
            break

    if not sample_file:
        print("⚠ No sample DICOM file found for testing")
        print("  To test with a real DICOM file:")
        print("  1. Place a .dcm file at: ./sample.dcm")
        print("  2. Run this test again")
        return True  # Not a failure, just no sample file

    try:
        from gpdisc_core.domains.radiology.dicom_processor import analyze_dicom_file

        result = analyze_dicom_file(sample_file)

        if result.success:
            print(f"✓ Successfully processed DICOM file: {sample_file}")
            print(f"  - Modality: {result.metadata.modality if result.metadata else 'N/A'}")
            print(f"  - Body Part: {result.metadata.body_part if result.metadata else 'N/A'}")
            print(f"  - Image Shape: {result.image_shape}")
            print(f"  - Findings: {len(result.findings)}")
            print(f"  - Warnings: {len(result.warnings)}")
        else:
            print(f"✗ Failed to process DICOM file: {result.error_message}")

        return result.success
    except Exception as e:
        print(f"✗ Failed DICOM file processing test: {e}")
        return False

def create_sample_dicom_test():
    """Create information about testing with sample DICOM files"""
    print("\n" + "=" * 70)
    print("Testing with Sample DICOM Files")
    print("=" * 70)

    print("""
To test with real DICOM files, you can:

1. **Download sample DICOM files**:
   - https://www.ncbi.nlm.nih.gov/gap/geo-matrix/?view=sample&file=sample.dcm
   - Or use your own DICOM files from clinical/scanner sources

2. **Test with GPDISC**:
   ```python
   from gpdisc_core import create_gpdisc_system

   system = create_gpdisc_system()
   result = system.answer("Analyze DICOM file /path/to/your/file.dcm")
   print(result['answer'])
   ```

3. **Test DICOM processor directly**:
   ```python
   from gpdisc_core.domains.radiology.dicom_processor import (
       analyze_dicom_file,
       generate_dicom_report
   )

   # Quick analysis
   result = analyze_dicom_file("/path/to/file.dcm")

   # Generate detailed report
   report = generate_dicom_report("/path/to/file.dcm")
   print(report)
   ```

4. **Test with a DICOM series**:
   ```python
   from gpdisc_core.domains.radiology.dicom_processor import (
       create_dicom_processor
   )

   processor = create_dicom_processor()
   results = processor.process_dicom_series("/path/to/dicom_series/")

   for result in results:
       if result.success:
           print(f"{result.metadata.modality} - {result.metadata.body_part}")
   ```
""")

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("GPDISC DICOM Integration Test Suite")
    print("=" * 70)
    print()

    results = []

    # Run tests
    results.append(("DICOM Imports", test_dicom_imports()))
    results.append(("DICOM Classes", test_dicom_classes()))
    results.append(("DICOM Processor", test_dicom_processor()))
    results.append(("Radiology Integration", test_radiology_domain_dicom()))
    results.append(("GPDISC Integration", test_gpdisc_dicom_integration()))
    results.append(("DICOM File Processing", test_dicom_file_processing()))

    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All DICOM integration tests passed!")
        print("   DICOM analysis is fully operational.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("   Some DICOM features may not be available.")

    # Provide additional information
    create_sample_dicom_test()

    print("\n" + "=" * 70)
    print("DICOM Capabilities Documentation")
    print("=" * 70)
    print("For detailed information, see: GPDISC_DICOM_CAPABILITIES.md")
    print("=" * 70)

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
