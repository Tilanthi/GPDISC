"""
V73 Curiosity Engine - Generate Questions from Knowledge Gaps

The foundation of autonomous discovery: identifying what we don't know
and generating questions to fill those gaps.

PRINCIPLES:
1. Knowledge Gap Detection: Find concepts mentioned but not explained
2. Pattern Anomaly: Identify surprising or unexpected patterns
3. Cross-Domain Opportunity: Find unexplored connections between domains
4. Meta-Question: Ask how to improve discovery capabilities themselves

CAPABILITIES:
- Analyze knowledge base for gaps
- Generate prioritized questions
- Estimate impact of filling gaps
- Track exploration history

Date: 2026-04-26
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
import re
import hashlib
from datetime import datetime


class QuestionType(Enum):
    """Types of curiosity-driven questions"""
    KNOWLEDGE_GAP = "knowledge_gap"           # Missing explanation
    PATTERN_ANOMALY = "pattern_anomaly"       # Surprising pattern
    CROSS_DOMAIN = "cross_domain"            # Unexplored connection
    META_DISCOVERY = "meta_discovery"        # How to improve discovery
    CAUSAL_MECHANISM = "causal_mechanism"    # How/why questions
    QUANTITATIVE_GAP = "quantitative_gap"     # Missing numbers/data


class Priority(Enum):
    """Priority levels for questions"""
    CRITICAL = "critical"    # Filling this gap would significantly improve capability
    HIGH = "high"           # Important but not urgent
    MEDIUM = "medium"       # Worth exploring
    LOW = "low"            # Nice to have


@dataclass
class CuriosityQuestion:
    """A question generated from knowledge gaps"""
    id: str
    question_type: QuestionType
    question: str
    context: str  # Why this question matters
    knowledge_gap: str  # What don't we know?
    potential_discovery: str  # What might we learn?
    priority: Priority
    confidence: float  # How confident this is worth exploring
    estimated_effort: float  # Estimated computational cost (0-1)
    exploration_history: List[str] = field(default_factory=list)  # Previous attempts


@dataclass
class KnowledgeGap:
    """A gap in understanding"""
    concept: str
    mentioned_count: int  # How often it's mentioned
    explained_count: int  # How often it's explained
    gap_severity: float  # 0-1, how large is the gap?
    context: str  # Where is it mentioned?
    related_questions: List[str] = field(default_factory=list)


class KnowledgeGapAnalyzer:
    """
    Analyze knowledge base to find gaps.

    DETECTS:
    1. Concepts mentioned but not explained
    2. Claims without evidence
    3. Domains not connected
    4. Quantitative claims without data
    """

    def __init__(self):
        self.concept_mentions: Dict[str, int] = {}
        self.concept_explanations: Dict[str, int] = {}
        self.claims_without_evidence: List[str] = []
        self.domain_connections: Set[Tuple[str, str]] = set()

    def analyze_text(self, text: str, domain: str = "general") -> List[KnowledgeGap]:
        """
        Analyze text for knowledge gaps.

        Returns list of gaps found.
        """
        gaps = []

        # Extract key concepts (simplified - would use NLP in production)
        concepts = self._extract_concepts(text)

        # Check which are mentioned vs explained
        for concept in concepts:
            if concept not in self.concept_mentions:
                self.concept_mentions[concept] = 0
            self.concept_mentions[concept] += 1

            # Check if concept is explained in this text
            if self._is_concept_explained(text, concept):
                if concept not in self.concept_explanations:
                    self.concept_explanations[concept] = 0
                self.concept_explanations[concept] += 1

        # Find claims without quantitative support
        self._find_unsupported_claims(text)

        # Find domain connections
        self._find_domain_connections(text, domain)

        # Generate gaps from analysis
        for concept, mentions in self.concept_mentions.items():
            explanations = self.concept_explanations.get(concept, 0)

            if mentions > 2 and explanations == 0:
                # Concept mentioned multiple times but never explained
                gap = KnowledgeGap(
                    concept=concept,
                    mentioned_count=mentions,
                    explained_count=explanations,
                    gap_severity=min(1.0, mentions / 10),
                    context=f"Mentioned {mentions} times but never explained",
                    related_questions=[
                        f"What is {concept}?",
                        f"How does {concept} work?",
                        f"Why is {concept} important?"
                    ]
                )
                gaps.append(gap)

        return gaps

    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text (simplified)"""
        # Look for capitalized terms that might be concepts
        concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

        # Filter out common words and basic biological terminology
        stopwords = {
            'The', 'This', 'That', 'These', 'Those', 'When', 'What', 'How', 'Why',
            'Natural', 'Mendelian', 'Evolutionary', 'Molecular', 'Cellular', 'Genetic',
            'Biochemical', 'Physical', 'Structural', 'Functional', 'Cell', 'Cells',
            'Gene', 'Genes', 'Protein', 'Proteins', 'DNA', 'RNA', 'Enzyme', 'Enzymes',
            'Membrane', 'Membranes', 'Nucleus', 'Mitochondria', 'Ribosome', 'Ribosomes',
            'System', 'Systems', 'Process', 'Processes', 'Mechanism', 'Mechanisms',
            'Analysis', 'Analyses', 'Method', 'Methods', 'Result', 'Results',
            'Based', 'Using', 'Through', 'During', 'Within', 'Without', 'About'
        }
        concepts = [c for c in concepts if c not in stopwords and len(c) > 3]

        # Filter out single common words that got capitalized
        common_biological_terms = {
            'Biology', 'Chemistry', 'Physics', 'Science', 'Research', 'Study',
            'Development', 'Function', 'Structure', 'Activity', 'Expression',
            'Regulation', 'Interaction', 'Pathway', 'Pathways', 'Network',
            'Organism', 'Organisms', 'Tissue', 'Tissues', 'Organ', 'Organs',
            'Synthesis', 'Degradation', 'Transport', 'Signaling', 'Response',
            'Factor', 'Factors', 'Level', 'Levels', 'Phase', 'Phases',
            'Cycle', 'Cycles', 'Stage', 'Stages', 'Type', 'Types', 'Form', 'Forms'
        }
        concepts = [c for c in concepts if c not in common_biological_terms]

        # Only keep concepts that appear to be multi-word technical terms or specific enough
        # Single words that are too generic are filtered out
        generic_single_words = {
            'Specific', 'Multiple', 'Different', 'Various', 'Several', 'Many',
            'Complex', 'Simple', 'Basic', 'Advanced', 'Primary', 'Secondary',
            'Major', 'Minor', 'High', 'Low', 'Large', 'Small', 'Long', 'Short',
            'Early', 'Late', 'Before', 'After', 'During', 'Through', 'Between'
        }
        concepts = [c for c in concepts if c not in generic_single_words]

        # Deduplicate
        return list(set(concepts))

    def _is_concept_explained(self, text: str, concept: str) -> bool:
        """Check if concept is explained in text"""
        # Look for explanation patterns
        explanation_patterns = [
            f'{concept} is',
            f'{concept} refers to',
            f'{concept} can be defined',
            f'{concept} involves',
            f'{concept} works by'
        ]

        text_lower = text.lower()
        concept_lower = concept.lower()

        for pattern in explanation_patterns:
            if pattern.lower() in text_lower:
                return True

        return False

    def _find_unsupported_claims(self, text: str):
        """Find claims without quantitative support"""
        # Look for claim patterns
        claim_patterns = [
            r'significantly improves?',
            r'dramatically increases?',
            r'substantially reduces?',
            r'clearly demonstrates?',
        ]

        for pattern in claim_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Check if there's numerical support nearby
                context_start = max(0, match.start() - 100)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end]

                # Look for numbers
                if not re.search(r'\d+\.?\d*', context):
                    self.claims_without_evidence.append(match.group())

    def _find_domain_connections(self, text: str, domain: str):
        """Find potential connections to other domains"""
        # Known domains
        domains = ['physics', 'chemistry', 'biology', 'mathematics',
                   'computer science', 'statistics', 'evolution']

        for other_domain in domains:
            if other_domain != domain and other_domain.lower() in text.lower():
                # Record potential connection
                connection = tuple(sorted([domain, other_domain]))
                self.domain_connections.add(connection)


