"""
Geriatric Medicine Domain for GPDISC

Comprehensive geriatric assessment and management covering:
- Multimorbidity and polypharmacy
- Falls prevention and assessment
- Cognitive impairment and dementia
- Delirium prevention and management
- Urinary incontinence
- Pressure ulcers and skin care
- Nutrition and hydration in older adults
- Elder abuse and safeguarding
- End-of-life care and advance planning
- Frailty assessment
- Syncope and orthostatic hypotension
- Sleep disorders in older adults
- Pain management in geriatrics
- Rehabilitation and functional recovery

Evidence-based guidelines: NICE, BGS, AGS, Geriatric Medicine resources
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Optional, Dict, List, Any
import re


class GeriatricMedicineDomain(BaseDomainModule):
    """
    Geriatric Medicine specialty domain for comprehensive older adult care.

    Covers comprehensive geriatric assessment, frailty, multimorbidity,
    cognitive disorders, falls, incontinence, and end-of-life care.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="geriatric_medicine",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive geriatric assessment and management of older adults with multimorbidity, frailty, cognitive impairment, and complex medical needs",
            keywords=[
                # Core geriatric concepts
                "elderly", "older adult", "geriatric", "aged", "palliative", "hospice",
                "frailty", "multimorbidity", "polypharmacy", "comprehensive geriatric assessment",

                # Cognitive/Neurologic
                "dementia", "alzheimer", "memory loss", "confusion", "delirium", "cognitive impairment",
                "behavioral and psychological symptoms", "bpsd", "capacity", "mental capacity",

                # Falls/Mobility
                "falls", "fall risk", "balance", "gait", "mobility", "syncope", "collapse",
                "orthostatic", "postural hypotension", "dizziness", "vertigo",

                # Continence
                "incontinence", "urinary incontinence", "frequency", "urgency", "nocturia",
                "catheter", "constipation", "bowel",

                # Skin/Pressure
                "pressure ulcer", "bedsore", "pressure sore", "skin tear", "moisture lesion",
                "skin care", "wound",

                # Nutrition
                "malnutrition", "weight loss", "anorexia", "dysphagia", "dehydration",
                "nutrition", "feeding", "sarcopenia",

                # Medication
                "polypharmacy", "medication review", "deprescribing", "beers criteria",
                "inappropriate prescribing", "adverse drug reaction", "stop-start",

                # Safeguarding
                "elder abuse", "safeguarding", "neglect", "financial abuse", "carer",
                "caregiver", "respite",

                # End of Life
                "end of life", "palliative", "advance directive", "living will",
                "dnar", "resuscitation", "dnacpr", "advance care planning",

                # Functional
                "activities of daily living", "adl", "iadl", "barthel", "rehabilitation",
                "discharge", "care home", "nursing home", "residential care"
            ],
            capabilities=[
                "comprehensive_geriatric_assessment", "frailty_screening", "multimorbidity_management",
                "polypharmacy_review", "dementia_diagnosis", "delirium_prevention",
                "falls_assessment", "incontinence_management", "pressure_ulcer_prevention",
                "nutritional_assessment", "end_of_life_care", "advance_care_planning",
                "elder_abuse_detection", "capacity_assessment", "rehabilitation_planning",
                "syncope_evaluation", "pain_management", "sleep_disorder_management"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """
        Process geriatric medicine queries with comprehensive assessment focus.
        """
        query_lower = query.lower()

        # EMERGENCY: Delirium with life-threatening cause
        if any(term in query_lower for term in ["delirium", "acute confusion", "sudden confusion"]):
            return self._handle_delirium_query(query, context)

        # EMERGENCY: Suspected elder abuse with immediate danger
        if any(term in query_lower for term in ["elder abuse", "abuse", "neglect", "safeguarding"]) and \
           any(term in query_lower for term in ["urgent", "emergency", "immediate danger", "physical harm"]):
            return self._handle_elder_abuse_emergency(query, context)

        # Cognitive impairment and dementia
        if any(term in query_lower for term in ["dementia", "alzheimer", "memory loss", "cognitive decline", "confusion"]):
            return self._handle_dementia_query(query, context)

        # Falls and syncope
        if any(term in query_lower for term in ["falls", "fallen", "fall risk", "syncope", "collapse", "blackout"]):
            return self._handle_falls_query(query, context)

        # Polypharmacy and medication review
        if any(term in query_lower for term in ["polypharmacy", "multiple medications", "medication review", "deprescribing", "drug interactions"]):
            return self._handle_polypharmacy_query(query, context)

        # Urinary incontinence
        if any(term in query_lower for term in ["incontinence", "leakage", "bladder", "catheter", "urgency", "frequency"]):
            return self._handle_incontinence_query(query, context)

        # Pressure ulcers
        if any(term in query_lower for term in ["pressure ulcer", "bedsore", "pressure sore", "skin breakdown"]):
            return self._handle_pressure_ulcer_query(query, context)

        # Malnutrition and nutrition
        if any(term in query_lower for term in ["malnutrition", "weight loss", "nutrition", "dysphagia", "feeding"]):
            return self._handle_nutrition_query(query, context)

        # End of life and palliative care
        if any(term in query_lower for term in ["end of life", "palliative", "hospice", "advance directive", "dnacpr", "resuscitation"]):
            return self._handle_palliative_query(query, context)

        # Frailty assessment
        if any(term in query_lower for term in ["frailty", "frail", "rockwood", "clinical frailty scale"]):
            return self._handle_frailty_query(query, context)

        # Elder abuse and safeguarding (non-emergency)
        if any(term in query_lower for term in ["elder abuse", "safeguarding", "vulnerable", "neglect", "financial abuse"]):
            return self._handle_elder_abuse_query(query, context)

        # Constipation and bowel care
        if any(term in query_lower for term in ["constipation", "bowel", "faecal impaction", "encopresis"]):
            return self._handle_bowel_query(query, context)

        # Sleep disorders
        if any(term in query_lower for term in ["insomnia", "sleep problem", "sleep disturbance", "restless legs"]):
            return self._handle_sleep_query(query, context)

        # Pain management
        if any(term in query_lower for term in ["pain", "chronic pain", "analgesia", "opioid"]):
            return self._handle_pain_query(query, context)

        # Capacity assessment
        if any(term in query_lower for term in ["capacity", "mental capacity", "best interests", "power of attorney"]):
            return self._handle_capacity_query(query, context)

        # Discharge planning and rehabilitation
        if any(term in query_lower for term in ["discharge", "rehabilitation", "care home", "nursing home", "placement"]):
            return self._handle_rehabilitation_query(query, context)

        # General geriatric assessment
        return self._handle_general_geriatric_query(query, context)

    def _handle_delirium_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle delirium queries - MEDICAL EMERGENCY requiring urgent assessment."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**DELIRIUM - MEDICAL EMERGENCY**

Delirium (acute confusional state) is a medical emergency requiring URGENT assessment for underlying cause.

**IMMEDIATE ACTIONS:**
1. **ABCDE assessment** - treat life-threatening causes first
2. **Urgent investigations**: CBC, electrolytes, calcium, glucose, CRP, TSH, urinalysis, CXR, blood cultures if febrile
3. **Consider CT head** if: focal neurology, head trauma, fall, sudden onset, anticoagulation

**COMMON CAUSES (PINCH ME):**
- **P**ain, Psychoactive medications, Polypharmacy
- **I**nfection (UTI, pneumonia, sepsis, cellulitis)
- **N**utrition (dehydration, electrolyte abnormalities, thiamine, B12)
- **C**onstipation, Urinary retention, **C**atheter-related
- **H**ypoxia, Heart failure, Hypotension, Hypertension
- **M**edication (new, changed, stopped), Metabolic, Environment
- **E**EG (epilepsy, non-convulsive status, post-ictal), Elimination

**MANAGEMENT:**
- **Treat underlying cause** - this is definitive treatment
- **Supportive care**: reorientation, calm environment, adequate lighting, mobility, nutrition, hydration
- **Avoid physical restraints** - increase distress and injury risk
- **Consider antipsychotics ONLY if**: severe distress, risk of harm to self/others, distressing hallucinations
  - Haloperidol 0.5-1mg PO/IM/IV PRN (start LOW, go slow)
  - Monitor for QT prolongation, EPS, NMS
  - Review regularly and discontinue as soon as possible

**PREVENTION IS CRITICAL:**
- Regular orientation, mobility, hydration, nutrition, sleep hygiene, pain control, minimize medications
- Consider delirium risk prediction models

**PROGNOSIS:**
- 30% mortality at 6 months
- May not fully resolve even after treating cause
- Recurrence risk is high

**SOURCES:** NICE NG103, British Geriatrics Society delirium guidelines
""",
            confidence=0.96,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Delirium - Medical Emergency",
                "urgency": "urgent",
                "sources": ["NICE NG103", "BGS Delirium Guidelines"]
            }
        )

    def _handle_dementia_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle dementia and cognitive impairment queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**DEMENTIA ASSESSMENT AND MANAGEMENT**

**DIAGNOSTIC CRITERIA (DSM-5):**
- Significant cognitive decline **interfering with independence**
- Involving **≥1 domains**: complex attention, executive function, learning/memory, language, perceptual-motor, social cognition
- **Not** occurring exclusively during delirium
- **Not** better explained by other mental disorder

**REVERSIBLE CAUSES TO EXCLUDE:**
- Depression ("pseudodementia")
- Vitamin B12/folate deficiency
- Hypothyroidism (TSH)
- Normal pressure hydrocephalus (wet, wobbly, wacky)
- Subdural hematoma
- Medication side effects (anticholinergics, benzodiazepines, opioids)
- Syphilis, HIV (in at-risk individuals)

**COGNITIVE ASSESSMENT TOOLS:**
- **MMSE** (0-30): <24 suggests impairment, but education/mood affect
- **MoCA** (0-30): better for mild cognitive impairment (MCI), <26 suggests impairment
- **GPCOG** (GP cognitive): brief, informant component included
- **6CIT**: quick primary care tool

**INVESTIGATIONS:**
- **Bloods**: FBC, U&E, LFT, calcium, glucose, TSH, B12, folate, syphilis serology (if indicated)
- **Neuroimaging**: MRI preferred (or CT) - assess vascular disease, atrophy patterns, NPH, space-occupying lesions
- **Consider**: EEG, lumbar puncture, genetic testing if atypical or young onset

**DEMENTIA SUBTYPES:**
1. **Alzheimer's Disease** (70%): Insidious onset, memory > executive, hippocampal atrophy on MRI
2. **Vascular Dementia** (15-20%): Stepwise decline, vascular risk factors, focal signs, extensive white matter disease
3. **Lewy Body Dementia**: Fluctuating cognition, visual hallucinations, parkinsonism, neuroleptic sensitivity
4. **Frontotemporal Dementia**: Early behavior/personality change, language deficits, relative memory preservation
5. **Mixed Dementia**: Alzheimer's + vascular features

**PHARMACOLOGICAL MANAGEMENT:**
- **AChE inhibitors** (mild-moderate Alzheimer's): Donepezil, Rivastigmine, Galantamine
  - modest cognitive/functional benefit, may delay institutionalization
  - Monitor for GI side effects, bradycardia, syncope
- **Memantine** (moderate-severe): NMDA antagonist, can be added to AChEI or used alone
- **NO evidence for prevention**: AChEIs do NOT prevent dementia in MCI

**NON-PHARMACOLOGICAL MANAGEMENT:**
- Cognitive stimulation therapy (CST)
- Physical activity, social engagement
- Safety: driving assessment, medication management, finances, home safety
- Advance care planning **early**

**BEHAVIORAL AND PSYCHOLOGICAL SYMPTOMS (BPSD):**
- First assess for: pain, infection, constipation, delirium, environmental triggers
- Non-pharmacological measures FIRST
- Antipsychotics only if severe distress/risk, at lowest dose, shortest duration
  - Risperidone 0.25-0.5mg BD is first-line (NICE)
  - Increased stroke risk in elderly with dementia - **warn families**

**DRIVING:**
- Legal obligation to notify licensing authority
- Formal assessment may be required

**SOURCES:** NICE NG97, DSM-5, Alzheimer's Association, BGS
""",
            confidence=0.94,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Dementia and Cognitive Impairment",
                "sources": ["NICE NG97", "DSM-5", "BGS"]
            }
        )

    def _handle_falls_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle falls and syncope queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**FALLS AND SYNCOPE ASSESSMENT**

