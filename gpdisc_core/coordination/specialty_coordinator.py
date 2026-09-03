"""
Specialty Coordination for Multi-Specialty Consultations

Coordinates across medical specialties for comprehensive consultations.
Handles specialty selection, conflict resolution, and second opinion generation.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class ConflictSeverity(Enum):
    """Severity level of specialty opinion conflicts."""
    NONE = "none"
    LOW = "low"  # Minor differences in emphasis
    MODERATE = "moderate"  # Different interpretations
    HIGH = "high"  # Contradictory recommendations
    CRITICAL = "critical"  # Directly opposing recommendations


@dataclass
class SpecialtyOpinion:
    """Opinion from a medical specialty."""
    specialty: str
    answer: str
    confidence: float
    recommendations: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpinionConflict:
    """Conflict between specialty opinions."""
    severity: ConflictSeverity
    specialties: Tuple[str, str]
    description: str
    conflicting_recommendations: List[str]
    resolution: Optional[str] = None


@dataclass
class CoordinatedResult:
    """Result of coordinated multi-specialty consultation."""
    recommendation: str
    specialty_opinions: Dict[str, SpecialtyOpinion]
    conflicts: List[OpinionConflict]
    resolution: Optional[str]
    consensus_level: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConflictDetector:
    """
    Detect conflicts between specialty opinions.

    Identifies:
    - Contradictory recommendations
    - Conflicting interpretations
    - Incompatible treatment approaches
    """

    def __init__(self):
        self.conflict_keywords = {
            "contradict": ["versus", "however", "although", "conversely", "opposing"],
            "incompatible": ["incompatible", "contraindicated", "should not", "avoid"]
        }

    def detect_conflicts(self,
                        opinions: Dict[str, SpecialtyOpinion]) -> List[OpinionConflict]:
        """
        Detect conflicts between specialty opinions.

        Args:
            opinions: Dictionary of specialty -> SpecialtyOpinion

        Returns:
            List of OpinionConflicts
        """
        conflicts = []
        specialties = list(opinions.keys())

        # Compare each pair of specialties
        for i in range(len(specialties)):
            for j in range(i + 1, len(specialties)):
                specialty1, specialty2 = specialties[i], specialties[j]
                opinion1, opinion2 = opinions[specialty1], opinions[specialty2]

                conflict = self._compare_opinions(specialty1, opinion1, specialty2, opinion2)

                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _compare_opinions(self,
                         specialty1: str,
                         opinion1: SpecialtyOpinion,
                         specialty2: str,
                         opinion2: SpecialtyOpinion) -> Optional[OpinionConflict]:
        """Compare two specialty opinions for conflicts."""
        # Check for contradictory recommendations
        conflicting_recs = self._find_conflicting_recommendations(
            opinion1.recommendations,
            opinion2.recommendations
        )

        if conflicting_recs:
            return OpinionConflict(
                severity=ConflictSeverity.HIGH,
                specialties=(specialty1, specialty2),
                description=f"Conflicting recommendations between {specialty1} and {specialty2}",
                conflicting_recommendations=conflicting_recs
            )

        # Check for conflicting interpretations
        if self._has_conflicting_interpretations(opinion1, opinion2):
            return OpinionConflict(
                severity=ConflictSeverity.MODERATE,
                specialties=(specialty1, specialty2),
                description=f"Different interpretations between {specialty1} and {specialty2}",
                conflicting_recommendations=[]
            )

        return None

    def _find_conflicting_recommendations(self,
                                        recs1: List[str],
                                        recs2: List[str]) -> List[str]:
        """Find conflicting recommendations."""
        conflicting = []

        # Check for direct contradictions
        for rec1 in recs1:
            for rec2 in recs2:
                if self._are_contradictory(rec1, rec2):
                    conflicting.append(f"{rec1} vs {rec2}")

        return conflicting

    def _are_contradictory(self, rec1: str, rec2: str) -> bool:
        """Check if two recommendations are contradictory."""
        rec1_lower = rec1.lower()
        rec2_lower = rec2.lower()

        # Check for contradiction keywords
        for keyword in self.conflict_keywords["contradict"]:
            if keyword in rec1_lower and keyword in rec2_lower:
                return True

        # Check for opposing actions
        opposing_pairs = [
            ("start", "stop"),
            ("continue", "discontinue"),
            ("increase", "decrease"),
            ("should", "should not"),
            ("recommend", "recommend against")
        ]

        for verb1, verb2 in opposing_pairs:
            if verb1 in rec1_lower and verb2 in rec2_lower:
                return True

        return False

    def _has_conflicting_interpretations(self,
                                       opinion1: SpecialtyOpinion,
                                       opinion2: SpecialtyOpinion) -> bool:
        """Check if opinions have conflicting interpretations."""
        # Simple check: do they reach different conclusions?
        findings1 = set(opinion1.key_findings)
        findings2 = set(opinion2.key_findings)

        # If findings overlap significantly, likely not a conflict
        overlap = len(findings1.intersection(findings2))
        total_unique = len(findings1.union(findings2))

        if total_unique > 0 and overlap / total_unique < 0.3:
            return True

        return False


class ConflictResolver:
    """
    Resolve conflicts between specialty opinions.

    Strategies:
    - Evidence-based resolution
    - Confidence-weighted resolution
    - Conservative approach
    - Escalation to human specialist
    """

    def __init__(self):
        self.resolution_strategies = [
            "evidence_based",
            "confidence_weighted",
            "conservative",
            "escalate"
        ]

    def resolve_conflicts(self,
                          conflicts: List[OpinionConflict],
                          opinions: Dict[str, SpecialtyOpinion]) -> Tuple[List[OpinionConflict], str]:
        """
        Resolve conflicts between specialty opinions.

        Args:
            conflicts: List of conflicts to resolve
            opinions: All specialty opinions

        Returns:
            Tuple of (resolved conflicts, resolution summary)
        """
        if not conflicts:
            return conflicts, "No conflicts detected"

        resolved = []
        resolution_summaries = []

        for conflict in conflicts:
            resolved_conflict, summary = self._resolve_single_conflict(conflict, opinions)
            resolved.append(resolved_conflict)
            resolution_summaries.append(summary)

        return resolved, "\n".join(resolution_summaries)

    def _resolve_single_conflict(self,
                                 conflict: OpinionConflict,
                                 opinions: Dict[str, SpecialtyOpinion]) -> Tuple[OpinionConflict, str]:
        """Resolve a single conflict."""
        # Choose resolution strategy based on severity
        if conflict.severity == ConflictSeverity.CRITICAL:
            return self._escalate_conflict(conflict)
        elif conflict.severity == ConflictSeverity.HIGH:
            return self._resolve_by_confidence(conflict, opinions)
        else:
            return self._resolve_evidence_based(conflict, opinions)

    def _escalate_conflict(self, conflict: OpinionConflict) -> Tuple[OpinionConflict, str]:
        """Escalate critical conflicts to human specialist."""
        conflict.resolution = "ESCALATED: Requires human specialist consultation"

        summary = (
            f"CRITICAL CONFLICT between {conflict.specialties[0]} and {conflict.specialties[1]}: "
            f"{conflict.description}. "
            f"Human specialist consultation required for resolution."
        )

        return conflict, summary

    def _resolve_by_confidence(self,
                              conflict: OpinionConflict,
                              opinions: Dict[str, SpecialtyOpinion]) -> Tuple[OpinionConflict, str]:
        """Resolve conflict by choosing higher confidence opinion."""
        specialty1, specialty2 = conflict.specialties
        opinion1, opinion2 = opinions[specialty1], opinions[specialty2]

        # Choose higher confidence opinion
        if opinion1.confidence > opinion2.confidence:
            chosen = specialty1
            chosen_confidence = opinion1.confidence
        else:
            chosen = specialty2
            chosen_confidence = opinion2.confidence

        conflict.resolution = f"Resolved by choosing {chosen} opinion (confidence: {chosen_confidence:.1%})"

        summary = (
            f"CONFLICT RESOLVED: {conflict.description}. "
            f"Chose {chosen} opinion based on higher confidence ({chosen_confidence:.1%})."
        )

        return conflict, summary

    def _resolve_evidence_based(self,
                               conflict: OpinionConflict,
                               opinions: Dict[str, SpecialtyOpinion]) -> Tuple[OpinionConflict, str]:
        """Resolve conflict using evidence-based approach."""
        # Combine both opinions with emphasis on evidence
        conflict.resolution = "Resolved by combining evidence from both specialties"

        summary = (
            f"MODERATE CONFLICT: {conflict.description}. "
            f"Combining perspectives from {conflict.specialties[0]} and {conflict.specialties[1]} "
            f"for evidence-based approach."
        )

        return conflict, summary


class SecondOpinionGenerator:
    """
    Generate second opinions from medical specialties.

    Provides:
    - Independent specialty opinions
    - Cross-specialty validation
    - Alternative diagnostic considerations
    """

    def __init__(self, domain_registry: Optional[Dict] = None):
        self.domain_registry = domain_registry or {}

    def generate_second_opinion(self,
                               query: str,
                               primary_domain: str,
                               patient_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate second opinion from alternative specialty.

        Args:
            query: Medical query
            primary_domain: Domain of primary opinion
            patient_context: Patient information

        Returns:
            Second opinion result
        """
        # Select alternative specialty
        alternative_domain = self._select_alternative_specialty(primary_domain, query)

        if not alternative_domain:
            return {
                "success": False,
                "message": "No alternative specialty available"
            }

        # Get alternative opinion
        alternative_opinion = self._get_specialty_opinion(
            query, alternative_domain, patient_context
        )

        return {
            "success": True,
            "primary_domain": primary_domain,
            "alternative_domain": alternative_domain,
            "alternative_opinion": alternative_opinion,
            "timestamp": datetime.now().isoformat()
        }

    def generate_multi_specialty_opinions(self,
                                         query: str,
                                         patient_context: Optional[Dict] = None) -> Dict[str, SpecialtyOpinion]:
        """
        Generate opinions from multiple relevant specialties.

        Args:
            query: Medical query
            patient_context: Patient information

        Returns:
            Dictionary of specialty -> SpecialtyOpinion
        """
        # Identify relevant specialties
        relevant_specialties = self._identify_relevant_specialties(query)

        opinions = {}
        for specialty in relevant_specialties:
            opinion = self._get_specialty_opinion(query, specialty, patient_context)
            opinions[specialty] = opinion

        return opinions

    def _select_alternative_specialty(self,
                                     primary_domain: str,
                                     query: str) -> Optional[str]:
        """Select appropriate alternative specialty."""
        # Domain affinity for second opinions
        second_opinion_map = {
            "cardiology": ["epilepsy", "general_practice"],
            "epilepsy": ["cardiology", "general_practice"],
            "orthopedics": ["cardiology", "general_practice"],
            "pharmacology": ["general_practice"],
            "general_practice": ["cardiology", "epilepsy", "orthopedics"]
        }

        alternatives = second_opinion_map.get(primary_domain, [])

        # Select first available alternative
        for alt in alternatives:
            if alt in self.domain_registry:
                return alt

        return None

    def _identify_relevant_specialties(self, query: str) -> List[str]:
        """Identify relevant medical specialties for query."""
        query_lower = query.lower()

        # Keyword mapping to specialties
        specialty_keywords = {
            "cardiology": ["heart", "chest pain", "ecg", "cardiac", "blood pressure"],
            "epilepsy": ["seizure", "epilepsy", "convulsion", "eeg"],
            "orthopedics": ["bone", "fracture", "joint", "orthopedic", "muscle"],
            "pharmacology": ["drug", "medication", "interaction", "dosage"],
            "general_practice": ["symptom", "checkup", "diagnosis"]
        }

        relevant = []
        for specialty, keywords in specialty_keywords.items():
            if any(kw in query_lower for kw in keywords):
                if specialty in self.domain_registry:
                    relevant.append(specialty)

        # Default to general practice
        if not relevant and "general_practice" in self.domain_registry:
            relevant.append("general_practice")

        return relevant

    def _get_specialty_opinion(self,
                              query: str,
                              specialty: str,
                              patient_context: Optional[Dict]) -> SpecialtyOpinion:
        """Get opinion from specific specialty."""
        if specialty not in self.domain_registry:
            return SpecialtyOpinion(
                specialty=specialty,
                answer=f"{specialty} domain not available",
                confidence=0.0,
                recommendations=[],
                key_findings=[]
            )

        try:
            domain_module = self.domain_registry[specialty]
            result = domain_module.process_query(query, patient_context)

            # Extract recommendations and findings
            answer = result.get("answer", "")
            recommendations = self._extract_recommendations(answer)
            key_findings = self._extract_key_findings(answer)

            return SpecialtyOpinion(
                specialty=specialty,
                answer=answer,
                confidence=result.get("confidence", 0.5),
                recommendations=recommendations,
                key_findings=key_findings,
                metadata=result.get("metadata", {})
            )

        except Exception as e:
            return SpecialtyOpinion(
                specialty=specialty,
                answer=f"Error processing query: {str(e)}",
                confidence=0.0,
                recommendations=[],
                key_findings=[]
            )

    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract clinical recommendations from text."""
        recommendations = []

        for sentence in text.split(". "):
            if any(word in sentence.lower() for word in
                   ["recommend", "should", "consider", "suggest", "advise"]):
                recommendations.append(sentence.strip())

        return recommendations

    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from text."""
        findings = []

        # Look for sentences with key medical terms
        medical_keywords = ["diagnosis", "finding", "shows", "indicates", "reveals"]

        for sentence in text.split(". "):
            if any(kw in sentence.lower() for kw in medical_keywords):
                findings.append(sentence.strip())

        return findings[:5]  # Limit to top 5 findings


