"""
Women's Health Domain for GPDISC

Comprehensive women's health covering:
- Menstrual disorders and abnormal uterine bleeding
- Contraception and family planning
- Fertility, conception, and pregnancy care
- Menopause and hormone replacement therapy
- Premenstrual syndrome (PMS) and PMDD
- Polycystic ovary syndrome (PCOS)
- Endometriosis and adenomyosis
- Pelvic pain and vulvovaginal conditions
- Breast health and screening
- Gynecological cancers prevention and screening
- Sexual health and vaginal atrophy
- Urinary incontinence and pelvic floor disorders
- Preconception counseling and postpartum care

Evidence-based guidelines: NICE, RCOG, FSRH, ACOG, WHO
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Optional, Dict, List, Any
import re


class WomensHealthDomain(BaseDomainModule):
    """
    Women's Health specialty domain covering reproductive health,
    gynecological conditions, and women-specific health concerns.

    Covers all aspects of women's health from adolescence through
    menopause and beyond.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="womens_health",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive women's health covering reproductive health, menstrual disorders, contraception, fertility, pregnancy, menopause, gynecological conditions, and women-specific preventive care",
            keywords=[
                # Core women's health
                "menstruation", "period", "menstrual cycle", "amenorrhea", "oligomenorrhea",
                "menorrhagia", "dysmenorrhea", "abnormal bleeding", "spotting",

                # Contraception
                "contraception", "birth control", "condom", "pill", "iud", "implant",
                "injection", "patch", "ring", "sterilization", "vasectomy", "emergency contraception",

                # Fertility and pregnancy
                "fertility", "infertility", "conception", "pregnancy", "pregnant",
                "antenatal", "prenatal", "postpartum", "miscarriage", "abortion",
                "ivf", "assisted reproduction",

                # Menopause
                "menopause", "perimenopause", "hrt", "hormone replacement therapy",
                "hot flashes", "night sweats", "vaginal dryness",

                # Gynecological conditions
                "pcos", "polycystic ovary", "endometriosis", "adenomyosis",
                "fibroids", "ovarian cyst", "pelvic pain",

                # PMS/PMDD
                "pms", "premenstrual", "pmdd", "premenstrual dysphoric",

                # Vaginal/vulvar
                "vagina", "vulva", "discharge", "itching", "thrush", "candida",
                "bacterial vaginosis", "vaginismus", "vulvodynia",

                # Breast
                "breast", "mastalgia", "breast pain", "breast lump", "nipple discharge",
                "breast screening", "mammogram",

                # Cancers
                "cervical cancer", "smear", "cervical screening", "hpv",
                "ovarian cancer", "womb cancer", "endometrial cancer",

                # Sexual health
                "sexual health", "sex", "dyspareunia", "libido", "sexual dysfunction",

                # Pelvic floor
                "incontinence", "prolapse", "pelvic floor", "stress incontinence",
                "urge incontinence", "cystocele", "rectocele"
            ],
            capabilities=[
                "menstrual_disorder_management", "contraception_counseling", "fertility_assessment",
                "prenatal_care_guidance", "menopause_management", "hrt_prescribing",
                "pcos_management", "endometriosis_treatment", "pelvic_pain_evaluation",
                "pms_pmdd_management", "breast_health_assessment", "cervical_screening",
                "vaginal_discharge_evaluation", "sexual_health_consultation",
                "pelvic_floor_rehabilitation", "preconception_counseling", "postpartum_care"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """
        Process women's health queries with comprehensive reproductive health focus.
        """
        query_lower = query.lower()

        # EMERGENCY: Ectopic pregnancy, miscarriage, severe bleeding
        if any(term in query_lower for term in ["ectopic", "rupture", "severe bleeding", "hemorrhage", "collapse", "faint"]) and \
           any(term in query_lower for term in ["pregnant", "pregnancy", "bleeding", "pain", "cramp"]):
            return self._handle_pregnancy_emergency(query, context)

        # EMERGENCY: Sexual assault
        if any(term in query_lower for term in ["sexual assault", "rape", "attacked"]):
            return self._handle_sexual_assault_emergency(query, context)

        # Pregnancy and fertility
        if any(term in query_lower for term in ["pregnant", "pregnancy", "missed period", "positive test", "trying to conceive"]):
            return self._handle_pregnancy_query(query, context)

        # Menstrual disorders
        if any(term in query_lower for term in ["period", "menstruation", "menstrual", "amenorrhea", "menorrhagia", "dysmenorrhea", "bleeding"]):
            return self._handle_menstrual_query(query, context)

        # Contraception
        if any(term in query_lower for term in ["contraception", "birth control", "contraceptive", "iud", "implant", "pill", "condom", "sterilization"]):
            return self._handle_contraception_query(query, context)

        # Menopause and HRT
        if any(term in query_lower for term in ["menopause", "perimenopause", "hrt", "hormone replacement", "hot flashes", "night sweats"]):
            return self._handle_menopause_query(query, context)

        # PCOS
        if any(term in query_lower for term in ["pcos", "polycystic ovary", "polycystic", "irregular periods", "hirsutism", "acne"]):
            return self._handle_pcos_query(query, context)

        # Endometriosis and adenomyosis
        if any(term in query_lower for term in ["endometriosis", "adenomyosis", "severe period pain", "chronic pelvic pain"]):
            return self._handle_endometriosis_query(query, context)

        # PMS/PMDD
        if any(term in query_lower for term in ["pms", "pmdd", "premenstrual", "mood swings", "period mood"]):
            return self._handle_pms_query(query, context)

        # Vaginal discharge and vulvovaginal symptoms
        if any(term in query_lower for term in ["discharge", "itching", "thrush", "candida", "bv", "vaginal", "vulva", "vaginitis"]):
            return self._handle_vaginal_query(query, context)

        # Breast symptoms
        if any(term in query_lower for term in ["breast pain", "breast lump", "mastalgia", "nipple discharge", "breast lump"]):
            return self._handle_breast_query(query, context)

        # Cervical screening and HPV
        if any(term in query_lower for term in ["smear", "cervical screening", "pap", "hpv"]):
            return self._handle_cervical_screening_query(query, context)

        # Sexual health and dysfunction
        if any(term in query_lower for term in ["painful sex", "dyspareunia", "low libido", "sex", "sexual"]):
            return self._handle_sexual_health_query(query, context)

        # Pelvic floor and incontinence
        if any(term in query_lower for term in ["incontinence", "prolapse", "pelvic floor", "leaking urine", "cystocele", "rectocele"]):
            return self._handle_pelvic_floor_query(query, context)

        # Preconception counseling
        if any(term in query_lower for term in ["planning pregnancy", "trying for baby", "preconception", "folic acid"]):
            return self._handle_preconception_query(query, context)

        # Postpartum care
        if any(term in query_lower for term in ["postpartum", "after birth", "new mom", "postnatal"]):
            return self._handle_postpartum_query(query, context)

        # Fibroids
        if any(term in query_lower for term in ["fibroid", "fibroids", "uterine fibroid"]):
            return self._handle_fibroids_query(query, context)

        # General women's health
        return self._handle_general_womens_health_query(query, context)

    def _handle_pregnancy_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pregnancy emergencies - ectopic pregnancy, miscarriage, severe bleeding."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**PREGNANCY EMERGENCY - URGENT MEDICAL ATTENTION REQUIRED**

**ECTOPIC PREGNANCY - MEDICAL EMERGENCY**
**Symptoms**: Missed period, positive pregnancy test, abdominal pain (often unilateral), vaginal bleeding, shoulder tip pain (sign of hemoperitoneum), collapse, syncope
**Risk factors**: Previous ectopic, pelvic inflammatory disease, IUD, tubal surgery, IVF, smoking, age >35
**Diagnosis**: Transvaginal ultrasound (adnexal mass, empty uterus), serial β-hCG (slow rise, plateau, decline)
**Treatment**: Methotrexate (if stable, unruptured, <3.5cm, β-hCG <5000) OR laparoscopic salpingectomy/salpingostomy
**IMMEDIATE action**: Refer to ED/early pregnancy assessment unit if suspected

**MISCARRIAGE**
**Symptoms**: Vaginal bleeding (spotting to heavy), abdominal cramps, passage of tissue, loss of pregnancy symptoms
**Types**: Threatened (bleeding, closed cervius, viable pregnancy), Inevitable (bleeding, open cervius), Incomplete (products of conception retained), Complete (all products passed), Missed (fetus died, no bleeding)
**Management**: Expectant (most complete spontaneously), Medical (misoprostol), Surgical (MVA - manual vacuum aspiration)
**Antiphospholipid syndrome**: Recurrent miscarriage (>3) - investigate for antiphospholipid antibodies, thrombophilia, parental karyotype

**SEVERE BLEEDING IN PREGNANCY**
**First trimester**: Miscarriage, ectopic (see above), molar pregnancy
**Second/third trimester**: Placenta previa (painless bright red bleeding), placental abruption (painful dark bleeding, uterine tenderness, fetal distress), vasa previa (fetal vessel rupture - fetal distress, bright red bleeding)
**IMMEDIATE action**: Urgent obstetric assessment, emergency delivery if indicated

**RED FLAGS IN PREGNANCY (Refer Urgently):**
- Vaginal bleeding (any amount)
- Severe abdominal pain
- Reduced/absent fetal movements (after 24 weeks)
- Severe headache, visual disturbances (pre-eclampsia)
- Premature rupture of membranes
- Suspected preterm labor (<37 weeks)
- Fever, chills, signs of infection

**SOURCES:** RCOG Green-top Guidelines, NICE
""",
            confidence=0.98,
            metadata={
                "specialty": "Women's Health",
                "focus": "Pregnancy Emergency",
                "urgency": "emergency",
                "sources": ["RCOG Green-top Guidelines", "NICE"]
            }
        )

    def _handle_sexual_assault_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sexual assault emergency."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**SEXUAL ASSAULT - IMMEDIATE SUPPORT REQUIRED**

**IMMEDIATE PRIORITIES:**
1. **Ensure safety**: Are you in a safe place? If not, police can help
2. **Medical care**: Urgent assessment for injuries, emergency contraception, STI prophylaxis, forensic evidence collection
3. **Emotional support**: You are not to blame, professional support available

**IMMEDIATE MEDICAL CARE:**
- **Sexual Assault Referral Centre (SARC)**: Specialist 24/7 service (UK) or Rape Crisis Center
- **Emergency department**: If SARC unavailable or injuries need treatment
- **Do NOT**: Wash, brush teeth, change clothes, eat/drink, use bathroom (if possible) before forensic examination
- **Timeframe**: Forensic evidence ideally within 7 days (earlier is better)

**EMERGENCY CONTRACEPTION:**
- **Levonorgestrel** (Plan B): Up to 72 hours (3 days) after, effectiveness decreases with time
- **Ulipristal acetate** (ellaOne): Up to 120 hours (5 days) after, more effective than levonorgestrel
- **Copper IUD**: Most effective (>99%), can be inserted up to 5 days after (or later if ovulation delayed)

**STI PROPHYLAXIS:**
- **HIV PEP** (post-exposure prophylaxis): Within 72 hours, ideally within 24 hours, 28-day course
- **Hepatitis B vaccine**: If not immune, vaccination series
- **Chlamydia/gonorrhea**: Test immediately, treat if positive or prophylactic azithromycin 1g + ceftriaxone 500mg
- **Syphilis, hepatitis C**: Test, treat if positive

**FOLLOW-UP:**
- **2 weeks**: STI test results, pregnancy test, emotional support
- **6-12 weeks**: Repeat HIV/hepatitis C tests
- **Ongoing**: Counseling, support services

**SUPPORT SERVICES:**
- **Rape Crisis**: 24/7 helpline, counseling, advocacy
- **Samaritans**: 24/7 emotional support
- **Police**: Can report anonymously initially, decide later about formal investigation

**LONG-TERM CONSIDERATIONS:**
- **Emotional impact**: PTSD, depression, anxiety, sexual dysfunction - professional counseling helps
- **Physical health**: Regular health checks, cervical screening

**YOU ARE NOT TO BLAME**. Sexual assault is never the victim's fault. Help is available.

**SOURCES:** NICE, NHS, RCOG, CDC
""",
            confidence=0.98,
            metadata={
                "specialty": "Women's Health",
                "focus": "Sexual Assault - Emergency Response",
                "urgency": "emergency",
                "sources": ["NICE", "NHS", "RCOG", "CDC"]
            }
        )

    def _handle_pregnancy_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pregnancy queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**PREGNANCY CARE AND CONSULTATION**

**CONFIRMING PREGNANCY:**
- **Urine pregnancy test**: Detects β-hCG from ~4 weeks after LMP (missed period), positive if >25 mIU/mL
- **Serum β-hCG**: More sensitive, quantitative, useful if uncertainty, ectopic concern
- **Ultrasound**: Transvaginal from 6 weeks, transabdominal from 8-10 weeks

**DATING PREGNANCY:**
- **LMP method**: Due date = LMP + 280 days (40 weeks), assumes regular 28-day cycle, ovulation day 14
- **Ultrasound dating**: More accurate, CRL measurement 7-14 weeks most accurate (±5 days)
- **If discrepancy >7 days** between LMP and ultrasound: Use ultrasound dates

**GESTATIONAL AGE:**
- **Preterm**: <37 weeks
- **Early preterm**: 34-36+6 weeks
- **Moderate preterm**: 32-33+6 weeks
- **Very preterm**: <32 weeks
- **Term**: 37-41+6 weeks
- **Post-term**: ≥42 weeks

**ANTENATAL CARE SCHEDULE (Low-risk pregnancy):**
- **Booking visit**: 8-10 weeks - history, exam, bloods, dating scan
- **Dating scan**: 10-14 weeks - confirm viability, dating, nuchal translucency
- **Combined screening**: 11-14 weeks - nuchal translucency + PAPP-A + β-hCG (Down syndrome screening)
- **Anomaly scan**: 18-20+6 weeks - detailed fetal anatomy
- **Routine antenatal visits**: 16 weeks, 24-28 weeks (OGTT for diabetes if risk), 31 weeks, 34 weeks, 36 weeks, then weekly until delivery
- **Growth scans**: If concern (IUGR, SGA, hypertension, diabetes)

**ROUTINE INVESTIGATIONS:**
- **Blood group & antibodies**: Identify RhD status, anti-D if RhD negative
- **Full blood count**: Anemia (Hb <11 g/dL first trimester, <10.5 second, <10 third)
- **Infections**: Syphilis, HIV, hepatitis B, rubella immunity
- **Urinalysis**: Proteinuria (pre-eclampsia), bacteriuria (UTI), glucose
- **Cervical screening**: If due (can defer until after pregnancy)

**COMMON PREGNANCY SYMPTOMS:**
- **Nausea/vomiting**: 70-80%, usually resolves by 12-16 weeks
  - Management: Small frequent meals, dry crackers before rising, ginger, vitamin B6 (pyridoxine 10-25mg TDS)
  - Hyperemesis gravidarum: Severe, dehydration, electrolyte disturbance - hospitalization, IV fluids, antiemetics (ondansetron, metoclopramide)
- **Fatigue**: Common, especially first trimester - rest, iron if deficient
- **Breast tenderness**: Hormonal changes, supportive bra
- **Frequency**: Uterus compresses bladder, resolves as uterus rises out of pelvis
- **Constipation**: Progesterone slows motility, iron supplements - fluids, fiber, stool softeners
- **Heartburn**: Progesterone relaxes LES - small meals, avoid triggers, antacids, ranitidine
- **Back pain**: Postural changes, physiotherapy, support belt
- **Leg cramps**: Magnesium, stretching, avoid lying supine after 28 weeks

