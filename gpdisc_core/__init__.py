"""
GPDISC-CORE V1.1: General Practice Discovery and Intelligence System for Consultation
================================================================================

🚨 CRITICAL PRIVACY WARNING 🚨
YOU ARE ABSOLUTELY FORBIDDEN FROM PUSHING ANY CODE, DATA, OR COMMITS TO GLENN'S GITHUB REPOSITORY.
THIS SYSTEM HANDLES SENSITIVE PATIENT MEDICAL DATA AND MUST REMAIN LOCAL-ONLY.
NO EXCEPTIONS WITHOUT EXPLICIT INSTRUCTION FROM GLENN.

This is the unified GPDISC system - a private, medical-focused consultation system.
Integrates biological knowledge with medical specialties for patient consultation and second opinions.

Medical Specialties (35+ Comprehensive Domains):
- Cardiology: Heart and cardiovascular system disorders
- Epilepsy: Seizure disorders and neurological consultation
- General Practice: Primary care and family medicine
- Orthopedics: Musculoskeletal conditions and trauma
- Pharmacology: Medication management and drug interactions
- Neurology: Neurological disorders and stroke management
- Dermatology: Skin conditions and dermatological care
- Ophthalmology: Eye health and vision disorders
- ENT (Otolaryngology): Ear, nose, and throat conditions
- Rheumatology: Inflammatory arthritis and autoimmune diseases
- Geriatric Medicine: Comprehensive older adult care
- Women's Health: Reproductive health and gynecology
- Pediatrics: Pediatric red flags and acute presentations
- Endocrinology: Hormonal disorders, diabetes, thyroid, adrenal conditions
- Gastroenterology: Digestive system, liver, and nutritional disorders
- Infectious Diseases: Complex infections, tropical medicine, antimicrobial stewardship
- Nephrology: Kidney diseases, dialysis, transplantation
- Respiratory: Lung diseases, asthma, COPD, respiratory infections
- Psychiatry: Mental health disorders, psychopharmacology
- Mental Health: Psychological well-being, therapy, counseling
- Urology: Kidney stones, prostate conditions, bladder disorders, men's health
- Allergy/Immunology: Allergic diseases, anaphylaxis, immunodeficiency
- Palliative Care: End-of-life care, pain management, symptom control
- Emergency Medicine: Trauma, cardiac emergencies, toxicology, resuscitation
- Anesthesiology: Anaesthesia techniques, airway management, critical care
- General Surgery: Abdominal surgery, trauma, endoscopy, surgical assessment
- Vascular Surgery: Arterial and venous disease, aneurysms, carotid disease
- Cardiothoracic Surgery: Cardiac surgery, thoracic surgery, lung resection
- Neurosurgery: Brain surgery, spine surgery, peripheral nerve surgery
- Plastic Surgery: Reconstructive surgery, hand surgery, burns management
- Radiology: Medical imaging, X-ray, CT, MRI, ultrasound, interventional radiology
- Pathology: Lab medicine, biochemistry, haematology, microbiology, histopathology
- Radiation Oncology: Radiotherapy planning, cancer treatment, radiation side effects
- Physical Medicine & Rehabilitation: Stroke, musculoskeletal, neurological, cardiac, pulmonary rehab
- Occupational Medicine: Work-related health, occupational diseases, workplace hazards
- Medical Genetics: Genetic counseling, inherited disorders, prenatal testing, cancer genetics

Biological Knowledge (Preserved):
- Molecular Biology, Biochemistry, Genetics, Cell Biology
- Biophysics, Bioinformatics, Computational Biology
- Genomics, Proteomics, Systems Biology

Core Capabilities:
- Advanced reasoning and causal inference
- Memory systems for patient records (local, private storage)
- Multi-domain medical consultation
- Second opinion generation with uncertainty quantification

Privacy Commitment:
- All patient records stored locally (no external LLM transmission)
- Long-term memory for blood tests, ECGs, MRIs, doctor's notes
- Private medical consultation mode

Directory Structure:
-------------------
gpdisc_core/
    core/           - Unified system architecture
    domains/        - Medical and biological domain modules
    memory/         - Local memory systems for patient records
    capabilities/   - Advanced reasoning capabilities
    causal/         - Causal reasoning and inference
    dashboard/      - Medical consultation dashboard (port 8790)
    tests/          - Integration and validation tests

Version: 1.0.0 (Medical Consultation System)
Date: May 3, 2026
"""

