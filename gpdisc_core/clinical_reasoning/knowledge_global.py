"""Stage 8 (Tier 3): the world — global high-burden and environmental
corpus part 6.

The Tier-3 premise: this doctor could be anywhere in the world. The
corpus so far is UK-plus-traveller; the conditions that carry most of
the world's actual burden — chronic viral hepatitis, HIV presenting
late, leprosy, the neglected tropical diseases — and the environments
that make their own emergencies (heat, cold, altitude, diving,
radiation) were absent. The pre-implementation probes exposed three
engine bugs before this file existed (see the validation fix commit):
a Nepal trek was a rabies 999 on bare geography; a known hepatitis B
carrier was a needlestick exposure story; every hangover with nausea
was a CO poisoning emergency on two generic words. Geography and
generics never carry a diagnosis — that discipline shapes every
token below: endemic-area tokens are deliberately LOW specificity
(<= 0.5) so they can only ever support a specific symptom token,
never lead alone.
"""
from typing import Dict, List

from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
)

CONDITIONS_PART6: List[ConditionProfile] = [
    # ================= CHRONIC VIRAL DISEASE (the silent burden) =====
    ConditionProfile(
        condition_id="chronic_hepatitis_b",
        name="Chronic hepatitis B",
        category="infection",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("known_hep_b_carrier", 0.90, 0.92),
            SymptomFrequency("hep_b_blood_result", 0.80, 0.95),
            SymptomFrequency("fatigue", 0.40, 0.05),
        ],
        discriminators=["carrier status known for years without "
                        "cirrhosis vs newly detected surface antigen",
                        "flare (acute-on-chronic): sudden jaundice or "
                        "transaminitis in a known carrier — treat as "
                        "acute",
                        "household and sexual contacts need testing "
                        "and vaccination",
                        "origin or family from a high-prevalence area "
                        "(East/Southeast Asia, sub-Saharan Africa, "
                        "Pacific) raises prior but NEVER replaces the "
                        "blood result"],
        red_flags=["jaundice, ascites, encephalopathy or GI bleeding "
                   "in a carrier = decompensation — emergency",
                   "rising AFP or a liver lesion on surveillance "
                   "imaging — hepatocellular carcinoma pathway"],
        investigations=[
            InvestigationProfile("HBsAg + anti-HBc (IgM vs IgG "
                                 "separates acute from chronic), HBV "
                                 "DNA viral load, HBeAg",
                                 "defines infection phase and "
                                 "treatment eligibility", 0.90, 0.90,
                                 "EASL hepatitis B guidelines"),
            InvestigationProfile("Liver fibrosis assessment "
                                 "(elastography/FibroScan or APRI)",
                                 "stage decides treatment urgency",
                                 0.80, 0.85, "NICE NG205 hepatitis B"),
            InvestigationProfile("Ultrasound + AFP 6-monthly once "
                                 "cirrhotic",
                                 "hepatocellular carcinoma "
                                 "surveillance", 0.85, 0.90,
                                 "EASL HCC surveillance"),
        ],
        management_first_line="Confirm phase (HBeAg/DNA/ALT), stage "
                              "fibrosis, refer for antiviral assessment "
                              "(tenofovir/entecavir suppress but rarely "
                              "cure). Test and vaccinate household and "
                              "sexual contacts. Alcohol cessation, "
                              "hepatitis A vaccination, co-check HIV "
                              "and hepatitis C.",
        referral_tier="routine",
        safety_net="Yellow eyes, abdominal swelling, vomiting blood or "
                   "sudden confusion in a known carrier — emergency "
                   "same day.",
        dangerous_mimic_of=["cirrhosis_decompensated", "hepatitis_a"],
        source="WHO hepatitis B fact sheet; EASL 2017; NICE NG205",
    ),
    ConditionProfile(
        condition_id="chronic_hepatitis_c",
        name="Chronic hepatitis C",
        category="infection",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("hep_c_antibody_found", 0.90, 0.95),
            SymptomFrequency("past_injection_drug_use", 0.35, 0.80),
            SymptomFrequency("fatigue", 0.45, 0.05),
        ],
        discriminators=["most infections are asymptomatic for decades "
                        "— found on screening, not symptoms",
                        "any past injecting drug use, even once "
                        "decades ago; also blood transfusion before "
                        "1991 or tattoo/medical procedures abroad",
                        "curable: 8-12 weeks of direct-acting "
                        "antivirals, >95% sustained virological "
                        "response"],
        red_flags=["jaundice/ascites/encephalopathy = cirrhosis "
                   "decompensation — emergency",
                   "decompensation rules out some DAA regimens — "
                   "specialist, fast"],
        investigations=[
            InvestigationProfile("HCV antibody then HCV RNA if "
                                 "positive, genotype (treatment "
                                 "planning), fibrosis staging",
                                 "antibody alone means exposure, RNA "
                                 "means current infection", 0.90, 0.90,
                                 "NICE NG200 hepatitis C"),
            InvestigationProfile("HIV and hepatitis B co-infection "
                                 "testing",
                                 "changes regimen and prognosis", 0.80,
                                 0.85, "WHO HCV guidance"),
        ],
        management_first_line="Confirm viraemia, stage fibrosis, refer "
                              "to hepatology/infectious diseases for "
                              "direct-acting antivirals — a CURE, so "
                              "case-finding is the intervention. "
                              "Counsel on blood-borne precautions; "
                              " opioid-assessment if past injecting.",
        referral_tier="routine",
        safety_net="Yellow eyes, abdominal swelling or vomiting blood "
                   "— emergency same day.",
        dangerous_mimic_of=["cirrhosis_decompensated"],
        source="WHO hepatitis C; NICE NG200",
    ),
    ConditionProfile(
        condition_id="hiv_undiagnosed",
        name="HIV infection (undiagnosed / late presentation)",
        category="infection",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("recurrent_thrush_shingles", 0.45, 0.85),
            SymptomFrequency("recurrent_infections_years", 0.40, 0.80),
            SymptomFrequency("weight_loss", 0.50, 0.15),
            SymptomFrequency("night_sweats", 0.35, 0.15),
            SymptomFrequency("diarrhoea", 0.30, 0.10),
        ],
        discriminators=["adult recurrent oral thrush WITHOUT steroid "
                        "inhaler/diabetes, or shingles more than once "
                        "— test for HIV",
                        "late presenters: unexplained weight loss, "
                        "night sweats, chronic diarrhoea, recurrent "
                        "chest infections; also severe/disseminated "
                        "TB, unusual cancers",
        ],
        red_flags=["CD4 < 200 territory: breathlessness + dry cough "
                   "(PCP), confusion (toxoplasma/crypto), severe "
                   "weight loss — urgent specialist same-week or "
                   "admission",
                   "any new meningism, severe headache or focal "
                   "neurology in possible HIV — emergency"],
        investigations=[
            InvestigationProfile("4th-generation HIV test (Ag/Ab) — "
                                 "laboratory or point-of-care",
                                 "modern tests are accurate from 4 "
                                 "weeks after exposure", 0.95, 0.95,
                                 "BASHH/BHIVA HIV testing guidelines"),
            InvestigationProfile("CD4 count + HIV viral load at "
                                 "diagnosis; TB and hepatitis "
                                 "co-infection screen",
                                 "stages urgency and baseline", 0.90,
                                 0.90, "BHIVA guidelines"),
        ],
        management_first_line="Offer the test universally — the "
                              "diagnosis is MISSED because nobody "
                              "asks, not because it hides. Link "
                              "same-day to specialist care: "
                              "antiretroviral therapy for ALL "
                              "diagnosed (U=U), partner notification "
                              "supported. Late presenters need "
                              "opportunistic-infection workup.",
        referral_tier="urgent",
        safety_net="Breathlessness with dry cough, confusion, or "
                   "rapid weight loss — urgent assessment now; do "
                   "not wait weeks.",
        dangerous_mimic_of=["tb_pulmonary", "lymphoma_suspect"],
        source="BHIVA; WHO HIV; UKHSA HIV testing",
    ),
    ConditionProfile(
        condition_id="hiv_prep_eligibility",
        name="HIV pre-exposure prophylaxis (PrEP) candidacy",
        category="sexual_health",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("prep_request", 0.90, 0.90),
            SymptomFrequency("condomless_multiple_partners", 0.50, 0.55),
        ],
        discriminators=["the person asking about PrEP has usually "
                        "already assessed their own risk — the "
                        "consultation confirms eligibility and "
                        "baseline tests",
                        "event-driven (2-1-1) vs daily dosing per "
                        "sex pattern",
                        "cross-check UKMEC-style issues: renal, bone, "
                        "hepatitis B co-infection (tenofovir treats "
                        "it too)"],
        red_flags=["recent high-risk exposure (<72h) is PEP not PrEP "
                   "— emergency pathway for post-exposure "
                   "prophylaxis",
                   "seroconversion illness (fever, rash, sore "
                   "throat weeks after exposure) — test before "
                   "starting PrEP"],
        investigations=[
            InvestigationProfile("HIV Ag/Ab test, hepatitis B/C, "
                                 "syphilis, gonorrhoea/chlamydia NAAT "
                                 "baseline; renal function",
                                 "PrEP needs a negative HIV test and "
                                 "a working kidney first", 0.95, 0.90,
                                 "BASHH PrEP guidelines"),
            InvestigationProfile("Repeat HIV test at 3 months with "
                                 "renal monitoring",
                                 "on-PrEP safety netting", 0.90, 0.85,
                                 "BASHH PrEP monitoring"),
        ],
        management_first_line="Confirm HIV negative, screen STIs and "
                              "hepatitis, check eGFR, then prescribe "
                              "per national PrEP scheme — daily or "
                              "event-driven. Stress adherence and "
                              "3-monthly review; condoms still "
                              "prevent the rest.",
        referral_tier="routine",
        safety_net="Fever with rash and sore throat in the weeks "
                   "after a new exposure — test BEFORE starting or "
                   "continuing PrEP.",
        source="WHO PrEP; BASHH/BHIVA PrEP",
    ),

    # ================= NEGLECTED TROPICAL + ZOONOTIC ================
    ConditionProfile(
        condition_id="leprosy",
        name="Leprosy (Hansen's disease)",
        category="tropical",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("numb_pale_patches", 0.85, 0.95),
            SymptomFrequency("skin_numbness_months", 0.60, 0.85),
            SymptomFrequency("nerve_thickening_palpable", 0.35, 0.95),
            SymptomFrequency("endemic_area_long_stay", 0.45, 0.45),
        ],
        discriminators=["hypopigmented patch with LOSS OF TOUCH/PAIN "
                        "inside it — the numbness IS the examination "
                        "sign (test with cotton wool/spinner)",
                        "paucibacillary (few patches, no organisms) "
                        "vs multibacillary (many lesions, nodules, "
                        "nasal involvement) — different regimens",
                        "thickened nerves at elbow/knee/neck or new "
                        "claw-hand/foot-drop — borderline towards "
                        "multibacillary",
                        "endemic stay ALONE never diagnoses: it "
                        "lowers the threshold to examine, nothing "
                        "more"],
        red_flags=["sudden painful nerve, new weakness, or visible "
                   "reaction (red swollen patches, fever) — lepra "
                   "reaction type 1/2: urgent, steroids, "
                   "same-day specialist",
                   "eye redness or reduced corneal sensation — "
                   "lagophthalmos exposure risk"],
        investigations=[
            InvestigationProfile("Skin slit smear / biopsy with "
                                 "histology (demonstrates AFB)",
                                 "classifies pauci- vs "
                                 "multibacillary", 0.85, 0.90,
                                 "WHO leprosy guide"),
            InvestigationProfile("Nerve function testing (monofilament "
                                 "+ voluntary muscle testing) at "
                                 "baseline and each review",
                                 "silent neuropathy precedes visible "
                                 "deformity", 0.85, 0.85,
                                 "WHO disability grading"),
        ],
        management_first_line="Refer to specialist (dermatology/"
                              "infectious diseases) for "
                              "WHO multidrug therapy: rifampicin + "
                              "clofazimine (+ dapsone if "
                              "paucibacillary), 6-12 months, FREE of "
                              "charge in endemic programmes. It is "
                              "CURABLE and not spread by casual "
                              "contact — say so out loud; stigma is "
                              "the complication that harms most.",
        referral_tier="routine",
        safety_net="New weakness, painful red nerves or eye "
                   "involvement — same-day review: reactions damage "
                   "nerves permanently in days.",
        dangerous_mimic_of=["vitiligo_naevoid_suspect", "tinea_corporis"],
        source="WHO Guide to Eliminate Leprosy",
    ),
    ConditionProfile(
        condition_id="neurocysticercosis",
        name="Neurocysticercosis",
        category="tropical",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("seizure_adult_new", 0.60, 0.30),
            SymptomFrequency("brain_cysts_imaging", 0.80, 0.92),
            SymptomFrequency("pork_tapeworm_exposure", 0.40, 0.85),
        ],
        discriminators=["new-onset seizures in someone from/long "
                        "resident in Latin America, South Asia, "
                        "sub-Saharan Africa or China — the world's "
                        "commonest cause of adult-onset epilepsy in "
                        "endemic zones",
                        "calcified lesions on imaging = old "
                        "infection; viable cysts = active",
                        "household carrier: the tapeworm lives in a "
                        "human gut, not the patient's pork — "
                        "stool-screen close contacts"],
        red_flags=["raised intracranial pressure (morning headache, "
                   "vomiting, papilloedema) or hydrocephalus on "
                   "imaging — emergency",
                   "multiple live cysts treated without steroid "
                   "cover can swell and herniate — NEVER start "
                   "antiparasitics without specialist oversight"],
        investigations=[
            InvestigationProfile("CT/MRI brain (contrast)",
                                 "cysts, scolex, calcifications; "
                                 "hydrocephalus", 0.95, 0.95,
                                 "WHO/IANTD cysticercosis"),
            InvestigationProfile("Serology (EITB immunoblot) + stool "
                                 "microscopy for taenia in household",
                                 "supports, imaging decides", 0.80,
                                 0.80, "CDC cysticercosis"),
        ],
        management_first_line="Specialist-led: antiepileptics for "
                              "seizures first, then staged "
                              "albendazole (+ praziquantel) WITH "
                              "corticosteroid cover depending on "
                              "cyst stage/number and pressure signs. "
                              "Ophthalmic screening before therapy "
                              "if ocular involvement possible.",
        referral_tier="urgent",
        safety_net="Seizure not stopping, drowsiness, worsening "
                   "headache or vomiting — emergency.",
        dangerous_mimic_of=["first_seizure_adult", "brain_tumour_suspect"],
        source="WHO cysticercosis; IANTD consensus",
    ),
    ConditionProfile(
        condition_id="brucellosis",
        name="Brucellosis (undulant fever)",
        category="zoonotic_infection",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("undulant_fever_waves", 0.65, 0.90),
            SymptomFrequency("raw_dairy_exposure", 0.55, 0.90),
            SymptomFrequency("farm_animal_contact", 0.40, 0.75),
            SymptomFrequency("joint_pain_adults", 0.50, 0.10),
            SymptomFrequency("night_sweats", 0.40, 0.15),
        ],
        discriminators=["fever that WAVES — days on, days off, weeks "
                        "long, drenching sweats, joint/lower-back "
                        "aches: the 'fever of unknown origin' that "
                        "travel plus raw dairy answers",
                        "unpasteurised milk/cheese (farm-gate, "
                        "imported, market) or work with cattle/"
                        "sheep/goats — the exposure is the "
                        "diagnosis",
                        "complications: sacroiliitis, orchitis, "
                        "spondylodiscitis, endocarditis (rare, "
                        "lethal)"],
        red_flags=["new murmur or heart failure signs — "
                   "brucella endocarditis: emergency, surgical",
                   "acute testicular pain/swelling (orchitis), "
                   "spinal pain with neurology — urgent imaging"],
        investigations=[
            InvestigationProfile("Brucella serology (SAT/ELISA) + "
                                 "blood cultures (hold 6 weeks, warn "
                                 "lab)",
                                 "culture is slow and lab staff must "
                                 "be warned — biohazard group 3",
                                 0.85, 0.90, "WHO brucellosis"),
            InvestigationProfile("FBC, CRP, LFTs; echocardiogram if "
                                 "any cardiac sign",
                                 "complication screen", 0.70, 0.70,
                                 "IDSA zoonoses"),
        ],
        management_first_line="Specialist advice: doxycycline + "
                              "rifampicin (or doxycycline + "
                              "streptomycin/gentamicin) 6 weeks "
                              "minimum; relapse is common so review "
                              "at 3/6/12 months. Report to public "
                              "health; screen exposed household.",
        referral_tier="urgent",
        safety_net="New heart symptoms, severe back pain with leg "
                   "weakness, or swelling of a testicle — same-day "
                   "assessment.",
        dangerous_mimic_of=["tb_pulmonary", "enteric_fever_group"],
        source="WHO brucellosis in humans and animals",
    ),
    ConditionProfile(
        condition_id="melioidosis",
        name="Melioidosis",
        category="zoonotic_infection",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("soil_water_exposure_endemic", 0.50, 0.85),
            SymptomFrequency("se_asia_stay_low", 0.45, 0.45),
            SymptomFrequency("pneumonia_not_responding", 0.45, 0.75),
            SymptomFrequency("fever", 0.70, 0.05),
            SymptomFrequency("sepsis_picture", 0.30, 0.40),
        ],
        discriminators=["the great imitator of northern Australia "
                        "and Southeast Asia: diabetes + wet-season + "
                        "soil/water contact (paddy, floods, "
                        "gardening barefoot, kava wading)",
                        "pneumonia not responding to standard "
                        "antibiotics, or abscesses in odd places "
                        "(liver, spleen, prostate, skin) — ask WHERE "
                        "and WHAT the feet were in",
                        "can present as severe sepsis with "
                        "multi-organ failure in days"],
        red_flags=["fever with confusion/low BP in a diabetic "
                   "returned traveller — emergency: sepsis pathway "
                   "plus melioidosis-specific cover",
                   "any abscess + travel history — do not drain "
                   "blindly, imaging first"],
        investigations=[
            InvestigationProfile("Blood + throat/urine/sputum/wound "
                                 "cultures for Burkholderia "
                                 "pseudomallei (warn lab: biohazard "
                                 "3)",
                                 "the culture IS the diagnosis; labs "
                                 "must not discard slow growers",
                                 0.90, 0.92, "Darwin melioidosis "
                                 "guidelines"),
            InvestigationProfile("Chest imaging + abdominal "
                                 "ultrasound/CT (abscess survey), "
                                 "prostate assessment in men",
                                 "maps the dissemination", 0.85, 0.85,
                                 "Melioidosis guidelines (Anderson)"),
        ],
        management_first_line="Admit: IV ceftazidime or meropenem >=2 "
                              "weeks (add trimethoprim-"
                              "sulfamethoxazole in severe disease), "
                              "then oral eradication for 3-6 months "
                              "— relapse kills. Glycaemic control is "
                              "part of the treatment.",
        referral_tier="emergency",
        safety_net="Fever, breathlessness or drowsiness after soil/"
                   "water exposure in an endemic area — emergency "
                   "now, say 'possible melioidosis' out loud to the "
                   "receiving team.",
        dangerous_mimic_of=["tb_pulmonary", "community_pneumonia"],
        source="CDC melioidosis; Darwin guidelines",
    ),
    ConditionProfile(
        condition_id="q_fever",
        name="Q fever (Coxiella burnetii)",
        category="zoonotic_infection",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("farm_animal_contact", 0.50, 0.90),
            SymptomFrequency("fever", 0.75, 0.05),
            SymptomFrequency("atypical_pneumonia_hepatitis", 0.40, 0.75),
            SymptomFrequency("headache", 0.40, 0.05),
        ],
        discriminators=["abattoir workers, sheep/cattle farmers, "
                        "vets, and anyone downwind of lambing pens — "
                        "inhalation of dust is the route (no bite "
                        "needed)",
                        "flu-like illness + atypical pneumonia + "
                        "mild hepatitis triad; occasionally "
                        "splenomegaly",
                        "CHRONIC Q (months later): culture-negative "
                        "endocarditis, especially valve disease/"
                        "immunosuppression/pregnancy"],
        red_flags=["new murmur, weight loss, night sweats over "
                   "months after farm exposure — chronic Q fever "
                   "endocarditis: urgent specialist",
                   "pregnancy + Q fever — obstetric infectious "
                   "diseases advice urgently"],
        investigations=[
            InvestigationProfile("Q fever serology phase I + II "
                                 "(IgG/IgM) — acute vs chronic "
                                 "pattern",
                                 "phase II high = acute, phase I "
                                 ">= phase II = chronic", 0.90, 0.90,
                                 "CDC Q fever diagnosis"),
            InvestigationProfile("FBC/LFTs, echocardiogram if "
                                 "chronic suspicion, {18F}FDG-PET "
                                 "where available",
                                 "chronic foci localisation", 0.75,
                                 0.80, "ESC endocarditis"),
        ],
        management_first_line="Acute: doxycycline 14 days (add "
                              "hydroxychloroquine in chronic disease "
                              "for >=18-24 months, specialist-led). "
                              "Notifiable in several jurisdictions — "
                              "occupational source matters (abattoir "
                              "outbreaks are found this way).",
        referral_tier="routine",
        safety_net="Fever lasting beyond a week of farm exposure, or "
                   "any new heart murmur later — return promptly for "
                   "serology.",
        dangerous_mimic_of=["community_pneumonia", "enteric_fever_group"],
        source="CDC Q fever; WHO zoonoses",
    ),
    ConditionProfile(
        condition_id="chagas_disease",
        name="Chronic Chagas disease (Trypanosoma cruzi)",
        category="tropical",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("chagas_screen_positive", 0.60, 0.95),
            SymptomFrequency("latin_america_rural_origin", 0.50, 0.45),
            SymptomFrequency("new_heart_block_cardiomyopathy", 0.30, 0.75),
        ],
        discriminators=["rural Latin America (mud walls, thatch — "
                        "the triatomine bug's home), often decades "
                        "ago: the heart and gut disease of "
                        "otherwise-unexplained cardiomyopathy, heart "
                        "block, or megacolon in a migrant",
                        "blood-donor/antenatal screening letters are "
                        "a common FIRST presentation in non-endemic "
                        "countries",
                        "reactivation in immunosuppression/HIV — "
                        "think Chagas in the right-origin patient "
                        "with a brain lesion or myocarditis"],
        red_flags=["syncope, heart failure or new block in someone "
                   "from rural Latin America — urgent cardiology",
                   "acute symmetrical facial swelling after return "
                   "from an endemic area (chagoma/Romaña sign) — "
                   "urgent"],
        investigations=[
            InvestigationProfile("T. cruzi serology x2 different "
                                 "assays (chronic); parasitaemia "
                                 "tests (blood film/PCR) for acute",
                                 "chronic = serology; acute/reaction "
                                 "= direct detection", 0.90, 0.90,
                                 "WHO Chagas"),
        ],
        management_first_line="Specialist referral: benznidazole (or "
                              "nifurtimox) for acute, congenital, "
                              "reactivated and selected chronic "
                              "cases; cardiology follow-up for "
                              "cardiomyopathy (device/heart-failure "
                              "management). Screen children of "
                              "infected mothers (congenital "
                              "transmission).",
        referral_tier="routine",
        safety_net="Fainting spells, breathlessness or palpitations "
                   "in a patient from rural Latin America — prompt "
                   "cardiac assessment, mention Chagas explicitly.",
        dangerous_mimic_of=["dilated_cardiomyopathy_suspect"],
        source="WHO Chagas disease control",
    ),
    ConditionProfile(
        condition_id="sleeping_sickness",
        name="Human African trypanosomiasis (sleeping sickness)",
        category="tropical",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("daytime_somnolence_fever", 0.55, 0.88),
            SymptomFrequency("tsetse_bite_history", 0.40, 0.90),
            SymptomFrequency("posterior_cervical_nodes", 0.30, 0.80),
            SymptomFrequency("fever", 0.60, 0.05),
        ],
        discriminators=["stage 1 (blood): intermittent fever, "
                        "headache, the chance chancre, posterior "
                        "cervical lymph nodes (Winterbottom's sign)",
                        "stage 2 (CNS): daytime somnolence with night "
                        "insomnia, personality change, movement "
                        "disorders — a lumbar puncture decides the "
                        "stage AND the drug",
                        "East African (T. brucei rhodesiense): "
                        "weeks, virulent, safari/game-park belt; "
                        "West African (gambiense): months-years, "
                        "insidious"],
        red_flags=["ANY neurological sign after tsetse-country "
                   "exposure — same-day specialist: stage-2 delay is "
                   "fatal",
                   "rhodesiense can kill within weeks of the bite"],
        investigations=[
            InvestigationProfile("Thick blood film/PCR + card "
                                 "agglutination test (CATT); "
                                 "lumbar puncture for staging",
                                 "parasites in CSF = stage 2 = "
                                 "different, toxic therapy", 0.95,
                                 0.95, "WHO HAT toolkit"),
        ],
        management_first_line="Urgent specialist/infectious-diseases "
                              "referral: stage determines therapy "
                              "(pentamidine/suramin for stage 1; "
                              "NECT — nifurtimox-eflornithine or "
                              "foscarnol-based for stage 2). "
                              "National/tropical programmes hold the "
                              "drugs; notify public health.",
        referral_tier="urgent",
        safety_net="Drowsiness, confusion or personality change "
                   "after travel to tsetse regions — emergency "
                   "assessment, do not wait for the classic "
                   "sleepiness.",
        dangerous_mimic_of=["cerebral_malaria_suspect", "meningitis"],
        source="WHO human African trypanosomiasis",
    ),
    ConditionProfile(
        condition_id="cutaneous_leishmaniasis",
        name="Cutaneous leishmaniasis",
        category="tropical",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("chronic_crater_ulcer", 0.80, 0.92),
            SymptomFrequency("sandfly_region_stay", 0.45, 0.55),
        ],
        discriminators=["painless chronic ulcer with raised "
                        "'volcano' edges on exposed skin, weeks "
                        "after sandfly-region travel (Middle East, "
                        "Americas, Mediterranean, Central Asia)",
                        "New World species can mucosally spread "
                        "(nose/mouth, years later) — origin matters "
                        "for follow-up",
                        "multiple lesions or lymphatic spread = "
                        "higher parasite load"],
        red_flags=["ulcer on the face, over a joint, or any nasal/"
                   "oral involvement — specialist faster: mucosal "
                   "risk",
                   "immunosuppression — can disseminate"],
        investigations=[
            InvestigationProfile("Dermal slit smear/biopsy or PCR "
                                 "for Leishmania species",
                                 "species predicts mucosal risk and "
                                 "chooses therapy", 0.90, 0.90,
                                 "WHO leishmaniasis"),
        ],
        management_first_line="Refer dermatology/tropical medicine: "
                              "many Old World lesions self-heal in "
                              "months (watchful waiting valid, "
                              "cosmetic sites excepted); options "
                              "include topical paromomycin, "
                              "intralesional antimony, or systemic "
                              "therapy for New World/multiple/"
                              "mucosal-risk lesions.",
        referral_tier="routine",
        safety_net="Ulcer enlarging after a month, new nose or "
                   "mouth symptoms, or fevers — prompt review.",
        dangerous_mimic_of=["skin_cancer_suspect_nonmelanoma",
                            "pyoderma_suspect"],
        source="WHO technical report leishmaniasis",
    ),
    ConditionProfile(
        condition_id="visceral_leishmaniasis",
        name="Visceral leishmaniasis (kala-azar)",
        category="tropical",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("enlarged_spleen_fever_months", 0.65, 0.88),
            SymptomFrequency("pancytopenia_counts_low", 0.60, 0.85),
            SymptomFrequency("fever", 0.80, 0.05),
            SymptomFrequency("weight_loss", 0.55, 0.15),
            SymptomFrequency("skin_greyed_darkening", 0.15, 0.80),
        ],
        discriminators=["fever + big spleen + pancytopenia after "
                        "months in an endemic area (South Asia, East "
                        "Africa, Brazil/Mediterranean): the "
                        "'kala-azar' — fever of unknown origin with "
                        "an enlarging spleen",
                        "post-kala-azar dermal leishmaniasis: "
                        "nodules/patches AFTER treatment — "
                        "parasitological relapse signal",
                        "HIV co-infection changes everything — test"],
        red_flags=["bleeding, secondary infection, or severe "
                   "anaemia — emergency; untreated kala-azar is "
                   ">90% fatal",
                   "any fever + splenomegaly + travel = same-week "
                   "specialist at most"],
        investigations=[
            InvestigationProfile("rK39 rapid test + bone-marrow/"
                                 "spleen aspirate or PCR where "
                                 "available; FBC (pancytopenia)",
                                 "rK39 screens, aspirate confirms",
                                 0.90, 0.90, "WHO VL guidelines"),
        ],
        management_first_line="Specialist/infectious diseases: "
                              "liposomal amphotericin B (or "
                              "miltefosine/paromomycin combos per "
                              "region) — treat as potentially fatal; "
                              "nutrition and anaemia correction ride "
                              "along; screen for HIV and malnutrition.",
        referral_tier="urgent",
        safety_net="Fever with a big spleen and low blood counts is "
                   "a same-week specialist problem — sooner if "
                   "bleeding or breathless.",
        dangerous_mimic_of=["malaria_falciparum", "lymphoma_suspect",
                            "enteric_fever_group"],
        source="WHO visceral leishmaniasis",
    ),
    # cholera_severe deliberately NOT repeated here: knowledge_tropical
    # already carries it (urgent tier, rice_water_stool token). A probe
    # caught the shadow duplicate rendering TWO cholera rows in one
    # differential — find_condition returns the first id match, so the
    # emergency-tier authoring here was silently dead anyway.
    ConditionProfile(
        condition_id="rabies_symptomatic",
        name="Rabies (symptomatic) — universally fatal",
        category="infection",
        prevalence_per_consult=0.00005,
        symptoms=[
            SymptomFrequency("bite_site_tingling_weeks", 0.65, 0.90),
            SymptomFrequency("water_swallow_spasm_fear", 0.80, 0.95),
            SymptomFrequency("air_draft_fear_spasm", 0.30, 0.90),
            SymptomFrequency("agitated_confused_bite_history", 0.45, 0.80),
        ],
        discriminators=["the window CLOSED: prodrome is itch/"
                        "tingling/pain AT THE OLD BITE SITE weeks-"
                        "months later, then hydrophobia (throat "
                        "spasms at the sight/thought of water), "
                        "aerophobia, agitation, then paralysis",
                        "at THIS stage palliation is the honest "
                        "plan — survival is anecdotal; the entire "
                        "battle is the exposure pathway BEFORE "
                        "symptoms",
                        "paralytic (dumb) rabies: ascending "
                        "weakness without the water spasms — "
                        "post-exposure history is the only clue"],
        red_flags=["this whole entry is a red flag — suspected "
                   "symptomatic rabia needs: isolation, specialist "
                   "ID + critical care discussion, palliative "
                   "framing with the family, public-health "
                   "notification, and contact PEP risk assessment"],
        investigations=[
            InvestigationProfile("Specialist-directed: saliva/CSF/"
                                 "skin PCR, serology (unvaccinated), "
                                 "corneal impressions",
                                 "clinical suspicion organises "
                                 "testing, never delays it", 0.90,
                                 0.90, "WHO rabies position paper"),
        ],
        management_first_line="Suspected symptomatic rabies: urgent "
                              "specialist ID involvement, strict "
                              "isolation (transmissible to staff), "
                              "comfort-focused care, family "
                              "explanation, and ABOVE ALL a public-"
                              "health review of every contact and "
                              "the source. The consultation's real "
                              "work: make sure no one else was "
                              "exposed and every exposure gets PEP.",
        referral_tier="emergency",
        safety_net="Tingling or pain at an old animal-bite site "
                   "abroad — treat as suspected rabies TODAY, not "
                   "tomorrow.",
        dangerous_mimic_of=["tetanus_suspect"],
        source="WHO rabies; UKHSA rabies PEP",
    ),

    # ================= ENVIRONMENTAL EXTREMES ========================
    ConditionProfile(
        condition_id="heat_exhaustion",
        name="Heat exhaustion",
        category="environmental",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("heat_exposure_context", 0.75, 0.80),
            SymptomFrequency("heavy_sweating_weak", 0.70, 0.75),
            SymptomFrequency("muscle_cramps_heat", 0.40, 0.70),
            SymptomFrequency("headache", 0.40, 0.05),
            SymptomFrequency("dizziness", 0.40, 0.10),
        ],
        discriminators=["SWEATING PRESENT and mentation NORMAL — that "
                        "is the line separating exhaustion from "
                        "heat stroke",
                        "weakness/thirst/dizziness/cramps after "
                        "sun or heatwave work or endurance events",
                        "salt/water depletion mix: cramps point to "
                        "salt loss"],
        red_flags=["ANY confusion, odd behaviour, ataxia or "
                   "cessation of sweating — heat STROKE: 999, this "
                   "is a differential-diagnosis killer",
                   "collapse with prolonged immobility → "
                   "rhabdomyolysis/renal failure"],
        investigations=[],
        management_first_line="Cool environment, lie flat, oral "
                              "ORS/electrolyte fluids (slowly if "
                              "nauseated), loose clothing, fan/"
                              "sponging; recheck mentation hourly — "
                              "recovery within 30-60 min expected. "
                              "Advise 24-48 h off heavy exertion.",
        referral_tier="urgent",
        safety_net="Confusion, not sweating, collapse or no "
                   "improvement after an hour of cooling — treat "
                   "as heat stroke, emergency.",
        source="NICE heat illness; WHO heat-health",
    ),
    ConditionProfile(
        condition_id="heat_stroke",
        name="Heat stroke",
        category="environmental",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("hot_dry_confused", 0.80, 0.92),
            SymptomFrequency("collapse_hot_environment", 0.60, 0.85),
            SymptomFrequency("core_temp_40_plus", 0.75, 0.95),
        ],
        discriminators=["core temperature >40°C + CNS dysfunction "
                        "(confusion, ataxia, seizures, coma) — "
                        "exertional (marathon, recruits, workers) "
                        "often STILL sweating; classic (elderly, "
                        "heatwave, medications) often dry",
                        "'cool and confused in a hot place' — the "
                        "environment is part of the diagnosis",
                        "anticholinergics, antipsychotics, "
                        "stimulants and dehydration predispose"],
        red_flags=["multi-organ failure timeline: rhabdomyolysis, "
                   "AKI, DIC, liver failure — hours decide outcome",
                   "cool FIRST, transport SECOND"],
        investigations=[
            InvestigationProfile("Rectal/core temp (tympanic "
                                 "under-reads), CK, renal function, "
                                 "LFTs, coagulation, glucose, "
                                 "electrolytes",
                                 "maps the organ damage", 0.90, 0.85,
                                 "Exertional heat stroke consensus"),
        ],
        management_first_line="999 + COOL AGGRESSIVELY NOW: shade, "
                              "strip, ice-water immersion where "
                              "possible (gold standard), else "
                              "evaporative (mist + fan + ice packs "
                              "to neck/axillae/groins). Target core "
                              "<39°C within 30 minutes. Fluids "
                              "carefully; avoid shivering and "
                              "antipyretics (useless in heat "
                              "stroke).",
        referral_tier="emergency",
        safety_net="Someone hot and not themselves in hot "
                   "conditions — start cooling before you finish "
                   "taking the history.",
        dangerous_mimic_of=["meningitis", "sepsis_adult",
                            "thyrotoxic_storm_suspect"],
        source="NICE heat illness; wilderness medicine consensus",
    ),
    ConditionProfile(
        condition_id="hypothermia_moderate_severe",
        name="Hypothermia (moderate/severe)",
        category="environmental",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("cold_exposure_drowsy_confused", 0.75, 0.90),
            SymptomFrequency("core_temp_below_35", 0.85, 0.95),
            SymptomFrequency("cold_water_immersion", 0.40, 0.85),
        ],
        discriminators=["shivering (mild) → SHIVERING STOPS with "
                        "drowsiness/confusion (moderate 28-32°C) → "
                        "unresponsive (severe <28°C): the mental "
                        "state tracks the temperature",
                        "'cold and confused' in the elderly indoors "
                        "is the classic UK presentation — poverty, "
                        "immobility, sedatives; outdoors: "
                        "immersion, mountain, alcohol",
                        "'not dead until warm and dead': severe "
                        "hypothermia mimics death; resuscitate "
                        "while rewarming"],
        red_flags=["arrhythmias (J-waves on ECG, bradycardia), "
                   "apnoea — handle gently: rough movement "
                   "triggers VF",
                   "severe hypothermia with any vital signs — "
                   "999 with gentle handling and active rewarming"],
        investigations=[
            InvestigationProfile("Low-reading thermometer (core), "
                                 "ECG (J-wave, arrhythmia), glucose "
                                 "(hypoglycaemia rides along), "
                                 "electrolytes, thyroid function, "
                                 "toxicology screen",
                                 "finds the cause and the "
                                 "complications", 0.90, 0.85,
                                 "NICE hypothermia; WMS guidelines"),
        ],
        management_first_line="999 for moderate/severe. Gentle "
                              "handling, wet clothes off, dry "
                              "blankets, active external rewarming "
                              "(forced warm air/blankets); warm IV "
                              "fluids if available; warm humidified "
                              "oxygen in severe. Check glucose and "
                              "sepsis — infection CAUSES "
                              "hypothermia too. Elderly: safeguard "
                              "the home situation before discharge.",
        referral_tier="emergency",
        safety_net="A cold person who is not shivering is an "
                   "emergency even if the house feels fine to you.",
        dangerous_mimic_of=["sepsis_adult", "opioid_overdose"],
        source="NICE hypothermia; Wilderness Medical Society",
    ),
    ConditionProfile(
        condition_id="acute_mountain_sickness",
        name="Acute mountain sickness",
        category="environmental",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("altitude_exposure_context", 0.90, 0.85),
            SymptomFrequency("altitude_headache", 0.80, 0.85),
            SymptomFrequency("altitude_nausea_fatigue", 0.55, 0.70),
        ],
        discriminators=["headache PLUS at least one of nausea/"
                        "fatigue/dizziness/poor sleep, above "
                        "~2500 m, within 6-12 h of ascent — AMS is "
                        "a CLINICAL score (Lake Louise), not a "
                        "machine",
                        "the two questions that matter: can they "
                        "walk a straight line (ataxia = HACE) and "
                        "are they breathless AT REST (HAPE)"],
        red_flags=["ANY ataxia, confusion or drowsiness at "
                   "altitude — HACE: descend NOW, dexamethasone, "
                   "this kills",
                   "breathlessness at rest, cough, blue lips — "
                   "HAPE: descend NOW, oxygen if available",
                   "symptoms worsening despite a rest day, or "
                   "vomiting preventing fluids"],
        investigations=[],
        management_first_line="Stop ascending; rest at the SAME "
                              "altitude or descend 300-500 m. "
                              "Analgesia + antiemetic, fluids. "
                              "Acetazolamide helps acclimatisation "
                              "(and can be used preventively "
                              "3000 m+). Hyperbaric bag only "
                              "bridges to descent — DESCENT is the "
                              "treatment.",
        referral_tier="routine",
        safety_net="Stumbling, slurred words, confusion, or "
                   "breathlessness lying down at altitude — "
                   "descend immediately, this is an emergency.",
        source="Wilderness Medical Society altitude; Lake Louise score",
    ),
    ConditionProfile(
        condition_id="hace_cerebral_edema_altitude",
        name="High-altitude cerebral oedema (HACE)",
        category="environmental",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("altitude_ataxia_confused", 0.85, 0.95),
            SymptomFrequency("altitude_exposure_context", 0.90, 0.85),
            SymptomFrequency("altitude_headache", 0.50, 0.50),
        ],
        discriminators=["ataxia (heel-to-toe FAILS) + confusion/"
                        "drowsiness at altitude — HACE is AMS with "
                        "BRAIN SIGNS; the finger-nose test on a "
                        "trek saves lives",
                        "may evolve with HAPE together — check "
                        "chest and gait"],
        red_flags=["coma, seizures, retinal haemorrhages — "
                   "critical; death from herniation within hours",
                   "descent is the only definitive treatment — "
                   "everything else buys time"],
        investigations=[],
        management_first_line="DESCEND IMMEDIATELY (even at night, "
                              "assisted). Dexamethasone 8 mg then "
                              "4 mg 6-hourly NOW, oxygen if "
                              "available, hyperbaric bag as bridge. "
                              "Never leave the patient to walk "
                              "alone — ataxia means THEY CANNOT "
                              "JUDGE IT.",
        referral_tier="emergency",
        safety_net="Anyone stumbling or muddled at altitude "
                   "descends NOW with help — no exceptions, no "
                   "waiting for morning.",
        dangerous_mimic_of=["stroke_tia", "hypoglycaemia_suspect"],
        source="WMS altitude guidelines",
    ),
    ConditionProfile(
        condition_id="hape_pulmonary_edema_altitude",
        name="High-altitude pulmonary oedema (HAPE)",
        category="environmental",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("altitude_breathless_rest", 0.85, 0.92),
            SymptomFrequency("altitude_exposure_context", 0.90, 0.85),
            SymptomFrequency("altitude_cough_pink", 0.35, 0.85),
        ],
        discriminators=["reduced exercise capacity then breathless "
                        "AT REST, dry cough, then pink/frothy "
                        "sputum at altitude — a chest full of "
                        "water at 4000 m",
                        "worse lying flat, fine crackles on exam; "
                        "often a FAST ascender or previous HAPE "
                        "sufferer"],
        red_flags=["pink frothy sputum, cyanosis, collapse — "
                   "critical; death within hours without descent",
                   "HACE signs alongside — combined emergency"],
        investigations=[],
        management_first_line="DESCEND immediately (300-500 m "
                              "minimum, sitting upright, carried if "
                              "possible). Oxygen if available; "
                              "nifedipine slow-release as "
                              "adjunct; hyperbaric bag as bridge. "
                              "NO exertion — carrying the patient "
                              "is treatment. Re-ascent only after "
                              "full recovery plus acclimatisation.",
        referral_tier="emergency",
        safety_net="Breathless lying down, or cough turning pink, "
                   "at altitude — descend NOW, urgently.",
        dangerous_mimic_of=["community_pneumonia", "pe_pulmonary_embolism"],
        source="WMS altitude guidelines",
    ),
    ConditionProfile(
        condition_id="decompression_illness",
        name="Decompression illness (the bends)",
        category="environmental",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("dive_then_joint_pain", 0.70, 0.92),
            SymptomFrequency("dive_neuro_symptoms", 0.60, 0.95),
            SymptomFrequency("dive_skin_itch_mottling", 0.25, 0.75),
        ],
        discriminators=["symptoms within minutes to 24 h OF "
                        "SURFACING from a dive — pain (often "
                        "shoulder/elbow), rash, fatigue, numbness, "
                        "weakness, vertigo, bladder problems",
                        "'a dive' includes unpressurised light "
                        "aircraft and caisson/tunnel work",
                        "a patent foramen ovale shunts bubbles "
                        "neurologically in young divers — "
                        "unexplained neurological DCI warrants PFO "
                        "workup later"],
        red_flags=["ANY neurological symptom after diving — "
                   "emergency hyperbaric referral; 100% oxygen + "
                   "fluids while transferring",
                   "breathing difficulties or chest pain after "
                   "dives — pulmonary barotrauma plus DCI"],
        investigations=[],
        management_first_line="100% oxygen ASAP, flat/horizontal "
                              "(no sitting upright if neurological), "
                              "isotonic fluids, call the diving "
                              "medicine service (recompression "
                              "chamber) — treatments work days "
                              "later, so refer even delayed "
                              "presentations. NO re-descent, no "
                              "flying, hyperbaric therapy is the "
                              "definitive treatment.",
        referral_tier="emergency",
        safety_net="Numbness, weakness, odd rash or joint pain "
                   "after any dive — phone the diving medicine "
                   "service the same day, even days after.",
        dangerous_mimic_of=["stroke_tia", "transverse_myelitis_suspect"],
        source="DAN diving medicine; UHMS",
    ),
    ConditionProfile(
        condition_id="radiation_exposure",
        name="Acute radiation syndrome / exposure",
        category="environmental",
        prevalence_per_consult=0.00005,
        symptoms=[
            SymptomFrequency("radiation_source_context", 0.90, 0.95),
            SymptomFrequency("radiation_early_vomiting", 0.55, 0.85),
            SymptomFrequency("burn_like_rash_latency", 0.35, 0.85),
        ],
        discriminators=["a NAMED source or event (orphan sources "
                        "found/scavenged, industrial radiography, "
                        "nuclear accident, radiotherapy mishandling) "
                        "— the history IS the dosimetry",
                        "time-to-vomiting estimates dose: <1 h "
                        "after = severe; erythema appearing in "
                        "hours-to-days maps to skin dose",
                        "latent 'walking ghost' phase fools "
                        "everyone — the symptom-free interval "
                        "before pancytopenia"],
        red_flags=["vomiting within an hour, confusion, or "
                   "erythema/burns without a burn story — "
                   "emergency specialist + radiation protection "
                   "authority NOW",
                   "contamination vs irradiation: contamination "
                   "needs decontamination BEFORE transport spreads "
                   "it"],
        investigations=[
            InvestigationProfile("CBC with differential serially "
                                 "(lymphocyte depletion kinetics "
                                 "dose-estimate), chromosomal "
                                 "dicentric assay via specialist "
                                 "centres",
                                 "the blood count is the dosimeter",
                                 0.90, 0.90, "REAC/TS; WHO REMPAN"),
        ],
        management_first_line="Emergency services + radiation "
                              "protection authority. Life-saving "
                              "trauma care FIRST (with PPE), then "
                              "decontamination (clothes off = "
                              "80-90% of contamination), "
                              "supportive care by syndrome (fluids, "
                              "infection prophylaxis when "
                              "neutropenic, cytokines per "
                              "specialist). Do NOT transport "
                              "contaminated patients unadvised.",
        referral_tier="emergency",
        safety_net="Anyone with vomiting or skin burns after "
                   "handling a found metal object or industrial "
                   "source — treat as radiation emergency and "
                   "involve the authorities immediately.",
        source="WHO REMPAN; REAC/TS guidance",
    ),

    # ================= GLOBAL HAEMATOLOGY / POST-INFECTIOUS =========
    ConditionProfile(
        condition_id="sickle_vaso_occlusive_crisis",
        name="Sickle cell vaso-occlusive crisis",
        category="haematology",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("known_sickle_cell", 0.90, 0.97),
            SymptomFrequency("severe_bone_pain_back_legs", 0.75, 0.75),
            SymptomFrequency("fever", 0.25, 0.05),
        ],
        discriminators=["KNOWN sickle disease + severe back/limb/"
                        "chest pain = crisis until proven "
                        "otherwise — the patient has had hundreds "
                        "and knows their baseline; 'different from "
                        "usual' is data",
                        "triggers: infection, cold, dehydration, "
                        "hypoxia (flights), exertion — but most "
                        "have no trigger",
                        "pain out of proportion to examination "
                        "findings is expected — do not "
                        "under-analgaese"],
        red_flags=["chest pain, breathlessness, cough or falling "
                   "sats = ACUTE CHEST SYNDROME — the killer: "
                   "emergency, escalate fast",
                   "painful persistent erection (priapism) — "
                   "emergency urology",
                   "new focal neurology (stroke — children "
                   "especially) or sudden pallor + massive spleen "
                   "(sequestration) — emergency",
                   "fever + crisis = assume infection; antibiotics "
                   "early"],
        investigations=[
            InvestigationProfile("FBC + reticulocytes (baseline "
                                 "comparison), pain score, sats, "
                                 "urinalysis; chest X-ray if ANY "
                                 "chest sign",
                                 "reticulocytopenia warns of "
                                 "aplastic crisis (parvovirus B19)",
                                 0.85, 0.85, "NICE sickle cell; "
                                 "NHS Sickle standards"),
        ],
        management_first_line="Trust the patient's pain: opioid "
                              "within 30 minutes (many have "
                              "portacaths/protocols), plus fluids, "
                              "oxygen only if hypoxic, warmth, "
                              "infection screen. Discharge planning "
                              "needs analgesia that actually works "
                              "at home and a written personal "
                              "protocol. Hydroxycarbamide review "
                              "if frequent crises.",
        referral_tier="emergency",
        safety_net="Chest pain, breathlessness, fever, new "
                   "weakness or hours-long erection in sickle "
                   "disease — emergency now, not tomorrow.",
        dangerous_mimic_of=["osteomyelitis_suspect", "pe_pulmonary_embolism"],
        source="NICE sickle cell acute; NHS England standards",
    ),
    ConditionProfile(
        condition_id="acute_rheumatic_fever",
        name="Acute rheumatic fever",
        category="cardiovascular",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("migratory_joint_pain_young", 0.75, 0.90),
            SymptomFrequency("recent_sore_throat_joints", 0.40, 0.80),
            SymptomFrequency("jerky_involuntary_movements", 0.15, 0.95),
            SymptomFrequency("fever", 0.60, 0.05),
        ],
        discriminators=["migratory LARGE-joint arthritis (knee → "
                        "ankle → elbow) 2-4 weeks after a sore "
                        "throat, in 5-14 year-olds (or endemic-"
                        "area/Aboriginal/Pacific/Maori populations "
                        "at any age)",
                        "Jones major criteria: carditis (listen "
                        "for the murmur!), polyarthritis, chorea, "
                        "erythema marginatum, subcutaneous nodules",
                        "in high-burden settings the threshold is "
                        "LOWER — a suspicious joint + recent strep "
                        "deserves echo"],
        red_flags=["chest pain, breathlessness, new murmur or "
                   "heart failure signs — carditis: urgent "
                   "admission (this is the valve disease of later "
                   "life being decided NOW)",
                   "chorea or inability to walk"],
        investigations=[
            InvestigationProfile("Throat swab + rising ASO/anti-"
                                 "DNAse B titres, ESR/CRP, ECG (PR "
                                 "prolongation), echocardiogram "
                                 "(ALL suspected cases — subclinical "
                                 "carditis counts)",
                                 "echo changes management even "
                                 "without a murmur", 0.85, 0.90,
                                 "WHO rheumatic fever; AHA Jones "
                                 "criteria revision"),
        ],
        management_first_line="Refer paediatrics/medicine: aspirin/"
                              "NSAIDs for arthritis, penicillin to "
                              "clear the strep (and SECONDARY "
                              "prophYLAXIS monthly benzathine "
                              "penicillin for years — the "
                              "recurrence, not the first attack, "
                              "destroys valves), carditis managed "
                              "by severity. Household strep "
                              "screening in endemic settings.",
        referral_tier="urgent",
        safety_net="A limping child with a recent sore throat and "
                   "any breathlessness or murmur — same-day "
                   "assessment.",
        dangerous_mimic_of=["septic_arthritis_suspect",
                            "iga_vasculitis_hsp"],
        source="WHO RF/RHD; AHA Jones revision",
    ),

    # ================= HUMAN-RIGHTS SENSITIVE CARE ===================
    ConditionProfile(
        condition_id="fgm_care_needs",
        name="Female genital mutilation — care and safeguarding",
        category="safeguarding",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("fgm_disclosure", 0.80, 0.95),
            SymptomFrequency("fgm_urinary_period_problems", 0.50, 0.80),
            SymptomFrequency("dyspareunia_chronic", 0.30, 0.50),
        ],
        discriminators=["disclosure phrasings vary: 'been cut', "
                        "'circumcised as a girl', 'closed up', "
                        "'sewn' — ask gently, never investigate "
                        "repeatedly",
                        "obstetric/urinary/menstrual/psychosexual "
                        "complications follow type 3 "
                        "(infibulation) most",
                        "pregnancy: deinfibulation planning "
                        "BEFORE labour, with consent and control "
                        "with the woman"],
        red_flags=["a girl under 18 with FGM OR at risk (family "
                   "travel plans to practising communities, "
                   "sisters cut) — mandatory reporting + "
                   "safeguarding referral: this is a legal duty "
                   "in the UK",
                   "rapid decompensation of type 3 with urinary "
                   "retention — urgent urogynaecology"],
        investigations=[],
        management_first_line="Person-led: ask what she wants, "
                              "explain what was done in her words, "
                              "offer specialist FGM clinic "
                              "(deinfibulation, psychosexual "
                              "support), document TYPE precisely "
                              "(WHO I-IV) with a diagram, and "
                              "safeguard any at-risk girls. NEVER "
                              "re-infibulate after delivery or "
                              "procedures. Interpreter: independent, "
                              "same language, never a family "
                              "member.",
        referral_tier="urgent",
        safety_net="Any girl at risk of being cut, or any woman "
                   "with urinary retention or pregnancy "
                   "complications from FGM — same-day senior "
                   "review.",
        dangerous_mimic_of=["vulval_pain_suspect"],
        source="WHO FGM; RCOG FGM green-top; UK mandatory reporting duty",
    ),
    ConditionProfile(
        condition_id="torture_survivor_care",
        name="Torture survivor — trauma-informed care",
        category="mental_health",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("torture_disclosure", 0.70, 0.95),
            SymptomFrequency("scars_from_beatings", 0.35, 0.80),
            SymptomFrequency("trauma_nightmares", 0.50, 0.40),
            SymptomFrequency("flashbacks", 0.45, 0.45),
            SymptomFrequency("chronic_pain_years", 0.40, 0.30),
        ],
        discriminators=["presentations are INDIRECT: chronic pain, "
                        "sleeplessness, panic, unexplained scars, "
                        "or an asylum/medico-legal report request "
                        "— disclosure may come only when trust "
                        "exists, sometimes never",
                        "physical after-effects (fractures healed "
                        "deformed, nerve damage, hearing loss, "
                        "scarring in patterns) sit beside PTSD/"
                        "depression",
                        "the consultation itself can re-traumatise: "
                        "control, consent and pacing ARE the "
                        "treatment"],
        red_flags=["active suicidality or self-harm — mental "
                   "health crisis pathway",
                   "disclosure of ongoing contact with perpetrators "
                   "or threats to family — safety planning"],
        investigations=[
            InvestigationProfile("Only what the survivor consents "
                                 "to and that serves them; medico-"
                                 "legal documentation (Istanbul "
                                 "Protocol) when they choose it",
                                 "an examination without consent "
                                 "repeats the harm", 0.80, 0.80,
                                 "Istanbul Protocol; Freedom from "
                                 "Torture"),
        ],
        management_first_line="Trauma-informed: explain everything "
                              "before doing it, offer chaperone and "
                              "independent interpreter (never "
                              "family), stop on request. Treat "
                              "PTSD/depression (trauma-focused "
                              "therapy first-line), pain, and "
                              "physical sequelae. Specialist "
                              "torture-rehab services (e.g. Freedom "
                              "from Torture) for therapy and "
                              "medico-legal reports. Document "
                              "facts verbatim — asylum outcomes "
                              "may hang on the GP record.",
        referral_tier="routine",
        safety_net="Any talk of ending their life, or fresh "
                   "injuries from threats — same-day crisis "
                   "assessment.",
        dangerous_mimic_of=["ptsd_suspect", "chronic_primary_pain"],
        source="Istanbul Protocol; WHO torture survivor care",
    ),
]

