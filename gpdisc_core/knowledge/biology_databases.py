#!/usr/bin/env python3
"""
Biology Database Connectors for GPDISC
Connects to major biological databases for knowledge retrieval
"""

import requests
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    """Types of biological databases"""
    UNIPROT = "uniprot"           # Protein sequences and annotations
    PDB = "pdb"                   # Protein 3D structures
    ENSEMBL = "ensembl"           # Genome databases
    KEGG = "kegg"                 # Pathway databases
    NCBI = "ncbi"                 # National Center for Biotechnology Information
    BIOGRID = "biogrid"           # Protein/genetic interactions
    GO = "gene_ontology"          # Gene Ontology
    REACTOME = "reactome"         # Pathway database


@dataclass
class DatabaseResult:
    """Result from database query"""
    database: DatabaseType
    success: bool
    data: Any
    error: Optional[str] = None
    query_time: float = 0.0


class UniProtConnector:
    """Connector for UniProt database (protein sequences and annotations)"""

    BASE_URL = "https://rest.uniprot.org"

    def get_protein_info(self, protein_id: str) -> DatabaseResult:
        """Get protein information by UniProt ID"""
        url = f"{self.BASE_URL}/uniprotkb/{protein_id}.json"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            protein_info = {
                'id': data.get('primaryAccession', ''),
                'name': data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', ''),
                'gene': data.get('genes', [{}])[0].get('geneName', {}).get('value', '') if data.get('genes') else '',
                'organism': data.get('organism', {}).get('scientificName', ''),
                'sequence': data.get('sequence', {}).get('value', ''),
                'length': data.get('sequence', {}).get('length', 0),
                'function': data.get('comments', [{}])[0].get('texts', [{}])[0].get('value', '')[:200] if data.get('comments') else '',
                'keywords': [kw.get('name') for kw in data.get('keywords', [])]
            }

            return DatabaseResult(
                database=DatabaseType.UNIPROT,
                success=True,
                data=protein_info
            )

        except Exception as e:
            logger.error(f"UniProt query error: {e}")
            return DatabaseResult(
                database=DatabaseType.UNIPROT,
                success=False,
                data=None,
                error=str(e)
            )

    def search_proteins(self, query: str, organism: str = "human", limit: int = 10) -> DatabaseResult:
        """Search proteins by name/description"""
        url = f"{self.BASE_URL}/uniprotkb/search"
        params = {
            'query': f"{query} AND organism_id:{9606 if organism == 'human' else organism}",
            'format': 'json',
            'size': limit
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            results = []
            for result in data.get('results', []):
                results.append({
                    'id': result.get('primaryAccession', ''),
                    'name': result.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', ''),
                    'gene': result.get('genes', [{}])[0].get('geneName', {}).get('value', '') if result.get('genes') else '',
                    'organism': result.get('organism', {}).get('scientificName', '')
                })

            return DatabaseResult(
                database=DatabaseType.UNIPROT,
                success=True,
                data=results
            )

        except Exception as e:
            logger.error(f"UniProt search error: {e}")
            return DatabaseResult(
                database=DatabaseType.UNIPROT,
                success=False,
                data=None,
                error=str(e)
            )


class PDBConnector:
    """Connector for Protein Data Bank (3D structures)"""

    BASE_URL = "https://data.rcsb.org/rest/v1"

    def get_structure_info(self, pdb_id: str) -> DatabaseResult:
        """Get protein structure information by PDB ID"""
        url = f"{self.BASE_URL}/core/entry/{pdb_id.upper()}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Get polymer entity information
            entity_url = f"{self.BASE_URL}/core/polymer_entity/{pdb_id.upper()}/1"
            entity_response = requests.get(entity_url, timeout=30)
            entity_data = entity_response.json() if entity_response.status_code == 200 else {}

            structure_info = {
                'id': pdb_id.upper(),
                'title': data.get('struct', {}).get('title', ''),
                'experimental_method': data.get('exptl', [{}])[0].get('method', '') if data.get('exptl') else '',
                'resolution': data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0],
                'deposition_date': data.get('rcsb_accession_info', {}).get('deposit_date', ''),
                'entity_count': data.get('rcsb_entry_info', {}).get('polymer_entity_count', 0),
                'chains': [e.get('pdbx_description', '') for e in entity_data.get('entity_poly', {}).get('pdbx_description', '').split(',') if e] if isinstance(entity_data.get('entity_poly', {}).get('pdbx_description', ''), str) else []
            }

            return DatabaseResult(
                database=DatabaseType.PDB,
                success=True,
                data=structure_info
            )

        except Exception as e:
            logger.error(f"PDB query error: {e}")
            return DatabaseResult(
                database=DatabaseType.PDB,
                success=False,
                data=None,
                error=str(e)
            )


