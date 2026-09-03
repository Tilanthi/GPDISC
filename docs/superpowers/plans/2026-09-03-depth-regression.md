# Stage 5: Curriculum Depth + Regression Bank Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the expertise program with the two things Glenn weighted hardest: consultation and "doctor" skills as a structured module, benign-vs-emergency discrimination pairs, and a dangerous-mimic regression bank that locks diagnostic reasoning behaviour in as executable curriculum.

**Architecture:** Three modules. `consultation_skills.py` — the consultation craft (ICE, chunking/checking, SPIKES, safety-net formula, difficult-consultation patterns, "I don't know yet" scripts). `benign_vs_emergency.py` — paired presentations where the benign twin and the emergency twin differ by specific discriminators. `regression_bank.py` — the data bank of presentations with expected pipeline behaviour (escalation, leader-or-retained condition, syndrome), consumed by a test suite that runs every case through the real ConsultationPipeline.

**Tech Stack:** Python 3.10+ stdlib only; pytest.

**Spec:** `docs/superpowers/specs/2026-09-03-gp-expertise-program-design.md`.

## Global Constraints

- Python 3.10+ stdlib only; local only; **NEVER `git push`**; commits LOCAL ONLY on `main`.
- Test harness: `pytest -q > file 2>&1; ec=$?` — never pipe into tail before branching.
- The regression bank documents the engine as curriculum: where a case fails, the question is whether the engine or the expectation is clinically wrong — tests are clinical ground truth, but verify each failing case by hand before changing either side.

---

### Task 1: consultation_skills — the "doctor" craft

**Files:**
- Create: `gpdisc_core/consultation_skills/__init__.py`, `gpdisc_core/consultation_skills/skills.py`
- Test: `gpdisc_core/tests/test_consultation_skills.py`

**Interfaces:**
- Produces:
  - `ice_questions(concern: str = "") -> List[str]` — ideas/concerns/expectations, tailored if a concern keyword matches
  - `CHUNKING_RULES: List[str]`, `chunking_rules() -> List[str]`
  - `SPIKES_STEPS: List[str]`, `spikes_steps() -> List[str]`
  - `safety_net_formula(what_to_expect, what_changes_mind, timescale) -> str`
  - `DIFFICULT_CONSULTATIONS: Dict[str, List[str]]` (keys: the_angry_patient, the_reassurance_seeker, the_bringer_of_lists, the_silent_patient, the_internet_researcher, the_denier), `difficult_consultation_guidance(kind: str) -> List[str]`
  - `uncertainty_scripts() -> List[str]` — honest "I don't know yet" language that maintains trust
  - `CONSULTATION_MODELS: Dict[str, str]` (calgary_cambridge, anthropic... no — calgary_cambridge, balint, neighbour, pendleton_functional) with one-line descriptions

**Implementation:** (write directly — each list is the module)

