"""
GPDISC ENT (Otolaryngology) Domain Module

This module provides ear, nose, and throat consultation capabilities including:
- Ear conditions (otitis externa, otitis media, tinnitus, vertigo, hearing loss)
- Nasal and sinus conditions (rhinosinusitis, nasal polyps, epistaxis)
- Throat conditions (sore throat, tonsillitis, hoarseness, dysphagia)
- Neck lumps and salivary gland disorders
- Head and neck cancer awareness
- Emergency ENT conditions

Evidence-based with guidelines from:
- ENT UK (British Association of Otolaryngology)
- NICE ENT Guidelines
- American Academy of Otolaryngology (AAO-HNS)
- Cochrane ENT reviews
"""

from typing import Optional, Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class ENTDomain(BaseDomainModule):
    """
    ENT specialty domain for ear, nose, and throat conditions.

    Covers comprehensive ENT consultation including:
    - Ear conditions (otitis externa, otitis media, tinnitus, vertigo, hearing loss)
    - Nasal and sinus conditions (rhinosinusitis, nasal polyps, epistaxis)
    - Throat conditions (sore throat, tonsillitis, hoarseness, dysphagia)
    - Neck lumps and salivary gland disorders
    - Head and neck cancer awareness
    - Emergency ENT conditions
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="ent",
            version="1.0.0",
            dependencies=[],
            description="ENT (Otolaryngology): Ear, nose, and throat conditions, hearing loss, sinusitis, sore throat",
            keywords=[
                "ent", "ear", "nose", "throat", "otolaryngology", "otorhinolaryngology",
                "earache", "ear pain", "otalgia",
                "ear infection", "otitis externa", "otitis media", "glue ear",
                "hearing loss", "deafness", "hard of hearing",
                "tinnitus", "ringing in ears", "buzzing in ears",
                "vertigo", "dizziness", "spinning", "meniere's",
                "discharge", "ear discharge", "runny ear",
                "sinus", "sinusitis", "rhinosinusitis", "sinus infection",
                "nasal", "nose", "blocked nose", "stuffy nose", "nasal congestion",
                "nasal polyps", "polyps",
                "epistaxis", "nosebleed", "nose bleed",
                "rhinitis", "allergic rhinitis", "hay fever",
                "sore throat", "throat pain", "tonsillitis", "quinsy",
                "hoarse", "hoarseness", "voice loss", "laryngitis",
                "swallowing", "difficulty swallowing", "dysphagia",
                "lump in throat", "globus",
                "tonsillitis", "tonsillectomy", "tonsil stones",
                "glandular fever", "mononucleosis",
                "neck lump", "swollen gland", "lymphadenopathy",
                "salivary gland", "parotid", "submandibular",
                "adenoids", "adenoidectomy",
                "snoring", "sleep apnoea", "obstructive sleep apnoea",
                "foreign body", "something in ear", "something in nose", "something in throat",
                "stridor", "noisy breathing", "croup",
                "head and neck cancer", "throat cancer", "laryngeal cancer", "oral cancer"
            ],
            capabilities=[
                "ear_conditions", "sinusitis_management", "sore_throat_evaluation",
                "hearing_assessment", "vertigo_management", "nosebleed_management",
                "hoarseness_evaluation", "neck_lump_assessment", "ent_emergencies"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Process ENT queries with appropriate specialty routing"""
        query_lower = query.lower()

        # Emergencies - HIGHEST PRIORITY
        if any(term in query_lower for term in ["stridor", "noisy breathing", "croup", "epiglottitis", "quinsy", "peritonsillar abscess", "airway obstruction"]):
            return self._handle_airway_emergency(query, context)

        # Ear conditions
        elif any(term in query_lower for term in ["earache", "ear pain", "otalgia", "ear infection", "otitis externa", "otitis media", "glue ear", "discharging ear"]):
            return self._handle_ear_pain(query, context)

        elif any(term in query_lower for term in ["hearing loss", "deafness", "hard of hearing", "can't hear"]):
            return self._handle_hearing_loss(query, context)

        elif any(term in query_lower for term in ["tinnitus", "ringing", "buzzing", "ear noise"]):
            return self._handle_tinnitus(query, context)

        elif any(term in query_lower for term in ["vertigo", "dizziness", "spinning", "meniere's", "room spinning", "loss of balance"]):
            return self._handle_vertigo(query, context)

        # Nasal and sinus conditions
        elif any(term in query_lower for term in ["sinus", "sinusitis", "rhinosinusitis", "sinus infection", "facial pain", "sinus headache"]):
            return self._handle_sinusitis(query, context)

        elif any(term in query_lower for term in ["nosebleed", "epistaxis", "nose bleed"]):
            return self._handle_epistaxis(query, context)

        elif any(term in query_lower for term in ["nasal polyps", "polyps", "nose polyp"]):
            return self._handle_nasal_polyps(query, context)

        elif any(term in query_lower for term in ["blocked nose", "stuffy nose", "nasal congestion", "runny nose", "rhinitis", "hay fever", "allergic rhinitis"]):
            return self._handle_rhinitis(query, context)

        # Throat conditions
        elif any(term in query_lower for term in ["sore throat", "throat pain", "tonsillitis", "tonsil", "quinsy", "peritonsillar abscess"]):
            return self._handle_sore_throat(query, context)

        elif any(term in query_lower for term in ["hoarse", "hoarseness", "voice loss", "lost voice", "laryngitis"]):
            return self._handle_hoarseness(query, context)

        elif any(term in query_lower for term in ["swallowing", "difficulty swallowing", "dysphagia", "choking", "food sticking"]):
            return self._handle_dysphagia(query, context)

        elif any(term in query_lower for term in ["lump in throat", "globus", "throat lump"]):
            return self._handle_globus(query, context)

        # Neck and glands
        elif any(term in query_lower for term in ["neck lump", "swollen gland", "lymphadenopathy", "enlarged lymph node"]):
            return self._handle_neck_lump(query, context)

        elif any(term in query_lower for term in ["salivary gland", "parotid", "submandibular"]):
            return self._handle_salivary_gland(query, context)

        # Foreign bodies
        elif any(term in query_lower for term in ["foreign body", "something in ear", "something in nose", "something in throat", "choked on"]):
            return self._handle_foreign_body(query, context)

        # Snoring and sleep apnoea
        elif any(term in query_lower for term in ["snoring", "sleep apnoea", "sleep apnea", "stop breathing", "choking at night"]):
            return self._handle_snoring_sleep_apnoea(query, context)

        # General ENT
        else:
            return self._handle_general_ent(query, context)

    def _handle_airway_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle airway emergencies - STRIDOR, CROUP, EPIGLOTTITIS"""
        answer = """**AIRWAY EMERGENCY - STRIDOR**

**⚠️ URGENT REFERRAL REQUIRED - POTENTIAL AIRWAY OBSTRUCTION**

---

## STRIDOR

**Definition**: Noisy breathing caused by turbulent airflow through narrowed upper airway

**Key Question**: **When does the stridor occur?**

---

## INSPIRATORY STRIDOR (INHALATION)

**Indicates**: Supraglottic or glottic obstruction

**Causes**:

### ACUTE EPIGLOTTITIS

**EMERGENCY** (rare due to Hib vaccination, but still occurs)

**Pathogen**: *Haemophilus influenzae* type B (Hib), other bacteria

**Age**: 2-7 years (but can occur in adults)

**Clinical Features**:
- **Rapid onset** (hours)
- **Severe sore throat** (out of proportion to exam)
- **Drooling**, inability to swallow
- **Muffled voice**, "hot potato voice"
- **Prefers sitting**, leaning forward (tripod position)
- **Toxic appearance**, high fever
- **Stridor**: Inspiratory
- **IMPORTANT**: **DO NOT examine throat** (may precipitate airway obstruction)

**Management**:
- **IMMEDIATE EMERGENCY** (call 999)
- **Urgent transfer** to hospital with ENT and anesthesia support
- **DO NOT upset child** (keep with parents, calm environment)
- **DO NOT examine throat**
- **IV antibiotics** (ceftriaxone)
- **Airway**: Intubation or tracheostomy (may be needed urgently)

---

### CROUP (Laryngotracheobronchitis)

**Viral**: Parainfluenza virus (most common)

**Age**: 6 months to 3 years (peak 2 years)

**Clinical Features**:
- **Barking cough**: ("seal-like")
- **Inspiratory stridor**
- **Hoarse voice**
- **Low-grade fever**
- **Worse at night**: (often)
- **Duration**: 3-7 days
- **Season**: Autumn, winter

**Management**:

**Mild Croup** (no stridor at rest):
- **Reassurance**
- **Cool mist**: (humidified air, though evidence limited)
- **Keep child calm** (agitation worsens stridor)
- **Observation**

**Moderate-Severe Croup** (stridor at rest, recessions):
- **Oral dexamethasone**: 0.15 mg/kg (single dose) OR prednisolone 1-2 mg/kg
- **Nebulized adrenaline**: 1:1000, 5 mL (if severe, admitted for observation)
- **Oxygen**: If hypoxic
- **ADMIT**: If severe, persistent stridor, hypoxia, dehydration

**Red Flags**:
- **Silent chest**: (impending respiratory failure)
- **Altered mental status**: (fatigue, cyanosis)
- **Dehydration**

---

### BACTERIAL TRACHEITIS

**Rare but serious**

**Pathogen**: *Staph aureus*, *Strep pyogenes*

**Clinical Features**:
- **Similar to croup** initially
- **High fever**, toxic appearance
- **Thick purulent secretions** in trachea
- **Worsening despite** croup treatment
- **Stridor**: Biphasic

**Management**:
- **ADMIT** (ICU)
- **IV antibiotics** (cefotaxime + flucloxacillin)
- **Airway**: May need intubation (secretions can block tube)

---

## BI-PHASIC STRIDOR (INSPIRATORY AND EXPIRATORY)

**Indicates**: Glottic or subglottic obstruction

**Causes**:
- **Foreign body aspiration**
- **Croup**
- **Vocal cord paralysis** (bilateral)
- **Subglottic stenosis** (post-intubation)

---

## EXPIRATORY STRIDOR (EXHALATION)

**Indicates**: Tracheobronchial obstruction

**Causes**:
- **Asthma** (wheeze, not true stridor, but may be confused)
- **Tracheomalacia** (infants)
- **Lower airway foreign body**

---

## FOREIGN BODY ASPIRATION

**Common in** 1-3 year olds

**Clinical Features**:
- **Sudden onset** choking, coughing
- **Stridor** (depends on location)
- **Unilateral wheeze** (if in bronchus)
- **Asymmetrical breath sounds**
- **May be asymptomatic** initially

**Management**:
- **If choking**: Back blows, chest thrusts (child)
- **DO NOT** blind finger sweep
- **Urgent referral**: To pediatric ENT for bronchoscopy
- **CXR**: May show air trapping, mediastinal shift

---

## CONGENITAL CAUSES

**Laryngomalacia**:
- **Most common** congenital cause of stridor
- **Stridor**: Inspiratory, worse with feeding, crying
- **Onset**: First weeks of life
- **Improves**: By 12-18 months
- **Management**: Reassurance, monitoring

**Subglottic stenosis**:
- **Stridor**: Biphasic
- **History**: Previous intubation (most common)
- **Management**: ENT referral, may need surgery

**Vocal cord paralysis**:
- **Bilateral**: Stridor, weak cry (birth trauma, cardiac surgery)
- **Unilateral**: Weak cry, aspiration risk

---

## ASSESSMENT OF STRIDOR

**History**:
- **Onset**: (sudden vs gradual)
- **Timing**: (at rest vs with activity, day vs night)
- **Feeding**: (difficulty swallowing, choking)
- **Voice**: (hoarse, weak, muffled)
- **Trauma**: (recent intubation, choking episode)
- **Fever**: (suggests infection)

**Examination**:
- **Observation**: (stridor pattern, work of breathing, color, alertness)
- **Auscultation**: (breath sounds, wheeze, stridor)
- **CAUTION**: Do NOT upset child if epiglottitis suspected

---

