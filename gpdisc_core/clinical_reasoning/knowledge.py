"""Structured condition knowledge for the GPDISC diagnostic engine.

Content model: each condition carries symptom frequencies (proportion of
presenting cases reporting the symptom) and specificities (how strongly the
symptom discriminates toward THIS condition versus its competitors), an
anchoring prevalence in a GP consultation population, red flags,
investigations with test characteristics where established, referral tier,
and safety-net advice. Sources are named in ``source``.

Frequency/specificity values are clinical estimates for ambulatory
presentations, anchored to standard guidance (NICE/CKS/BNF) where a number
matters; they drive relative ranking, not absolute probability claims.
"""
from typing import Dict, List, Optional

from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
)


CONDITIONS: List[ConditionProfile] = [
    # ================= CARDIOVASCULAR =================
    ConditionProfile(
        condition_id="acs_stemi",
        name="Acute coronary syndrome (ST-elevation MI)",
        category="cardiovascular",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("chest_pain", 0.90, 0.55),
            SymptomFrequency("pain_radiating_arm_jaw", 0.50, 0.75),
            SymptomFrequency("sweating", 0.55, 0.40),
            SymptomFrequency("nausea", 0.40, 0.15),
            SymptomFrequency("breathlessness", 0.45, 0.30),
        ],
        discriminators=["persistent >15 min", "cardiac risk factors",
                        "ST elevation on ECG", "troponin rise"],
        red_flags=["ST elevation", "haemodynamic instability", "ongoing pain"],
        investigations=[
            InvestigationProfile("12-lead ECG", "immediate; diagnostic for STEMI",
                                 0.55, 0.95, "NICE CG95 chest pain"),
            InvestigationProfile("troponin_hs", "high-sensitivity troponin; serial; "
                                 "myocardial injury", 0.95, 0.80,
                                 "NICE chest pain pathway"),
        ],
        management_first_line="Call 999 (emergency ambulance); aspirin 300 mg chewed "
                              "unless contraindicated; do not delay transfer.",
        referral_tier="emergency",
        safety_net="Any chest pain lasting >15 minutes, or with sweating, nausea or "
                   "breathlessness, is an emergency — call 999 immediately.",
        dangerous_mimic_of=["gerd", "musculoskeletal_chest_pain", "anxiety_atacks"],
        source="NICE chest pain (NG237); ESC ACS guideline 2023",
    ),
    ConditionProfile(
        condition_id="acs_nstemi",
        name="Acute coronary syndrome (non-ST-elevation)",
        category="cardiovascular",
        prevalence_per_consult=0.006,
        symptoms=[
            SymptomFrequency("chest_pain", 0.85, 0.50),
            SymptomFrequency("pain_radiating_arm_jaw", 0.40, 0.70),
            SymptomFrequency("sweating", 0.45, 0.35),
            SymptomFrequency("breathlessness", 0.40, 0.25),
        ],
        discriminators=["pain at rest or on minimal exertion", "risk factors",
                        "troponin rise without ST elevation"],
        red_flags=["ongoing pain", "troponin rise", "dynamic ECG changes"],
        investigations=[
            InvestigationProfile("troponin_hs", "high-sensitivity troponin; serial; "
                                 "detects myocardial injury", 0.95, 0.80,
                                 "NICE chest pain pathway"),
            InvestigationProfile("12-lead ECG", "ST depression / T inversion patterns",
                                 0.40, 0.90, "NICE CG95"),
        ],
        management_first_line="Urgent same-day assessment; aspirin 300 mg if ACS strongly "
                              "suspected and no contraindication; ED via 999 if ongoing pain.",
        referral_tier="emergency",
        safety_net="Chest pain at rest, or recurring episodes of chest pressure, needs "
                   "same-day assessment — call 111/999 if ongoing.",
        dangerous_mimic_of=["gerd", "musculoskeletal_chest_pain"],
        source="NICE chest pain pathway; ESC 2023",
    ),
    ConditionProfile(
        condition_id="stable_angina",
        name="Stable angina",
        category="cardiovascular",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("chest_pain", 0.95, 0.30),
            SymptomFrequency("breathlessness", 0.35, 0.10),
            SymptomFrequency("pain_radiating_arm_jaw", 0.30, 0.40),
            # Stage 9 probe: "on exertion / relieved by rest" — the
            # textbook discriminators — previously extracted as nothing,
            # so a months-long exertional story led with STEMI
            SymptomFrequency("exertional_chest_pain", 0.85, 0.85),
            SymptomFrequency("chest_pain_relieved_by_rest", 0.80, 0.85),
        ],
        discriminators=["brought on by exertion, relieved within minutes by rest/GTN",
                        "reproducible pattern", "risk factors present"],
        investigations=[
            InvestigationProfile("resting ECG", "baseline; excludes alternative",
                                 0.20, 0.90, "NICE CG95"),
            InvestigationProfile("CT coronary angiography", "diagnostic; NICE first-line",
                                 0.95, 0.90, "NICE CG95"),
        ],
        management_first_line="GTN sublingual PRN, aspirin, statin and cardiovascular risk "
                              "assessment; arrange diagnostic testing per NICE CG95; safety-net "
                              "for changing pattern.",
        referral_tier="routine",
        safety_net="If the pain comes on at rest, lasts >15 minutes, or is new and severe, "
                   "treat as possible ACS — call 999.",
        dangerous_mimic_of=[],
        source="NICE CG95 chest pain",
    ),
    ConditionProfile(
        condition_id="aortic_dissection",
        name="Aortic dissection",
        category="cardiovascular",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("tearing_chest_back_pain", 0.60, 0.95),
            SymptomFrequency("chest_pain", 0.70, 0.30),
            SymptomFrequency("syncope", 0.15, 0.30),
            SymptomFrequency("bp_differential_arms", 0.30, 0.95),
            SymptomFrequency("breathlessness", 0.20, 0.10),
        ],
        discriminators=["tearing/migrating pain to back", "BP differential between arms",
                        "pulse deficit", "known hypertension/Marfan"],
        red_flags=["tearing pain", "neurological deficit with chest pain",
                   "BP differential", "new aortic regurgitation murmur"],
        investigations=[
            InvestigationProfile("CT angiography aorta", "definitive; do not delay",
                                 0.95, 0.95, "NICE NG51"),
            InvestigationProfile("chest X-ray", "wide mediastinum clue",
                                 0.60, 0.70, "NICE NG51"),
        ],
        management_first_line="Call 999; surgical emergency — avoid anticoagulation; "
                              "transfer to a centre with cardiothoracic capability.",
        referral_tier="emergency",
        safety_net="Sudden tearing pain into the back or between shoulder blades is an "
                   "emergency — 999.",
        dangerous_mimic_of=["musculoskeletal_chest_pain", "renal_colic_pending"],
        source="NICE NG51 aortic diseases",
    ),
    ConditionProfile(
        condition_id="pe",
        name="Pulmonary embolism",
        category="cardiovascular",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("breathlessness", 0.70, 0.30),
            SymptomFrequency("pleuritic_chest_pain", 0.55, 0.65),
            SymptomFrequency("calf_swelling_pain", 0.30, 0.70),
            SymptomFrequency("haemoptysis", 0.12, 0.60),
            SymptomFrequency("syncope", 0.10, 0.40),
        ],
        discriminators=["pleuritic pain with sudden breathlessness", "VTE risk factors",
                        "Wells PE score >= 4 or D-dimer positive"],
        red_flags=["haemodynamic instability", "hypoxia", "syncope with breathlessness"],
        investigations=[
            InvestigationProfile("Wells PE score", "pre-test probability gate",
                                 None, None, "Wells 2001; NICE NG158"),
            InvestigationProfile("D-dimer", "rule-out if low probability",
                                 0.95, 0.45, "NICE NG158"),
            InvestigationProfile("CTPA", "definitive imaging",
                                 0.95, 0.95, "NICE NG158"),
        ],
        management_first_line="If Wells >= 2 with supportive features: same-day assessment; "
                              "intermediate/high probability needs CTPA before D-dimer "
                              "(NICE NG158).",
        referral_tier="emergency",
        safety_net="Sudden breathlessness with sharp chest pain, especially after travel, "
                   "surgery or immobility — same-day assessment.",
        dangerous_mimic_of=["viral_urti", "musculoskeletal_chest_pain"],
        source="NICE NG158 VTE",
    ),
    ConditionProfile(
        condition_id="acute_heart_failure",
        name="Acute heart failure",
        category="cardiovascular",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("orthopnoea", 0.60, 0.85),
            SymptomFrequency("breathlessness", 0.90, 0.25),
            SymptomFrequency("ankle_swelling", 0.60, 0.35),
            SymptomFrequency("fatigue", 0.50, 0.05),
        ],
        discriminators=["orthopnoea/PND", "raised JVP", "bibasal crepitations",
                        "peripheral oedema"],
        red_flags=["resting breathlessness", "hypoxia", "chest pain coexisting"],
        investigations=[
            InvestigationProfile("NT-proBNP", "rule-out <400 ng/L in non-acute setting",
                                 0.95, 0.60, "NICE NG106"),
            InvestigationProfile("echocardiogram", "characterise function",
                                 0.90, 0.90, "NICE NG106"),
        ],
        management_first_line="Acute breathlessness at rest = same-day admission. "
                              "Chronic: NICE NG106 — NT-proBNP then echo, diuretics for congestion.",
        referral_tier="emergency",
        safety_net="Breathlessness worse lying flat, or waking gasping at night, needs "
                   "urgent review.",
        dangerous_mimic_of=["copd_exacerbation", "urinary_tract_infection_simple"],
        source="NICE NG106 heart failure",
    ),
    ConditionProfile(
        condition_id="aaa_leak",
        name="Leaking abdominal aortic aneurysm",
        category="cardiovascular",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("abdominal_back_flank_pain", 0.85, 0.85),
            SymptomFrequency("syncope", 0.25, 0.35),
            SymptomFrequency("pulsatile_abdominal_mass", 0.30, 0.90),
        ],
        discriminators=["pain radiating from abdomen to back in vascular-risk patient",
                        "pulsatile mass", "haemodynamic compromise"],
        red_flags=["collapse with abdominal/back pain", "hypotension"],
        investigations=[
            InvestigationProfile("bedside ultrasound/aortic scan", "immediate if stable enough",
                                 0.95, 0.95, "NICE NG156AAA_screening_programme"),
        ],
        management_first_line="Call 999 — surgical emergency; permissive hypotension; "
                              "do not delay transfer.",
        referral_tier="emergency",
        safety_net="Severe abdominal or back pain with collapse or fainting in an older "
                   "person — call 999.",
        dangerous_mimic_of=["renal_colic_pending", "lumbago_nonspecific"],
        source="NICE abdominal aortic aneurysm guidance",
    ),
    ConditionProfile(
        condition_id="tachyarrhythmia_af",
        name="Atrial fibrillation (new/undetected)",
        category="cardiovascular",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("palpitations", 0.60, 0.60),
            SymptomFrequency("breathlessness", 0.40, 0.10),
            SymptomFrequency("dizziness", 0.25, 0.15),
            SymptomFrequency("fatigue", 0.30, 0.05),
        ],
        discriminators=["irregularly irregular pulse", "ECG confirms",
                        "new AF excludes reversible causes first"],
        red_flags=["AF with haemodynamic instability or ongoing chest pain = emergency",
                   "fast AF with syncope"],
        investigations=[
            InvestigationProfile("12-lead ECG", "diagnostic",
                                 0.90, 0.95, "NICE NG196"),
        ],
        management_first_line="Rate or rhythm control plus stroke-risk assessment "
                              "(CHA2DS2-VASc / ORBIT) and bleeding risk per NICE NG196.",
        referral_tier="routine",
        safety_net="Palpitations with chest pain, fainting or breathlessness need same-day "
                   "assessment; otherwise ECG within days.",
        dangerous_mimic_of=["anxiety_atacks"],
        source="NICE NG196 atrial fibrillation",
    ),
    ConditionProfile(
        condition_id="hypertensive_urgency",
        name="Severe hypertension",
        category="cardiovascular",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("headache", 0.25, 0.05),
            SymptomFrequency("visual_disturbance", 0.15, 0.40),
            SymptomFrequency("breathlessness", 0.10, 0.05),
        ],
        discriminators=["BP >= 180/120", "check for end-organ signs"],
        red_flags=["BP >= 180/120 with headache, visual change, chest pain or "
                   "confusion = possible accelerated phase — same-day"],
        investigations=[
            InvestigationProfile("BP recording (both arms)", "confirm severity",
                                 0.95, 0.95, "NICE NG136"),
            InvestigationProfile("urinalysis + fundoscopy", "end-organ damage screen",
                                 0.50, 0.80, "NICE NG136"),
        ],
        management_first_line="Confirm with repeat reading; assess end-organ damage. "
                              "Accelerated phase (papilloedema/encephalopathy) = emergency.",
        referral_tier="urgent",
        safety_net="Severe headache or visual change with known high BP — same-day review.",
        source="NICE NG136 hypertension",
    ),
    ConditionProfile(
        condition_id="infective_endocarditis",
        name="Infective endocarditis",
        category="cardiovascular",
        prevalence_per_consult=0.0003,
        symptoms=[
            SymptomFrequency("fever", 0.90, 0.25),
            SymptomFrequency("night_sweats", 0.40, 0.45),
            SymptomFrequency("fatigue", 0.60, 0.05),
            SymptomFrequency("weight_loss", 0.30, 0.25),
            SymptomFrequency("new_murmur", 0.50, 0.80),
        ],
        discriminators=["fever + new murmur or embolic phenomenon",
                        "positive blood cultures", "IVDU or valve disease"],
        red_flags=["fever with new murmur", "embolic signs", "heart failure signs"],
        investigations=[
            InvestigationProfile("blood cultures x3", "diagnostic anchor",
                                 0.90, 0.95, "NICE CG64_endocarditis"),
            InvestigationProfile("echocardiogram", "vegetations",
                                 0.75, 0.90, "NICE endocarditis"),
        ],
        management_first_line="Suspected IE = admission; 3 sets of blood cultures before "
                              "antibiotics; do not start blind therapy in stable patients.",
        referral_tier="emergency",
        safety_net="Prolonged fever with sweats and weight loss, especially with valve "
                   "disease — urgent admission.",
        dangerous_mimic_of=["viral_urti", "influenza_pending"],
        source="NICE infective endocarditis (CG64 update); ESC 2023",
    ),

    # ================= RESPIRATORY =================
    ConditionProfile(
        condition_id="asthma_exacerbation",
        name="Acute asthma exacerbation",
        category="respiratory",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("wheeze", 0.85, 0.70),
            SymptomFrequency("breathlessness", 0.85, 0.20),
            SymptomFrequency("cough", 0.60, 0.10),
            SymptomFrequency("chest_tightness", 0.50, 0.35),
        ],
        discriminators=["wheeze + variability/diurnal pattern", "known asthma",
                        "trigger exposure", "PEF reduced"],
        red_flags=["unable to complete sentences", "silent chest", "cyanosis",
                   "exhaustion", "PEF <33% predicted = life-threatening"],
        investigations=[
            InvestigationProfile("peak expiratory flow", "severity grading",
                                 0.80, 0.80, "BTSSIGN_asthma_2019"),
        ],
        management_first_line="Salbutamol via spacer (4-10 puffs, repeat per response); "
                              "oral prednisolone 40-50 mg 5 days; assess severity per "
                              "BTS/SIGN; life-threatening features = 999.",
        referral_tier="urgent",
        safety_net="Return immediately if speech becomes difficult, lips blue, or inhaler "
                   "stops helping — 999.",
        dangerous_mimic_of=["viral_urti"],
        source="BTS/SIGN British asthma guideline 2019",
    ),
    ConditionProfile(
        condition_id="copd_exacerbation",
        name="COPD exacerbation",
        category="respiratory",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("breathlessness", 0.90, 0.25),
            SymptomFrequency("productive_cough", 0.70, 0.35),
            SymptomFrequency("purulent_sputum", 0.60, 0.50),
            SymptomFrequency("wheeze", 0.50, 0.20),
        ],
        discriminators=["known COPD", "smoking history", "purulent sputum increase",
                        "DECAF score for severity"],
        red_flags=["confusion", "cyanosis, rising CO2", "PEF/respiratory deterioration",
                   "failure to improve on treatment"],
        investigations=[
            InvestigationProfile("spironetry (stable state)", "diagnosis confirmation",
                                 0.90, 0.95, "NICE NG115"),
            InvestigationProfile("chest X-ray", "exclude pneumonia/pneumothorax",
                                 0.50, 0.70, "NICE NG115"),
        ],
        management_first_line="Prednisolone 30 mg 5 days; antibiotics if purulent sputum "
                              "(5 days); review inhaler technique; consider hospital if "
                              "DECAF/NEWS2 elevated (NICE NG115).",
        referral_tier="urgent",
        safety_net="Drowsiness, confusion or worsening breathlessness on treatment = "
                   "same-day emergency review.",
        source="NICE NG115 COPD",
    ),
    ConditionProfile(
        condition_id="community_pneumonia",
        name="Community-acquired pneumonia",
        category="respiratory",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("fever", 0.80, 0.30),
            SymptomFrequency("productive_cough", 0.75, 0.30),
            SymptomFrequency("breathlessness", 0.60, 0.20),
            SymptomFrequency("pleuritic_chest_pain", 0.40, 0.50),
            SymptomFrequency("confusion", 0.15, 0.40),
        ],
        discriminators=["focal chest signs", "CURB-65 >= 1", "consolidation on CXR"],
        red_flags=["CURB-65 >= 3", "confusion", "hypoxia/RR >= 30", "hypotension"],
        investigations=[
            InvestigationProfile("chest X-ray", "consolidation",
                                 0.85, 0.90, "NICE CG191_pneumonia"),
            InvestigationProfile("CURB-65", "severity/admission decision",
                                 None, None, "NICE CG191"),
        ],
        management_first_line="CURB-65 0-1: amoxicillin 500 mg TDS 5 days (doxycycline or "
                              "clarithromycin if penicillin-allergic) + safety-net; "
                              ">= 2: refer for admission consideration (NICE CG191).",
        referral_tier="urgent",
        safety_net="If breathing speeds up, confusion appears, or no improvement in 48 h — "
                   "urgent review.",
        dangerous_mimic_of=["viral_urti", "covid_like_illness"],
        source="NICE CG191 pneumonia",
    ),
    ConditionProfile(
        condition_id="pneumothorax",
        name="Pneumothorax",
        category="respiratory",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("pleuritic_chest_pain", 0.80, 0.60),
            SymptomFrequency("breathlessness", 0.65, 0.20),
        ],
        discriminators=["sudden onset at rest", "tall thin young male or COPD/trauma",
                        "reduced expansion/hyper-resonance"],
        red_flags=["tension physiology (tracheal deviation, hypotension) = 999",
                   "breathlessness at rest", "underlying lung disease"],
        investigations=[
            InvestigationProfile("chest X-ray", "confirm size",
                                 0.85, 0.95, "BTS_pleural_2023"),
        ],
        management_first_line="Symptomatic or large: same-day ED; aspiration/insertion per "
                              "BTS. Small primary with minimal symptoms: ambulatory per BTS.",
        referral_tier="emergency",
        safety_net="Sudden one-sided chest pain with breathlessness — same-day assessment.",
        dangerous_mimic_of=["musculoskeletal_chest_pain"],
        source="BTS pleural disease guideline 2023",
    ),
    ConditionProfile(
        condition_id="lung_cancer",
        name="Lung cancer",
        category="respiratory",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("cough", 0.65, 0.10),
            SymptomFrequency("haemoptysis", 0.25, 0.60),
            SymptomFrequency("weight_loss", 0.40, 0.45),
            SymptomFrequency("breathlessness", 0.40, 0.10),
            SymptomFrequency("chest_pain", 0.30, 0.10),
            SymptomFrequency("hoarseness", 0.15, 0.50),
            SymptomFrequency("night_sweats", 0.15, 0.25),
        ],
        discriminators=["persistent >3-week cough in smoker/ex-smoker >= 40",
                        "haemoptysis", "finger clubbing", "unexplained weight loss",
                        "persistent hoarseness", "chest X-ray lesion"],
        red_flags=["haemoptysis in smoker", "cough >3 weeks with weight loss",
                   "resolved but recurrent pneumonia"],
        investigations=[
            InvestigationProfile("chest X-ray", "first-line; report within 2 weeks? no — "
                                 "urgent CXR for suspected cancer",
                                 0.70, 0.85, "NICE NG12"),
        ],
        management_first_line="Smoker/ex-smoker with red-flag features: urgent chest X-ray "
                              "and 2ww referral if suspicious (NICE NG12).",
        referral_tier="two_week_wait",
        safety_net="Any cough lasting >3 weeks, or blood in sputum, needs review and "
                   "chest X-ray.",
        dangerous_mimic_of=["copd_exacerbation", "viral_urti"],
        source="NICE NG12 suspected cancer",
    ),
    ConditionProfile(
        condition_id="tb_pulmonary",
        name="Pulmonary tuberculosis",
        category="respiratory",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("cough", 0.80, 0.15),
            SymptomFrequency("night_sweats", 0.55, 0.55),
            SymptomFrequency("weight_loss", 0.60, 0.40),
            SymptomFrequency("fever", 0.50, 0.15),
            SymptomFrequency("haemoptysis", 0.20, 0.45),
        ],
        discriminators=["cough >3 weeks + night sweats/weight loss", "risk group "
                        "(born in/visited high-incidence country, contact, immunosuppression)",
                        "positive sputum smear/culture"],
        red_flags=["haemoptysis", "HIV co-infection", "multidrug resistance risk"],
        investigations=[
            InvestigationProfile("sputum x3 for AFB + culture", "diagnostic",
                                 0.70, 0.95, "NICE NG33"),
            InvestigationProfile("chest X-ray", "upper-lobe changes",
                                 0.80, 0.75, "NICE NG33"),
        ],
        management_first_line="Notify; 6-month RIPE regimen supervised by TB service; "
                              "contact tracing; sputum before treatment (NICE NG33).",
        referral_tier="urgent",
        safety_net="Cough lasting >3 weeks with sweats or weight loss needs investigation — "
                   "not just antibiotics.",
        dangerous_mimic_of=["viral_urti", "lung_cancer"],
        source="NICE NG33 tuberculosis",
    ),
    ConditionProfile(
        condition_id="covid_like_illness",
        name="COVID-19 / respiratory viral illness with red flags",
        category="respiratory",
        prevalence_per_consult=0.05,
        symptoms=[
            SymptomFrequency("fever", 0.70, 0.15),
            SymptomFrequency("cough", 0.75, 0.15),
            SymptomFrequency("fatigue", 0.70, 0.10),
            SymptomFrequency("loss_of_taste_smell", 0.40, 0.80),
            SymptomFrequency("breathlessness", 0.30, 0.10),
            SymptomFrequency("sore_throat", 0.40, 0.15),
        ],
        discriminators=["loss of taste/smell", "contact with case", "widespread community activity"],
        red_flags=["breathlessness at rest", "oxygen desaturation <94%", "confusion",
                   "silent hypoxia — check saturations"],
        investigations=[
            InvestigationProfile("oxygen saturations", "severity gate",
                                 0.80, 0.80, "NICE COVID19_rapid"),
        ],
        management_first_line="Symptom control + advice; breathlessness at rest or "
                              "desaturation = emergency; consider antivirals in eligible "
                              "high-risk groups.",
        referral_tier="self_care",
        safety_net="Measure saturations if unwell; breathlessness at rest, blue lips or "
                   "confusion = 999.",
        source="NICE COVID-19 rapid guidelines",
    ),

    # ================= GASTROINTESTINAL =================
    ConditionProfile(
        condition_id="gerd",
        name="Gastro-oesophageal reflux disease",
        category="gastrointestinal",
        prevalence_per_consult=0.04,
        symptoms=[
            SymptomFrequency("heartburn", 0.90, 0.80),
            SymptomFrequency("chest_pain", 0.25, 0.05),
            SymptomFrequency("dysphagia", 0.10, 0.35),
            SymptomFrequency("acid_reflux_regurgitation", 0.75, 0.70),
        ],
        discriminators=["burning retrosternal, worse lying/bending, relieved by antacid",
                        "no exertional pattern"],
        red_flags=["dysphagia", "weight loss", "vomiting blood, melaena",
                   "age >= 55 with new persistent dyspepsia"],
        investigations=[
            InvestigationProfile("H pylori stool antigen/breath test", "test-and-treat "
                                 "in dyspepsia", 0.90, 0.90, "NICE CG184"),
        ],
        management_first_line="Lifestyle + antacid/alginate; 4-week PPI trial; H pylori "
                              "test-and-treat if dyspepsia (NICE CG184).",
        referral_tier="self_care",
        safety_net="Difficulty swallowing, weight loss, vomiting blood or black stools — "
                   "urgent review; never assume 'just reflux' for persistent chest pain "
                   "without excluding cardiac causes if risk factors.",
        dangerous_mimic_of=[],
        source="NICE CG184 dyspepsia",
    ),
    ConditionProfile(
        condition_id="peptic_ulcer",
        name="Peptic ulcer disease",
        category="gastrointestinal",
        prevalence_per_consult=0.01,
        symptoms=[
            SymptomFrequency("epigastric_pain", 0.85, 0.55),
            SymptomFrequency("heartburn", 0.30, 0.10),
            SymptomFrequency("nausea", 0.30, 0.10),
            SymptomFrequency("melaena", 0.10, 0.80),
        ],
        discriminators=["NSAID/aspirin use", "H pylori positive", "food-related pattern"],
        red_flags=["melaena, haematemesis", "perforation-type sudden pain"],
        investigations=[
            InvestigationProfile("H pylori test", "treat if positive",
                                 0.90, 0.90, "NICE CG184"),
        ],
        management_first_line="Stop NSAID if possible; PPI full-dose; H pylori eradication "
                              "triple therapy; review 4-6 weeks (NICE CG184).",
        referral_tier="routine",
        safety_net="Black tarry stools or vomiting blood = emergency; sudden severe "
                   "abdominal pain = possible perforation — emergency.",
        source="NICE CG184",
    ),
    ConditionProfile(
        condition_id="gi_bleed_upper",
        name="Upper gastrointestinal haemorrhage",
        category="gastrointestinal",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("coffee_ground_vomit", 0.45, 0.95),
            SymptomFrequency("melaena", 0.60, 0.90),
            SymptomFrequency("haematemesis", 0.55, 0.95),
            SymptomFrequency("epigastric_pain", 0.40, 0.10),
            SymptomFrequency("syncope", 0.20, 0.30),
        ],
        discriminators=["vomiting blood or coffee grounds", "black tarry stool",
                        "pallor/tachycardia"],
        red_flags=["haemodynamic compromise", "continuing bleeding", "anticoagulated"],
        investigations=[
            InvestigationProfile("FBC + crossmatch", "severity",
                                 0.90, 0.60, "NICE CG141"),
        ],
        management_first_line="Call 999; NBM; stop anticoagulants under guidance; "
                              "urgent endoscopy per Glasgow-Blatchford scoring (NICE CG141).",
        referral_tier="emergency",
        safety_net="Vomiting any blood or passing black tarry stools = 999.",
        dangerous_mimic_of=["gerd", "gastroenteritis"],
        source="NICE CG141 acute upper GI bleeding",
    ),
    ConditionProfile(
        condition_id="appendicitis",
        name="Acute appendicitis",
        category="gastrointestinal",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("abdominal_pain_rif", 0.85, 0.90),
            SymptomFrequency("anorexia", 0.60, 0.40),
            SymptomFrequency("nausea", 0.60, 0.10),
            SymptomFrequency("fever", 0.40, 0.15),
            SymptomFrequency("peritonism", 0.40, 0.85),
        ],
        discriminators=["pain migrating periumbilical -> RIF", "anorexia early",
                        "RIF tenderness/guarding", "Alvarado score"],
        red_flags=["generalised peritonism", "tachycardia/hypotension", "rigid abdomen"],
        investigations=[
            InvestigationProfile("clinical scoring (Alvarado)", "support decision",
                                 None, None, "Alvarado 1986"),
            InvestigationProfile("ultrasound/CT where diagnostic doubt", "confirm",
                                 0.85, 0.90, "RCS_commissioning_guide"),
        ],
        management_first_line="Nil by mouth, urgent surgical referral; do not give "
                              "antibiotics unless directed by surgical team.",
        referral_tier="emergency",
        safety_net="Worsening right-lower abdominal pain, especially with vomiting or "
                   "pain on movement — emergency same-day.",
        dangerous_mimic_of=["gastroenteritis"],
        source="RCS commissioning guide appendicitis; NICE",
    ),
    ConditionProfile(
        condition_id="cholecystitis",
        name="Acute cholecystitis",
        category="gastrointestinal",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("ruq_pain", 0.90, 0.85),
            SymptomFrequency("fever", 0.50, 0.15),
            SymptomFrequency("nausea", 0.60, 0.10),
            SymptomFrequency("murphy_sign", 0.60, 0.80),
            SymptomFrequency("jaundice", 0.10, 0.60),
        ],
        discriminators=["RUQ pain >6 h with fever + Murphy sign", "fat intolerance history",
                        "ultrasound wall thickening"],
        red_flags=["jaundice with fever (cholangitis — emergency)", "hypotension/confusion"],
        investigations=[
            InvestigationProfile("ultrasound gallbladder", "stones/wall",
                                 0.90, 0.90, "NICE CG188_gallstones"),
            InvestigationProfile("LFTs + CRP", "supporting",
                                 0.60, 0.60, "NICE CG188"),
        ],
        management_first_line="Analgesia + IV fluids; same-day surgical assessment; "
                              "antibiotics per local policy; early cholecystectomy "
                              "pathway (NICE CG188).",
        referral_tier="emergency",
        safety_net="Fever with right-upper abdominal pain or yellowing eyes — same-day "
                   "emergency.",
        source="NICE CG188 gallstones",
    ),
    ConditionProfile(
        condition_id="pancreatitis",
        name="Acute pancreatitis",
        category="gastrointestinal",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("severe_epigastric_pain_radiating_back", 0.85, 0.90),
            SymptomFrequency("vomiting", 0.70, 0.15),
            SymptomFrequency("nausea", 0.70, 0.05),
        ],
        discriminators=["severe epigastric radiating to back", "gallstones/alcohol",
                        "amylase/lipase >3x"],
        red_flags=["hypotension, oliguria", "severe unrelenting pain", "hypoxia"],
        investigations=[
            InvestigationProfile("serum lipase", ">3x normal diagnostic",
                                 0.90, 0.95, "NICE CG104"),
        ],
        management_first_line="Admission; aggressive fluid resuscitation; analgesia; "
                              "cause identification (gallstones/alcohol) (NICE CG104).",
        referral_tier="emergency",
        safety_net="Severe upper abdominal pain going through to the back with vomiting — "
                   "emergency.",
        dangerous_mimic_of=["peptic_ulcer", "gerd"],
        source="NICE CG104 pancreatitis",
    ),
    ConditionProfile(
        condition_id="bowel_obstruction",
        name="Acute bowel obstruction",
        category="gastrointestinal",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("vomiting", 0.80, 0.25),
            SymptomFrequency("abdominal_distension", 0.70, 0.75),
            SymptomFrequency("absolute_constipation", 0.65, 0.85),
            SymptomFrequency("abdominal_pain_colicky", 0.80, 0.45),
        ],
        discriminators=["pain then vomit then stop passing stool/wind",
                        "previous abdominal surgery (adhesions)", "distension"],
        red_flags=["peritonism", "faeculent vomiting", "hypotension"],
        investigations=[
            InvestigationProfile("erect CXR + AXR/CT", "confirm level",
                                 0.80, 0.85, "RCS_guidance"),
        ],
        management_first_line="Drip and suck: NBM, IV fluids, NG tube; urgent surgical "
                              "referral.",
        referral_tier="emergency",
        safety_net="Vomiting with a swollen stomach and no bowel movements — emergency.",
        source="RCS / NICE acute abdomen pathways",
    ),
    ConditionProfile(
        condition_id="diverticulitis",
        name="Acute diverticulitis",
        category="gastrointestinal",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("left_lower_quadrant_pain", 0.85, 0.85),
            SymptomFrequency("fever", 0.40, 0.10),
            SymptomFrequency("altered_bowel_habit", 0.50, 0.15),
        ],
        discriminators=["LIF pain + tenderness", "CT confirms", "older patient"],
        red_flags=["generalised peritonism (perforation)", "unable to tolerate fluids",
                   "signs of sepsis"],
        investigations=[
            InvestigationProfile("CT abdomen", "confirm + complications",
                                 0.95, 0.95, "NICE NG147"),
        ],
        management_first_line="Uncomplicated: liquids + paracetamol; consider antibiotics; "
                              "complicated/severe: admission (NICE NG147).",
        referral_tier="urgent",
        safety_net="Left-sided abdominal pain with fever, or pain spreading across the "
                   "abdomen — urgent review.",
        source="NICE NG147 diverticular disease",
    ),
    ConditionProfile(
        condition_id="ibs",
        name="Irritable bowel syndrome",
        category="gastrointestinal",
        prevalence_per_consult=0.04,
        symptoms=[
            SymptomFrequency("abdominal_pain_relieved_defecation", 0.80, 0.80),
            SymptomFrequency("bloating", 0.70, 0.40),
            SymptomFrequency("altered_bowel_habit", 0.85, 0.20),
            SymptomFrequency("diarrhoea", 0.40, 0.05),
        ],
        discriminators=["Rome IV criteria", "symptoms >6 months, chronic relapsing",
                        "no red flags"],
        red_flags=["weight loss", "rectal bleeding", "night symptoms", "anaemia",
                   "age >= 50 new change"],
        investigations=[
            InvestigationProfile("FBC, CRP, coeliac serology", "exclude alternatives per NICE",
                                 None, None, "NICE CG61_IBS"),
        ],
        management_first_line="Diagnosis positive per Rome IV after excluding red flags; "
                              "dietary advice, low-FODMAP trial, antispasmodics (NICE CG61).",
        referral_tier="routine",
        safety_net="Blood in stools, unintended weight loss or night-time symptoms are NOT "
                   "IBS — urgent review.",
        source="NICE CG61 IBS",
    ),
    ConditionProfile(
        condition_id="gallstones",
        name="Uncomplicated gallstone disease (biliary colic)",
        category="gastrointestinal",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("ruq_pain", 0.85, 0.60),
            SymptomFrequency("nausea", 0.50, 0.05),
            SymptomFrequency("vomiting", 0.30, 0.05),
        ],
        discriminators=["episodic RUQ pain 1-6 h after fatty meal, self-limiting",
                        "no fever, no jaundice"],
        red_flags=["fever (cholecystitis)", "jaundice (obstruction)",
                   "pain >6 h continuous"],
        investigations=[
            InvestigationProfile("ultrasound biliary", "stones",
                                 0.90, 0.95, "NICE CG188"),
        ],
        management_first_line="Low-fat diet; analgesia for attacks; elective surgical "
                              "opinion; avoid opioids if possible (NICE CG188).",
        referral_tier="routine",
        safety_net="Temperature, yellowing, or pain lasting >6 hours — same-day assessment.",
        source="NICE CG188 gallstones",
    ),
    ConditionProfile(
        condition_id="colorectal_cancer",
        name="Colorectal cancer",
        category="gastrointestinal",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("rectal_bleeding", 0.40, 0.40),
            SymptomFrequency("altered_bowel_habit", 0.55, 0.20),
            SymptomFrequency("weight_loss", 0.35, 0.45),
            SymptomFrequency("fatigue", 0.40, 0.05),
            SymptomFrequency("abdominal_pain", 0.40, 0.10),
        ],
        discriminators=["age >= 50 change in bowel habit", "iron-deficiency anaemia",
                        "rectal bleeding + looser stools >6 weeks", "positive FIT"],
        red_flags=["ID anaemia any age", "palpable mass", "obstruction"],
        investigations=[
            InvestigationProfile("FIT (faecal immunochemical test)", "triage for 2ww",
                                 0.75, 0.95, "NICE NG12/DG30"),
            InvestigationProfile("FBC (iron-deficiency anaemia)", "2ww trigger",
                                 0.60, 0.90, "NICE NG12"),
        ],
        management_first_line="NG12: >=40 with unexplained weight loss + abdominal pain, or "
                              ">=50 unexplained rectal bleeding, or >=60 change in bowel "
                              "habit — FIT/2ww referral as applicable.",
        referral_tier="two_week_wait",
        safety_net="Persistent change in bowel habit or rectal bleeding must never be "
                   "dismissed as piles without review.",
        source="NICE NG12 suspected cancer",
    ),
    ConditionProfile(
        condition_id="hepatitis_viral",
        name="Acute viral hepatitis",
        category="gastrointestinal",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("jaundice", 0.60, 0.90),
            SymptomFrequency("fatigue", 0.80, 0.10),
            SymptomFrequency("dark_urine", 0.50, 0.70),
            SymptomFrequency("nausea", 0.50, 0.05),
            SymptomFrequency("fever", 0.30, 0.05),
        ],
        discriminators=["prodrome then jaundice", "risk factors (travel, IVDU, contacts, "
                        "sexual)", "high transaminases"],
        red_flags=["encephalopathy (acute liver failure)", "coagulopathy",
                   "drowsiness + jaundice = emergency"],
        investigations=[
            InvestigationProfile("LFTs + hepatitis serology", "diagnostic",
                                 0.95, 0.90, "PHE_hepatitis_guidance"),
            InvestigationProfile("INR/clotting", "liver failure screen",
                                 0.80, 0.80, "NICE_liver"),
        ],
        management_first_line="Acute hepatitis with jaundice: urgent LFTs/clotting; "
                              "any confusion or bleeding = emergency admission; notify PHE.",
        referral_tier="urgent",
        safety_net="Yellow eyes/skin, dark urine, drowsiness or bruising — urgent review.",
        source="UKHSA hepatitis guidance; NICE",
    ),

    # ================= NEUROLOGICAL =================
    ConditionProfile(
        condition_id="stroke_tia",
        name="Stroke / TIA",
        category="neurological",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("facial_droop", 0.60, 0.90),
            SymptomFrequency("arm_weakness", 0.65, 0.85),
            SymptomFrequency("speech_disturbance", 0.60, 0.85),
            SymptomFrequency("unilateral_weakness", 0.70, 0.80),
            SymptomFrequency("visual_disturbance", 0.20, 0.30),
            SymptomFrequency("dizziness", 0.15, 0.05),
        ],
        discriminators=["sudden onset FAST positive", "time last known well",
                        "face-arm-speech distribution"],
        red_flags=["any acute neurological deficit", "fluctuating deficit = TIA — same-day "
                   "specialist even if resolved"],
        investigations=[
            InvestigationProfile("non-contrast CT head", "haemorrhage vs ischaemia",
                                 0.95, 0.95, "NICE NG128"),
        ],
        management_first_line="Call 999 (stroke pathway, thrombolysis/thrombectomy windows); "
                              "resolved deficit = same-day TIA clinic, do not wait (NICE NG128).",
        referral_tier="emergency",
        safety_net="Any sudden face droop, arm weakness or speech problem — 999 "
                   "immediately, even if it recovers.",
        dangerous_mimic_of=["migraine", "hypoglycaemia_pending", "bell_palsy"],
        source="NICE NG128 stroke",
    ),
    ConditionProfile(
        condition_id="sah_subarachnoid",
        name="Subarachnoid haemorrhage",
        category="neurological",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("thunderclap_headache", 0.95, 0.95),
            SymptomFrequency("vomiting", 0.70, 0.30),
            SymptomFrequency("neck_stiffness", 0.30, 0.50),
            SymptomFrequency("headache", 0.98, 0.15),
            SymptomFrequency("photophobia", 0.25, 0.30),
            SymptomFrequency("loss_of_consciousness", 0.25, 0.50),
        ],
        discriminators=["worst-ever pain peaking <1 min", "exertional onset",
                        "sentinel headache"],
        red_flags=["thunderclap headache = emergency until excluded",
                   "neurological deficit", "seizure at onset"],
        investigations=[
            InvestigationProfile("non-contrast CT head <6 h", "excludes SAH",
                                 0.99, 0.99, "NICE CG150_headache"),
            InvestigationProfile("LP xanthochromin 6h-14d if CT negative", "detects SAH",
                                 0.93, 0.95, "NICE CG150"),
        ],
        management_first_line="Immediate ED via 999; CT within 1 h of presentation.",
        referral_tier="emergency",
        safety_net="A headache that reaches maximum intensity within a minute — even if it "
                   "settles — is an emergency.",
        dangerous_mimic_of=["migraine", "tension_headache"],
        source="NICE CG150 headache",
    ),
    ConditionProfile(
        condition_id="meningitis",
        name="Meningitis / meningococcal disease",
        category="neurological",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("fever", 0.90, 0.20),
            SymptomFrequency("headache", 0.90, 0.20),
            SymptomFrequency("neck_stiffness", 0.55, 0.70),
            SymptomFrequency("photophobia", 0.40, 0.50),
            SymptomFrequency("non_blanching_rash", 0.35, 0.95),
            SymptomFrequency("confusion", 0.35, 0.35),
        ],
        discriminators=["fever + headache + neck stiffness", "non-blanching rash",
                        "kernig sign", "close-contact setting"],
        red_flags=["non-blanching rash", "confusion/drowsiness", "seizures",
                   "shock signs — do not wait for rash"],
        investigations=[
            InvestigationProfile("blood culture + LP (if safe)", "diagnostic",
                                 0.80, 0.90, "NICE CG102"),
        ],
        management_first_line="Call 999; IM/IV benzylpenicillin in community if suspected "
                              "meningococcal disease while awaiting transfer (NICE CG102).",
        referral_tier="emergency",
        safety_net="Fever with severe headache, stiff neck, light hurting eyes, drowsiness "
                   "or any rash that doesn't fade under glass — 999.",
        dangerous_mimic_of=["migraine", "viral_urti"],
        source="NICE CG102 meningitis",
    ),
    ConditionProfile(
        condition_id="status_epilepticus",
        name="Status epilepticus",
        category="neurological",
        prevalence_per_consult=0.0003,
        symptoms=[
            # Stage 7 Task 7.1 re-anchoring: the bare "seizure" token at
            # 0.90 specificity made EVERY seizure presentation — including
            # a fully recovered first-ever fit — rank status as an
            # emergency-tier leader, and the validator correctly refused
            # to let it pass as routine/urgent. Status now scores only on
            # not-stopping / repeated-without-recovery wording; the
            # emergency SAFETY RULE keeps its own >=5-min regex, so real
            # status still short-circuits to 999.
            SymptomFrequency("seizure_not_stopping", 0.95, 0.95),
            SymptomFrequency("repeated_seizures_no_recovery", 0.90, 0.85),
            SymptomFrequency("confusion", 0.50, 0.15),
        ],
        discriminators=["convulsion >5 min or repeated without recovery"],
        red_flags=["any convulsion >5 min", "not waking between seizures",
                   "first-ever seizure"],
        investigations=[],
        management_first_line="Call 999; airway positioning; buccal midazolam per "
                              "protocol if trained and available; time the seizure.",
        referral_tier="emergency",
        safety_net="Any seizure lasting over 5 minutes, or repeated seizures without "
                   "waking — 999.",
        source="NICE epilepsy; ALS guidance",
    ),
    ConditionProfile(
        condition_id="migraine",
        name="Migraine",
        category="neurological",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("headache", 0.95, 0.10),
            SymptomFrequency("unilateral_headache", 0.60, 0.55),
            SymptomFrequency("photophobia", 0.60, 0.50),
            SymptomFrequency("nausea", 0.70, 0.10),
            SymptomFrequency("aura", 0.30, 0.75),
            SymptomFrequency("phonophobia", 0.55, 0.45),
        ],
        discriminators=["recurrent episodic pattern", "photophobia + nausea",
                        "aura", "menstrual association"],
        red_flags=["first severe headache >50 y", "thunderclap onset", "fever",
                   "neurological deficit persisting", "papilloedema"],
        investigations=[],
        management_first_line="Triptan + NSAID early in attack; prophylaxis if >= 4 "
                              "attacks/month; headache diary (NICE CG150 headache).",
        referral_tier="self_care",
        safety_net="Sudden 'worst ever' headache, fever, rash, drowsiness or new weakness "
                   "— emergency, not migraine.",
        source="NICE CG150 headache",
    ),
    ConditionProfile(
        condition_id="tension_headache",
        name="Tension-type headache",
        category="neurological",
        prevalence_per_consult=0.06,
        symptoms=[
            SymptomFrequency("headache", 0.95, 0.10),
            SymptomFrequency("bilateral_headache", 0.80, 0.40),
            SymptomFrequency("band_like_pressure", 0.60, 0.55),
        ],
        discriminators=["bilateral pressing, no photo/phonophobia, no nausea",
                        "stress/postural association", "normal neurology"],
        red_flags=["thunderclap onset", "fever", "new neurology", "morning vomiting",
                   "age >50 new headache (GCA risk)"],
        investigations=[],
        management_first_line="Simple analgesia limited to <10 days/month (MOH risk), "
                              "stress management, sleep hygiene, hydration.",
        referral_tier="self_care",
        safety_net="Headache with fever, drowsiness, rash, sudden worst-ever onset, or "
                   "new neurological symptoms — urgent.",
        source="NICE CG150 headache; ICHD-3",
    ),
    ConditionProfile(
        condition_id="bell_palsy",
        name="Bell's palsy (idiopathic facial weakness)",
        category="neurological",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("facial_weakness_eye_closure", 0.95, 0.85),
            SymptomFrequency("facial_droop", 0.90, 0.30),
            SymptomFrequency("altered_taste", 0.30, 0.50),
            SymptomFrequency("hyperacusis", 0.20, 0.60),
        ],
        discriminators=["forehead sparing = central cause (stroke) vs included in Bell's",
                        "gradual over 24-72 h", "post-auricular pain"],
        red_flags=["forehead-sparing weakness (stroke)", "bilateral weakness",
                   "rash/otitis signs (Ramsay Hunt)", "new severe headache with weakness"],
        investigations=[],
        management_first_line="Prednisolone 60 mg (or 25 mg x2) within 72 h of onset for "
                              " Grades IV-VI; eye protection if incomplete closure (NICE CKS).",
        referral_tier="routine",
        safety_net="Sudden weakness that spares the forehead, or weakness with arm or "
                   "speech problems, is a stroke — 999.",
        dangerous_mimic_of=["stroke_tia"],
        source="NICE CKS Bell's palsy",
    ),
    ConditionProfile(
        condition_id="gbs_guillain_barre",
        name="Guillain-Barré syndrome",
        category="neurological",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("ascending_weakness", 0.80, 0.95),
            SymptomFrequency("limb_weakness_symmetric", 0.90, 0.40),
            SymptomFrequency("back_pain", 0.30, 0.05),
            SymptomFrequency("breathlessness", 0.25, 0.10),
        ],
        discriminators=["progressive symmetric weakness after diarrhoeal/resp illness",
                        "areflexia", "ascending progression"],
        red_flags=["any breathlessness (respiratory failure)", "rapid progression",
                   "bulbar weakness"],
        investigations=[
            InvestigationProfile("vital capacity monitoring", "respiratory risk",
                                 0.80, 0.85, "GBS_consensus"),
        ],
        management_first_line="Suspected GBS = urgent admission for respiratory monitoring; "
                              "IVIG or plasmapheresis.",
        referral_tier="emergency",
        safety_net="Weakness moving up the body, or any breathing difficulty with "
                   "weakness — emergency.",
        dangerous_mimic_of=["viral_urti"],
        source="GBS international guidance",
    ),
    ConditionProfile(
        condition_id="cauda_equina",
        name="Cauda equina syndrome",
        category="neurological",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("back_pain", 0.90, 0.10),
            SymptomFrequency("bladder_dysfunction", 0.70, 0.90),
            SymptomFrequency("saddle_anaesthesia", 0.60, 0.95),
            SymptomFrequency("sciatica_leg_pain", 0.60, 0.20),
            SymptomFrequency("bilateral_leg_weakness", 0.40, 0.80),
        ],
        discriminators=["urinary retention/incontinence with back pain",
                        "saddle numbness", "decreased anal tone"],
        red_flags=["retention", "saddle anaesthesia", "bilateral sciatica",
                   "any red flag = emergency MRI within hours"],
        investigations=[
            InvestigationProfile("urgent MRI lumbosacral", "confirm compression",
                                 0.95, 0.95, "NICE NG59"),
        ],
        management_first_line="Emergency referral for MRI and surgical decompression; "
                              "window is hours, not days (NICE NG59).",
        referral_tier="emergency",
        safety_net="Back pain with loss of bladder control, numbness between the legs, or "
                   "weakness in both legs — emergency.",
        dangerous_mimic_of=["lumbago_nonspecific", "sciatica_prolapse_pending"],
        source="NICE NG59 low back pain",
    ),
    ConditionProfile(
        condition_id="encephalitis",
        name="Encephalitis",
        category="neurological",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("confusion", 0.80, 0.55),
            SymptomFrequency("fever", 0.75, 0.15),
            SymptomFrequency("headache", 0.70, 0.10),
            SymptomFrequency("seizure", 0.30, 0.40),
            SymptomFrequency("behaviour_change", 0.40, 0.50),
        ],
        discriminators=["fever + altered behaviour/confusion", "HSV prodrome",
                        "temporal lobe signs"],
        red_flags=["any fever with confusion = treat as encephalitis until excluded"],
        investigations=[
            InvestigationProfile("LP + PCR panel", "diagnostic",
                                 0.85, 0.95, "NICE CG102"),
        ],
        management_first_line="Emergency admission; empirical aciclovir early (do not wait "
                              "for LP results) + antibiotics covering meningitis.",
        referral_tier="emergency",
        safety_net="Fever with confusion, odd behaviour or seizures — 999.",
        dangerous_mimic_of=["viral_urti"],
        source="NICE CG102; BASM encephalitis",
    ),

    # ================= BENIGN COMMON ANCHORS =================
    ConditionProfile(
        condition_id="musculoskeletal_chest_pain",
        name="Musculoskeletal (chest wall) pain",
        category="musculoskeletal",
        prevalence_per_consult=0.02,
        symptoms=[
            SymptomFrequency("chest_pain", 0.95, 0.15),
            SymptomFrequency("chest_wall_tenderness", 0.70, 0.80),
            SymptomFrequency("pain_on_movement", 0.60, 0.70),
        ],
        discriminators=["reproducible on palpation/movement", "post-exertional/unaccustomed activity",
                        "sharp, well-localised"],
        red_flags=["NEVER diagnose chest wall pain before excluding cardiac features "
                   "when risk factors present"],
        investigations=[],
        management_first_line="Reassurance + NSAID/paracetamol topical or oral; explain "
                              "expected course 1-3 weeks.",
        referral_tier="self_care",
        safety_net="If pain occurs at rest, lasts >15 min, or comes with sweating/"
                   "breathlessness — treat as cardiac until proven otherwise.",
        source="NICE CG95 context",
    ),
    ConditionProfile(
        condition_id="anxiety_atacks",
        name="Panic attacks / anxiety-related symptoms",
        category="mental_health",
        prevalence_per_consult=0.03,
        symptoms=[
            SymptomFrequency("palpitations", 0.70, 0.25),
            SymptomFrequency("chest_pain", 0.40, 0.05),
            SymptomFrequency("breathlessness", 0.50, 0.05),
            SymptomFrequency("dizziness", 0.50, 0.10),
            SymptomFrequency("anxiety", 0.90, 0.70),
            SymptomFrequency("tingling_fingers", 0.35, 0.55),
        ],
        discriminators=["episodic peaking ~10 min with fear", "resolves fully",
                        "hyperventilation reproduces symptoms"],
        red_flags=["first episode age >40 without psychiatric history — exclude physical",
                   "exertional component — exclude cardiac"],
        investigations=[],
        management_first_line="Breathing retraining; explanation; CBT referral if recurrent; "
                              "screen depression; avoid benzodiazepines long-term (NICE CG113).",
        referral_tier="routine",
        safety_net="Chest pain with sweating, or fainting, or lasting >15 min is not a "
                   "panic attack until physical causes excluded.",
        source="NICE CG113 anxiety",
    ),
    ConditionProfile(
        condition_id="viral_urti",
        name="Viral upper respiratory tract infection",
        category="infection",
        prevalence_per_consult=0.30,
        symptoms=[
            SymptomFrequency("sore_throat", 0.70, 0.30),
            SymptomFrequency("cough", 0.65, 0.15),
            SymptomFrequency("rhinorrhoea", 0.80, 0.60),
            SymptomFrequency("fever", 0.40, 0.10),
            SymptomFrequency("myalgia", 0.40, 0.25),
            SymptomFrequency("fatigue", 0.60, 0.10),
        ],
        discriminators=["self-limiting <1-2 weeks", "coryzal prodrome", "no focal signs"],
        red_flags=["breathlessness at rest", "stridor", "one-sided chest pain",
                   "immunosuppression", "symptoms >3 weeks"],
        investigations=[],
        management_first_line="Rest, fluids, paracetamol/ibuprofen; no antibiotics; "
                              "safety-net for deterioration (NICE antimicrobial stewardship).",
        referral_tier="self_care",
        safety_net="Breathlessness at rest, confusion, no urine for 12 h, or one-sided "
                   "chest pain — urgent.",
        source="NICE antimicrobial stewardship; CKS",
    ),
    ConditionProfile(
        condition_id="gastroenteritis",
        name="Acute gastroenteritis",
        category="infection",
        prevalence_per_consult=0.05,
        symptoms=[
            SymptomFrequency("diarrhoea", 0.95, 0.55),
            SymptomFrequency("vomiting", 0.70, 0.15),
            SymptomFrequency("abdominal_pain_colicky", 0.50, 0.15),
            SymptomFrequency("fever", 0.30, 0.05),
        ],
        discriminators=["self-limiting 1-3 days", "contacts/dietary history",
                        "no blood in stool typically"],
        red_flags=["blood in stool", "no urine >12 h / drowsy (dehydration)",
                   "severe pain localising RIF", "return from abroad with fever"],
        investigations=[
            InvestigationProfile("stool culture if blood/prolonged/travel", "public health + diagnosis",
                                 0.60, 0.90, "PHE_GI_guidance"),
        ],
        management_first_line="Oral rehydration; no antimotility if fever/blood; food "
                              "hygiene; notify if suspected food-borne outbreak.",
        referral_tier="self_care",
        safety_net="No urinating for 12 h, drowsiness, blood in stool, or pain moving to "
                   "the right lower abdomen — urgent.",
        dangerous_mimic_of=[],
        source="PHE/UKHSA GI guidance; CKS",
    ),
    ConditionProfile(
        condition_id="lumbago_nonspecific",
        name="Non-specific low back pain",
        category="musculoskeletal",
        prevalence_per_consult=0.07,
        symptoms=[
            SymptomFrequency("back_pain", 1.00, 0.25),
            SymptomFrequency("pain_on_movement", 0.80, 0.30),
        ],
        discriminators=["mechanical pattern, no red flags", "improves in 6 weeks",
                        "worse with movement better rest (variable)"],
        red_flags=["cauda equina features", "fever/IVDU (epidural abscess)",
                   "cancer history + weight loss", "night pain unrelieved",
                   "significant trauma", "age >50 new-onset fragility"],
        investigations=[],
        management_first_line="Stay active + analgesia; no routine imaging; exercise "
                              "programme if persistent; review red flags every consultation "
                              "(NICE NG59).",
        referral_tier="self_care",
        safety_net="Loss of bladder/bowel control, numbness between legs, fever, or "
                   "weakness in both legs — emergency.",
        source="NICE NG59",
    ),
    ConditionProfile(
        condition_id="urinary_tract_infection_simple",
        name="Lower urinary tract infection (uncomplicated)",
        category="urology_kidney",
        prevalence_per_consult=0.04,
        symptoms=[
            SymptomFrequency("dysuria", 0.85, 0.65),
            SymptomFrequency("frequency_micturition", 0.80, 0.55),
            SymptomFrequency("urgency_micturition", 0.70, 0.50),
            SymptomFrequency("suprapubic_pain", 0.40, 0.45),
        ],
        discriminators=["dysuria + frequency without systemic features",
                        "urine dipstick nitrites/leucocytes in ambiguous cases"],
        red_flags=["fever/flank pain (pyelonephritis)", "confusion in older people",
                   "pregnancy", "male UTI", "catheter + systemic signs"],
        investigations=[
            InvestigationProfile("urine dipstick", "supports in ambiguous cases",
                                 0.75, 0.70, "NICE UTI_lower"),
        ],
        management_first_line="Nitrofurantoin 100 mg MR BD 3 days (women, eGFR ok); "
                              "trimethoprim where resistance low; safety-net; men/pregnant "
                              "need different pathway (NICE UTI guidance).",
        referral_tier="self_care",
        safety_net="Fever, back pain, vomiting, or confusion — the infection may have "
                   "reached the kidneys: urgent review.",
        dangerous_mimic_of=[],
        source="NICE lower UTI guidance (NG111 family); PHE",
    ),
]

