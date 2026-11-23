"""Shared data contracts. See docs/DATA_MODEL.md (the official reference).

At runtime everything is a plain dict / list. The TypedDicts below are documentation
and type-checking helpers only. Field names are FROZEN once S1-02 is approved.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict

Orientation = Literal["horizontal", "vertical"]
VALID_BRIDGE_VALUES = (0, 1, 2)


class Island(TypedDict):
    id: str
    row: int  # 0-based, grows downward
    col: int  # 0-based, grows to the right
    required_bridges: int


# "from" is a Python keyword, so the functional TypedDict syntax is used.
CandidateBridge = TypedDict(
    "CandidateBridge",
    {"id": str, "from": str, "to": str, "orientation": Orientation},
)


class Puzzle(TypedDict):
    rows: int
    cols: int
    islands: List[Island]


class Solution(TypedDict):
    # edge id -> 0 | 1 | 2 (a missing edge id is treated as 0)
    bridge_counts: Dict[str, int]


class DegreeViolation(TypedDict):
    island: str
    required: int
    actual: int


class InvalidValue(TypedDict):
    edge: str
    value: object


class ValidationReport(TypedDict):
    valid: bool
    degree_violations: List[DegreeViolation]
    crossings: List[List[str]]
    connected_components: int
    invalid_values: List[InvalidValue]


# ---------------------------------------------------------------------------
# S2-01: Algorithm Interface & Standard Result Contract
# Reference: docs/ALGORITHM_INTERFACE.md
# ---------------------------------------------------------------------------

SolverStatus = Literal[
    "SOLVED",
    "UNSATISFIABLE",
    "LIMIT_REACHED",
    "NO_VALID_SOLUTION_FOUND",
    "INVALID_INPUT",
]


class SolverResult(TypedDict):
    status: SolverStatus
    solution: Optional[Solution]
    validation_report: Optional[ValidationReport]
    metrics: Dict[str, Any]

