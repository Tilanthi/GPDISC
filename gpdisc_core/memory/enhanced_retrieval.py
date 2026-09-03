"""
Enhanced Memory Retrieval Package

Advanced memory retrieval with semantic search and
context-aware ranking.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class MemoryItem:
    """Item in memory with relevance metadata."""
    content: str
    timestamp: datetime
    domain: str
    patient_id: str
    metadata: Dict[str, Any]
    similarity_score: float = 0.0
    temporal_score: float = 0.0
    combined_score: float = 0.0


class SemanticMemoryRetriever:
    """
    Retrieve memories using semantic similarity and temporal relevance.

    Features:
    - Semantic similarity scoring
    - Temporal decay weighting
    - Hybrid retrieval (semantic + keyword)
    - Context-aware ranking
    """

    def __init__(self, memory_system: Optional[Any] = None):
        self.memory_system = memory_system
        self.temporal_decay_hours = 24  # Decay period in hours
        self.decay_factor = 0.5  # Decay strength

    def retrieve_relevant_memories(self,
                                  query: str,
                                  patient_id: str,
                                  limit: int = 10,
                                  time_window: Optional[timedelta] = None) -> List[MemoryItem]:
        """
        Retrieve relevant memories using semantic and temporal scoring.

        Args:
            query: Search query
            patient_id: Patient identifier
            limit: Maximum number of memories to return
            time_window: Optional time window for retrieval

        Returns:
            List of MemoryItems sorted by relevance
        """
        # Get candidate memories
        candidates = self._get_candidate_memories(patient_id, time_window)

        if not candidates:
            return []

        # Score candidates
        scored_items = []
        for candidate in candidates:
            item = self._score_memory(candidate, query)
            scored_items.append(item)

        # Sort by combined score
        scored_items.sort(key=lambda x: x.combined_score, reverse=True)

        return scored_items[:limit]

    def semantic_search(self,
                       query: str,
                       patient_id: str,
                       limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic search on patient memories.

        Args:
            query: Search query
            patient_id: Patient identifier
            limit: Maximum results

        Returns:
            List of search results with similarity scores
        """
        if not self.memory_system:
            return []

        try:
            # Try memory system's semantic search
            if hasattr(self.memory_system, 'semantic_search'):
                results = self.memory_system.semantic_search(query, patient_id, limit)
                return results

            # Fallback to vector store search
            if hasattr(self.memory_system, 'vector_store'):
                # This would require embedding the query
                # For now, return empty
                return []

        except Exception as e:
            print(f"Warning: Semantic search failed: {e}")

        return []

    def hybrid_search(self,
                     query: str,
                     patient_id: str,
                     keywords: List[str],
                     limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform hybrid semantic + keyword search.

        Args:
            query: Search query
            patient_id: Patient identifier
            keywords: List of keywords for exact matching
            limit: Maximum results

        Returns:
            List of search results
        """
        # Get semantic results
        semantic_results = self.semantic_search(query, patient_id, limit * 2)

        # Get keyword results
        keyword_results = self._keyword_search(keywords, patient_id, limit * 2)

        # Combine and deduplicate
        combined = self._combine_search_results(semantic_results, keyword_results)

        # Re-rank combined results
        reranked = self._rerank_results(combined, query, keywords)

        return reranked[:limit]

    def _get_candidate_memories(self,
                                patient_id: str,
                                time_window: Optional[timedelta] = None) -> List[Dict[str, Any]]:
        """Get candidate memories for retrieval."""
        if not self.memory_system:
            return []

        try:
            # Get patient records
            if hasattr(self.memory_system, 'get_patient_records'):
                records = self.memory_system.get_patient_records(patient_id)

                # Filter by time window if specified
                if time_window:
                    cutoff = datetime.now() - time_window
                    records = [
                        r for r in records
                        if datetime.fromisoformat(r.get('timestamp', '')) >= cutoff
                    ]

                return records

        except Exception as e:
            print(f"Warning: Could not retrieve candidate memories: {e}")

        return []

    def _score_memory(self, memory: Dict[str, Any], query: str) -> MemoryItem:
        """Score memory by semantic similarity and temporal relevance."""
        # Create MemoryItem
        item = MemoryItem(
            content=memory.get('answer', memory.get('content', '')),
            timestamp=datetime.fromisoformat(memory.get('timestamp', datetime.now().isoformat())),
            domain=memory.get('domain', 'unknown'),
            patient_id=memory.get('patient_id', ''),
            metadata=memory
        )

        # Calculate semantic similarity
        item.similarity_score = self._calculate_similarity(item.content, query)

        # Calculate temporal score
        item.temporal_score = self._calculate_temporal_score(item.timestamp)

        # Calculate combined score
        item.combined_score = self._combine_scores(item.similarity_score, item.temporal_score)

        return item

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between texts.

        Note: This is a simple implementation using word overlap.
        Production systems should use embeddings.
        """
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _calculate_temporal_score(self, timestamp: datetime) -> float:
        """Calculate temporal relevance score."""
        now = datetime.now()
        age_hours = (now - timestamp).total_seconds() / 3600

        # Exponential decay
        score = math.exp(-self.decay_factor * age_hours / self.temporal_decay_hours)

        return score

    def _combine_scores(self, semantic_score: float, temporal_score: float) -> float:
        """Combine semantic and temporal scores."""
        # Weighted combination (favor semantic)
        semantic_weight = 0.7
        temporal_weight = 0.3

        return (semantic_weight * semantic_score +
                temporal_weight * temporal_score)

    def _keyword_search(self,
                       keywords: List[str],
                       patient_id: str,
                       limit: int) -> List[Dict[str, Any]]:
        """Perform keyword-based search."""
        candidates = self._get_candidate_memories(patient_id)

        if not candidates:
            return []

        # Score by keyword matches
        scored = []
        for candidate in candidates:
            content = candidate.get('answer', '').lower()
            keyword_score = sum(1 for kw in keywords if kw.lower() in content)

            if keyword_score > 0:
                candidate['keyword_score'] = keyword_score
                scored.append(candidate)

        # Sort by keyword score
        scored.sort(key=lambda x: x.get('keyword_score', 0), reverse=True)

        return scored[:limit]

    def _combine_search_results(self,
                               semantic_results: List[Dict],
                               keyword_results: List[Dict]) -> List[Dict]:
        """Combine semantic and keyword search results."""
        # Use dictionary to deduplicate by timestamp
        combined = {}

        # Add semantic results
        for result in semantic_results:
            key = result.get('timestamp', '')
            combined[key] = {**result, 'semantic_rank': len(combined)}

        # Add keyword results
        for result in keyword_results:
            key = result.get('timestamp', '')
            if key in combined:
                combined[key]['keyword_rank'] = result.get('keyword_score', 0)
            else:
                combined[key] = {**result, 'keyword_rank': result.get('keyword_score', 0)}

        return list(combined.values())

    def _rerank_results(self,
                       combined: List[Dict],
                       query: str,
                       keywords: List[str]) -> List[Dict]:
        """Re-rank combined search results."""
        for result in combined:
            # Calculate combined rank
            semantic_rank = result.get('semantic_rank', 999)
            keyword_rank = result.get('keyword_rank', 0)

            # Normalize ranks
            normalized_semantic = 1.0 / (1.0 + semantic_rank)
            normalized_keyword = keyword_rank / max(len(keywords), 1)

            # Combined score
            result['rerank_score'] = (
                0.7 * normalized_semantic +
                0.3 * normalized_keyword
            )

        # Sort by rerank score
        combined.sort(key=lambda x: x.get('rerank_score', 0.0), reverse=True)

        return combined


class ContextAwareRetriever:
    """
    Context-aware memory retrieval that considers consultation context.

    Features:
    - Conversation context awareness
    - Domain-specific retrieval
    - Confidence-based filtering
    """

    def __init__(self, semantic_retriever: Optional[SemanticMemoryRetriever] = None):
        self.semantic_retriever = semantic_retriever or SemanticMemoryRetriever()

    def retrieve_with_context(self,
                             query: str,
                             patient_id: str,
                             current_domain: str,
                             recent_context: List[Dict],
                             limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve memories with consultation context awareness.

        Args:
            query: Current query
            patient_id: Patient identifier
            current_domain: Current medical domain
            recent_context: Recent consultation context
            limit: Maximum results

        Returns:
            Context-aware retrieved memories
        """
        # Get base semantic results
        base_results = self.semantic_retriever.retrieve_relevant_memories(
            query, patient_id, limit * 2
        )

        # Filter by domain relevance
        domain_filtered = self._filter_by_domain(base_results, current_domain)

        # Boost by context similarity
        context_boosted = self._boost_by_context(domain_filtered, recent_context)

        # Filter by confidence threshold
        confidence_filtered = self._filter_by_confidence(context_boosted, 0.6)

        return confidence_filtered[:limit]

    def _filter_by_domain(self,
                         items: List[MemoryItem],
                         current_domain: str) -> List[MemoryItem]:
        """Filter and boost items by domain relevance."""
        # Domain affinity map
        domain_affinity = {
            "cardiology": ["cardiology", "general_practice"],
            "epilepsy": ["epilepsy", "neurology", "general_practice"],
            "orthopedics": ["orthopedics", "general_practice"],
            "pharmacology": ["pharmacology", "general_practice"],
            "general_practice": ["general_practice", "cardiology", "epilepsy", "orthopedics"]
        }

        related_domains = domain_affinity.get(current_domain, [current_domain])

        # Filter and boost
        filtered = []
        for item in items:
            if item.domain in related_domains:
                # Boost score if exact domain match
                if item.domain == current_domain:
                    item.combined_score *= 1.2

                filtered.append(item)

        return filtered

    def _boost_by_context(self,
                         items: List[MemoryItem],
                         recent_context: List[Dict]) -> List[MemoryItem]:
        """Boost items based on similarity to recent context."""
        if not recent_context:
            return items

        # Extract context keywords
        context_keywords = set()
        for ctx in recent_context:
            query_words = set(ctx.get('query', '').lower().split())
            context_keywords.update(query_words)

        # Boost items with context keyword matches
        for item in items:
            content_words = set(item.content.lower().split())
            overlap = len(context_keywords.intersection(content_words))

            if overlap > 0:
                # Boost proportional to overlap
                boost_factor = 1.0 + (0.1 * overlap)
                item.combined_score *= boost_factor

        return items

    def _filter_by_confidence(self,
                             items: List[MemoryItem],
                             threshold: float) -> List[MemoryItem]:
        """Filter items by confidence threshold."""
        # Get confidence from metadata
        filtered = []
        for item in items:
            confidence = item.metadata.get('confidence', 0.5)

            # Allow lower confidence if combined score is high
            if confidence >= threshold or item.combined_score >= 0.7:
                filtered.append(item)

        return filtered


__all__ = [
    "SemanticMemoryRetriever",
    "ContextAwareRetriever",
    "MemoryItem"
]
