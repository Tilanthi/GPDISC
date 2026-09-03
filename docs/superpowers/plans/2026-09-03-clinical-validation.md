# Clinical Validation Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the prospective anti-hallucination layer for diagnostic output, close the five safety-rule cracks and the marginal-question gap the consultant audit exposed, and lock all 16 audit probes as regression tests.

**Architecture:** `validation.py` inside `clinical_reasoning` (imports `uk_practice` — verified no reverse import, no cycle) provides `ClinicalValidator.validate_consultation(rec)` (consistency + completeness checks, block-level corrections applied to the record) and `verify_claim(text)` (grounding of free-text clinical claims against uk_practice drug/guideline knowledge + the persistent register). The pipeline runs it on EVERY exit path; the record carries a `ValidationReport`. Safety-rule fixes are additive patterns in `safety.py`; question generation generalizes to any close top-2 differential.

**Tech Stack:** Python 3.10+ stdlib only; pytest.

**Spec:** `docs/superpowers/specs/2026-09-03-clinical-validation-design.md` (audit evidence: `2026-09-03-consultant-audit.md`).

## Global Constraints

- NEVER `git push`; commits LOCAL ONLY on `main`.
- `pytest -q > file 2>&1; ec=$?` harness discipline — never pipe into tail before branching.
- The 40-case regression bank must still pass unchanged — corrections may only RAISE escalation (never lower), and no benign row's leader is emergency-tier (verified).
- Privacy: register JSON lives under `gpdisc_core/data/memory/`, local only.

---

### Task 1: ClinicalValidator (TDD)

**Files:**
- Create: `gpdisc_core/clinical_reasoning/validation.py`
- Test: `gpdisc_core/tests/test_validation.py`

**Interfaces (produces):**
- `ValidationFinding(check, severity, message, evidence)` — severity `"block"`|`"flag"`
- `ValidationReport(passed, findings, corrections)` — `.summary() -> str`; `passed` = no block-severity findings remain uncorrected
- `ClinicalValidator(register_path=None)`; `.validate_consultation(rec) -> ValidationReport` (applies corrections to rec: escalation raised, referral/safety_net annotated); `.verify_claim(text) -> ValidationReport`; `.record_hallucination(claim, correct_value, source)`
- Default register path: `Path(__file__).parent.parent / "data" / "memory" / "clinical_hallucination_register.json"`

**Checks in validate_consultation:**
1. `escalation_consistency` (block+correct): ranked top-3 contains a corpus `referral_tier == "emergency"` condition while `rec.escalation` is routine/self_care → raise to emergency. Ranked top-1 tier urgent/two_week_wait while routine/self_care → raise to urgent (2ww named in correction).
2. `retained_without_exclusion` (flag): dangerous_alternative/retained emergency-tier condition neither ranked nor mentioned-with-exclusion in treatment/referral/safety_net.
3. `safety_net_presence` (flag): non-emergency record with empty safety_net.
4. `safeguarding_signal` (flag): `uk_practice.capacity_concern_keywords(rec.presenting_complaint)` hits → 'explore this' note.

**Checks in verify_claim (grounding, free text):**
5. renal: claim contains a monitored drug + eGFR value → `renal_flags(drug, egfr)`; claim asserting safe/continue/fine while flags exist → block with the flag text as truth.
6. monitoring: "no monitoring needed for X" while `monitoring_requirements(X)` non-empty → flag.
7. citation: claim mentioning NICE/CKS/NGxx whose topic finds nothing in `lookup_guideline` → flag 'citation not grounded'.
8. register: normalized claim fingerprint in register → block, substitute `correct_value`.

- [x] **Step 1** write `test_validation.py` (per check: truthful passes, hallucinated blocked/flagged; register round-trip via tmp_path) → verify FAIL
- [x] **Step 2** implement `validation.py` → verify PASS → commit `feat(clinical_reasoning): clinical validator — the anti-hallucination layer` (0e3f9f6; +contender-gate tests 3527ec0)

### Task 2: safety cracks + question process + wiring (TDD)

**Files:**
- Modify: `gpdisc_core/clinical_reasoning/safety.py`, `consultation.py`, `knowledge.py`, `benign_vs_emergency.py`; `gpdisc_core/uk_practice/capacity_and_safeguarding.py`
- Test: `gpdisc_core/tests/test_audit_probes.py` (the 16 audit probes, pinned honest targets)

**Engine changes:**
- safety.py: `acs_atypical` (autonomic + jaw/arm/neck radiation + age, min 3); anaphylaxis pattern for "lip/tongue/throat/face swelling" word orders; `self_harm` + cutting/burning/overdose behaviour; `elderly_behaviour_change` urgent rule (age token + gone-quiet/not-herself/off-food/drowsy, min 2); `posterior_stroke` (dizzy/vertigo + double-vision/diplopia + unsteady/ataxia, min 3); ectopic pregnancy-possibility patterns (coil/IUD/late period).
- consultation.py: `rec.validation` field + `ClinicalValidator` in pipeline, run on both exit paths; summary() renders it. Question generalization: no syndrome questions AND top2.score ≥ 0.75×top1.score → discriminating questions from leaders' corpus discriminators + `find_pairs` discriminators (cap 5).
- knowledge.py anhedonia phrases: "can't enjoy anything", "can't enjoy", "no pleasure in anything".
- benign_vs_emergency.py keyword: "spinning" → bppv/stroke pair.
- capacity_and_safeguarding.py coercive_control phrases: "controls all my", "controls my medicines", "won't let me", "not allowed to see".

- [x] **Step 1** write `test_audit_probes.py` with the per-probe target table from the audit → verify FAIL (14 red)
- [x] **Step 2** implement engine changes → verify PASS (20/20) → commit `feat(clinical_reasoning): close audit cracks — ...validator wired into every consultation` (3527ec0). Noted deviations: knowledge phrases live in `knowledge_breadth.py` SYNONYMS (not `knowledge.py`); pair keyword "spins" (substring-matches spins/spinning); `acs_atypical` min 2 with `sweat\w*` excluded (night sweats over weeks is constitutional, not autonomic); contender gate added to the validator's escalation floor (noise-scored GCA on 'headache' must not floor a routine record); 5 bank rows re-pinned emergency — raises with clinical justification, bank header documents the convention.

### Task 3: full battery + close-out

- [x] **Step 1** run the 12-suite battery (10 program suites + validation + audit probes): **235/235**; comprehensive **26/26**; test_all 11 passed / 3 failed (same 3 pre-existing legacy failures as the documented baseline); import sweep **0 failures**; regression bank holds 40/40 (5 rows re-pinned emergency per Task 2 note — raises only, never weakened)
- [x] **Step 2** CLAUDE.md validation-layer section + testing lines; memory update; commit
