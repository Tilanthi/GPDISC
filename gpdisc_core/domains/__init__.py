"""
Base domain module interface for GPDISC

Provides abstract base class and configuration for all domain modules.
Enables plug-and-play domain expansion with hot-swapping capabilities.

Includes 10 preserved biology domains and 30+ comprehensive medical specialties.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


@dataclass
class DomainConfig:
    """
    Configuration for domain modules

    Attributes:
        domain_name: Unique identifier for the domain
        version: Domain module version
        dependencies: List of other domains this domain depends on
        keywords: Keywords for automatic domain detection
        task_types: Task types this domain can handle
        enabled: Whether the domain is enabled
        description: Human-readable description
        capabilities: List of specific capabilities provided
    """
    domain_name: str
    version: str
    dependencies: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    task_types: List[str] = field(default_factory=list)
    enabled: bool = True
    description: str = ""
    capabilities: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate configuration"""
        if not self.domain_name:
            raise ValueError("domain_name cannot be empty")
        if not self.version:
            raise ValueError("version cannot be empty")


@dataclass
class DomainQueryResult:
    """
    Result from domain query processing

    Attributes:
        domain_name: Name of domain that processed the query
        answer: Generated answer
        confidence: Confidence in the answer (0-1)
        reasoning_trace: List of reasoning steps
        capabilities_used: Capabilities used in processing
        metadata: Additional metadata
    """
    domain_name: str
    answer: str
    confidence: float
    reasoning_trace: List[str] = field(default_factory=list)
    capabilities_used: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate result"""
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    def __getitem__(self, key: str) -> Any:
        """Support dict-style access for backward compatibility"""
        return getattr(self, key, self.metadata.get(key))

    def get(self, key: str, default: Any = None) -> Any:
        """Get method for dict-like compatibility"""
        return getattr(self, key, self.metadata.get(key, default))


@dataclass
class CrossDomainConnection:
    """
    Represents a connection between two domains

    Attributes:
        source_domain: Source domain name
        target_domain: Target domain name
        connection_type: Type of connection (analogy, shared_concept, etc.)
        strength: Strength of connection (0-1)
        description: Description of the connection
        transferable_knowledge: Knowledge that can be transferred
    """
    source_domain: str
    target_domain: str
    connection_type: str
    strength: float
    description: str = ""
    transferable_knowledge: List[str] = field(default_factory=list)


class BaseDomainModule(ABC):
    """
    Abstract base class for all domain modules

    Provides standard interface for domain hot-swapping and orchestration.
    """

    def __init__(self, config: DomainConfig = None):
        self.config = config or self.get_default_config()
        self.domain_name = self.config.domain_name
        self._initialized = False

    @abstractmethod
    def get_default_config(self) -> DomainConfig:
        """Return default configuration for this domain"""
        pass

    @abstractmethod
    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process a query using this domain's expertise

        Args:
            query: The query to process
            context: Additional context for processing

        Returns:
            DomainQueryResult with answer and metadata
        """
        pass

    def initialize(self, global_config: Dict[str, Any] = None):
        """
        Initialize the domain with global configuration

        Called once when domain is first loaded.
        """
        if not self._initialized:
            self._initialized = True

    def get_capabilities(self) -> List[str]:
        """Return list of capabilities provided by this domain"""
        return self.config.capabilities

    def get_dependencies(self) -> List[str]:
        """Return list of domain dependencies"""
        return self.config.dependencies

    def get_config(self) -> DomainConfig:
        """Return the domain's configuration"""
        return self.config

    def can_handle(self, query: str) -> bool:
        """
        Check if this domain can handle the given query

        Uses keyword matching for simple detection.
        """
        query_lower = query.lower()
        return any(keyword.lower() in query_lower for keyword in self.config.keywords)


class DomainModuleRegistry:
    """
    Registry for all domain modules

    Provides hot-swapping capability and domain lookup.
    """

    def __init__(self):
        self._domains: Dict[str, BaseDomainModule] = {}
        self._domain_configs: Dict[str, DomainConfig] = {}

    def register(self, domain: BaseDomainModule):
        """Register a domain module"""
        self._domains[domain.domain_name] = domain
        self._domain_configs[domain.domain_name] = domain.config
        logger.info(f"Registered domain: {domain.domain_name}")

    def unregister(self, domain_name: str):
        """Unregister a domain module"""
        if domain_name in self._domains:
            del self._domains[domain_name]
            del self._domain_configs[domain_name]
            logger.info(f"Unregistered domain: {domain_name}")

    def get_domain(self, domain_name: str) -> Optional[BaseDomainModule]:
        """Get a domain by name"""
        return self._domains.get(domain_name)

    def list_domains(self) -> List[str]:
        """List all registered domain names"""
        return list(self._domains.keys())

    def find_domains_for_query(self, query: str) -> List[str]:
        """Find domains that can handle the given query"""
        return [name for name, domain in self._domains.items() if domain.can_handle(query)]


