"""
Endocrinology & Diabetes Domain for GPDISC
Comprehensive endocrine system consultation covering diabetes, thyroid disorders,
adrenal conditions, and hormonal imbalances.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class EndocrinologyDomain(BaseDomainModule):
    """
    Endocrinology & Diabetes Specialist Domain

    Covers:
    - Type 1 and Type 2 diabetes diagnosis and management
    - Insulin regimens and adjustment
    - Hypoglycemia management
    - Thyroid disorders (hypothyroidism, hyperthyroidism, nodules)
    - Adrenal insufficiency
    - Pituitary disorders
    - Calcium metabolism disorders
    - Gender hormones and menopause
    - Lipid metabolism
    - Metabolic syndrome
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="endocrinology",
            version="1.0.0",
            dependencies=[],
            description="Endocrinology & Diabetes: diabetes management, thyroid disorders, adrenal conditions, hormonal imbalances",
            keywords=[
                # Diabetes terms
                "diabetes", "diabetic", "type 1 diabetes", "type 2 diabetes",
                "insulin", "hba1c", "hba1c", "glycosylated hemoglobin",
                "hypoglycemia", "hyperglycemia", "blood sugar", "glucose",
                "metformin", "gliclazide", "sitagliptin", "empagliflozin",

                # Thyroid terms
                "thyroid", "hypothyroid", "hyperthyroid", "thyroxine", "levothyroxine",
                "tsh", "t4", "t3", "thyroid nodule", "goitre", "goiter",
                "graves", "hashimoto", "thyroiditis",

                # Adrenal terms
                "adrenal", "addison", "adrenal insufficiency", "cortisol",
                "prednisolone", "steroid", "hydrocortisone", "fludrocortisone",

                # Pituitary terms
                "pituitary", "prolactin", "growth hormone", "acromegaly",
                "adh", "vasopressin", "diabetes insipidus",

                # Calcium/parathyroid
                "calcium", "parathyroid", "pth", "vitamin d", "osteoporosis",

                # Reproductive endocrinology
                "menopause", "hrt", "hormone replacement", "testosterone",
                "estrogen", "progesterone", "pcos", "polycystic ovary",

                # Metabolic terms
                "metabolic syndrome", "lipid", "cholesterol", "triglyceride",
                "thyroid function", "endocrine", "hormone", "gland"
            ],
            capabilities=[
                "diabetes_diagnosis",
                "diabetes_management",
                "insulin_adjustment",
                "hypoglycemia_management",
                "thyroid_disorder_diagnosis",
                "thyroid_nodule_evaluation",
                "adrenal_insufficiency_management",
                "pituitary_disorder_assessment",
                "calcium_metabolism_disorders",
                "menopause_management",
                "hormone_interpretation",
                "metabolic_syndrome_management"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Route endocrinology query to appropriate handler"""
        query_lower = query.lower()

        # Diabetes queries
        if any(term in query_lower for term in ["diabetes", "insulin", "hba1c", "hypoglyc", "hyperglyc", "blood sugar", "glucose"]):
            return self._handle_diabetes_query(query, context)

        # Thyroid queries
        elif any(term in query_lower for term in ["thyroid", "tsh", "t4", "t3", "goitre", "goiter", "nodule"]):
            return self._handle_thyroid_query(query, context)

        # Adrenal queries
        elif any(term in query_lower for term in ["adrenal", "addison", "cortisol"]):
            return self._handle_adrenal_query(query, context)

        # Pituitary queries
        elif any(term in query_lower for term in ["pituitary", "prolactin", "acromegaly", "diabetes insipidus"]):
            return self._handle_pituitary_query(query, context)

        # Calcium/parathyroid queries
        elif any(term in query_lower for term in ["calcium", "parathyroid", "pth", "vitamin d"]):
            return self._handle_calcium_query(query, context)

        # Menopause/hormone queries
        elif any(term in query_lower for term in ["menopause", "hrt", "hormone replacement"]):
            return self._handle_menopause_query(query, context)

        # Metabolic syndrome
        elif any(term in query_lower for term in ["metabolic syndrome", "lipid"]):
            return self._handle_metabolic_query(query, context)

        # General endocrinology
        else:
            return self._handle_general_endocrinology(query, context)

    def _handle_diabetes_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle diabetes-related queries"""
        query_lower = query.lower()

        # HbA1c interpretation
        if "hba1c" in query_lower or "hba1c" in query_lower or "a1c" in query_lower:
            return self._interpret_hba1c(query, context)

        # Hypoglycemia management
        elif "hypoglyc" in query_lower or "low blood sugar" in query_lower or "hypo" in query_lower:
            return self._manage_hypoglycemia(query, context)

        # Insulin adjustment
        elif "insulin" in query_lower and ("adjust" in query_lower or "dose" in query_lower or "change" in query_lower):
            return self._adjust_insulin(query, context)

        # Diabetes diagnosis
        elif "diagnos" in query_lower or "criteria" in query_lower:
            return self._diabetes_diagnosis(query, context)

        # General diabetes management
        else:
            return self._general_diabetes_management(query, context)

    def _interpret_hba1c(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret HbA1c results"""
        # Try to extract HbA1c value from query
        hba1c_match = re.search(r'(\d+\.?\d*)\s*%?', query.replace('mmol/mol', ''))

        answer = """**HbA1c Interpretation and Diabetes Diagnosis**

HbA1c reflects average blood glucose over the past 2-3 months.

**Diagnostic Criteria (WHO/NICE):**
- **< 39 mmol/mol (< 5.7%)**: Normal
- **39-47 mmol/mol (5.7-6.4%)**: Pre-diabetes (high risk)
- **≥ 48 mmol/mol (≥ 6.5%)**: Diabetes (if confirmed with repeat test)

**Target Ranges:**
- **Tight control**: 42-47 mmol/mol (6.0-6.4%) for younger patients
- **Standard**: 48-53 mmol/mol (6.5-7.0%) for most adults
- **Relaxed**: 53-64 mmol/mol (7.0-8.0%) for elderly/frail
- **Individualized**: Higher targets for very elderly, limited life expectancy

**Conversion Formula:**
HbA1c (mmol/mol) = (HbA1c % - 2.15) × 10.929

**Factors Affecting Results:**
- **False elevation**: Anemia, iron deficiency, renal failure, alcoholism
- **False lowering**: Hemolysis, blood loss, recent transfusion

"""

        if hba1c_match:
            value = float(hba1c_match.group(1))
            if value > 10:  # Likely mmol/mol
                mmol = value
                percent = (value / 10.929) + 2.15
            else:  # Likely percentage
                percent = value
                mmol = (value - 2.15) * 10.929

            answer += f"\n**Your Result:** {mmol:.0f} mmol/mol ({percent:.1f}%)\n\n"

            if mmol < 39:
                answer += "**Assessment:** Normal - no diabetes\n\n"
                answer += "**Recommendation:** Healthy lifestyle, repeat screening every 3 years if at risk"
            elif mmol < 48:
                answer += "**Assessment:** Pre-diabetes - high risk of developing diabetes\n\n"
                answer += "**Recommendation:**\n"
                answer += "- Intensive lifestyle modification (diet, exercise, weight loss)\n"
                answer += "- Annual HbA1c monitoring\n"
                answer += "- Consider metformin if BMI > 35 or other risk factors\n"
                answer += "- Cardiovascular risk assessment"
            else:
                answer += "**Assessment:** Diabetes range\n\n"
                answer += "**Recommendation:**\n"
                answer += "- Confirm with repeat test (unless symptoms present)\n"
                answer += "- Refer to diabetes education program\n"
                answer += "- Initiate treatment based on type and clinical picture\n"
                answer += "- Comprehensive cardiovascular risk assessment\n"
                answer += "- Annual complications screening (retinopathy, nephropathy, neuropathy)"

        answer += "\n\n**Sources:** NICE NG28, ADA Standards of Care 2024"

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "endocrinology_diabetes",
                "focus": "hba1c_interpretation",
                "sources": ["NICE NG28", "ADA Standards 2024"]
            }
        )

    def _manage_hypoglycemia(self, query: str, context: dict) -> DomainQueryResult:
        """Provide hypoglycemia management guidance"""
        answer = """**Hypoglycemia (Low Blood Sugar) Management**

**Definition:** Blood glucose < 3.9 mmol/L (< 70 mg/dL)

**Classification:**
- **Mild:** 3.1-3.9 mmol/L - self-treatable
- **Moderate:** < 3.1 mmol/L but able to self-treat
- **Severe:** Requires assistance (may be unconscious)

**Immediate Treatment (15-15 Rule):**

**1. CONSCIOUS patient:**
- Take 15-20g fast-acting carbohydrate immediately:
  - 150-200mL fruit juice or regular (non-diet) soft drink
  - 3-4 glucose tablets
  - 4-5 jelly babies
  - 1 tablespoon honey or sugar
- **Wait 15 minutes**, then recheck
- If still < 4.0 mmol/L, repeat
- Once recovered, eat longer-acting carbohydrate (sandwich, cereal)

**2. UNCONSCIOUS patient:**
- **DO NOT** give anything by mouth (risk of aspiration)
- **IM glucagon 1mg** (if available)
- **IV 10% or 20% dextrose** (in hospital)
- Recovery position, monitor airway

**Prevention of Recurrence:**

**For Insulin Users:**
- Check blood glucose before driving
- Never skip meals after insulin
- Adjust insulin for exercise/activity
- Consider basal insulin reduction if recurrent nocturnal hypoglycemia

**For Sulfonylurea Users:**
- Check renal function (adjust dose if eGFR ↓)
- Consider switching to shorter-acting agent
- Be cautious in elderly (gliclazide preferred)

**Hypoglycemia Unawareness:**
- More common in long-standing diabetes
- Consider structured education (DAFNE, DESMOND)
- Relax glycemic targets temporarily
- Review medications that mask symptoms (beta-blockers)

**Red Flags - Seek Emergency Care:**
- Unconscious or having seizures
- Not improving after treatment
- Recurring hypoglycemia (requires medication review)
- Hypoglycemia while driving (must notify DVLA)

**Sources:** NICE NG28, Diabetes UK 2024"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "endocrinology_diabetes",
                "focus": "hypoglycemia_management",
                "sources": ["NICE NG28", "Diabetes UK"]
            }
        )

    def _adjust_insulin(self, query: str, context: dict) -> DomainQueryResult:
        """Provide insulin adjustment guidance"""
        answer = """**Insulin Dose Adjustment Guidance**

**GENERAL PRINCIPLES:**

**Basal-Bolus Regimen Adjustment:**

**Basal Insulin (Long-acting):**
- Target: Fasting glucose 4-7 mmol/L
- If fasting consistently > 7: Increase basal by 10-20%
- If fasting consistently < 4: Decrease basal by 10-20%
- Adjust every 3-4 days (longer for degludec/ Toujeo)
- Best taken at bedtime (but timing can be individualized)

**Bolus Insulin (Rapid-acting):**

**Carbohydrate Counting (Ratio):**
- Typical insulin:carb ratios:
  - Morning: 1 unit: 10g carbs
  - Lunch: 1 unit: 10g carbs
  - Evening: 1 unit: 15g carbs (often more insulin-sensitive)
- Adjust based on post-meal glucose patterns (2 hours after)

**Correction Factor (Insulin Sensitivity Factor):**
- Formula: 100 ÷ Total Daily Dose (TDD)
- Example: TDD = 50 units → ISF = 100÷50 = 2 (1 unit drops glucose by 2 mmol/L)
- Correction dose = (Current glucose - Target) ÷ ISF
- Usual target: 6-7 mmol/L

**Common Patterns & Adjustments:**

| Pattern | Adjustment |
|---------|-----------|
| High 2h post-breakfast | ↑ Breakfast bolus ratio or check pre-breakfast basal |
| High 2h post-lunch | ↑ Lunch bolus ratio |
| High 2h post-dinner | ↑ Dinner bolus ratio or check afternoon basal |
| High overnight | ↑ Basal dose or check for dawn phenomenon |
| Low overnight | ↓ Basal dose (watch for nocturnal hypoglycemia) |
| High at 3 AM | Consider splitting basal (evening basal too early) |

**Special Situations:**

**Exercise:**
- Reduce bolus for meal before exercise by 25-50%
- Consider reducing basal for prolonged exercise
- Monitor more frequently (hypo risk up to 24h post-exercise)

**Illness (Sick Day Rules):**
- **NEVER stop insulin** - may need MORE
- Check ketones if glucose > 13 mmol/L
- Increase insulin by 10-20% if significantly hyperglycemic
- Maintain hydration
- Seek urgent help if vomiting + ketones

**Steroid Therapy:**
- Significantly increases insulin requirements
- May need to increase doses by 50-100%
- Monitor closely, adjust as steroids tapered

**Safeguards:**
- Never make more than 10-20% adjustment at once
- Keep detailed records of doses, carbs, activity
- Review patterns over 3-5 days before adjusting
- Contact diabetes team if unsure or if glucose persistently out of range

**CAUTION:** These are general guidelines. Individualized advice from your diabetes team is essential, especially when starting insulin or making significant changes.

**Sources:** NICE NG28, DAFNE guidelines, ABCD (Association of British Clinical Diabetologists)"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "endocrinology_diabetes",
                "focus": "insulin_adjustment",
                "sources": ["NICE NG28", "DAFNE", "ABCD"]
            }
        )

    def _diabetes_diagnosis(self, query: str, context: dict) -> DomainQueryResult:
        """Provide diabetes diagnosis criteria"""
        answer = """**Diabetes Diagnosis Criteria**

