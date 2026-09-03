# Stage 4: MDT Debate + Multimorbidity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install Level 5 of the GP expertise architecture: `gpdisc_core/mdt/` — a multi-agent consultation team (specialist perspectives + an adversarial Diagnostic Challenger that attacks the leading diagnosis), a structured debate protocol, and the whole-patient multimorbidity reasoner built around Glenn's canonical 79-year-old.

**Architecture:** Four modules. `challenger.py` consumes a `DifferentialResult` from Stage 1's engine and produces structured attacks (dangerous mimics unexplored, anchor bias, missing discriminating tests). `roles.py` defines six MDT roles whose contributions are computed over the clinical-reasoning corpus. `debate.py` orchestrates: pipeline → differential → challenger attacks → role responses → synthesis with recorded disagreement. `multimorbidity.py` is independent of the debate: a rule-based whole-patient review (medication flags via Stage 3's `prescribing_safety`, treatment-tension pairs, anticholinergic burden, drug-causes for the presenting symptom). All deterministic, no LLM calls — privacy rule.

**Tech Stack:** Python 3.10+ stdlib only; pytest.

**Spec:** `docs/superpowers/specs/2026-09-03-gp-expertise-program-design.md` (MDT proposal + multimorbidity section).

## Global Constraints

- Python 3.10+ stdlib only; all local; **NEVER `git push`**. Commits LOCAL ONLY on `main`.
- No placeholders. Plan APIs are functions (Stage 3 lesson: list-returning knowledge is accessed via functions).
- Test harness discipline: `pytest -q > file 2>&1; ec=$?` then branch on `$ec` — piping into `tail` masks exit codes.
- The challenger is deliberately annoying: its job is to be wrong sometimes, never silent. An empty challenge list is a bug.

---

### Task 1: challenger — adversarial attacks on a differential

**Files:**
- Create: `gpdisc_core/mdt/__init__.py`, `gpdisc_core/mdt/challenger.py`
- Test: `gpdisc_core/tests/test_mdt.py`

**Interfaces:**
- Consumes: `DifferentialEngine().build_differential(text)` from Stage 1 (fields: `.ranked` (list of RankedDiagnosis with `.condition_id`, `.score`), `.retained_dangerous`).
- Produces: `Challenge(attack_type, target_condition, argument, action)`, `ATTACK_TYPES` = {"dangerous_mimic", "anchor_bias", "missing_discriminator", "prevalence_challenge"}, `challenge_differential(differential) -> List[Challenge]`.

**Implementation:**

```python
"""Adversarial Diagnostic Challenger — the MDT's designated dissenter.

Stage 4, Task 1. Deliberately over-inclusive: it attacks every leading
diagnosis with the questions a careful physician asks before committing —
especially "which dangerous mimic am I assuming away?". Attacks cite the
corpus's dangerous_mimic_of links so they stay evidence-anchored.
"""
from dataclasses import dataclass
from typing import List

from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS, find_condition

ATTACK_TYPES = ("dangerous_mimic", "anchor_bias", "missing_discriminator",
                "prevalence_challenge")


@dataclass(frozen=True)
class Challenge:
    attack_type: str
    target_condition: str
    argument: str
    action: str


def challenge_differential(differential) -> List[Challenge]:
    """Attack a DifferentialResult: dangerous mimics first, then anchor bias."""
    challenges: List[Challenge] = []
    if not differential.ranked:
        return challenges

    leader = differential.ranked[0]
    leader_profile = find_condition(leader.condition_id)
    ranked_ids = [d.condition_id for d in differential.ranked]

    # 1. Dangerous mimics of the leader that were NOT retained or ranked.
    if leader_profile:
        for mimic_id in leader_profile.dangerous_mimic_of:
            if mimic_id in ranked_ids:
                continue
            if any(d.condition_id == mimic_id for d in differential.retained_dangerous):
                continue
            mimic_profile = find_condition(mimic_id)
            mimic_name = mimic_profile.name if mimic_profile else mimic_id
            challenges.append(Challenge(
                attack_type="dangerous_mimic",
                target_condition=leader.condition_id,
                argument=(f"'{leader_profile.name}' is the leader, but its "
                          f"dangerous mimic '{mimic_name}' is neither ranked "
                          "nor on the retained-dangerous list."),
                action=(f"Ask explicitly what would distinguish {mimic_name} "
                        "and document why it is excluded."),
            ))

    # 2. Anchor bias: leader score dominates but runner-up is close.
    if len(differential.ranked) >= 2 and leader.score > 0:
        runner = differential.ranked[1]
        if runner.score / max(leader.score, 1e-9) > 0.6:
            second = find_condition(runner.condition_id)
            second_name = second.name if second else runner.condition_id
            challenges.append(Challenge(
                attack_type="anchor_bias",
                target_condition=leader.condition_id,
                argument=(f"The runner-up '{second_name}' scores "
                          f"{runner.score / leader.score:.0%} of the leader — "
                          "close enough that anchoring on the leader would be "
                          "premature."),
                action="Name one feature that would move you off the leader; "
                       "if none exists, the two are not yet distinguished.",
            ))

    # 3. Missing discriminator: leader has discriminators nobody has asked.
    if leader_profile and leader_profile.discriminators:
        challenges.append(Challenge(
            attack_type="missing_discriminator",
            target_condition=leader.condition_id,
            argument=(f"The leader '{leader_profile.name}' has discriminating "
                      "features that have not been elicited: "
                      + "; ".join(leader_profile.discriminators[:3]) + "."),
            action="Ask the discriminating questions before treating.",
        ))

    # 4. Prevalence challenge: leader is rare for a common presentation.
    if leader_profile and leader_profile.prevalence_per_consult < 0.005:
        challenges.append(Challenge(
            attack_type="prevalence_challenge",
            target_condition=leader.condition_id,
            argument=(f"'{leader_profile.name}' is rare in consultation "
                      f"(~{leader_profile.prevalence_per_consult:.1%}) — an "
                      "uncommon leader needs an explicit reason."),
            action="Justify the leader with a specific finding, or re-rank "
                   "with the common conditions first.",
        ))

    return challenges
```

