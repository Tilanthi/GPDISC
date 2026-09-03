"""Stage 7 (Tier 2): daily-breadth corpus part 5 — chronic neurology and
mental health.

Task 7.1 closes the gaps the pre-implementation probes exposed: dementia,
Parkinson's, MS, cluster headache and peripheral neuropathy were absent
entirely (empty or absurd differentials — the Parkinson's probe once led
with alcohol-withdrawal delirium); a first-ever seizure that had fully
recovered was over-triaged to emergency because the corpus entry for
status epilepticus scored on the bare word "seizure"; mania returned an
empty differential.

That over-triage fix lives HERE in spirit: knowledge.py's
status_epilepticus now scores only on not-stopping / repeated-without-
recovery tokens (defined in SYMPTOM_SYNONYMS_PART5), while the separate
SAFETY-RULE regex keeps its ">=5 min / not waking" wording. A recovered
first seizure is same-day-urgent, not 999.
"""
from typing import Dict, List

from gpdisc_core.clinical_reasoning.schema import (
    ConditionProfile,
    InvestigationProfile,
    SymptomFrequency,
)

CONDITIONS_PART5: List[ConditionProfile] = [
    # ================= CHRONIC NEUROLOGY =================
    ConditionProfile(
        condition_id="dementia_suspected",
        name="Suspected dementia (incl. Alzheimer/vascular/Lewy-body)",
        category="neurological",
        prevalence_per_consult=0.010,
        symptoms=[
            SymptomFrequency("progressive_forgetfulness", 0.90, 0.80),
            SymptomFrequency("unsafe_forgetting_events", 0.55, 0.95),
            SymptomFrequency("gradual_decline_over_months", 0.60, 0.55),
            SymptomFrequency("disorientation_time_place", 0.30, 0.85),
            SymptomFrequency("functional_decline_iadl", 0.50, 0.75),
            SymptomFrequency("personality_change", 0.25, 0.45),
        ],
        discriminators=[
            "Alzheimer: insidious, recent-memory first, anosmia early",
            "vascular: stepwise declines, stroke risk factors, past TIAs",
            "Lewy-body: visual hallucinations, fluctuating alertness, "
            "Parkinsonism, severe antipsychotic sensitivity",
            "normal-pressure hydrocephalus: gait change + incontinence + "
            "cognitive decline",
            "ALWAYS screen the reversible/imitators first: depression, "
            "hypothyroidism, B12/folate deficiency, delirium (rapid "
            "onset over days-weeks is delirium until proven otherwise), "
            "anticholinergic/opioid/sedative drug load, alcohol",
        ],
        red_flags=["rapid progression over days-weeks = delirium, "
                   "same-day assessment",
                   "new gait change with incontinence (NPH) or falls early "
                   "(atypical parkinsonism)",
                   "sudden focal onset (vascular event)",
                   "onset under 60 needs thorough early-onset workup",
                   "safety-critical forgetting: cooker, wandering, driving"],
        investigations=[
            InvestigationProfile("Reversible-cause bloods (FBC, U&E, LFT, "
                                 "TFT, calcium, glucose, CRP, B12/folate)",
                                 "excludes the treatable mimics before any "
                                 "dementia label", 0.90, 0.40,
                                 "NICE NG97 dementia"),
            InvestigationProfile("Structured cognitive test (MoCA / "
                                 "mini-Cog / 6-CIT)", "quantifies the "
                                 "deficit and tracks progression", 0.85,
                                 0.80, "NICE NG97"),
            InvestigationProfile("CT head (or MRI)", "excludes structural "
                                 "cause; not to diagnose dementia itself",
                                 0.70, 0.60, "NICE NG97"),
        ],
        management_first_line="Take a collateral history; review the drug "
                              "list (anticholinergics, opioids, "
                              "benzodiazepines); assess home safety "
                              "(cooker, driving, medication handling); "
                              "refer to a memory assessment service — do "
                              "not label dementia in one consultation.",
        referral_tier="routine",
        safety_net="Sudden confusion, drowsiness, rapid worsening or not "
                   "managing fluids needs same-day assessment — that is "
                   "delirium, not dementia, until proven otherwise.",
        dangerous_mimic_of=["depression_moderate", "hypothyroidism"],
        source="NICE NG97 dementia; CKS memory impairment",
    ),
    ConditionProfile(
        condition_id="first_seizure_adult",
        name="First-ever seizure (adult, recovered)",
        category="neurological",
        prevalence_per_consult=0.0008,
        symptoms=[
            SymptomFrequency("first_ever_seizure", 0.90, 0.92),
            SymptomFrequency("seizure", 1.00, 0.45),
            SymptomFrequency("recovered_after_seizure", 0.70, 0.30),
            SymptomFrequency("tongue_bitten", 0.20, 0.80),
            SymptomFrequency("seizure_incontinence", 0.15, 0.75),
        ],
        discriminators=["witness account and video beat every test — "
                        "was there convulsion, cyanosis, postictal "
                        "confusion, tongue-biting, incontinence?",
                        "vasovagal syncope: prodromal nausea/greying on "
                        "standing, brief, back to normal within a minute",
                        "cardiac syncope: no warning or exertional, "
                        "palpitations, family sudden-death history",
                        "hypoglycaemia: sweating, hunger, diabetic on "
                        "insulin/sulfonylurea",
                        "alcohol withdrawal, head injury, fever, "
                        "pregnancy (eclampsia) all change the pathway"],
        red_flags=["seizure >5 min or repeated without recovery — 999 "
                   "(status epilepticus)",
                   "not back to normal, or persisting confusion/focal "
                   "deficit",
                   "head injury before or after the seizure",
                   "fever, neck stiffness or rash",
                   "pregnant or within 6 weeks of birth"],
        investigations=[
            InvestigationProfile("Same-day assessment with bloods "
                                 "(glucose, U&E, calcium, FBC) and ECG",
                                 "first seizure is same-day medicine; "
                                 "ECG catches the cardiac syncope mimic",
                                 0.60, 0.50, "NICE CG137 / CKS epilepsy"),
        ],
        management_first_line="Same-day medical assessment (ED or "
                              "first-fit clinic per local pathway); stop "
                              "driving and inform DVLA — an isolated "
                              "first seizure usually means 6 months off; "
                              "do not start antiepileptics in general "
                              "practice.",
        referral_tier="urgent",
        safety_net="Seizure lasting more than 5 minutes, repeated "
                   "seizures, or not waking properly — 999.",
        dangerous_mimic_of=["cardiac_syncope", "hypoglycaemia"],
        source="NICE CG137 epilepsy; DVLA at-a-glance; CKS",
    ),
    ConditionProfile(
        condition_id="epilepsy_established",
        name="Known epilepsy — breakthrough seizure",
        category="neurological",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("known_epilepsy", 0.95, 0.95),
            SymptomFrequency("seizure", 0.90, 0.45),
            SymptomFrequency("breakthrough_pattern", 0.50, 0.70),
        ],
        discriminators=["missed doses is the commonest cause — ask "
                        "before adjusting anything",
                        "new interacting drug (enzyme inducers, some "
                        "antibiotics), alcohol, sleep deprivation, fever, "
                        "hyponatraemia",
                        "check the antiepileptic level before any dose "
                        "change",
                        "contraception failure both ways: enzyme "
                        "inducers reduce pill efficacy and some "
                        "epileptics harm the fetus"],
        red_flags=["status epilepticus or clustering (several in a day)",
                   "injury or aspiration during the seizure",
                   "not returning to baseline",
                   "seizures accelerating in frequency"],
        investigations=[
            InvestigationProfile("Antiepileptic drug level + U&E, "
                                 "glucose, LFT, FBC", "adherence and "
                                 "metabolic causes before dose changes",
                                 0.70, 0.60, "NICE CG137"),
        ],
        management_first_line="Urgent review (days, not months): "
                              "adherence history, drug level, trigger "
                              "screen; driving — a breakthrough seizure "
                              "restarts the off-driving clock; never stop "
                              "or change antiepileptics abruptly.",
        referral_tier="urgent",
        safety_net="More seizures than usual in one day, a seizure "
                   "lasting over 5 minutes, or not waking between "
                   "seizures — 999.",
        source="NICE CG137 epilepsy; DVLA guidance",
    ),
    ConditionProfile(
        condition_id="parkinsons_disease",
        name="Suspected Parkinson's disease",
        category="neurological",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("tremor_one_side", 0.70, 0.70),
            SymptomFrequency("smaller_handwriting", 0.40, 0.90),
            SymptomFrequency("slowed_walking", 0.60, 0.60),
            SymptomFrequency("limb_stiffness", 0.55, 0.35),
            SymptomFrequency("reduced_arm_swing", 0.30, 0.85),
            SymptomFrequency("reduced_smell", 0.25, 0.55),
        ],
        discriminators=["Parkinson's: asymmetric rest tremor, bradykinesia "
                        "(smaller handwriting, slower walking), rigidity; "
                        "response to levodopa",
                        "essential tremor: postural/action, family "
                        "history, improves with alcohol, no slowness",
                        "drug-induced parkinsonism: metoclopramide, "
                        "prochlorperazine, antipsychotics — symmetric and "
                        "reversible",
                        "atypical parkinsonism (MSA/PSP): early falls, "
                        "early autonomic failure, vertical gaze palsy"],
        red_flags=["falls or freezing within the first year",
                   "rapid bilateral onset",
                   "no response to adequate levodopa",
                   "early dementia, hallucinations or autonomic failure",
                   "current or recent dopamine-blocking drug"],
        investigations=[
            InvestigationProfile("Specialist diagnosis (Queen Square "
                                 "Brain Bank criteria) with levodopa "
                                 "challenge where needed", "PD is a "
                                 "specialist diagnosis — do not start "
                                 "treatment on suspicion alone", 0.90,
                                 0.85, "NICE NG71 Parkinson's disease"),
        ],
        management_first_line="Refer (non-urgent, but not delayed) to a "
                              "Parkinson's specialist; review and stop "
                              "any dopamine-blocking drug; physiotherapy, "
                              "exercise, and a medication review; watch "
                              "for impulse-control behaviours once "
                              "dopamine agonists start.",
        referral_tier="routine",
        safety_net="Falls, swallowing problems, hallucinations or "
                   "confusion need earlier specialist review — phone the "
                   "Parkinson's team rather than waiting for the clinic "
                   "letter.",
        source="NICE NG71 Parkinson's disease",
    ),
    ConditionProfile(
        condition_id="cluster_headache",
        name="Cluster headache",
        category="neurological",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("severe_unilateral_orbital_pain", 0.95, 0.55),
            SymptomFrequency("attacks_same_time_daily", 0.70, 0.92),
            SymptomFrequency("autonomic_eye_watering", 0.75, 0.88),
            SymptomFrequency("restlessness_during_attack", 0.40, 0.60),
            SymptomFrequency("short_attack_duration", 0.50, 0.50),
        ],
        discriminators=["cluster: excruciating unilateral orbital pain "
                        "15-180 minutes, same time daily (classically "
                        "1-2 hours into sleep), ipsilateral watering/red "
                        "eye, ptosis; patient paces rather than lies still",
                        "migraine: 4-72 hours, nausea/photophobia, "
                        "patient lies still in the dark",
                        "first-ever thunderclap onset is SAH until "
                        "proven otherwise regardless of the pattern",
                        "new headache over 50 with scalp tenderness or "
                        "jaw claudication is giant cell arteritis"],
        red_flags=["first attack was a thunderclap (SAH)",
                   "new headache over 50 (GCA)",
                   "any persisting neurological deficit or papilloedema",
                   "attacks losing the autonomic signature or changing "
                   "character"],
        investigations=[
            InvestigationProfile("Clinical diagnosis (ICHD-3 criteria); "
                                 "neurology referral", "no scan needed if "
                                 "the pattern is textbook, but atypical "
                                 "features warrant imaging", 0.95, 0.85,
                                 "NICE CKS cluster headache; ICHD-3"),
        ],
        management_first_line="Acute: 100% oxygen 12-15 L/min via "
                              "non-rebreather and/or subcutaneous "
                              "sumatriptan (NOT oral — too slow). "
                              "Prevention: verapamil under specialist "
                              "supervision with ECG monitoring. Alcohol "
                              "triggers attacks during a bout.",
        referral_tier="routine",
        safety_net="A first-ever sudden severe headache, weakness, "
                   "double vision or drowsiness — emergency, not a "
                   "cluster.",
        dangerous_mimic_of=["migraine", "tension_headache"],
        source="NICE CKS cluster headache; ICHD-3; SIGN",
    ),
    ConditionProfile(
        condition_id="multiple_sclerosis_suspect",
        name="Suspected multiple sclerosis (relapsing course)",
        category="neurological",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("episodic_neurological_symptoms", 0.85, 0.80),
            SymptomFrequency("unilateral_blurred_vision_history", 0.40, 0.70),
            SymptomFrequency("bilateral_foot_numbness", 0.50, 0.55),
            SymptomFrequency("fatigue", 0.50, 0.15),
            SymptomFrequency("heat_sensitivity", 0.20, 0.70),
        ],
        discriminators=["dissemination in time AND space: separate "
                        "episodes affecting separate sites (optic, cord, "
                        "brainstem, sensory)",
                        "optic neuritis: painful eye movement, unilateral "
                        "blur, washed-out colours",
                        "transverse myelitis: bilateral leg numbness "
                        "ascending over days with a sensory level",
                        "Lhermitte's (electric shock down the spine on "
                        "neck flexion)",
                        "functional/vascular/anatomical mimics are "
                        "commoner — refer rather than diagnose"],
        red_flags=["bladder or bowel involvement, or progressive leg "
                   "weakness climbing upward — possible cord lesion, "
                   "urgent same-day",
                   "bilateral simultaneous visual loss",
                   "persistent progressive deficit without remission"],
        investigations=[
            InvestigationProfile("Urgent neurology referral; MRI brain "
                                 "and cord with contrast", "dissemination "
                                 "in space/time; excludes cord "
                                 "compression mimics", 0.95, 0.85,
                                 "NICE CG186 multiple sclerosis"),
        ],
        management_first_line="Do not diagnose MS in general practice — "
                              "refer to a neurologist with the timeline "
                              "written down (dates, sites, durations). "
                              "Acute relapses with function-threatening "
                              "deficit are treated in secondary care.",
        referral_tier="routine",
        safety_net="Numbness spreading up the body, new weakness, or loss "
                   "of bladder control — same-day emergency assessment, "
                   "not a routine referral.",
        source="NICE CG186 multiple sclerosis",
    ),
    ConditionProfile(
        condition_id="peripheral_neuropathy",
        name="Peripheral neuropathy (distal symmetric)",
        category="neurological",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("burning_feet", 0.70, 0.85),
            SymptomFrequency("tingling_both_feet", 0.85, 0.60),
            SymptomFrequency("worse_at_night", 0.60, 0.35),
            SymptomFrequency("long_standing_diabetes", 0.50, 0.60),
        ],
        discriminators=["length-dependent (longest fibres first): both "
                        "feet, ascending; hands only later",
                        "diabetes is the commonest cause — but check B12, "
                        "thyroid, alcohol units, and HIV in risk groups",
                        "drug causes: metronidazole, isoniazid, "
                        "chemotherapy, statins (rare)",
                        "Guillain-Barré is the mimic that kills: ASCENDING "
                        "WEAKNESS over days (not months), post-infectious"],
        red_flags=["weakness developing or falls — ascending weakness "
                   "over days is Guillain-Barré, emergency",
                   "bladder/bowel change or a sensory level (cord)",
                   "rapid progression or asymmetric onset",
                   "any foot ulcer or numb undetected injury (charcot "
                   "risk)"],
        investigations=[
            InvestigationProfile("Bloods: HbA1c/glucose, B12, folate, "
                                 "TFT, U&E, LFT, ESR, protein "
                                 "electrophoresis, HIV where indicated",
                                 "find the cause — the list is treatable",
                                 0.75, 0.55, "NICE CKS peripheral "
                                 "neuropathy"),
        ],
        management_first_line="Optimise diabetes control; foot-care "
                              "education and podiatry referral (numb feet "
                              "ulcer silently); neuropathic pain "
                              "treatment ladder (duloxetine or "
                              "amitriptyline first in the UK, then "
                              "pregabalin); keep the drug list short in "
                              "older patients.",
        referral_tier="routine",
        safety_net="Legs getting weaker over days, trouble walking, or "
                   "loss of bladder control — emergency same-day "
                   "assessment.",
        dangerous_mimic_of=["hypothyroidism"],
        source="NICE CG173 neuropathic pain; CKS peripheral neuropathy",
    ),
    # ================= MENTAL HEALTH =================
    ConditionProfile(
        condition_id="bipolar_mania",
        name="Manic / hypomanic episode",
        category="mental_health",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("decreased_need_for_sleep", 0.85, 0.85),
            SymptomFrequency("pressured_speech", 0.60, 0.80),
            SymptomFrequency("grandiosity", 0.55, 0.90),
            SymptomFrequency("reckless_spending", 0.55, 0.85),
            SymptomFrequency("elevated_energy", 0.60, 0.40),
        ],
        discriminators=["mania is ELEVATED or IRRITABLE mood plus "
                        "increased energy — not just insomnia",
                        "the family usually knows before the patient: "
                        "collateral history is the test",
                        "screen the secondary causes: steroids, "
                        "antidepressants (a switch), thyrotoxicosis, "
                        "substances, sleep deprivation",
                        "postpartum onset is a red flag (postpartum "
                        "psychosis risk)"],
        red_flags=["psychotic symptoms — delusions, hallucinations, "
                   "paranoia",
                   "exhaustion, not eating or drinking",
                   "onset within weeks of birth",
                   "aggressive or threatening behaviour; risk to "
                   "children or dependants",
                   "spending that will cause real financial harm"],
        investigations=[
            InvestigationProfile("Mental-state examination plus TFT, "
                                 "U&E, LFT, glucose and drug screen",
                                 "excludes physical mimics before "
                                 "committing to a psychiatric diagnosis",
                                 0.60, 0.55, "NICE CG185 bipolar"),
        ],
        management_first_line="Urgent mental-health assessment (same "
                              "week; same-day if psychotic, exhausted or "
                              "with children at risk). Stop any "
                              "antidepressant. Protect finances (spending "
                              "blocks, card limits with the family). "
                              "Never diagnose bipolar in one consultation "
                              "— but never send mania away routinely.",
        referral_tier="urgent",
        safety_net="Voices, delusions, not drinking, or behaviour "
                   "threatening self or others — same-day crisis "
                   "assessment.",
        dangerous_mimic_of=["anxiety_generalised", "depression_moderate"],
        source="NICE CG185 bipolar disorder",
    ),
    ConditionProfile(
        condition_id="ocd",
        name="Obsessive-compulsive disorder",
        category="mental_health",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("compulsive_checking", 0.60, 0.85),
            SymptomFrequency("repetitive_washing", 0.60, 0.88),
            SymptomFrequency("recognised_irrational", 0.70, 0.75),
            SymptomFrequency("intrusive_obsessive_thoughts", 0.60, 0.60),
        ],
        discriminators=["obsessions are intrusive and ego-dystonic — the "
                        "patient knows it is irrational and that "
                        "distinction separates OCD from psychosis",
                        "compulsions neutralise anxiety short-term and "
                        "grow long-term",
                        "count hours lost per day, not symptoms counted",
                        "depression, tic disorders and psychosis "
                        "commonly co-travel — screen for each"],
        red_flags=["function paralysed by rituals (cannot leave the "
                   "house)",
                   "suicidal thoughts",
                   "food or fluid refusal",
                   "child or perinatal onset (higher-risk groups)"],
        investigations=[
            InvestigationProfile("Y-BOCS severity scale", "severity "
                                 "decides the treatment step", 0.90,
                                 0.85, "NICE CG31/CG113"),
        ],
        management_first_line="Step 1: guided CBT with exposure and "
                              "response prevention (ERP) — the treatment "
                              "with the strongest evidence. Step 2: "
                              "high-dose SSRI (e.g. sertraline to "
                              "maximum tolerated). Never reassure away "
                              "an obsession — it feeds it.",
        referral_tier="routine",
        safety_net="If rituals stop you eating, leaving the house, or "
                   "make you feel life is not worth living — come back "
                   "the same day.",
        source="NICE CG31/CG113 obsessive-compulsive disorder",
    ),
    ConditionProfile(
        condition_id="ptsd",
        name="Post-traumatic stress disorder",
        category="mental_health",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("trauma_exposure_reference", 0.95, 0.60),
            SymptomFrequency("flashbacks", 0.75, 0.90),
            SymptomFrequency("trauma_nightmares", 0.60, 0.75),
            SymptomFrequency("hypervigilance", 0.65, 0.70),
            SymptomFrequency("avoidance_trauma_cues", 0.60, 0.70),
        ],
        discriminators=["within 4 weeks of the trauma: acute stress "
                        "reaction — watchful waiting first",
                        "beyond 4 weeks with re-experiencing + avoidance "
                        "+ hyperarousal = PTSD",
                        "dissociative flashbacks (reliving, not "
                        "remembering) are the signature",
                        "screen for depression, alcohol misuse and "
                        "traumatic brain injury which mask and mimic",
                        "moral injury and childhood trauma behave "
                        "differently — complex PTSD"],
        red_flags=["suicidal thoughts or plans",
                   "alcohol or drug use escalating to cope",
                   "dissociative episodes (losing time, acting as if "
                   "back in the trauma)",
                   "violence or risk to others"],
        investigations=[],
        management_first_line="If under 4 weeks: active monitoring. If "
                              "PTSD established: trauma-focused "
                              "psychological therapy (trauma-focused CBT "
                              "or EMDR) — not medication first. Defer "
                              "single-session debriefing; it does not "
                              "help. Screen and treat the alcohol "
                              "before it entrenches.",
        referral_tier="routine",
        safety_net="Thoughts of ending your life, or drinking to block "
                   "it out — come back the same day; the crisis line is "
                   "open round the clock.",
        dangerous_mimic_of=["depression_moderate", "anxiety_generalised"],
        source="NICE CG26 PTSD",
    ),
    ConditionProfile(
        condition_id="eupd",
        name="Emotionally unstable personality disorder",
        category="mental_health",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("rapid_mood_swings_hours", 0.70, 0.80),
            SymptomFrequency("abandonment_fear", 0.55, 0.85),
            SymptomFrequency("identity_instability", 0.40, 0.80),
            SymptomFrequency("intense_inappropriate_anger", 0.55, 0.70),
            SymptomFrequency("chronic_emptiness", 0.50, 0.55),
            SymptomFrequency("self_harm_history_token", 0.50, 0.60),
        ],
        discriminators=["the pattern is YEARS long and pervasive, not "
                        "episodes — mood flips within hours, relationships "
                        "that alternate idealisation and rupture",
                        "bipolar mood episodes last days-weeks with "
                        "increased energy — EUPD mood shifts last hours "
                        "and are reactive",
                        "complex trauma history is the rule, not the "
                        "exception — ask once, gently",
                        "always assess current risk separately from the "
                        "label"],
        red_flags=["current suicidal intent or plan — same-day crisis "
                   "pathway regardless of diagnosis",
                   "escalating self-harm or new overdoses",
                   "risk to others",
                   "comorbid alcohol/drug dependence"],
        investigations=[],
        management_first_line="Consistency over novelty: one care "
                              "coordinator, planned reviews shorter and "
                              "more frequent. Psychological treatment "
                              "(DBT/MBT) is the evidence base — avoid "
                              "polypharmacy; never prescribe benzos or "
                              "antipsychotics for the personality itself.",
        referral_tier="routine",
        safety_net="Any thought of ending your life, or a plan — "
                   "same-day crisis assessment. An overdose is a "
                   "medical emergency first, a psychological signal "
                   "second.",
        source="NICE CG78 borderline personality disorder",
    ),
    ConditionProfile(
        condition_id="bulimia_nervosa",
        name="Bulimia nervosa",
        category="mental_health",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("self_induced_vomiting", 0.90, 0.90),
            SymptomFrequency("binge_eating_episodes", 0.75, 0.75),
            SymptomFrequency("fear_of_weight_gain", 0.60, 0.55),
            SymptomFrequency("compensatory_behaviours", 0.40, 0.70),
        ],
        discriminators=["binge–purge cycles with weight often NORMAL — "
                        "normal BMI does not exclude it",
                        "physical signs: Russell's sign (knuckle "
                        "calluses), dental erosion, parotid swelling",
                        "anorexia is the weight-based differential — "
                        "plot BMI and the trend",
                        "binge eating disorder purges nothing; OSFED "
                        "catches the rest"],
        red_flags=["fainting, palpitations or muscle weakness — "
                   "hypokalaemia until proven otherwise, same-day ECG "
                   "and U&E",
                   "blood in vomit (Mallory-Weiss/oesophageal tear)",
                   "vomiting multiple times daily",
                   "pregnancy or diabetes (destabilise fast)",
                   "BMI falling or suicidal thoughts"],
        investigations=[
            InvestigationProfile("U&E (potassium) + ECG when purging is "
                                 "frequent", "the killer is hypokalaemia",
                                 0.80, 0.70, "NICE NG69 eating disorders"),
        ],
        management_first_line="Guided self-help and CBT-ED first line; "
                              "fluoxetine 60 mg is the one licensed drug. "
                              "Non-judgemental weighing over time beats "
                              "reassurance; dental protection (don't "
                              "brush after vomiting — rinse and wait).",
        referral_tier="routine",
        safety_net="Fainting, palpitations, weakness, or blood in the "
                   "vomit — same-day assessment and bloods.",
        source="NICE NG69 eating disorders",
    ),
    ConditionProfile(
        condition_id="perinatal_mental_health",
        name="Perinatal mental illness (depression / anxiety / risk of "
             "psychosis)",
        category="mental_health",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("postnatal_period_marker", 0.95, 0.80),
            SymptomFrequency("tearfulness_postnatal", 0.70, 0.30),
            SymptomFrequency("intrusive_harm_thoughts", 0.40, 0.90),
            SymptomFrequency("insomnia_beyond_baby", 0.50, 0.70),
        ],
        discriminators=["baby blues: days 3-5, resolves by two weeks, "
                        "no functional impairment",
                        "perinatal depression: persistent low mood, "
                        "inability to enjoy or bond, beyond two weeks",
                        "unwanted intrusive thoughts of harm are common, "
                        "ego-dystonic and NOT protective-action triggers "
                        "— but postpartum PSYCHOSIS (delusions, voices, "
                        "confusion, not sleeping even when the baby "
                        "sleeps) is a psychiatric emergency",
                        "screen with Whooley questions at every "
                        "perinatal contact"],
        red_flags=["any psychotic symptom — postpartal psychosis is a "
                   "mother-and-baby-unit emergency",
                   "thoughts of harming the baby with intent or plan",
                   "not eating, not drinking, not sleeping despite the "
                   "baby sleeping",
                   "rapid deterioration over hours-days",
                   "previous postpartum psychosis or bipolar disorder — "
                   "high recurrence risk"],
        investigations=[
            InvestigationProfile("Whooley depression screen + risk "
                                 "assessment; TFT if postnatal exhaustion "
                                 "is atypical", "distinguish thyroid "
                                 "disease and screen every contact",
                                 0.80, 0.60, "NICE CG192 perinatal "
                                 "mental health"),
        ],
        management_first_line="Urgent perinatal mental-health referral "
                              "(same-day if any psychotic feature). "
                              "Depression: psychological therapy first; "
                              "sertraline is the usual SSRI in "
                              "breastfeeding. A pre-birth planning "
                              "meeting for known bipolar/psychosis "
                              "history prevents the emergency.",
        referral_tier="urgent",
        safety_net="Not sleeping even when the baby sleeps, hearing "
                   "things, feeling someone is controlling your "
                   "thoughts, or any thought of harming the baby — "
                   "same-day assessment via crisis line or A&E.",
        source="NICE CG192 perinatal mental health",
    ),
    # ================= 7.2 dermatology =================
    ConditionProfile(
        condition_id="acne_vulgaris",
        name="Acne vulgaris",
        category="dermatology",
        prevalence_per_consult=0.010,
        symptoms=[
            SymptomFrequency("facial_spots", 0.90, 0.80),
            SymptomFrequency("back_and_chest_spots", 0.55, 0.70),
            SymptomFrequency("greasy_skin", 0.60, 0.75),
            SymptomFrequency("teenage_onset", 0.60, 0.60),
            SymptomFrequency("comedones", 0.50, 0.80),
        ],
        discriminators=["open/closed comedones (blackheads/whiteheads) "
                        "plus inflammatory papules and pustules on "
                        "face, chest, back",
                        "acne rosacea: flushing, no comedones, "
                        "rhinophyma in men",
                        "folliculitis: scattered pustules, no comedones",
                        "drug acne: steroids, lithium, antiepileptics",
                        "in women with hirsutism, irregular periods or "
                        "weight gain think PCOS and check testosterone"],
        red_flags=["nodular/cystic acne with scarring — needs "
                   "dermatology before the scars are permanent",
                   "severe acne plus hirsutism and irregular periods "
                   "(PCOS workup)",
                   "acne with low mood or refusing to go out — treat "
                   "the psychosocial burden as seriously as the skin",
                   "sudden severe acne in a patient on steroids or "
                   "lithium — review the cause with the prescriber"],
        investigations=[
            InvestigationProfile("None needed unless PCOS suspected: "
                                 "then testosterone, SHBG, LH/FSH",
                                 "only for the hormonal pattern", 0.90,
                                 0.80, "NICE NG196 acne"),
        ],
        management_first_line="Grade severity honestly. Mild: benzoyl "
                              "peroxide + topical retinoid. Moderate: "
                              "add topical antibiotic or oral "
                              "doxycycline for 3 months; ALWAYS a "
                              "retinoid or benzoyl peroxide alongside "
                              "to resist resistance. Severe/scarring or "
                              "severe psychological distress: refer for "
                              "oral isotretinoin. Give it 3 months "
                              "before judging failure. Contraception "
                              "rules apply to isotretinoin and oral "
                              "tetracyclines.",
        referral_tier="self_care",
        safety_net="Spots becoming large, painful lumps under the skin, "
                   "leaving scars, or the acne is getting you down — "
                   "come back; referral for isotretinoin is justified "
                   "by scarring or psychological burden, not spot "
                   "counts alone.",
        source="NICE NG196 acne vulgaris",
    ),
    ConditionProfile(
        condition_id="urticaria_chronic",
        name="Chronic urticaria",
        category="dermatology",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("itchy_weals", 0.95, 0.90),
            SymptomFrequency("weals_come_and_go", 0.80, 0.85),
            SymptomFrequency("lip_swelling_angioedema", 0.30, 0.55),
        ],
        discriminators=["weals appear and resolve within 24 hours at "
                        "each site, itinerant, raised with pale centres "
                        "— the history IS the diagnosis",
                        "chronic (>6 weeks) urticaria is usually "
                        "AUTOIMMUNE or idiopathic — allergy testing is "
                        "not routinely indicated",
                        "urticarial vasculitis: weals lasting >24 h, "
                        "burning rather than itching, bruising — "
                        "biopsy",
                        "if each episode tracks a food or drug within "
                        "an hour, think IgE allergy and carry an "
                        "adrenaline auto-injector pending allergy "
                        "clinic"],
        red_flags=["any breathing difficulty, stridor, wheeze or "
                   "swelling of tongue/throat — anaphylaxis, 999",
                   "weals lasting over 24 hours or leaving bruising "
                   "(urticarial vasculitis)",
                   "associated fever, joint pain or weight loss "
                   "(systemic disease)"],
        investigations=[
            InvestigationProfile("None routinely; FBC/U&E/CRP/TSH only "
                                 "if systemic features", "chronic "
                                 "spontaneous urticaria is a clinical "
                                 "diagnosis", 0.95, 0.90,
                                 "NICE CKS urticaria; BSACI guideline"),
        ],
        management_first_line="Second-generation non-sedating "
                              "antihistamine DAILY (not as-needed), "
                              "up-titrating to four times the standard "
                              "dose before declaring failure; add a "
                              "second agent or short course only on "
                              "specialist advice. Avoid the "
                              "food-allergy fishing expedition — "
                              "6-week urticaria is not allergy until "
                              "proven.",
        referral_tier="routine",
        safety_net="Swelling of the lips or tongue with any difficulty "
                   "breathing, swallowing or a hoarse voice — 999. "
                   "Weals that stay in one place over a day or leave "
                   "bruises — book in for review and biopsy.",
        source="NICE CKS urticaria; BSACI chronic urticaria guideline",
    ),
    ConditionProfile(
        condition_id="scabies",
        name="Scabies",
        category="dermatology",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("family_itch_night", 0.70, 0.92),
            SymptomFrequency("burrow_tracks", 0.40, 0.92),
            SymptomFrequency("finger_web_itch", 0.50, 0.70),
            SymptomFrequency("worse_at_night", 0.80, 0.35),
        ],
        discriminators=["itch worse at night with similar symptoms in "
                        "household contacts — the two facts that "
                        "practically make the diagnosis",
                        "burrows in the finger webs, wrists, areolae, "
                        "genitals; spares the head in adults",
                        "atopic eczema: flexural, personal history, "
                        "no household spread",
                        "the itch persists 2-6 weeks after successful "
                        "treatment (post-scabetic itch) — do not "
                        "re-treat reflexively"],
        red_flags=["crusted (Norwegian) scabies in immunosuppressed, "
                   "elderly care-home or disabled patients — extremely "
                   "contagious, needs expert help and isolation",
                   "secondary bacterial infection (crusting, weeping, "
                   "cellulitis) — risk of post-streptococcal "
                   "glomerulonephritis",
                   "outbreak in a care home or ward — notify and "
                   "coordinate treatment of ALL residents and staff "
                   "same day"],
        investigations=[
            InvestigationProfile("Clinical diagnosis; dermatoscopy or "
                                 "skin scraping if doubt", "burrows or "
                                 "mites confirm", 0.90, 0.90,
                                 "NICE CKS scabies"),
        ],
        management_first_line="Permethrin 5% to the WHOLE body "
                              "including scalp/neck, re-applied at "
                              "day 7 — and treat EVERY contact and "
                              "household member the same day even if "
                              "itch-free. Wash bedding and clothes at "
                              "50 degrees on treatment day. Malathion "
                              "if permethrin unsuitable. Warn about "
                              "post-scabetic itch.",
        referral_tier="routine",
        safety_net="Spreading redness, weeping or fever means the skin "
                   "has become infected — same-day assessment. If the "
                   "whole household still itches after correct "
                   "treatment, come back (usually a missed contact, "
                   "not treatment failure).",
        source="NICE CKS scabies; UKHSA guidance on outbreaks",
    ),
    ConditionProfile(
        condition_id="tinea_corporis",
        name="Tinea (ringworm / athlete's foot)",
        category="dermatology",
        prevalence_per_consult=0.006,
        symptoms=[
            SymptomFrequency("ring_shaped_rash", 0.75, 0.88),
            SymptomFrequency("athletes_foot", 0.50, 0.80),
            SymptomFrequency("groin_itch", 0.40, 0.55),
            SymptomFrequency("scaly_ring_edge", 0.60, 0.60),
        ],
        discriminators=["annular plaque, scaly ACTIVE EDGE, central "
                        "clearing, slowly expanding",
                        "tinea pedis: maceration and itching between "
                        "the toes; check the groin — the foot is "
                        "usually the source",
                        "discoid eczema: coin-shaped, no active edge, "
                        "no central clearing",
                        "psoriasis: symmetrical plaques, elbow/knee/"
                        "scalp, no central clearing, nail pitting",
                        "STEROID-MODIFIED TINEA (tinea incognito): "
                        "rash spread and features muted by "
                        "corticosteroid cream — stop the steroid, "
                        "expect it to look worse before better"],
        red_flags=["scalp involvement in a child (kerion risk — "
                   "scarring alopecia; needs oral antifungal, never "
                   "topical alone)",
                   "diabetes or immunocompromise with rapidly "
                   "spreading or deep lesions",
                   "nail involvement (needs prolonged oral treatment "
                   "and confirmation)"],
        investigations=[
            InvestigationProfile("Skin scraping for mycology where "
                                 "diagnosis uncertain or treatment "
                                 "failing", "confirms and identifies "
                                 "species before long oral courses",
                                 0.85, 0.90, "NICE CKS fungal skin "
                                 "infection"),
        ],
        management_first_line="Topical antifungal (clotrimazole or "
                              "terbinafine — terbinafine faster) twice "
                              "daily for 2-4 weeks, continuing 1-2 "
                              "weeks after clearance; treat the feet "
                              "at the same time or the groin relapses. "
                              "NEVER combination steroid-antifungal "
                              "creams as first line. Wash towels and "
                              "bedding hot.",
        referral_tier="self_care",
        safety_net="If the ring keeps growing after four weeks of "
                   "correct treatment, the scalp or nails are involved, "
                   "or a child's scalp is affected — review (oral "
                   "treatment and confirmation needed).",
        source="NICE CKS fungal skin infections",
    ),
    ConditionProfile(
        condition_id="drug_eruption",
        name="Drug eruption (benign exanthem)",
        category="dermatology",
        prevalence_per_consult=0.003,
        symptoms=[
            # deliberately WEAK and few: the defining dangerous mimic
            # (SJS/TEN) lives in the emergency corpus, and a benign
            # exanthem must never out-score it on the same story.
            # An anchor to "a week after starting antibiotics"-style
            # phrasing only — bare "started <drug>" must NOT match.
            SymptomFrequency("new_drug_rash_week", 0.90, 0.70),
            SymptomFrequency("blistered_rash_benign", 0.30, 0.30),
        ],
        discriminators=["symmetric maculopapular exanthem starting "
                        "days-to-two-weeks after a new drug, patient "
                        "WELL — itch may be intense, mucous membranes "
                        "spared",
                        "antibiotics (penicillins, sulfonamides), "
                        "antiepileptics, allopurinol and NSAIDs are "
                        "the usual culprits",
                        "the patient being WELL is the discriminating "
                        "feature: fever + mucosal involvement + skin "
                        "pain = SJS/TEN, not a simple exanthem",
                        "viral exanthem identical — timing against "
                        "the drug list decides"],
        red_flags=["ANY mucosal involvement (lips, eyes, mouth, "
                   "genitals) — SJS/TEN until proven otherwise",
                   "skin pain out of proportion, blistering or skin "
                   "detaching",
                   "facial oedema, fever, lymphadenopathy or systemic "
                   "illness (DRESS — starts 2-6 weeks after drug, "
                   "eosinophilia)",
                   "breathing difficulty or collapse (anaphylaxis)"],
        investigations=[
            InvestigationProfile("Clinical diagnosis; no test proves "
                                 "a drug cause", "the drug-history "
                                 "timeline is the investigation",
                                 0.80, 0.70, "NICE CKS drug rash"),
        ],
        management_first_line="Stop the suspected drug where clinically "
                              "safe (coordinate with the prescriber if "
                              "it is an essential medicine); emollients "
                              "and sedating antihistamine at night for "
                              "itch; document the reaction in the "
                              "allergy record WITH the reaction "
                              "description — 'rash' alone poisons "
                              "future prescribing. Expect 1-2 weeks "
                              "to settle after stopping.",
        referral_tier="routine",
        safety_net="Blistering, sore lips/eyes/mouth, skin pain, "
                   "swelling of the face, fever or feeling very unwell "
                   "— same-day or emergency assessment. Anything that "
                   "gets worse rather than settles after stopping the "
                   "drug needs review.",
        source="NICE CKS drug eruptions; DermNet",
    ),
    ConditionProfile(
        condition_id="venous_leg_ulcer",
        name="Venous leg ulcer",
        category="dermatology",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("ankle_grazing_sore", 0.90, 0.88),
            SymptomFrequency("varicose_swollen_legs", 0.80, 0.75),
            SymptomFrequency("never_heals", 0.70, 0.65),
            SymptomFrequency("haemosiderin_staining", 0.50, 0.35),
        ],
        discriminators=["gaiter-area ulcer (above the ankle, medial "
                        "first) with oedema, haemosiderin staining, "
                        "lipodermatosclerosis or varicose veins — "
                        "venous",
                        "arterial ulcer: punched-out, painful AT "
                        "REST, distal (toes/pressure points), absent "
                        "pulses, needs vascular",
                        "mixed: venous picture plus absent pulses — "
                        "ABPI before compression (calciphylaxis and "
                        "vasculitis are the rarer mimics)",
                        "diabetic foot ulcer: plantar pressure points "
                        "and neuropathy"],
        red_flags=["ABPI <0.8 — do NOT compress; vascular referral",
                   "rapidly enlarging or deepening ulcer",
                   "surrounding cellulitis or systemic upset",
                   "rolled everted edge, non-healing beyond 12 weeks "
                   "despite treatment — squamous cell carcinoma "
                   "(Marjolin), 2ww"],
        investigations=[
            InvestigationProfile("ABPI (Doppler) before compression "
                                 "bandaging", "excludes arterial "
                                 "insufficiency; compression on an "
                                 "ischaemic leg causes gangrene",
                                 0.95, 0.95, "NICE CG168 leg ulcer"),
        ],
        management_first_line="Compression is the treatment — "
                              "four-layer bandaging or hosiery once "
                              "ABPI permits; treat infection only when "
                              "clinically infected (colonisation is "
                              "universal); simple non-adherent "
                              "dressings; analgesia before dressing "
                              "changes; elevate legs and keep walking.",
        referral_tier="routine",
        safety_net="Rapidly spreading redness, feeling feverish, black "
                   "areas, or pain at rest — same-day assessment. Any "
                   "ulcer not healing after 12 weeks of correct "
                   "compression goes to the 2-week-wait pathway to "
                   "exclude skin cancer.",
        source="NICE CG168 venous leg ulcers; SIGN",
    ),
    ConditionProfile(
        condition_id="seborrhoeic_dermatitis",
        name="Seborrhoeic dermatitis",
        category="dermatology",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("eyebrow_nasal_flaking", 0.80, 0.85),
            SymptomFrequency("scalp_flaking_dandruff", 0.70, 0.60),
        ],
        discriminators=["greasy scale in the SEBORRHOEIC sites: "
                        "nasolabial folds, eyebrows, scalp margin, "
                        "sternum, ears",
                        "psoriasis: well-demarcated thick silvery "
                        "plaques, elbows/knees/extensor, nail pitting",
                        "atopic eczema: flexural, dry, personal "
                        "atopy",
                        "NEW severe seborrhoeic dermatitis: think "
                        "HIV (test) and Parkinson's disease"],
        red_flags=["sudden severe or resistant disease — offer HIV "
                   "test and look for parkinsonism",
                   "widespread involvement or scalp involvement "
                   "causing hair loss",
                   "not settling after 8 weeks of correct treatment"],
        investigations=[
            InvestigationProfile("Clinical diagnosis; HIV test if "
                                 "severe/new/atypical", "one of the "
                                 "few skin diagnoses that hides a "
                                 "systemic cause", 0.70, 0.80,
                                 "NICE CKS seborrhoeic dermatitis"),
        ],
        management_first_line="Ketoconazole 2% shampoo used as a body "
                              "and scalp wash twice weekly for a "
                              "month, then weekly maintenance (it "
                              "recurs); mild steroid (hydrocortisone) "
                              "or tacrolimus briefly for florid "
                              "inflammation on the face — avoid "
                              "prolonged steroids. Set the "
                              "expectation early: control, not cure.",
        referral_tier="self_care",
        safety_net="Spreading, painful, weeping or crusted skin "
                   "(bacterial superinfection) — same-day review. "
                   "No better after two months of correct treatment — "
                   "review the diagnosis.",
        source="NICE CKS seborrhoeic dermatitis",
    ),
    # ================= 7.2 women's health =================
    ConditionProfile(
        condition_id="menopause",
        name="Menopause",
        category="womens_health",
        prevalence_per_consult=0.020,
        symptoms=[
            SymptomFrequency("periods_stopped_year", 0.85, 0.90),
            SymptomFrequency("hot_flushes", 0.80, 0.88),
            SymptomFrequency("night_sweats", 0.50, 0.15),
            SymptomFrequency("concentration_foggy", 0.40, 0.30),
            SymptomFrequency("vaginal_dryness", 0.35, 0.60),
        ],
        discriminators=["12 months of amenorrhoea (mean age 51 in the "
                        "UK) with vasomotor symptoms",
                        "perimenopause: irregular periods WHILE still "
                        "having them — symptoms often worst here",
                        "thyroid disease mimics: weight change, "
                        "palpitations, tremor — check TSH if "
                        "atypical",
                        "premature menopause under 40 is a separate "
                        "diagnosis needing specialist input and "
                        "hormone replacement at least to age 51"],
        red_flags=["ANY bleeding after 12 months without periods — "
                   "postmenopausal bleeding: 2ww endometrial cancer "
                   "pathway, never 'just a final period'",
                   "menopause under 40 (premature ovarian "
                   "insufficiency) — bone and cardiovascular "
                   "protection needed",
                   "severe new headaches on HRT, migraine with aura "
                   "and oestrogen choices, undiagnosed vaginal "
                   "bleeding before starting HRT"],
        investigations=[
            InvestigationProfile("Diagnosis is clinical over 45; FSH "
                                 "only if under 45 or doubt",
                                 "bloods add nothing after a year of "
                                 "amenorrhoea at 50+", 0.90, 0.85,
                                 "NICE NG23 menopause"),
        ],
        management_first_line="Explain the timeline (average 7 years "
                              "of symptoms, longer for some). CBT "
                              "first line for low mood/anxiety; HRT "
                              "for vasomotor symptoms (discuss the "
                              "real absolute risks, not the "
                              "headlines); vaginal oestrogen and "
                              "moisturisers for genitourinary "
                              "symptoms; bone/cardiovascular lifestyle "
                              "advice. Contraception still needed for "
                              "2 years after last period under 50, "
                              "1 year over 50.",
        referral_tier="routine",
        safety_net="ANY bleeding after a year without periods needs "
                   "an urgent appointment — that is a 2-week-wait "
                   "cancer pathway, not a wait-and-see. New severe "
                   "headaches, calf pain or breathlessness on HRT — "
                   "same-day.",
        source="NICE NG23 menopause",
    ),
    ConditionProfile(
        condition_id="perimenopause",
        name="Perimenopause",
        category="womens_health",
        prevalence_per_consult=0.015,
        symptoms=[
            SymptomFrequency("periods_irregular_transition", 0.85, 0.80),
            SymptomFrequency("hot_flushes", 0.60, 0.88),
            SymptomFrequency("sleep_mood_perimeno", 0.60, 0.50),
        ],
        discriminators=["cycle length varying by 7+ days, skipped "
                        "periods, heavier flow — the menopausal "
                        "transition typically starts mid-40s",
                        "pregnancy still possible until 2 years "
                        "after the last period — test before "
                        "attributing amenorrhoea",
                        "abnormal bleeding pattern with intermenstrual "
                        "bleeding or postcoital bleeding is NOT "
                        "perimenopause until examined",
                        "thyroid and iron studies for the tired "
                        "overlapping presentations"],
        red_flags=["intermenstrual or postcoital bleeding — "
                   "examine and consider 2ww",
                   "flooding, clots, anaemia — investigate and treat "
                   "heavy menstrual bleeding",
                   "pregnancy (ectopic) in the amenorrhoea phase",
                   "under 40 with menopausal symptoms — premature "
                   "ovarian insufficiency pathway"],
        investigations=[
            InvestigationProfile("Clinical; FSH unreliable in "
                                 "perimenopause; pregnancy test when "
                                 "periods missed", "a single normal "
                                 "FSH excludes nothing mid-transition",
                                 0.70, 0.70, "NICE NG23 menopause"),
        ],
        management_first_line="Contraception with symptom control in "
                              "one: the Mirena or a "
                              "levonorgestrel method plus transdermal "
                              "oestrogen is the classic combination; "
                              "CBT for mood/sleep; iron check when "
                              "flow increases. Review HRT/contraception "
                              "annually with BP and weight.",
        referral_tier="routine",
        safety_net="Bleeding between periods, after sex, or soaking "
                   "pads hourly — urgent review. A missed period with "
                   "one-sided pain — same-day (ectopic).",
        source="NICE NG23 menopause; NICE NG88 heavy menstrual bleeding",
    ),
    ConditionProfile(
        condition_id="subfertility",
        name="Subfertility",
        category="womens_health",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("trying_conceive_years", 0.95, 0.92),
            SymptomFrequency("periods_infrequent", 0.40, 0.40),
            SymptomFrequency("low_libido", 0.20, 0.20),
        ],
        discriminators=["definition: no conception after 12 months of "
                        "regular unprotected intercourse (under 35) — "
                        "6 months if the woman is 35-39; immediate "
                        "referral over 40 or a known cause",
                        "both partners are patients from day one: "
                        "semen analysis is the cheapest test in "
                        "fertility and 40% of factors are male",
                        "regular cycles + patent tubes + normal "
                        "semen = unexplained, not untreatable",
                        "frequency of intercourse (every 2-3 days) "
                        "before ovulation tracking"],
        red_flags=["woman over 36 — refer after 6 months, do not "
                   "wait the year",
                   "known endometriosis, PID history, chemotherapy, "
                   "undescended testis, erectile dysfunction — refer "
                   "now",
                   "no periods at all (hypothalamic or PCOS) — needs "
                   "induction, not patience",
                   "recurrent miscarriage (3+) — separate referral"],
        investigations=[
            InvestigationProfile("Day-21 progesterone (confirming "
                                 "ovulation) + semen analysis + rubella "
                                 "status; TSH/prolactin if cycle "
                                 "irregular; chlamydia screen before "
                                 "tubal assessment", "the basic "
                                 "fertility workup is primary care's "
                                 "job", 0.85, 0.80,
                                 "NICE CG156 fertility"),
        ],
        management_first_line="Folic acid 400 mcg (5 mg if diabetic "
                              "or antiepileptic), stop smoking BOTH "
                              "partners, alcohol under limits, BMI "
                              "20-30 (fertility treatment thresholds "
                              "apply), rubella immunity checked "
                              "BEFORE conception. Complete the "
                              "first-line workup in general practice "
                              "and refer with the results, not "
                              "before.",
        referral_tier="routine",
        safety_net="A positive test with one-sided pain or bleeding — "
                   "same-day (ectopic). Otherwise the safety net is "
                   "emotional: fertility strain is a risk factor for "
                   "depression — review mood at each visit.",
        source="NICE CG156 fertility problems",
    ),
    ConditionProfile(
        condition_id="pcos",
        name="Polycystic ovary syndrome",
        category="womens_health",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("periods_infrequent", 0.85, 0.55),
            SymptomFrequency("hirsutism", 0.60, 0.80),
            SymptomFrequency("weight_gain_pcos", 0.50, 0.30),
            SymptomFrequency("acne_pcos", 0.30, 0.25),
        ],
        discriminators=["Rotterdam: 2 of 3 — oligo/anovulation, "
                        "hyperandrogenism (clinical or biochemical), "
                        "polycystic ovaries on ultrasound",
                        "exclude mimics first: TSH, prolactin, and "
                        "17-OH-progesterone for late-onset CAH; "
                        "testosterone VERY high or virilisation "
                        "points to tumour — urgent endocrine",
                        "NOT just a fertility problem: T2DM risk "
                        "(OGTT annually if obese), cardiovascular "
                        "risk, endometrial protection, mood, sleep "
                        "apnoea, eating disorders",
                        "weight loss of 5% can restore cycles — the "
                        "most effective single intervention"],
        red_flags=["severe rapid virilisation (clitoromegaly, "
                   "deepening voice, balding) — androgen-secreting "
                   "tumour, urgent",
                   "no period for 3+ months repeatedly — unopposed "
                   "oestrogen, endometrial hyperplasia risk",
                   "fertility wishes — metformin/letrozole pathways "
                   "and referral thresholds differ"],
        investigations=[
            InvestigationProfile("Testosterone/SHBG, TSH, prolactin, "
                                 "17-OH-progesterone; pelvic "
                                 "ultrasound; OGTT/HbA1c if overweight",
                                 "diagnosis of exclusion + metabolic "
                                 "risk stratification", 0.85, 0.80,
                                 "NICE NG201 PCOS"),
        ],
        management_first_line="Combined hormonal contraception for "
                              "cycle control and "
                              "androgen symptoms (or metformin when "
                              "COCP unsuitable/wanted); cosmetic "
                              "measures for hair; weight management "
                              "as the foundation; ENDOMETRIAL "
                              "PROTECTION if periods absent 3+ "
                              "months; annual diabetes screen when "
                              "overweight; fertility referral per "
                              "NG201 when trying.",
        referral_tier="routine",
        safety_net="Bleeding after months of no periods that is heavy "
                   "or prolonged — review. Rapid masculinisation — "
                   "urgent endocrine. Trying for a baby with no "
                   "periods — refer rather than wait the full year.",
        source="NICE NG201 PCOS; Rotterdam criteria",
    ),
    ConditionProfile(
        condition_id="dysmenorrhoea",
        name="Primary dysmenorrhoea (period pain)",
        category="womens_health",
        prevalence_per_consult=0.010,
        symptoms=[
            SymptomFrequency("period_pain_cyclical", 0.95, 0.70),
            SymptomFrequency("period_pain_first_day", 0.70, 0.70),
        ],
        discriminators=["primary: starts with the period (or just "
                        "before), worst first 1-2 days, spasmodic, "
                        "from teenage years, normal examination — "
                        "NSAIDs and hormones both work",
                        "secondary: starts after 25, progressive, "
                        "pain through the month, deep dyspareunia, "
                        "irregular or heavy — ENDOMETRIOSIS or "
                        "fibroids until proven otherwise",
                        "do not normalise pain that stops school, "
                        "work or sleep — that severity earns a "
                        "workup even in teenagers"],
        red_flags=["progressive or mid-cycle pain, deep dyspareunia, "
                   "dyschezia — secondary dysmenorrhoea",
                   "pain with heavy flooding and anaemia",
                   "new pain after 30 or pelvic pain with fever "
                   "(PID)",
                   "unilateral pain with missed period (ectopic)"],
        investigations=[
            InvestigationProfile("Clinical + pelvic examination when "
                                 "secondary suspected; ultrasound for "
                                 "structural causes", "separates "
                                 "primary from secondary", 0.75, 0.75,
                                 "NICE NG73 endometriosis"),
        ],
        management_first_line="NSAID (ibuprofen/naproxen) started "
                              "EARLY at onset + heat; hormonal "
                              "options (COCP or progestogen) both "
                              "treat and contracept; TENS as adjunct. "
                              "If pain controls her life despite 3-6 "
                              "months of treatment — refer: "
                              "endometriosis is found at laparoscopy, "
                              "not in a consultation.",
        referral_tier="self_care",
        safety_net="Pain different from your normal pattern, fever, "
                   "discharge, pain between periods or during sex, "
                   "or a missed period — book in. Pain never "
                   "controlled by NSAIDs plus hormones — referral.",
        source="NICE NG73 endometriosis; CKS dysmenorrhoea",
    ),
    # ================= 7.2 men's health =================
    ConditionProfile(
        condition_id="erectile_dysfunction",
        name="Erectile dysfunction",
        category="urology_kidney",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("ed_difficulty_months", 0.95, 0.85),
            SymptomFrequency("morning_erections_preserved", 0.50, 0.70),
            SymptomFrequency("low_libido", 0.30, 0.45),
        ],
        discriminators=["morning/self-stimulated erections preserved = "
                        "predominantly psychological; absent = organic "
                        "(vascular, neurological, hormonal)",
                        "ED is a CARDIOVASCULAR warning light: the "
                        "penile arteries narrow first — screen BP, "
                        "lipids, HbA1c and count the risk years "
                        "before the angina arrives",
                        "drug causes: beta-blockers, thiazides, "
                        "SSRIs, finasteride, antipsychotics",
                        "low libido + fatigue + gynaecomastia: check "
                        "testosterone (morning) and prolactin",
                        "sudden onset after relationship change with "
                        "preserved morning erections points "
                        "psychological"],
        red_flags=["ED with claudication, angina or multiple vascular "
                   "risk factors — treat the vascular risk TODAY "
                   "(ED predicts cardiovascular events 2-5 years "
                   "ahead)",
                   "low libido, galactorrhoea or visual field loss — "
                   "prolactinoma workup",
                   "penile curvature with pain (Peyronie's)",
                   "ED as the first sign of diabetes — check glucose"],
        investigations=[
            InvestigationProfile("Cardiovascular screen (BP, "
                                 "lipids, HbA1c), morning testosterone "
                                 "if low libido; PSA only if "
                                 "prostate concern", "ED workup is a "
                                 "cardiovascular workup", 0.85, 0.80,
                                 "NICE CKS erectile dysfunction"),
        ],
        management_first_line="Screen and treat cardiovascular risk "
                              "first; PDE-5 inhibitors (sildenafil "
                              "first) — explain dosing: sexual "
                              "stimulation required, takes an hour, "
                              "fatty meals delay; NEVER with nitrates; "
                              "review dose at 4 weeks. Psychological "
                              "and couples factors respond to being "
                              "asked about. Refer the "
                              "treatment-resistant or young-onset "
                              "organic cases.",
        referral_tier="routine",
        safety_net="Chest pain on exertion, calf pain walking, or "
                   "anything suggesting the arteries are diseased "
                   "wider than the penis — urgent review of "
                   "cardiovascular risk. Prolonged painful erection "
                   "over 4 hours on treatment — emergency.",
        source="NICE CKS erectile dysfunction",
    ),
    ConditionProfile(
        condition_id="benign_prostatic_hyperplasia",
        name="Benign prostatic enlargement (BPH)",
        category="urology_kidney",
        prevalence_per_consult=0.008,
        symptoms=[
            # no bare age token: nocturia + weak stream + hesitancy
            # carry the diagnosis; "76 year old man" alone must not.
            SymptomFrequency("nocturia", 0.80, 0.70),
            SymptomFrequency("weak_urine_stream", 0.80, 0.80),
            SymptomFrequency("incomplete_emptying", 0.60, 0.65),
            SymptomFrequency("frequency_micturition", 0.60, 0.30),
        ],
        discriminators=["storage + voiding symptoms together over "
                        "months-years in an older man; prostate smooth "
                        "and enlarged on examination",
                        "prostate cancer: rarely causes flow symptoms "
                        "until advanced — but haematuria, weight loss "
                        "or bone pain change everything",
                        "urethral stricture: prior catheter or "
                        "infection, slow steady stream with spraying",
                        "overactive bladder: storage-only, no weak "
                        "stream",
                        "nocturnal polyuria (heart failure, late "
                        "fluids, sleep apnoea) vs bladder: a "
                        "frequency-volume chart separates them"],
        red_flags=["acute retention or overflow incontinence — "
                   "catheter, same-day",
                   "haematuria — bladder/kidney cancer pathways",
                   "recurrent infections or renal impairment from "
                   "obstruction (check creatinine/eGFR)",
                   "PSA discussion: counsel BEFORE testing (NICE "
                   "— the harms of overdiagnosis are real)"],
        investigations=[
            InvestigationProfile("Urinalysis, U&E/eGFR, frequency "
                                 "chart; PSA after counselling; "
                                 "post-residual ultrasound if "
                                 "retention suspected", "quantifies "
                                 "symptoms and protects the kidneys",
                                 0.80, 0.75, "NICE NG97 lower urinary "
                                 "tract symptoms"),
        ],
        management_first_line="Conservative: fluids 2h before bed "
                              "reduced, double voiding, review "
                              "anticholinergic burden and bladder-"
                              "irritating drugs. Alpha-blocker "
                              "(tamsulosin) for flow symptoms within "
                              "days-weeks; 5-alpha-reductase "
                              "inhibitor for large prostates over "
                              "months (PSA halves — halve the "
                              "reference range). Watch the "
                              "orthostatic-hypotension interaction "
                              "with other BP drugs, especially in "
                              "older patients on multiple agents.",
        referral_tier="routine",
        safety_net="Cannot pass water at all, or dribbling "
                   "overflow — emergency catheterisation. Blood in "
                   "the urine, weight loss or bone pain — urgent "
                   "cancer-pathway review.",
        source="NICE NG97 lower urinary tract symptoms in men",
    ),
    ConditionProfile(
        condition_id="testicular_cancer_suspect",
        name="Suspected testicular cancer",
        category="urology_kidney",
        prevalence_per_consult=0.0002,
        symptoms=[
            SymptomFrequency("testicular_hard_lump", 0.80, 0.92),
            SymptomFrequency("testicular_ache_chronic", 0.50, 0.55),
        ],
        discriminators=["painless hard lump or testicular "
                        "enlargement over weeks — cancer until "
                        "ultrasound says otherwise",
                        "epididymal cyst: separate from and behind "
                        "the testis, transilluminates",
                        "varicocele: bag of worms, left-sided, "
                        "collapses lying flat",
                        "torsion: sudden severe pain hours not "
                        "weeks, vomiting, high-riding testis",
                        "hydrocele: whole scrotum, transilluminates "
                        "— but ultrasound any hydrocele in a young "
                        "man to see the testis beneath"],
        red_flags=["any painless testicular lump, swelling or "
                   "firmness — urgent (2ww) ultrasound via the "
                   "suspected-cancer pathway",
                   "testicular ache persisting over 2 weeks without "
                   "explanation",
                   "gynaecomastia or back pain in a 20-40 year old "
                   "man (hormone-producing tumour or "
                   "retroperitoneal nodes)"],
        investigations=[
            InvestigationProfile("Urgent scrotal ultrasound + "
                                 "testicular tumour markers (AFP, "
                                 "hCG, LDH)", "diagnosis and "
                                 "staging in one move", 0.95, 0.90,
                                 "NICE NG12 suspected cancer"),
        ],
        management_first_line="Two-week-wait urology referral for any "
                              "painless lump or unexplained "
                              "persistent ache: do NOT needle-biopsy "
                              "a testicular lump, do not offer a "
                              "wait-and-see. Ultrasound + markers. "
                              "Testicular cancer is one of the most "
                              "curable cancers — 96%+ overall — but "
                              "only if it is found.",
        referral_tier="two_week_wait",
        safety_net="Any lump you are unsure of, or an ache that "
                   "persists two weeks — urgent referral, not "
                   "reassurance. Sudden severe testicular pain — "
                   "999/same-day emergency (torsion).",
        source="NICE NG12 suspected cancer referral",
    ),
    ConditionProfile(
        condition_id="prostatitis",
        name="Prostatitis",
        category="urology_kidney",
        prevalence_per_consult=0.002,
        symptoms=[
            SymptomFrequency("dysuria", 0.70, 0.30),
            # 0.85: pelvic/perineal pain is the DEFINING feature of chronic
            # prostatitis — without it leading, a male UTI story outranks it
            # by prevalence weighting alone (0.497 vs 0.494 on the probe).
            SymptomFrequency("deep_pelvic_pain_male", 0.85, 0.85),
            SymptomFrequency("frequency_micturition", 0.60, 0.25),
            SymptomFrequency("fever", 0.40, 0.15),
        ],
        discriminators=["perineal/low-back/pelvic pain with urinary "
                        "symptoms over weeks — chronic prostatitis/"
                        "chronic pelvic pain syndrome",
                        "ACUTE bacterial prostatitis: fever, rigors, "
                        "severe pain, often retention — admission, "
                        "IV antibiotics",
                        "UTI/cystitis in men is NOT simple: "
                        "investigate every one (outflow, stone, "
                        "prostate)",
                        "sexually acquired pelvic pain: sexual "
                        "history, test for chlamydia/gonorrhoea and "
                        "treat partner",
                        "chronic pelvic pain with negative cultures "
                        "and normal examination is still real — "
                        "multimodal management, not dismissal"],
        red_flags=["fever + rigors + acute pelvic pain = acute "
                   "bacterial prostatitis — admission for IV "
                   "antibiotics (sepsis risk)",
                   "acute urinary retention",
                   "recurrent episodes — underlying outflow or "
                   "stone; prostate cancer still needs excluding if "
                   "PSA raised",
                   "age >50 with new urinary symptoms and no clear "
                   "cause — examine and counsel about PSA"],
        investigations=[
            InvestigationProfile("Urinalysis + MSU; STI screen in "
                                 "younger men; consider prostatic "
                                 "secretion culture (specialist)",
                                 "guides the antibiotic class and "
                                 "duration", 0.75, 0.65, "NICE CKS "
                                 "prostatitis; EAU guidelines"),
        ],
        management_first_line="Acute: admit if systemically unwell — "
                              "IV antibiotics (avoid aminoglycoside "
                              "if renal impairment). Chronic "
                              "bacterial: 4-6 WEEKS of a "
                              "prostate-penetrating antibiotic "
                              "(ciprofloxacin or trimethoprim — "
                              "check resistance and mind "
                              "stewardship); alpha-blocker and "
                              "anti-inflammatories for pain; "
                              "realistic expectations — chronic "
                              "pelvic pain syndrome runs months and "
                              "needs a supportive plan not repeated "
                              "antibiotics.",
        referral_tier="urgent",
        safety_net="Fever, shaking chills, worsening pain or unable "
                   "to pass urine — same-day (sepsis/retention). "
                   "Pain not settling after the full antibiotic "
                   "course — review rather than repeat.",
        source="NICE CKS prostatitis; European Association of "
               "Urology guidelines",
    ),
    # ================= 7.3 chronic GI / hepatology / renal =================
    ConditionProfile(
        condition_id="constipation_simple",
        name="Constipation",
        category="gastrointestinal",
        prevalence_per_consult=0.020,
        symptoms=[
            SymptomFrequency("bowel_freq_reduced", 0.90, 0.85),
            SymptomFrequency("hard_stools_straining", 0.60, 0.70),
            SymptomFrequency("tummy_discomfort_constipation", 0.50, 0.30),
        ],
        discriminators=["reduced frequency against the patient's OWN "
                        "baseline, hard stools, straining — 'nine days "
                        "without' is normal for some and a change for "
                        "others",
                        "secondary causes first: opioids, iron, "
                        "anticholinergics, antacids, hypothyroidism, "
                        "diabetes, immobility, dehydration",
                        "IBS-C: chronic cramping relief with opening "
                        "bowels, years of alternation",
                        "overflow: hard impaction with liquid leakage "
                        "around it (paradoxical diarrhoea)"],
        red_flags=["absolute constipation with vomiting and a "
                   "distended tummy — obstruction: emergency",
                   "new constipation over 50 with weight loss or a "
                   "family history of colorectal cancer — 2ww",
                   "blood in or on the stool",
                   "severe or sudden abdominal pain",
                   "constipation with new neurological signs (cord "
                   "lesion)"],
        investigations=[
            InvestigationProfile("None routinely; bloods only for "
                                 "secondary-cause suspicion (TFT, "
                                 "calcium, glucose, FBC)", "the "
                                 "diagnosis is the history and the "
                                 "bowel pattern", 0.85, 0.85,
                                 "NICE CG61 constipation"),
        ],
        management_first_line="Treat the cause found (review opioids, "
                              "iron, anticholinergics); fluids, "
                              "fibre, mobility; osmotic laxative "
                              "(macrogols) first for hard stools, "
                              "stimulant (senna) added for slow "
                              "transit; review at 4 weeks and adjust "
                              "rather than rotate. Never straining "
                              "advice alone in the elderly — treat.",
        referral_tier="self_care",
        safety_net="Vomiting with a swollen tummy and no bowel "
                   "actions at all, blood in the motions, or new "
                   "severe pain — emergency/same-day. Constipation "
                   "that keeps recurring despite treatment — review "
                   "for secondary causes.",
        source="NICE CG61 constipation; CKS",
    ),
    ConditionProfile(
        condition_id="crohns_disease_suspect",
        name="Suspected Crohn's disease",
        category="gastrointestinal",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("crampy_abdominal_pain_months", 0.80, 0.55),
            SymptomFrequency("chronic_diarrhoea_months", 0.70, 0.40),
            SymptomFrequency("mouth_ulcers", 0.30, 0.55),
            SymptomFrequency("weight_loss", 0.50, 0.30),
            SymptomFrequency("perianal_disease", 0.25, 0.90),
        ],
        discriminators=["any-length gut, skip lesions, mouth to anus: "
                        "mouth ulcers + cramping pain + diarrhoea + "
                        "weight loss + perianal tags/fistula is the "
                        "classic tapestry",
                        "ulcerative colitis: bloody diarrhoea, "
                        "urgency, no skip areas, no mouth/perianal "
                        "disease",
                        "coeliac: bread-triggered bloating, no "
                        "weight loss pattern, no perianal disease",
                        "IBS: chronic pain but NO weight loss, NO "
                        "nocturnal symptoms, NO blood",
                        "appendicitis/lymphoma can present as the "
                        "first Crohn's event"],
        red_flags=["persistent diarrhoea >6 weeks with weight loss, "
                   "night symptoms or iron deficiency — refer "
                   "(gastroenterology; consider 2ww colorectal if "
                   "over 50 with change in bowel habit)",
                   "perianal fistula/abscess — surgical + "
                   "gastroenterology",
                   "severe flare: fever, tachycardia, distension, "
                   "vomiting — admission",
                   "family history of IBD or coeliac strengthens "
                   "suspicion in vague cases"],
        investigations=[
            InvestigationProfile("FBC, CRP, coeliac serology, ferritin "
                                 "+ faecal calprotectin", "calprotectin "
                                 "separates inflamed from irritable "
                                 "bowels and stops the wrong referral",
                                 0.85, 0.75, "NICE NG11 IBD"),
        ],
        management_first_line="Suspected Crohn's goes to "
                              "gastroenterology with the bloods and "
                              "calprotectin already done — referral "
                              "letters without them bounce. Stop "
                              "smoking (doubles flare risk), assess "
                              "nutrition and bone health (steroid "
                              "exposure ahead), check vaccination "
                              "status before immunosuppression.",
        referral_tier="urgent",
        safety_net="Fever with a swollen tender tummy and vomiting — "
                   "emergency. Rapid weight loss, night-time "
                   "diarrhoea, or new perianal pain/swelling — "
                   "same-week review.",
        source="NICE NG11 / CG152 Crohn's disease",
    ),
    ConditionProfile(
        condition_id="ulcerative_colitis_suspect",
        name="Suspected ulcerative colitis",
        category="gastrointestinal",
        prevalence_per_consult=0.0005,
        symptoms=[
            SymptomFrequency("bloody_diarrhoea_chronic", 0.85, 0.88),
            SymptomFrequency("mucous_rectal_passage", 0.50, 0.65),
            SymptomFrequency("nocturnal_diarrhoea", 0.60, 0.75),
            SymptomFrequency("bowel_urgency", 0.60, 0.45),
        ],
        discriminators=["continuous bloody diarrhoea with urgency and "
                        "nocturnal defaecation — blood is the "
                        "discriminator against every functional "
                        "story",
                        "infective diarrhoea: acute (<2 weeks), "
                        "travel/food history, fever, settles — "
                        "ALWAYS send stool culture on any chronic-"
                        "looking bloody diarrhoea",
                        "colorectal cancer: over 50, change in "
                        "habit, iron deficiency — 2ww",
                        "ischaemic colitis: elderly, vascular "
                        "disease, sudden pain then blood",
                        "haemorrhoids: bright blood on the paper, no "
                        "diarrhoea, no urgency"],
        red_flags=["more than six bloody stools a day with fever, "
                   "tachycardia or abdominal distension — toxic "
                   "megacolon: ADMIT",
                   "any chronic bloody diarrhoea is a specialist-"
                   "referral presentation, not a wait-and-see",
                   "severe anal pain or incontinence",
                   "weight loss, night sweats, frequent nocturnal "
                   " stools"],
        investigations=[
            InvestigationProfile("Stool culture + faecal "
                                 "calprotectin; FBC/CRP/ferritin",
                                 "exclude infection before the IBD "
                                 "label; calprotectin proves "
                                 "inflammation", 0.85, 0.80,
                                 "NICE NG11 IBD"),
        ],
        management_first_line="Refer to gastroenterology for "
                              "endoscopic diagnosis — treatment "
                              "(mesalazine, steroids, biologics) "
                              "follows extent and severity and "
                              "belongs in specialist hands. In "
                              "general practice: send the stool "
                              "culture, check bloods, exclude "
                              "infection, never steroid-mask an "
                              "undiagnosed bloody diarrhoea.",
        referral_tier="urgent",
        safety_net="More than six bloody stools a day, fever, "
                   "racing heart, swollen tummy or worsening "
                   "abdominal pain — emergency admission. Any "
                   "rectal bleeding that continues for more than a "
                   "couple of weeks — urgent review.",
        source="NICE NG11 ulcerative colitis; CKS",
    ),
    ConditionProfile(
        condition_id="coeliac_disease",
        name="Coeliac disease",
        category="gastrointestinal",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("wheat_triggered_bloating", 0.60, 0.85),
            SymptomFrequency("chronic_diarrhoea_months", 0.50, 0.40),
            SymptomFrequency("fatigue", 0.60, 0.10),
            SymptomFrequency("mouth_ulcers", 0.20, 0.55),
        ],
        discriminators=["bloating and diarrhoea tracking wheat "
                        "intake, with fatigue, iron deficiency or "
                        "mouth ulcers — 1% of the population, "
                        "mostly undiagnosed",
                        "IBS: no weight loss, no anaemia, normal "
                        "calprotectin, no trigger foods on testing",
                        "wheat intolerance/non-coeliac "
                        "sensitivity: symptoms without serology or "
                        "villous atrophy",
                        "dermatitis herpetiformis: the itchy "
                        "blistering elbows/knees rash IS coeliac "
                        "disease of the skin",
                        "type 1 diabetes, thyroid disease, family "
                        "history — test early"],
        red_flags=["weight loss with the wheat symptoms — refer "
                   "actively",
                   "iron-deficiency anaemia without a source (2ww if "
                   "over 50 or family history)",
                   "osteoporosis/fragility fracture on an "
                   "undiagnosed malabsorption background",
                   "persistent symptoms despite a gluten-free diet "
                   "— refractory disease and lymphoma risk need "
                   "specialist review"],
        investigations=[
            InvestigationProfile("Coeliac serology (anti-tTG IgA + "
                                 "total IgA) WHILE STILL EATING "
                                 "GLUTEN", "testing after starting a "
                                 "gluten-free diet falsely "
                                 "normalises — keep gluten in until "
                                 "diagnosis", 0.90, 0.95,
                                 "NICE NG20 coeliac disease"),
        ],
        management_first_line="Serology while eating gluten; confirm "
                              "with duodenal biopsy BEFORE the "
                              "diet; then lifelong gluten-free with "
                              "dietitian input, baseline DEXA, "
                              "vaccinations (pneumococcal — "
                              "hyposplenism), and annual review of "
                              "iron/B12/folate. First-degree "
                              "relatives: offer testing.",
        referral_tier="routine",
        safety_net="Weight loss, increasing pain, fever or the "
                   "anaemia worsening — review sooner. Do not "
                   "settle into a gluten-free diet without the "
                   "diagnosis confirmed — the diet changes the "
                   "tests.",
        source="NICE NG20 coeliac disease",
    ),
    ConditionProfile(
        condition_id="cirrhosis_decompensated",
        name="Decompensated cirrhosis",
        category="gastrointestinal",
        prevalence_per_consult=0.0004,
        symptoms=[
            SymptomFrequency("known_cirrhosis", 0.95, 0.92),
            SymptomFrequency("confusion", 0.60, 0.15),
            SymptomFrequency("jaundice", 0.60, 0.40),
            SymptomFrequency("ascites_swelling", 0.70, 0.80),
            SymptomFrequency("ankle_swelling", 0.40, 0.20),
        ],
        discriminators=["any NEW confusion, jaundice, ascites, "
                        "variceal bleed or encephalopathy in known "
                        "cirrhosis = decompensation — a different "
                        "disease from compensated cirrhosis",
                        "encephalopathy: fluctuating confusion with "
                        "asterixis (liver flap), reversed sleep "
                        "pattern — look for the precipitant: "
                        "constipation, infection, GI bleed, drugs, "
                        "electrolytes",
                        "ascites: new abdominal swelling with "
                        "shifting dullness; spontaneous bacterial "
                        "peritonitis until tapped and proven "
                        "otherwise when unwell",
                        "delirium of other causes: cirrhosis patients "
                        "develop every delirium cause faster"],
        red_flags=["confusion/drowsiness in a cirrhotic — hepatic "
                   "encephalopathy, same-day assessment",
                   "vomiting blood or melaena — varices: 999",
                   "fever or abdominal pain with ascites — SBP: "
                   "admit for diagnostic tap",
                   "jaundice deepening rapidly",
                   "reduced urine output (hepatorenal syndrome "
                   "develops silently)"],
        investigations=[
            InvestigationProfile("Bloods (FBC, U&E, LFT, clotting, "
                                 "ammonia if available), ascitic tap "
                                 "for cell count and culture, "
                                 "infection screen", "decompensation "
                                 "is usually a precipitated event — "
                                 "find the precipitant", 0.90, 0.85,
                                 "NICE NG50 cirrhosis"),
        ],
        management_first_line="Decompensation is a hospital event: "
                              "admit or same-day specialist review. "
                              "Encephalopathy — lactulose and find "
                              "the precipitant; ascites — salt "
                              "restriction and spironolactone AFTER "
                              "the SBP tap; NEVER NSAIDs, never "
                              "nephrotoxics, check every drug "
                              "against the liver. Alcohol aetiology "
                              "needs withdrawal cover started "
                              "prophylactically.",
        referral_tier="urgent",
        safety_net="Drowsiness deepening, vomiting blood, black "
                   "stools, fever or worsening abdominal pain — "
                   "emergency. Any new confusion in a cirrhotic "
                   "patient is same-day medicine, never 'wait and "
                   "see'.",
        source="NICE NG50 cirrhosis in over 16s",
    ),
    ConditionProfile(
        condition_id="ckd_advanced",
        name="Advanced chronic kidney disease (stage 4-5)",
        category="urology_kidney",
        prevalence_per_consult=0.003,
        symptoms=[
            SymptomFrequency("known_ckd", 0.95, 0.92),
            SymptomFrequency("fatigue", 0.60, 0.10),
            SymptomFrequency("uraemic_itch", 0.40, 0.70),
            SymptomFrequency("nausea", 0.40, 0.20),
            SymptomFrequency("ankle_swelling", 0.40, 0.20),
        ],
        discriminators=["the patient KNOWS they have CKD — the task "
                        "is recognising progression and the drug "
                        "dangers, not diagnosing it",
                        "uraemia: itch, nausea, anorexia, "
                        "restless legs, confusion late",
                        "frequency/nocturia out of proportion — "
                        "concentrating ability fails early",
                        "each new symptom in CKD-4/5 has a "
                        "drug-cause first hypothesis: the "
                        "prescribing-safety tables carry the renal "
                        "flags (metformin, NSAIDs, ACE dose, "
                        "DOACs, digoxin, lithium)"],
        red_flags=["reduced urine output or anuria — emergency",
                   "breathlessness at rest (fluid overload/"
                   "pulmonary oedema) — emergency",
                   "palpitations or muscle weakness — "
                   "hyperkalaemia: same-day bloods and ECG",
                   "confusion or seizures — severe uraemia",
                   "missed dialysis sessions or rapid eGFR fall"],
        investigations=[
            InvestigationProfile("eGFR + potassium + bicarbonate + "
                                 "Hb; urine ACR; renal ultrasound if "
                                 "obstruction possible", "the "
                                 "number that changes management is "
                                 "today's potassium", 0.95, 0.90,
                                 "NICE NG203 CKD"),
        ],
        management_first_line="Stage-appropriate: sick-day rules "
                              "(SADMANS — suspend NSAIDs, ACE, "
                              "diuretics, metformin, SGLT2i during "
                              "any dehydrating illness), anaemia "
                              "check, renal dietitian, bone "
                              "mineral (calcium/phosphate/PTH), "
                              "vaccinations, and low-clearance/"
                              "dialysis planning conversations "
                              "BEFORE the crash landing. Every "
                              "prescription crosses the renal "
                              "check.",
        referral_tier="routine",
        safety_net="Passing much less urine, breathless lying flat, "
                   "palpitations or muscle weakness — same-day "
                   "(fluid overload and potassium). Rising itch and "
                   "nausea with drowsiness — urgent review.",
        source="NICE NG203 chronic kidney disease",
    ),
    ConditionProfile(
        condition_id="inguinal_hernia",
        name="Inguinal hernia",
        category="gastrointestinal",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("groin_bulge_reducible", 0.90, 0.92),
            SymptomFrequency("lifting_ache", 0.50, 0.45),
        ],
        discriminators=["lump appears on standing/coughing, "
                        "disappears lying down, with an ache after "
                        "lifting — the cough impulse completes it",
                        "femoral hernia: below and lateral to the "
                        "pubic tubercle, more dangerous in women, "
                        "irreducible more often",
                        "lymph node: does not reduce, no cough "
                        "impulse, often tender",
                        "varicocele/hydrocele: scrotal, "
                        "transilluminates or bag-of-worms",
                        "incarceration vs reducibility is the "
                        "whole operative decision"],
        red_flags=["irreducible, tender, tense lump — especially "
                   "with vomiting or distension: strangulation, "
                   "emergency",
                   "sudden severe pain in a known hernia",
                   "redness over the lump",
                   "a hernia that stops reducing over days"],
        investigations=[
            InvestigationProfile("Clinical diagnosis; ultrasound "
                                 "only for doubt or femoral/"
                                 "obesity", "the examination IS the "
                                 "test", 0.90, 0.90, "NICE CKS hernia"),
        ],
        management_first_line="Examine standing and lying, cough "
                              "impulse, reducibility. Reducible and "
                              "asymptomatic: surgical opinion, "
                              "watchful waiting is legitimate. "
                              "Never truss long-term. Advise on "
                              "strangulation symptoms in words the "
                              "patient keeps. Referral is routine — "
                              "but strangulation is 999.",
        referral_tier="routine",
        safety_net="The lump becomes tender, hard, will not push "
                   "back, or vomiting and tummy pain start — "
                   "emergency, do not eat or drink. A lump that "
                   "changes character needs same-day review.",
        source="NICE CKS groin hernia; RCS commissioning guide",
    ),
    # ================= 7.3 eyes / ENT =================
    ConditionProfile(
        condition_id="wet_amd",
        name="Wet age-related macular degeneration",
        category="ent_eye",
        prevalence_per_consult=0.001,
        symptoms=[
            SymptomFrequency("distorted_straight_lines", 0.80, 0.90),
            SymptomFrequency("reading_difficulty_central", 0.60, 0.55),
        ],
        discriminators=["straight lines wobbly (metamorphopsia) in "
                        "ONE eye — cover each eye separately when "
                        "testing; central grey patch, reading "
                        "difficulty, preserved peripheral vision",
                        "dry AMD: gradual years-long central "
                        "fading, no distortion — monitoring and "
                        "aids, not injections",
                        "the Amsler grid at the desk separates the "
                        "eyes and the diagnoses",
                        "central visual loss with distortion = wet "
                        "conversion until the retina says otherwise"],
        red_flags=["sudden distortion, grey patch or central loss "
                   "— wet AMD treatment window: anti-VEGF "
                   "injections work best within WEEKS of onset",
                   "sudden total blackout of one eye like a "
                   "curtain — retinal artery occlusion: emergency",
                   "new floaters/flashes/field shadow — retinal "
                   "detachment: emergency",
                   "distortion with pain and red eye — other "
                   "retinal disease"],
        investigations=[
            InvestigationProfile("Same-day/urgent slit-lamp and "
                                 "OCT at ophthalmology (Amsler "
                                 "grid in the meantime)", "OCT sees "
                                 "the fluid that decides "
                                 "injection vs observation",
                                 0.95, 0.90, "NICE NG82 AMD"),
        ],
        management_first_line="Urgent (same-week, sooner if "
                              "possible) ophthalmology referral "
                              "with the onset DATE documented — "
                              "anti-VEGF injections preserve sight "
                              "in eyes that present early, and the "
                              "treatment window is measured in "
                              "weeks. Smoking cessation, and "
                              "discuss AREDS2-type supplementation "
                              "for dry disease.",
        referral_tier="urgent",
        safety_net="Sudden loss of central vision, a dark curtain, "
                   "or a burst of new floaters and flashing lights "
                   "— same-day eye emergency. Worsening distortion "
                   "week on week — keep the urgent appointment, do "
                   "not wait for it to settle.",
        source="NICE NG82 age-related macular degeneration",
    ),
    ConditionProfile(
        condition_id="sudden_sensorineural_hearing_loss",
        name="Sudden sensorineural hearing loss",
        category="ent_eye",
        prevalence_per_consult=0.0001,
        symptoms=[
            SymptomFrequency("hearing_lost_sudden_unilateral", 0.90, 0.92),
            SymptomFrequency("tinnitus_new", 0.40, 0.30),
        ],
        discriminators=["hearing gone over seconds-to-days in ONE "
                        "ear, often with tinnitus and a blocked "
                        "feeling — the ear canal is NORMAL (this "
                        "is not wax, not infection)",
                        "wax/outer-ear causes: visible on "
                        "otoscopy, removable",
                        "conductive loss after cold/flight: "
                        "middle-ear fluid, insidious not sudden",
                        "with vertigo and/or facial weakness — "
                        "labyrinthitis vs stroke: urgent "
                        "neuro-ENT pathway",
                        "Meniere's: episodic hours-long attacks "
                        "with roaring tinnitus and vertigo, not a "
                        "single permanent loss"],
        red_flags=["sudden unilateral deafness IS the red flag — "
                   "steroids within days (ideally under 2 weeks) "
                   "carry the best recovery odds; idiopathic "
                   "SSNHL is a treatment emergency without being "
                   "a 999",
                   "associated facial palsy, severe vertigo, or "
                   "neurology — urgent imaging for stroke/"
                   "acoustic neuroma",
                   "bilateral sudden loss — autoimmune/other, "
                   "specialist same week",
                   "hearing loss with ear discharge and pain — "
                   "infection pathway instead"],
        investigations=[
            InvestigationProfile("Urgent pure-tone audiometry + "
                                 "ENT review (weber/rinne at the "
                                 "desk distinguishes conductive "
                                 "from sensorineural)", "the "
                                 "tuning fork decides which urgent "
                                 "pathway before audiology "
                                 "confirms", 0.90, 0.85,
                                 "NICE CKS sudden sensorineural "
                                 "hearing loss"),
        ],
        management_first_line="Oral steroids (or intratympanic if "
                              "started late/contraindicated) as "
                              "early as possible — same-day or "
                              "next-day ENT contact, not a routine "
                              "appointment. Document onset time. "
                              "Do NOT diagnose wax or congestion "
                              "without looking and testing — "
                              "'blocked ear' is how SSNHL "
                              "presents and how it gets missed.",
        referral_tier="urgent",
        safety_net="Sudden deafness is never 'just an ear "
                   "infection' until examined — if the canal is "
                   "clean, keep the urgent ENT appointment. New "
                   "facial weakness, severe dizziness or "
                   "neurological symptoms — emergency.",
        source="NICE CKS hearing loss; ENT UK SSNHL guidance",
    ),
    ConditionProfile(
        condition_id="orbital_cellulitis",
        name="Orbital cellulitis",
        category="ent_eye",
        prevalence_per_consult=0.00005,
        symptoms=[
            SymptomFrequency("periorbital_swelling_red", 0.90, 0.75),
            SymptomFrequency("visual_disturbance", 0.30, 0.20),
            SymptomFrequency("painful_eye_movement", 0.50, 0.85),
            SymptomFrequency("fever", 0.50, 0.10),
        ],
        discriminators=["swollen painful RED eye with fever and "
                        "pain ON MOVING the eye — the pain on "
                        "movement and double vision separate "
                        "ORBITAL from simple preseptal cellulitis",
                        "preseptal: lid swelling and redness but "
                        "full eye movements, no double vision, "
                        "usually a stye/scratch origin — oral "
                        "antibiotics",
                        "ORBITAL: proptosis, painful/restricted "
                        "movement, vision change, often sinusitis "
                        "source — admission, IV antibiotics, CT",
                        "the child with periorbital swelling and "
                        "fever after sinusitis is the classic "
                        "presentation"],
        red_flags=["ANY double vision, reduced vision, "
                   "proptosis, painful eye movement or "
                   "ophthalmoplegia — admission for IV antibiotics "
                   "and imaging",
                   "periorbital swelling with fever in a child",
                   "drowsiness, severe headache or neck stiffness "
                   "(intracranial spread) — emergency",
                   "immunocompromise or diabetes — faster "
                   "deterioration"],
        investigations=[
            InvestigationProfile("Urgent CT orbits/sinuses + bloods "
                                 "+ swabs", "maps the abscess and "
                                 "the sinus source before surgery",
                                 0.95, 0.90, "RCS/ENT UK orbital "
                                 "cellulitis guidance"),
        ],
        management_first_line="Admit under joint ENT/ophthalmology: "
                              "IV antibiotics, treat the sinus "
                              "source, ophthalmology review of "
                              "vision and pressures, surgical "
                              "drainage if abscess or "
                              "deterioration. Preseptal disease in "
                              "a well adult with intact vision can "
                              "take oral antibiotics with a clear "
                              "safety net and review at 48 hours.",
        referral_tier="emergency",
        safety_net="Any problem moving the eye, double vision, "
                   "failing vision, spreading redness, drowsiness "
                   "or severe headache — emergency. A red swollen "
                   "eyelid not clearly improving within 48 hours — "
                   "review.",
        source="ENT UK / Royal College position; NICE CKS",
    ),
    # ================= 7.3 sleep / pain / continence =================
    ConditionProfile(
        condition_id="obstructive_sleep_apnoea",
        name="Obstructive sleep apnoea",
        category="respiratory",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("heavy_snoring", 0.85, 0.80),
            SymptomFrequency("daytime_sleepiness", 0.85, 0.80),
            SymptomFrequency("witnessed_apnoeas", 0.50, 0.92),
        ],
        discriminators=["loud snoring + witnessed pauses/gasps + "
                        "daytime sleepiness (Epworth quantifies) — "
                        "the partner's testimony is the "
                        "investigation",
                        "simple snoring: noisy but no pauses, no "
                        "sleepiness, no consequences",
                        "insomnia: can't sleep vs sleeps plenty "
                        "but wakes unrefreshed with micro-arousals",
                        "hypothyroidism, acromegaly and large "
                        "neck circumference raise the odds",
                        "resistant hypertension, AF, nocturia and "
                        "morning headaches travel with it"],
        red_flags=["SLEEPINESS AT THE WHEEL or near-miss RTA — stop "
                   "driving NOW and notify DVLA; this is a "
                   "licence-legal issue, not a comfort issue",
                   "sleepiness operating machinery or supervising "
                   "children alone",
                   "right heart failure signs (oedema, raised JVP) "
                   "from chronic hypoxia",
                   "cardiovascular events before the diagnosis"],
        investigations=[
            InvestigationProfile("STOP-Bang + Epworth scores, then "
                                 "home sleep study / oximetry; "
                                 "specialist polysomnography when "
                                 "complex", "the diagnosis is "
                                 "objective — nobody sleeps "
                                 "normally in a lab the first "
                                 "night", 0.85, 0.85, "NICE "
                                 "TA139 OSAHS; BTS sleep apnoea"),
        ],
        management_first_line="Weight loss where overweight (5-10% "
                              "can halve the apnoea index), alcohol "
                              "and sedatives off at night, sleep "
                              "hygiene, driving advice BEFORE "
                              "treatment, then CPAP with mask "
                              "follow-up (the machine fails at the "
                              "mask, not the pressure). Mandibular "
                              "devices for mild disease or CPAP "
                              "intolerance.",
        referral_tier="routine",
        safety_net="Any sleepiness at the wheel or a near-miss — "
                   "stop driving and tell DVLA, then the sleep "
                   "clinic accelerates the workup. Worsening "
                   "morning headaches, night-time breathlessness "
                   "or leg swelling — review sooner.",
        source="NICE TA139; BTS/TRL sleep apnoea guidance; DVLA "
               "at-a-glance",
    ),
    ConditionProfile(
        condition_id="insomnia_disorder",
        name="Insomnia disorder",
        category="mental_health",
        prevalence_per_consult=0.010,
        symptoms=[
            SymptomFrequency("insomnia_months", 0.90, 0.80),
            SymptomFrequency("night_worry_rumination", 0.60, 0.70),
            SymptomFrequency("daytime_tiredness_insomnia", 0.50, 0.10),
        ],
        discriminators=["at least three nights a week for three "
                        "months, with daytime consequence — the "
                        "definition is duration plus function",
                        "the 3-P model sorts the history: "
                        "predisposing (anxious temperament), "
                        "precipitating (job loss, baby, pain), "
                        "perpetuating (late caffeine, screens, "
                        "naps, compensating in bed) — treat the "
                        "perpetuating loop, it outlives the "
                        "precipitant",
                        "secondary insomnia: pain, nocturia, "
                        "SOB, reflux, restless legs, shift work, "
                        "drugs (steroids, SSRIs, beta-blockers, "
                        "caffeine, alcohol) — the sleep complaint "
                        "is the presenting symptom of those",
                        "mania and depression both distort sleep "
                        "in opposite directions"],
        red_flags=["suicidal ideation or self-neglect — mental "
                   "health crisis pathway",
                   "not sleeping at all night after night with "
                   "energy — screen for mania",
                   "suspected sleep apnoea (snoring, witnessed "
                   "pauses) — different pathway, CBT-i alone will "
                   "not fix it",
                   "insomnia with restless legs/numbness — iron "
                   "and neuropathy screen"],
        investigations=[
            InvestigationProfile("Two-week sleep diary (paper "
                                 "begets honesty); Epworth if "
                                 "apnoea suspected", "the diary "
                                 "exposes the perpetuating loop "
                                 "faster than any conversation",
                                 0.85, 0.80, "NICE NG207 insomnia; "
                                 "BIS guidance"),
        ],
        management_first_line="CBT for insomnia FIRST LINE — "
                              "sleep restriction, stimulus control "
                              "(bed for sleep and intimacy only), "
                              "no screens/caffeine late, fixed "
                              "rise time. Sleeping tablets "
                              "(z-drugs/benzodiazepines) only "
                              "short-term for acute distress with "
                              "a stop date, never repeated on "
                              "repeat prescription — dependence "
                              "and falls in the elderly are the "
                              "price. Melatonin for over-55s or "
                              "shift pattern problems.",
        referral_tier="routine",
        safety_net="Thoughts of self-harm, or the not-sleeping is "
                   "accompanied by feeling high, fast and "
                   "invincible — same-day mental health review. "
                   "Snoring with pauses in the sleep — apnoea "
                   "pathway, mention it at review.",
        source="NICE NG207 insomnia; BIS/CBT-i guidance",
    ),
    ConditionProfile(
        condition_id="chronic_primary_pain",
        name="Chronic primary pain",
        category="musculoskeletal",
        prevalence_per_consult=0.005,
        symptoms=[
            SymptomFrequency("pain_for_years", 0.90, 0.80),
            SymptomFrequency("nothing_helps_pain", 0.70, 0.60),
            SymptomFrequency("function_lost_pain", 0.50, 0.55),
        ],
        discriminators=["pain >3 months where distress and "
                        "dysfunction are as prominent as the "
                        "sensation — the diagnosis is made after "
                        "the red-flag screen is NEGATIVE and "
                        "remains open to revision",
                        "the biopsychosocial screen: mood, sleep, "
                        "work, beliefs about harm, flare patterns, "
                        "what helped before",
                        "chronic secondary pain: OA, neuropathic, "
                        "cancer-related — treat the driver first",
                        "fibromyalgia-type picture: widespread, "
                        "fatigue, non-restorative sleep, "
                        "tender points",
                        "every chronic pain patient deserves a "
                        " DOCUMENTED one-time red-flag review, "
                        "not a monthly one"],
        red_flags=["weight loss, night pain, fever, trauma, "
                   "cancer history, steroid use, injecting drug "
                   "use, age over 50 new-onset — re-screen when "
                   "the story changes",
                   "new neurology (weakness, numbness, bladder/"
                   "bowel) — cord syndrome pathway",
                   "escalating opioid doses without function "
                   "gain — opioid dependence review",
                   "suicidal ideation in the pain consult — "
                   "common and commonly missed"],
        investigations=[
            InvestigationProfile("Re-examine once, screen ESR/CRP/"
                                 "FBC where inflammatory doubt "
                                 "exists, then STOP testing",
                                 "repeat imaging of an unchanged "
                                 "chronic story finds "
                                 "incidentalomas, not answers",
                                 0.70, 0.70, "NICE NG193 chronic "
                                 "primary pain"),
        ],
        management_first_line="NICE NG193: a shared understanding "
                              "FIRST (pain does not mean damage; "
                              "flare does not mean deterioration). "
                              "Exercise and activity pacing, CBT/"
                              "ACT, sleep and mood treated in "
                              "their own right. AVOID starting "
                              "opioids, gabapentinoids and "
                              "benzodiazepines for chronic primary "
                              "pain — the guideline is explicit; "
                              "taper rather than abandon those "
                              "already on them. Antidepressant "
                              "classes for pain-modulating effect "
                              "where appropriate.",
        referral_tier="routine",
        safety_net="New night pain, weight loss, fevers, weakness "
                   "or bladder/bowel change — same-day review; "
                   "those restart the diagnostic clock. Pain with "
                   "thoughts of not coping — tell someone the "
                   "same day.",
        source="NICE NG193 chronic primary pain",
    ),
    ConditionProfile(
        condition_id="neuropathic_pain",
        name="Neuropathic pain",
        category="neurological",
        prevalence_per_consult=0.004,
        symptoms=[
            SymptomFrequency("burning_shooting_pain", 0.80, 0.85),
            SymptomFrequency("allodynia_clothes", 0.40, 0.88),
        ],
        discriminators=["the WORDS carry the diagnosis: burning, "
                        "shooting, electric, stabbing, ants "
                        "crawling — plus allodynia (clothes, "
                        "bedclothes, breeze hurt)",
                        "shingles-related: dermatomal scar, "
                        "post-herpetic neuralgia",
                        "diabetic: glove-and-stocking, distal, "
                        "symmetric, worse at night",
                        "sciatic/radicular: leg pain below the "
                        "back, dermatomal, worse sitting",
                        "trigeminal: electric face pain in "
                        "seconds-long bursts, trigger zones"],
        red_flags=["new asymmetry or progression — the underlying "
                   "lesion may be structural (imaging)",
                   "weakness, sphincter change — cord pathology",
                   "cancer history or steroid use with new focal "
                   "pain — metastasis until imaged",
                   "unexplained weight loss with neuropathy — "
                   "paraneoplastic/deficiency screen"],
        investigations=[
            InvestigationProfile("Screen for the cause: glucose/"
                                 "HbA1c, B12, TFT, ESR; imaging "
                                 "for focal/progressive patterns",
                                 "neuropathic pain is a symptom "
                                 "with a cause list, not a "
                                 "destination", 0.80, 0.75,
                                 "NICE CG173 neuropathic pain"),
        ],
        management_first_line="Confirm the cause, then NICE CG173 "
                              "ladder: amitriptyline or duloxetine "
                              "or gabapentin/pregabalin (offer ONE "
                              "at a time, review at 2-4 weeks, "
                              "change only on effect not dose "
                              "creep). Topical capsaicin/lignocaine "
                              "for localised disease. Enrol in "
                              "self-management: pacing, sleep, "
                              "mood — pain severity tracks distress "
                              "as much as nerve damage.",
        referral_tier="routine",
        safety_net="New weakness, numbness spreading, or any "
                   "bladder/bowel change — urgent review. Pain "
                   "with a cancer history — same-week imaging "
                   "pathway.",
        source="NICE CG173 neuropathic pain in adults",
    ),
    ConditionProfile(
        condition_id="stress_incontinence",
        name="Stress urinary incontinence",
        category="urology_kidney",
        prevalence_per_consult=0.008,
        symptoms=[
            SymptomFrequency("leak_on_cough", 0.85, 0.90),
            SymptomFrequency("parity_context", 0.50, 0.40),
        ],
        discriminators=["leakage ON cough/sneeze/exercise without "
                        "urgency — the sphincter fails under "
                        "pressure, the bladder does not squeeze",
                        "urge incontinence: sudden need THEN leak, "
                        "frequency, nocturia — overactive bladder, "
                        "different drugs",
                        "mixed: both patterns — treat the "
                        "dominant one first",
                        "overflow: dribbling, hesitancy, palpable "
                        "bladder — retention pathway",
                        "men after prostate surgery: sphincter "
                        "weakness is the mechanism there"],
        red_flags=["new incontinence with back pain, leg weakness "
                   "or saddle numbness — cord/cauda equina: "
                   "emergency",
                   "pain or haematuria with the leakage — "
                   "bladder pathology pathway",
                   "prolapse symptoms (heaviness, bulge)",
                   "constant dribbling after pelvic surgery — "
                   "fistula needs specialist repair"],
        investigations=[
            InvestigationProfile("Bladder diary (3 days) + post-"
                                 "void residual if mixed picture; "
                                 "urinalysis", "the diary "
                                 "separates stress from urge "
                                 "before any drug is chosen",
                                 0.80, 0.80, "NICE NG123 urinary "
                                 "incontinence"),
        ],
        management_first_line="Three months of supervised pelvic "
                              "floor muscle training FIRST LINE "
                              "(minimum 8 contractions x 3/day, "
                              "physio referral if not improving) — "
                              "it cures or improves most, and "
                              "surgery works better on a trained "
                              "floor. Weight loss, smoking "
                              "cessation, treat constipation and "
                              "chronic cough. Duloxetine only if "
                              "surgery declined/contraindicated.",
        referral_tier="routine",
        safety_net="Leakage with new weakness, numbness between "
                   "the legs, or problems controlling the bowels "
                   "too — emergency. Blood in the urine or pain "
                   "with it — urgent review.",
        source="NICE NG123 urinary incontinence and pelvic organ "
               "prolapse",
    ),
]


