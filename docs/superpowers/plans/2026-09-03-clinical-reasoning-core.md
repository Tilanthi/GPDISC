# Clinical Reasoning Core (Stage 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Level 1 + Level 6 clinical reasoning core — a diagnostic engine with ranked differentials and Bayesian test interpretation, a consultation pipeline, and a safety/metacognition layer — and wire it as the GP-led front door of the system's `answer()` path.

**Architecture:** New package `gpdisc_core/clinical_reasoning/` with five modules: `knowledge.py` (structured condition corpus), `test_interpretation.py` (Bayesian lab/test math), `safety.py` (escalation classifier + emergency overlays), `diagnostic_engine.py` (differential construction), `consultation.py` (pipeline state machine emitting a `ConsultationRecord`). `EnhancedUnifiedGPDISCSystem.answer()` routes medical queries through a safety screen and the engine before consulting specialty domains.

**Tech Stack:** Python 3.10+ stdlib only (dataclasses, enum, re, math). No new dependencies.

**Spec:** `docs/superpowers/specs/2026-09-03-gp-expertise-program-design.md` (Stage 1)

## Global Constraints

- Package is `gpdisc_core` (never `medidisc_core`); factory is `create_gpdisc_system()`.
- Local-only: no external API calls, no network. No git push — ever — without explicit instruction from Glenn.
- Every consultation output carries: confidence, red flags screened, safety-net advice, escalation tier.
- Clinical values must be defensible; quantitative test characteristics cite the named rule/source in the `source` field.
- Existing regression baseline must stay green: comprehensive test 26/26; 5 domain tests pass; import sweep 497 submodules 0 failures; `test_all.py` 11 pass / 3 legacy failures.
- Tests run with `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v`.

---

### Task 1: Knowledge schema + corpus part 1 (emergency-weighted conditions)

**Files:**
- Create: `gpdisc_core/clinical_reasoning/__init__.py`
- Create: `gpdisc_core/clinical_reasoning/knowledge.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Produces: `ConditionProfile`, `SymptomFrequency`, `InvestigationProfile` dataclasses; `CONDITIONS: list[ConditionProfile]`; `SYMPTOM_SYNONYMS: dict[str, list[str]]`; `find_condition(condition_id) -> ConditionProfile | None`; `conditions_for_symptom(token) -> list[ConditionProfile]`.

- [ ] **Step 1: Write the failing schema/corpus integrity test**

```python
# gpdisc_core/tests/test_clinical_reasoning.py
"""Tests for the GPDISC clinical reasoning core (Stage 1)."""
import pytest

from gpdisc_core.clinical_reasoning.knowledge import (
    CONDITIONS, SYMPTOM_SYNONYMS, ConditionProfile,
    find_condition, conditions_for_symptom,
)

VALID_TIERS = {"self_care", "routine", "urgent", "two_week_wait", "emergency"}

class TestCorpusIntegrity:
    def test_all_entries_are_profiles(self):
        assert all(isinstance(c, ConditionProfile) for c in CONDITIONS)

    def test_ids_unique(self):
        ids = [c.condition_id for c in CONDITIONS]
        assert len(ids) == len(set(ids))

    def test_every_field_populated(self):
        for c in CONDITIONS:
            assert c.name and c.category
            assert c.symptoms, c.condition_id
            assert 0.0 < c.prevalence_per_consult <= 0.5, c.condition_id
            for s in c.symptoms:
                assert 0.0 < s.frequency <= 1.0
                assert 0.0 <= s.specificity <= 1.0
            assert c.referral_tier in VALID_TIERS, c.condition_id
            assert c.safety_net and c.management_first_line

    def test_every_symptom_token_has_synonyms(self):
        tokens = {s.symptom for c in CONDITIONS for s in c.symptoms}
        for tok in tokens:
            assert tok in SYMPTOM_SYNONYMS, f"missing synonym entry: {tok}"

    def test_find_condition(self):
        assert find_condition("acs_stemi").name  # exemplar below
        assert find_condition("nope") is None

    def test_conditions_for_symptom(self):
        hits = conditions_for_symptom("chest_pain")
        assert any(c.condition_id == "acs_stemi" for c in hits)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'gpdisc_core.clinical_reasoning'`

- [ ] **Step 3: Implement schema, synonyms, and corpus part 1**

`gpdisc_core/clinical_reasoning/__init__.py`:

```python
"""GPDISC clinical reasoning core — Level 1 (diagnostic reasoning) and
Level 6 (safety/metacognition) of the GP expertise architecture."""

from .knowledge import ConditionProfile, CONDITIONS, SYMPTOM_SYNONYMS, find_condition
from .test_interpretation import TestInterpreter
from .safety import SafetyLayer, EscalationLevel
from .diagnostic_engine import DifferentialEngine
from .consultation import ConsultationPipeline, ConsultationRecord