- [x] **Step 1: failing tests:**

```python
"""Tests for the MDT layer (expertise program Stage 4)."""
import pytest
from gpdisc_core.clinical_reasoning.diagnostic_engine import DifferentialEngine
from gpdisc_core.mdt.challenger import (
    challenge_differential, Challenge, ATTACK_TYPES,
)


class TestChallenger:
    eng = DifferentialEngine()

    def test_challenges_are_structured(self):
        result = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, "
            "pain radiating to left arm, smoker")
        challenges = challenge_differential(result)
        for c in challenges:
            assert isinstance(c, Challenge)
            assert c.attack_type in ATTACK_TYPES
            assert c.argument and c.action

    def test_never_silent_on_a_leader(self):
        # every differential produces at least one challenge
        result = self.eng.build_differential("tired all the time")
        assert challenge_differential(result)

    def test_dangerous_mimic_attack_fires_on_benign_headache(self):
        result = self.eng.build_differential(
            "mild bilateral headache after stress for a week")
        challenges = challenge_differential(result)
        mimic_attacks = [c for c in challenges if c.attack_type == "dangerous_mimic"]
        assert any("SAH" in c.argument or "subarachnoid" in c.argument.lower()
                   or "GCA" in c.argument or "arteritis" in c.argument.lower()
                   or "meningitis" in c.argument.lower()
                   for c in mimic_attacks)

    def test_empty_differential_no_crash(self):
        class _Empty:
            ranked = []
            retained_dangerous = []
        assert challenge_differential(_Empty()) == []

    def test_missing_discriminator_cites_features(self):
        result = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, "
            "pain radiating to left arm, smoker")
        challenges = challenge_differential(result)
        md = [c for c in challenges if c.attack_type == "missing_discriminator"]
        assert md and md[0].action
```

- [x] **Step 2: verify fail** (collection ImportError). **Step 3: implement.** **Step 4: run** (5 pass). **Step 5: commit** `feat(mdt): adversarial Diagnostic Challenger — mimic/anchor/discriminator/prevalence attacks`.

---

### Task 2: roles — six MDT perspectives

**Files:**
- Create: `gpdisc_core/mdt/roles.py`
- Test: append `class TestMDTRoles`

**Interfaces:**
- Produces: `MDTRole(key, title, remit)`, `MDT_ROLES: List[MDTRole]` (6: gp_chair, geriatrician, clinical_pharmacologist, safeguarding_practitioner, mental_health, patient_advocate), `contribute(role_key, presentation, context, differential=None) -> List[str]` — computed observations (uses Stage 2/3 packages where relevant: `capacity_concern_keywords`, `renal_flags`, `monitoring_requirements`, `cvd` etc.).