**WHO/NICE Diagnostic Criteria:**

**Diabetes Mellitus:**
Diagnosed if ONE of the following is confirmed on a separate day (unless symptoms are unequivocal):

1. **HbA1c ≥ 48 mmol/mol (≥ 6.5%)**
   - Reflects 2-3 month average glucose
   - Does NOT require fasting
   - May be unreliable in anemia, pregnancy, recent transfusion

2. **Fasting Plasma Glucose ≥ 7.0 mmol/L**
   - No caloric intake for at least 8 hours
   - Venous plasma sample (not capillary)

3. **Random Plasma Glucose ≥ 11.1 mmol/L**
   - Taken at any time of day
   - + classic symptoms (polyuria, polydipsia, weight loss)

4. **2-hour OGTT ≥ 11.1 mmol/L**
   - 75g glucose load
   - Rarely needed in routine practice

**Type 1 vs Type 2 Diabetes:**

**Type 1 Diabetes:**
- Rapid onset (weeks-months)
- Younger age (but can occur at any age)
- Significant weight loss
- Ketosis prone
- **Autoantibodies positive:** GAD, IA-2, ZnT8
- Low/undetectable C-peptide
- **Immediate insulin required**

**Type 2 Diabetes:**
- Gradual onset (years)
- Usually > 40 years (but increasing in younger)
- Often overweight/obese
- Insulin resistant with relative deficiency
- May have no symptoms initially
- Lifestyle + oral medications initially

**Pre-diabetes (High Risk):**
- HbA1c 39-47 mmol/mol (5.7-6.4%)
- Fasting glucose 5.5-6.9 mmol/L (impaired fasting glucose)
- 2h OGTT 7.8-11.0 mmol/L (impaired glucose tolerance)
- **5-10% per year progress to diabetes**
- Lifestyle intervention can prevent/delay progression

**Gestational Diabetes:**
- Diagnosed by 75g OGTT at 24-28 weeks
- Fasting ≥ 5.6 mmol/L OR 2h ≥ 7.8 mmol/L
- Higher risk of future Type 2 diabetes

**Immediate Referral Criteria:**
- **Suspected Type 1 diabetes** (urgent same-day referral)
- **Diabetic ketoacidosis** (emergency)
- **Pregnancy with diabetes** (urgent joint obstetric/diabetes care)
- **Significant complications** (refer to appropriate specialist)