**MEDICATIONS IN PREGNANCY:**
- **Category system**: Avoid, use if benefit outweighs risk
- **SAFE**: Paracetamol/acetaminophen (first-line for pain), penicillins, cephalosporins, most asthma inhalers
- **AVOID**: ACE inhibitors, ARBs, statins, warfarin (use LMWH), tetracyclines, fluoroquinolones, NSAIDs (especially third trimester), ACE inhibitors
- **CAUTION**: SSRIs (risk of PPHN, neonatal adaptation syndrome), valproate (neural tube defects, cognitive impairment), carbamazepine (neural tube defects)

**RED FLAGS (Refer Immediately):**
- **Vaginal bleeding**: Any amount - miscarriage, placenta previa, abruption
- **Abdominal pain**: Ectopic, abruption, labor
- **Reduced fetal movements**: After 24 weeks, especially if <10 movements in 12 hours
- **Severe headache, visual disturbances**: Pre-eclampsia
- **Premature rupture of membranes**: Leakage of fluid, risk of chorioamnionitis, preterm labor
- **Preterm labor**: Regular contractions, cervical dilation before 37 weeks

**PRE-ECLAMPSIA:**
- **Definition**: Pregnancy-induced hypertension (≥140/90) + proteinuria (≥300 mg/24h) OR end-organ dysfunction after 20 weeks
- **Risk factors**: First pregnancy, age <20 or >35, obesity, hypertension, renal disease, diabetes, autoimmune disease, multiple pregnancy, previous pre-eclampsia
- **Symptoms**: Headache, visual disturbances (scotoma, photophobia), epigastric/RUQ pain, edema (not diagnostic)
- **Management**: Deliver baby (only cure), antihypertensives (labetalol, nifedipine), magnesium sulfate for seizure prophylaxis/treatment

**GESTATIONAL DIABETES:**
- **Screening**: OGTT 75g at 24-28 weeks (earlier if risk factors)
- **Diagnosis**: Fasting ≥5.6 mmol/L OR 2-hour ≥7.8 mmol/L (WHO criteria)
- **Management**: Diet, exercise, metformin, insulin if uncontrolled
- **Risks**: Macrosomia, shoulder dystocia, hypoglycemia, stillbirth

**PRECONCEPTION COUNSELING:**
- **Folic acid**: 400 mcg daily starting 1-3 months before conception (5 mg if diabetes, epilepsy, high BMI, previous NTD)
- **Medication review**: Stop teratogens, optimize chronic disease (hypertension, diabetes, epilepsy)
- **Rubella immunity**: Check, vaccinate if non-immune (avoid pregnancy 1 month after)
- **Lifestyle**: Smoking cessation, limit alcohol (avoid completely), healthy weight, exercise

**SOURCES:** NICE, RCOG, ACOG
""",
            confidence=0.95,
            metadata={
                "specialty": "Women's Health",
                "focus": "Pregnancy Care",
                "sources": ["NICE", "RCOG", "ACOG"]
            }
        )

    def _handle_menstrual_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle menstrual disorder queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**MENSTRUAL DISORDERS**

**NORMAL MENSTRUAL CYCLE:**
- **Length**: 21-35 days (average 28)
- **Duration**: 2-7 days (average 4-5)
- **Blood loss**: 30-80 mL (average 40-50, >80 is heavy)
- **Regularity**: May be irregular in first 1-2 years after menarche and perimenopause

**AMENORRHEA (Absent Periods):**

**Primary amenorrhea**: No menarche by age 15 OR no menarche within 3 years of breast development
- **Causes**: Gonadal dysgenesis (Turner syndrome), hypothalamic-pituitary disorders (Kallmann syndrome, hypopituitarism), genital outflow obstruction (imperforate hymen, transverse vaginal septum), androgen insensitivity

**Secondary amenorrhea**: No periods for ≥3 months in previously regular cycles or ≥6 months in previously irregular
- **Causes**:
  - **Pregnancy** (most common) - test first
  - **Hypothalamic**: Stress, exercise (athletic triad), weight loss, eating disorders
  - **Pituitary**: Prolactinoma, hypopituitarism, Sheehan's syndrome
  - **Ovarian**: PCOS, premature ovarian insufficiency (POI <40 years), menopause
  - **Other**: Thyroid disorders, adrenal disorders, medications (antipsychotics, chemotherapy)

**Investigations**: Pregnancy test, FSH, LH, prolactin, TSH, testosterone/androgens (if PCOS suspected), pelvic ultrasound

**OLIGOMENORRHEA (Infrequent Periods):**
- **Definition**: Cycles >35 days
- **Common causes**: PCOS, perimenopause, hypothalamic dysfunction

**MENORRHAGIA (Heavy Menstrual Bleeding):**
- **Definition**: Excessive menstrual blood loss (>80 mL) interfering with physical, social, emotional quality of life OR objective measure of >80 mL blood loss
- **Subjective assessment**: Passing large clots, flooding through clothes, "tide over," using double protection, frequent changes (every 1-2 hours)
- **Causes**:
  - **Structural** (50%): Fibroids, adenomyosis, polyps, malignancy
  - **Dysfunctional** (50%): Anovulatory cycles (PCOS, perimenopause), coagulation disorders (von Willebrand disease), ovulatory dysfunction, endometriosis
  - **Iatrogenic**: Copper IUD, anticoagulants

**Investigations**:
- **Full blood count**: Check for iron deficiency anemia
- **Pelvic ultrasound**: First-line imaging to identify structural causes
- **Endometrial sampling**: If >45 years, persistent bleeding, risk factors for endometrial cancer (obesity, PCOS, tamoxifen)
- **Coagulation screen**: If menorrhagia since menarche, family history, other bleeding symptoms

**Management**:
- **Medical** (first-line):
  - **Levonorgestrel IUS** (Mirena): First-line, reduces blood loss 95%, provides contraception, treats endometrial hyperplasia
  - **Tranexamic acid**: Antifibrinolytic, reduces blood loss 50%, take during menses only
  - **NSAIDs** (mefenamic acid, naproxen): Reduce blood loss 20-50%, also help dysmenorrhea
  - **Combined oral contraceptive pill**: Regulates cycles, reduces blood loss
  - **Oral progestogens** (norethisterone 5mg TDS days 5-26): Alternative if IUD not suitable
- **Surgical** (if medical fails, or structural lesion):
  - **Uterine artery embolization** (fibroids)
  - **Myomectomy** (fibroid removal, uterus-preserving)
  - **Endometrial ablation** (if fertility complete, no structural lesions)
  - **Hysterectomy** (definitive, last resort)

**DYSMENORRHEA (Painful Periods):**

**Primary dysmenorrhea**: Painful periods without structural disease
- **Pathophysiology**: Excess prostaglandin F2α causing uterine cramping
- **Management**: NSAIDs (ibuprofen, mefenamic acid) taken at onset and regularly during menses, COCP (suppresses ovulation, reduces prostaglandins), exercise, heat

**Secondary dysmenorrhea**: Painful periods due to structural disease
- **Causes**: Endometriosis, adenomyosis, fibroids, PID, adenomyosis
- **Investigate**: Pelvic ultrasound (first-line), laparoscopy (gold standard for endometriosis)
- **Management**: Treat underlying cause

**INTERMENSTRUAL BLEEDING (IMB):**
- **Definition**: Bleeding between periods, excluding post-coital bleeding
- **Causes**: Hormonal contraception (especially during first 3 months), pregnancy complications, cervical polyps, infection (chlamydia), cervical cancer, ovulation bleed (mid-cycle)
- **Management**: Pregnancy test, STI screen, pelvic exam, cervical cytology, ultrasound

**POST-COITAL BLEEDING (PCB):**
- **Definition**: Bleeding immediately after intercourse
- **Causes**: Cervical ectropion, cervical polyps, infection (chlamydia), cervical cancer (must exclude), vaginal atrophy (menopause), trauma
- **Management**: Speculum exam, STI screen, cervical cytology, colposcopy if cytology abnormal or persistent bleeding

**IRREGULAR BLEEDING ON HORMONAL CONTRACEPTION:**
- **COCP**: Breakthrough bleeding common in first 3 months, ensure correct use, consider different progestogen dose/type
- **POP/Progestogen-only**: Irregular bleeding common, especially early, may improve, consider switching
- **Levonorgestrel IUS**: Irregular bleeding first 3-6 months, then amenorrhea common
- **Implant**: Common, often settles, consider estrogen add-back (COCP) or switching methods

**SOURCES:** NICE NG88, RCOG Green-top Guidelines
""",
            confidence=0.94,
            metadata={
                "specialty": "Women's Health",
                "focus": "Menstrual Disorders",
                "sources": ["NICE NG88", "RCOG Green-top Guidelines"]
            }
        )

    def _handle_contraception_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle contraception queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**CONTRACEPTION AND FAMILY PLANNING**

**EMERGENCY CONTRACEPTION:**

**Levonorgestrel (Plan B, morning-after pill)**:
- **Timing**: Up to 72 hours (3 days) after unprotected sex (UPSI), effectiveness decreases with time (95% within 24h, 85% 25-48h, 58% 49-72h)
- **Dose**: 1.5 mg single dose (two 750 mcg tablets)
- **Mechanism**: Delays ovulation (not effective after ovulation)
- **Side effects**: Nausea, vomiting, irregular bleeding, next period may be early/late
- **Availability**: OTC pharmacy, prescription, sexual health clinics