**Implementation:**

```python
"""MDT roles — six computed perspectives on the consultation.

Stage 4, Task 2. Each role's contribution is computed from the packages
already installed (clinical reasoning, preventive, sexual health, uk
practice) — deterministic rules, no LLM. Roles contribute questions and
observations, never conclusions: the chair synthesises.
"""
from dataclasses import dataclass
from typing import List, Optional

from gpdisc_core.uk_practice.capacity_and_safeguarding import (
    capacity_concern_keywords,
)
from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements, renal_flags,
)


@dataclass(frozen=True)
class MDTRole:
    key: str
    title: str
    remit: str


MDT_ROLES: List[MDTRole] = [
    MDTRole("gp_chair", "GP (chair)",
            "Holds the whole picture; keeps the patient's agenda central"),
    MDTRole("geriatrician", "Geriatrician",
            "Frailty, falls, polypharmacy, atypical presentations"),
    MDTRole("clinical_pharmacologist", "Clinical pharmacologist",
            "Every symptom is a drug side effect until proven otherwise"),
    MDTRole("safeguarding_practitioner", "Safeguarding practitioner",
            "Capacity, coercion, neglect — the questions nobody else asks"),
    MDTRole("mental_health", "Mental health clinician",
            "Depression/anxiety as cause and consequence of physical illness"),
    MDTRole("patient_advocate", "Patient advocate",
            "What matters to THIS patient; plain language; no decision about "
            "them without them"),
]

_MEDICATION_HINTS = ("medication", "tablets", "pills", "on ", "prescribed",
                     "drug", "eight medications", "medicines")
_ELDER_HINTS = ("79", "85", "elderly", "old ", "frail", "falls",
                "confusion", "memory")
_MOOD_HINTS = ("low mood", "depressed", "anxious", "can't sleep",
               "no interest", "worry", "panic")


def contribute(role_key: str, presentation: str, context: Optional[dict] = None,
               differential=None) -> List[str]:
    """One role's computed observations on this consultation."""
    ctx = context or {}
    text = presentation.lower()
    meds = ctx.get("medications") or []
    notes: List[str] = []

    if role_key == "gp_chair":
        notes.append("Agree the agenda first: what does the patient think "
                     "is going on, and what are they most worried about?")
        if len(text.split()) > 30:
            notes.append("Long presentation — ask the patient to pick the "
                         "one problem they most want sorted today.")
        notes.append("Close the loop: summarise back, check understanding, "
                     "agree the next step out loud.")

    elif role_key == "geriatrician":
        if any(h in text for h in _ELDER_HINTS) or ctx.get("age_years", 0) >= 75:
            notes.append("Atypical presentation is the norm at this age: "
                         "infection presents as confusion, MI as breathlessness.")
            notes.append("Screen the geriatric giants: falls, continence, "
                         "cognition, nutrition, and who is at home.")
        if ctx.get("falls") or "fall" in text:
            notes.append("Falls: review the medication list first — "
                         "antihypertensives, sedatives, anticholinergics.")

    elif role_key == "clinical_pharmacologist":
        if meds or any(h in text for h in _MEDICATION_HINTS):
            notes.append("Reconcile the full list including over-the-counter "
                         "and hospital leftovers before attributing symptoms.")
            egfr = ctx.get("egfr")
            for drug in meds:
                flags = renal_flags(drug, egfr) if egfr else []
                mon = monitoring_requirements(drug)
                if flags:
                    notes.append(f"{drug}: {'; '.join(flags)}")
                if mon:
                    notes.append(f"{drug}: {mon[0]}")
        notes.append("Before adding any drug, ask which existing one could "
                     "be STOPPED — the indication may have expired.")

    elif role_key == "safeguarding_practitioner":
        hits = capacity_concern_keywords(presentation)
        if hits:
            notes.append("Concern indicators present (" + ", ".join(hits) +
                         ") — explore privately, without the accompanying person.")
        if ctx.get("accompanied") and hits:
            notes.append("Interview alone for part of the consultation; "
                         "document that the opportunity was offered.")
        notes.append("Consider capacity for the decisions actually being "
                     "made today — decision-specific, presumed until assessed.")

    elif role_key == "mental_health":
        if any(h in text for h in _MOOD_HINTS):
            notes.append("Screen openly: two questions beat ten — low mood "
                         "and anhedonia — then explore risk.")
        notes.append("Physical and mental causes are not mutually exclusive; "
                     "treat both streams, do not rank them.")

    elif role_key == "patient_advocate":
        notes.append("Ask what the patient has already tried and what they "
                     "were hoping for from this consultation.")
        if ctx.get("interpreter_needed"):
            notes.append("Book an interpreter — family translation changes "
                         "the clinical story.")

    return notes
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.mdt.roles import MDT_ROLES, MDTRole, contribute


class TestMDTRoles:
    def test_six_roles(self):
        assert len(MDT_ROLES) == 6
        assert {r.key for r in MDT_ROLES} == {
            "gp_chair", "geriatrician", "clinical_pharmacologist",
            "safeguarding_practitioner", "mental_health", "patient_advocate"}

    def test_every_role_contributes_something(self):
        for role in MDT_ROLES:
            assert contribute(role.key, "tired all the time", {})

    def test_pharmacologist_uses_renal_flags(self):
        notes = contribute("clinical_pharmacologist",
                           "dizzy and confused",
                           {"medications": ["metformin"], "egfr": 25})
        assert any("STOP" in n or "metformin" in n.lower() for n in notes)

    def test_geriatrician_fires_on_age(self):
        notes = contribute("geriatrician", "confusion", {"age_years": 82})
        assert any("atypical" in n.lower() for n in notes)

    def test_safeguarding_detects_concerns(self):
        notes = contribute("safeguarding_practitioner",
                           "son always answers for her, money missing", {})
        assert any("privately" in n.lower() or "alone" in n.lower()
                   for n in notes)

    def test_unknown_role_empty(self):
        assert contribute("astronaut", "anything") == []
```