class EnsemblConnector:
    """Connector for Ensembl genome database"""

    BASE_URL = "https://rest.ensembl.org"

    def get_gene_info(self, gene_id: str, species: str = "homo_sapiens") -> DatabaseResult:
        """Get gene information from Ensembl"""
        url = f"{self.BASE_URL}/lookup/id/{gene_id}"

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=30, params={'species': species})
            response.raise_for_status()
            data = response.json()

            gene_info = {
                'id': data.get('id', ''),
                'name': data.get('display_name', ''),
                'biotype': data.get('biotype', ''),
                'description': data.get('description', ''),
                'chromosome': data.get('seq_region_name', ''),
                'start': data.get('start', 0),
                'end': data.get('end', 0),
                'strand': data.get('strand', 0)
            }

            return DatabaseResult(
                database=DatabaseType.ENSEMBL,
                success=True,
                data=gene_info
            )

        except Exception as e:
            logger.error(f"Ensembl query error: {e}")
            return DatabaseResult(
                database=DatabaseType.ENSEMBL,
                success=False,
                data=None,
                error=str(e)
            )

    def get_gene_sequence(self, gene_id: str, species: str = "homo_sapiens") -> DatabaseResult:
        """Get gene sequence from Ensembl"""
        url = f"{self.BASE_URL}/sequence/id/{gene_id}"

        headers = {"Content-Type": "text/plain"}

        try:
            response = requests.get(url, headers=headers, timeout=30, params={'type': 'genomic', 'species': species})
            response.raise_for_status()

            return DatabaseResult(
                database=DatabaseType.ENSEMBL,
                success=True,
                data={'id': gene_id, 'sequence': response.text}
            )

        except Exception as e:
            logger.error(f"Ensembl sequence error: {e}")
            return DatabaseResult(
                database=DatabaseType.ENSEMBL,
                success=False,
                data=None,
                error=str(e)
            )


class KEGGConnector:
    """Connector for KEGG pathway database"""

    BASE_URL = "https://rest.kegg.jp"

    def get_pathway_info(self, pathway_id: str) -> DatabaseResult:
        """Get pathway information from KEGG"""
        url = f"{self.BASE_URL}/get/{pathway_id}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Parse KEGG format
            lines = response.text.split('\n')
            pathway_info = {
                'id': pathway_id,
                'name': '',
                'description': '',
                'genes': []
            }

            for line in lines:
                if line.startswith('NAME'):
                    pathway_info['name'] = line.replace('NAME', '').strip()
                elif line.startswith('DESCRIPTION'):
                    pathway_info['description'] = line.replace('DESCRIPTION', '').strip()
                elif line.startswith('GENE'):
                    gene_info = line.replace('GENE', '').strip().split(';')
                    if gene_info:
                        pathway_info['genes'].append(gene_info[0].strip())

            return DatabaseResult(
                database=DatabaseType.KEGG,
                success=True,
                data=pathway_info
            )

        except Exception as e:
            logger.error(f"KEGG query error: {e}")
            return DatabaseResult(
                database=DatabaseType.KEGG,
                success=False,
                data=None,
                error=str(e)
            )


