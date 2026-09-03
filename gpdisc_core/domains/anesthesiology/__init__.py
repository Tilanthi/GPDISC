"""
Anesthesiology Domain for GPDISC

Comprehensive anesthesiology consultation covering:
- Preoperative assessment and optimisation
- Anaesthesia techniques (general, regional, local)
- Airway management
- Intraoperative monitoring
- Postoperative care and analgesia
- Critical care medicine
- Pain management

Evidence-based guidelines:
- NICE NGxx guidelines
- Association of Anaesthetists of Great Britain & Ireland (AAGBI)
- Royal College of Anaesthetists
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class AnesthesiologyDomain(BaseDomainModule):
    """
    Anesthesiology domain for comprehensive anaesthetic and critical care consultation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="anesthesiology",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive anesthesiology: preoperative assessment, anaesthesia techniques, airway management, postoperative care, critical care, pain management",
            keywords=[
                "anaesthesia", "anesthesiology", "anesthesiologist", "anaesthetist",
                "preoperative", "preop", "pre-assessment", "surgical clearance",
                "general anaesthetic", "ga", "general anesthesia", "going to sleep",
                "regional anaesthesia", "epidural", "spinal", "nerve block", "plexus block",
                "local anaesthetic", "lidocaine", "bupivacaine", "ropivacaine", "levobupivacaine",
                "airway", "intubation", "laryngoscopy", "lma", "supraglottic airway",
                "difficult airway", "cricothyroidotomy", "surgical airway",
                "monitoring", "ecg", "bp", "pulse oximetry", "capnography", "bis",
                "iv", "intravenous cannula", "cannulation", "central line", "cvc",
                "arterial line", "art line", "invasive monitoring",
                "postoperative", "postop", "recovery", "pacu",
                "pain management", "analgesia", "opioid", " pca", "patient controlled analgesia",
                "epidural analgesia", "nerve block", "multimodal analgesia",
                "critical care", "itu", "icu", "ventilation", "mechanical ventilation",
                "sedation", "conscious sedation", "procedural sedation",
                "complications", "malignant hyperthermia", "anaphylaxis", "awareness"
            ],
            capabilities=[
                "preoperative_assessment",
                "anaesthesia_techniques",
                "airway_management",
                "perioperative_monitoring",
                "postoperative_care",
                "pain_management",
                "critical_care_medicine",
                "sedation",
                "complication_management"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process anesthesiology query with emergency detection
        """
        query_lower = query.lower()

        # ANAESTHESIOLOGY EMERGENCIES - HIGHEST PRIORITY

        # Malignant hyperthermia
        if any(term in query_lower for term in ["malignant hyperthermia", "mh", "dantrolene",
                                                   "rigidity", "hyperthermia", "hypercapnia"]):
            return self._handle_malignant_hyperthermia(query, context)

        # Anaphylaxis (perioperative)
        if any(term in query_lower for term in ["anaphylaxis", "anaphylactic shock", "severe allergic reaction",
                                                   "airway swelling", "throat closing"]):
            return self._handle_anaphylaxis(query, context)

        # Failed airway / cannot intubate
        if any(term in query_lower for term in ["cannot intubate", "cannot ventilate", "failed airway",
                                                   "difficult airway", "cricothyroidotomy"]):
            return self._handle_failed_airway(query, context)

        # Cardiac arrest (perioperative)
        if any(term in query_lower for term in ["cardiac arrest", "cpr", "perioperative arrest",
                                                   "intraoperative arrest"]):
            return self._handle_cardiac_arrest(query, context)

        # PREOPERATIVE ASSESSMENT

        if any(term in query_lower for term in ["preoperative", "preop", "pre-assessment", "surgical clearance",
                                                   "fitness for surgery", "anaesthetic assessment"]):
            return self._handle_preoperative_assessment(query, context)

        # ANAESTHESIA TECHNIQUES

        if any(term in query_lower for term in ["general anaesthetic", "ga", "general anesthesia",
                                                   "going to sleep", "induction"]):
            return self._handle_general_anaesthesia(query, context)

        if any(term in query_lower for term in ["regional anaesthesia", "epidural", "spinal", "nerve block",
                                                   "plexus block", "caudal"]):
            return self._handle_regional_anaesthesia(query, context)

        # AIRWAY MANAGEMENT

        if any(term in query_lower for term in ["airway", "intubation", "laryngoscopy", "lma",
                                                   "supraglottic airway", "difficult airway"]):
            return self._handle_airway_management(query, context)

        # POSTOPERATIVE CARE

        if any(term in query_lower for term in ["postoperative", "postop", "recovery", "pacu",
                                                   "postoperative care", "recovery room"]):
            return self._handle_postoperative_care(query, context)

        # PAIN MANAGEMENT

        if any(term in query_lower for term in ["pain management", "analgesia", "opioid", "pca",
                                                   "patient controlled analgesia", "epidural analgesia"]):
            return self._handle_pain_management(query, context)

        # CRITICAL CARE

        if any(term in query_lower for term in ["critical care", "itu", "icu", "ventilation",
                                                   "mechanical ventilation", "respiratory support"]):
            return self._handle_critical_care(query, context)

        # GENERAL ANAESTHESIOLOGY
        return self._handle_general_anesthesiology(query, context)

    def _handle_malignant_hyperthermia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle malignant hyperthermia"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**MALIGNANT HYPERTHERMIA - ANAESTHESIOLOGY EMERGENCY**

**DEFINITION:**
- **Life-threatening pharmacogenetic disorder** of skeletal muscle
- **Triggered** by volatile anaesthetics (halothane, sevoflurane, desflurane) and succinylcholine (SCh)
- **Incidence:** 1:10,000-1:50,000 anaesthetics
- **Mortality:** <5% (with early recognition and treatment)

**PATHOPHYSIOLOGY:**
- **RYR1 gene mutation** (ryanodine receptor) → uncontrolled calcium release from sarcoplasmic reticulum
- **Sustained muscle contraction** → ↑metabolism, heat production, CO₂ production, rigidity
- **Hypermetabolism** → hypercapnia, hyperthermia, metabolic acidosis, rhabdomyolysis, hyperkalaemia

**EARLY SIGNS:**
- **Unexplained hypercapnia** (rising ETCO₂)
- **Tachycardia** (often first sign)
- **Muscle rigidity** (especially masseter spasm, trismus)
- **Rising temperature** (late sign - may be rapid)
- **Tachypnoea** (despite adequate ventilation)
- **Skin flushing** (mottled, cyanotic later)
- **Sweating**

**LATE SIGNS:**
- **Temperature >38°C** (may exceed 40°C)
- **Mixed respiratory and metabolic acidosis**
- **Hyperkalaemia** (arrhythmias)
- **Rhabdomyolysis** (CK >10,000 IU/L, myoglobinuria)
- **Coagulopathy** (DIC)
- **Cardiac arrest** (VF/VT secondary to hyperkalaemia)

**IMMEDIATE MANAGEMENT:**

**1. CALL FOR HELP:**
- **Inform surgeon** (stop surgery ASAP)
- **Call senior anaesthetist**
- **Call for MH treatment drugs** (Dantrolene)

**2. STOP TRIGGERS:**
- **Discontinue volatile anaesthetic** (switch to total IV anaesthesia - TIVA)
- **Stop succinylcholine** (if being used)

**3. HYPERVENTILATE WITH 100% OXYGEN:**
- **High fresh gas flow** (10 L/min) to eliminate volatile anaesthetic
- **Hyperventilate** (to reduce PaCO₂)

**4. DANTROLENE (SPECIFIC ANTIDOTE):**
- **2.5 mg/kg IV** (rapid bolus)
- **Repeat:** 2.5 mg/kg IV every 5 minutes (until signs subside)
- **Total dose:** up to 10-20 mg/kg (rarely needed)
- **Reconstitute:** 20 mg dantrolene = 3 g sterile water (shake vigorously)
- **Administer:** rapid IV push (over 1-2 minutes)
- **Repeat** until:
   - **ETCO₂ normalises** (<6 kPa)
   - **Heart rate normalises**
   - **Temperature decreasing**
   - **Muscle rigidity resolves**

**5. ACTIVE COOLING:**
- **Surface cooling:** cold packs, ice packs to groin, axillae, neck
- **Cold IV fluids**
- **Lavage:** gastric, peritoneal, bladder (with cold saline)
- **Cooling blanket**
- **Target temperature:** <38°C

**6. CORRECT METABOLIC ACIDOSIS:**
- **Sodium bicarbonate** (if pH <7.2, or severe acidosis)
- **Hyperventilate** (to reduce PaCO₂)

**7. TREAT HYPERKALAEMIA:**
- **Calcium chloride 10 mL 10%** IV (cardiac membrane stabilisation)
- **Insulin 10 units + 50 mL 50% dextrose** IV (shifts K⁺ into cells)
- **Salbutamol 5 mg nebulised** (shifts K⁺ into cells)
- **Consider dialysis** (if severe, refractory hyperkalaemia, anuric renal failure)

**8. CARDIAC ARREST:**
- **Standard ALS** (if cardiac arrest occurs)
- **Treat arrhythmias:** hyperkalaemia-responsive (avoid calcium channel blockers, beta-blockers)

**9. ARRANGE ICU ADMISSION:**
- **All MH patients** require ICU admission (minimum 24-48 hours)
- **Monitoring:** ECG, SpO₂, ETCO₂, core temperature, ABG, CK, electrolytes, coagulation
- **Support:** mechanical ventilation, haemodynamic support, renal replacement therapy (if needed)

**10. DOCUMENT AND REPORT:**
- **Document:** time of onset, signs, treatment, response
- **Report:** to MH Investigational Group (Malignant Hyperthermia Investigation Unit)
- **Test:** patient for RYR1 mutation (genetic testing)
- **Inform:** patient and family (autosomal dominant inheritance)

**DANTROLENE SIDE EFFECTS:**
- **Muscle weakness** (prolonged ventilation)
- **Phlebitis** (venous irritation)
- **Respiratory depression** (weakness of respiratory muscles)

**POST-MH MANAGEMENT:**

**Monitoring (ICU):**
- **ECG** (arrhythmias)
- **Core temperature** (may rebound)
- **ETCO₂** (recurrence)
- **ABG** (acid-base status)
- **CK** (rhabdomyolysis - may peak at 12-24 hours)
- **Urine output** (myoglobinuria - renal failure)
- **Coagulation profile** (DIC)

**Complications:**
- **Renal failure** (rhabdomyolysis, myoglobinuria)
- **DIC** (disseminated intravascular coagulation)
- **Compartment syndrome** (muscle swelling → fasciotomy may be needed)
- **Recurrence** (up to 25% within 24-48 hours - continue dantrolene 1 mg/kg IV 4-hourly for 24-48 hours)

**PROPHYLAXIS (for future surgery):**
- **Avoid:** volatile anaesthetics, succinylcholine
- **Safe agents:** propofol, benzodiazepines, opioids, nitrous oxide, non-depolarising muscle relaxants
- **Pre-treatment:** Dantrolene 2.5 mg/kg IV before induction (controversial)
- **MH-safe anaesthetic machine:** flush with 10 L/min O₂ for ≥20 minutes (to eliminate volatile agents)
- **New breathing circuit**, new CO₂ absorber

**SCREENING:**
- **Family history:** (unexplained anaesthetic death, MH)
- **Personal history:** (unexplained fever, muscle rigidity after anaesthesia)
- **Investigations:** CK (resting), in vitro contracture test (IVCT - gold standard), genetic testing (RYR1 mutation)

**Sources:** AAGBI Guidelines 2021, MHAUS (Malignant Hyperthermia Association of the United States)"""
        )

    def _handle_anaphylaxis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle perioperative anaphylaxis"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**PERIOPERATIVE ANAPHYLAXIS - ANAESTHESIOLOGY EMERGENCY**