__version__ = "1.1.0"

# =============================================================================
# UNIFIED SYSTEM - All Capabilities Integrated (V36-V94 + V4)
# =============================================================================
try:
    from .core.unified import (
        UnifiedGPDISCSystem, UnifiedConfig, TaskType, TaskAnalyzer
    )
except ImportError:
    UnifiedGPDISCSystem = None
    UnifiedConfig = None
    TaskType = None
    TaskAnalyzer = None

# =============================================================================
# V4 Causal Reasoning Components
# =============================================================================
try:
    from .causal.model.scm import StructuralCausalModel, Variable, StructuralEquation
    from .causal.discovery.pc_algorithm import PCAlgorithm
    from .causal.discovery.temporal_discovery import TemporalCausalDiscovery
    from .causal.model.intervention import Intervention
    from .causal.model.counterfactual import CounterfactualQuery
except ImportError:
    StructuralCausalModel = None
    Variable = None
    StructuralEquation = None
    PCAlgorithm = None
    TemporalCausalDiscovery = None
    Intervention = None
    CounterfactualQuery = None

# =============================================================================
# V47+ Enhanced Causal Discovery
# =============================================================================
try:
    from .causal.discovery.bayesian_structure_learning import (
        InferenceMethod,
        DAGPosteriorSample,
        BayesianStructureLearningResult,
        BayesianStructureLearner,
        create_bayesian_structure_learner,
    )
except ImportError:
    InferenceMethod = None
    DAGPosteriorSample = None
    BayesianStructureLearningResult = None
    BayesianStructureLearner = None
    create_bayesian_structure_learner = None

try:
    from .causal.discovery.eig_calculator import (
        NoiseModel,
        ObservationPlan,
        EIGResult,
        LatentConfounderModel,
        ExpectedInformationGainCalculator,
        create_eig_calculator,
    )
except ImportError:
    NoiseModel = None
    ObservationPlan = None
    EIGResult = None
    LatentConfounderModel = None
    ExpectedInformationGainCalculator = None
    create_eig_calculator = None

try:
    from .causal.discovery.online_causal_learning import (
        UpdateMethod,
        ConceptDriftDetector,
        OnlineLearningResult,
        OnlineCausalLearner,
        create_online_causal_learner,
    )
except ImportError:
    UpdateMethod = None
    ConceptDriftDetector = None
    OnlineLearningResult = None
    OnlineCausalLearner = None
    create_online_causal_learner = None

try:
    from .causal.inference import (
        SBIMethod,
        SBIResult,
        SimulatorInterface,
        SimulationBasedInferenceEngine,
        create_sbi_engine,
        default_summary_statistics,
    )
except ImportError:
    SBIMethod = None
    SBIResult = None
    SimulatorInterface = None
    SimulationBasedInferenceEngine = None
    create_sbi_engine = None
    default_summary_statistics = None

# =============================================================================
# Memory Systems (Merged from both gpdisc_core and astra_core_v4)
# =============================================================================
try:
    from .memory import (
        # MORK Ontology (from gpdisc_core)
        MORKOntology, OntologyNode, SemanticRelation, SemanticRelationType,
        ExpandedMORK, MORKConcept, ScientificDomain,
        # Memory Graph (from gpdisc_core)
        MemoryGraph, GraphNode, GraphEdge, NodeType, EdgeType,
        # Vector Store (from gpdisc_core)
        MilvusVectorStore, VectorBackend, DistanceMetric, InMemoryVectorIndex,
        # RRF Fusion (from gpdisc_core)
        ThreeWayRRF, RRFResult,
    )
except ImportError:
    MORKOntology = None
# =============================================================================
# PHASE 2-4 ENHANCEMENTS: Domain Expansion, Physics Integration, Validation
# =============================================================================
# These represent the enhanced capabilities added to address RASTI paper limitations

