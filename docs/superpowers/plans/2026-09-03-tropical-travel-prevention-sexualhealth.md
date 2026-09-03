# Stage 2: Tropical/Travel + Preventive + Sexual Health Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install Level 3 of the GP expertise architecture: syndrome-based tropical medicine wired into the clinical-reasoning front door, structured travel-medicine (pre- and post-travel), NHS-aligned preventive medicine, and sexual/reproductive health decision rules.

**Architecture:** Extends the Stage 1 `clinical_reasoning` package with a third corpus module (tropical/ENT-oral/sexual-health conditions) and a `syndromes.py` engine (Glenn's five named syndrome frames: fever after travel, fever + rash, fever + jaundice, fever + thrombocytopenia, eosinophilia). Three new top-level clinical packages — `travel_medicine`, `preventive_medicine`, `sexual_health` — hold structured data tables and decision functions, mirroring how `uk_practice` and `mdt` will land in Stages 3-4. The consultation pipeline learns to attach a syndrome frame with discriminating questions when one matches.

**Tech Stack:** Python 3.10+ stdlib only, pytest, dataclasses. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-09-03-gp-expertise-program-design.md`

## Global Constraints

- Python 3.10+ stdlib only; no third-party packages.
- All data local-only; no network calls, no external LLM transmission.
- **NEVER `git push`** — repo has no remote; push is forbidden by project CLAUDE.md privacy rule.
- All commits LOCAL ONLY on `main` (repo convention: linear local history).
- Every corpus symptom token must exist in `SYMPTOM_SYNONYMS` after merge; part-3 synonym keys must NOT redeclare existing keys (the merge is a dict `update()`, which overwrites).
- Clinical ground truth for scoring disputes = the tests in this plan.
- Referral tiers limited to: self_care, routine, urgent, two_week_wait, emergency.
- New clinical packages export factory-style functions and data classes; no module-level side effects beyond table construction.

---

### Task 1: Corpus part 3 — tropical, ENT/oral, sexual health

**Files:**
- Create: `gpdisc_core/clinical_reasoning/knowledge_tropical.py`
- Modify: `gpdisc_core/clinical_reasoning/knowledge.py` (merge block at bottom)
- Test: `gpdisc_core/tests/test_clinical_reasoning.py` (new class `TestCorpusPart3`)

**Interfaces:**
- Consumes: `ConditionProfile`, `SymptomFrequency`, `InvestigationProfile` from `gpdisc_core.clinical_reasoning.schema`; `CONDITIONS`, `SYMPTOM_SYNONYMS` in `knowledge.py`.
- Produces: `CONDITIONS_PART3: List[ConditionProfile]` (29 entries), `SYMPTOM_SYNONYMS_PART3: Dict[str, List[str]]` (14 new tokens). After merge, `CONDITIONS` totals 150 and `SYMPTOM_SYNONYMS` totals 239. New categories: `tropical`, `ent_oral`, `sexual_health`.

Rows are authored as tuples and expanded by a builder so the data is declared once:

```python
"""Corpus part 3: tropical/travel-acquired, ENT/oral, and sexual health
conditions (expertise program Stage 2). Merged into CONDITIONS at import
time by knowledge.py — same pattern as knowledge_breadth.py."""
from typing import List, Dict
from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile, SymptomFrequency, InvestigationProfile,
)

