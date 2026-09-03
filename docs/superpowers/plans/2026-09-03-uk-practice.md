# Stage 3: UK Clinical Practice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install Level 4 of the GP expertise architecture: `gpdisc_core/uk_practice/` — the UK-specific regulatory and policy layer (NICE/CKS guideline index, 2ww cancer criteria, DVLA driving rules, MCA/DNACPR/safeguarding, controlled-drug guardrails, antimicrobial stewardship, high-risk prescribing monitoring, fit notes).

**Architecture:** One package, eight focused modules, each a structured table + lookup function. No module depends on another (except `guidelines_index`, standalone). Pure stdlib. Deliberately does NOT duplicate Stage 2's `preventive_medicine` (vaccination/screening cohorts) — this package holds the regulatory remainder of Glenn's UK list.

**Tech Stack:** Python 3.10+ stdlib only, pytest.

**Spec:** `docs/superpowers/specs/2026-09-03-gp-expertise-program-design.md`

## Global Constraints

- Python 3.10+ stdlib only; all data local-only; **NEVER `git push`** (no remote; forbidden by CLAUDE.md).
- All commits LOCAL ONLY on `main`.
- Clinical content reflects UK practice as at 2026 (NICE NG12, DVLA at-a-glance, MCA 2005, Misuse of Drugs Regulations 2001, NICE antimicrobial guidance, BNF monitoring). Tables carry `source` notes; when a rule is guidance-dependent the text says "check current" rather than inventing precision.
- Every module: tuple-rows + builder + dataclass exports + at least one decision function beyond raw table access.

---

### Task 1: Package skeleton + guidelines_index

**Files:**
- Create: `gpdisc_core/uk_practice/__init__.py`
- Create: `gpdisc_core/uk_practice/guidelines_index.py`
- Test: `gpdisc_core/tests/test_uk_practice.py`

**Interfaces:**
- Produces: `GuidelineRef(topic, nice_ref, cks_topic, note)`, `GUIDELINES: List[GuidelineRef]` (24 entries), `lookup_guideline(text: str) -> List[GuidelineRef]` (keyword substring match over topic).

```python
_ROWS = [
    ("chest pain", "NICE CG95", "Chest pain - recent onset", "Typical/angina → rapid-access chest pain clinic; 2ww if lung cancer features"),
    ("atrial fibrillation", "NICE NG196", "Atrial fibrillation", "CHA2DS2-VASc + ORBIT bleed; rate vs rhythm"),
    ("hypertension", "NICE NG136", "Hypertension - not diabetic", "Confirm ABPM/HBPM ≥135/85; A <55y ACEi"),
    ("heart failure", "NICE NG106", "Heart failure - chronic", "NT-proBNP >400 → echo; the 4 pillars"),
    ("type 2 diabetes", "NICE NG28", "Diabetes - type 2", "HbA1c targets individualised; SGLT2 first add-on if CVD/CKD"),
    ("type 1 diabetes", "NICE NG17", "Diabetes - type 1", ""),
    ("copd", "NICE NG115", "Chronic obstructive pulmonary disease", "Spirometry FEV1/FVC <0.7"),
    ("asthma", "NICE NG80", "Asthma", " objective tests before diagnosing in adults"),
    ("stroke", "NICE NG128", "Stroke and TIA", "Recognition: FAST; specialist within 24h"),
    ("tia", "NICE NG128", "Stroke and TIA", "Secondary prevention; carotid imaging"),
    ("epilepsy", "NICE CG137", "Epilepsy", "Specialist within 2 weeks of first seizure"),
    ("migraine", "NICE CG150", "Migraine", "Zolmitriptan nasal if vomiting; combination acute therapy"),
    ("depression", "NICE NG222", "Depression", "PHQ-9; stepped care"),
    ("generalised anxiety", "NICE CG113", "Generalised anxiety disorder", "GAD-7; low-intensity CBT first"),
    ("dementia", "NICE NG97", "Dementia", "Cognitive testing + history; do not use bloods alone"),
    ("urinary tract infection", "NICE NG109", "Urinary tract infection - lower", "Nitrofurantoin 100mg MR BD 3d women; 7d men"),
    ("pyelonephritis", "NICE NG109", "Urinary tract infection - upper", "Cefalexin or consider admission"),
    ("sore throat", "NICE NG84", "Sore throat - acute", "FeverPAIN; delayed prescribing"),
    ("otitis media", "NICE NG91", "Otitis media - acute", "No antibiotic or delayed 4-5d"),
    ("sinusitis", "NICE NG79", "Sinusitis - acute", "≥10 days + worsening course"),
    ("cellulitis", "NICE NG141 (antimicrobial)", "Cellulitis - acute", "Mark borders; Eron classification"),
    ("back pain", "NICE NG59", "Back pain - low", "Red flags first; no imaging without"),
    ("contraception", "FSRH 2025 (ceg); NICE", "Contraception", "UKMEC categories; LARC first discussion"),
    ("palliative care", "NICE NG31 + 'Guidelines' (Irish/Scottish used UK-wide)", "Palliative care", "Anticipatory prescribing"),
]
```

- [x] **Step 1: failing tests:**

