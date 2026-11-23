"""Comprehensive GA Unit and Regression Test Suite (Sprint 2 - S2-08).

Owner: Rovan (M4 - Genetic Algorithm)
Reviewer: Mostafa (M1)

Test Groups:
  1. Chromosome & Encoding (length mapping, domain validation, lossless round-trip)
  2. Fitness Function (P1 optimal score, degree error, crossing count, connectivity penalty)
  3. Genetic Operators (tournament selection, uniform crossover, mutation, elitism)
  4. Solver Loop & Termination (benchmark solving, bounded termination, validation guarantee)
"""
from __future__ import annotations

import random
from typing import List

import pytest

from algorithms.ga import (
    build_conflict_pairs,
    chromosome_to_solution,
    evaluate_fitness,
    get_elites,
    initialize_population,
    mutate,
    solution_to_chromosome,
    solve_genetic,
    tournament_selection,
    uniform_crossover,
    validate_chromosome,
)
from algorithms.ga.operators import VALID_GENES
from core.candidate_generator import generate_candidate_edges
from core.solution_validator import validate_solution
from tests.helpers import P1_EDGES, P1_PUZZLE


# ==============================================================================
# Test Fixtures & Puzzles
# ==============================================================================

# Plus puzzle where vertical E1 crosses horizontal E2
PLUS_PUZZLE = {
    "rows": 3,
    "cols": 3,
    "islands": [
        {"id": "T", "row": 0, "col": 1, "required_bridges": 1},
        {"id": "L", "row": 1, "col": 0, "required_bridges": 1},
        {"id": "R", "row": 1, "col": 2, "required_bridges": 1},
        {"id": "B", "row": 2, "col": 1, "required_bridges": 1},
    ],
}
PLUS_EDGES = [
    {"id": "E1", "from": "T", "to": "B", "orientation": "vertical"},
    {"id": "E2", "from": "L", "to": "R", "orientation": "horizontal"},
]

# Impossible puzzle: 2 islands requiring 5 bridges each (max possible is 2)
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
# Group 1: Chromosome & Encoding
# ==============================================================================
class TestChromosomeAndEncoding:
    """Validates chromosome data structure, domain enforcement, and conversion."""

    def test_chromosome_length_equals_candidate_list_length(self):
        """Chromosome length must strictly match len(candidate_bridges)."""
        valid_chromosome = [1, 1, 1, 1]
        assert len(valid_chromosome) == len(P1_EDGES)
        # Should validate without error
        validate_chromosome(valid_chromosome, len(P1_EDGES))

        # Length mismatch must raise ValueError
        with pytest.raises(ValueError, match="chromosome_length_mismatch"):
            validate_chromosome([1, 1, 1], len(P1_EDGES))

        with pytest.raises(ValueError, match="chromosome_length_mismatch"):
            validate_chromosome([1, 1, 1, 1, 1], len(P1_EDGES))

    @pytest.mark.parametrize(
        "bad_gene",
        [-1, 3, 10, 1.0, True, False, "1", None, [1]],
    )
    def test_gene_values_outside_domain_rejected(self, bad_gene):
        """Gene values strictly bounded to integers in {0, 1, 2}. Booleans and floats rejected."""
        bad_chromosome = [1, 0, bad_gene, 2]
        with pytest.raises(ValueError):
            validate_chromosome(bad_chromosome, len(P1_EDGES))

        with pytest.raises(ValueError):
            chromosome_to_solution(bad_chromosome, P1_EDGES)

    @pytest.mark.parametrize(
        "chromosome",
        [
            [1, 1, 1, 1],
            [2, 0, 0, 2],
            [0, 0, 0, 0],
            [2, 2, 2, 2],
            [0, 1, 2, 1],
            [2, 1, 0, 2],
        ],
    )
    def test_lossless_round_trip_conversion(self, chromosome):
        """Converting chromosome -> Solution -> chromosome must be completely lossless."""
        solution = chromosome_to_solution(chromosome, P1_EDGES)
        recovered = solution_to_chromosome(solution, P1_EDGES)
        assert recovered == chromosome

    def test_missing_known_candidate_ids_evaluate_to_zero(self):
        """DATA_MODEL: Missing known bridge IDs in Solution evaluate to count 0."""
        partial_solution = {"bridge_counts": {"E1": 2, "E4": 1}}
        chromosome = solution_to_chromosome(partial_solution, P1_EDGES)
        assert chromosome == [2, 0, 0, 1]

    def test_unknown_bridge_id_raises_explicit_error(self):
        """Unknown candidate IDs must never be silently ignored."""
        bad_solution = {"bridge_counts": {"E99": 1}}
        with pytest.raises(ValueError, match="unknown_candidate_bridge_id"):
            solution_to_chromosome(bad_solution, P1_EDGES)


