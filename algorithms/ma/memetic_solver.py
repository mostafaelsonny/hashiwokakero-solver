"""Memetic Algorithm Solver (Sprint 2 - S2-10).

Executes population-based hybrid global-local search by coupling the Genetic
Algorithm evolutionary cycle with bounded, problem-aware Hill Climbing Local Search
applied during each evolutionary generation.

Reuses foundational components:
  - M4: Chromosome encoding & validation (algorithms/ga/chromosome.py)
  - M4: Lexicographical multi-objective fitness evaluation (algorithms/ga/fitness.py)
  - M4: Modular genetic operators: selection, crossover, mutation, elitism (algorithms/ga/operators.py)
  - M5: Problem-aware Local Search neighborhood operators & Hill Climbing (algorithms/ma/local_search.py)
  - M2: Precomputed graph lookups & crossings (core/graph_context.py)
  - Core: Independent solution validator gate (core/solution_validator.py)

Conforms strictly to docs/ALGORITHM_INTERFACE.md section 3.2, section 7, and section 8.
"""
from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from algorithms.ga.chromosome import chromosome_to_solution, initialize_population
from algorithms.ga.fitness import build_conflict_pairs, evaluate_fitness
from algorithms.ga.operators import get_elites, mutate, tournament_selection, uniform_crossover
from algorithms.ma.local_search import conflict_pairs_from_graph_context, hill_climb
from core.candidate_generator import generate_candidate_edges
from core.graph_context import GraphContext, build_graph_context
from core.solution_validator import validate_solution

if TYPE_CHECKING:
    from core.models import CandidateBridge, Puzzle, Solution, SolverResult

DEFAULT_POPULATION_SIZE = 100
DEFAULT_MAX_GENERATIONS = 100
DEFAULT_TOURNAMENT_SIZE = 3
DEFAULT_CROSSOVER_RATE = 0.8
DEFAULT_ELITISM_COUNT = 2
DEFAULT_MAX_LS_STEPS = 10
DEFAULT_LS_INDIVIDUALS = 2
DEFAULT_LS_FREQUENCY = 1
DEFAULT_TIMEOUT_MS = 15000.0


