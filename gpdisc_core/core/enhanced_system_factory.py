"""
Enhanced GPDISC System Factory

Creates enhanced GPDISC system with all new architectural components:
- Orchestration harness
- Multi-layer safety
- Tool coordination
- Memory integration
- Specialty coordination
"""

from typing import Optional, Dict, Any
from ..orchestration import MedicalOrchestrationHarness, MedicalContextManager
from ..safety import MedicalSafetyLayers
from ..confidence import ConfidenceCalibrator
from ..tools import create_standard_tool_coordinator, ToolCoordinator
from ..coordination import SpecialtyCoordinator
from ..memory.persistent import create_integrator


def create_enhanced_gpdisc_system(
    domain_registry: Optional[Dict] = None,
    enable_safety_layers: bool = True,
    enable_tool_coordination: bool = True,
    enable_specialty_coordination: bool = True,
    enable_memory_integration: bool = True
) -> MedicalOrchestrationHarness:
    """
    Create enhanced GPDISC system with all architectural improvements.

    Args:
        domain_registry: Dictionary of domain name -> domain module
        enable_safety_layers: Enable multi-layer safety validation
        enable_tool_coordination: Enable standardized tool coordination
        enable_specialty_coordination: Enable multi-specialty coordination
        enable_memory_integration: Enable enhanced memory integration

    Returns:
        Configured MedicalOrchestrationHarness
    """
    domain_registry = domain_registry or {}

    # Create confidence calibrator
    confidence_calibrator = ConfidenceCalibrator()

    # Create safety validator if enabled
    safety_validator = None
    if enable_safety_layers:
        safety_validator = MedicalSafetyLayers()

    # Create tool coordinator if enabled
    tool_coordinator = None
    if enable_tool_coordination:
        tool_coordinator = create_standard_tool_coordinator()

    # Create memory system if enabled
    memory_system = None
    if enable_memory_integration:
        try:
            memory_system = create_integrator()
            memory_system.initialize_session()
        except Exception as e:
            print(f"Warning: Could not initialize memory system: {e}")

    # Create context manager if memory is enabled
    if memory_system:
        context_manager = MedicalContextManager(memory_system)
    else:
        context_manager = None

    # Create orchestration harness
    harness = MedicalOrchestrationHarness(
        domain_registry=domain_registry,
        memory_system=memory_system,
        safety_validator=safety_validator,
        confidence_calibrator=confidence_calibrator
    )

    # Attach additional components
    harness.tool_coordinator = tool_coordinator
    harness.context_manager = context_manager

    # Create specialty coordinator if enabled
    if enable_specialty_coordination:
        harness.specialty_coordinator = SpecialtyCoordinator(domain_registry)

    return harness


def create_gpdisc_with_coordination(
    domain_registry: Optional[Dict] = None
) -> MedicalOrchestrationHarness:
    """
    Create GPDISC system with specialty coordination enabled.

    Args:
        domain_registry: Dictionary of domain name -> domain module

    Returns:
        Configured MedicalOrchestrationHarness with coordination
    """
    return create_enhanced_gpdisc_system(
        domain_registry=domain_registry,
        enable_safety_layers=True,
        enable_tool_coordination=True,
        enable_specialty_coordination=True,
        enable_memory_integration=True
    )


def create_gpdisc_minimal(
    domain_registry: Optional[Dict] = None
) -> MedicalOrchestrationHarness:
    """
    Create minimal GPDISC system (orchestration only).

    Args:
        domain_registry: Dictionary of domain name -> domain module

    Returns:
        Basic MedicalOrchestrationHarness
    """
    return create_enhanced_gpdisc_system(
        domain_registry=domain_registry,
        enable_safety_layers=False,
        enable_tool_coordination=False,
        enable_specialty_coordination=False,
        enable_memory_integration=False
    )