# ==============================================================================
# Group 2: Fitness Function
# ==============================================================================
class TestFitnessFunction:
    """Validates multi-objective lexicographical fitness evaluation."""

    def test_evaluates_p1_valid_chromosome_to_optimal_zero(self):
        """The valid solution [1, 1, 1, 1] for P1 must evaluate to strictly (0, 0, 0)."""
        fitness = evaluate_fitness([1, 1, 1, 1], P1_PUZZLE, P1_EDGES)
        assert fitness == (0, 0, 0)

    def test_degree_error_calculated_as_sum_of_absolute_differences(self):
        """Degree error = sum over islands of |required - actual|."""
        # [1, 0, 1, 1]: E2 (A-C) is 0. Island A has degree 1 (req 2), C has degree 1 (req 2).
        # B has degree 2 (req 2), D has degree 2 (req 2).
        # Sum of absolute differences: |2-1| + |2-2| + |2-1| + |2-2| = 2
        fitness = evaluate_fitness([1, 0, 1, 1], P1_PUZZLE, P1_EDGES)
        assert fitness[0] == 2  # degree_error = 2

        # [0, 0, 0, 0]: All islands have degree 0 (req 2 each). Error = 2 + 2 + 2 + 2 = 8
        fitness_empty = evaluate_fitness([0, 0, 0, 0], P1_PUZZLE, P1_EDGES)
        assert fitness_empty[0] == 8

        # [2, 2, 0, 0]: Island A has degree 4 (diff 2), D has degree 0 (diff 2). Total error = 4
        fitness_over = evaluate_fitness([2, 2, 0, 0], P1_PUZZLE, P1_EDGES)
        assert fitness_over[0] == 4

    def test_crossing_count_reflects_intersecting_pairs_with_count_greater_than_zero(self):
        """Crossing count reflects pairs where both candidates have count > 0."""
        conflicts = build_conflict_pairs(PLUS_PUZZLE, PLUS_EDGES)
        assert conflicts == [(0, 1)]

        # Both bridges active -> crossing count = 1
        fitness_crossed = evaluate_fitness([1, 1], PLUS_PUZZLE, PLUS_EDGES, conflicts=conflicts)
        assert fitness_crossed[1] == 1

        # Double bridges still count as ONE crossing pair
        fitness_double_crossed = evaluate_fitness([2, 2], PLUS_PUZZLE, PLUS_EDGES, conflicts=conflicts)
        assert fitness_double_crossed[1] == 1

        # Only one bridge active -> crossing count = 0
        fitness_one = evaluate_fitness([1, 0], PLUS_PUZZLE, PLUS_EDGES, conflicts=conflicts)
        assert fitness_one[1] == 0

        fitness_other = evaluate_fitness([0, 2], PLUS_PUZZLE, PLUS_EDGES, conflicts=conflicts)
        assert fitness_other[1] == 0

    def test_disconnected_solutions_penalized_according_to_component_count(self):
        """Connectivity penalty = max(0, connected_components - 1)."""
        # [2, 0, 0, 2] on P1 forms two disconnected components: {A, B} and {C, D}
        # Penalty: 2 - 1 = 1
        fitness_split = evaluate_fitness([2, 0, 0, 2], P1_PUZZLE, P1_EDGES)
        assert fitness_split[2] == 1

        # [1, 0, 0, 0] leaves C and D isolated -> 3 components: {A, B}, {C}, {D}
        # Penalty: 3 - 1 = 2
        fitness_isolated = evaluate_fitness([1, 0, 0, 0], P1_PUZZLE, P1_EDGES)
        assert fitness_isolated[2] == 2

        # [0, 0, 0, 0] leaves all 4 islands isolated -> 4 components -> penalty: 3
        fitness_none = evaluate_fitness([0, 0, 0, 0], P1_PUZZLE, P1_EDGES)
        assert fitness_none[2] == 3


