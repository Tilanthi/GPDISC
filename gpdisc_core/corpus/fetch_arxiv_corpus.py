#!/usr/bin/env python3
"""
Fetch biology papers from arXiv q-bio subcategories for GPDISC corpus
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import time

# arXiv API namespace
NS = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

# q-bio subcategories to fetch
CATEGORIES = {
    'q-bio.CB': 'Cell Behavior',
    'q-bio.GN': 'Genomics',
    'q-bio.MN': 'Molecular Networks',
    'q-bio.NC': 'Neurons and Cognition',
    'q-bio.PE': 'Populations and Evolution',
    'q-bio.QM': 'Quantitative Methods',
    'q-bio.TO': 'Tissues and Organs'
}

def fetch_papers(category, max_results=100):
    """Fetch papers from a specific arXiv category"""
    query = f"cat:{category}"
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        papers = []
        for entry in root.findall('atom:entry', NS):
            paper_id = entry.find('atom:id', NS).text.split('/')[-1]
            title = entry.find('atom:title', NS).text.strip().replace('\n', ' ')

            authors = []
            for author in entry.findall('atom:author', NS):
                name = author.find('atom:name', NS).text
                authors.append(name)

            pub_date = None
            published = entry.find('atom:published', NS)
            if published is not None:
                pub_date = published.text.split('T')[0]

            summary = entry.find('atom:summary', NS).text.strip().replace('\n', ' ')

            categories = []
            for cat in entry.findall('atom:category', NS):
                term = cat.get('term')
                if term:
                    categories.append(term)

            papers.append({
                'id': paper_id,
                'title': title,
                'authors': authors[:5],
                'date': pub_date,
                'abstract': summary[:500],
                'categories': categories[:3]
            })

        return papers

    except Exception as e:
        print(f"Error fetching {category}: {e}")
        return []

def create_corpus_metadata(category_code, category_name, papers):
    """Create corpus metadata for a category"""
    domains_map = {
        'q-bio.CB': ['cell_mechanics', 'cell_signaling', 'cell_adhesion', 'cell_motility', 'cytoskeleton', 'cell_division'],
        'q-bio.GN': ['genome_assembly', 'sequencing', 'transcriptomics', 'epigenomics', 'functional_genomics', 'comparative_genomics'],
        'q-bio.MN': ['gene_regulatory_networks', 'protein_interaction_networks', 'metabolic_networks', 'signaling_networks'],
        'q-bio.NC': ['neural_networks', 'computational_neuroscience', 'brain_modeling', 'cognitive_models'],
        'q-bio.PE': ['population_genetics', 'evolutionary_dynamics', 'phylogenetics', 'ecological_modeling'],
        'q-bio.QM': ['bioinformatics', 'statistical_methods', 'machine_learning', 'data_analysis'],
        'q-bio.TO': ['tissue_engineering', 'organ_modeling', 'developmental_biology', 'organogenesis']
    }

    return {
        'source': f'arXiv Quantitative Biology - {category_name} ({category_code})',
        'fetched_date': datetime.now().strftime('%Y-%m-%d'),
        'total_papers': len(papers),
        'domains_covered': domains_map.get(category_code, []),
        'key_papers': papers[:15],
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

    all_results = {}

    for code, name in CATEGORIES.items():
        print(f"Fetching {name} ({code})...")
        papers = fetch_papers(code, max_results=100)

        if papers:
            metadata = create_corpus_metadata(code, name, papers)

            # Save individual category file
            filename = f"arxiv_{code.replace('.', '_').replace('-', '_')}_recent.json"
            filepath = corpus_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  Saved {len(papers)} papers to {filename}")

            all_results[code] = {
                'name': name,
                'papers_count': len(papers),
                'filename': filename
            }

        time.sleep(1)  # Rate limiting

    # Create master index
    index = {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'categories': all_results,
        'total_papers': sum(r['papers_count'] for r in all_results.values())
    }

    with open(corpus_dir / 'arxiv_qbio_index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nTotal papers fetched: {index['total_papers']}")
    print(f"Index saved to arxiv_qbio_index.json")

if __name__ == '__main__':
    main()