**Ulipristal acetate (ellaOne)**:
- **Timing**: Up to 120 hours (5 days) after UPSI, more effective than levonorgestrel especially after 72h
- **Dose**: 30 mg single dose
- **Mechanism**: Delays ovulation (may also inhibit implantation)
- **Interactions**: Enzyme inducers (rifampin, carbamazepine, phenytoin, St. John's wort) reduce efficacy
- **Availability**: Prescription only (UK), OTC with pharmacist consultation (some countries)

**Copper IUD**:
- **Timing**: Up to 5 days after UPSI (or later if ovulation delayed)
- **Efficacy**: >99% (most effective method)
- **Mechanism**: Prevents fertilization and implantation, copper is spermicidal
- **Additional benefit**: Provides ongoing long-term contraception (5-10 years)
- **Side effects**: Cramping, heavier/longer periods initially, perforation rare
- **Contraindications**: Pregnancy, active pelvic infection, uterine anomaly (specialist assessment), Wilson's disease (copper allergy)

**REVERSIBLE LONG-ACTING CONTRACEPTION (LARC)**:

**Levonorgestrel Intrauterine System (LNG-IUS, Mirena, Kyleena, Levosert)**:
- **Duration**: 3-8 years depending on device
- **Efficacy**: >99% (less user error, continuation highest of all methods)
- **Benefits**: Dramatically reduces menstrual bleeding (95%), treats dysmenorrhea, treats endometrial hyperplasia, progesterone-only (suitable if estrogen contraindicated)
- **Side effects**: Irregular bleeding first 3-6 months, then amenorrhea common, hormonal side effects (acne, breast tenderness, mood changes) but less systemic than COCP
- **Risks**: Perforation (1:1000), expulsion (5%), pelvic infection rare (not sterile insertion)
- **Fertility**: Immediate return on removal

**Copper IUD (non-hormonal)**:
- **Duration**: 5-10 years
- **Efficacy**: >99%
- **Benefits**: Hormone-free, immediately effective, long-term, emergency contraception
- **Side effects**: Heavier, longer periods (especially first 3 months), more cramping
- **Risks**: Perforation, expulsion, increased menstrual bleeding leading to anemia, PID risk
- **Fertility**: Immediate return on removal

**Subdermal implant (Nexplanon)**:
- **Duration**: 3 years
- **Efficacy**: >99%
- **Benefits**: Progesterone-only, convenient, estrogen-free, improves dysmenorrhea
- **Side effects**: Irregular bleeding (common, often settles), amenorrhea, hormonal side effects
- **Risks**: Expulsion (rare), difficult insertion/removal (rare complications)
- **Fertility**: Immediate return on removal

**Injectable (Depo-Provera)**:
- **Dose**: Medroxyprogesterone acetate 150 mg IM every 12 weeks
- **Efficacy**: 94-99% (user-dependent - timing of injections)
- **Benefits**: Convenient, estrogen-free, improves dysmenorrhea, may reduce endometriosis pain
- **Side effects**: Irregular bleeding common initially, then amenorrhea, weight gain (2-3 kg average), mood changes, decreased bone density (reversible)
- **Risks**: Delayed return to fertility (average 10 months, can take >1 year), decreased bone mineral density
- **Consider**: Not first-line due to delayed fertility, bone density concerns

**COMBINED HORMONAL METHODS**:

**Combined Oral Contraceptive Pill (COCP)**:
- **Efficacy**: 91-99% (perfect use 99%, typical use 91% due to missed pills)
- **Mechanism**: Inhibits ovulation, thickens cervical mucus, thins endometrium
- **Regimens**: 21/7 (21 active pills, 7 pill-free bleed), 24/4, 24/2/2 (extended regimens)
- **Benefits**: Regulates cycles, reduces menstrual bleeding, improves dysmenorrhea, reduces acne, reduces endometrial/ovarian cancer risk, improves iron deficiency
- **Risks**: VTE (4/10,000 vs 2/10,000 baseline), stroke, MI (very rare in <35 nonsmokers), breast cancer (slightly increased risk, but reduced ovarian/endometrial), cervical cancer (slight increase)
- **Contraindications**: Migraine with aura, age >35 + smoking, hypertension, VTE history, certain migraines, breast cancer, liver disease
- **Missed pill guidance**: Varies by type, generally if <12h late take as soon as possible, if >12h late use backup for 7 days

**Combined Patch (Evra)**:
- **Dose**: Apply 1 patch weekly for 3 weeks, patch-free week
- **Efficacy**: 91-99%
- **Risks**: VTE risk higher than COCP (60/10,000 vs 4-8/10,000), similar otherwise
- **Benefits**: Convenient, no daily pill, bypasses first-pass metabolism
- **Contraindications**: Same as COCP

**Combined Vaginal Ring (NuvaRing)**:
- **Dose**: Insert ring for 21 days, remove for 7 days (bleed)
- **Efficacy**: 91-99%
- **Benefits**: Convenient, steady hormone levels, bypasses first-pass
- **Contraindications**: Same as COCP

**PROGESTOGEN-ONLY PILL (POP, mini-pill)**:
- **Traditional POP** (norethisterone): Must take within 3-hour window
- **Desogestrel POP** (Cerazette): 12-hour window (more forgiving), also inhibits ovulation (some women)
- **Efficacy**: 91-99% (depends on adherence)
- **Benefits**: Progesterone-only, suitable if estrogen contraindicated, breastfeeding
- **Side effects**: Irregular bleeding common, amenorrhea, breast tenderness, mood changes
- **Contraindications**: Breast cancer (active), arterial disease (some types)

**BARRIER METHODS**:

**Male condom**:
- **Efficacy**: Typical use 82%, perfect use 98%
- **Benefits**: STI prevention, no hormones, readily available
- **Side effects**: Allergy (latex), reduced sensation
- **Use**: Every act of sex, correct use (space at tip, roll on fully, hold during withdrawal)

**Female condom (Femidom)**:
- **Efficacy**: Typical use 79%, perfect use 95%
- **Benefits**: STI protection, female-controlled, can insert in advance
- **Contraindications**: Latex allergy

**Diaphragm/cap with spermicide**:
- **Efficacy**: Typical use 88%, perfect use 94%
- **Requires**: Fitting by healthcare provider, insertion before sex, leave in 6 hours after
- **Side effects**: Cystitis risk, allergic reaction to spermicide

**PERMANENT METHODS (Sterilization)**:

**Female sterilization (tubal ligation)**:
- **Procedure**: Laparoscopic tubal occlusion (clips, rings, coagulation) or hysteroscopic (Essure discontinued)
- **Efficacy**: >99%
- **Benefits**: Permanent, no hormones, highly effective
- **Risks**: Surgical risks (anesthesia, infection, bleeding, injury to organs), regret (younger women higher), failure (1:200), ectopic pregnancy if failure occurs
- **Reversibility**: Difficult, expensive, not guaranteed, not funded in most healthcare systems

**Male sterilization (vasectomy)**:
- **Procedure**: Minor surgery under local anesthesia,切断输精管
- **Efficacy**: >99% (after clearance confirmed)
- **Benefits**: Less invasive than female sterilization, fewer complications, cheaper, highly effective
- **Risks**: Regret (rare, lower than female), failure (1:2000), hematoma, infection, chronic pain (rare)
- **Reversibility**: Possible but not guaranteed (microsurgical vasovasostomy), expensive
- **Clearance**: Not immediately effective - need 20 ejaculations OR 12-16 weeks AND negative semen analysis

**FERTILITY AWARENESS METHODS**:
- **Effectiveness**: Highly variable (76-99% depending on method and adherence)
- **Methods**: Calendar method, basal body temperature, cervical mucus, symptothermal, ovulation predictor kits
- **Advantages**: No hormones, understanding fertility, may help conception planning
- **Disadvantages**: High failure rates, requires daily diligence, no STI protection

**CONTRACEPTION CHOICE**: Depends on patient preferences, medical history, age, smoking status, desire for future fertility, frequency of intercourse, side effect tolerance, comorbidities, drug interactions

**SOURCES:** FSRH Guidelines, NICE, CDC
""",
            confidence=0.96,
            metadata={
                "specialty": "Women's Health",
                "focus": "Contraception",
                "sources": ["FSRH Guidelines", "NICE", "CDC"]
            }
        )

    def _handle_menopause_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle menopause and HRT queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**MENOPAUSE AND HORMONE REPLACEMENT THERAPY (HRT)**

**DEFINITIONS:**
- **Menopause**: 12 months after last menstrual period (average age 51 in UK, range 45-55)
- **Perimenopause**: Period of menstrual irregularity and symptoms before menopause (can last 2-8 years)
- **Postmenopause**: After 12 months amenorrhea, for the rest of life
- **Premature ovarian insufficiency (POI)**: Menopause before age 40 (<1% women)

**SYMPTOMS (Vasomotor Symptoms - VMS):**
- **Hot flashes**: Sudden feeling of heat, face/neck/chest flushing, palpitations, anxiety
- **Night sweats**: Hot flashes at night, disrupt sleep, fatigue
- **Sleep disturbance**: Insomnia, early waking
- **Mood changes**: Irritability, anxiety, low mood, mood swings
- **Vaginal dryness**: Dyspareunia (painful sex), reduced libido
- **Urinary symptoms**: Frequency, urgency, dysuria, recurrent UTIs
- **Joint aches, headaches, palpitations, weight gain (abdominal)**

**DIAGNOSIS:**
- **>45 years**: Clinical diagnosis based on symptoms, no tests needed
- **45-45 years**: Consider FSH if still menstruating (elevated FSH >30 IU/L on two occasions 4-6 weeks apart) but NOT diagnostic alone
- **<40 years**: Investigate for POI (FSH, LH, estradiol, consider karyotype, autoimmune screen)

**HRT INDICATIONS:**
- **Vasomotor symptoms**: Hot flashes, night sweats (most effective treatment)
- **Genitourinary syndrome of menopause (GSM)**: Vaginal atrophy, dyspareunia, urinary symptoms
- **Prevention of osteoporosis**: In women at increased risk (consider risks/benefits)
- **Premature ovarian insufficiency**: HRT recommended until at least age 51 (bone/cardiovascular protection)

**HRT RISKS (NICE 2023, most recent evidence)**:
- **Venous thromboembolism (VTE)**: Oral (but NOT transdermal) increases risk 2x (still rare: 4/1000 vs 2/1000 baseline)
- **Stroke**: Slightly increased risk with oral (but NOT transdermal)
- **Breast cancer**: Estrogen-only HRT (women without uterus) - NO increased risk (from 47/1000 to 47/1000 over 7.5 years). Combined HRT (estrogen + progestogen) - slightly increased risk (from 47/1000 to 61-63/1000 over 7.5 years, but risk returns to baseline after stopping)
- **Coronary heart disease**: NO increased risk if HRT started <60 years or within 10 years of menopause (timing hypothesis). May even be protective. Increased risk if started >60 years or >10 years after menopause
- **Endometrial cancer**: Estrogen-only HRT increases risk in women with uterus (hence progestogen needed). Combined HRT eliminates risk

**HRT BENEFITS:**
- **Effective symptom relief**: Hot flashes, night sweats, vaginal dryness (75-90% improvement)
- **Bone health**: Increases bone mineral density, reduces fracture risk (osteoporotic fractures reduced by 20-30%)
- **Cardiovascular**: Reduced risk if started early (<60, <10 years postmenopause)
- **Quality of life**: Improved sleep, mood, sexual function, overall well-being
- **Diabetes**: Reduced risk of type 2 diabetes

**HRT TYPES:**

**Estrogens**:
- **Oral**: Estradiol 1-2 mg daily, conjugated equine estrogens 0.3-0.625 mg daily (increases VTE/stroke risk)
- **Transdermal** (patch, gel): Estradiol 50-100 mcg daily (NO increased VTE/stroke risk, first-line if risk factors)
- **Vaginal**: Estriol, estradiol, creams, pessaries, vaginal ring (minimal systemic absorption, for GSM only)

**Progestogens** (oppose estrogen's endometrial effects, needed in women with uterus):
- **Micronized progesterone** (Utrogestan): Natural progesterone, neutral or beneficial for breast (preferable)
- **Dydrogesterone** (Duphaston): Retroprogesterone, neutral breast profile
- **Norethisterone**: Testosterone derivative, androgenic side effects (acne, hirsutism)
- **Medroxyprogesterone acetate**: Synthetic progestogen, may worsen breast risk

**Regimens**:
- **Sequential/cyclical** (for women with uterus, still menstruating): Estrogen daily + progestogen for 12-14 days each month (withdrawal bleed each month)
- **Continuous/combined** (for women with uterus, ≥1 year postmenopause): Estrogen + progestogen daily (no bleed, may have spotting initially)
- **Estrogen-only** (women without uterus/hysterectomy): Estrogen daily, no progestogen needed (no endometrial cancer risk)

**NON-HORMONAL ALTERNATIVES FOR HOT FLASHES:**
- **Lifestyle**: Weight loss if overweight, exercise, avoid triggers (caffeine, alcohol, spicy foods, hot drinks, stress), layered clothing, cool room, fan, paced breathing
- **CBT** (cognitive behavioral therapy): Effective for hot flashes and sleep/mood
- **SSRIs/SNRIs**: Paroxetine 7.5-12.5 mg (FDA-approved for menopausal hot flashes), escitalopram, venlafaxine
- **Gabapentin**: 300-900 mg TDS (especially effective for night sweats)
- **Clonidine**: 50-75 mcg BD (less effective, antihypertensive)

**VAGINAL ESTROGEN (for GSM)**:
- **Indications**: Dyspareunia, vaginal dryness, urinary symptoms, recurrent UTIs, vaginal atrophy
- **Preparations**: Estradiol tablets 10 mcg (Vagifem) - insert daily for 2 weeks then twice weekly; estriol cream; pessary; ring (Estring) - replace every 3 months
- **Safety**: Minimal systemic absorption, safe for long-term use, can be used alongside HRT or alone, safe with breast cancer history (oncologist approval)

**TESTOSTERONE**:
- **Indication**: Hypoactive sexual desire disorder (HSDD) in women (reduced libido causing distress)
- **Other options exhausted**: First address relationship issues, depression, other medications, vaginal estrogen for dyspareunia
- **Evidence**: Limited but shows benefit for sexual function
- **Preparations**: Testosterone gel (off-label, compounded) - 1% 0.5-1 g daily, aim for premenopausal levels
- **Monitoring**: Testosterone levels (aim 0.7-2.0 nmol/L), lipid profile, liver function (rarely needed with transdermal)
- **Side effects**: Acne, hirsutism, alopecia (if excessive dose)
- **Duration**: 6 months trial, reassess, long-term safety unknown

**HRT PRESCRIBING PRINCIPLES:**
- **Start low, go slow**: Lowest effective dose, titrate as needed
- **Review regularly**: 3 months after starting, then annually
- **Transdermal preferred**: If VTE risk factors (obesity, thrombophilia, immobility, smoking)
- **Duration**: As long as needed for symptom control (reassess annually, risks/benefits change with age)
- **Individualized**: No one-size-fits-all, tailor to patient symptoms, risk factors, preferences

**WHEN TO STOP HRT**:
- **NICE 2023**: No arbitrary limit, can continue indefinitely if symptoms persist and patient is informed of risks
- **Annual review**: Discuss ongoing need, dose reduction, alternative treatments
- **Gradual withdrawal**: Taper over months (not days) to minimize symptom recurrence

**BONE HEALTH**:
- **DEXA scan**: If risk factors (premature menopause, family history, steroid use, low BMI, smoking, alcohol, previous fracture)
- **FRAX calculation**: Assess 10-year fracture risk
- **Treatment**: Bisphosphonates (alendronate first-line), denosumab, HRT (bone protection if <60)

**SOURCES:** NICE NG23, BMS Menopause Guidelines, RCOG
""",
            confidence=0.97,
            metadata={
                "specialty": "Women's Health",
                "focus": "Menopause and HRT",
                "sources": ["NICE NG23", "BMS Menopause Guidelines", "RCOG"]
            }
        )

    def _handle_pcos_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle PCOS queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**POLYCYSTIC OVARY SYNDROME (PCOS)**

**PREVALENCE**: 6-20% of reproductive-aged women (depending on diagnostic criteria)

**DIAGNOSIS (Rotterdam 2003 - 2 out of 3 required)**:
1. **Oligo- or anovulation**: Irregular/absent periods, <8 cycles/year, or >35 day cycles
2. **Hyperandrogenism**: Clinical (hirsutism, acne, alopecia) OR biochemical (elevated free testosterone, free androgen index)
3. **Polycystic ovaries on ultrasound**: ≥20 follicles per ovary AND ovarian volume >10 mL (on either ovary)

**EXCLUDE OTHER CAUSES**: Thyroid disorders, hyperprolactinemia, androgen-secreting tumors, congenital adrenal hyperplasia (NCCAH)

**PATHOPHYSIOLOGY**: Insulin resistance → compensatory hyperinsulinemia → ovarian and adrenal androgen production → anovulation

**CLINICAL FEATURES**:
- **Menstrual**: Oligomenorrhea, amenorrhea, infertility, dysfunctional uterine bleeding
- **Androgen excess**: Hirsutism (Ferriman-Gallwey score >8), acne, male-pattern hair loss (androgenic alopecia)
- **Metabolic**: Insulin resistance, obesity (50-80%, android/abdominal distribution), impaired glucose tolerance, type 2 diabetes, dyslipidemia
- **Reproductive**: Infertility, increased pregnancy complications (gestational diabetes, pre-eclampsia)
- **Psychological**: Depression, anxiety, reduced quality of life, body image concerns

**INVESTIGATIONS**:
- **Hormonal**: Testosterone (total and free), SHBG, free androgen index (FAI), LH, FSH (LH:FSH ratio NOT diagnostic), prolactin, TSH, 17-OH progesterone (exclude NCCAH), DHEAS
- **Metabolic**: Fasting glucose/insulin, HbA1c, lipid profile, OGTT if high BMI or family history of diabetes
- **Ultrasound**: Transvaginal (preferred) or transabdominal
- **Other**: Pregnancy test, endometrial sampling if prolonged amenorrhea (endometrial hyperplasia/cancer risk)

**MANAGEMENT**:

**Lifestyle Modification (First-line for ALL)**:
- **Weight loss**: 5-10% weight loss improves insulin resistance, restores ovulation, reduces androgens, regulates periods
- **Diet**: Low glycemic index, balanced macronutrients, portion control
- **Exercise**: 150 min/week moderate intensity + resistance training
- **Sleep**: 7-9 hours, treat obstructive sleep apnea if present
- **Smoking cessation**: Increases cardiovascular risk, androgen levels

**Menstrual Regulation / Endometrial Protection**:
- **COCP**: First-line if not trying to conceive, regulates cycles, reduces endometrial cancer risk, reduces androgens (increases SHBG), improves acne/hirsutism
- **Progestogen-only**: If estrogen contraindicated (VTE risk, migraine with aura) - norethisterone 5-10 mg days 5-26 each cycle, or LNG-IUS (amenorrhea, endometrial protection)
- **Metformin**: Improves insulin sensitivity, may restore ovulation, reduces diabetes risk (especially if impaired glucose tolerance), 500 mg TDS or 850 mg BD, start low and titrate to minimize GI side effects

**Hyperandrogenism Management**:
- **Hirsutism**:
  - **COCP**: First-line, takes 6-12 months for full effect
  - **Anti-androgens** (in combination with contraception due to teratogenicity): Cyproterone acetate 50 mg days 1-10 of cycle + COCP; Spironolactone 50-200 mg daily (diuretic, monitor K+); Finasteride 5 mg daily; Flutamide (rare due to hepatotoxicity)
  - **Topical**: Eflornithine 13.9% cream (Vaniqa) slows facial hair growth
  - **Cosmetic**: Shaving, waxing, laser, electrolysis (immediate results, need maintenance)
- **Acne**: COCP, topical retinoids, benzoyl peroxide, antibiotics (erythromycin, lincosamide), isotretinoin (severe, specialist)
- **Androgenic alopecia**: COCP, finasteride off-label (specialist), minoxidil (cosmetic)

**Infertility Treatment**:
- **Weight loss**: First-line if overweight/obese (5-10% improves ovulation)
- **Clomifene citrate**: First-line ovulation induction, 50 mg days 2-6, increase to 100-150 mg if no ovulation, maximum 6 cycles (monitor for ovarian hyperstimulation, multiple pregnancy)
- **Metformin**: Adjunct to clomifene, especially if BMI >30 or impaired glucose tolerance
- **Letrozole**: Aromatase inhibitor, alternative to clomifene, better ovulation and live birth rates (especially in PCOS), 2.5-7.5 mg days 3-7
- **Gonadotropins** (FSH/LH): Specialist initiation, daily injections, intensive monitoring (ultrasound, estradiol), high ovarian hyperstimulation and multiple pregnancy risk, IVF conversion if too many follicles
- **IVF**: If failed ovulation induction or other infertility factors

**Metabolic Complications**:
- **Type 2 diabetes**: Annual screening with HbA1c or fasting glucose (or OGTT if high risk)
- **Cardiovascular risk**: Aggressive risk factor management (blood pressure, lipids, smoking cessation, weight management)
- **Obstructive sleep apnea**: Screen if obese, snoring, daytime somnolence
- **NAFLD**: Liver ultrasound, monitor LFTs

**Pregnancy Complications**:
- **Gestational diabetes**: Screen with OGTT at 16-18 weeks and 24-28 weeks (earlier if high risk)
- **Pre-eclampsia**: Low-dose aspirin 150 mg from 12 weeks until delivery (USPSTF recommendation)
- **Preterm birth, miscarriage**: Higher rates, early antenatal care

