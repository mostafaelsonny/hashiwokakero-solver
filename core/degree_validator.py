"""S1-04 - Degree Validator.  Owner: Ebrahim.  Reviewer: Mostafa.

Spec: docs/VALIDATOR_SPEC.md
"""
from __future__ import annotations

from typing import Dict, List

from core.models import CandidateBridge, DegreeViolation, Island, Solution


def compute_degrees(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> Dict[str, int]:
    """Return {island_id: actual number of bridges touching the island}.

    A double bridge (count 2) counts 2 for BOTH of its islands. Missing edge ids
    count as 0. Raise ValueError if a bridge value is not 0, 1 or 2.
    """
    raise NotImplementedError("S1-04 not implemented yet (owner: Ebrahim)")


def check_degrees(
    islands: List[Island],
    edges: List[CandidateBridge],
    solution: Solution,
    mode: str,
) -> List[DegreeViolation]:
    """Return a list of {island, required, actual}. Empty list = no problems.

    mode="partial": violation only when actual > required (used DURING search).
    mode="final"  : violation whenever actual != required (used on a finished solution).
    Raise ValueError for any other mode.
    """
    raise NotImplementedError("S1-04 not implemented yet (owner: Ebrahim)")