**Sources: NICE NG9 Feverish illness in children, ENT UK Croup Guidelines, RCPCH Guidelines**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.96,
            metadata={
                "specialty": "ent",
                "focus": "airway_emergency",
                "urgency": "emergency",
                "sources": ["NICE NG9", "ENT UK Croup Guidelines", "RCPCH Guidelines"]
            }
        )

    def _handle_ear_pain(self, query: str, context: dict) -> DomainQueryResult:
        """Handle ear pain (otalgia)"""
        answer = """**EAR PAIN (OTALGIA)**

---

## CLASSIFICATION

**Primary Otalgia**: Pain originating from ear
**Secondary (Referred) Otalgia**: Pain referred to ear from non-ear structures

---

## OTITIS EXTERNA

**Inflammation** of external auditory canal

**Causes**:
- **Trauma**: (cotton buds, fingernails, hearing aids)
- **Moisture**: (swimming, humid environment)
- **Dermatitis**: (eczema, psoriasis, seborrheic)
- **Infection**: (bacterial, fungal)

**Bacterial** (most common):
- **Pseudomonas aeruginosa** (most common)
- **Staphylococcus aureus**

**Fungal** (otomycosis):
- **Aspergillus** (black/white/green spores)
- **Candida** (white creamy)

---

**Clinical Features**:
- **Pain**: (severe, exacerbated by ear movement, tragus pressure)
- **Itch**: (often)
- **Discharge**: (white, yellow, green)
- **Hearing loss**: (mild, if canal swollen)
- ** canal**: Swollen, erythematous, narrowed

**Management**:

**Mild** (canal not obstructed):
- **Topical antibiotic**: (as directed by ENT)
  - **Ciprofloxacin 0.3%** with dexamethasone (Cilodex) 3-4 drops TID
  - OR **Gentamicin 0.3%** with betamethasone 0.1% (Betnesol) 3-4 drops TID
- **Duration**: 7 days
- **Aural toilet**: (if discharge obscuring canal, ENT may debride)
- **Keep dry**: (avoid swimming, use cotton wool with Vaseline when washing)
- **Analgesia**: Paracetamol, ibuprofen

**Severe** (canal obstructed):
- **ENT referral** (for aural toilet, wick insertion)
- **Topical antibiotic**: (as above, delivered via wick)

**Fungal**:
- **Topical antifungal**: (clotrimazole 1% solution BID)
- **Aural toilet**: (to remove spores, debris)
- **Keep dry**

**Prevention**:
- **Avoid trauma**: (no cotton buds in ear canal)
- **Keep dry**: (after swimming, use hair dryer on cool setting)
- **Ear drops**: (prophylactic alcohol/acetic acid if recurrent)

---

## OTITIS MEDIA

**Inflammation** of middle ear

### ACUTE OTITIS MEDIA (AOM)

**Bacterial infection** of middle ear

**Pathogens**:
- **Streptococcus pneumoniae** (most common)
- **Haemophilus influenzae**
- **Moraxella catarrhalis**

**Risk Factors**:
- **Age**: 6-24 months (peak)
- **Attendance**: (daycare)
- **Smoking**: (parental)
- **Feeding**: (bottle-feeding, supine)
- **Family history**
- **Cleft palate**, Down syndrome

**Clinical Features**:
- **Ear pain**: (sudden onset)
- **Fever**: (common, especially in children)
- **Irritability**: (infants)
- **Hearing loss**: (mild, conductive)
- **Otorrhoea**: (if tympanic membrane perforates)
- **Symptoms of URTI**: (cough, coryza)
- **Tympanic membrane**: Bulging, erythematous, obscured landmarks, decreased mobility

**Management**:

**Immediate Antibiotics** (NICE recommends):
- **Systemic features**: Fever >38°C, systemically unwell
- **Bilateral AOM**: In infants <2 years
- **Otorrhoea**: (discharge from ear)
- **Symptoms >4 days**: No improvement

**Antibiotic** (first-line):
- **Amoxicillin**: 40mg/kg/day TID (children) OR 500mg TDS (adults) for 5 days
- **Alternative** (if penicillin allergy):
  - **Clarithromycin**: 15mg/kg/day BID (children) OR 500mg BD (adults)
  - OR **Erythromycin**

**Delayed Antibiotic Prescribing** (2-3 days):
- **No systemic features**
- **Unilateral** in children >2 years
- **Mild symptoms**

**Supportive**:
- **Analgesia**: Paracetamol, ibuprofen (effective for pain)
- **Avoid**: (cotton buds in ear)

**Follow-up**:
- **Review** if no improvement after 3 days on antibiotics
- **Refer** if recurrent AOM (≥3 episodes in 6 months, ≥4 in 12 months)

---

### OTITIS MEDIA WITH EFFUSION (OME, "Glue Ear")

**Fluid** in middle ear without infection

**Clinical Features**:
- **Hearing loss**: (conductive, fluctuating)
- **Delayed speech**: (in children)
- **Behavioral problems**: (inattention, frustration)
- **Otalgia**: (absent, distinguishes from AOM)
- **Tympanic membrane**: Dull, retracted, air-fluid level, bubbles

**Management**:

**Initial** (3 months):
- **Observation**: (80% resolve spontaneously)
- **Autoinflation**: (Otovent, nasal balloon) - evidence limited
- **Hearing assessment**: (if concerns)

**Persistent** (>3 months with hearing loss):
- **Grommets** (ventilation tubes): (surgical)
  - **Indications**: Bilateral OME >3 months with hearing loss >25 dB, speech delay, educational problems
  - **Procedure**: Day case, small incision in tympanic membrane, insert tube
  - **Duration**: Tubes extrude spontaneously (6-12 months)
  - **Benefit**: Improved hearing, reduced infections

**Adenoidectomy**:
- **Adjuvant** to grommets for recurrent OME or AOM

---

## MASTOIDITIS

**Complication** of otitis media

**Clinical Features**:
- **Ear pain**, swelling behind ear
- **Protrusion** of pinna (downward, outward)
- **Fever**, malaise
- **Erythema**, tenderness over mastoid

**Management**:
- **Urgent ENT referral**
- **IV antibiotics**: (ceftriaxone)
- **Surgical drainage**: (if abscess)

---

## SECONDARY (REFERRED) OTALGIA

**Pain referred** to ear from non-ear structures

**Causes**:

**Temporomandibular Joint (TMJ)**:
- **Pain**: (worse with chewing)
- **Clicking**, limitation of opening
- **Tenderness**: (over TMJ)

**Dental**:
- **Tooth infection**, impacted wisdom tooth
- **Referred pain**: to ear

**Cervical spine**:
- **C2, C3**: (C3-C4 facet joints, atlantoaxial joint)

**Malignancy**:
- **Head and neck cancer**: (nasopharynx, tonsil, tongue base, larynx, pyriform sinus)
- **Red flag**: Persistent otalgia with no ear findings, especially if smoking/alcohol history

**Other**:
- **Sore throat**, tonsillitis
- **Glossopharyngeal neuralgia**: (severe paroxysmal pain, throat, ear, neck)

---

## DIFFERENTIAL DIAGNOSIS OF EAR PAIN

| Feature | Otitis Externa | Acute Otitis Media | Otitis Media with Effusion |
|---------|----------------|-------------------|---------------------------|
| Pain | Severe, worse with ear movement | Moderate-severe | Absent |
| Fever | Uncommon | Common | Absent |
| Hearing loss | Mild | Mild-moderate | Moderate |
| Discharge | Common | Perforation | Absent |
| Tympanic membrane | Canal swollen | Bulging, erythematous | Dull, retracted |
| Tragus pain | Yes | No | No |

---

## WHEN TO REFER

**Urgent** (same day):
- **Mastoiditis** (swelling behind ear, fever)
- **Severe otitis externa** (canal obstructed, needs aural toilet)
- **Perforated tympanic membrane** with profuse discharge

**Routine**:
- **Recurrent AOM** (≥3 in 6 months, ≥4 in 12 months)
- **Persistent OME** (>3 months with hearing loss)
- **Suspected TMJ dysfunction** (dental referral)
- **Unexplained otalgia** (persistent >4 weeks, especially with smoking/alcohol)

---

**Sources: NICE NG87 Otitis Media, ENT UK Otitis Externa Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "ent",
                "focus": "ear_pain_otalgia",
                "sources": ["NICE NG87", "ENT UK Otitis Externa Guidelines", "CKS"]
            }
        )

    def _handle_hearing_loss(self, query: str, context: dict) -> DomainQueryResult:
        """Handle hearing loss"""
        answer = """**HEARING LOSS**

---

## CLASSIFICATION

**Conductive**: (sound transmission blocked) - External or middle ear
**Sensorineural**: (cochlear or nerve) - Inner ear or auditory nerve
**Mixed**: (conductive + sensorineural)

---

## CONDUCTIVE HEARING LOSS

**Causes**:

**External Ear**:
- **Wax**: (cerumen impaction)
- **Foreign body**
- **Otitis externa**: (canal edema)

**Middle Ear**:
- **Otitis media with effusion** ("glue ear")
- **Perforated tympanic membrane**
- **Otosclerosis**: (stapes fixation, hereditary)
- **Cholesteatoma**: (skin growth in middle ear, destructive)
- **Tympanosclerosis**: (calcification of tympanic membrane)

---

**Clinical Features**:
- **Hearing loss**: (mild-moderate)
- **Weber test**: Lateralizes to affected ear (bone conduction better than air in diseased ear)
- **Rinne test**: BC > AC in affected ear (negative Rinne)

---

**Management**:

**Wax**:
- **Softening drops**: (olive oil, sodium bicarbonate 5% drops BID for 5 days)
- **Irrigation**: (if not contraindicated: perforation, previous ear surgery, otitis externa)
- **Microsuction**: (if irrigation contraindicated or failed)

**Otitis media with effusion**:
- *(See Otitis Media section)*
- **Observation** (3 months)
- **Grommets** (if persistent)

**Perforation**:
- **Dry**: (observation, avoid water entry)
- **Persistent**: (myringoplasty, surgical repair)

**Otosclerosis**:
- **Hearing aid**: (first-line)
- **Stapedectomy**: (surgical, if hearing aid inadequate)

**Cholesteatoma**:
- **Urgent ENT referral** (destructive, needs surgical removal)

---

## SENSORINEURAL HEARING LOSS

**Causes**:

**Congenital**:
- **Genetic**: (most common)
- **Congenital infections**: (rubella, CMV, toxoplasmosis)
- **Perinatal**: (birth asphyxia, jaundice, prematurity)

**Acquired**:
- **Noise-induced**: (occupational, recreational)
- **Age-related** (presbycusis): (most common)
- **Ototoxic drugs**: (gentamicin, furosemide, cisplatin)
- **Infections**: (meningitis, mumps, syphilis)
- **Trauma**: (head injury, temporal bone fracture)
- **Meniere's disease**: (endolymphatic hydrops)
- **Acoustic neuroma**: (vestibular schwannoma)

---

**Clinical Features**:
- **Hearing loss**: (often high-frequency initially)
- **Difficulty**: (understanding speech, especially in noisy environment)
- **Tinnitus**: (often)
- **Weber test**: Lateralizes to unaffected ear (better cochlear function)
- **Rinne test**: AC > BC in both ears (both positive, but decreased in affected ear)

---

## SUDDEN SENSORINEURAL HEARING LOSS (SSNHL)

**Definition**: ≥30 dB hearing loss in ≥3 frequencies over ≤72 hours

**Causes**:
- **Idiopathic**: (most common, 70%)
- **Viral**: (cochlear neuritis)
- **Vascular**: (ischemia, hemorrhage)
- **Autoimmune**
- **Perilymph fistula**: (membrane rupture)

**Clinical Features**:
- **Sudden**: (often unilateral)
- **Hearing loss**: (may be profound)
- **Tinnitus**: (90%)
- **Vertigo**: (30%)

**Management**:
- **Urgent ENT referral** (same day)
- **Oral steroids**: (prednisolone 1 mg/kg/day, taper over 10-14 days)
- **Intratympanic steroids**: (if oral contraindicated or failed)
- **Investigations**: (MRI internal auditory meatus to exclude acoustic neuroma)

---

## AGE-RELATED HEARING LOSS (PRESBYCUSIS)

**Gradual**, bilateral high-frequency loss

**Clinical Features**:
- **Onset**: >50 years (gradual)
- **High-frequency**: difficulty hearing consonants (f, s, th)
- **Speech**: difficulty in noisy environments
- **Tinnitus**: (common)

**Management**:
- **Hearing aids**: (primary treatment)
- **Assistive devices**: (amplified telephones, TV listeners)
- **Communication strategies**: (face speaker, reduce background noise)

---

## HEARING ASSESSMENT

**Primary Care**:
- **Whispered voice test**: (stand behind patient, whisper numbers, ask patient to repeat)
- **Tuning fork tests** (512 Hz):
  - **Weber test**: Place on vertex, ask where sound heard
  - **Rinne test**: Place on mastoid (BC), then near ear canal (AC), ask which is louder

**Audiology**:
- **Pure tone audiogram**: (hearing thresholds by frequency)
- **Tympanometry**: (middle ear pressure, mobility)
- **Speech audiometry**: (word recognition scores)

---

## HEARING AIDS

**Types**:
- **Behind-the-ear (BTE)**: (most common, suitable for all losses)
- **In-the-ear (ITE)**: (custom-molded, mild-moderate loss)
- **Completely-in-canal (CIC)**: (cosmetic, mild loss)
- **Bone conduction**: (conductive or mixed loss, cannot wear conventional hearing aid)

**Funding**:
- **NHS**: (available if hearing loss meets criteria)
- **Private**: (wider range of options)

---

## COCHLEAR IMPLANTS

**Indications**:
- **Severe-profound** sensorineural hearing loss
- **Inadequate benefit** from hearing aids
- **Children**: (early implantation for language development)

**Procedure**:
- **Surgical**: (implant electrode into cochlea)
- **Rehabilitation**: (auditory training, speech therapy)

---

## PREVENTION

**Noise-Induced Hearing Loss**:
- **Avoid** excessive noise exposure
- **Ear protection**: (earplugs, earmuffs for loud environments)
- **Reduce volume**: (personal audio devices)

**Ototoxic Drugs**:
- **Monitor** hearing if on ototoxic drugs
- **Avoid** if possible (gentamicin, high-dose loop diuretics, cisplatin)

---

## WHEN TO REFER

**Urgent**:
- **Sudden sensorineural hearing loss** (within 72 hours)
- **Cholesteatoma** (destructive, needs removal)

**Routine**:
- **Persistent hearing loss**: (>3 months)
- **Asymmetric hearing loss**: (unilateral)
- **Tinnitus with hearing loss**: (audiology assessment)
- **Occupational**: noise exposure (audiology)

---