# ---------------------------------------------------------------------------
# Synonym maps. Geography tokens deliberately carry LOW specificity
# (<= 0.55) in the entries above: a place name can only ever SUPPORT a
# symptom token, never lead — the Nepal-trek lesson.
# ---------------------------------------------------------------------------
SYMPTOM_SYNONYMS_PART6: Dict[str, List[str]] = {
    # --- chronic viral ---
    "known_hep_b_carrier": [
        "hepatitis b carrier", "hep b carrier", "known hepatitis b",
        "i have hepatitis b", "hepatitis b for years",
        "found out i had hepatitis b", "hep b for years",
    ],
    "hep_b_blood_result": [
        "surface antigen positive", "hbsag positive",
        "hepatitis b surface antigen", "hep b antigen positive",
        "hbv positive", "hbv dna",
    ],
    "hep_c_antibody_found": [
        "hepatitis c antibody positive", "hep c antibody",
        "hepatitis c positive", "hep c positive",
        "hep c antibodies found", "hcv positive",
        "hepatitis c virus detected",
    ],
    "past_injection_drug_use": [
        "used to inject", "injected in the past",
        "past injecting", "i injected years ago",
        "history of injecting", "used needles years ago",
    ],
    "recurrent_thrush_shingles": [
        "shingles twice", "shingles again", "shingles three times",
        "recurrent shingles", "thrush keeps coming back",
        "thrush again and again", "oral thrush recurring",
        "recurrent oral thrush", "constant thrush",
    ],
    "recurrent_infections_years": [
        "one infection after another", "always getting infections",
        "infections all the time", "every month another infection",
        "chest infection after chest infection", "boils keep coming",
    ],
    "prep_request": [
        "prep", "on prep", "start prep", "taking prep",
        "truvada", "want prep",
    ],
    "condomless_multiple_partners": [
        "condomless sex with", "without condoms with",
        "multiple partners", "new partners regularly",
    ],
    # --- neglected tropical + zoonotic ---
    "numb_pale_patches": [
        "patches that feel numb", "patch that feels numb",
        "numb white patch", "numb pale patches", "pale patch i can't feel",
        "can't feel the patch", "lost feeling in the patch",
        "numb spots on my skin", "patch has no feeling",
        "numb patches", "numb patch", "patches are numb",
        "patch is numb", "skin that feels numb", "skin that feel numb",
        "can't feel a patch", "patch on my skin i can't feel",
        "numb pale patch", "pale patches that are numb",
    ],
    "skin_numbness_months": [
        "skin feels numb", "numbness in the skin",
        "lost sensation in a patch", "numb area of skin",
    ],
    "nerve_thickening_palpable": [
        "thickened nerve", "nerve feels thick",
        "lumpy nerve at the elbow", "thickened nerves",
        "nerve enlargement",
    ],
    "endemic_area_long_stay": [
        "worked in india", "worked in africa", "lived in brazil",
        "years in nigeria", "grew up in bangladesh",
        "lived in africa", "years in india", "lived in nepal",
        "worked in pakistan", "years in indonesia",
    ],
    "seizure_adult_new": [
        "first seizure", "never had a seizure before",
        "new seizure", "first fit",
    ],
    "brain_cysts_imaging": [
        "cysts in the brain", "cysts on the scan",
        "multiple cysts on ct", "multiple cysts on the scan",
        "brain cysts", "cystic lesions in the brain",
    ],
    "pork_tapeworm_exposure": [
        "undercooked pork", "raw pork", "tapeworm in my stool",
        "tapeworm passed", "pigs at home", "pig farm",
        "ate pork in the village",
    ],
    "undulant_fever_waves": [
        "fever that comes and goes", "fever comes and goes",
        "fever in waves", "on and off fever for weeks",
        "fever every few days", "fever keeps returning",
        "fever for weeks that comes and goes",
    ],
    "raw_dairy_exposure": [
        "unpasteurised milk", "unpasteurized milk", "raw milk",
        "cheese from the farm", "milk straight from the cow",
        "farm cheese", "raw goat milk", "unpasteurised cheese",
    ],
    "farm_animal_contact": [
        "work with cattle", "sheep farmer", "cattle farmer",
        "abattoir", "slaughterhouse", "work with animals on the farm",
        "lambing season", "i am a vet", "work as a vet",
    ],
    "soil_water_exposure_endemic": [
        "waded through flood water", "cut my foot in the paddy",
        "paddy field", "flood water", "soil through a cut",
        "gardening barefoot", "stood in the rice field",
        "muddy water cut",
    ],
    "pneumonia_not_responding": [
        "not responding to antibiotics", "antibiotics not working",
        "pneumonia not responding", "still feverish on antibiotics",
        "worse on antibiotics",
    ],
    "sepsis_picture": [
        "blood pressure dropping", "cold and clammy",
        "confused and feverish", "racing heart and fever",
    ],
    "se_asia_stay_low": [
        "in thailand", "in vietnam", "in cambodia",
        "in laos", "northern australia", "in myanmar",
        "darwin",
    ],
    "atypical_pneumonia_hepatitis": [
        "patchy pneumonia", "abnormal liver tests with fever",
        "liver enzymes raised with fever",
    ],
    "chagas_screen_positive": [
        "chagas", "chagas positive", "chagas antibody",
        "blood donation letter", "transfusion service letter",
        "donation rejected", "screen positive for chagas",
    ],
    "latin_america_rural_origin": [
        "from bolivia", "from peru", "from paraguay",
        "from rural mexico", "from argentina", "from chile",
        "grew up in bolivia", "from rural brazil",
        "from ecuador", "from colombia",
    ],
    "new_heart_block_cardiomyopathy": [
        "heart block", "cardiomyopathy", "pacemaker at 40",
        "heart failure at 45", "conduction problem",
    ],
    "daytime_somnolence_fever": [
        "falls asleep during the day", "can't stay awake",
        "sleeps all day", "sleepy all day", "daytime sleeping",
        "sleeps in the day awake at night",
    ],
    "tsetse_bite_history": [
        "tsetse", "fly bite in the bush", "tsetse fly",
        "bite in the savannah", "game park flies",
        "safari in", "back from safari", "back from a safari",
        "on safari", "african safari", "game drive",
    ],
    "posterior_cervical_nodes": [
        "glands at the back of the neck",
        "neck glands at the back", "swelling back of neck",
        "nodes at the back of the neck",
    ],
    "chronic_crater_ulcer": [
        "ulcer that won't heal", "ulcer not healing",
        "crater-like ulcer", "volcano ulcer", "ulcer with raised edges",
        "ulcer with a rim", "skin ulcer for weeks",
        "painless ulcer on the skin",
    ],
    "sandfly_region_stay": [
        "in the amazon", "middle east deployment",
        "deployed to iraq", "deployed to afghanistan",
        "in saudi", "sahara trip", "mediterranean coast",
        "in sudan", "in ethiopia",
    ],
    "enlarged_spleen_fever_months": [
        "spleen enlarged", "enlarged spleen", "big spleen",
        "swelling under the ribs on the left",
        "doctor said my spleen", "spleen palpable",
        "mass on the left under ribs",
    ],
    "pancytopenia_counts_low": [
        "all my blood counts are low", "pancytopenia",
        "low white cells and platelets",
        "blood counts all low", "low platelets and low whites",
    ],
    "skin_greyed_darkening": [
        "skin looks darker grey", "skin gone darker",
        "greyish skin colour", "kala azar darkening",
    ],
    "rice_water_stools": [
        "rice water", "like rice water", "pouring like tap water",
        "watery diarrhoea pouring out", "clear fluid diarrhoea",
        "diarrhoea like water from a tap",
    ],
    "rapid_dehydration_signs": [
        "sunken eyes", "skin pinch goes back slowly",
        "no urine since morning", "too weak to stand",
        "voice gone quiet and dry", "eyes sunken",
    ],
    "bite_site_tingling_weeks": [
        "tingling where the bite was", "itching at the old bite",
        "pain where i was bitten months ago",
        "tingling at the old scar", "strange feeling where bitten",
    ],
    "water_swallow_spasm_fear": [
        "scared of water", "spasms when drinking",
        "can't swallow water", "throat spasms at water",
        "hydrophobia", "panic at the sight of water",
        "spasms when i try to drink",
    ],
    "air_draft_fear_spasm": [
        "spasms when air touches", "fear of air on the face",
        "air triggers spasms", "can't bear drafts",
    ],
    "agitated_confused_bite_history": [
        "agitated after a bite", "confused after a bite abroad",
        "bitten months ago now confused",
    ],
    # --- environmental extremes ---
    "heat_exposure_context": [
        "working in the sun", "in the sun all day",
        "heatwave", "in the heat all day", "hot warehouse",
        "no air conditioning in the heat", "running in the heat",
        "roofing in the sun", "kitchen in a heatwave",
    ],
    "heavy_sweating_weak": [
        "sweating heavily", "drenched in sweat", "soaked with sweat",
        "weak and shaky in the heat", "sweating and weak",
    ],
    "muscle_cramps_heat": [
        "cramps in my muscles", "muscle cramps",
        "legs cramping in the heat",
    ],
    "hot_dry_confused": [
        "burning hot but not sweating", "hot and confused",
        "dry skin and confused", "stopped sweating",
        "not sweating and muddled", "confused in the heat",
        "acting strangely in the heat",
    ],
    "collapse_hot_environment": [
        "collapsed while running", "collapsed in the sun",
        "collapsed at work in the heat", "keeled over on the run",
    ],
    "core_temp_40_plus": [
        "temperature of 40", "temperature of 41",
        "temp of 40", "temp 41", "40.5 degrees", "41 degrees",
        "temperature reads 41", "temperature is 40",
    ],
    "cold_exposure_drowsy_confused": [
        "found cold and drowsy", "cold to touch and confused",
        "shivering has stopped", "found unresponsive and cold",
        "cold and muddled", "drowsy and cold to touch",
        "found on the floor cold",
    ],
    "core_temp_below_35": [
        "temperature of 33", "temperature of 34",
        "temp of 32", "temp 34", "temperature is 34",
        "temperature reads 33", "core temperature 33",
        "temperature of 32",
    ],
    "cold_water_immersion": [
        "fell in the river", "fell into cold water",
        "cold water immersion", "in the sea for an hour",
        "fell through the ice",
    ],
    "altitude_exposure_context": [
        "altitude", "at 4000 metres", "at 3500 metres",
        "at 3000 metres", "at 4500 metres", "at 5000 metres",
        "at 5500 metres", "high camp", "trekking up",
        "climbing at", "base camp", "above 2500",
        "kilimanjaro", "everest base camp", "high pass",
        "metres up", "meters up", "the summit", "above the tree line",
    ],
    "altitude_headache": [
        "headache at altitude", "altitude headache",
        "headache since we climbed", "headache up high",
        "headache since the ascent",
    ],
    "altitude_nausea_fatigue": [
        "sick at altitude", "nauseous since the climb",
        "exhausted at altitude", "can't sleep at altitude",
        "dizzy on the trek",
    ],
    # every phrase here binds to an altitude/camp/pass/trail word: the
    # guard test proves a pub-stumble story ("stumbling like he's drunk
    # at the pub") never fires HACE. Ataxia alone below the tree line
    # is a hundred benign things.
    "altitude_ataxia_confused": [
        "stumbling at altitude", "acting drunk at altitude",
        "can't walk straight at altitude", "confused at height",
        "muddled since the pass", "stumbling on the trek",
        "not making sense at base camp", "confused at altitude",
        "not making sense at altitude",
        "stumbling around camp", "muddled at camp",
        "stumbling on the trail", "stumbling on the descent",
        "falling over on the descent", "stumbling on the path",
        "stumbles at camp", "stumbling since the pass",
        "walking drunk at altitude", "like he's drunk at altitude",
        "like she's drunk at altitude", "ataxia at altitude",
        "can't walk a straight line at altitude",
        "fails heel-to-toe at altitude", "heel-to-toe fails at camp",
    ],
    "altitude_breathless_rest": [
        "breathless at rest", "can't lie flat at altitude",
        "breathless at altitude", "gasping at camp",
        "breathless since the pass",
    ],
    "altitude_cough_pink": [
        "cough at altitude", "coughing up pink",
        "frothy sputum at altitude", "pink phlegm at altitude",
    ],
    "dive_then_joint_pain": [
        "after surfacing", "the bends", "joint pain after diving",
        "shoulder pain after the dive", "pain after surfacing",
        "elbow pain after a dive", "since i surfaced",
    ],
    "dive_neuro_symptoms": [
        "numbness after the dive", "pins and needles since surfacing",
        "weakness after diving", "numbness after diving",
        "vertigo after the dive", "can't feel my legs after the dive",
        "bladder problems after diving",
    ],
    "dive_skin_itch_mottling": [
        "itching skin after the dive", "skin mottling after diving",
        "rash after the dive", "skin feels itchy since surfacing",
    ],
    "radiation_source_context": [
        "radioactive", "radiation source", "nuclear accident",
        "contaminated source", "cesium", "caesium source",
        "cobalt source", "radiography camera", "orphan source",
        "found a metal capsule", "reactor",
    ],
    "radiation_early_vomiting": [
        "vomiting within an hour of", "vomited within minutes of",
        "threw up right after handling",
    ],
    "burn_like_rash_latency": [
        "burn like rash", "rash like sunburn appearing",
        "skin peeling in patches", "blistering without heat",
    ],
    # --- global haematology / post-infectious ---
    "known_sickle_cell": [
        "sickle cell", "sickle cell disease", "my sickle",
        "crisis coming on", "sickler", "hbss", "hbsc",
        "sickle crisis",
    ],
    "severe_bone_pain_back_legs": [
        "pain in my back and legs", "bone pain",
        "pain in the bones of my legs", "legs and back agony",
    ],
    "migratory_joint_pain_young": [
        "moved from knee to ankle", "one joint then another",
        "jumping from joint to joint", "started in the knee then the ankle",
        "arthritis moving between joints",
        "moved to the ankle", "moved to the other", "pain moved",
        "moved from the knee", "started in the knee then",
        "moved to his", "moved to her", "then the ankle",
        "then the elbow", "then the other knee", "joint to joint",
    ],
    "recent_sore_throat_joints": [
        "sore throat a few weeks ago", "strep throat before",
        "bad throat two weeks before", "tonsillitis a few weeks ago",
    ],
    "jerky_involuntary_movements": [
        "jerky movements", "can't sit still", "chorea",
        "involuntary jerking", "fidgety uncontrollable movements",
    ],
    # --- human-rights sensitive care ---
    "fgm_disclosure": [
        "fgm", "been cut", "circumcised as a girl",
        "closed up down below", "infibulated", "sewn up",
        "they cut me as a child", "female circumcision",
    ],
    "fgm_urinary_period_problems": [
        "periods take days to drain", "period trickle slowly",
        "difficulty passing urine slowly", "wee comes out slowly",
        "periods painful since being cut",
    ],
    "dyspareunia_chronic": [
        "pain during sex", "sex is painful",
    ],
    "torture_disclosure": [
        "was tortured", "tortured in", "detained and beaten",
        "asylum claim", "claimed asylum", "escaped detention",
        "political prisoner", "beaten in custody",
    ],
    "scars_from_beatings": [
        "scars on my back from", "whip marks", "whip scars",
        "cigarette burns", "cigarette burn scars",
        "scars from beatings",
    ],
    "chronic_pain_years": [
        "pain for years", "aches for years",
    ],
}
