"""
GPDISC Ophthalmology Domain Module

This module provides ophthalmological consultation capabilities including:
- Red eye evaluation and differential diagnosis
- Vision assessment and visual acuity
- Eye pain and trauma evaluation
- Cataract assessment and management
- Glaucoma screening and management
- Diabetic eye screening
- Age-related macular degeneration
- Retinal vascular disorders
- Pediatric eye conditions
- Emergency ophthalmology

Evidence-based with guidelines from:
- Royal College of Ophthalmologists (RCOphth)
- NICE Ophthalmology Guidelines
- American Academy of Ophthalmology (AAO)
- UK Ophthalmology Guidelines
"""

from typing import Optional, Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class OphthalmologyDomain(BaseDomainModule):
    """
    Ophthalmology specialty domain for eye conditions and diseases.

    Covers comprehensive ophthalmological consultation including:
    - Red eye differential (conjunctivitis, scleritis, uveitis, glaucoma)
    - Visual disturbances and vision loss
    - Eye pain and headache
    - Cataract assessment and management
    - Glaucoma (open-angle, angle-closure)
    - Diabetic retinopathy screening and management
    - Age-related macular degeneration (wet and dry)
    - Retinal vascular disorders (retinal vein/artery occlusion)
    - Pediatric eye conditions (amblyopia, strabismus)
    - Ocular trauma and emergencies
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="ophthalmology",
            version="1.0.0",
            dependencies=[],
            description="Ophthalmology: Eye diseases, red eye, vision loss, cataract, glaucoma, retinal disorders",
            keywords=[
                "eye", "eyes", "ophthalmology", "ophthalmologist", "ocular",
                "red eye", "pink eye", "conjunctivitis", "sticky eye",
                "vision", "visual", "acuity", "blurred", "blurry", "vision loss",
                "cataract", "lens opacity", "cloudy vision",
                "glaucoma", "eye pressure", "intraocular pressure", "iop", "optic nerve",
                "diabetic", "diabetic retinopathy", "diabetic eye", "retinopathy",
                "macular", "macula", "amd", "age-related macular degeneration", "armd",
                "retinal", "retina", "detachment", "vein occlusion", "artery occlusion",
                "eye pain", "painful eye", "photophobia", "light sensitivity",
                "watery eye", "dry eye", "gritty", "itchy eye",
                "floaters", "flashes", "spots", "cobwebs",
                "double vision", "diplopia", "squint", "strabismus",
                "lazy eye", "amblyopia",
                "ptosis", "drooping eyelid",
                "eyelid", "stye", "chalazion", "blepharitis",
                "cornea", "corneal", "abrasion", "ulcer", "keratitis",
                "uveitis", "iritis", "uvea",
                "scleritis", "episcleritis",
                "conjunctiva", "conjunctival", "pterygium",
                "pupil", "anisocoria", "unequal pupils",
                "optic nerve", "optic neuritis", "papilledema",
                "eye trauma", "eye injury", "foreign body", "chemical eye",
                "contact lens", "contacts",
                "squint", "cross-eyed", "wall-eyed", "strabismus",
                "nystagmus", "eye twitch", "eyelid twitch",
                "blocked tear duct", "epiphora", "tear duct",
                "eye examination", "slit lamp", "fundoscopy", "ophthalmoscope",
                "visual field", "perimetry",
                "intraocular pressure", "tonometry", "gonioscopy",
                "fluorescein", "eye stain"
            ],
            capabilities=[
                "red_eye_diagnosis", "vision_assessment", "cataract_evaluation",
                "glaucoma_screening", "diabetic_retinopathy", "macular_degeneration",
                "retinal_disorders", "pediatric_ophthalmology", "ocular_emergencies"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Process ophthalmology queries with appropriate specialty routing"""
        query_lower = query.lower()

        # Emergencies - HIGHEST PRIORITY
        if any(term in query_lower for term in ["vision loss", "sudden vision", "acute vision", "blind", "can't see", "sudden blindness"]):
            return self._handle_vision_loss_emergency(query, context)

        # Red eye - COMMON PRESENTATION
        elif any(term in query_lower for term in ["red eye", "pink eye", "bloodshot eye", "eye red", "conjunctivitis"]):
            return self._handle_red_eye(query, context)

        # Eye pain
        elif any(term in query_lower for term in ["eye pain", "painful eye", "eye hurts", "ocular pain"]):
            return self._handle_eye_pain(query, context)

        # Visual disturbances
        elif any(term in query_lower for term in ["blurred", "blurry", "floaters", "flashes", "double vision", "diplopia", "distortion", "wavy"]):
            return self._handle_visual_disturbance(query, context)

        # Cataract
        elif any(term in query_lower for term in ["cataract", "cloudy lens", "lens opacity"]):
            return self._handle_cataract(query, context)

        # Glaucoma
        elif any(term in query_lower for term in ["glaucoma", "eye pressure", "intraocular pressure", "iop", "optic nerve damage"]):
            return self._handle_glaucoma(query, context)

        # Diabetic retinopathy
        elif any(term in query_lower for term in ["diabetic retinopathy", "diabetic eye", "retinopathy", "diabetes eye"]):
            return self._handle_diabetic_retinopathy(query, context)

        # Macular degeneration
        elif any(term in query_lower for term in ["macular", "amd", "age-related macular degeneration", "armd", "macula degeneration"]):
            return self._handle_macular_degeneration(query, context)

        # Retinal disorders
        elif any(term in query_lower for term in ["retinal", "retina", "retinal detachment", "retinal tear", "retinal vein", "retinal artery"]):
            return self._handle_retinal_disorders(query, context)

        # Dry eye / watery eye
        elif any(term in query_lower for term in ["dry eye", "watery eye", "gritty", "itchy eye", "burning eye", "tearing"]):
            return self._handle_dry_eye(query, context)

        # Eyelid disorders
        elif any(term in query_lower for term in ["stye", "chalazion", "blepharitis", "eyelid", "ptosis"]):
            return self._handle_eyelid_disorders(query, context)

        # Contact lens issues
        elif any(term in query_lower for term in ["contact lens", "contacts", "contact lense", "lenses"]):
            return self._handle_contact_lens(query, context)

        # Eye trauma
        elif any(term in query_lower for term in ["eye trauma", "eye injury", "foreign body", "chemical eye", "something in eye"]):
            return self._handle_ocular_trauma(query, context)

        # Pediatric ophthalmology
        elif any(term in query_lower for term in ["lazy eye", "amblyopia", "squint", "strabismus", "cross-eyed", "wall-eyed", "child eye", "baby eye"]):
            return self._handle_pediatric_ophthalmology(query, context)

        # General ophthalmology
        else:
            return self._handle_general_ophthalmology(query, context)

    def _handle_vision_loss_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """Handle sudden vision loss - URGENT"""
        answer = """**SUDDEN VISION LOSS - OCULAR EMERGENCY**

**⚠️ URGENT REFERRAL REQUIRED**

---

## IMMEDIATE ASSESSMENT

**Key Questions**:
1. **Unilateral or bilateral?**
2. **Duration?** (Transient vs persistent)
3. **Associated symptoms?** (Pain, flashes, floaters, trauma)
4. **Visual field affected?** (Central, peripheral, altitudinal)

---

## DIFFERENTIAL DIAGNOSIS BY PRESENTATION

### PAINLESS VISION LOSS

**Central Retinal Artery Occlusion (CRAO)**:
- **Sudden**, profound, painless vision loss (unilateral)
- **Afferent pupillary defect** (RAPD)
- **Retina**: White, edematous with **cherry-red spot** at fovea
- **Causes**: Embolus (carotid atherosclerosis, AF), thrombosis, giant cell arteritis
- **Management**: **EMERGENCY**, urgent ophthalmology review
  - Ocular massage, anterior chamber paracentesis (may dislodge embolus)
  - Treat underlying cause
  - **Prognosis**: Poor (permanent vision loss common)

**Central Retinal Vein Occlusion (CRVO)**:
- **Sudden**, painless vision loss (unilateral)
- **Retinal**: Dilated veins, retinal hemorrhages, **disc edema** ("blood and thunder" appearance)
- **Risk factors**: Hypertension, diabetes, glaucoma, hypercoagulable states
- **Management**: Urgent ophthalmology referral
  - Control risk factors
  - Anti-VEGF for macular edema

**Branch Retinal Artery/Vein Occlusion**:
- **Sectoral** vision loss corresponding to affected territory
- Similar management to central occlusions

**Vitreous Hemorrhage**:
- **Sudden**, painless vision loss (unilateral)
- **History**: Diabetes, trauma, retinal tear
- **Fundus**: Cannot visualize retina (obscured by blood)
- **Management**: Urgent ophthalmology referral

**Retinal Detachment**:
- **Flash of light**, followed by **"curtain" or "shadow"** progressing across vision
- **Floaters** (increased)
- **Myopia**, trauma, family history risk factors
- **Management**: **URGENT ophthalmology referral** (surgical repair required)

**Amaurosis Fugax**:
- **Transient** vision loss (minutes, like a "shade coming down")
- **Unilateral**, painless
- **Cause**: Temporary retinal ischemia (carotid embolus)
- **Management**: **Urgent vascular assessment** (stroke risk)

**Optic Neuritis**:
- **Subacute** vision loss (days to weeks), unilateral
- **Pain on eye movement** (characteristic)
- **Afferent pupillary defect**
- **Color vision**: Reduced red color perception
- **Association**: Multiple sclerosis (50%)
- **Management**: Urgent ophthalmology/neurology referral
  - MRI brain/orbits
  - IV steroids (if vision significantly reduced)

**Giant Cell Arteritis (Temporal Arteritis)**:
- **Elderly** (>50 years)
- **Transient** or persistent vision loss
- **May be painful** (scalp tenderness, jaw claudication)
- **Other**: Headache, scalp tenderness, polymyalgia rheumatica
- **Management**: **EMERGENCY**
  - **Immediate high-dose steroids**: Prednisolone 40-60mg daily (DO NOT DELAY for ESR)
  - **Temporal artery biopsy** (within 2 weeks of starting steroids)
  - **ESR/CRP**: Usually elevated (but may be normal)
  - **IF SUSPECTED, TREAT FIRST** (irreversible vision loss risk)

**Anterior Ischemic Optic Neuropathy (AION)**:
- **Sudden**, painless vision loss (unilateral)
- **Disc edema** (usually altitudinal field defect)
- **Causes**: Giant cell arteritis (arteritic AION), hypertension, diabetes (non-arteritic AION)

---

### PAINFUL VISION LOSS

**Acute Angle-Closure Glaucoma**:
- **Sudden**, severe eye pain, headache
- **Nausea**, vomiting
- **Blurred vision**, **halos** around lights
- **Eye**: Red, rock-hard, mid-dilated pupil
- **Management**: **EMERGENCY**
  - **IV acetazolamide 500mg**
  - Topical IOP-lowering (timolol, brimonidine, pilocarpine)
  - **Urgent laser iridotomy** (ophthalmology)

**Endophthalmitis**:
- **Severe vision loss**, eye pain
- **History**: Recent intraocular surgery (cataract, injection), trauma
- **Eye**: Red, hypopyon (white cells in anterior chamber)
- **Management**: **EMERGENCY**
  - **Urgent ophthalmology referral**
  - **Vitreous tap** + **intravitreal antibiotics** (vancomycin, ceftazidime)

**Keratitis** (Corneal Ulcer):
- **Pain**, photophobia, reduced vision
- **Red eye**, **corneal opacity**
- **Contact lens wearers**: *Pseudomonas* risk
- **Management**: **Urgent ophthalmology review**
  - Corneal scrape, culture
  - **Fortified antibiotics** (hourly)

**Scleritis**:
- **Severe**, boring eye pain (may radiate to face, head)
- **Tender** to palpation
- **Vision** may be reduced (if posterior)
- **Management**: Urgent ophthalmology referral (systemic investigation required)

---

### BILATERAL VISION LOSS

**Cortical Blindness**:
- **Bilateral** vision loss with **normal pupillary reflexes** and fundi
- **Cause**: Occipital lobe infarction, stroke
- **Management**: **Emergency neurology**

**Bilateral Retinal Detachment** (rare):
- **Trauma**, underlying retinal disease

**Bilateral Optic Neuropathy**:
- **Toxic**: Methanol, ethambutol, isoniazid
- **Nutritional**: B12 deficiency, tobacco-alcohol amblyopia
- **Compressive**: Pituitary adenoma

---

## RED FLAGS: IMMEDIATE REFERRAL

- **Sudden**, painless vision loss (CRAO, CRVO, retinal detachment)
- **Retinal detachment symptoms** (flashes, floaters, curtain/shadow)
- **Painful vision loss with red eye** (acute angle-closure glaucoma, endophthalmitis, keratitis)
- **Suspected giant cell arteritis** (elderly, headache, scalp tenderness)
- **Trauma** with vision loss
- **Chemical injury** (immediate irrigation required)

---

## EXAMINATION IN PRIMARY CARE

**Visual Acuity**:
- Snellen chart (pinhole if refractive error)
- Document baseline

**Pupils**:
- **RAPD** (relative afferent pupillary defect): Shine light in each eye, observe consensual response
- **Anisocoria** (unequal pupils)

**Intraocular Pressure**:
- If tonometer available (caution if corneal ulcer suspected)

**Fundoscopy**:
- Optic disc (color, swelling)
- Retina (hemorrhages, exudates, detachment)
- Vessels (arteriovenous nipping, attenuation)

---

**Sources: RCOphth Emergency Ophthalmology Guidelines, NICE NG224 Glaucoma, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.96,
            metadata={
                "specialty": "ophthalmology",
                "focus": "vision_loss_emergency",
                "urgency": "emergency",
                "sources": ["RCOphth Emergency Guidelines", "NICE NG224", "AAO Guidelines"]
            }
        )

    def _handle_red_eye(self, query: str, context: dict) -> DomainQueryResult:
        """Handle red eye evaluation and differential diagnosis"""
        answer = """**RED EYE - DIFFERENTIAL DIAGNOSIS**

