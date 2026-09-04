# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL PRIVACY RULE - GITHUB PUSH FORBIDDEN 🚨

**YOU ARE ABSOLUTELY FORBIDDEN FROM PUSHING ANY CODE, DATA, OR COMMITS TO GLENN'S GITHUB REPOSITORY.**

**This prohibition applies to:**
- ❌ NO `git push` commands of any kind
- ❌ NO automatic or scheduled repository updates
- ❌ NO pushing patient data, even anonymized
- ❌ NO pushing medical records or consultation history
- ❌ NO pushing local memory dumps or knowledge bases
- ❌ NO pushing code changes without explicit instruction

**The ONLY exception:**
- ✅ You MAY push ONLY when given an explicit, direct instruction from Glenn to do so
- ✅ Example: "Please push this commit to GitHub" - ONLY then you may push

**Why this exists:**
- GPDISC handles sensitive patient medical data
- Patient privacy and confidentiality are paramount
- Unauthorized disclosure of medical information is illegal and unethical
- Local-only storage ensures HIPAA/GDPR compliance

**VIOLATION OF THIS RULE IS GROUNDS FOR IMMEDIATE SESSION TERMINATION.**

---

## Project Overview

**GPDISC** (General Practice Discovery and Intelligence System for Consultation) is a private consultation system, refocused on General Practice as the primary discipline, integrating biological knowledge with medical specialties for patient consultation and second opinions. Formerly **MEDIDISC** (Medical Discovery and Intelligence System for Consultation).

**Version**: 1.1.0 (GPDISC transition)
**Focus**: General Practitioner consultation, with specialist referral domains
**Privacy**: All patient records stored locally (no external LLM transmission)

### Transition Status (2026-09-03)

- **All patient records from the MEDIDISC era were purged** from this repository (archived outside the repo, then removed). The `patients/` directory and `gpdisc_core/data/` are empty skeletons awaiting fresh data.
- **The package rename is complete** (2026-09-03): `medidisc_core` → `gpdisc_core`, factory `create_medidisc_system()` → `create_gpdisc_system()`, with all imports, paths, configs, and docs updated. Import via `from gpdisc_core import create_gpdisc_system`.
- **Hallucination audit FIXED** (2026-09-04): the outside-consultant audit (`docs/superpowers/specs/2026-09-03-hallucination-audit.md`) found 23+ errors (legal facts, citations, clinical thresholds, collisions, typos) plus 8 routing gaps and 4 missing areas. ALL are fixed and locked by tests — every correction ships with both-direction probes (the genuine case still detected, the benign near-miss still benign). Key additions: alcohol-interaction table (`prescribing_safety.ALCOHOL_INTERACTIONS`), methotrexate warning-card urgent rule, ST-elevation emergency rule, `advanced_cancer_supportive` corpus entry (corpus now 273), pre-travel/prevention/alcohol-interaction front-door routes, urgent-rule advice now always rendered (never silently replaced by tier text).
- **ASTRA-lineage purge** (2026-09-04): the astronomy-specific code inherited from the ASTRA era was removed from the tracked tree (68 files: astro reasoning modules, ISM/multiwavelength/observational machinery, astro databases and paper library, SPH/stellar/interstellar self-teaching, v100 simulations, relativistic/quantum/nuclear physics, MNRAS-era docs and their tests). The generic BIODISC-era machinery (`reasoning/`, `causal/`, `self_teaching/`, `capabilities/`, `simulation/`, biophysics) is retained as the scientific foundation; `gpdisc_core/README.md` documents the split. Verified after the purge: import sweep 535 modules 0 failures, 24-suite battery 609 passed, comprehensive test green.

### Naming Convention

This system is **GPDISC** - General Practice Discovery and Intelligence System for Consultation.

- **Full name**: GPDISC: General Practice Discovery and Intelligence System for Consultation
- **Internal package**: `gpdisc_core` (renamed from `medidisc_core`, 2026-09-03)
- **Primary function**: `create_gpdisc_system()`
- **Purpose**: Private GP-led medical consultation and second opinions

---

## CRITICAL: Privacy Commitment

**GPDISC is designed for PRIVATE medical consultation**:

- **All patient records stored locally**: No transmission to external LLMs
- **Long-term memory**: Patient records, blood tests, ECGs, MRIs, doctor's notes
- **Second opinion mode**: Medical consultation supporting validation and diagnosis
- **Medical specialties**: Cardiology, Epilepsy, General Practice, Orthopedics, Pharmacology
- **Biology knowledge preserved**: All biological knowledge maintained for scientific foundation

---

## CRITICAL: Persistent Memory Initialization

**IMPORTANT**: At the start of EVERY session, initialize the persistent memory system:

```python
# RUN THIS AT SESSION START
from gpdisc_core.memory.persistent import create_integrator, quick_hallucination_check

integrator = create_integrator()
integrator.initialize_session()
```

### Before Making Any Medical Claim

ALWAYS verify medical claims against the hallucination register:

```python
result = integrator.verify_claim_before_output("medical claim")
if not result.safe:
    # Use the correct value instead
    correct = result.hallucination_match.correct_value
```

---

## Quick Start

### Basic Medical Consultation

```python
from gpdisc_core import create_gpdisc_system

# Create medical consultation system
system = create_gpdisc_system()

# Medical consultation with automatic specialty selection
result = system.answer("I'm experiencing chest pain, what should I do?")
print(result['answer'])
```

### Direct Medical Domain Usage

```python
# Cardiology consultation
from gpdisc_core.domains.cardiology import CardiologyDomain
cardio = CardiologyDomain()
result = cardio.process_query("Interpret this ECG: ST elevation in V1-V4")
print(result['answer'])
print(f"Confidence: {result.confidence}")

# Epilepsy consultation
from gpdisc_core.domains.epilepsy import EpilepsyDomain
epilepsy = EpilepsyDomain()
result = epilepsy.process_query("Patient had a seizure with aura")
print(result['answer'])

# General Practice consultation
from gpdisc_core.domains.general_practice import GeneralPracticeDomain
gp = GeneralPracticeDomain()
result = gp.process_query("I need a referral to a specialist")
print(result['answer'])

# Orthopedics consultation
from gpdisc_core.domains.orthopedics import OrthopedicsDomain
ortho = OrthopedicsDomain()
result = ortho.process_query("Knee injury from sports")
print(result['answer'])

# Pharmacology consultation
from gpdisc_core.domains.pharmacology import PharmacologyDomain
pharma = PharmacologyDomain()
result = pharma.process_query("Can I take ibuprofen with aspirin?")
print(result['answer'])
```