# Global registry instance
_domain_registry = DomainModuleRegistry()


def register_domain(domain: BaseDomainModule):
    """Register a domain in the global registry"""
    _domain_registry.register(domain)


def get_domain_registry() -> DomainModuleRegistry:
    """Get the global domain registry"""
    return _domain_registry


# Domain decorator for automatic registration
def domain(cls):
    """Decorator to automatically register a domain class"""
    class WrappedDomain(cls):
        def __new__(subclass, *args, **kwargs):
            instance = super().__new__(subclass)
            return instance

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            register_domain(self)

    return WrappedDomain


# Import DomainRegistry from registry module
from .registry import DomainRegistry

# Import GPDISC Biology Domain Modules
try:
    from .molecular_biology import MolecularBiologyDomain, create_molecular_biology_domain
except ImportError:
    MolecularBiologyDomain = None
    create_molecular_biology_domain = None

try:
    from .biochemistry import BiochemistryDomain, create_biochemistry_domain
except ImportError:
    BiochemistryDomain = None
    create_biochemistry_domain = None

try:
    from .genetics import GeneticsDomain, create_genetics_domain
except ImportError:
    GeneticsDomain = None
    create_genetics_domain = None

try:
    from .cell_biology import CellBiologyDomain, create_cell_biology_domain
except ImportError:
    CellBiologyDomain = None
    create_cell_biology_domain = None

try:
    from .biophysics import BiophysicsDomain, create_biophysics_domain
except ImportError:
    BiophysicsDomain = None
    create_biophysics_domain = None

try:
    from .bioinformatics import BioinformaticsDomain, create_bioinformatics_domain
except ImportError:
    BioinformaticsDomain = None
    create_bioinformatics_domain = None

try:
    from .computational_biology import ComputationalBiologyDomain, create_computational_biology_domain
except ImportError:
    ComputationalBiologyDomain = None
    create_computational_biology_domain = None

try:
    from .genomics import GenomicsDomain, create_genomics_domain
except ImportError:
    GenomicsDomain = None
    create_genomics_domain = None

try:
    from .proteomics import ProteomicsDomain, create_proteomics_domain
except ImportError:
    ProteomicsDomain = None
    create_proteomics_domain = None

try:
    from .systems_biology import SystemsBiologyDomain, create_systems_biology_domain
except ImportError:
    SystemsBiologyDomain = None
    create_systems_biology_domain = None


# GPDISC Medical Domain Modules (35+ Comprehensive Medical Specialties)

# Phase 1: High Priority Specialties
try:
    from .cardiology import CardiologyDomain, create_cardiology_domain
except ImportError:
    CardiologyDomain = None
    create_cardiology_domain = None

try:
    from .epilepsy import EpilepsyDomain, create_epilepsy_domain
except ImportError:
    EpilepsyDomain = None
    create_epilepsy_domain = None

try:
    from .general_practice import GeneralPracticeDomain, create_general_practice_domain
except ImportError:
    GeneralPracticeDomain = None
    create_general_practice_domain = None

try:
    from .orthopedics import OrthopedicsDomain, create_orthopedics_domain
except ImportError:
    OrthopedicsDomain = None
    create_orthopedics_domain = None

try:
    from .pharmacology import PharmacologyDomain, create_pharmacology_domain
except ImportError:
    PharmacologyDomain = None
    create_pharmacology_domain = None

try:
    from .neurology import NeurologyDomain, create_neurology_domain
except ImportError:
    NeurologyDomain = None
    create_neurology_domain = None

# Phase 2: Medium Priority Specialties
try:
    from .dermatology import DermatologyDomain, create_dermatology_domain
except ImportError:
    DermatologyDomain = None
    create_dermatology_domain = None

try:
    from .ophthalmology import OphthalmologyDomain, create_ophthalmology_domain
except ImportError:
    OphthalmologyDomain = None
    create_ophthalmology_domain = None

try:
    from .ent import ENTDomain, create_ent_domain
except ImportError:
    ENTDomain = None
    create_ent_domain = None

