"""
Mental Health/Psychiatry Domain for GPDISC
Comprehensive psychiatric consultation covering depression, anxiety, psychosis,
bipolar disorder, suicide risk assessment, and psychopharmacology.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class MentalHealthDomain(BaseDomainModule):
    """
    Mental Health/Psychiatry Specialist Domain

    Covers:
    - Depression recognition and management
    - Anxiety disorders
    - Psychosis evaluation
    - Bipolar disorder
    - Suicide risk assessment
    - Psychiatric medication basics
    - Delirium vs dementia
    - Capacity assessment
    - Mental Health Act principles
    - Schizophrenia
    - PTSD
    - OCD
    - Personality disorders
    - Eating disorders
    - Substance use disorders
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="mental_health",
            version="1.0.0",
            dependencies=[],
            description="Mental Health: depression, anxiety, psychosis, bipolar, suicide risk, psychopharmacology, dementia",
            keywords=[
                # Mood disorders
                "depression", "depressed", "low mood", "sadness", "hopelessness",
                "suicide", "suicidal", "self-harm", "overdose",
                "bipolar", "manic", "mania", "hypomania",

                # Anxiety disorders
                "anxiety", "anxious", "panic", "panic attack", "phobia",
                "worry", "nervous", "restless", "on edge",
                "generalized anxiety disorder", "gad", "social anxiety", "agoraphobia",

                # Psychotic disorders
                "psychosis", "psychotic", "hallucination", "delusion",
                "schizophrenia", "schizoaffective", "schizotypal",
                "hearing voices", "paranoia", "paranoid", "suspicious",

                # PTSD
                "ptsd", "post-traumatic stress", "trauma", "flashback", "nightmare",

                # OCD
                "obsessive compulsive", "ocd", "obsession", "compulsion", "ritual",

                # Cognitive disorders
                "dementia", "alzheimer's", "memory loss", "confusion",
                "delirium", "acute confusion", "cognitive impairment",

                # Substance use
                "addiction", "dependence", "withdrawal", "alcohol", "drug use",
                "opioid", "heroin", "cocaine", "cannabis", "benzodiazepine",

                # Eating disorders
                "anorexia", "bulimia", "binge eating", "eating disorder",

                # Personality disorders
                "personality disorder", "borderline", "narcissistic", "antisocial",

                # Medications
                "antidepressant", "ssri", "snri", "tricyclic", "mirtazapine",
                "antipsychotic", "haloperidol", "risperidone", "olanzapine", "quetiapine",
                "mood stabilizer", "lithium", "sodium valproate", "valproate",
                "benzodiazepine", "diazepam", "lorazepam",
                "hypnotic", "zolpidem", "zopiclone",

                # Mental health act
                "section", "sectioning", "involuntary admission", "mental health act",
                "capacity", "mental capacity", "competence",

                # General terms
                "mental health", "psychiatric", "psychology", "therapy", "counseling",
                "wellbeing", "stress", "burnout", "emotional"
            ],
            capabilities=[
                "depression_management",
                "anxiety_management",
                "psychosis_evaluation",
                "bipolar_management",
                "suicide_risk_assessment",
                "ptsd_management",
                "ocd_management",
                "dementia_assessment",
                "delirium_assessment",
                "substance_use_management",
                "psychopharmacology",
                "capacity_assessment",
                "personality_disorder_management",
                "eating_disorder_management"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Route mental health query to appropriate handler"""
        query_lower = query.lower()

        # Emergency - suicide/self-harm
        if any(term in query_lower for term in ["suicide", "suicidal", "self-harm", "overdose", "kill myself", "end my life"]):
            return self._handle_suicide_risk(query, context)

        # Psychosis
        elif any(term in query_lower for term in ["psychosis", "psychotic", "hallucination", "delusion", "hearing voices", "paranoia", "paranoid", "schizophrenia"]):
            return self._handle_psychosis(query, context)

        # Bipolar
        elif any(term in query_lower for term in ["bipolar", "manic", "mania", "hypomania"]):
            return self._handle_bipolar(query, context)

        # Depression
        elif any(term in query_lower for term in ["depression", "depressed", "low mood", "sadness", "hopeless"]):
            return self._handle_depression(query, context)

        # Anxiety
        elif any(term in query_lower for term in ["anxiety", "anxious", "panic", "phobia", "worry", "nervous", "generalized anxiety", "gad"]):
            return self._handle_anxiety(query, context)

        # PTSD
        elif any(term in query_lower for term in ["ptsd", "post-traumatic", "trauma", "flashback", "nightmare"]):
            return self._handle_ptsd(query, context)

        # OCD
        elif any(term in query_lower for term in ["obsessive compulsive", "ocd", "obsession", "compulsion", "ritual"]):
            return self._handle_ocd(query, context)

        # Dementia
        elif any(term in query_lower for term in ["dementia", "alzheimer's", "memory loss", "cognitive impairment"]):
            return self._handle_dementia(query, context)

        # Delirium
        elif any(term in query_lower for term in ["delirium", "acute confusion", "sudden confusion"]):
            return self._handle_delirium(query, context)

        # Substance use
        elif any(term in query_lower for term in ["addiction", "dependence", "withdrawal", "alcohol", "opiate", "cannabis"]):
            return self._handle_substance_use(query, context)

        # Eating disorders
        elif any(term in query_lower for term in ["anorexia", "bulimia", "binge eating", "eating disorder"]):
            return self._handle_eating_disorder(query, context)

        # Personality disorders
        elif "personality disorder" in query_lower or "borderline" in query_lower or "narcississ" in query_lower:
            return self._handle_personality_disorder(query, context)

        # Medications
        elif any(term in query_lower for term in ["antidepressant", "ssri", "antipsychotic", "lithium", "benzodiazepine", "mood stabilizer"]):
            return self._handle_psychopharmacology(query, context)

        # Capacity
        elif any(term in query_lower for term in ["capacity", "mental capacity", "competence"]):
            return self._handle_capacity(query, context)

        # General mental health
        else:
            return self._handle_general_mental_health(query, context)

    def _handle_suicide_risk(self, query: str, context: dict) -> DomainQueryResult:
        """Handle suicide risk assessment - CRITICAL EMphasis on safety"""
        answer = """**SUICIDE RISK ASSESSMENT - IMMEDIATE SAFETY**

**⚠️ CRITICAL: If this is an emergency, call emergency services (999/911) immediately**

**This information is for guidance only - if you or someone you know is in danger, seek immediate professional help**

---

**Emergency Resources:**

**UK:**
- **Emergency:** 999 or 112
- **Samaritans:** 116 123 (24/7, confidential)
- **Shout Crisis Text Line:** Text "SHOUT" to 85258
- **NHS 111:** 111 (non-emergency medical help)

**US:**
- **Emergency:** 911
- **National Suicide Prevention Lifeline:** 988 or 1-800-273-TALK (8255)
- **Crisis Text Line:** Text "HOME" to 741741

**Australia:**
- **Emergency:** 000
- **Lifeline:** 13 11 14
- **Beyond Blue:** 1300 22 4636

---

**Suicide Risk Assessment:**

**High-Risk Indicators (Require Immediate Evaluation):**
- **Current suicidal intent** (wanting to die, having a plan)
- **Access to means** (firearms, medications, sharp objects)
- **Specific plan** (method, time, place)
- **Previous attempts** (strongest predictor of future suicide)
- **Hopelessness**, **feeling trapped**
- **Command hallucinations** (voices telling to harm self)
- **Recent loss** (relationship, job, bereavement)
- **Substance use** (impairs judgment, increases impulsivity)
- **Chronic pain**, **terminal illness**
- **Social isolation**, **lack of support**

**Protective Factors:**
- **Family support**, **friends**
- **Children** (responsibility)
- **Pregnancy**, **religious beliefs**
- **Future plans** (events to look forward to)
- **Fear of death**, **fear of pain**

**Immediate Management (If High Risk):**

**1. Ensure Safety:**
- **Do NOT leave person alone**
- **Remove dangerous items** (medications, weapons, sharp objects)
- **Create safe environment**

**2. Seek Professional Help:**
- **Emergency department** (if imminent risk)
- **Crisis team** (home treatment team)
- **Police** (if person is uncooperative, danger to self or others)
- **Involuntary admission** (if necessary - Mental Health Act)

**3. Supportive Communication:**
- **Listen non-judgmentally**
- **Validate feelings** ("I can hear you're in a lot of pain")
- **Offer hope** ("These feelings are temporary, help is available")
- **Avoid:** Arguments, minimizing feelings, giving advice, keeping secrets

**For Family/Friends:**

**How to Help:**
- **Ask directly:** "Are you thinking about suicide?" (won't plant the idea)
- **Listen:** Let them express feelings without judgment
- **Don't keep secrets:** Safety > confidentiality
- **Remove access to means:** Medications, weapons
- **Stay with them:** Until professional help arrives
- **Encourage professional help:** Offer to go with them

**Warning Signs to Watch For:**
- **Talking about:** Wanting to die, being a burden, having no reason to live
- **Withdrawing:** From friends, family, activities
- **Giving away:** Possessions, making final arrangements
- **Mood changes:** Depression followed by sudden calm (may indicate decision)
- **Reckless behavior:** Substance use, dangerous activities
- **Sleep changes:** Too much or too little
- **Increased substance use**

**Treatment:**

**Psychotherapy:**
- **Cognitive Behavioral Therapy (CBT):** Address negative thoughts, develop coping skills
- **Dialectical Behavior Therapy (DBT):** For chronic suicidality, self-harm (especially borderline personality disorder)
- **Mindfulness-based therapies:** Stress reduction, emotional regulation

**Medication:**
- **Antidepressants:** (if depression present)
- **Antipsychotics:** (if psychosis present)
- **Mood stabilizers:** (if bipolar disorder present)
- **Anxiolytics:** Short-term (acute distress)

**Safety Planning:**
- **Identify warning signs** (thoughts, feelings, situations)
- **List coping strategies** (distraction, relaxation)
- **Identify supportive people** (friends, family, professionals)
- **Remove access to means**
- **Professional contacts:** Crisis line numbers, therapist, emergency department

**Sources:** NICE NG161, NHS England, SAMHSA, Suicide Prevention Lifeline

---

**If you are in crisis, please reach out for help. You are not alone, and support is available.**"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.95,
            metadata={
                "specialty": "mental_health_emergency",
                "focus": "suicide_prevention",
                "sources": ["NICE NG161", "NHS England", "SAMHSA"]
            }
        )

    def _handle_psychosis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle psychosis queries"""
        answer = """**Psychosis Assessment and Management**

**Definition:**
- **Psychosis:** Loss of contact with reality
- **Key symptoms:** Hallucinations, delusions, disorganized thinking, disorganized behavior

**Clinical Features:**

**Hallucinations:**
- **Auditory:** Hearing voices (most common - 70%)
  - **Commentary** (voices commenting on behavior)
  - **Command** (voices telling to do things - high risk)
  - **Conversing** (voices talking to each other)
- **Visual:** Seeing things that aren't there
- **Tactile:** Feeling things on skin (formication - insects crawling)
- **Olfactory:** Smelling things (burning, rotting)
- **Gustatory:** Tasting things (poison)

**Delusions:**
- **Fixed, false beliefs** (not corrected by evidence)
- **Types:**
  - **Persecutory:** "Someone is trying to harm me"
  - **Referential:** "TV is sending me messages"
  - **Grandiose:** "I have special powers", "I'm the Messiah"
  - **Erotomanic:** "Someone famous is in love with me"
  - **Nihilistic:** "The world is ending", "I'm already dead"
  - **Somatic:** "My organs are rotting", "I'm infested with parasites"

**Disorganized Thinking:**
- **Thought disorder:** Loosening of associations, derailment, tangentiality
- **Thought blocking:** Sudden stoppage of thoughts
- **Neologisms:** Made-up words
- **Word salad:** Incoherent speech

**Disorganized Behavior:**
- **Agitation**, **aggression**
- **Self-neglect** (poor hygiene, inadequate food)
- **Inappropriate affect** (laughing at sad things)
- **Catatonia:** Stupor, mutism, posturing, waxy flexibility

**Negative Symptoms:**
- **Flat affect** (reduced emotional expression)
- **Alogia** (poverty of speech)
- **Avolition** (lack of motivation)
- **Anhedonia** (inability to experience pleasure)
- **Asociality** (lack of social drive)

**Etiology:**

**Schizophrenia Spectrum:**
- **Schizophrenia:** Psychosis + functional decline > 6 months
- **Schizophreniform disorder:** Psychosis < 6 months
- **Schizoaffective disorder:** Psychosis + mood disorder (depression, mania)
- **Brief psychotic disorder:** Psychosis 1 day - 1 month (often stress-related)

**Other Causes:**
- **Mood disorders with psychotic features:** Bipolar disorder, severe depression
- **Substance-induced:** Amphetamines, cocaine, cannabis, hallucinogens, alcohol withdrawal
- **Medical:** Delirium, dementia, brain injury, epilepsy, lupus cerebritis
- **Primary psychiatric:** Schizophrenia, schizoaffective disorder

**Assessment:**

**History:**
- **Onset:** Acute (days-weeks) vs chronic (months-years)
- **Course:** Continuous vs episodic
- **Triggers:** Stress, substance use, sleep deprivation
- **Prodrome:** Social withdrawal, decline in function (months-years before psychosis)

**Mental Status Examination:**
- **Appearance:** Disheveled, inappropriate clothing
- **Behavior:** Agitated, retarded, catatonic
- **Speech:** Pressured, poverty, thought blocking
- **Mood:** Euthymic, depressed, elevated, anxious
- **Affect:** Flat, blunted, inappropriate, labile
- **Thought:** Delusions, hallucinations, thought disorder
- **Insight:** Absent, partial, intact

**Risk Assessment:**
- **Suicide risk:** 10% lifetime (highest in young males, early illness, depression)
- **Homicide risk:** Command hallucinations, persecutory delusions
- **Self-neglect:** Inability to care for self
- **Victimization:** Exploited by others

**Investigations:**
- **Rule out medical causes:**
  - **Delirium screen:** CBC, electrolytes, calcium, glucose, LFTs, TFTs, vitamin B12, folate
  - **Infectious:** Syphilis serology, HIV, Lyme disease
  - **Toxicology:** Urine drug screen, alcohol level
  - **Imaging:** CT head (if first psychosis, focal neurologic signs, head trauma)
  - **Neurophysiology:** EEG (if episodic symptoms, suspicion of epilepsy)

**Treatment:**

**Acute Psychosis (Hospitalization Often Required):**

**Antipsychotics:**

**First-generation (Typical):**
- **Haloperidol:** 2-10 mg PO/IM/IV (high potency, high risk of EPS)
  - **Side effects:** Extrapyramidal symptoms (EPS), dystonia, akathisia, parkinsonism, tardive dyskinesia, neuroleptic malignant syndrome (NMS)
  - **Anticholinergic:** Benztropine 1-2 mg PO/IM PRN (for EPS)

**Second-generation (Atypical):**
- **Risperidone:** 2-6 mg PO daily (first-line, well tolerated)
- **Olanzapine:** 10-20 mg PO daily (effective, metabolic side effects)
- **Quetiapine:** 150-750 mg PO daily (sedating, less EPS)
- **Aripiprazole:** 10-30 mg PO daily (partial agonist, lower EPS, metabolic side effects)

**Emergency Agitation:**
- **Rapid tranquilization:** Lorazepam 1-2 mg IM/IV + Haloperidol 5-10 mg IM/IV
- **Repeat** PRN every 30-60 minutes (monitor for oversedation, respiratory depression)

**Maintenance Treatment (Chronic Psychosis):**

**Schizophrenia:**
- **Antipsychotic:** Continue indefinitely (relapse risk > 80% if stopped)
- **First-line:** Risperidone, olanzapine, aripiprazole
- **Duration:** Minimum 1-2 years after first episode, lifelong if multiple episodes
- **Monitoring:** Weight, metabolic parameters (glucose, lipids), EPS (abnormal involuntary movements scale - AIMS)

**Clozapine (Treatment-Resistant Schizophrenia):**
- **Indications:** Failure of 2 adequate antipsychotic trials (6 weeks each at therapeutic dose)
- **Efficacy:** 30-60% response in treatment-resistant patients
- **Monitoring:** Weekly CBC for 18 weeks (agranulocytosis risk), then fortnightly, then monthly
- **Side effects:** Agranulocytosis (1%), myocarditis, cardiomyopathy, seizures, weight gain, diabetes, hypersalivation

**Psychosocial Interventions:**
- **Cognitive Behavioral Therapy for Psychosis (CBTp):** Challenge delusions, manage hallucinations
- **Family therapy:** Psychoeducation, communication skills, reduce expressed emotion (critical, hostile, emotional overinvolvement)
- **Supported employment:** Vocational rehabilitation, job coaching
- **Social skills training:** Improve interpersonal functioning
- **Assertive Community Treatment (ACT):** Intensive case management for high-risk patients

**Prognosis:**
- **Course:** Episodic (10-20%), continuous (60-70%), recovery with minimal residual (10-20%)
- **Predictors of good outcome:** Acute onset, obvious precipitant, late onset, female, good premorbid functioning, mood symptoms, early treatment
- **Predictors of poor outcome:** Insidious onset, no precipitant, early onset (adolescence), male, poor premorbid functioning, prominent negative symptoms, delays in treatment

**Sources:** NICE NG181, APA Practice Guidelines 2021, Maudsley Prescribing Guidelines 2024"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "mental_health_psychosis",
                "focus": "psychosis_management",
                "sources": ["NICE NG181", "APA 2021", "Maudsley 2024"]
            }
        )

    def _handle_bipolar(self, query: str, context: dict) -> DomainQueryResult:
        """Handle bipolar disorder queries"""
        answer = """**Bipolar Disorder Management**

**Definition:**
- **Bipolar disorder:** Mood disorder characterized by episodes of mania/hypomania and depression
- **Bipolar I:** Manic episode ± depressive episode
- **Bipolar II:** Hypomanic episode + depressive episode (no full mania)
- **Cyclothymia:** Numerous hypomanic periods + depressive symptoms (not meeting full episode criteria)

**Epidemiology:**
- **Lifetime prevalence:** 1-2%
- **Age of onset:** Late teens - early 20s (average 18-20)
- **Gender:** Equal (Bipolar I), female > male (Bipolar II)
- **Suicide risk:** 15-20% lifetime (higher than unipolar depression)

**Clinical Features:**

**Manic Episode (≥ 1 week, or hospitalization required):**

**Mood Symptoms:**
- **Elevated, expansive, irritable mood**
- **Inappropriate euphoria** (extreme happiness)
- **Irritability** (especially if activities thwarted)

**Increased Energy/Activity:**
- **Decreased need for sleep** (feels rested after 3 hours)
- **Increased goal-directed activity** (work, school, social)
- **Psychomotor agitation** (pacing, restlessness)

**Symptoms (≥ 3 if euphoric, ≥ 4 if irritable):**
- **Inflated self-esteem** (grandiosity - "I'm a genius", "I'm God")
- **Decreased need for sleep** (insomnia but not tired)
- **More talkative** (pressure of speech)
- **Flight of ideas** (racing thoughts)
- **Distractibility** (easily pulled to irrelevant stimuli)
- **Increased goal-directed activity** (socially, work, sexually)
- **Excessive involvement** in risky activities (spending sprees, risky investments, sexual indiscretions)
- **Psychosis:** Delusions, hallucinations (in severe mania)

**Hypomanic Episode (≥ 4 consecutive days, NOT severe enough to cause marked impairment, NO psychosis):**
- **Similar to mania but less severe**
- **No hospitalization required**
- **No psychosis**
- **Often not recognized** by patient (attributed to "feeling good")

**Depressive Episode:**
- **Similar to unipolar depression**
- **More likely to have:** Atypical features (hypersomnia, hyperphagia, leaden paralysis)
- **Higher suicide risk** (than unipolar depression - more lethal attempts)

**Mixed Episode:**
- **Manic + depressive symptoms** simultaneously
- **High suicide risk** (depressed mood + increased energy)
- **Agitation**, **insomnia**, **racing thoughts** + guilt, hopelessness, suicidal ideation

**Diagnosis:**

**Differential Diagnosis:**
- **Unipolar depression:** No manic/hypomanic episodes
- **Schizoaffective disorder:** Psychosis independent of mood episodes
- **Substance-induced:** Mania induced by antidepressants, stimulants, steroids
- **Medical:** Hyperthyroidism, neurological disorders, medications

**Assessment:**
- **Mood charting:** Daily mood, sleep, energy, medications (retrospective or prospective)
- **Collateral history:** Family, partner (patient lacks insight into manic symptoms)
- **Screening tools:** MDQ (Mood Disorder Questionnaire), HCL-32 (Hypomania Checklist)

**Treatment:**

**Acute Mania:**

**Hospitalization:**
- **Indications:** Psychosis, danger to self/others, marked impairment
- **Voluntary** vs **involuntary** (if lacks insight, dangerous behavior)

**Pharmacotherapy:**
- **Lithium:** 600-1200 mg daily (serum level 0.6-1.2 mmol/L)
  - **Onset:** 1-2 weeks (may need adjunctive antipsychotic initially)
  - **Side effects:** Tremor, nausea, diarrhea, hypothyroidism, renal toxicity
- **Valproate (sodium valproate):** 750-2000 mg daily (serum level 50-125 µg/mL)
  - **Onset:** Faster than lithium (days-weeks)
  - **Side effects:** Weight gain, tremor, hepatotoxicity, teratogenic (avoid in pregnancy)
- **Antipsychotics:**
  - **Olanzapine:** 10-20 mg daily (rapid onset)
  - **Quetiapine:** 300-800 mg daily (sedating, useful for agitation, insomnia)
  - **Aripiprazole:** 10-30 mg daily (lower metabolic side effects)
  - **Risperidone:** 2-6 mg daily
- **Combination:** Lithium/valproate + antipsychotic (severe mania, mixed episode)

**Adjunctive:**
- **Benzodiazepines:** Lorazepam 1-2 mg PO/IM q4-6h PRN (agitation, insomnia)
- **ECT:** Consider for severe mania, pregnancy, refractory to pharmacotherapy

**Acute Bipolar Depression:**

**Pharmacotherapy:**
- **Quetiapine:** 300-600 mg daily (only FDA/EMA-approved antipsychotic for bipolar depression)
- **Lurasidone:** 20-120 mg daily (FDA-approved for bipolar depression)
- **Olanzapine-fluoxetine combination (OFC):** Olanzapine 6-12 mg + Fluoxetine 25-50 mg daily
- **Lithium/valproate:** May help (if already taking for maintenance)
- **Antidepressants:** **CONTROVERSIAL** - may switch to mania (add mood stabilizer)

**Maintenance Treatment:**

**Goals:**
- **Prevent recurrence** of mania/depression
- **Reduce suicide risk**
- **Improve functioning**

**First-line:**
- **Lithium:** Most effective for classic Bipolar I (euphoric mania, depression-free intervals)
  - **Anti-suicidal** (reduces suicide risk by 80%)
  - **Maintenance:** Serum level 0.6-1.0 mmol/L
  - **Monitoring:** Serum levels every 3 months (more frequently if dose changes), TFTs, U&Es, calcium, ECG
  - **Duration:** Indefinite (lifelong)

**Alternatives:**
- **Valproate:** Bipolar I with rapid cycling, mixed episodes, comorbid anxiety/substance use
  - **Monitoring:** LFTs, serum levels (every 3-6 months)
- **Lamotrigine:** 100-200 mg daily (prevents bipolar depression more than mania)
  - **Slow titration** (risk of Stevens-Johnson syndrome)
  - **Monitoring:** CBC, LFTs (rare hepatotoxicity, blood dyscrasias)
- **Olanzapine:** Prevents mania and depression (but metabolic side effects limit use)
- **Quetiapine:** Prevents mania and depression

**Psychosocial Interventions:**
- **Psychoeducation:** Recognize early warning signs, medication adherence, lifestyle (sleep, substances)
- **CBT for bipolar disorder:** Mood monitoring, activity scheduling, challenge automatic thoughts, relapse prevention
- **Interpersonal and Social Rhythm Therapy (IPSRT):** Stabilize daily routines, sleep-wake cycle (prevent mania)
- **Family-focused therapy:** Improve communication, reduce expressed emotion

**Lifestyle:**
- **Sleep hygiene:** Regular sleep-wake cycle (sleep deprivation triggers mania)
- **Avoid:** Alcohol, cannabis, stimulants (caffeine, cocaine, amphetamines)
- **Stress management:** Mindfulness, relaxation techniques
- **Routine:** Regular meals, exercise, social activities

**Prognosis:**
- **Course:** Episodic with inter-episode recovery (most common), rapid cycling (≥ 4 episodes/year), continuous
- **Functional recovery:** 30-60% (lower than unipolar depression)
- **Predictors of good outcome:** Early diagnosis, good premorbid functioning, good adherence, no comorbidities
- **Predictors of poor outcome:** Early onset, psychotic symptoms, substance use, rapid cycling, mixed episodes, long duration before treatment

**Sources:** NICE CG185, BAP 2018, CANMAT/ISBD 2018"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "mental_health_mood",
                "focus": "bipolar_disorder",
                "sources": ["NICE CG185", "BAP 2018", "CANMAT/ISBD 2018"]
            }
        )

    def _handle_depression(self, query: str, context: dict) -> DomainQueryResult:
        """Handle depression queries"""
        answer = """**Depression Management**

