"""Urine dip, PFT, synovial fluid, culture logic (Stage 9 Task 9.2).

The four pattern-readers that decide whole pathways in one line:
dipstick (infection vs glomerular vs ketoacidosis), spirometry
(obstructive vs restrictive vs nothing), the joint aspirate
(non-inflammatory vs inflammatory vs septic), and the culture report
(pathogen vs contaminant). Deterministic thresholds from standard
tables; every output states what it does NOT settle.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PatternReport:
    pattern: str = ""
    urgency: str = "routine"        # emergency | urgent | routine
    findings: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    note: str = ""


def interpret_urine_dip(dip: Dict[str, bool], context: Optional[dict] = None) -> PatternReport:
    """dip keys: blood, protein, leukocytes, nitrites, glucose,
    ketones (True/False/absent)."""
    r = PatternReport(
        note="A dipstick is a screening test; culture decides treatment "
             "in pregnancy, men, and treatment failure.")
    g = lambda k: bool(dip.get(k))
    ctx = context or {}

    if g("nitrites") and g("leukocytes"):
        r.pattern = "UTI — both infection markers positive"
        r.urgency = "urgent" if ctx.get("pregnant") or \
            ctx.get("fever") else "routine"
        r.findings.append("Nitrites + leukocytes: bacteria converting "
                          "dietary nitrate + pyuria = established "
                          "infection.")
        r.actions.append("Nitrofurantoin first-line (3 days women, 7 men "
                         "per local policy) — check eGFR and pregnancy "
                         "before choosing.")
        if ctx.get("fever") or ctx.get("loin_pain"):
            r.findings.append("Fever or loin pain makes this upper-tract: "
                              "pyelonephritis, not cystitis.")
            r.actions.append("Urine culture + 7-day course; admission if "
                             "systemically unwell or vomiting the "
                             "antibiotics.")
    elif g("leukocytes") and not g("nitrites"):
        r.pattern = "Sterile pyuria picture (leukocytes alone)"
        r.findings.append("Pyuria without nitrites: early UTI, "
                          "atypical organism, or the three classics — "
                          "chlamydia, a stone, TB (sterile pyuria in a "
                          "high-prevalence patient).")
        r.actions.append("Culture before antibiotics; consider STI "
                         "screening in the young sexually-active patient.")
    elif g("blood") and g("protein") and not g("leukocytes"):
        r.pattern = "Glomerular pattern (blood + protein, no infection)"
        r.urgency = "urgent"
        r.findings.append("Blood + protein without pyuria is a kidney "
                          "filter problem until proven otherwise "
                          "(glomerulonephritis).")
        r.actions.append("Quantify: ACR/PCR, BP, creatinine, "
                         "complement + immunology screen; nephrology "
                         "referral — rapidly-progressive GN loses "
                         "kidneys in days.")
    if g("glucose") and g("ketones"):
        r.urgency = "emergency"
        r.pattern = (r.pattern + "; " if r.pattern else "") + \
            "Glucose + ketones: ketoacidosis until excluded"
        r.actions.append("Capillary ketones and a glucose NOW — DKA "
                         "pathway if confirmed; do not wait for the "
                         "laboratory.")
    elif g("glucose"):
        r.findings.append("Glycosuria: diabetes screen (HbA1c/FBG) — "
                          "renal glycosuria and SGLT2 inhibitors are the "
                          "benign reasons.")
    if not r.pattern and not r.findings:
        r.pattern = "Negative dipstick"
        r.findings.append("Negative dip with consistent symptoms still "
                          "deserves thought — stones and early "
                          "infection dip negative.")
    return r


def interpret_pft(fev1_pct_predicted: float,
                  fvc_pct_predicted: float,
                  reversibility_pct: Optional[float] = None,
                  context: Optional[dict] = None) -> PatternReport:
    """Classify spirometry. fev1/fvc percentages-of-predicted; the ratio
    is computed from them (assumes same predicted denominators)."""
    r = PatternReport(
        note="Spirometry classifies; it does not name the disease — "
             "the clinician correlates with exposure, history, and "
             "examination.")
    if fvc_pct_predicted <= 0:
        r.pattern = "Cannot interpret"
        r.findings.append("FVC missing or zero — ratio uncomputable.")
        return r
    ratio = fev1_pct_predicted / fvc_pct_predicted   # percent-of-pred ratio
    if ratio < 0.70:
        r.pattern = "Obstructive pattern (FEV1/FVC < 0.70)"
        sev = ("mild" if fev1_pct_predicted >= 80 else
               "moderate" if fev1_pct_predicted >= 50 else "severe")
        r.findings.append(f"Obstruction, {sev} by FEV1 "
                          f"({fev1_pct_predicted}% predicted).")
        if reversibility_pct is not None and \
                (reversibility_pct >= 12):
            r.findings.append(f"{reversibility_pct}% bronchodilator "
                              "reversibility — significant: asthma sits "
                              "on this side of the line.")
            r.actions.append("Treat as asthma-likely: steroid trial, "
                             "inhaler technique, FeNO/peak-flow diary.")
        else:
            r.findings.append("No significant reversibility — COPD "
                              "picture; asthma is not excluded by one "
                              "negative test.")
            r.actions.append("COPD bundle: smoking cessation (the only "
                             "disease-modifying step), vaccinations, "
                             "pulmonary rehab, inhaler choice by "
                             "severity.")
    elif fev1_pct_predicted < 80 and fvc_pct_predicted < 80:
        r.pattern = "Restrictive pattern (both reduced, ratio preserved)"
        r.findings.append("Low FEV1 AND FVC with a normal ratio: "
                          "restrictive — confirm with lung volumes; "
                          "the causes are parenchymal (fibrosis), "
                          "chest-wall (obesity, kyphosis), or muscle.")
        r.actions.append("Full lung volumes + TLCO: TLCO low = "
                         "parenchymal; TLCO preserved = chest wall or "
                         "neuromuscular; then image.")
    else:
        r.pattern = "Normal spirometry"
        r.findings.append("Normal pattern — symptoms with normal "
                          "spirometry point elsewhere (anaemia, "
                          "cardiac, upper airway, functional breath-"
                          "lessness).")
        if reversibility_pct is not None and reversibility_pct >= 12:
            r.findings.append("But reversibility is present — "
                              "asthma can normalise between attacks; "
                              "chase with peak-flow diary or challenge "
                              "testing.")
    return r


def interpret_synovial_fluid(appearance: str = "",
                             wbc: Optional[float] = None,
                             crystals: str = "",
                             gram_stain: str = "",
                             context: Optional[dict] = None) -> PatternReport:
    """The three-fluid rule: clear/inflammatory/septic by WBC, with the
    crystal modifier and the iron law that crystals never exclude "
    "infection."""
    r = PatternReport(
        note="Aspiration is both test and treatment for a hot joint — "
             "the biggest error is failing to aspirate at all.")
    ctx = context or {}

    if gram_stain and "no organism" not in gram_stain.lower() and \
            "negative" not in gram_stain.lower():
        r.pattern = "Gram-positive organisms in the joint"
        r.urgency = "emergency"
        r.actions.append("Septic arthritis: washout + IV antibiotics "
                         "TODAY — every hour of delay damages cartage "
                         "permanently.")
        return r

    septic_picture = (wbc is not None and wbc > 75000) or \
        "frankly purulent" in (appearance or "").lower() or "pus" in \
        (appearance or "").lower()
    if septic_picture:
        r.pattern = f"Septic-range fluid (WBC >75,000)"
        r.urgency = "emergency"
        r.findings.append("Turbid, high-WBC joint fluid is septic "
                          "arthritis until Gram stain and culture say "
                          "otherwise.")
        if crystals:
            r.findings.append(f"Crystals present ({crystals}) — THE "
                              "CRYSTAL DOES NOT EXCLUDE INFECTION: "
                              "gout and septic arthritis co-exist and "
                              "the wrong choice costs the joint.")
        r.actions.append("Urgent washout + IV antibiotics; do not "
                         "settle for aspiration alone unless the "
                         "patient cannot have surgery.")
        return r

    if wbc is not None and wbc > 2000:
        r.pattern = "Inflammatory fluid (WBC 2,000-75,000)"
        r.urgency = "urgent"
        if "needle" in crystals.lower() or "negative" in crystals.lower():
            r.findings.append("Negatively-birefringent needle crystals: "
                              "gout — the diagnosis is made.")
            r.actions.append("Treat the gout (NSAID/colchicine/steroid "
                             "per comorbidity); allopurinol LATER, "
                             "never in the flare.")
        elif "rhomboid" in crystals.lower() or "positive" in crystals.lower():
            r.findings.append("Positively-birefringent rhomboid "
                              "crystals: CPPD (pseudogout).")
            r.actions.append("Treat the flare; screen for the "
                             "associations (hyperparathyroidism, "
                             "haemochromatosis, hypothyroid, "
                             "hypomagnesaemia) in the recurrent case.")
        else:
            r.findings.append("Inflammatory without crystals: the "
                              "spondyloarthritides, RA, reactive, or "
                              "Lyme depending on the story.")
            r.actions.append("Rheumatology referral with the story, "
                             "not just the fluid.")
        if not crystals:
            r.findings.append("Culture sent even when the pattern looks "
                              "benign — crystal-negative inflammatory "
                              "joints still get infected.")
        return r

    r.pattern = "Non-inflammatory fluid (WBC <2,000)"
    r.findings.append("Clear, viscous, low-WBC fluid: OA or trauma.")
    if "blood" in (appearance or "").lower() or "haemorrhagic" in \
            (appearance or "").lower():
        r.findings.append("Bloody aspirate: haemarthrosis — trauma, "
                          "anticoagulation, or (in the right age) "
                          "pigmented villonodular synovitis.")
        r.actions.append("Check clotting + anticoagulants; recurrent "
                         "haemarthrosis in a young joint is an "
                         "orthopaedic question.")
    else:
        r.actions.append("Symptomatic OA management; the aspirate has "
                         "excluded the two things that end joints.")
    return r


