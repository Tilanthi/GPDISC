"""Malaria chemoprophylaxis selection and pre-travel consult assembly
(travel medicine, Stage 2). Contraindication logic mirrors UKHSA
malaria prevention guidance for travellers from the UK.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .destinations import DestinationRisk, find_destination


@dataclass
class ProphylaxisOption:
    drug: str
    regimen: str
    pros: str
    contraindications: List[str] = field(default_factory=list)


@dataclass
class TravelPlan:
    destination: str
    malaria: Dict
    vaccines: List[Dict]
    certificate: str
    general: List[str]


OPTIONS_ALL = [
    ProphylaxisOption("Atovaquone/proguanil",
        "1 tablet daily; start 1-2 days before, continue 7 days after leaving",
        "Well tolerated; short courses; good for last-minute",
        ["Not recommended in pregnancy (avoid as precaution)",
         "Caution severe renal impairment",
         "Long-term use needs annual review (acceptable to 1 year+)"]),
    ProphylaxisOption("Doxycycline",
        "100mg daily; start 1-2 days before, continue 4 weeks after leaving",
        "Cheap; also covers rickettsia/leptospirosis; good for long trips",
        ["Age <12 years", "Pregnancy/breastfeeding",
         "Photosensitivity — sunscreen SPF50",
         "Oesophagitis — take upright with water"]),
    ProphylaxisOption("Mefloquine",
        "250mg weekly; start 2-3 weeks before, continue 4 weeks after leaving",
        "Weekly suits erratic compliance; long trips",
        ["History of psychosis, depression with suicide risk, or epilepsy — ABSOLUTE",
         "Neuropsychiatric side effects (vivid dreams to psychosis)",
         "Not for diver/pilot safety-critical roles"]),
    ProphylaxisOption("Chloroquine", "300mg base weekly",
        "Only where resistance absent (nowhere in sub-Saharan Africa)",
        ["Not for chloroquine-resistant areas", "Retinal toxicity >5 years cumulative"]),
]


def recommend_prophylaxis(destination: DestinationRisk,
                          traveller: Optional[Dict] = None) -> List[ProphylaxisOption]:
    """Options for this destination filtered by traveller history."""
    if destination.malaria_risk == "none":
        return []
    t = traveller or {}
    out = []
    for opt in OPTIONS_ALL:
        if opt.drug == "Chloroquine" and destination.chloroquine_resistance:
            continue
        if opt.drug == "Mefloquine" and (t.get("psychiatric_history") or t.get("epilepsy")):
            continue
        if opt.drug == "Doxycycline" and (
                t.get("pregnant") or t.get("breastfeeding")
                or (t.get("age_years") is not None and t["age_years"] < 12)):
            continue
        if opt.drug == "Atovaquone/proguanil" and t.get("pregnant"):
            continue
        out.append(opt)
    return out


def pre_travel_consult(destinations_text: str, traveller: Optional[Dict] = None,
                       duration_weeks: int = 2) -> TravelPlan:
    dest = find_destination(destinations_text)
    if dest is None:
        return TravelPlan(
            destination="",
            malaria={"risk": "unknown",
                     "recommendation": "Destination not recognised — look up via "
                                       "TravelHealthPro/NaTHNaC country pages"},
            vaccines=[], certificate="",
            general=_general_advice())

    options = recommend_prophylaxis(dest, traveller)
    malaria = {
        "risk": dest.malaria_risk,
        "falciparum": dest.p_falciparum,
        "recommendation": (
            "Awareness, Bite avoidance (DEET 50%, nets, dusk-to-dawn), "
            "Chemoprophylaxis, Diagnosis promptly if fever" if options
            else "No chemoprophylaxis indicated — bite avoidance and fever "
                 "awareness still apply"),
        "options": [{"drug": o.drug, "regimen": o.regimen, "pros": o.pros,
                     "contraindications": o.contraindications} for o in options],
        "notes": dest.notes,
    }
    vaccines = [{"vaccine": v,
                 "reason": _vaccine_reason(v),
                 "when": "ideally 4-6 weeks pre-travel (some courses accelerate)"}
                for v in dest.vaccines_recommended]
    return TravelPlan(destination=dest.destination_id, malaria=malaria,
                      vaccines=vaccines, certificate=dest.certificate,
                      general=_general_advice())


def _vaccine_reason(v: str) -> str:
    if v.startswith("yellow_fever"):
        return "Entry requirement and/or mosquito-borne haemorrhagic risk in zone"
    if v.startswith("typhoid"):
        return "Food/water hygiene variable — typhoid is common in the region"
    if v.startswith("hepatitis_a"):
        return "Food/water borne — universal recommendation for most destinations"
    if v.startswith("hepatitis_b"):
        return "Blood-borne/sexual exposure; universal for most travellers"
    if v.startswith("rabies"):
        return "Rabies is endemic; pre-exposure course if remote/animal contact likely"
    if v.startswith("meningococcal"):
        return "Meningococcal ACWY — belt country or mass-gathering (Hajj) requirement"
    if v.startswith("japanese_encephalitis"):
        return "Rural rice-area mosquito exposure, especially >1 month or outbreaks"
    if v.startswith("polio"):
        return "Polio-exporting country — adult 10-year booster"
    if v.startswith("influenza"):
        return "Mass gathering / Southern-hemisphere season timing"
    return "Region-specific risk"


def _general_advice() -> List[str]:
    return [
        "Travel insurance including medical evacuation — check it covers the activities",
        "Regular medication in hand luggage + a doctor's letter for controlled drugs",
        "Traveller's diarrhoea kit: ORS, loperamide, stand-by antibiotic per GP advice",
        "Bite avoidance: DEET 50%, long sleeves dusk-to-dawn, impregnated bed nets",
        "Safe sex advice and condoms — STI/HIV risk varies by region",
        "Sun protection and altitude awareness where relevant",
    ]
