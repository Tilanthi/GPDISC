# How to Use GPDISC --- a practical guide in plain English

**Version 1.1.0 - 3 September 2026 - Private and local.**

GPDISC is a private consultation system that lives entirely on this computer. You type a question in your own words --- exactly as you would say it to your family doctor --- and it replies with a structured consultation record: what it thinks might be going on, what must not be missed, what to answer next, and what should send you back for help.

**Everything stays on this computer.** Nothing you type, and no answer or record GPDISC keeps, is ever sent to any external service or website. There is no account, no cloud, no transmission of any kind.

There is really only one rule for using it: **talk to it as you would talk to a doctor.** No commands, no special words, no jargon. Plain English describing how you feel is exactly what it wants.

**In an emergency, call 999 (or your local emergency number) FIRST.** Chest pain, stroke signs, heavy bleeding, a collapsed or blue child --- telephone for help before you type anything. Software can wait; an emergency cannot. Never wait for software to tell you what you already know is urgent.

## How to ask well

The difference between a vague reply and a sharp one is almost always the question. A doctor meeting you for fifteen minutes asks who, how long, how bad. Do the same in your message and GPDISC has something to work with.

**Say who it is about, and their age.** "My 14 year old daughter..." or "I'm 68..." changes what the sensible possibilities are. Age and pregnancy matter enormously to what a symptom can mean.

**Say how long it has been going on.** "Since breakfast", "for three weeks", "for months" --- timescale sorts the worrying from the routine better than almost anything else.

**Say how bad it is, in your own words.** "I can still walk on it", "I had to sit down", "worst pain I've ever had" --- that is exactly the language doctors use with each other.

**Say what makes it better or worse.** Coming on with stairs, easing when you sit forward, starting an hour after a tablet --- these details often crack the case.

**List the medicines, including ones you buy yourself.** "I take warfarin", "my doctor doubled my water tablet", "regular ibuprofen from the chemist" --- medicines cause and colour a remarkable share of symptoms.

**Name the other conditions.** Diabetes, kidney disease, pregnancy, anything long-term. The same symptom in a different body is a different problem.

**Describe tests in everyday words.** You do not need to understand a result to pass it on: "the ECG report says irregularly irregular, no P waves, rate 130". Say what the paper said, plus how the person feels.

**Asking about someone else** is fine and common. Say who they are, their age, and what you saw: "My husband collapsed and now his speech is slurred." For someone who cannot describe it themselves --- a confused parent, a small child, someone dying --- your observation is the consultation.

**Asking about medicines** works best when you say what the medicine is for and who takes it: "My mum takes ibuprofen for her arthritis and has kidney disease --- should she still?" rather than "is ibuprofen safe?"

**Asking to make sense of a test result** --- say the numbers and words exactly as written, who the test was on, and how that person feels. A result without the person is only half a question.

**Asking for a second opinion** --- say what you were told, roughly by whom ("the hospital", "my GP"), and what worries you about it. GPDISC will lay out its own reasoning to compare against what you heard.

**When GPDISC asks you questions back --- answer them in a follow-up message.** Every reply can carry an "Ask next:" line. Those are not a quiz; they are the exact questions a doctor would ask next, and each answer you send sharpens the picture.

**And when a question is asked too bare, GPDISC says so --- it never guesses.** These two replies are real, word for word:

```text
Presenting complaint: Can I drink alcohol while taking metronidazole?
I don't have enough knowledge to assess this presentation  -  describe more or see a clinician.
Uncertainty: I don't have enough knowledge to assess this presentation  -  describe more or see a clinician.
Safety net: If symptoms worsen or new concerning features appear, seek medical review.
Validation: PASS  -  no inconsistencies, claims grounded.
```

```text
Presenting complaint: I just don't feel right, I can't put my finger on it
I don't have enough knowledge to assess this presentation  -  describe more or see a clinician.
Uncertainty: I don't have enough knowledge to assess this presentation  -  describe more or see a clinician.
Safety net: If symptoms worsen or new concerning features appear, seek medical review.
Validation: PASS  -  no inconsistencies, claims grounded.
```

That is the honest answer of a system that would rather admit a gap than invent a fact. If you get one, do what it says: describe more --- who, how long, how bad, what else --- and ask again. The thirty examples ahead show how much a fuller question buys you.

## How to read the reply

Every GPDISC reply is a consultation record with the same shape every time. Here is a real one, word for word, to a question about a cough:

```text
Presenting complaint: I've had a cough for three weeks and I've lost a bit of weight
Problem representation: 1 discriminating features extracted: cough
Differential:
  - COVID-19 / respiratory viral illness with red flags (score 0.11)
  - Viral upper respiratory tract infection (score 0.10)
  - Pulmonary tuberculosis (score 0.06)
  - Bronchiolitis (score 0.05)
  - Influenza (score 0.05)
Must-not-miss (retained):
  ! Acute asthma exacerbation
  ! Lung cancer
  ! Pulmonary tuberculosis
  ! Asthma exacerbation (child)
  ! Superior vena cava obstruction (SVCO)
Ask next: loss of taste/smell | contact with case | self-limiting <1-2 weeks
Investigations: oxygen saturations  -  severity gate
Treatment: Symptom control + advice; breathlessness at rest or desaturation = emergency; consider antivirals in eligible high-risk groups.
Referral: self-care with pharmacy support
Safety net: Measure saturations if unwell; breathlessness at rest, blue lips or confusion = 999.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them. (low confidence differential  -  the leading match is weak; describe more or see a clinician)
Validation: PASS  -  no inconsistencies, claims grounded.
```

Part by part:

- **Presenting complaint** --- the question as GPDISC understood it. Check it read you right.
- **Problem representation** --- the features it extracted from your words. When this line says "EMERGENCY pattern matched", the rest of the reply is about speed, not diagnosis.
- **Differential** --- the conditions it is actually considering, most likely first, each with a confidence score. A small score means a weak match, not a small problem.
- **Must-not-miss** --- the dangerous conditions it refuses to forget even though they are unlikely. This list is deliberately cautious: a safety net, not a verdict that you have them.
- **Ask next** --- the questions a doctor would ask you next. Answer them in a follow-up message.
- **Investigations** --- the tests that would settle it, and what each is for.
- **Treatment** --- what could be done now, and on whose advice.
- **Referral** --- who should see you, and how soon. With the safety net, this is where the level of concern lives: "self-care with pharmacy support" is routine; "same-day urgent review" means today; "EMERGENCY ... call 999" means now.
- **Safety net** --- what should change your mind and send you back for help, and how fast. Read this line even if you read nothing else.
- **Ruleset** --- which country's rules the answer ran under: guidelines, emergency number, reporting duties. Say where you are for advice that fits.
- **Uncertainty** --- how sure it is, in plain words. "Competing hypotheses remain close" is an honest invitation to describe more.
- **Validation** --- its own final self-check before showing you the answer. If a line here says an escalation was raised, believe the more urgent version.

One habit ties it together: read the **safety net** and **referral** lines first, then work upwards.

## Thirty examples

Every answer below is a **real, unedited GPDISC reply** to the question shown, exactly as it came back from the live system. Longer replies were cut where the page ran out; the line " ..." marks the cut, and nothing before it was changed. Read the questions as lessons in asking well as much as answers in their own right.

**Describing your own symptoms**

**1. I've had a cough for three weeks and I've lost a bit of weight**

```text
Presenting complaint: I've had a cough for three weeks and I've lost a bit of weight
Problem representation: 1 discriminating features extracted: cough
Differential:
  - COVID-19 / respiratory viral illness with red flags (score 0.11)
  - Viral upper respiratory tract infection (score 0.10)
  - Pulmonary tuberculosis (score 0.06)
  - Bronchiolitis (score 0.05)
  - Influenza (score 0.05)
Must-not-miss (retained):
  ! Acute asthma exacerbation
  ! Lung cancer
  ! Pulmonary tuberculosis
  ! Asthma exacerbation (child)
  ! Superior vena cava obstruction (SVCO)
Ask next: loss of taste/smell | contact with case | self-limiting <1-2 weeks
Investigations: oxygen saturations  -  severity gate
Treatment: Symptom control + advice; breathlessness at rest or desaturation = emergency; consider antivirals in eligible high-risk groups.
Referral: self-care with pharmacy support
Safety net: Measure saturations if unwell; breathlessness at rest, blue lips or confusion = 999.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
 ...
```

**2. I keep getting headaches every weekend, always around one eye**

