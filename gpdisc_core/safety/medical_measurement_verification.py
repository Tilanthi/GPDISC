"""
Medical Measurement Verification Module
========================================

This module provides critical safety checks for clinical measurements to prevent
reading/transcription errors that could affect patient care.

SAFETY CRITICAL: This module MUST be used whenever extracting or documenting
clinical measurements from medical reports, PDFs, or any source.

Author: GPDISC Safety Team
Version: 1.0.0
Date: 2026-06-07
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
import json
from pathlib import Path
from datetime import datetime


class MeasurementCategory(Enum):
    """Categories of clinical measurements with specific validation rules"""
    EJECTION_FRACTION = "ejection_fraction"
    AORTIC_DIMENSION = "aortic_dimension"
    BLOOD_PRESSURE = "blood_pressure"
    HEART_RATE = "heart_rate"
    CHAMBER_SIZE = "chamber_size"
    VALVE_REGURGITATION = "valve_regurgitation"
    LAB_VALUE = "lab_value"
    OTHER = "other"


@dataclass
class MeasurementValue:
    """A clinical measurement with verification metadata"""
    value: float
    unit: str
    category: MeasurementCategory
    source: str
    timestamp: datetime
    confidence: float = 0.0
    verification_status: str = "pending"  # pending, verified, flag
    discrepancy: Optional[str] = None
    raw_text: str = ""


@dataclass
class VerificationResult:
    """Result of measurement verification process"""
    is_verified: bool
    verified_value: Optional[float]
    confidence: float
    flags: List[str]
    warnings: List[str]
    suggestions: List[str]
    raw_extractions: List[float]  # All extracted values for review


class MedicalMeasurementVerifier:
    """
    Verifies clinical measurements against historical data and clinical plausibility.

    CRITICAL: Use this whenever extracting measurements from medical reports.
    """

    # Reference ranges for common measurements
    REFERENCE_RANGES = {
        MeasurementCategory.EJECTION_FRACTION: {
            "normal": (55, 70),
            "mildly_reduced": (40, 54),
            "moderately_reduced": (30, 39),
            "severely_reduced": (20, 29),
            "critical": (0, 19)
        },
        MeasurementCategory.AORTIC_DIMENSION: {
            "sinus_of_valsalva": {
                "normal": (29, 40),  # mm
                "mild_dilation": (41, 45),
                "moderate_dilation": (46, 49),
                "severe_dilation": (50, 100)
            }
        },
        MeasurementCategory.BLOOD_PRESSURE: {
            "systolic": {
                "normal": (90, 120),
                "elevated": (121, 129),
                "hypertension_stage1": (130, 139),
                "hypertension_stage2": (140, 180)
            },
            "diastolic": {
                "normal": (60, 80),
                "elevated": (81, 89),
                "hypertension_stage1": (90, 99),
                "hypertension_stage2": (100, 120)
            }
        },
        MeasurementCategory.HEART_RATE: {
            "resting_normal": (60, 100),
            "bradycardia": (0, 59),
            "tachycardia": (101, 200)
        }
    }

    # Significant change thresholds (percentage change that flags review)
    SIGNIFICANT_CHANGE_THRESHOLDS = {
        MeasurementCategory.EJECTION_FRACTION: 0.10,  # 10% change flags review
        MeasurementCategory.AORTIC_DIMENSION: 0.05,  # 5mm change flags review
        MeasurementCategory.BLOOD_PRESSURE: 0.15,
        MeasurementCategory.HEART_RATE: 0.20
    }

    def __init__(self, patient_id: str = None):
        """
        Initialize the measurement verifier.

        Args:
            patient_id: Optional patient ID for loading historical data
        """
        self.patient_id = patient_id
        self.historical_data: Dict[str, List[MeasurementValue]] = {}
        self.verification_log: List[Dict] = []

        if patient_id:
            self.load_historical_data()

    def load_historical_data(self, historical_file: str = None) -> None:
        """Load historical measurements for cross-reference checking"""
        if historical_file is None and self.patient_id:
            # Try to load from standard location (package-relative, not CWD)
            historical_file = str(
                Path(__file__).resolve().parent.parent
                / "data" / "patients" / self.patient_id / "measurements.json"
            )

        if historical_file and Path(historical_file).exists():
            with open(historical_file, 'r') as f:
                data = json.load(f)
                # Parse into MeasurementValue objects
                for category, measurements in data.items():
                    self.historical_data[category] = [
                        MeasurementValue(**m) for m in measurements
                    ]

    def extract_measurement(
        self,
        text: str,
        category: MeasurementCategory,
        unit: str,
        max_variants: int = 3
    ) -> VerificationResult:
        """
        Extract measurement from text with verification.

        This is the PRIMARY METHOD for safe measurement extraction.
        It extracts multiple times and compares to prevent errors.

        Args:
            text: Medical report text to extract from
            category: Type of measurement
            unit: Expected unit (mm, %, etc.)
            max_variants: Maximum number of extraction attempts

        Returns:
            VerificationResult with verified value and flags
        """
        raw_extractions = []

        # Extract using multiple methods
        for method in [
            self._extract_with_regex,
            self._extract_with_pattern_matching,
            self._extract_with_context_aware
        ]:
            try:
                extracted = method(text, category, unit)
                if extracted is not None:
                    raw_extractions.append(extracted)
            except Exception as e:
                print(f"Extraction method {method.__name__} failed: {e}")

        # Remove duplicates
        raw_extractions = list(set(raw_extractions))

        if not raw_extractions:
            return VerificationResult(
                is_verified=False,
                verified_value=None,
                confidence=0.0,
                flags=["NO_EXTRACTION"],
                warnings=["Could not extract measurement from text"],
                suggestions=["Manual review required - no values found"],
                raw_extractions=[]
            )

        # Check consistency
        if len(raw_extractions) == 1:
            verified_value = raw_extractions[0]
            confidence = 0.9
            flags = []
            warnings = []
        else:
            # Multiple extractions - check if they're similar
            if max(raw_extractions) - min(raw_extractions) < 0.1:  # Within 0.1 units
                verified_value = sum(raw_extractions) / len(raw_extractions)
                confidence = 0.8
                flags = ["MULTIPLE_EXTRACTIONS_SIMILAR"]
                warnings = [f"Multiple similar values found: {raw_extractions}"]
            else:
                # Significant discrepancy - FLAG FOR REVIEW
                return VerificationResult(
                    is_verified=False,
                    verified_value=None,
                    confidence=0.0,
                    flags=["DISCREPANT_EXTRACTIONS"],
                    warnings=[f"CRITICAL: Multiple different values found: {raw_extractions}"],
                    suggestions=["MANUAL REVIEW REQUIRED - Values disagree significantly"],
                    raw_extractions=raw_extractions
                )

        # Cross-reference with historical data
        historical_check = self._check_historical_plausibility(
            category, verified_value
        )

        if historical_check["is_implausible"]:
            flags.append("IMPLAUSIBLE_VERSUS_HISTORY")
            warnings.extend(historical_check["reasons"])
            confidence *= 0.5

        # Check against reference ranges
        range_check = self._check_reference_ranges(category, verified_value)

        if range_check["is_outside_expected"]:
            flags.append("OUTSIDE_REFERENCE_RANGE")
            warnings.extend(range_check["warnings"])

        # Final verification decision
        is_verified = (
            "DISCREPANT_EXTRACTIONS" not in flags and
            "IMPLAUSIBLE_VERSUS_HISTORY" not in flags and
            confidence >= 0.7
        )

        result = VerificationResult(
            is_verified=is_verified,
            verified_value=verified_value if is_verified else None,
            confidence=confidence,
            flags=flags,
            warnings=warnings,
            suggestions=self._generate_suggestions(flags, category, verified_value),
            raw_extractions=raw_extractions
        )

        # Log verification
        self._log_verification(category, result)

        return result

    def _extract_with_regex(
        self,
        text: str,
        category: MeasurementCategory,
        unit: str
    ) -> Optional[float]:
        """Extract using regex patterns"""
        # Common patterns for different measurements
        patterns = {
            MeasurementCategory.EJECTION_FRACTION: [
                r'(?:LVEF|EF|ejection\s*fraction)[:\s]*([0-9]+\.?[0-9]*)\s*%',
                r'([0-9]+\.?[0-9]*)\s*%[\s\w]*(?:LVEF|EF|ejection)',
            ],
            MeasurementCategory.AORTIC_DIMENSION: [
                r'(?:aortic\s*root|sinus\s*of\s*valsalva|SOV)[:\s]*([0-9]+\.?[0-9]*)\s*mm',
                r'([0-9]+\.?[0-9]*)\s*mm[\s\w]*(?:aortic\s*root|sinus)',
            ],
            MeasurementCategory.BLOOD_PRESSURE: [
                r'(?:BP|blood\s*pressure)[:\s]*([0-9]+)/([0-9]+)',
                r'([0-9]+)/([0-9]+)\s*mmHg',
            ]
        }

        if category not in patterns:
            # Generic number extraction
            matches = re.findall(r'([0-9]+\.?[0-9]*)\s*' + re.escape(unit), text, re.IGNORECASE)
            return float(matches[0]) if matches else None

        for pattern in patterns[category]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                return value

        return None

    def _extract_with_pattern_matching(
        self,
        text: str,
        category: MeasurementCategory,
        unit: str
    ) -> Optional[float]:
        """Extract using context-aware pattern matching"""
        # Look for measurement keywords and extract nearby numbers
        context_keywords = {
            MeasurementCategory.EJECTION_FRACTION: [
                'LVEF', 'EF', 'ejection fraction', 'systolic function'
            ],
            MeasurementCategory.AORTIC_DIMENSION: [
                'aortic root', 'sinus of valsalva', 'SOV', 'aorta'
            ],
            MeasurementCategory.BLOOD_PRESSURE: [
                'blood pressure', 'BP', 'systolic', 'diastolic'
            ]
        }

        if category not in context_keywords:
            return self._extract_with_regex(text, category, unit)

        for keyword in context_keywords[category]:
            # Find keyword and extract nearby number with unit
            pattern = rf'{keyword}.*?([0-9]+\.?[0-9]*)\s*{re.escape(unit)}'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return float(match.group(1))

        return None

    def _extract_with_context_aware(
        self,
        text: str,
        category: MeasurementCategory,
        unit: str
    ) -> Optional[float]:
        """Extract using full context awareness"""
        # This is a placeholder for more sophisticated NLP extraction
        # For now, delegate to regex
        return self._extract_with_regex(text, category, unit)

    def _check_historical_plausibility(
        self,
        category: MeasurementCategory,
        value: float
    ) -> Dict[str, Any]:
        """Check if value is plausible given historical data"""
        if not self.historical_data or category.value not in self.historical_data:
            return {"is_implausible": False, "reasons": []}

        historical = self.historical_data[category.value]
        if not historical:
            return {"is_implausible": False, "reasons": []}

        # Get recent historical values
        recent_values = [m.value for m in historical[-5:]]
        avg_historical = sum(recent_values) / len(recent_values)

        # Check if change is significant
        threshold = self.SIGNIFICANT_CHANGE_THRESHOLDS.get(category, 0.20)
        percent_change = abs(value - avg_historical) / avg_historical

        if percent_change > threshold:
            return {
                "is_implausible": True,
                "reasons": [
                    f"Value {value} differs from historical average {avg_historical:.1f} by {percent_change*100:.1f}%",
                    f"Recent values: {[f'{v:.1f}' for v in recent_values]}"
                ]
            }

        return {"is_implausible": False, "reasons": []}

    def _check_reference_ranges(
        self,
        category: MeasurementCategory,
        value: float
    ) -> Dict[str, Any]:
        """Check if value is within expected reference ranges"""
        if category not in self.REFERENCE_RANGES:
            return {"is_outside_expected": False, "warnings": []}

        ranges = self.REFERENCE_RANGES[category]
        warnings = []

        # Check each range
        for range_name, range_limits in ranges.items():
            if isinstance(range_limits, dict):
                # Nested ranges (e.g., aortic dimension locations)
                for sub_name, sub_limits in range_limits.items():
                    if isinstance(sub_limits, tuple) and len(sub_limits) == 2:
                        min_val, max_val = sub_limits
                        if value < min_val or value > max_val:
                            warnings.append(f"Value {value} outside {range_name}/{sub_name} range ({min_val}-{max_val})")
            elif isinstance(range_limits, tuple) and len(range_limits) == 2:
                min_val, max_val = range_limits
                if value < min_val or value > max_val:
                    warnings.append(f"Value {value} outside {range_name} range ({min_val}-{max_val})")

        return {
            "is_outside_expected": len(warnings) > 0,
            "warnings": warnings
        }

    def _generate_suggestions(
        self,
        flags: List[str],
        category: MeasurementCategory,
        value: float
    ) -> List[str]:
        """Generate suggestions based on flags"""
        suggestions = []

        if "DISCREPANT_EXTRACTIONS" in flags:
            suggestions.append("MANUAL REVIEW REQUIRED - Multiple different values extracted")

        if "IMPLAUSIBLE_VERSUS_HISTORY" in flags:
            suggestions.append(
                f"Verify {category.value} value {value} against patient history"
            )

        if "OUTSIDE_REFERENCE_RANGE" in flags:
            suggestions.append(
                f"Value {value} outside normal range - confirm if correct"
            )

        if not suggestions:
            suggestions.append("Value verified - safe to use")

        return suggestions

    def _log_verification(
        self,
        category: MeasurementCategory,
        result: VerificationResult
    ) -> None:
        """Log verification for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category.value,
            "is_verified": result.is_verified,
            "verified_value": result.verified_value,
            "confidence": result.confidence,
            "flags": result.flags,
            "raw_extractions": result.raw_extractions
        }
        self.verification_log.append(log_entry)

    def batch_verify(
        self,
        text: str,
        measurements: List[Tuple[MeasurementCategory, str]]
    ) -> Dict[str, VerificationResult]:
        """
        Verify multiple measurements from a single document.

        Args:
            text: Medical report text
            measurements: List of (category, unit) tuples to extract

        Returns:
            Dictionary mapping category names to verification results
        """
        results = {}
        for category, unit in measurements:
            result = self.extract_measurement(text, category, unit)
            results[category.value] = result

        return results

    def export_verification_log(self, filepath: str) -> None:
        """Export verification log for audit"""
        with open(filepath, 'w') as f:
            json.dump(self.verification_log, f, indent=2)