**Long-Term Health**:
- **Endometrial cancer**: Risk from prolonged unopposed estrogen (anovulation) - COCP or progestogens for endometrial protection
- **Cardiovascular disease**: Increased risk - aggressive risk factor management
- **Type 2 diabetes**: 30-50% develop impaired glucose tolerance, 10% develop type 2 diabetes
- **Psychological**: Depression, anxiety, body image - address proactively

**SOURCES:** NICE NG23, Rotterdam Consensus, ASRM, ESHRE
""",
            confidence=0.95,
            metadata={
                "specialty": "Women's Health",
                "focus": "Polycystic Ovary Syndrome (PCOS)",
                "sources": ["NICE NG23", "Rotterdam Consensus", "ASRM", "ESHRE"]
            }
        )

    def _handle_endometriosis_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle endometriosis queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**ENDOMETRIOSIS AND ADENOMYOSIS**

**ENDOMETRIOSIS**

**DEFINITION**: Presence of endometrial-like tissue outside the uterus, causing chronic inflammation and pain

**PREVALENCE**: 6-10% of reproductive-aged women, up to 50% in women with infertility and 70% in women with chronic pelvic pain

**PATHOGENESIS**: Retrograde menstruation, coelomic metaplasia, lymphatic/vascular dissemination, stem cells

**CLINICAL PRESENTATION**:
- **Pain**: Dysmenorrhea (painful periods), dyspareunia (deep dyspareunia), chronic pelvic pain, dyschezia (painful bowel movements), dysuria (painful urination)
- **Infertility**: 30-50% of women with endometriosis have infertility
- **Asymptomatic**: Incidental finding at surgery or imaging

**STAGING (rAFS - Revised American Fertility Society)**:
- **Stage I (Minimal)**: Few superficial implants
- **Stage II (Mild)**: More implants, some deeper
- **Stage III (Moderate)**: Endometriomas, adhesions
- **Stage IV (Severe)**: Large endometriomas, dense adhesions, extensive disease

**DIAGNOSIS**:
- **Clinical**: Based on symptoms, physical examination (nodularity in uterosacral ligaments, fixed retroverted uterus, adnexal masses)
- **Imaging**:
  - **Transvaginal ultrasound**: First-line, identifies endometriomas (chocolate cysts), deep infiltrating endometriosis, adenomyosis
  - **MRI**: For deep infiltrating endometriosis, complex disease, preoperative planning
- **Definitive**: Laparoscopy with histology (gold standard, but not always required before empirical treatment)

**MANAGEMENT**:

**Analgesia**:
- **NSAIDs**: First-line, take regularly starting 1-2 days before expected pain, inhibit prostaglandin production
- **Paracetamol**: Adjunct
- **Heat**: Warm bath, heating pad
- **Exercise**: May reduce pain severity

**Hormonal Treatments** (suppress endometriosis by causing decidualization and atrophy):
- **COCP**: First-line, continuous or cyclical (continuous often better), reduces dysmenorrhea, dyspareunia, chronic pain
- **Progestogens**: Norethisterone 10-15 mg daily; LNG-IUS (reduces dysmenorrhea, effective for superficial peritoneal disease, less effective for deep infiltrating or ovarian endometriomas)
- **GnRH agonists**: Leuprorelin, goserelin - induce medical menopause, highly effective, limited to 6 months due to bone loss, add "add-back" HRT (estrogen + progestogen) to preserve bone density
- **GnRH antagonists**: Elagolix, relugolix - oral, effective, expensive
- **Aromatase inhibitors**: Letrozole, anastrozole - for refractory cases, specialist initiation

**Surgical Management**:
- **Laparoscopic ablation/excision** of endometriosis implants: Removes visible disease, reduces pain, improves fertility (excision preferred over ablation for deep infiltrating disease)
- **Adhesiolysis**: Divide adhesions, reduce pain, may improve fertility
- **Endometrioma cystectomy**: Remove endometrioma wall (ovarian tissue preservation), recurrence risk 20-30%, may reduce ovarian reserve (AMH decreases)
- **Hysterectomy with bilateral salpingo-oophorectomy**: Definitive treatment, last resort for women who have completed fertility, hormone replacement required (estrogen alone if <50, consider add-back if symptoms recur)

**Infertility**:
- **Surgical treatment**: Improves fertility, especially in early stages (I-II)
- **IVF**: Recommended if:
  - Surgery fails or not appropriate (advanced age, diminished ovarian reserve, tubal damage)
  - Stage III-IV endometriosis with other infertility factors
  - Duration of infertility >2 years
- **Medical suppression** (GnRH agonists) before IVF: May improve outcomes

**Follow-up**:
- **Regular review**: Monitor symptoms, side effects of treatment
- **Bone density**: If prolonged GnRH agonist use
- **Psychological support**: Chronic pain, infertility impact mental health

**ADENOMYOSIS**

**DEFINITION**: Endometrial tissue within the myometrium (uterine muscle), causing hypertrophy and hyperplasia

**PREVALENCE**: 20-35% of women, increases with age

**RISK FACTORS**: Parity, prior uterine surgery, endometriosis

**CLINICAL PRESENTATION**:
- **Heavy menstrual bleeding** (80%)
- **Dysmenorrhea** (50-70%)
- **Menorrhagia** (prolonged, heavy periods)
- **Uterine enlargement** (boggy, globular)
- **Dyspareunia**

**IMAGING**:
- **Transvaginal ultrasound** (first-line):
  - Thickened junctional zone (>12 mm)
  - Myometrial cysts
  - Asymmetrical uterine wall thickening
  - Poor delineation of endometrial-myometrial border
- **MRI**: Gold standard, especially if coexisting fibroids or if surgery planned

**MANAGEMENT**:
- **Medical** (first-line):
  - **LNG-IUS**: First-line, reduces bleeding 90-95%, amenorrhea common, reduces dysmenorrhea
  - **COCP**: Regularizes cycles, reduces bleeding, dysmenorrhea
  - **Tranexamic acid**: Reduces bleeding, take during menses only
  - **NSAIDs**: Reduces bleeding, dysmenorrhea
- **Uterine artery embolization** (UAE): If adenomyosis with coexisting fibroids, reduces bleeding, preserves uterus
- **MRI-guided focused ultrasound (MRgFUS)**: Non-invasive thermal ablation, limited availability
- **Surgical**:
  - **Adenomyomectomy**: Remove adenomyosis (high recurrence, difficult surgery, specialist only)
  - **Hysterectomy**: Definitive treatment, last resort if medical fails and fertility complete

**Fertility**: Adenomyosis associated with infertility, but treatment may improve pregnancy rates

**SOURCES:** RCOG Green-top Guidelines, NICE, ESHRE
""",
            confidence=0.94,
            metadata={
                "specialty": "Women's Health",
                "focus": "Endometriosis and Adenomyosis",
                "sources": ["RCOG Green-top Guidelines", "NICE", "ESHRE"]
            }
        )

    def _handle_pms_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle PMS/PMDD queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**PREMENSTRUAL SYNDROME (PMS) AND PREMENSTRUAL DYSPHORIC DISORDER (PMDD)**

**DEFINITIONS**:

**PMS (Premenstrual Syndrome)**:
- Physical, emotional, and behavioral symptoms occurring in luteal phase (after ovulation)
- Resolve with menses
- Symptom-free week after menses

**PMDD (Premenstrual Dysphoric Disorder)**:
- Severe form of PMS
- Predominantly psychological symptoms
- Significant functional impairment
- Meets DSM-5 diagnostic criteria

**PREVALENCE**:
- PMS: Up to 80% of menstruating women (at least mild symptoms)
- Clinically significant PMS: 20-30%
- PMDD: 3-8%

**CLINICAL FEATURES**:

**Physical (PMS)**:
- Breast tenderness
- Abdominal bloating
- Weight gain (fluid retention)
- Headache
- Fatigue
- Food cravings
- Sleep disturbance
- Acne
- Musculoskeletal pain

**Emotional/Behavioral (PMDD predominance)**:
- Irritability, anger, mood swings
- Anxiety, tension
- Sadness, depressed mood, hopelessness
- Crying spells
- Decreased interest in activities
- Difficulty concentrating
- Increased appetite, food cravings
- Sleep disturbance
- Feeling overwhelmed or out of control
- Physical symptoms (similar to PMS)

**DIAGNOSIS**:
- **Prospective charting for 2-3 cycles**: Record symptoms daily (rating severity), confirm timing (luteal phase), confirm symptom-free interval after menses
- **PMDD diagnostic criteria (DSM-5)**:
  1. ≥5 symptoms (including at least 1 mood symptom: irritability, tension, dysphoria, mood lability) during final week before menses
  2. Symptoms improve within days of menses onset
  3. Symptom-free week after menses
  4. Symptoms cause significant distress/impairment
  5. Not exacerbation of another disorder
  6. Confirmed by prospective daily ratings for ≥2 symptomatic cycles

**DIFFERENTIAL DIAGNOSIS**:
- Depression (not cyclical, continuous symptoms)
- Anxiety disorders (not cyclical)
- Thyroid disorders
- Perimenopause (irregular cycles, other symptoms)
- Endometriosis (continuous pain)

**MANAGEMENT**:

**Lifestyle and Self-Help** (First-line for mild PMS):
- **Exercise**: Regular aerobic exercise (3-4 times/week) - most effective non-medical intervention
- **Diet**: Small frequent meals, reduce salt/sugar/caffeine/alcohol, complex carbohydrates, adequate protein, evening primrose oil (limited evidence)
- **Sleep hygiene**: Regular schedule, adequate sleep
- **Stress management**: Relaxation techniques, meditation, yoga
- **Cognitive behavioral therapy (CBT)**: Effective for mood symptoms, coping strategies
- **Sleep**: Regular schedule, adequate hours

**Supplements**:
- **Vitamin B6** (pyridoxine): 50-100 mg daily - evidence for mood symptoms, avoid >100 mg (neuropathy risk)
- **Calcium**: 1000-1200 mg daily - reduces physical and emotional symptoms
- **Magnesium**: 250-400 mg daily - may reduce bloating, mood symptoms
- **Vitamin E**: 400 IU daily - limited evidence
- **Agnus castus** (chasteberry): Herbal, some evidence for breast tenderness, irritability

**Hormonal Treatments** (for moderate-severe PMS/PMDD):

**COCP** (Combined Oral Contraceptive Pill):
- **Regimens**: Tricycling (3 months continuous, 7-day break), continuous (no breaks)
- **Benefits**: Suppresses ovulation, stabilizes hormone fluctuations
- **First-line**: Especially if contraception also needed
- **Specific formulations**: Drospirenone-containing COCP (Yasmin, Yaz) has FDA approval for PMDD

**SSRIs** (Selective Serotonin Reuptake Inhibitors):
- **First-line for PMDD** (especially mood symptoms)
- **Luteal phase dosing** (only during 2 weeks before menses): Sertraline 50 mg, fluoxetine 20 mg, paroxetine 10-20 mg, escitalopram 10 mg
- **Continuous dosing**: If luteal phase dosing insufficient or if luteal phase unclear
- **Rapid onset**: Improvement within first cycle, benefit maximal within 2 cycles
- **Side effects**: Nausea, insomnia, sexual dysfunction (usually mild with luteal phase dosing)

**SNRIs** (Serotonin-Norepinephrine Reuptake Inhibitors):
- **Venlafaxine**: 37.5-75 mg daily luteal phase or continuous
- **Duloxetine**: 20-60 mg daily luteal phase or continuous
- **Alternative** if SSRIs ineffective or not tolerated

**GnRH Agonists**:
- **Leuprorelin, goserelin**: Induce temporary menopause
- **Indications**: Severe, refractory PMDD unresponsive to other treatments
- **Add-back therapy**: Low-dose HRT to prevent bone loss
- **Limited to 6 months** due to bone density loss, not first-line

**Other Treatments**:
- **Spironolactone**: 50-100 mg daily - especially for bloating, breast tenderness (aldosterone antagonist, also anti-androgen)
- **Buspirone**: 10 mg TDS - for anxiety symptoms (non-benzodiazepine anxiolytic)
- **Evening primrose oil**: Gamma-linolenic acid (GLA) - limited evidence

**Surgical**:
- **Hysterectomy with bilateral oophorectomy**: Definitive, last resort for severe, refractory PMDD in women who have completed fertility
- **HRT required** after surgery
- **Consider**: Psychological assessment preoperatively, ensure all conservative measures exhausted

**FOLLOW-UP**:
- **Regular review**: Assess response, adjust treatment
- **Prospective symptom charts**: If treatment ineffective, confirm diagnosis
- **Mental health**: Screen for depression, anxiety, consider referral if comorbid

**PROGNOSIS**:
- **Improves**: After pregnancy, with age (perimenopause may worsen)
- **Resolves**: Menopause (symptoms cease with menses)
- **Chronic**: Many women have symptoms for years, management focuses on symptom control

