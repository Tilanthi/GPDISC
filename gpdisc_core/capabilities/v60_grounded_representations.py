"""V60 Grounded Representations - Concept grounding and composition"""
from enum import Enum
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field


class CompositionType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


class GroundingType(Enum):
    PERCEPTUAL = "perceptual"
    FUNCTIONAL = "functional"
    CONCEPTUAL = "conceptual"


class AbstractionLevel(Enum):
    CONCRETE = 0
    ABSTRACT = 1


@dataclass
class FeatureSpace:
    name: str
    dimensions: int = 0
    features: List[str] = field(default_factory=list)


@dataclass
class ConceptRepresentation:
    name: str
    features: Dict[str, Any] = field(default_factory=dict)
    feature_space: Optional[str] = None


class ConceptHierarchy:
    def __init__(self):
        self.concepts: Dict[str, ConceptRepresentation] = {}
        self.parent_child: Dict[str, List[str]] = {}
    def add(self, concept: ConceptRepresentation):
        self.concepts[concept.name] = concept


class CompositionEngine:
    def compose(self, concepts: List[ConceptRepresentation], composition_type: CompositionType) -> ConceptRepresentation:
        return ConceptRepresentation(name="composed")


class GroundingEngine:
    def ground(self, concept: str, grounding_type: GroundingType) -> ConceptRepresentation:
        return ConceptRepresentation(name=concept)


class AnalogyEngine:
    def find_analogy(self, source: str, target: str) -> float:
        return 0.5


class GroundedRepresentationSystem:
    def __init__(self):
        self.hierarchy = ConceptHierarchy()
        self.composer = CompositionEngine()
        self.grounder = GroundingEngine()
        self.analogy = AnalogyEngine()


def create_representation_system():
    return GroundedRepresentationSystem()

def create_concept(name: str, features: Dict[str, Any] = None):
    return ConceptRepresentation(name=name, features=features or {})

def create_grounding(concept: str, grounding_type: GroundingType):
    return GroundingEngine().ground(concept, grounding_type)


__all__ = ['CompositionType', 'GroundingType', 'AbstractionLevel', 'FeatureSpace',
           'ConceptRepresentation', 'ConceptHierarchy', 'CompositionEngine',
           'GroundingEngine', 'AnalogyEngine', 'GroundedRepresentationSystem',
           'create_representation_system', 'create_concept', 'create_grounding']