__all__ = [
    "ConditionProfile", "CONDITIONS", "SYMPTOM_SYNONYMS", "find_condition",
    "TestInterpreter", "SafetyLayer", "EscalationLevel",
    "DifferentialEngine", "ConsultationPipeline", "ConsultationRecord",
]
```

`gpdisc_core/clinical_reasoning/knowledge.py` — schema exactly:

```python
"""Structured condition knowledge for the diagnostic engine.

Content model: each condition carries symptom frequencies (proportion of
presenting cases reporting the symptom) and specificities (how strongly the
symptom discriminates toward THIS condition versus its competitors), an
anchoring prevalence in a GP consultation population, red flags,
investigations with test characteristics where established, referral tier,
and safety-net advice. Sources are named in `source`.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SymptomFrequency:
    symptom: str        # canonical snake_case token, must exist in SYMPTOM_SYNONYMS
    frequency: float    # proportion of this condition's presentations, 0-1
    specificity: float  # discriminating power toward this condition, 0-1


@dataclass
class InvestigationProfile:
    name: str
    purpose: str
    sensitivity: Optional[float] = None   # established value or None
    specificity: Optional[float] = None
    source: str = ""                      # e.g. "NICE CG95", "Wells 1997"


@dataclass
class ConditionProfile:
    condition_id: str
    name: str
    category: str                       # e.g. "cardiovascular", "emergency"
    prevalence_per_consult: float       # rough prior among relevant GP consults
    symptoms: List[SymptomFrequency]
    discriminators: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    investigations: List[InvestigationProfile] = field(default_factory=list)
    management_first_line: str = ""
    referral_tier: str = "routine"      # self_care|routine|urgent|two_week_wait|emergency
    safety_net: str = ""
    dangerous_mimic_of: List[str] = field(default_factory=list)  # benign ids it can mimic
    source: str = ""
```

Exemplar entries (write all part-1 entries in this exact pattern — full
fields, defensible values, named sources for numbers):

```python
CONDITIONS: List[ConditionProfile] = [
    ConditionProfile(
        condition_id="acs_stemi",
        name="Acute coronary syndrome (ST-elevation MI)",
        category="cardiovascular_emergency",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("chest_pain", 0.90, 0.55),
            SymptomFrequency("pain_radiating_arm_jaw", 0.50, 0.75),
            SymptomFrequency("sweating", 0.55, 0.4),
            SymptomFrequency("nausea", 0.40, 0.15),
            SymptomFrequency("breathlessness", 0.45, 0.3),
        ],
        discriminators=["persistent >15 min", "cardiac risk factors",
                        "ST elevation on ECG", "troponin rise"],
        red_flags=["ST elevation", "haemodynamic instability", "ongoing pain"],
        investigations=[
            InvestigationProfile("12-lead ECG", "immediate; diagnostic for STEMI",
                                 0.55, 0.95, "NICE CG95 chest pain"),
            InvestigationProfile("high-sensitivity troponin", "myocardial injury; serial",
                                 0.95, 0.80, "NICE NG237 / CG95"),
        ],
        management_first_line="Call 999 (emergency ambulance); aspirin 300 mg chewed "
                              "unless contraindicated; do not delay transfer.",
        referral_tier="emergency",
        safety_net="Any chest pain lasting >15 minutes, or with sweating, nausea or "
                   "breathlessness, is an emergency — call 999 immediately.",
        dangerous_mimic_of=["gerd", "musculoskeletal_chest_pain", "anxiety_atacks"],
        source="NICE NG237 chest pain; ESC 2023 ACS guideline",
    ),
    # ... remaining part-1 entries
]
```

**Part-1 roster (author one entry each, pattern above):**
Emergency-weighted first because the safety layer depends on them:

- Cardiovascular: `acs_stemi`, `acs_nstemi` (troponin-positive without STE), `stable_angina`, `aortic_dissection` (tearing pain, BP differential — mimic of musculoskeletal pain), `pe`, `acute_heart_failure`, `aaa_leak` (mimic of renal colic), `tachyarrhythmia_af`, `hypertensive_urgency`, `infective_endocarditis`
- Respiratory: `asthma_exacerbation`, `copd_exacerbation`, `community_pneumonia` (CURB-65 named in source), `pneumothorax`, `pe_second_entry_not_needed — skip`, `lung_cancer` (2ww tier), `tb_pulmonary`, `covid_like_illness`
- GI: `gerd`, `peptic_ulcer`, `gi_bleed_upper` (emergency, mimic of dyspepsia), `appendicitis` (emergency, mimic of gastroenteritis), `cholecystitis`, `pancreatitis`, `bowel_obstruction`, `diverticulitis`, `ibs`, `gallstones`, `colorectal_cancer` (2ww), `hepatitis_viral`
- Neuro: `stroke_tia` (FAST, mimic of migraine/vestibular), `sah_subarachnoid` (thunderclap — mimic of tension headache/migraine), `meningitis` (emergency), `status_epilepticus` (emergency), `migraine`, `tension_headache`, `bell_palsy`, `gbs_guillain_barre` (ascending weakness — mimic of viral illness), `cauda_equina` (emergency, mimic of sciatica), `encephalitis`
- Benign-mimic anchors (needed so the engine can rank common things common): `musculoskeletal_chest_pain`, `anxiety_atacks` (typo-guard: use this id in both mimic lists and corpus), `viral_urti`, `gastroenteritis`, `lumbago_nonspecific`, `urinary_tract_infection_simple`

`SYMPTOM_SYNONYMS`: map every canonical token used above (and in part 2) to lowercase match phrases, e.g.:

```python
SYMPTOM_SYNONYMS: Dict[str, List[str]] = {
    "chest_pain": ["chest pain", "chest ache", "tightness in chest", "chest pressure"],
    "pain_radiating_arm_jaw": ["radiating to arm", "into left arm", "to jaw", "radiates to"],
    "thunderclap_headache": ["thunderclap", "worst headache", "sudden severe headache",
                             "headache came on like a blow"],
    "fever": ["fever", "temperature", "pyrexia", "febrile", "hot and cold"],
    "ascending_weakness": ["weakness moving up", "legs then arms", "ascending weakness"],
    # ... one entry per token
}
```

Helpers at module foot:

```python
def find_condition(condition_id: str) -> Optional[ConditionProfile]:
    for c in CONDITIONS:
        if c.condition_id == condition_id:
            return c
    return None

def conditions_for_symptom(token: str) -> List[ConditionProfile]:
    return [c for c in CONDITIONS if any(s.symptom == token for s in c.symptoms)]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/ gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): knowledge schema + emergency-weighted condition corpus"
```

---

### Task 2: Corpus part 2 (systematic breadth)

**Files:**
- Modify: `gpdisc_core/clinical_reasoning/knowledge.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Consumes: schema from Task 1.
- Produces: `CONDITIONS` extended to ≥75 entries.

- [ ] **Step 1: Extend the test with a breadth assertion**

```python
    def test_corpus_breadth(self):
        assert len(CONDITIONS) >= 75
        cats = {c.category for c in CONDITIONS}
        for needed in ("endocrine", "infection", "paediatric", "geriatric_frailty",
                       "mental_health", "musculoskeletal", "dermatology",
                       "ent_eye", "womens_health", "urology_kidney", "haematology"):
            assert needed in cats, f"missing category {needed}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestCorpusIntegrity::test_corpus_breadth -v`
Expected: FAIL — `assert 58 >= 75` (or whichever count part 1 reached)

- [ ] **Step 3: Author part-2 entries**

Append to `CONDITIONS`, same pattern as Task 1:

- Endocrine: `t1dm_new`, `t2dm_new`, `dka` (emergency, mimic of gastroenteritis), `hhs` (emergency), `hypoglycaemia` (emergency), `hypothyroidism`, `hyperthyroidism`, `addisonian_crisis` (emergency), `hypercalcaemia_malignancy`
- Infection: `sepsis` (emergency — fever/confusion/tachypnoea cluster), `cellulitis`, `influenza`, `tonsillitis_strep`, `otitis_media`, `pneumonia_aspiration`, `uti_simple` (already part 1 if written), `pyelonephritis`, `infectious_diarrhoea`, `scarlet_fever`, `measles`, `chickenpox`, `hiv_serconversion`
- Paediatric: `febrile_child_serious` (emergency — the seriously-ill-child overlay), `bronchiolitis`, `croup`, `paediatric_asthma`, `intussusception` (emergency), `meningococcal_child` (emergency, non-blanching rash)
- Geriatric/frailty: `delirium` (emergency-urgent — mimic of dementia), `falls_multifactorial`, `frailty_decompensation`, `polypharmacy_adverse_effect` (the multimorbidity entry point), `pressure_ulcer`
- Mental health: `depression_moderate`, `anxiety_generalised`, `panic_disorder`, `psychosis_first_episode` (urgent), `suicide_risk` (emergency), `eating_disorder_anorexia` (urgent), `alcohol_dependence`, `insomnia`
- Musculoskeletal: `osteoarthritis_knee`, `ra_early` (urgent — window for DMARDs), `gout_acute`, `polymyalgia_rheumatica`, `giant_cell_arteritis` (emergency — mimic of tension headache; visual threat), `septic_arthritis` (emergency — mimic of gout), `back_pain_mechanical`, `sciatica_prolapse`, `osteoporotic_fragility_fracture`
- Dermatology: `eczema_atopic`, `psoriasis_plaque`, `cellulitis_lower` (skip if already in infection), `melanoma_suspect` (2ww), `erythema_nodosum`, `shingles`
- ENT/eye: `red_eye_acute_glaucoma` (emergency), `red_eye_conjunctivitis`, `uveitis_anterior` (urgent), `retinal_detachment` (emergency — flashes/floaters/curtain), `sinusitis`, `epistaxis`, `hoarseness_persistent` (2ww), `vertigo_bppv`, `labyrinthitis`
- Women's health: `ectopic_pregnancy` (emergency — mimic of miscarriage/appendicitis), `pregnancy_test_positive_bleeding`, `preeclampsia` (emergency), `pid_pelvic_inflammatory` (urgent), `menorrhagia`, `pms`, `menopausal_symptoms`, `breast_lump_2ww`
- Urology/kidney: `renal_colic`, `aki_dehydration` (urgent), `ckd_progression`, `urinary_retention` (emergency), `prostate_cancer_suspect` (2ww), `haematuria_2ww`, `testicular_torsion` (emergency — mimic of epididymitis)
- Haematology: `ida_iron_deficiency` (with 2ww if male/postmenopausal — put in safety_net), `b12_deficiency`, `anaemia_chronic_disease`, `dvt` (urgent-emergency), `leukaemia_suspect` (2ww), `thrombocytopenia_2ww`, `polycythaemia`
- Tropical taster (full module is Stage 2 — just the fevers the safety layer must catch): `malaria_falciparum` (emergency — fever after travel), `dengue` , `typhoid`

Add every new token to `SYMPTOM_SYNONYMS` (integrity test enforces this).

- [ ] **Step 4: Run all corpus tests**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/knowledge.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): corpus part 2 — systematic breadth across systems"
```

---

### Task 3: TestInterpreter — Bayesian test mathematics

**Files:**
- Create: `gpdisc_core/clinical_reasoning/test_interpretation.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Produces: `TestInterpreter` with `interpret_value(analyte, value) -> str`, `predictive_values(sens, spec, prevalence) -> tuple[float, float]`, `post_test_probability(pre_test, lr) -> float`, `likelihood_ratio_positive(sens, spec) -> float`, `should_investigate(pre_test, condition_investigation, treatment_threshold, test_threshold) -> str`; `REFERENCE_RANGES: dict`.

- [ ] **Step 1: Write the failing tests**

```python
from gpdisc_core.clinical_reasoning.test_interpretation import (
    TestInterpreter, REFERENCE_RANGES,
)

class TestTestInterpreter:
    ti = TestInterpreter()

    def test_ppv_npv_classic_example(self):
        # sens .99, spec .95, prevalence 1% -> PPV ~16.6%, NPV ~99.99%
        ppv, npv = self.ti.predictive_values(0.99, 0.95, 0.01)
        assert ppv == pytest.approx(0.166, abs=0.01)
        assert npv > 0.9998

    def test_post_test_probability_with_lr(self):
        # pre-test 10% odds, LR+ 10 -> post ~52.6%
        assert self.ti.post_test_probability(0.10, 10.0) == pytest.approx(0.526, abs=0.005)

    def test_lr_positive_from_sens_spec(self):
        assert self.ti.likelihood_ratio_positive(0.99, 0.95) == pytest.approx(19.8, abs=0.1)

    def test_lr_below_one_lowers(self):
        assert self.ti.post_test_probability(0.5, 0.1) < 0.15

    def test_reference_range_classification(self):
        assert self.ti.interpret_value("potassium", 3.0) == "low"
        assert self.ti.interpret_value("potassium", 4.2) == "normal"
        assert self.ti.interpret_value("potassium", 6.7) == "critical_high"
        assert self.ti.interpret_value("haemoglobin", 70.0) == "low"

    def test_unknown_analyte(self):
        assert self.ti.interpret_value("not_a_test", 1.0) == "unknown_analyte"

    def test_should_investigate_test_only_if_it_changes_management(self):
        # very low pre-test, weak test, treatment threshold high -> do not test
        decision = self.ti.should_investigate(
            pre_test=0.01,
            sensitivity=0.5, specificity=0.5,
            test_threshold=0.05, treatment_threshold=0.9)
        assert decision == "no_value"
        # positive result would cross treatment threshold -> test
        decision = self.ti.should_investigate(
            pre_test=0.3,
            sensitivity=0.95, specificity=0.9,
            test_threshold=0.05, treatment_threshold=0.6)
        assert decision == "test"
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestTestInterpreter -v`
Expected: FAIL — `ModuleNotFoundError ... test_interpretation`

- [ ] **Step 3: Implement**

```python
"""Bayesian test interpretation: reference ranges, predictive values,
likelihood-ratio arithmetic, and treat/test threshold logic.

