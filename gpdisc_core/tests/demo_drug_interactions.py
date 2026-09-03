#!/usr/bin/env python3
"""
GPDISC Drug-Drug Interaction Checker Demonstration

Demonstrates the automated drug interaction checking system for patient safety.

Features:
- Comprehensive interaction database (UK-focused)
- Severity levels (Severe, Moderate, Mild, Contraindicated)
- Evidence-based recommendations
- Integration with patient records
- Automatic safety checking

All checks performed locally - no external API calls.
"""

from gpdisc_core.safety.drug_interactions import (
    check_drugs_interact,
    check_patient_medications,
    check_new_prescription,
    create_interaction_checker
)


def demo_check_two_drugs():
    """Demonstrate checking interaction between two specific drugs"""
    print("=" * 70)
    print("Checking Interaction: Warfarin + Ibuprofen")
    print("=" * 70)

    interaction = check_drugs_interact("warfarin", "ibuprofen")

    if interaction:
        severity_icon = {
            "severe": "🔴",
            "moderate": "🟠",
            "mild": "🟡",
            "contraindicated": "🚨"
        }.get(interaction.severity.value, "⚪")

        print(f"\n{severity_icon} INTERACTION DETECTED")
        print(f"Drugs: {interaction.drug1} + {interaction.drug2}")
        print(f"Severity: {interaction.severity.value.upper()}")
        print(f"Evidence: {interaction.evidence.value}")
        print(f"\nDescription: {interaction.description}")
        print(f"Mechanism: {interaction.mechanism}")
        print(f"\nClinical Effects:")
        for effect in interaction.clinical_effects:
            print(f"  • {effect}")
        print(f"\nRecommendations:")
        for rec in interaction.recommendations[:5]:
            print(f"  • {rec}")
        print(f"\nManagement: {interaction.management}")
        print(f"Onset: {interaction.onset}")
        print(f"\nReferences: {', '.join(interaction.references)}")
    else:
        print("✅ No interaction detected")


def demo_patient_medication_list():
    """Demonstrate checking entire patient medication list"""
    print("\n" + "=" * 70)
    print("Checking Patient Medication List for Interactions")
    print("=" * 70)

    patient_medications = [
        "warfarin",
        "simvastatin",
        "ramipril",
        "ibuprofen",
        "aspirin"
    ]

    print(f"\nPatient Medications:")
    for i, med in enumerate(patient_medications, 1):
        print(f"  {i}. {med.capitalize()}")

    result = check_patient_medications(patient_medications)

    print(f"\n{result.summary}")

    if result.interactions:
        print("\n" + "=" * 70)
        print("DETAILED INTERACTIONS:")
        print("=" * 70)

        for interaction in result.interactions:
            print(f"\n• {interaction.drug1} + {interaction.drug2}")
            print(f"  Severity: {interaction.severity.value.upper()}")
            print(f"  {interaction.description}")
            print(f"  Management: {interaction.management}")


def demo_check_new_prescription():
    """Demonstrate checking if new medication is safe with current meds"""
    print("\n" + "=" * 70)
    print("Checking New Prescription Against Current Medications")
    print("=" * 70)

    current_medications = [
        "warfarin",
        "simvastatin",
        "ramipril"
    ]

    new_prescription = "clarithromycin"  # Antibiotic

    print(f"\nCurrent Medications:")
    for med in current_medications:
        print(f"  • {med.capitalize()}")

    print(f"\nNew Prescription: {new_prescription.capitalize()}")

    result = check_new_prescription(current_medications, new_prescription)

    print(f"\n{result.summary}")

    if result.has_interactions:
        print("\n" + "=" * 70)
        print("PRESCRIPTION RECOMMENDATIONS:")
        print("=" * 70)

        for i, rec in enumerate(result.recommendations, 1):
            print(f"{i}. {rec}")


def demo_contraindicated_combinations():
    """Demonstrate life-threatening contraindicated combinations"""
    print("\n" + "=" * 70)
    print("CONTRAINDICATED COMBINATIONS (Never Use Together)")
    print("=" * 70)

    dangerous_combinations = [
        ("sildenafil", "glyceryl trinitrate"),
        ("clarithromycin", "simvastatin"),
        ("spironolactone", "ramipril")  # Hyperkalaemia risk
    ]

    print("\nChecking contraindicated combinations:\n")

    for drug1, drug2 in dangerous_combinations:
        print(f"Checking: {drug1} + {drug2}")
        interaction = check_drugs_interact(drug1, drug2)

        if interaction and interaction.severity.value == "contraindicated":
            print(f"  🚨 {interaction.severity.value.upper()}")
            print(f"  {interaction.description}")
            print(f"  → {interaction.management}")
        else:
            print(f"  ⚠ Unexpected result")
        print()


