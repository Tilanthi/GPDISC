---
title: "GPDISC User Manual"
date: "3 September 2026"
---

**General Practice Discovery and Intelligence System for Consultation**

**Version 1.1.0 — PRIVATE AND LOCAL, FOR PERSONAL USE**

> **Privacy first.** Everything you ask GPDISC, and every record it keeps, stays on this computer. Nothing is sent to any external service or website — no cloud, no accounts, no transmission of any kind.

# 1. Purpose

GPDISC — the **G**eneral **P**ractice **D**iscovery and **I**ntelligence **S**ystem for **C**onsultation — is a private, GP-led consultation and second-opinion system that lives entirely on this computer. You describe a problem in ordinary words, the way you would tell your doctor, and GPDISC writes back a structured consultation record: a ranked list of the conditions that best explain what you told it, the dangerous diagnoses it refuses to miss, the questions a doctor would ask next, the tests that would tell the possibilities apart, and clear advice on how urgently to seek help.

**How it thinks.** GPDISC never offers a single confident answer. Each reply is built the way a careful clinician thinks:

- **A differential diagnosis** — the conditions that could explain your story, ranked, so you can see the reasoning rather than a verdict.
- **A must-not-miss list** — the serious possibilities it is deliberately keeping on the table even when they are unlikely.
- **Questions to ask next** — the few pieces of information that would most change the answer.
- **A safety net** — what to watch for at home, what should change the plan, and how quickly.
- **Honest uncertainty** — when the story does not point anywhere yet, GPDISC says so plainly ("I don't know yet — describe more or see a clinician") instead of guessing.

**The privacy commitment.** GPDISC holds its records — questions, consultations, notes — in local storage on this machine only. There is no external transmission, no telemetry, and no account anywhere. This is what makes it suitable for the most personal questions.

**What GPDISC is not.** It is not a doctor, and it does not replace one. It is not for emergencies: in an emergency, call 999 (or 911) first and ask questions later. And it is not a data feed to anyone — nothing you type leaves this computer.

# 2. How to use GPDISC

## Asking your question

GPDISC works in **plain natural language only**. There are no commands, no special syntax and no codes to learn. You simply type what you would say to your doctor, in your own words, on the consultation screen — opened from GPDISC's dashboard on this computer. The answer appears as a consultation record like the ones shown in the examples section of this manual.

A few habits make the answers much better:

- **Say who the question is about** — the person's age, and their sex where it matters. "My 3 year old…" and "I'm 66…" both steer the reasoning immediately.
- **Say how long, and how bad** — "for 40 minutes", "for three months", "worst pain I've ever had".
- **Say what makes it better or worse** — "it comes on climbing stairs and goes when I rest" is worth a dozen vague words.
- **List current medicines and other conditions** — especially for questions about tablets, dizziness, confusion or tiredness.
- **Describe tests and results in plain words** — "the ECG shows ST elevation in leads II, III and aVF" or "my kidney blood test is poor" is all GPDISC needs.
- **Ask about someone else if you need to** — "my mother is 79 and…" works exactly as well as asking for yourself.

You can ask about symptoms, medicines and interactions, travel plans, prevention and screening, test results you have been given, and the care of someone nearing the end of life.

## Reading the reply

Every reply is a consultation record with the same sections, so it quickly becomes familiar:

- **Presenting complaint** — your question, restated as a doctor would file it.
- **Level of concern** — the bottom line: self-care, routine, urgent, or emergency, and where to go (999, same-day review, or a routine appointment).
- **Differential** — the ranked conditions that explain your story.
- **Must-not-miss** — the serious possibilities being deliberately kept in play.
- **Ask next** — the questions whose answers would most change the picture.
- **Investigations** — the tests that would separate the possibilities.
- **Treatment** and **Referral** — what to do and where to go.
- **Safety net** — what to watch for and what should bring you back sooner.
- **Ruleset** — which country's rules the advice ran under (GPDISC's detailed rules are UK-based; it says so when that matters).
- **Uncertainty** and **Validation** — GPDISC's honest statement of what it does not yet know, and its check of its own answer for consistency before showing it to you.

**Privacy, again, because it matters:** the conversation you have just had stays on this computer. All records remain local; nothing is sent to any external service or website.

# 3. What GPDISC covers

GPDISC is deliberately broad — a general practitioner sees everything — with specialists called on when a case touches their field. In outline:

