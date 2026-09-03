"""
V73 Memory Palace Integration - Automatic Discovery Storage

Ensures all autonomous discoveries are automatically stored in the memory palace
for persistence across sessions and continuity of learning.

INTEGRATION:
- V73 Autonomous Discovery → Memory Palace
- Automatic storage on validated discoveries
- Proper formatting and indexing
- Cross-session persistence

Date: 2026-04-26
Version: 1.0.0
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Import memory palace path
MEMORY_PALACE_PATH = str(Path(__file__).parent.parent / "data" / "memory")


@dataclass
class MemoryPalaceEntry:
    """An entry in the memory palace"""
    filename: str
    title: str
    category: str  # user, feedback, project, reference, discovery
    description: str
    content: str
    timestamp: str
    tags: List[str] = field(default_factory=list)


class DiscoveryMemoryFormatter:
    """
    Format autonomous discoveries for memory palace storage.

    Ensures discoveries follow the memory palace format and are
    properly indexed for retrieval.
    """

    def format_discovery(self, discovery: Dict[str, Any]) -> MemoryPalaceEntry:
        """
        Format a discovery from autonomous discovery system into memory palace entry.

        DISCOVERY FORMAT:
        {
            'id': str,
            'question': str,
            'discovery': str,
            'confidence': float,
            'evidence': List[str],
            'timestamp': float,
            'validation_status': str,
            'impact_estimate': float
        }
        """
        # Generate filename from discovery ID and timestamp
        timestamp_str = datetime.fromtimestamp(discovery['timestamp']).strftime("%Y%m%d_%H%M%S")
        filename = f"discovery_{discovery['id']}_{timestamp_str}.md"

        # Generate title from question
        question = discovery['question']
        title = question[:80] + "..." if len(question) > 80 else question

        # Determine category based on question type
        question_lower = question.lower()
        if 'meta' in question_lower or 'improve' in question_lower or 'capability' in question_lower:
            category = "discovery_meta"  # Meta-discoveries about system improvement
        elif 'connection' in question_lower or 'between' in question_lower:
            category = "discovery_cross_domain"  # Cross-domain connections
        elif 'mechanism' in question_lower or 'how' in question_lower or 'why' in question_lower:
            category = "discovery_mechanism"  # Mechanistic discoveries
        else:
            category = "discovery_general"  # General discoveries

        # Format content as markdown with frontmatter
        content = f"""---
name: {discovery['id']}
description: {title}
type: discovery
category: {category}
confidence: {discovery['confidence']:.2f}
validated: {discovery['validation_status']}
impact: {discovery.get('impact_estimate', 0.0):.2f}
---

# Autonomous Discovery: {discovery['id']}

**Question**: {discovery['question']}

**Discovery**: {discovery['discovery']}

## Details

- **Confidence**: {discovery['confidence']:.2f}
- **Validation Status**: {discovery['validation_status']}
- **Impact Estimate**: {discovery.get('impact_estimate', 0.0):.2f}
- **Timestamp**: {datetime.fromtimestamp(discovery['timestamp']).isoformat()}

## Evidence

