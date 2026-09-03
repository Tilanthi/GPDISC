"""
V50 Abstraction Learning - Hierarchical abstraction and analogy discovery

Learns hierarchical abstractions, discovers analogies, and transfers
knowledge across domains.

Date: 2026-04-23
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import numpy as np


class AbstractionLevel(Enum):
    """Levels of abstraction"""
    CONCRETE = 0
    SPECIFIC = 1
    GENERAL = 2
    ABSTRACT = 3
    UNIVERSAL = 4


@dataclass
class Concept:
    """A concept at some level of abstraction"""
    name: str
    level: AbstractionLevel
    attributes: Dict[str, Any] = field(default_factory=dict)
    relations: Dict[str, Set[str]] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)


@dataclass
class Analogy:
    """An analogical relationship between concepts"""
    source_concept: str
    target_concept: str
    similarity_score: float
    shared_attributes: Set[str] = field(default_factory=set)
    structural_mappings: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.5


@dataclass
class AbstractionResult:
    """Result of abstraction process"""
    abstracted_concept: Optional[Concept] = None
    abstraction_level: AbstractionLevel = AbstractionLevel.SPECIFIC
    confidence: float = 0.0


@dataclass
class TransferResult:
    """Result of knowledge transfer"""
    transferred_knowledge: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    confidence: float = 0.0


class ConceptHierarchy:
    """Hierarchical organization of concepts"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.concepts: Dict[str, Concept] = {}
        self.hierarchy: Dict[str, List[str]] = {}  # parent -> children

    def add_concept(self, concept: Concept):
        """Add a concept to the hierarchy"""
        self.concepts[concept.name] = concept

    def add_parent_child(self, parent: str, child: str):
        """Add parent-child relationship"""
        if parent not in self.hierarchy:
            self.hierarchy[parent] = []
        if child not in self.hierarchy:
            self.hierarchy[child] = []

        if child not in self.hierarchy[parent]:
            self.hierarchy[parent].append(child)

    def get_children(self, concept: str) -> List[str]:
        """Get children of a concept"""
        return self.hierarchy.get(concept, [])

    def get_parents(self, concept: str) -> List[str]:
        """Get parents of a concept"""
        parents = []
        for parent, children in self.hierarchy.items():
            if concept in children:
                parents.append(parent)
        return parents

    def get_siblings(self, concept: str) -> List[str]:
        """Get siblings of a concept"""
        siblings = []
        parents = self.get_parents(concept)
        for parent in parents:
            siblings.extend(self.hierarchy.get(parent, []))
        return [s for s in siblings if s != concept]

    def find_lca(self, concept1: str, concept2: str) -> Optional[str]:
        """Find lowest common ancestor of two concepts"""
        ancestors1 = set(self.get_ancestors(concept1))
        ancestors2 = set(self.get_ancestors(concept2))

        common = ancestors1 & ancestors2
        if not common:
            return None

        # Return lowest (most specific) common ancestor
        return max(common, key=lambda c: self._depth(c))

    def get_ancestors(self, concept: str) -> List[str]:
        """Get all ancestors of a concept"""
        ancestors = []
        to_visit = self.get_parents(concept)

        while to_visit:
            current = to_visit.pop()
            if current not in ancestors:
                ancestors.append(current)
                to_visit.extend(self.get_parents(current))

        return ancestors

    def _depth(self, concept: str) -> int:
        """Get depth of concept in hierarchy"""
        return len(self.get_ancestors(concept))