Threshold framework follows the classic treat-test/threshold-only-test
model (Djulbegovic & Heng 2007, 'Modern research methodologies').
"""
from typing import Dict, Optional, Tuple

# (low, high, critical_low, critical_high, unit) — adult ambulatory values;
# paediatric ranges differ and are deliberately NOT guessed here.
REFERENCE_RANGES: Dict[str, Tuple[float, float, Optional[float], Optional[float], str]] = {
    "potassium":      (3.5, 5.1, 2.8, 6.0, "mmol/L"),
    "sodium":         (133, 146, 120, 155, "mmol/L"),
    "creatinine":     (60, 110, None, 350, "umol/L"),
    "haemoglobin":    (115, 165, 70, None, "g/L"),
    "crp":            (0.0, 5.0, None, 350, "mg/L"),
    "white_cell":     (4.0, 11.0, 1.5, 25.0, "x10^9/L"),
    "platelets":      (150, 400, 50, 800, "x10^9/L"),
    "glucose_random": (4.0, 7.8, 2.5, 20.0, "mmol/L"),
    "hba1c":          (0.0, 41.0, None, 75.0, "mmol/mol"),
    "tsh":            (0.4, 4.0, 0.01, 20.0, "mU/L"),
    "calcium":        (2.20, 2.60, 1.90, 3.00, "mmol/L"),
    "troponin_hs":    (0.0, 14.0, None, 50.0, "ng/L"),
}


class TestInterpreter:
    def interpret_value(self, analyte: str, value: float) -> str:
        r = REFERENCE_RANGES.get(analyte)
        if r is None:
            return "unknown_analyte"
        low, high, crit_low, crit_high, _unit = r
        if crit_low is not None and value <= crit_low:
            return "critical_low"
        if crit_high is not None and value >= crit_high:
            return "critical_high"
        if value < low:
            return "low"
        if value > high:
            return "high"
        return "normal"

    def predictive_values(self, sens: float, spec: float,
                          prevalence: float) -> Tuple[float, float]:
        tp = sens * prevalence
        fp = (1 - spec) * (1 - prevalence)
        ppv = tp / (tp + fp) if (tp + fp) else 0.0
        fn = (1 - sens) * prevalence
        tn = spec * (1 - prevalence)
        npv = tn / (tn + fn) if (tn + fn) else 0.0
        return ppv, npv

    def likelihood_ratio_positive(self, sens: float, spec: float) -> float:
        return sens / (1 - spec)

    def post_test_probability(self, pre_test: float, lr: float) -> float:
        pre_odds = pre_test / (1 - pre_test) if 0 < pre_test < 1 else pre_test
        post_odds = pre_odds * lr
        return post_odds / (1 + post_odds)

    def should_investigate(self, pre_test: float, sensitivity: float,
                           specificity: float, test_threshold: float,
                           treatment_threshold: float) -> str:
        post_pos = self.post_test_probability(
            pre_test, self.likelihood_ratio_positive(sensitivity, specificity))
        post_neg = self.post_test_probability(pre_test, 1.0 / max(
            self.likelihood_ratio_positive(sensitivity, specificity), 1e-9))
        if post_pos >= treatment_threshold:
            return "test"
        if post_neg > test_threshold:
            return "test"          # negative result still matters
        if post_pos <= test_threshold and post_neg <= test_threshold:
            return "no_value"
        return "test"
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestTestInterpreter -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/test_interpretation.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): Bayesian test interpretation with treat/test thresholds"
```

---

### Task 4: SafetyLayer — escalation classifier and emergency overlays

**Files:**
- Create: `gpdisc_core/clinical_reasoning/safety.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Produces: `EscalationLevel` (EMERGENCY/URGENT/ROUTINE/SELF_CARE), `SafetyAssessment` (level, triggers, emergency_rule, advice), `SafetyLayer.screen(text, context) -> SafetyAssessment`, `SafetyLayer.safety_net_for(condition_id) -> str`, `SafetyLayer.requires_human(assessment) -> bool`.

- [ ] **Step 1: Write the failing tests**

```python
from gpdisc_core.clinical_reasoning.safety import SafetyLayer, EscalationLevel

class TestSafetyLayer:
    sl = SafetyLayer()

    def test_sepsis_cluster_is_emergency(self):
        a = self.sl.screen("My father is confused, breathing fast, feverish and hasn't passed urine since morning", {})
        assert a.level == EscalationLevel.EMERGENCY
        assert any("sepsis" in t for t in a.triggers)

    def test_stroke_fast_is_emergency(self):
        a = self.sl.screen("sudden drooping face and slurred speech this morning", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_thunderclap_headache_is_emergency(self):
        a = self.sl.screen("worst headache of my life came on like a blow an hour ago", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_benign_tension_headache_not_escalated(self):
        a = self.sl.screen("mild bilateral headache after stress for a week, no other symptoms", {})
        assert a.level in (EscalationLevel.ROUTINE, EscalationLevel.SELF_CARE)

    def test_cauda_equina_red_flag(self):
        a = self.sl.screen("back pain and now can't control my bladder, numbness in the saddle area", {})
        assert a.level == EscalationLevel.EMERGENCY
        assert any("cauda" in t for t in a.triggers)

    def test_fever_after_travel_flagged(self):
        a = self.sl.screen("fever for two days since returning from Ghana", {})
        assert a.level == EscalationLevel.URGENT
        assert any("travel" in t for t in a.triggers)

    def test_child_rash_non_blanching(self):
        a = self.sl.screen("my 3 year old has fever and a rash that doesn't fade when pressed", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_pregnancy_bleeding_urgent_plus(self):
        a = self.sl.screen("6 weeks pregnant and bleeding heavily with one-sided pain", {})
        assert a.level == EscalationLevel.EMERGENCY

    def test_safety_net_for_condition(self):
        assert "999" in self.sl.safety_net_for("acs_stemi")

    def test_requires_human(self):
        a = self.sl.screen("crushing chest pain sweating", {})
        assert self.sl.requires_human(a) is True
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestSafetyLayer -v`
Expected: FAIL — `ModuleNotFoundError ... safety`

- [ ] **Step 3: Implement**

```python
"""Level 6 safety and metacognition: emergency overlays that run BEFORE
benign reasoning, escalation classification, and safety-netting.

