"""Shared test fixtures: the two reference puzzles used across the whole project.

P1 (3x3)  - valid-solution / degree / connectivity examples. The ONLY valid solution is [1,1,1,1].
P2        - crossing example: E1 (vertical C-D) crosses E2 (horizontal A-B) at (1, 2).
Edges are written by hand here on purpose, so validator tests do NOT depend on S1-03.
"""
from __future__ import annotations

from typing import Dict, List


def isl(id: str, row: int, col: int, required: int) -> dict:
    return {"id": id, "row": row, "col": col, "required_bridges": required}


def edge(id: str, frm: str, to: str, orientation: str) -> dict:
    return {"id": id, "from": frm, "to": to, "orientation": orientation}


def make_solution(values: List[int], edges: List[dict]) -> Dict[str, Dict[str, int]]:
    """Build {"bridge_counts": {"E1": v1, ...}} following the edge order."""
    return {"bridge_counts": {e["id"]: v for e, v in zip(edges, values)}}


# ---- P1 -------------------------------------------------------------------
P1_ISLANDS = [isl("A", 0, 0, 2), isl("B", 0, 2, 2), isl("C", 2, 0, 2), isl("D", 2, 2, 2)]
P1_EDGES = [
    edge("E1", "A", "B", "horizontal"),
    edge("E2", "A", "C", "vertical"),
    edge("E3", "B", "D", "vertical"),
    edge("E4", "C", "D", "horizontal"),
]
P1_PUZZLE = {"rows": 3, "cols": 3, "islands": P1_ISLANDS}

# ---- P2 (crossing) ---------------------------------------------------------
P2_ISLANDS = [isl("C", 0, 2, 1), isl("A", 1, 0, 1), isl("B", 1, 4, 1), isl("D", 2, 2, 1)]
P2_EDGES = [
    edge("E1", "C", "D", "vertical"),
    edge("E2", "A", "B", "horizontal"),
]
P2_PUZZLE = {"rows": 3, "cols": 5, "islands": P2_ISLANDS}


def p1(values: List[int]) -> dict:
    return make_solution(values, P1_EDGES)


def p2(values: List[int]) -> dict:
    return make_solution(values, P2_EDGES)


def pair_set(pairs) -> set:
    """Normalise [["E1","E2"], ...] to {frozenset({"E1","E2"})} for order-free comparison."""
    return {frozenset(p) for p in pairs}


def component_set(components) -> set:
    return {frozenset(c) for c in components}