---

## Medical Specialties

### Domain structure (honest map)

`gpdisc_core/domains/` holds 44 domain packages, in three tiers:

- **5 primary medical domains (UK-framed)** — Cardiology, Epilepsy, General Practice, Orthopedics, Pharmacology. These are the supported direct-entry specialties.
- **29 legacy specialty domains (US-framed)** — emergency_medicine, dermatology, pediatrics, neurology, and the rest inherited from the MEDIDISC era. Their content is individually correct **in a US frame** (Beers criteria, FDA labels, ASCVD ≥7.5%, mg/dL units, acetaminophen/meperidine naming, PDMP) inside a UK-first system — a mismatch flagged by the 2026-09-03 audit. **Prefer the clinical-reasoning front door** (`create_gpdisc_system()` / `ConsultationPipeline`), which is UK-grounded and safety-screened; the legacy domains remain as background knowledge, not as consultation entry points.
- **10 biology domains (preserved)** — the scientific foundation, unchanged.

The consultation pathway a query should take is the front door, NOT a direct legacy-domain `process_query()`.

### The five primary specialties

### Cardiology
- ECG/EKG interpretation
- Chest pain evaluation and cardiac risk assessment
- Blood pressure and hypertension management
- Heart failure management
- Arrhythmia evaluation (atrial fibrillation, etc.)
- Cardiac imaging interpretation (echocardiogram, stress test, angiogram)
- Cardiovascular risk assessment and medication management

### Epilepsy
- Seizure classification and diagnosis
- EEG interpretation and seizure semiology
- Antiepileptic medication management
- Seizure first aid and safety protocols
- Epilepsy syndrome recognition
- Treatment-resistant epilepsy evaluation
- Pre-surgical evaluation considerations

### General Practice
- Triage and urgent care assessment
- Symptom evaluation and differential diagnosis
- Preventive care and health screening
- Chronic disease management (diabetes, hypertension, COPD, asthma)
- Medication reconciliation and deprescribing
- Mental health consultation (depression, anxiety)
- Health promotion and lifestyle medicine
- Specialist referral guidance

### Orthopedics
- Fracture assessment and management
- Joint pain evaluation (hip, knee, shoulder, spine)
- Sports injuries and soft tissue injuries
- Arthritis management (osteoarthritis, inflammatory arthritis)
- Back pain and spinal conditions
- Bone health and osteoporosis management
- Orthopedic surgery consultation

### Pharmacology
- Drug interaction checking
- Side effect evaluation and management
- Medication dosing and adjustment
- Polypharmacy review and optimization
- Prescription consultation
- Adverse drug reaction assessment
- Medication safety in special populations
- Therapeutic drug monitoring

---

## Preserved Biology Knowledge

The system maintains all biological knowledge domains for scientific foundation:

- **Molecular Biology**: DNA replication, transcription, translation
- **Biochemistry**: Metabolic pathways, enzyme kinetics
- **Genetics**: Heredity, variation, mutations
- **Cell Biology**: Cell structure, organelles, division
- **Biophysics**: Physical principles in biological systems
- **Bioinformatics**: Sequence analysis, structural biology
- **Computational Biology**: Biological modeling
- **Genomics**: Genome analysis
- **Proteomics**: Protein structure and function
- **Systems Biology**: Integrated biological networks

---

## Testing

### Comprehensive System Test

```bash
# Run comprehensive GPDISC system test
python gpdisc_core/comprehensive_system_test.py
```

### Clinical Reasoning Core

```bash
# Run clinical reasoning core tests (59 tests: corpus, safety, differential, consultation, syndromes)
python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v
```

### Stage 2 Suites (travel / prevention / sexual health)

```bash
python3 -m pytest gpdisc_core/tests/test_travel_medicine.py gpdisc_core/tests/test_preventive_medicine.py gpdisc_core/tests/test_sexual_health.py -v
```

### Stage 3 Suite (UK practice)

```bash
python3 -m pytest gpdisc_core/tests/test_uk_practice.py -v
```

### Stage 4 Suite (MDT + multimorbidity)

```bash
python3 -m pytest gpdisc_core/tests/test_mdt.py -v
```

### Stage 5 Suites (doctor craft + discrimination + regression bank)

```bash
# Consultation skills, benign-vs-emergency pairs, regression bank (now 75 rows)
python3 -m pytest gpdisc_core/tests/test_consultation_skills.py gpdisc_core/tests/test_benign_vs_emergency.py gpdisc_core/tests/test_regression_bank.py -v

# Validation layer + audit probes (anti-hallucination + marginal cases)
python3 -m pytest gpdisc_core/tests/test_validation.py gpdisc_core/tests/test_audit_probes.py -v

# Emergency breadth + post-exposure (Stage 6)
python3 -m pytest gpdisc_core/tests/test_emergency_breadth.py gpdisc_core/tests/test_post_exposure.py -v

# Daily breadth + front door + palliative care (Stage 7)
python3 -m pytest gpdisc_core/tests/test_breadth2.py gpdisc_core/tests/test_front_door.py gpdisc_core/tests/test_palliative_care.py -v

# The world: global corpus + resource settings + jurisdictions + humanitarian care (Stage 8)
python3 -m pytest gpdisc_core/tests/test_global.py gpdisc_core/tests/test_resource_settings.py gpdisc_core/tests/test_jurisdictions.py gpdisc_core/tests/test_humanitarian_care.py -v

# Consultant opinions + interpretation breadth (Stage 9)
python3 -m pytest gpdisc_core/tests/test_mdt_consultants.py gpdisc_core/tests/test_interpretation_breadth.py -v

# Routing gaps (hallucination-audit section D: the 8 presentations that
# once reached no specialist pathway, locked with their over-triage guards)
python3 -m pytest gpdisc_core/tests/test_routing_gaps.py -v

# Full battery (24 suites, 609 tests)
python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py gpdisc_core/tests/test_travel_medicine.py gpdisc_core/tests/test_sexual_health.py gpdisc_core/tests/test_preventive_medicine.py gpdisc_core/tests/test_pharmacology_safety.py gpdisc_core/tests/test_uk_practice.py gpdisc_core/tests/test_mdt.py gpdisc_core/tests/test_mdt_consultants.py gpdisc_core/tests/test_consultation_skills.py gpdisc_core/tests/test_benign_vs_emergency.py gpdisc_core/tests/test_regression_bank.py gpdisc_core/tests/test_validation.py gpdisc_core/tests/test_audit_probes.py gpdisc_core/tests/test_emergency_breadth.py gpdisc_core/tests/test_post_exposure.py gpdisc_core/tests/test_breadth2.py gpdisc_core/tests/test_front_door.py gpdisc_core/tests/test_palliative_care.py gpdisc_core/tests/test_global.py gpdisc_core/tests/test_resource_settings.py gpdisc_core/tests/test_jurisdictions.py gpdisc_core/tests/test_humanitarian_care.py gpdisc_core/tests/test_interpretation_breadth.py gpdisc_core/tests/test_routing_gaps.py -q
```