**Sources: NICE NG98 Hearing Loss, ENT UK Hearing Loss Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ent",
                "focus": "hearing_loss",
                "sources": ["NICE NG98", "ENT UK Hearing Loss Guidelines", "CKS"]
            }
        )

    def _handle_tinnitus(self, query: str, context: dict) -> DomainQueryResult:
        """Handle tinnitus"""
        answer = """**TINNITUS**

---

## DEFINITION

**Perception of sound** in the absence of external sound stimulus

**"Ringing in the ears"** (but can be buzzing, humming, hissing, whistling, clicking)

---

## CLASSIFICATION

**Subjective**: (perceived only by patient, 99%)
**Objective**: (actually audible to examiner, rare, vascular or muscular)

---

## EPIDEMIOLOGY

**Prevalence**: 10-15% of adults
**Significant impact**: 1-2% (severe, affects quality of life, sleep, concentration)

---

## CAUSES

**Hearing Loss** (most common):
- **Age-related** (presbycusis)
- **Noise-induced** (occupational, recreational)
- **Conductive** (wax, otitis media)

**Ear Pathology**:
- **Meniere's disease** (tinnitus + vertigo + hearing loss + aural fullness)
- **Otosclerosis**
- **Eustachian tube dysfunction**

**Medications** (ototoxic):
- **Aspirin** (high dose, reversible)
- **Gentamicin**, other aminoglycosides
- **Furosemide**, other loop diuretics
- **Cisplatin** (chemotherapy)
- **Quinine**, chloroquine

**Neurological**:
- **Acoustic neuroma** (vestibular schwannoma)
- **Multiple sclerosis**
- **Head injury**

**Other**:
- **Temporomandibular joint** (TMJ) dysfunction
- **Cervical spine** disease
- **Depression**, anxiety (exacerbates)

**Idiopathic**: (most common)

---

## CLINICAL FEATURES

**Sound Characteristics**:
- **Type**: (ringing, buzzing, humming, hissing)
- **Pitch**: (high, low)
- **Location**: (unilateral, bilateral, "in the head")
- **Pulsatile**: (suggests vascular cause, objective tinnitus)

**Associated Symptoms**:
- **Hearing loss**: (often)
- **Hyperacusis**: (sensitivity to sound)
- **Vertigo**: (if Meniere's)
- **Anxiety**, depression, insomnia (consequences of tinnitus)

---

## ASSESSMENT

**History**:
- **Onset**: (sudden vs gradual)
- **Characteristics**: (pitch, location, continuous vs intermittent)
- **Aggravating/relieving factors**
- **Impact**: (sleep, concentration, quality of life)
- **Medications**: (review for ototoxic drugs)
- **Noise exposure**: (occupational, recreational)
- **Associated symptoms**: (hearing loss, vertigo, neurological symptoms)

**Examination**:
- **Ear examination**: (wax, perforation)
- **Auscultation**: (for objective tinnitus, bruits)
- **Neurological**: (cranial nerves, especially VIII)

**Investigations**:
- **Audiogram**: (hearing assessment)
- **Tympanometry**: (middle ear function)
- **MRI IAM**: (if unilateral tinnitus, asymmetric hearing loss, or neurological symptoms - to exclude acoustic neuroma)

---

## MANAGEMENT

**Reassurance**:
- **Common**: (affects many people)
- **Often improves**: (spontaneously over time)
- **Not serious**: (in most cases)

**Treat Underlying Cause**:
- **Wax removal**
- **Hearing aid**: (if hearing loss present)
- **Medication adjustment**: (stop ototoxic drugs if possible)
- **TMJ treatment**: (dental referral)

**Sound Therapy**:
- **Sound enrichment**: (background noise, white noise machines, environmental sounds)
- **Hearing aids**: (amplify external sounds, mask tinnitus)
- **Masking devices**: (tinnitus maskers, combination hearing aid/masker)

**Cognitive Behavioral Therapy (CBT)**:
- **Effective** for tinnitus-related distress
- **Focus**: (coping strategies, reduce impact)

**Tinnitus Retraining Therapy (TRT)**:
- **Combination**: (sound therapy + counseling)
- **Goal**: (habituation to tinnitus)

**Medications**:
- **No evidence** for drug treatment
- **Avoid**: (unnecessary medications)

**Lifestyle**:
- **Stress management**: (relaxation techniques)
- **Sleep hygiene**: (improve sleep quality)
- **Avoid**: (silence, focus on tinnitus)
- **Caffeine**, alcohol: (may exacerbate, reduce if identified trigger)

---

## PROGNOSIS

**Good**: (most improve with time)
**Persistent**: (some, but impact can be reduced with management)
**Severe**: (1-2%, significant impact on quality of life)

---

## RED FLAGS: URGENT REFERRAL

- **Unilateral tinnitus** with neurological symptoms (asymmetric hearing loss, vertigo, facial weakness)
- **Pulsatile tinnitus** (may indicate vascular abnormality)
- **Sudden onset** tinnitus with hearing loss (SSNHL, urgent)

---

## PREVENTION

**Noise-induced**:
- **Avoid** excessive noise exposure
- **Ear protection**: (earplugs for loud environments)
- **Reduce volume**: (personal audio devices)

**Ototoxic drugs**:
- **Monitor** if on ototoxic medications
- **Avoid** if possible

---

**Sources: NICE NG155 Tinnitus Assessment and Management, ENT UK Tinnitus Guidelines, Cochrane Reviews**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "ent",
                "focus": "tinnitus",
                "sources": ["NICE NG155", "ENT UK Tinnitus Guidelines", "Cochrane Reviews"]
            }
        )

    def _handle_vertigo(self, query: str, context: dict) -> DomainQueryResult:
        """Handle vertigo and dizziness"""
        answer = """**VERTIGO**

---

## DEFINITION

**Vertigo**: Illusion of movement (spinning, rotation)
**Dizziness**: Non-specific term (lightheadedness, unsteadiness, vertigo)

---

## DIFFERENTIAL DIAGNOSIS

### PERIPHERAL VERTIGO (Ear problem)

**Benign Paroxysmal Positional Vertigo (BPPV)**:
- **Most common** cause of vertigo
- **Positional**: Triggered by head position changes (rolling over in bed, looking up)
- **Duration**: Seconds to minutes
- **Nystagmus**: Fatigable, geotropic (towards undermost ear)
- **Hearing**: Normal
- **Treatment**: Epley maneuver (canalith repositioning)

**Vestibular Neuritis**:
- **Viral** inflammation of vestibular nerve
- **Severe vertigo**: Vomiting, bedridden
- **Duration**: Days to weeks
- **Hearing**: Normal
- **Treatment**: Vestibular sedatives (acute), vestibular rehabilitation (recovery)

**Labyrinthitis**:
- **Viral** inflammation of labyrinth (vestibular + cochlear nerve)
- **Vertigo + hearing loss**: (distinguishes from vestibular neuritis)
- **Treatment**: Vestibular sedatives, vestibular rehabilitation

**Meniere's Disease**:
- **Endolymphatic hydrops** (fluid imbalance)
- **Triad**: Episodic vertigo (hours), tinnitus, hearing loss, aural fullness
- **Duration**: Hours (vertigo)
- **Hearing**: Fluctuating, sensorineural (low-frequency initially)
- **Treatment**: Low-salt diet, diuretics, intratympanic steroids, gentamicin (ablative)

---

### CENTRAL VERTIGO (Brain problem)

**Vascular**:
- **Vertebrobasilar TIA**: (transient vertigo, diplopia, ataxia, dysarthria)
- **Posterior circulation stroke**: (cerebellar infarct - lateral medullary syndrome)

**Migraine**:
- **Vestibular migraine**: Vertigo with migraine symptoms, headache may or may not be present

**Multiple Sclerosis**:
- **Demyelination**: (brainstem plaques)

**Tumor**:
- **Acoustic neuroma**: (gradual hearing loss, imbalance rather than true vertigo)

---

## ASSESSMENT

**History**:
- **Duration**: (seconds/minutes vs hours vs days)
- **Triggers**: (positional, spontaneous)
- **Associated symptoms**: (hearing loss, tinnitus, aural fullness, headache, neurological symptoms)
- **Frequency**: (single episode vs recurrent)

**Examination**:
- **Otoscopic**: (wax, perforation)
- **Hearing assessment**: (whisper test)
- **Oculomotor**: (nystagmus, especially with Hallpike maneuver)
- **Neurological**: (cranial nerves, cerebellar signs, gait)

**Hallpike-Dix-Hallpike Maneuver**:
- **Diagnoses**: BPPV (posterior semicircular canal)
- **Procedure**:
  1. Patient seated, turn head 45° to tested side
  2. Rapidly lay back, head extended 30° below horizontal
  3. Observe for nystagmus (latency 5-20 sec, fatigable, geotropic)
  4. Hold until nystagmus resolves
  5. Return to seated
  6. Repeat for other side

---

## MANAGEMENT

### BPPV

**Epley Maneuver** (canalith repositioning):
1. Patient seated, turn head 45° to affected side
2. Rapidly lay back, head extended
3. Rotate head 90° to opposite side
4. Roll body onto side (head turned)
5. Sit up
6. Repeat 2-3 times

**Brandt-Daroff Exercises** (home exercises):
- Repeated positioning exercises 2-3 times daily

**Success**: 80-90% with Epley maneuver

---

### VESTIBULAR NEURITIS/LABYRINTHITIS

**Acute Phase** (first few days):
- **Vestibular sedatives**: (prochlorperazine, cinnarizine) for severe symptoms
- **Anti-emetics**: (if vomiting)
- **Bed rest**: (if severe)

**Recovery** (after acute phase):
- **Vestibular rehabilitation**: (exercises to promote compensation)
- **Avoid**: vestibular sedatives (delay compensation)

---

### MENIERE'S DISEASE

**Acute Attack**:
- **Vestibular sedatives**: (as above)
- **Anti-emetics**

**Prevention**:
- **Low-salt diet**: (<2g sodium daily)
- **Diuretics**: (bendroflumethiazide 2.5mg daily)
- **Intratympanic steroids**: (for refractory)
- **Intratympanic gentamicin**: (ablative, for severe, frequent attacks)

---

## RED FLAGS: URGENT REFERRAL

- **Central signs**: (diplopia, dysarthria, weakness, ataxia, severe headache)
- **"Worst headache of life"**: (subarachnoid hemorrhage)
- **Posterior circulation stroke**: (VERTIGO + other brainstem symptoms)
- **Progressive**: (worsening over weeks, tumor)

---

## INVESTIGATIONS

**Audiogram**: (hearing assessment)
**MRI Brain**: (if central features, asymmetric hearing loss, progressive)
**Caloric testing**: (ENG/videonystagmography, specialist)

---

## PROGNOSIS

**BPPV**: (excellent, Epley maneuver effective)
**Vestibular neuritis**: (good, vestibular rehabilitation promotes recovery)
**Meniere's**: (variable, progressive hearing loss, vertigo may remit)

---

## VESTIBULAR REHABILITATION

**Exercises** to promote central compensation:
- **Gaze stabilization**: (focus on object while moving head)
- **Balance training**: (standing, walking with head movements)
- **Habituation**: (repeated exposure to provoking movements)

**Specialist**: (physiotherapist referral)

---

**Sources: NICE NG240 Hearing Loss and Vestibular Conditions, ENT UK Vertigo Guidelines, Cochrane Reviews**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ent",
                "focus": "vertigo_dizziness",
                "sources": ["NICE NG240", "ENT UK Vertigo Guidelines", "Cochrane Reviews"]
            }
        )

    def _handle_sinusitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sinusitis"""
        answer = """**RHINOSINUSITIS (SINUSITIS)**

---

## DEFINITION

**Inflammation** of paranasal sinuses (almost always associated with rhinitis)

---

## CLASSIFICATION

**Acute**: (<4 weeks)
**Subacute**: (4-12 weeks)
**Chronic**: (>12 weeks)
**Recurrent acute**: (≥4 episodes per year, resolving completely between episodes)

---

## ANATOMY

**Sinuses**:
- **Maxillary**: (largest, below orbits)
- **Ethmoid**: (between eyes)
- **Frontal**: (above eyes)
- **Sphenoid**: (deep, center of skull)

**Drainage**: Ostia into nasal cavity (mucociliary clearance)

---

## ACUTE RHINOSINUSITIS

**Causes**:
- **Viral URTI**: (most common, 90%)
- **Bacterial**: (secondary, 10%)

**Viral**:
- **Rhinovirus**, coronavirus, influenza, parainfluenza

**Bacterial**:
- **Streptococcus pneumoniae**
- **Haemophilus influenzae**
- **Moraxella catarrhalis**

**Risk Factors**:
- **Smoking**
- **Allergic rhinitis**
- **Anatomical**: (deviated septum, nasal polyps)
- **Immune deficiency**: (HIV, immunoglobulin deficiency)
- **Cystic fibrosis**
- **Dental**: (maxillary sinusitis from dental infection)

---

**Clinical Features**:
- **Nasal obstruction**: (bilateral)
- **Discharge**: (purulent, yellow/green, may be postnasal)
- **Facial pain/pressure**: (cheeks, forehead, around eyes)
- **Reduced sense of smell**: (hyposmia/anosmia)
- **Fever**: (may be present, especially in bacterial)
- **Cough**: (often worse at night, postnasal drip)
- **Dental pain**: (maxillary sinusitis)

---

**Diagnosis**:
- **Clinical**: (symptoms above)
- **Duration**: (>10 days suggests bacterial)
- **Examination**:
  - **Anterior rhinoscopy**: (purulence, mucosal edema)
  - **Sinus tenderness**: (percussion over maxillary, frontal sinuses)

---

**Management**:

**Viral** (most common):
- **Supportive**: (analgesia for pain/fever - paracetamol, ibuprofen)
- **Irrigation**: (nasal saline washout)
- **Decongestants**: (topical xylometazoline 0.1% for maximum 5-7 days, oral pseudoephedrine)
- **Avoid**: antibiotics (ineffective, side effects)

**Bacterial** (suspected if):
- **Duration**: >10 days without improvement
- **Severe**: (high fever >39°C, purulent discharge, facial pain >3 days)
- **Double worsening**: (improving then worsening)

**Antibiotics** (first-line):
- **Amoxicillin**: 500mg TDS for 5 days (adult)
- **Alternative** (if penicillin allergy):
  - **Doxycycline**: 200mg day 1, then 100mg daily for 4 days
  - OR **Clarithromycin**: 500mg BD for 5 days

**Failure to respond** (after 7 days on antibiotic):
- **Second-line**: Co-amoxiclav 625mg TDS for 5 days

---

## CHRONIC RHINOSINUSITIS

**Duration**: >12 weeks

**Causes**:
- **Persistent inflammation** (often non-infectious)
- **Nasal polyps**
- **Allergic fungal sinusitis**
- **Dental infection**
- **Anatomical abnormalities**

---

**Clinical Features**:
- **Nasal obstruction**: (persistent)
- **Discharge**: (mucopurulent, postnasal drip)
- **Facial pressure/pain**: (often mild, chronic)
- **Reduced smell**: (hyposmia/anosmia)
- **Cough**: (chronic, postnasal drip)
- **Systemic features**: (absent, distinguishes from acute)

---

**Management**:

**Nasal Irrigation**:
- **Saline washout**: (isotonic or hypertonic saline, once daily)

**Intranasal Corticosteroids**:
- **Mometasone 50mcg**: 2 sprays each nostril OD
- **Fluticasone 50mcg**: 2 sprays each nostril OD
- **Duration**: (minimum 8-12 weeks)

**Systemic Corticosteroids** (short course):
- **Prednisolone**: 30-40mg daily for 5-14 days (if nasal polyps, severe symptoms)

**Antibiotics** (if acute exacerbation):
- **As for acute sinusitis**

**Surgical Referral** (if medical management inadequate):
- **Endoscopic sinus surgery**: (improve drainage, remove polyps)

---

## COMPLICATIONS

**Orbital** (most common):
- **Preseptal cellulitis**
- **Orbital cellulitis**: (proptosis, ophthalmoplegia, visual loss)
- **Orbital abscess**: (surgical drainage)

**Intracranial** (rare, serious):
- **Meningitis**
- **Epidural abscess**
- **Subdural empyema**
- **Brain abscess**
- **Cavernous sinus thrombosis**

**Chronic**:
- **Mucocele**: (mucus retention cyst, expansile)

---

## RED FLAGS: URGENT REFERRAL

- **Severe headache**, eye swelling, visual changes (orbital/intracranial complications)
- **Altered mental status** (intracranial extension)
- **Periorbital cellulitis** (proptosis, ophthalmoplegia - orbital cellulitis)
- **Severe facial pain**, neurological signs

---

## PREVENTION

- **Smoking cessation**
- **Allergic rhinitis**: (treat with intranasal steroids, antihistamines)
- **Nasal irrigation**: (during URTI)
- **Manage GERD**: (if relevant)

---

## WHEN TO REFER

**Urgent**:
- **Complications**: (orbital, intracranial)
- **Severe symptoms**: (not responding to antibiotics)

**Routine**:
- **Chronic rhinosinusitis**: (>12 weeks, failed medical management)
- **Recurrent acute sinusitis**: (≥4 episodes per year)
- **Nasal polyps**: (visible on anterior rhinoscopy)
- **Immunocompromise**: (HIV, immunodeficiency)