```text
Presenting complaint: I keep getting headaches every weekend, always around one eye
Problem representation: 1 discriminating features extracted: headache
Differential:
  - Giant cell arteritis (score 0.10)
  - Tension-type headache (score 0.10)
  - Meningitis / meningococcal disease (score 0.09)
  - Carbon monoxide poisoning (score 0.09)
  - Migraine (score 0.08)
Must-not-miss (retained):
  ! Severe hypertension
  ! Subarachnoid haemorrhage
  ! Meningitis / meningococcal disease
  ! Encephalitis
  ! Acute angle-closure glaucoma
  ! Pre-eclampsia
  ! Malaria (falciparum)  -  fever after travel
  ! Enteric fever (typhoid)  -  fever after travel
  ! Malaria (P. vivax / P. ovale)
  ! Yellow fever (vaccine-preventable haemorrhagic fever)
  ! Leptospirosis (Weil disease)
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Carbon monoxide poisoning
  ! Eclampsia
  ! Heat exhaustion
Ask next: age > 50, new headache | jaw ache on chewing | bilateral pressing, no photo/phonophobia, no nausea
Investigations: ESR/CRP  -  supportive (can be normal); temporal artery ultrasound/biopsy  -  confirm (after steroids started)
Treatment: Suspected GCA: start prednisolone 40-60 mg (or IV methylprednisolone if visual symptoms) SAME DAY and refer urgently; do not delay steroids for biopsy.
Referral: emergency department / 999
 ...
```

**3. My right knee hurts when I go down stairs**

```text
Presenting complaint: My right knee hurts when I go down stairs
Problem representation: 1 discriminating features extracted: knee_pain
Differential:
  - Knee osteoarthritis (score 0.53)
Treatment: Exercise + weight loss core; topical NSAID; paracetamol; consider physio; arthroplasty referral if persistent functional impact (NICE NG226 OA).
Referral: routine GP review
Safety net: A single hot, swollen, painful knee  -  same-day review (septic arthritis until excluded).
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**4. I twisted my ankle playing football and it's swollen**

```text
Presenting complaint: I twisted my ankle playing football and it's swollen
Problem representation: 1 discriminating features extracted: limb_injury_event
Differential:
  - Closed limb fracture (score 0.29)
  - Open (compound) fracture (score 0.29)
Ask next: pain + swelling + bony tenderness + inability to weight-bear (Ottawa ankle/knee rules) | deformity or crepitus is fracture until X-rayed | any wound communicating with the fracture site  -  even a tiny puncture over a deformity
Investigations: X-ray  -  Ottawa rules gate the need
Treatment: Immobilise, elevate, analgesia, same-day fracture clinic / A&E; open wounds or neurovascular change are emergencies.
Referral: same-day urgent review | escalation raised routine -> urgent: ranked leader Closed limb fracture (urgent)
Safety net: Numbness, pins-and-needles, or cold pale digits beyond the injury  -  emergency now, not tomorrow.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation:
[BLOCK] escalation_consistency: escalation 'routine' contradicts the ranked differential (Closed limb fracture (urgent))
 ...
```

**5. I feel dizzy when I stand up ever since my doctor doubled my water tablet**

```text
Presenting complaint: I feel dizzy when I stand up ever since my doctor doubled my water tablet
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
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
 ...
```

**6. I've had an itchy scaly rash in my groin for a month**

```text
Presenting complaint: I've had an itchy scaly rash in my groin for a month
Problem representation: 2 discriminating features extracted: itchy_skin, rash_generalised
Differential:
  - Atopic eczema (score 0.38)
  - Chickenpox (varicella) (score 0.18)
  - Zika virus infection (score 0.09)
  - African tick-bite fever (rickettsia) (score 0.06)
  - Acute schistosomiasis (Katayama fever) (score 0.05)
Must-not-miss (retained):
  ! Suspected melanoma
Ask next: Glass test: blanching vs non-blanching | Drowsiness and poor drinking
Treatment: Emollients generously + topical steroid potency matched to site/age; trigger avoidance; bleach baths for recurrent infection; step-up plan (NICE CG57).
Referral: self-care with pharmacy support
Safety net: Clusters of small punched-out lesions, fever, or eczema suddenly worsening and painful  -  same-day (eczema herpeticum).
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**Asking about someone else**

**7. My husband collapsed and now his speech is slurred and his face has dropped**

```text
Presenting complaint: My husband collapsed and now his speech is slurred and his face has dropped
Problem representation: EMERGENCY pattern matched: stroke_fast
Differential:
Must-not-miss (retained):
  ! stroke fast
Treatment: Do not delay transfer for further history.
Referral: EMERGENCY: Possible stroke  -  call 999 immediately (FAST). Time = brain. Call 999 now.
Safety net: Possible stroke  -  call 999 immediately (FAST). Time = brain.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Emergency pathway overrides diagnostic refinement.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**8. My father has become confused since starting a new tablet last week**

```text
Presenting complaint: My father has become confused since starting a new tablet last week
Problem representation: 4 discriminating features extracted: confusion, medication_change_recent, confusion_after_injury, new_drug_started
Differential:
  - Adverse drug effect in polypharmacy (score 0.30)
  - Moderate/severe traumatic brain injury (score 0.29)
  - Stevens-Johnson syndrome / toxic epidermal necrolysis (score 0.26)
  - Delirium (score 0.23)
  - Encephalitis (score 0.22)
