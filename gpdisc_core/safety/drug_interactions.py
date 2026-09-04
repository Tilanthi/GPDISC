"""
GPDISC Drug-Drug Interaction Checker

Critical patient safety system that checks for harmful drug interactions.

Features:
- Comprehensive interaction database (UK-focused)
- Severity levels (Severe, Moderate, Mild)
- Evidence-based recommendations
- Integration with patient medication records
- Automatic checking during prescriptions
- Contraindication detection

Safety Commitment:
- All checks performed locally
- No external API calls
- Evidence-based from BNF, NICE, MHRA
"""

import logging
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)


class InteractionSeverity(Enum):
    """Severity of drug interaction"""
    SEVERE = "severe"  # Avoid combination - life-threatening
    MODERATE = "moderate"  # Use with caution - monitor
    MILD = "mild"  # Usually safe - be aware
    CONTRAINDICATED = "contraindicated"  # Never use together


class InteractionEvidence(Enum):
    """Quality of evidence for interaction"""
    DEFINITE = "definite"  # Proven interaction
    PROBABLE = "probable"  # Likely interaction
    POSSIBLE = "possible"  # Suspected interaction
    DOUBTFUL = "doubtful"  # Unlikely or theoretical


@dataclass
class DrugInteraction:
    """Represents a drug-drug interaction"""
    drug1: str  # Primary drug
    drug2: str  # Interacting drug
    severity: InteractionSeverity
    evidence: InteractionEvidence
    description: str
    mechanism: str = ""
    clinical_effects: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    onset: str = ""  # rapid, delayed, unknown
    management: str = ""  # How to manage the interaction


@dataclass
class InteractionCheckResult:
    """Result of interaction check"""
    has_interactions: bool
    patient_id: str = ""
    medications_checked: List[str] = field(default_factory=list)
    interactions: List[DrugInteraction] = field(default_factory=list)
    safe_combinations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""


