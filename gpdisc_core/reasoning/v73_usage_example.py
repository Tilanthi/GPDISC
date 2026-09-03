"""
V73 Autonomous Discovery - Usage Example and Integration

This file demonstrates how to use the autonomous discovery system
and how to integrate it into GPDISC.

Date: 2026-04-26
Version: 1.0.0
"""

from gpdisc_core.reasoning.v73_autonomous_discovery import (
    AutonomousDiscoveryConfig,
    get_autonomous_discovery_system,
    update_user_activity
)


def example_basic_usage():
    """
    Basic usage example: Start autonomous discovery and monitor status.
    """
    print("=== V73 Autonomous Discovery - Basic Usage ===\n")

    # Create system with default config
    system = get_autonomous_discovery_system()

    # Start autonomous discovery (runs in background)
    print("Starting autonomous discovery...")
    system.start()
    print("Autonomous discovery is now running in background.")
    print("It will start exploring when system is idle for 5+ minutes.\n")

    # Simulate some activity
    print("Simulating user activity...")
    import time
    for i in range(3):
        time.sleep(2)
        print(f"  Activity {i+1} - updating activity timer")
        update_user_activity()  # Call this whenever user interacts

    # Check status
    print("\nChecking autonomous discovery status...")
    status = system.get_status()
    print(f"Status: {status['status']}")
    print(f"Running: {status['running']}")
    print(f"Total discoveries: {status['total_discoveries']}")
    print(f"Validated discoveries: {status['validated_discoveries']}")

    # Get recent discoveries
    print("\nRecent discoveries:")
    discoveries = system.get_discoveries(limit=5)
    for i, discovery in enumerate(discoveries, 1):
        print(f"\n  Discovery {i}:")
        print(f"    Question: {discovery['question']}")
        print(f"    Confidence: {discovery['confidence']:.2f}")
        print(f"    Validated: {discovery['validated']}")

    # Stop when done (optional - can leave running)
    print("\nStopping autonomous discovery...")
    system.stop()
    print("Autonomous discovery stopped.")


def example_custom_config():
    """
    Example with custom configuration for stricter safeguards.
    """
    print("\n=== V73 Autonomous Discovery - Custom Config ===\n")

    # Create custom config with strict safeguards
    config = AutonomousDiscoveryConfig(
        # Resource limits - very conservative
        max_cpu_percent=5.0,  # Max 5% CPU
        max_hours_per_week=2.0,  # Max 2 hours per week
        idle_timeout_minutes=10,  # Start after 10 minutes idle

        # Validation thresholds - very high
        min_confidence_to_store=0.98,  # 98%+ confidence
        min_evidence_count=3,  # At least 3 evidence sources

        # Scope control - focus on biology only
        allowed_domains=["biology", "molecular_biology", "cell_biology"],
        forbidden_domains=["medical", "clinical"],  # Exclude clinical

        # Ethical safeguards
        require_human_review_for_capability_changes=True,
        max_self_modifications_per_session=1,

        # Transparency
        log_all_discoveries=True,
        discovery_log_path="/tmp/gpdisc_discoveries_strict.jsonl"
    )

    system = get_autonomous_discovery_system(config)

    print("Created autonomous discovery system with strict safeguards:")
    print(f"  Max CPU: {config.max_cpu_percent}%")
    print(f"  Max hours/week: {config.max_hours_per_week}")
    print(f"  Min confidence: {config.min_confidence_to_store}")
    print(f"  Allowed domains: {config.allowed_domains}")
    print(f"  Human review required: {config.require_human_review_for_capability_changes}")


