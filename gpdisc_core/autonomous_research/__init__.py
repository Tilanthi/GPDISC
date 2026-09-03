"""
Autonomous Research System

This module contains the V7.0 autonomous research scientist system.
Re-exports the full public surface (types + engines) so callers can import
everything from this package. Each engine is guarded so an optional engine
with heavy dependencies cannot break the core scientist imports.
"""

# Core system
from .v7_autonomous_scientist import (
    V7AutonomousScientist,
    create_v7_scientist,
    ResearchCycle,
    ResearchQuestion,
    Hypothesis,
    Experiment,
    ResearchResult,
    Publication
)

# Shared types (no external dependencies)
from .types import (
    QuestionType,
    QuestionImportance,
    HypothesisStatus,
    HypothesisType,
    ExperimentType,
    DesignParameters,
    DataSource,
    PredictionType,
    PredictionConfidence,
    AnalysisType,
    CausalInferenceResult,
    RevisionType,
    TheoryStatus,
    PaperStructure,
    FigureType,
    ExecutionResult,
)

# Engines (guarded: optional heavy dependencies)
try:
    from .engines.question_generator import QuestionGenerator
except ImportError:
    QuestionGenerator = None

try:
    from .engines.hypothesis_formulator import HypothesisFormulator
except ImportError:
    HypothesisFormulator = None

try:
    from .engines.experiment_designer import ExperimentDesigner
except ImportError:
    ExperimentDesigner = None

try:
    from .engines.experiment_executor import ExperimentExecutor
except ImportError:
    ExperimentExecutor = None

try:
    from .engines.prediction_engine import (
        PredictionEngine,
        AnalysisEngine,
        TheoryRevisionEngine,
        PublicationEngine,
    )
except ImportError:
    PredictionEngine = None
    AnalysisEngine = None
    TheoryRevisionEngine = None
    PublicationEngine = None

__all__ = [
    # Main system
    'V7AutonomousScientist',
    'create_v7_scientist',
    'ResearchCycle',
    'ResearchQuestion',
    'Hypothesis',
    'Experiment',
    'ResearchResult',
    'Publication',
    # Types
    'QuestionType',
    'QuestionImportance',
    'HypothesisStatus',
    'HypothesisType',
    'ExperimentType',
    'DesignParameters',
    'DataSource',
    'PredictionType',
    'PredictionConfidence',
    'AnalysisType',
    'CausalInferenceResult',
    'RevisionType',
    'TheoryStatus',
    'PaperStructure',
    'FigureType',
    'ExecutionResult',
    # Engines
    'QuestionGenerator',
    'HypothesisFormulator',
    'ExperimentDesigner',
    'ExperimentExecutor',
    'PredictionEngine',
    'AnalysisEngine',
    'TheoryRevisionEngine',
    'PublicationEngine',
]
