"""Dataclass schema for the GPDISC condition knowledge base.

Split from knowledge.py so breadth modules can author entries without a
circular import. The public import path for consumers remains
``gpdisc_core.clinical_reasoning.knowledge``.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SymptomFrequency:
    symptom: str        # canonical snake_case token, must exist in SYMPTOM_SYNONYMS
    frequency: float    # proportion of this condition's presentations, 0-1
    specificity: float  # discriminating power toward this condition, 0-1


@dataclass
class InvestigationProfile:
    name: str
    purpose: str
    sensitivity: Optional[float] = None   # established value or None
    specificity: Optional[float] = None
    source: str = ""                      # e.g. "NICE CG95", "Wells 1997"


@dataclass
class ConditionProfile:
    condition_id: str
    name: str
    category: str                       # e.g. "cardiovascular", "infection"
    prevalence_per_consult: float       # rough prior among relevant GP consults
    symptoms: List[SymptomFrequency]
    discriminators: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    investigations: List[InvestigationProfile] = field(default_factory=list)
    management_first_line: str = ""
    referral_tier: str = "routine"      # self_care|routine|urgent|two_week_wait|emergency
    safety_net: str = ""
    dangerous_mimic_of: List[str] = field(default_factory=list)
    source: str = ""