- [x] **Step 2: verify fail.** **Step 3: implement.** **Step 4: run** (11 total). **Step 5: commit** `feat(mdt): six MDT roles with computed contributions`.

---

### Task 3: debate — orchestrate the consultation MDT

**Files:**
- Create: `gpdisc_core/mdt/debate.py`
- Test: append `class TestDebate`

**Interfaces:**
- Consumes: Stage 1 `ConsultationPipeline`, Task 1 `challenge_differential`, Task 2 `contribute`/`MDT_ROLES`.
- Produces: `MDTResult(presentation, escalation, syndrome, differential_ids, challenges, role_notes, synthesis, disagreements, actions)` and `run_mdt(presentation, context=None) -> MDTResult`. `synthesis` always contains a sentence of the form "Working diagnosis …" and, when the differential is uncertain, the phrase "I don't know yet". `actions` is a de-duplicated ordered list of strings.

**Implementation:**

```python
"""MDT debate protocol — pipeline, challenge, respond, synthesise.

Stage 4, Task 3. One deterministic pass: the consultation pipeline builds
the differential and safety position; the challenger attacks it; each role
responds; the chair synthesises. Disagreement is recorded, never smoothed
away — 'the MDT was split' is clinical information.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.mdt.challenger import challenge_differential, Challenge
from gpdisc_core.mdt.roles import MDT_ROLES, contribute


@dataclass
class MDTResult:
    presentation: str
    escalation: str = ""
    syndrome: str = ""
    differential_ids: List[str] = field(default_factory=list)
    challenges: List[Challenge] = field(default_factory=list)
    role_notes: dict = field(default_factory=dict)
    synthesis: str = ""
    disagreements: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)


def run_mdt(presentation: str, context: Optional[dict] = None) -> MDTResult:
    ctx = context or {}
    rec = ConsultationPipeline().run(presentation, ctx)
    result = MDTResult(
        presentation=presentation,
        escalation=rec.escalation,
        syndrome=rec.syndrome,
        differential_ids=[d.condition_id for d in rec.ranked_differential],
    )
    result.challenges = challenge_differential(
        _as_differential_result(rec))

    for role in MDT_ROLES:
        notes = contribute(role.key, presentation, ctx)
        if notes:
            result.role_notes[role.key] = notes

    # The chair's synthesis — uncertainty is stated, never hidden.
    if rec.escalation == "emergency":
        result.synthesis = ("Emergency presentation: treat as "
                            + (result.differential_ids[0]
                               if result.differential_ids else "the emergency "
                                 "pathway") + " and escalate now.")
        result.actions.append("Escalate immediately (999/emergency pathway)")
    elif len(result.differential_ids) >= 3:
        result.synthesis = ("Working diagnosis: " + result.differential_ids[0]
                            + ", actively held against "
                            + ", ".join(result.differential_ids[1:3])
                            + ". Not settled — ")
        result.synthesis += ("I don't know yet" if not rec.investigation_strategy
                             else "investigate to discriminate")
    else:
        result.synthesis = ("Working diagnosis: "
                            + (result.differential_ids[0] if result.differential_ids
                               else "undetermined") + ". I don't know yet — "
                            "the presentation does not fit a single pattern.")

    # Disagreements: challenge targets the leader while a role treats a
    # different condition as important — that tension is recorded.
    leader = result.differential_ids[0] if result.differential_ids else ""
    for c in result.challenges:
        if c.target_condition == leader and leader:
            result.disagreements.append(
                f"Challenger vs leader: {c.argument}")
            break

    # Actions: safety first, then challenges, then discriminating questions.
    if rec.safety_net:
        result.actions.append("Safety-net: " + rec.safety_net)
    for c in result.challenges:
        result.actions.append(c.action)
    for q in rec.discriminating_questions:
        result.actions.append("Ask: " + q)

    seen = set()
    result.actions = [a for a in result.actions
                      if not (a in seen or seen.add(a))]
    return result


def _as_differential_result(rec):
    """Adapt a ConsultationRecord to the shape challenge_differential reads."""
    class _Adapter:
        pass
    a = _Adapter()
    a.ranked = list(rec.ranked_differential)
    a.retained_dangerous = list(rec.dangerous_alternatives or [])
    return a
```