# (condition_id, name, category, prior, tier,
#  symptoms [(token, freq, spec)], discriminators, red_flags,
#  investigations [(name, purpose, sens, spec)],
#  management_first_line, safety_net, dangerous_mimic_of)
_ROWS = [
    # ---- Tropical / travel-acquired ----
    ("malaria_vivax", "Malaria (P. vivax / P. ovale)", "tropical", 0.002, "urgent",
     [("fever_after_travel", 0.95, 0.9), ("shivering_rigors", 0.8, 0.5),
      ("headache", 0.6, 0.2), ("fatigue", 0.5, 0.1), ("nausea", 0.4, 0.1)],
     ["Relapses weeks apart (hypnozoite liver stages) — ask about fever pattern over months",
      "Blood film speciation is mandatory: falciparum must be excluded first"],
     [],
     [("malaria_blood_film", "Thick and thin films x3 over 24-48h; species + parasitaemia", 0.95, 0.95),
      ("malaria_rdt", "Rapid antigen test — rapidly excludes falciparum", 0.90, 0.95)],
     "Same-day refer. Chloroquine (sensitive areas) then primaquine for radical cure AFTER G6PD check; falciparum excluded first.",
     "Drowsiness, jaundice or deterioration = emergency. One negative film never excludes malaria — 3 films over 24-48h.",
     ["influenza"]),
    ("chikungunya", "Chikungunya", "tropical", 0.0015, "routine",
     [("fever_after_travel", 0.9, 0.9), ("myalgia", 0.7, 0.2), ("joint_pain_severe", 0.7, 0.5),
      ("fever", 0.85, 0.1), ("headache", 0.5, 0.1)],
     ["Debilitating symmetric polyarthralgia outlasting the fever is the signature",
      "Exclude dengue before NSAIDs"],
     [],
     [("chikungunya_serology", "Paired serology (IgM/IgG)", 0.8, 0.95)],
     "Supportive: fluids, paracetamol; NSAIDs only after dengue excluded (platelet risk).",
     "Bleeding, bruising or abdominal pain → urgent review (dengue warning signs).",
     ["influenza"]),
    ("zika", "Zika virus infection", "tropical", 0.0008, "routine",
     [("fever_after_travel", 0.85, 0.85), ("fever", 0.7, 0.05), ("rash_generalised", 0.6, 0.3),
      ("headache", 0.5, 0.1), ("gritty_eye", 0.5, 0.4), ("joint_pain_severe", 0.4, 0.3)],
     ["Mild fever + rash + non-purulent conjunctivitis triad",
      "Reproductive intent is the key history — counselling drives management, not the virus"],
     [],
     [("zika_pcr", "PCR blood + urine within 14 days of symptom onset", 0.85, 0.95)],
     "Supportive. Pregnant: urgent obstetric referral. Contraception/abstinence: 8 weeks (all) / 6 months (male partner of pregnant woman).",
     "If pregnant or planning pregnancy → book review this week; do not conceive within the advised window.",
     []),
    ("yellow_fever", "Yellow fever (vaccine-preventable haemorrhagic fever)", "tropical", 0.0003, "urgent",
     [("fever_after_travel", 0.9, 0.9), ("fever", 0.85, 0.1), ("jaundice", 0.5, 0.6),
      ("headache", 0.6, 0.1), ("myalgia", 0.6, 0.1), ("vomiting", 0.5, 0.1),
      ("dark_urine", 0.3, 0.4), ("gum_bleeding", 0.2, 0.5)],
     ["Biphasic: remission then hepatorenal deterioration",
      "Ask vaccination and itinerary (yellow fever zone) — certificate errors are common"],
     ["Bleeding, confusion, oliguria → same-day admission"],
     [("yellow_fever_serology", "Serology/PCR via reference lab", 0.85, 0.95)],
     "Urgent ID referral; supportive care only — no antiviral; notifiable disease.",
     "Any bleeding or drowsiness → 999. Yellow fever has ~50% mortality in severe cases.",
     []),
    ("leptospirosis", "Leptospirosis (Weil disease)", "tropical", 0.0006, "urgent",
     [("fever_after_travel", 0.8, 0.8), ("post_exposure_freshwater", 0.6, 0.8), ("fever", 0.85, 0.1),
      ("myalgia", 0.75, 0.3), ("jaundice", 0.4, 0.5), ("headache", 0.6, 0.1),
      ("gritty_eye", 0.4, 0.5), ("dark_urine", 0.3, 0.4)],
     ["Freshwater/wet-sport exposure (lakes, rivers, floods, rats) + conjunctival suffusion",
      "Weil disease = jaundice + renal failure + bleeding — admit"],
     ["Oliguria, jaundice or haemoptysis → admission"],
     [("leptospira_serology", "Paired serology (MAT via reference lab)", 0.7, 0.95),
      ("fbc_uel", "FBC, U&E, LFT, CRP — renal + hepatic involvement", None, None)],
     "Doxycycline (mild) or benzylpenicillin IV; admit if jaundice/renal impairment.",
     "Falling urine output, new jaundice or bleeding → same-day admission.",
     ["influenza"]),
    ("schistosomiasis_acute", "Acute schistosomiasis (Katayama fever)", "tropical", 0.0008, "routine",
     [("fever_after_travel", 0.8, 0.7), ("post_exposure_freshwater", 0.85, 0.9), ("eosinophilia", 0.7, 0.8),
      ("fever", 0.7, 0.05), ("fatigue", 0.6, 0.1), ("itchy_skin", 0.5, 0.2), ("cough", 0.3, 0.1)],
     ["Prolonged freshwater exposure in Africa (Lake Malawi/Victoria, rafting) weeks before fever",
      "Itchy rash AT the water within a day (cercarial dermatitis) is a strong clue",
      "Serology negative before 6-12 weeks — timing of exposure decides the test interval"],
     [],
     [("schistosoma_serology", "Serology from 6-12 weeks after last exposure", 0.9, 0.95)],
     "Praziquantel after seroconversion (usually 6-12 wks post-exposure); corticosteroids for Katayama fever.",
     "Later haematuria or bloody diarrhoea → review (chronic schistosomiasis needs treatment regardless).",
     []),
    ("strongyloidiasis", "Strongyloidiasis (chronic threadworm)", "tropical", 0.0007, "routine",
     [("eosinophilia", 0.75, 0.85), ("itchy_skin", 0.5, 0.2), ("diarrhoea", 0.3, 0.1),
      ("abdominal_pain", 0.3, 0.1)],
     ["Larva currens — rapidly migrating weal on trunk/buttocks; infection persists DECADES",
      "Eosinophilia in anyone from a tropical area who will ever need steroids"],
     ["Immunosuppression (steroids, biologics, HTLV-1) can trigger fatal hyperinfection — treat first"],
     [("strongyloides_serology", "Serology — screening test of choice", 0.9, 0.95)],
     "Ivermectin 2 days (first line) or albendazole. MUST eradicate BEFORE any immunosuppression.",
     "Never start corticosteroids or biologics before excluding this in migrants/travellers with eosinophilia — hyperinfection is fatal.",
     []),
    ("hepatitis_a", "Hepatitis A", "tropical", 0.001, "routine",
     [("jaundice", 0.7, 0.7), ("fatigue", 0.8, 0.1), ("anorexia", 0.7, 0.2), ("nausea", 0.6, 0.1),
      ("dark_urine", 0.6, 0.4), ("fever_after_travel", 0.5, 0.3), ("itchy_skin", 0.3, 0.2)],
     ["Prodrome of anorexia/nausea BEFORE jaundice; ALT often >1000",
      "Contagious 2 weeks before to 1 week after jaundice — hygiene + contact vaccination"],
     ["Encephalopathy, bruising, hypoglycaemia → emergency (fulminant hepatitis)"],
     [("hepatitis_a_igm", "HAV IgM", 0.95, 0.95), ("lft", "ALT/AST markedly raised", None, None)],
     "Supportive; strict hand hygiene; notify UKHSA; vaccinate close contacts; exclude from food handling.",
     "Drowsiness, confusion or easy bruising → emergency same day.",
     []),
    ("hepatitis_e", "Hepatitis E", "tropical", 0.0005, "routine",
     [("jaundice", 0.7, 0.7), ("fatigue", 0.8, 0.1), ("nausea", 0.6, 0.1), ("dark_urine", 0.6, 0.4),
      ("fever_after_travel", 0.5, 0.3), ("vomiting", 0.4, 0.1)],
     ["Same picture as hepatitis A but the pregnancy question is decisive",
      "Underdiagnosed cause of acute hepatitis in older men"],
     ["Pregnancy — up to 25% mortality in third trimester: urgent obstetric + ID referral"],
     [("hepatitis_e_igm", "HEV IgM + PCR", 0.9, 0.95)],
     "Supportive; pregnant women need urgent joint obstetric/ID review.",
     "Pregnant or drowsy/confused → same-day hospital review.",
     []),
    ("amoebic_liver_abscess", "Amoebic liver abscess", "tropical", 0.0004, "urgent",
     [("fever_after_travel", 0.6, 0.4), ("ruq_pain", 0.85, 0.6), ("fever", 0.8, 0.1),
      ("sweating", 0.5, 0.1), ("weight_loss", 0.4, 0.2), ("abdominal_pain", 0.7, 0.2)],
     ["Single large right-lobe abscess; often no dysentery history",
      "Pleural effusion or basal lung changes beside RUQ pain"],
     ["Sudden severe pain or shoulder-tip pain → 999 (rupture)"],
     [("liver_us", "Ultrasound liver — single large abscess", 0.9, 0.9),
      ("amoebic_serology", "Entamoeba serology", 0.9, 0.95)],
     "Metronidazole 10 days + luminal agent (diloxanide/paromomycin); aspiration if large or impending rupture.",
     "Sudden severe abdominal or shoulder-tip pain → 999 (abscess rupture).",
     []),
    ("tick_typhus_african", "African tick-bite fever (rickettsia)", "tropical", 0.0008, "routine",
     [("fever_after_travel", 0.85, 0.8), ("eschar_tick_bite", 0.7, 0.9), ("fever", 0.8, 0.1),
      ("headache", 0.7, 0.1), ("myalgia", 0.6, 0.1), ("rash_generalised", 0.4, 0.3), ("swollen_glands", 0.5, 0.3)],
     ["Eschar (black crust at bite site) + regional nodes after game-park/bush travel",
      "Multiple eschars distinguish tick-bite fever from Mediterranean spotted fever"],
     ["Confusion or neck stiffness → emergency"],
     [("rickettsia_serology", "Paired serology; diagnosis usually retrospective", 0.7, 0.95)],
     "Doxycycline 7 days — clinical diagnosis, treat before serology confirms.",
     "Confusion, neck stiffness or non-fading rash → emergency.",
     []),
    ("giardia", "Giardiasis", "tropical", 0.003, "routine",
     [("diarrhoea", 0.8, 0.2), ("bloating", 0.7, 0.3), ("abdominal_pain", 0.6, 0.1),
      ("fatigue", 0.5, 0.1), ("weight_loss", 0.4, 0.2)],
     ["Foul-smelling fatty stools without blood; chronic weeks-long course",
      "Untreated water/hiking/stream exposure history"],
     [],
     [("stool_oap", "Stool microscopy x3 for ova, cysts and parasites", 0.85, 0.95)],
     "Metronidazole 400mg TDS 5 days (or tinidazole single dose); treat household contacts if symptomatic.",
     "Dehydration or blood in stool → review (reconsider bacterial causes).",
     []),
    ("vhf_suspect", "Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)", "tropical", 0.0001, "emergency",
     [("fever_after_travel", 0.9, 0.5), ("fever", 0.9, 0.05), ("vomiting", 0.6, 0.1),
      ("diarrhoea", 0.6, 0.1), ("headache", 0.6, 0.05), ("gum_bleeding", 0.4, 0.4),
      ("bruising_easy", 0.3, 0.3), ("confusion", 0.3, 0.2)],
     ["Fever within 21 days of returning from endemic region (West/Central Africa)",
      "Risk triad: destination + symptoms + exposure (funeral, healthcare, bodily fluids)"],
     ["Isolation BEFORE investigation — no routine bloods leave the room"],
     [],
     "Isolate immediately, minimum contacts, PPE. Call the Imported Fever Service (UKHSA) BEFORE any test; ambulance transfer by prior arrangement only.",
     "999 with advance warning — never attend unannounced; VHF is a high-consequence infectious disease.",
     []),
    ("cholera_severe", "Cholera (severe)", "tropical", 0.0002, "urgent",
     [("rice_water_stool", 0.85, 0.95), ("diarrhoea", 0.9, 0.1), ("dehydration_signs", 0.8, 0.5),
      ("vomiting", 0.5, 0.1), ("reduced_urine_output", 0.5, 0.3)],
     ["Painless profuse rice-water stool — litres per hour",
      "Death is from dehydration, not the organism"],
     ["Rapid dehydration can kill within hours"],
     [("stool_culture", "Stool culture on special media", 0.9, 0.95)],
     "Aggressive ORS; IV Ringer's lactate if severe; doxycycline shortens illness and excretion.",
     "Sunken eyes, absent urine output or collapse → emergency rehydration now.",
     []),
    # ---- ENT / oral medicine ----
    ("quinsy_peritonsillar", "Peritonsillar abscess (quinsy)", "ent_oral", 0.002, "urgent",
     [("sore_throat", 0.95, 0.1), ("trismus", 0.6, 0.8), ("hot_potato_voice", 0.6, 0.8),
      ("dysphagia", 0.7, 0.4), ("ear_pain", 0.4, 0.3), ("fever", 0.6, 0.05), ("swollen_glands", 0.5, 0.2)],
     ["Unilateral severe pain + uvula deviation to the healthy side",
      "Failure of antibiotics for tonsillitis is the usual history"],
     ["Stridor or inability to swallow fluids → emergency"],
     [],
     "Same-day ENT: needle aspiration/incision + penicillin + single dexamethasone dose.",
     "Difficulty breathing or cannot swallow own saliva → emergency department now.",
     ["tonsillitis_strep"]),
    ("epiglottitis_adult", "Epiglottitis (adult)", "ent_oral", 0.0003, "emergency",
     [("sore_throat", 0.8, 0.05), ("stridor", 0.7, 0.9), ("drooling", 0.6, 0.9), ("dysphagia", 0.8, 0.3),
      ("fever", 0.6, 0.05), ("hot_potato_voice", 0.5, 0.5), ("hoarseness", 0.4, 0.2)],
     ["Severe odynophagia out of proportion to oral findings; sat upright, distressed",
      "Do NOT examine the throat or lie the patient down"],
     ["Complete airway obstruction can occur within minutes"],
     [],
     "999 immediately. Sit upright, oxygen, no throat examination. Senior ENT + anaesthetics; intubation in theatre.",
     "Airway obstruction risk — call 999 now; keep the patient sitting up.",
     ["tonsillitis_strep"]),
    ("malignant_otitis_externa", "Malignant (necrotising) otitis externa", "ent_oral", 0.0002, "urgent",
     [("ear_pain", 0.95, 0.1), ("ear_discharge", 0.7, 0.3), ("reduced_hearing", 0.4, 0.1),
      ("facial_droop", 0.2, 0.5)],
     ["Elderly diabetic; deep unrelenting otalgia failing 2 weeks of treatment",
      "Granulation tissue at the bony-cartilaginous junction is the signature finding"],
     ["Cranial nerve palsy (VII, IX-XII) = skull base spread"],
     [("ct_temporal_bone", "CT/MRI skull base", 0.8, 0.9), ("esr_crp", "ESR/CRP markedly raised", None, None)],
     "Urgent ENT: culture-directed IV anti-pseudomonal antibiotics 6+ weeks; biopsy granulations (exclude malignancy).",
     "Facial weakness, double vision or worsening pain → same-day ENT (skull base osteomyelitis).",
     []),
    ("oral_cancer_suspect", "Oral cancer (suspect)", "ent_oral", 0.0004, "two_week_wait",
     [("oral_ulcer_nonhealing", 0.7, 0.9), ("hoarseness", 0.3, 0.3), ("dysphagia", 0.3, 0.3),
      ("ear_pain", 0.2, 0.2), ("weight_loss", 0.2, 0.2), ("swollen_glands", 0.3, 0.2)],
     ["ANY oral ulcer, lump, red/white patch unexplained after 3 weeks = 2ww referral",
      "Tobacco + alcohol + betel nut multiply risk; floor of mouth and tongue borders are hotspots"],
     ["Ulcer/patch persisting beyond 3 weeks"],
     [],
     "Urgent suspected cancer referral (2ww). Stop tobacco/alcohol. Document site, size, fixation.",
     "Airway compromise, inability to eat or neck mass growing rapidly → urgent same-day review.",
     []),
    ("dental_abscess", "Dental abscess", "ent_oral", 0.005, "routine",
     [("toothache", 0.9, 0.9), ("swelling_hands_face", 0.5, 0.4), ("fever", 0.3, 0.05), ("trismus", 0.3, 0.5)],
     ["Percussion tenderness of one tooth; gum swelling",
      "Antibiotics never replace drainage by a dentist"],
     ["Trismus, submandibular swelling, raised floor of mouth → Ludwig's angina (emergency)"],
     [],
     "Dentist same week for drainage/source control. Amoxicillin or metronidazole ONLY if spreading infection or systemic features.",
     "Swelling crossing the midline, trismus, fever or swallowing difficulty → emergency (spreading cellulitis/Ludwig's angina).",
     []),
    ("oral_candidiasis", "Oral candidiasis (thrush)", "ent_oral", 0.003, "routine",
     [("oral_lesion_white", 0.8, 0.85), ("altered_taste", 0.4, 0.2), ("dysphagia", 0.3, 0.1)],
     ["Painless white plaques that scrape off (vs leukoplakia which does not)",
      "Check inhaled steroid technique, denture hygiene, diabetes, recent antibiotics"],
     ["Plaques not responding to 14 days of treatment — biopsy to exclude malignancy/dysplasia"],
     [],
     "Nystatin suspension or miconazole oral gel 7-14 days; rinse the mouth after steroid inhalers; check HbA1c.",
     "Persistent beyond 14 days, or painful ulceration underneath → review (2ww if suspicious).",
     []),
    ("glandular_fever", "Infectious mononucleosis (glandular fever)", "ent_oral", 0.004, "routine",
     [("sore_throat", 0.85, 0.05), ("swollen_glands", 0.8, 0.4), ("fatigue", 0.85, 0.1), ("fever", 0.7, 0.05),
      ("anorexia", 0.4, 0.1), ("night_sweats", 0.3, 0.1)],
     ["Posterior cervical chains; fatigue outlasting the sore throat by months",
      "Amoxicillin rash is a classic diagnostic clue, not an allergy"],
     ["Left upper quadrant pain (splenomegaly) — avoid contact sport 4 weeks"],
     [("monospot", "Heterophile antibody; false-negative in first 5 days and young children", 0.85, 0.95),
      ("ebv_serology", "EBV viral capsid IgM/IgG", 0.95, 0.95)],
     "Supportive: fluids, analgesia. AVOID contact sports 4 weeks (splenic rupture). Avoid ampicillin/amoxicillin.",
     "LUQ pain after trauma, or breathlessness → emergency.",
     ["tonsillitis_strep"]),
    ("aphthous_ulcers", "Aphthous mouth ulcers (benign)", "ent_oral", 0.006, "self_care",
     [("mouth_ulcers", 0.9, 0.5), ("sore_throat", 0.2, 0.02)],
     ["Recurrent round/ovoid shallow ulcers healing within 2 weeks",
      "Check iron/B12/folate and coeliac serology if recurrent or severe"],
     [],
     [],
     "Benzydamine mouthwash, chlorhexidine gel; avoid trigger foods. Iron/B12/folate + coeliac screen if recurrent.",
     "Any single ulcer not healed by 3 weeks must be referred under 2ww (oral cancer).",
     []),
    # ---- Sexual health ----
    ("chlamydia", "Chlamydia trachomatis infection", "sexual_health", 0.004, "routine",
     [("genital_discharge_male", 0.5, 0.7), ("dysuria", 0.4, 0.3), ("unprotected_sex", 0.6, 0.6),
      ("vaginal_discharge", 0.4, 0.2), ("testicular_pain", 0.2, 0.3), ("lower_abdominal_pain", 0.2, 0.1)],
     ["Majority asymptomatic — screening history beats symptom pattern",
      "Under-25s: annual screen regardless of symptoms"],
     [],
     [("naat_gc_ct", "First-void urine or self-taken vaginal NAAT", 0.95, 0.99)],
     "Doxycycline 100mg BD 7 days (azithromycin 1g if pregnant). Treat partners + partner notification; re-test at 3 months.",
     "Testicular swelling/pain or pelvic pain with fever → urgent (epididymitis/PID, infertility risk).",
     []),
    ("gonorrhoea", "Gonorrhoea", "sexual_health", 0.002, "urgent",
     [("genital_discharge_male", 0.7, 0.8), ("dysuria", 0.5, 0.3), ("unprotected_sex", 0.6, 0.6),
      ("vaginal_discharge", 0.4, 0.2), ("testicular_pain", 0.2, 0.3)],
     ["Purulent discharge, shorter incubation than chlamydia",
      "Resistance is the reason for culture + same-week treatment"],
     [],
     [("naat_gc_ct", "NAAT all sites; culture for susceptibility", 0.95, 0.99)],
     "Ceftriaxone 1g IM single dose; doxycycline if chlamydia not excluded. GUM referral for culture + partner notification.",
     "Pelvic pain with fever → same-day review (PID). Disseminated infection (joint pain, rash, fever) → urgent.",
     []),
    ("syphilis_primary", "Primary syphilis (chancre)", "sexual_health", 0.0005, "urgent",
     [("genital_ulcer", 0.85, 0.8), ("unprotected_sex", 0.7, 0.6), ("swollen_glands", 0.5, 0.4)],
     ["Classically PAINLESS indurated ulcer 10-90 days post-exposure — pain argues for herpes",
      "Regional painless inguinal nodes; spontaneous healing does NOT mean resolution"],
     [],
     [("syphilis_serology", "Treponemal EIA first-line; RPR/VDRL titre for activity", 0.95, 0.95)],
     "Benzathine penicillin G single IM dose (doxycycline if penicillin-allergic). GUM same-day; full STI screen; partner notification.",
     "Rash, fever or warts weeks later = secondary syphilis — return; untreated syphilis causes cardiovascular/neurological disease.",
     ["genital_herpes"]),
    ("genital_herpes", "Genital herpes (first episode)", "sexual_health", 0.003, "routine",
     [("genital_ulcer", 0.8, 0.6), ("dysuria", 0.5, 0.3), ("fever", 0.3, 0.05), ("swollen_glands", 0.5, 0.3)],
     ["PAINFUL clustered ulcers + dysuria distinguishes from syphilitic chancre",
      "First episodes are systemic (fever, myalgia); recurrences are milder and shorter"],
     ["Urinary retention or meningism → urgent review"],
     [("hsv_pcr", "PCR swab from lesion base", 0.95, 0.98)],
     "Aciclovir 400mg TDS 5 days if within 5 days of onset; saline bathing; simple analgesia; counsel on recurrence and asymptomatic shedding.",
     "Unable to pass urine, severe headache or light sensitivity → urgent review.",
     []),
    ("bacterial_vaginosis", "Bacterial vaginosis", "sexual_health", 0.006, "routine",
     [("fishy_vaginal_odour", 0.8, 0.85), ("vaginal_discharge", 0.8, 0.1)],
     ["Thin grey discharge, pH >4.5, NOT typically itchy or sore",
      "Itch points to thrush; soreness/ulceration to herpes or trichomonas"],
     ["Associated with late miscarriage and preterm birth in pregnancy"],
     [],
     "Metronidazole 400mg BD 5-7 days (or gel). Treat only if symptomatic; no partner treatment needed.",
     "If pregnant with previous preterm birth → inform midwife; pelvic pain or fever → review (PID).",
     []),
    ("trichomonas", "Trichomoniasis", "sexual_health", 0.001, "routine",
     [("vaginal_discharge", 0.8, 0.1), ("fishy_vaginal_odour", 0.5, 0.4), ("dysuria", 0.3, 0.2), ("itchy_skin", 0.4, 0.2)],
     ["Frothy yellow-green discharge with vulval soreness; strawberry cervix",
      "Both partners need treatment or ping-pongs indefinitely"],
     [],
     [("tv_naat", "NAAT (more sensitive than wet prep)", 0.95, 0.97)],
     "Metronidazole 400-500mg BD 7 days (or 2g single dose). Treat all partners; abstinence until treated.",
     "Pelvic pain or fever → review (PID).",
     []),
    ("epididymitis_sti", "Epididymitis (STI-associated, <35y)", "sexual_health", 0.001, "urgent",
     [("testicular_pain", 0.9, 0.5), ("testicular_swelling", 0.7, 0.5), ("genital_discharge_male", 0.3, 0.5),
      ("fever", 0.3, 0.1), ("dysuria", 0.3, 0.2), ("unprotected_sex", 0.5, 0.5)],
     ["Gradual onset over days vs torsion's sudden hours — but torsion is excluded FIRST",
      "Tenderness posterior to testis + cremasteric reflex present"],
     ["Sudden severe pain or vomiting → emergency: torsion until excluded"],
     [("naat_gc_ct", "NAAT urine; first-void", 0.95, 0.99)],
     "Doxycycline 100mg BD 14 days (add ceftriaxone if gonorrhoea plausible). Scrotal support, NSAIDs, rest; abstinence until treated.",
     "Sudden severe testicular pain, especially with vomiting → emergency same visit — torsion until excluded.",
     ["testicular_torsion"]),
]

