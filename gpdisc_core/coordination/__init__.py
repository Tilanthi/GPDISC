"""
Specialty Coordination Package

Coordinates multi-specialty consultations with conflict resolution
and second opinion generation.
"""

from .specialty_coordinator import (
    SpecialtyCoordinator,
    ConflictDetector,
    ConflictResolver,
    SecondOpinionGenerator,
    SpecialtyOpinion,
    OpinionConflict,
    CoordinatedResult,
    ConflictSeverity
)

__all__ = [
    "SpecialtyCoordinator",
    "ConflictDetector",
    "ConflictResolver",
    "SecondOpinionGenerator",
    "SpecialtyOpinion",
    "OpinionConflict",
    "CoordinatedResult",
    "ConflictSeverity"
]
