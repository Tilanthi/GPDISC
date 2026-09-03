"""
GPDISC Dermatology Domain Module

This module provides dermatological consultation capabilities including:
- Rash pattern recognition and differential diagnosis
- Acne and rosacea management
- Eczema and dermatitis
- Psoriasis management
- Skin lesion evaluation
- Melanoma and skin cancer recognition
- Contact dermatitis
- Fungal skin infections
- Drug eruptions
- Pediatric rashes

Evidence-based with guidelines from:
- British Association of Dermatologists (BAD)
- NICE Dermatology Guidelines
- American Academy of Dermatology (AAD)
- Primary Care Dermatology Society (PCDS)
"""

from typing import Optional, Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class DermatologyDomain(BaseDomainModule):
    """
    Dermatology specialty domain for skin conditions and diseases.

    Covers comprehensive dermatological consultation including:
    - Rash pattern recognition by morphology and distribution
    - Acne vulgaris and rosacea management
    - Eczema (atopic, discoid, seborrheic, contact, etc.)
    - Psoriasis and psoriatic arthritis
    - Skin lesion assessment (benign vs malignant)
    - Melanoma recognition (ABCDE criteria)
    - Non-melanoma skin cancer (BCC, SCC)
    - Contact dermatitis and allergy
    - Fungal and viral skin infections
    - Drug eruptions and pharmacology
    - Pediatric dermatology
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="dermatology",
            version="1.0.0",
            dependencies=[],
            description="Dermatology: Skin diseases, rash diagnosis, skin cancer, acne, eczema, psoriasis",
            keywords=[
                "skin", "rash", "dermatology", "dermatological", "dermatologist",
                "acne", "spots", "pimples", "blackheads", "whiteheads", "comedones",
                "eczema", "atopic", "dermatitis", "itchy", "pruritus", "scratching",
                "psoriasis", "plaques", "scales", "scalp", "silvery",
                "rosacea", "flushing", "redness", "telangiectasia",
                "melanoma", "skin cancer", "mole", "lesion", "abcd", "ugly duckling",
                "basal cell", "bcc", "rodent ulcer", "pearly", "telangiectasia",
                "squamous cell", "scc", "actinic keratosis", "solar keratosis",
                "fungal", "tinea", "ringworm", "athlete's foot", "thrush", "candida",
                "viral", "warts", "verruca", "herpes", "cold sore", "shingles", "chickenpox",
                "contact dermatitis", "allergy", "patch test", "nickel", "latex",
                "drug eruption", "allergic reaction", "sjs", "ten", "dress",
                "hives", "urticaria", "angioedema", "welts",
                "pediatric rash", "childhood rash", "measles", "rubella", "fifth", "sixth",
                "impetigo", "cellulitis", "erysipelas", "abscess", "boil",
                "scabies", "lice", "head lice", "pubic lice",
                "alopecia", "hair loss", "alopecia areata",
                "nail", "onychomycosis", "ingrown", "fungal nail",
                "urticaria", "angioma", "cherry angioma", "seborrhoeic keratosis",
                "actinic", "photoaging", "sun damage", "photoprotection", "sunscreen", "spf",
                "skin biopsy", "dermoscopy", "teledermatology"
            ],
            capabilities=[
                "rash_pattern_recognition", "acne_management", "eczema_management",
                "psoriasis_management", "skin_cancer_detection", "melanoma_assessment",
                "contact_dermatitis_diagnosis", "fungal_infection_treatment",
                "drug_eruption_identification", "pediatric_dermatology"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Process dermatology queries with appropriate specialty routing"""
        query_lower = query.lower()

        # Skin cancer and melanoma - HIGHEST PRIORITY
        if any(term in query_lower for term in ["melanoma", "skin cancer", "bcc", "basal cell", "scc", "squamous", "changing mole", "suspicious mole", "ugly duckling"]):
            return self._handle_skin_cancer(query, context)

        # Rash pattern recognition
        elif any(term in query_lower for term in ["rash", "skin rash", "erythema", "maculopapular", "vesicular", "bullous"]):
            return self._handle_rash_pattern(query, context)

        # Acne and rosacea
        elif any(term in query_lower for term in ["acne", "spots", "pimples", "blackheads", "whiteheads", "comedones", "rosacea", "flushing"]):
            return self._handle_acne_rosacea(query, context)

        # Eczema and dermatitis
        elif any(term in query_lower for term in ["eczema", "dermatitis", "atopic", "itchy", "pruritus", "dry skin"]):
            return self._handle_eczema(query, context)

        # Psoriasis
        elif any(term in query_lower for term in ["psoriasis", "psoriatic", "plaques", "silvery scales"]):
            return self._handle_psoriasis(query, context)

        # Fungal infections
        elif any(term in query_lower for term in ["fungal", "tinea", "ringworm", "athlete's foot", "thrush", "candida", "fungal nail"]):
            return self._handle_fungal(query, context)

        # Viral infections
        elif any(term in query_lower for term in ["warts", "verruca", "herpes", "cold sore", "shingles", "chickenpox", "viral"]):
            return self._handle_viral(query, context)

        # Contact dermatitis and allergy
        elif any(term in query_lower for term in ["contact dermatitis", "allergic rash", "patch test", "nickel", "latex"]):
            return self._handle_contact_dermatitis(query, context)

        # Drug eruptions
        elif any(term in query_lower for term in ["drug eruption", "drug rash", "allergic reaction to medication", "sjs", "ten", "dress"]):
            return self._handle_drug_eruption(query, context)

        # Urticaria and angioedema
        elif any(term in query_lower for term in ["hives", "urticaria", "angioedema", "welts", "swollen lips"]):
            return self._handle_urticaria(query, context)

        # Pediatric rashes
        elif any(term in query_lower for term in ["pediatric rash", "childhood rash", "baby rash", "measles", "rubella"]):
            return self._handle_pediatric_rash(query, context)

        # Bacterial skin infections
        elif any(term in query_lower for term in ["impetigo", "cellulitis", "erysipelas", "abscess", "boil"]):
            return self._handle_bacterial(query, context)

        # Scabies and lice
        elif any(term in query_lower for term in ["scabies", "lice", "head lice", "pubic lice", "itching all over"]):
            return self._handle_ectoparasites(query, context)

        # Hair and nail disorders
        elif any(term in query_lower for term in ["alopecia", "hair loss", "nail", "onychomycosis", "fungal nail"]):
            return self._handle_hair_nail(query, context)

        # Sun protection and photodermatology
        elif any(term in query_lower for term in ["sunscreen", "spf", "sun protection", "photoaging", "sun damage", "actinic"]):
            return self._handle_photoprotection(query, context)

        # General dermatology
        else:
            return self._handle_general_dermatology(query, context)

    def _handle_skin_cancer(self, query: str, context: dict) -> DomainQueryResult:
        """Handle skin cancer and melanoma queries - URGENT REFERRAL PRIORITY"""
        answer = """**SKIN CANCER ASSESSMENT AND MELANOMA RECOGNITION**

**⚠️ URGENT REFERRAL CRITERIA (2-week wait)**
- Suspected melanoma
- Squamous cell carcinoma with high-risk features
- Any lesion rapidly changing, growing, or bleeding

---

**MELANOMA: ABCDE CRITERIA**

**A - Asymmetry**: One half unlike the other
**B - Border**: Irregular, scalloped, or poorly defined
**C - Colour**: Varied from one area to another (shades of tan, brown, black; sometimes white, red, blue)
**D - Diameter**: Usually >6mm (but can be smaller)
**E - Evolving**: Changing in size, shape, colour, elevation, or new symptom (bleeding, crusting, itching)

**"Ugly Duckling" Sign**: Lesion that looks different from patient's other nevi

**High-Risk Features**:
- Thick melanoma (>2mm or >1mm with ulceration)
- Multiple atypical nevi
- Previous melanoma
- Family history of melanoma
- Fair skin, red hair, freckling
- UV exposure (sunbeds, intense sun exposure)

---

**BASAL CELL CARCINOMA (BCC)**

**Typical Features**:
- Pearly or translucent nodule
- Telangiectasia (visible blood vessels)
- Rolled edge with central ulceration ("rodent ulcer")
- Waxing and waning lesion
- Sun-exposed areas (head, neck)

**Subtypes**:
- Nodular BCC (most common)
- Superficial BCC (red scaly plaque)
- Morphoeic BCC (scar-like, ill-defined)

**Management**: Surgical excision (preferred) or radiotherapy

---

**SQUAMOUS CELL CARCINOMA (SCC)**

**Typical Features**:
- Hyperkeratotic or scaly nodule
- Crusting or ulceration
- Rapid growth
- Sun-exposed areas or chronic wounds/scars

**High-Risk SCC** (urgent referral):
- Lip or ear SCC
- >2cm thickness or invasion beyond dermis
- Perineural invasion
- Immunocompromised patient

---

**ACTINIC KERATOSIS (SOLAR KERATOSIS)**

**Features**: Rough, scaly plaques on sun-exposed skin
**Significance**: Pre-malignant, risk progression to SCC (~10% if untreated)
**Management**: Cryotherapy, topical 5-fluorouracil, imiquimod

---

**REFERRAL GUIDELINES (NICE NG12)**

**Urgent 2-Week Wait Referral For**:
- Suspected melanoma (ABCDE criteria or ugly duckling)
- SCC with high-risk features
- Lesion uncertain but could be sarcoma

**Routine Referral For**:
- Low-risk BCC
- Actinic keratosis (if extensive)
- Atypical mole but not suspicious

---

**PHOTOPROTECTION RECOMMENDATIONS**

**Primary Prevention**:
- SPF 30+ (broad spectrum UVA/UVB)
- Apply 15-30 minutes before sun exposure
- Reapply every 2 hours, after swimming/sweating
- Avoid midday sun (11am-3pm)
- Wear protective clothing, hat, sunglasses
- **NEVER use sunbeds**

**Vitamin D Consideration**:
- High SPF may reduce vitamin D synthesis
- Consider supplementation if strict sun avoidance

---

**⚠️ RED FLAGS: IMMEDIATE REFERRAL**

- Rapidly growing lesion (<8 weeks)
- Bleeding or ulceration without trauma
- Pigmented lesion with ABCDE features
- New nodule in elderly patient
- Lesion not healing after 4-6 weeks

**Sources: BAD Melanoma Guidelines 2022, NICE NG12, AAD Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "dermatology",
                "focus": "skin_cancer_melanoma",
                "urgency": "high_priority_referral",
                "sources": ["BAD Melanoma Guidelines 2022", "NICE NG12", "AAD Guidelines"]
            }
        )

    def _handle_rash_pattern(self, query: str, context: dict) -> DomainQueryResult:
        """Handle rash pattern recognition by morphology and distribution"""
        answer = """**RASH PATTERN RECOGNITION BY MORPHOLOGY**

**STEP 1: DESCRIBE THE RASH (Morphology)**

**Macule**: Flat, coloured spot (<1cm)
**Patch**: Flat, coloured spot (>1cm)
**Papule**: Solid raised spot (<1cm)
**Plaque**: Solid raised spot (>1cm)
**Nodule**: Solid, deeper lesion (>1cm)
**Vesicle**: Fluid-filled blister (<5mm)
**Bulla**: Fluid-filled blister (>5mm)
**Pustule**: Pus-filled blister
**Wheal**: Transient, itchy, oedematous plaque (urticaria)
**Scale**: Flaky skin
**Crust**: Dried serum or exudate
**Erosion**: Loss of epidermis (heals without scar)
**Ulcer**: Loss of epidermis and dermis (heals with scar)
**Excoriation**: Scratch mark
**Lichenification**: Thickened skin with accentuated markings (chronic rubbing)
**Atrophy**: Thin, translucent skin (loss of dermis)

---

**STEP 2: DISTRIBUTION PATTERN**

**Distribution Clues to Diagnosis**:

**Flexural (skin folds)**: Atopic eczema, flexural psoriasis, intertrigo
**Extensor**: Psoriasis, discoid eczema
**Trunk**: Tinea versicolor, pityriasis rosea, drug eruptions
**Face + scalp**: Seborrhoeic dermatitis, acne rosacea
**Hands and feet**: Dermatitis, psoriasis, scabies
**Sun-exposed**: Photodermatitis, LE, actinic keratosis
**Dermatomal**: Herpes zoster
**Linear**: Contact dermatitis (external allergen), scabies burrows

---

**STEP 3: COMMON MORPHOLOGICAL PATTERNS**

**Maculopapular Rash**:
- Macules + papules
- **Differential**: Viral exanthem (measles, rubella), drug eruption, meningococcal sepsis, guttate psoriasis, secondary syphilis

**Vesiculobullous Rash**:
- Vesicles/bullae
- **Differential**: Herpes simplex/zoster, varicella, pemphigus, pemphigoid, eczema herpeticum, bullous impetigo, contact dermatitis

**Erythroderma**:
- Widespread redness affecting >90% body surface area
- **Causes**: Eczema, psoriasis, drug reaction, CTCL, sepsis
- **EMERGENCY**: Admit for temperature/fluid management

