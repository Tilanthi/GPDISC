"""Jurisdictions — whose rules is this doctor working under?

Stage 8 Task 8.3 (Tier 3). GPDISC's regulatory layer is UK-deep (NICE/
CKS, DVLA, UKHSA notification, Misuse of Drugs Regulations, Med3). A
doctor in another country must be TOLD that, not left to assume NICE
guidance or a 2ww pathway transfers. Honesty about the ruleset is the
anti-hallucination principle applied to regulation itself.

Design: a WHO-neutral base describes the domains that vary by
jurisdiction (notification, controlled drugs, certification, driving,
consent, emergency number) with WHO/IHR-level generic guidance; a UK
adapter grounds those domains in the UK sources the uk_practice
package already implements. Any other named jurisdiction resolves to
the WHO-neutral base with an explicit 'verify national law' stance —
never a fabricated national rule.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class JurisdictionRules:
    """The domains that vary by jurisdiction, and what this system
    actually has for each."""
    code: str
    name: str
    emergency_number: str
    guideline_basis: str              # whose guidelines ground the advice
    notification: str                 # notifiable-disease framework
    controlled_drugs: str             # prescribing authority regime
    certification: str                # sickness certification style
    driving: str                      # fitness-to-drive regime
    consent: str                      # capacity/consent framework
    grounded: bool = True             # False = WHO-neutral generic only
    verify_note: str = ""
    # the deep UK packages: usable as-is only when grounded == "UK"
    uk_packages_valid: bool = False

    def summary_line(self) -> str:
        line = (f"Ruleset: {self.name} — guidelines {self.guideline_basis}; "
                f"emergency number {self.emergency_number}; "
                f"notification per {self.notification}.")
        if not self.grounded:
            line += (" WHO-neutral basis: verify national law and "
                     "guidelines before acting.")
        if not self.uk_packages_valid:
            line += (" UK-specific outputs (2ww pathways, DVLA rules, "
                     "Med3 fit notes, UK controlled-drug schedules) do "
                     "NOT transfer to this jurisdiction.")
        return line


WHO_NEUTRAL = JurisdictionRules(
    code="WHO",
    name="WHO-neutral (jurisdiction unspecified)",
    emergency_number="local emergency number",
    guideline_basis="WHO clinical guidance",
    notification="WHO International Health Regulations + national list",
    controlled_drugs="UN conventions on narcotic/psychotropic substances "
                     "+ national law",
    certification="national sick-leave certification rules",
    driving="national licensing authority rules",
    consent="national capacity and consent law; WHO consent principles",
    grounded=False,
    verify_note="national law decides",
)

JURISDICTIONS: Dict[str, JurisdictionRules] = {
    "UK": JurisdictionRules(
        code="UK",
        name="United Kingdom",
        emergency_number="999",
        guideline_basis="NICE / CKS (see guideline index)",
        notification="UKHSA notifiable diseases (Health Protection "
                     "Regulations 2010)",
        controlled_drugs="Misuse of Drugs Regulations 2001, schedules "
                         "1-5 (see controlled_drugs module)",
        certification="Med3 fit notes (see fit_note_guidance)",
        driving="DVLA fitness-to-drive, group 1 + 2 (see driving_rules)",
        consent="Mental Capacity Act 2005 two-stage test; Gillick "
                "competence for under-16s (see capacity_and_safeguarding)",
        grounded=True,
        uk_packages_valid=True,
    ),
    # named-but-unimplemented jurisdictions resolve to WHO-neutral with
    # their emergency number stated where it is commonly known — no
    # fabricated regulatory detail
    "AU": JurisdictionRules(
        code="AU",
        name="Australia",
        emergency_number="000",
        guideline_basis="WHO-neutral (Therapeutic Guidelines not loaded)",
        notification="national + state notifiable-diseases lists",
        controlled_drugs="national + state poisons schedules",
        certification="national medical certificate rules",
        driving="state licensing authority rules (Austroads guidance)",
        consent="state guardianship + capacity law",
        grounded=False, uk_packages_valid=False,
    ),
    "US": JurisdictionRules(
        code="US",
        name="United States",
        emergency_number="911",
        guideline_basis="WHO-neutral (USPSTF/CDC not loaded)",
        notification="state + CDC nationally notifiable conditions",
        controlled_drugs="DEA schedules",
        certification="FMLA/employer-specific certification",
        driving="state DMV rules",
        consent="state law; emergency exception doctrine",
        grounded=False, uk_packages_valid=False,
    ),
    "IN": JurisdictionRules(
        code="IN",
        name="India",
        emergency_number="112",
        guideline_basis="WHO-neutral (national programme guidance not "
                        "loaded)",
        notification="state/district health authority notification",
        controlled_drugs="NDPS Act schedules",
        certification="registered medical practitioner certificate",
        driving="state RTO rules",
        consent="Indian Majority Act + capacity at common law",
        grounded=False, uk_packages_valid=False,
    ),
}

# context keys the active jurisdiction may arrive under
_JURISDICTION_KEYS = ("jurisdiction", "country", "setting_country")
_ALIASES = {
    "united kingdom": "UK", "england": "UK", "scotland": "UK",
    "wales": "UK", "northern ireland": "UK", "uk": "UK", "gb": "UK",
    "australia": "AU", "aussie": "AU",
    "united states": "US", "usa": "US", "us": "US", "america": "US",
    "india": "IN",
}


def jurisdiction_for(context: Optional[Dict]) -> JurisdictionRules:
    """Resolve the active ruleset from a consultation context. No
    jurisdiction stated = the default the package is grounded in (UK);
    an unknown/unimplemented one = WHO-neutral with the verify note —
    never a fabricated national rule."""
    if not context:
        return JURISDICTIONS["UK"]
    for key in _JURISDICTION_KEYS:
        raw = context.get(key)
        if raw:
            code = _ALIASES.get(str(raw).strip().lower(),
                                str(raw).strip().upper())
            if code in JURISDICTIONS:
                return JURISDICTIONS[code]
            return WHO_NEUTRAL
    return JURISDICTIONS["UK"]


def ruleset_line(context: Optional[Dict]) -> str:
    """The ruleset statement for a consultation record. Always states
    the basis; the WHO-neutral and non-UK lines carry their caveats."""
    return jurisdiction_for(context).summary_line()