try:
    from .rheumatology import RheumatologyDomain, create_rheumatology_domain
except ImportError:
    RheumatologyDomain = None
    create_rheumatology_domain = None

# Phase 3: Special Populations
try:
    from .geriatric_medicine import GeriatricMedicineDomain, create_geriatric_medicine_domain
except ImportError:
    GeriatricMedicineDomain = None
    create_geriatric_medicine_domain = None

try:
    from .womens_health import WomensHealthDomain, create_womens_health_domain
except ImportError:
    WomensHealthDomain = None
    create_womens_health_domain = None

try:
    from .pediatrics import PediatricsDomain, create_pediatrics_domain
except ImportError:
    PediatricsDomain = None
    create_pediatrics_domain = None

# Phase 4: Additional Medical Specialties
try:
    from .endocrinology import EndocrinologyDomain, create_endocrinology_domain
except ImportError:
    EndocrinologyDomain = None
    create_endocrinology_domain = None

try:
    from .gastroenterology import GastroenterologyDomain, create_gastroenterology_domain
except ImportError:
    GastroenterologyDomain = None
    create_gastroenterology_domain = None

try:
    from .infectious_diseases import InfectiousDiseasesDomain, create_infectious_diseases_domain
except ImportError:
    InfectiousDiseasesDomain = None
    create_infectious_diseases_domain = None

try:
    from .nephrology import NephrologyDomain, create_nephrology_domain
except ImportError:
    NephrologyDomain = None
    create_nephrology_domain = None

try:
    from .respiratory import RespiratoryDomain, create_respiratory_domain
except ImportError:
    RespiratoryDomain = None
    create_respiratory_domain = None

try:
    from .psychiatry import PsychiatryDomain, create_psychiatry_domain
except ImportError:
    PsychiatryDomain = None
    create_psychiatry_domain = None

try:
    from .mental_health import MentalHealthDomain, create_mental_health_domain
except ImportError:
    MentalHealthDomain = None
    create_mental_health_domain = None

# Phase 5: Additional Medical Specialties
try:
    from .urology import UrologyDomain, create_urology_domain
except ImportError:
    UrologyDomain = None
    create_urology_domain = None

try:
    from .allergy_immunology import AllergyImmunologyDomain, create_allergy_immunology_domain
except ImportError:
    AllergyImmunologyDomain = None
    create_allergy_immunology_domain = None

try:
    from .palliative_care import PalliativeCareDomain, create_palliative_care_domain
except ImportError:
    PalliativeCareDomain = None
    create_palliative_care_domain = None

try:
    from .emergency_medicine import EmergencyMedicineDomain, create_emergency_medicine_domain
except ImportError:
    EmergencyMedicineDomain = None
    create_emergency_medicine_domain = None

try:
    from .anesthesiology import AnesthesiologyDomain, create_anesthesiology_domain
except ImportError:
    AnesthesiologyDomain = None
    create_anesthesiology_domain = None

# Phase 6: Surgical Specialties
try:
    from .general_surgery import GeneralSurgeryDomain, create_general_surgery_domain
except ImportError:
    GeneralSurgeryDomain = None
    create_general_surgery_domain = None

try:
    from .vascular_surgery import VascularSurgeryDomain, create_vascular_surgery_domain
except ImportError:
    VascularSurgeryDomain = None
    create_vascular_surgery_domain = None

try:
    from .cardiothoracic_surgery import CardiothoracicSurgeryDomain, create_cardiothoracic_surgery_domain
except ImportError:
    CardiothoracicSurgeryDomain = None
    create_cardiothoracic_surgery_domain = None

try:
    from .neurosurgery import NeurosurgeryDomain, create_neurosurgery_domain
except ImportError:
    NeurosurgeryDomain = None
    create_neurosurgery_domain = None

try:
    from .plastic_surgery import PlasticSurgeryDomain, create_plastic_surgery_domain
except ImportError:
    PlasticSurgeryDomain = None
    create_plastic_surgery_domain = None

# Phase 7: Other Specialties
try:
    from .radiology import RadiologyDomain, create_radiology_domain
except ImportError:
    RadiologyDomain = None
    create_radiology_domain = None

try:
    from .pathology import PathologyDomain, create_pathology_domain
except ImportError:
    PathologyDomain = None
    create_pathology_domain = None

try:
    from .radiation_oncology import RadiationOncologyDomain, create_radiation_oncology_domain
except ImportError:
    RadiationOncologyDomain = None
    create_radiation_oncology_domain = None

