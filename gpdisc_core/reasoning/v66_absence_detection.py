"""
V66 Absence Detection System - Noticing What's Missing

Most AI systems detect what's PRESENT. This system detects what's ABSENT.

CRITICAL INSIGHT from bacterial cell cycle review:
- L-forms were missing from discussion (expert noticed, I didn't)
- Cholesteric DNA organization was absent
- Evolutionary narrative was missing
- Alternative division systems not mentioned

CAPABILITIES:
- Detect absence of well-known domain mechanisms
- Compare against domain knowledge benchmarks
- Flag omissions that experts would notice
- Suggest missing mechanistic alternatives

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
import re


class AbsenceType(Enum):
    """Types of absences that can be detected"""
    ALTERNATIVE_SYSTEMS = "alternative_systems"      # L-forms, archaea, etc.
    PHYSICAL_MECHANISMS = "physical_mechanisms"      # Physical constraints
    EVOLUTIONARY_PERSPECTIVE = "evolutionary_perspective"  # Origins narrative
    QUANTITATIVE_SUPPORT = "quantitative_support"    # Worked examples, data
    CONTROVERSIAL_CLAIMS = "controversial_claims"    # Unmentioned debate
    COMPARATIVE_CONTEXT = "comparative_context"      # Cross-species, cross-domain


class DomainContext(Enum):
    """Biological and scientific domains"""
    BACTERIAL_CELL_CYCLE = "bacterial_cell_cycle"
    GENE_REGULATION = "gene_regulation"
    PROTEIN_STRUCTURE = "protein_structure"
    METABOLISM = "metabolism"
    EVOLUTION = "evolution"
    PHYSICS_CHEMISTRY = "physics_chemistry"


@dataclass
class AbsenceAlert:
    """An absence detected in the content"""
    absence_type: AbsenceType
    severity: float  # 0-1, how critical
    description: str
    what_should_be_present: str
    why_it_matters: str
    suggested_addition: str
    confidence: float  # How confident this is truly absent


class DomainKnowledgeBenchmark:
    """
    Benchmark knowledge that should be present for specific domains.

    This represents the "expert baseline" - what a domain expert would
    expect to see in a comprehensive discussion.
    """

    # Bacterial cell cycle benchmarks
    BACTERIAL_CELL_CYCLE_ESSENTIALS = {
        'alternative_systems': [
            "L-forms (cell wall-deficient bacteria)",
            "Archaeal division systems (ESCRT-III, Crenactin)",
            "Budding reproduction (Planctomycetes)",
            "Chlamydia unknown division mechanism"
        ],
        'physical_mechanisms': [
            "DNA supercoiling and topology",
            "Membrane physics (lateral/transverse asymmetry)",
            "Macromolecular crowding and entropic forces",
            "Turgor pressure and mechanical stress",
            "Polyelectrolyte effects",
            "Liquid crystalline phases (cholesteric DNA)"
        ],
        'evolutionary_perspectives': [
            "Physical chemistry as ancestral condition",
            "Molecular regulation as derived overlay",
            "Selective advantages for increasing complexity",
            "LUCA implications",
            "Evolutionary trajectory (Type C → B → A)"
        ],
        'quantitative_support': [
            "Worked examples for quantitative metrics",
            "Experimental data with effect sizes",
            "Confidence intervals or uncertainty quantification"
        ]
    }

    @classmethod
    def get_essentials(cls, domain: DomainContext) -> Dict[str, List[str]]:
        """Get essential knowledge benchmarks for a domain"""
        if domain == DomainContext.BACTERIAL_CELL_CYCLE:
            return cls.BACTERIAL_CELL_CYCLE_ESSENTIALS
        # Add other domains as needed
        return {}


class AbsenceDetector:
    """
    Detect what's missing from content that should be present.

    KEY CHALLENGE: Distinguishing "not mentioned yet" from "not relevant".

    HEURISTICS:
    1. If discussing mechanism X but not alternative Y, flag when Y is well-known
    2. If making claims about precision, flag if no quantitative support
    3. If discussing regulation, flag if no evolutionary context
    4. If discussing molecular systems, flag if no physical constraints
    """

    def __init__(self):
        self.benchmarks = DomainKnowledgeBenchmark()
        self.detected_absences: List[AbsenceAlert] = []

    def detect_absences(
        self,
        content: str,
        domain: DomainContext
    ) -> List[AbsenceAlert]:
        """
        Detect absences in content for a given domain.

        Returns list of absences that experts would notice.
        """
        alerts = []
        content_lower = content.lower()

        if domain == DomainContext.BACTERIAL_CELL_CYCLE:
            alerts.extend(self._detect_bacterial_cell_cycle_absences(content, content_lower))

        self.detected_absences = alerts
        return alerts

    def _detect_bacterial_cell_cycle_absences(
        self,
        content: str,
        content_lower: str
    ) -> List[AbsenceAlert]:
        """Detect absences specific to bacterial cell cycle domain"""
        alerts = []
        essentials = self.benchmarks.get_essentials(DomainContext.BACTERIAL_CELL_CYCLE)

        # Check for alternative systems
        if 'l-form' not in content_lower:
            alerts.append(AbsenceAlert(
                absence_type=AbsenceType.ALTERNATIVE_SYSTEMS,
                severity=0.8,
                description="L-forms (cell wall-deficient bacteria) not mentioned",
                what_should_be_present="Discussion of L-forms as evidence for Type C physical-default organization",
                why_it_matters="L-forms demonstrate that division can occur without FtsZ, showing physical processes alone can drive division. Expert would expect this in comprehensive discussion.",
                suggested_addition="Add section on L-forms: 'L-forms are cell wall-deficient bacteria that divide without FtsZ, relying instead on increased membrane synthesis and turgor pressure to drive spontaneous scission. This demonstrates physical processes alone can accomplish division, providing insight into early cell division mechanisms.'",
                confidence=0.95
            ))

        # Check for physical mechanisms
        physical_terms = ['cholesteric', 'liquid crystal', 'woldringh', 'bouligand']
        if not any(term in content_lower for term in physical_terms):
            alerts.append(AbsenceAlert(
                absence_type=AbsenceType.PHYSICAL_MECHANISMS,
                severity=0.7,
                description="Cholesteric DNA organization and liquid crystalline phases not mentioned",
                what_should_be_present="Discussion of DNA's liquid crystalline organization and its role in segregation",
                why_it_matters="Cholesteric DNA phases create entropic forces that favor chromosome extension and demixing, providing a physical mechanism for segregation. Experts in nucleoid organization expect this.",
                suggested_addition="Add: 'Beyond supercoiling, DNA within bacterial nucleoids can exhibit liquid crystalline phases, including cholesteric ordering. This creates entropic forces that favor chromosome extension and demixing, representing a purely physical mechanism for segregation.'",
                confidence=0.85
            ))

        # Check for evolutionary perspective
        evo_terms = ['evolution', 'origins', 'ancestral', 'luca', 'selective advantage']
        if not any(term in content_lower for term in evo_terms):
            alerts.append(AbsenceAlert(
                absence_type=AbsenceType.EVOLUTIONARY_PERSPECTIVE,
                severity=0.9,
                description="Evolutionary perspective missing from discussion",
                what_should_be_present="Evolutionary narrative tracing mechanisms back to physical foundations",
                why_it_matters="Biological mechanisms cannot be fully understood without considering their evolutionary origins. Experts expect discussion of selective advantages and evolutionary trajectories.",
                suggested_addition="Add evolutionary framing: 'Early cells likely relied primarily on physicochemical mechanisms. The evolution of molecular regulation provided increasingly specific and efficient control over these foundational processes. This evolutionary history is reflected in the hierarchical organization of modern systems.'",
                confidence=0.90
            ))

        # Check for quantitative support
        if 'asi' in content_lower or 'asymmetry index' in content_lower:
            if 'worked example' not in content_lower and 'example' not in content_lower:
                alerts.append(AbsenceAlert(
                    absence_type=AbsenceType.QUANTITATIVE_SUPPORT,
                    severity=0.95,
                    description="Quantitative metric (AsI) introduced without worked example",
                    what_should_be_present="Complete worked example with hypothetical data and step-by-step calculation",
                    why_it_matters="Quantitative metrics require concrete instantiation to be understood and validated. Without worked example, formula is abstract and potentially incorrect.",
                    suggested_addition="Add worked example section with: experimental setup, hypothetical data (SOS checkpoint: UV vs osmotic shock), step-by-step AsI calculation, interpretation of result (AsI=8.0 indicates molecular dominance)",
                    confidence=0.95
                ))

        # Check for membrane physics
        membrane_terms = ['membrane physics', 'lateral asymmetry', 'transverse asymmetry', 'cardiolipin']
        if any(term in content_lower for term in ['division', 'ftsz', 'septum']):
            if not any(term in content_lower for term in membrane_terms):
                alerts.append(AbsenceAlert(
                    absence_type=AbsenceType.PHYSICAL_MECHANISMS,
                    severity=0.6,
                    description="Membrane physics not discussed in context of division",
                    what_should_be_present="Discussion of how membrane physical properties influence division placement",
                    why_it_matters="Membrane curvature, fluidity, and asymmetry create spatial cues that molecular systems interpret. Experts in cell division expect this connection.",
                    suggested_addition="Add: 'Membrane physical properties provide spatial cues for division. Cardiolipin localizes to poles and division sites, creating regions of altered curvature and fluidity that influence divisome assembly.'",
                    confidence=0.75
                ))

        # Check for comparative context
        if 'e coli' in content_lower or 'escherichia coli' in content_lower:
            if 'bacillus' not in content_lower and ' Caulobacter' not in content_lower:
                alerts.append(AbsenceAlert(
                    absence_type=AbsenceType.COMPARATIVE_CONTEXT,
                    severity=0.5,
                    description="Discussion limited to E. coli without comparative context",
                    what_should_be_present="Comparison with other model systems (B. subtilis, Caulobacter)",
                    why_it_matters="Mechanisms vary across bacteria. What's true in E. coli may not be universal. Experts expect broader taxonomic sampling.",
                    suggested_addition="Add comparative notes: 'In B. subtilis, Noc performs nucleoid occlusion, and the division machinery differs in several details from E. coli. In Caulobacter, cell cycle regulation is obligately asymmetric, contrasting with E. coli's symmetric division.'",
                    confidence=0.70
                ))

        return alerts

    def check_completeness(
        self,
        content: str,
        domain: DomainContext
    ) -> Tuple[float, List[str]]:
        """
        Calculate completeness score for content.

        Returns: (completeness_ratio, missing_categories)
        """
        essentials = self.benchmarks.get_essentials(domain)
        content_lower = content.lower()

        total_items = sum(len(items) for items in essentials.values())
        if total_items == 0:
            return 1.0, []

        present_items = 0
        missing_categories = []

        for category, items in essentials.items():
            category_present = False
            for item in items:
                # Check if any key term from item is in content
                item_lower = item.lower()
                # Extract key terms (simplified)
                key_terms = re.findall(r'\b[a-z]{3,}\b', item_lower)
                if any(term in content_lower for term in key_terms[:3]):  # Check first 3 terms
                    category_present = True
                    present_items += 1
                    break

            if not category_present:
                missing_categories.append(category)

        completeness_ratio = present_items / total_items if total_items > 0 else 1.0
        return completeness_ratio, missing_categories

    def generate_suggestions(self, alerts: List[AbsenceAlert]) -> str:
        """
        Generate formatted suggestions from absence alerts.
        """
        if not alerts:
            return "No significant absences detected. Content appears comprehensive."

        suggestions = "## Suggested Additions Based on Detected Absences\n\n"

        # Sort by severity
        alerts_sorted = sorted(alerts, key=lambda a: a.severity, reverse=True)

        for i, alert in enumerate(alerts_sorted, 1):
            suggestions += f"### {i}. {alert.description} (Severity: {alert.severity:.2f})\n\n"
            suggestions += f"**Why important**: {alert.why_it_matters}\n\n"
            suggestions += f"**Suggested addition**: {alert.suggested_addition}\n\n"

        return suggestions


def create_absence_detector() -> AbsenceDetector:
    """Factory function to create absence detector"""
    return AbsenceDetector()


# Singleton instance
_instance = None

def get_absence_detector() -> AbsenceDetector:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_absence_detector()
    return _instance