**Definition:**
- **Major depressive disorder (MDD):** Depressed mood/loss of interest + ≥ 5 symptoms for ≥ 2 weeks
- **Persistent depressive disorder (dysthymia):** Milder symptoms for ≥ 2 years

**Epidemiology:**
- **Lifetime prevalence:** 15-20% (women > men 2:1)
- **Age of onset:** 20-30 years (can occur at any age)
- **Recurrence:** 50% (after 1 episode), 70% (after 2 episodes), 90% (after 3 episodes)
- **Suicide risk:** 2-5% lifetime

**Clinical Features:**

**Core Symptoms (Required for diagnosis):**
1. **Depressed mood** (sad, empty, hopeless) most of day, nearly every day
2. **Anhedonia** (loss of interest/pleasure in activities) most of day, nearly every day

**Additional Symptoms (≥ 5 total, including ≥ 1 core):**
3. **Weight/appetite change** (loss or gain)
4. **Sleep disturbance** (insomnia or hypersomnia)
5. **Psychomotor change** (agitation or retardation)
6. **Fatigue**, **loss of energy**
7. **Worthlessness**, **guilt** (excessive, inappropriate)
8. **Difficulty concentrating**, **indecisiveness**
9. **Recurrent thoughts of death**, **suicidal ideation**

**Specifiers:**

**Severity:**
- **Mild:** 5 symptoms, minimal impairment
- **Moderate:** 6-7 symptoms, impairment
- **Severe:** 8-9 symptoms, marked impairment
- **With psychotic features:** Hallucinations, delusions (mood-congruent - guilt, worthlessness; mood-incongruent - persecution)

**Atypical Features:**
- **Mood reactivity:** Mood brightens to positive events
- **Leaden paralysis:** Heavy, leaden feelings in arms/legs
- **Increased appetite**, **weight gain**
- **Hypersomnia** (sleeping > 10 hours/day)
- **Interpersonal rejection sensitivity** (easily hurt by criticism/rejection)

**Melancholic Features:**
- **Anhedonia:** No pleasure in activities (even if good things happen)
- **Depressed mood** worse in morning
- **Early morning awakening** (≥ 2 hours early)
- **Psychomotor retardation**, **weight loss**
- **Excessive guilt**

**Peripartum Onset:**
- **During pregnancy** or **within 4 weeks postpartum**
- **Requires urgent treatment** (maternal and infant bonding at risk)

**Seasonal Pattern:**
- **Fall/winter onset**, **spring/summer remission** (≥ 2 years)
- **Treatment:** Light therapy (10,000 lux, 30-60 min daily, morning), antidepressant