### Medical Domain Tests

```bash
# Test cardiology
python -c "
from gpdisc_core.domains.cardiology import CardiologyDomain
cardio = CardiologyDomain()
result = cardio.process_query('ECG showing ST elevation')
print(result['answer'])
"

# Test all medical domains
python -c "
from gpdisc_core.domains.cardiology import CardiologyDomain
from gpdisc_core.domains.epilepsy import EpilepsyDomain
from gpdisc_core.domains.general_practice import GeneralPracticeDomain
from gpdisc_core.domains.orthopedics import OrthopedicsDomain
from gpdisc_core.domains.pharmacology import PharmacologyDomain

for domain_class in [CardiologyDomain, EpilepsyDomain, GeneralPracticeDomain, OrthopedicsDomain, PharmacologyDomain]:
    domain = domain_class()
    result = domain.process_query('test query')
    print(f'{domain_class.__name__}: {result.confidence}')
"
```

### Integration Tests

```bash
# Test system integration
python -c "
from gpdisc_core import create_gpdisc_system
system = create_gpdisc_system()

# Test medical consultation
result = system.answer('What does this ECG show?')
print(result['answer'])

# Test second opinion generation
result = system.answer('I need a second opinion on this diagnosis')
print(result['answer'])
"
```

---

## Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Entry Points                                 │
│  create_gpdisc_system() | process_query()                     │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│      Primary Medical Domains (5, UK-framed)                     │
│  Cardiology | Epilepsy | General Practice | Orthopedics | Pharmacology │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│   Legacy Specialty Domains (29, US-framed — prefer front door)  │
│  Emergency Medicine | Dermatology | Paediatrics | Neurology ... │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│              Biology Domains (10) - Preserved                   │
│  Molecular Biology | Biochemistry | Genetics | Cell Biology      │
│  Biophysics | Bioinformatics | Computational Biology            │
│  Genomics | Proteomics | Systems Biology                       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                Advanced Capabilities                            │
│  Causal Reasoning | Meta-Learning | Swarm Intelligence          │
│  Meta-Context Engine | Counterfactual Analysis                 │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│           Clinical Reasoning Core (GP-led front door)           │
│  Safety Screen | Differential Engine | Consultation Pipeline     │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   Memory & Privacy Systems                       │
│  Persistent Memory | Anti-Hallucination | Local Storage          │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   Dashboard (Port 8790)                           │
│  Medical Consultation Interface | Private & Local               │
└─────────────────────────────────────────────────────────────────┘
```

### Clinical Reasoning Core (GP-led front door)

`gpdisc_core/clinical_reasoning/` — Level 1 + Level 6 of the GP expertise architecture: structured condition corpus (273 conditions across 20+ categories, Parts 1-6: core, breadth, emergencies, chronic/daily breadth, global burden), Bayesian test interpretation, safety/escalation layer with emergency and urgent overlays, differential engine with anti-anchoring, and the consultation pipeline. `answer()` routes every medical query through safety screening first; emergency patterns are never downgraded by benign reasoning. Uncertainty ("I don't know yet") is a first-class output, and unpopulated consultation stages become questions to ask. Routine-intent presentations route to their specialist modules after the safety screen: pre-travel questions to `travel_medicine`, "what am I due" prevention questions to `preventive_medicine`, alcohol-plus-medication questions to the `prescribing_safety.ALCOHOL_INTERACTIONS` table, end-of-life presentations to `palliative_care` — safety always wins, so each route fires only when no emergency/urgent rule did.

```python
from gpdisc_core.clinical_reasoning import ConsultationPipeline

pipe = ConsultationPipeline()
rec = pipe.run("66 year old man, chest pain for 40 minutes, sweating", {})
print(rec.summary())       # ranked differential, must-not-miss, safety net
print(rec.escalation)      # emergency | urgent | routine | self_care
```

### Tropical / Travel / Preventive / Sexual Health (Stage 2)

`gpdisc_core/clinical_reasoning/syndromes.py` — five syndrome frames (fever after travel, eosinophilia in a traveller, fever + thrombocytopenia, fever + jaundice, fever + rash) with discriminating questions; attached to every consultation that matches. `gpdisc_core/travel_medicine/` — 24-destination risk table, chemoprophylaxis rules (traveller-history aware), pre-travel consult and post-travel screening. `gpdisc_core/preventive_medicine/` — UK vaccination and screening tables + CVD prevention thresholds. `gpdisc_core/sexual_health/` — UKMEC eligibility, STI panels, emergency contraception rules.

```python
from gpdisc_core.travel_medicine import pre_travel_consult, post_travel_screening
from gpdisc_core.preventive_medicine import prevention_check
from gpdisc_core.sexual_health import ukmec_category

