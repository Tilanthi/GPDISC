"""
Orchestration Package

Medical consultation orchestration with task decomposition,
tool coordination, and context management.
"""

from .harness import (
    MedicalOrchestrationHarness,
    MedicalTaskDecomposer,
    ToolCoordinator,
    ConsultationResult,
    SubTask
)

from .context_manager import (
    MedicalContextManager,
    ConsultationContext,
    PatientSession
)

__all__ = [
    "MedicalOrchestrationHarness",
    "MedicalTaskDecomposer",
    "ToolCoordinator",
    "ConsultationResult",
    "SubTask",
    "MedicalContextManager",
    "ConsultationContext",
    "PatientSession"
]