**SOURCES:** NICE, RCOG, ACOG, DSM-5
""",
            confidence=0.93,
            metadata={
                "specialty": "Women's Health",
                "focus": "Premenstrual Syndrome and PMDD",
                "sources": ["NICE", "RCOG", "ACOG", "DSM-5"]
            }
        )

    def _handle_vaginal_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle vaginal discharge and vulvovaginal symptoms queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**VAGINAL DISCHARGE AND VULVOVAGINAL SYMPTOMS**

**NORMAL DISCHARGE**:
- **Physiological**: Clear or white, odorless or mild odor, varies with menstrual cycle
- **Cycle changes**: Increased mid-cycle (ovulation - clear, stretchy), pre-menstrual (thicker, whiter), pregnancy (increased)
- **External factors**: Sexual arousal, lubrication, semen

**ASSESSMENT**:
- **History**: Onset, duration, color, consistency, odor, itching, burning, pain, sexual activity, contraception, menstrual cycle, medications (antibiotics, steroids), hygiene practices
- **Examination**: Inspection of vulva, vagina, cervix (speculum), pH testing (normal 3.8-4.5), wet mount microscopy, whiff test (KOH)
- **Swabs**: High vaginal swab for culture/NAAT (chlamydia, gonorrhea), candidal microscopy/culture

**DIFFERENTIAL DIAGNOSIS**:

**Candidiasis (Thrush)**:
- **Pathogen**: Candida albicans (90%), other Candida species (10%)
- **Discharge**: Thick, white, curdy (cottage cheese), odorless
- **Symptoms**: Vulval itching, vulvovaginal soreness, dyspareunia, dysuria
- **Risk factors**: Antibiotics, pregnancy, diabetes, immunosuppression, COCP, tight clothing
- **pH**: Normal (3.8-4.5)
- **Diagnosis**: Microscopy (pseudohyphae, spores) or culture, or clinical diagnosis if classic presentation
- **Treatment**:
  - **Uncomplicated**: Clotrimazole 500 mg pessary stat OR fluconazole 150 mg oral stat (topical cream for vulval symptoms)
  - **Recurrent (>4 episodes/year)**: Exclude diabetes, immunosuppression, consider weekly fluconazole 150 mg for 6 months OR weekly clotrimazole for 6 months
  - **Pregnancy**: Topical azoles preferred (avoid oral fluconazole in first trimester)

**Bacterial Vaginosis (BV)**:
- **Pathogen**: Overgrowth of anaerobic bacteria (Gardnerella vaginalis, Mobiluncus, Prevotella), loss of lactobacilli
- **Discharge**: Thin, gray/white, homogeneous, **fishy odor** (especially after sex or with menses)
- **Symptoms**: Often asymptomatic (50%), malodorous discharge, occasionally itching
- **Risk factors**: Sexual activity (new partner, multiple partners), vaginal douching, smoking, IUD
- **pH**: Elevated (>4.5)
- **Whiff test**: Positive (fishy odor with KOH)
- **Clue cells**: Epithelial cells studded with bacteria on microscopy
- **Treatment**:
  - **First-line**: Metronidazole 400 mg BD for 5-7 days OR 2 g stat OR 0.75% vaginal gel daily for 5 days
  - **Recurrent**: Metronidazole gel twice weekly for 4-6 months OR consider oral clindamycin
  - **Pregnancy**: Symptomatic BV should be treated (risk of preterm birth), metronidazole 400 mg TDS for 7 days

**Trichomoniasis**:
- **Pathogen**: Trichomonas vaginalis (protozoan, STI)
- **Discharge**: Profuse, yellow/green, frothy, malodorous
- **Symptoms**: Vulval irritation, dyspareunia, dysuria, strawberry cervix (colpitis macularis - uncommon)
- **Risk factors**: STI, new/multiple sexual partners
- **pH**: Elevated (>4.5)
- **Diagnosis**: Wet mount (motile organisms), NAAT (highly sensitive)
- **Treatment**: Metronidazole 2 g stat OR 500 mg BD for 5-7 days (treat sexual partners, abstain 7 days after treatment)
- **Pregnancy**: Metronidazole safe after first trimester

**Cervicitis**:
- **Pathogens**: Chlamydia trachomatis, Neisseria gonorrhoeae
- **Discharge**: Mucopurulent (yellow/green), often asymptomatic
- **Symptoms**: Dysuria, intermenstrual bleeding, post-coital bleeding, pelvic pain
- **Signs**: Cervical ectropion (normal variant), mucopus, easily induced bleeding
- **Treatment**: Target pathogen (doxycycline 100 mg BD for 7 days for chlamydia, ceftriaxone 500 mg IM + azithromycin 1 g for gonorrhea), treat sexual partners

**Foreign body**:
- **Tampon**: Forgotten tampon (hours to weeks), foul-smelling discharge
- **Condom fragment**: Discharge, discomfort
- **Treatment**: Remove, consider antibiotics if secondary infection

**Atrophic vaginitis** (menopause):
- **Pathophysiology**: Decreased estrogen → thinning of vaginal epithelium, decreased glycogen → reduced lactobacilli → increased pH
- **Discharge**: Minimal or watery, often minimal
- **Symptoms**: Vaginal dryness, dyspareunia, vaginal soreness, burning, urinary symptoms (frequency, urgency, dysuria, recurrent UTIs)
- **pH**: Elevated (>5)
- **Treatment**: Vaginal estrogen (estriol cream, estradiol tablets, vaginal ring), vaginal moisturizers, lubricants for intercourse

**DESQUAMATIVE INFLAMMATORY VAGINITIS (DIV)**:
- **Rare**: Etiology unknown (possibly autoimmune)
- **Discharge**: Yellow/green purulent
- **Symptoms**: Vulvovaginal irritation, dyspareunia
- **Signs**: Vaginal erythema, epithelial cell stripping on microscopy
- **Treatment**: Clindamycin cream 2% nightly for 2-4 weeks, topical steroids

**VULVOVAGINAL CANDIDIASIS VS BV VS PHYSIOLOGICAL**:
| Feature | Candidiasis | BV | Physiological |
|---------|-------------|-----|---------------|
| Discharge | White, curdy | Gray, thin | Clear/white, variable |
| Odor | Minimal | Fishy | Minimal |
| Itching | Common | Rare | No |
| pH | Normal (3.8-4.5) | High (>4.5) | Normal (3.8-4.5) |
| Whiff test | Negative | Positive | Negative |

**HYGIENE ADVICE**:
- **Do NOT douche**: Disrupts normal flora, increases BV risk
- **Gentle cleansing**: Water or unperfumed soap, avoid harsh soaps, bubble baths
- **Pat dry**: Avoid rubbing
- **Cotton underwear**: Breathable, avoid thongs (spread bacteria)
- **Avoid tight clothing**: Increases moisture, heat
- **Wipe front to back**: Prevent fecal contamination
- **Urinate after sex**: Reduces UTI risk
- **Change tampons/pads regularly**: Avoid toxic shock syndrome

**SEXUAL HEALTH**:
- **STI screen**: New partner, multiple partners, symptoms suggestive (discharge, bleeding, dyspareunia)
- **Condom use**: Reduces STI transmission

**WHEN TO REFER**:
- **Persistent symptoms**: Despite treatment, consider referral for further investigation
- **Postmenopausal bleeding**: ALWAYS refer (2-week wait, endometrial cancer until proven otherwise)
- **Cervical cancer**: Abnormal cervical cytology, visible lesion, referral for colposcopy
- **Pelvic inflammatory disease**: Systemic symptoms, adnexal tenderness, cervical motion tenderness
- **Recurrent infections**: Consider diabetes, immunosuppression, anatomical abnormalities

**SOURCES:** BASHH, NICE, FSRH
""",
            confidence=0.94,
            metadata={
                "specialty": "Women's Health",
                "focus": "Vaginal Discharge and Vulvovaginal Conditions",
                "sources": ["BASHH", "NICE", "FSRH"]
            }
        )

    def _handle_breast_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle breast symptom queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**BREAST HEALTH AND SYMPTOMS**

**BREAST PAIN (MASTALGIA)**:

**Cyclical mastalgia** (70%):
- **Timing**: Related to menstrual cycle, worst before menses, improves after menses
- **Symptoms**: Bilateral, diffuse, heavy, aching, may radiate to axilla
- **Age**: 30-40 years most common
- **Management**: Reassurance, well-fitting bra, weight loss if overweight, reduce caffeine (limited evidence), evening primrose oil (limited evidence), consider danazol (not first-line due to side effects), consider tamoxifen (specialist)