plan = pre_travel_consult("two weeks in Ghana", {"age_years": 40})
due = prevention_check({"age_years": 68, "sex": "m"})       # bowel FIT, AAA, shingles...
cat, why = ukmec_category("cocp", "migraine_with_aura")      # (4, "Stroke risk...")
```

### UK Practice Layer (Stage 3)

`gpdisc_core/uk_practice/` — the UK-specific regulatory and policy layer: NICE/CKS guideline index (26 areas), 2ww urgent-suspected-cancer criteria (16 NG12-aligned rules with age/sex gating), DVLA fitness-to-drive rules (14 conditions, group 1 + 2), MCA two-stage capacity test + best-interests + DNACPR + safeguarding frameworks, controlled-drug schedules with prescribing guardrails, antimicrobial stewardship (first-line tables with penicillin-allergic alternatives and delayed-prescribing notes), high-risk drug monitoring (lithium, methotrexate, clozapine, DOACs...) with eGFR renal flags, an alcohol-interaction table (metronidazole AVOID 48h post-dose incl. alcohol-containing mouthwash; warfarin INR caution; honest "no row" for unknown drugs), and fit-note (Med3) rules. Vaccination/screening cohorts live in `preventive_medicine` (Stage 2).

```python
from gpdisc_core.uk_practice import (
    two_week_wait_check, driving_rules, antibiotic_for,
    monitoring_requirements, renal_flags, fit_note_guidance,
)

hits = two_week_wait_check("difficulty swallowing", age=58)    # oesophago_gastric 2ww
rules = driving_rules("first seizure", group=1)                # 6 months off driving
abx = antibiotic_for("cellulitis", penicillin_allergy=True)    # clarithromycin path
flags = renal_flags("metformin", egfr=25)                      # STOP metformin
mon = monitoring_requirements("methotrexate")                  # FBC/LFT schedule
fit = fit_note_guidance(3)                                     # self-certification
```

### MDT + Multimorbidity (Stage 4)

`gpdisc_core/mdt/` — the multi-agent consultation team. `challenger.py` attacks every leading differential (dangerous mimics neither ranked nor retained, anchor bias when the runner-up is close, unasked discriminating features, rare-leader prevalence challenges); `roles.py` gives six computed perspectives (GP chair, geriatrician, clinical pharmacologist, safeguarding practitioner, mental health, patient advocate) drawing on the Stage 1-3 packages; `debate.py` runs the full protocol — pipeline → challenges → role notes → chair's synthesis that states "I don't know yet" when that is the honest position, with disagreement recorded, never smoothed away. `multimorbidity.py` is the whole-patient reasoner: medication renal/monitoring flags, anticholinergic burden (ACB), ten treatment-tension pairs (CKD×OA, diabetes×MCI, AF×falls...), drug-cause checklists for dizziness/confusion, and priorities ordered by what can harm fastest — built around the canonical 79-year-old with CKD, diabetes, heart failure, OA, MCI and eight medications.

```python
from gpdisc_core.mdt import run_mdt, whole_patient_review

r = run_mdt("66 year old man, chest pain 40 minutes, sweating")   # synthesis + challenges + actions
review = whole_patient_review({
    "age_years": 79, "egfr": 28,
    "conditions": ["chronic_kidney_disease", "type_2_diabetes", "heart_failure",
                   "osteoarthritis", "cognitive_impairment", "hypertension"],
    "medications": ["metformin", "ramipril", "furosemide", "bisoprolol",
                    "amitriptyline", "gliclazide", "paracetamol", "omeprazole"],
    "symptoms": ["dizziness", "confusion"]})   # STOP metformin flag, ACB ≥4, CKD×OA + DM×MCI tensions
```

### Consultation Skills + Discrimination + Regression Bank (Stage 5)

`gpdisc_core/consultation_skills/` — the doctor craft Glenn weighted most heavily: ICE questions (tailored for cancer worries, tiredness, pain), consultation chunking rules, SPIKES for breaking bad news, the safety-net formula (what to expect / what changes my mind / timescale), six difficult-consultation kinds (angry patient, reassurance seeker, bringer of lists, silent patient, internet researcher, denier), uncertainty scripts that make "I don't know yet" an explicit, defensible answer, and four consultation models (Calgary-Cambridge, Balint, Neighbour, Pendleton).

`gpdisc_core/clinical_reasoning/benign_vs_emergency.py` — ten discrimination pairs (tension/SAH, MSK chest pain/ACS, vasovagal/cardiac syncope, gastroenteritis/mesenteric ischaemia, panic/PE, reactive nodes/lymphoma, mechanical back pain/cauda equina, BPPV/stroke, viral rash/meningococcal, glandular fever/epiglottitis). Each pair runs against the live SafetyLayer in tests — the discrimination is verified behaviour, not prose. Exported from `gpdisc_core.clinical_reasoning` (`find_pairs("chest pain")`).

`gpdisc_core/tests/regression_bank.py` — 40 locked presentations (14 emergencies, 10 urgent, 12 routine/benign, 4 syndrome-specific) with pinned escalation, leader/must-not-miss condition, and syndrome frame. Every row runs through the live `ConsultationPipeline`. This bank is the program's graduation exam: change the engine, all 40 must still hold. Authoring it caught seven genuine detection gaps (PE word orders, DKA breathing phrasing, curtain word order, "no drooling" negation, travel-phrase coverage, fever frame without a fever, "no weight loss" negation) — each fixed in the engine, never by weakening a row.

```python
from gpdisc_core.consultation_skills import ice_questions, safety_net_formula, uncertainty_scripts
from gpdisc_core.clinical_reasoning import find_pairs

ice_questions("I'm tired all the time, I'm worried it's cancer")   # tailored ideas/concerns/expectations
safety_net_formula("viral illness, 3-5 days", "rash that doesn't fade, drowsiness", "48h")
for p in find_pairs("worst headache of my life"):
    print(p.discriminators)   # speed of onset, vomiting, neck stiffness...
