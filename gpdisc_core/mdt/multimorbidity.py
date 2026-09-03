"""Whole-patient multimorbidity reasoning — the case generalism is FOR.

Stage 4, Task 4. Glenn's canonical case: a 79-year-old with CKD, type 2
diabetes, heart failure, osteoarthritis and cognitive impairment, on eight
medications, presenting with dizziness and confusion. The review asks, in
order: which DRUG is causing this, which TREATMENT TENSION is unmanaged,
and what is the SAFEST single priority for the next appointment.
"""
from typing import Dict, List

from gpdisc_core.uk_practice.prescribing_safety import (
    monitoring_requirements,
    renal_flags,
)

TREATMENT_TENSIONS: List[tuple] = [
    ("chronic_kidney_disease", "osteoarthritis",
     "NSAIDs (oral) for OA pain accelerate CKD and raise cardiovascular risk",
     "Paracetamol + topical NSAID first; orthopaedic referral for joint-focused "
     "options; never repeat oral NSAID prescriptions without reviewing eGFR"),
    ("heart_failure", "type_2_diabetes",
     "Historic tension resolved: SGLT2 inhibitors now benefit BOTH",
     "Consider SGLT2i — improves HF outcomes and glycaemic control"),
    ("type_2_diabetes", "cognitive_impairment",
     "Complex insulin regimes outstrip the patient's ability to follow them; "
     "hypoglycaemia from missed meals presents as confusion",
     "Simplify the regimen; prefer agents with low hypoglycaemia risk; involve "
     "carers; HbA1c targets relaxed (7.5-8.5%)"),
    ("copd", "heart_failure",
     "Historic beta-blocker fear led to under-treatment of HF in COPD",
     "Cardioselective beta-blockers (bisoprolol/metoprolol) are safe and "
     "under-used — start low, monitor symptoms"),
    ("hypertension", "falls",
     "Intensive BP lowering trades stroke reduction for falls and fractures",
     "Check LYING AND STANDING BP; if postural drop, relax the target and "
     "deprescribe the antihypertensive contributing most"),
    ("atrial_fibrillation", "falls",
     "Anticoagulation prevents stroke but falls raise bleed risk",
     "Count the falls, not the fear: most fallers still net-benefit from "
     "anticoagulation — document the shared decision"),
    ("gout", "chronic_kidney_disease",
     "NSAIDs and high-dose colchicine are both hazardous in CKD",
     "Acute flare: reduced-dose colchicine or short steroid course; allopurinol "
     "start low, titrate slowly, continue during flares"),
    ("type_2_diabetes", "corticosteroids",
     "Steroid courses provoke hyperglycaemia in diabetes",
     "Plan the steroid course: temporary uptitration, alert the patient to "
     "glucose checks, arrange review mid-course"),
    ("epilepsy", "contraception",
     "Enzyme-inducing antiepileptics reduce COCP/implant effectiveness",
     "UKMEC-aware method choice (progestogen options, copper IUD); the "
     "contraceptive and epilepsy decisions must be made together"),
    ("dementia", "urinary_incontinence",
     "Anticholinergic bladder drugs worsen cognition",
     "Non-drug measures first; if a drug is needed, review cognition after "
     "initiation and prefer the lowest anticholinergic load"),
]

ACB_SCORES: Dict[str, int] = {
    "amitriptyline": 3, "oxybutynin": 3, "procyclidine": 3,
    "trihexyphenidyl": 3,
    "solifenacin": 2, "tolterodine": 2, "cyclizine": 2,
    "chlorphenamine": 2, "promethazine": 2,
    "quetiapine": 1, "sertraline": 1, "furosemide": 1, "metoclopramide": 1,
    "ranitidine": 1, "digoxin": 1, "theophylline": 1, "warfarin": 1,
}

