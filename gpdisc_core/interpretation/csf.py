"""CSF interpretation (Stage 9 Task 9.2).

The three-question method: cells (who is in there?) → glucose (is the
bacteria eating it? compare with serum) → protein (is the barrier
broken?) — with xanthochromia answering the SAH question a CT cannot.
Gram stain and PCR override the cell counts whenever present.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CSFReport:
    pattern: str = "undetermined"
    urgency: str = "routine"        # emergency | urgent | routine
    findings: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    note: str = ("Interpret against the clinical picture; the single most "
                 "common CSF error is interpreting a traumatic tap as SAH "
                 "— or the reverse.")


def interpret_csf(appearance: str = "",
                  wbc: Optional[float] = None,
                  neutrophils_pct: Optional[float] = None,
                  protein: Optional[float] = None,
                  csf_glucose: Optional[float] = None,
                  serum_glucose: Optional[float] = None,
                  xanthochromia: Optional[bool] = None,
                  gram_stain: str = "",
                  context: Optional[dict] = None) -> CSFReport:
    """Interpret a CSF result. Units: WBC ×10^6/L, protein g/L, glucose
    mmol/L. Absent values are treated as unknown, never zero."""
    r = CSFReport()
    ctx = context or {}

    # stains/PCR outrank cells
    if gram_stain and "no organism" not in gram_stain.lower() and \
            "negative" not in gram_stain.lower():
        r.pattern = f"Gram-positive organisms seen: {gram_stain}"
        r.urgency = "emergency"
        r.findings.append("Organisms on Gram stain = meningitis, full "
                          "stop.")
        r.actions.append("Antibiotics NOW (third-generation "
                         "cephalosporin + dexamethasone per protocol) — "
                         "before anything else is waited for.")
        return r

    if xanthochromia:
        r.pattern = "Xanthochromia present"
        r.urgency = "emergency"
        r.findings.append("Xanthochromia confirms SAH even when the CT "
                          "is clean — blood has been in the CSF "
                          "hours-to-days.")
        r.actions.append("Neurosurgeons / interventional neuroradiology "
                         "referral today; CT angiography per pathway.")
        return r

    ratio = None
    if csf_glucose is not None and serum_glucose:
        ratio = csf_glucose / serum_glucose

    # the pattern table
    neutrophil_picture = bool(wbc is not None and wbc > 100 and
                              (neutrophils_pct is None
                               or neutrophils_pct > 60))
    lymphocyte_picture = bool(wbc is not None and wbc > 50 and
                              neutrophils_pct is not None
                              and neutrophils_pct <= 60)
    low_glucose = ratio is not None and ratio < 0.4

    if neutrophil_picture:
        if low_glucose or (protein is not None and protein > 1.0):
            r.pattern = ("Bacterial pattern (neutrophils, low glucose, "
                        "high protein)")
            r.urgency = "emergency"
            r.findings.append("Neutrophil-predominant pleocytosis with "
                              "glucose <40% of serum and/or protein "
                              ">1.0 g/L.")
            r.actions.append("Treat as bacterial meningitis NOW — "
                             "antibiotics within the hour beat every "
                             "diagnostic refinement.")
            r.actions.append("Notify public health; close contacts need "
                             "prophylaxis.")
        else:
            r.pattern = ("Neutrophilic picture without full bacterial "
                         "biochemistry")
            r.urgency = "emergency"
            r.findings.append("Partially treated meningitis still looks "
                              "like this — antibiotics given earlier "
                              "change the CSF, not the obligation to "
                              "treat.")
            r.actions.append("Treat as bacterial meningitis; the "
                             "history of pre-LP antibiotics explains a "
                             "blunted picture.")
    elif lymphocyte_picture:
        if low_glucose or (protein is not None and protein > 1.0):
            r.pattern = "Lymphocytic picture with low glucose/high " \
                        "protein"
            r.urgency = "urgent"
            r.findings.append("TB or fungal meningitis look like this — "
                              "subacute onset, lymphocytes, and the "
                              "glucose the organism eats.")
            r.actions.append("Same-day senior + ID review: TB work-up "
                             "(CT chest, NAAT, CSF opening pressure), "
                             "start empiric TB therapy on clinical "
                             "suspicion rather than waiting for "
                             "culture weeks.")
        else:
            r.pattern = "Viral pattern (lymphocytes, normal glucose)"
            r.urgency = "urgent"
            r.findings.append("Lymphocytic pleocytosis with preserved "
                              "glucose: enterovirus, HSV/VZV, or early "
                              "viral meningitis.")
            r.actions.append("HSV PCR if any encephalitic features "
                             "(confusion, seizures, behaviour change) — "
                             "acyclovir before the PCR returns if "
                             "encephalitis is on the table.")
    elif wbc is not None and wbc > 5:
        r.pattern = "Mild pleocytosis"
        r.urgency = "urgent"
        r.findings.append("Borderline cells: early viral illness, "
                          "post-infectious, or resolving process — "
                          "correlate with the story.")
        r.actions.append("Repeat LP only if the clinical picture "
                         "demands; most mild pleocytosis is followed, "
                         "not chased.")
    elif wbc is not None:
        r.pattern = "Normal cell count"
        r.urgency = "routine"
        r.findings.append("No pleocytosis; SAH effectively excluded "
                          "beyond 12h if the bilirubin assay was "
                          "properly run.")

    if appearance and ("blood" in appearance.lower() or
                       "rbc" in appearance.lower()):
        r.findings.append("Blood-stained CSF: count the WBC against the "
                          "RBC (1 WBC per ~500-700 RBC is the "
                          "correction) before calling it pleocytosis — "
                          "or dismissing SAH before xanthochromia "
                          "reports.")
    return r
