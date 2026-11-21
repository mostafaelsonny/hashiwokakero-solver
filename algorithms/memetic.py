"""Sprint 3 - Memetic Algorithm = GA + Local Search. Design: docs/MA_DESIGN.md (S1-10)."""
"""
algorithms/ma/local_search.py
Local-search neighborhood operators for the Memetic Algorithm.

Conforms to docs/DATA_MODEL.md (FROZEN):
  - chromosome[i] <-> candidate_bridges[i]   (Section 7.2)
  - genes are integers in {0, 1, 2}          (Section 7.2)
  - candidate_bridges is NEVER re-sorted / filtered / re-indexed (Section 5.4)
  - invalid values are reported, never coerced or clamped (Section 8.5)
"""
from typing import Dict, List, Set, Tuple

from core.graph_context import GraphContext

VALID_GENES = (0, 1, 2)


class InvalidChromosomeError(ValueError):
    """Raised when the input chromosome violates Section 7.2 / 11.3.

    `invalid_values` uses the exact entry shape of Section 8.5:
    {"path": ..., "value": ..., "reason": ...}
    """

    def __init__(self, invalid_values: List[dict]):
        self.invalid_values = invalid_values
        super().__init__(f"Invalid chromosome: {invalid_values}")


def find_invalid_values(
    chromosome: List[int], candidate_bridges: List[dict]
) -> List[dict]:
    """Return Section 8.5 entries for every violation (empty list = legal)."""
    issues: List[dict] = []

    if len(chromosome) != len(candidate_bridges):
        issues.append({
            "path": "chromosome",
            "value": len(chromosome),
            "reason": "chromosome_length_mismatch",
        })

    for i, gene in enumerate(chromosome):
        # `type(...) is int` rejects bool, "2", 2.5 (no coercion, Section 11.3)
        if type(gene) is not int or gene not in VALID_GENES:
            issues.append({
                "path": f"chromosome[{i}]",
                "value": gene,
                "reason": "chromosome_gene_must_be_integer_0_1_or_2",
            })
    return issues


def _islands_in_canonical_order(puzzle: dict) -> List[dict]:
    """Deterministic island order: row asc, then col asc (Section 8.2)."""
    return sorted(puzzle["islands"], key=lambda isl: (isl["row"], isl["col"]))


def _actual_degrees(
    chromosome: List[int], candidate_bridges: List[dict]
) -> Dict[str, int]:
    """actual_degree(island) = sum of counts of incident bridges (Section 6.3)."""
    degrees: Dict[str, int] = {}
    for i, bridge in enumerate(candidate_bridges):
        count = chromosome[i]
        degrees[bridge["from"]] = degrees.get(bridge["from"], 0) + count
        degrees[bridge["to"]] = degrees.get(bridge["to"], 0) + count
    return degrees


def _incident_indices(
    graph_context: GraphContext,
    island_id: str,
    id_to_index: Dict[str, int],
    n_bridges: int,
) -> List[int]:
    """Incident candidate-bridge INDICES of an island, in candidate-list order.

    Accepts graph_context storing either indices (int) or bridge IDs ("E3").
    """
    raw = graph_context.incident_edges_by_island.get(island_id, [])
    indices = []
    for edge in raw:
        if isinstance(edge, str):
            if edge not in id_to_index:
                raise ValueError(
                    f"Incident edge {edge!r} of island {island_id!r} is not a known candidate bridge ID"
                )
            idx = id_to_index[edge]
        else:
            idx = edge
        if not (0 <= idx < n_bridges):
            raise ValueError(f"Incident edge {edge!r} of island {island_id!r} is out of range")
        indices.append(idx)
    return sorted(indices)


# ---------------------------------------------------------------------------
# Operator 1: Single Gene Perturbation
# ---------------------------------------------------------------------------
def single_gene_neighbors(chromosome: List[int]) -> List[List[int]]:
    """Change one gene at a time to every other value in {0, 1, 2}."""
    neighbors: List[List[int]] = []
    for i, current in enumerate(chromosome):
        for new_val in VALID_GENES:
            if new_val != current:
                neighbor = list(chromosome)  # never mutate the original
                neighbor[i] = new_val
                neighbors.append(neighbor)
    return neighbors


# ---------------------------------------------------------------------------
# Operator 2: Pairwise Bridge Transfer
# ---------------------------------------------------------------------------
def pairwise_transfer_neighbors(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    graph_context: GraphContext,
    only_unbalanced: bool = True,
) -> List[List[int]]:
    """For a focal island, move one bridge from incident edge E_a to E_b.

    Focal island degree is unchanged (-1 + 1); the opposite endpoints change.
    With only_unbalanced=True only islands where
    actual_degree != required_bridges are used as focal islands.
    """
    n = len(candidate_bridges)
    id_to_index = {b["id"]: i for i, b in enumerate(candidate_bridges)}
    degrees = _actual_degrees(chromosome, candidate_bridges)
    neighbors: List[List[int]] = []

    for island in _islands_in_canonical_order(puzzle):
        island_id = island["id"]
        if only_unbalanced and degrees.get(island_id, 0) == island["required_bridges"]:
            continue

        incident = _incident_indices(graph_context, island_id, id_to_index, n)
        for x in range(len(incident)):
            for y in range(x + 1, len(incident)):
                a, b = incident[x], incident[y]

                if chromosome[a] > 0 and chromosome[b] < 2:   # a -> b
                    neighbor = list(chromosome)
                    neighbor[a] -= 1
                    neighbor[b] += 1
                    neighbors.append(neighbor)

                if chromosome[b] > 0 and chromosome[a] < 2:   # b -> a
                    neighbor = list(chromosome)
                    neighbor[b] -= 1
                    neighbor[a] += 1
                    neighbors.append(neighbor)
    return neighbors


# ---------------------------------------------------------------------------
# Neighborhood generator
# ---------------------------------------------------------------------------
def generate_neighbors(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    graph_context: GraphContext,
    only_unbalanced: bool = True,
) -> List[List[int]]:
    """All distinct legal neighbors of `chromosome`.

    - Original chromosome, puzzle and candidate_bridges are never modified.
    - Every neighbor has len == len(candidate_bridges) and genes in {0,1,2}.
    - Raises InvalidChromosomeError (with Section 8.5 entries) on illegal input.
    """
    issues = find_invalid_values(chromosome, candidate_bridges)
    if issues:
        raise InvalidChromosomeError(issues)

    seen: Set[Tuple[int, ...]] = {tuple(chromosome)}
    neighbors: List[List[int]] = []

    candidates = single_gene_neighbors(chromosome) + pairwise_transfer_neighbors(
        chromosome, puzzle, candidate_bridges, graph_context, only_unbalanced
    )
    for neighbor in candidates:
        key = tuple(neighbor)
        if key not in seen:
            seen.add(key)
            neighbors.append(neighbor)
    return neighbors

