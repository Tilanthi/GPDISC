"""
V61 Expert Feedback Learner - Meta-Learning from Domain Expertise

This module implements meta-learning capabilities specifically designed to
extract patterns from domain expert feedback and use them to improve future
performance.

CAPABILITIES:
- Extract attention patterns from expert feedback (what experts notice that I missed)
- Detect blind spots in domain-specific reasoning
- Update default heuristics based on learned patterns
- Integrate with V60 CognitiveSelfModification for continuous improvement

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
import numpy as np
from datetime import datetime
import json
import hashlib

class PatternType(Enum):
    """Types of patterns that can be extracted from expert feedback"""
    MISSING_CONNECTION = "missing_connection"      # Expert saw connection I missed
    CONCEPTUAL_REFRAME = "conceptual_reframe"       # Expert reframed concept
    WORKED_EXAMPLE_NEEDED = "worked_example_needed" # Expert wanted concrete calculation
    EVOLUTIONARY_CONTEXT = "evolutionary_context"   # Expert added origins perspective
    CITATION_INTEGRITY = "citation_integrity"       # Citation/formatting error
    DOMAIN_BRIDGE = "domain_bridge"                 # Physics-biology etc integration


class BlindSpotCategory(Enum):
    """Categories of blind spots"""
    FUNDAMENTAL_BIOLOGY = "fundamental_biology"     # L-forms, etc
    PHYSICS_CHEMISTRY = "physics_chemistry"         # Cholesteric DNA, etc
    EVOLUTIONARY_THINKING = "evolutionary_thinking" # Origins perspective
    QUANTITATIVE_RIGOR = "quantitative_rigor"       # Worked examples, calculations
    CITATION_ACCURACY = "citation_accuracy"         # Reference integrity


@dataclass
class ExpertFeedback:
    """A piece of feedback from a domain expert"""
    id: str
    timestamp: float
    domain: str
    feedback_text: str
    context: Dict[str, Any]  # What was I working on
    severity: float  # 0-1, how critical
    category: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


@dataclass
class ExtractedPattern:
    """A pattern extracted from expert feedback"""
    id: str
    pattern_type: PatternType
    description: str
    trigger_conditions: List[str]  # When to apply this pattern
    corrective_action: str  # What to do differently
    confidence: float  # How confident in this pattern
    feedback_sources: List[str]  # Which feedback items generated this
    times_observed: int = 1

    def strengthen(self):
        """Strengthen pattern confidence based on repeated observation"""
        self.times_observed += 1
        self.confidence = min(1.0, self.confidence + 0.1)


@dataclass
class BlindSpot:
    """A systematic blind spot identified from feedback"""
    id: str
    category: BlindSpotCategory
    description: str
    examples: List[str]  # Specific instances where this occurred
    detection_heuristic: str  # How to detect this in future
    mitigation_strategy: str  # How to avoid this blind spot


class ExpertFeedbackPatternExtractor:
    """
    Extract reusable patterns from domain expert feedback.

    LEARNED PATTERNS (from bacterial cell cycle review):
    1. "Missing physical-chemical mechanisms" → Look for fundamental physics constraints
    2. "Add evolutionary context" → Trace back to origins, show selective advantage
    3. "Give worked example" → Actual numbers, step-by-step, interpretation
    4. "Reframe conceptual distinction" → Check for teleological framing, revise terminology
    """

    def __init__(self):
        self.patterns: Dict[str, ExtractedPattern] = {}
        self.blind_spots: Dict[str, BlindSpot] = {}
        self.feedback_history: List[ExpertFeedback] = []
        self.domain_expertise_profiles: Dict[str, Set[str]] = {}

    def extract_patterns(self, feedback: List[ExpertFeedback]) -> List[ExtractedPattern]:
        """
        Extract reusable patterns from expert feedback.

        Returns patterns that can be applied to future tasks to avoid
        making the same mistakes.
        """
        extracted = []

        for fb in feedback:
            # Pattern 1: Missing physical-chemical mechanisms
            if any(term in fb.feedback_text.lower() for term in
                   ['physical', 'chemical', 'mechanism', 'constraint', 'fundamental']):
                pattern = ExtractedPattern(
                    id=f"phys_chem_mechanism_{hash(fb.feedback_text) % 10000}",
                    pattern_type=PatternType.MISSING_CONNECTION,
                    description="Expert pointed out missing physical-chemical mechanisms",
                    trigger_conditions=[
                        "Task involves biological regulation",
                        "No explicit discussion of physical constraints",
                        "No mention of membrane physics, DNA topology, thermodynamics, etc"
                    ],
                    corrective_action="Add section on fundamental physical constraints: "
                                    "DNA topology, membrane physics, thermodynamic constraints, "
                                    "macromolecular crowding, polyelectrolyte effects",
                    confidence=0.7,
                    feedback_sources=[fb.id]
                )
                extracted.append(pattern)

            # Pattern 2: Evolutionary context needed
            if any(term in fb.feedback_text.lower() for term in
                   ['evolution', 'origins', 'ancestral', 'luca', 'deep time', 'selective advantage']):
                pattern = ExtractedPattern(
                    id=f"evolutionary_context_{hash(fb.feedback_text) % 10000}",
                    pattern_type=PatternType.EVOLUTIONARY_CONTEXT,
                    description="Expert requested evolutionary/origins perspective",
                    trigger_conditions=[
                        "Biological question without evolutionary framing",
                        "No discussion of how mechanism evolved",
                        "No mention of selective advantage or ancestral state"
                    ],
                    corrective_action="Reframe with origins-first perspective: "
                                    "What physical constraints existed before molecular regulation? "
                                    "What selective advantages favored increasing complexity? "
                                    "What does this reveal about early cellular evolution?",
                    confidence=0.8,
                    feedback_sources=[fb.id]
                )
                extracted.append(pattern)

            # Pattern 3: Worked example needed
            if any(term in fb.feedback_text.lower() for term in
                   ['worked example', 'calculation', 'show me numbers', 'step by step', 'compute']):
                pattern = ExtractedPattern(
                    id=f"worked_example_{hash(fb.feedback_text) % 10000}",
                    pattern_type=PatternType.WORKED_EXAMPLE_NEEDED,
                    description="Expert requested concrete worked example with calculations",
                    trigger_conditions=[
                        "Introduced quantitative metric or formula",
                        "No concrete numerical example provided",
                        "Abstract discussion without instantiation"
                    ],
                    corrective_action="Provide complete worked example: "
                                    "Define experimental setup, give hypothetical data, "
                                    "show step-by-step calculation, interpret result",
                    confidence=0.9,
                    feedback_sources=[fb.id]
                )
                extracted.append(pattern)

            # Pattern 4: Conceptual reframing needed
            if any(term in fb.feedback_text.lower() for term in
                   ['reframe', 'not quite right', 'teleological', 'precision vs robustness']):
                pattern = ExtractedPattern(
                    id=f"conceptual_reframe_{hash(fb.feedback_text) % 10000}",
                    pattern_type=PatternType.CONCEPTUAL_REFRAME,
                    description="Expert requested conceptual reframing",
                    trigger_conditions=[
                        "Using terminology that implies purpose or design",
                        "Binary distinctions that should be nuanced",
                        "Concepts that could be framed more precisely"
                    ],
                    corrective_action="Check for teleological framing (avoid 'in order to', 'designed to'), "
                                    "use precise terminology (precision, accuracy, reproducibility), "
                                    "avoid false binaries",
                    confidence=0.75,
                    feedback_sources=[fb.id]
                )
                extracted.append(pattern)

        # Merge with existing patterns
        for pattern in extracted:
            if pattern.id in self.patterns:
                self.patterns[pattern.id].strengthen()
                self.patterns[pattern.id].feedback_sources.extend(pattern.feedback_sources)
            else:
                self.patterns[pattern.id] = pattern

        return extracted

    def detect_blind_spots(self, feedback: List[ExpertFeedback]) -> List[BlindSpot]:
        """
        Identify systematic blind spots from expert feedback.

        A blind spot is a category of error that occurs repeatedly across
        different tasks, indicating a gap in domain knowledge or reasoning.
        """
        blind_spots = []

        # Blind Spot 1: Fundamental biology gaps
        fundamental_biology_feedback = [
            fb for fb in feedback
            if any(term in fb.feedback_text.lower() for term in
                   ['l-form', 'cholesteric', 'liquid crystal', 'woldringh', 'bouligand'])
        ]
        if fundamental_biology_feedback:
            blind_spot = BlindSpot(
                id="fundamental_biology_gaps",
                category=BlindSpotCategory.FUNDAMENTAL_BIOLOGY,
                description="Missing fundamental biological mechanisms that experts consider obvious",
                examples=[
                    "L-forms as evidence for Type C physical-default organization",
                    "Cholesteric DNA organization and liquid crystalline phases",
                    "Woldringh's 'four-excluding arms' model for segregation"
                ],
                detection_heuristic="Check for: alternative division systems, "
                                   "non-molecular mechanisms, physical organization of biomolecules",
                mitigation_strategy="Before finalizing biological analysis, explicitly ask: "
                                  "What physical mechanisms exist beyond molecular regulation? "
                                  "Are there alternative systems (L-forms, archaea) that reveal defaults?"
            )
            blind_spots.append(blind_spot)

        # Blind Spot 2: Physics-chemistry integration gaps
        physics_chemistry_feedback = [
            fb for fb in feedback
            if any(term in fb.feedback_text.lower() for term in
                   ['membrane physics', 'polyelectrolyte', 'reptation', 'liquid crystal'])
        ]
        if physics_chemistry_feedback:
            blind_spot = BlindSpot(
                id="physics_chemistry_integration_gaps",
                category=BlindSpotCategory.PHYSICS_CHEMISTRY,
                description="Missing physics-chemistry mechanisms that constrain biological processes",
                examples=[
                    "Membrane physics (lateral/transverse asymmetry) affecting division",
                    "Polyelectrolyte theory and DNA reptation",
                    "Biomolecular condensates and phase separation"
                ],
                detection_heuristic="Check for: fundamental physical constraints, "
                                   "thermodynamic limits, physical organization",
                mitigation_strategy="Ask: What physical constraints exist independent of molecular systems? "
                                  "How do fundamental physics and chemistry limit what's possible?"
            )
            blind_spots.append(blind_spot)

        # Blind Spot 3: Evolutionary thinking gaps
        evolutionary_feedback = [
            fb for fb in feedback
            if any(term in fb.feedback_text.lower() for term in
                   ['evolution', 'origins', 'ancestral', 'selective advantage'])
        ]
        if evolutionary_feedback:
            blind_spot = BlindSpot(
                id="evolutionary_thinking_gaps",
                category=BlindSpotCategory.EVOLUTIONARY_THINKING,
                description="Not applying evolutionary/origins perspective by default",
                examples=[
                    "Framing physical vs molecular without evolutionary context",
                    "Not tracing mechanisms back to early cellular evolution",
                    "Missing discussion of selective advantages"
                ],
                detection_heuristic="Check for: biological questions without evolutionary framing, "
                                   "mechanisms without origin stories",
                mitigation_strategy="Default heuristic: For any biological mechanism, ask "
                                  "'How did this evolve from simpler physical processes?' "
                                  "'What selective advantage did it provide?'"
            )
            blind_spots.append(blind_spot)

        # Store blind spots
        for bs in blind_spots:
            self.blind_spots[bs.id] = bs

        return blind_spots

    def update_heuristics(self, patterns: List[ExtractedPattern]) -> None:
        """
        Update default reasoning heuristics based on learned patterns.

        This modifies the agent's default approach to tasks to incorporate
        lessons learned from expert feedback.
        """
        heuristic_updates = {
            PatternType.MISSING_CONNECTION: [
                "ALWAYS ask: What physical-chemical mechanisms constrain this process?",
                "Look for: membrane physics, DNA topology, thermodynamics, macromolecular crowding",
                "Principle: Physical chemistry provides general, low-affinity, inefficient processes"
            ],
            PatternType.EVOLUTIONARY_CONTEXT: [
                "ALWAYS ask: How did this evolve from simpler physical processes?",
                "Look for: selective advantages, ancestral states, LUCA implications",
                "Principle: Apply origins-first framing to biological questions"
            ],
            PatternType.WORKED_EXAMPLE_NEEDED: [
                "When introducing quantitative metrics, ALWAYS provide worked example",
                "Include: experimental setup, hypothetical data, step-by-step calculation, interpretation",
                "Principle: Abstract formulas need concrete instantiation"
            ],
            PatternType.CONCEPTUAL_REFRAME: [
                "Check for teleological framing (avoid 'in order to')",
                "Use precise terminology (precision, accuracy, reproducibility)",
                "Principle: Avoid false binaries, embrace nuanced distinctions"
            ]
        }

        for pattern in patterns:
            if pattern.pattern_type in heuristic_updates:
                # Store heuristics for retrieval during future tasks
                heuristics = heuristic_updates[pattern.pattern_type]
                # These would be integrated into the reasoning system
                # For now, store with the pattern
                pattern.trigger_conditions.extend(heuristics)

    def check_for_blind_spots(self, task_description: str, domain: str) -> List[str]:
        """
        Check if a task triggers any known blind spots.

        Returns warnings about potential blind spots that should be addressed.
        """
        warnings = []

        task_lower = task_description.lower()

        # Check evolutionary thinking blind spot
        if 'biology' in domain.lower() or 'cell' in task_lower or 'organism' in task_lower:
            if 'evolution' not in task_lower and 'origins' not in task_lower:
                if 'evolutionary_thinking_gaps' in self.blind_spots:
                    warnings.append(
                        f"BLIND SPOT WARNING: Biological task without explicit evolutionary framing. "
                        f"Consider: How did this mechanism evolve from simpler processes? "
                        f"What selective advantages favored increasing complexity?"
                    )

        # Check physics-chemistry integration blind spot
        if 'regulation' in task_lower or 'control' in task_lower:
            if 'physical' not in task_lower and 'constraint' not in task_lower:
                if 'physics_chemistry_integration_gaps' in self.blind_spots:
                    warnings.append(
                        f"BLIND SPOT WARNING: Regulatory discussion without physical constraints. "
                        f"Consider: What physical-chemical mechanisms constrain this process? "
                        f"Membrane physics, DNA topology, thermodynamics, etc."
                    )

        return warnings

    def get_relevant_patterns(self, task: Dict[str, Any]) -> List[ExtractedPattern]:
        """
        Get patterns relevant to a given task.

        Task should include domain, description, and other context.
        """
        relevant = []

        for pattern in self.patterns.values():
            # Check if trigger conditions match task
            for condition in pattern.trigger_conditions:
                if condition.lower() in str(task).lower():
                    relevant.append(pattern)
                    break

        # Sort by confidence
        relevant.sort(key=lambda p: p.confidence, reverse=True)

        return relevant


def create_expert_feedback_learner() -> ExpertFeedbackPatternExtractor:
    """Factory function to create expert feedback learner"""
    return ExpertFeedbackPatternExtractor()


# Singleton instance
_instance = None

def get_expert_feedback_learner() -> ExpertFeedbackPatternExtractor:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_expert_feedback_learner()
    return _instance
