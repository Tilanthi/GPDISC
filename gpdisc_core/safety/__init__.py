"""
GPDISC Safety Module

Patient safety systems including drug-drug interaction checking,
contraindication detection, and clinical decision support.

All safety checks performed locally - no external API calls.
"""

from .drug_interactions import (
    DrugInteractionChecker,
    DrugInteraction,
    InteractionCheckResult,
    InteractionSeverity,
    InteractionEvidence,
    create_interaction_checker,
    check_drugs_interact,
    check_patient_medications,
    check_new_prescription
)

from .medical_safety_layers import (
    MedicalSafetyLayers,
    EmergencyDetector,
    FactualConsistencyChecker,
    ClinicalAppropriatenessChecker,
    SafetyValidation,
    SafetyCheckResult,
    SafetyCheck
)

from .medical_measurement_verification import (
    MedicalMeasurementVerifier,
    MeasurementValue,
    MeasurementCategory,
    VerificationResult,
    verify_measurement,
    halt_on_critical_discrepancy
)

from .safe_medical_report_reader import (
    SafeMedicalReportReader,
    VerifiedMedicalReport,
    safely_read_report
)

__all__ = [
    'DrugInteractionChecker',
    'DrugInteraction',
    'InteractionCheckResult',
    'InteractionSeverity',
    'InteractionEvidence',
    'create_interaction_checker',
    'check_drugs_interact',
    'check_patient_medications',
    'check_new_prescription',
    'MedicalSafetyLayers',
    'EmergencyDetector',
    'FactualConsistencyChecker',
    'ClinicalAppropriatenessChecker',
    'SafetyValidation',
    'SafetyCheckResult',
    'SafetyCheck',
    'MedicalMeasurementVerifier',
    'MeasurementValue',
    'MeasurementCategory',
    'VerificationResult',
    'verify_measurement',
    'halt_on_critical_discrepancy',
    'SafeMedicalReportReader',
    'VerifiedMedicalReport',
    'safely_read_report'
]