- **Medical specialties** — cardiology (ECGs, chest pain, blood pressure, heart failure); epilepsy and neurology (seizures, headaches, nerve disease); general practice (the whole front door of medicine); orthopaedics (joints, fractures, back pain); pharmacology (medicines, interactions, dosing).
- **The consultant panel** — oncology, paediatrics, psychiatry and palliative medicine join the discussion when a case implicates them.
- **Emergency and urgent care** — trauma and burns, poisoning and overdose, obstetric emergencies, paediatric emergencies, and post-exposure prophylaxis (animal bites, needlestick injuries).
- **The everyday clinic** — skin problems, women's and men's health, digestion, eyes and ENT, sleep, and chronic pain.
- **Long-term conditions and older people** — several illnesses at once, whole-patient medicines review, and memory problems.
- **Mental health** — low mood and anxiety through to severe mental illness, including around childbirth.
- **Children and safeguarding** — childhood illness, recognition of non-accidental injury, and protection frameworks.
- **Travel and tropical medicine** — advice before travel, malaria, and fever after returning.
- **Prevention and screening** — vaccinations, health checks and screening programmes.
- **Sexual health** — contraception eligibility and infection testing.
- **UK practice rules** — urgent suspected-cancer referral, driving rules after illness, capacity, antibiotics, high-risk medicines, fit notes.
- **Interpreting tests** — ECGs, blood gases, spinal fluid, urine, lung function, joint fluid, and culture results.
- **End-of-life care** — symptom control, planning ahead, and support for families.
- **Anywhere in the world** — global and humanitarian care: refugee health, remote and resource-limited settings.
- **The scientific foundation** — the biology underneath it all: molecular biology, genetics, biochemistry, physiology and more.

# 4. Twenty examples

Every answer below is a real, unedited GPDISC reply, captured on the day this manual was published. Nothing has been reworded or corrected; where a reply was longer than the page allows, it ends with a line of three dots. The questions are numbered, with the exact words used, followed by the reply exactly as it appeared.

**1. I have had chest tightness for 40 minutes and I am sweating**

```text
Presenting complaint: I have had chest tightness for 40 minutes and I am sweating
Problem representation: 3 discriminating features extracted: chest_pain, sweating, chest_tightness
Differential:
  - Acute coronary syndrome (ST-elevation MI) (score 0.39)
  - Acute coronary syndrome (non-ST-elevation) (score 0.33)
  - Stable angina (score 0.20)
  - Acute asthma exacerbation (score 0.14)
  - Hypoglycaemia (score 0.11)
Must-not-miss (retained):
  ! Aortic dissection
  ! Acute asthma exacerbation
  ! Lung cancer
  ! Hypoglycaemia
  ! Amoebic liver abscess
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
Ask next: persistent >15 min | cardiac risk factors | pain at rest or on minimal exertion
Investigations: 12-lead ECG  -  immediate; diagnostic for STEMI; troponin_hs  -  high-sensitivity troponin; serial; myocardial injury
Treatment: Call 999 (emergency ambulance); aspirin 300 mg chewed unless contraindicated; do not delay transfer.
Referral: emergency department / 999 | escalation raised routine -> emergency: ranked leader Acute coronary syndrome (ST-elevation MI) (emergency)
Safety net: Any chest pain lasting >15 minutes, or with sweating, nausea or breathlessness, is an emergency  -  call 999 immediately.
 ...
```

**2. I have the worst headache of my life, it came on like a thunderclap**

```text
Presenting complaint: I have the worst headache of my life, it came on like a thunderclap
Problem representation: EMERGENCY pattern matched: thunderclap_headache
Differential:
Must-not-miss (retained):
  ! thunderclap headache
Treatment: Do not delay transfer for further history.
Referral: EMERGENCY: Possible subarachnoid haemorrhage  -  emergency assessment now. Call 999 now.
Safety net: Possible subarachnoid haemorrhage  -  emergency assessment now.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Emergency pathway overrides diagnostic refinement.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**3. My 3 year old has a fever and a stiff neck and won't wake up properly**

```text
Presenting complaint: My 3 year old has a fever and a stiff neck and won't wake up properly
Problem representation: 3 discriminating features extracted: fever, neck_stiffness, wont_wake
Differential:
  - Opioid overdose (score 0.30)
  - Meningitis / meningococcal disease (score 0.28)
  - Community-acquired pneumonia (score 0.14)
  - Meningococcal disease (child) (score 0.13)
  - Infective endocarditis (score 0.11)