**DEFINITIONS:**
- **Fall**: Involuntary coming to rest on ground/floor, not due to overwhelming force
- **Syncope**: Transient loss of consciousness (TLoC) due to cerebral hypoperfusion, with rapid recovery
- **Presyncope**: Feeling of imminent syncope without LOC

**IMMEDIATE ASSESSMENT AFTER FALL:**
1. **ABCDE** - rule out injury
2. **Timeline**: What happened? Prodrome? LOC? Injury? Ability to get up?
3. **Red flags**: Long lie (>1 hour), head injury, neck pain, anticoagulation, amnesia for event

**FALLS RISK ASSESSMENT:**
- **History**: Previous falls, fear of falling, gait/balance problems, medications, visual impairment, home hazards, cognitive impairment, continence issues, foot problems, postural hypotension
- **Examination**: Orthostatic vitals (lying-standing, wait 3 min), cognitive screen, visual acuity, gait assessment (TUG, "up and go"), balance tests, footwear check, home hazards assessment
- **Timed Up and Go (TUG)**: <10s normal, 10-20s mobility impaired, >20s high falls risk, >30s dependency needs

**CAUSES OF FALLS (Multifactorial in >75%):**
- **Musculoskeletal**: Muscle weakness, arthritis, balance problems, gait abnormalities
- **Neurological**: Stroke, Parkinson's, neuropathy, normal pressure hydrocephalus
- **Cardiovascular**: Orthostatic hypotension, arrhythmias, vasovagal syncope, carotid sinus hypersensitivity, aortic stenosis
- **Medications**: Sedatives, antidepressants, antipsychotics, diuretics, antihypertensives, polypharmacy (>4 meds)
- **Environmental**: Poor lighting, loose rugs, uneven surfaces, inadequate footwear
- **Acute illness**: Infection, dehydration, delirium, pain

**ORTHOSTATIC HYPOTENSION DEFINITION:**
- Drop in SBP ≥20 mmHg or DBP ≥10 mmHg within 3 minutes of standing
- **Symptoms**: Dizziness, lightheadedness, presyncope, syncope, weakness, visual disturbance
- **Causes**: Medications (diuretics, antihypertensives, alpha-blockers, TCAs, levodopa), dehydration, diabetes (autonomic neuropathy), parkinsonism, amyloidosis, bed rest

**MANAGEMENT:**
- **Multifactorial intervention** - address ALL identified risk factors
- **Strength and balance training**: Physiotherapy referral, Tai Chi, home exercise program
- **Medication review**: Reduce/stop fall-risk-increasing drugs (FRIDs)
- **Home hazards assessment**: Remove rugs, improve lighting, install grab rails, bed alarms if needed
- **Vision**: Regular optometry review, cataract referral if indicated
- **Footwear**: Properly fitting, supportive shoes with low heels and good grip
- **Treat orthostatic hypotension**:
  - Non-pharmacological: rise slowly, sit before standing, increase fluid/salt, compression stockings, elevate head of bed
  - Pharmacological: fludrocortisone, midodrine (specialist initiation)
- **Hip protectors**: May reduce fracture risk in nursing home residents

**SYNCOPE INVESTIGATION:**
- **ECG**: Arrhythmia, conduction disease, QT prolongation
- **Holter/event monitor** if recurrent unexplained syncope
- **Echocardiogram** if murmur, heart failure, or suspected valvular disease
- **Tilt table test** if suspected vasovagal or orthostatic syncope
- **Carotid sinus massage** (with ECG monitoring) if >50yo, syncope with head turning

**REFERRAL CRITERIA:**
- Falls clinic: Recurrent falls (>2 in 12 months), single fall with injury, or unexplained single fall in high-risk person
- Cardiology: Suspected cardiac syncope, abnormal ECG, structural heart disease
- Neurology: Suspected NPH, Parkinson's, gait abnormality

**FRACTURE PREVENTION:**
- **Osteoporosis assessment**: DXA scan, FRAX calculation
- **Calcium 1000-1200mg + Vitamin D 800-1000 IU daily**
- **Bisphosphonates**: Alendronate first-line (if eGFR >35), consider IV zoledronate if contraindications to oral
- **Denosumab**: alternative if renal impairment, contraindication to bisphosphonates

**SOURCES:** NICE NG161, AGS Falls Prevention Guidelines, BGS
""",
            confidence=0.93,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Falls, Syncope, and Orthostatic Hypotension",
                "sources": ["NICE NG161", "AGS Falls Prevention", "BGS"]
            }
        )

    def _handle_polypharmacy_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle polypharmacy and medication review queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**POLYPHARMACY AND DEPRESCRIBING**

**DEFINITIONS:**
- **Polypharmacy**: Multiple medications (commonly ≥5, though sometimes ≥10 is used)
- **Appropriate polypharmacy**: Prescribing for multiple conditions evidence-based and optimized
- **Inappropriate polypharmacy**: Multiple medications where harm outweighs benefit

**RISKS OF POLYPHARMACY IN OLDER ADULTS:**
- Adverse drug reactions (ADRs) - incidence increases linearly with number of medications
- Drug-drug interactions
- Prescribing cascades (treating side effects of one drug with another)
- Medication burden and non-adherence
- Falls, cognitive impairment, delirium, constipation, urinary retention, QT prolongation

**HIGH-RISK MEDICATIONS IN OLDER ADULTS (BEERS CRITERIA):**

**Anticholinergics** (cumulative anticholinergic burden increases dementia risk):
- First-generation antihistamines: diphenhydramine, hydroxyzine, promethazine
- Antispasmodics: oxybutynin, tolterodine (consider mirabegron instead)
- Antidepressants: amitriptyline, nortriptyline, imipramine, paroxetine
- Antipsychotics: all have anticholinergic effects
- Antiemetics: prochlorperazine, promethazine
- Muscle relaxants: cyclobenzaprine, orphenadrine
- **Use**: Anticholinergic burden scale (ACB, ADS, ARS) to assess cumulative risk

**Benzodiazepines and Z-drugs:**
- Increased fall risk, cognitive impairment, delirium, respiratory depression, dependence
- Avoid for insomnia, anxiety, agitation - safer alternatives exist
- If absolutely necessary: shortest duration, lowest dose, avoid long-acting agents (diazepam, flurazepam)

**Antipsychotics:**
- Increased stroke (2x) and mortality (1.6x) in dementia patients
- Minimize use for BPSD, avoid first-line for anxiety, insomnia, agitation
- Extrapyramidal side effects, tardive dyskinesia, metabolic syndrome, QT prolongation

**NSAIDs:**
- Increased GI bleed (2-4x), AKI, heart failure exacerbation, hypertension
- Avoid chronic use, consider topical NSAIDs for localized pain, use PPI if unavoidable

**Antihypertensives (excessive treatment):**
- Orthostatic hypotension, falls, syncope, acute kidney injury
- **Deprescribe if**: SBP <140 mmHg on multiple agents, orthostatic symptoms, falls

**Digoxin:**
- Narrow therapeutic index, toxicity confusion with other conditions
- **Deprescribe**: Not in atrial fibrillation or heart failure, or if <0.125 mg daily

**Sulfonylureas** (especially long-acting):
- Hypoglycemia risk, falls, cognitive impairment
- **Avoid**: Glibenclamide (glyburide), chlorpropamide
- **Prefer**: Shorter-acting agents or consider deprescribing if life expectancy limited

**PROACTIVE MEDICATION REVIEW:**
1. **List all medications**: prescription, OTC, herbal, supplements
2. **Assess indications**: What is each medication for? Is indication still present?
3. **Assess effectiveness**: Is it working? Can you tell?
4. **Assess safety**: Any ADRs, interactions, cumulative burdens (ACB, ADR risk score)
5. **Assess adherence**: Practical regimen, patient preferences
6. **STOP/START criteria**: Apply evidence-based tools
7. **Deprescribing plan**: Prioritize, taper slowly, monitor

**DEPRESCRIBING APPROACH:**
- Identify potentially inappropriate medications
- Discuss with patient/carer: benefits vs harms, goals of care, preferences
- **Prioritize**: High-risk medications first (anticholinergics, benzodiazepines, antipsychotics)
- **Taper slowly**: Especially benzodiazepines, antidepressants, antipsychotics (risk of withdrawal)
- **Monitor**: Withdrawal, rebound symptoms, disease control
- **Document**: Rationale, plan, monitoring

**STOPPING RULES (EXAMPLES):**
- **Benzodiazepines**: Reduce by 25-50% every 1-2 weeks, monitor for withdrawal (anxiety, insomnia, agitation, tremor, seizures)
- **Anticholinergics**: Can stop abruptly unless treating significant conditions (e.g., overactive bladder - taper)
- **Antipsychotics for BPSD**: Taper by 50% every 2-4 weeks, monitor for BPSD recurrence
- **Antihypertensives**: One drug at a time, monitor BP, symptoms

**USEFUL TOOLS:**
- **Beers Criteria** (AGS): Potentially inappropriate medications in older adults
- **STOPP/START** (Screening Tool of Older Persons' Prescriptions): Explicit criteria for inappropriate prescribing and prescribing omissions
- **MAI** (Medication Appropriateness Index): Comprehensive assessment
- **ACB Scale** (Anticholinergic Cognitive Burden): Cumulative anticholinergic load

**SOURCES:** Beers Criteria 2023, STOPP/START v3, NICE NG5, BGS
""",
            confidence=0.95,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Polypharmacy and Deprescribing",
                "sources": ["Beers Criteria 2023", "STOPP/START v3", "NICE NG5", "BGS"]
            }
        )

    def _handle_incontinence_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle urinary incontinence queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**URINARY INCONTINENCE IN OLDER ADULTS**

