"""
Psychiatry Domain for GPDISC

Comprehensive mental health care covering:
- Depressive disorders (MDD, dysthymia, bipolar disorder)
- Anxiety disorders (GAD, panic disorder, phobias, OCD, PTSD)
- Psychotic disorders (schizophrenia, schizoaffective disorder)
- Substance use disorders (alcohol, opioids, stimulants, cannabis)
- Personality disorders (borderline, antisocial, narcissistic, etc.)
- Eating disorders (anorexia, bulimia, binge eating)
- Sleep disorders (insomnia, hypersomnia, circadian rhythm disorders)
- ADHD and neurodevelopmental disorders
- Suicide risk assessment and management
- Psychiatric emergencies
- Psychopharmacology
- Psychotherapy modalities

Evidence-based guidelines: NICE, APA, BAP, Maudsley Prescribing Guidelines
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Optional, Dict, List, Any
import re


class PsychiatryDomain(BaseDomainModule):
    """
    Psychiatry specialty domain covering mental health disorders,
    psychiatric emergencies, and psychopharmacology.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="psychiatry",
            version="1.0.0",
            dependencies=[],
            description="Psychiatric assessment and management of mental health disorders including depression, anxiety, psychosis, substance use, personality disorders, eating disorders, and psychiatric emergencies",
            keywords=[
                # Core psychiatry
                "mental health", "psychiatry", "psychological", "depression", "anxiety",
                "psychosis", "schizophrenia", "bipolar", "manic", "hypomanic",

                # Depressive disorders
                "mdd", "major depressive disorder", "depressed", "low mood", "hopelessness",
                "dysthymia", "persistent depressive disorder", "sad", "suicidal", "suicide",

                # Anxiety disorders
                "generalized anxiety", "gad", "panic", "panic attack", "phobia",
                "social anxiety", "agoraphobia", "claustrophobia", "specific phobia",
                "ocd", "obsessive compulsive", "ptsd", "post-traumatic stress",

                # Psychotic disorders
                "schizophrenia", "psychosis", "psychotic", "hallucination", "delusion",
                "schizoaffective", "schizotypal", "paranoia", "paranoid",

                # Bipolar disorder
                "bipolar", "manic depression", "mania", "hypomania", "mixed episode",
                "mood stabilizer", "lithium",

                # Personality disorders
                "borderline", "bpd", "antisocial", "narcissistic", "histrionic",
                "personality disorder", "cluster b", "cluster a",

                # Substance use
                "addiction", "substance abuse", "alcohol", "drug", "opioid", "heroin",
                "cocaine", "amphetamine", "cannabis", "marijuana", "withdrawal",
                "detox", "rehab", "dependence",

                # Eating disorders
                "anorexia", "bulimia", "binge eating", "eating disorder",
                "body image", "weight concern",

                # Sleep disorders
                "insomnia", "hypersomnia", "nightmare", "sleep problem",

                # ADHD
                "adhd", "add", "attention deficit", "hyperactive", "impulsive",
                "concentration", "focus", "restless",

                # Children's mental health
                "autism", "asd", "asperger", "neurodevelopmental", "conduct disorder",

                # Geriatric psychiatry
                "dementia", "alzheimer", "confusion", "memory loss", "delirium",

                # Treatments
                "antidepressant", "ssri", "snri", "antipsychotic", "mood stabilizer",
                "anxiolytic", "benzodiazepine", "psychotherapy", "cbt", "therapy",
                "counseling", "medication"
            ],
            capabilities=[
                "depression_assessment", "anxiety_disorder_management", "psychosis_management",
                "bipolar_disorder_treatment", "substance_use_disorder_treatment",
                "personality_disorder_management", "eating_disorder_treatment",
                "suicide_risk_assessment", "psychiatric_emergency_management",
                "psychopharmacology", "psychotherapy_referral", "adhd_assessment",
                "sleep_disorder_management", "ptsd_treatment", "ocd_management"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """
        Process psychiatric queries with emphasis on emergency recognition.
        """
        query_lower = query.lower()

        # EMERGENCY: Suicide risk, self-harm, psychosis with violence
        if any(term in query_lower for term in ["suicide", "kill myself", "want to die", "end it", "self-harm", "overdose"]) and \
           any(term in query_lower for term in ["plan", "intent", "going to", "want to"]):
            return self._handle_suicide_emergency(query, context)

        # EMERGENCY: Psychosis with danger to self/others
        if any(term in query_lower for term in ["psychosis", "hallucination", "delusion", "voices"]) and \
           any(term in query_lower for term in ["violent", "danger", "hurt", "weapon", "threat"]):
            return self._handle_psychiatric_emergency(query, context)

        # Depression
        if any(term in query_lower for term in ["depression", "depressed", "low mood", "hopeless", "worthless", "mdd", "sad"]):
            return self._handle_depression_query(query, context)

        # Anxiety disorders
        if any(term in query_lower for term in ["anxiety", "anxious", "panic", "worried", "gad", "phobia"]):
            return self._handle_anxiety_query(query, context)

        # Bipolar disorder
        if any(term in query_lower for term in ["bipolar", "mania", "manic", "hypomanic", "mood swings"]):
            return self._handle_bipolar_query(query, context)

        # Psychosis/Schizophrenia
        if any(term in query_lower for term in ["psychosis", "schizophrenia", "hallucination", "delusion", "voices", "paranoia"]):
            return self._handle_psychosis_query(query, context)

        # OCD
        if any(term in query_lower for term in ["ocd", "obsessive compulsive", "obsession", "compulsion"]):
            return self._handle_ocd_query(query, context)

        # PTSD
        if any(term in query_lower for term in ["ptsd", "post-traumatic", "trauma", "flashback", "nightmare"]):
            return self._handle_ptsd_query(query, context)

        # Substance use
        if any(term in query_lower for term in ["alcohol", "drug", "addiction", "opioid", "cocaine", "cannabis", "withdrawal", "detox"]):
            return self._handle_substance_use_query(query, context)

        # Personality disorders
        if any(term in query_lower for term in ["borderline", "bpd", "personality disorder", "antisocial", "narcissistic"]):
            return self._handle_personality_disorder_query(query, context)

        # Eating disorders
        if any(term in query_lower for term in ["anorexia", "bulimia", "binge eating", "eating disorder"]):
            return self._handle_eating_disorder_query(query, context)

        # ADHD
        if any(term in query_lower for term in ["adhd", "attention deficit", "hyperactive", "impulsive", "concentration"]):
            return self._handle_adhd_query(query, context)

        # Insomnia/Sleep disorders
        if any(term in query_lower for term in ["insomnia", "sleep problem", "can't sleep", "sleepless"]):
            return self._handle_insomnia_query(query, context)

        # Suicide risk (non-emergency assessment)
        if any(term in query_lower for term in ["suicidal", "suicide", "self-harm", "thoughts of death"]):
            return self._handle_suicide_risk_query(query, context)

        # General psychiatry
        return self._handle_general_psychiatry_query(query, context)

    def _handle_suicide_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle suicide emergency."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**SUICIDE EMERGENCY - IMMEDIATE ACTION REQUIRED**

**IF SUICIDE RISK IS IMMINENT (Plan, intent, means available):**

**IMMEDIATE ACTIONS:**
1. **DO NOT leave the person alone**
2. **Remove lethal means** (medications, weapons, sharp objects)
3. **Call emergency services** (999/911/112) - say "SUICIDE RISK"
4. **Go to nearest Emergency Department (A&E)**
5. **Contact crisis line**:
   - **Samaritans**: 116 123 (UK), 988 (US)
   - **Crisis Text Line**: Text HOME to 741741 (US)
   - **National Suicide Prevention Lifeline**: 988 (US)

**DO NOT:**
- Promise secrecy
- Judge or argue
- Leave them alone
- Try to "talk them out of it"

**DO:**
- Stay calm and supportive
- Listen without judgment
- Express concern ("I care about you, I'm worried")
- Ask directly about suicide ("Are you thinking about killing yourself?")
- Keep them safe until help arrives

**SUICIDE RISK ASSESSMENT** (for healthcare professionals):

**High Risk** (Immediate hospitalization):
- Active suicidal ideation with plan AND intent
- Access to lethal means
- Previous attempts (especially violent or recent)
- Hopelessness, command hallucinations
- Impulsivity, substance use
- Lack of social support

**Moderate Risk** (Urgent psychiatric evaluation within 24-48 hours):
- Suicidal ideation without plan OR without intent
- Ambivalence about living
- Some protective factors (family, responsibilities)

**Low Risk** (Outpatient management):
- Passive suicidal ideation ("wish I were dead") without plan/intent
- Good social support, protective factors
- Willing to follow safety plan

**SAFETY PLANNING:**
- **Warning signs**: Triggers, situations, thoughts
- **Coping strategies**: What has helped before
- **Social contacts**: Who to call for support
- **Professional contacts**: Therapist, crisis line, emergency department
- **Environment means restriction**: Remove or secure medications, weapons

**MEDICATION CONSIDERATIONS:**
- **Prescribe cautiously**: Start low, go slow, limited quantity
- **Avoid** if high risk: Tricyclics (toxic in overdose), MAOIs, lithium (narrow therapeutic index)
- **Preferred**: SSRIs (sertraline, citalopram - less toxic in overdose), mirtazapine
- **Co-prescribe**: Consider anxiolytic short-term (benzodiazepine limited supply with caution)

**FOLLOW-UP:**
- **High risk**: Hospital admission (voluntary or involuntary)
- **Moderate risk**: Urgent psychiatric follow-up (within 48 hours), daily contact until seen
- **Low risk**: Outpatient treatment, regular follow-up, safety plan

**Sources:** NICE NG225, APA Guidelines, NHS England
""",
            confidence=0.99,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Suicide Emergency",
                "urgency": "emergency",
                "sources": ["NICE NG225", "APA Guidelines", "NHS England"]
            }
        )

    def _handle_psychiatric_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle psychiatric emergency (psychosis with danger)."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**PSYCHIATRIC EMERGENCY - IMMEDIATE ACTION REQUIRED**

**IF VIOLENT, DANGEROUS, OR ARMED:**

**IMMEDIATE ACTIONS:**
1. **Call police/emergency** (999/911/112) - say "MENTAL HEALTH EMERGENCY"
2. **DO NOT approach** if weapon present
3. **Keep safe distance**
4. **Wait for trained professionals**

**IF NO WEAPON BUT DANGEROUS BEHAVIOR:**

**IMMEDIATE ACTIONS:**
1. **Ensure safety** (yourself, patient, others)
2. **Remove other patients** if clinical setting
3. **Call security/police** if needed
4. **Calm environment** (quiet, no crowds, minimize stimulation)
5. **De-escalate**: Speak calmly, slowly, clearly, do not threaten or argue, validate distress ("I can see you're upset"), offer choices where possible
6. **DO NOT** argue about delusions/hallucinations (but don't validate them either), don't touch without permission, don't corner or block exits

**RAPID TRANQUILIZATION** (if aggression/danger imminent and not responding to de-escalation):
- **Lorazepam** (2 mg PO/IM) - first-line (less EPS than antipsychotics)
- **OR Haloperidol** (5-10 mg IM) - second-line (monitor for EPS)
- **OR Olanzapine** (10 mg IM) - alternative (less EPS, more sedating)
- **OR Combination** (Lorazepam + Haloperidol IM) - most effective
- **Repeat** if no response after 30 minutes

**AFTER STABILIZATION:**
- **Vital signs**: BP, HR, O2 sats, temperature, GCS
- **Assessment**: Mental state exam, risk assessment (suicide, homicide, self-neglect), MSE
- **Investigations**: Bloods (FBC, U&E, LFT, TSH, glucose, alcohol levels), toxicology, ECG (if QT-prolonging meds considered)
- **Observation**: Close observation, no leave, 1:1 if high risk
- **Involuntary admission**: If risk to self/others and refusing treatment (MHA 1983 Section in UK)

**CAUSES OF ACUTE PSYCHOSIS**:
- **Primary**: Schizophrenia, schizoaffective disorder, bipolar disorder (manic with psychosis), severe depression with psychosis
- **Secondary**: Substance-induced (amphetamines, cocaine, cannabis, alcohol withdrawal), medical (delirium, hypoglycemia, hyponatremia, hypercalcemia, porphyria, lupus, neurosyphilis, HIV), medication-induced (steroids, dopaminergics, anticholinergics), neurological (stroke, tumor, trauma, epilepsy, encephalitis)

**Sources:** NICE CG220, Maudsley Prescribing Guidelines
""",
            confidence=0.98,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Psychiatric Emergency",
                "urgency": "emergency",
                "sources": ["NICE CG220", "Maudsley Prescribing Guidelines"]
            }
        )

    def _handle_depression_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle depression queries."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**DEPRESSION (Major Depressive Disorder)**

**DIAGNOSTIC CRITERIA (DSM-5)**:
- **5+ symptoms** during same 2-week period, represents change from functioning
- **At least one** symptom is (1) depressed mood OR (2) anhedonia (loss of interest/pleasure)
- **Symptoms**:
  1. Depressed mood (sad, empty, hopeless) - in children/adolescents can be irritable mood
  2. Markedly diminished interest/pleasure in all activities (anhedonia)
  3. Significant weight loss/gain or appetite change
  4. Insomnia or hypersomnia
  5. Psychomotor agitation or retardation
  6. Fatigue/loss of energy
  7. Worthlessness or excessive guilt
  8. Diminished ability to think/concentrate, indecisiveness
  9. Recurrent thoughts of death, suicidal ideation (without plan) or suicide attempt

- **Causes significant distress/impairment**
- **Not** due to substance/medical condition
- **Not** better explained by other mental disorder

**SPECIFIERS**:
- **Mild**: Few symptoms beyond minimum, minor functional impairment
- **Moderate**: Symptoms/impairment between mild and severe
- **Severe**: Most symptoms, marked impairment, may have psychotic features
- **With psychotic features**: Hallucinations/delusions (mood-congruent or incongruent)
- **In remission**: Partial (some symptoms persist) or Full (no symptoms for ≥2 months)
- **With anxious distress**: Tension, worry, restlessness, difficulty concentrating
- **With mixed features**: Subthreshold manic symptoms
- **With melancholic features**: Profound anhedonia, depression worse in morning, early morning awakening, excessive guilt
- **With atypical features**: Mood reactivity, weight gain/ increased appetite, hypersomnia, leaden paralysis, rejection sensitivity
- **With seasonal pattern**: Fall/winter onset, spring remission