**Differential Diagnosis:**
- **Bipolar disorder** (current or past mania/hypomania - antidepressants may switch to mania)
- **Medical:** Hypothyroidism, anemia, vitamin B12/folate deficiency, medications (beta-blockers, steroids), neurological disorders (stroke, Parkinson's), chronic illness (cancer, chronic pain)
- **Substance-induced:** Alcohol, opioids, cannabis, stimulants
- **Grief/bereavement** (normal vs prolonged grief disorder)
- **Adjustment disorder** (stress-related, < 6 months)

**Assessment:**
- **Screening tools:** PHQ-9, PHQ-2, Beck Depression Inventory (BDI)
- **Suicide risk assessment:** Always ask about suicidal thoughts, plans, means, intent
- **Collateral history:** Family, partner (patient may minimize symptoms)
- **Physical examination:** Exclude medical causes (thyroid exam, neurological exam)
- **Laboratory tests:** TSH, CBC, electrolytes, calcium, glucose, LFTs, vitamin B12, folate
- **Substance use:** Urine drug screen, alcohol use (CAGE, AUDIT)

**Treatment:**

**Mild Depression:**

**Watchful Waiting:**
- **Reassure** that many mild cases resolve spontaneously
- **Regular review** (2-4 weeks)
- **Lifestyle:** Exercise, sleep hygiene, alcohol reduction, social activities

**Low-Intensity Psychological Interventions:**
- **Guided self-help:** CBT-based workbooks, online CBT
- **Computerized CBT (cCBT):** Beating the Blues, MoodGYM
- **Group-based CBT:** Psychoeducation, cognitive restructuring, behavioral activation
- **Individual CBT:** 6-12 sessions

**Moderate-Severe Depression:**

**Psychotherapy:**
- **CBT:** 16-20 sessions (first-line)
- **IPT (Interpersonal Therapy):** 12-16 sessions (focus on grief, role disputes, role transitions, interpersonal deficits)
- **Psychodynamic psychotherapy:** Long-term (personality factors, unresolved conflicts)

**Pharmacotherapy:**

**First-line Antidepressants:**

**SSRIs (Selective Serotonin Reuptake Inhibitors):**
- **Fluoxetine (Prozac):** 20-40 mg daily (first-line, activating, long half-life - easier to stop)
- **Citalopram (Celexa):** 20-40 mg daily (first-line, less drug interactions)
- **Escitalopram (Lexapro):** 10-20 mg daily (most selective SSRI, first-line)
- **Sertraline (Zoloft):** 50-200 mg daily (first-line, good for comorbid anxiety)
- **Paroxetine (Paxil):** 20-40 mg daily (more anticholinergic side effects, harder to stop - discontinuation syndrome)
- **Dose:** Start low, titrate to therapeutic dose over 1-2 weeks
- **Onset:** 2-4 weeks (improvement in sleep, appetite first - energy before mood)
- **Duration:** Continue for 6-9 months after remission (first episode), 2+ years (recurrent)
- **Side effects:** Nausea, diarrhea, headache, insomnia/somnolence, sexual dysfunction (delayed orgasm, anorgasmia), weight gain, agitation, anxiety
- **Discontinuation syndrome:** Dizziness, nausea, "electric shock" sensation (taper over 2-4 weeks)

**SNRIs (Serotonin-Norepinephrine Reuptake Inhibitors):**
- **Venlafaxine (Effexor):** 75-225 mg daily (first-line, good for severe depression, neuropathic pain)
  - **Dose-dependent:** SNRI at low dose (75 mg), SRI at higher dose (150+ mg)
  - **Side effects:** Hypertension (dose-dependent), nausea, sexual dysfunction
- **Duloxetine (Cymbalta):** 30-60 mg daily (good for comorbid pain, neuropathic pain, fibromyalgia)

**Second-line:**

**Mirtazapine (Remeron):**
- **Mechanism:** Alpha-2 antagonist, 5-HT2/5-HT3 antagonist (increases norepinephrine, serotonin release)
- **Dose:** 15-45 mg at night (sedating, good for insomnia, low appetite)
- **Side effects:** Sedation, weight gain (increased appetite), dry mouth, constipation
- **Advantages:** No sexual dysfunction, no nausea (antagonist at 5-HT3), helps sleep

**Bupropion (Wellbutrin):**
- **Mechanism:** Norepinephrine-dopamine reuptake inhibitor (NDRI)
- **Dose:** 150-300 mg daily (SR or XL formulation)
- **Indications:** Depression, seasonal affective disorder, smoking cessation
- **Advantages:** No sexual dysfunction, weight loss, energizing (good for hypersomnia, fatigue)
- **Contraindications:** Seizure disorder, eating disorders (anorexia, bulimia), head trauma, brain tumor
- **Side effects:** Insomnia, agitation, dry mouth

**Tricyclic Antidepressants (TCAs):**
- **Amitriptyline:** 50-150 mg at night (sedating, good for insomnia, neuropathic pain)
- **Nortriptyline:** 50-150 mg at night (less sedating, better tolerated)
- **Imipramine:** 50-150 mg at night (less sedating)
- **Indications:** Severe depression, neuropathic pain, migraine prophylaxis
- **Side effects:** Anticholinergic (dry mouth, constipation, blurred vision, urinary retention), orthostatic hypotension, sedation, weight gain, cardiac toxicity (arrhythmias)
- **Toxicity:** Fatal in overdose (≤ 1 week supply)
- **Monitoring:** ECG (if > 50 years, cardiac risk factors)

**MAOIs (Monoamine Oxidase Inhibitors):**
- **Phenelzine:** 30-60 mg daily
- **Indications:** Atypical depression (with hypersomnia, hyperphagia), refractory depression
- **Contraindications:** Tyramine-rich foods (aged cheese, cured meats, red wine, tap beer), SSRIs/SNRIs (serotonin syndrome risk)
- **Side effects:** Hypertensive crisis (tyramine), orthostatic hypotension, insomnia, weight gain, sexual dysfunction

**Treatment-Resistant Depression:**

**Definition:**
- **Failure to respond** to 2 adequate antidepressant trials (6 weeks each at therapeutic dose)
- **Prevalence:** 30-50%

**Strategies:**
1. **Optimize current antidepressant:** Dose, duration, adherence
2. **Switch antidepressant:** Different class (SSRI → SNRI, SSRI → bupropion)
3. **Augmentation:**
   - **Lithium:** 600-1200 mg daily (serum level 0.4-0.8 mmol/L) - most effective
   - **Atypical antipsychotic:** Quetiapine 150-300 mg daily, Aripiprazole 2-10 mg daily (FDA/EMA-approved augmentation)
   - **T3 (liothyronine):** 25-50 mcg daily (if hypothyroid, euthyroid)
4. **Combination:** Two antidepressants from different classes (SSRI + bupropion)
5. **Psychotherapy:** CBT, IPT (if not already done)
6. **Neuromodulation:**
   - **ECT:** Electroconvulsive therapy (severe, psychotic, refractory depression - most effective)
   - **rTMS:** Repetitive transcranial magnetic stimulation (non-invasive, less effective than ECT)
   - **VNS:** Vagus nerve stimulation (chronic refractory depression)
   - **DBS:** Deep brain stimulation (investigational)

**Suicide Risk Management:**
- **Assess:** Current suicidal thoughts, plans, means, intent, previous attempts
- **Protect:** Remove access to means, hospitalize if high risk
- **Treat:** Hospitalization, ECT (if severe), increase monitoring (more frequent follow-up)
- **Document:** Suicide risk assessment, safety plan

**Sources:** NICE CG90, APA Practice Guidelines 2010, CANMAT 2016"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "mental_health_mood",
                "focus": "depression_management",
                "sources": ["NICE CG90", "APA 2010", "CANMAT 2016"]
            }
        )

    def _handle_anxiety(self, query: str, context: dict) -> DomainQueryResult:
        """Handle anxiety queries"""
        answer = """**Anxiety Disorders Management**

**Classification:**

**Generalized Anxiety Disorder (GAD):**
- **Excessive worry** about multiple things (work, health, family, finances) most days for ≥ 6 months
- **Difficult to control worry**
- **≥ 3 physical symptoms:** Restlessness, fatigue, difficulty concentrating, irritability, muscle tension, sleep disturbance

**Panic Disorder:**
- **Recurrent panic attacks** (± agoraphobia)
- **Panic attack:** Abrupt surge of intense fear/discomfort reaching peak within 10 minutes
  - **Symptoms (≥ 4):** Palpitations, sweating, trembling, shortness of breath, choking, chest pain, nausea, dizziness, chills/hot flashes, paresthesias, derealization/depersonalization, fear of losing control/going crazy, fear of dying
- **Persistent worry** about having another panic attack or consequences (losing control, heart attack)
- **Behavioral changes:** Avoidance of situations associated with panic attacks

**Social Anxiety Disorder (Social Phobia):**
- **Fear of social situations** where scrutiny is possible (public speaking, meeting new people, eating in public)
- **Fear of negative evaluation** (embarrassment, humiliation, rejection)
- **Anxiety** is disproportionate to situation
- **Avoidance** of social situations or endured with intense anxiety

**Specific Phobias:**
- **Marked fear** of specific object/situation (animals, heights, injections, blood, flying)
- **Immediate anxiety** upon exposure
- **Avoidance** of phobic stimulus

**Agoraphobia:**
- **Fear** of situations where escape might be difficult or help unavailable (crowds, public transport, open spaces, enclosed spaces, being outside home alone)
- **Avoidance** of agoraphobic situations or requires companion

**Epidemiology:**
- **Lifetime prevalence:** GAD (5-7%), panic disorder (2-3%), social anxiety (7-13%), specific phobia (10-15%), agoraphobia (1-2%)
- **Gender:** Women > men (2:1 for GAD, panic disorder, specific phobias)
- **Age of onset:** GAD (30-40 years), panic disorder (20-30 years), social anxiety (adolescence)

**Differential Diagnosis:**
- **Medical:** Hyperthyroidism, arrhythmias, asthma, COPD, seizures, vestibular disorders, pheochromocytoma
- **Substance-induced:** Caffeine, alcohol withdrawal, stimulants (cocaine, amphetamines), cannabis, medications (beta-agonists, SSRIs)
- **Psychiatric:** Depression (anxiety common comorbidity), bipolar disorder, psychosis, PTSD, OCD

**Assessment:**
- **Screening tools:** GAD-7 (GAD), GAD-2 (GAD, panic, social anxiety)
- **Medical evaluation:** Exclude organic causes (TSH, ECG, fasting glucose, medications, substances)
- **Suicide risk:** Anxiety disorders associated with increased suicide risk (especially panic disorder, comorbid depression)

**Treatment:**

**Generalized Anxiety Disorder (GAD):**

**Mild GAD:**
- **Psychoeducation:** Anxiety is normal, adaptive (problem-solving), excessive anxiety is maladaptive
- **Watchful waiting:** Regular review (2-4 weeks)
- **Low-intensity interventions:** Guided self-help, cCBT, group psychoeducation

**Moderate-Severe GAD:**

**Psychotherapy:**
- **CBT:** First-line (12-20 sessions)
  - **Cognitive:** Challenge worry thoughts (probability, overestimation of threat, catastrophizing)
  - **Behavioral:** Problem-solving (structured approach to real-life problems), exposure (avoidance reduction), relaxation (deep breathing, progressive muscle relaxation, mindfulness)
  - **Metacognitive therapy:** Challenge beliefs about worry (worry is uncontrollable, dangerous, helpful)
  - **Acceptance and Commitment Therapy (ACT):** Accept anxiety, commit to values-based action

**Pharmacotherapy:**

**First-line:**
- **SSRIs:**
  - **Escitalopram:** 10-20 mg daily
  - **Sertraline:** 50-200 mg daily
  - **Paroxetine:** 20-40 mg daily
  - **Citalopram:** 20-40 mg daily
  - **Onset:** 2-4 weeks (improvement in anxiety, worry first)
  - **Duration:** 6-12 months (first episode), 2+ years (recurrent)
  - **Taper:** Gradual (2-4 weeks) to avoid discontinuation syndrome

- **SNRIs:**
  - **Venlafaxine XR:** 75-225 mg daily (first-line, especially if comorbid depression)
  - **Duloxetine:** 30-60 mg daily (first-line, good for GAD with pain)

**Second-line:**
- **Mirtazapine:** 15-45 mg at night (if insomnia, low appetite)
- **Buspirone:** 15-30 mg BID-TID (non-sedating, no sexual dysfunction, no dependence - but slow onset 2-4 weeks, less effective than SSRIs)
- **Pregabalin:** 150-600 mg daily (if refractory, especially if comorbid neuropathic pain)

**Benzodiazepines (Short-term, Second-line):**
- **Indications:** Severe anxiety, acute distress, while waiting for SSRI/SNRI to take effect
- **Agents:**
  - **Diazepam:** 5-10 mg PO TDS-QDS (short-acting, long half-life)
  - **Lorazepam:** 1-2 mg PO TDS-QDS (short-acting, intermediate half-life)
  - **Clonazepam:** 0.5-2 mg PO daily (long-acting, good for GAD, panic)
- **Duration:** 2-4 weeks maximum (risk of dependence, tolerance, withdrawal)
- **Avoid:** Long-term use (except rare cases), use in elderly (falls, confusion, delirium), comorbid depression (suicide risk)

**Panic Disorder:**

**Psychotherapy:**
- **CBT:** First-line (12-20 sessions)
  - **Psychoeducation:** Panic attacks are harmless (no cardiac danger), fear of fear (anticipatory anxiety)
  - **Interoceptive exposure:** Induce panic symptoms (hyperventilation, running in place) to habituate
  - **In vivo exposure:** Confront agoraphobic situations (malls, driving, public transport)
  - **Cognitive restructuring:** Challenge catastrophic misinterpretations of bodily sensations

**Pharmacotherapy:**
- **SSRIs:** First-line (escitalopram, sertraline, paroxetine, citalopram)
- **SNRIs:** Venlafaxine XR 75-225 mg daily
- **Benzodiazepines:** Adjunctive (short-term, while waiting for SSRI/SNRI)
  - **Clonazepam:** 0.5-2 mg daily (long-acting, prevents panic attacks)
  - **Alprazolam:** 0.25-0.5 mg TDS-QDS (short-acting, high abuse potential, avoid)

**Social Anxiety Disorder:**

**Psychotherapy:**
- **CBT:** First-line (12-20 sessions)
  - **Exposure:** Confront feared social situations (public speaking, meeting new people)
  - **Cognitive restructuring:** Challenge negative beliefs about performance (everyone will laugh at me, I'll embarrass myself)
  - **Social skills training:** Role-playing, conversation skills, assertiveness

**Pharmacotherapy:**
- **SSRIs:** First-line (escitalopram, sertraline, paroxetine)
- **SNRIs:** Venlafaxine XR
- **MAOIs:** Phenelzine (if refractory - dietary restrictions, drug interactions limit use)

**Specific Phobias:**

**Psychotherapy:**
- **Exposure therapy:** Gradual exposure to phobic stimulus (systematic desensitization, flooding)
- **CBT:** Combine exposure with cognitive restructuring (challenge catastrophic beliefs)

**Pharmacotherapy:**
- **Benzodiazepines:** PRN before exposure (propranolol sometimes used for performance anxiety)
- **SSRIs:** If multiple phobias, significant impairment

**Agoraphobia:**

**Psychotherapy:**
- **Exposure therapy:** Confront agoraphobic situations (crowds, public transport, open spaces)
- **CBT:** Combine exposure with cognitive restructuring

**Pharmacotherapy:**
- **SSRIs:** First-line
- **Benzodiazepines:** Adjunctive (short-term)

**General Principles:**
- **Combined treatment:** CBT + SSRI/SNRI (more effective than either alone)
- **Regular exercise:** Reduces anxiety (30 min daily, 3-5x/week)
- **Reduce caffeine:** Eliminate or limit caffeine (caffeine mimics anxiety symptoms)
- **Alcohol:** Avoid (reduces anxiety temporarily, increases anxiety next day, interferes with CBT/medications)
- **Sleep hygiene:** Anxiety disrupts sleep, poor sleep worsens anxiety

**Prognosis:**
- **Course:** Chronic (GAD, panic disorder, social anxiety) or episodic (specific phobias)
- **Functional impairment:** Significant (occupational, social, relationships)
- **Comorbidity:** Depression (50%), substance use (20%), other anxiety disorders (30%)
- **Response rates:** CBT (60-70%), SSRIs (60-70%), combined (70-80%)
- **Relapse:** Common (40-60% after discontinuation of treatment)

**Sources:** NICE CG123, NICE CG159, APA Practice Guidelines 2009"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "mental_health_anxiety",
                "focus": "anxiety_disorders",
                "sources": ["NICE CG123", "NICE CG159", "APA 2009"]
            }
        )

    def _handle_ptsd(self, query: str, context: dict) -> DomainQueryResult:
        """Handle PTSD queries"""
        answer = """**Post-Traumatic Stress Disorder (PTSD) Management**

**Definition:**
- **PTSD:** Trauma-related disorder following exposure to actual or threatened death, serious injury, or sexual violation

**Epidemiology:**
- **Lifetime prevalence:** 8-10% (higher in women than men)
- **Trauma exposure:** 60-90% (most exposed do NOT develop PTSD)
- **Risk factors:** Severity, duration, proximity of trauma; prior trauma; childhood adversity; family history of psychiatric disorders; lack of social support

**Diagnostic Criteria (DSM-5):**

**A. Stressor Criterion:**
- **Actual or threatened:** Death, serious injury, sexual violence
- **Exposure:** Direct, witnessing, learning about trauma to close family/friend, repeated exposure to aversive details (first responders, police)

**B. Intrusion Symptoms (≥ 1):**
- **Recurrent, unwanted, distressing memories** of trauma
- **Nightmares** (trauma-related)
- **Flashbacks** (dissociative reactions - feeling as if trauma recurring)
- **Psychological distress** at trauma reminders
- **Physiological reactions** to trauma reminders (heart racing, sweating, shortness of breath)

**C. Avoidance (≥ 1):**
- **Avoid trauma-related memories**, **thoughts**, **feelings**
- **Avoid external reminders** (people, places, conversations, activities, objects, situations)

**D. Negative alterations in cognitions/mood (≥ 2):**
- **Inability to remember** important aspects of trauma (dissociative amnesia)
- **Persistent negative beliefs** about self/others/world (I am bad, no one can be trusted, world is dangerous)
- **Persistent distorted blame** (self or others)
- **Persistent negative emotional state** (fear, horror, anger, guilt, shame)
- **Diminished interest** in activities
- **Feeling detached** or estranged from others
- **Inability to experience positive emotions** (anhedonia)

**E. Arousal/Reactivity (≥ 2):**
- **Irritable behavior**, **angry outbursts** (verbal/physical aggression)
- **Reckless behavior** (self-destructive)
- **Hypervigilance** (excessive scanning for danger)
- **Exaggerated startle response**
- **Problems with concentration**
- **Sleep disturbance** (difficulty falling/staying asleep, restless sleep)

