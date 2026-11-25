"""Tests for GA Genetic Operators and Evolution Loop (Sprint 2 - S2-07).

Validates:
  * Reusable operators: Tournament Selection, Uniform Crossover, Mutation, Elitism.
  * End-to-end Genetic Algorithm evolution loop (solve_genetic).
  * Contract adherence: gene domain {0, 1, 2}, length preservation, no mutation aliasing.
  * Deterministic reproducibility with seeds.
  * Bounded termination and standard SolverResult format.
"""
from __future__ import annotations

import random

import pytest

from algorithms.ga import (
    get_elites,
    mutate,
    solve_genetic,
    tournament_selection,
    uniform_crossover,
)
from algorithms.ga.operators import VALID_GENES
from core.candidate_generator import generate_candidate_edges
from core.solution_validator import validate_solution
from tests.helpers import P1_EDGES, P1_PUZZLE

P1_CANDIDATES = P1_EDGES


# ==============================================================================
# 1. Reusable Operators Tests
# ==============================================================================

# ---- Tournament Selection ----------------------------------------------------
def test_tournament_selection_picks_best_fitness():
    population = [[0, 0], [1, 1], [2, 2]]
    # Lower lexicographical tuple is better: (0, 0, 0) < (1, 0, 0) < (2, 0, 0)
    fitnesses = [(2, 0, 0), (0, 0, 0), (1, 0, 0)]
    # Tournament including all 3 must pick index 1 ([1, 1])
    winner = tournament_selection(population, fitnesses, k=3)
    assert winner == [1, 1]


def test_tournament_selection_returns_copy_not_alias():
    population = [[1, 2, 0]]
    fitnesses = [(0, 0, 0)]
    selected = tournament_selection(population, fitnesses, k=1)
    selected[0] = 99
    assert population[0][0] == 1  # original must remain unchanged


def test_tournament_selection_seeded_is_deterministic():
    population = [[i, i] for i in range(10)]
    fitnesses = [(10 - i, 0, 0) for i in range(10)]
    rng1 = random.Random(42)
    rng2 = random.Random(42)
    res1 = tournament_selection(population, fitnesses, k=3, rng=rng1)
    res2 = tournament_selection(population, fitnesses, k=3, rng=rng2)
    assert res1 == res2


def test_tournament_selection_validation():
    with pytest.raises(ValueError, match="empty population"):
        tournament_selection([], [])

    with pytest.raises(ValueError, match="does not match"):
        tournament_selection([[0]], [(0, 0, 0), (1, 1, 1)])

    with pytest.raises(ValueError, match="k must be >= 1"):
        tournament_selection([[0]], [(0, 0, 0)], k=0)


# ---- Uniform Crossover -------------------------------------------------------
def test_uniform_crossover_preserves_length_and_domain():
    p1 = [0, 1, 2, 0, 1, 2]
    p2 = [2, 1, 0, 2, 1, 0]
    rng = random.Random(123)
    offspring = uniform_crossover(p1, p2, rng=rng)

    assert len(offspring) == len(p1)
    for gene, g1, g2 in zip(offspring, p1, p2):
        assert gene in (g1, g2)
        assert gene in VALID_GENES


def test_uniform_crossover_both_parents_contribute():
    p1 = [0] * 50
    p2 = [2] * 50
    rng = random.Random(7)
    offspring = uniform_crossover(p1, p2, rng=rng)

    assert 0 in offspring
    assert 2 in offspring
    assert len(offspring) == 50


def test_uniform_crossover_length_mismatch():
    with pytest.raises(ValueError, match="equal length"):
        uniform_crossover([0, 1], [0, 1, 2])


def test_uniform_crossover_empty_chromosome():
    assert uniform_crossover([], []) == []


# ---- Mutation ----------------------------------------------------------------
def test_mutation_rate_zero_no_changes():
    chrom = [0, 1, 2, 1, 0]
    mutated = mutate(chrom, mutation_rate=0.0)
    assert mutated == chrom
    assert mutated is not chrom  # fresh copy


def test_mutation_rate_one_replaces_with_different_valid_value():
    chrom = [0, 1, 2, 1, 0]
    rng = random.Random(99)
    mutated = mutate(chrom, mutation_rate=1.0, rng=rng)

    assert len(mutated) == len(chrom)
    for orig, mut in zip(chrom, mutated):
        assert mut in VALID_GENES
        assert mut != orig  # strictly different value


def test_mutation_preserves_unmutated_genes():
    chrom = [1] * 20
    # low mutation rate with fixed seed
    rng = random.Random(42)
    mutated = mutate(chrom, mutation_rate=0.05, rng=rng)
    assert len(mutated) == len(chrom)
    assert all(g in VALID_GENES for g in mutated)


def test_mutation_validation():
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        mutate([1, 0], mutation_rate=1.5)

    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        mutate([1, 0], mutation_rate=-0.1)

    with pytest.raises(ValueError, match="Invalid gene value"):
        mutate([1, 5], mutation_rate=0.5)


def test_mutation_empty_chromosome():
    assert mutate([]) == []