Must-not-miss (retained):
  ! Infective endocarditis
  ! Community-acquired pneumonia
  ! Pulmonary tuberculosis
  ! Acute appendicitis
  ! Acute cholecystitis
  ! Acute diverticulitis
  ! Acute viral hepatitis
  ! Subarachnoid haemorrhage
  ! Encephalitis
  ! Sepsis
  ! Acute pyelonephritis
  ! Measles
  ! HIV seroconversion illness
  ! Croup (laryngotracheobronchitis)
  ! Meningococcal disease (child)
  ! Giant cell arteritis
  ! Septic arthritis
  ! Pelvic inflammatory disease
  ! Suspected leukaemia (urgent)
  ! Malaria (falciparum)  -  fever after travel
  ! Yellow fever (vaccine-preventable haemorrhagic fever)
  ! Leptospirosis (Weil disease)
  ! Amoebic liver abscess
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Peritonsillar abscess (quinsy)
  ! Epiglottitis (adult)
  ! Epididymitis (STI-associated, <35y)
  ! Infected wound
  ! Serotonin syndrome
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
  ! Puerperal sepsis (post-birth infection)
  ! Neutropenic sepsis
  ! Stevens-Johnson syndrome / toxic epidermal necrolysis
  ! Eczema herpeticum
  ! Necrotising fasciitis
  ! Febrile convulsion (simple)
  ! Prostatitis
  ! Orbital cellulitis
  ! Melioidosis
 ...
```

**4. I've had a sore throat for three days, no fever, just a runny nose**

```text
Presenting complaint: I've had a sore throat for three days, no fever, just a runny nose
Problem representation: 2 discriminating features extracted: sore_throat, rhinorrhoea
Differential:
  - Viral upper respiratory tract infection (score 0.69)
  - Streptococcal tonsillitis (score 0.21)
  - Scarlet fever (score 0.09)
  - Measles (score 0.06)
  - Bronchiolitis (score 0.06)
Must-not-miss (retained):
  ! Measles
  ! HIV seroconversion illness
  ! Peritonsillar abscess (quinsy)
  ! Epiglottitis (adult)
Ask next: Drooling or trismus = airway emergency | 'Hot potato' voice change
Treatment: Rest, fluids, paracetamol/ibuprofen; no antibiotics; safety-net for deterioration (NICE antimicrobial stewardship).
Referral: self-care with pharmacy support
Safety net: Breathlessness at rest, confusion, no urine for 12 h, or one-sided chest pain  -  urgent.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation:
[FLAG ] retained_without_exclusion: must-not-miss condition Epiglottitis (adult) retained but never addressed  -  document why it is excluded or ask its discriminating question
        evidence: epiglottitis_adult
```

**5. Can I take ibuprofen with the aspirin I take every day?**

```text
Presenting complaint: Can I take ibuprofen with the aspirin I take every day?
Problem representation: 1 discriminating features extracted: aspirin_ingested
Differential:
  - Salicylate (aspirin) overdose (score 0.41)
Investigations: salicylate level + ABG + glucose + electrolytes  -  levels guide haemodialysis; recheck 2h after ingestion
Treatment: Emergency transfer; activated charcoal if <1h; urine alkalinisation; haemodialysis for severe toxicity.
Referral: emergency department / 999 | escalation raised routine -> emergency: ranked leader Salicylate (aspirin) overdose (emergency)
Safety net: Emergency escalation on validation  -  the ranked differential demands it. Aspirin overdose worsens for hours  -  any tinnitus, fast deep breathing or confusion after ingestion means emergency assessment.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation:
[BLOCK] escalation_consistency: escalation 'routine' contradicts the ranked differential (Salicylate (aspirin) overdose (emergency))
        evidence: escalation raised routine -> emergency: ranked leader Salicylate (aspirin) overdose (emergency)