class HierarchicalAbstractionLearner:
    """Learns hierarchical abstractions from examples"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.concept_hierarchy = ConceptHierarchy()

    def learn_abstraction(self, examples: List[Dict[str, Any]],
                         abstraction_level: AbstractionLevel = AbstractionLevel.GENERAL) -> AbstractionResult:
        """Learn an abstract concept from examples"""
        if not examples:
            return AbstractionResult()

        # Extract common attributes
        common_attributes = self._find_common_attributes(examples)

        # Create abstract concept
        concept_name = f"abstract_concept_{len(self.concept_hierarchy.concepts)}"
        concept = Concept(
            name=concept_name,
            level=abstraction_level,
            attributes=common_attributes,
            examples=[str(ex) for ex in examples[:3]]
        )

        self.concept_hierarchy.add_concept(concept)

        # Calculate confidence based on consistency
        confidence = self._calculate_consistency(examples, common_attributes)

        return AbstractionResult(
            abstracted_concept=concept,
            abstraction_level=abstraction_level,
            confidence=confidence
        )

    def _find_common_attributes(self, examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find attributes common to all examples"""
        if not examples:
            return {}

        common = set(examples[0].keys())

        for example in examples[1:]:
            common &= set(example.keys())

        # For common keys, check if values are similar
        result = {}
        for key in common:
            values = [example.get(key) for example in examples]

            # Check if all values are the same or similar
            if all(v == values[0] for v in values):
                result[key] = values[0]
            else:
                # Store type or range
                if isinstance(values[0], (int, float)):
                    result[key] = {
                        "type": "numeric",
                        "min": min(values),
                        "max": max(values)
                    }
                else:
                    result[key] = {
                        "type": type(values[0]).__name__,
                        "values": list(set(str(v) for v in values))
                    }

        return result

    def _calculate_consistency(self, examples: List[Dict[str, Any]],
                             common_attributes: Dict[str, Any]) -> float:
        """Calculate consistency of examples under common attributes"""
        if not examples or not common_attributes:
            return 0.0

        consistent_count = 0
        total_checks = 0

        for example in examples:
            for key, value in common_attributes.items():
                total_checks += 1

                if isinstance(value, dict):
                    # Range or type check
                    continue
                elif example.get(key) == value:
                    consistent_count += 1

        return consistent_count / total_checks if total_checks > 0 else 0.0


class AbstractionEngine:
    """Engine for creating and manipulating abstractions"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.abstractions: Dict[str, Concept] = {}

    def create_abstraction(self, name: str, level: AbstractionLevel,
                          attributes: Dict[str, Any]) -> Concept:
        """Create a new abstraction"""
        concept = Concept(
            name=name,
            level=level,
            attributes=attributes
        )

        self.abstractions[name] = concept
        return concept

    def abstract_from_instance(self, instance: Dict[str, Any],
                              target_level: AbstractionLevel) -> Optional[Concept]:
        """Abstract an instance to target level"""
        # Remove specific details based on target level
        abstracted = {}

        if target_level == AbstractionLevel.CONCRETE:
            abstracted = instance.copy()
        elif target_level == AbstractionLevel.SPECIFIC:
            # Keep most attributes, remove context-specific
            abstracted = {k: v for k, v in instance.items()
                         if not k.startswith('_')}
        elif target_level == AbstractionLevel.GENERAL:
            # Keep only main attributes
            abstracted = {k: v for k, v in instance.items()
                         if k in ['type', 'category', 'class']}
        elif target_level in [AbstractionLevel.ABSTRACT, AbstractionLevel.UNIVERSAL]:
            # Keep only type information
            abstracted = {'type': instance.get('type', type(instance).__name__)}

        if abstracted:
            name = f"abstraction_{target_level.name}_{len(self.abstractions)}"
            return self.create_abstraction(name, target_level, abstracted)

        return None

    def instantiate(self, concept: Concept, context: Dict[str, Any]) -> Dict[str, Any]:
        """Instantiate an abstract concept with specific context"""
        instance = concept.attributes.copy()
        instance.update(context)
        return instance


class AnalogyFinder:
    """Finds analogies between concepts"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.concepts: Dict[str, Concept] = {}

    def register_concept(self, concept: Concept):
        """Register a concept for analogy finding"""
        self.concepts[concept.name] = concept

    def find_analogy(self, source: str, target: str) -> Optional[Analogy]:
        """Find analogy between source and target concepts"""
        if source not in self.concepts or target not in self.concepts:
            return None

        source_concept = self.concepts[source]
        target_concept = self.concepts[target]

        # Find shared attributes
        shared_attrs = set(source_concept.attributes.keys()) & set(target_concept.attributes.keys())

        # Calculate similarity
        similarity = self._calculate_similarity(source_concept, target_concept)

        # Find structural mappings
        mappings = self._find_structural_mappings(source_concept, target_concept)

        return Analogy(
            source_concept=source,
            target_concept=target,
            similarity_score=similarity,
            shared_attributes=shared_attrs,
            structural_mappings=mappings,
            confidence=min(similarity, len(mappings) / 10)
        )

    def _calculate_similarity(self, concept1: Concept, concept2: Concept) -> float:
        """Calculate similarity between two concepts"""
        attrs1 = set(concept1.attributes.keys())
        attrs2 = set(concept2.attributes.keys())

        if not attrs1 and not attrs2:
            return 1.0
        if not attrs1 or not attrs2:
            return 0.0

        intersection = attrs1 & attrs2
        union = attrs1 | attrs2

        return len(intersection) / len(union)

    def _find_structural_mappings(self, concept1: Concept,
                                 concept2: Concept) -> Dict[str, str]:
        """Find structural mappings between concepts"""
        mappings = {}

        for attr1, value1 in concept1.attributes.items():
            for attr2, value2 in concept2.attributes.items():
                if attr1 == attr2 and value1 == value2:
                    mappings[attr1] = attr2

        return mappings

    def find_analogous_concepts(self, query: Concept,
                                threshold: float = 0.3) -> List[Tuple[str, float]]:
        """Find concepts analogous to query"""
        results = []

        for name, concept in self.concepts.items():
            if concept.name != query.name:
                similarity = self._calculate_similarity(query, concept)
                if similarity >= threshold:
                    results.append((name, similarity))

        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)

        return results


