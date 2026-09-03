"""Urgent suspected cancer (2ww) referral criteria — NICE NG12-aligned.

Expertise program Stage 3, Task 2. Each rule is a symptom/finding trigger
with the age (and sex) at which it crosses the 2ww threshold in UK primary
care. Age floors of None mean "any adult age" (dysphagia, skin, oral,
lymphadenopathy). Thresholds are guidance-era 2026 — always check the
current NG12 pathway before referring.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class TwoWeekWaitRule:
    """One 2ww trigger: presentation phrase(s), age/sex gate, action."""
    cancer_site: str
    trigger: List[str] = field(default_factory=list)
    age_floor: Optional[int] = None   # None = any adult age
    sex: Optional[str] = None         # None = any sex; "f"/"m" restricts
    action: str = ""


_ROWS = [
    ("lung", ["haemoptysis", "coughing up blood", "chest x-ray suspicious",
              "chest xray suspicious", "abnormal chest x-ray"], 40, None,
     "Chest X-ray + urgent suspected cancer referral (2ww); a normal X-ray "
     "does not exclude cancer if suspicion persists clinically"),
    ("lung", ["persistent cough", "recurrent chest infection"], 40, None,
     "Chest X-ray; if persistent >3 weeks with risk factors → 2ww"),
    ("colorectal", ["rectal bleeding"], 50, None,
     "Unexplained rectal bleeding ≥50 → 2ww lower GI"),
    ("colorectal", ["iron deficiency anaemia", "ida", "change in bowel habit",
                    "altered bowel habit"], 60, None,
     "Unexplained change in bowel habit or iron-deficiency anaemia ≥60 → "
     "2ww + FIT as directed"),
    ("colorectal", ["weight loss"], 40, None,
     "≥40 with weight loss + abdominal pain → 2ww"),
    ("oesophago_gastric", ["dysphagia", "difficulty swallowing",
                           "food sticking"], None, None,
     "Dysphagia at ANY adult age → urgent direct-access endoscopy (2ww)"),
    ("oesophago_gastric", ["dyspepsia", "upper abdominal pain", "epigastric pain",
                           "refractory dyspepsia"], 55, None,
     "≥55 with new dyspepsia + weight loss → 2ww upper GI"),
    ("breast", ["breast lump", "breast mass"], 30, None,
     "Breast lump ≥30 (any age if skin/nipple change) → 2ww breast clinic"),
    ("breast", ["nipple eczema", "nipple discharge blood", "unilateral nipple"], 30, "f",
     "Unilateral eczematous nipple change or bloodstained discharge → 2ww"),
    ("ovarian", ["bloating persistent", "abdominal distension", "early satiety",
                 "feeling full quickly", "pelvic pain"], 50, "f",
     "≥50 with persistent bloating/distension/satiety/pelvic pain → "
     "CA125 + ultrasound pathway"),
    ("bladder", ["visible haematuria", "blood in my urine", "frank haematuria"], 45, None,
     "Unexplained visible haematuria ≥45 → 2ww urology"),
    ("bladder", ["recurrent urinary tract infection", "persistent urinary tract infection",
                 "recurrent cystitis"], 60, None,
     "≥60 unexplained recurrent/persistent UTI → 2ww (bladder)"),
    ("prostate", ["prostate symptoms", "urinary difficulty man",
                  "weak urine stream man"], 50, "m",
     "Men ≥50 with LUTS → consider PSA + DRE; counsel about PSA's limits first"),
    ("skin", ["changing mole", "bleeding mole", "new mole", "skin lesion suspicious",
              "non-healing skin lesion"], None, None,
     "Suspicious pigmented lesion (ABCDEF / dermoscopy) → 2ww skin; photograph it"),
    ("oral", ["mouth ulcer not healing", "oral ulcer for 3 weeks",
              "non-healing mouth ulcer", "mouth ulcer that won't heal"], None, None,
     "Any oral ulcer/patch >3 weeks → 2ww head & neck"),
    ("haematological", ["persistent lymph nodes", "persistent swollen glands",
                        "lymphadenopathy persistent"], None, None,
     "Persistent (>6 weeks) non-tender lymphadenopathy → 2ww haematological; "
     "check FBC + LDH first"),
]


def _build() -> List[TwoWeekWaitRule]:
    return [TwoWeekWaitRule(cancer_site=site, trigger=list(trig),
                            age_floor=age, sex=sex, action=action)
            for (site, trig, age, sex, action) in _ROWS]


TWO_WEEK_WAIT_RULES: List[TwoWeekWaitRule] = _build()


def two_week_wait_check(text: str, age: Optional[int] = None,
                        sex: Optional[str] = None) -> List[TwoWeekWaitRule]:
    """Return 2ww rules whose trigger phrases appear in the presentation,
    filtered by age floor and (when the rule is sex-restricted) patient sex.

    A rule fires when: a trigger phrase matches the text AND the patient is
    old enough (rules with age_floor=None apply at any age) AND the rule's
    sex restriction (if any) matches the patient's sex. If patient sex is
    unknown (None), sex-restricted rules still fire — the caller confirms.
    """
    t = text.lower()
    hits: List[TwoWeekWaitRule] = []
    for rule in TWO_WEEK_WAIT_RULES:
        if not any(phrase in t for phrase in rule.trigger):
            continue
        if rule.age_floor is not None:
            if age is None or age < rule.age_floor:
                continue
        if rule.sex is not None and sex is not None and sex != rule.sex:
            continue
        hits.append(rule)
    return hits