Must-not-miss (retained):
  ! Community-acquired pneumonia
  ! Meningitis / meningococcal disease
  ! Status epilepticus
  ! Encephalitis
  ! Hyperosmolar hyperglycaemic state
  ! Hypoglycaemia
  ! Adrenal crisis (Addisonian)
  ! Hypercalcaemia (incl. malignancy-related)
  ! Sepsis
  ! Delirium
  ! Frailty decompensation
  ! Acute kidney injury (pre-renal/dehydration)
  ! Enteric fever (typhoid)  -  fever after travel
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Haemorrhagic shock
  ! Crush injury / crush syndrome
  ! Salicylate (aspirin) overdose
  ! Carbon monoxide poisoning
  ! Alcohol withdrawal delirium (delirium tremens)
  ! Serotonin syndrome
  ! Methanol / ethylene glycol poisoning
  ! Puerperal sepsis (post-birth infection)
  ! Neutropenic sepsis
  ! Stevens-Johnson syndrome / toxic epidermal necrolysis
  ! Necrotising fasciitis
 ...
```

**9. My 14 year old daughter has stopped eating and is losing weight**

```text
Presenting complaint: My 14 year old daughter has stopped eating and is losing weight
Problem representation: 1 discriminating features extracted: weight_loss
Differential:
  - Anorexia nervosa (score 0.16)
  - New type 1 diabetes (score 0.14)
  - Pulmonary tuberculosis (score 0.12)
  - Hyperthyroidism / thyrotoxicosis (score 0.10)
  - Lung cancer (score 0.09)
Must-not-miss (retained):
  ! Infective endocarditis
  ! Lung cancer
  ! Pulmonary tuberculosis
  ! Colorectal cancer
  ! Diabetic ketoacidosis
  ! Prostate cancer (suspected)
  ! Suspected leukaemia (urgent)
  ! Amoebic liver abscess
  ! Oral cancer (suspect)
  ! Suspected Crohn's disease
  ! HIV infection (undiagnosed / late presentation)
  ! Visceral leishmaniasis (kala-azar)
Ask next: BMI <17.5 or rapid loss | body image distortion | young/lean patient, onset over weeks
Investigations: BMI + ECG + U&E/FBC/osteoporosis screen  -  physical risk assessment
Treatment: Assess physical risk (MEED); refer eating-disorder service  -  children/young people: immediate referral (NICE NG69); GP monitors bones, ECG, electrolytes.
Referral: same-day urgent review
Safety net: Fainting, heart rate under 40, or rapid weight loss  -  same-day medical assessment.
 ...
```

**10. My wife is 34 weeks pregnant and hasn't felt the baby move since this morning**

```text
Presenting complaint: My wife is 34 weeks pregnant and hasn't felt the baby move since this morning
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
 ...
```

**Asking about medicines**

**11. Is it safe to take paracetamol alongside warfarin?**

```text
Presenting complaint: Is it safe to take paracetamol alongside warfarin?
Problem representation: 1 discriminating features extracted: paracetamol_ingested
Differential:
  - Paracetamol (acetaminophen) overdose (score 0.45)
Investigations: paracetamol level (4h post-ingestion) + LFT/INR/creatinine  -  plot on the treatment nomogram; INR is the liver-failure tracker
Treatment: TOXBASE/poison centre advice; N-acetyl-cysteine per nomogram (start before levels return if >8h or staggered); never discharge without mental-health assessment if deliberate.
Referral: emergency department / 999 | escalation raised routine -> emergency: ranked leader Paracetamol (acetaminophen) overdose (emergency)
Safety net: Emergency escalation on validation  -  the ranked differential demands it. Any paracetamol overdose  -  however well the person looks  -  needs same-day hospital assessment.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
 ...
```

**12. I have type 2 diabetes and chronic kidney disease, I take metformin and my eGFR is now 28, is it still safe?**

```text
Presenting complaint: I have type 2 diabetes and chronic kidney disease, I take metformin and my eGFR is now 28, is it still safe?
Problem representation: 1 discriminating features extracted: known_ckd
Differential:
  - Advanced chronic kidney disease (stage 4-5) (score 0.46)
Investigations: eGFR + potassium + bicarbonate + Hb; urine ACR; renal ultrasound if obstruction possible  -  the number that changes management is today's potassium
Treatment: Stage-appropriate: sick-day rules (SADMANS  -  suspend NSAIDs, ACE, diuretics, metformin, SGLT2i during any dehydrating illness), anaemia check, renal dietitian, bone mineral (calcium/phosphate/PTH), vaccinations, and low-clearance/dialysis planning conversations BEFORE the crash landing. Every prescription crosses the renal check.
Referral: routine GP review
Safety net: Passing much less urine, breathless lying flat, palpitations or muscle weakness  -  same-day (fluid overload and potassium). Rising itch and nausea with drowsiness  -  urgent review.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
 ...
