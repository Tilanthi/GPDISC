#!/usr/bin/env python3
"""
Biology MORK Extensions for GPDISC
Extends MORK Ontology with biology-specific concepts and relationships

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# Import base MORK classes
try:
    from gpdisc_core.memory.mork_ontology import MORKOntology, OntologyNode, SemanticRelation, SemanticRelationType
except ImportError:
    # Fallback definitions if import fails
    class SemanticRelationType(Enum):
        IS_A = "is_a"
        HAS_PART = "has_part"
        CAUSES = "causes"
        PRECEDES = "precedes"
        INCOMPATIBLE = "incompatible"
        ANALOGOUS = "analogous"
        INSTANCE_OF = "instance_of"
        REGULATES = "regulates"
        INTERACTS_WITH = "interacts_with"
        PATHWAY_MEMBER = "pathway_member"

    @dataclass
    class OntologyNode:
        concept_id: str
        concept_name: str
        parent_id: Optional[str] = None
        children_ids: List[str] = field(default_factory=list)
        properties: Dict[str, Any] = field(default_factory=dict)
        domain_scope: List[str] = field(default_factory=lambda: ["ALL"])

        def __hash__(self):
            return hash(self.concept_id)


class BiologyMORKExtension:
    """
    Extension of MORK Ontology for biology-specific concepts

    Adds:
    - Molecular entities (DNA, RNA, proteins, metabolites)
    - Cellular structures (organelles, membranes)
    - Biological processes (transcription, translation, signaling)
    - Biological functions (enzyme catalysis, transport, regulation)
    - Disease states and phenotypes
    """

    # Biology-specific semantic relations
    BIOLOGY_RELATIONS = {
        'REGULATES': 'regulates',              # A regulates B (activation/inhibition)
        'INTERACTS_WITH': 'interacts_with',    # Molecular interaction
        'PATHWAY_MEMBER': 'pathway_member',    # Member of biological pathway
        'ENCODED_BY': 'encoded_by',            # Gene encodes protein
        'EXPRESSED_IN': 'expressed_in',        # Gene expressed in tissue
        'LOCALIZED_IN': 'localized_in',        # Protein localized to organelle
        'CATALYZES': 'catalyzes',              # Enzyme catalyzes reaction
        'BINDS': 'binds',                      # Binding interaction
        'PHOSPHORYLATES': 'phosphorylates',    # Phosphorylation
        'MUTATION_OF': 'mutation_of',          # Disease mutation
        'HOMOLOGOUS_TO': 'homologous_to',      # Evolutionary homology
    }

    def __init__(self, base_ontology: MORKOntology = None):
        """Initialize biology extensions"""
        self.base_ontology = base_ontology
        self.biology_nodes: Dict[str, OntologyNode] = {}
        self.biology_relations: List[SemanticRelation] = []

        self._build_biology_hierarchy()
        self._build_molecular_entities()
        self._build_cellular_components()
        self._build_biological_processes()
        self._build_biological_functions()
        self._build_disease_entities()
        self._build_biology_relations()

    def _add_node(self, node_id: str, name: str, parent_id: str = None,
                   properties: Dict = None, domain_scope: List[str] = None):
        """Add a biology node to the ontology"""
        if properties is None:
            properties = {}
        if domain_scope is None:
            domain_scope = ['biology']

        node = OntologyNode(
            concept_id=node_id,
            concept_name=name,
            parent_id=parent_id,
            properties=properties,
            domain_scope=domain_scope
        )
        self.biology_nodes[node_id] = node

        # Add to base ontology if available
        if self.base_ontology:
            self.base_ontology.nodes[node_id] = node

    def _add_relation(self, source: str, relation: str, target: str, strength: float = 1.0):
        """Add a semantic relation between biology concepts"""
        # Convert string relation to enum if it's a standard type
        if relation in [e.value for e in SemanticRelationType]:
            rel_type = SemanticRelationType(relation)
        else:
            # For biology-specific relations, store as custom
            rel_type = relation

        rel = SemanticRelation(
            source_id=source,
            relation_type=rel_type,
            target_id=target,
            strength=strength
        )
        self.biology_relations.append(rel)

        # Add to base ontology if available
        if self.base_ontology and isinstance(rel_type, SemanticRelationType):
            self.base_ontology.relations.append(rel)

    def _build_biology_hierarchy(self):
        """Build the top-level biology hierarchy"""
        self._add_node("BIOLOGY", "Biology", "ROOT", {
            "description": "All biological concepts and entities"
        })

        # Major biology domains
        self._add_node("MOLECULAR_BIOLOGY", "Molecular Biology", "BIOLOGY", {
            "description": "Study of biological molecules and their interactions"
        })
        self._add_node("CELL_BIOLOGY", "Cell Biology", "BIOLOGY", {
            "description": "Study of cell structure and function"
        })
        self._add_node("GENETICS", "Genetics", "BIOLOGY", {
            "description": "Study of genes and heredity"
        })
        self._add_node("BIOCHEMISTRY", "Biochemistry", "BIOLOGY", {
            "description": "Study of chemical processes in living organisms"
        })
        self._add_node("BIOPHYSICS", "Biophysics", "BIOLOGY", {
            "description": "Physical principles in biological systems"
        })
        self._add_node("SYSTEMS_BIOLOGY", "Systems Biology", "BIOLOGY", {
            "description": "Integration of biological systems"
        })

    def _build_molecular_entities(self):
        """Build molecular entity hierarchy"""
        # Nucleic acids
        self._add_node("NUCLEIC_ACID", "Nucleic Acid", "MOLECULAR_BIOLOGY", {
            "description": "DNA and RNA molecules"
        })
        self._add_node("DNA", "DNA", "NUCLEIC_ACID", {
            "description": "Deoxyribonucleic acid - genetic material",
            "structure": "double_helix",
            "components": ["A", "T", "G", "C"]
        })
        self._add_node("RNA", "RNA", "NUCLEIC_ACID", {
            "description": "Ribonucleic acid - various functional forms",
            "structure": "single_stranded",
            "components": ["A", "U", "G", "C"]
        })
        self._add_node("MRNA", "mRNA", "RNA", {
            "description": "Messenger RNA - protein coding template"
        })
        self._add_node("TRNA", "tRNA", "RNA", {
            "description": "Transfer RNA - amino acid carrier"
        })
        self._add_node("RRNA", "rRNA", "RNA", {
            "description": "Ribosomal RNA - structural component of ribosome"
        })

        # Proteins
        self._add_node("PROTEIN", "Protein", "MOLECULAR_BIOLOGY", {
            "description": "Polypeptide chains with biological function",
            "structure_levels": ["primary", "secondary", "tertiary", "quaternary"]
        })
        self._add_node("ENZYME", "Enzyme", "PROTEIN", {
            "description": "Catalytic protein",
            "function": "catalysis"
        })
        self._add_node("TRANSCRIPTION_FACTOR", "Transcription Factor", "PROTEIN", {
            "description": "Regulates gene expression",
            "function": "regulation"
        })
        self._add_node("MEMBRANE_PROTEIN", "Membrane Protein", "PROTEIN", {
            "description": "Protein associated with cell membrane",
            "location": "membrane"
        })
        self._add_node("RECEPTOR", "Receptor", "MEMBRANE_PROTEIN", {
            "description": "Receives and transmits signals",
            "function": "signal_transduction"
        })

        # Metabolites
        self._add_node("METABOLITE", "Metabolite", "BIOCHEMISTRY", {
            "description": "Small molecule involved in metabolism"
        })
        self._add_node("CARBOHYDRATE", "Carbohydrate", "METABOLITE", {
            "description": "Sugar molecules for energy and structure"
        })
        self._add_node("LIPID", "Lipid", "METABOLITE", {
            "description": "Hydrophobic molecules for membranes and energy"
        })
        self._add_node("AMINO_ACID", "Amino Acid", "METABOLITE", {
            "description": "Building blocks of proteins"
        })

    def _build_cellular_components(self):
        """Build cellular component hierarchy"""
        # Cell
        self._add_node("CELL", "Cell", "CELL_BIOLOGY", {
            "description": "Fundamental unit of life"
        })
        self._add_node("PROKARYOTE", "Prokaryotic Cell", "CELL", {
            "description": "Cell without nucleus",
            "examples": ["bacteria", "archaea"]
        })
        self._add_node("EUKARYOTE", "Eukaryotic Cell", "CELL", {
            "description": "Cell with nucleus and organelles",
            "examples": ["animal", "plant", "fungi", "protist"]
        })

        # Organelles
        self._add_node("ORGANELLE", "Organelle", "CELL_BIOLOGY", {
            "description": "Specialized structure within cell"
        })
        self._add_node("NUCLEUS", "Nucleus", "ORGANELLE", {
            "description": "Contains genetic material",
            "location": "eukaryotic_cell"
        })
        self._add_node("MITOCHONDRION", "Mitochondrion", "ORGANELLE", {
            "description": "Powerhouse of the cell - ATP production",
            "function": "energy_production"
        })
        self._add_node("RIBOSOME", "Ribosome", "ORGANELLE", {
            "description": "Protein synthesis machinery",
            "function": "translation"
        })
        self._add_node("ENDOPLASMIC_RETICULUM", "Endoplasmic Reticulum", "ORGANELLE", {
            "description": "Protein and lipid synthesis",
            "function": "synthesis"
        })
        self._add_node("GOLGI_APPARATUS", "Golgi Apparatus", "ORGANELLE", {
            "description": "Protein processing and sorting",
            "function": "processing"
        })
        self._add_node("LYSOSOME", "Lysosome", "ORGANELLE", {
            "description": "Digestive compartment",
            "function": "degradation"
        })
        self._add_node("CHLOROPLAST", "Chloroplast", "ORGANELLE", {
            "description": "Photosynthesis in plants",
            "function": "photosynthesis",
            "location": "plant_cell"
        })

        # Membranes
        self._add_node("MEMBRANE", "Membrane", "CELL_BIOLOGY", {
            "description": "Phospholipid bilayer boundary"
        })
        self._add_node("PLASMA_MEMBRANE", "Plasma Membrane", "MEMBRANE", {
            "description": "Outer boundary of cell"
        })
        self._add_node("NUCLEAR_MEMBRANE", "Nuclear Membrane", "MEMBRANE", {
            "description": "Boundary of nucleus"
        })

    def _build_biological_processes(self):
        """Build biological process hierarchy"""
        self._add_node("BIOLOGICAL_PROCESS", "Biological Process", "BIOLOGY", {
            "description": "Processes performed by living systems"
        })

        # Central dogma processes
        self._add_node("DNA_REPLICATION", "DNA Replication", "BIOLOGICAL_PROCESS", {
            "description": "Copy DNA before cell division",
            "input": "DNA",
            "output": "DNA"
        })
        self._add_node("TRANSCRIPTION", "Transcription", "BIOLOGICAL_PROCESS", {
            "description": "Synthesize RNA from DNA template",
            "input": "DNA",
            "output": "RNA"
        })
        self._add_node("TRANSLATION", "Translation", "BIOLOGICAL_PROCESS", {
            "description": "Synthesize protein from mRNA template",
            "input": "mRNA",
            "output": "Protein"
        })

        # Gene regulation
        self._add_node("GENE_REGULATION", "Gene Regulation", "BIOLOGICAL_PROCESS", {
            "description": "Control of gene expression"
        })
        self._add_node("TRANSCRIPTIONAL_REGULATION", "Transcriptional Regulation", "GENE_REGULATION", {
            "description": "Control of transcription rate"
        })
        self._add_node("POST_TRANSCRIPTIONAL_REGULATION", "Post-transcriptional Regulation", "GENE_REGULATION", {
            "description": "Control after transcription"
        })
        self._add_node("TRANSLATIONAL_REGULATION", "Translational Regulation", "GENE_REGULATION", {
            "description": "Control of translation rate"
        })
        self._add_node("POST_TRANSLATIONAL_REGULATION", "Post-translational Regulation", "GENE_REGULATION", {
            "description": "Control after translation"
        })

        # Cell processes
        self._add_node("CELL_DIVISION", "Cell Division", "BIOLOGICAL_PROCESS", {
            "description": "Process of cell reproduction"
        })
        self._add_node("MITOSIS", "Mitosis", "CELL_DIVISION", {
            "description": "Division of somatic cells"
        })
        self._add_node("MEIOSIS", "Meiosis", "CELL_DIVISION", {
            "description": "Division for gamete production"
        })
        self._add_node("APOPTOSIS", "Apoptosis", "BIOLOGICAL_PROCESS", {
            "description": "Programmed cell death"
        })

        # Metabolism
        self._add_node("METABOLISM", "Metabolism", "BIOLOGICAL_PROCESS", {
            "description": "Chemical reactions in organism"
        })
        self._add_node("CATABOLISM", "Catabolism", "METABOLISM", {
            "description": "Breakdown of molecules for energy"
        })
        self._add_node("ANABOLISM", "Anabolism", "METABOLISM", {
            "description": "Synthesis of molecules"
        })

        # Signaling
        self._add_node("SIGNAL_TRANSDUCTION", "Signal Transduction", "BIOLOGICAL_PROCESS", {
            "description": "Transmission of molecular signals"
        })
        self._add_node("RECEPTOR_SIGNALING", "Receptor Signaling", "SIGNAL_TRANSDUCTION", {
            "description": "Signaling through receptors"
        })
        self._add_node("INTRACELLULAR_SIGNALING", "Intracellular Signaling", "SIGNAL_TRANSDUCTION", {
            "description": "Signaling within cell"
        })

    def _build_biological_functions(self):
        """Build biological function hierarchy"""
        self._add_node("BIOLOGICAL_FUNCTION", "Biological Function", "BIOLOGY", {
            "description": "Functions performed by biological entities"
        })

        self._add_node("CATALYSIS", "Catalysis", "BIOLOGICAL_FUNCTION", {
            "description": "Acceleration of chemical reactions",
            "performed_by": "Enzyme"
        })
        self._add_node("TRANSPORT", "Transport", "BIOLOGICAL_FUNCTION", {
            "description": "Movement of molecules",
            "performed_by": ["Membrane Protein", "Channel"]
        })
        self._add_node("STORAGE", "Storage", "BIOLOGICAL_FUNCTION", {
            "description": "Storage of information or molecules"
        })
        self._add_node("STRUCTURAL_SUPPORT", "Structural Support", "BIOLOGICAL_FUNCTION", {
            "description": "Physical structure provision"
        })
        self._add_node("RECOGNITION", "Recognition", "BIOLOGICAL_FUNCTION", {
            "description": "Molecular recognition",
            "performed_by": ["Antibody", "Receptor"]
        })
        self._add_node("REGULATION", "Regulation", "BIOLOGICAL_FUNCTION", {
            "description": "Control of biological processes"
        })

    def _build_disease_entities(self):
        """Build disease and phenotype entities"""
        self._add_node("DISEASE", "Disease", "BIOLOGY", {
            "description": "Pathological condition"
        })
        self._add_node("GENETIC_DISEASE", "Genetic Disease", "DISEASE", {
            "description": "Disease caused by genetic mutations"
        })
        self._add_node("INFECTIOUS_DISEASE", "Infectious Disease", "DISEASE", {
            "description": "Disease caused by pathogens"
        })
        self._add_node("CANCER", "Cancer", "DISEASE", {
            "description": "Uncontrolled cell growth",
            "mechanism": "mutations_in_cell_cycle_regulation"
        })
        self._add_node("METABOLIC_DISEASE", "Metabolic Disease", "DISEASE", {
            "description": "Disorder of metabolism"
        })
        self._add_node("NEUROLOGICAL_DISEASE", "Neurological Disease", "DISEASE", {
            "description": "Disorder of nervous system"
        })

        # Phenotypes
        self._add_node("PHENOTYPE", "Phenotype", "BIOLOGY", {
            "description": "Observable characteristics"
        })
        self._add_node("GENOTYPE", "Genotype", "BIOLOGY", {
            "description": "Genetic constitution"
        })
        self._add_node("MUTATION", "Mutation", "GENETICS", {
            "description": "Change in DNA sequence"
        })
        self._add_node("SNP", "Single Nucleotide Polymorphism", "MUTATION", {
            "description": "Single base pair variation"
        })
        self._add_node("INDEL", "Insertion/Deletion", "MUTATION", {
            "description": "Insertion or deletion of bases"
        })

    def _build_biology_relations(self):
        """Build semantic relations between biology concepts"""
        # Molecular entity relationships
        self._add_relation("DNA", "PRECEDES", "RNA", 1.0)
        self._add_relation("RNA", "PRECEDES", "PROTEIN", 1.0)
        self._add_relation("ENZYME", "IS_A", "PROTEIN", 1.0)
        self._add_relation("RECEPTOR", "IS_A", "PROTEIN", 1.0)
        self._add_relation("TRANSCRIPTION_FACTOR", "IS_A", "PROTEIN", 1.0)

        # Process relationships
        self._add_relation("DNA_REPLICATION", "CAUSES", "DNA", 1.0)
        self._add_relation("TRANSCRIPTION", "CAUSES", "RNA", 1.0)
        self._add_relation("TRANSLATION", "CAUSES", "PROTEIN", 1.0)
        self._add_relation("TRANSCRIPTION", "PRECEDES", "TRANSLATION", 1.0)

        # Cellular component relationships
        self._add_relation("EUKARYOTE", "HAS_PART", "NUCLEUS", 1.0)
        self._add_relation("EUKARYOTE", "HAS_PART", "MITOCHONDRION", 1.0)
        self._add_relation("EUKARYOTE", "HAS_PART", "RIBOSOME", 1.0)
        self._add_relation("PROKARYOTE", "INCOMPATIBLE", "EUKARYOTE", 1.0)

        # Disease relationships
        self._add_relation("MUTATION", "CAUSES", "GENETIC_DISEASE", 0.8)
        self._add_relation("CANCER", "IS_A", "DISEASE", 1.0)
        self._add_relation("GENETIC_DISEASE", "CAUSES", "PHENOTYPE", 0.9)

    def get_biology_concepts(self, domain: str = None) -> List[str]:
        """Get all biology concepts, optionally filtered by domain"""
        if domain:
            return [node_id for node_id, node in self.biology_nodes.items()
                    if domain in node.domain_scope]
        return list(self.biology_nodes.keys())

    def get_concept_info(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a concept"""
        if concept_id in self.biology_nodes:
            node = self.biology_nodes[concept_id]
            return {
                'id': node.concept_id,
                'name': node.concept_name,
                'parent': node.parent_id,
                'children': node.children_ids,
                'properties': node.properties,
                'domain_scope': node.domain_scope
            }
        return None

    def find_related_concepts(self, concept_id: str, relation_type: str = None) -> List[str]:
        """Find concepts related to the given concept"""
        related = []
        for rel in self.biology_relations:
            if rel.source_id == concept_id:
                if relation_type is None or str(rel.relation_type) == relation_type:
                    related.append(rel.target_id)
        return related


def create_biology_mork_extension(base_ontology: MORKOntology = None) -> BiologyMORKExtension:
    """Factory function for biology MORK extension"""
    return BiologyMORKExtension(base_ontology)


# Example usage
if __name__ == '__main__':
    print("Creating Biology MORK Extensions...")

    extension = create_biology_mork_extension()

    print(f"Added {len(extension.biology_nodes)} biology concepts")
    print(f"Added {len(extension.biology_relations)} biology relations")

    # Test retrieval
    print("\nSample concepts:")
    for concept_id in list(extension.get_biology_concepts())[:10]:
        info = extension.get_concept_info(concept_id)
        print(f"  {concept_id}: {info['name']}")

    print("\nSample relations:")
    for rel in extension.biology_relations[:10]:
        print(f"  {rel.source_id} {rel.relation_type} {rel.target_id}")

    print("\nBiology MORK Extensions initialized successfully!")