```python
"""Tests for uk_practice (expertise program Stage 3)."""
import pytest
from gpdisc_core.uk_practice.guidelines_index import (
    GUIDELINES, GuidelineRef, lookup_guideline,
)


class TestGuidelinesIndex:
    def test_24_entries(self):
        assert len(GUIDELINES) == 24

    def test_every_entry_populated(self):
        for g in GUIDELINES:
            assert g.topic and g.nice_ref and g.cks_topic

    def test_lookup_chest_pain(self):
        hits = lookup_guideline("patient with chest pain")
        assert any(g.nice_ref == "NICE CG95" for g in hits)

    def test_lookup_diabetes_matches_both(self):
        hits = lookup_guideline("newly diagnosed type 2 diabetes")
        assert any(g.topic == "type 2 diabetes" for g in hits)

    def test_no_hit_empty(self):
        assert lookup_guideline("moon rocks") == []
```

- [x] **Step 2: verify fail.** **Step 3: implement** (`__init__.py` exports as modules land; initially guidelines only). **Step 4: run** (5 pass). **Step 5: commit** `feat(uk_practice): guidelines index — NICE/CKS reference registry`.

---

### Task 2: two_week_wait — cancer referral criteria

**Files:**
- Create: `gpdisc_core/uk_practice/two_week_wait.py`
- Test: append `class TestTwoWeekWait` to `gpdisc_core/tests/test_uk_practice.py`

**Interfaces:**
- Produces: `TwoWeekWaitRule(cancer_site, trigger, age_floor, sex, action)`, `TWO_WEEK_WAIT_RULES: List[TwoWeekWaitRule]` (16), `two_week_wait_check(text, age=None, sex=None) -> List[TwoWeekWaitRule]` (age-filtered substring trigger match).

```python
# (cancer_site, trigger_phrases, age_floor(None=any), sex(None=any), action)
_ROWS = [
    ("lung", ["haemoptysis", "coughing up blood", "chest x-ray suspicious",
              "chest xray suspicious", "abnormal chest x-ray"], 40, None,
     "Chest X-ray + urgent suspected cancer referral (2ww); X-ray does not exclude cancer if suspicious clinically"),
    ("lung", ["persistent cough", "recurrent chest infection"], 40, None,
     "Chest X-ray; if persistent >3 weeks with risk factors → 2ww"),
    ("colorectal", ["rectal bleeding"], 50, None,
     "Unexplained rectal bleeding ≥50 → 2ww lower GI"),
    ("colorectal", ["iron deficiency anaemia", "ida", "change in bowel habit",
                    "altered bowel habit"], 60, None,
     "Unexplained change in bowel habit or IDA ≥60 → 2ww + FIT as directed"),
    ("colorectal", ["weight loss"], 40, None,
     "≥40 with weight loss + abdominal pain → 2ww"),
    ("oesophago_gastric", ["dysphagia", "difficulty swallowing",
                           "food sticking"], None, None,
     "Dysphagia ANY ADULT AGE → urgent direct-access endoscopy (2ww)"),
    ("oesophago_gastric", ["dyspepsia", "upper abdominal pain", "epigastric pain",
                           "refractory dyspepsia"], 55, None,
     "≥55 with new dyspepsia + weight loss → 2ww upper GI"),
    ("breast", ["breast lump", "breast mass"], 30, None,
     "Breast lump ≥30 (any age if skin/nipple change) → 2ww breast clinic"),
    ("breast", ["nipple eczema", "nipple discharge blood", "unilateral nipple"], 30, "f",
     "Unilateral eczematous nipple change or bloodstained discharge → 2ww"),
    ("ovarian", ["bloating persistent", "abdominal distension", "early satiety",
                 "feeling full quickly", "pelvic pain"], 50, "f",
     "≥50 with persistent bloating/distension/satiety/pelvic pain → CA125 + ultrasound pathway"),
    ("bladder", ["visible haematuria", "blood in my urine", "frank haematuria"], 45, None,
     "Unexplained visible haematuria ≥45 → 2ww urology"),
    ("bladder", ["recurrent urinary tract infection", "persistent urinary tract infection",
                 "recurrent cystitis"], 60, None,
     "≥60 unexplained recurrent/persistent UTI → 2ww (bladder)"),
    ("prostate", ["prostate symptoms", "urinary difficulty man",
                  "weak urine stream man"], 50, "m",
     "Men ≥50 with LUTS → consider PSA + DRE; counsel about PSA limits first"),
    ("skin", ["changing mole", "bleeding mole", "new mole", "skin lesion suspicious",
              "non-healing skin lesion"], None, None,
     "Suspicious pigmented lesion (ABCDEF / dermoscopy) → 2ww skin; photograph"),
    ("oral", ["mouth ulcer not healing", "oral ulcer for 3 weeks",
              "non-healing mouth ulcer", "mouth ulcer that won't heal"], None, None,
     "Any oral ulcer/patch >3 weeks → 2ww head & neck"),
    ("haematological", ["persistent lymph nodes", "persistent swollen glands",
                        "lymphadenopathy persistent"], None, None,
     "Persistent (>6 weeks) non-tender lymphadenopathy → 2ww haematological; check FBC + LDH first"),
]
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.two_week_wait import (
    TWO_WEEK_WAIT_RULES, two_week_wait_check,
)


class TestTwoWeekWait:
    def test_16_rules(self):
        assert len(TWO_WEEK_WAIT_RULES) == 16
        for r in TWO_WEEK_WAIT_RULES:
            assert r.cancer_site and r.trigger and r.action

    def test_haemoptysis_age_46_lung(self):
        hits = two_week_wait_check("coughing up blood for a week", age=46)
        assert any(r.cancer_site == "lung" for r in hits)

    def test_haemoptysis_age_30_no_lung_rule(self):
        hits = two_week_wait_check("coughing up blood", age=30)
        assert not any(r.cancer_site == "lung" for r in hits)

    def test_dysphagia_any_age(self):
        hits = two_week_wait_check("food sticking when I swallow", age=28)
        assert any(r.cancer_site == "oesophago_gastric" for r in hits)

    def test_ovarian_sex_filtered(self):
        hits = two_week_wait_check("persistent bloating and early satiety",
                                   age=62, sex="f")
        assert any(r.cancer_site == "ovarian" for r in hits)
        hits_m = two_week_wait_check("persistent bloating and early satiety",
                                     age=62, sex="m")
        assert not any(r.cancer_site == "ovarian" for r in hits_m)

    def test_breast_lump_over_30(self):
        hits = two_week_wait_check("found a breast lump", age=41, sex="f")
        assert any(r.cancer_site == "breast" for r in hits)
```

