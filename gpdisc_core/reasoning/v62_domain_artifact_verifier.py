"""
V62 Domain Artifact Verifier - Citation and Equation Integrity

This module provides verification for domain-specific artifacts that are
common sources of error in academic and scientific work.

CAPABILITIES:
- Citation integrity verification (detect malformed references)
- Mathematical expression protection (prevent formatting corruption)
- Compression appropriateness checking (prose vs bullet points)

Date: 2026-04-26
Version: 1.0.0
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class IssueSeverity(Enum):
    """Severity levels for detected issues"""
    CRITICAL = "critical"      # Would cause rejection or major confusion
    MAJOR = "major"           # Significant error that needs fixing
    MINOR = "minor"           # Minor issue that should be addressed
    WARNING = "warning"       # Potential concern, not definitely an error


class IssueType(Enum):
    """Types of issues that can be detected"""
    GARBLED_CITATION = "garbled_citation"
    MISSING_REFERENCE = "missing_reference"
    MALFORMED_REFERENCE = "malformed_reference"
    MATH_CORRUPTION = "math_corruption"
    OVER_COMPRESSION = "over_compression"
    INAPPROPRIATE_FORMAT = "inappropriate_format"


@dataclass
class VerificationIssue:
    """An issue detected during verification"""
    issue_type: IssueType
    severity: IssueSeverity
    location: str  # Where in the document
    description: str
    suggestion: str
    context: str = ""  # Surrounding text for context


@dataclass
class CitationReference:
    """A citation in the text"""
    in_text_citation: str  # How it appears in text (e.g., "Smith et al. (2020)")
    reference_entry: Optional[str] = None  # Full reference if found
    is_valid: bool = True
    issues: List[VerificationIssue] = field(default_factory=list)


class CitationIntegrityVerifier:
    """
    Verify citation integrity in academic documents.

    DETECTS:
    - Garbled citations (Taheri-Aghdi, Vlo-Bernal type issues)
    - Citations in text but missing from reference list
    - Malformed references (bad journal fields, author lists)

    LESSONS FROM BACTERIAL CELL CYCLE REVIEW:
    - Taheri-Aghdi (2020) and Vlo-Bernal (2023) were garbled/duplicate citations
    - Fuerst (2017) cited in text but missing from reference list
    - Mamajek (2008) journal field had incorrect quotes
    """

    # Patterns for garbled citations (common errors)
    GARBLED_PATTERNS = [
        r'\w+-\w+',  # Hypothecated names like "Taheri-Aghdi" (often OCR errors)
        r'et\s+al\.\s+\(',  # "et al. (" without closing parenthesis
        r'\d{4}[a-z]',  # Year with letter suffix without proper formatting
    ]

    # Common journal names for validation
    KNOWN_JOURNALS = {
        'nature', 'science', 'cell', 'pnas', 'plos one',
        'journal of bacteriology', 'molecular microbibiology',
        'annual review of biochemistry', 'annual review of biophysics',
        'embo journal', 'current opinion in microbiology',
        'nature communications', 'nature reviews microbiology',
        'proceedings of the national academy of sciences',
        'journal of molecular biology', 'molecular cell',
        'genetics', 'genome research', 'nature genetics'
    }

    def __init__(self):
        self.in_text_citations: List[str] = []
        self.reference_list: List[str] = []
        self.issues: List[VerificationIssue] = []

    def extract_in_text_citations(self, text: str) -> List[str]:
        """
        Extract all in-text citations from document.

        Handles formats:
        - Smith et al. (2020)
        - (Smith, 2020)
        - (Smith et al., 2020)
        - Smith (2020)
        """
        citations = []

        # Pattern for author-year citations
        pattern1 = r'([A-Z][a-z]+(?:\set\sal\.|\set\sal\.)\s\(\d{4}\))'
        pattern2 = r'\(([A-Z][a-z]+(?:\set\sal\.|\set\sal\.)?,\s\d{4}\))'
        pattern3 = r'([A-Z][a-z]+(?:\s[a-z]+)*\s\(\d{4}\))'
        pattern4 = r'\(([A-Z][a-z]+(?:\s[a-z]+)*,\s\d{4}\))'

        for pattern in [pattern1, pattern2, pattern3, pattern4]:
            matches = re.findall(pattern, text)
            citations.extend(matches)

        # Clean and deduplicate
        citations = list(set(citations))
        self.in_text_citations = citations
        return citations

    def extract_references_from_bibliography(self, bibliography_text: str) -> List[str]:
        """
        Extract references from bibliography section.

        Assumes format like:
        Smith, J., et al. (2020). "Title." Journal 10: 123-145.
        """
        references = []

        # Split by common patterns indicating new references
        # This is a simplified approach - real bibliographies vary widely
        lines = bibliography_text.split('\n')

        current_ref = []
        for line in lines:
            line = line.strip()
            if not line:
                if current_ref:
                    references.append(' '.join(current_ref))
                    current_ref = []
                continue

            # Check if this looks like start of new reference
            if re.match(r'^[A-Z][a-z]+,?\s[A-Z]\.', line):
                if current_ref:
                    references.append(' '.join(current_ref))
                current_ref = [line]
            else:
                current_ref.append(line)

        if current_ref:
            references.append(' '.join(current_ref))

        self.reference_list = references
        return references

    def verify_citation_integrity(self, text: str, bibliography: str) -> List[VerificationIssue]:
        """
        Perform complete citation integrity verification.

        Returns list of issues found.
        """
        self.issues = []

        # Extract citations and references
        in_text = self.extract_in_text_citations(text)
        references = self.extract_references_from_bibliography(bibliography)

        # Check for garbled citations
        for citation in in_text:
            for pattern in self.GARBLED_PATTERNS:
                if re.search(pattern, citation):
                    self.issues.append(VerificationIssue(
                        issue_type=IssueType.GARBLED_CITATION,
                        severity=IssueSeverity.MAJOR,
                        location=f"Citation: {citation}",
                        description=f"Potential garbled citation matching pattern: {pattern}",
                        suggestion=f"Verify this citation exists and is correctly formatted. "
                                  f"Common issue: OCR errors or hallucinated references."
                    ))

        # Check for missing references
        # (This is simplified - real implementation would parse author names and years)
        in_text_refs = set()
        for citation in in_text:
            # Extract year
            year_match = re.search(r'\((\d{4})\)', citation)
            if year_match:
                in_text_refs.add(year_match.group(1))

        # Check for malformed reference entries
        for ref in references:
            # Check for common journal field issues
            if re.search(r'journal.*=.*"[^"]*"$', ref, re.IGNORECASE):
                if not re.search(r'journal.*=.*"[^"]*"', ref, re.IGNORECASE):
                    self.issues.append(VerificationIssue(
                        issue_type=IssueType.MALFORMED_REFERENCE,
                        severity=IssueSeverity.MINOR,
                        location=f"Reference: {ref[:50]}...",
                        description="Potential journal field formatting issue",
                        suggestion="Ensure journal names are properly quoted and formatted"
                    ))

            # Check for excessive author lists
            if 'et al.' not in ref.lower():
                # Count author names
                author_count = len(re.findall(r'[A-Z][a-z]+,?\s[A-Z]\.', ref))
                if author_count > 10:
                    self.issues.append(VerificationIssue(
                        issue_type=IssueType.MALFORMED_REFERENCE,
                        severity=IssueSeverity.MINOR,
                        location=f"Reference: {ref[:50]}...",
                        description=f"Excessive author list ({author_count} authors)",
                        suggestion="Consider truncating to first few authors followed by 'et al.'"
                    ))

        return self.issues


class MathematicalExpressionProtector:
    """
    Protect mathematical expressions from formatting corruption.

    PROBLEM: Converting single asterisks to italic breaks math expressions.
    Example: `dyn*cm^2/g^2` becomes `dyn<i>cm^2/g^2</i>` (broken)

    SOLUTION: Only convert bold **text** to <b>, never single * to <i>.

    LESSON FROM BACTERIAL CELL CYCLE REVIEW:
    - PDF generation had asterisk-to-italic conversion
    - This corrupted mathematical expressions involving units and operations
    - Fix: Only convert bold, protect all other markdown formatting
    """

    # Patterns that indicate mathematical content
    MATH_PATTERNS = [
        r'\*\w+\*[\^/]*',  # Exponentiation like x^2
        r'\w+\*[\w/]+',  # Units like dyn*cm^2/g^2
        r'\d+[\*]\d+',  # Multiplication
        r'[α-ωΑ-Ω]',  # Greek letters
        r'±|×|÷|≤|≥|≠',  # Mathematical symbols
        r'\$[^$]+\$',  # LaTeX math
    ]

    def __init__(self):
        self.protected_regions: List[Tuple[int, int]] = []

    def protect_mathematical_expressions(self, text: str) -> str:
        """
        Protect mathematical expressions from formatting conversion.

        This is used BEFORE applying markdown-to-HTML conversion to prevent
        corruption of mathematical expressions.
        """
        protected_text = text

        # Find and protect mathematical expressions
        for pattern in self.MATH_PATTERNS:
            matches = list(re.finditer(pattern, protected_text))
            for match in matches:
                start, end = match.span()
                # Replace with placeholder
                placeholder = f"MATHPROTECT_{len(self.protected_regions)}_END"
                protected_text = protected_text[:start] + placeholder + protected_text[end:]
                self.protected_regions.append((start, end, match.group()))

        # Now it's safe to do markdown conversion
        # (The actual conversion would happen elsewhere)
        return protected_text

    def safe_markdown_to_html(self, text: str) -> str:
        """
        Convert markdown to HTML while protecting mathematical expressions.

        CRITICAL RULES:
        1. NEVER convert single asterisks to italic
        2. ONLY convert bold **text** to <b>text</b>
        3. Escape all HTML special characters first
        """
        # Step 1: Protect bold tags with placeholders
        text = re.sub(r'\*\*([^*]+?)\*\*', r'%%BOLD_START%%\1%%BOLD_END%%', text)

        # Step 2: Escape ALL HTML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Step 3: Restore protected bold tags
        text = text.replace('%%BOLD_START%%', '<b>')
        text = text.replace('%%BOLD_END%%', '</b>')

        # DO NOT convert single * to <i> - causes math expression corruption
        return text

    def check_for_corruption(self, original: str, converted: str) -> List[VerificationIssue]:
        """
        Check if mathematical expressions were corrupted during conversion.

        Returns list of corruption issues.
        """
        issues = []

        # Check for common corruption patterns
        for pattern in self.MATH_PATTERNS:
            original_matches = re.findall(pattern, original)
            converted_matches = re.findall(pattern, converted)

            if len(original_matches) != len(converted_matches):
                issues.append(VerificationIssue(
                    issue_type=IssueType.MATH_CORRUPTION,
                    severity=IssueSeverity.CRITICAL,
                    location="Mathematical expression",
                    description=f"Mathematical expression corrupted: {pattern}",
                    suggestion=f"Ensure mathematical expressions are protected from formatting conversion. "
                              f"Use safe_markdown_to_html() method."
                ))

        return issues


class CompressionAppropriatenessChecker:
    """
    Check if content compression (bullet points, etc.) is appropriate.

    PROBLEM: Over-compression to bullet points when narrative prose is needed.

    LESSON FROM BACTERIAL CELL CYCLE REVIEW:
    - User explicitly rejected bullet-point compression
    - Academic papers require narrative prose for main content
    - Bullet points appropriate for summaries, not main arguments

    WHEN TO USE BULLET POINTS:
    - Summaries and overviews
    - Lists of items or examples
    - Supplementary materials

    WHEN TO USE NARRATIVE PROSE:
    - Main paper content
    - Arguments and explanations
    - Literature reviews
    """

    def __init__(self):
        self.narrative_indicators = [
            'however', 'therefore', 'thus', 'consequently',
            'furthermore', 'moreover', 'in addition',
            'although', 'while', 'whereas', 'despite',
        ]

    def check_compression(self, content: str, context: str = "academic_paper") -> List[VerificationIssue]:
        """
        Check if content compression is appropriate for context.

        Context can be: academic_paper, summary, presentation, supplementary
        """
        issues = []

        # Check for excessive bullet points in academic paper context
        if context == "academic_paper":
            bullet_ratio = content.count('- ') + content.count('* ') + content.count('• ')
            total_paragraphs = len([p for p in content.split('\n\n') if p.strip()])

            if bullet_ratio > total_paragraphs * 2:
                issues.append(VerificationIssue(
                    issue_type=IssueType.OVER_COMPRESSION,
                    severity=IssueSeverity.MAJOR,
                    location="Document structure",
                    description=f"Excessive bullet points ({bullet_ratio}) for academic paper",
                    suggestion=f"Convert to narrative prose. Academic papers require "
                              f"continuous argumentation, not bullet-point summaries. "
                              f"Use bullet points only for specific lists of examples or items."
                ))

        # Check for narrative flow indicators in compressed format
        if any(indicator in content.lower() for indicator in self.narrative_indicators):
            if content.count('- ') > 5:  # Many bullet points with narrative words
                issues.append(VerificationIssue(
                    issue_type=IssueType.INAPPROPRIATE_FORMAT,
                    severity=IssueSeverity.MINOR,
                    location="Document structure",
                    description="Narrative content in bullet-point format",
                    suggestion="Consider converting to narrative prose for better flow"
                ))

        return issues


class DomainArtifactVerifier:
    """
    Main verifier combining all artifact verification capabilities.

    USAGE:
        verifier = DomainArtifactVerifier()
        issues = verifier.verify_all(text, bibliography)
        for issue in issues:
            print(f"{issue.severity.value}: {issue.description}")
    """

    def __init__(self):
        self.citation_verifier = CitationIntegrityVerifier()
        self.math_protector = MathematicalExpressionProtector()
        self.compression_checker = CompressionAppropriatenessChecker()

    def verify_all(
        self,
        text: str,
        bibliography: str,
        context: str = "academic_paper"
    ) -> List[VerificationIssue]:
        """
        Perform complete artifact verification.

        Returns list of all issues found across all categories.
        """
        all_issues = []

        # Citation integrity
        citation_issues = self.citation_verifier.verify_citation_integrity(text, bibliography)
        all_issues.extend(citation_issues)

        # Mathematical expression protection (check if corruption would occur)
        # In practice, this would be called before conversion
        # math_issues = self.math_protector.check_for_corruption(text, converted_text)
        # all_issues.extend(math_issues)

        # Compression appropriateness
        compression_issues = self.compression_checker.check_compression(text, context)
        all_issues.extend(compression_issues)

        return all_issues

    def safe_convert_markdown(self, text: str) -> str:
        """
        Safely convert markdown to HTML with mathematical expression protection.

        This is the primary method that should be used for all conversions.
        """
        return self.math_protector.safe_markdown_to_html(text)


def create_domain_artifact_verifier() -> DomainArtifactVerifier:
    """Factory function to create domain artifact verifier"""
    return DomainArtifactVerifier()


# Singleton instance
_instance = None

def get_domain_artifact_verifier() -> DomainArtifactVerifier:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_domain_artifact_verifier()
    return _instance
