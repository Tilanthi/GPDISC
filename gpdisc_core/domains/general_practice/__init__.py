"""
General Practice Domain Module for GPDISC
============================================

This domain specializes in primary care, family medicine, and general medical consultation.
Provides first-point-of-contact consultation, triage, and coordination of specialist care.

Key capabilities:
- General medical consultation and triage
- Symptom evaluation and differential diagnosis
- Preventive care and health screening
- Chronic disease management
- Medication reconciliation
- Specialist referral guidance
- Health promotion and disease prevention
- Multi-morbidity management

Privacy: All patient data stored locally, no external transmission.
"""

from typing import Dict, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class GeneralPracticeDomain(BaseDomainModule):
    """General Practice domain specializing in primary care and family medicine."""

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="general_practice",
            version="1.0.0",
            dependencies=[],
            description="Primary care, family medicine, general medical consultation, triage, preventive care",
            keywords=[
                "gp", "general practice", "primary care", "family doctor", "family medicine",
                "symptom", "symptoms", "triage", "medical advice", "consultation",
                "referral", "specialist", "second opinion", "diagnosis", "what should i do",
                "check-up", "health check", "screening", "preventive", "vaccination",
                "immunization", "blood test", "results", "lab results", "investigation",
                "chronic disease", "diabetes", "hypertension", "copd", "asthma", "thyroid",
                "depression", "anxiety", "mental health", "wellbeing", "lifestyle",
                "diet", "exercise", "smoking", "alcohol", "weight loss", "obesity"
            ],
            capabilities=[
                "general_consultation",
                "symptom_evaluation",
                "triage",
                "preventive_care",
                "chronic_disease_management",
                "medication_reconciliation",
                "referral_guidance",
                "health_promotion"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """Process general practice queries with primary care consultation."""
        try:
            query_lower = query.lower()

            # Urgent/emergency triage
            if any(term in query_lower for term in ["emergency", "urgent", "call 999", "call 911", "chest pain", "difficulty breathing"]):
                return self._handle_urgent_triage(query, context)

            # Symptom evaluation
            elif any(term in query_lower for term in ["symptom", "i have", "i'm experiencing", "feeling", "pain"]):
                return self._handle_symptom_evaluation(query, context)

            # Test results
            elif any(term in query_lower for term in ["blood test", "lab result", "test result", "what does this mean"]):
                return self._handle_test_results(query, context)

            # Preventive care
            elif any(term in query_lower for term in ["screening", "check-up", "preventive", "vaccine", "immunization"]):
                return self._handle_preventive_care(query, context)

            # Chronic disease
            elif any(term in query_lower for term in ["diabetes", "hypertension", "asthma", "copd", "chronic"]):
                return self._handle_chronic_disease(query, context)

            # Mental health
            elif any(term in query_lower for term in ["depression", "anxiety", "mental health", "stress", "mood"]):
                return self._handle_mental_health(query, context)

            # Medication
            elif any(term in query_lower for term in ["medication", "drug", "prescription", "interaction"]):
                return self._handle_medication(query, context)

            # Referral guidance
            elif any(term in query_lower for term in ["referral", "specialist", "see a", "should i see"]):
                return self._handle_referral(query, context)

            # General GP consultation
            else:
                return self._handle_general_gp_query(query, context)

        except Exception as e:
            return DomainQueryResult(
                domain_name="general_practice",
                answer=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )

    def _handle_urgent_triage(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle urgent/emergency triage."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**⚠️ URGENT TRIAGE - Emergency Assessment**\n\n"
                "**EMERGENCY - Call 999/911 IMMEDIATELY if**:\n"
                "- Chest pain/tightness/heaviness\n"
                "- Difficulty breathing/shortness of breath\n"
                "- Sudden weakness/slurred speech (stroke signs)\n"
                "- Severe abdominal pain\n"
                "- Loss of consciousness\n"
                "- Severe bleeding\n"
                "- Sudden severe headache\n\n"
                "**URGENT - See GP TODAY/A&E if**:\n"
                "- High fever with rigors\n"
                "- Severe headache with neck stiffness\n"
                "- Acute confusion\n"
                "- Inability to urinate\n"
                "- Severe pain limiting function\n\n"
                "**ROUTINE - Book GP appointment if**:\n"
                "- Non-urgent symptoms\n"
                "- Ongoing concerns\n"
                "- Test result review\n"
                "- Preventive care\n\n"
                "**If unsure, call NHS 111 (UK) or your GP for advice.**\n\n"
                "**This is triage guidance. For medical emergencies, call emergency services immediately.**"
            ),
            confidence=0.95,
            metadata={
                "urgency": "emergency",
                "sources": ["NHS Emergency Care", "NICE Triage Guidelines"]
            }
        )

    def _handle_symptom_evaluation(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle symptom evaluation."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Symptom Evaluation - GP Second Opinion**\n\n"
                "To provide proper evaluation, please describe:\n"
                "- **What**: Specific symptoms\n"
                "- **When**: Duration, timing, onset\n"
                "- **Severity**: Mild/moderate/severe (1-10)\n"
                "- **Aggravating/relieving factors**: What makes it better/worse\n"
                "- **Associated symptoms**: Other symptoms present\n"
                "- **Medical history**: Relevant conditions\n"
                "- **Medications**: Current treatments\n\n"
                "**Common symptom categories I can help evaluate**:\n"
                "- Pain (headache, abdominal, joint, back)\n"
                "- Respiratory (cough, dyspnea, wheeze)\n"
                "- Gastrointestinal (nausea, vomiting, diarrhea, dyspepsia)\n"
                "- Neurological (headache, dizziness, numbness)\n"
                "- Dermatological (rash, itching)\n"
                "- Constitutional (fever, fatigue, weight loss)\n\n"
                "**My approach**:\n"
                "1. Identify red flags (urgent/emergency features)\n"
                "2. Form differential diagnosis\n"
                "3. Recommend investigations if indicated\n"
                "4. Suggest management plan\n"
                "5. Advise on specialist referral if needed\n\n"
                "**Please provide detailed symptom description for evaluation.**"
            ),
            confidence=0.82,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "symptom_evaluation"
            }
        )

    def _handle_test_results(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle test result interpretation."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Test Result Interpretation - GP Second Opinion**\n\n"
                "To help interpret test results, please provide:\n"
                "- **Test name**: Which investigation\n"
                "- **Results**: Actual values and reference ranges\n"
                "- **Context**: Why tested, symptoms, medical history\n\n"
                "**Common tests I can interpret**:\n\n"
                "**Full Blood Count (FBC)**:\n"
                "- Hemoglobin (anemia, polycythemia)\n"
                "- WBC (infection, inflammation, leukemia)\n"
                "- Platelets (clotting, bleeding risk)\n\n"
                "**Biochemistry**:\n"
                "- U&Es (kidney function, electrolytes)\n"
                "- Liver function tests\n"
                "- Glucose/HbA1c (diabetes)\n"
                "- Lipids (cholesterol)\n"
                "- TSH (thyroid)\n\n"
                "**Inflammatory markers**:\n"
                "- CRP, ESR (infection, autoimmune)\n\n"
                "**Urinalysis**:\n"
                "- Infection, protein, glucose\n\n"
                "**IMPORTANT**:\n"
                "- Reference ranges vary by lab\n"
                "- Results must be interpreted in clinical context\n"
                "- Abnormal results need clinical correlation\n"
                "- Trends over time often more important than single values\n\n"
                "**Disclaimer**: Test interpretation requires clinical context. Discuss with ordering GP."
            ),
            confidence=0.83,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "test_interpretation"
            }
        )

    def _handle_preventive_care(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle preventive care queries."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Preventive Care and Health Screening - GP Consultation**\n\n"
                "**UK NHS Screening Programs**:\n\n"
                "**Adults**:\n"
                "- **Bowel cancer screening**: Age 50-74, every 2 years (FIT home kit; anyone 50+ can self-request)\n"
                "- **Breast screening**: Women 50-71 (every 3 years)\n"
                "- **Cervical screening**: Women 25-64 (every 3-5 years)\n"
                "- **AAA screening**: Men 65 (one-time)\n"
                "- **Diabetic eye screening**: Annual if diabetic\n\n"
                "**General Preventive Care**:\n\n"
                "**Vaccinations**:\n"
                "- **Influenza**: Annual, age 65+, at-risk groups\n"
                "- **Pneumococcal**: Age 65+, at-risk groups\n"
                "- **Shingles (Zoster)**: Age 70-79\n"
                "- **COVID-19**: As per current guidance\n"
                "- **Tetanus/Diphtheria/Polio**: 10-yearly if at risk\n\n"
                "**Cardiovascular Risk**:\n"
                "- **QRISK3**: Age 25-84, assesses 10-year CVD risk\n"
                "- Blood pressure check: Every 5 years (or annually if high)\n"
                "- Cholesterol check: As part of QRISK assessment\n\n"
                "**Other Health Checks**:\n"
                "- **NHS Health Check**: Age 40-74, every 5 years\n"
                "- **Dental check**: Annually\n"
                "- **Eye test**: Every 2 years\n"
                "- **Skin checks**: Annual if at-risk (skin cancer)\n\n"
                "**Cancer Awareness**:\n"
                "- Breast awareness (women)\n"
                "- Testicular awareness (men)\n"
                "- Cervical screening (women)\n"
                "- Bowel cancer screening (kit)\n"
                "- Skin lesion changes (ABCDE rule)\n\n"
                "**Lifestyle Health**:\n"
                "- **Smoking cessation**: Single most impactful\n"
                "- **Alcohol**: <14 units/week (men and women)\n"
                "- **Exercise**: 150 min moderate + 2x strength weekly\n"
                "- **Diet**: 5-a-day fruits/veg, limit processed foods\n"
                "- **Weight**: BMI 18.5-24.9 kg/m²\n"
                "- **Sleep**: 7-9 hours/night\n\n"
                "**Disclaimer**: Individualized preventive care based on risk factors. Discuss with GP."
            ),
            confidence=0.86,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "preventive_care",
                "sources": ["NHS Screening Programs", "NICE Guidelines"]
            }
        )

    def _handle_chronic_disease(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle chronic disease management."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Chronic Disease Management - GP Second Opinion**\n\n"
                "**Common Chronic Conditions Managed in Primary Care**:\n\n"
                "**Type 2 Diabetes**:\n"
                "- **Targets**: HbA1c <48 mmol/mol (individualized), BP <140/90 (NICE NG28; <150/90 if 80+)\n"
                "- **Monitoring**: Annual HbA1c, retinopathy screening, foot check, urine ACR\n"
                "- **Medications**: Metformin first-line, SGLT2/GLP-1 if high risk\n\n"
                "**Hypertension**:\n"
                "- **Targets**: <140/90 if under 80 years, <150/90 if 80 or over (NICE NG136)\n"
                "- **Monitoring**: Home BP monitoring, annual review\n"
                "- **Medications**: ACEi/ARBs, CCBs, thiazides, beta-blockers\n\n"
                "**Asthma**:\n"
                "- **Monitoring**: Annual review, asthma control test (ACT)\n"
                "- **Medications**: SABA (reliever), ICS/LABA (preventer)\n"
                "- **Action plan**: Written personalized plan\n\n"
                "**COPD**:\n"
                "- **Monitoring**: Annual review, spirometry, FEV1\n"
                "- **Medications**: LAMA/LABA inhalers, consider roflumilast\n"
                "- **Vaccinations**: Influenza, pneumococcal, COVID\n\n"
                "**Hypothyroidism**:\n"
                "- **Monitoring**: TSH every 3-6 months initially, then annually\n"
                "- **Target**: TSH 0.4-4.0 mU/L\n"
                "- **Medication**: Levothyroxine titrated to TSH\n\n"
                "**Depression/Anxiety**:\n"
                "- **Screening**: PHQ-9, GAD-7\n"
                "- **Treatment**: SSRI first-line, consider CBT\n"
                "- **Monitoring**: Symptom review, medication side effects\n\n"
                "**Chronic Kidney Disease (CKD)**:\n"
                "- **Staging**: eGFR and ACR categories\n"
                "- **Monitoring**: Annual eGFR, ACR, BP, lipids\n"
                "- **Targets**: BP <130/80, SGLT2i if proteinuric\n\n"
                "**QOF (Quality and Outcomes Framework)**:\n"
                "- UK primary care quality indicators for chronic disease management\n"
                "- Ensures systematic, evidence-based care\n\n"
                "**Disclaimer**: Individualized management essential. Regular review with GP."
            ),
            confidence=0.85,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "chronic_disease",
                "sources": ["NICE Guidelines", "QOF", "BNF"]
            }
        )

    def _handle_mental_health(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle mental health queries."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Mental Health Consultation - GP Second Opinion**\n\n"
                "**CRISIS SUPPORT**:\n"
                "If you're in crisis, having thoughts of self-harm, or need immediate support:\n"
                "- **UK**: Call 111, Samaritans 116 123, Shout Crisis Text Line (text 85258)\n"
                "- **Emergency**: Call 999 if immediate danger to life\n\n"
                "**Common Mental Health Conditions in Primary Care**:\n\n"
                "**Depression**:\n"
                "- **Screening**: PHQ-9 questionnaire\n"
                "- **Diagnosis**: DSM-5/ICD-11 criteria (5+ symptoms for 2+ weeks)\n"
                "- **Treatment**:\n"
                "  - Mild: Self-help, CBT, watchful waiting\n"
                "  - Moderate: CBT, consider SSRI\n"
                "  - Severe: SSRI, consider psychiatry referral\n"
                "- **Medications**: SSRIs first-line (fluoxetine, citalopram, sertraline)\n"
                "- **Monitoring**: PHQ-9 review every 2-4 weeks initially\n\n"
                "**Generalized Anxiety Disorder (GAD)**:\n"
                "- **Screening**: GAD-7 questionnaire\n"
                "- **Treatment**: CBT, SSRI/SNRI first-line\n"
                "- **Medications**: SSRIs, SNRIs (venlafaxine, duloxetine)\n\n"
                "**Insomnia**:\n"
                "- **First-line**: Sleep hygiene, CBT-I\n"
                "- **Medications**: Short-term only (z-drugs, promethazine)\n\n"
                "**Other mental health presentations**:\n"
                "- **Bipolar disorder**: Psychiatry referral, mood stabilizers\n"
                "- **Psychosis**: Urgent psychiatry referral, antipsychotics\n"
                "- **Eating disorders**: Specialist referral\n"
                "- **PTSD**: Trauma-focused CBT, EMDR\n\n"
                "**Non-pharmacological Interventions**:\n"
                "- **CBT (Cognitive Behavioral Therapy)**: First-line for depression/anxiety\n"
                "- **Counselling**: For mild-moderate depression\n"
                "- **Mindfulness**: For anxiety, depression relapse prevention\n"
                "- **Exercise**: Evidence-based for depression (150 min/week)\n\n"
                "**Red Flags**:\n"
                "- Suicidal ideation (urgent assessment needed)\n"
                "- Psychotic symptoms (urgent referral)\n"
                "- Bipolar features (psychiatry referral)\n"
                "- Postpartum depression (urgent referral)\n\n"
                "**Disclaimer**: Mental health requires comprehensive assessment. Urgent cases need emergency care."
            ),
            confidence=0.85,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "mental_health",
                "sources": ["NICE Guidelines", "DSM-5", "ICD-11"]
            }
        )

    def _handle_medication(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle medication queries."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Medication Consultation - GP Second Opinion**\n\n"
                "**Common Medication Classes in Primary Care**:\n\n"
                "**Analgesics**:\n"
                "- **Paracetamol**: First-line, safer than NSAIDs\n"
                "- **NSAIDs** (ibuprofen, naproxen): Risk of GI bleed, renal impairment, hypertension\n"
                "- **Opioids** (codeine, tramadol): Last resort, risk of dependence\n\n"
                "**Cardiovascular**:\n"
                "- **Antihypertensives**: See cardiology domain\n"
                "- **Statins**: Atorvastatin 20-80mg (monitor LFTs)\n"
                "- **Antiplatelets**: Aspirin 75mg (secondary prevention)\n"
                "- **Anticoagulants**: DOACs for AF, warfarin (valve)\n\n"
                "**Respiratory**:\n"
                "- **Inhalers**: SABA (salbutamol), ICS (beclomethasone), LABA, LAMA\n"
                "- **Technique**: spacer use, inhaler technique check\n\n"
                "**Gastrointestinal**:\n"
                "- **PPIs** (omeprazole, lansoprazole): Short-term for PUD/GORD, review long-term use\n"
                "- **Laxatives**: Macrogol, lactulose (maintain fluid intake)\n\n"
                "**Antibiotics**:\n"
                "- **Delayed prescribing**: For self-limiting infections\n"
                "- **Antibiotic stewardship**: Only when indicated\n"
                "- **Common choices**: Amoxicillin, doxycycline, clarithromycin, nitrofurantoin\n\n"
                "**Psychotropics**:\n"
                "- **SSRIs**: First-line depression/anxiety (takes 4-6 weeks for effect)\n"
                "- **Benzodiazepines**: Avoid long-term (dependence risk)\n"
                "- **Z-drugs**: Short-term insomnia only\n\n"
                "**Medication Safety**:\n"
                "- **Interactions**: Check for drug interactions (BNF interactions checker)\n"
                "- **Contraindications**: Allergies, renal impairment, pregnancy\n"
                "- **Side effects**: Discuss with patient, monitor\n"
                "- **Deprescribing**: Review long-term medications regularly\n\n"
                "**Polypharmacy**:\n"
                "- **Definition**: ≥5 regular medications\n"
                "- **Risks**: Interactions, falls, confusion, adverse effects\n"
                "- **Review**: Regular medication review, deprescribe if possible\n\n"
                "**Disclaimer**: This is general information. Always consult prescribing clinician/pharmacist."
            ),
            confidence=0.84,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "medication",
                "sources": ["BNF", "NICE Guidelines"]
            }
        )

    def _handle_referral(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle referral guidance."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**Specialist Referral Guidance - GP Second Opinion**\n\n"
                "**When to Refer to Specialists**:\n\n"
                "**Urgent Referral (2-week wait)**:\n"
                "- **Suspected cancer**: Red flag symptoms\n"
                "- **Cardiology**: Unstable angina, heart failure\n"
                "- **Neurology**: First seizure, rapidly progressive neurological\n\n"
                "**Routine Referral**:\n\n"
                "- **Cardiology**: Echocardiogram, stress test, complex arrhythmia\n"
                "- **Respiratory**: COPD, complex asthma, bronchoscopy\n"
                "- **Gastroenterology**: Endoscopy, IBD, liver disease\n"
                "- **Rheumatology**: Inflammatory arthritis, connective tissue disease\n"
                "- **Orthopedics**: Joint replacement, fracture management\n"
                "- **Dermatology**: Skin lesion biopsy, complex dermatology\n"
                "- **Gynecology**: Menorrhagia, pelvic pain, post-menopausal bleeding\n"
                "- **Urology**: Hematuria, prostate assessment, recurrent UTI\n"
                "- **Neurology**: Seizure disorder, neuropathy, movement disorder\n"
                "- **Psychiatry**: Severe depression, bipolar, psychosis\n"
                "- **Ophthalmology**: Cataract, glaucoma, retinal pathology\n"
                "- **ENT**: Sinus surgery, tonsillectomy, hearing loss\n\n"
                "**Referral Process** (UK NHS)**:\n"
                "- **Choose and Book**: Patient can choose hospital/consultant\n"
                "- **e-RS**: Electronic referral service\n"
                "- **Letters**: Include reason, history, investigations, medications\n"
                "- **Waiting times**: Vary, 18-week target for routine\n\n"
                "**Private Referral**:\n"
                "- If patient requests private care\n"
                "- Provide referral letter\n"
                "- Patient pays or uses private insurance\n\n"
                "**Before Referring**:\n"
                "- Ensure appropriate investigations done\n"
                "- Optimize primary care management\n"
                "- Discuss patient preference\n"
                "- Provide clear referral question\n\n"
                "**Disclaimer**: Referral decisions individualized. Discuss with GP."
            ),
            confidence=0.85,
            metadata={
                "specialty": "general_practice",
                "subspecialty": "referral_guidance",
                "sources": ["NICE Referral Guidelines", "NHS Referral Criteria"]
            }
        )

    def _handle_general_gp_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general GP queries."""
        return DomainQueryResult(
            domain_name="general_practice",
            answer=(
                "**General Practice Consultation - Second Opinion**\n\n"
                "I provide primary care consultation on:\n\n"
                "**General Consultation**:\n"
                "- Symptom evaluation and triage\n"
                "- Differential diagnosis\n"
                "- Investigation planning\n"
                "- Management plan recommendations\n\n"
                "**Preventive Care**:\n"
                "- Health screening\n"
                "- Vaccinations\n"
                "- Cardiovascular risk assessment\n"
                "- Cancer awareness\n\n"
                "**Chronic Disease Management**:\n"
                "- Diabetes, hypertension, asthma, COPD\n"
                "- Hypothyroidism, mental health\n"
                "- Chronic kidney disease\n\n"
                "**Medication**:\n"
                "- Medication review\n"
                "- Side effect management\n"
                "- Drug interactions\n"
                "- Deprescribing\n\n"
                "**Coordination of Care**:\n"
                "- Specialist referral guidance\n"
                "- Test result interpretation\n"
                "- Care coordination\n\n"
                "**Common Presentations**:\n"
                "- Infections (UTI, respiratory, skin)\n"
                "- Pain (headache, back, joint, abdominal)\n"
                "- Dermatological (rash, acne, lesion)\n"
                "- Gastrointestinal (reflux, diarrhea, constipation)\n"
                "- Respiratory (cough, dyspnea, wheeze)\n"
                "- Constitutional (fever, fatigue, weight loss)\n\n"
                "**Please provide**: Age, gender, symptoms, duration, medical history, "
                "medications, specific questions for second opinion.\n\n"
                "**Privacy**: All data stored locally.\n"
                "**Medical Disclaimer**: This is second opinion, not emergency care. "
                "For emergencies, call 999/911."
            ),
            confidence=0.85,
            metadata={
                "specialty": "general_practice",
                "sources": ["NICE Guidelines", "BNF", "Clinical Knowledge Summaries"]
            }
        )


def create_general_practice_domain():
    """Factory function for creating GP domain instances."""
    return GeneralPracticeDomain()