---

## IMMEDIATE ASSESSMENT

**Key Features**:
1. **Vision affected?** (Urgent if yes)
2. **Painful or painless?**
3. **Unilateral or bilateral?**
4. **Discharge?** (Watery, purulent, sticky)
5. **Photophobia?**
6. **Contact lens use?**
7. **Trauma?**

---

## DIFFERENTIAL DIAGNOSIS

### CONJUNCTIVITIS (Most Common)

**Types**:

**1. Viral Conjunctivitis**:
- **Cause**: Adenovirus, others
- **Presentation**:
  - **Bilateral** (usually starts unilateral, becomes bilateral)
  - **Watery discharge**
  - **Red eyes**, foreign body sensation
  - **Preauricular lymphadenopathy** (pathognomonic)
  - **May have**: URTI symptoms, sore throat
- **Management**:
  - **Supportive**: Cold compresses, artificial tears
  - **Hygiene**: Hand washing, separate towels (highly contagious)
  - **Exclude**: From school/work until discharge resolves (usually 5-7 days)

**2. Bacterial Conjunctivitis**:
- **Cause**: *Staph aureus*, *Strep pneumoniae*, *H. influenzae*
- **Presentation**:
  - **Unilateral or bilateral**
  - **Purulent discharge** (sticky eyelids in morning)
  - **Red eyes**, mild discomfort
  - **No lymphadenopathy** (usually)
- **Management**:
  - **Topical antibiotic**: Chloramphenicol 0.5% drops QID (or fusidic acid 1% BID)
  - **Duration**: 5 days
  - **Hygiene**: As above

**3. Allergic Conjunctivitis**:
- **Cause**: Hay fever, allergens
- **Presentation**:
  - **Bilateral**, **itchy** eyes (key feature)
  - **Watery discharge**, stringy mucus
  - **Red eyes**, eyelid edema
  - **History**: Atopy, allergic rhinitis
- **Management**:
  - **Antihistamine**: Oral cetirizine 10mg daily OR loratadine 10mg daily
  - **Mast cell stabilizer**: Sodium cromoglicate 2% drops QID (preventive)
  - **Topical antihistamine**: Antazoline + xylometazoline (Otrivine-Antistin) PRN

---

### EPISCLERITIS

**Inflammation** of episclera (superficial to sclera)

**Presentation**:
- **Sectoral** or diffuse redness (localized or generalized)
- **Mild discomfort** (not severe pain)
- **No vision loss**
- **Tender** to palpation (unlike conjunctivitis)
- **May be**: Nodular (episcleritis nodule)

**Management**:
- **Self-limiting** (resolves in 1-3 weeks)
- **Artificial tears** for comfort
- **Oral NSAID**: Ibuprofen 400mg TDS (if discomfort significant)
- **Urgent referral** if recurrent or associated systemic disease (rule out scleritis)

---

### SCLERITIS

**Inflammation** of sclera (deeper, more serious)

**Presentation**:
- **Severe, boring pain** (radiates to face, head, may wake at night)
- **Tender** to palpation (often very tender)
- **Purple/violaceous hue** (due to deeper vascular congestion)
- **Vision** may be reduced (if posterior scleritis)
- **Association**: Systemic disease (rheumatoid arthritis, SLE, granulomatosis with polyangiitis, gout)

**Management**:
- **Urgent ophthalmology referral**
- **Investigate** underlying systemic disease (rheumatology referral)
- **Treatment**: Oral NSAID, systemic steroids, immunosuppressants (specialist)

---

### ACUTE ANTERIOR UVEITIS (Iritis)

**Inflammation** of anterior uvea (iris and ciliary body)

**Presentation**:
- **Unilateral** (usually)
- **Painful** (aching, tenderness)
- **Photophobia** (significant)
- **Red eye** (especially around cornea, "ciliary flush")
- **Miosis** (small pupil), **irregular pupil** (posterior synechiae)
- **Vision**: May be blurred
- **Association**: HLA-B27 (ankylosing spondylitis, reactive arthritis), sarcoidosis, TB, syphilis

**Management**:
- **Urgent ophthalmology referral** (same day)
- **Treatment**: Dilating drops (cyclopentolate 1%), topical steroid (prednisolone 0.5% drops QID)
- **Investigation** for underlying cause

---

### ACUTE ANGLE-CLOSURE GLAUCOMA

**EMERGENCY**

**Presentation**:
- **Sudden**, severe eye pain, headache
- **Nausea**, vomiting
- **Blurred vision**, **halos** around lights
- **Red eye** (often injected)
- **Mid-dilated**, oval pupil (semi-dilated)
- **Eye**: Rock-hard (increased IOP)
- **Risk factors**: Hypermetropia, elderly, female, family history

**Management**:
- **EMERGENCY ophthalmology referral**
- **Immediate**: IV acetazolamide 500mg PO
- **Topical**: Timolol 0.5% (if not contraindicated), brimonidine, pilocarpine 2% (after IOP reduced)
- **Definitive**: Laser iridotomy (ophthalmology)

---

### KERATITIS (Corneal Ulcer)

**Inflammation** of cornea

**Presentation**:
- **Pain** (often severe), photophobia
- **Red eye**
- **Reduced vision**
- **Corneal opacity/ulcer** (visible with slit lamp or careful examination)
- **Fluorescein staining**: Ulcer stains green

**Causes**:
- **Contact lens**: *Pseudomonas* (rapidly progressive, severe)
- **Herpes simplex virus**: Dendritic ulcer (branching lesions)
- **Bacterial**: *Staph aureus*, *Pseudomonas*, *Pneumococcus*
- **Fungal**: (trauma with vegetable matter)

**Management**:
- **Urgent ophthalmology referral** (same day)
- **STOP contact lenses** (if relevant)
- **Topical antibiotics**: Fortified (cefazolin 5% + gentamicin 1.5% hourly)
- **HSV**: Oral aciclovir 400mg 5x daily ± topical aciclovir

---

### SUBCONJUNCTIVAL HAEMORRHAGE

**Presentation**:
- **Asymptomatic**, red eye (sharply demarcated, bright red patch)
- **No pain**, no vision change
- **Patient notices** incidentally
- **May be**: Bilateral

**Causes**:
- **Spontaneous** (most common)
- **Trauma**, coughing, sneezing, straining
- **Hypertension**, bleeding disorder, anticoagulation

**Management**:
- **Reassurance** (benign, self-limiting)
- **Resolves** in 2-3 weeks
- **Investigate**: If recurrent (check BP, clotting, INR if on warfarin)

---

### DRY EYE (Keratoconjunctivitis Sicca)

**Presentation**:
- **Red eyes**, burning, gritty, foreign body sensation
- **Watery eyes** (paradoxical, due to reflex tearing)
- **Worse**: Reading, computer use, air conditioning, wind
- **Bilateral** (usually)
- **Symptoms > signs**

**Management**:
- **Artificial tears** QID (preservative-free if frequent use)
- **Lipid-based tears** for evaporative dry eye
- **Warm compresses**: For meibomian gland dysfunction
- **Lid hygiene**: For blepharitis
- **Punctal plugs**: Refractory cases (specialist)

---

## RED FLAGS: URGENT REFERRAL

- **Painful red eye** with **visual loss**
- **Contact lens wearers** with red eye (pseudomonas risk)
- **History of trauma** (foreign body, corneal abrasion, penetrating injury)
- **Corneal opacity/ulcer** visible
- **Severe photophobia** (uveitis)
- **Halos** with headache/nausea (acute angle-closure glaucoma)
- **Recurrent subconjunctival hemorrhage** (investigate cause)

---

## DIAGNOSTIC APPROACH

**History**: Onset, unilateral/bilateral, pain/discomfort, discharge, photophobia, vision changes, contact lens use, trauma, systemic disease

**Examination**:
- **Visual acuity**: (pinhole if decreased)
- **Pupils**: Shape, size, reaction
- **Intraocular pressure** (if available)
- **Fluorescein staining** (corneal ulcer, abrasion)
- **Slit lamp** (if available)

---

**Sources: RCOphth Red Eye Guidelines, NICE CKS, BMJ Best Practice Red Eye**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "ophthalmology",
                "focus": "red_eye",
                "sources": ["RCOphth Red Eye Guidelines", "NICE CKS", "BMJ Best Practice"]
            }
        )

    def _handle_eye_pain(self, query: str, context: dict) -> DomainQueryResult:
        """Handle eye pain evaluation"""
        answer = """**EYE PAIN - DIFFERENTIAL DIAGNOSIS**

---

## CLASSIFICATION BY LOCATION

### ANTERIOR EYE PAIN (Cornea, Conjunctiva, Anterior Chamber)

**Corneal Causes**:

**1. Corneal Abrasion**:
- **Foreign body** sensation, severe pain
- **Photophobia**, tearing, redness
- **History**: Trauma, contact lens use
- **Fluorescein**: Stains green (area of epithelial defect)
- **Management**:
  - **Remove foreign body** (if present)
  - **Topical antibiotic**: Chloramphenicol 0.5% QID (for 2-3 days) to prevent infection
  - **Review**: 24 hours (ensure healing)
  - **Contact lens wearers**: Urgent ophthalmology review (pseudomonas risk)

**2. Corneal Ulcer (Keratitis)**:
- Severe pain, photophobia, reduced vision
- **Visible corneal opacity/ulcer**
- **Fluorescein**: Stains
- **Management**: Urgent ophthalmology referral

**3. Foreign Body**:
- **Foreign body sensation**, pain, tearing
- **May be**: Visible on examination (everting eyelid)
- **Management**:
  - **Everting eyelids**: Look for foreign body
  - **Remove** (if easily accessible)
  - **Fluorescein**: After removal (check for abrasion)
  - **If unable to remove**: Urgent ophthalmology referral

**4. Photokeratitis** (Welder's flash, snow blindness):
- **History**: UV exposure (welding without protection, snow reflection)
- **Onset**: 6-12 hours after exposure
- **Symptoms**: Pain, photophobia, foreign body sensation, tearing
- **Bilateral** (usually)
- **Management**:
  - **Supportive**: Topical antibiotic (chloramphenicol), cycloplegic (cyclopentolate) for pain
  - **Padding**: May help (bilateral padding not recommended)
  - **Resolves**: 24-48 hours

---

**Conjunctival Causes**:

**1. Episcleritis**:
- **Mild discomfort**, tenderness
- **Sectoral or diffuse redness**
- **Self-limiting** (1-3 weeks)

**2. Scleritis**:
- **Severe**, boring pain (radiates)
- **Purple/violaceous hue**
- **Tender** to palpation
- **Urgent ophthalmology referral**

---

**Anterior Chamber Causes**:

**1. Acute Anterior Uveitis (Iritis)**:
- **Aching pain**, tenderness
- **Photophobia**, red eye
- **Miosis**, irregular pupil
- **Urgent ophthalmology referral**

**2. Endophthalmitis**:
- **Severe pain**, vision loss
- **History**: Recent intraocular surgery/injection
- **EMERGENCY ophthalmology referral**

---

### POSTERIOR EYE PAIN (Orbit, Retina, Optic Nerve)

**Orbital Causes**:

**1. Orbital Cellulitis**:
- **Painful**, swollen eyelid
- **Fever**, malaise
- **Proptosis**, ophthalmoplegia (eye movement limitation)
- **Vision** may be affected
- **Management**: **ADMIT for IV antibiotics** (CT orbit to rule out abscess)

**2. Orbital Inflammatory Syndrome** (Pseudotumor):
- **Painful**, proptosis, ophthalmoplegia
- **No infection**
- **Management**: Urgent ophthalmology referral (may need oral steroids)

**3. Thyroid Eye Disease (Graves' Ophthalmopathy)**:
- **Pain**, pressure sensation
- **Proptosis**, periorbital edema
- **Double vision** (from extraocular muscle involvement)
- **History**: Thyroid dysfunction (usually hyperthyroidism)
- **Management**: Ophthalmology ± endocrinology referral

---

**Optic Nerve Causes**:

**1. Optic Neuritis**:
- **Pain on eye movement** (characteristic)
- **Vision loss** (decreased acuity, color vision)
- **Afferent pupillary defect**
- **Management**: Urgent ophthalmology referral (MRI brain/orbits)

**2. Ischemic Optic Neuropathy**:
- **Anterior Ischemic Optic Neuropathy (AION)**:
  - **Painless** usually (but may have mild pain)
  - **Sudden vision loss**
  - **Disc edema**
  - **Causes**: Giant cell arteritis (arteritic), hypertension, diabetes (non-arteritic)

---

**Migraine**:
- **Unilateral**, throbbing headache
- **May have**: Visual aura (scintillating scotoma, fortification spectra)
- **Associated**: Nausea, photophobia, phonophobia
- **Management**: Standard migraine treatment

---

**Tension Headache**:
- **Bilateral**, band-like pressure
- **Associated**: Neck muscle tension
- **Eye examination**: Normal

---

## RED FLAGS: URGENT REFERRAL

- **Severe pain** with **vision loss**
- **Corneal ulcer** visible
- **Foreign body** unable to remove
- **Proptosis**, ophthalmoplegia (orbital cellulitis)
- **Pain on eye movement** with vision loss (optic neuritis)
- **Contact lens wearers** with pain (pseudomonas risk)
- **History of recent intraocular surgery** with pain (endophthalmitis)
- **Suspected giant cell arteritis** (elderly, headache, scalp tenderness, jaw claudication)

---

## PAIN CHARACTERISTICS

| Pain Type | Typical Cause | Features |
|-----------|--------------|----------|
| Foreign body sensation | Corneal abrasion, foreign body | Worse with blinking, tearing |
| Aching | Uveitis, scleritis | Worse with eye movement |
| Boring | Scleritis | Radiates, severe, nocturnal |
| Throbbing | Acute angle-closure glaucoma, migraine | Associated with nausea, headache |
| Pressure | Thyroid eye disease | Proptosis, double vision |

---

**Sources: RCOphth Eye Pain Guidelines, NICE CKS, BMJ Best Practice**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ophthalmology",
                "focus": "eye_pain",
                "sources": ["RCOphth Eye Pain Guidelines", "NICE CKS", "BMJ Best Practice"]
            }
        )

    def _handle_visual_disturbance(self, query: str, context: dict) -> DomainQueryResult:
        """Handle visual disturbances"""
        answer = """**VISUAL DISTURBANCES**