**PREVALENCE:**
- Women: 30-40% (community), 50-70% (care homes)
- Men: 10-20% (community), 60-80% (care homes)
- Under-recognized, under-treated, significant impact on QoL

**URGENT ASSESSMENT (RED FLAGS):**
- Painless hematuria (bladder cancer until proven otherwise)
- Recurrent UTIs with hematuria
- Acute urinary retention (catheterize, urgent urology referral)
- Cauda equina signs (saddle anesthesia, urinary/fecal incontinence, bilateral leg weakness) - **EMERGENCY**
- Suspected spinal cord compression

**TYPES OF INCONTINENCE:**

**1. STRESS INCONTINENCE (SUI)**
- **Mechanism**: Incompetent urethral sphincter, increased intra-abdominal pressure
- **Symptoms**: Leakage with cough, sneeze, exercise, position change
- **Risk factors**: Parity, vaginal delivery, menopause, obesity, smoking, chronic cough
- **Management**: Weight loss if overweight, pelvic floor muscle training (PFMT) - 3+ months, vaginal estrogen (postmenopausal), duloxetine (second-line), consider surgery if conservative fails (MUS, mid-urethral sling, colposuspension)

**2. URGE INCONTINENCE (Detrusor Overactivity)**
- **Mechanism**: Detrusor muscle overactivity (idiopathic or neurogenic)
- **Symptoms**: Sudden, intense urge, frequency, nocturia, leakage before reaching toilet
- **Management**: Bladder training, lifestyle modifications (caffeine, fluid, weight), anticholinergics (oxybutynin, tolterodine, darifenacin, solifenacin) OR mirabegron (beta-3 agonist) - consider anticholinergic burden
- **Avoid** in significant cognitive impairment, delirium risk

**3. MIXED INCONTINENCE**
- Combination of stress and urge symptoms
- Treat predominant component first

**4. OVERFLOW INCONTINENCE**
- **Mechanism**: Bladder outlet obstruction or underactive detrusor
- **Symptoms**: Frequent small voids, weak stream, hesitancy, sensation of incomplete emptying, palpable bladder
- **Causes**: Prostate enlargement (BPH), anticholinergics, opioids, diabetes (autonomic neuropathy), spinal cord injury
- **Management**: Catheterize if retention, treat underlying cause, alpha-blockers for prostatic obstruction, minimize anticholinergic burden

**5. FUNCTIONAL INCONTINENCE**
- **Mechanism**: Mobility or cognitive impairment prevents timely toileting
- **Symptoms**: No bladder dysfunction, but unable to reach toilet
- **Management**: Mobility aids, toileting assistance, prompted voiding, clothing adaptations, environmental modifications (grab rails, raised toilet seat)

**ASSESSMENT:**
- **History**: Onset, triggers, frequency, volume, nocturia, color, hematuria, pain, medications (especially anticholinergics, diuretics, alpha-blockers), previous pelvic surgery/radiotherapy, neurological symptoms
- **Physical**: Abdominal (distended bladder?), genital exam (atrophy?), prostate (if male), neurology (sacral reflexes, anal tone, perineal sensation), mobility/cognition
- **Investigations**: Urinalysis (infection, hematuria, glucose), post-void residual (bladder scan), consider urodynamics if surgical intervention considered, cystoscopy if hematuria

**NOCTURIA:**
- **Definition**: ≥2 voids per night disrupting sleep
- **Causes**: Polyuria (diabetes insipidus/mellitus, diuretics - take morning), nocturnal polyuria (CV disease, sleep apnea, peripheral edema), reduced bladder capacity, sleep disturbance (insomnia, BPH)
- **Management**: Restrict evening fluids, elevate legs during day (peripheral edema), treat BPH, limit evening caffeine/alcohol, desmopressin (cautiously - hyponatremia risk in elderly)

**URINARY CATHETER CONSIDERATIONS:**
- **Indications**: Acute urinary retention, accurate fluid monitoring in critically ill, perioperative for selected procedures, sacral/perineal pressure ulcers requiring healing, terminal care for comfort
- **Contraindications** (long-term): Convenience, incontinence without retention
- **Alternatives**: Condom catheters (men), absorbent pads, prompted voiding programs, intermittent catheterization
- **Complications**: CAUTI (most common nosocomial infection), trauma, hematuria, blockage, encrustation, bladder stones

**SOURCES:** NICE NG123, EAU Guidelines, BGS
""",
            confidence=0.94,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Urinary Incontinence",
                "sources": ["NICE NG123", "EAU Guidelines", "BGS"]
            }
        )

    def _handle_pressure_ulcer_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pressure ulcer queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**PRESSURE ULCER PREVENTION AND MANAGEMENT**

**DEFINITION:**
Localized injury to skin and/or underlying tissue, usually over bony prominence, due to pressure/pressure with shear.

**RISK FACTORS:**
- Immobility, reduced mobility, spinal cord injury
- Sensory impairment (reduced pain perception)
- Poor nutrition, malnutrition, dehydration, low albumin
- Incontinence (moisture, maceration)
- Advanced age, frailty
- Poor perfusion (PVD, heart failure, hypotension)
- Previous pressure ulcers
- Medical devices (catheters, oxygen tubing, masks)

**PRESSURE ULCER CLASSIFICATION (NPUAP-EPUAP):**

**Stage 1: Non-blanchable Erythema**
- Intact skin with non-blanchable redness
- May appear differently in darker skin (discoloration, warmth, hardness)
- **Action**: Relieve pressure, protect skin, monitor closely

**Stage 2: Partial-thickness Skin Loss**
- Shallow open ulcer with red-pink wound bed
- May appear as intact or ruptured serum-filled blister
- **Action**: Clean with saline, protect with dressing, relieve pressure

**Stage 3: Full-thickness Skin Loss**
- Full-thickness tissue loss, subcutaneous fat visible
- May include undermining/tunneling
- **Action**: Specialist wound care, debridement if necrotic, appropriate dressing

**Stage 4: Full-thickness Tissue Loss**
- Full-thickness skin and tissue loss, muscle, bone, tendon exposed
- High infection risk
- **Action**: Urgent specialist referral, surgical debridement, antibiotics if infected

**Unstageable: Obscured Full-thickness Skin Loss**
- Covered by slough (yellow, tan, gray, green) or eschar (tan, brown, black)
- Cannot assess depth until debrided
- **Action**: Debride, reassess stage

**Deep Tissue Pressure Injury (DTPI)**
- Persistent non-blanchable deep red, maroon, purple discoloration
- May be preceded by blood-filled blister
- Results from deep tissue injury (shear, ischemia)
- **Action**: Immediate pressure relief, monitor for rapid deterioration

**MEDICAL DEVICE-RELATED PRESSURE INJURY**
- Under or around medical device (catheter, mask, tubing)
- Follows same staging system

**PREVENTION STRATEGIES:**
- **Risk assessment on admission** and regularly thereafter (Braden, Waterlow scales)
- **Skin inspection**: Daily (especially bony prominences - sacrum, heels, hips, elbows)
- **Pressure relief**:
  - Repositioning every 2 hours (bedridden), every 15-30 minutes (chair-bound)
  - Use pressure-redistributing surfaces (mattress, cushion)
  - Offload heels (float heels, pillows under calves NOT heels)
  - Avoid positioning directly on trochanter/hips (30° lateral tilt preferred)
  - Avoid massage over bony prominences (increases tissue damage)
- **Skin care**:
  - Keep clean and dry
  - Use pH-balanced cleansers
  - Apply moisturizer to dry skin (avoid bony prominences if ulcer present)
  - Protect high-risk areas (barrier creams, dressings)
  - Minimize skin exposure to moisture/incontinence
- **Nutrition**:
  - Adequate protein (1.2-1.5 g/kg/day if ulcer present)
  - Adequate calories, hydration
  - Consider nutritional supplements (high-protein, high-calorie)
  - Address micronutrient deficiencies (zinc, vitamin C)
- **Minimize shear and friction**: Lift, don't drag; use slide sheets; keep bed head ≤30° unless contraindicated

**MANAGEMENT:**
- **Relieve pressure**: Most important intervention!
- **Debride necrotic tissue**: Autolytic, enzymatic, surgical, mechanical (whirlpool)
- **Infection control**:
  - Clean with saline or water (avoid antiseptics - cytotoxic to granulation tissue)
  - Systemic antibiotics ONLY for cellulitis, sepsis, osteomyelitis (not for colonized wounds)
  - Topical antibiotics generally NOT recommended
- **Dressings**: Maintain moist wound environment, protect peri-ulcer skin, manage exudate
  - Hydrocolloids, foams, alginates, hydrogels, antimicrobial (silver, iodine) if infected
  - Choose based on ulcer depth, exudate, condition
- **Negative Pressure Wound Therapy (NPWT)**: For stage 3/4 ulcers, accelerates healing
- **Surgical intervention**: Debridement, flap closure for extensive, non-healing ulcers

**COMPLICATIONS:**
- Infection (cellulitis, osteomyelitis, sepsis)
- Pain
- Prolonged hospitalization
- Reduced mobility
- Septicemia
- Death (rare, but risk increases with stage)

**SOURCES:** NICE NG179, NPUAP-EPUAP Pressure Injury Guidelines, BGS
""",
            confidence=0.95,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Pressure Ulcer Prevention and Management",
                "sources": ["NICE NG179", "NPUAP-EPUAP Guidelines", "BGS"]
            }
        )

    def _handle_nutrition_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle nutrition and malnutrition queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**NUTRITION IN OLDER ADULTS**

**MALNUTRITION PREVALENCE:**
- Community: 10-15%
- Hospitalized: 30-50%
- Care homes: 20-60%

**RISK FACTORS FOR MALNUTRITION:**
- Chronic diseases (cancer, COPD, CHF, CKD)
- Cognitive impairment (forget to eat, inability to prepare food)
- Depression, loneliness, bereavement
- Poor dentition, ill-fitting dentures, dysphagia
- Reduced appetite, early satiety, taste changes
- Medications (anorexia, dry mouth, taste changes)
- Limited mobility, inability to shop/cook
- Poverty, social isolation
- Therapeutic diets (low salt, diabetic, dysphagia) - often unnecessarily restrictive
- Alcohol misuse

