"""
Agentic Retrieval Module for STAN
==================================

Implements advanced parallel retrieval patterns from "Building the 14 Key Pillars of Agentic AI":

Priority 1: Parallel Hybrid Search Fusion - Combine vector (semantic) and keyword (lexical) search
Priority 2: Parallel Context Pre-processing - Filter documents in parallel for relevance
Priority 3: Sharded & Scattered Retrieval - Parallel search across domain-scoped indexes
Priority 4: Parallel Query Expansion - Multi-strategy query generation for maximum recall
Priority 5: Redundant Execution (in intelligence/) - Fault-tolerant parallel execution

Expected Improvements:
- Accuracy: +25-50% on retrieval-augmented tasks
- Cost: -90% token usage for final generation
- Latency: -28% retrieval, -73% generation
- Reliability: +33% success rate for critical operations
- Scalability: Linear vs monolithic degradation

Version: 1.0
Date: 2026-01-04
"""

from .hybrid_search import (
    HybridRetriever,
    TfidfRetriever,
    VectorRetriever,
    HybridSearchResult,
    create_hybrid_retriever,
    Document,
)





__all__ = [
    # Priority 1: Hybrid Search
    'HybridRetriever',
    'TfidfRetriever',
    'VectorRetriever',
    'HybridSearchResult',
    'create_hybrid_retriever',
    'Document',

    # Priority 2: Context Distillation
    # Priority 3: Sharded Retrieval
    # Priority 4: Query Expansion
    # Unified Parallel RAG
    'ParallelRAGOrchestrator',
    'ParallelRAGConfig',
    'ParallelRAGResult',
]
