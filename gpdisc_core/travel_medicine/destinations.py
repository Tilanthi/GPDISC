"""Destination malaria/vaccine risk table (travel medicine, Stage 2).

Risk categories and vaccine recommendations follow UKHSA/NaTHNaC travel
health guidance as at 2026; certificate rules reflect entry requirements.
All data local-only.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DestinationRisk:
    destination_id: str              # canonical id e.g. "ghana"
    aliases: List[str]               # lowercase matching strings
    region: str                      # "West Africa" etc.
    malaria_risk: str                # "none" | "low" | "high"
    p_falciparum: bool               # falciparum present
    chloroquine_resistance: bool
    vaccines_recommended: List[str]  # beyond routine UK immunisations
    certificate: str                 # "" | "yellow_fever" | "meningococcal_acwy_hajj"
    notes: str


# (id, aliases, region, malaria_risk, falciparum, chloroquine_resistance,
#  vaccines_recommended, certificate, notes)
_ROWS = [
    ("ghana", ["ghana", "accra"], "West Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)",
      "meningococcal_acwy"],
     "yellow_fever",
     "YF certificate required for entry; malaria all regions including Accra."),
    ("nigeria", ["nigeria", "lagos", "abuja"], "West Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "meningococcal_acwy"],
     "yellow_fever", "High YF risk + Lassa fever zones; strict bite avoidance."),
    ("kenya", ["kenya", "nairobi", "mombasa"], "East Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "yellow_fever",
     "Nairobi >2500m lower risk; coast and west high risk."),
    ("tanzania", ["tanzania", "kilimanjaro", "dar es salaam", "zanzibar"],
     "East Africa", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b"],
     "yellow_fever",
     "Zanzibar lower but non-zero; Kilimanjaro altitude needs acclimatisation plan."),
    ("gambia", ["gambia", "the gambia", "senegal", "dakar"], "West Africa",
     "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a"], "yellow_fever",
     "Coastal strip high risk."),
    ("uganda", ["uganda", "kampala", "rwanda", "kigali"], "East Africa",
     "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b",
      "ebola screening (region)"],
     "yellow_fever",
     "YF certificate required; eastern DRC border regions check outbreaks."),
    ("india", ["india", "delhi", "mumbai", "goa", "kolkata"], "South Asia",
     "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)",
      "japanese_encephalitis (rural/long-stay)"],
     "", "Goa/coast low risk; Assam and east higher; rabies decision is the big one here."),
    ("thailand", ["thailand", "bangkok", "phuket", "chiang mai"], "Southeast Asia",
     "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)",
      "japanese_encephalitis (rural)"],
     "", "Major cities minimal risk; borders with Myanmar/Cambodia higher."),
    ("vietnam", ["vietnam", "hanoi", "ho chi minh", "mekong"], "Southeast Asia",
     "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "japanese_encephalitis (rural)"],
     "", "Mekong delta higher risk; cities low."),
    ("cambodia", ["cambodia", "siem reap", "angkor"], "Southeast Asia",
     "high", True, True,
     ["typhoid", "hepatitis_a"], "", "Forest areas high risk."),
    ("laos", ["laos", "luang prabang", "vyentiane", "vientiane"], "Southeast Asia",
     "high", True, True,
     ["typhoid", "hepatitis_a"], "", "Remote forest areas; medical access poor."),
    ("myanmar", ["myanmar", "burma", "yangon"], "Southeast Asia", "high", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b"], "",
     "Politics affect medical evacuation cover."),
    ("indonesia", ["indonesia", "bali", "jakarta", "borneo", "komodo"],
     "Southeast Asia", "low", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (Bali specifically)"],
     "", "Bali rabies deaths in unvaccinated travellers; Java rural areas risk malaria."),
    ("philippines", ["philippines", "manila", "palawan"], "Southeast Asia",
     "low", True, True,
     ["typhoid", "hepatitis_a"], "", "Palawan and Mindanao higher risk."),
    ("malaysia_borneo", ["borneo", "sabah", "sarawak", "malaysian borneo"],
     "Southeast Asia", "high", True, True,
     ["typhoid", "hepatitis_a"], "", "Sabah interior high risk; peninsula low."),
    ("sri_lanka", ["sri lanka", "colombo", "kandy"], "South Asia", "none",
     False, False,
     ["typhoid", "hepatitis_a", "rabies (consider)"], "",
     "Malaria-FREE (WHO-certified 2016; zero indigenous cases since 2012) — "
     "no prophylaxis needed. Dengue is the real vector risk, year-round."),
    ("bangladesh", ["bangladesh", "dhaka"], "South Asia", "high", True, True,
     ["typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "", "High typhoid + cholera risk; medical access limited outside Dhaka."),
    ("pakistan", ["pakistan", "karachi", "islamabad", "lahore"], "South Asia",
     "low", True, True,
     ["typhoid", "hepatitis_a", "polio booster"], "",
     "Polio exportation country — adult booster if <10 years."),
    ("brazil_amazon", ["amazon", "manaus", "brazil amazon", "the amazon"],
     "South America", "high", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a", "hepatitis_b", "rabies (consider)"],
     "yellow_fever",
     "YF certificate for Amazon travel; coastal Brazil malaria-free."),
    ("peru", ["peru", "cusco", "machu picchu", "lima"], "South America",
     "low", True, True,
     ["yellow_fever (Amazon basin only)", "typhoid", "hepatitis_a",
      "rabies (consider)"],
     "yellow_fever",
     "Cusco/Machu Picchu: altitude sickness plan (acetazolamide consider); "
     "Lima malaria-free."),
    ("bolivia", ["bolivia", "la paz"], "South America", "low", True, True,
     ["yellow_fever (lowlands)", "typhoid", "hepatitis_a"],
     "yellow_fever", "La Paz extreme altitude 3600m+; lowland YF risk."),
    ("colombia_venezuela", ["colombia", "venezuela", "cartagena", "bogota"],
     "South America", "low", True, True,
     ["yellow_fever", "typhoid", "hepatitis_a"], "yellow_fever",
     "Atlantic coast malaria-free; inland <1700m risk."),
    ("mexico", ["mexico", "cancun", "mexico city", "oaxaca", "chiapas"],
     "Central America", "low", True, True,
     ["typhoid", "hepatitis_a"], "",
     "Cancun/resorts malaria-free; Chiapas/Oaxaca rural risk."),
    ("saudi_hajj", ["hajj", "umrah", "mecca", "medina", "saudi arabia"],
     "Middle East", "none", False, False,
     ["meningococcal_acwy", "influenza", "hepatitis_b"],
     "meningococcal_acwy_hajj",
     "ACWY certificate mandatory within 3-5 years for Hajj/Umrah visa; no malaria."),
]


def _build(rows) -> List[DestinationRisk]:
    return [DestinationRisk(
        destination_id=r[0], aliases=r[1], region=r[2], malaria_risk=r[3],
        p_falciparum=r[4], chloroquine_resistance=r[5], vaccines_recommended=r[6],
        certificate=r[7], notes=r[8]) for r in rows]


DESTINATIONS = _build(_ROWS)


def find_destination(text: str) -> Optional[DestinationRisk]:
    """Match free text against destination aliases (substring, lowercase)."""
    t = (text or "").lower()
    for d in DESTINATIONS:
        if any(a in t for a in d.aliases):
            return d
    return None
