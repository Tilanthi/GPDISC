"""Stage 1 Task 2: breadth corpus — systematic coverage across systems.

Categories: endocrine, infection, paediatric, geriatric_frailty,
mental_health, musculoskeletal, dermatology, ent_eye, womens_health,
urology_kidney, haematology, plus a tropical taster (full tropical module
is Stage 2). Emergency-weighted: every entry that is a dangerous mimic of
a benign presentation says so in ``dangerous_mimic_of``.

Merged into knowledge.CONDITIONS at import; symptom tokens must appear in
SYMPTOM_SYNONYMS_PART2 (the corpus integrity test enforces it).
"""
from typing import Dict, List

from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
)

CONDITIONS_PART2: List[ConditionProfile] = [
    # ================= ENDOCRINE =================
    ConditionProfile(
        condition_id="t1dm_new",
        name="New type 1 diabetes",
        category="endocrine",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("polyuria", 0.85, 0.75),
            SymptomFrequency("polydipsia", 0.85, 0.70),
            SymptomFrequency("weight_loss", 0.70, 0.40),
            SymptomFrequency("fatigue", 0.70, 0.05),
            SymptomFrequency("ketone_breath", 0.25, 0.90),
        ],
        discriminators=["young/lean patient, onset over weeks",
                        "ketones present", "weight loss despite normal intake"],
        red_flags=["vomiting, drowsiness or breathlessness -> DKA"],
        investigations=[
            InvestigationProfile("capillary glucose", "immediate",
                                 0.95, 0.95, "NICE NG18 diabetes children"),
        ],
        management_first_line="Same-day specialist referral; confirm with glucose "
                              "+ ketones; never watch and wait (NICE NG17/NG18).",
        referral_tier="urgent",
        safety_net="Vomiting, sleepiness, deep sighing breathing or fruity-smelling "
                   "breath — emergency same-day.",
        source="NICE NG17/NG18 diabetes",
    ),
    ConditionProfile(
        condition_id="t2dm_new",
        name="New type 2 diabetes",
        category="endocrine",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("polyuria", 0.60, 0.35),
            SymptomFrequency("polydipsia", 0.55, 0.30),
            SymptomFrequency("fatigue", 0.60, 0.05),
            SymptomFrequency("recurrent_infections", 0.25, 0.35),
            SymptomFrequency("blurred_vision", 0.20, 0.20),
        ],
        discriminators=["gradual onset, older/obese, family history",
                        "HbA1c >= 48 mmol/mol on two samples"],
        red_flags=["osmotic symptoms with ketones or weight loss — exclude T1DM/DKA"],
        investigations=[
            InvestigationProfile("HbA1c", "diagnostic >= 48 mmol/mol",
                                 0.90, 0.95, "NICE NG28 diabetes"),
        ],
        management_first_line="Structured education, metformin if HbA1c >= 48, "
                              "cardiovascular risk review, retinal screening "
                              "referral (NICE NG28).",
        referral_tier="routine",
        safety_net="Rapid weight loss, vomiting or drowsiness — same-day review "
                   "(possible insulin deficiency).",
        source="NICE NG28 type 2 diabetes",
    ),
    ConditionProfile(
        condition_id="dka",
        name="Diabetic ketoacidosis",
        category="endocrine",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("vomiting", 0.70, 0.15),
            SymptomFrequency("abdominal_pain", 0.50, 0.15),
            SymptomFrequency("breathlessness", 0.50, 0.15),
            SymptomFrequency("drowsiness", 0.50, 0.40),
            SymptomFrequency("polyuria", 0.60, 0.30),
            SymptomFrequency("polydipsia", 0.60, 0.30),
            SymptomFrequency("ketone_breath", 0.40, 0.90),
            SymptomFrequency("weight_loss", 0.40, 0.20),
        ],
        discriminators=["known T1DM or new insulin-deficient presentation",
                        "glucose high + ketones >= 3", "Kussmaul breathing"],
        red_flags=["drowsiness", "vomiting everything", "any DKA suspicion = emergency"],
        investigations=[
            InvestigationProfile("capillary ketones", ">= 3 mmol/L supports DKA",
                                 0.90, 0.90, "JBDS DKA guidance"),
        ],
        management_first_line="Call 999 — hospital admission, fixed-rate IV insulin, "
                              "fluids, potassium monitoring (JBDS/IPU DKA guidance).",
        referral_tier="emergency",
        safety_net="A person with diabetes who is vomiting, drowsy or breathless — "
                   "999 immediately.",
        dangerous_mimic_of=["gastroenteritis", "viral_urti"],
        source="JBDS DKA guideline 2021; NICE NG17",
    ),
    ConditionProfile(
        condition_id="hhs",
        name="Hyperosmolar hyperglycaemic state",
        category="endocrine",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("drowsiness", 0.70, 0.55),
            SymptomFrequency("confusion", 0.50, 0.30),
            SymptomFrequency("polyuria", 0.80, 0.30),
            SymptomFrequency("polydipsia", 0.80, 0.30),
            SymptomFrequency("dehydration_signs", 0.70, 0.55),
        ],
        discriminators=["older T2DM patient, glucose often >30, little ketosis",
                        "days-weeks of deterioration"],
        red_flags=["any reduced consciousness with hyperglycaemia = emergency"],
        investigations=[
            InvestigationProfile("capillary glucose", "markedly elevated",
                                 0.95, 0.80, "JBDS HHS guidance"),
        ],
        management_first_line="Call 999 — admission; careful slow fluid rehydration "
                              "and insulin infusion (JBDS HHS guidance).",
        referral_tier="emergency",
        safety_net="An older person with diabetes becoming drowsy and very dry-mouthed "
                   "over days — emergency.",
        dangerous_mimic_of=["delirium", "frailty_decompensation"],
        source="JBDS HHS guideline",
    ),
    ConditionProfile(
        condition_id="hypoglycaemia",
        name="Hypoglycaemia",
        category="endocrine",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("sweating", 0.70, 0.30),
            SymptomFrequency("tremor", 0.60, 0.45),
            SymptomFrequency("confusion", 0.50, 0.25),
            SymptomFrequency("hunger", 0.50, 0.50),
            SymptomFrequency("drowsiness", 0.40, 0.30),
            SymptomFrequency("seizure", 0.10, 0.25),
        ],
        discriminators=["insulin/sulfonylurea user", "rapid onset, resolves with glucose",
                        "Whipple triad"],
        red_flags=["severe (needs third-party help)", "unconscious", "recurrent hypos"],
        investigations=[
            InvestigationProfile("capillary glucose", "<4.0 mmol/L confirms",
                                 0.95, 0.95, "NICE NG17 hypo management"),
        ],
        management_first_line="Conscious: 15-20 g fast-acting carbohydrate, repeat at "
                              "15 min; review regimen and driving advice; sulfonylurea "
                              "hypos need observation (NICE NG17).",
        referral_tier="emergency",
        safety_net="Drowsy or unable to swallow — 999; glucagon if available.",
        dangerous_mimic_of=["stroke_tia", "alcohol_intoxication_pending"],
        source="NICE NG17; Diabetes UK hypo guidance",
    ),
    ConditionProfile(
        condition_id="hypothyroidism",
        name="Hypothyroidism",
        category="endocrine",
        prevalence_per_consult=0.015,
        symptoms=[
            SymptomFrequency("fatigue", 0.80, 0.10),
            SymptomFrequency("weight_gain", 0.50, 0.30),
            SymptomFrequency("cold_intolerance", 0.55, 0.55),
            SymptomFrequency("constipation", 0.40, 0.25),
            SymptomFrequency("dry_skin", 0.50, 0.35),
            SymptomFrequency("hair_thinning", 0.35, 0.40),
        ],
        discriminators=["TSH high, T4 low", "slow-relaxing reflexes",
                        "insidious over months"],
        red_flags=["hypothermia, bradycardia, drowsiness — myxoedema coma (rare)"],
        investigations=[
            InvestigationProfile("TSH then T4", "diagnostic cascade",
                                 0.95, 0.95, "NICE NG145 thyroid"),
        ],
        management_first_line="Levothyroxine starting dose by age/cardiac status "
                              "(25 mcg if >70 or cardiac); recheck TSH 6-8 weeks "
                              "(NICE NG145).",
        referral_tier="routine",
        safety_net="Confusion, very slow pulse or low temperature — emergency.",
        source="NICE NG145 thyroid disease",
    ),
    ConditionProfile(
        condition_id="hyperthyroidism",
        name="Hyperthyroidism / thyrotoxicosis",
        category="endocrine",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("weight_loss", 0.60, 0.30),
            SymptomFrequency("palpitations", 0.55, 0.25),
            SymptomFrequency("heat_intolerance", 0.55, 0.55),
            SymptomFrequency("tremor", 0.50, 0.40),
            SymptomFrequency("anxiety", 0.40, 0.15),
            SymptomFrequency("diarrhoea", 0.25, 0.20),
            SymptomFrequency("goitre", 0.40, 0.50),
        ],
        discriminators=["TSH suppressed", "lid lag/stare", " Graves orbitopathy"],
        red_flags=["AF, heart failure", "fever + agitation + delirium = thyroid storm",
                   "eye signs need urgent ophthalmology pathway"],
        investigations=[
            InvestigationProfile("TSH then T4/T3", "diagnostic cascade",
                                 0.95, 0.95, "NICE NG145"),
        ],
        management_first_line="Refer to endocrine for cause (Graves/nodular); beta-blocker "
                              "for symptoms; block-and-replace or carbimazole "
                              "(NICE NG145).",
        referral_tier="routine",
        safety_net="Fever, marked agitation or confusion with overactive thyroid signs — "
                   "emergency (thyroid storm).",
        source="NICE NG145 thyroid disease",
    ),
    ConditionProfile(
        condition_id="addisonian_crisis",
        name="Adrenal crisis (Addisonian)",
        category="endocrine",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("dizziness", 0.70, 0.20),
            SymptomFrequency("vomiting", 0.80, 0.20),
            SymptomFrequency("abdominal_pain", 0.50, 0.10),
            SymptomFrequency("fatigue", 0.90, 0.05),
            SymptomFrequency("hyperpigmentation", 0.50, 0.85),
            SymptomFrequency("confusion", 0.40, 0.25),
        ],
        discriminators=["known Addison/long-term steroids missed", "hyponatraemia + "
                        "hyperkalaemia + hypoglycaemia", "postural drop"],
        red_flags=["hypotension with vomiting", "collapse"],
        investigations=[
            InvestigationProfile("short Synacthen test", "confirms (after hydrocortisone "
                                 "if crisis)", 0.95, 0.95, "NICE endocrine"),
        ],
        management_first_line="Suspected crisis: call 999; IM hydrocortisone 100 mg "
                              "immediately + IV fluids; do not delay for tests.",
        referral_tier="emergency",
        safety_net="Steroid-dependent person vomiting or collapsing — emergency "
                   "(needs injectable hydrocortisone).",
        dangerous_mimic_of=["gastroenteritis", "viral_urti"],
        source="Addison's clinical guidance; ADSHG",
    ),
    ConditionProfile(
        condition_id="hypercalcaemia_malignancy",
        name="Hypercalcaemia (incl. malignancy-related)",
        category="endocrine",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("confusion", 0.40, 0.30),
            SymptomFrequency("polyuria", 0.40, 0.25),
            SymptomFrequency("polydipsia", 0.45, 0.30),
            SymptomFrequency("constipation", 0.45, 0.25),
            SymptomFrequency("abdominal_pain", 0.35, 0.10),
            SymptomFrequency("bone_pain", 0.30, 0.55),
            SymptomFrequency("fatigue", 0.70, 0.05),
        ],
        discriminators=["'bones, stones, groans, moans'", "adjusted calcium >3.0 = severe",
                        "weight loss or known cancer"],
        red_flags=["calcium >3.0 mmol/L with confusion/vomiting", "dehydration"],
        investigations=[
            InvestigationProfile("adjusted serum calcium", "severity",
                                 0.95, 0.95, "local biochemistry protocol"),
        ],
        management_first_line="Symptomatic or >3.0: admit for IV fluids and bisphosphonate; "
                              "seek cause (myeloma, malignancy, hyperparathyroidism).",
        referral_tier="urgent",
        safety_net="Confusion with vomiting and constipation needs urgent bloods.",
        dangerous_mimic_of=["delirium"],
        source="Standard endocrine practice",
    ),

    # ================= INFECTION =================
    ConditionProfile(
        condition_id="sepsis",
        name="Sepsis",
        category="infection",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("fever", 0.70, 0.10),
            SymptomFrequency("confusion", 0.40, 0.35),
            SymptomFrequency("fast_breathing", 0.50, 0.45),
            SymptomFrequency("reduced_urine_output", 0.40, 0.50),
            SymptomFrequency("dizziness", 0.35, 0.15),
            SymptomFrequency("shivering_rigors", 0.40, 0.30),
        ],
        discriminators=["source + systemic upset", "NEWS2 >= 5",
                        "immunocompromised/elderly may be afebrile"],
        red_flags=["hypotension", "confusion with fever", "mottled skin",
                   "not passing urine"],
        investigations=[
            InvestigationProfile("NEWS2", "escalation gate", None, None,
                                 "RCP NEWS2 2017"),
            InvestigationProfile("lactate + blood cultures", "severity + source",
                                 0.60, 0.70, "Sepsis Six"),
        ],
        management_first_line="Call 999; Sepsis Six within an hour in hospital; "
                              "in the community — urgent transfer, do not wait for "
                              "test results (NICE NG51 sepsis).",
        referral_tier="emergency",
        safety_net="Fever with confusion, fast breathing, mottled skin or no urine — "
                   "999 immediately.",
        dangerous_mimic_of=["viral_urti", "gastroenteritis", "influenza"],
        source="NICE NG51 sepsis; RCP NEWS2",
    ),
    ConditionProfile(
        condition_id="cellulitis",
        name="Cellulitis",
        category="infection",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("spreading_redness", 0.85, 0.85),
            SymptomFrequency("hot_swollen_skin", 0.80, 0.80),
            SymptomFrequency("fever", 0.30, 0.05),
        ],
        discriminators=["unilateral, warm, tender, demarcated edge",
                        "portal of entry (tinea, ulcer, bite)"],
        red_flags=["pain out of proportion / blisters / crepitus — necrotising "
                   "infection", "spreading fast", "systemic upset"],
        investigations=[],
        management_first_line="Flucloxacillin 500 mg QDS 5-7 days (clarithromycin if "
                              "allergic); mark erythema edge; escalate if spreading "
                              "(NICE cellulitis pathway/CKS).",
        referral_tier="routine",
        safety_net="Mark the border with a pen: if it spreads past it, or pain "
                   "worsens dramatically, urgent review.",
        dangerous_mimic_of=[],
        source="NICE/CKS cellulitis; Eron class",
    ),
    ConditionProfile(
        condition_id="influenza",
        name="Influenza",
        category="infection",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("fever", 0.80, 0.15),
            SymptomFrequency("myalgia", 0.80, 0.45),
            SymptomFrequency("cough", 0.70, 0.10),
            SymptomFrequency("sore_throat", 0.40, 0.10),
            SymptomFrequency("headache", 0.60, 0.10),
            SymptomFrequency("fatigue", 0.85, 0.10),
        ],
        discriminators=["sudden onset within hours", "myalgia prominent",
                        "seasonal/community activity"],
        red_flags=["breathlessness", "confusion", "deterioration day 3-5 "
                   "(secondary bacterial infection)"],
        investigations=[],
        management_first_line="Rest, fluids, analgesia; antivirals only if within "
                              "48 h AND at-risk group (per PHE/NICE); safety-net.",
        referral_tier="self_care",
        safety_net="Breathlessness, chest pain, confusion or improving then suddenly "
                   "worse — urgent review.",
        source="PHE/NICE influenza antiviral guidance",
    ),
    ConditionProfile(
        condition_id="tonsillitis_strep",
        name="Streptococcal tonsillitis",
        category="infection",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("sore_throat", 1.00, 0.30),
            SymptomFrequency("fever", 0.70, 0.10),
            SymptomFrequency("pus_on_tonsils", 0.60, 0.70),
            SymptomFrequency("swollen_glands", 0.60, 0.40),
        ],
        discriminators=["Centor/FeverPAIN score >= 4", "absence of cough/coryza",
                        "tonsillar exudate + tender anterior nodes"],
        red_flags=["trismus, muffled voice, uvular deviation (quinsy)",
                   "stridor/drooling — emergency"],
        investigations=[
            InvestigationProfile("FeverPAIN score", "strep probability gate",
                                 None, None, "FeverPAIN; NICE NG84 sore throat"),
        ],
        management_first_line="FeverPAIN 4-5: penicillin V 10 days (or delayed "
                              "prescription 3-4); analgesia (NICE NG84).",
        referral_tier="self_care",
        safety_net="Unable to swallow fluids, drooling, or voice muffled — urgent "
                   "same-day.",
        source="NICE NG84 sore throat",
    ),
    ConditionProfile(
        condition_id="otitis_media",
        name="Acute otitis media",
        category="infection",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("ear_pain", 0.90, 0.80),
            SymptomFrequency("fever", 0.50, 0.05),
            SymptomFrequency("reduced_hearing", 0.40, 0.30),
            SymptomFrequency("ear_discharge", 0.20, 0.60),
        ],
        discriminators=["bulging red tympanic membrane", "child 6-24 months",
                        "recent URTI"],
        red_flags=["mastoid pain/swelling (mastoiditis)", "facial palsy",
                   "under-3-months with fever — paediatric assessment"],
        investigations=[],
        management_first_line="Most resolve in 3-7 days: analgesia + safety-net "
                              "(delayed antibiotic); antibiotics if systemically "
                              "unwell, <2 y bilateral, or otorrhoea (NICE NG91).",
        referral_tier="self_care",
        safety_net="Swelling or pain behind the ear, drowsiness, or worsening after "
                   "48 h — urgent review.",
        source="NICE NG91 otitis media",
    ),
    ConditionProfile(
        condition_id="pyelonephritis",
        name="Acute pyelonephritis",
        category="infection",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("fever", 0.80, 0.20),
            SymptomFrequency("flank_pain", 0.75, 0.75),
            SymptomFrequency("dysuria", 0.60, 0.30),
            SymptomFrequency("vomiting", 0.40, 0.10),
            SymptomFrequency("shivering_rigors", 0.40, 0.40),
        ],
        discriminators=["fever + loin pain + urinary symptoms", "positive urine culture",
                        "systemic upset"],
        red_flags=["hypotension/confusion — urosepsis", "pregnancy", "unable to "
                   "tolerate oral"],
        investigations=[
            InvestigationProfile("urine culture", "confirm + sensitivity",
                                 0.80, 0.90, "NICE pyelonephritis guidance"),
        ],
        management_first_line="7-day oral cefalexin or quinolone per local resistance; "
                              "admit if systemically unwell, pregnant or vomiting "
                              "(NICE upper UTI).",
        referral_tier="urgent",
        safety_net="Vomiting, drowsiness or no urine — emergency review.",
        dangerous_mimic_of=["urinary_tract_infection_simple"],
        source="NICE upper UTI guidance (NG111 family)",
    ),
    ConditionProfile(
        condition_id="scarlet_fever",
        name="Scarlet fever",
        category="infection",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("fever", 0.85, 0.10),
            SymptomFrequency("sore_throat", 0.80, 0.20),
            SymptomFrequency("sandpaper_rash", 0.70, 0.90),
            SymptomFrequency("strawberry_tongue", 0.40, 0.85),
        ],
        discriminators=["rough sandpaper texture rash", "flushed face with perioral "
                        "pallor", "school/nursery contacts"],
        red_flags=["dehydrated/drowsy", "severe pain out of proportion (IGGAS)"],
        investigations=[],
        management_first_line="Phenoxymethylpenicillin 10 days (azithromycin 5 days if "
                              "allergic); exclude from school 24 h after antibiotics "
                              "start; notify the health protection team.",
        referral_tier="routine",
        safety_net="Drowsiness, not drinking, or pain far worse than expected — urgent.",
        source="PHE/UKHSA scarlet fever guidance",
    ),
    ConditionProfile(
        condition_id="measles",
        name="Measles",
        category="infection",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("fever", 0.95, 0.10),
            SymptomFrequency("blotchy_rash", 0.90, 0.80),
            SymptomFrequency("rhinorrhoea", 0.85, 0.15),
            SymptomFrequency("red_eye", 0.60, 0.30),
            SymptomFrequency("koplik_spots", 0.30, 0.95),
        ],
        discriminators=["prodrome 2-4 days then rash descending from face",
                        "unvaccinated / travel / outbreak link", "Koplik spots"],
        red_flags=["chest involvement / breathlessness", "drowsiness / convulsions "
                   "(encephalitis 1 in 1000)", "immunocompromised contact"],
        investigations=[
            InvestigationProfile("salivary MEASLES IgM / PCR", "confirm + notify",
                                 0.90, 0.95, "UKHSA measles guidance"),
        ],
        management_first_line="Notify UKHSA; confirm with oral fluid/saliva test; "
                              "isolation advice; supportive care; review complications "
                              "(otitis, pneumonia, encephalitis).",
        referral_tier="urgent",
        safety_net="Drowsiness, fits or breathlessness in suspected measles — emergency.",
        dangerous_mimic_of=["viral_urti"],
        source="UKHSA measles guidance; NICE CKS",
    ),
    ConditionProfile(
        condition_id="chickenpox",
        name="Chickenpox (varicella)",
        category="infection",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("vesicular_rash", 0.95, 0.90),
            SymptomFrequency("fever", 0.70, 0.05),
            SymptomFrequency("itchy_skin", 0.85, 0.40),
        ],
        discriminators=["crops of vesicles at different stages, centripetal",
                        "contact history", "unvaccinated child"],
        red_flags=["red painful skin around lesions (bacterial superinfection)",
                   "drowsiness/vomiting (cerebellitis, encephalitis)",
                   "adult, pregnant, immunosuppressed — higher risk, needs antiviral"],
        investigations=[],
        management_first_line="Supportive: fluids, paracetamol (NOT ibuprofen), "
                              "chlorphenamine/cooling for itch; aciclovir if adult, "
                              "pregnant contact risk or immunosuppressed (UKHSA).",
        referral_tier="self_care",
        safety_net="Skin around spots becoming red and painful, drowsiness, repeated "
                   "vomiting or breathlessness — urgent.",
        source="UKHSA chickenpox guidance; NICE CKS",
    ),
    ConditionProfile(
        condition_id="hiv_seroconversion",
        name="HIV seroconversion illness",
        category="infection",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("fever", 0.80, 0.05),
            SymptomFrequency("blotchy_rash", 0.50, 0.30),
            SymptomFrequency("sore_throat", 0.60, 0.05),
            SymptomFrequency("swollen_glands", 0.60, 0.35),
            SymptomFrequency("night_sweats", 0.40, 0.25),
            SymptomFrequency("fatigue", 0.80, 0.05),
        ],
        discriminators=["glandular-fever-like illness 2-6 weeks after exposure",
                        "multiple/anal ulceration", "test 4th-gen lab assay"],
        red_flags=["new diagnosis needs partner notification + immediate linkage "
                   "to care; CD4 <200 with symptoms = urgent"],
        investigations=[
            InvestigationProfile("4th-generation HIV test", "antigen+antibody",
                                 0.99, 0.99, "BHIVA/BASHH testing"),
        ],
        management_first_line="Test — do not treat empirically; urgent sexual health "
                              "referral if positive; offer PrEP/PEP context assessment.",
        referral_tier="urgent",
        safety_net="A glandular-fever-like illness after sexual exposure — test for HIV; "
                   "keep the door open for repeat testing.",
        dangerous_mimic_of=["viral_urti", "influenza"],
        source="BHIVA testing guidelines; BASHH",
    ),
    # ================= PAEDIATRIC =================
    ConditionProfile(
        condition_id="febrile_child_serious",
        name="Serious illness in a febrile child (overlay)",
        category="paediatric",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("drowsiness", 0.60, 0.60),
            SymptomFrequency("poor_feeding", 0.55, 0.45),
            SymptomFrequency("reduced_fluid_intake", 0.55, 0.45),
            SymptomFrequency("reduced_urine_output", 0.40, 0.45),
            SymptomFrequency("fast_breathing", 0.50, 0.50),
            SymptomFrequency("non_blanching_rash", 0.10, 0.95),
        ],
        discriminators=["NICE traffic-light system: amber/red features",
                        "age <3 months with fever >= 38 = red", "parental concern"],
        red_flags=["non-blanching rash", "drowsy/ill-looking child",
                   "grunting, chest indrawing", "under 3 months with any fever"],
        investigations=[
            InvestigationProfile("paediatric traffic-light assessment", "risk stratify",
                                 None, None, "NICE CG160 feverish child"),
        ],
        management_first_line="Any red feature (or amber if uncertain): same-day "
                              "paediatric assessment. Under 3 months with fever: "
                              "refer. Never a telephone-only diagnosis (NICE CG160).",
        referral_tier="emergency",
        safety_net="A child who is floppy, drowsy, not drinking, breathing fast or "
                   "has a rash that doesn't fade — emergency now.",
        dangerous_mimic_of=["viral_urti", "otitis_media", "chickenpox"],
        source="NICE CG160 feverish children",
    ),
    ConditionProfile(
        condition_id="bronchiolitis",
        name="Bronchiolitis",
        category="paediatric",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("breathlessness", 0.80, 0.25),
            SymptomFrequency("cough", 0.85, 0.10),
            SymptomFrequency("wheeze", 0.70, 0.30),
            SymptomFrequency("poor_feeding", 0.60, 0.45),
            SymptomFrequency("rhinorrhoea", 0.70, 0.15),
        ],
        discriminators=["infant <2 y, winter, RSV season", "fine crackles + wheeze",
                        "peaks day 3-5"],
        red_flags=["apnoea", "dehydration / <50% feeds", "RR >60, severe recession",
                   "under 3 months or premature", "oxygen <92%"],
        investigations=[],
        management_first_line="Supportive: feeding support, small frequent feeds, "
                              "saline drops; no bronchodilators/steroids/antibiotics "
                              "routinely (NICE NG9).",
        referral_tier="self_care",
        safety_net="Not feeding half normal, breathing >60/min, pauses in breathing, "
                   "or becoming blue — emergency.",
        source="NICE NG9 bronchiolitis",
    ),
    ConditionProfile(
        condition_id="croup",
        name="Croup (laryngotracheobronchitis)",
        category="paediatric",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("barking_cough", 0.95, 0.95),
            SymptomFrequency("stridor", 0.60, 0.85),
            SymptomFrequency("hoarseness", 0.60, 0.50),
            SymptomFrequency("fever", 0.40, 0.05),
        ],
        discriminators=["6 months-3 years", "worse at night", "inspiratory stridor "
                        "± intercostal recession"],
        red_flags=["stridor at rest", "cyanosis/exhaustion", "drooling + no bark "
                   "(think epiglottitis)"],
        investigations=[],
        management_first_line="Mild: single oral dexamethasone 0.15 mg/kg; moderate/"
                              "severe: nebulised budesonide, consider adrenaline, "
                              "hospital transfer (NICE CKS croup).",
        referral_tier="urgent",
        safety_net="Stridor while resting or sleepy, or struggling to breathe — 999.",
        source="NICE CKS croup; BTS paedic",
    ),
    ConditionProfile(
        condition_id="paediatric_asthma",
        name="Asthma exacerbation (child)",
        category="paediatric",
        prevalence_per_consult=0.015,
        symptoms=[
            SymptomFrequency("wheeze", 0.85, 0.65),
            SymptomFrequency("breathlessness", 0.80, 0.15),
            SymptomFrequency("cough", 0.70, 0.10),
            SymptomFrequency("poor_feeding", 0.30, 0.25),
        ],
        discriminators=["known asthma or recurrent wheeze episodes", "response to "
                        "bronchodilator", "no fever focus usually"],
        red_flags=["too breathless to speak/feed", "silent chest", "exhaustion, "
                   "blue lips", "PEF <50%"],
        investigations=[],
        management_first_line="Salbutamol via spacer (2-10 puffs per severity, repeat "
                              "15-30 min); oral prednisolone 1-2 mg/kg (max 40 mg) 3-5 "
                              "days; BTS/SIGN asthma.",
        referral_tier="urgent",
        safety_net="Cannot finish sentences or feed, lips blue, inhaler not working — "
                   "999 immediately.",
        source="BTS/SIGN asthma 2019 (paediatric)",
    ),
    ConditionProfile(
        condition_id="intussusception",
        name="Intussusception",
        category="paediatric",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("abdominal_pain_colicky", 0.90, 0.45),
            SymptomFrequency("vomiting", 0.80, 0.20),
            SymptomFrequency("redcurrant_jelly_stool", 0.30, 0.95),
            SymptomFrequency("drawing_up_legs", 0.60, 0.75),
            SymptomFrequency("pallor_episodes", 0.50, 0.65),
        ],
        discriminators=["infant 3 months-2 years", "episodic screaming drawing up legs "
                        "then quiet intervals", "sausage-shaped mass"],
        red_flags=["redcurrant jelly stool", "lethargy between episodes",
                   "signs of shock"],
        investigations=[
            InvestigationProfile("ultrasound abdomen", "target sign",
                                 0.95, 0.95, "paediatric surgical guidance"),
        ],
        management_first_line="Emergency paediatric surgical referral; nil by mouth; "
                              "air/pneumatic reduction or surgery.",
        referral_tier="emergency",
        safety_net="A baby with repeated screaming-pain episodes, drawing legs up, "
                   "vomiting or passing blood — emergency.",
        dangerous_mimic_of=["gastroenteritis", "colic_pending"],
        source="Paediatric surgery standard texts",
    ),
    ConditionProfile(
        condition_id="meningococcal_child",
        name="Meningococcal disease (child)",
        category="paediatric",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("fever", 0.95, 0.10),
            SymptomFrequency("non_blanching_rash", 0.60, 0.90),
            SymptomFrequency("drowsiness", 0.60, 0.45),
            SymptomFrequency("neck_stiffness", 0.30, 0.55),
            SymptomFrequency("cold_hands_feet", 0.35, 0.70),
            SymptomFrequency("limb_pain", 0.30, 0.60),
        ],
        discriminators=["rapid deterioration over hours", "early septic features "
                        "before rash", "petechiae first"],
        red_flags=["any non-blanching rash with fever = 999",
                   "cold peripheries with fever", "not responding normally"],
        investigations=[],
        management_first_line="Call 999; IM benzylpenicillin (unless anaphylactic) "
                              "before transfer; do not wait for a rash.",
        referral_tier="emergency",
        safety_net="Fever plus any rash that doesn't fade under a glass, or cold hands "
                   "and feet with abnormal drowsiness — 999.",
        dangerous_mimic_of=["viral_urti", "scarlet_fever"],
        source="NICE CG102; UKHSA meningococcal guidance",
    ),

    # ================= GERIATRIC / FRAILTY =================
    ConditionProfile(
        condition_id="delirium",
        name="Delirium",
        category="geriatric_frailty",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("confusion", 0.95, 0.45),
            SymptomFrequency("fluctuating_confusion", 0.70, 0.85),
            SymptomFrequency("hallucination", 0.35, 0.55),
            SymptomFrequency("reduced_mobility", 0.40, 0.20),
            SymptomFrequency("drowsiness", 0.35, 0.25),
        ],
        discriminators=["ACUTE change (hours-days) + inattention — 4AT score",
                        "often hypoactive and missed", "fluctuating through day"],
        red_flags=["delirium is itself a red flag — always seek cause: infection, "
                   "retention, hypoxia, drugs, metabolic, pain"],
        investigations=[
            InvestigationProfile("4AT", "rapid delirium screen", None, None,
                                 "4AT www.4at.org.uk; NICE CG103"),
        ],
        management_first_line="Treat the cause; reorientation, glasses/hearing aids, "
                              "hydration, avoid sedatives; never assume dementia without "
                              "excluding delirium (NICE CG103).",
        referral_tier="urgent",
        safety_net="Sudden confusion in an older person is a medical emergency until "
                   "cause found — same-day assessment.",
        dangerous_mimic_of=["dementia_pending", "urinary_tract_infection_simple"],
        source="NICE CG103 delirium; 4AT",
    ),
    ConditionProfile(
        condition_id="falls_multifactorial",
        name="Falls (multifactorial, older person)",
        category="geriatric_frailty",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("fall", 1.00, 0.55),
            SymptomFrequency("dizziness", 0.40, 0.10),
            SymptomFrequency("reduced_mobility", 0.35, 0.15),
        ],
        discriminators=["postural drop", "medication review (psychotropics, "
                        "antihypertensives)", "home hazards, vision, footwear"],
        red_flags=["loss of consciousness", "head injury on anticoagulant",
                   "injury unable to weight-bear", "recurrent falls"],
        investigations=[
            InvestigationProfile("lying/standing BP", "postural hypotension",
                                 0.60, 0.85, "NICE CG161 falls"),
        ],
        management_first_line="Multifactorial falls assessment: strength/balance "
                              "training, medication review, vision, home hazards "
                              "(NICE CG161); osteoporosis risk review after fracture.",
        referral_tier="routine",
        safety_net="Head injury while on warfarin/DOAC, or any fall with loss of "
                   "consciousness — urgent same-day.",
        source="NICE CG161 falls assessment",
    ),
    ConditionProfile(
        condition_id="frailty_decompensation",
        name="Frailty decompensation",
        category="geriatric_frailty",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("reduced_mobility", 0.85, 0.60),
            SymptomFrequency("reduced_fluid_intake", 0.60, 0.50),
            SymptomFrequency("confusion", 0.40, 0.20),
            SymptomFrequency("fatigue", 0.70, 0.10),
        ],
        discriminators=["change from baseline function over days", "often triggered "
                        "by minor insult (UTI, constipation, drug)", " frailty score"],
        red_flags=["not drinking", "off feet entirely", "new confusion"],
        investigations=[
            InvestigationProfile("baseline-function comparison", "the key geriatric "
                                 "test: what changed?", None, None,
                                 "comprehensive geriatric assessment"),
        ],
        management_first_line="Comprehensive geriatric assessment; find the trigger; "
                              "rehydration; avoid admitting unless needed — consider "
                              "CGA-led community response.",
        referral_tier="urgent",
        safety_net="An older person who has stopped walking or drinking needs same-day "
                   "review — waiting is a decision.",
        source="BGS frailty guidance; CGA standards",
    ),
    ConditionProfile(
        condition_id="polypharmacy_adverse_effect",
        name="Adverse drug effect in polypharmacy",
        category="geriatric_frailty",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("dizziness", 0.45, 0.15),
            SymptomFrequency("confusion", 0.30, 0.15),
            SymptomFrequency("fall", 0.35, 0.30),
            SymptomFrequency("nausea", 0.25, 0.05),
            SymptomFrequency("medication_change_recent", 0.60, 0.75),
        ],
        discriminators=["new symptom within weeks of new/changed drug",
                        "anticholinergic burden", "renal function decline on old doses"],
        red_flags=["bleeding on anticoagulant", "hypoglycaemia on insulin/"
                    "sulfonylurea", "falls on psychotropics"],
        investigations=[
            InvestigationProfile("medication review + renal function", "the diagnostic "
                                 "test is reading the drug chart",
                                 None, None, "NICE medicines optimisation NG5"),
        ],
        management_first_line="Structured medication review: STOPP/START criteria; "
                              "deprescribe the suspect drug; one change at a time; "
                              "check renal dosing (NICE NG5).",
        referral_tier="routine",
        safety_net="Any new symptom in someone on many drugs — think drug cause first; "
                   "review within days, not months.",
        source="NICE NG5 medicines optimisation; STOPP/START v3",
    ),
    ConditionProfile(
        condition_id="pressure_ulcer",
        name="Pressure ulcer",
        category="geriatric_frailty",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("skin_breakdown", 0.95, 0.85),
            SymptomFrequency("reduced_mobility", 0.70, 0.20),
        ],
        discriminators=["over bony prominence", "pressure/shear history",
                        "category 1-4 grading"],
        red_flags=["black eschar/necrosis (cat 3-4)", "surrounding cellulitis",
                   "bone exposed", "systemic sepsis"],
        investigations=[],
        management_first_line="Repositioning + pressure-relieving surface; wound "
                              "assessment; nutritional review; document category; "
                              "district nursing referral; safeguarding if neglect "
                              "possible (NICE CG179).",
        referral_tier="urgent",
        safety_net="Rapidly worsening skin breakdown, spreading redness or fever — "
                   "urgent review.",
        source="NICE CG179 pressure ulcers",
    ),

    # ================= MENTAL HEALTH =================
    ConditionProfile(
        condition_id="depression_moderate",
        name="Depression (moderate)",
        category="mental_health",
        prevalence_per_consult=0.04,
        symptoms=[
            SymptomFrequency("low_mood", 0.95, 0.60),
            SymptomFrequency("anhedonia", 0.85, 0.65),
            SymptomFrequency("poor_sleep", 0.70, 0.25),
            SymptomFrequency("fatigue", 0.70, 0.05),
            SymptomFrequency("poor_concentration", 0.60, 0.35),
            SymptomFrequency("suicidal_thoughts", 0.25, 0.45),
        ],
        discriminators=["PHQ-9 >= 10", "2+ weeks persistent", "functional impact"],
        red_flags=["active suicidal intent/plan", "psychotic features",
                   "not eating/drinking", "postnatal"],
        investigations=[
            InvestigationProfile("PHQ-9", "severity + monitoring",
                                 None, None, "NICE CG90 depression"),
        ],
        management_first_line="PHQ-9 severity; guided self-help/low-intensity CBT "
                              "first; SSRI if moderate-severe or preference "
                              "(NICE CG90); always ask about suicidal thoughts.",
        referral_tier="routine",
        safety_net="Thoughts of harming yourself — seek help same day; 999 if there "
                   "is a plan or intent.",
        source="NICE CG90 depression",
    ),
    ConditionProfile(
        condition_id="anxiety_generalised",
        name="Generalised anxiety disorder",
        category="mental_health",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("excessive_worry", 0.90, 0.75),
            SymptomFrequency("restlessness", 0.60, 0.40),
            SymptomFrequency("poor_sleep", 0.55, 0.20),
            SymptomFrequency("palpitations", 0.35, 0.10),
            SymptomFrequency("anxiety", 0.85, 0.35),
        ],
        discriminators=["GAD-7 >= 8", "worry across multiple domains, months",
                        "not episodic panic"],
        red_flags=["alcohol self-medication", "suicidal thoughts", "function collapse"],
        investigations=[
            InvestigationProfile("GAD-7", "severity", None, None, "NICE CG113"),
        ],
        management_first_line="Step 2: self-help/psychoeducation; high-intensity CBT "
                              "or applied relaxation; SSRI if severe (NICE CG113).",
        referral_tier="routine",
        safety_net="If anxiety comes with chest pain on exertion or fainting — "
                   "exclude physical causes too.",
        source="NICE CG113 anxiety",
    ),
    ConditionProfile(
        condition_id="psychosis_first_episode",
        name="First-episode psychosis",
        category="mental_health",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("hallucination", 0.70, 0.85),
            SymptomFrequency("delusion", 0.75, 0.90),
            SymptomFrequency("social_withdrawal", 0.55, 0.30),
            SymptomFrequency("poor_concentration", 0.40, 0.10),
            SymptomFrequency("disorganised_thinking", 0.45, 0.75),
        ],
        discriminators=["duration >= 1 week", "functional decline",
                        "exclude drug causes (stimulants, steroids, cannabis)"],
        red_flags=["risk to self or others", "not eating/drinking",
                   "organic signs — delirium mimic"],
        investigations=[
            InvestigationProfile("physical + drug screen", "exclude organic causes",
                                 0.50, 0.80, "NICE CG178 psychosis"),
        ],
        management_first_line="Urgent referral to early intervention in psychosis "
                              "team (within 2 weeks; same-day if risk); do not start "
                              "antipsychotics in primary care routinely (NICE CG178).",
        referral_tier="urgent",
        safety_net="Voices or beliefs that others don't share, getting worse — urgent "
                   "mental health assessment; 999 if there is risk to life.",
        dangerous_mimic_of=["delirium"],
        source="NICE CG178 psychosis & schizophrenia",
    ),
    ConditionProfile(
        condition_id="suicide_risk",
        name="Acute suicide risk",
        category="mental_health",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("suicidal_thoughts", 1.00, 0.85),
            SymptomFrequency("hopelessness", 0.70, 0.50),
            SymptomFrequency("low_mood", 0.70, 0.20),
            SymptomFrequency("insomnia_severe", 0.40, 0.30),
        ],
        discriminators=["plan, means, intent, timeframe", "previous attempts",
                        "isolation, drug/alcohol use, recent loss"],
        red_flags=["stated intent + plan + means = emergency",
                   "says goodbye / gives possessions", "attempt in progress"],
        investigations=[],
        management_first_line="Do not leave the person alone; remove means if safe; "
                              "same-day mental health crisis team / 999; safety plan "
                              "if lower risk; never rely on no-suicide contracts.",
        referral_tier="emergency",
        safety_net="If you feel you may act on thoughts of ending your life — call "
                   "999, or Samaritans 116 123 now.",
        source="NICE self-harm guidance; NCISH",
    ),
    ConditionProfile(
        condition_id="eating_disorder_anorexia",
        name="Anorexia nervosa",
        category="mental_health",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("weight_loss", 0.90, 0.35),
            SymptomFrequency("fear_of_weight_gain", 0.90, 0.90),
            SymptomFrequency("restricted_eating", 0.90, 0.75),
            SymptomFrequency("amenorrhoea", 0.50, 0.55),
        ],
        discriminators=["BMI <17.5 or rapid loss", "body image distortion",
                        "excessive exercise/purging"],
        red_flags=["BMI <15, potassium disturbance, ECG changes, bradycardia <40, "
                   "syncope — medical emergency", "suicidality"],
        investigations=[
            InvestigationProfile("BMI + ECG + U&E/FBC/osteoporosis screen", "physical "
                                 "risk assessment", 0.80, 0.80,
                                 "MEED guidance (RCPsych)"),
        ],
        management_first_line="Assess physical risk (MEED); refer eating-disorder "
                              "service — children/young people: immediate referral "
                              "(NICE NG69); GP monitors bones, ECG, electrolytes.",
        referral_tier="urgent",
        safety_net="Fainting, heart rate under 40, or rapid weight loss — same-day "
                   "medical assessment.",
        source="NICE NG69 eating disorders; MEED RCPsych",
    ),
    ConditionProfile(
        condition_id="alcohol_dependence",
        name="Alcohol dependence",
        category="mental_health",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("morning_shakes", 0.50, 0.75),
            SymptomFrequency("alcohol_heavy_pattern", 0.75, 0.85),
            SymptomFrequency("alcohol_craving", 0.80, 0.70),
            SymptomFrequency("poor_sleep", 0.50, 0.15),
            SymptomFrequency("anxiety", 0.40, 0.10),
        ],
        discriminators=["AUDIT-C first (score >=5 positive): how often, "
                        "how many units a typical day, how often 6+ in "
                        "one session",
                        "withdrawal on waking; tolerance + loss of control",
                        "ALWAYS the paracetamol question (PabQ): "
                        "co-ingested paracetamol on a chronic-drinking "
                        "liver is the UK's classic hepatotoxic disaster"],
        red_flags=["withdrawal seizures/delirium tremens", "jaundice/ascites",
                   "withdrawal at home unsupervised with history of fits"],
        investigations=[
            InvestigationProfile("AUDIT questionnaire", "severity",
                                 None, None, "NICE CG115 alcohol"),
            InvestigationProfile("LFTs + GGT", "physical harm marker",
                                 0.60, 0.70, "NICE CG115"),
        ],
        management_first_line="AUDIT; brief intervention or community-assisted "
                              "withdrawal with ORAL chlordiazepoxide + thiamine "
                              "(thiamine BEFORE any glucose; never an abrupt "
                              "unsupported stop); relapse prevention; involve "
                              "the local community alcohol service and the "
                              "family (NICE CG115).",
        referral_tier="routine",
        safety_net="Fits, confusion or shaking badly on stopping alcohol — emergency "
                   "(withdrawal can kill); never stop suddenly unsupervised if "
                   "heavy drinker with past fits.",
        source="NICE CG115 alcohol-use disorders",
    ),
    # ================= MUSCULOSKELETAL =================
    ConditionProfile(
        condition_id="osteoarthritis_knee",
        name="Knee osteoarthritis",
        category="musculoskeletal",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("knee_pain", 0.95, 0.70),
            SymptomFrequency("joint_stiffness", 0.60, 0.35),
            SymptomFrequency("pain_on_movement", 0.80, 0.25),
        ],
        discriminators=[">45 y, activity-related, brief morning stiffness <30 min",
                        "bony tenderness/crepitus", "no systemic features"],
        red_flags=["hot swollen joint", "sudden severe pain + giving way",
                   "night pain/weight loss"],
        investigations=[],
        management_first_line="Exercise + weight loss core; topical NSAID; paracetamol; "
                              "consider physio; arthroplasty referral if persistent "
                              "functional impact (NICE NG226 OA).",
        referral_tier="routine",
        safety_net="A single hot, swollen, painful knee — same-day review (septic "
                   "arthritis until excluded).",
        source="NICE NG226 osteoarthritis",
    ),
    ConditionProfile(
        condition_id="ra_early",
        name="Rheumatoid arthritis (early)",
        category="musculoskeletal",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("symmetrical_joint_pain", 0.80, 0.75),
            SymptomFrequency("small_joint_swelling", 0.70, 0.75),
            SymptomFrequency("morning_stiffness_prolonged", 0.75, 0.75),
            SymptomFrequency("fatigue", 0.50, 0.05),
        ],
        discriminators=[">30 min morning stiffness", "MCP/PIP swelling, spares DIP",
                        "symptoms >6 weeks"],
        red_flags=["the window for DMARDs is early — never watch-and-wait beyond "
                   "3 months", "hot single joint = septic until excluded"],
        investigations=[
            InvestigationProfile("RF + anti-CCP + CRP/ESR", "support early referral",
                                 0.70, 0.85, "NICE NG100 RA"),
        ],
        management_first_line="Urgent (2ww-equivalent) referral to rheumatology with "
                              "bloods; do NOT wait for positive serology — send with "
                              "negative tests if clinical suspicion (NICE NG100).",
        referral_tier="urgent",
        safety_net="Persistent joint swelling over 6 weeks needs a rheumatology "
                   "referral, not more ibuprofen.",
        source="NICE NG100 rheumatoid arthritis",
    ),
    ConditionProfile(
        condition_id="gout_acute",
        name="Acute gout",
        category="musculoskeletal",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("big_toe_pain", 0.60, 0.85),
            SymptomFrequency("hot_swollen_joint", 0.80, 0.50),
            SymptomFrequency("unable_weight_bear", 0.50, 0.40),
            SymptomFrequency("fever", 0.15, 0.05),
        ],
        discriminators=["rapid onset overnight", "first MTP joint", "previous episodes",
                        "diuretics/alcohol/CKD"],
        red_flags=["fever with a hot joint — consider septic arthritis: aspirate "
                   "before treating as gout if any doubt"],
        investigations=[],
        management_first_line="NSAID or colchicine within 24 h (or steroid if "
                              "contraindicated); rest, ice; check urate after 4-6 "
                              "weeks, not during attack (NICE NG219 gout).",
        referral_tier="routine",
        safety_net="Hot joint WITH fever, or you feel very unwell — same-day: septic "
                   "arthritis must be excluded.",
        dangerous_mimic_of=[],
        source="NICE NG219 gout",
    ),
    ConditionProfile(
        condition_id="polymyalgia_rheumatica",
        name="Polymyalgia rheumatica",
        category="musculoskeletal",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("girdle_pain_stiffness", 0.95, 0.85),
            SymptomFrequency("morning_stiffness_prolonged", 0.85, 0.60),
            SymptomFrequency("fatigue", 0.50, 0.05),
        ],
        discriminators=["age > 50", "shoulder/hip girdle both sides >45 min stiffness",
                        "rapid response to low-dose steroid (diagnostic clue)",
                        "raise GCA question at every review"],
        red_flags=["headache, jaw pain, visual change = giant cell arteritis "
                   "— emergency, sight-threatening"],
        investigations=[
            InvestigationProfile("ESR/CRP", "usually raised",
                                 0.80, 0.70, "NICE NG100/B SR RA related"),
        ],
        management_first_line="Prednisolone 15 mg (never >30 unless GCA suspected); "
                              "assess GCA symptoms at every review; rheumatology "
                              "referral if atypical; bone protection.",
        referral_tier="routine",
        safety_net="Any new headache, scalp tenderness, jaw chewing pain or visual "
                   "change — emergency same-day (GCA).",
        source="NICE PMR guidance; BSR PMR guideline 2010",
    ),
    ConditionProfile(
        condition_id="giant_cell_arteritis",
        name="Giant cell arteritis",
        category="musculoskeletal",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("headache", 0.80, 0.25),
            SymptomFrequency("scalp_tenderness", 0.50, 0.80),
            SymptomFrequency("jaw_claudication", 0.45, 0.90),
            SymptomFrequency("visual_disturbance", 0.30, 0.60),
            SymptomFrequency("girdle_pain_stiffness", 0.40, 0.30),
            SymptomFrequency("fever", 0.20, 0.10),
        ],
        discriminators=["age > 50, new headache", "jaw ache on chewing",
                        "raised ESR/CRP", "temporal artery tenderness"],
        red_flags=["ANY visual symptom = threatened sight loss: high-dose steroid "
                   "immediately, before investigations", "twice-daily dosing if "
                   "visual symptoms"],
        investigations=[
            InvestigationProfile("ESR/CRP", "supportive (can be normal)",
                                 0.80, 0.70, "NICE/B SR GCA guidance"),
            InvestigationProfile("temporal artery ultrasound/biopsy", "confirm "
                                 "(after steroids started)", 0.70, 0.90,
                                 "BSR GCA guideline"),
        ],
        management_first_line="Suspected GCA: start prednisolone 40-60 mg (or IV "
                              "methylprednisolone if visual symptoms) SAME DAY and "
                              "refer urgently; do not delay steroids for biopsy.",
        referral_tier="emergency",
        safety_net="A new headache over age 50 with jaw ache, tender scalp or any "
                   "change in vision — emergency: sight is at risk.",
        dangerous_mimic_of=["tension_headache", "migraine"],
        source="BSR GCA guideline; NICE CKS",
    ),
    ConditionProfile(
        condition_id="septic_arthritis",
        name="Septic arthritis",
        category="musculoskeletal",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("hot_swollen_joint", 0.95, 0.60),
            SymptomFrequency("unable_weight_bear", 0.70, 0.45),
            SymptomFrequency("fever", 0.50, 0.10),
            SymptomFrequency("joint_pain_severe", 0.95, 0.40),
        ],
        discriminators=["single joint, severe pain, any movement agony",
                        "IVDU, immunosuppression, prosthetic joint, skin breach"],
        red_flags=["prosthetic joint", "systemic sepsis", "never start antibiotics "
                   "before aspiration unless septic"],
        investigations=[
            InvestigationProfile("joint aspiration before antibiotics", "diagnostic",
                                 0.80, 0.95, "standard orthopaedic practice"),
        ],
        management_first_line="Same-day orthopaedic referral for aspiration/washout; "
                              "analgesia; antibiotics per culture after aspiration.",
        referral_tier="emergency",
        safety_net="A single hot, swollen, exquisitely painful joint — emergency "
                   "same-day; delay destroys the joint.",
        dangerous_mimic_of=["gout_acute"],
        source="Orthopaedic/septic arthritis standards",
    ),
    ConditionProfile(
        condition_id="sciatica_prolapse",
        name="Sciatica (disc prolapse)",
        category="musculoskeletal",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("sciatica_leg_pain", 0.95, 0.80),
            SymptomFrequency("back_pain", 0.70, 0.10),
            SymptomFrequency("pins_needles_leg", 0.45, 0.55),
        ],
        discriminators=["pain below knee, dermatomal", "worse sitting/sneezing",
                        "straight-leg reproduce"],
        red_flags=["bilateral or progressive neurology", "saddle numbness",
                   "bladder dysfunction — cauda equina: emergency"],
        investigations=[],
        management_first_line="Stay active + analgesia; most resolve 4-6 weeks; "
                              "no routine imaging; refer if >6 weeks disabling or "
                              "progressive neurology (NICE NG59).",
        referral_tier="self_care",
        safety_net="Numbness between the legs, trouble passing urine, or weakness in "
                   "both legs — emergency (cauda equina).",
        source="NICE NG59 low back pain",
    ),
    ConditionProfile(
        condition_id="osteoporotic_fragility_fracture",
        name="Osteoporotic fragility fracture (vertebral)",
        category="musculoskeletal",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("back_pain", 0.95, 0.20),
            SymptomFrequency("pain_after_minimal_trauma", 0.80, 0.80),
            SymptomFrequency("reduced_mobility", 0.40, 0.20),
        ],
        discriminators=["age >50, low-impact", "sudden well-localised mid/low thoracic",
                        "height loss/knows to use FRAX"],
        red_flags=["neurological deficit", "cancer history (pathological fracture)"],
        investigations=[
            InvestigationProfile("spinal X-ray", "confirm fracture",
                                 0.80, 0.90, "NICE TA/CKS osteoporosis"),
            InvestigationProfile("DXA", "bone density (after event)",
                                 0.90, 0.90, "NICE CG146 osteoporosis"),
        ],
        management_first_line="Analgesia, stay mobile; DXA + FRAX/QFracture; bone "
                              "protection treatment if eligible; falls review "
                              "(NICE CG146).",
        referral_tier="routine",
        safety_net="New back pain after age 50 with only minor injury — needs "
                   "assessment, not just painkillers.",
        source="NICE CG146 osteoporosis",
    ),

    # ================= DERMATOLOGY =================
    ConditionProfile(
        condition_id="eczema_atopic",
        name="Atopic eczema",
        category="dermatology",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("itchy_skin", 0.95, 0.50),
            SymptomFrequency("dry_skin", 0.80, 0.35),
            SymptomFrequency("flexural_rash", 0.60, 0.65),
        ],
        discriminators=["flexural distribution in child", "personal/family atopy",
                        "chronic relapsing"],
        red_flags=["weeping, crusted, painful, sudden worsening — eczema herpeticum: "
                   "emergency", "widespread erythroderma"],
        investigations=[],
        management_first_line="Emollients generously + topical steroid potency matched "
                              "to site/age; trigger avoidance; bleach baths for "
                              "recurrent infection; step-up plan (NICE CG57).",
        referral_tier="self_care",
        safety_net="Clusters of small punched-out lesions, fever, or eczema suddenly "
                   "worsening and painful — same-day (eczema herpeticum).",
        source="NICE CG57 atopic eczema",
    ),
    ConditionProfile(
        condition_id="psoriasis_plaque",
        name="Plaque psoriasis",
        category="dermatology",
        prevalence_per_consult=0.015,
        symptoms=[
            SymptomFrequency("scaly_plaques", 0.95, 0.85),
            SymptomFrequency("nail_pitting", 0.35, 0.70),
            SymptomFrequency("itchy_skin", 0.40, 0.10),
        ],
        discriminators=["extensor surfaces, scalp, natal cleft", "Auspitz sign, "
                        "Koebner phenomenon", "family history"],
        red_flags=["widespread redness + scaling + systemic unwell — erythrodermic/"
                   "pustular psoriasis: urgent", "new psoriasis + joint pain — "
                   "psoriatic arthritis, rheumatology"],
        investigations=[],
        management_first_line="Potent topical steroid + vitamin D analogue short "
                              "contact; emollients; phototherapy/ systemic pathway if "
                              "severe (NICE CG153).",
        referral_tier="routine",
        safety_net="Skin becoming universally red with fever or feeling unwell — "
                   "urgent review.",
        source="NICE CG153 psoriasis",
    ),
    ConditionProfile(
        condition_id="melanoma_suspect",
        name="Suspected melanoma",
        category="dermatology",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("changing_mole", 0.85, 0.85),
            SymptomFrequency("bleeding_mole", 0.30, 0.75),
            SymptomFrequency("itchy_skin", 0.20, 0.05),
        ],
        discriminators=["ABCDEF: asymmetry, border, colour variation, diameter >6 mm, "
                        "evolution, funny-looking vs neighbours"],
        red_flags=["any mole meeting 7-point checklist or ugly-duckling — 2ww",
                   "new pigmented lesion over 40"],
        investigations=[],
        management_first_line="Do NOT biopsy in primary care; photograph, measure, "
                              "2ww dermatology referral (NICE NG12).",
        referral_tier="two_week_wait",
        safety_net="Any mole changing shape, colour, size, bleeding or itching — "
                   "urgent GP review for 2ww assessment.",
        source="NICE NG12 suspected cancer",
    ),
    ConditionProfile(
        condition_id="shingles",
        name="Herpes zoster (shingles)",
        category="dermatology",
        prevalence_per_consult=0.006,
        symptoms=[
            SymptomFrequency("burning_skin_pain", 0.80, 0.80),
            SymptomFrequency("vesicular_rash", 0.90, 0.55),
            SymptomFrequency("one_sided_rash", 0.95, 0.85),
        ],
        discriminators=["dermatomal, does not cross midline", "pain precedes rash "
                        "1-5 days", "older/immunosuppressed"],
        red_flags=["zoster of eye/ophthalmic branch — urgent ophthalmology",
                   "immunosuppressed patient", "motor involvement or bladder "
                   "dysfunction"],
        investigations=[],
        management_first_line="Aciclovir 800 mg 5x daily 7 days if within 72 h of "
                              "rash (or active eye/immunosuppressed any time); "
                              "analgesia for neuropathic pain; 48 h only for "
                              "immunocompetent (NICE CKS).",
        referral_tier="routine",
        safety_net="Rash touching the eye or tip of nose — same-day eye assessment; "
                   "confusion or rash becoming widespread — urgent.",
        source="NICE CKS shingles",
    ),

    # ================= ENT / EYE =================
    ConditionProfile(
        condition_id="red_eye_acute_glaucoma",
        name="Acute angle-closure glaucoma",
        category="ent_eye",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("eye_pain_severe", 0.95, 0.85),
            SymptomFrequency("red_eye", 0.90, 0.20),
            SymptomFrequency("vision_reduced", 0.70, 0.40),
            SymptomFrequency("halos_around_lights", 0.50, 0.85),
            SymptomFrequency("vomiting", 0.40, 0.15),
            SymptomFrequency("headache", 0.50, 0.05),
        ],
        discriminators=["mid-dilated fixed pupil", "hazy cornea", "halos around lights",
                        "usually long-sighted older patient"],
        red_flags=["eye pain + reduced vision + vomiting = emergency; vision "
                   "permanently at risk"],
        investigations=[],
        management_first_line="Same-day emergency ophthalmology; do not give "
                              "tropicamide; analgesia/antiemetic; urgent acetazolamide "
                              "per ophthalmology.",
        referral_tier="emergency",
        safety_net="A painful red eye with blurred vision, halos or vomiting — "
                   "emergency same hour.",
        dangerous_mimic_of=["migraine", "red_eye_conjunctivitis"],
        source="RCOphth emergency eye care",
    ),
    ConditionProfile(
        condition_id="red_eye_conjunctivitis",
        name="Infective conjunctivitis",
        category="ent_eye",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("red_eye", 0.95, 0.30),
            SymptomFrequency("gritty_eye", 0.70, 0.55),
            SymptomFrequency("eye_discharge", 0.80, 0.60),
        ],
        discriminators=["both eyes often", "discharge, lids stuck in morning",
                        "vision normal, pupil normal, no pain"],
        red_flags=["true pain, photophobia, reduced vision — NOT conjunctivitis: "
                   "urgent eye assessment", "contact lens wearer with red eye "
                   "(keratitis risk)", "newborn"],
        investigations=[],
        management_first_line="Usually self-limiting 5-7 days; lid hygiene; delayed "
                              "antibiotic drops if severe/prolonged; exclude red-flag "
                              "features first (NICE CKS).",
        referral_tier="self_care",
        safety_net="Red eye with pain, light sensitivity or blurred sight — same-day "
                   "eye assessment; conjunctivitis never impairs vision.",
        source="NICE CKS conjunctivitis",
    ),
    ConditionProfile(
        condition_id="uveitis_anterior",
        name="Acute anterior uveitis (iritis)",
        category="ent_eye",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("eye_pain_severe", 0.70, 0.50),
            SymptomFrequency("photophobia", 0.80, 0.40),
            SymptomFrequency("red_eye", 0.85, 0.15),
            SymptomFrequency("vision_reduced", 0.40, 0.25),
        ],
        discriminators=["ciliary flush pattern", "small pupil", "associated HLA-B27/"
                        "ankylosing spondylitis/IBD"],
        red_flags=["photophobia + pain — urgent same-day ophthalmology"],
        investigations=[],
        management_first_line="Urgent same-day ophthalmology for slit-lamp "
                              "assessment and steroid drops; screen for associated "
                              "systemic disease.",
        referral_tier="urgent",
        safety_net="Painful red eye with light sensitivity — same-day eye unit.",
        dangerous_mimic_of=["red_eye_conjunctivitis"],
        source="RCOphth; standard ophthalmology",
    ),
    ConditionProfile(
        condition_id="retinal_detachment",
        name="Retinal detachment / tear",
        category="ent_eye",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("flashes_lights", 0.60, 0.75),
            SymptomFrequency("floaters_sudden", 0.80, 0.70),
            SymptomFrequency("visual_curtain", 0.40, 0.90),
            SymptomFrequency("vision_reduced", 0.50, 0.20),
        ],
        discriminators=["sudden shower of floaters/flash", "shadow like curtain",
                        "myopia/trauma/cataract surgery history"],
        red_flags=["any curtain or sudden floaters+flashes = same-day emergency eye",
                   "vision loss expanding"],
        investigations=[],
        management_first_line="Same-day emergency ophthalmology referral; no "
                              "examination delay; rest advice per unit.",
        referral_tier="emergency",
        safety_net="Sudden flashes, a shower of floaters, or a shadow/curtain across "
                   "vision — emergency same-day.",
        source="RCOphth retinal detachment pathways",
    ),
    ConditionProfile(
        condition_id="sinusitis",
        name="Acute sinusitis",
        category="ent_eye",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("facial_pressure_pain", 0.85, 0.70),
            SymptomFrequency("purulent_nasal_discharge", 0.70, 0.55),
            SymptomFrequency("rhinorrhoea", 0.50, 0.10),
            SymptomFrequency("headache", 0.50, 0.05),
        ],
        discriminators=["worse bending forward", "maxillary tenderness",
                        "symptoms >10 days or double-sickening"],
        red_flags=["periorbital swelling/eye movement limitation — orbital "
                   "cellulitis: emergency", "frontal swelling (Pott puffy)",
                   "confusion/severe headache"],
        investigations=[],
        management_first_line="Most viral: analgesia + saline irrigation; consider "
                              "delayed antibiotic if >10 days and no improvement "
                              "(NICE NG79 sinusitis).",
        referral_tier="self_care",
        safety_net="Swelling around the eye, double vision, or severe one-sided "
                   "forehead pain with swelling — emergency.",
        source="NICE NG79 sinusitis",
    ),
    ConditionProfile(
        condition_id="epistaxis",
        name="Epistaxis (nosebleed)",
        category="ent_eye",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("nose_bleed", 1.00, 0.95),
        ],
        discriminators=["Little's area (anterior) most common", "dry air/trauma/picking",
                        "anticoagulant use"],
        red_flags=["bleeding >20-30 min despite pressure", "posterior bleed (both "
                   "sides, swallowing blood)", "anticoagulated + unable to control",
                   "recurrent unilateral — consider tumour"],
        investigations=[],
        management_first_line="Sit forward, pinch soft cartilage 10-15 min without "
                              "release; ice; consider tranexamic cream; if ongoing — "
                              "ED for cautery/packing; review anticoagulants "
                              "(never stop blindly — discuss).",
        referral_tier="urgent",
        safety_net="Bleeding not stopping after 20-30 minutes of continuous "
                   "pressure, or swallowing large amounts of blood — ED now.",
        source="NICE CKS epistaxis",
    ),
    ConditionProfile(
        condition_id="vertigo_bppv",
        name="Benign paroxysmal positional vertigo (BPPV)",
        category="ent_eye",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("positional_vertigo", 0.95, 0.85),
            SymptomFrequency("rotational_dizziness", 0.80, 0.45),
            SymptomFrequency("nausea", 0.50, 0.05),
        ],
        discriminators=["seconds only (<1 min)", "rolling over in bed / looking up",
                        "no hearing loss, no neurology", "positive Dix-Hallpike"],
        red_flags=["new headache/neck pain with vertigo", "any neurological sign",
                   "sudden onset with clumsiness — consider stroke"],
        investigations=[],
        management_first_line="Diagnose with Dix-Hallpike; Epley manoeuvre cures "
                              "most; vestibular rehabilitation if recurrent "
                              "(NICE CKS vertigo).",
        referral_tier="self_care",
        safety_net="Dizziness with new deafness, double vision, slurred speech, "
                   "weakness or worst-ever headache — emergency (stroke).",
        dangerous_mimic_of=["stroke_tia"],
        source="NICE CKS vertigo",
    ),
    ConditionProfile(
        condition_id="labyrinthitis",
        name="Acute labyrinthitis / vestibular neuritis",
        category="ent_eye",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("rotational_dizziness", 0.95, 0.55),
            SymptomFrequency("nausea", 0.80, 0.10),
            SymptomFrequency("vomiting", 0.60, 0.10),
            SymptomFrequency("reduced_hearing", 0.30, 0.40),
        ],
        discriminators=["continuous hours-days, then improves", "recent viral illness",
                        "unsteadiness without neurology"],
        red_flags=["sudden deafness with dizziness — urgent audiovestibular "
                   "(SSNHL window)", "new neurology — stroke"],
        investigations=[],
        management_first_line="Short course prochlorperazine (max 3 days — delays "
                              "compensation); vestibular rehabilitation if persists "
                              ">2 weeks; safety-net neurological red flags.",
        referral_tier="routine",
        safety_net="Cannot walk, double vision, slurred speech, weak side, or sudden "
                   "deafness — emergency.",
        dangerous_mimic_of=["stroke_tia"],
        source="NICE CKS; audiovestibular medicine",
    ),
    # ================= WOMEN'S HEALTH =================
    ConditionProfile(
        condition_id="ectopic_pregnancy",
        name="Ectopic pregnancy",
        category="womens_health",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("lower_abdominal_pain", 0.90, 0.40),
            SymptomFrequency("vaginal_bleeding", 0.60, 0.45),
            SymptomFrequency("shoulder_tip_pain", 0.20, 0.90),
            SymptomFrequency("syncope", 0.20, 0.40),
            SymptomFrequency("missed_period", 0.70, 0.40),
        ],
        discriminators=["positive pregnancy test + pain", "shoulder tip referred pain",
                        "risk: previous ectopic, IUD, PID, IVF"],
        red_flags=["any woman of reproductive age with abdominal pain needs a "
                   "pregnancy test — before any other reasoning"],
        investigations=[
            InvestigationProfile("urine b-hCG", "gate every pelvic pain case",
                                 0.98, 0.98, "NICE CG154 ectopic"),
        ],
        management_first_line="Positive test + pain/bleeding: same-day early pregnancy "
                              "unit; 999 if collapsed or shoulder tip pain (rupture).",
        referral_tier="emergency",
        safety_net="Positive or possibly pregnant with one-sided pain, dizziness or "
                   "shoulder-tip pain — emergency same-hour.",
        dangerous_mimic_of=["pid_pelvic_inflammatory", "appendicitis"],
        source="NICE CG154 ectopic pregnancy & miscarriage",
    ),
    ConditionProfile(
        condition_id="pregnancy_bleeding",
        name="Bleeding in early pregnancy (threatened miscarriage)",
        category="womens_health",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("vaginal_bleeding", 1.00, 0.60),
            SymptomFrequency("lower_abdominal_pain", 0.50, 0.15),
        ],
        discriminators=["pregnancy < 12 weeks most common", "spotting vs heavy "
                        "with clots", "cervical os closed"],
        red_flags=["heavy bleeding with clots/dizziness", "shoulder tip pain "
                   "(ectopic)", "pain + bleeding always needs scan"],
        investigations=[
            InvestigationProfile("urine b-hCG", "confirm pregnancy",
                                 0.98, 0.98, "NICE CG154"),
        ],
        management_first_line="Refer to early pregnancy assessment unit for scan; "
                              "rhesus anti-D if rhesus-negative; no sex/tampons until "
                              "reviewed (NICE CG154).",
        referral_tier="urgent",
        safety_net="Soaking a pad an hour, feeling faint, or shoulder-tip pain — "
                   "emergency.",
        source="NICE CG154",
    ),
    ConditionProfile(
        condition_id="preeclampsia",
        name="Pre-eclampsia",
        category="womens_health",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("headache", 0.40, 0.05),
            SymptomFrequency("visual_disturbance", 0.25, 0.35),
            SymptomFrequency("swelling_hands_face", 0.40, 0.55),
            SymptomFrequency("epigastric_pain", 0.20, 0.60),
            SymptomFrequency("vomiting", 0.20, 0.05),
        ],
        discriminators=[">= 20 weeks pregnant", "new hypertension + proteinuria",
                        "epigastric/right upper quadrant pain"],
        red_flags=["severe headache + visual change + epigastric pain in pregnancy "
                   "= emergency (eclampsia/imminent)"],
        investigations=[
            InvestigationProfile("BP + urine protein", "diagnostic pair",
                                 0.85, 0.85, "NICE NG107 hypertension pregnancy"),
        ],
        management_first_line="Measure BP and urine; any suspicion — same-day "
                              "maternity assessment; never manage new hypertension "
                              "in pregnancy in the community (NICE NG107).",
        referral_tier="emergency",
        safety_net="After 20 weeks of pregnancy: bad headache, flashing/visual "
                   "change, pain under ribs right side, or sudden swelling of face/"
                   "hands — call maternity immediately.",
        source="NICE NG107 hypertension in pregnancy",
    ),
    ConditionProfile(
        condition_id="pid_pelvic_inflammatory",
        name="Pelvic inflammatory disease",
        category="womens_health",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("lower_abdominal_pain", 0.90, 0.35),
            SymptomFrequency("vaginal_discharge", 0.55, 0.45),
            SymptomFrequency("deep_dyspareunia", 0.35, 0.55),
            SymptomFrequency("fever", 0.20, 0.05),
            SymptomFrequency("intermenstrual_bleeding", 0.25, 0.40),
        ],
        discriminators=["cervical motion tenderness", "recent IUD insertion or new "
                        "partner", "STI screen positive"],
        red_flags=["severe pain + fever + vomiting — admit IV antibiotics",
                   "pregnancy test before treating", "ruptured ectopic mimic"],
        investigations=[
            InvestigationProfile("STI screen (chlamydia/gonorrhoea)", "supportive "
                                 "(can be negative)", 0.60, 0.95,
                                 "BASHH PID 2018; NICE CKS"),
        ],
        management_first_line="Empirical antibiotics per BASHH: ceftriaxone IM + "
                              "doxycycline + metronidazole 14 days; analgesia; "
                              "partner notification; exclude pregnancy first (BASHH/NICE).",
        referral_tier="urgent",
        safety_net="Pain becoming severe, fever, vomiting, or faintness — same-day "
                   "review; always treat partners.",
        source="BASHH PID guideline; NICE",
    ),
    ConditionProfile(
        condition_id="menorrhagia",
        name="Heavy menstrual bleeding",
        category="womens_health",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("heavy_menstrual_bleeding", 1.00, 0.85),
            SymptomFrequency("fatigue", 0.30, 0.05),
            SymptomFrequency("clots_flooding", 0.50, 0.60),
        ],
        discriminators=["flooding, clots >2.5 cm, doubling protection", "impact on "
                        "life", "check ferritin not just Hb"],
        red_flags=["bleeding between periods / after sex (cancer pathway)",
                   "postmenopausal bleeding — 2ww endometrial", "symptoms of shock"],
        investigations=[
            InvestigationProfile("FBC + ferritin", "anaemia assessment",
                                 0.70, 0.90, "NICE NG88 heavy menstrual bleeding"),
        ],
        management_first_line="Test FBC; treat anaemia; levonorgestrel IUS first-line "
                              "pharmacotherapy; non-hormonal: tranexamic acid "
                              "(NICE NG88).",
        referral_tier="routine",
        safety_net="Bleeding after the menopause, between periods, or after sex "
                   "needs urgent review — never 'just a heavy period' by default.",
        source="NICE NG88 heavy menstrual bleeding",
    ),
    ConditionProfile(
        condition_id="breast_lump_2ww",
        name="Breast lump (suspected cancer)",
        category="womens_health",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("breast_lump", 0.95, 0.85),
            SymptomFrequency("nipple_change", 0.25, 0.75),
            SymptomFrequency("skin_change_breast", 0.15, 0.80),
        ],
        discriminators=["age > 50", "fixed, irregular", "nipple retraction/discharge "
                        "bloodstained", "skin dimpling/peau d'orange"],
        red_flags=["any discrete lump 30+ = 2ww", "nipple eczema change "
                   "(Paget disease)", "one-sided duct discharge blood"],
        investigations=[],
        management_first_line="Urgent 2ww breast clinic referral; do not aspirate or "
                              "observe lumps in primary care (NICE NG12/CG80).",
        referral_tier="two_week_wait",
        safety_net="Any new breast lump, dimpling, or nipple change — urgent "
                   "assessment even in younger women.",
        source="NICE NG12 suspected cancer; CG80",
    ),

    # ================= UROLOGY / KIDNEY =================
    ConditionProfile(
        condition_id="renal_colic",
        name="Renal colic (ureteric stone)",
        category="urology_kidney",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("flank_pain", 0.95, 0.70),
            SymptomFrequency("groin_pain", 0.60, 0.70),
            SymptomFrequency("vomiting", 0.50, 0.15),
            SymptomFrequency("haematuria_visible", 0.30, 0.55),
        ],
        discriminators=["writhing, cannot lie still", "wave-like loin-to-groin",
                        "previous stones"],
        red_flags=["fever with obstructed kidney = infected obstructed system: "
                   "emergency", "anuria/solitary kidney", "uncontrolled pain/vomiting"],
        investigations=[
            InvestigationProfile("urine dipstick (blood)", "supports (95% dipstick "
                                 "positive)", 0.95, 0.60, "BAUS/EAU stones"),
            InvestigationProfile("CT KUB (low-dose)", "definitive",
                                 0.97, 0.97, "EAU/BAUS"),
        ],
        management_first_line="Diclofenac IM/PR first-line (if no contraindication) + "
                              "antiemetic; medical expulsion therapy if distal stone; "
                              "fever + obstruction = emergency decompression.",
        referral_tier="urgent",
        safety_net="Fever or rigors with kidney pain — emergency (infected "
                   "obstruction); pain not controlled — same-day assessment.",
        dangerous_mimic_of=["aaa_leak"],
        source="EAU/BAU stone guidelines",
    ),
    ConditionProfile(
        condition_id="aki_dehydration",
        name="Acute kidney injury (pre-renal/dehydration)",
        category="urology_kidney",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("reduced_urine_output", 0.60, 0.55),
            SymptomFrequency("drowsiness", 0.30, 0.20),
            SymptomFrequency("nausea", 0.40, 0.05),
            SymptomFrequency("vomiting", 0.30, 0.05),
            SymptomFrequency("confusion", 0.25, 0.15),
        ],
        discriminators=["AKI stages 1-3 by creatinine rise", "trigger: sepsis, "
                        "dehydration, NSAID/ACE-I + diarrhoea", "older/frail typical"],
        red_flags=["potassium >= 6", "pulmonary oedema", "uraemia (drowsiness, "
                   "pericarditis)", "no urine 12 h"],
        investigations=[
            InvestigationProfile("U&E + creatinine (compare baseline)", "diagnostic",
                                 0.95, 0.90, "Think Kidneys/NICE AKI"),
        ],
        management_first_line="Stop nephrotoxins (NSAIDs, ACE-I, metformin, "
                              "diuretics per status); treat trigger; fluid resuscitate "
                              "carefully; admit if stage 2+ or red flags (NICE NG148 AKI).",
        referral_tier="urgent",
        safety_net="Not passing urine, drowsy or breathless with vomiting/diarrhoea — "
                   "urgent same-day bloods and review.",
        source="NICE NG148 acute kidney injury",
    ),
    ConditionProfile(
        condition_id="urinary_retention",
        name="Acute urinary retention",
        category="urology_kidney",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("bladder_dysfunction", 0.90, 0.60),
            SymptomFrequency("suprapubic_pain", 0.80, 0.60),
        ],
        discriminators=["palpable bladder", "older man with prostate symptoms",
                        "precipitant: anticholinergics, constipation, infection"],
        red_flags=["with fever (retention + prostatitis)", "painless retention "
                   "with neurological signs (cord compression)"],
        investigations=[],
        management_first_line="Urgent catheterisation; check U&E; for men: consider "
                              "TURP pathway; avoid treating constipation with "
                              "anticholinergics; chronic retention painless + "
                              "overflow needs urology.",
        referral_tier="emergency",
        safety_net="Unable to pass urine with a painful full bladder — same-day "
                   "emergency catheterisation.",
        source="NICE CKS retention; BAUS",
    ),
    ConditionProfile(
        condition_id="prostate_cancer_suspect",
        name="Prostate cancer (suspected)",
        category="urology_kidney",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("nocturia", 0.50, 0.20),
            SymptomFrequency("weak_urine_stream", 0.50, 0.30),
            SymptomFrequency("weight_loss", 0.15, 0.40),
            SymptomFrequency("bone_pain", 0.15, 0.55),
        ],
        discriminators=["age >= 50 (>= 45 if Black or family history)",
                        "lower urinary symptoms + PSA", "examine prostate"],
        red_flags=["age >= 50 with LUTS — offer DRE + PSA", "bone pain + weight loss "
                   "in older man"],
        investigations=[
            InvestigationProfile("PSA (+ DRE)", "case-finding; counsel about "
                                 "uncertainty first", 0.80, 0.70, "NICE NG12"),
        ],
        management_first_line="DRE + PSA with counselling; 2ww urology if DRE "
                              "suspicious, PSA age-specific raised, or metastatic "
                              "features (NICE NG12).",
        referral_tier="two_week_wait",
        safety_net="Progressive difficulty passing urine, or new bone pain with "
                   "weight loss in an older man — urgent review.",
        source="NICE NG12 suspected cancer",
    ),
    ConditionProfile(
        condition_id="haematuria_2ww",
        name="Visible haematuria (suspected urological cancer)",
        category="urology_kidney",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("haematuria_visible", 1.00, 0.85),
        ],
        discriminators=["age >= 45 visible haematuria", "painless", "clots",
                        "smoker/aniline dye exposure"],
        red_flags=["painless visible blood ANY age needs urgent workup; >= 45 = 2ww "
                   "if unexplained or persistent"],
        investigations=[
            InvestigationProfile("urine dipstick + FBC/U&E", "first steps",
                                 0.90, 0.85, "NICE NG12"),
        ],
        management_first_line="Exclude infection first (treat, recheck); if persistent "
                              "or unexplained visible haematuria >= 45 — 2ww urology "
                              "(CT urogram/cystoscopy pathway) (NICE NG12).",
        referral_tier="two_week_wait",
        safety_net="Blood in the urine always needs review — even if it settles "
                   "spontaneously.",
        source="NICE NG12 suspected cancer",
    ),
    ConditionProfile(
        condition_id="testicular_torsion",
        name="Testicular torsion",
        category="urology_kidney",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("testicular_pain", 0.95, 0.85),
            SymptomFrequency("vomiting", 0.50, 0.15),
            SymptomFrequency("testicular_swelling", 0.40, 0.55),
            SymptomFrequency("lower_abdominal_pain", 0.40, 0.15),
        ],
        discriminators=["sudden severe pain, hours old", "age 12-18 typical",
                        "high-riding testis, absent cremasteric"],
        red_flags=["time-critical: 6-hour window for salvage — never delay for "
                   "imaging", " torsion is a clinical diagnosis"],
        investigations=[],
        management_first_line="Immediate surgical referral/999 — do not arrange "
                              "ultrasound; scrotal exploration if any doubt.",
        referral_tier="emergency",
        safety_net="Sudden severe testicular pain with vomiting — emergency now; "
                   "minutes decide whether the testicle survives.",
        dangerous_mimic_of=["epididymitis_pending"],
        source="BAUS torsion guidance",
    ),

    # ================= HAEMATOLOGY =================
    ConditionProfile(
        condition_id="ida_iron_deficiency",
        name="Iron-deficiency anaemia",
        category="haematology",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("fatigue", 0.80, 0.05),
            SymptomFrequency("breathlessness", 0.50, 0.10),
            SymptomFrequency("pallor", 0.40, 0.35),
            SymptomFrequency("hair_thinning", 0.15, 0.30),
        ],
        discriminators=["low Hb + low MCV + low ferritin", "menstrual or dietary "
                        "cause in young women", "coeliac screen"],
        red_flags=["iron deficiency in a man or postmenopausal woman — investigate "
                   "GI malignancy (2ww criteria apply)", "weight loss"],
        investigations=[
            InvestigationProfile("FBC + ferritin", "diagnostic",
                                 0.90, 0.90, "NICE NG12/CKS anaemia"),
        ],
        management_first_line="Ferrous sulfate 200 mg alternate days (better "
                              "absorption/tolerability); recheck Hb at 4 weeks; "
                              "find the cause — never just replace iron in older "
                              "patients (NICE/ BSG).",
        referral_tier="routine",
        safety_net="Tiredness with breathlessness needs a blood test; unexplained "
                   "iron deficiency in men/postmenopausal women always needs gut "
                   "investigation.",
        source="NICE NG12; BSG iron deficiency anaemia",
    ),
    ConditionProfile(
        condition_id="b12_deficiency",
        name="Vitamin B12 deficiency",
        category="haematology",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("fatigue", 0.80, 0.05),
            SymptomFrequency("paraesthesia_feet", 0.45, 0.55),
            SymptomFrequency("memory_problems", 0.30, 0.40),
            SymptomFrequency("pallor", 0.25, 0.20),
            SymptomFrequency("unsteady_gait", 0.20, 0.50),
        ],
        discriminators=["macrocytosis", "vegan/PPI/metformin/autoimmune thyroid",
                        "neurological signs before Hb falls"],
        red_flags=["neurological symptoms — treat before levels return; never folate "
                   "alone first (can precipitate cord damage)"],
        investigations=[
            InvestigationProfile("B12 + folate + FBC", "diagnostic",
                                 0.85, 0.90, "NICE CKS B12"),
        ],
        management_first_line="Hydroxocobalamin IM loading then maintenance (more "
                              "frequent if neurology); investigate pernicious "
                              "anaemia; review at 3 months.",
        referral_tier="routine",
        safety_net="Numb feet, unsteadiness or memory change with tiredness — "
                   "blood test soon; tell the doctor if symptoms worsen.",
        source="NICE CKS; BSH guidelines",
    ),
    ConditionProfile(
        condition_id="dvt",
        name="Deep vein thrombosis",
        category="haematology",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("calf_swelling_pain", 0.90, 0.80),
            SymptomFrequency("hot_swollen_skin", 0.40, 0.20),
        ],
        discriminators=["unilateral swelling >3 cm difference", "Wells DVT score",
                        "recent surgery/immobility/cancer/oestrogen"],
        red_flags=["chest pain/breathlessness — PE: emergency",
                   "whole-leg swelling/phlegmasia"],
        investigations=[
            InvestigationProfile("Wells score + D-dimer", "stepwise rule-out",
                                 0.95, 0.50, "NICE NG158 VTE"),
            InvestigationProfile("duplex ultrasound", "confirm",
                                 0.95, 0.95, "NICE NG158"),
        ],
        management_first_line="Wells >= 2 (likely): proximal leg vein ultrasound within 4h; "
                              "unlikely: D-dimer, if positive scan; anticoagulate per "
                              "NICE NG158; DOAC typical.",
        referral_tier="urgent",
        safety_net="A swollen, painful calf — same-day assessment; breathlessness "
                   "with it = 999.",
        source="NICE NG158 VTE",
    ),
    ConditionProfile(
        condition_id="leukaemia_suspect",
        name="Suspected leukaemia (urgent)",
        category="haematology",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("fatigue", 0.80, 0.05),
            SymptomFrequency("fever", 0.40, 0.05),
            SymptomFrequency("night_sweats", 0.30, 0.25),
            SymptomFrequency("weight_loss", 0.35, 0.30),
            SymptomFrequency("bruising_easy", 0.35, 0.55),
            SymptomFrequency("pallor", 0.40, 0.25),
        ],
        discriminators=["cytopenias on FBC + blasts", "lymphadenopathy + "
                        "hepatosplenomegaly", "B symptoms"],
        red_flags=["any unexplained cytopenia combination = urgent haematology; "
                   "bruising + fever + pallor same-day if unwell"],
        investigations=[
            InvestigationProfile("FBC + blood film", "diagnostic first step",
                                 0.85, 0.90, "NICE NG12 haematological cancers"),
        ],
        management_first_line="Urgent FBC; unexplained cytopenias or blasts — "
                              "same-day/2ww haematology per NICE NG12; avoid "
                              "IM injections if severe thrombocytopenia suspected.",
        referral_tier="two_week_wait",
        safety_net="Tiredness + frequent infections + bruising or drenching night "
                   "sweats — blood test promptly.",
        source="NICE NG12 haematological",
    ),
    ConditionProfile(
        condition_id="thrombocytopenia_2ww",
        name="Unexplained thrombocytopenia / bruising (suspected haematological)",
        category="haematology",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("bruising_easy", 0.80, 0.60),
            SymptomFrequency("non_blanching_rash", 0.40, 0.50),
            SymptomFrequency("gum_bleeding", 0.30, 0.65),
            SymptomFrequency("nose_bleed", 0.30, 0.40),
        ],
        discriminators=["platelets < 100 unexplained", "wet purpura (blisters in "
                        "mouth) = emergency", "drug-induced vs ITP vs marrow"],
        red_flags=["platelets < 20 or any wet purpura/active bleeding — emergency",
                   "petechiae + fever — meningococcal/leukaemia pathways"],
        investigations=[
            InvestigationProfile("FBC + film (repeat to exclude clumped)", "confirm",
                                 0.90, 0.90, "BSH thrombocytopenia"),
        ],
        management_first_line="Confirm true thrombocytopenia (citrate tube if "
                              "clumping); avoid IM/NSAIDs; urgent haematology; "
                              "2ww if unexplained persistent (NICE NG12).",
        referral_tier="two_week_wait",
        safety_net="Sudden widespread bruising or pinpoint rash, especially with "
                   "fever or mouth blood blisters — emergency.",
        source="NICE NG12; BSH",
    ),

    # ================= TROPICAL TASTER (full module Stage 2) =================
    ConditionProfile(
        condition_id="malaria_falciparum",
        name="Malaria (falciparum) — fever after travel",
        category="infection",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("fever_after_travel", 1.00, 0.85),
            SymptomFrequency("fever", 0.95, 0.05),
            SymptomFrequency("headache", 0.60, 0.05),
            SymptomFrequency("myalgia", 0.60, 0.05),
            SymptomFrequency("jaundice", 0.20, 0.45),
            SymptomFrequency("drowsiness", 0.15, 0.35),
        ],
        discriminators=["returned from malaria zone within 12 months (usually <3 "
                        "months)", "no prophylaxis or imperfect use",
                        "any fever after travel = same-day bloods"],
        red_flags=["falciparum can kill within 24 h", "confusion, jaundice, low "
                   "platelets, renal impairment = severe malaria: emergency",
                   "children and pregnant women deteriorate fastest"],
        investigations=[
            InvestigationProfile("urgent malaria blood film / rapid test", "same-day; "
                                 "repeat if initially negative", 0.95, 0.99,
                                 "UKHSA malaria guidelines"),
        ],
        management_first_line="Ask travel history at every fever; same-day thick/thin "
                              "films; positive falciparum = same-day admission for "
                              "IV artesunate if any severity signs (UKHSA).",
        referral_tier="emergency",
        safety_net="Any fever within a year of visiting a malaria country — same-day "
                   "medical assessment with blood tests; do not wait.",
        dangerous_mimic_of=["viral_urti", "influenza", "gastroenteritis"],
        source="UKHSA malaria guidelines (2023)",
    ),
    ConditionProfile(
        condition_id="dengue",
        name="Dengue — fever after travel",
        category="infection",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("fever_after_travel", 1.00, 0.75),
            SymptomFrequency("severe_backache", 0.50, 0.75),
            SymptomFrequency("retro_orbital_pain", 0.40, 0.80),
            SymptomFrequency("blotchy_rash", 0.40, 0.25),
            SymptomFrequency("bruising_easy", 0.20, 0.45),
        ],
        discriminators=["travel to endemic region", "breakbone myalgia",
                        "thrombocytopenia", "warning: deterioration around day 4-6 "
                        "as fever settles"],
        red_flags=["severe abdominal pain, persistent vomiting, bleeding gums, "
                   "lethargy — severe dengue: emergency", "shock"],
        investigations=[
            InvestigationProfile("FBC (platelets/haematocrit) + NS1/IgM", "monitor "
                                 "severity", 0.80, 0.90, "WHO/UKHSA dengue"),
        ],
        management_first_line="Same-day assessment; FBC tracking; paracetamol ONLY "
                              "(avoid NSAIDs/aspirin — bleeding); admit if warning "
                              "signs or falling platelets.",
        referral_tier="urgent",
        safety_net="Fever after tropical travel with severe backache/eye pain — "
                   "same-day bloods; avoid ibuprofen; return immediately if "
                   "abdominal pain or bleeding as fever settles.",
        source="WHO/UKHSA dengue guidance",
    ),
    ConditionProfile(
        condition_id="typhoid",
        name="Enteric fever (typhoid) — fever after travel",
        category="infection",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("fever_after_travel", 1.00, 0.70),
            SymptomFrequency("abdominal_pain", 0.50, 0.10),
            SymptomFrequency("constipation", 0.30, 0.30),
            SymptomFrequency("headache", 0.60, 0.05),
            SymptomFrequency("confusion", 0.20, 0.30),
        ],
        discriminators=["stepwise rising fever over days", "relative bradycardia",
                        "returned from South Asia/W Africa; incomplete vaccination"],
        red_flags=["GI bleeding/perforation (rising pulse + rigid abdomen)",
                   "confusion", "severe illness"],
        investigations=[
            InvestigationProfile("blood cultures (x2)", "diagnostic",
                                 0.80, 0.95, "UKHSA enteric fever"),
        ],
        management_first_line="Same-day blood cultures before antibiotics; discuss "
                              "with infectious diseases; admission usually; notify "
                              "UKHSA; screen contacts/exclude from food handling.",
        referral_tier="urgent",
        safety_net="Fever rising day by day after travel, with constipation or "
                   "abdominal pain — same-day assessment with cultures.",
        dangerous_mimic_of=["viral_urti", "gastroenteritis"],
        source="UKHSA enteric fever guidance",
    ),
]

