"""GPDISC post-exposure prophylaxis package (expertise program Stage 6,
Task 6.8): rabies, hepatitis B and HIV PEP decisions — all window-
aware, all answerable with incomplete information, because the first
dose is always given before the story is complete. Local data only.
"""
import re
from typing import Dict, Optional

from .rabies import rabies_pep, RabiesAssessment          # noqa: F401
from .bloodborne import (                                  # noqa: F401
    bloodborne_exposure, BloodborneAssessment,
)

_BITE_PATHWAY = re.compile(
    r"\bbitten\b|\bbite\b|bite wound|scratched|scratch from|"
    r"\bbats?\b|animal saliva|licked and (?:broke|cut)", re.I)
_BLOOD_PATHWAY = re.compile(
    r"needlestick|needle stick|sharps|used needle|needle|"
    r"blood splash|splash of blood|blood in (?:my|the) eye|"
    r"condom (?:broke|split|came off)|sexually assault\w*|rape|"
    r"hepatitis [bc] positive source|unprotected", re.I)


def pep_screen(presentation: str,
               context: Optional[Dict] = None) -> Dict:
    """Route a possible-exposure presentation to its PEP pathway.

    Returns {"pathway": "rabies" | "bloodborne" | "none", ...} with the
    matching assessment object attached under "assessment".
    """
    t = (presentation or "") + " " + " ".join(
        str(v) for v in (context or {}).values())
    if _BITE_PATHWAY.search(t):
        return {"pathway": "rabies",
                "assessment": rabies_pep(presentation, context)}
    if _BLOOD_PATHWAY.search(t):
        return {"pathway": "bloodborne",
                "assessment": bloodborne_exposure(presentation, context)}
    return {"pathway": "none",
            "note": ("No post-exposure pathway matched. If there was a "
                     "bite, a needle, a splash, or an unprotected "
                     "exposure, say so explicitly — these decisions are "
                     "measured in hours.")}

__all__ = [
    "rabies_pep", "RabiesAssessment",
    "bloodborne_exposure", "BloodborneAssessment",
    "pep_screen",
]
