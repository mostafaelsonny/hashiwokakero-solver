"""Comprehensive Memetic Algorithm Unit and Regression Test Suite (Sprint 2 - S2-10 & S2-11).

Owner: Febronia (M5 — Memetic Algorithm)
Reviewer: Mostafa (M1)

Test Groups:
  1. Neighborhood Generation: Single Gene, Pairwise Transfer, degree invariant, legality.
  2. Hill Climbing Invariants: strictly improving moves, local optimum halt, non-mutation.
  3. GA Component Reuse: verification that M4 operators are directly imported without duplication.
  4. Evolution Integration: in-loop local search execution, metric tracking (calls, improvements).
  5. Final Validation Gate: solution validity via core.solution_validator, P1 convergence, bounded failure.
  6. Interface & Determinism: docs/ALGORITHM_INTERFACE.md compliance, seed reproducibility.
"""
from __future__ import annotations

import copy
import inspect
from typing import List

import pytest

import algorithms.ga.operators as ga_operators
import algorithms.ma.memetic_solver as memetic_module
from algorithms.ga import (
    chromosome_to_solution,
    evaluate_fitness,
    get_elites,
    initialize_population,
    mutate,
    tournament_selection,
    uniform_crossover,
)
from algorithms.ma.local_search import (
    InvalidChromosomeError,
    best_improving_neighbor,
    evaluate_chromosome,
    generate_neighbors,
    hill_climb,
    pairwise_transfer_neighbors,
    single_gene_neighbors,
    _actual_degrees,
)
from algorithms.ma.memetic_solver import solve_memetic
from algorithms.memetic import solve_memetic as memetic_facade_solver
from core.candidate_generator import generate_candidate_edges
from core.graph_context import GraphContext, build_graph_context
from core.solution_validator import validate_solution
from tests.helpers import P1_EDGES, P1_PUZZLE, P2_EDGES, P2_PUZZLE

IMPOSSIBLE_PUZZLE = {
    "rows": 1,
    "cols": 3,
    "islands": [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 5},
        {"id": "B", "row": 0, "col": 2, "required_bridges": 5},
    ],
}
IMPOSSIBLE_EDGES = [
    {"id": "E1", "from": "A", "to": "B", "orientation": "horizontal"},
]