- [x] **Step 2: verify fail.** **Step 3: implement** (substring matching lowercase; `age_floor is None or (age is not None and age >= age_floor)`; sex filter when rule sex set and patient sex known). **Step 4: run** (11 total pass). **Step 5: commit** `feat(uk_practice): 2ww cancer referral criteria (16 rules, NG12-aligned)`.

---

### Task 3: dvla_rules — driving and medical conditions

**Files:**
- Create: `gpdisc_core/uk_practice/dvla_rules.py`
- Test: append `class TestDVLARules`

**Interfaces:**
- Produces: `DrivingRule(condition, keywords, group1_rule, group2_rule, note)`, `DRIVING_RULES: List[DrivingRule]` (14), `driving_rules(text: str, group: int = 1) -> List[DrivingRule]`.

```python
_ROWS = [
    ("First seizure", ["first seizure", "first fit", "single seizure"],
     "6 months off (may reduce to 3 months if low risk on specialist assessment)",
     "5 years off; assessments required",
     "DVLA must be informed; cause sought"),
    ("Epilepsy (established)", ["epilepsy"],
     "12 months seizure-free, or 1 year awake-seizure-free with sleep-only pattern",
     "10 years seizure-free off medication",
     "Medication changes can restart the clock"),
    ("TIA / stroke", ["tia", "stroke", "mini stroke"],
     "1 month off after TIA/stroke",
     "1 month off; licensing review",
     "Recurrent TIAs: until pattern controlled"),
    ("Myocardial infarction", ["heart attack", "myocardial infarction", "mi "],
     "1 week off if uncomplicated + successful treatment (e.g. PCI)",
     "6 weeks; may need functional test",
     "Angina: must not drive if symptomatic"),
    ("Angioplasty (elective)", ["angioplasty", "stent", "pci"],
     "1 week (private); 2 days after elective PCI per DVLA update — check current",
     "6 weeks", "Check current DVLA guidance"),
    ("Syncope", ["syncope", "faint", "blackout"],
     "4 weeks off if unexplained/untreated; 4 days if explained and treated (e.g. vasovagal with prodrome)",
     "Case-by-case; often 3 months",
     "Identify cause; 5-yearly risk review if cardiac"),
    ("Diabetes on insulin", ["insulin", "diabetes on insulin"],
     "3-year licence with hypoglycaemia awareness; monitor blood glucose driving >2h",
     "Annual with consultant report; demonstrated awareness",
     "Hypoglycaemia unawareness: stop driving; renotify"),
    ("Hypoglycaemia unawareness", ["hypo unawareness", "hypoglycaemia unawareness",
                                   "hypo unaware"],
     "Stop driving until awareness restored (usually ≥6 months documented)",
     "Stop driving; specialist confirmation",
     "Most common insulin-driver pitfall"),
    ("Sleep apnoea", ["sleep apnoea", "osa", "obstructive sleep apnoea"],
     "Stop until symptoms controlled AND compliance with therapy",
     "Same; annual review",
     "Excessive sleepiness = the trigger, not the diagnosis"),
    ("Visual field defect", ["visual field", "hemianopia", "field defect",
                             "glaucoma"],
     "Must meet visual field standards; binocular field testing",
     "Higher standard",
     "Acuity: read post-plate at 20m"),
    ("Alcohol misuse", ["alcohol misuse", "alcohol problem"],
     "6 months off after controlled drinking confirmed",
     "1 year; medical review",
     "Dependency: 1 year (group1) after remission"),
    ("Drug misuse", ["drug misuse", "illicit drugs"],
     "6 months - 1 year after cessation per pattern",
     "1 year; testing may be required",
     "Cannabis/persistence varies"),
    ("Dementia / cognitive impairment", ["dementia", "cognitive impairment",
                                         "mci with driving"],
     "Case-by-case: functional driving assessment, informant history",
     "Likely refused at significant impairment",
     "GPS: 'I have to notify DVLA — here is what happens' conversation"),
    ("Pacemaker insertion", ["pacemaker"],
     "1 week off after first implant",
     "6 weeks",
     "ICD: 6 months + licence refused group 2"),
]
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.dvla_rules import DRIVING_RULES, driving_rules


class TestDVLARules:
    def test_14_rules(self):
        assert len(DRIVING_RULES) == 14

    def test_seizure_rule_found(self):
        hits = driving_rules("patient had a first seizure last week")
        assert hits and "seizure" in hits[0].condition.lower()

    def test_insulin_group2_stricter(self):
        g1 = driving_rules("diabetes on insulin", group=1)
        g2 = driving_rules("diabetes on insulin", group=2)
        assert "3-year" in g1[0].group1_rule or "3 year" in g1[0].group1_rule
        assert "Annual" in g2[0].group2_rule

    def test_unknown_empty(self):
        assert driving_rules("sprained ankle") == []
```