---

## FLOATERS AND FLASHES

**Floaters**:
- **"Spots", "cobwebs", "specks"** moving across visual field
- **Due to**: Vitreous condensation, degeneration
- **Normal aging**: Common, benign
- **Sudden increase**: May indicate vitreous detachment/retinal tear

**Flashes**:
- **"Lightning streaks", "flashing lights"** in peripheral vision
- **Due to**: Vitreous traction on retina
- **Retinal tear/detachment risk**: 15%

**Posterior Vitreous Detachment (PVD)**:
- **Symptoms**: Sudden onset floaters, flashes
- **Age**: >50 years (myopes earlier)
- **Risk**: 10-15% develop retinal tear
- **Management**: **Urgent ophthalmology referral** (same day) to rule out retinal tear/detachment

---

## BLURRED VISION

**Transient**:
- **Dry eye**: Artificial tears
- **Refractive change**: Review optician (especially if diabetic)
- **Medication side effects**: Anticholinergics, topiramate, etc.

**Persistent**:
- **Cataract**: Cloudy lens, gradual progression
- **Glaucoma**: Progressive vision loss (peripheral first)
- **Diabetic retinopathy**: Macular edema, vitreous hemorrhage
- **Macular degeneration**: Central vision loss

**Sudden**:
- **Retinal vascular occlusion**: (See Vision Loss section)

---

## DISTORTED VISION (METAMORPHOPSIA)

**Straight lines appear wavy**:

**Causes**:
- **Age-related macular degeneration** (wet AMD): Most common
- **Diabetic macular edema**
- **Macular hole**
- **Epiretinal membrane**
- **Vitreomacular traction**

**Amsler Grid** (home monitoring):
- Grid of straight lines with central dot
- **Patient covers one eye**, stares at dot
- **Abnormal**: Lines appear wavy, missing, distorted
- **Indicates**: Macular pathology

**Management**:
- **Urgent ophthalmology referral** (if sudden onset)

---

## DOUBLE VISION (DIPLOPIA)

**Classification**:

**Binocular Diplopia** (resolves with closing one eye):
- **Misalignment** of eyes (strabismus, palsy)
- **Causes**:
  - **Cranial nerve palsy** (III, IV, VI): Diabetes, hypertension, trauma, aneurysm, tumor
  - **Thyroid eye disease**: Extraocular muscle fibrosis
  - **Myasthenia gravis**: Variable, fatigable
  - **Orbital fracture**: Entrapment, trauma
  - **Stroke**, tumor

**Monocular Diplopia** (persists with closing one eye):
- **Ocular** cause (not neurological)
- **Causes**:
  - **Cataract**: Lens opacity
  - **Refractive error**: Uncorrected astigmatism
  - **Dry eye**: Irregular tear film
  - **Corneal irregularity**: Keratoconus, scarring

**Management**:
- **Urgent referral** if:
  - **Sudden onset**, associated neurological symptoms (stroke risk)
  - **Trauma** (blowout fracture)
  - **Painful** (inflammatory/infectious)
  - **Associated**: Ptosis, pupillary abnormality (III nerve palsy - aneurysm)

---

## HALOS AROUND LIGHTS

**Rainbow-colored rings** around lights:

**Causes**:
- **Acute angle-closure glaucoma** (EMERGENCY):
  - Sudden onset
  - Pain, headache, nausea, vomiting
  - **Immediate ophthalmology referral**
- **Cataract**: Chronic, gradual
- **Corneal edema**: Contact lens overwear, endothelial decompensation

---

## NIGHT BLINDNESS (NYCTALOPIA)

**Difficulty seeing in low light**:

**Causes**:
- **Vitamin A deficiency** (rare in developed countries)
- **Retinitis pigmentosa** (hereditary retinal degeneration)
- **Cataract**
- **Glaucoma** (advanced)

---

## COLOR VISION ABNORMALITIES

**Red Desaturation**:
- **Optic nerve disease** (optic neuritis, glaucoma)

**Complete Color Blindness**:
- **Congenital** (achromatopsia, very rare)

**Red-Green Deficiency**:
- **X-linked** congenital (8% males, 0.5% females)
- **Acquired**: Optic neuritis

---

## VISUAL FIELD DEFECTS

**Types**:

**Central Scotoma**:
- **Optic nerve** disease (optic neuritis, glaucoma)

**Peripheral Field Loss**:
- **Glaucoma**: Peripheral first ("tunnel vision")
- **Retinitis pigmentosa**: Peripheral (ring scotoma)
- **Stroke**: Homonymous hemianopia (same field defect in both eyes)

**Altitudinal**:
- **Ischemic optic neuropathy**

**Bitemporal Hemianopia**:
- **Chiasmal lesion** (pituitary adenoma compressing optic chiasm)

**Management**:
- **Urgent referral** if new or progressive

---

## PHOTOPHOBIA (LIGHT SENSITIVITY)

**Causes**:
- **Anterior uveitis** (with pain, red eye)
- **Corneal abrasion/ulcer**
- **Migraine** (with headache)
- **Meningitis** (with neck stiffness, headache) - **EMERGENCY**
- **Albinism**, aniridia (congenital)

---

**Sources: RCOphth Visual Disturbance Guidelines, NICE CKS, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ophthalmology",
                "focus": "visual_disturbances",
                "sources": ["RCOphth Visual Disturbance Guidelines", "NICE CKS", "AAO Guidelines"]
            }
        )

    def _handle_cataract(self, query: str, context: dict) -> DomainQueryResult:
        """Handle cataract assessment and management"""
        answer = """**CATARACT**

---

## DEFINITION

**Opacity** of the normally clear lens

---

## CLASSIFICATION

**By Location**:

**1. Nuclear Sclerotic Cataract**:
- **Central lens** opacity
- **Symptoms**: Gradual blurred vision, **myopic shift** (reading vision improves, then worsens)
- **Colour**: Yellow/brown discoloration

**2. Cortical Cataract**:
- **Lens cortex** (peripheral)
- **Symptoms**: **Glare** (especially with night driving), monocular diplopia
- **Appearance**: Wedge-shaped opacities, white spoke-like

**3. Posterior Subcapsular Cataract**:
- **Posterior lens capsule**
- **Symptoms**: **Glare**, difficulty reading (affects central vision early)
- **Risk**: Steroid use, diabetes, myopia

---

## RISK FACTORS

- **Age**: Most common (age-related)
- **Diabetes**
- **Steroid use** (systemic or topical)
- **Trauma**: Blunt or penetrating
- **UV exposure**
- **Smoking**
- **Previous ocular surgery** (vitrectomy)
- **Myopia**
- **Family history**
- **Congenital**: (rubella, metabolic disorders)

---

## SYMPTOMS

- **Gradual**: Blurred vision (like looking through frosted glass)
- **Glare**: Difficulty with night driving, oncoming headlights
- **Colour vision**: Dull, yellowed colours
- **Frequent prescription changes**
- **Monocular diplopia**: (double vision in one eye)
- **"Second sight"**: Temporary reading vision improvement (nuclear cataract)

---

## DIAGNOSIS

**Visual Acuity**: Reduced (may improve with pinhole if refractive)

**Slit Lamp Examination**:
- Lens opacity visible
- **Grading**: Based on density, location

**Retinoscopy/Refraction**:
- **Myopic shift** (nuclear cataract)

**Fundus**:
- May be **difficult to visualize** (if cataract dense)

---

## MANAGEMENT

**Indications for Surgery**:

**1. Visual**:
- **Symptomatic**: Patient noticing visual difficulties
- **Reduced acuity**: (varies by patient needs)

**2. Medical**:
- **Lens-induced glaucoma**: Phacomorphic glaucoma (lens swelling, angle closure)
- **Retinal pathology**: Need to visualize fundus (e.g., diabetic retinopathy)

---

**Surgery**:

**Phacoemulsification** (standard):
- **Ultrasound** to break up lens
- **Aspiration** of lens fragments
- **Intraocular lens (IOL)** implantation
- **Day case**, local anesthesia (topical or block)
- **Success rate**: >95%

**Risks**:
- **Infection** (endophthalmitis): 0.1%
- **Retinal detachment**: 0.1-1% (higher in myopes)
- **Posterior capsule rupture**: 2-5%
- **Posterior capsule opacification** (secondary cataract): 20% (treated with YAG laser capsulotomy)

**Preoperative Assessment**:
- **Biometry**: IOL power calculation (axial length, keratometry)
- **Optimize**: Co-pathologies (glaucoma, diabetic retinopathy)

---

## PRE-OPERATIVE COUNSELING

**Expectations**:
- **Improved** vision (not guaranteed)
- **Glasses** may still be needed (reading glasses if monofocal IOL)
- **Recovery**: 2-4 weeks (visual improvement gradual)

**IOL Options**:
- **Monofocal**: Distance vision (most common, usually need reading glasses)
- **Multifocal**: Distance and near (may reduce dependence on glasses, increased glare/halos)
- **Toric**: Corrects astigmatism
- **Accommodative**: (limited availability)

---

## POST-OPERATIVE CARE

**Immediate**:
- **Topical antibiotic**: Chloramphenicol 0.5% QID x 1 week
- **Topical steroid**: Prednisolone 0.5% QID tapering over 4-6 weeks
- ** NSAID**: (if needed)
- **Shield**: At night (1 week)

**Follow-up**:
- **Day 1**: Check IOP, wound, IOL position
- **Weeks 1-4**: Monitor for complications

**Complications**:
- **Endophthalmitis**: (rare, urgent treatment)
- **Cystoid macular edema** (CME): Decreased vision (treat with NSAID, steroid)
- **Posterior capsule opacification**: YAG laser capsulotomy (secondary cataract)

---

## WAITING LIST MANAGEMENT

- **Annual review** (if waiting >1 year)
- **Driving**: If acuity below legal limit, must inform DVLA (UK)
- **Second eye**: Usually 6-12 weeks after first eye (if first eye successful)

---

## CONGENITAL CATARACT

**Presentation**:
- **Leukocoria** (white pupil)
- **Nystagmus**, strabismus (if untreated)
- **Failure to fix/follow**

**Management**:
- **Urgent referral**: (within 1 week of diagnosis)
- **Surgery**: (usually before 8 weeks of age for dense cataract to prevent amblyopia)
- **Long-term**: Glaucoma risk, amblyopia management

---

**Sources: RCOphth Cataract Guidelines, NICE NG97 Cataract, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "ophthalmology",
                "focus": "cataract",
                "sources": ["RCOphth Cataract Guidelines", "NICE NG97", "AAO Guidelines"]
            }
        )

    def _handle_glaucoma(self, query: str, context: dict) -> DomainQueryResult:
        """Handle glaucoma assessment and management"""
        answer = """**GLAUCOMA**

---

## DEFINITION

**Progressive optic neuropathy** with characteristic optic disc changes and visual field loss, **usually associated with elevated intraocular pressure (IOP)**

---

## CLASSIFICATION

### PRIMARY OPEN-ANGLE GLAUCOMA (POAG)

**Most common** form (90% in Caucasians)

**Pathogenesis**:
- **Increased resistance** to aqueous outflow through trabecular meshwork
- **Elevated IOP** (>21 mmHg)
- **Optic nerve** damage (cupping)
- **Visual field loss** (peripheral first)

**Risk Factors**:
- **Age**: >60 years (increases with age)
- **Family history**: First-degree relative (2-4x risk)
- **Ethnicity**: African-Caribbean (higher prevalence, earlier onset, more aggressive)
- **Myopia**
- **Diabetes**
- **Hypertension** (controversial)

