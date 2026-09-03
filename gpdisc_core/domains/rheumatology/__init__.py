"""
GPDISC Rheumatology Domain Module

This module provides rheumatological consultation capabilities including:
- Inflammatory arthritis (RA, PsA, AS, gout, pseudogout)
- Connective tissue diseases (SLE, Sjögren's, scleroderma, myositis)
- Osteoarthritis and degenerative joint disease
- Back pain and spinal disorders
- Vasculitis (GCA, polymyalgia rheumatica, others)
- Soft tissue rheumatism (tendinopathies, bursitis)
- Bone health (osteoporosis, Paget's disease)
- Pediatric rheumatology (JIA, Kawasaki disease)

Evidence-based with guidelines from:
- British Society for Rheumatology (BSR)
- NICE Rheumatology Guidelines
- EULAR (European Alliance of Associations for Rheumatology)
- ACR (American College of Rheumatology)
"""

from typing import Optional, Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class RheumatologyDomain(BaseDomainModule):
    """
    Rheumatology specialty domain for musculoskeletal and autoimmune diseases.

    Covers comprehensive rheumatological consultation including:
    - Inflammatory arthritis (RA, PsA, AS, gout, pseudogout)
    - Connective tissue diseases (SLE, Sjögren's, scleroderma, myositis)
    - Osteoarthritis and degenerative joint disease
    - Back pain and spinal disorders
    - Vasculitis (GCA, PMR, others)
    - Soft tissue rheumatism (tendinopathies, bursitis)
    - Bone health (osteoporosis, Paget's disease)
    - Pediatric rheumatology (JIA, Kawasaki disease)
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="rheumatology",
            version="1.0.0",
            dependencies=[],
            description="Rheumatology: Arthritis, autoimmune diseases, connective tissue disorders, vasculitis, osteoporosis",
            keywords=[
                "rheumatology", "rheumatologist", "arthritis", "joint pain", "joint swelling", "joint stiffness",
                "rheumatoid arthritis", "ra", "seropositive", "seronegative",
                "osteoarthritis", "oa", "degenerative", "wear and tear",
                "gout", "pseudogout", "cppd", "crystal arthritis",
                "ankylosing spondylitis", "as", "spondyloarthritis", "spondylitis",
                "psoriatic arthritis", "psa",
                "lupus", "sle", "systemic lupus erythematosus",
                "sjogren's", "sicca", "dry eyes", "dry mouth",
                "scleroderma", "systemic sclerosis", "crest",
                "myositis", "polymyositis", "dermatomyositis",
                "vasculitis", "giant cell arteritis", "gca", "temporal arteritis",
                "polymyalgia rheumatica", "pmr",
                "back pain", "low back pain", "sciatica",
                "osteoporosis", "bone density", "fragility fracture",
                "paget's disease", "paget",
                "tendinitis", "tendinopathy", "bursitis",
                "fibromyalgia", "chronic widespread pain",
                "jia", "juvenile idiopathic arthritis", "still's disease",
                "kawasaki disease",
                "raynaud's", "raynauds",
                "sarcoidosis"
            ],
            capabilities=[
                "inflammatory_arthritis", "connective_tissue_diseases", "osteoporosis",
                "vasculitis", "back_pain_management", "soft_tissue_rheumatism",
                "pediatric_rheumatology", "autoimmune_diseases"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Process rheumatology queries with appropriate specialty routing"""
        query_lower = query.lower()

        # Emergencies - HIGHEST PRIORITY
        if any(term in query_lower for term in ["giant cell arteritis", "gca", "temporal arteritis", "blindness", "vision loss temporal"]):
            return self._handle_gca(query, context)

        elif any(term in query_lower for term in ["septic arthritis", "infected joint", "joint infection"]):
            return self._handle_septic_arthritis(query, context)

        # Inflammatory arthritis
        elif any(term in query_lower for term in ["rheumatoid arthritis", "ra", "seropositive", "seronegative"]):
            return self._handle_ra(query, context)

        elif any(term in query_lower for term in ["gout", "podagra"]):
            return self._handle_gout(query, context)

        elif any(term in query_lower for term in ["pseudogout", "cppd", "calcium pyrophosphate"]):
            return self._handle_pseudogout(query, context)

        elif any(term in query_lower for term in ["ankylosing spondylitis", "as", "spondylitis", "spondyloarthritis"]):
            return self._handle_as(query, context)

        elif any(term in query_lower for term in ["psoriatic arthritis", "psa"]):
            return self._handle_psa(query, context)

        # Connective tissue diseases
        elif any(term in query_lower for term in ["lupus", "sle", "systemic lupus erythematosus"]):
            return self._handle_sle(query, context)

        elif any(term in query_lower for term in ["sjogren", "sjogren's", "sicca", "dry eyes"]):
            return self._handle_sjogrens(query, context)

        elif any(term in query_lower for term in ["scleroderma", "systemic sclerosis", "crest"]):
            return self._handle_scleroderma(query, context)

        elif any(term in query_lower for term in ["myositis", "polymyositis", "dermatomyositis"]):
            return self._handle_myositis(query, context)

        elif any(term in query_lower for term in ["vasculitis", "gca", "pmr", "henoch-schönlein", "kawasaki"]):
            return self._handle_vasculitis(query, context)

        # Degenerative and mechanical
        elif any(term in query_lower for term in ["osteoarthritis", "oa", "degenerative", "wear and tear"]):
            return self._handle_oa(query, context)

        elif any(term in query_lower for term in ["back pain", "low back pain", "lbp", "sciatica"]):
            return self._handle_back_pain(query, context)

        # Soft tissue
        elif any(term in query_lower for term in ["fibromyalgia", "chronic widespread pain", "tender points"]):
            return self._handle_fibromyalgia(query, context)

        elif any(term in query_lower for term in ["tendinitis", "tendinopathy", "bursitis", "rotator cuff"]):
            return self._handle_soft_tissue(query, context)

        # Bone health
        elif any(term in query_lower for term in ["osteoporosis", "bone density", "fragility fracture", "compression fracture"]):
            return self._handle_osteoporosis(query, context)

        elif any(term in query_lower for term in ["paget's", "paget"]):
            return self._handle_paget(query, context)

        # Pediatric
        elif any(term in query_lower for term in ["jia", "juvenile idiopathic arthritis", "still's disease"]):
            return self._handle_jia(query, context)

        # General rheumatology
        else:
            return self._handle_general_rheumatology(query, context)

    def _handle_gca(self, query: str, context: dict) -> DomainQueryResult:
        """Handle giant cell arteritis - EMERGENCY"""
        answer = """**GIANT CELL ARTERITIS (TEMPORAL ARTERITIS) - MEDICAL EMERGENCY**

**⚠️ URGENT: Irreversible blindness can occur without prompt treatment**

---

## DEFINITION

**Granulomatous vasculitis** of medium and large arteries, especially branches of carotid artery (temporal artery)

---

## EPIDEMIOLOGY

**Age**: >50 years (rare <50)
**Female**: (2-3:1 female:male ratio)
**Prevalence**: (increases with age, highest >70 years)
**Association**: with Polymyalgia Rheumatica (PMR)

---

## CLINICAL FEATURES

**Headache** (most common):
- **New-onset**, localized to temporal region
- **Severity**: (variable, often severe)
- **Duration**: (persistent, >4 weeks)

**Scalp Tenderness**:
- **Temporal artery**: (tender to touch, painful when brushing hair)
- **Nodularity**: (thickened, tender, pulseless artery)

**Jaw Claudication**:
- **Pain**: (jaw, masseter muscles with chewing)
- **Fatigue**: (unable to continue eating)
- **Resolves**: with rest

**Visual Symptoms** (EMERGENCY):
- **Amaurosis fugax**: (transient vision loss, "shade coming down")
- **Permanent vision loss**: (anterior ischemic optic neuropathy)
- **Diplopia**: (double vision)
- **Ocular pain**

**Systemic**:
- **PMR symptoms**: (proximal muscle stiffness, shoulders, hips)
- **Fever**, malaise, weight loss
- **Anorexia**
- **Anemia**

**Other Ischemic Symptoms**:
- **Limb claudication**: (arm claudication if axillary arteries involved)
- **Neck pain**, tongue claudication

---

## RED FLAGS: EMERGENCY

- **Visual symptoms**: (amaurosis fugax, vision loss - URGENT)
- **Jaw claudication**
- **Scalp necrosis**
- **Stroke**, TIA

---

## DIAGNOSIS

**Clinical**: (high index of suspicion in elderly with new headache)

**Blood Tests** (do NOT delay treatment):
- **ESR**: (usually >50 mm/hr, often >100)
- **CRP**: (elevated, often >50 mg/L)
- **FBC**: (normocytic anemia, thrombocytosis)
- **LFTs**: (ALP often elevated)

**Temporal Artery Biopsy** (confirmatory):
- **Indication**: (all suspected cases)
- **Timing**: (within 2 weeks of starting steroids, can still be positive up to 2 weeks)
- **Histology**: (granulomatous inflammation, giant cells, intimal hyperplasia)
- **Sensitivity**: (80-90% - skip areas may cause false negative)

**Imaging** (if biopsy negative or high suspicion):
- **Temporal artery ultrasound**: (halo sign - edema of vessel wall)
- **PET-CT**: (FDG uptake in large vessels)

---

## MANAGEMENT

**IF SUSPECTED GCA - START HIGH-DOSE STEROIDS IMMEDIATELY** (DO NOT WAIT FOR BIOPSY)

**Initial Treatment**:
- **Prednisolone 40-60mg daily**: (40mg if no visual symptoms, 60mg if visual symptoms)
- **Timing**: (start immediately, before biopsy, before ESR/CRP results)
- **Duration**: (continue until biopsy, then if positive, continue treatment)

**Visual Loss** (EMERGENCY):
- **IV methylprednisolone**: (500mg-1g daily for 3 days)
- **Urgent ophthalmology referral**: (same day)
- **Admit**: (for IV steroids, monitoring)

**Oral Steroid Taper** (after initial 2-4 weeks):
- **Reduce by 10mg** every 2-4 weeks until 20mg daily
- **Then reduce by 2.5mg** every 2-4 weeks until 10mg daily
- **Then reduce by 1mg** every 1-2 months until 0
- **Duration**: (usually 12-18 months, some may need longer)

**Adjunctive Therapy** (for steroid-sparing):
- **Methotrexate**: (10-20mg weekly, if relapsing, unable to taper steroids)
- **Tocilizumab**: (IL-6 receptor antagonist, 162mg SC weekly - reduces relapse, steroid-sparing)

**Monitoring**:
- **ESR, CRP**: (baseline, 2-4 weeks, then every 1-3 months)
- **Symptoms**: (headache, scalp tenderness, PMR symptoms)
- **Steroid side effects**: (glucose, BP, bone density, cataracts)

---

## POLYMYALGIA RHEUMATICA (PMR)

**Association**: (50% of GCA patients have PMR)
**Symptoms**: (proximal muscle stiffness, shoulders, hips, morning stiffness >45 minutes)
**Management**: (treat as GCA if coexisting, prednisolone 15mg daily for isolated PMR)

---

## PROGNOSIS

**Good**: (with prompt treatment)
**Complications**:
- **Blindness**: (if untreated, irreversible)
- **Aortic aneurysm**: (thoracic aortic aneurysm increased risk, monitor with imaging)
- **Stroke**, TIA: (increased risk)
- **Relapses**: (15-20% during taper)

---

## PATIENT ADVICE

- **Take steroids**: (as prescribed, do NOT stop suddenly)
- **Report visual changes**: (immediately - go to A&E)
- **Vaccinations**: (flu, pneumococcal, shingles - consider before starting steroids if possible)
- **Bone protection**: (calcium, vitamin D, bisphosphonate if risk factors)
- **Steroid card**: (carry)
- **Medical alert**: (bracelet if on long-term steroids)

---

## WHEN TO REFER

**Urgent** (same day):
- **Suspected GCA**: (especially with visual symptoms, jaw claudication)
- **Visual loss**: (EMERGENCY)

**Routine**:
- **PMR**: (for diagnosis, management)
- **Relapse**: (during taper)

---

**Sources: BSR Guidelines Giant Cell Arteritis 2020, NICE NG158 Polymyalgia Rheumatica and Giant Cell Arteritis, ACR Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.97,
            metadata={
                "specialty": "rheumatology",
                "focus": "giant_cell_arteritis",
                "urgency": "emergency",
                "sources": ["BSR GCA Guidelines 2020", "NICE NG158", "ACR Guidelines"]
            }
        )

    def _handle_septic_arthritis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle septic arthritis - EMERGENCY"""
        answer = """**SEPTIC ARTHRITIS - ORTHOPAEDIC EMERGENCY**

**⚠️ URGENT: Joint destruction can occur within days without prompt treatment**

---

## DEFINITION

**Bacterial infection** of joint space

---

## PATHOGENS

**Staphylococcus aureus** (most common, 50-70%)
**Streptococcus** (20-30%)
**Gram-negative**: (E. coli, Pseudomonas - risk factors: IV drug use, immunocompromised)
**Neisseria gonorrhoeae**: (sexually active young adults)

---

## RISK FACTORS

- **Pre-existing arthritis**: (RA, OA)
- **Joint surgery**: (arthroscopy, replacement)
- **Joint injection**: (recent steroid injection)
- **Skin infection**: (cellulitis, abscess)
- **Trauma**: (penetrating injury)
- **IV drug use**
- **Immunocompromised**: (diabetes, HIV, immunosuppression)
- **Prosthetic joint**: (higher risk, different pathogens)

---

## CLINICAL FEATURES

**Typical Presentation**:
- **Single joint**: (acute, severe)
- **Knee** (most common), hip, shoulder, ankle, wrist
- **Pain**: (severe, weight-bearing impossible if lower limb)
- **Swelling**: (rapid, tense effusion)
- **Erythema**, warmth
- **Fever**: (present in 60-80%)
- **Inability to move joint**: (pseudoparalysis)

**Hip Infection** (children):
- **Pain**: (hip, thigh, knee referred)
- **Limp**: (refusal to walk)
- **Position**: (hip flexed, externally rotated, abducted)
- **Fever** (may be absent in infants)

**Gonococcal Arthritis**:
- **Migratory arthralgia**: (especially wrists, ankles, knees)
- **Tenosynovitis**: (especially fingers, wrists)
- **Rash**: (pustular, vesicular on extremities)
- **Sexually active**: young adults

---

## DIAGNOSIS

**Clinical suspicion**: (single hot swollen joint)

**Investigations**:
- **Joint aspiration**: (critical, do NOT delay antibiotics)
  - **Cell count**: WBC >50,000/mm³ (suggestive), >100,000 (diagnostic)
  - **Gram stain**: (positive in 50-70%)
  - **Culture**: (gold standard, takes 24-48 hours)
  - **Crystals**: (exclude gout/pseudogout)
- **Blood cultures**: (positive in 50%)
- **FBC**: (leukocytosis)
- **CRP/ESR**: (elevated)

**Imaging**:
- **X-ray**: (soft tissue swelling, effusion, exclude other causes)
- **Ultrasound**: (confirm effusion, guide aspiration)
- **MRI**: (if hip or spine infection, or diagnosis uncertain)

---

## MANAGEMENT

**ADMIT**: (all suspected cases, for IV antibiotics, drainage)

**Do NOT Delay Antibiotics** for aspiration if infection suspected

**Empirical IV Antibiotics** (after cultures):

**If >50 years** or comorbidities:
- **Flucloxacillin 2g QDS** (IV) OR
- **Ceftriaxone 2g OD** (IV) (if MRSA risk, gram-negative risk)

**If <50 years**, sexually active:
- **Ceftriaxone 2g OD** (IV) + **Azithromycin 1g** (single dose, then 500mg OD) (covers gonococcus)

**If MRSA risk**: (IV drug use, healthcare contact, previous MRSA)
- **Vancomycin** (IV)

**Duration**: (4-6 weeks, depending on organism, response)

---

**Joint Drainage**:
- **Needle aspiration**: (daily aspiration until dry)
- **Surgical drainage**: (arthroscopic or open washout - especially for hip, shoulder, or if no improvement with aspiration)

---

**Prosthetic Joint Infection**:
- **Urgent orthopedic referral**
- **Multiple samples**: (tissue, fluid, intraoperative)
- **Treatment**: (surgical debridement, prosthesis removal, 6 weeks IV antibiotics, revision arthroplasty)

---

## DIFFERENTIAL DIAGNOSIS

**Crystal Arthritis**: (gout, pseudogout) - diagnose with joint aspiration, polarized microscopy

**Atraumatic Hemarthrosis**: (trauma, coagulopathy, anticoagulation)

**Inflammatory Arthritis**: (RA flare - usually polyarticular)

**Reactive Arthritis**: (post-infection)

**Palindromic Rheumatism**: (intermittent attacks)

**Villonodular Synovitis**: (pigmented villonodular synovitis)

---

## RED FLAGS: URGENT REFERRAL

- **Suspected septic arthritis**: (single hot swollen joint)
- **Prosthetic joint infection**
- **Spinal infection**: (epidural abscess, vertebral osteomyelitis - neurological symptoms)

---

## PROGNOSIS

**Good**: (with prompt treatment)
**Complications** (if delayed):
- **Joint destruction**: (permanent damage)
- **Osteomyelitis**
- **Sepsis**, death (10-15% mortality, especially elderly)

---

**Sources: NICE CKS Septic Arthritis, BSR Guidelines, MIMS Septic Arthritis**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.96,
            metadata={
                "specialty": "rheumatology",
                "focus": "septic_arthritis",
                "urgency": "emergency",
                "sources": ["NICE CKS", "BSR Guidelines", "MIMS"]
            }
        )

    def _handle_ra(self, query: str, context: dict) -> DomainQueryResult:
        """Handle rheumatoid arthritis"""
        answer = """**RHEUMATOID ARTHRITIS (RA)**

