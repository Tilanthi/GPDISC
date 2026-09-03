"""NHS screening programmes (England schedule as at 2026) — preventive
medicine Stage 2. Local data only.
"""
from dataclasses import dataclass
from typing import List

from .schedules import VACCINES_UK, vaccine_due
from .cvd_prevention import cvd_prevention_advice


@dataclass
class ScreeningEntry:
    programme: str
    cohort: str
    interval: str
    test: str
    abnormal_pathway: str


SCREENING_UK = [
    ScreeningEntry("Bowel cancer screening (FIT)", "54-74 (expanding to 50), men and women",
        "Every 2 years", "Faecal immunochemical test at home",
        "Positive FIT → colonoscopy via SSP"),
    ScreeningEntry("Breast cancer screening", "Women 50-70 (self-request 71+)",
        "Every 3 years", "Mammography", "Recall/assessment clinic"),
    ScreeningEntry("Cervical screening (HPV)",
        "Women 25-49: 3-yearly; 50-64: 5-yearly", "3 or 5 years",
        "HPV primary with cytology triage (self-sampling rolling out)",
        "HPV+ → colposcopy"),
    ScreeningEntry("Abdominal aortic aneurysm", "Men 65 (one-off; self-request older)",
        "Once at 65", "Ultrasound aorta",
        ">=3cm → surveillance; >=5.5cm → vascular referral"),
    ScreeningEntry("Diabetic eye screening", "Everyone with diabetes 12+", "Annual",
        "Retinal photography", "R1M0+ → grading/refer ophthalmology"),
    ScreeningEntry("NHS Health Check", "Adults 40-74 without existing CVD/dementia",
        "Every 5 years", "Risk assessment: BP, lipids, BMI, HbA1c, QRISK",
        "QRISK >=10% → statin discussion"),
    ScreeningEntry("Antenatal screening", "Pregnant women",
        "Booking + specific points",
        "HIV/syphilis/hepatitis B/rubella, sickle cell & thalassaemia, "
        "Down/Edwards/Patau, fetal anomaly",
        "Positive → specialist counselling"),
    ScreeningEntry("Newborn screening", "All newborns", "Day 5",
        "Blood spot: 9 conditions incl. PKU, CF, sickle cell, MCADD; "
        "hearing; NIPE examination",
        "Positive → confirmatory testing"),
]


def screening_due(entry: ScreeningEntry, patient: dict) -> bool:
    age = patient.get("age_years")
    sex = patient.get("sex")
    p = patient
    if entry.programme.startswith("Bowel"):
        return age is not None and 54 <= age <= 74
    if entry.programme.startswith("Breast"):
        return sex == "f" and age is not None and 50 <= age <= 70
    if entry.programme.startswith("Cervical"):
        return sex == "f" and age is not None and 25 <= age <= 64
    if entry.programme.startswith("Abdominal aortic aneurysm"):
        return (sex == "m" and age is not None and age >= 65
                and not p.get("aaa_done"))
    if entry.programme.startswith("Diabetic eye"):
        return bool(p.get("diabetes"))
    if entry.programme.startswith("NHS Health Check"):
        return age is not None and 40 <= age <= 74
    if entry.programme.startswith("Antenatal"):
        return bool(p.get("pregnant"))
    if entry.programme.startswith("Newborn"):
        return False  # maternity pathway, not GP recall
    return False


def prevention_check(patient: dict) -> List[dict]:
    """Everything due for this patient: vaccines, screening, CVD prevention.
    Each entry: {"kind", "name", "due": True, "detail"}."""
    out = []
    for v in VACCINES_UK:
        if vaccine_due(v, patient):
            out.append({"kind": "vaccine", "name": v.vaccine, "due": True,
                        "detail": v.schedule_notes})
    for s in SCREENING_UK:
        if screening_due(s, patient):
            out.append({"kind": "screening", "name": s.programme, "due": True,
                        "detail": f"{s.interval} — {s.test}"})
    out.extend(cvd_prevention_advice(patient))
    return out
