"""The clinical validator — GPDISC's prospective anti-hallucination layer.

Verification happens BEFORE output leaves the pipeline, on two levels:

1. CONSULT-level consistency (`validate_consultation`): the diagnostic
   record must agree with itself — an emergency-tier condition ranked at
   the top can never leave under a 'routine' label; a retained
   must-not-miss condition dropped without a word of exclusion is silent
   anchoring; a non-emergency disposition without a safety net is
   incomplete; safeguarding signals in the presenting complaint are
   surfaced, never missed.

2. CLAIM-level grounding (`verify_claim`): free-text clinical assertions
   must trace to the knowledge base — drug/renal claims against the
   prescribing-safety tables, monitoring claims against the monitoring
   schedules, guideline citations against the guideline index — or be
   corrected from the persistent clinical hallucination register.

Corrections only ever RAISE the level of concern. The register is local
JSON under gpdisc_core/data/memory/ — the same privacy boundary as all
patient data.
"""
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .knowledge import find_condition

DEFAULT_REGISTER_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "memory"
    / "clinical_hallucination_register.json")

# corpus referral tiers ranked by urgency of the action they demand
_TIER_LEVEL = {"self_care": 1, "routine": 1, "urgent": 2,
               "two_week_wait": 2, "emergency": 3}
_ESC_LEVEL = {"self_care": 1, "routine": 1, "urgent": 2, "emergency": 3}
_LEVEL_NAME = {1: "routine", 2: "urgent", 3: "emergency"}
# A single-token rank-1 leader must carry at least this much score to
# floor the escalation on its own (Stage 7 Task 7.1). Calibrated between
# the legitimate one-token leaders — tetanus-prone wound on
# 'tetanus status unknown' (0.29), SJS/TEN on 'new drug started'
# (0.26), SAH on 'thunderclap' (~0.45) — and a leaking-AAA entry
# topping an otherwise-empty differential at 0.04 on 'blacked out'
# (pure noise).
_GENUINE_LEADER_FLOOR = 0.20


def _matched_token_count(entry: dict) -> int:
    """How many distinct symptom tokens the engine matched for this entry,
    parsed from its reasons ('matched: fever, travel_context'). A
    single-token match is noise no matter how close the score. Empty or
    unparsable reasons count as multi-token so synthetic records (and any
    future reasons format) keep the pre-existing behaviour."""
    tokens = _matched_tokens(entry)
    return len(tokens) if tokens else 2


def _matched_tokens(entry: dict) -> List[str]:
    """The token ids the engine matched, parsed from reasons."""
    for r in entry.get("reasons") or []:
        if isinstance(r, str) and r.startswith("matched:"):
            tokens = [t.strip() for t in r[len("matched:"):].split(",")
                      if t.strip()]
            if tokens:
                return tokens
    return []


def _has_specific_token(entry: dict, condition) -> bool:
    """Does at least one MATCHED token carry discriminating weight
    (specificity >= 0.5)? An emergency-tier condition matched purely on
    generics — CO on 'headache, nausea' (specificity 0.20 / 0.10) — is
    the two-word version of the one-word noise the gate already rejects:
    it 999'd every hangover and altitude headache (8.1). Unknown
    condition or unparsable reasons stay permissive (pre-existing
    behaviour)."""
    tokens = _matched_tokens(entry)
    if not tokens or condition is None:
        return True
    spec = {s.symptom: s.specificity for s in condition.symptoms}
    return any(spec.get(t, 0.0) >= 0.5 for t in tokens)

_SAFE_WORDS = re.compile(r"\b(safe|safely|fine|okay|ok|continue|"
                         r"no problem|carry on|keep taking)\b", re.I)
_EGFR = re.compile(r"egfr\s*(?:of|=|is|:)?\s*(\d+)", re.I)
_MONITORING_DRUGS = re.compile(
    r"\b(lithium|methotrexate|clozapine|amiodarone|digoxin|doac|apixaban|"
    r"rivaroxaban|warfarin|ace inhibitor|ramipril|enalapril|nsaid|"
    r"ibuprofen|naproxen|metformin|sodium valproate|valproate)\b", re.I)
_CITATION = re.compile(r"\b(NICE|CKS|NG\s?\d+|CS\s?\d+)\b", re.I)
_CITATION_STRIP = re.compile(
    r"\b(NICE|CKS|NG\s?\d+|CS\s?\d+|guidance|guideline|says|state|"
    r"recommends?|per|according to|the)\b", re.I)