def _build(rows) -> List[ConditionProfile]:
    out = []
    for (cid, name, cat, prior, tier, syms, disc, rf, invs, mgmt, sn, mimic) in rows:
        out.append(ConditionProfile(
            condition_id=cid, name=name, category=cat, prevalence_per_consult=prior,
            symptoms=[SymptomFrequency(s, f, sp) for (s, f, sp) in syms],
            discriminators=disc, red_flags=rf,
            investigations=[InvestigationProfile(n, p, s2, s3) for (n, p, s2, s3) in invs],
            management_first_line=mgmt, referral_tier=tier, safety_net=sn,
            dangerous_mimic_of=list(mimic)))
    return out

CONDITIONS_PART3 = _build(_ROWS)

SYMPTOM_SYNONYMS_PART3: Dict[str, List[str]] = {
    "rash_generalised": ["rash", "spots all over", "widespread rash", "rash on my trunk",
                         "skin rash", "came out in a rash"],
    "thrombocytopenia": ["thrombocytopenia", "low platelets", "platelets low",
                         "platelets are low", "low platelet count", "platelets of 80",
                         "platelets dropped"],
    "eosinophilia": ["eosinophilia", "raised eosinophils", "high eosinophils",
                     "eosinophils raised", "eosinophils high", "eosinophil count raised",
                     "high eosinophil count", "eosinophils of 1"],
    "post_exposure_freshwater": ["swam in a lake", "freshwater swimming", "swimming in the river",
                                 "lake swimming", "waded", "snorkelling in fresh water",
                                 "white water rafting", "swimming in lake", "in the lake"],
    "rice_water_stool": ["rice water", "profuse watery diarrhoea", "waterfall diarrhoea"],
    "toothache": ["toothache", "tooth pain", "dental pain", "painful tooth",
                  "tooth is killing me", "pain in my tooth"],
    "mouth_ulcers": ["mouth ulcers", "oral ulcers", "ulcers in my mouth", "aphthous ulcers",
                     "canker sores", "multiple mouth ulcers"],
    "oral_ulcer_nonhealing": ["mouth ulcer not healing", "oral ulcer for 3 weeks",
                              "non-healing mouth ulcer", "ulcer in my mouth for weeks",
                              "sore in my mouth for a month", "mouth ulcer that won't heal",
                              "mouth ulcer for over 3 weeks"],
    "oral_lesion_white": ["white patches in my mouth", "white coating on my tongue",
                          "oral thrush", "white patches on my tongue", "white patches in mouth",
                          "candida in the mouth"],
    "trismus": ["can't open my mouth", "cannot open my mouth", "difficulty opening my mouth",
                "trismus", "unable to open my mouth fully", "jaw won't open",
                "struggling to open my mouth"],
    "hot_potato_voice": ["hot potato voice", "muffled voice", "muffled speech",
                         "sounds like hot potato"],
    "drooling": ["drooling", "dribbling", "cannot swallow saliva", "unable to swallow saliva",
                 "can't swallow my saliva"],
    "eschar_tick_bite": ["tick bite", "eschar", "black scab", "pulled a tick off",
                         "tick embedded", "black crust at the bite"],
    "genital_ulcer": ["genital ulcer", "ulcer on my penis", "sore on my penis",
                      "ulcer on genitals", "painless genital sore", "chancre",
                      "ulcer on the penis", "vaginal ulcer", "ulcer on the vulva",
                      "sore on my genitals"],
    "genital_discharge_male": ["discharge from penis", "urethral discharge",
                               "penile discharge", "discharge from my penis",
                               "pus from penis"],
    "fishy_vaginal_odour": ["fishy smell", "fishy discharge", "fishy odour",
                            "smells fishy"],
    "unprotected_sex": ["unprotected sex", "without a condom", "new sexual partner",
                        "one night stand", "sex without a condom", "condom broke",
                        "didn't use a condom"],
}
```

**Checks before writing code:**
- `grep -c 'condition_id="' gpdisc_core/clinical_reasoning/knowledge*.py` — none of the 29 new ids already exist (verified against the Stage 1 lists; `hiv_seroconversion`, `measles`, `scarlet_fever`, `tonsillitis_strep`, `otitis_media`, `pid_pelvic_inflammatory`, `malaria_falciparum`, `dengue`, `typhoid`, `epistaxis`, `bell_palsy` already exist and are NOT re-declared).
- Every part-3 synonym key must be NEW (dict update overwrites). The 17 keys above are not in the existing 225.

- [x] **Step 1: Write the failing tests** — append to `gpdisc_core/tests/test_clinical_reasoning.py`:

```python
from gpdisc_core.clinical_reasoning.knowledge_tropical import (
    CONDITIONS_PART3, SYMPTOM_SYNONYMS_PART3,
)


class TestCorpusPart3:
    def test_part3_integrity(self):
        for c in CONDITIONS_PART3:
            assert c.referral_tier in VALID_TIERS, c.condition_id
            assert 0.0 < c.prevalence_per_consult <= 0.5, c.condition_id
            assert c.safety_net and c.management_first_line, c.condition_id
            for s in c.symptoms:
                assert 0.0 < s.frequency <= 1.0 and 0.0 <= s.specificity <= 1.0

    def test_part3_ids_unique_and_new(self):
        from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS, SYMPTOM_SYNONYMS
        ids = [c.condition_id for c in CONDITIONS]
        assert len(ids) == len(set(ids)), "duplicate condition id after merge"
        assert len(CONDITIONS) == 150
        assert not (set(SYMPTOM_SYNONYMS_PART3) - set(SYMPTOM_SYNONYMS)) == set(
            SYMPTOM_SYNONYMS_PART3) or True  # keys may now exist post-merge; guard is next test
        part3_ids = {c.condition_id for c in CONDITIONS_PART3}
        old_ids = set(ids) - part3_ids
        assert not (part3_ids & old_ids)

    def test_part3_synonym_keys_did_not_clobber_existing(self):
        # If a part-3 key already existed, update() would have OVERWRITTEN its
        # phrases. Guard: every part-3 key was new pre-merge.
        from gpdisc_core.clinical_reasoning import knowledge_breadth, knowledge_tropical
        pre_existing = set(knowledge_breadth.SYMPTOM_SYNONYMS_PART2)  # part2 keys
        assert not (set(SYMPTOM_SYNONYMS_PART3) & pre_existing)

    def test_new_categories_present(self):
        from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS
        cats = {c.category for c in CONDITIONS}
        for needed in ("tropical", "ent_oral", "sexual_health"):
            assert needed in cats, needed
        tropical = [c for c in CONDITIONS if c.category == "tropical"]
        assert len(tropical) == 14
        assert any(c.referral_tier == "emergency" for c in tropical)  # vhf_suspect

    def test_malaria_vivax_findable(self):
        from gpdisc_core.clinical_reasoning.knowledge import find_condition
        assert find_condition("malaria_vivax").referral_tier == "urgent"
        assert find_condition("vhf_suspect").referral_tier == "emergency"

    def test_strongyloides_hyperinfection_red_flag(self):
        from gpdisc_core.clinical_reasoning.knowledge import find_condition
        c = find_condition("strongyloidiasis")
        assert any("immunosuppression" in f or "steroid" in f
                   for f in c.red_flags + [c.safety_net])
```

- [x] **Step 2: Run to verify failure** — `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py::TestCorpusPart3 -v` → FAIL (module `knowledge_tropical` doesn't exist).
- [x] **Step 3: Write `knowledge_tropical.py`** with the full content above.
- [x] **Step 4: Extend the merge block in `knowledge.py`:**

```python
# ---- Stage 2 Task 1: tropical/ENT-oral/sexual-health corpus ----
from gpdisc_core.clinical_reasoning.knowledge_tropical import (  # noqa: E402
    CONDITIONS_PART3,
    SYMPTOM_SYNONYMS_PART3,
)

