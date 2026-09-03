#!/usr/bin/env python3
"""
Fetch biology papers from Semantic Scholar API for GPDISC corpus
Semantic Scholar is a free, AI-powered research tool
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

# Semantic Scholar API base URL
S2_API = "https://api.semanticscholar.org/graph/v1"

# Biology fields of study
FIELDS_OF_STUDY = [
    'Molecular Biology',
    'Cell Biology',
    'Genetics',
    'Biochemistry',
    'Biophysics',
    'Computational Biology',
    'Genomics',
    'Proteomics',
    'Systems Biology',
    'Bioinformatics'
]

def fetch_papers_by_field(field_name, max_results=100):
    """Fetch recent papers from Semantic Scholar by field of study"""
    url = f"{S2_API}/paper/search"

    # Calculate date range (last 6 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    params = {
        'query': f'fieldOfStudy:"{field_name}"',
        'fields': 'paperId,title,authors,abstract,year,publicationDate,fieldsOfStudy,citationCount,url',
        'limit': min(max_results, 100),  # API limit
        'year': f'{start_date.year}-{end_date.year}'
    }

    try:
        print(f"  Fetching {field_name} papers...")
        response = requests.get(url, params=params, timeout=30, headers={'x-api-key': ''})
        response.raise_for_status()

        data = response.json()

        if 'data' not in data:
            return []

        papers = []
        for item in data['data']:
            authors = []
            if 'authors' in item:
                authors = [a.get('name', '') for a in item['authors'][:5] if a.get('name')]

            pub_date = item.get('publicationDate', '')
            if pub_date:
                pub_date = pub_date[:10]  # YYYY-MM-DD format

            abstract = item.get('abstract', '')
            if abstract:
                abstract = abstract[:500]

            papers.append({
                'id': item.get('paperId', ''),
                'title': item.get('title', ''),
                'authors': authors,
                'date': pub_date,
                'abstract': abstract,
                'year': item.get('year', ''),
                'fields': item.get('fieldsOfStudy', [])[:3],
                'citation_count': item.get('citationCount', 0),
                'url': item.get('url', '')
            })

        return papers

    except Exception as e:
        print(f"  Error fetching {field_name}: {e}")
        return []

def create_s2_metadata(field_code, field_name, papers):
    """Create corpus metadata for Semantic Scholar field"""
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
        'source': f'Semantic Scholar - {field_name}',
        'fetched_date': datetime.now().strftime('%Y-%m-%d'),
        'total_papers': len(papers),
        'domains_covered': domains_map.get(field_code, [field_code]),
        'key_papers': papers[:15],
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

    for field_name in FIELDS_OF_STUDY:
        papers = fetch_papers_by_field(field_name, max_results=100)

        if papers:
            field_code = field_name.lower().replace(' ', '_')
            metadata = create_s2_metadata(field_code, field_name, papers)

            # Save individual field file
            filename = f"semantic_scholar_{field_code}_recent.json"
            filepath = corpus_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  Saved {len(papers)} papers to {filename}")

            all_results[field_name] = {
                'papers_count': len(papers),
                'filename': filename
            }

        time.sleep(2)  # Rate limiting for Semantic Scholar API

    # Create Semantic Scholar index
    index = {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'categories': all_results,
        'total_papers': sum(r['papers_count'] for r in all_results.values()),
        'source': 'Semantic Scholar API'
    }

    with open(corpus_dir / 'semantic_scholar_index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nTotal Semantic Scholar papers fetched: {index['total_papers']}")
    print(f"Index saved to semantic_scholar_index.json")

if __name__ == '__main__':
    main()
