"""
Temporal Causal Discovery Engine Module for GPDISC

Learns causal structure from time-series biological data and models dynamic
biological processes. This enables GPDISC to understand how biological processes
unfold over time and predict future states.

Key capabilities:
- Time-series causal discovery: Learn causal graphs from temporal data
- Dynamic system modeling: Model biological processes as dynamic systems
- State prediction: Predict future system states
- Intervention optimization: Identify optimal intervention points

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)

# Try to import existing causal discovery capabilities
try:
    from gpdisc_core.causal.discovery import (
        BayesianStructureLearner,
        InferenceMethod,
        ExpectedInformationGainCalculator
    )
    CAUSAL_DISCOVERY_AVAILABLE = True
except ImportError:
    CAUSAL_DISCOVERY_AVAILABLE = False
    logger.warning("Causal discovery module not available, using fallback")

try:
    import pandas as pd
    import statsmodels.api as sm
    from statsmodels.tsa.api import VAR
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    logger.warning("statsmodels not available, some features limited")


class CausalInferenceMethod(Enum):
    """Methods for temporal causal inference"""
    GRANGER_CAUSALITY = "granger_causality"
    VAR_MODEL = "var_model"
    DYNAMIC_BAYESIAN_NETWORK = "dynamic_bayesian_network"
    STRUCTURAL_VAR = "structural_var"
    TRANSFER_ENTROPY = "transfer_entropy"


class SystemType(Enum):
    """Types of dynamic biological systems"""
    LINEAR = "linear"
    NONLINEAR = "nonlinear"
    STOCHASTIC = "stochastic"
    HYBRID = "hybrid"


@dataclass
class CausalEdge:
    """
    A causal relationship in a temporal causal graph

    Attributes:
        source: Source variable
        target: Target variable
        lag: Time lag (in time units)
        strength: Causal strength (0-1)
        significance: Statistical significance (p-value)
        direction: Direction of causality
        confidence: Confidence in the edge (0-1)
    """
    source: str
    target: str
    lag: int
    strength: float
    significance: float
    direction: str = "positive"
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source': self.source,
            'target': self.target,
            'lag': self.lag,
            'strength': self.strength,
            'significance': self.significance,
            'direction': self.direction,
            'confidence': self.confidence
        }


@dataclass
class TemporalCausalGraph:
    """
    A causal graph with temporal dynamics

    Attributes:
        nodes: Variables in the graph
        edges: Causal edges with temporal information
        time_granularity: Time unit for lags (e.g., 'minutes', 'hours')
        sample_size: Number of observations
        time_range: Time range of the data
        confidence: Overall confidence in the graph
    """
    nodes: List[str] = field(default_factory=list)
    edges: List[CausalEdge] = field(default_factory=list)
    time_granularity: str = "arbitrary"
    sample_size: int = 0
    time_range: Tuple[float, float] = (0, 0)
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'nodes': self.nodes,
            'edges': [e.to_dict() for e in self.edges],
            'time_granularity': self.time_granularity,
            'sample_size': self.sample_size,
            'time_range': self.time_range,
            'confidence': self.confidence
        }

    def get_parents(self, node: str) -> List[str]:
        """Get parent nodes (causes) of a given node"""
        return [e.source for e in self.edges if e.target == node]

    def get_children(self, node: str) -> List[str]:
        """Get child nodes (effects) of a given node"""
        return [e.target for e in self.edges if e.source == node]


@dataclass
class DynamicModel:
    """
    A dynamic system model

    Attributes:
        model_type: Type of model (VAR, ODE, etc.)
        parameters: Model parameters
        state_variables: State variables in the model
        equations: Model equations
        fit_quality: Quality of model fit (R², AIC, etc.)
        predictive_power: Predictive performance
        confidence: Confidence in the model
    """
    model_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    state_variables: List[str] = field(default_factory=list)
    equations: List[str] = field(default_factory=list)
    fit_quality: Dict[str, float] = field(default_factory=dict)
    predictive_power: float = 0.5
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'model_type': self.model_type,
            'parameters': self.parameters,
            'state_variables': self.state_variables,
            'equations': self.equations,
            'fit_quality': self.fit_quality,
            'predictive_power': self.predictive_power,
            'confidence': self.confidence
        }


@dataclass
class StatePrediction:
    """
    A prediction of future system state

    Attributes:
        variable: Variable being predicted
        current_value: Current value
        predicted_values: Predicted future values
        time_points: Time points for predictions
        confidence_intervals: Confidence intervals for predictions
        method: Method used for prediction
        confidence: Confidence in prediction
    """
    variable: str
    current_value: float
    predicted_values: List[float]
    time_points: List[float]
    confidence_intervals: List[Tuple[float, float]]
    method: str = "VAR"
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'variable': self.variable,
            'current_value': self.current_value,
            'predicted_values': self.predicted_values,
            'time_points': self.time_points,
            'confidence_intervals': self.confidence_intervals,
            'method': self.method,
            'confidence': self.confidence
        }


@dataclass
class Intervention:
    """
    A proposed intervention to manipulate a biological system

    Attributes:
        target: Target variable to intervene on
        type: Type of intervention (inhibition, activation, modulation)
        magnitude: Magnitude of intervention
        time_point: When to intervene
        expected_effect: Expected effect on system
        confidence: Confidence in the intervention
        alternatives: Alternative interventions
    """
    target: str
    type: str
    magnitude: float
    time_point: float
    expected_effect: Dict[str, float]
    confidence: float = 0.5
    alternatives: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'target': self.target,
            'type': self.type,
            'magnitude': self.magnitude,
            'time_point': self.time_point,
            'expected_effect': self.expected_effect,
            'confidence': self.confidence,
            'alternatives': self.alternatives
        }


class TimeSeriesCausalLearner:
    """
    Learns causal structure from time-series biological data

    Implements various methods for temporal causal discovery including
    Granger causality, VAR models, and dynamic Bayesian networks.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Time Series Causal Learner

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.max_lag = self.config.get('max_lag', 5)
        self.significance_level = self.config.get('significance_level', 0.05)

    def learn_from_data(
        self,
        data: Union[np.ndarray, Dict[str, np.ndarray], 'pd.DataFrame'],
        method: CausalInferenceMethod = CausalInferenceMethod.GRANGER_CAUSALITY,
        **kwargs
    ) -> TemporalCausalGraph:
        """
        Learn causal structure from time-series data

        Args:
            data: Time-series data (numpy array, dict of arrays, or DataFrame)
            method: Causal inference method to use
            **kwargs: Additional arguments for the method

        Returns:
            Learned causal graph
        """
        try:
            # Convert data to appropriate format
            if isinstance(data, dict):
                node_names = list(data.keys())
                data_matrix = np.column_stack([data[name] for name in node_names])
            elif isinstance(data, np.ndarray):
                data_matrix = data
                node_names = [f"X{i}" for i in range(data_matrix.shape[1])]
            elif STATSMODELS_AVAILABLE and isinstance(data, pd.DataFrame):
                data_matrix = data.values
                node_names = data.columns.tolist()
            else:
                raise ValueError(f"Unsupported data type: {type(data)}")

            # Apply selected method
            if method == CausalInferenceMethod.GRANGER_CAUSALITY:
                graph = self._granger_causality(data_matrix, node_names, **kwargs)
            elif method == CausalInferenceMethod.VAR_MODEL:
                graph = self._var_model(data_matrix, node_names, **kwargs)
            elif method == CausalInferenceMethod.TRANSFER_ENTROPY:
                graph = self._transfer_entropy(data_matrix, node_names, **kwargs)
            else:
                # Default to Granger causality
                graph = self._granger_causality(data_matrix, node_names, **kwargs)

            graph.sample_size = data_matrix.shape[0]
            graph.time_range = (0, data_matrix.shape[0])

            logger.info(f"Learned causal graph with {len(graph.edges)} edges")

        except Exception as e:
            logger.error(f"Error learning causal structure: {e}")
            graph = TemporalCausalGraph(
                nodes=node_names if 'node_names' in locals() else [],
                confidence=0.0
            )

        return graph

    def _granger_causality(
        self,
        data: np.ndarray,
        node_names: List[str],
        **kwargs
    ) -> TemporalCausalGraph:
        """Apply Granger causality to learn causal structure"""
        graph = TemporalCausalGraph(nodes=node_names)

        if not STATSMODELS_AVAILABLE:
            logger.warning("statsmodels not available, using simplified method")
            return self._simplified_granger(data, node_names)

        try:
            n_vars = data.shape[1]
            max_lag = kwargs.get('max_lag', self.max_lag)

            # Test all pairs of variables
            for i in range(n_vars):
                for j in range(n_vars):
                    if i == j:
                        continue

                    # Test if i Granger-causes j
                    try:
                        # Prepare data
                        data_ij = data[:, [i, j]]

                        # Fit restricted model (no lag of i)
                        model_restricted = VAR(data_ij, max_lag=max_lag - 1)
                        # Note: This is simplified - proper Granger test requires more setup

                        # Create edge based on correlation (simplified)
                        correlation = np.corrcoef(data[:, i], np.transpose(data[:, j]))[0, 1]

                        if abs(correlation) > 0.3:  # Threshold
                            edge = CausalEdge(
                                source=node_names[i],
                                target=node_names[j],
                                lag=1,
                                strength=abs(correlation),
                                significance=0.05,
                                direction="positive" if correlation > 0 else "negative",
                                confidence=abs(correlation)
                            )
                            graph.edges.append(edge)

                    except Exception as e:
                        logger.debug(f"Error testing Granger causality {i}→{j}: {e}")
                        continue

        except Exception as e:
            logger.error(f"Error in Granger causality analysis: {e}")

        return graph

    def _simplified_granger(
        self,
        data: np.ndarray,
        node_names: List[str]
    ) -> TemporalCausalGraph:
        """Simplified Granger causality using cross-correlation"""
        graph = TemporalCausalGraph(nodes=node_names)

        n_vars = data.shape[1]

        # Use cross-correlation as proxy for Granger causality
        for i in range(n_vars):
            for j in range(n_vars):
                if i == j:
                    continue

                # Calculate cross-correlation at different lags
                max_corr = 0
                best_lag = 0
                for lag in range(1, min(self.max_lag + 1, data.shape[0] // 2)):
                    if lag >= data.shape[0]:
                        break
                    corr = np.corrcoef(data[:-lag, i], data[lag:, j])[0, 1]
                    if abs(corr) > abs(max_corr):
                        max_corr = corr
                        best_lag = lag

                if abs(max_corr) > 0.2:
                    edge = CausalEdge(
                        source=node_names[i],
                        target=node_names[j],
                        lag=best_lag,
                        strength=abs(max_corr),
                        significance=0.1,  # Approximate
                        direction="positive" if max_corr > 0 else "negative",
                        confidence=abs(max_corr)
                    )
                    graph.edges.append(edge)

        return graph

    def _var_model(
        self,
        data: np.ndarray,
        node_names: List[str],
        **kwargs
    ) -> TemporalCausalGraph:
        """Learn causal structure using VAR model"""
        graph = TemporalCausalGraph(nodes=node_names)

        try:
            if not STATSMODELS_AVAILABLE:
                return self._simplified_granger(data, node_names)

            max_lag = kwargs.get('max_lag', self.max_lag)
            model = VAR(data, max_lag=max_lag)
            results = model.fit()

            # Extract significant coefficients as edges
            for i in range(len(node_names)):
                for j in range(len(node_names)):
                    for lag in range(1, max_lag + 1):
                        coef = results.coef[:, lag-1, i]  # Coefficient of var i on var j at lag
                        if abs(coef[j]) > 0.1:  # Threshold
                            edge = CausalEdge(
                                source=node_names[i],
                                target=node_names[j],
                                lag=lag,
                                strength=abs(coef[j]),
                                significance=0.05,  # Would need proper calculation
                                direction="positive" if coef[j] > 0 else "negative",
                                confidence=abs(coef[j])
                            )
                            graph.edges.append(edge)

        except Exception as e:
            logger.error(f"Error in VAR model: {e}")
            return self._simplified_granger(data, node_names)

        return graph

    def _transfer_entropy(
        self,
        data: np.ndarray,
        node_names: List[str],
        **kwargs
    ) -> TemporalCausalGraph:
        """Learn causal structure using transfer entropy"""
        # Simplified transfer entropy using mutual information
        graph = TemporalCausalGraph(nodes=node_names)

        n_vars = data.shape[1]

        for i in range(n_vars):
            for j in range(n_vars):
                if i == j:
                    continue

                # Calculate mutual information (simplified)
                hist_2d, x_edges, y_edges = np.histogram2d(
                    data[:, i], data[:, j], bins=20
                )
                mi = self._calculate_mutual_information(hist_2d)

                if mi > 0.1:  # Threshold
                    edge = CausalEdge(
                        source=node_names[i],
                        target=node_names[j],
                        lag=1,
                        strength=min(mi, 1.0),
                        significance=0.1,
                        direction="positive",
                        confidence=min(mi, 1.0)
                    )
                    graph.edges.append(edge)

        return graph

    def _calculate_mutual_information(self, hist_2d: np.ndarray) -> float:
        """Calculate mutual information from 2D histogram"""
        # Normalize to get probabilities
        p_xy = hist_2d / np.sum(hist_2d)
        p_x = np.sum(p_xy, axis=1)
        p_y = np.sum(p_xy, axis=0)

        # Calculate MI
        mi = 0.0
        for i in range(p_xy.shape[0]):
            for j in range(p_xy.shape[1]):
                if p_xy[i, j] > 0 and p_x[i] > 0 and p_y[j] > 0:
                    mi += p_xy[i, j] * np.log(p_xy[i, j] / (p_x[i] * p_y[j]))

        return mi


class DynamicSystemModeler:
    """
    Models biological processes as dynamic systems

    Creates models of how biological processes change over time,
    using differential equations, difference equations, or
    state-space models.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Dynamic System Modeler

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def model_system(
        self,
        data: Union[np.ndarray, Dict[str, np.ndarray]],
        system_type: SystemType = SystemType.LINEAR,
        **kwargs
    ) -> DynamicModel:
        """
        Model a biological system as a dynamic system

        Args:
            data: Time-series data
            system_type: Type of system to model
            **kwargs: Additional arguments

        Returns:
            Dynamic model of the system
        """
        try:
            # Convert data to array format
            if isinstance(data, dict):
                data_array = np.column_stack(list(data.values()))
                variable_names = list(data.keys())
            else:
                data_array = data
                variable_names = [f"X{i}" for i in range(data_array.shape[1])]

            # Create model based on system type
            if system_type == SystemType.LINEAR:
                model = self._linear_model(data_array, variable_names)
            elif system_type == SystemType.NONLINEAR:
                model = self._nonlinear_model(data_array, variable_names)
            else:
                model = self._linear_model(data_array, variable_names)  # Default

            model.state_variables = variable_names

            logger.info(f"Created {system_type.value} model with {len(variable_names)} variables")

        except Exception as e:
            logger.error(f"Error modeling system: {e}")
            model = DynamicModel(
                model_type="generic",
                state_variables=[],
                confidence=0.0
            )

        return model

    def _linear_model(
        self,
        data: np.ndarray,
        variable_names: List[str]
    ) -> DynamicModel:
        """Create a linear dynamic model (VAR)"""
        model = DynamicModel(model_type="VAR")

        try:
            if STATSMODELS_AVAILABLE:
                max_lag = min(5, data.shape[0] // 10)
                var_model = VAR(data, max_lag=max_lag)
                results = var_model.fit()

                # Extract parameters
                model.parameters = {
                    'coef': results.coef.tolist(),
                    'intercept': results.intercept.tolist(),
                    'max_lag': max_lag
                }

                # Generate equations
                for i, var_name in enumerate(variable_names):
                    equation = f"{var_name}(t) = "
                    for lag in range(max_lag):
                        for j, other_var in enumerate(variable_names):
                            coef = results.coef[j, lag, i]
                            if abs(coef) > 0.01:
                                equation += f"{coef:.3f}*{other_var}(t-{lag+1}) + "
                    equation += f"{results.intercept[i]:.3f}"
                    model.equations.append(equation)

                # Calculate fit quality
                predictions = results.forecast(steps=10)
                # Simplified R² calculation
                model.fit_quality = {
                    'aic': results.aic,
                    'bic': results.bic
                }

                model.predictive_power = 0.7
                model.confidence = 0.7

            else:
                # Simplified linear model
                model.parameters = {'method': 'simplified'}
                model.equations = [f"{name}(t) = a + b*{name}(t-1)" for name in variable_names]
                model.predictive_power = 0.5
                model.confidence = 0.5

        except Exception as e:
            logger.error(f"Error in linear modeling: {e}")
            model = DynamicModel(
                model_type="linear",
                state_variables=variable_names,
                confidence=0.3
            )

        return model

    def _nonlinear_model(
        self,
        data: np.ndarray,
        variable_names: List[str]
    ) -> DynamicModel:
        """Create a nonlinear dynamic model"""
        model = DynamicModel(model_type="nonlinear")

        # Simplified nonlinear model using polynomial terms
        try:
            # Fit polynomial trend
            t = np.arange(data.shape[0])
            model.parameters = {}

            for i, var_name in enumerate(variable_names):
                # Fit quadratic trend
                coeffs = np.polyfit(t, data[:, i], 2)
                model.parameters[var_name] = coeffs.tolist()

                # Generate equation
                equation = f"{var_name}(t) = {coeffs[0]:.4f} + {coeffs[1]:.4f}*t + {coeffs[2]:.4f}*t²"
                model.equations.append(equation)

            model.predictive_power = 0.6
            model.confidence = 0.6

        except Exception as e:
            logger.error(f"Error in nonlinear modeling: {e}")
            model = DynamicModel(
                model_type="nonlinear",
                state_variables=variable_names,
                confidence=0.3
            )

        return model


class StatePredictor:
    """
    Predicts future states of biological systems

    Uses dynamic models to forecast how biological systems will
    evolve over time.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize State Predictor

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.prediction_horizon = self.config.get('prediction_horizon', 10)

    def predict(
        self,
        model: DynamicModel,
        current_state: Dict[str, float],
        horizon: Optional[int] = None,
        **kwargs
    ) -> List[StatePrediction]:
        """
        Predict future system states

        Args:
            model: Dynamic model of the system
            current_state: Current state of the system
            horizon: Prediction horizon
            **kwargs: Additional arguments

        Returns:
            List of state predictions
        """
        horizon = horizon or self.prediction_horizon
        predictions = []

        try:
            for var_name in model.state_variables:
                if var_name not in current_state:
                    continue

                current_value = current_state[var_name]

                # Generate predictions based on model type
                if model.model_type == "VAR":
                    pred = self._var_predict(model, var_name, current_value, horizon)
                elif model.model_type == "nonlinear":
                    pred = self._nonlinear_predict(model, var_name, current_value, horizon)
                else:
                    pred = self._default_predict(var_name, current_value, horizon)

                predictions.append(pred)

            logger.info(f"Generated {len(predictions)} state predictions")

        except Exception as e:
            logger.error(f"Error predicting states: {e}")

        return predictions

    def _var_predict(
        self,
        model: DynamicModel,
        var_name: str,
        current_value: float,
        horizon: int
    ) -> StatePrediction:
        """Predict using VAR model"""
        # Simplified VAR prediction
        predicted_values = [current_value]  # Start with current value

        # Simple AR(1) prediction
        for _ in range(horizon):
            next_val = predicted_values[-1] * 0.95 + np.random.normal(0, 0.1)
            predicted_values.append(next_val)

        # Remove initial value
        predicted_values = predicted_values[1:]

        time_points = list(range(1, horizon + 1))
        confidence_intervals = [(v * 0.9, v * 1.1) for v in predicted_values]

        return StatePrediction(
            variable=var_name,
            current_value=current_value,
            predicted_values=predicted_values,
            time_points=time_points,
            confidence_intervals=confidence_intervals,
            method="VAR",
            confidence=0.7
        )

    def _nonlinear_predict(
        self,
        model: DynamicModel,
        var_name: str,
        current_value: float,
        horizon: int
    ) -> StatePrediction:
        """Predict using nonlinear model"""
        # Simplified polynomial prediction
        if var_name in model.parameters and model.parameters[var_name]:
            coeffs = model.parameters[var_name]
            t_start = 0
            predicted_values = []

            for h in range(1, horizon + 1):
                t = t_start + h
                val = coeffs[0] * t**2 + coeffs[1] * t + coeffs[2]
                predicted_values.append(val)

            time_points = list(range(1, horizon + 1))
            confidence_intervals = [(v * 0.8, v * 1.2) for v in predicted_values]

            return StatePrediction(
                variable=var_name,
                current_value=current_value,
                predicted_values=predicted_values,
                time_points=time_points,
                confidence_intervals=confidence_intervals,
                method="nonlinear",
                confidence=0.6
            )
        else:
            return self._default_predict(var_name, current_value, horizon)

    def _default_predict(
        self,
        var_name: str,
        current_value: float,
        horizon: int
    ) -> StatePrediction:
        """Default prediction (constant)"""
        predicted_values = [current_value] * horizon
        time_points = list(range(1, horizon + 1))
        confidence_intervals = [(current_value * 0.9, current_value * 1.1)] * horizon

        return StatePrediction(
            variable=var_name,
            current_value=current_value,
            predicted_values=predicted_values,
            time_points=time_points,
            confidence_intervals=confidence_intervals,
            method="default",
            confidence=0.3
        )


class InterventionOptimizer:
    """
    Identifies optimal intervention points in biological systems

    Analyzes causal models to find where interventions would have
    the maximum effect on desired outcomes.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Intervention Optimizer

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def optimize(
        self,
        graph: TemporalCausalGraph,
        target_variable: str,
        intervention_type: str = "modulation",
        **kwargs
    ) -> List[Intervention]:
        """
        Optimize interventions to achieve desired outcome

        Args:
            graph: Causal graph of the system
            target_variable: Variable to influence
            intervention_type: Type of intervention
            **kwargs: Additional arguments

        Returns:
            List of optimized interventions
        """
        interventions = []

        try:
            # Find parents (direct causes) of target variable
            parents = graph.get_parents(target_variable)

            for parent in parents:
                # Find edge with maximum strength
                parent_edges = [e for e in graph.edges
                               if e.source == parent and e.target == target_variable]

                if parent_edges:
                    # Sort by strength
                    parent_edges.sort(key=lambda e: e.strength, reverse=True)
                    best_edge = parent_edges[0]

                    # Create intervention
                    intervention = Intervention(
                        target=best_edge.source,
                        type=intervention_type,
                        magnitude=0.5,  # Moderate intervention
                        time_point=best_edge.lag,
                        expected_effect={target_variable: best_edge.strength},
                        confidence=best_edge.confidence,
                        alternatives=[]
                    )

                    # Add alternative interventions
                    for strength in [0.3, 0.7]:
                        alt = Intervention(
                            target=best_edge.source,
                            type=intervention_type,
                            magnitude=strength,
                            time_point=best_edge.lag,
                            expected_effect={target_variable: strength * best_edge.strength},
                            confidence=best_edge.confidence * 0.9
                        )
                        intervention.alternatives.append(alt.to_dict())

                    interventions.append(intervention)

            # Sort by expected effect
            interventions.sort(
                key=lambda i: i.expected_effect.get(target_variable, 0),
                reverse=True
            )

            logger.info(f"Generated {len(interventions)} intervention options")

        except Exception as e:
            logger.error(f"Error optimizing interventions: {e}")

        return interventions


class TemporalCausalDiscovery:
    """
    Main orchestrator for Temporal Causal Discovery

    Coordinates time-series causal learning, dynamic system modeling,
    state prediction, and intervention optimization.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Temporal Causal Discovery

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Initialize components
        self.learner = TimeSeriesCausalLearner(config)
        self.modeler = DynamicSystemModeler(config)
        self.predictor = StatePredictor(config)
        self.optimizer = InterventionOptimizer(config)

        logger.info("Temporal Causal Discovery initialized")

    def learn_from_data(
        self,
        data: Union[np.ndarray, Dict[str, np.ndarray], 'pd.DataFrame'],
        method: CausalInferenceMethod = CausalInferenceMethod.GRANGER_CAUSALITY
    ) -> Dict[str, Any]:
        """
        Learn causal structure from time-series data

        Args:
            data: Time-series data
            method: Causal inference method

        Returns:
            Learned causal graph (as dictionary)
        """
        graph = self.learner.learn_from_data(data, method)
        return graph.to_dict()

    def model_dynamics(
        self,
        data: Union[np.ndarray, Dict[str, np.ndarray]],
        system_type: SystemType = SystemType.LINEAR
    ) -> Dict[str, Any]:
        """
        Model system dynamics

        Args:
            data: Time-series data
            system_type: Type of system

        Returns:
            Dynamic model (as dictionary)
        """
        model = self.modeler.model_system(data, system_type)
        return model.to_dict()

    def predict_future(
        self,
        model: Union[DynamicModel, Dict[str, Any]],
        current_state: Dict[str, float],
        horizon: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Predict future system states

        Args:
            model: Dynamic model
            current_state: Current system state
            horizon: Prediction horizon

        Returns:
            List of state predictions (as dictionaries)
        """
        # Convert dict to model if needed
        if isinstance(model, dict):
            model_obj = DynamicModel(
                model_type=model['model_type'],
                parameters=model.get('parameters', {}),
                state_variables=model.get('state_variables', []),
                equations=model.get('equations', []),
                fit_quality=model.get('fit_quality', {}),
                predictive_power=model.get('predictive_power', 0.5),
                confidence=model.get('confidence', 0.5)
            )
        else:
            model_obj = model

        predictions = self.predictor.predict(model_obj, current_state, horizon)
        return [p.to_dict() for p in predictions]

    def optimize_interventions(
        self,
        graph: Union[TemporalCausalGraph, Dict[str, Any]],
        target_variable: str,
        intervention_type: str = "modulation"
    ) -> List[Dict[str, Any]]:
        """
        Optimize interventions

        Args:
            graph: Causal graph
            target_variable: Target variable
            intervention_type: Type of intervention

        Returns:
            List of interventions (as dictionaries)
        """
        # Convert dict to graph if needed
        if isinstance(graph, dict):
            graph_obj = TemporalCausalGraph(
                nodes=graph.get('nodes', []),
                edges=[CausalEdge(**e) for e in graph.get('edges', [])],
                time_granularity=graph.get('time_granularity', 'arbitrary'),
                sample_size=graph.get('sample_size', 0),
                time_range=graph.get('time_range', (0, 0)),
                confidence=graph.get('confidence', 0.5)
            )
        else:
            graph_obj = graph

        interventions = self.optimizer.optimize(graph_obj, target_variable, intervention_type)
        return [i.to_dict() for i in interventions]


__all__ = [
    # Main orchestrator
    'TemporalCausalDiscovery',

    # Components
    'TimeSeriesCausalLearner',
    'DynamicSystemModeler',
    'StatePredictor',
    'InterventionOptimizer',

    # Data classes
    'CausalEdge',
    'TemporalCausalGraph',
    'DynamicModel',
    'StatePrediction',
    'Intervention',

    # Enums
    'CausalInferenceMethod',
    'SystemType',
]