**Execution note:** verify at implementation time (Read the actual `ConsultationRecord` fields in `consultation.py`) that the fields referenced are `rec.escalation`, `rec.syndrome`, `rec.ranked_differential` (list of RankedDiagnosis), `rec.dangerous_alternatives`, `rec.investigation_strategy`, `rec.discriminating_questions`, `rec.safety_net` — match whatever the real names are; the tests below only depend on `run_mdt`'s outputs, so adapt the adapter, not the clinical logic.

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.mdt.debate import run_mdt, MDTResult


class TestDebate:
    def test_result_shape(self):
        r = run_mdt("66 year old man, chest pain for 40 minutes, "
                    "sweating, pain radiating to left arm")
        assert r.escalation == "emergency"
        assert r.differential_ids
        assert r.synthesis and r.actions

    def test_emergency_first_action_is_escalation(self):
        r = run_mdt("crushing chest pain 30 minutes, sweating")
        assert r.actions[0].startswith("Escalate")

    def test_uncertainty_is_stated(self):
        r = run_mdt("tired all the time")
        assert "I don't know yet" in r.synthesis or "Not settled" in r.synthesis

    def test_challenges_flow_into_actions(self):
        r = run_mdt("mild bilateral headache after stress for a week")
        assert len(r.actions) >= 2  # safety net + at least one challenge action

    def test_roles_recorded(self):
        r = run_mdt("79 year old woman, dizzy and confused, eight medications",
                    {"medications": ["metformin", "ramipril"], "egfr": 28})
        assert "clinical_pharmacologist" in r.role_notes
        assert "geriatrician" in r.role_notes

    def test_actions_deduplicated(self):
        r = run_mdt("fever for two days since returning from Ghana")
        assert len(r.actions) == len(set(r.actions))

    def test_syndrome_survives_the_debate(self):
        r = run_mdt("fever for two days since returning from Ghana")
        assert r.syndrome == "fever_after_travel"