[FIXED] escalation raised routine -> emergency: ranked leader Salicylate (aspirin) overdose (emergency)
```

**6. My mother is dying at home, she's in pain and she can't swallow tablets**

```text
Presenting complaint: My mother is dying at home, she's in pain and she can't swallow tablets
Problem representation: End-of-life care  -  terminal pain.
Treatment: Assess first: Total pain  -  physical, emotional, social and spiritual components all contribute; treat more than the body. Separate continuous background pain (needs regular analgesia) from breakthrough pain (needs a rescue dose). Severe renal impairment changes the opioid: morphine accumulates  -  alfentanil or fentanyl are the safer subcutaneous choices; involve specialist palliative care.
Care measures: Positioning, warmth, presence of family, calm environment. Review whether the existing oral analgesia still works before adding anything.
Medicines: Morphine oral solution while the patient can still swallow  -  regular dose every 4 hours plus a matching breakthrough dose. When tablets cannot be swallowed: morphine subcutaneously by syringe driver over 24 hours  -  convert the total ORAL 24-hour dose and HALVE it for the subcutaneous route. Breakthrough dose = one sixth (divide by 6) of the total 24-hour subcutaneous dose, given PRN subcutaneously. Confirm every conversion and dose with the local palliative care team / formulary before prescribing.
Route (tablets cannot be swallowed): morphine: Subcutaneous  -  syringe driver over 24 h, or PRN subcutaneous injections. Divide the total 24-hour ORAL morphine dose by 2 for the subcutaneous route (oral : SC = 2 : 1). Breakthrough = one sixth of the 24-h SC dose.
Referral: GP today; district nursing / hospice-at-home team; local out-of-hours palliative advice line.
Safety net: If pain, agitation, breathlessness or vomiting escalate beyond what the medicines at home control, call the GP or out-of-hours service the same day; 999 for a sudden catastrophic event.
 ...
```

**7. I'm 66 and for the last three months I get chest tightness when climbing stairs, it goes when I rest**

```text
Presenting complaint: I'm 66 and for the last three months I get chest tightness when climbing stairs, it goes when I rest
Problem representation: 3 discriminating features extracted: chest_pain, chest_tightness, exertional_chest_pain
Differential:
  - Stable angina (score 0.70)
  - Acute coronary syndrome (ST-elevation MI) (score 0.27)
  - Acute coronary syndrome (non-ST-elevation) (score 0.24)
  - Acute asthma exacerbation (score 0.14)
  - Aortic dissection (score 0.11)
Must-not-miss (retained):
  ! Acute coronary syndrome (non-ST-elevation)
  ! Aortic dissection
  ! Acute asthma exacerbation
  ! Lung cancer
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
Investigations: resting ECG  -  baseline; excludes alternative; CT coronary angiography  -  diagnostic; NICE first-line
Treatment: GTN sublingual PRN, aspirin, statin and cardiovascular risk assessment; arrange diagnostic testing per NICE CG95; safety-net for changing pattern.
Referral: routine GP review
Safety net: If the pain comes on at rest, lasts >15 minutes, or is new and severe, treat as possible ACS  -  call 999.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**8. I burned my hand on the kettle this morning**

```text
Presenting complaint: I burned my hand on the kettle this morning
Problem representation: EMERGENCY pattern matched: major_burn
Differential:
Must-not-miss (retained):
  ! major burn
Treatment: Do not delay transfer for further history.
Referral: EMERGENCY: Major burn/scald  -  cool with running water 20 minutes, cling-film, keep warm, emergency transfer. Airway burns (hoarseness, singed hairs) need 999 immediately. Call 999 now.
Safety net: Major burn/scald  -  cool with running water 20 minutes, cling-film, keep warm, emergency transfer. Airway burns (hoarseness, singed hairs) need 999 immediately.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Emergency pathway overrides diagnostic refinement.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**9. I've been back from Nigeria for three days and now I have a fever**

```text
Presenting complaint: I've been back from Nigeria for three days and now I have a fever
Problem representation: 1 discriminating features extracted: fever
Differential:
  - Community-acquired pneumonia (score 0.14)
  - Infective endocarditis (score 0.11)
  - COVID-19 / respiratory viral illness with red flags (score 0.10)
  - Meningitis / meningococcal disease (score 0.09)
  - Neutropenic sepsis (score 0.09)
