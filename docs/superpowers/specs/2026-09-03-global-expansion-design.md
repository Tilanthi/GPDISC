# GPDISC Global Expansion — Stages 6–9 Design (Spec)

**Date:** 2026-09-03
**Approved by Glenn:** "Add the contents of everything above to improve the training, i.e. as mentioned in all four tiers and Stages 6, 7, 8, 9, also including the front door mentioned with Tier 1."
**Evidence base:** the global-scope consultant audit (55-probe sweep in session; 19/55 empty differential, ~14/55 materially wrong leader — see transcript report of 2026-09-03). The four-tier gap analysis below is the requirements list; this spec is the build contract.

## Goal

Take GPDISC from a UK-GP-grade system (150 conditions, 235 green tests) to a
system fit for **any situation, anywhere in the world, routine general
practice to consultant-level opinion**: ~300 conditions, time-critical
presentations that currently get nothing (PPH, rabies exposure, cord
compression, SJS, TCA overdose, snake bite, safeguarding injuries), the
front door actually displaying the diagnosis, jurisdiction awareness, and
consultant-level interpretation machinery.

## Non-negotiable design rules (inherited from the program)

1. **Tests are clinical ground truth.** Fix the engine when the gap is real; never weaken an expectation. Every stage adds rows to the 40-case regression bank (which grows with the corpus).
2. **Corrections only ever RAISE.** The validator's contender gate (≥0.5× leader score) and every consistency rule stay intact; new corpus must not turn benign rows noisy.
3. **Safety detection is deliberately over-inclusive** — but each new rule is pattern-tested against the benign corpus rows before landing (the `acs_atypical`/night-sweats lesson: a rule word that matches a chronic constitutional phrase makes every such presentation an emergency).
4. **Privacy:** all new modules local, stdlib-only, no external data.
5. **Honesty over force-fitting:** when the corpus has nothing to say, the system says so (uncertainty scripts), instead of ranking quinsy for a dying patient.

## Corpus architecture (unchanged pattern, three new parts)

- `clinical_reasoning/knowledge_emergencies.py` → `CONDITIONS_PART4` + `SYMPTOM_SYNONYMS_PART4` (Stage 6, ~55 conditions: trauma/burns, toxicology, obstetric emergencies, oncology-supportive, dermatological emergencies, paediatric protection & syndromes)
- `clinical_reasoning/knowledge_breadth2.py` → `CONDITIONS_PART5` + `SYMPTOM_SYNONYMS_PART5` (Stage 7, ~55: neurology-chronic incl. dementia & first seizure, mental-health breadth, derm breadth, women's/men's health, GI/renal chronic, eyes/ENT windows, sleep, pain)
- `clinical_reasoning/knowledge_global.py` → `CONDITIONS_PART6` + `SYMPTOM_SYNONYMS_PART6` (Stage 8, ~40: global high-burden disease, environmental/occupational, humanitarian)
- Merged at the foot of `knowledge.py` exactly as PART2/PART3 are today; the corpus integrity test (every symptom token has synonyms; unique condition ids) must stay green.
- Every condition carries the full profile standard: symptoms with frequencies, discriminators, red_flags, investigations, management_first_line, referral_tier, safety_net, dangerous_mimic_of, source.

## Stage 6 — "Nobody dies of nothing" (Tier 1 + front door + honesty)

### 6a. Front door (the most dangerous system gap)
`answer()`'s primary `answer` text becomes the validated consultation summary when the pipeline produces one (`rec.summary()`), with the legacy domain text demoted to a metadata field. Dashboard surfaces the same. The consultation attachment, escalation and safety blocks already exist — this rewires what is *displayed*. Existing legacy tests re-run; comprehensive_system_test must stay 26/26.

### 6b. Empty-differential honesty
When the differential is empty OR the leader is noise-scored (below a floor verified against all benign bank rows), the record states explicitly: "I don't have enough knowledge to assess this presentation — describe more or see a clinician", wired to the Stage-5 uncertainty scripts. No force-fit leaders (the palliative→quinsy failure class).

### 6c–6g. New corpus + safety rules (each task: corpus + synonyms + rules + tests + bank rows)
- **Trauma & burns (6c):** traumatic brain injury (mild/moderate/severe + CT-decision discriminators), penetrating torso trauma, blunt chest trauma, haemorrhagic shock (catastrophic-bleeding first-aid), open/closed limb fracture, crush injury, major burn (fluids, airway, referral), minor burn, tetanus-prone wound, infected wound. Safety rules: head injury + LOC/vomiting; penetrating injury; shocked (pale+cold+rapid pulse); major burn.
- **Toxicology (6d):** paracetamol/TCA/opioid/salicylate overdose, CO poisoning, organophosphate, methanol, snake envenomation, alcohol-withdrawal delirium tremens, serotonin syndrome, neuroleptic malignant syndrome, lithium toxicity. General overdose rule widened beyond paracetamol phrasing; CO rule (multiple people unwell + combustion source); TCA (antidepressant + tablets); opioid triad; DT (withdrawal + tremor/hallucinosis).
- **Obstetrics (6e):** normal labour (safe framing — "this baby is coming now"), obstructed labour, postpartum haemorrhage, eclampsia + severe pre-eclampsia, shoulder dystocia, cord prolapse, miscarriage (threatened/incomplete with ringing changes), puerperal sepsis. Rules: eclampsia (seizure + pregnan/weeks), PPH (bleeding after deliver/birth), imminent delivery ("in labour" + "coming").
- **Oncology supportive (6f):** metastatic cord compression, neutropenic sepsis (chemotherapy context floor), SVCO. Rules: known cancer + new weakness; chemo + fever.
- **Dermatological emergencies (6g):** SJS/TEN, eczema herpeticum, necrotising fasciitis, erythroderma. Rules: blistering + mucosal; eczema + clustered blisters; pain-out-of-proportion skin + rapid spread.
- **Paediatric protection & syndromes (6h):** non-accidental injury (bruising in a non-mobile child = emergency; inconsistent story), Kawasaki, IgA vasculitis (HSP), febrile convulsion, neonatal jaundice (well vs unwell), neonatal sepsis. Safeguarding rule: bruise + baby/toddler who cannot walk yet.
- **Post-exposure prophylaxis (6i):** new `post_exposure/` module — rabies PEP decision (bite type + species + country + elapsed time), HBV needlestick PEP (source status + vaccination window 48–72h), HIV PEP (window 72h). Time-boxed binary decisions; rules attach urgent escalation with the window stated.

