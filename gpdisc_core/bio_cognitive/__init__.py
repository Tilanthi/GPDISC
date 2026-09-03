"""
Bio-Cognitive Discovery Layer (BCDL) for GPDISC

A transformational architectural layer that enables GPDISC to transition from
knowledge retrieval to knowledge creation through autonomous scientific discovery.

This layer sits above the 10 biology domain modules and provides:
1. Abductive Theory Formation - Generate novel scientific hypotheses
2. Temporal Causal Discovery - Learn causal structure from time-series data
3. Multi-Scale Reasoning - Integrate knowledge across biological scales
4. Experimental Design - Generate experimental protocols
5. Discovery Value Calculation - Prioritize research directions

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Import BCDL modules
try:
    from .abductive_theory_former import (
        AbductiveTheoryFormer,
        HypothesisGenerator,
        KnowledgeGapIdentifier,
        TheorySynthesizer,
        MechanismExplainer,
        Hypothesis,
        KnowledgeGap,
        Theory,
        Mechanism
    )
    ABDUCTIVE_THEORY_FORMER_AVAILABLE = True
except ImportError:
    ABDUCTIVE_THEORY_FORMER_AVAILABLE = False
    logger.warning("Abductive Theory Former not available")

try:
    from .temporal_causal_discovery import (
        TemporalCausalDiscovery,
        TimeSeriesCausalLearner,
        DynamicSystemModeler,
        StatePredictor,
        InterventionOptimizer,
        TemporalCausalGraph,
        DynamicModel,
        StatePrediction,
        Intervention,
        CausalInferenceMethod,
        SystemType,
        CausalEdge
    )
    TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE = True
    logger.info("Temporal Causal Discovery module loaded")
except ImportError as e:
    TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE = False
    logger.warning(f"Temporal Causal Discovery not available: {e}")

try:
    from .multi_scale_reasoner import (
        MultiScaleReasoner,
        ScaleMapper,
        EmergentPropertyDetector,
        PerturbationPropagator,
        ScaleInvariantReasoner,
        ScaleMapping,
        EmergentProperty,
        PerturbationPath,
        ScaleInvariantMechanism,
        BiologicalScale,
        ScaleRelationship
    )
    MULTI_SCALE_REASONER_AVAILABLE = True
    logger.info("Multi-Scale Reasoner module loaded")
except ImportError as e:
    MULTI_SCALE_REASONER_AVAILABLE = False
    logger.warning(f"Multi-Scale Reasoner not available: {e}")

try:
    from .experimental_designer import (
        ExperimentalDesigner,
        ProtocolGenerator,
        InformationGainOptimizer,
        ControlSuggester,
        OutcomePredictor,
        ExperimentalProtocol,
        OptimizationResult,
        ControlExperiment,
        OutcomePrediction,
        ExperimentalType,
        InformationMetric
    )
    EXPERIMENTAL_DESIGNER_AVAILABLE = True
    logger.info("Experimental Designer module loaded")
except ImportError as e:
    EXPERIMENTAL_DESIGNER_AVAILABLE = False
    logger.warning(f"Experimental Designer not available: {e}")

try:
    from .discovery_value_calculator import (
        DiscoveryValueCalculator,
        ResearchPrioritizer,
        InformationGainEstimator,
        ImpactPredictor,
        ResourceOptimizer,
        ResearchPriority,
        ValueEstimate,
        ImpactPrediction,
        ResourceAllocation,
        ImpactMetric,
        ResourceConstraint
    )
    DISCOVERY_VALUE_CALCULATOR_AVAILABLE = True
    logger.info("Discovery Value Calculator module loaded")
except ImportError as e:
    DISCOVERY_VALUE_CALCULATOR_AVAILABLE = False
    logger.warning(f"Discovery Value Calculator not available: {e}")


class BioCognitiveDiscoveryLayer:
    """
    Main orchestrator for the Bio-Cognitive Discovery Layer

    Coordinates all 5 BCDL modules to enable autonomous scientific discovery:
    - Generates novel hypotheses through abductive reasoning
    - Learns causal structure from temporal data
    - Integrates knowledge across biological scales
    - Designs experiments to test hypotheses
    - Prioritizes research for maximum impact
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Bio-Cognitive Discovery Layer

        Args:
            config: Configuration dictionary for BCDL modules
        """
        self.config = config or {}

        # Initialize available modules
        self.abductive_theory_former = None
        self.temporal_causal_discovery = None
        self.multi_scale_reasoner = None
        self.experimental_designer = None
        self.discovery_value_calculator = None

        # Try to initialize each module
        if ABDUCTIVE_THEORY_FORMER_AVAILABLE:
            try:
                self.abductive_theory_former = AbductiveTheoryFormer(
                    self.config.get('abductive', {})
                )
                logger.info("Abductive Theory Former initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Abductive Theory Former: {e}")

        if TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE:
            try:
                self.temporal_causal_discovery = TemporalCausalDiscovery(
                    self.config.get('temporal_causal', {})
                )
                logger.info("Temporal Causal Discovery initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Temporal Causal Discovery: {e}")

        if MULTI_SCALE_REASONER_AVAILABLE:
            try:
                self.multi_scale_reasoner = MultiScaleReasoner(
                    self.config.get('multi_scale', {})
                )
                logger.info("Multi-Scale Reasoner initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Multi-Scale Reasoner: {e}")

        if EXPERIMENTAL_DESIGNER_AVAILABLE:
            try:
                self.experimental_designer = ExperimentalDesigner(
                    self.config.get('experimental_design', {})
                )
                logger.info("Experimental Designer initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Experimental Designer: {e}")

        if DISCOVERY_VALUE_CALCULATOR_AVAILABLE:
            try:
                self.discovery_value_calculator = DiscoveryValueCalculator(
                    self.config.get('discovery_value', {})
                )
                logger.info("Discovery Value Calculator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Discovery Value Calculator: {e}")

        # Check if at least one module is available
        if not any([
            self.abductive_theory_former,
            self.temporal_causal_discovery,
            self.multi_scale_reasoner,
            self.experimental_designer,
            self.discovery_value_calculator
        ]):
            raise RuntimeError("No BCDL modules available - cannot initialize")

        logger.info("Bio-Cognitive Discovery Layer initialized")

    def discover(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "full"
    ) -> Dict[str, Any]:
        """
        Perform autonomous scientific discovery

        Args:
            query: Scientific query or phenomenon to investigate
            context: Additional context (data, constraints, etc.)
            mode: Discovery mode ("full", "hypothesis_only", "experimental_only")

        Returns:
            Discovery results including hypotheses, experimental designs, etc.
        """
        context = context or {}
        results = {
            'query': query,
            'mode': mode,
            'hypotheses': [],
            'temporal_models': [],
            'multi_scale_insights': [],
            'experimental_designs': [],
            'research_priorities': [],
            'synthesis': None
        }

        try:
            # Phase 1: Generate hypotheses
            if self.abductive_theory_former and mode in ["full", "hypothesis_only"]:
                hypotheses = self.abductive_theory_former.generate_hypotheses(
                    query, context
                )
                results['hypotheses'] = hypotheses

                # Identify knowledge gaps
                gaps = self.abductive_theory_former.identify_gaps(query, context)
                results['knowledge_gaps'] = gaps

                # Synthesize theory
                theory = self.abductive_theory_former.synthesize_theory(
                    query, context, hypotheses
                )
                results['synthesis'] = theory

            # Phase 2: Temporal causal discovery
            if self.temporal_causal_discovery and mode in ["full", "temporal_only"]:
                if 'temporal_data' in context:
                    temporal_models = self.temporal_causal_discovery.learn_from_data(
                        context['temporal_data']
                    )
                    results['temporal_models'] = temporal_models

            # Phase 3: Multi-scale reasoning
            if self.multi_scale_reasoner and mode in ["full", "multi_scale_only"]:
                if 'multi_scale_data' in context:
                    scale_insights = self.multi_scale_reasoner.reason_across_scales(
                        context['multi_scale_data']
                    )
                    results['multi_scale_insights'] = scale_insights

            # Phase 4: Experimental design
            if self.experimental_designer and mode in ["full", "experimental_only"]:
                if results['hypotheses']:
                    for hypothesis in results['hypotheses'][:3]:  # Top 3 hypotheses
                        design = self.experimental_designer.design_experiment(
                            hypothesis, context
                        )
                        results['experimental_designs'].append(design)

            # Phase 5: Discovery value calculation
            if self.discovery_value_calculator and mode == "full":
                priorities = self.discovery_value_calculator.prioritize_research(
                    query, results, context
                )
                results['research_priorities'] = priorities

            logger.info(f"Discovery complete for query: {query[:50]}...")

        except Exception as e:
            logger.error(f"Error during discovery: {e}")
            results['error'] = str(e)

        return results

    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities"""
        capabilities = []

        if self.abductive_theory_former:
            capabilities.extend([
                "hypothesis_generation",
                "knowledge_gap_identification",
                "theory_synthesis",
                "mechanism_explanation"
            ])

        if self.temporal_causal_discovery:
            capabilities.extend([
                "temporal_causal_discovery",
                "dynamic_system_modeling",
                "state_prediction",
                "intervention_optimization"
            ])

        if self.multi_scale_reasoner:
            capabilities.extend([
                "multi_scale_reasoning",
                "emergent_property_detection",
                "perturbation_propagation",
                "scale_invariant_reasoning"
            ])

        if self.experimental_designer:
            capabilities.extend([
                "experimental_design",
                "protocol_generation",
                "information_gain_optimization",
                "outcome_prediction"
            ])

        if self.discovery_value_calculator:
            capabilities.extend([
                "research_prioritization",
                "information_gain_estimation",
                "impact_prediction",
                "resource_optimization"
            ])

        return capabilities

    def get_status(self) -> Dict[str, Any]:
        """Get status of all BCDL modules"""
        return {
            'abductive_theory_former': self.abductive_theory_former is not None,
            'temporal_causal_discovery': self.temporal_causal_discovery is not None,
            'multi_scale_reasoner': self.multi_scale_reasoner is not None,
            'experimental_designer': self.experimental_designer is not None,
            'discovery_value_calculator': self.discovery_value_calculator is not None,
            'total_capabilities': len(self.get_capabilities())
        }