**Purpura**:
- Non-blanching (doesn't fade with pressure)
- **Petechiae** (<3mm), **Purpura** (3mm-1cm), **Ecchymosis** (>1cm, bruise)
- **Differential**: Meningococcal sepsis (URGENT), vasculitis, ITP, trauma, disseminated intravascular coagulation

**Nodular Rash**:
- Deep, solid lesions
- **Differential**: Erythema nodosum (shins, painful), sarcoidosis, lymphoma, metastatic cancer

**Urticarial Rash**:
- Wheals, transient, itchy, blanches with pressure
- **Differential**: Urticaria (allergic), anaphylaxis, serum sickness, autoimmune

**Scaly Rash**:
- **Silvery scales**: Psoriasis
- **Yellow, greasy**: Seborrhoeic dermatitis
- **Fine, white**: Atopic eczema
- **Annular (ring-shaped)**: Tinea corporis, annular psoriasis, granuloma annulare

---

**STEP 4: ITCH (PRURITUS) ASSESSMENT**

**Severe Itch Suggests**:
- Scabies (worse at night, burrows in finger webs)
- Eczema
- Urticaria
- Lichen planus (violaceous flat-topped papules)

**Minimal Itch Suggests**:
- Psoriasis (usually mild or absent)
- Fungal infections (mild)
- Drug eruptions (variable)

---

**RED FLAGS: URGENT REFERRAL**

**Meningococcal Meningitis/Sepsis**:
- Non-blanching purpuric rash
- Fever, headache, neck stiffness, altered mental status
- **IMMEDIATE EMERGENCY**

**Erythroderma** (>90% BSA involvement):
- Risk of hypothermia, fluid loss, sepsis
- **ADMIT**

**Stevens-Johnson Syndrome / TEN**:
- Widespread bullous eruption, mucosal involvement
- **ADMIT TO BURNS UNIT**

**Necrotizing Fasciitis**:
- Pain out of proportion, swelling, crepitus, sepsis
- **IMMEDIATE SURGICAL EMERGENCY**

---

**CLINICAL APPROACH TO RASH**

1. **Full skin examination** (including scalp, nails, mucosa)
2. **Document morphology** (use terminology above)
3. **Map distribution** (draw body map or photograph)
4. **Assess systemic symptoms** (fever, malaise, joint pain)
5. **Medication history** (drug eruptions)
6. **Timeline** (acute vs chronic, progression)
7. **Exposure history** (contacts, travel, allergens, sun)

**Sources: NICE Dermatology Guidelines, PCDS Handbook, BAD Dermatology Handbook**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "dermatology",
                "focus": "rash_pattern_recognition",
                "sources": ["NICE Dermatology Guidelines", "PCDS Handbook", "BAD Dermatology Handbook"]
            }
        )

    def _handle_acne_rosacea(self, query: str, context: dict) -> DomainQueryResult:
        """Handle acne and rosacea management"""
        answer = """**ACNE VULGARIS AND ROSACEA MANAGEMENT**

---

## ACNE VULGARIS

**Pathogenesis**: Follicular hyperkeratinization, sebum overproduction, *Cutibacterium acnes*, inflammation

**Grading Severity**:
- **Mild**: Open/closed comedones (blackheads/whiteheads) ± few papules/pustules
- **Moderate**: Multiple papules/pustules, some nodules
- **Severe**: Numerous nodulocystic lesions, scarring risk

**Treatment by Severity**:

**MILD ACNE (Comedonal)**:
1. **Benzoyl Peroxide 2.5-5%** (once daily, morning)
   - Antimicrobial, comedolytic, reduces antibiotic resistance
   - Side effects: Irritation, bleaching of clothes

2. **Topical Retinoid** (Adapalene 0.1% or Tretinoin 0.025%)
   - Applied at night (comedolytic, prevents microcomedones)
   - Use with moisturiser, may cause initial flare

3. **Azelaic Acid 15-20%** (BID)
   - Alternative if BP/retinoid not tolerated
   - Anti-inflammatory, comedolytic

**MODERATE ACNE (Inflammatory)**:
1. **Combination Therapy**:
   - Benzoyl peroxide + topical retinoid
   - OR Benzoyl peroxide + topical antibiotic (erythromycin/clindamycin)
   - **NEVER use topical antibiotic alone** (resistance risk)

2. **Oral Antibiotics** (if inadequate topical response):
   - **Doxycycline 100mg OD** (or lymecycline 408mg OD)
   - **Minocycline 100mg OD** (if doxycycline intolerance)
   - Always combine with BP (prevents resistance)
   - Duration: 3-6 months, then review
   - Cautions: Photosensitivity (doxycycline), vestibular side effects (minocycline)

**SEVERE ACNE (Nodulocystic)**:
1. **Oral Isotretinoin** (Referral to dermatology)
   - Indication: Severe nodulocystic acne, scarring, psychological distress
   - Dose: 0.5-1.0 mg/kg/day
   - Duration: Usually 16-24 weeks (cumulative dose 120-150 mg/kg)
   - **MUST avoid pregnancy** (teratogenic - pregnancy prevention program)
   - Side effects: Dryness, mucosal dryness, mood changes (rare), raised lipids/LFTs

---

**ACNE MANAGEMENT TIPS**:
- Wash face twice daily with gentle cleanser (avoid scrubbing)
- Use non-comedogenic moisturiser and sunscreen
- **DO NOT squeeze spots** (risk of scarring)
- Counsel on treatment timeline: **6-8 weeks for improvement**
- Maintain treatment for 6-12 months after clearance
- Manage expectations: 70-80% improvement is good response

---

## ROSACEA

**Chronic facial flushing disorder** (NOT acne)

**Subtypes**:
1. **Erythematotelangiectatic**: Flushing, persistent erythema, telangiectasia
2. **Papulopustular**: Acne-like lesions (but NO comedones)
3. **Phymatous**: Rhinophyma (thickened nose tissue), skin thickening
4. **Ocular**: Blepharitis, conjunctivitis, dry/gritty eyes

**Triggers to Avoid**:
- Hot drinks, alcohol (especially red wine)
- Spicy foods, sunlight, heat
- Emotional stress, exercise
- Topical steroids (can cause steroid-induced rosacea)

**Management**:

**Erythematotelangiectatic Rosacea**:
- **Topical Brimonidine 0.33% gel** (OD for transient erythema)
- **Topical Oxymetazoline 1% cream** (similar)
- **Laser/IPL** for telangiectasia (dermatology referral)

**Papulopustular Rosacea**:
1. **First-line**:
   - Topical ivermectin 1% cream (OD) OR metronidazole 0.75% gel (BID)
   - Duration: 2-4 months for effect

2. **Moderate-Severe**:
   - **Doxycycline 40mg MR (anti-inflammatory dose)** OR 100mg OD
   - OR **Isotretinoin** (low-dose, refractory cases)

**Ocular Rosacea**:
- Oral doxycycline (anti-inflammatory dose)
- Ophthalmology referral if severe
- Eyelid hygiene, artificial tears

**Phymatous Rosacea**:
- Surgical referral (dermatology/plastic surgery)
- Laser or surgical debulking

---

**PERIORAL DERMATITIS** (Rosacea variant)

**Presentation**: Red papules around mouth, nasolabial folds
**Cause**: Often from topical steroid use
**Management**:
- STOP topical steroids (may flare initially)
- Topical metronidazole OR oral doxycycline
- Emollients only for dryness

---

**ACNE EXCORIÉE**:

**Definition**: Picking at acne lesions, excoriations
**Approach**: Psychological support, treat underlying acne, consider SSRI

---

**Sources**: NICE NG198 Acne Management, BAD Acne Guidelines 2023, ROSCOA Rosacea Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "dermatology",
                "focus": "acne_rosacea",
                "sources": ["NICE NG198", "BAD Acne Guidelines 2023", "ROSCOA Rosacea Guidelines"]
            }
        )

    def _handle_eczema(self, query: str, context: dict) -> DomainQueryResult:
        """Handle eczema and dermatitis management"""
        answer = """**ECZEMA AND DERMATITIS MANAGEMENT**

---

## ATOPIC ECZEMA (ATOPIC DERMATITIS)

**Pathogenesis**: Skin barrier dysfunction (filaggrin mutation), immune dysregulation, IgE-mediated

**Diagnostic Criteria (UK Working Party)**:
- Itchy skin condition (PLUS 3+ of following):
  1. History of flexural involvement (elbow/knee creases, ankles, neck)
  2. Personal history of asthma/hay fever (or first-degree relative)
  3. History of dry skin in last year
  4. Onset <2 years old (not used if child <4)
  5. Visible flexural eczema

**Severity Grading**:
- **Mild**: Small areas, minimal sleep disturbance
- **Moderate**: Larger areas, frequent flares, sleep disturbance
- **Severe**: Widespread, constant flares, severe sleep disturbance, poor QoL

**Management**:

**1. EMOLLIENTS (Cornerstone of Therapy)**:
- Apply **liberally and frequently** (at least 2-3 times daily)
- **50:50 mix**: 50% ointment + 50% cream (for ease of use)
- Use 250-500g per week (adults), 125-250g (children)
- **Soap substitute**: Emollient instead of soap for washing
- **Bath additives**: Emollient oil in bath water
- Pump dispensers (less contamination than jars)
- **Choose patient preference** (improves adherence)

**2. TOPICAL STEROIDS** (Inflammation Control):

| Severity | Steroid Potency | Adult | Child |
|----------|----------------|-------|-------|
| Mild | Hydrocortisone 1% | Face/neck | Face/neck |
| Moderate | Potent (e.g., Mometasone, Betamethasone) | Body/trunk | Body only (avoid face) |
| Severe | Very potent (e.g., Clobetasol) | Short-term only | AVOID |

**Topical Steroid Rules**:
- Apply **thin layer** (fingertip unit: FTU = 0.5g)
- **Once daily** is as effective as BID (less systemic absorption)
- **Step down** as improves (reduce potency then frequency)
- **2 weeks continuous**, then 1-week break, then repeat if needed
- **Safe for face with mild potency** (hydrocortisone 1%)
- **Do NOT fear steroids** - undertreatment causes more harm

**3. FLARE MANAGEMENT**:
- **Steroid burst**: Potent steroid BID for 3-7 days during flare
- Maintain emollients during and after flare
- Identify and avoid triggers (stress, irritants, allergens)

**4. SECOND-LINE** (if inadequate response):
- **Calcineurin inhibitors**: Tacrolimus 0.03%/0.1% OD or BID (face/sensitive areas)
- **Wet wraps**: For severe flares (apply damp tubular bandage over emollient + steroid)
- **Phototherapy**: UVB or PUVA (dermatology referral)
- **Systemic immunosuppressants**: Ciclosporin, methotrexate, azathioprine (specialist only)

**5. COMPLICATIONS**:

**Eczema Herpeticum** (EMERGENCY):
- Widespread painful vesicles, fever, unwell
- **Urgent referral** (IV aciclovir)

**Bacterial Infection**:
- Staphylococcus aureus common (crusting, weeping, honey-coloured crusts)
- Oral flucloxacillin 500mg QDS (or clarithromycin if penicillin allergy)
- Topical antibiotics NOT recommended (resistance)

**Antihistamines**:
- **Sedating** (chlorphenamine 4mg QID) for sleep disturbance
- **Non-sedating** (cetirizine, loratadine) NOT effective for itch (but safe)

---

## OTHER ECZEMA SUBTYPES

**DISCOID ECZEMA** (Nummular):
- Coin-shaped lesions on limbs (extensor surfaces)
- Often confused with psoriasis or tinea
- Management: Potent topical steroid + emollient

**SEBORRHOEIC DERMATITIS**:
- **Distribution**: Scalp (dandruff), eyebrows, nasolabial folds, ears, chest
- **Cause**: *Malassezia yeast* overgrowth (NOT dry skin)
- **Scalp**: Ketoconazole 2% shampoo (twice weekly), coal tar shampoo
- **Face**: Ketoconazole 2% cream OR mild hydrocortisone 1% (short-term)
- **Chronic**: Often requires long-term maintenance

**IRRITANT CONTACT DERMATITIS**:
- **Causes**: Detergents, solvents, water, friction, wet work
- **Occupational**: Healthcare workers (hand washing), hairdressers, cleaners
- **Management**: Avoid irritant, emollients, barrier creams, gloves

**ALLERGIC CONTACT DERMATITIS**:
- **Type IV hypersensitivity** to allergen (nickel, fragrance, preservatives)
- **Patch testing** to identify allergen (dermatology referral)
- **Common allergens**: Nickel (jewelry), fragrance, preservatives, rubber accelerators
- **Management**: Avoid allergen, topical steroids during flares

**VENOUS ECZEMA** (Stasis Dermatitis):
- **Distribution**: Lower legs, associated with venous insufficiency
- **Management**: Compression stockings, emollients, mild topical steroid
- **Caution**: Exclude arterial disease before compression (ABPI)

**ASTEATOTIC ECZEMA** (Dry Skin):
- "Crazy-paving" appearance on shins in elderly
- **Cause**: Dry environment, excessive washing, aging
- **Management**: Emollients (ointment-based), avoid soap, humidifier

---

**EMOLLIENT AND STEROID CHART**

| Age | Emollient (daily) | Mild Steroid | Potent Steroid |
|-----|-------------------|--------------|----------------|
| Baby | 125g | Hydrocortisone 1% (face) | Hydrocortisone 1% (body) |
| Child | 125-250g | Hydrocortisone 1% | Mometasone (body) |
| Adult | 250-500g | Hydrocectisone 1% | Mometasone/Betamethasone |

**Sources: NICE NG57 Atopic Eczema, BAD Atopic Eczema Guidelines 2021, PCDS**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "dermatology",
                "focus": "eczema_dermatitis",
                "sources": ["NICE NG57", "BAD Atopic Eczema Guidelines 2021", "PCDS"]
            }
        )

    def _handle_psoriasis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle psoriasis management"""
        answer = """**PSORIASIS MANAGEMENT**

---

## PSORIASIS VULGARIS (CHRONIC PLAQUE PSORIASIS)

**Pathogenesis**: Autoimmune, IL-17/IL-23 driven, genetic predisposition (HLA-Cw6), Koebner phenomenon (trauma induces new lesions)

**Typical Features**:
- Well-demarcated erythematous plaques
- Overlying silvery scales
- Symmetrical distribution
- Extensor surfaces (elbows, knees), scalp, lumbosacral area
- Nail changes: pitting, onycholysis, oil spots

**Severity Assessment**:
- **Mild**: <5% body surface area (BSA) involvement
- **Moderate**: 5-10% BSA
- **Severe**: >10% BSA OR involvement of sensitive areas (face, hands, feet, genitals) OR significant QoL impact

**BSA Estimation**:
- Hand (including fingers) ≈ 1% BSA
- Head ≈ 4%, each arm ≈ 4%, each leg ≈ 8%, trunk ≈ 36%

**Management**:

**MILD PSORIASIS (<5% BSA)**:

**1. Topical Corticosteroids** (first-line):
- **Scalp**: Potent steroid scalp application (e.g., betamethasone valerate lotion)
- **Body**: Potent steroid ointment (once daily, 4 weeks maximum)
- **Face/flexures**: Mild steroid (hydrocortisone 1%) or calcineurin inhibitor

**2. Vitamin D Analogues**:
- **Calcipotriol** (once or twice daily)
- **Calcitriol** (twice daily)
- Avoid on face/flexures (irritation risk)
- **Combination**: Calcipotriol/betamethasone ointment (more effective than either alone)

**3. Coal Tar**:
- Crude coal tar 1-10% (in cream or ointment base)
- Anti-inflammatory, keratolytic
- Issues: Messy, odour, staining

**4. Salicylic Acid** (keratolytic):
- 2-10% in ointment (removes scale)
- Allows better penetration of other agents

**5. Emollients** (adjunct):
- Regular use reduces scale and improves comfort

---

**MODERATE-SEVERE PSORIASIS (>5% BSA)**:

**PHOTOTHERAPY** (Second-line):
- **UVB** (narrowband UVB 311nm): 2-3 times weekly, clearance in ~20 treatments
- **PUVA** (psoralen + UVA): More effective but higher long-term cancer risk
- **Contraindications**: Photosensitivity, pregnancy, immunosuppression

**SYSTEMIC THERAPY** (Second/third-line):

**Methotrexate** (First-choice systemic):
- Dose: 10-25mg weekly (oral or SC)
- Folic acid 5mg weekly (6 days after MTX dose)
- Monitoring: FBC, U&E, LFTs, CRP (baseline, then weekly x4, then monthly)
- Contraindications: Pregnancy, liver disease, alcohol excess
- Side effects: Myelosuppression, hepatotoxicity, pneumonitis (rare)

**Ciclosporin**:
- Dose: 2.5-5mg/kg/day in divided doses
- Rapid onset (benefit in 3-4 weeks)
- Hypertension, renal impairment (monitor BP and U&E)
- Contraindicated with PUVA (increased SCC risk)

