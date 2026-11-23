"""GA / MA shared fitness evaluation (S2-06).

fitness = (degree_error, crossing_count, connectivity_penalty)
  * degree_error          = sum over islands of |required_bridges - actual_degree|
  * crossing_count        = number of crossing candidate pairs with BOTH counts > 0
  * connectivity_penalty  = max(0, connected_components - 1)

Optimal fitness is (0, 0, 0); tuples are compared lexicographically (lower is better).
(0, 0, 0) is a necessary signal only: final validity is confirmed by validate_solution.

Field names follow docs/DATA_MODEL.md: island {id, row, col, required_bridges},
candidate bridge {id, from, to, orientation}.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from algorithms.ga.chromosome import validate_chromosome

if TYPE_CHECKING:  # type hints only
    from core.models import CandidateBridge, Puzzle

ConflictPairs = List[Tuple[int, int]]
Fitness = Tuple[int, int, int]


def build_conflict_pairs(
    puzzle: "Puzzle", candidate_bridges: List["CandidateBridge"]
) -> ConflictPairs:
    """Return every pair (i, j), i < j, of candidate INDICES that geometrically cross.

    A horizontal (row r, cols c1..c2) and a vertical (col c, rows r1..r2) candidate
    cross when r1 < r < r2 and c1 < c < c2 (strict: touching at endpoints is not a
    crossing, DATA_MODEL 8.3). The result depends only on the puzzle and the
    canonical candidate order, so compute it once per puzzle and reuse it.
    """
    coords = {isl["id"]: (isl["row"], isl["col"]) for isl in puzzle.get("islands", [])}

    horizontals = []  # (candidate_index, row, col_start, col_end)
    verticals = []    # (candidate_index, col, row_start, row_end)
    for idx, bridge in enumerate(candidate_bridges):
        start = coords.get(bridge["from"])
        end = coords.get(bridge["to"])
        if start is None or end is None:
            raise ValueError(
                f"unknown_island_id: candidate {bridge['id']} references "
                f"{bridge['from']!r} or {bridge['to']!r}"
            )
        orientation = bridge["orientation"]
        if orientation == "horizontal":
            horizontals.append((idx, start[0], min(start[1], end[1]), max(start[1], end[1])))
        elif orientation == "vertical":
            verticals.append((idx, start[1], min(start[0], end[0]), max(start[0], end[0])))
        else:
            raise ValueError(
                f"invalid_orientation: candidate {bridge['id']} has {orientation!r}"
            )

    pairs: ConflictPairs = []
    for h_idx, row, c1, c2 in horizontals:
        for v_idx, col, r1, r2 in verticals:
            if c1 < col < c2 and r1 < row < r2:
                pairs.append((min(h_idx, v_idx), max(h_idx, v_idx)))
    pairs.sort()
    return pairs


def evaluate_fitness(
    chromosome: List[int],
    puzzle: "Puzzle",
    candidate_bridges: List["CandidateBridge"],
    conflicts: Optional[ConflictPairs] = None,
) -> Fitness:
    """Return (degree_error, crossing_count, connectivity_penalty) for a chromosome.

    `conflicts` is optional: pass build_conflict_pairs(puzzle, candidate_bridges)
    (computed once per puzzle) to avoid recomputing the geometry on every call.
    Without it the result is identical, just slower.

    Raises ValueError for an invalid chromosome or a bridge that references an
    island missing from the puzzle (solvers must catch it, Interface 2.5).
    """
    validate_chromosome(chromosome, len(candidate_bridges))

    islands = puzzle.get("islands", [])
    degrees: Dict[str, int] = {isl["id"]: 0 for isl in islands}

    # Union-find over islands: every island is a vertex, even with no bridge.
    parent: Dict[str, str] = {island_id: island_id for island_id in degrees}
    components = len(degrees)

    def find(node: str) -> str:
        root = node
        while parent[root] != root:
            root = parent[root]
        while parent[node] != root:  # path compression
            parent[node], node = root, parent[node]
        return root

    for gene, bridge in zip(chromosome, candidate_bridges):
        if gene == 0:
            continue
        a, b = bridge["from"], bridge["to"]
        if a not in degrees or b not in degrees:
            raise ValueError(
                f"unknown_island_id: candidate {bridge['id']} references "
                f"{a!r} or {b!r}"
            )
        degrees[a] += gene
        degrees[b] += gene
        root_a, root_b = find(a), find(b)
        if root_a != root_b:  # a double bridge (gene 2) is still ONE adjacency
            parent[root_a] = root_b
            components -= 1

    degree_error = sum(abs(isl["required_bridges"] - degrees[isl["id"]]) for isl in islands)

    if conflicts is None:
        conflicts = build_conflict_pairs(puzzle, candidate_bridges)
    crossing_count = sum(1 for i, j in conflicts if chromosome[i] > 0 and chromosome[j] > 0)

    connectivity_penalty = max(0, components - 1)
    return (degree_error, crossing_count, connectivity_penalty)