**Sources:** WHO 2023, NICE NG28, ADA Standards 2024"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.95,
            metadata={
                "specialty": "endocrinology_diabetes",
                "focus": "diagnosis_criteria",
                "sources": ["WHO 2023", "NICE NG28", "ADA 2024"]
            }
        )

    def _general_diabetes_management(self, query: str, context: dict) -> DomainQueryResult:
        """General diabetes management guidance"""
        answer = """**Diabetes Management Overview**

**Type 2 Diabetes - Stepwise Management:**

**FIRST LINE:**
1. **Lifestyle Modification**
   - Weight loss (5-10% if overweight)
   - Mediterranean-style diet
   - Regular exercise (150 min/week moderate)
   - Smoking cessation
   - Alcohol moderation

2. **Metformin** (if not contraindicated)
   - Starting: 500mg with food, increase to 1g BD over weeks
   - Standard dose: 1g BD (2g/day maximum)
   - Adjust for renal function (review if eGFR < 45)
   - Monitor B12 annually (long-term use)

**SECOND LINE (add if HbA1c not at target):**
- **SGLT2 inhibitor** (empagliflozin, dapagliflozin)
  - Cardiovascular and renal benefits
  - Weight loss, blood pressure reduction
  - Monitor for genital infections, DKA risk
- **DPP-4 inhibitor** (sitagliptin, linagliptin)
  - Weight neutral, well tolerated
  - Lower cardiovascular benefit than SGLT2i
- **SU** (gliclazide, glimepiride)
  - Effective, low cost
  - Hypoglycemia risk, weight gain
  - Gliclazide preferred in renal impairment

**THIRD LINE (dual therapy inadequate):**
- Consider triple therapy
- insulin (discuss if HbA1c > 75 mmol/mol or symptomatic)

**Insulin Indications:**
- Persistent hyperglycemia despite maximal oral agents
- Significant weight loss
- Symptoms of hyperglycemia
- Pregnancy planning
- Contra-indications to oral agents

**Annual Screening (9 Core Processes):**
1. HbA1c
2. Blood pressure
3. Cholesterol
4. Retinopathy screening
5. Foot examination
6. Urine albumin:creatinine ratio
7. eGFR
8. Weight/BMI
9. Smoking status

**Blood Pressure Targets:**
- **Standard:** 140/80 mmHg
- **With kidney disease/albuminuria:** 130/80 mmHg
- **Elderly (>80):** 150/90 mmHg

**Lipid Targets:**
- **Total cholesterol:** < 4.0 mmol/L
- **LDL cholesterol:** < 2.0 mmol/L (or < 1.4 if CVD)
- **Statin:** Offer atorvastatin 20mg to all > 40 years

**Sources:** NICE NG28, ADA Standards 2024, SIGN 154"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "endocrinology_diabetes",
                "focus": "general_management",
                "sources": ["NICE NG28", "ADA 2024", "SIGN 154"]
            }
        )

    def _handle_thyroid_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle thyroid-related queries"""
        query_lower = query.lower()

        # Thyroid function test interpretation
        if any(term in query_lower for term in ["tsh", "t4", "t3", "thyroid function", "thyroid test", "result"]):
            return self._interpret_thyroid_function(query, context)

        # Thyroid nodule
        elif "nodule" in query_lower or "lump" in query_lower:
            return self._evaluate_thyroid_nodule(query, context)

        # Hypothyroidism
        elif "hypothyroid" in query_lower or "underactive" in query_lower or "myxoedema" in query_lower:
            return self._manage_hypothyroidism(query, context)

        # Hyperthyroidism
        elif "hyperthyroid" in query_lower or "overactive" in query_lower or "thyrotoxic" in query_lower:
            return self._manage_hyperthyroidism(query, context)

        # General thyroid
        else:
            return self._general_thyroid_guidance(query, context)

    def _interpret_thyroid_function(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret thyroid function tests"""
        answer = """**Thyroid Function Test (TFT) Interpretation**

**Standard TFT Panel:**
- **TSH** (Thyroid Stimulating Hormone) - first-line screening test
- **Free T4** (Thyroxine) - measures active hormone
- **Free T3** (Triiodothyronine) - measured if T4/TSH discordant

**Common Patterns:**

| TSH | Free T4 | Interpretation |
|-----|---------|---------------|
| **Normal** | Normal | **Euthyroid** (normal thyroid function) |
| **High** | Low | **Primary hypothyroidism** (underactive thyroid) |
| **Low** | High | **Primary hyperthyroidism** (overactive thyroid) |
| **Low** | Normal | Subclinical hyperthyroidism |
| **High** | Normal | Subclinical hypothyroidism |
| **Low/Normal** | Low | **Secondary hypothyroidism** (pituitary problem) |

**Normal Ranges (varies by lab):**
- TSH: 0.4 - 4.0 mU/L (milliunits per litre)
- Free T4: 9 - 25 pmol/L
- Free T3: 3.5 - 6.5 pmol/L

**Subclinical Hypothyroidism:**
- **Mild:** TSH 4.0 - 10.0 mU/L, normal T4
- **Severe:** TSH > 10.0 mU/L, normal T4
- **Treatment:**
  - TSH > 10: Treat with levothyroxine
  - TSH 4-10 + symptoms: Consider treatment
  - TSH 4-10 + asymptomatic: Monitor every 6 months

**Subclinical Hyperthyroidism:**
- TSH < 0.1 mU/L, normal T4/T3
- **Causes:** Excessive levothyroxine, early Graves' disease, autonomous nodule
- **Risks:** Atrial fibrillation, osteoporosis
- **Action:** Repeat in 3 months, consider referral if persistent

**Pregnancy-Specific Ranges:**
- TSH higher in first trimester (hCG effect)
- Target TSH: < 2.5 mU/L in first trimester
- < 3.0 mU/L in second/third trimesters

**When TFTs Are Discordant:**

**Normal TSH, abnormal T4/T3:**
- Consider assay error
- Thyroid hormone resistance (rare)
- TSH-secreting pituitary adenoma (rare)

**Abnormal TSH, normal T4/T3:**
- **TSH high, T4 normal:** Early hypothyroidism, recovery from illness
- **TSH low, T4 normal:** Early hyperthyroidism, medication effects

**Common Medication Effects:**
- **Amiodarone:** Can cause hypo- or hyperthyroidism
- **Lithium:** Can cause hypothyroidism
- **Levothyroxine:** Suppresses TSH
- **Glucocorticoids:** Can suppress TSH

**Secondary Hypothyroidism (Pituitary):**
- Low/normal TSH + Low T4
- **RED FLAG:** Requires investigation of pituitary function
- Check other pituitary hormones (prolactin, cortisol, IGF-1)

**Sources:** NICE NG145, British Thyroid Association 2023, ATA Guidelines"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "endocrinology_thyroid",
                "focus": "tft_interpretation",
                "sources": ["NICE NG145", "BTA 2023", "ATA Guidelines"]
            }
        )

    def _evaluate_thyroid_nodule(self, query: str, context: dict) -> DomainQueryResult:
        """Thyroid nodule evaluation guidance"""
        answer = """**Thyroid Nodule Evaluation**

**Prevalence:** 5% of adults have palpable nodules; up to 50% have nodules on ultrasound

**Initial Assessment:**

**RED FLAGS (urgent referral - 2-week wait):**
- Firm, irregular, fixed nodule
- Rapidly enlarging
- Associated with lymphadenopathy
- Voice hoarseness (recurrent laryngeal nerve palsy)
- Age < 20 or > 65
- History of neck irradiation
- Family history of thyroid cancer
- **Stridor or dysphagia** (immediate referral)

**Routine Referral Indications:**
- Solitary nodule > 1 cm
- Increasing size
- Suspicious ultrasound features
- Nodule associated with symptoms

**Investigation Pathway:**

**1. TSH Measurement:**
- **Low TSH:** Possible "hot" (toxic) nodule → radionuclide scan
- **Normal/High TSH:** "Cold" nodule → ultrasound

**2. Thyroid Ultrasound (USS):**
- Assesses size, composition, vascularity
- Looks for suspicious features:
  - Hypoechogenicity
  - Microcalcifications
  - Irregular margins
  - Taller-than-wide shape
  - Cervical lymphadenopathy

**3. Fine Needle Aspiration (FNA):**
- Indicated if:
  - Nodule > 1 cm with suspicious USS features
  - Nodule > 1.5 cm even if benign-appearing
- Thy1: Non-diagnostic (repeat FNA)
- Thy2: Benign (routine surveillance)
- Thy3a: Indeterminate (repeat FNA or molecular testing)
- Thy3f: Follicular lesion (surgery for definitive diagnosis)
- Thy4: Suspicious (surgery)
- Thy5: Malignant (surgery)

**Management Categories:**

**Benign Nodules:**
- **Surveillance:** Repeat ultrasound in 6-12 months
- **Asymptomatic, stable:** No further intervention
- **Large/compressive symptoms:** Surgery or ethanol ablation

**Indeterminate Nodules (Thy3):**
- **Options:**
  - Repeat FNA in 3-6 months
  - Molecular testing (Afirma GEC, Thyroseq)
  - Diagnostic lobectomy
- Malignancy risk: 5-30%

**Malignant/Suspicious Nodules (Thy4/Thy5):**
- **Referral to thyroid surgeon**
- Total thyroidectomy ± neck dissection
- Risk-adapted approach for low-risk cancers

**Toxic (Hot) Nodules:**
- Autonomous hormone production
- **TSH suppressed, elevated T4/T3**
- **Treatment:**
  - Antithyroid drugs (temporary)
  - Radioiodine ablation (definitive)
  - Surgery (compressive symptoms, suspicious features)

**Follow-up:**
- Benign nodules: USS every 1-2 years
- Thy3: USS every 6-12 months
- Post-surgery: lifelong surveillance

**Sources:** NICE NG145, British Thyroid Association, ATA 2015 Guidelines"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "endocrinology_thyroid",
                "focus": "nodule_evaluation",
                "sources": ["NICE NG145", "BTA", "ATA 2015"]
            }
        )

    def _manage_hypothyroidism(self, query: str, context: dict) -> DomainQueryResult:
        """Hypothyroidism management guidance"""
        answer = """**Hypothyroidism (Underactive Thyroid) Management**

**Etiology:**
- **Hashimoto's thyroiditis** (most common - autoimmune)
- Post-radioiodine treatment
- Post-thyroidectomy
- **Iodine deficiency** (rare in UK with fortified salt)
- Medications (amiodarone, lithium)

**Symptoms:**
- Fatigue, weight gain, cold intolerance
- Dry skin, hair loss
- Constipation, depression
- Menorrhagia, infertility
- **Myxoedema coma** (rare emergency)

**Diagnosis:**
- **TSH > 10 mU/L** + Low Free T4 = Overt hypothyroidism
- **TSH 4-10 mU/L** + Normal Free T4 = Subclinical
- **Positive TPO antibodies** = Hashimoto's

**Treatment: Levothyroxine Replacement**

**Starting Dose:**
- **Adults < 65:** 50-100 mcg daily
- **Elderly > 65:** 25-50 mcg daily (start lower)
- **Cardiac disease:** 25 mcg daily
- **Pregnancy:** Full replacement immediately

**Titration:**
- Recheck TSH in 6-8 weeks after starting/changing dose
- Target TSH: 0.4 - 4.0 mU/L (some aim 0.5-2.5)
- Typical maintenance: 100-150 mcg daily

**Administration:**
- **Take on empty stomach**, 30 minutes before breakfast
- **Separate from:** Calcium, iron, PPIs (wait 4 hours)
- **Consistent timing** (same time each day)

**Monitoring:**
- TSH annually once stable
- TSH more frequently in pregnancy, elderly, cardiac disease
- **Monitor for over-treatment:** TSH < 0.1 → increased AF risk, osteoporosis

**Pregnancy:**
- **Pre-conception:** Optimize TSH < 2.5 mU/L
- **Increase dose by 25-50% immediately** when pregnant
- Target TSH < 2.5 (first trimester)
- **Check TSH each trimester**

**Subclinical Hypothyroidism (TSH 4-10, normal T4):**
- **Treat if:**
  - TSH > 10
  - TSH 4-10 + symptoms
  - Positive TPO antibodies
  - Pregnancy or planning pregnancy
  - Age < 65
- **Monitor if:** Asymptomatic, TSH < 10

**Myxoedema Coma (Emergency):**
- Altered mental status, hypothermia, bradycardia
- **IV levothyroxine 200-500 mcg** + **IV hydrocortisone**
- Gradual warming, ventilatory support if needed
- **ICU admission required**

**Sources:** NICE NG145, BTA 2023, ATA Guidelines 2014"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "endocrinology_thyroid",
                "focus": "hypothyroidism_management",
                "sources": ["NICE NG145", "BTA 2023", "ATA 2014"]
            }
        )

    def _manage_hyperthyroidism(self, query: str, context: dict) -> DomainQueryResult:
        """Hyperthyroidism management guidance"""
        answer = """**Hyperthyroidism (Overactive Thyroid) Management**

**Etiology:**
- **Graves' disease** (most common - autoimmune)
- **Toxic multinodular goiter**
- **Toxic adenoma** (single hot nodule)
- Thyroiditis (temporary)
- **Amiodarone-induced**

**Symptoms:**
- Weight loss, heat intolerance, sweating
- Palpitations, tachycardia, **atrial fibrillation**
- Tremor, anxiety, irritability
- **Eye signs** (Graves'): lid lag, stare, ophthalmopathy
- **Thyroid storm** (life-threatening emergency)

**Diagnosis:**
- **Suppressed TSH** + **Elevated Free T4/T3**
- **TSH receptor antibodies (TRAB):** Positive in Graves'
- **Radioisotope scan:** Differentiates causes

**Treatment Options:**

**1. Antithyroid Drugs (ATD):**

**Carbimazole / Methimazole:**
- **Starting:** 10-20 mg daily (Graves')
- **Titration:** Reduce to maintenance (5-10 mg) over 12-18 months
- **Monitoring:** FBC regularly (agranulocytosis risk - 0.3%)
- **Remission:** 40-50% achieve long-term remission

**PTU (Propylthiouracil):**
- Second-line (carbimazole intolerance)
- **First trimester pregnancy** (safer than carbimazole)
- Higher hepatotoxicity risk

**2. Radioiodine (I-131):**
- **Definitive treatment** ( thyroid ablation)
- **Contraindicated in pregnancy/breastfeeding**
- **Hypothyroidism eventual outcome** (levothyroxine needed)
- **Worsen eye disease** (if Graves' ophthalmopathy)

**3. Thyroidectomy:**
- **Total thyroidectomy** (definitive)
- Indications:
  - Large goiter with compressive symptoms
  - Severe ophthalmopathy
  - Failed radioiodine/ATD
  - Patient preference
- **Lifelong levothyroxine** required post-op

**Special Situations:**

**Pregnancy:**
- **PTU in first trimester**, switch to carbimazole after
- Target FT4 at upper limit of normal
- **TSH unreliable** in pregnancy (suppressed in 1st trimester)
- **Avoid radioiodine** (contraindicated)

**Graves' Ophthalmopathy:**
- **Mild:** Lubricating eye drops, sunglasses, smoking cessation
- **Moderate-severe:** Refer to ophthalmologist
- **Steroids** (IV methylprednisolone)
- **Radiotherapy** or orbital decompression (severe cases)

**Thyroid Storm (Emergency):**
- **Temperature > 38.5°C, AF, heart failure**
- **IV propranolol**, **IV glucocorticoids**
- **High-dose ATD** (PTU preferred)
- **Iodine** (block hormone release) - give AFTER ATD
- Supportive care, cooling, monitoring
- **ICU admission required**

**Monitoring During Treatment:**
- **TSH/FT4** every 6 weeks initially
- **FBC** at onset, then if symptoms of infection (agranulocytosis)
- **LFTs** if PTU used

**Sources:** NICE NG145, BTA 2023, ATA Guidelines 2016"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "endocrinology_thyroid",
                "focus": "hyperthyroidism_management",
                "sources": ["NICE NG145", "BTA 2023", "ATA 2016"]
            }
        )

    def _general_thyroid_guidance(self, query: str, context: dict) -> DomainQueryResult:
        """General thyroid information"""
        answer = """**Thyroid Disorders Overview**