def example_integration_with_biodisc():
    """
    Example of integrating autonomous discovery into GPDISC workflow.
    """
    print("\n=== V73 Integration with BIODISC ===\n")

    # Get autonomous discovery system
    system = get_autonomous_discovery_system()

    # Start at system initialization
    print("1. Initialize autonomous discovery at BIODISC startup")
    system.start()

    # Update activity on user interactions
    print("2. Call update_user_activity() on each user interaction:")
    print("   - User sends message → update_user_activity()")
    print("   - User runs command → update_user_activity()")
    print("   - System processes query → update_user_activity()")

    # Periodically check for discoveries
    print("3. Periodically check for new discoveries:")
    print("   discoveries = system.get_discoveries(limit=10)")
    print("   for discovery in discoveries:")
    print("       if discovery['validated']:")
    print("           incorporate_into_knowledge_base(discovery)")

    # Review capability evolution requests
    print("4. Review meta-discoveries that suggest capability improvements:")
    print("   discoveries = system.get_discoveries()")
    print("   for d in discoveries:")
    print("       if 'meta' in d['question'].lower():")
    print("           review_capability_change(d)")

    # Clean shutdown
    print("5. On shutdown:")
    print("   system.stop()")


def example_monitoring_dashboard():
    """
    Example of how to create a monitoring dashboard.
    """
    print("\n=== V73 Monitoring Dashboard Example ===\n")

    system = get_autonomous_discovery_system()

    # Dashboard would show:
    dashboard = """
    =====================================
    BIODISC Autonomous Discovery Dashboard
    =====================================

    Status: {status}
    Running: {running}
    Paused: {paused}

    Resource Usage:
    - CPU Hours This Week: {cpu_hours:.2f} / {max_cpu_hours:.2f}
    - Last User Activity: {last_activity}

    Discovery Statistics:
    - Total Discoveries: {total}
    - Validated: {validated}
    - Pending Validation: {pending}

    Recent Discoveries:
    {discoveries}

    Controls:
    [Start] [Stop] [Pause] [Resume]
    [View Full Log] [Export Discoveries]
    =====================================
    """

    # Populate dashboard with current data
    status = system.get_status()
    print(dashboard.format(
        status=status['status'].upper(),
        running=status['running'],
        paused=status.get('paused', False),
        cpu_hours=status['weekly_cpu_hours'],
        max_cpu_hours=4.0,  # From config
        last_activity=status['last_activity'],
        total=status['total_discoveries'],
        validated=status['validated_discoveries'],
        pending=status['total_discoveries'] - status['validated_discoveries'],
        discoveries="\n".join([
            f"  - {d['question'][:60]}..."
            for d in status.get('recent_discoveries', [])
        ]) or "  (No discoveries yet)"
    ))


def example_curiosity_engine_usage():
    """
    Example of using the curiosity engine directly.
    """
    print("\n=== V73 Curiosity Engine Usage ===\n")

    from gpdisc_core.reasoning.v73_curiosity_engine import get_curiosity_engine

    # Get curiosity engine
    engine = get_curiosity_engine()

    # Generate questions from knowledge base
    print("Generating curiosity questions...")

    # In production, would pass actual knowledge base
    # For now, generates meta-questions
    questions = engine.generate_questions(knowledge_base={}, max_questions=5)

    print(f"\nGenerated {len(questions)} curiosity questions:\n")

    for i, question in enumerate(questions, 1):
        print(f"{i}. {question.question}")
        print(f"   Type: {question.question_type.value}")
        print(f"   Priority: {question.priority.value}")
        print(f"   Confidence: {question.confidence:.2f}")
        print(f"   Context: {question.context}")
        print(f"   Knowledge gap: {question.knowledge_gap}")
        print(f"   Potential discovery: {question.potential_discovery}")
        print()


# Integration hook for GPDISC initialization
def initialize_autonomous_discovery():
    """
    Call this when GPDISC initializes to start autonomous discovery.

    INTEGRATION POINT:
    Add this to gpdisc_core/__init__.py or main initialization code.
    """
    try:
        system = get_autonomous_discovery_system()
        system.start()
        print("Autonomous discovery initialized and running in background")
        return system
    except Exception as e:
        print(f"Failed to initialize autonomous discovery: {e}")
        return None


# Activity tracking hook
def track_user_activity():
    """
    Call this whenever user interacts with GPDISC.

    INTEGRATION POINT:
    Add this to all user interaction points in GPDISC.
    """
    update_user_activity()


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_custom_config()
    example_integration_with_biodisc()
    example_monitoring_dashboard()
    example_curiosity_engine_usage()

    print("\n=== All Examples Complete ===")