**Non-cyclical mastalgia** (30%):
- **Timing**: Not related to menstrual cycle
- **Symptoms**: Unilateral, localized, burning, sharp
- **Causes**: Trauma, infection (mastitis), costochondritis (Tietze's), chest wall strain, medication-induced (HRT, COCP), large breast size (macromastia)
- **Management**: Treat underlying cause, analgesia, NSAIDs, consider referral for imaging if localized

**BREAST LUMP**:

**BENIGN CONDITIONS** (90% of breast lumps):
- **Fibroadenoma**: Benign breast tumor, rubbery, mobile, smooth, well-circumscribed, age 15-35, no increased cancer risk, management: observation (may regress), excision if growing or symptomatic
- **Breast cyst**: Fluid-filled sac, smooth, mobile, may be tender, age 35-50, aspiration if symptomatic/imperative, mammography/ultrasound if complex or recurrent
- **Fat necrosis**: After trauma, surgery, biopsy, feels hard/irregular, mimics cancer, biopsy for diagnosis
- **Sclerosing adenosis**: Benign proliferation, may present as lump or calcifications, biopsy for diagnosis

**BREAST CANCER RED FLAGS**:
- **Hard, irregular lump**: Fixed to underlying tissues
- **Skin changes**: Dimpling (peau d'orange), nipple retraction, ulceration
- **Nipple discharge**: Blood-stained, spontaneous, unilateral, persistent
- **Nipple eczema**: Paget's disease (unilateral, unresponsive to topical steroids)
- **Axillary lymphadenopathy**: Hard, fixed, painless
- **Age**: Risk increases with age (postmenopausal)

**IMAGING**:
- **<35 years**: Ultrasound first (mammography less sensitive due to dense breast tissue)
- **≥35 years**: Mammography ± ultrasound (3-view mammogram if symptom, ultrasound if mammogram dense/inconclusive)
- **If suspicious**: Core biopsy (14G) for histology

**NIPPLE DISCHARGE**:

**Physiological**:
- **Color**: Green/yellow/milky, bilateral, multi-duct, spontaneous or expressed
- **Causes**: Duct ectasia, hormonal (pregnancy, lactation, hypothyroidism), medications (antipsychotics, antidepressants, COCP, HRT)

**Pathological** (refer):
- **Blood-stained** (spontaneous, unilateral): Intraductal papilloma, DCIS, cancer
- **Single duct**: Intraductal papilloma, DCIS, cancer
- **Associations**: Breast lump, skin changes, nipple eczema

**Investigation**:
- **If bloody or single duct**: Mammogram + ultrasound + duct excision (microdochectomy)
- **If bilateral/multi-duct/non-bloody**: Consider prolactin, TSH, medications

**BREAST SCREENING** (Asymptomatic Women):
- **Mammography**: 2-view (CC, MLO), every 3 years (UK), ages 50-70 (50-74 in some areas)
- **Purpose**: Detect breast cancer early, reduce mortality
- **Sensitivity**: 85-90% (lower in dense breasts)
- **Risks**: Radiation (minimal), false positives (recall, biopsies), overdiagnosis

**FAMILY HISTORY**:
- **Significant family history**:
  - 1 first-degree relative <40
  - 2 first-degree or second-degree relatives on same side <50
  - 3+ relatives on same side with breast/ovarian cancer
  - Male breast cancer
  - Ashkenazi Jewish ancestry
  - Known BRCA1/2 mutation
- **Refer**: Clinical genetics, consider BRCA testing, enhanced screening (MRI)
- **Risk-reducing strategies**: Tamoxifen/raloxifene, risk-reducing mastectomy, risk-reducing oophorectomy

**BREAST CANCER RISK FACTORS**:
- **Non-modifiable**: Female sex, age, genetics (BRCA1/2, TP53, PTEN, PALB2), family history, benign breast disease (atypical hyperplasia), radiation exposure
- **Modifiable**: Alcohol (increases risk), obesity (postmenopausal), HRT (combined HRT increases risk, estrogen-only does not), COCP (slight increase but returns to baseline after stopping), nulliparity or late first pregnancy, early menarche, late menopause
- **Protective**: Exercise, breastfeeding, parity, young age at first pregnancy

**MASTITIS** (Breast Infection):
- **Causes**: Lactation (stasis, cracked nipple), non-lactational (periductal mastitis, smoker's risk)
- **Symptoms**: Breast pain, redness, heat, swelling, fever, malaise
- **Treatment**: Antibiotics (flucloxacillin 500 mg QDS or co-amoxiclav, erythromycin if penicillin allergy), continue breastfeeding (if lactational) or express, supportive measures (analgesia, cold compresses, rest)
- **Complications**: Breast abscess (if not improving after 48 hours antibiotics → ultrasound ± aspiration/incision and drainage)

**FIBROCYSTIC CHANGES**:
- **Premenstrual**: Breast fullness, lumpiness, pain
- **Benign**: No increased cancer risk
- **Management**: Reassurance, well-fitting bra, analgesia (NSAIDs), reduce caffeine (limited evidence)

**SOURCES:** NICE, RCOG, ABS (Association of Breast Surgery)
""",
            confidence=0.93,
            metadata={
                "specialty": "Women's Health",
                "focus": "Breast Health",
                "sources": ["NICE", "RCOG", "ABS"]
            }
        )

    def _handle_cervical_screening_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle cervical screening queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**CERVICAL SCREENING AND HPV**

**CERVICAL CANCER**:
- **Cause**: Persistent infection with high-risk human papillomavirus (HPV), especially types 16 and 18 (70% of cancers)
- **Progression**: HPV infection → cervical intraepithelial neoplasia (CIN) → invasive cancer (usually 10-20 years, allows screening)
- **Risk factors**: HPV infection (most common STI), smoking, immunosuppression (HIV, transplant), early sexual activity, multiple partners, high parity, long-term COCP use (slight increase)
- **Protection**: HPV vaccination, cervical screening

**HPV VACCINATION**:
- **UK**: Girls and boys aged 12-13 years (school year 8), two-dose schedule (6-12 months apart), catch-up until age 25
- **Vaccine**: Gardasil 9 (protects against HPV 16, 18 (cervical cancer) + 31, 33, 45, 52, 58 (cancer) + 6, 11 (genital warts))
- **Efficacy**: >90% protection against HPV 16/18-related CIN2+, reduces cervical cancer incidence
- **Catch-up**: Women <25 not vaccinated, can request vaccination (3 doses if >15)

**CERVICAL SCREENING PROGRAMME**:
- **Ages**: 25-49 years: every 3 years; 50-64 years: every 5 years
- **Purpose**: Detect and treat CIN to prevent cervical cancer
- **Test**: Liquid-based cytology (LBC) with HPV testing (primary HPV screening in UK)
- **Procedure**: Speculum examination, cells collected from transformation zone using brush/spatula, sent to lab

**PRIMARY HPV SCREENING** (UK):
- **HPV negative**: Return to routine recall (3 or 5 years)
- **HPV positive**:
  - **HPV 16/18** (highest risk): Immediate colposcopy
  - **HPV other types** (non-16/18): Cytology triage
    - **Normal/Negative**: Repeat HPV + cytology in 12 months
    - **Abnormal (borderline/dyskaryosis)**: Colposcopy

**ABNORMAL CYTOLOGY** (Historical terminology, still used in reporting):
- **Borderline changes**: Low risk, return to routine screening or repeat in 12 months
- **Mild dyskaryosis**: CIN1 (low-grade), may return to routine screening or colposcopy
- **Moderate dyskaryosis**: CIN2 (high-grade), colposcopy
- **Severe dyskaryosis**: CIN3 (high-grade), colposcopy

**CIN (Cervical Intraepithelial Neoplasia)**:
- **CIN1**: Mild dysplasia, low-grade, 30% progress to CIN2/3, many regress
- **CIN2**: Moderate dysplasia, high-grade, 5% progress to cancer if untreated, 40% regress
- **CIN3**: Severe dysplasia, high-grade, 12% progress to cancer if untreated

**COLPOSCOPY** (Detailed examination of cervix with magnification):
- **Indications**: Abnormal screening result, persistent HPV infection, visible lesion
- **Procedure**: Speculum, acetic acid (3-5%) application, iodine solution, colposcope (binocular microscope), biopsy of abnormal areas
- **Treatment** (if CIN2/3 confirmed):
  - **Large loop excision of transformation zone (LLETZ)**: Most common, wire loop with diathermy, remove abnormal area, 90% cure with single treatment
  - **Cold coagulation**: Heat treatment, outpatient, for smaller lesions
  - **Cone biopsy**: Knife excision for glandular disease or unsatisfactory colposcopy
  - **Hysterectomy**: If completed fertility and persistent/recurrent disease, or invasive cancer

**POST-TREATMENT FOLLOW-UP**:
- **Cytology + HPV testing**: 6 months after treatment, then annually for 10 years (negative HPV = cured)
- **Pregnancy**: Fertility generally preserved, slight increase in preterm birth, mid-trimester loss (especially after cone biopsy)

**SYMPTOMATIC CERVICAL CANCER**:
- **Symptoms**: Post-coital bleeding, intermenstrual bleeding, postmenopausal bleeding, vaginal discharge (offensive, blood-stained), pelvic pain, leg swelling (lymphedema), urinary frequency, constipation (advanced)
- **Signs**: Visible exophytic lesion on cervix, ulcerative/necrotic lesion, barrel-shaped cervix (advanced)
- **Investigation**: Urgent referral (2-week wait), colposcopy with biopsy, imaging (MRI, PET-CT for staging)

**COLPOSCOPY IN PREGNANCY**:
- **Safe**: No increased miscarriage risk
- **Conservative**: Defer treatment until postpartum if possible (CIN often regresses)
- **Treatment only if**: Microinvasive cancer on biopsy (rare)

**WHEN SCREENING STOPS**:
- **Age 65**: If last 3 tests negative and no abnormal results in past 10 years
- **Hysterectomy**: If cervix removed AND no prior CIN2/3 (can stop screening)

**INCREASED RISK** (More frequent screening):
- **HIV positive**: Annual screening
- **Immunosuppressed** (transplant, steroids, other immunosuppressants): Annual screening
- **Previous CIN2/3**: Annual screening for 10 years after treatment
- **DES exposure** (in utero): Annual screening

**PATIENT CONCERNS**:
- **Embarrassment**: Common, nurses trained, offer chaperone, explain procedure, offer appointment with female smear taker
- **Discomfort**: Use smallest speculum, warm speculum, lubricant, patient-controlled insertion (if appropriate), breathing exercises
- **Anxiety**: Explain results clearly, provide written information, ensure understanding

**DECREASED ATTENDANCE**:
- **Barriers**: Embarrassment, discomfort, fear, cultural, practical (work, childcare), lack of knowledge, previous bad experience
- **Solutions**: Flexible appointments, female smear taker, chaperone, education, reminders, self-sampling (future)

**SOURCES:** NHS Cervical Screening Programme, NICE, BSCCP
""",
            confidence=0.96,
            metadata={
                "specialty": "Women's Health",
                "focus": "Cervical Screening and HPV",
                "sources": ["NHS Cervical Screening Programme", "NICE", "BSCCP"]
            }
        )

    def _handle_sexual_health_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sexual health and dysfunction queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**WOMEN'S SEXUAL HEALTH AND DYSFUNCTION**

**FEMALE SEXUAL DYSFUNCTION** (Prevalence: up to 40%):
- **Hypoactive sexual desire disorder (HSDD)**: Reduced/absent sexual desire causing distress
- **Sexual arousal disorder**: Inability to achieve/maintain arousal/lubrication
- **Orgasmic disorder**: Difficulty achieving orgasm despite adequate arousal
- **Sexual pain disorders**: Dyspareunia (painful intercourse), vaginismus (involuntary vaginal muscle spasm preventing penetration)

**DYSPAREUNIA (Painful Intercourse)**:

**Superficial dyspareunia** (introital pain):
- **Causes**:
  - **Vaginal atrophy** (menopause, breastfeeding): Dryness, loss of elasticity, thinning epithelium
  - **Vulvovaginal candidiasis**: Itching, soreness, discharge
  - **Vestibulodynia** (provoked vestibulodynia, formerly vulvar vestibulitis): Severe pain at vestibule on touch (tampon insertion, intercourse), unknown etiology
  - **Lichen sclerosus**: White plaques, vulvar atrophy, itching, pain (increased squamous cell cancer risk)
  - **Lichen planus**: Erosive vulvovaginal inflammation, pain, bleeding
  - **Vaginismus**: Involuntary spasm preventing penetration, often psychological/trauma-related
  - **Postpartum**: Perineal trauma (episiotomy, tear), scar tissue, breastfeeding (atrophic changes)
- **Management**: Treat underlying cause (vaginal estrogen for atrophy, antifungal for candidiasis, topical steroids for lichen sclerosus), vaginal dilators (vaginismus), pelvic floor physiotherapy (vaginismus, vestibulodynia), CBT, psychosexual therapy, lubricants during intercourse

**Deep dyspareunia** (deep pelvic pain):
- **Causes**:
  - **Endometriosis**: Dyspareunia (often deep), dysmenorrhea, chronic pelvic pain
  - **Adenomyosis**: Heavy bleeding, dysmenorrhea, uterine enlargement
  - **Pelvic inflammatory disease** (PID): Lower abdominal pain, cervical motion tenderness, vaginal discharge
  - **Ovarian cysts**: Sudden onset pain if rupture/torsion, or chronic pain
  - **Uterine fibroids**: Heavy bleeding, bulk symptoms, dysmenorrhea
  - **Adhesions**: Previous surgery/appendicitis/pelvic infection causing scar tissue
  - **Interstitial cystitis** (painful bladder syndrome): Suprapubic pain, urinary frequency, urgency, dyspareunia
  - **Irritable bowel syndrome** (IBS): Worsened by intercourse, associated with bowel symptoms
- **Management**: Treat underlying cause, analgesia, hormonal treatments (COCP, GnRH agonists for endometriosis), surgery (adhesiolysis, myomectomy), physiotherapy

**LOW LIBIDO (HSDD)**:

**Causes**:
- **Hormonal**: Menopause (low estrogen, low testosterone), postpartum (prolactin, low estrogen), COCP (reduced free testosterone)
- **Psychological**: Depression, anxiety, stress, relationship issues, body image, past trauma/abuse
- **Medications**: SSRIs/SNRIs (most common), antipsychotics, antihypertensives, COCP (some women)
- **Medical**: Chronic illness, fatigue, pain
- **Lifestyle**: Fatigue, stress, sleep deprivation, childcare, work-life balance

**Management**:
- **Address reversible causes**: Treat depression/anxiety, switch/stop offending medications (with specialist input), optimize hormones
- **Relationship counseling**: Address relationship issues, communication
- **Psychosexual therapy**: CBT-based, sensate focus techniques, behavioral therapy
- **Testosterone**: For HSDD in postmenopausal women (off-label in UK, FDA-approved in US), consider if other causes addressed, 1% gel 0.5-1 g daily (aim premenopausal levels), monitor for side effects (acne, hirsutism, alopecia), 6-month trial, reassess
- **Flibanserin**: (Addyi) FDA-approved for premenopausal HSDD, not available in UK (NICE not recommended)
- **Bupropion**: (Wellbutrin) antidepressant with less sexual side effects, may improve libido (off-label)

**ORGASMIC DISORDER**:

**Causes**:
- **Psychological**: Anxiety, distraction, cultural/religious beliefs, past trauma
- **Medical**: Diabetes (neuropathy), MS, spinal cord injury
- **Medications**: SSRIs (most common), antipsychotics
- **Hormonal**: Menopause (reduced clitoral sensitivity)

**Management**:
- **Education**: Normal anatomy, clitoral stimulation
- **Self-exploration**: Masturbation, vibrators
- **Psychosexual therapy**: CBT, sensate focus
- **Pelvic floor exercises**: Improve pelvic floor tone and orgasmic intensity
- **Switch medications** (if SSRIs): Bupropion, mirtazapine

**VAGINISMUS**:

**Diagnosis**: Inability to achieve vaginal penetration due to involuntary muscle spasm, causing distress, not due to another medical condition

**Primary vaginismus**: Never achieved penetration
**Secondary vaginismus**: Previously achieved penetration, now unable

**Causes**: Fear/anxiety, past sexual abuse/assault, painful intercourse (dyspareunium), cultural/religious beliefs, lack of sex education, relationship issues

**Management**:
- **First-line**: Pelvic floor physiotherapy with vaginal dilators (graduated sizes), psychosexual counseling
- **CBT**: Address fear/anxiety, negative thought patterns
- **Botox injections**: (refractory cases) into pelvic floor muscles, specialist
- **Dilators**: Used regularly at home, gradually increasing size, combined with relaxation techniques

**LICHEN SCLEROSUS**:
- **Chronic inflammatory dermatosis**: Vulvar, perineal, perianal area
- **Symptoms**: Itching (often severe), soreness, dyspareunia, dysuria, architectural changes (labial resorption, clitoral burial, introital stenosis)
- **Signs**: White atrophic plaques, parchment-like skin, purpura (bruising), fissuring
- **Risk**: Squamous cell carcinoma (4-5%, especially if untreated)
- **Treatment**: Ultra-potent topical corticosteroid (clobetasol propionate 0.05%) ointment daily initially, then taper to maintenance (2-3 times/week), long-term treatment required, regular follow-up, biopsy if suspicious lesions or poor response
- **Surgery**: Perineotomy if introital stenosis preventing intercourse (after disease controlled)

**VAGINAL ATROPHY** (GSM - Genitourinary Syndrome of Menopause):
- **Symptoms**: Vaginal dryness, dyspareunia, vaginal burning/itching, urinary symptoms (frequency, urgency, dysuria, recurrent UTIs)
- **Signs**: Pale, dry vaginal mucosa, loss of rugae, petechiae
- **Treatment**: Vaginal estrogen (first-line) - estradiol tablets 10 mcg, estriol cream, vaginal ring (Estring), improve symptoms within weeks, safe for long-term use, minimal systemic absorption, can use alongside systemic HRT, lubricants during intercourse (water-based, silicone-based)

**POSTPARTUM SEXUAL HEALTH**:
- **Timing**: Wait until bleeding stopped (usually 6 weeks), perineal tears/episiotomy healed (pain settled), comfortable
- **Breastfeeding**: Low estrogen → vaginal atrophy, dryness, use vaginal estrogen if needed
- **Dyspareunium**: Perineal pain (episiotomy/tear), vaginal dryness, C-section scar pain, pelvic floor weakness
- **Contraception**: Discuss if not planning another pregnancy immediately (progestogen-only if breastfeeding)

**SOURCES:** NICE, BASHH, ISSWSH
""",
            confidence=0.93,
            metadata={
                "specialty": "Women's Health",
                "focus": "Sexual Health and Dysfunction",
                "sources": ["NICE", "BASHH", "ISSWSH"]
            }
        )

    def _handle_pelvic_floor_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pelvic floor and incontinence queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**PELVIC FLOOR DISORDERS AND URINARY INCONTINENCE**

**PELVIC FLOOR ANATOMY**:
- **Levator ani muscles**: Puborectalis, pubococcygeus, iliococcygeus (support pelvic organs, maintain continence)
- **Endopelvic fascia**: Connective tissue support
- **Pudendal nerve**: Innervates pelvic floor, external anal sphincter, perineum

**PELVIC FLOOR DYSFUNCTION**:
- **Causes**: Pregnancy, vaginal delivery (especially instrumental - forceps/ventouse), menopause (estrogen deficiency), aging, obesity, chronic straining (constipation), chronic cough, heavy lifting, high-impact exercise, genetics (connective tissue disorders)
- **Consequences**: Urinary incontinence, fecal incontinence, pelvic organ prolapse, sexual dysfunction

**URINARY INCONTINENCE** (Prevalence: 30-50% lifetime risk)

**Stress urinary incontinence (SUI)** (50%):
- **Symptoms**: Leakage with increased intra-abdominal pressure (cough, sneeze, exercise, laugh, position change)
- **Pathophysiology**: Urethral hypermobility (displacement of urethra/bladder neck) OR intrinsic sphincter deficiency (weak sphincter)
- **Risk factors**: Childbirth (especially instrumental), menopause, age, obesity, smoking, chronic cough, high-impact exercise
- **Management**:
  - **First-line**: Weight loss if overweight, pelvic floor muscle training (PFMT) - 3 months supervised, reduce caffeine/fluid management
  - **Second-line**: Vaginal estrogen (if postmenopausal) - improves vaginal tissues, enhances PFMT efficacy
  - **Third-line**: Surgical (if conservative fails)
    - **Mid-urethral slings** (TVT, TOT): 80-90% cure, day case, rapid recovery
    - **Colposuspension** (Burch): Open or laparoscopic, slightly less effective than slings
    - **Bulking agents**: Periurethral injections (less effective, repeat procedures, lower morbidity)
    - **Autologous fascial sling**: For recurrent or failed sling surgery

**Urge urinary incontinence (UUI)** (20%):
- **Symptoms**: Sudden, intense urge to void, leakage before reaching toilet, frequency, nocturia
- **Pathophysiology**: Detrusor overactivity (idiopathic or neurogenic), bladder hypersensitivity
- **Management**:
  - **First-line**: Bladder training (increase voiding interval, suppress urge), lifestyle modifications (caffeine, fluid, weight loss)
  - **Second-line**: Anticholinergics (oxybutynin, tolterodine, solifenacin, darifenacin) OR mirabegron (beta-3 agonist), monitor for anticholinergic burden (dry mouth, constipation, confusion)
  - **Third-line**: Botulinum toxin A injections into detrusor (specialist), requires self-catheterization if urinary retention, tibial nerve stimulation, sacral neuromodulation

**Mixed urinary incontinence (MUI)** (30%):
- **Symptoms**: Both stress and urge symptoms
- **Management**: Treat predominant component first (usually SUI), PFMT + bladder training, anticholinergics if urge symptoms predominate, surgery if SUI predominates and conservative fails

**PELVIC ORGAN PROLAPSE (POP)** (Prevalence: 50% of parous women, 10-20% symptomatic)

**Anterior wall prolapse (Cystocele)**:
- **Symptoms**: Vaginal bulge, sensation of something coming down, incomplete bladder emptying, stress urinary incontinence (occasionally occult incontinence - stress leakage only when prolapse reduced), recurrent UTIs, urinary frequency
- **Management**: Pessary (ring or shelf), pelvic floor physiotherapy, anterior colporrhaphy (surgical repair)

**Posterior wall prolapse (Rectocele)**:
- **Symptoms**: Vaginal bulge, incomplete bowel emptying, straining to defecate, digital evacuation of stool, constipation
- **Management**: Pessary, pelvic floor physiotherapy, posterior colporrhaphy (surgical repair)

**Apical prolapse (Uterine or vault prolapse)**:
- **Uterine prolapse**: Uterus descends into vagina
- **Vault prolapse**: After hysterectomy, vaginal vault descends (small bowel may enter - enterocele)
- **Symptoms**: Vaginal bulge, sensation of heaviness/dragging, low backache, difficulty walking, ulceration (if prolonged)
- **Staging** (POP-Q system): Stage 0 (no prolapse) to Stage 4 (complete eversion)
- **Management**: Pessary (ring, shelf, Gellhorn), pelvic floor physiotherapy (mild), surgery:
  - **Uterine preservation**: Sacrospinous ligament fixation (SSLF), uterosacral ligament suspension (USLS)
  - **Hysterectomy** (with sacrocolpopexy or sacrospinous fixation)
  - **Sacrocolpopexy** (vault prolapse): Abdominal mesh (gold standard for apical prolapse)
  - **Vaginal mesh**: NOT recommended (transvaginal mesh complications - pain, erosion, dyspareunia)

**PESSARIES**:
- **Types**: Ring (most common, can stay in 3-6 months), shelf (for more severe prolapse), Gellhorn (for severe prolapse, high suction), donut (for vault prolapse)
- **Management**: Fitting by healthcare provider, teach self-removal and cleaning (or change every 3-6 months), topical estrogen (if postmenopausal)
- **Contraindications**: Active infection, severe vaginal atrophy (treat first), unlikely to be retained/used

**PELVIC FLOOR MUSCLE TRAINING (PFMT)**:
- **Indications**: Stress urinary incontinence, urge urinary incontinence, pelvic organ prolapse (mild), prevention (postpartum, postmenopausal)
- **Technique**: Identify pelvic floor muscles (stop urine flow - do NOT do regularly), squeeze and lift (like holding gas), hold 3-10 seconds, relax, repeat 8-12 times, 3 times/day for 3-6 months
- **Supervised**: Better adherence and outcomes (physiotherapist, biofeedback, electrical stimulation)
- **Maintenance**: Continue lifelong after initial 3-6 months

**PELVIC FLOOR PHYSIOTHERAPY**:
- **Assessment**: Vaginal examination (muscle strength 0-5, Oxford scale), assess prolapse, assess ability to contract/relax
- **Interventions**: PFMT (supervised), biofeedback (visual or auditory feedback on muscle contraction), electrical stimulation (for weak muscles), vaginal weights (cones), bladder training (for urgency)
- **Indications**: Stress/urge/mixed incontinence, prolapse, preoperative (optimize outcomes), postpartum (prevent dysfunction), postmenopausal (maintain function)

**FECAL INCONTINENCE**:
- **Prevalence**: 10% (increases with age)
- **Causes**: Obstetric trauma (third/fourth degree tear - anal sphincter injury), sphincter weakness, pudendal neuropathy (prolonged second stage, forceps delivery), IBD, diarrhea, overflow fecal impaction
- **Management**: Pelvic floor physiotherapy, biofeedback, dietary modifications (fiber, fluid), antidiarrheals (if diarrhea), sacral nerve stimulation (refractory), sphincter repair (if sphincter defect)

**POSTPARTUM PELVIC FLOOR CARE**:
- **Assessment**: At 6-week postpartum review, ask about incontinence, prolapse symptoms, dyspareunia
- **PFMT**: Advise all women (even if asymptomatic), teach technique, refer to physiotherapist if symptomatic
- **Third/fourth degree tear**: Review in perineal clinic, pelvic floor physiotherapy, consider defecation proctogram if symptoms persist, sphincter repair if sphincter disruption confirmed

**WHEN TO REFER**:
- **New onset incontinence** (exclude red flags: hematuria, recurrent UTIs, constant leakage)
- **Prolapse symptomatic**: Refer to gynecology
- **Failed conservative management** (PFMT for 3-6 months)
- **Surgical consideration**: For incontinence or prolapse
- **Complex cases**: Previous surgery, recurrent prolapse, mesh complications

**SOURCES:** NICE CG171, IUGA, ICS
""",
            confidence=0.94,
            metadata={
                "specialty": "Women's Health",
                "focus": "Pelvic Floor Disorders and Urinary Incontinence",
                "sources": ["NICE CG171", "IUGA", "ICS"]
            }
        )

    def _handle_preconception_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle preconception counseling queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**PRECONCEPTION COUNSELING**

**GOAL**: Optimize health BEFORE conception to improve pregnancy outcomes, reduce complications, prevent birth defects

**TIMING**: Ideally 3-6 months before trying to conceive

**FOLIC ACID SUPPLEMENTATION**:
- **Dose**: 400 mcg (0.4 mg) daily starting at least 1 month before conception, continue until 12 weeks pregnancy
- **High dose (5 mg daily)**: If diabetes, epilepsy, obesity (BMI >30), previous child with neural tube defect, taking anti-folate medications (valproate, carbamazepine), family history of neural tube defects, malabsorption (celiac, IBD)
- **Neural tube defects**: Anencephaly, spina bifida, encephalocele - closure by day 28 post-conception (often before pregnancy recognized)

**MEDICATION REVIEW**:
- **Stop teratogens**: Isotretinoin (acne), thalidomide, methotrexate, warfarin (switch to LMWH), ACE inhibitors/ARBs (switch to labetalol/nifedipine), statins, tetracyclines, fluoroquinolones, sodium valproate (transition to safer alternative), carbamazepine (if possible)
- **Optimize chronic diseases**: Hypertension (target <140/90), diabetes (tight glucose control, HbA1c <6.5% if possible), epilepsy (monotherapy if possible, lowest effective dose, choose safest agent - lamotrigine preferred), thyroid disease (TSH 0.5-2.5 mIU/L), depression (continue effective treatment, consider safer options)

**CHRONIC DISEASE MANAGEMENT**:
- **Diabetes**: Preconception counseling vital, target HbA1c <6.5% (reduce congenital anomalies, miscarriage), optimize medications (stop ACE inhibitors/ARBs/statins, switch insulin), retinal screening (worsens in pregnancy), nephropathy assessment
- **Hypertension**: Medication review (stop ACE inhibitors/ARBs, switch to labetalol, nifedipine, methyldopa), target <140/90, assess for end-organ damage
- **Epilepsy**: Review medication (valproate highest risk - avoid if possible, lamotrigine preferred), folic acid 5 mg, monitor levels, counsel on risks (major malformations 4-9% vs 2-3% baseline)
- **Thyroid disease**: TSH target 0.5-2.5 mIU/L, adjust thyroxine dose (usually need 30-50% increase early pregnancy), autoimmune thyroiditis - no change in management
- **Obesity**: Weight loss before pregnancy reduces gestational diabetes, pre-eclampsia, macrosomia, stillbirth, cesarean section
- **Mental health**: Continue effective treatment (untreated depression/anxiety also risky), consider medication safety (SSRIs generally safe, avoid paroxetine if possible, avoid valproate in bipolar), consider CBT

**IMMUNIZATIONS**:
- **Rubella**: Check immunity, vaccinate if non-immune (MMR), avoid pregnancy for 1 month after vaccination
- **Varicella**: Check immunity (especially healthcare workers), vaccinate if non-immune, avoid pregnancy for 1 month after vaccination
- **Hepatitis B**: Vaccinate if at risk (healthcare worker, travel, partner positive)
- **Influenza**: Annual vaccination (safe in pregnancy, recommended)
- **COVID-19**: Vaccination recommended before pregnancy (safe in pregnancy but better before)
- **NOT in pregnancy**: Live vaccines (MMR, varicella, yellow fever)

**INFECTIONS**:
- **STI screen**: Chlamydia, gonorrhea (especially if <25, new partner, multiple partners), HIV, syphilis
- **Hepatitis B/C**: Screen if at risk
- **Toxoplasmosis**: Avoid cat litter (or wear gloves), avoid undercooked meat, wash fruits/vegetables
- **CMV**: Hand hygiene (especially around young children), avoid sharing utensils with young children
- **Listeria**: Avoid unpasteurized dairy, soft cheeses (brie, camembert), deli meats, pâté

**LIFESTYLE MODIFICATIONS**:
- **Smoking cessation**: Quit completely (increases miscarriage, ectopic, placental abruption, preterm birth, low birth weight, stillbirth, SIDS), offer NRT (nicotine replacement therapy) if needed, provide support
- **Alcohol**: Avoid completely (no safe level, fetal alcohol spectrum disorders, miscarriage, stillbirth)
- **Caffeine**: Limit to <200 mg/day (1-2 cups of coffee), higher levels associated with miscarriage, low birth weight
- **Weight**: Aim BMI 18.5-25, weight loss if overweight/obese reduces gestational diabetes, pre-eclampsia, macrosomia, stillbirth, cesarean
- **Diet**: Balanced diet, avoid shark, swordfish, marlin (high mercury), limit tuna (2 steaks/week), avoid raw/undercooked meat/eggs (toxoplasmosis, salmonella), avoid unpasteurized dairy, avoid soft cheeses unless pasteurized
- **Exercise**: Regular moderate exercise (150 min/week), avoid high-impact sports with risk of trauma, avoid hot yoga (overheating)

**FAMILY HISTORY**:
- **Genetic conditions**: Cystic fibrosis, sickle cell, thalassemia, Tay-Sachs, Canavan disease - carrier screening if indicated (ethnicity, family history)
- **Chromosomal abnormalities**: Previous child with Down syndrome, parental translocation - refer to genetics
- **Single gene disorders**: Huntington's, Duchenne, hemophilia - refer to genetics
- **BRCA1/2**: Personal/family history of breast/ovarian cancer - refer to genetics, discuss implications for pregnancy (timing, testing)

**RECURRENT MISCARRIAGE** (>2 consecutive):
- **Investigate**: Antiphospholipid antibodies (lupus anticoagulant, anticardiolipin, anti-beta2 glycoprotein), parental karyotype (translocation), uterine anatomy (HSG, 3D ultrasound), thrombophilia screen (if indicated)
- **Management**: Aspirin 75 mg + heparin (if antiphospholipid syndrome), progesterone (some evidence for vaginal micronized progesterone 400 mg BD), surgery (septum, adhesions), lifestyle modifications

**AGE AND FERTILITY**:
- **Fertility**: Declines after age 35, more rapidly after 40 (decreased ovarian reserve, increased aneuploidy)
- **Risks**: Miscarriage (15% age 20-35, 50% age 40+), chromosomal abnormalities (Down syndrome 1:1000 at age 20, 1:100 at age 40), gestational diabetes, pre-eclampsia, stillbirth
- **Counseling**: Discuss age-related risks, offer fertility testing (AMH, FSH) if concerned

**POSTPARTUM INTERVAL**:
- **Optimal interval**: 18-23 months between pregnancies (lowest risk of adverse outcomes)
- **Short interval** (<6 months): Increased risk of preterm birth, low birth weight, maternal anemia, depletion
- **Contraception**: Discuss if not planning immediate pregnancy

**PARTNER HEALTH**:
- **Sperm quality**: Improves with smoking cessation, reducing alcohol, healthy weight, avoiding hot tubs/saunas
- **STI screen**: If at risk, chlamydia/gonorrhea/HIV/syphilis
- **Medications**: Some affect fertility (testosterone, anabolic steroids, chemotherapy)
- **Age**: Advanced paternal age associated with increased autism, schizophrenia, chromosomal abnormalities (small absolute risk)

**TIMING INTERCOURSE**:
- **Fertile window**: 6 days ending on day of ovulation (ovulation -1 day to ovulation +1 day most fertile)
- **Ovulation prediction**: LH surge kits (most reliable), cervical mucus (clear, stretchy), basal body temperature (after ovulation, retrospective)
- **Frequency**: Every 2-3 days throughout cycle (covers fertile window, reduces stress)

**WHEN TO REFER**:
- **Infertility** (>12 months if <35, >6 months if ≥35)
- **Recurrent miscarriage** (>2 consecutive)
- **Previous pregnancy complications** (pre-eclampsia, IUGR, stillbirth, preterm birth)
- **Chronic diseases** requiring specialist input (diabetes, hypertension, epilepsy, cardiac disease, renal disease)
- **Genetic concerns** (family history, ethnicity, previous affected child)
- **Medication teratogenicity** requiring specialist advice

**SOURCES:** NICE, RCOG, USPSTF
""",
            confidence=0.95,
            metadata={
                "specialty": "Women's Health",
                "focus": "Preconception Counseling",
                "sources": ["NICE", "RCOG", "USPSTF"]
            }
        )

    def _handle_postpartum_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle postpartum care queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**POSTPARTUM CARE (THE "FOURTH TRIMESTER")**

**POSTPARTUM DEFINITION**: First 6-12 weeks after delivery (extended to 6-12 months by some)

**IMMEDIATE POSTPARTUM (First 24 hours)**:
- **Vital signs**: BP, pulse, temperature (pyrexia - infection), pulse tachycardia (hemorrhage, infection)
- **Blood loss**: Estimate, check uterine tone (atony?), examine perineum (tears, hematoma?), check lochia (rubra, serosa, alba)
- **Bladder**: Ensure voiding, urinary retention (common after epidural, instrumental delivery)
- **Pain**: Analgesia (paracetamol/acetaminophen, NSAIDs, consider opioids if severe), encourage regular analgesia rather than PRN
- **Mobility**: Early mobilization (VTE prophylaxis if risk factors), thromboembolism risk highest postpartum
- **Breastfeeding**: Initiate within first hour, skin-to-skin, latch assistance
- **Thromboprophylaxis**: LMWH for 10 days if risk factors (CS, emergency CS, preeclampsia, BMI >30, age >35, smoking, VTE history, thrombophilia)

**POSTPARTUM CHECK** (6-8 weeks):
- **Physical examination**: BP, weight, abdominal exam (uterine involution), breast exam, perineum/c-section scar check, pelvic exam if indicated
- **Mental health**: Postnatal depression screening (EPDS), anxiety, OCD, PTSD (especially after traumatic birth)
- **Contraception**: Discuss and provide if desired
- **Breastfeeding**: Support, latch assessment, mastitis, thrush, supply concerns
- **Pelvic floor**: PFMT teaching, incontinence, prolapse symptoms
- **Medical conditions**: Gestational diabetes (OGTT), hypertension, thyroid disease
- **Lifestyle**: Nutrition, exercise, sleep, smoking/alcohol

**POSTNATAL DEPRESSION (PND)**:
- **Prevalence**: 10-15% (more common in developing countries)
- **Onset**: Anytime in first year (usually first 3 months)
- **Symptoms**: Low mood, anhedonia, tearfulness, anxiety, irritability, guilt, worthlessness, sleep disturbance (beyond baby), appetite changes, bonding difficulties, intrusive thoughts (harming baby - seek help immediately)
- **Risk factors**: Previous PND, anxiety/depression in pregnancy, traumatic birth, poor social support, relationship difficulties, baby health problems, stressful life events, history of abuse
- **Screening**: EPDS (Edinburgh Postnatal Depression Scale) at 6 weeks, 3-6 months
- **Management**:
  - **Mild**: Self-help, support groups, counseling, CBT
  - **Moderate**: CBT, medication (SSRIs - sertraline, paroxetine, escitalopram considered safe), breastfeeding-compatible medications
  - **Severe**: Antidepressants, consider psychiatric referral, specialist mother-baby unit (if psychosis, severe suicidality)
- **Postpartum psychosis**: Medical emergency (1-2/1000), hallucinations, delusions, mood swings, confusion, suicidal/infanticidal ideation - urgent psychiatric assessment

**POSTPARTUM CONTRACEPTION**:
- **Return of fertility**: As early as 4 weeks (non-breastfeeding), 6 months (exclusive breastfeeding, but ovulation before first period possible)
- **Options**:
  - **LAM** (Lactational Amenorrhea Method): Effective if <6 months, fully/exclusively breastfeeding, amenorrheic (98% effective, but not reliable)
  - **POP** (Progestogen-only pill): Safe for breastfeeding, start 21 days postpartum if not breastfeeding, 6 weeks if breastfeeding
  - **COCP**: Avoid if breastfeeding <6 weeks (reduces milk supply, small risk of VTE), can start after 6 weeks if not breastfeeding
  - **IUD/IUS**: Can insert from 4 weeks postpartum (immediate if CS >48h or vaginal delivery >48h and no infection)
  - **Implant**: Insert from 4 weeks postpartum
  - **Sterilization**: Can be performed at CS or interval (3-6 months postpartum), ensure informed consent (no regrets)

**BREASTFEEDING SUPPORT**:
- **Benefits**: Baby (antibodies, nutrition, reduced SIDS, infection, allergy, obesity, diabetes), Mother (bonding, postpartum weight loss, reduced ovarian/breast cancer, reduced diabetes)
- **Latch**: Baby facing mother, nose to nipple, wait for wide mouth, aim nipple to roof of mouth, chin touches breast first
- **Frequency**: 8-12 times/24 hours (on demand), feed from both breasts each time, let baby finish first breast (foremilk to hindmilk)
- **Duration**: Exclusive breastfeeding for 6 months, continued alongside solids until 2 years (WHO)
- **Common problems**:
  - **Sore/cracked nipples**: Improve latch, express breast milk on nipples, lanolin, air dry, avoid soap
  - **Mastitis**: Flu-like symptoms, breast redness, heat, tenderness - frequent feeds, express if necessary, antibiotics (flucloxacillin) if systemic symptoms/no improvement after 24 hours, continue breastfeeding
  - **Thrush**: Shiny/flukey nipples, breast pain (burning/shooting), baby white patches in mouth - oral nystatin for baby, topical miconazole for nipples, continue breastfeeding
  - **Low supply**: Feed frequently, express after feeds, ensure effective latch, consider galactagogues (domperidone - specialist), ensure adequate hydration/nutrition/rest
  - **Oversupply**: Block feeding (one breast per feed), reduce stimulation, hand express for comfort
  - **Engorgement**: Frequent feeds, warm compress before feed, cold compress after, hand express if necessary
  - **Ductal/nipple bleb**: White spot on nipple, milk blister - warm compresses, massage, lecithin, sterile needle to release (specialist)

**INFANT FEEDING CHOICE**:
- **Formula**: Safe alternative, support choice not judgment, educate on preparation (sterilize bottles, correct powder-to-water ratio, temperature), growth monitoring
- **Mixed feeding**: Breastfeeding + formula - beware of milk supply reduction

**POSTPARTUM PELVIC FLOOR RECOVERY**:
- **PFMT**: Start 24 hours after vaginal birth, 48 hours after CS (if comfortable), 3 sets of 10 contractions, 3 times/day
- **Perineal care**: Ice packs (first 24 hours), warm baths after 24 hours, keep clean and dry, pelvic floor exercises, pain relief
- **Perineal tears**:
  - **First/second degree**: PFMT, pain relief, observe for infection/dehiscence
  - **Third/fourth degree**: Follow-up in perineal clinic, PFMT, laxatives (stool softeners), antibiotics, physiotherapy
- **Urinary/fecal incontinence**: Common, usually improves with PFMT, refer to physiotherapist if persists >6-8 weeks
- **Prolapse**: Sensation of heaviness/dragging, refer to gynecology, PFMT, pessary if symptomatic

**POSTPARTUM PHYSICAL RECOVERY**:
- **Lochia**: Vaginal discharge for 4-6 weeks (rubra red 1-3 days, serosa pink/brown 2-3 weeks, alba white/yellow up to 6 weeks), heavy bleeding (soaking pad in <1 hour - seek review), clots (small normal, large - seek review), foul odor (infection)
- **Afterpains**: Uterine cramping (more pronounced in subsequent pregnancies), analgesia (paracetamol/acetaminophen, NSAIDs)
- **Episiotomy/tear healing**: Keep clean, pain relief, PFMT, observe for infection/dehiscence
- **CS recovery**: Wound care, pain relief, mobilization, thromboprophylaxis, driving after 6 weeks (if comfortable, emergency stop), pelvic floor exercises
- **Hemorrhoids**: Common, stool softeners, fiber, fluids, analgesia, topical treatments (anusol, rectogesic), resolves usually
- **Hair loss**: Telogen effluvium 3-4 months postpartum (due to hormonal changes), resolves by 12 months

**POSTPARTUM MEDICAL CONDITIONS**:
- **Postpartum thyroiditis**: Transient hyperthyroidism (1-3 months) then hypothyroidism (3-6 months), usually resolves by 12 months, treat if symptomatic
- **Postpartum hypertension**: Monitor BP, can develop up to 6 weeks postpartum, treat if ≥150/100, antihypertensives (nifedipine, labetalol), seek specialist if refractory
- **Postpartum cardiomyopathy**: Heart failure (dyspnea, orthopnea, edema) in last month of pregnancy or 5 months postpartum, echocardiogram, medications (ACE inhibitors, beta-blockers), risk in future pregnancies
- **Sheehan's syndrome**: Postpartum pituitary necrosis due to hemorrhage, hypopituitarism (inability to breastfeed, amenorrhea, fatigue), hormone replacement

**POSTPARTUM SEXUAL HEALTH**:
- **Timing**: When comfortable (usually 6 weeks), if perineal tears/episiotomy - wait until healed
- **Dyspareunium**: Common, perineal pain, vaginal dryness (especially if breastfeeding), pelvic floor weakness, use vaginal estrogen if dryness, PFMT, lubricants
- **Contraception**: Discuss (see above), important if not planning immediate pregnancy (short interval pregnancy risks)

**POSTPARTUM EXERCISE**:
- **Start**: Gentle walking from day 1 (or after CS when comfortable)
- **Return to exercise**:
  - **0-6 weeks**: Walking, pelvic floor exercises, gentle stretching
  - **6-12 weeks**: Gradual return to exercise (low impact), avoid high impact until pelvic floor recovered (3-6 months), avoid abdominal crunches (separation of recti abdominis - diastasis recti)
  - **3-6 months**: Return to higher impact if pelvic floor strong, no urinary leakage, no prolapse symptoms

**POSTPARTUM NUTRITION**:
- **Increased requirements**: Breastfeeding requires +500 kcal/day, protein, fluids (3-4 L/day)
- **Iron**: If anemic, continue supplementation
- **Calcium**: 5 portions dairy/day or supplements
- **Vitamin D**: 10 mcg daily
- **Caffeine**: Limit (200 mg/day) - crosses into breast milk, may affect baby
- **Alcohol**: Avoid if possible, if consume - time feed for after alcohol (1 unit takes 1-2 hours to clear)

**SOURCES:** NICE, RCOG, WHO
""",
            confidence=0.95,
            metadata={
                "specialty": "Women's Health",
                "focus": "Postpartum Care",
                "sources": ["NICE", "RCOG", "WHO"]
            }
        )

    def _handle_fibroids_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle uterine fibroid queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**UTERINE FIBROIDS (LEIOMYOMAS)**