```

**13. Should my mum still take ibuprofen for her arthritis if she has kidney disease?**

```text
Presenting complaint: Should my mum still take ibuprofen for her arthritis if she has kidney disease?
Problem representation: 1 discriminating features extracted: known_ckd
Differential:
  - Advanced chronic kidney disease (stage 4-5) (score 0.46)
Investigations: eGFR + potassium + bicarbonate + Hb; urine ACR; renal ultrasound if obstruction possible  -  the number that changes management is today's potassium
Treatment: Stage-appropriate: sick-day rules (SADMANS  -  suspend NSAIDs, ACE, diuretics, metformin, SGLT2i during any dehydrating illness), anaemia check, renal dietitian, bone mineral (calcium/phosphate/PTH), vaccinations, and low-clearance/dialysis planning conversations BEFORE the crash landing. Every prescription crosses the renal check.
Referral: routine GP review
Safety net: Passing much less urine, breathless lying flat, palpitations or muscle weakness  -  same-day (fluid overload and potassium). Rising itch and nausea with drowsiness  -  urgent review.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
 ...
```

**Making sense of tests**

**14. I've been thirsty and passing lots of urine for a week, now I'm breathing deeply, my blood gas shows pH 7.28, pCO2 3.4, bicarbonate 12**

```text
Presenting complaint: I've been thirsty and passing lots of urine for a week, now I'm breathing deeply, my blood gas shows pH 7.28, pCO2 3.4, bicarbonate 12
Problem representation: EMERGENCY pattern matched: dka
Differential:
Must-not-miss (retained):
  ! dka
Treatment: Do not delay transfer for further history.
Referral: EMERGENCY: Possible DKA  -  emergency; diabetic decompensation. Call 999 now.
Safety net: Possible DKA  -  emergency; diabetic decompensation.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Emergency pathway overrides diagnostic refinement.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**15. My urine test shows blood and protein and my ankles are swollen, but it doesn't sting when I wee**

```text
Presenting complaint: My urine test shows blood and protein and my ankles are swollen, but it doesn't sting when I wee
Problem representation: 2 discriminating features extracted: ankle_swelling, joint_pain_ankles_hsp
Differential:
  - IgA vasculitis (Henoch-Schönlein purpura) (score 0.19)
  - Acute heart failure (score 0.11)
  - Advanced chronic kidney disease (stage 4-5) (score 0.04)
  - Decompensated cirrhosis (score 0.04)
Must-not-miss (retained):
  ! Decompensated cirrhosis
Investigations: BP measurement + urinalysis at diagnosis and weekly x4-6, FBC (platelets normal), U&E, albumin  -  the kidneys are the organ at risk; platelet count separates from ITP
Treatment: Most children need rest, simple analgesia and BP+urine monitoring; admit for abdominal or testicular pain, renal involvement or being unable to walk comfortably.
Referral: same-day urgent review
Safety net: Return immediately with severe tummy pain, swollen or painful testicles, headache or visual change, or if the rash spreads to the trunk; BP and urine checks weekly for a month whatever the child's outlook today.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
 ...
```

**16. I've had palpitations for two days, the ECG says irregularly irregular, no P waves, rate 130**

```text
Presenting complaint: I've had palpitations for two days, the ECG says irregularly irregular, no P waves, rate 130
Problem representation: 1 discriminating features extracted: palpitations
Differential:
  - Atrial fibrillation (new/undetected) (score 0.25)
  - Panic attacks / anxiety-related symptoms (score 0.14)
  - Stimulant toxicity (cocaine / MDMA / amphetamine) (score 0.09)
  - Hyperthyroidism / thyrotoxicosis (score 0.08)
  - Tricyclic antidepressant overdose (score 0.06)
Must-not-miss (retained):
  ! Tricyclic antidepressant overdose
  ! Stimulant toxicity (cocaine / MDMA / amphetamine)
Investigations: 12-lead ECG  -  diagnostic
Treatment: Rate or rhythm control plus stroke-risk assessment (CHA2DS2-VASc / ORBIT) and bleeding risk per NICE NG196.
Referral: routine GP review
Safety net: Palpitations with chest pain, fainting or breathlessness need same-day assessment; otherwise ECG within days.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**17. I've been feverish with drenching night sweats, my doctor heard a new heart murmur, and my blood culture has grown Staphylococcus aureus**

```text
Presenting complaint: I've been feverish with drenching night sweats, my doctor heard a new heart murmur, and my blood culture has grown Staphylococcus aureus
Problem representation: 3 discriminating features extracted: fever, night_sweats, new_murmur
Differential:
  - Infective endocarditis (score 0.41)
  - Pulmonary tuberculosis (score 0.19)
  - Community-acquired pneumonia (score 0.14)
  - COVID-19 / respiratory viral illness with red flags (score 0.10)
  - Meningitis / meningococcal disease (score 0.09)
