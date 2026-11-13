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
    # Step 1: Sort islands by row, then by column
    sorted_islands = sorted(
        islands,
        key=lambda island: (island["row"], island["col"])
    )

    # Step 2: Prepare the result and edge counter
    edges: List[CandidateBridge] = []
    edge_counter = 1

    # Step 3: Process islands in sorted order
    for current in sorted_islands:

        # Step 4: Find the nearest island to the RIGHT
        right_candidates = [
            candidate
            for candidate in sorted_islands
            if candidate["row"] == current["row"]
            and candidate["col"] > current["col"]
        ]

        if right_candidates:
            nearest_right = min(
                right_candidates,
                key=lambda island: island["col"]
            )

            edges.append({
                "id": f"E{edge_counter}",
                "from": current["id"],
                "to": nearest_right["id"],
                "orientation": "horizontal"
            })

            edge_counter += 1

        # Step 5: Find the nearest island BELOW
        bottom_candidates = [
            candidate
            for candidate in sorted_islands
            if candidate["col"] == current["col"]
            and candidate["row"] > current["row"]
        ]

        if bottom_candidates:
            nearest_bottom = min(
                bottom_candidates,
                key=lambda island: island["row"]
            )

            edges.append({
                "id": f"E{edge_counter}",
                "from": current["id"],
                "to": nearest_bottom["id"],
                "orientation": "vertical"
            })

            edge_counter += 1
    # Step 6: Return all candidate edges
    return edges
