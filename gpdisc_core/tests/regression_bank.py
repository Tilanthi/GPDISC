"""Dangerous-mimic regression bank — diagnostic reasoning as curriculum.

Stage 5, Task 3. Forty presentations with the behaviour the GPDISC
pipeline MUST show: escalation level, a leader or must-not-miss condition
in the differential (ranked, retained-dangerous, or syndrome set), and
syndrome frames where they apply. Every row was verified against the live
ConsultationPipeline; where the engine disagreed with clinical ground
truth during authoring, the SAFETY LAYER was fixed, not the expectation
(see the benign-vs-emergency safety commits).
"""
from typing import Dict, List

# escalation: expected pipeline escalation (None = deliberately unpinned).
#   Some same-day rows are pinned "emergency" rather than the urgent-rule
#   "urgent" because the clinical VALIDATOR raises them: an emergency-tier
#   corpus condition ranking as a genuine contender (>= 0.5x the leader's
#   score, e.g. malaria_falciparum on any returning-traveller fever, bowel
#   obstruction leading an acute abdomen) floors the escalation. A RAISE,
#   never a weaken (2026-09-03 validation layer).
# leader_or_retained: acceptable condition ids (any hit passes). On an
#   emergency/urgent short-circuit the record carries the SAFETY RULE id
#   ("acs", "sepsis", "pe"...) rather than a corpus id — rule ids are listed
#   alongside the corpus conditions they stand for.
# syndrome: expected syndrome frame key (omitted = none expected)
BANK: List[Dict] = [
    # ---- Emergencies (14): the must-never-miss bank ----
    {"case": "crushing central chest pain for 30 minutes, sweating, "
             "pain radiating to the left arm, 66 year old smoker",
     "escalation": "emergency",
     "leader_or_retained": ["acs_stemi", "acs_nstemi", "acs"]},
    {"case": "chest pain and breathless, pain worse on breathing in, "
             "swollen right calf after a long flight last week",
     "escalation": "emergency",
     "leader_or_retained": ["pe_pulmonary_embolism", "pe"]},
    {"case": "sudden drooping face and slurred speech this morning",
     "escalation": "emergency",
     "leader_or_retained": ["stroke_tia", "stroke_fast"]},
    {"case": "my father is confused, breathing fast, feverish and hasn't "
             "passed urine since morning",
     "escalation": "emergency",
     "leader_or_retained": ["sepsis_adult", "sepsis"]},
    {"case": "worst headache of my life came on like a blow an hour ago "
             "with vomiting",
     "escalation": "emergency",
     "leader_or_retained": ["sah_subarachnoid", "thunderclap_headache"]},
    {"case": "back pain and now can't control my bladder, numbness in the "
             "saddle area",
     "escalation": "emergency",
     "leader_or_retained": ["cauda_equina"]},
    {"case": "my 3 year old has fever and a rash that doesn't fade when "
             "pressed, drowsy",
     "escalation": "emergency",
     "leader_or_retained": ["meningococcal_child"],
     "syndrome": "fever_rash"},
    {"case": "muffled hot potato voice, drooling, can't swallow saliva, "
             "severe sore throat",
     "escalation": "emergency",
     "leader_or_retained": ["epiglottitis_adult", "quinsy_peritonsillar",
                            "airway_obstruction"]},
    {"case": "fever, headache, neck stiffness and light hurts my eyes",
     "escalation": "emergency",
     "leader_or_retained": ["meningitis"]},
    {"case": "6 weeks pregnant and bleeding heavily with one-sided pain",
     "escalation": "emergency",
     "leader_or_retained": ["ectopic_pregnancy"]},
    {"case": "diabetic, vomiting for two days, drowsy, breathing deeply "
             "and fast",
     "escalation": "emergency",
     "leader_or_retained": ["dka"]},
    {"case": "vomiting blood after a night of retching and alcohol",
     "escalation": "emergency",
     "leader_or_retained": ["gi_bleed_upper", "gi_bleed"]},
    {"case": "sudden loss of vision in one eye like a curtain coming down",
     "escalation": "emergency",
     "leader_or_retained": ["retinal_detachment", "gca_eye", "visual_curtain"]},
    {"case": "blackout with no warning while sitting, palpitations just "
             "before it happened",
     "escalation": "urgent",
     "leader_or_retained": ["cardiac_syncope", "tachyarrhythmia_af"]},

    # ---- Urgent / same-day (10) ----
    # NB: this row's escalation is "emergency" rather than the urgent-rule
    # "urgent" because the validator raises it: malaria_falciparum (corpus
    # tier: emergency — same-day admission) ranks top-3, and a ranked
    # emergency-tier leader is the floor for the stated escalation. A
    # RAISE, never a weaken (2026-09-03 validation layer).
    {"case": "fever for two days since returning from Ghana",
     "escalation": "emergency",
     "leader_or_retained": ["malaria_falciparum"],
     "syndrome": "fever_after_travel"},
    {"case": "high fever for three days since returning from Nigeria with "
             "a rash appearing",
     "escalation": "emergency",
     "leader_or_retained": ["malaria_falciparum", "meningococcal_child"],
     "syndrome": "fever_after_travel"},
    {"case": "fever and one week in Thailand, mosquito bites everywhere",
     "escalation": "emergency",
     "leader_or_retained": ["dengue", "malaria_falciparum"],
     "syndrome": "fever_after_travel"},
    {"case": "routine bloods show raised eosinophils, back from Kenya "
             "three months ago",
     "escalation": None,
     "leader_or_retained": ["strongyloidiasis", "schistosomiasis_acute",
                            "hookworm"],
     "syndrome": "eosinophilia_returning_traveller"},
    {"case": "fever after returning from Vietnam, platelets are low on "
             "the bloods",
     "escalation": "emergency",
     "leader_or_retained": ["dengue", "malaria_falciparum"],
     "syndrome": "fever_after_travel"},
    {"case": "fever and yellow eyes after returning from a trip with "
             "freshwater swimming",
     "escalation": "urgent",
     "leader_or_retained": ["leptospirosis", "hepatitis_a"],
     "syndrome": "fever_after_travel"},
    {"case": "mouth ulcer that has not healed for six weeks, smoker",
     "escalation": None,
     "leader_or_retained": ["oral_cancer_suspect"]},
    {"case": "coughing up blood for a week, 46 year old, lost weight",
     "escalation": None,
     "leader_or_retained": ["lung_cancer_suspect", "tb_pulmonary",
                            "acs_stemi"]},
    {"case": "painful swollen calf after a long coach journey, mild "
             "breathlessness",
     "escalation": "emergency",
     "leader_or_retained": ["dvt_leg", "pe_pulmonary_embolism", "pe"]},
    {"case": "severe constant abdominal pain out of proportion, "
             "distended and very tender",
     "escalation": "emergency",
     "leader_or_retained": ["acute_mesenteric_ischaemia", "surgical_abdomen",
                            "bowel_obstruction"]},

    # ---- Routine / benign (12): must NOT escalate ----
    {"case": "mild bilateral headache coming on over days after stress, "
             "no other symptoms",
     "escalation": "routine",
     "leader_or_retained": ["tension_headache"]},
    {"case": "low back pain after lifting boxes at the weekend, worse "
             "with movement, no leg symptoms",
     "escalation": "routine",
     "leader_or_retained": ["back_pain_mechanical", "lumbago_nonspecific"]},
    {"case": "dry itchy skin in the elbow creases, comes and goes, "
             "worse with soap, no fever",
     "escalation": None,
     "leader_or_retained": ["eczema_atopic"]},
    {"case": "recurrent painful mouth ulcers in crops, otherwise well",
     "escalation": None,
     "leader_or_retained": ["aphthous_ulcers"]},
    {"case": "sore throat, runny nose and cough for three days, no fever, "
             "no tonsillar pus",
     "escalation": None,
     "leader_or_retained": ["viral_urti", "common_cold"]},
    {"case": "room spinning for a few seconds whenever I turn over in bed",
     "escalation": None,
     "leader_or_retained": ["bppv", "vertigo_bppv"]},
    {"case": "18 year old, tired, sore throat, swollen neck glands for a "
             "week, no drooling",
     "escalation": None,
     "leader_or_retained": ["glandular_fever"]},
    {"case": "white coating on my tongue since starting a steroid "
             "inhaler, well in myself, no pain on swallowing",
     "escalation": None,
     "leader_or_retained": ["oral_candidiasis"]},
    {"case": "burning upper abdominal pain after spicy food, 34 year old, "
             "no weight loss",
     "escalation": None,
     "leader_or_retained": ["gerd", "dyspepsia_functional"]},
    {"case": "fever for two days after a holiday in Portugal, no rash",
     "escalation": None,
     "leader_or_retained": ["viral_urti", "influenza"]},
    {"case": "burning when passing urine for two days, no fever, no "
             "loin pain, woman of 30",
     "escalation": None,
     "leader_or_retained": ["urinary_tract_infection_simple"]},
    {"case": "tired all the time, sleeping badly, stress at work, "
             "periods normal",
     "escalation": None,
     "leader_or_retained": ["tired_all_the_time", "iron_deficiency",
                            "hypothyroidism"]},

    # ---- Syndrome-specific (4) ----
    {"case": "fever and a widespread rash that started yesterday, no "
             "travel, adult",
     "escalation": None,
     "leader_or_retained": ["meningococcal_child", "viral_exanthem",
                            "measles"],
     "syndrome": "fever_rash"},
    {"case": "returned from Ghana, fever, dark urine and yellow eyes",
     "escalation": "emergency",
     "leader_or_retained": ["malaria_falciparum", "leptospirosis",
                            "hepatitis_a"],
     "syndrome": "fever_after_travel"},
    {"case": "back three months from working in Tanzania, routine bloods "
             "show eosinophils raised, itchy rash was present",
     "escalation": None,
     "leader_or_retained": ["strongyloidiasis", "schistosomiasis_acute"],
     "syndrome": "eosinophilia_returning_traveller"},
    {"case": "fever and confusion in my 80 year old mother, not passing "
             "much urine",
     "escalation": "emergency",
     "leader_or_retained": ["sepsis_adult", "uti_elderly", "sepsis"]},
    # ---- Stage 6 Task 6.3: trauma & burns (the audit's empty-
    # differential probes, now locked) ----
    {"case": "my husband fell off a ladder and hit his head, he was "
             "knocked out for a minute and has vomited twice since",
     "escalation": "emergency",
     "leader_or_retained": ["head_injury_red_flags",
                            "head_injury_moderate_severe"]},
    {"case": "my neighbour has been stabbed in the chest",
     "escalation": "emergency",
     "leader_or_retained": ["penetrating_trauma",
                            "penetrating_torso_trauma"]},
    {"case": "man trapped under rubble for two hours, crushed legs, "
             "pale and cold",
     "escalation": "emergency",
     "leader_or_retained": ["haemorrhagic_shock", "crush_injury"]},
    {"case": "my baby pulled a kettle of boiling water over, scalded her "
             "arm",
     "escalation": "emergency",
     "leader_or_retained": ["major_burn"]},
    {"case": "grazed my elbow in the garden, tetanus injection status "
             "unknown",
     "escalation": "urgent",
     "leader_or_retained": ["tetanus_prone_wound"]},
    # ---- Stage 6 Task 6.4: toxicology ----
    {"case": "took 20 paracetamol tablets six hours ago, feels sick",
     "escalation": "emergency",
     "leader_or_retained": ["paracetamol_overdose", "any_overdose"]},
    {"case": "found my son unconscious next to a needle, breathing "
             "slowly, blue lips",
     "escalation": "emergency",
     "leader_or_retained": ["opioid_overdose", "opioid_toxidrome"]},
    {"case": "whole family headache and nausea every evening at home, "
             "gas boiler, better at work",
     "escalation": "emergency",
     "leader_or_retained": ["carbon_monoxide_poisoning", "carbon_monoxide"]},
    {"case": "heavy drinker, in custody since yesterday, seeing things "
             "and confused",
     "escalation": "emergency",
     "leader_or_retained": ["alcohol_withdrawal_delirium",
                            "delirium_tremens"]},
    # ---- Stage 6 Task 6.5: obstetric emergencies ----
    {"case": "34 weeks pregnant, just had a seizure at home",
     "escalation": "emergency",
     "leader_or_retained": ["eclampsia", "eclampsia_seizure"]},
    {"case": "gave birth this morning, bleeding heavily, soaking pads "
             "every hour, pale and dizzy",
     "escalation": "emergency",
     "leader_or_retained": ["postpartum_haemorrhage"]},
    {"case": "the baby is coming now, contractions every two minutes, "
             "need to push",
     "escalation": "emergency",
     "leader_or_retained": ["imminent_birth"]},
    {"case": "six days after giving birth, fever 39, smelly bleeding, "
             "womb tender",
     "escalation": "emergency",
     "leader_or_retained": ["puerperal_sepsis", "sepsis",
                            "puerperal_sepsis_rule"]},
    # ---- Stage 6 Task 6.6: oncology-supportive + derm emergencies ----
    {"case": "on chemotherapy for lung cancer, fever 38.5 at home tonight",
     "escalation": "emergency",
     "leader_or_retained": ["neutropenic_sepsis"]},
    {"case": "breast cancer spread to bones, back pain worse at night, "
             "legs feel weak",
     "escalation": "emergency",
     "leader_or_retained": ["malignant_cord_compression",
                            "cord_compression_cancer"]},
    {"case": "started lamotrigine two weeks ago, now a rash with sore "
             "blistered lips and eyes, skin hurts",
     "escalation": "emergency",
     "leader_or_retained": ["stevens_johnson_ten"]},
    {"case": "calf pain far more painful than it looks after a small "
             "graze, spreading fast, fever",
     "escalation": "emergency",
     "leader_or_retained": ["necrotising_fasciitis",
                            "necrotising_infection"]},
    # ---- Stage 6 Task 6.7: paediatric protection & syndromes ----
    {"case": "my 5 month old baby has bruises on his back and i don't "
             "know how he got them",
     "escalation": "urgent",
     "leader_or_retained": ["non_accidental_injury",
                            "non_mobile_bruise"]},
    {"case": "my 2 year old has had fever for six days, both eyes red, "
             "cracked lips, so irritable",
     "escalation": "emergency",
     "leader_or_retained": ["kawasaki_disease", "kawasaki_fever_days"]},
    {"case": "7 year old, purple spots you can feel on his legs and "
             "bottom, ankles swollen, tummy pain",
     "escalation": "urgent",
     "leader_or_retained": ["iga_vasculitis_hsp"]},
    # ---- Stage 6 Task 6.8: post-exposure prophylaxis ----
    {"case": "bitten by a dog in Bali two days ago, broke the skin "
             "and bled",
     "escalation": "urgent",
     "leader_or_retained": ["rabies_exposure_risk",
                            "animal_bite_exposure"]},
    {"case": "needlestick injury, source patient known hepatitis B "
             "positive, 2 hours ago",
     "escalation": "urgent",
     "leader_or_retained": ["occupational_bbv_exposure",
                            "bloodborne_exposure_rule"]},
    # ---- Stage 7 Task 7.1: chronic neurology + mental health ----
    {"case": "my husband is 74 and getting forgetful, left the cooker on "
             "twice this month",
     "escalation": None,
     "leader_or_retained": ["dementia_suspected"]},
    {"case": "had my first ever seizure this morning, fully recovered now, "
             "never had a seizure before",
     "escalation": "urgent",
     "leader_or_retained": ["first_seizure_adult"]},
    {"case": "haven't slept for three nights, talking fast, spending money "
             "wildly, feeling invincible",
     "escalation": "urgent",
     "leader_or_retained": ["bipolar_mania"]},
    # ---- Stage 7 Task 7.2: derm + women's + men's health ----
    {"case": "I'm 52, periods stopped a year ago, hot flushes and night "
             "sweats, finding it hard to concentrate",
     "escalation": None,
     "leader_or_retained": ["menopause"]},
    {"case": "trying for a baby for two years, periods come every three "
             "months, put on weight, hairs on my chin",
     "escalation": None,
     "leader_or_retained": ["pcos", "subfertility"]},
    {"case": "difficulty getting erections for six months, still get "
             "early morning erections",
     "escalation": None,
     "leader_or_retained": ["erectile_dysfunction"]},
    # ---- Stage 7 Task 7.3: chronic GI + eyes + sleep ----
    {"case": "haven't opened my bowels for nine days, tummy is "
             "uncomfortable, hard stools",
     "escalation": None,
     "leader_or_retained": ["constipation_simple"]},
    {"case": "straight lines look wobbly in one eye, been a month, "
             "reading is hard",
     "escalation": "urgent",
     "leader_or_retained": ["wet_amd"]},
    {"case": "snoring terribly, exhausted in the day, falling asleep "
             "at the wheel",
     "escalation": None,
     "leader_or_retained": ["obstructive_sleep_apnoea"]},
    # ---- Stage 8 Task 8.1: the world (Tier 3) ----
    {"case": "collapsed in the sun at the marathon, burning hot but not "
             "sweating, temperature of 41",
     "escalation": "emergency",
     "leader_or_retained": ["heat_stroke"]},
    {"case": "at 5000 metres my friend is stumbling around camp and not "
             "making sense since the pass",
     "escalation": "emergency",
     "leader_or_retained": ["hace_cerebral_edema_altitude"]},
    {"case": "I have sickle cell disease, severe pain in my back and "
             "legs since last night, and it feels different from usual",
     "escalation": "emergency",
     "leader_or_retained": ["sickle_vaso_occlusive_crisis"]},
    {"case": "numb patches on my skin, worked in India for years, "
             "the patch on my arm has no feeling",
     "escalation": "routine",
     "leader_or_retained": ["leprosy"]},
]