---

## DEFINITION

**Chronic, systemic autoimmune disease** primarily affecting joints, causing synovial inflammation, cartilage damage, bone erosion

---

## EPIDEMIOLOGY

**Prevalence**: 0.5-1% (women 2-3x more than men)
**Age**: 35-50 years (peak onset)
**Genetic**: HLA-DRB1 (shared epitope)

---

## CLINICAL FEATURES

**Joint Symptoms**:
- **Hands**: (MCP, PIP joints - sparing DIP joints)
- **Feet**: (MTP joints)
- **Symmetrical**: (usually)
- **Morning stiffness**: (>30 minutes, often >1 hour)
- **Pain**: (inflammatory - worse with rest, improves with activity)
- **Swelling**, warmth
- **Functional limitation**: (grip strength, dexterity)

**Extra-Articular Manifestations**:
- **Rheumatoid nodules**: (extensor surfaces, olecranon, pressure points)
- **Lung**: (interstitial lung disease, pleural effusion, nodules)
- **Heart**: (pericarditis, myocarditis, accelerated atherosclerosis)
- **Eye**: (scleritis, episcleritis, dry eyes - secondary Sjögren's)
- **Vasculitis**: (skin ulcers, mononeuritis multiplex, cutaneous vasculitis)
- **Blood**: (anemia of chronic disease, Felty's syndrome - splenomegaly + neutropenia)
- **Cervical spine**: (atlantoaxial subluxation - neck pain, myelopathy)

---

## DIAGNOSIS

**ACR/EULAR 2010 Criteria** (for early RA):

**Involvement** (score 0-5):
- **1 large joint**: (0)
- **2-10 large joints**: (1)
- **1-3 small joints** (with or without large joints): (2)
- **4-10 small joints** (with or without large joints): (3)
- **>10 joints** (at least 1 small joint): (5)

**Serology** (score 0-3):
- **RF** and **ACPA** negative: (0)
- **RF** or **ACPA** low positive: (2)
- **RF** or **ACPA** high positive: (3)

**Acute Phase Reactants** (score 0-1):
- **CRP** and **ESR** normal: (0)
- **CRP** or **ESR** abnormal: (1)

**Duration** (score 0-2):
- **<6 weeks**: (0)
- **≥6 weeks**: (2)

**Score ≥6** = definite RA

---

**Investigations**:
- **RF**: (rheumatoid factor - present in 70-80%, not specific)
- **ACPA**: (anti-citrullinated protein antibody - more specific, present in 60-70%)
- **CRP**, **ESR**: (elevated)
- **FBC**: (anemia, thrombocytosis)
- **X-ray**: (hands, feet - periarticular osteopenia, erosions, joint space narrowing)
- **Ultrasound/MRI**: (early synovitis, erosions before X-ray)

---

## MANAGEMENT

**Treat to Target**: (aim for remission or low disease activity)

**Early Treatment**: (within 3 months of diagnosis improves outcome)

**First-line DMARD**:
- **Methotrexate**: (10-20mg weekly, folic acid 5mg weekly) - **anchor drug**
  - **Side effects**: (nausea, mouth ulcers, liver toxicity, myelosuppression, pneumonitis)
  - **Monitoring**: (FBC, LFTs, CRP baseline, then every 1-3 months)
  - **Alcohol**: (avoid excess, regular LFTs)

**Alternatives**: (if methotrexate contraindicated, intolerant, inadequate response)
- **Leflunomide**: (20mg daily)
- **Sulfasalazine**: (2-3g daily)
- **Hydroxychloroquine**: (200-400mg daily)

**Combination DMARDs**:
- **Methotrexate + Hydroxychloroquine ± Sulfasalazine**

**Biologics** (if inadequate response to conventional DMARDs):
- **Anti-TNF**: (etanercept, adalimumab, certolizumab, golimumab)
- **Anti-IL-6**: (tocilizumab)
- **B-cell depletion**: (rituximab)
- **T-cell costimulation blocker**: (abatacept)
- **IL-1 inhibitor**: (anakinra)

**JAK Inhibitors** (targeted synthetic DMARDs):
- **Tofacitinib**, **Baricitinib**

**Adjunctive**:
- **NSAIDs**: (for symptom control while waiting for DMARD effect)
- **Glucocorticoids**: (bridging therapy - prednisolone 5-10mg daily for 4-8 weeks, then taper)
- **Intra-articular steroids**: (for flare of single joint)

---

## MONITORING

**Disease Activity**:
- **DAS28**: (Disease Activity Score using 28 joints)
- **Remission**: DAS28 <2.6
- **Low**: 2.6-3.2
- **Moderate**: 3.2-5.1
- **High**: >5.1

**DMARD Toxicity Monitoring**:
- **Methotrexate**: (FBC, LFTs, CRP baseline, 2 weeks, then every 1-3 months)
- **Leflunomide**: (FBC, LFTs, BP baseline, then monthly for 6 months, then every 2 months)
- **Sulfasalazine**: (FBC, LFTs baseline, then every 3 months)
- **Hydroxychloroquine**: (baseline eye examination, then annually)

---

## PROGNOSIS

**Variable**: (5% mild, 90% moderate, 5% severe)
**Worse with**: (RF/ACPA positive, high disease activity, early erosions, extra-articular manifestations, smoking)
**Mortality**: (reduced life expectancy by 5-10 years, mainly cardiovascular)

---

## LIFESTYLE

- **Smoking cessation**: (major risk factor, worsens disease, reduces treatment response)
- **Exercise**: (maintains joint mobility, muscle strength, cardiovascular health)
- **Joint protection**: (avoid repetitive stress, use assistive devices)
- **Vaccinations**: (flu, pneumococcal, shingles - before immunosuppression if possible)
- **Pregnancy**: (plan, switch to safe medications, teratogenic drugs contraindicated)

---

## COMPLICATIONS

**Cervical Spine**:
- **Atlantoaxial subluxation**: (anterior, posterior, vertical, subaxial)
- **Symptoms**: (neck pain, myelopathy - weakness, numbness, gait disturbance)
- **Management**: (urgent neurosurgery referral if myelopathy, cervical spine fusion if unstable)

**Osteoporosis**: (secondary to inflammation, steroids)
**Cardiovascular**: (accelerated atherosclerosis)
**Infection**: (increased risk with immunosuppression)

---

## WHEN TO REFER

**Urgent**:
- **Atlantoaxial subluxation** with myelopathy

**Routine**:
- **Suspected RA**: (for early diagnosis, DMARD initiation)
- **Extra-articular manifestations**: (lung involvement, vasculitis)
- **Pregnancy planning**: (for medication review)

---

**Sources: NICE NG100 Rheumatoid Arthritis, BSR RA Guidelines 2021, EULAR Recommendations**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "rheumatology",
                "focus": "rheumatoid_arthritis",
                "sources": ["NICE NG100", "BSR RA Guidelines 2021", "EULAR Recommendations"]
            }
        )

    def _handle_gout(self, query: str, context: dict) -> DomainQueryResult:
        """Handle gout"""
        answer = """**GOUT**

---

## DEFINITION

**Crystal-induced arthritis** caused by deposition of monosodium urate crystals in joints and soft tissues

---

## PATHOPHYSIOLOGY

**Hyperuricemia**: (serum urate >6.8 mg/dL or >400 µmol/L)
- **Overproduction**: (purine metabolism, cell turnover)
- **Underexcretion**: (90% - renal)

**Uric Acid** → **Urate Crystals** → **Inflammation** (via NLRP3 inflammasome, IL-1β)

---

## RISK FACTORS

**Modifiable**:
- **Alcohol**: (especially beer, spirits)
- **Diet**: (purine-rich foods - red meat, seafood, fructose)
- **Obesity**
- **Diuretics**: (thiazides, loop diuretics)
- **Dehydration**
- **Weight gain**

**Non-modifiable**:
- **Genetics**: (urate transporters - SLC2A9, ABCG2)
- **Age**: (increases with age)
- **Male**: (more common, post-menopausal women)
- **Renal impairment**

---

## CLINICAL FEATURES

**Acute Gouty Arthritis**:
- **Sudden onset**: (often at night)
- **Severe pain**: (excruciating)
- **Swelling**, erythema, warmth
- **First MTP joint** (podagra) - 50% (classically)
- **Other joints**: (knee, ankle, midfoot, wrist, fingers)
- **Monoarticular**: (usually, but can be polyarticular)
- **Duration**: (days to 2 weeks if untreated)
- **Triggers**: (alcohol, excess food, dehydration, trauma, surgery, diuretics)

**Intercritical Gout**: (asymptomatic periods between attacks)

**Chronic Tophaceous Gout**:
- **Tophi**: (urate crystal deposits - fingers, ears, olecranon, Achilles)
- **Joint damage**: (erosions, deformity)
- **Renal disease**: (urate nephropathy, stones)

---

## DIAGNOSIS

**Clinical**: (typical presentation)

**Synovial Fluid Analysis** (gold standard):
- **Urate crystals**: (needle-shaped, negatively birefringent under polarized light)
- **Cell count**: (WBC elevated, 2,000-100,000/mm³)

**Serum Urate**:
- **Elevated**: (>420 µmol/L in men, >360 µmol/L in women)
- **Normal**: (does NOT exclude gout - can be normal during acute attack)

**Ultrasound**: (double contour sign, tophi, erosions)

**Dual-Energy CT**: (urate crystal deposition)

---

## DIFFERENTIAL DIAGNOSIS

**Septic Arthritis** (MUST EXCLUDE):
- **Single hot joint**
- **Fever**, high inflammatory markers
- **Joint aspiration**: (diagnostic)

**Pseudogout**: (CPPD crystals - rhomboid, weakly positive birefringence)

**Cellulitis**: (can mimic gout, but joint is not as painful)

**Palindromic Rheumatism**: (intermittent attacks, no crystals)

---

## MANAGEMENT

### ACUTE ATTACK

**Treat Early** (within 24 hours optimal)

**First-line**:
- **Colchicine**: (500mcg 2-4 times daily - usually 500mcg TDS for 3-5 days)
  - **Caution**: (dose reduce in renal impairment, drug interactions)
- **NSAIDs**: (naproxen 500mg BID, ibuprofen 400mg TDS - for 5-7 days)
  - **Caution**: (asthma, renal impairment, peptic ulcer, anticoagulation)
- **Glucocorticoids**: (prednisolone 30-35mg daily for 5-7 days)
  - **Indications**: (if NSAIDs/colchicine contraindicated or polyarticular)
  - **Intra-articular**: (if single joint, especially if contraindicated to systemic)

**Joint Aspiration**: (if diagnosis uncertain, to exclude sepsis)

**Comorbidities**: (treat simultaneously)

---

### URATE-LOWERING THERAPY (ULT)

**Indications**:
- **Recurrent attacks**: (≥2 per year)
- **Tophi**
- **Joint damage**: (erosions on X-ray)
- **Urolithiasis**
- **Chronic kidney disease**

**Start**: (after acute attack resolves, 2-4 weeks, or can start during attack if prophylaxis given)

**First-line**:
- **Allopurinol**: (xanthine oxidase inhibitor)
  - **Start**: (100mg daily, titrate by 100mg every 2-4 weeks to target)
  - **Target**: (serum urate <360 µmol/L, <300 µm/L if severe gout)
  - **Max dose**: (800mg daily, but higher doses may be needed)
  - **Side effects**: (rash, hypersensitivity - HLA-B*5801 risk in Asian patients, renal impairment)

**Second-line** (if allopurinol intolerant or target not achieved):
- **Febuxostat**: (80-120mg daily)
  - **Caution**: (cardiovascular risk - avoid if established CVD)

**Prophylaxis** (when starting ULT):
- **Colchicine**: (500mcg BID for 6-12 months)
- **Or NSAID**: (low dose)

---

### LIFESTYLE

**Diet**:
- **Low purine**: (limit red meat, seafood, especially organ meats)
- **Avoid**: (fructose-sweetened drinks, excessive alcohol, especially beer)
- **Dairy**: (low-fat dairy may be protective)
- **Vitamin C**: (500mg daily may reduce urate)
- **Cherries**: (may reduce gout attacks)

**Weight Loss**: (gradual, avoid crash diets)

**Hydration**: (2-3 liters daily)

**Alcohol**: (avoid beer, limit wine/spirits)

---

### SCREENING FOR COMORBIDITIES

**Cardiovascular**: (hypertension, ischemic heart disease, heart failure)
**Metabolic**: (obesity, diabetes, dyslipidemia)
**Renal**: (CKD, stones)

---

## PROGNOSIS

**Good**: (with appropriate treatment)
**Complications** (if untreated):
- **Joint destruction**
- **Tophi**: (cosmetic, functional)
- **Renal disease**
- **Cardiovascular disease**

---

## WHEN TO REFER

**Urgent**:
- **Septic arthritis** suspected (single hot joint)
- **First attack**: (to confirm diagnosis, especially if atypical)

**Routine**:
- **Recurrent attacks**: (for ULT initiation)
- **Tophaceous gout**: (for management)
- **Renal impairment**: (allopurinol dosing)

---

**Sources: NICE NG153 Gout, BSR Gout Guidelines 2022, EULAR Gout Recommendations**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.93,
            metadata={
                "specialty": "rheumatology",
                "focus": "gout",
                "sources": ["NICE NG153", "BSR Gout Guidelines 2022", "EULAR Gout Recommendations"]
            }
        )

    def _handle_pseudogout(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pseudogout (CPPD)"""
        answer = """**PSEUDOGOUT (CALCIUM PYROPHOSPHATE DEPOSITION - CPPD)**

---

## DEFINITION

**Crystal-induced arthritis** caused by calcium pyrophosphate (CPP) crystal deposition in cartilage and synovium

---

## PATHOPHYSIOLOGY

**CPPD crystals**: (calcium pyrophosphate dihydrate)
- **Deposit** in fibrocartilage (knee meniscus, symphysis pubis, intervertebral discs, triangular fibrocartilage of wrist)
- **Release** into joint space → inflammation

**Cause**: (unknown, but associated with aging, metabolic disorders)

---

## RISK FACTORS

- **Age**: (>60 years, rare <50)
- **Genetics**: (familial forms)
- **Metabolic**: (hyperparathyroidism, hemochromatosis, hypomagnesemia, hypophosphatasia)
- **Degenerative**: (OA - common association)

---

## CLINICAL FEATURES

**Acute CPPD Crystal Arthritis** (Pseudogout):
- **Knee** (50%), **wrist**, shoulder, ankle
- **Acute onset**: (resembles gout)
- **Monoarticular**: (usually)
- **Pain**, swelling, erythema, warmth
- **Fever**: (may occur)
- **Duration**: (days to weeks)

**Chronic CPPD**:
- **Degenerative arthropathy**: (resembles OA, but unusual distribution - wrist, MCP, shoulder, ankle)
- **Multiple joints**: (polyarticular)
- **Radiographic chondrocalcinosis**: (calcified cartilage)

---

## DIAGNOSIS

**Synovial Fluid**:
- **CPPD crystals**: (rhomboid, rod-shaped, weakly positive birefringence under polarized light)
- **Cell count**: (WBC elevated)

**X-ray**:
- **Chondrocalcinosis**: (linear calcification in cartilage, especially knee meniscus, triangular fibrocartilage of wrist, symphysis pubis)

**Ultrasound**: (cartilage calcification, synovitis)

---

## MANAGEMENT

**Acute Attack**:
- **NSAIDs**: (naproxen, ibuprofen - 5-7 days)
- **Colchicine**: (500mcg BID-TID)
- **Glucocorticoids**: (oral prednisolone 20-30mg daily, or intra-articular)

**Chronic**:
- **NSAIDs**: (low dose, prn)
- **Physical therapy**: (joint protection, exercises)

**Treat Underlying Cause**:
- **Hyperparathyroidism**: (parathyroidectomy)
- **Hemochromatosis**: (venesection)
- **Hypomagnesemia**: (magnesium supplementation)

---

## PROGNOSIS

**Good**: (self-limiting acute attacks)
**Chronic**: (progressive joint damage, disability)

---

## DIFFERENTIAL DIAGNOSIS

**Gout**: (urate crystals, negatively birefringent)
**Septic arthritis**: (must exclude)
**Osteoarthritis**: (degenerative, but unusual distribution)

---

**Sources: NICE NG153 Gout (includes CPPD), BSR Guidelines, EULAR CPPD Recommendations**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "pseudogout_cppd",
                "sources": ["NICE NG153", "BSR Guidelines", "EULAR CPPD Recommendations"]
            }
        )

    def _handle_as(self, query: str, context: dict) -> DomainQueryResult:
        """Handle ankylosing spondylitis and spondyloarthritis"""
        answer = """**ANKYLOSING SPONDYLITIS (AS) AND SPONDYLOARTHRITIS (SpA)**