---

**Sources: NICE NG151 Sinusitis, ENT UK Sinusitis Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ent",
                "focus": "sinusitis",
                "sources": ["NICE NG151", "ENT UK Sinusitis Guidelines", "CKS"]
            }
        )

    def _handle_epistaxis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle nosebleeds (epistaxis)"""
        answer = """**NOSEBLEED (EPISTAXIS)**

---

## CLASSIFICATION

**Anterior** (90%): Kiesselbach's plexus (Little's area) - anterior nasal septum
**Posterior** (10%): Woodruff's plexus - posterior nasal cavity (more common in elderly)

---

## CAUSES

**Local**:
- **Trauma**: (nose picking, blow to nose)
- **Dry air**: (central heating, air conditioning)
- **Nasal surgery**: (previous septoplasty, turbinectomy)
- **Deviated septum**: (airflow turbulence)
- **Foreign body**: (children)
- **Nasal sprays**: (overuse, incorrect technique)
- **Tumors**: (rare, juvenile nasopharyngeal angiofibroma - adolescent males, malignancy)

**Systemic**:
- **Hypertension**: (very common)
- **Bleeding disorders**: (hemophilia, von Willebrand disease)
- **Anticoagulation**: (warfarin, DOACs, antiplatelets)
- **Liver disease**: (coagulopathy)
- **Renal failure**: (platelet dysfunction)
- **Alcohol**: (vasodilation)
- **Pregnancy**: (vascular changes)

**Idiopathic**: (most common)

---

## ASSESSMENT

**ABC**: Airway, Breathing, Circulation (if severe)

**History**:
- **Side**: (which nostril)
- **Duration**: (how long bleeding)
- **Amount**: (estimate, cups, soaked towels)
- **Bleeding elsewhere**: (gums, bruising, melena)
- **Medications**: (anticoagulants, antiplatelets)
- **Family history**: (bleeding disorders)
- **Trauma**: (recent, nose picking)

**Examination**:
- **Vital signs**: (BP, pulse, shock if severe)
- **Inspect**: (use headlight, nasal speculum if available)
- **Identify source**: (anterior vs posterior)

---

## MANAGEMENT

### FIRST AID

**For patient**:
1. **Sit forward** (do NOT lean back - risk of swallowing blood)
2. **Pinch soft part** of nose (just below bony bridge) for 10-15 minutes continuously
3. **Apply ice** to bridge of nose (vasoconstriction)
4. **Spit out** blood (do NOT swallow - causes nausea, vomiting)
5. **Avoid blowing nose** for several hours after bleeding stops

**DO NOT**:
- Lean back (blood swallowed)
- Blow nose (dislodges clot)
- Remove clot prematurely

---

### PRIMARY CARE MANAGEMENT

**Anterior Epistaxis** (bleeding point visible):

**Cautery** (if bleeding point visible):
- **Silver nitrate**: (chemical cautery)
  - Apply to bleeding point (caution: avoid septal both sides - risk of septal perforation)
- **Equipment**: (headlight, nasal speculum, suction)

**Nasal Packing** (if cautery unsuccessful or bleeding point not visible):

**Merocel** (expandable sponge):
- **Insert**: (along floor of nasal cavity)
- **Moisten**: (with water or saline to expand)
- **Remove**: (after 24-48 hours)

**Rapid Rhino** (inflatable balloon):
- **Insert**: (along floor of nasal cavity)
- **Inflate**: (with air to appropriate volume)
- **Remove**: (after 24-48 hours)

**Antibiotic prophylaxis**:
- **Co-amoxiclav 625mg TDS**: (while packing in place, prevent toxic shock syndrome)
- OR **Doxycycline 100mg OD** (if penicillin allergy)

**Posterior Packing** (if anterior packing unsuccessful):
- **Specialist procedure** (requires ENT referral)
- **Foley catheter**, **posterior nasal balloon**
- **Admission**: (for airway observation)

---

### SECONDARY MANAGEMENT

**Identify and treat cause**:
- **Control hypertension**: (if elevated)
- **Correct coagulopathy**: (warfarin reversal if major bleed)
- **Treat infection**: (if present)

**Investigations**:
- **FBC**: (anemia, thrombocytopenia)
- **Coagulation screen**: (INR, APTT)
- **U&E**: (renal failure)
- **LFTs**: (liver disease)
- **Nasal endoscopy**: (if recurrent, identify source or tumor)

---

### ONGOING BLEEDING

**If bleeding persists** despite packing:
- **Urgent ENT referral**
- **Surgical options**:
  - **Endoscopic arterial ligation**: (sphenopalatine artery)
  - **Embolization**: (interventional radiology)

---

## PREVENTION

**Nasal Care**:
- **Keep moist**: (Vaseline, saline sprays)
- **Avoid trauma**: (no nose picking, gentle blowing)
- **Humidify**: (especially in dry environments)

**Vasoconstrictor**:
- **Xylometazoline 0.1%**: (nasal spray, avoid >5-7 days)

**Cautery**:
- **Silver nitrate**: (prophylactic for recurrent epistaxis)

---

## RED FLAGS: URGENT REFERRAL

- **Hemodynamic instability**: (shock, tachycardia, hypotension)
- **Uncontrolled bleeding**: (despite packing)
- **Posterior epistaxis**: (requires specialist packing)
- **Recurrent**: (especially unilateral, consider tumor)
- **Bleeding disorders**: (uncontrolled)
- **Anticoagulated**: (with major bleed)

---

## WHEN TO REFER

**Urgent**:
- **Uncontrolled bleeding**: (despite packing)
- **Hemodynamic compromise**
- **Posterior epistaxis**

**Routine**:
- **Recurrent epistaxis**: (not responding to first aid, cautery)
- **Unexplained**: (especially unilateral, nasal obstruction)
- **Suspicion of tumor**: (adolescent male, nasal mass, discharge)
- **Bleeding disorder**: (for investigation)

---

## PATIENT ADVICE

**For future episodes**:
- **Sit forward**, pinch nose (10-15 min)
- **Ice** to bridge
- **Seek medical help** if:
  - Bleeding >20 minutes
  - Feeling faint, dizzy
  - Large amount of blood
  - Recurrent bleeding

**Prevention**:
- **Keep nose moist** (Vaseline, saline spray)
- **Avoid picking**
- **Gentle blowing**
- **Humidifier**: (in dry environments)
- **Control hypertension** (if applicable)

---

