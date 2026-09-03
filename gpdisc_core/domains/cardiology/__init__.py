"""
Cardiology Domain Module for GPDISC
======================================

This domain specializes in cardiovascular medicine, heart disease, and cardiac diagnostics.
Provides consultation on ECG interpretation, chest pain evaluation, blood pressure management,
and general cardiac consultation.

Key capabilities:
- ECG/EKG interpretation
- Chest pain evaluation and cardiac risk assessment
- Blood pressure and hypertension management
- Heart failure management
- Arrhythmia evaluation (atrial fibrillation, etc.)
- Cardiac imaging interpretation (echocardiogram, stress test, angiogram)
- Cardiovascular risk assessment
- Medication management for cardiac conditions

Privacy: All patient data stored locally, no external transmission.
"""

from typing import Dict, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class CardiologyDomain(BaseDomainModule):
    """
    Cardiology domain specializing in cardiovascular medicine and heart disorders.

    This domain provides medical consultation on cardiac conditions, ECG interpretation,
    chest pain evaluation, blood pressure management, and cardiovascular risk assessment.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="cardiology",
            version="1.0.0",
            dependencies=[],
            description="Cardiovascular medicine, heart disease, cardiac diagnostics, ECG interpretation",
            keywords=[
                "heart", "cardiac", "cardiovascular", "chest pain", "chest tightness",
                "palpitations", "blood pressure", "hypertension", "high blood pressure", "cholesterol",
                "ecg", "ekg", "electrocardiogram", "echocardiogram", "echo", "stress test",
                "angiogram", "cardiac catheterization", "stent", "bypass", "cabg",
                "arrhythmia", "atrial fibrillation", "afib", "heart failure", "myocardial",
                "infarction", "heart attack", "mi", "cardiac arrest", "cardiomyopathy",
                "valve", "aortic stenosis", "mitral valve", "tricuspid", "pulmonic",
                "pericarditis", "myocarditis", "endocarditis", "pacemaker", "icd",
                "cardioversion", "defibrillation", "cardiac enzymes", "troponin", "ck-mb",
                "bnp", "nt-probnp", "cardiac biomarkers", "lipid panel", "ldl", "hdl",
                "triglycerides", "statin", "aspirin", "beta blocker", "ace inhibitor", "arb",
                "calcium channel blocker", "diuretic", "anticoagulant", "warfarin", "doac",
                "cardiac risk", "framingham", "ascvd", "qrisk", "cardiovascular disease",
                "coronary artery disease", "cad", "atherosclerosis", "ischemic heart disease"
            ],
            capabilities=[
                "cardiovascular_diagnosis",
                "ecg_interpretation",
                "chest_pain_evaluation",
                "risk_assessment",
                "cardiac_imaging",
                "heart_failure_management",
                "arrhythmia_management",
                "hypertension_management",
                "lipid_management",
                "cardiac_medication_management"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """
        Process cardiology-related queries with specialized consultation.

        This method provides medical consultation on cardiac conditions, ECG interpretation,
        chest pain evaluation, and cardiovascular risk assessment.

        Args:
            query: Patient query or medical question
            context: Optional patient context (age, gender, medical history, medications)

        Returns:
            DomainQueryResult with cardiology consultation and recommendations
        """
        try:
            query_lower = query.lower()

            # ECG interpretation
            if any(term in query_lower for term in ["ecg", "ekg", "electrocardiogram", " rhythm", "wave", "interval"]):
                return self._handle_ecg_query(query, context)

            # Chest pain evaluation
            elif any(term in query_lower for term in ["chest pain", "chest tightness", "chest pressure", "chest discomfort"]):
                return self._handle_chest_pain_query(query, context)

            # Blood pressure / hypertension
            elif any(term in query_lower for term in ["blood pressure", "hypertension", "high bp", "bp"]):
                return self._handle_bp_query(query, context)

            # Heart failure
            elif any(term in query_lower for term in ["heart failure", "fluid retention", "swelling legs", "shortness of breath"]):
                return self._handle_heart_failure_query(query, context)

            # Arrhythmia
            elif any(term in query_lower for term in ["arrhythmia", "palpitation", "irregular heartbeat", "atrial fibrillation", "afib"]):
                return self._handle_arrhythmia_query(query, context)

            # Cardiac risk assessment
            elif any(term in query_lower for term in ["risk", "cardiovascular risk", "heart risk", "ascvd"]):
                return self._handle_risk_assessment_query(query, context)

            # Lipid / cholesterol management
            elif any(term in query_lower for term in ["cholesterol", "lipid", "ldl", "hdl", "triglyceride", "statin"]):
                return self._handle_lipid_query(query, context)

            # Medication-related
            elif any(term in query_lower for term in ["medication", "drug", "prescription", "beta blocker", "ace inhibitor"]):
                return self._handle_medication_query(query, context)

            # General cardiology consultation
            else:
                return self._handle_general_cardiology_query(query, context)

        except Exception as e:
            return DomainQueryResult(
                domain_name="cardiology",
                answer=f"I encountered an error processing your cardiology query: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e), "domain": "cardiology"}
            )

    def _handle_ecg_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle ECG interpretation queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**ECG Interpretation - Second Opinion Consultation**\n\n"
                "To provide an accurate ECG interpretation, I would need to see the actual ECG tracing. "
                "Key elements I evaluate include:\n\n"
                "1. **Rate and Rhythm**: Sinus rhythm? Rate normal (60-100 bpm)?\n"
                "2. **Axis**: Normal axis deviation?\n"
                "3. **Intervals**: PR, QRS, QT durations normal?\n"
                "4. **Waveforms**: P waves, QRS complexes, T waves normal?\n"
                "5. **Segments**: ST elevation/depression present?\n\n"
                "Common abnormalities I assess:\n"
                "- Atrial fibrillation (irregularly irregular)\n"
                "- Atrial flutter (sawtooth waves)\n"
                "- Myocardial infarction (ST elevation, Q waves)\n"
                "- Heart block (PR prolongation, dropped beats)\n"
                "- Ventricular hypertrophy (voltage criteria)\n"
                "- Arrhythmias\n\n"
                "**Please provide the ECG image or describe specific findings for detailed consultation.**\n\n"
                "**Guidelines**: AHA/ACC, ESC clinical practice guidelines for ECG interpretation.\n"
                "**Confidence**: This is general guidance. For definitive diagnosis, consult a cardiologist."
            ),
            confidence=0.85,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "ecg_interpretation",
                "sources": ["AHA/ACC Guidelines", "ESC Guidelines", "Standard ECG textbooks"]
            }
        )

    def _handle_chest_pain_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle chest pain evaluation queries."""
        age = context.get("age", "not specified") if context else "not specified"
        gender = context.get("gender", "not specified") if context else "not specified"

        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                f"**Chest Pain Evaluation - Second Opinion Consultation**\n\n"
                f"**Patient Context**: Age {age}, {gender}\n\n"
                "**CRITICAL WARNING**: Chest pain can be life-threatening. If this is acute/severe, "
                "**seek emergency care immediately** (call 999/911).\n\n"
                "**My Differential Diagnosis Approach**:\n\n"
                "1. **Acute Coronary Syndrome (ACS)**:\n"
                "   - Typical: Crushing substernal pain, radiation to arm/jaw, diaphoresis, nausea\n"
                "   - Risk factors: Age, hypertension, diabetes, smoking, family history\n"
                "   - Workup: ECG, cardiac enzymes (troponin), urgent cardiology review\n\n"
                "2. **Pulmonary Embolism**:\n"
                "   - Pleuritic pain, dyspnea, tachycardia, risk factors (DVT, recent surgery)\n"
                "   - Workup: CT pulmonary angiogram, D-dimer\n\n"
                "3. **Aortic Dissection**:\n"
                "   - Tearing/radating pain to back, pulse deficits, blood pressure discrepancy\n"
                "   - Workup: CT angiogram, urgent surgical consultation\n\n"
                "4. **Other Cardiac**: Pericarditis, myocarditis\n\n"
                "5. **Non-Cardiac**: GERD, musculoskeletal, anxiety, pneumonia\n\n"
                "**My Recommendation**: If you have chest pain, especially with risk factors, "
                "urgent medical evaluation is warranted. This includes ECG, cardiac biomarkers, "
                "and clinical assessment by emergency medicine/cardiology.\n\n"
                "**Disclaimer**: This is a second opinion, not a replacement for emergency care."
            ),
            confidence=0.90,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "chest_pain_evaluation",
                "urgency": "high",
                "sources": ["AHA/ACC Guidelines for Chest Pain", "NICE Guidelines"]
            }
        )

    def _handle_bp_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle blood pressure/hypertension queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Blood Pressure Management - Second Opinion Consultation**\n\n"
                "**Normal BP**: <120/80 mmHg\n"
                "**Elevated**: Systolic 120-129 AND Diastolic <80\n"
                "**Hypertension Stage 1**: Systolic 130-139 OR Diastolic 80-89\n"
                "**Hypertension Stage 2**: Systolic ≥140 OR Diastolic ≥90\n\n"
                "**My Management Approach**:\n\n"
                "1. **Lifestyle Modifications (First-line)**:\n"
                "   - DASH diet (low sodium, high fruits/vegetables)\n"
                "   - Regular aerobic exercise (150 min/week moderate)\n"
                "   - Weight loss if overweight\n"
                "   - Limit alcohol, reduce stress\n"
                "   - <1500 mg sodium/day\n\n"
                "2. **Medication Indications** (NICE/ESC guidelines):\n"
                "   - Stage 2 hypertension (≥140/90)\n"
                "   - Stage 1 with CVD, diabetes, CKD, or 10-year ASCVD risk ≥10%\n"
                "   - Failed lifestyle modification\n\n"
                "3. **First-line Medications**:\n"
                "   - **ACE inhibitors/ARBs**: Patients <55, diabetic, CKD\n"
                "   - **Calcium channel blockers**: Patients >55, Afro-Caribbean\n"
                "   - **Thiazide diuretics**: Add-on therapy\n"
                "   - **Beta-blockers**: If post-MI, heart failure, arrhythmia\n\n"
                "4. **Target BP**: Generally <130/80 if tolerated\n\n"
                "**Monitoring**: Home BP monitoring recommended. Log readings.\n\n"
                "**Disclaimer**: Individualized treatment based on comorbidities. Consult your GP/cardiologist."
            ),
            confidence=0.88,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "hypertension_management",
                "sources": ["NICE NG136 Hypertension", "ESC/ESH Guidelines", "JNC 8"]
            }
        )

    def _handle_heart_failure_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle heart failure queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Heart Failure Management - Second Opinion Consultation**\n\n"
                "**Heart Failure** is the inability of the heart to pump sufficient blood to meet metabolic needs.\n\n"
                "**Classification**:\n"
                "- **HFrEF** (Reduced EF): LVEF ≤40%\n"
                "- **HFpEF** (Preserved EF): LVEF ≥50% with diastolic dysfunction\n"
                "- **HFmrEF** (Mid-range): LVEF 41-49%\n\n"
                "**Typical Symptoms**:\n"
                "- Dyspnea (exertional, orthopnea, PND)\n"
                "- Fluid retention (peripheral edema, ascites)\n"
                "- Fatigue, reduced exercise tolerance\n"
                "- Nocturnal cough, weight gain\n\n"
                "**Guideline-Directed Medical Therapy (GDMT) for HFrEF**:\n"
                "1. **ACE inhibitors/ARBs/ARNIs** (e.g., ramipril, losartan, sacubitril/valsartan)\n"
                "2. **Beta-blockers** (bisoprolol, carvedilol, metoprolol succinate)\n"
                "3. **Mineralocorticoid Receptor Antagonists** (spironolactone, eplerenone)\n"
                "4. **SGLT2 inhibitors** (dapagliflozin, empagliflozin) - newer recommendation\n\n"
                "**Device Therapy** (if indicated):\n"
                "- ICD (primary/secondary prevention)\n"
                "- CRT (if LBBB, QRS ≥150ms)\n\n"
                "**Monitoring**: Daily weights, regular review, medication titration.\n\n"
                "**Disclaimer**: Individualized management essential. Consult cardiologist."
            ),
            confidence=0.87,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "heart_failure",
                "sources": ["ESC Guidelines", "AHA/ACC/HFSA Guidelines"]
            }
        )

    def _handle_arrhythmia_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle arrhythmia queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Arrhythmia Consultation - Second Opinion**\n\n"
                "**Atrial Fibrillation (AF)** is the most common sustained arrhythmia.\n\n"
                "**Stroke Risk Assessment (CHA₂DS₂-VASc Score)**:\n"
                "- C (Congestive HF): 1 point\n"
                "- H (Hypertension): 1 point\n"
                "- A (Age ≥75): 2 points\n"
                "- D (Diabetes): 1 point\n"
                "- S (Stroke/TIA): 2 points\n"
                "- V (Vascular disease): 1 point\n"
                "- A (Age 65-74): 1 point\n"
                "- Sc (Sex category Female): 1 point\n\n"
                "**Score 0 (men) or 1 (women)**: No anticoagulation needed\n"
                "**Score ≥2 (men) or ≥3 (women)**: Consider anticoagulation\n\n"
                "**Management Options**:\n\n"
                "1. **Rate Control** (beta-blockers, diltiazem, digoxin)\n"
                "2. **Rhythm Control** (amiodarone, flecainide, electrical cardioversion)\n"
                "3. **Anticoagulation** (DOACs preferred over warfarin unless mechanical valve)\n"
                "4. **Left Atrial Appendage Occlusion** (if anticoagulation contraindicated)\n\n"
                "**Bleeding Risk (HAS-BLED)**: Assess before starting anticoagulation.\n\n"
                "**Other Arrhythmias**:\n"
                "- SVT: Vagal maneuvers, adenosine\n"
                "- VT: Amiodarone, consider ICD\n"
                "- Heart Block: Pacemaker evaluation\n\n"
                "**Disclaimer**: ECG confirmation and cardiology review essential."
            ),
            confidence=0.86,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "arrhythmia",
                "sources": ["ESC AF Guidelines", "AHA/ACC/HRS Guidelines"]
            }
        )

    def _handle_risk_assessment_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle cardiovascular risk assessment queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Cardiovascular Risk Assessment - Second Opinion**\n\n"
                "**Primary Prevention Tools**:\n\n"
                "1. **ASCVD Risk Calculator** (AHA/ACC):\n"
                "   - Estimates 10-year risk of MI, stroke, death\n"
                "   - Factors: Age, sex, race, BP, cholesterol, smoking, diabetes, treatment\n"
                "   - **≥7.5%**: Consider statin therapy\n"
                "   - **≥20%**: High risk, aggressive management\n\n"
                "2. **QRISK3** (UK-specific):\n"
                "   - 10-year CVD risk including CKD, atrial fibrillation, lupus, etc.\n"
                "   - **≥10%**: Offer statin\n\n"
                "3. **Framingham Risk Score**:\n"
                "   - Traditional risk factor-based\n\n"
                "**Risk Factor Optimization**:\n"
                "- **Smoking cessation**: Single most impactful\n"
                "- **BP control**: Target <130/80 if tolerated\n"
                "- **Lipid management**: LDL targets based on risk\n"
                "- **Diabetes control**: HbA1c <7% if achievable\n"
                "- **Weight**: BMI 18.5-24.9 kg/m²\n"
                "- **Exercise**: 150 min/week moderate intensity\n"
                "- **Diet**: Mediterranean, DASH, plant-predominant\n\n"
                "**Statin Therapy Indications**:\n"
                "- ASCVD risk ≥7.5% (age 40-75)\n"
                "- Diabetes mellitus (age 40-75)\n"
                "- LDL ≥190 mg/dL\n"
                "- Known ASCVD (secondary prevention)\n\n"
                "**Disclaimer**: Risk assessment is population-based. Individual factors matter."
            ),
            confidence=0.85,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "risk_assessment",
                "sources": ["AHA/ACC Guidelines", "NICE NG181", "ESC Guidelines"]
            }
        )

    def _handle_lipid_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle lipid/cholesterol queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Lipid Management - Second Opinion Consultation**\n\n"
                "**Lipid Panel Interpretation**:\n\n"
                "**LDL Cholesterol** (Primary target):\n"
                "- Optimal: <100 mg/dL (<2.6 mmol/L)\n"
                "- Near optimal: 100-129 (2.6-3.3 mmol/L)\n"
                "- Borderline high: 130-159 (3.4-4.1 mmol/L)\n"
                "- High: 160-189 (4.1-4.9 mmol/L)\n"
                "- Very high: ≥190 (≥4.9 mmol/L)\n\n"
                "**HDL Cholesterol**:\n"
                "- Low (risk factor): <40 mg/dL (<1.0 mmol/L) men, <50 (1.3 mmol/L) women\n"
                "- High (protective): ≥60 mg/dL (≥1.6 mmol/L)\n\n"
                "**Triglycerides**:\n"
                "- Normal: <150 mg/dL (<1.7 mmol/L)\n"
                "- Borderline high: 150-199\n"
                "- High: 200-499\n"
                "- Very high: ≥500 mg/dL (risk of pancreatitis)\n\n"
                "**LDL Targets by Risk Category**:\n"
                "- **Very high risk** (ASCVD + risk factors): <55 mg/dL (<1.4 mmol/L)\n"
                "- **High risk** (ASCVD, diabetes, high risk score): <70 mg/dL (<1.8 mmol/L)\n"
                "- **Moderate risk**: <100 mg/dL (<2.6 mmol/L)\n"
                "- **Low risk**: <116 mg/dL (<3.0 mmol/L)\n\n"
                "**First-line Therapy**: Statins (atorvastatin, rosuvastatin)\n\n"
                "**Second-line / Adjuncts**:\n"
                "- Ezetimibe (add-on to statin)\n"
                "- PCSK9 inhibitors (if LDL still elevated)\n"
                "- Bempedoic acid, inclisiran (newer agents)\n\n"
                "**Lifestyle Impact**:\n"
                "- Saturated fat <7% calories\n"
                "- Eliminate trans fats\n"
                "- Soluble fiber (10-25 g/day)\n"
                "- Plant sterols/stanols (2 g/day)\n\n"
                "**Disclaimer**: Targets individualized. Regular monitoring essential."
            ),
            confidence=0.86,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "lipid_management",
                "sources": ["ESC/EAS Guidelines", "AHA/ACC Guidelines"]
            }
        )

    def _handle_medication_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle cardiac medication queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Cardiac Medication Consultation - Second Opinion**\n\n"
                "**Common Cardiac Medication Classes**:\n\n"
                "1. **Antiplatelets**:\n"
                "   - Aspirin: 75mg daily (secondary prevention)\n"
                "   - Clopidogrel, ticagrelor, prasugrel: Post-ACS/stent\n\n"
                "2. **Anticoagulants**:\n"
                "   - **DOACs** (apixaban, rivaroxaban, dabigatran, edoxaban): AF, VTE\n"
                "   - Warfarin: Mechanical valves, certain conditions\n\n"
                "3. **Statin Therapy**:\n"
                "   - Atorvastatin, rosuvastatin: High-intensity preferred\n"
                "   - Monitor LFTs at baseline, if symptomatic\n\n"
                "4. **Beta-Blockers**:\n"
                "   - Bisoprolol, carvedilol, metoprolol: HF, post-MI, arrhythmia, HTN\n"
                "   - Contraindications: Asthma (caution), bradycardia, heart block\n\n"
                "5. **ACE Inhibitors/ARBs**:\n"
                "   - Ramipril, lisinopril (ACEs); losartan, valsartan (ARBs)\n"
                "   - Indications: HF, post-MI, diabetes, CKD, HTN\n"
                "   - ARNI (sacubitril/valsartan): HFrEF\n\n"
                "6. **Calcium Channel Blockers**:\n"
                "   - Amlodipine, felodipine: HTN, angina\n"
                "   - Diltiazem, verapamil: Rate control in AF\n\n"
                "7. **Diuretics**:\n"
                "   - Furosemide, bumetanide: Loop diuretics (HF)\n"
                "   - Thiazides: HTN\n\n"
                "**Important**:\n"
                "- Check for drug interactions\n"
                "- Monitor renal function, electrolytes\n"
                "- Be aware of contraindications\n"
                "- Regular medication review\n\n"
                "**Disclaimer**: This is general information. Always consult prescribing doctor/pharmacist."
            ),
            confidence=0.84,
            metadata={
                "specialty": "cardiology",
                "subspecialty": "cardiac_medication",
                "sources": ["BNF", "ESC Guidelines", "Clinical Pharmacology"]
            }
        )

    def _handle_general_cardiology_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general cardiology queries."""
        return DomainQueryResult(
            domain_name="cardiology",
            answer=(
                "**Cardiology Consultation - Second Opinion**\n\n"
                "I specialize in cardiovascular medicine and can provide consultation on:\n\n"
                "**Conditions**:\n"
                "- Coronary artery disease, angina, heart attack\n"
                "- Heart failure (reduced and preserved EF)\n"
                "- Arrhythmias (AF, SVT, VT, palpitations)\n"
                "- Valvular heart disease\n"
                "- Hypertension\n"
                "- Lipid disorders\n"
                "- Cardiac risk assessment\n\n"
                "**Diagnostic Tests**:\n"
                "- ECG/EKG interpretation\n"
                "- Echocardiogram findings\n"
                "- Stress test results\n"
                "- Cardiac biomarkers\n"
                "- Lipid panels\n\n"
                "**Medications**:\n"
                "- Antiplatelets and anticoagulants\n"
                "- Statins and lipid-lowering therapy\n"
                "- Blood pressure medications\n"
                "- Heart failure medications\n"
                "- Antiarrhythmics\n\n"
                "**Prevention**:\n"
                "- Cardiovascular risk assessment\n"
                "- Lifestyle modifications\n"
                "- Primary prevention strategies\n\n"
                "**Please provide specific details**: symptoms, test results, medications, "
                "questions you'd like a second opinion on.\n\n"
                "**Privacy Note**: All information is stored locally and not transmitted externally.\n"
                "**Medical Disclaimer**: This is a second opinion consultation, not a replacement "
                "for in-person medical care. For emergencies, seek immediate care."
            ),
            confidence=0.85,
            metadata={
                "specialty": "cardiology",
                "sources": ["AHA/ACC Guidelines", "ESC Guidelines", "NICE Guidelines"]
            }
        )


def create_cardiology_domain():
    """
    Factory function for creating cardiology domain instances.

    Returns:
        CardiologyDomain: Configured cardiology domain module
    """
    return CardiologyDomain()