**DEFINITION:**
- **Severe, life-threatening allergic reaction** occurring during anaesthesia
- **Incidence:** 1:10,000-1:20,000 anaesthetics
- **Mortality:** 3-6% (despite appropriate treatment)

**COMMON TRIGGERS:**
- **Neuromuscular blocking agents (NMBAs):** 50-60% (Suxamethonium, Rocuronium most common)
- **Antibiotics:** 15% (Penicillins, Cephalosporins, Teicoplanin, Vancomycin)
- **Latex:** 5-10% (gloves, catheters, equipment)
- **Chlorhexidine:** 5% (skin prep)
- **IV colloid:** (Gelofusine, Haemaccel)
- **Dyes:** (methylene blue, indocyanine green)
- **Others:** Opioids, NSAIDs, Protamine, Aprotinin

**IMMEDIATE RECOGNITION:**

**Cardiovascular:**
- **Hypotension** (often severe, refractory)
- **Tachycardia** (initially), then bradycardia (shock)
- **Cardiac arrest** (in severe cases)

**Respiratory:**
- **Bronchospasm** (wheeze, increased airway pressures)
- **Hypoxia** (desaturation)
- **Airway oedema** (difficulty ventilating)

**Cutaneous:**
- **Flushing,** erythema, urticaria (hives)
- **Angioedema** (facial, laryngeal)

**Other:**
- **Abdominal cramping, diarrhoea**

**IMMEDIATE MANAGEMENT:**

**1. CALL FOR HELP:**
- **Inform surgeon** (stop surgery ASAP)
- **Call senior anaesthetist**
- **Call crash team** (if cardiac arrest)

**2. STOP ALL ANAESTHETIC AGENTS:**
- **Stop volatile anaesthetic, IV infusions**
- **Stop NMBA, antibiotics** (if possible)

**3. GIVE ADRENALINE (EPINEPHRINE) - FIRST LINE:**
- **10-100 mcg IV** (10-100 mcg = 0.1-1 mL of 1:10,000)
- **Start:** 10 mcg IV (small dose) - titrate to effect
- **Repeat:** every 1-2 minutes (as needed)
- **Intramuscular:** (if IV access not available) 0.5 mg IM (0.5 mL of 1:1000) into anterolateral thigh