def solve_memetic(
    puzzle: "Puzzle",
    candidate_bridges: Optional[Union[List["CandidateBridge"], Dict[str, Any]]] = None,
    config: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
) -> "SolverResult":
    """Execute Memetic Algorithm evolution loop with in-loop Hill Climbing local search.

    Args:
        puzzle: Canonical Puzzle dictionary containing rows, cols, and islands.
        candidate_bridges: Deterministically ordered list of CandidateBridge objects (E1..En).
            If omitted or passed as a dict, candidates are automatically generated from islands.
        config: Optional dictionary containing hyperparameters:
            - population_size / pop_size (int, default 100)
            - max_generations (int, default 100)
            - tournament_size (int, default 3)
            - crossover_rate (float, default 0.8)
            - mutation_rate (float, default 1 / len(candidate_bridges))
            - elitism_count (int, default 2)
            - max_ls_steps (int, default 10)
            - ls_individuals (int, default 2): Number of top individuals per generation
              to subject to bounded Hill Climbing.
            - ls_frequency (int, default 1): Apply local search every N generations.
            - seed (int, optional): Random seed for reproducibility.
            - timeout_ms (float, default 15000.0): Search time limit in milliseconds.
        seed: Optional seed override for convenience.

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
                "local_search_calls": int,
                "local_search_improvements": int,
                "avg_ls_steps_per_call": float,
            }
        }
    """
    start_time = time.perf_counter()

    # Normalize polymorphic calling convention: solve_memetic(puzzle, params, seed)
    if isinstance(candidate_bridges, dict) and config is None:
        config = candidate_bridges
        candidate_bridges = None

    if candidate_bridges is None:
        candidate_bridges = generate_candidate_edges(puzzle["islands"])

    cfg: Dict[str, Any] = dict(config) if config else {}
    if seed is not None and "seed" not in cfg:
        cfg["seed"] = seed

    # Hyperparameters
    pop_size = int(cfg.get("population_size", cfg.get("pop_size", DEFAULT_POPULATION_SIZE)))
    max_generations = int(cfg.get("max_generations", DEFAULT_MAX_GENERATIONS))
    tournament_size = int(cfg.get("tournament_size", DEFAULT_TOURNAMENT_SIZE))
    crossover_rate = float(cfg.get("crossover_rate", DEFAULT_CROSSOVER_RATE))
    elitism_count = int(cfg.get("elitism_count", DEFAULT_ELITISM_COUNT))
    max_ls_steps = int(cfg.get("max_ls_steps", DEFAULT_MAX_LS_STEPS))
    ls_individuals = int(cfg.get("ls_individuals", DEFAULT_LS_INDIVIDUALS))
    ls_frequency = int(cfg.get("ls_frequency", DEFAULT_LS_FREQUENCY))
    cfg_seed = cfg.get("seed")
    timeout_ms = float(cfg.get("timeout_ms", DEFAULT_TIMEOUT_MS))

    chromosome_len = len(candidate_bridges)
    p_mut = cfg.get("mutation_rate")
    if p_mut is not None:
        p_mut = float(p_mut)
    else:
        p_mut = (1.0 / chromosome_len) if chromosome_len > 0 else 0.0

    rng = random.Random(cfg_seed) if cfg_seed is not None else random.Random()

    # Precompute geometric context & conflict pairs once per puzzle run
    graph_context: GraphContext = build_graph_context(puzzle, candidate_bridges)
    conflicts = conflict_pairs_from_graph_context(graph_context)

    # Initialize population using shared M4 initializer
    population: List[List[int]] = initialize_population(pop_size, chromosome_len, seed=cfg_seed)

    # Metrics counters
    evaluations = 0
    generations_completed = 0
    local_search_calls = 0
    local_search_improvements = 0
    total_ls_steps_executed = 0
    best_overall_fitness: Optional[Tuple[int, int, int]] = None

    # Evaluate initial generation (gen 0)
    fitnesses: List[Tuple[int, int, int]] = []
    for chromosome in population:
        fit = evaluate_fitness(chromosome, puzzle, candidate_bridges, conflicts=conflicts)
        evaluations += 1
        fitnesses.append(fit)

        if best_overall_fitness is None or fit < best_overall_fitness:
            best_overall_fitness = fit

        # If ideal fitness reached immediately, verify with independent solution validator
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
                        "local_search_calls": 0,
                        "local_search_improvements": 0,
                        "avg_ls_steps_per_call": 0.0,
                    },
                }

    # Helper function to apply bounded in-loop Hill Climbing on top-k individuals
    def _apply_in_loop_local_search(
        curr_pop: List[List[int]], curr_fits: List[Tuple[int, int, int]]
    ) -> Optional[Tuple["Solution", Dict[str, Any]]]:
        nonlocal local_search_calls, local_search_improvements, total_ls_steps_executed, evaluations, best_overall_fitness

        if ls_individuals <= 0 or not curr_pop:
            return None

        # Sort indices by fitness (ascending / lowest is best)
        sorted_indices = sorted(range(len(curr_pop)), key=lambda idx: curr_fits[idx])
        target_count = min(ls_individuals, len(curr_pop))

        for rank in range(target_count):
            idx = sorted_indices[rank]
            chrom = curr_pop[idx]

            local_search_calls += 1
            improved_chrom, ls_stats = hill_climb(
                chrom,
                puzzle,
                candidate_bridges,
                graph_context=graph_context,
                max_steps=max_ls_steps,
                only_unbalanced=True,
            )

            total_ls_steps_executed += ls_stats.get("steps", 0)

            if ls_stats.get("improved", False):
                local_search_improvements += ls_stats.get("improvements", 0)
                curr_pop[idx] = improved_chrom
                improved_fit = tuple(ls_stats["final_fitness"])
                curr_fits[idx] = improved_fit

                if improved_fit < best_overall_fitness:
                    best_overall_fitness = improved_fit

                # Check if ideal fitness was reached through local search
                if improved_fit == (0, 0, 0):
                    sol = chromosome_to_solution(improved_chrom, candidate_bridges)
                    rep = validate_solution(puzzle, sol)
                    if rep["valid"]:
                        return (sol, rep)

        return None

    # Apply local search to initial generation top individuals
    sol_early = _apply_in_loop_local_search(population, fitnesses)
    if sol_early is not None:
        sol, rep = sol_early
        runtime_ms = (time.perf_counter() - start_time) * 1000.0
        avg_steps = (
            (total_ls_steps_executed / local_search_calls) if local_search_calls > 0 else 0.0
        )
        return {
            "status": "SOLVED",
            "solution": sol,
            "validation_report": rep,
            "metrics": {
                "runtime_ms": runtime_ms,
                "generations": 0,
                "evaluations": evaluations,
                "best_fitness": [0, 0, 0],
                "population_size": pop_size,
                "local_search_calls": local_search_calls,
                "local_search_improvements": local_search_improvements,
                "avg_ls_steps_per_call": avg_steps,
            },
        }

    # Evolutionary Generations Loop
    for gen in range(1, max_generations + 1):
        generations_completed = gen

        # Enforce search timeout
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if elapsed_ms >= timeout_ms:
            break

        # 1. Elitism: preserve top E individuals as isolated copies
        elites = get_elites(population, fitnesses, elitism_count)
        next_population: List[List[int]] = [list(e) for e in elites]

        # 2. Reproduction: selection, uniform crossover, and mutation
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

        # 3. Evaluate new generation fitness
        fitnesses = []
        found_solution = None

        for chromosome in population:
            fit = evaluate_fitness(chromosome, puzzle, candidate_bridges, conflicts=conflicts)
            evaluations += 1
            fitnesses.append(fit)

            if best_overall_fitness is None or fit < best_overall_fitness:
                best_overall_fitness = fit

            if fit == (0, 0, 0) and found_solution is None:
                solution = chromosome_to_solution(chromosome, candidate_bridges)
                report = validate_solution(puzzle, solution)
                if report["valid"]:
                    found_solution = (solution, report)

        if found_solution is not None:
            sol, rep = found_solution
            runtime_ms = (time.perf_counter() - start_time) * 1000.0
            avg_steps = (
                (total_ls_steps_executed / local_search_calls) if local_search_calls > 0 else 0.0
            )
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
                    "local_search_calls": local_search_calls,
                    "local_search_improvements": local_search_improvements,
                    "avg_ls_steps_per_call": avg_steps,
                },
            }

        # 4. In-Loop Local Search: Apply bounded Hill Climbing on top individuals
        if ls_frequency > 0 and (gen % ls_frequency == 0):
            sol_ls = _apply_in_loop_local_search(population, fitnesses)
            if sol_ls is not None:
                sol, rep = sol_ls
                runtime_ms = (time.perf_counter() - start_time) * 1000.0
                avg_steps = (
                    (total_ls_steps_executed / local_search_calls)
                    if local_search_calls > 0
                    else 0.0
                )
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
                        "local_search_calls": local_search_calls,
                        "local_search_improvements": local_search_improvements,
                        "avg_ls_steps_per_call": avg_steps,
                    },
                }

    # Search limit reached without finding a valid solution
    runtime_ms = (time.perf_counter() - start_time) * 1000.0
    best_fit_list = (
        list(best_overall_fitness) if best_overall_fitness is not None else [999, 999, 999]
    )
    avg_steps = (
        (total_ls_steps_executed / local_search_calls) if local_search_calls > 0 else 0.0
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
            "local_search_calls": local_search_calls,
            "local_search_improvements": local_search_improvements,
            "avg_ls_steps_per_call": avg_steps,
        },
    }
