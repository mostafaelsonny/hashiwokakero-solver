"""Sprint 2 / Sprint 3 - Memetic Algorithm = GA + Local Search. Design: docs/MA_DESIGN.md (S1-10)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from algorithms.ma.local_search import (
    InvalidChromosomeError,
    _actual_degrees,
    _incident_indices,
    _islands_in_canonical_order,
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
from algorithms.ma.memetic_solver import solve_memetic as _solve_memetic
from core.models import CandidateBridge, Puzzle, SolverResult

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
    "_actual_degrees",
    "_incident_indices",
    "_islands_in_canonical_order",
]


def solve_memetic(
    puzzle: Puzzle,
    candidate_bridges: Optional[Union[List[CandidateBridge], Dict[str, Any]]] = None,
    config: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
) -> SolverResult:
    """Entry point for the Memetic Algorithm solver, conforming to docs/ALGORITHM_INTERFACE.md."""
    return _solve_memetic(
        puzzle=puzzle,
        candidate_bridges=candidate_bridges,
        config=config,
        seed=seed,
    )