"""

        # Add evidence if present
        evidence = discovery.get('evidence', [])
        if evidence:
            for i, e in enumerate(evidence, 1):
                content += f"{i}. {e}\n"
        else:
            content += "No specific evidence sources recorded.\n"

        # Generate tags
        tags = self._generate_tags(discovery)

        # Create entry
        entry = MemoryPalaceEntry(
            filename=filename,
            title=title,
            category=category,
            description=f"Autonomous discovery: {title}",
            content=content,
            timestamp=datetime.fromtimestamp(discovery['timestamp']).isoformat(),
            tags=tags
        )

        return entry

    def _generate_tags(self, discovery: Dict[str, Any]) -> List[str]:
        """Generate tags for discovery"""
        tags = ["autonomous_discovery", "v73"]

        question_lower = discovery['question'].lower()

        # Add type-specific tags
        if 'meta' in question_lower:
            tags.append("meta_discovery")
        if 'connection' in question_lower or 'between' in question_lower:
            tags.append("cross_domain")
        if 'mechanism' in question_lower:
            tags.append("mechanism")
        if 'improve' in question_lower or 'efficiency' in question_lower:
            tags.append("improvement")

        # Add domain tags
        domains = ['biology', 'physics', 'chemistry', 'mathematics', 'evolution']
        for domain in domains:
            if domain in question_lower:
                tags.append(domain)

        return tags


class MemoryPalaceStorage:
    """
    Handle storage of autonomous discoveries to memory palace.

    ENSURES:
    - All validated discoveries are stored
    - Proper formatting and indexing
    - MEMORY.md is updated
    - Cross-session persistence
    """

    def __init__(self, memory_palace_path: str = MEMORY_PALACE_PATH):
        self.memory_palace_path = memory_palace_path
        self.formatter = DiscoveryMemoryFormatter()
        self.memory_index_path = os.path.join(memory_palace_path, "MEMORY.md")

    def store_discovery(self, discovery: Dict[str, Any]) -> bool:
        """
        Store a discovery in the memory palace.

        Returns True if successfully stored.
        """
        try:
            # Format discovery for memory palace
            entry = self.formatter.format_discovery(discovery)

            # Write discovery file
            discovery_path = os.path.join(self.memory_palace_path, entry.filename)
            with open(discovery_path, 'w', encoding='utf-8') as f:
                f.write(entry.content)

            # Update MEMORY.md index
            self._update_memory_index(entry)

            return True

        except Exception as e:
            print(f"Error storing discovery to memory palace: {e}")
            return False

    def _update_memory_index(self, entry: MemoryPalaceEntry):
        """Update MEMORY.md with new discovery entry"""
        try:
            # Read existing MEMORY.md
            if os.path.exists(self.memory_index_path):
                with open(self.memory_index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "# BIODISC Memory Index\n\nThis file indexes all memory entries.\n"

            # Add new entry under "Autonomous Discoveries" section
            new_entry = f"- [{entry.title}]({entry.filename}) — {entry.description} (confidence: {entry.tags[1] if len(entry.tags) > 1 else 'N/A'})\n"

            # Check if "Autonomous Discoveries" section exists
            if "## Autonomous Discoveries" in content:
                # Add to existing section
                content = content.replace(
                    "## Autonomous Discoveries",
                    f"## Autonomous Discoveries\n{new_entry}"
                )
            else:
                # Create new section
                content += f"\n## Autonomous Discoveries\n\n{new_entry}"

            # Write updated index
            with open(self.memory_index_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception as e:
            print(f"Error updating memory index: {e}")

    def store_discoveries_batch(self, discoveries: List[Dict[str, Any]]) -> int:
        """
        Store multiple discoveries in batch.

        Returns number of successfully stored discoveries.
        """
        stored = 0
        for discovery in discoveries:
            if self.store_discovery(discovery):
                stored += 1
        return stored

    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get summary of discoveries stored in memory palace"""
        try:
            if not os.path.exists(self.memory_index_path):
                return {'total': 0, 'by_category': {}}

            with open(self.memory_index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count discoveries (simplified - would parse properly)
            discovery_count = content.count("autonomous_discovery")

            return {
                'total': discovery_count,
                'last_updated': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error getting discovery summary: {e}")
            return {'total': 0, 'error': str(e)}


class AutomaticMemoryPalaceIntegration:
    """
    Automatic integration between V73 Autonomous Discovery and Memory Palace.

    ENSURES:
    - Every validated discovery is automatically stored
    - No manual intervention required
    - Continuous accumulation of discoveries
    - Cross-session persistence

    USAGE:
    - Automatically called by V73 Autonomous Discovery Orchestrator
    - Can be called manually to retroactively store discoveries
    """

    def __init__(self):
        self.storage = MemoryPalaceStorage()
        self.last_storage_time = None
        self.storage_count = 0

    def auto_store_discovery(self, discovery: Dict[str, Any]) -> bool:
        """
        Automatically store discovery to memory palace.

        Called automatically by V73 when discovery is validated.
        """
        # Only store validated discoveries
        if discovery.get('validation_status') != 'validated':
            return False

        # Store to memory palace
        success = self.storage.store_discovery(discovery)

        if success:
            self.last_storage_time = datetime.now()
            self.storage_count += 1
            print(f"Discovery {discovery['id']} stored to memory palace")

        return success

    def auto_store_discoveries(self, discoveries: List[Dict[str, Any]]) -> int:
        """
        Automatically store multiple discoveries.

        Returns count of successfully stored.
        """
        stored = 0
        for discovery in discoveries:
            if self.auto_store_discovery(discovery):
                stored += 1
        return stored

    def get_status(self) -> Dict[str, Any]:
        """Get status of memory palace integration"""
        return {
            'total_stored': self.storage_count,
            'last_storage_time': self.last_storage_time.isoformat() if self.last_storage_time else None,
            'memory_palace_path': MEMORY_PALACE_PATH,
            'summary': self.storage.get_discovery_summary()
        }


# Global instance for automatic integration
_global_integration = None

def get_automatic_memory_integration() -> AutomaticMemoryPalaceIntegration:
    """Get global automatic memory palace integration instance"""
    global _global_integration
    if _global_integration is None:
        _global_integration = AutomaticMemoryPalaceIntegration()
    return _global_integration


def auto_store_discovery_to_memory_palace(discovery: Dict[str, Any]) -> bool:
    """
    Convenience function to automatically store discovery to memory palace.

    This is called automatically by V73 Autonomous Discovery Orchestrator
    whenever a validated discovery is made.
    """
    integration = get_automatic_memory_integration()
    return integration.auto_store_discovery(discovery)


def retroactively_store_discoveries(discoveries: List[Dict[str, Any]]) -> int:
    """
    Retroactively store existing discoveries to memory palace.

    Use this to migrate discoveries made before memory palace integration
    was set up.
    """
    integration = get_automatic_memory_integration()
    return integration.auto_store_discoveries(discoveries)


if __name__ == "__main__":
    # Test the integration with a sample discovery
    sample_discovery = {
        'id': 'test_discovery_001',
        'question': 'What connections exist between membrane physics and gene regulation?',
        'discovery': 'Exploration of cross-domain connection between membrane physical properties and genetic regulatory mechanisms. Potential for novel regulatory coupling where membrane state influences gene expression patterns.',
        'confidence': 0.96,
        'evidence': [
            'Membrane curvature affects division site selection',
            'Cardiolipin domains correlate with certain gene expression patterns',
            'Physical stress can trigger transcriptional responses'
        ],
        'timestamp': datetime.now().timestamp(),
        'validation_status': 'validated',
        'impact_estimate': 0.7
    }

    integration = get_automatic_memory_integration()
    success = integration.auto_store_discovery(sample_discovery)

    print(f"Storage test: {'SUCCESS' if success else 'FAILED'}")
    print(f"Status: {integration.get_status()}")