Design rule: a dangerous cluster detected in free text can never be
downgraded by later benign reasoning. Emergency detection is deliberately
over-inclusive — the cost of a false emergency escalation is a wasted
call; the cost of a missed emergency is a death.
"""
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .knowledge import find_condition


class EscalationLevel(Enum):
    EMERGENCY = "emergency"
    URGENT = "urgent"
    ROUTINE = "routine"
    SELF_CARE = "self_care"


@dataclass
class SafetyAssessment:
    level: EscalationLevel
    triggers: List[str] = field(default_factory=list)
    emergency_rule: str = ""
    advice: str = ""


@dataclass
class EmergencyPattern:
    rule_id: str
    patterns: List[str]          # regex, case-insensitive, all matched on same text
    min_matches: int             # how many patterns must hit
    advice: str


# Emergency rules ordered by clinical priority
EMERGENCY_RULES: List[EmergencyPattern] = [
    EmergencyPattern("sepsis", [
        r"confus", r"breath\w* fast|rapid breath|tachypno",
        r"fever|temperature|rigor",
        r"not (?:passed|passed any) urine|oliguria|mottl",
        r"fast heart|palpitation|tachycard",
    ], 2, "Possible sepsis — this is a medical emergency (999)."),
    EmergencyPattern("stroke_fast", [
        r"face (?:droop|drooping|drooped)|facial droop",
        r"slurr|arm weakness|arm drift|sudden weakness on one side",
        r"speech (?:difficulty|slurred|lost)|can'?t speak|words jumbled",
    ], 1, "Possible stroke — call 999 immediately (FAST). Time = brain."),
    EmergencyPattern("thunderclap_headache", [
        r"worst headache|thunderclap|like a (?:blow|thunder)|hit by",
        r"sudden(?:ly)? (?:severe|worst) headache",
    ], 1, "Possible subarachnoid haemorrhage — emergency assessment now."),
    EmergencyPattern("anaphylaxis", [
        r"swelling of (?:tongue|lips|throat)|throat closing",
        r"difficulty breath\w* (?:after|following) (?:bee|wasp|nut|peanut|sting|food|medicin)",
        r"widespread (?:rash|hives|urticaria).*(breath|swell|faint)",
    ], 1, "Possible anaphylaxis — adrenaline auto-injector and 999."),
    EmergencyPattern("cauda_equina", [
        r"(?:can'?t|cannot|loss of) control (?:of )?(?:my )?bladder|incontinen",
        r"saddle (?:area|numbness|anaesthesia)|numb\w* (?:between|around) (?:the )?legs",
        r"retention",
    ], 1, "Possible cauda equina syndrome — emergency MRI/same-day assessment."),
    EmergencyPattern("meningitis", [
        r"neck stiff|photophobia|light hurts",
        r"non-?blanch\w*|doesn'?t fade when press|doesn'?t disappear when pressed",
        r"fever.*headache|headache.*fever",
        r"bulging fontanelle",
    ], 2, "Possible meningitis — emergency assessment."),
    EmergencyPattern("gi_bleed", [
        r"vomit\w* blood|haematemesis|coffee-?ground",
        r"black tarry|melaena|black stool",
    ], 1, "GI bleeding — same-day emergency assessment."),
    EmergencyPattern("dka", [
        r"thirsty.*passing lots of urine|polyuria",
        r"vomit\w*.*(?:diabet|breath smell|fruity)",
        r"deep (?:fast )?breath\w*|kussmaul",
        r"diabet\w*.*(?:vomit|drowsy|breathless)",
    ], 2, "Possible DKA — emergency; diabetic decompensation."),
    EmergencyPattern("testicular_torsion", [
        r"(?:testicle|testicular|scrotal?).*(?:sudden|swollen|pain)",
    ], 1, "Possible testicular torsion — surgical emergency, time-critical."),
    EmergencyPattern("ectopic_pregnancy", [
        r"pregnan\w*",
        r"(?:one-?sided|lower) (?:abdominal|pelvic|tummy) pain",
        r"bleed\w* (?:heavily|with pain)|shoulder tip pain",
    ], 2, "Possible ectopic pregnancy — emergency."),
    EmergencyPattern("paediatric_rash_fever", [
        r"\b(?:child|toddler|baby|year old|infant)\b",
        r"rash.*(?:doesn'?t|does not) (?:fade|disappear)|non-?blanch",
        r"fever",
    ], 2, "Non-blanching rash with fever in a child — emergency (999)."),
    EmergencyPattern("pe", [
        r"(?:calf )?(?:swollen|painful|red) calf|recent (?:flight|surgery|immobilis)",
        r"breathless.*(?:sudden|pleuritic|chest pain)|pleuritic chest pain",
    ], 2, "Possible pulmonary embolism — urgent assessment same day."),
    EmergencyPattern("acs", [
        r"crush\w* chest pain|chest pain.*(sweat|cold clammy|radiat\w* to (?:arm|jaw))",
        r"chest (?:pain|pressure|tightness).*\b(?:20|30|60|hour|night)s?\b",
    ], 1, "Possible acute coronary syndrome — call 999."),
    EmergencyPattern("visual_curtain", [
        r"curtain.*(?:vision|eye)|flashes? and floaters|sudden (?:vision|sight) loss",
    ], 1, "Possible retinal detachment/glaucoma — same-day emergency eye assessment."),
    EmergencyPattern("status_epilepticus", [
        r"seizure.*(more than|over) (?:five|5) minutes|seizure.*not (?:stopped|waking)",
        r"convulsion.*(continuous|repeated)",
    ], 1, "Status epilepticus — 999."),
]

URGENT_RULES: List[EmergencyPattern] = [
    EmergencyPattern("fever_after_travel", [r"fever|temperature"], 1,
                     "Fever after travel — needs same-day assessment with travel history; malaria until proven otherwise."),
    EmergencyPattern("pregnancy_bleeding_pain", [r"pregnan\w*", r"bleed|pain"], 2,
                     "Bleeding/pain in pregnancy — same-day assessment (EPU)."),
    EmergencyPattern("new_confusion_elderly", [r"confus", r"\b(?:elderly|old|78|80|85|90)\b|\byears?\b"], 2,
                     "New confusion in an older person — same-day assessment; delirium until proven otherwise."),
    EmergencyPattern("self_harm", [r"kill myself|suicide|end it all|self[- ]harm|hurt myself"], 1,
                     "Risk of self-harm — same-day mental-health crisis pathway."),
]


def _match_count(pattern: EmergencyPattern, text: str) -> int:
    n = 0
    for p in pattern.patterns:
        if re.search(p, text, re.IGNORECASE):
            n += 1
    return n


class SafetyLayer:
    def screen(self, text: str, context: Optional[Dict] = None) -> SafetyAssessment:
        t = (text or "")
        ctx_text = t + " " + " ".join(str(v) for v in (context or {}).values())
        for rule in EMERGENCY_RULES:
            if _match_count(rule, ctx_text) >= rule.min_matches:
                return SafetyAssessment(
                    level=EscalationLevel.EMERGENCY,
                    triggers=[rule.rule_id],
                    emergency_rule=rule.rule_id,
                    advice=rule.advice)
        for rule in URGENT_RULES:
            # travel rule only fires if travel actually mentioned
            if rule.rule_id == "fever_after_travel" and not re.search(
                    r"travel|returned|holiday abroad|from (?:Africa|Asia|South America|Ghana|Nigeria|India|Thailand|Kenya)", ctx_text, re.I):
                continue
            if _match_count(rule, ctx_text) >= rule.min_matches:
                return SafetyAssessment(
                    level=EscalationLevel.URGENT,
                    triggers=[rule.rule_id],
                    emergency_rule=rule.rule_id,
                    advice=rule.advice)
        return SafetyAssessment(level=EscalationLevel.ROUTINE,
                                 triggers=[], advice="")

    def safety_net_for(self, condition_id: str) -> str:
        c = find_condition(condition_id)
        return c.safety_net if c else (
            "If symptoms worsen, change, or you feel much unwell, seek urgent medical review.")

    def requires_human(self, assessment: SafetyAssessment) -> bool:
        return assessment.level in (EscalationLevel.EMERGENCY, EscalationLevel.URGENT)
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestSafetyLayer -v`
Expected: 10 passed. If a benign test escalates (e.g. tension headache), tighten the specific regex — never loosen an emergency rule to pass a benign case unless the rule is factually over-broad.

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/safety.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): safety layer — emergency overlays and escalation"
```

---

### Task 5: DifferentialEngine — ranked differentials with anti-anchoring

**Files:**
- Create: `gpdisc_core/clinical_reasoning/diagnostic_engine.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Consumes: `CONDITIONS`, `SYMPTOM_SYNONYMS` (Task 1–2), `TestInterpreter` (Task 3).
- Produces: `RankedDiagnosis(condition_id, name, score, post_test_probability, is_retained_dangerous, reasons)`, `DifferentialResult(ranked, retained_dangerous, key_features, uncertainty)`, `DifferentialEngine.build_differential(presentation_text, context=None) -> DifferentialResult`, `DifferentialEngine.update_with_test(result, condition_id) -> float`.

- [ ] **Step 1: Write the failing tests**

```python
from gpdisc_core.clinical_reasoning.diagnostic_engine import DifferentialEngine

class TestDifferentialEngine:
    eng = DifferentialEngine()

    def test_typical_chest_pain_ranks_acs_in_top3(self):
        r = self.eng.build_differential(
            "66 year old man, chest pain for 40 minutes, sweating, pain radiating to left arm, smoker")
        top3 = [d.condition_id for d in r.ranked[:3]]
        assert "acs_stemi" in top3 or "acs_nstemi" in top3

    def test_common_things_common(self):
        r = self.eng.build_differential(
            "mild bilateral headache coming on over days after stress, no other symptoms")
        top2 = [d.condition_id for d in r.ranked[:2]]
        assert "tension_headache" in top2
        assert "sah_subarachnoid" not in top2

    def test_anti_anchoring_retains_dangerous_alternative(self):
        r = self.eng.build_differential(
            "mild bilateral headache coming on over days after stress, no other symptoms")
        retained_ids = {d.condition_id for d in r.retained_dangerous}
        assert "sah_subarachnoid" in retained_ids or "giant_cell_arteritis" in retained_ids \
            or "meningitis" in retained_ids

    def test_thunderclap_puts_sah_top(self):
        r = self.eng.build_differential(
            "sudden worst headache of my life one hour ago, vomiting")
        assert r.ranked[0].condition_id == "sah_subarachnoid"

    def test_every_result_has_uncertainty_statement(self):
        r = self.eng.build_differential("tired all the time")
        assert r.uncertainty  # non-empty — uncertainty is first-class

    def test_test_update_uses_likelihood_ratios(self):
        p = self.eng.update_with_test({"test": "troponin_hs", "value": 45}, "acs_nstemi")
        assert p > 0.5
        p_neg = self.eng.update_with_test({"test": "troponin_hs", "value": 3}, "acs_nstemi")
        assert p_neg < p
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestDifferentialEngine -v`
Expected: FAIL — `ModuleNotFoundError ... diagnostic_engine`

- [ ] **Step 3: Implement**

```python
"""Diagnostic engine: problem representation from free text, ranked
differential construction, Bayesian updating, and anti-anchoring.