- [x] **Step 2: verify fail.** **Step 3: implement** (keyword substring match; return rules whose keywords hit). **Step 4: run** (15 total). **Step 5: commit** `feat(uk_practice): DVLA driving rules (14 conditions, group 1+2)`.

---

### Task 4: capacity_and_safeguarding — MCA, DNACPR, safeguarding, Gillick

**Files:**
- Create: `gpdisc_core.uk_practice/capacity_and_safeguarding.py`
- Test: append `class TestCapacitySafeguarding`

**Interfaces:**
- Produces:
  - `capacity_two_stage_test() -> List[str]` (diagnostic then functional)
  - `best_interests_checklist() -> List[str]`
  - `dnacpr_principles() -> List[str]`
  - `safeguarding_adult_types() -> List[str]` (10)
  - `safeguarding_children_levels() -> List[dict]` (4 levels)
  - `gillick_checklist() -> List[str]`
  - `capacity_concern_keywords(text) -> List[str]`

```python
def capacity_two_stage_test() -> List[str]:
    return [
        "Stage 1 (diagnostic): Is there an impairment of, or disturbance in, the "
        "functioning of the mind or brain? If no → MCA does not apply.",
        "Stage 2 (functional): Can the person (a) understand the information "
        "relevant to the decision, (b) retain it long enough to decide, "
        "(c) use or weigh it, (d) communicate the decision by any means?",
        "All four abilities must be present for capacity; fail any one → lacks "
        "capacity FOR THIS DECISION (capacity is decision-specific and time-specific).",
        "Capacity is presumed — assess, do not assume; unwise decisions ≠ incapacity.",
        "Maximise capacity first: best time of day, hearing aids, glasses, simple "
        "language, involving a trusted person.",
    ]

def best_interests_checklist() -> List[str]:
    return [
        "The person's past and present wishes, feelings, beliefs and values",
        "Written statements made when they had capacity (advance decisions, LPA)",
        "Views of family, carers, attorney or deputy — weigh, not obey",
        "Whether capacity might return (reassess later / defer non-urgent decisions)",
        "Least restrictive option that achieves the purpose",
        "Involve the person in the decision as far as possible",
        "For serious medical treatment: consider IMCA if no family/friends",
    ]

def dnacpr_principles() -> List[str]:
    return [
        "A DNACPR decision is about CPR ONLY — it does not stop any other treatment.",
        "Should be made in advance as part of emergency care planning (ReSPECT), "
        "not left to the moment of arrest.",
        "Where capacity exists: the patient's informed decision governs; discuss "
        "in plain language what CPR can and cannot achieve for them.",
        "Where capacity is lacking: best-interests decision (futility, burden, "
        "outcome), documented with reasons.",
        "Aim to involve family/representatives; disagreement → second opinion, "
        "ethics support, or court for unresolved dispute.",
        "Review the decision when circumstances change; communicate it across "
        "care settings (ambulance, out-of-hours, care home).",
    ]

SAFEGUARDING_ADULT_TYPES = [
    "Physical abuse", "Sexual abuse", "Psychological/emotional abuse",
    "Financial/material abuse", "Neglect and acts of omission",
    "Self-neglect", "Discriminatory abuse", "Organisational abuse",
    "Domestic abuse (including coercive control)", "Modern slavery",
]

SAFEGUARDING_CHILDREN_LEVELS = [
    {"level": 1, "name": "Universal", "detail": "All children — universal services, GP registration"},
    {"level": 2, "name": "Additional need", "detail": "Early help (Team Around the Family); no statutory threshold"},
    {"level": 3, "name": "Complex need / child in need (s17)",
     "detail": "Statutory social care assessment required"},
    {"level": 4, "name": "Child protection / s47",
     "detail": "Significant harm suspected → referral same day + strategy discussion"},
]

def gillick_checklist() -> List[str]:
    return [
        "Understands the advice and its implications (including risks)",
        "Cannot be persuaded to inform parents / to allow clinician to do so",
        "Likely to begin or continue sexual activity without contraception",
        "Physical or mental health likely to suffer without treatment",
        "Best interests require treatment WITHOUT parental consent",
    ]

_CONCERN_KEYWORDS = {
    "capacity_fluctuating": ["fluctuating capacity", "confusion comes and goes",
                             "lucid intervals"],
    "undue_influence": ["undue influence", "controlling", "won't let them speak",
                        "always answers for them"],
    "coercive_control": ["coercive control", "checks her phone", "not allowed out"],
    "financial_abuse": ["money missing", "pressure to change the will",
                        "new best friend managing finances"],
    "self_neglect": ["not eating", "hoarding", "squalor", "refusing care"],
    "pressure_ulcer_neglect": ["pressure ulcer", "pressure sore at home"],
}
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.capacity_and_safeguarding import (
    capacity_two_stage_test, best_interests_checklist, dnacpr_principles,
    safeguarding_adult_types, safeguarding_children_levels, gillick_checklist,
    capacity_concern_keywords,
)


class TestCapacitySafeguarding:
    def test_capacity_two_stage(self):
        stages = capacity_two_stage_test()
        assert any("Stage 1" in s for s in stages)
        assert any("Stage 2" in s for s in stages)
        assert any("decision-specific" in s for s in stages)

    def test_best_interests_items(self):
        ci = best_interests_checklist()
        assert any("least restrictive" in s.lower() for s in ci)
        assert any("IMCA" in s for s in ci)

    def test_dnacpr_scope_limited_to_cpr(self):
        assert any("CPR only" in p or "CPR ONLY" in p for p in dnacpr_principles())

    def test_ten_adult_abuse_types(self):
        assert len(safeguarding_adult_types()) == 10

    def test_children_levels(self):
        lv = safeguarding_children_levels()
        assert [x["level"] for x in lv] == [1, 2, 3, 4]
        assert "significant harm" in lv[3]["detail"].lower()

    def test_gillick_five(self):
        assert len(gillick_checklist()) == 5

    def test_concern_keywords(self):
        hits = capacity_concern_keywords("daughter always answers for him "
                                         "and checks her phone")
        assert "undue_influence" in hits and "coercive_control" in hits
```