class ImpactEstimator:
    """
    Estimate potential impact of filling a knowledge gap.

    CONSIDERS:
    1. Centrality: How connected is this concept to other concepts?
    2. Generality: Does this apply broadly or narrowly?
    3. Validation: How confident are we this is worth pursuing?
    4. Novelty: Is this a new direction or well-trodden?
    """

    def __init__(self):
        self.exploration_history: Dict[str, List[str]] = {}

    def estimate_impact(
        self,
        question: CuriosityQuestion,
        knowledge_base_size: int = 1000
    ) -> Tuple[float, str]:
        """
        Estimate potential impact of pursuing this question.

        Returns: (impact_score 0-1, reasoning)
        """
        impact = 0.5  # Base impact
        reasoning_parts = []

        # Priority contributes to impact
        priority_scores = {
            Priority.CRITICAL: 0.4,
            Priority.HIGH: 0.3,
            Priority.MEDIUM: 0.2,
            Priority.LOW: 0.1
        }
        impact += priority_scores.get(question.priority, 0.2)
        reasoning_parts.append(f"Priority: {question.priority.value}")

        # Confidence affects impact (higher confidence = higher potential)
        impact += (question.confidence - 0.5) * 0.3
        reasoning_parts.append(f"Confidence: {question.confidence:.2f}")

        # Question type affects impact
        type_impacts = {
            QuestionType.META_DISCOVERY: 0.2,  # Improving discovery is high impact
            QuestionType.KNOWLEDGE_GAP: 0.15,
            QuestionType.CROSS_DOMAIN: 0.15,
            QuestionType.PATTERN_ANOMALY: 0.1,
            QuestionType.CAUSAL_MECHANISM: 0.1,
            QuestionType.QUANTITATIVE_GAP: 0.05
        }
        impact += type_impacts.get(question.question_type, 0.1)
        reasoning_parts.append(f"Type: {question.question_type.value}")

        # Cap at 1.0
        impact = min(1.0, max(0.0, impact))

        reasoning = ", ".join(reasoning_parts)
        return impact, reasoning

    def estimate_effort(self, question: CuriosityQuestion) -> float:
        """
        Estimate computational effort required (0-1).

        Lower is better (faster, cheaper).
        """
        effort = 0.5  # Base effort

        # Question type affects effort
        type_effort = {
            QuestionType.META_DISCOVERY: 0.8,  # Meta-questions are harder
            QuestionType.CROSS_DOMAIN: 0.7,
            QuestionType.CAUSAL_MECHANISM: 0.6,
            QuestionType.KNOWLEDGE_GAP: 0.4,
            QuestionType.PATTERN_ANOMALY: 0.5,
            QuestionType.QUANTITATIVE_GAP: 0.3
        }
        effort += type_effort.get(question.question_type, 0.5) - 0.5

        # Cap at 1.0
        return min(1.0, max(0.0, effort))