---

## DEFINITION

**Chronic, inflammatory arthritis** primarily affecting axial skeleton (spine, sacroiliac joints), associated with HLA-B27

---

## CLASSIFICATION

**Axial Spondyloarthritis**:
- **Ankylosing Spondylitis** (radiographic - sacroiliitis on X-ray)
- **Non-radiographic Axial SpA** (symptoms, HLA-B27, but no sacroiliitis on X-ray, may be seen on MRI)

**Peripheral Spondyloarthritis**:
- **Psoriatic Arthritis**
- **Reactive Arthritis**
- **Enteropathic Arthritis** (associated with IBD)
- **Undifferentiated**

---

## EPIDEMIOLOGY

**Prevalence**: (0.1-1%)
**Age**: (onset 20-30 years)
**Male**: (2-3:1 male:female for AS, more equal for SpA)
**Genetic**: (HLA-B27 positive 90% in AS, 70-80% in SpA)

---

## CLINICAL FEATURES

**Inflammatory Back Pain** ( hallmark):
- **Onset**: (gradual, insidious)
- **Duration**: (>3 months)
- **Age**: (<45 years at onset)
- **Morning stiffness**: (>30 minutes, improves with exercise)
- **Night pain**: (wakes in second half of night, improves with rising)
- **Improvement with exercise**, not rest

**Peripheral Arthritis** (30-50%):
- **Lower limbs**: (knees, ankles, hips)
- **Asymmetric**: (often)
- **Dactylitis**: ("sausage digit")

**Enthesitis** (inflammation at tendon/ligament insertion):
- **Achilles tendonitis**
- **Plantar fasciitis**
- **Costosternal junction**: (anterior chest wall pain)

**Extra-Articular**:
- **Uveitis** (acute anterior uveitis - 30-40%):
  - **Red, painful eye**, photophobia
  - **Recurrent**: (often unilateral)
  - **Urgent ophthalmology review**
- **IBD**: (ulcerative colitis, Crohn's - 5-10%)
- **Psoriasis**: (10-20%)
- **Cardiac**: (aortic regurgitation, conduction abnormalities)
- **Pulmonary**: (apical fibrosis - rare)

---

## DIAGNOSIS

**Modified New York Criteria** (for AS):

**Clinical**:
1. **Low back pain**: (>3 months, improves with exercise, not rest, morning stiffness)
2. **Limited lumbar spine motion**: (sagittal, frontal planes)
3. **Chest expansion**: (<2.5 cm)

**Radiographic** (Sacroiliitis):
- **Bilateral**: (grade 2-4)
- **Unilateral**: (grade 3-4)

**Definite AS**: (1 clinical + bilateral sacroiliitis grade 2-4 OR unilateral grade 3-4)

---

**ASAS Criteria** (for Axial SpA):

**Imaging arm**:
- **Sacilitis** on MRI (active) OR X-ray (radiographic) + **1 SpA feature**

**Clinical arm** (no imaging):
- **HLA-B27 positive** + **2 SpA features**

**SpA Features**:
- **Inflammatory back pain**
- **Arthritis**: (asymmetric, lower limb)
- **Enthesitis**: (heel pain)
- **Uveitis**
- **Dactylitis**
- **Psoriasis**
- **IBD**
- **Good response to NSAIDs**
- **Family history** of SpA
- **Elevated CRP**
- **HLA-B27**

---

## INVESTIGATIONS

**Blood**:
- **HLA-B27**: (present in 90% AS, 70-80% SpA)
- **CRP**: (elevated in 60-70%, but may be normal)
- **ESR**: (elevated)
- **FBC**: (may have mild anemia)

**Imaging**:
- **X-ray sacroiliac joints**: (AP pelvis - sclerosis, erosions, fusion)
- **MRI sacroiliac joints/spine**: (active inflammation - edema, bone marrow edema)
- **X-ray spine**: (bamboo spine, syndesmophytes, squaring, shiny corner)

---

## MANAGEMENT

**Education**, **Exercise**:
- **Physiotherapy**: (core strengthening, spinal mobility exercises)
- **Daily exercise**: (swimming, walking, Pilates, yoga)
- **Posture**: (maintain upright posture, avoid kyphosis)

**NSAIDs** (first-line):
- **Continuous**: (for symptom control)
- **Indomethacin**: (25-50mg TDS - historically used)
- **Naproxen**: (500mg BID)
- **Celecoxib**: (200mg OD)
- **Duration**: (long-term if effective)

**Biologics** (if inadequate response to NSAIDs):
- **Anti-TNF**: (etanercept, adalimumab, certolizumab, golimumab)
  - **Indications**: (active disease despite NSAIDs, elevated CRP, active inflammation on MRI)
- **IL-17 inhibitor**: (secukinumab, ixekizumab)

**Sulfasalazine**: (for peripheral arthritis)

**Physical Therapy**:
- **Spinal extension exercises**
- **Posture training**
- **Breathing exercises** (chest wall mobility)

**Orthotics**:
- **Corrective lenses**: (if cervical fusion limits downward gaze)

---

## COMPLICATIONS

**Spinal**:
- **Sacrolitis**: (inflammation, fusion)
- **Bamboo spine**: (complete spinal fusion)
- **Spinal fracture**: (fragile spine, even minor trauma)
- **Cauda equina**: (rare)

**Hip**: (inflammatory arthritis, may require replacement)

**Osteoporosis**: (reduced mobility, inflammation)

---

## PROGNOSIS

**Variable**: (mild to severe)
**Disability**: (if spinal fusion, hip involvement)
**Mortality**: (slightly increased, mainly cardiovascular)

---

## WHEN TO REFER

**Urgent**:
- **Acute anterior uveitis**: (ophthalmology)

**Routine**:
- **Suspected AS/SpA**: (for diagnosis, HLA-B27, imaging, management)
- **New symptoms**: (uveitis, IBD, psoriasis)

---

**Sources: NICE NG65 Spondyloarthritis, BSR AS Guidelines, ASAS SpA Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "rheumatology",
                "focus": "ankylosing_spondylitis_spa",
                "sources": ["NICE NG65", "BSR AS Guidelines", "ASAS SpA Guidelines"]
            }
        )

    def _handle_psa(self, query: str, context: dict) -> DomainQueryResult:
        """Handle psoriatic arthritis"""
        answer = """**PSORIATIC ARTHRITIS (PsA)**

---

## DEFINITION

**Chronic inflammatory arthritis** associated with psoriasis, seronegative for rheumatoid factor, HLA-B27 association

---

## EPIDEMIOLOGY

**Prevalence**: (0.3-1% of population)
- **30% of psoriasis patients**: (develop PsA)
**Age**: (30-50 years)
**Sex**: (equal, or slight female predominance)
**Genetic**: (HLA-B27, HLA-Cw6, HLA-B38, HLA-B39)

---

## CLASSIFICATION

**CASPAR Criteria** (for classification):

Must have **inflammatory articular disease** (joint, spine, or enthesis) **PLUS** ≥3 points from:
- **Psoriasis**: (current - 2 points, past - 1 point, family history - 1 point)
- **Psoriatic nail dystrophy**: (onycholysis, pitting, hyperkeratosis - 1 point)
- **Negative RF**: (1 point)
- **Negative DIP joints**: (dactylitis - 1 point)
- **Juxtaarticular new bone formation**: (on X-ray - 1 point)
- **RF negativity**: (implied by seronegative)

≥3 points = PsA

---

## CLINICAL FEATURES

**Psoriasis**:
- **Plaque psoriasis**: (most common)
- **Onset**: (may precede, coincide, or follow arthritis)
- **Scalp**, extensor elbows/knees, umbilicus, gluteal cleft
- **Nail changes**: (pitting, onycholysis, hyperkeratosis, oil spots - highly specific)

**Arthritis Patterns**:
- **Asymmetric oligoarthritis**: (30-50% - knees, ankles, wrists)
- **Symmetric polyarthritis**: (resembling RA - 30-50%)
- **DIP joint involvement**: (classic, distinguishes from RA)
- **Arthritis mutilans**: (severe, resorptive, rare)
- **Spondylitis**: (sacroiliitis, spinal fusion - 20-40%)

**Dactylitis** ("Sausage Digit"):
- **Diffuse swelling**: (entire digit - toes, fingers)
- **Inflammation**: (tenosynovitis, synovitis, soft tissue edema)

**Enthesitis**:
- **Achilles tendonitis**
- **Plantar fasciitis**
- **Pelvic entheses**: (ischial tuberosity, iliac crests)

**Extra-Articular**:
- **Uveitis**: (anterior, less common than AS)
- **IBD**: (Crohn's, UC - increased association)

---

## DIAGNOSIS

**Clinical**: (psoriasis + inflammatory arthritis)

**Blood**:
- **RF**: (negative)
- **ACPA**: (negative)
- **CRP**: (elevated, but may be normal)
- **ESR**: (elevated)

**Imaging**:
- **X-ray**:
  - **Periarticular osteopenia**: (early)
  - **Erosions**: (marginal, ill-defined)
  - **New bone formation**: (periostitis, ankylosis, pencil-in-cup)
  - **Sacroiliitis**: (asymmetric, unilateral)
  - **Spine**: (syndesmophytes, non-marginal)

**Ultrasound/MRI**: (synovitis, enthesitis, dactylitis)

---

## MANAGEMENT

**Treat to Target**: (aim for remission/minimal disease activity)

**NSAIDs**: (for symptom control)

**Conventional DMARDs**:
- **Methotrexate**: (anchor drug, for peripheral arthritis)
- **Leflunomide**, **Sulfasalazine**
- **Hydroxychloroquine**: (less effective than in RA)

**Biologics** (if inadequate response to conventional DMARDs):
- **Anti-TNF**: (etanercept, adalimumat, certolizumab, golimumab)
  - **Indications**: (active PsA, inadequate response to DMARDs)
  - **Improves**: (skin, joints, enthesitis, dactylitis, spinal)
- **IL-17 inhibitor**: (secukinumab, ixekizumab, brodalumab)
  - **Effective**: (especially for skin, joints, enthesitis)
- **IL-12/23 inhibitor**: (ustekinumab)
- **JAK inhibitor**: (tofacitinib)

**Intra-articular steroids**: (for flare)

**Topical therapies** (for psoriasis):
- **Corticosteroids**, **Vitamin D analogues**, **Coal tar**, **Phototherapy**

---

## MONITORING

**Disease Activity**:
- **DAPSA**: (Disease Activity in Psoriatic Arthritis)
- **CPDAI**: (Composite Psoriatic Disease Activity Index)
- **PASI**: (Psoriasis Area and Severity Index)

---

## PROGNOSIS

**Variable**: (mild to severe)
**Worse**: (polyarticular, elevated CRP, erosions, early onset, DIP involvement)
**Mortality**: (slightly increased, mainly cardiovascular)

---

## COMPLICATIONS

**Joint damage**: (erosions, deformity, disability)
**Spinal fusion**: (ankylosing spondylitis-like)
**Uveitis**: (acute anterior)
**Cardiovascular**: (accelerated atherosclerosis)

---

## WHEN TO REFER

**Urgent**:
- **Acute anterior uveitis**: (ophthalmology)

**Routine**:
- **Suspected PsA**: (for diagnosis, management)
- **Skin disease**: (dermatology referral if severe)
- **New symptoms**: (uveitis, IBD)

---

**Sources: NICE NG65 Spondyloarthritis, BSR PsA Guidelines, GRAPPA Recommendations**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "psoriatic_arthritis",
                "sources": ["NICE NG65", "BSR PsA Guidelines", "GRAPPA Recommendations"]
            }
        )

    def _handle_sle(self, query: str, context: dict) -> DomainQueryResult:
        """Handle systemic lupus erythematosus"""
        answer = """**SYSTEMIC LUPUS ERYTHEMATOSUS (SLE)**