**NUTRITION SCREENING TOOLS:**
- **MNA** (Mini Nutritional Assessment): Full version (18 questions) or Short Form (MNA-SF, 6 questions)
- **MUST** (Malnutrition Universal Screening Tool): BMI, weight loss, acute disease effect
- Screen on admission and regularly during hospitalization/care

**DYSPHAGIA ASSESSMENT:**
- **History**: Coughing/choking during meals, wet voice, recurrent chest infections, weight loss, prolonged mealtimes, food avoidance, residue in mouth after swallowing
- **Bedside swallow assessment**: Water test with different consistencies (observe for coughing, voice change, throat clearing)
- **Instrumental**: Videofluoroscopy (modified barium swallow), fiberoptic endoscopic evaluation of swallowing (FEES)
- **Silent aspiration**: No cough despite penetration into airway (common after stroke, dementia)

**DYSPHAGIA MANAGEMENT:**
- **Postural adjustments**: Chin tuck, head rotation (if unilateral weakness), supraglottic swallow
- **Diet modification**: Texture modification (pureed, minced, soft, thickened liquids)
- **Compensatory strategies**: Small frequent meals, adequate time, rest before meals, upright positioning (remain upright 30 min post-meal)
- **Oral care**: Before and after meals (reduce aspiration pneumonia risk)
- **Rehabilitation**: Swallowing exercises, thermal stimulation

**FEEDING TUBES:**
- **Nasogastric (NG)**: Short-term (<4 weeks), risk of tube displacement, aspiration, sinusitis, esophageal injury
- **Percutaneous Endoscopic Gastrostomy (PEG)**: Long-term (>4 weeks), more comfortable, but still carries risks
- **INDICATIONS**: Acute stroke with dysphagia (temporary), head/neck cancer, neurological disease (ALS, MS)
- **NOT for**: Advanced dementia (does NOT prevent aspiration pneumonia, does NOT prolong survival, does NOT improve comfort, increases agitation, requires restraints)
- **Ethical considerations**: Goals of care, quality of life, advance directives

**VITAMIN DEFICIENCIES IN OLDER ADULTS:**
- **Vitamin D**: Very common (insufficiency up to 80% in some populations)
  - Consequences: Osteomalacia, osteoporosis, falls, fractures, muscle weakness
  - Supplementation: 800-1000 IU daily for all older adults, 2000-4000 IU if deficient
- **Vitamin B12**: Deficiency 10-20% (atrophic gastritis, PPIs, metformin, malabsorption)
  - Consequences: Megaloblastic anemia, subacute combined degeneration, neuropathy, cognitive impairment
  - Treatment: Oral cyanocobalamin 1000 mcg daily (or IM if malabsorption)
- **Folate**: Deficiency less common, but assess concurrently with B12

**NUTRITION INTERVENTIONS:**
- **Food fortification**: Add protein, calories to regular foods (powdered milk, cheese, oils, butter)
- **Oral nutritional supplements** (ONS): High-protein, high-calorie drinks (2 kcal/mL) between meals
- **Smaller, more frequent meals**: 6-8 small meals vs 3 large
- **Favorite foods**: Respect preferences, encourage social meals
- **Address barriers**: Denture review, dysphagia management, depression treatment, social support (Meals on Wheels, lunch clubs)
- **Limit restrictions**: Relax therapeutic diets if quality of life paramount

**DEHYDRATION:**
- **Causes**: Reduced thirst sensation (aging), mobility limitations, fear of incontinence, medications (diuretics), cognitive impairment, fever, diarrhea
- **Symptoms**: Dry mouth, reduced skin turgor (less reliable), oliguria, concentrated urine, confusion, constipation, hypotension, tachycardia
- **Consequences**: AKI, constipation, confusion, falls, hypotension, hospitalization
- **Prevention**: Encourage fluids (1.5-2 L/day unless contraindicated), preferred beverages available, accessible drinks, address incontinence (toileting assistance, pads), monitor fluid balance

**OBESITY IN OLDER ADULTS:**
- **"Obesity paradox"**: Mild obesity (BMI 27-30) may be protective in elderly (mortality)
- **Weight loss** in older adults leads to muscle loss (sarcopenia), frailty
- **Focus**: Physical activity, strength training, maintaining muscle mass rather than weight loss alone

**SARCOPENIA:**
- Age-related loss of muscle mass, strength, function
- **Prevention**: Adequate protein (1.0-1.2 g/kg/day, up to 1.5 g/kg if active/ill), resistance exercise, vitamin D
- **Treatment**: Progressive resistance training, protein supplementation, vitamin D if deficient

**SOURCES:** NICE NG184, ESPEN Guidelines on Enteral Nutrition, BGS
""",
            confidence=0.94,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Nutrition, Malnutrition, and Dysphagia",
                "sources": ["NICE NG184", "ESPEN Guidelines", "BGS"]
            }
        )

    def _handle_frailty_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle frailty assessment queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**FRAILTY ASSESSMENT AND MANAGEMENT**

**DEFINITION:**
Frailty is a clinically recognizable state of increased vulnerability resulting from aging-associated decline in reserve and function across multiple physiologic systems such that the ability to cope with everyday or acute stressors is compromised.

**FRAILTY PHENOTYPE (FRIED CRITERIA):**
Diagnose frailty if ≥3 of:
1. **Unintentional weight loss** (≥10 lbs in past year)
2. **Exhaustion** (self-reported)
3. **Low physical activity**
4. **Slow walking speed** (adjusted for gender and height)
5. **Weak grip strength** (adjusted for gender and BMI)

- **Robust**: 0 criteria
- **Pre-frail**: 1-2 criteria
- **Frail**: ≥3 criteria

**FRAILTY INDEX (DEFICIT ACCUMULATION):**
- Proportion of potential health deficits present (symptoms, signs, diseases, disabilities, laboratory abnormalities)
- More continuous measure (0 = fit, 1 = very frail)
- More predictive but more complex

**CLINICAL FRAILTY SCALE (CFS):**
1. Very Fit - robust, active, energetic
2. Well - without active disease, but less fit than category 1
3. Well Managed - treated comorbidities, no symptoms
4. Vulnerable - symptoms but independent
5. Mildly Frail - needs help with IADLs (finances, transportation, medications)
6. Moderately Frail - needs help with ADLs (shopping, housework)
7. Severely Frail - completely dependent on others for ADLs, or appears very frail
8. Very Severely Frail - terminally ill,接近 end of life
9. Terminally Ill - life expectancy <6 months, not strictly frailty

**SCREENING TOOLS:**
- **PRISMA-7**: 7-item questionnaire
- **ED identifying frailty**: Clinical Frailty Scale, ISAR (Identification of Seniors at Risk)
- **Timed Up and Go (TUG)**: <10s robust, 10-20s pre-frail, >20s frail, >30s dependent

**IMPLICATIONS OF FRAILTY:**
- **Increased vulnerability**: Minor stressors cause disproportionate deterioration
- **Adverse outcomes**: Falls, delirium, functional decline, institutionalization, hospitalization, death
- **Altered risk-benefit**: More likely to experience ADRs, less likely to benefit from aggressive interventions
- **Surgical outcomes**: Higher complication rates, mortality, longer hospital stays
- **Chemotherapy**: Toxicity, reduced tolerance, need for dose adjustments

**MANAGEMENT:**
- **Exercise**: Resistance training + aerobic exercise (most evidence-based intervention)
  - 2-3 sessions per week, progressive intensity
  - Improves strength, gait speed, balance, ADLs, may even reverse frailty
- **Nutrition**: Adequate protein (1.0-1.5 g/kg/day), adequate calories, treat deficiencies (vitamin D, B12)
- **Multicomponent interventions**: Exercise + nutrition + cognitive stimulation + social engagement
- **Medication review**: Deprescribe fall-risk-increasing drugs, reduce polypharmacy burden
- **Comprehensive Geriatric Assessment (CGA)**: Multidimensional, interdisciplinary diagnostic process
  - Medical, functional, psychological, social assessment
  - Develops coordinated, integrated care plan
  - Reduces institutionalization, improves outcomes

**FRAILTY IN SURGICAL DECISION-MAKING:**
- **Preoperative CGA**: Assess fitness, identify optimization opportunities, set expectations
- **Shared decision-making**: Discuss goals of care, risks/benefits, quality of life
- **Perioperative care**: Early mobilization, optimal nutrition, delirium prevention, pain management
- **Conservative vs surgical**: Frail patients may benefit from less invasive approaches (watchful waiting, medical management)

**FRAILTY IN ONCOLOGY:**
- **Chemotherapy toxicity**: Use Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) or CARG (Cancer and Aging Research Group) tools
- **Dose adjustments**: Reduce initial dose, monitor closely, consider adjuvant treatment differently
- **Goals of care**: Focus on quality of life, symptom control, may opt for palliative approaches

**REVERSIBILITY:**
- **Pre-frailty is potentially reversible** with targeted interventions
- **Early frailty may be ameliorated** but unlikely to completely resolve
- **Severe frailty is less reversible** but still benefits from interventions (function, QoL)

**SCREENING RECOMMENDATIONS:**
- All adults aged ≥70 should be screened for frailty
- Use a rapid screening tool first (PRISMA-7, CFS)
- Positive screen warrants comprehensive assessment

**SOURCES:** NICE NG161, Fried Frailty Phenotype, BGS, AGS
""",
            confidence=0.96,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Frailty Assessment and Management",
                "sources": ["NICE NG161", "Fried Frailty Phenotype", "BGS", "AGS"]
            }
        )

    def _handle_elder_abuse_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle elder abuse queries (non-emergency)."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**ELDER ABUSE AND SAFEGUARDING**

**PREVALENCE:**
- Community: ~10% (likely under-reported)
- Care homes: 20-40% (varies by study)
- Only 1 in 24 cases reported to authorities

**TYPES OF ELDER ABUSE:**
1. **Physical**: Slapping, hitting, restraining, force-feeding, inappropriate use of medications
2. **Psychological/Emotional**: Threats, humiliation, isolation, ignoring, treating like a child
3. **Financial**: Misuse of money, property, assets; theft; fraud; coercion; undue influence
4. **Sexual**: Non-consensual sexual contact, inappropriate comments
5. **Neglect**: Failure to provide basic needs (food, water, shelter, clothing, medical care, hygiene)
6. **Abandonment**: Desertion by person with responsibility for care
7. **Self-neglect**: Failure to perform self-care (may be due to cognitive impairment, depression)

**RISK FACTORS:**
- **Victim**: Cognitive impairment (dementia), functional impairment, social isolation, history of domestic violence, poor physical health, dependence on others
- **Perpetrator**: Mental illness, substance misuse, financial stress, dependency on victim, history of violence, lack of support/caregiver training, unrealistic expectations