_DIZZINESS_DRUG_CAUSES: List[str] = [
    "Postural drop from antihypertensives — CHECK LYING AND STANDING BP",
    "Hypoglycaemia from insulin/sulfonylurea, worse with small appetite",
    "Hyponatraemia: SSRI + thiazide + PPI is the classic trio",
    "Digoxin toxicity (nausea, visual change) especially with renal decline",
    "Anticholinergic load: dizziness + confusion together suggests it",
    "Bradycardia from beta-blocker or rate-limiting calcium blocker",
]

_CONFUSION_DRUG_CAUSES: List[str] = [
    "Sepsis FIRST: infection presents as confusion at this age — screen "
    "urine, chest, skin",
    "Anticholinergic burden — score the list (ACB)",
    "Opioids, benzodiazepines, z-drugs: new confusion in the elderly",
    "Steroid course: mood and sleep disturbance, rare psychosis",
    "Antiepileptic toxicity: unsteadiness that looks like 'confusion'",
]


def whole_patient_review(patient: dict) -> dict:
    """Whole-patient review for a multimorbid patient.

    The question is never "what single disease explains this?" but "which of
    this patient's drugs, diseases and their tensions explain this — and
    what is the safest priority?"
    """
    conditions = set(patient.get("conditions", []))
    medications = list(patient.get("medications", []))
    egfr = patient.get("egfr")

    # 1. Medication flags: renal thresholds and monitoring, drug by drug.
    medication_flags: List[str] = []
    for drug in medications:
        for flag in (renal_flags(drug, egfr) if egfr is not None else []):
            medication_flags.append(f"{drug}: {flag}")
        for req in monitoring_requirements(drug)[:1]:
            medication_flags.append(f"{drug}: {req}")

    # 2. Anticholinergic burden.
    acb_total = sum(ACB_SCORES.get(d.lower(), 0) for d in medications)
    acb_drugs = [d for d in medications if d.lower() in ACB_SCORES]

    # 3. Treatment tensions between coexisting conditions.
    tensions = []
    for (a, b, tension, resolution) in TREATMENT_TENSIONS:
        if a in conditions and b in conditions:
            tensions.append({"conditions": [a, b], "tension": tension,
                             "resolution": resolution})

    # 4. Drug-cause checklists for the presenting symptoms.
    symptom_causes: Dict[str, List[str]] = {}
    symptoms = [s.lower() for s in patient.get("symptoms", [])]
    if any("dizz" in s for s in symptoms):
        symptom_causes["dizziness"] = _DIZZINESS_DRUG_CAUSES
    if any("confus" in s for s in symptoms):
        symptom_causes["confusion"] = _CONFUSION_DRUG_CAUSES

    # 5. Priorities — ordered by what can harm fastest.
    priorities: List[str] = []
    if egfr is not None and egfr < 30:
        priorities.append("Renal function is the keystone: re-check eGFR and "
                          "potassium, and adjust every renally-cleared drug")
    if any("confus" in s for s in symptoms):
        priorities.append("Confusion at this age: rule out sepsis and drug "
                          "causes before assuming dementia progression")
    if any("dizz" in s for s in symptoms):
        priorities.append("Lying AND standing BP today — before any other "
                          "diagnostic reasoning about dizziness")
    if acb_total >= 3:
        priorities.append(f"Anticholinergic burden {acb_total} — propose a "
                          "deprescribing plan for: " + ", ".join(acb_drugs))
    if not priorities:
        priorities.append("Agree the patient's own priority first — the "
                          "problem they most want solved is the one to solve")

    # 6. Appointment design for multimorbidity.
    appointment_design = [
        "One problem per appointment, chosen WITH the patient",
        "Stop before you start: review every drug's indication annually",
        "Goals-of-care conversation once, not repeatedly — record what "
        "matters to this patient",
        "Share the plan in writing (large print) with patient and carer",
    ]

    return {"medication_flags": medication_flags,
            "anticholinergic_burden": acb_total,
            "anticholinergic_drugs": acb_drugs,
            "tensions": tensions,
            "symptom_causes": symptom_causes,
            "priorities": priorities,
            "appointment_design": appointment_design}