```

- [x] **Step 2: verify fail.** **Step 3: implement** (checking real field names in consultation.py first). **Step 4: run** (18 total). **Step 5: commit** `feat(mdt): debate protocol — pipeline → challenge → roles → synthesis with recorded disagreement`.

---

### Task 4: multimorbidity — the whole-patient reasoner

**Files:**
- Create: `gpdisc_core/mdt/multimorbidity.py`
- Test: append `class TestMultimorbidity`

**Interfaces:**
- Consumes: `renal_flags`, `monitoring_requirements` from uk_practice; `fit_note_guidance` not needed here.
- Produces:
  - `TREATMENT_TENSIONS: List[Tuple[str, str, str, str]]` (condition_a, condition_b, tension, resolution) — 10 pairs
  - `ACB_SCORES: Dict[str, int]` — anticholinergic cognitive burden, common drugs
  - `whole_patient_review(patient: dict) -> dict` with keys: `medication_flags` (renal + monitoring), `anticholinergic_burden` (int + drugs), `tensions` (matched pair dicts), `symptom_causes` (for dizziness/confusion: the drug-cause checklist), `priorities` (ordered list), `appointment_design` (the "one thing at a time" guidance)

**Implementation:**

```python
TREATMENT_TENSIONS = [
    ("chronic_kidney_disease", "osteoarthritis",
     "NSAIDs (oral) for OA pain accelerate CKD and raise cardiovascular risk",
     "Paracetamol + topical NSAID first; orthopaedic referral for joint-focused "
     "options; never repeat oral NSAID prescriptions without reviewing eGFR"),
    ("heart_failure", "type_2_diabetes",
     "Historic tension resolved: SGLT2 inhibitors now benefit BOTH",
     "Consider SGLT2i — improves HF outcomes and glycaemic control"),
    ("type_2_diabetes", "cognitive_impairment",
     "Complex insulin regimes outstrip the patient's ability to follow them; "
     "hypoglycaemia from missed meals presents as confusion",
     "Simplify the regimen; prefer agents with low hypoglycaemia risk; involve "
     "carers; HbA1c targets relaxed (7.5-8.5%)"),
    ("copd", "heart_failure",
     "Historic beta-blocker fear led to under-treatment of HF in COPD",
     "Cardioselective beta-blockers (bisoprolol/metoprolol) are safe and "
     "under-used — start low, monitor symptoms"),
    ("hypertension", "falls",
     "Intensive BP lowering trades stroke reduction for falls and fractures",
     "Check LYING AND STANDING BP; if postural drop, relax the target and "
     "deprescribe the antihypertensive contributing most"),
    ("atrial_fibrillation", "falls",
     "Anticoagulation prevents stroke but falls raise bleed risk",
     "Count the falls, not the fear: most fallers still net-benefit from "
     "anticoagulation — document the shared decision"),
    ("gout", "chronic_kidney_disease",
     "NSAIDs and high-dose colchicine are both hazardous in CKD",
     "Acute flare: reduced-dose colchicine or short steroid course; allopurinol "
     "start low, titrate slowly, continue during flares"),
    ("type_2_diabetes", "corticosteroids",
     "Steroid courses provoke hyperglycaemia in diabetes",
     "Plan the steroid course: temporary uptitration, alert patient to glucose "
     "checks, arrange review mid-course"),
    ("epilepsy", "contraception",
     "Enzyme-inducing antiepileptics reduce COCP/implant effectiveness",
     "UKMEC-aware method choice (progestogen options, copper IUD); the "
     "contraceptive and epilepsy decisions must be made together"),
    ("dementia", "urinary_incontinence",
     "Anticholinergic bladder drugs worsen cognition",
     "Non-drug measures first; if a drug is needed, review cognition after "
     "initiation and prefer the lowest anticholinergic load"),
]

ACB_SCORES = {
    "amitriptyline": 3, "oxybutynin": 3, "procyclidine": 3,
    "solifenacin": 2, "tolterodine": 2, "cyclizine": 2,
    "chlorphenamine": 2, "promethazine": 2, "trihexyphenidyl": 3,
    "quetiapine": 1, "sertraline": 1, "furosemide": 1, "metoclopramide": 1,
    "ranitidine": 1, "digoxin": 1, "theophylline": 1, "warfarin": 1,
}

_DIZZINESS_DRUG_CAUSES = [
    "Postural drop from antihypertensives — CHECK LYING AND STANDING BP",
    "Hypoglycaemia from insulin/sulfonylurea, worse with small appetite",
    "Hyponatraemia: SSRI + thiazide + PPI is the classic trio",
    "Digoxin toxicity (nausea, visual change) especially with renal decline",
    "Anticholinergic load: dizziness + confusion together suggests it",
    "Bradycardia from beta-blocker or rate-limiting calcium blocker",
]

