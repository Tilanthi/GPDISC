"""UKMEC contraceptive eligibility table and emergency contraception
rules (sexual health, Stage 2). Categories: 1 = no restriction,
2 = benefits outweigh risks, 3 = risks usually outweigh benefits,
4 = unacceptable health risk. FSRH UKMEC 2016+ (as at 2026).
"""
from typing import Dict, List, Tuple

METHODS = ("cocp", "pop", "implant", "dmpa", "ius_iud")

UKMEC: Dict[Tuple[str, str], Tuple[int, str]] = {
    ("cocp", "migraine_with_aura"): (4, "Stroke risk — oestrogen absolutely contraindicated"),
    ("cocp", "smoker_35_plus_heavy"): (4, "Age >=35 smoking >=15/day: "
     "unacceptable - VTE + arterial risk; stop CHC"),
    ("cocp", "smoker_35_plus"): (3, "Age >=35 smoking <15/day: risks "
     "usually outweigh benefits - switch to progestogen-only"),
    ("cocp", "vte_history"): (4, "Oestrogen multiplies recurrence risk"),
    ("cocp", "bp_160_100"): (4, "Uncontrolled severe hypertension"),
    ("cocp", "breastfeeding_6wks"): (4, "Oestrogen suppresses lactation before 6 weeks"),
    ("cocp", "migraine_no_aura"): (3, "Continue only if no aura and no other risk factors"),
    ("cocp", "smoker_under_35"): (2, "Counsel; VTE risk acceptable if no other factors"),
    ("cocp", "bmi_35"): (3, "VTE risk rises steeply >=35; POP/implant preferred"),
    ("cocp", "controlled_htn"): (3, "Risk usually outweighs benefit — progestogen-only preferred"),
    ("pop", "breastfeeding_6wks"): (2, "Compatible with lactation"),
    ("pop", "vte_history"): (2, "Progestogen-only does not raise VTE risk meaningfully"),
    ("pop", "migraine_with_aura"): (1, "No oestrogen — safe with aura"),
    ("implant", "breastfeeding_6wks"): (2, "Compatible"),
    ("implant", "vte_history"): (1, "Safe"),
    ("implant", "unspecified_vaginal_bleeding"): (3, "Investigate before insertion"),
    ("dmpa", "bmi_30"): (2, "Counsel on weight gain + bone density with >2y use"),
    ("dmpa", "osteoporosis_risk"): (3, "Bone mineral density concern with prolonged use"),
    ("ius_iud", "pregnancy"): (4, "Never insert in pregnancy"),
    ("ius_iud", "pid_current"): (4, "Treat infection first — insertion risks spread"),
    ("ius_iud", "unspecified_vaginal_bleeding"): (3, "Investigate before insertion"),
}


def ukmec_category(method: str, condition: str) -> Tuple[int, str]:
    """Category for (method, condition); (0, "no rule") when unmatched —
    0 means use clinical judgement, not 'safe'."""
    return UKMEC.get((method, condition), (0, "no rule"))


def safe_methods(condition: str) -> List[str]:
    """Methods explicitly rated category 1-2 for this condition.
    Only explicit rows are listed; absence means 'no specific rule'."""
    return [m for m in METHODS
            if UKMEC.get((m, condition), (99, ""))[0] in (1, 2)]


def emergency_contraception(hours_since_upsi: float, bmi: float = 0,
                            wants_ongoing: bool = False) -> dict:
    """Copper IUD is the most effective EC at any BMI and acts up to 120h.
    Ulipristal acetate: licensed 0-120h, less effective BMI >=26 (still usable).
    Levonorgestrel: licensed 0-72h, less effective BMI >=26; doubling the
    dose is an option but ulipristal/IUD are preferred."""
    options = []
    if hours_since_upsi <= 120:
        options.append({"method": "Copper IUD", "effectiveness": "99.9%",
                        "note": "Most effective at any BMI; acts up to 120h; "
                                "also provides ongoing contraception",
                        "first_line": True})
    if hours_since_upsi <= 120:
        eff = "reduced if BMI >=26" if bmi >= 26 else "good"
        options.append({"method": "Ulipristal acetate 30mg",
                        "effectiveness": eff,
                        "note": "Single dose; avoid with enzyme-inducers; "
                                "not with breastfeeding; wait 5 days before "
                                "starting hormonal contraception",
                        "first_line": False})
    if hours_since_upsi <= 72:
        eff = ("reduced if BMI >=26 (consider double dose, but prefer "
               "ulipristal/IUD)" if bmi >= 26 else "good")
        options.append({"method": "Levonorgestrel 1.5mg", "effectiveness": eff,
                        "note": "Safe in breastfeeding; re-dose if vomit <3h; "
                                "can quick-start ongoing contraception next day",
                        "first_line": False})
    return {
        "options": options,
        "recommendation": ("Copper IUD" if hours_since_upsi <= 120
                           else "None in-window — discuss referral"),
        "advise": "Pharmacy access free of charge; pregnancy test if no period "
                  "within 3 weeks",
        "ongoing": "Quick-start LARC discussion recommended" if wants_ongoing else "",
    }