**PREVALENCE**: 70-80% of women by age 50, 20-50% symptomatic

**PATHOGENESIS**: Benign smooth muscle tumors of uterus, estrogen/progesterone dependent, monoclonal origin, genetic predisposition (racial variation - more common, larger, earlier onset in Black women)

**RISK FACTORS**:
- **Increased risk**: Black race, nulliparity, early menarche, family history, obesity, diet (red meat, alcohol), hypertension
- **Decreased risk**: Parity, oral contraceptives, smoking (controversial - dose-dependent)

**TYPES**:
- **Intramural** (most common): Within uterine wall
- **Subserosal**: Project outside uterus (pedunculated if on stalk)
- **Submucosal**: Project into uterine cavity (most symptomatic)
- **Cervical**: Rare

**SYMPTOMS** (50% asymptomatic):
- **Abnormal uterine bleeding**: Menorrhagia (prolonged, heavy), intermenstrual bleeding, clot passage
- **Bulk symptoms**: Urinary frequency, urgency, constipation, pelvic pressure/pain, bloating, palpable mass
- **Pain**: Dysmenorrhea, dyspareunia (if submucosal or pedunculated), acute pain (degeneration in pregnancy, torsion of pedunculated fibroid)
- **Reproductive issues**: Infertility, recurrent miscarriage, pregnancy complications (malpresentation, obstructed labor, postpartum hemorrhage)

