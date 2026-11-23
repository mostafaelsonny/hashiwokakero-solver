"""Genetic Algorithm entry point (S2-07).

Core implementation: algorithms/ga/genetic_solver.py
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from algorithms.ga.genetic_solver import solve_genetic as _solve_ga
from core.candidate_generator import generate_candidate_edges
from core.models import CandidateBridge, Puzzle, SolverResult


def solve_genetic(
    puzzle: Puzzle,
    candidate_bridges: Optional[List[CandidateBridge]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> SolverResult:
    """Execute Genetic Algorithm solver.

    Supports both canonical interface (puzzle, candidate_bridges, config) and
    convenience calls without pre-generated candidate bridges.
    """
    if candidate_bridges is None:
        candidate_bridges = generate_candidate_edges(puzzle["islands"])

    cfg = dict(config or {})
    if "params" in kwargs and isinstance(kwargs["params"], dict):
        cfg.update(kwargs["params"])
    if "seed" in kwargs and kwargs["seed"] is not None:
        cfg["seed"] = kwargs["seed"]

    return _solve_ga(puzzle, candidate_bridges, config=cfg)
