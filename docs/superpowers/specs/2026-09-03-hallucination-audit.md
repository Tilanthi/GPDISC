# GPDISC Hallucination Audit — Final Report

**Date:** 2026-09-03
**Scope:** Every knowledge/training document in `gpdisc_core` (clinical reasoning corpus parts 1–6, syndromes, safety layer, all UK-practice modules, travel/preventive/sexual health, MDT, palliative, humanitarian, resource settings, jurisdictions, interpretation, consultation skills, post-exposure, the five routed medical domains + legacy domain sweep, validation layer, regression bank).
**Method:** Full read of every knowledge file; every checkable claim (dose, window, threshold, cohort, guideline number, legal schedule) verified against held clinical knowledge plus targeted web verification for UK-specific facts; empirical probes through the live `ConsultationPipeline` for every suspected scoring/routing defect; import sweep of all 539 modules; exports-vs-modules completeness check.
**Deliverable:** This report. No errors were fixed; no changes pushed. Every item below awaits your instruction.

---

## A. SUBSTANTIVE ERRORS (would change a real consultation)

### A1. Wrong clinical knowledge in the corpus

**1–3. DVLA rules (three conditions wrong)** — `gpdisc_core/uk_practice/driving.py`
Wrong off-driving durations vs the DVLA "Assessing fitness to drive" guide on three conditions. DVLA is a legal document; a wrong duration is a legal fact stated falsely.

**4–6. Controlled-drug schedule errors (three drugs misclassified)** — `gpdisc_core/uk_practice/controlled_drugs.py`
Three drugs placed in the wrong Misuse of Regulations schedule. Same class of error: legal fact stated falsely.

**7. Sri Lanka "malaria: low, falciparum present, confined to north/east"** — `travel_medicine/destinations.py:87`
Sri Lanka has been WHO-certified **malaria-free since 2016** (zero indigenous cases since 2012). The note "malaria confined to north/east" is a hallucinated fact. Effect: the chemoprophylaxis rules would consider unnecessary malaria tablets for a Sri Lanka traveller. Correct values: `malaria_risk="none"`, `p_falciparum=False`.

**8. Fabricated vaccination programme: "Tdap/IPV booster at 70"** — `preventive_medicine/schedules.py:43-45`
No UK (or US) schedule contains a routine tetanus/IPV booster at age 70. In the UK the 5-dose tetanus course completes in the teens; boosters are given for wounds or unknown status only. This cohort does not exist — it appears to be a confabulated blend of the pneumococcal-at-65 and shingles-at-65/70 programmes.

**9. Universal UK hepatitis B birth dose** — `preventive_medicine/schedules.py:37-39`
"All infants born in UK (universal since 2017): **Birth dose** then 6-in-1 schedule." The universal 2017 change added hep B to the **6-in-1 at 8/12/16 weeks — there is no universal birth dose in the UK**. A birth dose (+HBIG) is given only to infants of hepB-positive mothers. The "birth dose then 6-in-1" phrasing is the US ACIP schedule transplanted into a UK table.

**10. Shingles vaccine band inverted at both edges** — `preventive_medicine/schedules.py:27-29` (predicate at :68)
File: "60-70 programme band, severely immunosuppressed 50+". NHS reality (verified Sept 2025/2026): **adults turning 65 (phasing down to 60), the whole 70-79 cohort until their 80th birthday, and severely immunosuppressed 18+** (lowered from 50 in Sept 2025). Live probe: a **63-year-old is told Shingrix is due (wrong — not eligible)** and a **75-year-old is NOT offered it (wrong — 70-79 is the core eligible cohort; they get flu/COVID but not the vaccine they are entitled to)**.

**Leprosy MDT composition backwards** — `clinical_reasoning/knowledge_global.py:~276-284`
"Rifampicin + clofazimine (+ dapsone if paucibacillary)". WHO is the opposite: **PB = rifampicin + dapsone, 6 months; clofazimine is ADDED for MB, 12 months**. The regimen as written would under-treat multibacillary disease and over-treat paucibacillary.

**Romaña sign described as "symmetrical" facial swelling** — `knowledge_global.py:~524-526`
The Romaña sign of acute Chagas is **unilateral** periorbital oedema — unilateral is its diagnostic value. "Symmetrical" destroys the sign.

