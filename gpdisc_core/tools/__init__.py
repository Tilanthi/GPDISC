"""
Medical Tools Package

Standardized tool interfaces and implementations for medical consultation.
"""

from .medical_tools import (
    MedicalTool,
    ToolResult,
    ECGInterpreterTool,
    DrugInteractionCheckerTool,
    DiagnosticReasoningTool,
    LaboratoryInterpreterTool
)

from .registry import (
    ToolRegistry,
    ToolCoordinator,
    create_standard_tool_registry,
    create_standard_tool_coordinator
)

__all__ = [
    "MedicalTool",
    "ToolResult",
    "ECGInterpreterTool",
    "DrugInteractionCheckerTool",
    "DiagnosticReasoningTool",
    "LaboratoryInterpreterTool",
    "ToolRegistry",
    "ToolCoordinator",
    "create_standard_tool_registry",
    "create_standard_tool_coordinator"
]