**Symptoms**:
- **Asymptomatic** (early stages)
- **Late**: Peripheral visual field loss ("tunnel vision")
- **Advanced**: Central vision loss (may be preserved until late)

**Signs**:
- **Increased IOP**: (>21 mmHg, often 22-30 mmHg)
- **Optic disc cupping**: Vertical cup:disc ratio >0.7, asymmetry >0.2 between eyes
- **Rim thinning**: Notching at disc
- **Retinal nerve fiber layer** loss
- **Visual field defects**: Peripheral arcuate, paracentral scotomas

**Diagnosis**:
- **IOP**: Gold standard (Goldmann applanation tonometry)
- **Optic disc**: Assessment (cup:disc ratio)
- **Visual field testing**: (automated perimetry, Humphrey)
- **Gonioscopy**: Open angle (diagnostic)

**Management**:

**Goal**: Reduce IOP to prevent further optic nerve damage

**Medical** (first-line):
- **Prostaglandin analogue**: (most effective first-line)
  - Latanoprost 0.005% (ONCE daily at night)
  - Bimatoprost 0.01%, Travoprost 0.004%
  - **Side effects**: Conjunctival hyperemia, iris darkening, lash growth, periorbital fat atrophy
- **Beta-blocker**: (alternative or adjunct)
  - Timolol 0.25% or 0.5% BD (CAUTION: contraindicated in asthma, heart failure)
  - **Side effects**: Bradycardia, bronchospasm
- **Carbonic anhydrase inhibitor**: (adjunct)
  - Acetazolamide 250mg TDS PO (short-term), Brinzolamide 1% TID (topical)
- **Alpha-2 agonist**: (adjunct)
  - Brimonidine 0.2% TID
  - **Side effects**: Allergic conjunctivitis (10-15%)

**Laser** (if medical therapy inadequate):
- **Selective laser trabeculoplasty (SLT)**:
  - Low-energy laser to trabecular meshwork
  - **Indications**: Intolerant of drops, non-compliance
  - **Success**: 70-80% (may need repeat)

**Surgical** (if medical/laser inadequate):
- **Trabeculectomy**: (gold standard)
  - Creates new drainage channel
  - **Success**: 80-90% (1 year)
  - **Risks**: Infection, bleeding, hypotony, cataract progression

---

### PRIMARY ANGLE-CLOSURE GLAUCOMA (PACG)

**Pathogenesis**:
- **Anterior displacement** of iris (relative pupillary block)
- **Closure** of drainage angle
- **Elevated IOP** (often >40 mmHg)

**Risk Factors**:
- **Hypermetropia** (shallow anterior chamber)
- **Age**: >60 years
- **Ethnicity**: Asian, Inuit, African-Caribbean (higher risk)
- **Female**: (2:1 female:male)
- **Family history**

**Types**:

**1. Acute Angle-Closure Glaucoma**:
- **EMERGENCY**
- **Symptoms**: Sudden severe eye pain, headache, nausea, vomiting, blurred vision, **halos** around lights
- **Signs**: Red eye, mid-dilated oval pupil, rock-hard eye, corneal edema
- **Management**: **EMERGENCY**
  - **IV acetazolamide** 500mg PO
  - **Topical**: Timolol 0.5%, Brimonidine, Pilocarpine 2% (after IOP reduced)
  - **Laser iridotomy**: (definitive, creates hole in iris)

**2. Chronic Angle-Closure Glaucoma**:
- **Gradual** IOP elevation (angle partially closed)
- **Asymptomatic** (like POAG)
- **Management**: Laser iridotomy, medical therapy, trabeculectomy

---

### OCULAR HYPERTENSION (OHT)

**Elevated IOP** (>21 mmHg) **without** optic disc damage or visual field loss

**Risk of conversion to POAG**: ~1% per year (without treatment)

**Management**:
- **Observation** (if low risk)
- **Treatment** (if high risk: IOP >30 mmHg, thin central cornea, family history)

---

### NORMAL TENSION GLAUCOMA (NTG)

**Optic neuropathy** with normal IOP (<21 mmHg)

**Causes**: Nocturnal hypotension, vasospasm, autoimmune

**Management**: Reduce IOP further (30% reduction from baseline)

---

### SECONDARY GLAUCOMA

**Causes**:
- **Pigment dispersion**: Pigment release from iris (young, myopic males)
- **Pseudoexfoliation**: White flaky material on lens, zonules (elderly)
- **Trauma**: Angle recession (blunt trauma)
- **Uveitis**: Inflammatory debris blocks angle
- **Steroid-induced**: (topical, inhaled, systemic)
- **Neovascular**: (PDR, CRVO, ocular ischemic syndrome)
- **Lens-induced**: Phacomorphic (swollen cataract), phacolytic (leaky cataract)

**Management**: Treat underlying cause + IOP-lowering

---

## SCREENING

**Who to Screen**:
- **Age**: >40 years (every 2 years)
- **High risk**: Family history, African-Caribbean, diabetes (annual)
- **Optician**: Routine eye examination includes IOP, optic disc assessment

**Optic Disc Assessment**:
- **Cup:disc ratio**: Vertical >0.7 (suspicious)
- **Asymmetry**: >0.2 between eyes (suspicious)
- **Rim notching**: (suspicious)

**Visual Field Testing**:
- **Automated perimetry**: (Humphrey, Goldmann)

---

## MONITORING

**Stable Glaucoma**:
- **Review**: 6-12 months
- **Visual field**: Every 1-2 years (or sooner if progression)
- **Optic disc**: Every 1-2 years (photographic documentation)

**Progression**:
- **Worsening visual field** (new or enlarged defects)
- **Increasing cup:disc ratio**
- **IOP**: Despite maximum therapy

**Treatment Escalation**:
- **Add** second/third agent
- **Laser**: SLT
- **Surgery**: Trabeculectomy
- **Cyclodestructive**: (cyclodiode laser) (if refractory)

---

## PATIENT ADVICE

- **Lifelong condition**: (no cure, control only)
- **Medication compliance**: (instill drops regularly)
- **Regular follow-up**: (prevent progression)
- **Driving**: Must meet visual field requirements (inform DVLA if not)
- **Family screening**: First-degree relatives should be screened

---

**Sources: RCOphth Glaucoma Guidelines, NICE NG224, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ophthalmology",
                "focus": "glaucoma",
                "sources": ["RCOphth Glaucoma Guidelines", "NICE NG224", "AAO Guidelines"]
            }
        )

    def _handle_diabetic_retinopathy(self, query: str, context: dict) -> DomainQueryResult:
        """Handle diabetic retinopathy screening and management"""
        answer = """**DIABETIC RETINOPATHY**

---

## EPIDEMIOLOGY

**Most common cause of blindness** in working-age population (20-65 years) in developed countries

**Prevalence**:
- **Type 1 diabetes**: 80% have retinopathy after 15 years
- **Type 2 diabetes**: 50% have retinopathy at diagnosis

---

## PATHOPHYSIOLOGY

**Chronic hyperglycemia** → microvascular damage:

1. **Pericyte loss** (capillary support cells)
2. **Basement membrane thickening** (capillary weakening)
3. **Microaneurysms** (capillary outpouchings)
4. **Capillary non-perfusion** (ischemia)
5. **Increased VEGF** (vascular endothelial growth factor) → neovascularization

---

## CLASSIFICATION

### BACKGROUND DIABETIC RETINOPATHY (BDR)

**Mild, Non-Proliferative**:
- **Microaneurysms**: (earliest sign)
- **Dot and blot hemorrhages**: (deep retinal)
- **Hard exudates**: (lipid leakage, yellow deposits)

**Moderate, Non-Proliferative**:
- **More numerous** microaneurysms, hemorrhages, exudates
- **Cotton wool spots**: (retinal nerve fiber layer infarcts, white/fluffy)

**Severe, Non-Proliferative**:
- **"4-2-1 rule"** (any of following):
  - **4 quadrants** with severe hemorrhages/microaneurysms
  - **2 quadrants** with venous beading
  - **1 quadrant** with IRMA (intraretinal microvascular abnormalities)
- **High risk** of progression to proliferative (50% within 1 year)

---

### PROLIFERATIVE DIABETIC RETINOPATHY (PDR)

**Advanced** stage, high risk of vision loss

**Features**:
- **Neovascularization**: New, abnormal blood vessels
  - **NVE** (new vessels elsewhere): On retina or optic disc
  - **NVD** (new vessels at disc): Higher risk of complications
- **Fibrovascular proliferation**: (vessels + fibrous tissue)
- **Vitreous hemorrhage**: (from neovascularization)
- **Tractional retinal detachment**: (fibrous tissue contraction)
- **Neovascular glaucoma**: (new vessels on iris → glaucoma)

**Symptoms**:
- **Floaters** (vitreous hemorrhage)
- **Sudden vision loss** (vitreous hemorrhage, retinal detachment)
- **May be asymptomatic** (until complications)

**Management**:
- **Urgent ophthalmology referral**
- **Pan-retinal photocoagulation (PRP)**: Laser to ischemic retina (reduces VEGF, causes neovascular regression)
- **Anti-VEGF**: (ranibizumab, aflibercept) for macular edema, vitreous hemorrhage
- **Vitrectomy**: For non-resolving vitreous hemorrhage, tractional retinal detachment

---

### DIABETIC MACULOPATHY (MACULAR EDEMA)

**Most common cause of vision loss** in diabetic retinopathy

**Pathophysiology**: Increased vascular permeability → fluid accumulation in macula

**Features**:
- **Retinal thickening** (macular edema)
- **Hard exudates**: (circinate, near macula)
- **Microaneurysms**: (near fovea)

**Symptoms**:
- **Blurred central vision**
- **Difficulty reading**
- **Distortion** (metamorphopsia)

**Management**:
- **Focal/grid laser**: (for focal edema away from fovea)
- **Anti-VEGF**: (ranibizumab, aflibercept, bevacizumab) - **first-line for center-involving edema**
- **Steroids**: (dexamethasone implant, triamcinolone) - if anti-VEGF contraindicated or refractory

---

## SCREENING

**UK Diabetic Eye Screening Programme**:

**Eligibility**:
- **All** diagnosed diabetics (age 12+)

**Frequency**:
- **Annual**: (if no retinopathy or background only)
- **More frequent**: (if pre-proliferative, proliferative, or maculopathy)

**Method**:
- **Digital retinal photography**: (2 fields, macula centered)
- **Grading**: R0 (none), R1 (background), R2 (pre-proliferative), R3 (proliferative)
- **M1** (maculopathy present)

**Sensitivity**: 80-90% (not 100%)

---

## RISK FACTORS FOR PROGRESSION

- **Duration of diabetes**: (strongest risk factor)
- **Poor glycemic control**: (HbA1c)
- **Hypertension**: (worsens retinopathy)
- **Hyperlipidemia**: (associated with hard exudates)
- **Pregnancy**: (may accelerate)
- **Smoking**
- **Renal disease**: (nephropathy associated)

---

## SYSTEMIC MANAGEMENT

**Glycemic Control**:
- **DCCT trial**: Intensive control reduced progression by 76%
- **HbA1c target**: <48 mmol/mol (6.5%) or individualized

**Blood Pressure Control**:
- **UKPDS**: Tight BP control reduced progression by 34%
- **Target**: <130/80 mmHg

**Lipid Management**:
- **Statin**: (for all diabetics >40 years)

**Smoking Cessation**:
- **Reduces progression**

---

## OPHTHALMOLOGY REFERRAL

**Urgent** (within 2 weeks):
- **Proliferative diabetic retinopathy**
- **Diabetic maculopathy** (with reduced vision)
- **Pre-proliferative** (if close monitoring not possible)
- **Unexplained vision loss**

**Routine**:
- **Background retinopathy** (continue screening)
- **Pre-proliferative** (if can be monitored closely)

---

## PREGNANCY

**Risk**: Progression or new onset

**Management**:
- **Pre-conception**: Optimize control, refer for baseline assessment
- **During pregnancy**: Screen each trimester (or more frequently if retinopathy present)
- **Postpartum**: Screen within 3 months

---

## PATIENT ADVICE

- **Attend screening**: (annual, prevent vision loss)
- **Glycemic control**: (prevents/delays onset and progression)
- **Blood pressure control**: (reduces progression)
- **Smoking cessation**: (reduces progression)
- **Report symptoms**: (sudden vision loss, floaters, flashes, distortion)
- **Driving**: Must meet visual standards (inform DVLA if not)

---

## PROGNOSIS

**Background**: Good (may not progress with good control)
**Pre-proliferative**: 50% progress to proliferative within 1 year (without treatment)
**Proliferative**: High risk of vision loss (with treatment, 50% maintain driving vision)

---

**Sources: RCOphth Diabetic Retinopathy Guidelines, NICE NG28 Diabetes, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "ophthalmology",
                "focus": "diabetic_retinopathy",
                "sources": ["RCOphth Diabetic Retinopathy Guidelines", "NICE NG28", "AAO Guidelines"]
            }
        )

    def _handle_macular_degeneration(self, query: str, context: dict) -> DomainQueryResult:
        """Handle age-related macular degeneration"""
        answer = """**AGE-RELATED MACULAR DEGENERATION (AMD)**