**Acitretin** (Oral retinoid):
- Dose: 25-50mg daily
- Effective for pustular psoriasis
- Teratogenic (avoid pregnancy for 2 years after stopping)
- Side effects: Mucocutaneous dryness, hyperlipidaemia, hepatotoxicity

**BIOLOGICS** (Third-line, dermatology initiation):
- **Anti-TNF**: Etanercept, Adalimumab, Infliximab
- **Anti-IL12/23**: Ustekinumab
- **Anti-IL17**: Secukinumab, Ixekizumab
- **Anti-IL23**: Guselkumab, Risankizumab
- Screening for TB, hepatitis B/C before initiation

---

**PSORIATIC ARTHRITIS**:
- Affects ~30% of psoriasis patients
- **Patterns**: Asymmetric oligoarthritis, symmetric polyarthritis (RA-like), DIP joint involvement, spondylitis, arthritis mutilans
- **Screen**: Ask about joint pain, stiffness, swelling, back pain
- **Management**: NSAIDs, DMARDs (methotrexate), biologics (rheumatology referral)

---

**SCALP PSORIASIS**:
- Common, distressing, difficult to treat
- **First-line**: Potent steroid scalp lotion + coconut oil compound (to soften scale)
- **Second-line**: Vitamin D analogue scalp lotion
- **Third-line**: Coal tar shampoo (messy)
- **Severe**: Phototherapy (UVB comb) or systemic therapy

---

**NAIL PSORIASIS**:
- Pitting, onycholysis, oil spots, subungual hyperkeratosis
- Difficult to treat (topicals penetrate poorly)
- **Intralesional steroid** injection (triamcinolone) for severe cases
- Systemic therapy for extensive disease

---

**GUTTATE PSORIASIS**:
- Acute onset, numerous small teardrop-shaped plaques
- Usually post-streptococcal infection (2-3 weeks after)
- **Children and young adults**
- **Management**: Emollients ± topical steroid (often self-limiting, 50% resolve)
- **Consider**: Oral antibiotics if evidence of streptococcal infection
- **Progression**: 30-40% develop chronic plaque psoriasis

---

**OTHER PSORIASIS SUBTYPES**:

**Pustular Psoriasis**:
- **Generalized**: Fever, widespread pustules, systemic upset (ADMIT)
- **Palmoplantar**: Pustules on palms/soles (disabling)

**Erythrodermic Psoriasis**:
- Widespread redness affecting >90% BSA
- Temperature regulation impaired, risk of hypothermia
- **ADMIT**

---

**COMORBIDITIES** (Psoriasis as systemic inflammatory disease):
- Metabolic syndrome (obesity, diabetes, hypertension)
- Cardiovascular disease (increased MI risk)
- Psoriatic arthritis
- Depression, anxiety
- **Screen**: BMI, BP, fasting glucose, lipids, joint examination

---

**Sources: NICE NG153 Psoriasis, BAD Psoriasis Guidelines 2021, BSR Psoriatic Arthritis Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "dermatology",
                "focus": "psoriasis",
                "sources": ["NICE NG153", "BAD Psoriasis Guidelines 2021", "BSR Psoriatic Arthritis Guidelines"]
            }
        )

    def _handle_fungal(self, query: str, context: dict) -> DomainQueryResult:
        """Handle fungal skin infections"""
        answer = """**FUNGAL SKIN INFECTIONS (SUPERFICIAL MYCOSES)**

---

## DERMATOPHYTOSIS (TINEA INFECTIONS)

Caused by dermatophyte fungi: *Trichophyton*, *Microsporum*, *Epidermophyton*

---

**TINEA PEDIS** (Athlete's Foot)

**Patterns**:
1. **Interdigital**: Moist, macerated, scaling between toes (most common)
2. **Moccasin type**: Dry, diffuse scaling on soles, heels
3. **Vesiculobullous**: Vesicles, bullae on soles (inflammatory)

**Treatment**:
- **First-line**: Topical terbinafine 1% cream BID for 1-2 weeks
- **Alternative**: Topical azoles (clotrimazole, miconazole, ketoconazole)
- **Severe/chronic**: Oral terbinafine 250mg daily for 2-4 weeks
- **Adjunct**: Dry feet thoroughly, absorbent socks, rotate shoes, avoid occlusive footwear

---

**TINEA CRURIS** (Jock Itch)

**Presentation**: Red, itchy, scaling plaques in groin (may spread to thighs, buttocks)
**Risk Factors**: Men, occlusive clothing, obesity, excessive sweating
**Treatment**:
- Topical terbinafine or azole BID for 1-2 weeks
- Dry area thoroughly, loose clothing, cotton underwear
- **Tip**: Treat concomitant tinea pedis (often source of reinfection)

---

**TINEA CORPORIS** (Ringworm)

**Presentation**: Annular (ring-shaped) plaque with active, scaly, advancing border and central clearing
**Differential**: Annular psoriasis, granuloma annulare, nummular eczema
**Treatment**:
- Topical terbinafine or azole BID for 1-2 weeks
- **Extensive**: Oral terbinafine 250mg daily for 2-4 weeks

---

**TINEA CAPITIS** (Scalp Ringworm)

**Pathogens**: *Trichophyton tonsurans* (most common), *Microsporum canis* (from cats/dogs)
**Presentation**:
- Patchy alopecia with scale, erythema
- Black dot tinea (broken hairs at scalp surface)
- Kerion (inflammatory mass with pus, may scar alopecia)
- **Wood's light**: *M. canis* fluoresces green, *T. tonsurans* does NOT

**Treatment**:
- **Oral terbinafine** (weight-based dosing) for 4-6 weeks
- **Alternative**: Oral griseofulvin (traditional)
- **Adjunct**: Antifungal shampoo (ketoconazole 2% or selenium sulfide) twice weekly
- **Do NOT use topical alone** (ineffective for hair follicle infection)

**School Exclusion**: No exclusion once treatment started

---

**TINEA UNGUIUM** (Fungal Nail Infection / Onychomycosis)

**Presentation**:
- Distal onycholysis (nail lifting from nail bed)
- Subungual hyperkeratosis (debris under nail)
- Nail thickening, discolouration (yellow-white, brown)
- Brittle, crumbly nail

**Diagnosis**:
- Clinical appearance
- **Confirm**: Nail clipping microscopy + culture (to exclude other conditions)

**Treatment**:
- **Oral terbinafine 250mg daily** for 6 weeks (fingernails) or 12 weeks (toenails)
- **Alternative**: Oral itraconazole (pulse therapy)
- **Topical**: Amorolfine or ciclopirox nail lacquer (for mild disease or contraindications to oral)
- **Adjunct**: Debride nail, keep short

**Cautions**:
- Check LFTs baseline and at 4-6 weeks (terbinafine)
- Contraindicated in severe liver disease
- Drug interactions (itraconazole more than terbinafine)

---

**TINEA VERSICOLOR** (Pityriasis Versicolor)

**Pathogen**: *Malassezia furfur* (yeast, not dermatophyte)
**Presentation**:
- Multiple, small, hypo- or hyperpigmented macules
- Fine scale
- Upper trunk, neck, shoulders
- **Wood's light**: Yellow-green fluorescence

**Treatment**:
- **Topical**: Ketoconazole 2% shampoo (apply to affected areas, leave 10 min, wash off - daily for 5 days)
- **Alternative**: Selenium sulfide 2.5% lotion
- **Oral**: Single-dose oral itraquinazole 400mg (extensive disease)

**Prognosis**: Good, but high recurrence rate

---

## CANDIDIASIS (YEAST INFECTION)

**Pathogen**: *Candida albicans*

**Cutaneous Candidiasis**:
- **Intertriginous**: Moist, red, satellite lesions in skin folds
- **Perineal**: Napkin dermatitis in infants (bright red, satellite lesions)
- **Paronychia**: Chronic nail fold inflammation

**Treatment**:
- **Mild**: Topical azole (clotrimazole, miconazole, ketoconazole) BID for 1-2 weeks
- **Severe**: Oral fluconazole 150mg (single dose or 100-200mg daily for 1-2 weeks)

**Oral Candidiasis** (Thrush):
- **Pseudomembranous**: White plaques on oral mucosa (wipes off leaving erythema)
- **Erythematous**: Red, atrophic patches
- **Angular cheilitis**: Red, fissured mouth corners

**Treatment**:
- Topical nystatin suspension (100,000 U/mL, 1mL QID, swallow after) OR miconazole gel
- **Fluconazole 50-100mg daily** (severe, recurrent)

**Risk Factors**: Diabetes, antibiotics, immunosuppression, dentures

**Chronic Mucocutaneous Candidiasis**:
- Recurrent, persistent candidiasis
- **Screen for HIV, diabetes, immunosuppression**

---

## PITYRIASIS VERSICOLOR
*(covered above under Tinea Versicolor)*

---

## KEY POINTS

**Diagnosis**:
- Skin scraping for microscopy (KOH prep) - hyphae seen in dermatophytes, spores in *Malassezia*
- Culture confirmation
- Nail clippings for onychomycosis

**Prevention of Recurrence**:
- Dry skin thoroughly (especially between toes, skin folds)
- Absorbent socks, change daily
- Loose, breathable clothing
- Treat all affected sites simultaneously (e.g., feet + groin)
- Avoid sharing towels, footwear
- Disinfect footwear (antifungal powder or spray)

**Sources**: BAD Fungal Skin Infection Guidelines, NICE Clinical Knowledge Summaries**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "dermatology",
                "focus": "fungal_infections",
                "sources": ["BAD Fungal Skin Infection Guidelines", "NICE CKS"]
            }
        )

    def _handle_viral(self, query: str, context: dict) -> DomainQueryResult:
        """Handle viral skin infections"""
        answer = """**VIRAL SKIN INFECTIONS**

---

## HERPES SIMPLEX INFECTIONS

**Primary Infection**:
- **Herpes Labialis** (Cold sores, HSV-1): Painful vesicles on lips, perioral area
- **Herpes Genitalis** (HSV-2 or HSV-1): Vesicles, ulcers, dysuria, systemic symptoms

**Recurrent Infection**:
- Prodrome (tingling, burning) 24-48 hours before lesions
- Vesicles → pustules → ulcers → crusting (7-10 days)
- Triggers: Stress, sunlight, illness, immunosuppression, menstruation

**Management**:

**Topical (mild disease)**:
- Aciclovir 5% cream: Apply 5 times daily for 5 days (most effective if applied during prodrome)

**Oral (moderate-severe, frequent recurrences)**:
- **Aciclovir 400mg TDS** for 5 days (400mg TDS for 5-10 days if severe)
- **Valaciclovir 500mg BD** for 5 days (more convenient dosing)

**Suppression** (if ≥6 recurrences/year):
- **Aciclovir 400mg BD** (long-term)
- **Valaciclovir 500mg OD** (long-term)
- Review after 6-12 months (consider stopping)

**Patient Advice**:
- Avoid kissing, oral sex during active lesions
- Do not share towels, cutlery, lip products
- Avoid touching eyes (herpetic keratitis risk)
- Sun protection (UV can trigger recurrences)

---

## HERPES ZOSTER (SHINGLES)

**Pathogenesis**: Reactivation of varicella-zoster virus (VZV) from dorsal root ganglia

**Clinical Features**:
- **Prodrome**: Pain, tingling, burning (dermatomal distribution, 1-5 days before rash)
- **Rash**: Unilateral vesicles in dermatomal distribution (does NOT cross midline)
- **Common sites**: Thoracic (most common), trigeminal (ophthalmic zoster), lumbar, sacral
- **Systemic**: Fever, malaise, headache

**Complications**:
- **Postherpetic Neuralgia (PHN)**: Pain persisting >90 days after rash onset (risk increases with age)
- **Ophthalmic Zoster**: If V1 branch of trigeminal nerve involved → **URGENT ophthalmology referral**
- **Motor zoster**: Weakness in affected myotome
- **Disseminated zoster**: Widespread lesions (immunocompromised)

**Management**:

**Antiviral Therapy** (start within 72 hours of rash onset):
- **Aciclovir 800mg 5 times daily** for 7 days
- **Valaciclovir 1g TDS** for 7 days (more convenient)
- **Famciclovir 500mg TDS** for 7 days
- **Indications**: Age >50, severe pain, immunocompromised, ophthalmic involvement

**Pain Management**:
- **Paracetamol + NSAID** for mild-moderate pain
- **Neuropathic agents**: Amitriptyline 10-25mg nocte OR gabapentin/pregabalin (severe pain, PHN)
- **Consider**: Lidocaine 5% patch for localized pain

**Prevention**:
- **Shingles vaccine (HZ/su or Shingrix)**: Recommended for age 70-79 (UK), 50+ (some countries)
- **Contraindicated in immunosuppression**

**Advice**:
- Contagious (causes chickenpox in non-immune contacts)
- Avoid contact with pregnant women, neonates, immunocompromised
- Cover lesions, avoid sharing towels

---

## VERRUCAE (WARTS)

**Pathogen**: Human papillomavirus (HPV), various types

**VERRUCA VULGARIS** (Common Wart):
- **Location**: Fingers, hands, knees
- **Appearance**: Dome-shaped, hyperkeratotic papule, may have black dots (thrombosed capillaries)

**PLANTAR WART (Verruca)**:
- **Location**: Soles of feet (pressure points)
- **Appearance**: Flat, hyperkeratotic, painful on walking, black dots

**PLANE WARTS**:
- **Location**: Face, hands, legs
- **Appearance**: Flat-topped, flesh-coloured, multiple

**ANOGENITAL WARTS** (Condylomata acuminata):
- **Location**: Penis, vulva, perineum, perianal
- **Pathogen**: HPV types 6, 11 (low oncogenic risk)
- **Screen for high-risk HPV types** (persistent warts, consider STI screen)

**Treatment** (none is definitively superior):

**First-line**:
1. **Salicylic acid** (15-50%): Apply daily, debride weekly (6-12 weeks)
2. **Cryotherapy** (liquid nitrogen): Every 2-3 weeks (may be painful)

**Second-line** (referral to dermatology):
- **Podophyllotoxin** (for anogenital warts)
- **Imiquimod** (immune response modifier)
- **Diphencyprone** (contact immunotherapy)
- **Laser ablation**
- **Surgical excision**

**Expectations**:
- **50% resolve spontaneously within 1 year** (especially in children)
- Treatment accelerates resolution but not guaranteed

---

## MOLLUSCUM CONTAGIOSUM

**Pathogen**: Molluscum contagiosum virus (poxvirus)

**Appearance**:
- Small, flesh-coloured papules with central umbilication (dell)
- **Pearl-like** appearance
- Usually 2-6mm, but can be larger

**Distribution**:
- Children: Trunk, axillae, popliteal fossae
- Adults: Genital, lower abdomen (sexually transmitted)

**Course**: Self-limiting, usually resolves in 6-18 months

**Treatment** (not always necessary):
- **Observation** (first-line, especially in children)
- **Curettage** (mechanical removal)
- **Cryotherapy**
- **Imiquimod** (off-label)