**Sources: NICE Epistaxis Guidelines, ENT UK Epistaxis Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "ent",
                "focus": "epistaxis",
                "sources": ["NICE Epistaxis Guidelines", "ENT UK Epistaxis Guidelines", "CKS"]
            }
        )

    def _handle_nasal_polyps(self, query: str, context: dict) -> DomainQueryResult:
        """Handle nasal polyps"""
        answer = """**NASAL POLYPS**

---

## DEFINITION

**Benign edematous** projections of nasal mucosa

---

## CAUSES

**Chronic rhinosinusitis** with nasal polyposis (CRSwNP): (most common)
- **Chronic inflammation** (eosinophilic, Th2-mediated)
- **Asthma**: (especially aspirin-exacerbated respiratory disease - AERD)
- **Allergic fungal sinusitis**: (rare)
- **Cystic fibrosis**: (children)

**Genetic**: (cystic fibrosis, primary ciliary dyskinesia)

---

## CLINICAL FEATURES

**Symptoms**:
- **Nasal obstruction**: (bilateral, progressive)
- **Reduced smell**: (hyposmia/anosmia - common)
- **Rhinorrhea**: (clear or mucopurulent, postnasal drip)
- **Facial pressure/pain**: (less common than chronic sinusitis)
- **Mouth breathing**: (especially at night)
- **Snoring**: (due to nasal obstruction)

**Signs**:
- **Visible polyps**: (on anterior rhinoscopy, grey, grape-like)
- **Bilateral**: (usually)
- **Multiple**: (usually)

---

## DIAGNOSIS

**Clinical**: (visible on examination)

**Nasal Endoscopy**: (confirms diagnosis, assesses extent)

**CT Sinuses**: (if surgery considered, assesses extent, bony anatomy)

---

## MANAGEMENT

### MEDICAL (first-line)

**Intranasal Corticosteroids** (mainstay):
- **Mometasone 50mcg**: 2 sprays each nostril OD
- **Fluticasone 50mcg**: 2 sprays each nostril OD
- **Duration**: (minimum 8-12 weeks to assess response)
- **Side effects**: (epistaxis, nasal dryness)

**Systemic Corticosteroids** (short course):
- **Prednisolone**: 30-40mg daily for 5-14 days
- **Indications**: (severe symptoms, short-term reduction before surgery)
- **Side effects**: (hyperglycemia, mood changes, insomnia - warn patient)

**Other**:
- **Nasal saline irrigation**: (adjunct)
- **Antileukotrienes**: (montelukast 10mg OD - if aspirin-exacerbated respiratory disease)
- **Doxycycline**: (100mg daily for 4-6 weeks - anti-inflammatory)

---

### SURGICAL (if medical management inadequate)

**Endoscopic Sinus Surgery** (ESS):
- **Polypectomy**: (remove polyps)
- **Functional endoscopic sinus surgery (FESS)**: (open sinuses, improve drainage)
- **Indications**: (obstructive symptoms, reduced smell, recurrent sinusitis)
- **Success**: (symptom improvement in 80-90%)
- **Recurrence**: (30-50% at 5 years, especially with AERD)

**Postoperative Care**:
- **Nasal irrigation**: (saline washout)
- **Intranasal corticosteroids**: (continue long-term)
- **Review**: (to assess healing, recurrence)

---

## ASPIRIN-EXACERBATED RESPIRATORY DISEASE (AERD)

**Samter's Triad**:
1. **Asthma**
2. **Nasal polyps**
3. **Aspirin sensitivity** (severe bronchospasm)

**Pathogenesis**: Cyclooxygenase-1 (COX-1) inhibition → leukotriene overproduction

**Management**:
- **Avoid aspirin**, NSAIDs (ibuprofen, naproxen)
- **Leukotriene receptor antagonist**: (montelukast)
- **Aspirin desensitization**: (specialist, if severe asthma refractory to other treatment)
- **Surgery**: (often needed, high recurrence)

---

## DIFFERENTIAL DIAGNOSIS

**Benign**:
- **Antrochoanal polyp**: (solitary, from maxillary sinus, children)
- **Inverted papilloma**: (locally aggressive, may transform to malignancy)
- **Hemangioma**, fibroma, neurofibroma

**Malignant**:
- **Squamous cell carcinoma** (most common sinonasal malignancy)
- **Adenocarcinoma**
- **Esthesioneuroblastoma** (olfactory neuroblastoma)
- **Lymphoma**, melanoma

---

## RED FLAGS: URGENT REFERRAL

- **Unilateral polyp**: (especially with bleeding, pain)
- **Facial pain**, swelling, paresthesia
- **Proptosis**, diplopia, visual loss (orbital extension)
- **Nasal obstruction with epiphora** (nasolacrimal duct obstruction)
- **Hard, ulcerated, bleeding lesion** (malignancy)

---

## PROGNOSIS

**Good**: (with appropriate treatment)
**Recurrence**: (30-50% at 5 years, higher with AERD, asthma)
**Medical**: (may need long-term intranasal corticosteroids)

---

## WHEN TO REFER

**Urgent**:
- **Red flags** above (unilateral, bleeding, pain, orbital symptoms)

**Routine**:
- **Visible polyps**: (not responding to intranasal corticosteroids)
- **Recurrent sinusitis**: (due to obstruction)
- **Reduced smell**: (affecting quality of life)
- **Surgical consideration**: (failed medical management)

---

**Sources: NICE NG151 Rhinosinusitis, ENT UK Nasal Polyps Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "ent",
                "focus": "nasal_polyps",
                "sources": ["NICE NG151", "ENT UK Nasal Polyps Guidelines", "CKS"]
            }
        )

    def _handle_rhinitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle rhinitis (allergic and non-allergic)"""
        answer = """**RHINITIS**

---

## DEFINITION

**Inflammation** of nasal mucosa resulting in rhinorrhea, congestion, sneezing, itching

---

## CLASSIFICATION

**Allergic Rhinitis**: (IgE-mediated)
**Infectious Rhinitis**: (viral, bacterial)
**Non-Allergic Rhinitis**: (vasomotor, hormonal, drug-induced)
**Atrophic Rhinitis**: (rare, elderly)

---

## ALLERGIC RHINITIS

**Types**:

**Seasonal** (Hay Fever, Pollinosis):
- **Pollens**: Tree (spring), Grass (summer), Weed (autumn)
- **Spores**: Molds (autumn)
- **Seasonal pattern**: (predictable)

**Perennial**:
- **House dust mite**: (Der p 1, Der f 1 - most common)
- **Pets**: (cat dander, dog dander)
- **Cockroaches**: (urban)
- **Occupational**: (laboratory animals, flour, wood dust)

---

**Clinical Features**:
- **Rhinorrhea**: (clear, watery)
- **Nasal congestion**: (obstruction)
- **Sneezing**: (paroxysms)
- **Nasal itching**: (palate, ears)
- **Conjunctivitis**: (itchy, red, watery eyes)
- **Postnasal drip**: (cough, throat clearing)
- **Snoring**: (due to nasal obstruction)

---

**Diagnosis**:
- **History**: (seasonal pattern, triggers, atopy)
- **Examination**: (pale, boggy turbinates, clear mucus)
- **Allergy testing**: (skin prick testing, specific IgE blood tests)

---

**Management**:

**Allergen Avoidance**:
- **Pollen**: (windows closed during pollen season, avoid outdoor activities during high pollen counts, shower after outdoor exposure)
- **Dust mite**: (impermeable bedding covers, hot wash bedding >60°C weekly, remove soft toys from bed, vacuum with HEPA filter)
- **Pets**: (remove from bedroom, home if possible, HEPA filter)

**Intranasal Corticosteroids** (first-line):
- **Mometasone 50mcg**: 2 sprays each nostril OD
- **Fluticasone 50mcg**: 2 sprays each nostril OD
- **Onset**: (12 hours, maximum effect days)
- **Duration**: (throughout pollen season, or long-term for perennial)

**Oral Antihistamines** (second-line or adjunct):
- **Cetirizine 10mg**: OD (may cause drowsiness)
- **Loratadine 10mg**: OD (less drowsy)
- **Fexofenadine 180mg**: OD (non-drowsy)
- **Acrivastine 8mg**: TID (rapid onset, prn)

**Intranasal Antihistamines**:
- **Azelastine 0.1%**: 1 spray each nostril BD (rapid onset, but bitter taste)

**Decongestants**:
- **Topical** (xylometazoline 0.1%): PRN, MAXIMUM 5-7 DAYS (risk of rhinitis medicamentosa with overuse)
- **Oral** (pseudoephedrine 60mg QDS): PRN, short-term (caution in hypertension)

**Mast Cell Stabilizers**:
- **Sodium cromoglicate 2%**: 1 spray each nostril QID (prophylactic, especially in children)
- **Nedocromil 1%**: BID-TID (more effective than cromoglicate)

**Leukotriene Receptor Antagonists**:
- **Montelukast 10mg**: OD (if asthma also present, or if antihistamines inadequate)

**Immunotherapy**:
- **Subcutaneous** (SCIT): (injections, specialist only)
- **Sublingual** (SLIT): (tablets, specialist)
- **Indications**: (severe symptoms, inadequate response to pharmacotherapy, confirmed IgE sensitization)

---

## NON-ALLERGIC RHINITIS

**Vasomotor (Idiopathic) Rhinitis**:
- **Triggers**: (temperature changes, humidity, spicy food, alcohol, emotion)
- **Symptoms**: (congestion, rhinorrhea, but no itching/sneezing)
- **Management**: (intranasal corticosteroids, antihistamines less effective)

**Hormonal Rhinitis**:
- **Pregnancy**: (estrogen-induced, usually resolves after delivery)
- **Hypothyroidism**, (acromegaly)
- **Contraceptive pill**

**Drug-Induced Rhinitis**:
- **Topical decongestants**: (overuse → rhinitis medicamentosa)
- **ACE inhibitors**: (cough, rhinorrhea)
- **Beta-blockers**, (aspirin, NSAIDs)
- **Management**: (stop offending drug if possible)

**Atrophic Rhinitis** (Ozena):
- **Rare**: (elderly, post-surgery)
- **Symptoms**: (crusting, foul odor, epistaxis)
- **Management**: (nasal irrigation, topical antibiotics)

---

## INFECTIOUS RHINITIS

**Viral** (most common):
- **Rhinovirus**, coronavirus, adenovirus, influenza, RSV
- **Management**: (supportive, analgesia, decongestants PRN)

**Bacterial** (rare):
- **Streptococcus pneumoniae**, *Staph aureus*
- **Management**: (antibiotics if persistent)

---

## COMPLICATIONS

**Sinusitis**: (acute, chronic)
**Otitis media**: (especially in children)
**Nasal polyps**: (especially with allergic rhinitis)
**Asthma**: (allergic rhinitis is risk factor)

---

## RED FLAGS: URGENT REFERRAL

- **Unilateral symptoms**: (especially with pain, bleeding)
- **Nasal mass**: (visible or palpable)
- **Facial pain**, swelling
- **Proptosis**, visual changes
- **Hard, ulcerated lesion**

---

## WHEN TO REFER

**Urgent**:
- **Red flags** above

**Routine**:
- **Severe symptoms**: (inadequate response to pharmacotherapy)
- **Allergy testing**: (to confirm allergens)
- **Immunotherapy**: (consideration)
- **Nasal polyps**: (suspected)
- **Surgery**: (septoplasty for deviated septum, turbinectomy)

---

**Sources: NICE NG231 Allergic Rhinitis, ENT UK Allergic Rhinitis Guidelines, BSACI Guidelines**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "ent",
                "focus": "rhinitis",
                "sources": ["NICE NG231", "ENT UK Allergic Rhinitis Guidelines", "BSACI Guidelines"]
            }
        )

    def _handle_sore_throat(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sore throat, tonsillitis, quinsy"""
        answer = """**SORE THROAT (PHARYNGITIS, TONSILLITIS)**

---

## DEFINITION

**Pain**, discomfort, or irritation in the throat

---

## DIFFERENTIAL DIAGNOSIS

**Viral Pharyngitis** (most common)
**Bacterial Pharyngitis/Tonsillitis**
**Glandular Fever** (Infectious Mononucleosis)
**Peritonsillar Abscess** (Quinsy)
**Other**: (Post-nasal drip, GERD, trauma, malignancy)

---

## ACUTE SORE THROAT

### VIRAL PHARYNGITIS (70-80%)

**Pathogens**:
- **Rhinovirus**, coronavirus, adenovirus, influenza, parainfluenza, Epstein-Barr virus, Coxsackievirus

**Clinical Features**:
- **Sore throat**: (gradual onset, less severe)
- **Coryza**: (nasal congestion, rhinorrhea)
- **Cough**: (common)
- **Hoarseness**: (laryngeal involvement)
- **Conjunctivitis**: (adenovirus)
- **Fever**: (low-grade or absent)
- **Exudate**: (uncommon or absent)

**Management**:
- **Supportive**: (analgesia - paracetamol, ibuprofen)
- **Salt water gargles**: (symptomatic relief)
- **Lozenges**: (benzydamine, chlorhexidine, lidocaine)
- **Antibiotics**: (ineffective, not indicated)

---

### BACTERIAL PHARYNGITIS/TONSILLITIS (20-30%)

**Pathogen**:
- **Group A β-hemolytic Streptococcus** (GABHS, *Streptococcus pyogenes*) - most common

**Clinical Features**:
- **Sore throat**: (sudden onset, severe)
- **Fever**: (>38°C)
- **Tonsillar exudate**: (white/yellow patches)
- **Tender anterior cervical lymphadenopathy**
- **Absence** of cough, coryza (Centor criteria)
- **Age**: 5-15 years (peak), rare <3 years

**Centor Criteria** (for GABHS):
- **Fever >38°C**: 1 point
- **Absence of cough**: 1 point
- **Tender anterior cervical lymphadenopathy**: 1 point
- **Tonsillar exudate**: 1 point
- **Age**: 3-14 years (+1), 15-44 years (0), ≥45 years (-1)

**Interpretation**:
- **Score 0-1**: No antibiotics (viral likely)
- **Score 2-3**: Consider antibiotics (or throat swab if available)
- **Score 4-5**: Antibiotics (GABHS likely)

**Management**:

**Antibiotics** (first-line):
- **Phenoxymethylpenicillin (Penicillin V)**: 500mg QDS (adult), 250mg QDS (child) for 10 days
- **Alternative** (if penicillin allergy):
  - **Clarithromycin**: 250-500mg BD for 5 days
  - OR **Erythromycin**: 250-500mg QDS for 5 days

**Benefits of Antibiotics**:
- **Reduce duration**: (by ~1 day if started within 3 days)
- **Prevent complications**: (peritonsillar abscess, rheumatic fever, glomerulonephritis)
- **Reduce transmission**

**Supportive**:
- **Analgesia**: (paracetamol, ibuprofen)
- **Rest**, fluids

---

### GLANDULAR FEVER (INFECTIOUS MONONUCLEOSIS)

**Pathogen**: Epstein-Barr virus (EBV)

**Age**: 15-25 years

**Clinical Features**:
- **Sore throat**: (severe, prolonged)
- **Fever**: (high)
- **Fatigue**: (pronounced, prolonged)
- **Lymphadenopathy**: (posterior cervical, generalized)
- **Splenomegaly**: (50%)
- **Hepatomegaly**: (10%)
- **Periorbital edema**: (especially children)
- **Rash**: (if given ampicillin/amoxicillin - "ampicillin rash")

**Diagnosis**:
- **FBC**: (lymphocytosis, atypical lymphocytes)
- **Monospot test**: (heterophile antibody, sensitive but not specific)
- **EBV serology**: (VCA IgM positive - acute infection)

**Management**:
- **Supportive**: (analgesia, rest, fluids)
- **Avoid**: contact sports (4-6 weeks) due to splenic rupture risk
- **Corticosteroids**: (if airway compromise, severe thrombocytopenia, hemolytic anemia)
- **Antibiotics**: (ineffective - viral, avoid ampicillin/amoxicillin - causes rash)

---

## PERITONSILLAR ABSCESS (QUINSY)

**Complication** of tonsillitis (spread of infection to peritonsillar space)

**Clinical Features**:
- **Severe sore throat**: (unilateral)
- **Fever**, malaise
- **Odynophagia**: (painful swallowing, difficulty swallowing, drooling)
- **Trismus**: (difficulty opening mouth due to pain and muscle spasm)
- **"Hot potato voice"**: (muffled speech)
- **Tonsil**: (displaced medially, deviated uvula to contralateral side)
- **Cervical lymphadenopathy**: (ipsilateral)

**Management**:
- **Urgent ENT referral** (same day)
- **Needle aspiration**: (diagnostic and therapeutic)
- **Incision and drainage**: (if aspiration fails, or recurrent)
- **Antibiotics**: (co-amoxiclav 625mg TDS or clindamycin 300mg QDS for 10 days)
- **Analgesia**: (IV, oral often not tolerated)
- **IV fluids**: (if dehydrated)
- **Admission**: (for drainage, observation)

---

## RECURRENT TONSILLITIS

**Definition**: ≥7 episodes in 1 year, ≥5 episodes/year for 2 years, or ≥3 episodes/year for 3 years

**Management**:
- **Tonsillectomy**: (consideration)
- **Indications** (NICE):
  - **Sore throats**: due to tonsillitis
  - **≥7 episodes** in last year OR ≥5 episodes/year for 2 years OR ≥3 episodes/year for 3 years
  - AND **Severe**: affecting quality of life, time off work/school
  - AND **Paradise criteria** met

**Paradise Criteria** (for tonsillectomy):
- **≥3 episodes** of tonsillitis in 1 year (documented by medical practitioner)
- **Tonsillar exudate**: +1 point
- **Temperature >38.5°C**: +1 point
- **Cervical lymphadenopathy**: +1 point
- **Positive culture for GABHS**: +1 point
- **Score ≥4**: Consider tonsillectomy

---

## DIFFERENTIAL DIAGNOSIS OF SORE THROAT

| Feature | Viral | Bacterial (GABHS) | Glandular Fever | Quinsy |
|---------|-------|-------------------|----------------|--------|
| Onset | Gradual | Sudden | Gradual | Sudden (worsening after tonsillitis) |
| Cough | Common | Absent | Uncommon | Uncommon |
| Coryza | Common | Absent | Common | Uncommon |
| Fever | Low/absent | High | High | High |
| Exudate | Uncommon | Common | Uncommon | May be obscured |
| Lymphadenopathy | Mild | Anterior | Posterior | Ipsilateral |
| Splenomegaly | Absent | Absent | Common | Absent |
| Trismus | Absent | Absent | Absent | Present |
| Unilateral | No | No | No | Yes |

---

## RED FLAGS: URGENT REFERRAL

- **Peritonsillar abscess**: (trismus, unilateral swelling, drooling, hot potato voice)
- **Airway obstruction**: (difficulty breathing, stridor)
- **Suspicion of malignancy**: (persistent sore throat >3 weeks, neck mass, hoarseness, dysphagia, weight loss, smoking/alcohol history)
- **Severe dehydration**: (unable to swallow fluids)

---

## WHEN TO REFER

**Urgent**:
- **Quinsy**: (same-day ENT referral)
- **Airway compromise**

**Routine**:
- **Recurrent tonsillitis**: (meeting tonsillectomy criteria)
- **Unexplained**: (persistent >3 weeks, especially with red flag symptoms)
- **Asymmetric tonsils**: (especially if enlargement, ulceration)

---

**Sources: NICE NG84 Sore Throat, ENT UK Tonsillitis Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ent",
                "focus": "sore_throat_tonsillitis",
                "sources": ["NICE NG84", "ENT UK Tonsillitis Guidelines", "CKS"]
            }
        )

    def _handle_hoarseness(self, query: str, context: dict) -> DomainQueryResult:
        """Handle hoarseness and voice disorders"""
        answer = """**HOARSENESS (DYSPHONIA)**

---

## DEFINITION

**Abnormal voice quality** (rough, raspy, strained, weak, breathy)

---

## ANATOMY

**Vocal cords** (true vocal folds) in larynx:
- **Vibration**: produces sound
- **Glottis**: space between vocal cords
- **Adduction**: (cords come together for phonation)

---

## CAUSES

**Acute** (onset days-weeks):
- **Acute laryngitis**: (viral URTI, vocal strain, overuse)
- **Allergic reaction**: (angioedema, anaphylaxis)
- **Trauma**: (intubation, vocal abuse)
- **Reflux**: (laryngopharyngeal reflux)

**Chronic** (onset >3 weeks):
- **Smoking**: (laryngeal irritation, malignancy risk)
- **Vocal cord nodules**: (singers, teachers - "singer's nodules")
- **Vocal cord polyps**: (vocal abuse, smoking)
- **Reinke's edema**: (smoking, reflux - "smoker's polyps")
- **Laryngopharyngeal reflux** (LPR)
- **Hypothyroidism**
- **Malignancy**: (laryngeal cancer, especially glottis)

**Neurological**:
- **Vocal cord paralysis**: (recurrent laryngeal nerve palsy - thyroid surgery, lung cancer, aortic aneurysm, idiopathic)
- **Myasthenia gravis**
- **Parkinson's disease**
- **Stroke** (bulbar palsy)

---

## ASSESSMENT

**History**:
- **Duration**: (acute vs chronic)
- **Voice use**: (overuse, occupation, singing)
- **Smoking**: (pack-years, current)
- **Alcohol**: (intake)
- **Reflux symptoms**: (heartburn, regurgitation)
- **Associated symptoms**: (dysphagia, odynophagia, throat pain, cough, hemoptysis, weight loss, neck mass)
- **Medical history**: (thyroid surgery, intubation, neurological disease)

**Examination**:
- **Voice quality**: (breathy, rough, strained, weak)
- **Neck**: (palpate for thyroid enlargement, lymphadenopathy)

---

## MANAGEMENT

### ACUTE LARYNGITIS

**Viral**: (most common)
- **Supportive**: (voice rest, humidification, hydration)
- **Avoid**: (smoking, alcohol, caffeine, vocal strain)
- **Analgesia**: (if discomfort)

**Bacterial**: (rare)
- **Antibiotics**: (if bacterial etiology suspected)

---

### VOCAL STRAIN NODULES, POLYPS

**Nodules**:
- **Bilateral**: (callus-like lesions)
- **Occupation**: (singers, teachers, actors)
- **Management**: (speech therapy, voice rest)

**Polyps**:
- **Unilateral**: (often)
- **Vocal abuse**, smoking
- **Management**: (speech therapy, surgical removal if persistent)

---

### LARYNGOPHARYNGEAL REFLUX (LPR)

**Reflux** into larynx, pharynx (without classic GERD symptoms)

**Symptoms**:
- **Hoarseness**: (especially morning)
- **Throat clearing**: (chronic)
- **Globus sensation**: (lump in throat)
- **Chronic cough**: (often)
- **Dysphagia**: (mild)