class GeneOntologyConnector:
    """Connector for Gene Ontology database"""

    BASE_URL = "https://go.owlfab.org"

    def get_term_info(self, go_id: str) -> DatabaseResult:
        """Get Gene Ontology term information"""
        url = f"{self.BASE_URL}/api/ontology/{go_id}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            term_info = {
                'id': go_id,
                'name': data.get('name', ''),
                'namespace': data.get('namespace', ''),
                'definition': data.get('def', ''),
                'is_obsolete': data.get('is_obsolete', False)
            }

            return DatabaseResult(
                database=DatabaseType.GO,
                success=True,
                data=term_info
            )

        except Exception as e:
            logger.error(f"GO query error: {e}")
            return DatabaseResult(
                database=DatabaseType.GO,
                success=False,
                data=None,
                error=str(e)
            )


class BiologyDatabaseManager:
    """Manager for all biology database connections"""

    def __init__(self):
        """Initialize all connectors"""
        self.uniprot = UniProtConnector()
        self.pdb = PDBConnector()
        self.ensembl = EnsemblConnector()
        self.kegg = KEGGConnector()
        self.go = GeneOntologyConnector()

        self.connectors = {
            DatabaseType.UNIPROT: self.uniprot,
            DatabaseType.PDB: self.pdb,
            DatabaseType.ENSEMBL: self.ensembl,
            DatabaseType.KEGG: self.kegg,
            DatabaseType.GO: self.go
        }

    def query_database(self, db_type: DatabaseType, query: str, **kwargs) -> DatabaseResult:
        """Query a specific database"""
        connector = self.connectors.get(db_type)

        if db_type == DatabaseType.UNIPROT:
            if 'search' in kwargs and kwargs['search']:
                return connector.search_proteins(query, kwargs.get('organism', 'human'))
            return connector.get_protein_info(query)

        elif db_type == DatabaseType.PDB:
            return connector.get_structure_info(query)

        elif db_type == DatabaseType.ENSEMBL:
            if 'sequence' in kwargs and kwargs['sequence']:
                return connector.get_gene_sequence(query, kwargs.get('species', 'homo_sapiens'))
            return connector.get_gene_info(query, kwargs.get('species', 'homo_sapiens'))

        elif db_type == DatabaseType.KEGG:
            return connector.get_pathway_info(query)

        elif db_type == DatabaseType.GO:
            return connector.get_term_info(query)

        return DatabaseResult(
            database=db_type,
            success=False,
            data=None,
            error=f"Unknown database type: {db_type}"
        )

    def get_comprehensive_protein_info(self, protein_id: str) -> Dict[str, Any]:
        """Get comprehensive protein information from multiple sources"""
        info = {
            'uniprot_id': protein_id,
            'uniprot': None,
            'pdb_structures': [],
            'ensembl_gene': None
        }

        # Get UniProt info
        uniprot_result = self.query_database(DatabaseType.UNIPROT, protein_id)
        if uniprot_result.success:
            info['uniprot'] = uniprot_result.data

            # Try to find PDB structures if available
            if info['uniprot'] and 'name' in info['uniprot']:
                # Could search for structures here
                pass

        return info


def create_biology_db_manager() -> BiologyDatabaseManager:
    """Factory function for biology database manager"""
    return BiologyDatabaseManager()


# Example usage
if __name__ == '__main__':
    manager = create_biology_db_manager()

    # Test UniProt
    print("Testing UniProt...")
    result = manager.query_database(DatabaseType.UNIPROT, "P53_HUMAN")
    if result.success:
        print(f"Protein: {result.data.get('name')}")
        print(f"Gene: {result.data.get('gene')}")

    # Test PDB
    print("\nTesting PDB...")
    result = manager.query_database(DatabaseType.PDB, "1CRN")
    if result.success:
        print(f"Structure: {result.data.get('title')}")
        print(f"Method: {result.data.get('experimental_method')}")

    print("\nBiology database connectors initialized successfully!")