- [x] **Step 2: verify fail.** **Step 3: implement.** **Step 4: run** (22 total). **Step 5: commit** `feat(uk_practice): MCA/DNACPR/safeguarding knowledge — two-stage test, checklists, abuse types`.

---

### Task 5: controlled_drugs — schedules and prescribing guardrails

**Files:**
- Create: `gpdisc_core/uk_practice/controlled_drugs.py`
- Test: append `class TestControlledDrugs`

**Interfaces:**
- Produces: `controlled_drug_class(drug: str) -> str` ("" if not CD), `CD_SCHEDULES: Dict[str, List[str]]`, `prescribing_guardrails(drug: str) -> List[str]`, `CD_SAFE_PRACTICE: List[str]`.

```python
CD_SCHEDULES = {
    "1": ["heroin (diamorphine for special licence)", "lysergide", "mdma", "psilocin"],
    "2": ["morphine", "diamorphine", "fentanyl", "oxycodone", "pethidine",
          "methadone", "amphetamine", "methylphenidate"],
    "3": ["buprenorphine", "temazepam is NOT (moved)", "midazolam is 3? no - see note",
          "flunitrazepam", "ketamine (special rules)", "buprenorphine for dependence"],
    "4": ["diazepam", "lorazepam", "zopiclone", "zolpidem", "temazepam",
          "clonazepam", "nitrazepam", "midazolam"],
    "5": ["codeine preparations <100mg with other actives", "morphine oral solution "
          "low-concentration preparations", "kaolin & morphine"],
}
```

**Correction during implementation:** the schedule-3 row above contains draft noise — write it as `["buprenorphine", "ketamine (special rules)", "flunitrazepam", "temazepam was moved to 4 — see schedule 4"]` and note that midazolam is schedule 4 (it is — Midazolam: Sch 4 Part 1 in the UK).

```python
_GUARDRAILS = {
    "fentanyl_patch": ["NEVER initiate patches in opioid-naïve patients — "
                       "only after ≥60mg oral morphine-equivalent daily",
                       "Patch change every 72h (some 96h); document site rotation",
                       "After stopping: analgesia persists 12-24h — cover breakthrough"],
    "morphine": ["Start oral MR only when pain controlled on immediate-release",
                 "Prescribe immediate-release for breakthrough at 1/6 total daily dose",
                 "Offer laxative ALWAYS + antiemetic first week; naloxone if overdose risk"],
    "oxycodone": ["Second-line opioid after morphine intolerance/renal issues",
                  "Equianalgesic: oxy 2/3 potency of oral morphine — halve then titrate"],
    "methadone": ["Specialist initiation only — long and variable half-life",
                  "QT monitoring in high dose / with other QT drugs"],
    "diazepam": ["Max 2-4 weeks for anxiety/insomnia — dependence in weeks",
                 "Withdraw slowly after long use (months) to avoid seizures",
                 "No repeat prescribing of borrowed hospital benzodiazepines without review"],
    "zopiclone": ["Same 2-4 week ceiling as benzodiazepines",
                  "No driving next morning if residual sedation"],
    "methylphenidate": ["Shared-care with specialist after titration and stabilisation",
                        "Monitor BP, HR, height/weight 6-monthly"],
    "buprenorphine": ["For dependence: supervised consumption initially; naloxone "
                      "co-prescription recommended"],
}

CD_SAFE_PRACTICE = [
    "Controlled drug register: entries within 24h, kept 2 years after last entry",
    "Instalment prescriptions (FP10MDA) for opioid substitution; quantity in "
    "words AND figures for schedule 2/3",
    "Valid CD prescription: total quantity written in words and figures, "
    "precise dose, prescriber address",
    "Prescribe naloxone to patients at risk of opioid overdose (and family training)",
    "Check the patient's full opioid picture (PDMP/SafeScript-equivalent where available)",
]
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.controlled_drugs import (
    controlled_drug_class, prescribing_guardrails, CD_SAFE_PRACTICE,
)


class TestControlledDrugs:
    def test_schedule_lookup(self):
        assert controlled_drug_class("morphine") == "2"
        assert controlled_drug_class("diazepam") == "4"
        assert controlled_drug_class("codeine 30mg") == ""  # plain codeine not listed as CD here

    def test_fentanyl_patch_guardrail(self):
        g = prescribing_guardrails("fentanyl_patch")
        assert any("opioid-naïve" in x or "opioid-naive" in x for x in g)

    def test_benzo_ceiling(self):
        g = prescribing_guardrails("diazepam")
        assert any("2-4 weeks" in x for x in g)

    def test_unknown_drug_empty(self):
        assert prescribing_guardrails("paracetamol") == []

    def test_safe_practice_nonempty(self):
        assert len(CD_SAFE_PRACTICE) >= 5
```