**Management**:
- **PPI**: (omeprazole 20mg OD or lansoprazole 15mg OD for 8-12 weeks)
- **Lifestyle**: (weight loss, avoid eating before bed, elevate head of bed, avoid alcohol, caffeine, spicy foods)

---

### VOCAL CORD PARALYSIS

**Causes**:
- **Surgical**: (thyroidectomy, carotid endarterectomy, cardiothoracic surgery)
- **Malignancy**: (lung cancer, thyroid cancer, esophageal cancer)
- **Neurological**: (stroke, myasthenia gravis)
- **Idiopathic**: (unknown)

**Symptoms**:
- **Breathy voice**: (incomplete glottic closure)
- **Aspiration**: (coughing with drinking)
- **Shortness of breath**: (if bilateral)

**Management**:
- **Investigate**: (CT chest, neck, CT with contrast - identify underlying cause)
- **Speech therapy**: (compensatory techniques)
- **Surgical**: (medialization thyroplasty, injection laryngoplasty)

---

## RED FLAGS: URGENT REFERRAL

- **Hoarseness >3 weeks**: (especially if >6 weeks)
- **Smoking history**: (especially >10 pack-years)
- **Alcohol excess**: (especially with smoking)
- **Associated symptoms**:
  - **Dysphagia**: (difficulty swallowing)
  - **Odynophagia**: (painful swallowing)
  - **Throat pain**: (persistent)
  - **Hemoptysis**: (coughing blood)
  - **Neck mass**: (palpable lymph node)
  - **Weight loss**: (unintentional)
  - **Otalgia**: (referred ear pain)
- **Previous head/neck irradiation**

---

## WHEN TO REFER

**Urgent** (2-week wait):
- **Persistent hoarseness** >3-4 weeks (especially with red flags)

**Routine**:
- **Hoarseness >6 weeks** (even without red flags)
- **Vocal cord nodules/polyps**: (for ENT assessment, speech therapy)
- **Vocal cord paralysis**: (for investigation, management)
- **LPR**: (if inadequate response to PPI, 8-12 weeks)

---

## INVESTIGATIONS (SPECIALIST)

**Laryngoscopy**:
- **Nasendoscopy**: (flexible fiberoptic laryngoscopy - office-based)
- **Microlaryngoscopy**: (direct laryngoscopy under anesthesia - biopsy, surgery)

**Stroboscopy**: (assess vocal cord vibration)

**Imaging**:
- **CT**: (neck, chest - if malignancy suspected)
- **MRI**: (larynx, if vocal cord paralysis)

---

## PREVENTION

**Vocal Hygiene**:
- **Hydration**: (drink plenty of water)
- **Avoid**: (smoking, alcohol, excessive caffeine)
- **Voice rest**: (if ill, after strain)
- **Avoid throat clearing**: (instead, swallow or sip water)
- **Steam inhalation**: (humidify, especially before voice use)
- **Warm up**: (before singing/prolonged voice use)

---

**Sources: NICE NG23 Hoarseness, ENT UK Hoarseness Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ent",
                "focus": "hoarseness_dysphonia",
                "sources": ["NICE NG23", "ENT UK Hoarseness Guidelines", "CKS"]
            }
        )

    def _handle_dysphagia(self, query: str, context: dict) -> DomainQueryResult:
        """Handle swallowing difficulties"""
        answer = """**DYSPHAGIA (DIFFICULTY SWALLOWING)**

---

## DEFINITION

**Subjective sensation** of difficulty passing food or liquid from mouth to stomach

---

## CLASSIFICATION

**Oropharyngeal**: (difficulty initiating swallow, coughing/choking during swallow)
**Esophageal**: (food "sticking", retrosternal)

---

## OROPHARYNGEAL DYSPHAGIA

**Causes**:

**Neurological**:
- **Stroke**: (bulbar, pseudobulbar palsy)
- **Parkinson's disease**
- **Motor neuron disease**
- **Multiple sclerosis**
- **Myasthenia gravis**
- **Myopathy**: (muscular dystrophy, polymyositis)

**Structural**:
- **Zenker's diverticulum**: (pharyngeal pouch)
- **Cricopharyngeal bar**: (upper esophageal sphincter dysfunction)
- **Tumors**: (oropharyngeal, laryngeal, esophageal)
- **Cervical osteophytes**: (Forestier's disease)

**Inflammatory**:
- **Achalasia**: (lower esophageal sphincter dysfunction, can cause upper symptoms)
- **Stricture**: (esophageal, after radiation, caustic ingestion)
- **Eosinophilic esophagitis**: (food impaction)

**Other**:
- **Foreign body**: (food bolus impaction)
- **Radiation**: (fibrosis after head/neck radiation)

---

**Symptoms**:
- **Nasal regurgitation**: (food/fluid comes out nose)
- **Coughing/choking**: (during or after swallow)
- **Wet voice**: (gurgly voice after swallow)
- **Recurrent chest infections**: (aspiration)
- **Weight loss**: (due to inadequate intake)
- **Prolonged mealtime**

---

## ESOPHAGEAL DYSPHAGIA

**Causes**:

**Motility**:
- **Achalasia**: (dilated esophagus, bird's beak tapering)
- **Diffuse esophageal spasm**: (corkscrew esophagus)
- **Scleroderma**: (esophageal dysmotility)

**Structural**:
- **Peptic stricture**: (GERD, chronic)
- **Esophageal cancer**: (progressive dysphagia, weight loss)
- **Extrinsic compression**: (lung cancer, mediastinal mass, enlarged left atrium, vascular ring)
- **Esophagitis**: (Candida, HSV, CMV in HIV, reflux)

**Other**:
- **Eosinophilic esophagitis**: (food impaction, dysphagia, young adults, atopy)

---

**Symptoms**:
- **Food sticking**: (localized, retrosternal)
- **Regurgitation**: (food, fluid)
- **Heartburn**: (if reflux-related)
- **Weight loss**: (if esophageal cancer, achalasia)

---

## ASSESSMENT

**History**:
- **Onset**: (sudden vs gradual)
- **Progression**: (intermittent vs progressive)
- **Solids vs liquids**: (solids first suggests structural, liquids too suggests motility)
- **Localization**: (where it feels stuck - may correlate with site of obstruction)
- **Pain**: (odynophagia suggests infection, malignancy)
- **Regurgitation**: (suggests obstruction or motility)
- **Associated symptoms**: (weight loss, heartburn, cough, neurological symptoms)

**Examination**:
- **General**: (nutrition, weight loss)
- **Neck**: (lymphadenopathy, thyroid)
- **Neurological**: (bulbar function, tongue, palate)

---

## RED FLAGS: URGENT REFERRAL (2-week wait)

- **Progressive dysphagia**: (worsening over time)
- **Solids then liquids**: (suggests structural narrowing)
- **Weight loss**: (unintentional)
- **Age >55** with new-onset dysphagia
- **Odynophagia**: (painful swallowing)
- **Vomiting**: (especially if blood-stained)
- **Neck mass**: (lymphadenopathy)
- **Iron deficiency anemia**: (with dysphagia - Plummer-Vinson syndrome, esophageal web)
- **History of head/neck cancer**, alcohol, smoking (esophageal cancer risk)

---

## MANAGEMENT

**Acute Dysphagia** (foreign body impaction):
- **Supportive**: (nothing by mouth, IV fluids if needed)
- **Urgent referral**: (for endoscopy, removal)

**Chronic Dysphagia**:
- **Refer**: (to gastroenterology, speech and language therapy)
- **Investigations**:
  - **Endoscopy**: (OGD, direct visualization, biopsy)
  - **Barium swallow**: (functional assessment, anatomical)
  - **Manometry**: (motility assessment)
  - **CT**: (if malignancy suspected)

**Speech and Language Therapy**:
- **Assessment**: (swallowing function)
- **Rehabilitation**: (swallowing techniques, compensatory strategies)
- **Diet modification**: (thickened fluids, texture modification)

---

## PREVENTION

**Choking Prevention**:
- **Eat slowly**, chew thoroughly
- **Avoid talking** while eating
- **Sit upright** during and after meals
- **Avoid alcohol** with meals (impairs swallowing)
- **Small bites**, alternate solids and liquids

**Aspiration Prevention**:
- **Sit upright** (90° angle)
- **Chin tuck**: (during swallow, protects airway)
- **Thickened fluids**: (if aspiration)
- **Small portions**, frequent meals

---

## SPECIFIC CONDITIONS

### ACHALASIA

**Esophageal motility disorder**: (lower esophageal sphincter fails to relax, esophageal aperistalsis)

**Symptoms**:
- **Dysphagia**: (solids and liquids)
- **Regurgitation**: (undigested food, especially at night)
- **Chest pain**: (esophageal spasm)
- **Weight loss**: (may be significant)

**Management**:
- **Pneumatic dilation**: (endoscopic balloon dilation of LES)
- **Surgical myotomy**: (Heller myotomy - laparoscopic)
- **Botulinum toxin**: (injection into LES - temporary, for poor surgical candidates)
- **Calcium channel blockers**, nitrates: (adjunct)

---

### ZENKER'S DIVERTICULUM

**Pharyngeal pouch**: (outpouching of pharyngeal mucosa)

**Symptoms**:
- **Dysphagia**: (intermittent)
- **Regurgitation**: (undigested food, often hours after meal)
- **Halitosis**: (bad breath from food decomposing in pouch)
- **Cough**: (especially at night, aspiration)
- **Gurgling**: (in neck)

**Management**:
- **Surgical**: (diverticulectomy, cricopharyngeal myotomy)
- **Endoscopic**: (endoscopic stapling - less invasive)

---

**Sources: NICE NG12 Dysphagia, ENT UK Dysphagia Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "ent",
                "focus": "dysphagia",
                "sources": ["NICE NG12", "ENT UK Dysphagia Guidelines", "CKS"]
            }
        )

    def _handle_globus(self, query: str, context: dict) -> DomainQueryResult:
        """Handle globus sensation (lump in throat)"""
        answer = """**GLOBUS PHARYNGEUS (LUMP IN THROAT)**

---

## DEFINITION

**Sensation of a lump** or foreign body in the throat, in the absence of dysphagia, odynophagia, or organic pathology

---

## CAUSES

**Gastroesophageal Reflux** (LPR): (most common)
- **Laryngopharyngeal reflux**: (acid/pepsin reflux into larynx/pharynx)

**Psychological**:
- **Anxiety**, stress, depression
- **Globus hystericus**: (historical term)

**Pharyngeal**:
- **Pharyngitis**: (post-viral, chronic)
- **Cricopharyngeal spasm**: (upper esophageal sphincter dysfunction)

**Cervical**:
- **Cervical spine disease**: (osteophytes, muscle tension)
- **Goiter**: (thyroid enlargement)

**Other**:
- **Post-nasal drip**: (allergic rhinitis, sinusitis)
- **Medications**: (ACE inhibitors - cough, throat irritation)
- **Dehydration**: (dry, scratchy throat)

---

## CLINICAL FEATURES

**Typical**:
- **Lump sensation**: (intermittent or constant)
- **Non-painful**: (usually)
- **Swallows**: (may improve temporarily with swallowing)
- **No dysphagia**: (swallowing normal)
- **No odynophagia**: (no pain on swallowing)
- **Worse**: (stress, anxiety, dry throat)

**Duration**:
- **Often chronic**: (months to years)

---

## ASSESSMENT

**History**:
- **Duration**: (acute vs chronic)
- **Swallowing**: (normal - distinguishes from dysphagia)
- **Pain**: (absent - distinguishes from odynophagia)
- **Reflux**: (heartburn, regurgitation, sour taste)
- **Allergies**: (post-nasal drip)
- **Stress**: (anxiety, life events)
- **Medications**: (ACE inhibitors)

**Examination**:
- **Neck**: (thyroid enlargement, lymphadenopathy)
- **Oropharynx**: (post-nasal drip, erythema)

---

## MANAGEMENT

**Reassurance**:
- **Benign**: (not serious)
- **Common**: (many people experience)

**Identify and treat cause**:

**Reflux** (LPR):
- **PPI**: (omeprazole 20mg OD for 8-12 weeks)
- **Lifestyle**: (weight loss, avoid eating before bed, elevate head of bed)

**Allergic rhinitis/post-nasal drip**:
- **Intranasal corticosteroid**: (mometasone, fluticasone)
- **Antihistamine**: (cetirizine, loratadine)

**Dehydration**:
- **Hydration**: (drink plenty of water)
- **Steam inhalation**: (humidify, especially in winter)

**Anxiety/stress**:
- **Reassurance**: (stress, anxiety correlation)
- **Relaxation techniques**
- **Counselling/CBT**: (if severe)

**Stop** ACE inhibitors:
- **Switch**: (to alternative antihypertensive)

---

## RED FLAGS: URGENT REFERRAL

- **Dysphagia**: (difficulty swallowing)
- **Odynophagia**: (painful swallowing)
- **Neck mass**: (palpable lymph node, thyroid)
- **Weight loss**: (unintentional)
- **Hemoptysis**: (coughing blood)
- **Progressive**: (worsening symptoms)
- **Age >55**, smoking, alcohol (malignancy risk)

---

## WHEN TO REFER

**Urgent** (2-week wait):
- **Red flags** above (especially dysphagia, odynophagia, neck mass, weight loss)

**Routine**:
- **Persistent symptoms**: (>3 months despite treatment)
- **Uncertain diagnosis**

---