**Advice**:
- Avoid sharing towels
- Cover with plaster if swimming (reduce transmission)

---

## VIRAL EXANTHEMS

**CHICKENPOX (Varicella)**:
- **Pathogen**: Varicella-zoster virus (primary infection)
- **Incubation**: 10-21 days
- **Infectious**: 2 days before rash until all lesions crusted
- **Rash**: Crops of vesicles at different stages (macule → papule → vesicle → pustule → crust)
- **Management**: Supportive, calamine, oral aciclovir if within 24h and immunocompromised
- **Exclusion**: Until all lesions crusted (usually 5-7 days)

**HAND, FOOT, AND MOUTH DISEASE**:
- **Pathogen**: Coxsackievirus A16, enterovirus 71
- **Rash**: Vesicles on palms, soles, buttocks, oral ulcers
- **Age**: Children <10
- **Management**: Supportive, analgesia for oral ulcers

**MEASLES** (Morbilli):
- **Pathogen**: Measles virus (paramyxovirus)
- **Prodrome**: Fever, cough, coryza, conjunctivitis (3 days)
- **Koplik spots**: White spots on buccal mucosa (pathognomonic)
- **Rash**: Maculopapular, starts head/neck, descends, becomes confluent
- **Complications**: Pneumonia, encephalitis, SSPE
- **Notify**: Notifiable disease

**RUBELLA** (German Measles):
- **Pathogen**: Rubella virus
- **Rash**: Pink maculopapular, starts face, descends, 2-3 days
- **Lymphadenopathy**: Post-auricular, suboccipital
- **Importance**: Teratogenic in pregnancy (congenital rubella syndrome)

**Sources**: NICE Clinical Knowledge Summaries, BAD Viral Skin Infection Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "dermatology",
                "focus": "viral_infections",
                "sources": ["NICE CKS", "BAD Viral Skin Infection Guidelines"]
            }
        )

    def _handle_contact_dermatitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle contact dermatitis"""
        answer = """**CONTACT DERMATITIS**

---

## IRRITANT CONTACT DERMATITIS (ICD)

**Pathogenesis**: Non-immune inflammatory response to direct skin damage from irritant

**Common Irritants**:
- **Water** (wet work: healthcare workers, hairdressers, cleaners)
- **Detergents** (soaps, shampoos, dishwashing liquids)
- **Solvents** (alcohol, acetone, degreasers)
- **Fragrances**, preservatives, disinfectants
- **Friction**, heat, sweat, dust

**Clinical Features**:
- Dry, red, scaly plaques
- **Sharp demarcation** at area of contact with irritant
- Hands most commonly affected (interdigital webs, dorsal hands)
- Painful fissuring, hyperkeratosis (chronic)

**Management**:

**1. Avoid/Reduce Irritant Exposure**:
- Minimize wet work (use gloves)
- Use soap substitutes
- Pat dry (do not rub)
- Emollients frequently

**2. Barrier Protection**:
- **Gloves**: Cotton-lined rubber/vinyl gloves for wet work
- **Barrier creams**: May help but NOT substitute for gloves

**3. Treatment**:
- **Emollients**: Liberal application (2-3x daily)
- **Topical steroids**: During flares (potent on body, mild on face/flexures)
- **Review occupation**: If work-related, occupational health referral

---

## ALLERGIC CONTACT DERMATITIS (ACD)

**Pathogenesis**: Type IV delayed-type hypersensitivity (T-cell mediated)

**Clinical Features**:
- Pruritic, eczematous plaque at site of allergen contact
- **Spreads beyond area of contact** (unlike ICD)
- Onset 24-72 hours after exposure

**Common Allergens**:

**1. Nickel**:
- **Most common allergen**
- **Sources**: Jewelry (earrings, watches, belt buckles), jeans buttons, keys, coins
- **Distribution**: Earlobes, wrist, waistline

**2. Fragrance Mix**:
- **Sources**: Perfumes, cosmetics, soaps, moisturizers, fragranced products
- **Distribution**: Face, neck, axillae

**3. Fragrance Mix II**:
- **Sources**: Similar to above, additional fragrances

**4. Myroxylon pereirae (Balsam of Peru)**:
- **Sources**: Perfumes, cough mixtures, hemorrhoid preparations, certain foods (cinnamon, vanilla, tomatoes, citrus)

**5. Colophony (Rosin)**:
- **Sources**: Adhesives, sticking plasters, soldering flux, violin rosin

**6. paraphenylenediamine (PPD)**:
- **Sources**: Hair dyes (black/brown), temporary tattoos, henna, rubber, textiles, dyes

**7. Rubber Accelerators**:
- **Sources**: Rubber gloves, shoes, elastic
- **Chemicals**: Thiuram mix, mercapto mix, carbamates

**8. Preservatives**:
- **Methylisothiazolinone (MI/MCI)**: Wet wipes, moisturizers, shampoos, paints
- **Formaldehyde**: Clothing, cosmetics, nail products
- **Parabens**: Cosmetics, pharmaceuticals

**9. Medicament Allergens**:
- **Neomycin**: Topical antibiotic (ot preparations, creams)
- **Bacitracin**: Ointments
- **Corticosteroids**: Uncommon but possible

**10. Plants**:
- **Poison ivy/oak**: Urushiol oil
- **Primula**: Primin

---

## PATCH TESTING

**Indication**: Suspected ACD not responding to conventional management

**Procedure**:
- Allergens applied to back (non-irritated skin) in Finn chambers
- Removed after 48 hours
- Read at 72 hours and again at 7 days (delayed reactions)
- **Standard series**: ~70 allergens
- **Additional series**: Occupational, hairdressing, cosmetics, footwear, medicaments

**Interpretation**:
- **Negative**: No reaction
- **Irritant reaction** (not allergy)
- **+ (Weak)**: Erythema, infiltration
- **++ (Strong)**: Erythema, infiltration, vesicles
- **+++ (Extreme)**: Bullous reaction

**After Diagnosis**:
- Identify sources of allergen in patient's environment
- Advise on allergen avoidance
- Provide information sheets (alternative products)
- Occupational Health referral if work-related

---

## COMMON SCENARIOS

**HAND DERMATITIS**:
- **Differential**: ICD (wet work), ACD (rubber accelerators, fragrances), atopic eczema, psoriasis
- **Management**: Emollients, topical steroids, avoid irritants, patch test if ACD suspected

**OCCUPATIONAL CONTACT DERMATITIS**:
- **Common occupations**: Hairdressers (ammonium persulfate, PPD, rubber), healthcare (rubber accelerators, fragrances, preservatives), cleaners (detergents, solvents)
- **Management**: Occupational Health referral, workplace adjustments, redeployment if severe

**EYELID DERMATITIS**:
- **Causes**: ACD (fragrances, nail polish transferred to eyes, eye drops, mascara, eyelash glue), atopic eczema
- **Management**: Identify allergen (patch testing), avoid, topical steroid (hydrocortisone 1% butyrate)

**SHOE DERMATITIS**:
- **Causes**: Rubber accelerators, leather (chromium), glue (colophony), adhesives
- **Management**: Identify allergen, avoid, alternative footwear

---

## PREVENTION STRATEGIES

**Irritant Avoidance**:
- Use soap substitutes
- Emollient gloves (cotton) under rubber gloves
- Minimize wet work
- Pat dry, don't rub
- Emollients frequently (at work and home)

**Allergen Avoidance**:
- Once allergen identified, meticulous avoidance required
- Read product labels
- Alternative products available
- **Tip**: Use "fragrance-free" products (not "unscented" which may contain masking fragrance)

---

**Sources**: BAD Contact Dermatitis Guidelines, NICE Dermatitis Guidelines, PCDS**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "dermatology",
                "focus": "contact_dermatitis",
                "sources": ["BAD Contact Dermatitis Guidelines", "NICE Dermatitis Guidelines", "PCDS"]
            }
        )

    def _handle_drug_eruption(self, query: str, context: dict) -> DomainQueryResult:
        """Handle drug eruptions"""
        answer = """**DRUG ERUPTIONS**

---

## MACULOPAPULAR DRUG ERUPTION

**Most common type of drug rash (90% of drug eruptions)**

**Common Culprits**:
- **Antibiotics**: Penicillins, cephalosporins, sulfonamides
- **NSAIDs**: Ibuprofen, naproxen, diclofenac
- **Anticonvulsants**: Carbamazepine, phenytoin, lamotrigine
- **Allopurinol**

**Timing**: 4-14 days after drug initiation (earlier if re-exposure)

**Clinical Features**:
- Morbilliform (measles-like) rash
- Macules + papules
- Often starts on trunk, spreads peripherally
- May become confluent
- **Mild or absent pruritus**
- **Spares palms, soles, mucosa**

**Management**:
- **STOP suspected drug**
- Symptomatic relief: Emollients, oral antihistamines (if pruritic)
- **Topical steroid**: Mild-moderate potency for symptomatic relief
- Self-limiting (1-2 weeks after withdrawal)
- **Report** via Yellow Card scheme (UK)

---

## URTICARIAL DRUG ERUPTIONS

**Similar to idiopathic urticaria but drug-induced**

**Common Culprits**:
- Antibiotics (penicillins)
- NSAIDs
- ACE inhibitors (angioedema)
- Opioids (morphine-induced histamine release)
- **Radiocontrast media**

**Clinical Features**:
- Wheals, angioedema
- Pruritic
- May be associated with anaphylaxis

**Management**:
- **STOP drug**
- If anaphylaxis: **IM adrenaline 0.5mg (0.5ml 1:1000)**
- Antihistamine: Cetirizine 10mg daily
- Short course of oral steroid if severe (prednisolone 40-50mg daily for 5 days)

---

## FIXED DRUG ERUPTION

**Recurrent eruption at same site with each drug exposure**

**Common Culprits**:
- NSAIDs
- Tetracyclines
- Paracetamol (less common)
- COX-2 inhibitors

**Clinical Features**:
- **Well-demarcated, round/oval plaque**
- Erythematous, hyperpigmented (residual pigmentation)
- **Always recurs at exact same location**
- Common sites: Hands, feet, genitalia, lips
- May be single or multiple lesions

**Management**:
- **STOP drug**
- Topical steroid for active lesions
- Educate patient (advise to avoid drug)
- Hyperpigmentation fades over months

---

## SEVERE CUTANEOUS ADVERSE REACTIONS (SCAR)

**EMERGENCIES requiring hospitalization**

---

### STEVENS-JOHNSON SYNDROME (SJS) AND TOXIC EPIDERMAL NECROLYSIS (TEN)

**Spectrum of disease**:
- **SJS**: <10% body surface area (BSA) detachment
- **SJS/TEN overlap**: 10-30% BSA detachment
- **TEN**: >30% BSA detachment

**Common Culprits**:
- **Allopurinol** (high risk)
- **Anticonvulsants**: Carbamazepine, phenytoin, lamotrigine, phenobarbital
- **Sulfonamides**: Co-trimoxazole, sulfasalazine
- **NSAIDs**: Oxicam derivatives (piroxicam)
- **Nevirapine** (HIV)
- **Antibiotics**: Less common but possible

**Clinical Features**:
- **Prodrome**: Fever, malaise, myalgia, sore throat (1-3 days)
- **Rash**: Painful (burning), erythematous, atypical targetoid lesions
- **Mucosal involvement**: Eyes (conjunctivitis), mouth, genitalia (erosions)
- **Nikolsky sign**: Lateral pressure causes skin detachment
- **Skin loss**: Epidermal detachment, sheet-like loss

**Management**:
- **ADMIT TO BURNS UNIT OR ICU**
- **STOP ALL non-essential drugs**
- **Supportive care**: Fluid/electrolyte management, temperature regulation, wound care
- **Specific therapy**: IV immunoglobulin (controversial), ciclosporin (some evidence)
- **Ophthalmology review** (risk of ocular sequelae)
- **Mortality**: SJS ~10%, TEN ~30%

---

### DRUG REACTION WITH EOSINOPHILIA AND SYSTEMIC SYMPTOMS (DRESS)

**Also known as: Drug-induced hypersensitivity syndrome (DIHS)**

**Common Culprits**:
- **Anticonvulsants**: Carbamazepine, phenytoin, lamotrigine, phenobarbital
- **Allopurinol**
- **Sulfonamides**
- **Minocycline**

**Clinical Features** (Triad):
1. **Rash**: Widespread, often morbilliform, may become edematous, facial edema common
2. **Eosinophilia**: Usually >1.5 × 10^9/L (may be delayed)
3. **Systemic involvement** (one or more):
   - Fever (>38°C)
   - Lymphadenopathy
   - Hepatitis (elevated LFTs, common)
   - Interstitial nephritis
   - Pneumonitis
   - Myocarditis (rare)
   - Thyroiditis (later)

**Timing**: 2-6 weeks after drug initiation (later than other drug eruptions)

**Management**:
- **ADMIT**
- **STOP drug**
- **Systemic steroids**: Prednisolone 0.5-1 mg/kg/day (taper over 6-8 weeks)
- Monitor organ involvement (LFTs, renal, CXR, ECG/echo)
- **Rule out infection** (HHV-6 reactivation common)
- **Mortality**: ~10%

---

### ACUTE GENERALIZED EXANTHEMATOUS PUSTULOSIS (AGEP)

**Common Culprits**:
- Antibiotics (β-lactams, macrolides)
- Calcium channel blockers
- Terbinafine

**Clinical Features**:
- **Acute onset**: Fever, extensive erythema
- **Numerous small, sterile pustules** (follicular)
- Predilection for intertriginous areas
- **Rapid resolution** (within 15 days after drug withdrawal)

**Management**:
- **STOP drug**
- Supportive care
- Topical steroids, antipyretics
- Usually self-limiting

---

## DIAGNOSTIC APPROACH TO SUSPECTED DRUG ERUPTION

**History**:
- **Drug history**: ALL medications (including OTC, herbal), start dates
- **Previous drug exposures** (any prior reactions?)
- **Timing**: Rash onset relative to drug initiation
- **Symptoms**: Pain, pruritus, fever, mucosal involvement, systemic symptoms
- **Atopy**: History of atopy, drug allergies

**Examination**:
- **Distribution**: Pattern, morphology, BSA involvement
- **Mucosa**: Eyes, mouth, genitalia
- **Nikolsky sign**: For suspected SJS/TEN
- **Lymphadenopathy**
- **Systemic signs**: Fever, hypotension, tachycardia

**Investigations** (if severe):
- **FBC**: Eosinophilia (DRESS), leukocytosis, thrombocytopenia (SJS/TEN)
- **U&E**: Renal impairment
- **LFTs**: Hepatitis (DRESS)
- **CRP/ESR**: Inflammatory markers
- **Skin biopsy**: For SJS/TEN, AGEP, DRESS (dermatology)
- **Patch testing**: For delayed reactions (type IV), once recovered

---

## MANAGEMENT PRINCIPLES

**Mild-Moderate Drug Eruptions**:
- **STOP suspected drug**
- Symptomatic relief (emollients, antihistamines, topical steroids)
- **Re-challenge**: Contraindicated (risk of more severe reaction)
- **Cross-reactivity**: Avoid structurally related drugs
- **Report**: Yellow Card scheme (UK)

**Severe Drug Eruptions** (SJS/TEN, DRESS, AGEP):
- **ADMIT TO HOSPITAL**
- **STOP drug(s)**
- **Supportive care** (ICU/burns unit if SJS/TEN)
- **Specialist involvement** (dermatology, ophthalmology, ICU)
- **Consider systemic steroids** (DRESS)

---

## PREVENTION

- **Document drug allergy** clearly in records and inform patient
- **Avoid cross-reactive drugs** (e.g., avoid all penicillins if penicillin allergy)
- **Educate patient** to avoid drug and alert future healthcare providers
- **Medical alert bracelet** if severe reaction (anaphylaxis, SJS/TEN, DRESS)

---

**Sources**: BAD Drug Eruptions Guidelines, NICE Clinical Knowledge Summaries, BJDD Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "dermatology",
                "focus": "drug_eruptions",
                "sources": ["BAD Drug Eruptions Guidelines", "NICE CKS", "BJDD Guidelines"]
            }
        )

    def _handle_urticaria(self, query: str, context: dict) -> DomainQueryResult:
        """Handle urticaria and angioedema"""
        answer = """**URTICARIA (HIVES) AND ANGIOEDEMA**