Must-not-miss (retained):
  ! Community-acquired pneumonia
  ! Lung cancer
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
 ...
```

**Travel and the wider world**

**18. I'm going trekking in Nepal for three weeks, what should I do to prepare?**

```text
Presenting complaint: I'm going trekking in Nepal for three weeks, what should I do to prepare?
Problem representation: 1 discriminating features extracted: prep_request
Differential:
  - HIV pre-exposure prophylaxis (PrEP) candidacy (score 0.42)
Investigations: HIV Ag/Ab test, hepatitis B/C, syphilis, gonorrhoea/chlamydia NAAT baseline; renal function  -  PrEP needs a negative HIV test and a working kidney first; Repeat HIV test at 3 months with renal monitoring  -  on-PrEP safety netting
Treatment: Confirm HIV negative, screen STIs and hepatitis, check eGFR, then prescribe per national PrEP scheme  -  daily or event-driven. Stress adherence and 3-monthly review; condoms still prevent the rest.
Referral: routine GP review
Safety net: Fever with rash and sore throat in the weeks after a new exposure  -  test BEFORE starting or continuing PrEP.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**19. I've come back from Kenya with a fever and a rash**

```text
Presenting complaint: I've come back from Kenya with a fever and a rash
Problem representation: 2 discriminating features extracted: fever, rash_generalised
Differential:
  - Community-acquired pneumonia (score 0.14)
  - Infective endocarditis (score 0.11)
  - Zika virus infection (score 0.11)
  - COVID-19 / respiratory viral illness with red flags (score 0.10)
  - African tick-bite fever (rickettsia) (score 0.10)
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
 ...
```

**20. It's been 40 degrees on my building site and my workmate is confused and has stopped sweating**

```text
Presenting complaint: It's been 40 degrees on my building site and my workmate is confused and has stopped sweating
Problem representation: 3 discriminating features extracted: sweating, confusion, hot_dry_confused
Differential:
  - Heat stroke (score 0.37)
  - Delirium (score 0.23)
  - Encephalitis (score 0.22)
  - Hypoglycaemia (score 0.18)
  - Acute coronary syndrome (ST-elevation MI) (score 0.12)
Must-not-miss (retained):
  ! Acute coronary syndrome (ST-elevation MI)
  ! Acute coronary syndrome (non-ST-elevation)
  ! Community-acquired pneumonia
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
  ! Amoebic liver abscess
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
Investigations: Rectal/core temp (tympanic under-reads), CK, renal function, LFTs, coagulation, glucose, electrolytes  -  maps the organ damage
Treatment: 999 + COOL AGGRESSIVELY NOW: shade, strip, ice-water immersion where possible (gold standard), else evaporative (mist + fan + ice packs to neck/axillae/groins). Target core <39 C within 30 minutes. Fluids carefully; avoid shivering and antipyretics (useless in heat stroke).
Referral: emergency department / 999 | escalation raised routine -> emergency: ranked leader Heat stroke (emergency)
Safety net: Emergency escalation on validation  -  the ranked differential demands it. Someone hot and not themselves in hot conditions  -  start cooling before you finish taking the history.
 ...
```

**21. I work on an oil rig and my colleague has had chest pain for half an hour**

```text
Presenting complaint: I work on an oil rig and my colleague has had chest pain for half an hour
Problem representation: EMERGENCY pattern matched: acs
Differential:
Must-not-miss (retained):
  ! acs
Treatment: Do not delay transfer for further history.
Referral: EMERGENCY: Possible acute coronary syndrome  -  call 999. Call 999 now.
Safety net: Possible acute coronary syndrome  -  call 999.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Emergency pathway overrides diagnostic refinement.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**22. My joints ache since a tick bite in the New Forest**

```text
Presenting complaint: My joints ache since a tick bite in the New Forest
Problem representation: 1 discriminating features extracted: eschar_tick_bite
Differential:
  - African tick-bite fever (rickettsia) (score 0.32)