try:
    from .physical_medicine_rehab import PhysicalMedicineRehabDomain, create_physical_medicine_rehab_domain
except ImportError:
    PhysicalMedicineRehabDomain = None
    create_physical_medicine_rehab_domain = None

try:
    from .occupational_medicine import OccupationalMedicineDomain, create_occupational_medicine_domain
except ImportError:
    OccupationalMedicineDomain = None
    create_occupational_medicine_domain = None

try:
    from .medical_genetics import MedicalGeneticsDomain, create_medical_genetics_domain
except ImportError:
    MedicalGeneticsDomain = None
    create_medical_genetics_domain = None


# Export all public classes
__all__ = [
    'DomainConfig',
    'DomainQueryResult',
    'CrossDomainConnection',
    'BaseDomainModule',
    'DomainModuleRegistry',
    'DomainRegistry',
    'register_domain',
    # GPDISC Biology Domains (10 domains)
    'MolecularBiologyDomain',
    'create_molecular_biology_domain',
    'BiochemistryDomain',
    'create_biochemistry_domain',
    'GeneticsDomain',
    'create_genetics_domain',
    'CellBiologyDomain',
    'create_cell_biology_domain',
    'BiophysicsDomain',
    'create_biophysics_domain',
    'BioinformaticsDomain',
    'create_bioinformatics_domain',
    'ComputationalBiologyDomain',
    'create_computational_biology_domain',
    'GenomicsDomain',
    'create_genomics_domain',
    'ProteomicsDomain',
    'create_proteomics_domain',
    'SystemsBiologyDomain',
    'create_systems_biology_domain',
    # GPDISC Medical Domains (30+ comprehensive medical specialties)
    # Phase 1: High Priority Specialties
    'CardiologyDomain',
    'create_cardiology_domain',
    'EpilepsyDomain',
    'create_epilepsy_domain',
    'GeneralPracticeDomain',
    'create_general_practice_domain',
    'OrthopedicsDomain',
    'create_orthopedics_domain',
    'PharmacologyDomain',
    'create_pharmacology_domain',
    'NeurologyDomain',
    'create_neurology_domain',
    # Phase 2: Medium Priority Specialties
    'DermatologyDomain',
    'create_dermatology_domain',
    'OphthalmologyDomain',
    'create_ophthalmology_domain',
    'ENTDomain',
    'create_ent_domain',
    'RheumatologyDomain',
    'create_rheumatology_domain',
    # Phase 3: Special Populations
    'GeriatricMedicineDomain',
    'create_geriatric_medicine_domain',
    'WomensHealthDomain',
    'create_womens_health_domain',
    'PediatricsDomain',
    'create_pediatrics_domain',
    # Phase 4: Additional Medical Specialties
    'EndocrinologyDomain',
    'create_endocrinology_domain',
    'GastroenterologyDomain',
    'create_gastroenterology_domain',
    'InfectiousDiseasesDomain',
    'create_infectious_diseases_domain',
    'NephrologyDomain',
    'create_nephrology_domain',
    'RespiratoryDomain',
    'create_respiratory_domain',
    'PsychiatryDomain',
    'create_psychiatry_domain',
    'MentalHealthDomain',
    'create_mental_health_domain',
    # Phase 5: Additional Medical Specialties
    'UrologyDomain',
    'create_urology_domain',
    'AllergyImmunologyDomain',
    'create_allergy_immunology_domain',
    'PalliativeCareDomain',
    'create_palliative_care_domain',
    'EmergencyMedicineDomain',
    'create_emergency_medicine_domain',
    'AnesthesiologyDomain',
    'create_anesthesiology_domain',
    # Phase 6: Surgical Specialties
    'GeneralSurgeryDomain',
    'create_general_surgery_domain',
    'VascularSurgeryDomain',
    'create_vascular_surgery_domain',
    'CardiothoracicSurgeryDomain',
    'create_cardiothoracic_surgery_domain',
    'NeurosurgeryDomain',
    'create_neurosurgery_domain',
    'PlasticSurgeryDomain',
    'create_plastic_surgery_domain',
    # Phase 7: Other Specialties
    'RadiologyDomain',
    'create_radiology_domain',
    'PathologyDomain',
    'create_pathology_domain',
    'RadiationOncologyDomain',
    'create_radiation_oncology_domain',
    'PhysicalMedicineRehabDomain',
    'create_physical_medicine_rehab_domain',
    'OccupationalMedicineDomain',
    'create_occupational_medicine_domain',
    'MedicalGeneticsDomain',
    'create_medical_genetics_domain',
]
