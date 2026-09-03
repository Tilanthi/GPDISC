#!/usr/bin/env python3
"""
V73 Memory Palace Integration - Manual Tools

Manual tools for managing memory palace integration with autonomous discoveries.

Date: 2026-04-26
Version: 1.0.0
"""

import os
import sys
import json
from datetime import datetime


from gpdisc_core.reasoning.v73_memory_palace_integration import (
    retroactively_store_discoveries,
    get_automatic_memory_integration,
    MEMORY_PALACE_PATH
)


def list_memory_palace_discoveries():
    """List all discoveries currently stored in memory palace"""
    memory_index = os.path.join(MEMORY_PALACE_PATH, "MEMORY.md")

    if not os.path.exists(memory_index):
        print("No memory palace found at:", MEMORY_PALACE_PATH)
        return []

    try:
        with open(memory_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract discovery entries
        discoveries = []
        in_discovery_section = False

        for line in content.split('\n'):
            if "## Autonomous Discoveries" in line:
                in_discovery_section = True
                continue

            if in_discovery_section and line.startswith('- ['):
                # Extract discovery info
                if 'autonomous_discovery' in line:
                    discoveries.append(line.strip())

            if in_discovery_section and line.startswith('## ') and "Autonomous Discoveries" not in line:
                break

        return discoveries

    except Exception as e:
        print(f"Error reading memory palace: {e}")
        return []


def show_discovery_status():
    """Show current status of memory palace integration"""
    print("=== V73 Memory Palace Integration Status ===\n")

    integration = get_automatic_memory_integration()
    status = integration.get_status()

    print(f"Memory Palace Path: {MEMORY_PALACE_PATH}")
    print(f"Total Discoveries Stored: {status['total_stored']}")
    print(f"Last Storage: {status['last_storage_time'] or 'Never'}")
    print(f"Memory Palace Summary: {status['summary']}")

    print("\nDiscoveries in Memory Palace:")
    discoveries = list_memory_palace_discoveries()

    if discoveries:
        for i, discovery in enumerate(discoveries, 1):
            print(f"  {i}. {discovery}")
    else:
        print("  (No discoveries yet)")


def create_sample_discoveries():
    """Create sample discoveries for testing"""
    return [
        {
            'id': 'sample_membrane_gene_regulation',
            'question': 'What connections exist between membrane physics and gene regulation?',
            'discovery': 'Cross-domain connection identified: Membrane physical properties (curvature, tension, lipid composition) may influence gene expression through mechanosensitive transcription factors. This represents a novel regulatory coupling where physical state directly modulates genetic programs.',
            'confidence': 0.96,
            'evidence': [
                'Membrane curvature affects division site selection (known)',
                'Cardiolipin domains correlate with certain gene expression patterns (observed)',
                'Physical stress triggers transcriptional responses (known in other systems)'
            ],
            'timestamp': datetime.now().timestamp(),
            'validation_status': 'validated',
            'impact_estimate': 0.7
        },
        {
            'id': 'sample_causal_discovery_improvement',
            'question': 'How can we improve the efficiency of causal discovery algorithms?',
            'discovery': 'Meta-discovery: Causal discovery efficiency can be improved by (1) pre-filtering variables using domain knowledge, (2) parallelizing hypothesis tests, (3) caching intermediate results for repeated queries. Expected 3-5x speedup on large datasets.',
            'confidence': 0.94,
            'evidence': [
                'Pre-filtering reduces search space (theoretical)',
                'Parallel processing is embarrassingly parallel (known)',
                'Result caching avoids recomputation (established technique)'
            ],
            'timestamp': datetime.now().timestamp(),
            'validation_status': 'validated',
            'impact_estimate': 0.8
        },
        {
            'id': 'sample_ftsz_independent_division',
            'question': 'Why do some bacteria use FtsZ-independent division mechanisms?',
            'discovery': 'Pattern anomaly discovered: L-forms and some archaea divide without FtsZ, relying instead on increased membrane synthesis and turgor pressure. This suggests physical processes alone can accomplish cell division, representing the ancestral condition before evolution of molecular division machinery.',
            'confidence': 0.92,
            'evidence': [
                'L-forms divide without FtsZ (established)',
                'Archaea use ESCRT-III or Crenactin (known)',
                'Physical scission occurs in lipid vesicles (experimental)'
            ],
            'timestamp': datetime.now().timestamp(),
            'validation_status': 'validated',
            'impact_estimate': 0.75
        }
    ]


def test_memory_palace_integration():
    """Test memory palace integration with sample discoveries"""
    print("=== Testing Memory Palace Integration ===\n")

    # Create sample discoveries
    discoveries = create_sample_discoveries()
    print(f"Created {len(discoveries)} sample discoveries\n")

    # Store them
    print("Storing discoveries to memory palace...")
    stored = retroactively_store_discoveries(discoveries)
    print(f"Successfully stored {stored}/{len(discoveries)} discoveries\n")

    # Show status
    show_discovery_status()


def import_discoveries_from_log():
    """
    Import discoveries from V73 discovery log file.

    Reads from /tmp/gpdisc_discoveries.jsonl and stores validated
    discoveries to memory palace.
    """
    log_file = "/tmp/gpdisc_discoveries.jsonl"

    if not os.path.exists(log_file):
        print(f"No discovery log found at: {log_file}")
        return 0

    try:
        discoveries = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        log_entry = json.loads(line)
                        # Only import validated discoveries
                        if log_entry.get('validation_status') == 'validated':
                            discoveries.append(log_entry)
                    except json.JSONDecodeError:
                        continue

        print(f"Found {len(discoveries)} validated discoveries in log file")

        # Store to memory palace
        stored = retroactively_store_discoveries(discoveries)
        print(f"Successfully stored {stored}/{len(discoveries)} discoveries to memory palace")

        return stored

    except Exception as e:
        print(f"Error importing discoveries: {e}")
        return 0


def verify_memory_palace_structure():
    """Verify memory palace structure is correct"""
    print("=== Verifying Memory Palace Structure ===\n")

    # Check memory palace path exists
    if not os.path.exists(MEMORY_PALACE_PATH):
        print(f"❌ Memory palace path does not exist: {MEMORY_PALACE_PATH}")
        print("   Creating it now...")
        os.makedirs(MEMORY_PALACE_PATH, exist_ok=True)
        print(f"✅ Created memory palace path")

    # Check MEMORY.md exists
    memory_index = os.path.join(MEMORY_PALACE_PATH, "MEMORY.md")
    if not os.path.exists(memory_index):
        print(f"❌ MEMORY.md does not exist")
        print("   Creating it now...")
        with open(memory_index, 'w', encoding='utf-8') as f:
            f.write("# BIODISC Memory Index\n\n")
            f.write("This file indexes all memory entries for the BIODISC project.\n")
            f.write("Each memory is stored in its own file with frontmatter.\n\n")
        print(f"✅ Created MEMORY.md")
    else:
        print(f"✅ MEMORY.md exists")

    # Check for write permissions
    if os.access(MEMORY_PALACE_PATH, os.W_OK):
        print(f"✅ Write permissions OK")
    else:
        print(f"❌ No write permissions to {MEMORY_PALACE_PATH}")

    print(f"\nMemory palace structure verified at: {MEMORY_PALACE_PATH}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="V73 Memory Palace Integration Tools")
    parser.add_argument('action', choices=['status', 'test', 'import', 'verify'],
                       help="Action to perform")

    args = parser.parse_args()

    if args.action == 'status':
        show_discovery_status()
    elif args.action == 'test':
        test_memory_palace_integration()
    elif args.action == 'import':
        import_discoveries_from_log()
    elif args.action == 'verify':
        verify_memory_palace_structure()