---

## EPIDEMIOLOGY

**Most common cause of registered blindness** in developed countries

**Prevalence**:
- **Age 65-74**: 10%
- **Age 75-84**: 30%
- **Age >85**: 50%

---

## CLASSIFICATION

### DRY AMD (Non-Neovascular, Atrophic)

**80-90%** of AMD

**Pathophysiology**:
- **RPE (retinal pigment epithelium) atrophy**
- **Drusen**: Yellow-white deposits between RPE and Bruch's membrane

**Features**:
- **Drusen**: (hard, small vs soft, large)
- **RPE changes**: (hyperpigmentation, hypopigmentation, atrophy)
- **Geographic atrophy**: (well-demarcated areas of RPE loss)

**Symptoms**:
- **Gradual** central vision loss
- **Difficulty reading**, recognizing faces
- **Need for brighter light**
- **May be asymptomatic** (early)

**Management**:
- **AREDS2 supplements**: (for intermediate AMD)
  - Vitamin C 500mg
  - Vitamin E 400 IU
  - Lutein 10mg
  - Zeaxanthin 2mg
  - Zinc 80mg
  - Copper 2mg
  - **Reduced progression** to advanced AMD by 25%
- **Smoking cessation**: (most important modifiable risk factor)
- **Amsler grid**: (home monitoring)
- **Low vision aids**: (magnifiers, electronic aids)

---

### WET AMD (Neovascular, Exudative)

**10-20%** of AMD but **90% of vision loss** from AMD

**Pathophysiology**:
- **Choroidal neovascularization** (CNV): New abnormal blood vessels from choroid grow through Bruch's membrane into sub-RPE or sub-retinal space
- **Fluid leakage**: (exudation, hemorrhage)
- **Fibrosis**: (eventual scarring)

**Symptoms**:
- **Sudden** or rapid central vision loss
- **Metamorphopsia**: (distortion, straight lines appear wavy)
- **Scotoma**: (central blind spot)
- **Micropsia**: (objects appear smaller)
- **Choroidal neovascular membrane** (CNVM)

**Signs**:
- **Retinal thickening**: (macular edema)
- **Exudates**: (lipid)
- **Hemorrhage**: (sub-retinal, sub-RPE, intraretinal)
- **RPE detachment**: (serous)
- **Disciform scar**: (end-stage, fibrosis)

**Diagnosis**:
- **OCT** (optical coherence tomography): (demonstrates fluid, retinal thickening)
- **Fluorescein angiography**: (identifies CNV location, type)
- **Indocyanine green angiography**: (identifies occult CNV)

**Classification of CNV**:
- **Classic**: Well-defined leakage on fluorescein
- **Occult**: Poorly defined leakage
- **Minimally classic**: Mixture

**Management**:

**Anti-VEGF Therapy** (first-line):

**Agents**:
- **Ranibizumab** (Lucentis): 0.5mg monthly intravitreal injection
- **Aflibercept** (Eylea): 2mg monthly for 3 months, then every 2 months
- **Bevacizumab** (Avastin): (off-label, lower cost, similar efficacy)

**Regimens**:
- **Monthly**: (continuous)
- **PRN** (pro re nata): (as needed, based on OCT findings)
- **Treat and extend**: (extend interval if stable)

**Success**:
- **Stabilization** or improvement of vision in 90%
- **Gain >15 letters**: (3 lines on Snellen) in 30-40%

**Side Effects**:
- **Intravitreal injection**: Endophthalmitis (0.1%), retinal detachment, hemorrhage, cataract
- **Systemic**: Theoretical risk of thromboembolic events (unproven)

**Laser Photocoagulation** (historical):
- **Indications**: Juxtafoveal or extrafoveal CNV (not subfoveal)
- **Limitation**: Causes immediate retinal destruction

**Photodynamic Therapy (PDT)** (historical):
- **Verteporfin**: (photosensitizer)
- **Cold laser**: (activates verteporfin)
- **Indication**: (occult CNV with good vision) - largely replaced by anti-VEGF

---

## RISK FACTORS

**Non-Modifiable**:
- **Age**: (most significant)
- **Genetics**: (CFH, ARMS2/HTRA1 genes)
- **Race**: (Caucasian > African, Asian)
- **Gender**: (Female > male, partly due to longer life expectancy)
- **Family history**: (2-3x risk)

**Modifiable**:
- **Smoking**: (3-4x risk, most important modifiable)
- **Diet**: (low antioxidants, high fat)
- **Obesity**
- **Cardiovascular disease**: (hypertension, hypercholesterolemia)
- **UV exposure**: (possible)

---

## PREVENTION

**AREDS2 Supplements** (for intermediate AMD):
- Vitamin C 500mg
- Vitamin E 400 IU
- Lutein 10mg
- Zeaxanthin 2mg
- Zinc 80mg
- Copper 2mg

**Diet**:
- **Mediterranean diet**: (fish, vegetables, fruits, nuts)
- **Omega-3 fatty acids**: (fish)
- **Lutein/zeaxanthin**: (leafy green vegetables, eggs)

**Lifestyle**:
- **Smoking cessation**: (most important)
- **Exercise**
- **UV protection**: (sunglasses)
- **Weight control**

---

## SCREENING / DETECTION

**Amsler Grid** (home monitoring):
- Grid of straight lines with central dot
- **Patient covers one eye**, stares at dot
- **Abnormal**: Lines appear wavy, missing, distorted
- **Indicates**: Wet AMD conversion

**Regular Eye Examinations**:
- **Annual** (if >50 years or risk factors)
- **Self-monitoring**: (Amsler grid, check weekly)

---

## PROGNOSIS

**Dry AMD**: (slow progression, 10-20% progress to wet)
**Wet AMD**: (rapid progression, 90% central vision loss if untreated)
**With anti-VEGF**: (maintain driving vision in 50-70%)

---

## LOW VISION AIDS

**Optical Aids**:
- **Magnifiers**: (hand-held, stand, illuminated)
- **High-add reading glasses**

**Electronic Aids**:
- **CCTV**: (closed-circuit television, video magnifiers)
- **Tablet apps**: (magnification, contrast enhancement)

**Non-Optical Aids**:
- **Large print**, audiobooks, voice recognition

**Rehabilitation**:
- **Orientation and mobility training**
- **Occupational therapy**

---

## PATIENT ADVICE

- **Stop smoking**: (most important modifiable risk factor)
- **Amsler grid**: (weekly home monitoring)
- **Healthy diet**: (Mediterranean, AREDS2 supplements if intermediate AMD)
- **Regular eye examinations**: (annual)
- **Report symptoms**: (sudden distortion, vision loss, central scotoma)
- **Low vision services**: (if vision loss)

---

**Sources: RCOphth AMD Guidelines, NICE NG82 Age-Related Macular Degeneration, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ophthalmology",
                "focus": "macular_degeneration",
                "sources": ["RCOphth AMD Guidelines", "NICE NG82", "AAO Guidelines"]
            }
        )

    def _handle_retinal_disorders(self, query: str, context: dict) -> DomainQueryResult:
        """Handle retinal vascular disorders"""
        answer = """**RETINAL VASCULAR DISORDERS**

---

## RETINAL VEIN OCCLUSION

### CENTRAL RETINAL VEIN OCCLUSION (CRVO)

**Pathophysiology**:
- **Thrombosis** of central retinal vein at lamina cribrosa
- **Venous congestion**, retinal hemorrhages, disc edema

**Risk Factors**:
- **Hypertension** (most common)
- **Diabetes**
- **Glaucoma** (elevated IOP compresses vein)
- **Hypercoagulable states**
- **Age**: >60 years

**Clinical Features**:
- **Sudden**, painless vision loss (unilateral)
- **Disc edema**: (blurred disc margins)
- **Retinal hemorrhages**: ("blood and thunder" appearance)
  - **Dot and blot hemorrhages**: (deep retinal)
  - **Flame-shaped hemorrhages**: (nerve fiber layer)
  - **Roth spots**: (white-centered hemorrhages)
  - **Subhyaloid hemorrhage**: (between retina and vitreous)
- **Dilated veins**: (tortuous)
- **Cotton wool spots**: (retinal infarcts)

**Types**:

**Non-Ischemic CRVO** (milder):
- **Better vision**: (6/12 or better)
- **Relative afferent pupillary defect**: (absent or mild)
- **Prognosis**: Good, 30% resolve, 50% progress to ischemic

**Ischemic CRVO** (severe):
- **Poor vision**: (6/60 or worse)
- **RAPD**: (marked)
- **Prognosis**: Poor, high risk of neovascular glaucoma (50% within 3-4 months)

**Management**:
- **Urgent ophthalmology referral** (same day)
- **Investigate**: BP, diabetes, coagulation screen, glaucoma assessment
- **Monitor**: (for neovascularization: iris, angle, retina)
- **Macular edema**: Anti-VEGF (ranibizumab, aflibercept)
- **Neovascularization**: Pan-retinal photocoagulation (PRP) laser
- **Observation**: (for non-ischemic, may resolve)

---

### BRANCH RETINAL VEIN OCCLUSION (BRVO)

**Pathophysiology**:
- **Thrombosis** of branch retinal vein at arteriovenous crossing
- **Arteriosclerosis** compresses vein

**Risk Factors**: (same as CRVO)

**Clinical Features**:
- **Sectoral** vision loss (corresponding to affected territory)
- **Retinal hemorrhages**: (limited to sector)
- **Venous dilation**: (in affected sector)
- **No disc edema**: (distinguishes from CRVO)
- **Common sites**: Superotemporal, inferotemporal (70%)

**Management**:
- **Urgent ophthalmology referral**
- **Investigate**: (as for CRVO)
- **Macular edema**: Anti-VEGF, grid laser
- **Neovascularization**: Sectoral PRP laser

---

## RETINAL ARTERY OCCLUSION

### CENTRAL RETINAL ARTERY OCCLUSION (CRAO)

**Pathophysiology**:
- **Embolus** (most common) or thrombosis of central retinal artery
- **Retinal ischemia**, infarction

**Risk Factors**:
- **Carotid atherosclerosis** (most common)
- **Atrial fibrillation** (cardioembolic)
- **Giant cell arteritis** (elderly, may be first manifestation)
- **Hypercoagulable states**
- **Migraine**, vasospasm
- **Trauma**

**Clinical Features**:
- **Sudden**, profound, painless vision loss (unilateral)
- **Afferent pupillary defect** (RAPD)
- **Retina**: White, edematous with **"cherry-red spot"** at fovea (foveola thin, allows choroidal circulation to show)
- **Box-carring**: (segmented blood flow in arteries, late)
- **Arteriolar attenuation**: (narrow vessels)

**Management**:
- **EMERGENCY ophthalmology referral**
- **Immediate interventions** (may dislodge embolus if done within 90 minutes):
  - **Ocular massage**: (intermittent digital pressure for 10-15 seconds, repeat)
  - **Anterior chamber paracentesis**: (withdraw aqueous, lower IOP)
  - **Acetazolamide 500mg IV** (lower IOP)
  - **Breathing carbogen** (95% O2 + 5% CO2) (vasodilates)
- **Efficacy**: Poor (permanent vision loss common)
- **Investigate**: Urgent vascular assessment (carotid Doppler, echocardiogram, ECG, GCA screening if elderly)

---

### BRANCH RETINAL ARTERY OCCLUSION (BRAO)

**Pathophysiology**:
- **Embolus** at arteriolar bifurcation

**Clinical Features**:
- **Sectoral** vision loss (corresponding to affected territory)
- **Retinal whitening**: (in sector)
- **No cherry-red spot**: (unless fovea involved)

**Management**:
- **Urgent ophthalmology referral**
- **Investigate**: (as for CRAO)

---

## RETINAL DETACHMENT

**Pathophysiology**:
- **Separation** of neurosensory retina from retinal pigment epithelium
- **Fluid accumulation** in sub-retinal space

**Types**:

**1. Rhegmatogenous Retinal Detachment** (most common):
- **Retinal break** (hole or tear) allows fluid to enter
- **Causes**: Posterior vitreous detachment (PVD) causing retinal tear, trauma, lattice degeneration
- **Risk factors**: Myopia, previous retinal detachment in fellow eye, family history, trauma, cataract surgery

**2. Tractional Retinal Detachment**:
- **Fibrovascular membranes** pull on retina
- **Causes**: Proliferative diabetic retinopathy, retinopathy of prematurity, sickle cell retinopathy

**3. Exudative (Serous) Retinal Detachment**:
- **Fluid accumulation** without retinal break
- **Causes**: Inflammation (uveitis, VKH), tumors (choroidal melanoma, metastasis), Coats' disease, central serous chorioretinopathy

**Clinical Features**:
- **Symptoms**:
  - **Flashes** (photopsia) from vitreous traction
  - **Floaters** (increased) from vitreous hemorrhage or debris
  - **"Curtain" or "shadow"**: (progressing across vision from periphery)
  - **Central vision loss**: (if macula detached)
- **Signs**:
  - **Elevated retina**: (grey, corrugated)
  - **Loss of red reflex**: (behind detached retina)
  - **Retinal break**: visible (if no hemorrhage)
  - **Reduced intraocular pressure**: (compared to fellow eye)

**Management**:
- **URGENT ophthalmology referral** (same day)
- **Surgical repair**:
  - **Pneumatic retinopexy**: (gas bubble + cryotherapy, for small superior breaks)
  - **Scleral buckle**: (silicone band indents sclera, brings choroid closer to retina)
  - **Vitrectomy**: (removes vitreous, flattens retina, uses gas or silicone oil tamponade)

**Prognosis**:
- **Macula-on detachment**: (better prognosis, urgent repair)
- **Macula-off detachment**: (worse prognosis, repair within 7 days for best results)

---

## RETINAL TEAR (WITHOUT DETACHMENT)

**Symptoms**:
- **Flashes**, floaters (increased)
- **No curtain/shadow** (distinguishes from detachment)

**Signs**:
- **Retinal break**: visible (horseshoe tear, operculated hole)
- **Vitreous hemorrhage**: (may be present)

**Management**:
- **Urgent ophthalmology referral** (same day)
- **Laser retinopexy** or **cryotherapy**: (creates chorioretinal adhesion around break, prevents progression to detachment)

---

## DIABETIC RETINOPATHY

*(See separate section)*

---

**Sources: RCOphth Retinal Vascular Disease Guidelines, NICE CKS, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "ophthalmology",
                "focus": "retinal_disorders",
                "sources": ["RCOphth Retinal Vascular Disease Guidelines", "NICE CKS", "AAO Guidelines"]
            }
        )

    def _handle_dry_eye(self, query: str, context: dict) -> DomainQueryResult:
        """Handle dry eye evaluation and management"""
        answer = """**DRY EYE (Keratoconjunctivitis Sicca)**

