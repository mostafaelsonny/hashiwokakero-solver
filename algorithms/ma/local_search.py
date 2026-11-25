"""Local Search Neighborhood Operators for Memetic Algorithm (Sprint 2 - S2-09).

This module implements problem-aware local search operators for Hashiwokakero chromosomes:
1. Single Gene Perturbation (explore bridge counts in {0, 1, 2} for candidate bridges).
2. Pairwise Bridge Transfer (transfer a bridge count between incident edges of an island,
   preserving the focal island's degree invariant).
3. Neighborhood Generator (combines operators to generate distinct, valid candidate chromosomes).
4. Local Search Improvement / Hill Climbing (evaluates neighbors for strict fitness improvement).

Conforms strictly to project contracts:
- Chromosome representation & domain {0, 1, 2}: algorithms/ga/chromosome.py (M4)
- Lexicographical multi-objective fitness evaluation: algorithms/ga/fitness.py (M4)
- Pre-computed incident edge and crossing lookups: core/graph_context.py (M2)
- Machine-readable error shape and validation rules: docs/DATA_MODEL.md (Sections 7.2, 8.5, 11.3)
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple

from algorithms.ga.chromosome import VALID_COUNTS, validate_chromosome
from algorithms.ga.fitness import (
    ConflictPairs,
    Fitness,
    build_conflict_pairs,
    evaluate_fitness,
)
from core.graph_context import GraphContext, build_graph_context

if TYPE_CHECKING:
    from core.models import CandidateBridge, Island, Puzzle

VALID_GENES: Tuple[int, ...] = VALID_COUNTS


class InvalidChromosomeError(ValueError):
    """Raised when an input chromosome violates docs/DATA_MODEL.md Section 7.2 / 11.3.

    Contains `invalid_values` structured per Section 8.5:
    [{"path": ..., "value": ..., "reason": ...}]
    """

    def __init__(self, invalid_values: List[dict]):
        self.invalid_values = invalid_values
        super().__init__(f"Invalid chromosome: {invalid_values}")


def find_invalid_values(
    chromosome: List[int], candidate_bridges: List[dict]
) -> List[dict]:
    """Return Section 8.5 entries for every chromosome violation (empty list = legal)."""
    issues: List[dict] = []

    if len(chromosome) != len(candidate_bridges):
        issues.append({
            "path": "chromosome",
            "value": len(chromosome),
            "reason": "chromosome_length_mismatch",
        })

    for i, gene in enumerate(chromosome):
        # type(gene) is int explicitly rejects bool, float, str (no coercion, Section 11.3)
        if type(gene) is not int or gene not in VALID_GENES:
            issues.append({
                "path": f"chromosome[{i}]",
                "value": gene,
                "reason": "chromosome_gene_must_be_integer_0_1_or_2",
            })
    return issues


def validate_local_search_input(
    chromosome: List[int], candidate_bridges: List[dict]
) -> None:
    """Validate chromosome using both shared M4 validator and structured issue reporting."""
    issues = find_invalid_values(chromosome, candidate_bridges)
    if issues:
        raise InvalidChromosomeError(issues)
    # Also verify M4's validate_chromosome contract
    validate_chromosome(chromosome, len(candidate_bridges))


def _islands_in_canonical_order(puzzle: dict) -> List[dict]:
    """Deterministic island order: row ascending, then column ascending (Section 8.2)."""
    return sorted(puzzle["islands"], key=lambda isl: (isl["row"], isl["col"]))


def _actual_degrees(
    chromosome: List[int], candidate_bridges: List[dict]
) -> Dict[str, int]:
    """Compute actual_degree for every island: sum of incident bridge counts (Section 6.3)."""
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
    """Retrieve incident candidate-bridge indices of an island, in candidate-list order.

    Robust to GraphContext getters, direct dict lookups, or legacy mock shapes.
    """
    raw: List = []
    if hasattr(graph_context, "get_incident_edges"):
        raw = graph_context.get_incident_edges(island_id)
    if not raw and hasattr(graph_context, "incident_edges_by_island"):
        raw = graph_context.incident_edges_by_island.get(island_id, [])
    if not raw and hasattr(graph_context, "islands_by_id") and isinstance(graph_context.islands_by_id, dict):
        val = graph_context.islands_by_id.get(island_id)
        if isinstance(val, list):
            raw = val

    indices: List[int] = []
    for edge in raw:
        if isinstance(edge, str):
            if edge not in id_to_index:
                raise ValueError(
                    f"Incident edge {edge!r} of island {island_id!r} is not a known candidate bridge ID"
                )
            idx = id_to_index[edge]
        elif type(edge) is int:
            idx = edge
        else:
            raise ValueError(
                f"Incident edge {edge!r} of island {island_id!r} has invalid type {type(edge).__name__}"
            )

        if not (0 <= idx < n_bridges):
            raise ValueError(
                f"Incident edge {edge!r} of island {island_id!r} is out of range (0..{n_bridges - 1})"
            )
        indices.append(idx)
    return sorted(indices)


def conflict_pairs_from_graph_context(
    graph_context: GraphContext,
) -> ConflictPairs:
    """Derive conflict pairs (i, j) with i < j from GraphContext.crossing_edges_by_index (M2)."""
    pairs: ConflictPairs = []
    crossing_map = getattr(graph_context, "crossing_edges_by_index", {})
    if isinstance(crossing_map, dict):
        for i, crosses in crossing_map.items():
            if isinstance(crosses, list):
                for j in crosses:
                    if i < j:
                        pairs.append((i, j))
    pairs.sort()
    return pairs


# ---------------------------------------------------------------------------
# Operator 1: Single Gene Perturbation
# ---------------------------------------------------------------------------
def single_gene_neighbors(
    chromosome: List[int], gene_index: Optional[int] = None
) -> List[List[int]]:
    """Generate neighboring chromosomes by perturbing gene values to other values in {0, 1, 2}.

    - If `gene_index` is provided: perturbs only that specific gene (safe bounds checked).
    - If `gene_index` is None: perturbs each gene in the chromosome across all positions.
    - Safe bounds check: ensures all generated gene values are strictly in {0, 1, 2}.
    - Never mutates the original chromosome object in-place.
    """
    neighbors: List[List[int]] = []
    indices = [gene_index] if gene_index is not None else list(range(len(chromosome)))

    for i in indices:
        if not (0 <= i < len(chromosome)):
            raise ValueError(f"gene_index {i} is out of range for chromosome length {len(chromosome)}")
        current = chromosome[i]
        for new_val in VALID_GENES:
            if new_val != current:
                neighbor = list(chromosome)
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
    graph_context: Optional[GraphContext] = None,
    only_unbalanced: bool = True,
    focal_island_id: Optional[str] = None,
) -> List[List[int]]:
    """Transfer one bridge count between two incident bridges (E_a, E_b) of a focal island.

    Transfer rules:
    - Decrement count of E_a (requires count > 0), increment count of E_b (requires count < 2).
    - Invariant: Degree of the focal island remains CONSTANT (-1 + 1 = 0).
    - Degrees of the opposite endpoint islands adjust by -1 and +1.
    - If `only_unbalanced=True`: only islands where actual_degree != required_bridges are selected.
    - If `focal_island_id` is specified: only transfers incident to that island are generated.
    - Never mutates the original chromosome object in-place.
    """
    if graph_context is None:
        graph_context = build_graph_context(puzzle, candidate_bridges)

    n = len(candidate_bridges)
    id_to_index = {b["id"]: i for i, b in enumerate(candidate_bridges)}
    degrees = _actual_degrees(chromosome, candidate_bridges)
    neighbors: List[List[int]] = []

    islands = _islands_in_canonical_order(puzzle)
    if focal_island_id is not None:
        islands = [isl for isl in islands if isl["id"] == focal_island_id]
        if not islands:
            raise ValueError(f"focal_island_id {focal_island_id!r} not found in puzzle islands")

    for island in islands:
        island_id = island["id"]
        # Skip balanced islands when only_unbalanced is requested
        if only_unbalanced and degrees.get(island_id, 0) == island["required_bridges"]:
            continue

        incident = _incident_indices(graph_context, island_id, id_to_index, n)
        if len(incident) < 2:
            continue

        for x in range(len(incident)):
            for y in range(x + 1, len(incident)):
                a, b = incident[x], incident[y]

                # Transfer a -> b (decrement a, increment b)
                if chromosome[a] > 0 and chromosome[b] < 2:
                    neighbor = list(chromosome)
                    neighbor[a] -= 1
                    neighbor[b] += 1
                    neighbors.append(neighbor)

                # Transfer b -> a (decrement b, increment a)
                if chromosome[b] > 0 and chromosome[a] < 2:
                    neighbor = list(chromosome)
                    neighbor[b] -= 1
                    neighbor[a] += 1
                    neighbors.append(neighbor)

    return neighbors


# ---------------------------------------------------------------------------
# Neighborhood Generator
# ---------------------------------------------------------------------------
def generate_neighbors(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    graph_context: Optional[GraphContext] = None,
    only_unbalanced: bool = True,
) -> List[List[int]]:
    """Generate all distinct legal neighboring candidate chromosomes.

    Combines:
    - Operator 1: Single Gene Perturbation
    - Operator 2: Pairwise Bridge Transfer

    Guarantees:
    - Validates input chromosome strictly; raises InvalidChromosomeError on violations.
    - Every generated neighbor is a legal chromosome (correct length, valid gene domain {0, 1, 2}).
    - Never mutates the original chromosome object in-place.
    - Excludes the input chromosome itself and eliminates duplicates deterministically.
    """
    validate_local_search_input(chromosome, candidate_bridges)

    if graph_context is None:
        graph_context = build_graph_context(puzzle, candidate_bridges)

    seen: Set[Tuple[int, ...]] = {tuple(chromosome)}
    neighbors: List[List[int]] = []

    candidates = single_gene_neighbors(chromosome) + pairwise_transfer_neighbors(
        chromosome, puzzle, candidate_bridges, graph_context, only_unbalanced=only_unbalanced
    )

    for neighbor in candidates:
        key = tuple(neighbor)
        if key not in seen:
            seen.add(key)
            # Safe validation guarantee
            validate_chromosome(neighbor, len(candidate_bridges))
            neighbors.append(neighbor)

    return neighbors


# ---------------------------------------------------------------------------
# Fitness Evaluation and Local Search Improvement (Hill Climbing)
# ---------------------------------------------------------------------------
def evaluate_chromosome(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    conflicts: Optional[ConflictPairs] = None,
    graph_context: Optional[GraphContext] = None,
) -> Fitness:
    """Evaluate chromosome fitness returning (degree_error, crossing_count, connectivity_penalty).

    Uses M4's evaluate_fitness function and leverages M2's pre-computed crossings from GraphContext.
    """
    if conflicts is None and graph_context is not None:
        conflicts = conflict_pairs_from_graph_context(graph_context)
    if conflicts is None:
        conflicts = build_conflict_pairs(puzzle, candidate_bridges)

    return evaluate_fitness(chromosome, puzzle, candidate_bridges, conflicts=conflicts)


def best_improving_neighbor(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    graph_context: Optional[GraphContext] = None,
    conflicts: Optional[ConflictPairs] = None,
    only_unbalanced: bool = True,
) -> Optional[Tuple[List[int], Fitness]]:
    """Find the neighbor with strictly better (lexicographically lower) fitness than current.

    Returns (best_neighbor, best_fitness) if a strict improvement exists, otherwise None.
    """
    if graph_context is None:
        graph_context = build_graph_context(puzzle, candidate_bridges)
    if conflicts is None:
        conflicts = conflict_pairs_from_graph_context(graph_context)

    current_fitness = evaluate_chromosome(
        chromosome, puzzle, candidate_bridges, conflicts=conflicts, graph_context=graph_context
    )

    neighbors = generate_neighbors(
        chromosome, puzzle, candidate_bridges, graph_context, only_unbalanced=only_unbalanced
    )

    best_candidate: Optional[List[int]] = None
    best_candidate_fitness: Fitness = current_fitness

    for nb in neighbors:
        nb_fitness = evaluate_chromosome(
            nb, puzzle, candidate_bridges, conflicts=conflicts, graph_context=graph_context
        )
        if nb_fitness < best_candidate_fitness:  # strictly better
            best_candidate_fitness = nb_fitness
            best_candidate = nb

    if best_candidate is not None:
        return (best_candidate, best_candidate_fitness)
    return None


def hill_climb(
    chromosome: List[int],
    puzzle: dict,
    candidate_bridges: List[dict],
    graph_context: Optional[GraphContext] = None,
    max_steps: int = 50,
    only_unbalanced: bool = True,
) -> Tuple[List[int], dict]:
    """Execute problem-aware Hill Climbing local search on an individual chromosome.

    Contract:
    - Never accepts a worse or equal fitness move (strictly improving).
    - Stops when no neighbor strictly improves fitness (local optimum) or max_steps is reached.
    - Returns (improved_chromosome, stats_dict).
    """
    if graph_context is None:
        graph_context = build_graph_context(puzzle, candidate_bridges)
    conflicts = conflict_pairs_from_graph_context(graph_context)

    current = list(chromosome)
    initial_fitness = evaluate_chromosome(
        current, puzzle, candidate_bridges, conflicts=conflicts, graph_context=graph_context
    )
    current_fitness = initial_fitness

    steps = 0
    improvements = 0

    while steps < max_steps:
        steps += 1
        result = best_improving_neighbor(
            current,
            puzzle,
            candidate_bridges,
            graph_context=graph_context,
            conflicts=conflicts,
            only_unbalanced=only_unbalanced,
        )
        if result is None:
            # Reached local optimum
            break

        current, current_fitness = result
        improvements += 1
        if current_fitness == (0, 0, 0):
            # Target fitness reached
            break

    stats = {
        "steps": steps,
        "improvements": improvements,
        "initial_fitness": list(initial_fitness),
        "final_fitness": list(current_fitness),
        "improved": improvements > 0,
    }
    return current, stats
