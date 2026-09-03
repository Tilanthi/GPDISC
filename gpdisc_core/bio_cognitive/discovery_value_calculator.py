"""
Discovery Value Calculator for GPDISC Bio-Cognitive Discovery Layer

This module prioritizes research directions using information theory and
calculates expected value of discoveries to optimize resource allocation.

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import numpy as np
from scipy import optimize
from scipy.stats import entropy as scipy_entropy

logger = logging.getLogger(__name__)


class ImpactMetric(Enum):
    """Metrics for measuring scientific impact"""
    CITATION_POTENTIAL = "citation_potential"
    NOVELTY_SCORE = "novelty_score"
    TRANSLATIONAL_POTENTIAL = "translational_potential"
    TECHNOLOGY_TRANSFER_VALUE = "technology_transfer"
    KNOWLEDGE_ADVANCEMENT = "knowledge_advancement"
    FIELD_ADVANCEMENT = "field_advancement"
    INTERDISCIPLINARY_BRIDGE = "interdisciplinary_bridge"


class ResourceConstraint(Enum):
    """Types of resource constraints"""
    BUDGET = "budget"
    TIME = "time"
    PERSONNEL = "personnel"
    EQUIPMENT = "equipment"
    SAMPLES = "samples"
    COMPUTATIONAL = "computational"


@dataclass
class ResearchPriority:
    """Research direction with priority score"""
    priority_id: str
    title: str
    description: str

    # Priority metrics
    overall_priority_score: float
    information_gain_score: float
    impact_score: float
    feasibility_score: float
    resource_efficiency_score: float

    # Details
    hypotheses: List[str]
    required_resources: Dict[str, Any]
    expected_duration: Dict[str, Any]
    estimated_cost: float

    # Risk assessment
    technical_risk: float
    resource_risk: float
    timeline_risk: float

    # Value breakdown
    value_components: Dict[str, float]
    confidence_interval: Tuple[float, float]

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValueEstimate:
    """Estimated value of a research direction"""
    expected_information_gain: float
    confidence_bound: Tuple[float, float]

    # Value components
    scientific_value: float
    translational_value: float
    educational_value: float
    societal_value: float

    # Risk factors
    technical_risk: float
    market_risk: float
    regulatory_risk: float
    competitive_risk: float

    # Time value
    time_to_discovery: Dict[str, float]
    value_decay_rate: float


@dataclass
class ImpactPrediction:
    """Prediction of scientific impact"""
    predicted_impact: float
    confidence_interval: Tuple[float, float]

    # Impact dimensions
    academic_impact: float
    clinical_impact: float
    industrial_impact: float
    public_health_impact: float

    # Timeline
    time_to_peak_impact: float
    impact_duration: float
    sustained_impact_probability: float

    # Reach
    audience_size: int
    geographic_reach: str
    disciplinary_reach: List[str]


@dataclass
class ResourceAllocation:
    """Optimal resource allocation across research directions"""
    allocations: Dict[str, Dict[str, Any]]
    total_budget: float
    total_time: float

    # Efficiency metrics
    portfolio_efficiency: float
    diversification_score: float
    risk_adjusted_return: float

    # Recommendations
    funded_priorities: List[str]
    deferred_priorities: List[str]
    alternative_funding_sources: Dict[str, List[str]]


class ResearchPrioritizer:
    """
    Prioritizes research directions using multi-criteria decision analysis

    Combines information theory, impact prediction, and resource constraints
    to rank research opportunities.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ResearchPrioritizer

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Weightings for different criteria
        self.weights = self.config.get('weights', {
            'information_gain': 0.3,
            'impact': 0.3,
            'feasibility': 0.2,
            'resource_efficiency': 0.2
        })

        logger.info("ResearchPrioritizer initialized")

    def prioritize(
        self,
        research_directions: List[Dict[str, Any]],
        constraints: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> List[ResearchPriority]:
        """
        Prioritize research directions

        Args:
            research_directions: List of research directions to evaluate
            constraints: Resource and time constraints
            context: Additional context (field, lab capabilities, etc.)

        Returns:
            Ranked list of research priorities
        """
        constraints = constraints or {}
        context = context or {}

        priorities = []

        for i, direction in enumerate(research_directions):
            # Calculate component scores
            info_gain = self._calculate_information_gain_score(direction, context)
            impact = self._calculate_impact_score(direction, context)
            feasibility = self._calculate_feasibility_score(direction, constraints)
            resource_efficiency = self._calculate_resource_efficiency_score(
                direction, constraints
            )

            # Calculate overall priority
            overall = (
                self.weights['information_gain'] * info_gain +
                self.weights['impact'] * impact +
                self.weights['feasibility'] * feasibility +
                self.weights['resource_efficiency'] * resource_efficiency
            )

            # Assess risks
            technical_risk = direction.get('technical_risk', 0.3)
            resource_risk = direction.get('resource_risk', 0.2)
            timeline_risk = direction.get('timeline_risk', 0.2)

            # Create priority object
            priority = ResearchPriority(
                priority_id=f"priority_{i:04d}",
                title=direction.get('title', f'Research Direction {i+1}'),
                description=direction.get('description', ''),
                overall_priority_score=overall,
                information_gain_score=info_gain,
                impact_score=impact,
                feasibility_score=feasibility,
                resource_efficiency_score=resource_efficiency,
                hypotheses=direction.get('hypotheses', []),
                required_resources=direction.get('required_resources', {}),
                expected_duration=direction.get('expected_duration', {}),
                estimated_cost=direction.get('estimated_cost', 0),
                technical_risk=technical_risk,
                resource_risk=resource_risk,
                timeline_risk=timeline_risk,
                value_components={
                    'information_gain': info_gain,
                    'impact': impact,
                    'feasibility': feasibility,
                    'resource_efficiency': resource_efficiency
                },
                confidence_interval=(overall * 0.8, overall * 1.2),
                metadata={
                    'direction_index': i,
                    'field': context.get('field', 'unknown')
                }
            )

            priorities.append(priority)

        # Sort by overall priority
        priorities.sort(key=lambda p: p.overall_priority_score, reverse=True)

        logger.info(f"Prioritized {len(priorities)} research directions")
        return priorities

    def _calculate_information_gain_score(
        self,
        direction: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Calculate information gain potential score (0-1)"""
        # Base score from hypothesis novelty
        novelty = direction.get('novelty', 0.5)

        # Bonus for addressing knowledge gaps
        knowledge_gap_bonus = 0.2 if direction.get('addresses_gap', False) else 0.0

        # Bonus for cross-disciplinary potential
        interdisciplinary_bonus = 0.1 if direction.get('interdisciplinary', False) else 0.0

        # Penalty for incremental work
        incremental_penalty = 0.2 if direction.get('incremental', False) else 0.0

        score = novelty + knowledge_gap_bonus + interdisciplinary_bonus - incremental_penalty
        return max(0.0, min(score, 1.0))

    def _calculate_impact_score(
        self,
        direction: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Calculate impact score (0-1)"""
        impact_components = []

        # Clinical impact
        if direction.get('clinical_applications'):
            impact_components.append(0.8)

        # Technology transfer potential
        if direction.get('technology_transfer'):
            impact_components.append(0.7)

        # Field advancement
        field_advancement = direction.get('field_advancement', 0.5)
        impact_components.append(field_advancement)

        # Citation potential
        citation_potential = direction.get('citation_potential', 0.5)
        impact_components.append(citation_potential)

        return np.mean(impact_components) if impact_components else 0.5

    def _calculate_feasibility_score(
        self,
        direction: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> float:
        """Calculate feasibility score (0-1)"""
        feasibility_components = []

        # Technical feasibility
        technical = direction.get('technical_feasibility', 0.7)
        feasibility_components.append(technical)

        # Resource availability
        if constraints:
            budget_available = constraints.get('budget', float('inf'))
            budget_required = direction.get('estimated_cost', 0)
            resource_feasibility = min(1.0, budget_available / max(budget_required, 1))
            feasibility_components.append(resource_feasibility)

        # Expertise availability
        if direction.get('requires_expertise'):
            expertise_feasibility = direction.get('expertise_available', 0.5)
            feasibility_components.append(expertise_feasibility)

        # Equipment availability
        if direction.get('requires_equipment'):
            equipment_feasibility = direction.get('equipment_available', 0.5)
            feasibility_components.append(equipment_feasibility)

        return np.mean(feasibility_components) if feasibility_components else 0.5

    def _calculate_resource_efficiency_score(
        self,
        direction: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> float:
        """Calculate resource efficiency score (0-1)"""
        # Efficiency = information_gain / cost
        info_gain = self._calculate_information_gain_score(direction, {})
        cost = direction.get('estimated_cost', 1)

        if cost <= 0:
            return 0.0

        # Normalize to reasonable range
        efficiency = info_gain / np.log(cost + 1)

        # Scale to 0-1
        return min(efficiency, 1.0)


class InformationGainEstimator:
    """
    Estimates expected information gain using information theory

    Calculates Shannon entropy, KL divergence, and mutual information
    to quantify the expected knowledge advance from research.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize InformationGainEstimator

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        logger.info("InformationGainEstimator initialized")

    def estimate(
        self,
        hypotheses: List[str],
        current_knowledge: Dict[str, Any],
        planned_experiments: Optional[List[Dict[str, Any]]] = None
    ) -> float:
        """
        Estimate expected information gain

        Args:
            hypotheses: Hypotheses under consideration
            current_knowledge: Current knowledge state (priors)
            planned_experiments: Planned experiments to evaluate

        Returns:
            Expected information gain (0-1, normalized)
        """
        # Calculate prior entropy
        prior_entropy = self._calculate_prior_entropy(hypotheses, current_knowledge)

        # Calculate expected posterior entropy
        planned_experiments = planned_experiments or []
        if planned_experiments:
            posterior_entropy = self._estimate_posterior_entropy(
                hypotheses, current_knowledge, planned_experiments
            )
        else:
            # If no experiments, assume moderate reduction
            posterior_entropy = prior_entropy * 0.7

        # Information gain = reduction in entropy
        information_gain = prior_entropy - posterior_entropy

        # Normalize to 0-1
        normalized_gain = min(information_gain / prior_entropy if prior_entropy > 0 else 0, 1.0)

        return normalized_gain

    def _calculate_prior_entropy(
        self,
        hypotheses: List[str],
        current_knowledge: Dict[str, Any]
    ) -> float:
        """Calculate entropy of current hypothesis distribution"""
        # Get prior probabilities (could be uniform if unknown)
        n_hypotheses = len(hypotheses)

        if n_hypotheses == 0:
            return 0.0

        # Assume uniform priors if not specified
        priors = np.ones(n_hypotheses) / n_hypotheses

        # Calculate Shannon entropy
        return scipy_entropy(priors)

    def _estimate_posterior_entropy(
        self,
        hypotheses: List[str],
        current_knowledge: Dict[str, Any],
        experiments: List[Dict[str, Any]]
    ) -> float:
        """Estimate expected posterior entropy after experiments"""
        # For each experiment, estimate its discriminative power
        total_discrimination = 0.0

        for experiment in experiments:
            # Estimate how well experiment can discriminate hypotheses
            power = experiment.get('statistical_power', 0.8)
            discrimination = power * 0.5  # Max 50% entropy reduction per experiment
            total_discrimination += discrimination

        # Apply reduction to prior entropy
        prior_entropy = self._calculate_prior_entropy(hypotheses, current_knowledge)
        reduction_factor = max(0.0, 1.0 - total_discrimination)

        return prior_entropy * reduction_factor


class ImpactPredictor:
    """
    Predicts scientific impact of research directions

    Uses bibliometric models and impact metrics to predict potential
    scientific, clinical, and societal impact.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ImpactPredictor

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Impact weights
        self.impact_weights = self.config.get('impact_weights', {
            'academic': 0.4,
            'clinical': 0.3,
            'industrial': 0.2,
            'public_health': 0.1
        })

        logger.info("ImpactPredictor initialized")

    def predict(
        self,
        research_direction: Dict[str, Any],
        field_context: Optional[Dict[str, Any]] = None
    ) -> ImpactPrediction:
        """
        Predict impact of research direction

        Args:
            research_direction: Research direction details
            field_context: Field-specific context

        Returns:
            Impact prediction with confidence intervals
        """
        # Predict impact in each dimension
        academic_impact = self._predict_academic_impact(research_direction)
        clinical_impact = self._predict_clinical_impact(research_direction)
        industrial_impact = self._predict_industrial_impact(research_direction)
        public_health_impact = self._predict_public_health_impact(research_direction)

        # Calculate overall impact
        overall_impact = (
            self.impact_weights['academic'] * academic_impact +
            self.impact_weights['clinical'] * clinical_impact +
            self.impact_weights['industrial'] * industrial_impact +
            self.impact_weights['public_health'] * public_health_impact
        )

        # Estimate timeline
        time_to_peak = self._estimate_time_to_peak(research_direction)
        impact_duration = self._estimate_impact_duration(research_direction)
        sustained_probability = self._estimate_sustained_impact_probability(research_direction)

        # Estimate reach
        audience_size = self._estimate_audience_size(research_direction, field_context)
        geographic_reach = self._estimate_geographic_reach(research_direction)
        disciplinary_reach = self._estimate_disciplinary_reach(research_direction)

        # Calculate confidence interval (wider for more novel/uncertain work)
        uncertainty = self._calculate_impact_uncertainty(research_direction)
        confidence_interval = (
            max(0, overall_impact - uncertainty),
            min(1, overall_impact + uncertainty)
        )

        prediction = ImpactPrediction(
            predicted_impact=overall_impact,
            confidence_interval=confidence_interval,
            academic_impact=academic_impact,
            clinical_impact=clinical_impact,
            industrial_impact=industrial_impact,
            public_health_impact=public_health_impact,
            time_to_peak_impact=time_to_peak,
            impact_duration=impact_duration,
            sustained_impact_probability=sustained_probability,
            audience_size=audience_size,
            geographic_reach=geographic_reach,
            disciplinary_reach=disciplinary_reach
        )

        logger.info(f"Generated impact prediction: {overall_impact:.3f}")
        return prediction

    def _predict_academic_impact(self, direction: Dict[str, Any]) -> float:
        """Predict academic impact (citations, knowledge advancement)"""
        impact = 0.5  # Base impact

        # Novelty bonus
        if direction.get('novel', False):
            impact += 0.2

        # Field advancement bonus
        field_advancement = direction.get('field_advancement', 0)
        impact += field_advancement * 0.2

        # Multi-disciplinary bonus
        if direction.get('interdisciplinary', False):
            impact += 0.1

        return min(impact, 1.0)

    def _predict_clinical_impact(self, direction: Dict[str, Any]) -> float:
        """Predict clinical impact"""
        if not direction.get('clinical_applications'):
            return 0.0

        impact = 0.3  # Base for having clinical applications

        # Stage of research
        stage = direction.get('research_stage', 'basic')
        if stage == 'clinical_trial':
            impact += 0.4
        elif stage == 'preclinical':
            impact += 0.2
        elif stage == 'translational':
            impact += 0.3

        # Disease burden
        disease_burden = direction.get('disease_burden', 0)
        impact += disease_burden * 0.2

        return min(impact, 1.0)

    def _predict_industrial_impact(self, direction: Dict[str, Any]) -> float:
        """Predict industrial/commercial impact"""
        if not direction.get('technology_transfer'):
            return 0.0

        impact = 0.3  # Base for having transfer potential

        # Market size
        market_size = direction.get('market_size', 0)
        impact += market_size * 0.3

        # IP potential
        if direction.get('patentable', False):
            impact += 0.2

        return min(impact, 1.0)

    def _predict_public_health_impact(self, direction: Dict[str, Any]) -> float:
        """Predict public health impact"""
        impact = 0.0

        # Population affected
        population = direction.get('population_affected', 0)
        if population > 1e6:  # > 1 million
            impact += 0.3
        elif population > 1e5:  # > 100k
            impact += 0.2

        # Prevention vs treatment
        if direction.get('prevention_focused', False):
            impact += 0.2

        # Health disparity reduction
        if direction.get('addresses_disparities', False):
            impact += 0.2

        return min(impact, 1.0)

    def _estimate_time_to_peak(self, direction: Dict[str, Any]) -> float:
        """Estimate years to peak impact"""
        # Basic research takes longer
        if direction.get('research_stage') == 'basic':
            return 5.0
        elif direction.get('research_stage') == 'translational':
            return 3.0
        else:
            return 2.0

    def _estimate_impact_duration(self, direction: Dict[str, Any]) -> float:
        """Estimate duration of significant impact (years)"""
        # Foundational work has longer impact
        if direction.get('foundational', False):
            return 20.0
        elif direction.get('novel', False):
            return 10.0
        else:
            return 5.0

    def _estimate_sustained_impact_probability(self, direction: Dict[str, Any]) -> float:
        """Estimate probability of sustained impact"""
        base_prob = 0.5

        if direction.get('foundational', False):
            base_prob += 0.2

        if direction.get('interdisciplinary', False):
            base_prob += 0.1

        return min(base_prob, 1.0)

    def _estimate_audience_size(self, direction: Dict[str, Any], context: Dict[str, Any]) -> int:
        """Estimate audience size (researchers, clinicians, etc.)"""
        field_size = context.get('field_size', 10000) if context else 10000

        # Multipliers based on reach
        multiplier = 1.0
        if direction.get('interdisciplinary', False):
            multiplier *= 3

        if direction.get('clinical_applications'):
            multiplier *= 5

        return int(field_size * multiplier)

    def _estimate_geographic_reach(self, direction: Dict[str, Any]) -> str:
        """Estimate geographic reach"""
        if direction.get('global_health', False):
            return "global"
        elif direction.get('clinical_applications'):
            return "international"
        else:
            return "national"

    def _estimate_disciplinary_reach(self, direction: Dict[str, Any]) -> List[str]:
        """Estimate disciplinary reach"""
        base_discipline = direction.get('discipline', 'biology')
        reach = [base_discipline]

        if direction.get('interdisciplinary', False):
            reach.extend(['medicine', 'bioengineering'])

        if direction.get('computational', False):
            reach.append('computer_science')

        return list(set(reach))

    def _calculate_impact_uncertainty(self, direction: Dict[str, Any]) -> float:
        """Calculate uncertainty in impact prediction"""
        base_uncertainty = 0.2

        # Novel work is more uncertain
        if direction.get('novel', False):
            base_uncertainty += 0.1

        # Early stage is more uncertain
        if direction.get('research_stage') == 'basic':
            base_uncertainty += 0.1

        return min(base_uncertainty, 0.5)


class ResourceOptimizer:
    """
    Optimizes resource allocation across research directions

    Uses portfolio optimization and multi-objective optimization to
    allocate resources for maximum expected value.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ResourceOptimizer

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        logger.info("ResourceOptimizer initialized")

    def optimize(
        self,
        priorities: List[ResearchPriority],
        total_budget: float,
        total_time: float,
        constraints: Optional[Dict[str, Any]] = None
    ) -> ResourceAllocation:
        """
        Optimize resource allocation across priorities

        Args:
            priorities: Ranked research priorities
            total_budget: Total available budget
            total_time: Total available time (years)
            constraints: Additional constraints

        Returns:
            Optimal resource allocation
        """
        constraints = constraints or {}

        # Filter to feasible priorities
        feasible = [
            p for p in priorities
            if p.estimated_cost <= total_budget and
               p.expected_duration.get('total', 0) <= total_time
        ]

        # Solve knapsack-like optimization
        result = self._solve_allocation_problem(
            feasible, total_budget, total_time, constraints
        )

        # Calculate portfolio metrics
        funded_priority_ids = [p.priority_id for p in result['funded']]
        deferred_priority_ids = [p.priority_id for p in result['deferred']]

        portfolio_efficiency = self._calculate_portfolio_efficiency(result['funded'])
        diversification_score = self._calculate_diversification(result['funded'])
        risk_adjusted_return = self._calculate_risk_adjusted_return(result['funded'])

        # Build allocations dict
        allocations = {}
        for priority, allocation in zip(result['funded'], result['allocations']):
            allocations[priority.priority_id] = {
                'budget': allocation['budget'],
                'time': allocation['time'],
                'priority': priority
            }

        # Identify alternative funding sources for deferred priorities
        alternative_sources = self._identify_alternative_funding(result['deferred'])

        allocation = ResourceAllocation(
            allocations=allocations,
            total_budget=sum(a['budget'] for a in allocations.values()),
            total_time=sum(a['time'] for a in allocations.values()),
            portfolio_efficiency=portfolio_efficiency,
            diversification_score=diversification_score,
            risk_adjusted_return=risk_adjusted_return,
            funded_priorities=funded_priority_ids,
            deferred_priorities=deferred_priority_ids,
            alternative_funding_sources=alternative_sources
        )

        logger.info(f"Optimized allocation: {len(funded_priority_ids)} funded, "
                   f"{len(deferred_priority_ids)} deferred")
        return allocation

    def _solve_allocation_problem(
        self,
        priorities: List[ResearchPriority],
        total_budget: float,
        total_time: float,
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Solve resource allocation optimization problem"""
        # Use greedy algorithm with priority scoring
        # (Could use MILP for exact solution)

        sorted_priorities = sorted(priorities, key=lambda p: p.overall_priority_score, reverse=True)

        funded = []
        deferred = []
        allocations = []

        remaining_budget = total_budget
        remaining_time = total_time

        for priority in sorted_priorities:
            cost = priority.estimated_cost
            time = priority.expected_duration.get('total', 1)

            if cost <= remaining_budget and time <= remaining_time:
                # Can fund this priority
                funded.append(priority)
                allocations.append({'budget': cost, 'time': time})
                remaining_budget -= cost
                remaining_time -= time
            else:
                # Defer this priority
                deferred.append(priority)

        return {
            'funded': funded,
            'deferred': deferred,
            'allocations': allocations
        }

    def _calculate_portfolio_efficiency(self, funded: List[ResearchPriority]) -> float:
        """Calculate portfolio efficiency (value per unit cost)"""
        if not funded:
            return 0.0

        total_value = sum(p.overall_priority_score for p in funded)
        total_cost = sum(p.estimated_cost for p in funded)

        if total_cost == 0:
            return 0.0

        return total_value / total_cost

    def _calculate_diversification(self, funded: List[ResearchPriority]) -> float:
        """Calculate diversification score"""
        if not funded:
            return 0.0

        # Count distinct fields/topics
        fields = set()
        for priority in funded:
            field = priority.metadata.get('field', 'unknown')
            fields.add(field)

        # Diversity = unique fields / total priorities
        return len(fields) / len(funded)

    def _calculate_risk_adjusted_return(self, funded: List[ResearchPriority]) -> float:
        """Calculate risk-adjusted expected return"""
        if not funded:
            return 0.0

        total_score = 0.0
        total_weight = 0.0

        for priority in funded:
            # Risk = average of all risk scores
            risk = (
                priority.technical_risk +
                priority.resource_risk +
                priority.timeline_risk
            ) / 3.0

            # Weight = 1 - risk (higher risk = lower weight)
            weight = 1.0 - risk

            total_score += priority.overall_priority_score * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_score / total_weight

    def _identify_alternative_funding(self, deferred: List[ResearchPriority]) -> Dict[str, List[str]]:
        """Identify alternative funding sources for deferred priorities"""
        sources = {
            'nih_grants': ['R01', 'R21', 'R03'],
            'nsf_grants': ['CAREER', 'Standard Grant'],
            'private_foundations': ['Howard Hughes', 'Gates Foundation', 'Chan Zuckerberg'],
            'industry_partnerships': ['Biotech', 'Pharma'],
            'crowdfunding': ['Experiment.com', 'GoFundMe']
        }

        alternative_sources = {}
        for priority in deferred:
            # Assign relevant sources based on priority characteristics
            relevant = ['nih_grants', 'nsf_grants']  # Most can apply to these

            if priority.metadata.get('translational_potential'):
                relevant.append('private_foundations')

            if priority.metadata.get('commercial_potential'):
                relevant.append('industry_partnerships')

            alternative_sources[priority.priority_id] = [
                source for source in relevant if source in sources
            ]

        return alternative_sources


class DiscoveryValueCalculator:
    """
    Main orchestrator for discovery value calculation

    Coordinates research prioritization, information gain estimation,
    impact prediction, and resource optimization.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DiscoveryValueCalculator

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Initialize components
        self.research_prioritizer = ResearchPrioritizer(
            self.config.get('prioritizer', {})
        )
        self.information_gain_estimator = InformationGainEstimator(
            self.config.get('information_gain', {})
        )
        self.impact_predictor = ImpactPredictor(
            self.config.get('impact_predictor', {})
        )
        self.resource_optimizer = ResourceOptimizer(
            self.config.get('resource_optimizer', {})
        )

        logger.info("DiscoveryValueCalculator initialized")

    def prioritize_research(
        self,
        query: str,
        discovery_results: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Prioritize research directions based on discovery results

        Args:
            query: Original scientific query
            discovery_results: Results from BCDL discovery process
            context: Additional context (constraints, lab capabilities, etc.)

        Returns:
            Prioritized list of research directions
        """
        context = context or {}

        # Extract research directions from discovery results
        research_directions = self._extract_research_directions(
            query, discovery_results
        )

        # Prioritize directions
        priorities = self.research_prioritizer.prioritize(
            research_directions,
            constraints=context.get('constraints'),
            context=context
        )

        # Add value estimates and impact predictions
        enriched_priorities = []
        for priority in priorities[:10]:  # Top 10
            # Estimate value
            value_estimate = self._estimate_value(priority, discovery_results, context)

            # Predict impact
            impact_prediction = self.impact_predictor.predict(
                self._priority_to_dict(priority),
                context.get('field_context')
            )

            enriched_priority = {
                'priority': priority,
                'value_estimate': value_estimate,
                'impact_prediction': impact_prediction,
                'summary': self._generate_priority_summary(priority, value_estimate, impact_prediction)
            }

            enriched_priorities.append(enriched_priority)

        # Optimize resource allocation if constraints provided
        if context.get('constraints'):
            allocation = self.resource_optimizer.optimize(
                priorities,
                total_budget=context['constraints'].get('budget', 1e6),
                total_time=context['constraints'].get('time', 1.0),
                constraints=context.get('constraints')
            )

            return {
                'priorities': enriched_priorities,
                'resource_allocation': allocation,
                'query': query,
                'total_directions_evaluated': len(research_directions)
            }

        return {
            'priorities': enriched_priorities,
            'query': query,
            'total_directions_evaluated': len(research_directions)
        }

    def _extract_research_directions(
        self,
        query: str,
        discovery_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract research directions from discovery results"""
        directions = []

        # Extract from hypotheses
        hypotheses = discovery_results.get('hypotheses', [])
        for i, hypothesis in enumerate(hypotheses):
            if isinstance(hypothesis, dict):
                direction = {
                    'title': f"Test hypothesis: {hypothesis.get('statement', 'Unknown')[:80]}",
                    'description': hypothesis.get('reasoning', ''),
                    'hypotheses': [hypothesis.get('statement', '')],
                    'novelty': hypothesis.get('novelty_score', 0.5),
                    'interdisciplinary': hypothesis.get('cross_domain', False),
                    'estimated_cost': 50000,
                    'expected_duration': {'total': 1.0},
                    'required_resources': {},
                    'technical_feasibility': 0.7
                }
            else:
                direction = {
                    'title': f"Test hypothesis {i+1}",
                    'description': str(hypothesis)[:200],
                    'hypotheses': [str(hypothesis)],
                    'novelty': 0.5,
                    'estimated_cost': 50000,
                    'expected_duration': {'total': 1.0},
                    'technical_feasibility': 0.7
                }
            directions.append(direction)

        # Extract from multi-scale insights
        multi_scale_insights = discovery_results.get('multi_scale_insights', [])
        for insight in multi_scale_insights:
            if isinstance(insight, dict) and insight.get('emergent_properties'):
                direction = {
                    'title': f"Investigate emergent property at {insight.get('scale', 'multiple')} scale",
                    'description': insight.get('description', ''),
                    'hypotheses': [insight.get('hypothesis', '')],
                    'novelty': 0.7,
                    'interdisciplinary': True,
                    'estimated_cost': 75000,
                    'expected_duration': {'total': 1.5},
                    'technical_feasibility': 0.6
                }
                directions.append(direction)

        return directions

    def _estimate_value(
        self,
        priority: ResearchPriority,
        discovery_results: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ValueEstimate:
        """Estimate value of research priority"""
        # Estimate information gain
        hypotheses = priority.hypotheses or [priority.description]
        current_knowledge = context.get('current_knowledge', {})

        expected_gain = self.information_gain_estimator.estimate(
            hypotheses, current_knowledge
        )

        # Calculate value components
        scientific_value = priority.information_gain_score * 0.4 + priority.impact_score * 0.3
        translational_value = priority.impact_score * 0.3
        educational_value = priority.information_gain_score * 0.2
        societal_value = priority.impact_score * 0.2

        # Risk factors
        technical_risk = priority.technical_risk
        market_risk = 0.3 if context.get('translational_focus') else 0.1
        regulatory_risk = 0.4 if context.get('clinical_applications') else 0.0
        competitive_risk = 0.2

        # Time value
        time_to_discovery = {
            'optimistic': priority.expected_duration.get('total', 1) * 0.7,
            'expected': priority.expected_duration.get('total', 1),
            'pessimistic': priority.expected_duration.get('total', 1) * 1.5
        }

        value_decay = 0.05  # 5% per year value decay

        return ValueEstimate(
            expected_information_gain=expected_gain,
            confidence_bound=(expected_gain * 0.8, expected_gain * 1.2),
            scientific_value=scientific_value,
            translational_value=translational_value,
            educational_value=educational_value,
            societal_value=societal_value,
            technical_risk=technical_risk,
            market_risk=market_risk,
            regulatory_risk=regulatory_risk,
            competitive_risk=competitive_risk,
            time_to_discovery=time_to_discovery,
            value_decay_rate=value_decay
        )

    def _priority_to_dict(self, priority: ResearchPriority) -> Dict[str, Any]:
        """Convert priority to dict for impact predictor"""
        return {
            'title': priority.title,
            'description': priority.description,
            'novel': priority.information_gain_score > 0.7,
            'interdisciplinary': any('cross' in str(priority.metadata).lower() for _ in [True]),
            'clinical_applications': 'clinical' in priority.description.lower(),
            'technology_transfer': 'technology' in priority.description.lower(),
            'field_advancement': priority.impact_score,
            'research_stage': 'basic',
            'discipline': priority.metadata.get('field', 'biology')
        }

    def _generate_priority_summary(
        self,
        priority: ResearchPriority,
        value_estimate: ValueEstimate,
        impact_prediction: ImpactPrediction
    ) -> Dict[str, Any]:
        """Generate priority summary"""
        return {
            'priority_id': priority.priority_id,
            'title': priority.title,
            'overall_score': priority.overall_priority_score,
            'expected_information_gain': value_estimate.expected_information_gain,
            'predicted_impact': impact_prediction.predicted_impact,
            'estimated_cost': priority.estimated_cost,
            'risk_level': (priority.technical_risk + priority.resource_risk + priority.timeline_risk) / 3,
            'recommendation': self._generate_recommendation(priority, value_estimate, impact_prediction)
        }

    def _generate_recommendation(
        self,
        priority: ResearchPriority,
        value_estimate: ValueEstimate,
        impact_prediction: ImpactPrediction
    ) -> str:
        """Generate funding recommendation"""
        score = priority.overall_priority_score
        risk = (priority.technical_risk + priority.resource_risk + priority.timeline_risk) / 3

        if score > 0.8 and risk < 0.3:
            return "HIGHLY RECOMMENDED - High value, low risk"
        elif score > 0.7:
            return "RECOMMENDED - Strong potential"
        elif score > 0.5 and risk < 0.4:
            return "CONSIDER - Moderate potential, acceptable risk"
        elif risk > 0.6:
            return "HIGH RISK - Consider only if high strategic value"
        else:
            return "DEFER - Lower priority or pursue alternative funding"


__all__ = [
    # Main orchestrator
    'DiscoveryValueCalculator',

    # Components
    'ResearchPrioritizer',
    'InformationGainEstimator',
    'ImpactPredictor',
    'ResourceOptimizer',

    # Data classes
    'ResearchPriority',
    'ValueEstimate',
    'ImpactPrediction',
    'ResourceAllocation',

    # Enums
    'ImpactMetric',
    'ResourceConstraint',
]
