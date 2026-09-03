"""STI screening panels and keyword routing (sexual health, Stage 2).
Local data only.
"""
from typing import List, Tuple

STI_PANELS = {
    "asymptomatic_screen": [
        "Chlamydia + gonorrhoea NAAT",
        "HIV 4th-gen ag/ab",
        "Syphilis serology",
        "Hepatitis B (if unvaccinated/risk)",
        "Hepatitis C if risk",
    ],
    "symptomatic_male_discharge": [
        "Urethral NAAT GC/CT",
        "HIV + syphilis serology",
        "MC&S urethral discharge (gonococcus culture)",
        "First-void urine NAAT",
    ],
    "symptomatic_female_pelvic_pain": [
        "NAAT GC/CT (self-taken vaginal)",
        "HIV + syphilis",
        "Urine dip + MSU",
        "Pregnancy test (ectopic/PID distinction)",
        "Swab for TV/BV/candida; endocervical culture if PID suspected",
    ],
    "genital_ulcer": [
        "HSV PCR + syphilis serology",
        "HIV test",
        "NAAT GC/CT",
        "Consider LGV serology if perianal/MSM",
    ],
    "pregnant_screen": [
        "HIV, syphilis, hepatitis B (routine antenatal)",
        "NAAT GC/CT if <25y or risk",
        "Hepatitis C if risk",
    ],
}


def panel_for(text: str) -> Tuple[str, List[str]]:
    """Route a presentation to the right panel. Symptom routing beats
    screening intent — the pregnancy test inside the pelvic-pain panel
    is the safety-critical part."""
    t = (text or "").lower()
    if any(w in t for w in ["ulcer", "sore on", "chancre", "genital sore"]):
        return "genital_ulcer", list(STI_PANELS["genital_ulcer"])
    if "discharge" in t and any(w in t for w in ["penis", "urethral", "penile"]):
        return "symptomatic_male_discharge", list(STI_PANELS["symptomatic_male_discharge"])
    if any(w in t for w in ["pelvic", "lower abdominal", "lower tummy"]) and \
            "pain" in t:
        return ("symptomatic_female_pelvic_pain",
                list(STI_PANELS["symptomatic_female_pelvic_pain"]))
    if "pregnan" in t:
        return "pregnant_screen", list(STI_PANELS["pregnant_screen"])
    return "asymptomatic_screen", list(STI_PANELS["asymptomatic_screen"])
