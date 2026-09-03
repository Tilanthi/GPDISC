"""
V50 Meta-Learner - Learning to learn across reasoning tasks

Implements meta-learning capabilities that learn from previous reasoning
attempts to improve future performance.

Date: 2026-04-23
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime


class FailureType(Enum):
    """Types of reasoning failures"""
    INSUFFICIENT_KNOWLEDGE = "insufficient_knowledge"
    WRONG_APPROACH = "wrong_approach"
    COMPUTATIONAL_ERROR = "computational_error"
    MISUNDERSTANDING = "misunderstanding"
    TIME_LIMIT = "time_limit"


class CompetenceLevel(Enum):
    """Levels of competence"""
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ReasoningAttempt:
    """Record of a reasoning attempt"""
    task_id: str
    task_description: str
    task_type: str
    approach: str
    success: bool
    time_taken: float
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FailureAnalysis:
    """Analysis of a reasoning failure"""
    attempt: ReasoningAttempt
    failure_type: FailureType
    root_cause: str
    suggested_fix: str
    confidence: float


@dataclass
class Strategy:
    """A reasoning strategy"""
    name: str
    description: str
    applicable_task_types: List[str]
    success_rate: float = 0.0
    average_time: float = 0.0


@dataclass
class CompetenceBoundary:
    """Boundary of competence for a task type"""
    task_type: str
    current_level: CompetenceLevel
    successful_tasks: int = 0
    failed_tasks: int = 0
    best_strategy: Optional[str] = None


@dataclass
class CurriculumProblem:
    """A problem in a learning curriculum"""
    problem_id: str
    task_type: str
    difficulty: CompetenceLevel
    description: str
    prerequisite_skills: List[str] = field(default_factory=list)


class MetaLearningSystem:
    """
    Main meta-learning system

    Tracks performance across tasks and learns optimal strategies
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.attempts: List[ReasoningAttempt] = []
        self.strategies: Dict[str, Strategy] = {}
        self.competence_boundaries: Dict[str, CompetenceBoundary] = {}
        self._initialize_default_strategies()

    def _initialize_default_strategies(self):
        """Initialize default reasoning strategies"""
        default_strategies = [
            Strategy(
                name="chain_of_thought",
                description="Step-by-step reasoning",
                applicable_task_types=["math", "logic", "physics"]
            ),
            Strategy(
                name="divide_and_conquer",
                description="Break problem into sub-problems",
                applicable_task_types=["planning", "optimization"]
            ),
            Strategy(
                name="analogy",
                description="Use analogical reasoning",
                applicable_task_types=["creative", "explanation"]
            ),
            Strategy(
                name="formal",
                description="Use formal methods",
                applicable_task_types=["proof", "verification"]
            ),
            Strategy(
                name="heuristic",
                description="Use heuristic search",
                applicable_task_types=["search", "optimization"]
            ),
        ]

        for strategy in default_strategies:
            self.strategies[strategy.name] = strategy

    def record_attempt(self, attempt: ReasoningAttempt):
        """Record a reasoning attempt"""
        self.attempts.append(attempt)
        self._update_competence_boundaries(attempt)
        self._update_strategy_stats(attempt)

    def _update_competence_boundaries(self, attempt: ReasoningAttempt):
        """Update competence boundaries based on attempt"""
        task_type = attempt.task_type

        if task_type not in self.competence_boundaries:
            self.competence_boundaries[task_type] = CompetenceBoundary(
                task_type=task_type,
                current_level=CompetenceLevel.NOVICE
            )

        boundary = self.competence_boundaries[task_type]

        if attempt.success:
            boundary.successful_tasks += 1
        else:
            boundary.failed_tasks += 1

        # Update competence level
        total = boundary.successful_tasks + boundary.failed_tasks
        if total > 0:
            success_rate = boundary.successful_tasks / total

            if success_rate >= 0.9:
                boundary.current_level = CompetenceLevel.EXPERT
            elif success_rate >= 0.7:
                boundary.current_level = CompetenceLevel.ADVANCED
            elif success_rate >= 0.5:
                boundary.current_level = CompetenceLevel.INTERMEDIATE
            elif success_rate >= 0.3:
                boundary.current_level = CompetenceLevel.BEGINNER
            else:
                boundary.current_level = CompetenceLevel.NOVICE

    def _update_strategy_stats(self, attempt: ReasoningAttempt):
        """Update strategy statistics"""
        if attempt.approach not in self.strategies:
            self.strategies[attempt.approach] = Strategy(
                name=attempt.approach,
                description="Learned strategy",
                applicable_task_types=[attempt.task_type]
            )

        strategy = self.strategies[attempt.approach]

        # Update success rate
        strategy_attempts = [a for a in self.attempts if a.approach == attempt.approach]
        if strategy_attempts:
            successful = sum(1 for a in strategy_attempts if a.success)
            strategy.success_rate = successful / len(strategy_attempts)

            # Update average time
            strategy.average_time = sum(a.time_taken for a in strategy_attempts) / len(strategy_attempts)

    def get_competence_level(self, task_type: str) -> CompetenceLevel:
        """Get current competence level for a task type"""
        if task_type in self.competence_boundaries:
            return self.competence_boundaries[task_type].current_level
        return CompetenceLevel.NOVICE

    def recommend_strategy(self, task_type: str) -> Optional[str]:
        """Recommend best strategy for a task type"""
        applicable_strategies = [
            (name, strat) for name, strat in self.strategies.items()
            if task_type in strat.applicable_task_types
        ]

        if not applicable_strategies:
            return None

        # Sort by success rate
        applicable_strategies.sort(key=lambda x: x[1].success_rate, reverse=True)

        return applicable_strategies[0][0]