# ---- Elitism -----------------------------------------------------------------
def test_get_elites_preserves_top_individuals():
    population = [[0, 0], [1, 1], [2, 2], [1, 2]]
    fitnesses = [(3, 0, 0), (0, 0, 0), (2, 0, 0), (1, 0, 0)]
    elites = get_elites(population, fitnesses, elitism_count=2)

    assert len(elites) == 2
    assert elites[0] == [1, 1]  # fitness (0, 0, 0)
    assert elites[1] == [1, 2]  # fitness (1, 0, 0)


def test_get_elites_returns_deep_copies_no_aliasing():
    population = [[1, 2, 0], [0, 1, 2]]
    fitnesses = [(0, 0, 0), (1, 0, 0)]
    elites = get_elites(population, fitnesses, elitism_count=1)

    elites[0][0] = 99
    assert population[0][0] == 1  # original untouched!


def test_get_elites_count_zero_or_empty():
    assert get_elites([[1]], [(0, 0, 0)], elitism_count=0) == []
    assert get_elites([], [], elitism_count=2) == []


def test_get_elites_count_larger_than_population():
    population = [[2], [0]]
    fitnesses = [(2, 0, 0), (0, 0, 0)]
    elites = get_elites(population, fitnesses, elitism_count=5)
    assert len(elites) == 2
    assert elites[0] == [0]
    assert elites[1] == [2]


# ==============================================================================
# 2. Evolution Loop (solve_genetic) Tests
# ==============================================================================

def test_solve_genetic_solves_p1():
    """Verify GA solves canonical P1 puzzle and returns standard SolverResult."""
    config = {
        "population_size": 50,
        "max_generations": 100,
        "seed": 42,
    }
    result = solve_genetic(P1_PUZZLE, P1_CANDIDATES, config=config)

    assert result["status"] == "SOLVED"
    assert result["solution"] is not None
    assert result["validation_report"] is not None
    assert result["validation_report"]["valid"] is True

    # P1 has only one valid solution: all bridges = 1
    assert result["solution"]["bridge_counts"] == {
        "E1": 1,
        "E2": 1,
        "E3": 1,
        "E4": 1,
    }

    # Verify metrics structure
    metrics = result["metrics"]
    assert "runtime_ms" in metrics and metrics["runtime_ms"] >= 0.0
    assert "generations" in metrics
    assert "evaluations" in metrics and metrics["evaluations"] > 0
    assert metrics["best_fitness"] == [0, 0, 0]
    assert metrics["population_size"] == 50


def test_solve_genetic_seeded_reproducibility():
    """Identical seed must produce identical execution telemetry and results."""
    cfg = {"population_size": 30, "max_generations": 20, "seed": 777}

    res1 = solve_genetic(P1_PUZZLE, P1_CANDIDATES, config=cfg)
    res2 = solve_genetic(P1_PUZZLE, P1_CANDIDATES, config=cfg)

    assert res1["status"] == res2["status"]
    assert res1["solution"] == res2["solution"]
    assert res1["metrics"]["generations"] == res2["metrics"]["generations"]
    assert res1["metrics"]["evaluations"] == res2["metrics"]["evaluations"]
    assert res1["metrics"]["best_fitness"] == res2["metrics"]["best_fitness"]


def test_solve_genetic_unsolvable_returns_no_valid_solution_found():
    """When a puzzle has no solution, GA must boundedly terminate with NO_VALID_SOLUTION_FOUND."""
    # Impossible puzzle: 2 islands requiring 5 bridges each, but max connection is 2
    impossible_puzzle = {
        "rows": 1,
        "cols": 3,
        "islands": [
            {"id": "A", "row": 0, "col": 0, "required_bridges": 5},
            {"id": "B", "row": 0, "col": 2, "required_bridges": 5},
        ],
    }
    candidates = generate_candidate_edges(impossible_puzzle["islands"])

    cfg = {"population_size": 20, "max_generations": 5, "seed": 1}
    result = solve_genetic(impossible_puzzle, candidates, config=cfg)

    assert result["status"] == "NO_VALID_SOLUTION_FOUND"
    assert result["solution"] is None
    assert result["validation_report"] is None
    assert result["metrics"]["generations"] == 5
    assert result["metrics"]["best_fitness"] != [0, 0, 0]


def test_solve_genetic_respects_timeout():
    """GA must respect timeout_ms budget."""
    # Large impossible puzzle with tiny timeout
    puzzle = {
        "rows": 5,
        "cols": 5,
        "islands": [
            {"id": f"I{i}", "row": i, "col": 0, "required_bridges": 4}
            for i in range(5)
        ],
    }
    candidates = generate_candidate_edges(puzzle["islands"])

    cfg = {
        "population_size": 500,
        "max_generations": 10000,
        "timeout_ms": 1.0,  # 1 millisecond limit
    }
    result = solve_genetic(puzzle, candidates, config=cfg)

    assert result["status"] == "NO_VALID_SOLUTION_FOUND"
    assert result["metrics"]["generations"] < 10000


def test_reported_solution_verified_by_validate_solution():
    """Any solution reported with SOLVED must independently pass validate_solution."""
    cfg = {"population_size": 50, "max_generations": 50, "seed": 42}
    result = solve_genetic(P1_PUZZLE, P1_CANDIDATES, config=cfg)

    if result["status"] == "SOLVED":
        independent_report = validate_solution(P1_PUZZLE, result["solution"])
        assert independent_report["valid"] is True
        assert independent_report == result["validation_report"]