class DrugInteractionDatabase:
    """
    Database of known drug-drug interactions

    UK-focused based on BNF, NICE, and MHRA guidance.
    All interactions evidence-based.
    """

    def __init__(self):
        self.interactions = self._load_interactions()

    def _load_interactions(self) -> Dict[str, Dict[str, DrugInteraction]]:
        """Load interaction database"""
        interactions = {}

        # =========================================================================
        # SEVERE INTERACTIONS (Avoid combination - life-threatening)
        # =========================================================================

        # ACE Inhibitors + ARBs
        interactions["acei_arb"] = DrugInteraction(
            drug1="ACE Inhibitors",
            drug2="Angiotensin Receptor Blockers (ARBs)",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Dual blockade of renin-angiotensin system",
            mechanism="Additive effect on renin-angiotensin-aldosterone system",
            clinical_effects=[
                "Severe hypotension",
                "Hyperkalaemia",
                "Worsening renal function",
                "Increased risk of acute kidney injury"
            ],
            recommendations=[
                "AVOID combination",
                "Use only under specialist supervision",
                "Monitor renal function and potassium closely if combined",
                "Consider alternative antihypertensive regimen"
            ],
            references=["BNF 75", "NICE NG136", "MHRA"],
            onset="delayed",
            management="Stop one agent, monitor renal function and potassium"
        )

        # Warfarin + Aspirin (high dose)
        interactions["warfarin_aspirin_high"] = DrugInteraction(
            drug1="Warfarin",
            drug2="Aspirin (high dose, >325mg/day)",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Increased bleeding risk",
            mechanism="Additive antiplatelet and anticoagulant effects",
            clinical_effects=[
                "Life-threatening bleeding",
                "GI haemorrhage",
                "Intracranial haemorrhage",
                "Reduced INR control"
            ],
            recommendations=[
                "AVOID routine combination",
                "Low-dose aspirin (75mg) may be used with INR monitoring",
                "Consider gastroprotection with PPI",
                "Strict INR monitoring required"
            ],
            references=["BNF 75", "NICE CG184", "MHRA"],
            onset="rapid",
            management="Monitor INR more frequently, consider gastroprotection"
        )

        # NSAIDs + Anticoagulants
        interactions["nsaid_anticoagulant"] = DrugInteraction(
            drug1="NSAIDs (ibuprofen, naproxen, diclofenac)",
            drug2="Anticoagulants (warfarin, DOACs)",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Increased bleeding risk",
            mechanism="NSAIDs inhibit platelet function + damage gastric mucosa",
            clinical_effects=[
                "Life-threatening bleeding",
                "GI haemorrhage",
                "Reduced anticoagulant control (warfarin)",
                "Worsening renal function"
            ],
            recommendations=[
                "AVOID combination if possible",
                "Use paracetamol for analgesia instead",
                "If NSAID essential, use gastroprotection",
                "Monitor INR closely if warfarin",
                "Consider DOAC dose adjustment"
            ],
            references=["BNF 75", "NICE NG54", "MHRA Drug Safety Update"],
            onset="rapid",
            management="Stop NSAID, use alternative analgesic, monitor for bleeding"
        )

        # Lithium + ACE Inhibitors/ARBs
        interactions["lithium_raasi"] = DrugInteraction(
            drug1="Lithium",
            drug2="ACE Inhibitors or ARBs",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Increased lithium levels - toxicity risk",
            mechanism="RAAS inhibitors reduce lithium excretion",
            clinical_effects=[
                "Lithium toxicity",
                "Confusion, ataxia, tremor",
                "Seizures",
                "Cardiac arrhythmias"
            ],
            recommendations=[
                "AVOID combination if possible",
                "If essential, reduce lithium dose by 50%",
                "Monitor lithium levels frequently (weekly initially)",
                "Monitor renal function",
                "Educate patient on toxicity symptoms"
            ],
            references=["BNF 75", "NICE CG185", "MHRA"],
            onset="delayed",
            management="Reduce lithium dose, frequent monitoring, check levels"
        )

        # Digoxin + Verapamil/Diltiazem
        interactions["digoxin_verapamil"] = DrugInteraction(
            drug1="Digoxin",
            drug2="Verapamil or Diltiazem",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Increased digoxin levels",
            mechanism="Calcium channel blockers reduce digoxin excretion",
            clinical_effects=[
                "Digoxin toxicity",
                "Nausea, vomiting, visual disturbance",
                "Life-threatening arrhythmias",
                "Heart block"
            ],
            recommendations=[
                "AVOID combination if possible",
                "If essential, reduce digoxin dose by 50%",
                "Monitor digoxin levels closely",
                "Monitor ECG for digoxin toxicity",
                "Monitor renal function"
            ],
            references=["BNF 75", "NICE CKS"],
            onset="delayed",
            management="Reduce digoxin dose, check levels, monitor ECG"
        )

        # Potassium-Sparing Diuretics + ACE Inhibitors/ARBs
        interactions["k_sparing_raasi"] = DrugInteraction(
            drug1="Potassium-Sparing Diuretics (spironolactone, amiloride)",
            drug2="ACE Inhibitors or ARBs",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Severe hyperkalaemia risk",
            mechanism="Additive effect on potassium retention",
            clinical_effects=[
                "Severe hyperkalaemia",
                "Cardiac arrhythmias",
                "Muscle weakness",
                "Life-threatening cardiac effects"
            ],
            recommendations=[
                "AVOID combination",
                "Monitor potassium closely if combined",
                "Avoid potassium supplements",
                "Consider alternative diuretic",
                "ECG monitoring if combined"
            ],
            references=["BNF 75", "NICE NG136", "MHRA"],
            onset="delayed",
            management="Stop combination, monitor potassium and ECG"
        )

        # Metformin + IV Contrast (Iodinated)
        interactions["metformin_contrast"] = DrugInteraction(
            drug1="Metformin",
            drug2="Iodinated IV Contrast Media",
            severity=InteractionSeverity.SEVERE,
            evidence=InteractionEvidence.DEFINITE,
            description="Lactic acidosis risk",
            mechanism="Contrast-induced renal impairment + metformin accumulation",
            clinical_effects=[
                "Lactic acidosis",
                "Acute kidney injury",
                "Metabolic acidosis",
                "Life-threatening metabolic derangement"
            ],
            recommendations=[
                "STOP metformin before contrast",
                "Withhold metformin for 48 hours after contrast",
                "Check renal function before restarting",
                "Ensure adequate hydration",
                "Restart only if renal function stable"
            ],
            references=["BNF 75", "NICE NG28", "RCR Guidelines"],
            onset="delayed",
            management="Stop metformin 48h before contrast, restart after renal function confirmed normal"
        )

        # =========================================================================
        # MODERATE INTERACTIONS (Use with caution - monitor)
        # =========================================================================

        # Warfarin + Antibiotics
        interactions["warfarin_antibiotics"] = DrugInteraction(
            drug1="Warfarin",
            drug2="Broad-spectrum Antibiotics (amoxicillin, ciprofloxacin, erythromycin, etc.)",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.PROBABLE,
            description="Increased INR - bleeding risk",
            mechanism="Antibiotics reduce vitamin K production/gut flora",
            clinical_effects=[
                "Increased INR",
                "Bleeding risk",
                "Unstable anticoagulation"
            ],
            recommendations=[
                "Monitor INR frequently during and after course",
                "Consider dose adjustment",
                "Patient education on bleeding signs",
                "May need temporary warfarin dose reduction"
            ],
            references=["BNF 75", "NICE CG184"],
            onset="delayed",
            management="Frequent INR monitoring, adjust warfarin dose as needed"
        )

        # Warfarin + Paracetamol
        # 2026-09-04: added after a live question ("Is it safe to take
        # paracetamol alongside warfarin?") returned a false all-clear
        # because the pair had no row. Occasional short courses ARE
        # acceptable - paracetamol stays the preferred analgesic on
        # warfarin - but regular use raises the INR, and the answer must
        # say both halves.
        interactions["warfarin_paracetamol"] = DrugInteraction(
            drug1="Warfarin",
            drug2="Paracetamol",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.PROBABLE,
            description="Regular paracetamol increases INR - bleeding risk",
            mechanism=("Not fully established; sustained paracetamol "
                       "(esp. >=2g/day) enhances warfarin's anticoagulant "
                       "effect - possible NAPQI effect on vitamin "
                       "K-dependent factor synthesis"),
            clinical_effects=[
                "Increased INR with regular use",
                "Bleeding risk (bruising, haematuria, melaena)",
                "Unstable anticoagulation"
            ],
            recommendations=[
                "Paracetamol remains the PREFERRED analgesic on warfarin "
                "- NSAIDs and aspirin are the ones to avoid",
                "Occasional short courses (1-2 days, standard dose) are "
                "acceptable without extra monitoring",
                "If regular use is needed (especially >=2g/day for "
                "several days): check INR after a few days",
                "Educate on bleeding signs (bruising, blood in urine, "
                "black stools, prolonged bleeding)",
                "Maximum 4g/day; reduce in elderly, low body weight, or "
                "liver disease"
            ],
            references=["BNF 75", "Stockley's Drug Interactions"],
            onset="delayed",
            management=("Continue paracetamol if needed; add an INR check "
                        "after several days of regular co-administration")
        )

        # Statins + Macrolides
        interactions["statin_macrolide"] = DrugInteraction(
            drug1="Statins (simvastatin, atorvastatin)",
            drug2="Macrolide Antibiotics (erythromycin, clarithromycin)",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.PROBABLE,
            description="Increased statin levels - myopathy risk",
            mechanism="Macrolides inhibit statin metabolism (CYP3A4)",
            clinical_effects=[
                "Increased statin levels",
                "Myopathy, rhabdomyolysis risk",
                "Muscle pain, weakness"
            ],
            recommendations=[
                "TEMPORARILY STOP statin during macrolide course",
                "Use azithromycin instead (no interaction)",
                "Monitor CK if combination essential",
                "Patient education on myopathy symptoms"
            ],
            references=["BNF 75", "MHRA Drug Safety Update"],
            onset="delayed",
            management="Stop statin during macrolide course, monitor CK"
        )

        # Beta-Blockers + Verapamil
        interactions["beta_verapamil"] = DrugInteraction(
            drug1="Beta-Blockers",
            drug2="Verapamil",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.DEFINITE,
            description="Excessive bradycardia and heart block",
            mechanism="Additive negative chronotropic effects",
            clinical_effects=[
                "Severe bradycardia",
                "Heart block",
                "Hypotension",
                "Heart failure exacerbation"
            ],
            recommendations=[
                "AVOID combination if possible",
                "If essential, specialist supervision required",
                "Monitor ECG and blood pressure",
                "Avoid in heart failure patients"
            ],
            references=["BNF 75", "NICE CG185"],
            onset="rapid",
            management="Specialist supervision, ECG monitoring, consider stopping one agent"
        )

        # SSRIs + NSAIDs
        interactions["ssri_nsaid"] = DrugInteraction(
            drug1="SSRIs (citalopram, fluoxetine, sertraline)",
            drug2="NSAIDs (ibuprofen, naproxen, diclofenac)",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.PROBABLE,
            description="Increased GI bleeding risk",
            mechanism="Additive effect on gastric mucosa + platelet inhibition",
            clinical_effects=[
                "GI bleeding",
                "Peptic ulceration",
                "Anaemia"
            ],
            recommendations=[
                "Use with caution",
                "Consider gastroprotection (PPI)",
                "Use lowest effective NSAID dose",
                "Monitor for anaemia"
            ],
            references=["BNF 75", "NICE CG184"],
            onset="delayed",
            management="Consider gastroprotection, use lowest NSAID dose, monitor"
        )

        # Loop Diuretics + Aminoglycosides
        interactions["loop_aminoglycoside"] = DrugInteraction(
            drug1="Loop Diuretics (furosemide, bumetanide)",
            drug2="Aminoglycosides (gentamicin, amikacin)",
            severity=InteractionSeverity.MODERATE,
            evidence=InteractionEvidence.PROBABLE,
            description="Increased ototoxicity and nephrotoxicity",
            mechanism="Additive renal toxicity",
            clinical_effects=[
                "Worsening renal function",
                "Hearing loss, ototoxicity",
                "Vestibular toxicity"
            ],
            recommendations=[
                "Use with caution",
                "Monitor renal function closely",
                "Monitor drug levels",
                "Adequate hydration",
                "Consider alternative antibiotics"
            ],
            references=["BNF 75", "NICE NG114"],
            onset="delayed",
            management="Monitor renal function and drug levels, ensure hydration"
        )

        # =========================================================================
        # MILD INTERACTIONS (Usually safe - be aware)
        # =========================================================================

        # PPIs + Clopidogrel
        interactions["ppi_clopidogrel"] = DrugInteraction(
            drug1="Proton Pump Inhibitors (omeprazole, esomeprazole)",
            drug2="Clopidogrel",
            severity=InteractionSeverity.MILD,
            evidence=InteractionEvidence.PROBABLE,
            description="Possible reduced clopidogrel efficacy",
            mechanism="PPIs inhibit clopidogrel activation (CYP2C19)",
            clinical_effects=[
                "Possibly reduced antiplatelet effect",
                "May increase cardiovascular events"
            ],
            recommendations=[
                "Consider alternative gastroprotection",
                "Use pantoprazole or H2RA instead",
                "Monitor cardiovascular status",
                "Not absolute contraindication"
            ],
            references=["BNF 75", "MHRA Drug Safety Update"],
            onset="delayed",
            management="Consider pantoprazole instead of omeprazole"
        )

        # SSRIs + Tramadol
        interactions["ssri_tramadol"] = DrugInteraction(
            drug1="SSRIs",
            drug2="Tramadol",
            severity=InteractionSeverity.MILD,
            evidence=InteractionEvidence.POSSIBLE,
            description="Increased risk of serotonin syndrome",
            mechanism="Additive serotonergic effects",
            clinical_effects=[
                "Serotonin syndrome (rare)",
                "Confusion, agitation",
                "Hyperreflexia, fever"
            ],
            recommendations=[
                "Be aware of interaction",
                "Monitor for serotonin syndrome",
                "Consider alternative analgesic if symptoms",
                "Usually safe at normal doses"
            ],
            references=["BNF 75"],
            onset="delayed",
            management="Monitor for serotonin syndrome symptoms"
        )

        # Calcium Supplements + Thyroxine
        interactions["calcium_thyroxine"] = DrugInteraction(
            drug1="Calcium Supplements",
            drug2="Levothyroxine",
            severity=InteractionSeverity.MILD,
            evidence=InteractionEvidence.DEFINITE,
            description="Reduced thyroxine absorption",
            mechanism="Calcium binds thyroxine in GI tract",
            clinical_effects=[
                "Reduced thyroxine effect",
                "Elevated TSH",
                "Hypothyroid symptoms"
            ],
            recommendations=[
                "Separate administration by 4 hours",
                "Take thyroxine on empty stomach",
                "Monitor TSH if starting calcium",
                "Usually manageable with timing"
            ],
            references=["BNF 75", "NICE NG145"],
            onset="delayed",
            management="Separate doses by 4 hours, monitor TSH"
        )

        # =========================================================================
        # CONTRAINDICATED COMBINATIONS (Never use together)
        # =========================================================================

        # Clarithromycin + Simvastatin
        interactions["clarithromycin_simvastatin"] = DrugInteraction(
            drug1="Clarithromycin",
            drug2="Simvastatin",
            severity=InteractionSeverity.CONTRAINDICATED,
            evidence=InteractionEvidence.DEFINITE,
            description="Contraindicated - severe myopathy risk",
            mechanism="Clarithromycin inhibits simvastatin metabolism (CYP3A4)",
            clinical_effects=[
                "Severe myopathy",
                "Rhabdomyolysis",
                "Acute kidney injury",
                "Life-threatening muscle breakdown"
            ],
            recommendations=[
                "STOP simvastatin temporarily",
                "Use atorvastatin 20mg max during macrolide",
                "Or use rosuvastatin",
                "Resume simvastatin after antibiotic course"
            ],
            references=["BNF 75", "MHRA Drug Safety Update"],
            onset="delayed",
            management="Stop simvastatin during macrolide course, use alternative statin"
        )

        # PDE5 Inhibitors + Nitrates
        interactions["pde5_nitrates"] = DrugInteraction(
            drug1="PDE5 Inhibitors (sildenafil, tadalafil)",
            drug2="Nitrates (GTN, isosorbide mononitrate)",
            severity=InteractionSeverity.CONTRAINDICATED,
            evidence=InteractionEvidence.DEFINITE,
            description="Contraindicated - severe hypotension",
            mechanism="Additive vasodilation",
            clinical_effects=[
                "Life-threatening hypotension",
                "Myocardial ischaemia",
                "Syncope",
                "Cardiovascular collapse"
            ],
            recommendations=[
                "CONTRAINDICATED - NEVER combine",
                "Patient education critical",
                "Emergency: may need nitrates - use with extreme caution",
                "Consider alternative ED treatment"
            ],
            references=["BNF 75", "NICE CG185"],
            onset="rapid",
            management="NEVER combine - patient education essential, emergency protocols needed"
        )

        return interactions