# Part-2 symptom tokens -> free-text match phrases (merged into
# knowledge.SYMPTOM_SYNONYMS at import; the corpus integrity test enforces
# every token has an entry SOMEWHERE in the merged dict).
SYMPTOM_SYNONYMS_PART2: Dict[str, list] = {
    # endocrine
    "polyuria": ["passing lots of urine", "urinating a lot", "weeing constantly",
                 "polyuria", "getting up at night to urinate"],
    "polydipsia": ["really thirsty", "always thirsty", "drinking a lot", "polydipsia",
                   "can't stop drinking"],
    "ketone_breath": ["fruity breath", "pear drops", "acetone breath", "smell of "
                      "nail polish remover"],
    "recurrent_infections": ["keep getting infections", "repeated infections",
                             "one infection after another"],
    "blurred_vision": ["blurred vision", "blurry", "vision is blurry",
                       "can't see clearly", "eyesight blurry"],
    "dehydration_signs": ["dry mouth", "dry tongue", "sunken eyes", "skin tenting",
                          "very dry", "not drinking"],
    "weight_gain": ["gaining weight", "putting on weight", "weight gain"],
    "cold_intolerance": ["always cold", "can't get warm", "feeling the cold",
                         "cold all the time"],
    "constipation": ["constipated", "constipation", "can't open bowels", "hard stools"],
    "dry_skin": ["dry skin", "skin is dry", "flaky skin"],
    "hair_thinning": ["hair falling out", "hair thinning", "losing hair", "alopecia"],
    "heat_intolerance": ["always hot", "can't stand heat", "sweating easily",
                         "intolerant of heat"],
    "tremor": ["shaky hands", "tremor", "trembling", "shaking"],
    "hunger": ["very hungry", "starving all the time", "hungry constantly"],
    "goitre": ["neck swelling", "swelling in the neck", "goitre", "goiter",
               "lump in the front of my neck"],
    "hyperpigmentation": ["darkened skin", "skin going darker", "bronze skin",
                          "pigmentation", "dark creases"],
    "bone_pain": ["bone pain", "deep pain in the bones", "aching bones"],
    # infection
    "shivering_rigors": ["rigors", "shivering", "shaking with fever", "teeth "
                         "chattering", "violent shivering"],
    "reduced_urine_output": ["not passing urine", "no urine", "hardly any urine",
                             "not peeing", "oliguria", "not passed urine"],
    "fast_breathing": ["breathing fast", "rapid breathing", "fast breathing",
                       "tachypnoea", "breathing quickly"],
    "spreading_redness": ["spreading redness", "redness spreading", "getting redder",
                          "red area growing", "red streaking"],
    "hot_swollen_skin": ["hot and red", "skin hot to touch", "warm swollen area",
                         "hot swollen"],
    "ear_pain": ["earache", "ear pain", "painful ear", "ear hurts"],
    "reduced_hearing": ["can't hear well", "muffled hearing", "deaf in one ear",
                        "hearing reduced", "hard of hearing suddenly"],
    "ear_discharge": ["discharge from ear", "pus from the ear", "weeping ear",
                      "liquid from the ear"],
    "pus_on_tonsils": ["white spots on tonsils", "pus on tonsils", "pus on the "
                       "throat", "exudate on tonsils"],
    "swollen_glands": ["swollen glands", "lumps in the neck", "lymph nodes swollen",
                       "swollen glands in the groin"],
    "flank_pain": ["flank pain", "loin pain", "pain in my side", "kidney pain",
                   "pain in the side of my back"],
    "sandpaper_rash": ["sandpaper rash", "rough rash", "raspy rash texture",
                       "like sandpaper"],
    "strawberry_tongue": ["strawberry tongue", "red bumpy tongue", "white then red "
                          "tongue"],
    "blotchy_rash": ["blotchy rash", "red blotches", "spotty rash", "maculopapular",
                     "rash spreading down the body"],
    "red_eye": ["red eye", "bloodshot", "eye is red", "red eyes"],
    "koplik_spots": ["koplik", "white spots inside the cheek"],
    "vesicular_rash": ["fluid-filled blisters", "blisters", "vesicles",
                       "clear fluid spots", "water blisters"],
    "itchy_skin": ["itchy", "itching", "itchy rash", "scratching a lot", "pruritus"],
    # paediatric
    "poor_feeding": ["not feeding", "off feeds", "poor feeding", "not eating",
                     "refusing milk"],
    "reduced_fluid_intake": ["not drinking", "drinking less", "won't take fluids",
                             "off drinks", "poor fluid intake"],
    "barking_cough": ["barking cough", "seal-like cough", "barky cough", "croupy "
                      "cough", "like a seal"],
    "stridor": ["stridor", "noisy breathing in", "harsh noise breathing in"],
    "redcurrant_jelly_stool": ["redcurrant jelly", "jelly-like bloody stool",
                               "blood and mucus in the nappy"],
    "drawing_up_legs": ["drawing up legs", "pulling legs up", "knees to chest",
                        "legs pulled up screaming"],
    "pallor_episodes": ["goes pale", "pale episodes", "turns white", "as pale as "
                        "a sheet intermittently"],
    "cold_hands_feet": ["cold hands and feet", "cold peripheries", "hands and feet "
                        "are cold"],
    "limb_pain": ["limb pain", "leg pain worse than expected", "arm or leg pain "
                  "severe"],
    # geriatric
    "fall": ["fell over", "had a fall", "falls", "kept falling", "collapsed to the "
             "floor", "fallen"],
    "fluctuating_confusion": ["confusion comes and goes", "fluctuating", "confused "
                              "then lucid", "worse at night then better", "sundowning"],
    "hallucination": ["hallucinating", "hearing voices", "seeing things", "visions",
                      "talking to people who aren't there"],
    "reduced_mobility": ["not walking", "off legs", "can't walk like before",
                         "stopped walking", "off her feet", "off his feet"],
    "skin_breakdown": ["pressure sore", "bed sore", "skin breakdown", "open area on "
                       "the heel", "wound on the hip", "pressure ulcer"],
    "medication_change_recent": ["new tablet", "recently started medication",
                                 "dose was increased", "new medication", "changed "
                                 "tablets", "started a new drug"],
    # mental health
    "low_mood": ["low mood", "feeling down", "depressed", "sad all the time",
                 "can't be bothered"],
    "anhedonia": ["no enjoyment", "nothing is fun any more", "lost interest",
                  "don't enjoy anything", "anhedonia", "can't enjoy anything",
                  "can't enjoy", "no pleasure in anything"],
    "poor_sleep": ["can't sleep", "not sleeping", "insomnia", "waking at night",
                   "poor sleep", "trouble sleeping", "sleeping badly"],
    "poor_concentration": ["can't concentrate", "poor concentration", "brain fog",
                           "can't focus", "forgetting things"],
    "suicidal_thoughts": ["suicidal", "want to die", "ending it all", "kill myself",
                          "thoughts of harming myself", "better off dead"],
    "hopelessness": ["hopeless", "no point", "nothing to live for", "despair"],
    "excessive_worry": ["worrying all the time", "can't stop worrying", "worry about "
                        "everything", "excessive worry"],
    "restlessness": ["restless", "can't relax", "on edge physically", "fidgety"],
    "delusion": ["delusion", "believes people are against", "paranoid", "conspiracy "
                 "about them", "thoughts people are reading their mind"],
    "social_withdrawal": ["staying in the room", "not seeing friends", "withdrawing",
                          "isolating", "stopped going out"],
    "disorganised_thinking": ["thoughts are jumbled", "speech doesn't make sense",
                              "jumping between topics", "incoherent"],
    "fear_of_weight_gain": ["terrified of gaining weight", "scared of being fat",
                            "fear of weight gain"],
    "restricted_eating": ["hardly eating", "restricting food", "cutting out meals",
                          "counting every calorie", "avoiding food"],
    "amenorrhoea": ["periods stopped", "no period for months", "missed periods",
                    "amenorrhoea"],
    "morning_shakes": ["shaking in the morning", "need a drink to steady",
                       "morning shakes", "hands shake until first drink"],
    "alcohol_craving": ["craving alcohol", "need a drink", "can't stop drinking",
                        "alcohol dependent", "drinking every day"],
    # audit missing-area 2 (2026-09-04): the entry existed but common
    # phrasings missed it - a bottle-of-wine-a-night question drew nothing
    "alcohol_heavy_pattern": [
        "drink every day", "drinks every day", "drink every night",
        "drinks every night", "bottle of wine a night",
        "bottle of wine every night", "wine every night",
        "drinks a bottle", "cans every night", "spirits every day",
        "vodka every", "units a week", "units a day",
        "drinking too much", "drinks too much", "hiding drink",
        "hidden bottles", "drinking alone", "detox before",
    ],
    "insomnia_severe": ["not sleeping at all", "severe insomnia", "awake all night "
                        "every night"],
    # musculoskeletal
    "knee_pain": ["knee pain", "knee hurts", "painful knee", "both knees ache"],
    "joint_stiffness": ["stiff joints", "joint stiffness", "stiff in the morning"],
    "morning_stiffness_prolonged": ["stiff for more than an hour", "morning stiffness "
                                    "over an hour", "stiffness lasts hours"],
    "symmetrical_joint_pain": ["both hands hurt", "same joints both sides",
                               "symmetrical joint pain", "both wrists and hands"],
    "small_joint_swelling": ["swollen fingers", "knuckles swollen", "swollen hands",
                             "swollen joints in the fingers"],
    "big_toe_pain": ["big toe pain", "pain in the big toe", "first toe", "podagra"],
    "hot_swollen_joint": ["hot swollen joint", "joint is hot and swollen",
                          "swollen red joint", "knee is hot and swollen",
                          "joint hot to touch"],
    "unable_weight_bear": ["can't put weight on", "can't walk on it",
                           "unable to weight bear", "can't stand on it"],
    "joint_pain_severe": ["severe joint pain", "joint agony", "excruciating joint"],
    "girdle_pain_stiffness": ["shoulders and hips stiff", "aching shoulders and upper "
                              "arms", "thighs and shoulders ache", "girdle stiffness"],
    "jaw_claudication": ["jaw pain chewing", "jaw aches when eating", "chewing makes "
                         "jaw ache", "jaw tires when chewing"],
    "scalp_tenderness": ["scalp tender", "scalp hurts to touch", "head tender to "
                         "touch", "sore to brush hair"],
    "pins_needles_leg": ["pins and needles in the leg", "leg feels numb and tingly",
                         "numb leg", "tingling down the leg"],
    "pain_after_minimal_trauma": ["after a minor fall", "no injury just bent down",
                                  "sudden pain without injury", "coughed and then pain",
                                  "minimal trauma"],
    # dermatology
    "scaly_plaques": ["scaly patches", "silvery scale", "flaky plaques", "thick scaly "
                      "skin", "well-defined scaly"],
    "nail_pitting": ["pitted nails", "nail pitting", "little dents in nails",
                     "nails coming away"],
    "changing_mole": ["mole changing", "mole has changed", "mole getting bigger",
                      "changed shape", "mole looks different", "new mole"],
    "bleeding_mole": ["mole bleeding", "mole that bleeds", "bleeding from a mole"],
    "burning_skin_pain": ["burning skin", "skin on fire", "burning pain before the "
                          "rash", "stinging pain on the skin"],
    "one_sided_rash": ["one side only", "rash on one side", "doesn't cross the "
                       "middle", "left side only", "right side only"],
    "flexural_rash": ["rash in the creases", "inside elbows", "behind knees",
                      "rash in the folds"],
    # ent / eye
    "eye_pain_severe": ["eye pain", "painful eye", "eye really hurts", "deep eye "
                        "ache", "pain in the eye"],
    "vision_reduced": ["can't see properly", "vision got worse", "sight is reduced",
                       "blurred and reduced vision", "vision decreased"],
    "halos_around_lights": ["halos around lights", "rainbow rings around lights",
                            "lights have halos"],
    "gritty_eye": ["gritty eye", "something in my eye", "sandy feeling eye",
                   "eye feels gritty"],
    "eye_discharge": ["eye discharge", "pus in the eye", "eyes stuck together",
                      "weeping eye", "yellow discharge from eye"],
    "flashes_lights": ["flashing lights", "flashes in the eye", "light flashes",
                       "lightning streaks"],
    "floaters_sudden": ["floaters", "sudden floaters", "cobwebs in my vision",
                        "spots floating", "shower of black dots"],
    "visual_curtain": ["curtain over my vision", "shadow across the eye", "like a "
                       "curtain coming down", "part of vision missing"],
    "facial_pressure_pain": ["facial pressure", "cheek pain", "face pain over the "
                             "sinuses", "pressure under the eyes", "sinus pain"],
    "purulent_nasal_discharge": ["green mucus from nose", "yellow nasal discharge",
                                 "pus from the nose", "infected mucus"],
    "nose_bleed": ["nose bleed", "nosebleed", "nose is bleeding", "bleeding nose"],
    "positional_vertigo": ["dizzy when i roll over", "spinning when i turn in bed",
                           "dizzy looking up", "vertigo on position change",
                           "spins when i get out of bed", "spins when i move",
                           "dizzy when i move quickly", "spinning when i move"],
    "rotational_dizziness": ["room spinning", "everything spins", "vertigo",
                             "spinning sensation", "the room is rotating",
                             "room spins", "the room spins",
                             "everything is spinning"],
    # women's health
    "lower_abdominal_pain": ["lower abdominal pain", "pelvic pain", "lower tummy "
                             "pain", "pain below the belly"],
    "missed_period": ["missed period", "period is late", "no period", "late period"],
    "vaginal_bleeding": ["vaginal bleeding", "bleeding from the vagina", "period "
                         "heavier than ever", "bleeding between periods"],
    "shoulder_tip_pain": ["shoulder tip pain", "pain at the tip of the shoulder",
                          "pain in the shoulder tip"],
    "swelling_hands_face": ["swollen hands", "swollen face", "face is puffy",
                            "rings too tight", "swelling of hands and face"],
    "epigastric_pain": ["epigastric", "pain under the ribs right side in pregnancy",
                        "pain at the top of the bump"],
    "vaginal_discharge": ["discharge", "vaginal discharge", "unusual discharge",
                          "new discharge with odour"],
    "deep_dyspareunia": ["deep pain during sex", "painful intercourse deep",
                         "deep dyspareunia", "pain during sex inside"],
    "intermenstrual_bleeding": ["bleeding between periods", "spotting between "
                                "periods"],
    "heavy_menstrual_bleeding": ["heavy periods", "periods very heavy", "flooding",
                                 "very heavy menstrual bleeding"],
    "clots_flooding": ["passing clots", "large clots", "flooding through pads"],
    "breast_lump": ["lump in the breast", "breast lump", "found a lump in my breast",
                    "breast is lumpy in one spot"],
    "nipple_change": ["nipple turned in", "nipple discharge", "nipple retracted",
                      "nipple has changed", "nipple rash", "blood from the nipple"],
    "skin_change_breast": ["skin dimpling on the breast", "breast skin changing",
                           "orange peel skin on the breast", "peau d'orange"],
    # urology / kidney
    "groin_pain": ["groin pain", "pain into the groin", "pain toward the groin",
                   "testicle and groin pain"],
    "haematuria_visible": ["blood in urine", "visible blood in urine", "pink urine",
                           "red urine", "blood in my wee", "coke-coloured urine"],
    "testicular_pain": ["testicle pain", "testicular pain", "painful testicle",
                        "ball hurts", "scrotal pain"],
    "testicular_swelling": ["swollen testicle", "testicle is swollen", "swollen "
                            "scrotum"],
    "nocturia": ["waking at night to urinate", "nocturia", "up three times a night "
                 "to pee",
                 # 7.2: the '... to pass urine' phrasing of the same complaint
                 "up at night to pass urine", "up twice a night to pass urine",
                 "up three times a night to pass urine"],
    "weak_urine_stream": ["poor stream", "weak flow", "takes ages to start urinating",
                          "difficulty starting", "straining to pass urine",
                          # 7.2: plain 'weak stream' as patients say it
                          "weak stream", "weak urine stream"],
    # haematology
    "pallor": ["pale", "looking pale", "pale as a ghost", "very pale"],
    "bruising_easy": ["bruising easily", "easy bruising", "bruises appearing without "
                      "injury", "unexplained bruising"],
    "gum_bleeding": ["bleeding gums", "gums bleeding"],
    "paraesthesia_feet": ["numb feet", "pins and needles in feet", "tingling feet",
                          "feet feel numb"],
    "memory_problems": ["memory problems", "forgetting", "can't remember things",
                        "memory getting worse"],
    "unsteady_gait": ["unsteady on my feet", "off balance", "unsteady walking",
                      "wobbly walking"],
    # tropical
    # 8.1: the bare country entries (" in india"...) are gone — they fired
    # malaria on ANY mention of the country ("worked in India for years"),
    # the same over-reach that made a Nepal trek a rabies 999. Country
    # presence now needs a RECENCY or TRAVEL binding (weeks in, holiday
    # in...); long-ago residence belongs to the endemic-area tokens at
    # low specificity, never to a fever token.
    "fever_after_travel": ["fever after travel", "just back from", "returned from "
                           "abroad", "returned from", "returning from",
                           "holiday in africa", "holiday in asia",
                           "holiday in india", "holiday in south america",
                           "travelled to", "back from africa",
                           "back from asia", "back from india", "back from south "
                           "america", "visiting family overseas", "fever since "
                           "getting back", "malaria area",
                           "weeks in", "week in", "days in", "month in",
                           "trip to africa", "trip to asia", "trip to india",
                           "trip to south america"],
    "retro_orbital_pain": ["pain behind the eyes", "retro-orbital pain",
                           "eye socket pain"],
    "severe_backache": ["severe backache", "back pain terrible", "spine aches "
                        "intensely", "whole back aching badly"],
}