**Thyroid Gland Function:**
- Butterfly-shaped gland in neck
- Produces T4 (thyroxine) and T3 (triiodothyronine)
- Regulated by TSH from pituitary gland
- Controls metabolism, temperature, heart rate

**Common Thyroid Conditions:**

**Hypothyroidism (Underactive):**
- Hashimoto's thyroiditis (autoimmune)
- Symptoms: fatigue, weight gain, cold, dry skin
- Treatment: Levothyroxine replacement

**Hyperthyroidism (Overactive):**
- Graves' disease (autoimmune)
- Toxic nodules
- Symptoms: weight loss, palpitations, anxiety, tremor
- Treatment: Antithyroid drugs, radioiodine, surgery

**Thyroid Nodules:**
- Very common (50% have nodules on USS)
- Most are benign (95%)
- Evaluation: Ultrasound ± FNA

**Thyroid Cancer:**
- Papillary (most common, excellent prognosis)
- Follicular, Medullary, Anaplastic (rare, aggressive)
- Treatment: Surgery ± radioiodine

**Who to Test:**
- Symptoms of thyroid dysfunction
- Goiter (enlarged thyroid)
- Nodules
- Atrial fibrillation
- Pregnancy or planning pregnancy
- Family history of thyroid disease
- **NOT** recommended for asymptomatic screening

**Sources:** NICE NG145, British Thyroid Association"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "endocrinology_thyroid",
                "focus": "general_information",
                "sources": ["NICE NG145", "BTA"]
            }
        )

    def _handle_adrenal_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle adrenal-related queries"""
        query_lower = query.lower()

        if "addison" in query_lower or "adrenal insufficiency" in query_lower:
            return self._manage_adrenal_insufficiency(query, context)
        elif "cushing" in query_lower or "cortisol" in query_lower:
            return self._assess_cushing(query, context)
        elif "pheochromocytoma" in query_lower or "phaeo" in query_lower:
            return self._assess_pheochromocytoma(query, context)
        else:
            return self._general_adrenal(query, context)

    def _manage_adrenal_insufficiency(self, query: str, context: dict) -> DomainQueryResult:
        """Adrenal insufficiency management"""
        answer = """**Adrenal Insufficiency (Addison's Disease) Management**

**Etiology:**
- **Primary (Addison's):** Autoimmune adrenalitis (70%), TB, HIV, metastases
- **Secondary:** Pituitary failure (ACTH deficiency)
- **Tertiary:** Prolonged glucocorticoid use → suppression

**Symptoms:**
- **Fatigue, weakness, anorexia**
- **Weight loss, nausea, vomiting**
- **Abdominal pain, diarrhea**
- **Salt craving, hyponatremia, hyperkalemia**
- **Hypotension, postural dizziness**
- **Hyperpigmentation** (primary only - ACTH elevated)
- **Hypoglycemia** (children)

**Diagnosis:**
- **Short Synacthen test:** Cortisol < 500 nmol/L at 30 min
- **9 AM cortisol:** < 100 nmol/L suggests AI
- **ACTH level:** Distinguishes primary vs secondary
- **Aldosterone/renin:** Low in primary, normal in secondary
- **Adrenal antibodies:** Positive if autoimmune

**Treatment: Glucocorticoid Replacement**

**Hydrocortisone:**
- **Dose:** 15-20 mg/day divided (10 mg morning, 5 mg afternoon)
- **Stress dosing:** 2-3x for minor illness, 5-10x for major stress
- **Immediate IV hydrocortisone 100mg** in adrenal crisis

**Alternative (Prednisolone):**
- 3-5 mg daily (longer-acting)
- Less physiological cortisol curve
- **NOT** for adrenal crisis (doesn't convert)

**Mineralocorticoid Replacement (Primary AI only):**

**Fludrocortisone:**
- **Dose:** 50-200 mcg daily
- Adjust based on BP, electrolytes, renin
- **NOT** needed for secondary AI (aldosterone intact)

**Adrenal Crisis (Emergency):**

**Triggers:**
- Infection, stress, surgery
- **Missed doses**, abrupt withdrawal
- **KEY:** STOP steroids abruptly

**Management:**
1. **IV Hydrocortisone 100mg** immediately, then 50-100mg 6-hourly
2. **IV Saline 1L** (0.9% NaCl) rapidly
3. Correct hypoglycemia (IV dextrose)
4. Treat underlying cause
5. Monitor electrolytes, glucose

**Sick Day Rules:**
- **Minor illness:** 2-3x hydrocortisone dose for 2-3 days
- **Major illness/surgery:** 5-10x dose, IV hydrocortisone if needed
- **Never stop steroids** - ensure emergency injection available

**Patient Education:**
- **Wear Medic Alert bracelet**
- Carry emergency hydrocortisone injection
- Educate family/friends about adrenal crisis
- Sick day rules printed and available
- Regular endocrinology follow-up

**Monitoring:**
- Blood pressure, electrolytes
- Weight, well-being
- **Don't** routinely check cortisol levels (treat clinically)
- Monitor for over-replacement (Cushingoid features)

**Sources:** NICE NG169, Society for Endocrinology UK 2023"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "endocrinology_adrenal",
                "focus": "adrenal_insufficiency",
                "sources": ["NICE NG169", "Society for Endocrinology UK 2023"]
            }
        )

    def _assess_cushing(self, query: str, context: dict) -> DomainQueryResult:
        """Cushing's syndrome assessment"""
        answer = """**Cushing's Syndrome Assessment**

**Definition:** Chronic glucocorticoid excess

**Etiology:**
- **ACTH-dependent (80%):**
  - Pituitary adenoma (Cushing's disease) - 70%
  - Ectopic ACTH (small cell lung cancer) - 10%
- **ACTH-independent (20%):**
  - Adrenal adenoma
  - Adrenal carcinoma
  - **Iatrogenic** (exogenous steroids - MOST COMMON)

**Clinical Features:**
- **Central obesity, moon facies**
- **Buffalo hump** (dorsocervical fat pad)
- **Plethora, thin skin, easy bruising**
- **Purple striae** (abdomen, thighs)
- **Proximal myopathy** (difficulty rising from chair)
- **Hypertension, diabetes, osteoporosis**
- **Hirsutism, menstrual irregularity** (women)

**Investigation:**

**First-line Screening:**
1. **24-hour urinary free cortisol (UFC)** - 2 collections
2. **Late-night salivary cortisol** - 2 measurements
3. **Overnight dexamethasone suppression test (DST):**
   - 1 mg dexamethasone at 11 PM
   - Measure cortisol at 9 AM
   - **Cushing's:** Cortisol > 50 nmol/L (not suppressed)

**Second-line (if screening positive):**
- **ACTH level:**
  - **High/normal:** ACTH-dependent (pituitary or ectopic)
  - **Low:** ACTH-independent (adrenal)
- **High-dose DST:** Distinguishes pituitary from ectopic
- **CRH stimulation test**
- **Imaging:**
  - Pituitary MRI (if ACTH-dependent)
  - CT adrenals (if ACTH-independent)
  - CT chest/abdomen (if ectopic suspected)

**Differential Diagnosis:**

**Pseudo-Cushing's:**
- Depression, alcoholism, obesity
- Normal UFC, normal DST
- **False positives** can occur

**Treatment:**

**Cushing's Disease (Pituitary):**
- **Transsphenoidal hypophysectomy** (first-line)
- **Radiotherapy** (if surgery contraindicated)
- **Medical:** Pasireotide, cabergoline, ketoconazole

**Ectopic ACTH:**
- **Tumor resection** (if localized)
- **Medical control:** Ketoconazole, metyrapone, mitotane
- **Bilateral adrenalectomy** (if refractory)

**Adrenal Adenoma:**
- **Laparoscopic adrenalectomy**

**Perioperative Management:**
- **Glucocorticoid replacement** post-op until HPA axis recovers
- **Stress-dose steroids** during surgery
- Monitor for adrenal insufficiency

**Sources:** NICE NG169, Endocrine Society 2023"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "endocrinology_adrenal",
                "focus": "cushing_syndrome",
                "sources": ["NICE NG169", "Endocrine Society 2023"]
            }
        )

    def _assess_pheochromocytoma(self, query: str, context: dict) -> DomainQueryResult:
        """Pheochromocytoma assessment"""
        answer = """**Pheochromocytoma Assessment**

**Definition:** Catecholamine-secreting tumor from adrenal medulla

**Rule of 10s:**
- 10% bilateral
- 10% extra-adrenal (paraganglioma)
- 10% malignant
- 10% familial
- 10% pediatric

**Clinical Presentation:**
- **Episodic:** Headache, sweating, tachycardia ("paroxysmal")
- **Sustained:** Hypertension, palpitations, anxiety
- **Crisis:** Hypertensive emergency, cardiomyopathy, shock
- **Associated symptoms:** Anxiety, tremor, weight loss

**Genetic Syndromes:**
- MEN2 (RET mutation)
- Von Hippel-Lindau (VHL)
- Neurofibromatosis type 1 (NF1)
- **Screen all patients** for genetic mutations

**Diagnosis:**

**Biochemical Testing:**
1. **24-hour urinary metanephrines** (most sensitive)
2. **Plasma-free metanephrines** (high sensitivity, some false positives)
3. **Plasma catecholamines** (less sensitive)

**Interpretation:**
- **3x upper limit:** Pheo highly likely
- **Borderline:** Repeat testing, consider clonidine suppression test

**Localization:**
- **CT abdomen** (adrenals)
- **MRI** (better for extra-adrenal)
- **123I-MIBG scan** (if CT negative or metastatic disease)
- **68Ga-DOTATATE PET/CT** (most sensitive)

**Treatment:**

**Preoperative Preparation:**
1. **Alpha-blockade:** Phenoxybenzamine 10-20 mg TDS for 10-14 days
2. **Volume expansion:** High sodium diet, hydration
3. **Beta-blockade:** AFTER alpha-blockade (if tachycardia)
4. **Avoid:** Drugs that trigger catecholamine release (metoclopramide, anesthetics)

**Surgery:**
- **Laparoscopic adrenalectomy** (tumor < 8 cm)
- **Open surgery** (large or invasive tumors)
- **Intraoperative monitoring:** Arterial line, CVP
- **IV phentolamine** for hypertensive crises

**Malignant Pheochromocytoma:**
- **Metastases** (bone, liver, lung)
- **Treatment:** Surgical debulking, radionuclide therapy (131I-MIBG), chemotherapy
- **Prognosis:** Variable (5-year survival 50%)

**Follow-up:**
- Annual biochemical testing (recurrence risk)
- Genetic counseling
- Screening for associated tumors (MEN2)

**Sources:** Endocrine Society 2024, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "endocrinology_adrenal",
                "focus": "pheochromocytoma",
                "sources": ["Endocrine Society 2024", "NICE NG169"]
            }
        )

    def _general_adrenal(self, query: str, context: dict) -> DomainQueryResult:
        """General adrenal information"""
        answer = """**Adrenal Gland Disorders Overview**

**Adrenal Anatomy:**
- Two glands sitting on kidneys
- **Adrenal cortex:** Glucocorticoids (cortisol), mineralocorticoids (aldosterone), androgens
- **Adrenal medulla:** Catecholamines (adrenaline, noradrenaline)

**Common Adrenal Conditions:**

**Adrenal Insufficiency (Addison's):**
- Underactive adrenal glands
- Fatigue, low blood pressure, salt craving
- Treatment: Hydrocortisone + fludrocortisone

**Cushing's Syndrome:**
- Cortisol excess
- Weight gain, moon facies, easy bruising
- Most commonly: Exogenous steroid use

**Conn's Syndrome:**
- Aldosterone-producing adenoma
- Hypertension, low potassium
- Treatment: Adrenalectomy or mineralocorticoid antagonist

**Pheochromocytoma:**
- Catecholamine-secreting tumor
- Paroxysmal hypertension, palpitations, sweating
- Surgical removal after alpha-blockade

**Adrenal Incidentaloma:**
- Adrenal nodule found incidentally on imaging
- Most are benign non-functioning adenomas
- Assessment: Hormone evaluation + imaging characteristics

**Sources:** NICE NG169, Society for Endocrinology"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.84,
            metadata={
                "specialty": "endocrinology_adrenal",
                "focus": "general_information",
                "sources": ["NICE NG169", "Society for Endocrinology"]
            }
        )

    def _handle_pituitary_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pituitary-related queries"""
        query_lower = query.lower()

        if "prolactin" in query_lower or "prolactinoma" in query_lower:
            return self._manage_prolactinoma(query, context)
        elif "acromegaly" in query_lower or "growth hormone" in query_lower:
            return self._assess_acromegaly(query, context)
        elif "diabetes insipidus" in query_lower:
            return self._manage_diabetes_insipidus(query, context)
        elif "pituitary tumor" in query_lower or "pituitary adenoma" in query_lower:
            return self._manage_pituitary_tumor(query, context)
        else:
            return self._general_pituitary(query, context)

    def _manage_prolactinoma(self, query: str, context: dict) -> DomainQueryResult:
        """Prolactinoma management"""
        answer = """**Prolactinoma Management**

**Definition:** Prolactin-secreting pituitary adenoma

**Epidemiology:**
- Most common functioning pituitary adenoma
- **Women:** Amenorrhea, galactorrhea, infertility
- **Men:** Decreased libido, impotence, visual symptoms (larger tumors)

**Symptoms:**

**Women:**
- **Amenorrhea/oligomenorrhea**
- **Galactorrhea** (milk discharge)
- **Infertility**
- **Low estrogen** (osteoporosis risk)
- **Headache, visual symptoms** (macroprolactinoma)

**Men:**
- **Decreased libido, erectile dysfunction**
- **Gynecomastia** (rare galactorrhea)
- **Low testosterone**
- **Visual field defects** (bitemporal hemianopia)

**Diagnosis:**
- **Elevated prolactin:**
  - Microprolactinoma: 50-200 ng/mL
  - Macroprolactinoma: > 200 ng/mL
- **Pituitary MRI:** Confirm adenoma, assess size
- **Exclude other causes:**
  - Pregnancy (always check!)
  - Hypothyroidism (check TSH)
  - Medications (antipsychotics, metoclopramide)
  - **Macroprolactin** (biologically inactive - repeat with PEG precipitation)

**Treatment:**

**First-line: Dopamine Agonists**

**Cabergoline:**
- **Dose:** 0.5 mg weekly (increase gradually)
- **Efficacy:** 80-90% tumor shrinkage, normalize prolactin
- **Side effects:** Nausea, dizziness, impulse control disorders
- **Monitoring:** Echocardiography (valvular heart disease risk - rare)

**Bromocriptine:**
- **Dose:** 2.5-10 mg daily divided
- **Less expensive** than cabergoline
- **More side effects:** Nausea, hypotension
- **Safe in pregnancy** (extensive experience)

**Surgery (Transsphenoidal Hypophysectomy):**
- Indications:
  - **Dopamine agonist intolerance**
  - **Resistant tumors** (prolactin not normalizing)
  - **Apoplexy** (tumor hemorrhage)
  - **Patient preference**

**Radiotherapy:**
- Rarely used
- For refractory cases post-surgery

**Pregnancy:**
- **Stop cabergoline/bromocriptine** once pregnant
- **Monitor visual fields** (macroprolactinoma may grow)
- **Bromocriptine** can be restarted if symptomatic tumor growth
- **Breastfeeding:** Safe (prolactin naturally elevated)

**Monitoring:**
- Prolactin levels
- MRI pituitary (if symptoms of mass effect)
- Visual fields (macroprolactinoma)
- Bone density (hypogonadism risk)

**Sources:** Pituitary Society 2023, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "endocrinology_pituitary",
                "focus": "prolactinoma",
                "sources": ["Pituitary Society 2023", "NICE NG169"]
            }
        )

    def _assess_acromegaly(self, query: str, context: dict) -> DomainQueryResult:
        """Acromegaly assessment"""
        answer = """**Acromegaly Assessment**

