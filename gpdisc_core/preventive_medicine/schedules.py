"""UK vaccination schedule (adult-relevant slice) — preventive medicine
Stage 2. Cohorts follow the UK national immunisation programme (NHS/
UKHSA) as at 2026. Local data only.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class VaccineEntry:
    vaccine: str
    cohort: str
    schedule_notes: str


VACCINES_UK = [
    VaccineEntry("Influenza (annual)",
        "65+, under-65 risk groups (CKD, cardiac, respiratory, diabetes, "
        "immunosuppressed, pregnancy, BMI>=40, care home)",
        "Every year, September onwards"),
    VaccineEntry("COVID-19 (seasonal)",
        "75+, immunosuppressed, care home residents, housebound",
        "Per JCVI seasonal campaign"),
    VaccineEntry("Pneumococcal (PPV23)",
        "65+, or >=2y with risk condition",
        "Single dose at 65; every 5y if immunosuppressed/splenectomy"),
    VaccineEntry("Shingles (Shingrix)",
        "60-70 programme band (expanding), severely immunosuppressed 50+",
        "2 doses 8 weeks-12 months apart"),
    VaccineEntry("Pertussis (whooping cough)",
        "Pregnant women, from 16 weeks gestation",
        "Every pregnancy, ideally 16-32 weeks"),
    VaccineEntry("RSV",
        "Pregnant 28+ weeks (seasonal), adults 75-79",
        "Single dose programme"),
    VaccineEntry("Hepatitis B (infants)",
        "All infants born in UK (universal since 2017), plus risk groups",
        "Birth dose then 6-in-1 schedule"),
    VaccineEntry("MMR (2 doses)",
        "Anyone without 2 documented doses",
        "Check at 25+ health checks, travel, pre-registration"),
    VaccineEntry("Tdap/IPV booster",
        "70+ (at 70), pregnant (from 16w as part of pertussis)",
        "Once at 70; each pregnancy"),
    VaccineEntry("MenACWY",
        "Adolescents (school year 9-10), university freshers <=25y who missed",
        "Single dose"),
    VaccineEntry("HPV",
        "Girls and boys 12-13, MSM up to 45 via clinics",
        "1 dose <25y (JCVI 2021); 2 doses if older/immunosuppressed"),
    VaccineEntry("Bexsero (MenB)",
        "Infants; catch-up for at-risk",
        "2+1 schedule"),
]


def vaccine_due(entry: VaccineEntry, patient: dict) -> bool:
    """Cohort predicates for the adult-relevant slice of the schedule."""
    age = patient.get("age_years")
    p = patient
    if entry.vaccine.startswith("Influenza"):
        return age is not None and (age >= 65 or p.get("immunosuppressed")
                                    or p.get("pregnant") or p.get("diabetes"))
    if entry.vaccine.startswith("COVID"):
        return age is not None and (age >= 75 or p.get("immunosuppressed"))
    if entry.vaccine.startswith("Pneumococcal"):
        return age is not None and (age >= 65 or p.get("immunosuppressed"))
    if entry.vaccine.startswith("Shingles"):
        return age is not None and 60 <= age <= 70
    if entry.vaccine.startswith("Pertussis"):
        return bool(p.get("pregnant"))
    if entry.vaccine.startswith("RSV"):
        return (bool(p.get("pregnant")) and p.get("gestation_weeks", 0) >= 28) or (
            age is not None and 75 <= age <= 79)
    if entry.vaccine.startswith("Hepatitis B"):
        return False  # infant programme — not adult recall
    if entry.vaccine.startswith("MMR"):
        return age is not None and age >= 25 and not p.get("mmr_two_doses")
    if entry.vaccine.startswith("Tdap"):
        return (age is not None and age >= 70) or bool(p.get("pregnant"))
    if entry.vaccine.startswith("MenACWY"):
        return False  # adolescent/university programme — captured opportunistically
    if entry.vaccine.startswith("HPV"):
        return False  # school programme
    if entry.vaccine.startswith("Bexsero"):
        return False  # infant programme
    return False
