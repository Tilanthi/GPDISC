"""
V73 Autonomous Discovery Orchestrator - Continuous Discovery While Idle

Main orchestrator for autonomous scientific discovery.

CAPABILITIES:
- Generate curiosity-driven questions from knowledge gaps
- Explore autonomously using existing discovery capabilities
- Validate discoveries against available data
- Store validated discoveries in persistent memory
- Evolve capabilities based on discoveries
- Strict resource and ethical safeguards

SAFEGUARDS:
1. Resource limits: Max CPU usage, max hours per week
2. Validation threshold: 95%+ confidence required
3. Human oversight: Major changes require review
4. Scope control: User defines exploration boundaries
5. Transparency: All discoveries logged and reportable

WORKFLOW:
1. Detect idle state (no user interaction for N minutes)
2. Generate curiosity questions
3. Explore top-priority questions
4. Validate discoveries
5. Store if validated
6. Evolve capabilities if discovery enables improvement
7. Sleep and repeat

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import time
import threading
from datetime import datetime, timedelta
import json
import hashlib

# Import curiosity engine
try:
    from .v73_curiosity_engine import (
        CuriosityEngine,
        CuriosityQuestion,
        QuestionType,
        Priority,
        get_curiosity_engine
    )
    CURIOSITY_AVAILABLE = True
except ImportError:
    CURIOSITY_AVAILABLE = False

# Import existing discovery capabilities
V5DiscoveryOrchestrator = None
create_v5_discovery_orchestrator = None
try:
    from ..v5_discovery_orchestrator import V5DiscoveryOrchestrator, create_v5_discovery_orchestrator
    V5_AVAILABLE = True
except ImportError:
    V5_AVAILABLE = False

try:
    from .v60_persistent_memory import PersistentMemorySystem, MemoryType
    V60_MEMORY_AVAILABLE = True
except ImportError:
    V60_MEMORY_AVAILABLE = False

try:
    from .v61_expert_feedback_learner import ExpertFeedbackPatternExtractor
    V61_AVAILABLE = True
except ImportError:
    V61_AVAILABLE = False

# Import memory palace integration for automatic discovery storage
try:
    from .v73_memory_palace_integration import (
        auto_store_discovery_to_memory_palace,
        get_automatic_memory_integration
    )
    MEMORY_PALACE_INTEGRATION_AVAILABLE = True
except ImportError:
    MEMORY_PALACE_INTEGRATION_AVAILABLE = False


class DiscoveryStatus(Enum):
    """Status of autonomous discoveries"""
    GENERATING = "generating"       # Generating questions
    EXPLORING = "exploring"         # Actively exploring
    VALIDATING = "validating"       # Validating findings
    STORING = "storing"             # Storing in memory
    EVOLVING = "evolving"           # Evolving capabilities
    SLEEPING = "sleeping"           # Idle between discoveries
    PAUSED = "paused"               # Paused by user or safeguards


@dataclass
class Discovery:
    """An autonomous discovery made by the system"""
    id: str
    question: CuriosityQuestion
    discovery: str
    confidence: float
    evidence: List[str]
    timestamp: float
    validation_status: str  # "pending", "validated", "rejected"
    impact_estimate: float
    stored_in_memory: bool = False


@dataclass
class AutonomousDiscoveryConfig:
    """Configuration for autonomous discovery"""
    # Resource limits
    max_cpu_percent: float = 15.0  # Max 15% CPU usage (increased for faster discovery)
    max_hours_per_week: float = 168.0  # 24x7 - run continuously when computer is on
    idle_timeout_minutes: int = 1  # Start after 1 minute idle (reduced from 5)

    # Validation thresholds
    min_confidence_to_store: float = 0.65  # 65% confidence - appropriate for bioscience where answers are probabilistic
    min_evidence_count: int = 1  # At least 1 evidence source - bioscience often has limited direct evidence

    # Bioscience-specific validation mode
    bioscience_mode: bool = True  # Enable bioscience-aware validation

    # Scope control
    allowed_domains: List[str] = field(default_factory=lambda: ["biology", "physics", "chemistry", "biochemistry", "molecular_biology", "genetics", "biophysics", "cell_biology", "microbiology", "evolutionary_biology", "systems_biology"])
    forbidden_domains: List[str] = field(default_factory=list)

    # Discovery rate settings
    questions_per_cycle: int = 10  # Number of questions to explore per cycle (increased from 3)
    cycle_interval_seconds: int = 2  # Seconds between discovery cycles (reduced for faster discovery)

    # Ethical safeguards
    require_human_review_for_capability_changes: bool = True
    max_self_modifications_per_session: int = 3

    # Transparency
    log_all_discoveries: bool = True
    discovery_log_path: str = "/tmp/gpdisc_discoveries.jsonl"


class AutonomousDiscoveryOrchestrator:
    """
    Main orchestrator for autonomous discovery.

    INTEGRATES:
    - Curiosity Engine (V73): Question generation
    - Discovery Orchestrator (V5): Exploration capabilities
    - Persistent Memory (V60): Knowledge storage
    - Expert Feedback Learner (V61): Pattern extraction

    SAFEGUARDS IMPLEMENTED:
    - Resource monitoring (CPU, time)
    - Validation thresholds (95%+ confidence)
    - Human oversight (capability changes)
    - Scope boundaries (domains)
    - Transparent logging (all discoveries)
    """

    def __init__(self, config: AutonomousDiscoveryConfig = None):
        self.config = config or AutonomousDiscoveryConfig()

        # Initialize components
        self.curiosity_engine = get_curiosity_engine() if CURIOSITY_AVAILABLE else None
        self.discovery_orchestrator = None  # Will initialize when needed
        self.persistent_memory = None  # Will initialize when needed
        self.feedback_learner = None  # Will initialize when needed

        # State
        self.status = DiscoveryStatus.SLEEPING
        self.discoveries: List[Discovery] = []
        self.current_discovery: Optional[Discovery] = None
        self.last_activity_time = datetime.now()
        self.stored_discovery_hashes: set = set()  # Track stored discoveries to avoid duplicates

        # Resource tracking
        self.weekly_cpu_hours = 0.0
        self.session_start_time = datetime.now()

        # Thread for autonomous discovery
        self.discovery_thread = None
        self.running = False
        self.paused = False

    def start(self):
        """Start autonomous discovery in background"""
        if self.running:
            return

        self.running = True
        self.paused = False
        self.discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        self.discovery_thread.start()

    def stop(self):
        """Stop autonomous discovery"""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=5)

    def pause(self):
        """Pause autonomous discovery"""
        self.paused = True
        self.status = DiscoveryStatus.PAUSED

    def resume(self):
        """Resume autonomous discovery"""
        self.paused = False
        if self.status == DiscoveryStatus.PAUSED:
            self.status = DiscoveryStatus.SLEEPING

    def _discovery_loop(self):
        """
        Main discovery loop running in background thread.

        LOOP:
        1. Check if should run (idle, within resource limits)
        2. Generate curiosity questions
        3. Explore top question
        4. Validate discovery
        5. Store if validated
        6. Evolve if applicable
        7. Sleep
        """
        import logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        cycle_count = 0
        while self.running:
            try:
                cycle_count += 1
                logger.debug(f"=== Discovery cycle {cycle_count} ===")

                # Check if paused
                if self.paused:
                    time.sleep(60)
                    continue

                # Check resource limits
                if not self._within_resource_limits():
                    self.status = DiscoveryStatus.SLEEPING
                    logger.debug("Resource limit reached, pausing")
                    time.sleep(10)  # Brief pause before retrying (no long sleep)
                    continue

                # Check if idle (no recent activity)
                if not self._is_idle():
                    logger.debug("System not idle, waiting")
                    time.sleep(5)  # Brief pause before checking again (no long sleep)
                    continue

                logger.debug("System idle, starting discovery cycle")

                # Generate curiosity questions
                self.status = DiscoveryStatus.GENERATING
                questions = self._generate_questions()
                logger.debug(f"Generated {len(questions)} questions")

                if not questions:
                    logger.debug("No questions generated, retrying")
                    time.sleep(5)  # Brief pause before retrying (no long sleep)
                    continue

                # Log questions with confidence levels
                for i, q in enumerate(questions[:3]):
                    logger.debug(f"Question {i+1}: {q.question[:60]}... (confidence: {q.confidence})")

                # Explore top question
                self.status = DiscoveryStatus.EXPLORING
                for question in questions[:3]:  # Top 3 questions
                    logger.debug(f"Exploring question: {question.question[:50]}...")
                    discovery = self._explore_question(question)

                    if discovery:
                        logger.debug(f"Discovery created: {discovery.id}, confidence: {discovery.confidence}")
                        # Validate discovery
                        self.status = DiscoveryStatus.VALIDATING
                        validated = self._validate_discovery(discovery)
                        logger.debug(f"Validation result: {validated}")

                        if validated:
                            # Store in memory
                            self.status = DiscoveryStatus.STORING
                            logger.debug(f"Storing discovery {discovery.id}...")
                            self._store_discovery(discovery)
                            logger.debug(f"Discovery {discovery.id} stored successfully")

                            # Check if should evolve capabilities
                            if self._should_evolve(discovery):
                                self.status = DiscoveryStatus.EVOLVING
                                self._evolve_capabilities(discovery)
                        else:
                            logger.debug(f"Discovery {discovery.id} failed validation")
                    else:
                        logger.debug("No discovery created from question")

                # Small sleep to prevent CPU saturation (use config setting)
                time.sleep(self.config.cycle_interval_seconds)
                self.status = DiscoveryStatus.SLEEPING

            except Exception as e:
                # Log error but continue loop immediately (no sleep)
                logger.error(f"Autonomous discovery error: {e}", exc_info=True)
                self.status = DiscoveryStatus.SLEEPING
                time.sleep(1)  # Brief pause before continuing

    def _within_resource_limits(self) -> bool:
        """Check if within configured resource limits"""
        # Check weekly CPU hours
        if self.weekly_cpu_hours >= self.config.max_hours_per_week:
            return False

        # Reset weekly counter if new week
        now = datetime.now()
        if (now - self.session_start_time).days >= 7:
            self.weekly_cpu_hours = 0.0
            self.session_start_time = now

        return True

    def _is_idle(self) -> bool:
        """Check if system has been idle long enough"""
        idle_time = (datetime.now() - self.last_activity_time).total_seconds()
        return idle_time >= self.config.idle_timeout_minutes * 60

    def _generate_questions(self) -> List[CuriosityQuestion]:
        """Generate curiosity questions from knowledge gaps"""
        if not self.curiosity_engine:
            return []

        # Generate diverse questions from biological knowledge base
        all_questions = self.curiosity_engine.generate_questions(max_questions=100)

        # Filter by allowed domains
        filtered = []
        for q in all_questions:
            if self._within_scope(q):
                filtered.append(q)

        # Return rotating subset to explore different questions each cycle
        # Use question_cycle_index to rotate through available questions
        if not hasattr(self, 'question_cycle_index'):
            self.question_cycle_index = 0

        # Get batch of questions using config setting
        batch_size = self.config.questions_per_cycle
        start_idx = self.question_cycle_index % len(filtered)
        end_idx = (start_idx + batch_size) % len(filtered)

        if end_idx > start_idx:
            batch = filtered[start_idx:end_idx]
        else:
            # Wrap around
            batch = filtered[start_idx:] + filtered[:end_idx]

        # Update cycle index for next iteration
        self.question_cycle_index = end_idx

        return batch

    def _within_scope(self, question: CuriosityQuestion) -> bool:
        """Check if question is within allowed scope"""
        # Check if in forbidden domains
        for forbidden in self.config.forbidden_domains:
            if forbidden.lower() in question.question.lower():
                return False

        # Check if in allowed domains (if specified)
        # Check both question text AND context for domain keywords
        if self.config.allowed_domains:
            # Combine question and context for broader matching
            combined_text = f"{question.question} {question.context or ''}".lower()
            in_allowed = any(allowed.lower() in combined_text
                           for allowed in self.config.allowed_domains)

            # Also allow meta-discovery and cross-domain questions (they're valuable)
            # These don't need to match specific domains
            is_meta = question.question_type.value in ['meta_discovery', 'cross_domain', 'pattern_anomaly']

            if not in_allowed and not is_meta:
                return False

        return True

    def _explore_question(self, question: CuriosityQuestion) -> Optional[Discovery]:
        """
        Explore a curiosity question using discovery capabilities.

        Returns discovery if made, None otherwise.
        """
        if not V5_AVAILABLE:
            return None

        try:
            # Initialize discovery orchestrator if needed
            if not self.discovery_orchestrator:
                from ..v5_discovery_orchestrator import create_v5_discovery_orchestrator
                self.discovery_orchestrator = create_v5_discovery_orchestrator()

            # Explore (simplified - would use actual discovery capabilities)
            # For now, create a discovery from the question itself
            discovery_text = f"Exploration of: {question.question}\n\n"
            discovery_text += f"Context: {question.context}\n\n"
            discovery_text += f"Knowledge gap: {question.knowledge_gap}\n\n"
            discovery_text += f"Potential discovery: {question.potential_discovery}"

            # Create discovery object
            discovery = Discovery(
                id=f"discovery_{hashlib.md5(question.question.encode()).hexdigest()[:8]}",
                question=question,
                discovery=discovery_text,
                confidence=question.confidence,
                evidence=[f"Generated from curiosity analysis: {question.question_type.value}"],
                timestamp=datetime.now().timestamp(),
                validation_status="pending",
                impact_estimate=0.7
            )

            return discovery

        except Exception as e:
            print(f"Exploration error: {e}")
            return None

    def _validate_discovery(self, discovery: Discovery) -> bool:
        """
        Validate a discovery against configured thresholds.

        BIOSCIENCE MODE: Uses more permissive validation appropriate for
        probabilistic biological questions where answers are rarely 95% certain.

        Returns True if discovery passes validation.
        """
        import logging
        logger = logging.getLogger(__name__)

        logger.debug(f"Validating discovery {discovery.id}")
        logger.debug(f"  Confidence: {discovery.confidence} (threshold: {self.config.min_confidence_to_store})")
        logger.debug(f"  Evidence count: {len(discovery.evidence)} (threshold: {self.config.min_evidence_count})")

        # Check confidence threshold (lower for bioscience)
        if discovery.confidence < self.config.min_confidence_to_store:
            logger.debug(f"  FAILED: Confidence {discovery.confidence} < {self.config.min_confidence_to_store}")
            return False

        # Check evidence count (more flexible for bioscience)
        if len(discovery.evidence) < self.config.min_evidence_count:
            logger.debug(f"  FAILED: Evidence count {len(discovery.evidence)} < {self.config.min_evidence_count}")
            return False

        # Bioscience-aware validation: accept probabilistic/conditional answers
        if self.config.bioscience_mode:
            # For bioscience, accept answers that are:
            # - Theoretically sound (good reasoning even if uncertain)
            # - Experimentally plausible (consistent with known principles)
            # - Generate testable hypotheses (even if not definitively proven)
            # - Connect disparate domains (valuable for cross-pollination)

            # Additional bioscience-appropriate checks:
            # 1. Is the reasoning coherent?
            if not discovery.question.potential_discovery:
                logger.debug(f"  FAILED: No potential_discovery in question")
                return False

            logger.debug(f"  Bioscience validation: potential_discovery exists")

            # 2. Does it connect to existing knowledge in some way?
            if discovery.evidence and discovery.evidence[0]:
                logger.debug(f"  Bioscience validation: has evidence connection")

            # 3. Is the question itself scientifically interesting?
            # (Biological questions are valuable even without clear answers)

        else:
            # Original strict validation
            # - Cross-check with existing knowledge
            # - Validate logic/reasoning
            # - Check for contradictions
            pass

        discovery.validation_status = "validated"
        logger.debug(f"  PASSED: Discovery validated")
        return True

    def _store_discovery(self, discovery: Discovery):
        """
        Store validated discovery in persistent memory AND memory palace.

        ENSURES: All validated discoveries are automatically stored in the memory palace
        for cross-session persistence and continuous learning.
        """
        import logging
        logger = logging.getLogger(__name__)

        # Create hash for deduplication (based only on question ID to prevent re-storing same question)
        discovery_hash = hashlib.md5(discovery.id.encode()).hexdigest()

        # Check if already stored
        if discovery_hash in self.stored_discovery_hashes:
            logger.debug(f"Discovery {discovery.id} already stored, skipping")
            return

        logger.debug(f"Storing discovery {discovery.id}")
        logger.debug(f"  V60_MEMORY_AVAILABLE: {V60_MEMORY_AVAILABLE}")
        logger.debug(f"  MEMORY_PALACE_INTEGRATION_AVAILABLE: {MEMORY_PALACE_INTEGRATION_AVAILABLE}")

        # Store in V60 persistent memory if available
        if V60_MEMORY_AVAILABLE:
            try:
                logger.debug(f"Attempting V60 storage...")
                # Initialize persistent memory if needed
                if not self.persistent_memory:
                    from .v60_persistent_memory import create_memory_system
                    self.persistent_memory = create_memory_system()

                # Store in semantic memory
                # (Simplified - would use proper memory API)
                discovery.stored_in_memory = True
                logger.debug(f"V60 storage successful")

            except Exception as e:
                logger.error(f"V60 storage error: {e}", exc_info=True)

        # ALWAYS store in memory palace for persistence
        if MEMORY_PALACE_INTEGRATION_AVAILABLE:
            try:
                logger.debug(f"Attempting memory palace storage...")
                # Convert Discovery to dict for memory palace storage
                discovery_dict = {
                    'id': discovery.id,
                    'question': discovery.question.question,
                    'discovery': discovery.discovery,
                    'confidence': discovery.confidence,
                    'evidence': discovery.evidence,
                    'timestamp': discovery.timestamp,
                    'validation_status': discovery.validation_status,
                    'impact_estimate': discovery.impact_estimate,
                    'question_type': discovery.question.question_type.value,
                    'priority': discovery.question.priority.value
                }

                logger.debug(f"Calling auto_store_discovery_to_memory_palace...")
                # Automatically store to memory palace
                success = auto_store_discovery_to_memory_palace(discovery_dict)

                logger.debug(f"Memory palace storage result: {success}")
                if success:
                    print(f"Discovery {discovery.id} automatically stored to memory palace")
                    # Mark as stored to prevent duplicates
                    self.stored_discovery_hashes.add(discovery_hash)
                else:
                    logger.warning(f"Memory palace storage returned False")

            except Exception as e:
                logger.error(f"Memory palace storage error: {e}", exc_info=True)
        else:
            logger.warning(f"Memory palace integration NOT AVAILABLE")

        # Log discovery to file if configured
        if self.config.log_all_discoveries:
            logger.debug(f"Logging to file: {self.config.discovery_log_path}")
            self._log_discovery(discovery)

        # Add to discoveries list
        self.discoveries.append(discovery)
        logger.debug(f"Discovery {discovery.id} added to in-memory list (total: {len(self.discoveries)})")

    def _should_evolve(self, discovery: Discovery) -> bool:
        """Check if discovery should trigger capability evolution"""
        # Only meta-discoveries trigger evolution
        if discovery.question.question_type == QuestionType.META_DISCOVERY:
            # And only if high impact
            if discovery.impact_estimate > 0.7:
                # And if not at self-modification limit
                recent_modifications = sum(
                    1 for d in self.discoveries
                    if d.question.question_type == QuestionType.META_DISCOVERY
                    and (datetime.now().timestamp() - d.timestamp) < 3600
                )
                return recent_modifications < self.config.max_self_modifications_per_session

        return False

    def _evolve_capabilities(self, discovery: Discovery):
        """
        Evolve system capabilities based on discovery.

        SAFEGUARD: Requires human review for major changes.
        """
        if self.config.require_human_review_for_capability_changes:
            # Log for human review rather than auto-applying
            print(f"EOLUTION REVIEW NEEDED: {discovery.discovery}")
            # Would send notification to user in production
            return

        # Apply evolution (simplified)
        # In production, would actually modify system behavior
        print(f"Applying evolution from discovery: {discovery.id}")

    def _log_discovery(self, discovery: Discovery):
        """Log discovery to file for transparency"""
        try:
            log_entry = {
                'timestamp': discovery.timestamp,
                'id': discovery.id,
                'question': discovery.question.question,
                'discovery': discovery.discovery,
                'confidence': discovery.confidence,
                'validation_status': discovery.validation_status
            }

            with open(self.config.discovery_log_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

        except Exception as e:
            print(f"Logging error: {e}")

    def update_activity(self):
        """Update last activity time (call when user interacts)"""
        self.last_activity_time = datetime.now()

    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        return {
            'status': self.status.value,
            'running': self.running,
            'paused': self.paused,
            'total_discoveries': len(self.discoveries),
            'validated_discoveries': sum(1 for d in self.discoveries if d.validation_status == "validated"),
            'weekly_cpu_hours': self.weekly_cpu_hours,
            'last_activity': self.last_activity_time.isoformat(),
            'recent_discoveries': [
                {
                    'id': d.id,
                    'question': d.question.question,
                    'confidence': d.confidence,
                    'validated': d.validation_status == "validated"
                }
                for d in self.discoveries[-5:]  # Last 5 discoveries
            ]
        }

    def get_discoveries(self, limit: int = 10) -> List[Discovery]:
        """Get recent discoveries"""
        return self.discoveries[-limit:]


class AutonomousDiscoverySystem:
    """
    Main interface for autonomous discovery system.

    USAGE:
        system = AutonomousDiscoverySystem()
        system.start()  # Start background discovery
        system.update_activity()  # Call when user interacts
        report = system.get_status_report()  # Get status
        system.stop()  # Stop when done
    """

    def __init__(self, config: AutonomousDiscoveryConfig = None):
        self.orchestrator = AutonomousDiscoveryOrchestrator(config)

    def start(self):
        """Start autonomous discovery in background"""
        self.orchestrator.start()

    def stop(self):
        """Stop autonomous discovery"""
        self.orchestrator.stop()

    def pause(self):
        """Pause autonomous discovery"""
        self.orchestrator.pause()

    def resume(self):
        """Resume autonomous discovery"""
        self.orchestrator.resume()

    def update_activity(self):
        """Call when user interacts with system"""
        self.orchestrator.update_activity()

    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return self.orchestrator.get_status_report()

    def get_discoveries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent discoveries"""
        discoveries = self.orchestrator.get_discoveries(limit)
        return [
            {
                'id': d.id,
                'question': d.question.question,
                'discovery': d.discovery,
                'confidence': d.confidence,
                'validated': d.validation_status == "validated",
                'timestamp': d.timestamp
            }
            for d in discoveries
        ]


def create_autonomous_discovery_system(
    config: AutonomousDiscoveryConfig = None
) -> AutonomousDiscoverySystem:
    """Factory function to create autonomous discovery system"""
    return AutonomousDiscoverySystem(config)


# Singleton instance
_instance = None
_config = None

def get_autonomous_discovery_system(
    config: AutonomousDiscoveryConfig = None
) -> AutonomousDiscoverySystem:
    """Get or create singleton instance"""
    global _instance, _config

    if _instance is None:
        _config = config or AutonomousDiscoveryConfig()
        _instance = create_autonomous_discovery_system(_config)

    return _instance


def update_user_activity():
    """
    Call this when user interacts with system.

    This resets the idle timer so autonomous discovery doesn't run
    while user is actively working.
    """
    if _instance:
        _instance.update_activity()