SYMPTOM_SYNONYMS_PART5: Dict[str, List[str]] = {
    # --- chronic neurology ---
    "progressive_forgetfulness": [
        "getting forgetful", "more forgetful", "become forgetful",
        "forgetting things", "memory is going", "poor memory",
        "memory problems", "memory getting worse", "can't remember things",
        "repeats herself", "repeats himself", "repeating the same questions",
        "asks the same questions", "short-term memory going",
    ],
    "unsafe_forgetting_events": [
        "left the cooker on", "left the stove on", "left the hob on",
        "forgot to turn the cooker off", "left the gas on",
        "left the iron on", "got lost coming home",
        "got lost on the way home", "found wandering",
        "left the bath running", "went out and left the door open",
    ],
    "gradual_decline_over_months": [
        # 7.3: bare 'for months'/'past year' removed — they fire on every
        # chronic complaint there is (the insomnia probe once led with
        # dementia_suspected on this token alone).
        "over the last year", "getting worse slowly",
        "slowly getting worse", "worse over months",
        "progressively worse", "gradual decline",
    ],
    "disorientation_time_place": [
        "confused about the time", "doesn't know what day it is",
        "not sure what day it is", "mixed up day and night",
        "doesn't know where she is", "doesn't know where he is",
    ],
    "functional_decline_iadl": [
        "stopped cooking", "can't manage her finances",
        "not managing at home", "needing help with washing and dressing",
        "neglecting the house", "can't look after himself anymore",
    ],
    "personality_change": [
        "personality has changed", "not herself lately",
        "not himself lately", "behaviour has changed",
    ],
    "first_ever_seizure": [
        "first seizure", "first ever seizure", "first fit",
        "first ever fit", "first convulsion", "never had a seizure before",
        "never had a fit before", "first time i've had a seizure",
        "first time i've had a fit", "seizure for the first time",
    ],
    "recovered_after_seizure": [
        "fully recovered", "back to normal now", "feeling fine now",
        "recovered quickly", "came round quickly",
    ],
    "tongue_bitten": [
        "bit my tongue", "bitten my tongue", "bit the side of my tongue",
        "bitten tongue", "bit her tongue", "bit his tongue",
    ],
    "seizure_incontinence": [
        "wet myself during", "wet myself", "passed urine during the fit",
        "incontinence during",
    ],
    "known_epilepsy": [
        # anchored to ESTABLISHED-USE wording: bare drug names burned us —
        # "started lamotrigine two weeks ago" is a new-drug story (SJS
        # territory), not known epilepsy.
        "i have epilepsy", "known epilepsy", "epilepsy medication",
        "on epilepsy tablets", "epileptic and take", "take carbamazepine",
        "on carbamazepine", "carbamazepine for", "take keppra", "on keppra",
        "keppra for", "take lamotrigine", "on lamotrigine",
        "lamotrigine for", "take sodium valproate", "on sodium valproate",
        "valproate for", "take phenytoin", "on phenytoin", "phenytoin for",
        "take levetiracetam", "on levetiracetam", "levetiracetam for",
        "anti-epileptic", "antiepileptic", "anti epileptic",
        "epilepsy nurse", "under the epilepsy clinic",
    ],
    "breakthrough_pattern": [
        "breakthrough seizure", "first one in two years",
        "first fit in years", "usually well controlled",
        "hadn't had one in", "first seizure in years",
        "seizures coming back", "first fit since",
    ],
    "tremor_one_side": [
        "tremor in my right hand", "tremor in my left hand",
        "tremor in one hand", "tremor in my hand", "shaking in one hand",
        "tremor at rest", "right hand tremor", "left hand tremor",
        "tremor in my right", "tremor in my left",
    ],
    "smaller_handwriting": [
        "smaller handwriting", "handwriting has got smaller",
        "writing has got smaller", "handwriting is getting smaller",
        "handwriting smaller",
    ],
    "slowed_walking": [
        "walking has slowed", "walking slower", "walk has slowed",
        "slower walking", "small shuffling steps", "shuffling",
        "gait has slowed", "taking smaller steps",
    ],
    "limb_stiffness": [
        "stiffness in my arm", "arm feels stiff", "stiff arm",
        "stiffness in my leg", "legs feel stiff", "stiff shoulder",
        "arm has become stiff",
    ],
    "reduced_arm_swing": [
        "arm doesn't swing", "not swinging his arm", "one arm not swinging",
        "arm not swinging",
    ],
    "reduced_smell": [
        "lost my sense of smell", "can't smell anything", "no sense of smell",
        "lost sense of smell",
    ],
    "severe_unilateral_orbital_pain": [
        "severe one-sided headache", "one-sided headache",
        "pain behind one eye", "severe pain around one eye",
        "one sided headache", "pain in one eye with the headache",
    ],
    "attacks_same_time_daily": [
        "every night at the same time", "same time every night",
        "every night like clockwork", "wakes me at the same time",
        "every day at the same time", "like clockwork every",
    ],
    "autonomic_eye_watering": [
        "eye watering", "watery eye", "eye is watering", "watering eye",
        "one eye watering", "eye red and watering", "drooping eyelid",
        "nose running with the headache", "eye bloodshot",
    ],
    "restlessness_during_attack": [
        "pacing up and down", "can't sit still", "rocking",
        "have to move around",
    ],
    "short_attack_duration": [
        "lasting half an hour", "lasts 30 minutes", "lasts an hour",
        "lasts about 15 minutes", "twenty minutes",
        "attacks last less than an hour",
    ],
    "episodic_neurological_symptoms": [
        "episodes of numbness", "two separate episodes",
        "episodes of blurred vision", "symptoms that come and go",
        "coming and going over months", "episode lasting weeks",
        "separate episodes", "relapsing symptoms", "two episodes of",
    ],
    "unilateral_blurred_vision_history": [
        "blurred vision in one eye", "vision went blurry in one eye",
        "one eye went blurry", "painful eye movement",
        "colours looked washed out", "grey patch in one eye",
    ],
    "bilateral_foot_numbness": [
        "numbness in both feet", "numb feet", "both feet numb",
        "pins and needles in both feet", "numbness in my feet",
        "numbness in both legs",
    ],
    "heat_sensitivity": [
        "worse after a hot bath", "worse in the heat",
        "hot bath makes it worse", "warm weather makes it worse",
    ],
    "burning_feet": [
        "burning feet", "burning in both feet", "burning sensation in my feet",
        "feet burn", "burning pain in my feet", "hot feet at night",
        "burning and pins and needles", "burning and tingling in my feet",
        "burning and numbness in my feet", "burning in my feet",
    ],
    "tingling_both_feet": [
        "pins and needles in both feet", "tingling in both feet",
        "tingling in my feet", "numbness in both feet", "numb feet",
        "both feet tingle", "pins and needles in my feet",
    ],
    "worse_at_night": [
        "worse at night", "bad at night", "every night",
        "worse in the evening", "keeps me awake at night",
    ],
    "long_standing_diabetes": [
        "diabetic for twenty years", "diabetic for years",
        "diabetes for twenty years", "diabetes for years",
        "diabetic for thirty years", "had diabetes for",
    ],
    # --- status epilepticus token re-anchoring (Task 7.1 fix) ---
    "seizure_not_stopping": [
        "seizure not stopping", "seizures not stopping", "still fitting",
        "still having seizures", "seizure won't stop",
        "seizure hasn't stopped", "fit not stopping", "fits not stopping",
        "seizing continuously", "seizure going on for",
        "one seizure after another", "seizure after seizure",
        "convulsion lasting more than", "still convulsing",
        "won't stop fitting",
    ],
    "repeated_seizures_no_recovery": [
        "seizures without waking", "not waking up between",
        "not waking between seizures",
        "repeated seizures without recovery", "fits without recovering",
        "one after another without waking",
    ],
    # --- mental health ---
    "decreased_need_for_sleep": [
        "haven't slept for three nights", "haven't slept for days",
        "haven't slept in days", "havent slept for days",
        "not sleeping at all", "days without sleep", "days without sleeping",
        "sleeping two hours a night", "only need three hours sleep",
        "no sleep for three nights", "sleeping a couple of hours",
        "not slept for three", "haven't slept all week",
    ],
    "pressured_speech": [
        "talking fast", "talking quickly", "racing speech",
        "can't stop talking", "words tumbling out", "talks non-stop",
        "talks nonstop",
    ],
    "grandiosity": [
        "feeling invincible", "feel invincible", "on top of the world",
        "special powers", "chosen for a mission", "can do anything",
        "untouchable", "destined for greatness",
    ],
    "reckless_spending": [
        "spending money wildly", "spending sprees", "maxed out credit cards",
        "gambling everything", "spending thousands", "wild spending",
        "spending money i don't have", "bought a car on a whim",
    ],
    "elevated_energy": [
        "full of energy", "bursting with energy", "so much energy",
        "racing thoughts", "mind racing", "wired",
    ],
    "compulsive_checking": [
        "checking the locks", "check things over and over",
        "checking the stove repeatedly", "check the door repeatedly",
        "keep checking", "checking for an hour",
    ],
    "repetitive_washing": [
        "washing my hands fifty times", "washing my hands over and over",
        "washing hands repeatedly", "excessive hand washing",
        "washing my hands twenty times", "washing my hands raw",
        "can't stop washing",
    ],
    "recognised_irrational": [
        "know it's silly", "know it's irrational",
        "know it doesn't make sense", "i know it's ridiculous",
        "can't stop even though", "knows it's silly",
    ],
    "intrusive_obsessive_thoughts": [
        "same thought keeps coming", "can't get the thought out",
        "intrusive thoughts", "counting everything",
        "arranging things symmetrically", "everything must be even",
    ],
    "trauma_exposure_reference": [
        "since the car crash", "since the accident", "since the attack",
        "after the crash", "since the assault", "since i was robbed",
        "after the fire", "since combat", "since afghanistan",
        "since the explosion", "since the crash",
    ],
    "flashbacks": [
        "flashbacks", "flashback", "reliving the accident", "reliving it",
        "recurring memories of the", "it plays over and over",
    ],
    "trauma_nightmares": [
        "nightmares since", "nightmares about the crash",
        "nightmares about what happened", "bad dreams about the",
        "nightmares and flashbacks", "nightmares every night",
    ],
    "hypervigilance": [
        "jumping at noises", "jumping at loud noises", "on edge all the time",
        "constantly on guard", "startle easily", "startled by",
        "can't relax since", "hyperaware of everything",
    ],
    "avoidance_trauma_cues": [
        "avoiding the motorway", "avoid the motorway", "avoiding driving",
        "won't go near the road", "avoiding anything that reminds",
        "won't talk about what happened", "avoiding the news",
        "not driving since",
    ],
    "rapid_mood_swings_hours": [
        "mood changes within hours", "mood swings several times a day",
        "up and down within hours",
        "fine one minute and in tears the next", "mood flips within",
    ],
    "abandonment_fear": [
        "terrified of being abandoned", "can't be alone",
        "fear of being left", "everyone leaves me",
        "terrified she'll leave me", "cling to relationships",
    ],
    "identity_instability": [
        "don't know who i am", "different person depending",
        "no sense of myself",
    ],
    "intense_inappropriate_anger": [
        "explosive anger", "rage over small things",
        "lose my temper completely", "smash things when angry",
        "rage then fine",
    ],
    "chronic_emptiness": [
        "feeling empty inside", "empty all the time", "chronic emptiness",
        "feel hollow",
    ],
    "self_harm_history_token": [
        "history of self-harm", "cut myself in the past",
        "previous overdoses", "self-harmed before", "history of overdoses",
    ],
    "self_induced_vomiting": [
        "making myself sick", "making myself throw up",
        "being sick after meals", "vomiting after eating",
        "sick after meals", "bring food back up", "purging",
        "make myself vomit", "throw up after eating",
    ],
    "binge_eating_episodes": [
        "eat huge amounts", "eating huge amounts", "binge", "bingeing",
        "binging", "eat loads then", "thousands of calories in one go",
        "eat and eat",
    ],
    "compensatory_behaviours": [
        "laxatives", "diuretics to lose", "exercising to compensate",
        "exercise for hours after eating",
    ],
    "postnatal_period_marker": [
        "since the baby was born", "four weeks since the baby",
        "weeks since the baby", "since the birth", "after the birth",
        "postnatal", "postpartum", "since having my baby",
        "after having my baby", "months after the baby",
    ],
    "tearfulness_postnatal": [
        "tearful all the time", "tearful", "can't stop crying",
        "crying all the time", "crying for no reason", "in tears constantly",
    ],
    "intrusive_harm_thoughts": [
        "thoughts of harming the baby", "thoughts about harming the baby",
        "scary thoughts about the baby",
        "frightening thoughts about harming", "intrusive thoughts about the baby",
        "thoughts of hurting the baby",
    ],
    "insomnia_beyond_baby": [
        "can't sleep even when the baby sleeps",
        "can't sleep even when she sleeps", "awake even when the baby",
        "not sleeping even when the baby sleeps",
    ],
    # --- 7.2 dermatology ---
    "facial_spots": [
        "spotty rash on my face", "spotty face", "spots on my face",
        "face is spotty", "spots on my forehead", "acne on my face",
    ],
    "back_and_chest_spots": [
        "rash on my face and back", "spots on my back",
        "spots on my chest and back", "spots on my chest",
        "acne on my back", "acne on my chest",
    ],
    "greasy_skin": [
        "greasy skin", "oily skin", "skin is greasy", "very oily",
    ],
    "teenage_onset": [
        "since i was a teenager", "since my teens", "teenage spots",
        "started as a teenager", "had them since school",
    ],
    "comedones": [
        "blackheads", "whiteheads", "blackheads and whiteheads",
        "blocked pores",
    ],
    "itchy_weals": [
        "itchy weals", "weals", "wheals", "hives", "nettle rash",
        "welts", "raised itchy patches",
    ],
    "weals_come_and_go": [
        "coming and going", "come and go", "come up then fade",
        "appear then disappear", "move around", "there one day and gone the next",
    ],
    "lip_swelling_angioedema": [
        "lips swelling", "swollen lips", "lip swelling", "eyes swelling shut",
        "angioedema",
    ],
    "family_itch_night": [
        "whole family scratching", "family all itching", "everyone in the house itching",
        "everyone scratching", "my partner has it too", "kids are scratching too",
        "both of us are itching",
    ],
    "burrow_tracks": [
        "burrow tracks", "burrows", "little tracks", "thin wavy lines",
    ],
    "finger_web_itch": [
        "between the fingers", "in the finger webs", "webs of my fingers",
        "itchy fingers",
    ],
    "ring_shaped_rash": [
        "ring-shaped", "ring shaped", "ringworm", "circular rash",
        "ring like rash", "expanding ring", "a ring on my skin",
    ],
    "athletes_foot": [
        "between the toes", "athlete's foot", "athletes foot",
        "itchy feet", "peeling between the toes", "macerated toes",
    ],
    "groin_itch": [
        "in the groin", "itchy groin", "groin rash", "jock itch",
        "rash in the groin",
    ],
    "scaly_ring_edge": [
        "scaly edge", "flaky ring", "raised edge", "active edge",
        "clearing in the middle", "clear centre",
    ],
    # 7.2: anchored to 'a week after starting antibiotics'-style phrasing.
    # Bare 'started <drug>' must NOT match — that is SJS/TEN language.
    "new_drug_rash_week": [
        "a week after starting antibiotics", "week after starting",
        "days after starting", "after starting antibiotics",
        "since starting the tablets", "new medication and a rash",
        "rash since the new tablets", "a week after the new medicine",
    ],
    "blistered_rash_benign": [
        "blistered rash on my arms", "blisters on my arms",
        "blistering on my arms", "blistered rash on my legs",
        "blisters on my hands",
    ],
    "ankle_grazing_sore": [
        "grazing sore above the ankle", "sore above the ankle",
        "ulcer above the ankle", "grazing sore on my ankle",
        "open sore on my ankle", "breakdown above the ankle",
    ],
    "varicose_swollen_legs": [
        "varicose legs", "varicose veins", "swollen ankles",
        "legs are swollen", "varicose eczema",
    ],
    "never_heals": [
        "that never heals", "never heals", "won't heal",
        "not healing for months", "hasn't healed for", "months and not healed",
    ],
    "haemosiderin_staining": [
        "brown staining", "dark staining", "skin discolouration",
        "discoloured skin", "purple brown skin",
    ],
    "eyebrow_nasal_flaking": [
        "in my eyebrows", "eyebrows are flaky", "around my nose",
        "nasolabial", "flaky rash in the eyebrows", "flaking around the nose",
        "red flaky nose",
    ],
    "scalp_flaking_dandruff": [
        "dandruff", "flaky scalp", "scaly scalp", "dry flaky scalp",
    ],
    # --- 7.2 women's health ---
    "periods_stopped_year": [
        "periods stopped a year ago", "periods stopped",
        "no periods for a year", "last period a year ago",
        "not had a period for over a year", "periods stopped fourteen months",
    ],
    "hot_flushes": [
        "hot flushes", "hot flashes", "flushes", "flushing and sweating",
        "burning up at night", "sudden heat all over",
    ],
    "concentration_foggy": [
        "hard to concentrate", "can't concentrate", "brain fog",
        "foggy", "forgetful and fuzzy", "can't think straight",
    ],
    "vaginal_dryness": [
        "vaginal dryness", "dry down below", "sore during sex",
        "dryness making sex painful",
    ],
    "periods_irregular_transition": [
        "periods are irregular", "irregular periods", "periods changing",
        "skipped a period", "periods heavier than they used to be",
        "cycles all over the place", "some months i miss it",
    ],
    "sleep_mood_perimeno": [
        "not sleeping well and irritable", "mood all over the place",
        "tearful and not sleeping", "irritable and low",
    ],
    "trying_conceive_years": [
        "trying for a baby", "trying to conceive", "trying to get pregnant",
        "trying for a baby for two years", "trying for over a year",
        "trying for months", "not conceiving",
    ],
    "periods_infrequent": [
        "periods come every three months", "periods every three months",
        "periods every few months", "periods every two months",
        "only three or four periods a year", "periods far apart",
    ],
    "hirsutism": [
        "hairs on my chin", "hair on my chin", "hairy face",
        "excess hair", "hirsutism", "hair on my lip", "shaving my face",
    ],
    "weight_gain_pcos": [
        "put on weight", "weight gain", "gaining weight",
    ],
    "acne_pcos": [
        "acne and irregular periods", "spots and irregular periods",
    ],
    "period_pain_cyclical": [
        "periods are agony", "period pain", "painful periods",
        "agonising periods", "period cramps", "periods are agony every month",
        "bad period pain", "cramps every month",
    ],
    "period_pain_first_day": [
        "first day especially", "worst on the first day",
        "first day of my period", "first two days are the worst",
    ],
    # --- 7.2 men's health ---
    "ed_difficulty_months": [
        "difficulty getting erections", "difficulty getting an erection",
        "can't get an erection", "erection problems",
        "trouble keeping an erection", "losing erections",
        "problems with erections", "not getting hard",
    ],
    "morning_erections_preserved": [
        "still get early morning erections", "morning erections",
        "erections in the morning", "still wake with an erection",
    ],
    "incomplete_emptying": [
        "bladder doesn't feel empty", "never feels empty",
        "dribbles at the end", "still feels full after",
    ],
    # 7.2: testicular-lump language must carry its location with it —
    # bare 'hard lump' fires on every breast and neck lump story.
    "testicular_hard_lump": [
        "hard lump in my testicle", "hard lump in one testicle",
        "lump on my testicle", "lump in the testicle", "testicular lump",
        "testicle is hard", "hard area in the testicle",
    ],
    "testicular_ache_chronic": [
        "dull ache in one testicle", "dull ache in my testicle",
        "testicle aches", "aching testicle for weeks", "aching testicle for months",
        "nagging ache in the testicle",
    ],
    "deep_pelvic_pain_male": [
        "deep pelvic ache", "deep pelvic pain", "perineal pain",
        "pain between the legs", "aching prostate", "pelvic ache",
        "deep ache between my legs",
    ],
    "low_libido": [
        "low libido", "lost interest in sex", "no sex drive",
        "not interested in sex",
    ],
    # --- 7.3 chronic GI / hepatology / renal ---
    "bowel_freq_reduced": [
        "haven't opened my bowels", "not opened my bowels for",
        "haven't had a poo for", "haven't had a bowel movement",
        "days since i opened my bowels", "can't open my bowels",
        "not been to the toilet for days", "no bowel action for",
    ],
    "hard_stools_straining": [
        "hard stools", "straining", "rabbit droppings",
        "pebble stools", "hard to pass",
    ],
    "tummy_discomfort_constipation": [
        "tummy is uncomfortable", "uncomfortable tummy",
        "tummy feels blocked", "tender bloated tummy",
    ],
    "crampy_abdominal_pain_months": [
        "crampy tummy pain", "cramping abdominal pain",
        "colicky tummy pain", "crampy abdominal pain",
    ],
    "chronic_diarrhoea_months": [
        "diarrhoea for months", "diarrhea for months",
        "loose stools for months", "diarrhoea for weeks",
        "loose stools for weeks", "running to the toilet for months",
    ],
    "perianal_disease": [
        "perianal", "skin tags around the anus", "fistula",
        "abscess near the anus", "discharge from the back passage",
    ],
    "bloody_diarrhoea_chronic": [
        "diarrhoea with blood", "blood in the diarrhoea",
        "bloody diarrhoea", "blood and mucous", "blood and mucus",
        "bloody stools with diarrhoea", "diarrhoea with blood and mucous",
    ],
    "mucous_rectal_passage": [
        "mucous", "mucus with", "slime in the motions",
        "mucus in the stool",
    ],
    "nocturnal_diarrhoea": [
        "waking me at night", "waking me from sleep to go",
        "diarrhoea at night", "up in the night with diarrhoea",
        "night-time diarrhoea",
    ],
    "bowel_urgency": [
        "rushing to the toilet", "can't hold my bowels",
        "urgency to open my bowels", "accidents if i don't go",
        "desperate to open my bowels",
    ],
    "wheat_triggered_bloating": [
        "every time i eat bread", "after bread", "when i eat bread",
        "bread or pasta", "when i eat pasta", "after eating wheat",
        "bread makes me", "wheat sets me off",
    ],
    "known_cirrhosis": [
        "has cirrhosis", "cirrhosis", "liver cirrhosis",
        "known liver disease", "liver disease", "he's a drinker with a liver problem",
    ],
    "ascites_swelling": [
        "tummy is swelling", "swelling of the tummy",
        "fluid in the tummy", "ascites", "tummy getting bigger",
        "belly is swelling",
    ],
    "known_ckd": [
        "kidney disease", "chronic kidney disease",
        "stage four", "stage 4 ckd", "ckd stage", "renal failure",
        "kidney failure", "ckd",
    ],
    "uraemic_itch": [
        "itchy skin", "itching all over", "itchy all over",
        "skin itch",
    ],
    "groin_bulge_reducible": [
        "bulge in my groin", "lump in the groin that comes and goes",
        "groin lump that comes and goes", "lump in my groin",
        "swelling in the groin comes and goes",
    ],
    "lifting_ache": [
        "aches after lifting", "after lifting", "after carrying",
        "worse after lifting", "heavy lifting",
    ],
    # --- 7.3 eyes / ENT ---
    "distorted_straight_lines": [
        "straight lines look wobbly", "wavy lines",
        "lines look bent", "straight lines are wavy",
        "door frames look bent", "distorted lines",
        "lines are distorted",
    ],
    "reading_difficulty_central": [
        "reading is hard", "can't read the small print",
        "central grey patch", "grey patch in the middle",
        "struggling to read", "words jump about",
    ],
    "hearing_lost_sudden_unilateral": [
        "lost the hearing in my", "hearing gone overnight",
        "woke up deaf", "hearing went suddenly",
        "deaf in one ear", "lost the hearing overnight",
        "sudden hearing loss", "hearing disappeared",
    ],
    "tinnitus_new": [
        "ringing in my ear", "buzzing in the ear",
        "new ringing", "roaring in the ear",
    ],
    "periorbital_swelling_red": [
        "swollen red painful eye", "eyelid swollen and red",
        "around the eyelid", "eye is swollen and red",
        "swollen painful eyelid", "red swollen eye",
        "eyelid is red and swollen",
    ],
    "painful_eye_movement": [
        "pain when i move my eye", "hurts to move my eye",
        "pain moving the eye", "painful to look around",
        "hurts to look around",
    ],
    # --- 7.3 sleep / pain / continence ---
    "heavy_snoring": [
        "snoring terribly", "snoring badly", "snores loudly",
        "heavy snoring", "terrible snoring", "snoring loudly",
        "snores terribly",
    ],
    "daytime_sleepiness": [
        "exhausted in the day", "falling asleep in the day",
        "falling asleep at the wheel", "dozing in the day",
        "sleepy all day", "falling asleep at work",
        "fighting sleep during the day",
    ],
    "witnessed_apnoeas": [
        "stops breathing in his sleep", "stops breathing in her sleep",
        "gasps in his sleep", "gasps in her sleep",
        "witnessed him stop breathing", "wakes up gasping",
    ],
    "insomnia_months": [
        "can't sleep at all", "can't get to sleep", "lying awake",
        "waking at 3am", "not sleeping properly", "can't stay asleep",
        "hours awake at night",
    ],
    "night_worry_rumination": [
        "worrying about work", "mind racing at night",
        "can't switch off", "worrying at night",
        "thoughts going round at night",
    ],
    "daytime_tiredness_insomnia": [
        "tired in the day from not sleeping", "wrecked in the mornings",
    ],
    "pain_for_years": [
        "pain for years", "in pain every day for years",
        "for two years in pain", "pain every day for",
        "years of pain",
    ],
    "nothing_helps_pain": [
        "nothing helps", "no painkiller touches it",
        "tried everything", "nothing takes it away",
        "nothing helps any more",
    ],
    "function_lost_pain": [
        "can't work", "can't work any more", "can't work anymore",
        "stopped working because of the pain", "had to give up work",
    ],
    "burning_shooting_pain": [
        "burning pain", "shooting pain", "electric shocks",
        "burning stabbing", "stabbing burning", "like electric",
        "like ants crawling", "electric shock pains",
    ],
    "allodynia_clothes": [
        "even clothes hurt", "can't bear the bedclothes",
        "even a sheet hurts", "clothes brushing against it hurts",
    ],
    "leak_on_cough": [
        "leaking urine when i cough", "leak when i sneeze",
        "wet myself when i", "leaking when i exercise",
        "leak when i cough", "when i laugh i leak",
        "leak urine when i sneeze",
    ],
    "parity_context": [
        "had three children", "after three children",
        "had four children", "since having children",
        "after my children", "had two children",
    ],
}
