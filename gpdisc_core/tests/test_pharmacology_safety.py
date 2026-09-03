"""
Regression tests for the pharmacology domain's drug-interaction safety layer.

Regression for the standalone audit finding (2026-08-21): the domain imported
``..safety.drug_interactions`` (two dots = gpdisc_core.domains.safety, which
does not exist) instead of ``...safety.drug_interactions`` (three dots =
gpdisc_core.safety.drug_interactions). The guarded import failed silently,
so every pharmacology consultation ran with the interaction checker set to
None - i.e. without the drug-interaction checking the domain advertises.

Run from repo root:  python3 -m pytest gpdisc_core/tests/test_pharmacology_safety.py -v
"""

import pytest

from gpdisc_core.domains import pharmacology
from gpdisc_core.safety.drug_interactions import DrugInteractionChecker


def test_interaction_checker_imported_not_none():
    """The guarded import must actually resolve - a None checker is a silent
    loss of a patient-safety feature and must fail loudly in tests."""
    assert pharmacology.check_patient_medications is not None, (
        "pharmacology.check_patient_medications is None: the drug-interaction "
        "import failed silently (check relative import depth: it must be "
        "...safety.drug_interactions, three dots)"
    )
    assert pharmacology.check_new_prescription is not None
    assert pharmacology.DrugInteractionChecker is DrugInteractionChecker
    assert pharmacology.InteractionSeverity is not None


def test_domain_uses_interaction_checker():
    """The PharmacologyDomain must expose interaction checking in its
    capability set, and that capability must be backed by real code."""
    domain = pharmacology.PharmacologyDomain()
    assert "drug_interaction_checking" in domain.get_default_config().capabilities


def test_check_patient_medications_runs():
    """End-to-end: checking a realistic medication list returns structured
    output (smoke-level - correctness of severity mapping lives with the
    checker module's own tests)."""
    result = pharmacology.check_patient_medications(
        ["warfarin", "aspirin"]
    )
    assert result is not None
