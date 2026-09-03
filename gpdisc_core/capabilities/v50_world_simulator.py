"""
V50 World Simulator - Physics, Chemistry, and Biological Simulation Engine

Provides multi-domain simulation capabilities for counterfactual reasoning
and mechanistic understanding across scientific domains.

Date: 2026-04-23
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
import numpy as np


class SimulationDomain(Enum):
    """Domains available for simulation"""
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COUNTERFACTUAL = "counterfactual"


@dataclass
class SimulationResult:
    """Result of a simulation run"""
    domain: SimulationDomain
    success: bool
    final_state: Dict[str, Any]
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    error_message: Optional[str] = None


@dataclass
class PhysicalState:
    """State representation for physical simulations"""
    position: np.ndarray
    velocity: np.ndarray
    mass: float
    charge: float
    time: float = 0.0
    additional_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChemicalState:
    """State representation for chemical simulations"""
    concentrations: Dict[str, float]
    temperature: float
    pressure: float
    volume: float
    ph: Optional[float] = None
    time: float = 0.0


@dataclass
class BiologicalState:
    """State representation for biological simulations"""
    species_counts: Dict[str, float]
    gene_expression: Dict[str, float]
    metabolic_state: Dict[str, float]
    time: float = 0.0


class WorldModelInterface:
    """Base interface for world models"""

    def simulate(self, initial_state: Dict[str, Any], duration: float,
                 parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """Run simulation from initial state for specified duration"""
        raise NotImplementedError

    def reset(self):
        """Reset simulation to initial conditions"""
        raise NotImplementedError

    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        raise NotImplementedError


class PhysicsEngine(WorldModelInterface):
    """
    Physics simulation engine for mechanistic reasoning

    Supports:
    - Classical mechanics (F = ma)
    - Gravitational interactions
    - Electromagnetic forces
    - Thermodynamic processes
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.constants = {
            'G': 6.674e-11,  # Gravitational constant
            'k_e': 8.987e9,  # Coulomb constant
            'h': 6.626e-34,  # Planck constant
        }
        self.current_state = None

    def simulate(self, initial_state: Dict[str, Any], duration: float,
                 parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """Run physics simulation"""
        try:
            params = parameters or {}
            dt = params.get('timestep', 0.01)
            n_steps = int(duration / dt)

            # Initialize state
            state = PhysicalState(
                position=np.array(initial_state.get('position', [0.0, 0.0, 0.0])),
                velocity=np.array(initial_state.get('velocity', [0.0, 0.0, 0.0])),
                mass=initial_state.get('mass', 1.0),
                charge=initial_state.get('charge', 0.0),
                time=0.0
            )

            trajectory = []
            forces = params.get('forces', [])

            # Time integration
            for _ in range(n_steps):
                # Calculate net force
                F_net = np.zeros(3)
                for force_config in forces:
                    force_type = force_config.get('type')
                    if force_type == 'gravitational':
                        F_net += self._gravitational_force(state, force_config)
                    elif force_type == 'electric':
                        F_net += self._electric_force(state, force_config)
                    elif force_type == 'constant':
                        F_net += np.array(force_config.get('vector', [0.0, 0.0, 0.0]))

                # Update velocity and position (Euler integration)
                acceleration = F_net / state.mass
                state.velocity += acceleration * dt
                state.position += state.velocity * dt
                state.time += dt

                trajectory.append({
                    'position': state.position.copy(),
                    'velocity': state.velocity.copy(),
                    'time': state.time
                })

            self.current_state = state

            return SimulationResult(
                domain=SimulationDomain.PHYSICS,
                success=True,
                final_state={
                    'position': state.position.tolist(),
                    'velocity': state.velocity.tolist(),
                    'time': state.time
                },
                trajectory=trajectory,
                metrics={'final_kinetic_energy': 0.5 * state.mass * np.linalg.norm(state.velocity)**2}
            )

        except Exception as e:
            return SimulationResult(
                domain=SimulationDomain.PHYSICS,
                success=False,
                final_state={},
                error_message=str(e)
            )

    def _gravitational_force(self, state: PhysicalState, config: Dict[str, Any]) -> np.ndarray:
        """Calculate gravitational force"""
        other_mass = config.get('mass', 1.0)
        other_position = np.array(config.get('position', [0.0, 0.0, 0.0]))

        r_vec = other_position - state.position
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-10:
            return np.zeros(3)

        force_mag = self.constants['G'] * state.mass * other_mass / (r_mag**2)
        return force_mag * r_vec / r_mag

    def _electric_force(self, state: PhysicalState, config: Dict[str, Any]) -> np.ndarray:
        """Calculate electric force"""
        other_charge = config.get('charge', 1.0)
        other_position = np.array(config.get('position', [0.0, 0.0, 0.0]))

        r_vec = state.position - other_position
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-10:
            return np.zeros(3)

        force_mag = self.constants['k_e'] * state.charge * other_charge / (r_mag**2)
        return force_mag * r_vec / r_mag

    def reset(self):
        self.current_state = None

    def get_state(self) -> Dict[str, Any]:
        if self.current_state is None:
            return {}
        return {
            'position': self.current_state.position.tolist(),
            'velocity': self.current_state.velocity.tolist(),
            'mass': self.current_state.mass,
            'time': self.current_state.time
        }


class ChemistryReactor(WorldModelInterface):
    """
    Chemical reactor simulation engine

    Supports:
    - Reaction kinetics (mass action)
    - Equilibrium calculations
    - pH calculations
    - Thermodynamic properties
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.current_state = None

    def simulate(self, initial_state: Dict[str, Any], duration: float,
                 parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """Run chemical simulation"""
        try:
            params = parameters or {}
            reactions = params.get('reactions', [])

            # Initialize state
            state = ChemicalState(
                concentrations=initial_state.get('concentrations', {}).copy(),
                temperature=initial_state.get('temperature', 298.15),
                pressure=initial_state.get('pressure', 1.0),
                volume=initial_state.get('volume', 1.0),
                ph=initial_state.get('ph'),
                time=0.0
            )

            dt = params.get('timestep', 0.1)
            n_steps = int(duration / dt)

            trajectory = []

            for _ in range(n_steps):
                # Calculate reaction rates
                rate_equations = self._calculate_rates(state, reactions)

                # Update concentrations
                for species, rate in rate_equations.items():
                    if species in state.concentrations:
                        state.concentrations[species] += rate * dt

                state.time += dt
                trajectory.append(state.concentrations.copy())

            self.current_state = state

            return SimulationResult(
                domain=SimulationDomain.CHEMISTRY,
                success=True,
                final_state={
                    'concentrations': state.concentrations,
                    'temperature': state.temperature,
                    'time': state.time
                },
                trajectory=trajectory
            )

        except Exception as e:
            return SimulationResult(
                domain=SimulationDomain.CHEMISTRY,
                success=False,
                final_state={},
                error_message=str(e)
            )

    def _calculate_rates(self, state: ChemicalState, reactions: List[Dict]) -> Dict[str, float]:
        """Calculate reaction rates using mass action kinetics"""
        rates = {}

        for reaction in reactions:
            rate_constant = reaction.get('rate_constant', 0.0)
            reactants = reaction.get('reactants', {})
            products = reaction.get('products', {})

            # Calculate reaction rate
            reaction_rate = rate_constant
            for species, stoichiometry in reactants.items():
                if species in state.concentrations:
                    reaction_rate *= state.concentrations[species] ** stoichiometry

            # Update species rates
            for species, stoichiometry in reactants.items():
                rates[species] = rates.get(species, 0.0) - stoichiometry * reaction_rate
            for species, stoichiometry in products.items():
                rates[species] = rates.get(species, 0.0) + stoichiometry * reaction_rate

        return rates

    def reset(self):
        self.current_state = None

    def get_state(self) -> Dict[str, Any]:
        if self.current_state is None:
            return {}
        return {
            'concentrations': self.current_state.concentrations,
            'temperature': self.current_state.temperature,
            'pressure': self.current_state.pressure,
            'time': self.current_state.time
        }


class BiologicalPathwaySimulator(WorldModelInterface):
    """
    Biological pathway simulation engine

    Supports:
    - Metabolic pathway simulations
    - Gene regulatory networks
    - Signal transduction
    - Population dynamics
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.current_state = None

    def simulate(self, initial_state: Dict[str, Any], duration: float,
                 parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """Run biological simulation"""
        try:
            params = parameters or {}
            interactions = params.get('interactions', [])

            state = BiologicalState(
                species_counts=initial_state.get('species_counts', {}).copy(),
                gene_expression=initial_state.get('gene_expression', {}).copy(),
                metabolic_state=initial_state.get('metabolic_state', {}).copy(),
                time=0.0
            )

            dt = params.get('timestep', 0.1)
            n_steps = int(duration / dt)

            trajectory = []

            for _ in range(n_steps):
                # Update state based on interactions
                self._update_state(state, interactions, dt)

                trajectory.append({
                    'species_counts': state.species_counts.copy(),
                    'gene_expression': state.gene_expression.copy(),
                    'time': state.time
                })

                state.time += dt

            self.current_state = state

            return SimulationResult(
                domain=SimulationDomain.BIOLOGY,
                success=True,
                final_state={
                    'species_counts': state.species_counts,
                    'gene_expression': state.gene_expression,
                    'time': state.time
                },
                trajectory=trajectory
            )

        except Exception as e:
            return SimulationResult(
                domain=SimulationDomain.BIOLOGY,
                success=False,
                final_state={},
                error_message=str(e)
            )

    def _update_state(self, state: BiologicalState, interactions: List[Dict], dt: float):
        """Update biological state based on interactions"""
        for interaction in interactions:
            interaction_type = interaction.get('type')

            if interaction_type == 'gene_regulation':
                self._apply_gene_regulation(state, interaction, dt)
            elif interaction_type == 'metabolic':
                self._apply_metabolic_interaction(state, interaction, dt)
            elif interaction_type == 'population_dynamics':
                self._apply_population_dynamics(state, interaction, dt)

    def _apply_gene_regulation(self, state: BiologicalState, interaction: Dict, dt: float):
        """Apply gene regulation interaction"""
        target = interaction.get('target')
        regulator = interaction.get('regulator')
        effect = interaction.get('effect', 'activate')  # or 'repress'
        strength = interaction.get('strength', 1.0)

        if regulator in state.gene_expression and target in state.gene_expression:
            regulator_level = state.gene_expression[regulator]
            change = strength * regulator_level * dt

            if effect == 'activate':
                state.gene_expression[target] += change
            elif effect == 'repress':
                state.gene_expression[target] -= change

            # Clamp to reasonable bounds
            state.gene_expression[target] = max(0.0, min(1.0, state.gene_expression[target]))

    def _apply_metabolic_interaction(self, state: BiologicalState, interaction: Dict, dt: float):
        """Apply metabolic interaction"""
        reactants = interaction.get('reactants', {})
        products = interaction.get('products', {})
        rate = interaction.get('rate', 1.0)

        # Check if all reactants are available
        can_proceed = True
        limiting_factor = float('inf')
        for species, amount in reactants.items():
            if species not in state.species_counts or state.species_counts[species] < amount:
                can_proceed = False
                break
            limiting_factor = min(limiting_factor, state.species_counts[species] / amount)

        if can_proceed:
            actual_rate = rate * limiting_factor
            for species, amount in reactants.items():
                state.species_counts[species] -= amount * actual_rate * dt
            for species, amount in products.items():
                state.species_counts[species] = state.species_counts.get(species, 0.0) + amount * actual_rate * dt

    def _apply_population_dynamics(self, state: BiologicalState, interaction: Dict, dt: float):
        """Apply population dynamics (e.g., Lotka-Volterra)"""
        species = interaction.get('species')
        growth_rate = interaction.get('growth_rate', 1.0)
        carrying_capacity = interaction.get('carrying_capacity')

        if species in state.species_counts:
            current = state.species_counts[species]
            if carrying_capacity:
                # Logistic growth
                change = growth_rate * current * (1 - current / carrying_capacity) * dt
            else:
                # Exponential growth
                change = growth_rate * current * dt

            state.species_counts[species] = max(0.0, current + change)

    def reset(self):
        self.current_state = None

    def get_state(self) -> Dict[str, Any]:
        if self.current_state is None:
            return {}
        return {
            'species_counts': self.current_state.species_counts,
            'gene_expression': self.current_state.gene_expression,
            'metabolic_state': self.current_state.metabolic_state,
            'time': self.current_state.time
        }


class CounterfactualEngine(WorldModelInterface):
    """
    Counterfactual reasoning engine

    Simulates what would have happened under different conditions
    by modifying initial conditions or parameters and comparing outcomes.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.base_simulations = {
            SimulationDomain.PHYSICS: PhysicsEngine(),
            SimulationDomain.CHEMISTRY: ChemistryReactor(),
            SimulationDomain.BIOLOGY: BiologicalPathwaySimulator()
        }

    def simulate(self, initial_state: Dict[str, Any], duration: float,
                 parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """Run counterfactual simulation"""
        try:
            params = parameters or {}
            domain = SimulationDomain(params.get('domain', 'physics'))
            intervention = params.get('intervention')

            # Get base simulator
            simulator = self.base_simulations.get(domain)
            if simulator is None:
                return SimulationResult(
                    domain=SimulationDomain.COUNTERFACTUAL,
                    success=False,
                    final_state={},
                    error_message=f"Unknown domain: {domain}"
                )

            # Apply intervention if specified
            modified_state = initial_state.copy()
            if intervention:
                modified_state = self._apply_intervention(initial_state, intervention)

            # Run simulation with modified conditions
            result = simulator.simulate(modified_state, duration, params)

            return SimulationResult(
                domain=SimulationDomain.COUNTERFACTUAL,
                success=result.success,
                final_state=result.final_state,
                trajectory=result.trajectory,
                metrics=result.metrics,
                error_message=result.error_message
            )

        except Exception as e:
            return SimulationResult(
                domain=SimulationDomain.COUNTERFACTUAL,
                success=False,
                final_state={},
                error_message=str(e)
            )

    def _apply_intervention(self, state: Dict[str, Any], intervention: Dict[str, Any]) -> Dict[str, Any]:
        """Apply counterfactual intervention to state"""
        modified = state.copy()
        intervention_type = intervention.get('type')

        if intervention_type == 'set_value':
            # Set a variable to a specific value
            modified[intervention['variable']] = intervention['value']
        elif intervention_type == 'multiply':
            # Multiply a variable by a factor
            variable = intervention['variable']
            if variable in modified:
                modified[variable] = modified[variable] * intervention['factor']
        elif intervention_type == 'add':
            # Add to a variable
            variable = intervention['variable']
            if variable in modified:
                modified[variable] = modified[variable] + intervention['amount']

        return modified

    def reset(self):
        for simulator in self.base_simulations.values():
            simulator.reset()

    def get_state(self) -> Dict[str, Any]:
        states = {}
        for domain, simulator in self.base_simulations.items():
            states[domain.value] = simulator.get_state()
        return states


# Factory functions for convenience
def create_world_simulator(domain: SimulationDomain, config: Optional[Dict[str, Any]] = None) -> WorldModelInterface:
    """Create a world simulator for the specified domain"""
    simulators = {
        SimulationDomain.PHYSICS: PhysicsEngine,
        SimulationDomain.CHEMISTRY: ChemistryReactor,
        SimulationDomain.BIOLOGY: BiologicalPathwaySimulator,
        SimulationDomain.COUNTERFACTUAL: CounterfactualEngine
    }
    simulator_class = simulators.get(domain)
    if simulator_class:
        return simulator_class(config)
    raise ValueError(f"Unknown domain: {domain}")


def create_physics_engine(config: Optional[Dict[str, Any]] = None) -> PhysicsEngine:
    """Create a physics simulation engine"""
    return PhysicsEngine(config)


def create_chemistry_reactor(config: Optional[Dict[str, Any]] = None) -> ChemistryReactor:
    """Create a chemical reactor simulation engine"""
    return ChemistryReactor(config)


def create_biology_simulator(config: Optional[Dict[str, Any]] = None) -> BiologicalPathwaySimulator:
    """Create a biological pathway simulator"""
    return BiologicalPathwaySimulator(config)


def create_counterfactual_engine(config: Optional[Dict[str, Any]] = None) -> CounterfactualEngine:
    """Create a counterfactual reasoning engine"""
    return CounterfactualEngine(config)


__all__ = [
    'WorldModelInterface',
    'PhysicsEngine',
    'ChemistryReactor',
    'BiologicalPathwaySimulator',
    'CounterfactualEngine',
    'SimulationDomain',
    'SimulationResult',
    'PhysicalState',
    'ChemicalState',
    'BiologicalState',
    'create_world_simulator',
    'create_physics_engine',
    'create_chemistry_reactor',
    'create_biology_simulator',
    'create_counterfactual_engine',
]
