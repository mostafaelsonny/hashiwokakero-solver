"""S1-06 - Connectivity Checker.  Owner: Ebrahim.  Reviewer: Mostafa.

Spec: docs/VALIDATOR_SPEC.md   (BFS or DFS over ACTUAL bridges only: count > 0)
"""
from __future__ import annotations

from typing import List

from core.models import CandidateBridge, Island, Solution


def find_connected_components(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> List[List[str]]:
    """Return the connected components as lists of island ids.

    Only edges with a bridge count > 0 connect islands (a candidate edge with 0 does not).
    An island with no bridge is its own component. Output order must be deterministic.
    """
    raise NotImplementedError("S1-06 not implemented yet (owner: Ebrahim)")


def is_connected(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> bool:
    """True when there is exactly one component."""
    raise NotImplementedError("S1-06 not implemented yet (owner: Ebrahim)")