Scoring: each condition scores sum over matched symptom tokens of
(frequency x specificity), anchored by prior prevalence, normalised to a
0-1 score. Anti-anchoring: any condition in the top quartile of
dangerousness (referral_tier emergency/two_week_wait) that shares at
least one matched symptom with the leader is RETAINED and displayed even
when ranked low — the engine is forbidden from presenting a differential
that has pruned every dangerous mimic.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .knowledge import CONDITIONS, SYMPTOM_SYNONYMS
from .test_interpretation import TestInterpreter, REFERENCE_RANGES

DANGEROUS_TIERS = {"emergency", "two_week_wait", "urgent"}


@dataclass
class RankedDiagnosis:
    condition_id: str
    name: str
    score: float
    post_test_probability: Optional[float] = None
    is_retained_dangerous: bool = False
    reasons: List[str] = field(default_factory=list)


@dataclass
class DifferentialResult:
    ranked: List[RankedDiagnosis]
    retained_dangerous: List[RankedDiagnosis]
    key_features: List[str]
    uncertainty: str


def _extract_features(text: str, context: Optional[Dict]) -> List[str]:
    t = (text or "").lower()
    for v in (context or {}).values():
        t += " " + str(v).lower()
    hits = []
    for token, phrases in SYMPTOM_SYNONYMS.items():
        if any(p in t for p in phrases):
            hits.append(token)
    return hits


