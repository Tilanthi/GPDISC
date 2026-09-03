"""GPDISC UK practice layer (expertise program Stage 3).

UK-specific regulatory and policy knowledge: NICE/CKS index, 2ww cancer
referral criteria, DVLA driving rules, MCA/DNACPR/safeguarding, controlled
drugs, antimicrobial stewardship, high-risk prescribing monitoring, fit
notes. Vaccination/screening cohorts live in ``gpdisc_core.preventive_medicine``
(Stage 2) and are not duplicated here.
"""
from gpdisc_core.uk_practice.guidelines_index import (
    GuidelineRef,
    GUIDELINES,
    lookup_guideline,
)
from gpdisc_core.uk_practice.two_week_wait import (
    TwoWeekWaitRule,
    TWO_WEEK_WAIT_RULES,
    two_week_wait_check,
)
from gpdisc_core.uk_practice.dvla_rules import (
    DrivingRule,
    DRIVING_RULES,
    driving_rules,
)
from gpdisc_core.uk_practice.capacity_and_safeguarding import (
    capacity_two_stage_test,
    best_interests_checklist,
    dnacpr_principles,
    safeguarding_adult_types,
    safeguarding_children_levels,
    gillick_checklist,
    capacity_concern_keywords,
)
from gpdisc_core.uk_practice.controlled_drugs import (
    controlled_drug_class,
    prescribing_guardrails,
    CD_SCHEDULES,
    CD_SAFE_PRACTICE,
)
from gpdisc_core.uk_practice.antimicrobial_stewardship import (
    AntibioticGuidance,
    ANTIBIOTIC_GUIDANCE,
    antibiotic_for,
    stewardship_principles,
)
from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements,
    renal_flags,
    MONITORING,
)
from gpdisc_core.uk_practice.fit_notes import (
    fit_note_guidance,
    ADJUSTMENT_OPTIONS,
)

# 8.3: every output of this package is UK-law-and-guideline grounded.
# The jurisdiction layer reads this tag so a consultation running under
# another ruleset can say WHICH outputs do not transfer.
JURISDICTION = "UK"

__all__ = [
    "GuidelineRef", "GUIDELINES", "lookup_guideline",
    "TwoWeekWaitRule", "TWO_WEEK_WAIT_RULES", "two_week_wait_check",
    "DrivingRule", "DRIVING_RULES", "driving_rules",
    "capacity_two_stage_test", "best_interests_checklist",
    "dnacpr_principles", "safeguarding_adult_types",
    "safeguarding_children_levels", "gillick_checklist",
    "capacity_concern_keywords",
    "controlled_drug_class", "prescribing_guardrails",
    "CD_SCHEDULES", "CD_SAFE_PRACTICE",
    "AntibioticGuidance", "ANTIBIOTIC_GUIDANCE", "antibiotic_for",
    "stewardship_principles",
    "monitoring_requirements", "renal_flags", "MONITORING",
    "fit_note_guidance", "ADJUSTMENT_OPTIONS",
    "JURISDICTION",
]