Investigations: rickettsia_serology  -  Paired serology; diagnosis usually retrospective
Treatment: Doxycycline 7 days  -  clinical diagnosis, treat before serology confirms.
Referral: routine GP review
Safety net: Confusion, neck stiffness or non-fading rash -> emergency.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**Sensitive questions**

**23. Can I take the contraceptive pill if I get migraines with aura?**

```text
Presenting complaint: Can I take the contraceptive pill if I get migraines with aura?
Problem representation: 2 discriminating features extracted: headache, aura
Differential:
  - Migraine (score 0.26)
  - Giant cell arteritis (score 0.10)
  - Tension-type headache (score 0.10)
  - Meningitis / meningococcal disease (score 0.09)
  - Carbon monoxide poisoning (score 0.09)
Must-not-miss (retained):
  ! Severe hypertension
  ! Subarachnoid haemorrhage
  ! Meningitis / meningococcal disease
  ! Encephalitis
  ! Acute angle-closure glaucoma
  ! Pre-eclampsia
  ! Malaria (falciparum)  -  fever after travel
  ! Enteric fever (typhoid)  -  fever after travel
  ! Malaria (P. vivax / P. ovale)
  ! Yellow fever (vaccine-preventable haemorrhagic fever)
  ! Leptospirosis (Weil disease)
  ! Viral haemorrhagic fever (suspect: Lassa/Ebola/Marburg)
  ! Carbon monoxide poisoning
  ! Eclampsia
  ! Heat exhaustion
Treatment: Triptan + NSAID early in attack; prophylaxis if >= 4 attacks/month; headache diary (NICE CG150 headache).
Referral: self-care with pharmacy support
Safety net: Sudden 'worst ever' headache, fever, rash, drowsiness or new weakness  -  emergency, not migraine.
 ...
```

**24. I had unprotected sex last night, what are my options?**

```text
Presenting complaint: I had unprotected sex last night, what are my options?
Problem representation: 1 discriminating features extracted: unprotected_sex
Differential:
  - Primary syphilis (chancre) (score 0.21)
  - Chlamydia trachomatis infection (score 0.19)
  - Gonorrhoea (score 0.19)
  - Epididymitis (STI-associated, <35y) (score 0.13)
Must-not-miss (retained):
  ! Gonorrhoea
  ! Epididymitis (STI-associated, <35y)
Ask next: Classically PAINLESS indurated ulcer 10-90 days post-exposure  -  pain argues for herpes | Regional painless inguinal nodes; spontaneous healing does NOT mean resolution | Majority asymptomatic  -  screening history beats symptom pattern
Investigations: syphilis_serology  -  Treponemal EIA first-line; RPR/VDRL titre for activity
Treatment: Benzathine penicillin G single IM dose (doxycycline if penicillin-allergic). GUM same-day; full STI screen; partner notification.
Referral: same-day urgent review | escalation raised routine -> urgent: ranked leader Primary syphilis (chancre) (urgent)
Safety net: Rash, fever or warts weeks later = secondary syphilis  -  return; untreated syphilis causes cardiovascular/neurological disease.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
 ...
```

**25. I think I've got an STI, there's a discharge**

```text
Presenting complaint: I think I've got an STI, there's a discharge
Problem representation: 1 discriminating features extracted: vaginal_discharge
Differential:
  - Pelvic inflammatory disease (score 0.13)
  - Bacterial vaginosis (score 0.04)
  - Chlamydia trachomatis infection (score 0.04)
  - Gonorrhoea (score 0.04)
  - Trichomoniasis (score 0.04)
Must-not-miss (retained):
  ! Gonorrhoea
Investigations: STI screen (chlamydia/gonorrhoea)  -  supportive (can be negative)
Treatment: Empirical antibiotics per BASHH: ceftriaxone IM + doxycycline + metronidazole 14 days; analgesia; partner notification; exclude pregnancy first (BASHH/NICE).
Referral: same-day urgent review
Safety net: Pain becoming severe, fever, vomiting, or faintness  -  same-day review; always treat partners.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**26. I'm 25 and worried about a lump in my testicle**

```text
Presenting complaint: I'm 25 and worried about a lump in my testicle
Problem representation: 1 discriminating features extracted: anxiety
Differential:
  - Panic attacks / anxiety-related symptoms (score 0.50)
  - Generalised anxiety disorder (score 0.24)
  - Hyperthyroidism / thyrotoxicosis (score 0.04)
  - Alcohol dependence (score 0.03)
Treatment: Breathing retraining; explanation; CBT referral if recurrent; screen depression; avoid benzodiazepines long-term (NICE CG113).
Referral: routine GP review
Safety net: Chest pain with sweating, or fainting, or lasting >15 min is not a panic attack until physical causes excluded.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**Mind, memory and long-term illness**