---

## DEFINITION

**Chronic, multisystem autoimmune disease** with autoantibodies, immune complex deposition, inflammation

---

## EPIDEMIOLOGY

**Prevalence**: (20-150 per 100,000)
**Sex**: (9:1 female:male)
**Age**: (15-45 years peak, but all ages)
**Ethnicity**: (more common, severe in African, Asian, Hispanic ancestry)

---

## GENETICS

**HLA**: (HLA-DR2, HLA-DR3)
**Complement**: (C1q, C4, C2 deficiency)
**Others**: (IRF5, STAT4, TYK2)

---

## CLINICAL FEATURES

**Constitutional** (90-100%):
- **Fatigue**: (severe, debilitating)
- **Fever**: (low-grade)
- **Malaise**, weight loss

**Musculoskeletal** (80-90%):
- **Arthralgia/arthritis**: (migratory, symmetric, small joints of hands, wrists)
- **Morning stiffness**: (<30 min)
- **Deformity**: (Jaccoud arthropathy - reducible, swan-neck, boutonniere - less common now)
- **Myalgias**

**Mucocutaneous** (70-80%):
- **Malar rash**: ("butterfly rash" - cheeks, bridge of nose, spares nasolabial folds)
- **Photosensitivity**: (sun-induced rash)
- **Discoid lesions**: (discoid rash - atrophic, scarring, hypopigmentation)
- **Oral ulcers**: (painless, palate, buccal mucosa, nasal)
- **Alopecia**: (diffuse, patchy)
- **Raynaud's phenomenon**: (30-50%)

**Renal** (40-50%):
- **Lupus nephritis**: ( Classes I-VI)
- **Proteinuria**: (nephrotic syndrome)
- **Hematuria**, casts
- **Renal impairment**

**Neuropsychiatric** (10-20%):
- **Headache**, mood disorders
- **Cognitive dysfunction**
- **Seizures**, psychosis
- **Peripheral neuropathy**

**Hematological** (50-70%):
- **Leukopenia**, lymphopenia
- **Anemia**: (AIHA, ACD)
- **Thrombocytopenia**

**Cardiopulmonary** (30-50%):
- **Pleurisy**, pleural effusion
- **Pericarditis**
- **Myocarditis** (rare)
- **Pulmonary hypertension** (rare, late)

**Vascular** (20-30%):
- **Raynaud's**
- **Vasculitis**: (cutaneous, digital infarcts)
- **Antiphospholipid syndrome**: (thrombosis, miscarriage)

**Ophthalmic**:
- **Keratoconjunctivitis sicca**: (dry eyes - secondary Sjögren's)
- **Cotton wool spots**: (retinal vasculitis)

---

## DIAGNOSIS

**ACR/EULAR 2019 Criteria** (for classification):

**ANA** ≥1:80 (entry criterion)

**Weighted Clinical and Immunologic Domains** (≥10 points = SLE):
- **Clinical**: (fever, arthritis, rash, alopecia, mucosal ulcers, serositis, renal, neurologic, hematologic)
- **Immunologic**: (ANA, anti-dsDNA, anti-Smith, antiphospholipid, low complement, direct Coombs)

---

**Investigations**:

**Blood**:
- **ANA**: (positive in 95-100%, but not specific)
- **Anti-dsDNA**: (specific, 60-70%, correlates with disease activity, nephritis)
- **Anti-Smith**: (highly specific, 10-30%)
- **Antiphospholipid antibodies**: (lupus anticoagulant, anticardiolipin, anti-β2GPI)
- **Complement**: (C3, C4 low - correlate with disease activity)
- **FBC**, **ESR**, **CRP**: (anemia, thrombocytopenia, elevated ESR, CRP may be normal/inappropriately low)
- **LFTs**, **U&E**

**Urine**:
- **Dipstick**: (proteinuria, hematuria)
- **Protein/creatinine ratio**: (if proteinuria)
- **Microscopy**: (casts, dysmorphic RBCs)

**Renal Biopsy** (if nephritis):
- **Class I**: minimal mesangial
- **Class II**: mesangial proliferative
- **Class III**: focal proliferative
- **Class IV**: diffuse proliferative (severe)
- **Class V**: membranous
- **Class VI**: advanced sclerosing

**ECG**, **ECHO**: (if pericarditis, myocarditis suspected)

**CXR/CT**: (serositis, interstitial lung disease)

---

## MANAGEMENT

**Mild Disease** (skin, joints, fatigue):
- **Hydroxychloroquine**: (anchor drug, 200-400mg daily)
  - **Reduces**: flares, damage, thrombosis risk, improves survival
  - **Monitoring**: (baseline ophthalmology, then annually after 5 years)
- **NSAIDs**: (for arthritis, serositis)
- **Topical steroids**: (for skin rash)

**Moderate-Severe** (organ involvement, hemolytic anemia, thrombocytopenia):
- **Glucocorticoids**: (prednisolone 0.5-1 mg/kg/day, then taper)
- **Immunosuppressants**:
  - **Azathioprine**: (2-2.5 mg/kg/day)
  - **Methotrexate**: (15-20mg weekly)
  - **Mycophenolate mofetil**: (1-2g daily)

**Severe/Refractory** (nephritis, neuropsychiatric, hemolytic anemia):
- **IV cyclophosphamide**: (500-1000mg/m² monthly for 6 months, then quarterly)
- **Mycophenolate mofetil**: (for nephritis)
- **Calcineurin inhibitors**: (tacrolimus, cyclosporine)

**Biologics** (refractory):
- **Belimumab**: (anti-BLyS, B-cell survival)
- **Rituximab**: (anti-CD20, B-cell depletion)

---

## FLARES

**Triggers**: (UV light, infections, stress, medications, pregnancy)

**Mild flare**: (skin, joints)
- **Hydroxychloroquine**
- **NSAIDs**
- **Low-dose steroids**

**Severe flare** (organ involvement):
- **High-dose steroids**: (prednisolone 1 mg/kg/day)
- **Immunosuppressants**: (depending on severity)

---

## ANTIPHOSPHOLIPID SYNDROME (APS)

**Secondary APS**: (in 30-40% of SLE patients)

**Clinical**:
- **Thrombosis**: (DVT, PE, arterial - stroke, MI)
- **Pregnancy morbidity**: (recurrent miscarriage, pre-eclampsia, fetal loss)
- **Thrombocytopenia**

**Laboratory** (2 occasions, 12 weeks apart):
- **Lupus anticoagulant**
- **Anticardiolipin**: (IgG/IgM)
- **Anti-β2 glycoprotein I**: (IgG/IgM)

**Management**:
- **Anticoagulation**: (warfarin target INR 2-3, or DOAC)
- **Low-dose aspirin**: (primary prevention)
- **Heparin/LMWH**: (pregnancy)

---

## PROGNOSIS

**Improved**: (with better treatment, 10-year survival 90-95%)
**Worse**: (renal involvement, antiphospholipid, non-Caucasian, low socioeconomic status)
**Causes of death**: (infection, active disease, cardiovascular)

---

## LIFESTYLE

- **Sun protection**: (avoid UV, sunscreen, protective clothing)
- **Exercise**: (bone health, fatigue, cardiovascular)
- **Smoking cessation**: (cardiovascular risk)
- **Vaccinations**: (flu, pneumococcal, HPV - before immunosuppression if possible)
- **Pregnancy planning**: (high-risk, planned remission, avoid teratogenic drugs)

---

## PREGNANCY

**High-risk**: (flares, preeclampsia, fetal loss, neonatal lupus)

**Planning**: (remission >6 months, replace teratogenic drugs)

**Safe**: (hydroxychloroquine, azathioprine)
**Avoid**: (methotrexate, mycophenolate, cyclophosphamide)
**Consult**: (maternal-fetal medicine)

---

## NEONATAL LUPUS

**Passive transfer**: of maternal anti-Ro/SSA, anti-La/SSB antibodies

**Clinical**:
- **Rash**: (annular, photosensitive, face, scalp - resolves)
- **Liver dysfunction**: (elevated LFTs)
- **Congenital heart block**: (permanent, requires pacemaker)

---

## WHEN TO REFER

**Urgent**:
- **Severe flare**: (organ involvement, nephritis, neuropsychiatric)
- **Pregnancy**: (maternal-fetal medicine)
- **New diagnosis**: (for confirmation, baseline investigations)

**Routine**:
- **Confirmed SLE**: (for ongoing management)
- **Flares**: (if not responding to treatment)

---

**Sources: NICE NG144 SLE, BSR SLE Guidelines 2017, EULAR/ACR SLE Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.94,
            metadata={
                "specialty": "rheumatology",
                "focus": "systemic_lupus_erythematosus",
                "sources": ["NICE NG144", "BSR SLE Guidelines 2017", "EULAR/ACR SLE Guidelines"]
            }
        )

    def _handle_sjogrens(self, query: str, context: dict) -> DomainQueryResult:
        """Handle Sjögren's syndrome"""
        answer = """**SJÖGREN'S SYNDROME**

---

## DEFINITION

**Autoimmune exocrinopathy** causing lymphocytic infiltration of lacrimal and salivary glands, resulting in dry eyes (keratoconjunctivitis sicca) and dry mouth (xerostomia)

---

## CLASSIFICATION

**Primary Sjögren's**: (intrinsic, not associated with other CTD)
**Secondary Sjögren's**: (associated with RA, SLE, SSc)

---

## EPIDEMIOLOGY

**Prevalence**: (0.1-1%)
**Sex**: (9:1 female:male)
**Age**: (40-60 years)

---

## CLINICAL FEATURES

**Ocular** (sicca):
- **Dry eyes**: (gritty, burning, foreign body sensation)
- **Photophobia**
- **Red eyes**: (conjunctival injection)
- **Corneal ulceration**: (severe)
- **Visual disturbance**: (blur from tear film instability)

**Oral** (sicca):
- **Dry mouth**: (xerostomia - difficulty swallowing, speaking)
- **Dental caries**: (rampant, cervical)
- **Oral candidiasis**: (thrush)
- **Dysgeusia**: (altered taste)
- **Salivary gland enlargement**: (parotid, bilateral, firm, non-tender)

**Systemic** (30-50%):
- **Fatigue**: (common, debilitating)
- **Arthralgia/arthritis**: (non-erosive)
- **Raynaud's phenomenon**
- **Skin**: (dry skin, vasculitis, purpura)
- **Lung**: (interstitial lung disease - rare)
- **Renal**: (tubulointerstitial nephritis - rare)
- **Neurologic**: (peripheral neuropathy, cranial neuropathy)
- **Lymphoma**: (5-10% increased risk - MALT lymphoma)

---

## DIAGNOSIS

**ACR/EULAR 2016 Criteria** (for classification):

**Positive** if (≥4 points, with each item ≥1 point):
1. **Anti-Ro/SSA positive**: (3 points)
2. **Labial salivary gland biopsy** with focal lymphocytic sialadenitis: (3 points)
3. **Keratoconjunctivitis sicca**: (1 point - ocular staining score ≥3 in at least one eye)
4. **Schirmer test**: (≤5 mm/5 min) in at least one eye: (1 point)
5. **Unstimulated whole salivary flow**: (≤0.1 mL/min): (1 point)

---

**Investigations**:

**Blood**:
- **Anti-Ro/SSA**: (most sensitive, 60-70%)
- **Anti-La/SSB**: (more specific, 30-40%)
- **ANA**: (positive in 70-80%)
- **RF**: (positive in 60-80%)
- **Cryoglobulins**
- **Immunoglobulins**: (polyclonal hypergammaglobulinemia)

**Ocular**:
- **Schirmer test**: (<5 mm in 5 min - low sensitivity)
- **Ocular surface staining**: (fluorescein, lissamine green - more sensitive)

**Salivary**:
- **Unstimulated salivary flow**: (<0.1 mL/min)
- **Sialography**: (sialectasis, ductal changes)
- **Salivary scintigraphy**: (reduced uptake, excretion)
- **Salivary gland biopsy**: (focal lymphocytic sialadenitis, Chisholm grade ≥3)

**Labial Salivary Gland Biopsy**:
- **Procedure**: (minor lip biopsy)
- **Histology**: (lymphocytic infiltrates, Chisholm grade 3-4)

---

## MANAGEMENT

**Symptomatic** (primary):

**Dry Eyes**:
- **Artificial tears**: (preservative-free, QID)
- **Lipid-based tears**: (for evaporative dry eye)
- **Ointments**: (at night)
- **Punctal plugs**: (if severe)
- **Anti-inflammatory**: (topical cyclosporine 0.05% BID)
- **Avoid**: (low humidity, fans, wind, smoking)

**Dry Mouth**:
- **Saliva substitutes**: (artificial saliva, gels)
- **Sugar-free gum**: (stimulate saliva)
- **Water**: (sip frequently)
- **Dental hygiene**: (fluoride, regular dental review, high fluoride toothpaste)
- **Antifungals**: (nystatin, fluconazole for thrush)
- **Pilocarpine**: (5mg TID - stimulates secretion, if not contraindicated)
- **Cease**: (anticholinergics, alcohol, caffeine, smoking)

**Systemic**:
- **Hydroxychloroquine**: (200-400mg daily - for fatigue, arthralgia, systemic manifestations)
- **Methotrexate**: (for arthritis)
- **Steroids**: (for severe systemic manifestations)
- **Biologics**: (rituximab - for severe systemic disease)

---

## COMPLICATIONS

**Lymphoma**: (5-10% increased risk, especially MALT lymphoma)
- **Monitor**: (persistent salivary gland enlargement, lymphadenopathy, constitutional symptoms)
- **Biopsy**: (if suspicious)

**Dental**: (rampant caries, tooth loss)
- **Prevention**: (meticulous oral hygiene, fluoride, regular dental review)

**Vaginal Dryness**: (dyspareunia)
- **Lubricants**: (water-based)
- **Estrogen**: (if appropriate)

---

## PROGNOSIS**

**Good**: (generally benign, but significant impact on QoL)
**Fatigue**: (major cause of disability)
**Lymphoma**: (most serious complication, increased risk)
**Survival**: (slightly reduced, mainly due to lymphoma)

---

## PREGNANCY

**Anti-Ro/SSA**: (cross placenta, neonatal lupus)
- **Neonatal lupus**: (rash, liver dysfunction)
- **Congenital heart block**: (1-2%, permanent, requires pacemaker)

---

## WHEN TO REFER

**Urgent**:
- **Lymphoma suspicion**: (persistent gland enlargement, B symptoms)

**Routine**:
- **Suspected Sjögren's**: (for diagnosis)
- **Systemic manifestations**: (fatigue, arthritis, pulmonary, renal)
- **Pregnancy planning**: (anti-Ro/SSA positive - obstetric cardiology)

---

**Sources: BSR Sjögren's Guidelines 2017, ACR/EULAR Sjögren's Criteria 2016**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "rheumatology",
                "focus": "sjogrens_syndrome",
                "sources": ["BSR Sjögren's Guidelines 2017", "ACR/EULAR Criteria 2016"]
            }
        )

    def _handle_scleroderma(self, query: str, context: dict) -> DomainQueryResult:
        """Handle scleroderma/systemic sclerosis"""
        answer = """**SYSTEMIC SCLEROSIS (SCLERODERMA)**