---

## DEFINITION

**Multifactorial disorder** of the tear film and ocular surface resulting in **symptoms of discomfort, visual disturbance, and tear film instability**, with potential damage to the ocular surface.

---

## PATHOPHYSIOLOGY

**Tear Film Components**:
- **Lipid layer** (outer): Meibomian glands, prevents evaporation
- **Aqueous layer** (middle): Lacrimal glands, provides moisture, oxygen, nutrients
- **Mucin layer** (inner): Goblet cells, anchors tear film to cornea

---

## CLASSIFICATION

### 1. AQUEOUS DEFICIENCY

**Decreased aqueous production** (lacrimal gland dysfunction)

**Causes**:
- **Age**: (lacrimal gland function declines)
- **Sjögren's syndrome**: (autoimmune, sicca symptoms)
- **Systemic medications**: (anticholinergics, antihistamines, diuretics, beta-blockers)
- **Lacrimal gland damage**: (radiation, sarcoidosis)

### 2. EVAPORATIVE

**Increased tear evaporation** (meibomian gland dysfunction)

**Causes**:
- **Meibomian gland dysfunction (MGD)**: (most common cause)
- **Blepharitis**: (anterior, posterior)
- **Contact lens wear**
- **Low humidity**: (air conditioning, wind)

---

## SYMPTOMS

**Typical**:
- **Dryness**, grittiness, foreign body sensation
- **Burning**, stinging
- **Redness**
- **Tearing** (paradoxical reflex tearing)
- **Blurred vision** (fluctuates with blinking)
- **Contact lens intolerance**
- **Eye fatigue** (especially with reading, computer use)

**Aggravating factors**:
- Reading, computer use
- Air conditioning, wind
- Concentrated tasks (reduced blink rate)

---

## SIGNS

**Tear Film**:
- **Tear breakup time (TBUT)**: <10 seconds (abnormal)
- **Schirmer test**: <5 mm/5 min (severe aqueous deficiency)

**Ocular Surface**:
- **Corneal staining**: (fluorescein, rose bengal)
- **Conjunctival staining**
- **Conjunctival hyperemia**: (redness)
- **Filamentary keratitis**: (mucoid filaments on cornea)

**Eyelids**:
- **Meibomian gland dysfunction**: (blocked glands, inspissated secretions)
- **Blepharitis**: (collarettes, crusting)

**Paradox**: **Symptoms > signs** (common in dry eye)

---

## MANAGEMENT

**Artificial Tears** (first-line):

**Types**:
- **Hypromellose 0.3%**: (inexpensive, preservative-free available)
- **Carbomer 0.2%**: (gel, longer-lasting)
- **Sodium hyaluronate 0.1%**: (high-quality, longer-lasting)
- **Lipid-based tears**: (Systane Complete, Lipimic) for evaporative dry eye
- **Preservative-free**: (preferred if frequent use, >4x daily)

**Dosing**: QID (or more frequently if needed)

---

**Lifestyle Measures**:
- **Blinking**: (conscious blinking, especially during computer use)
- **20-20-20 rule**: (every 20 minutes, look 20 feet away for 20 seconds)
- **Humidifier**: (for dry environments)
- **Avoid**: (drafts, fans, air conditioning blowing directly on face)
- **Omega-3 fatty acids**: (fish oil, flaxseed) - may improve meibomian gland function

---

**Eyelid Hygiene** (for blepharitis/MGD):
- **Warm compresses**: (5-10 minutes BID)
- **Lid massage**: (horizontal strokes for upper lid, vertical for lower lid)
- **Lid scrubs**: (baby shampoo or commercial lid scrubs)
- **Antibiotic ointment**: (fusidic acid 1% nocte) if blepharitis

---

**Punctal Plugs**:
- **Indication**: Refractory to artificial tears
- **Mechanical occlusion** of puncta (reduces tear drainage)
- **Collagen plugs**: (temporary, dissolve in 3-6 months)
- **Silicone plugs**: (permanent but removable)
- **Surgical punctal occlusion**: (permanent, cautery)

---

**Anti-Inflammatory**:
- **Topical cyclosporine 0.05%**: (for aqueous deficiency, specialist only)
- **Topical corticosteroids**: (short course, for severe cases)

---

**Systemic**:
- **Pilocarpine**, cevimeline: (for Sjögren's syndrome)
- **Treat underlying cause**: (stop offending medications if possible)

---

## CONTACT LENS-RELATED DRY EYE

**Contributing factors**:
- **Increased tear evaporation**
- **Mechanical irritation**
- **Reduced blink rate**

**Management**:
- **Contact lens holiday**: (temporarily discontinue)
- **Change lens type**: (silicone hydrogel, higher water content)
- **Reduce wearing time**
- **Preservative-free artificial tears**: (compatible with contact lenses)
- **Punctal plugs**: (if refractory)

---

## PROGNOSIS

**Chronic condition** (usually):
- **Symptoms** may fluctuate
- **Exacerbations** with environmental factors
- **Most** managed conservatively

---

## WHEN TO REFER

**Urgent**:
- **Severe symptoms** despite treatment
- **Corneal ulceration** (severe dry eye)

**Routine**:
- **Refractory** to treatment
- **Suspected Sjögren's syndrome** (dry mouth, systemic symptoms)
- **Punctal plugs** consideration
- **Recurrent corneal erosions** (associated with dry eye)

---

**Sources: RCOphth Dry Eye Guidelines, NICE CKS, TFOS DEWS II Report**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "ophthalmology",
                "focus": "dry_eye",
                "sources": ["RCOphth Dry Eye Guidelines", "NICE CKS", "TFOS DEWS II Report"]
            }
        )

    def _handle_eyelid_disorders(self, query: str, context: dict) -> DomainQueryResult:
        """Handle eyelid disorders"""
        answer = """**EYELID DISORDERS**

---

## BLEPHARITIS

**Inflammation** of eyelid margins

**Types**:

**1. Anterior Blepharitis**:
- **Staphylococcal**: *S. aureus* infection
- **Seborrheic**: Seborrheic dermatitis

**2. Posterior Blepharitis** (Meibomian Gland Dysfunction):
- **Obstruction** of meibomian glands
- **Abnormal secretions** (thick, inspissated)

---

**Symptoms**:
- **Red, itchy eyelids**
- **Crusting**, scaling at lash roots
- **"Gritty" eyes**, foreign body sensation
- **Burning**, discomfort
- **Tearing** (reflex)
- **Worse**: In morning

**Signs**:
- **Eyelid erythema**, edema
- **Collarettes**: (crusts around lashes, pathognomonic for staphylococcal)
- **Meibomian gland dysfunction**: (blocked glands, clouded secretions on expression)
- **Conjunctival injection**: (secondary)

**Management**:

**Eyelid Hygiene** (cornerstone):
- **Warm compresses**: (5-10 minutes BID, to soften secretions)
- **Lid massage**: (horizontal strokes for upper lid, vertical for lower lid, to express glands)
- **Lid scrubs**: (baby shampoo diluted with water, or commercial lid scrubs)
- **Duration**: Long-term (chronic condition)

**Antibiotics** (if staphylococcal or refractory):
- **Topical**: Fusidic acid 1% gel or ointment BD for 1-2 weeks
- **Oral**: Doxycycline 100mg daily for 6-12 weeks (anti-inflammatory effect for posterior blepharitis/MGD)

**Artificial tears**: (for associated dry eye)

---

## HORDEOLUM (STYE)

**Acute infection** of eyelid glands

**Types**:

**1. External Hordeolum** (Stye):
- **Infection** of glands of Zeis or Moll (lash follicles)
- **Staph aureus** (most common)

**2. Internal Hordeolum**:
- **Infection** of meibomian gland (inside eyelid)

**Symptoms**:
- **Painful**, red nodule on eyelid
- **Swelling**, local tenderness
- **Tearing**, photophobia
- **May have**: Purulent discharge (if points)

**Management**:
- **Warm compresses**: (5-10 minutes TID-QID)
- **Topical antibiotic**: (fusidic acid 1% or chloramphenicol 0.5% if pointing)
- **Incision and drainage**: (if pointing and not resolving)
- **Oral antibiotics**: (if cellulitis: flucloxacillin 500mg QDS)
- **Do NOT squeeze**: (risk of cellulitis)

---

## CHALAZION

**Chronic lipogranuloma** of meibomian gland

**Pathogenesis**:
- **Obstruction** of meibomian gland duct
- **Lipid retention**, granulomatous inflammation (not infection)

**Symptoms**:
- **Painless**, slowly enlarging nodule on eyelid
- **Firm**, rubbery
- **May cause**: Astigmatism (if large), cosmetic concern
- **No acute inflammation** (distinguishes from hordeolum)

**Management**:

**Conservative** (first-line):
- **Warm compresses**: (5-10 minutes BID)
- **Lid massage**: (to express contents)
- **Resolution**: (weeks to months, 50% resolve)

**Intralesional Steroid** (if persistent):
- **Triamcinolone** (2-5mg) injection into chalazion
- **Effective**: (80% resolve)

**Incision and Curettage** (if persistent):
- **Indication**: Not resolved after 3-6 months of conservative treatment
- **Procedure**: (day case, local anesthesia)
- **Recurrence**: (uncommon)

---

## PTOSIS

**Drooping** of upper eyelid

**Types**:

**1. Aponeurotic Ptosis** (most common):
- **Dehiscence** of levator aponeurosis
- **Causes**: Age, contact lens wear, trauma, eye surgery
- **Features**: Good levator function, high lid crease

**2. Myogenic Ptosis**:
- **Myasthenia gravis**: (fatigable, variable)
- **Chronic progressive external ophthalmoplegia**: (bilateral)
- **Oculopharyngeal dystrophy**: (familial)

**3. Neurogenic Ptosis**:
- **Third nerve palsy**: (associated pupillary abnormality, eye movement limitation)
- **Horner's syndrome**: (ptosis + miosis + anhidrosis, lesion of sympathetic chain)
- **Myasthenia gravis**: (variable, fatigable)

**4. Mechanical Ptosis**:
- **Scarring**, tumor, dermatochalasis (excess skin)

**5. Congenital Ptosis**:
- **Present from birth**
- **Poor levator function**
- **Risk**: Amblyopia (if covers visual axis)

**Management**:
- **Treat underlying cause**: (myasthenia, third nerve palsy, Horner's)
- **Surgical**: (levator advancement, frontalis sling) for persistent aponeurotic ptosis
- **Urgent referral**: (if sudden onset, pupil involvement, neurologic symptoms)
- **Pediatric**: (urgent referral if congenital, amblyopia risk)

---

## DERMATOCHALASIS

**Excess eyelid skin** (age-related)

**Symptoms**:
- **Cosmetic concern**
- **Functional**: (visual field obstruction if severe)
- **Heavy**, tired eyelids

**Management**:
- **Blepharoplasty**: (surgical removal of excess skin, fat)

---

## ENTROPION

**Inward turning** of eyelid (lashes rub on eye)

**Causes**:
- **Involutional** (age-related): (horizontal lid laxity, disinsertion of lid retractors)
- **Cicatricial** (scarring): (cicatricial pemphigoid, trachoma, chemical burn)

**Symptoms**:
- **Irritation**, foreign body sensation
- **Redness**, tearing
- **Corneal abrasion**: (from lashes)

**Management**:
- **Temporary**: Taping eyelid, botulinum toxin
- **Surgical**: (eyelid tightening, tarsal rotation)

---

## ECTROPION

**Outward turning** of eyelid

**Causes**:
- **Involutional** (age-related): (horizontal lid laxity, disinsertion of lid retractors)
- **Cicatricial** (scarring): (sun damage, previous surgery)
- **Mechanical**: (tumor)
- **Paralytic**: (facial nerve palsy)

**Symptoms**:
- **Tearing** (epiphora, due to poor tear drainage)
- **Exposure** (corneal drying)
- **Redness**, irritation

**Management**:
- **Lubrication**: (artificial tears)
- **Surgical**: (eyelid tightening, lateral tarsal strip)

---

## LACRIMAL SYSTEM DISORDERS

**Epiphora** (watery eye):

**Causes**:
- **Obstruction**: (blocked nasolacrimal duct)
- **Pump failure**: (eyelid laxity, facial nerve palsy)
- **Dry eye**: (paradoxical reflex tearing)
- **Allergy**: (conjunctivitis)

**Management**:
- **Syringing and probing**: (for obstruction)
- **Dacryocystorhinostomy (DCR)**: (surgical creation of new drainage passage)

**Dacryocystitis** (infection of lacrimal sac):
- **Symptoms**: Pain, redness, swelling over medial canthus, purulent discharge
- **Management**: Oral flucloxacillin 500mg QDS, urgent ophthalmology referral if recurrent or child

---

**Sources: RCOphth Eyelid Disorders Guidelines, NICE CKS, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "ophthalmology",
                "focus": "eyelid_disorders",
                "sources": ["RCOphth Eyelid Disorders Guidelines", "NICE CKS", "AAO Guidelines"]
            }
        )

    def _handle_contact_lens(self, query: str, context: dict) -> DomainQueryResult:
        """Handle contact lens-related issues"""
        answer = """**CONTACT LENS-RELATED ISSUES**