class DifferentialEngine:
    def __init__(self, conditions: Optional[List] = None):
        self.conditions = conditions or CONDITIONS
        self.interp = TestInterpreter()

    def build_differential(self, presentation: str,
                           context: Optional[Dict] = None) -> DifferentialResult:
        feats = _extract_features(presentation, context)
        scored: List[RankedDiagnosis] = []
        for c in self.conditions:
            matched, s, reasons = [], 0.0, []
            for sf in c.symptoms:
                if sf.symptom in feats:
                    matched.append(sf.symptom)
                    s += sf.frequency * sf.specificity
            if s <= 0:
                continue
            prior = c.prevalence_per_consult
            score = s * (0.5 + 0.5 * min(prior / 0.05, 1.0))  # prior-anchored
            scored.append(RankedDiagnosis(
                condition_id=c.condition_id, name=c.name, score=score,
                reasons=[f"matched: {', '.join(sorted(set(matched)))}"]))
        scored.sort(key=lambda d: d.score, reverse=True)

        # anti-anchoring: retain dangerous conditions sharing a matched feature
        leader_feats = set(feats)
        retained = []
        ranked_ids = {d.condition_id for d in scored[:8]}
        for c in self.conditions:
            if c.referral_tier not in DANGEROUS_TIERS:
                continue
            shares = any(sf.symptom in leader_feats for sf in c.symptoms)
            if shares and c.condition_id not in ranked_ids:
                retained.append(RankedDiagnosis(
                    condition_id=c.condition_id, name=c.name, score=0.0,
                    is_retained_dangerous=True,
                    reasons=["retained as must-not-miss despite low rank"]))
        uncertainty = self._uncertainty_statement(feats, scored)
        return DifferentialResult(ranked=scored[:8], retained_dangerous=retained,
                                  key_features=feats, uncertainty=uncertainty)

    def _uncertainty_statement(self, feats: List[str],
                               scored: List[RankedDiagnosis]) -> str:
        if not feats:
            return ("Insufficient information to localise the problem — the "
                    "medically correct next step is targeted history, not a "
                    "diagnosis. 'I don't know yet' applies.")
        if not scored:
            return ("No corpus condition matched these features; presentation "
                    "is outside current knowledge — human assessment advised.")
        top = scored[0]
        if len(scored) == 1 or (top.score > 0 and scored[1].score / top.score < 0.35):
            return ("Leading diagnosis is favoured but premature closure is a "
                    "known error — dangerous alternatives retained below must "
                    "be actively excluded.")
        return ("Competing hypotheses remain close — treat the differential as "
                "genuinely open and use targeted tests to separate them.")

    def update_with_test(self, result: Dict, condition_id: str) -> float:
        """Update a condition's probability given a test result dict
        {test, value} using corpus test characteristics where available."""
        from .knowledge import find_condition
        c = find_condition(condition_id)
        if c is None:
            return 0.0
        inv = next((i for i in c.investigations if i.name == result.get("test")), None)
        pre = c.prevalence_per_consult
        if inv is None or inv.sensitivity is None or inv.specificity is None:
            return pre
        interp = self.interp.interpret_value(result.get("test", ""), result.get("value", 0))
        lr_pos = self.interp.likelihood_ratio_positive(inv.sensitivity, inv.specificity)
        lr_neg = 1.0 / lr_pos
        lr = lr_pos if interp in ("high", "critical_high", "low", "critical_low") else lr_neg
        return self.interp.post_test_probability(max(pre, 0.01), lr)
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestDifferentialEngine -v`
Expected: 6 passed. If ranking tests fail, adjust corpus frequencies/specificities or synonym coverage — the test scenarios are the clinical ground truth.

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/diagnostic_engine.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): differential engine with anti-anchoring"
```