def create_bio_cognitive_layer(config: Optional[Dict[str, Any]] = None) -> BioCognitiveDiscoveryLayer:
    """
    Factory function to create Bio-Cognitive Discovery Layer

    Args:
        config: Configuration dictionary

    Returns:
        Initialized BioCognitiveDiscoveryLayer instance
    """
    return BioCognitiveDiscoveryLayer(config)


__all__ = [
    # Main orchestrator
    'BioCognitiveDiscoveryLayer',
    'create_bio_cognitive_layer',

    # Module availability flags
    'ABDUCTIVE_THEORY_FORMER_AVAILABLE',
    'TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE',
    'MULTI_SCALE_REASONER_AVAILABLE',
    'EXPERIMENTAL_DESIGNER_AVAILABLE',
    'DISCOVERY_VALUE_CALCULATOR_AVAILABLE',

    # Abductive Theory Former exports
    'AbductiveTheoryFormer',
    'HypothesisGenerator',
    'KnowledgeGapIdentifier',
    'TheorySynthesizer',
    'MechanismExplainer',
    'Hypothesis',
    'KnowledgeGap',
    'Theory',
    'Mechanism',

    # Temporal Causal Discovery exports
    'TemporalCausalDiscovery',
    'TimeSeriesCausalLearner',
    'DynamicSystemModeler',
    'StatePredictor',
    'InterventionOptimizer',
    'TemporalCausalGraph',
    'DynamicModel',
    'StatePrediction',
    'Intervention',
    'CausalInferenceMethod',
    'SystemType',
    'CausalEdge',

    # Multi-Scale Reasoner exports
    'MultiScaleReasoner',
    'ScaleMapper',
    'EmergentPropertyDetector',
    'PerturbationPropagator',
    'ScaleInvariantReasoner',
    'ScaleMapping',
    'EmergentProperty',
    'PerturbationPath',
    'ScaleInvariantMechanism',
    'BiologicalScale',
    'ScaleRelationship',

    # Experimental Designer exports
    'ExperimentalDesigner',
    'ProtocolGenerator',
    'InformationGainOptimizer',
    'ControlSuggester',
    'OutcomePredictor',
    'ExperimentalProtocol',
    'OptimizationResult',
    'ControlExperiment',
    'OutcomePrediction',
    'ExperimentalType',
    'InformationMetric',

    # Discovery Value Calculator exports
    'DiscoveryValueCalculator',
    'ResearchPrioritizer',
    'InformationGainEstimator',
    'ImpactPredictor',
    'ResourceOptimizer',
    'ResearchPriority',
    'ValueEstimate',
    'ImpactPrediction',
    'ResourceAllocation',
    'ImpactMetric',
    'ResourceConstraint',
]
