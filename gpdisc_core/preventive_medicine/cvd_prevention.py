"""Cardiovascular primary prevention rules — preventive medicine Stage 2.
Thresholds: NICE CG181/NG238 — QRISK3 10-year risk >=10%: offer
atorvastatin 20mg after lifestyle discussion; clinic BP >=140/90 →
confirm with ABPM/HBPM before diagnosing.
"""
from typing import List


def cvd_prevention_advice(patient: dict) -> List[dict]:
    out = []
    q = patient.get("qrisk10")
    if q is not None and q >= 10 and not patient.get("on_statin") \
            and patient.get("age_years", 0) <= 84:
        out.append({"kind": "cardiovascular", "name": "Statin discussion",
                    "due": True,
                    "detail": f"QRISK3 {q}% >=10% — offer atorvastatin 20mg nightly "
                              "after informed discussion (lifestyle first/alongside)"})
    sbp = patient.get("systolic")
    if sbp is not None and sbp >= 140:
        out.append({"kind": "cardiovascular", "name": "Confirm hypertension",
                    "due": True,
                    "detail": "Clinic BP >=140/90 — confirm with ABPM/HBPM before "
                              "diagnosing (>=135/85 daytime average = hypertension)"})
    if patient.get("smoker"):
        out.append({"kind": "cardiovascular", "name": "Smoking cessation offer",
                    "due": True,
                    "detail": "Very brief advice + referral to stop-smoking service; "
                              "NRT/varenicline per preference"})
    return out