---

## CONTACT LENS TYPES

**Soft Lenses**:
- **Hydrogel**: (water content, oxygen permeability)
- **Silicone hydrogel**: (higher oxygen permeability, extended wear)
- **Daily disposable**: (most convenient, lowest infection risk)
- **Monthly**: (more affordable, require cleaning)

**Rigid Gas-Permeable (RGP) Lenses**:
- **Better oxygen permeability**
- **Sharper vision** (for astigmatism, keratoconus)
- **Longer adaptation** period

---

## CONTACT LENS-RELATED COMPLICATIONS

### CORNEAL HYPOXIA

**Insufficient oxygen** to cornea

**Causes**:
- **Overwear**: (extended wear, overnight wear)
- **Low oxygen permeability lenses**: (old hydrogel)

**Signs**:
- **Neovascularization**: (new blood vessels growing into cornea, 1-4 mm from limbus)
- **Corneal edema**: (stromal thickening, striae)

**Management**:
- **Change lenses**: (to higher Dk/t, silicone hydrogel)
- **Reduce wearing time**: (discontinue overnight wear)

---

### GIANT PAPILLARY CONJUNCTIVITIS (GPC)

**Allergic reaction** to contact lens deposits

**Symptoms**:
- **Itching**, mucus discharge
- **Lens movement**: (excessive, lens rides up)
- **Blurred vision** (lens displacement)

**Signs**:
- **Giant papillae**: (>1mm, on upper tarsal conjunctiva)
- **Contact lens deposits**: (visible)

**Management**:
- **Discontinue contact lenses**: (temporarily, 2-4 weeks)
- **Change lenses**: (to daily disposable)
- **Optimize cleaning**: (if reusable lenses)
- **Mast cell stabilizer**: (sodium cromoglicate 2% QID) if persistent

---

### CORNEAL INFILTRATES

**Inflammatory** or **infectious** infiltrates

**Types**:

**1. Contact Lens-Induced Acute Red Eye (CLARE)**:
- **Inflammatory** (toxic response to lens deposits or endotoxin)
- **Pain**, redness, photophobia
- **Small peripheral infiltrates**
- **Management**: Discontinue lenses, supportive, no antibiotic

**2. Microbial Keratitis** (SERIOUS):
- **Infectious** (bacteria, *Pseudomonas*, *Acanthamoeba*)
- **Pain** (severe), redness, photophobia, reduced vision
- **Corneal ulcer**: (white opacity, stain)
- **Management**: **URGENT ophthalmology referral**

---

### CORNEAL ULCER (INFECTIOUS KERATITIS)

**EMERGENCY**

**Risk Factors**:
- **Overnight wear**: (5-10x increased risk)
- **Poor hygiene**: (tap water rinsing, poor case cleaning)
- **Extended wear**: (monthly, annual lenses)
- **Trauma**: (dirt, dust)

**Pathogens**:
- **Bacteria**: *Pseudomonas aeruginosa* (most common, most severe)
- **Acanthamoeba**: (from tap water, rare but severe)
- **Fungal**: (rare, trauma with vegetable matter)

**Symptoms**:
- **Severe pain**, photophobia
- **Red eye**, tearing
- **Reduced vision**
- **Foreign body sensation**

**Signs**:
- **Corneal opacity/ulcer**: (white lesion)
- **Anterior chamber reaction**: (cells and flare)
- **Hypopyon**: (white cells in anterior chamber, if severe)

**Management**:
- **STOP contact lenses immediately**
- **Urgent ophthalmology referral** (same day)
- **Corneal scrape**: (culture, identify organism)
- **Fortified antibiotics**: (hourly, e.g., cefazolin 5% + gentamicin 1.5%)
- **Acanthamoeba**: (polyhexamethylene biguanide + propamidine isethionate)

---

### CORNEAL ABRASION

**Scratch** on corneal epithelium

**Symptoms**:
- **Foreign body sensation**, pain, tearing, photophobia

**Management**:
- **Remove lens**: (if still present)
- **Fluorescein stain**: (confirm abrasion, rule out foreign body)
- **Topical antibiotic**: (chloramphenicol 0.5% QID for 2-3 days)
- **Do NOT patch**: (increases infection risk)
- **Review**: (24 hours)

---

## CONTACT LENS HYGIENE

**Do's**:
- **Wash hands** before handling lenses
- **Rub, rinse, store**: (cleaning case with solution, rub lenses)
- **Replace case**: (every 1-3 months)
- **Use fresh solution**: (never top up or reuse)
- **Follow replacement schedule**: (daily, 2-weekly, monthly)

**Don'ts**:
- **NO water exposure**: (swimming, showering, hot tub with lenses in)
- **NO saliva**: (to wet lenses)
- **NO tap water**: (to rinse lenses or case)
- **NO sleeping in lenses**: (unless extended wear, approved by optician)
- **NO overwear**: (adhere to recommended wearing time)

---

## CONTACT LENS INTOLERANCE

**Causes**:
- **Dry eye**: (most common)
- **Giant papillary conjunctivitis**
- **Poor fit**: (tight or loose lens)
- **Overwear**: (corneal hypoxia)
- **Presbyopia**: (age-related near vision difficulty)

**Management**:
- **Treat dry eye**: (artificial tears, preservative-free)
- **Change lens type**: (daily disposable, silicone hydrogel)
- **Refit**: (different base curve, diameter)
- **Reduce wearing time**
- **Consider alternatives**: (spectacles, refractive surgery)

---

## CONTACT LENS PRESCRIPTION

**Legal Requirement**:
- **Must be in-date**: (UK: within 1 year)
- **Must specify**: (power, base curve, diameter, type)

**Over-the-Counter Lenses** (cosmetic):
- **Still require fitting**: (to ensure safe fit)
- **Poor quality**: (higher risk of complications)

---