**4. FLUID RESUSCITATION:**
- **Crystalloid bolus:** 500-1000 mL rapid IV (0.9% NaCl or Hartmann's)
- **Repeat:** as needed (shock may require large volumes)

**5. DISCONTINUE TRIGGER:**
- **Remove latex** (gloves, equipment)
- **Stop antibiotic infusion** (if suspected)
- **Stop NMBA** (if possible)

**6. AIRWAY AND BREATHING:**
- **100% oxygen** (high flow)
- **Bronchodilators:** Salbutamol 5 mg nebulised (if bronchospasm)
- **Consider:** early intubation (if airway oedema, respiratory failure)
- **Consider:** cricothyroidotomy (if cannot intubate, airway obstruction)

**7. ANTIHISTAMINES AND CORTICOSTEROIDS:**
- **Chlorpheniramine 10 mg IV** (or Cetirizine 10 mg IV)
- **Hydrocortisone 200 mg IV** (or Methylprednisolone 100-125 mg IV)
- **Note:** second-line treatments (do NOT delay adrenaline)

**8. REFRACTORY SHOCK:**
- **Adrenaline infusion:** start 0.05-0.1 mcg/kg/min, titrate
- **Noradrenaline infusion:** (if persistent hypotension despite adrenaline)
- **Consider:** vasopressin, methylene blue (if refractory)

**CONFIRMATION TESTING:**

**Mast cell tryptase:**
- **Sample 1:** as soon as possible after reaction (within 1-2 hours)
- **Sample 2:** 24-48 hours later (baseline)
- **Sample 3:** if recurrent reaction (another sample at 24-48 hours)
- **Elevated:** >1.2 × baseline + 2 ng/mL (consistent with anaphylaxis)

**Other tests:**
- **Specific IgE (RAST):** (for suspected allergen)
- **Skin prick testing:** (after recovery, usually 6 weeks later)
- **Basophil activation test:** (if skin testing unavailable)

**POST-ANAPHYLAXIS MANAGEMENT:**

**ICU admission:**
- **All patients** (for monitoring, treatment)
- **Monitoring:** ECG, SpO₂, invasive BP, urine output
- **Duration:** minimum 12-24 hours (may be biphasic - recurs within 8-12 hours)

**Observations:**
- **Cardiovascular:** BP, HR, ECG (arrhythmias, ischaemia)
- **Respiratory:** SpO₂, respiratory rate, auscultation (bronchospasm)
- **Cutaneous:** urticaria, angioedema
- **Neurological:** GCS, focal signs (ischaemic stroke)

**Documentation:**
- **Record:** time, signs, treatment, response
- **Inform:** patient, GP, anaesthetist (for future surgeries)

**PREVENTION (FUTURE SURGERY):**

**Identify trigger:**
- **From history:** previous allergy, atopy, latex allergy
- **From testing:** mast cell tryptase, specific IgE, skin prick testing
- **Unknown trigger:** (assume all possible triggers, avoid)

**Safe anaesthetic:**
- **Avoid:** identified trigger
- **Alternatives:**
   - **If NMBA allergy:** use total IV anaesthesia (TIVA) without NMBA (or use different NMBA if safe on skin testing)
   - **If latex allergy:** use latex-free equipment, latex-free environment
   - **If antibiotic allergy:** use different antibiotic class (based on allergy testing)
   - **If chlorhexidine allergy:** use alternative skin prep (povidone-iodine)

**Preparation:**
- **MH-safe machine:** (if NMBA allergy - flush with 10 L/min O₂ for ≥20 minutes)
- **Latex-free environment:** (if latex allergy)
- **Premedication:** (antihistamine, corticosteroid - controversial)
- **Communication:** (inform entire theatre team)

**PATIENT INFORMATION:**
- **Provide:** allergy bracelet/medic alert
- **Explain:** trigger, symptoms, management
- **Letter:** for future hospital admissions (detailing allergy, safe alternatives)
- **Report:** to local anaesthetic allergy service (for investigation, documentation)

**Sources:** AAGBI Guidelines 2020, NICE CG134, British Society for Allergy and Clinical Immunology (BSACI)"""
        )

    def _handle_failed_airway(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle failed airway / cannot intubate/cannot ventilate"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**FAILED AIRWAY / CANNOT INTUBATE, CANNOT VENTILATE - ANAESTHESIOLOGY EMERGENCY**

**DEFINITION:**
- **"Cannot Intubate, Cannot Ventilate" (CICV):** failed airway, life-threatening emergency
- **Failed airway:** 3 attempts at intubation by experienced anaesthetist, OR >10 minutes elapsed
- **Cannot ventilate:** unable to maintain SpO₂ >90% with bag-mask ventilation

**IMMEDIATE MANAGEMENT:**

**1. CALL FOR HELP:**
- **Senior anaesthetist**
- **Surgeon** (for surgical airway)
- **ENT surgeon** (if available)

**2. ASSESS VENTILATION:**
- **Can you ventilate with bag-mask?**
   - **YES:** maintain oxygenation, proceed to Plan B
   - **NO:** CICV → proceed to emergency surgical airway (Plan D)

**3. MAINTAIN OXYGENATION:**
- **Bag-mask ventilation** (2-person technique, oral airway, optimal head position)
- **Oral airway** (Guedel) or **Nasopharyngeal airway** (if bag-mask difficult)
- **100% oxygen**
- **Consider:** LMA (Supraglottic Airway Device) - may improve ventilation

**DIFFICULT AIRWAY ALGORITHM (DAS 2015):**

**Plan A: Initial Intubation Attempts:**
- **Optimise:** position (ramped, sniffing), optimal laryngoscopy (external laryngeal manipulation)
- **3 attempts** by experienced anaesthetist
- **Equipment:** Macintosh blade, gum elastic bougie, stylet
- **If fails:** proceed to Plan B

**Plan B: Supraglottic Airway Device (SAD):**
- **Insert:** LMA (Classic, ProSeal, i-gel)
- **Assess:** ventilation (chest rise, ETCO₂, SpO₂, airway pressures)
- **If ventilation successful:** proceed to Plan C
- **If fails:** proceed to Plan D (CICV)

**Plan C: Rescue Techniques (if SAD ventilation successful):**
- **Options:**
   - **Blind intubation through SAD** (using ILMA, Fastrach, LMA Fastrach)
   - **Fibreoptic intubation through SAD**
   - **Video laryngoscopy** (if not already attempted)
   - **Blind bougie-guided intubation** (if feasible)
- **Goal:** secure definitive airway (endotracheal tube)
- **If fails:** maintain SAD ventilation, wake patient (if possible)

**Plan D: Emergency Surgical Airway (CICV):**
- **Indicated:** cannot intubate AND cannot ventilate (CICV)
- **Procedure:** **Surgical Cricothyroidotomy** (not needle cricothyroidotomy - too small)
- **Technique:**
   1. **Identify:** cricothyroid membrane (palpate between thyroid and cricoid cartilages)
   2. **Stabilise:** thyroid cartilage with non-dominant hand
   3. **Incise:** vertical incision through skin, horizontal incision through cricothyroid membrane
   4. **Dilate:** use Trousseau dilator or scalpel handle to open hole
   5. **Insert:** bougie, then size 6.0 cuffed tube (or small tracheostomy tube 4.0-6.0)
   6. **Inflate:** cuff
   7. **Confirm:** ETCO₂, chest rise, breath sounds
- **Alternative:** **Percutaneous Seldinger cricothyroidotomy** (if kit available, trained)
- **Complications:** bleeding, laryngeal injury, failed placement, posterior tracheal wall injury

**POST-PROCEDURE:**
- **Secure:** airway (tie tube, secure position)
- **Confirm:** ETCO₂, chest rise, breath sounds, chest X-ray
- **Maintain:** anaesthesia (reduce volatile agent, consider TIVA)
- **Monitor:** SpO₂, ETCO₂, airway pressures

**EXTUBATION:**
- **Consider:** leaving surgical airway in place (if difficult airway anticipated post-op)
- **Deferring:** extubation until fully awake, reversed NMBA, spontaneous ventilation
- **Plan:** for extubation over airway exchange catheter (if difficult airway likely to recur)
- **Have:** difficult airway cart immediately available

**POST-OPERATIVE:**
- **Inform:** patient (and document) of difficult airway
- **Document:** in anaesthetic record, patient notes
- **Referral:** to difficult airway clinic (for further investigation, planning)
- **Alert:** for future surgeries (patient has difficult airway)

**DIFFICULT AIRWAY PREDICTION:**

**History:**
- **Previous difficult airway:** (patient or family history)
- **Airway trauma:** (previous surgery, radiation)
- **Symptoms:** (stridor, dysphagia, sleep apnoea)

**Examination:**
- **Mouth opening:** (inter-incisor distance <3 cm = difficult)
- **Mallampati score:** (3 or 4 = difficult)
- **Thyromental distance:** (<6.5 cm = difficult)
- **Neck mobility:** (limited extension = difficult)
- **Obesity:** (BMI >35 = difficult)
- **Facial abnormalities:** (micrognathia, retrognathia, macroglossia)

**Investigations:**
- **CXR:** (mandibular abnormalities, soft tissue swelling)
- **CT neck:** (airway dimensions, pathology)
- **Fibreoptic nasendoscopy:** (assess larynx, vocal cords)

**PREPARATION FOR DIFFICULT AIRWAY:**
- **Assess:** preoperative airway examination
- **Plan:** primary technique, backup techniques, surgical airway
- **Equipment:** difficult airway cart immediately available
- **Team:** experienced anaesthetist, surgeon present
- **Communication:** inform patient, surgical team

**Sources:** DAS Guidelines 2015 (Difficult Airway Society), AAGBI Guidelines 2015"""
        )

    def _handle_cardiac_arrest(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle perioperative cardiac arrest"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**PERIOPERATIVE CARDIAC ARREST - ANAESTHESIOLOGY EMERGENCY**

**CAUSES OF PERIOPERATIVE CARDIAC ARREST (4H4T):**

**Hypoxia:**
- **Inadequate oxygenation** (airway obstruction, bronchospasm, pulmonary oedema, PE)

**Hypovolaemia:**
- **Blood loss** (surgical bleeding, coagulopathy)
- **Fluid loss** (dehydration, third spacing)

**Hypo/hyperkalaemia:**
- **Electrolyte abnormalities** (K⁺, Na⁺, Ca²⁺, Mg²⁺)

**Hypothermia:**
- **Accidental hypothermia** (insufficient warming, large surface area exposure)

**Tension pneumothorax:**
- **Iatrogenic** (central line, CVP insertion, positive pressure ventilation)

**Tamponade (cardiac):**
- **Iatrogenic** (central line complications), trauma

**Thrombosis (coronary):**
- **ACS** (myocardial infarction, demand ischaemia)

**Thrombosis (pulmonary):**
- **PE** (deep vein thrombosis, fat embolism, amniotic fluid embolism)

**IMMEDIATE MANAGEMENT:**

**1. CALL FOR HELP:**
- **Crash team** (or cardiac arrest team)
- **Surgeon** (open chest massage if indicated)

**2. START CPR (if cardiac arrest):**
- **Quality CPR:** 100-120 compressions/min, depth 5-6 cm, allow full chest recoil
- **Minimise interruptions:** chest compression fraction >60%
- **Airway:** intubate (if not already), ventilate 10 breaths/min
- **IV access:** secure (if not already)

**3. IDENTIFY RHYTHM:**
- **Shockable (VF/pVT):** defibrillate immediately (150-200 J biphasic)
- **Non-shockable (PEA/Asystole):** CPR, identify and treat reversible causes

**4. DEFIBRILLATION (if shockable rhythm):**
- **Immediate shock** (150-200 J biphasic)
- **Resume CPR** immediately after shock (2 minutes)
- **Adrenaline 1 mg IV** (after 2nd shock, then every 3-5 minutes)
- **Amiodarone 300 mg IV** (after 3rd shock)

**5. OPEN CHEST MASSAGE (if indicated):**
- **Indications:**
   - **Cardiac surgery** (post-sternotomy, post-thoracotomy)
   - **Abdominal aortic surgery**
   - **Penetrating thoracic trauma**
   - **Pregnancy** (after 20 weeks gestation)
   - **Pericardial tamponade** (suspected)
   - **PE** (massive, refractory to standard CPR)
   - **Failed closed chest CPR** (after 10 minutes)

**Technique:**
- **Re-open:** sternotomy or thoracotomy wound
- **Internal cardiac massage:** compress heart directly (60-80 beats/min)
- **Cross-clamp:** aorta (if needed)
- **Defibrillate:** directly paddles on heart (10-20 J)

**6. TREAT REVERSIBLE CAUSES:**

**Hypoxia:**
- **Check:** tube position (confirm with capnography), bilateral breath sounds
- **Treat:** bronchospasm (Salbutamol 5 mg nebulised), pulmonary oedema (diuretics, NIV), pneumothorax (decompress)

**Hypovolaemia:**
- **Fluid resuscitation:** crystalloid or blood (rapid bolus)
- **Blood:** cross-match, transfuse (O negative if urgent)

**Hypo/hyperkalaemia:**
- **K⁺ <2.5 mmol/L:** KCl infusion
- **K⁺ >6.5 mmol/L:** Calcium chloride 10 mL 10% IV, Insulin 10 units + 50 mL 50% dextrose IV, Salbutamol 5 mg nebulised, dialysis (if severe)

**Hypothermia:**
- **Active warming:** forced-air warmer, warm IV fluids

**Tension pneumothorax:**
- **Needle decompression:** 14-16G cannula 2nd intercostal space, midclavicular line
- **Chest drain:** follow with formal chest drain

**Tamponade:**
- **Pericardiocentesis:** 18G cannella subxiphoid, aspirate blood
- **Surgical drainage:** if available (pericardial window)

**Thrombosis (coronary):**
- **ACS:** consider PCI (if available), Thrombolysis (if PCI not available)
- **Demand ischaemia:** optimise haemodynamics (reduce oxygen demand, increase supply)

**Thrombosis (pulmonary):**
- **PE:** consider thrombolysis (if massive PE), surgical embolectomy

**POST-RESUSCITATION CARE:**

**Optimisation:**
- **Airway:** advanced airway, capnography (EtCO₂ 35-40 mmHg)
- **Breathing:** SpO₂ 94-98%, ventilation 6-8 breaths/min
- **Circulation:** MAP >65 mmHg, inotropes/vasopressors if needed
- **Disability:** normoglycaemia (6-10 mmol/L), seizure prophylaxis

**Therapeutic hypothermia:**
- **Consider:** Targeted temperature management (32-36°C) for comatose survivors
- **Duration:** 24 hours

**Identify cause:**
- **12-lead ECG** (ACS, ischaemia)
- **ABG** (hypoxia, hypercapnia, acidosis, electrolytes)
- **CXR** (pneumothorax, pulmonary oedema)
- **Echocardiogram** (tamponade, LV function, wall motion abnormalities)
- **Blood tests:** FBC, U&E, glucose, troponin, lactate

**Sources:** AAGBI Guidelines 2015, Resuscitation Council (UK) ALS Guidelines 2021"""
        )

    def _handle_preoperative_assessment(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle preoperative assessment"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**PREOPERATIVE ASSESSMENT**

**PURPOSE:**
- **Fitness for surgery:** assess risk, optimise medical conditions
- **Anaesthetic planning:** choose appropriate anaesthetic technique
- **Patient information:** explain anaesthesia, address concerns

**ASSESSMENT:**

**History:**
- **Indication for surgery:** (elective, urgent, emergency)
- **Comorbidities:** (cardiac, respiratory, renal, hepatic, endocrine, neurological)
- **Medications:** (regular, OTC, herbal, allergies)
- **Previous anaesthetics:** (problems, difficult airway, PONV, MH)
- **Family history:** (MH, bleeding disorders, sickle cell)
- **Social history:** (smoking, alcohol, drugs, occupation)
- **Functional status:** (exercise tolerance, METs - Metabolic Equivalents)

**Examination:**
- **Airway assessment:** (Mallampati, mouth opening, thyromental distance, neck mobility, obesity)
- **Cardiovascular:** (BP, HR, murmurs, oedema, JVP)
- **Respiratory:** (auscultation, respiratory rate)
- **General:** (BMI, deformities)

**INVESTIGATIONS:**

**ECG:**
- **Indicated:** age >65 years, cardiovascular disease, respiratory disease, diabetes, renal disease, major surgery

**Chest X-ray:**
- **Indicated:** cardiopulmonary disease, recent respiratory infection, major surgery

**Blood tests:**
- **FBC:** (major surgery, cardiovascular disease)
- **U&E:** (renal disease, diuretics, ACEi/ARBs, major surgery)
- **Glucose:** (diabetes, steroids)
- **LFTs:** (liver disease, alcohol abuse, major surgery)
- **Coagulation:** (bleeding disorder, anticoagulation, liver disease)
- **Group and save:** (major surgery, possible blood transfusion)
- **Cross-match:** (major surgery, anticipated blood loss)

**PFTs:**
- **Indicated:** dyspnoea on exertion, chronic lung disease, major surgery (thoracic, upper abdominal)

**Echocardiogram:**
- **Indicated:** symptomatic heart failure, murmur, dyspnoea of unknown cause, major surgery with cardiac disease

**CARDIAC RISK STRATIFICATION:**

**Goldman's Cardiac Risk Index:**
- **Class I:** 0.5-4% mortality (low risk)
- **Class II:** 9% mortality (intermediate risk)
- **Class III:** 22% mortality (high risk)
- **Class IV:** 56% mortality (very high risk)

**Revised Cardiac Risk Index (RCRI):**
- **Points:** (high-risk type of surgery, ischemic heart disease, heart failure, cerebrovascular disease, renal insufficiency, diabetes mellitus)
- **0 points:** 0.4% cardiac complications
- **1 point:** 0.9% cardiac complications
- **2 points:** 6.6% cardiac complications
- **≥3 points:** 11% cardiac complications

**ACC/AHA Guidelines:**
- **Low risk:** (minor surgery, no active cardiac conditions) - no further testing
- **Intermediate risk:** (intermediate surgery, 1-2 clinical risk factors) - consider testing
- **High risk:** (major surgery, ≥3 clinical risk factors, poor functional capacity) - investigate, optimise

**OPTIMISATION:**

**Cardiovascular:**
- **Hypertension:** continue antihypertensives (except ACEi/ARBs - hold day of surgery)
- **Ischaemic heart disease:** optimise medication, consider coronary angiography (if high risk)
- **Heart failure:** optimise medication, consider echocardiography, consider invasive monitoring
- **Arrhythmias:** AF (rate control, anticoagulation), ventricular ectopics (investigate, optimise electrolytes)

**Respiratory:**
- **COPD:** optimise bronchodilators, consider steroids, smoking cessation (≥6-8 weeks pre-op)
- **Asthma:** optimise, review inhalers, consider oral steroids if severe
- **Smoking cessation:** (reduce respiratory complications, wound healing)
- **Chest physiotherapy:** (pre-op teaching, post-op exercises)

**Diabetes:**
- **HbA1c:** (assess glycaemic control)
- **Medication:** (hold metformin day of surgery, continue insulin)
- **Target:** (perioperative glucose 6-10 mmol/L)

**Renal:**
- **AKI/CKD:** optimise hydration, avoid nephrotoxins, monitor renal function
- **Dialysis:** (coordinate with renal team)

**Anaemia:**
- **Iron studies:** (iron deficiency anaemia)
- **Treatment:** iron replacement, erythropoietin (if indicated)
- **Transfusion:** (if severe, symptomatic)

**Anticoagulation:**
- **Warfarin:** stop 5 days pre-op, bridge with LMWH if high risk (AF, mechanical valve, VTE)
- **DOACs:** stop 24-48 hours pre-op (depending on drug, renal function, bleeding risk)
- **LMWH:** stop 12 hours pre-op (therapeutic dose), 24 hours pre-op (high dose)

**MEDICATION MANAGEMENT:**

**Continue:**
- **Cardiovascular:** (beta-blockers, calcium channel blockers, nitrates)
- **Respiratory:** (inhaled bronchodilators, inhaled steroids)
- **Endocrine:** (thyroxine, steroids - give stress dose if long-term)
- **Neurological:** (anti-Parkinson's, anti-epileptics)
- **Psychiatric:** (most antidepressants, antipsychotics)

**Hold:**
- **ACEi/ARBs:** (hold day of surgery - risk of intraoperative hypotension)
- **Diuretics:** (hold morning of surgery)
- **Metformin:** (hold day of surgery - risk of lactic acidosis)
- **DOACs:** (stop 24-48 hours pre-op)
- **Warfarin:** (stop 5 days pre-op)

**RED FLAGS:**
- **Unstable angina:** (admit, investigate, treat - cancel elective surgery)
- **Uncontrolled heart failure:** (optimise, consider inotropes - cancel elective surgery)
- **Severe aortic stenosis:** (high surgical risk - consider valve replacement first)
- **Malignant hypertension:** (treat, optimise - cancel elective surgery)
- **Acute respiratory infection:** (treat, optimise - postpone elective surgery)

**ANAESTHETIC CHOICE:**

**General Anaesthesia:**
- **Indicated:** major surgery, thoracic, upper abdominal, emergency surgery, patient preference
- **Technique:** induction (IV or inhalational), maintenance (volatile or IV), airway (ETT, LMA)
- **Advantages:** secure airway, controlled ventilation, amnesia, immobility
- **Disadvantages:** PONV, haemodynamic instability, MH risk, awareness

**Regional Anaesthesia:**
- **Indicated:** orthopaedic (lower limb), abdominal, thoracic, obstetrics, patient preference
- **Technique:** spinal, epidural, nerve block, plexus block
- **Advantages:** avoid GA, postoperative analgesia, faster recovery, reduced DVT/PE
- **Disadvantages:** technical failure, nerve injury, local anaesthetic toxicity, bilateral block (spinal, epidural)

**MONOBLOCK LOCAL ANAESTHESIA:**
- **Indicated:** minor procedures (skin lumps, biopsies, carpal tunnel)
- **Technique:** local infiltration
- **Advantages:** safe, simple, no fasting
- **Disadvantages:** limited duration, tourniquet pain, toxicity (if high dose)

**SEDATION:**
- **Indicated:** minor procedures, investigations, patient anxiety
- **Technique:** benzodiazepines ± opioids
- **Advantages:** anxiolysis, amnesia, analgesia
- **Disadvantages:** respiratory depression, airway obstruction, delayed recovery

**FASTING GUIDELINES:**
- **Solids:** 6 hours (light meal, 2 hours for clear fluids - some centres)
- **Breast milk:** 4 hours
- **Infant formula:** 6 hours
- **Clear fluids:** 2 hours (water, clear juice, black tea/coffee, carbonated drinks)

**PREMEDICATION:**
- **Anxiolysis:** (temazepam 10-20 mg PO 1 hour pre-op)
- **Analgesia:** (paracetamol 1 g PO PRN, NSAID PRN)
- **Prophylaxis:** (anti-emetic, antibiotic, DVT prophylaxis)

**Sources:** NICE NG45, AAGBI Guidelines 2016, ACC/AHA Guidelines 2014"""
        )

    def _handle_general_anaesthesia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general anaesthesia"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**GENERAL ANAESTHESIA**