class CuriosityEngine:
    """
    Main curiosity engine - generates questions from knowledge gaps.

    WORKFLOW:
    1. Analyze knowledge base for gaps
    2. Generate questions from gaps
    3. Estimate impact and effort
    4. Prioritize by impact/effort ratio
    5. Return top questions for exploration

    INTEGRATES WITH:
    - V60 Persistent Memory (knowledge base)
    - V5 Discovery Orchestrator (exploration)
    - V73 Autonomous Discovery (orchestration)
    """

    def __init__(self):
        self.gap_analyzer = KnowledgeGapAnalyzer()
        self.impact_estimator = ImpactEstimator()
        self.question_history: List[CuriosityQuestion] = []
        self.exploration_queue: List[CuriosityQuestion] = []
        self.biological_kb = self._build_biological_knowledge_base()
        self.generated_questions_pool: List[CuriosityQuestion] = []  # Pool of generated questions
        self.question_cycle_index = 0  # Track position in question pool

    def generate_questions(
        self,
        knowledge_base: Dict[str, Any] = None,
        max_questions: int = 10
    ) -> List[CuriosityQuestion]:
        """
        Generate prioritized curiosity questions from knowledge gaps.

        Returns top N questions worth exploring.
        """
        # Use built-in biological KB if none provided
        if knowledge_base is None:
            knowledge_base = self.biological_kb

        questions = []

        # Analyze knowledge base for gaps
        if isinstance(knowledge_base, dict):
            for domain, content in knowledge_base.items():
                if isinstance(content, str):
                    gaps = self.gap_analyzer.analyze_text(content, domain)
                    for gap in gaps:
                        question = self._question_from_gap(gap, domain)
                        # Apply quality filter
                        if self._is_high_quality_question(question.question):
                            questions.append(question)
                elif isinstance(content, dict):
                    # Nested knowledge base
                    for sub_domain, sub_content in content.items():
                        if isinstance(sub_content, str):
                            gaps = self.gap_analyzer.analyze_text(sub_content, sub_domain)
                            for gap in gaps:
                                question = self._question_from_gap(gap, sub_domain)
                                # Apply quality filter
                                if self._is_high_quality_question(question.question):
                                    questions.append(question)

        # If no knowledge base provided or no gaps found, generate diverse questions
        if not questions:
            questions = self._generate_diverse_biological_questions()

        # Estimate impact for each question
        for question in questions:
            impact, _ = self.impact_estimator.estimate_impact(question)
            question.potential_discovery = f"Impact: {impact:.2f}"

        # Prioritize by impact/effort ratio
        scored_questions = []
        for question in questions:
            impact, _ = self.impact_estimator.estimate_impact(question)
            effort = self.impact_estimator.estimate_effort(question)
            ratio = impact / (effort + 0.1)  # Avoid division by zero
            scored_questions.append((ratio, question))

        # Sort by ratio and return top N
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        top_questions = [q for _, q in scored_questions[:max_questions]]

        # Store in history
        self.question_history.extend(top_questions)

        return top_questions

    def _build_biological_knowledge_base(self) -> Dict[str, str]:
        """Build a biological knowledge base from domain concepts"""
        return {
            "molecular_biology": """
            DNA replication is the process by which a cell copies its DNA before division.
            Transcription converts DNA into RNA, which is then translated into proteins.
            Gene expression regulation occurs at multiple levels including epigenetic modifications.
            CRISPR-Cas9 is a revolutionary gene editing technology adapted from bacterial immune systems.
            Alternative splicing allows a single gene to produce multiple protein variants.
            Non-coding RNAs play crucial regulatory roles beyond coding for proteins.
            """,

            "cell_biology": """
            The cell cycle consists of G1, S, G2, and M phases regulated by cyclins and CDKs.
            Apoptosis is programmed cell death essential for development and homeostasis.
            Autophagy is the cellular recycling process that degrades damaged components.
            Membrane trafficking involves vesicle transport between organelles.
            Cell junctions include tight junctions, adherens junctions, and gap junctions.
            """,

            "biochemistry": """
            Enzymes catalyze biochemical reactions by lowering activation energy.
            Allosteric regulation allows metabolic control through effector binding.
            Protein folding is assisted by chaperones that prevent aggregation.
            Post-translational modifications include phosphorylation, acetylation, and ubiquitination.
            Metabolic pathways are regulated through feedback inhibition and substrate availability.
            """,

            "genetics": """
            Mendelian inheritance describes dominant and recessive trait transmission.
            Linkage disequilibrium occurs when alleles are inherited together more often than expected.
            Epigenetic inheritance can transmit traits across generations without DNA sequence changes.
            Genetic variants include single nucleotide polymorphisms and copy number variations.
            Gene-environment interactions influence phenotypic expression.
            """,

            "biophysics": """
            Protein structure is determined by amino acid sequence and folding energy landscapes.
            Molecular dynamics simulations reveal protein conformational changes over time.
            Membrane potential arises from ion concentration gradients across cell membranes.
            Protein-protein interactions depend on binding affinity and cellular concentration.
            Mechanotransduction converts mechanical signals into biochemical responses.
            """,

            "microbiology": """
            Quorum sensing allows bacteria to communicate via signaling molecules.
            Biofilms are structured microbial communities embedded in extracellular matrix.
            Bacterial persistence involves dormant cells surviving antibiotic treatment.
            Horizontal gene transfer spreads antibiotic resistance between bacteria.
            Bacterial cell wall synthesis is targeted by many antibiotics.
            """,

            "evolutionary_biology": """
            Natural selection favors traits that increase reproductive fitness.
            Genetic drift causes random changes in allele frequencies in small populations.
            Convergent evolution produces similar traits in unrelated species facing similar pressures.
            Evolutionary developmental biology examines how developmental processes evolve.
            Molecular clocks use mutation rates to estimate evolutionary time scales.
            """,

            "systems_biology": """
            Network analysis reveals emergent properties in biological systems.
            Feedback loops maintain homeostasis or drive switch-like responses.
            Synthetic biology engineers novel biological functions from standardized parts.
            Multi-scale modeling connects molecular interactions to organism-level phenotypes.
            Robustness allows biological systems to maintain function despite perturbations.
            """
        }

    def _generate_diverse_biological_questions(self) -> List[CuriosityQuestion]:
        """Generate diverse biological questions from knowledge base analysis"""
        questions = []

        # Questions from each domain based on knowledge gaps
        domain_questions = {
            "molecular_biology": [
                ("How does alternative splicing specificity determine which isoforms are produced?", 0.75, "knowledge_gap"),
                ("What mechanisms regulate non-coding RNA stability and degradation?", 0.72, "knowledge_gap"),
                ("How do chromatin remodeling complexes coordinate with transcription factors?", 0.78, "causal_mechanism"),
            ],
            "cell_biology": [
                ("What determines the switch between apoptosis and autophagy under stress?", 0.80, "pattern_anomaly"),
                ("How do cells sense and regulate organelle size and number?", 0.73, "knowledge_gap"),
                ("What mechanisms ensure accurate spindle positioning during asymmetric cell division?", 0.76, "causal_mechanism"),
            ],
            "biochemistry": [
                ("How do allosteric effects propagate through protein structures?", 0.71, "causal_mechanism"),
                ("What determines the specificity of kinase-substrate recognition?", 0.74, "knowledge_gap"),
                ("How do chaperones distinguish between folding intermediates and misfolded proteins?", 0.69, "pattern_anomaly"),
            ],
            "genetics": [
                ("How do epigenetic marks escape reprogramming during gametogenesis?", 0.77, "pattern_anomaly"),
                ("What factors influence penetrance and expressivity of genetic variants?", 0.72, "knowledge_gap"),
                ("How do gene-gene interactions modify phenotypic outcomes?", 0.75, "cross_domain"),
            ],
            "biophysics": [
                ("How do intrinsically disordered proteins maintain functional conformations?", 0.73, "pattern_anomaly"),
                ("What physical principles govern membrane protein folding and insertion?", 0.71, "causal_mechanism"),
                ("How do cells amplify mechanical signals at the molecular level?", 0.76, "knowledge_gap"),
            ],
            "microbiology": [
                ("What triggers the transition from planktonic to biofilm lifestyle?", 0.79, "pattern_anomaly"),
                ("How do persister cells form and resuscitate in bacterial populations?", 0.74, "knowledge_gap"),
                ("What mechanisms limit horizontal gene transfer between species?", 0.70, "causal_mechanism"),
            ],
            "evolutionary_biology": [
                ("How does phenotypic plasticity influence evolutionary trajectories?", 0.78, "cross_domain"),
                ("What determines the rate of molecular clock variation across genes?", 0.71, "knowledge_gap"),
                ("How do novel genes arise from non-coding sequences?", 0.75, "pattern_anomaly"),
            ],
            "systems_biology": [
                ("How do biological networks balance robustness with evolvability?", 0.81, "cross_domain"),
                ("What design principles enable metabolic pathway optimality?", 0.73, "knowledge_gap"),
                ("How do feedback loops create bistable switches in cell fate decisions?", 0.77, "causal_mechanism"),
            ],
        }

        # Generate CuriosityQuestion objects
        for domain, questions_list in domain_questions.items():
            for question_text, confidence, qtype_str in questions_list:
                qtype = QuestionType(qtype_str)

                # Determine priority based on confidence
                if confidence >= 0.78:
                    priority = Priority.HIGH
                elif confidence >= 0.73:
                    priority = Priority.MEDIUM
                else:
                    priority = Priority.MEDIUM

                question = CuriosityQuestion(
                    id=f"q_{hashlib.md5(f"{domain}_{question_text}".encode()).hexdigest()[:8]}",
                    question_type=qtype,
                    question=question_text,
                    context=f"{domain.replace('_', ' ').title()}: Critical knowledge gap",
                    knowledge_gap=f"Understanding {question_text.lower().split('?')[0]} would advance {domain}",
                    potential_discovery=f"Could reveal fundamental principles in {domain.replace('_', ' ')}",
                    priority=priority,
                    confidence=confidence,
                    estimated_effort=0.5
                )
                questions.append(question)

        # Add original meta-questions for diversity
        questions.extend(self._generate_meta_questions())

        return questions

    def _is_high_quality_question(self, question_text: str) -> bool:
        """Check if a question is sufficiently complex to be worth exploring"""
        # Filter out simple "What is X" definition questions
        if re.match(r'^What (is|are|does|do) \w+\?$', question_text, re.IGNORECASE):
            return False

        # Filter out overly simple questions
        simple_patterns = [
            r'^What is \w+\?$',
            r'^Define \w+\?$',
            r'^Explain \w+\?$',
        ]
        for pattern in simple_patterns:
            if re.match(pattern, question_text, re.IGNORECASE):
                return False

        # Question should be at least somewhat complex
        # - Either multi-clause, or
        # - Contains domain-specific terminology, or
        # - Asks about relationships/mechanisms
        quality_indicators = [
            'how', 'why', 'mechanism', 'determine', 'regulate', 'specificity',
            'interaction', 'pathway', 'signal', 'cascade', 'network', 'complex',
            'relationship', 'between', 'affect', 'influence', 'control', 'modulate',
            'coordinate', 'integrate', 'synthesize', 'degrade', 'transport'
        ]

        question_lower = question_text.lower()
        return any(indicator in question_lower for indicator in quality_indicators)

    def _question_from_gap(self, gap: KnowledgeGap, domain: str) -> CuriosityQuestion:
        """Generate curiosity question from knowledge gap"""
        question_text = gap.related_questions[0] if gap.related_questions else f"What is {gap.concept}?"

        # Determine question type
        if gap.gap_severity > 0.7:
            qtype = QuestionType.KNOWLEDGE_GAP
            priority = Priority.HIGH
        else:
            qtype = QuestionType.KNOWLEDGE_GAP
            priority = Priority.MEDIUM

        return CuriosityQuestion(
            id=f"q_{hashlib.md5(question_text.encode()).hexdigest()[:8]}",
            question_type=qtype,
            question=question_text,
            context=f"In {domain}: {gap.context}",
            knowledge_gap=f"We mention {gap.concept} {gap.mentioned_count} times but never explain it",
            potential_discovery=f"Understanding {gap.concept} would fill a critical knowledge gap",
            priority=priority,
            confidence=min(0.9, gap.gap_severity + 0.5),
            estimated_effort=0.5
        )

    def _generate_meta_questions(self) -> List[CuriosityQuestion]:
        """Generate meta-questions about improving discovery"""
        return [
            CuriosityQuestion(
                id="meta_001",
                question_type=QuestionType.META_DISCOVERY,
                question="How can we improve the efficiency of causal discovery algorithms?",
                context="Meta-discovery: improving discovery capabilities themselves",
                knowledge_gap="We don't know which algorithmic improvements would yield the biggest gains",
                potential_discovery="Improving discovery efficiency would accelerate all future discoveries",
                priority=Priority.HIGH,
                confidence=0.7,
                estimated_effort=0.7
            ),
            CuriosityQuestion(
                id="meta_002",
                question_type=QuestionType.CROSS_DOMAIN,
                question="What connections exist between membrane physics and gene regulation that we haven't explored?",
                context="Cross-domain: physics-biology interface",
                knowledge_gap="Membrane physical properties affect cellular processes but connections to gene regulation are unclear",
                potential_discovery="Could reveal novel regulatory mechanisms coupling physical state to genetic regulation",
                priority=Priority.HIGH,
                confidence=0.6,
                estimated_effort=0.6
            ),
            CuriosityQuestion(
                id="meta_003",
                question_type=QuestionType.PATTERN_ANOMALY,
                question="Why do some bacteria use FtsZ-independent division mechanisms?",
                context="Evolutionary anomaly: L-forms and some archaea divide without FtsZ",
                knowledge_gap="Physical division mechanisms exist but their evolutionary advantage is unclear",
                potential_discovery="Could reveal fundamental principles about cell division and early evolution",
                priority=Priority.MEDIUM,
                confidence=0.8,
                estimated_effort=0.4
            )
        ]

    def get_next_question(self) -> Optional[CuriosityQuestion]:
        """Get next question from exploration queue"""
        if self.exploration_queue:
            return self.exploration_queue.pop(0)
        return None

    def update_exploration_history(self, question_id: str, result: str):
        """Update exploration history for a question"""
        for q in self.question_history:
            if q.id == question_id:
                q.exploration_history.append(result)
                break


def create_curiosity_engine() -> CuriosityEngine:
    """Factory function to create curiosity engine"""
    return CuriosityEngine()


# Singleton instance
_instance = None

def get_curiosity_engine() -> CuriosityEngine:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_curiosity_engine()
    return _instance
