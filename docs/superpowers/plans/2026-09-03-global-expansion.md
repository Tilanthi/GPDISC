# Global Expansion (Stages 6–9) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stages 6–9 of the approved global-expansion spec — Tier 1–4 coverage (~150 → ~300 conditions), front door + honesty, jurisdiction/resource layers, consultant roles and interpretation breadth.

**Architecture:** Follows the established corpus pattern (`CONDITIONS_PARTn` + `SYMPTOM_SYNONYMS_PARTn` merged at the foot of `clinical_reasoning/knowledge.py`), the established safety-rule pattern (`EmergencyPattern` in `safety.py`), and the established module pattern (function-returning knowledge packages like `travel_medicine`). Spec: `docs/superpowers/specs/2026-09-03-global-expansion-design.md`.

**Tech Stack:** Python 3.10+ stdlib only; pytest.

## Global Constraints

- NEVER `git push`; commits LOCAL ONLY on `main`.
- `pytest -q > file 2>&1; ec=$?` harness discipline.
- Every stage's new bank rows are ADDED, never weaken existing rows.
- Each new safety rule must be grepped against all bank cases + benign corpus phrases for collateral matches before landing (night-sweats lesson).
- Corpus integrity test must stay green: every symptom token has synonyms; unique condition ids; full profile standard.
- Privacy: local only; no new dependencies.

---

## Stage 6 — "Nobody dies of nothing" (Tier 1 + front door + honesty)

### Task 6.1: Front door — answer() displays the consultation
**Files:** Modify `gpdisc_core/core/unified_enhanced.py` (answer()); Test `gpdisc_core/tests/test_front_door.py`
- [ ] Failing test: `answer("3 year old fever stiff neck")` primary text contains the differential/meningitis + "999"/emergency language and NOT the STAN banner; non-medical query keeps a sane legacy path
- [ ] Rewire: when consultation attached → `result["answer"] = rec.summary()`, legacy text to `result["legacy_answer"]`; dashboard server checked for the same field
- [ ] Full battery + comprehensive 26/26 → commit `feat(front-door): the diagnosis is what gets displayed`

### Task 6.2: Empty-differential honesty
**Files:** Modify `consultation.py`; Test `gpdisc_core/tests/test_front_door.py` (class 2)
- [ ] Failing test: empty differential OR leader score below floor → summary leads with explicit "outside what I know — describe more / see a clinician"; no force-fit leader line for noise (palliative probe)
- [ ] Floor verified against every benign bank row's leader score (must sit below all of them)
- [ ] Battery → commit `feat(clinical_reasoning): honest uncertainty replaces force-fitting`

### Task 6.3: Trauma & burns corpus + rules
**Files:** Create `gpdisc_core/clinical_reasoning/knowledge_emergencies.py` (CONDITIONS_PART4, SYMPTOM_SYNONYMS_PART4); Modify `knowledge.py` (merge), `safety.py` (rules); Test `gpdisc_core/tests/test_emergency_breadth.py`; bank rows
- [ ] Corpus (~15): TBI mild/moderate/severe, penetrating torso, blunt chest, haemorrhagic shock, open + closed fracture, crush injury, major + minor burn, tetanus-prone wound, wound infection, degloving
- [ ] Rules: head_injury (LOC/vomiting/confusion post-head-injury), penetrating_trauma, shock (pale+cold+fast), major_burn
- [ ] Tests: ladder-fall probe, stab-wound probe (no more "COPD"), crush probe, scald probe, tetanus probe → emergency/urgent with correct leaders
- [ ] Bank +5 (head injury, stab, shock, burn, tetanus) → commit `feat(corpus): trauma and burns — the missing category`

### Task 6.4: Toxicology corpus + rules
- [ ] Corpus (~12): paracetamol/TCA/opioid/salicylate OD, CO, organophosphate, methanol, snake envenomation, DT, serotonin syndrome, NMS, lithium toxicity
- [ ] Rules: general overdose widened (any drug + count), TCA, opioid triad, CO (multiple unwell + combustion), DT (withdrawal + tremor/hallucinations)
- [ ] Tests + bank +4 (TCA OD, CO, snake, DT) → commit `feat(corpus): toxicology and withdrawal emergencies`