**WARNING SIGNS:**
- **Physical**: Unexplained injuries, bruising in unusual patterns (grab marks, restraint marks), pressure ulcers, poor hygiene, untreated medical conditions, weight loss, dehydration
- **Behavioral/Emotional**: Fear, anxiety, depression, withdrawal, agitation, low self-esteem, hopelessness, rocking, sucking (especially in dementia)
- **Financial**: Unexplained bank withdrawals, missing belongings, suspicious changes in wills/property deeds, unnecessary services/goods, lack of necessities despite adequate funds
- **Caregiver**: Prevents private visits, speaks for the patient, dismisses concerns, shows anger, indifference, aggressive behavior, financial dependence

**ASSESSMENT:**
- **Private interview**: See patient alone, explain confidentiality, build trust, use simple questions
- **Specific questions**: "Has anyone hurt you?" "Are you afraid of anyone?" "Has anyone taken your money without asking?" "Does anyone make you feel uncomfortable?"
- **Cognitive assessment**: Determine capacity to understand situation, make decisions
- **Physical examination**: Document injuries, photographic evidence with consent
- **Capacity assessment**: If cognitive impairment, determine if patient can make decisions about safety

**REPORTING AND SAFEGUARDING:**
- **Mandatory reporting**: Varies by jurisdiction - know your local laws
- **Safeguarding Adults**: Vulnerable adults protection procedures
- **Adult Protective Services (APS)**: US; **Safeguarding Adults Boards**: UK
- **Law enforcement**: If criminal activity (assault, theft, fraud)
- **Emergency**: If immediate danger, involve police, emergency protective services, medical treatment

**MANAGEMENT:**
- **Ensure safety**: May require emergency placement, protective services, legal intervention
- **Medical treatment**: Address injuries, health neglect
- **Support services**: Social work, victim advocacy, legal aid, mental health
- **Address perpetrator**: Legal action, restraining orders, mandatory treatment programs, removal from caregiving role
- **Patient choice**: If patient has capacity, respect their autonomy (may choose to stay with abuser), but ensure safety planning
- **Capacity**: If lacks capacity, must act in best interests (may require protective intervention)

**PREVENTION:**
- **Caregiver support**: Respite care, counseling, education, financial support
- **Socialization**: Reduce isolation, community programs, senior centers
- **Financial protection**: Direct deposit, powers of attorney, monitoring, financial education
- **Early intervention**: Recognize warning signs, address caregiver stress, connect with services

**DOCUMENTATION:**
- **Detailed documentation**: Quotes from patient, descriptions of injuries, observations, conversations, concerns
- **Objective**: Factual, non-judgmental, specific dates/times
- **Photographic evidence**: With consent, document injuries
- **Report**: Follow local safeguarding procedures, document all referrals and actions

**SOURCES**: NICE NG22, WHO Elder Abuse Guidelines, BGS, National Center on Elder Abuse
""",
            confidence=0.93,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Elder Abuse and Safeguarding",
                "sources": ["NICE NG22", "WHO Elder Abuse Guidelines", "BGS"]
            }
        )

    def _handle_elder_abuse_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle emergency elder abuse situations."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**ELDER ABUSE - EMERGENCY PROTOCOL**

**IF IMMEDIATE DANGER EXISTS:**

**IMMEDIATE ACTIONS:**
1. **ENSURE SAFETY**: Remove from dangerous situation if possible, call police/emergency services (911/999/112)
2. **MEDICAL ASSESSMENT**: Treat injuries, arrange emergency evaluation if needed
3. **DO NOT CONFRONT PERPETRATOR**: May increase danger to victim and yourself
4. **DOCUMENT**: Take photographs if safe, note injuries, record statements
5. **REPORT**: Contact Adult Protective Services (APS) or equivalent, law enforcement
6. **PROTECTIVE SERVICES**: Arrange emergency placement, restraining order if needed

**EMERGENCY CONTACTS:**
- **Police/Emergency**: 911 (US), 999 (UK), 112 (EU)
- **Adult Protective Services**: 24-hour emergency lines in most jurisdictions
- **Domestic violence hotlines**: Often serve elder abuse victims
- **Hospital social work**: Available 24/7 in emergency departments

**RED FLAGS FOR IMMEDIATE DANGER:**
- Threats of harm with weapon access
- History of escalating violence
- Severe injuries requiring hospitalization
- Life-threatening neglect (starvation, dehydration, untreated medical conditions)
- Sexual assault
- Patient expresses fear for life

**LEGAL EMERGENCY POWERS:**
- **Emergency protective orders**: Can be issued by police or courts (ex parte)
- **Emergency removal**: APS/authorities can remove victim if danger present
- **Emergency medical treatment**: Can provide despite lack of consent if life-threatening

**DO NOT:**
- Send patient back to dangerous situation
- Leave patient alone with perpetrator
- Dismiss concerns or minimize allegations
- Wait for "more proof" if danger present

**REMEMBER**: Elder abuse is a crime. Immediate danger requires immediate action. Protect the patient, document findings, report to authorities.

**URGENT REFERRAL REQUIRED**
""",
            confidence=0.98,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Elder Abuse - Emergency",
                "urgency": "emergency",
                "sources": ["Adult Protective Services Guidelines", "Safeguarding Adults Boards"]
            }
        )

    def _handle_bowel_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle constipation and bowel care queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**CONSTIPATION AND BOWEL CARE IN OLDER ADULTS**

**PREVALENCE:**
- Community: 20-30%
- Care homes: 40-60%
- More common in women, with age, immobility, polypharmacy

**DEFINITION:**
- **Rome IV criteria**: Fewer than 3 spontaneous bowel movements per week, plus at least 2 of:
  - Straining >25% of defecations
  - Lumpy/hard stools >25%
  - Sensation of incomplete evacuation >25%
  - Sensation of anorectal obstruction/blockage >25%
  - Manual maneuvers to facilitate >25%
  - Loose stools rarely without laxatives

**CAUSES (MULTIFACTORIAL):**
- **Reduced mobility**: Immobility, weakness, bed rest
- **Medications**: Opioids (major cause), anticholinergics, calcium channel blockers, iron, calcium, aluminum, diuretics (dehydration), antipsychotics
- **Dietary**: Low fiber, inadequate fluid intake, poor appetite
- **Neurological**: Stroke, Parkinson's, diabetes (autonomic neuropathy), spinal cord injury
- **Anorectal**: Hemorrhoids, anal fissures (pain → withholding), rectal prolapse
- **Metabolic**: Hypothyroidism, hypercalcemia, diabetes, hypokalemia
- **Psychological**: Depression, dementia (forgetting to toilet, ignoring urge), lack of privacy
- **Functional**: Inability to access toilet, bedpans, inadequate toileting assistance

**COMPLICATIONS:**
- **Fecal impaction**: Mass of hard stool in rectum, can cause overflow incontinence (encopresis)
- **Bowel obstruction**: Complete or partial obstruction
- **Stercoral ulcer**: Pressure necrosis from impacted stool, can perforate
- **Diverticular disease**: Increased pressure in colon
- **Hemorrhoids, anal fissures**: Straining
- **Urinary retention**: Distended rectum compresses urethra
- **Delirium**: Constipation as cause in elderly

**ASSESSMENT:**
- **History**: Frequency, consistency (Bristol Stool Form Scale), straining, pain, bleeding, medications, mobility, diet, fluids, toileting routine
- **Physical**: Abdominal examination (distension, masses, fecal loading), digital rectal exam (assess tone, masses, fecal impaction), anal inspection (hemorrhoids, fissures)
- **Investigations**: If red flags present (weight loss, rectal bleeding, anemia, family history of colon cancer, change in bowel habit)
  - **Colonoscopy/CT colonography**: Exclude colorectal cancer if not screened within interval
  - **Thyroid function tests**: If clinical suspicion
  - **Calcium**: If suspected hypercalcemia

**MANAGEMENT:**
- **Non-pharmacological FIRST**:
  - Increase fiber intake gradually (30 g/day) - fruits, vegetables, whole grains, bran
  - Adequate fluids (1.5-2 L/day unless contraindicated - heart failure, renal failure)
  - Regular toileting routines (same time daily, especially after breakfast - gastrocolic reflex)
  - Adequate privacy, comfortable positioning, footstool to flex hips
  - Address mobility: encourage walking, physiotherapy
  - Medication review: reduce/stop constipating medications if possible
- **Laxatives (if needed)**:
  1. **Bulk-forming** (first-line): Psyllium, methylcellulose, bran - take with PLENTY of water (risk of obstruction without adequate fluids)
  2. **Osmotic**: Polyethylene glycol (PEG) - first-line if bulk-forming inadequate, safe for long-term use; lactulose - can cause bloating, flatulence
  3. **Stimulant**: Senna, bisacodyl - for短期 use, may cause cramping, avoid long-term daily use
  4. **Stool softener**: Docusate - weak evidence, generally not used alone
  5. **Suppositories/enemas**: For fecal impaction or acute relief
- **Fecal impaction management**:
  - Manual evacuation if necessary (gloved, lubricated finger, may need sedation)
  - Enemas (phosphate, mineral oil) followed by oral laxatives
  - May require multiple attempts
  - Consider underlying cause to prevent recurrence

**PREVENTION:**
- **High-fiber diet** (if no contraindications like dysphagia, intestinal obstruction)
- **Adequate hydration**
- **Regular physical activity**
- **Toileting routine**: Same time daily, after meals, respond promptly to urge
- **Medication review**: Minimize constipating medications, prophylactic laxatives with opioids
- **Address functional barriers**: Easy toilet access, mobility aids, adequate assistance

**RED FLAGS (REFER):**
- Rectal bleeding (exclude cancer)
- Unintentional weight loss (>5% in 1 month)
- Anemia
- Family history of colorectal cancer
- Change in bowel habit >6 weeks (especially if looser stools, more frequent)
- Positive fecal occult blood test
- New-onset constipation in someone previously regular

