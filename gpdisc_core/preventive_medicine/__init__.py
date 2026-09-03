"""GPDISC preventive medicine package (expertise program Stage 2).

UK vaccination schedule (adult-relevant slice), NHS screening
programmes, and cardiovascular primary-prevention thresholds.
Local data only.
"""
from .schedules import VaccineEntry, VACCINES_UK, vaccine_due
from .screening import ScreeningEntry, SCREENING_UK, screening_due, prevention_check
from .cvd_prevention import cvd_prevention_advice

__all__ = [
    "VaccineEntry",
    "VACCINES_UK",
    "vaccine_due",
    "ScreeningEntry",
    "SCREENING_UK",
    "screening_due",
    "prevention_check",
    "cvd_prevention_advice",
]
