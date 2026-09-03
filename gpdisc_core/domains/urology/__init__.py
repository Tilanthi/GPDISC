"""
Urology Domain for GPDISC

Comprehensive urological consultation covering:
- Kidney stones and renal colic
- Prostate conditions (BPH, prostatitis, prostate cancer)
- Bladder disorders (UTI, haematuria, bladder cancer)
- Erectile dysfunction and men's health
- Urological emergencies (testicular torsion, priapism, Fournier's gangrene)
- Paediatric urology (undescended testis, hypospadias)
- Urological imaging and investigations

Evidence-based guidelines:
- EAU (European Association of Urology)
- NICE NGxx guidelines
- AUA (American Urological Association)
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class UrologyDomain(BaseDomainModule):
    """
    Urology domain for comprehensive urological consultation

    Covers all aspects of adult and paediatric urology including
    kidney stones, prostate conditions, bladder disorders, and
    urological emergencies.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="urology",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive urology: kidney stones, prostate conditions, bladder disorders, men's health, urological emergencies",
            keywords=[
                "kidney stone", "renal stone", "ureteric", "colic", "flank pain",
                "prostate", "bph", "benign prostatic hyperplasia", "prostatitis", "psa",
                "prostate cancer", "turp", "prostatectomy",
                "bladder", "urinary tract infection", "uti", "cystitis", "haematuria",
                "blood in urine", "bladder cancer", "turbot",
                "erectile", "ed", "impotence", "viagra", "sildenafil", "tadalafil",
                "testicle", "testicular", "torsion", "pain", "lump",
                "priapism", "fournier", "gangrene", "urology emergency",
                "incontinence", "retention", "catheter", "prostate",
                "undescended testis", "hydrocele", "varicocele", "paediatric urology",
                "urology", "urological", "nephrolithiasis", "urolithiasis"
            ],
            capabilities=[
                "kidney_stone_management",
                "prostate_disease_evaluation",
                "bladder_disorder_consultation",
                "mens_health",
                "urological_emergency_triage",
                "haematuria_investigation",
                "erectile_dysfunction_management",
                "urinary_incontinence_assessment",
                "paediatric_urology"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process urology query with emergency detection and evidence-based responses
        """
        query_lower = query.lower()

        # UROLOGICAL EMERGENCIES - Highest priority

        # Testicular torsion - surgical emergency
        if any(term in query_lower for term in ["testicular torsion", "torsion testicle", "twisted testicle",
                                                   "severe testicular pain", "acute scrotal pain"]):
            return self._handle_testicular_torsion(query, context)

        # Priapism - emergency
        if any(term in query_lower for term in ["priapism", "persistent erection", "erection more than 4 hours"]):
            return self._handle_priapism(query, context)

        # Fournier's gangrene - emergency
        if any(term in query_lower for term in ["fournier", "gangrene", "scrotal gangrene", "perineal gangrene",
                                                   "necrotising fasciitis scrotum"]):
            return self._handle_fournier_gangrene(query, context)

        # Acute urinary retention with overflow
        if any(term in query_lower for term in ["acute retention", "cannot pass urine", "overflow",
                                                   "bladder bursting", "distended bladder"]):
            return self._handle_acute_retention(query, context)

        # Severe haematuria with clot retention
        if any(term in query_lower for term in ["clot retention", "heavy haematuria", "passing clots",
                                                   "bladder full of clots"]):
            return self._handle_clot_retention(query, context)

        # KIDNEY STONES / RENAL COLIC

        # Renal colic / kidney stone
        if any(term in query_lower for term in ["kidney stone", "renal stone", "renal colic", "ureteric stone",
                                                   "flank pain", "loin to groin", "ureteroscopy", "lithotripsy"]):
            return self._handle_kidney_stone(query, context)

        # PROSTATE CONDITIONS

        # Prostate cancer
        if any(term in query_lower for term in ["prostate cancer", "prostatic cancer", "psa cancer",
                                                   "prostate biopsy", "prostatectomy", "radical prostate"]):
            return self._handle_prostate_cancer(query, context)

        # BPH / enlarged prostate
        if any(term in query_lower for term in ["bph", "benign prostatic hyperplasia", "enlarged prostate",
                                                   "prostate enlargement", "difficulty starting", "poor flow",
                                                   "frequency", "urgency", "nocturia", "turp"]):
            return self._handle_bph(query, context)

        # Prostatitis
        if any(term in query_lower for term in ["prostatitis", "prostate infection", "chronic pelvic pain",
                                                   "chronic prostatitis", "acute prostatitis"]):
            return self._handle_prostatitis(query, context)

        # Elevated PSA
        if any(term in query_lower for term in ["elevated psa", "raised psa", "high psa", "psa level",
                                                   "psa test", "psa result"]):
            return self._handle_psa(query, context)

        # BLADDER CONDITIONS

        # Bladder cancer
        if any(term in query_lower for term in ["bladder cancer", "bladder tumour", "transurethral",
                                                   "tur bladder", "bladder tumor"]):
            return self._handle_bladder_cancer(query, context)

        # Haematuria (blood in urine)
        if any(term in query_lower for term in ["haematuria", "hematuria", "blood in urine", "bloody urine",
                                                   "red urine", "urine blood"]):
            return self._handle_haematuria(query, context)

        # Urinary tract infection
        if any(term in query_lower for term in ["uti", "urinary tract infection", "cystitis", "bladder infection",
                                                   "urine infection", "burning urine", "dysuria"]):
            return self._handle_uti(query, context)

        # MEN'S HEALTH

        # Erectile dysfunction
        if any(term in query_lower for term in ["erectile dysfunction", "ed", "impotence", "erection problem",
                                                   "viagra", "sildenafil", "tadalafil", "cialis", "erection"]):
            return self._handle_erectile_dysfunction(query, context)

        # Incontinence
        if any(term in query_lower for term in ["incontinence", "leaking urine", "urine leakage", "stress incontinence",
                                                   "urge incontinence", "overflow incontinence", "pad"]):
            return self._handle_incontinence(query, context)

        # TESTICULAR CONDITIONS

        # Testicular pain/lump
        if any(term in query_lower for term in ["testicular pain", "testicle pain", "testicular lump",
                                                   "testicle lump", "testicular mass", "epididymitis",
                                                   "orchitis", "varicocele", "hydrocele"]):
            return self._handle_testicular_condition(query, context)

        # PAEDIATRIC UROLOGY

        # Undescended testis
        if any(term in query_lower for term in ["undescended testis", "undescended testicle", "cryptorchidism",
                                                   "testicle not descended"]):
            return self._handle_undescended_testis(query, context)

        # Hypospadias
        if any(term in query_lower for term in ["hypospadias", "urethral opening", "penis opening"]):
            return self._handle_hypospadias(query, context)

        # GENERAL UROLOGY

        # General urology query
        return self._handle_general_urology(query, context)

    def _handle_testicular_torsion(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle testicular torsion - surgical emergency"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**TESTICULAR TORSION - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Refer to EMERGENCY DEPARTMENT immediately**
- **Time to detorsion is critical** - salvage rate decreases after 6 hours
- **DO NOT delay for imaging if clinical suspicion is high**

**TYPICAL PRESENTATION:**
- Acute onset severe testicular pain (usually <6 hours duration)
- Nausea and vomiting (common)
- Affected testis: high-riding, horizontal, tender, swollen
- Absent cremasteric reflex on affected side
- Prehn's sign negative (pain does NOT improve with elevation)

**DIFFERENTIAL DIAGNOSIS:**
- Epididymo-orchitis (usually more gradual, prehn's sign positive, cremasteric reflex present)
- Torsion of testicular appendage
- Testicular trauma
- Inguinal hernia

**INVESTIGATIONS (if time permits):**
- **Ultrasound Doppler** is gold standard
  - Torsion: absent/flow on affected side
  - Epididymo-orchitis: increased flow
- **DO NOT delay treatment for imaging** if clinical suspicion is high

**TREATMENT:**
1. **Emergency surgical exploration** via scrotal approach
2. **Manual detorsion** (if expertise available) - "open book" maneuver (laterally to medially)
   - Only as temporizing measure - surgery still required
3. **Orochiopexy** (fixation) of both testes (contralateral at risk)
4. **If necrotic**: orchidectomy (removal)

**TIME CRITICAL:**
- <6 hours: ~90-100% salvage rate
- 6-12 hours: ~50-70% salvage rate
- >24 hours: <10% salvage rate

**Sources:** EAU Guidelines on Paediatric Urology, BAUS Standards"""

        )

    def _handle_priapism(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle priapism - urological emergency"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**PRIAPISM - UROLOGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Refer to EMERGENCY DEPARTMENT immediately**
- **Persistent erection >4 hours requires urgent treatment**
- **Goal: Detumescence within 4-6 hours to prevent permanent impotence**

**TYPES:**

1. **Ischaemic (Low-flow) Priapism** - EMERGENCY (95% of cases)
   - Pathology: venous outflow obstruction
   - Presentation: painful rigid erection, corpus cavernosum rigid, spongiosum soft
   - Causes: Sickle cell disease (34%), intracavernosal injections, trauma, medications
   - **Treatment urgent:**
     - Aspiration of corpus cavernosum
     - Irrigation with phenylephrine
     - If fails: surgical shunt procedure

2. **Arterial (High-flow) Priapism** - Not usually emergency
   - Pathology: uncontrolled arterial inflow (usually perineal trauma)
   - Presentation: painless, partially rigid erection
   - Treatment: observation, selective embolisation

**IMMEDIATE MANAGEMENT:**
1. **History:** Duration, trauma, sickle cell disease, medications (PDE5 inhibitors, trazodone, etc.)
2. **Examination:** corpora cavernosa rigidity, spongiosum involvement
3. **Blood gas:** cavernosal blood sample (ischaemic: dark, low pO2, low pH)
4. **Haemoglobin electrophoresis:** if sickle cell suspected

**TREATMENT STEPS (Ischaemic):**
1. **Aspiration** - 21G needle, aspirate 20-30ml blood
2. **Irrigation** - with phenylephrine ( diluted to 1mg/ml, 1ml every 3-5 minutes)
3. **If no detumescence:** surgical shunt (cavernoglanular, cavernospongiosal)
4. **Treat underlying cause**

**COMPLICATIONS if delayed:**
- Corporal fibrosis
- Permanent erectile dysfunction
- Penile shortening

**Sources:** EAU Guidelines on Sexual and Reproductive Health, AUA Priapism Guidelines"""

        )

    def _handle_fournier_gangrene(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle Fournier's gangrene - surgical emergency"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**FOURNIER'S GANGRENE - SURGICAL EMERGENCY**

**IMMEDIATE ACTION REQUIRED:**
- **Refer to EMERGENCY DEPARTMENT immediately**
- **Necrotising fasciitis of perineum/genitalia**
- **High mortality (20-40%) if not treated aggressively**

**RISK FACTORS:**
- Diabetes mellitus (60-70% of cases)
- Alcoholism
- Immunosuppression
- Obesity
- Age >50
- Perineal/genital trauma/surgery

**TYPICAL PRESENTATION:**
- Perineal/scrotal pain (often severe) + swelling
- Erythema progressing to necrosis (purple/black discoloration)
- Crepitus (gas in tissues) on palpation
- Fever and systemic signs of sepsis
- May have foul-smelling discharge

**PATHOGENS:** usually polymicrobial:
- Aerobic: E. coli, Klebsiella, Proteus, Staphylococcus, Streptococcus
- Anaerobic: Bacteroides, Clostridium, Peptostreptococcus

**INVESTIGATIONS:**
- **CBC** - leukocytosis
- **CRP/Elevated** - inflammatory markers
- **Blood cultures** before antibiotics
- **Wound swab** for culture
- **CT scan** - assess extent (showing gas, fascial thickening)
- **DO NOT delay for imaging** if clinical diagnosis clear

**TREATMENT:**
1. **Aggressive fluid resuscitation**
2. **Broad-spectrum antibiotics immediately:**
   - Ceftriaxone 2g IV + Metronidazole 500mg IV + Gentamicin
   - Or Meropenem 1g IV TDS
3. **Emergency surgical debridement:**
   - Wide excision of all necrotic tissue
   - May require orchidectomy (testes usually spared due to separate blood supply)
   - May require colostomy if rectal involvement
4. **Repeat debridements** in theatre (often daily)
5. **Wound care** - negative pressure dressing, dressing changes
6. **Reconstruction** - skin grafting once infection controlled

**PROGNOSTIC INDICATORS (Fournier's Gangrene Severity Index):**
- Age, temperature, heart rate, respiratory rate, sodium, potassium, creatinine, Hb, WBC, bicarbonate
- Higher score = worse prognosis

**Sources:** EAU Guidelines on Urological Infections, BAUS Standards"""

        )

    def _handle_acute_retention(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle acute urinary retention"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**ACUTE URINARY RETENTION - URGENT**

**IMMEDIATE ACTION:**
- **Catheterise within 1-2 hours** to prevent permanent bladder damage
- **If cannot pass catheter: URGENT urology referral**

**TYPICAL PRESENTATION:**
- Sudden inability to pass urine
- Suprapubic pain (often severe)
- Distended bladder (palpable/percussible)
- May have overflow incontinence (dribbling)

**CAUSES:**

**MALE (Common):**
1. **BPH** with acute retention (most common)
2. Acute prostatitis
3. Prostate cancer
4. Constipation/fecal impaction
5. Medications (anticholinergics, sympathomimetics, opioids)
6. Postoperative (especially pelvic surgery, spinal anesthesia)
7. Urethral stricture
8. Calculus/stone

**FEMALE:**
1. Pelvic organ prolapse
2. Constipation/fecal impaction
3. Medications
4. Neurological causes (spinal cord compression, cauda equina)
5. Urethral diverticulum
6. Severe vaginal atrophy

**INVESTIGATIONS:**
1. **Bladder scan** or post-void residual (confirm retention)
2. **Urinalysis** - rule out UTI
3. **Serum creatinine** - assess renal function
4. **PSA** (if not done recently)
5. **CT abdomen/pelvis** if obstructing stone suspected

**MANAGEMENT:**

1. **Immediate catheterisation:**
   - **Urethral catheter (16-18Fr)** - first line
   - If fails: **Suprapubic catheter** (SPC)
   - If cannot place SPC: URGENT urology referral

2. **Trial without catheter (TWOC):**
   - After 2-3 days (once cause addressed)
   - Remove catheter, monitor for voiding
   - 50-70% succeed in BPH-related retention
   - If fails: long-term catheter or TURP

3. **Address underlying cause:**
   - BPH: alpha-blocker (tamsulosin) ± 5-alpha reductase inhibitor
   - Constipation: laxatives, enema
   - Infection: treat UTI
   - Medication review

**COMPLICATIONS if delayed:**
- Bladder decompression (may cause post-obstructive diuresis)
- Permanent detrusor damage
- Renal impairment
- Bladder rupture (rare)

**Sources:** NICE NG123, BAUS Guidelines on Acute Urinary Retention""",
            metadata={
                "urgency": "urgent",
                "condition": "acute_urinary_retention",
                "time_to_catheter": "1-2_hours"
            }
        )

    def _handle_clot_retention(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle clot retention"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**CLOT RETENTION - URGENT**

**IMMEDIATE ACTION:**
- **Urgent catheterisation** to relieve bladder outflow obstruction
- **Three-way catheter with bladder irrigation**
- **Urgent urology referral**

**TYPICAL PRESENTATION:**
- Heavy haematuria with clot passage
- Inability to pass urine due to clot obstruction
- Suprapubic pain and distended bladder
- May be hypotensive if significant blood loss

**CAUSES:**
- Bladder cancer/TCC
- Prostate cancer
- BPH with vascular congestion
- Post-biopsy bleeding
- Coagulopathy/anticoagulation
- Radiation cystitis
- Severe UTI

**IMMEDIATE MANAGEMENT:**

1. **Large bore (20-22Fr) three-way catheter:**
   - Insert carefully (may be difficult due to clots)
   - If cannot pass: use larger size or guidewire
   - If still fails: suprapubic catheter

2. **Bladder irrigation:**
   - Normal saline via irrigation port
   - Run freely until output clears
   - May need hand irrigation (syringe) to evacuate clots

3. **Monitor:**
   - Vital signs (hypovolemia)
   - Haemoglobin
   - Clot retention recurrence

4. **Treat underlying cause:**
   - Stop anticoagulation if safe
   - Correct coagulopathy
   - Tranexamic acid (caution in haematuria - may increase clot formation)
   - Urgent cystoscopy for bladder washout/clot evacuation

**INVESTIGATIONS:**
- FBC (haemoglobin)
- Coagulation profile
- Renal function (creatinine)
- CT urogram (once stable)
- Cystoscopy (to identify bleeding source)

**Sources:** BAUS Guidelines on Haematuria, EAU Guidelines on Urological Trauma""",
            metadata={
                "urgency": "urgent",
                "condition": "clot_retention",
                "intervention": "catheterisation"
            }
        )

    def _handle_kidney_stone(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle kidney stone/renal colic"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**KIDNEY STONE (NEPHROLITHIASIS/URETEROLITHIASIS)**

**PRESENTATION:**
- Severe colicky flank pain (loin to groin)
- Nausea and vomiting
- Haematuria (microscopic or gross)
- May have urinary symptoms (frequency, urgency)
- Restless (cannot get comfortable)

**IMMEDIATE MANAGEMENT:**

1. **Analgesia:**
   - **NSAIDs first line:** Diclofenac 75mg IM/IV or Ibuprofen 400mg PO
   - **Opioids** if no response: Morphine 10mg IV/IM
   - **Paracetamol** 1g PO/IV
   - **Anti-emetics** if vomiting: Metoclopramide 10mg IV/IM or Ondansetron 4mg IV

2. **IV fluids** if dehydrated

3. **Investigations:**
   - **CT KUB (CT of kidneys, ureters, bladder)** - gold standard
   - **Urinalysis** - haematuria, pH, crystals
   - **Serum creatinine** - renal function
   - **Serum calcium** - hyperparcaemia
   - **Urine culture** if infection suspected

**STONE CLASSIFICATION:**

**By size (ureteric):**
- <5mm: 80-90% spontaneous passage
- 5-10mm: 50% spontaneous passage
- >10mm: <10% spontaneous passage (need intervention)

**By location:**
- Proximal ureter: harder to pass
- Mid ureter: intermediate
- Distal ureter: easier to pass

**INDICATIONS FOR ADMISSION:**
- Single functioning kidney
- Renal transplant kidney
- Uncontrolled pain
- AKI (elevated creatinine)
- Fever/UTI (sepsis risk)
- Pregnancy

**TREATMENT OPTIONS:**

**Conservative (observation):**
- <10mm stone, no complication
- Tamsulosin 400mcg daily (medical expulsive therapy)
- Strain urine to retrieve stone for analysis
- Follow-up imaging in 2-4 weeks

**Intervention (if fails conservative or complications):**

1. **ESWL (Extracorporeal Shock Wave Lithotripsy):**
   - For renal stones <20mm, proximal ureteric <10mm
   - Non-invasive, outpatient
   - Success: 60-80% depending on stone composition

2. **Ureteroscopy + Laser Lithotripsy:**
   - For ureteric stones
   - Endoscopic removal with laser fragmentation
   - Success: 90%+
   - May require JJ stent post-procedure

3. **PCNL (Percutaneous Nephrolithotomy):**
   - For large renal stones >20mm
   - Direct removal through tract in kidney
   - Success: 90%+

**STONE PREVENTION:**
- Increase fluid intake (>2L/day)
- Low sodium diet
- Low animal protein diet
- Calcium intake normal (don't restrict unless hypercalciuria)
- DASH diet

**SPECIFIC PREVENTION:**
- Calcium stones: Thiazide diuretic, low sodium, normal calcium
- Uric acid stones: Allopurinol, urine alkalinisation (potassium citrate)
- Struvite (infection) stones: treat UTI, complete stone removal
- Cystine stones: high fluid, alkalinisation, chelating agents

**Sources:** EAU Guidelines on Urolithiasis, NICE NG118""",
            metadata={
                "urgency": "urgent",
                "condition": "renal_colic",
                "pain_management": "priority"
            }
        )

    def _handle_prostate_cancer(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle prostate cancer"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**PROSTATE CANCER**

**RISK FACTORS:**
- Age >50 (rare <50)
- Ethnicity: African-Caribbean (higher risk)
- Family history (first-degree relative)
- BRCA2 gene mutations
- Obesity (possible link)

**SCREENING CONTROVERSY:**
- No universal screening programme
- PSA testing available via "informed choice" programme
- Discuss benefits/harms before testing

**DIAGNOSTIC PATHWAY:**

**1. Suspicious PSA:**
- Age-specific PSA:
  - <50: PSA <2.5 ng/mL
  - 50-59: PSA <3.5 ng/mL
  - 60-69: PSA <4.5 ng/mL
  - 70-79: PSA <6.5 ng/mL
- Free/total PSA ratio if PSA 4-10 ng/mL
- PSA velocity/rise over time

**2. MRI Prostate (mpMRI):**
- Multiparametric MRI (T2, DWI, DCE)
- PI-RADS scoring 1-5
- PI-RADS 4-5: high suspicion, proceed to biopsy
- PI-RADS 3: equivocal, consider other factors

**3. Prostate Biopsy:**
- Transperineal template biopsy (now standard)
- Transrectal ultrasound (TRUS) guided (less common now)
- 12+ cores sampled
- Histology: Gleason score (Grade Group 1-5)

**STAGING:**

**TNM Staging:**
- T1: clinically not palpable
- T2: confined to prostate
- T3: extracapsular extension
- T4: fixed to adjacent structures

**Risk Stratification (NICE):**
- **Low risk:** T1-T2a, Gleason ≤6 (Grade Group 1), PSA <10
- **Intermediate risk:** T2b, Gleason 7 (Grade Group 2-3), PSA 10-20
- **High risk:** T2c-T4, Gleason 8-10 (Grade Group 4-5), PSA >20

**TREATMENT OPTIONS:**

**Low-risk (localized):**
1. **Active surveillance** - monitor with PSA, repeat MRI, biopsy
2. **Radical prostatectomy** - surgical removal
3. **Radical radiotherapy** - external beam or brachytherapy

**Intermediate-risk (localized):**
1. **Radical prostatectomy**
2. **Radical radiotherapy** + androgen deprivation therapy (ADT)

**High-risk (localized/locally advanced):**
1. **Radical prostatectomy** + pelvic lymph node dissection
2. **Radical radiotherapy** + long-term ADT (18-36 months)
3. **ADT alone** if not fit for radical treatment

**Metastatic disease:**
- **Androgen deprivation therapy (ADT):**
  - GnRH agonists (goserelin, leuprorelin)
  - GnRH antagonists (degarelix)
  - Anti-androgens (bicalutamide)
  - Combined androgen blockade
- **Chemotherapy** (docetaxel) for castration-resistant
- **Newer agents:** Abiraterone, Enzalutamide, Rucaparib (if BRCA mutation)

**FOLLOW-UP:**
- PSA monitoring every 3-6 months
- Digital rectal examination
- Imaging if PSA rises
- Watch for treatment side effects:
  - Surgery: erectile dysfunction, urinary incontinence
  - Radiotherapy: urinary symptoms, bowel symptoms, erectile dysfunction
  - ADT: hot flushes, osteoporosis, metabolic syndrome, gynecomastia

**Sources:** NICE NG131, EAU Guidelines on Prostate Cancer, ASCO Guidelines""",
            metadata={
                "sources": ["NICE NG131", "EAU Guidelines", "ASCO"]
            }
        )

    def _handle_bph(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle benign prostatic hyperplasia"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**BENIGN PROSTATIC HYPERPLASIA (BPH)**

**PATHOPHYSIOLOGY:**
- Age-related enlargement of transition zone prostate
- Can cause bladder outflow obstruction (BOO)
- Affects 50% men age 60, 90% age 85

**SYMPTOMS (LUTS - Lower Urinary Tract Symptoms):**

**Voiding symptoms (obstructive):**
- Hesitancy (difficulty starting)
- Poor stream
- Straining to void
- Intermittent stream
- Terminal dribbling
- Feeling of incomplete emptying

**Storage symptoms (irritative):**
- Frequency (>8 times/day)
- Nocturia (>1 time/night)
- Urgency
- Urgency incontinence

**ASSESSMENT:**

**1. History:**
- IPSS (International Prostate Symptom Score)
- Bothersome score
- Red flags: haematuria, pain, weight loss (prostate cancer)

**2. Examination:**
- Abdominal: palpable bladder (retention)
- DRE: prostate size, consistency, nodules (cancer?)
- Neurological: sacral sensation, anal tone (neuropathic bladder)

**3. Investigations:**
- **Urinalysis** - rule out infection, haematuria
- **PSA** - if not done, or if change in symptoms
- **Renal function** - creatinine
- **Post-void residual** - bladder scan (if retention suspected)
- **Uroflowmetry** - peak flow rate <15 mL/s suggests obstruction
- **Ultrasound** - prostate size, kidneys, bladder wall thickness

**MANAGEMENT:**

**Mild symptoms (IPSS <8):**
- Watchful waiting
- Lifestyle modifications:
  - Fluid management (reduce evening fluids)
  - Avoid caffeine, alcohol
  - Double voiding
  - Bladder training

**Moderate-Severe symptoms (IPSS ≥8):**

**Medical management (first line):**
1. **Alpha-blockers** (relax smooth muscle):
   - Tamsulosin 400mcg daily
   - Alfuzosin 10mg daily
   - Doxazosin 4mg daily
   - Onset: 2-4 weeks
   - Side effects: dizziness, orthostatic hypotension, retrograde ejaculation

2. **5-alpha reductase inhibitors** (shrink prostate):
   - Finasteride 5mg daily
   - Dutasteride 0.5mg daily
   - Onset: 3-6 months
   - Indicated: prostate >40g or PSA >1.4
   - Side effects: decreased libido, erectile dysfunction

3. **Combination therapy** (both drugs):
   - For larger prostates >40g
   - Most effective for symptom relief and preventing progression

**Surgical management (if medical therapy fails, complications, or patient preference):**

1. **TURP (Transurethral Resection of Prostate)** - gold standard
   - Endoscopic resection via urethra
   - 1-3 night hospital stay
   - Success: 80-90%
   - Complications: bleeding, retrograde ejaculation (70%), erectile dysfunction (5-10%), incontinence (1-3%)

2. **Holmium laser enucleation (HoLEP)** - for large prostates >80g
3. **Prostate Urethral Lift (PUL)** - minimally invasive
4. **Water vapor thermal therapy (Rezūm)** - minimally invasive
5. **Simple prostatectomy** - open surgery for very large prostates >100g

**INDICATIONS FOR SURGERY:**
- Recurrent urinary retention
- refractory urinary retention (after trial without catheter fails)
- Recurrent UTIs
- Haematuria due to BPH
- Bladder stones
- Renal impairment due to BPH
- Failed medical therapy

**RED FLAGS (refer urgently):**
- Haematuria (visible)
- Palpable malignant-feeling prostate on DRE
- Bone pain (metastases)
- Unexplained weight loss

**Sources:** NICE NG123, EAU Guidelines on Management of Non-Neurogenic Male LUTS"""
        )

    def _handle_prostatitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle prostatitis"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**PROSTATITIS**

**CLASSIFICATION (NIH Classification):**

**1. Acute Bacterial Prostatitis:**
- **SYSTEMIC ILLNESS - requires urgent treatment**
- Presentation: fever, chills, malaise, perineal/suprapubic pain, urinary symptoms
- EPS: abundant leukocytes, bacteria
- **Management:**
  - **Admit if septic** or cannot tolerate oral
  - **Ciprofloxacin 500mg BD** (or Levofloxacin 500mg OD) for 4 weeks
  - **If severe/septic:** Ceftriaxone 2g IV → oral when improved
  - **Analgesia** (NSAIDs)
  - **Alpha-blocker** if urinary retention (tamsulosin)
  - **Avoid prostate massage** (can cause bacteraemia)

**2. Chronic Bacterial Prostatitis:**
- Recurrent UTIs with same organism
- Perineal/discomfort, mild urinary symptoms
- EPS: leukocytes, culture-positive
- **Management:**
  - **Ciprofloxacin 500mg BD** for 4-6 weeks
  - **Or:** Levofloxacin 500mg OD
  - If fails: based on culture and sensitivity
  - Consider TMP-SMX if quinolone resistance

**3. Chronic Pelvic Pain Syndrome (CPPS) - 90% of prostatitis cases:**
- **No proven infection**
- **CPPS IIIA:** inflammatory (leukocytes in EPS)
- **CPPS IIIB:** non-inflammatory (no leukocytes)
- Presentation: chronic pelvic/perineal pain, urinary symptoms, sexual dysfunction
- **Management (multimodal):**

  a) **Alpha-blockers** (tamsulosin 400mcg) - 4-12 weeks trial
  b) **NSAIDs** for pain
  c) **Pregabalin/Gabapentin** for neuropathic pain
  d) **Amitriptyline** 10-25mg at night
  e) **Pelvic floor physiotherapy**
  f) **Biofeedback/relaxation techniques**
  g) **Psychological support** (depression, anxiety common)
  h) **5-alpha reductase inhibitor** (finasteride) - may help

**4. Asymptomatic Inflammatory Prostatitis:**
- Incidental finding (elevated PSA, leukocytes in EPS)
- No treatment required

**DIAGNOSTIC TESTS:**

**Expressed Prostatic Secretion (EPS):**
- Post-prostatic massage fluid
- Microscopy: leukocytes (>10 WBC/hpf suggests inflammation)
- Culture: bacteria identification

**Urine culture:**
- Pre-massage urine (VB1)
- Post-massage urine (VB3)
- Prostatic fluid (EPS)

**Additional tests:**
- Urinalysis and culture
- STI screen (Chlamydia, Gonorrhoea) if young sexually active
- PSA (elevated in prostatitis - repeat after 6-8 weeks)

**RED FLAGS:**
- Acute prostatitis with sepsis → admit
- Unable to pass urine → catheterise cautiously (risk of seeding)
- Prostate abscess suspected (fluctuant, boggy) → URGENT urology referral

**Sources:** EAU Guidelines on Urological Infections, NICE NG110"""
        )

    def _handle_psa(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle elevated PSA"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**ELEVATED PSA (Prostate-Specific Antigen)**

**PSA BASICS:**
- Produced by prostate epithelial cells
- Normal range: varies by age (no absolute cut-off)
- **Age-specific PSA:**
  - <50 years: <2.5 ng/mL
  - 50-59 years: <3.5 ng/mL
  - 60-69 years: <4.5 ng/mL
  - 70-79 years: <6.5 ng/mL

**CAUSES OF ELEVATED PSA:**

**1. Benign conditions (most common):**
- BPH (enlarged prostate)
- Prostatitis (infection)
- Urinary retention
- Ejaculation (abstain 48h before test)
- Digital rectal examination (wait 1 week)
- Prostate biopsy (wait 6-8 weeks)

**2. Prostate cancer:**
- Not all prostate cancers elevate PSA
- Not all elevated PSA = cancer
- PSA velocity/rise over time is important

**3. Other factors:**
- Age (PSA increases with age)
- Ethnicity (higher in African-Caribbean)
- Medications (5-alpha reductase inhibitors lower PSA)
- vigorous exercise (cycling)

**INVESTIGATION OF ELEVATED PSA:**

**Repeat PSA** (if first elevated result):
- Wait 6-8 weeks if recent DRE, prostatitis, UTI, ejaculation
- Ensure no active infection

**Additional PSA measures:**

**1. Free/Total PSA Ratio:**
- PSA exists in free and bound forms
- Lower free PSA (<10-15%) = higher cancer risk
- Useful if total PSA 4-10 ng/mL

**2. PSA Density (PSAD):**
- PSA divided by prostate volume
- >0.15 ng/mL/cc suggests cancer

**3. PSA Velocity:**
- Rate of rise over time
- >0.35 ng/mL/year suggests cancer

**4. PSA Doubling Time:**
- Time for PSA to double
- <3 years = aggressive disease

**IMAGING:**

**mpMRI Prostate (Multiparametric MRI):**
- First-line investigation for elevated PSA
- PI-RADS scoring 1-5:
  - PI-RADS 1-2: clinically significant cancer unlikely
  - PI-RADS 3: equivocal
  - PI-RADS 4-5: high suspicion
- Guides need for biopsy

**BIOPSY:**
- Consider if:
  - PSA > age-specific threshold
  - mpMRI PI-RADS 4-5
  - PSA velocity/PSA density concerning
  - Abnormal DRE (nodule, hard prostate)
- Transperineal template biopsy (now standard)

**RED FLAGS FOR URGENT REFERRAL:**
- PSA >100 ng/mL (very high risk of metastatic)
- Palpable nodule on DRE
- Bone pain (pathological fracture risk)
- Weight loss, lethargy (metastatic)

**Sources:** NICE NG131, EAU Guidelines on Prostate Cancer"""
        )

    def _handle_bladder_cancer(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle bladder cancer"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**BLADDER CANCER (Transitional Cell Carcinoma - TCC)**

**RISK FACTORS:**
- Smoking (50% of cases) - strongest risk factor
- Occupational exposure (aromatic amines, dyes, rubber, petroleum)
- Age >60
- Male > Female (3:1)
- Schistosomiasis (endemic areas)
- Previous bladder cancer (recurrence risk 50-70%)
- Chemotherapy (cyclophosphamide)
- Radiation therapy

**PRESENTATION:**
- **Painless visible haematuria** (70-90% of cases) - **REFER URGENT**
- Microscopic haematuria (detected on dipstick)
- Urinary symptoms (frequency, urgency, dysuria) - may mimic UTI
- Pelvic pain (advanced disease)
- Weight loss, lethargy (metastatic)

**INVESTIGATION:**

**1. Urinalysis and Microscopy:**
- Haematuria confirmed
- Cytology (malignant cells) - low sensitivity

**2. Imaging:**
- **CT Urogram** (CT intravenous urogram) - gold standard
  - Visualises entire urinary tract (kidneys, ureters, bladder)
  - Detects filling defects, masses, obstruction
- **Ultrasound** if CT contraindicated (renal impairment, contrast allergy)
- **Chest X-ray** (if muscle-invasive disease suspected)

**3. Cystoscopy:**
- **Gold standard for diagnosis**
- Visualise bladder, take biopsies
- Flexible cystoscopy (outpatient, local anaesthetic)
- Rigid cystoscopy (general anaesthetic, allows resection)

**PATHOLOGY:**
- **TCC (Urothelial carcinoma)** - 90-95%
- Squamous cell carcinoma - 5% (associated with schistosomiasis, chronic irritation)
- Adenocarcinoma - <2%

**STAGING (TNM):**

**Ta:** Papillary, non-invasive
**T1:** Invades lamina propria (submucosa)
**T2:** Invades muscle (detrusor muscle)
**T3:** Invades perivesical fat
**T4:** Invades adjacent structures (prostate, vagina, pelvic wall)

**TREATMENT:**

**Non-Muscle-Invasive (Ta, T1, CIS):**

1. **TURBT (Transurethral Resection of Bladder Tumour):**
   - Endoscopic removal via urethra
   - Diagnostic and therapeutic

2. **Intravesical therapy:**
   - **Mitomycin C** (chemotherapy) - single dose post-TURBT
   - **BCG (Bacillus Calmette-Guérin)** - immunotherapy
     - Induction course: weekly ×6 weeks
     - Maintenance: weekly ×3 weeks at 3, 6, 12 months
     - Reduces recurrence and progression

3. **Surveillance cystoscopy:**
   - 3-monthly for 2 years
   - 6-monthly for next 2 years
   - Yearly thereafter

**Muscle-Invasive (T2+):**

1. **Radical Cystectomy:**
   - Removal of bladder, prostate, seminal vesicles (men)
   - Removal of bladder, uterus, adnexa, anterior vaginal wall (women)
   - Pelvic lymph node dissection
   - **Urinary diversion:**
     - Ileal conduit (urostomy bag)
     - Neo-bladder (continent reservoir)
     - Continent cutaneous diversion

2. **Radical Radiotherapy:**
   - Alternative to surgery
   - Bladder preservation
   - Combined with chemotherapy (radiosensitiser)

3. **Chemotherapy:**
   - Neoadjuvant (before surgery): MVAC or CMV
   - Palliative (metastatic disease)

**FOLLOW-UP:**
- Cystoscopy surveillance (lifelong)
- CT imaging (upper tract surveillance)
- Urine cytology
- Monitor for recurrence (50-70% risk)

**PROGNOSIS:**
- Non-muscle invasive: 5-year survival 80-90%
- Muscle-invasive: 5-year survival 50-60%
- Metastatic: 5-year survival <10%

**RED FLAGS:**
- Visible haematuria → **URGENT urology referral**
- clot retention → **urgent admission**
- Weight loss, bone pain (metastatic)

**Sources:** NICE NG140, EAU Guidelines on Bladder Cancer"""
        )

    def _handle_haematuria(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle haematuria"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**HAEMATURIA (Blood in Urine)**

**DEFINITIONS:**
- **Macroscopic (visible) haematuria:** Visible red/brown urine
- **Microscopic haematuria:** Detected on dipstick/microscopy

**VISIBLE HAEMATURIA - URGENT REFERRAL**

**CAUSES:**

**1. Urological malignancy (10-20%):**
- Bladder cancer (TCC) - most common serious cause
- Renal cell carcinoma
- Prostate cancer
- Upper tract TCC (ureter, renal pelvis)

**2. Benign urological causes:**
- UTI (cystitis, pyelonephritis)
- Stones (renal, ureteric, bladder)
- BPH / prostate enlargement
- Trauma (catheterisation, injury)
- Exercise-induced (running)
- Recent urological procedure/surgery

**3. Medical causes:**
- Anticoagulation/antiplatelets (warfarin, DOACs, clopidogrel)
- Coagulopathy (bleeding disorder)
- Glomerular disease (glomerulonephritis)
- Menstruation contamination

**ASSESSMENT:**

**History:**
- Duration, frequency
- Pain? (loin pain = stone; painless = cancer until proven)
- Clots? (suggests bladder source)
- Storage LUTS? (BPH, bladder cancer)
- Smoking history? (bladder cancer risk)
- Occupational exposures? (aromatic amines)
- Recent exercise? (running)
- Medications? (anticoagulation)
- Recent catheterisation/procedure?

**Examination:**
- Abdominal: masses, palpable bladder (retention)
- DRE: prostate (enlargement, nodules, malignancy)
- Suprapubic tenderness (UTI, bladder stone)

**INVESTIGATIONS:**

**1. Urinalysis and Microscopy:**
- Confirm haematuria
- Look for RBC casts (glomerular)
- Look for WBCs, nitrites (infection)
- Protein (glomerular disease)

**2. Urine Cytology:**
- Malignant cells
- Low sensitivity but high specificity

**3. Blood tests:**
- FBC (anaemia)
- Renal function (creatinine, eGFR)
- Coagulation profile (if anticoagulated)
- PSA (men >50, or if prostate concerns)

**4. Imaging:**
- **CT Urogram** (first-line for visible haematuria)
  - Visualises kidneys, ureters, bladder
  - Detects tumours, stones, obstruction
- **Ultrasound** if CT contraindicated (renal impairment)

**5. Cystoscopy:**
- **Mandatory for visible haematuria**
- Visualise bladder, urethra
- Biopsies if abnormalities
- Flexible cystoscopy (outpatient)

**MICROSCOPIC HAEMATURIA:**
- Asymptomatic: repeat in 6 weeks (exclude transient causes)
- Persistent: refer for imaging (CTU or ultrasound)
- Cystoscopy if risk factors (smoker, >50, persistent)

**RED FLAGS (urgent referral):**
- Visible haematuria in >45 year old
- Visible haematuria + smoking history
- Visible haematuria + palpable mass on examination
- Visible haematuria + clot retention
- Visible haematuria + unexplained weight loss

**Sources:** NICE NG140, BAUS Guidelines on Haematuria"""
        )

    def _handle_uti(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle urinary tract infection"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**URINARY TRACT INFECTION (UTI)**

**CLASSIFICATION:**

**Women:**
- **Lower UTI (Cystitis):** dysuria, frequency, urgency, suprapubic pain
- **Upper UTI (Pyelonephritis):** fever, flank pain, systemic illness
- **Recurrent UTI:** ≥3 infections in 12 months

**Men:**
- **UTI is ALWAYS abnormal** (until proven otherwise)
- **Always investigate for underlying cause**

**CAUSES:**
- **E. coli** (80% of community-acquired)
- **Proteus mirabilis** (stones)
- **Klebsiella**
- **Pseudomonas** (catheter-associated)
- **Enterococcus**
- **Staphylococcus saprophyticus** (young women)

**RISK FACTORS:**
- Female (short urethra)
- Sexual activity
- Pregnancy
- Diabetes
- Catheterisation
- Obstruction (stones, BPH)
- Immunosuppression

**ASYMPTOMATIC BACTERIURIA:**
- Positive urine culture WITHOUT symptoms
- **DO NOT treat** (except pregnancy, urological procedures)
- Does NOT progress to symptomatic UTI

**UNCOMPLICATED CYSTITIS (Women):**

**Diagnosis:**
- Dipstick: nitrites, leukocytes
- **Do NOT send urine culture** for uncomplicated cases

**Treatment (3 days):**
- **Nitrofurantoin 100mg MR BD** (first line)
- **Or:** Trimethoprim 200mg BD (if local resistance <20%)
- **Or:** Fosfomycin 3g single dose

**Recurrent UTI (Women):**
- UTI ≥3 times/year
- **Investigate:** ultrasound, cystoscopy (if risk factors)
- **Prevention:**
  - Post-coital antibiotics (Nitrofurantoin 50mg or Trimethoprim 100mg)
  - Daily antibiotic prophylaxis (6 months trial)
  - Vaginal oestrogen (post-menopausal)
  - Cranberry products (controversial)

**COMPLICATED UTI:**

**Definition:**
- Men, pregnancy, catheter-associated, obstruction, immunosuppression, renal impairment

**Management:**
- **Send urine culture** (before antibiotics)
- **Treat for 7-14 days**
- **Antibiotics:**
  - Ciprofloxacin 500mg BD
  - Or Levofloxacin 500mg OD
  - Or Cefalexin 500mg TDS

**PYELONEPHRITIS (Upper UTI):**
- Fever + flank pain + systemic illness
- **Treat for 10-14 days**
- **Admit if:** septic, unable to tolerate oral, pregnant, obstruction
- **IV antibiotics** (Ceftriaxone 2g OD or Gentamicin)

**UTI IN MEN:**
- **Always send urine culture**
- **Treat for 7-14 days**
- **Investigate:** refer for ultrasound, cystoscopy, PSA
- **Underlying causes:**
  - BPH / prostatic enlargement
  - Prostatitis
  - Urethral stricture
  - Stone

**CATHETER-ASSOCIATED UTI:**
- Treat ONLY if symptomatic
- Change catheter if present >7 days
- Send culture
- Treat based on sensitivities (often Pseudomonas, multi-resistant)

**PREGNANCY:**
- **Screen all** with urine culture at booking, 16 weeks, 28 weeks
- **Treat all bacteriuria** (reduces pyelonephritis risk)
- **Avoid:** quinolones, tetracyclines
- **Safe:** Nitrofurantoin (not at term), Cefalexin

**PREVENTION:**
- Hydration
- Void after intercourse
- Wipe front to back
- Avoid douching/spermicides
- Treat constipation
- Cranberry (may help)

**Sources:** NICE NG110, EAU Guidelines on Urological Infections"""
        )

    def _handle_erectile_dysfunction(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle erectile dysfunction"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**ERECTILE DYSFUNCTION (ED)**

**DEFINITION:**
- Inability to achieve or maintain erection sufficient for satisfactory sexual performance
- Persistent for ≥3 months

**PREVALENCE:**
- Age-dependent
- 40% men age 40
- 70% men age 70

**AETIOLOGY (Multiple factors often):**

**1. Organic (80%):**
- **Vascular:** atherosclerosis, hypertension, diabetes, smoking
- **Neurological:** diabetic neuropathy, spinal cord injury, MS, Parkinson's
- **Hormonal:** hypogonadism (low testosterone), hyperprolactinaemia, thyroid disorders
- **Anatomical:** Peyronie's disease, congenital curvature
- **Drug-induced:**
  - Antihypertensives: thiazides, beta-blockers, spironolactone
  - Antidepressants: SSRIs, TCAs
  - Antiandrogens: finasteride, bicalutamide
  - Others: opioids, anticonvulsants, H2 blockers

**2. Psychogenic (20%):**
- Performance anxiety
- Stress, depression
- Relationship issues
- Pornography-induced

**ASSESSMENT:**

**History:**
- Onset (gradual = organic; sudden = psychogenic)
- Situation (generalised vs. situational)
- Morning/night erections (present = psychogenic)
- Libido (low = hormonal)
- Risk factors: diabetes, hypertension, smoking, obesity
- Medications
- Relationship status, psychological factors

**Examination:**
- BMI, waist circumference (metabolic syndrome)
- Blood pressure
- Genitalia: Peyronie's plaques, testicular atrophy
- Neurological: perineal sensation, anal tone (S2-S4)
- Secondary sexual characteristics (hypogonadism)

**Investigations:**
- **Fasting glucose/HbA1c** (diabetes)
- **Lipids** (vascular risk)
- **Testosterone** (morning sample, repeat if low)
- **Prolactin** (if low testosterone or reduced libido)
- **PSA** (before testosterone therapy)
- **Thyroid function** (if indicated)

**MANAGEMENT (Stepwise approach):**

**Lifestyle modifications (first line for all):**
- Weight loss
- Regular exercise
- Smoking cessation
- Reduce alcohol
- Stress management

**Oral Pharmacotherapy (first line):**

**1. PDE5 inhibitors (Sildenafil, Tadalafil, Vardenafil, Avanafil):**
- **Sildenafil (Viagra) 50mg** 1h before sex (max 100mg)
- **Tadalafil (Cialis) 10mg** 30min before sex (max 20mg)
  - Daily low-dose (5mg) option available
- **Contraindicated:** Nitrates (severe hypotension)
- **Side effects:** headache, flushing, dyspepsia, visual disturbance, nasal congestion
- **Success:** 70-80%

**2. Vacuum erection devices:**
- Mechanical pump, constriction ring
- Non-invasive, no drug interactions
- Success: 50-80%

**3. Intracavernosal injections (ICI):**
- **Alprostadil** (Caverject)
- Inject into penis 10-15min before sex
- Success: 80-90%
- Side effects: priapism, pain, fibrosis

**4. Intraurethral alprostadil:**
- Medicated urethral system for erection (MUSE)
- Less effective than ICI

**5. Testosterone replacement:**
- **ONLY if hypogonadism confirmed** (low testosterone + symptoms)
- Gel, injections, patches
- Check PSA, haematocrit before and during

**6. Penile prosthesis:**
- Inflatable or malleable rods
- Last resort when other treatments fail
- High patient satisfaction (80-90%)

**7. Psychosexual therapy:**
- If psychogenic component
- Couples therapy
- CBT for performance anxiety

**REFERRAL CRITERIA:**
- Primary ED (young man)
- Curved penis (Peyronie's)
- Low testosterone
- Penile rehabilitation post-prostatectomy
- Failed PDE5 inhibitors

**Sources:** NICE NG123, EAU Guidelines on Sexual and Reproductive Health"""
        )

    def _handle_incontinence(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle urinary incontinence"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**URINARY INCONTINENCE**

**CLASSIFICATION:**

**1. Stress Urinary Incontinence (SUI):**
- Leakage with increased abdominal pressure (coughing, sneezing, exercise)
- More common in women
- Cause: urethral sphincter incompetence, pelvic floor weakness

**2. Urge Urinary Incontinence (UUI):**
- Sudden compelling desire to pass urine, unable to defer
- Associated with overactive bladder (OAB)
- Cause: detrusor overactivity

**3. Mixed Urinary Incontinence:**
- Combination of stress and urge components
- Most common type

**4. Overflow Incontinence:**
- Chronic retention, overflow leakage
- Painless bladder distension
- Cause: bladder outlet obstruction (BPH), neuropathic bladder

**5. Functional Incontinence:**
- Mobility/cognitive impairment prevents reaching toilet

**ASSESSMENT:**

**History:**
- Onset, duration, frequency
- Triggers (cough, urge)
- Fluid intake (type, amount, timing)
- Medications (diuretics, anticholinergics)
- Bowel function (constipation)
- Neurological symptoms (cauda equina, spinal cord)
- Obstetric history (parity, mode of delivery)

**Examination:**
- Abdominal: palpable bladder (retention)
- Pelvic floor assessment (cough test)
- Rectal/vaginal examination (prolapse, sphincter tone)
- Neurological: lower limb neurology, perineal sensation

**Investigations:**
- **Urinalysis** (UTI, haematuria)
- **Bladder diary** (3 days)
- **Post-void residual** (bladder scan)
- **Urodynamics** (if surgical management considered)

**MANAGEMENT:**

**Stress Urinary Incontinence:**

**Conservative (first line):**
1. **Pelvic floor muscle training (PFMT):**
   - Kegel exercises: 8-12 contractions, 3 times/day
   - Duration: 3-6 months
   - Success: 60-70%
2. **Weight loss** (if BMI >30)
3. **Vaginal cones/pessaries**

**Surgical (if conservative fails):**
1. **Mid-urethral sling (TVT/TOT):**
   - Tension-free vaginal tape
   - Retropubic (TVT) or transobturator (TOT) approach
   - Success: 80-90%
   - Complications: bladder injury (5-10%), retention, erosion
2. **Colposuspension (Burch):** open or laparoscopic
3. **Bulking agents:** periurethral injections
4. **Artificial urinary sphincter:** (severe SUI, male)

**Urge Urinary Incontinence / Overactive Bladder:**

**Conservative (first line):**
1. **Bladder training:**
   - Scheduled voiding
   - Gradually increase intervals
   - Duration: 6 weeks
2. **Pelvic floor muscle training**
3. **Lifestyle:**
   - Reduce caffeine, alcohol
   - Weight loss
   - Fluid management

**Pharmacological:**
1. **Anticholinergics:**
   - Oxybutynin, Tolterodine, Solifenacin, Darifenacin
   - Mechanism: relax detrusor muscle
   - Side effects: dry mouth, constipation, blurred vision, cognitive
   - Caution in elderly (anticholinergic burden)

2. **Mirabegron (beta-3 agonist):**
   - Alternative to anticholinergics
   - Fewer side effects
   - Contraindicated in uncontrolled hypertension

3. **Botulinum toxin A (Botox):**
   - Intradetrusor injections
   - For refractory OAB
   - Risk of retention (may need ISC)

**Overflow Incontinence:**
- Treat underlying obstruction
- Clean intermittent self-catheterisation (ISC)
- Indwelling catheter (if ISC not possible)

**MEN:**
- SUI: post-prostatectomy (radiation, sling, artificial sphincter)
- UUI: anticholinergics, Botox

**Sources:** NICE NG123, EAU Guidelines on Urinary Incontinence"""
        )

    def _handle_testicular_condition(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle testicular pain/lump"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**TESTICULAR PAIN / LUMP**

**DIFFERENTIAL DIAGNOSIS:**

**EMERGENCY:**
- **Testicular torsion** - surgical emergency

**URGENT:**
- **Epididymo-orchitis** - infection
- **Fournier's gangrene** - necrotising infection

**NON-URGENT:**
- **Testicular cancer** - urgent referral
- **Hydrocele** - fluid collection
- **Varicocele** - dilated veins
- **Epididymal cyst** - benign cyst

**ASSESSMENT:**

**History:**
- Onset, duration
- Pain (yes/no, severity)
- Trauma
- Systemic symptoms (fever, weight loss)
- Urinary symptoms (dysuria, frequency)

**Examination:**
- **Inspect:** swelling, redness, position of testis
- **Palpate:** testis (consistency, lumps), epididymis
- **Transillumination:** hydrocele (transilluminates)
- **Cremasteric reflex** (absent in torsion)
- **Prehn's sign** (pain relief with elevation = epididymitis)

**SPECIFIC CONDITIONS:**

**1. Epididymo-orchitis:**
- Infection of epididymis ± testis
- **Causes:**
  - <35: Chlamydia trachomatis, Neisseria gonorrhoeae
  - >35: E. coli, Pseudomonas (UTI organisms)
- **Treatment:**
  - <35: Doxycycline 100mg BD + Ceftriaxone 500mg IM
  - >35: Ciprofloxacin 500mg BD or Ofloxacin 200mg BD
  - Duration: 2-4 weeks
- **Supportive:** scrotal elevation, analgesia, ice packs

**2. Testicular Cancer:**
- Painless testicular lump
- Age 15-45 peak incidence
- **Risk factors:** undescended testis, previous testicular cancer, family history
- **Types:**
  - Seminoma (50%) - radiosensitive
  - Non-seminoma (50%) - teratoma, yolk sac, choriocarcinoma, embryonal
- **Investigations:**
  - **Tumour markers:** AFP, hCG, LDH
  - **Ultrasound** - solid mass = cancer until proven otherwise
  - **CT chest/abdomen/pelvis** - staging
- **Treatment:**
  - **Radical inguinal orchidectomy** (never scrotal approach)
  - Surveillance, radiotherapy, or chemotherapy (depending on stage)
  - Excellent cure rate (>95%)
- **URGENT UROLOGY REFERRAL** (within 2 weeks)

**3. Hydrocele:**
- Fluid collection around testis
- **Primary:** idiopathic
- **Secondary:** infection, tumour, trauma
- **Investigation:** ultrasound (if not transilluminating, or red flags)
- **Treatment:** observation (if small, asymptomatic), surgical repair (if large)

**4. Varicocele:**
- Dilated pampiniform plexus veins
- "Bag of worms" sensation
- Left side >90% (anatomy)
- **Complications:** infertility, testicular atrophy
- **Treatment:** observation, varicocelectomy, embolisation (if infertility or pain)

**5. Epididymal Cyst:**
- Benign cyst in epididymis
- Common, asymptomatic
- No treatment needed
- Reassurance

**RED FLAGS (urgent referral):**
- Suspected testicular cancer (solid mass)
- Testicular torsion
- Fournier's gangrene

**Sources:** EAU Guidelines on Testicular Cancer, NICE NG123"""
        )

    def _handle_undescended_testis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle undescended testis"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**UNDESCENDED TESTIS (Cryptorchidism)**

**DEFINITION:**
- Testis not located in scrotum
- **Congenital:** present at birth (3-5% full-term, 30% preterm)
- **Acquired:** previously descended, then ascends (1-2%)

**CLASSIFICATION:**
- **Palpable:** 80% (inguinal canal, superficial inguinal pouch)
- **Impalpable:** 20% (intra-abdominal, atrophic, absent)

**COMPLICATIONS IF NOT TREATED:**
- **Infertility** (reduced sperm production)
- **Testicular cancer** (3-5x increased risk)
- **Testicular torsion** (higher risk)
- **Psychological** (cosmetic concerns)

**ASSESSMENT:**

**History:**
- Birth history (prematurity)
- Previous testicular exams
- Family history

**Examination:**
- Locate testis (may need warm room, relaxed child)
- Assess size (atrophic?)
- Assess contralateral testis (compensatory hypertrophy?)
- Examine for hypospadias (disorder of sexual differentiation?)

**INVESTIGATIONS:**
- **Ultrasound** (if palpable - confirm location)
- **MRI** (if impalpable)
- **Diagnostic laparoscopy** (if impalpable, intra-abdominal)

**MANAGEMENT:**

**1. Orchidopexy (surgical fixation):**
- **Timing:** 6-12 months (optimal: 9-15 months)
- **Procedure:** testis mobilised, fixed in scrotum
- **Success:** 80-95%
- **Complications:** testicular atrophy (5%), recurrence (5%)

**2. Hormone therapy (less common):**
- hCG or GnRH
- Success: 20%
- Usually reserved for bilateral cases

**3. Orchidectomy (testis removal):**
- If post-pubertal, atrophic
- If intra-abdominal, cannot be brought down

**4. Testicular prosthesis:**
- For cosmetic reasons
- Inserted after puberty (can be earlier)

**FOLLOW-UP:**
- Annual testicular exam (cancer risk)
- Fertility assessment in adulthood
- Self-examination education

**SOURCES:** EAU Guidelines on Paediatric Urology, NICE NG195"""
        )

    def _handle_hypospadias(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle hypospadias"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**HYPOSPADIAS**

**DEFINITION:**
- Abnormal urethral opening on ventral aspect of penis
- Present at birth (congenital)
- Incidence: 1 in 250-300 male births

**CLASSIFICATION:**
- **Glanular:** urethral opening on glans (mild)
- **Coronal:** opening at coronal sulcus
- **Distal shaft:** opening on distal penis
- **Mid shaft:** opening on mid-penis
- **Proximal shaft:** opening on proximal penis
- **Penoscrotal:** opening at penoscrotal junction (severe)
- **Perineal:** opening on perineum (severe)

**ASSOCIATED FEATURES:**
- **Chordee:** ventral curvature of penis (30%)
- **Hooded prepuce:** incomplete foreskin (dorsal only)
- **Cryptorchidism:** undescended testis (10%)
- **Disorder of Sexual Development (DSD)** if severe (bilateral cryptorchidism)

**ASSESSMENT:**
- Physical exam: location of meatus, chordee, penis size
- Karyotype if DSD suspected (severe hypospadias, bilateral undescended testis)
- Renal ultrasound (if associated anomalies)

**MANAGEMENT:**

**Surgical Repair:**
- **Timing:** 6-18 months (optimal: 12-18 months)
- **Procedure:** hypospadias repair (multiple techniques)
  - Tubularised incised plate (TIP) - most common
  - Mathieu, flip-flap, graft techniques for severe
- **Stent/catheter:** often placed for 5-7 days
- **Dressing:** protective dressing for 5-7 days

**OUTCOMES:**
- **Success:** 80-90%
- **Complications:**
  - Urethrocutaneous fistula (10-20%)
  - Meatal stenosis (5-10%)
  - Recurrence of chordee
  - Wound dehiscence
  - Hair-bearing urethra (if graft used)

**LONG-TERM:**
- Normal urinary stream
- Normal erections
- Fertility usually normal
- Cosmetic appearance acceptable
- May need further surgery if complications

**DO NOT CIRCUMCISE:**
- Foreskin may be needed for reconstruction
- **Wait until hypospadias repaired**

**Sources:** EAU Guidelines on Paediatric Urology"""
        )

    def _handle_general_urology(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general urology query"""
        return DomainQueryResult(
            domain_name="urology",
            answer="""**UROLOGY - General Consultation**

Urology covers diagnosis and treatment of conditions of the urinary tract (kidneys, ureters, bladder, urethra) and male reproductive system (testes, prostate, penis).

**COMMON UROLOGICAL CONDITIONS:**

**Kidney and Ureter:**
- Kidney stones (nephrolithiasis, renal colic)
- Kidney cancer (renal cell carcinoma)
- PUJ obstruction (congenital)
- UPJ obstruction

**Bladder:**
- Bladder cancer (transitional cell carcinoma)
- Overactive bladder (OAB)
- Urinary incontinence
- Interstitial cystitis
- Bladder stones

**Prostate:**
- Benign prostatic hyperplasia (BPH)
- Prostate cancer
- Prostatitis

**Testis and Scrotum:**
- Testicular cancer
- Epididymo-orchitis
- Testicular torsion
- Hydrocele, varicocele, epididymal cyst
- Undescended testis

**Penis:**
- Erectile dysfunction (ED)
- Peyronie's disease
- Hypospadias
- Phimosis, paraphimosis
- Priapism

**Paediatric Urology:**
- Undescended testis
- Hypospadias
- Vesicoureteric reflux (VUR)
- PUJ obstruction
- Neurogenic bladder (spina bifida)

**Female Urology:**
- Stress urinary incontinence
- Urge urinary incontinence
- Overactive bladder
- Pelvic organ prolapse
- Recurrent UTIs

**UROLOGICAL INVESTIGATIONS:**

**Imaging:**
- CT urogram (kidneys, ureters, bladder)
- Ultrasound (kidneys, bladder, prostate, scrotum)
- MRI (prostate, staging)
- X-ray (KUB - kidneys, ureters, bladder)

**Endoscopic:**
- Cystoscopy (bladder, urethra)
- Ureteroscopy (ureter, kidney)
- Nephroscopy (kidney)

**Functional:**
- Uroflowmetry (urinary flow rate)
- Urodynamics (bladder pressure studies)
- Bladder diary
- Post-void residual (bladder scan)

**Laboratory:**
- Urinalysis and microscopy
- Urine culture
- PSA (prostate-specific antigen)
- Tumour markers (AFP, hCG for testicular cancer)

**When to refer URGENTLY:**
- Visible haematuria (blood in urine)
- Suspected testicular cancer (painless lump)
- Testicular torsion (acute scrotal pain)
- Acute urinary retention
- priapism (erection >4 hours)
- Suspected urological cancer

**When to refer ROUTINELY:**
- Lower urinary tract symptoms (LUTS)
- Erectile dysfunction
- Recurrent UTIs
- Kidney stones (small, uncomplicated)
- Hydrocele, varicocele
- Undescended testis (child)

**Sources:** EAU Guidelines, NICE Guidelines, BAUS Standards"""
        )


def create_urology_domain():
    """Factory function to create urology domain"""
    return UrologyDomain()