```

### Emergency Breadth + Post-Exposure (Stage 6 — "nobody dies of nothing")

`gpdisc_core/clinical_reasoning/knowledge_emergencies.py` — the Tier-1 emergencies corpus (CONDITIONS_PART4, 52 entries; total corpus 202): trauma & burns (14: TBI, penetrating torso, haemorrhagic shock, major burns, spinal injury, crush, tetanus-prone wound...), toxicology & withdrawal (13: paracetamol staggered, opioid, carbon monoxide, organophosphate, snake envenomation, serotonin syndrome, alcohol withdrawal delirium...), obstetric emergencies (9: eclampsia, PPH, shoulder dystocia, cord prolapse, obstructed labour, puerperal sepsis...), oncology-supportive + derm emergencies (7: neutropenic sepsis, malignant cord compression, SVCO, SJS/TEN, eczema herpeticum, necrotising fasciitis, erythroderma), paediatric protection (7: NAI — the corpus's first `safeguarding` category — Kawasaki, IgA vasculitis/HSP, febrile convulsion, neonatal jaundice, neonatal sepsis, slapped cheek), and post-exposure risk (2). Twenty-plus emergency/urgent safety rules with a zero-collateral standard: every new rule is swept against all bank rows and benign-pair sides before commit. Substring discipline is enforced by guard tests — bare `band` once matched "husband", bare `bat` sits inside "combat".

`gpdisc_core/post_exposure/` — time-boxed prophylaxis decisions. `rabies_pep()` classifies WHO category I/II/III (negation-aware: "no scratch" after a lick is I, not II), treats any bat anywhere as category III, defers observable UK pets to 10-day observation, and states "never too late until symptoms". `bloodborne_exposure()` handles needlestick/splash/sexual exposures: HIV PEP inside 72h (first dose before the story is complete), HBIG inside ~48h for HBsAg-positive sources, honest framing for undetectable-HIV sources, an HCV test plan (no PEP exists). `pep_screen()` routes a presentation to its pathway.

```python
from gpdisc_core.post_exposure import rabies_pep, bloodborne_exposure, pep_screen

a = rabies_pep("bitten by a dog in Bali two days ago, broke the skin", {})
assert (a.exposure_category, a.needs_pep, a.rig_needed) == ("III", True, True)
b = bloodborne_exposure("needlestick, source hepatitis B positive, 2 hours ago", {})
assert b.hbv_pep   # HBIG + vaccine, ideally <48h
```

Tests: `test_emergency_breadth.py` (52 — every class carries its over-triage guards: minor finger burns, mobile-toddler shin bruises, plain cellulitis, three-day fevers and short recovered fits must NOT escalate), `test_post_exposure.py` (19). Regression bank grew 40 → 62 rows.

### Daily Breadth + Palliative Care (Stage 7 — "the clinic you actually see")

`gpdisc_core/clinical_reasoning/knowledge_breadth2.py` — CONDITIONS_PART5 (44 conditions; total corpus 246): the chronic and bread-and-butter presentations a real clinic holds. Chronic neurology + mental health (7.1, 13: dementia + reversible causes, first seizure adult, Parkinson's, MS, cluster headache, peripheral neuropathy, bipolar mania, OCD, PTSD, EUPD, bulimia, perinatal mental health), dermatology + women's/men's health (7.2, 16: acne, chronic urticaria, scabies, tinea, drug eruption, venous leg ulcer, seborrhoeic dermatitis, menopause/perimenopause, subfertility, PCOS, dysmenorrhoea, ED, BPH, testicular cancer 2ww, prostatitis), and chronic GI/hepato-renal + eyes/ENT + sleep/pain (7.3, 15: constipation, Crohn's, UC, coeliac, decompensated cirrhosis, advanced CKD, inguinal hernia, wet AMD, sudden sensorineural hearing loss, orbital cellulitis, OSA, insomnia, chronic primary pain, neuropathic pain, stress incontinence). Every cohort ships with its over-triage guards — tiredness is not CKD, viral diarrhoea is not UC, snoring without sleepiness is not OSA, migraine zigzags are not AMD — and two pre-existing engine bugs were caught by probes while building it (bare `stab\w*` once 999'd "stabbing pain"; a bare "for months" token once led every chronic complaint with dementia).

`gpdisc_core/palliative_care/` — end-of-life care as a first-class module (7.4). Five terminal symptom frames (pain, agitation, respiratory secretions, nausea, breathlessness), each: assess-before-treating, non-drug care measures first, then PCF-standard subcutaneous dose scaffolding — morphine oral:SC 2:1 with the breakthrough-one-sixth rule, midazolam, hyoscine/glycopyrronium given early, haloperidol by cause — every drug section carrying the standing instruction to confirm against the LOCAL formulary. `cant_swallow_route_advice()` answers the moment tablets can no longer be swallowed (12-drug route table; unknown drugs get "ask the specialist", never a guessed ratio). `end_of_life_plan()` carries the anticipatory ("just in case") medications, capacity/DNACPR/place-of-death decisions, SPIKES cross-referenced from `consultation_skills`, and the warning that an expected death at home is not a 999 call. The front door routes every `_EOL_INTENT` presentation here — but only when no emergency rule fired, so a dying patient who develops a massive bleed still gets 999 first.

```python
from gpdisc_core.palliative_care import eol_guidance_for, cant_swallow_route_advice

