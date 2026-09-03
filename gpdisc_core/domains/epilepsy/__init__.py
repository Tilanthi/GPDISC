"""
Epilepsy Domain Module for GPDISC
=====================================

This domain specializes in seizure disorders, epilepsy diagnosis and treatment,
EEG interpretation, and antiepileptic medication management.

Key capabilities:
- Seizure classification and diagnosis
- EEG interpretation
- Antiepileptic medication management
- Seizure first aid and safety
- Epilepsy syndrome recognition
- Differential diagnosis of seizure-like events
- Treatment-resistant epilepsy evaluation
- Pre-surgical evaluation considerations

Privacy: All patient data stored locally, no external transmission.
"""

from typing import Dict, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class EpilepsyDomain(BaseDomainModule):
    """
    Epilepsy domain specializing in seizure disorders and neurological consultation.

    This domain provides medical consultation on epilepsy, seizure classification,
    EEG interpretation, and antiepileptic medication management.
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="epilepsy",
            version="1.0.0",
            dependencies=[],
            description="Seizure disorders, epilepsy diagnosis, EEG interpretation, antiepileptic medication management",
            keywords=[
                "seizure", "epilepsy", "convulsion", "fit", "antiepileptic", "aeds",
                "eeg", "electroencephalogram", "ictal", "postictal", "preictal",
                "aura", "focal seizure", "generalized seizure", "tonic-clonic",
                "absence seizure", "myoclonic", "atonic", "tonic", "clonic",
                "status epilepticus", "febrile seizure", "neurology", "brain",
                "neuron", "epileptiform", "sharp wave", "spike", "slow wave",
                "temporal lobe epilepsy", "frontal lobe epilepsy", "juvenile myoclonic",
                "lennox-gastaut", "dravet syndrome", "epilepsy surgery",
                "vns", "vagus nerve stimulator", "ketogenic diet", "carbamazepine",
                "lamotrigine", "levetiracetam", "sodium valproate", "phenytoin",
                "phenobarbital", "topiramate", "brivaracetam", "lacosamide",
                "clobazam", "clonazepam", "pregabalin", "gabapentin"
            ],
            capabilities=[
                "seizure_classification",
                "epilepsy_diagnosis",
                "eeg_interpretation",
                "treatment_options",
                "medication_management",
                "seizure_first_aid",
                "differential_diagnosis",
                "epilepsy_syndrome_recognition"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """Process epilepsy-related queries with specialized consultation."""
        try:
            query_lower = query.lower()

            # Seizure classification
            if any(term in query_lower for term in ["type of seizure", "seizure type", "classify", "classification"]):
                return self._handle_classification_query(query, context)

            # Treatment/medication
            elif any(term in query_lower for term in ["treatment", "medication", "drug", "aeds", "antiepileptic"]):
                return self._handle_treatment_query(query, context)

            # EEG
            elif any(term in query_lower for term in ["eeg", "electroencephalogram"]):
                return self._handle_eeg_query(query, context)

            # First aid
            elif any(term in query_lower for term in ["first aid", "what to do", "during seizure", "help"]):
                return self._handle_first_aid_query(query, context)

            # Diagnosis
            elif any(term in query_lower for term in ["diagnosis", "diagnose", "test", "workup"]):
                return self._handle_diagnosis_query(query, context)

            # General epilepsy
            else:
                return self._handle_general_epilepsy_query(query, context)

        except Exception as e:
            return DomainQueryResult(
                domain_name="epilepsy",
                answer=f"I encountered an error processing your epilepsy query: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e), "domain": "epilepsy"}
            )

    def _handle_classification_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle seizure classification queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**Seizure Classification - Second Opinion Consultation**\n\n"
                "**ILAE 2017 Classification**:\n\n"
                "**Focal Onset Seizures**:\n"
                "- **Aware**: Patient conscious during seizure (simple focal)\n"
                "- **Impaired Awareness**: Altered consciousness (complex focal)\n"
                "- Can evolve to bilateral tonic-clonic seizure\n"
                "- Typical auras: rising epigastric sensation, déjà vu, fear\n"
                "- Examples: Temporal lobe, frontal lobe seizures\n\n"
                "**Generalized Onset Seizures**:\n"
                "- **Tonic-Clonic**: Convulsive, loss of consciousness (formerly grand mal)\n"
                "- **Absence**: Brief staring, unresponsive (formerly petit mal)\n"
                "- **Myoclonic**: Brief jerks, often morning\n"
                "- **Atonic**: Sudden loss of tone (drop attacks)\n"
                "- **Tonic**: Stiffening\n"
                "- **Clonic**: Rhythmic jerking without tonic phase\n\n"
                "**Unknown Onset**: Insufficient information\n\n"
                "**Epilepsy Syndromes**:\n"
                "- **Juvenile Myoclonic Epilepsy**: Myoclonus + generalized tonic-clonic, awakening seizures\n"
                "- **Temporal Lobe Epilepsy**: Most common focal epilepsy, mesial temporal sclerosis\n"
                "- **Childhood Absence Epilepsy**: Typical absence seizures 3-11 years\n"
                "- **Lennox-Gastaut**: Multiple seizure types, intellectual disability, treatment-resistant\n"
                "- **Dravet Syndrome**: SCN1A mutation, fever-sensitive seizures, refractory\n\n"
                "**Key Question**: Does the seizure start focally or generalize from onset?\n\n"
                "**Sources**: ILAE Classification Commission, NICE CG137 Epilepsies."
            ),
            confidence=0.90,
            metadata={
                "specialty": "epilepsy",
                "subspecialty": "seizure_classification",
                "sources": ["ILAE 2017 Classification", "NICE Guidelines"]
            }
        )

    def _handle_treatment_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle treatment/medication queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**Epilepsy Treatment - Second Opinion Consultation**\n\n"
                "**First-Line AEDs by Seizure Type**:\n\n"
                "**Focal Seizures**:\n"
                "- **Carbamazepine**: First-line, hepatic enzyme inducer\n"
                "- **Lamotrigine**: First-line, mood stabilizing, slow titration (rash risk)\n"
                "- **Levetiracetam**: First-line, minimal interactions, behavioral SEs\n"
                "- **Sodium Valproate**: Alternative, teratogenic, broad spectrum\n\n"
                "**Generalized Seizures**:\n"
                "- **Sodium Valproate**: First-line for most generalized types\n"
                "- **Lamotrigine**: Alternative, good for absence, myoclonic\n"
                "- **Levetiracetam**: Alternative\n"
                "- **Ethosuximide**: For absence seizures only\n\n"
                "**Important Considerations**:\n\n"
                "**Women of Childbearing Age**:\n"
                "- Sodium valproate contraindicated (teratogenic: neural tube defects)\n"
                "- Lamotrigine preferred\n"
                "- Levetiracetam safe\n"
                "- Discuss pregnancy planning\n\n"
                "**Elderly**:\n"
                "- Levetiracetam preferred (no interactions)\n"
                "- Lamotrigine alternative\n"
                "- Avoid enzyme inducers (interactions)\n\n"
                "**Treatment-Resistant Epilepsy**:\n"
                "- Defined: Failure of 2 appropriate, tolerated AEDs\n"
                "- Consider: combination therapy, epilepsy surgery evaluation, VNS, ketogenic diet\n\n"
                "**AED Side Effects**:\n"
                "- Carbamazepine: Rash, SIADH, leukopenia\n"
                "- Lamotrigine: Stevens-Johnson (slow titration prevents), dizziness\n"
                "- Levetiracetam: Irritability, depression, behavioral changes\n"
                "- Sodium valproate: Weight gain, tremor, hair loss, hepatotoxicity\n"
                "- Phenytoin: Gum hypertrophy, ataxia, osteomalacia\n\n"
                "**Monitoring**:\n"
                "- Baseline: LFTs, FBC, U&Es\n"
                "- Therapeutic drug monitoring: Phenytoin, valproate (others: clinical response)\n\n"
                "**Disclaimer**: Individualized treatment essential. Consult neurologist/epileptologist."
            ),
            confidence=0.88,
            metadata={
                "specialty": "epilepsy",
                "subspecialty": "treatment",
                "sources": ["NICE CG137", "Scottish SIGN 70", "ILAE Guidelines"]
            }
        )

    def _handle_eeg_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle EEG queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**EEG Interpretation - Second Opinion Consultation**\n\n"
                "**EEG Utility**:\n"
                "- Support diagnosis of epilepsy (not definitive alone)\n"
                "- Classify seizure type\n"
                "- Identify epileptiform activity (spikes, sharp waves)\n"
                "**Note**: Normal EEG does NOT exclude epilepsy (sensitivity ~50%)\n\n"
                "**Epileptiform Abnormalities**:\n"
                "- **Spike**: Duration <70ms, predominantly negative field\n"
                "- **Sharp Wave**: Duration 70-200ms\n"
                "- **Spike-and-Slow Wave**: Spike followed by slow wave\n"
                "- **Periodic Lateralized Epileptiform Discharges (PLEDs)**: Acute injury\n\n"
                "**Localization Patterns**:\n"
                "- **Temporal**: Temporal spikes/sharp waves (mesial temporal sclerosis)\n"
                "- **Frontal**: Frontal spikes, often brief, stereotyped\n"
                "- **Generalized**: Bilateral synchronous spike-wave (3 Hz in absence)\n\n"
                "**Common EEG Patterns**:\n\n"
                "1. **Generalized Spike-Wave (3 Hz)**:\n"
                "   - Childhood absence epilepsy\n"
                "   - Typical absence seizures activated by hyperventilation\n\n"
                "2. **Hypsarrhythmia**:\n"
                "   - Infantile spasms\n"
                "   - High-amplitude, disorganized background\n\n"
                "3. **Photoconvulsive Response**:\n"
                "   - Occipital spikes triggered by photic stimulation\n"
                "   - Risk of photosensitive epilepsy\n\n"
                "4. **Focal Temporal Spike**:\n"
                "   - Temporal lobe epilepsy\n"
                "   - Mesial temporal sclerosis\n\n"
                "**Background Rhythm**:\n"
                "- Normal: Posterior dominant rhythm 8-13 Hz (alpha)\n"
                "- Slowing: Encephalopathy, postictal, focal dysfunction\n\n"
                "**Activation Procedures**:\n"
                "- Hyperventilation: Absence seizures\n"
                "- Photic stimulation: Photosensitive epilepsy\n"
                "- Sleep: Increases epileptiform yield\n\n"
                "**Limitations**:\n"
                "- Routine EEG (20-30 min): ~50% sensitivity in epilepsy\n"
                "- Ambulatory EEG (24-72 hr): Higher yield\n"
                "- Video-EEG telemetry: Capture events for characterization\n\n"
                "**Recommendation**: If clinical suspicion high despite normal EEG, consider sleep-deprived or ambulatory EEG.\n\n"
                "**Disclaimer**: EEG must be interpreted in clinical context. Consult neurologist."
            ),
            confidence=0.87,
            metadata={
                "specialty": "epilepsy",
                "subspecialty": "eeg_interpretation",
                "sources": ["NICE Guidelines", "ACNS Standardized Terminology"]
            }
        )

    def _handle_first_aid_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle seizure first aid queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**Seizure First Aid - Immediate Action**\n\n"
                "**DURING A SEIZURE**:\n\n"
                "**✓ DO**:\n"
                "- Protect from injury (cushion head, remove hazards)\n"
                "- Note time: Seizure >5 min = status epilepticus (call 999/911)\n"
                "- Place in recovery position after seizure ends\n"
                "- Stay with person until fully recovered\n"
                "- Reassure when conscious\n\n"
                "**✗ DON'T**:\n"
                "- DON'T put anything in mouth (risk of injury, choking)\n"
                "- DON'T restrain (risk of injury, fracture)\n"
                "- DON't attempt to \"swallow tongue\" (impossible)\n\n"
                "**RECOGNIZING EMERGENCIES**:\n\n"
                "**Call 999/911 if**:\n"
                "- Seizure lasts >5 minutes (or >3 min if known to have seizures)\n"
                "- Another seizure starts immediately (status epilepticus)\n"
                "- Injury occurred during seizure\n"
                "- Difficulty breathing after seizure\n"
                "- Seizure in water (near-drowning risk)\n"
                "- First seizure ever\n"
                "- Pregnant, diabetes, or other medical concerns\n\n"
                "**RECOVERY (Postictal) Phase**:\n"
                "- Confusion, drowsiness normal (may last minutes to hours)\n"
                "- Do not give food/drink until fully alert\n"
                "- Document: duration, type, triggers, aura, postictal symptoms\n\n"
                "**STATUS EPILEPTICUS**:\n"
                "- Medical emergency: Continuous seizure >5 min OR 3+ seizures without full recovery\n"
                "- Treatment: Benzodiazepines (lorazepam IV, buccal midazolam)\n"
                "- Hospital admission required\n\n"
                "**Seizure Safety Precautions**:\n"
                "- Avoid swimming alone, heights, unprotected heavy machinery\n"
                "- Shower instead of bath\n"
                "- Wear medical alert bracelet\n"
                "- Inform driving authority (regulations vary)\n\n"
                "**Disclaimer**: This is general first aid guidance. For individual emergencies, call emergency services."
            ),
            confidence=0.92,
            metadata={
                "specialty": "epilepsy",
                "subspecialty": "first_aid",
                "sources": ["Epilepsy Society", "NICE Guidelines", "ILAE"]
            }
        )

    def _handle_diagnosis_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle epilepsy diagnosis queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**Epilepsy Diagnosis - Second Opinion Consultation**\n\n"
                "**ILAE 2014 Definition**:\n"
                "At least **two unprovoked seizures** occurring >24 hours apart\n"
                "OR **one unprovoked seizure** with probability of further seizures >60%\n\n"
                "**Diagnostic Workup**:\n\n"
                "**1. Clinical History** (CRITICAL):\n"
                "- Detailed description of event (eyewitness account invaluable)\n"
                "- Aura (preceding symptoms)\n"
                "- Seizure semiology (motor, automatisms, awareness)\n"
                "- Postictal symptoms\n"
                "- Triggers (sleep deprivation, alcohol, flickering lights, stress)\n"
                "- Family history, birth history, developmental history\n\n"
                "**2. EEG**:\n"
                "- Routine EEG: First-line\n"
                "- Sleep-deprived EEG: If normal routine EEG\n"
                "- Ambulatory EEG: If events frequent\n"
                "- Video-EEG telemetry: If diagnostic uncertainty\n\n"
                "**3. Neuroimaging**:\n"
                "- **MRI brain** (epilepsy protocol) indicated:\n"
                "  - Focal seizures\n"
                "  - Abnormal neurological exam\n"
                "  - History suggesting structural lesion\n\n"
                "**Differential Diagnosis** (Conditions mimicking seizures):\n\n"
                "1. **Syncope** (fainting):\n"
                "   - Prodrome (lightheadedness, vision graying)\n"
                "   - Brief (<1 min), rapid recovery\n"
                "   - No postictal confusion\n\n"
                "2. **Psychogenic Non-Epileptic Seizures (PNES)**:\n"
                "   - Often longer duration (>2 min)\n"
                "   - Variable semiology, asynchronous movements\n"
                "   - No postictal phase, rapid return to baseline\n"
                "   - Diagnosis by video-EEG telemetry\n\n"
                "3. **Migraine**:\n"
                "   - Headache, visual aura, longer duration\n\n"
                "4. **Sleep Disorders**:\n"
                "   - Narcolepsy, sleep paralysis\n\n"
                "5. **Movement Disorders**:\n"
                "   - Tics, myoclonus, dystonia\n\n"
                "**Red Flags**:\n"
                "- Sudden onset, headache at onset (consider bleed, tumor)\n"
                "- Fever, meningism (consider meningitis, encephalitis)\n"
                "- Focal deficit (consider stroke, mass lesion)\n\n"
                "**Disclaimer**: Diagnosis requires comprehensive evaluation by neurologist/epileptologist."
            ),
            confidence=0.89,
            metadata={
                "specialty": "epilepsy",
                "subspecialty": "diagnosis",
                "sources": ["ILAE 2014 Definition", "NICE CG137"]
            }
        )

    def _handle_general_epilepsy_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general epilepsy queries."""
        return DomainQueryResult(
            domain_name="epilepsy",
            answer=(
                "**Epilepsy Consultation - Second Opinion**\n\n"
                "I specialize in seizure disorders and can provide consultation on:\n\n"
                "**Seizure Types**:\n"
                "- Focal (aware, impaired awareness)\n"
                "- Generalized (tonic-clonic, absence, myoclonic, atonic)\n"
                "- Unknown onset\n\n"
                "**Epilepsy Syndromes**:\n"
                "- Juvenile myoclonic epilepsy\n"
                "- Temporal lobe epilepsy\n"
                "- Childhood absence epilepsy\n"
                "- Lennox-Gastaut, Dravet syndrome\n\n"
                "**Diagnostic Evaluation**:\n"
                "- EEG interpretation\n"
                "- MRI epilepsy protocol\n"
                "- Differential diagnosis (syncope, PNES, migraine)\n\n"
                "**Treatment Options**:\n"
                "- Antiepileptic medications (first-line, combination therapy)\n"
                "- Medication side effects and interactions\n"
                "- Treatment-resistant epilepsy options\n"
                "- Epilepsy surgery evaluation\n"
                "- Vagus nerve stimulation (VNS)\n"
                "- Ketogenic diet\n\n"
                "**Living with Epilepsy**:\n"
                "- Seizure first aid\n"
                "- Safety precautions\n"
                "- Driving regulations\n"
                "- Pregnancy planning\n"
                "- Employment considerations\n\n"
                "**Please provide**: Event description, EEG/MRI results, current medications, "
                "specific questions for second opinion.\n\n"
                "**Privacy Note**: All information stored locally, not transmitted.\n"
                "**Medical Disclaimer**: This is second opinion, not replacement for in-person neurological care. "
                "For emergencies, seek immediate care."
            ),
            confidence=0.85,
            metadata={
                "specialty": "epilepsy",
                "sources": ["NICE Guidelines", "ILAE Guidelines", "Epilepsy Society"]
            }
        )


def create_epilepsy_domain():
    """Factory function for creating epilepsy domain instances."""
    return EpilepsyDomain()