**COMPLICATIONS**:
- **Degeneration**: Red degeneration (hemorrhagic necrosis - acute pain, fever, common in pregnancy), carneous degeneration
- **Torsion**: Pedunculated fibroid torsion - acute pain, surgical emergency
- **Infection**: Necrotic fibroid, postpartum
- **Malignant transformation**: Leiomyosarcoma (rare, <0.5%, rapid growth, postmenopausal women)

**IMAGING**:
- **Transvaginal/transabdominal ultrasound**: First-line, size, location, number, character (hypoechoic, heterogenous, calcifications)
- **MRI**: If complex, planning surgery, differentiating fibroid from adenomyosis

**MANAGEMENT** (asymptomatic - observation, symptomatic - treat):

**MEDICAL MANAGEMENT**:
- **Tranexamic acid**: 1 g TDS during menses (reduces blood loss 50%), take during menses only
- **NSAIDs**: Mefenamic acid 500 mg TDS, naproxen 250 mg TDS (reduces blood loss 20-50%)
- **COCP**: Regulates cycles, reduces bleeding, may slow growth
- **Levonorgestrel IUS** (Mirena): Reduces bleeding 95%, amenorrhea common, treats adenomyosis, less effective if cavity distorted by large/submucosal fibroids
- **GnRH agonists**: Leuprorelin 3.75 mg IM monthly, creates menopausal state, reduces fibroid size 30-50%, used preoperatively (reduce size, correct anemia), limited to 3-6 months due to bone loss, add-back HRT if longer
- **Ulipristal acetate** (SPRM - selective progesterone receptor modulator): 5 mg daily for 3 months (intermittent courses), reduces bleeding, shrinks fibroids, liver injury rare (monitor LFTs), UK license suspended 2020 (use specialist only)
- **Relugolix**: GnRH antagonist, available in some countries

**SURGICAL MANAGEMENT**:

**Myomectomy** (fibroid removal, uterus-preserving):
- **Hysteroscopic**: Submucosal fibroids (<4-5 cm), day case, rapid recovery, resection with loop or morcellator
- **Laparoscopic**: Intramural/subserosal fibroids (<10-12 cm), 3-4 ports, morcellation (fibroid cut into pieces for removal), concern about occult malignancy spread (if contained morcellation - bag, not currently recommended without specialist assessment)
- **Abdominal** (open): Large fibroids (>12 cm), multiple fibroids, previous surgery (adhesions), larger incision, longer recovery
- **Robotic**: Similar to laparoscopic, expensive, limited availability
- **Risks**: Bleeding, infection, injury to surrounding organs, adhesion formation, recurrence (10-30% depending on technique), uterine rupture in future pregnancy (rare, especially if hysteroscopic)

**Hysterectomy** (definitive):
- **Indications**: Completed fertility, failed medical/surgical management, rapid growth (postmenopausal - concern for malignancy), severe symptoms
- **Approach**: Vaginal (if uterus <12 weeks size, no adhesions), Laparoscopic (if <16 weeks), Abdominal (if >16 weeks or complex)
- **Oophorectomy**: Consider concurrent removal of ovaries (if postmenopausal or age >45)
- **Risks**: Surgical complications (bleeding, infection, injury), loss of fertility, premature menopause (if ovaries removed)

**UTERINE ARTERY EMBOLIZATION (UAE)**:
- **Procedure**: Angiographic catheterization of uterine arteries, embolization with particles (polyvinyl alcohol, gelatin sponge), fibroid infarction and shrinkage
- **Indications**: Symptomatic fibroids in women who wish to avoid surgery, medical comorbidities, refuse surgery
- **Outcomes**: 80-90% improvement in bleeding, 70-80% improvement in bulk symptoms, fibroid shrinkage 40-60%
- **Pregnancy**: Possible after UAE but increased risk of miscarriage, preterm birth, placental abnormalities - generally avoided if fertility desired
- **Complications**: Post-embolization syndrome (pain, fever, nausea - common, self-limiting), infection, ovarian failure (5% especially age >45), need for hysterectomy (5-10%)
- **Recurrence**: 10-20% (new fibroids or regrowth)

**MRI-GUIDED FOCUSED ULTRASOUND (MRgFUS)**:
- **Procedure**: MRI guidance, focused ultrasound waves cause thermal ablation of fibroid, outpatient, no incision
- **Indications**: Symptomatic fibroids <10 cm, women who wish to avoid surgery
- **Outcomes**: 70-80% symptom improvement, 30-40% volume reduction
- **Risks**: Skin burns, pain, need for repeat treatment or surgery (30-40%)
- **Pregnancy**: Possible after, limited data

**FIBROIDS IN PREGNANCY**:
- **Prevalence**: 2-10% of pregnancies
- **Complications**: Miscarriage (especially submucosal), malpresentation (breech), placental abruption, preterm labor, postpartum hemorrhage, obstructed labor (if lower segment fibroid), pain (degeneration - especially 2nd trimester)
- **Management**: Usually conservative (analgesia, hydration, rest), myomectomy during pregnancy only if symptomatic and refractory (rare, high morbidity), cesarean section if fibroid obstructs labor

**FIBROIDS AND INFERTILITY**:
- **Distorted cavity** (submucosal): Interfere with implantation, sperm transport - myomectomy improves fertility
- **Large intramural/subserosal**: May impair implantation, blood flow - myomectomy may improve fertility (controversial)
- **IVF outcomes**: Submucosal fibroids reduce success, intramural may affect outcomes, consider myomectomy if cavity distortion or >4 cm

**WHEN TO REFER**:
- **Symptomatic fibroids** (bleeding, pain, bulk symptoms)
- **Rapid growth** (postmenopausal - rule out malignancy, premenopausal if >6 cm or >1 cm/6 months)
- **Infertility** (especially if submucosal)
- **Anemia** (iron deficiency)
- **Pregnancy planning** (consider myomectomy if submucosal or large intramural)

**SOURCES:** NICE CG44, RCOG Green-top Guidelines
""",
            confidence=0.93,
            metadata={
                "specialty": "Women's Health",
                "focus": "Uterine Fibroids",
                "sources": ["NICE CG44", "RCOG Green-top Guidelines"]
            }
        )

    def _handle_general_womens_health_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general women's health queries."""

        return DomainQueryResult(
            domain_name="womens_health",
            answer="""
**WOMEN'S HEALTH - COMPREHENSIVE CARE**

Women's health encompasses the unique health needs of women throughout their lives, from puberty through menopause and beyond.

**LIFECOURSE APPROACH**:

**Adolescence (11-18 years)**:
- Menarche education, menstrual cycle, menstrual disorders
- HPV vaccination (ages 12-13)
- Healthy lifestyle, body image, eating disorders
- Contraception education (if sexually active)
- STI prevention

**Reproductive Years (18-45 years)**:
- Contraception and family planning
- Preconception counseling
- Pregnancy care and postpartum support
- Cervical screening (25-49: every 3 years)
- Menstrual health (PCOS, endometriosis, PMS)
- Fertility and infertility
- Sexual health and function
- Breast awareness

**Perimenopause (45-55 years)**:
- Menstrual cycle changes, irregular bleeding
- Menopause symptoms (hot flashes, night sweats)
- HRT decision-making
- Cervical screening (50-64: every 5 years)
- Breast screening (mammography 50-70 every 3 years)
- Cardiovascular risk assessment

**Postmenopause (55+ years)**:
- Continuation of HRT (if appropriate)
- Bone health (osteoporosis screening/treatment)
- Cardiovascular risk reduction
- Cancer screening (breast, colorectal)
- Pelvic floor health (incontinence, prolapse)
- Healthy aging

**KEY PREVENTIVE HEALTH MEASURES**:

**Cervical Cancer Prevention**:
- HPV vaccination (ages 12-13)
- Cervical screening (25-64 years, every 3-5 years)
- Safe sexual practices

**Breast Cancer Prevention**:
- Breast awareness (know what's normal for you)
- Breast screening (mammography 50-70 years)
- Risk factor modification (weight, exercise, alcohol)
- Family history assessment

**Ovarian Cancer Awareness**:
- No effective screening test (CA125 + ultrasound NOT recommended for population screening)
- Know symptoms: Bloating, pelvic/abdominal pain, difficulty eating/feeling full quickly, urinary urgency/frequency (persistent, frequent, new)
- Family history assessment (BRCA)

**Cardiovascular Health**:
- Leading cause of death in women (often under-recognized)
- Risk factors: Hypertension, cholesterol, smoking, diabetes, obesity, family history
- Atypical symptoms in women (nausea, fatigue, jaw/back pain)
- Regular health checks

**Bone Health**:
- Osteoporosis prevention: Weight-bearing exercise, calcium (1000-1200 mg/day), vitamin D (800-1000 IU daily), avoid smoking/excess alcohol
- Screening: DEXA scan if risk factors (family history, early menopause, steroid use, low BMI, smoking, alcohol, previous fracture)
- Treatment: Bisphosphonates, denosumab, HRT (if <60)

**Reproductive Health**:
- Regular cervical screening
- Contraception access and counseling
- Preconception counseling
- Pregnancy planning and support
- Postpartum care
- Menopause management

**Sexual Health**:
- STI prevention (condoms, vaccination, testing)
- STI testing (new partner, multiple partners)
- Sexual function and dysfunction
- Contraception and family planning

**Mental Health**:
- Depression/anxiety screening (especially postpartum)
- Postnatal depression awareness
- Eating disorders
- Trauma/abuse support

**Sources:** NICE Guidelines, RCOG, WHO
""",
            confidence=0.90,
            metadata={
                "specialty": "Women's Health",
                "focus": "General Women's Health",
                "sources": ["NICE", "RCOG", "WHO"]
            }
        )


def create_womens_health_domain():
    """
    Factory function to create women's health domain instance.

    Returns:
        WomensHealthDomain: Configured women's health specialty domain
    """
    return WomensHealthDomain()