**Definition:** Growth hormone (GH) secreting pituitary adenoma

**Epidemiology:**
- 3-4 cases per million
- Diagnosis delayed 7-10 years on average
- Mean age at diagnosis: 40-50 years

**Clinical Features:**

**Coarse Facial Features:**
- **Frontal bossing, prognathism**
- **Macroglossia** (large tongue)
- **Dental malocclusion**
- ** enlarged hands and feet** (ring size, shoe size)
- **Skin thickening, oily skin**

**Systemic Manifestations:**
- **Cardiomyopathy** (leading cause of death)
- **Hypertension**
- **Sleep apnea**
- **Diabetes mellitus** (insulin resistance)
- **Carpal tunnel syndrome**
- **Arthropathy** (joint pain)
- **Colon polyps/cancer** (increased risk)

**Diagnosis:**

**First-line:**
- **IGF-1** (Insulin-like Growth Factor-1)
  - Age-adjusted normal ranges
  - **Elevated:** Screen for acromegaly

**Confirmation:**
- **Oral Glucose Tolerance Test (OGTT) with GH:**
  - 75g glucose load
  - **Acromegaly:** GH fails to suppress < 1 ng/mL (or < 0.4 ng/mL sensitive assays)
  - **Nadir GH** > 1 ng/mL confirms diagnosis

**Localization:**
- **Pituitary MRI**
- **Microadenoma** (< 10 mm) vs **Macroadenoma** (> 10 mm)

**Treatment:**

**First-line: Transsphenoidal Surgery**
- **Goal:** Complete tumor resection
- **Remission rates:**
  - Microadenoma: 85%
  - Macroadenoma: 40-50%
- **Complications:** Hypopituitarism, diabetes insipidus, CSF leak

**Medical Therapy (if surgery contraindicated or persistent disease):**

**Somatostatin Analogues:**
- **Octreotide LAR:** 20-30 mg IM monthly
- **Lanreotide:** 60-120 mg IM monthly
- **Efficacy:** 50-70% normalize IGF-1
- **Side effects:** Gallstones, GI upset, bradycardia

**GH Receptor Antagonist:**
- **Pegvisomant:** 10-30 mg SC daily
- **Efficacy:** 90% normalize IGF-1
- **Cost:** Very expensive
- **Monitoring:** Liver enzymes

**Dopamine Agonists:**
- **Cabergoline:** Less effective, cheap
- **For:** Mild disease, combination therapy

**Radiotherapy:**
- **Conventional fractionated:** 10-20% remission per year
- **Stereotactic (Gamma Knife):** Faster response
- **Indications:** Residual disease post-surgery, medical therapy failure

**Monitoring:**
- IGF-1 levels (treatment target)
- Glucose tolerance
- Cardiac echo (cardiomyopathy)
- Colonoscopy (polyps)
- Sleep study (apnea)

**Prognosis:**
- **Mortality 2-3x increased** if untreated (cardiovascular disease)
- Normalizes with successful treatment

