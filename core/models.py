"""Shared data contracts. See docs/DATA_MODEL.md (the official reference).

At runtime everything is a plain dict / list. The TypedDicts below are documentation
and type-checking helpers only. Field names are FROZEN once S1-02 is approved.
"""
from __future__ import annotations

from typing import Dict, List, Literal, TypedDict

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