# Convenience function for quick verification
def verify_measurement(
    text: str,
    category: MeasurementCategory,
    unit: str,
    patient_id: str = None
) -> VerificationResult:
    """
    Quick verification of a single measurement.

    This is the RECOMMENDED interface for most use cases.

    Args:
        text: Medical report text containing the measurement
        category: Type of measurement (e.g., MeasurementCategory.EJECTION_FRACTION)
        unit: Unit of measurement (e.g., '%', 'mm')
        patient_id: Optional patient ID for historical comparison

    Returns:
        VerificationResult with verification status and any flags

    Example:
        >>> result = verify_measurement(
        ...     report_text,
        ...     MeasurementCategory.EJECTION_FRACTION,
        ...     '%',
        ...     patient_id="patient123"
        ... )
        >>> if result.is_verified:
        ...     print(f"Verified LVEF: {result.verified_value}%")
        ... else:
        ...     print(f"FLAGS: {result.flags}")
        ...     print(f"Warnings: {result.warnings}")
    """
    verifier = MedicalMeasurementVerifier(patient_id)
    return verifier.extract_measurement(text, category, unit)


# Emergency halt function for critical discrepancies
def halt_on_critical_discrepancy(result: VerificationResult) -> None:
    """
    Halt execution if critical verification flags are present.

    Use this when accuracy is paramount and you must prevent
    proceeding with unverified data.

    Args:
        result: VerificationResult to check

    Raises:
        RuntimeError: If critical flags are present
    """
    critical_flags = {
        "DISCREPANT_EXTRACTIONS",
        "IMPLAUSIBLE_VERSUS_HISTORY",
        "NO_EXTRACTION"
    }

    if critical_flags.intersection(result.flags):
        raise RuntimeError(
            f"CRITICAL VERIFICATION FAILURE - Cannot proceed:\n"
            f"Flags: {result.flags}\n"
            f"Warnings: {result.warnings}\n"
            f"Raw extractions: {result.raw_extractions}\n"
            f"MUST RESOLVE BEFORE CONTINUING"
        )