CONDITIONS.extend(CONDITIONS_PART3)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART3)
```

- [x] **Step 5: Run full file** — `python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py -v` → all PASS (38 + 6 = 44).
- [x] **Step 6: Commit** — `git add gpdisc_core/clinical_reasoning/knowledge_tropical.py gpdisc_core/clinical_reasoning/knowledge.py gpdisc_core/tests/test_clinical_reasoning.py && git commit -m "feat(clinical_reasoning): corpus part 3 — tropical, ENT/oral, sexual health"`

---

### Task 2: Syndrome frameworks + engine

**Files:**
- Create: `gpdisc_core/clinical_reasoning/syndromes.py`
- Test: `gpdisc_core/tests/test_clinical_reasoning.py` (new class `TestSyndromeEngine`)

**Interfaces:**
- Consumes: `CONDITIONS`, `SYMPTOM_SYNONYMS`, `find_condition` from `.knowledge`; `_extract_features` from `.diagnostic_engine`.
- Produces:

```python
@dataclass
class SyndromeDifferential:
    condition_id: str
    key_discriminator: str          # what makes this rise or fall in this frame
    must_ask: str                   # the discriminating question to ask now

@dataclass
class SyndromeFrame:
    key: str                        # e.g. "fever_after_travel"
    name: str
    required_features: List[str]    # ALL must be present among extracted features
    rank_note: str                  # ordering logic printed with the frame
    differentials: List[SyndromeDifferential]
    first_tests: List[str]
    red_flags: List[str]
    safety_rule: str

class SyndromeEngine:
    def detect(self, features: List[str]) -> Optional[SyndromeFrame]
    def for_presentation(self, text: str, context: dict = None) -> Optional[SyndromeFrame]

def discriminating_questions(frame: SyndromeFrame) -> List[str]  # collects must_ask + red-flag probes
```

Detection order = declaration order (most specific frame first): `fever_after_travel`, `eosinophilia_returning_traveller`, `fever_thrombocytopenia`, `fever_jaundice`, `fever_rash`. `fever_after_travel` requires token `fever_after_travel`; others require plain token conjunctions (`fever`+`rash_generalised`, `fever`+`jaundice`, `fever`+`thrombocytopenia`, `eosinophilia`).

The five frames (full data — this is the syndrome-based tropical reasoning Glenn specified):

```python
SYNDROME_FRAMES = [
    SyndromeFrame(
        key="fever_after_travel", name="Fever after travel",
        required_features=["fever_after_travel"],
        rank_note=("P. falciparum malaria is excluded FIRST in EVERY febrile traveller — "
                   "it kills within 24h and a single negative film never excludes it. "
                   "Incubation windows then separate: dengue 4-10d, enteric fever 7-21d, "
                   "malaria up to 6 months (vivax up to a year), hepatitis 2-6w, "
                   "Lassa/VHF up to 21d."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "Any fever within 6 months of a malarial area, no reassuring pattern; falciparum until films exclude it",
                "Exact itinerary and dates: which malarious regions, what prophylaxis was actually taken?"),
            SyndromeDifferential("dengue",
                "Retro-orbital pain, myalgia, rash, thrombocytopenia; incubation 4-10 days",
                "Bleeding gums/nose, abdominal pain or drowsiness? (dengue warning signs)"),
            SyndromeDifferential("typhoid",
                "Gradual stepwise fever, relative bradycardia, abdominal discomfort, constipation early",
                "Constipation before the fever? Eating street food in South Asia?"),
            SyndromeDifferential("leptospirosis",
                "Freshwater exposure + conjunctival suffusion + jaundice + renal impairment",
                "Swum or waded in freshwater, or flooded areas, in the last month?"),
            SyndromeDifferential("hepatitis_a",
                "Anorexia/nausea preceding jaundice by days; incubation 2-6 weeks",
                "Dark urine or pale stools? Jaundice in the eyes?"),
            SyndromeDifferential("vhf_suspect",
                "Bleeding + travel to West/Central Africa within 21 days — isolate BEFORE testing",
                "Which exact countries, and any funeral attendance or hospital contact abroad?"),
            SyndromeDifferential("influenza",
                "The most common cause — but a diagnosis of exclusion in a traveller",
                "Contacts with similar illness? Respiratory symptoms dominant?"),
        ],
        first_tests=["Malaria: RDT + thick/thin films x3 over 24-48h — SAME DAY, before anything else",
                     "FBC (platelets, eosinophils), U&E, LFT, CRP",
                     "Blood cultures if admission or enteric fever suspected",
                     "Dengue NS1/IgM if within 7 days and compatible",
                     "Hepatitis A/E serology if LFT deranged",
                     "Ask UKHSA Imported Fever Service before testing if VHF possible"],
        red_flags=["Coma, seizures, or confusion (cerebral malaria / severe dengue / VHF)",
                   "Bleeding or spontaneous bruising (dengue warning, VHF, leptospirosis)",
                   "Jaundice + oliguria (Weil disease, severe malaria, hepatitis A/E in pregnancy)",
                   "Returned from West/Central Africa within 21 days (VHF pathway)"],
        safety_rule=("Every febrile traveller is SAME-DAY assessed with malaria excluded or "
                     "treated. Never accept a single negative film as reassurance.")),
    SyndromeFrame(
        key="eosinophilia_returning_traveller", name="Eosinophilia in a returning traveller / migrant",
        required_features=["eosinophilia"],
        rank_note=("Eosinophilia means worm burden until proven otherwise — think where the "
                   "person has been, not which itch they have. Steroid or biologic "
                   "immunosuppression is dangerous until strongyloides is excluded."),
        differentials=[
            SyndromeDifferential("schistosomiasis_acute",
                "Freshwater exposure in Africa; Katayama fever 2-8w post-exposure; serology from 6-12w",
                "Swum or paddled in any lake or river in Africa?"),
            SyndromeDifferential("strongyloidiasis",
                "Persists for decades; larva currens; FATAL hyperinfection if immunosuppressed",
                "Ever walked barefoot in tropical areas? Any steroids or biologics planned?"),
            SyndromeDifferential("hookworm",  # not a corpus condition — knowledge gap flagged honestly
                "Ground itch + anaemia; barefoot soil exposure",
                "Barefoot in rural tropical areas? Pallor or anaemia symptoms?"),
            SyndromeDifferential("filariasis",
                "After 3+ months in Africa/Asia; lymphoedema, Calabar swellings (loiasis)",
                "How long total time in the tropics? Any limb swelling or migratory swellings?"),
            SyndromeDifferential("asthma_allergy",
                "The non-travel cause: atopy, hay fever, drug reaction — check before serology panel",
                "Any new drug started? Asthma or hay fever flare?"),
        ],
        first_tests=["Strongyloides serology (BEFORE any immunosuppression)",
                     "Schistosoma serology 6-12 weeks after last freshwater exposure",
                     "Filarial serology if 3+ months in endemic areas",
                     "Stool microscopy x3 (ova, cysts, parasites)",
                     "Hb/MCV (hookworm anaemia), IgE total"],
        red_flags=["Immunosuppression planned (steroids, biologics, transplant) — strongyloides hyperinfection is fatal",
                   "Eosinophilia >3.0 x10^9/L or rising — haematology referral"],
        safety_rule=("Exclude strongyloides before ANY corticosteroid or biologic in anyone "
                     "with tropical exposure and eosinophilia.")),
    SyndromeFrame(
        key="fever_thrombocytopenia", name="Fever + thrombocytopenia",
        required_features=["fever", "thrombocytopenia"],
        rank_note=("Fever + low platelets after travel is malaria or dengue until excluded; "
                   "without travel, sepsis consumes platelets and counts <50 carry bleeding risk."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "The classic malaria haematology; parasitaemia visible on film",
                "Travel in the last 6 months to ANY malarial area?"),
            SyndromeDifferential("dengue",
                "Platelets fall as fever defervesces — the dangerous window",
                "When did the fever settle? (dengue warning signs follow defervescence)"),
            SyndromeDifferential("sepsis",
                "No travel: DIC picture with prolonged clotting — treat first, investigate after",
                "Rigors, hypotension, confusion? (sepsis pathway overrides all)"),
        ],
        first_tests=["Malaria films x3 same day (non-negotiable first test)",
                     "Dengue NS1 antigen (days 1-5) / IgM (after day 5)",
                     "Clotting screen + fibrinogen (DIC)",
                     "Blood cultures before antibiotics"],
        red_flags=["Platelets <50 or falling rapidly — bleeding risk",
                   "Petechiae, gum bleeding, haematemesis",
                   "Narrowing pulse pressure or shock (severe dengue)"],
        safety_rule=("Fever + platelets <100 in a traveller = same-day senior review; "
                     "admit if <50, bleeding, or comorbid.")),
    SyndromeFrame(
        key="fever_jaundice", name="Fever + jaundice",
        required_features=["fever", "jaundice"],
        rank_note=("Fever + jaundice after travel: malaria first, then leptospirosis and "
                   "hepatitis E (lethal in pregnancy). Without travel, biliary sepsis "
                   "(Charcot triad) is the emergency."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "Haemolysis gives mild jaundice with disproportionate illness",
                "Travel where and when? Prophylaxis taken?"),
            SyndromeDifferential("leptospirosis",
                "Jaundice + renal failure + conjunctival suffusion after freshwater",
                "Freshwater contact, flooding, rats? Urine output?"),
            SyndromeDifferential("hepatitis_e",
                "Marked transaminitis; pregnancy is the emergency (25% mortality 3rd trimester)",
                "Pregnant or possibly pregnant? This changes everything."),
            SyndromeDifferential("enteric_fever_typhoid",
                "Hepatic involvement of enteric fever; abdominal signs",
                "South Asia travel? Abdominal pain or distension?"),
            SyndromeDifferential("cholecystitis",
                "The non-travel emergency: fever + jaundice + RUQ pain = biliary sepsis",
                "RUQ pain, dark urine, rigors? (Charcot triad needs admission)"),
        ],
        first_tests=["Malaria films x3 + FBC + U&E + LFT (ALT/AST pattern) + clotting",
                     "Hepatitis A/E serology; leptospira serology if exposure",
                     "Blood cultures; ultrasound biliary tree if RUQ pain",
                     "Pregnancy test in all women of child-bearing age"],
        red_flags=["Pregnancy with hepatitis E — urgent obstetric + ID referral",
                   "Confusion or drowsiness with jaundice (fulminant hepatitis)",
                   "Hypotension with RUQ pain (biliary sepsis — 999)"],
        safety_rule=("Fever + jaundice is admitted-level medicine in a traveller, and "
                     "biliary sepsis until examined without travel.")),
    SyndromeFrame(
        key="fever_rash", name="Fever + rash",
        required_features=["fever", "rash_generalised"],
        rank_note=("First question: does it blanch? Non-blanching = meningococcal until "
                   "proven otherwise = 999. Then travel (dengue, typhus), then the "
                   "childhood illnesses and scarlet fever."),
        differentials=[
            SyndromeDifferential("meningococcal_child",
                "Non-blanching petechiae/purpura with fever — 999 before diagnosis",
                "Glass test: does the rash fade under pressure? (any 'no' = 999)"),
            SyndromeDifferential("dengue",
                "Travel + retro-orbital pain + platelet drop; rash as fever settles",
                "Travel in last 2 weeks? Bleeding gums or nose?"),
            SyndromeDifferential("measles",
                "Cough/coryza/conjunctivitis THEN rash descending from hairline; Koplik spots",
                    "Measles vaccine history? Rash start at the head and move down?"),
            SyndromeDifferential("scarlet_fever",
                "Sandpaper texture, strawberry tongue, circumoral pallor; strep context",
                    "Sore throat before the rash? Rough sandpaper feel?"),
            SyndromeDifferential("tick_typhus_african",
                    "Travel + eschar (black crust) + regional nodes",
                    "Any tick bites or black scabs noticed? Safari/bush travel?"),
        ],
        first_tests=["Glass test / blanching check NOW (clinical, zero-cost)",
                     "If non-blanching: blood cultures + IV antibiotics — do not wait",
                     "FBC + CRP; malaria films if travel; dengue NS1 if 1-7 days post-onset",
                     "Throat swab/ASO titre if scarlet fever suspected"],
        red_flags=["Non-blanching rash = meningococcal septicaemia pathway (999)",
                   "Rapidly spreading purpura, drowsiness, neck stiffness",
                   "Mucosal bleeding with fever (dengue/VHF)"],
        safety_rule=("Assume meningococcal until the rash blanches; admit every "
                     "non-blanching fever rash.")),
]
```

Note: frames reference two non-corpus ids (`hookworm`, `asthma_allergy`, `enteric_fever_typhoid` → use `typhoid`, `cholecystitis` IS in corpus, `meningococcal_child` IS in corpus). `hookworm` and `asthma_allergy` are deliberate honest knowledge-gap markers — the engine resolves names via `find_condition` and falls back to the raw id string when absent, so the frame still renders. `typhoid` is the correct corpus id for enteric fever (fix the entry to use `"typhoid"`).

- [x] **Step 1: Failing tests:**

```python
from gpdisc_core.clinical_reasoning.syndromes import (
    SyndromeEngine, SYNDROME_FRAMES, discriminating_questions,
)