_CONFUSION_DRUG_CAUSES = [
    "Anticholinergic burden — score the list (ACB)",
    "Opioids, benzodiazepines, z-drugs: new confusion in the elderly",
    "Steroid course: mood and sleep disturbance, rare psychosis",
    "Antiepileptic toxicity: unsteadiness that looks like 'confusion'",
    "Sepsis FIRST: infection presents as confusion at this age — screen urine, "
    "chest, skin",
]


def whole_patient_review(patient: dict) -> dict:
    """Glenn's canonical case: the 79-year-old with many conditions, eight
    medications, dizziness and confusion. The review asks, in order: which
    DRUG is causing this, which TREATMENT TENSION is unmanaged, and what is
    the SAFEST single priority for the next appointment."""
    conditions = set(patient.get("conditions", []))
    medications = list(patient.get("medications", []))
    egfr = patient.get("egfr")

    medication_flags = []
    for drug in medications:
        for flag in renal_flags(drug, egfr) if egfr else []:
            medication_flags.append(f"{drug}: {flag}")
        for req in monitoring_requirements(drug)[:1]:
            medication_flags.append(f"{drug}: {req}")

    acb_total = sum(ACB_SCORES.get(d.lower(), 0) for d in medications)
    acb_drugs = [d for d in medications if d.lower() in ACB_SCORES]

    tensions = []
    for (a, b, tension, resolution) in TREATMENT_TENSIONS:
        if a in conditions and b in conditions:
            tensions.append({"conditions": [a, b], "tension": tension,
                             "resolution": resolution})

    symptom_causes = {}
    symptoms = [s.lower() for s in patient.get("symptoms", [])]
    if any("dizz" in s for s in symptoms):
        symptom_causes["dizziness"] = _DIZZINESS_DRUG_CAUSES
    if any("confus" in s or "confusion" in s for s in symptoms):
        symptom_causes["confusion"] = _CONFUSION_DRUG_CAUSES

    priorities = []
    if egfr and egfr < 30:
        priorities.append("Renal function is the keystone: re-check eGFR and "
                          "potassium, and adjust every renally-cleared drug")
    if any("dizz" in s for s in symptoms):
        priorities.append("Lying AND standing BP today — before any other "
                          "diagnostic reasoning about dizziness")
    if any("confus" in s for s in symptoms):
        priorities.append("Confusion at this age: rule out sepsis and "
                          "drug causes before assuming dementia progression")
    if acb_total >= 3:
        priorities.append(f"Anticholinergic burden {acb_total} — propose a "
                          "deprescribing plan for: " + ", ".join(acb_drugs))
    if not priorities:
        priorities.append("Agree the patient's own priority first — the "
                          "problem they most want solved is the one to solve")

    appointment_design = [
        "One problem per appointment, chosen WITH the patient",
        "Stop before you start: review every drug's indication annually",
        "Goals of care conversation once, not repeatedly — record what "
        "matters to this patient",
        "Share the plan in writing (large print) with patient and carer",
    ]

    return {"medication_flags": medication_flags,
            "anticholinergic_burden": acb_total,
            "anticholinergic_drugs": acb_drugs,
            "tensions": tensions,
            "symptom_causes": symptom_causes,
            "priorities": priorities,
            "appointment_design": appointment_design}
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.mdt.multimorbidity import (
    TREATMENT_TENSIONS, ACB_SCORES, whole_patient_review,
)


GLENN_CASE = {
    "age_years": 79,
    "conditions": ["chronic_kidney_disease", "type_2_diabetes",
                   "heart_failure", "osteoarthritis", "cognitive_impairment",
                   "hypertension"],
    "medications": ["metformin", "ramipril", "furosemide", "bisoprolol",
                    "amitriptyline", "gliclazide", "paracetamol", "omeprazole"],
    "egfr": 28,
    "symptoms": ["dizziness", "confusion"],
}