**Sources: NICE NG12, ENT UK Globus Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "ent",
                "focus": "globus_sensation",
                "sources": ["NICE NG12", "ENT UK Globus Guidelines", "CKS"]
            }
        )

    def _handle_neck_lump(self, query: str, context: dict) -> DomainQueryResult:
        """Handle neck lumps and lymphadenopathy"""
        answer = """**NECK LUMPS (CERVICAL LYMPHADENOPATHY)**

---

## CLASSIFICATION

**Congenital**: (branchial cleft cyst, thyroglossal duct cyst, cystic hygroma)
**Inflammatory**: (lymphadenitis, reactive)
**Malignant**: (lymphoma, metastatic carcinoma)
**Endocrine**: (thyroid nodule, parathyroid)
**Salivary**: (parotid, submandibular gland enlargement)

---

## ANATOMICAL LEVELS (American Academy of Otolaryngology - Head and Neck Surgery)

**Level I**: Submental, submandibular (submandibular gland, nodes)
**Level II**: Upper jugular (upper deep cervical nodes)
**Level III**: Middle jugular (middle deep cervical nodes)
**Level IV**: Lower jugular (lower deep cervical nodes)
**Level V**: Posterior triangle (spinal accessory nodes)
**Level VI**: Anterior compartment (pretracheal, prelaryngeal, paratracheal nodes)
**Level VII**: Superior mediastinal nodes

---

## COMMON CAUSES BY LEVEL

**Level I**:
- **Submandibular gland**: (sialolithiasis, tumor, infection)
- **Submental nodes**: (dental infection, infection of lower lip, floor of mouth, anterior tongue)

**Level II, III, IV**:
- **Metastatic squamous cell carcinoma**: (from oropharynx, larynx, hypopharynx)
- **Lymphoma**: (multiple, rubbery nodes)
- **Reactive lymphadenopathy**: (URTI, dental infection)

**Level V**:
- **Lymphoma**: (especially if supraclavicular - Virchow's node - gastric cancer)
- **Metastatic**: (nasopharyngeal carcinoma, thyroid)
- **Cystic hygroma**: (congenital)

**Level VI**:
- **Thyroid**: (goiter, nodule, carcinoma)
- **Parathyroid**: (adenoma)
- **Delphian node** (prelaryngeal): (thyroid, laryngeal pathology)

---

## ASSESSMENT

**History**:
- **Duration**: (acute vs chronic)
- **Painful** (infective/inflammatory) vs **painless** (malignancy)
- **Progression**: (increasing size, number)
- **Associated symptoms**: (fever, night sweats, weight loss, hoarseness, dysphagia)
- **Risk factors**: (smoking, alcohol, HPV, sexual history, TB exposure, recent travel, animal bites, HIV)
- **Medications**: (carbimazole, phenytoin - cause lymphadenopathy)

**Examination**:
- **Location**: (anatomical level)
- **Size**: (measure, <1cm, 1-2cm, >2cm)
- **Consistency**: (soft, rubbery, hard, fixed)
- **Tenderness**: (present vs absent)
- **Mobility**: (mobile vs fixed to underlying structures)
- **Overlying skin**: (erythema, warmth, sinus, ulceration)
- **Systemic**: (other lymph node groups, hepatosplenomegaly)

---

## SPECIFIC CAUSES

### REACTIVE LYMPHADENOPATHY

**Common**: (URTI, dental infection, skin infection)

**Clinical Features**:
- **Recent infection**: (history of URTI, dental abscess, skin infection)
- **Painful**, tender
- **Mobile**
- **Resolves**: (with treatment of infection)

**Management**:
- **Treat cause**: (antibiotics if bacterial)
- **Review**: (2-4 weeks)
- **Refer**: (if not resolved after 4-6 weeks)

---

### LYMPHOMA

**Hodgkin Lymphoma**:
- **Painless**, rubbery lymphadenopathy
- **Often cervical**, mediastinal
- **B symptoms**: (fever, night sweats, weight loss)
- **Age**: (bimodal: 20s, >60 years)
- **Alcohol-induced pain**: (in affected nodes - pathognomonic but rare)

**Non-Hodgkin Lymphoma**:
- **Painless**, rubbery nodes
- **Extra-nodal involvement**: (common)
- **B symptoms**: (if advanced)
- **Age**: (older, >60 years)

**Management**:
- **Urgent referral** (2-week wait)
- **Biopsy**: (excisional lymph node biopsy for diagnosis)
- **Staging**: (CT chest/abdomen/pelvis, PET-CT)
- **Treatment**: (chemotherapy, immunotherapy, radiotherapy)

---

### METASTATIC CARCINOMA

**Squamous Cell Carcinoma** (SCC):
- **Level II, III, IV** most common
- **Primary**: (oropharynx - tonsil, tongue base; larynx; hypopharynx)
- **Risk factors**: (smoking, alcohol, HPV)
- **Hard**, fixed, often painless

**Management**:
- **Urgent referral** (2-week wait)
- **Panendoscopy**: (examination under anesthesia to identify primary)
- **Biopsy**: (FNA, excisional)
- **Imaging**: (CT/MRI, PET-CT)
- **Treatment**: (surgery, radiotherapy, chemotherapy)

---

### THYROID

**Goiter/Multinodular Goiter**:
- **Level VI** (anterior compartment)
- **Moves with swallowing**
- **May be asymptomatic** or compressive (dysphagia, dyspnea, hoarseness)
- **Investigate**: (TSH, T4, ultrasound, FNA if suspicious)

**Thyroid Cancer**:
- **Solitary nodule**: (hard, fixed)
- **History**: (previous neck radiation)
- **Vocal cord paralysis**: (recurrent laryngeal nerve palsy)
- **Management**: (surgery, radioactive iodine)

---

### SALIVARY GLAND

**Parotid**:
- **Level I** (pre-auricular)
- **Pleomorphic adenoma**: (most common benign, mobile, slow-growing)
- **Warthin's tumor**: (bilateral, smokers)
- **Mucoepidermoid carcinoma**: (malignant, rapid growth, facial nerve involvement)
- **Management**: (superficial parotidectomy, facial nerve preservation)

**Submandibular**:
- **Level I** (submandibular)
- **Sialolithiasis**: (stone in duct - painful, especially with eating, swelling)
- **Tumor**: (benign/malignant)

---

### CONGENITAL

**Branchial Cleft Cyst**:
- **Level II** (upper neck, lateral)
- **Cystic**, fluctuant, mobile
- **Painful** if infected
- **Young adults**
- **Management**: (surgical excision if symptomatic)

**Thyroglossal Duct Cyst**:
- **Midline**, anterior neck (upper)
- **Moves with protrusion of tongue** (pathognomonic)
- **Infected**: (painful)
- **Management**: (Sistrunk procedure - excision of cyst with central hyoid bone to prevent recurrence)

**Cystic Hygroma**:
- **Level V** (posterior triangle)
- **Transilluminates** (cystic)
- **Infants**, children
- **Management**: (sclerotherapy, surgical excision)

---

### OTHER

**Tuberculous Lymphadenitis** (Scrofula):
- **Painless**, enlarging nodes
- **Matted**, fluctuant
- **Systemic TB symptoms**: (fever, night sweats, weight loss, cough)
- **Risk**: (immunosuppression, TB exposure)
- **Management**: (anti-tuberculous therapy)

**Kikuchi Disease**:
- **Cervical lymphadenitis**: (young Asian females)
- **Fever**, night sweats
- **Self-limiting** (weeks-months)
- **Diagnosis of exclusion** (biopsy needed)

---

## RED FLAGS: URGENT REFERRAL (2-week wait)

- **Age >40** with unexplained persistent neck lump
- **Unexplained persistent** neck lump >3 weeks (any age)
- **Hard**, fixed, painless lump
- **Ulceration**, bleeding of overlying skin
- **Associated symptoms**: (hoarseness, dysphagia, odynophagia, weight loss, night sweats)
- **Smoking**, alcohol history (malignancy risk)
- **Previous head/neck cancer**, radiation
- **Supraclavicular node** (Virchow's node - malignancy, especially gastric)

---

## WHEN TO REFER

**Urgent** (2-week wait):
- **Red flags** above (especially unexplained persistent lump >3 weeks, hard/fixed, associated symptoms)

**Routine**:
- **Persistent lymphadenopathy**: (>4-6 weeks despite treatment)
- **Suspected congenital**: (branchial cleft cyst, thyroglossal duct cyst)
- **Suspected salivary gland**: (parotid, submandibular)
- **Uncertain diagnosis**: (needs FNA, biopsy)

---

## INVESTIGATIONS (SPECIALIST)

**Fine Needle Aspiration (FNA)**:
- **First-line** investigation (for most neck lumps >1cm)
- **Diagnosis**: (benign vs malignant, cell type)
- **Limitations**: (cannot distinguish architecture, may need excisional biopsy for lymphoma)

**Imaging**:
- **Ultrasound**: (first-line, assesses characteristics, guides FNA)
- **CT**: (assesses extent, relationship to structures)
- **MRI**: (soft tissue characterization)
- **PET-CT**: (staging of malignancy)

**Bloods**:
- **FBC**, ESR/CRP: (infection, inflammation)
- **TB test**: (if risk)
- **HIV test**: (if risk)
- **Thyroid function**: (if thyroid)

---

**Sources: NICE NG12 Neck Lump, ENT UK Neck Lump Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ent",
                "focus": "neck_lump_lymphadenopathy",
                "sources": ["NICE NG12", "ENT UK Neck Lump Guidelines", "CKS"]
            }
        )

    def _handle_salivary_gland(self, query: str, context: dict) -> DomainQueryResult:
        """Handle salivary gland disorders"""
        answer = """**SALIVARY GLAND DISORDERS**

---

## ANATOMY

**Major Salivary Glands**:
- **Parotid**: (largest, anterior to ear, serous secretions)
- **Submandibular**: (submandibular triangle, mixed serous/mucous)
- **Sublingual**: (floor of mouth, mucous secretions)

**Minor Salivary Glands**: (scattered throughout oral cavity, pharynx)

---

## PAROTID GLAND DISORDERS

### ACUTE PAROTITIS

**Viral** (most common):
- **Mumps**: (paramyxovirus, unilateral or bilateral)
  - **Symptoms**: (painful swelling, fever, malaise)
  - **Complications**: (orchitis, oophoritis, meningitis, pancreatitis)
  - **Management**: (supportive, analgesia, isolation (exclude from school/work for 5 days from onset of swelling))