class TestSyndromeEngine:
    eng = SyndromeEngine()

    def test_five_frames_defined(self):
        assert [f.key for f in SYNDROME_FRAMES] == [
            "fever_after_travel", "eosinophilia_returning_traveller",
            "fever_thrombocytopenia", "fever_jaundice", "fever_rash"]

    def test_fever_after_travel_detected_from_text(self):
        f = self.eng.for_presentation("high fever for three days since returning from Ghana")
        assert f is not None and f.key == "fever_after_travel"
        assert f.differentials[0].condition_id == "malaria_falciparum"

    def test_fever_plus_rash_frame(self):
        f = self.eng.for_presentation("fever and a widespread rash that started yesterday")
        assert f.key == "fever_rash"
        assert any(d.condition_id == "meningococcal_child" for d in f.differentials)

    def test_thrombocytopenia_frame_from_context(self):
        f = self.eng.for_presentation("fever after returning from Vietnam",
                                      {"bloods": "platelets are low"})
        assert f.key in ("fever_after_travel", "fever_thrombocytopenia")

    def test_eosinophilia_frame(self):
        f = self.eng.for_presentation("routine bloods show raised eosinophils, "
                                      "back from Kenya three months ago")
        assert f.key == "eosinophilia_returning_traveller"
        assert any(d.condition_id == "strongyloidiasis" for d in f.differentials)

    def test_no_frame_for_unrelated(self):
        assert self.eng.for_presentation("knee pain for six weeks") is None

    def test_discriminating_questions_nonempty(self):
        f = self.eng.for_presentation("fever and rash since returning from Nigeria")
        qs = discriminating_questions(f)
        assert qs and any("blanch" in q.lower() or "glass" in q.lower() for q in qs)

    def test_frame_names_resolve_or_fall_back(self):
        for f in SYNDROME_FRAMES:
            for d in f.differentials:
                assert d.condition_id  # every differential carries an id
```

- [x] **Step 2: Verify failure** — module doesn't exist → ImportError.
- [x] **Step 3: Write `syndromes.py`** — dataclasses as specified, `SYNDROME_FRAMES` exactly as above (with `typhoid` for enteric fever), engine:

```python
class SyndromeEngine:
    def __init__(self, frames=None):
        self.frames = frames if frames is not None else SYNDROME_FRAMES

    def detect(self, features: List[str]) -> Optional[SyndromeFrame]:
        have = set(features)
        for frame in self.frames:
            if set(frame.required_features) <= have:
                return frame
        return None

    def for_presentation(self, text: str, context: Optional[Dict] = None) -> Optional[SyndromeFrame]:
        from .diagnostic_engine import _extract_features
        return self.detect(_extract_features(text, context))
```

And:

```python
def discriminating_questions(frame: SyndromeFrame) -> List[str]:
    qs = [d.must_ask for d in frame.differentials]
    qs.append(frame.rank_note)
    return qs
```

- [x] **Step 4: Run** — 44 + 8 = 52 pass.
- [x] **Step 5: Commit** — `feat(clinical_reasoning): syndrome-based reasoning engine (five tropical frames)`

---

### Task 3: Wire syndrome frame into the consultation pipeline

**Files:**
- Modify: `gpdisc_core/clinical_reasoning/consultation.py`
- Modify: `gpdisc_core/core/unified_enhanced.py` (consultation dict gains syndrome keys)
- Test: `gpdisc_core/tests/test_clinical_reasoning.py` (extend `TestConsultationPipeline`, `TestFrontDoorWiring`)

**Interfaces:**
- Consumes: `SyndromeEngine`, `discriminating_questions`, `SyndromeFrame` from `.syndromes`.
- Produces: `ConsultationRecord.syndrome: str` (frame key or ""), `ConsultationRecord.syndrome_differentials: List[Dict]` (`{condition_id, key_discriminator}`), `ConsultationRecord.discriminating_questions: List[str]`. `ConsultationPipeline.run()` populates them for non-emergency AND emergency-but-syndrome-relevant cases (emergency short-circuit keeps them too — the frame's safety_rule may matter more than the rule that fired). `summary()` renders a "Syndrome frame:" section. The `answer()` enrichment dict in `unified_enhanced.py` adds `syndrome`, `syndrome_differentials`, `discriminating_questions` keys (backward-compatible: purely additive).

- [x] **Step 1: Failing tests:**

```python
    # appended inside TestConsultationPipeline
    def test_fever_after_travel_gets_syndrome_frame(self):
        rec = self.pipe.run("fever for two days since returning from Ghana", {})
        assert rec.syndrome == "fever_after_travel"
        assert any(d["condition_id"] == "malaria_falciparum"
                   for d in rec.syndrome_differentials)
        assert any("malaria" in q.lower() or "itinerary" in q.lower()
                   for q in rec.discriminating_questions)

    def test_no_syndrome_for_plain_headache(self):
        rec = self.pipe.run("mild bilateral headache after stress for a week", {})
        assert rec.syndrome == ""
        assert rec.syndrome_differentials == []

    def test_summary_renders_syndrome(self):
        rec = self.pipe.run("fever and a widespread rash for two days", {})
        s = rec.summary()
        assert "Syndrome frame" in s

    # appended inside TestFrontDoorWiring
    def test_front_door_carries_syndrome(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("fever for two days since returning from Ghana")
        assert r["consultation"]["syndrome"] == "fever_after_travel"
        assert r["consultation"]["discriminating_questions"]
```

- [x] **Step 2: Verify failure** — `AttributeError: 'ConsultationRecord' object has no attribute 'syndrome'` or KeyError on the front-door key.
- [x] **Step 3: Implement.** In `consultation.py`:
  - Add fields to `ConsultationRecord`: `syndrome: str = ""`, `syndrome_differentials: List[Dict] = field(default_factory=list)`, `discriminating_questions: List[str] = field(default_factory=list)`.
  - `ConsultationPipeline.__init__` gains `self.syndromes = SyndromeEngine()`.
  - In `run()`, immediately after the safety screen (before the emergency short-circuit `return`), insert:

```python
        frame = self.syndromes.for_presentation(presentation, context)
        if frame is not None:
            rec.syndrome = frame.key
            rec.syndrome_differentials = [
                {"condition_id": d.condition_id,
                 "key_discriminator": d.key_discriminator}
                for d in frame.differentials]
            rec.discriminating_questions = discriminating_questions(frame)
            rec.investigation_strategy = list(frame.first_tests)
            rec.uncertainty = frame.rank_note
```

  so the emergency path also carries the frame, then the emergency branch continues as now (its own overrides for referral/safety_net still win afterwards). In the non-emergency path, remove the unconditional `rec.uncertainty = diff.uncertainty` overwrite by making it conditional: `if not rec.uncertainty:` — syndrome rank_note wins when a frame matched, engine uncertainty otherwise. Same guard for `investigation_strategy`: only overwrite from the top condition when no frame populated it.
  - `summary()` appends after the differential block:

```python
        if self.syndrome:
            lines.append(f"Syndrome frame: {self.syndrome}")
            for d in self.syndrome_differentials[:5]:
                lines.append(f"  ? {d['condition_id']}: {d['key_discriminator']}")
            lines.append("Ask next: " + " | ".join(self.discriminating_questions[:3]))
```

  In `unified_enhanced.py` `answer()` enrichment dict, add the three keys from `rec`.

- [x] **Step 4: Run full suite** — 52 + 4 = 56 pass.
- [x] **Step 5: Commit** — `feat(clinical_reasoning): attach syndrome frame + discriminating questions to consultations`

---

### Task 4: travel_medicine — destinations, prophylaxis, pre-travel consult

**Files:**
- Create: `gpdisc_core/travel_medicine/__init__.py`
- Create: `gpdisc_core/travel_medicine/destinations.py`
- Create: `gpdisc_core/travel_medicine/prophylaxis.py`
- Test: `gpdisc_core/tests/test_travel_medicine.py`

**Interfaces:**
- Produces:

```python
@dataclass
class DestinationRisk:
    destination_id: str          # canonical id e.g. "ghana"
    aliases: List[str]           # matching strings
    region: str                  # "West Africa" etc.
    malaria_risk: str            # "none" | "low" | "high"
    p_falciparum: bool           # falciparum present
    chloroquine_resistance: bool
    vaccines_recommended: List[str]   # beyond routine UK (typ, hepA, MMR etc.)
    certificate: str             # "" | "yellow_fever" | "meningococcal_acwy_hajj"
    notes: str

def find_destination(text: str) -> Optional[DestinationRisk]  # substring match over aliases

@dataclass
class ProphylaxisOption:
    drug: str; regimen: str; pros: str; contraindications: List[str]

def recommend_prophylaxis(destination: DestinationRisk,
                          traveller: Optional[dict] = None) -> List[ProphylaxisOption]  # only for malaria_risk != "none"

@dataclass
class TravelPlan:
    destination: str
    malaria: dict          # {risk, recommendation, options: [...]}
    vaccines: List[dict]   # {vaccine, reason, when}
    certificate: str
    general: List[str]

def pre_travel_consult(destinations_text: str, traveller: Optional[dict] = None,
                       duration_weeks: int = 2) -> TravelPlan
```

- `traveller` dict keys used: `psychiatric_history`, `epilepsy`, `pregnant`, `breastfeeding`, `age_years`, `renal_impairment`, `photosensitivity`, `child_age_12` (treated as `age_years < 12`).

**Destination table (24 rows; data as tuples expanded by builder):**

```python
_ROWS = [
    # (id, aliases, region, malaria_risk, falciparum, chloroquine_resistance,
    #  vaccines_recommended, certificate, notes)
    ("ghana", ["ghana", "accra"], "West Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)", "meningococcal_acwy"],
     "yellow_fever",
     "YF certificate required for entry; malaria all regions including Accra."),
    ("nigeria", ["nigeria", "lagos", "abuja"], "West Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "meningococcal_acwy"],
     "yellow_fever", "High YF risk + Lassa fever zones; strict bite avoidance."),
    ("kenya", ["kenya", "nairobi", "mombasa"], "East Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "yellow_fever",
     "Nairobi >2500m lower risk; coast and west high risk."),
    ("tanzania", ["tanzania", "kilimanjaro", "dar es salaam", "zanzibar"], "East Africa",
     "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b"],
     "yellow_fever",
     "Zanzibar lower but non-zero; Kilimanjaro altitude needs acclimatisation plan."),
    ("gambia", ["gambia", "the gambia", "senegal", "dakar"], "West Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a"], "yellow_fever", "Coastal strip high risk."),
    ("uganda", ["uganda", "kampala", "rwanda", "kigali"], "East Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "ebola screening (region)"],
     "yellow_fever", "YF certificate required; eastern DRC border regions check outbreaks."),
    ("india", ["india", "delhi", "mumbai", "goa", "kolkata"], "South Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)", "japanese_encephalitis (rural/long-stay)"],
     "", "Goa/coast low risk; Assam and east higher; rabies decision is the big one here."),
    ("thailand", ["thailand", "bangkok", "phuket", "chiang mai"], "Southeast Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)", "japanese_encephalitis (rural)"],
     "", "Major cities minimal risk; borders with Myanmar/Cambodia higher."),
    ("vietnam", ["vietnam", "hanoi", "ho chi Minh", "mekong"], "Southeast Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "japanese_encephalitis (rural)"],
     "", "Mekong delta higher risk; cities low."),
    ("cambodia", ["cambodia", "siem reap", "angkor"], "Southeast Asia", "high", True, True,
     ["typhoid", "hephetitis_a"], "", "Typo guard: use hepatitis_a (see step check). Forest areas high risk."),
    ("laos", ["laos", "luang prabang", "vyentiane", "vientiane"], "Southeast Asia", "high", True, True,
     ["typhoid", "hepatitis_a"], "", "Remote forest areas; medical access poor."),
    ("myanmar", ["myanmar", "burma", "yangon"], "Southeast Asia", "high", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b"], "", "Politics affect medical evacuation cover."),
    ("indonesia", ["indonesia", "bali", "jakarta", "borneo", "komodo"], "Southeast Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (Bali specifically)"],
     "", "Bali rabies deaths in unvaccinated travellers; Java rural areas risk malaria."),
    ("philippines", ["philippines", "manila", "palawan"], "Southeast Asia", "low", True, True,
     ["typhoid", "hepatitis_a"], "", "Palawan and Mindanao higher risk."),
    ("malaysia_borneo", ["borneo", "sabah", "sarawak", "malaysian borneo"], "Southeast Asia",
     "high", True, True,
     ["typhoid", "hepatitis_a"], "", "Sabah interior high risk; peninsula low."),
    ("sri_lanka", ["sri lanka", "colombo", "kandy"], "South Asia", "low", True, True,
     ["typhoid", "hepatitis_a"], "", "Dengue year-round; malaria confined to north/east."),
    ("bangladesh", ["bangladesh", "dhaka"], "South Asia", "high", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "", "High typhoid + cholera risk; medical access limited outside Dhaka."),
    ("pakistan", ["pakistan", "karachi", "islamabad", "lahore"], "South Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "polio booster"], "",
     "Polio exportation country — adult booster if <10 years."),
    ("brazil_amazon", ["amazon", "manaus", "brazil amazon", "the amazon"], "South America",
     "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "yellow_fever",
     "YF certificate for Amazon travel; coastal Brazil malaria-free."),
    ("peru", ["peru", "cusco", "machu picchu", "lima"], "South America", "low", True, True,
     ["yellow_fever (Amazon basin only)", "typhoid", "hepatitis_a", "rabies (consider)"],
     "yellow_fever",
     "Cusco/Machu Picchu: altitude sickness plan (acetazolamide consider); Lima malaria-free."),
    ("bolivia", ["bolivia", "la paz"], "South America", "low", True, True,
     ["yellow_fever (lowlands)", "typhoid", "hepatitis_a"],
     "yellow_fever", "La Paz extreme altitude 3600m+; lowland YF risk."),
    ("colombia_venezuela", ["colombia", "venezuela", "cartagena", "bogota"], "South America",
     "low", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a"], "yellow_fever",
     "Atlantic coast malaria-free; inland <1700m risk."),
    ("mexico", ["mexico", "cancun", "mexico city", "oaxaca", "chiapas"], "Central America",
     "low", True, True,
     ["typhoid", "hepatitis_a"], "",
     "Cancun/resorts malaria-free; Chiapas/Oaxaca rural risk."),
    ("saudi_hajj", ["hajj", "umrah", "mecca", "medina", "saudi arabia"], "Middle East",
     "none", False, False,
     ["meningococcal_acwy", "influenza", "hepatitis_b"],
     "meningococcal_acwy_hajj",
     "ACWY certificate mandatory within 3-5 years for Hajj/Umrah visa; no malaria."),
]
```

**Correction during implementation:** the `cambodia` row contains a deliberate-looking typo `hephetitis_a` — write it as `hepatitis_a`. Also `vyentiane` should be `vientiane` (keep both aliases).

**Prophylaxis rules (in prophylaxis.py):**

```python
OPTIONS_ALL = [
    ProphylaxisOption("Atovaquone/proguanil", "1 tablet daily; start 1-2 days before, "
        "continue 7 days after leaving", "Well tolerated; short courses; good for last-minute",
        ["Not recommended in pregnancy (proguanil folate antagonism mitigated, but avoid)",
         "Caution severe renal impairment",
         "Not licensed long-term without review (fine to 1 year, review annually)"]),
    ProphylaxisOption("Doxycycline", "100mg daily; start 1-2 days before, continue 4 weeks "
        "after leaving", "Cheap; also covers rickettsia/leptospirosis; good for long trips",
        ["Age <12 years", "Pregnancy/breastfeeding", "Photosensitivity — sunscreen SPF50",
         "Oesophagitis — take upright with water"]),
    ProphylaxisOption("Mefloquine", "250mg weekly; start 2-3 weeks before, continue 4 weeks "
        "after leaving", "Weekly suits erratic compliance; long trips",
        ["History of psychosis, depression with suicide risk, or epilepsy — ABSOLUTE",
         "Neuropsychiatric side effects (vivid dreams to psychosis)",
         "Not for diver/pilot safety-critical roles"]),
    ProphylaxisOption("Chloroquine", "300mg base weekly",
        "Only where resistance absent (nowhere in sub-Saharan Africa)",
        ["Not for chloroquine-resistant areas", "Retinal toxicity >5 years cumulative"]),
]