def interpret_culture(site: str, organisms: List[str],
                      context: Optional[dict] = None) -> PatternReport:
    """Culture logic: pathogen vs contaminant vs no-growth, with the
    timing rules (blood cultures before antibiotics — except when
    sepsis says otherwise)."""
    r = PatternReport(
        note="A culture names an organism; it does not name a disease. "
             "Treat the patient, not the report.")
    ctx = context or {}
    s = site.lower()
    orgs = [o for o in organisms if o]
    skin_flora = ("coagulase negative", "corynebacterium", "bacillus",
                  "micrococcus", "diphtheroid", "propionibacter")
    n_skin = sum(1 for o in orgs if any(f in o.lower()
                                        for f in skin_flora))

    if not orgs:
        r.pattern = "No growth"
        r.urgency = "routine"
        r.findings.append("No growth" + (" after 5 days" if "blood" in s
                                         else "") + ".")
        if "blood" in s and ctx.get("antibiotics_first"):
            r.findings.append("Antibiotics before the cultures: "
                              "culture-negative is expected, not "
                              "reassuring — treat on the clinical "
                              "syndrome (and remember culture-negative "
                              "endocarditis when the story fits).")
        if "blood" in s and ctx.get("endocarditis_suspected"):
            r.actions.append("Serial cultures over 48h + echocardiogram "
                             "before abandoning the chase: some "
                             "organisms (Coxiella, Bartonella, HACEK) "
                             "need special media or serology.")
        return r

    if "blood" in s:
        if n_skin >= 2:
            r.pattern = "Likely contaminant (skin flora in multiple " \
                "bottles)"
            r.urgency = "routine"
            r.findings.append(f"{' and '.join(orgs[:2])} — but "
                              "indistinguishable from poor sampling "
                              "technique.")
            r.actions.append("Do NOT treat a well patient for skin "
                             "flora; if the patient is septic or has a "
                             "central line, repeat cultures properly "
                             "and culture the line tip on removal.")
        elif n_skin == 1 and not ctx.get("line_in_situ") and \
                not ctx.get("septic"):
            r.pattern = "Single-bottle skin flora: probable contaminant"
            r.urgency = "routine"
            r.actions.append("Correlate: a well patient with one "
                             "coagulase-negative bottle needs a repeat, "
                             "not antibiotics.")
        else:
            r.pattern = "Significant bacteraemia"
            r.urgency = "urgent"
            if "aureus" in " ".join(orgs).lower():
                r.urgency = "emergency"
                r.findings.append("S. aureus in blood is NEVER a "
                                  "contaminant: hunt the source "
                                  "(skin, endocarditis, bone, line) — "
                                  "echo if any doubt.")
                r.actions.append("Repeat cultures, source hunt, "
                                 "endocarditis screen; MSSA/MRSA "
                                 "directs the antibiotic, not the "
                                 "urgency.")
            else:
                r.findings.append(f"{', '.join(orgs)} from a normally "
                                  "sterile site: treat and find the "
                                  "source.")
                r.actions.append("Source control + targeted therapy; "
                                 "repeat cultures 48h into treatment "
                                 "for the persistent-bacteraemia "
                                 "question.")
        return r

    if "urine" in s:
        r.pattern = "Growth in urine"
        r.urgency = "routine"
        if ctx.get("catheter") or ctx.get("asymptomatic"):
            r.findings.append("Asymptomatic bacteriuria (catheter or "
                              "no symptoms): NOT an infection — "
                              "treating it breeds resistance and "
                              "C. difficile without helping.")
            r.actions.append("No antibiotics; treat only if pregnant, "
                             "pre-urological-procedure, or symptomatic.")
        else:
            r.actions.append("Treat per sensitivities; short course per "
                             "sex/pregnancy policy.")
        return r

    # default: single sterile-site organism is significant
    r.pattern = "Growth reported"
    r.urgency = "urgent"
    r.findings.append(f"{', '.join(orgs)} from {site or 'this site'} — "
                      "interpret with the specimen quality and the "
                      "patient.")
    r.actions.append("Correlate with the clinical picture; treat when "
                     "the organism, the site, and the patient agree.")
    return r
