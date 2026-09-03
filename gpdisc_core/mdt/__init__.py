"""GPDISC MDT layer (expertise program Stage 4).

The multi-agent consultation team: adversarial Diagnostic Challenger, six
MDT roles, a debate protocol, and the whole-patient multimorbidity review.
Deterministic rules over the Stage 1-3 knowledge — no LLM, no external
transmission.
"""
from gpdisc_core.mdt.challenger import (
    Challenge,
    ATTACK_TYPES,
    challenge_differential,
)
from gpdisc_core.mdt.roles import (
    MDTRole,
    MDT_ROLES,
    CONSULTANT_ROLES,
    contribute,
)
from gpdisc_core.mdt.debate import (
    MDTResult,
    run_mdt,
)
from gpdisc_core.mdt.multimorbidity import (
    TREATMENT_TENSIONS,
    ACB_SCORES,
    whole_patient_review,
)

__all__ = [
    "Challenge", "ATTACK_TYPES", "challenge_differential",
    "MDTRole", "MDT_ROLES", "CONSULTANT_ROLES", "contribute",
    "MDTResult", "run_mdt",
    "TREATMENT_TENSIONS", "ACB_SCORES", "whole_patient_review",
]
