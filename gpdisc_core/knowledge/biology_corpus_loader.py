#!/usr/bin/env python3
"""
Biology Corpus Loader for GPDISC
Loads and processes biology research papers for knowledge base construction
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


class BiologyCorpusLoader:
    """Load and process biology research papers from the corpus"""

    def __init__(self, corpus_dir: str = None):
        """Initialize corpus loader"""
        if corpus_dir is None:
            corpus_dir = str(Path(__file__).parent.parent / "corpus")

        self.corpus_dir = Path(corpus_dir)
        self.master_index = self._load_master_index()
        self.papers_cache = {}

    def _load_master_index(self) -> Dict[str, Any]:
        """Load the master corpus index"""
        index_path = self.corpus_dir / 'MASTER_INDEX.json'
        if index_path.exists():
            with open(index_path) as f:
                return json.load(f)
        return {}

    def list_corpus_files(self) -> List[str]:
        """List all corpus JSON files"""
        return [f.name for f in self.corpus_dir.glob('*.json')
                if f.name not in ['MASTER_INDEX.json', 'arxiv_qbio_index.json',
                                   'openalex_index.json', 'biorxiv_index.json']]

    def load_corpus_file(self, filename: str) -> Dict[str, Any]:
        """Load a specific corpus file"""
        if filename in self.papers_cache:
            return self.papers_cache[filename]

        filepath = self.corpus_dir / filename
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
                self.papers_cache[filename] = data
                return data
        return {}

    def get_papers_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Get all papers relevant to a specific biology domain"""
        domain_mapping = {
            'molecular_biology': ['arxiv_qbio_biomolecules_recent.json',
                                  'arxiv_q_bio_MN_recent.json'],
            'biochemistry': ['arxiv_qbio_biomolecules_recent.json'],
            'genetics': ['arxiv_q_bio_GN_recent.json',
                         'arxiv_q_bio_PE_recent.json'],
            'cell_biology': ['arxiv_q_bio_CB_recent.json'],
            'biophysics': ['arxiv_qbio_biomolecules_recent.json',
                           'arxiv_q_bio_QM_recent.json'],
            'bioinformatics': ['arxiv_q_bio_GN_recent.json',
                               'arxiv_q_bio_QM_recent.json'],
            'computational_biology': ['arxiv_q_bio_QM_recent.json',
                                      'arxiv_q_bio_GN_recent.json'],
            'genomics': ['arxiv_q_bio_GN_recent.json'],
            'proteomics': ['arxiv_qbio_biomolecules_recent.json'],
            'systems_biology': ['arxiv_q_bio_MN_recent.json']
        }

        papers = []
        files = domain_mapping.get(domain, [])

        for filename in files:
            data = self.load_corpus_file(filename)
            if 'key_papers' in data:
                papers.extend(data['key_papers'])

        return papers

    def extract_entities(self, papers: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract biological entities from papers"""
        entities = defaultdict(list)

        for paper in papers:
            title = paper.get('title', '')
            abstract = paper.get('abstract', '')

            # Extract protein names (simple heuristic)
            protein_pattern = r'\b[A-Z][A-Z0-9]{2,}\b'
            proteins = set(re.findall(protein_pattern, title + ' ' + abstract))
            entities['proteins'].extend(list(proteins))

            # Extract gene names
            gene_pattern = r'\b[A-Z][a-z]{2,}[0-9]+\b'
            genes = set(re.findall(gene_pattern, title + ' ' + abstract))
            entities['genes'].extend(list(genes))

            # Extract techniques
            techniques = ['CRISPR', 'PCR', 'RNA-seq', 'ChIP-seq', 'mass spectrometry',
                         'crystallography', 'cryo-EM', 'NMR', 'X-ray', 'sequencing']
            for technique in techniques:
                if technique.lower() in (title + ' ' + abstract).lower():
                    entities['techniques'].append(technique)

            # Extract organisms
            organisms = ['E. coli', 'human', 'mouse', 'yeast', 'Arabidopsis',
                        'Drosophila', 'zebrafish', 'E. coli', 'S. cerevisiae']
            for organism in organisms:
                if organism.lower() in (title + ' ' + abstract).lower():
                    entities['organisms'].append(organism)

        return {k: list(set(v)) for k, v in entities.items()}

    def build_term_frequencies(self, papers: List[Dict[str, Any]]) -> Counter:
        """Build term frequency dictionary from papers"""
        terms = Counter()

        for paper in papers:
            title = paper.get('title', '').lower()
            abstract = paper.get('abstract', '').lower()

            # Tokenize and count
            words = re.findall(r'\b[a-z]{3,}\b', title + ' ' + abstract)
            terms.update(words)

        # Remove common stopwords
        stopwords = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
                    'had', 'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been'}
        for word in stopwords:
            terms.pop(word, None)

        return terms

    def get_corpus_statistics(self) -> Dict[str, Any]:
        """Get overall corpus statistics"""
        stats = {
            'total_papers': 0,
            'sources': defaultdict(int),
            'domains': defaultdict(int),
            'authors': Counter(),
            'top_terms': Counter()
        }

        for filename in self.list_corpus_files():
            data = self.load_corpus_file(filename)
            if data:
                stats['total_papers'] += data.get('total_papers', 0)
                source = data.get('source', '').split('-')[0].strip()
                stats['sources'][source] += data.get('total_papers', 0)

                if 'domains_covered' in data:
                    for domain in data['domains_covered']:
                        stats['domains'][domain] += 1

                if 'key_papers' in data:
                    for paper in data['key_papers']:
                        for author in paper.get('authors', []):
                            stats['authors'][author] += 1

        return stats

    def create_knowledge_snapshot(self) -> Dict[str, Any]:
        """Create a snapshot of knowledge from the corpus"""
        snapshot = {
            'corpus_summary': self.get_corpus_statistics(),
            'domain_entities': {},
            'domain_terms': {}
        }

        for domain in ['molecular_biology', 'biochemistry', 'genetics', 'cell_biology']:
            papers = self.get_papers_by_domain(domain)
            if papers:
                entities = self.extract_entities(papers[:20])  # Sample for speed
                terms = self.build_term_frequencies(papers[:50])

                snapshot['domain_entities'][domain] = entities
                snapshot['domain_terms'][domain] = dict(terms.most_common(20))

        return snapshot

    def search_papers(self, query: str, domain: str = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search papers by query string"""
        query_lower = query.lower()

        # Determine which files to search
        if domain:
            papers = self.get_papers_by_domain(domain)
        else:
            papers = []
            for filename in self.list_corpus_files():
                data = self.load_corpus_file(filename)
                if 'key_papers' in data:
                    papers.extend(data['key_papers'])

        # Filter papers matching query
        results = []
        for paper in papers:
            title = paper.get('title', '').lower()
            abstract = paper.get('abstract', '').lower()

            if query_lower in title or query_lower in abstract:
                results.append(paper)
                if len(results) >= max_results:
                    break

        return results


def create_corpus_loader(corpus_dir: str = None) -> BiologyCorpusLoader:
    """Factory function for corpus loader"""
    return BiologyCorpusLoader(corpus_dir)


if __name__ == '__main__':
    loader = create_corpus_loader()

    # Print corpus statistics
    stats = loader.get_corpus_statistics()
    print(f"Total papers: {stats['total_papers']}")
    print(f"Sources: {dict(stats['sources'])}")
    print(f"Top authors: {stats['authors'].most_common(5)}")

    # Create knowledge snapshot
    snapshot = loader.create_knowledge_snapshot()

    # Save snapshot
    output_path = Path(__file__).parent / "corpus_snapshot.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(snapshot, f, indent=2, default=str)

    print(f"\nKnowledge snapshot saved to {output_path}")
