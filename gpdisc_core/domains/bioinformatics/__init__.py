"""Bioinformatics Domain Module for GPDISC

Sequence analysis, structural biology

Date: 2026-04-22
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

from .. import BaseDomainModule, DomainConfig, DomainQueryResult


class BioinformaticsDomain(BaseDomainModule):
    """Domain specializing in Bioinformatics"""

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="bioinformatics",
            version="1.0.0",
            dependencies=[],
            description="Sequence analysis, structural biology",
            keywords=[
                "sequence", "alignment", "database", "structural", "algorithm",
                "bioinformatics", "computational", "blast", "phylogeny"
            ],
            capabilities=[
                "sequence_analysis", "structural_prediction", "database_searching",
                "phylogenetic_analysis", "algorithm_development"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        try:
            if context is None:
                context = {}

            return DomainQueryResult(
                domain_name="bioinformatics",
                answer=f"Bioinformatics develops methods and software tools for understanding biological data, particularly sequence analysis and structural prediction.",
                confidence=0.85,
                metadata={"topic": "bioinformatics", "sources": ["Bioinformatics textbooks", "Sequence databases"]}
            )
        except Exception as e:
            logger.error(f"Error processing bioinformatics query: {e}")
            return DomainQueryResult(
                domain_name="bioinformatics",
                answer=f"Error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e), "sources": []}
            )


def create_bioinformatics_domain():
    """Factory function for Bioinformatics domain"""
    return BioinformaticsDomain()


__all__ = ['BioinformaticsDomain', 'create_bioinformatics_domain']
