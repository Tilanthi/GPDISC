"""
Safe Medical Report Reader
==========================

Provides safe extraction of clinical measurements from medical reports (PDFs, etc.)
with built-in verification to prevent transcription errors.

CRITICAL: Always use this module when reading medical reports.
Never extract measurements manually without verification.

Author: GPDISC Safety Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
from datetime import datetime

from gpdisc_core.safety.medical_measurement_verification import (
    MedicalMeasurementVerifier,
    MeasurementCategory,
    VerificationResult,
    verify_measurement,
    halt_on_critical_discrepancy
)


class SafeMedicalReportReader:
    """
    Safe reader for medical reports with automatic measurement verification.

    This is the PRIMARY INTERFACE for reading medical reports safely.

    Usage:
        >>> reader = SafeMedicalReportReader(patient_id="patient123")
        >>> report = reader.read_and_verify("path/to/report.pdf")
        >>> print(report.get_verified_measurement("LVEF"))
        55.0
        >>> print(report.get_flags())
        []
    """

    def __init__(self, patient_id: str = None):
        """
        Initialize the safe report reader.

        Args:
            patient_id: Patient ID for loading historical data
        """
        self.patient_id = patient_id
        self.verifier = MedicalMeasurementVerifier(patient_id)
        self.verified_measurements: Dict[str, VerificationResult] = {}
        self.report_metadata: Dict = {}

    def read_and_verify(
        self,
        report_path: str,
        required_measurements: List[Tuple[str, MeasurementCategory, str]] = None,
        halt_on_error: bool = True
    ) -> 'VerifiedMedicalReport':
        """
        Read medical report and verify all measurements.

        Args:
            report_path: Path to medical report (PDF, text file, etc.)
            required_measurements: List of (name, category, unit) tuples
            halt_on_error: Whether to halt on critical discrepancies

        Returns:
            VerifiedMedicalReport with all verified measurements

        Raises:
            RuntimeError: If halt_on_error=True and critical verification fails
            FileNotFoundError: If report file doesn't exist
        """
        # Read the report
        text_content = self._read_report_file(report_path)

        # Store metadata
        self.report_metadata = {
            "file_path": report_path,
            "timestamp": datetime.now().isoformat(),
            "file_size": Path(report_path).stat().st_size if Path(report_path).exists() else 0
        }

        # If no specific measurements required, auto-detect common ones
        if required_measurements is None:
            required_measurements = self._auto_detect_measurements(text_content)

        # Verify each measurement
        for name, category, unit in required_measurements:
            result = self.verifier.extract_measurement(text_content, category, unit)

            self.verified_measurements[name] = result

            if halt_on_error and not result.is_verified:
                halt_on_critical_discrepancy(result)

        return VerifiedMedicalReport(
            metadata=self.report_metadata,
            measurements=self.verified_measurements,
            raw_text=text_content
        )

    def _read_report_file(self, file_path: str) -> str:
        """Read medical report file and extract text"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Report file not found: {file_path}")

        # Handle different file types
        suffix = path.suffix.lower()

        if suffix == '.pdf':
            return self._extract_from_pdf(file_path)
        elif suffix in ['.txt', '.md']:
            with open(file_path, 'r') as f:
                return f.read()
        elif suffix in ['.json']:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return json.dumps(data)
        else:
            # Try to read as text
            with open(file_path, 'r', errors='ignore') as f:
                return f.read()

    def _extract_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using multiple methods for robustness"""
        try:
            # Try PyPDF2 first
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except ImportError:
            pass

        try:
            # Try pdfplumber
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except ImportError:
            pass

        try:
            # Try pdfminer
            from pdfminer.high_level import extract_text
            return extract_text(pdf_path)
        except ImportError:
            pass

        # Fallback: warn user
        raise ImportError(
            "No PDF library available. Install one of: PyPDF2, pdfplumber, pdfminer"
        )

    def _auto_detect_measurements(
        self,
        text: str
    ) -> List[Tuple[str, MeasurementCategory, str]]:
        """Auto-detect common measurements in report"""
        detections = []

        # Check for LVEF/EF
        if any(term in text.lower() for term in ['lvef', 'ejection fraction', 'ef %']):
            detections.append(("LVEF", MeasurementCategory.EJECTION_FRACTION, "%"))

        # Check for aortic root
        if any(term in text.lower() for term in ['aortic root', 'sinus of valsalva', 'sov']):
            detections.append(("Aortic_Root", MeasurementCategory.AORTIC_DIMENSION, "mm"))

        # Check for blood pressure
        if 'blood pressure' in text.lower() or '/' in text:  # Simple heuristic
            detections.append(("BP", MeasurementCategory.BLOOD_PRESSURE, "mmHg"))

        # Check for heart rate
        if any(term in text.lower() for term in ['heart rate', 'pulse', 'hr', 'bpm']):
            detections.append(("HR", MeasurementCategory.HEART_RATE, "bpm"))

        return detections

    def get_verification_summary(self) -> Dict:
        """Get summary of verification results"""
        verified_count = sum(
            1 for r in self.verified_measurements.values() if r.is_verified
        )
        total_count = len(self.verified_measurements)

        return {
            "total_measurements": total_count,
            "verified": verified_count,
            "flagged": total_count - verified_count,
            "overall_confidence": (
                sum(r.confidence for r in self.verified_measurements.values()) / total_count
                if total_count > 0 else 0
            ),
            "critical_flags": [
                name for name, result in self.verified_measurements.items()
                if any(f in result.flags for f in ["DISCREPANT_EXTRACTIONS", "NO_EXTRACTION"])
            ]
        }


class VerifiedMedicalReport:
    """
    Container for verified medical report data.

    Provides safe access to verified measurements with full audit trail.
    """

    def __init__(
        self,
        metadata: Dict,
        measurements: Dict[str, VerificationResult],
        raw_text: str = None
    ):
        self.metadata = metadata
        self.measurements = measurements
        self.raw_text = raw_text

    def get_verified_measurement(self, name: str) -> Optional[float]:
        """
        Get verified measurement value.

        Returns None if measurement was not verified.
        """
        if name not in self.measurements:
            return None

        result = self.measurements[name]
        if result.is_verified:
            return result.verified_value

        return None

    def get_measurement_result(self, name: str) -> Optional[VerificationResult]:
        """Get full verification result for a measurement"""
        return self.measurements.get(name)

    def is_all_verified(self) -> bool:
        """Check if all measurements are verified"""
        return all(r.is_verified for r in self.measurements.values())

    def get_flags(self) -> Dict[str, List[str]]:
        """Get all flags from all measurements"""
        flags = {}
        for name, result in self.measurements.items():
            if result.flags:
                flags[name] = result.flags
        return flags

    def get_warnings(self) -> Dict[str, List[str]]:
        """Get all warnings from all measurements"""
        warnings = {}
        for name, result in self.measurements.items():
            if result.warnings:
                warnings[name] = result.warnings
        return warnings

    def export_report(self, filepath: str) -> None:
        """Export verified report to JSON"""
        export_data = {
            "metadata": self.metadata,
            "verified_at": datetime.now().isoformat(),
            "all_verified": self.is_all_verified(),
            "measurements": {
                name: {
                    "verified": result.is_verified,
                    "value": result.verified_value,
                    "confidence": result.confidence,
                    "flags": result.flags,
                    "warnings": result.warnings,
                    "raw_extractions": result.raw_extractions
                }
                for name, result in self.measurements.items()
            },
            "raw_text_sample": self.raw_text[:500] if self.raw_text else None
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

    def __repr__(self) -> str:
        verified = sum(1 for r in self.measurements.values() if r.is_verified)
        total = len(self.measurements)
        return f"<VerifiedMedicalReport {verified}/{total} verified>"


# Convenience function for one-time safe reading
def safely_read_report(
    report_path: str,
    patient_id: str = None,
    required_measurements: List[Tuple[str, MeasurementCategory, str]] = None
) -> VerifiedMedicalReport:
    """
    Safely read a medical report with automatic verification.

    This is the RECOMMENDED interface for most use cases.

    Args:
        report_path: Path to medical report
        patient_id: Optional patient ID for historical comparison
        required_measurements: Optional list of (name, category, unit) to extract

    Returns:
        VerifiedMedicalReport with all measurements verified

    Example:
        >>> report = safely_read_report(
        ...     "echo_report.pdf",
        ...     patient_id="patient123",
        ...     required_measurements=[
        ...         ("LVEF", MeasurementCategory.EJECTION_FRACTION, "%"),
        ...         ("Aortic_Root", MeasurementCategory.AORTIC_DIMENSION, "mm")
        ...     ]
        ... )
        >>> lvef = report.get_verified_measurement("LVEF")
        >>> if lvef is not None:
        ...     print(f"LVEF: {lvef}%")
        >>> if not report.is_all_verified():
        ...     print("WARNING: Some measurements could not be verified")
    """
    reader = SafeMedicalReportReader(patient_id)
    return reader.read_and_verify(report_path, required_measurements)


if __name__ == "__main__":
    # Test the safe reader
    print("Safe Medical Report Reader - Test Mode")
    print("=" * 60)

    # Create a test report file
    test_report = """
    CARDIOLOGY CLINICAL LETTER
    Date: 21 May 2026

    ECHOCARDIOGRAM REPORT (6th May 2026)
    =====================================

    LVEF: 55%
    Aortic root diameter: 42mm at sinus of Valsalva

    Additional findings:
    - Normal LV cavity size
    - Grade 0 diastolic function
    - No significant valvular disease
    """

    test_path = "/tmp/test_medical_report.txt"
    with open(test_path, 'w') as f:
        f.write(test_report)

    try:
        # Read and verify
        report = safely_read_report(
            test_path,
            required_measurements=[
                ("LVEF", MeasurementCategory.EJECTION_FRACTION, "%"),
                ("Aortic_Root", MeasurementCategory.AORTIC_DIMENSION, "mm")
            ]
        )

        print(f"\nVerification Results:")
        print(f"  All verified: {report.is_all_verified()}")
        print(f"  LVEF: {report.get_verified_measurement('LVEF')}%")
        print(f"  Aortic Root: {report.get_verified_measurement('Aortic_Root')}mm")
        print(f"  Flags: {report.get_flags()}")

        # Export report
        export_path = "/tmp/verified_report.json"
        report.export_report(export_path)
        print(f"\nExported verified report to: {export_path}")

        print("\n" + "=" * 60)
        print("✓ Safe reader operational")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
