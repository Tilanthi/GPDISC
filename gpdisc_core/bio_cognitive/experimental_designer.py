"""
Experimental Design Orchestrator for GPDISC Bio-Cognitive Discovery Layer

This module generates experimental protocols to test hypotheses and optimize
for information gain. It enables GPDISC to transition from passive knowledge
retrieval to active experimental design.

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import numpy as np
from scipy import optimize
from scipy.stats import entropy

logger = logging.getLogger(__name__)


class ExperimentalType(Enum):
    """Types of experimental designs"""
    OBSERVATIONAL = "observational"
    INTERVENTION = "intervention"
    PERTURBATION = "perturbation"
    COMPARATIVE = "comparative"
    LONGITUDINAL = "longitudinal"
    HIGH_THROUGHPUT = "high_throughput"
    SINGLE_CELL = "single_cell"
    IMAGING = "imaging"
    OMICS = "omics"
    BEHAVIORAL = "behavioral"


class InformationMetric(Enum):
    """Metrics for information gain calculation"""
    SHANNON_ENTROPY = "shannon_entropy"
    KULLBACK_LEIBLER = "kl_divergence"
    MUTUAL_INFORMATION = "mutual_information"
    BAYESIAN_INFORMATION_GAIN = "bayesian_information_gain"
    EXPECTED_VARIANCE_REDUCTION = "variance_reduction"
    CAUSAL_DISCOVERY_SCORE = "causal_discovery_score"


@dataclass
class ExperimentalProtocol:
    """Generated experimental protocol"""
    protocol_id: str
    name: str
    description: str
    experimental_type: ExperimentalType
    hypothesis: str

    # Protocol details
    steps: List[Dict[str, Any]]
    materials: List[str]
    equipment: List[str]
    duration: Dict[str, Any]  # {'prep': hours, 'execution': hours, 'analysis': hours}

    # Expected outcomes
    expected_outcomes: List[str]
    predicted_observations: List[str]
    success_criteria: List[str]

    # Information metrics
    expected_information_gain: float
    confidence_bounds: Tuple[float, float]
    cost_estimate: Dict[str, Any]

    # Controls and validation
    control_experiments: List['ControlExperiment']
    validation_methods: List[str]
    potential_confounders: List[str]

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ControlExperiment:
    """Control experiment specification"""
    control_id: str
    name: str
    description: str
    control_type: str  # negative, positive, sham, vehicle, etc.
    purpose: str
    modifications: Dict[str, Any]
    expected_result: str


@dataclass
class OptimizationResult:
    """Result of information gain optimization"""
    optimal_design: ExperimentalProtocol
    expected_information_gain: float
    alternative_designs: List[ExperimentalProtocol]
    optimization_trace: List[Dict[str, Any]]
    sensitivity_analysis: Dict[str, Any]
    convergence_criteria: List[str]


@dataclass
class OutcomePrediction:
    """Prediction of experimental outcomes"""
    predicted_outcomes: List[Dict[str, Any]]
    confidence_intervals: List[Tuple[float, float]]
    probability_distribution: Dict[str, float]
    sensitivity_to_parameters: Dict[str, float]
    alternative_hypothesis_support: Dict[str, float]
    recommended_measurements: List[str]


class ProtocolGenerator:
    """
    Generates detailed experimental protocols for testing biological hypotheses

    Uses templates from biological literature and domain knowledge to create
    rigorous, reproducible experimental protocols.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ProtocolGenerator

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Experimental templates (would be loaded from knowledge base in full implementation)
        self.templates = self._initialize_templates()

        # Biological techniques database
        self.techniques = self._initialize_techniques()

        logger.info("ProtocolGenerator initialized")

    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize experimental protocol templates"""
        return {
            'protein_interaction': {
                'type': ExperimentalType.INTERVENTION,
                'steps': ['sample_preparation', 'treatment', 'measurement', 'analysis'],
                'equipment': ['centrifuge', 'spectrophotometer', 'incubator'],
                'duration': {'prep': 2, 'execution': 24, 'analysis': 4}
            },
            'gene_expression': {
                'type': ExperimentalType.OMICS,
                'steps': ['rna_extraction', 'library_prep', 'sequencing', 'analysis'],
                'equipment': ['rna_sequencer', 'qPCR_machine', 'bioanalyzer'],
                'duration': {'prep': 4, 'execution': 48, 'analysis': 24}
            },
            'cellular_imaging': {
                'type': ExperimentalType.IMAGING,
                'steps': ['cell_culture', 'staining', 'imaging', 'analysis'],
                'equipment': ['microscope', 'incubator', 'plate_reader'],
                'duration': {'prep': 24, 'execution': 4, 'analysis': 8}
            },
            'drug_response': {
                'type': ExperimentalType.COMPARATIVE,
                'steps': ['cell_culture', 'drug_treatment', 'viability_assay', 'analysis'],
                'equipment': ['incubator', 'plate_reader', 'pipettes'],
                'duration': {'prep': 24, 'execution': 72, 'analysis': 4}
            }
        }

    def _initialize_techniques(self) -> Dict[str, Dict[str, Any]]:
        """Initialize biological techniques database"""
        return {
            'crispr': {
                'category': 'genetic_perturbation',
                'precision': 'high',
                'information_content': 0.9,
                'cost': 'medium'
            },
            'rnaseq': {
                'category': 'omics',
                'precision': 'high',
                'information_content': 0.95,
                'cost': 'high'
            },
            'western_blot': {
                'category': 'protein_analysis',
                'precision': 'medium',
                'information_content': 0.7,
                'cost': 'low'
            },
            'microscopy': {
                'category': 'imaging',
                'precision': 'high',
                'information_content': 0.85,
                'cost': 'medium'
            },
            'flow_cytometry': {
                'category': 'single_cell',
                'precision': 'high',
                'information_content': 0.8,
                'cost': 'medium'
            }
        }

    def _extract_hypothesis_text(self, hypothesis) -> str:
        """Extract hypothesis text from string or dict"""
        if isinstance(hypothesis, dict):
            return hypothesis.get('statement', str(hypothesis))
        return str(hypothesis)

    def generate(
        self,
        hypothesis: str,
        experimental_type: Optional[ExperimentalType] = None,
        constraints: Optional[Dict[str, Any]] = None,
        available_techniques: Optional[List[str]] = None
    ) -> ExperimentalProtocol:
        """
        Generate experimental protocol for hypothesis testing

        Args:
            hypothesis: Hypothesis to test
            experimental_type: Type of experiment (auto-detected if None)
            constraints: Experimental constraints (time, budget, equipment)
            available_techniques: List of available experimental techniques

        Returns:
            Complete experimental protocol
        """
        constraints = constraints or {}
        available_techniques = available_techniques or list(self.techniques.keys())

        # Analyze hypothesis to determine experimental type
        if experimental_type is None:
            experimental_type = self._infer_experimental_type(hypothesis)

        # Select appropriate template
        template = self._select_template(hypothesis, experimental_type)

        # Generate protocol steps
        steps = self._generate_steps(hypothesis, template, constraints)

        # Select techniques
        techniques = self._select_techniques(hypothesis, experimental_type, available_techniques)

        # Generate materials list
        materials = self._generate_materials(hypothesis, techniques)

        # Generate equipment list
        equipment = self._generate_equipment(techniques, template)

        # Estimate duration
        duration = self._estimate_duration(steps, techniques)

        # Define expected outcomes
        expected_outcomes = self._predict_outcomes(hypothesis, techniques)

        # Generate success criteria
        success_criteria = self._generate_success_criteria(hypothesis)

        # Estimate initial information gain (will be refined by optimizer)
        initial_info_gain = self._estimate_initial_information_gain(hypothesis, techniques)

        # Create protocol
        hypothesis_text = self._extract_hypothesis_text(hypothesis)
        protocol = ExperimentalProtocol(
            protocol_id=f"exp_{hash(hypothesis_text) % 1000000:06d}",
            name=f"Test: {hypothesis_text[:80]}",
            description=f"Experimental protocol to test: {hypothesis_text}",
            experimental_type=experimental_type,
            hypothesis=hypothesis_text,
            steps=steps,
            materials=materials,
            equipment=equipment,
            duration=duration,
            expected_outcomes=expected_outcomes,
            predicted_observations=[],
            success_criteria=success_criteria,
            expected_information_gain=initial_info_gain,
            confidence_bounds=(initial_info_gain * 0.7, initial_info_gain * 1.3),
            cost_estimate=self._estimate_cost(techniques, duration),
            control_experiments=[],  # Will be populated by ControlSuggester
            validation_methods=[],
            potential_confounders=[],
            metadata={
                'techniques_used': techniques,
                'template_used': template.get('name', 'custom')
            }
        )

        logger.info(f"Generated protocol: {protocol.protocol_id}")
        return protocol

    def _infer_experimental_type(self, hypothesis: str) -> ExperimentalType:
        """Infer experimental type from hypothesis"""
        # Handle both string and dict hypotheses
        if isinstance(hypothesis, dict):
            hypothesis_text = hypothesis.get('statement', str(hypothesis))
        else:
            hypothesis_text = str(hypothesis)

        hypothesis_lower = hypothesis_text.lower()

        # Keywords for different experiment types
        type_keywords = {
            ExperimentalType.PERTURBATION: ['perturb', 'knockdown', 'knockout', 'inhibit', 'disrupt'],
            ExperimentalType.INTERVENTION: ['treat', 'administer', 'apply', 'intervene'],
            ExperimentalType.OMICS: ['transcriptom', 'proteom', 'genom', 'metabolom', 'expression'],
            ExperimentalType.IMAGING: ['visualize', 'image', 'microscopy', 'localization'],
            ExperimentalType.SINGLE_CELL: ['single cell', 'heterogeneity', 'cell-to-cell'],
            ExperimentalType.COMPARATIVE: ['compare', 'difference', 'versus', 'relative'],
            ExperimentalType.LONGITUDINAL: ['temporal', 'time course', 'kinetics', 'dynamics'],
        }

        for exp_type, keywords in type_keywords.items():
            if any(kw in hypothesis_lower for kw in keywords):
                return exp_type

        # Default to intervention
        return ExperimentalType.INTERVENTION

    def _select_template(self, hypothesis: str, exp_type: ExperimentalType) -> Dict[str, Any]:
        """Select appropriate experimental template"""
        # In full implementation, would use semantic matching
        # For now, return generic template
        return {
            'name': 'generic',
            'type': exp_type,
            'steps': ['preparation', 'execution', 'measurement', 'analysis'],
            'equipment': [],
            'duration': {'prep': 1, 'execution': 24, 'analysis': 2}
        }

    def _generate_steps(
        self,
        hypothesis: str,
        template: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate detailed experimental steps"""
        steps = []

        template_steps = template.get('steps', ['preparation', 'execution', 'analysis'])

        for i, step_name in enumerate(template_steps, 1):
            steps.append({
                'step_number': i,
                'name': step_name,
                'description': f"Perform {step_name} for hypothesis testing",
                'duration_hours': template.get('duration', {}).get(step_name, 1),
                'critical_points': [],
                'potential_issues': []
            })

        return steps

    def _select_techniques(
        self,
        hypothesis: str,
        exp_type: ExperimentalType,
        available: List[str]
    ) -> List[str]:
        """Select optimal techniques for hypothesis"""
        # Score techniques by information content
        scored = []
        for tech in available:
            if tech in self.techniques:
                tech_info = self.techniques[tech]
                score = tech_info['information_content']
                scored.append((tech, score))

        # Sort by score and return top 3
        scored.sort(key=lambda x: x[1], reverse=True)
        return [tech for tech, _ in scored[:3]]

    def _generate_materials(self, hypothesis: str, techniques: List[str]) -> List[str]:
        """Generate materials list"""
        materials = ['cell culture media', 'buffer solutions']

        for tech in techniques:
            if tech == 'crispr':
                materials.extend(['cas9 protein', 'grna', 'donor template'])
            elif tech == 'rnaseq':
                materials.extend(['rna extraction kit', 'library prep kit'])
            elif tech == 'western_blot':
                materials.extend(['antibodies', 'membranes', 'substrates'])

        return materials

    def _generate_equipment(self, techniques: List[str], template: Dict[str, Any]) -> List[str]:
        """Generate equipment list"""
        equipment = template.get('equipment', ['pipettes', 'centrifuge'])

        for tech in techniques:
            if tech == 'rnaseq':
                equipment.append('sequencer')
            elif tech == 'microscopy':
                equipment.append('microscope')

        return list(set(equipment))

    def _estimate_duration(self, steps: List[Dict[str, Any]], techniques: List[str]) -> Dict[str, Any]:
        """Estimate experiment duration"""
        prep_time = sum(step.get('duration_hours', 1) for step in steps if 'prep' in step['name'].lower())
        exec_time = sum(step.get('duration_hours', 1) for step in steps if 'exec' in step['name'].lower())
        analysis_time = sum(step.get('duration_hours', 1) for step in steps if 'anal' in step['name'].lower())

        return {
            'prep': max(prep_time, 4),
            'execution': max(exec_time, 24),
            'analysis': max(analysis_time, 8),
            'total': max(prep_time, 4) + max(exec_time, 24) + max(analysis_time, 8)
        }

    def _predict_outcomes(self, hypothesis: str, techniques: List[str]) -> List[str]:
        """Predict experimental outcomes"""
        return [
            "Quantitative measurement of hypothesized effect",
            "Statistical significance assessment",
            "Effect size estimation"
        ]

    def _generate_success_criteria(self, hypothesis: str) -> List[str]:
        """Generate success criteria"""
        return [
            "P-value < 0.05 for primary outcome",
            "Effect size > 0.5 (Cohen's d)",
            "Reproducibility across replicates (CV < 20%)"
        ]

    def _estimate_initial_information_gain(self, hypothesis: str, techniques: List[str]) -> float:
        """Estimate initial information gain"""
        # Base information gain from hypothesis
        base_gain = 0.5

        # Add technique-specific information
        tech_bonus = sum(self.techniques.get(t, {}).get('information_content', 0.5) for t in techniques)

        return min(base_gain + tech_bonus * 0.3, 1.0)

    def _estimate_cost(self, techniques: List[str], duration: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate experiment cost"""
        # Cost estimation based on techniques and duration
        tech_costs = {
            'crispr': 500,
            'rnaseq': 1000,
            'western_blot': 200,
            'microscopy': 300,
            'flow_cytometry': 400
        }

        material_cost = sum(tech_costs.get(t, 250) for t in techniques)
        time_cost = duration['total'] * 50  # $50 per hour

        return {
            'materials': material_cost,
            'labor': time_cost,
            'total': material_cost + time_cost,
            'currency': 'USD'
        }


class InformationGainOptimizer:
    """
    Optimizes experimental designs for maximum information gain

    Uses Bayesian experimental design and information theory to maximize
    the expected information gain from experiments.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize InformationGainOptimizer

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.metric = InformationMetric(
            self.config.get('metric', 'bayesian_information_gain')
        )

        logger.info("InformationGainOptimizer initialized")

    def optimize(
        self,
        protocol: ExperimentalProtocol,
        hypothesis_space: Optional[List[str]] = None,
        constraints: Optional[Dict[str, Any]] = None,
        n_alternatives: int = 5
    ) -> OptimizationResult:
        """
        Optimize experimental protocol for maximum information gain

        Args:
            protocol: Initial protocol to optimize
            hypothesis_space: Alternative hypotheses to consider
            constraints: Optimization constraints (budget, time, etc.)
            n_alternatives: Number of alternative designs to generate

        Returns:
            Optimization result with optimal design and alternatives
        """
        constraints = constraints or {}

        # Calculate information gain for initial protocol
        initial_gain = self._calculate_information_gain(
            protocol, hypothesis_space
        )

        # Generate alternative designs
        alternatives = self._generate_alternatives(
            protocol, n_alternatives, constraints
        )

        # Score all designs
        designs = [protocol] + alternatives
        scores = []

        for design in designs:
            score = self._calculate_information_gain(design, hypothesis_space)
            scores.append((design, score))

        # Sort by information gain
        scores.sort(key=lambda x: x[1], reverse=True)

        # Select optimal design
        optimal_design, optimal_gain = scores[0]
        optimal_design.expected_information_gain = optimal_gain

        # Generate optimization trace
        trace = [
            {
                'iteration': i,
                'design_id': d.protocol_id,
                'information_gain': s,
                'parameters': self._extract_design_parameters(d)
            }
            for i, (d, s) in enumerate(scores)
        ]

        # Perform sensitivity analysis
        sensitivity = self._perform_sensitivity_analysis(optimal_design, hypothesis_space)

        result = OptimizationResult(
            optimal_design=optimal_design,
            expected_information_gain=optimal_gain,
            alternative_designs=[d for d, _ in scores[1:n_alternatives+1]],
            optimization_trace=trace,
            sensitivity_analysis=sensitivity,
            convergence_criteria=[
                f"Information gain plateau: {scores[0][1] - scores[-1][1]:.3f}",
                f"Optimal design: {optimal_design.protocol_id}"
            ]
        )

        logger.info(f"Optimization complete: {optimal_gain:.3f} information gain")
        return result

    def _calculate_information_gain(
        self,
        protocol: ExperimentalProtocol,
        hypothesis_space: Optional[List[str]] = None
    ) -> float:
        """
        Calculate expected information gain for protocol

        Args:
            protocol: Experimental protocol
            hypothesis_space: Alternative hypotheses

        Returns:
            Expected information gain (0-1)
        """
        # Base information from experimental type
        type_gain = {
            ExperimentalType.OMICS: 0.9,
            ExperimentalType.SINGLE_CELL: 0.85,
            ExperimentalType.IMAGING: 0.8,
            ExperimentalType.PERTURBATION: 0.85,
            ExperimentalType.INTERVENTION: 0.7,
            ExperimentalType.COMPARATIVE: 0.65,
            ExperimentalType.LONGITUDINAL: 0.75,
            ExperimentalType.OBSERVATIONAL: 0.5,
            ExperimentalType.HIGH_THROUGHPUT: 0.9,
            ExperimentalType.BEHAVIORAL: 0.6
        }.get(protocol.experimental_type, 0.5)

        # Information from techniques
        techniques = protocol.metadata.get('techniques_used', [])
        tech_info = sum(
            0.1 for t in techniques
            if t in ['rnaseq', 'crispr', 'microscopy']
        )

        # Information from duration (longer experiments = more data)
        duration_factor = min(protocol.duration['total'] / 168, 1.0) * 0.1  # Normalize to week

        # Sample size bonus (if specified)
        sample_size = protocol.metadata.get('sample_size', 1)
        sample_bonus = min(np.log(sample_size) / 10, 0.15)

        # Hypothesis discrimination bonus
        discrimination_bonus = 0
        if hypothesis_space and len(hypothesis_space) > 1:
            discrimination_bonus = 0.1

        # Calculate total information gain
        total_gain = type_gain + tech_info + duration_factor + sample_bonus + discrimination_bonus

        return min(total_gain, 1.0)

    def _generate_alternatives(
        self,
        protocol: ExperimentalProtocol,
        n: int,
        constraints: Dict[str, Any]
    ) -> List[ExperimentalProtocol]:
        """Generate alternative experimental designs"""
        alternatives = []

        for i in range(n):
            # Create variant by modifying parameters
            variant = self._create_variant(protocol, i, constraints)
            alternatives.append(variant)

        return alternatives

    def _create_variant(
        self,
        protocol: ExperimentalProtocol,
        variant_id: int,
        constraints: Dict[str, Any]
    ) -> ExperimentalProtocol:
        """Create a variant of the protocol"""
        # Modify parameters based on variant_id
        modifications = {
            0: {'sample_size': protocol.metadata.get('sample_size', 3) * 2},
            1: {'duration_multiplier': 0.5},
            2: {'add_technique': 'microscopy'},
            3: {'sample_size': protocol.metadata.get('sample_size', 3) + 2},
            4: {'duration_multiplier': 1.5}
        }

        mod = modifications.get(variant_id % 5, {})

        # Create variant
        import copy
        variant = copy.deepcopy(protocol)
        variant.protocol_id = f"{protocol.protocol_id}_v{variant_id}"

        # Apply modifications
        if 'sample_size' in mod:
            variant.metadata['sample_size'] = mod['sample_size']

        if 'duration_multiplier' in mod:
            factor = mod['duration_multiplier']
            variant.duration = {
                k: v * factor for k, v in variant.duration.items()
            }

        if 'add_technique' in mod:
            techniques = variant.metadata.get('techniques_used', [])
            techniques.append(mod['add_technique'])
            variant.metadata['techniques_used'] = techniques

        return variant

    def _extract_design_parameters(self, protocol: ExperimentalProtocol) -> Dict[str, Any]:
        """Extract key parameters from design"""
        return {
            'experimental_type': protocol.experimental_type.value,
            'n_steps': len(protocol.steps),
            'duration_total': protocol.duration['total'],
            'n_techniques': len(protocol.metadata.get('techniques_used', [])),
            'sample_size': protocol.metadata.get('sample_size', 1)
        }

    def _perform_sensitivity_analysis(
        self,
        protocol: ExperimentalProtocol,
        hypothesis_space: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Perform sensitivity analysis on design parameters"""
        parameters = {
            'sample_size': protocol.metadata.get('sample_size', 3),
            'duration': protocol.duration['total'],
            'n_replicates': protocol.metadata.get('n_replicates', 3)
        }

        sensitivity = {}

        # Test sensitivity to each parameter
        base_gain = self._calculate_information_gain(protocol, hypothesis_space)

        for param, base_value in parameters.items():
            # Test ±20% variation
            variations = [base_value * 0.8, base_value * 1.2]
            gains = []

            for variation in variations:
                import copy
                test_protocol = copy.deepcopy(protocol)

                if param == 'sample_size':
                    test_protocol.metadata['sample_size'] = int(variation)
                elif param == 'duration':
                    factor = variation / base_value
                    test_protocol.duration = {
                        k: v * factor for k, v in test_protocol.duration.items()
                    }
                elif param == 'n_replicates':
                    test_protocol.metadata['n_replicates'] = int(variation)

                gain = self._calculate_information_gain(test_protocol, hypothesis_space)
                gains.append(gain)

            # Calculate sensitivity as change in information gain
            sensitivity[param] = {
                'base_value': base_value,
                'sensitivity': (gains[1] - gains[0]) / (0.4 * base_value),
                'variation_impact': [
                    {'value': variations[0], 'gain': gains[0]},
                    {'value': variations[1], 'gain': gains[1]}
                ]
            }

        return sensitivity


class ControlSuggester:
    """
    Suggests appropriate control experiments for biological experiments

    Ensures experimental validity through proper controls including negative,
    positive, sham, and vehicle controls.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ControlSuggester

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Control type templates
        self.control_templates = self._initialize_control_templates()

        logger.info("ControlSuggester initialized")

    def _initialize_control_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize control experiment templates"""
        return {
            'negative_control': {
                'purpose': 'Establish baseline behavior',
                'modifications': {'treatment': 'vehicle only', 'intervention': 'none'}
            },
            'positive_control': {
                'purpose': 'Verify system responds to known stimulus',
                'modifications': {'treatment': 'known_active_compound'}
            },
            'sham_control': {
                'purpose': 'Control for procedural effects',
                'modifications': {'procedure': 'all_steps_except_active_intervention'}
            },
            'vehicle_control': {
                'purpose': 'Control for solvent/excipient effects',
                'modifications': {'treatment': 'vehicle_only'}
            },
            'untreated_control': {
                'purpose': 'Establish natural baseline',
                'modifications': {'treatment': 'none'}
            },
            'dose_response_control': {
                'purpose': 'Establish dose-response relationship',
                'modifications': {'treatment': 'multiple_doses'}
            }
        }

    def suggest_controls(
        self,
        protocol: ExperimentalProtocol,
        context: Optional[Dict[str, Any]] = None
    ) -> List[ControlExperiment]:
        """
        Suggest control experiments for protocol

        Args:
            protocol: Experimental protocol
            context: Additional context

        Returns:
            List of recommended control experiments
        """
        controls = []
        exp_type = protocol.experimental_type

        # Always include negative control
        controls.append(self._create_control(
            protocol, 'negative_control', context
        ))

        # Positive control for intervention experiments
        if exp_type in [ExperimentalType.INTERVENTION, ExperimentalType.PERTURBATION]:
            controls.append(self._create_control(
                protocol, 'positive_control', context
            ))

        # Vehicle control for drug/treatment experiments
        if any(kw in protocol.hypothesis.lower() for kw in ['drug', 'treatment', 'compound']):
            controls.append(self._create_control(
                protocol, 'vehicle_control', context
            ))

        # Sham control for surgical/procedural experiments
        if any(kw in protocol.hypothesis.lower() for kw in ['inject', 'surgery', 'implant']):
            controls.append(self._create_control(
                protocol, 'sham_control', context
            ))

        # Dose-response control for dose-dependent experiments
        if 'dose' in protocol.hypothesis.lower() or 'concentration' in protocol.hypothesis.lower():
            controls.append(self._create_control(
                protocol, 'dose_response_control', context
            ))

        logger.info(f"Generated {len(controls)} control experiments")
        return controls

    def _create_control(
        self,
        protocol: ExperimentalProtocol,
        control_type: str,
        context: Optional[Dict[str, Any]]
    ) -> ControlExperiment:
        """Create a specific control experiment"""
        template = self.control_templates.get(control_type, {})

        control = ControlExperiment(
            control_id=f"{protocol.protocol_id}_{control_type}",
            name=f"{control_type.replace('_', ' ').title()}",
            description=f"Control experiment: {template.get('purpose', '')}",
            control_type=control_type,
            purpose=template.get('purpose', ''),
            modifications=template.get('modifications', {}),
            expected_result=self._predict_control_result(control_type, protocol)
        )

        return control

    def _predict_control_result(self, control_type: str, protocol: ExperimentalProtocol) -> str:
        """Predict expected result for control"""
        predictions = {
            'negative_control': 'No significant effect compared to baseline',
            'positive_control': 'Significant effect of known magnitude',
            'sham_control': 'Effect due to procedure only (no treatment effect)',
            'vehicle_control': 'Effect due to vehicle/solvent only',
            'untreated_control': 'Natural baseline behavior',
            'dose_response_control': 'Monotonic relationship between dose and response'
        }

        return predictions.get(control_type, 'Control baseline measurement')


class OutcomePredictor:
    """
    Predicts experimental outcomes under different hypotheses

    Uses mechanistic models and domain knowledge to predict likely
    experimental outcomes and their probability distributions.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize OutcomePredictor

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        logger.info("OutcomePredictor initialized")

    def _extract_hypothesis_text(self, hypothesis) -> str:
        """Extract hypothesis text from string or dict"""
        if isinstance(hypothesis, dict):
            return hypothesis.get('statement', str(hypothesis))
        return str(hypothesis)

    def predict(
        self,
        protocol: ExperimentalProtocol,
        hypotheses: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> OutcomePrediction:
        """
        Predict experimental outcomes

        Args:
            protocol: Experimental protocol
            hypotheses: Hypotheses to evaluate
            context: Additional context

        Returns:
            Outcome prediction with probabilities and confidence intervals
        """
        hypotheses = hypotheses or [protocol.hypothesis]

        # Predict outcomes for each hypothesis
        predicted_outcomes = []
        probability_distribution = {}

        for i, hypothesis in enumerate(hypotheses):
            outcome = self._predict_outcome_for_hypothesis(protocol, hypothesis)
            predicted_outcomes.append(outcome)

            # Assign probability (simplified - would use Bayesian updating)
            probability_distribution[f"hypothesis_{i+1}"] = 1.0 / len(hypotheses)

        # Calculate confidence intervals
        confidence_intervals = [
            (outcome.get('effect_size', 0) * 0.7, outcome.get('effect_size', 0) * 1.3)
            for outcome in predicted_outcomes
        ]

        # Calculate parameter sensitivity
        sensitivity_to_parameters = self._calculate_parameter_sensitivity(protocol)

        # Calculate alternative hypothesis support
        alternative_support = {
            f"hypothesis_{i+1}": prob for i, prob in enumerate(probability_distribution.values())
        }

        # Recommend measurements
        recommended_measurements = self._recommend_measurements(protocol)

        prediction = OutcomePrediction(
            predicted_outcomes=predicted_outcomes,
            confidence_intervals=confidence_intervals,
            probability_distribution=probability_distribution,
            sensitivity_to_parameters=sensitivity_to_parameters,
            alternative_hypothesis_support=alternative_support,
            recommended_measurements=recommended_measurements
        )

        logger.info(f"Generated predictions for {len(hypotheses)} hypotheses")
        return prediction

    def _predict_outcome_for_hypothesis(
        self,
        protocol: ExperimentalProtocol,
        hypothesis: str
    ) -> Dict[str, Any]:
        """Predict outcome for specific hypothesis"""
        # In full implementation, would use mechanistic models
        # For now, generate reasonable predictions

        hypothesis_text = self._extract_hypothesis_text(hypothesis)
        hypothesis_lower = hypothesis_text.lower()

        # Detect effect direction
        if any(kw in hypothesis_lower for kw in ['increase', 'enhance', 'promote', 'activate']):
            direction = 'positive'
        elif any(kw in hypothesis_lower for kw in ['decrease', 'reduce', 'inhibit', 'suppress']):
            direction = 'negative'
        else:
            direction = 'neutral'

        # Estimate effect size
        if 'strongly' in hypothesis_lower or 'significantly' in hypothesis_lower:
            effect_size = 0.8
        elif 'moderately' in hypothesis_lower or 'partial' in hypothesis_lower:
            effect_size = 0.5
        else:
            effect_size = 0.6

        # Map direction to effect size
        if direction == 'negative':
            effect_size = -effect_size
        elif direction == 'neutral':
            effect_size = 0.0

        return {
            'hypothesis': hypothesis,
            'direction': direction,
            'effect_size': effect_size,
            'p_value': 0.01,  # Predicted significance
            'power': 0.8,  # Statistical power
            'primary_readout': self._infer_primary_readout(hypothesis, protocol)
        }

    def _infer_primary_readout(self, hypothesis: str, protocol: ExperimentalProtocol) -> str:
        """Infer primary experimental readout"""
        hypothesis_text = self._extract_hypothesis_text(hypothesis)
        hypothesis_lower = hypothesis_text.lower()

        if any(kw in hypothesis_lower for kw in ['expression', 'gene', 'rna', 'transcript']):
            return 'gene_expression_level'
        elif any(kw in hypothesis_lower for kw in ['protein', 'phosphorylation', 'modification']):
            return 'protein_abundance_or_activity'
        elif any(kw in hypothesis_lower for kw in ['cell', 'growth', 'proliferation', 'death']):
            return 'cell_viability_or_proliferation'
        elif any(kw in hypothesis_lower for kw in ['localization', 'position', 'movement']):
            return 'subcellular_localization'
        else:
            return 'phenotypic_change'

    def _calculate_parameter_sensitivity(self, protocol: ExperimentalProtocol) -> Dict[str, float]:
        """Calculate sensitivity to experimental parameters"""
        return {
            'sample_size': 0.7,
            'treatment_duration': 0.5,
            'concentration': 0.8,
            'temperature': 0.3,
            'measurement_timing': 0.6
        }

    def _recommend_measurements(self, protocol: ExperimentalProtocol) -> List[str]:
        """Recommended measurements for protocol"""
        measurements = [
            'Primary outcome measurement',
            'Negative control measurement',
            'Positive control measurement (if applicable)'
        ]

        # Add protocol-specific measurements
        if protocol.experimental_type == ExperimentalType.OMICS:
            measurements.extend(['Quality control metrics', 'Normalization factors'])
        elif protocol.experimental_type == ExperimentalType.IMAGING:
            measurements.extend(['Image quality metrics', 'Blinding verification'])

        return measurements


class ExperimentalDesigner:
    """
    Main orchestrator for experimental design

    Coordinates protocol generation, information gain optimization,
    control suggestion, and outcome prediction.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ExperimentalDesigner

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Initialize components
        self.protocol_generator = ProtocolGenerator(
            self.config.get('protocol_generator', {})
        )
        self.information_gain_optimizer = InformationGainOptimizer(
            self.config.get('information_gain', {})
        )
        self.control_suggester = ControlSuggester(
            self.config.get('control_suggester', {})
        )
        self.outcome_predictor = OutcomePredictor(
            self.config.get('outcome_predictor', {})
        )

        logger.info("ExperimentalDesigner initialized")

    def _extract_hypothesis_text(self, hypothesis) -> str:
        """Extract hypothesis text from string or dict"""
        if isinstance(hypothesis, dict):
            return hypothesis.get('statement', str(hypothesis))
        return str(hypothesis)

    def design_experiment(
        self,
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None,
        optimize: bool = True,
        predict_outcomes: bool = True
    ) -> Dict[str, Any]:
        """
        Design complete experiment for hypothesis testing

        Args:
            hypothesis: Hypothesis to test
            context: Additional context and constraints
            optimize: Whether to optimize for information gain
            predict_outcomes: Whether to predict outcomes

        Returns:
            Complete experimental design
        """
        context = context or {}

        # Generate initial protocol
        protocol = self.protocol_generator.generate(
            hypothesis,
            constraints=context.get('constraints'),
            available_techniques=context.get('available_techniques')
        )

        # Optimize for information gain
        if optimize:
            optimization_result = self.information_gain_optimizer.optimize(
                protocol,
                hypothesis_space=context.get('alternative_hypotheses'),
                constraints=context.get('constraints')
            )
            optimal_protocol = optimization_result.optimal_design
            optimization_info = {
                'optimized': True,
                'information_gain': optimization_result.expected_information_gain,
                'alternatives_considered': len(optimization_result.alternative_designs),
                'sensitivity_analysis': optimization_result.sensitivity_analysis
            }
        else:
            optimal_protocol = protocol
            optimization_info = {'optimized': False}

        # Suggest controls
        controls = self.control_suggester.suggest_controls(optimal_protocol, context)
        optimal_protocol.control_experiments = controls

        # Predict outcomes
        outcome_prediction = None
        if predict_outcomes:
            outcome_prediction = self.outcome_predictor.predict(
                optimal_protocol,
                hypotheses=context.get('alternative_hypotheses'),
                context=context
            )
            optimal_protocol.predicted_observations = [
                outcome.get('primary_readout', '')
                for outcome in outcome_prediction.predicted_outcomes
            ]

        # Add validation methods
        optimal_protocol.validation_methods = self._suggest_validation_methods(
            optimal_protocol
        )

        # Identify potential confounders
        optimal_protocol.potential_confounders = self._identify_confounders(
            optimal_protocol, optimal_protocol.hypothesis
        )

        return {
            'protocol': optimal_protocol,
            'optimization': optimization_info,
            'outcome_prediction': outcome_prediction,
            'controls': controls,
            'summary': self._generate_design_summary(optimal_protocol, optimization_info)
        }

    def _suggest_validation_methods(self, protocol: ExperimentalProtocol) -> List[str]:
        """Suggest validation methods for experiment"""
        methods = ['Technical replicates', 'Biological replicates']

        if protocol.experimental_type == ExperimentalType.OMICS:
            methods.extend([
                'Independent validation by qPCR',
                'Pathway analysis validation',
                'Cross-platform validation'
            ])
        elif protocol.experimental_type == ExperimentalType.IMAGING:
            methods.extend([
                'Blinded analysis',
                'Multiple observer validation',
                'Automated segmentation validation'
            ])
        else:
            methods.extend([
                'Alternative assay validation',
                'Independent repetition'
            ])

        return methods

    def _identify_confounders(
        self,
        protocol: ExperimentalProtocol,
        hypothesis: str
    ) -> List[str]:
        """Identify potential confounding factors"""
        confounders = [
            'Batch effects',
            'Sample handling variability',
            'Environmental fluctuations'
        ]

        # Add hypothesis-specific confounders
        hypothesis_text = self._extract_hypothesis_text(hypothesis)
        hypothesis_lower = hypothesis_text.lower()

        if 'temperature' in hypothesis_lower:
            confounders.append('Temperature fluctuations')
        if 'time' in hypothesis_lower or 'temporal' in hypothesis_lower:
            confounders.append('Circadian effects')
            confounders.append('Time-of-day effects')
        if 'drug' in hypothesis_lower or 'treatment' in hypothesis_lower:
            confounders.append('Solvent effects')
            confounders.append('Drug degradation')
        if 'cell' in hypothesis_lower:
            confounders.append('Cell density effects')
            confounders.append('Passage number effects')

        return confounders

    def _generate_design_summary(
        self,
        protocol: ExperimentalProtocol,
        optimization_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate design summary"""
        return {
            'protocol_id': protocol.protocol_id,
            'experimental_type': protocol.experimental_type.value,
            'estimated_duration_hours': protocol.duration['total'],
            'estimated_cost': protocol.cost_estimate.get('total', 'unknown'),
            'expected_information_gain': optimization_info.get('information_gain', protocol.expected_information_gain),
            'n_control_experiments': len(protocol.control_experiments),
            'primary_validation_method': protocol.validation_methods[0] if protocol.validation_methods else None
        }


__all__ = [
    # Main orchestrator
    'ExperimentalDesigner',

    # Components
    'ProtocolGenerator',
    'InformationGainOptimizer',
    'ControlSuggester',
    'OutcomePredictor',

    # Data classes
    'ExperimentalProtocol',
    'ControlExperiment',
    'OptimizationResult',
    'OutcomePrediction',

    # Enums
    'ExperimentalType',
    'InformationMetric',
]
