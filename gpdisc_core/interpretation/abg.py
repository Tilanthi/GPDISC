"""Arterial blood gas interpretation (Stage 9 Task 9.2).

The four-step method: disorder → cause (respiratory/metabolic) →
compensation check → severity. Values accepted in kPa for pCO2/pO2
(a value > 20 is read as mmHg and converted — the unit heuristics real
programs use). Compensation arithmetic: Winter's formula for metabolic
acidosis; the acute/chronic 0.08/0.03 rules for respiratory disorders.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ABGReport:
    disorder: str = "normal"
    cause: str = ""
    compensation: str = ""
    severity: str = ""              # emergency | concern | routine
    findings: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    note: str = ("Numbers describe the moment arterial blood was taken — "
                 "trend and clinical state outrank any single set.")


def _kpa(pco2_or_pao2: float) -> float:
    return v * 0.133 if (v := pco2_or_pao2) > 20 else v


def interpret_abg(ph: float, pco2: float, hco3: float,
                  lactate: Optional[float] = None,
                  pao2: Optional[float] = None,
                  on_air: bool = True) -> ABGReport:
    """Interpret a blood gas. ph unitless, pco2/pao2 in kPa (mmHg values
    are auto-converted), hco3/lactate in mmol/L."""
    r = ABGReport()
    pco2 = _kpa(pco2)
    pao2 = _kpa(pao2) if pao2 is not None else None

    # step 1-2: disorder and cause
    if ph < 7.35:
        r.disorder = "acidosis"
        if pco2 > 6.0 and hco3 < 22.0:
            r.cause = "mixed acidosis (respiratory AND metabolic)"
        elif pco2 > 6.0:
            r.cause = "respiratory"
        else:
            r.cause = "metabolic"
    elif ph > 7.45:
        r.disorder = "alkalosis"
        if pco2 < 4.7 and hco3 > 26.0:
            r.cause = "mixed alkalosis (respiratory AND metabolic)"
        elif pco2 < 4.7:
            r.cause = "respiratory"
        else:
            r.cause = "metabolic"
    else:
        # pH normal: still check for a compensated disorder
        if pco2 > 6.0 or pco2 < 4.7 or hco3 < 22.0 or hco3 > 26.0:
            r.cause = ("compensated — pH held normal while the numbers "
                       "are not")
            r.disorder = "compensated disorder"
        else:
            r.severity = "routine"
            r.findings.append("No acid-base disorder.")
            if lactate is not None and lactate >= 2.0:
                r.findings.append(f"Lactate {lactate} — raised despite "
                                  "normal acid-base: perfusion may still "
                                  "be the problem.")
                r.severity = "concern"
            if pao2 is not None and pao2 < 8.0:
                r.findings.append(f"pO2 {pao2:.1f} kPa — hypoxia with a "
                                  "normal pH is still an emergency of "
                                  "oxygenation, not acid-base.")
                r.severity = "concern"
            return r

    r.findings.append(f"pH {ph}, pCO2 {pco2:.1f} kPa, HCO3 {hco3} — "
                      f"{r.disorder}, {r.cause}.")

    # step 3: compensation arithmetic
    if r.disorder == "acidosis" and r.cause.startswith("metabolic"):
        # Winter's: expected pCO2(mmHg) = 1.5*HCO3 + 8, ±2; the ±2 band
        # is in mmHg too, so everything converts to kPa before comparing
        expected = (1.5 * hco3 + 8) * 0.133      # mmHg → kPa
        band = 2 * 0.133
        if pco2 > expected + band:
            r.compensation = (
                f"Under-compensated: expected pCO2 ~{expected:.1f} kPa "
                "(Winter's) — a concurrent respiratory acidosis is "
                "fatiguing the patient")
            r.findings.append(r.compensation)
        elif pco2 < expected - band:
            r.compensation = (
                f"Over-compensated vs Winter's (expected ~{expected:.1f} "
                "kPa) — look for a second, respiratory alkalosis "
                "(sepsis, PE, salicylates)")
            r.findings.append(r.compensation)
        else:
            r.compensation = "appropriately compensated (Winter's)"
    if r.cause.startswith("respiratory"):
        r.compensation = ("acute vs chronic changes the diagnosis: "
                          "0.08 pH per 10 mmHg pCO2 = acute; 0.03 = "
                          "chronic (retaining kidneys)")
        r.findings.append(r.compensation)

    # step 4: severity and the frames that matter
    r.severity = "concern"
    if ph <= 7.20 or ph >= 7.60:
        r.severity = "emergency"
        r.actions.append("pH in the danger band — senior review now; "
                         "this is an admission whatever the cause.")
    if lactate is not None and lactate >= 4.0:
        r.severity = "emergency"
        r.findings.append(f"Lactate {lactate} — tissue hypoperfusion: "
                          "sepsis, shock or hypoxia driving it; find "
                          "the driver with the sepsis screen, don't "
                          "just re-test.")
        r.actions.append("Sepsis Six if any infection pointer; "
                         "crystalloid, cultures, lactate re-check.")
    if r.disorder == "acidosis" and r.cause.startswith("metabolic") and \
            hco3 < 10:
        r.findings.append("HCO3 <10 with acidosis: think ketoacidosis, "
                          "lactate, or toxin (check ketones, lactate, "
                          "salicylates, and the anion gap you can "
                          "calculate from the rest of the chemistry).")
    if pao2 is not None and pao2 < 8.0:
        r.severity = "emergency"
        r.findings.append(f"pO2 {pao2:.1f} kPa — hypoxia is the "
                          "emergency; oxygenation before acid-base "
                          "elegance.")
        if on_air and pco2 < 5.0:
            r.findings.append("Hypoxia WITHOUT high pCO2: the problem is "
                              "gas exchange (PE, pneumonia, shunt) not "
                              "ventilation — an A-a gradient problem.")
    if not r.actions:
        r.actions.append("Treat the cause, not the pH — repeat the gas "
                         "after each meaningful intervention.")
    return r