**Sources:** Pituitary Society 2023, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "endocrinology_pituitary",
                "focus": "acromegaly",
                "sources": ["Pituitary Society 2023", "NICE NG169"]
            }
        )

    def _manage_diabetes_insipidus(self, query: str, context: dict) -> DomainQueryResult:
        """Diabetes insipidus management"""
        answer = """**Diabetes Insipidus Management**

**Definition:** Inability to concentrate urine (large volumes of dilute urine)

**NOT** related to diabetes mellitus (sugar diabetes)

**Types:**

**1. Central DI (Cranial DI):**
- **ADH (vasopressin) deficiency**
- Posterior pituitary dysfunction
- **Causes:**
  - Pituitary surgery/transsphenoidal surgery (30% transient)
  - Head trauma
  - Brain tumors (craniopharyngioma, pituitary adenoma)
  - Infiltrative diseases (sarcoidosis, histiocytosis)
  - Idiopathic (30%)

**2. Nephrogenic DI:**
- **Kidney unresponsive to ADH**
- **Causes:**
  - Congenital (V2 receptor mutations, aquaporin-2 mutations)
  - **Lithium** (most common acquired cause)
  - Hypercalcemia, hypokalemia
  - Chronic kidney disease
  - Medications (demeclocycline, amphotericin B)

**3. Gestational DI:**
- Placental vasopressinase degradation of ADH
- Resolves after delivery

**Clinical Presentation:**
- **Polyuria:** > 3L/day (can be > 10L/day)
- **Polydipsia:** Excessive thirst
- **Nocturia:** Waking multiple times to urinate
- **Dehydration, hypernatremia** if access to water restricted

**Diagnosis:**

**Water Deprivation Test:**
- **Withhold water** under supervision
- **Measure:** Urine osmolality, plasma osmolality, sodium
- **Desmopressin challenge**
- **Interpretation:**
  - **Central DI:** Urine remains dilute, concentrates after desmopressin
  - **Nephrogenic DI:** Urine remains dilute, NO response to desmopressin
  - **Primary polydipsia:** Psychogenic water drinking

**Treatment:**

**Central DI:**
- **Desmopressin (DDAVP):**
  - **Oral:** 100-200 mcg BID-TID
  - **Intranasal:** 10-20 mcg BID
  - **SC/IV:** 1-2 mcg daily
- **Thiazide diuretics:** (if mild)
- **Low-sodium diet**

**Nephrogenic DI:**
- **Treat underlying cause** (stop lithium, correct electrolytes)
- **Thiazide diuretics:** (reduce polyuria)
- **Indomethacin:** (prostaglandin synthesis inhibitor)
- **Low-sodium diet**

**Emergency Management:**
- **IV hypotonic fluids** (D5W or 0.45% NaCl)
- **Desmopressin** (central DI)
- **Correct hypernatremia** slowly (0.5 mmol/L/hour)

**Monitoring:**
- Serum sodium
- Urine output
- Plasma/urine osmolality
- Watch for hyponatremia (over-treatment)

**Sources:** Pituitary Society 2023, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "endocrinology_pituitary",
                "focus": "diabetes_insipidus",
                "sources": ["Pituitary Society 2023", "NICE NG169"]
            }
        )

    def _manage_pituitary_tumor(self, query: str, context: dict) -> DomainQueryResult:
        """Pituitary tumor management"""
        answer = """**Pituitary Tumor Management**

**Classification:**

**Microadenoma:** < 10 mm
**Macroadenoma:** > 10 mm

**Types:**
1. **Functioning:** Secrete hormones (prolactinoma, GH, ACTH, TSH)
2. **Non-functioning:** No hormone secretion (most common macroadenoma)

**Clinical Presentation:**

**Hormonal Effects:**
- **Prolactinoma:** Amenorrhea, galactorrhea
- **Acromegaly:** Coarse features, enlarged hands/feet
- **Cushing's:** Weight gain, striae, hypertension
- **TSH-oma:** Palpitations, weight loss (hyperthyroidism)
- **Non-functioning:** Hypopituitarism (low gonadotropins → hypogonadism)

**Mass Effects:**
- **Visual field defects:** Bitemporal hemianopia (chiasm compression)
- **Headache**
- **Apoplexy:** Tumor hemorrhage/infarction → headache, visual loss, ophthalmoplegia (EMERGENCY)

**Investigation:**

**Hormonal Evaluation:**
- **Prolactin, IGF-1, 8 AM cortisol, TSH, FT4, LH, FSH, testosterone/estradiol**
- **24-hour urinary cortisol** (Cushing's screen)
- **Tests for hormonal hypersecretion**

**Imaging:**
- **Pituitary MRI** (gold standard)
- **CT head** (if MRI contraindicated)

**Visual Field Testing:**
- Formal perimetry (macroadenoma)

**Treatment:**

**Surgery (Transsphenoidal Hypophysectomy):**
- **First-line for:**
  - Non-functioning macroadenoma
  - Acromegaly, Cushing's, TSH-oma
  - Visual symptoms
- **Outcomes:**
  - Microadenoma: 80-90% remission
  - Macroadenoma: 40-60% remission

**Medical Therapy:**
- **Prolactinoma:** Dopamine agonists (cabergoline)
- **Acromegaly:** Somatostatin analogues, pegvisomant
- **Cushing's:** Ketoconazole, metyrapone, pasireotide

**Radiotherapy:**
- **Conventional fractionated** (slow response, 5-10 years)
- **Stereotactic (Gamma Knife)** (faster, more precise)
- **Indications:** Residual disease post-surgery, medical therapy failure

**Pituitary Apoplexy (Emergency):**
- **Sudden headache, visual loss, ophthalmoplegia**
- **Urgent neurosurgical decompression**
- **Hormone replacement** (acute adrenal insufficiency common)

**Post-treatment Monitoring:**
- Hormone replacement (hypopituitarism)
- Visual fields
- MRI surveillance (recurrence)
- Quality of life

**Sources:** Pituitary Society 2023, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "endocrinology_pituitary",
                "focus": "pituitary_tumor",
                "sources": ["Pituitary Society 2023", "NICE NG169"]
            }
        )

    def _general_pituitary(self, query: str, context: dict) -> DomainQueryResult:
        """General pituitary information"""
        answer = """**Pituitary Gland Overview**

**Pituitary Anatomy:**
- **"Master gland"** at base of brain
- **Anterior pituitary:** TSH, ACTH, LH/FSH, GH, prolactin
- **Posterior pituitary:** ADH (vasopressin), oxytocin
- Regulated by hypothalamus

**Common Pituitary Conditions:**

**Prolactinoma:**
- Most common functioning adenoma
- Amenorrhea, galactorrhea, infertility

**Acromegaly:**
- GH excess (adults)
- Coarse features, enlarged hands/feet

**Cushing's Disease:**
- ACTH excess → cortisol excess
- Weight gain, striae, hypertension

**Non-functioning Adenoma:**
- No hormone secretion
- Mass effects (headache, visual symptoms)

**Hypopituitarism:**
- Underactive pituitary
- Low hormone levels (ACTH → adrenal insufficiency, TSH → hypothyroidism)

**Diabetes Insipidus:**
- ADH deficiency
- Large volumes of dilute urine, excessive thirst

**Sources:** Pituitary Society, NICE NG169"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.83,
            metadata={
                "specialty": "endocrinology_pituitary",
                "focus": "general_information",
                "sources": ["Pituitary Society", "NICE NG169"]
            }
        )

    def _handle_calcium_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle calcium/parathyroid queries"""
        query_lower = query.lower()

        if "hyperparathyroid" in query_lower or "high calcium" in query_lower:
            return self._manage_hyperparathyroidism(query, context)
        elif "hypoparathyroid" in query_lower or "low calcium" in query_lower:
            return self._manage_hypoparathyroidism(query, context)
        elif "osteoporosis" in query_lower:
            return self._manage_osteoporosis(query, context)
        elif "vitamin d" in query_lower:
            return self._manage_vitamin_d(query, context)
        else:
            return self._general_calcium(query, context)

    def _manage_hyperparathyroidism(self, query: str, context: dict) -> DomainQueryResult:
        """Hyperparathyroidism management"""
        answer = """**Hyperparathyroidism Management**

**Types:**

**Primary Hyperparathyroidism:**
- **PTH excessive, calcium high**
- **Causes:**
  - **Parathyroid adenoma** (85%, single gland)
  - **Parathyroid hyperplasia** (15%, 4 glands)
  - **Parathyroid carcinoma** (rare < 1%)

**Secondary Hyperparathyroidism:**
- **PTH high, calcium low/normal**
- **Causes:**
  - **Chronic kidney disease** (most common)
  - Vitamin D deficiency
  - Malabsorption

**Clinical Presentation:**

**Asymptomatic (80%):**
- Incidentally discovered hypercalcemia

**Symptomatic:**
- **"Stones, bones, groans, thrones":**
  - **Stones:** Nephrolithiasis (kidney stones)
  - **Bones:** Osteopenia, osteoporosis
  - **Groans:** Abdominal pain, constipation, nausea
  - **Thrones:** Depression, fatigue, cognitive impairment
- **Polyuria, polydipsia**

**Diagnosis:**

**Labs:**
- **Calcium:** High (or high-normal)
- **PTH:** High or inappropriately normal (should be suppressed with high calcium)
- **Phosphate:** Low (PTH decreases renal phosphate reabsorption)
- **Vitamin D:** 25-OH vitamin D (to exclude deficiency)
- **24-hour urine calcium:** For stone risk assessment

**Localization (preoperative):**
- **Parathyroid ultrasound**
- **Sestamibi scan** (Tc-99m)
- **CT 4D-CT** (if ultrasound/sestamibi discordant)

**Treatment:**

**Asymptomatic (meeting surgery criteria):**
- **Age < 50**
- **Serum calcium > 1 mg/dL above normal**
- **Creatinine clearance < 60 mL/min**
- **T-score < -2.5** at any site
- **Nephrolithiasis**
- **24-hour urine calcium > 400 mg/day**

**Parathyroidectomy:**
- **Focused exploration** (if localized)
- **Bilateral exploration** (if not localized)
- **Intraoperative PTH monitoring** (drops > 50% indicates success)
- **Cure rate:** 95-98%

**Medical Management (if not surgical candidate):**
- **Hydration** (2-3 L/day)
- **Avoid:** Thiazide diureptics (increase calcium)
- **Bisphosphonates:** (for bone protection)
- **Cinacalcet:** (calcimimetic, lowers calcium, PTH)
- **Observation** (mild cases)

**Monitoring (untreated):**
- Serum calcium, creatinine every 6 months
- Bone density annually

**Postoperative:**
- **Hungry bone syndrome:** (rapid bone remineralization → hypocalcemia)
- Calcium supplementation post-op (often needed)
- PTH normalization (if successful)

**Sources:** American Association of Endocrine Surgeons 2022, NICE NG132"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "endocrinology_calcium",
                "focus": "hyperparathyroidism",
                "sources": ["AAES 2022", "NICE NG132"]
            }
        )

    def _manage_hypoparathyroidism(self, query: str, context: dict) -> DomainQueryResult:
        """Hypoparathyroidism management"""
        answer = """**Hypoparathyroidism Management**

**Definition:** Low PTH → hypocalcemia, hyperphosphatemia

