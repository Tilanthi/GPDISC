"""
Orthopedics Domain Module for GPDISC
=======================================

This domain specializes in musculoskeletal conditions, trauma, and orthopedic surgery.
Provides consultation on fractures, joint disorders, sports injuries, and bone health.

Key capabilities:
- Fracture assessment and management
- Joint pain evaluation (hip, knee, shoulder, spine)
- Sports injuries and soft tissue injuries
- Arthritis management (osteoarthritis, rheumatoid arthritis)
- Back pain and spinal conditions
- Orthopedic post-operative care
- Bone health and osteoporosis
- Pre-operative consultation for orthopedic surgery

Privacy: All patient data stored locally, no external transmission.
"""

from typing import Dict, Any, Optional
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult


class OrthopedicsDomain(BaseDomainModule):
    """Orthopedics domain specializing in musculoskeletal conditions and trauma."""

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="orthopedics",
            version="1.0.0",
            dependencies=[],
            description="Musculoskeletal conditions, trauma, fractures, arthritis, sports medicine, orthopedic surgery",
            keywords=[
                "bone", "joint", "fracture", "break", "crack", "orthopedic", "orthopaedic",
                "musculoskeletal", "sports injury", "sprain", "strain", "ligament", "tendon",
                "arthritis", "osteoarthritis", "rheumatoid arthritis", "inflammation",
                "back pain", "lower back pain", "sciatica", "disc", "spine", "spinal",
                "hip", "hip pain", "hip replacement", "knee", "knee pain", "knee replacement",
                "shoulder", "shoulder pain", "rotator cuff", "elbow", "wrist", "hand",
                "ankle", "foot", "heel", "achilles", "gout", "pseudogout",
                "osteoporosis", "bone health", "calcium", "vitamin d", "bone density",
                "trauma", "injury", "accident", "fall", "car accident", "whiplash",
                "meniscus", "acl", "pcl", "mcl", "lcl", "cartilage", "labrum",
                "bursitis", "tendonitis", "tennis elbow", "golfer's elbow", "frozen shoulder",
                "trigger finger", "carpal tunnel", "dupuytren's", "ganglion cyst"
            ],
            capabilities=[
                "fracture_assessment",
                "joint_evaluation",
                "sports_injury_management",
                "arthritis_management",
                "spinal_conditions",
                "orthopedic_surgery_consultation",
                "bone_health",
                "postoperative_care"
            ]
        )

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> DomainQueryResult:
        """Process orthopedics-related queries."""
        try:
            query_lower = query.lower()

            # Fracture/trauma
            if any(term in query_lower for term in ["fracture", "broken", "break", "crack", "trauma", "fall", "accident"]):
                return self._handle_fracture_query(query, context)

            # Joint pain
            elif any(term in query_lower for term in ["joint pain", "hip pain", "knee pain", "shoulder pain", "elbow pain"]):
                return self._handle_joint_pain_query(query, context)

            # Back/spine
            elif any(term in query_lower for term in ["back pain", "spine", "spinal", "sciatica", "disc", "slipped disc"]):
                return self._handle_spine_query(query, context)

            # Arthritis
            elif any(term in query_lower for term in ["arthritis", "inflammation", "osteoarthritis", "rheumatoid", "joint stiffness"]):
                return self._handle_arthritis_query(query, context)

            # Sports injury
            elif any(term in query_lower for term in ["sports injury", "sprain", "strain", "acl", "meniscus", "ligament"]):
                return self._handle_sports_injury_query(query, context)

            # Soft tissue
            elif any(term in query_lower for term in ["tendon", "ligament", "muscle", "bursitis", "tendonitis", "frozen"]):
                return self._handle_soft_tissue_query(query, context)

            # Bone health
            elif any(term in query_lower for term in ["osteoporosis", "bone health", "bone density", "calcium"]):
                return self._handle_bone_health_query(query, context)

            # Surgery
            elif any(term in query_lower for term in ["surgery", "operation", "replacement", "arthroscopy"]):
                return self._handle_surgery_query(query, context)

            # General orthopedics
            else:
                return self._handle_general_orthopedics_query(query, context)

        except Exception as e:
            return DomainQueryResult(
                domain_name="orthopedics",
                answer=f"Error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )

    def _handle_fracture_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle fracture assessment queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Fracture Assessment - Orthopedic Second Opinion**\n\n"
                "**⚠️ WARNING**: If you have a suspected fracture, **seek urgent medical attention** "
                "(A&E/Minor Injury Unit or Urgent Care). **Do not delay.**\n\n"
                "**Fracture Signs**:\n"
                "- **Pain**: Severe, worse with movement/weight-bearing\n"
                "- **Swelling**: Rapid onset, significant\n"
                "- **Deformity**: Visible deformity, angulation\n"
                "- **Inability to use**: Cannot bear weight or use limb\n"
                "- **Bruising**: May develop over hours\n\n"
                "**Urgent Assessment Indicated If**:\n"
                "- Open fracture (bone visible)\n"
                "- Deformity\n"
                "- Inability to move limb/weight-bear\n"
                "- Numbness/tingling (nerve injury)\n"
                "- Pale/cold limb (vascular injury)\n\n"
                "**Common Fractures**:\n\n"
                "**Hip Fracture** (elderly, fall):\n"
                "- Groin pain, shortened, externally rotated leg\n"
                "- **URGENT**: Surgical fixation required\n\n"
                "**Distal Radius Fracture** (FOOSH - fall on outstretched hand):\n"
                "- Wrist pain, dinner fork deformity\n"
                "- X-ray, possible manipulation/plating\n\n"
                "**Ankle Fracture**:\n"
                "- Pain, swelling, inability to weight-bear\n"
                "- X-ray, possible ORIF if unstable\n\n"
                "**Rib Fracture**:\n"
                "- Pain with breathing, coughing\n"
                "- Conservative management (pain control)\n\n"
                "**Vertebral Compression Fracture**:\n"
                "- Back pain after fall (or spontaneous in osteoporosis)\n"
                "- X-ray, consider vertebroplasty if severe\n\n"
                "**Initial Management** (before hospital):\n"
                "- **Immobilize**: Don't move fractured limb\n"
                "- **Elevate**: Reduce swelling\n"
                "- **Ice**: Reduce pain/swelling (15 min every 2-3 hours)\n"
                "- **Analgesia**: Paracetamol, avoid NSAIDs if surgery possible\n"
                "- **DON'T**: Attempt to manipulate fracture\n\n"
                "**Definitive Treatment**:\n"
                "- **Conservative**: Cast/splint (non-displaced, stable fractures)\n"
                "- **Surgical**: ORIF (open reduction internal fixation), intramedullary nailing, plating, external fixation\n\n"
                "**Healing Time**:\n"
                "- Adults: 6-12 weeks (variable by bone/age)\n"
                "- Children: Faster (4-6 weeks)\n"
                "- Delayed union: >3 months\n"
                "- Non-union: >6 months with no healing\n\n"
                "**Disclaimer**: Fractures require urgent medical assessment. This is guidance, not diagnosis."
            ),
            confidence=0.88,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "fracture_assessment",
                "urgency": "urgent"
            }
        )

    def _handle_joint_pain_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle joint pain queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Joint Pain Evaluation - Orthopedic Second Opinion**\n\n"
                "To provide consultation, please specify which joint(s), characteristics, duration, and functional impact.\n\n"
                "**Common Joint Pain Presentations**:\n\n"
                "**Hip Pain**:\n"
                "- **Osteoarthritis**: Groin pain, stiffness, reduced range, pain with walking\n"
                "- **Greater trochanteric pain**: Lateral hip pain, tenderness, bursitis\n"
                "- **Referred pain**: From lumbar spine (radiculopathy)\n"
                "- **Investigation**: X-ray (AP pelvis), consider ultrasound if trochanteric pain\n"
                "- **Treatment**: NSAIDs, physiotherapy, weight loss, consider joint replacement\n\n"
                "**Knee Pain**:\n"
                "- **Osteoarthritis**: Pain worse with activity, stiffness <30 min, crepitus\n"
                "- **Meniscal tear**: Mechanical symptoms (catching, locking), joint line tenderness\n"
                "- **Ligament injury**: ACL (instability, pivoting), MCL/LCL (medial/lateral pain)\n"
                "- **Patellofemoral**: Anterior knee pain, worse with stairs/sitting\n"
                "- **Investigation**: X-ray (weight-bearing), MRI if ligament/meniscal injury suspected\n"
                "- **Treatment**: Physiotherapy, NSAIDs, injections, arthroscopy, replacement\n\n"
                "**Shoulder Pain**:\n"
                "- **Rotator cuff**: Pain with overhead activity, weakness, painful arc\n"
                "- **Frozen shoulder**: Stiffness (global), pain, phases (freezing, frozen, thawing)\n"
                "- **Acromioclavicular joint**: Localized pain at top of shoulder\n"
                "- **Investigation**: X-ray, ultrasound (rotator cuff), MRI (tear, labrum)\n"
                "- **Treatment**: Physiotherapy, steroid injection, subacromial decompression, cuff repair\n\n"
                "**Elbow Pain**:\n"
                "- **Tennis elbow (lateral epicondylitis)**: Lateral pain, gripping, wrist extension\n"
                "- **Golfer's elbow (medial epicondylitis)**: Medial pain, gripping, wrist flexion\n"
                "- **Olecranon bursitis**: Posterior swelling, redness\n"
                "- **Treatment**: Physiotherapy, brace, steroid injection, surgery if refractory\n\n"
                "**Hand/Wrist Pain**:\n"
                "- **Carpal tunnel**: Numbness/tingling in median nerve distribution, worse at night\n"
                "- **Trigger finger**: Catching, locking, painful clicking\n"
                "- **Thumb base arthritis**: Pain with pinch, grip weakness\n"
                "- **Treatment**: Splinting, steroid injection, carpal tunnel release, surgery\n\n"
                "**Red Flags**:\n"
                "- Septic arthritis (hot, swollen joint, fever) - URGENT\n"
                "- Acute hemarthrosis (trauma, bleeding disorder)\n"
                "- Malignancy (unexplained weight loss, night pain)\n\n"
                "**Disclaimer**: Joint pain may require imaging and specialist assessment."
            ),
            confidence=0.86,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "joint_evaluation"
            }
        )

    def _handle_spine_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle spinal/back pain queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Spine/Back Pain Consultation - Orthopedic Second Opinion**\n\n"
                "**⚠️ RED FLAGS - Urgent Imaging/Referral**:\n"
                "- **Cauda equina**: Saddle anesthesia, urinary retention, fecal incontinence\n"
                "- **Infection**: Fever, IV drug use, recent infection\n"
                "- **Fracture**: Major trauma, osteoporosis, steroid use\n"
                "- **Malignancy**: Unexplained weight loss, night pain, age >50, history of cancer\n"
                "- **Progressive neurological deficit**: Weakness, gait disturbance\n\n"
                "**Low Back Pain (LBP) Classification**:\n\n"
                "1. **Mechanical LBP** (90%):\n"
                "   - Non-specific, no radiculopathy\n"
                "   - **Treatment**: NSAIDs, physiotherapy, early mobilization\n"
                "   - **Prognosis**: 80-90% recover within 6 weeks\n\n"
                "2. **Radiculopathy** (sciatica):\n"
                "   - Pain radiating down leg, numbness/tingling, weakness\n"
                "   - Most common: L4-L5, L5-S1 (affects L5, S1 roots)\n"
                "   - **Investigation**: MRI if persistent (>6-12 weeks) or severe\n"
                "   - **Treatment**: NSAIDs, physiotherapy, consider discectomy if persistent\n\n"
                "3. **Spinal Stenosis**:\n"
                "   - Neurogenic claudication: Pain/weakness with walking, relieved by sitting\n"
                "   - Usually L2-L3, L3-L4, L4-L5 levels\n"
                "   - **Investigation**: MRI\n"
                "   - **Treatment**: Physiotherapy, epidural steroid, decompression if severe\n\n"
                "**Specific Causes**:\n"
                "- **Herniated disc**: Back pain ± radiculopathy, worse with sitting, coughing\n"
                "- **Spondylolisthesis**: Slip of one vertebra on another (isthmic vs degenerative)\n"
                "- **Spondylosis**: Degenerative changes, facet joint arthropathy\n"
                "- **Ankylosing spondylitis**: Inflammatory back pain (<45 y, morning stiffness, improves with activity)\n\n"
                "**Imaging**:\n"
                "- **X-ray**: First-line, shows fracture, spondylolisthesis, spondylosis\n"
                "- **MRI**: Gold standard for disc herniation, spinal stenosis, infection, malignancy\n"
                "- **CT**: Better bone detail, contraindication to MRI\n\n"
                "**Treatment**:\n"
                "- **Non-surgical**: 90% improve with conservative care (NSAIDs, PT, time)\n"
                "- **Surgical indications**: Cauda equina, progressive deficit, severe stenosis, persistent radiculopathy (>6-12 weeks)\n"
                "- **Procedures**: Discectomy, decompression, fusion, disc replacement\n\n"
                "**Prevention**:\n"
                "- Core strengthening, proper lifting technique, ergonomic workstation\n"
                "- Weight management, smoking cessation\n"
                "- Regular low-impact exercise (walking, swimming)\n\n"
                "**Disclaimer**: Back pain with red flags requires urgent assessment."
            ),
            confidence=0.88,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "spinal_conditions"
            }
        )

    def _handle_arthritis_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle arthritis queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Arthritis Management - Orthopedic Second Opinion**\n\n"
                "**Osteoarthritis (OA)** - Degenerative joint disease:\n\n"
                "**Common Sites**: Knee, hip, hand (DIP, PIP, CMC), spine\n"
                "**Symptoms**: Pain with activity, stiffness (<30 min), crepitus, reduced function\n"
                "**Risk Factors**: Age, obesity, previous injury, family history, occupational\n\n"
                "**Management**:\n"
                "- **Weight loss**: 5-10% weight loss significantly reduces symptoms\n"
                "- **Exercise**: Strengthening, aerobic, range of motion\n"
                "- **Analgesia**: Paracetamol first-line, topical NSAIDs, consider oral NSAIDs\n"
                "- **Injections**: Steroid (rapid but temporary), hyaluronic acid (controversial)\n"
                "- **Surgery**: Arthroscopy (rarely, only if mechanical symptoms), osteotomy (younger), joint replacement (end-stage)\n\n"
                "**Joint Replacement**:\n"
                "- **Indications**: Pain unresponsive to conservative, loss of function, night pain\n"
                "- **Hip replacement**: Excellent outcomes, lasts 15-20 years\n"
                "- **Knee replacement**: Good outcomes, lasts 15-20 years\n"
                "- **Recovery**: 6-12 weeks for basic recovery, 6-12 months for full\n\n"
                "**Rheumatoid Arthritis (RA)** - Inflammatory arthritis:\n\n"
                "**Symptoms**: Morning stiffness >1 hour, symmetrical, swelling, fatigue, systemic features\n"
                "**Pathology**: Autoimmune, synovitis, joint erosion\n"
                "**Treatment** (rheumatology-led):\n"
                "- **DMARDs**: Methotrexate first-line, sulfasalazine, hydroxychloroquine\n"
                "- **Biologics**: TNF inhibitors (if DMARD failure)\n"
                "- **Orthopedic surgery**: Synovectomy, tendon repair, joint replacement (after disease control)\n\n"
                "**Other Arthropathies**:\n"
                "- **Gout**: Podagra (1st MTP), severe inflammatory arthritis, treat with colchicine, NSAIDs, steroids; long-term allopurinol/febuxostat\n"
                "- **Pseudogout (CPPD)**: Similar to gout, knee/wrist affected, intra-articular calcification on X-ray\n"
                "- **Psoriatic arthritis**: Associated with psoriasis, DIP involvement, dactylitis\n"
                "- **Ankylosing spondylitis**: Inflammatory back pain, sacroiliitis, bamboo spine\n\n"
                "**Diagnosis**:\n"
                "- **X-ray**: Joint space narrowing, osteophytes, subchondral sclerosis, cysts\n"
                "- **Blood tests**: ESR/CRP (inflammatory), RF, anti-CCP (RA), uric acid (gout)\n"
                "- **Arthrocentesis**: Septic arthritis ruled out, crystal analysis (gout/pseudogout)\n\n"
                "**Disclaimer**: RA requires rheumatology management. Septic arthritis is urgent."
            ),
            confidence=0.86,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "arthritis_management"
            }
        )

    def _handle_sports_injury_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle sports injury queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Sports Injury Consultation - Orthopedic Second Opinion**\n\n"
                "**Common Sports Injuries**:\n\n"
                "**Knee Injuries**:\n"
                "- **ACL tear**: Pivoting sport, \"pop\", immediate swelling, instability\n"
                "  - **Diagnosis**: Lachman, pivot shift, MRI\n"
                "  - **Treatment**: ACL reconstruction (active individuals), physiotherapy\n"
                "- **Meniscal tear**: Twisting injury, mechanical symptoms, joint line pain\n"
                "  - **Diagnosis**: McMurray, Apley, MRI\n"
                "  - **Treatment**: Conservative (outer third), repair (vascular zone), menisectomy\n"
                "- **Patellar dislocation**: Lateral displacement, medial pain, apprehension\n"
                "  - **Treatment**: Reduction, immobilization, physiotherapy, consider surgery if recurrent\n\n"
                "**Ankle Injuries**:\n"
                "- **Lateral ankle sprain**: Inversion injury, ATFL/CFL injury\n"
                "  - **Grades**: 1 (stretch), 2 (partial tear), 3 (complete tear)\n"
                "  - **Treatment**: RICE, physiotherapy, bracing, surgery (Grade 3, high-demand athlete)\n\n"
                "**Shoulder Injuries**:\n"
                "- **Rotator cuff tear**: Overhead activity, pain, weakness, >40 years\n"
                "  - **Diagnosis**: Empty can, drop arm, ultrasound/MRI\n"
                "  - **Treatment**: Physiotherapy (small/partial), repair (large, full-thickness, active)\n"
                "- **Labral tears (SLAP)**: Throwing athletes, popping, clicking\n"
                "- **AC joint separation**: Fall on shoulder, deformity, classification (I-VI)\n\n"
                "**Muscle Injuries**:\n"
                "- **Hamstring strain**: Sprinting, posterior thigh pain, grade 1-3\n"
                "  - **Recovery**: 1-6 weeks depending on grade, high recurrence risk\n"
                "- **Calf strain**: Tennis leg (gastrocnemius), sudden push-off\n"
                "- **Achilles tendon rupture**: \"pop\", gap, inability to plantarflex\n"
                "  - **Treatment**: Surgical (young, active), conservative (older, less active)\n\n"
                "**Stress Fractures**:\n"
                "- **Common sites**: Metatarsals, tibia, femoral neck, pars interarticularis\n"
                "- **Risk factors**: Overtraining, female athlete triad, osteoporosis\n"
                "- **Diagnosis**: X-ray (may be normal initially), MRI/bone scan\n"
                "- **Treatment**: Rest, non-weight-bearing if lower limb, gradual return\n\n"
                "**Return to Sport**:\n"
                "- **Criteria**: Pain-free, full strength, full range, functional testing\n"
                "- **Progression**: Sport-specific drills → non-contact → full contact\n"
                "- **Prevention**: Strengthening, proper technique, adequate recovery\n\n"
                "**RICE vs PEACE & LOVE**:\n"
                "- **RICE** (Rest, Ice, Compression, Elevation): Acute phase (first 24-48 hours)\n"
                "- **PEACE & LOVE**: Protect, Elevate, Avoid anti-inflammatories, Compress, Educate + Load, Optimism, Vascularization, Exercise\n\n"
                "**Disclaimer**: Sports injuries may require imaging and specialist assessment."
            ),
            confidence=0.86,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "sports_medicine"
            }
        )

    def _handle_soft_tissue_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle soft tissue injury queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Soft Tissue Injury - Orthopedic Second Opinion**\n\n"
                "**Tendinopathies**:\n"
                "- **Tennis elbow (lateral epicondylitis)**: Repetitive gripping, wrist extension\n"
                "  - **Exam**: Tenderness at lateral epicondyle, pain with resisted wrist extension\n"
                "  - **Treatment**: Counter-force brace, eccentric exercises, steroid injection (short-term), PRP (emerging)\n"
                "- **Golfer's elbow (medial epicondylitis)**: Medial pain, wrist flexion\n"
                "- **Achilles tendinopathy**: Mid-substance pain, stiffness, worse with activity\n"
                "  - **Treatment**: Eccentric exercises, shockwave therapy, consider surgery if >6 months refractory\n"
                "- **Patellar tendinopathy (jumper's knee)**: Anterior knee pain, jumping sports\n\n"
                "**Bursitis**:\n"
                "- **Trochanteric bursitis**: Lateral hip pain, tenderness, can't sleep on affected side\n"
                "- **Subacromial bursitis**: Shoulder pain, impingement, painful arc\n"
                "- **Olecranon bursitis**: Posterior elbow swelling, student's elbow\n"
                "- **Prepatellar bursitis**: Anterior knee swelling, housemaid's knee\n"
                "**Treatment**: Avoid aggravating activity, NSAIDs, steroid injection, aspiration if infected\n\n"
                "**Tendonitis vs Tendinosis**:\n"
                "- **Tendonitis**: Acute inflammation, short-term, NSAIDs effective\n"
                "- **Tendinosis**: Chronic degeneration, no inflammation, eccentric exercise, load management\n\n"
                "**Ligament Injuries**:\n"
                "- **Grades**: 1 (stretch, minimal tearing), 2 (partial tear), 3 (complete tear)\n"
                "- **Treatment**:\n"
                "  - Grade 1-2: Conservative (RICE → physiotherapy)\n"
                "  - Grade 3: Consider surgical reconstruction (high-demand individuals)\n\n"
                "**Frozen Shoulder (Adhesive Capsulitis)**:\n"
                "- **Phases**: Freezing (pain, 2-9 months) → Frozen (stiff, 4-12 months) → Thawing (gradual recovery, 5-24 months)\n"
                "- **Risk factors**: Diabetes (20-30%), age 40-60, female\n"
                "- **Treatment**: Physiotherapy, steroid injection, hydrodilatation, manipulation under anesthesia\n\n"
                "**Other Conditions**:\n"
                "- **Trigger finger**: Catching, locking, painful click → steroid injection, surgery\n"
                "- **Carpal tunnel syndrome**: Median nerve compression → splinting, steroid injection, surgery\n"
                "- **Ganglion cyst**: Wrist/hand mass, aspiration, surgery if recurrent\n"
                "- **Dupuytren's contracture**: Palmar nodules, cord contracture → fasciectomy\n\n"
                "**Recovery Time**:\n"
                "- Mild (Grade 1): 1-3 weeks\n"
                "- Moderate (Grade 2): 3-6 weeks\n"
                "- Severe (Grade 3): 6-12 weeks (or longer if surgery)\n\n"
                "**Disclaimer**: Soft tissue injuries may benefit from physiotherapy referral."
            ),
            confidence=0.84,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "soft_tissue"
            }
        )

    def _handle_bone_health_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle bone health queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Bone Health & Osteoporosis - Orthopedic Second Opinion**\n\n"
                "**Osteoporosis**:\n"
                "- **Definition**: T-score ≤ -2.5 (bone mineral density by DXA)\n"
                "- **Osteopenia**: T-score -1.0 to -2.5\n"
                "- **Epidemiology**: 50% women, 20% men >50 will have osteoporosis-related fracture\n\n"
                "**Risk Assessment**:\n"
                "- **FRAX**: 10-year fracture risk assessment (age, sex, weight, fracture history, glucocorticoids, RA, secondary osteoporosis, parental hip fracture, smoking, alcohol, BMD)\n"
                "- **QFracture**: UK alternative\n\n"
                "**Screening Indications**:\n"
                "- Women ≥65, men ≥70\n"
                "- Postmenopausal women with risk factors\n"
                "- Adults with fragility fracture\n"
                "- Long-term glucocorticoids (≥3 months, prednisolone ≥5mg)\n"
                "- Early menopause, hypogonadism, RA, CKD\n\n"
                "**DXA Scanning**:\n"
                "- **Sites**: Lumbar spine (L1-L4), proximal femur\n"
                "- **T-score**: Compared to young adult (30yo)\n"
                "- **Z-score**: Compared to age-matched\n"
                "- **Frequency**: Every 2 years (or 1-2 years if on treatment)\n\n"
                "**Prevention**:\n"
                "- **Calcium**: 1000-1200 mg/day (diet + supplements)\n"
                "- **Vitamin D**: 800-1000 IU/day (to achieve level >30 ng/mL)\n"
                "- **Weight-bearing exercise**: 30 min, 3x/week\n"
                "- **Smoking cessation**, **alcohol moderation** (<2 drinks/day)\n"
                "- **Fall prevention**: Home safety, balance training, vision check, medication review\n\n"
                "**Pharmacological Treatment**:\n"
                "- **First-line**:\n"
                "  - **Oral bisphosphonates**: Alendronate 70mg weekly, risedronate 35mg weekly\n"
                "  - **IV bisphosphonates**: Zoledronic acid 5mg yearly (better adherence)\n"
                "- **Second-line**:\n"
                "  - **Denosumab**: 60mg SC every 6 months (RANKL inhibitor)\n"
                "  - **Teriparatide**: 20µg SC daily (anabolic, max 2 years, high risk)\n"
                "  - **Romosozumab**: 210mg SC monthly (anabolic then antiresorptive)\n"
                "- **Selective estrogen receptor modulators**: Raloxifene (postmenopausal women)\n\n"
                "**Treatment Duration**:\n"
                "- Bisphosphonates: 3-5 years (then drug holiday reassessment)\n"
                "- Denosumab: NO drug holiday (rebound fracture risk if stopped)\n\n"
                "**Monitoring**:\n"
                "- DXA every 1-2 years on treatment\n"
                "- Height, vertebral assessment\n"
                "- Calcium, vitamin D, renal function\n\n"
                "**Disclaimer**: Osteoporosis management individualized. Specialist referral for complex cases."
            ),
            confidence=0.86,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "bone_health",
                "sources": ["NICE Guidelines", "NOF Guidelines", "FRAX"]
            }
        )

    def _handle_surgery_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle surgery queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Orthopedic Surgery Consultation - Second Opinion**\n\n"
                "**Common Orthopedic Surgeries**:\n\n"
                "**Joint Replacement**:\n"
                "- **Total Hip Arthroplasty (THA)**:\n"
                "  - **Indications**: OA, AVN, rheumatoid arthritis, fracture\n"
                "  - **Approaches**: Posterior (most common), anterior, lateral\n"
                "  - **Implants**: Cemented (elderly), uncemented (younger), hybrid\n"
                "  - **Recovery**: 6 weeks basic, 6-12 weeks full, 80-90% excellent outcomes\n"
                "  - **Longevity**: 15-20 years (85-90% survival)\n\n"
                "- **Total Knee Arthroplasty (TKA)**:\n"
                "  - **Indications**: OA, rheumatoid arthritis\n"
                "  - **Implants**: Cruciate-retaining vs posterior-stabilized\n"
                "  - **Recovery**: More challenging than hip, 3-6 months basic, 6-12 months full\n"
                "  - **Outcomes**: 80-85% satisfaction\n\n"
                "**Arthroscopy**:\n"
                "- **Knee arthroscopy**: Meniscal tear (repair/partial menisectomy), loose body, chondroplasty\n"
                "- **Shoulder arthroscopy**: Rotator cuff repair, labral repair (SLAP, Bankart), subacromial decompression\n"
                "- **Advantages**: Minimally invasive, faster recovery\n"
                "- **Disadvantages**: Limited visualization, compartment syndrome risk\n\n"
                "**Fracture Fixation**:\n"
                "- **ORIF** (Open Reduction Internal Fixation): Plates, screws\n"
                "- **Intramedullary nailing**: Femur, tibia, humerus\n"
                "- **External fixation**: Open fractures, severe soft tissue injury, temporary stabilization\n"
                "- **Indications**: Displaced, unstable, articular fractures\n\n"
                "**Spine Surgery**:\n"
                "- **Discectomy**: Herniated disc with radiculopathy, failed conservative\n"
                "- **Decompression**: Spinal stenosis, laminectomy\n"
                "- **Fusion**: Spondylolisthesis, deformity, instability\n"
                "- **Approaches**: Anterior, posterior, lateral (XLIF, TLIF, PLIF)\n\n"
                "**Pre-operative Preparation**:\n"
                "- **Medical optimization**: Blood pressure, diabetes control, smoking cessation (4-6 weeks pre-op)\n"
                "- **Medication management**: Stop anticoagulants, NSAIDs 7 days prior\n"
                "- **Anesthesia assessment**: Cardiac clearance if indicated\n"
                "- **Patient education**: Expectations, rehabilitation, complications\n\n"
                "**Post-operative Care**:\n"
                "- **DVT prophylaxis**: LMWH, aspirin, mechanical compression\n"
                "- **Pain management**: Multimodal (regional anesthesia, NSAIDs, paracetamol, opioids)\n"
                "- **Rehabilitation**: Early mobilization, physiotherapy, home exercises\n"
                "- **Follow-up**: 2 weeks (wound check), 6 weeks, 3 months, 6 months, yearly\n\n"
                "**Complications**:\n"
                "- **Infection**: Superficial (1-2%), deep (<1%)\n"
                "- **DVT/PE**: 1-3% (with prophylaxis)\n"
                "- **Implant loosening**: 1%/year\n"
                "- **Nerve injury**: Rare (<1%)\n\n"
                "**Disclaimer**: Surgery decision individualized. Pre-op assessment essential."
            ),
            confidence=0.85,
            metadata={
                "specialty": "orthopedics",
                "subspecialty": "orthopedic_surgery"
            }
        )

    def _handle_general_orthopedics_query(self, query: str, context: Optional[Dict[str, Any]]) -> DomainQueryResult:
        """Handle general orthopedics queries."""
        return DomainQueryResult(
            domain_name="orthopedics",
            answer=(
                "**Orthopedics Consultation - Second Opinion**\n\n"
                "I specialize in musculoskeletal conditions and can provide consultation on:\n\n"
                "**Trauma & Fractures**:\n"
                "- Fracture assessment and management\n"
                "- Dislocations\n"
                "- Soft tissue injuries\n\n"
                "**Joint Disorders**:\n"
                "- Hip, knee, shoulder, elbow, ankle, foot\n"
                "- Osteoarthritis\n"
                "- Inflammatory arthritis\n\n"
                "**Spine**:\n"
                "- Low back pain\n"
                "- Sciatica\n"
                "- Spinal stenosis\n"
                "- Disc herniation\n\n"
                "**Sports Medicine**:\n"
                "- ACL, meniscus, rotator cuff injuries\n"
                "- Tendinopathies\n"
                "- Stress fractures\n"
                "- Return to sport\n\n"
                "**Bone Health**:\n"
                "- Osteoporosis\n"
                "- Fracture prevention\n"
                "- Calcium/vitamin D\n\n"
                "**Surgery**:\n"
                "- Joint replacement (hip, knee, shoulder)\n"
                "- Arthroscopy\n"
                "- Fracture fixation\n"
                "- Spine surgery\n\n"
                "**Please provide**: Location, symptoms, duration, functional limitation, "
                "injury mechanism, test results (X-ray, MRI), specific questions.\n\n"
                "**Privacy**: All data stored locally.\n"
                "**Medical Disclaimer**: This is second opinion. Urgent conditions require immediate care."
            ),
            confidence=0.85,
            metadata={
                "specialty": "orthopedics"
            }
        )


def create_orthopedics_domain():
    """Factory function for creating orthopedics domain instances."""
    return OrthopedicsDomain()