```python
def ice_questions(concern: str = "") -> List[str]:
    base = [
        "Ideas: 'What do you think might be going on?'",
        "Concerns: 'Is there anything you're worried this might be?'",
        "Expectations: 'What were you hoping we could do about it today?'",
    ]
    c = concern.lower()
    if "cancer" in c:
        base.append("Name the fear: 'You mentioned cancer — can I ask what "
                    "made that come to mind?'")
    if "tired" in c or "fatigue" in c:
        base.append("Fatigue expectations: 'What would good energy look like "
                    "for you — what are you aiming to get back to?'")
    if "pain" in c:
        base.append("Pain goal: 'What could you do again that the pain stops "
                    "you doing now?'")
    return base

CHUNKING_RULES = [
    "Ask one question at a time; park the rest visibly ('I'll come back to "
    "the sleep problem — first the chest pain')",
    "Chunk and check: after 2-3 exchanges, summarise what you heard and ask "
    "what you missed",
    "Screen: 'Is there anything else you were hoping to cover?' — ask it "
    "TWICE; the second ask surfaces the real agenda",
    "The golden minute: let the patient speak uninterrupted for the first "
    "60 seconds — it shortens the consultation",
    "Sit down, look up from the screen, match pace — the consultation is "
    "the treatment as much as anything prescribed",
]

SPIKES_STEPS = [
    "Setting: privacy, sitting down, no interruptions, warning shot "
    "('I'm afraid I have some difficult news')",
    "Perception: 'What do you understand about your illness so far?' — "
    "anchor to what they already know",
    "Invitation: 'How much detail would you like?'",
    "Knowledge: warn, pause, then deliver the information in plain language "
    "in small chunks — no jargon",
    "Emotions: respond to the reaction BEFORE more information — name the "
    "silence, allow it",
    "Strategy and summary: agree concrete next steps; write them down; "
    "book the follow-up before they leave",
]

def safety_net_formula(what_to_expect: str, what_changes_mind: str,
                       timescale: str) -> str:
    return (f"Expected course: {what_to_expect}. Come back or seek urgent "
            f"care if: {what_changes_mind}. Timeframe: {timescale}. "
            "Say it, then write it down.")

DIFFICULT_CONSULTATIONS = {
    "the_angry_patient": [
        "Anger is usually fear wearing armour — ask about the fear under it",
        "Do not match tone; slow down, lower volume",
        "Acknowledge explicitly: 'I can see this has been frustrating' — "
        "before any explanation",
        "Separate the system's failure from your own: apologise for what "
        "you own, explain what you will do next",
        "Never block the exit; stay seated; if threatened, end the "
        "consultation and follow the practice protocol",
    ],
    "the_reassurance_seeker": [
        "Repeated reassurance without exploration feeds the loop",
        "Ask what the worry would mean if true (catastrophic meaning drives "
        "the return)",
        "Reassure against the SPECIFIC fear, with the evidence: 'the ECG "
        "shows X, which is why this isn't Y'",
        "Agree a plan for if symptoms change — structure replaces infinite "
        "reassurance",
    ],
    "the_bringer_of_lists": [
        "Negotiate the agenda in the first minute; the list is anxiety "
        "management, not rudeness",
        "Pick one or two items together; book the rest — do not attempt all "
        "in ten minutes",
    ],
    "the_silent_patient": [
        "Silence is data: allow it, count five seconds before filling it",
        "Try the indirect route: 'Some people with this find it hard to "
        "talk about — is that how it is for you?'",
        "Consider depression, shame, coercion, or a hidden agenda (the "
        "presenting complaint is not the complaint)",
    ],
    "the_internet_researcher": [
        "Ask what they found and what worried them — engage, never mock",
        "Use their research as a shared document to correct — 'this part "
        "doesn't apply to you because...'",
    ],
    "the_denier": [
        "Check understanding of what has been said — denial is often "
        "unprocessed shock",
        "Do not argue; leave the door marked: 'this stays on the table "
        "whenever you want to return to it'",
        "Enlist a trusted person (with consent); document the refusal "
        "conversation and the capacity assessment",
    ],
}

def uncertainty_scripts() -> List[str]:
    return [
        "I don't know yet — and here is how we'll find out: [tests]. "
        "Here is what would change my mind: [signs].",
        "There are three possibilities at this point; today's job is to "
        "narrow them, not to guess.",
        "I can tell you what this isn't, which matters as much as what "
        "it is.",
        "If you're worse in [timescale], that isn't the plan failing — "
        "it's information, and I want to see it.",
    ]

CONSULTATION_MODELS = {
    "calgary_cambridge": "Structural: initiating the session, gathering "
                         "information, explanation & planning, closing — "
                         "with the relationship continuous throughout",
    "balint": "The doctor as drug: the consultation's therapeutic effect "
              "and the patient's 'offer'",
    "neighbour": "Five checkpoints: connecting, summarising, handing over, "
                 "safety-netting, housekeeping",
    "pendleton_functional": "Consultation tasks: reason for attendance, "
                            "considered actions, doctor's management, "
                            "achieving shared understanding and shared plans",
}
```

- [x] **Step 1: failing tests:**

```python
"""Tests for consultation skills (expertise program Stage 5)."""
import pytest
from gpdisc_core.consultation_skills import (
    ice_questions, chunking_rules, spikes_steps, safety_net_formula,
    difficult_consultation_guidance, uncertainty_scripts, CONSULTATION_MODELS,
)


class TestConsultationSkills:
    def test_ice_three_core_questions(self):
        q = ice_questions()
        assert len(q) == 3
        assert any("think" in x for x in q)
        assert any("worried" in x for x in q)
        assert any("hoping" in x for x in q)

    def test_ice_tailors_to_cancer_fear(self):
        q = ice_questions("I'm worried this is cancer")
        assert len(q) == 4 and any("Name the fear" in x for x in q)

    def test_chunking_five_rules(self):
        assert len(chunking_rules()) == 5

    def test_spikes_six_steps_in_order(self):
        s = spikes_steps()
        assert len(s) == 6
        assert s[0].startswith("Setting") and s[5].startswith("Strategy")

    def test_safety_net_formula(self):
        s = safety_net_formula("viral illness settles in a week",
                               "rash that doesn't fade, drowsiness",
                               "48 hours")
        assert "viral illness" in s and "48 hours" in s

    def test_six_difficult_consultations(self):
        assert len(difficult_consultation_guidance("the_angry_patient")) >= 3
        assert difficult_consultation_guidance("the_dragon") == []

    def test_uncertainty_scripts_honest(self):
        s = uncertainty_scripts()
        assert any("I don't know" in x for x in s)

    def test_four_models(self):
        assert len(CONSULTATION_MODELS) == 4
```