class KnowledgeTransferEngine:
    """Transfers knowledge across domains via analogy"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.analogy_finder = AnalogyFinder(config)

    def transfer_knowledge(self, source_domain: str, target_domain: str,
                          source_knowledge: Dict[str, Any]) -> TransferResult:
        """Transfer knowledge from source to target domain"""
        # Find analogy between domains
        # In practice, would use registered concepts

        # Simple transfer: map attribute names
        transferred = {}

        for key, value in source_knowledge.items():
            # Apply domain-specific transformations
            new_key = self._transform_key(key, source_domain, target_domain)
            new_value = self._transform_value(value, source_domain, target_domain)

            transferred[new_key] = new_value

        # Calculate confidence based on mapping quality
        confidence = self._calculate_transfer_confidence(source_knowledge, transferred)

        return TransferResult(
            transferred_knowledge=transferred,
            success=True,
            confidence=confidence
        )

    def _transform_key(self, key: str, source: str, target: str) -> str:
        """Transform key for target domain"""
        # Simple transformation
        return key.replace(source, target)

    def _transform_value(self, value: Any, source: str, target: str) -> Any:
        """Transform value for target domain"""
        # In practice, would do domain-specific transformations
        return value

    def _calculate_transfer_confidence(self, source: Dict[str, Any],
                                      transferred: Dict[str, Any]) -> float:
        """Calculate confidence in transferred knowledge"""
        if not source:
            return 0.0

        # Simple metric: ratio of successfully transferred items
        return len(transferred) / len(source)


# Factory functions
def create_abstraction_learner(config: Optional[Dict[str, Any]] = None) -> HierarchicalAbstractionLearner:
    """Create an abstraction learner"""
    return HierarchicalAbstractionLearner(config)


def create_concept_hierarchy(config: Optional[Dict[str, Any]] = None) -> ConceptHierarchy:
    """Create a concept hierarchy"""
    return ConceptHierarchy(config)


def create_analogy_finder(config: Optional[Dict[str, Any]] = None) -> AnalogyFinder:
    """Create an analogy finder"""
    return AnalogyFinder(config)


def create_transfer_engine(config: Optional[Dict[str, Any]] = None) -> KnowledgeTransferEngine:
    """Create a knowledge transfer engine"""
    return KnowledgeTransferEngine(config)


__all__ = [
    'AbstractionLevel',
    'Concept',
    'Analogy',
    'AbstractionResult',
    'TransferResult',
    'ConceptHierarchy',
    'HierarchicalAbstractionLearner',
    'AbstractionEngine',
    'AnalogyFinder',
    'KnowledgeTransferEngine',
    'create_abstraction_learner',
    'create_concept_hierarchy',
    'create_analogy_finder',
    'create_transfer_engine',
]