---

## ACUTE URTICARIA

**Definition**: Transient, pruritic wheals (hives) lasting <6 weeks

**Etiology**:
- **Idiopathic**: 50% (no identifiable cause)
- **IgE-mediated**: Foods (nuts, shellfish, eggs, milk), medications (antibiotics, NSAIDs), insect stings
- **Physical**: Cold, heat, solar, pressure, vibration, exercise (cholinergic)
- **Infections**: Viral (URTI), bacterial (streptococcus), parasitic
- **Stress**

**Clinical Features**:
- **Wheals**: Raised, erythematous, pruritic plaques
- **Blanches with pressure**
- **Transient**: Individual wheals last <24 hours (move around body)
- **Any distribution**: Trunk, limbs, face, palms/soles may be involved
- **No residual marks** (unless excoriated)

**Management**:

**First-line**:
- **Oral antihistamine**: Cetirizine 10mg OD or loratadine 10mg OD
- **Increase dose** (up to 4x standard dose) if inadequate response
- **Add second antihistamine** (if high-dose single agent ineffective)

**Severe symptoms**:
- Short course of oral steroids (prednisolone 40mg daily for 3-5 days)

**Identify and avoid triggers** (if identified)

---

## CHRONIC URTICARIA

**Definition**: Urticaria lasting >6 weeks (recurrent or persistent)

**Classification**:
- **Chronic spontaneous urticaria (CSU)**: No specific trigger identified (80%)
- **Chronic inducible urticaria**: Triggered by physical stimulus

**Chronic Inducible Urticaria Subtypes**:

**1. Symptomatic Dermographism**:
- **Trigger**: Stroking or scratching skin
- **Wheals**: Linear, at site of mechanical trauma
- **Confirm**: Stroke skin with blunt object (wheal forms in 5-10 minutes)

**2. Cold Urticaria**:
- **Trigger**: Cold objects, cold air, cold water
- **Wheals**: At site of cold contact
- **Systemic**: Swimming in cold water → risk of hypotension, drowning
- **Confirm**: Ice cube test (ice cube on forearm for 5 minutes → wheal after rewarming)

**3. Cholinergic Urticaria**:
- **Trigger**: Heat, emotion, exercise, sweating
- **Wheals**: Small (2-4mm), pin-point, surrounded by red flare
- **Distribution**: Trunk, limbs
- **Confirm**: Exercise test (e.g., running on treadmill)

**4. Solar Urticaria**:
- **Trigger**: Sunlight (UVA, visible light, UVB)
- **Wheals**: Within minutes of sun exposure

**5. Delayed Pressure Urticaria**:
- **Trigger**: Sustained pressure (tight clothing, sitting, standing)
- **Wheals**: Deep, painful swelling 3-12 hours after pressure
- **Distribution**: Buttocks, feet, hands, waistline

**6. Heat Urticaria**:
- **Trigger**: Localized heat (rare)

**7. Vibratory Angioedema**:
- **Trigger**: Vibration (rare)

**8. Aquagenic Urticaria**:
- **Trigger**: Water contact (regardless of temperature) (extremely rare)

---

## ANGIOEDEMA

**Definition**: Transient swelling of deeper dermis, subcutaneous, or submucosal tissues

**Types**:

**1. Histamine-Mediated Angioedema**:
- **Associated with urticaria** (often)
- **Same triggers**: Foods, drugs, physical stimuli
- **Responsive**: Antihistamines, steroids
- **No family history**

**2. Bradykinin-Mediated Angioedema** (histamine-resistant):
- **Hereditary Angioedema (HAE)**:
  - **C1 esterase inhibitor deficiency** (type I) or dysfunction (type II)
  - **Autosomal dominant**
  - **Family history**: 75% (de novo mutation 25%)
  - **Triggers**: Stress, trauma, dental procedures, ACE inhibitors (may precipitate)
  - **NOT associated with urticaria**
  - **NOT responsive** to antihistamines or steroids
  - **Locations**: Face, tongue, lips, airway, hands, feet, abdomen (abdominal pain)
  - **Duration**: 48-72 hours (longer than histamine-mediated)
  - **Diagnostic**: Low C4, low/absent C1 esterase inhibitor
  - **Treatment**: C1 esterase inhibitor concentrate, icatibant (bradykinin B2 receptor antagonist), tranexamic acid

- **Acquired Angioedema (AAE)**:
  - **C1 esterase inhibitor consumption** (lymphoproliferative disease, autoimmune)
  - **No family history**
  - **Low C1q** (distinguishes from HAE)

- **ACE Inhibitor-Induced Angioedema**:
  - **Incidence**: 0.1-0.7%
  - **More common**: African descent
  - **Timing**: Can occur months to years after starting
  - **NOT dose-dependent**
  - **Management**: **STOP ACE inhibitor permanently** (switch to ARB)
  - **NOT associated with urticaria**

---

## URTICARIA MANAGEMENT

**Stepwise Approach**:

**Step 1: Standard-dose second-generation antihistamine**:
- Cetirizine 10mg OD OR loratadine 10mg OD OR fexofenadine 180mg OD

**Step 2: Increase dose**:
- Up to **4 times standard dose** (e.g., cetirizine 10mg QID)
- **First-generation antihistamines** (sedating): Chlorphenamine 4mg QID (add at night if needed)

**Step 3: Add leukotriene receptor antagonist**:
- Montelukast 10mg OD (especially if NSAID-induced)

**Step 4: Referral to dermatology** (for consideration of):
- **Omalizumab** (anti-IgE monoclonal antibody): NICE-recommended for antihistamine-resistant CSU
- **Ciclosporin**: 3-5 mg/kg/day (specialist only)
- **Oral steroids**: Short courses only for flares (NOT long-term)

**Chronic Inducible Urticaria-Specific Management**:
- **Symptomatic dermographism**: High-dose antihistamine
- **Cold urticaria**: Cold avoidance, high-dose antihistamine
- **Cholinergic urticaria**: High-dose antihistamine, avoid heat triggers
- **Solar urticaria**: Sun protection, antihistamine
- **Delayed pressure urticaria**: Poor response to antihistamines (consider montelukast, steroids)

---

## EMERGENCY MANAGEMENT: ANAPHYLAXIS-ASSOCIATED ANGIOEDEMA

**Features of anaphylaxis**:
- Angioedema (lips, tongue, pharynx)
- Stridor, wheeze, respiratory distress
- Hypotension, tachycardia
- Urticaria often present

**Management**:
1. **IM Adrenaline (Epinephrine) 0.5mg (0.5ml of 1:1000)** intramuscularly into mid-anterolateral thigh
2. Call for help, **call ambulance (999)**
3. Airway, breathing, circulation
4. Oxygen 15 L/min
5. **Second dose** IM adrenaline after 5 minutes if no improvement
6. **Antihistamine**: Cetirizine 10mg PO or chlorphenamine 10mg IV/IM/PO
7. **Steroid**: Hydrocortisone 200mg IV/IM
8. **Admit**: All patients with airway compromise, hypotension, or requiring >2 doses adrenaline

---

## TRIGGER IDENTIFICATION AND AVOIDANCE

**Take Detailed History**:
- Food triggers (onset within 2 hours, rarely after 6 hours)
- Medications (including OTC)
- Physical stimuli
- Infections
- Stress
- Contact allergens (latex)

**Investigations** (if indicated):
- **Skin prick testing** (IgE-mediated)
- **Specific IgE blood tests** (RAST)
- **Elimination diets** (food-induced)
- **Physical challenge tests** (for inducible urticarias, specialist only)

**Avoidance** (if trigger identified):
- Elimination of confirmed food trigger
- Medication avoidance (cross-reactive drugs)
- Avoid physical triggers where possible

---

## PROGNOSIS

**Acute Urticaria**:
- Usually self-limiting (<6 weeks)
- Recurrence common if trigger re-exposure

**Chronic Spontaneous Urticaria**:
- **Duration**: 1-5 years (average 2-3 years)
- **50% resolve** within 1 year
- **20% persist** >5 years
- May remit and relapse