class FailureAnalyzer:
    """Analyzes reasoning failures to identify root causes"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def analyze_failure(self, attempt: ReasoningAttempt) -> FailureAnalysis:
        """Analyze a failed reasoning attempt"""
        if attempt.success:
            raise ValueError("Cannot analyze successful attempt")

        # Determine failure type
        failure_type = self._classify_failure(attempt)

        # Identify root cause
        root_cause = self._identify_root_cause(attempt, failure_type)

        # Suggest fix
        suggested_fix = self._suggest_fix(attempt, failure_type, root_cause)

        return FailureAnalysis(
            attempt=attempt,
            failure_type=failure_type,
            root_cause=root_cause,
            suggested_fix=suggested_fix,
            confidence=0.7
        )

    def _classify_failure(self, attempt: ReasoningAttempt) -> FailureType:
        """Classify the type of failure"""
        error_msg = attempt.error_message or ""

        if "timeout" in error_msg.lower() or "time" in error_msg.lower():
            return FailureType.TIME_LIMIT

        if "not found" in error_msg.lower() or "unknown" in error_msg.lower():
            return FailureType.INSUFFICIENT_KNOWLEDGE

        if "calculation" in error_msg.lower() or "compute" in error_msg.lower():
            return FailureType.COMPUTATIONAL_ERROR

        if "wrong" in error_msg.lower() or "incorrect" in error_msg.lower():
            return FailureType.WRONG_APPROACH

        return FailureType.MISUNDERSTANDING

    def _identify_root_cause(self, attempt: ReasoningAttempt,
                            failure_type: FailureType) -> str:
        """Identify root cause of failure"""
        causes = {
            FailureType.INSUFFICIENT_KNOWLEDGE: "Missing domain knowledge or facts",
            FailureType.WRONG_APPROACH: "Selected approach inappropriate for task",
            FailureType.COMPUTATIONAL_ERROR: "Error in calculation or computation",
            FailureType.MISUNDERSTANDING: "Misinterpretation of problem requirements",
            FailureType.TIME_LIMIT: "Insufficient time for chosen approach"
        }

        return causes.get(failure_type, "Unknown cause")

    def _suggest_fix(self, attempt: ReasoningAttempt,
                    failure_type: FailureType,
                    root_cause: str) -> str:
        """Suggest fix for the failure"""
        fixes = {
            FailureType.INSUFFICIENT_KNOWLEDGE: "Acquire relevant domain knowledge or use external knowledge sources",
            FailureType.WRONG_APPROACH: "Try alternative reasoning strategies",
            FailureType.COMPUTATIONAL_ERROR: "Verify calculations step-by-step or use computational tools",
            FailureType.MISUNDERSTANDING: "Re-read problem statement and clarify requirements",
            FailureType.TIME_LIMIT: "Use more efficient approach or allocate more time"
        }

        return fixes.get(failure_type, "Review approach and try different method")


class StrategyAbstractor:
    """Abstracts successful strategies for reuse"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.abstracted_strategies: Dict[str, Dict[str, Any]] = {}

    def abstract_strategy(self, attempts: List[ReasoningAttempt]) -> Optional[Dict[str, Any]]:
        """Abstract a strategy from successful attempts"""
        # Filter successful attempts
        successful = [a for a in attempts if a.success]

        if not successful:
            return None

        # Group by approach
        by_approach: Dict[str, List[ReasoningAttempt]] = {}
        for attempt in successful:
            if attempt.approach not in by_approach:
                by_approach[attempt.approach] = []
            by_approach[attempt.approach].append(attempt)

        # Find most successful approach
        best_approach = None
        best_success_rate = 0.0

        for approach, attempt_list in by_approach.items():
            if len(attempt_list) >= 3:  # Need multiple examples
                success_rate = 1.0  # All successful by construction
                if success_rate > best_success_rate:
                    best_success_rate = success_rate
                    best_approach = approach

        if best_approach is None:
            return None

        # Abstract the strategy
        strategy = {
            "name": best_approach,
            "task_types": list(set(a.task_type for a in by_approach[best_approach])),
            "success_rate": best_success_rate,
            "average_time": sum(a.time_taken for a in by_approach[best_approach]) / len(by_approach[best_approach]),
            "extracted_from": len(by_approach[best_approach])
        }

        self.abstracted_strategies[best_approach] = strategy

        return strategy


