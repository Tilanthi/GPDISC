"""GPDISC palliative care: terminal symptom control and end-of-life
planning (Stage 7 Task 7.4). The consultation front door routes
end-of-life presentations here instead of declaring them outside
scope.

All doses are decision-support scaffolding carrying a standing
instruction to confirm against the local palliative formulary.
"""
from gpdisc_core.palliative_care.symptom_control import (
    DRUG_ROUTE_TABLE,
    TERMINAL_SYMPTOMS,
    cant_swallow_route_advice,
    eol_guidance_for,
    terminal_symptom_control,
)
from gpdisc_core.palliative_care.planning import end_of_life_plan

__all__ = [
    "DRUG_ROUTE_TABLE",
    "TERMINAL_SYMPTOMS",
    "cant_swallow_route_advice",
    "eol_guidance_for",
    "end_of_life_plan",
    "terminal_symptom_control",
]
