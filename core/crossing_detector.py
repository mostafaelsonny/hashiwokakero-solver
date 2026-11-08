"""S1-05 - Crossing Detection.  Owner: Monzer.  Reviewer: Mostafa.

Notes: docs/GRAPH_ENGINE_NOTES.md

Geometry rule (strict comparisons):
  horizontal bridge at row r between cols c1 < c2, vertical bridge at col c between
  rows r1 < r2  ->  they cross  iff  c1 < c < c2  AND  r1 < r < r2.
Bridges that only share an island do NOT cross. A count of 0 means "no bridge".
A double bridge still counts as ONE crossing pair.
"""
from __future__ import annotations

from typing import List

from core.models import CandidateBridge, Island, Solution


def get_crossing_pairs(
    islands: List[Island], edges: List[CandidateBridge]
) -> List[List[str]]:
    """All candidate-edge pairs that WOULD cross if both had a bridge, e.g. [["E1","E2"]].

    Computed once up front; Backtracking and GA reuse it for speed.
    """
    raise NotImplementedError("S1-05 not implemented yet (owner: Monzer)")


def detect_crossings(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> List[List[str]]:
    """Pairs of edges that actually cross in `solution` (both counts > 0)."""
    raise NotImplementedError("S1-05 not implemented yet (owner: Monzer)")