### Task 6.5: Obstetric emergencies corpus + rules
- [ ] Corpus (~10): normal labour, obstructed labour, PPH, eclampsia, severe pre-eclampsia, shoulder dystocia, cord prolapse, threatened + incomplete miscarriage, puerperal sepsis
- [ ] Rules: eclampsia (seizure + pregnancy), PPH (bleed + after deliver/birth), imminent birth (in labour + coming/crowning)
- [ ] Tests + bank +4 (PPH, eclampsia, labour, miscarriage) → commit `feat(corpus): obstetric emergencies — PPH and eclampsia named`

### Task 6.6: Oncology supportive + derm emergencies
- [ ] Corpus (~9): cord compression, neutropenic sepsis, SVCO; SJS/TEN, eczema herpeticum, necrotising fasciitis, erythroderma (+DRESS)
- [ ] Rules: known_cancer_weakness, chemo_fever, sjs_mucosal, eczema_blisters, nec_fasc
- [ ] Tests + bank +4 (cord compression, neutropenic sepsis, SJS, eczema herpeticum) → commit `feat(corpus): oncology-supportive and dermatological emergencies`

### Task 6.7: Paediatric protection & syndromes
- [x] Corpus (~8): NAI, Kawasaki, IgA vasculitis, febrile convulsion, neonatal jaundice, neonatal sepsis, intussusception exists — verify; slapped cheek
- [x] Rules: non_mobile_bruise (bruise + baby/infant + not walking), kawasaki_fever_days (fever ≥5 days + red eyes/strawberry tongue)
- [x] Tests + bank +3 (NAI, Kawasaki, HSP) → commit `feat(corpus): paediatric protection and syndromes — NAI and Kawasaki` (b938c2a)

### Task 6.8: Post-exposure prophylaxis module
**Files:** Create `gpdisc_core/post_exposure/` (rabies/hbv/hiv PEP decisions, window-aware); Test `gpdisc_core/tests/test_post_exposure.py`; bank rows
- [x] Failing tests: Bali dog bite → rabies PEP now + window; needlestick HBV+ source → urgent PEP; HIV exposure <72h → PEP
- [x] Implement + rules attach → bank +2 → commit `feat(post_exposure): rabies, HBV and HIV PEP — time-boxed decisions` (27dc7f1)

### Task 6.9: Stage 6 close-out
- [x] Full battery (14 suites, 309 tests) + comprehensive 26/26 + test_all baseline (fixed 3 generations of stale names: create_stan_system→biodisc→gpdisc; granger stub skipped honestly) + import sweep (457 modules clean); CLAUDE.md Stage 6 section; plan ticks; commit

## Stage 7 — Daily breadth (Tier 2)

### Task 7.1: knowledge_breadth2.py PART5 — neurology chronic + mental health (~18)
- [x] Dementia (Alzheimer/vascular/LBD + reversible causes), first seizure/epilepsy (fix over-escalation — urgent not status), Parkinson's, MS, cluster headache, peripheral neuropathy; bipolar, OCD, PTSD, EUPD, bulimia, perinatal MH
- [x] First-seizure safety-rule adjustment verified against bank (status rule keeps ≥5 min / not stopping wording)
- [x] Tests + bank +3 (dementia, mania, first seizure) → commit

### Task 7.2: PART5 — derm + women's/men's health (~20)
- [x] Acne, urticaria, scabies, tinea, drug eruption, venous leg ulcer, seborrhoeic dermatitis; menopause, perimenopause, subfertility, PCOS, dysmenorrhoea; ED, BPH, testicular cancer 2ww, prostatitis
- [x] Tests (menopause probe no longer "anxiety"; incontinence next task) + bank +3 (menopause, subfertility, ED) → commit

