"""S1-03 - Candidate Edge Generator.  Owner: Monzer.  Reviewer: Mostafa.

Spec: docs/CANDIDATE_EDGES_SPEC.md   Task list: docs/SPRINT_PLAN.md
"""
from __future__ import annotations

from typing import List

from core.models import CandidateBridge, Island


def generate_candidate_edges(islands: List[Island]) -> List[CandidateBridge]:
    """Return every possible bridge between NEAREST islands in the same row/column.

    Contract (must match docs/DATA_MODEL.md):
      * Only horizontal or vertical links between the nearest island to the right
        (same row) / below (same column). Never link over another island.
      * Each island pair appears once (no A->B and B->A).
      * Deterministic order: sort islands by (row, col); for each island in that
        order add its RIGHT edge first, then its DOWN edge. Ids are E1, E2, ...
      * `from` = top/left island, `to` = bottom/right island.
      * Same islands in any input order must give identical ids.
    """
    raise NotImplementedError("S1-03 not implemented yet (owner: Monzer)")