**SOURCES:** NICE CG177, BGS Constipation Guidelines
""",
            confidence=0.92,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Constipation and Bowel Care",
                "sources": ["NICE CG177", "BGS Guidelines"]
            }
        )

    def _handle_sleep_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sleep disorder queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**SLEEP DISORDERS IN OLDER ADULTS**

**AGE-RELATED CHANGES:**
- **Reduced total sleep time**: From 7-9 hours (young adult) to 6-7 hours (older adult)
- **Increased sleep fragmentation**: More awakenings, lighter sleep
- **Advanced sleep phase**: Earlier bedtime, earlier awakening
- **Reduced slow-wave sleep** (deep sleep)
- **Increased napping**

**COMMON SLEEP COMPLAINTS:**
- **Insomnia**: Difficulty falling or staying asleep, 30-50% prevalence
- **Sleep apnea**: Obstructive (OSA) and central (CSA), 20-40% prevalence (under-diagnosed)
- **Restless legs syndrome (RLS)**: Urge to move legs, worse at rest/evening, relieved by movement, 10-35%
- **Periodic limb movement disorder (PLMD)**: Repetitive leg movements during sleep, can cause sleep fragmentation
- **REM sleep behavior disorder (RBD)**: Acting out dreams, can precede Parkinson's by years
- **Circadian rhythm disorders**: Advanced sleep phase syndrome, irregular sleep-wake rhythm

**INSOMNIA:**
- **Types**: Initial (difficulty falling asleep), Middle (difficulty staying asleep), Late (early awakening), Non-restorative sleep
- **Causes**: Medical conditions (pain, COPD, CHF, GERD, nocturia), medications (diuretics, theophylline, corticosteroids, stimulants), psychiatric (depression, anxiety), circadian changes, poor sleep hygiene, sleep apnea, RLS, environment (noise, light, temperature)
- **Management**:
  1. **Treat underlying causes** (pain, nocturia, depression, sleep apnea)
  2. **Sleep hygiene**: Regular schedule, relaxing bedtime routine, dark/quiet/cool bedroom, limit caffeine/alcohol/nicotine (especially later in day), limit daytime naps (<30 min, not late afternoon), exercise (but not too close to bedtime)
  3. **Cognitive behavioral therapy for insomnia (CBT-I)**: First-line treatment (stimulus control, sleep restriction, cognitive restructuring, relaxation techniques)
  4. **Medications** (short-term only, <4 weeks):
     - **NON-benzodiazepines** ("Z-drugs"): Zolpidem, Zopiclone, Eszopiclone - shorter half-life, less dependence risk than benzodiazepines but still carry fall, confusion, dependence risk; use lowest dose for shortest duration
     - **Melatonin receptor agonists**: Ramelteon - less abuse potential, may be safer in elderly
     - **Sedating antidepressants**: Trazodone 25-50 mg at bedtime (often used off-label, relatively safe but can cause orthostasis)
     - **Benzodiazepines**: AVOID in elderly - high risk of falls, confusion, delirium, dependence, respiratory depression, interactions
     - **Antihistamines**: AVOID - anticholinergic effects, delirium risk, tolerance develops

**SLEEP APNEA:**
- **Risk factors**: Obesity, male gender, neck circumference >17" (men) >16" (women), craniofacial abnormalities, family history, alcohol, sedatives, smoking
- **Symptoms**: Snoring, witnessed apneas, gasping/choking, daytime sleepiness, morning headaches, cognitive impairment, hypertension, nocturia
- **Consequences**: Hypertension, cardiovascular disease, stroke, cognitive impairment, falls, motor vehicle accidents, mortality
- **Diagnosis**: Overnight polysomnography (sleep study) or home sleep apnea test
- **Management**:
  - **Weight loss** if overweight
  - **Positional therapy** (avoid supine sleeping)
  - **CPAP** (continuous positive airway pressure) - first-line for moderate-severe OSA, highly effective but adherence is challenging
  - **Oral appliances** (mandibular advancement devices) - for mild-moderate OSA or CPAP intolerance
  - **Surgery** (UPPP, MMA, hypoglossal nerve stimulator) - select cases
  - **Oxygen** - for central sleep apnea (Cheyne-Stokes respiration in heart failure)

**RESTLESS LEGS SYNDROME (RLS):**
- **Diagnostic criteria** (all 4 required):
  1. Urge to move legs, usually accompanied by uncomfortable sensations
  2. Symptoms begin/worsen during periods of rest/inactivity
  3. Partially/totally relieved by movement
  4. Symptoms worse in evening/night
- **Causes**: Iron deficiency, renal failure, neuropathy, pregnancy, medications (antidepressants, antipsychotics), familial
- **Investigations**: Ferritin level (iron stores), consider sleep study if PLMD suspected
- **Management**:
  - Treat iron deficiency if present (oral iron if ferritin <75 mcg/L, IV if malabsorption)
  - **Dopamine agonists**: Pramipexole, ropinirole - effective but risk of augmentation (symptoms worsen, start earlier, affect other body parts)
  - **Alpha-2-delta ligands**: Gabapentin, pregabalin - effective, no augmentation risk, may help comorbid pain/neuropathy
  - **Opioids**: For refractory cases (low-dose oxycodone, methadone)
  - Avoid caffeine, alcohol, smoking; warm baths, massage, exercise

**REM SLEEP BEHAVIOR DISORDER (RBD):**
- **Symptoms**: Acting out dreams (punching, kicking, shouting, falling out of bed), can cause injury to patient or bed partner
- **Causes**: Synucleinopathies (Parkinson's, Lewy body dementia, MSA), medications (antidepressants), brainstem lesions
- **Management**:
  - **Safety first**: Pad bed, remove dangerous objects, floor mattress
  - **Melatonin** 3-12 mg at bedtime (first-line)
  - **Clonazepam** 0.5-2 mg at bedtime (effective but risk of falls, confusion, respiratory depression)
  - Treat underlying Parkinson's if present
  - **Prognosis**: May precede Parkinson's by years (mean 7-10 years) - neurodegenerative marker

**SOURCES:** NICE, AASM Sleep Guidelines, BGS
""",
            confidence=0.91,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Sleep Disorders",
                "sources": ["NICE", "AASM Guidelines", "BGS"]
            }
        )

    def _handle_pain_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pain management queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**PAIN MANAGEMENT IN OLDER ADULTS**

**PREVALENCE:**
- Community: 25-50%
- Care homes: 45-80%
- Under-recognized and under-treated

**PAIN ASSESSMENT CHALLENGES:**
- **Cognitive impairment**: Patients may not report pain due to memory problems, communication difficulties, aphasia
- **Atypical presentation**: Pain may manifest as agitation, aggression, confusion, withdrawal, decreased appetite, sleep disturbance
- **Beliefs**: "Pain is part of aging," fear of addiction, fear of being a burden
- **Communication barriers**: Sensory deficits (hearing, vision), language barriers

**ASSESSMENT TOOLS:**
- **Self-report**: Numeric rating scale (0-10), verbal descriptor scale (no pain to worst pain), visual analog scale
- **Observational scales** (if dementia present):
  - PAINAD (Pain Assessment in Advanced Dementia)
  - DOLOPLUS-2
  - Abbey Pain Scale
- **Clinical assessment**: Facial expressions, vocalizations, body movements, changes in interpersonal interactions, changes in routine activities, mental status changes

**TYPES OF PAIN:**
1. **Nociceptive**:
   - **Somatic**: Musculoskeletal, skin, bone (well-localized, aching/throbbing)
   - **Visceral**: Organs (poorly localized, cramping/pressure)
2. **Neuropathic**: Nerve damage (burning, shooting, electric-shock-like, allodynia, hyperalgesia)
3. **Mixed**: Both nociceptive and neuropathic components

**MULTIMODAL PAIN MANAGEMENT:**
- **Non-pharmacological**: First-line or adjunct (exercise, physical therapy, heat/cold, massage, acupuncture, TENS, cognitive-behavioral therapy, relaxation techniques)
- **Pharmacological**: Stepwise approach, start low, go slow, assess regularly

**PHARMACOLOGICAL LADDER (WHO Adapted for Geriatrics):**

**Step 1: Non-opioids**
- **Paracetamol/Acetaminophen**: First-line for mild-moderate pain, 3-4 g/day (max 4 g), safe in most patients (reduce dose to 2-3 g if liver disease, malnutrition, alcohol use)
- **Topical NSAIDs**: Diclofenac, ketoprofen - effective for localized pain (knee OA), minimal systemic absorption, safer than oral NSAIDs
- **Oral NSAIDs**: Last resort, short-term, low-dose, with PPI if absolutely necessary (GI bleed, AKI, heart failure exacerbation, hypertension risk)

**Step 2: Adjuvants** (for neuropathic pain)
- **Gabapentinoids**: Gabapentin, Pregabalin - first-line for neuropathic pain, titrate slowly, monitor for sedation, dizziness, edema, reduce dose in renal impairment
- **TCAs**: Amitriptyline, Nortriptyline - effective but anticholinergic burden (arrhythmias, constipation, urinary retention, confusion), nortriptyline better tolerated, avoid in cardiac disease, glaucoma, significant prostatism
- **SNRIs**: Duloxetine, Venlafaxine - effective for diabetic neuropathy, musculoskeletal pain, safer than TCAs in cardiac disease, watch for hypertension (duloxetine)

**Step 3: Weak opioids** (if Step 1+2 inadequate)
- **Codeine**: Prodrug (requires CYP2D6 conversion to morphine), 5-10% of population are poor metabolizers (ineffective), constipation, N/V
- **Tramadol**: Weak mu-opioid agonist + serotonin/norepinephrine reuptake inhibitor, 50-100 mg q6h PRN, risk of serotonin syndrome (especially with SSRIs), lowers seizure threshold
- **Consider constipation prevention**: Stimulant laxatives (senna, bisacodyl) prophylactically

**Step 4: Strong opioids** (severe pain, specialist initiation preferred)
- **Morphine**: Gold standard, 2.5-5 mg q4h PRN or 5-10 mg sustained-release q12h, titrate to effect, monitor for sedation, respiratory depression, constipation, nausea, hallucinations, myoclonus
- **Oxycodone**: More potent than morphine, 1.5-2x, less histamine release (less pruritus), similar side effect profile
- **Hydromorphone**: For renal failure (no active metabolites)
- **Methadone**: Complex pharmacokinetics, long half-life, QT prolongation, specialist only
- **Fentanyl**: Transdermal patch for chronic stable pain (calculations complex, not for opioid-naïve, risk of fatal overdose if misused), transmucosal for breakthrough pain

**OPIOID RISKS IN OLDER ADULTS:**
- **Falls**: Increased risk (sedation, dizziness)
- **Delirium**: Opioids are deliriogenic, especially in those with cognitive impairment
- **Constipation**: Universal side effect, requires prophylactic laxatives
- **Respiratory depression**: Risk increases with age, renal impairment, drug interactions
- **Urinary retention**: Especially in men with BPH
- **Cognitive impairment**: Sedation, confusion, hallucinations

**OPIOID PRESCRIBING PRINCIPLES:**
- **Clear indication**: Document expected benefits and risks
- **Start LOW, go SLOW**: 25-50% of starting dose for younger adults
- **Regular review**: Discontinue if not achieving goals, reassess risks/benefits
- **Set goals**: Pain reduction, functional improvement, not necessarily pain-free
- **Opioid agreement**: If long-term opioids, document expectations, single prescriber, regular urine drug screens (if high risk)
- **Avoid concurrent benzodiazepines**: Fatal overdose risk
- **Risk assessment**: History of substance misuse, mental health disorders