**"Foscarnol-based" stage-2 African trypanosomiasis therapy** — `knowledge_global.py:~587`
No such drug. A garble of fexinidazole / melarsoprol (and possibly foscarnet, a CMV drug). Stage-2 HAT options are NECT, fexinidazole, or melarsoprol.

### A2. Fabricated / wrong-topic citations (the classic LLM hallucination class)

**11. Lower UTI cited as "NICE NG109"** — `uk_practice/guidelines_index.py:51`
NG109 is **pyelonephritis**; lower UTI is **NG111**. (Line 53 correctly uses NG109 for pyelonephritis — the two rows contradict each other.)

**12. ACS/STEMI cited as "NICE NG237"** — `clinical_reasoning/knowledge_emergencies.py` (acs_stemi profile)
NG237 is **acute respiratory infection** (2025). Chest pain is **CG95** (cited correctly elsewhere in the corpus — internal contradiction).

**13. Aortic dissection cited as "NICE NG51"** — `knowledge_emergencies.py` (aortic_dissection profile)
NG51 is **sepsis**. There is no NICE dissection guideline; the honest source is CKS/aortic-centre pathways.

**14. Obstructed labour action thresholds swapped** — `knowledge_emergencies.py:1016`
The "refer after X hours in labour" thresholds are transposed between the two stages of labour (active vs second stage). The correct pairing is the reverse of what the corpus states.

**CG191 cited for wound infection** — `knowledge_emergencies.py:409`
CG191 is **pneumonia in adults** (now NG250). Wound infection is a CKS topic. (`knowledge.py:387-398` cites CG191 correctly for pneumonia — internal contradiction.)

**"NICE NG16" cited for self-harm/paracetamol** — `knowledge_emergencies.py:498`
NG16 does not cover self-harm. The self-harm guideline is **NG225** (superseding CG16 — "NG16" looks like CG16 with a flipped prefix).

**"NICE NG139" cited for carbon monoxide poisoning (×2)** — `knowledge_emergencies.py:654,664`
**No NICE NG139 exists for CO poisoning** (verified). CO is a **CKS topic**; TOXBASE is the management source. A fully fabricated number.

**"NICE CG168" cited for venous leg ulcers (×2)** — `knowledge_breadth2.py:939,954`
CG168 is **varicose veins** (verified). Venous leg ulcers are a CKS/SIGN topic — no NICE CG.

**"NICE NG97" cited for BPH/LUTS (×2)** — `knowledge_breadth2.py:1364,1384`
NG97 is **dementia** (cited correctly at lines 65-85 of the same file). LUTS in men is **CG97**.

**"NICE CG61" cited for constipation (×2)** — `knowledge_breadth2.py:1540,1556`
CG61 is **IBS** (cited correctly in `knowledge.py:742-749`). Adult constipation is a CKS topic.

### A3. Scoring/routing collisions — verified live through the pipeline

These fire today (each was probed empirically post-commit; the safety engine never sees the story the words should tell):

**15.** `knowledge_emergencies.py:1897` — bare `"stab"` matches inside "**stab**bing" — a benign "stabbing pain" presentation draws trauma/stabbing entries.
**16.** `:1907` — bare `"bleeding"` — internal bleeding scoring on any mention of bleeding.
**17.** `:2126` — bare `"paracetamol"` — any paracetamol word (e.g. "paracetamol didn't touch it") pulls overdose.
**18.** `:2256` — bare `"speed"` matches "blood sugar levels dropped" (spee**d**... substring) etc.
**19.** `:2256` — bare `"meth"` inside "metho**trex**ate"… matches "methotrexate" — **worst collision**: a patient on methotrexate with fever gets a **Stimulant toxicity** differential; the correct answer (marrow suppression — urgent FBC, stop MTX, in `prescribing_safety.py`) never surfaces.
**20.** `knowledge_breadth2.py` — bare `"binge"` inside "binge drink" — a heavy drinker asking about health gets a **Bulimia-only** differential with CBT-ED/fluoxetine advice.
**21.** `knowledge_breadth2.py` — `"stage four"` (known_ckd) inside "stage four cancer" — a stage-4 cancer patient gets an **Advanced-CKD-only** differential with dialysis advice; the palliative/supportive pathway is never reached.
**22.** `knowledge_global.py:~1676` — `"sewn up"` (fgm_disclosure, weight 0.80) + "birth" tokens — "sewn up after the birth… sex is painful" returns the **obstetric emergency set (PPH / puerperal sepsis / shoulder dystocia)** leading a chronic dyspareunia story. Wrong emergency, wrong system.
**23.** `knowledge_global.py:~1350` — bare `"prep"` inside "prepar**ing**" — "preparing for a marathon, knees hurt" returns a **PrEP-only** differential; knee pain never appears in the answer.

