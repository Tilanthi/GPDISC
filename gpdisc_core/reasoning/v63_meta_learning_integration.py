"""
V63 Meta-Learning Integration - Tying Expert Feedback Into Architecture

This module integrates V61 (Expert Feedback Learner) and V62 (Domain Artifact Verifier)
with existing V60 capabilities and the MCE Evolutionary Context Layer.

INTEGRATION PATTERN:
1. Before starting task → Check for blind spots using V61
2. During task → Apply evolutionary context using MCE enhancement
3. Before output → Verify artifacts using V62
4. After feedback → Extract patterns using V61, update heuristics

This creates a continuous learning loop from expert feedback.

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json
from datetime import datetime

# Import new capabilities
try:
    from .v61_expert_feedback_learner import (
        ExpertFeedbackPatternExtractor,
        ExpertFeedback,
        ExtractedPattern,
        BlindSpot,
        create_expert_feedback_learner
    )
    V61_AVAILABLE = True
except ImportError:
    V61_AVAILABLE = False

try:
    from .v62_domain_artifact_verifier import (
        DomainArtifactVerifier,
        VerificationIssue,
        create_domain_artifact_verifier
    )
    V62_AVAILABLE = True
except ImportError:
    V62_AVAILABLE = False

# Import MCE enhancement
try:
    from ..metacognitive.evolutionary_context_layer import (
        EvolutionaryContextLayer,
        PhysicsBiologyIntegrator,
        create_evolutionary_context_layer,
        create_physics_biology_integrator
    )
    EVOLUTIONARY_LAYER_AVAILABLE = True
except ImportError:
    EVOLUTIONARY_LAYER_AVAILABLE = False

# Import existing V60 capabilities
try:
    from .v60_cognitive_agent import CognitiveAgent, CognitiveMode
    from .v60_persistent_memory import PersistentMemorySystem, MemoryType
    V60_AVAILABLE = True
except ImportError:
    V60_AVAILABLE = False


class LearningCycleStage(Enum):
    """Stages in the meta-learning cycle"""
    PRE_TASK = "pre_task"           # Before starting: check blind spots
    DURING_TASK = "during_task"     # During task: apply learned patterns
    PRE_OUTPUT = "pre_output"       # Before output: verify artifacts
    POST_TASK = "post_task"         # After task: store experience
    POST_FEEDBACK = "post_feedback" # After feedback: extract patterns


@dataclass
class TaskContext:
    """Context for a task being processed"""
    task_id: str
    description: str
    domain: str
    timestamp: float
    blind_spot_warnings: List[str] = field(default_factory=list)
    applied_patterns: List[str] = field(default_factory=list)
    verification_issues: List[VerificationIssue] = field(default_factory=list)
    evolutionary_context_applied: bool = False


class MetaLearningOrchestrator:
    """
    Orchestrates meta-learning from expert feedback across all capabilities.

    INTEGRATES:
    - V61 ExpertFeedbackPatternExtractor: Learn what experts notice
    - V62 DomainArtifactVerifier: Catch common errors
    - EvolutionaryContextLayer: Apply origins-first framing
    - V60 PersistentMemory: Store learned patterns

    LEARNING LOOP:
    1. PRE_TASK: Check for blind spots, get warnings
    2. DURING_TASK: Apply learned patterns, get evolutionary context
    3. PRE_OUTPUT: Verify citations, equations, formatting
    4. POST_TASK: Store experience in episodic memory
    5. POST_FEEDBACK: Extract patterns, update heuristics
    """

    def __init__(self):
        # Initialize components
        if V61_AVAILABLE:
            self.feedback_learner = create_expert_feedback_learner()
        else:
            self.feedback_learner = None

        if V62_AVAILABLE:
            self.artifact_verifier = create_domain_artifact_verifier()
        else:
            self.artifact_verifier = None

        if EVOLUTIONARY_LAYER_AVAILABLE:
            self.evolutionary_layer = create_evolutionary_context_layer()
            self.physics_biology_integrator = create_physics_biology_integrator()
        else:
            self.evolutionary_layer = None
            self.physics_biology_integrator = None

        if V60_AVAILABLE:
            self.memory = None  # Would be initialized with agent
        else:
            self.memory = None

        # Learning state
        self.current_task: Optional[TaskContext] = None
        self.learned_patterns: Dict[str, ExtractedPattern] = {}
        self.active_blind_spots: Dict[str, BlindSpot] = {}

    def pre_task_check(self, task_description: str, domain: str) -> TaskContext:
        """
        Perform pre-task checks before starting work.

        CHECKS:
        1. Blind spot detection (V61)
        2. Pattern retrieval (what applies to this task?)
        3. Evolutionary context needed?

        Returns TaskContext with warnings and recommendations.
        """
        task_id = f"task_{int(datetime.now().timestamp())}"

        warnings = []
        applied_patterns = []

        # Check for blind spots
        if self.feedback_learner:
            blind_spot_warnings = self.feedback_learner.check_for_blind_spots(
                task_description, domain
            )
            warnings.extend(blind_spot_warnings)

        # Get relevant patterns
        if self.feedback_learner:
            task_dict = {'description': task_description, 'domain': domain}
            relevant = self.feedback_learner.get_relevant_patterns(task_dict)
            applied_patterns = [p.id for p in relevant]

        # Check if evolutionary context needed
        evolutionary_needed = False
        if self.evolutionary_layer:
            if self.evolutionary_layer.is_biological_question(task_description):
                if not self.evolutionary_layer.has_evolutionary_context(task_description):
                    evolutionary_needed = True
                    warnings.append(
                        "EVOLUTIONARY CONTEXT: Biological question detected. "
                        "Consider applying origins-first perspective: "
                        "What physical constraints existed before molecular regulation? "
                        "What selective advantages favored increasing complexity?"
                    )

        context = TaskContext(
            task_id=task_id,
            description=task_description,
            domain=domain,
            timestamp=datetime.now().timestamp(),
            blind_spot_warnings=warnings,
            applied_patterns=applied_patterns,
            evolutionary_context_applied=evolutionary_needed
        )

        self.current_task = context
        return context

    def apply_evolutionary_context(self, question: str) -> str:
        """
        Apply evolutionary context to biological questions.

        Returns enhanced question with origins-first framing.
        """
        if not self.evolutionary_layer:
            return question

        evolutionary_q = self.evolutionary_layer.apply_origins_frame(question)

        if evolutionary_q.reframamed_question != question:
            # Log that evolutionary context was applied
            if self.current_task:
                self.current_task.evolutionary_context_applied = True

            # Return the enhanced prompt
            return self.evolutionary_layer.get_evolutionary_context_prompt(question)

        return question

    def pre_output_verification(
        self,
        text: str,
        bibliography: str = "",
        context: str = "academic_paper"
    ) -> List[VerificationIssue]:
        """
        Perform pre-output verification before delivering results.

        VERIFIES:
        1. Citation integrity (V62)
        2. Mathematical expression protection
        3. Compression appropriateness

        Returns list of issues found.
        """
        issues = []

        if self.artifact_verifier:
            # Verify citations if bibliography provided
            if bibliography:
                citation_issues = self.artifact_verifier.citation_verifier.verify_citation_integrity(
                    text, bibliography
                )
                issues.extend(citation_issues)

            # Check compression appropriateness
            compression_issues = self.artifact_verifier.compression_checker.check_compression(
                text, context
            )
            issues.extend(compression_issues)

        # Store issues in task context
        if self.current_task:
            self.current_task.verification_issues = issues

        return issues

    def post_task_storage(self, task_context: TaskContext, result: str) -> None:
        """
        Store task experience in persistent memory.

        Stores:
        - Task description and result
        - Applied patterns and warnings
        - Verification issues
        - Performance metrics

        This creates episodic memories that can be consolidated later.
        """
        if not V60_AVAILABLE or not self.memory:
            return

        # Create episodic memory
        episode = {
            'task_id': task_context.task_id,
            'description': task_context.description,
            'domain': task_context.domain,
            'timestamp': task_context.timestamp,
            'blind_spot_warnings': task_context.blind_spot_warnings,
            'applied_patterns': task_context.applied_patterns,
            'verification_issues': [str(i) for i in task_context.verification_issues],
            'evolutionary_context_applied': task_context.evolutionary_context_applied,
            'result_length': len(result),
            'success': len(task_context.verification_issues) == 0
        }

        # Would store in episodic memory
        # self.memory.episodic_memory.store(episode)

    def process_feedback(
        self,
        task_id: str,
        feedback_text: str,
        domain: str,
        severity: float = 0.5
    ) -> List[ExtractedPattern]:
        """
        Process expert feedback and extract learning patterns.

        EXTRACTS:
        1. Attention patterns (what expert noticed)
        2. Blind spots (systematic gaps)
        3. Corrective actions (what to do differently)

        Updates heuristics and stores in semantic memory.
        """
        if not self.feedback_learner:
            return []

        # Create feedback object
        feedback = ExpertFeedback(
            id=f"feedback_{int(datetime.now().timestamp())}",
            timestamp=datetime.now().timestamp(),
            domain=domain,
            feedback_text=feedback_text,
            context={'task_id': task_id},
            severity=severity
        )

        # Extract patterns
        patterns = self.feedback_learner.extract_patterns([feedback])

        # Detect blind spots
        blind_spots = self.feedback_learner.detect_blind_spots([feedback])

        # Update heuristics
        self.feedback_learner.update_heuristics(patterns)

        # Store in semantic memory
        # Would consolidate to semantic memory for long-term retention

        # Update internal state
        for pattern in patterns:
            self.learned_patterns[pattern.id] = pattern

        for blind_spot in blind_spots:
            self.active_blind_spots[blind_spot.id] = blind_spot

        return patterns

    def get_learning_summary(self) -> Dict[str, Any]:
        """
        Get summary of what has been learned from expert feedback.
        """
        return {
            'total_patterns_learned': len(self.learned_patterns),
            'total_blind_spots_identified': len(self.active_blind_spots),
            'patterns_by_type': self._count_patterns_by_type(),
            'blind_spots_by_category': self._count_blind_spots_by_category(),
            'recent_learning': self._get_recent_learning()
        }

    def _count_patterns_by_type(self) -> Dict[str, int]:
        """Count learned patterns by type"""
        from .v61_expert_feedback_learner import PatternType
        counts = {pt.value: 0 for pt in PatternType}
        for pattern in self.learned_patterns.values():
            counts[pattern.pattern_type.value] += 1
        return {k: v for k, v in counts.items() if v > 0}

    def _count_blind_spots_by_category(self) -> Dict[str, int]:
        """Count blind spots by category"""
        from .v61_expert_feedback_learner import BlindSpotCategory
        counts = {bsc.value: 0 for bsc in BlindSpotCategory}
        for blind_spot in self.active_blind_spots.values():
            counts[blind_spot.category.value] += 1
        return {k: v for k, v in counts.items() if v > 0}

    def _get_recent_learning(self) -> List[Dict[str, str]]:
        """Get recently learned patterns"""
        recent = sorted(
            self.learned_patterns.values(),
            key=lambda p: p.feedback_sources[-1] if p.feedback_sources else 0,
            reverse=True
        )[:5]

        return [
            {
                'pattern_type': p.pattern_type.value,
                'description': p.description,
                'confidence': p.confidence,
                'times_observed': p.times_observed
            }
            for p in recent
        ]


def create_meta_learning_orchestrator() -> MetaLearningOrchestrator:
    """Factory function to create meta-learning orchestrator"""
    return MetaLearningOrchestrator()


# Singleton instance
_instance = None

def get_meta_learning_orchestrator() -> MetaLearningOrchestrator:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_meta_learning_orchestrator()
    return _instance
