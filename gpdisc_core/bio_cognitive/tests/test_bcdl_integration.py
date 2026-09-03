"""
Comprehensive integration tests for Bio-Cognitive Discovery Layer (BCDL)

Tests all 5 modules working together:
1. Abductive Theory Former
2. Temporal Causal Discovery
3. Multi-Scale Reasoner
4. Experimental Designer
5. Discovery Value Calculator

Date: 2026-04-22
Version: 1.0.0
"""

import sys
import os
import logging
import numpy as np
from typing import Dict, Any, List


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BCDLTestRunner:
    """Test runner for BCDL integration tests"""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def run_test(self, test_name: str, test_func):
        """Run a single test"""
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Running: {test_name}")
            logger.info('='*60)

            result = test_func()

            if result.get('passed', False):
                self.tests_passed += 1
                status = "PASSED"
                logger.info(f"✓ {test_name}: PASSED")
            else:
                self.tests_failed += 1
                status = "FAILED"
                logger.error(f"✗ {test_name}: FAILED - {result.get('error', 'Unknown error')}")

            self.results.append({
                'name': test_name,
                'status': status,
                'result': result
            })

        except Exception as e:
            self.tests_failed += 1
            logger.error(f"✗ {test_name}: FAILED with exception - {str(e)}")
            import traceback
            traceback.print_exc()

            self.results.append({
                'name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    def print_summary(self):
        """Print test summary"""
        total = self.tests_passed + self.tests_failed
        logger.info(f"\n{'='*60}")
        logger.info("BCDL INTEGRATION TEST SUMMARY")
        logger.info('='*60)
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {self.tests_passed}")
        logger.info(f"Failed: {self.tests_failed}")
        logger.info(f"Success Rate: {100 * self.tests_passed / total:.1f}%")
        logger.info('='*60)

        return self.tests_failed == 0


# ============================================================================
# TEST 1: Module Imports
# ============================================================================

def test_module_imports():
    """Test that all BCDL modules can be imported"""
    try:
        from gpdisc_core.bio_cognitive import (
            BioCognitiveDiscoveryLayer,
            create_bio_cognitive_layer,
            ABDUCTIVE_THEORY_FORMER_AVAILABLE,
            TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE,
            MULTI_SCALE_REASONER_AVAILABLE,
            EXPERIMENTAL_DESIGNER_AVAILABLE,
            DISCOVERY_VALUE_CALCULATOR_AVAILABLE
        )

        # Check availability flags
        assert ABDUCTIVE_THEORY_FORMER_AVAILABLE, "Abductive Theory Former not available"
        assert TEMPORAL_CAUSAL_DISCOVERY_AVAILABLE, "Temporal Causal Discovery not available"
        assert MULTI_SCALE_REASONER_AVAILABLE, "Multi-Scale Reasoner not available"
        assert EXPERIMENTAL_DESIGNER_AVAILABLE, "Experimental Designer not available"
        assert DISCOVERY_VALUE_CALCULATOR_AVAILABLE, "Discovery Value Calculator not available"

        logger.info("✓ All 5 BCDL modules imported successfully")
        return {'passed': True}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 2: Abductive Theory Former
# ============================================================================

def test_abductive_theory_former():
    """Test Abductive Theory Former functionality"""
    try:
        from gpdisc_core.bio_cognitive import AbductiveTheoryFormer

        # Create instance
        atf = AbductiveTheoryFormer({})

        # Test hypothesis generation
        query = "What causes protein misfolding in neurodegenerative diseases?"
        hypotheses = atf.generate_hypotheses(query)

        assert len(hypotheses) > 0, "No hypotheses generated"
        assert all(hasattr(h, 'statement') for h in hypotheses), "Hypotheses missing statement"

        logger.info(f"✓ Generated {len(hypotheses)} hypotheses")
        for i, h in enumerate(hypotheses[:3]):
            logger.info(f"  H{i+1}: {h.statement[:80]}...")

        # Test knowledge gap identification
        gaps = atf.identify_gaps(query)
        assert len(gaps) > 0, "No knowledge gaps identified"
        logger.info(f"✓ Identified {len(gaps)} knowledge gaps")

        # Test theory synthesis
        theory = atf.synthesize_theory(query, {}, hypotheses)
        assert theory is not None, "Theory synthesis failed"
        logger.info(f"✓ Synthesized theory: {theory.title[:80]}...")

        return {'passed': True, 'hypotheses_count': len(hypotheses), 'gaps_count': len(gaps)}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 3: Temporal Causal Discovery
# ============================================================================

def test_temporal_causal_discovery():
    """Test Temporal Causal Discovery functionality"""
    try:
        from gpdisc_core.bio_cognitive import TemporalCausalDiscovery

        # Create instance
        tcd = TemporalCausalDiscovery({})

        # Generate synthetic time-series data
        np.random.seed(42)
        n_samples = 100
        n_vars = 3

        data = {
            'gene_A': np.random.randn(n_samples),
            'gene_B': np.random.randn(n_samples),
            'gene_C': np.random.randn(n_samples)
        }

        # Add causal relationship: A -> B
        for i in range(1, n_samples):
            data['gene_B'][i] += 0.5 * data['gene_A'][i-1]

        # Test causal learning
        causal_graph = tcd.learn_from_data(data, method='granger')

        assert causal_graph is not None, "Causal graph not learned"
        logger.info(f"✓ Learned causal graph with {len(causal_graph.nodes)} nodes")

        # Test dynamic system modeling
        model = tcd.model_dynamics(data)
        assert model is not None, "Dynamic model not created"
        logger.info(f"✓ Created dynamic system model")

        # Test state prediction
        predictions = tcd.predict_future_state(data, steps=5)
        assert predictions is not None, "State prediction failed"
        logger.info(f"✓ Generated {len(predictions)} state predictions")

        # Test intervention optimization
        intervention = tcd.optimize_intervention(data, target='gene_B')
        assert intervention is not None, "Intervention optimization failed"
        logger.info(f"✓ Optimized intervention: {intervention.recommended_action}")

        return {'passed': True, 'nodes': len(causal_graph.nodes)}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 4: Multi-Scale Reasoner
# ============================================================================

def test_multi_scale_reasoner():
    """Test Multi-Scale Reasoner functionality"""
    try:
        from gpdisc_core.bio_cognitive import MultiScaleReasoner

        # Create instance
        msr = MultiScaleReasoner({})

        # Test cross-scale reasoning
        query = "How do mitochondrial DNA mutations affect cellular metabolism and tissue function?"
        result = msr.reason_across_scales(query)

        assert result is not None, "Multi-scale reasoning failed"
        logger.info(f"✓ Performed multi-scale reasoning")

        # Check for scale mappings
        if 'scale_maps' in result:
            logger.info(f"✓ Generated {len(result['scale_maps'])} scale mappings")

        # Check for emergent properties
        if 'emergent_properties' in result:
            logger.info(f"✓ Identified {len(result['emergent_properties'])} emergent properties")

        # Test perturbation propagation
        perturbation = msr.propagate_perturbation(
            scale='molecular',
            perturbation_type='mutation',
            target='mitochondrial DNA'
        )
        assert perturbation is not None, "Perturbation propagation failed"
        logger.info(f"✓ Propagated perturbation across {len(perturbation.path)} scales")

        # Test scale-invariant mechanism detection
        mechanisms = msr.find_scale_invariant_mechanisms(query)
        assert mechanisms is not None, "Scale-invariant mechanism detection failed"
        logger.info(f"✓ Found {len(mechanisms)} scale-invariant mechanisms")

        return {'passed': True}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 5: Experimental Designer
# ============================================================================

def test_experimental_designer():
    """Test Experimental Designer functionality"""
    try:
        from gpdisc_core.bio_cognitive import ExperimentalDesigner

        # Create instance
        ed = ExperimentalDesigner({})

        # Design experiment
        hypothesis = "Inhibition of protein X aggregation reduces cellular toxicity in neurodegenerative disease models"
        design = ed.design_experiment(hypothesis, optimize=True, predict_outcomes=True)

        assert design is not None, "Experimental design failed"
        logger.info(f"✓ Generated experimental design")

        # Check protocol
        protocol = design['protocol']
        assert protocol is not None, "Protocol not generated"
        logger.info(f"✓ Protocol: {protocol.protocol_id}")
        logger.info(f"  Type: {protocol.experimental_type.value}")
        logger.info(f"  Duration: {protocol.duration['total']} hours")

        # Check optimization
        if design['optimization']['optimized']:
            logger.info(f"✓ Information gain optimized: {design['optimization']['information_gain']:.3f}")

        # Check controls
        controls = design['controls']
        logger.info(f"✓ Generated {len(controls)} control experiments")

        # Check outcome prediction
        outcome_pred = design['outcome_prediction']
        if outcome_pred:
            logger.info(f"✓ Predicted {len(outcome_pred.predicted_outcomes)} outcomes")

        return {'passed': True, 'controls': len(controls)}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 6: Discovery Value Calculator
# ============================================================================

def test_discovery_value_calculator():
    """Test Discovery Value Calculator functionality"""
    try:
        from gpdisc_core.bio_cognitive import DiscoveryValueCalculator

        # Create instance
        dvc = DiscoveryValueCalculator({})

        # Create mock discovery results
        discovery_results = {
            'hypotheses': [
                {'statement': 'H1', 'novelty_score': 0.8},
                {'statement': 'H2', 'novelty_score': 0.6}
            ],
            'multi_scale_insights': [
                {'description': 'Cross-scale mechanism', 'scale': 'molecular_to_cellular'}
            ]
        }

        # Prioritize research
        priorities = dvc.prioritize_research(
            query="protein misfolding mechanisms",
            discovery_results=discovery_results,
            context={'constraints': {'budget': 100000, 'time': 1.0}}
        )

        assert priorities is not None, "Research prioritization failed"
        logger.info(f"✓ Prioritized research directions")

        # Check priorities
        if 'priorities' in priorities:
            logger.info(f"✓ Generated {len(priorities['priorities'])} priority rankings")
            for i, p in enumerate(priorities['priorities'][:3]):
                logger.info(f"  {i+1}. {p['priority'].title[:60]}... (score: {p['priority'].overall_priority_score:.3f})")

        # Check resource allocation if present
        if 'resource_allocation' in priorities:
            alloc = priorities['resource_allocation']
            logger.info(f"✓ Funded {len(alloc.funded_priorities)} priorities")

        return {'passed': True}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 7: Full BCDL Discovery Pipeline
# ============================================================================

def test_full_bcdl_discovery():
    """Test complete BCDL discovery pipeline"""
    try:
        from gpdisc_core.bio_cognitive import BioCognitiveDiscoveryLayer

        # Create BCDL layer
        bcdl = BioCognitiveDiscoveryLayer({})

        logger.info(f"✓ BCDL layer initialized")
        logger.info(f"  Status: {bcdl.get_status()}")
        logger.info(f"  Capabilities: {len(bcdl.get_capabilities())}")

        # Run discovery
        query = "What molecular mechanisms underlie protein misfolding in Alzheimer's disease?"
        context = {
            'constraints': {'budget': 150000, 'time': 2.0},
            'available_techniques': ['rnaseq', 'microscopy', 'crispr']
        }

        results = bcdl.discover(query, context=context, mode='full')

        logger.info(f"✓ Discovery pipeline completed")
        logger.info(f"  Hypotheses: {len(results.get('hypotheses', []))}")
        logger.info(f"  Knowledge gaps: {len(results.get('knowledge_gaps', []))}")
        logger.info(f"  Experimental designs: {len(results.get('experimental_designs', []))}")
        logger.info(f"  Research priorities: {len(results.get('research_priorities', []))}")

        # Verify synthesis
        if results.get('synthesis'):
            logger.info(f"✓ Theory synthesis: {results['synthesis'].title}")

        return {'passed': True, 'results': results}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# TEST 8: Cross-Module Integration
# ============================================================================

def test_cross_module_integration():
    """Test integration between BCDL modules"""
    try:
        from gpdisc_core.bio_cognitive import (
            AbductiveTheoryFormer,
            ExperimentalDesigner,
            DiscoveryValueCalculator
        )

        # Create modules
        atf = AbductiveTheoryFormer({})
        ed = ExperimentalDesigner({})
        dvc = DiscoveryValueCalculator({})

        # Generate hypotheses
        query = "How does autophagy regulate protein aggregate clearance?"
        hypotheses = atf.generate_hypotheses(query)

        # Design experiment for top hypothesis
        if hypotheses:
            top_hypothesis = hypotheses[0].statement
            design = ed.design_experiment(top_hypothesis)

            # Prioritize based on design
            discovery_results = {
                'hypotheses': [{'statement': h.statement, 'novelty_score': h.novelty_score}
                              for h in hypotheses]
            }

            priorities = dvc.prioritize_research(
                query, discovery_results,
                context={'constraints': {'budget': 100000, 'time': 1.0}}
            )

            logger.info(f"✓ Cross-module integration successful")
            logger.info(f"  Hypotheses → Experimental Design → Prioritization")

            return {'passed': True}

        return {'passed': False, 'error': 'No hypotheses generated'}

    except Exception as e:
        return {'passed': False, 'error': str(e)}


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    """Run all BCDL integration tests"""
    logger.info("="*60)
    logger.info("BCDL INTEGRATION TESTS")
    logger.info("Testing all 5 modules of Bio-Cognitive Discovery Layer")
    logger.info("="*60)

    runner = BCDLTestRunner()

    # Run all tests
    runner.run_test("Module Imports", test_module_imports)
    runner.run_test("Abductive Theory Former", test_abductive_theory_former)
    runner.run_test("Temporal Causal Discovery", test_temporal_causal_discovery)
    runner.run_test("Multi-Scale Reasoner", test_multi_scale_reasoner)
    runner.run_test("Experimental Designer", test_experimental_designer)
    runner.run_test("Discovery Value Calculator", test_discovery_value_calculator)
    runner.run_test("Full BCDL Discovery Pipeline", test_full_bcdl_discovery)
    runner.run_test("Cross-Module Integration", test_cross_module_integration)

    # Print summary
    all_passed = runner.print_summary()

    if all_passed:
        logger.info("\n🎉 ALL BCDL INTEGRATION TESTS PASSED! 🎉")
        return 0
    else:
        logger.error("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    exit(main())