class CurriculumGenerator:
    """Generates learning curricula based on competence boundaries"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.problem_database: List[CurriculumProblem] = []
        self._initialize_problems()

    def _initialize_problems(self):
        """Initialize problem database"""
        # Sample problems - in practice would be much larger
        self.problem_database = [
            CurriculumProblem(
                problem_id="math_001",
                task_type="math",
                difficulty=CompetenceLevel.BEGINNER,
                description="Simple arithmetic"
            ),
            CurriculumProblem(
                problem_id="math_002",
                task_type="math",
                difficulty=CompetenceLevel.INTERMEDIATE,
                description="Algebra equations",
                prerequisite_skills=["basic_arithmetic"]
            ),
            CurriculumProblem(
                problem_id="math_003",
                task_type="math",
                difficulty=CompetenceLevel.ADVANCED,
                description="Calculus problems",
                prerequisite_skills=["algebra", "functions"]
            ),
            CurriculumProblem(
                problem_id="logic_001",
                task_type="logic",
                difficulty=CompetenceLevel.BEGINNER,
                description="Simple syllogisms"
            ),
            CurriculumProblem(
                problem_id="logic_002",
                task_type="logic",
                difficulty=CompetenceLevel.INTERMEDIATE,
                description="Propositional logic",
                prerequisite_skills=["logical_connectives"]
            ),
        ]

    def generate_curriculum(self, task_type: str,
                           current_level: CompetenceLevel) -> List[CurriculumProblem]:
        """Generate a curriculum for a task type"""
        # Filter problems by task type
        task_problems = [p for p in self.problem_database if p.task_type == task_type]

        # Order by difficulty
        level_order = {
            CompetenceLevel.NOVICE: 0,
            CompetenceLevel.BEGINNER: 1,
            CompetenceLevel.INTERMEDIATE: 2,
            CompetenceLevel.ADVANCED: 3,
            CompetenceLevel.EXPERT: 4
        }

        # Start from current level and include harder problems
        current_value = level_order.get(current_level, 0)

        curriculum = []
        for problem in task_problems:
            problem_level_value = level_order.get(problem.difficulty, 0)
            if problem_level_value >= current_value - 1:  # Include slightly easier for practice
                curriculum.append(problem)

        # Sort by difficulty
        curriculum.sort(key=lambda p: level_order.get(p.difficulty, 0))

        return curriculum[:10]  # Return up to 10 problems


class CompetenceTracker:
    """Tracks competence across task types"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.competence_history: Dict[str, List[Tuple[datetime, CompetenceLevel]]] = {}

    def update_competence(self, task_type: str, level: CompetenceLevel):
        """Update competence level for a task type"""
        if task_type not in self.competence_history:
            self.competence_history[task_type] = []

        self.competence_history[task_type].append((datetime.now(), level))

    def get_competence_trend(self, task_type: str) -> str:
        """Get trend in competence over time"""
        if task_type not in self.competence_history:
            return "unknown"

        history = self.competence_history[task_type]

        if len(history) < 2:
            return "insufficient_data"

        level_order = {
            CompetenceLevel.NOVICE: 0,
            CompetenceLevel.BEGINNER: 1,
            CompetenceLevel.INTERMEDIATE: 2,
            CompetenceLevel.ADVANCED: 3,
            CompetenceLevel.EXPERT: 4
        }

        recent = history[-5:]  # Look at recent 5 entries

        if len(recent) < 2:
            return "stable"

        first_level = level_order.get(recent[0][1], 0)
        last_level = level_order.get(recent[-1][1], 0)

        if last_level > first_level:
            return "improving"
        elif last_level < first_level:
            return "declining"
        else:
            return "stable"


# Factory functions
def create_meta_learner(config: Optional[Dict[str, Any]] = None) -> MetaLearningSystem:
    """Create a meta-learning system"""
    return MetaLearningSystem(config)


def create_failure_analyzer(config: Optional[Dict[str, Any]] = None) -> FailureAnalyzer:
    """Create a failure analyzer"""
    return FailureAnalyzer(config)


def create_curriculum_generator(config: Optional[Dict[str, Any]] = None) -> CurriculumGenerator:
    """Create a curriculum generator"""
    return CurriculumGenerator(config)


def create_competence_tracker(config: Optional[Dict[str, Any]] = None) -> CompetenceTracker:
    """Create a competence tracker"""
    return CompetenceTracker(config)


__all__ = [
    'FailureType',
    'CompetenceLevel',
    'ReasoningAttempt',
    'FailureAnalysis',
    'Strategy',
    'CompetenceBoundary',
    'CurriculumProblem',
    'MetaLearningSystem',
    'FailureAnalyzer',
    'StrategyAbstractor',
    'CurriculumGenerator',
    'CompetenceTracker',
    'create_meta_learner',
    'create_failure_analyzer',
    'create_curriculum_generator',
    'create_competence_tracker',
]