**Sources**: NICE CG183 Anaphylaxis, BAD Urticaria Guidelines, EAACI Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "dermatology",
                "focus": "urticaria_angioedema",
                "sources": ["NICE CG183", "BAD Urticaria Guidelines", "EAACI Guidelines"]
            }
        )

    def _handle_pediatric_rash(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pediatric rashes"""
        answer = """**PEDIATRIC RASHES**

---

## VIRAL EXANTHEMS

### MEASLES (Rubeola, Morbilli)

**Pathogen**: Measles virus (paramyxovirus)

**Age**: Unvaccinated children, 1-4 years (but can affect any age)

**Incubation**: 10-12 days

**Prodrome** (2-4 days):
- **High fever** (often >39°C)
- **"The 3 Cs"**: Cough, Coryza (nasal congestion), Conjunctivitis
- Irritability, malaise

**Koplik Spots**:
- **Pathognomonic**: White lesions on buccal mucosa opposite molars
- **Appear**: 1-2 days before rash
- **Grayish-white**, surrounded by red halo

**Rash**:
- **Onset**: 3-4 days after prodrome begins (fever peaks)
- **Start**: Hairline, behind ears, forehead
- **Spread**: Descends to face, trunk, limbs (palms/soles involved)
- **Morphology**: Maculopapular, initially discrete, becomes confluent
- **Colour**: Red to violaceous
- **Duration**: 5-7 days, then desquamation

**Complications**:
- **Pneumonia** (most common cause of death)
- **Otitis media**
- **Diarrhea**
- **Encephalitis** (1 in 1000, 15% mortality)
- **SSPE** (subacute sclerosing panencephalitis) - rare, years later

**Management**:
- **Supportive** (antipyretics, fluids)
- **Vitamin A**: 200,000 IU daily for 2 days (WHO recommendation for measles in deficient populations)
- **Isolate**: Exclude from school/nursery for 4 days after rash onset
- **Notifiable disease**

**Prevention**: MMR vaccine (12 months, 3 years 4 months)

---

### RUBELLA (German Measles)

**Pathogen**: Rubella virus (togavirus)

**Age**: Unvaccinated children

**Incubation**: 14-21 days

**Prodrome** (mild, 1-5 days):
- Low-grade fever, malaise, coryza, headache
- **Mild** compared to measles

**Rash**:
- **Onset**: 1-5 days after prodrome
- **Start**: Face, behind ears
- **Spread**: Rapidly spreads to trunk, limbs within 24 hours
- **Morphology**: Pink maculopapular, discrete (NOT confluent)
- **Duration**: 2-3 days

**Lymphadenopathy**:
- **Post-auricular**, suboccipital, posterior cervical
- **Prominent**, tender
- **Precedes rash** by up to 1 week

**Complications**:
- **Arthralgia/arthritis** (more common in adult women, fingers, wrists, knees)
- **Encephalitis** (rare)
- **Thrombocytopenia** (rare)

**Congenital Rubella Syndrome**:
- **Risk**: Up to 90% if maternal infection in first trimester
- **Features**: Deafness, cataracts, cardiac defects (PDA), microcephaly, intellectual disability
- **Management**: **Terminate pregnancy** if maternal infection in first trimester (discuss)

**Management**:
- **Supportive**
- **Isolate**: Exclude for 5 days from rash onset
- **Notifiable disease**

**Prevention**: MMR vaccine

---

### CHICKENPOX (Varicella)

**Pathogen**: Varicella-zoster virus (herpesvirus)

**Age**: 1-10 years (peak 5-9)

**Incubation**: 10-21 days (average 14)

**Infectious Period**:
- **2 days before rash** until **all lesions crusted** (usually 5-7 days)

**Prodrome** (1-2 days):
- Fever, malaise, headache, anorexia (mild)

**Rash**:
- **Crops**: New lesions appear in crops over 3-5 days
- **Progression**: Macule → Papule → Vesicle (teardrop) → Pustule → Crust
- **Distribution**: Centripetal (starts on trunk, scalp, face, then limbs)
- **Polymorphous**: Lesions at different stages in same area (pathognomonic)
- **Pruritic**: Intense itching

**Management**:
- **Calamine lotion**: For pruritus
- **Oral antihistamine**: Cetirizine (for children >2 years)
- **Fever management**: Paracetamol (AVOID ibuprofen - risk necrotizing soft tissue infections)
- **Keep fingernails short** (prevent excoriation and secondary infection)
- **Exclude**: Until all lesions crusted (usually 5-7 days)
- **Avoid contact** with high-risk individuals (pregnant women, neonates, immunocompromised)

**Complications**:
- **Secondary bacterial infection** (Staph aureus, Strep pyogenes): Cellulitis, necrotizing fasciitis
- **Pneumonia** (more common in adults, smokers)
- **Encephalitis**, cerebellar ataxia
- **Neonatal varicella** (if maternal infection 5 days before to 2 days after delivery - severe)

**Prevention**: Varicella vaccine (not routine in UK, consider for seronegative healthcare workers)

---

### HAND, FOOT, AND MOUTH DISEASE

**Pathogen**: Coxsackievirus A16 (most common), Enterovirus 71 (more severe)

**Age**: Children <10 years (peak 2-6)

**Incubation**: 3-7 days

**Clinical Features**:
- **Oral lesions**: Painful vesicles/ulcers on tongue, buccal mucosa, palate
- **Rash**: Vesicles on palms, soles, buttocks (sometimes)
- **Systemic**: Low-grade fever, malaise, anorexia
- **Duration**: 7-10 days

**Management**:
- **Supportive**: Fluids, analgesia (paracetamol, ibuprofen)
- **Topical analgesic**: Lidocaine gel for oral ulcers
- **Exclude**: Until feeling well (some schools exclude until lesions healed)

**Complications**:
- **Dehydration** (oral pain)
- **Enterovirus 71**: Encephalitis, myocarditis, pulmonary edema (rare, severe)

---

### FIFTH DISEASE (Erythema Infectiosum)

**Pathogen**: Parvovirus B19

**Age**: 4-12 years

**Incubation**: 4-14 days

**Prodrome** (mild):
- Low-grade fever, headache, coryza (mild)

**Rash** (3 stages):
1. **"Slapped-cheek" appearance**: Bright red, erythematous cheeks, circumoral pallor
2. **Lacy, reticular rash**: On trunk, limbs (day 1-4 after slapped cheek)
3. **Evanescent**: Rash fades and recurs with heat, exercise, sunlight (weeks to months)

**Arthropathy** (more common in adult women):
- Symmetric, hands, wrists, knees, ankles
- Self-limiting (weeks to months)

**Complications**:
- **Aplastic crisis** in patients with underlying hemolytic anemia (sickle cell, hereditary spherocytosis)
- **Hydrops fetalis** if maternal infection in second trimester (10% risk)

**Management**:
- **Supportive**
- **Exclude**: No exclusion if feeling well

**Pregnancy**: If exposed, check parvovirus IgM/IgG (if susceptible, serial ultrasounds for fetal hydrops)

---

### SIXTH DISEASE (Roseola Infantum, Exanthem Subitum)

**Pathogen**: Human herpesvirus 6 (HHV-6), HHV-7

**Age**: 6 months to 3 years (peak 6-15 months)

**Incubation**: 5-15 days

**Prodrome**:
- **High fever** (often >39°C) for 3-5 days
- Febrile seizures (common due to rapid fever rise)
- Irritability

**Rash**:
- **Onset**: As fever defervesces
- **Morphology**: Rose-pink macules or maculopapules
- **Distribution**: Trunk, spreads to neck, face, limbs
- **Duration**: 1-2 days, then fades

**Management**:
- **Supportive** (antipyretics)
- **Exclude**: No exclusion if feeling well

---

### KAWASAKI DISEASE

**IMPORTANT**: Most common cause of acquired heart disease in children in developed countries

**Age**: 6 months to 5 years (peak 1-2 years), rare >8 years

**Diagnostic Criteria** (must have fever ≥5 days + 4/5 criteria):

1. **Extremity changes**:
   - Acute: Erythema, edema of hands/feet
   - Subacute (2-3 weeks): Desquamation of fingers/toes

2. **Rash**: Polymorphous (maculopapular, urticarial, scarlatiniform) - NO vesicles/bullae

3. **Conjunctival injection**: Bilateral, non-exudative

4. **Oral changes**: Strawberry tongue, cracked lips, erythema of oropharynx

5. **Cervical lymphadenopathy**: Usually unilateral, >1.5cm

**Complications**:
- **Coronary artery aneurysms** (25% untreated, 5% with treatment)
- **Myocardial infarction** (ruptured aneurysm, thrombosis)
- **Myocarditis**, pericardial effusion

**Management**:
- **ADMIT** (all suspected Kawasaki)
- **IV immunoglobulin** (2g/kg over 10-12 hours, single dose)
- **High-dose aspirin** (initially 80-100 mg/kg/day, then low-dose 3-5 mg/kg/day for 6-8 weeks)
- **Echocardiogram**: Baseline, 2-6 weeks, 6-12 months

---

## MENINGOCOCCAL SEPSIS (MENINGOCOCCEMIA)

**PATHOGEN**: *Neisseria meningitidis*

**Medical Emergency**

**Clinical Features**:
- **Non-blanching purpuric rash** (petechiae, purpura, ecchymoses)
- **Fever**, headache, myalgia
- **Neck stiffness**, photophobia (meningitis)
- **Altered mental status**, shock

**Management**:
- **IMMEDIATE EMERGENCY** (call 999)
- **IM benzylpenicillin** (before transfer if available) OR cefotaxime
- **Urgent transfer** to hospital (ICU)
- **IV antibiotics**, fluids, inotropes

---

## KEY DIAGNOSTIC CLUES

| Feature | Measles | Rubella | Chickenpox | Fifth | Sixth | Kawasaki |
|---------|---------|---------|------------|-------|-------|----------|
| Koplik spots | Yes | No | No | No | No | No |
| Conjunctivitis | Yes | No | No | No | No | Yes (non-exudative) |
| Lymphadenopathy | No | Yes (post-auricular) | No | No | No | Yes (cervical) |
| Lesion stages | Same stage | Same stage | Different stages | N/A | N/A | Polymorphous |
| Vesicles | No | No | Yes | No | No | No |
| Desquamation | Yes | No | No | No | No | Yes (fingers/toes) |

---

**Sources**: NICE Clinical Knowledge Summaries, RCPCH Guidelines, BAD Pediatric Dermatology Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "dermatology",
                "focus": "pediatric_rashes",
                "sources": ["NICE CKS", "RCPCH Guidelines", "BAD Pediatric Dermatology Guidelines"]
            }
        )

    def _handle_bacterial(self, query: str, context: dict) -> DomainQueryResult:
        """Handle bacterial skin infections"""
        answer = """**BACTERIAL SKIN INFECTIONS**

---

## IMPETIGO

**Pathogen**: *Staphylococcus aureus* (most common), *Streptococcus pyogenes* (group A strep)

**Age**: Children (2-5 years)

**Types**:

**1. Non-Bullous Impetigo** (most common, 70%):
- **Lesions**: Small vesicles → honey-coloured crusts, golden-yellow
- **Distribution**: Face (around nose, mouth), extremities
- **Contagious**: Autoinoculation (scratching spreads lesions)
- **Healing**: Without scarring

**2. Bullous Impetigo**:
- **Pathogen**: *S. aureus* (phage group II)
- **Lesions**: Large, flaccid bullae containing clear fluid
- **Distribution**: Trunk, axillae, diaper area (infants)
- **Bullae rupture**: Collar of scale (rim of scale around lesion)

**Management**:

**Localized impetigo (few lesions)**:
- **Topical fusidic acid 2%** cream/ointment TDS for 5 days
- OR **Topical retapamulin 1%** ointment BID for 5 days
- **Soak crusts** with warm saline or sodium hypochlorite solution before application

**Widespread impetigo**:
- **Oral flucloxacillin 500mg QDS** (500mg QDS for 5-7 days) (adult) OR 125-250mg QDS (child)
- OR **Oral clarithromycin 250-500mg BD** (if penicillin allergy)
- **Topical adjunct**: As above

**Exclusion**: Exclude from school/nursery until lesions are crusted or healed (or 48 hours after antibiotics started)

---

## CELLULITIS

**Pathogen**: *Streptococcus pyogenes* (group A strep) most common, *Staphylococcus aureus*

**Definition**: Acute infection of dermis and subcutaneous tissue

**Risk Factors**:
- **Break in skin**: Wound, ulcer, tinea pedis, insect bite, surgery
- **Lymphedema**, venous insufficiency, obesity
- **Diabetes**, immunosuppression

**Clinical Features**:
- **Erythema**: Well-demarcated, redness
- **Warmth**, swelling, tenderness
- **Systemic**: Fever, chills, malaise (common)
- **Lymphangitis**: Red streaks from infection to lymph nodes
- **Location**: Lower legs most common (tinea pedis portal of entry)

**Management**:

**Mild Cellulitis**:
- **Oral flucloxacillin 500mg QDS** (7 days) (adult)
- OR **Oral clarithromycin 500mg BD** (if penicillin allergy)
- **Elevation** of affected limb
- **Analgesia**: Paracetamol, ibuprofen
- **Treat portal of entry**: e.g., tinea pedis

**Moderate-Severe Cellulitis** (systemic symptoms, extensive involvement):
- **ADMIT**
- **IV flucloxacillin 2g QDS** (IV benzylpenicillin if strep suspected)
- OR **IV clindamycin 600mg QDS** (if penicillin allergy)

**Special Situations**:

**Facial Cellulitis**:
- **Periorbital cellulitis**: Around eye
- **Orbital cellulitis** (EMERGENCY): Eye involvement, proptosis, ophthalmoplegia → **URGENT ophthalmology referral**

**Recurrent Cellulitis**:
- **Identify and treat portal of entry** (tinea pedis, ulcer)
- **Prophylaxis**: Consider penicillin V 500mg BD (or clindamycin) for 6-12 months (frequent recurrences)

---

## ERYSIPELAS

**Pathogen**: *Streptococcus pyogenes* (group A strep)

**Definition**: Superficial cellulitis involving upper dermis and lymphatics

**Clinical Features**:
- **Well-demarcated**, raised, indurated plaque
- **"Orange peel"** appearance (peau d'orange)
- **Bright red** colour
- **Systemic**: High fever, chills, malaise (prominent)
- **Location**: Lower legs, face

**Management**:
- **Oral phenoxymethylpenicillin (Penicillin V) 500mg QDS** (7-10 days)
- OR **Oral clarithromycin 500mg BD** (if penicillin allergy)
- **Elevation** of affected limb
- **IV therapy** if systemic symptoms

---

## FOLLICULITIS, FURUNCLES, AND CARBUNCLES

**Pathogen**: *Staphylococcus aureus*

**Folliculitis**:
- **Inflammation**: Of hair follicle
- **Lesions**: Small pustules with hair at center
- **Distribution**: Anywhere hair-bearing
- **Management**: Topical fusidic acid or antiseptic wash (chlorhexidine)

**Furuncle (Boil)**:
- **Infection**: Deeper, extends into dermis and subcutis
- **Lesion**: Inflammatory nodule with pustular center
- **Location**: Neck, axillae, buttocks, thighs
- **Management**:
  - **Incision and drainage** (if fluctuant)
  - **Do NOT squeeze** (risk of cellulitis, abscess spread)
  - Oral flucloxacillin if systemic symptoms or extensive

**Carbuncle**:
- **Multiple furuncles** coalescing
- **Deeper infection**, larger area
- **Systemic symptoms**: Fever, malaise (common)
- **Location**: Nape of neck, back
- **Management**:
  - **Incision and drainage** (surgical)
  - **Oral flucloxacillin 500mg QDS** (or IV if severe)

**Risk Factors**: Diabetes, obesity, immunosuppression, malnutrition, hygiene

---

## NECROTIZING FASCIITIS

**Medical Emergency**

**Pathogens**:
- **Type I**: Mixed anaerobes + aerobes (*Bacteroides*, *Peptostreptococcus*, *E. coli*, *Klebsiella*)
- **Type II**: Group A strep ± *S. aureus*

**Risk Factors**: Diabetes, IV drug use, trauma, surgery, childbirth

**Clinical Features**:
- **Severe pain** out of proportion to physical findings
- **Swelling**, edema beyond erythema
- **Crepitus** (gas in tissues)
- **Purple/ violaceous bullae**, necrosis, ecchymosis
- **Systemic**: Fever, hypotension, sepsis, multi-organ failure
- **"Hardness"**: Wood-like feel of affected tissue

**Management**:
- **IMMEDIATE surgical debridement** (emergency)
- **IV antibiotics**: Dual therapy (e.g., meropenem + clindamycin)
- **ICU admission**
- **High mortality** (20-40%)

---

## STAPHYLOCOCCAL SCALDED SKIN SYNDROME (SSSS)

**Pathogen**: *Staphylococcus aureus* (phage group II) producing exfoliative toxins

**Age**: Children <5 years (especially neonates)

**Clinical Features**:
- **Prodrome**: Fever, irritability, malaise (1-2 days)
- **Tender skin**
- **Superficial erosion**, sheet-like desquamation
- **Positive Nikolsky sign**: Lateral pressure causes skin detachment
- **Periorificial crusting**: Around mouth, nose, eyes, ears
- **Trunk** involvement (spares mucosa, palms, soles)

**Management**:
- **ADMIT**
- **IV flucloxacillin** (to eradicate toxin-producing focus)
- **Supportive care**: Fluid management, temperature regulation
- **Antibiotics**: Treat secondary infection (if present)
- **Prognosis**: Good, usually self-limiting (mortality low)

---

## ERYSIPELOID

**Pathogen**: *Erysipelothrix rhusiopathiae* (gram-positive bacillus)

**Occupational**: Butchers, fishermen, veterinarians (animal contact)

**Clinical Features**:
- **Purple-red plaque** with well-defined, raised border
- **Location**: Fingers, hands, arms
- **Painful**, burning
- **Minimal systemic symptoms**

**Management**:
- **Oral penicillin V 500mg QDS** (7-10 days)
- OR **Oral erythromycin 500mg QDS** (if penicillin allergy)

---

## TINEA (FUNGAL) VERSUS BACTERIAL INFECTION

| Feature | Tinea (Fungal) | Bacterial (Impetigo/Cellulitis) |
|---------|----------------|----------------------------------|
| Scale | Prominent | Minimal/absent |
| Border | Active, advancing | Well-demacrated (cellulitis) |
| Honey crust | No | Yes (impetigo) |
| Vesicles | May be present | May be present (bullous impetigo) |
| Lymphangitis | No | Yes (cellulitis) |
| KOH prep | Positive | Negative |

---

**Sources**: NICE Clinical Knowledge Summaries, BAD Bacterial Skin Infection Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "dermatology",
                "focus": "bacterial_infections",
                "sources": ["NICE CKS", "BAD Bacterial Skin Infection Guidelines"]
            }
        )

    def _handle_ectoparasites(self, query: str, context: dict) -> DomainQueryResult:
        """Handle scabies and lice"""
        answer = """**ECTOPARASITIC INFESTATIONS**

---

## SCABIES

**Pathogen**: *Sarcoptes scabiei var. hominis* (mite)

**Transmission**:
- **Direct skin-to-skin contact** (prolonged, holding hands, sexual contact)
- **Fomites**: Less common (mite survives 2-3 days off host)

**Incubation**:
- **First infestation**: 2-6 weeks (sensitization period)
- **Re-infestation**: 1-3 days (already sensitized)

---

### CLINICAL FEATURES

**Pruritus**:
- **Severe**, worse at night
- **Generalized** (often spares face)
- **Persists** after adequate treatment (post-scabetic itch, weeks-months)

**Burrows**:
- **Pathognomonic**: Small, wavy, linear, greyish tracks
- **Location**: Interdigital webs, wrists, elbows, axillae, areolae, genitalia (men), buttocks
- **Length**: 1-10mm
- **Mite** at end of burrow (small grey speck)

**Secondary Lesions**:
- Excoriations, eczema, nodules, crusts
- **Infection**: Secondary bacterial infection (impetigo, cellulitis) common

---

### SPECIAL POPULATIONS

**Infants**:
- **Distribution**: Whole body (including face, scalp, palms, soles)
- **Vesicles**, pustules common
- **Irritable**, poor feeding, failure to thrive

**Elderly**:
- **Pruritus** may be only manifestation
- **Nodular scabies**: Persistent pruritic nodules (especially on genitalia, axillae)