**Sources: RCOphth Contact Lens Guidelines, BCLA Contact Lens Guidelines, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "ophthalmology",
                "focus": "contact_lenses",
                "sources": ["RCOphth Contact Lens Guidelines", "BCLA Guidelines", "AAO Guidelines"]
            }
        )

    def _handle_ocular_trauma(self, query: str, context: dict) -> DomainQueryResult:
        """Handle ocular trauma and emergencies"""
        answer = """**OCULAR TRAUMA**

---

## CHEMICAL INJURY

**EMERGENCY - IMMEDIATE IRRIGATION**

**Time is critical** (irrigate immediately, do not wait for full assessment)

**Management**:
1. **Remove contact lenses** (if present)
2. **Immediate irrigation**: (water, tap water, saline) for **15-30 minutes** (or until pH normal)
3. **Continue irrigation**: (during transfer to hospital)
4. **pH testing**: (check pH after irrigation, aim for pH 7.0-7.2)
5. **Refer**: **Urgent to ophthalmology** (same day, may require admission)

**Chemicals**:
- **Alkali** (more severe): (lime, cement, ammonia, bleach) - penetrates deeper
- **Acid**: (hydrochloric, sulfuric) - coagulates proteins, may limit penetration

**Prognosis**:
- **Immediate irrigation**: (improves outcome)
- **Alkali**: (worse prognosis than acid)

---

## CORNEAL FOREIGN BODY

**Symptoms**:
- **Foreign body sensation**, pain
- **Tearing**, photophobia
- **History**: (metal grinding, hammering, wind-blown debris)

**Management**:
1. **Everting eyelids**: (look for foreign body on upper tarsal conjunctiva)
2. **Remove**: (if easily accessible, using cotton tip or needle (slit lamp) with topical anesthesia)
3. **Fluorescein stain**: (after removal, check for abrasion)
4. **Topical antibiotic**: (chloramphenicol 0.5% QID for 2-3 days)
5. **Rust ring**: (if ferrous foreign body, may need removal by ophthalmologist)

**Caution**:
- **Do NOT** remove if deeply embedded or perforating (refer)
- **Tetanus prophylaxis**: (update if required)

---

## CORNEAL ABRASION

**Scratch** on corneal epithelium

**Causes**:
- **Foreign body**: (removed or still present)
- **Contact lens**: (overwear, trauma)
- **Fingernail**, paper

**Symptoms**:
- **Foreign body sensation**, pain
- **Tearing**, photophobia
- **Red eye**, blepharospasm

**Management**:
- **Remove foreign body**: (if present)
- **Fluorescein stain**: (green uptake confirms abrasion)
- **Topical antibiotic**: (chloramphenicol 0.5% QID for 2-3 days)
- **Do NOT patch**: (increases infection risk, no faster healing)
- **Review**: (24 hours)
- **Contact lens wearers**: **Urgent ophthalmology review** (pseudomonas risk)

---

## BLUNT OCULAR TRAUMA

**Mechanisms**:
- **Fist**, ball, object hitting eye
- **Airbag**, dashboard impact

---

**Hyphema** (blood in anterior chamber):

**Grading**:
- **Grade I**: (layered blood, <1/3 anterior chamber)
- **Grade II**: (1/3 - 1/2)
- **Grade III**: (>1/2)
- **Grade IV**: (total hyphema, "8-ball")

**Management**:
- **Urgent ophthalmology referral**
- **Bed rest**: (head elevated 30-45°)
- **Topical steroid**: (prednisolone 0.5% QID)
- **Cycloplegic**: (cyclopentolate 1% TID)
- **IOP-lowering**: (if elevated)
- **Surgical**: (washout if corneal blood staining, elevated IOP refractory)

---

**Traumatic Iritis**:
- **Pain**, photophobia, red eye (unilateral)
- **History**: (blunt trauma days earlier)
- **Management**: Cycloplegic (cyclopentolate 1% TID), topical steroid

---

**Lens Dislocation/Subluxation**:
- **History**: (significant blunt trauma)
- **Signs**: (lens visible in anterior chamber [dislocation] or vitreous [subluxation])
- **Management**: **Urgent ophthalmology referral**

---

**Vitreous Hemorrhage**:
- **History**: (significant trauma, especially if pre-existing retinal condition)
- **Symptoms**: (floaters, decreased vision)
- **Signs**: (unable to visualize retina on fundoscopy)
- **Management**: **Urgent ophthalmology referral**

---

**Retinal Detachment**:
- **Symptoms**: (flashes, floaters, curtain/shadow)
- **History**: (significant blunt trauma)
- **Management**: **Urgent ophthalmology referral**

---

**Orbital Blowout Fracture**:
- **Mechanism**: (blunt trauma to eye, force transmitted to orbital floor/medial wall)
- **Signs**:
  - **Enophthalmos**: (sunken eye)
  - **Diplopia**: (from entrapment of inferior rectus or medial rectus)
  - **Infraorbital nerve anesthesia**: (numb cheek, upper gum)
  - **Emphysema**: (air in orbit, crepitus)
- **Management**: **Urgent ophthalmology referral** (CT orbit to assess)

---

**Globe Rupture** (severe):
- **History**: (severe trauma, sharp object)
- **Signs**:
  - **Deep anterior chamber**, flat anterior chamber
  - **Hyphema**, vitreous hemorrhage
  - **Uveal tissue prolapse**
  - **Misshapen eye** (if scleral rupture)
- **Management**:
  - **Do NOT examine** (avoid manipulation, may cause extrusion of contents)
  - **Shield eye**: (protect, do not apply pressure)
  - **Urgent ophthalmology referral** (for surgical repair)

---

## PENETRATING OCULAR INJURY

**Foreign body** penetrating globe

**History**:
- **Sharp object**: (metal, glass, wood)
- **High-velocity**: (grinding, hammering)

**Signs**:
- **Visible foreign body** (in cornea, sclera, or intraocular)
- **Corneal or scleral laceration**
- **Vitreous hemorrhage**
- **Lens injury** (cataract)
- **Shallow/flat anterior chamber**
- **Pupil**: may be irregular, peaked toward laceration

**Management**:
- **Do NOT remove foreign body** (if globe penetration suspected)
- **Shield eye**: (protect, do not apply pressure)
- **NPO**: (nothing by mouth, may need surgery)
- **Urgent ophthalmology referral** (for surgical exploration, foreign body removal)

---

## INTRAOCULAR FOREIGN BODY

**High-velocity** foreign body (metal, glass) penetrates globe

**History**:
- **Hammering**, grinding metal (high risk)
- **May be asymptomatic**: (small foreign body)

**Management**:
- **High index of suspicion**: (any high-velocity injury)
- **CT scan**: (to locate foreign body, MRI contraindicated if metal)
- **Urgent ophthalmology referral** (for foreign body removal)

---

## ORBITAL CELLULITIS

**(See Red Eye section)**

---

## EYELID LACERATION

**Management**:
- **Assess depth**: (superficial vs through tarsal plate)
- **Canalicular involvement**: (medial eyelid lacerations may involve nasolacrimal duct)
- **Ophthalmology referral**: (for repair if through tarsal plate or canalicular involvement)

---

## TETANUS PROPHYLAXIS

**Indications**:
- **Penetrating ocular injury**: (organic material, soil-contaminated)
- **Assess immunization status**: (give booster if not fully vaccinated or >10 years since last dose)

---

## OCULAR TRAUMA ASSESSMENT

**History**:
- **Mechanism**: (blunt vs penetrating, chemical, foreign body)
- **Time**: (of injury)
- **Visual symptoms**: (decreased vision, double vision)
- **Eye protection**: (worn or not)

**Examination**:
- **Visual acuity**: (baseline)
- **Pupils**: (RAPD, shape, reactivity)
- **Extraocular movements**: (entrapment, palsy)
- **Anterior segment**: (hyphema, lens dislocation, foreign body)
- **Intraocular pressure**: (if globe intact)
- **Fundoscopy**: (if view possible)

---

## PREVENTION

**Eye Protection**:
- **Safety glasses**: (with side shields for high-risk activities)
- **Polycarbonate lenses**: (impact-resistant)
- **Sports**: (racquet sports, basketball, lacrosse)
- **Occupational**: (metal grinding, welding, construction)

**Chemical Safety**:
- **Goggles**: (for chemical handling)
- **Eyewash stations**: (accessible, maintained)

---

**Sources: RCOphth Ocular Trauma Guidelines, NICE Ocular Trauma Guidelines, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "ophthalmology",
                "focus": "ocular_trauma",
                "urgency": "emergency",
                "sources": ["RCOphth Ocular Trauma Guidelines", "NICE Ocular Trauma Guidelines", "AAO Guidelines"]
            }
        )

    def _handle_pediatric_ophthalmology(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pediatric ophthalmology conditions"""
        answer = """**PEDIATRIC OPHTHALMOLOGY**

---

## AMBLYOPIA ("Lazy Eye")

**Definition**: Decreased vision due to abnormal visual development during childhood

**Causes**:
- **Strabismus**: (misaligned eyes, brain suppresses deviating eye)
- **Anisometropia**: (unequal refractive error between eyes)
- **Deprivation**: (cataract, ptosis obscuring visual axis)
- **High refractive error**: (unilateral or bilateral)

**Critical Period**: **0-7 years** (treatment more effective when younger)

**Screening**:
- **All children**: (vision assessment at age 4-5 years, UK)
- **Risk factors**: (family history, prematurity, developmental delay)

**Management**:
- **Correct refractive error**: (glasses)
- **Occlusion therapy**: (patching of good eye)
  - **Patching**: (2-6 hours daily, depending on age and severity)
  - **Atropine penalization**: (blur good eye with atropine drops, alternative to patching)
- **Compliance**: (critical for success)

**Prognosis**:
- **Better**: (younger age at treatment, <7 years optimal)
- **Poor**: (if untreated after age 7-8, permanent vision loss)

---

## STRABISMUS (Squint)

**Misalignment** of eyes

**Types**:

**1. Esotropia** (inward turn):
- **Infantile esotropia**: (onset <6 months, constant)
- **Accommodative esotropia**: (onset 2-3 years, associated with hypermetropia)
- **Intermittent esotropia**: (worse with fatigue, illness)

**2. Exotropia** (outward turn):
- **Intermittent exotropia**: (most common, worse when tired, daydreaming)
- **Constant exotropia**: (less common)

**3. Hypertropia** (upward turn): (usually due to vertical muscle imbalance)

**4. Hypotropia** (downward turn)

---

**Pseudostrabismus**:
- **Appearance** of strabismus but eyes are straight
- **Epicanthal folds**: (common in Asian, African infants, wide nasal bridge)
- **No treatment** needed

---

**Management**:
- **Refractive correction**: (glasses for accommodative esotropia)
- **Patching**: (if amblyopia present)
- **Surgery**: (to realign muscles, usually after amblyopia treated)
- **Botulinum toxin**: (alternative to surgery in selected cases)

---

## NASOLACRIMAL DUCT OBSTRUCTION

**Blocked tear duct** (common in infants)

**Incidence**: 5-10% of newborns

**Symptoms**:
- **Tearing** (epiphora)
- **Sticky discharge**: (recurrent)
- **Matted eyelashes**: (especially in morning)
- **Onset**: (first few weeks of life)
- **Usually unilateral**

**Management**:
- **Conservative** (first-line):
  - **Crigler massage**: (massage over lacrimal sac, downward pressure)
  - **Antibiotic drops**: (if infection, fusidic acid 1% TID)
  - **Resolution**: (90% by 12 months)
- **Probing** (if not resolved by 12 months):
  - **Day case**, general anesthesia
  - **Success**: (95% after first probing)

---

## CONGENITAL CATARACT

**Lens opacity** present at birth

**Causes**:
- **Genetic**: (autosomal dominant, most common)
- **Congenital infections**: (rubella, CMV, toxoplasmosis)
- **Metabolic**: (galactosemia, diabetes)
- **Syndromic**: (Down syndrome, others)
- **Idiopathic**

**Presentation**:
- **Leukocoria** (white pupil)
- **Nystagmus**: (if bilateral, dense cataract)
- **Failure to fix/follow**
- **Strabismus**

**Management**:
- **Urgent referral**: (within 1 week of diagnosis)
- **Surgery**: (usually before 8 weeks for dense unilateral cataract, to prevent amblyopia)
- **Long-term**: (amblyopia management, glaucoma risk, IOL implantation or contact lens)

---

## RETINOPATHY OF PREMATURITY (ROP)

**Abnormal retinal vascular development** in premature infants

**Risk Factors**:
- **Gestational age**: <32 weeks
- **Birth weight**: <1500g
- **Oxygen therapy**: (high concentrations, duration)

**Screening**:
- **Gestational age <32 weeks** OR birth weight <1500g
- **First examination**: (at 30-31 weeks postmenstrual age or 4-5 weeks after birth)
- **Frequency**: (every 1-2 weeks until vascularization mature)

**Classification**:
- **Stages 1-5**: (increasing severity)
- **Plus disease**: (dilated, tortuous vessels, indicates active disease)
- **Threshold disease**: (requires treatment)

**Management**:
- **Laser photocoagulation**: (for threshold disease, ablate avascular retina)
- **Anti-VEGF**: (emerging, intravitreal bevacizumab)
- **Surgery**: (for stage 4-5 retinal detachment)

**Prognosis**:
- **Good**: (with early treatment, 90% avoid blindness)
- **Complications**: (myopia, strabismus, amblyopia, glaucoma)

---

## PEDIATRIC GLAUCOMA

**Primary Congenital Glaucoma**:
- **Onset**: (birth to 3 years)
- **Triad**:
  1. **Epiphora** (tearing)
  2. **Photophobia** (light sensitivity)
  3. **Blepharospasm** (eye squeezing)
- **Signs**:
  - **Corneal enlargement**: (buphthalmos)
  - **Corneal edema**, Haab's striae (breaks in Descemet's membrane)
  - **Elevated IOP**
  - **Optic disc cupping**
- **Management**: **Urgent ophthalmology referral** (surgery: goniotomy, trabeculectomy)

**Juvenile Glaucoma**:
- **Onset**: (3 years to adulthood)
- **Similar to adult glaucoma**: (asymptomatic until advanced)
- **Management**: (medications, surgery)

---

## PTOSIS IN CHILDREN

**Causes**:
- **Congenital**: (most common, due to levator aponeurosis dysgenesis)
- **Myasthenia gravis**: (variable, fatigable)
- **Neurogenic**: (third nerve palsy, Horner's syndrome)
- **Mechanical**: (trauma, tumor)

**Congenital Ptosis**:
- **Poor levator function**: (minimal eyelid movement)
- **Amblyopia risk**: (if ptosis covers visual axis)
- **Management**:
  - **Observation**: (if mild, no amblyopia)
  - **Surgery**: (if moderate-severe, before age 5 for amblyopia prevention)

---

## RETINOBLASTOMA

**Most common** primary intraocular malignancy of childhood

**Incidence**: 1 in 15,000-20,000 live births

**Presentation**:
- **Leukocoria** (white pupil): (60-80%, most common)
- **Strabismus**: (20%)
- **Decreased vision**: (if macular involvement)
- **Orbital inflammation**: (if extraocular extension)

**Diagnosis**:
- **Clinical**: (characteristic appearance on fundoscopy)
- **Imaging**: (ultrasound, CT, MRI)
- **Genetic testing**: (RB1 gene, family screening)

**Management**:
- **Urgent referral**: (to ocular oncology center)
- **Chemoreduction**: (systemic or intra-arterial chemotherapy)
- **Focal therapy**: (laser, cryotherapy)
- **Enucleation**: (if advanced)

**Prognosis**:
- **Survival**: (>95% in developed countries)
- **Vision**: (varies, depends on tumor size, location, treatment)

---

## PEDIATRIC EYE EXAMINATION

**Age-appropriate** assessment:

**Newborn**:
- **Red reflex test**: (to detect cataract, retinoblastoma)
- **Corneal clarity**
- **Pupil responses**

**Infant (6 weeks)**:
- **Fix and follow**: (visual behavior)
- **Eye alignment**: (corneal light reflex, cover test)

**Toddler (1-3 years)**:
- **Visual acuity**: (preferential looking, Cardiff cards)
- **Cover test**: (detect strabismus)
- **Refractive screening**: (photoscreener or autorefractor)

**Preschool (3-5 years)**:
- **Visual acuity**: (Snellen or LogMAR, matched to age)
- **Cover test**
- **Colour vision**: (Ishihara plates, age 5+)

**School Age**:
- **Visual acuity**: (Snellen 6/6 or better)
- **Colour vision**: (boys especially, 8% red-green deficiency)

---

**Sources: RCOphth Pediatric Ophthalmology Guidelines, NICE, RCPCH Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "ophthalmology",
                "focus": "pediatric_ophthalmology",
                "sources": ["RCOphth Pediatric Ophthalmology Guidelines", "NICE", "RCPCH Guidelines"]
            }
        )

    def _handle_general_ophthalmology(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general ophthalmology consultation"""
        answer = """**GENERAL OPHTHALMOLOGY CONSULTATION**

Ophthalmology covers the diagnosis and management of eye and vision disorders.

**Common Conditions Managed**:
- **Red eye**: Conjunctivitis, scleritis, uveitis, glaucoma
- **Vision disturbances**: Blurred vision, floaters, flashes, double vision
- **Eye pain**: Corneal abrasion, foreign body, uveitis, glaucoma
- **Cataract**: Cloudy lens, age-related, congenital
- **Glaucoma**: Increased eye pressure, optic nerve damage
- **Diabetic eye disease**: Diabetic retinopathy, macular edema
- **Macular degeneration**: Age-related, wet and dry forms
- **Dry eye**: Tear film dysfunction
- **Eyelid disorders**: Blepharitis, stye, chalazion, ptosis
- **Ocular trauma**: Chemical injury, foreign body, blunt trauma

**Diagnostic Approaches**:
- **Visual acuity**: Snellen chart, pinhole testing
- **Intraocular pressure**: Tonometry
- **Slit lamp examination**: Anterior segment, cornea, anterior chamber
- **Fundoscopy**: Optic disc, retina, vessels
- **Visual fields**: Perimetry, confrontation
- **Fluorescein staining**: Corneal abrasions, ulcers

**When to Seek Urgent Review**:
- **Sudden vision loss** (CRAO, CRVO, retinal detachment)
- **Painful red eye** (acute angle-closure glaucoma, uveitis, keratitis)
- **Eye trauma** (chemical injury, penetrating injury)
- **Contact lens wearers** with red eye (pseudomonas risk)
- **Flashes and floaters** (retinal tear, detachment)

**Sources**: RCOphth Guidelines, NICE Ophthalmology Guidelines, AAO Guidelines**
"""

        return DomainQueryResult(
            domain_name="ophthalmology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "ophthalmology",
                "focus": "general_consultation",
                "sources": ["RCOphth Guidelines", "NICE Ophthalmology Guidelines", "AAO Guidelines"]
            }
        )


def create_ophthalmology_domain():
    """Factory function to create ophthalmology domain instance"""
    return OphthalmologyDomain()


# Domain registration
try:
    from gpdisc_core.domains.registry import DomainModuleRegistry
    DomainModuleRegistry.register(OphthalmologyDomain)
except ImportError:
    # Registry not available yet
    pass