Must-not-miss (retained):
  ! Pulmonary tuberculosis
  ! Acute appendicitis
  ! Acute cholecystitis
  ! Acute diverticulitis
  ! Acute viral hepatitis
  ! Meningitis / meningococcal disease
  ! Encephalitis
  ! Sepsis
  ! Acute pyelonephritis
  ! Measles
  ! HIV seroconversion illness
  ! Croup (laryngotracheobronchitis)
  ! Meningococcal disease (child)
  ! Giant cell arteritis
  ! Septic arthritis
  ! Pelvic inflammatory disease
  ! Suspected leukaemia (urgent)
  ! Malaria (falciparum)  -  fever after travel
  ! Yellow fever (vaccine-preventable haemorrhagic fever)
  ! Leptospirosis (Weil disease)
  ! Amoebic liver abscess
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Peritonsillar abscess (quinsy)
  ! Epiglottitis (adult)
  ! Epididymitis (STI-associated, <35y)
  ! Infected wound
  ! Serotonin syndrome
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
  ! Puerperal sepsis (post-birth infection)
  ! Neutropenic sepsis
  ! Stevens-Johnson syndrome / toxic epidermal necrolysis
  ! Eczema herpeticum
  ! Necrotising fasciitis
  ! Febrile convulsion (simple)
  ! Prostatitis
  ! Orbital cellulitis
  ! Melioidosis
  ! Human African trypanosomiasis (sleeping sickness)
 ...
```

**10. I'm 58 and I'm having difficulty swallowing my food, and I've lost weight**

```text
Presenting complaint: I'm 58 and I'm having difficulty swallowing my food, and I've lost weight
Problem representation: 2 discriminating features extracted: weight_loss, dysphagia
Differential:
  - Anorexia nervosa (score 0.16)
  - Peritonsillar abscess (quinsy) (score 0.15)
  - New type 1 diabetes (score 0.14)
  - Pulmonary tuberculosis (score 0.12)
  - Epiglottitis (adult) (score 0.12)
Must-not-miss (retained):
  ! Infective endocarditis
  ! Lung cancer
  ! Pulmonary tuberculosis
  ! Colorectal cancer
  ! New type 1 diabetes
  ! Diabetic ketoacidosis
  ! Prostate cancer (suspected)
  ! Suspected leukaemia (urgent)
  ! Amoebic liver abscess
  ! Epiglottitis (adult)
  ! Oral cancer (suspect)
  ! Suspected Crohn's disease
  ! HIV infection (undiagnosed / late presentation)
  ! Visceral leishmaniasis (kala-azar)
Ask next: BMI <17.5 or rapid loss | body image distortion | Unilateral severe pain + uvula deviation to the healthy side
Investigations: BMI + ECG + U&E/FBC/osteoporosis screen  -  physical risk assessment
Treatment: Assess physical risk (MEED); refer eating-disorder service  -  children/young people: immediate referral (NICE NG69); GP monitors bones, ECG, electrolytes.
Referral: same-day urgent review
Safety net: Fainting, heart rate under 40, or rapid weight loss  -  same-day medical assessment.
 ...
```

**11. I was bitten by a dog in Bali two days ago, it broke the skin**

```text
Presenting complaint: I was bitten by a dog in Bali two days ago, it broke the skin
Problem representation: 2 discriminating features extracted: dirty_or_deep_wound, bite_wound_exposure
Differential:
  - Tetanus-prone wound (score 0.38)
  - Rabies exposure risk (mammalian bite/scratch) (score 0.27)
Investigations: none  -  immune status history is the test  -  decide vaccine vs immunoglobulin by wound class + vaccine history
Treatment: Clean and debride; complete primary course or booster per schedule; tetanus immunoglobulin for dirty wounds with incomplete/unknown immunity  -  same day.
Referral: same-day urgent review
Safety net: Jaw stiffness, difficulty opening the mouth, or muscle spasms days-weeks after any wound = emergency now.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**12. I've taken twenty paracetamol tablets**

```text
Presenting complaint: I've taken twenty paracetamol tablets
Problem representation: 1 discriminating features extracted: paracetamol_ingested
Differential:
  - Paracetamol (acetaminophen) overdose (score 0.45)
Investigations: paracetamol level (4h post-ingestion) + LFT/INR/creatinine  -  plot on the treatment nomogram; INR is the liver-failure tracker
Treatment: TOXBASE/poison centre advice; N-acetyl-cysteine per nomogram (start before levels return if >8h or staggered); never discharge without mental-health assessment if deliberate.
Referral: emergency department / 999 | escalation raised routine -> emergency: ranked leader Paracetamol (acetaminophen) overdose (emergency)
Safety net: Emergency escalation on validation  -  the ranked differential demands it. Any paracetamol overdose  -  however well the person looks  -  needs same-day hospital assessment.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation:
[BLOCK] escalation_consistency: escalation 'routine' contradicts the ranked differential (Paracetamol (acetaminophen) overdose (emergency))
        evidence: escalation raised routine -> emergency: ranked leader Paracetamol (acetaminophen) overdose (emergency)
[FIXED] escalation raised routine -> emergency: ranked leader Paracetamol (acetaminophen) overdose (emergency)
```