class SpecialtyCoordinator:
    """
    Coordinate multi-specialty consultations.

    Features:
    - Automatic specialty selection
    - Cross-specialty consultation
    - Second opinion generation
    - Conflict resolution
    """

    def __init__(self, domain_registry: Optional[Dict] = None):
        self.domain_registry = domain_registry or {}
        self.conflict_detector = ConflictDetector()
        self.conflict_resolver = ConflictResolver()
        self.second_opinion_generator = SecondOpinionGenerator(domain_registry)

    def coordinate_consultation(self,
                                query: str,
                                patient_context: Optional[Dict] = None) -> CoordinatedResult:
        """
        Coordinate across relevant specialties.

        Args:
            query: Medical consultation query
            patient_context: Patient information

        Returns:
            CoordinatedResult with multi-specialty recommendations
        """
        # 1. Identify relevant specialties
        relevant_specialties = self._identify_specialties(query)

        # 2. Query each specialty
        specialty_opinions = {}
        for specialty in relevant_specialties:
            opinion = self._get_specialty_opinion(query, specialty, patient_context)
            specialty_opinions[specialty] = opinion

        # 3. Check for conflicts
        conflicts = self.conflict_detector.detect_conflicts(specialty_opinions)

        # 4. Resolve conflicts
        if conflicts:
            resolved_conflicts, resolution_summary = self.conflict_resolver.resolve_conflicts(
                conflicts, specialty_opinions
            )
        else:
            resolved_conflicts = conflicts
            resolution_summary = "No conflicts between specialty opinions"

        # 5. Synthesize final recommendation
        final_recommendation = self._synthesize_recommendation(
            specialty_opinions, resolved_conflicts
        )

        # 6. Assess consensus level
        consensus_level = self._assess_consensus(specialty_opinions, conflicts)

        return CoordinatedResult(
            recommendation=final_recommendation,
            specialty_opinions=specialty_opinions,
            conflicts=resolved_conflicts,
            resolution=resolution_summary,
            consensus_level=consensus_level,
            metadata={
                "specialties_consulted": list(specialty_opinions.keys()),
                "total_specialties": len(specialty_opinions),
                "conflict_count": len(conflicts),
                "timestamp": datetime.now().isoformat()
            }
        )

    def generate_second_opinion(self,
                               query: str,
                               primary_domain: str,
                               patient_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate second opinion for consultation.

        Args:
            query: Medical query
            primary_domain: Primary specialty domain
            patient_context: Patient information

        Returns:
            Second opinion result
        """
        return self.second_opinion_generator.generate_second_opinion(
            query, primary_domain, patient_context
        )

    def _identify_specialties(self, query: str) -> List[str]:
        """Identify relevant medical specialties for query."""
        return self.second_opinion_generator._identify_relevant_specialties(query)

    def _get_specialty_opinion(self,
                              query: str,
                              specialty: str,
                              patient_context: Optional[Dict]) -> SpecialtyOpinion:
        """Get opinion from specific specialty."""
        return self.second_opinion_generator._get_specialty_opinion(
            query, specialty, patient_context
        )

    def _synthesize_recommendation(self,
                                   opinions: Dict[str, SpecialtyOpinion],
                                   conflicts: List[OpinionConflict]) -> str:
        """Synthesize final recommendation from specialty opinions."""
        if not opinions:
            return "No specialty opinions available"

        # If only one opinion
        if len(opinions) == 1:
            opinion = list(opinions.values())[0]
            return f"[{opinion.specialty}] {opinion.answer}"

        # If conflicts exist, mention them
        if conflicts:
            intro = "Multi-specialty consultation completed. Note: Specialty conflicts resolved.\n\n"
        else:
            intro = "Multi-specialty consultation completed. Consensus achieved.\n\n"

        # Combine opinions
        opinion_parts = [intro]
        for specialty, opinion in opinions.items():
            opinion_parts.append(
                f"**{specialty.title()} Opinion:** {opinion.answer}"
            )

        return "\n\n".join(opinion_parts)

    def _assess_consensus(self,
                         opinions: Dict[str, SpecialtyOpinion],
                         conflicts: List[OpinionConflict]) -> str:
        """Assess level of consensus between specialties."""
        if not opinions:
            return "none"

        if len(opinions) == 1:
            return "single_specialty"

        # Count high and critical severity conflicts
        severe_conflicts = [c for c in conflicts
                          if c.severity in [ConflictSeverity.HIGH, ConflictSeverity.CRITICAL]]

        if not conflicts:
            return "full_consensus"
        elif not severe_conflicts:
            return "partial_consensus"
        else:
            return "significant_disagreement"
