"""Bloodborne-virus post-exposure decisions — HBIG inside 48 hours,
HIV PEP inside 72, hepatitis C with no PEP at all but a test plan.

Occupational needlestick, community needle, mucosal splash, broken
condom, sexual assault: the first dose is given on incomplete
information and the questions are sorted out afterwards. Local data
only; stdlib only.
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

_NEEDLESTICK = re.compile(
    r"needlestick|needle stick|sharps injury|stuck by a needle|"
    r"used needle|needle went through|jabbed myself with a needle|"
    r"stood on a needle|stepped on a needle|needle in the (?:park|grass|"
    r"bin|sand)", re.I)
_SPLASH = re.compile(
    r"blood splash\w* (?:in|into|to|onto)|splash of blood (?:in|into|"
    r"to|onto)|blood in my eye|blood in the eye|splashed my eye|"
    r"mucous membrane exposure", re.I)
_SEXUAL = re.compile(
    r"condom broke|condom split|condom came off|unprotected (?:sex|"
    r"intercourse|anal|vaginal)|sexually assault\w*|rape|"
    r"sexual assault", re.I)
_SOURCE_HBV = re.compile(r"hepatitis b positive|hb ?sag positive|"
                         r"known hepatitis b", re.I)
_SOURCE_HIV = re.compile(
    r"\bhiv positive|known hiv|with hiv\b|has hiv|source hiv|hiv\+", re.I)
_SOURCE_HCV = re.compile(r"hepatitis c positive|known hepatitis c", re.I)
_UNDETECTABLE = re.compile(r"undetectable|viral load (?:is |was )?zero|"
                           r"on treatment,? suppressed", re.I)
_HOURS = re.compile(
    r"(\d+)\s*(?:hours?|hrs?)\s*ago|"
    r"(\d+)\s*(?:days?|day)\s*ago|"
    r"this morning|last night|yesterday|just now")


@dataclass
class BloodborneAssessment:
    hiv_pep: bool = False
    hiv_note: str = ""
    hbv_pep: bool = False
    hbv_note: str = ""
    hcv_note: str = ""
    tests: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)


def _hours_ago(text: str) -> int:
    m = re.search(r"(\d+)\s*(?:hours?|hrs?)\s*ago", text, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*(?:days?|day)\s*ago", text, re.I)
    if m:
        return int(m.group(1)) * 24
    if re.search(r"this morning|just now", text, re.I):
        return 4
    if re.search(r"last night|yesterday", text, re.I):
        return 20
    return 6   # assume inside the window when unstated; assessment says so


def bloodborne_exposure(
        presentation: str, context: Optional[Dict] = None
) -> BloodborneAssessment:
    t = (presentation or "") + " " + " ".join(
        str(v) for v in (context or {}).values())
    a = BloodborneAssessment()
    hours = _hours_ago(t)

    occupational = bool(_NEEDLESTICK.search(t) or _SPLASH.search(t))
    sexual = bool(_SEXUAL.search(t))
    if not (occupational or sexual):
        a.hiv_note = ("No recognised bloodborne exposure in this "
                      "description — clarify what happened, to what "
                      "fluid, over what broken skin or membrane.")

    source_hiv = bool(_SOURCE_HIV.search(t))
    undetectable = bool(_UNDETECTABLE.search(t))

    # ---- HIV ----
    if source_hiv and undetectable:
        a.hiv_pep = False
        a.hiv_note = (
            "Source HIV positive but undetectable on treatment: "
            "transmission risk is effectively zero — PEP is not "
            "indicated. Baseline HIV test for the exposed person "
            "anyway, and document the decision.")
    elif (source_hiv or sexual or occupational) and hours < 72:
        a.hiv_pep = True
        a.hiv_note = (
            f"Exposure ~{hours}h ago, inside the 72-hour window: give "
            "the FIRST DOSE of HIV PEP now — a 28-day starter pack — "
            "and complete the risk assessment afterwards. The earlier "
            "the first dose, the better it works.")
    elif (source_hiv or sexual or occupational) and hours >= 72:
        a.hiv_pep = False
        a.hiv_note = (
            f"~{hours}h have passed: outside the 72-hour PEP window. "
            "Discuss with a specialist (exceptional cases are "
            "sometimes still offered), and arrange HIV testing at the "
            "appropriate interval instead.")
    elif occupational:
        # unknown low-risk community source
        a.hiv_pep = False
        a.hiv_note = (
            "Unknown community source: HIV PEP is usually not "
            "indicated (HIV prevalence in discarded needles is very "
            "low) — but HBV and tetanus DO need deciding today.")

    # ---- HBV ----
    if _SOURCE_HBV.search(t):
        a.hbv_pep = True
        a.hbv_note = (
            f"HBsAg-positive source, ~{hours}h ago: HBIG plus an "
            "accelerated hepatitis B vaccine course, ideally within 48 "
            "hours (works up to ~2 weeks). Check the exposed person's "
            "anti-HBs: a documented response ≥10 mIU/mL means no PEP "
            "needed.")
    elif occupational or sexual:
        a.hbv_note = (
            "Source HBV status unknown: check the exposed person's "
            "vaccine response (anti-HBs ≥10 = protected); give vaccine "
            "booster/HBIG per the table if unprotected and the source "
            "cannot be excluded.")

    # ---- HCV ----
    a.hcv_note = (
        "There is no PEP for hepatitis C. If the source is HCV "
        "positive or unknown-risk, test the exposed person: HCV RNA at "
        "6 weeks (antibody at 12) — and modern direct-acting antiviral "
        "treatment cures >95%, so a positive result is a treatment "
        "conversation, not a catastrophe.")

    # ---- baseline tests, always ----
    a.tests = [
        "Baseline now: HIV 4th-generation test, HBsAg + anti-HBs, HCV "
        "antibody, LFTs",
        "Repeat HIV test at 6 weeks (4th-gen) and 3 months",
        "HCV RNA at 6 weeks if source HCV-positive or unknown-risk",
        "Check anti-HBs vaccine response before deciding HBV PEP",
    ]

    a.questions = [
        "Exactly when did it happen (the HIV window is 72 hours)?",
        "What is known about the source — HIV, hepatitis B and C "
        "status, or a category you can risk-assign?",
        "Has the exposed person had hepatitis B vaccine, and do they "
        "have a documented antibody response?",
        "Tetanus status?",
    ]
    if sexual:
        a.questions += [
            "Emergency contraception needed (within 5 days)?",
            "Full STI screen at the appropriate window, chlamydia/"
            "gonorrhoea now and repeat later per protocol?",
        ]
        a.hiv_pep = a.hiv_pep or hours < 72
    return a
