"""Benign-versus-emergency discrimination pairs.

Stage 5, Task 2. The expertise Glenn called out by name: "particularly
strong at distinguishing benign presentations from emergencies". Each pair
holds the benign twin and the emergency twin of one presentation, with the
specific discriminators that separate them — the pairs run against the
live SafetyLayer in tests, so the discrimination is verified behaviour,
not prose.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class DiscriminationPair:
    benign_presentation: str
    emergency_presentation: str
    benign_condition: str
    emergency_condition: str
    discriminators: List[str] = field(default_factory=list)


_ROWS = [
    ("mild bilateral headache coming on over days after stress",
     "worst headache of my life instantly like a blow an hour ago, vomiting",
     "tension_headache", "sah_subarachnoid",
     ["Speed of onset (seconds vs days)", "Severity: 'worst ever'",
      "Vomiting, neck stiffness, photophobia",
      "Thunderclap = SAH until excluded"]),
    ("musculoskeletal chest pain, tender rib, worse on movement after the gym",
     "crushing central chest pain 30 minutes, sweating, radiating to left arm",
     "musculoskeletal_chest_pain", "acs_stemi",
     ["Exertional vs movement-related", "Autonomic sweating points to ACS",
      "Reproducible tenderness points musculoskeletal",
      "Duration and crescendo pattern"]),
    ("simple faint in a hot room after standing, minutes of warning",
     "blackout with no warning while sitting, palpitations just before",
     "vasovagal_syncope", "cardiac_syncope",
     ["Prodrome (hot, dizzy, vision greying) vs none",
      "Trigger (standing, heat) vs any position",
      "Palpitations before = arrhythmia until proved otherwise"]),
    ("gastroenteritis, cramping pain with diarrhoea that is settling",
     "severe constant abdominal pain out of proportion, no diarrhoea, "
     "distended and very tender",
     "gastroenteritis", "acute_mesenteric_ischaemia",
     ["Pain out of proportion to examination findings",
      "Constant vs colicky", "Blood in stool; AF history raises risk",
      "Rapid deterioration over hours"]),
    ("panic attack with tingling fingers and breathlessness in a young adult",
     "sudden breathlessness with sharp pleuritic pain and a swollen calf "
     "after a long flight",
     "panic_attack", "pe_pulmonary_embolism",
     ["Calf swelling / immobility / recent surgery (PE risk factors)",
      "Pleuritic pain and haemoptysis",
      "Tingling fingers and hyperventilation pattern (panic)"]),
    ("reactive neck node after a sore throat, small and tender",
     "painless hard neck lump enlarging over six weeks with night sweats",
     "lymphadenopathy_reactive", "lymphoma_suspect",
     ["Tender + small + recent (reactive) vs painless + progressive",
      "Night sweats, weight loss, itch",
      "Persistence beyond 6 weeks = urgent suspected cancer pathway"]),
    ("simple lower back pain after lifting, moving freely, no neurology",
     "back pain with numbness in the saddle area and can't pass urine",
     "back_pain_mechanical", "cauda_equina",
     ["Urinary retention or incontinence", "Saddle anaesthesia",
      "Bilateral leg weakness",
      "Constipation from any cause does NOT exclude it"]),
    ("young adult vertigo on head movement lasting seconds at a time",
     "sudden continuous vertigo with double vision, slurred speech and "
     "one-sided weakness",
     "bppv", "stroke_tia",
     ["Positional and seconds-long (BPPV) vs continuous",
      "ANY other neurological sign alongside the vertigo",
      "First-ever headache with vertigo is vascular until excluded"]),
    ("child with fever and a blanching viral rash, drinking normally",
     "3 year old with fever and a rash that does not fade when pressed, "
     "drowsy with cold hands",
     "viral_rash_child", "meningococcal_child",
     ["Glass test: blanching vs non-blanching",
      "Drowsiness and poor drinking",
      "Cold peripheries or leg pain", "Progression over hours"]),
    ("teenager tired with a sore throat and swollen glands for a week",
     "muffled 'hot potato' voice, drooling, can't swallow saliva, trismus",
     "glandular_fever", "epiglottitis_adult",
     ["Drooling or trismus = airway emergency",
      "'Hot potato' voice change",
      "Preferring to sit up",
      "Do NOT examine the throat or lie them down"]),
]


def _build() -> List[DiscriminationPair]:
    return [DiscriminationPair(
        benign_presentation=b, emergency_presentation=e,
        benign_condition=bc, emergency_condition=ec,
        discriminators=list(d))
        for (b, e, bc, ec, d) in _ROWS]


PAIRS: List[DiscriminationPair] = _build()

# Distinctive keywords for find_pairs when no condition id is mentioned
_KEYWORDS = {
    "headache": ["sah_subarachnoid", "tension_headache"],
    "chest pain": ["acs_stemi", "musculoskeletal_chest_pain"],
    "faint": ["vasovagal_syncope", "cardiac_syncope"],
    "blackout": ["vasovagal_syncope", "cardiac_syncope"],
    "syncope": ["vasovagal_syncope", "cardiac_syncope"],
    "abdominal pain": ["gastroenteritis", "acute_mesenteric_ischaemia"],
    "breathless": ["pe_pulmonary_embolism", "panic_attack"],
    "panic": ["panic_attack", "pe_pulmonary_embolism"],
    "neck lump": ["lymphadenopathy_reactive", "lymphoma_suspect"],
    "swollen glands": ["lymphadenopathy_reactive", "lymphoma_suspect"],
    "back pain": ["back_pain_mechanical", "cauda_equina"],
    "vertigo": ["bppv", "stroke_tia"],
    "dizzy": ["bppv", "stroke_tia"],
    "spins": ["bppv", "stroke_tia"],
    "rash": ["viral_rash_child", "meningococcal_child"],
    "sore throat": ["glandular_fever", "epiglottitis_adult"],
}


def find_pairs(text: str) -> List[DiscriminationPair]:
    """Return discrimination pairs relevant to a presentation: by condition
    id mention, or by presentation keyword."""
    t = text.lower()
    hits: List[DiscriminationPair] = []
    for p in PAIRS:
        if p.benign_condition in t or p.emergency_condition in t:
            hits.append(p)
    if not hits:
        for kw, _ in _KEYWORDS.items():
            if kw in t:
                for p in PAIRS:
                    if p.benign_condition in _KEYWORDS[kw] or \
                            p.emergency_condition in _KEYWORDS[kw]:
                        if p not in hits:
                            hits.append(p)
    return hits
