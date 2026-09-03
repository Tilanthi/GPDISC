"""GPDISC clinical reasoning core (expertise program Stage 1).

Level 1 (expert general-medicine core) + Level 6 (safety & metacognition)
of the GP expertise architecture.
"""
from gpdisc_core.clinical_reasoning.knowledge import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
    CONDITIONS,
    SYMPTOM_SYNONYMS,
    conditions_for_symptom,
    find_condition,
)
from gpdisc_core.clinical_reasoning.test_interpretation import (
    TestInterpreter,
    REFERENCE_RANGES,
)
from gpdisc_core.clinical_reasoning.safety import (
    SafetyLayer,
    SafetyAssessment,
    EscalationLevel,
)
from gpdisc_core.clinical_reasoning.diagnostic_engine import (
    DifferentialEngine,
    RankedDiagnosis,
    DifferentialResult,
)
from gpdisc_core.clinical_reasoning.consultation import (
    ConsultationPipeline,
    ConsultationRecord,
)
from gpdisc_core.clinical_reasoning.syndromes import (
    SyndromeEngine,
    SyndromeFrame,
    SyndromeDifferential,
    SYNDROME_FRAMES,
    discriminating_questions,
)
from gpdisc_core.clinical_reasoning.benign_vs_emergency import (
    DiscriminationPair,
    PAIRS,
    find_pairs,
)
from gpdisc_core.clinical_reasoning.validation import (
    ClinicalValidator,
    ValidationReport,
    ValidationFinding,
)

__all__ = [
    "ConditionProfile",
    "InvestigationProfile",
    "SymptomFrequency",
    "CONDITIONS",
    "SYMPTOM_SYNONYMS",
    "conditions_for_symptom",
    "find_condition",
    "TestInterpreter",
    "REFERENCE_RANGES",
    "SafetyLayer",
    "SafetyAssessment",
    "EscalationLevel",
    "DifferentialEngine",
    "RankedDiagnosis",
    "DifferentialResult",
    "ConsultationPipeline",
    "ConsultationRecord",
    "SyndromeEngine",
    "SyndromeFrame",
    "SyndromeDifferential",
    "SYNDROME_FRAMES",
    "discriminating_questions",
    "DiscriminationPair",
    "PAIRS",
    "find_pairs",
    "ClinicalValidator",
    "ValidationReport",
    "ValidationFinding",
]