class DrugInteractionChecker:
    """
    Drug-drug interaction checker for patient safety

    Checks patient medications for harmful interactions.
    All checks performed locally - no external API calls.
    """

    def __init__(self):
        """Initialize interaction checker"""
        self.database = DrugInteractionDatabase()
        self.drug_mappings = self._load_drug_mappings()
        logger.info("DrugInteractionChecker initialized")

    def _load_drug_mappings(self) -> Dict[str, Set[str]]:
        """
        Load mappings of drug names to categories

        Maps individual drugs to their classes/categories for interaction checking.
        """
        mappings = {
            # ACE Inhibitors
            "ace_inhibitors": {
                "ramipril", "enalapril", "lisinopril", "perindopril",
                "captopril", "benazepril", "quinapril", "fosinopril",
                "trandolapril", "moexipril", "zofenopril"
            },
            # ARBs
            "angiotensin_receptor_blockers": {
                "losartan", "candesartan", "valsartan", "irbesartan",
                "telmisartan", "olmesartan", "eprosartan", "azilsartan"
            },
            # Warfarin
            "warfarin": {"warfarin", "coumadin"},
            # Paracetamol (includes compounds that contain it)
            "paracetamol": {
                "paracetamol", "acetaminophen", "tylenol", "panadol",
                "co-codamol", "co-dydramol", "solpadeine"
            },
            # DOACs
            "doacs": {
                "apixaban", "rivaroxaban", "edoxaban", "dabigatran"
            },
            # NSAIDs
            "nsaids": {
                "ibuprofen", "naproxen", "diclofenac", "celecoxib",
                "etoricoxib", "indomethacin", "ketoprofen", "meloxicam",
                "piroxicam", "sulindac", "tolmetin"
            },
            # Aspirin
            "aspirin": {"aspirin", "acetylsalicylic acid"},
            # Statins
            "statins": {
                "simvastatin", "atorvastatin", "rosuvastatin",
                "pravastatin", "fluvastatin", "pitavastatin"
            },
            # Macrolides
            "macrolides": {
                "erythromycin", "clarithromycin", "azithromycin"
            },
            # Beta-Blockers
            "beta_blockers": {
                "bisoprolol", "atenolol", "metoprolol", "propranolol",
                "carvedilol", "nebivolol", "sotalol", "timolol"
            },
            # Calcium Channel Blockers
            "ccb_verapamil": {"verapamil"},
            "ccb_diltiazem": {"diltiazem"},
            "ccb_dihydropyridine": {"amlodipine", "felodipine", "nifedipine"},
            # Diuretics
            "loop_diuretics": {"furosemide", "bumetanide", "torasemide"},
            "thiazides": {"bendroflumethiazide", "indapamide", "hydrochlorothiazide"},
            "potassium_sparing": {"spironolactone", "amiloride", "triamterene", "eplerenone"},
            # Lithium
            "lithium": {"lithium", "lithium carbonate"},
            # Digoxin
            "digoxin": {"digoxin", "lanoxin"},
            # Metformin
            "metformin": {"metformin"},
            # SSRIs
            "ssris": {
                "citalopram", "escitalopram", "fluoxetine", "paroxetine",
                "sertraline", "fluvoxamine", "vortioxetine"
            },
            # PPIs
            "ppis": {"omeprazole", "esomeprazole", "lansoprazole", "pantoprazole", "rabeprazole"},
            # Clopidogrel
            "clopidogrel": {"clopidogrel", "plavix"},
            # Tramadol
            "tramadol": {"tramadol"},
            # Thyroxine
            "levothyroxine": {"levothyroxine", "thyroxine", "eltroxin"},
            # Nitrates
            "nitrates": {"glyceryl trinitrate", "gtn", "isosorbide mononitrate", "isosorbide dinitrate"},
            # PDE5 Inhibitors
            "pde5_inhibitors": {"sildenafil", "tadalafil", "vardenafil", "avanafil"},
            # Aminoglycosides
            "aminoglycosides": {"gentamicin", "amikacin", "tobramycin", "neomycin"}
        }

        return mappings

    def _normalize_drug_name(self, drug_name: str) -> str:
        """Normalize drug name for matching"""
        return drug_name.lower().strip().replace("-", " ").replace("_", " ")

    def _get_drug_category(self, drug_name: str) -> Optional[str]:
        """Get drug category from drug name"""
        normalized = self._normalize_drug_name(drug_name)

        for category, drugs in self.drug_mappings.items():
            # normalize the set entries too: "co-codamol" in the set must
            # match the normalized lookup name "co codamol"
            if normalized in {self._normalize_drug_name(d) for d in drugs}:
                return category

        return None

    def check_interaction(self, drug1: str, drug2: str) -> Optional[DrugInteraction]:
        """
        Check if two drugs interact

        Args:
            drug1: First drug name
            drug2: Second drug name

        Returns:
            DrugInteraction if found, None otherwise
        """
        drug1_norm = self._normalize_drug_name(drug1)
        drug2_norm = self._normalize_drug_name(drug2)

        # Direct drug name checks
        for interaction_id, interaction in self.database.interactions.items():
            int_drug1_norm = self._normalize_drug_name(interaction.drug1)
            int_drug2_norm = self._normalize_drug_name(interaction.drug2)

            # Check if drugs match (either order)
            if (drug1_norm in int_drug1_norm and drug2_norm in int_drug2_norm) or \
               (drug1_norm in int_drug2_norm and drug2_norm in int_drug1_norm):
                return interaction

        # Category-based checks
        category1 = self._get_drug_category(drug1)
        category2 = self._get_drug_category(drug2)

        if category1 and category2:
            for interaction_id, interaction in self.database.interactions.items():
                # Check category match
                if (category1 in interaction.drug1.lower() and category2 in interaction.drug2.lower()) or \
                   (category1 in interaction.drug2.lower() and category2 in interaction.drug1.lower()):
                    return interaction

        return None

    def check_patient_medication_list(self, medications: List[str]) -> InteractionCheckResult:
        """
        Check entire patient medication list for interactions

        Args:
            medications: List of medication names

        Returns:
            InteractionCheckResult with all interactions found
        """
        result = InteractionCheckResult(
            has_interactions=False,
            medications_checked=medications,
            interactions=[],
            safe_combinations=[],
            warnings=[],
            recommendations=[]
        )

        # Check all combinations
        for i in range(len(medications)):
            for j in range(i + 1, len(medications)):
                drug1 = medications[i]
                drug2 = medications[j]

                interaction = self.check_interaction(drug1, drug2)

                if interaction:
                    result.has_interactions = True
                    result.interactions.append(interaction)

                    # Add recommendations based on severity
                    if interaction.severity in [InteractionSeverity.SEVERE, InteractionSeverity.CONTRAINDICATED]:
                        result.recommendations.append(
                            f"SEVERE: {interaction.drug1} + {interaction.drug2} - {interaction.description}"
                        )
                        result.warnings.append(
                            f"⚠️ {interaction.drug1} + {interaction.drug2}: {interaction.severity.value.upper()} interaction"
                        )
                    elif interaction.severity == InteractionSeverity.MODERATE:
                        result.recommendations.append(
                            f"MODERATE: {interaction.drug1} + {interaction.drug2} - {interaction.description}"
                        )
                        result.warnings.append(
                            f"⚠ {interaction.drug1} + {interaction.drug2}: {interaction.severity.value.upper()} interaction"
                        )
                else:
                    result.safe_combinations.append(f"{drug1} + {drug2}")

        # Generate summary
        result.summary = self._generate_summary(result)

        return result

    def check_new_medication(self, patient_medications: List[str],
                            new_medication: str) -> InteractionCheckResult:
        """
        Check if new medication interacts with patient's current medications

        Args:
            patient_medications: List of patient's current medications
            new_medication: New medication being considered

        Returns:
            InteractionCheckResult with interactions found
        """
        result = InteractionCheckResult(
            has_interactions=False,
            medications_checked=patient_medications + [new_medication],
            interactions=[],
            warnings=[],
            recommendations=[]
        )

        for med in patient_medications:
            interaction = self.check_interaction(med, new_medication)

            if interaction:
                result.has_interactions = True
                result.interactions.append(interaction)

                # Severity-based recommendations
                if interaction.severity in [InteractionSeverity.SEVERE, InteractionSeverity.CONTRAINDICATED]:
                    result.recommendations.append(
                        f"DO NOT PRESCRIBE {new_medication}: {interaction.description}"
                    )
                    result.warnings.append(
                        f"🚨 {med} + {new_medication}: {interaction.severity.value.upper()} - {interaction.description}"
                    )
                elif interaction.severity == InteractionSeverity.MODERATE:
                    result.recommendations.append(
                        f"USE WITH CAUTION: {med} + {new_medication} - {interaction.description}"
                    )
                    result.warnings.append(
                        f"⚠️ {med} + {new_medication}: {interaction.severity.value.upper()} - {interaction.description}"
                    )
                elif interaction.severity == InteractionSeverity.MILD:
                    result.recommendations.append(
                        f"BE AWARE: {med} + {new_medication} - {interaction.description}"
                    )

        result.summary = self._generate_summary(result)

        return result

    def _generate_summary(self, result: InteractionCheckResult) -> str:
        """Generate human-readable summary"""
        lines = []

        if result.has_interactions:
            # Count by severity
            severe = sum(1 for i in result.interactions if i.severity == InteractionSeverity.SEVERE)
            contraindicated = sum(1 for i in result.interactions if i.severity == InteractionSeverity.CONTRAINDICATED)
            moderate = sum(1 for i in result.interactions if i.severity == InteractionSeverity.MODERATE)
            mild = sum(1 for i in result.interactions if i.severity == InteractionSeverity.MILD)

            lines.append(f"⚠️ DRUG INTERACTIONS DETECTED ({len(result.interactions)} total)")
            lines.append("")

            if contraindicated > 0:
                lines.append(f"🚨 CONTRAINDICATED: {contraindicated} interaction(s) - DO NOT USE TOGETHER")
            if severe > 0:
                lines.append(f"🔴 SEVERE: {severe} interaction(s) - AVOID COMBINATION")
            if moderate > 0:
                lines.append(f"🟠 MODERATE: {moderate} interaction(s) - USE WITH CAUTION")
            if mild > 0:
                lines.append(f"🟡 MILD: {mild} interaction(s) - BE AWARE")

            lines.append("")
            lines.append("CRITICAL INTERACTIONS:")
            for interaction in result.interactions:
                if interaction.severity in [InteractionSeverity.SEVERE, InteractionSeverity.CONTRAINDICATED]:
                    lines.append(f"  • {interaction.drug1} + {interaction.drug2}")
                    lines.append(f"    {interaction.description}")
                    lines.append(f"    Management: {interaction.management}")

            lines.append("")
            lines.append("RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations[:5], 1):
                lines.append(f"  {i}. {rec}")

            lines.append("")
            lines.append("📋 See detailed interaction list below")

        else:
            # 2026-09-04 honesty fix: "no row in this table" must never
            # read as "all combinations appear safe" - the paracetamol +
            # warfarin live question exposed exactly that false all-clear
            # before its row was added. State the table's size and defer.
            n_pairs = len(self.database.interactions)
            lines.append(f"NO KNOWN INTERACTIONS in the local table "
                         f"({n_pairs} evidence-based pairs)")
            lines.append("")
            lines.append(f"Checked {len(result.medications_checked)} medication(s)")
            lines.append("The local table is LIMITED - absence of a row here "
                         "is not evidence that a combination is safe")
            lines.append("Confirm with the BNF or a pharmacist before combining")

        return "\n".join(lines)

    def generate_interaction_report(self, result: InteractionCheckResult) -> str:
        """Generate detailed interaction report"""
        lines = []
        lines.append("=" * 70)
        lines.append("DRUG-DRUG INTERACTION CHECK REPORT")
        lines.append("=" * 70)
        lines.append("")

        lines.append(f"Medications Checked: {', '.join(result.medications_checked)}")
        lines.append("")

        if result.has_interactions:
            lines.append(f"INTERACTIONS FOUND: {len(result.interactions)}")
            lines.append("")

            for i, interaction in enumerate(result.interactions, 1):
                severity_icon = {
                    InteractionSeverity.CONTRAINDICATED: "🚨",
                    InteractionSeverity.SEVERE: "🔴",
                    InteractionSeverity.MODERATE: "🟠",
                    InteractionSeverity.MILD: "🟡"
                }.get(interaction.severity, "⚪")

                lines.append(f"{severity_icon} INTERACTION {i}: {interaction.severity.value.upper()}")
                lines.append(f"Drugs: {interaction.drug1} + {interaction.drug2}")
                lines.append(f"Description: {interaction.description}")
                lines.append(f"Mechanism: {interaction.mechanism}")
                lines.append(f"Effects: {', '.join(interaction.clinical_effects[:3])}")
                lines.append(f"Management: {interaction.management}")
                lines.append(f"Onset: {interaction.onset}")
                lines.append(f"References: {', '.join(interaction.references)}")
                lines.append("")

                lines.append("Recommendations:")
                for rec in interaction.recommendations[:3]:
                    lines.append(f"  • {rec}")
                lines.append("")
                lines.append("-" * 70)
                lines.append("")

        else:
            lines.append("✅ NO INTERACTIONS DETECTED")
            lines.append("")

        lines.append("=" * 70)
        lines.append("SAFETY REMINDER:")
        lines.append("- This is a safety check, not a replacement for professional review")
        lines.append("- Always consult BNF 75 or pharmacist for comprehensive checking")
        lines.append("- Monitor patients for adverse effects")
        lines.append("- Report any suspected interactions to MHRA Yellow Card")
        lines.append("=" * 70)

        return "\n".join(lines)


def create_interaction_checker() -> DrugInteractionChecker:
    """Factory function to create interaction checker"""
    return DrugInteractionChecker()


# Convenience functions
def check_drugs_interact(drug1: str, drug2: str) -> Optional[DrugInteraction]:
    """Quick check if two drugs interact"""
    checker = create_interaction_checker()
    return checker.check_interaction(drug1, drug2)


def check_patient_medications(medications: List[str]) -> InteractionCheckResult:
    """Check patient medication list for interactions"""
    checker = create_interaction_checker()
    return checker.check_patient_medication_list(medications)


def check_new_prescription(current_meds: List[str], new_med: str) -> InteractionCheckResult:
    """Check if new medication interacts with current medications"""
    checker = create_interaction_checker()
    return checker.check_new_medication(current_meds, new_med)


__all__ = [
    'DrugInteractionChecker',
    'DrugInteraction',
    'InteractionCheckResult',
    'InteractionSeverity',
    'InteractionEvidence',
    'create_interaction_checker',
    'check_drugs_interact',
    'check_patient_medications',
    'check_new_prescription'
]
