"""
GPDISC Scientific Discovery Module
==================================

Generic scientific-discovery machinery retained from the BIODISC/ASTRA
era: feasibility checking for proposed experiments, literature
synthesis stubs, and the theoretical-physics solver stubs used by the
simulation-based inference layer.

GPDISC note (2026-09-04): the astronomy-specific modules —
astro_databases (Vizier/SIMBAD/ADS), data_repositories
(ALMA/NASA/ESO/CADC), advanced_analysis (galaxy classification,
photo-z, SED fitting) and the paper library — were removed in the
ASTRA-lineage purge.

Modules:
--------
- feasibility_checker: experiment feasibility, resource, and safety limits
- literature_synthesis: multi-paper synthesis (stub)
- theoretical_physics: MHD/plasma solver stubs (used by simulation_based_inference)

Version: 1.1.0-Discovery
"""

from .feasibility_checker import (
    FeasibilityAssessor,
    ResourceEstimator,
    SafetyValidator,
)
from .literature_synthesis import (
    LiteratureSynthesizer,
    HypothesisExtractor,
    FindingAggregator,
)
from .theoretical_physics import (
    TheoreticalPhysicsEngine,
    MHDSolver,
    PlasmaPhysicsModule,
    RadiationHydrodynamics,
    GRMHDModule,
    CosmicRayTransport,
    MagneticReconnection,
    solve_mhd,
    run_radiation_hydro,
)

__all__ = [
    'FeasibilityAssessor',
    'ResourceEstimator',
    'SafetyValidator',
    'LiteratureSynthesizer',
    'HypothesisExtractor',
    'FindingAggregator',
    'TheoreticalPhysicsEngine',
    'MHDSolver',
    'PlasmaPhysicsModule',
    'RadiationHydrodynamics',
    'GRMHDModule',
    'CosmicRayTransport',
    'MagneticReconnection',
    'solve_mhd',
    'run_radiation_hydro',
]

__version__ = '1.1.0-Discovery'