# Symptom synonyms: canonical token -> lowercase match phrases.
SYMPTOM_SYNONYMS: Dict[str, List[str]] = {
    # cardiovascular / general
    "chest_pain": ["chest pain", "chest ache", "chest pressure", "chest tightness",
                   "tightness in chest", "pain in chest"],
    "pain_radiating_arm_jaw": ["radiating to arm", "radiates to arm", "into left arm",
                               "to the arm", "to jaw", "radiating to jaw", "into the jaw"],
    "sweating": ["sweating", "sweaty", "cold sweat", "clammy", "diaphoresis", "drenched"],
    "nausea": ["nausea", "nauseous", "feel sick", "feeling sick", "queasy"],
    "breathlessness": ["breathless", "short of breath", "shortness of breath",
                       "difficulty breathing", "can't breathe", "cant breathe",
                       "struggling to breathe", "dyspnoea", "dyspnea",
                       # 8.2 probe: "finding it hard to breathe, wheezy,
                       # inhalers not helping" extracted ZERO features and
                       # returned outside-scope — an acute asthma attack
                       # with no differential is a crack, not honesty
                       "hard to breathe", "hard to breath",
                       "finding it hard to breathe", "trouble breathing",
                       "trouble catching my breath", "winded"],
    "palpitations": ["palpitation", "racing heart", "heart pounding", "fluttering heart",
                     "fast heart"],
    "dizziness": ["dizzy", "dizziness", "light-headed", "lightheaded", "woozy"],
    "syncope": ["fainted", "collapse", "passed out", "blackout", "syncope",
                "blacked out"],
    "tearing_chest_back_pain": ["tearing", "ripping pain", "torn", "pain moving to back",
                                "through to the back"],
    "bp_differential_arms": ["different blood pressure", "bp different in each arm",
                             "blood pressure difference between arms"],
    "calf_swelling_pain": ["swollen calf", "calf pain", "calf swelling", "painful calf",
                           "red calf", "swollen leg", "one leg swollen"],
    "orthopnoea": ["breathless lying flat", "can't lie flat", "cant lie flat",
                   "worse lying down", "propped up on pillows", "waking gasping",
                   "paroxysmal nocturnal"],
    "ankle_swelling": ["ankle swelling", "swollen ankles", "swollen feet", "oedema", "edema",
                       # 7.3: patient word order
                       "ankles are swollen", "ankles swollen"],
    "fatigue": ["tired", "tiredness", "fatigue", "exhausted", "no energy", "worn out",
                "lethargic"],
    "fever": ["fever", "feverish", "temperature", "pyrexia", "hot and cold", "rigors",
              "rigor", "febrile"],
    "weight_loss": ["weight loss", "losing weight", "lost weight", "clothes loose"],
    "night_sweats": ["night sweats", "sweating at night", "drenched at night",
                     "waking sweaty"],
    "new_murmur": ["new murmur", "heart murmur"],
    "visual_disturbance": ["blurred vision", "vision blurred", "visual disturbance",
                           "double vision", "lost vision", "vision loss", "curtain over"],
    "pulsatile_abdominal_mass": ["pulsatile", "pulsating mass", "pulsing in the stomach"],
    "abdominal_back_flank_pain": ["abdominal and back pain", "belly pain to the back",
                                  "flank pain", "loin pain", "side pain to back"],
    # respiratory
    "cough": ["cough", "coughing"],
    "productive_cough": ["productive cough", "coughing up", "bringing up phlegm",
                         "sputum", "phlegm", "chesty cough"],
    "purulent_sputum": ["green phlegm", "yellow phlegm", "green sputum", "purulent",
                        "infected looking phlegm"],
    "wheeze": ["wheeze", "wheezing", "whistling chest", "wheez",
               "wheezy", "wheezing sound"],
    "chest_tightness": ["chest tightness", "tight chest"],
    # Stage 9: the stable-angina discriminators — bound phrasings only
    # ("on exertion" with chest/walk/climb context words where needed)
    "exertional_chest_pain": [
        "chest pain on exertion", "pain on exertion", "chest pain on walking",
        "chest pain walking", "when i walk uphill", "walking uphill",
        "climbing stairs", "climbing the stairs", "going uphill",
        "when i climb", "pain comes on when i walk", "chest pain on climbing"],
    "chest_pain_relieved_by_rest": [
        "relieved by rest", "eases with rest", "goes when i stop",
        "stops when i sit down", "settles with rest", "goes away with rest",
        "better once i stop", "relieved by gtn", "goes with gtn"],
    "haemoptysis": ["coughing up blood", "blood in phlegm", "blood-streaked sputum",
                    "haemoptysis", "hemoptysis"],
    "pleuritic_chest_pain": ["pleuritic", "sharp pain when breathing", "pain on breathing in",
                             "catches when i breathe", "stabbing chest pain"],
    "hoarseness": ["hoarse", "hoarseness", "voice change", "lost my voice",
                   "croaky voice"],
    "loss_of_taste_smell": ["loss of taste", "loss of smell", "can't taste", "can't smell",
                            "cant smell", "anosmia"],
    "sore_throat": ["sore throat", "throat pain", "painful throat", "pharyngitis"],
    "rhinorrhoea": ["runny nose", "blocked nose", "nasal congestion", "coryza", "cold-like",
                    "sneezing"],
    "myalgia": ["muscle ache", "aching muscles", "myalgia", "body aches", "aching all over"],
    # gastrointestinal
    "heartburn": ["heartburn", "acid reflux", "burning chest after food",
                  "reflux", "water brash", "burning upper abdominal pain",
                  "burning stomach after food", "burning in upper abdomen"],
    "acid_reflux_regurgitation": ["acid coming up", "regurgitation", "sour taste",
                                  "food repeating"],
    "dysphagia": ["dysphagia", "difficulty swallowing", "food sticking",
                  "trouble swallowing", "can't swallow"],
    "epigastric_pain": ["epigastric", "upper stomach pain", "pain at top of stomach",
                        "below the breastbone", "upper abdominal pain"],
    "coffee_ground_vomit": ["coffee ground", "coffee-ground", "vomiting blood",
                            "haematemesis", "hematemesis", "blood in vomit"],
    "melaena": ["black stool", "black tarry", "tarry stool", "melaena", "melena",
                "black poo", "black stool"],
    "haematemesis": ["vomiting blood", "blood in vomit", "haematemesis"],
    "abdominal_pain_rif": ["right lower abdomen", "right iliac", "right lower tummy",
                           "right side of my stomach", "right lower quadrant"],
    "anorexia": ["no appetite", "loss of appetite", "not eating", "anorexia"],
    "peritonism": ["guarding", "rebound tenderness", "rigid abdomen", "pain on touching",
                   "hurts to touch the stomach", "pain on movement of the belly"],
    "ruq_pain": ["right upper", "ruq", "under the right ribs", "right side under ribs"],
    "murphy_sign": ["murphy", "catches breath when pressed"],
    "severe_epigastric_pain_radiating_back": ["epigastric pain radiating to back",
                                              "upper abdominal pain to the back",
                                              "through to my back"],
    "abdominal_distension": ["distended", "swollen stomach", "swollen abdomen",
                             "bloating of the whole stomach"],
    "absolute_constipation": ["not passing wind", "no bowel movement", "haven't opened bowels",
                              "absolute constipation", "not opened my bowels"],
    "abdominal_pain_colicky": ["colicky", "cramping abdominal pain", "waves of pain",
                               "crampy stomach pain"],
    "left_lower_quadrant_pain": ["left lower", "left iliac", "left side of my stomach",
                                 "left lower tummy"],
    "altered_bowel_habit": ["change in bowel habit", "bowel habit changed",
                            "different bowel pattern", "constipation and diarrhoea"],
    "rectal_bleeding": ["rectal bleeding", "blood in stool", "blood when i wipe",
                        "bleeding from the back passage", "blood in my poo"],
    "bloating": ["bloating", "bloated", "wind"],
    "abdominal_pain_relieved_defecation": ["better after opening bowels",
                                           "relieved by going to the toilet",
                                           "eases after a bowel movement"],
    "diarrhoea": ["diarrhoea", "diarrhea", "loose stools", "watery stools", "the runs"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "tummy pain", "belly pain",
                       "stomach ache", "pain in my stomach"],
    "jaundice": ["jaundice", "yellow eyes", "yellow skin", "jaundiced",
                # 7.3: the patient-order phrasings
                "turned yellow", "gone yellow", "yellow all over"],
    "dark_urine": ["dark urine", "tea-coloured", "coke-coloured", "dark wee"],
    "vomiting": ["vomiting", "being sick", "threw up", "throwing up", "couldn't stop being sick"],
    "suprapubic_pain": ["suprapubic", "lower tummy pain", "bladder pain",
                        "pain above the pubic"],
    "dysuria": ["dysuria", "burning when i pass urine", "stinging urine",
                "painful urination", "burns when i pee", "stings when i urinate",
                "burning when passing urine", "burning when passing water",
                "burning pee", "stings when i pass urine",
                # 7.2: 'burning when I pass water' is the common UK phrasing
                "burning when i pass water", "stings when i pass water"],
    "frequency_micturition": ["passing urine frequently", "going to the toilet a lot",
                              "urinary frequency", "peeing constantly"],
    "urgency_micturition": ["urgency", "desperate to pass urine", "can't hold my urine",
                            "need to go suddenly"],
    # neurological
    "thunderclap_headache": ["thunderclap", "worst headache", "sudden severe headache",
                             "like a blow", "hit by", "came on instantly", "within a minute",
                             "explosive headache"],
    "headache": ["headache", "head pain", "migraine", "head hurts"],
    "unilateral_headache": ["one side of my head", "one-sided headache", "left side of my head",
                            "right side of my head"],
    "bilateral_headache": ["both sides of my head", "bilateral headache", "all over my head",
                           "band around", "both temples"],
    "band_like_pressure": ["like a band", "band-like", "band like",
                           "tight band", "band around my head",
                           "pressure around my head", "tightness around head",
                           "vice-like"],
    "photophobia": ["photophobia", "light hurts", "sensitive to light", "light makes it worse"],
    "phonophobia": ["phonophobia", "sensitive to sound", "noise makes it worse"],
    "aura": ["aura", "flashing lights", "zigzag", "visual warning before"],
    "neck_stiffness": ["neck stiffness", "stiff neck", "can't touch chin to chest",
                       "neck rigidity"],
    "non_blanching_rash": ["non-blanching", "nonblanching", "doesn't fade when pressed",
                           "does not fade", "doesn't disappear when pressed",
                           "rash that doesn't fade", "petechiae", "purpura"],
    "seizure": ["seizure", "fit", "convulsion", "epileptic"],
    "facial_droop": ["face drooping", "facial droop", "face droop", "drooping face",
                     "face is drooping", "mouth drooping", "eye drooping"],
    "arm_weakness": ["arm weakness", "weak arm", "arm is weak", "can't lift arm",
                     "arm drift"],
    "unilateral_weakness": ["weakness on one side", "one-sided weakness", "left side weak",
                            "right side weak", "weak down one side"],
    "speech_disturbance": ["slurred speech", "speech is slurred", "can't speak properly",
                           "words jumbled", "trouble speaking", "speech difficulty"],
    "facial_weakness_eye_closure": ["can't close my eye", "eye won't close", "eye won't shut",
                                    "cannot close eye", "one side of my face won't move",
                                    "face won't move on one side", "cannot shut eye"],
    "altered_taste": ["altered taste", "taste is different", "things taste odd"],
    "hyperacusis": ["sounds are louder", "noise is distorted", "hyperacusis"],
    "ascending_weakness": ["ascending weakness", "weakness moving up", "started in my legs "
                           "now my arms", "legs then arms", "moving up my body"],
    "limb_weakness_symmetric": ["both legs weak", "weakness in both", "symmetric weakness"],
    "back_pain": ["back pain", "backache", "my back hurts", "lower back pain"],
    "bladder_dysfunction": ["can't control my bladder", "can't pass urine", "retention",
                            "incontinent", "wet myself without knowing", "cannot control bladder",
                            "loss of bladder control"],
    "saddle_anaesthesia": ["saddle", "numb between my legs", "numbness around the bottom",
                           "numb groin", "numbness between legs"],
    "sciatica_leg_pain": ["sciatica", "pain down my leg", "shooting pain down leg",
                          "leg pain from back"],
    "bilateral_leg_weakness": ["both legs are weak", "legs giving way", "weak in both legs"],
    "confusion": ["confused", "confusion", "muddled", "not making sense", "disoriented",
                  "didn't know where she was", "didn't know where he was"],
    "drowsiness": ["drowsy", "sleepy", "hard to wake", "unrousable", "unresponsive"],
    "behaviour_change": ["behaviour change", "acting strangely", "personality change",
                         "not themselves", "odd behaviour"],
    # NB 'blacked out' moved to the syncope token (Stage 7 Task 7.1):
    # it is syncope language ("blacked out when I stood up"), and as a
    # loss_of_consciousness phrase it let the emergency-tier TBI entry
    # lead rank-1 on one generic token, flooring every simple faint to
    # emergency. TBI keeps the trauma-phrased LOC synonyms.
    "loss_of_consciousness": ["lost consciousness", "unconscious",
                               "knocked out", "knocked unconscious", "out cold"],
    "anxiety": ["anxious", "anxiety", "panic", "worried", "on edge", "dread"],
    "tingling_fingers": ["tingling fingers", "pins and needles in hands", "numb fingers",
                         "paresthesia hands"],
    "chest_wall_tenderness": ["tender chest", "chest wall tender", "hurts to press",
                              "sore to touch chest", "tender rib"],
    "pain_on_movement": ["pain on movement", "worse when i move", "hurts to move",
                         "worse on twisting", "worse with movement"],
    "flank_pain": ["flank pain", "loin pain", "pain in my side", "kidney pain"],
    "constipation": ["constipated", "constipation", "can't open bowels", "hard stools"],
}