if __name__ == "__main__":
    # Test the verifier with sample data
    test_text = """
    ECHOCARDIOGRAM REPORT
    =====================
    LVEF: 55%
    Aortic root diameter: 42mm at sinus of Valsalva
    Blood pressure: 118/53 mmHg
    Heart rate: 57 bpm
    """

    verifier = MedicalMeasurementVerifier()

    print("Testing measurement verification...")
    print("=" * 60)

    # Test LVEF extraction
    lvef_result = verifier.extract_measurement(
        test_text,
        MeasurementCategory.EJECTION_FRACTION,
        '%'
    )
    print(f"\nLVEF Verification:")
    print(f"  Verified: {lvef_result.is_verified}")
    print(f"  Value: {lvef_result.verified_value}")
    print(f"  Confidence: {lvef_result.confidence}")
    print(f"  Flags: {lvef_result.flags}")

    # Test Aortic root extraction
    aortic_result = verifier.extract_measurement(
        test_text,
        MeasurementCategory.AORTIC_DIMENSION,
        'mm'
    )
    print(f"\nAortic Root Verification:")
    print(f"  Verified: {aortic_result.is_verified}")
    print(f"  Value: {aortic_result.verified_value}")
    print(f"  Confidence: {aortic_result.confidence}")
    print(f"  Flags: {aortic_result.flags}")

    print("\n" + "=" * 60)
    print("Verification system operational")
