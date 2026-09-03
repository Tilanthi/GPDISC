"""
Pharmacology Domain Module for GPDISC
=======================================

This domain specializes in pharmacology, medication management, and drug safety.
Provides consultation on drug interactions, side effects, dosing, and medication optimization.

Key capabilities:
- Drug interaction checking
- Side effect evaluation and management
- Medication dosing and adjustment
- Polypharmacy review
- Prescription optimization
- Adverse drug reaction assessment
- Medication safety in special populations
- Pharmacological consultation

Privacy: All patient data stored locally, no external transmission.
"""

from typing import Dict, Any, Optional, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult

# Import interaction checker
try:
    from ...safety.drug_interactions import (
        create_interaction_checker,
        check_patient_medications,
        check_new_prescription,
        DrugInteractionChecker,
        InteractionSeverity
    )
    INTERACTION_CHECKER_AVAILABLE = True
except ImportError:
    INTERACTION_CHECKER_AVAILABLE = False
    DrugInteractionChecker = None
    InteractionSeverity = None


class PharmacologyDomain(BaseDomainModule):
    """Pharmacology domain specializing in medication management and drug safety."""

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="pharmacology",
            version="1.0.0",
            dependencies=[],
            description="Pharmacology, medication management, drug interactions, side effects, dosing, polypharmacy, medication safety",
            keywords=[
                "medication", "drug", "medicine", "pill", "tablet", "capsule", "prescription",
                "interaction", "drug interaction", "side effect", "adverse effect", "adverse reaction",
                "dosage", "dose", "dosing", "overdose", "toxicity", "therapeutic index",
                "pharmacokinetics", "pharmacodynamics", "metabolism", "excretion", "half-life",
                "contraindication", "precaution", "warning", "black box warning",
                "polypharmacy", "multiple medications", "medication list", "drug regimen",
                "antibiotic", "anticoagulant", "antiplatelet", "statin", "beta blocker",
                "ace inhibitor", "arb", "calcium channel blocker", "diuretic", "nsaid",
                "opioid", "analgesic", "antidepressant", "anxiolytic", "sedative",
                "insulin", "diabetic medication", "blood pressure medication",
                "warfarin", "doac", "apixaban", "rivaroxaban", "dabigatran", "edoxaban",
                "amiodarone", "digoxin", "lithium", "theophylline", "phenytoin",
                "renal dose", "hepatic dose", "dose adjustment", "monitoring", "blood level"
            ],
            capabilities=[
                "drug_interaction_checking",
                "side_effect_management",
                "dosing_optimization",
                "polypharmacy_review",
                "medication_safety",
                "adverse_drug_reaction_assessment",
                "prescription_consultation",
                "therapeutic_drug_monitoring"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """Process pharmacology-related queries."""
        try:
            query_lower = query.lower()

            # Drug interactions
            if any(term in query_lower for term in ["interaction", "interact with", "can i take", "safe to take together"]):
                return self._handle_interaction_query(query, context)

            # Side effects
            elif any(term in query_lower for term in ["side effect", "adverse effect", "reaction", "causes"]):
                return self._handle_side_effects_query(query, context)

            # Dosing
            elif any(term in query_lower for term in ["dosage", "dose", "dosing", "how much", "take"]):
                return self._handle_dosing_query(query, context)

            # Polypharmacy
            elif any(term in query_lower for term in ["multiple medications", "polypharmacy", "too many medications"]):
                return self._handle_polypharmacy_query(query, context)

            # Specific drug classes
            elif any(term in query_lower for term in ["antibiotic", "anticoagulant", "blood thinner", "statin", "opioid"]):
                return self._handle_drug_class_query(query, context)

            # Contraindications
            elif any(term in query_lower for term in ["contraindication", "should not take", "avoid", "caution"]):
                return self._handle_contraindications_query(query, context)

            # Medication safety
            elif any(term in query_lower for term in ["safe", "safety", "monitoring", "blood test"]):
                return self._handle_safety_query(query, context)

            # General pharmacology
            else:
                return self._handle_general_pharmacology_query(query, context)

        except Exception as e:
            return DomainQueryResult(
                domain_name="pharmacology",
                answer=f"Error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )

    def _handle_interaction_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle drug interaction queries with integrated interaction checker."""

        # Extract medications from query
        medications = self._extract_medications_from_query(query)

        # If we have medications and the checker is available, use it
        if medications and INTERACTION_CHECKER_AVAILABLE:
            try:
                from ...safety.drug_interactions import check_patient_medications

                result = check_patient_medications(medications)

                # Build comprehensive response
                response_lines = []
                response_lines.append("**Drug Interaction Check - GPDISC Safety System**\n")
                response_lines.append(f"**Medications Checked**: {', '.join(medications)}\n")
                response_lines.append(result.summary)
                response_lines.append("\n")

                # Add detailed interaction information
                if result.interactions:
                    response_lines.append("**DETAILED INTERACTIONS:**\n")
                    for interaction in result.interactions:
                        severity_icon = {
                            "contraindicated": "🚨",
                            "severe": "🔴",
                            "moderate": "🟠",
                            "mild": "🟡"
                        }.get(interaction.severity.value, "⚪")

                        response_lines.append(f"{severity_icon} **{interaction.drug1} + {interaction.drug2}**")
                        response_lines.append(f"**Severity**: {interaction.severity.value.upper()}")
                        response_lines.append(f"**Description**: {interaction.description}")
                        response_lines.append(f"**Mechanism**: {interaction.mechanism}")
                        response_lines.append(f"**Clinical Effects**:")
                        for effect in interaction.clinical_effects[:3]:
                            response_lines.append(f"  • {effect}")
                        response_lines.append(f"**Management**: {interaction.management}")
                        response_lines.append(f"**Recommendations**:")
                        for rec in interaction.recommendations[:3]:
                            response_lines.append(f"  • {rec}")
                        response_lines.append("")

                    # Add safety warnings
                    if any(i.severity in [InteractionSeverity.CONTRAINDICATED, InteractionSeverity.SEVERE]
                           for i in result.interactions):
                        response_lines.append("**⚠️ SAFETY WARNING:**")
                        response_lines.append("Severe or contraindicated interactions detected.")
                        response_lines.append("DO NOT PRESCRIBE these combinations without specialist supervision.")
                        response_lines.append("Consult pharmacist or specialist before proceeding.")
                        response_lines.append("")

                response_lines.append("**Sources:** BNF 75, NICE Guidelines, MHRA Drug Safety Update")
                response_lines.append("**Disclaimer:** This is a safety check tool. Always consult BNF, pharmacist,")
                response_lines.append("or specialist for comprehensive medication review.")

                answer = "\n".join(response_lines)

                return DomainQueryResult(
                    domain_name="pharmacology",
                    answer=answer,
                    confidence=0.95,
                    metadata={
                        "specialty": "pharmacology",
                        "subspecialty": "drug_interactions",
                        "medications_checked": medications,
                        "interactions_found": len(result.interactions),
                        "has_severe_interactions": any(
                            i.severity in [InteractionSeverity.SEVERE, InteractionSeverity.CONTRAINDICATED]
                            for i in result.interactions
                        ),
                        "sources": ["BNF 75", "NICE Guidelines", "MHRA Drug Safety Update"],
                        "checker_used": "GPDISC_interaction_checker_v1.0"
                    }
                )

            except Exception as e:
                logger.error(f"Error using interaction checker: {e}")
                # Fall back to manual response

        # Default manual response (fallback or if no medications extracted)
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Drug Interaction Consultation - Pharmacology Second Opinion**\n\n"
                "**Automated Drug Interaction Checking Available**\n\n"
                "To use the automated interaction checker, provide medications in your query:\n"
                "- **Example 1**: \"Check interactions: warfarin, aspirin, ibuprofen\"\n"
                "- **Example 2**: \"Can I take simvastatin with clarithromycin?\"\n"
                "- **Example 3**: \"Interactions between ramipril, lithium, and NSAIDs\"\n\n"
                "- **Doses**: If known\n"
                "- **Indication**: Why each medication is prescribed\n"
                "- **Medical history**: Kidney/liver function, comorbidities\n\n"
                "**Common Clinically Significant Interactions**:\n\n"
                "**Warfarin Interactions** (High Risk):\n"
                "- **Amiodarone**: Increases warfarin effect (reduce warfarin dose by 30-50%)\n"
                "- **Antibiotics**: Macrolides, fluoroquinolones, TMP-SMX increase effect\n"
                "- **NSAIDs**: Increase bleeding risk (antiplatelet + GI irritation)\n"
                "- **SSRIs**: Sertraline, fluoxetine increase bleeding risk\n"
                "- **Grapefruit juice**: May increase effect\n"
                "- **St. John's wort**: Decreases warfarin effect (avoid)\n"
                "- **Monitoring**: INR regularly, especially when starting/stopping interacting drugs\n\n"
                "**DOAC Interactions**:\n"
                "- **Drugs that increase DOAC levels**: Azole antifungals, macrolides, dronedarone, verapamil, amiodarone\n"
                "- **NSAIDs + DOACs**: Increased bleeding risk (avoid if possible)\n"
                "- **Antiplatelets + DOACs**: Increased bleeding (generally avoid)\n\n"
                "**Statin Interactions**:\n"
                "- **CYP3A4 inhibitors**: Increase statin levels (myopathy risk)\n"
                "  - **Simvastatin**: AVOID with clarithromycin, itraconazole, HIV protease inhibitors\n"
                "  - **Atorvastatin**: Dose limit with CYP3A4 inhibitors\n"
                "  - **Rosuvastatin**: Minimal CYP interactions (safer choice)\n"
                "- **Gemfibrozil**: Increases all statin levels (avoid)\n"
                "- **Grapefruit juice**: Increases simvastatin, atorvastatin levels\n\n"
                "**Antibiotic Interactions**:\n"
                "- **Macrolides + statins**: Myopathy risk\n"
                "- **Macrolides + QT-prolonging drugs**: Torsades de pointes risk\n"
                "- **Quinolones + divalent cations**: Decreased absorption (separate by 2 hours)\n"
                "- **Tetracyclines + dairy/antacids**: Decreased absorption\n"
                "- **Metronidazole + alcohol**: Disulfiram-like reaction (avoid alcohol)\n\n"
                "**Antidepressant Interactions**:\n"
                "- **SSRIs + SNRIs + tramadol**: Serotonin syndrome risk\n"
                "- **SSRIs + antiplatelets/anticoagulants**: Increased bleeding\n"
                "- **MAOIs**: Tyramine interaction (hypertensive crisis) - many drug-drug interactions\n"
                "- **Linezolid** (antibiotic): Serotonin syndrome with SSRIs\n\n"
                "**QT Prolongation**:\n"
                "- **Drugs**: Quinolones, macrolides, antipsychotics, TCAs, methadone, ondansetron\n"
                "- **Risk**: Torsades de pointes (fatal arrhythmia)\n"
                "- **ECG monitoring**: If multiple QT-prolonging drugs or electrolyte abnormalities\n\n"
                "**Renal Dose Adjustments**:\n"
                "- **DOACs**: Dose reduction if CrCl <30-50 mL/min (drug-specific)\n"
                "- **DOACs**: Contraindicated if CrCl <15-30 mL/min (drug-specific)\n"
                "- **Direct Xa inhibitors**: Avoid in CrCl <15 mL/min (most)\n"
                "- **Dabigatran**: Avoid if CrCl <30 mL/min\n"
                "- **Warfarin**: No dose adjustment for renal function\n\n"
                "**Herbal Supplements**:\n"
                "- **St. John's wort**: CYP inducer (decreases many drugs: warfarin, DOACs, cyclosporine, OCPs)\n"
                "- **Ginkgo biloba**: Increased bleeding risk with anticoagulants\n"
                "- **Grapefruit juice**: Inhibits CYP3A4 (increases many drugs)\n"
                "- **Garlic supplements**: Increased bleeding risk\n\n"
                "**Resources**:\n"
                "- **BNF Appendix 1**: Drug interactions\n"
                "- **Liverpool Drug Interactions**: HIV/hepatitis interactions\n"
                "- **Medscape**: Drug interaction checker\n\n"
                "**Disclaimer**: Interaction risk depends on doses, individual factors. "
                "Comprehensive medication review by pharmacist/physician recommended."
            ),
            confidence=0.88,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "drug_interactions",
                "sources": ["BNF", "Medscape Drug Interaction Checker", "Liverpool Drug Interactions"]
            }
        )

    def _handle_side_effects_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle side effect queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Side Effect Management - Pharmacology Second Opinion**\n\n"
                "**Principles of Side Effect Management**:\n\n"
                "**1. Confirm Causality**:\n"
                "- **Timing**: Did symptom start after drug initiation?\n"
                "- **Dechallenge**: Did symptom improve with drug discontinuation?\n"
                "- **Rechallenge**: Did symptom recur with re-administration?\n"
                "- **Alternative explanations**: Disease progression, other drugs\n\n"
                "**2. Assess Severity**:\n"
                "- **Mild**: Tolerable, no intervention needed\n"
                "- **Moderate**: Bothersome, interferes with function, dose reduction or treatment\n"
                "- **Severe**: Intolerable, dangerous, discontinuation\n\n"
                "**3. Management Strategies**:\n"
                "- **Wait**: Tolerance may develop (e.g., nausea, headache)\n"
                "- **Dose reduction**: Lower dose if possible\n"
                "- **Switch**: Alternative drug within same class or different class\n"
                "- **Add**: Symptomatic treatment (e.g., antiemetic for nausea)\n"
                "- **Discontinue**: If severe, dangerous, or intolerable\n\n"
                "**Common Drug Class Side Effects**:\n\n"
                "**Statins**:\n"
                "- **Myalgia**: Muscle pain, tenderness (7-29%)\n"
                "- **Myopathy/rhabdomyolysis**: Rare (<0.1%), CK monitoring if symptoms\n"
                "- **Management**: Check CK, discontinue if >10x ULN or symptoms\n"
                "- **Re-challenge**: Lower dose or different statin (rosuvastatin, pravastatin)\n"
                "- **CoQ10**: Evidence for myalgia management mixed\n\n"
                "**Beta-blockers**:\n"
                "- **Fatigue**: 10-20%\n"
                "- **Bradycardia**: May require dose reduction\n"
                "- **Bronchospasm**: Avoid in asthma (use cardioselective: bisoprolol, metoprolol)\n"
                "- **Cold extremities**: Common, benign\n"
                "- **Sexual dysfunction**: Erectile dysfunction\n"
                "- **Mask hypoglycemia symptoms**: In diabetes\n\n"
                "**ACE Inhibitors**:\n"
                "- **Dry cough**: 5-20% (bradykinin-mediated)\n"
                "  - **Management**: Switch to ARB\n"
                "- **Hyperkalemia**: Monitor K+ if renal impairment, diabetes, concurrent K+-sparing drugs\n"
                "- **Angioedema**: Rare (<1%), life-threatening, contraindicates all ACE inhibitors\n"
                "- **First-dose hypotension**: More common if volume-depleted, high-dose diuretic\n"
                "- **Taste disturbance**: Metallic taste (dose-dependent)\n\n"
                "**Calcium Channel Blockers**:\n"
                "- **Peripheral edema**: Dose-dependent, amlodipine > others\n"
                "- **Constipation**: Verapamil > others\n"
                "- **Gingival hyperplasia**: Rare\n"
                "- **Bradycardia/AV block**: Verapamil, diltiazem (contraindicated if 2nd/3rd degree block)\n\n"
                "**SSRIs**:\n"
                "- **GI upset**: Nausea, diarrhea (take with food, usually transient)\n"
                "- **Sexual dysfunction**: ED, delayed ejaculation, anorgasmia (25-50%)\n"
                "- **Weight gain**: Long-term use\n"
                "- **Insomnia/anxiety**: May occur early, consider morning dosing\n"
                "- **Hyponatremia**: SIADH (elderly risk)\n"
                "- **Discontinuation syndrome**: Dizziness, paresthesia (taper slowly)\n\n"
                "**Opioids**:\n"
                "- **Constipation**: Universal, prophylactic laxatives recommended\n"
                "- **Nausea**: Common initially, usually transient\n"
                "- **Sedation**: Early, tolerance develops\n"
                "- **Respiratory depression**: Dose-dependent, life-threatening\n"
                "- **Pruritus**: Histamine release, antihistamines may help\n"
                "- **Endocrine effects**: Hypogonadism (long-term use)\n"
                "- **Hyperalgesia**: Paradoxical increased pain sensitivity\n\n"
                "**NSAIDs**:\n"
                "- **GI irritation**: Dyspepsia, ulcer, bleed (take with food, consider PPI)\n"
                "- **Renal impairment**: AKI (avoid in CKD, dehydration)\n"
                "- **Hypertension**: Worsens BP control\n"
                "- **Heart failure**: Fluid retention, exacerbates HF\n"
                "- **Platelet inhibition**: Increased bleeding (irreversible: aspirin; reversible: others)\n\n"
                "**Anticoagulants**:\n"
                "- **Bleeding**: Major complication, requires monitoring\n"
                "- **Warfarin**: Skin necrosis (rare, protein C depletion), purple toe syndrome\n\n"
                "**Antibiotics**:\n"
                "- **GI upset**: Common (amoxicillin/clavulanate > amoxicillin)\n"
                "- **C. difficile**: Any antibiotic, especially clindamycin, fluoroquinolones\n"
                "- **Photosensitivity**: Tetracyclines, fluoroquinolones\n"
                "- **Tendon rupture**: Fluoroquinolones (avoid in elderly, steroid use)\n"
                "- **QT prolongation**: Macrolides, fluoroquinolones\n"
                "- **Ototoxicity**: Aminoglycosides, furosemide (synergistic)\n"
                "- **Nephrotoxicity**: Aminoglycosides, amphotericin, vancomycin\n\n"
                "**Serious/Deadly Side Effects** (immediate discontinuation):\n"
                "- **Stevens-Johnson syndrome / Toxic epidermal necrolysis**: Lamotrigine, carbamazepine, allopurinol, sulfonamides, others\n"
                "- **Anaphylaxis**: Penicillins, others\n"
                "- **Agranulocytosis**: Clozapine, carbimazole, others\n"
                "- **Aplastic anemia**: Carbamazepine, others\n"
                "- **Rhabdomyolysis**: Statins (especially with interactions)\n"
                "- **Torsades de pointes**: QT-prolonging drugs\n"
                "- **Serotonin syndrome**: SSRIs/SNRIs + serotonergic drugs\n"
                "- **Neuroleptic malignant syndrome**: Antipsychotics\n"
                "- **Malignant hyperthermia**: Succinylcholine, volatile anesthetics\n\n"
                "**Reporting Adverse Drug Reactions**:\n"
                "- **UK**: Yellow Card Scheme (MHRA)\n"
                "- **US**: MedWatch (FDA)\n"
                "- **Purpose**: Pharmacovigilance, identify rare/late reactions\n\n"
                "**Disclaimer**: Side effect management individualized. Consult prescriber/pharmacist."
            ),
            confidence=0.86,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "adverse_drug_reactions",
                "sources": ["BNF", "Meyler's Side Effects of Drugs", "MHRA Yellow Card"]
            }
        )

    def _handle_dosing_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle dosing queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Medication Dosing - Pharmacology Second Opinion**\n\n"
                "**General Dosing Principles**:\n\n"
                "**Adult Dosing**:\n"
                "- **Start low, go slow**: Especially in elderly\n"
                "- **Individualize**: Consider weight, renal/hepatic function, comorbidities\n"
                "- **Therapeutic drug monitoring**: Warfarin (INR), lithium, digoxin, phenytoin, theophylline, aminoglycosides, vancomycin\n"
                "- **Check renal/hepatic function**: Before prescribing renally/hepatically cleared drugs\n"
                "- **Consider drug interactions**: May increase or decrease levels\n\n"
                "**Renal Dose Adjustment**:\n"
                "- **Calculate CrCl (Cockcroft-Gault)** or eGFR (CKD-EPI, MDRD)\n"
                "- **Drugs requiring renal adjustment**:\n"
                "  - **DOACs**: Dose reduce or avoid if CrCl <15-30 mL/min\n"
                "  - **Direct Xa inhibitors**: Avoid if CrCl <15 mL/min (most)\n"
                "  - **Dabigatran**: Avoid if CrCl <30 mL/min\n"
                "  - **Antibiotics**: Many require adjustment (penicillins, cephalosporins, fluoroquinolones, vancomycin, aminoglycosides)\n"
                "  - **Antivirals**: Acyclovir, valacyclovir, ganciclovir, Tenofovir\n"
                "  - **Antidiabetics**: Most don't require adjustment, except SGLT2 (eGFR <20-30)\n"
                "  - **Statins**: No adjustment (except high-dose atorvastatin with CKD)\n"
                "  - **PPIs**: No adjustment for most, dose reduction for severe CKD\n"
                "  - **Levothyroxine**: No adjustment\n"
                "  - **Anticoagulants**: Warfarin (no adjustment), DOACs (adjust)\n"
                "  - **Diuretics**: Loop diuretics (dose adjust), thiazides (ineffective eGFR <30)\n"
                "  - **Allopurinol**: Dose reduce to 100mg if eGFR <20\n"
                "  - **Colchicine**: Dose reduce or avoid\n"
                "  - **Gabapentin/Pregabalin**: Dose reduce\n"
                "  - **Apixaban**: Dose reduce if 2 of: age ≥80, weight ≤60kg, Cr ≤1.3 mg/dL\n\n"
                "**Hepatic Dose Adjustment**:\n"
                "- **Child-Pugh classification**: A (mild), B (moderate), C (severe)\n"
                "- **Drugs requiring hepatic adjustment**:\n"
                "  - **Statins**: Avoid if active liver disease, LFT monitoring\n"
                "  - **Amiodarone**: Use caution, monitor LFTs\n"
                "  - **Paracetamol**: Reduce dose to 2g/day if severe liver disease\n"
                "  - **Warfarin**: No adjustment (synthetic liver)\n"
                "  - **DOACs**: Use caution in Child-Pugh B, avoid in C\n"
                "  - **PPIs**: Dose reduction in severe liver disease\n"
                "  - **Antidepressants**: Use caution, dose reduce (except sertraline, escitalopram - safer)\n"
                "  - **Antibiotics**: No adjustment for most (except dose reduction for severe disease)\n"
                "  - **Antiepileptics**: Many require dose reduction (phenytoin, valproate)\n\n"
                "**Geriatric Dosing**:\n"
                "- **Start low, go slow**: Increased sensitivity, decreased clearance\n"
                "- **Renal function**: Declines with age (even if \"normal\" creatinine)\n"
                "- **Beers Criteria**: Drugs to avoid in older adults\n"
                "- **Falls risk**: CNS drugs, anticholinergics, orthostatic hypotension\n"
                "- **Polypharmacy**: Drug interaction risk increased\n"
                "- **Adherence**: Simplify regimen, once-daily if possible\n\n"
                "**Pediatric Dosing**:\n"
                "- **Weight-based dosing**: Most pediatric medications\n"
                "- **Surface area-based**: Some oncologic drugs\n"
                "- **Age-based**: Some OTC medications\n"
                "- **Contraindications**: Some drugs contraindicated in children\n\n"
                "**Pregnancy and Lactation**:\n"
                "- **FDA/EMA pregnancy categories**: A, B, C, D, X\n"
                "- **Teratogenic**: Avoid ACE inhibitors/ARBs (2nd/3rd trimester), warfarin, sodium valproate, retinoids, statins, tetracyclines, fluoroquinolones\n"
                "- **Safe in pregnancy**: Penicillins, cephalosporins, macrolides (azithromycin), most asthma inhalers, paracetamol\n"
                "- **Lactation**: Most drugs compatible (check LactMed, Hale's Medications)\n"
                "- **Avoid**: Codeine (maternal ultra-rapid metabolizer risk)\n\n"
                "**Loading Dose**:\n"
                "- **Purpose**: Rapidly achieve steady-state\n"
                "- **Drugs with loading doses**: Digoxin, amiodarone, phenytoin, some antibiotics\n"
                "- **Calculation**: Loading dose = Target concentration × Volume of distribution\n\n"
                "**Therapeutic Drug Monitoring (TDM)**:\n"
                "- **Warfarin**: INR (target 2-3 for most indications)\n"
                "- **Lithium**: 0.6-1.2 mmol/L (12 hours post-dose)\n"
                "- **Digoxin**: 0.5-2.0 ng/mL (≥6 hours post-dose)\n"
                "- **Phenytoin**: 10-20 mg/L (free level if albumin abnormal)\n"
                "- **Theophylline**: 10-20 mg/L\n"
                "- **Vancomycin**: Trough 10-15 mg/L (15-20 if serious MRSA)\n"
                "- **Aminoglycosides**: Peak and trough levels\n\n"
                "**Disclaimer**: Dosing is individualized. Always consult prescribing information, clinical pharmacist."
            ),
            confidence=0.85,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "dosing",
                "sources": ["BNF", "Drug Prescribing in Renal Failure", "Clinical Pharmacokinetics"]
            }
        )

    def _handle_polypharmacy_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle polypharmacy queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Polypharmacy Review - Pharmacology Second Opinion**\n\n"
                "**Polypharmacy**: Generally defined as ≥5 regular medications.\n\n"
                "**Risks of Polypharmacy**:\n"
                "- **Drug-drug interactions**: Increased with more drugs\n"
                "- **Cumulative side effects**: Additive toxicities\n"
                "- **Prescribing cascade**: Treating side effects with more drugs\n"
                "- **Adherence**: More complex regimen, lower adherence\n"
                "- **Falls**: Especially CNS drugs, anticholinergics, orthostatic drugs\n"
                "- **Cognitive impairment**: Anticholinergic burden\n"
                "- **Mortality**: Increased mortality with inappropriate polypharmacy\n\n"
                "**Deprescribing Principles**:\n"
                "1. **Identify inappropriate medications**:\n"
                "   - No clear indication\n"
                "   - Ineffective (no benefit despite adequate trial)\n"
                "   - Harm outweighs benefit\n"
                "   - Duplicated therapy (two drugs in same class)\n"
                "   - Not tolerated (side effects)\n"
                "   - No longer needed (treatment completed)\n"
                "   - Patient preference\n"
                "   - Goal of care changed (palliative vs curative)\n\n"
                "2. **Prioritize**: Which drugs to deprescribe first\n"
                "   - Highest risk drugs\n"
                "   - Drugs with least evidence\n"
                "   - Drugs patient most wants to stop\n\n"
                "3. **Plan**: Taper slowly, monitor for withdrawal/discontinuation syndrome\n"
                "   - **Rapid taper**: Days to weeks (antihypertensives, Parkinson drugs)\n"
                "   - **Slow taper**: Weeks to months (antidepressants, benzodiazepines, antiepileptics)\n\n"
                "4. **Monitor**: Watch for recurrence of symptoms, withdrawal\n\n"
                "5. **Support**: Non-pharmacological alternatives\n\n"
                "**Common Inappropriate Prescribing in Elderly** (Beers Criteria):\n"
                "- **Anticholinergics**: Amitriptyline, oxybutynin, diphenhydramine, bladder antimuscarinics, first-generation antihistamines\n"
                "- **Benzodiazepines**: Falls, cognitive impairment, safer alternatives exist\n"
                "- **Z-drugs**: Similar risks to benzodiazepines\n"
                "- **NSAIDs**: GI bleed, renal impairment, HF exacerbation, hypertension\n"
                "- **Digoxin**: >0.125 mg/day if eGFR <30\n"
                "- **Sulfonylureas**: Hypoglycemia risk (glipizide > glyburide)\n"
                "- **Muscle relaxants**: Anticholinergic, sedation\n"
                "- **Antipsychotics for dementia**: Stroke risk, mortality\n"
                "- **Barbiturates**: Falls, respiratory depression\n"
                "- **Meperidine (pethidine)**: Toxic metabolites\n"
                "- **Chlorpropamide**: Hypoglycemia, SIADH\n"
                "- **Antispasmodics**: Anticholinergic burden\n\n"
                "**Medication Review Process**:\n"
                "1. **Comprehensive list**: Prescription, OTC, herbal, supplements\n"
                "2. **Indication**: Why is each drug prescribed?\n"
                "3. **Effectiveness**: Is it working?\n"
                "4. **Adverse effects**: Any side effects?\n"
                "5. **Interactions**: Any drug-drug interactions?\n"
                "6. **Necessity**: Can any be discontinued?\n"
                "7. **Optimization**: Can regimen be simplified?\n\n"
                "**Simplification Strategies**:\n"
                "- **Once-daily dosing**: If possible\n"
                "- **Combination pills**: Fixed-dose combinations (e.g., ACEi + HCTZ)\n"
                "- **Pill organizers**: Improve adherence\n"
                "- **Align medication times**: Reduce dosing frequency\n"
                "- **Deprescribe**: Eliminate unnecessary drugs\n\n"
                "**Specific Deprescribing Examples**:\n"
                "- **PPIs**: Deprescribe if no clear indication, trial of taper (rebound acid possible)\n"
                "- **Antidepressants**: Taper slowly (over weeks-months) to avoid discontinuation syndrome\n"
                "- **Benzodiazepines**: Taper slowly (10-25% dose reduction weekly/monthly)\n"
                "- **Antipsychotics**: Taper slowly (risk of withdrawal psychosis)\n"
                "- **Dementia medications**: Reassess if no clear benefit, cholinesterase inhibitors, memantine\n"
                "- **Antihypertensives**: If hypotensive, reduce dose (especially if multiple)\n"
                "- **Statins**: In palliative care, limited life expectancy\n\n"
                "**Disclaimer**: Deprescribing requires careful planning. Consult pharmacist/physician."
            ),
            confidence=0.87,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "polypharmacy",
                "sources": ["Beers Criteria", "STOPP/START Criteria", "Deprescribing Guidelines"]
            }
        )

    def _handle_drug_class_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle drug class-specific queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Pharmacology Consultation - Drug Classes**\n\n"
                "**Common Drug Class Considerations**:\n\n"
                "**Antibiotics**:\n"
                "- **Duration**: Shortest effective duration (stewardship)\n"
                "- **Renal dose**: Most require adjustment\n"
                "- **Interactions**: Macrolides (QT prolongation, statins), fluoroquinolones (QT prolongation, divalent cations)\n"
                "- **C. difficile risk**: Any antibiotic, especially clindamycin, fluoroquinolones, cephalosporins\n"
                "- **Resistance**: Avoid if viral infection\n\n"
                "**Anticoagulants**:\n"
                "- **Warfarin**: INR monitoring, many interactions (antibiotics, amiodarone, SSRIs, NSAIDs), vitamin K diet\n"
                "- **DOACs**: No monitoring, fewer interactions, dose adjust for renal function\n"
                "- **Bleeding risk**: All anticoagulants, increased with NSAIDs, antiplatelets, SSRIs\n"
                "- **Reversal**: Warfarin (vitamin K, prothrombin complex concentrate), DOACs (idarucizumab for dabigatran, andexanet alfa for apixaban/rivaroxaban)\n\n"
                "**Antiplatelets**:\n"
                "- **Aspirin**: 75mg daily (secondary prevention), GI bleed risk, consider PPI\n"
                "- **Clopidogrel**: Prodrug, CYP2C19 interactions (PPIs except pantoprazole), aspirin + clopidogrel (DAPT)\n"
                "- **Prasugrel, ticagrelor**: More potent, more bleeding, DAPT for ACS\n\n"
                "**Statins**:\n"
                "- **Indications**: ASCVD risk ≥7.5%, diabetes, LDL ≥190, known ASCVD\n"
                "- **Monitoring**: LFTs at baseline, if symptomatic\n"
                "- **Interactions**: CYP3A4 inhibitors (increase myopathy risk), grapefruit juice\n"
                "- **Contraindications**: Active liver disease, pregnancy\n\n"
                "**Opioids**:\n"
                "- **Indications**: Severe acute pain, cancer pain, palliative care (NOT chronic non-cancer pain)\n"
                "- **Risks**: Respiratory depression, addiction, overdose, constipation, nausea, sedation, endocrine effects\n"
                "- **Safer alternatives**: NSAIDs, acetaminophen, duloxetine, gabapentin, physical therapy\n"
                "- **If prescribed**: Lowest effective dose, shortest duration, avoid concurrent benzodiazepines, naloxone available\n"
                "- **Monitoring**: Prescription drug monitoring program (PDMP), urine drug screening, opioid agreements\n\n"
                "**Antidepressants**:\n"
                "- **SSRIs**: First-line (except in pregnancy, consider sertraline/escitalopram), sexual dysfunction (25-50%), GI upset (early), discontinuation syndrome (taper)\n"
                "- **SNRIs**: Venlafaxine (dose-dependent BP increase), duloxetine (many drug interactions)\n"
                "- **Tricyclics**: Amitriptyline (off-label neuropathic pain), anticholinergic side effects, overdose risk\n"
                "- **MAOIs**: Rarely used, many drug-food interactions, hypertensive crisis with tyramine\n"
                "- **Bupropion**: Contraindicated with eating disorder, seizure disorder\n\n"
                "**Benzodiazepines**:\n"
                "- **Indications**: Severe anxiety, insomnia (short-term), alcohol withdrawal, seizures\n"
                "- **NOT first-line**: For chronic anxiety/insomnia (CBT preferred)\n"
                "- **Risks**: Sedation, falls, cognitive impairment, dependence, withdrawal\n"
                "- **Withdrawal**: Taper slowly (can be life-threatening if abrupt stop)\n"
                "- **Driving**: May be impaired, avoid if sedated\n\n"
                "**Beta-blockers**:\n"
                "- **Non-selective**: Propranolol (contraindicated in asthma, COPD)\n"
                "- **Cardioselective**: Bisoprolol, metoprolol (safer in lung disease)\n"
                "- **Side effects**: Fatigue, bradycardia, cold extremities, sexual dysfunction, mask hypoglycemia symptoms\n"
                "- **Abrupt withdrawal**: Can cause rebound tachycardia, hypertension, angina\n\n"
                "**ACE Inhibitors/ARBs**:\n"
                "- **ACEi cough**: 5-20%, switch to ARB\n"
                "- **Angioedema**: Rare (<1%), contraindicates all ACE inhibitors\n"
                "- **Hyperkalemia**: Monitor K+ if renal impairment, diabetes, concurrent K+-sparing drugs\n"
                "- **Renal protection**: Beneficial in diabetes, proteinuric CKD\n\n"
                "**PPIs**:\n"
                "- **Indications**: PUD, GORD, erosive esophagitis, H. pylori eradication, NSAID prophylaxis\n"
                "- **Risks**: Hypomagnesemia, B12 deficiency (long-term), C. difficile infection, bone fracture (long-term, high-dose), dementia (controversial)\n"
                "- **Deprescribing**: Reassess if on long-term (>8 weeks), trial of taper\n"
                "- **Interactions**: Clopidogrel (omeprazole, esomeprazole reduce activation, avoid)\n\n"
                "**Disclaimer**: Drug class selection individualized. Consult prescriber/pharmacist."
            ),
            confidence=0.85,
            metadata={
                "specialty": "pharmacology",
                "sources": ["BNF", "Clinical Pharmacology", "Therapeutic Guidelines"]
            }
        )

    def _handle_contraindications_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle contraindication queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Contraindications and Precautions - Pharmacology Second Opinion**\n\n"
                "**Absolute Contraindications** (Do NOT prescribe):\n\n"
                "**Drug Allergy**:\n"
                "- **Penicillin allergy**: Avoid all penicillins, cephalosporins (if true allergy/anaphylaxis)\n"
                "- **Sulfonamide allergy**: Avoid sulfonylureas, thiazides, sulfa-antibiotics, celecoxib\n"
                "- **NSAID allergy**: Avoid all NSAIDs, aspirin (if aspirin-exacerbated respiratory disease)\n"
                "- **ACE inhibitor angioedema**: Contraindicates all ACE inhibitors (may consider ARB if no previous angioedema)\n\n"
                "**Pregnancy (Teratogenic Drugs)**:\n"
                "- **ACE inhibitors/ARBs**: 2nd/3rd trimester (renal failure, oligohydramnios, fetal death)\n"
                "- **Warfarin**: All trimesters (embryopathy, 1st; hemorrhage, 2nd/3rd)\n"
                "- **Sodium valproate**: Neural tube defects, cognitive impairment\n"
                "- **Retinoids**: Isotretinoin, acitretin (teratogenic, pregnancy prevention program required)\n"
                "- **Statins**: Pregnancy (LFT abnormalities, limited data)\n"
                "- **Tetracyclines**: Discolored teeth, inhibited bone growth\n"
                "- **Fluoroquinolones**: Tendonopathy, cartilage damage (animal data)\n"
                "- **Methotrexate**: Abortion, fetal death\n\n"
                "**Specific Conditions**:\n"
                "- **Asthma/COPD**: Non-selective beta-blockers (propranolol) contraindicated\n"
                "- **2nd/3rd degree AV block**: Beta-blockers, verapamil, diltiazem contraindicated\n"
                "- **Severe renal failure (CrCl <30)**: DOACs contraindicated (drug-specific)\n"
                "- **Severe liver disease (Child-Pugh C)**: DOACs, statins contraindicated\n"
                "- **Porphyria**: Barbiturates, sulfonamides contraindicated\n"
                "- **G6PD deficiency**: Sulfonamides, dapsone, nitrofurantoin contraindicated\n"
                "- **Myasthenia gravis**: Fluoroquinolones contraindicated\n"
                "- **Long QT syndrome**: QT-prolonging drugs contraindicated\n"
                "- **Pheochromocytoma**: Non-selective beta-blockers alone contraindicated (give alpha-blocker first)\n"
                "- **Closed-angle glaucoma**: Anticholinergics contraindicated\n"
                "- **BPH**: Anticholinergics contraindicated (can cause urinary retention)\n\n"
                "**Relative Contraindications** (Use with caution, alternatives preferred):\n\n"
                "**Elderly (Beers Criteria)**:\n"
                "- Anticholinergics: Falls, cognitive impairment\n"
                "- Benzodiazepines: Falls, cognitive impairment, safer alternatives\n"
                "- Z-drugs: Similar risks to benzodiazepines\n"
                "- NSAIDs: GI bleed, renal impairment, HF exacerbation\n"
                "- Skeletal muscle relaxants: Anticholinergic, sedation\n"
                "- Digoxin: If dose >0.125 mg and eGFR <30\n"
                "- Antipsychotics for dementia: Stroke risk, mortality\n\n"
                "**Renal Impairment**:\n"
                "- **Dose adjust**: Most antibiotics, antivirals, direct Xa inhibitors, DOACs, colchicine, gabapentin/pregabalin, allopurinol, many others\n"
                "- **Avoid**: If possible, drugs with nephrotoxic potential (NSAIDs, aminoglycosides, amphotericin, iodinated contrast if alternatives)\n\n"
                "**Hepatic Impairment**:\n"
                "- **Dose reduce/avoid**: Statins (active liver disease), amiodarone, paracetamol (reduce dose), warfarin (no adjustment), DOACs (Child-Pugh C avoid), many others\n\n"
                "**Heart Failure**:\n"
                "- **Avoid**: NSAIDs (fluid retention, worsen HF), thiazolidinediones (fluid retention), dronedarone (NYHA III-IV)\n"
                "- **Use with caution**: Calcium channel blockers (negative inotropy)\n"
                "- **Prefer**: Beta-blockers, ACE inhibitors/ARBs, aldosterone antagonists (if HFrEF)\n\n"
                "**Precautions** (Monitoring required):\n"
                "- **Warfarin**: Many drug interactions, INR monitoring\n"
                "- **Lithium**: Renal function, thyroid function, serum level, drug interactions\n"
                "- **Digoxin**: Renal function, serum level, electrolytes (hypokalemia increases toxicity)\n"
                "- **Phenytoin**: Serum level, therapeutic range narrow, protein binding changes in hypoalbuminemia\n"
                "- **Theophylline**: Serum level, narrow therapeutic index\n"
                "- **Aminoglycosides**: Serum levels, renal function, ototoxicity\n"
                "- **Vancomycin**: Serum levels (trough), renal function\n"
                "- **Amiodarone**: LFTs, TFTs, CXR (pulmonary toxicity), ECG (QT prolongation), ophthalmologic exam (corneal deposits)\n"
                "- **Statins**: LFTs at baseline, if symptomatic (rare hepatotoxicity)\n"
                "- **Methotrexate**: CBC, LFTs, renal function\n"
                "- **Azathioprine**: TPMT testing (risk of myelosuppression)\n"
                "- **Carbamazepine**: CBC (risk of aplastic anemia), LFTs, serum level\n\n"
                "**Disclaimer**: Contraindications individualized. Consider risk-benefit ratio."
            ),
            confidence=0.86,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "contraindications",
                "sources": ["BNF", "MIMS", "Drug Prescribing in Renal Failure"]
            }
        )

    def _handle_safety_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle medication safety queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Medication Safety - Pharmacology Second Opinion**\n\n"
                "**Principles of Safe Prescribing**:\n\n"
                "**1. Right Drug**:\n"
                "- **Indication**: Clear indication for prescribing\n"
                "- **Evidence-based**: Use first-line drugs when possible\n"
                "- **Avoid**: Duplicate therapy (two drugs in same class)\n"
                "- **Contraindications**: Check for absolute and relative contraindications\n\n"
                "**2. Right Dose**:\n"
                "- **Start low, go slow**: Especially in elderly, renal/hepatic impairment\n"
                "- **Renal dose adjustment**: Check CrCl/eGFR, adjust drugs cleared renally\n"
                "- **Hepatic dose adjustment**: Use caution in liver disease\n"
                "- **Therapeutic drug monitoring**: When appropriate (warfarin, lithium, digoxin, phenytoin)\n\n"
                "**3. Right Route**:\n"
                "- **Oral**: Preferred route (if patient can take)\n"
                "- **Parenteral**: IV/IM if oral not possible, faster onset, higher risk\n"
                "- **Topical**: Local effect, minimal systemic absorption\n\n"
                "**4. Right Frequency**:\n"
                "- **Once-daily**: Preferred (improves adherence)\n"
                "- **Simplify**: Align medication times\n"
                "- **Pill organizers**: Improve adherence\n\n"
                "**5. Right Duration**:\n"
                "- **Antibiotics**: Shortest effective duration (stewardship)\n"
                "- **Opioids**: Shortest duration, lowest effective dose\n"
                "- **PPIs**: Reassess if on long-term (>8 weeks)\n"
                "- **Benzodiazepines**: Short-term only, reassess regularly\n\n"
                "**Medication Reconciliation**:\n"
                "- **Admission**: Comprehensive medication list (prescription, OTC, herbal)\n"
                "- **Discharge**: Review medications, reconcile with admission list\n"
                "- **Transitions of care**: Ensure medication continuity\n\n"
                "**High-Alert Medications** (ISMP Institute for Safe Medication Practices):\n"
                "- **Anticoagulants**: Warfarin, DOACs, heparin\n"
                "- **Concentrated electrolytes**: Potassium chloride, magnesium sulfate, sodium chloride >0.9%\n"
                "- **Insulin**: Subcutaneous and IV (risk of hypoglycemia)\n"
                "- **Opioids**: IV and oral (risk of respiratory depression)\n"
                "- **Chemotherapeutic agents**: Cytotoxic drugs\n"
                "- **Neuromuscular blocking agents**: Vecuronium, rocuronium, succinylcholine\n"
                "- **Moderate sedation agents**: Propofol, midazolam, fentanyl\n"
                "- **Dopamine agonists**: Dopamine, dobutamine\n\n"
                "**Look-Alike Sound-Alike (LASA) Drugs**:\n"
                "- **Hydrochlorothiazide** vs **Hydralazine**\n"
                "- **Lamotrigine** vs **Labetalol**, **Lamivudine**, **Lomotil**\n"
                "- **Metformin** vs **Metronidazole**, **Metoprolol**, **Methotrexate**, **Morphine**\n"
                "- **Prednisolone** vs **Prednisone** vs **Prilosec** (omeprazole)\n"
                "- **Sertraline** vs **Sertindole**, **Sirukumab**\n"
                "- **Zolpidem** vs **Zopiclone** vs **Zolmitriptan**\n"
                "- **Tall Man Lettering**: Use to distinguish (e.g., predniSONE vs prednisoLONE)\n\n"
                "**Black Box Warnings** (FDA)\n"
                "- **Antidepressants**: Suicidality in children, adolescents, young adults\n"
                "- **NSAIDs**: Cardiovascular thrombotic events, GI bleeding\n"
                "- **Anticoagulants**: Spinal/epidural hematoma (with neuraxial anesthesia)\n"
                "- **Fluoroquinolones**: Tendonitis, tendon rupture, peripheral neuropathy, CNS effects\n"
                "- **Metformin**: Lactic acidosis\n"
                "- **Statins**: Liver injury, myopathy/rhabdomyolysis\n"
                "- **Opioids**: Addiction, abuse, misuse, respiratory depression\n"
                "- **Benzodiazepines**: Risks of concomitant use with opioids\n"
                "- **PPIs**: C. difficile-associated diarrhea, hypomagnesemia\n"
                "- **Leuprorelin**: Psychiatric events\n"
                "- **Montelukast**: Neuropsychiatric events\n"
                "- **Beta agonists**: Asthma-related death\n"
                "- **Antipsychotics**: Mortality in dementia-related psychosis\n"
                "- **Carbamazepine**: Stevens-Johnson syndrome, toxic epidermal necrolysis\n"
                "- **Lamotrigine**: Stevens-Johnson syndrome, toxic epidermal necrolysis\n"
                "- **Valproate**: Hepatic failure, pancreatitis, neural tube defects\n"
                "- **Phenytoin**: Stevens-Johnson syndrome, toxic epidermal necrolysis\n"
                "- **Sulfonamides**: Stevens-Johnson syndrome, toxic epidermal necrolysis\n"
                "- **Allopurinol**: Stevens-Johnson syndrome, toxic epidermal necrolysis\n"
                "- **Abciximab**: Severe bleeding\n"
                "- **Rituximab**: PML (progressive multifocal leukoencephalopathy)\n"
                "- **TNF inhibitors**: TB, fungal infections, other opportunistic infections\n\n"
                "**Medication Errors Prevention**:\n"
                "- **Read**: Label carefully (drug name, strength, dose, route, frequency, patient)\n"
                "- **Write**: Clearly, avoid abbreviations (use \"units\" not \"U\")\n"
                "- **Check**: Patient identity, drug allergies, interactions, dose, route\n"
                "- **Barcode scanning**: If available\n"
                "- **Double-check**: High-alert medications\n"
                "- **Educate**: Patient about medication (purpose, dose, side effects)\n\n"
                "**Adverse Drug Reaction Reporting**:\n"
                "- **UK**: Yellow Card Scheme (MHRA)\n"
                "- **US**: MedWatch (FDA)\n"
                "- **Purpose**: Identify rare/late adverse reactions\n"
                "- **Serotonin syndrome**: SSRIs/SNRIs + tramadol, linezolid, MAOIs\n"
                "- **Neuroleptic malignant syndrome**: Antipsychotics\n"
                "- **Stevens-Johnson syndrome/TEN**: Lamotrigine, carbamazepine, allopurinol, sulfonamides\n"
                "- **Rhabdomyolysis**: Statins (especially with interactions)\n"
                "- **Torsades de pointes**: QT-prolonging drugs\n"
                "- **Anaphylaxis**: Penicillins, others\n"
                "- **Agranulocytosis**: Clozapine, carbimazole\n"
                "- **Aplastic anemia**: Carbamazepine\n"
                "- **Malignant hyperthermia**: Succinylcholine, volatile anesthetics\n\n"
                "**Disclaimer**: Medication safety requires vigilance. Report all suspected ADRs."
            ),
            confidence=0.87,
            metadata={
                "specialty": "pharmacology",
                "subspecialty": "medication_safety",
                "sources": ["ISMP", "BNF", "MHRA Yellow Card", "FDA MedWatch"]
            }
        )

    def _handle_general_pharmacology_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general pharmacology queries."""
        return DomainQueryResult(
            domain_name="pharmacology",
            answer=(
                "**Pharmacology Consultation - Second Opinion**\n\n"
                "I provide consultation on:\n\n"
                "**Drug Interactions**:\n"
                "- Drug-drug interactions\n"
                "- Drug-food interactions (grapefruit juice, tyramine)\n"
                "- Drug-herbal interactions (St. John's wort, ginkgo)\n"
                "- Drug-disease interactions (renal, hepatic, cardiac)\n\n"
                "**Side Effects**:\n"
                "- Common and serious side effects\n"
                "- Side effect management strategies\n"
                "- Adverse drug reaction assessment\n\n"
                "**Dosing**:\n"
                "- Standard dosing\n"
                "- Renal dose adjustment\n"
                "- Hepatic dose adjustment\n"
                "- Geriatric dosing\n"
                "- Pediatric dosing\n"
                "- Therapeutic drug monitoring\n\n"
                "**Medication Safety**:\n"
                "- Contraindications\n"
                "- Precautions\n"
                "- Black box warnings\n"
                "- High-alert medications\n"
                "- Medication errors prevention\n\n"
                "**Polypharmacy**:\n"
                "- Medication review\n"
                "- Deprescribing\n"
                "- Prescribing cascade\n"
                "- Drug burden assessment\n\n"
                "**Specific Drug Classes**:\n"
                "- Antibiotics\n"
                "- Anticoagulants/antiplatelets\n"
                "- Analgesics (NSAIDs, opioids)\n"
                "- Cardiovascular drugs\n"
                "- Psychotropics\n"
                "- Others\n\n"
                "**Please provide**: Medication list (including doses), medical history, "
                "renal/hepatic function, age, specific questions.\n\n"
                "**Privacy**: All data stored locally.\n"
                "**Medical Disclaimer**: This is second opinion. Consult prescriber/pharmacist."
            ),
            confidence=0.85,
            metadata={
                "specialty": "pharmacology",
                "sources": ["BNF", "Clinical Pharmacology", "Therapeutic Guidelines"]
            }
        )

    def _extract_medications_from_query(self, query: str) -> List[str]:
        """
        Extract medication names from query text

        Args:
            query: User query text

        Returns:
            List of medication names found
        """
        import re

        # Common medication names to look for
        medication_keywords = [
            # Common cardiovascular
            "warfarin", "simvastatin", "atorvastatin", "ramipril", "lisinopril",
            "bisoprolol", "atenolol", "amlodipine", "losartan", "candesartan",
            "furosemide", "spironolactone", "diltiazem", "verapamil",
            "digoxin", "amiodarone",
            # Anticoagulants
            "apixaban", "rivaroxaban", "edoxaban", "dabigatran", "clopidogrel",
            # NSAIDs
            "ibuprofen", "naproxen", "diclofenac", "celecoxib",
            # Antibiotics
            "clarithromycin", "erythromycin", "azithromycin", "amoxicillin",
            "ciprofloxacin", "doxycycline", "gentamicin", "amikacin",
            # Psychotropics
            "citalopram", "fluoxetine", "sertraline", "paroxetine", "escitalopram",
            "fluvoxamine", "venlafaxine", "mirtazapine", "diazepam",
            # Others
            "lithium", "tramadol", "codeine", "morphine", "metformin",
            "levothyroxine", "thyroxine", "omeprazole", "esomeprazole",
            "lansoprazole", "aspirin", "insulin", "gtn", "glyceryl trinitrate",
            "sildenafil", "tadalafil", "prednisolone", "beclometasone"
        ]

        query_lower = query.lower()
        medications_found = []

        # Direct matches
        for med in medication_keywords:
            if med in query_lower:
                medications_found.append(med)

        # Pattern matching for drug names in query
        # Look for patterns like "X and Y", "X with Y", "X, Y", "take X with Y"
        patterns = [
            r'(?:interact?:?\s+(?:between|with)?|check:?\s+(?:interact?:?\s+(?:between|with)?)?)([a-z\s,]+(?:\?|$))',
            r'(?:can|i)\s+(?:i\s+)?take\s+([a-z]+)(?:\s+with\s+([a-z]+))?',
            r'(?:is\s+)?([a-z]+)\s+safe\s+(?:with|for)?\s+([a-z]+)?',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, query_lower)
            for match in matches:
                if isinstance(match, tuple):
                    for m in match:
                        if m and m not in medications_found:
                            medications_found.append(m.strip())
                else:
                    if match and match not in medications_found:
                        medications_found.append(match.strip())

        # Remove duplicates while preserving order
        seen = set()
        unique_medications = []
        for med in medications_found:
            if med not in seen:
                seen.add(med)
                unique_medications.append(med)

        return unique_medications


def create_pharmacology_domain():
    """Factory function for creating pharmacology domain instances."""
    return PharmacologyDomain()