**DIFFERENTIAL DIAGNOSIS**:
- **Grief/bereavement**: Pangs of grief, self-esteem preserved, waves of grief intermixed with positive memories
- **Adjustment disorder**: Depressed mood in response to stressor, but less severe, resolution when stressor remits
- **Dysthymia/Persistent depressive disorder**: Milder but chronic (≥2 years)
- **Bipolar disorder**: Screen for mania/hypomania (especially if antidepressant-induced)
- **Medical causes**: Hypothyroidism, anemia, vitamin B12/folate deficiency, medication side effects, substance use, neurological disorders (stroke, Parkinson's, dementia)

**INVESTIGATIONS** (if indicated):
- **Bloods**: FBC (anemia), U&E (electrolytes), LFT (liver disease), TSH (hypothyroidism), B12/folate (deficiency), calcium (hyperparathyroidism), fasting glucose/HbA1c (diabetes), syphilis serology (if risk), HIV (if risk)
- **Drug screen**: If substance use suspected
- **ECG**: If considering antidepressants with cardiac risk or QT-prolongation risk

**PSYCHOSOCIAL ASSESSMENT**:
- **Current stressors**: Relationships, work, finances, housing, bereavement, trauma
- **Social support**: Family, friends, community
- **Protective factors**: Employment, children, responsibilities, religious/spiritual beliefs, hope for future
- **Risk factors**: Previous episodes, suicide attempts, family history of depression/suicide, substance use, chronic illness, trauma, abuse, lack of support, unemployment, social isolation
- **Suicide risk**: Always assess - ideation, plan, intent, means, attempts, protective factors

**MANAGEMENT**:

**Mild depression**:
- **Psychoeducation**: Depression is common, treatable, not weakness, recovery expected
- **Self-help**: Exercise, sleep hygiene, regular routine, avoid alcohol/drugs, healthy eating, sunlight
- **Bibliotherapy**: CBT-based self-help books
- **Group CBT**: If available and acceptable
- **Watchful waiting**: With regular review (every 2 weeks)
- **Consider antidepressants** if: Persistent after 2 weeks of self-help, patient prefers, previous episodes

**Moderate-severe depression**:
- **Antidepressants + Psychotherapy** (CBT first-line)
- **SSRIs** (first-line):
  - **Citalopram** 20 mg daily (max 40 mg) - most evidence in primary care, dose-dependent QT prolongation (max 40 mg, caution if risk factors for QT prolongation)
  - **Escitalopram** 10 mg daily (max 20 mg) - S-enantiomer of citalopram, slightly more effective, same QT risk
  - **Sertraline** 50 mg daily (max 200 mg) - activating (good if low energy), safe in pregnancy, many drug interactions (CYP450)
  - **Fluoxetine** 20 mg daily (max 60 mg) - activating, long half-life (missed doses less problematic), safe in pregnancy
  - **Paroxetine** 20 mg daily (max 50 mg) - more sedating (good if anxious), anticholinergic (dry mouth, constipation, sexual dysfunction, weight gain), discontinuation syndrome (worst of SSRIs), AVOID in pregnancy
  - **Fluvoxamine** 100 mg daily (max 300 mg) - more sedating, many drug interactions
- **SNRIs** (second-line if SSRI ineffective or not tolerated):
  - **Venlafaxine XR** 75 mg daily (max 375 mg) - more activating, dose-dependent noradrenergic effects (≥150 mg), hypertension (monitor BP), discontinuation syndrome (bad)
  - **Duloxetine** 30 mg daily (max 120 mg) - also treats neuropathic pain, anxiety, hypertension (monitor BP), nausea (common)
- **Other antidepressants** (if SSRIs/SNRIs ineffective or not tolerated):
  - **Mirtazapine** 15 mg daily (max 45 mg) - sedating (good if insomnia), increased appetite (weight gain), no sexual dysfunction, no discontinuation syndrome, safe in cardiac disease, orthostatic hypotension
  - **Bupropion** (Wellbutrin) 150 mg daily (max 300 mg) - activating (good if low energy), no sexual dysfunction, aids smoking cessation, AVOID if eating disorder (seizure risk), seizure risk (0.1-0.4%, dose-dependent, caution with comorbid eating disorders, head trauma, brain injury, alcohol withdrawal, medications lowering seizure threshold)
  - **Trazodone** 150 mg daily (max 400 mg) - sedating (often used off-label for insomnia), orthostatic hypotension, priapism (rare but urgent), α1-blockade (nasal congestion)
  - **Vortioxetine** 10 mg daily (max 20 mg) - multimodal (serotonin modulator), cognitive benefits (may improve processing speed, executive function), sexual dysfunction (less than SSRIs but still occurs), nausea
  - **Reboxetine** 4 mg BD (max 12 mg) - NRI, less effective than SSRIs (second-line), activating, insomnia, dry mouth, urinary retention
- **Tricyclics** (third-line, specialist initiation):
  - **Amitriptyline** 25 mg daily (max 150 mg) - sedating, neuropathic pain, cheap, cardiotoxic (toxic in overdose), anticholinergic (dry mouth, constipation, urinary retention, blurred vision, cognitive impairment, confusion in elderly), orthostatic hypotension, weight gain, arrhythmias (prolonged QT)
  - **Lofepramine** 140 mg daily (max 210 mg) - less toxic than amitriptyline in overdose
  - **Clomipramine** 25 mg daily (max 250 mg) - most serotonergic TCA (good for OCD), similar side effects to amitriptyline
- **MAOIs** (fourth-line, specialist only, dietary and medication restrictions):
  - **Phenelzine**, **Tranylcypromine** - very effective but significant dietary restrictions (tyramine-rich foods - aged cheese, cured meats, tap beer, wine, soy sauce, broad beans), drug interactions (sympathomimetics, SSRIs, SNRIs, TCAs, meperidine, dextromethorphan), hypertensive crisis, orthostatic hypotension, weight gain, sexual dysfunction, insomnia, hepatotoxicity (phenelzine)
  - **Moclobemide** (RIMA) - reversible, dietary restrictions less strict but still advised, less effective

**TREATMENT PRINCIPLES**:
- **Start low, go slow** (especially in anxiety, elderly)
- **Therapeutic dose**: If no response after 2-4 weeks at starting dose, increase to therapeutic dose (SSRIs often need higher doses: fluoxetine 20-40 mg, sertraline 100-150 mg, citalopram 20-40 mg, escitalopram 10-20 mg, paroxetine 20-40 mg)
- **Therapeutic trial**: Continue for 6-8 weeks at therapeutic dose before switching (most respond by 4-6 weeks)
- **Partial response**: Continue current dose, consider augmentation
- **No response**: Switch antidepressant (different mechanism or class) or add augmentation
- **Recurrence prevention**: Continue antidepressant for ≥6 months after remission (first episode), 1-2 years (multiple episodes), possibly lifelong (multiple severe episodes with residual symptoms, chronic depression, comorbid anxiety, ongoing psychosocial stressors)

**AUGMENTATION STRATEGIES** (if partial response to adequate antidepressant trial):
- **Atypical antipsychotic**: Aripiprazole 2-15 mg daily, Quetiapine 150-300 mg daily (best evidence for augmentation), Olanzapine ± fluoxetine (especially with psychotic features), Risperidone 0.5-2 mg daily
- **Lithium**: 0.4-0.8 mmol/L (serum level), augmentation (especially if suicidality, hospitalization), monitor levels, thyroid, renal
- **Thyroid hormone** (T3): Liothyronine 20-40 mcg daily (augmentation, especially if subclinical hypothyroidism)
- **Buspirone**: 10-30 mg TDS (anxiety)
- **Combination antidepressants**: SSRI + Bupropion, SSRI + Mirtazapine (California rocket fuel), SSRI + Trazodone (insomnia), monitor for drug interactions and serotonin syndrome

**SIDE EFFECT MANAGEMENT**:
- **Nausea**: Take with food, start low, go slow, temporary, may persist with venlafaxine/duloxetine
- **Insomnia**: Take in morning (if activating), add trazodone/mirtazapine (if sedating), sleep hygiene
- **Sexual dysfunction**: Erectile dysfunction, delayed ejaculation, anorgasmia, decreased libido (dose-dependent, common with SSRIs/SNRIs - 30-70%), management: wait (may improve), dose reduction, switch to bupropion/reboxetine (no sexual dysfunction), mirtazapine (less sexual dysfunction), add bupropion (antidote), PDE5 inhibitors (sildenafil, tadalafil) for men
- **Weight gain**: Mirtazapine, paroxetine, amitriptyline, TCAs, MAOIs, quetiapine, olanzapine; monitor weight, lifestyle advice, consider switching (bupropion, fluoxetine, sertraline, venlafaxine cause less weight gain)
- **Dry mouth**: Sugar-free gum/candy, sip water, artificial saliva
- **Constipation**: Increase fluids, fiber, exercise, stool softeners, osmotic laxatives (macrogol, lactulose)
- **Urinary retention**: Reduce dose, switch (avoid TCAs, SNRIs if problematic), alpha-blockers (tamsulosin)
- **Blurred vision**: Reduce dose, switch (anticholinergic effect), reassure usually temporary
- **Discontinuation syndrome**: Flu-like symptoms (dizziness, nausea, headache, fatigue, sensory disturbances, anxiety, insomnia), dose-dependent (more common with paroxetine, venlafaxine, duloxetine), prevention: taper slowly (especially paroxetine, venlafaxine, duloxetine - over weeks-months), hold dose for several weeks before tapering, switch to fluoxetine (long half-life) then taper fluoxetine, treatment: restart antidepressant (if missed dose) or switch to fluoxetine then taper

**PSYCHOTHERAPY**:
- **CBT** (Cognitive Behavioral Therapy): First-line psychotherapy, as effective as antidepressants for mild-moderate depression, combined treatment better than either alone for moderate-severe, 12-20 sessions, homework, skills training: cognitive restructuring, behavioral activation, problem-solving
- **Behavioral activation**: Activity scheduling, graded activation, monitor mood, master schedule, pleasant events schedule
- **Interpersonal therapy (IPT)**: Focus on relationships, role transitions, grief, interpersonal disputes, interpersonal deficits
- **Psychodynamic psychotherapy**: Exploratory, insight-oriented, longer-term (especially if personality factors, trauma)
- **Couples therapy**: If relationship distress
- **Family therapy**: If family conflict, high expressed emotion
- **Group therapy**: Cost-effective, peer support, role modeling

**SPECIAL POPULATIONS**:
- **Pregnancy/postpartum**: Untreated depression risks (poor nutrition, poor prenatal care, preterm birth, low birth weight, developmental delay, postpartum depression), antidepressant risks (persistent pulmonary hypertension of newborn, neonatal adaptation syndrome, congenital malformations - small absolute risk), decision is individualized based on severity, previous episodes, patient preference, SSRIs generally safe (paroxetine associated with cardiac defects - avoid if possible), sertraline often preferred (most data), avoid paroxetine, TCAs (nortriptyline preferred if TCA), electroconvulsive therapy (ECT) if severe (especially with suicidality, catatonia)
- **Breastfeeding**: Sertraline preferred (low levels in breastmilk), paroxetine (also low), avoid doxepin, fluoxetine (higher levels), monitor infant
- **Children/adolescents**: Fluoxetine only SSRI approved for ≥8 years (depression), fluoxetine + CBT first-line, close monitoring for suicidality (especially first few weeks, dose changes), initiate low dose, go slow (5-10 mg, increase to 20 mg after 1-2 weeks, max 20-30 mg), regular follow-up (weekly for first 4 weeks), involve parents/school, screen for bipolar (mania risk with antidepressants)
- **Elderly**: Start low, go slow (half starting dose), increase slowly, therapeutic trial longer (12 weeks), lower therapeutic doses (citalopram 20 mg max due to QT risk, sertraline 50-100 mg, escitalopram 10 mg max due to QT risk), monitor for hyponatremia (SIADH), falls (orthostatic hypotension), anticholinergic burden (cognitive impairment, confusion, constipation, urinary retention), prefer SSRIs (sertraline, citalopram <65, escitalopram <65) or mirtazapine (if insomnia/anorexia), avoid TCAs (toxicity), avoid paroxetine (anticholinergic), avoid fluoxetine (long half-life - drug accumulation), consider venlafaxine (caution with hypertension), consider bupropion (avoid if seizure risk, dementia)

**TREATMENT-RESISTANT DEPRESSION (TRD)**:
- **Definition**: Failure to respond to ≥2 adequate antidepressant trials (different mechanisms, adequate dose, adequate duration)
- **Prevalence**: 30-50% of patients
- **Management**:
  - **Re-evaluate diagnosis**: Bipolar disorder, medical causes, medication adherence, comorbid substance use
  - **Optimization**: Adequate dose, adequate duration, therapeutic plasma levels (if available)
  - **Switch**: To different class (SSRI → SNRI → Mirtazapine/Bupropion → TCA → MAOI)
  - **Augmentation**: Atypical antipsychotic (aripiprazole, quetiapine), Lithium, Thyroid hormone, Buspirone, Combination antidepressants
  - **Psychotherapy**: CBT, IPT, psychodynamic
  - **Neuromodulation** (if severe, specialist):
    - **ECT** (Electroconvulsive Therapy): Most effective treatment for severe depression (especially with psychosis, catatonia, suicidality, pregnancy), 70-90% response, remission common, bilateral (more effective, more side effects) vs unilateral (less effective, fewer side effects), acute course 6-12 treatments (2-3 times/week), then maintenance/continuation ECT if relapse risk, side effects: memory problems (usually improves), confusion (post-ictal), headache, muscle aches
    - **rTMS** (Repetitive Transcranial Magnetic Stimulation): Non-invasive, magnetic fields to left dorsolateral prefrontal cortex, daily for 4-6 weeks, less effective than ECT but fewer side effects, good for mild-moderate depression or ECT-refractory, side effects: headache, scalp discomfort, rare seizure
    - **VNS** (Vagus Nerve Stimulation): Implanted device, chronic treatment, less effective than ECT, surgical risks
    - **DBS** (Deep Brain Stimulation): Experimental, surgical, highly selected patients

**PROGNOSIS**:
- **Recovery**: Most recover (50% within 6 months, 70% within 12 months), but relapse common (50% recur after first episode, 70% after second, 90% after third)
- **Chronic**: 10-20% develop chronic depression (>2 years)
- **Recurrence prevention**: Long-term antidepressants (especially if multiple episodes, severe episodes, residual symptoms, comorbid anxiety), psychotherapy (especially CBT, IPT), lifestyle (exercise, sleep hygiene, regular routine, avoid alcohol/drugs), monitoring for early warning signs (sleep disturbance, anxiety, irritability, anhedonia)

**SOURCES:** NICE CG90, APA Guidelines, BAP Guidelines, CANMAT Guidelines
""",
            confidence=0.97,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Depression",
                "sources": ["NICE CG90", "APA Guidelines", "BAP", "CANMAT"]
            }
        )

    def _handle_anxiety_query(self, str: str, context: dict) -> DomainQueryResult:
        """Handle anxiety disorder queries."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**ANXIETY DISORDERS**

**GENERALIZED ANXIETY DISORDER (GAD)**:

**Diagnostic Criteria (DSM-5)**:
- **Excessive anxiety/worry** about multiple events/activities (work, school, health, family, finances)
- **Difficult to control** worry
- **≥3 symptoms** (for ≥6 months): Restlessness/feeling keyed up, fatigue, concentration problems, irritability, muscle tension, sleep disturbance
- **Causes significant distress/impairment**
- **Not** due to substance/medical condition, better explained by another mental disorder

**PANIC DISORDER**:

**Diagnostic Criteria (DSM-5)**:
- **Recurrent unexpected panic attacks**: Abrupt surge of intense fear/discomfort peaking within minutes, with ≥4 of:
  - Palpitations, pounding heart, accelerated heart rate
  - Sweating
  - Trembling/shaking
  - Shortness of breath, feeling of smothering
  - Choking sensation
  - Chest pain/discomfort
  - Nausea/abdominal distress
  - Dizziness, unsteady, lightheaded, faint
  - Chills or heat sensations
  - Paresthesias (numbness/tingling)
  - Derealization/depersonalization
  - Fear of losing control or "going crazy"
  - Fear of dying
- **At least one attack** followed by ≥1 month of: Persistent worry about additional attacks or their consequences, maladaptive behavioral change (avoidance) to avoid attacks
- **Not** due to substance/medical condition, better explained by another mental disorder

**SPECIFIC PHOBIA**:
- **Marked fear/anxiety** about specific object/situation (e.g., flying, heights, animals, injections, blood)
- **Phobic object/situation almost always provokes immediate fear/anxiety**
- **Actively avoided** or endured with intense fear/anxiety
- **Fear/anxiety is disproportionate** to actual danger
- **Duration ≥6 months**, causes significant distress/impairment
- **Not** better explained by another mental disorder

**SOCIAL ANXIETY DISORDER** (Social Phobia):
- **Marked fear/anxiety** about one or more social situations (conversations, meeting unfamiliar people, being observed, performing in front of others)
- **Fear** of being negatively evaluated by others (humiliated, rejected, offended)
- **Social situations almost always provoke fear/anxiety** (children expressed by crying, tantrums, freezing, clinging, shrinking)
- **Social situations avoided** or endured with intense fear/anxiety
- **Fear/anxiety is disproportionate** to actual threat
- **Duration ≥6 months**, causes significant distress/impairment
- **Not** due to substance/medical condition, better explained by another mental disorder

**AGORAPHOBIA**:
- **Marked fear/anxiety** about ≥2 situations: Using public transportation, being in open spaces, being in enclosed spaces (shops, theaters), standing in line/being in a crowd, being outside home alone
- **Fear** that escape might be difficult or help unavailable if panic-like symptoms occur
- **Situations almost always provoke fear/anxiety**, avoided or endured with intense fear/anxiety
- **Duration ≥6 months**, causes significant distress/impairment
- **Not** better explained by another mental disorder

**SEPARATION ANXIETY DISORDER**:
- **Developmentally inappropriate/excessive fear/anxiety** about separation from attachment figures
- **≥3 symptoms**: Distress when anticipating/experiencing separation, worry about losing major attachment figures, worry about harm befalling attachment figures, reluctance to go out/away/sleep away from home/attachment figure, repeated nightmares about separation, repeated physical symptoms when separation occurs
- **Duration ≥4 weeks** (children) or ≥6 months (adults), causes significant distress/impairment
- **Not** better explained by another mental disorder

**MANAGEMENT**:

**GAD & Panic Disorder**:

**Psychotherapy** (first-line for mild-moderate, combined with meds for moderate-severe):
- **CBT**: Psychoeducation, anxiety monitoring, cognitive restructuring (identify and challenge catastrophic thoughts), worry time (schedule worry periods), problem-solving, relaxation techniques (deep breathing, progressive muscle relaxation, mindfulness, meditation), exposure (especially for panic disorder - interoceptive exposure: voluntarily induce physical symptoms of anxiety - hyperventilation, spinning - to learn they're not dangerous), behavioral experiments

**Pharmacotherapy** (first-line for moderate-severe):
- **SSRIs** (first-line):
  - **Escitalopram** 10 mg daily (max 20 mg) - first-line
  - **Paroxetine** 20 mg daily (max 60 mg) - first-line
  - **Sertraline** 50 mg daily (max 200 mg)
  - **Citalopram** 20 mg daily (max 40 mg)
  - **Fluoxetine** 20 mg daily (max 60 mg)
- **SNRIs**:
  - **Venlafaxine XR** 75 mg daily (max 225 mg) - first-line (extended-release)
  - **Duloxetine** 30 mg daily (max 120 mg)
- **Benzodiazepines** (short-term only, 2-4 weeks maximum, while waiting for SSRI/SNRI to take effect):
  - **Diazepam** 2-10 mg daily in divided doses - long-acting, anxiolytic
  - **Alprazolam** 0.25-1 mg TDS - short-acting, more abuse potential
  - **Lorazepam** 1-4 mg daily in divided doses - intermediate-acting, safer in elderly/liver disease
  - **Clonazepam** 0.5-2 mg daily - long-acting, also treats panic
  - **Risks**: Sedation, cognitive impairment, falls (elderly), respiratory depression, dependence, tolerance, withdrawal (anxiety rebound, tremor, seizures), contraindicated in pregnancy, breastfeeding, substance use disorders, caution in elderly, caution if respiratory disease, caution if driving/operating machinery
- **Pregabalin** (if SSRI/SNRI contraindicated or ineffective): 150-600 mg daily in divided doses - GABA analog, effective for GAD, side effects: dizziness, drowsiness, weight gain, edema
- **Buspirone** (if SSRI/SNRI contraindicated or as augmentation): 15-30 mg daily in divided doses - partial 5-HT1A agonist, non-sedating, no dependence/withdrawal, takes 2-4 weeks to work, less effective than SSRIs/SNRIs
- **Hydroxyzine** (if SSRI/SNRI contraindicated or as short-term adjunct): 25-100 mg daily in divided doses - antihistamine, sedating, short-term use only

**Panic Disorder**:
- **SSRIs/SNRIs**: First-line (prevention of panic attacks), same as GAD
- **Benzodiazepines**: Alprazolam, clonazepam (short-term, 2-4 weeks maximum, while waiting for SSRI/SNRI to take effect)
- **TCAs**: Imipramine, clomipramine (second-line, more side effects)
- **Psychotherapy**: CBT with interoceptive exposure (most effective non-pharmacological)

**Specific Phobia**:
- **CBT with exposure**: First-line, gradual exposure to feared object/situation, relaxation training, cognitive restructuring, response prevention, very effective (80-90% improvement)
- **Medications**: NOT routinely effective (anxiolytics may impair exposure)

**Social Anxiety Disorder**:
- **CBT**: First-line (especially in adolescents), exposure, cognitive restructuring, social skills training
- **SSRIs**: First-line pharmacotherapy (if CBT ineffective or not available/acceptable) - sertraline, paroxetine, escitalopram, venlafaxine
- **SNRIs**: Venlafaxine
- **Benzodiazepines**: Short-term only (2-4 weeks maximum) while waiting for SSRI/SNRI to take effect
- **Beta-blockers**: Propranolol 10-40 mg PRN (performance anxiety - public speaking, performing) - reduces somatic symptoms (palpitations, tremor, sweating), does NOT reduce psychological anxiety, not first-line

**Agoraphobia**:
- **CBT with exposure**: First-line, in vivo exposure, interoceptive exposure
- **SSRIs/SNRIs**: Pharmacotherapy (same as panic disorder)

**Separation Anxiety Disorder**:
- **CBT**: First-line
- **SSRIs**: If CBT ineffective (especially in adults)

**PROGNOSIS**:
- **Chronic but treatable**: Most anxiety disorders are chronic without treatment but respond well to CBT and/or medications
- **Relapse common**: Continue treatment for ≥12 months after remission, taper medications slowly, CBT skills help prevent relapse

**SOURCES:** NICE CG123, NICE CG159, APA Guidelines
""",
            confidence=0.95,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Anxiety Disorders",
                "sources": ["NICE CG123", "NICE CG159", "APA Guidelines"]
            }
        )

    def _handle_bipolar_query(self, str: str, context: dict) -> DomainQueryResult:
        """Handle bipolar disorder queries."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**BIPOLAR DISORDER**

**DIAGNOSTIC CRITERIA (DSM-5)**:

**Bipolar I Disorder**:
- **Manic episode**: ≥1 week (or any duration if hospitalization) of abnormally/ persistently elevated/irritable mood + increased energy/activity, plus ≥3 (4 if mood irritable) symptoms:
  - Inflated self-esteem/grandiosity
  - Decreased need for sleep
  - More talkative/pressure to keep talking
  - Flight of ideas/racing thoughts
  - Distractibility
  - Increased goal-directed activity (socially, occupationally, sexually) or psychomotor agitation
  - Excessive involvement in risky activities (buying sprees, sexual indiscretions, foolish business investments)
- **Causes significant impairment** or hospitalization, or psychotic features
- **NOT** due to substance/medical condition
- **Major depressive episodes** (optional but common)

**Bipolar II Disorder**:
- **Hypomanic episode**: ≥4 consecutive days of abnormally/ persistently elevated/irritable mood + increased energy/activity, plus ≥3 (4 if mood irritable) symptoms (same as mania but milder, no hallucinations/delusions, no hospitalization, no severe impairment)
- **Major depressive episode**: ≥2 weeks of ≥5 symptoms (depressed mood, anhedonia, plus 3 of: weight/appetite change, sleep disturbance, psychomotor change, fatigue, worthlessness/guilt, concentration difficulties, suicidal ideation)
- **Causes significant distress/impairment**
- **NOT** due to substance/medical condition
- **NO** manic episode (by definition)

**Cyclothymic Disorder**:
- **≥2 years** (1 year in children/adolescents) of numerous periods of hypomanic symptoms (not meeting full criteria) and depressive symptoms (not meeting full criteria)
- **Symptom-free intervals** <2 months at a time
- **NO** major depressive episode, manic episode, or hypomanic episode of ≥4 days

**SPECIFIERS**:
- **With psychotic features**: Hallucinations/delusions (mood-congruent or mood-incongruent)
- **With rapid cycling**: ≥4 mood episodes in 12 months (more common in women, associated with hypothyroidism, antidepressant use)
- **With mixed features**: Concurrent symptoms of opposite pole (e.g., mania with depressive symptoms, depression with hypomanic symptoms)
- **With atypical features**: Atypical depression (mood reactivity, weight gain, hypersomnia, leaden paralysis, rejection sensitivity)
- **With melancholic features**: Profound anhedonia, depression worse in morning, early morning awakening, excessive guilt
- **With seasonal pattern**: Regular temporal relationship between season and mood episode onset/remission (more common for bipolar II)
- **With peripartum onset**: Mood episode onset during pregnancy or in 4 weeks postpartum
- **Anxious distress**: Prominent anxiety symptoms

**DIFFERENTIAL DIAGNOSIS**:
- **Unipolar depression** (MDD): Screen for hypomania/mania (especially if antidepressant-induced, early onset depression, family history of bipolar, atypical depression, psychotic depression, rapid cycling, severe depression)
- **Schizoaffective disorder**: Mood episode plus psychotic symptoms without mood symptoms (≥2 weeks)
- **Drug-induced** (cocaine, amphetamines, cannabis, alcohol withdrawal): Urine drug screen, abstinence, re-evaluate after 4 weeks of abstinence
- **Medical causes**: Hyperthyroidism (TSH, T4), Cushing's syndrome (24-hour urine cortisol, dexamethasone suppression test), neurological disorders (stroke, brain tumor, epilepsy, MS, head trauma), medications (corticosteroids, dopaminergics, antidepressants)
- **Borderline personality disorder**: Mood instability (but mood episodes last hours to days, not weeks to months), chronic, emptiness, abandonment fears, self-harm, identity disturbance, unstable relationships (comorbid with bipolar)

**INVESTIGATIONS** (if indicated):
- **Bloods**: FBC, U&E, LFT, TSH, free T4, glucose, calcium, albumin, CRP, ESR (to rule out medical causes)
- **Drug screen**: Urine toxicology (especially if psychosis, mania, or unclear diagnosis)
- **ECG**: If considering medications with cardiac risk (lithium, antipsychotics)
- **MRI brain**: If neurological symptoms, focal deficits, atypical presentation, first-episode psychosis, late-onset (>40)

**MANAGEMENT**:

**Acute Mania**:
- **Hospitalization**: If severe (psychosis, risk to self/others, inability to care for self), involuntary admission if refusing treatment and danger present
- **Medications** (first-line):
  - **Atypical antipsychotic** (monotherapy or with mood stabilizer):
    - **Olanzapine** 10-20 mg daily (max 30 mg) - first-line, rapid onset, sedating, weight gain, metabolic syndrome, triglycerides, diabetes risk, hyperprolactinemia
    - **Quetiapine** 100-300 mg daily in 2 divided doses (max 800 mg) - first-line, sedating, orthostatic hypotension, weight gain, metabolic syndrome
    - **Risperidone** 2-6 mg daily in 2 divided doses (max 16 mg) - first-line, hyperprolactinemia (gynecomastia, galactorrhea, sexual dysfunction, osteoporosis), EPS, weight gain
    - **Aripiprazole** 10-30 mg daily (max 30 mg) - activation (may be needed for depression), akathisia (inner restlessness - common), less weight gain/metabolic issues
    - **Asenapine** 10 mg SC BD (sublingual) - fast-acting, less weight gain
    - **Cariprazine** 1.5-3 mg daily - metabolic neutrality, less weight gain
    - **Brexpiprazole** 2-4 mg daily - metabolic neutrality
    - **Haloperidol** (typical antipsychotic) 5-15 mg daily in divided doses IM/PO - rapid tranquilization if highly agitated, high EPS risk (dystonia, parkinsonism, akathisia, tardive dyskinesia), neuroleptic malignant syndrome (rare but life-threatening), hyperprolactinemia
  - **Mood stabilizer** (if already on or if continuing after acute episode):
    - **Lithium** 600-1200 mg daily (serum level 0.6-1.2 mmol/L), loading dose (600-1200 mg daily) for rapid stabilization, monitor levels (6-12 hours after loading, then twice weekly until stable, then every 3 months), ECG (if risk factors), TFTs (hypothyroidism risk - every 6-12 months), U&E (renal toxicity risk - every 3-6 months), avoid in renal impairment, pregnancy (teratogenic - Ebstein's anomaly if first trimester), dehydration (risk of toxicity), NSAIDs (ACE inhibitors, ARBs, diuretics - reduce lithium excretion, increase levels)
    - **Sodium Valproate** (Depakote) 1000-2000 mg daily in 2-3 divided doses (serum level 50-100 mcg/mL), rapid onset, loading dose (20 mg/kg), teratogenic (neural tube defects - avoid in pregnancy, especially first trimester), weight gain, polycystic ovaries, hyperandrogenism, thrombocytopenia, hepatotoxicity (rare but life-threatening), pancreatitis, monitor LFTs, FBC, valproate level
    - **Carbamazepine** 400-800 mg daily in 2 divided doses (serum level 4-12 mg/L), enzyme inducer (reduces levels of many medications including oral contraceptives, warfarin, antipsychotics), bone marrow suppression (aplastic anemia, agranulocytosis - rare but life-threatening, monitor FBC weekly for first 3 months), SIADH, hyponatremia, rash (Stevens-Johnson syndrome - HLA-B*1502 in Han Chinese, SE Asian), teratogenic (neural tube defects), less effective for acute mania than lithium or valproate
- **Combination**: Antipsychotic + mood stabilizer (more effective than either alone, especially for severe mania with psychosis)

**Bipolar Depression**:
- **Quetiapine** 300 mg daily (in divided doses) - first-line (FDA-approved), sedating, weight gain, metabolic syndrome
- **Lurasidone** 20-120 mg daily (with food) - FDA-approved, metabolic neutrality, akathisia
- **Olanzapine + Fluoxetine** (OFC) 6/25, 12/25, 6/50 mg daily - FDA-approved, weight gain, metabolic syndrome
- **Cariprazine** 1.5-3 mg daily - FDA-approved, metabolic neutrality, akathisia
- **Lithium** (serum level 0.6-1.2 mmol/L) - augmentation, especially if suicidality, good evidence for suicidal prevention
- **Lamotrigine** 25-200 mg daily - maintenance, prevention of depressive episodes, slow titration (25 mg daily for 2 weeks, then 50 mg daily for 2 weeks, then increase by 25-50 mg every 1-2 weeks to 200 mg daily), Stevens-Johnson syndrome (rare but life-threatening rash - 10% of patients, more common if rapid titration, valproate reduces clearance, stop immediately if rash occurs), teratogenic (avoid in pregnancy)
- **Quetiapine** + Lamotrigine - combination therapy
- **Other mood stabilizers**: Lithium (if not already on), Valproate (if not pregnant, avoid in women of childbearing age unless contraception used)
- **Antidepressants** (CONTROVERSIAL):
  - **Generally AVOID** as monotherapy (may switch to mania/hypomania or rapid cycling)
  - **May be considered** as adjunct to mood stabilizer if depression severe (especially bipolar II, rapid cycling), always with mood stabilizer, avoid tricyclics (higher switch risk), prefer SSRIs (sertraline, escitalopram), bupropion (no sexual dysfunction, may help smoking cessation), monitor for mania/hypomania, discontinue if manic/hypomanic symptoms occur
  - **Alternatives to antidepressants**: Psychotherapy (CBT, IPSRT - interpersonal and social rhythm therapy), sleep regulation, regular routines

**Maintenance/Prevention of Relapse**:
- **Mood stabilizer**: Long-term (lifelong for most patients, especially if severe episodes, psychotic features, suicidality)
  - **Lithium** (first-line): Most evidence for suicide prevention, also reduces manic and depressive episodes, monitor levels, renal, thyroid, pregnancy (teratogenic, avoid if possible, risks vs benefits discussion)
  - **Sodium Valproate** (first-line in men, women with effective contraception): Effective for mania and depression maintenance, avoid in pregnancy (teratogenic), monitor LFTs, FBC, valproate level
  - **Lamotrigine**: More effective for depression prevention than mania prevention, slow titration, Stevens-Johnson syndrome (rare but life-threatening rash), safer in pregnancy than valproate/lithium (but still discuss risks)
  - **Carbamazepine**: Less commonly used now, enzyme inducer (drug interactions), less effective for depression
  - **Olanzapine**: Long-term, especially if psychotic features, weight gain, metabolic syndrome
  - **Quetiapine**: Long-term, especially if bipolar depression, weight gain, metabolic syndrome
  - **Aripiprazole**: Long-term, less weight gain/metabolic issues, akathisia
  - **Asenapine**: Long-term, less weight gain
  - **Combination**: Mood stabilizer + atypical antipsychotic (if breakthrough episodes)
- **Psychotherapy**:
  - **CBT**: Identify early warning signs, lifestyle regularity (sleep, routine), stress management, problem-solving
  - **IPSRT** (Interpersonal and Social Rhythm Therapy): Stabilize daily rhythms (sleep, meals, activity), interpersonal issues
  - **Family-focused therapy**: Psychoeducation, communication training, problem-solving
  - **Group therapy**: Peer support, skill-building
- **Lifestyle**: Regular sleep schedule (critical - sleep deprivation triggers mania), avoid alcohol/drugs (trigger episodes), regular exercise, stress management, regular routines, mood monitoring (daily mood chart), early intervention for warning signs

**Rapid Cycling**:
- **Definition**: ≥4 mood episodes per year (manic, hypomanic, depressive, mixed)
- **Management**: Optimize mood stabilizer (lithium or valproate first-line), avoid antidepressants (may worsen rapid cycling), consider combination therapy (mood stabilizer + atypical antipsychotic), treat hypothyroidism (if present), avoid sleep deprivation, regular routines, psychotherapy (IPSRT)

**Mixed Episode** (Manic + Depressive symptoms):
- **High risk**: Suicidality, rapid cycling, poor treatment response
- **Management**: Olanzapine, Quetiapine, Lithium, Valproate, Aripiprazole, combination therapy, AVOID antidepressants

**Catatonia** (if present):
- **Symptoms**: Mutism, stupor, staring, posturing, waxy flexibility, stereotypies, echolalia/echopraxia, negativism
- **Management**: Benzodiazepines (lorazepam 2-4 mg IM/PO) - first-line, ECT (rapid, life-saving if catatonia is severe, especially malignant catatonia, NMS)

**SPECIAL POPULATIONS**:
- **Pregnancy**: High risk of relapse (especially postpartum - 50% relapse, especially if off medications), untreated bipolar risks (poor self-care, poor prenatal care, postpartum depression, psychosis, suicide, infanticide), medication risks (teratogenicity - lithium: Ebstein's anomaly, valproate: neural tube defects, carbamazepine: neural tube defects, lamotrigine: cleft lip/palate), decision is individualized based on severity, previous episodes, patient preference, generally AVOID valproate (highest teratogenic risk), consider lithium (especially if suicide risk), lamotrigine (safer than lithium/valproate), atypical antipsychotics (olanzapine, quetiapine - limited data), AVOID carbamazepine, AVOID valproate, close monitoring (more frequent reviews), involve obstetrics, pediatrics, mental health, ECT (if severe, especially with suicidality, psychosis, catatonia, safer than medications)
- **Postpartum**: High risk of relapse (especially postpartum psychosis - 25-50% of women with bipolar disorder), prophylactic mood stabilizer (lithium) immediately postpartum (especially if previous postpartum psychosis), close monitoring (weekly for first month), sleep (critical - sleep deprivation triggers mania), support (partner, family), infant safety (if psychosis, hospitalization with baby), ECT (if severe)
- **Children/adolescents**: Similar presentation but more rapid cycling, mixed episodes, more irritability than euphoria, more comorbid ADHD, more severe course, high suicide risk, lithium, valproate, atypical antipsychoids (aripiprazole, risperidone), lamotrigine (slow titration), psychoeducation, family therapy, school involvement

**PROGNOSIS**:
- **Chronic**: Lifelong condition
- **Episodic**: Mood episodes with inter-episode recovery (most common), but residual symptoms common between episodes, functional impairment may persist
- **Suicide risk**: 15-20% complete suicide (highest of all psychiatric disorders), especially during mixed episodes, depressive episodes, early illness, postpartum, lithium reduces suicide risk
- **Comorbidities**: Anxiety disorders (especially GAD, panic, social anxiety), substance use disorders (30-60%), ADHD, personality disorders (especially borderline), medical conditions (metabolic syndrome, cardiovascular disease)
- **Functioning**: Variable, some maintain good functioning between episodes, others have significant impairment, early diagnosis and treatment improves prognosis

**SOURCES:** NICE CG185, BAP Guidelines, CANMAT Guidelines, WFSBP Guidelines
""",
            confidence=0.97,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Bipolar Disorder",
                "sources": ["NICE CG185", "BAP", "CANMAT", "WFSBP"]
            }
        )

    def _handle_psychosis_query(self, str: str, context: dict) -> DomainQueryResult:
        """Handle psychosis/schizophrenia queries."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**PSYCHOSIS AND SCHIZOPHRENIA**

**PSYCHOSIS DEFINITION**:
- **Symptoms**: Hallucinations (auditory, visual, tactile, olfactory, gustatory), delusions (false fixed beliefs - persecutory, referential, somatic, religious, grandiose), disorganized thought/speech (loose associations, derailment, tangentiality, incoherence, word salad), disorganized/abnormal motor behavior (catatonia, posturing, stereotypies, agitation), negative symptoms (flattened affect, alogia, avolition, anhedonia, asociality)
- **Duration**: ≥1 month (or less if successfully treated)
- **Causes significant distress/impairment**

**SCHIZOPHRENIA** (DSM-5):
- **Two or more** of the following, each present for significant portion during 1-month period (or less if successfully treated):
  1. Delusions
  2. Hallucinations
  3. Disorganized speech
  4. Grossly disorganized or catatonic behavior
  5. Negative symptoms
- **At least one** of items 1, 2, or 3 must be present
- **Functioning**: Markedly below level achieved before onset (in work, interpersonal relations, self-care)
- **Duration**: Continuous signs ≥6 months (6 months must include symptoms of active psychosis, may include prodromal/residual periods)
- **Schizoaffective disorder and depressive/bipolar disorder with psychotic features excluded**
- **Not** due to substance/medical condition
- **Not** better explained by autism spectrum disorder or communication disorder

**SCHIZOPHRENIFORM DISORDER**: Same symptoms as schizophrenia but duration 1-6 months

**BRIEF PSYCHOTIC DISORDER**: Psychotic symptoms lasting ≥1 day to <1 month, eventual full recovery

**DELUSIONAL DISORDER**: Fixed false belief(s) for ≥1 month, apart from delusion, functioning is not markedly impaired, hallucinations are not prominent ( tactile/olfactory if present), tactile/olfactory hallucinations may be present if related to delusional theme

**SCHIZOAFFECTIVE DISORDER**: Unrestricted period of illness during which there is a major mood episode (manic or depressive) concurrent with symptoms meeting criterion A for schizophrenia, plus delusions or hallucinations for ≥2 weeks in absence of mood episode (during the lifetime duration of the illness)

**PRODROME** (Early Warning Signs):
- **Duration**: Months to years before full psychosis
- **Symptoms**: Social withdrawal, anhedonia, avolition, reduced concentration, odd beliefs, unusual perceptual experiences, disorganized speech, odd behavior, decline in functioning (school, work, social), sleep disturbance, anxiety, irritability, depression, suicidal ideation
- **High-risk states**: UHR (Ultra High Risk), ARMS (At Risk Mental States), CHR (Clinical High Risk)
- **Conversion to psychosis**: 20-35% within 2 years (higher if family history of psychosis, substance use, high symptom severity, poor functioning, male gender)
- **Intervention**: Antipsychotics (may reduce conversion but unclear if benefits outweigh risks - metabolic syndrome, EPS), CBT, family therapy, case management, monitor closely, treat comorbidities (depression, anxiety, substance use)

**DIFFERENTIAL DIAGNOSIS**:
- **Substance-induced psychosis**: Cannabis (especially high-potency, early use, heavy use, synthetic cannabinoids), stimulants (cocaine, amphetamines, methamphetamine, ADHD medications, modafinil), hallucinogens (LSD, psilocybin), alcohol (rare but occurs, especially withdrawal/delirium tremens), sedatives (benzodiazepine withdrawal), inhalants, anticholinergics, steroids, dissociatives (ketamine, PCP) - urine drug screen, abstinence, re-evaluate after 4 weeks of abstinence, consider cannabinoid hyperemesis syndrome
- **Medical causes**: Delirium (acute, fluctuating consciousness, medical illness, medications, substance withdrawal), neurological disorders (stroke, tumor, epilepsy (temporal lobe epilepsy especially), TBI, encephalitis, HIV, neurosyphilis, Huntington's, Wilson's disease, metachromatic leukodystrophy), endocrine disorders (hyperthyroidism, hypercortisolism, hypo/hyperglycemia, hyperparathyroidism, porphyria), autoimmune disorders (SLE, vasculitis, CNS lupus, multiple sclerosis, paraneoplastic syndromes, Hashimoto's encephalopathy, anti-NMDA receptor encephalitis, limbic encephalitis), nutritional deficiencies (B12, thiamine, niacin), infections (malaria, syphilis, HIV, Creutzfeldt-Jakob disease) - bloods (FBC, U&E, LFT, TFT, glucose, calcium, albumin, CRP, ESR), syphilis serology, HIV test, autoimmune screen (ANA, ANCA, anti-NMDA, anti-TPO, anti-thyroglobulin, anti-LGI1, CASPR2), MRI brain (always for first-episode psychosis, late-onset (>40), focal neurological symptoms, atypical presentation), EEG (if seizures, episodic symptoms, fluctuating consciousness), lumbar puncture (if infection suspected, especially if fever, headache, meningism, neurological signs, autoimmune encephalitis suspected)
- **Other psychiatric disorders**: Bipolar disorder with psychotic features, major depressive disorder with psychotic features, schizoaffective disorder, brief psychotic disorder, schizophreniform disorder, delusional disorder, PTSD with flashbacks, dissociative disorders (dissociative identity disorder), severe OCD with poor insight, severe anxiety with depersonalization/derealization

**INVESTIGATIONS** (for first-episode psychosis):
- **Bloods**: FBC, U&E, LFT, TFT, glucose, calcium, albumin, CRP, ESR, syphilis serology, HIV, B12, folate, copper (Wilson's), ceruloplasmin (Wilson's)
- **Urine toxicology**: Screen for substances (amphetamines, cocaine, opiates, cannabis, benzodiazepines)
- **MRI brain**: Always for first-episode psychosis, late-onset (>40), focal neurological signs
- **EEG**: If seizures, episodic symptoms, fluctuating consciousness
- **Lumbar puncture**: If infection suspected (fever, headache, meningism, neurological signs), or autoimmune encephalitis suspected
- **ECG**: If considering antipsychotics (especially ziprasidone, iloperidone - QT prolongation risk)

**TREATMENT** (Comprehensive, Multidisciplinary):

**Acute Psychosis** (First-Episode or Relapse):
- **Hospitalization**: If risk to self/others, unable to care for self, severe symptoms, medical assessment needed, involuntary admission if refusing treatment and danger present (MHA 1983 Section in UK)
- **Antipsychotics** (rapid tranquilization if agitated/risk):
  - **Second-generation (atypical) antipsychotics** (first-line):
    - **Olanzapine** 10-20 mg daily (max 30 mg) - first-line, rapid onset, sedating, effective for positive and negative symptoms (better than other antipsychotics for negative symptoms), weight gain (very common, significant), metabolic syndrome (diabetes, dyslipidemia), hyperprolactinemia (less than risperidone but occurs), sedation, orthostatic hypotension, QT prolongation (monitor ECG if risk factors), dose-dependent side effects, most effective for negative symptoms and relapse prevention (with clozapine)
    - **Risperidone** 2-6 mg daily in 2 divided doses (max 16 mg) - first-line, effective for positive symptoms, hyperprolactinemia (gynecomastia, galactorrhea, sexual dysfunction, amenorrhea, osteoporosis, higher prolactin than other atypicals), EPS (dystonia, parkinsonism, akathisia - less than typical antipsychotics but more than other atypicals), weight gain, sedation, orthostatic hypotension, QT prolongation (monitor ECG if risk factors), available in long-acting injection (Risperdal Consta)
    - **Amisulpride** 400-800 mg daily (max 1200 mg) - first-line in some countries, effective for positive symptoms, some evidence for negative symptoms (at lower doses 50-300 mg), hyperprolactinemia (gynecomastia, galactorrhea, sexual dysfunction, amenorrhea), less weight gain/metabolic issues than olanzapine/quetiapine, EPS (less than risperidone), QT prolongation (monitor ECG if risk factors), renal excretion (reduce dose if renal impairment)
    - **Quetiapine** 400-800 mg daily in 2 divided doses (max 800 mg) - first-line, sedating (may help with agitation, insomnia), orthostatic hypotension (especially initial titration), weight gain, metabolic syndrome, hyperprolactinemia (less than risperidone), minimal EPS (even at high doses), QT prolongation (dose-dependent, monitor ECG if risk factors), available in extended-release (Seroquel XR), used in bipolar depression as well
    - **Aripiprazole** 10-30 mg daily (max 30 mg) - first-line, dopamine partial agonist (stabilizes dopamine), may be activating (may help with negative symptoms, depression, cognitive symptoms), akathisia (very common, inner restlessness - 10-20%, dose-dependent), less weight gain/metabolic issues, less hyperprolactinemia (may lower prolactin), EPS (less than risperidone, but akathisia more common), available in long-acting injection (Abilify Maintena), used in bipolar disorder, augmentation of depression
    - **Ziprasidone** 40-160 mg daily in 2 divided doses with meals (max 160 mg) - first-line in some countries, metabolic neutrality (no weight gain, less metabolic issues), QT prolongation (dose-dependent, black box warning, requires ECG monitoring, contraindicated with other QT-prolonging meds, cardiac disease, electrolyte disturbances), EPS (similar to risperidone), hyperprolactinemia, sedation
    - **Clozapine** 300-600 mg daily in 2 divided doses (max 900 mg) - **TREATMENT-RESISTANT SCHIZOPHRENIA** (failure to respond to ≥2 adequate trials of antipsychotics from different classes), most effective antipsychotic for refractory schizophrenia, reduces suicidality (in schizophrenia), effective for positive symptoms (especially hallucinations, delusions), effective for negative symptoms (some evidence), agranulocytosis (0.5-1%, life-threatening, requires weekly FBC for 18 weeks, then fortnightly for 6 months, then monthly thereafter, stop immediately if agranulocytosis (ANC <1500/mm³ or significant drop)), seizures (dose-dependent), myocarditis/cardiomyopathy (rare but fatal, 0.1-0.5%, tachycardia, chest pain, palpitations, dyspnea, ECG changes (arrhythmias, T wave inversions, elevated troponin), stop immediately, cardiology review), myocarditis risk highest in first 2 months (especially 3-4 weeks), monitor ECG, troponin, CRP, ESR weekly for first 4 weeks, monthly thereafter, orthostatic hypotension, tachycardia, sedation, sialorrhea (drooling - very common, uncomfortable, social stigma, treat with anticholinergic - hyoscine, glycopyrrolate, botulinum toxin), constipation, urinary retention (anticholinergic), weight gain, metabolic syndrome, diabetes, dyslipidemia, NMS (neuroleptic malignant syndrome - rare but life-threatening, fever, rigidity, autonomic instability, altered mental status), requires clozapine monitoring service (weekly FBCs), mandatory for treatment-resistant schizophrenia
  - **First-generation (typical) antipsychotics** (second-line, due to more side effects):
    - **Haloperidol** 5-15 mg daily in 2 divided doses IM/PO (max 30 mg) - rapid tranquilization, high EPS risk (dystonia, parkinsonism, akathisia, tardive dyskinesia), neuroleptic malignant syndrome (rare but life-threatening), hyperprolactinemia, QT prolongation, less commonly used now due to EPS, still used for rapid tranquilization, available in long-acting depot (Haldol Decanoate)
    - **Chlorpromazine** 100-400 mg daily in 3-4 divided doses (max 1000 mg) - sedating, anticholinergic, hypotension, minimal EPS compared to haloperidol, used in low doses for agitation in dementia (caution - black box warning for increased mortality in elderly dementia patients), rarely used now in schizophrenia
    - **Flupenthixol** (depot) 20-40 mg IM every 2-4 weeks (first-generation depot) - long-acting, EPS, hyperprolactinemia, used if non-adherence to oral meds
    - **Pimozide** 2-10 mg daily (max 20 mg) - typical antipsychotic, EPS, QT prolongation (black box warning), rarely used now
  - **Rapid tranquilization** (if highly agitated, violent, dangerous):
    - **Lorazepam** 1-2 mg IM/PO (repeat every 30-60 minutes if needed, max 10 mg/day) - first-line, anxiolytic, sedating, safer in elderly/liver disease (metabolized by glucuronidation, not CYP450), less respiratory depression than other benzodiazepines, amnestic (blackout risk), dependence (limit to 2-4 weeks maximum)
    - **Haloperidol** 5-10 mg IM (repeat every 30-60 minutes if needed, max 30 mg/day) - alternative if lorazepam ineffective, high EPS risk (dystonia, parkinsonism, akathisia, tardive dyskinesia), neuroleptic malignant syndrome (rare but life-threatening), may combine with lorazepam (haloperidol + lorazepam IM)
    - **Olanzapine** 10 mg IM - alternative rapid tranquilization, less EPS than haloperidol, more sedation, QT prolongation (monitor ECG if risk factors)
    - **Ziprasidone** 10-20 mg IM - alternative rapid tranquilization, less EPS, QT prolongation (monitor ECG)
    - **Restraint**: Last resort, only if danger and less restrictive interventions failed, follow protocols (debrief after, document, minimize duration, prevent complications - aspiration, DVT, nerve compression, injury)

**Maintenance/Relapse Prevention**:
- **Continuation**: Same antipsychotic that achieved remission (unless poor tolerability/side effects)
- **Duration**: Lifelong (after first-episode psychosis, especially if relapse risk factors - poor premorbid functioning, severe symptoms, long duration of untreated psychosis, negative symptoms, cognitive impairment, family history, male gender), relapse risk high if antipsychotic stopped (70-80% relapse within 1 year vs 30-40% if continued), discuss risks/benefits with patient/family, informed decision-making
- **Dose**: Lowest effective dose (minimize side effects, ensure adherence), some patients may need lower doses than acute phase
- **Depot/long-acting injectable antipsychotics** (LAIs): If non-adherence, preference for depot, consider first-episode (especially if poor insight, non-adherence, substance use), advantages: guaranteed adherence (no forgetting, no refusal to take), steady levels, early warning of relapse (no need to rely on patient reporting insight), less risk of overdose/suicide (no pills to hoard), disadvantages: injections, cost, less flexible dosing, less patient autonomy
  - **Risperidone LAI** (Risperdal Consta) 25-50 mg IM every 2 weeks (first LAI, oral risperidone supplementation for 3 weeks after first injection)
  - **Paliperidone LAI** (Invega Sustenna, Xeplion) 117-234 mg IM every 4 weeks (once monthly, no oral supplementation needed, paliperidone is active metabolite of risperidone, less prolactin than risperidone)
  - **Olanzapine LAI** (Zypadhera) 210-405 mg IM every 2-4 weeks (requires oral supplementation for 3 weeks after first injection, post-injection delirium syndrome - sedation, confusion, delirium lasting 1-3 days after injection)
  - **Aripiprazole LAI** (Abilify Maintena) 400 mg IM monthly (loading dose 675 mg with oral aripiprazole for 14 days, then 400 mg monthly, or 975 mg every 6 weeks, 1080 mg every 2 months)
  - **Haloperidol decanoate** (Haldol Decanoate) 50-200 mg IM every 4 weeks (first-generation depot, high EPS)
  - **Flupenthixol decanoate** 20-40 mg IM every 2-4 weeks (first-generation depot, high EPS)
  - **Clozapine LAI** (Clozapine Depot) - not widely available, off-label

**Treatment-Resistant Schizophrenia** (failure to respond to ≥2 adequate antipsychotic trials from different classes, duration ≥6 weeks at therapeutic dose, failure to respond is defined as <20% symptom reduction, persistent symptoms, functional impairment):
- **Clozapine**: Gold standard for treatment-resistant schizophrenia, start 12.5-25 mg daily (or 12.5 mg BD), titrate by 25-50 mg every 2-3 days to 300 mg daily in divided doses (faster titration if inpatient), then increase by 50-100 mg every 1-2 weeks to 300-600 mg daily (max 900 mg), therapeutic dose varies (some respond to 300 mg, others need 600-900 mg), monitor levels (trough level >350 mcg/L is associated with better response, but not mandatory), requires mandatory clozapine monitoring service (weekly FBCs for 18 weeks, then fortnightly for 6 months, then monthly), most effective for refractory schizophrenia, reduces suicidality, reduces hospitalization, improves quality of life, improves functioning, improves negative symptoms (some evidence), side effects: agranulocytosis (0.5-1%, weekly FBC mandatory, stop immediately if ANC <1500/mm³ or significant drop), seizures (dose-dependent, especially if high dose, rapid titration, alcohol, benzodiazepine withdrawal, electrolyte disturbances, epilepsy), myocarditis/cardiomyopathy (0.1-0.5%, fatal in 50% of cases, tachycardia, chest pain, palpitations, dyspnea, ECG changes, elevated troponin, stop immediately, cardiology review, highest risk in first 2 months especially 3-4 weeks, monitor ECG, troponin, CRP, ESR weekly for first 4 weeks then monthly), orthostatic hypotension, tachycardia, sedation, sialorrhea (drooling - very common, uncomfortable, social stigma, treat with anticholinergic - hyoscine 0.125-0.25 mg BD, glycopyrrolate 1-2 mg BD, botulinum toxin injections), constipation (common), urinary retention (anticholinergic, especially in men with BPH), weight gain (very common, significant), metabolic syndrome (diabetes, dyslipidemia), diabetes risk (5-10% develop diabetes, monitor fasting glucose/HbA1c regularly), dyslipidemia (elevated triglycerides, cholesterol), NMS (rare), requires clozapine management protocol
- **Augmentation strategies** (if clozapine partial response or clozapine-resistant):
  - **Clozapine + Risperidone** - augmentation with another antipsychotic (evidence limited, increased side effects - EPS, metabolic, hyperprolactinemia)
  - **Clozapine + Lamotrigine** - lamotrigine 25-200 mg daily (slow titration due to rash risk, especially if also on valproate, stop lamotrigine immediately if rash occurs, carry rash more slowly), may help with depression, negative symptoms
  - **Clozapine + ECT** - very effective for clozapine-resistant schizophrenia, especially if catatonia, severe depression, suicidality, weekly or twice-weekly ECT for 6-12 treatments, then maintenance ECT
  - **Clozapine + Mood stabilizer** - lithium, valproate, lamotrigine (especially if comorbid bipolar, mood instability)
  - **Clozapine + Antidepressant** - citalopram, fluvoxamine (especially if comorbid depression, OCD symptoms)
  - **Clozapine + Memantine** - glutamatergic, cognitive benefits (some evidence)
  - **Clozapine + Sulpiride** - atypical antipsychotic augmentation (limited evidence)
- **Other strategies** (if clozapine contraindicated, not tolerated, or ineffective):
  - **Clozapine rechallenge** - if clozapine was previously effective but stopped due to agranulocytosis, neutropenia, myocarditis, seizures, may rechallenge if benefit outweighs risk, very cautious monitoring
  - **Olanzapine + Fluoxetine** (OFC) - combination may help with comorbid depression, but metabolic burden
  - **ECT** (Electroconvulsive Therapy) - effective for treatment-resistant schizophrenia, especially with catatonia, severe depression, suicidality, clozapine-resistant (70% response rate), acute course 6-12 treatments (2-3 times/week), then maintenance ECT (weekly then fortnightly then monthly) to prevent relapse, side effects: memory problems (anterograde amnesia - difficulty forming new memories, retrograde amnesia - difficulty remembering past events, usually improves within weeks-months, sometimes permanent), confusion (post-ictal), headache, muscle aches, rare seizure (during ECT), NMS (very rare), anesthesia risks, requires informed consent, consider if severe, treatment-resistant, clozapine-resistant, catatonia, severe depression, suicidality

**Psychotherapy** (adjunctive to medications, not alternative):
- **CBT for psychosis** (CBTp): Psychoeducation about psychosis, normalization of symptoms, coping strategies for hallucinations/delusions, challenging beliefs (reality testing), behavioral experiments, relapse prevention, moderately effective for positive symptoms, especially when combined with medications, most effective for recent-onset psychosis, persistent positive symptoms, relapse prevention
- **Family therapy**: Psychoeducation for families about schizophrenia, reduce expressed emotion (criticism, hostility, overinvolvement - increases relapse), improve communication, problem-solving, reduce relapse rates, improve functioning
- **Social skills training**: Improve social functioning, relationships, independent living skills
- **Cognitive remediation**: Improve cognitive functioning (attention, memory, executive functioning) which improves negative symptoms and functioning
- **Supported employment/volunteering/education**: Individual placement and support (IPS) - most effective vocational intervention, competitive employment with job coach, improves employment outcomes, functioning, quality of life
- **Case management**: Assertive community treatment (ACT) team - multidisciplinary team provides intensive community support, reduces hospitalization, improves adherence, improves functioning

**Negative Symptoms** (flattened affect, alogia, avolition, anhedonia, asociality):
- **Challenging to treat**: Less responsive to antipsychotics than positive symptoms
- **Antipsychotics**: Second-generation (especially olanzapine, amisulpride, clozapine) may have some benefit for negative symptoms, but often limited
- **Antidepressants**: Adding antidepressants (especially SSRIs - sertraline, fluoxetine, SNRIs - venlafaxine) may help (especially if comorbid depression, but even without depression, some evidence), but may risk switching to mania/hypomania in bipolar, careful monitoring
- **Glutamatergic agents**: Memantine 5-20 mg daily (NMDA antagonist), sarcosine (N-methylglycine) (NMDA co-agonist), limited evidence
- **Cholinesterase inhibitors**: Galantamine (for cognitive symptoms, especially in older adults with cognitive impairment), limited evidence
- **Psychotherapy**: CBTp (address negative beliefs about abilities, behavioral activation, graded activity), cognitive remediation (improves cognitive functioning which may improve negative symptoms), social skills training, supported employment
- **Combination strategies**: Olanzapine + Fluoxetine (OFC), Olanzapine + Samidorphan (glutamatergic agent, investigational), Clozapine + Lamotrigine

**Cognitive Symptoms** (attention, memory, executive functioning):
- **Very common**: 80-90% have cognitive impairment (even in first-episode), cognitive deficits are present, contribute to functional impairment, often overlooked
- **Domains**: Attention/vigilance, working memory, verbal memory, visual memory, executive functioning (planning, cognitive flexibility, abstraction), processing speed, social cognition
- **Assessment**: Repeatable Battery for the Assessment of Neuropsychological Status (RBANS), MATRICS Consensus Cognitive Battery (MCCB)
- **Treatment**: Cognitive remediation (computer-based cognitive training, improves cognition, functioning), second-generation antipsychotics (especially olanzapine, clozapine may have some cognitive benefits compared to first-generation), cholinesterase inhibitors (galantamine, donepezil - investigational), modafinil (wakefulness-promoting, may help attention), aerobic exercise (may improve cognition), avoid anticholinergic medications (TCAs, antiparkinsonian agents, antihistamines, bladder antimuscarinics - worsen cognition)

**Special Populations**:
- **Pregnancy**: Untreated psychosis risks (poor self-care, poor prenatal care, suicide, infanticide, poor mother-infant bonding), medication risks (teratogenicity - typical antipsychotics: neural tube defects, congenital malformations; clozapine: agranulocytosis, myocarditis, seizures; olanzapine: diabetes risk, weight gain; aripiprazole: safest in pregnancy - more data), decision is individualized based on severity, patient preference, generally AVOID typical antipsychotics if possible, AVOID valproate (highest teratogenic risk), consider clozapine (if treatment-resistant, risks vs benefits discussion, requires clozapine monitoring service), consider aripiprazole (safer in pregnancy), consider second-generation antipsychotics (olanzapine, quetiapine - limited data, monitor for diabetes, weight gain), ECT (if severe, especially with suicidality, psychosis, catatonia, safer than medications), involve obstetrics, pediatrics, mental health
- **Postpartum**: High risk of relapse (especially if medications stopped), postpartum psychosis (15-20% of women with schizophrenia, risk of infanticide), prophylactic antipsychotic (especially if previous postpartum psychosis), close monitoring (weekly for first month), sleep (critical), support (partner, family), infant safety (if psychosis, hospitalization without baby or with baby depending on severity), ECT (if severe)

**PROGNOSIS**:
- **Chronic**: Lifelong condition for most (60-70%)
- **Course**: Variable (10-20% recover completely after first episode with minimal residual symptoms, 20-30% have multiple episodes with good inter-episode recovery, 40-50% have significant symptoms between episodes, 10-20% have severe, continuous course), earlier diagnosis and treatment improves prognosis, negative symptoms and cognitive impairment predict worse course, substance use worsens prognosis, poor premorbid functioning predicts worse course, male gender predicts worse course, duration of untreated psychosis (DUP) predicts worse course (shorter DUP - better prognosis)
- **Functional outcomes**: 20-30% achieve good functioning (employment, independent living, relationships), 30-40% moderate functioning (some support needed), 30-40% poor functioning (significant support needed, disability), early intervention improves outcomes, cognitive remediation improves functioning, supported employment improves vocational outcomes
- **Suicide risk**: 5-10% complete suicide (especially young males, first 5-10 years, during active psychosis, post-discharge, after treatment failure, with command hallucinations, with comorbid depression), clozapine reduces suicidality in schizophrenia
- **Comorbidities**: Depression (50%), anxiety disorders (30-40%), substance use disorders (30-60%), OCD (10-20%), PTSD (10-20%), personality disorders (especially borderline, schizotypal, schizotypal), medical conditions (metabolic syndrome, cardiovascular disease, respiratory disease - smoking-related), homelessness, incarceration
- **Life expectancy**: Reduced by 15-20 years (mostly due to cardiovascular disease, suicide, accidents, respiratory disease, unhealthy lifestyle - smoking, obesity, inactivity, poor diet, substance use, medication side effects - metabolic syndrome, diabetes, dyslipidemia, weight gain, EPS (parkinsonism, tardive dyskinesia), hyperprolactinemia), physical health monitoring essential (weight, BMI, waist circumference, BP, fasting glucose/HbA1c, fasting lipids, smoking cessation, exercise, healthy diet)

**SOURCES:** NICE CG178, APA Guidelines, Maudsley Prescribing Guidelines, BAP Guidelines
""",
            confidence=0.98,
            metadata={
                "specialty": "Psychiatry",
                "focus": "Psychosis and Schizophrenia",
                "sources": ["NICE CG178", "APA", "Maudsley", "BAP"]
            }
        )

    def _handle_substance_use_query(self, str: str, context: dict) -> DomainQueryResult:
        """Handle substance use disorder queries."""

        return DomainQueryResult(
            domain_name="psychiatry",
            answer="""
**SUBSTANCE USE DISORDERS**

**DEFINITION (DSM-5)**:
- **Impaired control**: Craving, unsuccessful efforts to cut down, substance use in larger amounts/longer than intended, great deal of time spent obtaining/using/recovering, use despite knowledge of problems
- **Social impairment**: Failure to fulfill major role obligations, continued use despite interpersonal problems
- **Risky use**: Recurrent use in hazardous situations, continued use despite physical/psychological problems
- **Tolerance**: Need increased amounts to achieve desired effect, diminished effect with continued use
- **Withdrawal**: Characteristic withdrawal syndrome when stopped (or use to avoid/relieve withdrawal)

**ALCOHOL USE DISORDER**:

**Severity**: Mild (2-3 criteria), Moderate (4-5 criteria), Severe (≥6 criteria)

**Withdrawal** ( occurs 6-24 hours after last drink, peaks 24-48 hours, resolves by 5-7 days):
- **Mild-moderate**: Tremor, anxiety, nausea, vomiting, sweating, tachycardia, hypertension, insomnia, agitation
- **Severe (delirium tremens)**: Hallucinations (visual, tactile - "formication" - bugs crawling on skin), delusions, disorientation, confusion, agitation, tachycardia, hypertension, fever, dehydration, electrolyte disturbances, seizures (6-48 hours after last drink), occurs 2-3 days after last drink, lasts 2-3 days, high mortality (5-15% if untreated)
- **Wernicke's encephalopathy**: Ocular abnormalities (nystagmus, ophthalmoplegia), ataxia, confusion - thiamine (vitamin B1) deficiency, EMERGENCY (thiamine 100 mg IV TDS before glucose, then 100 mg TDS for 3-5 days, then 100 mg daily), untreated → Korsakoff's syndrome (irreversible anterograde/retrograde amnesia, confabulation)
- **Management**:
  - **Benzodiazepine** (to prevent seizures, DT, reduce agitation): Chlordiazepoxide (Librium) 50-100 mg PO QDS (or 25-50 mg QID if severe), tapering over 5-7 days; Diazepam 10-20 mg PO QDS (or 5-10 mg QID if severe), tapering over 5-7 days; Lorazepam 2-4 mg PO/IM TDS (if hepatic failure - safer), tapering over 5-7 days
  - **Thiamine** 100 mg PO/IV TDS (or 100 mg PO daily for prophylaxis) - BEFORE glucose (avoid Wernicke's), continue for 3-5 days then daily
  - **Fluids**: Correct dehydration, electrolytes (especially Mg, K, Na), glucose (correct hypoglycemia)
  - **Monitoring**: Vitals, CIWA-Ar (Clinical Institute Withdrawal Assessment) score every 4-8 hours, adjust benzodiazepine based on score
  - **Nutrition**: Multivitamin, folate, B12, magnesium
  - **Environment**: Quiet, low stimulation, observation

**AUDIT-C** screening:
- **C**: How many drinks in a typical day?
- **C**: How many drinks in a typical week?
- **A**: How often do you have 6+ drinks (men) or 4+ drinks (women) on one occasion?
- **Cut down**: Have people ever criticized your drinking?
- **Annoyed**: Have people ever annoyed you by criticizing your drinking?
- **Guilty**: Have you ever felt guilty about your drinking?
- **Eye-opener**: Have you ever had a drink first thing in the morning to steady your nerves or get rid of a hangover?
- **Score**: ≥3 suggests hazardous drinking, ≥4 suggests alcohol use disorder

**Management (Abstinence/Reduction)**:
- **Detoxification**: Benzodiazepine taper (5-7 days), thiamine, vitamins, fluids, monitoring
- **Psychosocial**:
  - **Motivational interviewing**: Enhance motivation to change, resolve ambivalence
  - **CBT**: Coping with cravings, refusal skills, relapse prevention, problem-solving
  - **Groups**: AA (Alcoholics Anonymous), SMART Recovery, LifeRing
  - **Family therapy**: Involve family, address enabling behaviors, improve communication
  - **Contingency management**: Rewards for abstinence (voucher, privileges)
- **Medications** (to reduce craving, prevent relapse):
  - **Naltrexone** 50 mg daily (or 380 mg IM monthly) - opioid antagonist, reduces craving, reduces heavy drinking, especially if strong cravings, family history of alcoholism, contraindicated in liver failure, opioid use, hepatitis, hepatotoxicity (monitor LFTs)
  - **Acamprosate** 666 mg TDS (2 g daily) - normalizes glutamate, reduces craving, especially if abstinent, safe in liver failure, diarrhea (common side effect)
  - **Disulfiram** 250-500 mg daily - deterrent (causes unpleasant reaction [flushing, throbbing headache, nausea, vomiting, palpitations, hypotension, tachycardia, anxiety, syncope] if alcohol consumed while taking disulfiram), compliance is major issue, requires supervised administration (clinic, family), contraindicated in cardiovascular disease, psychosis, pregnancy, caution if hepatic failure (even more hepatotoxicity with alcohol + disulfiram)
  - **Baclofen** 30-80 mg daily in 3 divided doses - GABA-B agonist, reduces craving, some evidence, sedation, dizziness, weakness

**OPIOID USE DISORDER**:

**Withdrawal** (occurs 6-12 hours after last use for short-acting opioids like heroin, 24-72 hours for long-acting opioids like methadone, peaks 2-3 days, resolves by 5-7 days):
- **Symptoms**: Anxiety, agitation, insomnia, lacrimation, rhinorrhea, yawning, sweating, gooseflesh, muscle aches, GI cramps, diarrhea, nausea, vomiting, fever, chills, dilated pupils
- **Management**:
  - **Methadone** 20-30 mg daily (titrate to 40-80 mg daily) - first-line, opioid agonist, prevents withdrawal, reduces craving, illicit opioid use, high retention, reduces HIV/HCV, employment, monitored dispensing (daily), pregnancy-safe, QT prolongation (monitor ECG), interactions with many medications (CYP450), risk of diversion (take-home doses after 3-6 months of abstinence)
  - **Buprenorphine** 4-16 mg daily (sublingual) - first-line, partial opioid agonist, safer than methadone (ceiling on respiratory depression), take-home possible from start, office-based treatment, precipitates withdrawal if not opioid-dependent (wait until moderate withdrawal - COWS ≥8), available as buprenorphine/naloxone (Suboxone) - discourages injection, available as depot (Buvidal, Sublocade) - monthly/biweekly injections
  - **Naltrexone** 50 mg daily (or 380 mg IM monthly) - opioid antagonist, requires complete detoxification (must be opioid-free for 7-10 days), reduces craving, prevents relapse, contraindicated if still using opioids (precipitates severe withdrawal), less effective than methadone/buprenorphine (poor adherence), no opioid effects, safer in pregnancy
  - **Lofexidine** 2.16-2.88 mg daily in 3-4 divided doses (0.18-0.24 mg TDS/QID) - alpha-2 agonist, non-opioid treatment for withdrawal (clonidine alternative), reduces withdrawal symptoms, FDA-approved, hypotension, bradycardia
  - **Symptomatic treatment**: Loperamide 2 mg QID PRN diarrhea, NSAIDs for muscle aches, promethazine 25 mg TDS/QID for nausea, sleep
  - **Harm reduction**: If not abstinent, supervised consumption sites, needle/syringe programs, naloxone distribution (overdose reversal), safe injection education, HIV/HCV testing/treatment

**STIMULANT USE DISORDER** (Cocaine, Amphetamine, Methamphetamine):

**Withdrawal** (occurs hours to days after last use, lasts days to weeks):
- **Symptoms**: Dysphoria, anhedonia, fatigue, increased appetite, insomnia or hypersomnia, vivid unpleasant dreams, psychomotor retardation or agitation, craving
- **Management**: No FDA-approved medications (supportive care), symptomatic treatment (modafinil for fatigue/sleepiness, antidepressants for depression - especially bupropion for cocaine), CBT, contingency management (voucher for cocaine-free urine screens), abstinence-based incentives, avoid stimulants (caffeine, nicotine), exercise, sleep hygiene, relapse prevention planning

**CANNABIS USE DISORDER**:

**Withdrawal** (occurs 1-2 days after stopping heavy daily use, lasts 1-2 weeks):
- **Symptoms**: Irritability, anxiety, insomnia, decreased appetite, restlessness, depressed mood, nightmares, sweating, shakiness, fever, chills, headache
- **Management**: No FDA-approved medications (supportive care), symptomatic treatment (short-term benzodiazepines (lorazepam 1-2 mg TDS for 3-7 days if severe insomnia/anxiety), gabapentin 300-900 mg TDS (may help anxiety, insomnia, craving), SSRIs if depression/anxiety persists after 1-2 weeks of abstinence), CBT, motivational enhancement, abstinence, exercise, sleep hygiene, psychoeducation about cannabis hyperemesis syndrome, cannabis psychosis risk (especially if early onset, heavy use, high-potency, genetic vulnerability)

**SMOKING CESSATION**:

**Management**:
- **Behavioral interventions**: Motivational interviewing, CBT, Quitline counseling, smoking cessation programs, identify triggers, develop coping strategies, relapse prevention planning
- **Pharmacotherapy** (double abstinence rates):
  - **Varenicline** (Chantix/Champix) 0.5-1 mg BID for 12 weeks + 1 week titration (0.5 mg daily for 3 days, then 0.5 mg BID for 4 days, then 1 mg BID for 11 weeks) - nicotine receptor partial agonist, reduces craving, withdrawal, pleasure from smoking, most effective monotherapy, nausea (30%, take with food, dose reduction if needed), insomnia, vivid dreams (uncommon but unpleasant), depression, suicidality (black box warning, monitor for depression, suicidality, especially if previous psychiatric illness, recent suicidal ideation), contraindicated in pregnancy, avoid if severe renal impairment
  - **Bupropion** (Zyban) 150 mg daily for 3 days, then 150 mg BID for 7-12 weeks - NDRI (dopamine-norepinephrine reuptake inhibitor), reduces craving, withdrawal, weight gain (unlike varenicline), contraindicated in seizure disorder, eating disorders, head trauma, alcohol withdrawal, MAOIs, contraindicated in pregnancy, avoid if liver failure
  - **NRT** (Nicotine Replacement Therapy) - patch, gum, lozenge, inhaler, nasal spray, combination (patch + acute form) most effective, safe in pregnancy, reduce withdrawal, craving
  - **Combination**: NRT + bupropion (especially if previous relapse)
- **Follow-up**: Close follow-up (weekly for first month), monitor for relapse, encourage quit attempts (most require multiple quit attempts before success), reward abstinence

**GENERAL PRINCIPLES**:
- **Harm reduction**: If not abstinent, reduce harms (needle/syringe programs, naloxone, safe injection education, supervised consumption sites, HIV/HCV testing/treatment, safe sex education)
- **Motivational interviewing**: Enhance motivation to change, resolve ambivalence, patient-centered, non-judgmental, collaborative
- **Stages of change**: Precontemplation (not considering change), contemplation (ambivalent), preparation (planning to change), action (making changes), maintenance (maintaining change), relapse (return to use), interventions matched to stage
- **Relapse prevention**: Identify triggers (people, places, things, emotions - HALT: hungry, angry, lonely, tired), develop coping strategies, emergency plan (who to call, what to do), lifestyle changes (avoid using friends, avoid using places, new activities, new friends who don't use), support groups, CBT
- **Co-occurring disorders**: Treat comorbid psychiatric disorders (depression, anxiety, psychosis), integrated treatment (simultaneous treatment of substance use and mental health disorders), psychiatric symptoms may improve with abstinence, but not always (especially if primary psychiatric disorder)

**SOURCES:** NICE CG115, NICE CG181, APA Guidelines, ASAM Guidelines
""",
            confidence=0.96,
    metadata={
                "specialty": "Psychiatry",
        "focus": "Substance Use Disorders",
        "sources": ["NICE CG115", "NICE CG181", "APA", "ASAM"]
    }
        )

def _handle_general_psychiatry_query(self, str: str, context: dict) -> DomainQueryResult:
    """Handle general psychiatry queries."""

    return DomainQueryResult(
        domain_name="psychiatry",
        answer="""
**PSYCHIATRY - GENERAL PRINCIPLES**

**PSYCHIATRIC ASSESSMENT**:

**Mental Status Examination (MSE)**:
- **Appearance**: Grooming, hygiene, clothing (appropriate for season/weather?), eye contact, psychomotor activity (retarded, agitated, catatonia, stereotypies), self-harm signs (scars, tattoos, track marks)
- **Behavior**: Cooperation, eye contact, rapport, level of consciousness, orientation (x3 - person, place, time), attention/concentration, psychomotor agitation/retardation, abnormal movements (tardive dyskinesia, parkinsonism, dystonia, akathisia), self-harm behaviors (head-banging, cutting, burning, scratching, picking, hair-pulling)
- **Speech**: Rate (pressured, slowed, normal), volume (loud, soft, normal), flow (organized, tangential, derailment, incoherence), content (pressure of speech, poverty of content, thought blocking, thought withdrawal, thought insertion, thought broadcasting, neologisms, word salad, clang associations, echolalia, mutism)
- **Mood**: Subjective mood (depressed, elevated, anxious, irritable, euthymic), objective affect (constricted, blunted, flat, expansive, labile, euthymic), congruence between mood and affect
- **Thoughts**: Form (linear, tangential, circumstantial, flight of ideas, loosening of associations, thought blocking, thought withdrawal, thought insertion, thought broadcasting, derailment, incoherence), content (delusions - persecutory, referential, grandiose, somatic, religious, guilt, shame, jealousy, nihilistic, mood-congruent vs mood-incongruent, bizzare, systematized, primary vs secondary), suicidal ideation (passive vs active, plan, intent, means, precautions, attempts), homicidal ideation (target, plan, intent, means, precautions)
- **Perception**: Hallucinations (auditory [most common in psychosis], visual [most common in medical/organic], tactile, olfactory, gustatory, hypnagogic, hypnopompic), illusions (misinterpretations), depersonalization (feeling detached from self, unreal, like observing self), derealization (feeling detached from environment, unreal, dreamlike), thought insertion/withdrawal/broadcasting (passive phenomena - psychotic symptoms)
- **Cognition**: Orientation (person, place, time), attention (sustained, concentration), memory (immediate [registration], short-term [working memory], long-term [remote memory]), executive functioning (abstraction, judgment, planning, insight, reasoning), intelligence (estimated from fund of knowledge, vocabulary), cognitive deficits (dementia, delirium, intellectual disability, head injury, stroke)
- **Insight**: Illness insight (awareness of psychiatric illness, attribution of symptoms to illness), treatment insight (willingness to accept treatment), prognosis insight, dangerousness insight (risk to self/others - may require involuntary treatment)

**SUICIDE RISK ASSESSMENT** (always assess):
- **Ideation**: "Do you have thoughts that life is not worth living?" "Do you wish you were dead?" "Do you have thoughts of killing yourself?" (ask directly, does NOT increase risk)
- **Plan**: "Do you have a plan for how you would kill yourself?" (specificity, lethality, availability)
- **Intent**: "Do you think you will act on these thoughts?" "When do you think you would do it?" (active vs passive ideation)
- **Means**: "Do you have access to [means]?" (firearms, medications, sharp objects, high places)
- **History**: Previous attempts (most important risk factor), family history of suicide/psychiatric illness, recent loss (relationship, job, bereavement), recent discharge from psychiatric hospitalization (especially within 3 months), recent start/change of antidepressants (especially <30 years), chronic illness/pain, hopelessness, worthlessness, loneliness, isolation, intoxication, impulsivity, personality traits (borderline, antisocial), pregnancy/postpartum (if maternal suicide risk, protect baby as well as mother)
- **Protective factors**: Children, family responsibilities, religious/spiritual beliefs, fear of death, hope for future, reasons for living, future plans, social support, treatment engagement, fears of suicide method (pain, disfigurement), pets
- **Intervention**: Hospitalize if high risk (plan + intent + means, severe symptoms, lack of protective factors), remove means (firearms, medications, sharp objects), close observation (1:1 if high risk, 15-minute checks), safety contract (limit reliance - not reliable if high risk), involve family/supports, crisis plan (who to call, what to do), emergency contact numbers (911/999/112, crisis lines), follow-up (very soon, daily if high risk), medications (antidepressants, hospitalization, ECT if severe)

**PSYCHOTROPIC MEDICATIONS**:

**Antidepressants** - See Depression section

**Antipsychotics** (see Psychosis section for full details):
- **Second-generation (atypical)**: Olanzapine, Quetiapine, Risperidone, Aripiprazole, Ziprasidone, Clozapine, Lurasidone, Brexpiprazole, Cariprazine, Asenapine, Iloperidone, Sertindole
- **First-generation (typical)**: Haloperidol, Chlorpromazine, Flupentixol, Pimozide (less commonly used due to EPS)
- **Side effects**: EPS (extrapyramidal symptoms) - dystonia (spasms, muscle spasms, especially neck, eyes, tongue, jaw, opisthotonus, torticollis, oculogyric crisis - EMERGENCY if respiratory compromise), parkinsonism (bradykinesia, rigidity, tremor - cogwheeling, pill-rolling, mask-like facies, shuffling gait, stooped posture), akathisia (inner restlessness, inability to sit still, rocking, pacing, fidgeting, very distressing, mistaken for agitation/psychosis - do NOT increase antipsychotic), tardive dyskinesia (involuntary, choreoathetoid movements of tongue, lips, face, trunk, extremities, irreversible in 50%, especially with long-term use, more common in elderly, women, mood disorders, risk factors - duration, dose, high-potency typicals, smoking, withdrawal worsens, AIMS exam), neuroleptic malignant syndrome (NMS - rare but life-threatening: fever, rigidity, autonomic instability - tachycardia, labile BP, diaphoresis, incontinence, delirium, elevated CK, leukocytosis, metabolic acidosis, renal failure, death), hyperprolactinemia (galactorrhea, gynecomastia, amenorrhea, sexual dysfunction, osteoporosis, infertility - especially with risperidone, amisulpride, less with olanzapine/quetiapine, less with aripiprazole/brexpiprazole), weight gain (very common with olanzapine, clozapine, quetiapine, less with risperidone, less with aripiprazole/brexpiprazole/ziprasidone/lurasidone/cariprazine), metabolic syndrome (diabetes, dyslipidemia, hypertension), QT prolongation (ziprasidone, iloperidone, especially if risk factors, electrolyte disturbances, congenital long QT, medications), sedation, orthostatic hypotension (quetiapine, clozapine, especially initial titration), anticholinergic effects (dry mouth, constipation, urinary retention, blurred vision, cognitive impairment - more with clozapine, chlorpromazine, less with second-generation antipsychotics), seizures (clozapine - dose-dependent, especially with rapid titration, alcohol withdrawal, benzodiazepine withdrawal, electrolyte disturbances, epilepsy), agranulocytosis (clozapine - mandatory weekly FBC for 18 weeks, then fortnightly for 6 months, then monthly), myocarditis/cardiomyopathy (clozapine - tachycardia, chest pain, palpitations, dyspnea, ECG changes, elevated troponin, highest risk first 2 months), sialorrhea (clozapine - drooling, uncomfortable, treat with hyoscine 0.125-0.25 mg BD, glycopyrrolate 1-2 mg BD, botulinum toxin), hepatotoxicity (carbamazepine, valproate, rare with others), thrombocytopenia (valproate)

**Mood Stabilizers**:
- **Lithium**: 600-1200 mg daily (serum level 0.6-1.2 mmol/L) - first-line for bipolar disorder, suicide prevention, augmentation (severe depression, rapid cycling), narrow therapeutic index (toxicity if >1.5 mmol/L), dehydration (diarrhea, vomiting, sweating, fever), lithium toxicity (nausea, vomiting, diarrhea, coarse tremor, ataxia, drowsiness, confusion, seizures, arrhythmias, death - requires urgent medical attention, stop lithium, aggressive IV hydration, monitor levels, consider hemodialysis if severe), renal toxicity (nephrogenic diabetes insipidus - polyuria, polydipsia, chronic tubulointerstitial nephritis - worsens with dehydration, NSAIDs, ACE inhibitors, ARBs, diuretics), hypothyroidism (goiter, need to add levothyroxine, especially if long-term, monitor TFTs every 6-12 months), weight gain, tremor (fine, dose-dependent, may respond to dose reduction, beta-blocker - propranolol 10-40 mg TDS), teratogenic (Ebstein's anomaly - tricuspid valve deformity, especially first trimester), safe in breastfeeding, ECG (if risk factors for QT prolongation), avoid in renal impairment (eGFR <30), dehydration, pregnancy (unless risks vs benefits discussion), monitor levels (6-12 hours after loading, twice weekly until stable, then every 3 months), U&E (every 3-6 months), TFTs (every 6-12 months), pregnancy test if women of childbearing age, patient education (toxicity symptoms, dehydration risks, maintain fluids, avoid NSAIDs, ACE inhibitors, ARBs, diuretics, report symptoms early), alternatives (valproate, lamotrigine, atypical antipsychotics)
- **Sodium Valproate** (Depakote): 1000-2000 mg daily in 2-3 divided doses (serum level 50-100 mcg/mL) - rapid onset, effective for mania, migraine prophylaxis, neuropathic pain, teratogenic (neural tube defects - spina bifida, anencephaly, especially first trimester, 5-10% risk, avoid in pregnancy, especially first trimester, use contraception if women of childbearing age, discuss risks, folic acid 5 mg daily if continuing), weight gain, polycystic ovaries (hyperandrogenism, hirsutism, oligomenorrhea/amenorrhea, infertility), thrombocytopenia (dose-dependent, usually mild-moderate, resolves with dose reduction/stop), hepatotoxicity (rare but fatal - especially in children <2, "Reye's-like" syndrome, monitor LFTs, avoid if liver disease, alcohol use), pancreatitis (rare but painful, monitor amylase/lipase if abdominal pain), hair loss (usually reversible, dose-dependent), tremor, nausea, sedation, LFTs (baseline, then every 6 months), FBC (platelets), valproate level, pregnancy test if women of childbearing age, avoid in pregnancy (unless risks vs benefits discussion - severe mania with suicidality, risks to mother and baby, alternatives - lithium, lamotrigine, atypical antipsychotics), contraception (effective hormonal contraceptives interact - increase valproate levels), inform women of childbearing age of risks
- **Lamotrigine** (Lamictal): 25-200 mg daily (slow titration to reduce rash risk: 25 mg daily for 2 weeks, then 50 mg daily for 2 weeks, then increase by 25-50 mg every 1-2 weeks to 100-200 mg daily, if also on valproate - halves rate, if also on carbamazepine/phenytoin/phenobarbital - doubles rate) - maintenance, depression prevention (especially bipolar depression, rapid cycling, mixed episodes), less effective for mania prevention, slow titration (may take months to reach therapeutic dose), Stevens-Johnson syndrome (rare but life-threatening rash, 10% of patients, more common if rapid titration, especially if also on valproate, more common in children, more common in certain ethnic groups [HLA-B*1502 in Han Chinese, SE Asian]), stop immediately if rash occurs, carry rash card (instruct patient to stop lamotrigine immediately and seek urgent medical attention if rash), fever, flu-like symptoms, mouth ulcers, facial swelling, peeling skin, monitor bloods (FBC, LFTs) if rash occurs, alternative if rash (alternative mood stabilizers, antipsychotics), teratogenic (cleft lip/palate, safer than lithium/valproate in pregnancy, discuss risks), safer than valproate/lithium in pregnancy, may cause neural tube defects (less risk than valproate), folic acid 5 mg daily if pregnant, advantages (fewer side effects than lithium/valproate, no renal toxicity, no weight gain, no metabolic effects, no need for blood monitoring, no therapeutic drug monitoring), disadvantages (slow titration, rash risk, less effective for mania, may not prevent mania), use if valproate/lithium not tolerated, not effective, or contraindicated
- **Carbamazepine**: 400-800 mg daily in 2 divided doses (serum level 4-12 mg/L) - first-line in some countries, enzyme inducer (induces CYP3A4, reduces levels of many medications - oral contraceptives, warfarin, antipsychotics, TCAs, lamotrigine, valproate, check drug interactions), less commonly used now, sedation, bone marrow suppression (aplastic anemia, agranulocytosis - rare but life-threatening, monitor FBC weekly for first 3 months, then every 3-6 months), SIADH (hyponatremia - especially elderly), rash (Stevens-Johnson syndrome - HLA-B*1502 in Han Chinese, SE Asian), teratogenic (neural tube defects), less effective for depression, less effective than lithium/valproate for mania, use if lithium/valproate not tolerated or not effective, monitor levels, FBC, sodium, LFTs, pregnancy test if women of childbearing age
- **Oxcarbazepine** (Trileptal): 600-2400 mg daily in 2 divided doses - similar to carbamazepine but safer (fewer drug interactions, less hematotoxicity, less rash), also enzyme inducer but less than carbamazepine, hyponatremia (more common than carbamazepine, especially if high dose, elderly), monitoring similar to carbamazepine

**Anxiolytics**:
- **SSRIs/SNRIs** (first-line): See anxiety section
- **Buspirone**: 15-30 mg daily in 3 divided doses - partial 5-HT1A agonist, non-sedating, no dependence/withdrawal, takes 2-4 weeks to work, less effective than benzodiazepines but safer for long-term use
- **Benzodiazepines** (short-term only, 2-4 weeks maximum): Diazepam 2-10 mg daily, Lorazepam 1-4 mg daily, Clonazepam 0.5-2 mg daily - rapid onset, effective, sedating, risk of dependence, tolerance, withdrawal (rebound anxiety, tremor, seizures), cognitive impairment, falls (elderly), respiratory depression (especially with alcohol), contraindicated in pregnancy, breastfeeding, substance use disorders, caution in elderly, caution if respiratory disease, caution if driving/operating machinery, taper slowly (especially short-acting like alprazolone - risk of withdrawal seizures), used only short-term while waiting for SSRI/SNRI to take effect, or for acute anxiety, or for detoxification from alcohol/benzodiazepines (substitution taper), not first-line for GAD/panic (due to dependence risk), prefer SSRIs/SNRIs or buspirone for long-term
- **Hydroxyzine**: 25-100 mg daily in 3-4 divided doses - antihistamine, sedating, short-term use only, alternative if benzodiazepines contraindicated or not tolerated
- **Pregabalin**: 150-600 mg daily in 3 divided doses - GABA analog, effective for GAD, off-label for anxiety, side effects: dizziness, drowsiness, weight gain, edema, abuse potential (controlled substance)

**Hypnotics** (for insomnia):
- **Non-pharmacological**: Sleep hygiene, CBT-I (stimulus control, sleep restriction, cognitive restructuring, relaxation techniques, sleep scheduling), exercise, avoid caffeine/alcohol/nicotine, regular routine, dark/quiet/cool bedroom, limit screens (blue light) before bed, relaxing bedtime routine, warm bath, reading, meditation, mindfulness
- **Pharmacological** (short-term <4 weeks, plus sleep hygiene):
  - **Z-drugs** (Z-hypnotics): Zopiclone 7.5 mg nightly (max 7.5 mg), Eszopiclone 2-3 mg nightly (Lunesta - longer-acting), Zaleplon 10-20 mg nightly (Sonata - ultra-short-acting, good for sleep onset problems), Zolpidem 5-10 mg nightly (Ambien - short-acting, good for sleep onset problems, available as controlled release for sleep maintenance) - GABA-A receptor agonists (alpha1 subunit), effective for sleep onset, maintenance, reduce sleep latency, improve sleep quality, next-day residual sedation (especially with long-acting), tolerance (loss of effectiveness with long-term use), dependence (with long-term use, withdrawal - rebound insomnia, anxiety, tremor, seizures), memory impairment (anterograde amnesia - especially with zolpidem, zaleplon - especially if taken after only a few hours of sleep, complex sleep-related behaviors [sleep eating, sleep driving, sleep texting, sleep shopping - no memory]), fall risk (elderly), contraindicated in pregnancy, breastfeeding, severe sleep apnea (may worsen respiratory depression), severe liver disease, alcohol, limit to 2-4 weeks maximum, taper slowly to avoid withdrawal, sleep hygiene essential, avoid alcohol, take immediately before bed, avoid rapid onset (especially zolpidem, zaleplon - wait until in bed), ensure 7-8 hours in bed before taking
  - **Melatonin receptor agonists**: Ramelteon 8 mg nightly (Rozerem) - melatonin MT1/MT2 agonist, no dependence, no withdrawal, less effective than Z-drugs, especially for sleep onset problems, especially in elderly, especially with circadian rhythm disorders (delayed sleep phase), safe in pregnancy? (limited data, avoid if possible), minimal side effects (headache, somnolence), advantages over Z-drugs (no dependence, no tolerance, no withdrawal, safe in elderly, minimal next-day sedation, safe in pregnancy? [limited data, avoid if possible])
  - **Sedating antidepressants**: Trazodone 25-100 mg nightly (more effective for insomnia, less effective for depression, off-label but common), Mirtazapine 15-45 mg nightly (more effective for insomnia, especially with anxiety/depression), Amitriptyline 10-50 mg nightly (especially if neuropathic pain, many side effects, avoid in elderly), Doxepin 10-50 mg nightly (especially if anxiety, many side effects, avoid in elderly) - used for insomnia, especially if comorbid depression/anxiety/pain, many side effects (anticholinergic - dry mouth, constipation, urinary retention, blurred vision, cognitive impairment, confusion in elderly, orthostatic hypotension, weight gain, QT prolongation), especially trazodone/mirtazapine (fewer anticholinergic effects)
  - **Melatonin** 1-5 mg nightly - over-the-counter supplement (in US, requires prescription in UK/Europe), effective for circadian rhythm disorders (delayed sleep phase, jet lag, shift work), minimal side effects (headache, somnolence), especially helpful for circadian rhythm disorders (delayed sleep phase - take several hours before desired bedtime, jet lag - take at destination bedtime for several days, shift work - take before daytime sleep), elderly (decreased melatonin production), minimal dependence, no withdrawal, safe in pregnancy (limited data, avoid if possible), minimal side effects, low cost, varies in quality, dose-dependent effects, start low (0.5-1 mg), increase if needed, avoid high doses (>5 mg - may cause grogginess, next-day sedation), take 30-60 minutes before bedtime, timing important for circadian effects
  - **Antihistamines**: Diphenhydramine 25-50 mg nightly, Doxylamine 25 mg nightly - over-the-counter, sedating, anticholinergic effects (dry mouth, constipation, urinary retention, blurred vision, cognitive impairment, confusion in elderly, next-day sedation), tolerance (loss of effectiveness with long-term use), dependence (mild, especially diphenhydramine), short-term use only (<2 weeks), elderly (use caution), use regularly (nightly) rather than PRN to avoid tolerance, not first-line for chronic insomnia due to tolerance, anticholinergic effects
  - **Orexin receptor antagonists** (new): Suvorexant 10-20 mg nightly (Belsomra) - dual orexin receptor antagonist (OX1/2), effective for sleep maintenance, limited data, expensive, next-day sedation (dose-dependent), Lemborexant 5-10 mg nightly (Dayvigo) - orexin OX2 receptor antagonist, more selective than suvorexant, effective for sleep maintenance, next-day sedation (less than suvorexant), limited data, expensive

**PSYCHOTHERAPIES**:
- **CBT** (Cognitive Behavioral Therapy): First-line for depression, anxiety, psychosis, eating disorders, substance use, personality disorders (DBT), ADHD, insomnia (CBT-I), 12-20 sessions, homework, skills training, relapse prevention
- **DBT** (Dialectical Behavior Therapy): For borderline personality disorder, chronic suicidality, self-harm, emotion dysregulation, individual therapy, group skills training, phone coaching, therapist consultation team
- **IPT** (Interpersonal Therapy): For depression, focuses on relationships, role transitions, grief, interpersonal disputes, interpersonal deficits, 12-16 sessions
- **Family Therapy**: For children, adolescents, eating disorders, psychosis, substance use, improves family communication, reduces expressed emotion (criticism, hostility, overinvolvement), relapse prevention
- **Group Therapy**: Depression, anxiety, substance use (AA, NA, SMART Recovery), personality disorders (DBT skills groups), eating disorders, cost-effective, peer support
- **Psychodynamic Therapy**: For personality disorders, chronic depression, trauma, childhood abuse, long-term (months-years), insight-oriented, explores unconscious patterns, transference, countertransference

**THERAPEUTIC RELATIONSHIP**:
- **Empathy**: Understand patient's perspective, validate feelings, avoid judgment
- **Collaboration**: Shared decision-making, work together on goals
- **Boundaries**: Professional boundaries, avoid dual relationships, avoid self-disclosure (except when strategically helpful), avoid gifts (except small tokens), avoid treating family/friends
- **Confidentiality**: Except with informed consent, except risk to self/others, except mandatory reporting (child protection, vulnerable adults, terrorism, fitness to drive, fitness to practice, gunshot wounds, stab wounds)
- **Informed consent**: Explain diagnosis, treatment options, risks/benefits, alternatives, right to refuse treatment, right to second opinion, answer questions

**Sources:** APA Guidelines, Maudsley Prescribing Guidelines, NICE Guidelines
""",
            confidence=0.93,
            metadata={
                "specialty": "Psychiatry",
                "focus": "General Psychiatry",
                "sources": ["APA", "Maudsley Prescribing Guidelines", "NICE"]
            }
        )


def create_psychiatry_domain():
    """
    Factory function to create psychiatry domain instance.

    Returns:
        PsychiatryDomain: Configured psychiatry specialty domain
    """
    return PsychiatryDomain()
