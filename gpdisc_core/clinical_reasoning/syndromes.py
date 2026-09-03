"""Syndrome-based reasoning for the returning traveller (expertise program
Stage 2). Five named frames — fever after travel, eosinophilia in a
traveller, fever + thrombocytopenia, fever + jaundice, fever + rash —
each carrying an ordered differential with key discriminators, the
questions that separate the hypotheses, first tests, red flags, and a
safety rule.

Detection order is declaration order: the most specific frame wins
(fever_after_travel before the plain conjunction frames).
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SyndromeDifferential:
    condition_id: str
    key_discriminator: str          # what makes this rise or fall in this frame
    must_ask: str                   # the discriminating question to ask now


@dataclass
class SyndromeFrame:
    key: str                        # e.g. "fever_after_travel"
    name: str
    required_features: List[str]    # ALL must be present among extracted features
    rank_note: str                  # ordering logic printed with the frame
    differentials: List[SyndromeDifferential] = field(default_factory=list)
    first_tests: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    safety_rule: str = ""


SYNDROME_FRAMES = [
    SyndromeFrame(
        key="fever_after_travel", name="Fever after travel",
        required_features=["fever", "fever_after_travel"],
        rank_note=("P. falciparum malaria is excluded FIRST in EVERY febrile traveller — "
                   "it kills within 24h and a single negative film never excludes it. "
                   "Incubation windows then separate: dengue 4-10d, enteric fever 7-21d, "
                   "malaria up to 6 months (vivax up to a year), hepatitis 2-6w, "
                   "Lassa/VHF up to 21d."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "Any fever within 6 months of a malarial area, no reassuring pattern; "
                "falciparum until films exclude it",
                "Exact itinerary and dates: which malarious regions, what prophylaxis "
                "was actually taken?"),
            SyndromeDifferential("dengue",
                "Retro-orbital pain, myalgia, rash, thrombocytopenia; incubation 4-10 days",
                "Bleeding gums/nose, abdominal pain or drowsiness? (dengue warning signs)"),
            SyndromeDifferential("typhoid",
                "Gradual stepwise fever, relative bradycardia, abdominal discomfort, "
                "constipation early",
                "Constipation before the fever? Eating street food in South Asia?"),
            SyndromeDifferential("leptospirosis",
                "Freshwater exposure + conjunctival suffusion + jaundice + renal impairment",
                "Swum or waded in freshwater, or flooded areas, in the last month?"),
            SyndromeDifferential("hepatitis_a",
                "Anorexia/nausea preceding jaundice by days; incubation 2-6 weeks",
                "Dark urine or pale stools? Jaundice in the eyes?"),
            SyndromeDifferential("vhf_suspect",
                "Bleeding + travel to West/Central Africa within 21 days — isolate "
                "BEFORE testing",
                "Which exact countries, and any funeral attendance or hospital contact "
                "abroad?"),
            SyndromeDifferential("meningococcal_child",
                "Fever + non-blanching rash — travel to the meningitis belt or Hajj "
                "multiplies risk; 999 before diagnosis",
                "Any rash? Glass test: does it fade under pressure? Neck stiffness "
                "or light sensitivity?"),
            SyndromeDifferential("influenza",
                "The most common cause — but a diagnosis of exclusion in a traveller",
                "Contacts with similar illness? Respiratory symptoms dominant?"),
        ],
        first_tests=["Malaria: RDT + thick/thin films x3 over 24-48h — SAME DAY, "
                     "before anything else",
                     "FBC (platelets, eosinophils), U&E, LFT, CRP",
                     "Blood cultures if admission or enteric fever suspected",
                     "Dengue NS1/IgM if within 7 days and compatible",
                     "Hepatitis A/E serology if LFT deranged",
                     "Ask UKHSA Imported Fever Service before testing if VHF possible"],
        red_flags=["Coma, seizures, or confusion (cerebral malaria / severe dengue / VHF)",
                   "Bleeding or spontaneous bruising (dengue warning, VHF, leptospirosis)",
                   "Jaundice + oliguria (Weil disease, severe malaria, hepatitis A/E "
                   "in pregnancy)",
                   "Returned from West/Central Africa within 21 days (VHF pathway)"],
        safety_rule=("Every febrile traveller is SAME-DAY assessed with malaria excluded "
                     "or treated. Never accept a single negative film as reassurance.")),
    SyndromeFrame(
        key="eosinophilia_returning_traveller",
        name="Eosinophilia in a returning traveller / migrant",
        required_features=["eosinophilia"],
        rank_note=("Eosinophilia means worm burden until proven otherwise — think where "
                   "the person has been, not which itch they have. Steroid or biologic "
                   "immunosuppression is dangerous until strongyloides is excluded."),
        differentials=[
            SyndromeDifferential("schistosomiasis_acute",
                "Freshwater exposure in Africa; Katayama fever 2-8w post-exposure; "
                "serology from 6-12w",
                "Swum or paddled in any lake or river in Africa?"),
            SyndromeDifferential("strongyloidiasis",
                "Persists for decades; larva currens; FATAL hyperinfection if "
                "immunosuppressed",
                "Ever walked barefoot in tropical areas? Any steroids or biologics "
                "planned?"),
            SyndromeDifferential("hookworm",
                "Ground itch + anaemia; barefoot soil exposure",
                "Barefoot in rural tropical areas? Pallor or anaemia symptoms?"),
            SyndromeDifferential("filariasis",
                "After 3+ months in Africa/Asia; lymphoedema, Calabar swellings (loiasis)",
                "How long total time in the tropics? Any limb swelling or migratory "
                "swellings?"),
            SyndromeDifferential("asthma_allergy",
                "The non-travel cause: atopy, hay fever, drug reaction — check before "
                "the serology panel",
                "Any new drug started? Asthma or hay fever flare?"),
        ],
        first_tests=["Strongyloides serology (BEFORE any immunosuppression)",
                     "Schistosoma serology 6-12 weeks after last freshwater exposure",
                     "Filarial serology if 3+ months in endemic areas",
                     "Stool microscopy x3 (ova, cysts, parasites)",
                     "Hb/MCV (hookworm anaemia), total IgE"],
        red_flags=["Immunosuppression planned (steroids, biologics, transplant) — "
                   "strongyloides hyperinfection is fatal",
                   "Eosinophilia >3.0 x10^9/L or rising — haematology referral"],
        safety_rule=("Exclude strongyloides before ANY corticosteroid or biologic in "
                     "anyone with tropical exposure and eosinophilia.")),
    SyndromeFrame(
        key="fever_thrombocytopenia", name="Fever + thrombocytopenia",
        required_features=["fever", "thrombocytopenia"],
        rank_note=("Fever + low platelets after travel is malaria or dengue until "
                   "excluded; without travel, sepsis consumes platelets and counts <50 "
                   "carry bleeding risk."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "The classic malaria haematology; parasitaemia visible on film",
                "Travel in the last 6 months to ANY malarial area?"),
            SyndromeDifferential("dengue",
                "Platelets fall as fever defervesces — the dangerous window",
                "When did the fever settle? (dengue warning signs follow defervescence)"),
            SyndromeDifferential("sepsis",
                "No travel: DIC picture with prolonged clotting — treat first, "
                "investigate after",
                "Rigors, hypotension, confusion? (sepsis pathway overrides all)"),
        ],
        first_tests=["Malaria films x3 same day (non-negotiable first test)",
                     "Dengue NS1 antigen (days 1-5) / IgM (after day 5)",
                     "Clotting screen + fibrinogen (DIC)",
                     "Blood cultures before antibiotics"],
        red_flags=["Platelets <50 or falling rapidly — bleeding risk",
                   "Petechiae, gum bleeding, haematemesis",
                   "Narrowing pulse pressure or shock (severe dengue)"],
        safety_rule=("Fever + platelets <100 in a traveller = same-day senior review; "
                     "admit if <50, bleeding, or comorbid.")),
    SyndromeFrame(
        key="fever_jaundice", name="Fever + jaundice",
        required_features=["fever", "jaundice"],
        rank_note=("Fever + jaundice after travel: malaria first, then leptospirosis "
                   "and hepatitis E (lethal in pregnancy). Without travel, biliary "
                   "sepsis (Charcot triad) is the emergency."),
        differentials=[
            SyndromeDifferential("malaria_falciparum",
                "Haemolysis gives mild jaundice with disproportionate illness",
                "Travel where and when? Prophylaxis taken?"),
            SyndromeDifferential("leptospirosis",
                "Jaundice + renal failure + conjunctival suffusion after freshwater",
                "Freshwater contact, flooding, rats? Urine output?"),
            SyndromeDifferential("hepatitis_e",
                "Marked transaminitis; pregnancy is the emergency (25% mortality "
                "3rd trimester)",
                "Pregnant or possibly pregnant? This changes everything."),
            SyndromeDifferential("typhoid",
                "Hepatic involvement of enteric fever; abdominal signs",
                "South Asia travel? Abdominal pain or distension?"),
            SyndromeDifferential("cholecystitis",
                "The non-travel emergency: fever + jaundice + RUQ pain = biliary sepsis",
                "RUQ pain, dark urine, rigors? (Charcot triad needs admission)"),
        ],
        first_tests=["Malaria films x3 + FBC + U&E + LFT (ALT/AST pattern) + clotting",
                     "Hepatitis A/E serology; leptospira serology if exposure",
                     "Blood cultures; ultrasound biliary tree if RUQ pain",
                     "Pregnancy test in all women of child-bearing age"],
        red_flags=["Pregnancy with hepatitis E — urgent obstetric + ID referral",
                   "Confusion or drowsiness with jaundice (fulminant hepatitis)",
                   "Hypotension with RUQ pain (biliary sepsis — 999)"],
        safety_rule=("Fever + jaundice is admitted-level medicine in a traveller, and "
                     "biliary sepsis until examined without travel.")),
    SyndromeFrame(
        key="fever_rash", name="Fever + rash",
        required_features=["fever", "rash_generalised"],
        rank_note=("First question: does it blanch? Non-blanching = meningococcal "
                   "until proven otherwise = 999. Then travel (dengue, typhus), then "
                   "the childhood illnesses and scarlet fever."),
        differentials=[
            SyndromeDifferential("meningococcal_child",
                "Non-blanching petechiae/purpura with fever — 999 before diagnosis",
                "Glass test: does the rash fade under pressure? (any 'no' = 999)"),
            SyndromeDifferential("dengue",
                "Travel + retro-orbital pain + platelet drop; rash as fever settles",
                "Travel in last 2 weeks? Bleeding gums or nose?"),
            SyndromeDifferential("measles",
                "Cough/coryza/conjunctivitis THEN rash descending from hairline; "
                "Koplik spots",
                "Measles vaccine history? Rash start at the head and move down?"),
            SyndromeDifferential("scarlet_fever",
                "Sandpaper texture, strawberry tongue, circumoral pallor; strep context",
                "Sore throat before the rash? Rough sandpaper feel?"),
            SyndromeDifferential("tick_typhus_african",
                "Travel + eschar (black crust) + regional nodes",
                "Any tick bites or black scabs noticed? Safari/bush travel?"),
        ],
        first_tests=["Glass test / blanching check NOW (clinical, zero-cost)",
                     "If non-blanching: blood cultures + IV antibiotics — do not wait",
                     "FBC + CRP; malaria films if travel; dengue NS1 if 1-7 days "
                     "post-onset",
                     "Throat swab/ASO titre if scarlet fever suspected"],
        red_flags=["Non-blanching rash = meningococcal septicaemia pathway (999)",
                   "Rapidly spreading purpura, drowsiness, neck stiffness",
                   "Mucosal bleeding with fever (dengue/VHF)"],
        safety_rule=("Assume meningococcal until the rash blanches; admit every "
                     "non-blanching fever rash.")),
]


class SyndromeEngine:
    def __init__(self, frames: Optional[List[SyndromeFrame]] = None):
        self.frames = frames if frames is not None else SYNDROME_FRAMES

    def detect(self, features: List[str]) -> Optional[SyndromeFrame]:
        have = set(features)
        for frame in self.frames:
            if set(frame.required_features) <= have:
                return frame
        return None

    def for_presentation(self, text: str, context: Optional[Dict] = None) -> Optional[SyndromeFrame]:
        from .diagnostic_engine import _extract_features
        return self.detect(_extract_features(text, context))


def discriminating_questions(frame: SyndromeFrame) -> List[str]:
    """The questions that separate the hypotheses, plus the frame's ordering logic."""
    qs = [d.must_ask for d in frame.differentials]
    qs.append(frame.rank_note)
    return qs
