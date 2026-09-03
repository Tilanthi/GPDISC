# GPDISC External Consultant Audit — 2026-09-03

Commissioned: "act as an outside medical consultant… census of the expertise
levels… What areas are missing, where are the cracks into which people with
marginal conditions could fall."

Method: codebase census + wiring trace + 16 marginal presentations executed
through the live `ConsultationPipeline`. Evidence below is observed engine
behaviour, not review of documentation.

## Census (built)

150 conditions / 18 categories; 242 symptom tokens; 19 emergency+urgent
safety rules; 5 tropical syndrome frames; travel (24 destinations),
prevention, sexual health (UKMEC) packages; uk_practice (24 guideline refs,
16 2ww rules, 14 DVLA conditions, MCA/DNACPR/safeguarding, CDs,
stewardship, high-risk-drug monitoring, fit notes); MDT challenger + 6 roles
+ chair synthesis; multimorbidity whole-patient review; consultation skills
(ICE, SPIKES, safety-net formula, 6 difficult-consultation kinds,
uncertainty scripts); 10 benign-vs-emergency pairs; 40-case regression bank.
193 tests green.

## Missing whole domains (vs the 26-domain specification)

- Toxicology/poisoning/overdose — absent entirely
- Palliative/end-of-life care — absent entirely
- Occupational/environmental medicine — absent entirely
- Dermatology — 4 conditions (visual specialty, minimal coverage)
- Paediatrics — 6 conditions; Oncology — no detection pathway (9 scattered 2ww suspects)
- Ophthalmology breadth; addiction/perinatal psychiatry breadth

## Cracks — marginal-presentation probe results (live engine)

| # | Probe | Engine output | Verdict |
|---|---|---|---|
| 1 | 67F nausea+sweating+jaw ache 20 min, no chest-pain words | routine (acs_stemi ranked FIRST) | FAIL — differential/safety disconnect |
| 2 | 88F "gone quiet, off food, not herself", no fever | routine, empty differential | FAIL — afebrile elderly delirium invisible |
| 3 | 32F severe one-sided pelvic pain, dizzy standing, coil | routine (ectopic ranked FIRST) | FAIL — same disconnect |
| 4 | 79M sudden dizziness + diplopia + unsteady | routine; GCA/Addison's/preeclampsia | FAIL — no posterior-circulation rule |
| 5 | lip swelling + itchy rash after food | routine; eczema/chickenpox/zika | FAIL — anaphylaxis word-order blindness |
| 6 | husband controls medicines, won't let her attend alone | routine; tension_headache | FAIL — safeguarding unwired to front door |
| 7 | 17F cutting herself, no suicide words | routine, empty | FAIL — self-harm rule lacks behaviour words |
| 8 | 20 paracetamol tablets 6 h ago | routine, empty | FAIL — no toxicology (missing domain) |
| 9 | 63M 6 kg loss + night sweats | routine; TB/endocarditis/HIV, no 2ww surfaced | PARTIAL — 2ww layer unwired |
| 10 | 45F 6 months no energy, aching, anhedonia | influenza/URTI/leptospirosis | FAIL — depression extraction blind |
| 11 | 4-month infant poor feeding, fewer wet nappies | urgent, febrile_child_serious | PASS |
| 12 | post-op knee replacement + breathless | emergency, pe | PASS |
| 13 | new ankle swelling + orthopnoea | routine, acute_heart_failure first | PASS (judgement: defensible) |
| 14 | 22M headache + photophobia + vomiting, no fever stated | routine; meningitis in top 3 | BORDERLINE — differential right, escalation arguable |
| 15 | medication-change postural dizziness | routine; polypharmacy_adverse_effect first | PASS (differential); monitoring flags unwired |
| 16 | "room spins sometimes" | routine; b12_deficiency; zero questions | FAIL on process — no discriminating questions outside tropical frames |

**Meta-crack**: emergency escalation is decided by keyword rules that never
consult the differential they precede. The engine twice ranked the killer
condition first and still said "routine". (Probes 1, 3.)

## Accessibility — is each expertise level reachable by the diagnoser?

| Layer | Reached via front door? |
|---|---|
| Differential, syndromes, escalation, uncertainty | YES — `answer()` surfaces the consultation record |
| 2ww cancer criteria, DVLA, capacity/safeguarding, CD rules, stewardship, monitoring/renal flags | NO — libraries only, nothing calls them in a consultation |
| MDT (challenger/roles/debate), multimorbidity review | NO — standalone `run_mdt`/`whole_patient_review` |
| Discrimination pairs, consultation skills | NO — exported but never invoked by the pipeline |
| Dashboard | static files; no consultation endpoint |

`answer()`'s primary text remains the legacy canned-domain answer; clinical
reasoning rides as an enrichment attachment.

## Marginal-condition question process

`discriminating_questions` generates ONLY for the 5 tropical syndrome frames.
All 16 probes: zero questions emitted. The raw material exists (condition
discriminators, pair discriminators, the challenger's missing-discriminator
attack, the closeness detector) but is connected to nothing. Fix specified in
the validation design: top-2 close → leader + pair discriminators emitted.

## Anti-hallucination verdict

The existing hallucination system is a retrospective string-similarity
blacklist from the BIODISC era, unwired to clinical reasoning, unable to
catch novel wrong clinical claims. No grounding, consistency, completeness,
or provenance verification of diagnostic output existed. → Built as
`clinical_reasoning/validation.py` per
`2026-09-03-clinical-validation-design.md`.