---

### Task 6: ConsultationPipeline — the consultation state machine

**Files:**
- Create: `gpdisc_core/clinical_reasoning/consultation.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Consumes: `SafetyLayer`, `DifferentialEngine`, `TestInterpreter`.
- Produces: `ConsultationRecord` (dataclass with the 15 stages), `ConsultationPipeline.run(presentation, context) -> ConsultationRecord`, `ConsultationRecord.summary() -> str`.

- [ ] **Step 1: Write the failing tests**

```python
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline

class TestConsultationPipeline:
    pipe = ConsultationPipeline()

    def test_record_has_all_stages(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        for stage in ("presenting_complaint", "history", "problem_representation",
                      "ranked_differential", "dangerous_alternatives",
                      "investigation_strategy", "treatment", "referral",
                      "follow_up", "safety_net"):
            assert hasattr(rec, stage) or stage in rec.stages

    def test_emergency_short_circuits_to_referral(self):
        rec = self.pipe.run("crushing chest pain for 30 minutes, sweating, "
                            "pain radiating to left arm", {})
        assert rec.escalation == "emergency"
        assert "999" in rec.referral or "999" in rec.safety_net

    def test_summary_is_human_readable(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        s = rec.summary()
        assert "Differential" in s and "Safety net" in s

    def test_benign_gets_safety_net_anyway(self):
        rec = self.pipe.run("mild headache for a week after stress", {})
        assert rec.safety_net  # never empty

    def test_uncertainty_is_carried(self):
        rec = self.pipe.run("tired all the time", {})
        assert rec.uncertainty
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestConsultationPipeline -v`
Expected: FAIL — `ModuleNotFoundError ... consultation`

- [ ] **Step 3: Implement**

```python
"""Consultation pipeline: presenting complaint -> history -> background ->
medication/allergies -> risk factors -> targeted examination -> problem
representation -> ranked differential -> dangerous alternatives ->
investigation strategy -> interpretation -> treatment -> referral ->
follow-up -> safety net. Emits a structured ConsultationRecord.

The engine never fabricates history the patient did not give: stages the
input does not populate are marked as questions to ask, which is the
consultation skill of knowing what to ask next.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .diagnostic_engine import DifferentialEngine, DifferentialResult
from .safety import SafetyLayer, EscalationLevel

STAGES = ["presenting_complaint", "history", "background", "medication_allergies",
          "risk_factors", "targeted_examination", "problem_representation",
          "ranked_differential", "dangerous_alternatives", "investigation_strategy",
          "interpretation", "treatment", "referral", "follow_up", "safety_net"]

QUESTIONS_BY_STAGE = {
    "history": ["Onset, character, radiation, timing, severity, exacerbators?",
                "Systemic features: fever, weight loss, night sweats?"],
    "background": "Relevant past history not yet provided — ask.",
    "medication_allergies": "Drug history and allergies not yet provided — ask.",
    "risk_factors": "Smoking, alcohol, family history, occupation, travel?",
    "targeted_examination": "Focused examination guided by the differential.",
}


@dataclass
class ConsultationRecord:
    presenting_complaint: str = ""
    history: List[str] = field(default_factory=list)
    background: str = ""
    medication_allergies: str = ""
    risk_factors: str = ""
    targeted_examination: str = ""
    problem_representation: str = ""
    ranked_differential: List[Dict] = field(default_factory=list)
    dangerous_alternatives: List[Dict] = field(default_factory=list)
    investigation_strategy: List[str] = field(default_factory=list)
    interpretation: str = ""
    treatment: str = ""
    referral: str = ""
    follow_up: str = ""
    safety_net: str = ""
    escalation: str = "routine"
    uncertainty: str = ""
    stages: Dict[str, str] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [f"Presenting complaint: {self.presenting_complaint}"]
        lines.append(f"Problem representation: {self.problem_representation}")
        lines.append("Differential:")
        for d in self.ranked_differential[:5]:
            lines.append(f"  - {d['name']} (score {d['score']:.2f})")
        if self.dangerous_alternatives:
            lines.append("Must-not-miss (retained):")
            for d in self.dangerous_alternatives:
                lines.append(f"  ! {d['name']}")
        if self.investigation_strategy:
            lines.append("Investigations: " + "; ".join(self.investigation_strategy))
        if self.treatment:
            lines.append(f"Treatment: {self.treatment}")
        if self.referral:
            lines.append(f"Referral: {self.referral}")
        lines.append(f"Safety net: {self.safety_net}")
        if self.uncertainty:
            lines.append(f"Uncertainty: {self.uncertainty}")
        return "\n".join(lines)


class ConsultationPipeline:
    def __init__(self, engine: Optional[DifferentialEngine] = None,
                 safety: Optional[SafetyLayer] = None):
        self.engine = engine or DifferentialEngine()
        self.safety = safety or SafetyLayer()

    def run(self, presentation: str, context: Optional[Dict] = None) -> ConsultationRecord:
        rec = ConsultationRecord(presenting_complaint=presentation[:300])
        assessment = self.safety.screen(presentation, context)
        rec.escalation = assessment.level.value

        if assessment.level == EscalationLevel.EMERGENCY:
            rec.stages["presenting_complaint"] = presentation[:300]
            rec.problem_representation = (
                f"EMERGENCY pattern matched: {assessment.emergency_rule}")
            rec.dangerous_alternatives = [{
                "condition_id": assessment.emergency_rule,
                "name": assessment.emergency_rule.replace("_", " ")}]
            rec.referral = f"EMERGENCY: {assessment.advice} Call 999 now."
            rec.safety_net = assessment.advice
            rec.treatment = "Do not delay transfer for further history."
            rec.uncertainty = "Emergency pathway overrides diagnostic refinement."
            return rec

        diff: DifferentialResult = self.engine.build_differential(presentation, context)
        rec.problem_representation = (
            f"{len(diff.key_features)} discriminating features extracted: "
            + ", ".join(diff.key_features[:8]) if diff.key_features
            else "Problem not yet localisable")
        rec.ranked_differential = [
            {"condition_id": d.condition_id, "name": d.name,
             "score": round(d.score, 3), "reasons": d.reasons}
            for d in diff.ranked]
        rec.dangerous_alternatives = [
            {"condition_id": d.condition_id, "name": d.name}
            for d in diff.retained_dangerous]
        rec.uncertainty = diff.uncertainty

        # stages the input did not populate become questions to ask
        for stage, q in QUESTIONS_BY_STAGE.items():
            rec.stages[stage] = q if not getattr(rec, stage, "") else getattr(rec, stage)

        top = diff.ranked[0] if diff.ranked else None
        if top is not None:
            from .knowledge import find_condition
            c = find_condition(top.condition_id)
            if c:
                rec.investigation_strategy = [i.name + " — " + i.purpose
                                              for i in c.investigations]
                rec.treatment = c.management_first_line
                tier_text = {
                    "self_care": "self-care with pharmacy support",
                    "routine": "routine GP review",
                    "urgent": "same-day urgent review",
                    "two_week_wait": "urgent suspected-cancer (2ww) referral",
                    "emergency": "emergency department / 999",
                }
                rec.referral = tier_text.get(c.referral_tier, "routine GP review")
                rec.safety_net = self.safety.safety_net_for(c.condition_id)
        if not rec.safety_net:
            rec.safety_net = ("If symptoms worsen, change, or new red-flag "
                              "features appear, seek urgent medical review.")
        rec.follow_up = "Review if not improving within the expected course, or sooner per safety net."
        return rec
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestConsultationPipeline -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/clinical_reasoning/consultation.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): consultation pipeline state machine"
```

---

### Task 7: Wire into the system front door

**Files:**
- Modify: `gpdisc_core/core/unified_enhanced.py` (`answer()` method, ~line 363)
- Test: `gpdisc_core/tests/test_clinical_reasoning.py`

**Interfaces:**
- Consumes: `ConsultationPipeline`, `SafetyLayer` (Tasks 4–6).
- Produces: `answer()` result dict gains `consultation` (full ConsultationRecord as dict), `escalation` (str), `safety` (dict with triggers/advice) for medical queries; existing keys (`answer`, `confidence`, …) unchanged in shape.

- [ ] **Step 1: Write the failing integration test**

```python
from gpdisc_core.core.unified_enhanced import EnhancedUnifiedGPDISCSystem

class TestFrontDoorWiring:
    def test_emergency_query_carries_escalation(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("crushing chest pain 30 minutes, sweating, radiating to left arm")
        assert r.get("escalation") == "emergency"
        assert "consultation" in r

    def test_benign_query_gets_consultation_record(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("mild headache for a week after stress")
        assert "consultation" in r
        assert r["consultation"]["safety_net"]

    def test_existing_answer_key_preserved(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("What does this ECG show: ST elevation in V1-V4")
        assert "answer" in r
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestFrontDoorWiring -v`
Expected: FAIL — `KeyError: 'escalation'` / missing `consultation`

- [ ] **Step 3: Implement wiring**

In `gpdisc_core/core/unified_enhanced.py`:

1. Import at top: `from gpdisc_core.clinical_reasoning import ConsultationPipeline, SafetyLayer` (guard with try/except ImportError setting both to None if absent, so the enhanced system never hard-fails).
2. In `__init__` of `EnhancedUnifiedGPDISCSystem`, add:
   `self.consultation_pipeline = ConsultationPipeline() if ConsultationPipeline else None`
3. In `answer()`, before returning the existing dict, enrich it:

```python
        # GP-led clinical reasoning front door (Stage 1 of the expertise program)
        if self.consultation_pipeline is not None:
            try:
                rec = self.consultation_pipeline.run(query, context)
                result["consultation"] = {
                    "presenting_complaint": rec.presenting_complaint,
                    "problem_representation": rec.problem_representation,
                    "ranked_differential": rec.ranked_differential,
                    "dangerous_alternatives": rec.dangerous_alternatives,
                    "investigation_strategy": rec.investigation_strategy,
                    "treatment": rec.treatment,
                    "referral": rec.referral,
                    "follow_up": rec.follow_up,
                    "safety_net": rec.safety_net,
                    "escalation": rec.escalation,
                    "uncertainty": rec.uncertainty,
                    "stages": rec.stages,
                }
                result["escalation"] = rec.escalation
                if rec.escalation == "emergency":
                    result["safety"] = {
                        "level": "emergency",
                        "advice": rec.safety_net,
                    }
            except Exception:
                # Reasoning core must never break the consultation system
                pass
        return result
```

Adapt variable names to the actual `answer()` body (the dict may be named differently — follow what is there; the enrichment is additive keys before return).

- [ ] **Step 4: Run to verify pass + no regressions**

Run: `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v`
Expected: all passed (Tasks 1–7 tests).
Run: `python3 -c "from gpdisc_core import create_gpdisc_system; s=create_gpdisc_system(); r=s.answer('I need a second opinion on this diagnosis'); print(r['answer'][:80]); print('escalation:', r.get('escalation'))"`
Expected: answer prints, escalation key present.

- [ ] **Step 5: Commit**

```bash
git add gpdisc_core/core/unified_enhanced.py gpdisc_core/tests/test_clinical_reasoning.py
git commit -m "feat(clinical_reasoning): wire reasoning core into answer() front door"
```

---

### Task 8: Full regression + CLAUDE.md documentation

**Files:**
- Modify: `CLAUDE.md` (Architecture Overview and Quick Start)
- Test: full suite

**Interfaces:** none new — documentation and verification.

- [ ] **Step 1: Run the complete regression battery**

```bash
python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v
python3 gpdisc_core/comprehensive_system_test.py 2>&1 | tail -3
python3 -c "
from gpdisc_core.domains.cardiology import CardiologyDomain
from gpdisc_core.domains.epilepsy import EpilepsyDomain
from gpdisc_core.domains.general_practice import GeneralPracticeDomain
from gpdisc_core.domains.orthopedics import OrthopedicsDomain
from gpdisc_core.domains.pharmacology import PharmacologyDomain
for cls in (CardiologyDomain, EpilepsyDomain, GeneralPracticeDomain, OrthopedicsDomain, PharmacologyDomain):
    d = cls(); d.process_query('test'); print(cls.__name__, 'OK')
"
python3 gpdisc_core/tests/test_all.py 2>&1 | tail -3   # expect 11 pass / 3 legacy fail
```

Expected: all green at baseline.

- [ ] **Step 2: Import sweep still clean**

Run: the walk_packages sweep (497+ submodules, 0 failures).

- [ ] **Step 3: Update CLAUDE.md**

In Architecture Overview, add after the Advanced Capabilities layer:

```
### Clinical Reasoning Core (GP-led front door)

`gpdisc_core/clinical_reasoning/` — Level 1 + Level 6 of the GP expertise
architecture: structured condition corpus, Bayesian test interpretation,
safety/escalation layer with emergency overlays, differential engine with
anti-anchoring, and the consultation pipeline. `answer()` routes every
medical query through safety screening first; emergency patterns are never
downgraded by benign reasoning.
```

Add to Testing section:

```bash
# Clinical reasoning core
python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: document clinical reasoning core in CLAUDE.md"
```

---

## Self-Review Notes

- Spec coverage: Stage 1 of the spec = Tasks 1–8 here (schema+corpus, interpreter, safety, engine, pipeline, wiring, regression). Levels 2–5 are later plans.
- No placeholders: every code block is complete; corpus rosters are explicit per-entry lists with the exemplar defining the pattern and integrity tests as the gate.
- Type consistency: `RankedDiagnosis.score` float; `ConsultationRecord.stages` dict; `SafetyAssessment.level` `EscalationLevel`; `answer()` enrichment keys match Task 7 tests.