# -----------------------------------------------------------------------------
# Domain System (Phase 2): Modular domain architecture for specialized astronomy
# -----------------------------------------------------------------------------
try:
    from .domains import (
        # Base domain module interface
        BaseDomainModule,
        DomainConfig,
        DomainQueryResult,
        CrossDomainConnection,
        DomainModuleRegistry,
        register_domain,
    )
    from .domains.registry import DomainRegistry as DomainsRegistry
except ImportError:
    BaseDomainModule = None
    DomainConfig = None
    DomainQueryResult = None
    CrossDomainConnection = None
    DomainModuleRegistry = None
    register_domain = None
    DomainsRegistry = None

# Available domain modules (Biology-focused)
try:
    from .domains.molecular_biology import MolecularBiologyDomain
    from .domains.biochemistry import BiochemistryDomain
    from .domains.genetics import GeneticsDomain
    from .domains.cell_biology import CellBiologyDomain
    from .domains.biophysics import BiophysicsDomain
    from .domains.bioinformatics import BioinformaticsDomain
    from .domains.computational_biology import ComputationalBiologyDomain
    from .domains.genomics import GenomicsDomain
    from .domains.proteomics import ProteomicsDomain
    from .domains.systems_biology import SystemsBiologyDomain
except ImportError:
    MolecularBiologyDomain = None
    BiochemistryDomain = None
    GeneticsDomain = None
    CellBiologyDomain = None
    BiophysicsDomain = None
    BioinformaticsDomain = None
    ComputationalBiologyDomain = None
    GenomicsDomain = None
    ProteomicsDomain = None
    SystemsBiologyDomain = None

# Medical domains (NEW for GPDISC) - Phase 1: High Priority Specialties
try:
    from .domains.cardiology import CardiologyDomain
    from .domains.epilepsy import EpilepsyDomain
    from .domains.general_practice import GeneralPracticeDomain
    from .domains.orthopedics import OrthopedicsDomain
    from .domains.pharmacology import PharmacologyDomain
    from .domains.neurology import NeurologyDomain
except ImportError:
    CardiologyDomain = None
    EpilepsyDomain = None
    GeneralPracticeDomain = None
    OrthopedicsDomain = None
    PharmacologyDomain = None
    NeurologyDomain = None

# Medical domains - Phase 2: Medium Priority Specialties
try:
    from .domains.dermatology import DermatologyDomain
    from .domains.ophthalmology import OphthalmologyDomain
    from .domains.ent import ENTDomain
    from .domains.rheumatology import RheumatologyDomain
except ImportError:
    DermatologyDomain = None
    OphthalmologyDomain = None
    ENTDomain = None
    RheumatologyDomain = None

# Medical domains - Phase 3: Special Populations
try:
    from .domains.geriatric_medicine import GeriatricMedicineDomain
    from .domains.womens_health import WomensHealthDomain
    from .domains.pediatrics import PediatricsDomain
except ImportError:
    GeriatricMedicineDomain = None
    WomensHealthDomain = None
    PediatricsDomain = None

# Medical domains - Phase 4: Additional Medical Specialties
try:
    from .domains.endocrinology import EndocrinologyDomain
    from .domains.gastroenterology import GastroenterologyDomain
    from .domains.infectious_diseases import InfectiousDiseasesDomain
    from .domains.nephrology import NephrologyDomain
    from .domains.respiratory import RespiratoryDomain
    from .domains.psychiatry import PsychiatryDomain
    from .domains.mental_health import MentalHealthDomain
except ImportError:
    EndocrinologyDomain = None
    GastroenterologyDomain = None
    InfectiousDiseasesDomain = None
    NephrologyDomain = None
    RespiratoryDomain = None
    PsychiatryDomain = None
    MentalHealthDomain = None

# Medical domains - Phase 5: Additional Medical Specialties
try:
    from .domains.urology import UrologyDomain
    from .domains.allergy_immunology import AllergyImmunologyDomain
    from .domains.palliative_care import PalliativeCareDomain
    from .domains.emergency_medicine import EmergencyMedicineDomain
    from .domains.anesthesiology import AnesthesiologyDomain
