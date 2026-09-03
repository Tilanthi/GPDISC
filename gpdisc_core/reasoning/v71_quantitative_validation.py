"""
V71 Quantitative Validation Engine - Ensuring Quantitative Claims Have Quantitative Support

CRITICAL ISSUE from bacterial cell cycle review:
- Introduced AsI metric without worked example
- Formula provided but no concrete instantiation
- Signal-to-noise rationale not demonstrated with numbers
- No step-by-step calculation shown

CAPABILITIES:
- Detect when quantitative metrics are introduced without worked examples
- Validate that formulas have concrete numerical demonstration
- Check that signal-to-noise claims are justified
- Require step-by-step calculations for new metrics

PRINCIPLE:
Every quantitative claim must have quantitative support.
Every new metric must have a complete worked example.

Date: 2026-04-26
Version: 1.0.0
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Union
from enum import Enum


class ValidationType(Enum):
    """Types of quantitative validation"""
    WORKED_EXAMPLE = "worked_example"          # Need concrete numerical example
    SIGNAL_NOISE_JUSTIFICATION = "signal_noise"  # Need S/N justification
    PARAMETER_VALUE = "parameter_value"        # Need justification for parameter values
    UNCERTAINTY_QUANTIFICATION = "uncertainty"  # Need confidence intervals
    DATA_REFERENCE = "data_reference"          # Need reference to experimental data


class ValidationSeverity(Enum):
    """Severity of validation issues"""
    CRITICAL = "critical"      # Metric completely unusable without this
    MAJOR = "major"           # Significantly weakens the metric
    MODERATE = "moderate"     # Should be addressed but not fatal
    MINOR = "minor"           # Nice to have


@dataclass
class QuantitativeClaim:
    """A quantitative claim detected in text"""
    claim_text: str
    claim_type: str  # "metric", "formula", "threshold", "comparison"
    location: str
    variables: Dict[str, str]  # Variable names and their descriptions
    formula: Optional[str] = None
    claimed_value: Optional[Union[float, str]] = None


@dataclass
class ValidationIssue:
    """A quantitative validation issue"""
    validation_type: ValidationType
    severity: ValidationSeverity
    claim: QuantitativeClaim
    description: str
    what_is_missing: str
    why_it_matters: str
    suggested_addition: str
    confidence: float


class QuantitativeClaimDetector:
    """
    Detect quantitative claims in scientific text.

    DETECTS:
    - New metrics defined (AsI = |ΔM/σM| / |ΔP/σP|)
    - Formulas introduced
    - Threshold values specified (AsI >> 1, AsI ≈ 1, AsI << 1)
    - Quantitative comparisons made
    """

    # Patterns for detecting quantitative claims
    METRIC_DEFINITION_PATTERNS = [
        r'(\w+)\s*=\s*[\w\|\\/\+\-\*\s]+',  # X = formula
        r'(\w+)\s+(?:is|represents|denotes)\s+(?:defined as|given by)',
        r'(?:let|define)\s+(\w+)\s*='
    ]

    THRESHOLD_PATTERNS = [
        r'(\w+)\s*(?:>>|<<|≈|>=|<=|>)\s*[\d\.]+',  # X >> 1, X ≈ 1
        r'(\w+)\s*(?:much greater|much less|approximately)\s*(?:than)?\s*[\d\.]+'
    ]

    FORMULA_PATTERNS = [
        r'[\w\|\\/\+\-\*\s\^]+',  # Mathematical expressions
        r'\$[^$]+\$',  # LaTeX math
        r'\\\[?[^\\]+\\]?'  # LaTeX display math
    ]

    def __init__(self):
        self.claims: List[QuantitativeClaim] = []

    def detect_claims(self, text: str) -> List[QuantitativeClaim]:
        """
        Detect all quantitative claims in text.

        Returns list of claims that need validation.
        """
        claims = []
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check for metric definitions
            metric_matches = self._detect_metric_definitions(sentence)
            for match in metric_matches:
                claims.append(match)

            # Check for threshold statements
            threshold_matches = self._detect_thresholds(sentence)
            for match in threshold_matches:
                claims.append(match)

            # Check for formulas
            formula_matches = self._detect_formulas(sentence)
            for match in formula_matches:
                claims.append(match)

        self.claims = claims
        return claims

    def _detect_metric_definitions(self, sentence: str) -> List[QuantitativeClaim]:
        """Detect metric definitions like 'AsI = |ΔM/σM| / |ΔP/σP|'"""
        claims = []

        for pattern in self.METRIC_DEFINITION_PATTERNS:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                # Extract metric name
                metric_name = match.group(1) if match.lastindex >= 1 else match.group(0)

                # Extract formula if present
                formula_match = re.search(r'=\s*([\w\|\\/\+\-\*\s\^]+)', sentence)
                formula = formula_match.group(1) if formula_match else None

                # Extract variables from formula
                variables = {}
                if formula:
                    # Find all variable names (simplified)
                    var_matches = re.findall(r'(\w+)', formula)
                    for var in var_matches:
                        if var not in variables and not var.isdigit():
                            variables[var] = "variable"

                claims.append(QuantitativeClaim(
                    claim_text=sentence,
                    claim_type="metric_definition",
                    location=sentence,
                    variables=variables,
                    formula=formula
                ))

        return claims

    def _detect_thresholds(self, sentence: str) -> List[QuantitativeClaim]:
        """Detect threshold statements like 'AsI >> 1 indicates molecular dominance'"""
        claims = []

        for pattern in self.THRESHOLD_PATTERNS:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                metric_name = match.group(1) if match.lastindex >= 1 else "unknown"

                # Extract threshold value
                value_match = re.search(r'[\d\.]+', sentence)
                threshold = value_match.group() if value_match else None

                claims.append(QuantitativeClaim(
                    claim_text=sentence,
                    claim_type="threshold",
                    location=sentence,
                    variables={},
                    claimed_value=threshold
                ))

        return claims

    def _detect_formulas(self, sentence: str) -> List[QuantitativeClaim]:
        """Detect mathematical formulas"""
        claims = []

        # Look for sentences with mathematical expressions
        for pattern in self.FORMULA_PATTERNS:
            if re.search(pattern, sentence):
                claims.append(QuantitativeClaim(
                    claim_text=sentence,
                    claim_type="formula",
                    location=sentence,
                    variables={},
                    formula=re.search(pattern, sentence).group(0) if re.search(pattern, sentence) else None
                ))

        return claims


class QuantitativeValidator:
    """
    Validate that quantitative claims have appropriate quantitative support.

    VALIDATES:
    - New metrics have worked examples
    - Formulas have numerical demonstration
    - Thresholds have justification
    - Signal-to-noise claims have concrete examples
    """

    def __init__(self):
        self.detector = QuantitativeClaimDetector()
        self.issues: List[ValidationIssue] = []

    def validate(self, text: str) -> List[ValidationIssue]:
        """
        Validate quantitative claims in text.

        Returns list of validation issues found.
        """
        issues = []
        claims = self.detector.detect_claims(text)

        for claim in claims:
            # Check if claim has worked example in surrounding text
            worked_example_present = self._check_for_worked_example(text, claim)

            if not worked_example_present:
                if claim.claim_type == "metric_definition":
                    issues.append(self._create_worked_example_issue(claim))
                elif claim.claim_type == "threshold":
                    issues.append(self._create_threshold_justification_issue(claim))
                elif claim.claim_type == "formula":
                    issues.append(self._create_formula_demonstration_issue(claim))

            # Check for signal-to-noise justification
            if 'signal' in text.lower() and 'noise' in text.lower():
                if not self._check_for_signal_noise_example(text):
                    issues.append(self._create_signal_noise_issue(text))

        self.issues = issues
        return issues

    def _check_for_worked_example(self, text: str, claim: QuantitativeClaim) -> bool:
        """
        Check if text contains a worked example for the claim.

        INDICATORS of worked example:
        - "For example" followed by numbers
        - "Consider" followed by concrete values
        - Hypothetical data with calculations
        - Step-by-step demonstration
        """
        text_lower = text.lower()

        # Look for worked example indicators
        example_indicators = [
            'for example',
            'consider',
            'worked example',
            'hypothetical data',
            'suppose',
            'imagine'
        ]

        has_indicator = any(indicator in text_lower for indicator in example_indicators)

        # Look for numerical calculations
        has_calculation = bool(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text))

        # Look for step-by-step language
        has_steps = 'step' in text_lower or 'calculation' in text_lower

        return has_indicator and (has_calculation or has_steps)

    def _check_for_signal_noise_example(self, text: str) -> bool:
        """Check if signal-to-noise rationale has concrete example"""
        # Look for numbers in context of signal/noise
        signal_noise_section = re.search(
            r'signal.*?noise.*?[:\.].*?(?:\n|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if signal_noise_section:
            section_text = signal_noise_section.group(0)
            # Check for numbers
            has_numbers = bool(re.search(r'\d+\.?\d*', section_text))
            return has_numbers

        return False

    def _create_worked_example_issue(self, claim: QuantitativeClaim) -> ValidationIssue:
        """Create validation issue for missing worked example"""
        metric_name = self._extract_metric_name(claim)

        return ValidationIssue(
            validation_type=ValidationType.WORKED_EXAMPLE,
            severity=ValidationSeverity.CRITICAL,
            claim=claim,
            description=f"Metric '{metric_name}' introduced without worked example",
            what_is_missing=f"Complete worked example with hypothetical data, step-by-step calculation, and interpretation",
            why_it_matters=f"Quantitative metrics require concrete instantiation to be understood and validated. Without worked example, the formula is abstract and readers cannot verify it is correctly specified or appropriately interpreted.",
            suggested_addition=self._generate_worked_example_suggestion(claim),
            confidence=0.90
        )

    def _create_threshold_justification_issue(self, claim: QuantitativeClaim) -> ValidationIssue:
        """Create validation issue for unjustified threshold"""
        threshold = claim.claimed_value if claim.claimed_value else "specified"

        return ValidationIssue(
            validation_type=ValidationType.PARAMETER_VALUE,
            severity=ValidationSeverity.MAJOR,
            claim=claim,
            description=f"Threshold value '{threshold}' introduced without justification",
            what_is_missing="Justification for why this threshold value is meaningful",
            why_it_matters="Threshold values should be empirically justified or theoretically grounded. Arbitrary thresholds undermine the metric's validity.",
            suggested_addition=f"Add explanation: 'The threshold of {threshold} is based on [empirical observations / theoretical considerations / prior literature]'",
            confidence=0.75
        )

    def _create_formula_demonstration_issue(self, claim: QuantitativeClaim) -> ValidationIssue:
        """Create validation issue for formula without demonstration"""
        return ValidationIssue(
            validation_type=ValidationType.WORKED_EXAMPLE,
            severity=ValidationSeverity.MAJOR,
            claim=claim,
            description=f"Formula introduced without numerical demonstration",
            what_is_missing="Concrete example showing formula calculation",
            why_it_matters="Formulas need numerical demonstration to verify correctness and show readers how to apply them.",
            suggested_addition="Add numerical example: 'For instance, if [values], then [calculation] = [result]'",
            confidence=0.80
        )

    def _create_signal_noise_issue(self, text: str) -> ValidationIssue:
        """Create validation issue for signal-to-noise without example"""
        return ValidationIssue(
            validation_type=ValidationType.SIGNAL_NOISE_JUSTIFICATION,
            severity=ValidationSeverity.MAJOR,
            claim=QuantitativeClaim(
                claim_text="Signal-to-noise discussion",
                claim_type="discussion",
                location=text,
                variables={}
            ),
            description="Signal-to-noise rationale discussed without concrete example",
            what_is_missing="Example showing low vs high signal-to-noise scenarios",
            why_it_matters="Readers need concrete examples to understand why signal-to-noise ratio matters more than raw effect sizes.",
            suggested_addition="Add example: 'If complete knockout changes CV by 0.20 ± 0.05 (signal-to-noise = 4.0) while osmotic shock changes CV by 0.10 ± 0.08 (signal-to-noise = 1.25), the molecular perturbation is more reliable despite smaller effect size.'",
            confidence=0.85
        )

    def _extract_metric_name(self, claim: QuantitativeClaim) -> str:
        """Extract metric name from claim"""
        if claim.formula:
            # Try to extract from formula context
            match = re.search(r'(\w+)\s*=', claim.location)
            if match:
                return match.group(1)

        return "metric"

    def _generate_worked_example_suggestion(self, claim: QuantitativeClaim) -> str:
        """Generate suggestion for worked example"""
        metric_name = self._extract_metric_name(claim)

        return f"""Add complete worked example section for {metric_name}:

### Worked Example: SOS Checkpoint

**Experimental setup**:
- Molecular perturbation: UV-induced DNA damage
- Physical perturbation: Osmotic upshock
- Measured outcome: Division timing coefficient of variation (CV)

**Hypothetical data**:
- Control: CV = 0.15 ± 0.02 (n=20)
- UV damage (molecular): Division timing = 120 ± 10 min vs control 60 ± 5 min
  ΔM = 60 min, σM = 10 min, |ΔM/σM| = 6.0
- Osmotic shock (physical): Division timing = 75 ± 20 min
  ΔP = 15 min, σP = 20 min, |ΔP/σP| = 0.75

**Calculation**:
{metric_name} = |ΔM/σM| / |ΔP/σP| = 6.0 / 0.75 = 8.0

**Interpretation**:
{metric_name} = 8.0 >> 1, indicating strong molecular dominance (Type A). The molecular perturbation has a large, reliable effect while the physical perturbation has a smaller, more variable effect.
"""

    def generate_validation_report(self, issues: List[ValidationIssue]) -> str:
        """Generate formatted validation report"""
        if not issues:
            return "## Quantitative Validation Report\n\n**Result**: PASSED - All quantitative claims have appropriate support.\n"

        report = "## Quantitative Validation Report\n\n"
        report += f"**Result**: NEEDS ATTENTION - {len(issues)} issue(s) found.\n\n"

        # Group by severity
        critical = [i for i in issues if i.severity == ValidationSeverity.CRITICAL]
        major = [i for i in issues if i.severity == ValidationSeverity.MAJOR]
        moderate = [i for i in issues if i.severity == ValidationSeverity.MODERATE]

        if critical:
            report += "### CRITICAL Issues (must fix)\n\n"
            for issue in critical:
                report += f"- **{issue.description}**\n"
                report += f"  - *Why it matters*: {issue.why_it_matters}\n"
                report += f"  - *Suggested*: {issue.suggested_addition[:100]}...\n\n"

        if major:
            report += "### MAJOR Issues (should fix)\n\n"
            for issue in major:
                report += f"- **{issue.description}**\n"
                report += f"  - *Why it matters*: {issue.why_it_matters}\n"
                report += f"  - *Suggested*: {issue.suggested_addition[:100]}...\n\n"

        if moderate:
            report += "### MODERATE Issues (nice to have)\n\n"
            for issue in moderate:
                report += f"- **{issue.description}**\n"
                report += f"  - *Suggested*: {issue.suggested_addition[:100]}...\n\n"

        return report


class QuantitativeValidationEngine:
    """
    Main interface for quantitative validation.

    USAGE:
        engine = QuantitativeValidationEngine()
        issues = engine.validate(text)
        report = engine.generate_report(issues)
    """

    def __init__(self):
        self.validator = QuantitativeValidator()

    def validate(self, text: str) -> List[ValidationIssue]:
        """Validate quantitative claims in text"""
        return self.validator.validate(text)

    def generate_report(self, issues: List[ValidationIssue]) -> str:
        """Generate validation report"""
        return self.validator.generate_validation_report(issues)

    def get_summary(self, issues: List[ValidationIssue]) -> Dict[str, Any]:
        """Get summary of validation results"""
        if not issues:
            return {
                'total_issues': 0,
                'status': 'passed',
                'recommendation': 'All quantitative claims have appropriate support.'
            }

        # Count by severity
        severity_counts = {}
        for issue in issues:
            severity = issue.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Count by type
        type_counts = {}
        for issue in issues:
            vtype = issue.validation_type.value
            type_counts[vtype] = type_counts.get(vtype, 0) + 1

        # Determine recommendation
        if severity_counts.get('critical', 0) > 0:
            recommendation = "Critical issues found. Must add worked examples before submission."
        elif severity_counts.get('major', 0) > 0:
            recommendation = "Major issues found. Strongly recommend addressing before submission."
        else:
            recommendation = "Moderate issues found. Consider addressing if time permits."

        return {
            'total_issues': len(issues),
            'status': 'failed',
            'severity_breakdown': severity_counts,
            'type_breakdown': type_counts,
            'recommendation': recommendation
        }


def create_quantitative_validation_engine() -> QuantitativeValidationEngine:
    """Factory function to create quantitative validation engine"""
    return QuantitativeValidationEngine()


# Singleton instance
_instance = None

def get_quantitative_validation_engine() -> QuantitativeValidationEngine:
    """Get or create singleton instance"""
    global _instance
    if _instance is None:
        _instance = create_quantitative_validation_engine()
    return _instance