**PHASES OF GENERAL ANAESTHESIA:**

**1. PREOXYGENATION (Pre-induction):**
- **100% oxygen** for 3-5 minutes (or 8 vital capacity breaths)
- **Goal:** increase oxygen reserve, prolong safe apnoea time
- **Monitoring:** ECG, SpO₂, NIBP

**2. INDUCTION:**
- **IV induction:** Propofol 1.5-2.5 mg/kg (titrated to effect)
- **Alternative:** Thiopental 3-5 mg/kg (rarely used), Etomidate 0.2-0.3 mg/kg (cardiovascular instability), Ketamine 1-2 mg/kg (asthma, hypovolaemia, shock)
- **Adjuncts:** Fentanyl 1-2 mcg/kg (analgesia, blunts sympathetic response), Midazolam 0.02-0.05 mg/kg (amnesia, anxiolysis)
- **Muscle relaxation:** Rocuronium 0.6 mg/kg (for intubation), Suxamethonium 1-1.5 mg/kg (rapid sequence)

**3. AIRWAY MANAGEMENT:**
- **Bag-mask ventilation** (until paralysis adequate)
- **Intubation:** (Macintosh laryngoscope + gum elastic bougie, or video laryngoscope)
- **Confirmation:** ETCO₂ (waveform + value), chest rise, breath sounds

**4. MAINTENANCE:**
- **Volatile agents:** Sevoflurane 1-2%, Desflurane 3-6% ( MAC - minimum alveolar concentration)
- **IV agents:** Propofol infusion 4-12 mg/kg/hr (total IV anaesthesia - TIVA)
- **Opioids:** Fentanyl infusion, Remifentanil infusion (ultra-short acting)
- **Muscle relaxants:** Rocuronium, Vecuronium, Atracurium (as needed)
- **Ventilation:** tidal volume 6-8 mL/kg, RR 10-14, I:E 1:2, PEEP 5 cm H₂O

**5. EMERGENCE:**
- **Reverse NMBA:** (Sugammadex 2-4 mg/kg if Rocuronium/Vecuronium, Neostigmine 0.05 mg/kg + Glycopyrrolate 0.01 mg/kg if Atracurium)
- **Turn off volatile agent** (or stop propofol infusion)
- **100% oxygen** (until patient awake)
- **Extubate:** when awake, following commands, adequate respiratory effort, protective reflexes present

**MONITORING (minimum standards):**
- **ECG** (continuous)
- **SpO₂** (continuous)
- **NIBP** (every 5 minutes)
- **ETCO₂** (continuous - essential for intubated patients)
- **Temperature** (pre-induction, then every 30 minutes)
- **Inspired/expired volatile agent concentration** (if volatile anaesthesia)
- **Neuromuscular blockade** (if NMBA used)
- **Urine output** (for major surgery)

**INDUCTION AGENTS:**

**Propofol (most common):**
- **Advantages:** rapid onset, rapid recovery, antiemetic, bronchodilator
- **Disadvantages:** hypotension (vasodilatation, myocardial depression), pain on injection, apnoea
- **Dose:** 1.5-2.5 mg/kg IV (reduced in elderly, cardiovascular disease)

**Thiopental (barbiturate):**
- **Advantages:** rapid onset, cheap
- **Disadvantages:** cardiovascular depression, respiratory depression, prolonged recovery, nausea
- **Dose:** 3-5 mg/kg IV

**Etomidate:**
- **Advantages:** cardiovascular stability (minimal haemodynamic effects)
- **Disadvantages:** adrenal suppression (inhibits 11β-hydroxylase), nausea, vomiting, myoclonus
- **Dose:** 0.2-0.3 mg/kg IV
- **Indicated:** cardiovascular instability, trauma, sepsis

**Ketamine:**
- **Advantages:** cardiovascular stimulation (sympathomimetic), bronchodilator, analgesia, amnesia
- **Disadvantages:** hallucinations, emergence reactions, increased ICP, secretions
- **Dose:** 1-2 mg/kg IV
- **Indicated:** asthma, hypovolaemia, shock, trauma

**Sevoflurane (volatile):**
- **Advantages:** rapid induction, rapid recovery, minimal airway irritation (sweet smell)
- **Disadvantages:** malignant hyperthermia trigger, pollution, expensive
- **Dose:** 8% for induction, 1-2% for maintenance
- **Indicated:** inhalational induction (paediatrics), day case surgery

**MUSCLE RELAXANTS (NMBA):**

**Depolarising:**
- **Suxamethonium (SCh):** 1-1.5 mg/kg IV
- **Onset:** 30-60 seconds
- **Duration:** 5-10 minutes
- **Contraindications:** MH, hyperkalaemia (burns, spinal cord injury, prolonged immobility), open eye injury, raised ICP
- **Side effects:** fasciculations, myalgia, hyperkalaemia, malignant hyperthermia trigger, bradycardia (especially in children)

