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


class TestParacetamolWarfarinInteraction:
    """Live-question finding (2026-09-04): 'Is it safe to take paracetamol
    alongside warfarin?' returned 'NO DRUG INTERACTIONS DETECTED' because the
    pair had no row in the table - absence of data was reported as absence of
    interaction. The row now exists; these locks pin both directions (the
    genuine pair flagged, benign pairs still clean, and the no-row answer
    honest about the table's limits)."""

    def test_pair_flagged_both_orders(self):
        c = DrugInteractionChecker()
        for a, b in [("paracetamol", "warfarin"), ("warfarin", "paracetamol")]:
            hit = c.check_interaction(a, b)
            assert hit is not None, f"{a} + {b} returned no interaction"
            assert hit.severity.value == "moderate"
            assert "INR" in hit.description

    def test_brand_and_us_aliases_also_match(self):
        c = DrugInteractionChecker()
        # acetaminophen (US) and coumadin (brand) must reach the same row
        assert c.check_interaction("acetaminophen", "coumadin") is not None

    def test_benign_pair_stays_clean(self):
        c = DrugInteractionChecker()
        assert c.check_interaction("paracetamol", "amlodipine") is None
        assert c.check_interaction("amlodipine", "paracetamol") is None

    def test_recommendations_carry_the_Practical_rules(self):
        c = DrugInteractionChecker()
        hit = c.check_interaction("paracetamol", "warfarin")
        joined = " ".join(hit.recommendations)
        assert "PREFERRED" in joined          # paracetamol stays first choice
        assert "INR" in joined                # monitoring instruction present
        assert "NSAID" in joined or "nsaid" in joined.lower()

    def test_medication_list_check_surfaces_the_pair(self):
        result = pharmacology.check_patient_medications(
            ["warfarin", "paracetamol"])
        assert result.has_interactions
        assert any("INR" in i.description for i in result.interactions)

    def test_domain_flags_paracetamol_warfarin(self):
        domain = pharmacology.PharmacologyDomain()
        r = domain.process_query("Can I take paracetamol with warfarin?")
        text = r["answer"] if isinstance(r, dict) else r.answer
        assert "NO DRUG INTERACTIONS DETECTED" not in text
        assert "paracetamol + warfarin" in text.lower() or \
            "warfarin + paracetamol" in text.lower() or \
            "moderate" in text.lower()

    def test_no_row_answer_is_honest_about_the_tables_limits(self):
        """A pair absent from the table must never read as an all-clear."""
        domain = pharmacology.PharmacologyDomain()
        r = domain.process_query("Can I take cetirizine with amlodipine?")
        text = r["answer"] if isinstance(r, dict) else r.answer
        assert "All combinations appear safe" not in text
        assert "appear safe" not in text
        # and it must defer to a comprehensive source
        assert "BNF" in text or "pharmacist" in text