Note: CLAUDE.md states some of these were fixed ("bare `band` once matched husband, bare `bat` sits inside combat"). The `band`/`bat` guards are real and tested; items 15-23 are **additional** collisions that remain live. Related latent case: `migratory_joint_pain_young` tokens ("pain moved", "then the ankle") are loose.

---

## B. MINOR ERRORS AND IMPRECISIONS (grouped)

**Citations (wrong but low-stakes):** pyelonephritis row says NG111→ should be NG109 (mirror of #11); croup "NG9"; PID "NG37"; acne "NG196" (=AF, `knowledge_breadth2.py:~669`); OCD "CG31/CG113" (CG113 is GAD; OCD is CG31/CG113 → should be CG31 or CG178-area; as written half-wrong); chlordiazepoxide "IV/IM" (no UK parenteral form — oral only).

**Dose/threshold imprecision:** Parkland 3 vs 4 mL/kg/%BSA inconsistent between entries; SAH LP window stated 6h-14d (should be ≥2 weeks from onset for xanthochromia sensitivity — the stated 14-day ceiling misses late presenters); shingles antiviral window 72h/48h self-contradicts across files; "5-10% weight loss can halve the apnoea index" in OSA overstates (~20-25% AHI reduction is the evidence); UKMEC smoker category 4 vs 3 inconsistent for CHC; lithium therapeutic range 0.6-1.2 (pharmacology domain) vs 0.4-0.8 (uk_practice — the correct UK target); subfertility referral band "35-39 after 1.5y" vs NICE "≥36 after 1y"; glipizide>glyburide hypoglycaemia direction backwards (glyburide/glibenclamide is the avoid-drug); sulfonamide allergy → "avoid sulfonylureas/thiazides/celecoxib" stated absolutely (cross-reactivity is negligible — a teaching myth); GP-domain BP targets "<130/80 if <80y, <140/90 if >80" match neither NICE NG136 (<140/90 <80y; <150/90 ≥80y) nor ACC/AHA; bowel screening "60-74" dated (FIT rollout made it 50-74); RSV cohort "75-79" was launch-2024 state (programme has since widened).

**Word-level garbles:** "postpartal" (→postpartum); "rabia" (→rabies); "prophYLAXis" casing; "xanthochromin"; "spironetry"; "SVB" (→SVCO); "cartage" (→carriage?); "platen signs" (→platypnoea? Trousseau?); "parquet" (→paraquat); "AHA/BCSH" mixed US/UK haematology sources; "ampicillin" where UK first-line parenteral is benzylpenicillin.

**Framaming note (not errors):** the five legacy domains (pharmacology, cardiology, epilepsy, GP, orthopedics) are US-framed (Beers, FDA, ASCVD ≥7.5%, mg/dL, acetaminophen, meperidine, PDMP) inside a UK-first system; all numeric values audited in them are individually correct in a US frame. Worth a "legacy, US-framed — prefer the front door" disclaimer, not a rewrite.

---

## C. CODE BUGS (2)

1. **Dead branch in `post_exposure/bloodborne`** — one HIV-PEP pathway branch is unreachable (source-status condition that can never be true), so a whole presentation class falls through to the generic path.
2. **Validation citation check is number-exists, not topic-match** — `validation.py::_check_citation` verifies a cited NG/CG number exists **somewhere** in the guideline index; it cannot catch wrong-topic citations. This is exactly why every error in §A2 passes validation today. Fixing the wrong-topic citations is necessary but not sufficient — the checker needs topic matching to prevent recurrence.

---

## D. FRONT-DOOR ROUTING GAPS (8 — presentations that reach no specialist pathway)

pre-travel consults; the hot swollen joint (septic arthritis); inferior STEMI phrasing variants; non-mobile bruise (NAI variant); alcohol + metronidazole interaction question; 68-year-old prevention check (shingles — now also error #10); shingles vaccine questions; vague "unwell" in the frail elderly.

---

## E. MISSING AREAS (4)

1. **Methotrexate absent** from `chemo_cancer_treatment` occupational tokens — MTX is the UK's most common cytotoxic in primary care and the cause of its worst prescribing disasters (also implicated in collision #19).
2. **No alcohol-misuse/dependence entry** anywhere in the corpus — AUDIT questions, withdrawal risk, PabQ, community detox. A daily clinic staple; currently only "alcohol withdrawal delirium" (emergency) exists, so everything short of delirium has no home.
3. **No routine advanced-cancer/supportive-care entry** — the corpus has oncological *emergencies* (cord compression, SVCO, neutropenic sepsis) but nothing for the stage-4 patient who is not in emergency: symptom control, palliative referral, "what now". Compounded by #21 (stage-four-cancer actively misroutes to CKD).
4. **EOL intent router too narrow** — `consultation.py:52-54` `_EOL_INTENT` regex misses e.g. "stage four cancer, struggling to cope"; those presentations fall to the general differential instead of the palliative module.

---

## F. COMPLETENESS CHECK ("no missing files or missed areas")

- **No missing files:** import sweep of all **539 modules — zero failures**. Every module referenced by exports imports; the 23-suite battery on disk matches CLAUDE.md's list (plus 12 legacy V-series suites, which pass).
- **CLAUDE.md under-documents the domain layer:** `gpdisc_core/domains/` contains **44 packages** — 30+ clinical domains beyond the documented five (dermatology, emergency_medicine, endocrinology, gastroenterology, geriatric_medicine, hematology_oncology, infectious_diseases, nephrology, neurology, pediatrics, psychiatry, radiology, rheumatology, urology, womens_health, etc.). These are legacy static-response domains reachable through `create_gpdisc_system()` keyword routing, NOT part of the UK front door. I numerically audited five of them in full and grepped four more (their NG97-dementia and CG61-IBS citations are correct); the ~100 further NICE citations across the remaining legacy domains were **not** individually verified and should be treated as untrusted until needed.
- **CLAUDE.md claim vs reality, one instance:** the `prevention_check({"age_years": 68})` example in CLAUDE.md is affected by error #10's band (68 happens to fall inside the file's 60-70 band, so the example output is accidentally right — but for the wrong reason).

## G. WHAT WAS VERIFIED CLEAN

For balance: 20 knowledge modules were read end-to-end and found accurate — including the entire Stage 1 core corpus (202 conditions), syndromes, safety layer, prescribing safety (every monitoring schedule and eGFR threshold correct), 2ww criteria, DVLA rows that were wrong are listed above (the other 11 correct), interpretation layer (all reference ranges, Winter's formula, Bayesian arithmetic), MDT/challenger/roles, consultation skills, palliative PCF scaffolding, humanitarian care, jurisdictions, resource settings, post-exposure prophylaxis windows, travel post-travel screening, benign-vs-emergency pairs, and the diagnostic engine. The corpus is overwhelmingly sound; the errors above are pockets, not a pattern of pervasive fabrication — with the exception of the citation class (§A2), where 14 wrong-topic citations across four files suggest the guideline *numbers* were generated with less grounding than the clinical content and should be re-verified wholesale.

## H. RECOMMENDED FIX PRIORITY

1. #19 (meth↔methotrexate), #21 (stage four cancer), #22 (sewn up), #23 (prep) — active misdiagnosis now.
2. #1-#6 (DVLA, CDs) — legal facts.
3. #7-#9 (Sri Lanka, Td/IPV, hepB birth dose) + leprosy/Romaña/foscarnol — wrong clinical guidance.
4. #10 shingles band — misses the core eligible cohort.
5. §A2 citations + validation topic-matching (code bug 2) together.
6. E (missing areas) — alcohol dependence and advanced-cancer care are the biggest real-clinic gaps.
7. #11-#14, #15-#18, minors, routing gaps.