**F. Duration:** > 1 month
**G. Impairment:** Significant distress or impairment in social, occupational, other important areas

**Specifiers:**
- **With dissociative symptoms:** Depersonalization (detached from self), derealization (world unreal, dreamlike)
- **With delayed expression:** Full criteria not met until 6 months after trauma (some symptoms immediately present)

**Comorbidity:**
- **Depression** (40-50%)
- **Anxiety disorders** (40-50%)
- **Substance use disorders** (30-40%)
- **Suicidality** (increased risk)

**Differential Diagnosis:**
- **Acute stress disorder:** Similar symptoms but duration 3 days - 1 month after trauma
- **Adjustment disorder:** Stress-related symptoms not meeting PTSD criteria
- **Depression:** Intrusion, avoidance symptoms absent
- **Grief/bereavement:** Yearning for deceased, no traumatic symptoms
- **TBI:** Similar symptoms (irritability, concentration, memory) but head injury present

**Assessment:**
- **Screening tools:** PCL-5 (PTSD Checklist for DSM-5), PHQ-9 (depression), GAD-7 (anxiety)
- **Trauma history:** Type, severity, duration, perceived life threat, peritraumatic dissociation
- **Risk assessment:** Suicide, self-harm, substance use, risky behaviors, anger, aggression
- **Functional impairment:** Occupational, social, relationships

**Treatment:**

**Psychotherapy (First-line):**

**Trauma-Focused CBT (TF-CBT):**
- **Duration:** 12-16 sessions (90 minutes each)
- **Components:**
  - **Psychoeducation:** PTSD symptoms are normal responses to abnormal events
  - **Anxiety management:** Relaxation training, breathing retraining, thought stopping
  - **Cognitive restructuring:** Challenge trauma-related beliefs (I am to blame, I am weak, world is dangerous, no one can be trusted)
  - **Exposure:** Imaginal exposure (relive trauma memories to reduce fear) + in vivo exposure (confront avoided situations)
  - **Relapse prevention:** Identify triggers, coping strategies

**EMDR (Eye Movement Desensitization and Reprocessing):**
- **Duration:** 6-12 sessions
- **Components:**
  - **History taking:** Trauma memories, target memories
  - **Preparation:** Self-soothing techniques (safe place)
  - **Desensitization:** Recall trauma memory while making eye movements (or taps, tones)
  - **Installation:** Positive cognition (I survived, I'm safe now) paired with trauma memory
  - **Body scan:** Monitor residual physical tension
  - **Closure:** Return to safe place
- **Efficacy:** Similar to TF-CBT (effective for single traumas, less evidence for complex PTSD)

**Pharmacotherapy (Second-line or Comorbid Depression/Anxiety):**

**First-line:**
- **SSRIs:**
  - **Sertraline:** 50-200 mg daily (FDA/EMA-approved for PTSD)
  - **Paroxetine:** 20-40 mg daily (FDA/EMA-approved for PTSD)
  - **Fluoxetine:** 20-60 mg daily (FDA-approved for PTSD)
  - **Escitalopram:** 10-20 mg daily (evidence from studies)
  - **Onset:** 2-4 weeks (intrusion, avoidance improve first; then hyperarousal)
  - **Duration:** 6-12 months (continue if responding, longer if comorbid depression/anxiety)

**Second-line:**
- **SNRIs:** Venlafaxine XR 75-225 mg daily (evidence from studies)
- **Mirtazapine:** 15-45 mg at night (if insomnia, low appetite)

**Avoid:**
- **Benzodiazepines:** Interfere with exposure therapy, prevent emotional processing, risk of dependence (avoid except short-term crisis stabilization)
- **Non-trauma-focused psychotherapy initially:** Supportive therapy, psychodynamic therapy (may be helpful later but not first-line)

**Comorbidity:**
- **Depression:** Add antidepressant (SSRI), include in trauma-focused CBT (depression symptoms improve with PTSD treatment)
- **Substance use:** Integrated treatment (treat PTSD and substance use simultaneously), trauma-focused therapies adapted for substance use disorders
- **Suicidality:** Monitor closely, crisis plan, hospitalize if acute risk

**Prognosis:**
- **Recovery:** 30-50% within 3 months without treatment, 50-70% with treatment
- **Chronic PTSD:** 30-40% (symptoms persist for years)
- **Predictors of good outcome:** Early treatment, social support, good premorbid functioning, no comorbidities, single trauma (vs multiple traumas)
- **Predictors of poor outcome:** Chronic PTSD, multiple traumas (complex PTSD), comorbid depression/substance use, poor social support, severe trauma (sexual assault, combat)

**Sources:** NICE NG116, APA Practice Guidelines 2017, ISTSS 2019"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "mental_health_trauma",
                "focus": "ptsd_management",
                "sources": ["NICE NG116", "APA 2017", "ISTSS 2019"]
            }
        )

    def _handle_ocd(self, query: str, context: dict) -> DomainQueryResult:
        """Handle OCD queries"""
        answer = """**Obsessive-Compulsive Disorder (OCD) Management**

**Definition:**
- **Obsessions:** Recurrent, intrusive, unwanted thoughts, images, or urges (egodystonic - recognized as own thoughts, distressing)
- **Compulsions:** Repetitive behaviors or mental acts performed in response to obsessions (to reduce anxiety/distress, prevent feared outcome)
- **Time-consuming:** > 1 hour/day, cause significant impairment

**Epidemiology:**
- **Lifetime prevalence:** 1-3%
- **Gender:** Equal (males earlier onset than females)
- **Age of onset:** Bimodal (early: 10-12 years; late: 20-25 years)
- **Course:** Chronic, waxing-waning (worsens with stress)

**Clinical Features:**

**Common Obsessions:**
- **Contamination:** Germs, dirt, chemicals, bodily fluids (feces, urine)
- **Doubting:** Did I lock the door? Turn off the stove? Hurt someone?
- **Symmetry/ordering:** Things must be just right, arranged symmetrically
- **Aggressive:** Harming self/others (e.g., stabbing someone, sexual intrusive thoughts)
- **Sexual:** Forbidden, immoral sexual thoughts, images
- **Religious:** Blasphemous thoughts, sinful thoughts
- **Hoarding:** Can't throw anything away (fear of losing something important)
- **Health:** Having a serious illness (cancer, AIDS)

**Common Compulsions:**
- **Washing/cleaning:** Hand washing, showering, cleaning (contamination obsessions)
- **Checking:** Repeatedly checking locks, appliances, car, homework (doubting obsessions)
- **Counting:** Repeating actions a certain number of times (symmetry obsessions)
- **Ordering/arranging:** Lining up objects symmetrically (symmetry obsessions)
- **Mental rituals:** Praying, repeating words, counting, reviewing (all obsessions)
- **Hoarding:** Collecting, saving items (hoarding obsessions)
- **Seeking reassurance:** Asking others for reassurance (doubting obsessions)

**Insight:**
- **Good/fair insight:** Recognize obsessions/compulsions are excessive/unreasonable (most patients)
- **Poor insight:** Believe obsessions/compulsions are reasonable (10-20%)
- **Absent insight:** Delusional beliefs (no insight) (< 5%)

**Comorbidity:**
- **Depression:** 30-50% (most common comorbidity)
- **Anxiety disorders:** 30-40% (GAD, panic disorder, social anxiety, specific phobias)
- **Tourette's/tic disorders:** 5-10% (shared genetic vulnerability)
- **OCD-related disorders:** Body dysmorphic disorder, hoarding disorder, trichotillomania, excoriation disorder, hypochondriasis

**Differential Diagnosis:**
- **GAD:** Worry (obsessions) are about real-life problems, not intrusive, resisted less successfully
- **Psychosis:** OCD patients have insight (recognize thoughts as own thoughts, ego-dystonic), psychotic patients lack insight (delusional, ego-syntonic)
- **Tourette's:** Tics are less complex, preceded by premonitory urge, relieved by tic, not resisted
- **OCPD (Obsessive-Compulsive Personality Disorder):** Perfectionism, rigidity, hoarding, miserliness (ego-syntonic, patient doesn't see problem)
- **Autism spectrum:** Repetitive behaviors, restricted interests, lack flexibility (ego-syntonic)

**Assessment:**
- **Screening tools:** Y-BOCS (Yale-Brown Obsessive Compulsive Scale), OCI-R (Obsessive-Compulsive Inventory-Revised)
- **History:** Onset, triggers, stressors, functional impairment, insight
- **Family history:** OCD, Tourette's, tics (autosomal dominant, incomplete penetrance)
- **Comorbidity:** Depression, anxiety, tics, autism spectrum

**Treatment:**

**Psychotherapy (First-line):**

**Exposure and Response Prevention (ERP):**
- **Duration:** 12-20 sessions (90 minutes each, twice weekly preferred)
- **Mechanism:** Habituation (reduced fear with repeated exposure) + inhibitory learning (fear doesn't come true despite no compulsion)
- **Components:**
  - **Psychoeducation:** OCD cycle (obsession → anxiety → compulsion → temporary relief → obsession returns stronger)
  - **Hierarchy:** Rank fears from least to most distressing
  - **Exposure:** Confront feared situation (e.g., touch doorknob, not wash hands)
  - **Response prevention:** Delay or prevent compulsion (e.g., wait 1 hour before washing, don't wash at all)
  - **Homework:** Daily ERP practice between sessions (15-30 minutes, gradually increasing)
  - **Relapse prevention:** Identify triggers, early warning signs, booster sessions

**Cognitive Therapy (CT) for OCD:**
- **Duration:** 12-20 sessions
- **Components:**
  - **Cognitive restructuring:** Challenge OCD beliefs (overinflated responsibility, overestimation of threat, intolerance of uncertainty, thought-action fusion, importance of thoughts, need to control thoughts)
  - **Beliefs:**
    - **Overinflated responsibility:** "If I don't wash my hands, someone will get sick and it will be my fault"
    - **Overestimation of threat:** "If I don't check the stove, my house will burn down"
    - **Intolerance of uncertainty:** "I must be 100% certain"
    - **Thought-action fusion:** "If I think about stabbing someone, I might do it"
    - **Importance of thoughts:** "Having bad thoughts means I'm a bad person"
    - **Need to control thoughts:** "I must control my thoughts or something terrible will happen"

**Pharmacotherapy (First-line, moderate-severe OCD):**

**First-line:**

**SSRIs (High Doses Required):**
- **Fluoxetine (Prozac):** 40-80 mg daily (start 20 mg, increase by 20 mg every 2-4 weeks)
- **Sertraline (Zoloft):** 150-200 mg daily (start 50 mg, increase by 50 mg every 2-4 weeks)
- **Paroxetine (Paxil):** 40-60 mg daily (start 20 mg, increase by 20 mg every 2-4 weeks)
- **Fluvoxamine (Luvox):** 200-300 mg daily (start 50 mg, increase by 50 mg every 2-4 weeks) - FDA-approved for OCD
- **Escitalopram (Lexapro):** 20-40 mg daily (start 10 mg, increase by 10 mg every 2-4 weeks)
- **Citalopram (Celexa):** 40-60 mg daily (start 20 mg, increase by 20 mg every 2-4 weeks)
- **Onset:** 6-12 weeks (slower than depression, require higher doses)
- **Duration:** 12-24 months (continue if responding, longer if comorbid depression/anxiety)
- **Taper:** Gradual (2-4 weeks) to avoid discontinuation syndrome

**Second-line:**

**Clomipramine (Anafranil):**
- **Mechanism:** Tricyclic antidepressant (potent SRI - serotonin reuptake inhibitor)
- **Dose:** 150-250 mg daily (start 25 mg, increase by 25 mg every 3-7 days)
- **Efficacy:** More effective than SSRIs (but more side effects)
- **Side effects:** Anticholinergic (dry mouth, constipation, blurred vision, urinary retention), sedation, weight gain, sexual dysfunction, cardiac toxicity (arrhythmias)
- **Monitoring:** ECG (if > 50 years, cardiac risk factors), therapeutic drug monitoring (levels not routinely required)

**Augmentation (if inadequate response to SSRI monotherapy):**

**Antipsychotics:**
- **Risperidone:** 0.5-2 mg daily (added to SSRI)
- **Haloperidol:** 2-5 mg daily (added to clomipramine or SSRI)
- **Aripiprazole:** 2-10 mg daily (added to SSRI)
- **Indications:** Poor response to SSRI alone, comorbid tics (Tourette's), psychotic features (poor insight)

**Other augmentation strategies:**
- **Buspirone:** 15-30 mg BID (if comorbid anxiety)
- **Memantine:** 10-20 mg daily (glutamatergic agent - investigational)
- **Lamotrigine:** 100-200 mg daily (glutamate modulator - investigational)

**Refractory OCD (failure to respond to adequate SSRI + ERP trial):**
- **Switch SSRI** (try another SSRI)
- **Switch to clomipramine**
- **Combination:** SSRI + clomipramine (watch for serotonin syndrome)
- **Antipsychotic augmentation** (risperidone, haloperidol, aripiprazole)
- **Intravenous clomipramine** (specialist clinics)
- **Neuromodulation:** Deep brain stimulation (DBS) (investigational, highly selected cases)

**Prognosis:**
- **Course:** Chronic, waxing-waning (worsens with stress)
- **Functional impairment:** Significant (occupational, social, relationships)
- **Response rates:** ERP (60-70%), SSRIs (40-60%), combined (70-80%)
- **Remission:** 20-30% (minimal residual symptoms)
- **Relapse:** Common if treatment stopped (continue long-term)

**Sources:** NICE CG31, APA Practice Guidelines 2007, BAP 2013"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "mental_health_ocd",
                "focus": "ocd_management",
                "sources": ["NICE CG31", "APA 2007", "BAP 2013"]
            }
        )

    def _handle_dementia(self, query: str, context: dict) -> DomainQueryResult:
        """Handle dementia queries"""
        answer = """**Dementia Assessment and Management**

**Definition:**
- **Dementia:** Acquired progressive cognitive decline (memory, executive function, language, visuospatial, personality) sufficient to impair social/occupational functioning, not due to delirium

**Epidemiology:**
- **Prevalence:** Age-related (5% age 65-70, 20% age 80-85, 40% age 90+)
- **Incidence:** 1-2% per year (age 65+)
- **Risk factors:** Age, genetics (APOE ε4 allele), cardiovascular risk factors (hypertension, diabetes, hyperlipidemia, smoking, obesity), low education, head trauma, social isolation, hearing loss

**Etiology:**

**Alzheimer's Disease (60-70%):**
- **Progressive memory loss**, **episodic memory** (learning new information) affected first
- **Language:** Anomia (word-finding difficulty), circumlocution
- **Visuospatial:** Getting lost (even in familiar places)
- **Executive:** Poor judgment, planning, abstraction
- **Personality:** Apathy, withdrawal, irritability (later)
- **Imaging:** Medial temporal lobe atrophy (hippocampus) on MRI

**Vascular Dementia (10-20%):**
- **Stepwise decline** (worsening after each stroke)
- **Patchy cognitive deficits** (depending on location of infarcts)
- **Executive dysfunction**, **slowing**, **gait disturbance**
- **Risk factors:** Hypertension, diabetes, hyperlipidemia, smoking, stroke, TIA
- **Imaging:** Multiple infarcts, white matter changes, lacunes on CT/MRI

**Lewy Body Dementia (10-15%):**
- **Fluctuating cognition** (good days, bad days)
- **Visual hallucinations** (well-formed, detailed, people, animals)
- **Parkinsonism** (bradykinesia, rigidity, tremor)
- **REM sleep behavior disorder** (act out dreams, shout, punch, kick while asleep)
- **Neuroleptic sensitivity** (severe reactions to antipsychotics - confusion, rigidity, fever, rhabdomyolysis)
- **Intrusion:** Overlap with Parkinson's disease dementia, Alzheimer's disease