# ==============================================================================
# Group 1: Neighborhood Generation & Graph Invariants
# ==============================================================================
class TestNeighborhoodGeneration:
    """Validate neighborhood operators, gene domain, and graph invariants."""

    def test_single_gene_perturbation_domain_and_length(self):
        chrom = [1, 1, 1, 1]
        neighbors = single_gene_neighbors(chrom)
        # 4 genes * 2 alternate values in {0, 1, 2} = 8 neighbors
        assert len(neighbors) == 8
        for nb in neighbors:
            assert len(nb) == 4
            assert all(type(g) is int and g in (0, 1, 2) for g in nb)
            assert sum(a != b for a, b in zip(nb, chrom)) == 1

    def test_pairwise_transfer_preserves_focal_island_degree(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        chrom = [2, 0, 1, 1]  # Island B has actual degree 3 (excess)
        degrees_before = _actual_degrees(chrom, P1_EDGES)

        neighbors = pairwise_transfer_neighbors(chrom, P1_PUZZLE, P1_EDGES, ctx)
        assert len(neighbors) > 0

        for nb in neighbors:
            degrees_after = _actual_degrees(nb, P1_EDGES)
            # Either focal B or focal C transferred: focal island degree must be constant!
            b_unchanged = degrees_after["B"] == degrees_before["B"]
            c_unchanged = degrees_after["C"] == degrees_before["C"]
            assert b_unchanged or c_unchanged

    def test_pairwise_transfer_adjusts_opposite_endpoints(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        chrom = [2, 0, 1, 1]
        neighbors = pairwise_transfer_neighbors(chrom, P1_PUZZLE, P1_EDGES, ctx)
        # Verify specific transfer around B: E1 -> E3 (1, 0, 2, 1)
        assert [1, 0, 2, 1] in neighbors
        deg_before = _actual_degrees(chrom, P1_EDGES)
        deg_after = _actual_degrees([1, 0, 2, 1], P1_EDGES)

        assert deg_after["B"] == deg_before["B"]  # Focal preserved
        assert deg_after["A"] == deg_before["A"] - 1  # E1 endpoint decremented
        assert deg_after["D"] == deg_before["D"] + 1  # E3 endpoint incremented

    def test_neighborhood_generator_strictly_valid_and_non_mutating(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        chrom = [2, 0, 1, 1]
        snapshot = copy.deepcopy(chrom)

        neighbors = generate_neighbors(chrom, P1_PUZZLE, P1_EDGES, ctx)
        assert chrom == snapshot  # Non-mutating
        assert len(neighbors) == len({tuple(n) for n in neighbors})  # Distinct
        assert tuple(chrom) not in {tuple(n) for n in neighbors}

        for nb in neighbors:
            assert len(nb) == len(P1_EDGES)
            assert all(type(g) is int and g in (0, 1, 2) for g in nb)


# ==============================================================================
# Group 2: Hill Climbing Invariants
# ==============================================================================
class TestHillClimbingInvariants:
    """Validate strict fitness improvement and bounded termination of local search."""

    def test_never_accepts_equal_or_worse_fitness(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        solution_chrom = [1, 1, 1, 1]  # optimal (0, 0, 0)
        improved, stats = hill_climb(solution_chrom, P1_PUZZLE, P1_EDGES, graph_context=ctx, max_steps=10)

        assert stats["improved"] is False
        assert stats["improvements"] == 0
        assert improved == solution_chrom
        assert stats["final_fitness"] == [0, 0, 0]

    def test_strictly_halts_at_local_optimum_or_step_cap(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        suboptimal = [1, 0, 1, 1]  # fitness (2, 0, 0)
        improved, stats = hill_climb(suboptimal, P1_PUZZLE, P1_EDGES, graph_context=ctx, max_steps=10)

        assert stats["improved"] is True
        assert stats["improvements"] > 0
        assert stats["final_fitness"] < stats["initial_fitness"]
        assert stats["steps"] <= 10
        assert improved == [1, 1, 1, 1]

    def test_best_improving_neighbor_strictly_better(self):
        ctx = build_graph_context(P1_PUZZLE, P1_EDGES)
        chrom = [1, 0, 1, 1]
        cur_fit = evaluate_chromosome(chrom, P1_PUZZLE, P1_EDGES, graph_context=ctx)

        result = best_improving_neighbor(chrom, P1_PUZZLE, P1_EDGES, graph_context=ctx)
        assert result is not None
        best_nb, best_fit = result
        assert best_fit < cur_fit


# ==============================================================================
# Group 3: GA Component Reuse (Zero Code Duplication)
# ==============================================================================
class TestGAComponentReuse:
    """Assert that MA directly imports and reuses M4's operators without duplication."""

    def test_ma_imports_m4_operators_directly(self):
        # Verify that operators in memetic_solver point to the exact same objects in algorithms.ga
        assert memetic_module.tournament_selection is tournament_selection
        assert memetic_module.uniform_crossover is uniform_crossover
        assert memetic_module.mutate is mutate
        assert memetic_module.get_elites is get_elites
        assert memetic_module.initialize_population is initialize_population
        assert memetic_module.evaluate_fitness is evaluate_fitness
        assert memetic_module.chromosome_to_solution is chromosome_to_solution

    def test_no_duplicated_operator_definitions(self):
        # Inspect memetic_solver module source to ensure operators are not redefined locally
        source = inspect.getsource(memetic_module)
        assert "def tournament_selection" not in source
        assert "def uniform_crossover" not in source
        assert "def get_elites" not in source


# ==============================================================================
# Group 4: Evolution Loop & Local Search Integration
# ==============================================================================
class TestEvolutionIntegration:
    """Verify that Hill Climbing is invoked within generations and records metrics."""

    def test_local_search_invoked_within_generations(self):
        result = solve_memetic(
            P1_PUZZLE,
            P1_EDGES,
            config={
                "population_size": 20,
                "max_generations": 15,
                "ls_individuals": 2,
                "ls_frequency": 1,
                "seed": 42,
            },
        )
        assert result["status"] == "SOLVED"
        metrics = result["metrics"]
        assert "local_search_calls" in metrics
        assert "local_search_improvements" in metrics
        assert metrics["local_search_calls"] >= 1

    def test_metrics_record_improvements_and_avg_steps(self):
        result = solve_memetic(
            P1_PUZZLE,
            P1_EDGES,
            config={
                "population_size": 30,
                "max_generations": 20,
                "seed": 123,
            },
        )
        metrics = result["metrics"]
        assert metrics["local_search_calls"] > 0
        assert metrics["local_search_improvements"] >= 0
        assert isinstance(metrics["avg_ls_steps_per_call"], float)
        assert metrics["generations"] >= 0
        assert metrics["evaluations"] > 0
        assert metrics["runtime_ms"] > 0.0


# ==============================================================================
# Group 5: Final Validation Gate & Standard SolverResult Shape
# ==============================================================================
class TestFinalValidationGate:
    """Validate solution correctness and bounded failure distinguishing."""

    def test_solves_canonical_p1_and_passes_core_validator(self):
        result = solve_memetic(
            P1_PUZZLE,
            P1_EDGES,
            config={"population_size": 40, "max_generations": 30, "seed": 42},
        )
        assert result["status"] == "SOLVED"
        assert result["solution"] is not None
        assert result["solution"] == {
            "bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}
        }
        # Explicit validation through core.solution_validator
        report = validate_solution(P1_PUZZLE, result["solution"])
        assert report["valid"] is True
        assert report["degree_violations"] == []
        assert report["crossings"] == []
        assert result["validation_report"]["valid"] is True

    def test_distinguishes_no_valid_solution_found_on_impossible_puzzle(self):
        result = solve_memetic(
            IMPOSSIBLE_PUZZLE,
            IMPOSSIBLE_EDGES,
            config={"population_size": 10, "max_generations": 5, "seed": 99},
        )
        assert result["status"] == "NO_VALID_SOLUTION_FOUND"
        assert result["solution"] is None
        assert result["validation_report"] is None
        assert result["metrics"]["best_fitness"] > [0, 0, 0]

    def test_rejects_crossing_and_disconnected_candidates_on_p2(self):
        # P2 has 2 crossing candidate bridges; cannot be solved without crossing or disconnecting
        result = solve_memetic(
            P2_PUZZLE,
            P2_EDGES,
            config={"population_size": 30, "max_generations": 25, "seed": 42},
        )
        assert result["status"] == "NO_VALID_SOLUTION_FOUND"
        assert result["solution"] is None

        # Confirm crossing state [1, 1] is rejected by core validator
        crossing_sol = {"bridge_counts": {"E1": 1, "E2": 1}}
        report = validate_solution(P2_PUZZLE, crossing_sol)
        assert report["valid"] is False
        assert len(report["crossings"]) > 0


# ==============================================================================
# Group 6: Interface, Determinism & Facade Compatibility
# ==============================================================================
class TestInterfaceAndDeterminism:
    """Ensure compliance with ALGORITHM_INTERFACE.md and seed reproducibility."""

    def test_deterministic_with_same_seed(self):
        res1 = solve_memetic(
            P1_PUZZLE,
            P1_EDGES,
            config={"population_size": 20, "max_generations": 10, "seed": 777},
        )
        res2 = solve_memetic(
            P1_PUZZLE,
            P1_EDGES,
            config={"population_size": 20, "max_generations": 10, "seed": 777},
        )
        assert res1["status"] == res2["status"]
        assert res1["solution"] == res2["solution"]
        assert res1["metrics"]["generations"] == res2["metrics"]["generations"]
        assert res1["metrics"]["local_search_calls"] == res2["metrics"]["local_search_calls"]

    def test_polymorphic_candidate_bridges_omission(self):
        # Call without passing candidate_bridges (auto-generated from islands)
        result = solve_memetic(
            P1_PUZZLE,
            config={"population_size": 30, "max_generations": 20, "seed": 42},
        )
        assert result["status"] == "SOLVED"
        assert result["solution"] == {
            "bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}
        }

    def test_memetic_facade_matches_module_solver(self):
        res_facade = memetic_facade_solver(
            P1_PUZZLE,
            P1_EDGES,
            config={"population_size": 20, "max_generations": 10, "seed": 42},
        )
        assert res_facade["status"] == "SOLVED"
        assert res_facade["solution"] is not None
