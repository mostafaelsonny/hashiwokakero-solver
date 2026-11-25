"""Backtracking Solver facade (Sprint 2 - S2-04 / S2-05).

Core implementation: core/backtracking_solver.py
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.backtracking_solver import solve_backtracking as _solve_bt
from core.candidate_generator import generate_candidate_edges
from core.models import CandidateBridge, Puzzle, SolverResult


def solve_backtracking(
    puzzle: Puzzle,
    candidate_bridges: Optional[List[CandidateBridge]] = None,
    config: Optional[Dict[str, Any]] = None,
    max_states: Optional[int] = None,
    time_limit: Optional[float] = None,
    **kwargs: Any,
) -> SolverResult:
    """Execute Backtracking solver.

    Supports canonical interface (puzzle, candidate_bridges, config) as well
    as convenience calls where candidate_bridges is omitted.
    """
    if candidate_bridges is None:
        candidate_bridges = generate_candidate_edges(puzzle["islands"])

    cfg = dict(config or {})
    if max_states is not None:
        cfg["max_states"] = max_states
    if time_limit is not None:
        cfg["timeout_ms"] = int(time_limit * 1000)
    if "params" in kwargs and isinstance(kwargs["params"], dict):
        cfg.update(kwargs["params"])

    return _solve_bt(puzzle, candidate_bridges, config=cfg)