- [x] **Step 2: verify fail.** **Step 3: implement** (`controlled_drug_class` checks each schedule's drug list by substring; guardrails direct dict lookup). **Step 4: run** (27 total). **Step 5: commit** `feat(uk_practice): controlled drug schedules + prescribing guardrails`.

---

### Task 6: antimicrobial_stewardship — first-line infections

**Files:**
- Create: `gpdisc_core/uk_practice/antimicrobial_stewardship.py`
- Test: append `class TestStewardship`

**Interfaces:**
- Produces: `AntibioticGuidance(infection, first_line, dose_text, duration, penicillin_allergic, delayed_note)`, `ANTIBIOTIC_GUIDANCE: List[AntibioticGuidance]` (12), `antibiotic_for(infection_text, penicillin_allergy=False) -> List[AntibioticGuidance]`, `stewardship_principles() -> List[str]`.

```python
_ROWS = [
    ("sore throat", "Phenoxymethylpenicillin (only FeverPAIN 4-5)",
     "500mg QDS", "5-10 days", "Clarithromycin 250-500mg BD",
     "FeverPAIN 0-1: no antibiotic; 2-3: delayed (3-5d) backup"),
    ("otitis media", "Amoxicillin (systemically very unwell or <2y bilateral)",
     "500mg TDS", "5 days", "Clarithromycin 500mg BD",
     "Most need NO antibiotic or delayed 4-5 days"),
    ("sinusitis", "Phenoxymethylpenicillin",
     "500mg QDS", "5 days", "Doxycycline 200mg then 100mg OD",
     "Only if ≥10 days + worsening after improving (double worsening)"),
    ("lower uti (women)", "Nitrofurantoin MR",
     "100mg BD", "3 days", "Trimethoprim 200mg BD (low resistance risk only)",
     "Back-up prescription reasonable for mild symptoms"),
    ("lower uti (men)", "Trimethoprim or nitrofurantoin",
     "200mg BD / 100mg BD", "7 days", "As first line alternatives",
     "Men always 7 days; consider prostatitis"),
    ("pyelonephritis", "Cefalexin (oral if mild)",
     "500mg BD", "7 days", "Ciprofloxacin 500mg BD (resistance concerns)",
     "Admit if systemically unwell, pregnant, or cannot take oral"),
    ("cellulitis", "Flucloxacillin",
     "500mg QDS (1g if >50kg or severe)", "5-7 days", "Clarithromycin 500mg BD (or doxycycline)",
     "Mark erythema with a pen; review 48h; IV if systemic"),
    ("impetigo", "Topical fusidic acid (localised) / oral flucloxacillin (widespread)",
     "TDS topical / 500mg QDS", "5 days localised / 7 days oral",
     "Topical mupirocin / clarithromycin", "Hygiene measures; exclude from school until lesions crusted"),
    ("dental infection", "Amoxicillin OR metronidazole (dentist still needed)",
     "500mg TDS / 400mg TDS", "3-5 days", "Metronidazole or clindamycin 300mg BD",
     "Antibiotics NEVER replace dental drainage — refer to dentist"),
    ("copd exacerbation", "Amoxicillin (or doxycycline first if sputum purulent per local)",
     "500mg TDS", "5 days", "Doxycycline 200mg then 100mg",
     "Only if increased sputum purulence + more breathless"),
    ("lower respiratory (chest infection)", "Amoxicillin",
     "500mg TDS", "5 days", "Doxycycline or clarithromycin",
     "Most viral; CRP point-of-care where available; pneumonia severity (CURB-65) for admission"),
    ("c. difficile risk", "N/A — avoidance message",
     "", "", "",
     "Cephalosporins, clindamycin, quinolones, and broad cover drive C. difficile "
     "and MRSA — choose the narrowest effective drug, shortest sensible course"),
]

STEWARDSHIP_PRINCIPLES = [
    "Do not start antibiotics without a plausible bacterial diagnosis + documented plan",
    "Record on the prescription: indication, duration, review date",
    "Take cultures BEFORE the first dose where safe (but never delay sepsis treatment)",
    "48-72h review: stop, de-escalate, switch oral, or continue with reason",
    "Shortest effective duration; delayed prescribing for self-limiting illness",
    "Explain the no-antibiotic decision to the patient — safety-net the expected course",
]
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.antimicrobial_stewardship import (
    ANTIBIOTIC_GUIDANCE, antibiotic_for, stewardship_principles,
)


class TestStewardship:
    def test_12_infections(self):
        assert len(ANTIBIOTIC_GUIDANCE) == 12

    def test_sore_throat_feverpain(self):
        hits = antibiotic_for("sore throat score 4")
        assert hits and "FeverPAIN" in (hits[0].first_line + hits[0].delayed_note)

    def test_penicillin_allergy_changes_answer(self):
        plain = antibiotic_for("cellulitis of the leg")
        allergic = antibiotic_for("cellulitis of the leg", penicillin_allergy=True)
        assert plain[0].first_line == "Flucloxacillin"
        assert "Clarithromycin" in allergic[0].penicillin_allergic

    def test_womens_uti_3_days(self):
        hits = antibiotic_for("cystitis symptoms for two days, woman")
        assert any("3 days" in h.duration for h in hits)

    def test_principles_include_review(self):
        assert any("48" in p for p in stewardship_principles())
```

- [x] **Step 2: verify fail.** **Step 3: implement** (match infection keywords: "throat" → sore throat; "otitis"/"ear" → otitis media; "sinus" → sinusitis; "cystitis"/"uti" + "men" → men else women; "pyelonephritis"/"kidney"; "cellulitis"; "impetigo"; "dental"/"tooth"; "copd"; "chest infection"/"lrti"/"pneumonia"; "c. difficile"/"antibiotic risk" → last row). **Step 4: run** (32 total). **Step 5: commit** `feat(uk_practice): antimicrobial stewardship — first-line tables + principles`.

---

### Task 7: prescribing_safety — monitoring + renal flags

**Files:**
- Create: `gpdisc_core.uk_practice/prescribing_safety.py`
- Test: append `class TestPrescribingSafety`

**Interfaces:**
- Produces: `monitoring_requirements(drug: str) -> List[str]`, `MONITORING: Dict[str, List[str]]` (10 drugs), `renal_flags(drug: str, egfr: float) -> List[str]`.

```python
MONITORING = {
    "lithium": [
        "Level 12h post-dose: target 0.4-0.8mmol/L (mania up to 1.0)",
        "U&E + TFT + calcium every 6 months; weight/BP",
        "Acute illness / dehydration / ACE-i / NSAID → toxicity risk: hold + check level",
        "Interactions: NSAIDs, ACEi/ARB, thiazides, D&V — the classic exam stem",
    ],
    "methotrexate": [
        "FBC + LFT baseline, weekly until dose stable 4-6 weeks, then every 2-4w "
        "for 3 months, then 3-monthly",
        "Folic acid 5mg once WEEKLY (not on methotrexate day); NEVER daily dosing",
        "Cough/dyspnoea → stop + chest imaging (pneumonitis)",
        "Sore throat/mouth ulcers/fever → urgent FBC (marrow suppression)",
        "Alcohol ≤ within unit guidance; contraception for both sexes",
    ],
    "warfarin": [
        "INR to target range; more frequent after dose/interaction changes",
        "INR 4-5 no bleeding: reduce/omit dose; >8 no bleeding: hold + vitamin K per protocol",
        "Interactions: antibiotics (esp. macrolides, metronidazole, co-trimoxazole), "
        "amiodarone, NSAIDs, alcohol binge",
    ],
    "doac": [
        "Annual: FBC, U&E, LFT + weight",
        "Renal function drives dosing — recheck annually (or 6-monthly if CKD3+)",
        "No routine coagulation monitoring — but DO NOT assume 'no monitoring'",
    ],
    "digoxin": [
        "U&E + level if toxicity suspected (nausea, visual disturbance, arrhythmia)",
        "Toxicity: hypokalaemia/hypomagnesaemia amplify; check before increasing",
    ],
    "amiodarone": [
        "TFT + LFT every 6 months",
        "Annual chest X-ray (pneumonitis); corneal deposits + photosensitivity counsel",
    ],
    "ace_or_arki": [
        "U&E before start, 1-2 weeks after starting/each dose increase",
        "Acceptable rise: creatinine <30% — beyond that, stop and reconsider",
    ],
    "spironolactone": [
        "U&E at 1 week, 1 month, then 6-monthly",
        "Hyperkalaemia risk with ACEi/ARB — the trilogy of death: ACEi + spironolactone + NSAID",
    ],
    "sodium_valproate": [
        "LFT + FBC baseline and if clinically indicated",
        "Never in women of childbearing potential without pregnancy prevention "
        "programme (neural tube + neurodevelopmental harm)",
    ],
    "clozapine": [
        "Weekly FBC for 18 weeks, then 2-weekly to a year, then monthly for life",
        "Any fever/sore throat → urgent FBC (agranulocytosis) + stop until result",
        "Shared care with mental health; monitoring service registration mandatory",
    ],
}

_RENAL_FLAGS = {
    "metformin": [
        (45.0, "Review dose; eGFR 30-45: halve max 1g/day, avoid starting"),
        (30.0, "STOP metformin — eGFR <30 contraindicated"),
    ],
    "nitrofurantoin": [
        (45.0, "Avoid if eGFR <45 (insufficient urinary concentration; neuropathy risk)"),
        (30.0, "Contraindicated eGFR <30"),
    ],
    "doac": [
        (30.0, "Apixaban can be used with caution ≥15; dabigatran avoid <30 — "
               "check drug-specific threshold"),
    ],
    "nsaid": [
        (60.0, "Avoid in CKD; if unavoidable use lowest dose shortest course + "
               "PPI + review renal function 1-2 weeks"),
    ],
    "ace_or_arki": [
        (30.0, "Specialist advice before continuing/starting ACEi at eGFR <30"),
    ],
}
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements, renal_flags, MONITORING,
)


class TestPrescribingSafety:
    def test_methotrexate_never_daily(self):
        m = monitoring_requirements("methotrexate")
        assert any("NEVER daily" in x or "weekly" in x.lower() for x in m)

    def test_lithium_interactions(self):
        m = monitoring_requirements("lithium")
        assert any("NSAID" in x for x in m)

    def test_unknown_drug_empty(self):
        assert monitoring_requirements("paracetamol") == []

    def test_metformin_egfr_25_stops(self):
        flags = renal_flags("metformin", egfr=25)
        assert any("STOP" in f for f in flags)

    def test_metformin_egfr_50_clean(self):
        assert renal_flags("metformin", egfr=50) == []

    def test_nitrofurantoin_egfr_40_avoid(self):
        flags = renal_flags("nitrofurantoin", egfr=40)
        assert any("45" in f for f in flags)

    def test_ten_drugs_monitored(self):
        assert len(MONITORING) == 10
```

- [x] **Step 2: verify fail.** **Step 3: implement** (`renal_flags` collects every `(threshold, message)` where `egfr < threshold`, message included; drug-name aliasing `ace`, `ramipril`, `enalapril` → `ace_or_arki`, `apixaban|edoxaban|rivaroxaban|dabigatran` → `doac`, `ibuprofen|naproxen` → `nsaid`). **Step 4: run** (39 total). **Step 5: commit** `feat(uk_practice): high-risk prescribing monitoring + renal dose flags`.

---

### Task 8: fit_notes + package exports + regression + docs

**Files:**
- Create: `gpdisc_core/uk_practice/fit_notes.py`
- Modify: `gpdisc_core/uk_practice/__init__.py` (export everything)
- Test: append `class TestFitNotes`; then full battery
- Modify: `CLAUDE.md`; memory update

**Interfaces:**
- Produces: `fit_note_guidance(days_off: int) -> dict`, `ADJUSTMENT_OPTIONS: List[str]`.

```python
ADJUSTMENT_OPTIONS = [
    "Phased return — building up hours over 1-2 weeks",
    "Altered hours",
    "Amended duties",
    "Workplace adaptations (equipment, seating, breaks)",
]

def fit_note_guidance(days_off: int) -> dict:
    if days_off <= 7:
        route = "Self-certification (Statutory Sick Pay first 7 days) — no fit note needed"
        employer = "Employee self-certifies; employer cannot require a GP certificate for ≤7 days"
    elif days_off <= 92:
        route = "GP fit note (Med3) required from day 8"
        employer = "Fit note may advise 'may be fit for work' with adjustments — "
                   "employer and employee discuss feasibility"
    else:
        route = "GP fit note; consider the 'fit for work' conversation + "
                "occupational health referral if off >4 weeks"
        employer = "Long-term sickness: occupational health + phased-return planning; "
                   "DWP may assess ESA after 28 weeks"
    return {"days_off": days_off, "route": route, "employer_guidance": employer,
            "adjustments": ADJUSTMENT_OPTIONS}
```

- [x] **Step 1: failing tests:**

```python
from gpdisc_core.uk_practice.fit_notes import fit_note_guidance, ADJUSTMENT_OPTIONS


class TestFitNotes:
    def test_day_3_self_cert(self):
        g = fit_note_guidance(3)
        assert "Self-certification" in g["route"]

    def test_day_10_needs_med3(self):
        g = fit_note_guidance(10)
        assert "fit note" in g["route"].lower()

    def test_long_term_signposts_oh(self):
        g = fit_note_guidance(120)
        assert "occupational health" in g["employer_guidance"].lower()

    def test_adjustments_listed(self):
        assert "Phased return" in " ".join(ADJUSTMENT_OPTIONS)
```

- [x] **Step 2: verify fail.** **Step 3: implement fit_notes.py + `__init__.py` full exports:**

```python
from .guidelines_index import GuidelineRef, GUIDELINES, lookup_guideline
from .two_week_wait import TwoWeekWaitRule, TWO_WEEK_WAIT_RULES, two_week_wait_check
from .dvla_rules import DrivingRule, DRIVING_RULES, driving_rules
from .capacity_and_safeguarding import (
    capacity_two_stage_test, best_interests_checklist, dnacpr_principles,
    safeguarding_adult_types, safeguarding_children_levels, gillick_checklist,
    capacity_concern_keywords,
)
from .controlled_drugs import (
    controlled_drug_class, prescribing_guardrails, CD_SCHEDULES, CD_SAFE_PRACTICE,
)
from .antimicrobial_stewardship import (
    AntibioticGuidance, ANTIBIOTIC_GUIDANCE, antibiotic_for, stewardship_principles,
)
from .prescribing_safety import monitoring_requirements, renal_flags, MONITORING
from .fit_notes import fit_note_guidance, ADJUSTMENT_OPTIONS
```

- [x] **Step 4: full battery** — `pytest` all 5 suites (clinical 59 + travel 15 + preventive 10 + sexual 14 + uk_practice 43 = 141), comprehensive 26/26, test_all 11/3 baseline, import sweep 0 failures.
- [x] **Step 5: CLAUDE.md** — add "### UK Practice Layer (Stage 3)" section + Testing line.
- [x] **Step 6: Commit** `docs: document Stage 3 uk_practice in CLAUDE.md`; update memory `gpidisc-transition.md`; tick plan checkboxes; commit.

---

## Self-Review (completed)

- **Spec coverage:** Glenn's UK list — NICE/CKS (Task 1), 2ww (Task 2), DVLA (Task 3), MCA/DNACPR/safeguarding (Task 4), controlled drugs (Task 5), antimicrobial stewardship (Task 6), BNF prescribing safety (Task 7), fit notes (Task 8). Vaccination/screening policy already delivered in Stage 2 `preventive_medicine` (documented there) — not duplicated.
- **Placeholders:** none.
- **Type consistency:** dataclass names match between rows and tests across tasks; `two_week_wait_check(text, age=None, sex=None)` signature consistent.
- **Execution corrections to apply:** Task 5 schedule-3 draft noise → clean list as noted; Task 5 codeine answer for `controlled_drug_class("codeine 30mg")` is `""` (only listed preparations are CD5 — plain 30mg tablets are NOT CDs).
