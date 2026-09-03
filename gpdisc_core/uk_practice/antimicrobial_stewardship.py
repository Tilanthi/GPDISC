"""Antimicrobial stewardship — first-line empiric therapy + principles.

Expertise program Stage 3, Task 6. NICE/PHE-style quick-reference rows for
the infections that dominate UK primary care prescribing, each with the
delayed-prescribing note and the penicillin-allergic alternative. Doses are
adult oral defaults (renal adjustment via prescribing_safety.renal_flags).
"""
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class AntibioticGuidance:
    infection: str
    first_line: str
    dose_text: str
    duration: str
    penicillin_allergic: str
    delayed_note: str = ""


_ROWS = [
    ("sore throat", "Phenoxymethylpenicillin (only if FeverPAIN 4-5)",
     "500mg QDS", "5-10 days", "Clarithromycin 250-500mg BD",
     "FeverPAIN 0-1: no antibiotic; 2-3: delayed (3-5 day) backup prescription"),
    ("otitis media", "Amoxicillin (only if systemically very unwell or <2y bilateral)",
     "500mg TDS", "5 days", "Clarithromycin 500mg BD",
     "Most need NO antibiotic, or a delayed prescription to collect after 4-5 days"),
    ("sinusitis", "Phenoxymethylpenicillin",
     "500mg QDS", "5 days", "Doxycycline 200mg then 100mg OD",
     "Only if ≥10 days AND worsening after initial improvement (double worsening)"),
    ("lower uti (women)", "Nitrofurantoin MR",
     "100mg BD", "3 days", "Trimethoprim 200mg BD (if low resistance risk)",
     "A back-up prescription is reasonable for mild symptoms"),
    ("lower uti (men)", "Trimethoprim or nitrofurantoin",
     "200mg BD / 100mg BD", "7 days", "As the first-line alternatives",
     "Men always need 7 days; consider prostatitis if systemically unwell"),
    ("pyelonephritis", "Cefalexin (oral if mild)",
     "500mg BD", "7 days", "Ciprofloxacin 500mg BD (resistance concerns)",
     "Admit if systemically unwell, pregnant, or unable to take oral"),
    ("cellulitis", "Flucloxacillin",
     "500mg QDS (1g if >50kg or severe)", "5-7 days",
     "Clarithromycin 500mg BD (or doxycycline)",
     "Mark the erythema margin with a pen; review at 48h; IV if systemic"),
    ("impetigo", "Topical fusidic acid (localised) / oral flucloxacillin (widespread)",
     "TDS topical / 500mg QDS", "5 days localised / 7 days oral",
     "Topical mupirocin / clarithromycin",
     "Hygiene measures; stay off school until lesions are crusted/dried"),
    ("dental infection", "Amoxicillin OR metronidazole (dentist still needed)",
     "500mg TDS / 400mg TDS", "3-5 days", "Metronidazole, or clindamycin 300mg BD",
     "Antibiotics NEVER replace dental drainage — arrange dental referral"),
    ("copd exacerbation", "Amoxicillin (or doxycycline first if sputum purulent, per local policy)",
     "500mg TDS", "5 days", "Doxycycline 200mg then 100mg OD",
     "Only if increased sputum purulence AND more breathless than baseline"),
    ("lower respiratory (chest infection)", "Amoxicillin",
     "500mg TDS", "5 days", "Doxycycline or clarithromycin",
     "Most are viral; use point-of-care CRP where available; CURB-65 for admission"),
    ("c. difficile risk", "N/A — avoidance message",
     "", "", "",
     "Cephalosporins, clindamycin, quinolones and broad cover drive C. difficile "
     "and MRSA — choose the narrowest effective drug for the shortest sensible course"),
]


def _build() -> List[AntibioticGuidance]:
    return [AntibioticGuidance(infection=i, first_line=f, dose_text=d,
                               duration=du, penicillin_allergic=p,
                               delayed_note=n)
            for (i, f, d, du, p, n) in _ROWS]


ANTIBIOTIC_GUIDANCE: List[AntibioticGuidance] = _build()

STEWARDSHIP_PRINCIPLES: List[str] = [
    "Do not start an antibiotic without a plausible bacterial diagnosis and "
    "a documented plan",
    "Record on the prescription: indication, duration, review date",
    "Take cultures BEFORE the first dose where safe (but never delay "
    "treatment of suspected sepsis)",
    "Review at 48-72h: stop, de-escalate, switch to oral, or continue with "
    "a documented reason",
    "Shortest effective duration; use delayed prescribing for self-limiting illness",
    "Explain the no-antibiotic decision to the patient — safety-net the "
    "expected course and what should prompt review",
]


def stewardship_principles() -> List[str]:
    """The six prescribing behaviours that make stewardship real."""
    return list(STEWARDSHIP_PRINCIPLES)

_MALE_RE = re.compile(r"\b(man|men|male|gentleman)\b")


def _match_infections(text: str) -> List[str]:
    """Map free text to infection row keys, most specific first."""
    t = text.lower()
    keys: List[str] = []
    if "pyelonephritis" in t or "kidney infection" in t:
        keys.append("pyelonephritis")
    if "throat" in t:
        keys.append("sore throat")
    if "otitis media" in t or "ear infection" in t or "earache" in t:
        keys.append("otitis media")
    if "sinus" in t:
        keys.append("sinusitis")
    if any(w in t for w in ("cystitis", "uti", "urinary tract infection",
                            "waterwork infection", "urine infection")):
        keys.append("lower uti (men)" if _MALE_RE.search(t)
                    else "lower uti (women)")
    if "cellulitis" in t:
        keys.append("cellulitis")
    if "impetigo" in t:
        keys.append("impetigo")
    if "dental" in t or "tooth" in t or "toothache" in t:
        keys.append("dental infection")
    if "copd" in t:
        keys.append("copd exacerbation")
    if any(w in t for w in ("chest infection", "lrti", "pneumonia",
                            "lower respiratory")):
        keys.append("lower respiratory (chest infection)")
    if "c. difficile" in t or "cdiff" in t or "antibiotic risk" in t:
        keys.append("c. difficile risk")
    return keys


def antibiotic_for(infection_text: str, penicillin_allergy: bool = False
                   ) -> List[AntibioticGuidance]:
    """Return empiric therapy rows for an infection description.

    With ``penicillin_allergy`` the returned rows are copies whose
    ``first_line`` is the penicillin-allergic alternative, so the caller
    surfaces the safe choice directly.
    """
    hits: List[AntibioticGuidance] = []
    for key in _match_infections(infection_text):
        for row in ANTIBIOTIC_GUIDANCE:
            if row.infection == key:
                if penicillin_allergy and row.penicillin_allergic:
                    hits.append(AntibioticGuidance(
                        infection=row.infection,
                        first_line=row.penicillin_allergic,
                        dose_text=row.dose_text,
                        duration=row.duration,
                        penicillin_allergic=row.penicillin_allergic,
                        delayed_note=row.delayed_note))
                else:
                    hits.append(row)
    return hits