class TestMultimorbidity:
    def test_ten_tensions_defined(self):
        assert len(TREATMENT_TENSIONS) == 10

    def test_glenn_case_renal_flags_fire(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("metformin" in f and "STOP" in f
                   for f in review["medication_flags"])

    def test_glenn_case_acb_scores(self):
        review = whole_patient_review(GLENN_CASE)
        assert review["anticholinergic_burden"] >= 4  # amitriptyline 3 + furosemide 1
        assert "amitriptyline" in review["anticholinergic_drugs"]

    def test_glenn_case_tensions_matched(self):
        review = whole_patient_review(GLENN_CASE)
        pairs = [tuple(t["conditions"]) for t in review["tensions"]]
        assert ("chronic_kidney_disease", "osteoarthritis") in pairs
        assert ("type_2_diabetes", "cognitive_impairment") in pairs

    def test_dizziness_causes_include_postural_bp(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("standing" in c.lower()
                   for c in review["symptom_causes"]["dizziness"])

    def test_confusion_rules_out_sepsis_first(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("sepsis" in c.lower()
                   for c in review["symptom_causes"]["confusion"])

    def test_priorities_ordered_and_nonempty(self):
        review = whole_patient_review(GLENN_CASE)
        assert review["priorities"]
        standing = [p for p in review["priorities"] if "standing" in p.lower()]
        assert standing  # postural BP is in the priority list for dizziness

    def test_appointment_design_present(self):
        review = whole_patient_review(GLENN_CASE)
        assert any("Stop before you start" in a for a in review["appointment_design"])

    def test_minimal_patient_defaults_sensibly(self):
        review = whole_patient_review({})
        assert review["medication_flags"] == []
        assert review["priorities"]  # patient's own priority is still first
```

- [x] **Step 2: verify fail.** **Step 3: implement.** **Step 4: run** (27 total). **Step 5: commit** `feat(mdt): whole-patient multimorbidity review — Glenn's 79-year-old case first-class`.

---

### Task 5: package exports + full regression + docs

**Files:**
- Modify: `gpdisc_core/mdt/__init__.py` (full exports)
- Test: append `class TestMDTExports`
- Modify: `CLAUDE.md`; memory update; tick plan checkboxes

**Step 1: failing tests:**

```python
from gpdisc_core.mdt import (
    run_mdt, challenge_differential, MDT_ROLES, contribute,
    whole_patient_review, TREATMENT_TENSIONS,
)


class TestMDTExports:
    def test_package_root_exports(self):
        assert callable(run_mdt)
        assert len(MDT_ROLES) == 6
        assert len(TREATMENT_TENSIONS) == 10
        assert whole_patient_review({"medications": ["metformin"], "egfr": 25})
```

- [x] **Step 2: verify fail.** **Step 3: implement** `__init__.py`:

```python
"""GPDISC MDT layer (expertise program Stage 4).

The multi-agent consultation team: adversarial Diagnostic Challenger, six
MDT roles, a debate protocol, and the whole-patient multimorbidity review.
Deterministic rules over the Stage 1-3 knowledge — no LLM, no external
transmission.
"""
from gpdisc_core.mdt.challenger import (
    Challenge, ATTACK_TYPES, challenge_differential,
)
from gpdisc_core.mdt.roles import MDTRole, MDT_ROLES, contribute
from gpdisc_core.mdt.debate import MDTResult, run_mdt
from gpdisc_core.mdt.multimorbidity import (
    TREATMENT_TENSIONS, ACB_SCORES, whole_patient_review,
)

__all__ = [
    "Challenge", "ATTACK_TYPES", "challenge_differential",
    "MDTRole", "MDT_ROLES", "contribute",
    "MDTResult", "run_mdt",
    "TREATMENT_TENSIONS", "ACB_SCORES", "whole_patient_review",
]
```

- [x] **Step 4: full battery** — all 6 suites (143 + 27 + 1 export = 171), comprehensive 26/26, test_all 11/3 baseline, import sweep 0 failures.
- [x] **Step 5: CLAUDE.md** — "### MDT + Multimorbidity (Stage 4)" section + Testing line.
- [x] **Step 6: commit** `docs: document Stage 4 mdt in CLAUDE.md`; memory; tick checkboxes; commit.

---

## Self-Review (completed)

- **Spec coverage:** MDT multi-agent proposal → Tasks 1-3 (challenger, roles, debate); multimorbidity whole-patient reasoning with the 79-year-old → Task 4 (exact case: CKD, T2DM, HF, OA, MCI, eight medications, dizziness + confusion); "when 'I don't know yet' is the medically correct conclusion" → debate synthesis states it explicitly.
- **Placeholders:** none.
- **Type consistency:** `challenge_differential` consumed in Task 3 matches Task 1 signature; `contribute(role_key, presentation, context)` matches; `renal_flags(drug, egfr)` signature matches Stage 3 implementation (positional). ConsultationRecord field names are verified at Task 3 implementation time (execution note included).
