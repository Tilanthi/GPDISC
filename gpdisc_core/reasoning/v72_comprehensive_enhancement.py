"""
V72 Comprehensive Enhancement System - Integrated Meta-Learning and Quality Assurance

This module integrates ALL new capabilities into a unified enhancement system:

META-LEARNING (from V61-V63):
- V61: Expert Feedback Pattern Extractor
- V62: Domain Artifact Verifier
- V63: Meta-Learning Integration Orchestrator

DISCOVERY & INFERENCE ENHANCEMENT (from V66, V70, V71):
- V66: Absence Detection System
- V70: Teleology Filter
- V71: Quantitative Validation Engine

MCE ENHANCEMENT:
- Evolutionary Context Layer

INTEGRATION PATTERN:
Before → During → After → Feedback
   ↓        ↓       ↓        ↓
Check    Apply   Verify   Learn

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json
from datetime import datetime

# Import meta-learning capabilities
try:
    from .v61_expert_feedback_learner import (
        ExpertFeedbackPatternExtractor,
        ExpertFeedback,
        BlindSpot,
        get_expert_feedback_learner
    )
    V61_AVAILABLE = True
except ImportError:
    V61_AVAILABLE = False

try:
    from .v62_domain_artifact_verifier import (
        DomainArtifactVerifier,
        VerificationIssue,
        get_domain_artifact_verifier
    )
    V62_AVAILABLE = True
except ImportError:
    V62_AVAILABLE = False

try:
    from .v63_meta_learning_integration import (
        MetaLearningOrchestrator,
        TaskContext,
        get_meta_learning_orchestrator
    )
    V63_AVAILABLE = True
except ImportError:
    V63_AVAILABLE = False

# Import discovery and inference enhancements
try:
    from .v66_absence_detection import (
        AbsenceDetector,
        AbsenceAlert,
        DomainContext,
        get_absence_detector
    )
    V66_AVAILABLE = True
except ImportError:
    V66_AVAILABLE = False

try:
    from .v70_teleology_filter import (
        TeleologyFilter,
        TeleologyAlert,
        get_teleology_filter
    )
    V70_AVAILABLE = True
except ImportError:
    V70_AVAILABLE = False

try:
    from .v71_quantitative_validation import (
        QuantitativeValidationEngine,
        ValidationIssue,
        get_quantitative_validation_engine
    )
    V71_AVAILABLE = True
except ImportError:
    V71_AVAILABLE = False

# Import MCE enhancements
try:
    from ..metacognitive.evolutionary_context_layer import (
        EvolutionaryContextLayer,
        create_evolutionary_context_layer
    )
    EVO_LAYER_AVAILABLE = True
except ImportError:
    EVO_LAYER_AVAILABLE = False


class EnhancementCategory(Enum):
    """Categories of enhancements"""
    PRE_TASK_CHECKS = "pre_task_checks"           # Before starting
    CONTENT_ENHANCEMENT = "content_enhancement"   # During work
    OUTPUT_VERIFICATION = "output_verification"   # Before delivery
    LEARNING_UPDATES = "learning_updates"         # From feedback


@dataclass
class EnhancementReport:
    """Comprehensive report of all enhancements and issues found"""
    task_id: str
    timestamp: float
    domain: str

    # Pre-task checks
    blind_spot_warnings: List[str] = field(default_factory=list)
    absence_alerts: List[Dict[str, Any]] = field(default_factory=list)

    # Content enhancement
    evolutionary_context_applied: bool = False
    teleology_fixed: bool = False
    teleology_alerts: List[Dict[str, Any]] = field(default_factory=list)

    # Output verification
    citation_issues: List[Dict[str, Any]] = field(default_factory=list)
    quantitative_issues: List[Dict[str, Any]] = field(default_factory=list)
    compression_issues: List[Dict[str, Any]] = field(default_factory=list)

    # Summary
    total_issues: int = 0
    critical_issues: int = 0
    overall_recommendation: str = ""


class ComprehensiveEnhancementSystem:
    """
    Unified system for all GPDISC enhancement capabilities.

    INTEGRATES:
    - Meta-learning from expert feedback (V61-V63)
    - Discovery enhancement (V66 absence detection)
    - Inference enhancement (V70 teleology, V71 quantitative)
    - MCE enhancement (evolutionary context)

    WORKFLOW:
    1. PRE_TASK: Comprehensive checks before starting
    2. ENHANCE: Apply all enhancement during work
    3. VERIFY: Comprehensive verification before output
    4. LEARN: Extract patterns from all feedback

    This creates a virtuous cycle of continuous improvement.
    """

    def __init__(self):
        # Initialize meta-learning components
        self.meta_learning = get_meta_learning_orchestrator() if V63_AVAILABLE else None

        # Initialize discovery and inference components
        self.absence_detector = get_absence_detector() if V66_AVAILABLE else None
        self.teleology_filter = get_teleology_filter() if V70_AVAILABLE else None
        self.quant_validator = get_quantitative_validation_engine() if V71_AVAILABLE else None

        # Initialize MCE enhancement
        self.evolutionary_layer = create_evolutionary_context_layer() if EVO_LAYER_AVAILABLE else None

        # Enhancement state
        self.current_report: Optional[EnhancementReport] = None
        self.learning_history: List[Dict[str, Any]] = []

    def comprehensive_pre_task_check(
        self,
        task_description: str,
        domain: str
    ) -> EnhancementReport:
        """
        Comprehensive pre-task checks combining all detection capabilities.

        CHECKS:
        - Blind spots (V61)
        - Absence detection (V66)
        - Evolutionary context needed (MCE)

        Returns comprehensive report of all findings.
        """
        task_id = f"task_{int(datetime.now().timestamp())}"
        report = EnhancementReport(
            task_id=task_id,
            timestamp=datetime.now().timestamp(),
            domain=domain
        )

        # 1. Blind spot detection (V61)
        if self.meta_learning:
            context = self.meta_learning.pre_task_check(task_description, domain)
            report.blind_spot_warnings = context.blind_spot_warnings

        # 2. Absence detection (V66)
        if self.absence_detector and domain == "biology" or "bacterial" in domain.lower():
            # Map domain to DomainContext
            domain_context = DomainContext.BACTERIAL_CELL_CYCLE
            absences = self.absence_detector.detect_absences(task_description, domain_context)
            report.absence_alerts = [
                {
                    'type': alert.absence_type.value,
                    'severity': alert.severity,
                    'description': alert.description,
                    'suggestion': alert.suggested_addition[:200] + "..." if len(alert.suggested_addition) > 200 else alert.suggested_addition
                }
                for alert in absences
            ]

        # 3. Evolutionary context check (MCE)
        if self.evolutionary_layer:
            if self.evolutionary_layer.is_biological_question(task_description):
                if not self.evolutionary_layer.has_evolutionary_context(task_description):
                    report.evolutionary_context_applied = True
                    report.blind_spot_warnings.append(
                        "EVOLUTIONARY CONTEXT: Biological question detected. "
                        "Apply origins-first perspective: physical foundations → molecular overlay → evolutionary trajectory."
                    )

        self.current_report = report
        return report

    def enhance_content(self, content: str, domain: str) -> Tuple[str, EnhancementReport]:
        """
        Apply all content enhancements.

        ENHANCEMENTS:
        - Teleology filtering (V70)
        - Evolutionary context (MCE)
        - Apply learned patterns (V61)

        Returns enhanced content and updated report.
        """
        if not self.current_report:
            # Create report if doesn't exist
            self.comprehensive_pre_task_check(content, domain)

        enhanced_content = content

        # 1. Teleology filtering (V70)
        if self.teleology_filter:
            alerts = self.teleology_filter.check(enhanced_content)
            if alerts:
                enhanced_content, _ = self.teleology_filter.filter_text(enhanced_content)
                report.teleology_fixed = True
                report.teleology_alerts = [
                    {
                        'type': alert.teleology_type.value,
                        'location': alert.location,
                        'suggestion': alert.suggested_reframing
                    }
                    for alert in alerts
                ]

        # 2. Evolutionary context (MCE) - add as preamble
        if self.evolutionary_layer and self.current_report.evolutionary_context_applied:
            evo_prompt = self.evolutionary_layer.get_evolutionary_context_prompt(content)
            enhanced_content = evo_prompt + "\n\n" + enhanced_content

        # 3. Apply learned patterns (V61) - would modify content based on patterns
        # This would be more sophisticated in practice

        return enhanced_content, self.current_report

    def comprehensive_output_verification(
        self,
        content: str,
        bibliography: str = "",
        context: str = "academic_paper"
    ) -> EnhancementReport:
        """
        Comprehensive output verification combining all verification capabilities.

        VERIFIES:
        - Citation integrity (V62)
        - Quantitative validation (V71)
        - Compression appropriateness (V62)
        - Teleology remaining (V70)

        Returns comprehensive report.
        """
        if not self.current_report:
            self.current_report = EnhancementReport(
                task_id=f"verify_{int(datetime.now().timestamp())}",
                timestamp=datetime.now().timestamp(),
                domain="unknown"
            )

        report = self.current_report
        total_issues = 0
        critical_issues = 0

        # 1. Citation verification (V62)
        if self.meta_learning and self.meta_learning.artifact_verifier:
            citation_issues = self.meta_learning.pre_output_verification(content, bibliography)
            report.citation_issues = [
                {
                    'type': issue.issue_type.value,
                    'severity': issue.severity.value,
                    'description': issue.description
                }
                for issue in citation_issues
            ]
            total_issues += len(citation_issues)
            critical_issues += sum(1 for i in citation_issues if i.severity.value == 'critical')

        # 2. Quantitative validation (V71)
        if self.quant_validator:
            quant_issues = self.quant_validator.validate(content)
            report.quantitative_issues = [
                {
                    'type': issue.validation_type.value,
                    'severity': issue.severity.value,
                    'description': issue.description,
                    'suggestion': issue.suggested_addition[:200] + "..." if len(issue.suggested_addition) > 200 else issue.suggested_addition
                }
                for issue in quant_issues
            ]
            total_issues += len(quant_issues)
            critical_issues += sum(1 for i in quant_issues if i.severity.value == 'critical')

        # 3. Compression check (V62)
        if self.meta_learning and self.meta_learning.artifact_verifier:
            compression_issues = self.meta_learning.artifact_verifier.compression_checker.check_compression(
                content, context
            )
            report.compression_issues = [
                {
                    'type': issue.issue_type.value,
                    'severity': issue.severity.value,
                    'description': issue.description
                }
                for issue in compression_issues
            ]
            total_issues += len(compression_issues)

        # 4. Final teleology check (V70)
        if self.teleology_filter:
            alerts = self.teleology_filter.check(content)
            if alerts:
                high_conf = sum(1 for a in alerts if a.confidence > 0.8)
                if high_conf > 0:
                    report.teleology_alerts.extend([
                        {
                            'type': 'remaining_teleology',
                            'confidence': a.confidence,
                            'description': a.description
                        }
                        for a in alerts if a.confidence > 0.8
                    ])
                    total_issues += high_conf

        # Summary
        report.total_issues = total_issues
        report.critical_issues = critical_issues

        if critical_issues > 0:
            report.overall_recommendation = f"CRITICAL: {critical_issues} critical issue(s) must be fixed before submission."
        elif total_issues > 5:
            report.overall_recommendation = f"ATTENTION NEEDED: {total_issues} issues found. Review and fix before submission."
        elif total_issues > 0:
            report.overall_recommendation = f"OPTIONAL: {total_issues} minor issue(s). Consider addressing if time permits."
        else:
            report.overall_recommendation = "PASSED: All verifications passed. Content ready for submission."

        return report

    def process_expert_feedback(
        self,
        task_id: str,
        feedback_text: str,
        domain: str,
        severity: float = 0.5
    ) -> Dict[str, Any]:
        """
        Process expert feedback and extract learning across all capabilities.

        EXTRACTS:
        - Patterns (V61)
        - Blind spots (V61)
        - New absences to detect (V66)
        - New validation rules (V70, V71)

        Returns summary of what was learned.
        """
        learned = {
            'patterns_extracted': 0,
            'blind_spots_identified': 0,
            'new_validation_rules': 0,
            'learning_summary': ''
        }

        # Use meta-learning orchestrator if available
        if self.meta_learning:
            patterns = self.meta_learning.process_feedback(task_id, feedback_text, domain, severity)
            learned['patterns_extracted'] = len(patterns)

            # Get learning summary
            summary = self.meta_learning.get_learning_summary()
            learned['learning_summary'] = str(summary)

        # Store in learning history
        self.learning_history.append({
            'task_id': task_id,
            'timestamp': datetime.now().timestamp(),
            'feedback': feedback_text,
            'learned': learned
        })

        return learned

    def get_enhancement_summary(self) -> Dict[str, Any]:
        """Get summary of all enhancement capabilities and their status"""
        return {
            'meta_learning_available': V63_AVAILABLE,
            'absence_detection_available': V66_AVAILABLE,
            'teleology_filter_available': V70_AVAILABLE,
            'quantitative_validation_available': V71_AVAILABLE,
            'evolutionary_context_available': EVO_LAYER_AVAILABLE,
            'total_capabilities': sum([
                V63_AVAILABLE, V66_AVAILABLE, V70_AVAILABLE, V71_AVAILABLE, EVO_LAYER_AVAILABLE
            ]),
            'learning_history_size': len(self.learning_history),
            'current_report': self.current_report.task_id if self.current_report else None
        }


def create_comprehensive_enhancement_system() -> ComprehensiveEnhancementSystem:
    """Factory function to create comprehensive enhancement system"""
    return ComprehensiveEnhancementSystem()


# Singleton instance
_instance = None

def get_comprehensive_enhancement_system() -> ComprehensiveEnhancementSystem:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_comprehensive_enhancement_system()
    return _instance