g = eol_guidance_for("my mother is dying, in pain, she can't swallow tablets")
assert g["key"] == "pain" and g["cant_swallow"]
a = cant_swallow_route_advice("morphine")   # SC route, oral:SC = 2:1, confirm locally
```

Tests: `test_breadth2.py` (PART5 cohorts + guards), `test_front_door.py` (the answer IS the consultation; honesty locks), `test_palliative_care.py` (18). Regression bank grew 62 → 71 rows.

### The World (Stage 8 — Tier 3 global: any patient, anywhere)

`gpdisc_core/clinical_reasoning/knowledge_global.py` — CONDITIONS_PART6 (26 conditions; total corpus 272): the burden a UK-first corpus never sees. Chronic viral cohorts (hepatitis B/C, undiagnosed HIV), symptomatic rabies (emergency — the vaccine history decides), neglected tropical diseases (leprosy with its numb pale patches, neurocysticercosis, Chagas, sleeping sickness, cutaneous/visceral leishmaniasis), zoonotics (brucellosis, melioidosis, Q fever), eight environmental extremes (heat exhaustion vs heat stroke, hypothermia, AMS with HACE/HAPE runners-up, decompression illness, radiation), sickle vaso-occlusive crisis, acute rheumatic fever with migratory joint pain, FGM care needs, torture survivor care. The substring-discipline lessons of earlier stages compound here and are locked structurally by `test_geography_tokens_never_carry_alone`: endemic-area tokens cap at 0.55 specificity so "worked in India for years" is not malaria; altitude ataxia phrases are bound to altitude/camp words so a pub stumble is not HACE; "holiday in" is bound to malaria-belt destinations so the Alps stays benign.

`gpdisc_core/resource_settings/` — the same patient, four resource worlds. `SETTINGS`: UK general practice (default, has ambulance), remote rural clinic, humanitarian field, offshore vessel. `disposition_guidance(level, setting)` gives the action/transport/alongside line per level×setting; the pipeline appends it in `_finalize` — the differential and level of concern are IDENTICAL everywhere (locked by `test_differential_identical_across_settings` and a parametrised never-lower-concern invariant), only the disposition adapts: "No 999 here: stabilise NOW".

`gpdisc_core/jurisdictions/` — whose rules this consultation ran under. UK is grounded (999, NICE basis, MCA 2005 + Gillick); AU/US/IN carry correct emergency numbers with an honest not-yet-loaded caveat for national law; an unknown country resolves to WHO-neutral with "verify national law" — nothing is fabricated. Every record states its ruleset (`record.ruleset`, rendered in `summary()`), and `uk_practice.JURISDICTION = "UK"` tags the UK-specific outputs (2ww, DVLA, Med3, CD schedules) as non-transferable outside the UK.

`gpdisc_core/humanitarian_care/` — the refugee/asylum consultation layer. `arrival_health_screen()` is the evidence-based minimal bundle sequenced trauma-informed (TB screen highest-yield, baseline bloods, malaria TODAY if febrile after endemic transit, immunisation RESTART on the WHO no-records principle, medico-legal verbatim from day one) with a do-NOT list of equal weight; `interpreter_principles()` carries the never-family/never-children rules with the dialect check ("which language they dream in"); `unaccompanied_minor_review()` frames age assessment as NOT a medical act with nine trafficking indicators and the same-day social-services duty. The front door routes ROUTINE arrival presentations here — but safety always wins: an asylum seeker with chest pain is ACS first, and a torture disclosure stays with the corpus entry.

```python
from gpdisc_core.resource_settings import disposition_guidance
from gpdisc_core.jurisdictions import jurisdiction_for
from gpdisc_core.humanitarian_care import arrival_health_screen

d = disposition_guidance("emergency", "remote_rural_clinic")  # stabilise NOW, no 999
j = jurisdiction_for({"country": "kenya"})    # WHO-neutral, verify caveat
s = arrival_health_screen()                   # TB first, interpreter always
```

Tests: `test_global.py` (38), `test_resource_settings.py` (19), `test_jurisdictions.py` (14), `test_humanitarian_care.py` (17). Regression bank grew 71 → 75 rows.

### Consultant Opinions + Interpretation Breadth (Stage 9 — Tier 4: the specialist on the telephone)

`gpdisc_core/mdt/roles.py` — six consultant roles join the MDT (registry 6 → 12): cardiologist, neurologist, oncologist, paediatrician, psychiatrist, palliative physician. **A consultant speaks ONLY when their domain is implicated, and only from GENUINE contenders** — a ranked entry must score ≥ 0.5× the leader (the validator's contender gate); the retained dangerous-mimic tail counts only on the emergency short-circuit path. Notes are corpus-driven (discriminators and investigations from the ConditionProfile in play) plus craft: the trace before the troponin; onset speed as half the neuro differential; 2ww referral thresholds and the oncological emergencies; weight-based everything; risk in structure (means/plan/intent — command hallucinations count) and delirium-before-label; the reversibility check and anticipatory prescribing. Locked by the contender-gate test: the heart-failure differential's noise tail (HSP, GBS, neutropenic sepsis) triggers no one — only the cardiologist speaks. The 9.1 probes also found and fixed a corpus gap: "on exertion / relieved by rest" — the stable-angina discriminators — previously extracted as nothing, so a months-long exertional story led with STEMI; exertional-months now leads stable angina at routine.

`gpdisc_core/interpretation/` — seven pattern-readers for the tests whose one-line answers steer whole pathways: **ECG** (territories map leads→artery and co-report; inferior gets the right-sided-lead action; posterior MI caught on its mirror-image ST depression; treat-first order hyperkalaemia→digoxin→VT→AF→conduction; normal ECG with chest pain is serial troponins, not discharge), **ABG** (disorder→cause→compensation→severity with Winter's in correct units, lactate ≥4 emergency, hypoxia outranks acid-base), **CSF** (cells→glucose-vs-serum→protein, xanthochromia, Gram stain overrides, the partially-treated picture), and **bedside fluids**: urine dip (glomerular blood+protein → nephrology), spirometry (obstruction/restriction/reversibility), synovial fluid (three-fluid rule; the crystal does not exclude infection), culture logic (double skin flora = contaminant; S. aureus in blood is never a contaminant; asymptomatic bacteriuria is not an infection).

```python
from gpdisc_core.mdt import run_mdt
from gpdisc_core.interpretation import interpret_ecg, interpret_abg

r = run_mdt("58 year old, difficulty swallowing, losing weight", {})
# oncologist speaking: "2ww (oesophago_gastric): Dysphagia at ANY adult age..."
ecg = interpret_ecg("ST elevation in II, III, aVF")   # emergency + V4R action
gas = interpret_abg(7.28, 3.4, 12, lactate=2.0)        # metabolic, Winter's-appropriate
```

Tests: `test_mdt_consultants.py` (23), `test_interpretation_breadth.py` (53). Battery 24 suites / 609 tests (with `test_routing_gaps.py`); import sweep 580 modules clean.

### Consultant Audit + Validation Layer (2026-09-03)

The outside-consultant audit (`docs/superpowers/specs/2026-09-03-consultant-audit.md`) probed 16 marginal presentations empirically — the ACS with no chest-pain words, the ectopic with a coil in place, the elderly mother who "just went quiet" — and found the cracks. All 16 are now locked as `gpdisc_core/tests/test_audit_probes.py` so those exact patients can never fall through again.

`gpdisc_core/clinical_reasoning/validation.py` — **the prospective anti-hallucination layer**, answering "how does anyone know this system won't hallucinate a diagnosis". Two verification levels, both running automatically inside `ConsultationPipeline` (every exit path, report rendered in `summary()`):

- **Consult-level consistency** (`validate_consultation`): the record must agree with itself — an emergency-tier condition ranking as a genuine contender (≥ 0.5× the leader's score — a noise match on one generic word does not count) floors the stated escalation; a retained must-not-miss condition dropped without a word of exclusion is flagged; a non-emergency disposition without a safety net is flagged; safeguarding signals in the presenting complaint are surfaced. **Corrections only ever RAISE the level of concern.**
- **Claim-level grounding** (`verify_claim`): free-text clinical assertions must trace to the knowledge base — renal/dosing claims against the prescribing-safety tables (`renal_flags`), monitoring claims against `monitoring_requirements`, guideline citations against the guideline index (invented NG/CS numbers are the classic citation hallucination) — or be corrected from the persistent local register at `gpdisc_core/data/memory/clinical_hallucination_register.json`.

```python
from gpdisc_core.clinical_reasoning import ClinicalValidator

