"""
Medical Tools Interface and Implementations

Standardized tool interface for medical consultation capabilities.
Provides consistent tool execution with validation and confidence scoring.
"""

from typing import Protocol, TypedDict, Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
import json


@dataclass
class ToolResult:
    """Standardized result from medical tool execution."""
    success: bool
    data: Dict[str, Any]
    confidence: float
    metadata: Dict[str, Any]
    timestamp: datetime = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class MedicalTool(ABC):
    """
    Standardized medical tool interface.

    All medical tools must implement this interface for consistency.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__doc__ or "Medical tool"
        self.version = "1.0.0"

    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool parameters."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute tool with given parameters."""
        pass

    def validate_parameters(self, parameters: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate tool parameters before execution.

        Returns:
            Tuple of (is_valid, error_message)
        """
        schema = self.get_parameters_schema()
        required = schema.get("required", [])

        # Check required parameters
        for param in required:
            if param not in parameters:
                return False, f"Missing required parameter: {param}"

        return True, None

    def format_result(self, data: Dict[str, Any], confidence: float,
                     metadata: Optional[Dict] = None) -> ToolResult:
        """Format execution result as ToolResult."""
        return ToolResult(
            success=True,
            data=data,
            confidence=confidence,
            metadata=metadata or {},
            timestamp=datetime.now()
        )

    def format_error(self, error_message: str) -> ToolResult:
        """Format error as ToolResult."""
        return ToolResult(
            success=False,
            data={},
            confidence=0.0,
            metadata={},
            timestamp=datetime.now(),
            error_message=error_message
        )


class ECGInterpreterTool(MedicalTool):
    """
    ECG/EKG interpretation tool.

    Analyzes ECG data and provides clinical assessment with:
    - Rhythm interpretation
    - Conduction analysis
    - Ischemia/infarction detection
    - Clinical significance assessment
    """

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "ecg_data": {
                    "type": "object",
                    "description": "ECG data including rhythm, rate, intervals, waves"
                },
                "patient_context": {
                    "type": "object",
                    "description": "Patient clinical context (age, symptoms, history)"
                }
            },
            "required": ["ecg_data"]
        }

    def execute(self, ecg_data: Dict[str, Any],
                patient_context: Optional[Dict] = None) -> ToolResult:
        """
        Execute ECG interpretation.

        Args:
            ecg_data: ECG data including rhythm, rate, intervals, waves
            patient_context: Optional patient clinical context

        Returns:
            ToolResult with interpretation
        """
        try:
            # Validate parameters
            is_valid, error = self.validate_parameters({"ecg_data": ecg_data})
            if not is_valid:
                return self.format_error(error)

            # Interpret ECG
            interpretation = self._interpret_ecg(ecg_data, patient_context)

            # Calculate confidence based on data quality
            confidence = self._calculate_confidence(ecg_data, interpretation)

            return self.format_result(
                data={"interpretation": interpretation},
                confidence=confidence,
                metadata={
                    "tool": "ecg_interpreter",
                    "data_quality": self._assess_data_quality(ecg_data),
                    "rhythm": interpretation.get("rhythm"),
                    "clinical_significance": interpretation.get("clinical_significance")
                }
            )

        except Exception as e:
            return self.format_error(f"ECG interpretation failed: {str(e)}")

    def _interpret_ecg(self, ecg_data: Dict, patient_context: Optional[Dict]) -> Dict[str, Any]:
        """Perform detailed ECG interpretation."""
        interpretation = {
            "rhythm": self._interpret_rhythm(ecg_data),
            "rate": self._interpret_rate(ecg_data),
            "intervals": self._interpret_intervals(ecg_data),
            "waves": self._interpret_waves(ecg_data),
            "abnormalities": self._detect_abnormalities(ecg_data),
            "clinical_significance": self._assess_clinical_significance(ecg_data, patient_context)
        }

        return interpretation

    def _interpret_rhythm(self, ecg_data: Dict) -> str:
        """Interpret cardiac rhythm."""
        rhythm = ecg_data.get("rhythm", "").lower()

        if "sinus" in rhythm:
            return "Sinus Rhythm"
        elif "atrial fibrillation" in rhythm or "af" in rhythm:
            return "Atrial Fibrillation"
        elif "atrial flutter" in rhythm:
            return "Atrial Flutter"
        elif "tachycardia" in rhythm:
            return f"Supraventricular Tachycardia" if "sv" in rhythm else "Ventricular Tachycardia"
        else:
            return rhythm.title()

    def _interpret_rate(self, ecg_data: Dict) -> Dict[str, Any]:
        """Interpret heart rate."""
        rate = ecg_data.get("heart_rate", 0)

        if rate == 0:
            return {"rate": rate, "interpretation": "Rate not specified"}

        if rate < 60:
            interpretation = "Bradycardia"
        elif rate > 100:
            interpretation = "Tachycardia"
        else:
            interpretation = "Normal"

        return {"rate": rate, "interpretation": interpretation}

    def _interpret_intervals(self, ecg_data: Dict) -> Dict[str, Any]:
        """Interpret PR, QRS, QT intervals."""
        intervals = ecg_data.get("intervals", {})

        return {
            "pr": {
                "duration_ms": intervals.get("pr", 0),
                "interpretation": self._interpret_pr_interval(intervals.get("pr", 0))
            },
            "qrs": {
                "duration_ms": intervals.get("qrs", 0),
                "interpretation": self._interpret_qrs_interval(intervals.get("qrs", 0))
            },
            "qt": {
                "duration_ms": intervals.get("qt", 0),
                "corrected": intervals.get("qtc", 0),
                "interpretation": self._interpret_qt_interval(intervals.get("qtc", intervals.get("qt", 0)))
            }
        }

    def _interpret_pr_interval(self, pr_ms: int) -> str:
        """Interpret PR interval."""
        if pr_ms == 0:
            return "Not specified"
        elif pr_ms < 120:
            return "Short (possible pre-excitation)"
        elif pr_ms > 200:
            return "Prolonged (AV block)"
        else:
            return "Normal"

    def _interpret_qrs_interval(self, qrs_ms: int) -> str:
        """Interpret QRS interval."""
        if qrs_ms == 0:
            return "Not specified"
        elif qrs_ms < 80:
            return "Narrow"
        elif qrs_ms > 120:
            return "Wide (intraventricular conduction delay)"
        else:
            return "Normal"

    def _interpret_qt_interval(self, qt_ms: int) -> str:
        """Interpret QT interval."""
        if qt_ms == 0:
            return "Not specified"
        elif qt_ms > 450:
            return "Prolonged (risk of arrhythmia)"
        else:
            return "Normal"

    def _interpret_waves(self, ecg_data: Dict) -> Dict[str, Any]:
        """Interpret P waves, QRS complexes, T waves."""
        waves = ecg_data.get("waves", {})

        return {
            "p_waves": {
                "morphology": waves.get("p_wave", "Normal"),
                "interpretation": "Normal sinus P waves" if "normal" in waves.get("p_wave", "").lower() else "Abnormal"
            },
            "qrs_complexes": {
                "morphology": waves.get("qrs", "Normal"),
                "interpretation": "Normal QRS morphology" if "normal" in waves.get("qrs", "").lower() else "Abnormal"
            },
            "t_waves": {
                "morphology": waves.get("t_wave", "Normal"),
                "interpretation": "Normal T waves" if "normal" in waves.get("t_wave", "").lower() else "Abnormal"
            }
        }

    def _detect_abnormalities(self, ecg_data: Dict) -> List[str]:
        """Detect ECG abnormalities."""
        abnormalities = []

        # Check for ST elevation
        if "st_elevation" in ecg_data.get("findings", "").lower():
            abnormalities.append("ST elevation (suggests myocardial infarction)")

        # Check for ST depression
        if "st_depression" in ecg_data.get("findings", "").lower() or "st depression" in ecg_data.get("findings", "").lower():
            abnormalities.append("ST depression (suggests ischemia)")

        # Check for T wave inversion
        if "t_wave_inversion" in ecg_data.get("findings", "").lower() or "t wave inversion" in ecg_data.get("findings", "").lower():
            abnormalities.append("T wave inversion (suggests ischemia)")

        # Check for Q waves
        if "pathological_q" in ecg_data.get("findings", "").lower():
            abnormalities.append("Pathological Q waves (suggests prior infarction)")

        return abnormalities

    def _assess_clinical_significance(self, ecg_data: Dict, patient_context: Optional[Dict]) -> str:
        """Assess clinical significance of findings."""
        abnormalities = self._detect_abnormalities(ecg_data)

        if not abnormalities:
            return "Normal ECG - no acute abnormalities"

        # Check for emergency findings
        emergency_findings = ["st elevation", "myocardial infarction", "ventricular tachycardia"]
        for abnormality in abnormalities:
            if any(finding in abnormality.lower() for finding in emergency_findings):
                return "EMERGENCY: Requires immediate medical evaluation"

        return "Abnormal findings present - clinical correlation required"

    def _assess_data_quality(self, ecg_data: Dict) -> str:
        """Assess quality of ECG data provided."""
        required_fields = ["rhythm", "heart_rate", "intervals", "waves"]
        present_fields = sum(1 for field in required_fields if field in ecg_data)

        if present_fields == len(required_fields):
            return "Complete"
        elif present_fields >= len(required_fields) / 2:
            return "Partial"
        else:
            return "Limited"

    def _calculate_confidence(self, ecg_data: Dict, interpretation: Dict) -> float:
        """Calculate confidence score based on data quality and findings."""
        base_confidence = 0.8

        # Adjust for data quality
        quality = self._assess_data_quality(ecg_data)
        if quality == "Complete":
            quality_modifier = 1.0
        elif quality == "Partial":
            quality_modifier = 0.8
        else:
            quality_modifier = 0.6

        # Adjust for clinical significance (emergency findings increase certainty)
        significance = interpretation.get("clinical_significance", "")
        if "emergency" in significance.lower():
            significance_modifier = 1.1
        elif "abnormal" in significance.lower():
            significance_modifier = 1.0
        else:
            significance_modifier = 0.95

        confidence = base_confidence * quality_modifier * significance_modifier

        return min(1.0, max(0.0, confidence))


class DrugInteractionCheckerTool(MedicalTool):
    """
    Drug interaction checking tool.

    Checks for drug-drug interactions with:
    - Interaction severity grading
    - Clinical recommendations
    - Evidence levels
    """

    def __init__(self):
        super().__init__()
        # Common drug interactions database
        self.interaction_database = self._load_interaction_database()

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "medications": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of medication names"
                },
                "patient_context": {
                    "type": "object",
                    "description": "Patient clinical context (age, renal function, etc.)"
                }
            },
            "required": ["medications"]
        }

    def execute(self, medications: List[str],
                patient_context: Optional[Dict] = None) -> ToolResult:
        """
        Execute drug interaction check.

        Args:
            medications: List of medication names
            patient_context: Optional patient clinical context

        Returns:
            ToolResult with interaction analysis
        """
        try:
            # Validate parameters
            is_valid, error = self.validate_parameters({"medications": medications})
            if not is_valid:
                return self.format_error(error)

            if len(medications) < 2:
                return self.format_result(
                    data={"interactions": [], "message": "At least 2 medications required for interaction check"},
                    confidence=1.0,
                    metadata={"tool": "drug_interaction_checker"}
                )

            # Check for interactions
            interactions = self._check_interactions(medications, patient_context)

            return self.format_result(
                data={
                    "interactions": interactions,
                    "total_medications": len(medications),
                    "interactions_found": len(interactions)
                },
                confidence=0.95,  # High confidence for interaction checks
                metadata={
                    "tool": "drug_interaction_checker",
                    "medications_checked": medications
                }
            )

        except Exception as e:
            return self.format_error(f"Drug interaction check failed: {str(e)}")

    def _load_interaction_database(self) -> Dict[str, Any]:
        """Load drug interaction database."""
        return {
            "warfarin": {
                "aspirin": {
                    "severity": "moderate",
                    "effect": "increased bleeding risk",
                    "recommendation": "Monitor INR closely, consider dose adjustment",
                    "evidence_level": "A"
                },
                "nsaids": {
                    "severity": "moderate",
                    "effect": "increased bleeding risk",
                    "recommendation": "Avoid concurrent use if possible",
                    "evidence_level": "B"
                },
                "antibiotics": {
                    "severity": "major",
                    "effect": "increased INR, bleeding risk",
                    "recommendation": "Close INR monitoring, dose adjustment",
                    "evidence_level": "A"
                }
            },
            "ace_inhibitors": {
                "potassium_supplements": {
                    "severity": "major",
                    "effect": "hyperkalemia",
                    "recommendation": "Monitor potassium, avoid combination",
                    "evidence_level": "A"
                },
                "nsaids": {
                    "severity": "moderate",
                    "effect": "reduced antihypertensive effect",
                    "recommendation": "Monitor blood pressure",
                    "evidence_level": "B"
                }
            },
            "statins": {
                "grapefruit": {
                    "severity": "moderate",
                    "effect": "increased statin levels",
                    "recommendation": "Avoid large quantities of grapefruit",
                    "evidence_level": "C"
                },
                "macrolide_antibiotics": {
                    "severity": "major",
                    "effect": "increased risk of myopathy",
                    "recommendation": "Consider temporary statin discontinuation",
                    "evidence_level": "B"
                }
            }
        }

    def _check_interactions(self, medications: List[str],
                           patient_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Check for interactions between medications."""
        interactions = []
        medications_lower = [m.lower() for m in medications]

        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                interaction = self._check_pair_interaction(med1, med2)
                if interaction:
                    interactions.append(interaction)

        return interactions

    def _check_pair_interaction(self, med1: str, med2: str) -> Optional[Dict[str, Any]]:
        """Check for interaction between two medications."""
        med1_lower = med1.lower()
        med2_lower = med2.lower()

        # Check both directions in database
        if med1_lower in self.interaction_database:
            if med2_lower in self.interaction_database[med1_lower]:
                return self._format_interaction(med1, med2,
                    self.interaction_database[med1_lower][med2_lower])

        if med2_lower in self.interaction_database:
            if med1_lower in self.interaction_database[med2_lower]:
                return self._format_interaction(med2, med1,
                    self.interaction_database[med2_lower][med1_lower])

        return None

    def _format_interaction(self, med1: str, med2: str, interaction_data: Dict) -> Dict[str, Any]:
        """Format interaction result."""
        return {
            "medication_1": med1,
            "medication_2": med2,
            "severity": interaction_data["severity"],
            "effect": interaction_data["effect"],
            "recommendation": interaction_data["recommendation"],
            "evidence_level": interaction_data["evidence_level"]
        }


class DiagnosticReasoningTool(MedicalTool):
    """
    Diagnostic reasoning tool.

    Generates differential diagnosis based on:
    - Symptom analysis
    - Patient history
    - Clinical reasoning
    - Evidence-based approach
    """

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "symptoms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of patient symptoms"
                },
                "patient_history": {
                    "type": "object",
                    "description": "Patient medical history, demographics"
                }
            },
            "required": ["symptoms"]
        }

    def execute(self, symptoms: List[str],
                patient_history: Optional[Dict] = None) -> ToolResult:
        """
        Execute diagnostic reasoning.

        Args:
            symptoms: List of patient symptoms
            patient_history: Optional patient medical history

        Returns:
            ToolResult with differential diagnosis
        """
        try:
            # Validate parameters
            is_valid, error = self.validate_parameters({"symptoms": symptoms})
            if not is_valid:
                return self.format_error(error)

            # Generate differential diagnosis
            differential = self._generate_differential(symptoms, patient_history)

            # Calculate confidence
            confidence = self._calculate_confidence(symptoms, patient_history, differential)

            return self.format_result(
                data={
                    "differential_diagnosis": differential,
                    "symptoms_analyzed": symptoms,
                    "patient_context_provided": patient_history is not None
                },
                confidence=confidence,
                metadata={
                    "tool": "diagnostic_reasoning",
                    "number_of_diagnoses": len(differential)
                }
            )

        except Exception as e:
            return self.format_error(f"Diagnostic reasoning failed: {str(e)}")

    def _generate_differential(self, symptoms: List[str],
                              patient_history: Optional[Dict]) -> List[Dict[str, Any]]:
        """Generate differential diagnosis."""
        differential = []

        # Analyze symptoms to generate potential diagnoses
        symptoms_str = " ".join(s.lower() for s in symptoms)

        # Cardiac symptoms
        if any(s in symptoms_str for s in ["chest pain", "chest discomfort", "pressure"]):
            differential.extend([
                {
                    "diagnosis": "Acute Coronary Syndrome",
                    "probability": self._assess_probability(symptoms, patient_history, "acs"),
                    "key_features": ["chest pain", "pressure", "radiation"],
                    "red_flags": ["radiating pain", "shortness of breath", "diaphoresis"],
                    "workup_recommendation": "ECG, troponin, urgent evaluation"
                },
                {
                    "diagnosis": "Pulmonary Embolism",
                    "probability": "low",
                    "key_features": ["pleuritic chest pain", "shortness of breath"],
                    "red_flags": ["tachycardia", "hypoxia", "risk factors"],
                    "workup_recommendation": "CT pulmonary angiogram, D-dimer"
                }
            ])

        # Neurological symptoms
        if any(s in symptoms_str for s in ["headache", "weakness", "numbness", "confusion"]):
            differential.append({
                "diagnosis": "Stroke/CVA",
                "probability": "moderate",
                "key_features": ["focal weakness", "speech difficulty", "vision changes"],
                "red flags": ["sudden onset", "FAST symptoms"],
                "workup_recommendation": "CT head, neurological evaluation, TIME IS BRAIN"
            })

        # Respiratory symptoms
        if any(s in symptoms_str for s in ["shortness of breath", "dyspnea", "cough"]):
            differential.append({
                "diagnosis": "Community Acquired Pneumonia",
                "probability": "moderate",
                "key_features": ["cough", "fever", "shortness of breath"],
                "red flags": ["high fever", "confusion", "hypotension"],
                "workup_recommendation": "CXR, CBC, blood cultures"
            })

        # If no specific pattern, add general categories
        if not differential:
            differential.append({
                "diagnosis": "Symptomatic - requires further evaluation",
                "probability": "unknown",
                "key_features": symptoms,
                "red_flags": [],
                "workup_recommendation": "Comprehensive history and physical examination"
            })

        return differential

    def _assess_probability(self, symptoms: List[str], history: Optional[Dict],
                           condition: str) -> str:
        """Assess probability of specific condition."""
        # Simple probability assessment
        # In production, use more sophisticated reasoning

        if history and history.get("age", 0) > 50 and condition == "acs":
            return "moderate to high"

        return "moderate"

    def _calculate_confidence(self, symptoms: List[str], history: Optional[Dict],
                            differential: List[Dict]) -> float:
        """Calculate confidence in differential diagnosis."""
        base_confidence = 0.6

        # Increase confidence with more symptoms
        symptom_bonus = min(0.2, len(symptoms) * 0.05)

        # Increase confidence with patient history
        history_bonus = 0.1 if history else 0.0

        confidence = base_confidence + symptom_bonus + history_bonus

        return min(0.85, max(0.5, confidence))


