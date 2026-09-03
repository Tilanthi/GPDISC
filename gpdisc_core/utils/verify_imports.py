#!/usr/bin/env python3
"""
GPDISC Import Verification Script
==================================

This script verifies that all core GPDISC imports work correctly
without warnings or errors. It tests:

1. PDF Generator imports (multiple naming styles)
2. PDF generation imports
3. Physics engine imports
4. Core unified system imports

Run this script after making changes to GPDISC to verify imports work.
"""

import sys
import os

# Add GPDISC to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
biodisc_dir = os.path.dirname(os.path.dirname(script_dir))
if biodisc_dir not in sys.path:
    sys.path.insert(0, biodisc_dir)

# Suppress debug warnings during import verification
import logging
logging.basicConfig(level=logging.WARNING)

def test_pdf_generator_imports():
    """Test PDF generator with multiple naming styles."""
    print("Testing PDF Generator imports...")
    try:
        from gpdisc_core.utils.pdf_generator import (
            PDFGenerator,  # Recommended
            BIODISCPDFGenerator,  # Full GPDISC name
            ASTRAPDFGenerator,  # Legacy GPDISC name
            PDFStyles,
            BIODISCPDFStyles,
            ASTRAPDFStyles,
            MarkdownConverter,
            WrappedTableCell,
            create_pdf_from_markdown,
            REPORTLAB_AVAILABLE
        )

        # Verify they're the same class
        assert PDFGenerator is BIODISCPDFGenerator is ASTRAPDFGenerator
        assert PDFStyles is BIODISCPDFStyles is ASTRAPDFStyles

        print("  ✓ PDFGenerator")
        print("  ✓ BIODISCPDFGenerator")
        print("  ✓ ASTRAPDFGenerator (legacy)")
        print("  ✓ All aliases refer to same class")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_pdf_generator_functionality():
    """Test PDF generator functionality."""
    print("Testing PDF Generator functionality...")
    try:
        from gpdisc_core.utils.pdf_generator import PDFGenerator
        import tempfile
        import os

        # Create a test PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            pdf = PDFGenerator(temp_path)
            pdf.add_title('BIODISC Test Document')
            pdf.add_paragraph('Testing **bold** and *italic* text.')
            pdf.add_heading('Test Section', 2)
            pdf.add_paragraph('This is a test paragraph.')
            result = pdf.build()

            # Verify file was created
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0

            print(f"  ✓ PDF created: {os.path.basename(temp_path)}")
            print(f"  ✓ File size: {os.path.getsize(result)} bytes")
            return True
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_physics_imports():
    """Test physics engine imports."""
    print("Testing Physics Engine imports...")
    try:
        from gpdisc_core.physics import (
            UnifiedPhysicsEngine,
            PhysicsDomain,
            PhysicsConstraint,
            PhysicsResult
        )
        print("  ✓ UnifiedPhysicsEngine")
        print("  ✓ PhysicsDomain")
        print("  ✓ PhysicsConstraint")
        print("  ✓ PhysicsResult")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_core_unified_imports():
    """Test core unified system imports."""
    print("Testing Core Unified imports...")
    try:
        from gpdisc_core.core.unified import (
            TaskType,
            UnifiedConfig,
            UnifiedGPDISCSystem
        )
        print("  ✓ TaskType")
        print("  ✓ UnifiedConfig")
        print("  ✓ UnifiedGPDISCSystem")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def main():
    """Run all import verification tests."""
    print("="*60)
    print("BIODISC Import Verification")
    print("="*60)
    print()

    results = []

    # Run all tests
    results.append(("PDF Generator Imports", test_pdf_generator_imports()))
    results.append(("PDF Generator Functionality", test_pdf_generator_functionality()))
    results.append(("Physics Engine Imports", test_physics_imports()))
    results.append(("Core Unified Imports", test_core_unified_imports()))

    # Print summary
    print()
    print("="*60)
    print("Summary")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print()
        print("✓ All imports working correctly!")
        return 0
    else:
        print()
        print("✗ Some imports failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
