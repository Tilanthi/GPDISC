"""
Confidence Calibration for Medical Decisions

Calibrates confidence scores for medical consultations based on:
- Domain-specific difficulty
- Information completeness
- Clinical uncertainty
- Evidence quality
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UncertaintyQuantification:
    """Quantified uncertainty for medical decisions."""
    level: str  # "low", "moderate", "high"
    description: str
    recommended_action: str
    confidence_range: tuple[float, float]


class ConfidenceCalibrator:
    """
    Calibrate confidence scores for medical decisions.

    Principles:
    - Confidence should reflect true probability of correctness
    - Uncertainty should be quantified and communicated
    - Low confidence should trigger specialist referral
    """

    def __init__(self, calibration_data: Optional[Dict] = None):
        self.calibration_data = calibration_data or {}
        self.domain_difficulty = {
            "cardiology": 0.82,
            "epilepsy": 0.78,
            "general_practice": 0.88,
            "orthopedics": 0.85,
            "pharmacology": 0.95,
            "molecular_biology": 0.90,
            "biochemistry": 0.90,
            "genetics": 0.87,
            "cell_biology": 0.89,
            "biophysics": 0.86,
            "bioinformatics": 0.88,
            "computational_biology": 0.87,
            "genomics": 0.86,
            "proteomics": 0.85,
            "systems_biology": 0.84
        }

    def calibrate(self, raw_confidence: float, metadata: Dict[str, Any]) -> float:
        """
        Calibrate raw confidence score.

        Args:
            raw_confidence: Raw confidence from domain module
            metadata: Metadata including domain, completeness, etc.

        Returns:
            Calibrated confidence score
        """
        domain = metadata.get("domain", "general_practice")
        difficulty_modifier = self.domain_difficulty.get(domain, 0.85)

        # Apply domain-specific difficulty
        calibrated = raw_confidence * difficulty_modifier

        # Account for information completeness
        completeness = metadata.get("information_completeness", 1.0)
        calibrated *= completeness

        # Account for evidence quality
        evidence_quality = metadata.get("evidence_quality", 1.0)
        calibrated *= evidence_quality

        # Account for data freshness
        data_freshness = metadata.get("data_freshness", 1.0)
        calibrated *= data_freshness

        # Clamp to valid range
        return max(0.0, min(1.0, calibrated))

    def quantify_uncertainty(self, confidence: float) -> UncertaintyQuantification:
        """
        Quantify uncertainty for communication.

        Args:
            confidence: Calibrated confidence score

        Returns:
            UncertaintyQuantification object
        """
        if confidence >= 0.90:
            return UncertaintyQuantification(
                level="low",
                description="High confidence in this assessment",
                recommended_action="proceed with standard care",
                confidence_range=(0.90, 1.0)
            )
        elif confidence >= 0.70:
            return UncertaintyQuantification(
                level="moderate",
                description="Moderate confidence - additional verification recommended",
                recommended_action="consider specialist consultation if clinically indicated",
                confidence_range=(0.70, 0.89)
            )
        else:
            return UncertaintyQuantification(
                level="high",
                description="Significant uncertainty - specialist consultation required",
                recommended_action="refer to appropriate specialist for definitive assessment",
                confidence_range=(0.0, 0.69)
            )

    def validate_confidence_threshold(self, confidence: float, domain: str) -> bool:
        """
        Validate if confidence meets domain-specific threshold.

        Args:
            confidence: Calibrated confidence score
            domain: Medical domain

        Returns:
            True if confidence meets threshold
        """
        thresholds = {
            "cardiology": 0.75,
            "epilepsy": 0.75,
            "general_practice": 0.70,
            "orthopedics": 0.75,
            "pharmacology": 0.85
        }

        threshold = thresholds.get(domain, 0.75)
        return confidence >= threshold

    def calculate_confidence_interval(self, confidence: float, sample_size: int = 1) -> tuple[float, float]:
        """
        Calculate confidence interval using Wilson score interval.

        Args:
            confidence: Point estimate
            sample_size: Sample size for interval calculation

        Returns:
            Lower and upper bounds of confidence interval
        """
        import math

        if sample_size < 2:
            # Conservative interval for small samples
            margin = 0.1
        else:
            # Wilson score interval
            z = 1.96  # 95% confidence
            denominator = 1 + (z ** 2) / sample_size
            center = (confidence + (z ** 2) / (2 * sample_size)) / denominator
            margin = z * math.sqrt((confidence * (1 - confidence) / sample_size) +
                                  (z ** 2) / (4 * (sample_size ** 2))) / denominator

        lower = max(0.0, confidence - margin)
        upper = min(1.0, confidence + margin)

        return (lower, upper)