**PAIN IN DEMENTIA:**
- **Assessment**: Use observational scales, ask family/carers about typical behaviors indicating pain
- **Common conditions**: Osteoarthritis, constipation, urinary tract infection, pressure ulcers, dental disease
- **Management**: Same principles but lower thresholds for treatment, avoid high anticholinergic burden medications

**END-OF-LIFE PAIN:**
- **Pain is common** but treatable
- **WHO analgesic ladder** applies, be aggressive with pain control
- **OPIOIDS are appropriate** and necessary for severe pain - fear of addiction is irrelevant at end of life
- **Regular vs PRN**: Scheduled dosing prevents pain recurrence
- **Parenteral routes** (SC, IV) if unable to take oral

**SOURCES:** AGS Beers Criteria 2023, BGS Pain Guidelines, WHO Analgesic Ladder
""",
            confidence=0.94,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Pain Management",
                "sources": ["AGS Beers Criteria 2023", "BGS Guidelines", "WHO Analgesic Ladder"]
            }
        )

    def _handle_capacity_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle mental capacity queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**MENTAL CAPACITY ASSESSMENT**

**CAPACITY DEFINITION:**
Ability to understand, retain, and use information to make a decision, and communicate that decision.

**LEGAL FRAMEWORK:**
- **UK**: Mental Capacity Act 2005 (MCA)
- **US**: Varies by state, generally common law principles, advance directives, healthcare proxies
- **Assumption of capacity**: All adults are assumed to have capacity unless proven otherwise

**KEY PRINCIPLES (UK MCA):**
1. **Presumption of capacity**: Adults have capacity unless proven otherwise
2. **Maximize decision-making**: All practical steps to support decision-making must be taken before concluding lack of capacity
3. **Unwise decisions**: People have the right to make decisions others might consider unwise (this doesn't mean they lack capacity)
4. **Best interests**: Decisions made for those lacking capacity must be in their best interests
5. **Least restrictive option**: Choose option least restrictive of person's rights/freedom

**ASSESSING CAPACITY:**
- **Decision-specific**: Capacity is assessed for each specific decision at a specific time (not global)
- **Time-specific**: Capacity can fluctuate (delirium, medications, time of day)
- **Four test components** (ALL must be present):
  1. **Understand**: Comprehend information relevant to decision (diagnosis, treatment options, risks, benefits, alternatives, consequences of no treatment)
  2. **Retain**: Hold information long enough to make decision (may need repeated explanations, written information)
  3. **Use/Weigh**: Use information to weigh options and come to decision (appreciate how decision affects them)
  4. **Communicate**: Communicate decision by any means (speech, writing, gestures, blinking)

**FACTORS AFFECTING CAPACITY:**
- **Cognitive impairment**: Dementia (severity, type), delirium (acute fluctuation), intellectual disability
- **Psychiatric**: Depression, psychosis, anxiety
- **Neurological**: Stroke (aphasia, neglect), brain injury, Parkinson's
- **Medical**: Pain, medications (sedatives, anticholinergics, opioids), metabolic disturbances
- **Sensory**: Hearing/vision impairment (affects communication, not cognition)
- **Emotional**: Fear, fatigue, stress

**CAPACITY ASSESSMENT PROCESS:**
1. **Identify specific decision**: What decision needs to be made?
2. **Provide relevant information**: Diagnosis, treatment options, risks/benefits, consequences of refusing, in simple language
3. **Assess understanding**: Ask patient to explain back in their own words
4. **Check retention**: Repeat information if needed, assess recall
5. **Assess weighing**: Can they articulate reasons for decision?
6. **Assess communication**: Can they communicate their decision?
7. **Document**: All findings, reasons for conclusions

**IMPAIRED CAPACITY:**
- **Decision-specific**: May have capacity for simple decisions (what to eat, what to wear) but not complex (medical treatment, finances)
- **Temporary**: Delirium, acute illness, medications - reassess when condition improves
- **Permanent**: Severe dementia, advanced neurodegenerative disease

**ADVANCE PLANNING:**
- **Advance decisions (living will)**: Refusal of specific treatments in specific circumstances in advance, must be in writing, signed, witnessed, specific
- **Advance statements**: Expressions of preferences, wishes, beliefs (not legally binding but must be considered)
- **Lasting Power of Attorney (LPOA)**: Appoint someone to make decisions if lose capacity (health/welfare, property/financial)
- **Do Not Attempt Cardiopulmonary Resuscitation (DNACPR)**: Specific to CPR, not broader treatment decisions

**BEST INTERESTS DECISION-MAKING** (if patient lacks capacity):
- **Multidisciplinary**: Involve family, carers, healthcare team
- **Consider**: Past/present wishes, feelings, values, beliefs, written statements, appointed representatives
- **Avoid discrimination**: Not based on age, appearance, condition, behavior
- **Consider**: All relevant circumstances, likelihood of regaining capacity
- **Least restrictive**: Choose least restrictive option

**SPECIAL CONSIDERATIONS:**
- **Emergency**: Life-saving treatment without consent if emergency and lack capacity
- **Fluctuating capacity**: Make decisions when capacity is best (morning, after medication adjustment)
- **Communication barriers**: Use interpreters, hearing aids, glasses, communication aids
- **Psychiatric illness**: Treat underlying condition before concluding permanent lack of capacity
- **Detrimental effects**: Consider if untreated condition affecting capacity

**SOURCES:** Mental Capacity Act 2005, BGS Capacity Guidelines
""",
            confidence=0.93,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Mental Capacity Assessment",
                "sources": ["Mental Capacity Act 2005", "BGS Guidelines"]
            }
        )

    def _handle_palliative_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle end-of-life and palliative care queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**END-OF-LIFE CARE AND PALLIATIVE MEDICINE**

**DEFINITIONS:**
- **Palliative care**: Active, holistic care for patients with advanced, progressive illness; focus on QoL, relief of suffering
- **End-of-life care**: Last days/weeks of life, when death is imminent (hours to days) or expected within days to weeks
- **Terminal care**: Care during the dying phase when death is expected within hours to days

**PROGNOSTICATION:**
- **Surprise question**: "Would I be surprised if this patient died in the next 6-12 months?"
- **Clinical indicators**:
  - Performance status (ECOG 3-4, Karnofsky <50%, bedbound >50% of day)
  - Progressive weight loss (>10% in 6 months)
  - Recurrent hospitalizations, ED visits
  - Increasing symptom burden, refractory symptoms
  - Declining functional status
  - Physiological changes (albumin <2.5, lymphocytopenia)
  - Specific disease indicators (metastatic cancer, NYHA IV CHF, FEV1 <30% predicted)

**RECOGNIZING THE DYING PHASE (LAST DAYS-HOURS):**
- **Breathing**: Changes in respiratory pattern (Cheyne-Stokes, apnea periods), noisy breathing (secretions)
- **Consciousness**: Decreasing consciousness, drowsiness, unresponsive
- **Skin**: Mottling, pallor, cool extremities
- **Urine**: Decreased output, dark/concentrated
- **Oral**: Dry mouth, decreased oral intake, difficulty swallowing meds
- **Vital signs**: BP drops, pulse may increase or decrease, temperature variability
- **Communication**: Unable to communicate verbally

**COMMUNICATION:**
- **Advance care planning (ACP)**: Discuss goals of care, preferred place of death, life-sustaining treatments EARLY (before crisis)
- **Honesty**: Prognosis is uncertain, but general estimates helpful (days to weeks vs months)
- **Explore**: Understanding of illness, expectations, fears, priorities
- **Family meetings**: Include key family members, document decisions, provide written summary
- **Cultural considerations**: Respect cultural/religious beliefs around death, dying

**SYMPTOM MANAGEMENT IN LAST DAYS OF LIFE:**

**Pain**:
- **Regular opioids**: Morphine subcutaneous 10 mg q4h or 2.5-5 mg q1h PRN, titrate to comfort
- **Adjuvant analgesics**: Gabapentin, dexamethasone for bone pain, nerve compression
- **Monitor**: For sedation, respiratory depression (less concern when dying)
- **Parenteral routes**: Subcutaneous infusion (syringe driver) if unable to take oral

**Nausea/Vomiting**:
- **Anti-emetics**: Levomepromazine 6.25 mg SC q8-12h, or haloperidol 1.5-3 mg SC q8-12h, or metoclopramide 10 mg SC q8h (avoid in complete bowel obstruction)
- **Identify cause**: Constipation, hypercalcemia,Raised ICP, medications, gastric stasis, bowel obstruction

**Respiratory Secretions (Death Rattle)**:
- **Anticholinergics**: Hyoscine butylbromide 20-60 mg SC q4-6h, or glycopyrronium 200-400 mcg SC q4-6h
- **Repositioning**: Turn patient regularly, gentle suctioning if distressing
- **Educate family**: Common, does not cause distress to patient (can distress family)

**Dyspnea/Breathlessness**:
- **Opioids**: Morphine 2.5-5 mg SC/PO q4h PRN (reduces respiratory drive, anxiety)
- **Oxygen**: If hypoxic, but not routine if SpO2 normal (may prolong dying)
- **Cool air**, open window, fan
- **Anxiolytics**: Midazolam 2.5-5 mg SC/SL q1h PRN (for anxiety, not routine)

**Agitation/Delirium**:
- **Identify reversible causes**: Pain, urinary retention, constipation, hypoxia, metabolic disturbances, medications
- **Treat underlying cause** if feasible and consistent with goals
- **Antipsychotics**: Haloperidol 1.5-3 mg SC q8-12h, or levomepromazine (sedating antipsychotic)
- **Benzodiazepines**: Midazolam 2.5-10 mg SC infusion for severe agitation

**Fever**:
- **Paracetamol/acetaminophen**: 1 g PR/PO q6h PRN
- **Cool measures**: Tepid sponging, fan
- **Avoid antibiotics** unless consistent with goals (no evidence improves comfort, prolongs dying)

**MYOCLONUS** (muscle jerks):
- **Common**: Opioid toxicity, renal failure, metabolic disturbances
- **Treatment**: Reduce opioid dose if toxicity suspected, midazolam, clonazepam, or gabapentin

**CARE AFTER DEATH**:
- **Confirm death**: Absent heart sounds, no pulse, no respiration, fixed pupils
- **Time of death**: Document
- **Family**: Time with body, cultural/religious practices
- **Bereavement support**: Offer follow-up, resources
- **Post-mortem**: If required (coroner/medical examiner)

**ETHICAL ISSUES:**
- **Artificial nutrition/hydration (ANH)**: No evidence prolongs life, reduces comfort (edema, secretions, incontinence), mouth care more important
- **Antibiotics**: Treat infection if symptoms (pain, dysuria) but not routine for asymptomatic bacteriuria, consider goals
- **Hospitalization**: Generally avoid unless symptoms cannot be managed at home
- **Resuscitation**: DNACPR if dying, CPR inappropriate (futile, harms body)
- **Organ donation**: Early referral if appropriate

