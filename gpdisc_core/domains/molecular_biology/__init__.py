"""Molecular Biology Domain Module for GPDISC

DNA replication, transcription, translation, gene expression

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Import domain base
from .. import BaseDomainModule, DomainConfig, DomainQueryResult


class MolecularBiologyDomain(BaseDomainModule):
    """
    Domain specializing in Molecular Biology

    Capabilities:
    - dna_replication: DNA synthesis and replication mechanisms
    - transcription: RNA synthesis from DNA templates
    - translation: Protein synthesis from mRNA
    - gene_expression: Regulation of gene expression
    - molecular_techniques: PCR, sequencing, cloning
    """

    def get_default_config(self) -> DomainConfig:
        """Return default configuration for Molecular Biology domain"""
        return DomainConfig(
            domain_name="molecular_biology",
            version="1.0.0",
            dependencies=[],
            description="DNA replication, transcription, translation, gene expression",
            keywords=[
                "dna", "rna", "transcription", "translation",
                "gene expression", "replication", "protein synthesis",
                "molecular biology", "genetics", "genome", "polymerase"
            ],
            capabilities=[
                "dna_replication", "transcription", "translation",
                "gene_expression", "molecular_techniques"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process molecular biology queries

        Args:
            query: User query about molecular biology
            context: Additional context

        Returns:
            DomainQueryResult with analysis and insights
        """
        try:
            if context is None:
                context = {}

            query_lower = query.lower()

            # Route to appropriate handler
            if any(term in query_lower for term in ["replication", "dna synthesis", "polymerase"]):
                return self._handle_replication_query(query, context)
            elif any(term in query_lower for term in ["transcription", "rna synthesis", "rna polymerase"]):
                return self._handle_transcription_query(query, context)
            elif any(term in query_lower for term in ["translation", "protein synthesis", "ribosome"]):
                return self._handle_translation_query(query, context)
            elif any(term in query_lower for term in ["gene expression", "regulation", "promoter"]):
                return self._handle_expression_query(query, context)
            else:
                return self._handle_general_query(query, context)

        except Exception as e:
            logger.error(f"Error processing molecular biology query: {e}")
            return DomainQueryResult(
                domain_name="molecular_biology",
                answer=f"Error processing molecular biology query: {str(e)}",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e)}
            )

    def _handle_replication_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle DNA replication queries"""
        return DomainQueryResult(
            domain_name="molecular_biology",
            answer=f"DNA replication is the biological process of producing two identical replicas of DNA from one original DNA molecule.",
            confidence=0.9,
            metadata={"topic": "replication", "sources": ["DNA replication mechanisms", "Molecular biology textbooks"]}
        )

    def _handle_transcription_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle transcription queries"""
        return DomainQueryResult(
            domain_name="molecular_biology",
            answer=f"Transcription is the process of copying a segment of DNA into RNA, catalyzed by RNA polymerase.",
            confidence=0.9,
            metadata={"topic": "transcription", "sources": ["Molecular biology of the cell", "Gene regulation resources"]}
        )

    def _handle_translation_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle translation queries"""
        return DomainQueryResult(
            domain_name="molecular_biology",
            answer=f"Translation is the process by which ribosomes synthesize proteins using mRNA as a template.",
            confidence=0.9,
            metadata={"topic": "translation", "sources": ["Protein synthesis mechanisms", "Ribosome structure and function"]}
        )

    def _handle_expression_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle gene expression queries"""
        return DomainQueryResult(
            domain_name="molecular_biology",
            answer=f"Gene expression is the process by which information from a gene is used in the synthesis of a functional gene product.",
            confidence=0.85,
            metadata={"topic": "expression", "sources": ["Gene regulation databases", "Expression analysis resources"]}
        )

    def _handle_general_query(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general molecular biology queries"""
        return DomainQueryResult(
            domain_name="molecular_biology",
            answer=f"Molecular biology covers the study of biological activity at the molecular level, particularly DNA, RNA, and protein synthesis.",
            confidence=0.75,
            metadata={"topic": "general", "sources": ["Molecular biology textbooks", "Biochemistry resources"]}
        )


def create_molecular_biology_domain():
    """Factory function for Molecular Biology domain"""
    return MolecularBiologyDomain()


__all__ = ['MolecularBiologyDomain', 'create_molecular_biology_domain']
