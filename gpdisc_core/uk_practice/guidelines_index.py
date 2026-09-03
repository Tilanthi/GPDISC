"""NICE / CKS guideline index — UK practice reference registry.

Expertise program Stage 3, Task 1. Structured pointers to the guidelines a
GP consults daily. Reference pointers only (IDs + topic names); full text
lives with NICE/CKS. Ages/thresholds inside notes are guidance-era 2026 —
always "check current" for medicolegal decisions.
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GuidelineRef:
    """Pointer to a NICE guideline / CKS topic for a clinical area."""
    topic: str
    nice_ref: str
    cks_topic: str
    note: str = ""


_ROWS = [
    ("chest pain", "NICE CG95", "Chest pain - recent onset",
     "Typical/angina → rapid-access chest pain clinic; 2ww if lung cancer features"),
    ("atrial fibrillation", "NICE NG196", "Atrial fibrillation",
     "CHA2DS2-VASc + ORBIT bleed; rate vs rhythm"),
    ("hypertension", "NICE NG136", "Hypertension - not diabetic",
     "Confirm ABPM/HBPM ≥135/85; A <55y ACEi"),
    ("heart failure", "NICE NG106", "Heart failure - chronic",
     "NT-proBNP >400 → echo; the 4 pillars"),
    ("type 2 diabetes", "NICE NG28", "Diabetes - type 2",
     "HbA1c targets individualised; SGLT2 first add-on if CVD/CKD"),
    ("type 1 diabetes", "NICE NG17", "Diabetes - type 1", ""),
    ("copd", "NICE NG115", "Chronic obstructive pulmonary disease",
     "Spirometry FEV1/FVC <0.7"),
    ("asthma", "NICE NG80", "Asthma",
     "Objective tests before diagnosing in adults"),
    ("stroke", "NICE NG128", "Stroke and TIA",
     "Recognition: FAST; specialist within 24h"),
    ("tia", "NICE NG128", "Stroke and TIA",
     "Secondary prevention; carotid imaging"),
    ("epilepsy", "NICE CG137", "Epilepsy",
     "Specialist within 2 weeks of first seizure"),
    ("migraine", "NICE CG150", "Migraine",
     "Zolmitriptan nasal if vomiting; combination acute therapy"),
    ("depression", "NICE NG222", "Depression",
     "PHQ-9; stepped care"),
    ("generalised anxiety", "NICE CG113", "Generalised anxiety disorder",
     "GAD-7; low-intensity CBT first"),
    ("dementia", "NICE NG97", "Dementia",
     "Cognitive testing + history; do not use bloods alone"),
    ("urinary tract infection", "NICE NG109", "Urinary tract infection - lower",
     "Nitrofurantoin 100mg MR BD 3d women; 7d men"),
    ("pyelonephritis", "NICE NG109", "Urinary tract infection - upper",
     "Cefalexin or consider admission"),
    ("sore throat", "NICE NG84", "Sore throat - acute",
     "FeverPAIN; delayed prescribing"),
    ("otitis media", "NICE NG91", "Otitis media - acute",
     "No antibiotic or delayed 4-5d"),
    ("sinusitis", "NICE NG79", "Sinusitis - acute",
     "≥10 days + worsening course"),
    ("cellulitis", "NICE NG141 (antimicrobial)", "Cellulitis - acute",
     "Mark borders; Eron classification"),
    ("back pain", "NICE NG59", "Back pain - low",
     "Red flags first; no imaging without"),
    ("contraception", "FSRH 2025 (ceg); NICE", "Contraception",
     "UKMEC categories; LARC first discussion"),
    ("palliative care", "NICE NG31 + 'Guidelines' (Irish/Scottish used UK-wide)",
     "Palliative care", "Anticipatory prescribing"),
]


def _build() -> List[GuidelineRef]:
    return [GuidelineRef(topic=t, nice_ref=r, cks_topic=c, note=n)
            for (t, r, c, n) in _ROWS]


GUIDELINES: List[GuidelineRef] = _build()


def lookup_guideline(text: str) -> List[GuidelineRef]:
    """Return guideline refs whose topic keywords appear in the text."""
    t = text.lower()
    return [g for g in GUIDELINES if g.topic in t]