**Immunocompromised**:
- **Crusted (Norwegian) scabies**:
  - Widespread hyperkeratotic, crusted plaques
  - Thousands to millions of mites
  - Highly contagious
  - Minimal pruritus (immune response impaired)
  - **ADMIT for isolation and treatment**

---

### DIAGNOSIS

**Clinical diagnosis** (usually)
- Typical history, symptoms, burrows

**Confirmatory** (if uncertain):
- **Skin scraping**: Microscopy (mite, eggs, feces)
- **Burrow ink test**: Ink wiped over burrow, mite highlighted
- **Dermoscopy**: Delta wing jet with triangular head (mite)

---

### MANAGEMENT

**Permethrin 5%** (first-line):
- **Cream**, head to toe (including scalp, face, genitals, under nails)
- **Leave on 8-24 hours** (usually overnight), wash off
- **Repeat after 7 days**
- **Treat all household contacts** simultaneously (even if asymptomatic)
- **Pregnancy/lactation**: Permethrin considered safe

**Malathion 0.5%** (alternative):
- **Aqueous lotion**, 24 hours, repeat after 7 days
- If permethrin contraindicated or treatment failure

**Ivermectin** (oral) (second-line):
- **Single dose** 200 mcg/kg, repeat after 7-10 days
- **Indication**: Crusted scabies, treatment failure, institutional outbreaks
- **Contraindications**: Pregnancy, breastfeeding, children <15kg

---

### POST-TREATMENT CARE

**Itch Management**:
- **Post-scabetic itch**: May persist for weeks to months (dead mites, hypersensitivity)
- **Topical steroid**: Potent steroid BID for 1-2 weeks
- **Oral antihistamine**: Sedating (chlorphenamine) at night
- **Emollients**: Liberal application

**Reassurance**:
- Itch does NOT mean treatment failure
- Exclude re-infestation or treatment failure if:
  - Itch persists >2-4 weeks after second treatment
  - New burrows appear
  - Household contacts not treated

---

### ENVIRONMENTAL MEASURES

**Decontamination**:
- **Wash** all clothes, bed linen, towels (used in previous 48 hours)
- **Hot wash** (50°C+) or hot tumble dry
- **Seal** non-washable items in plastic bag for 72 hours

**Household Contacts**:
- **Treat all** household members (simultaneously)
- **Exclude**: No exclusion from school/work after first treatment

---

## PEDICULOSIS CAPITIS (HEAD LICE)

**Pathogen**: *Pediculus humanus capitis* (louse)

**Transmission**:
- **Direct head-to-head contact** (most common)
- **Fomites** (less common: hats, combs, pillows)

**Life Cycle**:
- Eggs (nits) → Nymphs → Adult lice
- Eggs hatch in 7-10 days
- Nymphs mature in 7-10 days
- **Adult lifespan**: 30 days (feed on blood every 4-6 hours)

---

### CLINICAL FEATURES

**Pruritus**:
- Scalp itch (may be absent initially)
- Scratching, excoriation, secondary infection

**Nits**:
- **Eggs** attached to hair shaft
- **Location**: Within 1-2cm of scalp (viable)
- **Appearance**: Small, oval, white/cream/brown
- **Distinguish**: From dandruff (nits firmly attached, dandruff easily removed)

**Lice**:
- **Adults**: 2-4mm, grey-brown, move quickly
- **Nymphs**: Smaller, same colour
- **Visible**: On scalp, behind ears, nape of neck

**Cervical lymphadenopathy** (due to secondary infection)

---

### DIAGNOSIS

**Detection Combing**:
- **Wet hair**, conditioner
- **Fine-toothed detection comb**
- Comb from root to tip, wipe comb on tissue
- **Live lice** indicate active infestation (nits alone insufficient)

---

### MANAGEMENT

**Insecticides** (first-line):
1. **Malathion 0.5% aqueous lotion**:
   - Apply to dry hair, saturate scalp and hair
   - Leave 12 hours (overnight), wash out
   - **Repeat after 7 days** (to kill newly hatched nymphs)

2. **Permethrin 1%** (if malathion contraindicated or resistance):
   - Apply to damp hair, leave 10 minutes, wash out
   - Repeat after 7 days

3. **Phenothrin** (less used due to resistance)

**Physical Methods**:
- **Wet combing**: Fine-toothed comb, conditioner, every 3-4 days for 2 weeks
- **Dimeticone** (silicone-based): Suffocates lice, 8 hours, repeat after 7 days

**Household Contacts**:
- **Check** all household contacts
- **Treat** only if live lice found (do NOT treat prophylactically)

**Exclusion**: No exclusion from school (once treatment started)

---

### RESISTANCE

- **Common** to permethrin, phenothrin (increasing)
- **Less common** to malathion (but reported)
- **Consider alternative** if treatment failure (verify correct application first)

---

## PEDICULOSIS CORPORIS (BODY LICE)

**Pathogen**: *Pediculus humanus corporis*

**Risk Factors**:
- Poor hygiene, overcrowding, homelessness, refugee camps

**Transmission**:
- **Fomites** (clothing, bedding)
- **Direct contact** (less common)

**Clinical Features**:
- **Pruritus**: Generalized
- **Lesions**: Excoriations, eczema, secondary infection
- **Lice**: In clothing seams (not on body)
- **Nits**: In clothing fibers

**Management**:
- **Improve hygiene**: Regular washing of clothes and bedding (hot water >50°C)
- **Insecticide**: Treat clothing (permethrin, malathion)
- **Treat**: All individuals in close contact

---

## PEDICULOSIS PUBIS (PUBIC LICE / "CRABS")

**Pathogen**: *Pthirus pubis* (crab louse)

**Transmission**:
- **Sexual contact** (most common)
- **Fomites** (less common: towels, bed linen)

**Clinical Features**:
- **Pruritus**: Pubic, perianal, axillary (if heavy infestation)
- **Lice**: Visible on pubic hair (crab-shaped)
- **Nits**: Attached to pubic hair
- **Blue spots**: Maculae caeruleae (at bite sites, pathognomonic)
- **Secondary lesions**: Excoriations, eczema, infection

**Management**:
- **Permethrin 5%** or **Malathion 0.5%** (same regimen as scabies, single application)
- **Treat sexual partners** (within last month)
- **Screen for other STIs** (high risk population)

---

## KEY POINTS

**Scabies**:
- **Treat all** household contacts simultaneously
- **Permethrin 5%** first-line (two applications, 7 days apart)
- **Post-scabetic itch** common (not treatment failure)
- **Admit** if crusted scabies (isolation)

**Head Lice**:
- **Diagnosis**: Detection combing (live lice)
- **Treatment**: Malathion 0.5% (two applications, 7 days apart)
- **Do NOT treat** asymptomatic contacts
- **No school exclusion** after treatment started

**Sources**: NICE CKS, BAD Scabies Guidelines, PHL Scabies Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "dermatology",
                "focus": "ectoparasites_scabies_lice",
                "sources": ["NICE CKS", "BAD Scabies Guidelines", "PHL Scabies Guidelines"]
            }
        )

    def _handle_hair_nail(self, query: str, context: dict) -> DomainQueryResult:
        """Handle hair and nail disorders"""
        answer = """**HAIR AND NAIL DISORDERS**

---

## ALOPECIA (HAIR LOSS)

### ANDROGENETIC ALOPECIA (Pattern Baldness)

**Male Pattern Baldness**:
- **Prevalence**: 80% of men by age 70
- **Pattern**: Receding hairline (bitemporal), vertex thinning, eventual complete baldness
- **Pathogenesis**: Androgen-mediated (dihydrotestosterone, genetic predisposition)
- **Age**: Starts after puberty

**Female Pattern Hair Loss**:
- **Prevalence**: 40% of women by age 70
- **Pattern**: Diffuse thinning over crown (Ludwig grading), preservation of frontal hairline
- **Pathogenesis**: Androgen-mediated (less than male)
- **Age**: Perimenopausal onwards

**Management**:
- **Topical minoxidil 5%**: BID, apply to scalp (men), 2% or 5% BID (women)
  - Onset: 4-6 months
  - Maintenance: Continue indefinitely
  - Side effects: Local irritation, hypertrichosis
- **Oral finasteride 1mg daily**: (men only)
  - Contraindicated in pregnancy (teratogenic)
  - Side effects: Sexual dysfunction (rare)
- **Hair transplant**: For suitable candidates (dermatology/plastic surgery)
- **Cosmetic**: Wigs, hairpieces, styling techniques

---

### ALOPECIA AREATA

**Pathogenesis**: Autoimmune (T-cell mediated attack on hair follicles)

**Clinical Features**:
- **Well-demarcated**, smooth, circular patches of hair loss
- **"Exclamation mark" hairs**: Short, broken hairs at periphery
- **Nail changes**: Pitting, ridging (20%)
- **Course**: Unpredictable (may regrow spontaneously, may recur or progress)

**Types**:
- **Alopecia areata patchy**: Localized patches (most common)
- **Alopecia totalis**: Complete scalp hair loss
- **Alopecia universalis**: Loss of all body hair

**Management**:
- **Observation** (for limited patches, may regrow spontaneously)
- **Intralesional steroid** (triamcinolone 10mg/mL): Every 4-6 weeks (for localized disease)
- **Topical steroids**: Potent steroid lotion/foam
- **Minoxidil**: Adjunct
- **Oral steroids** (for rapidly progressive): Prednisolone 200-300mg monthly (specialist)
- **Immunotherapy** (Diphenylcyclopropenone, Diphencyprone): For extensive disease (specialist)

---

### TELOGEN EFFLUVIUM

**Pathogenesis**: Premature transition of hair follicles to telogen (resting) phase

**Causes**:
- **Physiological**: Postpartum (3-6 months after delivery), severe illness, surgery
- **Psychological stress**: Major life events
- **Medications**: Retinoids, anticoagulants, anticonvulsants, β-blockers
- **Nutritional**: Iron deficiency, zinc deficiency, protein-calorie malnutrition
- **Endocrine**: Thyroid dysfunction

**Clinical Features**:
- **Diffuse hair shedding**: Increased hair fall (>100 hairs/day)
- **Acute onset**: 2-4 months after trigger
- **No scarring**: Scalp appears normal
- **Spontaneous recovery**: Within 6 months (if trigger removed)

**Management**:
- **Reassurance**: Self-limiting
- **Identify and correct** underlying cause
- **Iron supplementation**: If deficient
- **Minoxidil**: May accelerate recovery

---

### ANAGEN EFFLUVIUM

**Pathogenesis**: Interruption of anagen (growth) phase (hair matrix damage)

**Causes**:
- **Chemotherapy**: Most common cause
- **Radiation therapy**: Scalp irradiation
- **Toxins**: Thallium, arsenic
- **Alopecia totalis**: Potentially universal hair loss

**Clinical Features**:
- **Rapid hair loss**: Within weeks of exposure
- **Diffuse shedding**
- **Regrowth**: 3-6 months after cessation

**Management**:
- **Scalp cooling**: During chemotherapy (reduces hair loss)
- **Wigs**: For cosmetic purposes
- **Reassurance**: Regrowth expected

---

### SCARRING ALOPECIA (Cicatricial Alopecia)

**Pathogenesis**: Permanent destruction of hair follicles (replacement with fibrous tissue)

**Types**:

**1. Lichen Planopilaris**:
- **Clinical**: Perifollicular erythema, scaling, follicular keratotic plugs
- **Symptoms**: Pruritus, pain, burning
- **Nail changes**: Lichen planus of nails
- **Progression**: Irreversible hair loss

**2. Discoid Lupus Erythematosus**:
- **Clinical**: Follicular plugging, hypo- or hyperpigmentation, scarring
- **Distribution**: Scalp, face, ears
- **Systemic lupus**: May have systemic features

**3. Folliculitis Decalvans**:
- **Clinical**: Pustules, crusting, tufted folliculitis (multiple hairs from one follicle)
- **Pathogen**: *Staph aureus*

**Management**:
- **Dermatology referral** (urgent)
- **Biopsy**: For diagnosis
- **Treatment**:
  - **Intralesional steroid**: For early disease
  - **Oral steroid**: For active inflammation
  - **Hydroxychloroquine**: For LPP, DLE
  - **Doxycycline**: For folliculitis decalvans
  - **Immunosuppressants**: Methotrexate, mycophenolate (specialist)

---

### TRICHOTILLOMANIA

**Pathogenesis**: Compulsive hair pulling (psychological disorder)

**Clinical Features**:
- **Patchy hair loss**: Irregular shapes
- **Broken hairs**: Of varying lengths
- **No scarring**: Scalp normal
- **Age**: Children, adolescents

**Management**:
- **Psychological referral**: CBT, habit reversal therapy
- **SSRI**: May help

---

## NAIL DISORDERS

### ONYCHOMYCOSIS (Fungal Nail Infection)

**Pathogen**: Dermatophytes (most common), *Candida*, molds

**Clinical Features**:
- **Distal subungual onychomycosis** (most common):
  - Distal onycholysis
  - Subungual hyperkeratosis
  - Discolouration (yellow-white)
- **Proximal subungual onychomycosis**: Proximal spread (immunocompromised)
- **White superficial onychomycosis**: White powdery plaques on nail surface
- **Candidal onychomycosis**: Chronic paronychia, nail dystrophy (immunocompromised, wet work)

**Management**:
- **Confirm diagnosis**: Nail clipping microscopy + culture
- **Oral terbinafine 250mg daily**: 6 weeks (fingernails), 12 weeks (toenails)
- **Alternative**: Oral itraconazole (pulse therapy)
- **Topical**: Amorolfine, ciclopirox (mild disease only)
- **Adjunct**: Debride nail, keep short

---

### PSORIATIC NAIL DISEASE

**Clinical Features**:
- **Pitting**: Small depressions in nail plate
- **Onycholysis**: Separation of nail from nail bed (oil drop sign)
- **Subungual hyperkeratosis**: Crumbly debris under nail
- **Splinter haemorrhages**: Linear haemorrhages
- **Salmon patches**: Oil-drop discoloration

**Management**:
- **Treat underlying psoriasis**
- **Intralesional steroid**: Triamcinolone injection into nail matrix (painful)
- **Topical steroid**: Potent steroid lotion or ointment
- **Systemic therapy**: For extensive disease

---

### LICHEN PLANUS OF NAILS

**Clinical Features**:
- **Nail thinning**: Longitudinal grooving
- **Pterygium formation**: Scarring from proximal nail fold to nail plate
- **Nail loss**: Permanent

**Management**:
- **Intralesional steroid**
- **Systemic steroid**: For active inflammation
- **Referral**: To dermatology

---

### ACRODERMATITIS ENTEROPATHICA

**Pathogenesis**: Zinc deficiency

**Clinical Features**:
- **Nail dystrophy**: Onycholysis, nail loss
- **Periungual dermatitis**: Around nails
- **Alopecia**: Hair loss
- **Diarrhea**

**Management**: Zinc supplementation

---

### YELLOW NAIL SYNDROME

**Clinical Features**:
- **Yellow, thickened nails**: Slow growth
- **Lymphedema**: Lower extremity
- **Respiratory**: Chronic cough, bronchiectasis, pleural effusion

**Management**: Treat underlying cause (if identifiable)

---

### BEAU'S LINES

**Pathogenesis**: Transient interruption of nail matrix growth

**Causes**: Severe illness, high fever, malnutrition, chemotherapy

**Clinical Features**:
- **Transverse groove**: Across all nails
- **Timing**: Onset 2-3 weeks after event (distance from proximal nail fold correlates with timing)

**Management**: Reassurance (growth out)

---

### CLUBBING

**Pathogenesis**: Fibrovascular proliferation (associated with systemic disease)

**Causes**:
- **Respiratory**: Lung cancer, bronchiectasis, fibrosis, TB
- **Cardiovascular**: Cyanotic congenital heart disease, infective endocarditis
- **Gastrointestinal**: IBD, cirrhosis, coeliac disease
- **Idiopathic**: 10%

**Clinical Features**:
- **Loss of Lovibond angle**: Angle between nail and nail fold >180°
- **Nail bed sponginess**: Floating nail feel
- **Drumstick appearance**: Distal digit enlargement

**Management**: Investigate underlying cause

---

### KOILONYCHIA (Spoon Nails)

**Causes**: Iron deficiency, trauma, occupational

**Clinical Features**: Thin nails with central depression (spoon-shaped)

**Management**: Correct iron deficiency

---

### LEUKONYCHIA (White Nails)

**Types**:
- **Punctate**: Small white spots (trauma)
- **Striate**: Transverse white lines (trauma, Muehrcke's lines - hypoalbuminemia)
- **Total**: Entire nail white (hereditary, hepatic disease)

---

### ONYCHOGRYPHOSIS (Ram's Horn Nail)

**Causes**: Neglect, trauma, age, poor circulation

**Clinical Features**: Thickened, curved nail (ram's horn appearance)

**Management**: Podiatry referral for nail avulsion/debridement

---

**Sources**: BAD Hair and Nail Disorder Guidelines, NICE CKS**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "dermatology",
                "focus": "hair_nail_disorders",
                "sources": ["BAD Hair and Nail Disorder Guidelines", "NICE CKS"]
            }
        )

    def _handle_photoprotection(self, query: str, context: dict) -> DomainQueryResult:
        """Handle photoprotection and sun damage"""
        answer = """**PHOTOPROTECTION AND PHOTOAGING**