**Non-depolarising:**
- **Rocuronium:** 0.6 mg/kg IV (intubating dose), onset 60-90 sec, duration 30-40 min
- **Vecuronium:** 0.1 mg/kg IV, onset 2-3 min, duration 25-35 min
- **Atracurium:** 0.5 mg/kg IV, onset 2-3 min, duration 20-35 min (Hofmann elimination - good in renal failure)
- **Cisatracurium:** 0.15 mg/kg IV, onset 2-3 min, duration 30-40 min (Hofmann elimination, fewer histamine release)

**OPIOIDS:**

**Short-acting (intraoperative):**
- **Fentanyl:** 1-2 mcg/kg IV (onset 1-2 min, duration 30-60 min)
- **Remifentanil:** 0.1-0.5 mcg/kg/min infusion (context-sensitive half-life 3-5 min)
- **Alfentanil:** 5-10 mcg/kg IV (onset 30-60 sec, duration 10-15 min)

**POSTOPERATIVE ANALGESIA:**
- **Morphine:** 0.1-0.2 mg/kg IV/SC
- **PCA:** Morphine 1 mg bolus, 5 min lockout
- **Multimodal:** Paracetamol 1 g IV/PO QDS, NSAID (if appropriate), regional anaesthesia

**ANTIEMETICS:**
- **Dexamethasone 8 mg IV** (at induction)
- **Ondansetron 4 mg IV** (at end of surgery)
- **Metoclopramide 10 mg IV** (PRN)
- **Or:** Cyclizine 50 mg IV (PRN)

