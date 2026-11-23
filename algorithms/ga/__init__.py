"""GA / MA shared chromosome and fitness module (Sprint 2 - S2-06).

Exposes foundational utilities for chromosome encoding/decoding and
lexicographical multi-objective fitness evaluation.
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

__all__ = [
    "chromosome_to_solution",
    "solution_to_chromosome",
    "validate_chromosome",
    "initialize_population",
    "evaluate_fitness",
    "build_conflict_pairs",
]
