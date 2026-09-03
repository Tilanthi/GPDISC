"""ECG pattern interpretation (Stage 9 Task 9.2).

Text-pattern driven: the clinician types what they see ("irregularly
irregular, no P waves", "ST elevation V2-V4"). The interpreter names the
rhythm, maps territory to artery, states urgency, and gives the next
actions — deterministic rules, never a guessed measurement. Describes
patterns, not patients: the clinician correlates.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ECGReport:
    rhythm: str = "undetermined"
    urgency: str = "routine"       # emergency | urgent | routine
    findings: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    note: str = ("Pattern interpretation only — correlate with the patient, "
                 "the previous ECG, and the specimen in front of you.")

    def summary(self) -> str:
        lines = [f"Rhythm/pattern: {self.rhythm}",
                 f"Urgency: {self.urgency}"]
        for f in self.findings:
            lines.append(f"  - {f}")
        for a in self.actions:
            lines.append(f"  → {a}")
        lines.append(self.note)
        return "\n".join(lines)


# STEMI territory: leads mentioned → artery → what it changes. Multiple
# territories can legitimately co-exist (inferolateral); all matches are
# reported, none overwrite each other.
_TERRITORIES = [
    (re.compile(r"\bv[12]\b|anteroseptal", re.I),
     "Anteroseptal (V1-V2)",
     "LAD — the highest-mortality territory",
     "Primary PCI now; door-to-balloon is the metric. Watch for "
     "cardiogenic shock and VF."),
    (re.compile(r"\bv[34]\b|anterior", re.I),
     "Anterior (V3-V4)",
     "LAD occlusion",
     "Primary PCI now; continuous monitoring."),
    (re.compile(r"\bii\b|\biii\b|inferior|\bavf\b", re.I),
     "Inferior (II, III, aVF)",
     "RCA occlusion (usually)",
     "Record RIGHT-SIDED leads (V4R): RV involvement makes nitrates and "
     "opioids hypotension-inducing — these patients are preload-dependent."),
    (re.compile(r"\bi\b(?!i)|\bavl\b|lateral|\bv[56]\b", re.I),
     "Lateral (I, aVL, V5-V6)",
     "Circumflex territory",
     "PCI; look for reciprocal changes in the inferior leads."),
    (re.compile(r"st depression.*v[1-3]|tall r.*v[1-3]|posterior", re.I),
     "Posterior (ST depression V1-V3 with tall R waves)",
     "Posterior MI — the mirror image that gets missed",
     "Treat as STEMI-equivalent: posterior leads V7-V9, and prime PCI "
     "on the ST-depression pattern alone."),
]


def _stem(text: str, rep: ECGReport) -> bool:
    if not re.search(r"st elevat\w*|stelevation|stem[il]|"
                     r"st depression.*v[1-3]|tall r.*v[1-3]|posterior",
                     text, re.I):
        return False
    names = []
    for rx, name, artery, action in _TERRITORIES:
        if rx.search(text):
            names.append(name)
            rep.findings.append(f"Territory: {name} → {artery}")
            rep.actions.append(action)
    if names:
        rep.rhythm = "ST elevation — " + " + ".join(names)
    else:
        rep.findings.append("ST elevation described; leads not stated — "
                            "territory unmapped, treat as STEMI until "
                            "mapped.")
        rep.rhythm = "ST elevation — territory unmapped"
    rep.urgency = "emergency"
    rep.actions.append("Do not wait for troponin — the ECG is the "
                       "activation test; emergency call now.")
    if re.search(r"chest pain|sweat|clammy|collapse|syncope", text, re.I):
        rep.findings.append("Presentation consistent with occlusion "
                            "(pain/sweating) — do not serial-test.")
    return True


def interpret_ecg(text: str, context: Optional[Dict] = None) -> ECGReport:
    """Interpret a described ECG. Every exit states urgency and the next
    action; "I don't recognise this pattern" is a valid output."""
    rep = ECGReport()
    t = text or ""
    ctx = context or {}

    # hyperkalaemia before digoxin before benign rhythms: the treat-first
    # patterns claim the trace
    if re.search(r"peak\w* t waves|tall t waves|sine wave|wide qrs.*"
                 r"(no p|absent p)|broadening qrs", t, re.I):
        rep.rhythm = "Hyperkalaemia pattern until excluded"
        rep.urgency = "emergency"
        rep.findings.append("Peaked T waves / widening QRS / loss of P "
                            "waves is potassium killing conduction.")
        rep.actions.append("Calcium gluconate IV to stabilise the "
                           "myocardium NOW; insulin-dextrose to shift K; "
                           "treat on the ECG — do not wait to repeat the "
                           "blood test.")
        if ctx.get("potassium"):
            rep.findings.append(
                f"Given K+ {ctx['potassium']} — hyperkalaemia is "
                "confirmed, not suspected.")
        return rep

    if re.search(r"digoxin|digitoxin", t, re.I) and \
            re.search(r"block|bradycard|arrhythmi|tachycard|irregular|"
                      r"ectopic|tick", t, re.I):
        rep.rhythm = "Digoxin effect/toxicity pattern"
        rep.urgency = "urgent"
        rep.findings.append("ANY arrhythmia on digoxin is toxicity until "
                            "proven otherwise; AV block with atrial "
                            "tachycardia and the reverse-tick ST are the "
                            "classics.")
        rep.actions.append("Digoxin level + U&E today; hypokalaemia "
                           "potentiates toxicity — check and replace; "
                           "digoxin-specific antibody fragments if "
                           "haemodynamically unwell.")
        return rep

    if re.search(r"polymorphic|torsades|twisting", t, re.I):
        rep.rhythm = "Polymorphic VT / possible torsades de pointes"
        rep.urgency = "emergency"
        rep.actions.append("Magnesium IV regardless of magnesium level; "
                           "stop every QT-prolonging drug on the chart; "
                           "defibrillate if pulseless.")
        return rep

    if re.search(r"(broad|wide)[- ]complex.*tachycard|"
                 r"tachycard.*(broad|wide)[- ]complex|"
                 r"\bvt\b|monomorphic|"
                 r"(broad|wide)[- ]complex.*(regular|vr)", t, re.I):
        rep.rhythm = "Broad-complex tachycardia — VT until proven otherwise"
        rep.urgency = "emergency"
        rep.findings.append("A regular broad-complex tachycardia in an "
                            "adult is VT even when the patient looks "
                            "well — treating it as SVB with verapamil "
                            "has killed patients.")
        rep.actions.append("DC cardioversion if compromised; amiodarone "
                           "or cardioversion if stable; expert review "
                           "before any calcium-channel blocker.")
        return rep

    if _stem(t, rep):
        return rep

    if re.search(r"irregularly irregular|no p waves.*irregular|"
                 r"absent p waves|atrial fibrillation|\baf\b with", t,
                 re.I) and "flutter" not in t.lower():
        rep.rhythm = "Atrial fibrillation"
        rate = ctx.get("ventricular_rate") or ctx.get("rate")
        fast = bool(rate and rate > 110) or \
            bool(re.search(r"fast|110|120|130|140|rvr", t, re.I))
        rep.urgency = "urgent" if fast else "routine"
        rep.findings.append("Irregularly irregular with absent P waves.")
        if fast:
            rep.findings.append("Rate-driven: control comes before "
                                "rhythm decisions today.")
        rep.actions.append("Rate or rhythm decision (stable/unstable "
                           "first), then the stroke question: "
                           "CHA2DS2-VASc before anticoagulation, and "
                           "the bleed risk does not cancel it — it "
                           "modifies it.")
        if ctx.get("chest_pain") or "chest pain" in t.lower():
            rep.urgency = "emergency"
            rep.actions.append("AF with chest pain or instability = "
                               "emergency department now.")
        return rep

    if re.search(r"complete heart block|third[- ]degree|"
                 r"(p waves?|qrs).*(dissociat|independent)", t, re.I):
        rep.rhythm = "Complete (third-degree) heart block"
        rep.urgency = "emergency"
        rep.findings.append("AV dissociation — atria and ventricles "
                            "beating independently.")
        rep.actions.append("Pacing: transcutaneous bridge while arranging "
                           "temporary then permanent pacing; atropine is "
                           "often useless in infranodal block.")
        return rep

    if re.search(r"mobitz ii|second[- ]degree.*2|second degree type 2",
                 t, re.I):
        rep.rhythm = "Second-degree AV block, Mobitz II"
        rep.urgency = "urgent"
        rep.actions.append("Pacing assessment today — Mobitz II can "
                           "progress to complete block without warning.")
        return rep

    if re.search(r"wenckebach|mobitz i", t, re.I):
        rep.rhythm = "Second-degree AV block, Mobitz I (Wenckebach)"
        rep.urgency = "routine"
        rep.findings.append("Usually vagal and benign — observe unless "
                            "symptomatic.")
        return rep

    if re.search(r"st depression|t inversion|dynamic changes|"
                 r"troponin.*rise", t, re.I):
        rep.rhythm = "Ischaemic changes without ST elevation"
        rep.urgency = "urgent"
        rep.actions.append("Treat as NSTEMI pathway until troponin says "
                           "otherwise: serial troponin, antiplatelets per "
                           "protocol, risk-score (GRACE) for timing.")
        return rep

    if re.search(r"\bnormal\b|unremarkable|nothing acute", t, re.I):
        rep.rhythm = "Described as normal"
        rep.urgency = "routine"
        rep.findings.append("A normal ECG does not exclude ACS — up to a "
                            "quarter of MIs have a first normal trace.")
        if ctx.get("chest_pain") or "chest pain" in t.lower():
            rep.urgency = "urgent"
            rep.actions.append("Normal ECG with ongoing chest pain: "
                               "serial ECGs + troponin, not discharge.")
        return rep

    rep.rhythm = "Pattern not recognised"
    rep.findings.append("No rule matched this description — describe the "
                        "rate, rhythm, axes, and ST/T segments, or take "
                        "the trace to someone who reads them daily.")
    rep.urgency = "urgent" if re.search(r"unstable|collapse|chest pain",
                                        t, re.I) else "routine"
    return rep