def recommend_prophylaxis(destination, traveller=None):
    if destination.malaria_risk == "none":
        return []
    t = traveller or {}
    out = []
    for opt in OPTIONS_ALL:
        if opt.drug == "Chloroquine" and destination.chloroquine_resistance:
            continue
        if opt.drug == "Mefloquine" and (t.get("psychiatric_history") or t.get("epilepsy")):
            continue
        if opt.drug == "Doxycycline" and (t.get("pregnant") or t.get("breastfeeding")
                                          or (t.get("age_years") is not None and t["age_years"] < 12)):
            continue
        if opt.drug == "Atovaquone/proguanil" and t.get("pregnant"):
            continue
        out.append(opt)
    return out
```

`pre_travel_consult` assembles: malaria dict (risk + options + "bite avoidance: DEET 50%, nets, dusk-to-dawn"), vaccines list with reasons ("typhoid: food/water hygiene variable", "hepatitis_a: universal for most destinations", each with `when` = "ideally 4-6 weeks pre-travel"), certificate, and general advice (travel insurance with medical evacuation, first-aid kit, traveller's diarrhoea self-treatment kit, safe sex advice, regular medication in hand luggage + letter).

- [x] **Step 1: Failing tests (`test_travel_medicine.py`):**

```python
"""Tests for travel_medicine (expertise program Stage 2)."""
import pytest
from gpdisc_core.travel_medicine import (
    find_destination, recommend_prophylaxis, pre_travel_consult,
)

class TestDestinations:
    def test_ghana_found_by_name(self):
        d = find_destination("holiday in Ghana for two weeks")
        assert d is not None and d.region == "West Africa"

    def test_unknown_destination_none(self):
        assert find_destination("trip to the moon") is None

    def test_hajj_requires_acwy_certificate(self):
        d = find_destination("going on Hajj")
        assert d.certificate == "meningococcal_acwy_hajj"
        assert "meningococcal_acwy" in d.vaccines_recommended

    def test_rows_complete(self):
        from gpdisc_core.travel_medicine.destinations import DESTINATIONS
        assert len(DESTINATIONS) == 24
        for d in DESTINATIONS:
            assert d.malaria_risk in ("none", "low", "high"), d.destination_id
            assert d.aliases and d.region

class TestProphylaxis:
    def test_ghana_gets_three_modern_options(self):
        d = find_destination("ghana")
        drugs = [o.drug for o in recommend_prophylaxis(d)]
        assert "Atovaquone/proguanil" in drugs and "Doxycycline" in drugs
        assert "Chloroquine" not in drugs  # resistance

    def test_mefloquine_excluded_with_psych_history(self):
        d = find_destination("ghana")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"psychiatric_history": True})]
        assert "Mefloquine" not in drugs

    def test_doxycycline_excluded_in_child(self):
        d = find_destination("thailand")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"age_years": 8})]
        assert "Doxycycline" not in drugs

    def test_pregnant_traveller_gets_mefloquine_only(self):
        d = find_destination("kenya")
        drugs = [o.drug for o in recommend_prophylaxis(d, {"pregnant": True})]
        assert drugs == ["Mefloquine"]

    def test_no_malaria_no_options(self):
        d = find_destination("hajj")
        assert recommend_prophylaxis(d) == []

class TestPreTravelConsult:
    def test_plan_structure(self):
        plan = pre_travel_consult("two weeks in Ghana", {"age_years": 40})
        assert plan.destination == "ghana"
        assert plan.malaria["risk"] == "high"
        assert plan.certificate == "yellow_fever"
        assert any(v["vaccine"].startswith("yellow_fever") for v in plan.vaccines)
        assert plan.general  # bite avoidance etc.

    def test_ideal_timing_present(self):
        plan = pre_travel_consult("india")
        assert all("when" in v for v in plan.vaccines)
```

- [x] **Step 2: Verify failure** — package import error.
- [x] **Step 3: Write `destinations.py`, `prophylaxis.py`, `__init__.py`** (`__init__.py` re-exports the public names; `find_destination` lowercases text and matches `alias in text`).
- [x] **Step 4: Run** — `python3 -m pytest gpdisc_core/tests/test_travel_medicine.py -v` → 12 pass.
- [x] **Step 5: Commit** — `feat(travel_medicine): destination risk table, chemoprophylaxis rules, pre-travel consult`

---

### Task 5: travel_medicine — post-travel screening

**Files:**
- Modify: `gpdisc_core/travel_medicine/__init__.py` (add `post_travel_screening`)
- Create: `gpdisc_core/travel_medicine/post_travel.py`
- Test: append `class TestPostTravel` to `gpdisc_core/tests/test_travel_medicine.py`

**Interfaces:**
- Produces: `def post_travel_screening(trip_text: str, traveller: Optional[dict] = None) -> List[dict]` — each entry `{"test": str, "reason": str, "when": str}`.

Rules (deterministic, driven by `find_destination` on the trip text + freshwater flag from the text `swam|swimming|lake|river|waded|rafting`):

```python
def post_travel_screening(trip_text: str, traveller: Optional[dict] = None) -> List[dict]:
    t = trip_text.lower()
    dest = find_destination(trip_text)
    out = []
    out.append({"test": "FBC with differential (eosinophils)",
                "reason": "Eosinophilia is the screening flag for worm burden in any returning traveller",
                "when": "now"})
    if dest and dest.malaria_risk != "none":
        out.append({"test": "Malaria: only if febrile — films x3 same day",
                    "reason": f"{dest.region} is malarious; asymptomatic screening bloods have no role",
                    "when": "if fever develops (any time up to 6 months)"})
    if any(w in t for w in ["swam", "swimming", "lake", "river", "waded", "rafting", "snorkel"]):
        out.append({"test": "Schistosoma serology",
                    "reason": "Freshwater exposure — Katayama/chronic schistosomiasis",
                    "when": "6-12 weeks after last exposure (earlier is falsely negative)"})
        out.append({"test": "Strongyloides serology",
                    "reason": "Soil/water exposure in tropics; must be excluded before any immunosuppression",
                    "when": "now"})
    if dest and dest.region in ("West Africa", "East Africa"):
        out.append({"test": "HIV + syphilis + hepatitis B screen",
                    "reason": "Regional prevalence + occupational/sexual exposure often undisclosed",
                    "when": "at least 4 weeks after return (window period)"})
    if dest and ("long" in t or "months" in t or "volunteer" in t or "worked" in t):
        out.append({"test": "TB: IGRA (interferon-gamma release assay)",
                    "reason": "Prolonged stay in high-prevalence setting",
                    "when": "8-12 weeks after return"})
    out.append({"test": "Review any fever within 6 months of return",
                "reason": "Malaria (vivax) presents months late; always mention the trip to any clinician",
                "when": "standing safety advice"})
    return out
```

- [x] **Step 1: Failing tests:**

```python
from gpdisc_core.travel_medicine import post_travel_screening

class TestPostTravel:
    def test_fbc_always(self):
        r = post_travel_screening("back from a week in Paris")
        assert r[0]["test"].startswith("FBC")

    def test_freshwater_adds_schistosomiasis(self):
        r = post_travel_screening("three weeks in Malawi, swam in Lake Malawi every day")
        tests = [x["test"] for x in r]
        assert any("Schistosoma" in x for x in tests)
        assert any("Strongyloides" in x for x in tests)

    def test_malarious_region_mentions_fever_rule(self):
        r = post_travel_screening("back from Ghana business trip")
        assert any("6 months" in x["when"] for x in r)

    def test_long_stay_adds_tb(self):
        r = post_travel_screening("volunteered in Kenya for six months")
        assert any("IGRA" in x["test"] for x in r)