except ImportError:
    UrologyDomain = None
    AllergyImmunologyDomain = None
    PalliativeCareDomain = None
    EmergencyMedicineDomain = None
    AnesthesiologyDomain = None

# Medical domains - Phase 6: Surgical Specialties
try:
    from .domains.general_surgery import GeneralSurgeryDomain
    from .domains.vascular_surgery import VascularSurgeryDomain
    from .domains.cardiothoracic_surgery import CardiothoracicSurgeryDomain
    from .domains.neurosurgery import NeurosurgeryDomain
    from .domains.plastic_surgery import PlasticSurgeryDomain
except ImportError:
    GeneralSurgeryDomain = None
    VascularSurgeryDomain = None
    CardiothoracicSurgeryDomain = None
    NeurosurgeryDomain = None
    PlasticSurgeryDomain = None

# Medical domains - Phase 7: Other Specialties
try:
    from .domains.radiology import RadiologyDomain
    from .domains.pathology import PathologyDomain
    from .domains.radiation_oncology import RadiationOncologyDomain
    from .domains.physical_medicine_rehab import PhysicalMedicineRehabDomain
    from .domains.occupational_medicine import OccupationalMedicineDomain
    from .domains.medical_genetics import MedicalGeneticsDomain
except ImportError:
    RadiologyDomain = None
    PathologyDomain = None
    RadiationOncologyDomain = None
    PhysicalMedicineRehabDomain = None
    OccupationalMedicineDomain = None
    MedicalGeneticsDomain = None

# -----------------------------------------------------------------------------
# Cross-Domain Meta-Learning (Phase 2): Rapid domain adaptation
# -----------------------------------------------------------------------------
try:
    from .reasoning.cross_domain_meta_learner import (
        CrossDomainMetaLearner,
        DomainSimilarity,
        DomainFeatures,
        AdaptationResult,
    )
except ImportError:
    CrossDomainMetaLearner = None
    DomainSimilarity = None
    DomainFeatures = None
    AdaptationResult = None

# -----------------------------------------------------------------------------
# Unified Physics Engine (Phase 3): Differentiable physics with constraints
# -----------------------------------------------------------------------------
try:
    from .physics import (
        # Main physics engine
        UnifiedPhysicsEngine,
        PhysicsDomain,
        PhysicsResult,
        PhysicsConstraint,
        # Physics intuition development
        PhysicsCurriculum,
        PhysicalAnalogicalReasoner,
        # Learning and reasoning
        ComplexityLevel,
        LearningStage,
        PhysicalAnalogy,
        Phenomenon,
    )
except ImportError:
    UnifiedPhysicsEngine = None
    PhysicsDomain = None
    PhysicsResult = None
    PhysicsConstraint = None
    PhysicsCurriculum = None
    PhysicalAnalogicalReasoner = None
    ComplexityLevel = None
    LearningStage = None
    PhysicalAnalogy = None
    Phenomenon = None

# -----------------------------------------------------------------------------
# Enhanced Unified System (Phase 4): Integration of all enhancements
# -----------------------------------------------------------------------------
try:
    from .core.unified_enhanced import (
        EnhancedUnifiedGPDISCSystem,
        EnhancedUnifiedConfig,
        create_gpdisc_system,
    )
except ImportError:
    EnhancedUnifiedGPDISCSystem = None
    EnhancedUnifiedConfig = None
    create_gpdisc_system = None

# -----------------------------------------------------------------------------
# Validation Framework (Phase 4): Benchmarking and testing
# -----------------------------------------------------------------------------
try:
    from .tests.validation_benchmarks import (
        ValidationSuite,
        BenchmarkResult,
        create_validation_suite,
        run_validation_suite,
    )
except ImportError:
    ValidationSuite = None
    BenchmarkResult = None
    create_validation_suite = None
    run_validation_suite = None

# Export aliases for backwards compatibility
create_enhanced_stan_system = create_gpdisc_system  # Deprecated
create_stan_system = create_gpdisc_system  # Deprecated but maintained for compatibility

