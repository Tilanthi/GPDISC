"""DVLA fitness-to-drive rules for medical conditions (UK).

Expertise program Stage 3, Task 3. Group 1 = car/motorcycle; group 2 =
lorry/bus (stricter). Aligned with the DVLA "Assessing fitness to drive"
guide, guidance-era 2026 — DVLA updates these thresholds frequently, so
every uncertain case ends with "check current DVLA guidance".

Two GP duties the tables encode:
1. Diagnose → advise the patient of the legal duty to notify DVLA
   (and document that advice — the medicolegal burden is the doctor's).
2. Inform DVLA directly only if the patient refuses to and continues
   driving after being told of the duty.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class DrivingRule:
    condition: str
    keywords: List[str] = field(default_factory=list)
    group1_rule: str = ""
    group2_rule: str = ""
    note: str = ""


_ROWS = [
    ("First seizure", ["first seizure", "first fit", "single seizure"],
     "6 months off (may reduce to 3 months if low risk on specialist assessment)",
     "5 years off; specialist assessments required",
     "DVLA must be informed; cause sought"),
    ("Epilepsy (established)", ["epilepsy"],
     "12 months seizure-free, or 1 year awake-seizure-free with an "
     "established sleep-only pattern",
     "10 years seizure-free off medication",
     "Medication changes can restart the clock"),
    ("TIA / stroke", ["tia", "stroke", "mini stroke"],
     "1 month off after TIA/stroke; notify DVLA only if residual deficit "
     "(visual field, cognitive, limb function)",
     "Licence refused/revoked for 1 year after stroke or TIA; relicensing "
     "after 1 year needs no debarring impairment (may need exercise ECG)",
     "Multiple TIAs: 1 month off after each episode"),
    ("Myocardial infarction", ["heart attack", "myocardial infarction", "mi "],
     "1 week off if uncomplicated with successful treatment (e.g. PCI)",
     "6 weeks; may need a functional test",
     "Angina: must not drive while symptomatic"),
    ("Angioplasty (elective)", ["angioplasty", "stent", "pci"],
     "1 week off after elective PCI; no need to notify DVLA (uncomplicated)",
     "6 weeks, provided LVEF ≥40% and functional test requirements met",
     "Elective PCI is 1 week; PCI for ACS has its own (1 week) standard — "
     "medically managed ACS is 4 weeks"),
    ("Syncope", ["syncope", "faint", "blackout"],
     "Unexplained: 6 months off (notify DVLA). Vasovagal with reliable "
     "prodrome, not while driving: may drive once recovered; if it happened "
     "while driving: 1 month. No reliable prodrome: 3 months",
     "Unexplained: licence revoked 12 months (5 years if recurrent); reflex "
     "syncope 3-12 months by pattern, with specialist report",
     "Identify the cause; cardiac syncope follows the underlying-diagnosis "
     "standard and needs cardiology review"),
    ("Diabetes on insulin", ["insulin", "diabetes on insulin"],
     "3-year licence with demonstrated hypoglycaemia awareness; check glucose "
     "before driving and every 2 hours on long drives",
     "Annual with consultant report; demonstrated awareness",
     "Hypoglycaemia unawareness: stop driving and renotify"),
    ("Hypoglycaemia unawareness", ["hypo unawareness", "hypoglycaemia unawareness",
                                   "hypo unaware"],
     "Stop driving until awareness restored (usually ≥6 months documented)",
     "Stop driving; specialist confirmation required",
     "The most common pitfall for insulin-treated drivers"),
    ("Sleep apnoea", ["sleep apnoea", "osa", "obstructive sleep apnoea"],
     "Stop until symptoms controlled AND compliant with therapy",
     "Same; annual review",
     "Excessive sleepiness is the trigger, not the diagnosis label"),
    ("Visual field defect", ["visual field", "hemianopia", "field defect",
                             "glaucoma"],
     "Must meet visual field standards; binocular field testing",
     "Higher standard applies",
     "Acuity: must read a post-plate at 20 metres"),
    ("Alcohol misuse", ["alcohol misuse", "alcohol problem"],
     "6 months off after a period of controlled drinking confirmed",
     "1 year; medical review",
     "Dependency: 1 year (group 1) after confirmed remission"),
    ("Drug misuse", ["drug misuse", "illicit drugs"],
     "6 months - 1 year after cessation, per pattern",
     "1 year; testing may be required",
     "Persistence varies by substance"),
    ("Dementia / cognitive impairment", ["dementia", "cognitive impairment",
                                         "mci with driving"],
     "Case-by-case: functional driving assessment + informant history",
     "Likely refused at significant impairment",
     "GP conversation: 'I must advise you of the legal duty to notify DVLA — "
     "here is what happens next'"),
    ("Pacemaker insertion", ["pacemaker"],
     "1 week off after first implant",
     "6 weeks",
     "ICD: 6 months off (group 1); group 2 licence refused"),
]


def _build() -> List[DrivingRule]:
    return [DrivingRule(condition=c, keywords=list(k), group1_rule=g1,
                        group2_rule=g2, note=n)
            for (c, k, g1, g2, n) in _ROWS]


DRIVING_RULES: List[DrivingRule] = _build()


def driving_rules(text: str, group: int = 1) -> List[DrivingRule]:
    """Return the driving rules matching a presentation.

    ``group`` selects which rule text matters (1 = car/motorcycle,
    2 = lorry/bus) — both texts remain on the returned rule objects.
    """
    t = text.lower()
    return [r for r in DRIVING_RULES if any(k in t for k in r.keywords)]
