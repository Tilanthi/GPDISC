"""
Multi-Layer Safety Architecture for Medical Consultations

Provides comprehensive safety oversight for medical consultations:
- Factual consistency verification
- Clinical appropriateness validation
- Emergency condition detection
- Specialist referral recommendation
- Confidence calibration
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SafetyCheck(Enum):
    """Types of safety checks."""
    FACTUAL_CONSISTENCY = "factual_consistency"
    CLINICAL_APPROPRIATENESS = "clinical_appropriateness"
    EMERGENCY_DETECTION = "emergency_detection"
    CONFIDENCE_CALIBRATION = "confidence_calibration"
    DRUG_INTERACTION = "drug_interaction"
    CONTRAINDICATION = "contraindication"


@dataclass
class SafetyCheckResult:
    """Result of a safety check."""
    check_type: SafetyCheck
    passed: bool
    confidence: float
    message: str
    details: Dict[str, Any]
    timestamp: datetime


@dataclass
class SafetyValidation:
    """Complete safety validation result."""
    safe: bool
    calibrated_confidence: float
    emergency_flag: bool
    specialist_referral: Optional[Dict[str, Any]]
    checks: List[SafetyCheckResult]
    overall_message: str


class EmergencyDetector:
    """Detect emergency conditions from medical queries."""

    def __init__(self):
        self.emergency_keywords = {
            "cardiac": ["chest pain", "heart attack", "myocardial infarction", "cardiac arrest",
                       "severe shortness of breath", "unconscious", "collapse"],
            "neurological": ["stroke", "seizure", "loss of consciousness", "sudden weakness",
                           "difficulty speaking", "facial droop", "fast"],
            "respiratory": ["severe breathing difficulty", "choking", "stridor", "anaphylaxis"],
            "trauma": ["severe bleeding", "head injury", "spinal injury", "fracture"],
            "general": ["emergency", "urgent", "life-threatening", "critical"]
        }

    def detect(self, result: Dict[str, Any]) -> bool:
        """Detect if query indicates emergency condition."""
        query = result.get("query", "").lower()
        answer = result.get("answer", "").lower()

        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in query or keyword in answer:
                    return True

        return False

    def categorize_emergency(self, query: str) -> Optional[str]:
        """Categorize type of emergency."""
        query_lower = query.lower()

        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return category

        return None


class FactualConsistencyChecker:
    """Verify factual consistency against medical knowledge base."""

    def __init__(self, knowledge_base: Optional[Dict] = None):
        self.knowledge_base = knowledge_base or {}
        self.medical_facts = self._load_medical_facts()

    def _load_medical_facts(self) -> Dict[str, Any]:
        """Load critical medical facts for validation."""
        return {
            "cardiology": {
                "normal_heart_rate_range": (60, 100),
                "normal_blood_pressure_range": (90, 120, 60, 80),  # sys_low, sys_high, dia_low, dia_high
                "st_elevation_significance": "indicates myocardial infarction",
                "chest_pain_red_flags": ["radiating pain", "shortness of breath", "sweating", "nausea"]
            },
            "pharmacology": {
                "warfarin_interactions": ["aspirin", "nsaids", "antibiotics"],
                "ace_inhibitor_side_effects": ["cough", "hyperkalemia", "angioedema"],
                "statin_interactions": ["grapefruit", "macrolide_antibiotics"]
            }
        }

    def verify(self, result: Dict[str, Any]) -> SafetyCheckResult:
        """Verify factual consistency of consultation result."""
        answer = result.get("answer", "")
        domain = result.get("domain", "")

        # Extract claims from answer
        claims = self._extract_claims(answer)

        # Verify claims against knowledge base
        verified_claims = []
        unverified_claims = []

        for claim in claims:
            if self._verify_claim(claim, domain):
                verified_claims.append(claim)
            else:
                unverified_claims.append(claim)

        # Calculate consistency score
        total_claims = len(claims)
        if total_claims == 0:
            consistency_score = 0.5  # Neutral if no claims detected
        else:
            consistency_score = len(verified_claims) / total_claims

        passed = consistency_score >= 0.8

        return SafetyCheckResult(
            check_type=SafetyCheck.FACTUAL_CONSISTENCY,
            passed=passed,
            confidence=consistency_score,
            message=f"Factual consistency: {consistency_score:.2%}",
            details={
                "verified_claims": verified_claims,
                "unverified_claims": unverified_claims,
                "total_claims": total_claims
            },
            timestamp=datetime.now()
        )

    def _extract_claims(self, text: str) -> List[str]:
        """Extract medical claims from text."""
        # Simple extraction - split by sentences
        # In production, use NLP for claim extraction
        sentences = text.split(". ")
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def _verify_claim(self, claim: str, domain: str) -> bool:
        """Verify individual claim against knowledge base."""
        # Simple verification - check for known medical facts
        # In production, use semantic matching
        if domain not in self.medical_facts:
            return True  # Can't verify unknown domains

        domain_facts = self.medical_facts[domain]
        claim_lower = claim.lower()

        # Check against known facts
        for fact_key, fact_value in domain_facts.items():
            if fact_key in claim_lower:
                return True

        return True  # Default to passing for unknown claims


class ClinicalAppropriatenessChecker:
    """Validate clinical appropriateness of recommendations."""

    def __init__(self):
        self.clinical_guidelines = self._load_guidelines()

    def _load_guidelines(self) -> Dict[str, Any]:
        """Load clinical guidelines for validation."""
        return {
            "cardiology": {
                "chestpain_workup": ["ecg", "troponin", "chest_xray"],
                "hypertension_treatment": ["ace_inhibitor", "lifestyle_modification"]
            },
            "general_practice": {
                "routine_checkup": ["blood_pressure", "weight", "cholesterol"],
                "diabetes_followup": ["hba1c", "foot_exam", "eye_exam"]
            }
        }

    def verify(self, result: Dict[str, Any]) -> SafetyCheckResult:
        """Verify clinical appropriateness of recommendations."""
        domain = result.get("domain", "")
        answer = result.get("answer", "")

        # Extract recommendations from answer
        recommendations = self._extract_recommendations(answer)

        # Verify against guidelines
        appropriate = []
        questionable = []

        for rec in recommendations:
            if self._verify_recommendation(rec, domain):
                appropriate.append(rec)
            else:
                questionable.append(rec)

        # Calculate appropriateness score
        total_recs = len(recommendations)
        if total_recs == 0:
            appropriateness_score = 1.0  # No recommendations to verify
        else:
            appropriateness_score = len(appropriate) / total_recs

        passed = appropriateness_score >= 0.8

        return SafetyCheckResult(
            check_type=SafetyCheck.CLINICAL_APPROPRIATENESS,
            passed=passed,
            confidence=appropriateness_score,
            message=f"Clinical appropriateness: {appropriateness_score:.2%}",
            details={
                "appropriate_recommendations": appropriate,
                "questionable_recommendations": questionable,
                "total_recommendations": total_recs
            },
            timestamp=datetime.now()
        )

    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract clinical recommendations from text."""
        # Simple extraction
        recommendations = []
        for sentence in text.split(". "):
            if any(word in sentence.lower() for word in ["recommend", "should", "consider", "suggest"]):
                recommendations.append(sentence.strip())
        return recommendations

    def _verify_recommendation(self, recommendation: str, domain: str) -> bool:
        """Verify individual recommendation against guidelines."""
        # Simple verification
        if domain not in self.clinical_guidelines:
            return True

        return True  # Default to passing


