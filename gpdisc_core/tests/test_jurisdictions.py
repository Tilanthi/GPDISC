"""Stage 8 Task 8.3: jurisdictions — whose rules is this doctor under?

GPDISC's regulatory layer is UK-deep. The tests hold the honesty
invariant: the consultation RECORD SAYS which ruleset it ran under; a
non-UK ruleset is WHO-neutral with a verify-national-law caveat, never
a fabricated national guideline; the deep UK packages declare their
scope; and UK outputs are flagged as non-transferring when another
jurisdiction is active.
"""
import pytest

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.jurisdictions import (
    JURISDICTIONS, WHO_NEUTRAL, JurisdictionRules,
    jurisdiction_for, ruleset_line,
)

PIPE = ConsultationPipeline()


class TestRegistry:
    def test_uk_ruleset_is_grounded(self):
        uk = JURISDICTIONS["UK"]
        assert uk.grounded and uk.uk_packages_valid
        assert uk.emergency_number == "999"
        assert "NICE" in uk.guideline_basis
        assert "DVLA" in uk.driving and "Med3" in uk.certification

    def test_who_neutral_is_honest_about_being_generic(self):
        assert not WHO_NEUTRAL.grounded
        assert not WHO_NEUTRAL.uk_packages_valid
        assert "verify" in WHO_NEUTRAL.summary_line().lower()

    def test_every_ruleset_declares_every_domain(self):
        for code, r in JURISDICTIONS.items():
            for domain in ("emergency_number", "guideline_basis",
                           "notification", "controlled_drugs",
                           "certification", "driving", "consent"):
                assert getattr(r, domain), (code, domain)

    def test_known_aliases_resolve(self):
        assert jurisdiction_for({"country": "england"}).code == "UK"
        assert jurisdiction_for({"jurisdiction": "Australia"}).code == "AU"
        assert jurisdiction_for({"country": "usa"}).code == "US"
        assert jurisdiction_for({"country": "India"}).code == "IN"

    def test_unknown_country_is_who_neutral_not_fabricated(self):
        """A country with no adapter must never get invented national
        rules — WHO-neutral with the verify note is the honest answer."""
        r = jurisdiction_for({"country": "Brazil"})
        assert r is WHO_NEUTRAL
        assert "verify national law" in r.summary_line().lower()

    def test_no_context_defaults_to_uk(self):
        assert jurisdiction_for(None).code == "UK"
        assert jurisdiction_for({}).code == "UK"


class TestRecordCarriesRuleset:
    def test_summary_states_uk_ruleset_by_default(self):
        rec = PIPE.run("sore throat for two days", {})
        assert "Ruleset: United Kingdom" in rec.summary()
        assert "999" in rec.ruleset

    def test_us_record_states_911_and_flags_uk_outputs(self):
        rec = PIPE.run("sore throat for two days, difficulty swallowing",
                       {"jurisdiction": "US"})
        assert "United States" in rec.ruleset
        assert "911" in rec.ruleset
        assert "do NOT transfer" in rec.ruleset or \
            "not transfer" in rec.ruleset.lower()

    def test_au_record_states_000(self):
        rec = PIPE.run("knee pain after a fall", {"country": "Australia"})
        assert "000" in rec.ruleset

    def test_unknown_country_record_gets_verify_caveat(self):
        rec = PIPE.run("fever and cough for three days",
                       {"country": "Kenya"})
        assert "Ruleset: WHO-neutral" in rec.ruleset
        assert "verify national law" in rec.ruleset.lower()

    def test_ruleset_line_changes_nothing_clinical(self):
        text = "crushing central chest pain for 30 minutes, sweating"
        uk = PIPE.run(text, {})
        us = PIPE.run(text, {"jurisdiction": "US"})
        assert uk.escalation == us.escalation == "emergency"
        assert uk.ranked_differential == us.ranked_differential


class TestUKPackageTagging:
    def test_uk_practice_declares_its_jurisdiction(self):
        from gpdisc_core.uk_practice import JURISDICTION
        assert JURISDICTION == "UK"

    def test_uk_registry_entry_matches_package_tag(self):
        import gpdisc_core.uk_practice as ukp
        assert JURISDICTIONS[ukp.JURISDICTION].uk_packages_valid

    def test_non_uk_rulesets_declare_uk_packages_invalid(self):
        for code, r in JURISDICTIONS.items():
            if code == "UK":
                continue
            assert not r.uk_packages_valid, code