---

## DEFINITION

**Multisystem autoimmune disease** characterized by fibrosis of skin and internal organs, vascular abnormalities, autoantibodies

---

## CLASSIFICATION

**Diffuse Cutaneous SSc** (dcSSc):
- **Skin thickening**: (trunk, proximal limbs, face, neck)
- **Rapid onset**, early internal organ involvement
- **Anti-Scl-70**: (associated with PAH)

**Limited Cutaneous SSc** (lcSSc, CREST):
- **Skin thickening**: (distal to elbows, knees, face, neck)
- **Late onset**, slower progression
- **Anti-centromere**: (associated with PAH)

**CREST Syndrome**:
- **Calcinosis** (calcium deposits)
- **Raynaud's**
- **Esophageal dysmotility**
- **Sclerodactyly**
- **Telangiectasia**

---

## EPIDEMIOLOGY

**Prevalence**: (10-20 per 100,000)
**Sex**: (4:1 female:male)
**Age**: (30-50 years)
**Ethnicity**: (more common, severe in African ancestry)

---

## CLINICAL FEATURES

**Vascular**:
- **Raynaud's phenomenon**: (90-95%, often first symptom)
- **Digital ischemia**: (ulcers, gangrene)

**Skin**:
- **Sclerodactyly**: (tight skin, fingers, loss of wrinkles, limited flexion)
- **Skin thickening**: (modified Rodnan score)
- **Calcinosis**: (calcium deposits - fingers, elbows, knees - painful, ulcerated)
- **Telangiectasia**: (face, hands, mucosa)

**Musculoskeletal**:
- **Arthralgia**, arthritis
- **Tendon friction rubs**: (pathognomonic)
- **Myalgias**, weakness
- **Muscle atrophy**

**Gastrointestinal**:
- **Esophageal dysmotility**: (dysphagia, reflux, dysphagia)
- **Gastroparesis**: (nausea, vomiting)
- **Intestinal pseudo-obstruction**
- **Malabsorption**: (bacterial overgrowth)

**Pulmonary** (leading cause of death):
- **Interstitial lung disease**: (NSIP, UIP - fibrosis)
- **Pulmonary arterial hypertension**: (late complication)
- **Restrictive lung disease**

**Cardiac**:
- **Myocardial fibrosis**
- **Conduction abnormalities**
- **Pericardial effusion**

**Renal**:
- **Scleroderma renal crisis** (rare, severe):
  - **Malignant hypertension**
  - **Rapid renal failure**
  - **Microangiopathic hemolytic anemia**

---

## DIAGNOSIS

**2013 ACR/EULAR Criteria** (for classification):

**Skin thickening** (of fingers) **PLUS** either:
1. **Scleroderma-specific antibodies** (anti-centromere, anti-topoisomerase I, anti-RNA polymerase III)
2. **Scleroderma-pattern nailfold capillary changes**

---

**Investigations**:

**Blood**:
- **ANA**: (positive in 95-100%)
- **Anti-centromere**: (lcSSc)
- **Anti-Scl-70 (anti-topoisomerase I)**: (dcSSc)
- **Anti-RNA polymerase III**: (dcSSc, diffuse skin)
- **Anti-fibrillarin**: (dcSSc, PAH)
- **FBC**, **UE**, **LFTs**: (anemia, CK, renal impairment)

**Pulmonary**:
- **CXR/CT**: (ILD)
- **PFTs**: (restrictive pattern)
- **ECHO**: (PAH)

**Cardiac**:
- **ECG**, **ECHO**: (fibrosis, conduction abnormality)

**Renal**:
- **BP**, **U&E**, **urinalysis**: (monitor for renal crisis)

**GI**:
- **Barium swallow**: (esophageal dysmotility)
- **Manometry**: (motility studies)
- **Endoscopy**: (if dysphagia, reflux)

**Nailfold Capillar Microscopy**:
- **Giant capillaries**, hemorrhages, avascular areas (early)

**Skin Biopsy** (rarely needed):
- **Fibrosis**, atrophy of dermis

---

## MANAGEMENT

**Organ-based**:

**Raynaud's**:
- **Keep warm**: (gloves, socks, avoid cold)
- **CCB**: (nifedipine 30mg TDS, amlodipine 5-10mg OD)
- **Avoid**: (smoking, caffeine, beta-blockers)
- **IV iloprost**: (severe digital ischemia)
- **PDE5 inhibitor**: (sildenafil - for ulcers)
- **Bosentan**: (for digital ulcers)

**Skin**:
- **Methotrexate**: (for skin disease)
- **Mycophenolate mofetil**: (for skin disease, ILD)
- **Autologous stem cell transplant**: (severe dcSSc)

**Lung**:
- **ILD**: (mycophenolate mofetil, cyclophosphamide, autologous stem cell transplant)
- **PAH**: (bosentan, ambrisentan, sildenafil, tadalafil, epoprostenol)

**Renal Crisis**:
- **ACE inhibitor**: (first-line - enalapril, ramipril)
- **Urgent nephrology referral**

**GI**:
- **PPI**: (proton pump inhibitor - esomeprazole 40mg OD)
- **Prokinetics**: (domperidone, metoclopramide)
- **Antibiotics**: (for bacterial overgrowth)

**Cardiac**:
- **Pacemaker**: (if conduction abnormality)

---

## PROGNOSIS

**Variable**: (worse with dcSSc, ILD, PAH, renal crisis, anti-Scl-70)
**Survival**: (10-year survival 60-80%)
**Causes of death**: (lung, heart, renal)

---

## WHEN TO REFER

**Urgent**:
- **Renal crisis**: (malignant hypertension, acute renal failure)
- **New-onset dyspnea**: (ILD, PAH - urgent cardiopulmonary referral)

**Routine**:
- **Suspected SSc**: (for diagnosis, baseline investigations)
- **Organ involvement**: (ILD, PAH, GI - specialist management)

---

**Sources: BSR SSc Guidelines, ACR/EULAR SSc Criteria 2013**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "systemic_sclerosis_scleroderma",
                "sources": ["BSR SSc Guidelines", "ACR/EULAR Criteria 2013"]
            }
        )

    def _handle_myositis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle myositis (polymyositis, dermatomyositis)"""
        answer = """**INFLAMMATORY MYOPATHIES (POLYMYOSITIS, DERMATOMYOSITIS, INCLUSION BODY MYOSITIS)**

---

## DEFINITION

**Acquired, immune-mediated myopathies** characterized by muscle weakness, inflammation on biopsy

---

## CLASSIFICATION

**Polymyositis (PM)**:
- **Proximal muscle weakness**
- **No skin rash**
- **Adults** (rare children)

**Dermatomyositis (DM)**:
- **Proximal muscle weakness**
- **Skin rash** (heliotrope rash, Gottron's papules)
- **Adults**, children (JDM)

**Inclusion Body Myositis (IBM)**:
- **Distal + proximal weakness**
- **Older men**
- **Resistant to treatment**

**Immune-Mediated Necrotizing Myopathy (IMNM)**:
- **Proximal weakness**
- **Anti-SRP**, **Anti-HMGCR** antibodies
- **Severe**, statin-exposure may trigger

**Overlap Myositis**:
- **With CTD**: (SLE, SSc, MCTD)
- **Anti-synthetase syndrome**: (anti-Jo1, fever, ILD, arthritis, Raynaud's, mechanic's hands)

---

## EPIDEMIOLOGY

**Prevalence**: (10-20 per 100,000)
**Sex**: (DM 2:1 female:male, PM equal)
**Age**: (PM/DM 40-60 years, IBM >60 years)

---

## CLINICAL FEATURES

**Muscle Weakness**:
- **Proximal**: (shoulders, hips - difficulty rising from chair, combing hair, lifting)
- **Symmetrical**: (usually)
- **Progressive**: (weeks to months)
- **Pain**: (may be present)

**Skin** (DM):
- **Heliotrope rash**: (violaceous, periorbital, edematous)
- **Gottron's papules**: (violaceous papules over extensor surfaces - MCP, PIP, elbows, knees)
- **Shawl sign**: (photosensitive poikiloderma - upper back, shoulders)
- **V-sign**: (V-neck distribution)
- **Holster sign**: (lateral hip)
- **Mechanic's hands**: (hyperkeratosis, fissuring of lateral fingers)
- **Calcinosis**: (subcutaneous calcium deposits - children, late DM)

**Systemic**:
- **Fever**, malaise, weight loss
- **Joint pain**
- **ILD**: (anti-synthetase syndrome - cough, dyspnea)
- **Dysphagia** (esophageal weakness)
- **Cardiac**: (myocarditis, arrhythmias)
- **Malignancy** (DM association)

---

## DIAGNOSIS

**Clinical**: (proximal weakness ± skin rash)

**Blood**:
- **CK**: (elevated 10-100x normal)
- **Transaminases**: (AST, ALT elevated - from muscle)
- **LDH**, aldolase
- **Myositis-specific antibodies**: (anti-Jo1, anti-Mi2, anti-SRP, anti-HMGCR, anti-TIF1γ, anti-NXP2)
- **ANA**, **RF**: (often positive)

**EMG**:
- **Myopathic changes**: (small, short, polyphasic MUAPs)
- **Fibrillation potentials**, positive sharp waves
- **Irritability**

**Muscle Biopsy** (gold standard):
- **Inflammation**: (lymphocytic infiltrates)
- **Necrosis**, regeneration
- **Fiber atrophy**
- **MHC class I upregulation**
- **Complement deposition** (DM)

**MRI**:
- **Edema**: (STIR hyperintensity, T2)
- **Guides biopsy**, monitors response

**Pulmonary**:
- **CXR/CT**: (ILD)
- **PFTs**: (restrictive pattern)

**Malignancy Screening** (DM):
- **Age**, **sex**-, **smoking**, **alcohol**-appropriate
- **CT chest/abdomen/pelvis**: (for occult malignancy)
- **Pap smear**, **mammogram**: (women)
- **PSA**: (men)

---

## MANAGEMENT

**Acute**:
- **High-dose steroids**: (prednisolone 1 mg/kg/day)
- **IV methylprednisolone**: (severe, dysphagia, ILD)
- **Immunosuppressants**: (azathioprine, methotrexate, mycophenolate mofetil)
- **IVIG**: (if refractory)
- **Biologics**: (rituximab - refractory)
- **Exercise**, **physical therapy**: (maintain strength, prevent contractures)

**Dysphagia**:
- **Speech/swallow therapy**
- **Diet modification**: (soft diet, thickened fluids)
- **NG/PEG tube**: (if severe)

**ILD**:
- **High-dose steroids**
- **Mycophenolate mofetil**, **cyclophosphamide**
- **Pulmonology referral**

**Calcinosis**:
- **Diltiazem**: (for symptomatic)
- **Surgical excision**: (if severe, infected)

**Malignancy**: (treat underlying cancer)

---

## PROGNOSIS

**PM/DM**: (60-70% respond to treatment, 20-30% refractory)
**IBM**: (poor response, progressive disability)
**Mortality**: (cancer, ILD, infection, cardiovascular)

---

## WHEN TO REFER

**Urgent**:
- **Severe weakness**: (difficulty walking, dysphagia - aspiration risk)
- **ILD**: (dyspnea, hypoxia)

**Routine**:
- **Suspected myositis**: (for diagnosis, baseline investigations)
- **Refractory**: (for biologics)

---

**Sources: BSR Myositis Guidelines, EULAR/ACR Myositis Criteria 2017**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "myositis",
                "sources": ["BSR Myositis Guidelines", "EULAR/ACR Criteria 2017"]
            }
        )

    def _handle_vasculitis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle vasculitis"""
        answer = """**VASCULITIS**

---

## DEFINITION

**Inflammation of blood vessel walls**, leading to ischemia, tissue damage

---

## CLASSIFICATION

**Size of Vessel**:

**Large Vessel**:
- **Giant Cell Arteritis (GCA)**: (temporal arteritis)
- **Takayasu Arteritis**: (aortic arch branches, young women)

**Medium Vessel**:
- **Polyarteritis Nodosa (PAN)**
- **Kawasaki Disease**: (children)