def find_condition(condition_id: str) -> Optional[ConditionProfile]:
    for c in CONDITIONS:
        if c.condition_id == condition_id:
            return c
    return None


def conditions_for_symptom(token: str) -> List[ConditionProfile]:
    return [c for c in CONDITIONS if any(s.symptom == token for s in c.symptoms)]


# ---- Stage 1 Task 2: systematic breadth corpus, merged in at import time ----
from gpdisc_core.clinical_reasoning.knowledge_breadth import (  # noqa: E402
    CONDITIONS_PART2,
    SYMPTOM_SYNONYMS_PART2,
)

CONDITIONS.extend(CONDITIONS_PART2)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART2)

# ---- Stage 2 Task 1: tropical/ENT-oral/sexual-health corpus ----
from gpdisc_core.clinical_reasoning.knowledge_tropical import (  # noqa: E402
    CONDITIONS_PART3,
    SYMPTOM_SYNONYMS_PART3,
)

CONDITIONS.extend(CONDITIONS_PART3)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART3)

# ---- Stage 6 Task 6.3: trauma & burns (the emergencies corpus) ----
from gpdisc_core.clinical_reasoning.knowledge_emergencies import (  # noqa: E402
    CONDITIONS_PART4,
    SYMPTOM_SYNONYMS_PART4,
)

CONDITIONS.extend(CONDITIONS_PART4)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART4)

# ---- Stage 7 Task 7.1: chronic neurology + mental health ----
from gpdisc_core.clinical_reasoning.knowledge_breadth2 import (  # noqa: E402
    CONDITIONS_PART5,
    SYMPTOM_SYNONYMS_PART5,
)

CONDITIONS.extend(CONDITIONS_PART5)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART5)

# ---- Stage 8 Task 8.1: the world — global burden + environmental ----
from gpdisc_core.clinical_reasoning.knowledge_global import (  # noqa: E402
    CONDITIONS_PART6,
    SYMPTOM_SYNONYMS_PART6,
)

CONDITIONS.extend(CONDITIONS_PART6)
SYMPTOM_SYNONYMS.update(SYMPTOM_SYNONYMS_PART6)