# =============================================================================
# PDF Generator (Publication-Ready Paper Generation)
# =============================================================================
try:
    from .utils.pdf_generator import (
        PDFGenerator,
        PDFFormat,
        TextAlign,
        PDFSection,
        PDFTable,
        PDFCodeBlock,
        generate_stan_paper_with_figures,
        create_publication_pdf_from_markdown,
        REPORTLAB_AVAILABLE,
        FPDF_AVAILABLE,
    )
except ImportError:
    PDFGenerator = None
    PDFFormat = None
    TextAlign = None
    PDFSection = None
    PDFTable = None
    PDFCodeBlock = None
    generate_stan_paper_with_figures = None
    create_publication_pdf_from_markdown = None
    REPORTLAB_AVAILABLE = False
    FPDF_AVAILABLE = False

# =============================================================================
# V6.0 Theoretical Discovery System (NEW)
# =============================================================================
# Major enhancement: Theoretical discovery capabilities beyond empirical analysis
try:
    from .theoretical_discovery import (
        # Main theoretical discovery system
        V6TheoreticalDiscovery,
        create_v6_theoretical_system,
        DiscoveryMode,
        DiscoveryResult,
        TheoreticalProblem,
        # Component modules
        SymbolicTheoreticEngine,
        TheorySpaceMapper,
        TheoryRefutationEngine,
        LiteratureTheorySynthesizer,
        ComputationalTheoreticalBridge,
        # Supporting classes
        PhysicsDomain,
        PhysicalConstraint,
        ScalingRelation,
        TheoryFramework,
        TheoryConnection,
        TheoryType,
        TheoryRelation,
        Equation,
        TheoreticalInsight,
        InsightType,
        SimulationDesign,
        SimulationResult,
        SimulationInsight,
        InsightCategory,
        ConstraintViolation,
        Severity,
    )
except ImportError:
    V6TheoreticalDiscovery = None
    create_v6_theoretical_system = None
    DiscoveryMode = None
    DiscoveryResult = None
    TheoreticalProblem = None
    SymbolicTheoreticEngine = None
    TheorySpaceMapper = None
    TheoryRefutationEngine = None
    LiteratureTheorySynthesizer = None
    ComputationalTheoreticalBridge = None
    PhysicsDomain = None
    PhysicalConstraint = None
    ScalingRelation = None
    TheoryFramework = None
    TheoryConnection = None
    TheoryType = None
    TheoryRelation = None
    Equation = None
    TheoreticalInsight = None
    InsightType = None
    SimulationDesign = None
    SimulationResult = None
    SimulationInsight = None
    InsightCategory = None
    ConstraintViolation = None
    Severity = None

# =============================================================================
# V7.0 Autonomous Research Scientist (NEW)
# =============================================================================
# Transformative enhancement: Full autonomous research cycle capability
try:
    from .autonomous_research import (
        # Main autonomous scientist system
        V7AutonomousScientist,
        create_v7_scientist,
        ResearchCycle,
        ResearchQuestion,
        Hypothesis,
        Experiment,
        ResearchResult,
        Publication,
        # Engines
        QuestionGenerator,
        QuestionType,
        QuestionImportance,
        HypothesisFormulator,
        HypothesisType as V7HypothesisType,
        HypothesisStatus,
        ExperimentDesigner,
        ExperimentType,
        DesignParameters,
        ExperimentExecutor,
        ExecutionResult as V7ExecutionResult,
        DataSource,
        PredictionEngine,
        PredictionType,
        PredictionConfidence,
        AnalysisEngine,
        AnalysisType,
        CausalInferenceResult,
        TheoryRevisionEngine,
        RevisionType,
        TheoryStatus,
        PublicationEngine,
        PaperStructure,
        FigureType,
    )