**Small Vessel**:
- **ANCA-associated**: (GPA, MPA, EGPA)
- **Immune Complex**: (IgA vasculitis, cryoglobulinemic vasculitis, hypocomplementemic urticarial vasculitis)
- **Variable Vessel**: (Behçet's disease)

---

## GIANT CELL ARTERITIS

*(See separate GCA section - covered earlier)*

---

## POLYARTERITIS NODOSA (PAN)

**Medium-vessel necrotizing vasculitis**

**Clinical**:
- **Systemic**: (fever, weight loss, malaise)
- **Skin**: (livedo reticularis, nodules, ulcers)
- **Peripheral neuropathy**: (mononeuritis multiplex)
- **Renal**: (glomerulonephritis)
- **GI**: (abdominal pain, bleeding, perforation)
- **Cardiac**: (myocarditis, infarction)
- **Testicular pain**: (orchitis)

**Diagnosis**:
- **Biopsy**: (affected tissue - nerve, muscle, skin)
- **Angiography**: (aneurysms, stenosis of medium vessels)

**Management**:
- **High-dose steroids**: (prednisolone 1 mg/kg/day)
- **Cyclophosphamide**: (severe disease)

---

## KAWASAKI DISEASE

**Medium-vessel vasculitis** of childhood

**Age**: (<5 years, peak 18-24 months)

**Clinical** (Diagnostic Criteria - need 4/5):
1. **Fever**: ≥5 days
2. **Conjunctivitis**: (bilateral, non-exudative)
3. **Rash**: (polymorphous)
4. **Strawberry tongue**: (erythema, edema)
5. **Cervical lymphadenopathy**: (unilateral, >1.5cm)

**Coronary artery aneurysms**: (complication)

**Management**:
- **IVIG**: (2g/kg single dose)
- **High-dose aspirin**: (initially, then low-dose)

---

## ANCA-ASSOCIATED VASCULITIS

**GPA** (Granulomatosis with Polyangiitis, formerly Wegener's):
- **Granulomas**: (respiratory tract, kidney)
- **Anti-PR3 ANCA**: (positive)

**MPA** (Microscopic Polyangiitis):
- **Necrotizing glomerulonephritis**: (pauci-immune)
- **Anti-MPO ANCA**: (positive)

**EGPA** (Eosinophilic Granulomatosis with Polyangiitis, formerly Churg-Strauss):
- **Asthma**, **eosinophilia**
- **Anti-MPO ANCA**: (positive)

---

**Clinical**:

**Constitutional**: (fever, weight loss, malaise)

**ENT**: (GPA - sinusitis, epistaxis, ulcerations, saddle nose deformity)

**Pulmonary**: (ILD, nodules, cavities, hemoptysis)

**Renal**: (rapidly progressive glomerulonephritis - crescentic GN)

**Skin**: (purpura, ulcers)

**Peripheral neuropathy**: (mononeuritis multiplex)

**Ocular**: (scleritis, orbital pseudotumor)

---

**Diagnosis**:
- **ANCA**: (anti-PR3, anti-MPO)
- **Biopsy**: (affected tissue - sinus, kidney, lung)
- **Urinalysis**: (protein, blood, casts)
- **CXR/CT**: (nodules, cavities, ILD)
- **Renal biopsy**: (if nephritis)

---

**Management**:
- **Induction**: (high-dose steroids + cyclophosphamide or rituximab)
- **Maintenance**: (azathioprine, methotrexate, rituximab)
- **Plasma exchange**: (if severe renal involvement, DAH)

---

## IGA VASCULITIS (HENOCH-SCHÖNLEIN PURPURA)

**Small-vessel IgA immune complex vasculitis**

**Age**: (children 4-7 years, adults 20-30 years)

**Trigger**: (infections, drugs, foods)

**Clinical**:
- **Palpable purpura**: (lower extremities, buttocks - mandatory)
- **Arthritis**: (ankles, knees - 70%)
- **Abdominal pain**: (colic, bleeding, intussusception)
- **Renal**: (hematuria, proteinuria - 30-40%)

**Diagnosis**:
- **Clinical**: (palpable purpura + 1 of: arthritis, abdominal pain, renal)
- **Skin biopsy**: (IgA deposition)

**Management**:
- **Supportive**: (rest, hydration, analgesia)
- **Steroids**: (if severe abdominal pain, renal involvement)
- **Renal referral**: (if nephritis)

---

**Sources: NICE NG158 Vasculitis, BSR Vasculitis Guidelines, Chapel Hill Consensus**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "rheumatology",
                "focus": "vasculitis",
                "sources": ["NICE NG158", "BSR Vasculitis Guidelines", "Chapel Hill Consensus"]
            }
        )

    def _handle_oa(self, query: str, context: dict) -> DomainQueryResult:
        """Handle osteoarthritis"""
        answer = """**OSTEOARTHRITIS (OA)**

---

## DEFINITION

**Degenerative joint disorder** characterized by hyaline cartilage loss, osteophyte formation, subchondral sclerosis

---

## EPIDEMIOLOGY

**Prevalence**: (increases with age, 80% >70 years)
**Risk Factors**: (age, obesity, female, genetics, trauma, occupational)

---

## PATHOPHYSIOLOGY

**Dynamic process**: (repair vs damage)
- **Cartilage degradation**: (chondrocyte apoptosis, matrix degradation)
- **Subchondral bone**: (sclerosis, microfractures, cysts)
- **Osteophytes**: (new bone formation at joint margins)
- **Synovitis**: (low-grade inflammation)
- **Ligament laxity**: (joint instability)

---

## CLINICAL FEATURES

**Symptoms**:
- **Pain**: (use-related, improves with rest)
- **Stiffness**: (morning stiffness <30 min, gelling)
- **Function**: (reduced range of motion, instability, locking)
- **Swelling**: (effusion, especially knee)

**Common Sites**:
- **Knee**: (most common)
- **Hip**: (groin, lateral hip pain)
- **Hand**: (DIP, PIP, CMC1 - Heberden's, Bouchard's nodes)
- **Spine**: (facet joints, DDD)
- **Foot**: (1st MTP - hallux valgus, rigidus)

**Examination**:
- **Crepitus**: (bony crepitus)
- **Tenderness**: (joint line)
- **Effusion**: (patellar tap)
- **Restricted ROM**: (joint specific)
- **Bony enlargement**

---

## DIAGNOSIS

**Clinical** (typical age, pattern, symptoms)

**Imaging**:
- **X-ray**: (gold standard)
  - **Joint space narrowing** (asymmetric)
  - **Osteophytes**: (marginal, central)
  - **Subchondral sclerosis**
  - **Subchondral cysts**
  - **Loose bodies** (knee)

**MRI**: (if diagnosis uncertain, early disease, meniscal tears, loose bodies)

**Blood**:
- **Normal** (exclude inflammatory arthritis if elevated ESR/CRP)

---

## MANAGEMENT

**Core Treatments**:

**Education**, **Self-Management**:
- **Weight loss**: (if overweight - 5-10% weight loss significantly improves pain, function)
- **Exercise**: (muscle strengthening, aerobic, ROM)
- **Joint protection**: (avoid aggravating activities, pacing)

**Exercise** (first-line):
- **Local muscle strengthening**: (quadriceps for knee, abductor strengthening for hip)
- **Aerobic**: (walking, cycling, swimming)
- **ROM**: (to maintain flexibility)
- **Physical therapy**: (supervised exercise program)

**Weight Loss**:
- **Target**: (BMI 18.5-25)
- **5-10% weight loss**: (significant improvement)

**Adjunctive**:

**Analgesia**:
- **Topical NSAIDs**: (knee, hand - diclofenac 1% gel QID)
- **Oral NSAIDs**: (naproxen, ibuprofen - lowest effective dose, shortest duration, add PPI if risk)
  - **Caution**: (asthma, PUD, renal impairment, anticoagulation, CVD, age >65)
- **Opioids**: (avoid if possible - tramadol 50-100mg QDS PRN if severe, consider capsaicin patches)

**Intra-articular Therapies**:
- **Corticosteroid injection**: (knee, hip - triamcinolone 40-80mg, guided by imaging for hip)
  - **Frequency**: (maximum 3-4/year - joint damage)
  - **Indications**: (flare, effusion)
- **Hyaluronic acid**: (viscosupplementation - knee, limited evidence, consider if NSAID contraindicated)

**Bracing**:
- **Knee brace**: (valgus offloading for medial knee OA)
- **Thumb spica**: (1st CMC OA)

**Assistive Devices**:
- **Walking stick** (use in opposite hand - reduces load 20-30%)
- **Shoe wedges** (lateral wedge for medial knee OA)
- **Raised toilet seat** (hip, knee OA)

**Surgery** (if conservative fails, severe symptoms):
- **Knee**: (total knee replacement - excellent pain relief, function)
- **Hip**: (total hip replacement - excellent outcomes)
- **Hand**: (1st CMC arthroplasty, DIP fusion)
- **Spine**: (discectomy, fusion - decompression for stenosis)

---

## MONITORING

**Pain**: (WOMAC, KOOS, HOOS scores)
**Function**: (gait speed, stair climb)
**Imaging**: (X-ray - not routinely repeated unless changing management)

---

## COMPLICATIONS

**Pain**, **functional limitation**, **disability**
**Secondary effects**: (obesity, depression, sleep disturbance)
**Medication side effects**: (NSAID gastropathy, renal impairment, CVD)

---

## PROGNOSIS

**Variable**: (symptoms fluctuate, some improve, many deteriorate)
**Worse**: (obesity, multi-joint, knee OA, severe pain)

---

## PREVENTION

**Weight maintenance**, **exercise**
**Joint protection**: (avoid repetitive stress, injury)
**Occupational**: (modify activities if possible)

---

## WHEN TO REFER

**Urgent**:
- **Septic arthritis** suspected (hot swollen joint)

**Routine**:
- **Failed conservative management**: (severe symptoms, functional limitation)
- **Surgical assessment**: (joint replacement)
- **Young age**: (<45 years - investigate secondary cause)

---

**Sources: NICE NG177 Osteoarthritis, OARSI Guidelines, BSR OA Guidelines 2022**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "rheumatology",
                "focus": "osteoarthritis",
                "sources": ["NICE NG177", "OARSI Guidelines", "BSR OA Guidelines 2022"]
            }
        )

    def _handle_back_pain(self, query: str, context: dict) -> DomainQueryResult:
        """Handle back pain and spinal disorders"""
        answer = """**LOW BACK PAIN**

---

## CLASSIFICATION

**Duration**:
- **Acute**: (<6 weeks)
- **Subacute**: (6-12 weeks)
- **Chronic**: (>12 weeks)

**Type**:
- **Non-specific** (mechanical, 85-90%)
- **Specific** (identifiable cause)
- **Red flags** (serious pathology)

---

## COMMON CAUSES

**Non-Specific Mechanical Low Back Pain** (85-90%):
- **Muscle strain**, ligament sprain
- **Facet joint dysfunction**
- **Degenerative disc disease**

**Specific Causes**:
- **Radicular pain**: (nerve root compression - herniated disc, spinal stenosis)
- **Spinal stenosis**: (central canal, lateral recess, foraminal narrowing)
- **Spondylolisthesis**: (slippage of one vertebra on another)
- **Sacroiliac joint dysfunction**
- **Compression fracture**: (osteoporosis, trauma)
- **Infection**: (discitis, vertebral osteomyelitis, epidural abscess)
- **Malignancy**: (metastasis, myeloma, lymphoma)
- **Inflammatory**: (ankylosing spondylitis)
- ** visceral**: (pancreatitis, aortic aneurysm, renal colic)

---

## ASSESSMENT

**History**:
- **Onset**: (trauma, insidious)
- **Duration**, **progression**
- **Location**, **radiation** (radicular pain - below knee)
- **Aggravating/relieving factors**: (rest, activity, position)
- **Red flags**: (see below)
- **Systemic symptoms**: (fever, weight loss, history of cancer)

**Examination**:
- **Inspection**: (posture, deformity, muscle spasm)
- **ROM**: (flexion, extension, side bending - limited)
- **Palpation**: (tenderness, step-off)
- **Neurologic**: (sensation, strength, reflexes, gait)

**Red Flags** (serious pathology, urgent referral):
- **Age**: (<20 or >50 years with new-onset back pain)
- **Trauma**: (fall, accident - especially elderly, osteoporosis risk)
- **History of cancer**, **weight loss**, **night pain**
- **Infection**: (fever, IV drug use, recent infection)
- **Neurologic deficits**: (progressive weakness, gait disturbance, saddle anesthesia, bowel/bladder dysfunction - **EMERGENCY**)
- **Systemic symptoms**: (fever, chills, weight loss)
- **Night pain**, **rest pain**
- **Duration**: (>6 weeks, progressive)
- **Steroid use**, **immunosuppression**
- **Unrelenting pain**

---

## INVESTIGATIONS

**Acute Non-Specific**: (NO imaging needed)

**Imaging**:
- **X-ray**: (if red flags, trauma, age >50, >6 weeks duration)
- **MRI**: (red flags, neurologic deficits, >6 weeks, surgical planning)
- **CT**: (fracture, congenital anomalies)

**Blood**:
- **FBC**, **ESR**, **CRP**: (if infection, malignancy suspected)
- **Alk phos**, **calcium**, **PSA**: (if malignancy suspected)

---

## MANAGEMENT

**Acute Non-Specific** (<6 weeks):

**Education**:
- **Reassurance**: (90% resolve within 6 weeks)
- **Stay active**: (bed rest >2 days worse)

**Exercise**:
- **Continue normal activities**: (as tolerated)
- **Gentle mobilization**: (walking, swimming, yoga)
- **Core strengthening**: (abdominal, lumbar)

**Analgesia**:
- **Paracetamol**: 1g QDS (first-line)
- **NSAIDs**: (naproxen, ibuprofen - add if paracetamol inadequate)
  - **Caution**: (asthma, PUD, renal impairment, anticoagulation, CVD, age >65)
  - **PPI**: (add if risk)
- **Weak opioids**: (codeine, tramadol - short-term, if severe, avoid if possible)
- **Muscle relaxants**: (baclofen, diazepam - short-term, if muscle spasm)

**Manual Therapies**:
- **Spinal manipulation**: (mobilization, manipulation - may help)
- **Massage**, **acupuncture**: (evidence limited)

---

**Chronic Low Back Pain** (>12 weeks):

**Exercise Therapy**:
- **Core strengthening**: (stabilization exercises)
- **Aerobic**: (walking, cycling, swimming)
- **Yoga**, **Pilates**: (evidence for benefit)
- **Physical therapy**: (supervised exercise program)

**Multidisciplinary Rehabilitation**:
- **Pain management program**
- **CBT**: (for pain catastrophizing, depression)
- **Graded activity**: (fear-avoidance reduction)

**Adjunctive**:
- **Antidepressants**: (amitriptyline 10-50mg nocte, duloxetine 30-60mg daily - for chronic pain)
- **Pregabalin**, **gabapentin**: (if neuropathic component)

---

**Radicular Pain** (Sciatica):

**Conservative**: (6-12 weeks, unless severe/progressive)
- **Exercise**: (McKenzie method, nerve gliding)
- **Analgesia**: (paracetamol, NSAIDs, neuropathic agents)
- **Epidural steroid injection**: (may reduce pain, functional improvement)

**Surgery**: (if severe/progressive neurologic deficit, cauda equina, >12 weeks conservative failed)
- **Discectomy**: (microdiscectomy, laminectomy)

---

## PREVENTION

**Core strengthening**: (plank, bridges, abdominal exercises)
**Posture**: (maintain lumbar lordosis, avoid slouching)
**Ergonomics**: (workstation assessment, lifting techniques)
**Weight management**
**Smoking cessation**: (reduces degeneration risk)
**Regular exercise**

---

## PROGNOSIS

**Good**: (90% recover within 6 weeks)
**Recurrence**: (common, 20-30%)
**Chronic**: (10-20% develop chronic pain)

---

## WHEN TO REFER

**Urgent** (same day):
- **Cauda equina syndrome**: (saddle anesthesia, urinary retention, fecal incontinence, progressive weakness)
- **Severe/progressive neurologic deficit**
- **Infection**, **malignancy** suspected

**Routine**:
- **Red flags** (investigate)
- **>6 weeks** duration, not improving
- **Surgical assessment**: (consider discectomy, decompression)

---