# ==============================================================================
# Group 3: Operators
# ==============================================================================
class TestOperators:
    """Validates tournament selection, uniform crossover, mutation, and elitism."""

    def test_tournament_selection_picks_fitter_individual(self):
        """Tournament selection must pick the individual with lowest lexicographical fitness."""
        population = [[0, 0], [1, 1], [2, 2]]
        # Fitness: [1, 1] is best (0, 0, 0), [2, 2] is second (1, 0, 0), [0, 0] is worst (3, 0, 0)
        fitnesses = [(3, 0, 0), (0, 0, 0), (1, 0, 0)]

        # Fixed seed ensures deterministic contestant selection
        rng = random.Random(42)
        winner = tournament_selection(population, fitnesses, k=3, rng=rng)
        assert winner == [1, 1]

        # Selected individual must be an isolated copy
        winner[0] = 99
        assert population[1] == [1, 1]

    def test_uniform_crossover_preserves_length_and_gene_domain(self):
        """Offspring must have identical length and all genes from parents within {0, 1, 2}."""
        p1 = [0, 1, 2, 0, 1, 2]
        p2 = [2, 1, 0, 2, 1, 0]
        rng = random.Random(101)

        offspring = uniform_crossover(p1, p2, rng=rng)
        assert len(offspring) == len(p1)
        for i, gene in enumerate(offspring):
            assert gene in (p1[i], p2[i])
            assert gene in VALID_GENES

    def test_mutation_produces_valid_gene_values_in_domain(self):
        """Mutated genes must be in {0, 1, 2} and strictly different from original value."""
        chrom = [0, 1, 2, 1, 0]
        rng = random.Random(55)

        # 100% mutation forces every gene to mutate
        mutated = mutate(chrom, mutation_rate=1.0, rng=rng)
        assert len(mutated) == len(chrom)
        for original, new_val in zip(chrom, mutated):
            assert new_val in VALID_GENES
            assert new_val != original

        # 0% mutation leaves chromosome unchanged (but returns fresh copy)
        unchanged = mutate(chrom, mutation_rate=0.0)
        assert unchanged == chrom
        assert unchanged is not chrom

    def test_elitism_retains_top_individuals_unmodified(self):
        """Top E individuals are copied directly without mutation aliasing."""
        population = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [1, 2, 1]]
        fitnesses = [(4, 0, 0), (0, 0, 0), (3, 0, 0), (1, 0, 0)]

        elites = get_elites(population, fitnesses, elitism_count=2)
        assert len(elites) == 2
        assert elites[0] == [1, 1, 1]  # fitness (0, 0, 0)
        assert elites[1] == [1, 2, 1]  # fitness (1, 0, 0)

        # Modifying elite copy must not affect population
        elites[0][0] = 99
        assert population[1][0] == 1


# ==============================================================================
# Group 4: Solver Loop & Termination
# ==============================================================================
class TestSolverLoopAndTermination:
    """Validates end-to-end execution, benchmark convergence, and termination guarantees."""

    def test_solves_p1_benchmark_within_reasonable_generations_using_fixed_seed(self):
        """GA must solve P1 fixture deterministically when a fixed seed is provided."""
        config = {
            "population_size": 50,
            "max_generations": 100,
            "seed": 42,
        }
        result = solve_genetic(P1_PUZZLE, P1_EDGES, config=config)

        assert result["status"] == "SOLVED"
        assert result["solution"] is not None
        assert result["solution"]["bridge_counts"] == {"E1": 1, "E2": 1, "E3": 1, "E4": 1}
        assert result["metrics"]["best_fitness"] == [0, 0, 0]
        assert result["metrics"]["generations"] < 100
        assert result["metrics"]["evaluations"] > 0
        assert result["metrics"]["runtime_ms"] >= 0.0

    def test_successfully_terminates_on_max_generations_with_no_valid_solution_found(self):
        """On an impossible puzzle, GA terminates boundedly with NO_VALID_SOLUTION_FOUND."""
        config = {
            "population_size": 20,
            "max_generations": 5,
            "seed": 1,
        }
        result = solve_genetic(IMPOSSIBLE_PUZZLE, IMPOSSIBLE_EDGES, config=config)

        assert result["status"] == "NO_VALID_SOLUTION_FOUND"
        assert result["solution"] is None
        assert result["validation_report"] is None
        assert result["metrics"]["generations"] == 5
        assert result["metrics"]["best_fitness"] != [0, 0, 0]

    def test_reported_solution_passes_core_solution_validator(self):
        """Every reported solution with status SOLVED must pass validate_solution."""
        config = {"population_size": 50, "max_generations": 50, "seed": 42}
        result = solve_genetic(P1_PUZZLE, P1_EDGES, config=config)

        if result["status"] == "SOLVED":
            # Independent verification gate
            report = validate_solution(P1_PUZZLE, result["solution"])
            assert report["valid"] is True
            assert len(report["degree_violations"]) == 0
            assert len(report["crossings"]) == 0
            assert report["connected_components"] == 1
            assert len(report["invalid_values"]) == 0
            assert report == result["validation_report"]