**PREFERRED PLACE OF DEATH:**
- **Most people prefer to die at home**, but not always feasible (caregiver burden, symptom burden)
- **Support needed**: 24/7 access to medications/equipment, caregiver support/respite, community nursing, rapid response
- **Hospice**: Alternative to hospital, more home-like, expert symptom control, family support

**SOURCES:** NICE NG31, Gold Standards Framework, BGS
""",
            confidence=0.95,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "End-of-Life Care and Palliative Medicine",
                "sources": ["NICE NG31", "Gold Standards Framework", "BGS"]
            }
        )

    def _handle_rehabilitation_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle rehabilitation and discharge planning queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**REHABILITATION AND DISCHARGE PLANNING**

**COMPREHENSIVE GERIATRIC ASSESSMENT (CGA):**
- **Multidimensional, interdisciplinary**: Medical, functional, psychological, social assessment
- **Goal**: Optimize function, QoL, independence, reduce institutionalization, mortality
- **Components**:
  - Medical: Diagnoses, medications, prognosis
  - Functional: ADLs (activities of daily living), IADLs (instrumental ADLs), mobility, balance, continence
  - Psychological: Cognition, mood, behavior
  - Social: Living situation, support, finances, social network
  - Environmental: Home hazards, accessibility

**FUNCTIONAL ASSESSMENT:**
- **ADLs** (Katz Index): Bathing, dressing, toileting, transferring, continence, feeding
- **IADLs** (Lawton Scale): Shopping, cooking, housekeeping, laundry, transportation, medication management, finances, telephone
- **Mobility**: Ambulation, transfers (bed-chair, bed-standing), stairs, walking aid use
- **Tools**: Barthel Index, Functional Independence Measure (FIM), Timed Up and Go (TUG)

**REHABILITATION PRINCIPLES:**
- **Goal-oriented**: Set realistic, measurable goals with patient/family
- **Function-focused**: Aim for independence, safety, not necessarily "cure"
- **Multidisciplinary**: Physiotherapy, occupational therapy, speech therapy, nursing, social work, dietetics, psychology, medicine
- **Early mobilization**: Start ASAP after acute illness, bed rest is harmful
- **Intensity**: Higher intensity = better outcomes (but not to exhaustion)
- **Task-specific**: Practice specific tasks (walking, dressing, toileting)
- **Progressive**: Gradually increase difficulty as patient improves

**DISCHARGE PLANNING:**
- **Start early**: On admission, not day of discharge
- **Assess needs**: What support needed at home? Equipment, home modifications, caregivers
- **Home assessment**: Occupational therapy home visit for safety assessment
- **Medication reconciliation**: Ensure discharge medications correct, understood
- **Follow-up**: Arrange appointments (GP, specialist), therapy continuity
- **Patient/family education**: Diagnosis, medications, red flags, who to contact

**DISCHARGE DESTINATIONS:**
- **Home**: With or without support (family, home health aides, community nursing)
- **Rehabilitation unit**: For intensive therapy (usually 2-3 weeks), requires rehabilitation potential
- **Skilled nursing facility**: For subacute care, complex medical needs, some rehabilitation
- **Long-term care (nursing home)**: For permanent placement when unable to return home safely
- **Respite care**: Temporary placement for caregiver relief (usually 1-2 weeks)
- **Hospice**: For end-of-life care (home, hospice facility, hospital)

**CAREGIVER SUPPORT:**
- **Assess**: Caregiver burden, willingness, ability (physical, financial, emotional)
- **Education**: Training on medical tasks, medications, equipment
- **Respite**: Regular breaks to prevent burnout (adult day programs, in-home respite, residential respite)
- **Support groups**: Connect with other caregivers
- **Financial**: Identify available resources, insurance coverage

**EQUIPMENT NEEDS:**
- **Mobility**: Walkers, rollators, wheelchairs, scooters
- **ADL assistance**: Grab bars (bathroom, stair), raised toilet seat, shower chair, bed rails, transfer aids
- **Home modifications**: Ramps, stairlift, bathroom modifications, kitchen modifications
- **Communication**: Hearing aids, glasses, amplifiers
- **Other**: Oxygen, nebulizer, hospital bed, Hoyer lift

**COMMUNITY SERVICES:**
- **Home health agency**: Skilled nursing, physical/occupational/speech therapy, home health aide
- **Meals on Wheels**: Meal delivery for homebound
- **Adult day programs**: Socialization, activities, some healthcare
- **Transportation**: Paratransit services, volunteer driver programs
- **PACES (Program of All-Inclusive Care for the Elderly)**: Comprehensive care for nursing home-eligible who wish to remain at home (US)

**READMISSION PREVENTION:**
- **Medication reconciliation**: Ensure discharge medications correct, patient understands
- **Follow-up**: Prompt follow-up (within 7 days), preferably with same provider who knows patient
- **Red flags education**: Teach patient/family warning signs, who to contact
- **Transition**: Ensure smooth handoff to outpatient providers, send discharge summary promptly
- **Address social determinants**: Housing, food insecurity, transportation, caregiver support

**PROGNOSIS FOR REHABILITATION:**
- **Better prognosis**: Premorbid independence, acute illness (vs chronic decompensation), good cognition, motivation, social support
- **Poorer prognosis**: Severe dementia, severe functional dependence, multiple comorbidities, limited social support, very advanced age

**SOURCES:** NICE, BGS Rehabilitation Guidelines
""",
            confidence=0.92,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "Rehabilitation and Discharge Planning",
                "sources": ["NICE", "BGS Guidelines"]
            }
        )

    def _handle_general_geriatric_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general geriatric medicine queries."""

        return DomainQueryResult(
            domain_name="geriatric_medicine",
            answer="""
**GERIATRIC MEDICINE - COMPREHENSIVE OLDER ADULT CARE**

Geriatric medicine focuses on the unique needs of older adults, emphasizing comprehensive assessment, function, and quality of life over single-disease management.

**CORE GERIATRIC PRINCIPLES:**
- **Comprehensive Geriatric Assessment (CGA)**: Multidimensional, interdisciplinary evaluation
- **Function over disease**: Focus on what patient CAN do, independence, QoL
- **Multimorbidity management**: Coordinating care for multiple conditions, not single-disease guidelines
- **Medication optimization**: Deprescribing inappropriate medications, reducing polypharmacy burden
- **Frailty assessment**: Identifying vulnerability, targeting interventions
- **Person-centered care**: Respect preferences, goals, values

**GERIATRIC GIANTS (I'LL HELP FLOW mnemonic):**
- **I**mmobility: Falls, gait disorders, balance problems, syncope
- **L**oss of continence: Urinary and fecal incontinence
- **L**oss of cognition: Dementia, delirium, mild cognitive impairment
- **H** instability including falls: Postural hypotension, syncope, gait disorders
- **E**nd of life issues: Palliative care, advance care planning, goals of care
- **L**oneliness: Social isolation, depression, bereavement
- **F**ailure to thrive: Weight loss, malnutrition, sarcopenia, frailty
- **L**ow mood: Depression, anxiety, behavioral problems
- **O**lder carer needs: Caregiver burden, respite, support
- **W**orld turned upside down: Loss of home, role, independence

**COMPREHENSIVE GERIATRIC ASSESSMENT (CGA) COMPONENTS:**
1. **Medical**: Diagnoses, medications, symptoms, prognosis
2. **Functional**: ADLs, IADLs, mobility, balance, continence
3. **Psychological**: Cognition (MMSE, MoCA), mood (GDS), behavior
4. **Social**: Living situation, support, finances, social network, isolation
5. **Environmental**: Home hazards, accessibility, transportation

**GERIATRIC SYNDROMES:**
- Multifactorial health conditions that occur when accumulated deficits in multiple systems render older adult vulnerable
- Delirium, falls, incontinence, pressure ulcers, malnutrition, functional decline, frailty
- Not single-disease focused, require comprehensive, multifactorial assessment and management

**MULTIMORBIDITY MANAGEMENT:**
- **Problem**: Disease-specific guidelines often conflict when multiple conditions present
- **Approach**: Focus on patient priorities, symptom burden, functional status, prognosis
- **Deprescribing**: Systematically identify and discontinue inappropriate medications
- **Medication review**: Regular, structured reviews focusing on benefits vs harms, goals of care

**FRAILTY:**
- **Biological syndrome** of decreased reserve and resistance to stressors
- **Assessment**: Fried Frailty Phenotype, Clinical Frailty Scale (CFS), PRISMA-7
- **Management**: Exercise (resistance + aerobic), nutrition (adequate protein), medication optimization, treat underlying conditions

**POLYPHARMACY:**
- **Appropriate**: Evidence-based prescribing for multiple conditions
- **Inappropriate**: Prescribing where harms outweigh benefits
- **Management**: Proactive medication reviews, deprescribing, minimizing anticholinergic burden, avoid high-risk medications (Beers Criteria)

**FUNCTIONAL STATUS:**
- **ADLs** (activities of daily living): Bathing, dressing, toileting, transferring, continence, feeding
- **IADLs** (instrumental ADLs): Shopping, cooking, housekeeping, laundry, transportation, medication management, finances
- **Goals**: Maintain independence, safety, quality of life

**COGNITIVE DISORDERS:**
- **Dementia**: Progressive cognitive decline interfering with independence, multiple types (Alzheimer's, vascular, Lewy body, FTD)
- **Mild Cognitive Impairment (MCI)**: Objective cognitive decline without functional impairment (increased dementia risk but may not progress)
- **Delirium**: Acute confusional state, medical emergency, requires urgent assessment for underlying cause

**COMMON GERIATRIC CONDITIONS:**
- Falls, syncope, orthostatic hypotension
- Urinary and fecal incontinence
- Pressure ulcers
- Malnutrition, weight loss, sarcopenia
- Pain (under-recognized, under-treated)
- Sleep disorders (insomnia, sleep apnea, RLS)
- Depression (not a normal part of aging)
- Elder abuse and neglect

**END-OF-LIFE CARE:**
- Advance care planning discussions EARLY
- Goals of care discussions (curative vs palliative)
- Symptom management (pain, dyspnea, nausea, agitation, secretions)
- Hospice referral when prognosis <6 months
- Support for patients and families

**SOURCES:** NICE Guidelines, British Geriatrics Society, American Geriatrics Society
""",
            confidence=0.90,
            metadata={
                "specialty": "Geriatric Medicine",
                "focus": "General Geriatric Medicine",
                "sources": ["NICE", "British Geriatrics Society", "American Geriatrics Society"]
            }
        )


def create_geriatric_medicine_domain():
    """
    Factory function to create geriatric medicine domain instance.

    Returns:
        GeriatricMedicineDomain: Configured geriatric medicine specialty domain
    """
    return GeriatricMedicineDomain()