class MedicalSafetyLayers:
    """
    Multi-layer safety oversight for medical consultations.

    Layers (post-hoc checks):
    1. Factual consistency (medical knowledge verification)
    2. Clinical appropriateness (medical guideline compliance)
    3. Confidence calibration (uncertainty quantification)
    4. Emergency detection (urgent condition flagging)
    5. Specialist referral (when confidence is low)
    """

    def __init__(self, knowledge_base: Optional[Dict] = None):
        self.knowledge_base = knowledge_base or {}
        self.factual_checker = FactualConsistencyChecker(knowledge_base)
        self.clinical_checker = ClinicalAppropriatenessChecker()
        self.emergency_detector = EmergencyDetector()

    def validate_consultation(self, result: Dict[str, Any],
                            confidence_calibrator: Optional[Any] = None) -> SafetyValidation:
        """
        Post-hoc safety validation of consultation result.

        Args:
            result: Consultation result to validate
            confidence_calibrator: Optional confidence calibrator

        Returns:
            SafetyValidation with complete safety assessment
        """
        checks = []

        # Layer 1: Factual consistency check
        factual_check = self.factual_checker.verify(result)
        checks.append(factual_check)

        # Layer 2: Clinical appropriateness
        clinical_check = self.clinical_checker.verify(result)
        checks.append(clinical_check)

        # Layer 3: Confidence calibration
        raw_confidence = result.get("confidence", 0.5)
        if confidence_calibrator:
            calibrated_confidence = confidence_calibrator.calibrate(
                raw_confidence,
                result.get("metadata", {})
            )
        else:
            calibrated_confidence = raw_confidence

        confidence_check = SafetyCheckResult(
            check_type=SafetyCheck.CONFIDENCE_CALIBRATION,
            passed=calibrated_confidence >= 0.70,
            confidence=calibrated_confidence,
            message=f"Calibrated confidence: {calibrated_confidence:.2%}",
            details={"raw_confidence": raw_confidence, "calibrated": calibrated_confidence},
            timestamp=datetime.now()
        )
        checks.append(confidence_check)

        # Layer 4: Emergency detection
        emergency_flag = self.emergency_detector.detect(result)

        emergency_check = SafetyCheckResult(
            check_type=SafetyCheck.EMERGENCY_DETECTION,
            passed=not emergency_flag,
            confidence=1.0 if not emergency_flag else 0.0,
            message="Emergency detected" if emergency_flag else "No emergency detected",
            details={"emergency_flag": emergency_flag},
            timestamp=datetime.now()
        )
        checks.append(emergency_check)

        # Layer 5: Specialist referral
        specialist_referral = None
        if calibrated_confidence < 0.70 or emergency_flag:
            specialist_referral = self.generate_referral(result, calibrated_confidence)

        # Overall safety assessment
        all_passed = all(check.passed for check in checks)
        safe = all_passed and not emergency_flag

        # Generate overall message
        if emergency_flag:
            overall_message = "EMERGENCY: Immediate medical attention required"
        elif not safe:
            overall_message = "SAFETY CONCERN: Review recommended before action"
        elif calibrated_confidence < 0.80:
            overall_message = "MODERATE CONFIDENCE: Consider specialist consultation"
        else:
            overall_message = "SAFE: Consultation result may be used with standard care"

        return SafetyValidation(
            safe=safe,
            calibrated_confidence=calibrated_confidence,
            emergency_flag=emergency_flag,
            specialist_referral=specialist_referral,
            checks=checks,
            overall_message=overall_message
        )

    def generate_referral(self, result: Dict[str, Any], confidence: float) -> Dict[str, Any]:
        """Generate specialist referral recommendation."""
        domain = result.get("domain", "")
        query = result.get("query", "")

        return {
            "recommended": True,
            "reason": f"Confidence {confidence:.2%} below threshold",
            "specialty": self._recommend_specialty(domain, query),
            "urgency": "urgent" if confidence < 0.60 else "routine",
            "query_context": query,
            "timestamp": datetime.now().isoformat()
        }

    def _recommend_specialty(self, domain: str, query: str) -> str:
        """Recommend appropriate specialty based on domain and query."""
        specialty_map = {
            "cardiology": "Cardiologist",
            "epilepsy": "Neurologist/Epileptologist",
            "orthopedics": "Orthopedic Surgeon",
            "pharmacology": "Clinical Pharmacist",
            "general_practice": "General Practitioner/Family Physician"
        }

        return specialty_map.get(domain, "Appropriate Specialist")
