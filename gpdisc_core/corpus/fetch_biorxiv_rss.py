#!/usr/bin/env python3
"""
Fetch biology papers from bioRxiv RSS feeds for GPDISC corpus
bioRxiv provides RSS feeds for each category
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import time

# bioRxiv RSS feed URLs by category
BIORXIV_RSS_FEEDS = {
    'Biochemistry': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=54',
    'Biophysics': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=52',
    'Cell Biology': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=45',
    'Computational Biology': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=48',
    'Genetics': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=47',
    'Genomics': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=46',
    'Molecular Biology': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=43',
    'Systems Biology': 'https://www.biorxiv.org/cgi/collection?action=show&type=rss&feed=xml&categoryid=49'
}

def fetch_rss_papers(feed_url, category_name, max_results=50):
    """Fetch papers from a bioRxiv RSS feed"""
    try:
        print(f"  Fetching {category_name} RSS feed...")
        response = requests.get(feed_url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        # Parse RSS
        root = ET.fromstring(response.content)

        papers = []
        for item in root.findall('.//item')[:max_results]:
            title = item.find('title')
            if title is not None:
                title = title.text.strip()

            link = item.find('link')
            if link is not None:
                link = link.text.strip()
                # Extract DOI from link
                doi = link.split('/')[-1] if link else ''

            # Get authors
            authors = []
            author_elem = item.find('author')
            if author_elem is not None and author_elem.text:
                author_text = author_elem.text
                authors = [a.strip() for a in author_text.split(',')][:5]

            # Get date
            pub_date = item.find('dc:date')
            if pub_date is not None:
                pub_date = pub_date.text
            else:
                pub_date_elem = item.find('pubDate')
                if pub_date_elem is not None:
                    pub_date = pub_date_elem.text
                else:
                    pub_date = ''

            # Get abstract (description)
            description = item.find('description')
            abstract = ''
            if description is not None and description.text:
                # Remove HTML tags
                import re
                abstract = re.sub(r'<[^>]+>', '', description.text)
                abstract = abstract.strip()[:500]

            papers.append({
                'id': doi,
                'title': title,
                'authors': authors,
                'date': pub_date[:10] if pub_date else '',
                'abstract': abstract,
                'category': category_name,
                'link': link
            })

        return papers

    except Exception as e:
        print(f"  Error fetching {category_name}: {e}")
        return []

def create_biorxiv_metadata(category_code, category_name, papers):
    """Create corpus metadata for bioRxiv category"""
    domains_map = {
        'biochemistry': ['enzymes', 'metabolism', 'protein_structure', 'molecular_interactions'],
        'biophysics': ['molecular_mechanics', 'single_molecule', 'biophysical_chemistry', 'structural_biology'],
        'cell_biology': ['cell_signaling', 'cell_cycle', 'organelles', 'membrane_biology'],
        'computational_biology': ['bioinformatics_algorithms', 'computational_methods', 'data_analysis'],
        'genetics': ['genetic_variation', 'gene_regulation', 'heritability', 'genetic_mapping'],
        'genomics': ['genome_analysis', 'sequencing', 'transcriptomics', 'epigenomics'],
        'molecular_biology': ['dna_replication', 'transcription', 'translation', 'gene_regulation'],
        'systems_biology': ['pathway_analysis', 'network_biology', 'integrative_analysis', 'computational_modeling']
    }

    return {
        'source': f'bioRxiv RSS Feed - {category_name}',
        'fetched_date': datetime.now().strftime('%Y-%m-%d'),
        'total_papers': len(papers),
        'domains_covered': domains_map.get(category_code, [category_code]),
        'key_papers': papers[:15],
        'statistics': {
            'total_authors': sum(len(p['authors']) for p in papers),
            'avg_authors_per_paper': sum(len(p['authors']) for p in papers) / len(papers) if papers else 0
        }
    }

def main():
    """Main fetch function"""
    corpus_dir = Path(__file__).parent
    corpus_dir.mkdir(exist_ok=True)

    all_results = {}

    for category_name, feed_url in BIORXIV_RSS_FEEDS.items():
        print(f"Fetching {category_name}...")
        papers = fetch_rss_papers(feed_url, category_name, max_results=50)

        if papers:
            category_code = category_name.lower().replace(' ', '_')
            metadata = create_biorxiv_metadata(category_code, category_name, papers)

            # Save individual category file
            filename = f"biorxiv_rss_{category_code}_recent.json"
            filepath = corpus_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  Saved {len(papers)} papers to {filename}")

            all_results[category_name] = {
                'papers_count': len(papers),
                'filename': filename
            }

        time.sleep(1)  # Rate limiting

    # Create bioRxiv RSS index
    index = {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'categories': all_results,
        'total_papers': sum(r['papers_count'] for r in all_results.values()),
        'source': 'bioRxiv RSS feeds'
    }

    with open(corpus_dir / 'biorxiv_rss_index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nTotal bioRxiv papers fetched: {index['total_papers']}")
    print(f"Index saved to biorxiv_rss_index.json")

if __name__ == '__main__':
    main()