- [x] **Step 2: verify fail.** **Step 3: implement** (`__init__.py` re-exports everything). **Step 4: run** (8 pass). **Step 5: commit** `feat(consultation_skills): the doctor craft — ICE, SPIKES, safety-net formula, difficult consultations, uncertainty scripts`.

---

### Task 2: benign_vs_emergency — the discrimination pairs

**Files:**
- Create: `gpdisc_core/clinical_reasoning/benign_vs_emergency.py`
- Test: `gpdisc_core/tests/test_benign_vs_emergency.py`

**Interfaces:**
- Produces: `DiscriminationPair(benign_presentation, emergency_presentation, benign_condition, emergency_condition, discriminators: List[str])`, `PAIRS: List[DiscriminationPair]` (10), `find_pairs(text) -> List[DiscriminationPair]` (matches either side by condition id or keyword), and verification via the real SafetyLayer: for each pair, the emergency presentation must screen ≥ URGENT.

```python
_ROWS = [
    # (benign_text, emergency_text, benign_id, emergency_id, discriminators)
    ("mild bilateral headache coming on over days after stress",
     "worst headache of my life instantly like a blow an hour ago, vomiting",
     "tension_headache", "sah_subarachnoid",
     ["Speed of onset (seconds vs days)", "Severity 'worst ever'",
      "Vomiting, neck stiffness, photophobia", "Thunderclap = first SAH "
      "until excluded"]),
    ("musculoskeletal chest pain, tender rib, worse on movement after gym",
     "crushing central chest pain 30 minutes, sweating, radiating to left arm",
     "musculoskeletal_chest_pain", "acs_stemi",
     ["Exertional vs movement-related", "Autonomic sweating (ACS)",
      "Reproducible tenderness (musculoskeletal)", "Duration and crescendo"]),
    ("simple faint in a hot room with minutes of warning",
     "blackout with no warning while sitting, palpitations before",
     "vasovagal_syncope", "cardiac_syncope",
     ["Prodrome (hot, dizzy, vision greying) vs none",
      "Trigger (standing, heat) vs no position",
      "Palpitations before = arrhythmia until proved otherwise"]),
    ("gastroenteritis, cramping pain with diarrhoea settling",
     "severe constant abdominal pain out of proportion, no diarrhoea, "
     "distended and tender",
     "gastroenteritis", "acute_mesenteric_ischaemia",
     ["Pain out of proportion to findings", "Constant vs colicky",
      "Blood in stool, AF history", "Rapid deterioration"]),
    ("panic attack with tingling fingers and breathlessness in a young adult",
     "sudden breathlessness with sharp pleuritic pain and a swollen calf "
     "after a long flight",
     "panic_attack", "pe_pulmonary_embolism",
     ["Calf swelling/immobility/recent surgery (PE risk)", "Pleuritic "
      "pain and haemoptysis", "Tingling fingers and hyperventilation "
      "(panic)"]),
    ("reactive lymph node after a sore throat, small and tender",
     "painless hard neck lump enlarging over six weeks, night sweats",
     "lymphadenopathy_reactive", "lymphoma_suspect",
     ["Tender+small+recent (reactive) vs painless+progressive",
      "Night sweats, weight loss, itch", "Alcohol-induced pain (rare, "
      "Hodgkin)", "Persistent >6 weeks = 2ww"]),
    ("simple lower back pain after lifting, no neurology",
     "back pain with numbness in the saddle area and can't pass urine",
     "back_pain_mechanical", "cauda_equina",
     ["Urinary retention/incontinence", "Saddle anaesthesia", "Bilateral "
      "leg weakness", "Constipation from any cause does NOT exclude it"]),
    ("young adult vertigo on head movement, seconds at a time",
     "sudden continuous vertigo with double vision, slurred speech, "
     "weakness on one side",
     "bppv", "stroke_tia",
     ["Positional seconds (BPPV) vs continuous", "ANY other neurological "
      "sign", "Direction of nystagmus", "HINTS exam (specialist use)"]),
    ("child with fever and blanching viral rash, drinking normally",
     "3 year old with fever and a rash that does not fade when pressed, "
     "drowsy and cold hands",
     "viral_rash_child", "meningococcal_child",
     ["Glass test: blanching vs non-blanching", "Drowsiness, poor drinking",
      "Cold peripheries/leg pain", "Rapid progression over hours"]),
    ("teenager with mono, tired with a sore throat, glandular fever",
     "muffled 'hot potato' voice, drooling, can't swallow saliva, trismus",
     "glandular_fever", "epiglottitis_adult",
     ["Drooling or trismus = airway emergency", "Voice change (hot "
      "potato)", "Posture preferring to sit up", "Do NOT examine the "
      "throat or lie them down"]),
]
```