@dataclass
class ValidationFinding:
    check: str
    severity: str          # "block" | "flag"
    message: str
    evidence: str = ""


@dataclass
class ValidationReport:
    passed: bool = True
    findings: List[ValidationFinding] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)

    def summary(self) -> str:
        if not self.findings:
            return "Validation: PASS — no inconsistencies, claims grounded."
        lines = []
        for f in self.findings:
            mark = "BLOCK" if f.severity == "block" else "FLAG "
            lines.append(f"[{mark}] {f.check}: {f.message}")
            if f.evidence:
                lines.append(f"        evidence: {f.evidence}")
        for c in self.corrections:
            lines.append(f"[FIXED] {c}")
        return "Validation:\n" + "\n".join(lines)


@dataclass
class RegisterEntry:
    claim: str
    correct_value: str
    source: str
    first_seen: str = ""

    @property
    def fingerprint(self) -> str:
        return re.sub(r"\s+", " ", self.claim.lower().strip())


class ClinicalValidator:
    def __init__(self, register_path: Optional[Path] = None):
        self.register_path = Path(register_path) if register_path \
            else DEFAULT_REGISTER_PATH
        self._register: Dict[str, RegisterEntry] = self._load_register()

    # ------------------------------------------------------------------
    # consult-level consistency
    # ------------------------------------------------------------------
    def validate_consultation(self, rec) -> ValidationReport:
        report = ValidationReport()
        self._check_escalation_consistency(rec, report)
        self._check_retained_exclusion(rec, report)
        self._check_safety_net(rec, report)
        self._check_safeguarding(rec, report)
        report.passed = not any(f.severity == "block" for f in report.findings)
        return report

    def _check_escalation_consistency(self, rec, report) -> None:
        ranked = list(getattr(rec, "ranked_differential", []) or [])
        if not ranked:
            return
        current = _ESC_LEVEL.get(rec.escalation, 1)

        # top-3 leaders: the corpus tier of a ranked leader is the floor
        # for the stated escalation — the engine 'knowing' ACS is first
        # while saying 'routine' is the failure mode this exists for.
        # Contender gate, two criteria (both calibrated 2026-09-03):
        # 1. score >= 0.5x the leader — an emergency-tier condition matched
        #    on one generic word scores far below the leader (GCA on
        #    'headache' at 0.1 beside a 0.4 tension-headache leader).
        # 2. >= 2 matched symptom tokens — when EVERY entry scores low the
        #    ratio is meaningless: eclampsia sat at 0.93x an 8-week
        #    miscarriage leader by matching the single word 'pregnant'.
        #    A one-token match is noise regardless of ratio.
        #
        # The RANK-1 leader floors UNCONDITIONALLY only when it is a
        # genuine commitment: >= 2 matched tokens, or a single token
        # carrying real credit (score >= _GENUINE_LEADER_FLOOR — SAH on
        # 'thunderclap' scores ~0.45; 'blacked out when I stood up' once
        # made a leaking-AAA entry rank-1 at 0.04 and floored every
        # simple faint to emergency). A rank-1 under both thresholds is
        # the top of an EMPTY differential, not a diagnosis (Stage 7).
        #
        # Criterion 3 (8.1): an EMERGENCY-tier entry matched entirely on
        # low-specificity generics cannot floor the escalation — CO on
        # 'headache, nausea' (0.20/0.10) made every hangover and every
        # altitude headache a 999. At least one matched token must be a
        # real discriminator.
        leader_score = max(d.get("score", 0) for d in ranked[:3]) \
            if ranked else 0
        required = current
        why = ""
        for i, d in enumerate(ranked[:3]):
            if leader_score > 0 and d.get("score", 0) < 0.5 * leader_score:
                continue
            if i > 0 and _matched_token_count(d) < 2:
                continue
            if i == 0 and _matched_token_count(d) < 2 \
                    and d.get("score", 0) < _GENUINE_LEADER_FLOOR:
                continue
            c = find_condition(d.get("condition_id", ""))
            if not c:
                continue
            tier = _TIER_LEVEL.get(c.referral_tier, 1)
            if tier == 3 and not _has_specific_token(d, c):
                continue
            if tier > required:
                required = tier
                why = f"{d.get('name', d.get('condition_id'))} ({c.referral_tier})"
        if required > current:
            rec.escalation = _LEVEL_NAME[required]
            correction = (f"escalation raised { _LEVEL_NAME[current] } -> "
                          f"{rec.escalation}: ranked leader {why}")
            if "two_week_wait" in (why or ""):
                correction += " — urgent suspected-cancer (2ww) pathway"
            rec.referral = (getattr(rec, "referral", "") + " | " + correction).strip(" |")
            if required == 3 and "999" not in (rec.safety_net or ""):
                rec.safety_net = ("Emergency escalation on validation — "
                                  "the ranked differential demands it. " +
                                  (rec.safety_net or "")).strip()
            report.findings.append(ValidationFinding(
                check="escalation_consistency", severity="block",
                message=f"escalation '{_LEVEL_NAME[current]}' contradicts the "
                        f"ranked differential ({why})",
                evidence=correction))
            report.corrections.append(correction)

    def _check_retained_exclusion(self, rec, report) -> None:
        ranked_ids = {d.get("condition_id") for d in
                      getattr(rec, "ranked_differential", []) or []}
        for d in getattr(rec, "dangerous_alternatives", []) or []:
            cid = d.get("condition_id", "")
            c = find_condition(cid)
            if c is None or c.referral_tier != "emergency":
                continue          # rule ids from emergency short-circuit
            if cid in ranked_ids:
                continue          # ranked and addressed
            evidence_text = " ".join([
                getattr(rec, "treatment", "") or "",
                getattr(rec, "referral", "") or "",
                getattr(rec, "safety_net", "") or ""]).lower()
            name = c.name.lower()
            mentioned = (cid.split("_")[0] in evidence_text
                         or name.split("(")[0].strip() in evidence_text
                         or "exclude" in evidence_text
                         or "rule out" in evidence_text
                         or "red flag" in evidence_text)
            if not mentioned:
                report.findings.append(ValidationFinding(
                    check="retained_without_exclusion", severity="flag",
                    message=f"must-not-miss condition {c.name} retained but "
                            f"never addressed — document why it is excluded "
                            f"or ask its discriminating question",
                    evidence=cid))

    def _check_safety_net(self, rec, report) -> None:
        if rec.escalation != "emergency" and not (rec.safety_net or "").strip():
            report.findings.append(ValidationFinding(
                check="safety_net_presence", severity="flag",
                message="non-emergency disposition without safety-netting"))

    def _check_safeguarding(self, rec, report) -> None:
        try:
            from gpdisc_core.uk_practice import capacity_concern_keywords
        except Exception:
            return
        hits = capacity_concern_keywords(rec.presenting_complaint or "")
        if hits:
            report.findings.append(ValidationFinding(
                check="safeguarding_signal", severity="flag",
                message="safeguarding indicator in the presenting complaint — "
                        "explore it; a hit means 'ask', never 'this is abuse'",
                evidence=", ".join(hits)))

    # ------------------------------------------------------------------
    # claim-level grounding
    # ------------------------------------------------------------------
    def verify_claim(self, text: str) -> ValidationReport:
        """Grounding check for a free-text claim. Unlike a consultation
        (where advisory flags do not fail the record), a claim with ANY
        grounding finding is 'not verified' — passed is False."""
        report = ValidationReport()
        t = text or ""
        self._check_register(t, report)
        self._check_renal(t, report)
        self._check_monitoring(t, report)
        self._check_citation(t, report)
        report.passed = not report.findings
        return report

    def _check_register(self, text: str, report) -> None:
        fp = re.sub(r"\s+", " ", text.lower().strip())
        if fp in self._register:
            e = self._register[fp]
            report.findings.append(ValidationFinding(
                check="register_match", severity="block",
                message=f"known hallucination: '{e.claim}'",
                evidence=f"use instead: {e.correct_value} (source: {e.source})"))

    def _check_renal(self, text: str, report) -> None:
        m = _EGFR.search(text)
        if not m or not _SAFE_WORDS.search(text):
            return
        from gpdisc_core.uk_practice.prescribing_safety import renal_flags
        for drug_m in _MONITORING_DRUGS.finditer(text):
            drug = drug_m.group(0).lower()
            flags = renal_flags(drug, egfr=int(m.group(1)))
            if flags:
                report.findings.append(ValidationFinding(
                    check="claim_grounding", severity="block",
                    message=f"renal claim contradicts the knowledge base for "
                            f"{drug} at eGFR {m.group(1)}",
                    evidence="; ".join(flags)))

    def _check_monitoring(self, text: str, report) -> None:
        t = text.lower()
        if not re.search(r"no (monitoring|bloods|blood tests)", t):
            return
        from gpdisc_core.uk_practice.prescribing_safety import (
            monitoring_requirements)
        for drug_m in _MONITORING_DRUGS.finditer(text):
            drug = drug_m.group(0).lower()
            if monitoring_requirements(drug):
                report.findings.append(ValidationFinding(
                    check="claim_grounding", severity="flag",
                    message=f"claim of no monitoring for {drug} contradicts "
                            f"the monitoring schedule",
                    evidence="; ".join(monitoring_requirements(drug))))

    def _check_citation(self, text: str, report) -> None:
        if not _CITATION.search(text):
            return
        from gpdisc_core.uk_practice import lookup_guideline
        from gpdisc_core.uk_practice.guidelines_index import GUIDELINES

        # a specific numbered reference (NG99, CS17...) must exist in the
        # index — invented numbers are the classic citation hallucination
        claimed_refs = [m.group(1).replace(" ", "").upper()
                        for m in re.finditer(r"\b(NG\s?\d+|CS\s?\d+)\b",
                                             text, re.I)]
        if claimed_refs:
            _ref_re = re.compile(r"\b(NG|CS)\s?\d+", re.I)
            rows_by_ref: Dict[str, list] = {}
            for g in GUIDELINES:
                m = _ref_re.search(g.nice_ref)
                if m:
                    rows_by_ref.setdefault(
                        m.group(0).replace(" ", "").upper(), []).append(g)
            missing = [r for r in claimed_refs if r not in rows_by_ref]
            if missing:
                report.findings.append(ValidationFinding(
                    check="claim_grounding", severity="flag",
                    message="specific guideline reference not in the index — "
                            "verify before use",
                    evidence=f"unknown references: {', '.join(missing)}"))
                return

            # existing number, WRONG TOPIC: if the claim's own topic words
            # map to an index row, the cited ref should be (one of) that
            # row's — NG111-for-lower-UTI mirrors passed the old number-
            # exists check, which is exactly how the audit's wrong-topic
            # citations survived
            topic_rows = lookup_guideline(text)
            if topic_rows:
                cited_rows = [g for r in claimed_refs
                              for g in rows_by_ref.get(r, [])]
                if not set(map(id, topic_rows)) & set(map(id, cited_rows)):
                    report.findings.append(ValidationFinding(
                        check="claim_grounding", severity="flag",
                        message="guideline reference exists but covers a "
                                "different topic than the claim — verify "
                                "before use",
                        evidence=f"claim topic matches "
                                 f"{', '.join(g.nice_ref for g in topic_rows)}"
                                 f" ({', '.join(g.topic for g in topic_rows)})"
                                 f" but cites {', '.join(claimed_refs)}"))

        # otherwise the topic area itself must be grounded: the index
        # matches topic-in-text, so try the whole claim, then word pairs,
        # then single words
        content = _CITATION_STRIP.sub(" ", text)
        words = [w for w in re.findall(r"[a-z]{4,}", content.lower())
                 if w not in ("says", "state", "recommends", "guidance")]
        candidates = [text] + [" ".join(pair) for pair in zip(words, words[1:])] \
                     + words
        grounded = any(lookup_guideline(c) for c in candidates)
        if words and not grounded:
            report.findings.append(ValidationFinding(
                check="claim_grounding", severity="flag",
                message="guideline citation not grounded in the guideline "
                        "index — verify before use",
                evidence=f"topic words without a matching guideline: "
                         f"{', '.join(words[:5])}"))

    # ------------------------------------------------------------------
    # persistent register
    # ------------------------------------------------------------------
    def _load_register(self) -> Dict[str, RegisterEntry]:
        if not self.register_path.exists():
            return {}
        try:
            raw = json.loads(self.register_path.read_text())
            return {e["claim_fingerprint"]: RegisterEntry(
                claim=e["claim"], correct_value=e["correct_value"],
                source=e["source"], first_seen=e.get("first_seen", ""))
                for e in raw.get("entries", [])}
        except (json.JSONDecodeError, KeyError, OSError):
            return {}   # a corrupt register never blocks consultations

    def record_hallucination(self, claim: str, correct_value: str,
                             source: str) -> RegisterEntry:
        entry = RegisterEntry(
            claim=claim, correct_value=correct_value, source=source,
            first_seen=datetime.now(timezone.utc).isoformat(
                timespec="seconds"))
        self._register[entry.fingerprint] = entry
        self.register_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"entries": [
            {"claim_fingerprint": fp, **asdict(e)}
            for fp, e in self._register.items()]}
        self.register_path.write_text(json.dumps(payload, indent=2))
        return entry