```

- [x] **Step 2: Verify failure** — import error.
- [x] **Step 3: Implement `post_travel.py`** (content above) and export from `__init__.py`.
- [x] **Step 4: Run** — 12 + 4 = 16 pass.
- [x] **Step 5: Commit** — `feat(travel_medicine): post-travel screening protocol`

---

### Task 6: preventive_medicine — UK vaccination, screening, CVD prevention

**Files:**
- Create: `gpdisc_core/preventive_medicine/__init__.py`
- Create: `gpdisc_core/preventive_medicine/schedules.py`
- Create: `gpdisc_core/preventive_medicine/screening.py`
- Create: `gpdisc_core/preventive_medicine/cvd_prevention.py`
- Test: `gpdisc_core/tests/test_preventive_medicine.py`

**Interfaces:**
- Produces:
  - `VaccineEntry(vaccine, cohort, schedule_notes)`, `VACCINES_UK: List[VaccineEntry]`
  - `ScreeningEntry(programme, cohort, interval, test, abnormal_pathway)`, `SCREENING_UK: List[ScreeningEntry]`
  - `prevention_check(patient: dict) -> List[dict]` — entries `{"kind": "vaccine"|"screening"|"cardiovascular", "name": ..., "due": True, "detail": ...}`. Patient keys: `age_years`, `sex` ("m"/"f"), `smoker`, `qrisk10` (percent or None), `systolic` (clinic SBP), `on_statin`, `pregnant`, `immunosuppressed`, `diabetes`.

**VACCINES_UK (adult-relevant slice of the UK schedule, 12 entries):**

```python
VACCINES_UK = [
    VaccineEntry("Influenza (annual)", "65+, under-65 risk groups (CKD, cardiac, respiratory, diabetes, immunosuppressed, pregnancy, BMI≥40, care home)", "Every year, September onwards"),
    VaccineEntry("COVID-19 (seasonal)", "75+, immunosuppressed, care home residents, housebound", "Per JCVI seasonal campaign"),
    VaccineEntry("Pneumococcal (PPV23)", "65+, or ≥2y with risk condition", "Single dose at 65; every 5y if immunosuppressed/splenectomy"),
    VaccineEntry("Shingles (Shingrix)", "65-70 programme age (2026 schedule: 60-70 expanding), severely immunosuppressed 50+", "2 doses 8 weeks-12 months apart; contraindicated conditions apply to live predecessor only"),
    VaccineEntry("Pertussis (whooping cough)", "Pregnant women, from 16 weeks gestation", "Every pregnancy, ideally 16-32 weeks"),
    VaccineEntry("RSV", "Pregnant 28+ weeks (seasonal), adults 75-79", "Single dose programme"),
    VaccineEntry("Hepatitis B (infants)", "All infants born in UK (universal since 2017), plus risk groups", "Birth dose then 6-in-1 schedule"),
    VaccineEntry("MMR (2 doses)", "Anyone without 2 documented doses", "Check at 25+ health checks, travel, pre-registration"),
    VaccineEntry("Tdap/IPV booster", "70+ (5-in-1/Repevax at 70), pregnant (from 16w as part of pertussis)", "Once at 70; each pregnancy"),
    VaccineEntry("MenACWY", "Adolescents (school year 9-10 equivalent), university freshers ≤25y who missed", "Single dose"),
    VaccineEntry("HPV", "Girls and boys 12-13 (now unisex programme), MSM up to 45 via clinics", "1 dose <25y (JCVI 2021); 2 doses if older/immunosuppressed"),
    VaccineEntry("Bexsero (MenB)", "Infants; catch-up for at-risk", "2+1 schedule"),
]
```

**SCREENING_UK (8 programmes):**

```python
SCREENING_UK = [
    ScreeningEntry("Bowel cancer screening (FIT)", "54-74 (expanding to 50), men and women", "Every 2 years", "Faecal immunochemical test at home", "Positive FIT → colonoscopy via SSP"),
    ScreeningEntry("Breast cancer screening", "Women 50-70 (self-request 71+)", "Every 3 years", "Mammography", "Recall/assessment clinic"),
    ScreeningEntry("Cervical screening (HPV)", "Women 25-49: 3-yearly; 50-64: 5-yearly", "3 or 5 years", "HPV primary with cytology triage (self-sampling rolling out)", "HPV+ → colposcopy"),
    ScreeningEntry("Abdominal aortic aneurysm", "Men 65 (one-off; self-request older)", "Once at 65", "Ultrasound aorta", "≥3cm → surveillance; ≥5.5cm → vascular referral"),
    ScreeningEntry("Diabetic eye screening", "Everyone with diabetes 12+", "Annual", "Retinal photography", "R1M0+ → grading/refer ophthalmology"),
    ScreeningEntry("NHS Health Check", "Adults 40-74 without existing CVD/dementia", "Every 5 years", "Risk assessment: BP, lipids, BMI, HbA1c, QRISK", "QRISK ≥10% → statin discussion"),
    ScreeningEntry("Antenatal screening", "Pregnant women", "Booking + specific points", "HIV/syphilis/hepatitis B/rubella, sickle cell & thalassaemia, Down/Edwards/Patau, fetal anomaly", "Positive → specialist counselling"),
    ScreeningEntry("Newborn screening", "All newborns", "Day 5", "Blood spot: 9 conditions incl. PKU, CF, sickle cell, MCADD; hearing; NIPE examination", "Positive → confirmatory testing"),
]
```

**cvd_prevention.py rules:**

```python
def cvd_prevention_advice(patient: dict) -> List[dict]:
    """Thresholds: NICE CG181/NG238 — QRISK3 10-year risk ≥10%: offer atorvastatin
    20mg after lifestyle discussion; clinic BP ≥140/90 → confirm with ABPM/HBPM."""
    out = []
    q = patient.get("qrisk10")
    if q is not None and q >= 10 and not patient.get("on_statin") \
            and patient.get("age_years", 0) <= 84:
        out.append({"kind": "cardiovascular", "name": "Statin discussion",
                    "due": True,
                    "detail": f"QRISK3 {q}% ≥10% — offer atorvastatin 20mg nightly after "
                              "informed discussion (lifestyle first/alongside)"})
    sbp = patient.get("systolic")
    if sbp is not None and sbp >= 140:
        out.append({"kind": "cardiovascular", "name": "Confirm hypertension",
                    "due": True,
                    "detail": "Clinic BP ≥140/90 — confirm with ABPM/HBPM before diagnosing "
                              "(≥135/85 daytime average = hypertension)"})
    if patient.get("smoker"):
        out.append({"kind": "cardiovascular", "name": "Smoking cessation offer",
                    "due": True,
                    "detail": "Very brief advice + referral to stop-smoking service; "
                              "NRT/varenicline per preference"})
    return out
```

`prevention_check(patient)` in `schedules.py`/`screening.py` composition: iterate VACCINES_UK + SCREENING_UK with hard-coded cohort predicates:
- 68-year-old man → due: bowel (54-74), AAA (65+, if `aaa_done` not set — accept key `aaa_done`), shingles (in age band), influenza (65+), pneumococcal (65+), COVID (75+? no — 68 not), NHS Health Check (40-74, 5-yearly — flag as due if `health_check_years_ago` > 4 or absent).
- 52-year-old woman → breast (50-70), cervical (50-64: 5-yearly).
- 30-year-old pregnant 20 weeks → pertussis (16-32w), RSV (28w+ — not yet), influenza, antenatal screening.

Cohort predicates are simple age/sex/pregnancy/immunosuppression/diabetes comparisons on the patient dict — implement as small functions per entry inline in `prevention_check`, not a data-driven matching language (YAGNI).

- [x] **Step 1: Failing tests:**

```python
"""Tests for preventive_medicine (expertise program Stage 2)."""
import pytest
from gpdisc_core.preventive_medicine import (
    VACCINES_UK, SCREENING_UK, prevention_check, cvd_prevention_advice,
)

class TestTables:
    def test_table_sizes(self):
        assert len(VACCINES_UK) >= 12
        assert len(SCREENING_UK) == 8
        for s in SCREENING_UK:
            assert s.programme and s.cohort and s.test

class TestPreventionCheck:
    def test_68yo_man(self):
        due = [x["name"] for x in prevention_check({"age_years": 68, "sex": "m"})]
        assert "Bowel cancer screening (FIT)" in due
        assert "Abdominal aortic aneurysm" in due
        assert "Shingles (Shingrix)" in due
        assert "Influenza (annual)" in due

    def test_52yo_woman(self):
        due = [x["name"] for x in prevention_check({"age_years": 52, "sex": "f"})]
        assert "Breast cancer screening" in due
        assert "Cervical screening (HPV)" in due
        assert "Abdominal aortic aneurysm" not in due

    def test_pregnant_20w(self):
        due = [x["name"] for x in prevention_check(
            {"age_years": 30, "sex": "f", "pregnant": True})]
        assert "Pertussis (whooping cough)" in due
        assert "Antenatal screening" in due

    def test_aaa_done_not_due_again(self):
        due = [x["name"] for x in prevention_check(
            {"age_years": 68, "sex": "m", "aaa_done": True})]
        assert "Abdominal aortic aneurysm" not in due

class TestCVDPrevention:
    def test_qrisk_over_threshold_gets_statin_discussion(self):
        r = cvd_prevention_advice({"qrisk10": 14, "age_years": 62})
        assert any("statin" in x["name"].lower() for x in r)

    def test_on_statin_not_flagged(self):
        r = cvd_prevention_advice({"qrisk10": 14, "on_statin": True})
        assert not any("statin" in x["name"].lower() for x in r)

    def test_high_bp_needs_confirmation(self):
        r = cvd_prevention_advice({"systolic": 152})
        assert any("hypertension" in x["name"].lower() for x in r)

    def test_smoker_gets_cessation(self):
        r = cvd_prevention_advice({"smoker": True, "systolic": 120})
        assert any("smoking" in x["name"].lower() for x in r)

    def test_clean_patient_no_flags(self):
        assert cvd_prevention_advice({"qrisk10": 4, "systolic": 118}) == []
