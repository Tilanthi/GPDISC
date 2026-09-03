"""
Medical Context Manager

Manages medical consultation context with memory integration.
Provides context tracking, retrieval, and summarization for consultations.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import json


@dataclass
class ConsultationContext:
    """Context entry for a consultation turn."""
    query: str
    result: Dict[str, Any]
    timestamp: datetime
    patient_id: str
    domain: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PatientSession:
    """Session tracking for patient consultations."""
    patient_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    consultation_count: int = 0
    domains_consulted: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    summary: Optional[str] = None


class MedicalContextManager:
    """
    Manage medical consultation context with memory integration.

    Features:
    - Patient context tracking
    - Conversation history management
    - Relevant knowledge retrieval
    - Context summarization for long consultations
    - Semantic search for relevant past consultations
    """

    def __init__(self, memory_system: Optional[Any] = None, context_window: int = 10):
        self.memory_system = memory_system
        self.context_window = context_window
        self.active_sessions: Dict[str, PatientSession] = {}
        self.context_history: Dict[str, deque] = {}

    def update_context(self, query: str, result: Dict[str, Any], patient_id: str) -> None:
        """
        Update consultation context.

        Args:
            query: Query string
            result: Consultation result
            patient_id: Patient identifier
        """
        # Create context entry
        context_entry = ConsultationContext(
            query=query,
            result=result,
            timestamp=datetime.now(),
            patient_id=patient_id,
            domain=result.get("domain", "unknown"),
            confidence=result.get("confidence", 0.5),
            metadata=result.get("metadata", {})
        )

        # Initialize context history for patient if needed
        if patient_id not in self.context_history:
            self.context_history[patient_id] = deque(maxlen=self.context_window)

        # Add to context history
        self.context_history[patient_id].append(context_entry)

        # Update session
        self._update_session(patient_id, context_entry)

        # Store in long-term memory if available
        if self.memory_system:
            self._store_in_memory(patient_id, context_entry)

    def get_relevant_context(self, query: str, patient_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant consultation context.

        Args:
            query: Current query
            patient_id: Patient identifier

        Returns:
            List of relevant context entries
        """
        relevant_context = []

        # Get recent context from working memory
        recent_context = self._get_recent_context(patient_id)
        relevant_context.extend(recent_context)

        # Get semantically similar context from long-term memory
        if self.memory_system:
            semantic_context = self._get_semantic_context(query, patient_id)
            relevant_context.extend(semantic_context)

        return relevant_context

    def get_patient_session(self, patient_id: str) -> Optional[PatientSession]:
        """
        Get or create patient session.

        Args:
            patient_id: Patient identifier

        Returns:
            PatientSession object
        """
        if patient_id not in self.active_sessions:
            self.active_sessions[patient_id] = PatientSession(
                patient_id=patient_id,
                start_time=datetime.now()
            )

        return self.active_sessions[patient_id]

    def end_session(self, patient_id: str) -> Optional[str]:
        """
        End patient session and generate summary.

        Args:
            patient_id: Patient identifier

        Returns:
            Session summary or None
        """
        if patient_id not in self.active_sessions:
            return None

        session = self.active_sessions[patient_id]
        session.end_time = datetime.now()

        # Generate summary
        summary = self._generate_session_summary(session, patient_id)
        session.summary = summary

        # Store summary in memory
        if self.memory_system:
            self._store_session_summary(patient_id, session)

        return summary

    def summarize_context(self, patient_id: str) -> str:
        """
        Generate consultation summary for patient.

        Args:
            patient_id: Patient identifier

        Returns:
            Consultation summary
        """
        # Get session
        session = self.get_patient_session(patient_id)

        # Get context history
        history = self.context_history.get(patient_id, deque())

        if not history:
            return f"No consultation history for patient {patient_id}"

        # Generate summary
        summary = self._generate_summary_from_history(history, session)

        return summary

    def get_context_window(self, patient_id: str) -> List[ConsultationContext]:
        """
        Get current context window for patient.

        Args:
            patient_id: Patient identifier

        Returns:
            List of recent context entries
        """
        if patient_id not in self.context_history:
            return []

        return list(self.context_history[patient_id])

    def clear_context(self, patient_id: str) -> None:
        """
        Clear context history for patient.

        Args:
            patient_id: Patient identifier
        """
        if patient_id in self.context_history:
            self.context_history[patient_id].clear()

    def _update_session(self, patient_id: str, context_entry: ConsultationContext) -> None:
        """Update patient session with new context entry."""
        session = self.get_patient_session(patient_id)
        session.consultation_count += 1

        # Track domains consulted
        if context_entry.domain not in session.domains_consulted:
            session.domains_consulted.append(context_entry.domain)

        # Extract key findings from result
        key_finding = self._extract_key_finding(context_entry)
        if key_finding:
            session.key_findings.append(key_finding)

    def _get_recent_context(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get recent context from working memory."""
        if patient_id not in self.context_history:
            return []

        recent = list(self.context_history[patient_id])

        return [
            {
                "query": ctx.query,
                "domain": ctx.domain,
                "confidence": ctx.confidence,
                "timestamp": ctx.timestamp.isoformat(),
                "source": "recent_context"
            }
            for ctx in recent
        ]

    def _get_semantic_context(self, query: str, patient_id: str) -> List[Dict[str, Any]]:
        """Get semantically similar context from long-term memory."""
        if not self.memory_system:
            return []

        try:
            # Try semantic search if available
            if hasattr(self.memory_system, 'semantic_search'):
                results = self.memory_system.semantic_search(query, patient_id)

                return [
                    {
                        "query": r.get("query", ""),
                        "domain": r.get("domain", ""),
                        "confidence": r.get("confidence", 0.5),
                        "timestamp": r.get("timestamp", ""),
                        "source": "semantic_search",
                        "similarity": r.get("similarity", 0.0)
                    }
                    for r in results
                ]
        except Exception as e:
            print(f"Warning: Semantic search failed: {e}")

        return []

    def _store_in_memory(self, patient_id: str, context_entry: ConsultationContext) -> None:
        """Store context entry in long-term memory."""
        try:
            memory_data = {
                "query": context_entry.query,
                "result": context_entry.result,
                "domain": context_entry.domain,
                "confidence": context_entry.confidence,
                "timestamp": context_entry.timestamp.isoformat(),
                "patient_id": patient_id
            }

            # Store in memory system
            if hasattr(self.memory_system, 'store_consultation'):
                self.memory_system.store_consultation(patient_id, memory_data)
            elif hasattr(self.memory_system, 'store_patient_record'):
                self.memory_system.store_patient_record(patient_id, memory_data)

        except Exception as e:
            print(f"Warning: Could not store in memory: {e}")

    def _store_session_summary(self, patient_id: str, session: PatientSession) -> None:
        """Store session summary in long-term memory."""
        try:
            summary_data = {
                "patient_id": patient_id,
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "consultation_count": session.consultation_count,
                "domains_consulted": session.domains_consulted,
                "key_findings": session.key_findings,
                "summary": session.summary
            }

            if hasattr(self.memory_system, 'store_session_summary'):
                self.memory_system.store_session_summary(patient_id, summary_data)

        except Exception as e:
            print(f"Warning: Could not store session summary: {e}")

    def _extract_key_finding(self, context_entry: ConsultationContext) -> Optional[str]:
        """Extract key finding from consultation result."""
        answer = context_entry.result.get("answer", "")

        # Extract first sentence or key insight
        sentences = answer.split(". ")
        if sentences:
            return sentences[0].strip()

        return None

    def _generate_session_summary(self, session: PatientSession, patient_id: str) -> str:
        """Generate summary for patient session."""
        duration = (session.end_time or datetime.now()) - session.start_time

        summary_parts = [
            f"Patient Session Summary for {patient_id}",
            f"Duration: {duration}",
            f"Consultations: {session.consultation_count}",
            f"Specialties Consulted: {', '.join(session.domains_consulted)}",
        ]

        if session.key_findings:
            summary_parts.append(f"\nKey Findings:")
            for i, finding in enumerate(session.key_findings, 1):
                summary_parts.append(f"{i}. {finding}")

        return "\n".join(summary_parts)

    def _generate_summary_from_history(self, history: deque, session: PatientSession) -> str:
        """Generate summary from consultation history."""
        if not history:
            return "No consultation history available"

        summary_parts = [
            f"Consultation Summary for {session.patient_id}",
            f"Total Consultations: {len(history)}",
            f"Specialties Consulted: {', '.join(session.domains_consulted)}",
            ""
        ]

        # Add recent consultations
        summary_parts.append("Recent Consultations:")
        for i, ctx in enumerate(history[-5:], 1):  # Last 5 consultations
            summary_parts.append(
                f"{i}. [{ctx.domain}] {ctx.query[:50]}... "
                f"(Confidence: {ctx.confidence:.1%})"
            )

        # Add key findings
        if session.key_findings:
            summary_parts.append("\nKey Findings:")
            for i, finding in enumerate(session.key_findings[-5:], 1):  # Last 5 findings
                summary_parts.append(f"{i}. {finding}")

        return "\n".join(summary_parts)

    def get_patient_statistics(self, patient_id: str) -> Dict[str, Any]:
        """
        Get statistics for patient consultations.

        Args:
            patient_id: Patient identifier

        Returns:
            Dictionary with consultation statistics
        """
        session = self.get_patient_session(patient_id)
        history = self.context_history.get(patient_id, deque())

        # Calculate statistics
        if history:
            confidences = [ctx.confidence for ctx in history]
            avg_confidence = sum(confidences) / len(confidences)

            domain_counts = {}
            for ctx in history:
                domain_counts[ctx.domain] = domain_counts.get(ctx.domain, 0) + 1

            most_common_domain = max(domain_counts, key=domain_counts.get) if domain_counts else "none"
        else:
            avg_confidence = 0.0
            domain_counts = {}
            most_common_domain = "none"

        return {
            "patient_id": patient_id,
            "total_consultations": session.consultation_count,
            "active_domains": len(session.domains_consulted),
            "average_confidence": avg_confidence,
            "most_common_domain": most_common_domain,
            "domain_breakdown": domain_counts,
            "key_findings_count": len(session.key_findings),
            "session_active": session.end_time is None
        }

    def get_context_for_llm(self, patient_id: str, max_tokens: int = 2000) -> str:
        """
        Get formatted context for LLM consumption.

        Args:
            patient_id: Patient identifier
            max_tokens: Maximum tokens (approximate)

        Returns:
            Formatted context string
        """
        history = self.context_history.get(patient_id, deque())

        if not history:
            return "No previous consultation context."

        # Format context
        context_parts = ["Previous Consultation Context:", ""]

        for ctx in list(history)[-5:]:  # Last 5 consultations
            context_parts.append(f"Q: {ctx.query}")
            context_parts.append(f"A: {ctx.result.get('answer', '')[:200]}...")
            context_parts.append(f"[Domain: {ctx.domain}, Confidence: {ctx.confidence:.1%}]")
            context_parts.append("")

        return "\n".join(context_parts)