**FLUID MANAGEMENT:**
- **Maintenance:** 1-2 mL/kg/hr (crystalloid: Hartmann's or Plasma-Lyte)
- **Deficit:** preoperative fasting, insensible losses
- **Blood loss:** replace 3:1 (crystalloid:blood) or 1:1 (colloid:blood)
- **Goal:** euvolaemia (avoid under-resuscitation, over-resuscitation)

**COMPLICATIONS:**

**Cardiovascular:**
- **Hypotension:** (vasodilatation from volatile, propofol, spinal; hypovolaemia; sepsis; anaphylaxis)
- **Hypertension:** (light anaesthesia, pain, intubation response)
- **Arrhythmias:** (bradycardia from vagal stimulation, SCh, opioids; tachyarrhythmias from sympathetic stimulation, MH)

**Respiratory:**
- **Hypoxia:** (atelectasis, pneumonia, PE, bronchospasm, opioid-induced respiratory depression)
- **Hypercapnia:** (hypoventilation, bronchospasm, MH)
- **Bronchospasm:** (asthma, anaphylaxis, light anaesthesia)

**Other:**
- **Malignant hyperthermia:** (volatile anaesthetics, SCh)
- **Anaphylaxis:** (NMBAs, antibiotics, latex)
- **Awareness:** (light anaesthesia, patient recall) - incidence 1-20,000
- **PONV:** (postoperative nausea and vomiting) - incidence 20-30%

**Sources:** AAGBI Guidelines 2016, NICE NG179"""
        )

    def _handle_regional_anaesthesia(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle regional anaesthesia"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**REGIONAL ANAESTHESIA**

**DEFINITION:**
- **Anaesthesia** produced by blocking nerve conduction in a specific region
- **Advantages:** avoid GA, postoperative analgesia, reduced PONV, faster recovery, reduced DVT/PE
- **Disadvantages:** technical failure, nerve injury, LA toxicity, hemodynamic instability

**TYPES:**

**1. Central Neuraxial Blockade:**
- **Spinal (Subarachnoid block):** LA injected into subarachnoid space
- **Epidural:** LA injected into epidural space (outside dura)
- **Caudal:** epidural block at sacral hiatus (paediatrics)

**2. Peripheral Nerve Blockade:**
- **Single shot:** one-time injection
- **Continuous:** catheter for continuous infusion

**3. Plexus Blockade:**
- **Brachial plexus:** interscalene, supraclavicular, infraclavicular, axillary
- **Lumbar plexus:** psoas compartment, femoral, 3-in-1
- **Sacral plexus:** sciatic, posterior popliteal, parasacral

**SPINAL ANAESTHESIA:**

**Technique:**
- **Patient position:** sitting or lateral
- **Level:** L3-L4 or L4-L5 (iliac crest = L4)
- **Needle:** 25G or 27G pencil-point needle (Whitacre, Sprotte)
- **Approach:** midline, paramedian
- **Identification:** loss of resistance to air (or saline), CSF flow

**Local Anaesthetics:**
- **Hyperbaric Bupivacaine 0.5%:** (heavy, settles down) - 2-3 mL (10-15 mg)
- **Plain Bupivacaine 0.5%:** (isobaric) - 2-4 mL (10-20 mg)
- **Lidocaine 5%:** (short-acting) - 1.5-2 mL (75-100 mg)

**Additives:**
- **Fentanyl 10-25 mcg:** (prolongs block by ~30-60 min)
- **Morphine 0.1-0.2 mg:** (prolongs block 12-24 hours) - risk of respiratory depression, pruritus

**Block height:**
- **T4:** (nipples) - abdominal surgery
- **T10:** (umbilicus) - lower abdominal, inguinal
- **L1:** (groin) - orthopaedic lower limb

**Duration:**
- **Lidocaine:** 1-2 hours
- **Bupivacaine:** 2-4 hours

**Contraindications:**
- **Patient refusal**
- **Coagulopathy:** (therapeutic anticoagulation, bleeding diathesis)
- **Infection:** (local, systemic sepsis)
- **Raised ICP:** (relative)
- **Hypovolaemia:** (correct first)

**Complications:**
- **Post-dural puncture headache (PDPH):** (1-3% after spinal, higher if <25 years, female, pregnancy)
- **High spinal:** (respiratory paralysis, hypotension, bradycardia, unconsciousness)
- **Total spinal:** (if epidural dose given intrathecally - massive block)
- **Nerve injury:** (cauda equina syndrome, conus medullaris syndrome)
- **Backache:** (common, usually self-limiting)
- **Urinary retention:** (common, may require catheterisation)

**EPIDURAL ANAESTHESIA:**

**Technique:**
- **Patient position:** sitting or lateral
- **Level:** according to surgery (T10-T12 for lower limb, L1-L2 for lower abdominal)
- **Needle:** 16G or 18G Tuohy needle
- **Approach:** midline, paramedian
- **Identification:** loss of resistance to saline/air
- **Catheter:** thread 3-5 cm into epidural space
- **Test dose:** 3 mL Lidocaine 2% with Adrenaline 1:200,000 (to exclude IV or intrathecal placement)

**Local Anaesthetics:**
- **Bupivacaine 0.25-0.5%** (most common)
- **Levobupivacaine 0.25-0.5%** (less cardiotoxic)
- **Ropivacaine 0.2-1%** (less motor block, differential block)

**Dosing:**
- **Initial dose:** 10-20 mL (depends on concentration, level, desired block height)
- **Top-up:** 5-10 mL every 60-90 min
- **Continuous infusion:** 5-15 mL/hr (depends on concentration)

**Indications:**
- **Labour analgesia:** (most common)
- **Caesarean section:** (with adrenaline-containing LA)
- **Lower limb surgery:** (orthopaedic, vascular)
- **Abdominal surgery:** (lower abdominal, pelvic)
- **Thoracic surgery:** (thoracic epidural)
- **Postoperative analgesia:** (epidural infusion)

**Contraindications:**
- **Patient refusal**
- **Coagulopathy:** (therapeutic anticoagulation, bleeding diathesis)
- **Infection:** (local, systemic sepsis)
- **Raised ICP:** (relative)
- **Hypovolaemia:** (correct first)
- **Severe aortic stenosis:** (avoid - can cause catastrophic hypotension)

**Complications:**
- **Dural puncture:** (accidental wet tap - 0.5-3%)
- **Post-dural puncture headache:** (if dural puncture)
- **High/total spinal:** (if catheter migrates intrathecally)
- **Epidural haematoma:** (rare, catastrophic - spinal cord compression)
- **Epidural abscess:** (rare, catastrophic - spinal cord infection)
- **Nerve injury:** (rare)
- **Catheter problems:** (kinking, migration, difficult removal)

**PERIPHERAL NERVE BLOCKS:**

**Upper limb:**
- **Interscalene block:** (shoulder surgery) - risk of phrenic nerve block (hemidiaphragm paralysis)
- **Supraclavicular block:** (surgery below elbow) - most effective for upper limb
- **Infraclavicular block:** (surgery below elbow) - avoids phrenic nerve block
- **Axillary block:** (forearm, hand surgery) - spares musculocutaneous nerve
- **Wrist blocks:** (median, ulnar, radial nerves) - hand surgery

**Lower limb:**
- **Femoral nerve block:** (anterior thigh, knee surgery)
- **Sciatic nerve block:** (posterior thigh, leg, foot surgery)
- **3-in-1 block:** (femoral, obturator, lateral cutaneous nerve) - knee surgery
- **Ankle block:** (deep peroneal, superficial peroneal, saphenous, sural nerves) - foot surgery

**Trunk:**
- **Paravertebral block:** (thoracic or lumbar) - unilateral thoracic/abdominal wall anaesthesia
- **Transversus abdominis plane (TAP) block:** (abdominal wall, inguinal surgery)
- **Rectus sheath block:** (midline abdominal wall, umbilical surgery)
- **Ilioinguinal/iliohypogastric block:** (inguinal surgery)

**LOCAL ANAESTHETIC TOXICITY:**

**Causes:**
- **Accidental intravascular injection:** (high peak levels)
- **Excessive dose:** (weight-based maximum)
- **Rapid absorption:** (highly vascular areas)

**Symptoms:**
- **CNS:** circumoral numbness, metallic taste, tinnitus, agitation, seizures, coma
- **CV:** hypotension, bradycardia, arrhythmias, cardiovascular collapse

**Treatment:**
- **Stop injection immediately**
- **Airway:** secure airway, oxygen, ventilation (if seizures, respiratory depression)
- **Seizures:** benzodiazepines (Lorazepam 2 mg IV, Midazolam 2-5 mg IV)
- **Cardiovascular collapse:** ACLS (20% lipid emulsion therapy)

**LIPID EMULSION THERAPY:**
- **Indication:** local anaesthetic toxicity (CV collapse, refractory seizures)
- **Dose:** 20% lipid emulsion 1.5 mL/kg bolus, then 0.25 mL/kg/min infusion
- **Repeat:** bolus once if CV collapse persists
- **Duration:** continue until haemodynamic stability (up to 10 minutes)

**ULTRASOUND-GUIDED REGIONAL ANAESTHESIA:**
- **Advantages:** faster block onset, higher success rate, reduced LA dose, fewer complications, nerve visualisation
- **Standard of care** for most regional anaesthesia
- **Training required** (image interpretation, needle visualisation)

**Sources:** AAGBI Guidelines 2014, NICE NG179"""
        )

    def _handle_airway_management(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle airway management"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**AIRWAY MANAGEMENT**

**BASIC AIRWAY MANOEUVRES:**
- **Head tilt-chin lift:** (unless trauma → jaw thrust)
- **Oropharyngeal airway (Guedel):** (size: distance from incisors to angle of mandible)
- **Nasopharyngeal airway:** (size: diameter of little finger)
- **Bag-mask ventilation:** (2-person technique, oral airway, optimal head position)

**LARYNGOSCOPY:**

**Direct Laryngoscopy (Macintosh blade):**
- **Technique:** (left hand holds laryngoscope, right hand advances tube)
- **Grades:** (Cormack & Lehane)
   - **Grade 1:** full view of glottis
   - **Grade 2:** partial view of glottis (anterior commissure visible)
   - **Grade 3:** only epiglottis visible
   - **Grade 4:** epiglottis not visible

**Video Laryngoscopy:**
- **Indications:** (anticipated difficult airway, poor glottic view with direct laryngoscopy)
- **Advantages:** (improved glottic view, easier intubation, teaching tool)
- **Disadvantages:** (cost, learning curve, fogging)

**DIFFICULT AIRWAY PREDICTION:**

**History:**
- **Previous difficult airway:** (patient or family)
- **Airway trauma:** (surgery, radiation, burns)
- **Symptoms:** (stridor, dysphagia, sleep apnoea)

**Examination:**
- **Mouth opening:** (inter-incisor distance <3 cm = difficult)
- **Mallampati score:** (classify 1-4)
   - **Class 1:** (soft palate, fauces, uvula visible)
   - **Class 2:** (soft palate, fauces visible, uvula masked by base of tongue)
   - **Class 3:** (soft palate, base of uvula visible)
   - **Class 4:** (soft palate not visible)
   - **Class 3-4:** = difficult airway
- **Thyromental distance:** (<6.5 cm = difficult)
- **Sternomental distance:** (<12.5 cm = difficult)
- **Neck mobility:** (extension <35° = difficult)
- **BMI:** (>35 = difficult)
- **Facial abnormalities:** (micrognathia, retrognathia, macroglossia)

**INTUBATION:**

**Equipment:**
- **Laryngoscope:** (Macintosh blade 3-4 adult, 2-3 paediatric)
- **Endotracheal tube:** (size 7.0-8.0 mm adult, 3.5-4.5 mm paediatric)
- **Stylet:** (malleable metal stylet)
- **Gum elastic bougie:** (introducer for difficult intubation)
- **Suction:** (Yankauer sucker)

**Technique:**
1. **Pre-oxygenate:** (100% O₂ for 3-5 min)
2. **Position:** (sniffing position - head extended, neck flexed)
3. **Insert laryngoscope:** (right side of mouth, sweep tongue to left)
4. **Visualise:** (epiglottis, glottis)
5. **Pass tube:** (through vocal cords)
6. **Inflate cuff:** (10 mL air, check cuff pressure)
7. **Confirm:** (ETCO₂, chest rise, breath sounds)

**CONFIRMATION OF ETT PLACEMENT:**
- **Primary:** waveform capnography (ETCO₂ 35-45 mmHg)
- **Secondary:** chest rise, breath sounds (bilateral), no gastric sounds
- **Tertiary:** suction ( gastric contents? )

**SUPRAGLOTTIC AIRWAY DEVICES (SAD):**

**LMA (Laryngeal Mask Airway):**
- **Indications:** (airway maintenance during anaesthesia, difficult airway backup, airway rescue)
- **Types:** Classic, ProSeal (gastric access), i-gel (gel-filled cuff)
- **Size:** (based on weight: 1 = <5 kg, 1.5 = 5-10 kg, 2 = 10-20 kg, 2.5 = 20-30 kg, 3 = 30-50 kg, 4 = 50-70 kg, 5 = >70 kg)
- **Insertion:** (deflate cuff, lubricate, insert along hard palate, inflate cuff, secure)

**i-gel:**
- **Advantages:** (gel-filled cuff, no inflation needed, gastric channel, easier insertion)
- **Indications:** (airway maintenance, difficult airway, resuscitation)
- **Size:** (based on weight: 1 = <5 kg, 1.5 = 5-10 kg, 2 = 10-20 kg, 2.5 = 20-30 kg, 3 = 30-50 kg, 4 = 50-70 kg, 5 = >70 kg)

**INTUBATING AIDS:**

**Gum Elastic Bougie:**
- **Indication:** (difficult intubation - Grade 2 or 3 view)
- **Technique:** (pass bougie into trachea, rail road tracheal clicks, hold-up at bronchi, pass ETT over bougie)
- **Success rate:** (high for Grade 2-3 views)

**Stylet:**
- **Indication:** (improve ETV tip control, anterior vocal cords)
- **Technique:** (shape to "hockey stick", pass ETT over stylet)

**VIDEO LARYNGOSCOPE:**
- **Indication:** (difficult airway, poor glottic view with direct laryngoscopy)
- **Advantages:** (improved glottic view, easier intubation)
- **Types:** (GlideScope, McGrath, C-MAC)

**FIBREOPTIC INTUBATION:**
- **Indication:** (awake intubation, difficult airway, cervical spine immobilisation)
- **Technique:** (nasal or oral route, pass fibrescope into trachea, rail road tracheal rings/carina, pass ETT over fibrescope)
- **Disadvantages:** (learning curve, requires skill, time-consuming)

**EXTUBATION:**
- **Indications:** (patient awake, following commands, adequate respiratory effort, protective reflexes present, reversal of NMBA)
- **Technique:** (suction airway and mouth, deflate cuff, remove tube at end-inspiration)
- **Complications:** (laryngospasm, bronchospasm, breath-holding, airway obstruction)

**LARYNGOSPASM:**
- **Definition:** (reflex closure of vocal cords - spasm of adductor muscles)
- **Triggers:** (light anaesthesia, secretions, stimulation)
- **Signs:** (stridor, respiratory distress, desaturation, chest wall recession)
- **Treatment:**
   - **Remove stimulus:** (stop suction, stop surgical manipulation)
   - **Airway:** (jaw thrust, CPAP with 100% O₂)
   - **Deepen anaesthesia:** (Propofol 20-50 mg increments)
   - **Muscle relaxant:** (Suxamethonium 10-20 mg IV if severe, refractory)
- **Prevention:** (adequate depth of anaesthesia, extubate when fully awake, suction airway before extubation)

**CRICOTHYROIDOTOMY (SURGICAL AIRWAY):**
- **Indication:** (CICV - Cannot Intubate, Cannot Ventilate)
- **Technique:** (vertical skin incision, horizontal incision through cricothyroid membrane, dilate, insert bougie, insert ETT)
- **Complications:** (bleeding, laryngeal injury, failed placement, posterior tracheal wall injury)

**Sources:** DAS Guidelines 2015 (Difficult Airway Society), AAGBI Guidelines 2015"""
        )

    def _handle_postoperative_care(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle postoperative care"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**POSTOPERATIVE CARE (RECOVERY ROOM - PACU)**

**PHASES OF RECOVERY:**

**Phase 1 (PACU - Post-Anaesthetic Care Unit):**
- **Monitoring:** ECG, SpO₂, NIBP (every 5 min), temperature, pain, PONV, surgical site
- **Duration:** until modified Aldrete score ≥9
- **Discharge:** (ward, critical care, day surgery unit)

**Phase 2 (Day Surgery Unit - DSU):**
- **Monitoring:** observations, pain, PONV, oral fluids
- **Duration:** until ready for discharge home
- **Discharge:** (home with responsible adult)

**MODIFIED ALDRETE SCORE:**
- **Activity:** (2 = spontaneous movement of all extremities, 1 = limited movement, 0 = unable to move)
- **Respiration:** (2 = able to cough deeply, 1 = dyspnoea/limited breathing, 0 = apnoeic)
- **Circulation:** (2 = BP ±20% of baseline, 1 = BP ±20-50% of baseline, 0 = BP ±50% of baseline)
- **Consciousness:** (2 = fully awake, 1 = arousable on calling, 0 = not responding)
- **Oxygen saturation:** (2 = SpO₂ >92% on room air, 1 = requires O₂ 2-4 L/min to maintain >90%, 0 = SpO₂ <90% even with O₂)
- **Score ≥9:** (ready for discharge from PACU)

**PAIN MANAGEMENT:**

**Assessment:**
- **Pain score:** (0-10 numeric rating scale, VAS)
- **Goal:** (pain score <4)

**Analgesia:**
- **Mild pain (score 1-3):** Paracetamol 1 g IV/PO QDS ± NSAID (if not contraindicated)
- **Moderate pain (score 4-6):** Paracetamol + Opioid (Codeine 30-60 mg PO, Tramadol 50-100 mg PO/IV)
- **Severe pain (score 7-10):** Opioid (Morphine 2.5-5 mg IV/SC, repeat PRN)
- **PCA:** (Patient Controlled Analgesia) - Morphine 1 mg bolus, 5 min lockout
- **Regional:** (Epidural, nerve block) - if performed

**PONV (Postoperative Nausea and Vomiting):**

**Risk Factors:**
- **Patient-related:** (female, non-smoker, previous PONV/motion sickness)
- **Anaesthetic-related:** (volatile anaesthetics, opioids, nitrous oxide)
- **Surgery-related:** (laparoscopic, gynaecological, ear nose throat, prolonged surgery)

**Prophylaxis:**
- **Dexamethasone 8 mg IV** (at induction) - most effective
- **Ondansetron 4 mg IV** (at end of surgery) - add if high risk
- **Metoclopramide 10 mg IV** (PRN) - add if high risk
- **Droperidol 0.625-1.25 mg IV** (PRN) - add if high risk

**Treatment:**
- **Ondansetron 4 mg IV** (first line)
- **Metoclopramide 10 mg IV** (second line)
- **Cyclizine 50 mg IV** (second line)
- **Dexamethasone 4-8 mg IV** (if not already given)
- **Aprepitant 40 mg PO** (if refractory)

**HYPOXIA:**
- **Causes:** (atelectasis, pneumonia, PE, opioid-induced respiratory depression, residual NMBA)
- **Treatment:** (oxygen, physiotherapy, CPAP/NIV, reversal of NMBA, reversal of opioids)

**HYPOTENSION:**
- **Causes:** (hypovolaemia, vasodilatation from anaesthetic, sepsis, cardiac)
- **Treatment:** (IV fluids, vasopressors, treat underlying cause)

**HYPERTENSION:**
- **Causes:** (pain, anxiety, emergence, shivering, bladder distension)
- **Treatment:** (analgesia, anxiolysis, treat underlying cause)

**SHIVERING:**
- **Causes:** (hypothermia, pain, emergence)
- **Treatment:** (warm patient, tramadol 25-50 mg IV, pethidine 25-50 mg IV, clonidine 75 mcg PO)

**AGITATION/DELIRIUM:**
- **Causes:** (pain, hypoxia, hypercapnia, hypotension, sepsis, bladder distension, full urinary catheter)
- **Treatment:** (exclude organic causes, analgesia, oxygenation, treat sepsis, sedation if severe)

**TEMPERATURE:**
- **Hypothermia:** (<35°C) - warm patient (forced-air warmer, warm blankets, warm IV fluids)
- **Hyperthermia:** (>38°C) - exclude MH (malignant hyperthermia), sepsis, treat cause

**FLUIDS:**
- **Indications:** (thirst, hypotension, oliguria, high output losses)
- **Type:** (crystalloid: Hartmann's, Plasma-Lyte; colloids: Gelofusine, Voluven; blood)
- **Goal:** (euvolaemia - avoid under/over resuscitation)

**CATHETER:**
- **Indications:** (major surgery, anticipated large fluid shifts, need for accurate urine output, epidural)
- **Removal:** (when urine output adequate, patient ambulating)

**DISCHARGE CRITERIA:**

**To ward:**
- **Stable:** (observations stable for 30-60 min)
- **Aldrete score ≥9**
- **Pain:** (controlled)
- **PONV:** (minimal)
- **Surgical site:** (dry, no bleeding)
- **Airway:** (patent, patient protecting airway)

**To home (day surgery):**
- **Modified Aldrete score ≥9**
- **Able to drink:** (tolerating oral fluids)
- **Able to walk:** (mobility adequate)
- **Pain:** (controlled with oral analgesia)
- **PONV:** (minimal, tolerated oral fluids)
- **Responsible adult:** (to accompany for 24 hours)
- **Written instructions:** (what to expect, when to seek help)

**RED FLAGS (return to theatre):**
- **Bleeding:** (soaked dressings, hypotension, tachycardia)
- **Respiratory compromise:** (stridor, wheeze, desaturation)
- **Cardiac compromise:** (chest pain, ischaemic ECG changes, arrhythmias)
- **Surgical complications:** (anastomotic leak, organ injury)
- **Severe pain:** (uncontrolled despite analgesia)
- **Severe PONV:** (intractable vomiting, dehydration)

**Sources:** AAGBI Guidelines 2013, NICE NG179"""
        )

    def _handle_pain_management(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle pain management"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**PAIN MANAGEMENT (POSTOPERATIVE ANALGESIA)**

**PRINCIPLES:**
- **Multimodal analgesia:** (combining different analgesics to reduce opioid use)
- **Preventive:** (give analgesia before pain occurs - preemptive analgesia)
- **Regular:** (around-the-clock dosing, not PRN)
- **Patient-controlled:** (PCA - allows patient to titrate to effect)

**MULTIMODAL ANALGESIA:**

**1. Paracetamol (Acetaminophen):**
- **Dose:** (1 g IV/PO QDS - 4 g/day max)
- **Mechanism:** (central COX inhibition, cannabinoid receptor activation)
- **Advantages:** (opioid-sparing, safe, cheap)
- **Contraindications:** (liver failure, paracetamol allergy)

**2. NSAIDs (Non-steroidal anti-inflammatory drugs):**
- **Dose:** (Diclofenac 50-75 mg PO TDS, Ibuprofen 400-600 mg PO TDS)
- **IV:** (Diclofenac 75 mg IV TDS, Ketorolac 10-30 mg IV QDS)
- **Mechanism:** (COX inhibition - reduces prostaglandin synthesis)
- **Advantages:** (opioid-sparing, reduce inflammation)
- **Contraindications:** (renal impairment, peptic ulcer disease, bleeding diathesis, asthma with aspirin sensitivity, pregnancy)
- **Side effects:** (gastric irritation, renal impairment, bleeding, platelet inhibition)

**3. Opioids:**
- **Weak:** (Codeine 30-60 mg PO QDS, Tramadol 50-100 mg PO QDS)
- **Strong:** (Morphine 10-20 mg PO/SC QDS PRN, Oxycodone 5-15 mg PO QDS PRN)
- **IV:** (Morphine 2.5-5 mg IV/SC PRN, Oxycodone 5-10 mg IV PRN)
- **Mechanism:** (mu-opioid receptor agonism)
- **Advantages:** (potent analgesia)
- **Disadvantages:** (PONV, respiratory depression, sedation, constipation, urinary retention, pruritus)
- **Contraindications:** (respiratory failure, acute abdomen, undiagnosed abdominal pain)

**4. PCA (Patient Controlled Analgesia):**
- **Indications:** (major surgery, expected severe pain)
- **Setup:** (Morphine 1 mg/mL, bolus 1 mg, lockout 5 min, 4-hour max 10-20 mg)
- **Advantages:** (patient autonomy, consistent analgesia, patient satisfaction)
- **Disadvantages:** (requires understanding, equipment, monitoring)
- **Nurse-controlled analgesia:** (if patient unable to use PCA - cognitive impairment, frailty)

**5. Epidural Analgesia:**
- **Indications:** (major thoracic, abdominal, lower limb surgery)
- **Local anaesthetic:** (Bupivacaine 0.1%, Levobupivacaine 0.1%, Ropivacaine 0.2%)
- **Opioid:** (Fentanyl 2 mcg/mL, Morphine 0.05 mg/mL)
- **Dose:** (5-15 mL/hr infusion, top-up 5-10 mL PRN)
- **Advantages:** (excellent analgesia, opioid-sparing, reduced stress response)
- **Disadvantages:** (technical failure, hypotension, motor block, urinary retention, pruritus, nausea, respiratory depression)
- **Contraindications:** (coagulopathy, infection at site, patient refusal, severe hypovolaemia)

**6. Nerve Blocks:**
- **Indications:** (orthopaedic surgery, breast surgery, thoracic surgery)
- **Types:** (single shot, continuous catheter)
- **Local anaesthetic:** (Bupivacaine 0.25-0.5%, Levobupivacaine 0.25-0.5%, Ropivacaine 0.2-0.5%)
- **Duration:** (single shot 6-24 hours, catheter 2-5 days)
- **Advantages:** (excellent site-specific analgesia, opioid-sparing)
- **Disadvantages:** (technical failure, nerve injury, LA toxicity)

**7. Gabapentinoids:**
- **Gabapentin:** (300-600 mg PO nocte - start day before surgery, continue for 5-7 days)
- **Pregabalin:** (75-150 mg PO BD - start day before surgery, continue for 5-7 days)
- **Mechanism:** (binds α₂δ subunit of voltage-gated calcium channels - reduces neuropathic pain)
- **Indications:** (major surgery, chronic pain pre-op, plastic surgery, thoracic surgery)
- **Advantages:** (reduce opioid consumption, improve analgesia, reduce chronic pain)
- **Side effects:** (sedation, dizziness, visual disturbance)

**8. Ketamine:**
- **Dose:** (sub-anaesthetic dose: 0.1-0.5 mg/kg IV infusion or 0.25-0.5 mg PO QDS PRN)
- **Mechanism:** (NMDA receptor antagonism - reduces central sensitisation, opioid tolerance, hyperalgesia)
- **Indications:** (opioid-tolerant patients, major surgery, acute pain service involvement)
- **Advantages:** (opioid-sparing, reduces opioid tolerance, reduces hyperalgesia)
- **Side effects:** (hallucinations, dysphoria, nausea, sedation)

**9. Dexmedetomidine:**
- **Dose:** (0.2-0.7 mcg/kg/hr infusion)
- **Mechanism:** (α₂ agonist - sedative, analgesic, anxiolytic)
- **Indications:** (ICU sedation, mechanical ventilation, alcohol withdrawal, delirium)
- **Advantages:** (reduces opioid requirement, no respiratory depression, preserves respiratory drive)
- **Side effects:** (bradycardia, hypotension, sedation)

**REGIONAL TECHNIQUES:**

**Peripheral Nerve Catheters:**
- **Indications:** (major orthopaedic surgery: shoulder, elbow, wrist, hip, knee, ankle)
- **Duration:** (2-5 days)
- **Local anaesthetic:** (Ropivacaine 0.2%, Levobupivacaine 0.125%)
- **Infusion:** (5-10 mL/hr, bolus 5-10 mL PRN)

**Wound Infiltration:**
- **Indications:** (all surgical wounds)
- **Local anaesthetic:** (Bupivacaine 0.25-0.5%, 10-20 mL)
- **Technique:** (surgeon infiltrates wound before closure)
- **Advantages:** (simple, safe, cheap)

**Transversus Abdominis Plane (TAP) Block:**
- **Indications:** (abdominal surgery, inguinal hernia, caesarean section)
- **Local anaesthetic:** (Bupivacaine 0.25%, 15-20 mL each side)
- **Duration:** (12-24 hours)
- **Advantages:** (simple, safe, effective)

**PAIN ASSESSMENT:**
- **Numerical Rating Scale:** (0-10, 0 = no pain, 10 = worst pain imaginable)
- **Visual Analogue Scale:** (100 mm line, 0 = no pain, 100 = worst pain)
- **Faces Rating Scale:** (paediatrics, cognitive impairment)
- **Behavioural:** (facial expression, vocalisation, body movement, consolability)

**Goals:**
- **Resting pain:** (<3/10)
- **Dynamic pain:** (<5/10) - coughing, deep breathing, mobilising

**NON-PHARMACOLOGICAL:**
- **Psychological:** (preparation, reassurance, distraction)
- **Physiotherapy:** (early mobilisation, breathing exercises)
- **Heat/Cold:** (localised pain relief)
- **TENS:** (transcutaneous electrical nerve stimulation)
- **Acupuncture:** (may reduce opioid requirement)

**Sources:** AAGBI Guidelines 2020, NICE NG189"""
        )

    def _handle_critical_care(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle critical care"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**CRITICAL CARE (ITU/ICU)**

**ADMISSION CRITERIA:**

**Level 2 (High Dependency Unit - HDU):**
- **Single organ failure** (requiring advanced monitoring)
- **Post-major surgery** (high-dependency care)
- **Step-down from Level 3**

**Level 3 (Intensive Therapy Unit - ITU/ICU):**
- **Multi-organ failure** (requiring advanced respiratory/ cardiovascular support)
- **Mechanical ventilation** (invasive or non-invasive)
- **Advanced cardiovascular support** (vasopressors, inotropes)
- **Renal replacement therapy** (dialysis, haemofiltration)

**ORGAN SUPPORT:**

**Respiratory Support:**
- **Level 1:** (oxygen by mask, nasal cannulae)
- **Level 2:** (non-invasive ventilation - CPAP/BiPAP)
- **Level 3:** (invasive mechanical ventilation - endotracheal tube, tracheostomy)

**Cardiovascular Support:**
- **Level 1:** (inotropes/vasopressors via peripheral line)
- **Level 2:** (inotropes/vasopressors via central line, basic monitoring)
- **Level 3:** (advanced cardiovascular support - arterial line, CVC, PAC, echocardiography)

**Renal Support:**
- **Indications:** (severe AKI, refractory metabolic acidosis, hyperkalaemia, fluid overload, uraemia)
- **Types:** (haemodialysis, haemofiltration, peritoneal dialysis)

**NEUROLOGICAL SUPPORT:**
- **ICP monitoring:** (intracranial pressure bolt, ventricular catheter)
- **Seizure management:** (EEG monitoring, anticonvulsants)
- **Therapeutic hypothermia:** (targeted temperature management after cardiac arrest)

**INVASIVE MONITORING:**

**Arterial Line:**
- **Indications:** (haemodynamic instability, vasopressors, frequent ABG, close monitoring)
- **Sites:** (radial, brachial, femoral)
- **Complications:** (bleeding, thrombosis, infection, limb ischaemia)

**Central Venous Catheter (CVC):**
- **Indications:** (vasopressors, central venous pressure monitoring, TPN, poor peripheral access)
- **Sites:** (internal jugular, subclavian, femoral)
- **Types:** (single lumen, double lumen, triple lumen, quadruple lumen)
- **Complications:** (pneumothorax, haemothorax, arterial puncture, infection, thrombosis)

**Pulmonary Artery Catheter (PAC):**
- **Indications:** (shock, pulmonary oedema, severe cardiac failure, major surgery)
- **Measurements:** (CVP, RAP, RV pressure, PAP, PAOP/PCWP, Cardiac Output, SVR)
- **Complications:** (arrhythmias, infection, PA rupture, pulmonary infarction)

**Cardiac Output Monitoring:**
- **Oesophageal Doppler:** (minimally invasive)
- **Pulse Contour Analysis:** (PiCCO, LiDCO - arterial waveform analysis)
- **Bioreactance:** (NICOM, bioreactance)
- **Echocardiography:** (transoesophageal - TEE, transthoracic - TTE)

**MECHANICAL VENTILATION:**

**Modes:**
- **Volume Controlled:** (VCV - set tidal volume, rate, I:E, PEEP)
- **Pressure Controlled:** (PCV - set inspiratory pressure, rate, I:E, PEEP)
- **Pressure Support Ventilation (PSV):** (patient triggers, set pressure support, PEEP)
- **SIMV (Synchronised Intermittent Mandatory Ventilation):** (combination of controlled and spontaneous)
- **CPAP (Continuous Positive Airway Pressure):** (spontaneous breathing with PEEP)

**Settings:**
- **Tidal volume:** (6-8 mL/kg - lung-protective strategy)
- **Respiratory rate:** (10-20 breaths/min - target PaCO₂ 4.5-6 kPa)
- **FiO₂:** (0.21-1.0 - target SpO₂ 94-98%)
- **PEEP:** (5-10 cm H₂O - recruit alveoli, improve oxygenation)
- **I:E ratio:** (1:2 or 1:1.5 - allow adequate expiratory time)

**Complications:**
- **Barotrauma:** (pneumothorax, pneumomediastinum)
- **Volutrauma:** (alveolar overdistension)
- **Atelectrauma:** (atelectasis from cyclic opening/closing)
- **Biotrauma:** (inflammatory response from mechanical ventilation)
- **VAP:** (Ventilator-Associated Pneumonia - after 48 hours)

**WEANING:**
- **Spontaneous Breathing Trial (SBT):** (T-piece, CPAP 5 cm H₂O, low PS)
- **Criteria for weaning:** (resolution of underlying cause, adequate gas exchange, haemodynamic stability, patient able to trigger breaths)
- **Extubation:** (once SBT passed - adequate respiratory effort, strong cough, minimal secretions)

**VASOPRESSORS/INOTROPES:**

**Noradrenaline (Norepinephrine):**
- **First-line vasopressor** (septic shock, cardiogenic shock)
- **Dose:** (0.05-0.5 mcg/kg/min)
- **Effect:** (α1 dominant - vasoconstriction)

**Adrenaline (Epinephrine):**
- **Second-line vasopressor** (refractory septic shock, cardiogenic shock, anaphylaxis)
- **Dose:** (0.05-0.5 mcg/kg/min)
- **Effect:** (α1 + β1 + β2 - vasoconstriction, inotropy, bronchodilatation)

**Dopamine:**
- **Alternative vasopressor** (selected patients)
- **Dose:** (2-20 mcg/kg/min)
- **Effect:** (dose-dependent: dopaminergic <5 mcg/kg/min, β1 5-10 mcg/kg/min, α1 >10 mcg/kg/min)

**Dobutamine:**
- **Inotrope** (cardiogenic shock, low cardiac output)
- **Dose:** (2.5-20 mcg/kg/min)
- **Effect:** (β1 + β2 - inotropy, vasodilatation)

**Milrinone:**
- **Inotrope** (cardiogenic shock, weaning from CPB)
- **Dose:** (loading: 50 mcg/kg over 10 min, infusion: 0.375-0.75 mcg/kg/min)
- **Effect:** (phosphodiesterase III inhibitor - inotropy, vasodilatation)

**Vasopressin:**
- **Second-line vasopressor** (refractory septic shock - catecholamine-sparing)
- **Dose:** (0.03 units/min)
- **Effect:** (V1 receptor stimulation - vasoconstriction)

**SEDATION:**

**Propofol:**
- **First-line sedative** (most critically ill patients)
- **Dose:** (1-4 mg/kg/hr infusion)
- **Advantages:** (rapid onset, rapid offset, titratable, reduces ICP)
- **Disadvantages:** (hypotension, hypertriglyceridaemia, propofol infusion syndrome)

**Midazolam:**
- **Second-line sedative** (if propofol contraindicated)
- **Dose:** (0.02-0.2 mg/kg/hr infusion)
- **Advantages:** (anxiolysis, amnesia, no hypotension)
- **Disadvantages:** (prolonged infusion leads to accumulation, delayed recovery)

**Dexmedetomidine:**
- **Sedative for lighter sedation** (awake, cooperative)
- **Dose:** (0.2-0.7 mcg/kg/hr infusion)
- **Advantages:** (analgesic-sparing, no respiratory depression, preserves respiratory drive, delirium-sparing)
- **Disadvantages:** (bradycardia, hypotension)

**NEUROMUSCULAR BLOCKADE:**
- **Indications:** (facilitate mechanical ventilation, reduce oxygen consumption, treat shivering, treat raised ICP)
- **Agents:** (Atracurium, Cisatracurium, Vecuronium, Rocuronium)
- **Monitoring:** (train-of-four monitoring - goal 1-2 twitches)
- **Reversal:** (Sugammadex for Rocuronium/Vecuronium, Neostigmine for Atracurium/Cisatracurium)

**DELIRIUM:**
- **Prevention:** (minimise sedation, early mobilisation, orientation, sleep optimisation, avoid benzodiazepines)
- **Treatment:** (exclude organic causes, optimise analgesia, treat underlying cause, antipsychotics if severe - Haloperidol, Quetiapine)

**Sources:** FICS (Faculty of Intensive Care Medicine), NICE NG145"""
        )

    def _handle_general_anesthesiology(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general anesthesiology query"""
        return DomainQueryResult(
            domain_name="anesthesiology",
            answer="""**ANESTHESIOLOGY - General Consultation**

Anesthesiology provides perioperative care, anaesthesia, pain management, and critical care.

**SCOPE:**

**Perioperative Care:**
- Preoperative assessment and optimisation
- Intraoperative management
- Postoperative care (PACU)
- Critical care (ITU/ICU)

**Anaesthesia Techniques:**
- General anaesthesia
- Regional anaesthesia (spinal, epidural, nerve blocks)
- Local anaesthesia
- Sedation

**Pain Management:**
- Acute pain (postoperative, trauma, medical)
- Chronic pain (interventional procedures)
- Cancer pain
- Multimodal analgesia

**Critical Care:**
- Level 2 (High Dependency Unit - HDU)
- Level 3 (Intensive Therapy Unit - ITU/ICU)
- Mechanical ventilation
- Cardiovascular support (inotropes, vasopressors)
- Renal replacement therapy

**COMMON PROCEDURES:**

**Anaesthesia for:**
- General surgery
- Orthopaedic surgery
- Gynaecological surgery
- Obstetric surgery (Caesarean section)
- Paediatric surgery
- Cardiac surgery
- Thoracic surgery
- Neurosurgery
- Plastic surgery
- Day surgery

**Airway Management:**
- Bag-mask ventilation
- Supraglottic airway devices (LMA, i-gel)
- Intubation (direct laryngoscopy, video laryngoscopy)
- Fibreoptic intubation
- Surgical airway (cricothyroidotomy)

**Monitoring:**
- Basic: ECG, SpO₂, NIBP, Temperature
- Advanced: ETCO₂, invasive BP, CVP, arterial line, cardiac output
- Neuromuscular blockade monitoring

**COMPLICATIONS:**

**Cardiovascular:**
- Hypotension, Hypertension
- Arrhythmias
- Cardiac arrest

**Respiratory:**
- Hypoxia, Hypercapnia
- Bronchospasm
- Pneumothorax

**Neurological:**
- Awareness (recall under anaesthesia)
- Nerve injury
- Stroke (perioperative)

**Other:**
- Malignant hyperthermia
- Anaphylaxis
- PONV (postoperative nausea and vomiting)
- Dental injury
- Eye injury
- Peripheral neuropathy

**Sources:** AAGBI Guidelines, Royal College of Anaesthetists, NICE Guidelines"""
        )


def create_anesthesiology_domain():
    """Factory function to create anesthesiology domain"""
    return AnesthesiologyDomain()