**Bacterial** (acute suppurative parotitis):
- **Staph aureus** (most common), *Streptococcus*
- **Risk factors**: (dehydration, post-operative, elderly, immunocompromised, duct obstruction)
- **Symptoms**: (painful swelling, erythema, purulent discharge from Stensen's duct)
- **Management**:
  - **Rehydration**
  - **Antibiotics**: (flucloxacillin 500mg QDS or clarithromycin if penicillin allergy)
  - **Sialagogues**: (sour sweets, lemon juice to promote flow)
  - **Warm compresses**
  - **Massage**

---

### CHRONIC PAROTITIS

**Recurrent**: (infections, sjogren's, sialolithiasis)
**Autoimmune**: (Sjogren's syndrome)
**Obstructive**: (calculi, strictures)

**Management**:
- **Hydration**, sialagogues, massage
- **Antibiotics**: (if acute exacerbation)
- **Sialendoscopy**: (removal of calculi, stricture dilation)
- **Surgery**: (superficial parotidectomy if refractory)

---

### PAROTID TUMORS

**Benign** (80%):
- **Pleomorphic adenoma** (mixed tumor): (most common, 60%)
  - **Mobile**, slow-growing, painless
  - **Risk**: (malignant transformation if long-standing)
  - **Management**: (superficial parotidectomy, facial nerve preservation)

- **Warthin's tumor**: (second most common, bilateral in 10%)
  - **Smokers**, males >60 years
  - **Cystic**, slow-growing
  - **Management**: (superficial parotidectomy)

**Malignant** (20%):
- **Mucoepidermoid carcinoma** (most common malignant)
- **Adenoid cystic carcinoma**: (perineural invasion, high recurrence)
- **Carcinoma ex pleomorphic adenoma**: (malignant transformation of pleomorphic adenoma)
- **Acinic cell carcinoma**
- **Undifferentiated carcinoma**

**Red Flags** (suggest malignancy):
- **Rapid growth**
- **Pain**, facial nerve involvement (facial palsy)
- **Fixed**, hard
- **Cervical lymphadenopathy**
- **Skin invasion**, ulceration

**Management**:
- **Urgent referral** (2-week wait if red flags)
- **CT/MRI**: (assess extent, relationship to facial nerve)
- **FNA**: (diagnosis)
- **Surgery**: (total parotidectomy, neck dissection if nodes involved)
- **Radiotherapy**: (adjuvant for high-grade, involved margins)

---

## SUBMANDIBULAR GLAND DISORDERS

### SIALOLITHIASIS (SALIVARY STONES)

**Calculi** in submandibular duct (Wharton's duct) or gland

**Risk factors**:
- **Dehydration**
- **Stasis**: (duct stenosis, sialadenitis)
- **Gout**, hypercalcemia

**Symptoms**:
- **Painful swelling**: (submandibular, especially with eating)
- **Colicky pain**: (during meals)
- **Obstruction**: (reduced salivary flow)
- **Infection**: (if secondary)

**Investigation**:
- **Palpation**: (feel for stone in floor of mouth along duct)
- **Imaging**: (OCG - oblique lateral radiograph, ultrasound, CT)

**Management**:
- **Conservative**: (hydration, sialagogues, massage, warm compresses, antibiotics if infected)
- **Stone removal** (if symptomatic):
  - **Transoral**: (if ductal stone, small)
  - **Sialendoscopy**: (endoscopic removal)
  - **Gland excision**: (if proximal stone, recurrent)

---

### SUBMANDIBULAR TUMORS

**Less common** than parotid tumors

**Benign** (50%):
- **Pleomorphic adenoma**

**Malignant** (50%):
- **Adenoid cystic carcinoma**
- **Mucoepidermoid carcinoma**

**Management**:
- **Excision**: (submandibular gland excision)
- **Neck dissection**: (if nodes involved)

---

## SJÖGREN'S SYNDROME

**Autoimmune** exocrinopathy (affects lacrimal, salivary glands)

**Primary**: (sicca symptoms only)
**Secondary**: (with other autoimmune disease - RA, SLE, scleroderma)

**Symptoms**:
- **Xerophthalmia** (dry eyes): (gritty, burning)
- **Xerostomia** (dry mouth): (difficulty swallowing, speaking, dental caries, oral candidiasis)
- **Salivary gland enlargement**: (parotid, bilateral)

**Diagnosis**:
- **Anti-Ro (SSA)**, **anti-La (SSB)** antibodies
- **Schirmer test**: (assess tear production)
- **Salivary gland biopsy**: (focus score)
- **Sialography**: (ductal changes)

**Management**:
- **Artificial tears**: (for dry eyes)
- **Saliva substitutes**, sugar-free gum
- **Dental hygiene**: (fluoride, regular dental review)
- **Systemic**: (pilocarpine for symptoms, hydroxychloroquine if systemic)

---

## RANULA

**Mucus retention cyst**, usually in floor of mouth (from sublingual gland)

**Types**:
- **Simple ranula**: (confined to floor of mouth)
- **Plunging ranula**: (extends beyond floor of mouth into neck)

**Management**:
- **Marsupialization**: (unroofing of cyst)
- **Excision**: (of sublingual gland if recurrent)

---

## WHEN TO REFER

**Urgent** (2-week wait):
- **Parotid/submandibular mass**: (especially if red flags - rapid growth, pain, facial nerve involvement, fixed, cervical nodes)
- **Unexplained salivary gland swelling**: (>3 weeks)

**Routine**:
- **Recurrent sialadenitis**: (for investigation)
- **Suspected sialolithiasis**: (for imaging, removal)
- **Suspected Sjogren's**: (for diagnosis, rheumatology)
- **Benign tumor**: (for surgical planning)

---

**Sources: NICE NG12, ENT UK Salivary Gland Guidelines, CKS**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "ent",
                "focus": "salivary_gland_disorders",
                "sources": ["NICE NG12", "ENT UK Salivary Gland Guidelines", "CKS"]
            }
        )

    def _handle_foreign_body(self, query: str, context: dict) -> DomainQueryResult:
        """Handle foreign bodies (ear, nose, throat)"""
        answer = """**FOREIGN BODIES (EAR, NOSE, THROAT)**

---

## FOREIGN BODIES IN EAR

**Common**:
- **Children**: (beads, toys, food)
- **Adults**: (cotton buds, insects, earplugs)

**Symptoms**:
- **Pain**, discomfort
- **Hearing loss** (if obstructing canal)
- **Discharge** (if irritated, infected)
- **Tinnitus**

**Management**:
- **DO NOT remove**: (if not easily accessible, risk of pushing deeper, perforation)
- **Urgent referral**: (to ENT for removal)
- **Removal methods**: (microsuction, instrumentation, irrigation - specialist only)

**Insect**:
- **Kill insect first**: (if alive - use mineral oil, olive oil drops)
- **Then refer** for removal

---

## FOREIGN BODIES IN NOSE

**Common**:
- **Children**: (beads, toys, food, paper)
- **Adults**: (less common, usually tissue, nasal spray)

**Symptoms**:
- **Unilateral nasal discharge**: (purulent, foul-smelling if long-standing)
- **Nasal obstruction**
- **Foul odor**
- **Epistaxis** (if mucosa eroded)

**Management**:
- **Do NOT attempt removal**: (unless easily visible anteriorly)
- **Child**: (if distressed, refer urgently)
- **Specialist removal**: (ENT, using suction, instrumentation, balloon catheter)

---

## FOREIGN BODIES IN THROAT (INGESTED)

**Common**:
- **Fish bones**, chicken bones
- **Food bolus** (meat, bread)
- **Dentures**, coins, toys (children)

**Symptoms**:
- **Foreign body sensation**: (throat, often localized)
- **Odynophagia**: (painful swallowing)
- **Dysphagia**: (difficulty swallowing)
- **Hypersalivation**: (inability to swallow saliva)
- **Cough**, choking

**Management**:

**Emergency** (if airway compromise, respiratory distress):
- **Call 999**, Heimlich maneuver (if choking)

**Stable**:
- **Assess ABC**: (airway, breathing, circulation)
- **Examination**: (oropharynx, may be visible)
- **Imaging**: (lateral neck X-ray - radioopaque foreign bodies)
- **Urgent referral**: (to ENT for endoscopic removal if:
  - **Complete dysphagia** (unable to swallow saliva)
  - **Respiratory distress**
  - **Foreign body visible** on X-ray
  - **High suspicion** (sharp object, battery))

**Discharged** (if no foreign body identified, swallowing normal):
- **Soft diet**, avoid sharp foods
- **Re-review**: (if persistent symptoms)
- **CXR**: (if foreign body may have been aspirated)

**Sharp objects** (fish bones, chicken bones):
- **Urgent ENT referral** (risk of perforation, abscess)

**Batteries** (button batteries):
- **EMERGENCY**: (corrosive, tissue necrosis)
- **Urgent removal**

---

## INHALED FOREIGN BODIES (ASPIRATION)

**Common**:
- **Children** (nuts, seeds, toys)
- **Adults** (less common - usually while eating)

**Symptoms**:
- **Choking**: (acute episode)
- **Cough**: (persistent)
- **Wheeze**: (unilateral)
- **Recurrent pneumonia**: (same location)
- **Breath sound asymmetry**: (reduced on affected side)

**Management**:
- **Choking**: (back blows, chest thrusts, Heimlich maneuver if necessary)
- **CXR**: (may show hyperinflation, mediastinal shift, atelectasis)
- **Urgent referral**: (to pediatric ENT for bronchoscopy)

---

## PREVENTION

**Children**:
- **Avoid small objects**: (until age 3 - choke test tube <3cm diameter)
- **Supervise eating**: (nuts, grapes, hot dogs - high choking risk)
- **Cut food**: (into small pieces)
- **Avoid**: (playing while eating)

**Adults**:
- **Cut food**: (especially meat, avoid talking while eating)
- **Avoid alcohol**: (excess with meals)
- **Chew thoroughly**

---

**Sources: NICE Clinical Knowledge Summaries, ENT UK Foreign Body Guidelines**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "ent",
                "focus": "foreign_bodies",
                "sources": ["NICE CKS", "ENT UK Foreign Body Guidelines"]
            }
        )

    def _handle_snoring_sleep_apnoea(self, query: str, context: dict) -> DomainQueryResult:
        """Handle snoring and obstructive sleep apnoea"""
        answer = """**SNORING AND OBSTRUCTIVE SLEEP APNOEA (OSA)**

---

## SNORING

**Definition**: Noise generated during sleep by vibration of soft tissues of upper airway

**Causes**:
- **Nasal obstruction**: (rhinitis, polyps, deviated septum)
- **Adenoids/tonsils**: (especially children)
- **Obesity**: (soft tissue deposition around airway)
- **Alcohol**, sedatives: (muscle relaxation)
- **Sleep position**: (supine worsens)
- **Anatomy**: (retrognathia, macroglossia)
- **Hypothyroidism**, pregnancy, smoking

---

## OBSTRUCTIVE SLEEP APNOEA (OSA)

**Definition**: Repetitive episodes of upper airway obstruction during sleep resulting in sleep disruption, hypoxia

**Epidemiology**:
- **Prevalence**: 2-4% of middle-aged adults
- **Risk increases**: with age, obesity

---

**Symptoms**:

**Daytime**:
- **Excessive daytime sleepiness** (EDS)
- **Morning headache**
- **Poor concentration**, memory
- **Irritability**, mood changes
- **Reduced libido**, erectile dysfunction

**Nighttime** (bed partner reports):
- **Loud snoring**: (worse in supine)
- **Apneic episodes**: (cessation of breathing >10 seconds)
- **Gasping**, choking arousals
- **Restless sleep**
- **Nocturia** (frequent urination)

**Complications**:
- **Hypertension**, cardiovascular disease, stroke
- **Metabolic syndrome**, diabetes
- **Cognitive impairment**, depression
- **Motor vehicle accidents** (sleepiness while driving)

---

**Risk Factors**:
- **Obesity**: (BMI >30, neck circumference >17 inches men, >16 inches women)
- **Age**: (>40 years)
- **Male**: (2-3x more common)
- **Anatomy**: (retrognathia, macroglossia, tonsillar hypertrophy)
- **Alcohol**, sedatives
- **Smoking**
- **Family history**

---

## ASSESSMENT

**Epworth Sleepiness Scale** (ESS):

**Question**: "How likely are you to doze off or fall asleep in the following situations?" (0 = never, 3 = high chance)

1. Sitting and reading
2. Watching TV
3. Sitting inactive in a public place (theater, meeting)
4. Passenger in a car for 1 hour without break
5. Lying down to rest in afternoon when circumstances permit
6. Sitting and talking to someone
7. Sitting quietly after lunch without alcohol
8. In a car, while stopped for a few minutes in traffic

**Interpretation**:
- **0-7**: Normal
- **8-9**: Mild sleepiness
- **10-15**: Moderate sleepiness
- **16-24**: Severe sleepiness

**Physical Examination**:
- **BMI**, neck circumference
- **Mouth**: (mallampati score, tonsil size, uvula size, jaw size)
- **Nasal patency**: (septum, polyps)
- **BP**: (hypertension)

**Investigations**:
- **Polysomnography** (gold standard): (overnight sleep study in lab)
  - **Apnea-Hypopnea Index (AHI)**: (number of apneas/hypopneas per hour)
  - **Normal**: AHI <5
  - **Mild OSA**: AHI 5-15
  - **Moderate OSA**: AHI 15-30
  - **Severe OSA**: AHI >30

- **Home Sleep Apnea Test** (HSAT): (limited channels, for uncomplicated moderate-severe suspected OSA)

---

## MANAGEMENT

**Conservative** (first-line):

**Weight Loss**:
- **Target**: (BMI <25, 10-15% weight loss)
- **Bariatric surgery**: (if BMI >40, or >35 with comorbidities)

**Positional Therapy**:
- **Avoid supine sleep**: (sleep on side, tennis ball technique, position alarms)
- **Effective** for positional OSA (worse in supine)

**Avoid**:
- **Alcohol**: (within 4 hours of bedtime)
- **Sedatives**: (especially benzodiazepines)
- **Smoking**: (cessation)

**Nasal**:
- **Treat nasal obstruction**: (rhinitis, polyps)

---

**Continuous Positive Airway Pressure (CPAP)** (gold standard):
- **Indications**: (moderate-severe OSA, or mild OSA with symptoms, especially EDS)
- **Mechanism**: (pneumatic splint to keep airway open)
- **Pressure**: (titrated during sleep study)
- **Compliance**: (aim for >4 hours/night, 70% nights)
- **Benefits**: (improves symptoms, BP, cardiovascular risk, QoL, reduces accidents)

**Alternatives to CPAP**:
- **Auto-CPAP**: (auto-adjusting pressure)
- **Bilevel**: (different inspiratory/expiratory pressures - for high CPAP pressures)
- **Humidification**: (if nasal dryness)

---

**Mandibular Advancement Devices (MAD)**:
- **Indication**: (mild-moderate OSA, primary snoring, CPAP refusal/intolerance)
- **Mechanism**: (advances mandible, enlarges airway)
- **Custom-made**: (dental referral)
- **Compliance**: (better than CPAP for some)

---

**Surgical** (if CPAP/MAD refused or intolerant, and anatomical abnormality):
- **Uvulopalatopharyngoplasty (UPPP)**: (removal of uvula, part of soft palate, tonsils - limited success)
- **Maxillomandibular advancement**: (advances jaws, enlarges airway - highly effective but major surgery)
- **Tracheostomy**: (last resort, severe OSA with life-threatening complications)
- **Nasal surgery**: (septoplasty, turbinectomy - if nasal obstruction contributing)
- **Hypoglossal nerve stimulation**: (implantable device - selective cases)

---

**Pharmacological**: (limited role)
- **Modafinil**: (for residual EDS despite CPAP - specialist only)

---

## DRIVING

**UK DVLA Regulations**:
- **OSA with excessive sleepiness** (EDS sufficient to impair driving):
  - **Must cease driving** until symptoms controlled (treatment effective)
  - **Must notify DVLA**
  - **Can resume driving** when symptoms controlled and confirmed by specialist

- **Driving while sleepy**: (criminal offense, risk to public)

---

## PEDIATRIC OSA

**Common cause**: (enlarged tonsils/adenoids)

**Symptoms**:
- **Loud snoring**
- **Observed apneas**
- **Restless sleep**
- **Enuresis** (bedwetting)
- **Behavioral problems**: (ADHD-like symptoms)
- **Poor growth**, failure to thrive

**Management**:
- **Adenotonsillectomy**: (first-line, effective)
- **CPAP**: (if adenotonsillectomy contraindicated or refused)

---

## WHEN TO REFER

**Urgent**:
- **Severe OSA**: (AHI >30, cardiovascular complications, severe EDS)
- **Driving**: (if sleepy while driving)
- **Respiratory failure**: (cor pulmonale, pulmonary hypertension)

**Routine**:
- **Suspected OSA**: (for sleep study, CPAP initiation)
- **Snoring**: (if causing social/relationship issues, or OSA suspected)
- **Surgical assessment**: (if CPAP intolerance, anatomical abnormality)

---

## PROGNOSIS

**Good** with treatment:
- **CPAP**: (symptom improvement, reduced cardiovascular risk)
- **Weight loss**: (may cure mild OSA)
- **Surgery**: (variable, highly selected cases)

**Untreated**:
- **Progressive**: (worsens with age, weight gain)
- **Complications**: (cardiovascular, metabolic, cognitive, increased mortality)

---

**Sources: NICE NG159 Obstructive Sleep Apnoea, ENT UK OSA Guidelines, OSA UK Alliance**
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ent",
                "focus": "snoring_sleep_apnoea",
                "sources": ["NICE NG159", "ENT UK OSA Guidelines", "OSA UK Alliance"]
            }
        )

    def _handle_general_ent(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general ENT consultation"""
        answer = """**GENERAL ENT (OTOLARYNGOLOGY) CONSULTATION**

ENT (Ear, Nose, and Throat) covers the diagnosis and management of head and neck conditions.

**Common Conditions Managed**:
- **Ear**: Earache, hearing loss, tinnitus, vertigo, discharge (otitis externa, otitis media)
- **Nose and Sinus**: Sinusitis, nasal polyps, nosebleeds, allergic rhinitis, nasal obstruction
- **Throat**: Sore throat, tonsillitis, hoarseness, difficulty swallowing, lump in throat
- **Neck**: Neck lumps, lymphadenopathy, salivary gland disorders
- **Emergency**: Stridor, airway obstruction, peritonsillar abscess (quinsy)
- **Other**: Snoring, obstructive sleep apnoea, foreign bodies, head and neck cancer

**Diagnostic Approaches**:
- **Otoscopy**: Examination of ear canal and tympanic membrane
- **Nasal examination**: Anterior rhinoscopy, nasal endoscopy
- **Throat examination**: Oropharynx, indirect laryngoscopy, nasendoscopy
- **Neck examination**: Palpation of lymph nodes, salivary glands, thyroid
- **Hearing assessment**: Tuning fork tests, audiometry
- **Investigations**: Nasopharyngolaryngoscopy (NPL), imaging, allergy testing

**When to Seek Urgent Review**:
- **Stridor or noisy breathing** (airway emergency)
- **Severe sore throat** with difficulty swallowing or breathing (quinsy)
- **Sudden hearing loss** (urgent)
- **Severe nosebleed** uncontrolled by first aid
- **Unexplained persistent hoarseness** >3-4 weeks (red flag for malignancy)
- **Neck lump** >3 weeks (red flag for malignancy)
- **Foreign body** ingestion or inhalation

**Sources**: ENT UK Guidelines, NICE ENT Guidelines, CKS
"""

        return DomainQueryResult(
            domain_name="ent",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "ent",
                "focus": "general_consultation",
                "sources": ["ENT UK Guidelines", "NICE ENT Guidelines", "CKS"]
            }
        )


def create_ent_domain():
    """Factory function to create ENT domain instance"""
    return ENTDomain()


# Domain registration
try:
    from gpdisc_core.domains.registry import DomainModuleRegistry
    DomainModuleRegistry.register(ENTDomain)
except ImportError:
    # Registry not available yet
    pass