### Task 7.3: PART5 — GI/renal chronic + eyes/ENT + sleep/pain (~17)
- [x] Constipation, Crohn's, UC, coeliac, decompensated cirrhosis, CKD 4–5, inguinal hernia; wet AMD, sudden sensorineural hearing loss, orbital cellulitis; OSA, insomnia, chronic pain, neuropathic pain; stress incontinence
- [x] Tests + bank +3 (constipation, AMD, OSA) → commit

### Task 7.4: palliative_care module
- [x] Terminal symptom control (pain, agitation, secretions, nausea), end-of-life planning, 'can't swallow tablets' route advice; consultation_skills SPIKES cross-ref
- [x] Tests: palliative probe now answered honestly and usefully → commit `feat(palliative_care): end-of-life care`

### Task 7.5: Stage 7 close-out (battery, CLAUDE.md, commit)

## Stage 8 — The world (Tier 3)

### Task 8.1: knowledge_global.py PART6 — high-burden + environmental (~40)
- [x] Chronic HBV/HCV, HIV chronic/PrEP, rabies exposure, leprosy, neurocysticercosis, brucellosis, melioidosis, Q fever, Chagas, sleeping sickness, leishmaniasis; heat exhaustion/stroke, hypothermia, AMS/HACE/HAPE, DCI, radiation; FGM care, torture-survivor care (3e348ed; 26 conditions, corpus 272, cholera shadow-duplicate dropped; sickle crisis + acute rheumatic fever added)
- [x] Tests (leprosy probe, altitude, heat) + bank +4 → commit (test_global.py 38 tests incl. geography-tokens-never-carry-alone structural lock; bank 71→75)

### Task 8.2: resource_settings module
- [x] Setting descriptor (icu/ambulance/imaging/labs) + `disposition_guidance(level, setting)`; wired into referral text when declared (e4c271d; four settings, setting_line appended in _finalize AFTER validation)
- [x] Tests: same emergency, two settings → different actionable advice → commit (test_resource_settings.py 19 tests; never-lower-concern invariant + differential-identical-across-settings locked; asthma synonym gap found by probe and fixed)

### Task 8.3: jurisdiction package
- [x] WHO-neutral base + UK adapter; consultation summary states its ruleset; uk_practice outputs tagged as UK (a1c469d; AU/US/IN emergency numbers with honest not-loaded caveats, unknown country → WHO-neutral, uk_packages_valid tagging)
- [x] Tests → commit (test_jurisdictions.py 14 tests)

### Task 8.4: humanitarian module
- [x] Refugee/asylum arrival screening, interpreter principles, unaccompanied minors (0f647be; front-door routing with safety-wins: refugee chest pain = ACS, torture disclosure not hijacked)
- [x] Tests → commit; Stage 8 close-out (battery, CLAUDE.md) (test_humanitarian_care.py 17 tests; battery 21 suites 506 green)

## Stage 9 — Consultant opinions (Tier 4)

### Task 9.1: Consultant MDT roles
- [x] Six specialist roles (cardiologist, neurologist, oncologist, paediatrician, psychiatrist, palliative physician) computing corpus-driven perspectives; run_mdt specialists pass (743f609; contender gate ≥0.5×leader — the mimic tail triggers no one; stable-angina corpus gap found by probe and fixed: exertional/relieved-by-rest tokens)
- [x] Tests → commit (test_mdt_consultants.py 23 tests; test_mdt.py pins 6→12)

### Task 9.2: Interpretation breadth
- [x] ECG patterns (AF, STEMI territories, VT, CHB, hyperkalaemia, digoxin), ABG, CSF, urine dip, PFT, synovial fluid, culture logic (0e73656; gpdisc_core/interpretation/ four modules, seven readers; Winter's unit bug caught by the DKA test)
- [x] Tests → commit (test_interpretation_breadth.py 53 tests)

### Task 9.3: Program close-out
- [x] Full battery + comprehensive + import sweep; CLAUDE.md Stage 7–9 sections; memory; final commit (battery 23 suites 583 green; comprehensive exit 0; import sweep 580 modules clean)