except ImportError:
    V7AutonomousScientist = None
    create_v7_scientist = None
    ResearchCycle = None
    ResearchQuestion = None
    Hypothesis = None
    Experiment = None
    ResearchResult = None
    Publication = None
    QuestionGenerator = None
    QuestionType = None
    QuestionImportance = None
    HypothesisFormulator = None
    V7HypothesisType = None
    HypothesisStatus = None
    ExperimentDesigner = None
    ExperimentType = None
    DesignParameters = None
    ExperimentExecutor = None
    V7ExecutionResult = None
    DataSource = None
    PredictionEngine = None
    PredictionType = None
    PredictionConfidence = None
    AnalysisEngine = None
    AnalysisType = None
    CausalInferenceResult = None
    TheoryRevisionEngine = None
    RevisionType = None
    TheoryStatus = None
    PublicationEngine = None
    PaperStructure = None
    FigureType = None

# =============================================================================
# V8.0 Enhanced Architecture (NEW) - Claude-inspired Orchestration
# =============================================================================
# Advanced medical consultation architecture with:
# - Multi-layer safety validation
# - Tool coordination and standardization
# - Memory integration with semantic search
# - Specialty coordination and conflict resolution
try:
    from .orchestration import (
        MedicalOrchestrationHarness,
        MedicalTaskDecomposer,
        ToolCoordinator as OrchestratorToolCoordinator,
        ConsultationResult,
        SubTask,
        MedicalContextManager,
        ConsultationContext,
        PatientSession,
    )
except ImportError:
    MedicalOrchestrationHarness = None
    MedicalTaskDecomposer = None
    OrchestratorToolCoordinator = None
    ConsultationResult = None
    SubTask = None
    MedicalContextManager = None
    ConsultationContext = None
    PatientSession = None

try:
    from .safety import (
        MedicalSafetyLayers,
        EmergencyDetector,
        FactualConsistencyChecker,
        ClinicalAppropriatenessChecker,
        SafetyValidation,
        SafetyCheckResult,
        SafetyCheck,
    )
except ImportError:
    MedicalSafetyLayers = None
    EmergencyDetector = None
    FactualConsistencyChecker = None
    ClinicalAppropriatenessChecker = None
    SafetyValidation = None
    SafetyCheckResult = None
    SafetyCheck = None

try:
    from .confidence import (
        ConfidenceCalibrator,
        UncertaintyQuantification,
    )
except ImportError:
    ConfidenceCalibrator = None
    UncertaintyQuantification = None

try:
    from .tools import (
        MedicalTool,
        ToolResult,
        ECGInterpreterTool,
        DrugInteractionCheckerTool,
        DiagnosticReasoningTool,
        LaboratoryInterpreterTool,
        ToolRegistry,
        ToolCoordinator,
        create_standard_tool_registry,
        create_standard_tool_coordinator,
    )
except ImportError:
    MedicalTool = None
    ToolResult = None
    ECGInterpreterTool = None
    DrugInteractionCheckerTool = None
    DiagnosticReasoningTool = None
    LaboratoryInterpreterTool = None
    ToolRegistry = None
    ToolCoordinator = None
    create_standard_tool_registry = None
    create_standard_tool_coordinator = None

try:
    from .coordination import (
        SpecialtyCoordinator,
        ConflictDetector,
        ConflictResolver,
        SecondOpinionGenerator,
        SpecialtyOpinion,
        OpinionConflict,
        CoordinatedResult,
        ConflictSeverity,
    )
except ImportError:
    SpecialtyCoordinator = None
    ConflictDetector = None
    ConflictResolver = None
    SecondOpinionGenerator = None
    SpecialtyOpinion = None
    OpinionConflict = None
    CoordinatedResult = None
    ConflictSeverity = None

try:
    from .memory.enhanced_retrieval import (
        SemanticMemoryRetriever,
        ContextAwareRetriever,
        MemoryItem,
    )
except ImportError:
    SemanticMemoryRetriever = None
    ContextAwareRetriever = None
    MemoryItem = None

try:
    from .core.enhanced_system_factory import (
        create_enhanced_gpdisc_system,
        create_gpdisc_with_coordination,
        create_gpdisc_minimal,
    )
except ImportError:
    create_enhanced_gpdisc_system = None
    create_gpdisc_with_coordination = None
    create_gpdisc_minimal = None
