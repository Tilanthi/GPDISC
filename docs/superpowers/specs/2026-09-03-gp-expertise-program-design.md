# GPDISC GP Expertise Program — Design

Date: 2026-09-03
Status: Approved by Glenn ("Do all of them in the order you wish, I need all these expertise levels installed")
Spec source: Glenn's 27-domain curriculum + 6-level architecture + MDT proposal (2026-09-03)

## Goal

Transform GPDISC from a keyword-routed specialty encyclopaedia into a GP-led
consultation intelligence with genuine diagnostic reasoning: symptom → ranked
differential → Bayesian investigation strategy → safe management or referral,
deliberately strong at separating benign from dangerous presentations, with a
virtual MDT and adversarial diagnostic challenger for difficult cases.

## Existing assets (built upon, not replaced)

- 37 specialty domain modules (~2,000–2,600 lines each) under
  `gpdisc_core/domains/` — Level 2 substrate of varying depth
- `gpdisc_core/coordination/specialty_coordinator.py` — SpecialtyOpinion,
  ConflictDetector/Resolver, SecondOpinionGenerator — MDT substrate
- `gpdisc_core/memory/persistent/` anti-hallucination verification — all
  clinical claims in new code run through it where quantitative
- `GeneralPracticeDomain` — currently a 517-line keyword dispatcher; superseded
  as front door by the reasoning core, retained for triage routing

## Architecture (Glenn's 6 levels, mapped to packages)

```
Level 6  Safety & metacognition        gpdisc_core/clinical_reasoning/safety.py
Level 5  Integrative + MDT             gpdisc_core/mdt/  (+ multimorbidity.py)
Level 4  UK practice layer             gpdisc_core/uk_practice/
Level 3  Global medicine               domains/tropical_medicine, travel_medicine
Level 2  Specialty modules             existing 37 domains + missing ones below
Level 1  General medicine core         gpdisc_core/clinical_reasoning/
```

## Stage 1 — Clinical Reasoning Core + Safety Layer (Levels 1 + 6)

New package `gpdisc_core/clinical_reasoning/`:

- `knowledge.py` — structured condition knowledge:
  `ConditionProfile`: epidemiology (prevalence in GP setting), presenting
  symptoms with frequencies, red flags, discriminators, investigations with
  test characteristics (sensitivity/specificity/likelihood ratios where
  meaningful), first-line management, referral tier (self-care / routine /
  urgent / 2ww-suspected-cancer / emergency), safety-net advice. Initial
  corpus: high-yield GP conditions across all systems, weighted toward
  dangerous mimics of benign presentations.
- `diagnostic_engine.py` — problem representation from free text; ranked
  differential with pre-test probabilities; Bayesian update via likelihood
  ratios; pattern-recognition fast path vs analytical path; must-not-miss
  overlay; anti-anchoring (competing hypotheses retained and re-scored, never
  pruned by conviction alone); premature-closure guard.
- `test_interpretation.py` — reference ranges; sens/spec → PPV/NPV at given
  pre-test probability; LR arithmetic; "when not to investigate" logic
  (test only if result changes management).
- `consultation.py` — the consultation pipeline as an explicit state machine:
  presenting complaint → history → background → medication/allergies → risk
  factors → targeted examination → problem representation → ranked
  differential → dangerous alternatives → investigation strategy →
  interpretation → treatment → referral → follow-up → safety net. Emits a
  structured `ConsultationRecord` the dashboard can render.
- `safety.py` — escalation classifier (emergency/urgent/routine), emergency
  keyword+cluster detection (ABCDE, sepsis, ACS, stroke, anaphylaxis…),
  dangerous-uncertainty detection, "I don't know yet" as a valid clinical
  output, remote-assessment limitations, mandatory human-clinician triggers,
  safety-net generation.

Wiring: `EnhancedUnifiedGPDISCSystem.answer()` routes medical queries through
the reasoning core first (GP-led); specialist domains are consulted as
referral opinions beneath it.

## Stage 2 — Missing domains (Levels 2 + 3)

New domain modules (same `BaseDomainModule` pattern, registered in the
registry):

- `tropical_medicine/` — **syndrome-based** diagnosis first (fever after
  travel, fever + rash, fever + jaundice, fever + thrombocytopenia, fever +
  neurological signs, bloody diarrhoea, eosinophilia…), then disease profiles
  (malaria incl. severe falciparum, dengue, chikungunya, Zika, yellow fever,
  Japanese encephalitis, rabies, trypanosomiasis, Chagas, leishmaniasis,
  schistosomiasis, filariasis, onchocerciasis, strongyloidiasis, geohelminths,
  taeniasis/cysticercosis, echinococcosis, amoebiasis, giardiasis, cholera,
  typhoid, leptospirosis, rickettsiae, brucellosis, melioidosis, TB/MDR-TB,
  leprosy, HIV + opportunistic infection, VHF, mpox, measles, snakebite/
  envenomation, heat illness, severe dehydration, malnutrition).