**Causes:**
- **Post-thyroidectomy** (most common, transient or permanent)
- **Post-parathyroidectomy** (for hyperparathyroidism)
- **Autoimmune** (polyglandular autoimmune syndrome)
- **Genetic** (DiGeorge syndrome, CASR mutations)
- **Infiltrative** (hemochromatosis, Wilson's disease)

**Clinical Presentation:**

**Acute Hypocalcemia:**
- **Neuromuscular irritability:**
  - **Tetany, perioral numbness, carpopedal spasm**
  - **Trousseau's sign** (carpal spasm after BP cuff)
  - **Chvostek's sign** (facial muscle spasm)
- **Seizures**
- **Laryngospasm, bronchospasm** (life-threatening)

**Chronic Hypocalcemia:**
- **Basal ganglia calcification**
- **Cataracts**
- **Dry skin, brittle nails**
- **Dental abnormalities**

**Diagnosis:**
- **Calcium:** Low
- **Phosphate:** High
- **PTH:** Low or inappropriately normal
- **Vitamin D:** Normal/high (distinguish from vitamin D deficiency)
- **Urine calcium:** Low (distinguish from vitamin D deficiency)

**Treatment:**

**Acute Hypocalcemia (Symptomatic):**
- **IV Calcium gluconate** 10% (10-20 mL over 10 minutes)
- **Followed by:** IV calcium infusion (1-2 mg/kg/hour)
- **Oral calcium + vitamin D** (once stable)

**Chronic Hypocalcemia:**

**Calcium Supplements:**
- **Calcium carbonate** (500-1000 mg TID-QID)
  - Take with food (requires acid for absorption)
- **Calcium citrate** (if on PPIs)

**Active Vitamin D (Calcitriol):**
- **Calcitriol** (1,25-dihydroxyvitamin D): 0.25-0.5 mcg BID
- **Alfacalcidol:** 0.5-1.0 mcg daily
- **NOT regular vitamin D** (ineffective in hypoparathyroidism)

**Thiazide Diuretics:**
- **Decrease urinary calcium loss**
- **For:** Persistent hypocalcemia despite high-dose calcium

**Monitoring:**
- Calcium, phosphate (target low-normal calcium)
- 24-hour urine calcium (watch for hypercalciuria → nephrolithiasis)
- Renal function

**Complications:**
- **Hypercalciuria, nephrolithiasis** (if calcium too high)
- **Basal ganglia calcification**
- **Cataracts**

**Sources:** NICE NG132, European Society of Endocrinology 2015"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "endocrinology_calcium",
                "focus": "hypoparathyroidism",
                "sources": ["NICE NG132", "ESE 2015"]
            }
        )

    def _manage_osteoporosis(self, query: str, context: dict) -> DomainQueryResult:
        """Osteoporosis management"""
        answer = """**Osteoporosis Management**

**Definition:**
- **T-score ≤ -2.5** (bone mineral density 2.5 SD below young adult mean)
- **Low bone mass**, increased fracture risk

**Risk Factors:**

**Non-modifiable:**
- **Age > 65**, female sex
- **Caucasian, Asian**
- **Family history** of hip fracture
- **Previous fracture** (fragility fracture)
- **Menopause** (estrogen deficiency)

**Modifiable:**
- **Glucocorticoids** (> 3 months)
- **Smoking**, excessive alcohol
- **Low BMI** (< 20)
- **Rheumatoid arthritis**
- **Vitamin D deficiency**
- **Secondary causes:** Hyperparathyroidism, hyperthyroidism, malabsorption, CKD

**Screening:**

**DEXA Scan (Dual-energy X-ray Absorptiometry):**
- **Sites:** Lumbar spine, hip
- **T-score:**
  - Normal: > -1.0
  - Osteopenia: -1.0 to -2.5
  - Osteoporosis: ≤ -2.5
- **FRAX** (fracture risk assessment)

**Treatment:**

**Lifestyle:**
- **Weight-bearing exercise** (30 min, 3x/week)
- **Smoking cessation**
- **Alcohol moderation** (< 2 units/day)
- **Fall prevention:** Home safety, balance training, vision check

**Calcium + Vitamin D:**
- **Calcium:** 1000-1200 mg/day (diet + supplement)
- **Vitamin D:** 800-1000 IU/day (20-25 mcg)
- **Essential baseline** (but NOT sufficient alone for treatment)

**Antiresorptive Agents:**

**Bisphosphonates (First-line):**
- **Alendronate:** 70 mg weekly
- **Risedronate:** 35 mg weekly
- **Zoledronic acid:** 5 mg IV yearly
- **Contraindications:** Esophageal disorders, unable to sit upright
- **Side effects:** Esophagitis, osteonecrosis of jaw (rare), atypical femur fracture (rare)

**Denosumab:**
- **RANKL inhibitor:** 60 mg SC every 6 months
- **Indications:** Bisphosphonate failure, CKD
- **Side effects:** Hypocalcemia, infection risk, rebound vertebral fractures if stopped

**Selective Estrogen Receptor Modulators (SERMs):**
- **Raloxifene:** 60 mg daily
- **For:** Postmenopausal women with vertebral fractures
- **Reduces breast cancer risk**

**Hormone Replacement Therapy (HRT):**
- **For:** Menopausal symptoms + osteoporosis prevention
- **Not first-line** for osteoporosis alone

**Anabolic Agents (Severe Osteoporosis):**

**Teriparatide (PTH 1-34):**
- **20 mcg SC daily** for 2 years (max lifetime)
- **Indications:** Severe osteoporosis, fractures on bisphosphonates

**Romosozumab:**
- **Sclerostin antibody:** 210 mg SC monthly for 1 year
- **Anabolic + antiresorptive**

**Monitoring:**
- **DEXA** every 1-2 years
- **Height** (annual)
- **Vertebral fracture assessment** (if height loss)
- **Calcium, vitamin D** levels
- **Bone turnover markers** (optional)

**Fracture Risk Reduction:**
- **Vertebral:** 50-70% reduction
- **Hip:** 40-50% reduction
- **Non-vertebral:** 20-30% reduction

**Sources:** NICE CG146, NOF 2023, Royal College of Physicians 2024"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "endocrinology_calcium",
                "focus": "osteoporosis",
                "sources": ["NICE CG146", "NOF 2023", "RCP 2024"]
            }
        )

    def _manage_vitamin_d(self, query: str, context: dict) -> DomainQueryResult:
        """Vitamin D management"""
        answer = """**Vitamin D Management**

**Metabolism:**
- **Vitamin D3 (cholecalciferol):** Synthesized in skin (UVB), dietary sources
- **25-hydroxyvitamin D:** Storage form, measured in blood (half-life 2-3 weeks)
- **1,25-dihydroxyvitamin D (calcitriol):** Active form, regulated by PTH

**Sources:**
- **Sunlight:** 10-15 minutes midday sun (face, arms) → 10,000 IU
- **Diet:** Fatty fish, fortified milk, eggs (minimal dietary sources)

**Deficiency Classification:**

| Category | 25-OH Vitamin D Level |
|----------|----------------------|
| **Severe deficiency** | < 12 ng/mL (< 30 nmol/L) |
| **Mild-moderate deficiency** | 12-20 ng/mL (30-50 nmol/L) |
| **Insufficiency** | 20-30 ng/mL (50-75 nmol/L) |
| **Sufficient** | > 30 ng/mL (> 75 nmol/L) |
| **Optimal** | 40-60 ng/mL (100-150 nmol/L) |
| **Toxicity** | > 150 ng/mL (> 375 nmol/L) |

**Causes of Deficiency:**
- **Limited sun exposure** (winter, high latitude, sunscreen, clothing)
- **Dark skin** (melanin blocks UVB)
- **Elderly** (reduced skin synthesis)
- **Obesity** (vitamin D sequestration in fat)
- **Malabsorption** (celiac, IBD, bariatric surgery)
- **Medications:** Anticonvulsants, glucocorticoids

**Clinical Effects of Deficiency:**

**Adults:**
- **Osteomalacia** (bone pain, proximal muscle weakness)
- **Osteoporosis** (low bone mass, fractures)
- **Secondary hyperparathyroidism**
- **Hypocalcemia** (severe deficiency)

**Children:**
- **Rickets** (bony deformities, growth failure)

**Extra-skeletal Effects (controversial):**
- Falls, muscle weakness
- Cancer, cardiovascular disease (association unclear)

**Treatment:**

**Severe Deficiency (< 12 ng/mL):**
- **Vitamin D3:** 50,000 IU weekly for 6-12 weeks
- **Followed by:** Maintenance therapy

**Mild-Moderate Deficiency (12-20 ng/mL):**
- **Vitamin D3:** 2,000-4,000 IU daily for 3 months
- **Recheck** 25-OH vitamin D level

**Insufficiency (20-30 ng/mL):**
- **Vitamin D3:** 1,000-2,000 IU daily

**Maintenance:**
- **800-2,000 IU daily** (individualized based on level, BMI, sun exposure)

**Co-factors:**
- **Calcium:** 1,000-1,200 mg daily (diet + supplement)
- **Magnesium:** 400 mg daily (optional, for bone health)

**Toxicity:**
- **Rare** (requires > 40,000 IU/day for months)
- **Hypercalcemia**, hypercalciuria, nephrolithiasis
- **Treatment:** Stop vitamin D, hydration, consider glucocorticoids

**Monitoring:**
- **25-OH vitamin D** (after 3 months of treatment)
- **Calcium** (if high dose)
- **NOT** 1,25-dihydroxyvitamin D (unreliable, can be high in deficiency)

