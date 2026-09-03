"""Test interpretation breadth (expertise program Stage 9, Task 9.2).

Pattern-level readers for the tests whose one-line answers steer whole
pathways: the ECG (rhythm, territory, the treat-first patterns), the
blood gas (disorder → cause → compensation → severity), the CSF (the
three-question method), and the bedside fluids (dipstick, spirometry,
joint aspirate, culture logic). Deterministic tables over text patterns
and numeric thresholds — no LLM, no fabrication: every reader says what
it does NOT settle.
"""
from .ecg import ECGReport, interpret_ecg
from .abg import ABGReport, interpret_abg
from .csf import CSFReport, interpret_csf
from .bedside_fluids import (
    PatternReport,
    interpret_urine_dip,
    interpret_pft,
    interpret_synovial_fluid,
    interpret_culture,
)

__all__ = [
    "ECGReport", "interpret_ecg",
    "ABGReport", "interpret_abg",
    "CSFReport", "interpret_csf",
    "PatternReport", "interpret_urine_dip", "interpret_pft",
    "interpret_synovial_fluid", "interpret_culture",
]
