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
    degrees: Dict[str, int] = {isl["id"]: 0 for isl in islands}

    for e in edges:
        count = solution["bridge_counts"].get(e["id"], 0)
        if count not in (0, 1, 2):
            raise ValueError(
                f"Invalid bridge value {count!r} for edge {e['id']!r}. Must be 0, 1, or 2."
            )
        degrees[e["from"]] += count
        degrees[e["to"]] += count

    return degrees


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
    if mode not in ("partial", "final"):
        raise ValueError(f"Unknown mode: {mode!r}. Expected 'partial' or 'final'.")

    degrees = compute_degrees(islands, edges, solution)
    violations: List[DegreeViolation] = []

    for isl in islands:
        actual = degrees[isl["id"]]
        required = isl["required_bridges"]

        if mode == "partial" and actual > required:
            violations.append({"island": isl["id"], "required": required, "actual": actual})
        elif mode == "final" and actual != required:
            violations.append({"island": isl["id"], "required": required, "actual": actual})

    return sorted(violations, key=lambda v: v["island"])