class LaboratoryInterpreterTool(MedicalTool):
    """
    Laboratory test interpretation tool.

    Interprets common laboratory tests with:
    - Reference ranges
    - Clinical significance
    - Pattern recognition
    """

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "test_results": {
                    "type": "object",
                    "description": "Laboratory test results with values"
                },
                "patient_context": {
                    "type": "object",
                    "description": "Patient demographics, clinical context"
                }
            },
            "required": ["test_results"]
        }

    def execute(self, test_results: Dict[str, Any],
                patient_context: Optional[Dict] = None) -> ToolResult:
        """
        Execute laboratory interpretation.

        Args:
            test_results: Dictionary of test name -> value
            patient_context: Optional patient context

        Returns:
            ToolResult with interpretation
        """
        try:
            # Validate parameters
            is_valid, error = self.validate_parameters({"test_results": test_results})
            if not is_valid:
                return self.format_error(error)

            # Interpret tests
            interpretation = self._interpret_tests(test_results, patient_context)

            return self.format_result(
                data={
                    "interpretation": interpretation,
                    "abnormal_results": interpretation["abnormal_results"],
                    "clinical_significance": interpretation["clinical_significance"]
                },
                confidence=0.90,
                metadata={
                    "tool": "laboratory_interpreter",
                    "tests_interpreted": list(test_results.keys())
                }
            )

        except Exception as e:
            return self.format_error(f"Laboratory interpretation failed: {str(e)}")

    def _interpret_tests(self, test_results: Dict, patient_context: Optional[Dict]) -> Dict[str, Any]:
        """Interpret laboratory tests."""
        interpretations = []
        abnormal_results = []

        # Common reference ranges
        reference_ranges = {
            "hemoglobin": (13.5, 17.5),  # g/dL for men
            "hematocrit": (41, 50),      # % for men
            "wbc": (4.5, 11.0),          # x10^9/L
            "platelets": (150, 450),     # x10^9/L
            "sodium": (135, 145),        # mmol/L
            "potassium": (3.5, 5.0),     # mmol/L
            "creatinine": (0.7, 1.3),    # mg/dL
            "glucose": (70, 100),        # mg/dL fasting
            "troponin": (0, 0.04)        # ng/mL
        }

        for test_name, value in test_results.items():
            if test_name in reference_ranges:
                lower, upper = reference_ranges[test_name]

                if isinstance(value, (int, float)):
                    if value < lower or value > upper:
                        abnormal_results.append({
                            "test": test_name,
                            "value": value,
                            "reference_range": f"{lower}-{upper}",
                            "abnormality": "low" if value < lower else "high"
                        })

                    interpretations.append({
                        "test": test_name,
                        "value": value,
                        "reference": f"{lower}-{upper}",
                        "interpretation": "normal" if lower <= value <= upper else "abnormal"
                    })

        # Assess clinical significance
        clinical_significance = self._assess_lab_significance(abnormal_results)

        return {
            "interpretations": interpretations,
            "abnormal_results": abnormal_results,
            "clinical_significance": clinical_significance
        }

    def _assess_lab_significance(self, abnormal_results: List[Dict]) -> str:
        """Assess clinical significance of abnormal labs."""
        if not abnormal_results:
            return "All tests within normal limits"

        # Check for critical abnormalities
        critical_tests = ["troponin", "potassium", "sodium"]
        for result in abnormal_results:
            if result["test"] in critical_tests:
                return f"CRITICAL: {result['test']} abnormal - urgent evaluation required"

        return f"Abnormalities present: {len(abnormal_results)} abnormal results"