**Sources: NICE NG59 Low Back Pain and Sciatica, European Guidelines, STarT Back Tool**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "low_back_pain",
                "sources": ["NICE NG59", "European Guidelines", "STarT Back Tool"]
            }
        )

    def _handle_fibromyalgia(self, query: str, context: dict) -> DomainQueryResult:
        """Handle fibromyalgia"""
        answer = """**FIBROMYALGIA**

---

## DEFINITION

**Chronic widespread pain** accompanied by fatigue, sleep disturbances, cognitive symptoms, often comorbid with other conditions

---

## EPIDEMIOLOGY

**Prevalence**: (2-8%)
**Sex**: (7-9:1 female:male)
**Age**: (20-50 years peak, but all ages)

---

## CLINICAL FEATURES

**Widespread Pain** (3 months):
- **Bilateral**: (both sides of body)
- **Above and below waist**: (includes upper back, chest)
- **Axial**: (spine, chest)

**Tender Points** (ACR 1990 criteria - not required for diagnosis):
- **18 specific tender points**: (9 pairs - occiput, low cervical, trapezius, supraspinatus, second rib, lateral epicondyle, gluteal, greater trochanter, knee)
- **Diagnosis**: (≥11 tender points on digital palpation - 4 kg pressure)

**Associated Symptoms** (90-100%):
- **Fatigue**: (severe, unrefreshing sleep)
- **Sleep disturbances**: (non-restorative, frequent awakenings)
- **Cognitive**: ("fibro fog" - memory, concentration difficulties)
- **Stiffness**: (generalized, morning stiffness >30 min)
- **Paresthesias**: (numbness, tingling in hands, feet)

**Comorbidities** (30-50%):
- **Depression**, **anxiety**
- **IBS**, **GERD**
- **Migraine**, **tension headache**
- **Interstitial cystitis**
- **Temporomandibular joint dysfunction**

---

## DIAGNOSIS

**ACR 2010 Criteria** (for classification):

**Widespread Pain Index** (WPI) ≥7 **AND** Symptom Severity (SS) score ≥5 **OR** WPI 3-6 **AND** SS score ≥9

**Symptom Severity** (0-3 scale):
- **Fatigue**, **waking unrefreshed**, **cognitive symptoms**, **somatic symptoms** (headache, abdominal pain, IBS)

**Duration**: (≥3 months)

---

**Investigations**:

**Blood**:
- **FBC**, **ESR**, **CRP**: (normal - exclude inflammatory arthritis)
- **TSH**, **CK**: (exclude hypothyroidism, myopathy)
- **Vit D**, **B12**: (exclude deficiency)

**No definitive diagnostic test**: (diagnosis of exclusion)

---

## MANAGEMENT

**Education**:
- **Reassurance**: (benign, no joint damage)
- **Explanation**: (central sensitization, pain amplification)
- **Acceptance**: (diagnosis, chronic nature, focus on management not cure)

**Exercise** (most effective):
- **Aerobic**: (walking, cycling, swimming - 20-30 min, 3x/week)
- **Strengthening**: (gradual, low-intensity)
- **Yoga**, **Tai Chi**, **Pilates**
- **Physical therapy**: (supervised, graded)

**Cognitive Behavioral Therapy** (CBT):
- **Effective** (for pain catastrophizing, maladaptive coping)
- **Group** or individual

**Pharmacological**:

**First-line**:
- **Amitriptyline**: (10-50mg nocte - start low, titrate slowly)
  - **Side effects**: (sedation, dry mouth, constipation, urinary retention)
- **Duloxetine**: (30-60mg daily)
- **Milnacipran**: (not FDA-approved for fibromyalgia)
- **Pregabalin**, **Gabapentin**: (for sleep, neuropathic pain)

**Sleep Hygiene**:
- **Regular schedule**
- **Bedtime routine**: (avoid screens, caffeine, heavy meals before bed)
- **Cool**, **dark**, **quiet** bedroom

**Comorbidities**:
- **Treat**: (depression, anxiety, sleep apnea, IBS, migraines)

---

## PROGNOSIS

**Chronic**: (but symptoms may wax and wane)
**Disability**: (10-30% work disability)
**Improvement**: (with multidisciplinary treatment)

---

## WHEN TO REFER

**Routine**:
- **Suspected fibromyalgia**: (for diagnosis, exclusion of inflammatory arthritis)
- **Refractory**: (to multidisciplinary management - pain clinic, CBT, physical therapy)

---

**Sources: NICE CG59 Fibromyalgia, EULAR Fibromyalgia Guidelines 2016, ACR Criteria**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "rheumatology",
                "focus": "fibromyalgia",
                "sources": ["NICE CG59", "EULAR Fibromyalgia Guidelines 2016", "ACR Criteria"]
            }
        )

    def _handle_soft_tissue(self, query: str, context: dict) -> DomainQueryResult:
        """Handle soft tissue rheumatism (tendinopathies, bursitis)"""
        answer = """**SOFT TISSUE RHEUMATISM**

---

## DEFINITION

**Pain**, **dysfunction** arising from periarticular tissues (tendons, ligaments, bursae, fascia), not from joints

---

## COMMON CONDITIONS

### ROTATOR CUFF TENDINOPATHY

**Anatomy**: (supraspinatus, infraspinatus, teres minor, subscapularis)

**Causes**:
- **Overuse**: (overhead activities - tennis, swimming, painting, window cleaning)
- **Degeneration**: (age-related, impingement)
- **Trauma**: (fall, lifting)
- **Calcific tendinitis**: (calcium deposits)

**Clinical**:
- **Shoulder pain**: (lateral, worse with overhead activity, night pain)
- **Weakness**, **limited ROM** (especially abduction, external rotation)
- **Impingement sign**: (pain with arc between 60-120° abduction)
- **Drop arm sign**: (severe tear)

**Management**:
- **Rest**, **avoid aggravating activities**
- **Physiotherapy**: (rotator cuff strengthening, scapular stabilizer exercises)
- **Analgesia**: (paracetamol, NSAIDs)
- **Subacromial steroid injection**: (if persistent - triamcinolone 40mg + local anesthetic)
- **Surgical repair**: (full-thickness tear in young, active patient)

---

### LATERAL EPICONDYLITIS (TENNIS ELBOW)

**Extensor tendon origin** at lateral epicondyle

**Causes**: (overuse - racquet sports, gripping, twisting)

**Clinical**:
- **Lateral elbow pain**: (worse with gripping, lifting)
- **Tenderness**: (lateral epicondyle)
- **Weak grip**: (painful)
- **Cozen's test**: (pain with resisted wrist extension)

**Management**:
- **Rest**, **activity modification**
- **Bracing**: (epicondylitis clasp)
- **Eccentric exercises**: (Strengthening program - Tyler Twist)
- **Physiotherapy**
- **Steroid injection**: (if refractory - triamcinolone 40mg + local anesthetic, max 2-3)

---

### MEDIAL EPICONDYLITIS (GOLFER'S ELBOW)

**Flexor tendon origin** at medial epicondyle

**Causes**: (golf, throwing, repetitive flexion)

**Clinical**:
- **Medial elbow pain**: (worse with gripping, valgus stress)
- **Tenderness**: (medial epicondyle)
- **Weak grip**
- **Golfer's test**: (pain with resisted wrist flexion)

**Management**: (as lateral epicondylitis)

---

### PLANTAR FASCIITIS

**Causes**: (overuse, flat feet, high arches, obesity, standing)

**Clinical**:
- **Heel pain**: (medial, worst first step in morning, improves with activity)
- **Tenderness**: (medial calcaneal tubercle)
- **Tightness**: (Achilles tendon, calf)

**Management**:
- **Stretching**: (plantar fascia, Achilles tendon, calf)
- **Orthotics**: (arch support, heel cushion)
- **Night splint**: (dorsiflexion splint)
- **NSAIDs**, **ice**
- **Steroid injection**: (if refractory - triamcinolone 40mg + local, avoid multiple)

---

### ACHILLES TENDINOPATHY

**Causes**: (overuse, fluoroquinolones, statins)

**Clinical**:
- **Achilles pain**: (2-6 cm above insertion, worse with activity)
- **Swelling**, **nodularity**
- **Stiffness** (especially morning)

**Management**:
- **Rest**, **avoid aggravating activities**
- **Eccentric exercises**: (Alfredson's protocol)
- **Orthotics** (heel lift)
- **Steroid injection**: (caution - risk of rupture, avoid if possible)
- **Surgery**: (rare, if refractory)

---

### BURSITIS

**Subacromial** (shoulder):
- **Pain**: (lateral shoulder, worse with overhead activity, night pain)
- **Weakness**, limited ROM
- **Management**: (as rotator cuff tendinopathy)

**Trochanteric** (hip):
- **Pain**: (lateral hip, worse with lying on side, stairs, rising from chair)
- **Tenderness**: (greater trochanter)
- **Management**: (rest, ice, NSAIDs, physiotherapy, steroid injection - trochanteric bursa)

**Olecranon** (elbow):
- **Pain**: (posterior elbow, worse with leaning)
- **Swelling**: (over olecranon)
- **Management**: (rest, compression, protection, steroid injection)

**Prepatellar** (knee):
- **Pain**: (anterior knee, worse with kneeling)
- **Swelling**: (over patella)
- **Management**: (rest, ice, knee pads, steroid injection)

---

### DE QUERVAIN'S TENOSYNOVITIS

**Abductor pollicis longus**, **extensor pollicis brevis** tendons

**Causes**: (overuse - texting, lifting, childcare)

**Clinical**:
- **Radial wrist pain**: (base of thumb, worse with thumb movement, gripping)
- **Swelling**: (first dorsal compartment)
- **Finkelstein's test**: (pain with ulnar deviation of wrist with thumb flexed)

**Management**:
- **Rest**, **splinting** (thumb spica)
- **NSAIDs**
- **Steroid injection**: (first dorsal compartment)
- **Surgery**: (if refractory)

---

### TRIGGER FINGER

**Flexor tenosynovitis** with nodular thickening

**Causes**: (overuse, diabetes, RA)

**Clinical**:
- **Catching**, **locking**, **triggering** of finger
- **Nodule**: (palmar aspect of MCP, A1 pulley)
- **Pain**: (base of finger)

**Management**:
- **Rest**
- **Steroid injection**: (into tendon sheath - triamcinolone 40mg + local)
- **Surgical release**: (A1 pulley release - if refractory)

---

## PRINCIPLES

**Diagnosis**: (clinical, imaging usually unnecessary unless atypical)
**Management**: (conservative first, rest, activity modification, physiotherapy, analgesia)
**Steroid Injections**: (use sparingly, avoid in tendons - rupture risk)
**Surgery**: (refractory cases, especially tears)

---

**Sources: NICE CKS Soft Tissue Rheumatism, BSR Guidelines, MSK Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "rheumatology",
                "focus": "soft_tissue_rheumatism",
                "sources": ["NICE CKS", "BSR Guidelines", "MSK Guidelines"]
            }
        )

    def _handle_osteoporosis(self, query: str, context: dict) -> DomainQueryResult:
        """Handle osteoporosis"""
        answer = """**OSTEOPOROSIS**

---

## DEFINITION

**Skeletal disorder** characterized by compromised bone strength, predisposing to increased risk of fracture

**WHO Definition**: (DXA T-score ≤ -2.5)

---

## EPIDEMIOLOGY

**Prevalence**: (women >50 years: 30%, men >50 years: 10%)
**Age**: (postmenopausal women, elderly men)
**Sex**: (3:1 female:male)

---

## RISK FACTORS

**Non-Modifiable**:
- **Age**: (risk increases with age)
- **Sex**: (female)
- **Genetics**: (family history, Caucasian, Asian)
- **Previous fracture**: (major risk factor)
- **Menopause**: (early <45 years)

**Modifiable**:
- **Low BMI**: (<19)
- **Smoking**, **alcohol**
- **Glucocorticoids**: (≥3 months, dose-dependent)
- **Secondary amenorrhea**
- **Hypogonadism**: (men, low testosterone)
- **Medical conditions**: (RA, IBD, celiac, hyperthyroidism, diabetes)
- **Medications**: (aromatase inhibitors, androgen deprivation, anticonvulsants, PPIs)
- **Falls**: (increased risk)

---

## FRACTURE RISK

**Vertebral**: (most common osteoporotic fracture, may be asymptomatic)
- **Compression fracture**: (height loss, kyphosis)
- **Acute back pain**: (may be severe)

**Hip** (most serious):
- **Fragility fracture**: (minor trauma)
- **Morbidity**, **mortality**: (high)

**Wrist** (Colles fracture)

**Humerus**

---

## DIAGNOSIS

**DXA** (dual-energy X-ray absorptiometry):
- **T-score**: (comparison to young adult mean)
  - **Normal**: T-score ≥ -1.0
  - **Osteopenia**: T-score between -1.0 and -2.5
  - **Osteoporosis**: T-score ≤ -2.5
- **Z-score**: (comparison to age-matched, used in premenopausal women, men <50)

**FRAX** (Fracture Risk Assessment):
- **10-year fracture probability**: (major osteoporotic fracture, hip)
- **Treatment threshold**: (based on country guidelines)

**Vertebral Fracture Assessment**:
- **Height loss**: (>2 cm)
- **Kyphosis**
- **X-ray**: (thoracolumbar spine if height loss, pain)

---

## MANAGEMENT

**Lifestyle**:
- **Weight-bearing exercise**: (walking, jogging, strength training)
- **Balance training**: (falls prevention)
- **Smoking cessation**
- **Alcohol moderation**: (≤2 units daily)
- **Fall prevention**: (home safety, vision check, medication review)

**Nutrition**:
- **Calcium**: (1000-1200 mg daily from diet + supplements if needed)
- **Vitamin D**: (800-1000 IU daily, maintain serum 25-OHD >50 nmol/L)
- **Protein**: (1-1.2 g/kg/day)

---

**Pharmacological** (high fracture risk):

**Bisphosphonates** (first-line):
- **Alendronate**: 70mg weekly (oral)
- **Risedronate**: 35mg weekly (oral)
- **Ibandronate**: 150mg monthly (oral)
- **Zoledronic acid**: 5mg IV annually (especially if unable to tolerate oral, adherence issues)

**Denosumab** (RANKL inhibitor):
- **Subcut**: 60mg every 6 months
- **Indications**: (high fracture risk, CKD, bisphosphonate failure)
- **Caution**: (risk of rebound vertebral fractures if stopped - transition to bisphosphonate)

**SERMs** (Selective Estrogen Receptor Modulators):
- **Raloxifene**: 60mg daily (postmenopausal women, reduces breast cancer, increases VTE risk)

**Anabolic Agents** (severe osteoporosis, fractures):
- **Teriparatide**: (PTH 1-34, 20 mcg SC daily for 18-24 months)
- **Romosozumab**: (sclerostin antibody, 210mg SC monthly for 12 months)

**HRT** (Hormone Replacement Therapy):
- **Indication**: (early menopause <45 years, menopausal symptoms)
- **Bone benefit**: (reduces fracture risk if started within 10 years of menopause)

**Testosterone**: (men with hypogonadism)

---

## MONITORING

**DXA**: (repeat every 2-3 years during treatment)
**Height**: (annual)
**Biochemistry**: (calcium, vitamin D, PTH, bone turnover markers)

---

## FRACTURE ASSESSMENT

**Hip Fracture**:
- **Urgent referral**: (orthopedics, surgical management)
- **Investigate**: (after fracture - DXA, secondary causes)

**Vertebral Fracture**:
- **X-ray**: (confirm diagnosis, assess severity)
- **MRI**: (if acute, uncertain)
- **Management**: (pain control, orthosis, consider vertebroplasty/kyphoplasty if severe pain, recent fracture)

---

## GLUCOCORTICOID-INDUCED OSTEOPOROSIS

**Risk** (dose-dependent):
- **≥5 mg prednisolone daily** for ≥3 months
- **Fracture risk**: (increases rapidly)

**Management**:
- **Lowest effective dose**: (of steroids)
- **Bisphosphonates**: (alendronate, risedronate)
- **Calcium**, **Vitamin D**
- **Monitor**: (DXA at baseline, 1-2 years, then every 2-3 years)

---

## PROGNOSIS

**Good**: (with treatment, reduces fracture risk 30-70%)
**Hip fracture**: (12-month mortality 20-30%)
**Vertebral fracture**: (pain, disability, height loss, kyphosis, mortality)

---

## WHEN TO REFER

**Urgent**:
- **Fragility fracture**: (for orthopedic management, DXA, osteoporosis assessment)

**Routine**:
- **T-score ≤ -2.5**: (to start treatment)
- **T-score between -1.0 and -2.5**: (if FRAX high fracture risk)
- **Long-term glucocorticoids**: (if ≥3 months, consider prophylaxis)
- **Monitoring**: (response to treatment, consider second-line if fracture on treatment)

---

**Sources: NICE NG143 Osteoporosis, BSR Osteoporosis Guidelines 2021, NOGG Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "rheumatology",
                "focus": "osteoporosis",
                "sources": ["NICE NG143", "BSR Osteoporosis Guidelines 2021", "NOGG Guidelines"]
            }
        )

    def _handle_paget(self, query: str, context: dict) -> DomainQueryResult:
        """Handle Paget's disease of bone"""
        answer = """**PAGET'S DISEASE OF BONE (OSTEITIS DEFORMANS)**

---

## DEFINITION

**Chronic bone disorder** characterized by excessive bone resorption followed by disorganized bone repair, leading to bone pain, deformity, fracture

---

## EPIDEMIOLOGY

**Prevalence**: (1-3% >55 years, increases with age)
**Age**: (>55 years, rare <40)
**Sex**: (slight male predominance)
**Geographic**: (common in UK, Europe, North America, rare in Asia, Africa)

---

## PATHOPHYSIOLOGY

**Osteoclastic** (increased bone resorption)
**Osteoblastic** (increased but disorganized bone formation)

**Initial**: (lytic phase - hot, hypervascular)
**Mixed**: (lytic + blastic - most active)
**Late**: (blastic phase - cold, sclerotic)

---

## CLINICAL FEATURES

**Asymptomatic**: (20-30% discovered incidentally)

**Bone Pain**: (most common symptom)
- **Dull, aching**: (worse at night, with warmth)
- **Weight-bearing bones**: (tibia, femur, pelvis, spine)
- **Increased local temperature**

**Deformity**:
- **Long bones**: (bowing, enlargement)
- **Skull**: (enlargement - "hat size" increase)
- **Tibia**: (saber shin - anterior bowing)

**Fracture**: (pathological, through diseased bone)
- **Femur**, **tibia**, **humerus**

**Nerve Compression**:
- **Hearing loss**: (temporal bone - 8th nerve)
- **Vertebral**: (spinal stenosis, cauda equina)
- **Base of skull**: (platybasia, basilar invagination)

**Increased vascularity**: (lytic phase)
- **Warmth** over bone
- **High-output heart failure** (rare)

---

## DIAGNOSIS

**X-ray**:
- **Osteolysis**: (lytic lesion)
- **Coarsening**: of trabeculae
- **Cortical thickening**: (long bones)
- **Sclerosis**: (blastic phase)
- **Bone enlargement**
- **Specific sites**: (pelvis, femur, tibia, spine, skull, humerus)

**Bone Scan**: (increased uptake - "hot spot")
- **Sensitive**: (detects extent, asymptomatic disease)

**Blood**:
- **ALP** (alkaline phosphatase): (elevated, marker of bone turnover)
- **Calcium**, **phosphate**: (usually normal)
- **25-OHD**, **PTH**: (exclude hyperparathyroidism)

**Urine**:
- **Hydroxyproline**, **Pyrilinks**: (markers of bone resorption - historical)

**Genetics**:
- **SQSTM1**: (p62 gene - Paget's susceptibility)

---

## MANAGEMENT

**Asymptomatic**: (no treatment needed)

**Symptomatic**:

**Bisphosphonates** (first-line):
- **Risedronate**: 30mg daily for 2-6 months
- **Alendronate**: 40mg daily for 6 months
- **Zoledronic acid**: 5mg IV single dose (often curative)

**Monitoring**:
- **ALP**: (marker of disease activity - should normalize with treatment)
- **Pain**: (should improve)
- **X-ray**: (healing - sclerosis)

**Surgery**:
- **Deformity correction**: (osteotomy, especially tibia, femur)
- **Joint replacement**: (if secondary OA, especially hip, knee)
- **Fracture fixation**

**Hearing Assessment**:
- **Audiometry**: (if temporal bone involvement)

---

## COMPLICATIONS

**Bone deformity**: (bowing, enlargement)
**Fracture**: (pathologic, delayed union)
**Osteoarthritis**: (secondary to deformity - hip, knee)
**Nerve compression**: (hearing loss, spinal stenosis, basilar invagination)
**Sarcoma**: (osteosarcoma, <1%)
**Hypercalcemia**: (in immobilized patients - lytic phase)

---

## PROGNOSIS

**Good**: (with bisphosphonate treatment, long remission)
**Morbidity**: (deformity, arthritis, fracture)
**Mortality**: (slightly increased, mainly due to complications)

---

## WHEN TO REFER

**Urgent**:
- **Fracture**: (through Paget's disease - orthopedic management)
- **Nerve compression**: (spinal stenosis, basilar invagination)

**Routine**:
- **Suspected Paget's**: (for diagnosis, treatment)
- **Symptomatic**: (pain, deformity)
- **Surgical planning**: (deformity correction, joint replacement)

---

**Sources: NICE CKS Paget's Disease, Paget's Association Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "rheumatology",
                "focus": "paget_disease",
                "sources": ["NICE CKS", "Paget's Association Guidelines"]
            }
        )

    def _handle_jia(self, query: str, context: dict) -> DomainQueryResult:
        """Handle juvenile idiopathic arthritis"""
        answer = """**JUVENILE IDIOPATHIC ARTHRITIS (JIA)**