**27. I've felt low since my wife died and I can't sleep**

```text
Presenting complaint: I've felt low since my wife died and I can't sleep
Problem representation: 1 discriminating features extracted: poor_sleep
Differential:
  - Depression (moderate) (score 0.16)
  - Generalised anxiety disorder (score 0.09)
  - Alcohol dependence (score 0.05)
Investigations: PHQ-9  -  severity + monitoring
Treatment: PHQ-9 severity; guided self-help/low-intensity CBT first; SSRI if moderate-severe or preference (NICE CG90); always ask about suicidal thoughts.
Referral: routine GP review
Safety net: Thoughts of harming yourself  -  seek help same day; 999 if there is a plan or intent.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**28. My son says I've been forgetting things for months**

```text
Presenting complaint: My son says I've been forgetting things for months
Problem representation: 3 discriminating features extracted: poor_concentration, memory_problems, progressive_forgetfulness
Differential:
  - Suspected dementia (incl. Alzheimer/vascular/Lewy-body) (score 0.43)
  - Depression (moderate) (score 0.19)
  - Vitamin B12 deficiency (score 0.07)
  - First-episode psychosis (score 0.02)
Must-not-miss (retained):
  ! First-episode psychosis
Investigations: Reversible-cause bloods (FBC, U&E, LFT, TFT, calcium, glucose, CRP, B12/folate)  -  excludes the treatable mimics before any dementia label; Structured cognitive test (MoCA / mini-Cog / 6-CIT)  -  quantifies the deficit and tracks progression; CT head (or MRI)  -  excludes structural cause; not to diagnose dementia itself
Treatment: Take a collateral history; review the drug list (anticholinergics, opioids, benzodiazepines); assess home safety (cooker, driving, medication handling); refer to a memory assessment service  -  do not label dementia in one consultation.
Referral: routine GP review
Safety net: Sudden confusion, drowsiness, rapid worsening or not managing fluids needs same-day assessment  -  that is delirium, not dementia, until proven otherwise.
 ...
```

**29. My terminally ill father gets agitated every evening**

```text
Presenting complaint: My terminally ill father gets agitated every evening
Problem representation: 1 discriminating features extracted: agitation
Differential:
  - Stimulant toxicity (cocaine / MDMA / amphetamine) (score 0.18)
Treatment: Emergency: active cooling, benzodiazepines in generous doses, fluids; treat cocaine chest pain as ACS (avoid beta-blockers).
Referral: emergency department / 999
Safety net: Anyone hot, agitated and twitching after stimulants needs emergency care now  -  cooled, not calmed down at home.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Leading diagnosis is favoured but premature closure is a known error  -  dangerous alternatives retained below must be actively excluded.
Validation: PASS  -  no inconsistencies, claims grounded.
```

**30. My dad's Parkinson's tablets were changed and now he's seeing things**

```text
Presenting complaint: My dad's Parkinson's tablets were changed and now he's seeing things
Problem representation: 2 discriminating features extracted: hallucination, hallucinations
Differential:
  - First-episode psychosis (score 0.30)
  - Alcohol withdrawal delirium (delirium tremens) (score 0.22)
  - Delirium (score 0.11)
Must-not-miss (retained):
  ! Delirium
Investigations: physical + drug screen  -  exclude organic causes
Treatment: Urgent referral to early intervention in psychosis team (within 2 weeks; same-day if risk); do not start antipsychotics in primary care routinely (NICE CG178).
Referral: same-day urgent review | escalation raised routine -> urgent: ranked leader First-episode psychosis (urgent)
Safety net: Voices or beliefs that others don't share, getting worse  -  urgent mental health assessment; 999 if there is risk to life.
Ruleset: United Kingdom  -  guidelines NICE / CKS (see guideline index); emergency number 999; notification per UKHSA notifiable diseases (Health Protection Regulations 2010).
Uncertainty: Competing hypotheses remain close  -  treat the differential as genuinely open and use targeted tests to separate them.
Validation:
[BLOCK] escalation_consistency: escalation 'routine' contradicts the ranked differential (First-episode psychosis (urgent))
 ...
```

## A last word

Notice how often the replies above end with a safety net --- *what should bring you back, and how fast*. That is GPDISC's most important sentence, every time.

**If in doubt, get a human.** A symptom that frightens you; anything a reply itself calls an emergency: **call 999 in the UK, 112 or 911 elsewhere --- first, and never wait for software.**

GPDISC provides second opinions, education and support for thinking. It is **not a replacement for professional medical care**, not a diagnosis to act on alone, and not a substitute for the emergency services. All medical decisions belong with qualified clinicians, taken together with you.