Implementation: dataclass + `_build()` + `find_pairs(text)` matching condition ids or distinctive keywords. The TEST verifies against the live SafetyLayer: emergency side escalates ≥ urgent for 8/10 pairs (allow 2 that rely on clinical judgement wording: cardiac_syncope, lymphoma_suspect if wording slips — verify individually at implementation and keep only achievable assertions; clinical accuracy wins over the 8/10 round number).

- [x] **Step 1: failing tests:**

```python
"""Tests for benign-vs-emergency discrimination (Stage 5)."""
from gpdisc_core.clinical_reasoning.benign_vs_emergency import (
    PAIRS, DiscriminationPair, find_pairs,
)
from gpdisc_core.clinical_reasoning.safety import SafetyLayer, EscalationLevel


class TestDiscriminationPairs:
    def test_ten_pairs(self):
        assert len(PAIRS) == 10
        for p in PAIRS:
            assert p.discriminators

    def test_find_pairs_by_condition(self):
        hits = find_pairs("sah_subarachnoid")
        assert any(p.emergency_condition == "sah_subarachnoid" for p in hits)

    def test_find_pairs_by_keyword(self):
        hits = find_pairs("rash that doesn't fade")
        assert any(p.emergency_condition == "meningococcal_child" for p in hits)

    def test_no_match_empty(self):
        assert find_pairs("prescription request") == []


class TestPairsAgainstLiveSafetyLayer:
    sl = SafetyLayer()

    def test_emergency_sides_escalate(self):
        escalated = 0
        for p in PAIRS:
            a = self.sl.screen(p.emergency_presentation, {})
            if a.level in (EscalationLevel.URGENT, EscalationLevel.EMERGENCY):
                escalated += 1
        assert escalated >= 8  # emergency twins must be caught

    def test_benign_sides_do_not_emergency_escalate(self):
        for p in PAIRS:
            a = self.sl.screen(p.benign_presentation, {})
            assert a.level != EscalationLevel.EMERGENCY, p.benign_presentation
```

- [x] **Step 2: verify fail.** **Step 3: implement.** **Step 4: run** (6 pass — adjusting the two threshold counts per verified behaviour if needed, clinical accuracy first). **Step 5: commit** `feat(clinical_reasoning): benign-vs-emergency discrimination pairs (10 twins)`.

---

### Task 3: regression bank — diagnostic reasoning as executable curriculum

**Files:**
- Create: `gpdisc_core/tests/regression_bank.py` (data module: `BANK: List[dict]`)
- Test: `gpdisc_core/tests/test_regression_bank.py`

**Interfaces:**
- `BANK` entries: `{"case": str, "escalation": str|None, "leader_or_retained": List[str], "syndrome": str|None}` — 40 cases spanning all 5 stages (ACS/SAH/sepsis/cauda equina from Stage 1; malaria/syndromes from Stage 2; the multimorbidity and debate paths from Stage 4; benign presentations that must NOT escalate).
- Test: for every case, run `ConsultationPipeline().run(case)` and assert escalation matches (if specified), at least one of `leader_or_retained` appears in ranked ids + retained ids + syndrome differentials, and syndrome matches (if specified).