**13. My wife is 34 weeks pregnant and hasn't felt the baby move since yesterday**

```text
Presenting complaint: My wife is 34 weeks pregnant and hasn't felt the baby move since yesterday
Problem representation: 1 discriminating features extracted: pregnancy_context
Differential:
  - Threatened miscarriage (score 0.29)
  - Eclampsia (score 0.27)
  - Incomplete / ongoing miscarriage (score 0.27)
  - Imminent birth / active labour (score 0.26)
  - Cord prolapse (score 0.18)
Must-not-miss (retained):
  ! Imminent birth / active labour
  ! Cord prolapse
  ! Incomplete / ongoing miscarriage
Ask next: bleeding <24 weeks with a closed cervix; many settle  -  but an ectopic can present identically | the EPU scan is what separates threatened miscarriage from missed/ectopic  -  clinical gestation alone cannot | any seizure or unresponsive collapse after 20 weeks of pregnancy, in labour, or within 6 weeks of birth  -  eclampsia until proven otherwise
Investigations: early pregnancy unit scan + hCG trajectory  -  location and viability
Treatment: Same-day EPU assessment (under 18 weeks); rest does not prevent miscarriage; anti-D if rhesus negative; return immediately for heavy bleeding, pain or dizziness.
Referral: same-day urgent review | escalation raised routine -> urgent: ranked leader Threatened miscarriage (urgent)
Safety net: Bleeding that soaks a pad an hour, faintness, or one-sided/shoulder-tip pain  -  emergency now.
 ...
```

**14. I had a seizure for the first time last week, do I need to stop driving?**

```text
Presenting complaint: I had a seizure for the first time last week, do I need to stop driving?
Problem representation: 2 discriminating features extracted: seizure, first_ever_seizure
Differential:
  - First-ever seizure (adult, recovered) (score 0.65)
  - Eclampsia (score 0.27)
  - Known epilepsy  -  breakthrough seizure (score 0.21)
  - Tricyclic antidepressant overdose (score 0.08)
  - Encephalitis (score 0.06)
Must-not-miss (retained):
  ! Encephalitis
  ! Hypoglycaemia
  ! Tricyclic antidepressant overdose
  ! Alcohol withdrawal delirium (delirium tremens)
  ! Known epilepsy  -  breakthrough seizure
Investigations: Same-day assessment with bloods (glucose, U&E, calcium, FBC) and ECG  -  first seizure is same-day medicine; ECG catches the cardiac syncope mimic
Treatment: Same-day medical assessment (ED or first-fit clinic per local pathway); stop driving and inform DVLA  -  an isolated first seizure usually means 6 months off; do not start antiepileptics in general practice.
Referral: same-day urgent review | escalation raised routine -> urgent: ranked leader First-ever seizure (adult, recovered) (urgent)
Safety net: Seizure lasting more than 5 minutes, repeated seizures, or not waking properly  -  999.
 ...
```

**15. My mum is 79, she has kidney disease, diabetes and heart failure, and now she's dizzy and confused on her eight tablets**

```text
Presenting complaint: My mum is 79, she has kidney disease, diabetes and heart failure, and now she's dizzy and confused on her eight tablets
Problem representation: 3 discriminating features extracted: dizziness, confusion, known_ckd
Differential:
  - Advanced chronic kidney disease (stage 4-5) (score 0.46)
  - Delirium (score 0.23)
  - Encephalitis (score 0.22)
  - Adrenal crisis (Addisonian) (score 0.12)
  - Carbon monoxide poisoning (score 0.11)
Must-not-miss (retained):
  ! Community-acquired pneumonia
  ! Stroke / TIA
  ! Meningitis / meningococcal disease
  ! Status epilepticus
  ! Encephalitis
  ! Hyperosmolar hyperglycaemic state
  ! Hypoglycaemia
  ! Adrenal crisis (Addisonian)
  ! Hypercalcaemia (incl. malignancy-related)
  ! Sepsis
  ! Frailty decompensation
  ! Acute kidney injury (pre-renal/dehydration)
  ! Enteric fever (typhoid)  -  fever after travel
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Salicylate (aspirin) overdose
  ! Carbon monoxide poisoning
  ! Alcohol withdrawal delirium (delirium tremens)
  ! Serotonin syndrome
  ! Methanol / ethylene glycol poisoning
  ! Puerperal sepsis (post-birth infection)
  ! Neutropenic sepsis
  ! Necrotising fasciitis
  ! Decompensated cirrhosis
  ! Heat exhaustion
Ask next: Positional and seconds-long (BPPV) vs continuous | ANY other neurological sign alongside the vertigo
Investigations: eGFR + potassium + bicarbonate + Hb; urine ACR; renal ultrasound if obstruction possible  -  the number that changes management is today's potassium
 ...
```

