# Clinical Validation Layer (Anti-Hallucination) — Design Spec

**Date**: 2026-09-03 · **Trigger**: external consultant audit ordered by Glenn —
"do you have an anti-hallucination layer in you to provide validation of the
diagnosis — and if not, you must build one"

**Audited state** (see `docs/superpowers/specs/2026-09-03-consultant-audit.md`):
the existing hallucination register (`gpdisc_core/memory/persistent/`) is a
BIODISC-era retrospective string-similarity blacklist, wired to nothing in
clinical reasoning, incapable of catching a novel wrong clinical claim. Ten of
sixteen marginal probe presentations produced dangerous failures, including a
structural one: the differential ranked the killer condition first while the
safety layer returned "routine".

## What is built

### 1. `gpdisc_core/clinical_reasoning/validation.py` — ClinicalValidator

The prospective anti-hallucination layer. It verifies a
`ConsultationRecord` BEFORE the output leaves the pipeline. Checks:

| Check | What it catches | Action |
|---|---|---|
| `escalation_consistency` | ranked leader (or any dangerous_alternative / retained_dangerous) has corpus `referral_tier == "emergency"` while `rec.escalation` is routine/self_care | **BLOCK + correct** — escalation is raised to emergency with the correction recorded |
| `urgent_leader_consistency` | leader tier == "urgent" (or two_week_wait) while escalation is routine/self_care | BLOCK + correct to urgent (2ww maps to urgent-tier action with tier named) |
| `retained_without_exclusion` | an emergency-tier condition sits in retained/dangerous set but the record neither ranks it nor documents its exclusion in treatment/referral/safety_net text | FLAG — never silent anchoring |
| `safety_net_presence` | non-emergency disposition carries no safety-net text | FLAG |
| `claim_grounding` | free-text answers assert verifiable facts — drug/renal claims checked against `uk_practice.prescribing_safety.renal_flags`, monitoring claims against `monitoring_requirements`, guideline citations against `guidelines_index.lookup_guideline`, 2ww assertions against `two_week_wait_check` | FLAG with the knowledge-base truth (e.g. "metformin at eGFR 20: STOP — contraindicated below 30") |
| `register_match` | any claim or diagnosis pattern recorded in the persistent clinical hallucination register | FLAG + substitute the recorded correct value |

Output: `ValidationReport` (dataclass) — `passed`, list of `ValidationFinding`
(severity `block`|`flag`, check name, message, evidence), `corrections_applied`.
Attached to every consultation as `rec.validation`; rendered in `summary()`.

### 2. Persistent clinical hallucination register

`gpdisc_core/data/memory/clinical_hallucination_register.json` (local only,
same privacy boundary as all patient data). Entries: `claim_fingerprint`,
`claim`, `correct_value`, `source` (which knowledge module grounds the
correction), `first_seen`. The validator records every block-level finding it
corrects and every externally-supplied correction; future consultations are
checked against it. Seed entries: none fabricated — the register fills from
real findings.

### 3. Marginal-presentation question process (audit §5 fix)

In `consultation.py`: when the top two ranked differentials' scores are within
25% (the same closeness the uncertainty field detects) the pipeline now emits
`discriminating_questions` from the leaders' corpus `discriminators` plus any
`benign_vs_emergency.find_pairs` discriminators for the presentation. Marginal
case → questions, not a shrug.

### 4. Safety-rule cracks found by the audit (engine, not validator)

Each is a genuine detection gap verified by probe; fixed in `safety.py` and
locked in the audit regression suite (`test_audit_probes.py`, the 16 probe
presentations as pinned expectations):

- atypical ACS: autonomic pattern (nausea/sweating/clammy) + age ≥ 45 or
  jaw/arm/neck radiation WITHOUT chest-pain negation
- anaphylaxis word order: "lip/tongue swelling", "swollen lips" etc.
- self-harm: cutting/burning/overdose behaviour words
- elderly afebrile delirium: "gone quiet / not herself / not himself / off
  food / new confusion" in an older person (urgent — same-day delirium rule
  exists; widen its patterns)
- posterior circulation: sudden dizziness/vertigo + diplopia OR ataxia/unsteady
  (emergency — stroke until excluded)

## Not in scope (recorded, not built here)

Toxicology domain, palliative care, dermatology breadth, oncology pathway
module, dashboard consultation endpoint — the audit's missing-domain list;
separate stages. This build is the validation layer plus the safety-critical
cracks it exposes on every run.

## Tests

`gpdisc_core/tests/test_validation.py` — per check: a truthful record passes;
a hallucinated record is blocked/flagged (fabricated renal claim, fabricated
guideline citation, emergency leader under a routine label, retained-without-
exclusion, missing safety-net). Register round-trip through the JSON store.
`gpdisc_core/tests/test_audit_probes.py` — the 16 audit probes with pinned
honest expectations (atypical ACS and ectopic must now reach urgent/emergency;
anaphylaxis emergency; self-harm urgent; coercive control surfaced as a
safeguarding flag — see plan for the per-probe target table).

## Constraints

Python 3.10+ stdlib only · local-only storage · NEVER `git push` ·
`pytest -q > file 2>&1; ec=$?` harness discipline · the 40-case regression
bank must still pass unchanged (engine fixes are additions, not rewrites).