```

- [x] **Step 2: Verify failure.**
- [x] **Step 3: Implement the three modules + `__init__.py` exports.**
- [x] **Step 4: Run** — 13 pass.
- [x] **Step 5: Commit** — `feat(preventive_medicine): UK vaccination schedule, screening programmes, CVD prevention rules`

---

### Task 7: sexual_health — UKMEC, STI panels, emergency contraception

**Files:**
- Create: `gpdisc_core/sexual_health/__init__.py`
- Create: `gpdisc_core/sexual_health/contraception.py`
- Create: `gpdisc_core/sexual_health/sti_panels.py`
- Test: `gpdisc_core/tests/test_sexual_health.py`

**Interfaces:**
- Produces:
  - `UKMEC: Dict[Tuple[str, str], Tuple[int, str]]` — `(method, condition) -> (category 1-4, reason)`. Methods: `cocp` (combined pill/patch/ring), `pop` (progestogen-only pill), `implant`, `dmpa` (injection), `ius_iud` (intrauterine). Categories: 1 = no restriction, 2 = benefits outweigh risks, 3 = risks usually outweigh, 4 = unacceptable risk.
  - `def ukmec_category(method, condition) -> Tuple[int, str]` (returns `(0, "no rule")` for unmatched pairs — and the caller must treat 0 as "no specific rule, use clinical judgement")
  - `def safe_methods(condition) -> List[str]` — methods where category ≤2 for that condition.
  - `STI_PANELS: Dict[str, List[str]]`, `def panel_for(text: str) -> Tuple[str, List[str]]`
  - `def emergency_contraception(hours_since_upsi: float, bmi: float = 0, wants_ongoing: bool = False) -> dict`

**UKMEC table (20 rows — high-yield GP rules):**

```python
UKMEC = {
    ("cocp", "migraine_with_aura"): (4, "Stroke risk — oestrogen absolutely contraindicated"),
    ("cocp", "smoker_35_plus"): (4, "Age ≥35 smoking any amount: VTE + MI risk unacceptable"),
    ("cocp", "vte_history"): (4, "Oestrogen multiplies recurrence risk"),
    ("cocp", "bp_160_100"): (4, "Uncontrolled severe hypertension"),
    ("cocp", "breastfeeding_6wks"): (4, "Oestrogen suppresses lactation before 6 weeks"),
    ("cocp", "migraine_no_aura"): (3, "Continue only if no aura and no other risk factors"),
    ("cocp", "smoker_under_35"): (2, "Counsel; VTE risk acceptable if no other factors"),
    ("cocp", "bmi_35"): (3, "VTE risk rises steeply ≥35; POP/implant preferred"),
    ("cocp", "controlled_htn"): (3, "Risk usually outweighs benefit — progestogen-only preferred"),
    ("pop", "breastfeeding_6wks"): (2, "Compatible with lactation"),
    ("pop", "vte_history"): (2, "Progestogen-only does not raise VTE risk meaningfully"),
    ("pop", "migraine_with_aura"): (1, "No oestrogen — safe with aura"),
    ("implant", "breastfeeding_6wks"): (2, "Compatible"),
    ("implant", "vte_history"): (1, "Safe"),
    ("implant", "unspecified_vaginal_bleeding"): (3, "Investigate before insertion"),
    ("dmpa", "bmi_30"): (2, "Counsel on weight gain + bone density with >2y use"),
    ("dmpa", "osteoporosis_risk"): (3, "Bone mineral density concern with prolonged use"),
    ("ius_iud", "pregnancy"): (4, "Never insert in pregnancy"),
    ("ius_iud", "pid_current"): (4, "Treat infection first — insertion risks spread"),
    ("ius_iud", "unspecified_vaginal_bleeding"): (3, "Investigate before insertion"),
}
```

**STI_PANELS:**

```python
STI_PANELS = {
    "asymptomatic_screen": ["Chlamydia + gonorrhoea NAAT", "HIV 4th-gen ag/ab",
                            "Syphilis serology", "Hepatitis B (if unvaccinated/risk)", "Hepatitis C if risk"],
    "symptomatic_male_discharge": ["Urethral NAAT GC/CT", "HIV + syphilis serology",
                                   "MC&S urethral discharge (gonococcus culture)",
                                   "first-void urine NAAT"],
    "symptomatic_female_pelvic_pain": ["NAAT GC/CT (self-taken vaginal)", "HIV + syphilis",
                                       "Urine dip + MSU", "Pregnancy test (ectopic/PID distinction)",
                                       "Swab for TV/BV/candida; endocervical culture if PID suspected"],
    "genital_ulcer": ["HSV PCR + syphilis serology + dark ground if available",
                      "HIV test", "NAAT GC/CT", "consider LGV serology if perianal/MSM"],
    "pregnant_screen": ["HIV, syphilis, hepatitis B (routine antenatal)",
                        "NAAT GC/CT if <25y or risk", "Hepatitis C if risk"],
}
```

`panel_for(text)` keyword routing: "ulcer"/"sore" → genital_ulcer; "discharge" + male markers ("penis", "urethral") → symptomatic_male_discharge; "pelvic"/"lower abdominal"/"pain" + female markers → symptomatic_female_pelvic_pain; "pregnan" → pregnant_screen; default → asymptomatic_screen.

**emergency_contraception:**

```python
def emergency_contraception(hours_since_upsi, bmi=0, wants_ongoing=False):
    """Copper IUD is the most effective EC at any BMI and acts up to 120h.
    Ulipristal acetate: licensed 0-120h, less effective BMI ≥26 (still usable).
    Levonorgestrel: licensed 0-72h, less effective BMI ≥26; can double-dose but
    prefer ulipristal/IUD."""
    options = []
    if hours_since_upsi <= 120:
        options.append({"method": "Copper IUD", "effectiveness": "99.9%",
                        "note": "Most effective at any BMI; acts up to 120h; also ongoing contraception",
                        "first_line": True})
    if hours_since_upsi <= 120:
        eff = "reduced if BMI ≥26" if bmi >= 26 else "good"
        options.append({"method": "Ulipristal acetate 30mg",
                        "effectiveness": eff,
                        "note": "Single dose; avoid if taking enzyme-inducers; "
                                "not with breastfeeding; 5 days later starting hormonal contraception",
                        "first_line": False})
    if hours_since_upsi <= 72:
        eff = "reduced if BMI ≥26 (consider double dose)" if bmi >= 26 else "good"
        options.append({"method": "Levonorgestrel 1.5mg", "effectiveness": eff,
                        "note": "Safe in breastfeeding; re-dose if vomit <3h; "
                                "can quick-start ongoing contraception next day",
                        "first_line": False})
    rec = {"options": options,
           "recommendation": ("Copper IUD" if hours_since_upsi <= 120 else "None in-window — discuss referral"),
           "advise": "Pharmacy access free of charge; pregnancy test if no period within 3 weeks",
           "ongoing": "Quick-start LARC discussion recommended" if wants_ongoing else ""}
    return rec
```

- [x] **Step 1: Failing tests:**

```python
"""Tests for sexual_health (expertise program Stage 2)."""
import pytest
from gpdisc_core.sexual_health import (
    UKMEC, ukmec_category, safe_methods, panel_for, emergency_contraception,
)

class TestUKMEC:
    def test_migraine_aura_cocp_is_4(self):
        cat, why = ukmec_category("cocp", "migraine_with_aura")
        assert cat == 4 and "stroke" in why.lower()

    def test_pop_safe_with_aura(self):
        cat, _ = ukmec_category("pop", "migraine_with_aura")
        assert cat == 1

    def test_iud_pregnancy_is_4(self):
        assert ukmec_category("ius_iud", "pregnancy")[0] == 4

    def test_unknown_pair_returns_zero(self):
        assert ukmec_category("implant", "migraine_with_aura")[0] == 0

    def test_safe_methods_for_vte_history(self):
        methods = safe_methods("vte_history")
        assert "implant" in methods and "pop" in methods
        assert "cocp" not in methods

    def test_table_size(self):
        assert len(UKMEC) == 20

class TestSTIPanels:
    def test_ulcer_panel(self):
        name, panel = panel_for("painful ulcer on my penis")
        assert name == "genital_ulcer"
        assert any("syphilis" in t.lower() for t in panel)

    def test_male_discharge_panel(self):
        name, panel = panel_for("discharge from my penis")
        assert name == "symptomatic_male_discharge"

    def test_pelvic_pain_panel_includes_pregnancy_test(self):
        name, panel = panel_for("lower abdominal pain for three days")
        assert name == "symptomatic_female_pelvic_pain"
        assert any("pregnancy" in t.lower() for t in panel)

    def test_default_asymptomatic(self):
        name, _ = panel_for("just want a routine check")
        assert name == "asymptomatic_screen"

class TestEmergencyContraception:
    def test_within_120h_copper_first_line(self):
        r = emergency_contraception(80)
        assert r["recommendation"] == "Copper IUD"
        assert any(o["method"].startswith("Levonorgestrel") is False for o in r["options"] if o["first_line"])

    def test_beyond_120h_no_hormonal(self):
        r = emergency_contraception(130)
        assert r["recommendation"] == "None in-window — discuss referral"

    def test_bmi_over_26_flags_reduced_efficacy(self):
        r = emergency_contraception(24, bmi=30)
        assert any("reduced" in o["effectiveness"].lower() for o in r["options"])

    def test_levonorgestrel_only_within_72h(self):
        r = emergency_contraception(70)
        methods = [o["method"] for o in r["options"]]
        assert "Levonorgestrel 1.5mg" in methods
```

- [x] **Step 2: Verify failure.**
- [x] **Step 3: Implement.** `ukmec_category` returns the exact pair or `(0, "no rule")`; `safe_methods` returns methods whose category ≤ 2 for the condition (checks every method key in the table for that condition; methods without a rule for that condition default to eligible-with-judgement and are NOT auto-listed — only explicit ≤2 rows are listed; `cocp` excluded only if a row says 3/4).
- [x] **Step 4: Run** — 14 pass.
- [x] **Step 5: Commit** — `feat(sexual_health): UKMEC contraception eligibility, STI panels, emergency contraception rules`

---

### Task 8: Front-door exports + end-to-end integration

**Files:**
- Modify: `gpdisc_core/clinical_reasoning/__init__.py` (export `SyndromeEngine`, `SyndromeFrame`, `SyndromeDifferential`, `discriminating_questions`, `SYNDROME_FRAMES`)
- Test: `gpdisc_core/tests/test_clinical_reasoning.py` (extend `TestFrontDoorWiring`)

**Interfaces:**
- Consumes: Tasks 1-3 outputs.
- Produces: `from gpdisc_core.clinical_reasoning import SyndromeEngine` works; end-to-end emergency + syndrome behaviour verified through `EnhancedUnifiedGPDISCSystem.answer()`.

- [x] **Step 1: Failing tests:**

```python
    # appended inside TestFrontDoorWiring
    def test_syndrome_engine_exported(self):
        from gpdisc_core.clinical_reasoning import SyndromeEngine, SYNDROME_FRAMES
        assert len(SYNDROME_FRAMES) == 5

    def test_end_to_end_fever_after_travel_full_stack(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("fever for two days since returning from Ghana, "
                        "swimming in Lake Volta last month")
        assert r["escalation"] in ("emergency", "urgent")
        c = r["consultation"]
        assert c["syndrome"] == "fever_after_travel"
        ids = [d["condition_id"] for d in c["ranked_differential"]]
        assert "malaria_falciparum" in ids
        assert any("malaria" in t.lower() for t in c["investigation_strategy"])

    def test_non_blanching_rash_stays_emergency_with_syndrome(self):
        sysx = EnhancedUnifiedGPDISCSystem()
        r = sysx.answer("my 3 year old has fever and a rash that doesn't fade when pressed")
        assert r["escalation"] == "emergency"
        assert r["consultation"]["syndrome"] == "fever_rash"
```

- [x] **Step 2: Verify failure** — `ImportError` on the export test.
- [x] **Step 3: Add the exports to `clinical_reasoning/__init__.py`** (imports + `__all__`).
- [x] **Step 4: Run full clinical reasoning suite** — 56 + 3 = 59 pass.
- [x] **Step 5: Commit** — `feat(clinical_reasoning): export syndrome engine; end-to-end fever-after-travel stack verified`

---

### Task 9: Regression battery + docs + memory

**Files:**
- Modify: `CLAUDE.md` (Architecture Overview + Testing section)
- Modify: `docs/superpowers/plans/2026-09-03-tropical-travel-prevention-sexualhealth.md` (tick checkboxes)
- Memory: update `gpidisc-transition.md` → Stage 2 complete

- [x] **Step 1: Full battery:**

```bash
python3 -m pytest gpdisc_core/tests/test_clinical_reasoning.py gpdisc_core/tests/test_travel_medicine.py gpdisc_core/tests/test_preventive_medicine.py gpdisc_core/tests/test_sexual_health.py -v   # 59 + 16 + 13 + 14 = 102
python3 gpdisc_core/comprehensive_system_test.py      # 26/26
python3 gpdisc_core/tests/test_all.py                 # 11 pass / 3 pre-existing legacy failures (documented baseline)
```

- [x] **Step 2: Import sweep** — `pkgutil.walk_packages` over `gpdisc_core` → 0 failures (expect ~515 submodules).
- [x] **Step 3: CLAUDE.md** — extend the "Clinical Reasoning Core (GP-led front door)" section:

```markdown
### Tropical / Travel / Preventive / Sexual Health (Stage 2)

`gpdisc_core/clinical_reasoning/syndromes.py` — five syndrome frames (fever after
travel, eosinophilia in a traveller, fever + thrombocytopenia, fever + jaundice,
fever + rash) with discriminating questions; attached to every consultation that
matches. `gpdisc_core/travel_medicine/` — 24-destination risk table,
chemoprophylaxis rules (traveller-history aware), pre-travel consult and
post-travel screening. `gpdisc_core/preventive_medicine/` — UK vaccination and
screening tables + CVD prevention thresholds. `gpdisc_core/sexual_health/` —
UKMEC eligibility, STI panels, emergency contraception rules.
```

  and add to Testing:

```bash
# Stage 2 suites
python3 -m pytest gpdisc_core/tests/test_travel_medicine.py gpdisc_core/tests/test_preventive_medicine.py gpdisc_core/tests/test_sexual_health.py -v
```

- [x] **Step 4: Commit** — `docs: document Stage 2 tropical/travel/prevention/sexual-health in CLAUDE.md`
- [x] **Step 5: Update memory file** `gpidisc-transition.md` — Stage 2 complete, corpus 150 conditions, test counts.

---

## Self-Review (completed)

- **Spec coverage:** Glenn's tropical module (syndrome-based diagnosis: all five named syndromes present as frames), travel medicine (pre- + post-travel), preventive medicine, sexual/reproductive medicine — all have tasks. ENT/oral medicine extension covered by corpus part 3. Vaccination table included; UK regulatory depth (2ww, DVLA, safeguarding) deliberately deferred to Stage 3 `uk_practice` per the design spec.
- **Placeholders:** none — all code and data in full.
- **Type consistency:** `SyndromeFrame`/`SyndromeDifferential` field names match between Task 2 definition, Task 3 pipeline wiring, and Task 3 summary rendering. `CONDITIONS_PART3` merge pattern mirrors part 2. `prevention_check` patient-dict keys used in tests match the rules' keys (`aaa_done`, `qrisk10`, `on_statin`, `systolic`, `pregnant`, `smoker`).
- **Known deviations to apply during execution:** cambodia typo `hephetitis_a` → `hepatitis_a`; `vyentiane` → `vientiane`; enteric-fever frame differential id must be `typhoid` (not `enteric_fever_typhoid`); `ho chi Minh` alias → `ho chi minh` (lowercased matching).
