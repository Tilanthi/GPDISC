"""
Multi-Scale Reasoner Module for GPDISC

Integrates knowledge across biological scales and discovers cross-scale emergent
properties. This enables GPDISC to reason about how phenomena at the molecular
level affect cellular behavior, tissue properties, and organism-level outcomes.

Key capabilities:
- Scale mapping: Map entities and relationships across biological scales
- Emergent property detection: Discover properties that emerge at specific scales
- Perturbation propagation: Model how perturbations propagate across scales
- Scale-invariant reasoning: Find mechanisms that are consistent across scales

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)


class BiologicalScale(Enum):
    """Biological scales from molecular to organism"""
    MOLECULAR = "molecular"      # Atoms, molecules, complexes
    SUPRAMOLECULAR = "supramolecular"  # Protein complexes, assemblies
    CELLULAR = "cellular"      # Cells, organelles
    TISSUE = "tissue"          # Tissues, organs
    ORGANISM = "organism"      # Whole organism, behavior


class ScaleRelationship(Enum):
    """Types of relationships between scales"""
    COMPOSITION = "composition"      # Higher scale composed of lower scale
    EMERGENCE = "emergence"         # Property emerges at higher scale
    CAUSATION = "causation"          # Lower scale causes higher scale
    REGULATION = "regulation"        # Higher scale regulates lower
    CORRELATION = "correlation"      # Correlated across scales


@dataclass
class ScaleMapping:
    """
    A mapping of an entity or relationship across biological scales

    Attributes:
        entity: The entity being mapped
        scale_mappings: Dictionary mapping scales to representations
        relationships: Relationships between scales
        confidence: Confidence in the mapping
    """
    entity: str
    scale_mappings: Dict[str, str] = field(default_factory=dict)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'entity': self.entity,
            'scale_mappings': self.scale_mappings,
            'relationships': self.relationships,
            'confidence': self.confidence
        }


@dataclass
class EmergentProperty:
    """
    A property that emerges at a specific biological scale

    Attributes:
        name: Name of the emergent property
        scale: Scale at which property emerges
        description: Description of the property
        constituents: Lower-scale components that give rise to it
        mechanism: Mechanism of emergence
        observables: How the property can be observed
        confidence: Confidence in the emergence claim
    """
    name: str
    scale: BiologicalScale
    description: str
    constituents: List[str] = field(default_factory=list)
    mechanism: str = ""
    observables: List[str] = field(default_factory=list)
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'scale': self.scale.value,
            'description': self.description,
            'constituents': self.constituents,
            'mechanism': self.mechanism,
            'observables': self.observables,
            'confidence': self.confidence
        }


@dataclass
class PerturbationPath:
    """
    A pathway showing how a perturbation propagates across scales

    Attributes:
        origin_scale: Scale where perturbation originates
        target_scale: Scale of final effect
        pathway: Sequence of intermediate steps
        magnitude: Magnitude of effect
        time_course: How effect unfolds over time
        confidence: Confidence in the pathway
    """
    origin_scale: BiologicalScale
    target_scale: BiologicalScale
    pathway: List[Dict[str, Any]] = field(default_factory=list)
    magnitude: float = 0.5
    time_course: str = ""
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'origin_scale': self.origin_scale.value,
            'target_scale': self.target_scale.value,
            'pathway': self.pathway,
            'magnitude': self.magnitude,
            'time_course': self.time_course,
            'confidence': self.confidence
        }


@dataclass
class ScaleInvariantMechanism:
    """
    A mechanism that operates consistently across multiple scales

    Attributes:
        name: Name of the mechanism
        description: Description of the mechanism
        scales: Scales at which mechanism operates
        invariant_properties: Properties that are scale-invariant
        scaling_laws: Mathematical descriptions of scaling behavior
        examples: Examples at different scales
        confidence: Confidence in scale-invariance
    """
    name: str
    description: str
    scales: List[BiologicalScale] = field(default_factory=list)
    invariant_properties: List[str] = field(default_factory=list)
    scaling_laws: List[str] = field(default_factory=list)
    examples: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'scales': [s.value for s in self.scales],
            'invariant_properties': self.invariant_properties,
            'scaling_laws': self.scaling_laws,
            'examples': self.examples,
            'confidence': self.confidence
        }


class ScaleMapper:
    """
    Maps entities and relationships across biological scales

    Creates representations of how the same phenomenon manifests
    at different scales and how entities relate across scales.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Scale Mapper

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Define scale hierarchy
        self.scale_hierarchy = [
            BiologicalScale.MOLECULAR,
            BiologicalScale.SUPRAMOLECULAR,
            BiologicalScale.CELLULAR,
            BiologicalScale.TISSUE,
            BiologicalScale.ORGANISM
        ]

        # Common scale mappings
        self.scale_vocabulary = {
            BiologicalScale.MOLECULAR: ['atom', 'molecule', 'binding site', 'conformation', 'complex'],
            BiologicalScale.SUPRAMOLECULAR: ['protein complex', 'assembly', 'aggregation', 'phase'],
            BiologicalScale.CELLULAR: ['organelle', 'compartment', 'cytoskeleton', 'membrane', 'gradient'],
            BiologicalScale.TISSUE: ['tissue architecture', 'organization', 'pattern', 'structure'],
            BiologicalScale.ORGANISM: ['organism', 'behavior', 'physiology', 'phenotype', 'system']
        }

    def map_entity(
        self,
        entity: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ScaleMapping:
        """
        Map an entity across biological scales

        Args:
            entity: Entity to map (e.g., "protein misfolding")
            context: Additional context

        Returns:
            Scale mapping for the entity
        """
        context = context or {}

        try:
            # Identify which scales the entity belongs to
            identified_scales = []
            for scale, vocab in self.scale_vocabulary.items():
                if any(term in entity.lower() for term in vocab):
                    identified_scales.append(scale)

            # If no specific scale identified, default to molecular
            if not identified_scales:
                identified_scales = [BiologicalScale.MOLECULAR]

            # Generate mappings across scales
            scale_mappings = {}
            for scale in identified_scales:
                scale_mappings[scale.value] = self._generate_scale_representation(entity, scale, context)

            # Generate relationships between scales
            relationships = self._generate_scale_relationships(identified_scales, entity, context)

            # Calculate confidence
            confidence = min(1.0, 0.3 + 0.2 * len(identified_scales))

            mapping = ScaleMapping(
                entity=entity,
                scale_mappings=scale_mappings,
                relationships=relationships,
                confidence=confidence
            )

            logger.info(f"Mapped '{entity}' across {len(identified_scales)} scales")

        except Exception as e:
            logger.error(f"Error mapping entity: {e}")
            mapping = ScaleMapping(
                entity=entity,
                confidence=0.0
            )

        return mapping

    def _generate_scale_representation(
        self,
        entity: str,
        scale: BiologicalScale,
        context: Dict[str, Any]
    ) -> str:
        """Generate representation of entity at a specific scale"""
        representations = {
            BiologicalScale.MOLECULAR: f"Molecular interactions and conformations of {entity}",
            BiologicalScale.SUPRAMOLECULAR: f"Supramolecular assemblies involving {entity}",
            BiologicalScale.CELLULAR: f"Cellular localization and function of {entity}",
            BiologicalScale.TISSUE: f"Tissue-level distribution and patterning of {entity}",
            BiologicalScale.ORGANISM: f"Organism-level effects and phenotypes of {entity}"
        }
        return representations.get(scale, f"{entity} at {scale.value} scale")

    def _generate_scale_relationships(
        self,
        scales: List[BiologicalScale],
        entity: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate relationships between scales"""
        relationships = []

        # Sort scales by hierarchy
        sorted_scales = sorted(scales, key=lambda s: self.scale_hierarchy.index(s))

        # Generate relationships between adjacent scales
        for i in range(len(sorted_scales) - 1):
            lower_scale = sorted_scales[i]
            higher_scale = sorted_scales[i + 1]

            relationships.append({
                'from': lower_scale.value,
                'to': higher_scale.value,
                'type': ScaleRelationship.COMPOSITION.value,
                'description': f"{entity} at {lower_scale.value} composes {entity} at {higher_scale.value} scale"
            })

            relationships.append({
                'from': higher_scale.value,
                'to': lower_scale.value,
                'type': ScaleRelationship.REGULATION.value,
                'description': f"{entity} at {higher_scale.value} can regulate {entity} at {lower_scale.value} scale"
            })

        return relationships


class EmergentPropertyDetector:
    """
    Detects properties that emerge at specific biological scales

    Identifies phenomena that cannot be predicted from lower-scale
    components alone.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Emergent Property Detector

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Common emergent properties at different scales
        self.known_emergent_properties = {
            BiologicalScale.SUPRAMOLECULAR: [
                "Allosteric regulation",
                "Cooperative binding",
                "Phase separation",
                "Protein aggregation"
            ],
            BiologicalScale.CELLULAR: [
                "Cell cycle control",
                "Apoptosis",
                "Differentiation",
                "Polarity"
            ],
            BiologicalScale.TISSUE: [
                "Tissue patterning",
                "Morphogenesis",
                "Homeostasis",
                "Regeneration"
            ],
            BiologicalScale.ORGANISM: [
                "Behavior",
                "Circadian rhythms",
                "Metabolism",
                "Aging"
            ]
        }

    def detect(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        num_properties: int = 5
    ) -> List[EmergentProperty]:
        """
        Detect emergent properties related to a query

        Args:
            query: Scientific query or phenomenon
            context: Additional context
            num_properties: Number of properties to detect

        Returns:
            List of detected emergent properties
        """
        context = context or {}
        properties = []

        try:
            # Identify relevant scales from query
            relevant_scales = self._identify_relevant_scales(query)

            # Detect emergent properties at relevant scales
            for scale in relevant_scales:
                known_properties = self.known_emergent_properties.get(scale, [])

                for prop in known_properties:
                    # Check if property is relevant to query
                    if self._is_relevant_to_query(prop, query, context):
                        # Create emergent property
                        emergent_property = EmergentProperty(
                            name=prop,
                            scale=scale,
                            description=f"Emergent property of {prop} at {scale.value} scale",
                            constituents=self._identify_constituents(prop, scale),
                            mechanism=self._infer_emergence_mechanism(prop, scale),
                            observables=self._suggest_observables(prop, scale),
                            confidence=0.6
                        )
                        properties.append(emergent_property)

                        if len(properties) >= num_properties:
                            break

                if len(properties) >= num_properties:
                    break

            # Generate novel emergent properties if needed
            if len(properties) < num_properties:
                novel_properties = self._generate_novel_emergent_properties(
                    query, relevant_scales, num_properties - len(properties)
                )
                properties.extend(novel_properties)

            # Sort by confidence
            properties.sort(key=lambda p: p.confidence, reverse=True)

            logger.info(f"Detected {len(properties)} emergent properties")

        except Exception as e:
            logger.error(f"Error detecting emergent properties: {e}")

        return properties[:num_properties]

    def _identify_relevant_scales(self, query: str) -> List[BiologicalScale]:
        """Identify which scales are relevant to the query"""
        query_lower = query.lower()

        relevant_scales = []
        if any(term in query_lower for term in ['molecule', 'protein', 'binding', 'complex']):
            relevant_scales.append(BiologicalScale.MOLECULAR)
            relevant_scales.append(BiologicalScale.SUPRAMOLECULAR)

        if any(term in query_lower for term in ['cell', 'organelle', 'compartment']):
            relevant_scales.append(BiologicalScale.CELLULAR)

        if any(term in query_lower for term in ['tissue', 'organ', 'pattern']):
            relevant_scales.append(BiologicalScale.TISSUE)

        if any(term in query_lower for term in ['organism', 'system', 'behavior']):
            relevant_scales.append(BiologicalScale.ORGANISM)

        # Default to including cellular scale
        if not relevant_scales:
            relevant_scales = [
                BiologicalScale.CELLULAR,
                BiologicalScale.TISSUE
            ]

        return relevant_scales

    def _is_relevant_to_query(
        self,
        property_name: str,
        query: str,
        context: Dict[str, Any]
    ) -> bool:
        """Check if an emergent property is relevant to the query"""
        query_lower = query.lower()
        property_lower = property_name.lower()

        # Check for keyword overlap
        property_words = set(property_lower.split('_'))
        query_words = set(query_lower.split())

        return bool(property_words & query_words)

    def _identify_constituents(
        self,
        property_name: str,
        scale: BiologicalScale
    ) -> List[str]:
        """Identify lower-scale constituents of an emergent property"""
        # Simplified constituency mapping
        constituents = []

        if scale == BiologicalScale.SUPRAMOLECULAR:
            constituents = ["Proteins", "Ligands", "Ions"]
        elif scale == BiologicalScale.CELLULAR:
            constituents = ["Protein complexes", "Organelles", "Molecular assemblies"]
        elif scale == BiologicalScale.TISSUE:
            constituents = ["Cells", "Extracellular matrix", "Signaling molecules"]
        elif scale == BiologicalScale.ORGANISM:
            constituents = ["Tissues", "Organ systems", "Physiological processes"]

        return constituents

    def _infer_emergence_mechanism(
        self,
        property_name: str,
        scale: BiologicalScale
    ) -> str:
        """Infer the mechanism by which a property emerges"""
        mechanisms = {
            BiologicalScale.SUPRAMOLECULAR: "Nonlinear interactions between components",
            BiologicalScale.CELLULAR: "Spatial organization and feedback loops",
            BiologicalScale.TISSUE: "Cell-cell communication and spatial patterning",
            BiologicalScale.ORGANISM: "System-level feedback and homeostatic regulation"
        }
        return mechanisms.get(scale, "Complex interactions")

    def _suggest_observables(
        self,
        property_name: str,
        scale: BiologicalScale
    ) -> List[str]:
        """Suggest how the emergent property can be observed"""
        observables = []

        if scale == BiologicalScale.SUPRAMOLECULAR:
            observables = [
                "Measure binding kinetics",
                "Assess cooperativity",
                "Monitor assembly/disassembly"
            ]
        elif scale == BiologicalScale.CELLULAR:
            observables = [
                "Live-cell imaging",
                "Fluorescence microscopy",
                "Functional assays"
            ]
        elif scale == BiologicalScale.TISSUE:
            observables = [
                "Histological analysis",
                "In vivo imaging",
                "Tissue-level function assays"
            ]
        elif scale == BiologicalScale.ORGANISM:
            observables = [
                "Behavioral assays",
                "Physiological measurements",
                "System-level monitoring"
            ]

        return observables

    def _generate_novel_emergent_properties(
        self,
        query: str,
        scales: List[BiologicalScale],
        num_properties: int
    ) -> List[EmergentProperty]:
        """Generate novel (hypothetical) emergent properties"""
        properties = []

        # Extract key terms from query
        query_words = query.lower().split()

        # Generate novel properties based on combinations
        for scale in scales:
            if len(properties) >= num_properties:
                break

            # Generate novel property name
            novel_name = f"Cross-scale integration of {query_words[0] if query_words else 'entity'}"

            property = EmergentProperty(
                name=novel_name,
                scale=scale,
                description=f"Hypothesized emergent property at {scale.value} scale",
                constituents=[f"Components at {scale.value} scale"],
                mechanism="Hypothetical integration mechanism",
                observables=["Experimental validation needed"],
                confidence=0.3  # Lower confidence for novel properties
            )
            properties.append(property)

        return properties


class PerturbationPropagator:
    """
    Models how perturbations propagate across biological scales

    Predicts how interventions at one scale affect other scales,
    enabling prediction of system-wide effects from targeted interventions.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Perturbation Propagator

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Define propagation patterns
        self.propagation_patterns = {
            (BiologicalScale.MOLECULAR, BiologicalScale.SUPRAMOLECULAR): {
                'delay': 'seconds',
                'amplification': 1.5,
                'noise': 0.1
            },
            (BiologicalScale.SUPRAMOLECULAR, BiologicalScale.CELLULAR): {
                'delay': 'minutes',
                'amplification': 2.0,
                'noise': 0.2
            },
            (BiologicalScale.CELLULAR, BiologicalScale.TISSUE): {
                'delay': 'hours',
                'amplification': 3.0,
                'noise': 0.3
            },
            (BiologicalScale.TISSUE, BiologicalScale.ORGANISM): {
                'delay': 'hours to days',
                'amplification': 5.0,
                'noise': 0.4
            }
        }

    def propagate(
        self,
        perturbation: Dict[str, Any],
        origin_scale: BiologicalScale,
        target_scale: BiologicalScale,
        context: Optional[Dict[str, Any]] = None
    ) -> PerturbationPath:
        """
        Model how a perturbation propagates across scales

        Args:
            perturbation: Description of the perturbation
            origin_scale: Scale where perturbation originates
            target_scale: Scale of final interest
            context: Additional context

        Returns:
            Perturbation pathway showing propagation across scales
        """
        context = context or {}

        try:
            # Get scale hierarchy index
            scale_hierarchy = [
                BiologicalScale.MOLECULAR,
                BiologicalScale.SUPRAMOLECULAR,
                BiologicalScale.CELLULAR,
                BiologicalScale.TISSUE,
                BiologicalScale.ORGANISM
            ]

            origin_idx = scale_hierarchy.index(origin_scale)
            target_idx = scale_hierarchy.index(target_scale)

            # Generate pathway steps
            pathway = []
            current_magnitude = perturbation.get('magnitude', 1.0)

            for i in range(origin_idx, target_idx):
                current_scale = scale_hierarchy[i]
                next_scale = scale_hierarchy[i + 1] if i + 1 < len(scale_hierarchy) else target_scale

                # Get propagation pattern
                pattern = self.propagation_patterns.get(
                    (current_scale, next_scale),
                    {'delay': 'unknown', 'amplification': 1.0, 'noise': 0.0}
                )

                # Update magnitude
                current_magnitude *= pattern['amplification']

                # Create pathway step
                step = {
                    'from_scale': current_scale.value,
                    'to_scale': next_scale.value,
                    'effect_size': current_magnitude,
                    'delay': pattern['delay'],
                    'mechanism': f"Propagation from {current_scale.value} to {next_scale.value}"
                }
                pathway.append(step)

            # Calculate overall magnitude
            final_magnitude = current_magnitude

            # Generate time course description
            time_course = self._generate_time_course(pathway)

            # Calculate confidence
            confidence = 0.7 - 0.1 * abs(target_idx - origin_idx)

            path = PerturbationPath(
                origin_scale=origin_scale,
                target_scale=target_scale,
                pathway=pathway,
                magnitude=final_magnitude,
                time_course=time_course,
                confidence=confidence
            )

            logger.info(f"Modeled perturbation propagation from {origin_scale.value} to {target_scale.value}")

        except Exception as e:
            logger.error(f"Error modeling perturbation propagation: {e}")
            path = PerturbationPath(
                origin_scale=origin_scale,
                target_scale=target_scale,
                pathway=[],
                magnitude=0.5,
                confidence=0.0
            )

        return path

    def _generate_time_course(self, pathway: List[Dict[str, Any]]) -> str:
        """Generate description of time course"""
        if not pathway:
            return "No propagation"

        delays = [step.get('delay', '') for step in pathway]
        return f"Effects propagate through scales with delays: {' → '.join(delays)}"


class ScaleInvariantReasoner:
    """
    Finds mechanisms that are consistent across biological scales

    Identifies scale-invariant principles and mechanisms that operate
    consistently across multiple levels of biological organization.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Scale-Invariant Reasoner

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Known scale-invariant mechanisms
        self.known_invariant_mechanisms = {
            "Mass conservation": {
                'description': "Mass is conserved across all scales",
                'scales': [BiologicalScale.MOLECULAR, BiologicalScale.SUPRAMOLECULAR, BiologicalScale.CELLULAR],
                'invariant': "Total mass remains constant"
            },
            "Energy minimization": {
                'description': "Systems tend toward energy-minimizing states",
                'scales': [BiologicalScale.MOLECULAR, BiologicalScale.SUPRAMOLECULAR, BiologicalScale.CELLULAR],
                'invariant': "Free energy is minimized"
            },
            "Information processing": {
                'description': "Information is processed through similar computational motifs",
                'scales': [BiologicalScale.CELLULAR, BiologicalScale.TISSUE, BiologicalScale.ORGANISM],
                'invariant': "Network motifs encode information"
            },
            "Homeostatic regulation": {
                'description': "Systems maintain stable states through feedback",
                'scales': [BiologicalScale.CELLULAR, BiologicalScale.TISSUE, BiologicalScale.ORGANISM],
                'invariant': "Negative feedback maintains stability"
            },
            "Diffusion-limited processes": {
                'description': "Diffusion constrains processes across scales",
                'scales': [BiologicalScale.MOLECULAR, BiologicalScale.SUPRAMOLECULAR, BiologicalScale.CELLULAR, BiologicalScale.TISSUE],
                'invariant': "Fick's laws apply"
            }
        }

    def find_invariants(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        num_invariants: int = 3
    ) -> List[ScaleInvariantMechanism]:
        """
        Find scale-invariant mechanisms relevant to a query

        Args:
            query: Scientific query or phenomenon
            context: Additional context
            num_invariants: Number of invariants to find

        Returns:
            List of scale-invariant mechanisms
        """
        context = context or {}
        invariants = []

        try:
            # Identify relevant scales
            relevant_scales = self._identify_relevant_scales(query)

            # Find known invariants that apply to relevant scales
            for name, inv_data in self.known_invariant_mechanisms.items():
                # Check if invariant applies to relevant scales
                applicable_scales = inv_data['scales']
                overlap = set(relevant_scales) & set(applicable_scales)

                if overlap:
                    # Create scale-invariant mechanism
                    mechanism = ScaleInvariantMechanism(
                        name=name,
                        description=inv_data['description'],
                        scales=list(applicable_scales),
                        invariant_properties=[inv_data['invariant']],
                        scaling_laws=self._generate_scaling_law(name, applicable_scales),
                        examples=self._generate_examples(name, query),
                        confidence=0.8  # High confidence for known invariants
                    )
                    invariants.append(mechanism)

                    if len(invariants) >= num_invariants:
                        break

            # Generate novel scale-invariant hypotheses if needed
            if len(invariants) < num_invariants:
                novel_invariants = self._generate_novel_invariants(
                    query, relevant_scales, num_invariants - len(invariants)
                )
                invariants.extend(novel_invariants)

            # Sort by confidence
            invariants.sort(key=lambda m: m.confidence, reverse=True)

            logger.info(f"Found {len(invariants)} scale-invariant mechanisms")

        except Exception as e:
            logger.error(f"Error finding scale-invariants: {e}")

        return invariants[:num_invariants]

    def _identify_relevant_scales(self, query: str) -> List[BiologicalScale]:
        """Identify scales relevant to query"""
        query_lower = query.lower()

        relevant_scales = []
        if 'molecule' in query_lower or 'protein' in query_lower:
            relevant_scales.extend([
                BiologicalScale.MOLECULAR,
                BiologicalScale.SUPRAMOLECULAR
            ])

        if 'cell' in query_lower:
            relevant_scales.extend([
                BiologicalScale.CELLULAR
            ])

        if 'tissue' in query_lower or 'organ' in query_lower:
            relevant_scales.extend([
                BiologicalScale.TISSUE,
                BiologicalScale.ORGANISM
            ])

        # Default to all scales if none identified
        if not relevant_scales:
            relevant_scales = list(BiologicalScale)

        return list(set(relevant_scales))

    def _generate_scaling_law(
        self,
        mechanism_name: str,
        scales: List[BiologicalScale]
    ) -> List[str]:
        """Generate scaling laws for a mechanism"""
        laws = []

        if "Diffusion" in mechanism_name:
            laws.append("Mean squared displacement ∝ time")
            laws.append("Flux ∝ concentration gradient / distance")

        elif "Mass conservation" in mechanism_name:
            laws.append("Σ inputs = Σ outputs (steady state)")

        elif "Energy" in mechanism_name:
            laws.append("ΔG < 0 for spontaneous processes")
            laws.append("Equilibrium: ΔG = 0")

        return laws

    def _generate_examples(
        self,
        mechanism_name: str,
        query: str
    ) -> Dict[str, str]:
        """Generate examples of mechanism at different scales"""
        examples = {}

        if "Diffusion" in mechanism_name:
            examples['molecular'] = "Molecular diffusion in cytoplasm"
            examples['cellular'] = "Organelle transport within cell"
            examples['tissue'] = "Morphogen gradient across tissue"

        elif "Homeostatic" in mechanism_name:
            examples['cellular'] = "Cell cycle control checkpoints"
            examples['tissue'] = "Tissue repair and regeneration"
            examples['organism'] = "Body temperature regulation"

        return examples

    def _generate_novel_invariants(
        self,
        query: str,
        scales: List[BiologicalScale],
        num_invariants: int
    ) -> List[ScaleInvariantMechanism]:
        """Generate novel (hypothetical) scale-invariant mechanisms"""
        invariants = []

        query_words = query.lower().split()

        for i in range(num_invariants):
            # Generate novel invariant name
            novel_name = f"Cross-scale principle {i+1}: {query_words[0] if query_words else 'entity'}"

            invariant = ScaleInvariantMechanism(
                name=novel_name,
                description=f"Hypothesized scale-invariant principle for {query_words[0] if query_words else 'entity'}",
                scales=scales,
                invariant_properties=["Property remains consistent across scales"],
                scaling_laws=["To be determined"],
                examples={"hypothetical": "Requires experimental validation"},
                confidence=0.3  # Lower confidence for novel invariants
            )
            invariants.append(invariant)

        return invariants


class MultiScaleReasoner:
    """
    Main orchestrator for Multi-Scale Reasoning

    Coordinates scale mapping, emergent property detection,
    perturbation propagation, and scale-invariant reasoning.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Multi-Scale Reasoner

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Initialize components
        self.scale_mapper = ScaleMapper(config)
        self.emergent_detector = EmergentPropertyDetector(config)
        self.perturbation_propagator = PerturbationPropagator(config)
        self.invariant_reasoner = ScaleInvariantReasoner(config)

        logger.info("Multi-Scale Reasoner initialized")

    def reason_across_scales(
        self,
        query: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform multi-scale reasoning on a query

        Args:
            query: Scientific query or phenomenon
            data: Multi-scale data (optional)
            **kwargs: Additional arguments

        Returns:
            Multi-scale reasoning results
        """
        data = data or {}
        results = {
            'query': query,
            'scale_mappings': [],
            'emergent_properties': [],
            'perturbation_pathways': [],
            'scale_invariants': [],
            'synthesis': None
        }

        try:
            # Map entity across scales
            mapping = self.scale_mapper.map_entity(query, data)
            results['scale_mappings'] = [mapping.to_dict()]

            # Detect emergent properties
            properties = self.emergent_detector.detect(query, data, num_properties=5)
            results['emergent_properties'] = [p.to_dict() for p in properties]

            # Model perturbation propagation
            if 'perturbation' in data:
                pert = data['perturbation']
                origin = data.get('origin_scale', BiologicalScale.MOLECULAR)
                target = data.get('target_scale', BiologicalScale.ORGANISM)
                pathway = self.perturbation_propagator.propagate(pert, origin, target, data)
                results['perturbation_pathways'] = [pathway.to_dict()]

            # Find scale-invariant mechanisms
            invariants = self.invariant_reasoner.find_invariants(query, data, num_invariants=3)
            results['scale_invariants'] = [inv.to_dict() for inv in invariants]

            # Synthesize multi-scale insights
            results['synthesis'] = self._synthesize_multi_scale_insights(results)

            logger.info(f"Multi-scale reasoning complete for query: {query[:50]}...")

        except Exception as e:
            logger.error(f"Error in multi-scale reasoning: {e}")
            results['error'] = str(e)

        return results

    def _synthesize_multi_scale_insights(self, results: Dict[str, Any]) -> str:
        """Synthesize multi-scale reasoning insights"""
        synthesis_parts = []

        if results['scale_mappings']:
            mapping = results['scale_mappings'][0]
            synthesis_parts.append(f"Entity '{mapping['entity']}' maps across scales with {mapping['confidence']:.2f} confidence")

        if results['emergent_properties']:
            count = len(results['emergent_properties'])
            synthesis_parts.append(f"Detected {count} emergent properties across biological scales")

        if results['scale_invariants']:
            count = len(results['scale_invariants'])
            synthesis_parts.append(f"Identified {count} scale-invariant mechanisms")

        if results['perturbation_pathways']:
            synthesis_parts.append("Modeled perturbation propagation across scales")

        return "; ".join(synthesis_parts) if synthesis_parts else "Multi-scale analysis complete"


__all__ = [
    # Main orchestrator
    'MultiScaleReasoner',

    # Components
    'ScaleMapper',
    'EmergentPropertyDetector',
    'PerturbationPropagator',
    'ScaleInvariantReasoner',

    # Data classes
    'ScaleMapping',
    'EmergentProperty',
    'PerturbationPath',
    'ScaleInvariantMechanism',

    # Enums
    'BiologicalScale',
    'ScaleRelationship',
]