---

## ULTRAVIOLET RADIATION

**UV Spectrum**:
- **UVA (320-400nm)**: 95% of UV reaching earth surface
  - Penetrates deeper (dermis)
  - Causes photoaging, wrinkling, DNA damage, immunosuppression
  - Involved in photocarcinogenesis
- **UVB (280-320nm)**: 5% of UV reaching earth surface
  - Penetrates epidermis
  - Causes sunburn, erythema
  - Primary cause of non-melanoma skin cancer
- **UVC (100-280nm)**: Absorbed by ozone layer, does not reach earth

**Factors Affecting UV Intensity**:
- **Time**: Peak 10am-4pm (highest at solar noon)
- **Season**: Summer > winter
- **Latitude**: Closer to equator = higher UV
- **Altitude**: Higher altitude = higher UV
- **Reflection**: Snow, sand, water reflect UV (increase exposure)
- **Cloud cover**: UVA penetrates clouds (UVB partially blocked)

---

## PHOTOPROTECTION STRATEGIES

### 1. BEHAVIORAL MEASURES

**Sun Avoidance**:
- **Avoid peak sun**: 10am-4pm (or 11am-3pm)
- **Seek shade**: Especially during peak hours
- **Plan activities**: Early morning or late afternoon

### 2. CLOTHING PROTECTION

**UPF (Ultraviolet Protection Factor)**:
- **UPF 15-24**: Good protection (93-96% UV blocked)
- **UPF 25-39**: Very good (96-97% UV blocked)
- **UPF 40-50+**: Excellent (97.5-99% UV blocked)

**Clothing Features**:
- **Tight weave**: Better protection
- **Dark colours**: Better than light
- **Long sleeves, long trousers**: Cover more skin
- **Hats**: Wide-brimmed (>7cm), legionnaire style (covers ears, neck)
- **Sunglasses**: Wrap-around, UV 400 label (blocks UVA and UVB)

### 3. SUNSCREEN

**SPF (Sun Protection Factor)**:
- Measures protection against UVB only
- **SPF calculation**: Time to burn with sunscreen ÷ time to burn without sunscreen
- **SPF 15**: Blocks 93% UVB
- **SPF 30**: Blocks 97% UVB
- **SPF 50**: Blocks 98% UVB
- **SPF 50+**: Blocks >98% UVB

**UVA Protection**:
- **Star rating** (UK): 0-5 stars (higher = better UVA protection)
- **UVA circle** (EU): UVA inside circle if meets EU standard (UVA protection at least 1/3 of SPF)
- **Broad spectrum**: Protects against UVA and UVB

**Sunscreen Types**:

**Chemical (Organic)**:
- Absorb UV radiation
- Examples: Oxybenzone, avobenzone, octocrylene, octinoxate
- May cause irritation, allergy
- Require application 15-30 minutes before sun exposure

**Physical (Inorganic)**:
- Reflect/scatter UV radiation
- Examples: Zinc oxide, titanium dioxide
- Less irritating, better for sensitive skin
- May leave white cast

**Application**:
- **Amount**: 2mg/cm² (1/4 teaspoon for face, 1/2 teaspoon for each arm, 1 teaspoon for each leg, front/back torso)
- **Timing**: 15-30 minutes before sun exposure
- **Frequency**: Reapply every 2 hours, after swimming, sweating, toweling
- **Common mistake**: Under-application (most people apply 25-50% of required amount)

**Water Resistance**:
- **Water-resistant**: 40 minutes water immersion
- **Very water-resistant**: 80 minutes water immersion

---

## PHOTODERMATOSES (ABNORMAL LIGHT SENSITIVITY)

### POLYMORPHIC LIGHT ERUPTION (PLE)

**Most common photodermatosis**

**Pathogenesis**: Delayed-type hypersensitivity to unknown photoallergen

**Clinical Features**:
- **Onset**: Hours to days after sun exposure
- **Rash**: Pruritic papules, vesicles, plaques
- **Distribution**: Sun-exposed areas (face, neck, arms, hands, "V" of neck, dorsum of hands)
- **Sparing**: Areas chronologically exposed (face, dorsal hands) may be less affected ("hardening")
- **Season**: Spring/summer (improves as season progresses - hardening)

**Management**:
- **Photoprotection**: Sun avoidance, clothing, sunscreen
- **Desensitization**: PUVA or narrowband UVB (hardening effect)
- **Prophylaxis**: Antihistamines, short course of steroid (severe)

---

### SOLAR URTICARIA

**Immediate hypersensitivity** to UV radiation

**Clinical Features**:
- **Onset**: Minutes after sun exposure
- **Rash**: Wheals, erythema, pruritus at sun-exposed sites
- **Systemic**: Headache, syncope, bronchospasm (rare, severe)

**Management**:
- **Photoprotection**: High-SPF sunscreen, clothing
- **Antihistamines**: High-dose (up to 4x standard dose)
- **Phototherapy**: PUVA desensitization
- **Omalizumab** (anti-IgE): For refractory cases (specialist)

---

### CHRONIC ACTINIC DERMATITIS

**Persistent eczema** in sun-exposed areas

**Risk Factors**: Older men, outdoor workers

**Clinical Features**:
- **Eczematous plaques**: Sun-exposed areas
- **May become**: Generalized (eczema spreads to covered areas)
- **Year-round**: Persists in winter

**Management**:
- **Rigorous photoprotection**
- **Topical steroids**: Potent
- **Systemic steroids**: For flares
- **Azathioprine**: Specialist

---

### PORPHYRIAS

**Disorders of heme biosynthesis** (accumulation of photosensitizing porphyrins)

**Types**:

**Porphyria Cutanea Tarda (PCT)** (most common):
- **Blistering**: Fragile vesicles, bullae on hands, forearms
- **Milium**: Small white cysts after healing
- **Hypertrichosis**: Facial hair growth
- **Sclerosis**: Thickening, scarring
- **Triggers**: Alcohol, estrogen, iron, hepatitis C, HIV, smoking

**Erythropoietic Protoporphyria (EPP)**:
- **Immediate burning**: Pain, stinging, pruritus within minutes of sun exposure
- **Edema**, erythema (no blisters)
- **Wheal-like** lesions

**Management**:
- **Strict sun avoidance**
- **Protective clothing** (opaque)
- **PCT treatment**: Phlebotomy, chloroquine, avoid triggers
- **EPP treatment**: Afamelanotide (implant), β-carotene (specialist)

---

### DRUG-INDUCED PHOTOSENSITIVITY

**Phototoxicity**:
- **Dose-dependent**, resembles sunburn
- **Caused by**: Doxycycline, tetracycline, NSAIDs, amiodarone, thiazides, psoralens, voriconazole
- **Timing**: Within hours of sun exposure
- **Management**: Discontinue drug if possible, photoprotection

**Photoallergy**:
- **Immunologic**, dose-independent
- **Caused by**: Ketoprofen, piroxicam, sulfonamides, phenothiazines
- **Timing**: 24-72 hours after sun exposure
- **Management**: Discontinue drug, photoprotection, avoid cross-reactive drugs

---

## PHOTOAGING

**Clinical Features**:
- **Fine lines**, wrinkles (crow's feet, forehead)
- **Dyspigmentation**: Solar lentigines ("age spots"), ephelides (freckles), mottled pigmentation
- **Telangiectasia**: Visible blood vessels
- **Loss of elasticity**: Leathery, sagging skin
- **Texture changes**: Coarseness, roughness
- **Precancerous lesions**: Actinic keratoses

**Prevention**:
- **Strict photoprotection** (never too late to start)
- **Avoid tanning beds**

**Treatment** (cosmetic):
- **Topical retinoids** (tretinoin): Improves fine lines, dyspigmentation
- **Chemical peels**: Glycolic acid, salicylic acid
- **Laser**: Ablative (CO2), non-ablative, IPL
- **Dermal fillers**, botulinum toxin

---

## ACTINIC KERATOSES (Solar Keratoses)

**Pathogenesis**: Chronic UV exposure, pre-malignant

**Clinical Features**:
- **Rough, scaly plaques**: Sun-exposed areas
- **Base**: Erythematous
- **Size**: 1cm to several cm
- **Multiple**: Often multiple lesions

**Management**:
- **Cryotherapy**: Liquid nitrogen (most common)
- **Topical**: 5-fluorouracil BID for 4 weeks (if multiple lesions)
- **Topical**: Imiquimod 3x weekly for 4-16 weeks
- **Photodynamic therapy**: For large lesions

**Progression to SCC**: ~10% if untreated

---

## TANNING BEDS

**Risks**:
- **Melanoma**: 75% increased risk (first use before age 35)
- **Non-melanoma skin cancer**: BCC, SCC
- **Photoaging**: Wrinkles, dyspigmentation
- **Eye damage**: Cataracts, ocular melanoma

**WHO**: Classifies tanning beds as **carcinogenic to humans** (Group 1)

**Recommendation**: **NEVER use tanning beds**

---

## VITAMIN D

**Photoprotection** may reduce vitamin D synthesis:

**Risk Factors for Deficiency**:
- Strict sun avoidance
- Darker skin (more melanin)
- Elderly
- Winter months (high latitudes)
- Clothing coverage

**Management**:
- **Vitamin D supplementation**: Consider 10-20 mcg (400-800 IU) daily
- **Dietary sources**: Fatty fish, fortified foods
- **Monitoring**: 25-hydroxyvitamin D levels if at risk

---

## PHOTOPROTECTION SUMMARY

**Primary Prevention**:
1. **Sun avoidance**: 10am-4pm peak
2. **Clothing**: UPF 50+, wide-brimmed hat, sunglasses
3. **Sunscreen**: SPF 30+ (broad spectrum), 15-30 min before exposure, reapply every 2 hours

**Special Populations**:
- **Children**: Strict photoprotection (severe sunburns in childhood increase melanoma risk)
- **Fair skin, red hair**: High risk, very strict photoprotection
- **Immunosuppressed**: Higher risk of skin cancer, strict photoprotection
- **Personal/family history of skin cancer**: Strict photoprotection

**Regular Skin Checks**:
- **Self-examination**: Monthly (ABCDE criteria, "ugly duckling" sign)
- **Professional examination**: Annually (or more frequently if high risk)
- **Photographic documentation**: For surveillance

---

**Sources**: BAD Photoprotection Guidelines, NICE Sunbed Guidelines, AAD Guidelines**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "dermatology",
                "focus": "photoprotection_sun_damage",
                "sources": ["BAD Photoprotection Guidelines", "NICE Sunbed Guidelines", "AAD Guidelines"]
            }
        )

    def _handle_general_dermatology(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general dermatology consultation"""
        answer = """**GENERAL DERMATOLOGY CONSULTATION**

Dermatology covers the diagnosis and management of skin, hair, and nail conditions.

**Common Conditions Managed**:
- **Acne and rosacea**: Spots, pimples, flushing, facial redness
- **Eczema and dermatitis**: Dry, itchy, inflamed skin (atopic, contact, seborrhoeic)
- **Psoriasis**: Scaly, silvery plaques, often on elbows, knees, scalp
- **Skin infections**: Bacterial (impetigo, cellulitis), fungal (tinea, athlete's foot), viral (warts, herpes, shingles)
- **Acne and rosacea**: Comedonal, inflammatory, cystic acne
- **Rash evaluation**: By morphology, distribution, timing
- **Hair and nail disorders**: Alopecia, fungal nails, nail dystrophy
- **Sun damage**: Actinic keratoses, photoaging, skin cancer prevention
- **Allergies**: Contact dermatitis, urticaria, drug eruptions

**Diagnostic Approach**:
- **History**: Onset, progression, triggers, symptoms, medications
- **Examination**: Morphology (lesion type), distribution, arrangement, color
- **Special tests**: Dermoscopy, skin scraping, patch testing, biopsy

**When to Seek Urgent Review**:
- **Rapidly changing lesion**: Growing, bleeding, ulcerating
- **Non-blanching rash**: Purpura, meningococcal sepsis
- **Severe skin reactions**: Widespread blistering (SJS/TEN), erythroderma
- **Severe cellulitis**: Spreading redness, fever, systemic symptoms

**Sources**: BAD Guidelines, NICE Dermatology Guidelines, PCDS Handbook**
"""

        return DomainQueryResult(
            domain_name="dermatology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "dermatology",
                "focus": "general_consultation",
                "sources": ["BAD Guidelines", "NICE Dermatology Guidelines", "PCDS Handbook"]
            }
        )


def create_dermatology_domain():
    """Factory function to create dermatology domain instance"""
    return DermatologyDomain()


# Domain registration
try:
    from gpdisc_core.domains.registry import DomainModuleRegistry
    DomainModuleRegistry.register(DermatologyDomain)
except ImportError:
    # Registry not available yet
    pass