- `travel_medicine/` — pre-travel risk assessment, geographic epidemiology,
  vaccination, malaria prophylaxis, traveller's diarrhoea, altitude illness,
  post-travel fever assessment, animal exposure/rabies PEP, migrant health.
- `preventive_medicine/` — screening programmes, CVD risk, diabetes
  prevention, obesity, smoking, alcohol, exercise, nutrition, vaccination
  frameworks, falls, health inequalities.
- `sexual_health/` — STIs, HIV, contraception, fertility, sexual dysfunction,
  assault pathways, safeguarding.
- ENT domain extended with oral medicine (dental infection, oral lesions/
  cancer) per the spec's grouping.

## Stage 3 — UK Practice Layer (Level 4)

New cross-cutting package `gpdisc_core/uk_practice/`:

- NICE/CKS guidance index (topic → key recommendations, cited by guideline ID)
- BNF prescribing principles: dose/renal-hepatic adjustment/contraindications/
  interactions/monitoring/stopping rules/overdose for high-risk drug classes
  (anticoagulants, antibiotics, steroids, insulin, opioids, psychotropics,
  immunosuppressants, narrow-therapeutic-index drugs)
- NHS vaccination schedule, NHS screening programmes
- Two-week-wait / urgent suspected-cancer pathway criteria per cancer
- Referral thresholds (routine/urgent/emergency), primary-secondary interface
- Safeguarding (children & adults), Mental Capacity Act, consent/
  confidentiality, DNACPR/advance care planning, DVLA medical standards,
  fit notes, controlled drugs rules, antimicrobial stewardship

Consumed by the reasoning core, MDT, and specialty domains — never a
standalone silo. Where a numeric clinical rule matters (e.g. Wells score,
CURB-65, NEWS2 thresholds, QFracture/QRISK concept), it is encoded as data
with the rule named so the anti-hallucination layer can verify.

## Stage 4 — MDT + Multimorbidity (Level 5)

New package `gpdisc_core/mdt/`:

- Team of specialist agents constructed over existing domains + reasoning
  core: GP Diagnostician (chair), Emergency Physician, ID/Tropical
  Specialist, Clinical Pharmacologist, Paediatrician, Psychiatrist,
  Geriatrician.
- **Adversarial Diagnostic Challenger** — deliberately attacks the leading
  diagnosis: proposes alternatives, identifies what evidence would
  distinguish them, flags anchoring/premature closure, argues for the
  dangerous mimic.
- Debate protocol: independent hypothesis construction → structured
  cross-examination → conflict detection/resolution (reuses coordination
  layer) → converged assessment with explicit residual uncertainty.
- `multimorbidity.py` — whole-patient engine: disease×disease interactions,
  drug×disease×drug interactions, renal-clearance cascade reasoning,
  deprescribing analysis, atypical-presentation reasoning in frailty.
  Triggered when a query/case involves multiple active problems, polypharmacy
  (≥5 drugs), frailty, or when single-domain confidence is low.
- Engagement policy: simple presentations → reasoning core alone;
  complex/multimorbidity/low-confidence/disagreement → full MDT.

## Stage 5 — Curriculum depth pass

Systematic deepening of every domain against the curriculum bullet lists,
starting with the domains Glenn flagged for extra weight (acute/emergency
discrimination, endocrine/diabetes, paediatrics, geriatrics, clinical
pharmacology, consultation skill). Adds a regression bank of multimorbidity
and dangerous-mimic cases (e.g. the 79-year-old with CKD+DM+HF+OA+MCI on
eight medications presenting with dizziness and confusion).

## Error handling & safety principles

- Any chest pain, breathlessness, neurological symptom, sepsis cluster, or
  paediatric red flag runs the emergency overlay FIRST; benign framing never
  suppresses it.
- Every consultation output carries: confidence, red flags screened,
  safety-net advice, escalation tier, and "GPDISC is not a substitute for
  professional care" positioning.
- Clinical content authored from established medical knowledge; quantitative
  claims (doses, thresholds, test characteristics) encoded with named sources
  (NICE/CKS/BNF IDs where applicable) and verified against the
  anti-hallucination register.
- Uncertainty is a first-class output, not a failure.

## Testing strategy

- Unit: Bayesian arithmetic (PPV/NPV/LR), reference-range logic, escalation
  classifier, pipeline state transitions.
- Clinical scenarios: benign-vs-emergency discrimination pairs (e.g. tension
  headache vs SAH; dyspepsia vs ACS; viral URTI vs sepsis in a child);
  multimorbidity cases; anti-anchoring checks (engine must retain the
  dangerous alternative).
- Regression: existing comprehensive test (26/26), domains, import sweep
  (497 submodules), test_all.py baseline (11 pass / 3 legacy failures).
- No push to any remote, ever, without explicit instruction (privacy rule).

## Explicitly out of scope (this program)

- No external LLM/API calls for patient data; no cloud services
- No live BNF/NICE scraping — knowledge is authored, versioned locally
- Dashboard visual overhaul (the ConsultationRecord is exposed so a UI can
  render it later)
