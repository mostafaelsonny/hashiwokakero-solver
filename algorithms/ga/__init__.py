"""GA / MA shared chromosome, fitness, and operators module (Sprint 2 - S2-06 & S2-07).

Exposes foundational utilities for chromosome encoding/decoding,
lexicographical multi-objective fitness evaluation, evolutionary operators,
and the genetic algorithm solver.
"""
from __future__ import annotations

from algorithms.ga.chromosome import (
    chromosome_to_solution,
    initialize_population,
    solution_to_chromosome,
    validate_chromosome,
)
from algorithms.ga.fitness import (
    build_conflict_pairs,
    evaluate_fitness,
)
from algorithms.ga.genetic_solver import (
    solve_genetic,
)
from algorithms.ga.operators import (
    get_elites,
    mutate,
    tournament_selection,
    uniform_crossover,
)

__all__ = [
    "chromosome_to_solution",
    "solution_to_chromosome",
    "validate_chromosome",
    "initialize_population",
    "evaluate_fitness",
    "build_conflict_pairs",
    "tournament_selection",
    "uniform_crossover",
    "mutate",
    "get_elites",
    "solve_genetic",
]
