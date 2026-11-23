"""Genetic Algorithm Solver (Sprint 2 - S2-07).

Executes population-based stochastic global search with tournament selection,
uniform crossover, gene mutation, and elitism to solve Hashiwokakero puzzles.

Conforms strictly to docs/ALGORITHM_INTERFACE.md section 3.2 and section 5.
"""
from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from algorithms.ga.chromosome import chromosome_to_solution, initialize_population
from algorithms.ga.fitness import build_conflict_pairs, evaluate_fitness
from algorithms.ga.operators import get_elites, mutate, tournament_selection, uniform_crossover
from core.solution_validator import validate_solution

if TYPE_CHECKING:
    from core.models import CandidateBridge, Puzzle, SolverResult

DEFAULT_POPULATION_SIZE = 100
DEFAULT_MAX_GENERATIONS = 100
DEFAULT_TOURNAMENT_SIZE = 3
DEFAULT_CROSSOVER_RATE = 0.8
DEFAULT_ELITISM_COUNT = 2
DEFAULT_TIMEOUT_MS = 15000.0


def solve_genetic(
    puzzle: "Puzzle",
    candidate_bridges: List["CandidateBridge"],
    config: Optional[Dict[str, Any]] = None,
) -> "SolverResult":
    """Execute Genetic Algorithm evolution loop using multi-objective tournament selection.

    Args:
        puzzle: Canonical Puzzle TypedDict with rows, cols, and islands.
        candidate_bridges: Deterministically ordered list of CandidateBridge objects (E1..En).
        config: Optional dictionary containing hyperparameters:
            - population_size (int, default 100)
            - max_generations (int, default 100)
            - tournament_size (int, default 3)
            - crossover_rate (float, default 0.8)
            - mutation_rate (float, default 1 / len(candidate_bridges))
            - elitism_count (int, default 2)
            - seed (int, optional)
            - timeout_ms (float, default 15000.0)

    Returns:
        Standard SolverResult dictionary matching docs/ALGORITHM_INTERFACE.md:
        {
            "status": "SOLVED" | "NO_VALID_SOLUTION_FOUND",
            "solution": Solution | None,
            "validation_report": ValidationReport | None,
            "metrics": {
                "runtime_ms": float,
                "generations": int,
                "evaluations": int,
                "best_fitness": List[int],
                "population_size": int,
            }
        }
    """
    start_time = time.perf_counter()
    cfg = config or {}

    pop_size = int(cfg.get("population_size", cfg.get("pop_size", DEFAULT_POPULATION_SIZE)))
    max_generations = int(cfg.get("max_generations", DEFAULT_MAX_GENERATIONS))
    tournament_size = int(cfg.get("tournament_size", DEFAULT_TOURNAMENT_SIZE))
    crossover_rate = float(cfg.get("crossover_rate", DEFAULT_CROSSOVER_RATE))
    elitism_count = int(cfg.get("elitism_count", DEFAULT_ELITISM_COUNT))
    seed = cfg.get("seed")
    timeout_ms = float(cfg.get("timeout_ms", DEFAULT_TIMEOUT_MS))

    chromosome_len = len(candidate_bridges)
    p_mut = cfg.get("mutation_rate")
    if p_mut is not None:
        p_mut = float(p_mut)
    else:
        p_mut = (1.0 / chromosome_len) if chromosome_len > 0 else 0.0

    rng = random.Random(seed) if seed is not None else random.Random()

    # Precompute geometric conflict pairs once for the entire run
    conflicts = build_conflict_pairs(puzzle, candidate_bridges)

    # Initialize population
    population = initialize_population(pop_size, chromosome_len, seed=seed)

    evaluations = 0
    generations_completed = 0
    best_overall_fitness: Optional[Tuple[int, int, int]] = None

    # Evaluate initial generation (gen 0)
    fitnesses: List[Tuple[int, int, int]] = []
    for chromosome in population:
        fit = evaluate_fitness(chromosome, puzzle, candidate_bridges, conflicts=conflicts)
        evaluations += 1
        fitnesses.append(fit)

        if best_overall_fitness is None or fit < best_overall_fitness:
            best_overall_fitness = fit

        # If ideal fitness reached, verify via core independent validator
        if fit == (0, 0, 0):
            solution = chromosome_to_solution(chromosome, candidate_bridges)
            report = validate_solution(puzzle, solution)
            if report["valid"]:
                runtime_ms = (time.perf_counter() - start_time) * 1000.0
                return {
                    "status": "SOLVED",
                    "solution": solution,
                    "validation_report": report,
                    "metrics": {
                        "runtime_ms": runtime_ms,
                        "generations": 0,
                        "evaluations": evaluations,
                        "best_fitness": [0, 0, 0],
                        "population_size": pop_size,
                    },
                }

    # Evolution loop
    for gen in range(1, max_generations + 1):
        generations_completed = gen

        # Check time limit
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if elapsed_ms >= timeout_ms:
            break

        # 1. Elitism: preserve top E individuals without mutation aliasing
        elites = get_elites(population, fitnesses, elitism_count)
        next_population: List[List[int]] = [list(e) for e in elites]

        # 2. Reproduction: selection, uniform crossover, and gene mutation
        while len(next_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, k=tournament_size, rng=rng)
            parent2 = tournament_selection(population, fitnesses, k=tournament_size, rng=rng)

            if rng.random() < crossover_rate:
                child = uniform_crossover(parent1, parent2, rng=rng)
            else:
                child = list(parent1)

            child = mutate(child, mutation_rate=p_mut, rng=rng)
            next_population.append(child)

        population = next_population

        # 3. Evaluate new population
        fitnesses = []
        found_solution = None

        for chromosome in population:
            fit = evaluate_fitness(chromosome, puzzle, candidate_bridges, conflicts=conflicts)
            evaluations += 1
            fitnesses.append(fit)

            if fit < best_overall_fitness:
                best_overall_fitness = fit

            if fit == (0, 0, 0) and found_solution is None:
                solution = chromosome_to_solution(chromosome, candidate_bridges)
                report = validate_solution(puzzle, solution)
                if report["valid"]:
                    found_solution = (solution, report)

        if found_solution is not None:
            sol, rep = found_solution
            runtime_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "status": "SOLVED",
                "solution": sol,
                "validation_report": rep,
                "metrics": {
                    "runtime_ms": runtime_ms,
                    "generations": generations_completed,
                    "evaluations": evaluations,
                    "best_fitness": [0, 0, 0],
                    "population_size": pop_size,
                },
            }

    # If search limits reached without a valid solution, return bounded failure
    runtime_ms = (time.perf_counter() - start_time) * 1000.0
    best_fit_list = (
        list(best_overall_fitness) if best_overall_fitness is not None else [999, 999, 999]
    )
    return {
        "status": "NO_VALID_SOLUTION_FOUND",
        "solution": None,
        "validation_report": None,
        "metrics": {
            "runtime_ms": runtime_ms,
            "generations": generations_completed,
            "evaluations": evaluations,
            "best_fitness": best_fit_list,
            "population_size": pop_size,
        },
    }