**Stage 6 exit:** all new suites green; bank extended ~18 rows (PPH, eclampsia, labour, TCA OD, CO, snake, rabies, cord compression, neutropenic sepsis, SJS, eczema herpeticum, orbital cellulitis coverage check, NAI, Kawasaki, head injury, major burn, DT, needlestick) — bank target 58 rows; full 12-suite battery + new suites green; comprehensive 26/26.

## Stage 7 — Daily breadth (Tier 2)

`knowledge_breadth2.py` (~55 conditions): dementia (Alzheimer/vascular/LBD presentation + reversible causes), first seizure/epilepsy (non-status — currently over-escalated), Parkinson's, MS, cluster headache, peripheral neuropathy; bipolar/mania, OCD, PTSD, emotionally unstable personality disorder, bulimia, perinatal mental health; acne, urticaria, scabies, tinea, drug eruption, venous leg ulcer, seborrhoeic dermatitis; menopause, perimenopause, subfertility, PCOS, dysmenorrhoea; erectile dysfunction, BPH, testicular cancer 2ww, prostatitis; constipation (incl. impaction red flags), Crohn's, UC, coeliac, decompensated cirrhosis, CKD 4–5, inguinal hernia; wet AMD, sudden sensorineural hearing loss, orbital cellulitis (cross-ref 6); OSA, insomnia; chronic pain framework, neuropathic pain. Palliative care: new `palliative_care/` module (terminal symptom control: pain, agitation, secretions, nausea, end-of-life planning, syringe-driver-equivalent knowledge) — a management discipline, not a differential, so a module like travel_medicine. Bank +~10 rows.

## Stage 8 — The world (Tier 3)

- `knowledge_global.py` (~40): chronic HBV/HCV, HIV chronic (ART monitoring, PrEP), rabies exposure presentation, leprosy, neurocysticercosis, brucellosis, melioidosis, Q fever, Chagas, African trypanosomiasis, leishmaniasis; heat exhaustion/stroke, hypothermia, altitude (AMS/HACE/HAPE), decompression illness, radiation exposure; FGM presentation care, torture-survivor presentation care, unaccompanied-minor safeguarding.
- `resource_settings/`: practice-setting descriptor (ICU/ambulance/imaging/labs available) + `disposition_guidance(escalation, setting)` — the same emergency gets different actionable advice in Kigali vs Kensington; wired into the consultation referral text when a setting is declared.
- `jurisdiction/`: jurisdiction-neutral WHO base + UK adapter; consultation summary states its ruleset ("Ruleset: UK — NICE/DVLA/2ww" vs "Ruleset: general (WHO)") so UK-specific artifacts are never presented as universal.
- `humanitarian/`: refugee/asylum arrival screening (TB, HBV, HIV, mental health), interpreter-use principles.

## Stage 9 — Consultant opinions (Tier 4 remainder)

- `mdt/roles.py` extended with corpus-driven consultant roles (cardiologist, neurologist, oncologist, paediatrician, psychiatrist, palliative physician): each computes a specialist perspective from the ranked differential (tier, dangerous mimics, investigations the specialist would demand). `run_mdt` gains a specialists pass.
- `test_interpretation.py` extended: ECG pattern interpreter (rhythm library: AF, STEMI territory mapping, VT, complete heart block, hyperkalaemia signs, digoxin effect), ABG (four-quadrant + A-a compensation), CSF (bacterial/viral/SAH), urine dip, PFT (obstructive/restrictive), synovial fluid (septic/inflammatory), blood-culture logic. Bayesian machinery already exists.

## Testing strategy per stage

Strict TDD: failing tests naming the clinical expectation → corpus/rules/modules → pass → bank rows added (never weakened) → full battery. The audit-probe discipline continues: any newly-discovered crack gets locked as a probe.

## Risks and mitigations

- **Rule false-positives on benign rows** (the night-sweats lesson): every new rule greps the entire bank + benign corpus phrases for collateral matches before landing.
- **Corpus growth turning rankings noisy:** contender gate + honesty floor already defend; benign bank rows re-verified each stage.
- **Volume diluting quality:** every condition must meet the full-profile standard or not ship; the integrity test enforces structure.