def demo_realistic_clinical_scenario():
    """Demonstrate realistic clinical scenario"""
    print("\n" + "=" * 70)
    print("CLINICAL SCENARIO: Patient with Multiple Conditions")
    print("=" * 70)

    print("""
Patient: 74-year-old woman

Medical History:
- Atrial fibrillation (on warfarin)
- Hypertension (on ramipril)
- Hypercholesterolaemia (on simvastatin)
- Osteoarthritis (occasional NSAID use)
- Recent diagnosis: Community-acquired pneumonia

Scenario: GP considering prescribing clarithromycin
    """)

    current_meds = ["warfarin", "ramipril", "simvastatin"]
    new_antibiotic = "clarithromycin"

    print(f"Current Medications: {', '.join(current_meds)}")
    print(f"Proposed Addition: {new_antibiotic}")

    print("\n" + "-" * 70)
    print("SAFETY CHECK:")
    print("-" * 70)

    result = check_new_prescription(current_meds, new_antibiotic)

    print(f"\n{result.summary}")

    if result.has_interactions:
        print("\n" + "=" * 70)
        print("CLINICAL DECISION SUPPORT:")
        print("=" * 70)

        for interaction in result.interactions:
            print(f"\n{interaction.drug1} + {interaction.drug2}:")
            print(f"  RISK: {interaction.severity.value.upper()}")
            print(f"  MECHANISM: {interaction.mechanism}")
            print(f"  WHAT TO DO:")
            for rec in interaction.recommendations[:3]:
                print(f"    • {rec}")

        print("\n" + "=" * 70)
        print("RECOMMENDED ACTION:")
        print("=" * 70)
        print("""
Given multiple interactions (Warfarin + Simvastatin + Clarithromycin):

1. STOP simvastatin temporarily during antibiotic course
2. INCREASE INR monitoring frequency (every 2-3 days)
3. EDUCATE patient on bleeding signs
4. CONSIDER alternative antibiotic (azithromycin has fewer interactions)
5. MONITOR renal function (ACEI + NSAID risk if patient uses NSAIDs)

Follow-up: Check INR in 3 days, clinical review in 1 week
        """)


def demo_interaction_checker_direct():
    """Demonstrate using interaction checker directly"""
    print("\n" + "=" * 70)
    print("Using Interaction Checker Directly")
    print("=" * 70)

    checker = create_interaction_checker()

    # Example 1: Check specific interaction
    print("\nExample 1: Specific Interaction Check")
    interaction = checker.check_interaction("lithium", "ramipril")
    if interaction:
        print(f"✓ Found: {interaction.drug1} + {interaction.drug2}")
        print(f"  Severity: {interaction.severity.value}")
        print(f"  Description: {interaction.description}")

    # Example 2: Check patient list
    print("\nExample 2: Patient Medication List")
    patient_meds = ["lithium", "carbamazepine", "sertraline"]
    result = checker.check_patient_medication_list(patient_meds)
    print(f"✓ Checked {len(result.medications_checked)} medications")
    print(f"  Interactions found: {len(result.interactions)}")

    # Example 3: Generate report
    if result.has_interactions:
        report = checker.generate_interaction_report(result)
        print("\nInteraction Report Generated (first 500 chars):")
        print(report[:500] + "...")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("GPDISC Drug-Drug Interaction Checker Demonstration")
    print("=" * 70)
    print("\n🔒 Privacy Notice:")
    print("- All interaction checks performed locally")
    print("- No external API calls or data transmission")
    print("- Evidence-based: BNF 75, NICE, MHRA")
    print("- UK-focused interaction database")
    print("=" * 70)

    # Run demonstrations
    demo_check_two_drugs()
    demo_patient_medication_list()
    demo_check_new_prescription()
    demo_contraindicated_combinations()
    demo_realistic_clinical_scenario()
    demo_interaction_checker_direct()

    print("\n" + "=" * 70)
    print("Demonstration Complete")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("✓ Two-drug interaction checking")
    print("✓ Patient medication list analysis")
    print("✓ New prescription safety checking")
    print("✓ Contraindicated combination detection")
    print("✓ Clinical decision support")
    print("✓ Evidence-based recommendations")
    print("✓ Severity-based warnings")
    print("=" * 70)
    print("\nThe Drug-Drug Interaction Checker is integrated with the")
    print("Pharmacology domain for automatic safety checking during")
    print("medical consultations.")
    print("=" * 70)


if __name__ == "__main__":
    main()
