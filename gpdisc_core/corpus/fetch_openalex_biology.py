#!/usr/bin/env python3
"""
Fetch biology papers from OpenAlex API for GPDISC corpus
OpenAlex is a fully open catalog of global research system
No API key required, no rate limits
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

# OpenAlex API base URL (Polite Pool - include email)
OPENALEX_API = "https://api.openalex.org/works"

# Biology concepts in OpenAlex (use concept IDs)
BIOLOGY_CONCEPTS = {
    'Molecular Biology': 'https://openalex.org/C185592680',
    'Cell Biology': 'https://openalex.org/C71924100',
    'Genetics': 'https://openalex.org/C185844422',
    'Biochemistry': 'https://openalex.org/C166323869',
    'Biophysics': 'https://openalex.org/C118552586',
    'Computational Biology': 'https://openalex.org/C121332964',
    'Genomics': 'https://openalex.org/C144024400',
    'Proteomics': 'https://openalex.org/C144133530',
    'Systems Biology': 'https://openalex.org/C2779940599',
    'Bioinformatics': 'https://openalex.org/C182752681'
}

def fetch_openalex_papers(concept_url, concept_name, max_results=100):
    """Fetch recent papers from OpenAlex by concept"""
    # Calculate date range (last 6 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    # OpenAlex filter for recent papers in concept
    # Use concepts.id:CONCEPT_ID format
    concept_id = concept_url.split('/')[-1]

    filter_str = f"concepts.id:{concept_id},from_publication_date:{start_date.strftime('%Y-%m-%d')},type:article"

    params = {
        'filter': filter_str,
        'per-page': min(max_results, 200),  # Max 200 per page
        'sort': 'publication_date:desc'
    }

    # Use polite pool email
    headers = {
        'User-Agent': 'mailto:biodisc-system@example.com',
        'Accept': 'application/json'
    }

    try:
        print(f"  Fetching {concept_name} papers...")
        response = requests.get(OPENALEX_API, params=params, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        if 'results' not in data:
            return []

        papers = []
        for item in data['results'][:max_results]:
            authors = []
            if 'authorships' in item:
                authors = [a['author']['display_name'] for a in item['authorships'][:5] if a.get('author', {}).get('display_name')]

            pub_date = item.get('publication_date', '')

            # Get primary location (journal)
            source = ''
            if 'primary_location' in item and item['primary_location']:
                if 'source' in item['primary_location'] and item['primary_location']['source']:
                    source = item['primary_location']['source'].get('display_name', '')

            # Get abstract (inverted index format)
            abstract = ''
            if 'abstract_inverted_index' in item and item['abstract_inverted_index']:
                # Note: OpenAlex stores abstracts as inverted index
                # For corpus purposes, we'll note it's available
                abstract = 'Abstract available in OpenAlex'

            papers.append({
                'id': item.get('id', '').split('/')[-1],
                'title': item.get('title', ''),
                'authors': authors,
                'date': pub_date[:10] if pub_date else '',
                'abstract': abstract,
                'year': item.get('publication_year', ''),
                'type': item.get('type', ''),
                'source': source,
                'concepts': [c.get('display_name', '') for c in item.get('concepts', [])[:5]],
                'citation_count': item.get('cited_by_count', 0),
                'openalex_url': item.get('id', '')
            })

        return papers

    except Exception as e:
        print(f"  Error fetching {concept_name}: {e}")
        return []

def create_openalex_metadata(concept_code, concept_name, papers):
    """Create corpus metadata for OpenAlex concept"""
    domains_map = {
        'molecular_biology': ['dna_replication', 'transcription', 'translation', 'gene_expression', 'molecular_genetics'],
        'cell_biology': ['cell_structure', 'cell_signaling', 'organelles', 'cell_cycle', 'membrane_biology'],
        'genetics': ['genetic_variation', 'gene_regulation', 'heritability', 'genetic_mapping', 'mutation'],
        'biochemistry': ['enzymes', 'metabolism', 'protein_structure', 'molecular_interactions', 'catalysis'],
        'biophysics': ['molecular_mechanics', 'single_molecule', 'biophysical_chemistry', 'structural_biology'],
        'computational_biology': ['bioinformatics_algorithms', 'computational_methods', 'data_analysis', 'modeling'],
        'genomics': ['genome_analysis', 'sequencing', 'transcriptomics', 'epigenomics', 'comparative_genomics'],
        'proteomics': ['protein_structure', 'protein_interactions', 'mass_spectrometry', 'protein_modification'],
        'systems_biology': ['pathway_analysis', 'network_biology', 'integrative_analysis', 'computational_modeling'],
        'bioinformatics': ['sequence_analysis', 'structural_prediction', 'data_integration', 'algorithm_development']
    }

    return {
        'source': f'OpenAlex - {concept_name}',
        'fetched_date': datetime.now().strftime('%Y-%m-%d'),
        'total_papers': len(papers),
        'domains_covered': domains_map.get(concept_code, [concept_code]),
        'key_papers': papers[:20],
        'statistics': {
            'total_authors': sum(len(p['authors']) for p in papers),
            'avg_citations': sum(p['citation_count'] for p in papers) / len(papers) if papers else 0,
            'avg_authors_per_paper': sum(len(p['authors']) for p in papers) / len(papers) if papers else 0
        }
    }

def main():
    """Main fetch function"""
    corpus_dir = Path(__file__).parent
    corpus_dir.mkdir(exist_ok=True)

    all_results = {}

    for concept_name, concept_url in BIOLOGY_CONCEPTS.items():
        papers = fetch_openalex_papers(concept_url, concept_name, max_results=100)

        if papers:
            concept_code = concept_name.lower().replace(' ', '_')
            metadata = create_openalex_metadata(concept_code, concept_name, papers)

            # Save individual concept file
            filename = f"openalex_{concept_code}_recent.json"
            filepath = corpus_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  Saved {len(papers)} papers to {filename}")

            all_results[concept_name] = {
                'papers_count': len(papers),
                'filename': filename
            }

        # No sleep needed for OpenAlex (no rate limits)

    # Create OpenAlex index
    index = {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'categories': all_results,
        'total_papers': sum(r['papers_count'] for r in all_results.values()),
        'source': 'OpenAlex API (open catalog of global research)'
    }

    with open(corpus_dir / 'openalex_index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nTotal OpenAlex papers fetched: {index['total_papers']}")
    print(f"Index saved to openalex_index.json")

if __name__ == '__main__':
    main()