**Sources:** NICE TA 161, Endocrine Society 2011, Royal Osteoporosis Society 2023"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "endocrinology_calcium",
                "focus": "vitamin_d",
                "sources": ["NICE TA 161", "Endocrine Society 2011", "ROS 2023"]
            }
        )

    def _general_calcium(self, query: str, context: dict) -> DomainQueryResult:
        """General calcium metabolism information"""
        answer = """**Calcium Metabolism Overview**

**Calcium Homeostasis:**
- **Total calcium:** 8.5-10.5 mg/dL (2.12-2.65 mmol/L)
- **Ionized calcium:** 4.6-5.3 mg/dL (1.15-1.33 mmol/L)
- **Regulated by:** PTH, vitamin D, calcitonin

**Common Calcium Disorders:**

**Hypercalcemia (High Calcium):**
- **Primary hyperparathyroidism** (most common outpatient)
- **Malignancy** (most common inpatient - PTHrP)
- Symptoms: "stones, bones, groans, thrones"

**Hypocalcemia (Low Calcium):**
- **Hypoparathyroidism** (post-thyroidectomy)
- **Vitamin D deficiency**
- **Chronic kidney disease**
- Symptoms: Tetany, perioral numbness, seizures

**Osteoporosis:**
- Low bone mass, increased fracture risk
- T-score ≤ -2.5 on DEXA
- Treatment: Bisphosphonates, denosumab, teriparatide

**Sources:** NICE NG132, Royal Osteoporosis Society"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.84,
            metadata={
                "specialty": "endocrinology_calcium",
                "focus": "general_information",
                "sources": ["NICE NG132", "ROS"]
            }
        )

    def _handle_menopause_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle menopause/HRT queries"""
        answer = """**Menopause and Hormone Replacement Therapy (HRT)**

**Definition:**
- **Cessation of menstruation** for 12 months
- **Average age:** 51 years (range 45-55)
- **Perimenopause:** 2-8 years before menopause (symptoms + irregular cycles)

**Symptoms:**
- **Vasomotor:** Hot flashes, night sweats (80%)
- **Urogenital:** Vaginal dryness, dyspareunia, urinary frequency
- **Psychological:** Mood swings, anxiety, depression, poor sleep
- **Sexual:** Low libido, sexual dysfunction
- **Somatic:** Joint pains, palpitations, headache, fatigue

**Diagnosis:**
- **Clinical:** No menstruation for 12 months (age > 45)
- **Perimenopause:** Irregular cycles + symptoms (age 45-55)
- **Biochemical:** FSH > 30 IU/L (if age < 45 or unclear)

**HRT (Hormone Replacement Therapy):**

**Benefits:**
- **Relieves vasomotor symptoms** (hot flashes, night sweats)
- **Prevents osteoporosis** (reduces fracture risk)
- **Improves urogenital symptoms** (vaginal dryness)
- **May improve mood, sleep, quality of life**

**Risks:**
- **Venous thromboembolism (VTE):** Increased 2-3x
- **Breast cancer:** Increased 1.3x (5 years use), 1.5x (10 years use)
- **Stroke:** Increased 1.3x
- **Coronary artery disease:** Neutral or reduced if started < 60 years

**HRT Types:**

**Estrogen:**
- **Oral:** Estradiol 1-2 mg daily, conjugated equine estrogen 0.3-0.625 mg
- **Transdermal:** Patch/gel (lower VTE risk than oral)
- **Vaginal:** Cream, tablet, ring (for local symptoms only, minimal systemic absorption)

**Progestogen (if uterus present):**
- **Micronized progesterone:** 100-200 mg daily (12-14 days/month or continuous)
- **Medroxyprogesterone acetate:** 2.5-10 mg daily
- **Norethisterone:** 0.5-1 mg daily

**Tibolone:**
- **Synthetic steroid:** 2.5 mg daily
- **Estrogenic, progestogenic, androgenic activity**
- **For:** Postmenopausal women (no uterus)

**HRT Regimens:**
- **Sequential (cyclical):** Estrogen daily + progestogen 12-14 days/month (regular bleeding)
- **Continuous:** Estrogen + progestogen daily (no bleeding after initial months)
- **Estrogen-only:** If no uterus (hysterectomy)

**Vaginal Estrogen:**
- **For:** Local urogenital symptoms (dryness, dyspareunia, urinary frequency)
- **NOT** systemic (minimal absorption, no progestogen needed)
- **Forms:** Cream, tablet, ring, pessary

**Decision-Making:**

**Benefits Outweigh Risks If:**
- **Age < 60**, within 10 years of menopause
- **Significant vasomotor symptoms** affecting quality of life
- **Premature menopause** (< 45 years, especially < 40)
- **High osteoporosis risk** (low bone density, family history)

**Risks Outweigh Benefits If:**
- **Age > 60** or > 10 years since menopause
- **History of VTE, stroke, breast cancer**
- **Active cardiovascular disease**
- **Undiagnosed vaginal bleeding**

**Alternatives to HRT:**
- **Vasomotor:** SSRIs (paroxetine), SNRIs (venlafaxine), gabapentin, clonidine
- **Vaginal:** Moisturizers, lubricants
- **Bone health:** Bisphosphonates, denosumab

**Premature Menopause (< 45):**
- **HRT recommended** (cardiovascular, bone, cognitive benefits)
- **Continue at least until average age of menopause (51)**
- **Higher dose** than standard HRT

**Monitoring:**
- **Blood pressure** (annually)
- **Breast awareness**, mammography (routine screening)
- **Cervical smear** (routine screening)
- **Review HRT need annually**

**Sources:** NICE NG23, BMJ Best Practice, RCOG 2023"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "endocrinology_reproductive",
                "focus": "menopause_hrt",
                "sources": ["NICE NG23", "BMJ Best Practice", "RCOG 2023"]
            }
        )

    def _handle_metabolic_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle metabolic syndrome queries"""
        answer = """**Metabolic Syndrome Management**

**Definition:** Cluster of conditions increasing cardiovascular disease and type 2 diabetes risk

**Diagnostic Criteria (NCEP ATP III):**
(3 or more of the following)

| Criteria | Abnormal |
|----------|----------|
| **Abdominal obesity** | Waist > 102 cm (men), > 88 cm (women) |
| **Triglycerides** | ≥ 150 mg/dL (≥ 1.7 mmol/L) |
| **HDL cholesterol** | < 40 mg/dL (men), < 50 mg/dL (women) |
| **Blood pressure** | ≥ 130/85 mmHg |
| **Fasting glucose** | ≥ 100 mg/dL (≥ 5.6 mmol/L) |

**Epidemiology:**
- **Prevalence:** 20-30% of adults
- **Increases with age**, higher in certain ethnicities
- **Strongly associated** with obesity, physical inactivity

**Complications:**
- **Type 2 diabetes:** 3-5x increased risk
- **Cardiovascular disease:** 2x increased risk
- **Non-alcoholic fatty liver disease (NAFLD)**
- **Polycystic ovary syndrome (PCOS)** (women)

**Management:**

**Lifestyle Modification (First-line):**

**Weight Loss:**
- **Target:** 5-10% weight loss (significant metabolic benefit)
- **Caloric deficit:** 500-750 kcal/day
- **Mediterranean diet:** High in vegetables, fruits, whole grains, olive oil, fish
- **Limit:** Processed foods, sugary beverages, saturated fat

**Physical Activity:**
- **Aerobic:** 150 min/week moderate-intensity (e.g., brisk walking)
- **Resistance training:** 2x/week
- **Reduce sedentary time**

**Dietary Changes:**
- **Replace saturated fat** with monounsaturated/polyunsaturated fat
- **Increase fiber** (whole grains, legumes, vegetables)
- **Limit refined carbohydrates** (white bread, sugary snacks)
- **Reduce sodium** (< 2.3 g/day, ideally < 1.5 g/day)

**Pharmacological Therapy:**

**For Individual Components:**
- **Hypertension:** ACE inhibitors, ARBs (first-line, reduce insulin resistance)
- **Hyperlipidemia:** Statins (atorvastatin 20-80 mg)
- **Hyperglycemia:** Metformin (reduce diabetes risk by 30-50%)
- **Obesity:** GLP-1 agonists (semaglutide, liraglutide), orlistat

**Metformin for Diabetes Prevention:**
- **Indications:** Pre-diabetes + BMI > 35, or age < 60, or women with prior gestational diabetes
- **Dose:** 500 mg BD to 1g BD
- **Reduces diabetes progression** by 30-50%

**Bariatric Surgery:**
- **Indications:** BMI > 40, or BMI > 35 with metabolic syndrome
- **Procedures:** Gastric bypass, sleeve gastrectomy
- **Outcomes:** 60-80% diabetes remission, significant weight loss

**Monitoring:**
- **Weight, waist circumference**
- **Blood pressure**
- **Fasting lipids, glucose**
- **HbA1c** (if pre-diabetes or diabetes)
- **Liver function tests** (NAFLD screening)

**Targets:**
- **Blood pressure:** < 130/85 mmHg
- **LDL cholesterol:** < 2.0 mmol/L
- **Triglycerides:** < 1.7 mmol/L
- **Fasting glucose:** < 5.6 mmol/L
- **Weight:** Maintain 5-10% loss

**Sources:** NICE PH46, IDF 2023, AHA/ACC 2023"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "endocrinology_metabolic",
                "focus": "metabolic_syndrome",
                "sources": ["NICE PH46", "IDF 2023", "AHA/ACC 2023"]
            }
        )

    def _handle_general_endocrinology(self, query: str, context: dict) -> DomainQueryResult:
        """General endocrinology information"""
        answer = """**Endocrinology Overview**

**Endocrine System:**
- Network of glands producing hormones
- Regulates metabolism, growth, reproduction, stress response
- **Major glands:** Pituitary, thyroid, adrenal, pancreas, parathyroid, gonads

**Common Endocrine Conditions:**

**Diabetes Mellitus:**
- Type 1 (autoimmune insulin deficiency)
- Type 2 (insulin resistance + relative deficiency)
- Treatment: Insulin, metformin, lifestyle

**Thyroid Disorders:**
- Hypothyroidism (underactive): Fatigue, weight gain, cold intolerance
- Hyperthyroidism (overactive): Weight loss, palpitations, heat intolerance
- Nodules: Most are benign, require evaluation

**Adrenal Disorders:**
- Adrenal insufficiency (Addison's): Fatigue, low blood pressure, salt craving
- Cushing's syndrome: Weight gain, easy bruising, striae

**Pituitary Disorders:**
- Prolactinoma: Amenorrhea, galactorrhea
- Acromegaly: GH excess → coarse features, enlarged hands/feet
- Hypopituitarism: Low pituitary hormones

**Reproductive Endocrinology:**
- Menopause: Cessation of menstruation, hot flashes
- PCOS: Irregular periods, hirsutism, infertility

**Calcium Disorders:**
- Hyperparathyroidism: High calcium, kidney stones
- Osteoporosis: Low bone mass, fracture risk

**Sources:** NICE guidelines, Endocrine Society, Society for Endocrinology UK"""

        return DomainQueryResult(
            domain_name="endocrinology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "endocrinology",
                "focus": "general_information",
                "sources": ["NICE", "Endocrine Society", "Society for Endocrinology"]
            }
        )

def create_endocrinology_domain():
    """Factory function to create endocrinology domain instance"""
    return EndocrinologyDomain()
