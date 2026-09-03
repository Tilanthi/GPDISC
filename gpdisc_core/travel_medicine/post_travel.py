"""Post-travel screening protocol (travel medicine, Stage 2).

Deterministic rules driven by the destination table plus exposure
keywords in the trip description. Serology timing windows matter:
schistosoma serology is falsely negative before 6-12 weeks.
"""
from typing import Dict, List, Optional

from .destinations import find_destination


def post_travel_screening(trip_text: str, traveller: Optional[Dict] = None) -> List[dict]:
    """Asymptomatic returnee screening plan: list of {test, reason, when}."""
    t = trip_text.lower()
    dest = find_destination(trip_text)
    out = []
    out.append({"test": "FBC with differential (eosinophils)",
                "reason": "Eosinophilia is the screening flag for worm burden in any "
                          "returning traveller",
                "when": "now"})
    if dest is not None and dest.malaria_risk != "none":
        out.append({"test": "Malaria: only if febrile — films x3 same day",
                    "reason": f"{dest.region} is malarious; asymptomatic screening "
                              "bloods have no role",
                    "when": "if fever develops (any time up to 6 months)"})
    if any(w in t for w in ["swam", "swimming", "lake", "river", "waded",
                            "rafting", "snorkel"]):
        out.append({"test": "Schistosoma serology",
                    "reason": "Freshwater exposure — Katayama/chronic schistosomiasis",
                    "when": "6-12 weeks after last exposure (earlier is falsely negative)"})
        out.append({"test": "Strongyloides serology",
                    "reason": "Soil/water exposure in tropics; must be excluded before "
                              "any immunosuppression",
                    "when": "now"})
    if dest is not None and dest.region in ("West Africa", "East Africa"):
        out.append({"test": "HIV + syphilis + hepatitis B screen",
                    "reason": "Regional prevalence + occupational/sexual exposure "
                              "often undisclosed",
                    "when": "at least 4 weeks after return (window period)"})
    if dest is not None and any(w in t for w in ["long", "months", "volunteer",
                                                 "worked", "working"]):
        out.append({"test": "TB: IGRA (interferon-gamma release assay)",
                    "reason": "Prolonged stay in high-prevalence setting",
                    "when": "8-12 weeks after return"})
    out.append({"test": "Review any fever within 6 months of return",
                "reason": "Malaria (vivax) presents months late; always mention the "
                          "trip to any clinician",
                "when": "standing safety advice"})
    return out
