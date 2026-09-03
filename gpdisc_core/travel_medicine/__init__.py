"""GPDISC travel medicine package (expertise program Stage 2).

Pre-travel risk assessment (destination malaria/vaccine tables,
traveller-history-aware chemoprophylaxis) and post-travel screening
protocols. Local-only; no external data sources.
"""
from .destinations import (
    DestinationRisk,
    DESTINATIONS,
    find_destination,
)
from .prophylaxis import (
    ProphylaxisOption,
    TravelPlan,
    OPTIONS_ALL,
    recommend_prophylaxis,
    pre_travel_consult,
)
from .post_travel import post_travel_screening

__all__ = [
    "DestinationRisk",
    "DESTINATIONS",
    "find_destination",
    "ProphylaxisOption",
    "TravelPlan",
    "OPTIONS_ALL",
    "recommend_prophylaxis",
    "pre_travel_consult",
    "post_travel_screening",
]