---

## DEFINITION

**Chronic arthritis** of unknown cause, onset <16 years, lasting ≥6 weeks

---

## EPIDEMIOLOGY

**Incidence**: (10-20 per 100,000)
**Age**: (peak 1-4 years)
**Sex**: (varies by subtype)

---

## CLASSIFICATION (ILAR)

**Oligoarticular** (60%):
- **Persistent**: (≤4 joints, 6 months)
- **Extended**: (>4 joints after 6 months)
- **Age**: (early onset <6 years)
- **Sex**: (F>M)
- **ANA positive** (high risk of uveitis)

**Polyarticular RF-Negative** (20%):
- **≥5 joints**, **RF negative**
- **Age**: (bimodal: early <6, late >10)
- **Sex**: (F>M)

**Polyarticular RF-Positive** (10%):
- **≥5 joints**, **RF positive**
- **Age**: (late onset, >10 years)
- **Sex**: (F>M)
- **Resembles adult RA**

**Systemic JIA** (10%:
- **Still's disease**: (daily fever ≥2 weeks, evanescent rash, arthritis)
- **Age**: (bimodal: <5, >10)
- **Sex**: (equal)
- **Macrophage activation syndrome**: (life-threatening)

**Psoriatic** (10%):
- **Arthritis** ± psoriasis
- **Dactylitis**: (sausage digit)
- **Nail pitting**
- **Family history**: (psoriasis)

**Enthesitis-Related Arthritis** (10%):
- **Arthritis**, **enthesitis**
- **HLA-B27 positive**
- **Boys >6 years**: (common)
- **Sacroiliitis**, **spinal involvement**

**Undifferentiated** (10%):
- **Arthritis**: (does not fit criteria for any category)

---

## CLINICAL FEATURES

**Arthritis**:
- **Swelling**, **pain**, **limited ROM**
- **Morning stiffness** (>30 min)
- **Limp**, (guarding)

**Systemic** (Systemic JIA):
- **Daily fever**: (quotidian, spiking)
- **Evanescent rash**: (salmon-pink, maculopapular, migratory, with fever)
- **Lymphadenopathy**, **hepatosplenomegaly**
- **Serositis**: (pericarditis, pleuritis)
- **Anemia**, **leukocytosis**, **thrombocytosis**

**Uveitis**:
- **Oligoarticular**: (30% risk, ANA positive)
- **Asymptomatic**: (usually)
- **Chronic**: (synechiae, cataract, visual loss)

**Growth Failure**:
- **Chronic inflammation**, **steroids**
- **Delayed puberty**, **short stature**

---

## DIAGNOSIS

**Clinical**: (arthritis ≥6 weeks, exclude other causes)

**Blood**:
- **FBC**: (anemia, leukocytosis, thrombocytosis - systemic JIA)
- **ESR**, **CRP**: (elevated)
- **RF**, **ANA**: (autoantibodies)
- **HLA-B27**: (enthesitis-related)

**Imaging**:
- **X-ray**: (periarticular osteopenia, erosions, joint space narrowing, growth disturbances)
- **MRI**: (synovitis, tenosynovitis, enthesitis)
- **Ultrasound**: (synovitis)

**Slit Lamp**: (uveitis screening - especially oligoarticular, ANA positive)

---

## DIFFERENTIAL DIAGNOSIS

**Infection**: (septic arthritis, osteomyelitis)
**Malignancy**: (leukemia, neuroblastoma)
**Trauma**
**Mechanical**: (hypermobility, overuse)
**Other CTD**: (SLE, JDM)

---

## MANAGEMENT

**Multidisciplinary**: (pediatric rheumatology, physiotherapy, occupational therapy, ophthalmology)

**NSAIDs**:
- **Naproxen**: 10-15 mg/kg/day BID
- **Ibuprofen**: 30-40 mg/kg/day TID-QID
- **Diclofenac**: 1-3 mg/kg/day TID
- **Duration**: (until disease control)

**Intra-articular Steroids**:
- **Triamcinolone hexacetonide**: (1 mg/kg, max 40mg, for persistent monoarthritis)

**DMARDs** (if NSAIDs inadequate):
- **Methotrexate**: (10-15 mg/m² weekly, folic acid 5mg weekly)
- **Sulfasalazine**
- **Leflunomide**

**Biologics** (if DMARDs inadequate):
- **Anti-TNF**: (etanercept, adalimumab)
- **Tocilizumab**: (IL-6 inhibitor, especially systemic JIA)

**Systemic JIA**:
- **High-dose steroids**: (prednisolone 1-2 mg/kg/day)
- **Anakinra**: (IL-1 receptor antagonist - first-line for systemic JIA)
- **Cyclosporine**, **tacrolimus**
- **Biologics**: (tocilizumab, canakinumab)

**Physical Therapy**:
- **Maintain ROM**: (prevent contractures)
- **Strengthening**: (prevent muscle atrophy)
- **Gait training**: (if limping)

**Occupational Therapy**:
- **Joint protection**
- **Assistive devices**: (splints, adaptive equipment)
- **School adaptation**

**Ophthalmology**:
- **Regular slit lamp**: (every 3-6 months, especially oligoarticular, ANA positive)

---

## COMPLICATIONS

**Uveitis**:
- **Cataract**, **synechiae**
- **Glaucoma**, **visual loss**

**Growth Disturbance**:
- **Local**: (leg length discrepancy, premature epiphyseal fusion)
- **Systemic**: (steroid-induced, chronic inflammation)

**Joint Contractures**, **deformity**
**Amyloidosis** (rare, systemic JIA)

---

## PROGNOSIS

**Variable**: (by subtype)
**Oligoarticular**: (good, 50% remission)
**Polyarticular RF-positive**: (more aggressive, resembles RA)
**Systemic**: (morbidity from amyloidosis, MAS)
**Extended oligoarticular**: (worse prognosis)

---

## WHEN TO REFER

**Urgent**:
- **Suspected JIA**: (for prompt diagnosis, treatment)
- **Systemic JIA**: (MAS - life-threatening)
- **Uveitis**: (ophthalmology)

**Routine**:
- **Confirmed JIA**: (for ongoing management)

---

**Sources: NICE NG100 JIA, BSR JIA Guidelines, PRINTO Guidelines**
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "rheumatology",
                "focus": "juvenile_idiopathic_arthritis",
                "sources": ["NICE NG100", "BSR JIA Guidelines", "PRINTO Guidelines"]
            }
        )

    def _handle_general_rheumatology(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general rheumatology consultation"""
        answer = """**GENERAL RHEUMATOLOGY CONSULTATION**

Rheumatology covers the diagnosis and management of musculoskeletal and autoimmune diseases.

**Common Conditions Managed**:
- **Inflammatory arthritis**: Rheumatoid arthritis, psoriatic arthritis, ankylosing spondylitis, gout, pseudogout
- **Connective tissue diseases**: SLE, Sjögren's, scleroderma, myositis
- **Degenerative joint disease**: Osteoarthritis
- **Spinal disorders**: Low back pain, neck pain
- **Vasculitis**: Giant cell arteritis, PAN, ANCA-associated, Henoch-Schönlein purpura
- **Soft tissue**: Tendinopathies, bursitis, fibromyalgia
- **Bone health**: Osteoporosis, Paget's disease
- **Pediatric**: Juvenile idiopathic arthritis, Kawasaki disease

**Diagnostic Approaches**:
- **Joint examination**: Inspection, palpation, ROM, special tests
- **Blood tests**: Autoantibodies, inflammatory markers, organ function
- **Imaging**: X-ray, ultrasound, MRI, CT (appropriate to condition)
- **Biopsy**: Temporal artery, synovium, kidney, skin (if indicated)

**When to Seek Urgent Review**:
- **GCA symptoms**: (headache, scalp tenderness, jaw claudication, visual changes - EMERGENCY)
- **Septic arthritis**: (single hot swollen joint - EMERGENCY)
- **SLE**: (new rash, renal impairment, neurologic symptoms)
- **Severe back pain**: (fever, trauma, neurologic deficits, unexplained weight loss)
- **Organ involvement**: (dyspnea, renal failure, red urine)

**Sources**: BSR Guidelines, NICE Rheumatology Guidelines, EULAR Recommendations
"""

        return DomainQueryResult(
            domain_name="rheumatology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "rheumatology",
                "focus": "general_consultation",
                "sources": ["BSR Guidelines", "NICE Rheumatology Guidelines", "EULAR Recommendations"]
            }
        )


def create_rheumatology_domain():
    """Factory function to create rheumatology domain instance"""
    return RheumatologyDomain()


# Domain registration
try:
    from gpdisc_core.domains.registry import DomainModuleRegistry
    DomainModuleRegistry.register(RheumatologyDomain)
except ImportError:
    # Registry not available yet
    pass