**16. I'm tired all the time**

```text
Presenting complaint: I'm tired all the time
Problem representation: 1 discriminating features extracted: fatigue
Differential:
  - COVID-19 / respiratory viral illness with red flags (score 0.07)
  - Viral upper respiratory tract infection (score 0.06)
  - Influenza (score 0.06)
  - Hypothyroidism (score 0.05)
  - Infectious mononucleosis (glandular fever) (score 0.05)
Must-not-miss (retained):
  ! Acute heart failure
  ! Infective endocarditis
  ! Colorectal cancer
  ! Acute viral hepatitis
  ! New type 1 diabetes
  ! Adrenal crisis (Addisonian)
  ! Hypercalcaemia (incl. malignancy-related)
  ! HIV seroconversion illness
  ! Frailty decompensation
  ! Rheumatoid arthritis (early)
  ! Suspected leukaemia (urgent)
  ! Malaria (P. vivax / P. ovale)
Ask next: loss of taste/smell | contact with case | self-limiting <1-2 weeks
Investigations: oxygen saturations  -  severity gate
Treatment: Symptom control + advice; breathlessness at rest or desaturation = emergency; consider antivirals in eligible high-risk groups.
Referral: self-care with pharmacy support
Safety net: Measure saturations if unwell; breathlessness at rest, blue lips or confusion = 999.
 ...
```

**17. I feel dizzy when I stand up since my doctor doubled my water tablet**

```text
Presenting complaint: I feel dizzy when I stand up since my doctor doubled my water tablet
Problem representation: 2 discriminating features extracted: dizziness, dizzy_on_standing
Differential:
  - Adrenal crisis (Addisonian) (score 0.07)
  - Haemorrhagic shock (score 0.07)
  - Carbon monoxide poisoning (score 0.06)
  - Postpartum haemorrhage (PPH) (score 0.05)
  - Adverse drug effect in polypharmacy (score 0.04)
Must-not-miss (retained):
  ! Stroke / TIA
  ! Sepsis
  ! Carbon monoxide poisoning
  ! Postpartum haemorrhage (PPH)
  ! Heat exhaustion
Ask next: known Addison/long-term steroids missed | hyponatraemia + hyperkalaemia + hypoglycaemia | pale, cold, clammy with fast weak pulse after injury or bleeding  -  blood pressure is normal until >30% lost (a late sign)
Investigations: short Synacthen test  -  confirms (after hydrocortisone if crisis)
Treatment: Suspected crisis: call 999; IM hydrocortisone 100 mg immediately + IV fluids; do not delay for tests.
Referral: emergency department / 999
Safety net: Steroid-dependent person vomiting or collapsing  -  emergency (needs injectable hydrocortisone).
 ...
```

**18. I had a needlestick injury two hours ago from a patient who is hepatitis B positive**

```text
Presenting complaint: I had a needlestick injury two hours ago from a patient who is hepatitis B positive
Problem representation: 1 discriminating features extracted: needlestick_event
Differential:
  - Bloodborne-virus exposure (needlestick/splash/sexual) (score 0.32)
Investigations: Baseline recipient labs: HIV 4th-gen, HBsAg + anti-HBs, HCV Ab, LFTs; source testing where consented  -  anchors the decision and the follow-up schedule; anti-HBs >=10 = already protected against HBV
Treatment: First dose before the full story: HIV PEP (28-day starter) if <72h and source positive/unknown-risk; HBIG + accelerated HBV vaccine if source HBsAg+ and recipient unprotected; wash/irrigate the site; report per occupational-health protocol.
Referral: same-day urgent review
Safety net: Needlestick, splash or unprotected exposure with a known-positive source: same-day assessment  -  HIV PEP works inside 72 hours and HBIG inside ~48. Never 'wait and see' inside those windows.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**19. My ankles are swollen and I'm breathless when I lie flat at night**

```text
Presenting complaint: My ankles are swollen and I'm breathless when I lie flat at night
Problem representation: 4 discriminating features extracted: breathlessness, ankle_swelling, breathless_acute, joint_pain_ankles_hsp
Differential:
  - Acute heart failure (score 0.23)
  - IgA vasculitis (Henoch-Schönlein purpura) (score 0.19)
  - COPD exacerbation (score 0.18)
  - Acute asthma exacerbation (score 0.14)
  - Bronchiolitis (score 0.12)