**Frontotemporal Dementia (5-10%):**
- **Behavioral variant FTD:** Personality change, disinhibition, apathy, loss of social awareness, hyperorality, dietary changes (sweet foods), compulsions
- **Primary progressive aphasia:** Language decline (non-fluent variant, semantic variant)
- **Age of onset:** Younger (50-65 years)
- **Imaging:** Frontal and/or temporal atrophy on MRI

**Other causes:**
- **Normal pressure hydrocephalus:** Triad of gait apraxia, urinary incontinence, dementia (treatable with shunt)
- **Brain tumor:** Frontal lobe tumors, meningioma (slowly progressive, focal signs)
- **Subdural hematoma:** Chronic, bilateral (especially in elderly, falls, alcoholism, anticoagulation)
- **Prion disease:** Creutzfeldt-Jakob disease (rapidly progressive dementia, myoclonus, characteristic EEG, MRI, brain biopsy)

**Differential Diagnosis:**

**Delirium (Acute Confusion):**
- **Acute onset** (hours-days)
- **Fluctuating course** (worse at night - sundowning)
- **Inattention** (easily distracted, difficulty focusing)
- **Disorganized thinking** (rambling, illogical)
- **Altered level of consciousness** (lethargy, stupor, agitation)
- **Medical causes:** Medications, dehydration, infection, metabolic disturbances, hypoxia, stroke, seizures

**Depression (Pseudodementia):**
- **Memory complaints** (but performance on testing is better than complaints)
- **"I don't know"** responses (lack of effort, not true memory loss)
- **Depressed mood**, **anhedonia**, **suicidal thoughts**, **somatic complaints**
- **Responds to antidepressants** (cognitive improvement with mood improvement)

**Mild Cognitive Impairment (MCI):**
- **Cognitive decline** (memory, executive function) > 1.5 SD below age/education-matched controls
- **Preserved activities of daily living** (not dementia)
- **Progression to dementia:** 10-15% per year (vs 1-2% in normal elderly)

**Assessment:**

