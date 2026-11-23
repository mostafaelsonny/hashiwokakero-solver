"""Memetic Algorithm (MA) package (Sprint 2 / Sprint 3).

Exposes Local Search operators, neighborhood generators, hill climbing,
and the unified Memetic Algorithm solver.
"""
from __future__ import annotations

from algorithms.ma.local_search import (
    InvalidChromosomeError,
    best_improving_neighbor,
    conflict_pairs_from_graph_context,
    evaluate_chromosome,
    find_invalid_values,
    generate_neighbors,
    hill_climb,
    pairwise_transfer_neighbors,
    single_gene_neighbors,
    validate_local_search_input,
)
from algorithms.ma.memetic_solver import solve_memetic

__all__ = [
    "solve_memetic",
    "InvalidChromosomeError",
    "find_invalid_values",
    "validate_local_search_input",
    "conflict_pairs_from_graph_context",
    "single_gene_neighbors",
    "pairwise_transfer_neighbors",
    "generate_neighbors",
    "evaluate_chromosome",
    "best_improving_neighbor",
    "hill_climb",
]
