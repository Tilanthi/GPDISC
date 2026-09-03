#!/usr/bin/env python3
"""
Fetch biology papers from bioRxiv for GPDISC corpus
bioRxiv is the preprint server for biology
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

# bioRxiv API base URL
BIORXIV_API = "https://api.biorxiv.org/details/biorxiv"

# bioRxiv categories (collections) relevant to our domains
CATEGORIES = {
    'Biochemistry': 'biochemistry',
    'Bioengineering': 'bioengineering',
    'Bioinformatics': 'bioinformatics',
    'Biology': 'general_biology',
    'Biophysics': 'biophysics',
    'Cancer Biology': 'cancer_biology',
    'Cell Biology': 'cell_biology',
    'Computational Biology': 'computational_biology',
    'Developmental Biology': 'developmental_biology',
    'Ecology': 'ecology',
    'Evolutionary Biology': 'evolutionary_biology',
    'Genetics': 'genetics',
    'Genomics': 'genomics',
    'Immunology': 'immunology',
    'Molecular Biology': 'molecular_biology',
    'Neuroscience': 'neuroscience',
    'Omics': 'omics',
    'Synthetic Biology': 'synthetic_biology',
    'Systems Biology': 'systems_biology'
}

def fetch_biorxiv_papers(category, days_back=30, max_results=100):
    """Fetch recent papers from a bioRxiv category"""
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    # bioRxiv API uses format: YYYY-MM-DD
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    url = f"{BIORXIV_API}/{start_str}/{end_str}"

    try:
        print(f"  Fetching {category} papers...")
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        data = response.json()

        if 'collection' not in data:
            return []

        papers = []
        for item in data['collection']:
            # Filter by category if provided
            if category and category != 'general_biology':
                if 'category' not in item or category.lower() not in item['category'].lower():
                    continue

            paper_id = item.get('doi', '').split('/')[-1] if item.get('doi') else item.get('doi_id', '')

            authors = []
            if 'authors' in item:
                author_list = item['authors'].split(';')
                authors = [a.strip() for a in author_list[:5] if a.strip()]

            pub_date = item.get('date', '')

            # Clean up abstract
            abstract = item.get('abstract', '')
            if abstract:
                abstract = abstract.replace('\n', ' ')[:500]

            papers.append({
                'id': paper_id,
                'title': item.get('title', '').strip(),
                'authors': authors,
                'date': pub_date,
                'abstract': abstract,
                'category': item.get('category', ''),
                'doi': item.get('doi', ''),
                'version': item.get('version', '')
            })

            if len(papers) >= max_results:
                break

        return papers

    except Exception as e:
        print(f"  Error fetching {category}: {e}")
        return []

def create_biorxiv_metadata(category_code, category_name, papers):
    """Create corpus metadata for bioRxiv category"""
    domains_map = {
        'biochemistry': ['enzymes', 'metabolism', 'protein_structure', 'molecular_interactions'],
        'biophysics': ['molecular_mechanics', 'single_molecule', 'biophysical_chemistry', 'structural_biology'],
        'cell_biology': ['cell_signaling', 'cell_cycle', 'organelles', 'membrane_biology'],
        'genomics': ['genome_analysis', 'sequencing', 'transcriptomics', 'epigenomics'],
        'molecular_biology': ['dna_replication', 'transcription', 'translation', 'gene_regulation'],
        'systems_biology': ['pathway_analysis', 'network_biology', 'integrative_analysis', 'computational_modeling']
    }

    return {
        'source': f'bioRxiv Preprint Server - {category_name}',
        'fetched_date': datetime.now().strftime('%Y-%m-%d'),
        'total_papers': len(papers),
        'domains_covered': domains_map.get(category_code, [category_code]),
        'key_papers': papers[:20],
        'statistics': {
            'total_authors': sum(len(p['authors']) for p in papers),
            'date_range': f"{papers[-1]['date']} to {papers[0]['date']}" if papers else 'N/A',
            'avg_authors_per_paper': sum(len(p['authors']) for p in papers) / len(papers) if papers else 0
        }
    }

def main():
    """Main fetch function"""
    corpus_dir = Path(__file__).parent
    corpus_dir.mkdir(exist_ok=True)

    # Focus on key categories for our domains
    target_categories = ['Molecular Biology', 'Cell Biology', 'Genomics', 'Biochemistry', 'Systems Biology']

    all_results = {}

    for category in target_categories:
        print(f"Fetching {category}...")
        papers = fetch_biorxiv_papers(category, days_back=30, max_results=100)

        if papers:
            category_code = category.lower().replace(' ', '_')
            metadata = create_biorxiv_metadata(category_code, category, papers)

            # Save individual category file
            filename = f"biorxiv_{category_code}_recent.json"
            filepath = corpus_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  Saved {len(papers)} papers to {filename}")

            all_results[category] = {
                'papers_count': len(papers),
                'filename': filename
            }

        time.sleep(2)  # Rate limiting

    # Create bioRxiv index
    index = {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'categories': all_results,
        'total_papers': sum(r['papers_count'] for r in all_results.values())
    }

    with open(corpus_dir / 'biorxiv_index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nTotal bioRxiv papers fetched: {index['total_papers']}")
    print(f"Index saved to biorxiv_index.json")

if __name__ == '__main__':
    main()
