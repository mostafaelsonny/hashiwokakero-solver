"""S1-05 - Crossing Detection.  Owner: Monzer.  Reviewer: Mostafa.

Notes: docs/GRAPH_ENGINE_NOTES.md

Geometry rule (strict comparisons):
  horizontal bridge at row r between cols c1 < c2, vertical bridge at col c between
  rows r1 < r2  ->  they cross  iff  c1 < c < c2  AND  r1 < r < r2.
Bridges that only share an island do NOT cross. A count of 0 means "no bridge".
A double bridge still counts as ONE crossing pair.
"""
from __future__ import annotations

from typing import Dict, List

from core.models import CandidateBridge, Island, Solution


def _build_island_map(islands: List[Island]) -> Dict[str, Island]:
    return {isl["id"]: isl for isl in islands}


def _would_cross(
    e1: CandidateBridge, e2: CandidateBridge, island_map: Dict[str, Island]
) -> bool:
    """Return True if e1 and e2 would geometrically cross (regardless of counts).

    Rules:
    - Both edges must have different orientations (one H, one V).
    - Edges sharing an endpoint island never cross.
    - Strict inequality check: c1 < c < c2  AND  r1 < r < r2.
    """
    if e1["orientation"] == e2["orientation"]:
        # Both horizontal or both vertical → cannot cross
        return False

    # Assign horizontal (h) and vertical (v)
    if e1["orientation"] == "horizontal":
        h, v = e1, e2
    else:
        h, v = e2, e1

    # Shared endpoint → not a crossing
    if (
        h["from"] == v["from"]
        or h["from"] == v["to"]
        or h["to"] == v["from"]
        or h["to"] == v["to"]
    ):
        return False

    # Horizontal bridge occupies: row=r, cols [c1, c2]
    r = island_map[h["from"]]["row"]
    c1 = island_map[h["from"]]["col"]
    c2 = island_map[h["to"]]["col"]
    if c1 > c2:
        c1, c2 = c2, c1

    # Vertical bridge occupies: col=c, rows [r1, r2]
    c = island_map[v["from"]]["col"]
    r1 = island_map[v["from"]]["row"]
    r2 = island_map[v["to"]]["row"]
    if r1 > r2:
        r1, r2 = r2, r1

    return c1 < c < c2 and r1 < r < r2


def get_crossing_pairs(
    islands: List[Island], edges: List[CandidateBridge]
) -> List[List[str]]:
    """All candidate-edge pairs that WOULD cross if both had a bridge, e.g. [["E1","E2"]].

    Computed once up front; Backtracking and GA reuse it for speed.
    """
    island_map = _build_island_map(islands)
    pairs: List[List[str]] = []

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            e1, e2 = edges[i], edges[j]
            if _would_cross(e1, e2, island_map):
                pairs.append([e1["id"], e2["id"]])

    return pairs


def detect_crossings(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> List[List[str]]:
    """Pairs of edges that actually cross in `solution` (both counts > 0)."""
    island_map = _build_island_map(islands)
    result: List[List[str]] = []

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            e1, e2 = edges[i], edges[j]
            count1 = solution["bridge_counts"].get(e1["id"], 0)
            count2 = solution["bridge_counts"].get(e2["id"], 0)
            if count1 > 0 and count2 > 0 and _would_cross(e1, e2, island_map):
                result.append([e1["id"], e2["id"]])

    return result