validator = ClinicalValidator()
rec = pipe.run("72 year old, dizzy on standing since new tablet", {})
print(rec.validation.summary())            # rides on every consultation record

report = validator.verify_claim("metformin is safe at egfr 20")
assert not report.passed                   # blocked, with the truth attached

validator.record_hallucination("claim", "correct value", "source")  # persists locally
```

### Hallucination Audit — FIXED (2026-09-04)

The second outside-consultant audit (`docs/superpowers/specs/2026-09-03-hallucination-audit.md`) went document-by-document through the knowledge base and found 23+ errors (wrong NICE numbers, wrong DVLA/controlled-drug facts, wrong preventive-medicine schedules, substring collisions that over-triaged, typos in clinical strings), 8 routing gaps (presentations that reached no specialist pathway) and 4 missing areas. **All fixed, every fix locked both directions** — the genuine case still detected, the benign near-miss still benign:

- **Legal/factual**: DVLA group-2 post-stroke 1 year, elective PCI group-1 1 week, unexplained syncope 6 months; midazolam/tramadol Schedule 3, diamorphine Schedule 2, temazepam Schedule 4; pyelonephritis NG111 (not NG109); Sri Lanka correctly malaria-free; bowel screening 50-74; shingles vaccine at 65 (phasing to 60, catch-up 70-79).
- **New mechanisms**: `ALCOHOL_INTERACTIONS` table + `alcohol_interaction()`; `methotrexate_warning_signs` paired urgent rule (fever/sore throat/ulcers ON methotrexate → STOP + same-day FBC; routine MTX blood checks stay routine); `st_elevation_ecg` emergency rule with negation guard ("no ST elevation" never 999s); word-number overdose rule ("swallowed twenty" is emergency, "two" stays routine); urgent-rule advice now always rendered on the referral line, never silently replaced by tier text.
- **Corpus**: `advanced_cancer_supportive` (PART5, corpus 273); `alcohol_dependence` enriched with heavy-drinking patterns ("bottle of wine every night"), PabQ paracetamol question, thiamine-before-glucose; hypoactive-delirium tokens ("gone quiet", "not herself today"); meth tokens end-anchored so "on methotrexate" is never "on meth".
- **Locks**: `test_routing_gaps.py` (21 tests) for the 8 gaps + over-triage guards; corrected pins in the affected suites; validator `_check_citation` now catches wrong-topic citations (existing NG number, wrong guideline), not just invented ones.

Marginal presentations now ask rather than shrug: a close top-2 differential emits its conditions' discriminators, and any benign-vs-emergency pair match emits the pair's discriminating questions (`Ask next:` in the summary).

### User Manual + How-To-Use Guide (2026-09-03)

`User_manual/` holds the two reader-facing PDFs and the toolchain that keeps them honest:

- **`GPDISC_User_Manual.pdf`** — purpose, how to use GPDISC (natural language only — no CLI content), compact coverage of every specialism, and 20 worked examples (question + real answer).
- **`GPDISC_How_To_Use.pdf`** — the plain-English practical guide: how to ask well, how to read the reply, 30 worked examples, hard 15-page cap.

**The honesty standard (do not break when regenerating):** every example response in both PDFs is a REAL output captured from the live system via `User_manual/capture.py` — verbatim, or trimmed at a sentence/line boundary for page budget with a trailing `...`. Never reworded, reordered, or fabricated. The `queries_*.json` / `outputs_*.json` pairs in the directory are the evidence trail; a rebuilt PDF is verified by whitespace-normalised prefix-matching every answer against `pdftotext` extraction.

```bash
# Capture real answers for a document's examples (any cwd)
python3 User_manual/capture.py User_manual/queries_manual.json User_manual/outputs_manual.json

# Render (A4, shared styling)
pandoc User_manual/GPDISC_User_Manual.md -o User_manual/GPDISC_User_Manual.pdf \
  --pdf-engine=xelatex --include-in-header=User_manual/preamble.tex \
  -V papersize=a4 -V geometry:margin=2.2cm -V fontsize=10pt -V colorlinks=true --toc --toc-depth=2
```

`capture.py` maps non-ASCII glyphs to ASCII (the repo PDF convention — no unicode boxes in print) but never edits wording; `preamble.tex` is the shared pandoc/xelatex styling smoke-tested against verbatim consultation records.

### Module Communication Patterns

**Domain Hot-Swapping**: All domain modules inherit from `BaseDomainModule` with standardized `process_query()` interface. Domains are loaded/unloaded at runtime via `DomainRegistry`.

**Privacy-First Architecture**: All patient data stored locally in `gpdisc_core/data/`. No external API calls for patient information.

**Multi-Specialty Coordination**: Medical domains collaborate for second opinion generation and cross-specialty consultation.

**Anti-Hallucination Protection**: Every consultation runs through the clinical validator (`validation.py`) before output — consult-level consistency plus claim-level grounding against the knowledge base and the persistent local hallucination register. Corrections only ever raise the level of concern.

---

## Key Design Patterns

### 1. Capability Auto-Selection

The system automatically selects medical specialties based on query analysis:

```python
# System auto-selects appropriate specialty
result = system.answer("I'm having chest pain")  # → Cardiology
result = system.answer("I had a seizure")        # → Epilepsy
result = system.answer("I need a checkup")       # → General Practice
```

### 2. Medical Domain Pattern

All medical domains follow the `BaseDomainModule` interface:

```python
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult

class MedicalDomain(BaseDomainModule):
    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="specialty_name",
            version="1.0.0",
            keywords=["keyword1", "keyword2"],
            capabilities=["capability1", "capability2"]
        )
    
    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        # Process medical query
        return DomainQueryResult(
            domain_name="specialty_name",
            answer="Medical consultation response",
            confidence=0.85,
            metadata={"sources": ["Medical Guidelines"]}
        )
```

### 3. Factory Function Pattern

Use factory functions for system creation:

```python
# Use factory functions
system = create_gpdisc_system()

# NOT: system = UnifiedGPDISCSystem()  # Avoid direct constructors
```

### 4. Privacy-First Memory Storage

All patient records stored locally:

```python
# Local storage only - no external transmission
from gpdisc_core.memory.persistent import create_integrator

integrator = create_integrator()
integrator.initialize_session()  # Restores previous patient records

# Store patient data locally
integrator.store_patient_record(patient_id, record)
```

---

## File Organization

### Directory Structure

```
gpdisc_core/
├── __init__.py              # Main module exports
├── core/                    # Unified system architecture
│   ├── unified.py          # Core GPDISC system
│   └── unified_enhanced.py # Enhanced system with medical domains
├── domains/                 # Medical and biological domains
│   ├── cardiology/         # Cardiology specialty
│   ├── epilepsy/           # Epilepsy specialty
│   ├── general_practice/   # General practice
│   ├── orthopedics/        # Orthopedics specialty
│   ├── pharmacology/       # Pharmacology specialty
│   ├── molecular_biology/  # Biology domain (preserved)
│   ├── biochemistry/       # Biology domain (preserved)
│   └── ...                 # Other biology domains
├── memory/                  # Local memory systems
│   └── persistent/         # Patient record storage
├── data/                    # Local data storage
│   ├── memory/             # Memory dumps
│   ├── knowledge/          # Knowledge bases
│   └── state/              # System state
├── capabilities/            # Advanced reasoning capabilities
├── causal/                 # Causal reasoning and inference
├── physics/                # Biophysics engine (generic BIODISC-era machinery preserved)
└── dashboard/              # Medical consultation dashboard
    └── server.py           # Dashboard server (port 8790)
```

### Important Files

- **Main system**: `gpdisc_core/core/unified_enhanced.py`
- **Medical domains**: `gpdisc_core/domains/<specialty>/__init__.py`
- **Memory system**: `gpdisc_core/memory/persistent/`
- **Dashboard**: `gpdisc_core/dashboard/server.py`
- **Data storage**: `gpdisc_core/data/`
- **User manuals**: `User_manual/` (PDFs + capture toolchain, see User Manual section)

---

## Dashboard

The GPDISC dashboard provides a web interface for medical consultation:

```bash
# Start the dashboard
python -m gpdisc_core.dashboard.server

# Or specify custom port
python -m gpdisc_core.dashboard.server 8790
```

Dashboard accessible at: `http://localhost:8790`

**Features**:
- Private medical consultation interface
- Multi-specialty consultation
- Second opinion generation
- Patient record management
- Local-only data storage

---

## Important Constants

### Medical Confidence Thresholds

- **High confidence**: ≥0.90 - Reliable for medical decisions
- **Medium confidence**: 0.70-0.89 - Requires verification
- **Low confidence**: <0.70 - Recommend specialist consultation

### Emergency Triage Keywords

System automatically detects emergency conditions:
- Chest pain, cardiac symptoms
- Seizure, consciousness changes
- Severe respiratory distress
- Stroke symptoms (FAST)
- Severe injuries

---

## Common Pitfalls

1. **🚨 NEVER push to GitHub**: FORBIDDEN without explicit instruction
2. **Not initializing memory**: Always call `integrator.initialize_session()` at start
3. **Skipping anti-hallucination check**: Verify medical claims before output
4. **Hardcoding medical values**: Always use knowledge base, not hardcoded values
5. **Ignoring confidence levels**: Low confidence requires specialist referral
6. **Breaking privacy**: Never transmit patient data externally

---

## Development Workflow

1. **Test before modifying**: Always run medical domain tests first
2. **Respect privacy**: All patient data must remain local
3. **Use factory functions**: Create via `create_gpdisc_system()`
4. **Register new domains**: Use `@register_domain` decorator
5. **Update exports**: Add new medical domains to `__init__.py`

---

## Post-Upgrade Verification

After any substantial changes, run comprehensive verification:

```bash
# Run comprehensive system test
python gpdisc_core/comprehensive_system_test.py

# Test all medical domains
python -c "
from gpdisc_core.domains.cardiology import CardiologyDomain
from gpdisc_core.domains.epilepsy import EpilepsyDomain
from gpdisc_core.domains.general_practice import GeneralPracticeDomain
from gpdisc_core.domains.orthopedics import OrthopedicsDomain
from gpdisc_core.domains.pharmacology import PharmacologyDomain

for domain_class in [CardiologyDomain, EpilepsyDomain, GeneralPracticeDomain, OrthopedicsDomain, PharmacologyDomain]:
    domain = domain_class()
    result = domain.process_query('test')
    print(f'{domain_class.__name__}: OK')
"

# Test system integration
python -c "
from gpdisc_core import create_gpdisc_system
system = create_gpdisc_system()
result = system.answer('Test medical query')
print('System OK')
"
```

---

## Medical Disclaimer

GPDISC provides second opinion consultation and is **NOT a replacement for professional medical care**. For medical emergencies, call emergency services (999/911).

The system provides:
- Second opinions on medical conditions
- Drug interaction checking
- Medical test interpretation
- Cross-specialty consultation
- Health information and education

All medical decisions should be made in consultation with qualified healthcare professionals.

---

## Code Statistics

- **Total Python Files**: 543
- **Tracked Tree**: 610 files; `gpdisc_core` package ~30 MB
- **Primary Medical Domains**: 5 (Cardiology, Epilepsy, General Practice, Orthopedics, Pharmacology — UK-framed)
- **Legacy Specialty Domains**: 29 (US-framed, MEDIDISC-era — background knowledge, prefer the front door)
- **Biology Domains**: 10 (preserved for scientific foundation)
- **Condition Corpus**: 273 conditions (Parts 1-6)
- **Test Battery**: 24 suites, 609 tests
- **Advanced Capabilities**: 66+ specialist capabilities
- **Dashboard Port**: 8790