**Bank content (write at implementation, verify case-by-case, 40 rows):** ~14 emergencies (chest pain variants, stroke FAST, sepsis clusters adult+child, thunderclap, cauda equina, meningococcal rash, epiglottitis, VHF-suspect wording, pregnancy bleeding, PE), ~10 urgent (fever after travel ×3 destinations, pyelonephrosis wording, 2ww-tier conditions — oral cancer non-healing ulcer, haemoptysis over 40), ~12 routine/benign (tension headache, mechanical back pain, hayfever, acne, viral URTI, BPPV, glandular fever, impetigo, dyspepsia under 55, domestic travel fever non-malarious, contraception routine, medication review), ~4 syndrome cases (eosinophilia Kenya, fever+thrombocytopenia Vietnam, fever+jaundice wording, fever+rash non-blanching child).

- [x] **Step 1: failing tests:**

```python
"""The dangerous-mimic regression bank — diagnostic reasoning as curriculum."""
import pytest
from gpdisc_core.tests.regression_bank import BANK
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline


class TestRegressionBank:
    pipe = ConsultationPipeline()

    def test_bank_has_40_cases(self):
        assert len(BANK) == 40
        for entry in BANK:
            assert entry["case"] and entry["leader_or_retained"]

    def test_every_case_produces_a_record(self):
        for entry in BANK:
            rec = self.pipe.run(entry["case"], {})
            assert rec.presenting_complaint or rec.problem_representation

    def test_escalations_hold(self):
        checked = 0
        for entry in BANK:
            if entry.get("escalation") is None:
                continue
            rec = self.pipe.run(entry["case"], {})
            assert rec.escalation == entry["escalation"], (
                entry["case"], rec.escalation)
            checked += 1
        assert checked >= 24  # most of the bank pins escalation

    def test_leaders_or_retained_present(self):
        for entry in BANK:
            rec = self.pipe.run(entry["case"], {})
            ids = ({d["condition_id"] for d in rec.ranked_differential}
                   | {d["condition_id"] for d in rec.dangerous_alternatives}
                   | {d["condition_id"] for d in rec.syndrome_differentials})
            assert ids & set(entry["leader_or_retained"]), (
                entry["case"], ids)

    def test_syndromes_hold(self):
        checked = 0
        for entry in BANK:
            if not entry.get("syndrome"):
                continue
            rec = self.pipe.run(entry["case"], {})
            assert rec.syndrome == entry["syndrome"], entry["case"]
            checked += 1
        assert checked >= 3
```

- [x] **Step 2: verify fail** (regression_bank module missing). **Step 3: implement** the bank data module; run the test; for every failing row, decide clinically: fix the expectation (if the engine's behaviour is defensible) or fix the engine/knowledge (if a dangerous gap). Iterate until green with honest rows only — no expectation may be weakened just to pass. **Step 4: run** (5 pass). **Step 5: commit** `test: dangerous-mimic regression bank — 40 locked diagnostic reasoning cases`.

---

### Task 4: wiring + final battery + docs + program close-out

**Files:**
- Modify: `gpdisc_core/clinical_reasoning/__init__.py` (export benign_vs_emergency names)
- Modify: `CLAUDE.md` (Stage 5 section + testing lines)
- Memory update; tick checkboxes

- [x] **Step 1:** export `DiscriminationPair, PAIRS, find_pairs` from `gpdisc_core.clinical_reasoning`; run uk/all suites to confirm no break.
- [x] **Step 2: final full battery** — all 8 suites (171 + consultation_skills 8 + benign 6 + bank 5 = 190), comprehensive 26/26, test_all 11/3 baseline, import sweep 0 failures.
- [x] **Step 3: CLAUDE.md** — "### Consultation Skills + Discrimination Pairs + Regression Bank (Stage 5)" section; Testing line.
- [x] **Step 4: commit** docs; update memory (program COMPLETE); tick checkboxes; commit.

---

## Self-Review (completed)

- **Spec coverage:** consultation/doctor skills (weighted "most heavily" by Glenn) → Task 1; benign-vs-emergency discrimination (acute & emergency medicine emphasis) → Task 2; "more training effort on diagnostic reasoning across diseases" → Task 3 regression bank; depth across endocrine/paediatrics/geriatrics is carried by the Stage 1 corpus + Stage 4 geriatrician role rather than new modules (recorded in the section's note).
- **Placeholders:** Task 3's bank content is enumerated by category counts and composed at implementation from cases verified against the live pipeline — no unspecified deliverable.
- **Type consistency:** `find_pairs` returns `List[DiscriminationPair]`; bank dict keys match the test's reads (`case`, `escalation`, `leader_or_retained`, `syndrome`).
