"""
Medical Orchestration Harness

Central coordinator for complex medical consultations.
Coordinates task decomposition, tool orchestration, memory management,
and safety oversight for comprehensive medical consultations.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class SubTask:
    """A subtask in a decomposed medical consultation."""
    id: str
    description: str
    domain: str
    priority: int
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed


@dataclass
class ConsultationResult:
    """Complete consultation result with orchestration metadata."""
    answer: str
    confidence: float
    domain: str
    subtasks: List[SubTask] = field(default_factory=list)
    validation_checks: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class MedicalTaskDecomposer:
    """
    Decompose complex medical queries into manageable subtasks.

    Analyzes query complexity and breaks down into:
    - Domain-specific subtasks
    - Multi-specialty coordination needs
    - Diagnostic vs treatment planning
    - Information gathering vs synthesis
    """

    def __init__(self):
        self.domain_keywords = {
            "cardiology": ["chest pain", "ecg", "heart", "blood pressure", "arrhythmia",
                         "cardiac", "coronary", "myocardial", "atrial fibrillation"],
            "epilepsy": ["seizure", "epilepsy", "eeg", "convulsion", "aura",
                        "antiepileptic", "epileptic"],
            "orthopedics": ["fracture", "joint", "bone", "orthopedic", "sports injury",
                           "arthritis", "spine", "knee", "shoulder", "hip"],
            "pharmacology": ["drug", "medication", "interaction", "side effect",
                           "dosage", "pharmacology", "prescription"],
            "general_practice": ["checkup", "symptom", "referral", "triage",
                              "diagnosis", "treatment"]
        }

    def decompose(self, query: str, context: Optional[Dict] = None) -> List[SubTask]:
        """
        Decompose medical query into subtasks.

        Args:
            query: Medical consultation query
            context: Optional patient context

        Returns:
            List of SubTasks
        """
        subtasks = []
        query_lower = query.lower()

        # Identify relevant domains
        domains = self._identify_domains(query)

        # Create subtasks for each domain
        for i, domain in enumerate(domains):
            subtask = SubTask(
                id=f"subtask_{i+1}",
                description=f"Analyze query from {domain} perspective",
                domain=domain,
                priority=self._calculate_priority(domain, query),
                dependencies=[]
            )
            subtasks.append(subtask)

        # Add coordination subtask if multiple domains
        if len(domains) > 1:
            coord_subtask = SubTask(
                id="coordination",
                description="Coordinate multi-specialty recommendations",
                domain="coordination",
                priority=1,
                dependencies=[st.id for st in subtasks]
            )
            subtasks.append(coord_subtask)

        return subtasks

    def _identify_domains(self, query: str) -> List[str]:
        """Identify relevant medical domains for query."""
        query_lower = query.lower()
        identified = []

        for domain, keywords in self.domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                identified.append(domain)

        # Default to general practice if no specific domain identified
        if not identified:
            identified.append("general_practice")

        return identified

    def _calculate_priority(self, domain: str, query: str) -> int:
        """Calculate priority for subtask."""
        # Emergency conditions get highest priority
        emergency_keywords = ["emergency", "urgent", "severe", "critical"]
        if any(kw in query.lower() for kw in emergency_keywords):
            return 1

        # Cardiology and epilepsy get higher priority
        if domain in ["cardiology", "epilepsy"]:
            return 2

        return 3


class ToolCoordinator:
    """
    Coordinate tool execution for medical subtasks.

    Manages:
    - Tool selection based on subtask requirements
    - Parallel execution where possible
    - Result aggregation
    - Error handling and fallback
    """

    def __init__(self, domain_registry: Optional[Dict] = None):
        self.domain_registry = domain_registry or {}
        self.tool_cache = {}

    def execute(self, subtask: SubTask, query: str,
                context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute subtask using appropriate domain tool.

        Args:
            subtask: SubTask to execute
            query: Original medical query
            context: Patient context

        Returns:
            Execution result
        """
        subtask.status = "in_progress"

        try:
            # Get domain module
            domain_module = self._get_domain_module(subtask.domain)

            if domain_module is None:
                return self._handle_missing_domain(subtask)

            # Process query through domain
            result = domain_module.process_query(query, context)

            subtask.status = "completed"

            return {
                "subtask_id": subtask.id,
                "success": True,
                "result": result,
                "domain": subtask.domain,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            subtask.status = "failed"
            return {
                "subtask_id": subtask.id,
                "success": False,
                "error": str(e),
                "domain": subtask.domain,
                "timestamp": datetime.now().isoformat()
            }

    def execute_batch(self, subtasks: List[SubTask], query: str,
                     context: Optional[Dict] = None) -> List[Dict]:
        """Execute multiple subtasks in parallel where possible."""
        results = []

        # Execute independent subtasks in parallel
        for subtask in subtasks:
            if subtask.status == "pending":
                result = self.execute(subtask, query, context)
                results.append(result)

        return results

    def _get_domain_module(self, domain: str):
        """Get domain module from registry."""
        if domain in self.domain_registry:
            return self.domain_registry[domain]
        return None

    def _handle_missing_domain(self, subtask: SubTask) -> Dict[str, Any]:
        """Handle case where domain module is not available."""
        return {
            "subtask_id": subtask.id,
            "success": False,
            "error": f"Domain module '{subtask.domain}' not available",
            "domain": subtask.domain,
            "timestamp": datetime.now().isoformat()
        }


class MedicalOrchestrationHarness:
    """
    Central coordinator for complex medical consultations.

    Coordinates:
    - Task decomposition (multi-specialty consultations)
    - Tool orchestration (diagnostic tools, knowledge bases)
    - Memory management (patient records, medical knowledge)
    - Safety oversight (clinical validation, hallucination detection)

    This is the main entry point for orchestrated medical consultations.
    """

    def __init__(self, domain_registry: Optional[Dict] = None,
                 memory_system: Optional[Any] = None,
                 safety_validator: Optional[Any] = None,
                 confidence_calibrator: Optional[Any] = None):

        self.domain_registry = domain_registry or {}
        self.memory_system = memory_system
        self.task_decomposer = MedicalTaskDecomposer()
        self.tool_coordinator = ToolCoordinator(domain_registry)
        self.safety_validator = safety_validator
        self.confidence_calibrator = confidence_calibrator

    def orchestrate_consultation(self, query: str,
                                 patient_context: Optional[Dict] = None) -> ConsultationResult:
        """
        Orchestrate complete medical consultation.

        Args:
            query: Medical consultation query
            patient_context: Optional patient information and history

        Returns:
            Complete ConsultationResult with safety validation
        """
        start_time = datetime.now()
        patient_context = patient_context or {}

        # 1. Decompose query into subtasks
        subtasks = self.task_decomposer.decompose(query, patient_context)

        # 2. Execute subtasks with appropriate tools
        execution_results = self.tool_coordinator.execute_batch(
            subtasks, query, patient_context
        )

        # 3. Synthesize results
        synthesized = self.synthesize_results(execution_results, query)

        # 4. Validate against medical knowledge base
        if self.safety_validator:
            validation_result = self.safety_validator.validate_consultation(
                synthesized,
                self.confidence_calibrator
            )

            # Update confidence with calibrated value
            synthesized["confidence"] = validation_result.calibrated_confidence
            synthesized["emergency_flag"] = validation_result.emergency_flag

            # Add referral if needed
            if validation_result.specialist_referral:
                synthesized["referral"] = validation_result.specialist_referral
        else:
            validation_result = None

        # 5. Store in memory if available
        if self.memory_system and patient_context.get("patient_id"):
            self._store_consultation_memory(
                query, synthesized, patient_context["patient_id"]
            )

        # 6. Create final result
        result = ConsultationResult(
            answer=synthesized.get("answer", ""),
            confidence=synthesized.get("confidence", 0.5),
            domain=synthesized.get("domain", "general_practice"),
            subtasks=subtasks,
            validation_checks=[check.__dict__ for check in validation_result.checks] if validation_result else [],
            metadata={
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "subtask_results": execution_results,
                "safety_validation": validation_result.__dict__ if validation_result else None,
                "patient_context_provided": bool(patient_context)
            }
        )

        return result

    def synthesize_results(self, execution_results: List[Dict], query: str) -> Dict[str, Any]:
        """
        Synthesize results from multiple subtasks into coherent response.

        Args:
            execution_results: Results from executed subtasks
            query: Original query

        Returns:
            Synthesized consultation result
        """
        successful_results = [r for r in execution_results if r.get("success", False)]

        if not successful_results:
            return {
                "answer": "Unable to process query - no domains available",
                "confidence": 0.0,
                "domain": "none",
                "query": query
            }

        if len(successful_results) == 1:
            # Single domain result
            result = successful_results[0]["result"]
            return {
                "answer": result.get("answer", ""),
                "confidence": result.get("confidence", 0.5),
                "domain": successful_results[0]["domain"],
                "query": query
            }
        else:
            # Multi-domain synthesis
            return self._synthesize_multi_domain(successful_results, query)

    def _synthesize_multi_domain(self, results: List[Dict], query: str) -> Dict[str, Any]:
        """Synthesize results from multiple domains."""
        # Collect answers from each domain
        answers = []
        confidences = []
        domains = []

        for result in results:
            domain_result = result["result"]
            answers.append(f"**{result['domain'].title()} Perspective:**\n{domain_result.get('answer', '')}")
            confidences.append(domain_result.get("confidence", 0.5))
            domains.append(result["domain"])

        # Calculate aggregate confidence
        avg_confidence = sum(confidences) / len(confidences)

        # Format multi-specialty response
        combined_answer = "\n\n".join(answers)

        return {
            "answer": combined_answer,
            "confidence": avg_confidence,
            "domain": "multi_specialty",
            "domains_consulted": domains,
            "query": query
        }

    def _store_consultation_memory(self, query: str, result: Dict, patient_id: str):
        """Store consultation in patient memory."""
        if self.memory_system:
            memory_entry = {
                "query": query,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "patient_id": patient_id
            }

            # Store in appropriate memory system
            try:
                self.memory_system.store_patient_record(patient_id, memory_entry)
            except Exception as e:
                # Log error but don't fail consultation
                print(f"Warning: Could not store in memory: {e}")

    def get_available_domains(self) -> List[str]:
        """Get list of available medical domains."""
        return list(self.domain_registry.keys())

    def register_domain(self, domain_name: str, domain_module: Any):
        """Register a new domain module."""
        self.domain_registry[domain_name] = domain_module
        self.tool_coordinator.domain_registry[domain_name] = domain_module