Must-not-miss (retained):
  ! Acute coronary syndrome (ST-elevation MI)
  ! Acute coronary syndrome (non-ST-elevation)
  ! Aortic dissection
  ! Pulmonary embolism
  ! Severe hypertension
  ! Acute asthma exacerbation
  ! COPD exacerbation
  ! Community-acquired pneumonia
  ! Pneumothorax
  ! Lung cancer
  ! Guillain-Barre syndrome
  ! Diabetic ketoacidosis
  ! Asthma exacerbation (child)
  ! Penetrating chest/abdominal trauma
  ! Blunt chest trauma (rib fracture / haemothorax)
  ! Major burn
  ! Neutropenic sepsis
  ! Superior vena cava obstruction (SVCO)
  ! Erythroderma (skin failure)
  ! Decompensated cirrhosis
Ask next: orthopnoea/PND | raised JVP | purpura you can FEEL (raised), concentrated on buttocks and legs, platelets normal
Investigations: NT-proBNP  -  rule-out <400 ng/L in non-acute setting; echocardiogram  -  characterise function
Treatment: Acute breathlessness at rest = same-day admission. Chronic: NICE NG106  -  NT-proBNP then echo, diuretics for congestion.
Referral: emergency department / 999
Safety net: Breathlessness worse lying flat, or waking gasping at night, needs urgent review.
 ...
```

**20. My toddler has had a fever for five days and his eyes look red**

```text
Presenting complaint: My toddler has had a fever for five days and his eyes look red
Problem representation: 2 discriminating features extracted: fever, fever_five_days_plus
Differential:
  - Kawasaki disease (score 0.48)
  - Community-acquired pneumonia (score 0.14)
  - Infective endocarditis (score 0.11)
  - COVID-19 / respiratory viral illness with red flags (score 0.10)
  - Meningitis / meningococcal disease (score 0.09)
Must-not-miss (retained):
  ! Infective endocarditis
  ! Pulmonary tuberculosis
  ! Acute appendicitis
  ! Acute cholecystitis
  ! Acute diverticulitis
  ! Acute viral hepatitis
  ! Meningitis / meningococcal disease
  ! Encephalitis
  ! Sepsis
  ! Acute pyelonephritis
  ! Measles
  ! HIV seroconversion illness
  ! Croup (laryngotracheobronchitis)
  ! Meningococcal disease (child)
  ! Giant cell arteritis
  ! Septic arthritis
  ! Pelvic inflammatory disease
  ! Suspected leukaemia (urgent)
  ! Malaria (falciparum)  -  fever after travel
  ! Yellow fever (vaccine-preventable haemorrhagic fever)
  ! Leptospirosis (Weil disease)
  ! Amoebic liver abscess
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Peritonsillar abscess (quinsy)
  ! Epiglottitis (adult)
  ! Epididymitis (STI-associated, <35y)
  ! Infected wound
  ! Serotonin syndrome
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
  ! Puerperal sepsis (post-birth infection)
  ! Neutropenic sepsis
  ! Stevens-Johnson syndrome / toxic epidermal necrolysis
  ! Eczema herpeticum
  ! Necrotising fasciitis
  ! Febrile convulsion (simple)
  ! Prostatitis
  ! Orbital cellulitis
  ! Melioidosis
 ...
```


# 5. Medical disclaimer and getting help

GPDISC provides second-opinion consultation, education and decision support. It is **not a replacement for professional medical care**, and it is not a diagnosis. All medical decisions should be made with a qualified healthcare professional who can examine you and know your full history.

**In an emergency, call 999 (or 911) first — never wait for software.** Chest pain, severe breathlessness, heavy bleeding, a seizure, a suspected stroke, or thoughts of harming yourself are reasons to pick up the phone immediately, not to type.

For everything else: your general practitioner, a pharmacist, or NHS 111 (in the UK) are the right next steps — and GPDISC's records are designed to be shown to them.