**History:**
- **Onset:** Gradual (Alzheimer's), stepwise (vascular), younger onset (FTD), acute (delirium)
- **Progression:** Progressive (dementia), fluctuating (LBD, delirium), static (depression)
- **Functional impairment:** ADLs (bathing, dressing, toileting, transferring, feeding) - 5 ADLs, IADLs (shopping, cooking, managing medications, finances, transportation, housework, telephone) - 8 IADLs
- **Collateral history:** Family, caregiver (patient lacks insight, minimizes symptoms)

**Cognitive Testing:**
- **MMSE (Mini-Mental State Examination):** 0-30 (mild 20-24, moderate 10-19, severe < 10)
- **MoCA (Montreal Cognitive Assessment):** 0-30 (more sensitive than MMSE for MCI, vascular dementia, FTD)
- **Clock drawing test:** Executive function, visuospatial (abnormal in Alzheimer's, vascular dementia, LBD)

**Physical Examination:**
- **Neurological exam:** Look for focal signs (stroke, tumor), Parkinsonism (LBD), gait disturbance (vascular, NPH)
- **Cardiovascular exam:** Hypertension, arrhythmias (atrial fibrillation), carotid bruits (vascular dementia)
- **Medication review:** Anticholinergics (bladder antispasmodics, antihistamines, tricyclics, antipsychotics), benzodiazepines, opioids (can worsen cognition)

**Laboratory Tests (Rule out reversible causes):**
- **CBC** (anemia, infection)
- **Electrolytes** (Na+, K+, Ca2+, glucose)
- **TSH** (hypothyroidism)
- **Vitamin B12**, **folate** (deficiency)
- **Syphilis serology** (neurosyphilis)
- **HIV** (HIV-associated dementia)
- **Liver function tests** (liver failure)
- **Toxicology** (medications, substances)

**Imaging:**
- **CT head:** Exclude tumor, subdural hematoma, NPH, vascular dementia (infarcts, white matter changes)
- **MRI brain:** Atrophy patterns (medial temporal - Alzheimer's; frontal/temporal - FTD; infarcts - vascular), hippocampal volumetry (early Alzheimer's), DaT scan (LBD vs Alzheimer's)

**Management:**

**Non-Pharmacological:**

**Cognitive Stimulation:**
- **Activities:** Puzzles, games, reading, music, art, crafts (maintain function, improve quality of life)
- **Reality orientation:** Calendars, clocks, orientation boards, frequent reminders of date, time, place

**Communication:**
- **Speak clearly**, **slowly**, **simple sentences**
- **Maintain eye contact**, **use gestures**
- **Give one instruction at a time**
- **Avoid correcting** (validation therapy - enter their reality, don't argue)

**Safety Measures:**
- **Driving:** Assess fitness to drive (report to licensing authority if unsafe)
- **Wandering:** ID bracelet, tracking device, door alarms, register with local police (Safe Return program)
- **Falls:** Remove hazards, install grab bars, improve lighting
- **Kitchen:** Remove hazards (sharp objects, medications, stove - unplug or use safety knobs)

**Caregiver Support:**
- **Respite care:** Give caregiver a break (adult day programs, respite care facilities)
- **Support groups:** Alzheimer's Association, caregiver support groups
- **Education:** Disease progression, managing behaviors, caregiver self-care
- **Advance care planning:** Lasting power of attorney, living will, end-of-life care wishes

**Pharmacological (Symptomatic, NOT disease-modifying):**

**Cholinesterase Inhibitors (Mild-Moderate Alzheimer's):**
- **Donepezil (Aricept):** 5-10 mg daily (first-line, good tolerability)
- **Rivastigmine (Exelon):** 1.5-6 mg BID (patch or oral, good for vascular dementia, LBD)
- **Galantamine (Razadyne):** 8-24 mg daily (moderate-severe Alzheimer's)
- **Mechanism:** Inhibit acetylcholinesterase (increase acetylcholine in brain)
- **Efficacy:** Modest (1-3 point improvement on MMSE, maintain function for 6-12 months)
- **Side effects:** Nausea, vomiting, diarrhea, anorexia, weight loss, bradycardia (caution with cardiac disease), syncope
- **Monitoring:** Weight, appetite, side effects (titrate slowly)

**Memantine (Moderate-Severe Alzheimer's):**
- **Dose:** 10-20 mg daily
- **Mechanism:** NMDA receptor antagonist (reduces glutamate excitotoxicity)
- **Indications:** Moderate-severe Alzheimer's (MMSE < 20), vascular dementia, LBD
- **Efficacy:** Modest (maintain function, reduce agitation, caregiver burden)
- **Side effects:** Dizziness, headache, confusion (less side effects than cholinesterase inhibitors)
- **Combination:** Memantine + cholinesterase inhibitor (more effective than either alone)

**Antipsychotics (BPSD - Behavioral and Psychological Symptoms of Dementia):**

**Indications:**
- **Agitation**, **aggression**, **psychosis** (hallucinations, delusions) causing distress or danger
- **Severe symptoms** (danger to patient or others, not responding to non-pharmacological interventions)

**Agents:**
- **Risperidone:** 0.5-2 mg daily (first-line, black box warning - increased mortality in dementia patients)
- **Aripiprazole:** 2-10 mg daily (first-line, lower mortality risk)
- **Quetiapine:** 12.5-100 mg daily (second-line, sedating, useful for insomnia, agitation)

**Duration:**
- **Short-term** (up to 12 weeks) - reassess regularly, taper if symptoms improved or no response
- **Black box warning:** Increased mortality (1.6-1.7x higher in dementia patients on antipsychotics vs placebo)
- **Stroke risk:** Increased risk of stroke (2-3x higher)
- **Tardive dyskinesia:** Risk with long-term use

**Non-pharmacological FIRST (before antipsychotics):**
- **Identify triggers:** Pain, hunger, thirst, constipation, infection (UTI), medications, environment (noise, overcrowding)
- **Address underlying cause:** Treat pain, infection, constipation, reduce medications
- **Environment:** Calm, quiet, familiar, adequate lighting, consistent routine
- **Communication:** Reassure, distract, validate (don't argue), don't confront

**Prognosis:**
- **Course:** Progressive (no cure, symptomatic treatment)
- **Survival:** 4-8 years (Alzheimer's), 3-5 years (vascular), 2-5 years (LBD), 8-10 years (FTD)
- **Institutionalization:** 2-3 years after diagnosis (average)
- **End-stage:** Bedbound, mute, incontinent, unable to recognize family

**Sources:** NICE NG97, NICE CG161, APA Practice Guidelines 2007**

---

**If you or someone you know is showing signs of cognitive decline, encourage them to see their GP for assessment. Early diagnosis allows for planning, access to treatments, and support.**"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "mental_health_cognitive",
                "focus": "dementia_management",
                "sources": ["NICE NG97", "NICE CG161", "APA 2007"]
            }
        )

    def _handle_delirium(self, query: str, context: dict) -> DomainQueryResult:
        """Handle delirium queries"""
        answer = """**Delirium Assessment and Management**

**Definition:**
- **Delirium (Acute Confusion):** Acute, fluctuating disturbance in attention, awareness, and cognition due to medical cause(s)
- **Medical emergency** (underlying medical illness requires urgent treatment)

**Epidemiology:**
- **Incidence:** 10-30% in hospitalized elderly (higher in ICU, postoperative)
- **Prevalence:** 10-20% in general hospital wards, 50-80% in ICU
- **Risk factors:** Age > 65, dementia, visual/hearing impairment, severe illness, multiple medications, dehydration, infection, immobility, urinary catheter, malnutrition

**Clinical Features:**

**Core Symptoms (DSM-5):**
- **Disturbance in attention** (easily distracted, difficulty focusing, lethargy or agitation)
- **Disturbance in awareness** (disorientation to time, place, person)
- **Cognitive disturbance** (memory impairment, disorientation, language disturbance, perceptual disturbances)
- **Acute onset** (hours-days, fluctuating course)
- **Not better explained** by pre-existing dementia or developing in context of severely reduced arousal (coma)

**Psychomotor Subtypes:**

**Hyperactive Delirium (25%):**
- **Agitation**, **restlessness**, **hypervigilance**
- **Hallucinations**, **delusions**
- **Aggression**, **wandering**
- **Autonomic hyperactivity:** Tachycardia, hypertension, fever, sweating, dilated pupils

**Hypoactive Delirium (50%):**
- **Lethargy**, **sedation**, **withdrawal**
- **Reduced alertness**, **slowed speech**
- **Apathy**, **reduced mobility**
- **Often missed** (attributed to depression, dementia, fatigue)

**Mixed Delirium (25%**
- **Fluctuating** between hyperactive and hypoactive

**Etiology (Multifactorial - usually 3+ causes):**

**Predisposing Factors (Vulnerability):**
- **Age** (elderly), **dementia**, **cognitive impairment**
- **Visual/hearing impairment**, **functional dependence**
- **Dehydration**, **malnutrition**, **comorbidities**

**Precipitating Factors (Triggers):**
- **Medications:** Anticholinergics, benzodiazepines, opioids, antipsychotics, steroids, antihistamines, muscle relaxants, antiemetics, anticholinesterases (withdrawal), digoxin toxicity
- **Substances:** Alcohol withdrawal, benzodiazepine withdrawal, cannabis, stimulants (cocaine, amphetamines), hallucinogens
- **Infections:** Pneumonia, UTI, sepsis, meningitis, encephalitis, HIV
- **Metabolic:** Dehydration, electrolyte disturbances (Na+, K+, Ca2+, Mg2+), acid-base disturbances, hypoglycemia, hyperglycemia, uremia, liver failure, thyroid disorders
- **Hypoxia:** Respiratory failure (pneumonia, PE, COPD), anemia, carbon monoxide poisoning
- **Cardiovascular:** Myocardial infarction, arrhythmias, stroke, TIA, shock, heart failure
- **Neurological:** Stroke, TIA, seizure (postictal), head trauma, brain tumor, subdural/epidural hematoma, meningitis, encephalitis
- **Environmental:** Immobility, pain, sleep deprivation, unfamiliar environment (hospital), sensory deprivation (hearing/vision loss, ICU)
- **Other:** Constipation, urinary retention, hypothermia, hyperthermia, postoperative states

**Differential Diagnosis:**
- **Dementia:** Chronic, progressive, slow onset (months-years), consciousness normal (until late), no fluctuation
- **Depression:** Low mood, anhedonia, "I don't know" responses (pseudodementia), neurovegetative symptoms (sleep, appetite, energy), no fluctuation
- **Psychosis:** No delirium symptoms (attention, awareness normal), hallucinations/delusions in context of normal arousal
- **Speech disorder:** Aphasia (stroke, brain tumor) but other aspects of cognition intact

**Assessment:**

**Bedside Tests:**
- **Attention:** Digit span forward/backward (normal 7 ± 2, < 5 suggests delirium), months of year backwards, serial 7s
- **Fluctuation:** Worse at night (sundowning), variability over hours-days
- **Disorientation:** Time (worst), place, person (least impaired until later)
- **Memory:** Impaired registration (forget things immediately after hearing them)
- **Instrument:** Confusion Assessment Method (CAM) - sensitivity 94%, specificity 89%
  - **Feature 1:** Acute onset + fluctuating course
  - **Feature 2:** Inattention
  - **Feature 3:** Disorganized thinking
  - **Feature 4:** Altered level of consciousness
  - **Diagnosis:** Features 1 + 2 + either 3 or 4

**Diagnostic Workup:**
- **History:** Onset, course, predisposing factors, precipitating factors, medications, substances, recent changes
- **Collateral history:** Family, caregiver (patient often unreliable historian)
- **Physical examination:** Vital signs, neurological exam, cardiovascular exam (arrhythmias, murmurs), respiratory exam, abdominal exam, skin (infection, pressure ulcers)
- **Medication review:** Recent additions, dose changes, anticholinergics (cumulative anticholinergic burden), benzodiazepines, opioids
- **Laboratory tests:**
  - **CBC** (anemia, infection)
  - **Electrolytes:** Na+, K+, Ca2+, Mg2+, glucose (hypoglycemia, hyperglycemia)
  - **Renal function:** Urea, creatinine (AKI)
  - **Liver function:** LFTs (liver failure)
  - **Thyroid:** TSH, free T4 (hypothyroidism, hyperthyroidism)
  - **Inflammatory markers:** CRP, ESR (infection)
  - **Toxicology:** Urine drug screen, alcohol level, medications (digoxin, anticonvulsants)
  - **Infection:** Blood cultures, urine culture, CXR (pneumonia), sputum culture, CSF analysis (if meningitis/encephalitis suspected)
  - **Vitamin levels:** B12, folate, thiamine (deficiency)
  - **Arterial blood gas** (hypoxia, hypercapnia, acid-base disturbances)
  - **Serum osmolality** (dehydration)
- **Imaging:** CT head (if focal signs, head trauma, fall, sudden onset, no improvement with treatment), EEG (if seizure, encephalitis)

**Management:**

**Treat Underlying Cause(s):**
- **Stop/reduce medications:** Anticholinergics, benzodiazepines, opioids, antipsychotics (if possible)
- **Treat infection:** Antibiotics for pneumonia, UTI, meningitis
- **Correct metabolic disturbances:** Fluids, electrolytes, glucose, thiamine
- **Treat pain:** Analgesics (avoid anticholinergics, opioids if possible)
- **Treat hypoxia:** Oxygen, respiratory support
- **Treat constipation/urinary retention:** Laxatives, catheter
- **Withdraw substances:** Alcohol, benzodiazepines (medically supervised taper)

**Supportive Care:**
- **Reorientation:** Calm approach, frequent reassurance, orient to person, place, time (clocks, calendars, windows)
- **Environment:** Quiet, well-lit (day/night cycle), familiar objects (photos, objects from home), reduce sensory deprivation (hearing aids, glasses)
- **Mobility:** Encourage mobility (prevent deconditioning, falls, DVT), assistance if needed, prevent falls (bed alarms, sensors)
- **Nutrition:** Adequate hydration, assistance with feeding if needed (monitor for aspiration)
- **Sleep-wake cycle:** Daytime activity, nighttime sleep (avoid daytime napping), reduce nighttime disruptions (limit care tasks, cluster care)
- **Family involvement:** Encourage family presence (calming effect, reorientation), educate family about delirium (symptoms, course, treatment)

**Pharmacological (Severe Agitation, Danger to Self/Others):**

**Antipsychotics:**
- **Indications:** Severe agitation, aggression, psychosis (hallucinations, delusions), distress, danger to self/others, non-pharmacological interventions ineffective
- **Agents:**
  - **Haloperidol:** 0.5-2 mg PO/IM/IV q4-6h PRN (high potency, high EPS risk, short-acting)
  - **Risperidone:** 0.5-2 mg PO/IM q12h PRN (lower EPS risk, longer-acting)
  - **Quetiapine:** 12.5-50 mg PO q8-12h PRN (sedating, low EPS risk, useful in Lewy body dementia)
  - **Olanzapine:** 2.5-5 mg PO q12h PRN (sedating, low EPS risk)
- **Caution:** Extrapyramidal symptoms (EPS), neuroleptic malignant syndrome (NMS), sedation, falls, stroke risk, increased mortality (black box warning)

**Benzodiazepines (Cautious):**
- **Indications:** Alcohol withdrawal, benzodiazepine withdrawal, severe anxiety, insomnia
- **Agents:**
  - **Lorazepam:** 0.5-1 mg PO/IM q4-6h PRN (short-acting, no active metabolites, safe in elderly, hepatic metabolism)
  - **Midazolam:** 2.5-5 mg IM q1-2h PRN (short-acting, IM formulation available)
- **Caution:** Sedation, respiratory depression, falls, delirium exacerbation (paradoxical agitation), dependence (short-term use only)

**Cholinesterase Inhibitors:**
- **Indications:** Delirium superimposed on dementia (Alzheimer's, Lewy body dementia)
- **Donepezil:** 5-10 mg daily (may help improve attention, alertness, reduce behavioral disturbances)

**Prevention:**
- **Identify at-risk patients** (elderly, dementia, severe illness, multiple medications)
- **Reduce risk factors:** Minimize anticholinergic medications, adequate hydration, early mobilization, pain control, sleep hygiene, sensory aids (glasses, hearing aids), orientation (familiar environment, family presence)
- **Screening:** Regular screening for delirium in at-risk patients (CAM, confusion assessment method)

**Prognosis:**
- **Mortality:** Increased hospital mortality (2-3x), increased 3-month mortality (20-30%), increased 12-month mortality (40-50%)
- **Duration:** Days to weeks (usually improves with treatment of underlying cause), some patients have persistent delirium (up to 50% at discharge)
- **Recurrence:** High (recurrent delirium 30-50%)
- **Functional decline:** Hospital-associated disability, increased risk of nursing home placement

**Sources:** NICE CG103, APA Practice Guidelines 1999, British Geriatrics Society 2019"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "mental_health_geriatric",
                "focus": "delirium_management",
                "sources": ["NICE CG103", "APA 1999", "BGS 2019"]
            }
        )

    def _handle_substance_use(self, query: str, context: dict) -> DomainQueryResult:
        """Handle substance use disorders"""
        answer = """**Substance Use Disorders Management**

**Definition:**
- **Addiction (Substance Use Disorder):** Maladaptive pattern of substance use leading to clinically significant impairment or distress, manifested by ≥ 2 of 11 criteria within 12 months (impaired control, social impairment, risky use, pharmacological criteria [tolerance, withdrawal])

**Common Substances:**

**Alcohol:**
- **Harmful use:** > 14 units/week (women), > 21 units/week (men) (1 unit = 8 g alcohol, 125 ml wine, 250 ml beer)
- **Dependence:** Tolerance (need more to get same effect), withdrawal (tremor, anxiety, seizures, delirium tremens), loss of control
- **Complications:** Liver disease (fatty liver, hepatitis, cirrhosis), pancreatitis, gastritis, anemia, thrombocytopenia, hypertension, cardiomyopathy, neuropathy, dementia, depression, suicide

**Opioids (Heroin, Prescription Opioids):**
- **Dependence:** Tolerance, withdrawal (muscle aches, anxiety, lacrimation, rhinorrhea, piloerection, yawning, diarrhea, fever), craving
- **Complications:** Overdose (respiratory depression), constipation, endocarditis, HIV, hepatitis B/C, abscesses, deep vein thrombosis, depression

**Stimulants (Cocaine, Amphetamines):**
- **Dependence:** Tolerance, withdrawal (fatigue, depression, increased appetite, hypersomnolence), craving
- **Complications:** Cardiovascular (hypertension, tachycardia, arrhythmias, MI, stroke), psychiatric (anxiety, paranoia, psychosis), seizures, weight loss

**Cannabis:**
- **Use disorder:** Problematic use (impaired functioning, continued use despite problems)
- **Dependence:** Controversial (tolerance, withdrawal mild - irritability, anxiety, insomnia, decreased appetite)
- **Complications:** Psychosis (acute paranoid psychosis), anxiety, depression, cognitive impairment, respiratory (chronic bronchitis), cardiovascular (tachycardia, hypertension)

**Benzodiazepines:**
- **Dependence:** Tolerance, withdrawal (anxiety, insomnia, tremor, seizures, delirium), loss of control
- **Complications:** Falls, confusion, delirium, respiratory depression (with alcohol, opioids), overdose

**Assessment:**

**History:**
- **Substance use:** Type, amount, frequency, duration, route of administration
- **Pattern:** Continuous, binge (heavy episodic), weekend use
- **Dependence:** Tolerance, withdrawal, loss of control, continued use despite problems
- **Consequences:** Medical, psychiatric, social, occupational, legal
- **Treatment history:** Previous quit attempts, detox, rehab, mutual aid (AA, NA)
- **Risk assessment:** Suicide, overdose (history of overdose, tolerance after period of abstinence, mixing substances), withdrawal (severity, complications)

**Physical Examination:**
- **Vital signs:** BP, HR, RR, Temp (infection withdrawal)
- **General:** Nutritional status, hygiene, injection sites (abscesses, track marks)
- **Neurological:** Tremor (alcohol withdrawal), ataxia (alcohol cerebellar degeneration), neuropathy (alcohol, opioids), pupil size (opioids - pinpoint; stimulants - dilated)
- **Psychiatric:** Mood, anxiety, psychosis, cognition, insight

**Laboratory Tests:**
- **Blood:** CBC, LFTs (alcohol), electrolytes, glucose, renal function, amylase (pancreatitis), lipase, toxicology (alcohol, opioids, stimulants, benzodiazepines)
- **Urine:** Drug screen (opioids, cocaine, amphetamines, benzodiazepines, cannabis), pregnancy test (women)
- **Infectious disease:** Hepatitis B, C, HIV (if risk factors: IVDU, unprotected sex)

**Treatment:**

**Alcohol Withdrawal:**
- **CIWA-Ar scale:** Assess severity (0-67)
- **Mild:** Outpatient detox, thiamine, multivitamin, benzodiazepines (chlordiazepoxide 50-100 mg q6h PRN, or diazepam 5-10 mg q6h PRN, taper over 5-7 days)
- **Moderate-severe:** Inpatient detox, benzodiazepines (diazepam 10-20 mg q6h PRN, taper over 7-10 days), thiamine, multivitamin
- **Complications:** Seizures (prophylaxis with benzodiazepines), delirium tremens (hallucinations, confusion, autonomic hyperactivity - treat with benzodiazepines), Wernicke's encephalopathy (thiamine 100 mg IV TDS, Korsakoff's psychosis)

**Opioid Withdrawal:**
- **COWS scale:** Assess severity (0-36)
- **Mild:** Outpatient detox, buprenorphine/naloxone (Suboxone) 4-8 mg SL daily, taper over 3-7 days
- **Moderate-severe:** Inpatient detox, methadone 20-30 mg daily, maintenance or taper, buprenorphine 8-16 mg daily, maintenance or taper
- **Complications:** Relapse (high risk of overdose due to reduced tolerance after detox), dehydration, suicide

**Stimulant Withdrawal:**
- **Self-limited:** Fatigue, depression, hypersomnolence, increased appetite, craving (resolves over 1-2 weeks)
- **Treatment:** Supportive care, monitoring for depression, suicidal ideation, relapse prevention

**Benzodiazepine Withdrawal:**
- **Severe:** Inpatient detox, gradual taper (reduce dose by 10-25% weekly) over 4-12 weeks depending on dose, duration (high-dose, long-term → slower taper)
- **Substitutes:** Diazepam 10-20 mg daily (long-acting, cross-tolerant with most benzodiazepines), chlordiazepoxide 25-50 mg QID
- **Adjunctive:** Propranolol 20-40 mg TID (autonomic symptoms), antidepressants (if depression/anxiety emerges)

**Relapse Prevention:**

**Psychosocial Interventions:**
- **Motivational interviewing:** Enhance motivation for change, resolve ambivalence
- **CBT:** Identify triggers, develop coping strategies, prevent relapse
- **Mutual aid:** Alcoholics Anonymous (AA), Narcotics Anonymous (NA), SMART Recovery
- **Residential rehabilitation:** Intensive, structured treatment (4-12 weeks) for severe dependence

**Pharmacological:**
- **Alcohol:** Acamprosate 666 mg TDS (reduce craving, maintenance), naltrexone 50 mg daily (reduce craving, reduce reinforcement if relapse), disulfiram 200-400 mg daily (aversion therapy - deterrent if alcohol consumed)
- **Opioids:** Methadone 40-100 mg daily (maintenance, stabilization), buprenorphine 8-24 mg daily (maintenance, stabilization), naltrexone 50 mg daily (abstinence-focused, reduce craving)
- **Nicotine:** Varenicline 1 mg BID (titrated), nicotine replacement therapy (patch, gum, lozenge), bupropion 150 mg SR daily (Zyban)

**Harm Reduction:**
- **Needle exchange:** Clean syringes, needles (reduce HIV, hepatitis C)
- **Supervised injection sites:** Overdose prevention, safer use, linkage to treatment
- **Naloxone distribution:** Take-home naloxone kits (overdose reversal - administer to unconscious person with respiratory depression)
- **Opioid substitution therapy:** Methadone, buprenorphine (maintenance, reduce mortality, morbidity)

**Prognosis:**
- **Recovery:** 30-40% achieve abstinence at 1 year (lower for some substances)
- **Course:** Chronic, relapsing, remitting (multiple treatment episodes often needed)
- **Predictors of good outcome:** Stable living situation, supportive family, employment, motivation, treatment adherence, mutual aid involvement
- **Predictors of poor outcome:** Poly-substance use, psychiatric comorbidity (depression, anxiety, psychosis), social instability, criminal justice involvement, lack of motivation

**Sources:** NICE CG115, APA Practice Guidelines 2006, NIDA 2020"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "mental_health_addiction",
                "focus": "substance_use_disorders",
                "sources": ["NICE CG115", "APA 2006", "NIDA 2020"]
            }
        )

    def _handle_eating_disorder(self, query: str, context: dict) -> DomainQueryResult:
        """Handle eating disorder queries"""
        answer = """**Eating Disorders Management**

**⚠️ CRITICAL: Eating disorders are serious mental health conditions with significant medical complications. If you or someone you know is affected, seek professional help immediately.**

---

**Emergency Resources:**

**UK:**
- **Eating disorders helpline:** Beat Eating Disorders: 0808 801 0677 (adult helpline)
- **Emergency:** 999 or 112 (if medical emergency - cardiac arrhythmia, electrolyte disturbances)

**US:**
- **National Eating Disorders Association (NEDA):** 800-931-2237
- **Emergency:** 911 (if medical emergency)

**Australia:**
- **Butterfly Foundation:** 1800 33 4677
- **Emergency:** 000 (if medical emergency)

---

**Anorexia Nervosa:**

**Diagnostic Criteria (DSM-5):**
- **Restriction of energy intake** (relative to requirements), leading to **low body weight**
- **Intense fear** of gaining weight or becoming fat, **persistent behavior** that interferes with weight gain
- **Disturbance** in self-perceived weight or shape, **denial** of seriousness of low body weight

**Subtypes:**
- **Restricting type:** Weight loss through dieting, fasting, excessive exercise
- **Binge-eating/purging type:** Regular binge-eating or purging (self-induced vomiting, laxatives, diuretics, enemas)

**Clinical Features:**
- **Low BMI:** < 18.5 kg/m² (adults), < 5th percentile (children)
- **Medical complications:** Bradycardia, hypotension, hypothermia, leukopenia, anemia, electrolyte disturbances (hypokalemia, hypomagnesemia, hypocalcemia), elevated liver enzymes, amenorrhea, osteoporosis
- **Psychiatric features:** Perfectionism, obsessive traits, anxiety, depression, OCD traits, body image disturbance

**Bulimia Nervosa:**

**Diagnostic Criteria (DSM-5):**
- **Recurrent episodes** of binge-eating (eating large amounts in discrete period, sense of lack of control)
- **Inappropriate compensatory behaviors** to prevent weight gain (vomiting, laxatives, diuretics, fasting, excessive exercise)
- **Self-evaluation** unduly influenced by body shape/weight
- **Frequency:** Once weekly for 3 months (average)

**Clinical Features:**
- **Normal weight** (often overweight or obese)
- **Medical complications:** Dental erosion (enamel loss from vomiting), parotid enlargement, esophagitis (Mallory-Weiss tears, esophageal rupture), electrolyte disturbances (hypokalemia from vomiting), constipation (laxative abuse), calluses on knuckles (Russell's sign - self-induced vomiting)
- **Psychiatric features:** Low self-esteem, depression, anxiety, impulsivity, substance use

**Binge-Eating Disorder:**

**Diagnostic Criteria (DSM-5):**
- **Recurrent episodes** of binge-eating (eating large amounts in discrete period, sense of lack of control)
- **Binge episodes** associated with 3+ of: eating rapidly, eating until uncomfortably full, eating large amounts when not hungry, eating alone due to embarrassment, feeling disgusted, depressed, guilty afterward
- **Distress** regarding binge-eating
- **Frequency:** Once weekly for 3 months (average)
- **NO compensatory behaviors** (distinguishes from bulimia nervosa)

**Clinical Features:**
- **Overweight** or **obese** (BMI 25-30+)
- **Medical complications:** Obesity-related (hypertension, hyperlipidemia, type 2 diabetes, sleep apnea, osteoarthritis)
- **Psychiatric features:** Depression, low self-esteem, disgust, shame, body image disturbance

**Assessment:**

**Medical Assessment:**
- **Weight/BMI:** Current weight, height, BMI, % expected body weight
- **Vital signs:** Orthostatic BP/HR, temperature (hypothermia if < 35°C)
- **Electrolytes:** Na+, K+, Ca2+, Mg2+, PO4 (hypokalemia from vomiting, malnutrition)
- **CBC:** Anemia, leukopenia (infection risk)
- **Renal/Liver function:** Elevated LFTs, renal impairment
- **Glucose:** Hypoglycemia (malnutrition), hyperglycemia (binge-eating disorder)
- **ECG:** Bradycardia, QT prolongation (electrolyte disturbances, refeeding syndrome risk)

**Psychiatric Assessment:**
- **Eating disorder examination:** Weight/shape concerns, dietary restriction, binge-eating, compensatory behaviors
- **Screening tools:** EDE-Q (Eating Disorder Examination Questionnaire), SCOFF (Sick, Control, One stone, Fat, Food)
- **Comorbidity:** Depression, anxiety, OCD, substance use, personality disorders

**Treatment:**

**Anorexia Nervosa:**

**Medical Stabilization:**
- **Inpatient:** If BMI < 15, rapid weight loss, electrolyte disturbances, cardiac arrhythmias, hypothermia, orthostatic symptoms
- **Goals:** Weight restoration (target BMI 20-22), normalize eating behaviors, treat medical complications, address psychiatric comorbidity

**Nutritional Rehabilitation:**
- **Refeeding:** Start low, advance gradually (avoid refeeding syndrome - hypophosphatemia, hypokalemia, thiamine deficiency, cardiac failure)
- **Meal support:** Regular meals and snacks (3 meals, 3 snacks daily), monitored meals, supervision
- **Weight gain:** 0.5-1 kg/week (inpatient), 0.5 kg/week (outpatient)

**Psychotherapy:**
- **CBT-E:** Enhanced CBT for eating disorders (focus on weight/shape concerns, dietary restriction, binge-eating)
- **FBT (Family-Based Treatment):** First-line for adolescents (parents empowered to manage refeeding, restore weight)
- **MANTRA:** Maudsley Model of Anorexia Nervosa Treatment for Adults (focus on identity, thinking styles, emotional regulation)
- **SSCM:** Specialist Supportive Clinical Management (support, education, monitoring)

**Pharmacotherapy:**
- **No FDA/EMA-approved medications** for anorexia nervosa
- **SSRIs:** For comorbid depression, anxiety, OCD (fluoxetine, sertraline, paroxetine)

**Bulimia Nervosa:**

**Psychotherapy:**
- **CBT-E:** First-line (20 sessions)
- **Components:**
  - **Self-monitoring:** Food diary (food eaten, thoughts/feelings, binge/purge episodes)
  - **Regular eating:** 3 meals, 3 snacks daily (reduce hunger, prevent binge-eating)
  - **Problem-solving:** Identify triggers for binge-eating, develop alternative coping
  - **Cognitive restructuring:** Challenge negative thoughts about weight/shape, strict dieting
  - **Relapse prevention:** Identify high-risk situations, develop strategies

**Pharmacotherapy:**
- **SSRIs:** First-line (fluoxetine 60 mg daily - FDA-approved for bulimia nervosa)
  - **Efficacy:** Reduces binge-eating and purging episodes by 50-70%
  - **Onset:** 4-6 weeks (improvement in mood first, then binge/purge reduction)
  - **Duration:** 6-12 months (continue if responding)

**Binge-Eating Disorder:**

**Psychotherapy:**
- **CBT:** First-line (focus on binge-eating triggers, alternative coping, regular eating)
- **IPT (Interpersonal Psychotherapy):** Focus on interpersonal issues (role disputes, role transitions, interpersonal deficits, grief)
- **DBT (Dialectical Behavior Therapy):** Focus on emotion regulation, distress tolerance

**Pharmacotherapy:**
- **SSRIs:** First-line (fluoxetine, sertraline, paroxetine, escitalopram)
  - **Efficacy:** Reduces binge-eating episodes by 50-70%
  - **Onset:** 4-6 weeks
  - **Duration:** 6-12 months
- **Topiramate:** 25-200 mg daily (reduces binge-eating, promotes weight loss, side effects: cognitive slowing, paresthesias, visual field changes, glaucoma)
- **Liraglutide:** 1.2-3 mg daily (GLP-1 agonist, FDA-approved for binge-eating disorder, reduces binge-eating, promotes weight loss, side effects: nausea, vomiting, diarrhea)

**Medical Monitoring:**
- **Anorexia nervosa:** Weekly weight checks, electrolytes (weekly until weight restored), ECG (if bradycardia, QT prolongation), bone density (DEXA - osteoporosis)
- **Bulimia nervosa:** Dental reviews, electrolytes (if purging), ECG (if electrolyte disturbances)
- **Binge-eating disorder:** Weight, BMI, blood pressure, lipids, glucose (monitor obesity-related complications)

**Prognosis:**
- **Anorexia nervosa:** Mortality 5-10% per decade (highest of all psychiatric disorders), recovery 30-50% (partial or full), chronic course (20-30%)
- **Bulimia nervosa:** Recovery 50-70% (partial or full), chronic course (20-30%), better prognosis than anorexia nervosa
- **Binge-eating disorder:** Chronic course (weight cycling), significant medical complications (obesity-related)

**Sources:** NICE NG69, Maudsley 2022, APA Practice Guidelines 2006"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "mental_health_eating",
                "focus": "eating_disorders",
                "sources": ["NICE NG69", "Maudsley 2022", "APA 2006"]
            }
        )

    def _handle_personality_disorder(self, query: str, context: dict) -> DomainQueryResult:
        """Handle personality disorder queries"""
        answer = """**Personality Disorders Overview**

**Definition:**
- **Enduring pattern** of inner experience and behavior that deviates markedly from cultural expectations
- **Manifests:** Cognition, affectivity, interpersonal functioning, impulse control
- **Pervasive** and **inflexible**
- **Onset:** Adolescence or early adulthood
- **Stable** over time (leads to distress or impairment)

**Cluster A (Odd/Eccentric):**

**Schizotypal PD:**
- **Features:** Social anxiety, magical thinking, odd beliefs, perceptual distortions, eccentric behavior
- **Epidemiology:** 3%
- **Treatment:** Low-dose antipsychotics (if perceptual distortions severe), CBT (challenge unusual beliefs, social skills training)

**Schizoid PD:**
- **Features:** Detached from social relationships, restricted emotional expression, solitary activities, indifference to praise/criticism
- **Epidemiology:** 3%
- **Treatment:** CBT (address social withdrawal, improve social skills, increase social engagement)

**Paranoid PD:**
- **Features:** Distrust/suspicious of others, preoccupation with doubts about loyalty, reluctance to confide, reads hidden meanings, bears grudges
- **Epidemiology:** 2-4%
- **Treatment:** CBT (challenge suspicious beliefs, develop trust), long-term psychotherapy (slowly develop therapeutic alliance)

**Cluster B (Dramatic/Erratic):**

**Antisocial PD:**
- **Features:** Disregard for/rights of others, deceitfulness, impulsivity, irritability/aggressiveness, reckless disregard for safety, irresponsibility, lack of remorse
- **Epidemiology:** 3% (men > women)
- **Treatment:** Difficult (lack of motivation, high dropout), CBT/DBT (impulse control, anger management, empathy training), contingency management (reinforce prosocial behavior)

**Borderline PD (BPD):**
- **Features:** Frantic efforts to avoid abandonment, unstable interpersonal relationships, identity disturbance, impulsivity (spending, sex, substance use, reckless driving, binge-eating), emotional instability, chronic emptiness, intense anger, stress-related paranoia, transient psychosis
- **Epidemiology:** 1-3% (women > men)
- **Risk:** Self-harm, suicide (10% lifetime)
- **Treatment:**
  - **DBT (Dialectical Behavior Therapy):** First-line (skills training: mindfulness, distress tolerance, emotion regulation, interpersonal effectiveness), individual therapy, group skills training, phone coaching
  - **Schema Therapy:** Early maladaptive schemas (mistrust/abuse, abandonment, defectiveness, failure), limited reparenting
  - **Mentalization-Based Therapy (MBT):** Improve understanding of mental states (self and others), reduce attachment trauma
  - **Transference-Focused Psychotherapy (TFP):** Explore transference, understand internalized object relations, integrate split-off parts of self
  - **Medications:** SSRIs (depression, anxiety), low-dose antipsychotics (transient psychosis, dissociation, severe anger), mood stabilizers (impulsivity, mood swings)

**Histrionic PD:**
- **Features:** Discomfort in situations not center of attention, interaction with others characterized by inappropriate sexually seductive/provocative behavior, rapidly shifting/shallow expression of emotions, use of physical appearance to draw attention, self-dramatization, suggestibility
- **Epidemiology:** 2-3% (women > men)
- **Treatment:** CBT (focus on core beliefs: "I must be the center of attention," "I'm helpless without attention"), psychodynamic therapy (unconscious conflicts about dependency)

**Narcissistic PD:**
- **Features:** Grandiosity (fantasy or actual), need for admiration, lack of empathy, envy, arrogance, entitlement, exploitativeness
- **Epidemiology:** 1-6% (men > women)
- **Treatment:** Difficult (rare seek treatment, lack of insight), CBT (challenge grandiosity, develop empathy), psychodynamic therapy (unconscious conflicts about self-esteem, shame), schema therapy (early maladaptive schemas: defectiveness, entitlement, grandiosity)

**Cluster C (Anxious/Fearful):**

**Avoidant PD:**
- **Features:** Avoids occupational activities involving interpersonal contact, unwilling to get involved with people unless certain of being liked, restraint in intimate relationships, preoccupation with criticism/rejection, feelings of inadequacy, inhibited in new interpersonal situations
- **Epidemiology:** 1-2%
- **Treatment:** CBT (gradual exposure to social situations, challenge negative beliefs about self, social skills training), group therapy (reduce social isolation)

**Dependent PD:**
- **Features:** Difficulty making everyday decisions without excessive advice/reassurance from others, needs others to assume responsibility for major areas of life, difficulty expressing disagreement, difficulty initiating projects (lacks confidence), goes to excessive lengths to obtain support/nurturance, feels uncomfortable/helpless when alone
- **Epidemiology:** 1-2%
- **Treatment:** CBT (develop autonomy, challenge dependency beliefs, assertiveness training), psychodynamic therapy (unconscious conflicts about autonomy, separation)

**Obsessive-Compulsive PD (OCPD):**
- **Features:** Preoccupation with orderliness, perfectionism, mental/interpersonal control (at expense of flexibility, openness, efficiency), rigidity, stubbornness, miserliness, hoarding
- **Epidemiology:** 2-8% (men > women)
- **Treatment:** CBT (challenge perfectionism, rigidity, need for control, increase flexibility, leisure activities), psychodynamic therapy (unconscious conflicts about anger, control, autonomy)

**Assessment:**

**Differential Diagnosis:**
- **Personality change** due to another medical condition (stroke, brain injury, dementia)
- **Substance use:** Chronic substance use can mimic personality disorder (impulsivity, disinhibition, mood instability)
- **Mood disorders:** Depression, bipolar disorder (can cause personality changes)
- **Anxiety disorders:** Social anxiety, GAD (can cause avoidance, dependency)
- **Psychosis:** Schizophrenia (can mimic schizotypal, paranoid PD)

**Diagnosis:**
- **Longitudinal assessment:** Personality disorders are stable over time, whereas episodic disorders (depression, anxiety, psychosis) are episodic
- **Collateral history:** Family, partners (patient often lacks insight)
- **Onset:** Adolescence or early adulthood (before age 18 for PD traits)

**Treatment Principles:**

**Psychotherapy (First-line):**
- **CBT:** Challenge maladaptive thoughts/behaviors, develop coping skills, improve interpersonal relationships
- **DBT:** Cluster B disorders (especially BPD) - focus on emotion regulation, distress tolerance, interpersonal effectiveness, mindfulness
- **Psychodynamic therapy:** Explore unconscious conflicts, transference, attachment trauma (especially Cluster A, Cluster B disorders)
- **Schema therapy:** Early maladaptive schemas, limited reparenting, experiential techniques (especially Cluster B, Cluster C disorders)
- **Mentalization-Based Therapy (MBT):** Improve understanding of mental states (self and others), reduce attachment trauma (especially BPD)

**Pharmacotherapy (Adjunctive):**
- **Antidepressants:** SSRIs (depression, anxiety - common comorbidities)
- **Antipsychotics:** Low-dose (schizotypal PD - perceptual distortions, BPD - transient psychosis, severe anger)
- **Mood stabilizers:** BPD (impulsivity, mood swings), Cluster B disorders (impulsivity, anger)
- **Avoid:** Benzodiazepines (dependence risk, disinhibition, especially Cluster B disorders)

**Prognosis:**
- **Course:** Chronic, stable over time (improvement slowly with age)
- **Functional impairment:** Significant (relationships, occupation)
- **Comorbidity:** Depression, anxiety, substance use (high rates)
- **Response to treatment:** Variable (Cluster A: poor; Cluster B: moderate, BPD: good with DBT; Cluster C: moderate with CBT)

**Sources:** NICE CG136, NICE CG150, ICD-11, DSM-5-TR"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "mental_health_personality",
                "focus": "personality_disorders",
                "sources": ["NICE CG136", "NICE CG150", "ICD-11", "DSM-5-TR"]
            }
        )

    def _handle_psychopharmacology(self, query: str, context: dict) -> DomainQueryResult:
        """Handle psychopharmacology queries"""
        answer = """**Psychopharmacology Overview**

**Antidepressants:**

**SSRIs (First-line):**
- **Mechanism:** Block serotonin reuptake (increase serotonin in synaptic cleft)
- **First-line:** Depression, anxiety disorders, OCD, PTSD, bulimia nervosa, binge-eating disorder, premenstrual dysphoric disorder
- **Agents:**
  - **Fluoxetine (Prozac):** 20-80 mg daily (long half-life, activating, less discontinuation syndrome)
  - **Sertraline (Zoloft):** 50-200 mg daily (first-line for anxiety disorders, good for depression, anxiety, OCD, PTSD, PMDD)
  - **Paroxetine (Paxil):** 20-40 mg daily (most anticholinergic, hardest to stop - discontinuation syndrome, activating)
  - **Citalopram (Celexa):** 20-40 mg daily (least drug interactions, good for elderly, medically ill)
  - **Escitalopram (Lexapro):** 10-20 mg daily (most selective SSRI, first-line for depression, anxiety)
  - **Fluvoxamine (Luvox):** 100-300 mg daily (good for OCD, many drug interactions)
- **Side effects:** Nausea, diarrhea, headache, insomnia/somnolence, sexual dysfunction (delayed orgasm, anorgasmia, reduced libido), weight gain, agitation, anxiety
- **Onset:** 2-4 weeks (anxiety improves first, then sleep, energy, mood last)
- **Duration:** 6-9 months after remission (first episode), 2+ years (recurrent)
- **Taper:** Gradual (2-4 weeks) to avoid discontinuation syndrome (dizziness, nausea, "electric shock" sensation)

**SNRIs (Second-line):**
- **Mechanism:** Block serotonin and norepinephrine reuptake
- **Indications:** Depression (especially with fatigue, low energy), anxiety disorders, neuropathic pain, fibromyalgia
- **Agents:**
  - **Venlafaxine XR (Effexor):** 75-225 mg daily (dose-dependent: SNRI at 75 mg, more SRI at 150+ mg)
  - **Duloxetine (Cymbalta):** 30-60 mg daily (good for pain, diabetic neuropathy, fibromyalgia)
- **Side effects:** Hypertension, sweating (venlafaxine), nausea, insomnia, sexual dysfunction, liver failure (duloxetine - rare)

**Other Antidepressants:**
- **Mirtazapine (Remeron):** 15-45 mg at night (sedating, good for insomnia, low appetite, no sexual dysfunction, weight gain, dry mouth, constipation)
- **Bupropion (Wellbutrin):** 150-300 mg daily (activating, good for low energy, fatigue, hypersomnia, no sexual dysfunction, weight loss, contraindicated in seizure disorder, eating disorders, head trauma, brain tumor)
- **TCAs (Tricyclics):** Amitriptyline (25-150 mg at night - good for neuropathic pain, migraine prophylaxis, insomnia), nortriptyline (25-150 mg at night - better tolerated), clomipramine (25-250 mg daily - OCD)
- **MAOIs (Monoamine Oxidase Inhibitors):** Phenelzine (30-90 mg daily - good for atypical depression, treatment-resistant depression, contraindicated with tyramine-rich foods, SSRIs/SNRIs, sympathomimetics, meperidine, dextromethorphan)

**Antipsychotics:**

**First-generation (Typical):**
- **Mechanism:** Dopamine D2 receptor antagonists
- **High-potency:** Haloperidol (2-10 mg daily), fluphenazine (2-20 mg daily), pimozide (2-10 mg daily - Tourette's)
- **Low-potency:** Chlorpromazine (25-200 mg daily - sedating, antihistaminic, anticholinergic), thioridazine (50-400 mg daily - less EPS, more cardiac toxicity)
- **Side effects:** EPS (extrapyramidal symptoms) - acute dystonia (spasms, torticollis, trismus), akathisia (restlessness), parkinsonism (bradykinesia, rigidity, tremor), tardive dyskinesia (late-onset, involuntary movements - choreoathetoid movements, buccolingual movements, trunk movements), NMS (neuroleptic malignant syndrome - hyperthermia, rigidity, autonomic instability, delirium, elevated CK), hyperprolactinemia (galactorrhea, amenorrhea, sexual dysfunction, osteoporosis), anticholinergic effects (dry mouth, constipation, blurred vision, urinary retention, sedation, confusion), weight gain, metabolic syndrome, QT prolongation, cardiac toxicity (thioridazine - arrhythmias)

**Second-generation (Atypical):**
- **Mechanism:** Dopamine D2 antagonism + serotonin 5-HT2A antagonism (various mechanisms)
- **Agents:**
  - **Risperidone (Risperdal):** 2-6 mg daily (first-line, less EPS than typicals, some metabolic side effects, dose-dependent hyperprolactinemia)
  - **Olanzapine (Zyprexa):** 10-20 mg daily (first-line for psychosis, mania, very effective, but significant metabolic side effects - weight gain, diabetes, dyslipidemia)
  - **Quetiapine (Seroquel):** 150-750 mg daily (sedating, low EPS, used in depression, anxiety, insomnia, metabolic side effects)
  - **Ziprasidone (Geodon):** 40-160 mg daily (less weight gain, QT prolongation)
  - **Aripiprazole (Abilify):** 10-30 mg daily (partial agonist - stabilizes dopamine, less EPS, metabolic side effects, akathisia common)
  - **Brexpiprazole (Rexulti):** 1-4 mg daily (partial agonist, similar to aripiprazole, approved as adjunct to antidepressants)
  - **Cariprazine (Vraylar):** 1.5-6 mg daily (partial agonist, approved for schizophrenia, bipolar mania)
  - **Clozapine (Clozaril):** 100-600 mg daily (treatment-resistant schizophrenia - 30-60% response, severe side effects - agranulocytosis [1%], myocarditis, seizures, weight gain, diabetes, hypersalivation, drooling, sedation, requires weekly-biweekly CBC monitoring)

**Mood Stabilizers:**

**Lithium:**
- **Indications:** Bipolar disorder (mania, depression prophylaxis), suicide prevention, adjunctive in depression (refractory, suicidal), aggression
- **Dose:** 600-1200 mg daily (serum level 0.6-1.2 mmol/L)
- **Onset:** 1-2 weeks (mania), 4-6 weeks (depression prophylaxis)
- **Side effects:** Tremor, nausea, diarrhea, polyuria, polydipsia, weight gain, hypothyroidism (treat with levothyroxine), renal toxicity (monitor creatinine), cardiac toxicity (arrhythmias - avoid in significant renal/cardiac disease), teratogenic (avoid in pregnancy, especially first trimester - Ebstein's anomaly)
- **Monitoring:** Serum levels (5-7 days after starting/changing dose, then every 3 months), TFTs, U&Es, calcium, ECG (if > 50, cardiac risk factors), pregnancy test (women of childbearing age)
- **Toxicity:** Acute (tremor, nausea, vomiting, diarrhea, ataxia, drowsiness, confusion), chronic (renal, thyroid, cardiac), overdose (tremor, nausea, vomiting, diarrhea, ataxia, seizures, coma, death)

**Valproate (Sodium Valproate):**
- **Indications:** Bipolar disorder (mania, depression prophylaxis), migraine prophylaxis, epilepsy
- **Dose:** 750-2000 mg daily (serum level 50-125 µg/mL)
- **Side effects:** Weight gain, tremor, hair loss, teratogenic (neural tube defects - avoid in pregnancy), hepatotoxicity, thrombocytopenia, polycystic ovaries
- **Monitoring:** LFTs, serum levels (every 3-6 months), CBC (thrombocytopenia), pregnancy test (women of childbearing age)

**Lamotrigine:**
- **Indications:** Bipolar depression (prevents depression more than mania), epilepsy
- **Dose:** 100-200 mg daily
- **Side effects:** Stevens-Johnson syndrome (10% risk - slow titration over 6-8 weeks), rash (distinguish from serious rash), dizziness, headache, nausea, insomnia
- **Monitoring:** CBC, LFTs (rare hepatotoxicity), slow titration (reduce SJS risk)

**Anxiolytics:**

**Benzodiazepines:**
- **Mechanism:** GABA-A receptor allosteric modulators (enhance GABAergic inhibition)
- **Indications:** Anxiety (short-term), insomnia (short-term), alcohol withdrawal, agitation, psychosis, muscle relaxation
- **Agents:**
  - **Diazepam (Valium):** 5-10 mg TDS-QDS (long half-life, good for alcohol withdrawal, anxiety)
  - **Lorazepam (Ativan):** 1-2 mg TDS-QDS (short half-life, no active metabolites, safe in elderly, hepatic metabolism, good for agitation)
  - **Clonazepam (Klonopin):** 0.5-2 mg daily (long half-life, good for panic disorder, tics)
  - **Alprazolam (Xanax):** 0.25-1 mg TDS-QDS (short-acting, rapid onset, high abuse potential, interdose anxiety, avoid if possible)
  - **Temazepam (Restoril):** 10-20 mg at night (short half-life, hypnotic, good for insomnia)
  - **Zolpidem (Ambien):** 5-10 mg at night (z-drug, GABA-A receptor agonist, hypnotic)
  - **Zopiclone (Imovane):** 7.5 mg at night (z-drug, non-benzodiazepine hypnotic)
- **Side effects:** Sedation, confusion, ataxia, falls (elderly), respiratory depression (especially with alcohol, opioids), anterograde amnesia, dependence, tolerance, withdrawal (anxiety, insomnia, tremors, seizures)
- **Contraindications:** Severe respiratory failure, severe sleep apnea, severe liver failure, pregnancy (especially first trimester), substance use disorder
- **Duration:** Short-term (2-4 weeks maximum) - risk of dependence, tolerance, withdrawal

**Non-benzodiazepine Anxiolytics:**
- **Buspirone:** 15-30 mg BID-TDS (buspirone - 5-HT1A partial agonist, non-sedating, no dependence, slow onset 2-4 weeks, used for GAD)
- **Hydroxyzine:** 25-50 mg TDS-QDS (antihistamine, sedating, short-term anxiety)
- **Pregabalin:** 150-600 mg daily (gabapentinoid, used for GAD, neuropathic pain, off-label for anxiety)

**Hypnotics:**

**Z-drugs:**
- **Zolpidem (Ambien):** 5-10 mg at night (short-acting, 6-8 hours duration)
- **Zopiclone (Imovane):** 7.5 mg at night (short-acting, 6-8 hours duration)
- **Eszopiclone (Lunesta):** 2-3 mg at night (long-acting z-drug, 8 hours duration)
- **Side effects:** Taste disturbance (metallic taste), amnesia, complex sleep behaviors (sleepwalking, sleep-eating, sleep-driving), dependence (tolerance, withdrawal)
- **Duration:** Short-term (2-4 weeks maximum) - risk of tolerance, dependence

**Melatonin Receptor Agonists:**
- **Ramelteon:** 8 mg at night (melatonin MT1/MT2 agonist, used for insomnia)
- **Suvorexant (Belsomra):** 10-20 mg at night (dual orexin receptor antagonist, used for insomnia)

**Sources:** BNF 2024, Maudsley Prescribing Guidelines 2024, Stahl's Essential Psychopharmacology 7th Edition"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "mental_health_psychopharmacology",
                "focus": "psychopharmacology_overview",
                "sources": ["BNF 2024", "Maudsley 2024", "Stahl 2021"]
            }
        )

    def _handle_capacity(self, query: str, context: dict) -> DomainQueryResult:
        """Handle mental capacity assessment"""
        answer = """**Mental Capacity Assessment**

**Definition:**
- **Capacity:** Ability to make a specific decision (understand, retain, use/weigh information, communicate decision) at a specific time
- **Competence:** Legal term (capacity assessed in court, but generally synonymous)

**Four Test of Capacity (UK Mental Capacity Act 2005):**

**1. Understanding:**
- **Does the person understand** the information relevant to the decision?
- **Example:** "Can you explain in your own words what this treatment involves, what the benefits and risks are?"

**2. Retention:**
- **Can the person retain** the information long enough to make the decision?
- **Example:** "I just explained the treatment options. Can you tell me what I said?"

**3. Use/Weighing:**
- **Can the person use/weigh** the information to arrive at a decision?
- **Example:** "What are your thoughts about this treatment? What factors are important to you?"

**4. Communication:**
- **Can the person communicate** their decision (by speech, gesture, or other means)?
- **Example:** "Can you let me know your decision?"

**Presumption of Capacity:**
- **Adults (≥ 18) are presumed to have capacity** unless proven otherwise
- **Specific decision:** Capacity is decision-specific (can have capacity for medical treatment but not financial decisions, or vice versa)
- **Time-specific:** Capacity can fluctuate (delirium, psychosis, intoxication, pain, fatigue)
- **Maximizing capacity:** Support communication, provide information in accessible format, optimize environment (reduce distractions, ensure glasses/hearing aids), time of day (patient most alert)

**Specific Decisions:**

**Consent to Medical Treatment:**
- **Information needed:** Nature, purpose, benefits, risks, alternatives, consequences of not having treatment
- **Example:** "You have atrial fibrillation. Warfarin reduces stroke risk by 60% but increases bleeding risk. The alternatives are aspirin (less effective) or no treatment (high stroke risk). What do you want to do?"

**Refusal of Life-Sustaining Treatment:**
- **Adults (≥ 18) with capacity have right** to refuse treatment (even if refusal results in death)
- **Challenge:** If clinician believes patient lacks capacity (depression, psychosis, delirium, cognitive impairment)
- **Second opinion:** Obtain second opinion from another clinician
- **Court:** If disagreement persists, court can make declaration of capacity (Court of Protection)

**Placement Decisions:**
- **Living at home vs care home:** Assess risk (falls, wandering, self-neglect, vulnerability to exploitation, safety)
- **Care home:** If lacks capacity to decide, "best interests" decision (family, caregivers, independent advocate)

**Financial Decisions:**
- **Property, finances, wills, gifts:** Assess capacity (understand consequences, appreciate value, recognize exploitation)
- **Power of attorney:** Lasting power of attorney (LPA) can make decisions if person lacks capacity (if registered)

**Advance Decisions:**
- **Advance decision to refuse treatment (Living Will):** Person can refuse specific treatments in advance (life-sustaining treatment) if has capacity when made decision
- **Advance statement:** Preferences, wishes, values (not legally binding but must be considered)
- **Lasting power of attorney (LPA):** Property and affairs (financial decisions), health and welfare (medical treatment, care)

**Fluctuating Capacity:**
- **Delirium:** Capacity fluctuates (worse at night, with infection, medications, metabolic disturbances) - reassess frequently
- **Psychosis:** May lack capacity during acute episode (paranoid delusions, command hallucinations) but regain capacity when remitted
- **Depression:** May affect capacity (hopelessness, guilt, worthlessness) but usually retains capacity unless severe with psychotic features
- **Dementia:** May lack capacity for complex decisions (medical treatment, finances, living arrangements) as disease progresses

**Assessment Process:**

**1. Identify the decision:** What decision is being made? (medical treatment, placement, finances, will)
**2. Identify the relevant information:** What information is necessary for this decision?
**3. Provide information:** In accessible format (simple language, written, diagrams, repetition, time to process)
**4. Assess understanding:** Ask person to explain in their own words (understanding)
**5. Assess retention:** Ask person to repeat information (retention)
**6. Assess use/weighing:** Ask person to discuss thoughts, preferences, values, decision-making process
**7. Assess communication:** Can person communicate decision clearly? (speech, gesture, communication aid)
**8. Document:** Clearly document capacity assessment (four test results, decision, rationale)

**Outcome:**

**Capacity Present:**
- **Respect autonomy:** Person makes their own decision (even if clinician disagrees, if decision is unwise)
- **Offer alternatives:** Suggest alternatives, discuss consequences, provide information, but respect autonomy

**Capacity Absent:**
- **Best interests decision:** Make decision in person's best interests (consider past wishes, values, views of family/friends/carers, advance decisions)
- **Least restrictive option:** Choose least restrictive option consistent with safety (e.g., care home vs home with care package vs home with 24-hour caregiver)
- **Involve others:** Family, friends, caregivers, Independent Mental Capacity Advocate (IMCA) if no family/friends available
- **Document:** Clearly document lack of capacity, best interests decision, reasoning

**Sources:** Mental Capacity Act 2005, NICE NG108, GMC Guidance 2022"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "mental_health_legal",
                "focus": "mental_capacity_assessment",
                "sources": ["MCA 2005", "NICE NG108", "GMC 2022"]
            }
        )

    def _handle_general_mental_health(self, query: str, context: dict) -> DomainQueryResult:
        """General mental health information"""
        answer = """**Mental Health Overview**

**Common Mental Disorders:**

**Mood Disorders:**
- **Depression:** Low mood, anhedonia, fatigue, sleep/appetite changes, guilt, worthlessness, suicidal thoughts
- **Bipolar disorder:** Mania (elevated mood, grandiosity, decreased need for sleep, racing thoughts) and depression

**Anxiety Disorders:**
- **GAD:** Excessive worry, restlessness, fatigue, concentration, muscle tension, sleep disturbance
- **Panic disorder:** Recurrent panic attacks (palpitations, sweating, shortness of breath, fear of dying)
- **Social anxiety:** Fear of social scrutiny, embarrassment, humiliation
- **Specific phobias:** Fear of specific objects/situations (heights, spiders, flying, needles)

**Psychotic Disorders:**
- **Schizophrenia:** Hallucinations, delusions, disorganized thinking, negative symptoms
- **Delusional disorder:** Fixed, false beliefs (non-bizarre), no other psychotic symptoms

**Trauma-Related:**
- **PTSD:** Intrusion (flashbacks, nightmares), avoidance, hyperarousal (increased startle, hypervigilance), negative alterations in mood/cognition

**Obsessive-Compulsive:**
- **OCD:** Obsessions (unwanted intrusive thoughts), compulsions (repetitive behaviors to reduce anxiety)

**Treatment:**
- **Psychotherapy:** CBT, IPT, DBT, EMDR (for trauma), family therapy
- **Medication:** Antidepressants, antipsychotics, mood stabilizers, anxiolytics
- **Combined:** Psychotherapy + medication (most effective for moderate-severe disorders)

**When to Seek Help:**
- **Persistent symptoms** (> 2 weeks)
- **Functional impairment** (work, relationships, self-care)
- **Suicidal thoughts**
- **Psychotic symptoms** (hallucinations, delusions)
- **Substance use** as coping mechanism

**Sources:** NICE guidelines, Royal College of Psychiatrists, APA"""

        return DomainQueryResult(
            domain_name="mental_health",
            answer=answer,
            confidence=0.84,
            metadata={
                "specialty": "mental_health",
                "focus": "general_information",
                "sources": ["NICE", "RCPsych", "APA"]
            }
        )

def create_mental_health_domain():
    """Factory function to create mental health domain instance"""
    return MentalHealthDomain()
